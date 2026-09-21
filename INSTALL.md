# CyberSec News Dashboard - Installation Guide

## Linux Apache Deployment Guide

This guide covers installing the Cybersecurity News Dashboard on a Linux server with Apache HTTP Server.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Setup (Development)](#quick-setup-development)
3. [Apache Production Deployment](#apache-production-deployment)
4. [Systemd Service Setup](#systemd-service-setup)
5. [SSL/HTTPS Configuration](#sslhttps-configuration)
6. [Firewall Configuration](#firewall-configuration)
7. [Maintenance & Monitoring](#maintenance--monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+, or RHEL 8+)
- Python 3.8 or later
- Apache 2.4 with mod_wsgi
- At least 512MB RAM
- At least 1GB disk space
- Internet access (for fetching RSS feeds)

### Install System Dependencies

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    apache2 libapache2-mod-wsgi-py3 \
    build-essential libxml2-dev libxslt1-dev \
    git curl
```

**CentOS / RHEL / Rocky Linux:**
```bash
sudo dnf install -y python3 python3-pip python3-devel \
    httpd mod_wsgi \
    gcc libxml2-devel libxslt-devel \
    git curl

# Enable Apache
sudo systemctl enable httpd
```

---

## Quick Setup (Development)

For quick testing on your local machine:

```bash
# 1. Clone or copy the project files
cd /opt
sudo mkdir -p cybersec-news
sudo chown $USER:$USER cybersec-news
cp -r /path/to/SecurityNewWeb/* /opt/cybersec-news/
cd /opt/cybersec-news

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Start the application
source venv/bin/activate
python app.py

# 4. Open in browser
# http://localhost:5000
```

The application will:
- Initialize the SQLite database with default sources and settings
- Start fetching RSS feeds from all enabled sources
- Run the priority scoring engine on fetched articles
- Display the dashboard on port 5000

---

## Apache Production Deployment

### Step 1: Create Application Directory

```bash
# Create the application directory
sudo mkdir -p /var/www/cybersec-news
sudo chown www-data:www-data /var/www/cybersec-news

# Copy application files
sudo cp -r /path/to/SecurityNewWeb/* /var/www/cybersec-news/
cd /var/www/cybersec-news

# Set ownership
sudo chown -R www-data:www-data /var/www/cybersec-news
```

### Step 2: Set Up Python Virtual Environment

```bash
cd /var/www/cybersec-news

# Create venv as the web user
sudo -u www-data python3 -m venv venv

# Install dependencies
sudo -u www-data venv/bin/pip install --upgrade pip
sudo -u www-data venv/bin/pip install -r requirements.txt

# Initialize the database
sudo -u www-data venv/bin/python -c "from database import init_db; init_db()"
```

### Step 3: Configure Apache Virtual Host

Create the Apache configuration file:

**Ubuntu / Debian:**
```bash
sudo nano /etc/apache2/sites-available/cybersec-news.conf
```

**CentOS / RHEL:**
```bash
sudo nano /etc/httpd/conf.d/cybersec-news.conf
```

Add the following configuration:

```apache
<VirtualHost *:80>
    # Server name - change to your domain or IP
    ServerName cybersec-news.example.com
    ServerAlias www.cybersec-news.example.com

    # Administrator email for error pages
    ServerAdmin admin@example.com

    # Document root (not directly served, but required)
    DocumentRoot /var/www/cybersec-news

    # ============================================================
    # WSGI Configuration
    # mod_wsgi runs the Flask application through the wsgi.py file
    # ============================================================

    # WSGI daemon process configuration:
    # - python-home: path to the virtual environment
    # - python-path: path to the application directory
    # - threads: number of threads per process
    # - processes: number of worker processes
    WSGIDaemonProcess cybersec-news \
        python-home=/var/www/cybersec-news/venv \
        python-path=/var/www/cybersec-news \
        threads=5 \
        processes=2

    # Map the root URL to the WSGI script
    WSGIScriptAlias / /var/www/cybersec-news/wsgi.py

    # Apply the daemon process to requests
    WSGIProcessGroup cybersec-news
    WSGIApplicationGroup %{GLOBAL}

    # ============================================================
    # Static Files
    # Serve CSS, JS, and images directly through Apache
    # (bypassing Flask for better performance)
    # ============================================================
    Alias /static /var/www/cybersec-news/static

    <Directory /var/www/cybersec-news/static>
        Require all granted
        # Cache static assets for 1 hour
        ExpiresActive On
        ExpiresDefault "access plus 1 hour"
    </Directory>

    # ============================================================
    # Application Directory Permissions
    # ============================================================
    <Directory /var/www/cybersec-news>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    # ============================================================
    # Logging
    # Separate access and error logs for this virtual host
    # ============================================================
    ErrorLog ${APACHE_LOG_DIR}/cybersec-news-error.log
    CustomLog ${APACHE_LOG_DIR}/cybersec-news-access.log combined

    # Log level (change to 'debug' for troubleshooting)
    LogLevel warn
</VirtualHost>
```

### Step 4: Enable the Site and Required Modules

**Ubuntu / Debian:**
```bash
# Enable required Apache modules
sudo a2enmod wsgi
sudo a2enmod expires
sudo a2enmod headers

# Enable the virtual host
sudo a2ensite cybersec-news.conf

# Disable the default site (optional)
# sudo a2dissite 000-default.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

**CentOS / RHEL:**
```bash
# mod_wsgi should already be loaded
# Test configuration
sudo httpd -t

# Restart Apache
sudo systemctl restart httpd
```

### Step 5: Set Proper File Permissions

```bash
# Ensure the web user can write to the database and logs
sudo chown -R www-data:www-data /var/www/cybersec-news
sudo chmod -R 755 /var/www/cybersec-news
sudo chmod 664 /var/www/cybersec-news/cybersec_news.db

# On CentOS/RHEL, the web user is 'apache' instead of 'www-data'
# sudo chown -R apache:apache /var/www/cybersec-news
```

### Step 6: Verify the Installation

```bash
# Check Apache status
sudo systemctl status apache2   # Ubuntu/Debian
sudo systemctl status httpd     # CentOS/RHEL

# Check the application logs
sudo tail -f /var/log/apache2/cybersec-news-error.log   # Ubuntu/Debian
sudo tail -f /var/log/httpd/cybersec-news-error.log     # CentOS/RHEL

# Test with curl
curl http://localhost/
```

Open your browser and navigate to `http://your-server-ip/` to see the dashboard.

---

## Systemd Service Setup

For the background scheduler (feed fetching, priority analysis) to work with Apache/mod_wsgi, you can also run a separate background worker:

```bash
sudo nano /etc/systemd/system/cybersec-news-worker.service
```

```ini
[Unit]
Description=CyberSec News Background Worker
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/cybersec-news
ExecStart=/var/www/cybersec-news/venv/bin/python -c "
from database import init_db
from feed_manager import fetch_all_feeds
from priority_engine import run_daily_priority_analysis
from auto_discovery import run_feed_discovery
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig(level=logging.INFO)
init_db()

scheduler = BlockingScheduler()
scheduler.add_job(fetch_all_feeds, 'interval', minutes=30, id='fetch')
scheduler.add_job(run_daily_priority_analysis, 'cron', hour=0, minute=0, id='analyze')
scheduler.add_job(run_feed_discovery, 'cron', hour=2, minute=0, id='discover')

logging.info('Background worker started')
scheduler.start()
"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable cybersec-news-worker
sudo systemctl start cybersec-news-worker
sudo systemctl status cybersec-news-worker
```

---

## SSL/HTTPS Configuration

For production, always use HTTPS:

### Option A: Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-apache   # Ubuntu/Debian
sudo dnf install -y certbot python3-certbot-apache    # CentOS/RHEL

# Obtain and install certificate
sudo certbot --apache -d cybersec-news.example.com

# Auto-renewal is set up automatically
# Test auto-renewal:
sudo certbot renew --dry-run
```

### Option B: Manual SSL Configuration

```apache
<VirtualHost *:443>
    ServerName cybersec-news.example.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/your-cert.pem
    SSLCertificateKeyFile /etc/ssl/private/your-key.pem
    SSLCertificateChainFile /etc/ssl/certs/your-chain.pem

    # ... same WSGI configuration as above ...

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName cybersec-news.example.com
    Redirect permanent / https://cybersec-news.example.com/
</VirtualHost>
```

---

## Firewall Configuration

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload

# firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## Maintenance & Monitoring

### View Application Logs

```bash
# Apache error log (application errors)
sudo tail -f /var/log/apache2/cybersec-news-error.log

# Apache access log (HTTP requests)
sudo tail -f /var/log/apache2/cybersec-news-access.log

# Background worker log
sudo journalctl -u cybersec-news-worker -f
```

### Database Maintenance

```bash
cd /var/www/cybersec-news
source venv/bin/activate

# Manual feed refresh
python -c "from feed_manager import fetch_all_feeds; print(fetch_all_feeds())"

# Manual priority analysis
python -c "from priority_engine import run_daily_priority_analysis; print(run_daily_priority_analysis())"

# Manual feed discovery
python -c "from auto_discovery import run_feed_discovery; print(run_feed_discovery())"

# Database backup
cp cybersec_news.db cybersec_news_backup_$(date +%Y%m%d).db
```

### Update the Application

```bash
cd /var/www/cybersec-news

# Backup database
cp cybersec_news.db cybersec_news.db.bak

# Copy new files
sudo cp -r /path/to/new-files/* .

# Update dependencies
sudo -u www-data venv/bin/pip install -r requirements.txt

# Restart services
sudo systemctl restart apache2
sudo systemctl restart cybersec-news-worker
```

---

## Troubleshooting

### Common Issues

**1. "Internal Server Error" (500)**
```bash
# Check Apache error log
sudo tail -50 /var/log/apache2/cybersec-news-error.log

# Common causes:
# - Python module not installed: pip install -r requirements.txt
# - File permission issue: chown -R www-data:www-data /var/www/cybersec-news
# - Database not initialized: python -c "from database import init_db; init_db()"
```

**2. "Forbidden" (403)**
```bash
# Check directory permissions
ls -la /var/www/cybersec-news/
ls -la /var/www/cybersec-news/wsgi.py

# Fix permissions
sudo chown -R www-data:www-data /var/www/cybersec-news
sudo chmod 755 /var/www/cybersec-news
sudo chmod 644 /var/www/cybersec-news/wsgi.py
```

**3. Static files not loading (CSS/JS missing)**
```bash
# Verify the Alias directive in Apache config
# Ensure /var/www/cybersec-news/static/ exists and has correct permissions
ls -la /var/www/cybersec-news/static/
sudo chmod -R 755 /var/www/cybersec-news/static/
```

**4. Database locked errors**
```bash
# SQLite can lock under concurrent writes
# The application uses WAL mode to minimize this
# If persistent, check for stuck processes:
sudo fuser /var/www/cybersec-news/cybersec_news.db
```

**5. Feed fetching not working**
```bash
# Test network connectivity
curl -I https://feeds.feedburner.com/TheHackersNews

# Check if the background worker is running
sudo systemctl status cybersec-news-worker

# Manual test
cd /var/www/cybersec-news
source venv/bin/activate
python -c "from feed_manager import fetch_all_feeds; print(fetch_all_feeds())"
```

**6. SELinux issues (CentOS/RHEL)**
```bash
# If SELinux is blocking Apache:
sudo setsebool -P httpd_can_network_connect 1
sudo chcon -R -t httpd_sys_content_t /var/www/cybersec-news/
sudo chcon -R -t httpd_sys_rw_content_t /var/www/cybersec-news/cybersec_news.db
```

---

## Application Architecture

```
cybersec-news/
├── app.py                 # Main Flask application with routes and scheduler
├── config.py              # Configuration: default feeds, regions, priorities
├── database.py            # SQLite database schema and CRUD operations
├── feed_manager.py        # RSS feed fetching, parsing, and classification
├── priority_engine.py     # Automated priority analysis engine (runs at midnight)
├── auto_discovery.py      # Automatic feed discovery module
├── wsgi.py                # WSGI entry point for Apache mod_wsgi
├── setup.sh               # Quick setup script
├── requirements.txt       # Python package dependencies
├── INSTALL.md             # This installation guide
├── cybersec_news.db       # SQLite database (created at runtime)
├── static/
│   ├── css/
│   │   └── style.css      # Dashboard stylesheet (dark theme)
│   └── js/
│       └── app.js         # Client-side JavaScript (nav, auto-refresh, shortcuts)
└── templates/
    ├── base.html           # Base layout template (navbar, footer)
    ├── dashboard.html      # Main dashboard with top 10 news and stats
    ├── news.html           # Full news list with all filters
    ├── cve.html            # CVE-focused monitoring view
    ├── sources.html        # Feed source management (add/edit/delete/discover)
    ├── priorities.html     # Priority rules management and analysis logs
    └── settings.html       # Application settings configuration
```

---

## Default Feed Sources

The application comes pre-configured with 60+ cybersecurity feed sources:

| Category | Sources |
|----------|---------|
| Web News | The Hacker News, BleepingComputer, SecurityWeek, Dark Reading, etc. |
| Blogs | Krebs on Security, Schneier, Troy Hunt, Graham Cluley, Medium |
| Vendor Research | Unit42, Cisco Talos, Microsoft, Google Project Zero, CrowdStrike, etc. |
| CVE / Advisories | NVD, CISA, Cisco, Palo Alto, Fortinet, Check Point, Juniper |
| Dark Web Intel | DarkOwl, Flashpoint, Recorded Future, Intel471 |
| Chinese Vendors | Qihoo 360, NSFOCUS, Antiy, Knownsec/Seebug, QiAnXin |
| Community | Reddit r/netsec, Reddit r/cybersecurity |
| Government CERTs | US-CERT, JPCERT/CC, CERT-EU, CNVD, AusCERT, CERT-In |
