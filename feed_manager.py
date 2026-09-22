"""
Feed Manager module for the Cybersecurity News Dashboard.
Handles fetching, parsing, and processing of RSS feeds and web content.
Applies priority scoring and classification to each news item.
"""

import re
import logging
import hashlib
from datetime import datetime
from urllib.parse import urlparse

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from config import HACKING_INCIDENT_KEYWORDS, CVE_PATTERN, CVE_VENDOR_KEYWORDS
from database import (
    get_sources, insert_news, update_source_fetch_status,
    get_priority_rules, increment_rule_hit, get_setting
)
from logger_config import feed_logger as logger

# Request timeout and headers
REQUEST_TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (compatible; CyberSecNewsDashboard/1.0; "
    "+https://github.com/cybersec-news-dashboard)"
)


def fetch_all_feeds():
    """
    Fetch all enabled feed sources and store new articles.
    Returns a summary dict with counts.
    """
    sources = get_sources(include_disabled=False)
    total_new = 0
    total_errors = 0
    total_processed = 0

    for source in sources:
        try:
            articles = fetch_single_feed(source)
            total_processed += len(articles)
            for article in articles:
                if insert_news(article):
                    total_new += 1
            update_source_fetch_status(source['id'])
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {e}")
            update_source_fetch_status(source['id'], error=str(e))
            total_errors += 1

    return {
        'sources_processed': len(sources),
        'articles_processed': total_processed,
        'new_articles': total_new,
        'errors': total_errors,
        'timestamp': datetime.utcnow().isoformat()
    }


def fetch_single_feed(source):
    """
    Fetch and parse a single feed source.
    Returns a list of processed article dicts ready for database insertion.
    """
    feed_type = source.get('feed_type', 'rss')

    if feed_type == 'rss':
        return _parse_rss_feed(source)
    elif feed_type == 'web_scrape':
        return _scrape_web_page(source)
    else:
        return _parse_rss_feed(source)


def _parse_rss_feed(source):
    """Parse an RSS/Atom feed and return processed articles."""
    articles = []
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(source['url'], headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        for entry in feed.entries[:50]:
            article = _process_feed_entry(entry, source)
            if article:
                articles.append(article)
    except Exception as e:
        logger.error(f"RSS parse error for {source['name']}: {e}")
        raise

    return articles


def _scrape_web_page(source):
    """Scrape a web page for articles (basic implementation)."""
    articles = []
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(source['url'], headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        for link in soup.find_all('a', href=True):
            title = link.get_text(strip=True)
            href = link['href']
            if title and len(title) > 20 and _is_security_relevant(title):
                if not href.startswith('http'):
                    parsed = urlparse(source['url'])
                    href = f"{parsed.scheme}://{parsed.netloc}{href}"

                article = {
                    'title': title[:500],
                    'url': href,
                    'summary': title,
                    'content': '',
                    'source_id': source['id'],
                    'category': source.get('category', 'web_news'),
                    'region': source.get('region', 'global'),
                    'published_date': datetime.utcnow().isoformat(),
                    'tags': '',
                    'image_url': '',
                }
                article = _apply_classification(article)
                articles.append(article)
    except Exception as e:
        logger.error(f"Scrape error for {source['name']}: {e}")
        raise

    return articles


def _process_feed_entry(entry, source):
    """Process a single feed entry into a standardized article dict."""
    title = entry.get('title', '').strip()
    if not title:
        return None

    link = entry.get('link', '')
    if not link:
        links = entry.get('links', [])
        if links:
            link = links[0].get('href', '')
    if not link:
        return None

    summary = ''
    if hasattr(entry, 'summary'):
        soup = BeautifulSoup(entry.summary, 'lxml')
        summary = soup.get_text(strip=True)[:1000]
    elif hasattr(entry, 'description'):
        soup = BeautifulSoup(entry.description, 'lxml')
        summary = soup.get_text(strip=True)[:1000]

    content = ''
    if hasattr(entry, 'content'):
        for c in entry.content:
            soup = BeautifulSoup(c.get('value', ''), 'lxml')
            content += soup.get_text(strip=True)
        content = content[:5000]

    published_date = ''
    if hasattr(entry, 'published'):
        try:
            published_date = dateparser.parse(entry.published).isoformat()
        except Exception:
            published_date = datetime.utcnow().isoformat()
    elif hasattr(entry, 'updated'):
        try:
            published_date = dateparser.parse(entry.updated).isoformat()
        except Exception:
            published_date = datetime.utcnow().isoformat()
    else:
        published_date = datetime.utcnow().isoformat()

    tags = ''
    if hasattr(entry, 'tags'):
        tags = ','.join(t.get('term', '') for t in entry.tags if t.get('term'))

    image_url = ''
    if hasattr(entry, 'media_content'):
        for media in entry.media_content:
            if 'image' in media.get('type', ''):
                image_url = media.get('url', '')
                break
    if not image_url and hasattr(entry, 'media_thumbnail'):
        for thumb in entry.media_thumbnail:
            image_url = thumb.get('url', '')
            break

    article = {
        'title': title[:500],
        'url': link,
        'summary': summary,
        'content': content,
        'source_id': source['id'],
        'category': source.get('category', 'web_news'),
        'region': source.get('region', 'global'),
        'published_date': published_date,
        'tags': tags,
        'image_url': image_url,
    }

    article = _apply_classification(article)
    return article


def _apply_classification(article):
    """
    Apply priority scoring and classification to an article.
    Checks for hacking incidents, CVEs, and matches priority rules.
    """
    text = f"{article['title']} {article['summary']} {article.get('content', '')}".lower()

    # Check for hacking incidents
    is_hacking = any(kw.lower() in text for kw in HACKING_INCIDENT_KEYWORDS)
    article['is_hacking_incident'] = is_hacking

    # Check for CVEs
    cve_matches = re.findall(CVE_PATTERN, text, re.IGNORECASE)
    article['has_cve'] = len(cve_matches) > 0
    article['cve_ids'] = ','.join(set(cve_matches)) if cve_matches else ''

    # Check CVE vendor associations
    matched_vendors = []
    for vendor, keywords in CVE_VENDOR_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            matched_vendors.append(vendor)
    article['cve_vendors'] = ','.join(matched_vendors)

    # Apply priority scoring from rules
    priority_score = 0
    priority_label = 'low'
    rules = get_priority_rules()

    for rule in rules:
        if rule['keyword'].lower() in text:
            if rule['score'] > priority_score:
                priority_score = rule['score']
                priority_label = rule['level']
            try:
                increment_rule_hit(rule['id'])
            except Exception:
                pass

    # Hacking incidents always get top priority
    hacking_top = get_setting('hacking_always_top', '1')
    if is_hacking and hacking_top == '1':
        priority_score = max(priority_score, 100)
        priority_label = 'critical'

    # CVE-related news gets at least high priority
    if article['has_cve'] and priority_score < 75:
        priority_score = 75
        priority_label = 'high'

    article['priority_score'] = priority_score
    article['priority_label'] = priority_label

    # Auto-detect category if source category is generic
    if article.get('category') in ('web_news', 'blog'):
        if is_hacking:
            article['category'] = 'hacking_incident'
        elif article['has_cve']:
            article['category'] = 'cve'

    return article


def _is_security_relevant(text):
    """Check if text is likely security-related (for web scraping filtering)."""
    security_terms = [
        'security', 'vulnerability', 'exploit', 'hack', 'breach',
        'malware', 'ransomware', 'phishing', 'CVE', 'threat',
        'cyber', 'attack', 'patch', 'zero-day', 'backdoor',
        'botnet', 'DDoS', 'encryption', 'firewall'
    ]
    text_lower = text.lower()
    return any(term.lower() in text_lower for term in security_terms)
