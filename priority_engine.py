"""
Priority Engine module for the Cybersecurity News Dashboard.
Handles automatic daily analysis of priority rules at 24:00 (midnight).
Analyzes which keywords appear most in high-importance news and adjusts
priority rules accordingly. Users can review and edit the updated rules.
"""

import logging
from datetime import datetime, timedelta
from collections import Counter

from database import (
    get_db, get_priority_rules, add_priority_rule,
    update_priority_rule, log_priority_analysis
)

logger = logging.getLogger(__name__)


def run_daily_priority_analysis():
    """
    Run the daily priority analysis at midnight.
    This function:
    1. Analyzes recent news articles to find frequently appearing keywords
    2. Identifies patterns in high-priority (hacking) news
    3. Suggests new priority rules or adjusts existing ones
    4. Logs the analysis for user review
    """
    logger.info("Starting daily priority analysis...")

    conn = get_db()
    rules_added = 0
    rules_modified = 0
    rules_removed = 0
    summary_parts = []

    try:
        # Get news from last 7 days for analysis
        week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
        recent_news = conn.execute('''
            SELECT title, summary, content, priority_score, priority_label,
                   is_hacking_incident, has_cve, category
            FROM news WHERE fetched_date >= ?
        ''', (week_ago,)).fetchall()

        if not recent_news:
            summary_parts.append("No recent news to analyze.")
            log_priority_analysis(0, 0, 0, "No recent news available for analysis.")
            conn.close()
            return

        # Analyze word frequency in high-priority news
        high_priority_words = Counter()
        all_words = Counter()
        hacking_words = Counter()

        for news in recent_news:
            text = f"{news['title']} {news['summary'] or ''}".lower()
            words = _extract_meaningful_words(text)

            for word in words:
                all_words[word] += 1
                if news['priority_score'] >= 75:
                    high_priority_words[word] += 1
                if news['is_hacking_incident']:
                    hacking_words[word] += 1

        # Get existing rules for comparison
        existing_rules = get_priority_rules()
        existing_keywords = {r['keyword'].lower() for r in existing_rules}

        # Find new candidate keywords that appear frequently in high-priority news
        # but are not yet in the rules
        new_candidates = []
        for word, count in high_priority_words.most_common(50):
            if (word not in existing_keywords
                    and count >= 3
                    and len(word) >= 4):
                # Calculate relevance: ratio of appearance in high-priority vs all
                total_count = all_words.get(word, 1)
                ratio = count / total_count
                if ratio >= 0.5:
                    new_candidates.append({
                        'keyword': word,
                        'count': count,
                        'ratio': ratio,
                        'score': _calculate_suggested_score(count, ratio)
                    })

        # Add top new candidates as system-suggested rules
        for candidate in new_candidates[:10]:
            score = candidate['score']
            level = _score_to_level(score)
            success = add_priority_rule(
                level=level,
                keyword=candidate['keyword'],
                score=score,
                is_user_defined=False
            )
            if success:
                rules_added += 1
                summary_parts.append(
                    f"Added '{candidate['keyword']}' (score: {score}, "
                    f"appeared {candidate['count']} times in high-priority news)"
                )

        # Adjust existing rules based on hit frequency
        for rule in existing_rules:
            if rule['is_user_defined']:
                continue

            # If a rule hasn't matched anything in 30 days, consider lowering it
            if rule['hit_count'] == 0 and rule['score'] > 25:
                new_score = max(25, rule['score'] - 10)
                if new_score != rule['score']:
                    update_priority_rule(rule['id'], {
                        'score': new_score,
                        'level': _score_to_level(new_score)
                    })
                    rules_modified += 1
                    summary_parts.append(
                        f"Lowered '{rule['keyword']}' score from {rule['score']} to {new_score} "
                        f"(no recent matches)"
                    )

            # If a rule matches very frequently, consider raising its priority
            elif rule['hit_count'] > 20 and rule['score'] < 100:
                new_score = min(100, rule['score'] + 10)
                if new_score != rule['score']:
                    update_priority_rule(rule['id'], {
                        'score': new_score,
                        'level': _score_to_level(new_score)
                    })
                    rules_modified += 1
                    summary_parts.append(
                        f"Raised '{rule['keyword']}' score from {rule['score']} to {new_score} "
                        f"(matched {rule['hit_count']} times)"
                    )

        # Analyze hacking incident patterns for new keywords
        for word, count in hacking_words.most_common(20):
            if word not in existing_keywords and count >= 2 and len(word) >= 4:
                success = add_priority_rule(
                    level='critical',
                    keyword=word,
                    score=90,
                    is_user_defined=False
                )
                if success:
                    rules_added += 1
                    summary_parts.append(
                        f"Added hacking-pattern keyword '{word}' "
                        f"(found in {count} hacking incidents)"
                    )

        # Reset hit counts for next analysis period
        conn.execute("UPDATE priority_rules SET hit_count = 0 WHERE is_user_defined = 0")
        conn.commit()

    except Exception as e:
        logger.error(f"Priority analysis error: {e}")
        summary_parts.append(f"Error during analysis: {e}")
    finally:
        conn.close()

    summary = "\n".join(summary_parts) if summary_parts else "Analysis complete. No changes needed."
    log_priority_analysis(rules_added, rules_modified, rules_removed, summary)

    logger.info(
        f"Priority analysis complete: "
        f"{rules_added} added, {rules_modified} modified, {rules_removed} removed"
    )

    return {
        'rules_added': rules_added,
        'rules_modified': rules_modified,
        'rules_removed': rules_removed,
        'summary': summary
    }


def _extract_meaningful_words(text):
    """
    Extract meaningful words from text, filtering out common stop words
    and short words that aren't useful for priority classification.
    """
    import re
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())

    stop_words = {
        'that', 'this', 'with', 'from', 'have', 'been', 'were', 'they',
        'their', 'will', 'would', 'could', 'should', 'about', 'which',
        'when', 'what', 'there', 'other', 'more', 'some', 'than', 'them',
        'also', 'just', 'after', 'before', 'into', 'over', 'such', 'most',
        'only', 'very', 'said', 'each', 'year', 'years', 'being', 'does',
        'those', 'these', 'your', 'here', 'where', 'many', 'like', 'then',
        'make', 'made', 'well', 'back', 'much', 'even', 'still', 'long',
        'come', 'since', 'good', 'last', 'first', 'need', 'know', 'used',
        'want', 'look', 'time', 'work', 'take', 'help', 'read', 'news',
        'http', 'https', 'www',
    }

    return [w for w in words if w not in stop_words]


def _calculate_suggested_score(count, ratio):
    """Calculate a suggested priority score based on frequency and relevance ratio."""
    base_score = 50
    if count >= 10:
        base_score = 80
    elif count >= 5:
        base_score = 65
    if ratio >= 0.8:
        base_score = min(100, base_score + 15)
    elif ratio >= 0.6:
        base_score = min(100, base_score + 10)
    return base_score


def _score_to_level(score):
    """Convert a numeric score to a priority level label."""
    if score >= 90:
        return 'critical'
    elif score >= 70:
        return 'high'
    elif score >= 40:
        return 'medium'
    else:
        return 'low'
