# Ubuntu Installation Guide - Cybersecurity News Dashboard

Quick and easy installation guide for Ubuntu 20.04/22.04/24.04

---

## 🚀 Quick Installation (5 minutes)

### Step 1: Update System & Install Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y python3 python3-pip python3-venv git
```

### Step 2: Clone the Repository

```bash
# Navigate to your home directory (or wherever you want to install)
cd ~

# Clone from GitHub
git clone https://github.com/boscolam/SecurityNewWeb.git

# Enter the directory
cd SecurityNewWeb
```

### Step 3: Run Setup Script

```bash
# Make setup script executable
chmod +x setup.sh

# Run the setup (creates venv and installs dependencies)
./setup.sh
```

### Step 4: Start the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the Flask application
python app.py
```

### Step 5: Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

Or if accessing from another computer:
```
http://YOUR_SERVER_IP:5000
```

---

## 🎯 That's It! You're Done!

The application will:
- ✅ Initialize the database with 140+ RSS feeds
- ✅ Start fetching cybersecurity news automatically
- ✅ Run background tasks for feed updates
- ✅ Display the dashboard on port 5000

### ✅ Verify Installation

```bash
# Check version
cat VERSION
# Should show: 2.2.1

# Check git version
git log --oneline -1
# Should show: a444813 or later

# Check service (if installed)
./service.sh status

# Access dashboard
curl http://localhost:5000
```

---

## 🔄 Run as Systemd Service (Recommended)

Instead of running manually, install as a background service that starts automatically on boot.

### Quick Service Installation

```bash
cd ~/SecurityNewWeb

# Install as user service (runs under your account)
./setup.sh --service

# OR install as system service (runs on boot, requires sudo)
sudo ./setup.sh --system-service
```

### Manual Service Installation

#### **Option A: User Service** (Recommended for home directory)

```bash
# 1. Create systemd user directory
mkdir -p ~/.config/systemd/user/

# 2. Copy service file
cp cybersec-news-user.service ~/.config/systemd/user/cybersec-news.service

# 3. Update paths in service file (if not in ~/SecurityNewWeb)
nano ~/.config/systemd/user/cybersec-news.service
# Edit WorkingDirectory and ExecStart paths

# 4. Reload systemd
systemctl --user daemon-reload

# 5. Enable service (start on login)
systemctl --user enable cybersec-news

# 6. Start service now
systemctl --user start cybersec-news

# 7. Enable linger (optional - runs even when not logged in)
sudo loginctl enable-linger $USER

# 8. Check status
systemctl --user status cybersec-news
```

#### **Option B: System Service** (For /var/www installations)

```bash
# 1. Copy service file
sudo cp cybersec-news.service /etc/systemd/system/

# 2. Edit service file with correct paths
sudo nano /etc/systemd/system/cybersec-news.service
# Update WorkingDirectory and ExecStart paths
# Update User if not using www-data

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable service (start on boot)
sudo systemctl enable cybersec-news

# 5. Start service now
sudo systemctl start cybersec-news

# 6. Check status
sudo systemctl status cybersec-news
```

### Service Management Commands

**User Service:**
```bash
# Start/Stop/Restart
systemctl --user start cybersec-news
systemctl --user stop cybersec-news
systemctl --user restart cybersec-news

# View status
systemctl --user status cybersec-news

# View logs (live)
journalctl --user -u cybersec-news -f

# View recent logs
journalctl --user -u cybersec-news -n 100

# Disable service
systemctl --user disable cybersec-news
```

**System Service:**
```bash
# Start/Stop/Restart
sudo systemctl start cybersec-news
sudo systemctl stop cybersec-news
sudo systemctl restart cybersec-news

# View status
sudo systemctl status cybersec-news

# View logs (live)
sudo journalctl -u cybersec-news -f

# View recent logs
sudo journalctl -u cybersec-news -n 100

# Disable service
sudo systemctl disable cybersec-news
```

### Auto-Restart After Updates

When running as a service, you can configure automatic restart after updates:

1. Go to: `http://localhost:5000/updates`
2. Enable "Restart After Update"
3. Save settings

The service will automatically restart when updates are installed via the auto-update feature.

---

## 🔧 Manual Installation (If setup.sh doesn't work)

If the automated setup script has issues, follow these manual steps:

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    build-essential libxml2-dev libxslt1-dev git
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/boscolam/SecurityNewWeb.git
cd SecurityNewWeb
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
# Start Python and run init
python3 << EOF
from database import init_db
init_db()
print("Database initialized successfully!")
EOF
```

### 6. Run Application

```bash
python app.py
```

---

## 🌐 Production Deployment (Apache)

For production deployment with Apache web server:

### 1. Install Apache and mod_wsgi

```bash
sudo apt update
sudo apt install -y apache2 libapache2-mod-wsgi-py3
```

### 2. Create Application Directory

```bash
# Create directory
sudo mkdir -p /var/www/cybersec-news

# Copy files
sudo cp -r ~/SecurityNewWeb/* /var/www/cybersec-news/

# Set ownership
sudo chown -R www-data:www-data /var/www/cybersec-news
```

### 3. Setup Virtual Environment

```bash
cd /var/www/cybersec-news

# Create venv as www-data user
sudo -u www-data python3 -m venv venv

# Install dependencies
sudo -u www-data venv/bin/pip install --upgrade pip
sudo -u www-data venv/bin/pip install -r requirements.txt

# Initialize database
sudo -u www-data venv/bin/python3 -c "from database import init_db; init_db()"
```

### 4. Configure Apache

Create Apache configuration:

```bash
sudo nano /etc/apache2/sites-available/cybersec-news.conf
```

Add this configuration:

```apache
<VirtualHost *:80>
    ServerName your-server-ip-or-domain.com
    ServerAdmin admin@example.com

    DocumentRoot /var/www/cybersec-news

    # WSGI Configuration
    WSGIDaemonProcess cybersec_news python-home=/var/www/cybersec-news/venv python-path=/var/www/cybersec-news
    WSGIProcessGroup cybersec_news
    WSGIScriptAlias / /var/www/cybersec-news/wsgi.py

    # Static files
    Alias /static /var/www/cybersec-news/static
    <Directory /var/www/cybersec-news/static>
        Require all granted
    </Directory>

    # Application directory
    <Directory /var/www/cybersec-news>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    # Logging
    ErrorLog ${APACHE_LOG_DIR}/cybersec-news-error.log
    CustomLog ${APACHE_LOG_DIR}/cybersec-news-access.log combined
</VirtualHost>
```

### 5. Enable Site and Restart Apache

```bash
# Enable the site
sudo a2ensite cybersec-news.conf

# Disable default site (optional)
sudo a2dissite 000-default.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

### 6. Configure Firewall

```bash
# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# Enable firewall if not already enabled
sudo ufw enable
```

### 7. Access Your Application

Open browser to:
```
http://your-server-ip
```

---

## 🔐 Security Hardening

### 1. Change Secret Key

Edit `app.py` and change the secret key:

```bash
nano /var/www/cybersec-news/app.py
```

Find this line:
```python
app.config['SECRET_KEY'] = 'cybersec-news-dashboard-secret-change-in-production'
```

Change to a random string:
```python
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

Or generate one manually:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Set File Permissions

```bash
cd /var/www/cybersec-news

# Set directory permissions
sudo find . -type d -exec chmod 755 {} \;

# Set file permissions
sudo find . -type f -exec chmod 644 {} \;

# Make scripts executable
sudo chmod +x setup.sh

# Protect database
sudo chmod 600 cybersec_news.db 2>/dev/null || true
```

### 3. Setup HTTPS with Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-apache

# Get SSL certificate (replace with your domain)
sudo certbot --apache -d your-domain.com

# Certbot will automatically configure Apache for HTTPS
```

---

## 🔄 Running as a Service (Systemd)

For development mode with systemd:

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/cybersec-news.service
```

Add this content:

```ini
[Unit]
Description=Cybersecurity News Dashboard
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/cybersec-news
Environment="PATH=/var/www/cybersec-news/venv/bin"
ExecStart=/var/www/cybersec-news/venv/bin/python app.py

Restart=always
RestartSec=10

StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=cybersec-news

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable cybersec-news

# Start the service
sudo systemctl start cybersec-news

# Check status
sudo systemctl status cybersec-news
```

### 3. Manage Service

```bash
# Start
sudo systemctl start cybersec-news

# Stop
sudo systemctl stop cybersec-news

# Restart
sudo systemctl restart cybersec-news

# View logs
sudo journalctl -u cybersec-news -f
```

---

## 📊 Verify Installation

### Check if Application is Running

```bash
# Check if port 5000 is listening (development)
sudo netstat -tulpn | grep 5000

# Or for Apache (port 80)
sudo netstat -tulpn | grep :80

# Check with curl
curl http://localhost:5000
# or
curl http://localhost
```

### Check Database

```bash
cd ~/SecurityNewWeb  # or /var/www/cybersec-news
source venv/bin/activate

python3 << EOF
from database import get_sources, get_news_stats
sources = get_sources()
stats = get_news_stats()
print(f"Sources configured: {len(sources)}")
print(f"News stats: {stats}")
EOF
```

### Check Logs

```bash
# Application logs (if running directly)
tail -f ~/SecurityNewWeb/logs/*.log

# Apache logs
sudo tail -f /var/log/apache2/cybersec-news-error.log
sudo tail -f /var/log/apache2/cybersec-news-access.log

# Systemd logs
sudo journalctl -u cybersec-news -f
```

---

## 🛠️ Troubleshooting

### Port 5000 Already in Use

```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
python app.py --port 5001
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/cybersec-news

# Fix permissions
sudo chmod -R 755 /var/www/cybersec-news
```

### Python Module Not Found

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Apache Not Starting

```bash
# Check configuration
sudo apache2ctl configtest

# Check Apache status
sudo systemctl status apache2

# View error logs
sudo tail -50 /var/log/apache2/error.log
```

### Database Errors

```bash
# Remove and reinitialize database
rm cybersec_news.db*

# Reinitialize
python3 -c "from database import init_db; init_db()"
```

---

## 🔄 Updating the Application

```bash
# Navigate to directory
cd ~/SecurityNewWeb  # or /var/www/cybersec-news

# Pull latest changes
git pull origin main

# Activate venv
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
# For direct run:
# (Stop with Ctrl+C and restart)

# For systemd:
sudo systemctl restart cybersec-news

# For Apache:
sudo systemctl restart apache2
```

---

## 📝 Configuration

### Change Refresh Interval

Access the web UI at:
```
http://localhost:5000/settings
```

Or modify in database:
```bash
sqlite3 cybersec_news.db "UPDATE settings SET value='60' WHERE key='refresh_interval';"
```

### Add Custom RSS Feeds

Access:
```
http://localhost:5000/sources
```

### Configure Priority Rules

Access:
```
http://localhost:5000/priorities
```

---

## 🎉 Success!

Your Cybersecurity News Dashboard is now running on Ubuntu!

**Access Points**:
- Development: `http://localhost:5000`
- Production: `http://your-server-ip` or `https://your-domain.com`

**Key Features**:
- 📰 90+ RSS feeds automatically fetching news
- 🎯 Priority scoring and filtering
- 🔍 CVE tracking and vendor monitoring
- 🌍 Region-based filtering (Global, NA, EU, APAC, China, etc.)
- 🤖 Automatic feed discovery
- 📊 Analytics and reporting

**Need Help?**
- Check [INSTALL.md](INSTALL.md) for detailed Apache configuration
- View [README.md](README.md) for features and API documentation
- Review [CODE_ANALYSIS.md](CODE_ANALYSIS.md) for architecture details
- Open an issue: https://github.com/boscolam/SecurityNewWeb/issues

---

**Enjoy your cybersecurity news aggregator!** 🚀🔐
