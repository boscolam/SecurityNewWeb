"""
Database module for the Cybersecurity News Dashboard.
Handles SQLite database initialization, schema creation,
and all CRUD operations for news, sources, settings, and priority rules.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from config import DATABASE_PATH, DEFAULT_FEEDS, DEFAULT_PRIORITY_RULES, NEWS_RETENTION_DAYS


def get_db():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize the database schema and seed default data."""
    conn = get_db()
    cursor = conn.cursor()

    # --- News articles table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            content TEXT,
            source_id INTEGER,
            category TEXT DEFAULT 'web_news',
            region TEXT DEFAULT 'global',
            priority_score INTEGER DEFAULT 50,
            priority_label TEXT DEFAULT 'medium',
            is_hacking_incident INTEGER DEFAULT 0,
            has_cve INTEGER DEFAULT 0,
            cve_ids TEXT,
            cve_vendors TEXT,
            published_date TEXT,
            fetched_date TEXT DEFAULT CURRENT_TIMESTAMP,
            tags TEXT,
            image_url TEXT,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        )
    ''')

    # --- Feed sources table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            category TEXT DEFAULT 'web_news',
            feed_type TEXT DEFAULT 'rss',
            region TEXT DEFAULT 'global',
            enabled INTEGER DEFAULT 1,
            last_fetched TEXT,
            fetch_error TEXT,
            auto_discovered INTEGER DEFAULT 0,
            added_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Application settings table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Priority rules table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS priority_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            keyword TEXT NOT NULL,
            score INTEGER NOT NULL,
            is_system INTEGER DEFAULT 0,
            is_user_defined INTEGER DEFAULT 0,
            hit_count INTEGER DEFAULT 0,
            last_hit_date TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Auto-discovered feeds table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discovered_feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            category TEXT DEFAULT 'web_news',
            region TEXT DEFAULT 'global',
            discovered_from TEXT,
            approved INTEGER DEFAULT 0,
            discovery_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Priority analysis log ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS priority_analysis_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_date TEXT DEFAULT CURRENT_TIMESTAMP,
            rules_added INTEGER DEFAULT 0,
            rules_modified INTEGER DEFAULT 0,
            rules_removed INTEGER DEFAULT 0,
            summary TEXT
        )
    ''')

    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_priority ON news(priority_score DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_category ON news(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_region ON news(region)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_date DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_hacking ON news(is_hacking_incident)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_cve ON news(has_cve)')

    conn.commit()

    # Seed default data if tables are empty
    _seed_default_sources(conn)
    _seed_default_settings(conn)
    _seed_default_priority_rules(conn)

    conn.close()


def _seed_default_sources(conn):
    """Insert default feed sources if the sources table is empty."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sources")
    if cursor.fetchone()[0] == 0:
        for feed in DEFAULT_FEEDS:
            cursor.execute('''
                INSERT OR IGNORE INTO sources (name, url, category, feed_type, region, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (feed['name'], feed['url'], feed['category'], feed['feed_type'],
                  feed['region'], 1 if feed['enabled'] else 0))
        conn.commit()


def _seed_default_settings(conn):
    """Insert default application settings."""
    cursor = conn.cursor()
    defaults = {
        'refresh_interval': ('30', 'Feed refresh interval in minutes'),
        'auto_discover_feeds': ('1', 'Enable automatic feed discovery (1=on, 0=off)'),
        'max_news_display': ('100', 'Maximum news items to display per page'),
        'priority_analysis_time': ('00:00', 'Time to run daily priority analysis (HH:MM)'),
        'news_retention_days': (str(NEWS_RETENTION_DAYS), 'Days to keep news before cleanup'),
        'hacking_always_top': ('1', 'Hacking incidents always top priority (1=on, 0=off)'),
        'dark_mode': ('0', 'Enable dark mode (1=on, 0=off)'),
        'items_per_page': ('25', 'Number of items per page'),
        # Auto-update settings
        'auto_update_enabled': ('false', 'Enable automatic updates from GitHub'),
        'update_schedule': ('daily', 'Update check schedule: hourly, every_6_hours, daily, weekly'),
        'backup_before_update': ('true', 'Backup database before updating'),
        'restart_after_update': ('false', 'Restart application after update (requires systemd)'),
        'notify_on_update': ('true', 'Log update notifications'),
    }
    for key, (value, desc) in defaults.items():
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value, description)
            VALUES (?, ?, ?)
        ''', (key, value, desc))
    conn.commit()


def _seed_default_priority_rules(conn):
    """Insert default priority rules."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM priority_rules")
    if cursor.fetchone()[0] == 0:
        for level, data in DEFAULT_PRIORITY_RULES.items():
            for keyword in data['keywords']:
                cursor.execute('''
                    INSERT INTO priority_rules (level, keyword, score, is_system)
                    VALUES (?, ?, ?, 1)
                ''', (level, keyword, data['score']))
        conn.commit()


# ============================================================
# NEWS CRUD Operations
# ============================================================

def insert_news(news_item):
    """Insert a single news article. Returns True if inserted, False if duplicate."""
    conn = get_db()
    try:
        conn.execute('''
            INSERT OR IGNORE INTO news
            (title, url, summary, content, source_id, category, region,
             priority_score, priority_label, is_hacking_incident, has_cve,
             cve_ids, cve_vendors, published_date, tags, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            news_item.get('title', ''),
            news_item.get('url', ''),
            news_item.get('summary', ''),
            news_item.get('content', ''),
            news_item.get('source_id'),
            news_item.get('category', 'web_news'),
            news_item.get('region', 'global'),
            news_item.get('priority_score', 50),
            news_item.get('priority_label', 'medium'),
            1 if news_item.get('is_hacking_incident') else 0,
            1 if news_item.get('has_cve') else 0,
            news_item.get('cve_ids', ''),
            news_item.get('cve_vendors', ''),
            news_item.get('published_date', ''),
            news_item.get('tags', ''),
            news_item.get('image_url', ''),
        ))
        conn.commit()
        return conn.total_changes > 0
    finally:
        conn.close()


def get_news(filters=None, page=1, per_page=25):
    """
    Fetch news articles with optional filters.
    filters dict can contain: category, region, source_id, priority_label,
    is_hacking_incident, has_cve, cve_vendor, search, date_from, date_to
    """
    conn = get_db()
    query = "SELECT n.*, s.name as source_name FROM news n LEFT JOIN sources s ON n.source_id = s.id WHERE 1=1"
    params = []

    if filters:
        if filters.get('category'):
            query += " AND n.category = ?"
            params.append(filters['category'])
        if filters.get('region'):
            query += " AND n.region = ?"
            params.append(filters['region'])
        if filters.get('source_id'):
            query += " AND n.source_id = ?"
            params.append(filters['source_id'])
        if filters.get('priority_label'):
            query += " AND n.priority_label = ?"
            params.append(filters['priority_label'])
        if filters.get('is_hacking_incident'):
            query += " AND n.is_hacking_incident = 1"
        if filters.get('has_cve'):
            query += " AND n.has_cve = 1"
        if filters.get('cve_vendor'):
            query += " AND n.cve_vendors LIKE ?"
            params.append(f"%{filters['cve_vendor']}%")
        if filters.get('search'):
            query += " AND (n.title LIKE ? OR n.summary LIKE ?)"
            params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
        if filters.get('date_from'):
            query += " AND n.published_date >= ?"
            params.append(filters['date_from'])
        if filters.get('date_to'):
            query += " AND n.published_date <= ?"
            params.append(filters['date_to'])

    query += " ORDER BY n.priority_score DESC, n.published_date DESC"
    query += f" LIMIT {per_page} OFFSET {(page - 1) * per_page}"

    rows = conn.execute(query, params).fetchall()
    count_query = query.split("ORDER BY")[0].replace(
        "SELECT n.*, s.name as source_name FROM", "SELECT COUNT(*) FROM"
    )
    total = conn.execute(count_query, params).fetchone()[0]
    conn.close()

    return [dict(row) for row in rows], total


def get_top_news(limit=10):
    """Get top N news items sorted by priority score, hacking incidents first."""
    conn = get_db()
    rows = conn.execute('''
        SELECT n.*, s.name as source_name
        FROM news n
        LEFT JOIN sources s ON n.source_id = s.id
        ORDER BY n.is_hacking_incident DESC, n.priority_score DESC, n.published_date DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_news_stats():
    """Get statistics for the dashboard."""
    conn = get_db()
    stats = {}
    stats['total_news'] = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    stats['today_news'] = conn.execute(
        "SELECT COUNT(*) FROM news WHERE date(fetched_date) = date('now')"
    ).fetchone()[0]
    stats['hacking_incidents'] = conn.execute(
        "SELECT COUNT(*) FROM news WHERE is_hacking_incident = 1"
    ).fetchone()[0]
    stats['cve_count'] = conn.execute(
        "SELECT COUNT(*) FROM news WHERE has_cve = 1"
    ).fetchone()[0]
    stats['active_sources'] = conn.execute(
        "SELECT COUNT(*) FROM sources WHERE enabled = 1"
    ).fetchone()[0]
    stats['total_sources'] = conn.execute(
        "SELECT COUNT(*) FROM sources"
    ).fetchone()[0]

    # Category breakdown
    stats['by_category'] = {}
    rows = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM news GROUP BY category"
    ).fetchall()
    for row in rows:
        stats['by_category'][row['category']] = row['cnt']

    # Priority breakdown
    stats['by_priority'] = {}
    rows = conn.execute(
        "SELECT priority_label, COUNT(*) as cnt FROM news GROUP BY priority_label"
    ).fetchall()
    for row in rows:
        stats['by_priority'][row['priority_label']] = row['cnt']

    conn.close()
    return stats


# ============================================================
# SOURCE CRUD Operations
# ============================================================

def get_sources(include_disabled=True):
    """Get all feed sources."""
    conn = get_db()
    if include_disabled:
        rows = conn.execute("SELECT * FROM sources ORDER BY name").fetchall()
    else:
        rows = conn.execute("SELECT * FROM sources WHERE enabled = 1 ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_source(source):
    """Add a new feed source."""
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO sources (name, url, category, feed_type, region, enabled, auto_discovered)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            source['name'], source['url'], source.get('category', 'web_news'),
            source.get('feed_type', 'rss'), source.get('region', 'global'),
            1 if source.get('enabled', True) else 0,
            1 if source.get('auto_discovered', False) else 0,
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_source(source_id, data):
    """Update an existing feed source."""
    conn = get_db()
    fields = []
    params = []
    for key in ['name', 'url', 'category', 'feed_type', 'region', 'enabled']:
        if key in data:
            fields.append(f"{key} = ?")
            params.append(data[key])
    if fields:
        params.append(source_id)
        conn.execute(f"UPDATE sources SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
    conn.close()


def delete_source(source_id):
    """Delete a feed source."""
    conn = get_db()
    conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))
    conn.commit()
    conn.close()


def update_source_fetch_status(source_id, error=None):
    """Update the last fetched time and error status for a source."""
    conn = get_db()
    conn.execute('''
        UPDATE sources SET last_fetched = ?, fetch_error = ? WHERE id = ?
    ''', (datetime.utcnow().isoformat(), error, source_id))
    conn.commit()
    conn.close()


# ============================================================
# SETTINGS CRUD Operations
# ============================================================

def get_settings():
    """Get all application settings."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM settings ORDER BY key").fetchall()
    conn.close()
    return {row['key']: {'value': row['value'], 'description': row['description']} for row in rows}


def get_setting(key, default=None):
    """Get a single setting value."""
    conn = get_db()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row['value'] if row else default


def update_setting(key, value, description=None):
    """Update a setting value."""
    conn = get_db()
    if description:
        conn.execute('''
            INSERT INTO settings (key, value, description, updated_date)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = ?, description = ?, updated_date = CURRENT_TIMESTAMP
        ''', (key, value, description, value, description))
    else:
        conn.execute('''
            INSERT INTO settings (key, value, updated_date)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = ?, updated_date = CURRENT_TIMESTAMP
        ''', (key, value, value))
    conn.commit()
    conn.close()


# ============================================================
# PRIORITY RULES CRUD Operations
# ============================================================

def get_priority_rules():
    """Get all priority rules."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM priority_rules ORDER BY score DESC, keyword"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_priority_rule(level, keyword, score, is_user_defined=True):
    """Add a new priority rule."""
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO priority_rules (level, keyword, score, is_user_defined)
            VALUES (?, ?, ?, ?)
        ''', (level, keyword, score, 1 if is_user_defined else 0))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def update_priority_rule(rule_id, data):
    """Update a priority rule."""
    conn = get_db()
    fields = []
    params = []
    for key in ['level', 'keyword', 'score']:
        if key in data:
            fields.append(f"{key} = ?")
            params.append(data[key])
    if fields:
        params.append(rule_id)
        conn.execute(f"UPDATE priority_rules SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
    conn.close()


def delete_priority_rule(rule_id):
    """Delete a priority rule."""
    conn = get_db()
    conn.execute("DELETE FROM priority_rules WHERE id = ?", (rule_id,))
    conn.commit()
    conn.close()


def increment_rule_hit(rule_id):
    """Increment the hit count for a priority rule."""
    conn = get_db()
    conn.execute('''
        UPDATE priority_rules
        SET hit_count = hit_count + 1, last_hit_date = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (rule_id,))
    conn.commit()
    conn.close()


# ============================================================
# DISCOVERED FEEDS Operations
# ============================================================

def get_discovered_feeds(approved_only=False):
    """Get discovered feeds."""
    conn = get_db()
    if approved_only:
        rows = conn.execute(
            "SELECT * FROM discovered_feeds WHERE approved = 1 ORDER BY discovery_date DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM discovered_feeds ORDER BY approved, discovery_date DESC"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_discovered_feed(feed):
    """Add a newly discovered feed."""
    conn = get_db()
    try:
        conn.execute('''
            INSERT OR IGNORE INTO discovered_feeds (name, url, category, region, discovered_from)
            VALUES (?, ?, ?, ?, ?)
        ''', (feed['name'], feed['url'], feed.get('category', 'web_news'),
              feed.get('region', 'global'), feed.get('discovered_from', '')))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def approve_discovered_feed(feed_id):
    """Approve a discovered feed and add it to active sources."""
    conn = get_db()
    feed = conn.execute("SELECT * FROM discovered_feeds WHERE id = ?", (feed_id,)).fetchone()
    if feed:
        conn.execute("UPDATE discovered_feeds SET approved = 1 WHERE id = ?", (feed_id,))
        conn.execute('''
            INSERT OR IGNORE INTO sources (name, url, category, feed_type, region, enabled, auto_discovered)
            VALUES (?, ?, ?, 'rss', ?, 1, 1)
        ''', (feed['name'], feed['url'], feed['category'], feed['region']))
        conn.commit()
    conn.close()


def reject_discovered_feed(feed_id):
    """Remove a discovered feed."""
    conn = get_db()
    conn.execute("DELETE FROM discovered_feeds WHERE id = ?", (feed_id,))
    conn.commit()
    conn.close()


# ============================================================
# MAINTENANCE
# ============================================================

def cleanup_old_news():
    """Remove news articles older than the retention period."""
    conn = get_db()
    retention = int(get_setting('news_retention_days', NEWS_RETENTION_DAYS))
    cutoff = (datetime.utcnow() - timedelta(days=retention)).isoformat()
    conn.execute("DELETE FROM news WHERE fetched_date < ?", (cutoff,))
    conn.commit()
    conn.close()


def log_priority_analysis(rules_added, rules_modified, rules_removed, summary):
    """Log a priority analysis run."""
    conn = get_db()
    conn.execute('''
        INSERT INTO priority_analysis_log (rules_added, rules_modified, rules_removed, summary)
        VALUES (?, ?, ?, ?)
    ''', (rules_added, rules_modified, rules_removed, summary))
    conn.commit()
    conn.close()


def get_analysis_logs(limit=10):
    """Get recent priority analysis logs."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM priority_analysis_log ORDER BY analysis_date DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
