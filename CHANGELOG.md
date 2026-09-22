# Changelog

All notable changes to the Cybersecurity News Dashboard will be documented in this file.

## [2.5.1] - 2026-09-22

### Fixed - Attack Map BuildError

- **Fixed BuildError on all pages** when service hasn't restarted after update
  - Changed Attack Map nav link from `url_for('attack_map_page')` to hardcoded `/attack-map` URL
  - Prevents `werkzeug.routing.exceptions.BuildError` from crashing every page
  - Other nav links using `url_for()` for established routes remain unchanged

---

## [2.5.0] - 2026-09-22

### Added - Real-Time Cyber Attack Map

#### Attack Map Visualization
- **New Attack Map page** (`/attack-map`) with real-time animated threat visualization
  - Dark-themed full-page canvas with equirectangular world map projection
  - 85+ city dots forming a recognizable world map pattern
  - Animated bezier arc attacks from source to destination countries
  - Glowing particle effects with trailing light paths
  - Source pulse animation on attack origin
  - Impact ripple effect at attack destination
  - Auto-refresh every 30 seconds for continuous updates

#### Threat Intelligence Data
- **Attack data derived from actual news** in the database
  - Analyzes hacking incidents and critical/high-priority news from last 30 days
  - Keyword-based attacker detection (APT groups, country names, threat actors)
  - Target detection from article region, title keywords, and content analysis
  - Supports Russia, China, North Korea, Iran as detected attack origins
  - Maps 35 countries with geographic coordinates

#### Interface Panels
- **Threat Overview** panel (top-left): total threats, critical count, high count, country count
- **Top Attack Origins** panel (bottom-left): ranked attacker countries with bar charts
- **Live Attack Feed** panel (right): scrolling log of attacks with severity badges
- **Legend** (bottom-center): color-coded severity levels (Critical, High, Medium, Low)
- **Pause/Resume** control button

#### Navigation
- New **Attack Map** link in main navigation bar between Priorities and Settings
- Full-page layout hides footer for maximum map area

#### Technical Details
- API endpoint: `GET /api/attack-data` returns structured attack events with coordinates
- Canvas rendering with `requestAnimationFrame` for smooth 60fps animation
- Device pixel ratio handling for sharp rendering on HiDPI displays
- Responsive design: panels collapse on mobile screens
- Memory-efficient arc lifecycle management (max 35 concurrent arcs)

---

## [2.4.1] - 2026-09-22

### Improved - Settings Consolidation & URL Display Fix

#### Navigation Reorganization
- **Moved Updates and Logs under Settings page** as tabs
  - Settings page now has 4 tabs: Application Settings, Feed Sources, Updates, Logs
  - Top navigation simplified: removed separate Updates and Logs menu items
  - All configuration and system pages grouped under one Settings entry
  - Consistent tabbed navigation across all 4 sub-pages

#### URL Display Fix
- **Fixed long URLs overflowing** in Auto-Discovered Feeds cards
  - URLs now display on **multiple lines** using CSS `word-break: break-all`
  - Full URL visible without overflow or truncation
  - URL displayed in styled box with monospace font for readability
  - "Found via" text also wraps properly on multiple lines
  - Source table URLs also wrap instead of being truncated

#### Navigation Before vs After
```
Before: Dashboard | News | CVE | Priorities | Settings | Updates | Logs
After:  Dashboard | News | CVE | Priorities | Settings
                                               └─> [App Settings] [Sources] [Updates] [Logs]
```

#### Files Modified
- templates/base.html: Removed Updates/Logs from top nav
- templates/settings.html: Added Updates/Logs tabs
- templates/sources.html: Added Updates/Logs tabs, fixed URL display
- templates/updates.html: Added Settings tabs header
- templates/logs.html: Added Settings tabs header
- static/css/style.css: Added URL wrapping styles for discovered feeds and source table

---

## [2.4.0] - 2026-09-22

### Added - Interactive UI with Clickable Badges & Filters

Major UI enhancement making all badges, tags, and metadata clickable for instant filtering.

#### Clickable Elements
- **Priority Badges**: Click to filter by priority level (Critical, High, Medium, Low)
- **Category Badges**: Click to filter by category (Web News, Blog, Vendor Research, Government, CVE, etc.)
- **Region Badges**: Click to filter by geographic region
- **Hacking Incident Badge**: Click to show only hacking incidents
- **CVE Badge**: Click to show only CVE-related articles
- **Source Names**: Click to filter news from specific source
- **CVE Tags**: Click to search for specific CVE ID
- **Vendor Tags**: Click to filter by vendor (Cisco, Palo Alto, Fortinet, etc.)

#### Visual Enhancements
- **Hover Effects**: All clickable elements show visual feedback
- **Transform Animation**: Elements lift on hover (translateY -2px)
- **Glow Effects**: Color-coded shadows on hover
- **Cursor Pointer**: Clear indication of clickability
- **Ripple Effect**: Badge click animation
- **Tooltips**: Descriptive hints on hover
- **Focus States**: Accessibility-friendly keyboard navigation
- **Mobile Optimized**: Larger touch targets on mobile devices

#### CSS Features
- **Dynamic Shadows**: Each badge type has unique hover glow
  - Critical/High priority: Red glow
  - Medium priority: Yellow glow
  - Low priority: Green glow
  - Info badges: Blue glow
- **Scale Transform**: Badges grow slightly on hover (1.05x)
- **Smooth Transitions**: 0.2s ease for all animations
- **Ripple Animation**: After-pseudo-element creates ripple effect
- **Click Hint Animation**: Pulse effect on focus
- **Loading States**: Spinner animation for async operations

#### JavaScript Functions
Added filter functions to all pages:
- `filterByPriority(priority)` - Filter by priority level
- `filterByCategory(category)` - Filter by news category
- `filterByRegion(region)` - Filter by geographic region
- `filterBySource(sourceId)` - Filter by specific source
- `filterByVendor(vendor)` - Filter by CVE vendor
- `filterByHacking()` - Show only hacking incidents
- `filterByCVE()` - Show only CVE articles
- `searchFor(term)` - Search for specific text/CVE

#### Pages Enhanced
1. **News Page** (`/news`):
   - All badges clickable
   - CVE tags search on click
   - Vendor tags filter on click
   - Source names filter on click
   - Preserves existing filters when adding new ones

2. **Dashboard** (`/`):
   - Top 10 news with clickable badges
   - Redirects to /news with appropriate filters
   - Stats cards unchanged (already had links)

3. **CVE Monitor** (`/cve`):
   - Priority badges filter CVE news
   - Vendor tags filter by vendor
   - CVE tags search within CVE page
   - Source names filter CVE news

#### CSS Additions
- **158 lines** of new CSS in `style.css`
- Comprehensive hover states for all clickable elements
- Mobile-responsive touch targets (min 32px height)
- Accessibility focus indicators
- Loading state animations
- Keyboard navigation support

#### User Experience
- **One-Click Filtering**: No need to use filter dropdowns
- **Contextual Navigation**: Click on what you see to explore more
- **Visual Feedback**: Immediate hover response
- **Intuitive**: Natural expectation that badges are clickable
- **Fast**: Direct URL manipulation, no AJAX delays
- **Mobile-Friendly**: Larger touch targets for mobile users

#### Accessibility
- **ARIA-friendly**: Focus visible indicators
- **Keyboard Navigation**: Tab through clickable elements
- **Screen Reader**: Title attributes provide context
- **High Contrast**: Clear visual distinction
- **Focus Rings**: 3px outline on focus-visible

#### Examples

**Click a Priority Badge**:
```
Click "HIGH" → Redirects to: /news?priority=high
```

**Click a Category Badge**:
```
Click "Vendor Research" → /news?category=vendor_research
```

**Click a CVE Tag**:
```
Click "CVE-2024-1234" → /news?search=CVE-2024-1234
```

**Click a Source Name**:
```
Click "The Hacker News" → /news?source_id=1
```

**Click a Vendor Tag**:
```
Click "Cisco" → /cve?vendor=cisco
```

#### Technical Implementation
- **Pure JavaScript**: No jQuery or external libraries
- **URL Manipulation**: Uses URL API for clean parameter handling
- **Page Reset**: Automatically resets to page 1 on filter change
- **Parameter Preservation**: Maintains existing filters when stacking
- **Lightweight**: Minimal performance impact
- **Cross-Browser**: Works on all modern browsers

#### Benefits
✅ **Faster Navigation**: One click instead of dropdown selection  
✅ **Better UX**: Intuitive, natural interaction  
✅ **Visual Polish**: Professional animations and effects  
✅ **Accessibility**: Full keyboard and screen reader support  
✅ **Mobile Optimized**: Touch-friendly interface  
✅ **Consistent**: Same behavior across all pages  
✅ **Discoverable**: Visual cues indicate clickability  

### Modified
- templates/news.html: Added clickable badges and JavaScript functions
- templates/dashboard.html: Added clickable badges and JavaScript functions
- templates/cve.html: Added clickable badges and JavaScript functions
- static/css/style.css: Added 158 lines of clickable element styles
- VERSION: Updated to 2.4.0
- README.md: Updated version badge
- CHANGELOG.md: Documented v2.4.0

---

## [2.3.2] - 2026-09-22

### Fixed - URL Length Issues & Navigation Reorganization

Fixed URL length issues in auto-discovered feeds and reorganized navigation for better usability.

#### Bug Fixes
- **URL Length Issues**: Fixed "URL too long" errors in Auto-Discovered Feeds section
  - Truncated `discovered_from` field to 200 characters maximum
  - Limited source names to 150 characters in linked feeds
  - Truncated feed names to 200 characters
  - Limited URL length to 500 characters in discovery
  - Added title attributes to show full text on hover
  - Improved display truncation in templates (name: 60 chars, URL: 70 chars, discovered_from: 40 chars)

#### Navigation Improvements
- **Reorganized Settings**: Moved Sources under Settings page
  - Sources is now a tab within Settings (Settings & Configuration)
  - Cleaner navigation with fewer top-level menu items
  - Tabbed interface: "Application Settings" and "Feed Sources"
  - Consistent navigation across both pages
  - Better organization of configuration options

#### UI Enhancements
- **Tabbed Navigation**: New tab system for Settings area
  - Active tab highlighting
  - Smooth transitions
  - Mobile-responsive tabs
  - Icon-based navigation
  - Hover effects and visual feedback

#### Technical Changes
- auto_discovery.py: Added truncation to prevent URL length issues
  - `_discover_from_page()`: Truncate name (200), URL (500)
  - `_discover_linked_feeds()`: Truncate name (200), URL (500)
  - `run_feed_discovery()`: Truncate discovered_from (200)
- templates/sources.html: Enhanced display with truncation and tooltips
- templates/settings.html: Added tabbed navigation
- templates/base.html: Updated navigation to combine Sources into Settings
- static/css/style.css: Added comprehensive tab styles with mobile support

#### Benefits
✅ **No More URL Length Errors**: All fields properly truncated  
✅ **Better Organization**: Settings and Sources logically grouped  
✅ **Cleaner Navigation**: Fewer menu items, better structure  
✅ **Full Text on Hover**: Title attributes show complete URLs  
✅ **Mobile Friendly**: Tabs work on all screen sizes  
✅ **Professional UI**: Modern tabbed interface  

#### Navigation Change
**Before:**
```
Dashboard | News | CVE Monitor | Sources | Priorities | Settings | Updates | Logs
```

**After:**
```
Dashboard | News | CVE Monitor | Priorities | Settings | Updates | Logs
                                              ↓
                                    [Application Settings] [Feed Sources]
```

#### Usage Examples

**Access Sources:**
```
1. Click "Settings" in navigation
2. Click "Feed Sources" tab
```

**View Full URLs:**
```
Hover over truncated text to see full content in tooltip
```

#### Files Modified
- auto_discovery.py: Added field truncation (5 locations)
- templates/sources.html: Added tabs, improved truncation
- templates/settings.html: Added tabs
- templates/base.html: Updated navigation
- static/css/style.css: Added tab styles (56 lines)
- VERSION: Updated to 2.3.2
- CHANGELOG.md: Documented v2.3.2
- README.md: Updated version badge

### Modified
- auto_discovery.py: Field truncation for URL length safety
- templates/sources.html: Tabbed interface and display truncation
- templates/settings.html: Tabbed interface
- templates/base.html: Navigation reorganization
- static/css/style.css: Tab navigation styles
- VERSION: Updated to 2.3.2
- README.md: Version badge

---

## [2.3.1] - 2026-09-22

### Fixed - Service Health Check & Verification

Fixed critical issues with service health checking and added service file verification.

#### Bug Fixes
- **Health Check Logic**: Fixed false negatives in service status detection
  - Previously reported "Service is not running" even when service was active
  - Now properly detects all service states: active, inactive, failed, activating
  - Shows detailed state information instead of just pass/fail
  - Better handling of edge cases and error states

#### New Features
- **Service File Verification**: New `verify` command to check service file integrity
  - Detects unreplaced placeholders (__INSTALL_USER__, __INSTALL_GROUP__, __INSTALL_PATH__)
  - Validates Description field
  - Checks if Python executable exists
  - Verifies working directory exists
  - Provides step-by-step fix instructions for corrupted service files

#### Enhanced Analysis
- **Better Error Detection**: Analyze command now:
  - Shows detailed service state information
  - Detects corrupted service files automatically
  - Displays more recent error logs (20 lines instead of 10)
  - Provides specific fix recommendations based on detected issues
  - Checks service file for unreplaced placeholders

#### Commands Updated
- `./service.sh health` - Improved service state detection
- `./service.sh analyze` - Enhanced error diagnostics
- `./service.sh verify` - NEW: Verify service file integrity

#### Usage Examples

**Check Service Status:**
```bash
./service.sh health
```

**Verify Service File:**
```bash
./service.sh verify
```

**If Service File is Corrupted:**
```bash
./service.sh uninstall
./setup.sh --service
```

#### Technical Changes
- service.sh: Enhanced cmd_health() with proper state detection
- service.sh: Enhanced cmd_analyze() with service file validation
- service.sh: Added cmd_verify() for service file integrity checking
- Removed use of `is-active --quiet` which caused false negatives
- Added explicit state checking with detailed output

#### Benefits
✅ **Accurate Health Checks**: No more false "service not running" errors  
✅ **Detect Corrupted Files**: Automatically find service file issues  
✅ **Easy Fixes**: Step-by-step instructions to repair problems  
✅ **Better Diagnostics**: Detailed state information for troubleshooting  
✅ **Proactive Checks**: Verify command prevents issues before they happen  

### Modified
- service.sh: Fixed health check logic and added verify command
- VERSION: Updated to 2.3.1
- CHANGELOG.md: Documented v2.3.1 fixes

---

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
