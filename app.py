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
import os
import threading
from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler

from database import (
    init_db, get_db, get_top_news, get_news, get_news_by_id, get_news_stats,
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

# Configure logging - route all module loggers to log files
from logger_config import (
    app_logger, error_logger, access_logger,
    LOG_DIR, DETAILED_FORMAT, APP_LOG
)
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add file handlers to root logger so all module loggers propagate to log files
_root = logging.getLogger()
_root.setLevel(logging.INFO)
_app_fh = RotatingFileHandler(APP_LOG, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
_app_fh.setFormatter(DETAILED_FORMAT)
_root.addHandler(_app_fh)
_err_fh = RotatingFileHandler(
    os.path.join(LOG_DIR, 'error.log'), maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
)
_err_fh.setLevel(logging.ERROR)
_err_fh.setFormatter(DETAILED_FORMAT)
_root.addHandler(_err_fh)

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

    # Setup auto-update scheduler
    setup_update_scheduler()


def setup_update_scheduler():
    """Configure the auto-update scheduler based on settings."""
    auto_update_enabled = get_setting('auto_update_enabled', 'false').lower() == 'true'

    if not auto_update_enabled:
        # Remove the job if it exists
        try:
            scheduler.remove_job('auto_update')
            logger.info("Auto-update scheduler disabled")
        except:
            pass
        return

    from git_updater import check_and_update_if_needed
    update_schedule = get_setting('update_schedule', 'daily')

    # Remove existing job if it exists
    try:
        scheduler.remove_job('auto_update')
    except:
        pass

    # Add scheduler job based on schedule setting
    if update_schedule == 'hourly':
        scheduler.add_job(
            check_and_update_if_needed,
            'interval',
            hours=1,
            id='auto_update',
            replace_existing=True,
            name='Hourly auto-update check'
        )
        logger.info("Auto-update scheduler: Every hour")
    elif update_schedule == 'every_6_hours':
        scheduler.add_job(
            check_and_update_if_needed,
            'interval',
            hours=6,
            id='auto_update',
            replace_existing=True,
            name='Auto-update check every 6 hours'
        )
        logger.info("Auto-update scheduler: Every 6 hours")
    elif update_schedule == 'weekly':
        scheduler.add_job(
            check_and_update_if_needed,
            'cron',
            day_of_week='sun',
            hour=0, minute=0,
            id='auto_update',
            replace_existing=True,
            name='Weekly auto-update check'
        )
        logger.info("Auto-update scheduler: Weekly (Sunday midnight)")
    else:  # daily
        scheduler.add_job(
            check_and_update_if_needed,
            'cron',
            hour=0, minute=30,
            id='auto_update',
            replace_existing=True,
            name='Daily auto-update check'
        )
        logger.info("Auto-update scheduler: Daily (00:30)")


# ============================================================
# ROUTES - Dashboard
# ============================================================

@app.route('/')
def dashboard():
    """Main dashboard page with top 20 security news, stats, and overview."""
    sort = request.args.get('sort', 'time')
    if sort not in ('time', 'priority', 'category'):
        sort = 'time'
    top_news = get_top_news(limit=20, sort=sort)
    stats = get_news_stats()
    return render_template('dashboard.html',
                           top_news=top_news,
                           stats=stats,
                           sort=sort,
                           regions=REGIONS,
                           categories=NEWS_CATEGORIES,
                           now=datetime.utcnow())


# ============================================================
# ROUTES - News List with Filters
# ============================================================

@app.route('/news')
def news_list():
    """Full news list page with filtering and sorting."""
    filters = {}
    page = request.args.get('page', 1, type=int)
    per_page = int(get_setting('items_per_page', '25'))
    sort = request.args.get('sort', 'priority')
    if sort not in ('time', 'priority', 'category', 'source'):
        sort = 'priority'

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

    news, total = get_news(filters=filters, page=page, per_page=per_page, sort=sort)
    sources = get_sources()
    total_pages = (total + per_page - 1) // per_page

    return render_template('news.html',
                           news=news,
                           total=total,
                           page=page,
                           total_pages=total_pages,
                           per_page=per_page,
                           filters=filters,
                           sort=sort,
                           sources=sources,
                           regions=REGIONS,
                           categories=NEWS_CATEGORIES,
                           cve_vendors=CVE_VENDOR_KEYWORDS)


# ============================================================
# ROUTES - CVE Monitoring
# ============================================================

@app.route('/cve')
def cve_page():
    """CVE-focused view with vendor filtering and sorting."""
    filters = {'has_cve': True}
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'time')
    if sort not in ('time', 'priority', 'category', 'source'):
        sort = 'time'

    if request.args.get('vendor'):
        filters['cve_vendor'] = request.args.get('vendor')
    if request.args.get('search'):
        filters['search'] = request.args.get('search')

    news, total = get_news(filters=filters, page=page, per_page=50, sort=sort)
    total_pages = (total + 50 - 1) // 50

    return render_template('cve.html',
                           news=news,
                           total=total,
                           page=page,
                           total_pages=total_pages,
                           sort=sort,
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
    """Priority rules management with search and sorting."""
    rules = get_priority_rules()
    search = request.args.get('search', '').strip().lower()
    if search:
        rules = [r for r in rules if search in r.get('keyword', '').lower()
                 or search in r.get('level', '').lower()]
    sort = request.args.get('sort', 'score')
    if sort == 'keyword':
        rules.sort(key=lambda r: r.get('keyword', ''))
    elif sort == 'hits':
        rules.sort(key=lambda r: r.get('hit_count', 0), reverse=True)
    elif sort == 'level':
        level_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        rules.sort(key=lambda r: level_order.get(r.get('level', 'low'), 4))

    analysis_logs = get_analysis_logs(limit=10)
    return render_template('priorities.html',
                           rules=rules,
                           analysis_logs=analysis_logs,
                           search=search,
                           sort=sort)


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
# GIT AUTO-UPDATE ROUTES
# ============================================================

@app.route('/updates')
def updates_page():
    """System updates configuration page."""
    import os
    app_path = os.path.abspath(os.path.dirname(__file__))
    return render_template('updates.html', app_path=app_path)


@app.route('/api/git/info')
def api_git_info():
    """Get Git repository information."""
    try:
        from git_updater import GitUpdater
        updater = GitUpdater()
        info = updater.get_git_info()
        return jsonify(info)
    except Exception as e:
        logger.error(f"Error getting git info: {e}")
        return jsonify({'error': str(e), 'is_git_repo': False})


@app.route('/api/git/check-updates')
def api_check_updates():
    """Check if updates are available from remote repository."""
    try:
        from git_updater import GitUpdater
        updater = GitUpdater()
        result = updater.check_for_updates()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error checking for updates: {e}")
        return jsonify({'available': False, 'error': str(e)})


@app.route('/api/git/update', methods=['POST'])
def api_perform_update():
    """Perform git pull to update the application."""
    try:
        from git_updater import GitUpdater
        updater = GitUpdater()
        result = updater.perform_update()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error performing update: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/git/history')
def api_update_history():
    """Get update history."""
    try:
        from git_updater import GitUpdater
        updater = GitUpdater()
        history = updater.get_update_history(limit=20)
        return jsonify({'history': history})
    except Exception as e:
        logger.error(f"Error getting update history: {e}")
        return jsonify({'history': [], 'error': str(e)})


@app.route('/api/update-settings', methods=['POST'])
def api_save_update_settings():
    """Save auto-update settings."""
    try:
        settings = request.get_json()
        for key, value in settings.items():
            update_setting(key, value)

        # Reschedule if auto-update settings changed
        if 'auto_update_enabled' in settings or 'update_schedule' in settings:
            setup_update_scheduler()

        return jsonify({'success': True, 'message': 'Settings saved successfully'})
    except Exception as e:
        logger.error(f"Error saving update settings: {e}")
        return jsonify({'success': False, 'error': str(e)})


# ============================================================
# LOGGING ROUTES
# ============================================================

@app.route('/logs')
def logs_page():
    """System logs viewing page."""
    return render_template('logs.html')


@app.route('/api/logs/list')
def api_logs_list():
    """Get list of all log files with metadata."""
    try:
        from logger_config import get_log_files
        log_files = get_log_files()
        return jsonify({'log_files': log_files})
    except Exception as e:
        logger.error(f"Error listing log files: {e}")
        return jsonify({'log_files': [], 'error': str(e)})


@app.route('/api/logs/<log_name>')
def api_logs_tail(log_name):
    """Get last N lines from a log file."""
    try:
        import os
        from logger_config import LOG_DIR, get_log_tail, get_log_files

        # Validate log name
        valid_logs = ['app.log', 'error.log', 'access.log', 'update.log', 'feed.log']
        if log_name not in valid_logs:
            return jsonify({'error': 'Invalid log file'}), 400

        log_path = os.path.join(LOG_DIR, log_name)
        lines = request.args.get('lines', 100, type=int)

        # Get log content
        content = get_log_tail(log_path, lines)

        # Get log metadata
        log_files = get_log_files()
        log_meta = next((lf for lf in log_files if lf['filename'] == log_name), {})

        return jsonify({
            'content': content,
            'filename': log_name,
            'size': log_meta.get('size', 0),
            'size_human': log_meta.get('size_human', '0 B'),
            'modified': log_meta.get('modified', 'Unknown')
        })
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return jsonify({'error': str(e), 'content': ''}), 500


@app.route('/api/logs/<log_name>/download')
def api_logs_download(log_name):
    """Download a log file."""
    try:
        import os
        from flask import send_file
        from logger_config import LOG_DIR

        # Validate log name
        valid_logs = ['app.log', 'error.log', 'access.log', 'update.log', 'feed.log']
        if log_name not in valid_logs:
            return jsonify({'error': 'Invalid log file'}), 400

        log_path = os.path.join(LOG_DIR, log_name)

        if not os.path.exists(log_path):
            return jsonify({'error': 'Log file not found'}), 404

        return send_file(log_path, as_attachment=True, download_name=log_name)
    except Exception as e:
        logger.error(f"Error downloading log file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs/<log_name>/clear', methods=['POST'])
def api_logs_clear(log_name):
    """Clear a log file."""
    try:
        import os
        from logger_config import LOG_DIR, clear_log

        # Validate log name
        valid_logs = ['app.log', 'error.log', 'access.log', 'update.log', 'feed.log']
        if log_name not in valid_logs:
            return jsonify({'error': 'Invalid log file', 'success': False}), 400

        log_path = os.path.join(LOG_DIR, log_name)

        if clear_log(log_path):
            return jsonify({'success': True, 'message': f'{log_name} cleared'})
        else:
            return jsonify({'success': False, 'error': 'Failed to clear log file'}), 500
    except Exception as e:
        logger.error(f"Error clearing log file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# ROUTES - Cyber Attack Map
# ============================================================

@app.route('/attack-map')
def attack_map_page():
    """Real-time cyber attack map visualization."""
    return render_template('attack_map.html')


@app.route('/api/attack-data')
def api_attack_data():
    """Get cyber attack data derived from news for the attack map."""
    import random

    COUNTRY_COORDS = {
        'United States': {'lat': 39.8, 'lon': -98.6},
        'Russia': {'lat': 55.8, 'lon': 37.6},
        'China': {'lat': 35.0, 'lon': 105.0},
        'North Korea': {'lat': 40.0, 'lon': 127.0},
        'Iran': {'lat': 35.7, 'lon': 51.4},
        'United Kingdom': {'lat': 51.5, 'lon': -0.1},
        'Germany': {'lat': 51.2, 'lon': 10.5},
        'France': {'lat': 46.2, 'lon': 2.2},
        'India': {'lat': 20.6, 'lon': 79.0},
        'Brazil': {'lat': -14.2, 'lon': -51.9},
        'Japan': {'lat': 36.2, 'lon': 138.3},
        'South Korea': {'lat': 36.5, 'lon': 128.0},
        'Australia': {'lat': -25.3, 'lon': 133.8},
        'Canada': {'lat': 56.1, 'lon': -106.3},
        'Ukraine': {'lat': 48.4, 'lon': 31.2},
        'Israel': {'lat': 31.0, 'lon': 34.8},
        'Turkey': {'lat': 39.9, 'lon': 32.9},
        'Singapore': {'lat': 1.4, 'lon': 103.8},
        'Netherlands': {'lat': 52.4, 'lon': 4.9},
        'Sweden': {'lat': 59.3, 'lon': 18.1},
        'Poland': {'lat': 52.2, 'lon': 21.0},
        'Spain': {'lat': 40.4, 'lon': -3.7},
        'Italy': {'lat': 41.9, 'lon': 12.5},
        'Egypt': {'lat': 30.0, 'lon': 31.2},
        'South Africa': {'lat': -33.9, 'lon': 18.4},
        'Mexico': {'lat': 19.4, 'lon': -99.1},
        'Indonesia': {'lat': -6.2, 'lon': 106.8},
        'Vietnam': {'lat': 21.0, 'lon': 105.8},
        'Thailand': {'lat': 13.8, 'lon': 100.5},
        'Saudi Arabia': {'lat': 24.7, 'lon': 46.7},
        'UAE': {'lat': 25.2, 'lon': 55.3},
        'Pakistan': {'lat': 30.4, 'lon': 69.3},
        'Nigeria': {'lat': 9.1, 'lon': 7.5},
        'Kenya': {'lat': -1.3, 'lon': 36.8},
        'Taiwan': {'lat': 23.7, 'lon': 121.0},
    }

    ATTACKER_PATTERNS = {
        'Russia': ['russia', 'russian', 'apt28', 'apt29', 'fancy bear', 'cozy bear',
                   'sandworm', 'turla', 'nobelium', 'midnight blizzard'],
        'China': ['china', 'chinese', 'apt41', 'apt10', 'apt40', 'hafnium',
                  'winnti', 'apt31', 'panda', 'volt typhoon', 'salt typhoon'],
        'North Korea': ['north korea', 'dprk', 'lazarus', 'kimsuky', 'apt38', 'andariel'],
        'Iran': ['iran', 'iranian', 'apt33', 'apt35', 'charming kitten',
                 'muddywater', 'phosphorus', 'peach sandstorm'],
    }

    TARGET_PATTERNS = {
        'United States': ['us ', 'u.s.', 'american', 'united states', 'fbi',
                          'cisa', 'pentagon', 'nsa', 'federal'],
        'United Kingdom': ['uk ', 'u.k.', 'british', 'britain', 'ncsc', 'england'],
        'Ukraine': ['ukrain', 'kiev', 'kyiv'],
        'Germany': ['german', 'germany'],
        'France': ['french', 'france'],
        'Japan': ['japan', 'jpcert'],
        'Australia': ['austral', 'auscert'],
        'India': ['india', 'indian'],
        'Israel': ['israel'],
        'South Korea': ['south korea', 'korean'],
        'Taiwan': ['taiwan', 'taiwanese'],
    }

    REGION_TARGETS = {
        'global': ['United States', 'United Kingdom', 'Germany', 'Japan', 'Australia'],
        'north_america': ['United States', 'Canada'],
        'europe': ['United Kingdom', 'Germany', 'France', 'Netherlands', 'Poland'],
        'asia_pacific': ['Japan', 'South Korea', 'Australia', 'Singapore', 'India'],
        'china': ['China', 'Taiwan'],
        'middle_east': ['Israel', 'Saudi Arabia', 'UAE', 'Turkey'],
        'africa': ['South Africa', 'Nigeria', 'Kenya', 'Egypt'],
        'south_america': ['Brazil', 'Mexico'],
    }

    DEFAULT_ATTACKERS = ['Russia', 'China', 'North Korea', 'Iran', 'Russia', 'China']

    conn = get_db()
    try:
        rows = conn.execute('''
            SELECT n.id, n.title, n.url, n.summary, n.region, n.priority_label,
                   n.is_hacking_incident, n.has_cve, n.cve_vendors,
                   n.published_date, n.category
            FROM news n
            WHERE (n.is_hacking_incident = 1 OR n.priority_label IN ('critical', 'high'))
            AND n.published_date >= datetime('now', '-30 days')
            ORDER BY n.published_date DESC
            LIMIT 200
        ''').fetchall()

        stats = {
            'total_incidents': conn.execute(
                "SELECT COUNT(*) FROM news WHERE is_hacking_incident = 1"
            ).fetchone()[0],
            'critical_count': conn.execute(
                "SELECT COUNT(*) FROM news WHERE priority_label = 'critical'"
            ).fetchone()[0],
        }
    finally:
        conn.close()

    attacks = []
    for row in rows:
        rd = dict(row)
        text = (rd.get('title', '') + ' ' + (rd.get('summary', '') or '')).lower()

        attacker = None
        for country, kws in ATTACKER_PATTERNS.items():
            if any(kw in text for kw in kws):
                attacker = country
                break
        if not attacker:
            attacker = random.choice(DEFAULT_ATTACKERS)

        target = None
        for country, kws in TARGET_PATTERNS.items():
            if any(kw in text for kw in kws):
                target = country
                break
        if not target:
            region = rd.get('region', 'global')
            targets = REGION_TARGETS.get(region, REGION_TARGETS['global'])
            target = random.choice(targets)

        if attacker == target:
            alts = [c for c in REGION_TARGETS.get(rd.get('region', 'global'),
                    ['United States']) if c != attacker]
            target = random.choice(alts) if alts else 'United States'

        if attacker in COUNTRY_COORDS and target in COUNTRY_COORDS:
            summary_text = rd.get('summary', '') or ''
            attacks.append({
                'id': rd['id'],
                'title': rd['title'],
                'url': rd.get('url', ''),
                'summary': summary_text[:300] if summary_text else '',
                'source': {
                    'country': attacker,
                    'lat': COUNTRY_COORDS[attacker]['lat'],
                    'lon': COUNTRY_COORDS[attacker]['lon'],
                },
                'target': {
                    'country': target,
                    'lat': COUNTRY_COORDS[target]['lat'],
                    'lon': COUNTRY_COORDS[target]['lon'],
                },
                'severity': rd.get('priority_label', 'medium'),
                'type': 'hacking' if rd.get('is_hacking_incident') else (
                    'cve' if rd.get('has_cve') else 'threat'),
                'time': rd.get('published_date', ''),
                'category': rd.get('category', 'web_news'),
            })

    return jsonify({'attacks': attacks, 'stats': stats, 'total': len(attacks)})


@app.route('/api/news/<int:news_id>')
def api_news_detail(news_id):
    """Get a single news article by ID (used by attack map detail overlay)."""
    item = get_news_by_id(news_id)
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item)


# ============================================================
# ACCESS LOGGING
# ============================================================

@app.after_request
def log_access(response):
    """Log every HTTP request to access.log for the logs page."""
    access_logger.info(f"{request.method} {request.path} {response.status_code}")
    return response


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
