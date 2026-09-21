# Changelog

All notable changes to the Cybersecurity News Dashboard will be documented in this file.

## [2.3.0] - 2026-09-22

### Added - Comprehensive Logging Architecture

Implemented comprehensive logging system with real-time web viewing and auto-restart after updates.

#### New Features
- **Structured Logging System**: Centralized logging with multiple log files
  - `app.log` - Application events and operations
  - `error.log` - Errors and exceptions with tracebacks
  - `access.log` - HTTP request logging
  - `update.log` - Git update operations and history
  - `feed.log` - RSS feed fetch operations
  - Automatic log rotation (10MB max, 5 backups per file)
  - Detailed and simple log formats

- **Web-Based Log Viewer**: Real-time log monitoring at `/logs`
  - View any log file in the browser
  - Auto-refresh every 5 seconds
  - Auto-scroll to latest entries
  - Search/filter logs by keyword
  - Color-coded by level (ERROR=red, WARNING=yellow, INFO=blue, DEBUG=green)
  - Statistics: total lines, error count, warning count
  - Download logs as files
  - Clear logs from web interface
  - Line count selector (50, 100, 200, 500, 1000 lines)
  - Toggle auto-refresh and auto-scroll

- **Auto-Restart After Updates**: Automatic service restart capability
  - Detects if running as systemd service (user or system mode)
  - Automatically restarts service after successful git pull
  - Configurable via `restart_after_update` setting
  - Logs restart operations to update.log
  - Graceful fallback if not running as service

#### Components Added
- `logger_config.py`: Core logging configuration module
  - `setup_logger()` - Configure loggers with rotation
  - `log_app()`, `log_error()`, `log_access()`, `log_update()`, `log_feed()` - Helper functions
  - `get_log_files()` - List log files with metadata
  - `get_log_tail()` - Read last N lines from log
  - `clear_log()` - Clear log file content
  
- `templates/logs.html`: Web interface for log viewing
  - Responsive design with dark code-style viewer
  - Real-time updates with JavaScript
  - Multiple controls and filters
  - Troubleshooting tips section
  - Log level badges and color coding

#### API Endpoints Added
- `GET /logs` - Logs viewing page
- `GET /api/logs/list` - List all log files with metadata
- `GET /api/logs/<log_name>?lines=N` - Get last N lines from log
- `GET /api/logs/<log_name>/download` - Download log file
- `POST /api/logs/<log_name>/clear` - Clear log file

#### Enhanced git_updater.py
- `restart_service()` - Restart systemd service method
- `_detect_service_mode()` - Detect user/system service mode
- Integrated with logger_config for structured update logging
- Auto-restart after successful update if enabled
- Logs all git operations to update.log

#### Documentation Added
- **LOGGING_GUIDE.md**: Comprehensive 480-line logging guide
  - Log files overview and rotation
  - Web interface features
  - Detailed description of each log type
  - Log levels explanation
  - Troubleshooting with logs
  - Log analysis tips
  - Real-time monitoring
  - Log management (clear, backup, rotation)
  - Best practices
  - Diagnostic bundle creation

#### Navigation Updated
- Added "Logs" link to main navigation in `base.html`
- Icon: 📋 (file-alt)
- Accessible from any page

#### Benefits
✅ **Better Troubleshooting**: Dedicated log files for each component  
✅ **Real-Time Monitoring**: Watch logs live in browser  
✅ **Search & Filter**: Find specific errors quickly  
✅ **Auto-Restart**: Service automatically restarts after updates  
✅ **Log Rotation**: Prevents disk space issues  
✅ **Color Coding**: Easy identification of errors/warnings  
✅ **Downloadable**: Export logs for support  
✅ **Comprehensive Guide**: Complete documentation for troubleshooting  

#### Usage Examples

**View Logs in Browser:**
```
http://localhost:5000/logs
```

**Check Update Log:**
```bash
tail -f logs/update.log
```

**View Error Log:**
```bash
grep ERROR logs/error.log
```

**Monitor Feed Operations:**
```bash
grep "Fetching" logs/feed.log
```

**Enable Auto-Restart After Updates:**
```
Go to /settings
Set "restart_after_update" to "true"
```

### Modified
- app.py: Added logging routes and API endpoints
- templates/base.html: Added Logs navigation link
- git_updater.py: Enhanced with auto-restart and structured logging
- VERSION: Updated to 2.3.0

---

## [2.2.3] - 2026-09-22

### Added - Comprehensive Health Check & Analysis

Enhanced service.sh with comprehensive health checking and system analysis capabilities.

#### New Commands
- **`./service.sh health`**: Complete health check with 10-point inspection
  - Service installation check
  - Service status check
  - Application process check
  - Port availability check (5000)
  - Virtual environment check
  - Database check with statistics
  - Python dependencies check
  - Recent error logs scan
  - Disk space check
  - Web access test (HTTP 200)
  - Color-coded results (✓ success, ✗ error, ⚠ warning)
  - Summary with status: ALL SYSTEMS OPERATIONAL / OPERATIONAL WITH WARNINGS / ISSUES DETECTED

- **`./service.sh analyze`**: Detailed analysis with recommendations
  - Service failure reason detection
  - Recent error log analysis
  - Configuration checks (venv, database, permissions)
  - Database integrity check
  - Owner/permission validation
  - Performance metrics (memory, CPU, uptime)
  - News feed statistics (sources, articles, recent activity)
  - Specific fix recommendations
  - Maintenance tips

#### Features
✅ **10-Point Health Inspection**
  1. Service Installation
  2. Service Status
  3. Application Process
  4. Port 5000 Availability
  5. Virtual Environment
  6. Database
  7. Python Dependencies
  8. Recent Error Logs
  9. Disk Space
  10. Web Access

✅ **Detailed Metrics**
  - Memory usage (MB)
  - CPU usage (%)
  - Process uptime
  - Database size
  - Source count (total/enabled)
  - News article count (total/24h)

✅ **Smart Recommendations**
  - Context-aware fix suggestions
  - Specific command examples
  - Issue prioritization
  - Maintenance tips

#### Usage Examples

**Quick Health Check:**
```bash
./service.sh health
```

Output:
```
[1/10] Service Installation
✓ Service installed (user mode)

[2/10] Service Status
✓ Service is running

[3/10] Application Process
✓ Process running (PID: 12345)

...

============================================
  Health Check Summary
============================================
✓ ALL SYSTEMS OPERATIONAL

Your Cybersecurity News Dashboard is healthy!
```

**Detailed Analysis:**
```bash
./service.sh analyze
```

Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configuration Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Virtual environment OK
✓ Database exists
✓ Database integrity OK
✓ Permissions OK (owner: bosco)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Performance Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Memory Usage: 85MB
✓ Memory usage normal
CPU Usage: 2.3%
Uptime: 2:15:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
News Feed Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Sources: 140
Enabled Sources: 140
Total News Articles: 2,543
News (Last 24h): 127
✓ Feeds are being updated
```

#### Benefits
✅ **Quick Problem Detection**: Identify issues in seconds  
✅ **Proactive Monitoring**: Check health before problems occur  
✅ **Smart Diagnostics**: Get specific fix recommendations  
✅ **Performance Insight**: Monitor memory, CPU, and database  
✅ **User-Friendly**: Color-coded output, clear summaries  
✅ **Comprehensive**: 10 checks cover all critical components  

### Modified
- service.sh: Added health and analyze commands
- CHANGELOG.md: Documented v2.2.3
- VERSION: Updated to 2.2.3
- README.md: Updated version badge

---

## [2.2.2] - 2026-09-22

### Fixed - Automatic User/Group/Path Detection

Removed all hardcoded usernames, groups, and paths from service files and installation scripts.

#### Service Files Enhanced
- **cybersec-news.service**: Now uses placeholders instead of hardcoded values
  - `__INSTALL_USER__` replaced with detected user
  - `__INSTALL_GROUP__` replaced with detected group  
  - `__INSTALL_PATH__` replaced with actual installation path
  
- **cybersec-news-user.service**: Now uses placeholders
  - `__INSTALL_PATH__` replaced with actual path
  - No more `%h/SecurityNewWeb` assumption

#### Setup Script Improved
- Automatically detects current user with `$USER` or `$(whoami)`
- Automatically detects current group with `$(id -gn)`
- Automatically detects installation path with `$(pwd)`
- Replaces all placeholders during service installation
- Shows detected configuration before installing
- Works with any username, group, or installation path

#### Benefits
✅ **No Manual Editing**: Service files auto-configured  
✅ **Any User**: Works with any username (bosco, ubuntu, www-data, etc.)  
✅ **Any Path**: Works with any installation directory  
✅ **No Hardcoding**: All values dynamically detected  
✅ **Error Prevention**: Eliminates permission issues from wrong usernames  

#### New Documentation
- **PERMISSIONS_FIX.md**: Complete guide for permission issues
  - Automatic detection examples
  - Fix scripts for common problems
  - Troubleshooting permission errors
  - Complete fix script included

#### Installation Examples

**Before (v2.2.1):**
```bash
# Had to manually edit service files for custom paths
# Hardcoded www-data user caused permission issues
```

**After (v2.2.2):**
```bash
cd /any/path/SecurityNewWeb
./setup.sh --service
# Automatically detects and configures everything!
```

#### Technical Changes
- Service template files use placeholder variables
- setup.sh performs sed substitution during install
- Detects user: `${USER:-$(whoami)}`
- Detects group: `$(id -gn)`
- Detects path: absolute path of current directory

### Modified
- cybersec-news.service: Template with placeholders
- cybersec-news-user.service: Template with placeholders
- setup.sh: Auto-detection and substitution logic
- PERMISSIONS_FIX.md: New troubleshooting guide

---

## [2.2.1] - 2026-09-22

### Added - Quick Fix Documentation

Added comprehensive troubleshooting guide for common update and installation issues.

#### New Documentation
- **QUICKFIX.md**: One-line solutions for 10 common issues
  - Git merge conflicts (most common)
  - Permission denied errors
  - Service startup problems
  - Port conflicts
  - Database locks
  - Module import errors
  - 404 errors after update
  - Git installation issues
  - Virtual environment problems
  - Service log errors
  - Nuclear option (clean reinstall)

#### Documentation Enhancements
- **UPDATE_INSTRUCTIONS.md**:
  - Added v2.2.0 features section
  - Prominent QUICKFIX.md reference
  - Enhanced merge conflict troubleshooting
  - One-line quick fix commands

- **README.md**:
  - Enhanced "Support & Troubleshooting" section
  - Added QUICKFIX.md reference
  - Listed common issues with solutions
  - Added all documentation links

#### User Experience Improvements
- Quick access to solutions for common problems
- One-command fixes for most issues
- Better error message guidance
- Clearer troubleshooting steps

### Modified
- UPDATE_INSTRUCTIONS.md: Enhanced with v2.2.0 info and quick fixes
- README.md: Better support section with troubleshooting
- Auto-update system verified to work across all versions

---

## [2.2.0] - 2026-09-22

### Added - Systemd Service Support

Implemented comprehensive systemd service support for running the application as a background service.

#### New Features
- **Systemd Service Files**: 
  - System-wide service (`cybersec-news.service`) for production
  - User service (`cybersec-news-user.service`) for home directory installations
  - Automatic startup on boot
  - Process management and monitoring
  
- **Enhanced Setup Script**:
  - `setup.sh` now supports `--service` and `--system-service` flags
  - Interactive installation with colored output
  - Automatic service installation and configuration
  - Production mode with Apache setup (`--production`)
  - Comprehensive error checking and validation

- **Service Management Script**:
  - New `service.sh` helper script for easy service management
  - Commands: status, start, stop, restart, logs, install, uninstall
  - Auto-detects service mode (user vs system)
  - Colored output for better readability

#### Service Features
- ✅ Automatic restart on failure (RestartSec=10)
- ✅ Runs on boot (system service)
- ✅ Runs on login (user service with linger)
- ✅ Proper logging via journald
- ✅ Security hardening (NoNewPrivileges, PrivateTmp, ProtectSystem)
- ✅ Resource limits (MemoryLimit=512M, LimitNOFILE=65535)
- ✅ Graceful shutdown handling

#### Installation Methods

**Quick Service Installation:**
```bash
# User service (home directory)
./setup.sh --service

# System service (production)
sudo ./setup.sh --system-service

# Full production setup (Apache)
sudo ./setup.sh --production
```

**Service Management:**
```bash
./service.sh status    # Check status
./service.sh restart   # Restart service
./service.sh logs      # View live logs
```

#### Components Added
- `cybersec-news.service`: System-wide service file
- `cybersec-news-user.service`: User service file
- `service.sh`: Service management helper script

#### Documentation Updates
- Enhanced `setup.sh` with service installation
- Updated `UBUNTU_INSTALL.md` with service instructions
- Added service management commands
- Updated quick start guide

#### Benefits
1. **Production Ready**: Run as proper daemon service
2. **Auto-Start**: Starts automatically on boot
3. **Reliability**: Automatic restart on crashes
4. **Management**: Easy control via systemctl
5. **Monitoring**: Integrated logging with journald
6. **Security**: Runs with proper permissions and isolation

### Modified
- `setup.sh`: Complete rewrite with service support
- `UBUNTU_INSTALL.md`: Added comprehensive service section
- `README.md`: Updated installation instructions

---

## [2.1.0] - 2026-09-21

### Added - Auto-Update Feature

Implemented comprehensive auto-update system with GitHub integration.

#### New Features
- **Auto-Update from GitHub**: Automatically check and install updates from repository
- **Web Configuration Interface**: Easy-to-use Updates page for configuration
- **Flexible Scheduling**: Choose update frequency (hourly, every 6 hours, daily, weekly)
- **Safety Features**: 
  - Automatic database backup before updates
  - Local changes automatically stashed
  - Git repository validation
  - Update history tracking
- **Manual Update Tools**: One-click update checks and installation
- **Update History**: View last 20 updates with commit details
- **API Endpoints**: Programmatic access to update functions

#### Components Added
- `git_updater.py`: Core update logic with GitUpdater class
- `templates/updates.html`: Web interface for update management
- API routes for Git operations
- Auto-update scheduler integration
- Database settings for update configuration

#### Configuration Options
- Enable/disable automatic updates
- Update check schedule (hourly/6h/daily/weekly)
- Backup database before update (recommended)
- Restart after update (requires systemd)
- Update logging and notifications

#### Documentation
- `AUTO_UPDATE_GUIDE.md`: Comprehensive guide for auto-update feature
- Troubleshooting section
- API documentation
- Security considerations
- FAQ section

#### Benefits
1. **Stay Current**: Automatically receive latest features and security patches
2. **Safe Updates**: Database backups prevent data loss
3. **Easy Management**: Web interface for non-technical users
4. **Flexible Control**: Manual or automatic update options
5. **Audit Trail**: Complete history of all updates

### Modified
- `app.py`: Added update routes and scheduler
- `database.py`: Added auto-update settings to defaults
- `templates/base.html`: Added Updates navigation link

---

## [2.0.0] - 2026-09-21

### Added - Government CERT Feeds Integration

Integrated comprehensive government CERT RSS feeds from [Pulsedive certrss](https://github.com/pulsedive/certrss) repository.

#### New Features
- **50+ Government CERT RSS Feeds**: Added official government Computer Emergency Response Team feeds from around the world
- **New Category**: Added "Government CERT" category for better organization
- **Global Coverage**: Enhanced international coverage with official government security advisories

#### Feed Statistics
Total feeds added: **52 new government CERT feeds**

**By Region**:
- **North America** (4 feeds):
  - CISA (US) - News & Advisories
  - Canadian Cyber Centre - News & Alerts

- **Europe** (32 feeds):
  - CERT-EU, UK NCSC, Finland NCSC, CERT-FR
  - CERT.at, CERT.BE, NCSC NL, Swiss GovCERT
  - CERT.PL, CERT.hr, NUKIB (Czech), DKCERT
  - CERT-EE, CSIRT Italia, CERT.LV
  - NSM NCSC (Norway), CERT.RO, SI-CERT
  - CCN-CERT & INCIBE-CERT (Spain), CERT-SE
  - CERT-UA, NCSC Hungary, CNCS Portugal

- **Asia Pacific** (6 feeds):
  - AusCERT, JPCERT/CC, SingCERT
  - GovCERT.HK, HKCERT, BGD e-GOV CIRT

- **South America** (1 feed):
  - CERT.br (Brazil)

- **Africa** (2 feeds):
  - EG-CERT (Egypt), NISSA (Libya)

#### Benefits
1. **Authoritative Sources**: Direct access to official government security advisories
2. **Early Warnings**: Government CERTs often publish early vulnerability warnings
3. **Regional Coverage**: Better coverage of regional cybersecurity threats
4. **Compliance**: Essential for organizations requiring government security updates
5. **Threat Intelligence**: Access to nation-state and critical infrastructure threats

#### Technical Changes
- Updated `config.py`:
  - Added 52 new government CERT feeds organized by region
  - Added "government" to NEWS_CATEGORIES
  - Maintained existing feed structure and organization
  - Added source attribution to Pulsedive certrss

#### Feed Types
All feeds categorized as "government" category with regional assignments:
- News feeds: General cybersecurity news and updates
- Advisory feeds: Security advisories and vulnerability warnings
- Alert feeds: Critical security alerts and incidents

### Modified
- `config.py`: Enhanced DEFAULT_FEEDS with government CERT sources
- `NEWS_CATEGORIES`: Added "Government CERT" category

### Documentation
- Added CHANGELOG.md to track version changes
- Updated README.md with new feed count (140+ total sources)
- Source attribution to https://github.com/pulsedive/certrss

---

## [1.0.0] - 2026-09-17

### Initial Release

#### Core Features
- Multi-source news aggregation (90+ feeds)
- Priority-based scoring system
- Region and category filtering
- Automatic feed discovery
- Background task scheduling
- SQLite database with WAL mode
- Web-based dashboard

#### Feed Categories
- Major cybersecurity news sites
- Vendor security research teams
- Dark web threat intelligence
- CVE databases and advisories
- Chinese cybersecurity vendors
- Social media and blog platforms

#### Regions
- Global
- North America
- Europe
- Asia Pacific
- China
- Middle East
- Africa
- South America

#### Components
- Flask web application
- APScheduler for background tasks
- RSS/Atom feed parser
- Priority scoring engine
- Auto-discovery system
- RESTful API
- Responsive web interface

---

## Version History

- **v2.0.0** (2026-09-21): Added 52 government CERT feeds, new category
- **v1.0.0** (2026-09-17): Initial release with 90+ feeds

---

## Upgrade Notes

### Upgrading from v1.0.0 to v2.0.0

**For Existing Installations**:

1. **Backup your database** (recommended):
   ```bash
   cp cybersec_news.db cybersec_news.db.backup
   ```

2. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

3. **No database migration required** - new feeds will be automatically added on next startup

4. **Restart application**:
   ```bash
   # For direct run:
   python app.py
   
   # For systemd:
   sudo systemctl restart cybersec-news
   
   # For Apache:
   sudo systemctl restart apache2
   ```

5. **Verify new feeds**:
   - Visit `/sources` page
   - Check for new "Government CERT" entries
   - All new feeds are enabled by default

**What Happens on Restart**:
- Application will detect 52 new feeds in config
- New feeds automatically inserted into database
- Immediate fetch of latest articles from government CERTs
- No data loss from existing feeds

**Optional - Reset Database** (if you want fresh start):
```bash
# Backup first!
cp cybersec_news.db cybersec_news.db.backup

# Remove database
rm cybersec_news.db*

# Restart application (will recreate with all feeds)
python app.py
```

---

## Future Roadmap

### v2.1.0 (Planned)
- [ ] Email notifications for critical alerts
- [ ] Slack webhook integration
- [ ] Custom alert rules per CERT

### v2.2.0 (Planned)
- [ ] API authentication
- [ ] User accounts and preferences
- [ ] Saved searches and filters

### v3.0.0 (Planned)
- [ ] Machine learning for priority prediction
- [ ] Natural language processing for better classification
- [ ] Advanced analytics dashboard
- [ ] Threat actor tracking
- [ ] Integration with SIEM platforms

---

## Credits

- **Government CERT Feeds**: [Pulsedive certrss](https://github.com/pulsedive/certrss)
- **Contributors**: Pulsedive, Curated Intelligence, CyberSquarePeg
- **CERT Feed Registry**: DCOD (2026-08-16 refresh)

---

## License

This project is licensed under the MIT License.
