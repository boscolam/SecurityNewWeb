"""
Cybersecurity News Dashboard - Main Application
================================================
Flask web application that aggregates cybersecurity news from multiple sources
including RSS feeds, vendor security blogs, dark web intelligence, CVE databases,
and social media. Features priority-based scoring, region/category filtering,
automatic feed discovery, and daily priority rule analysis.

Run with: python app.py
Or deploy behind Apache with mod_wsgi (see INSTALL.md)
"""

import logging
import threading
from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler

from database import (
    init_db, get_top_news, get_news, get_news_stats,
    get_sources, add_source, update_source, delete_source,
    get_settings, get_setting, update_setting,
    get_priority_rules, add_priority_rule, update_priority_rule, delete_priority_rule,
    get_discovered_feeds, approve_discovered_feed, reject_discovered_feed,
    get_analysis_logs, cleanup_old_news
)
from feed_manager import fetch_all_feeds, fetch_single_feed
from priority_engine import run_daily_priority_analysis
from auto_discovery import run_feed_discovery
from config import REGIONS, NEWS_CATEGORIES, FEED_TYPES, CVE_VENDOR_KEYWORDS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cybersec-news-dashboard-secret-change-in-production'

# ============================================================
# SCHEDULED TASKS
# Using APScheduler to run background tasks:
# - Feed fetching at configured intervals
# - Daily priority analysis at midnight
# - Daily feed auto-discovery
# - Weekly old news cleanup
# ============================================================

scheduler = BackgroundScheduler()


def setup_scheduler():
    """Configure and start the background task scheduler."""
    refresh_minutes = int(get_setting('refresh_interval', '30'))

    scheduler.add_job(
        fetch_all_feeds,
        'interval',
        minutes=refresh_minutes,
        id='fetch_feeds',
        replace_existing=True,
        name='Fetch all RSS feeds'
    )

    scheduler.add_job(
        run_daily_priority_analysis,
        'cron',
        hour=0, minute=0,
        id='priority_analysis',
        replace_existing=True,
        name='Daily priority rule analysis at midnight'
    )

    scheduler.add_job(
        run_feed_discovery,
        'cron',
        hour=2, minute=0,
        id='feed_discovery',
        replace_existing=True,
        name='Daily feed auto-discovery at 2 AM'
    )

    scheduler.add_job(
        cleanup_old_news,
        'cron',
        day_of_week='sun',
        hour=3, minute=0,
        id='cleanup',
        replace_existing=True,
        name='Weekly old news cleanup'
    )

    scheduler.start()
    logger.info(f"Scheduler started. Feed refresh every {refresh_minutes} minutes.")


# ============================================================
# ROUTES - Dashboard
# ============================================================

@app.route('/')
def dashboard():
    """
    Main dashboard page.
    Shows top 10 news summary, statistics, and quick overview.
    """
    top_news = get_top_news(limit=10)
    stats = get_news_stats()
    return render_template('dashboard.html',
                           top_news=top_news,
                           stats=stats,
                           regions=REGIONS,
                           categories=NEWS_CATEGORIES,
                           now=datetime.utcnow())


# ============================================================
# ROUTES - News List with Filters
# ============================================================

@app.route('/news')
def news_list():
    """
    Full news list page with filtering capabilities.
    Supports filters: category, region, source, priority, CVE vendor, search.
    """
    filters = {}
    page = request.args.get('page', 1, type=int)
    per_page = int(get_setting('items_per_page', '25'))

    if request.args.get('category'):
        filters['category'] = request.args.get('category')
    if request.args.get('region'):
        filters['region'] = request.args.get('region')
    if request.args.get('source_id'):
        filters['source_id'] = request.args.get('source_id', type=int)
    if request.args.get('priority'):
        filters['priority_label'] = request.args.get('priority')
    if request.args.get('hacking'):
        filters['is_hacking_incident'] = True
    if request.args.get('cve'):
        filters['has_cve'] = True
    if request.args.get('cve_vendor'):
        filters['cve_vendor'] = request.args.get('cve_vendor')
    if request.args.get('search'):
        filters['search'] = request.args.get('search')
    if request.args.get('date_from'):
        filters['date_from'] = request.args.get('date_from')
    if request.args.get('date_to'):
        filters['date_to'] = request.args.get('date_to')

    news, total = get_news(filters=filters, page=page, per_page=per_page)
    sources = get_sources()
    total_pages = (total + per_page - 1) // per_page

    return render_template('news.html',
                           news=news,
                           total=total,
                           page=page,
                           total_pages=total_pages,
                           per_page=per_page,
                           filters=filters,
                           sources=sources,
                           regions=REGIONS,
                           categories=NEWS_CATEGORIES,
                           cve_vendors=CVE_VENDOR_KEYWORDS)


# ============================================================
# ROUTES - CVE Monitoring
# ============================================================

@app.route('/cve')
def cve_page():
    """
    CVE-focused view showing vulnerability news.
    Pre-filters for CVE-related content with vendor filtering.
    """
    filters = {'has_cve': True}
    page = request.args.get('page', 1, type=int)

    if request.args.get('vendor'):
        filters['cve_vendor'] = request.args.get('vendor')
    if request.args.get('search'):
        filters['search'] = request.args.get('search')

    news, total = get_news(filters=filters, page=page, per_page=50)
    total_pages = (total + 50 - 1) // 50

    return render_template('cve.html',
                           news=news,
                           total=total,
                           page=page,
                           total_pages=total_pages,
                           cve_vendors=CVE_VENDOR_KEYWORDS)


# ============================================================
# ROUTES - Settings
# ============================================================

@app.route('/settings')
def settings_page():
    """Application settings page for refresh intervals and general config."""
    settings = get_settings()
    analysis_logs = get_analysis_logs(limit=5)
    return render_template('settings.html',
                           settings=settings,
                           analysis_logs=analysis_logs)


@app.route('/settings/update', methods=['POST'])
def settings_update():
    """Handle settings form submission."""
    for key in request.form:
        if key.startswith('setting_'):
            setting_key = key[8:]
            update_setting(setting_key, request.form[key])

    # Reschedule feed fetching if interval changed
    new_interval = request.form.get('setting_refresh_interval')
    if new_interval:
        try:
            scheduler.reschedule_job(
                'fetch_feeds',
                trigger='interval',
                minutes=int(new_interval)
            )
        except Exception as e:
            logger.error(f"Failed to reschedule feed fetching: {e}")

    return redirect(url_for('settings_page'))


# ============================================================
# ROUTES - Source Management
# ============================================================

@app.route('/sources')
def sources_page():
    """Feed source management page. Add, edit, enable/disable sources."""
    sources = get_sources()
    discovered = get_discovered_feeds()
    return render_template('sources.html',
                           sources=sources,
                           discovered=discovered,
                           regions=REGIONS,
                           categories=NEWS_CATEGORIES,
                           feed_types=FEED_TYPES)


@app.route('/sources/add', methods=['POST'])
def source_add():
    """Add a new feed source."""
    source = {
        'name': request.form.get('name', '').strip(),
        'url': request.form.get('url', '').strip(),
        'category': request.form.get('category', 'web_news'),
        'feed_type': request.form.get('feed_type', 'rss'),
        'region': request.form.get('region', 'global'),
        'enabled': request.form.get('enabled') == '1',
    }
    if source['name'] and source['url']:
        add_source(source)
    return redirect(url_for('sources_page'))


@app.route('/sources/update/<int:source_id>', methods=['POST'])
def source_update(source_id):
    """Update an existing feed source."""
    data = {
        'name': request.form.get('name', '').strip(),
        'url': request.form.get('url', '').strip(),
        'category': request.form.get('category', 'web_news'),
        'feed_type': request.form.get('feed_type', 'rss'),
        'region': request.form.get('region', 'global'),
        'enabled': 1 if request.form.get('enabled') == '1' else 0,
    }
    update_source(source_id, data)
    return redirect(url_for('sources_page'))


@app.route('/sources/delete/<int:source_id>', methods=['POST'])
def source_delete(source_id):
    """Delete a feed source."""
    delete_source(source_id)
    return redirect(url_for('sources_page'))


@app.route('/sources/discovered/approve/<int:feed_id>', methods=['POST'])
def discovered_approve(feed_id):
    """Approve a discovered feed and add it to active sources."""
    approve_discovered_feed(feed_id)
    return redirect(url_for('sources_page'))


@app.route('/sources/discovered/reject/<int:feed_id>', methods=['POST'])
def discovered_reject(feed_id):
    """Reject and remove a discovered feed."""
    reject_discovered_feed(feed_id)
    return redirect(url_for('sources_page'))


# ============================================================
# ROUTES - Priority Rules
# ============================================================

@app.route('/priorities')
def priorities_page():
    """Priority rules management page. View, add, edit priority keyword rules."""
    rules = get_priority_rules()
    analysis_logs = get_analysis_logs(limit=10)
    return render_template('priorities.html',
                           rules=rules,
                           analysis_logs=analysis_logs)


@app.route('/priorities/add', methods=['POST'])
def priority_add():
    """Add a new user-defined priority rule."""
    level = request.form.get('level', 'medium')
    keyword = request.form.get('keyword', '').strip().lower()
    score = request.form.get('score', 50, type=int)
    if keyword:
        add_priority_rule(level, keyword, score, is_user_defined=True)
    return redirect(url_for('priorities_page'))


@app.route('/priorities/update/<int:rule_id>', methods=['POST'])
def priority_update(rule_id):
    """Update an existing priority rule."""
    data = {
        'level': request.form.get('level', 'medium'),
        'keyword': request.form.get('keyword', '').strip().lower(),
        'score': request.form.get('score', 50, type=int),
    }
    update_priority_rule(rule_id, data)
    return redirect(url_for('priorities_page'))


@app.route('/priorities/delete/<int:rule_id>', methods=['POST'])
def priority_delete(rule_id):
    """Delete a priority rule."""
    delete_priority_rule(rule_id)
    return redirect(url_for('priorities_page'))


# ============================================================
# API ROUTES - For AJAX / JavaScript calls
# ============================================================

@app.route('/api/news')
def api_news():
    """API endpoint to fetch news with filters (JSON response)."""
    filters = {}
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)

    for key in ['category', 'region', 'priority_label', 'cve_vendor', 'search']:
        if request.args.get(key):
            filters[key] = request.args.get(key)
    if request.args.get('hacking'):
        filters['is_hacking_incident'] = True
    if request.args.get('cve'):
        filters['has_cve'] = True

    news, total = get_news(filters=filters, page=page, per_page=per_page)
    return jsonify({
        'news': news,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@app.route('/api/stats')
def api_stats():
    """API endpoint to fetch dashboard statistics."""
    return jsonify(get_news_stats())


@app.route('/api/fetch', methods=['POST'])
def api_fetch_feeds():
    """API endpoint to manually trigger feed fetching."""
    result = fetch_all_feeds()
    return jsonify(result)


@app.route('/api/analyze', methods=['POST'])
def api_run_analysis():
    """API endpoint to manually trigger priority analysis."""
    result = run_daily_priority_analysis()
    return jsonify(result)


@app.route('/api/discover', methods=['POST'])
def api_run_discovery():
    """API endpoint to manually trigger feed discovery."""
    result = run_feed_discovery()
    return jsonify(result)


# ============================================================
# TEMPLATE FILTERS
# ============================================================

@app.template_filter('timeago')
def timeago_filter(date_str):
    """Convert a date string to a human-readable time-ago format."""
    if not date_str:
        return 'Unknown'
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        now = datetime.utcnow()
        diff = now - dt.replace(tzinfo=None)

        if diff.days > 30:
            return dt.strftime('%Y-%m-%d')
        elif diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "Just now"
    except Exception:
        return date_str[:10] if date_str else 'Unknown'


@app.template_filter('priority_color')
def priority_color_filter(label):
    """Return a CSS color class based on priority label."""
    colors = {
        'critical': '#dc3545',
        'high': '#fd7e14',
        'medium': '#ffc107',
        'low': '#28a745',
    }
    return colors.get(label, '#6c757d')


@app.template_filter('category_label')
def category_label_filter(key):
    """Convert category key to human-readable label."""
    return NEWS_CATEGORIES.get(key, key.replace('_', ' ').title())


@app.template_filter('region_label')
def region_label_filter(key):
    """Convert region key to human-readable label."""
    return REGIONS.get(key, key.replace('_', ' ').title())


# ============================================================
# APPLICATION STARTUP
# ============================================================

if __name__ == '__main__':
    # Initialize the database (create tables, seed defaults)
    init_db()

    # Set up the background scheduler
    setup_scheduler()

    # Run initial feed fetch in background thread so the web server starts immediately
    def initial_fetch():
        logger.info("Running initial feed fetch in background...")
        try:
            fetch_all_feeds()
            logger.info("Initial feed fetch complete.")
        except Exception as e:
            logger.error(f"Initial feed fetch failed: {e}")

    threading.Thread(target=initial_fetch, daemon=True).start()

    # Start the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
