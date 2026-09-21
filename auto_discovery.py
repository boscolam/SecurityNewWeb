"""
Auto-Discovery module for the Cybersecurity News Dashboard.
Automatically discovers new cybersecurity RSS feeds by:
1. Checking known aggregator sites for new feeds
2. Searching for RSS links in existing news articles
3. Maintaining a list of discovered feeds for user approval
"""

import re
import logging
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from database import add_discovered_feed, get_sources

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (compatible; CyberSecNewsDashboard/1.0; "
    "+https://github.com/cybersec-news-dashboard)"
)
REQUEST_TIMEOUT = 20

# Known cybersecurity aggregator pages that list multiple feeds or blogs
DISCOVERY_SOURCES = [
    {
        "url": "https://www.reddit.com/r/cybersecurity/wiki/resources",
        "name": "Reddit Cybersecurity Resources"
    },
    {
        "url": "https://github.com/topics/cybersecurity-feeds",
        "name": "GitHub Cybersecurity Feeds"
    },
    {
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories",
        "name": "CISA Advisories Page"
    },
]

# Common RSS feed URL patterns for security sites
RSS_PATTERNS = [
    '/feed/', '/feed', '/rss', '/rss.xml', '/atom.xml',
    '/feeds/posts/default', '/blog/feed/', '/feed/rss/',
    '/index.xml', '/blog/rss', '/rss/news/'
]


def run_feed_discovery():
    """
    Main discovery function. Runs daily to find new cybersecurity feeds.
    Returns a summary of discovered feeds.
    """
    logger.info("Starting automatic feed discovery...")
    existing_sources = get_sources()
    existing_urls = {s['url'] for s in existing_sources}
    discovered_count = 0

    # Method 1: Look for RSS links in aggregator pages
    for source in DISCOVERY_SOURCES:
        try:
            feeds = _discover_from_page(source['url'], existing_urls)
            for feed in feeds:
                feed['discovered_from'] = source['name']
                if add_discovered_feed(feed):
                    discovered_count += 1
        except Exception as e:
            logger.error(f"Discovery error for {source['name']}: {e}")

    # Method 2: Check existing source pages for linked feeds
    for source in existing_sources[:20]:
        try:
            feeds = _discover_linked_feeds(source['url'], existing_urls)
            for feed in feeds:
                feed['discovered_from'] = f"Linked from {source['name']}"
                if add_discovered_feed(feed):
                    discovered_count += 1
        except Exception as e:
            logger.debug(f"Linked feed discovery error for {source['name']}: {e}")

    logger.info(f"Feed discovery complete. Found {discovered_count} new feeds.")
    return {'discovered': discovered_count}


def _discover_from_page(url, existing_urls):
    """Discover RSS feeds from a web page."""
    feeds = []
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Look for RSS/Atom link elements
        rss_links = soup.find_all('link', type=re.compile(r'(rss|atom|xml)'))
        for link in rss_links:
            href = link.get('href', '')
            if href and href not in existing_urls:
                title = link.get('title', urlparse(href).netloc)
                feeds.append({
                    'name': title,
                    'url': urljoin(url, href),
                    'category': 'web_news',
                    'region': 'global'
                })

        # Look for anchor tags pointing to RSS-like URLs
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            if any(pattern in href.lower() for pattern in ['/rss', '/feed', 'atom.xml', '.rss']):
                full_url = urljoin(url, href)
                if full_url not in existing_urls and _is_security_domain(full_url):
                    feeds.append({
                        'name': text or urlparse(full_url).netloc,
                        'url': full_url,
                        'category': _guess_category(text, full_url),
                        'region': 'global'
                    })
    except Exception as e:
        logger.debug(f"Page discovery error for {url}: {e}")

    return feeds[:20]


def _discover_linked_feeds(source_url, existing_urls):
    """Try common RSS paths on the domain of an existing source."""
    feeds = []
    parsed = urlparse(source_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    for pattern in RSS_PATTERNS:
        test_url = base_url + pattern
        if test_url in existing_urls or test_url == source_url:
            continue
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.head(
                test_url, headers=headers, timeout=10, allow_redirects=True
            )
            content_type = response.headers.get('content-type', '')
            if response.status_code == 200 and any(
                t in content_type for t in ['xml', 'rss', 'atom', 'text']
            ):
                feeds.append({
                    'name': f"{parsed.netloc} - {pattern.strip('/')}",
                    'url': test_url,
                    'category': 'web_news',
                    'region': 'global'
                })
                break
        except Exception:
            continue

    return feeds


def _is_security_domain(url):
    """Check if a URL likely belongs to a cybersecurity domain."""
    security_domains = [
        'security', 'cyber', 'threat', 'hack', 'vuln', 'exploit',
        'malware', 'infosec', 'cve', 'cert', 'csirt', 'soc',
        'firewall', 'antivirus', 'endpoint', 'detection',
    ]
    url_lower = url.lower()
    return any(term in url_lower for term in security_domains)


def _guess_category(text, url):
    """Guess the feed category based on text and URL."""
    combined = f"{text} {url}".lower()
    if any(w in combined for w in ['cve', 'advisory', 'vulnerability', 'cert']):
        return 'cve'
    elif any(w in combined for w in ['research', 'lab', 'threat', 'intel', 'unit42', 'talos']):
        return 'vendor_research'
    elif any(w in combined for w in ['dark', 'underground', 'onion']):
        return 'darkweb'
    elif any(w in combined for w in ['blog', 'medium', 'personal']):
        return 'blog'
    return 'web_news'
