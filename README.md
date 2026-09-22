# Cybersecurity News Dashboard

A comprehensive Flask-based web application that aggregates cybersecurity news from multiple sources including RSS feeds, vendor security blogs, dark web intelligence, CVE databases, and social media platforms.

![Version](https://img.shields.io/badge/version-2.5.2-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![RSS Feeds](https://img.shields.io/badge/RSS%20Feeds-140+-success.svg)

## Features

### Core Functionality
- **Multi-Source Aggregation**: Fetches news from **140+ predefined sources** across:
  - Major cybersecurity news sites (The Hacker News, BleepingComputer, SecurityWeek)
  - Vendor research teams (Palo Alto Unit42, Cisco Talos, Microsoft Security, Google Project Zero)
  - Dark web threat intelligence (DarkOwl, Flashpoint, Recorded Future)
  - CVE databases (NVD, CISA, US-CERT, Exploit-DB)
  - **52 Government CERTs** (CISA, UK NCSC, CERT-EU, JPCERT, AusCERT, and more - via [Pulsedive certrss](https://github.com/pulsedive/certrss))
  - Chinese cybersecurity vendors (Qihoo 360, NSFOCUS, Antiy Labs)
  - Social media platforms (Reddit r/netsec, Medium cybersecurity)

- **Priority-Based Scoring**: Intelligent prioritization system with:
  - Configurable priority rules based on keywords, categories, and sources
  - Automatic scoring (0-100) with labels: critical, high, medium, low
  - Hacking incident detection
  - CVE identification and vendor tracking
  - Daily priority rule analysis for effectiveness

- **Smart Filtering**:
  - Region-based filtering (Global, North America, Europe, Asia Pacific, China, Middle East, Latin America)
  - Category filtering (Web News, Blog, Vendor Research, Dark Web, CVE, Government)
  - Feed type classification (RSS, Web Scrape, API, Social Media)

- **Automatic Feed Discovery**: 
  - Daily automatic discovery of new RSS feeds from existing sources
  - Manual approval workflow for discovered feeds
  - Prevents duplicate feeds

- **Real-Time Cyber Attack Map** 🆕:
  - Animated world map showing cyber attacks from source to destination countries
  - Attack data derived from actual news (hacking incidents, CVEs, threat intelligence)
  - Keyword-based detection of threat actors (APT groups, nation-state attackers)
  - 35 country coordinates with 85+ city dots forming visual world map
  - Live attack feed, threat overview stats, and top attacker rankings
  - Severity-coded arcs: Critical (red), High (orange), Medium (yellow), Low (green)

- **Clickable Badges & Filtering**:
  - All badges/tags across Dashboard, News, and CVE pages are clickable
  - One-click filtering by priority, category, region, source, vendor
  - Hover animations with glow effects

- **Comprehensive Logging System**:
  - 5 separate log files (app, error, access, update, feed)
  - Web-based log viewer with search, auto-refresh, and download
  - RotatingFileHandler: 10MB max, 5 backups per log

### Technical Features
- **Background Task Scheduling**: APScheduler for automated operations:
  - Configurable feed refresh intervals (default: 30 minutes)
  - Daily priority analysis at midnight
  - Daily feed auto-discovery at 2 AM
  - Weekly cleanup of old news (90-day retention)

- **Auto-Update System** 🆕:
  - Automatic updates from GitHub repository
  - Configurable schedules (hourly, daily, weekly)
  - Automatic database backup before updates
  - Web-based configuration interface
  - Update history tracking

- **Database**: SQLite with Write-Ahead Logging (WAL) for concurrent access
- **Web Interface**: Responsive HTML/CSS/JavaScript dashboard
- **Production Ready**: Apache mod_wsgi deployment support

## Project Structure

```
SecurityNewWeb/
├── app.py                  # Main Flask application with routes
├── config.py               # Configuration and default feed sources
├── database.py             # Database operations and schema
├── feed_manager.py         # RSS/feed fetching and parsing
├── priority_engine.py      # Priority scoring and analysis
├── auto_discovery.py       # Automatic feed discovery
├── git_updater.py          # Git auto-update system
├── logger_config.py        # Logging configuration (5 log files)
├── requirements.txt        # Python dependencies
├── setup.sh               # Quick setup script
├── service.sh             # Systemd service management
├── wsgi.py                # WSGI entry point for Apache
├── INSTALL.md             # Detailed installation guide
├── static/
│   ├── css/style.css      # Dashboard styling
│   └── js/app.js          # Frontend JavaScript
└── templates/
    ├── base.html          # Base template with navigation
    ├── dashboard.html     # Main dashboard
    ├── news.html          # News listing with filters
    ├── cve.html           # CVE-specific view
    ├── attack_map.html    # Real-time cyber attack map
    ├── sources.html       # Feed source management (Settings tab)
    ├── priorities.html    # Priority rules management
    ├── settings.html      # Application settings (Settings tab)
    ├── updates.html       # System updates (Settings tab)
    └── logs.html          # System logs viewer (Settings tab)
```

## Installation

### Quick Start (Recommended - Run as Service)

```bash
# Clone the repository
git clone https://github.com/boscolam/SecurityNewWeb.git
cd SecurityNewWeb

# Install as systemd service (runs automatically on boot)
./setup.sh --service

# Access dashboard
# http://localhost:5000
```

**Service management:**
```bash
./service.sh status    # Check status
./service.sh restart   # Restart service
./service.sh logs      # View logs
```

### Alternative: Manual Run

```bash
# Clone and setup
git clone https://github.com/boscolam/SecurityNewWeb.git
cd SecurityNewWeb
./setup.sh

# Run manually
source venv/bin/activate
python app.py

# Access at http://localhost:5000
```

### Production Deployment (System Service)

```bash
# Full production setup with Apache
sudo ./setup.sh --production

# OR system service only
sudo ./setup.sh --system-service
```

### Production Deployment (Apache)

For Apache with mod_wsgi deployment, see [INSTALL.md](INSTALL.md) for detailed instructions.

## Configuration

### Application Settings
Access via web interface at `/settings` or modify directly in the database:

- **Refresh Interval**: How often to fetch feeds (default: 30 minutes)
- **Max News Items**: Maximum number of articles to store (default: 10,000)
- **Retention Days**: Days to keep old news (default: 90)

### Priority Rules
Customize at `/priorities` to define scoring rules based on:
- Keywords in title/content
- News category
- Source name
- Region

### Feed Sources
Manage at `/sources`:
- Add/edit/delete RSS feeds
- Enable/disable specific sources
- View fetch status and errors
- Approve auto-discovered feeds

## API Endpoints

### News
- `GET /` - Main dashboard
- `GET /news` - News listing with filters
- `GET /api/news` - JSON API for news articles
- `GET /api/top-news` - Top priority news items

### Sources
- `GET /sources` - Source management page
- `GET /api/sources` - List all sources
- `POST /api/sources` - Add new source
- `PUT /api/sources/<id>` - Update source
- `DELETE /api/sources/<id>` - Delete source

### Priority Rules
- `GET /priorities` - Priority rules management
- `GET /api/priority-rules` - List all rules
- `POST /api/priority-rules` - Add new rule
- `PUT /api/priority-rules/<id>` - Update rule
- `DELETE /api/priority-rules/<id>` - Delete rule

### CVE Tracking
- `GET /cve` - CVE-specific dashboard
- `GET /api/cve-news` - CVE news with vendor filtering

### Feed Discovery
- `GET /api/discovered-feeds` - View discovered feeds
- `POST /api/discovered-feeds/<id>/approve` - Approve feed
- `POST /api/discovered-feeds/<id>/reject` - Reject feed

### Attack Map
- `GET /attack-map` - Real-time cyber attack map visualization
- `GET /api/attack-data` - Attack events derived from news data (JSON)

### System
- `GET /settings` - Application settings (tabbed: Settings, Sources, Updates, Logs)
- `GET /updates` - System updates page
- `GET /logs` - System logs viewer
- `GET /api/logs/list` - List all log files
- `GET /api/logs/<name>` - Get log file content
- `GET /api/logs/<name>/download` - Download a log file
- `POST /api/logs/<name>/clear` - Clear a log file

### Analytics
- `GET /api/stats` - News statistics
- `GET /api/analysis-logs` - Priority analysis logs

## Database Schema

### Tables
- **news**: News articles with priority scores, CVE info, and metadata
- **sources**: Feed sources with configuration and status
- **settings**: Application settings (key-value pairs)
- **priority_rules**: Priority scoring rules with hit counters
- **discovered_feeds**: Auto-discovered feeds pending approval
- **priority_analysis_log**: Daily analysis results

## Security Considerations

### Default Secret Key
⚠️ **Important**: Change the default Flask secret key in production:

```python
# In app.py
app.config['SECRET_KEY'] = 'your-secure-random-key-here'
```

### Input Validation
- All user inputs are validated and sanitized
- HTML content is cleaned with bleach library
- SQL injection protection via parameterized queries
- XSS prevention with proper escaping

### Network Security
- Request timeouts prevent hanging connections
- User-Agent headers for respectful crawling
- Error handling for malformed feeds

## Dependencies

Core Python packages:
- **Flask 3.0.0**: Web framework
- **feedparser 6.0.11**: RSS/Atom feed parsing
- **beautifulsoup4 4.12.2**: HTML parsing
- **requests 2.31.0**: HTTP library
- **APScheduler 3.10.4**: Background task scheduling
- **lxml 4.9.3**: XML/HTML processing
- **python-dateutil 2.8.2**: Date parsing
- **bleach 6.1.0**: HTML sanitization

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Government CERT Feeds 🏛️

**New in v2.0.0!** Integrated 52 official government Computer Emergency Response Team (CERT) RSS feeds from around the world.

### Coverage by Region

**North America** (4 feeds)
- CISA (United States) - News & Advisories
- Canadian Centre for Cyber Security - News & Alerts

**Europe** (32 feeds)
- CERT-EU, UK NCSC, Finland NCSC, France CERT-FR
- Austria CERT.at, Belgium CERT.BE, Netherlands NCSC
- Switzerland GovCERT, Poland CERT.PL, Croatia CERT.hr
- Czech NUKIB, Denmark DKCERT, Estonia CERT-EE
- Italy CSIRT, Latvia CERT.LV, Norway NSM NCSC
- Romania CERT.RO, Slovenia SI-CERT, Spain CCN-CERT & INCIBE
- Sweden CERT-SE, Ukraine CERT-UA, Hungary NCSC, Portugal CNCS

**Asia Pacific** (6 feeds)
- Australia AusCERT, Japan JPCERT/CC
- Singapore SingCERT, Hong Kong GovCERT & HKCERT
- Bangladesh BGD e-GOV CIRT

**South America** (1 feed)
- Brazil CERT.br

**Africa** (2 feeds)
- Egypt EG-CERT, Libya NISSA

### Why Government CERTs Matter

✅ **Authoritative Sources**: Direct from official government cybersecurity agencies  
✅ **Early Warnings**: Often first to report critical vulnerabilities affecting their regions  
✅ **Compliance**: Essential for organizations with regulatory requirements  
✅ **Threat Intelligence**: Nation-state threats and critical infrastructure alerts  
✅ **Regional Context**: Local threat landscape and region-specific advisories

### Source Attribution

Government CERT feeds curated from [Pulsedive certrss](https://github.com/pulsedive/certrss) - a community-maintained registry of government CERT RSS feeds.

Credits to:
- [Pulsedive](https://pulsedive.com) for the original compilation
- [Curated Intelligence](https://github.com/curated-intel/) community
- [CyberSquarePeg](https://twitter.com/CyberSquarePeg) for contributions
- [DCOD](https://dcod.ch/) for the 2026-08-16 registry refresh

## Acknowledgments

- Thanks to all the cybersecurity news sources and vendors providing RSS feeds
- Special thanks to government CERTs worldwide for providing public RSS feeds
- Inspired by the need for centralized threat intelligence aggregation
- Built for security professionals, researchers, and enthusiasts

## Support & Troubleshooting

**Quick Fixes**: See [QUICKFIX.md](QUICKFIX.md) for one-line solutions to common issues

**Documentation**:
- [UBUNTU_INSTALL.md](UBUNTU_INSTALL.md) - Ubuntu installation guide
- [UPDATE_INSTRUCTIONS.md](UPDATE_INSTRUCTIONS.md) - Update guide (v1.0 → v2.2.0)
- [AUTO_UPDATE_GUIDE.md](AUTO_UPDATE_GUIDE.md) - Auto-update documentation
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - Logging system guide
- [UI_ENHANCEMENTS.md](UI_ENHANCEMENTS.md) - Clickable badges & attack map
- [INSTALL.md](INSTALL.md) - Detailed Apache deployment

**Common Issues**:
- Git merge conflict: `git stash && git pull origin main && chmod +x *.sh`
- Permission denied: `chmod +x setup.sh service.sh`
- Service won't start: `./service.sh status` and `./service.sh logs-tail`

**Get Help**:
- Open an issue on [GitHub](https://github.com/boscolam/SecurityNewWeb/issues)
- Check logs: `./service.sh logs` or `journalctl --user -u cybersec-news -f`

## Roadmap

Completed:
- [x] Real-time cyber attack map visualization
- [x] Clickable badges for instant filtering
- [x] Comprehensive logging system with web viewer
- [x] Auto-update system with service restart
- [x] Settings consolidation with tabbed navigation

Future enhancements:
- [ ] Email/Slack notifications for high-priority news
- [ ] Advanced NLP for better article classification
- [ ] Machine learning for priority prediction
- [ ] REST API with authentication
- [ ] Docker containerization
- [ ] Integration with SIEM platforms
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Threat actor tracking

---

**Made with ❤️ for the cybersecurity community**
