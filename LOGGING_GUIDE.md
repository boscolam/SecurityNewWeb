# Logging & Troubleshooting Guide

Comprehensive guide to the logging system in Cybersecurity News Dashboard v2.3.0+

---

## 📋 **Log Files Overview**

The application maintains separate log files for different components:

### **Log File Locations**

All logs are stored in `logs/` directory:

```
logs/
├── app.log        # Main application log
├── error.log      # Errors and exceptions
├── access.log     # HTTP access log
├── update.log     # Git updates and auto-updates
└── feed.log       # RSS feed operations
```

### **Log Rotation**

- **Max Size**: 10MB per file
- **Backups**: 5 rotated files kept
- **Format**: `app.log`, `app.log.1`, `app.log.2`, etc.

---

## 🖥️ **Web Interface**

### **Access Logs Page**

```
http://localhost:5000/logs
```

**Features:**
- ✅ Real-time log viewing
- ✅ Auto-refresh every 5 seconds
- ✅ Auto-scroll to latest entries
- ✅ Search/filter logs
- ✅ Color-coded by level (ERROR=red, WARNING=yellow, INFO=blue)
- ✅ Download logs
- ✅ Clear logs
- ✅ View statistics (total lines, error count, warning count)

---

## 📝 **Log Types**

### **1. Application Log (app.log)**

**Purpose**: General application events

**What's Logged:**
- Application startup/shutdown
- Scheduler events
- Feed refresh operations
- Priority analysis runs
- General operational messages

**Example:**
```
2026-09-22 10:30:00 - app - INFO - [app.py:465] - Scheduler started. Feed refresh every 30 minutes.
2026-09-22 10:30:05 - app - INFO - [feed_manager.py:34] - Fetching all feeds
```

**When to Check:**
- Application not starting
- Scheduler not running
- General operational issues

---

### **2. Error Log (error.log)**

**Purpose**: Errors and exceptions

**What's Logged:**
- Python exceptions and tracebacks
- Critical errors
- Database errors
- Module import errors
- Permission errors

**Example:**
```
2026-09-22 10:35:12 - error - ERROR - [database.py:16] - sqlite3.OperationalError: unable to open database file
Traceback (most recent call last):
  File "database.py", line 16, in get_db
    conn = sqlite3.connect(DATABASE_PATH)
sqlite3.OperationalError: unable to open database file
```

**When to Check:**
- Application crashes
- Features not working
- Database issues
- Service won't start

**Common Errors:**
```
Permission denied          → Fix with: sudo chown -R $USER:$(id -gn) .
Module not found          → Fix with: pip install -r requirements.txt
Database is locked        → Fix with: ./service.sh restart
Unable to open database   → Fix with: chmod 644 cybersec_news.db
```

---

### **3. Access Log (access.log)**

**Purpose**: HTTP requests to the dashboard

**What's Logged:**
- Page visits
- API calls
- Response codes
- IP addresses

**Example:**
```
2026-09-22 10:40:23 - access - INFO - GET / HTTP/1.1 200
2026-09-22 10:40:25 - access - INFO - GET /news HTTP/1.1 200
2026-09-22 10:40:30 - access - INFO - POST /api/fetch-feeds HTTP/1.1 200
```

**When to Check:**
- Unusual access patterns
- API performance issues
- Security monitoring

---

### **4. Update Log (update.log)**

**Purpose**: Git updates and auto-update operations

**What's Logged:**
- Update checks
- Git pull operations
- Update successes/failures
- Service restart after updates
- Commit information

**Example:**
```
2026-09-22 11:00:00 - update - INFO - Checking for updates
2026-09-22 11:00:02 - update - INFO - Updates available: 2 new commits
2026-09-22 11:00:05 - update - INFO - Git pull successful: Updated from abc1234 to def5678
2026-09-22 11:00:10 - update - INFO - Service restarted successfully
```

**When to Check:**
- Auto-update not working
- Update failures
- Service restart issues
- Version verification

---

### **5. Feed Log (feed.log)**

**Purpose**: RSS feed fetch operations

**What's Logged:**
- Feed fetch start/end
- Successful fetches
- Failed fetches
- Timeout errors
- Parse errors
- New articles found

**Example:**
```
2026-09-22 11:15:00 - feed - INFO - [The Hacker News] Fetching feed
2026-09-22 11:15:02 - feed - INFO - [The Hacker News] Found 15 new articles
2026-09-22 11:15:05 - feed - ERROR - [BrokenFeed] Fetch failed: HTTP 404
2026-09-22 11:15:10 - feed - WARNING - [SlowFeed] Timeout after 30 seconds
```

**When to Check:**
- Feeds not updating
- Specific source not working
- Slow feed performance

---

## 🔍 **Log Levels**

### **Priority Order** (most to least severe)

1. **CRITICAL** - System failure, requires immediate attention
2. **ERROR** - Error occurred, feature may not work
3. **WARNING** - Potential issue, may cause problems
4. **INFO** - Informational message, normal operation
5. **DEBUG** - Detailed debugging information

### **Color Coding in Web Interface**

- 🔴 **CRITICAL/ERROR** - Red background
- 🟡 **WARNING** - Yellow background
- 🔵 **INFO** - Blue text
- 🟢 **DEBUG** - Green text

---

## 🛠️ **Troubleshooting with Logs**

### **Problem: Application Won't Start**

**Logs to Check:**
1. `error.log` - Look for startup errors
2. `app.log` - Check last messages before crash

**Commands:**
```bash
# View error log
tail -50 logs/error.log

# Or use web interface
http://localhost:5000/logs
```

**Common Issues:**
```
ModuleNotFoundError        → pip install -r requirements.txt
Permission denied          → sudo chown -R $USER:$(id -gn) .
Port already in use        → pkill -f app.py
Database locked            → rm cybersec_news.db-shm cybersec_news.db-wal
```

---

### **Problem: Feeds Not Updating**

**Logs to Check:**
1. `feed.log` - Check feed fetch operations
2. `app.log` - Check if scheduler is running

**Commands:**
```bash
# Check feed log for errors
grep ERROR logs/feed.log

# Check specific feed
grep "The Hacker News" logs/feed.log

# Manual fetch
curl http://localhost:5000/api/fetch-feeds -X POST
```

---

### **Problem: Auto-Update Not Working**

**Logs to Check:**
1. `update.log` - Check update attempts
2. `error.log` - Check for git errors

**Commands:**
```bash
# View update log
cat logs/update.log

# Check for errors
grep ERROR logs/update.log

# Test git manually
git fetch origin
git status
```

---

### **Problem: High Memory/CPU Usage**

**Logs to Check:**
1. `app.log` - Check for loops or stuck operations
2. `feed.log` - Check for stuck feed fetches

**Commands:**
```bash
# Check performance
./service.sh analyze

# Check specific operations
grep "Fetching" logs/feed.log
```

---

## 📊 **Log Analysis Tips**

### **Find Recent Errors**

```bash
# Last hour of errors
tail -1000 logs/error.log | grep "$(date +%Y-%m-%d)"

# Count errors by type
grep ERROR logs/error.log | cut -d'-' -f4 | sort | uniq -c

# Find specific error
grep "Permission denied" logs/error.log
```

### **Monitor Specific Feed**

```bash
# Watch specific feed
grep "Source Name" logs/feed.log

# Count failures
grep "Fetch failed" logs/feed.log | wc -l

# Recent feed activity
tail -100 logs/feed.log
```

### **Check Update History**

```bash
# View all updates
cat logs/update.log

# Last update
tail -20 logs/update.log

# Failed updates
grep "failed" logs/update.log
```

---

## 🔄 **Real-Time Monitoring**

### **Web Interface (Recommended)**

```
http://localhost:5000/logs
```

Features:
- Auto-refresh every 5 seconds
- Color-coded entries
- Search functionality
- Multiple log files in tabs
- Download/clear options

### **Command Line**

```bash
# Watch application log
tail -f logs/app.log

# Watch error log
tail -f logs/error.log

# Watch all logs
tail -f logs/*.log

# Service logs (if using systemd)
./service.sh logs
journalctl --user -u cybersec-news -f
```

---

## 🧹 **Log Management**

### **Clear Logs**

**Web Interface:**
```
http://localhost:5000/logs → Select log → Clear button
```

**Command Line:**
```bash
# Clear specific log
> logs/app.log

# Clear all logs
for log in logs/*.log; do > $log; done

# Keep last 100 lines
tail -100 logs/app.log > /tmp/app.log && mv /tmp/app.log logs/app.log
```

### **Backup Logs**

```bash
# Backup all logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Backup before update
cp -r logs logs.backup.$(date +%Y%m%d)
```

### **Log Rotation**

Automatic rotation happens at 10MB:
- `app.log` → `app.log.1` → `app.log.2` → ... → `app.log.5`
- Oldest log (`app.log.5`) is deleted

**Manual rotation:**
```bash
# Force rotation
python3 << EOF
from logger_config import app_logger
app_logger.handlers[0].doRollover()
EOF
```

---

## 🚨 **Important Logs for Troubleshooting**

### **Service Won't Start**
1. `error.log` - Find the exception
2. `app.log` - Check initialization

### **Feeds Not Working**
1. `feed.log` - Check fetch attempts
2. `error.log` - Look for network/parse errors

### **Updates Failing**
1. `update.log` - Check git operations
2. `error.log` - Look for permissions/conflicts

### **Performance Issues**
1. `app.log` - Check for stuck operations
2. `feed.log` - Look for slow/hanging fetches

### **Database Problems**
1. `error.log` - Check for SQLite errors
2. `app.log` - Check for lock messages

---

## 💡 **Best Practices**

1. **Check logs regularly** - Use web interface for quick health checks
2. **Enable auto-refresh** - Monitor in real-time during troubleshooting
3. **Search before scrolling** - Use search feature to find specific issues
4. **Check error log first** - Start with errors, then work to other logs
5. **Download logs for support** - Share logs when asking for help
6. **Clear old logs** - Reduce clutter and improve search performance
7. **Backup before major changes** - Keep logs before updates/migrations

---

## 📞 **Getting Help**

When reporting issues, include:

1. **Error messages** from `error.log`
2. **Recent entries** from relevant log (app/feed/update)
3. **System info**: OS, Python version, installation path
4. **Steps to reproduce** the issue

**Export logs for support:**
```bash
# Create diagnostic bundle
tar -czf diagnostic-$(date +%Y%m%d).tar.gz \
    logs/ \
    cybersec_news.db \
    config.py \
    VERSION

# Send diagnostic-YYYYMMDD.tar.gz when reporting issues
```

---

---

## 🖥️ **Real-Time Log Monitoring from Linux/macOS CLI**

For administrators who prefer the terminal, you can monitor logs in real-time using `tail -f`:

```bash
# Watch the main application log
tail -f logs/app.log

# Watch errors only (useful for debugging)
tail -f logs/error.log

# Watch feed fetch operations
tail -f logs/feed.log

# Watch HTTP access requests
tail -f logs/access.log

# Watch auto-update activity
tail -f logs/update.log

# Watch ALL logs simultaneously
tail -f logs/*.log

# Watch with grep filter (e.g., only ERROR lines)
tail -f logs/app.log | grep --line-buffered ERROR

# Service logs (if running as systemd service)
journalctl --user -u cybersec-news -f
```

**Tip**: Use `multitail` for a split-screen view of multiple log files:
```bash
# Install multitail (Ubuntu/Debian)
sudo apt install multitail

# Monitor multiple logs in split view
multitail logs/app.log logs/error.log logs/feed.log
```

---

**Version**: 2.8.2 (All module loggers now properly propagate to log files since v2.6.0. Logs accessible under Settings → Logs tab since v2.4.1)  
**Updated**: 2026-09-23
