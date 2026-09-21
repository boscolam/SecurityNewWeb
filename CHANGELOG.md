# Changelog

All notable changes to the Cybersecurity News Dashboard will be documented in this file.

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
