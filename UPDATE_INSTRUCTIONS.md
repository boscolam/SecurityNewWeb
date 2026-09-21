# Update Instructions - v1.0 → v2.2.0

Complete guide to update your existing Cybersecurity News Dashboard to the latest version with government CERT feeds, auto-update features, and systemd service support.

---

## ⚡ Quick Fix Available!

**Having update issues?** See **[QUICKFIX.md](QUICKFIX.md)** for one-line solutions to common problems.

**Most Common Issue**: `git stash && git pull origin main && chmod +x *.sh && ./service.sh restart`

---

## 📊 What's New

**v2.2.0** (Systemd Service Support):
- ✅ Run as systemd background service
- ✅ Auto-start on boot
- ✅ Service management tools (service.sh)
- ✅ Enhanced setup script with --service flags
- ✅ Production-ready deployment

**v2.1.0** (Auto-Update System):
- ✅ Auto-update from GitHub with web interface
- ✅ Configurable update schedules
- ✅ Automatic database backups
- ✅ Update history tracking

**v2.0.0** (Government CERT Feeds):
- ✅ 52 new government CERT RSS feeds
- ✅ Global coverage (30+ countries)
- ✅ Official security advisories

**Total new feeds**: 140+ (up from 90+)
**Service support**: User and system services

---

## ⚠️ Before You Start

### 1. **Check Your Current Installation**

```bash
# Navigate to your installation directory
cd ~/SecurityNewWeb
# OR if installed in /var/www
cd /var/www/cybersec-news

# Check if it's a git repository
git status
```

**If you see**: "fatal: not a git repository"
- **Solution**: See [Method 2: Manual Update](#method-2-manual-update-non-git-installation) below

**If you see**: Git status output
- **Solution**: Continue with [Method 1: Git Pull Update](#method-1-git-pull-update-recommended)

### 2. **Backup Your Database** ⚠️ IMPORTANT

```bash
# Backup database (REQUIRED before updating)
cp cybersec_news.db cybersec_news.db.backup_$(date +%Y%m%d_%H%M%S)

# Verify backup was created
ls -lh cybersec_news.db*
```

### 3. **Check Running Process**

```bash
# Check if application is running
ps aux | grep app.py

# Or check systemd service
sudo systemctl status cybersec-news

# Or check Apache
sudo systemctl status apache2
```

---

## 🚀 Method 1: Git Pull Update (Recommended)

**Use this if your installation is a git repository**

### Step 1: Stop the Application

**If running directly:**
```bash
# Press Ctrl+C in the terminal where app.py is running
```

**If using systemd:**
```bash
sudo systemctl stop cybersec-news
```

**If using Apache:**
```bash
# No need to stop Apache, it will reload automatically
```

### Step 2: Backup Database

```bash
cd ~/SecurityNewWeb  # Or your installation path

# Create backup
cp cybersec_news.db cybersec_news.db.backup

# Verify
ls -lh cybersec_news.db*
```

### Step 3: Pull Latest Changes

```bash
# Fetch latest changes
git fetch origin

# Check what will be updated
git log HEAD..origin/main --oneline

# Pull the updates
git pull origin main
```

**Expected output:**
```
Updating 540a331..7d86097
Fast-forward
 AUTO_UPDATE_GUIDE.md      | 573 ++++++++++++++++++++++
 CHANGELOG.md              | 209 ++++++++
 README.md                 |  53 +-
 app.py                    | 105 ++++
 config.py                 |  63 ++-
 database.py               |  15 +
 git_updater.py            | 389 ++++++++++++++
 templates/base.html       |   5 +
 templates/updates.html    | 437 ++++++++++++++++
 9 files changed, 1831 insertions(+), 8 deletions(-)
```

### Step 4: Update Dependencies (if needed)

```bash
# Activate virtual environment
source venv/bin/activate

# Check if new dependencies added
pip install -r requirements.txt --upgrade
```

### Step 5: Verify Database

```bash
# Check database structure (optional)
sqlite3 cybersec_news.db "SELECT COUNT(*) FROM sources;"

# Should show around 90-105 sources (old installation)
```

### Step 6: Restart Application

**If running directly:**
```bash
source venv/bin/activate
python app.py
```

**If using systemd:**
```bash
sudo systemctl start cybersec-news
sudo systemctl status cybersec-news
```

**If using Apache:**
```bash
sudo systemctl restart apache2
sudo systemctl status apache2
```

### Step 7: Verify Update

Open your browser:
```
http://localhost:5000
```

Check:
1. ✅ New "Updates" link in navigation
2. ✅ Visit `/sources` - should see ~140 sources (52 new government CERTs)
3. ✅ Visit `/updates` - should see update configuration page

### Step 8: Test Auto-Update Feature

1. Go to: `http://localhost:5000/updates`
2. Click **"Check Now"**
3. Should show: "Already up to date" ✅

**Done!** Your installation is now at v2.1.0 🎉

---

## 📦 Method 2: Manual Update (Non-Git Installation)

**Use this if you downloaded as ZIP or not using git**

### Step 1: Backup Everything

```bash
cd ~  # Or wherever your installation is

# Backup entire directory
cp -r SecurityNewWeb SecurityNewWeb.backup_$(date +%Y%m%d)

# Verify backup
ls -lh SecurityNewWeb*
```

### Step 2: Download Latest Version

**Option A: Convert to Git Repository (Recommended)**

```bash
cd ~/SecurityNewWeb

# Initialize git repository
git init
git remote add origin https://github.com/boscolam/SecurityNewWeb.git
git fetch origin
git reset --hard origin/main

# Your existing database is preserved
ls -lh cybersec_news.db
```

**Option B: Manual File Download**

```bash
cd ~/SecurityNewWeb

# Download new files
wget https://raw.githubusercontent.com/boscolam/SecurityNewWeb/main/git_updater.py
wget https://raw.githubusercontent.com/boscolam/SecurityNewWeb/main/AUTO_UPDATE_GUIDE.md

# Download updated templates
cd templates
wget https://raw.githubusercontent.com/boscolam/SecurityNewWeb/main/templates/updates.html
wget https://raw.githubusercontent.com/boscolam/SecurityNewWeb/main/templates/base.html -O base.html.new

# Compare and merge manually
cd ..
```

**Option C: Fresh Install (Preserve Database)**

```bash
# 1. Save your database
cp ~/SecurityNewWeb/cybersec_news.db ~/cybersec_news.db.save

# 2. Remove old installation
rm -rf ~/SecurityNewWeb

# 3. Clone fresh copy
git clone https://github.com/boscolam/SecurityNewWeb.git
cd SecurityNewWeb

# 4. Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Restore your database
cp ~/cybersec_news.db.save cybersec_news.db

# 6. Start application
python app.py
```

### Step 3: Restart and Verify

```bash
# Restart application
source venv/bin/activate
python app.py

# Check browser
# http://localhost:5000
```

---

## 🔧 Method 3: Update in Production (Apache)

**For production servers running with Apache**

### Step 1: Backup

```bash
# Backup database
sudo cp /var/www/cybersec-news/cybersec_news.db /var/www/cybersec_news.db.backup

# Backup config (if customized)
sudo cp /var/www/cybersec-news/config.py /var/www/config.py.backup
```

### Step 2: Pull Updates

```bash
cd /var/www/cybersec-news

# Pull as www-data user (or your Apache user)
sudo -u www-data git pull origin main

# Or if permission issues, pull as root then fix ownership
sudo git pull origin main
sudo chown -R www-data:www-data /var/www/cybersec-news
```

### Step 3: Update Dependencies

```bash
cd /var/www/cybersec-news

# Update Python packages
sudo -u www-data venv/bin/pip install -r requirements.txt --upgrade
```

### Step 4: Restart Apache

```bash
# Restart Apache to load new code
sudo systemctl restart apache2

# Check status
sudo systemctl status apache2

# Check logs if issues
sudo tail -f /var/log/apache2/cybersec-news-error.log
```

### Step 5: Verify

```bash
# Test application
curl http://localhost/

# Check sources count
sudo -u www-data venv/bin/python3 << EOF
from database import get_sources
sources = get_sources()
print(f"Total sources: {len(sources)}")
EOF
```

Should show ~140 sources

---

## 🔍 Verification Checklist

After updating, verify these items:

### 1. **Navigation Menu**
- [ ] "Updates" link visible in navigation
- [ ] All existing links still work

### 2. **Sources Page** (`/sources`)
- [ ] Total sources: ~140 (was ~90)
- [ ] New "Government CERT" entries visible
- [ ] Sources from: CISA, UK NCSC, CERT-EU, etc.

### 3. **Updates Page** (`/updates`)
- [ ] Page loads successfully
- [ ] Shows repository information
- [ ] "Check Now" button works
- [ ] Shows "Already up to date" ✅

### 4. **Existing Functionality**
- [ ] Dashboard shows news
- [ ] News filtering works
- [ ] CVE page works
- [ ] Priority rules page works
- [ ] Settings page works

### 5. **New Feeds Working**
```bash
# Manually trigger feed fetch
curl http://localhost:5000/api/fetch-feeds -X POST

# Check news count increased
# Visit: http://localhost:5000/news
```

---

## 🔄 What Happens After Update

### Automatic Changes:

1. **New Feeds Added**
   - 52 government CERT feeds automatically added to database
   - All feeds enabled by default
   - Immediate fetch of latest articles

2. **New Settings Added**
   - `auto_update_enabled`: false (off by default)
   - `update_schedule`: daily
   - `backup_before_update`: true
   - `restart_after_update`: false
   - `notify_on_update`: true

3. **New Features Available**
   - Auto-update configuration page
   - Manual update checking
   - Update history tracking

### No Data Loss:

✅ Existing news articles preserved  
✅ Existing feed sources kept  
✅ Priority rules unchanged  
✅ Settings maintained  
✅ Custom configurations preserved  

---

## ❌ Troubleshooting

### ⚡ Quick Fix Reference

For common issues and one-line fixes, see **[QUICKFIX.md](QUICKFIX.md)**

### Problem 1: "Git Pull Failed - Merge Conflict" ⚠️ MOST COMMON

**Error Message**:
```
error: Your local changes to the following files would be overwritten by merge:
    setup.sh
Please commit your changes or stash them before you merge.
Aborting
```

**Cause**: Local files (especially `setup.sh`) were modified

**⚡ Quick Fix (One Command)**:
```bash
git stash && git pull origin main && chmod +x setup.sh service.sh
```

**Step-by-Step Solution**:
```bash
# 1. Stash your changes
git stash
# Output: Saved working directory and index state...

# 2. Pull updates
git pull origin main
# Output: Updating ab8fef0..7981291...

# 3. Make scripts executable
chmod +x setup.sh service.sh

# 4. Verify update
git log --oneline -1
# Should show: 7981291 v2.2.0

# 5. Restart application
./service.sh restart
```

**Important**: Your database and important files are safe! They're in `.gitignore` and won't be affected.

**Alternative**: If you don't need local changes:
```bash
# Discard all local changes (careful!)
git reset --hard origin/main
chmod +x setup.sh service.sh
```

### Problem 2: "Permission Denied"

**Cause**: Wrong file ownership

**Solution**:
```bash
# Fix ownership (adjust user as needed)
sudo chown -R www-data:www-data /var/www/cybersec-news

# Or for home directory
sudo chown -R $USER:$USER ~/SecurityNewWeb

# Fix permissions
chmod -R 755 /var/www/cybersec-news
```

### Problem 3: "Import Error: No module named 'git_updater'"

**Cause**: New file not loaded properly

**Solution**:
```bash
# Verify file exists
ls -lh git_updater.py

# If missing, download it
wget https://raw.githubusercontent.com/boscolam/SecurityNewWeb/main/git_updater.py

# Restart application
```

### Problem 4: "Database Error After Update"

**Cause**: Database corruption or locked

**Solution**:
```bash
# Stop application
sudo systemctl stop cybersec-news

# Check database integrity
sqlite3 cybersec_news.db "PRAGMA integrity_check;"

# If corrupted, restore backup
cp cybersec_news.db.backup cybersec_news.db

# Restart
sudo systemctl start cybersec-news
```

### Problem 5: "No New Sources Showing"

**Cause**: Database didn't update

**Solution**:
```bash
# Manually add new sources
source venv/bin/activate
python3 << EOF
from database import init_db
init_db()  # This will add missing sources
EOF

# Restart application
```

### Problem 6: "Updates Page Shows 404"

**Cause**: Template not loaded or old code cached

**Solution**:
```bash
# Verify template exists
ls -lh templates/updates.html

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Restart with --no-cache
python app.py
```

### Problem 7: "Apache Won't Restart"

**Cause**: Syntax error or missing dependency

**Solution**:
```bash
# Check Apache configuration
sudo apache2ctl configtest

# Check Python syntax
python3 -m py_compile app.py

# View error logs
sudo tail -50 /var/log/apache2/error.log

# Check wsgi logs
sudo tail -50 /var/log/apache2/cybersec-news-error.log
```

---

## 🆘 Emergency Rollback

If something goes wrong and you need to revert:

### Rollback Using Git

```bash
cd ~/SecurityNewWeb

# View commits
git log --oneline

# Rollback to previous version (v1.0)
git reset --hard 540a331  # Replace with your old commit hash

# Restore database backup
cp cybersec_news.db.backup cybersec_news.db

# Restart
python app.py
```

### Rollback Using Backup

```bash
# Stop application
sudo systemctl stop cybersec-news

# Restore from backup
rm -rf ~/SecurityNewWeb
mv ~/SecurityNewWeb.backup_20260921 ~/SecurityNewWeb

# Restart
cd ~/SecurityNewWeb
source venv/bin/activate
python app.py
```

---

## 📊 Post-Update Configuration

### 1. Enable Auto-Update (Optional)

```
1. Visit: http://localhost:5000/updates
2. Check "Enable Automatic Updates"
3. Select schedule: "Daily"
4. Keep "Backup Database" checked
5. Click "Save Settings"
```

### 2. Test New Government CERT Feeds

```
1. Visit: http://localhost:5000/sources
2. Filter by category: "Government CERT"
3. Should see 52 new sources
4. Click "Fetch All Feeds" to get latest news
```

### 3. Review New Features

```
1. Dashboard: Should show news from new CERT sources
2. News page: Filter by "Government" category
3. Updates page: Configure auto-update settings
```

---

## 📞 Need Help?

**Documentation:**
- AUTO_UPDATE_GUIDE.md - Auto-update feature guide
- CHANGELOG.md - Version history
- README.md - Full feature documentation
- UBUNTU_INSTALL.md - Installation guide

**Support:**
- GitHub Issues: https://github.com/boscolam/SecurityNewWeb/issues
- Check logs: `tail -f logs/*.log`

---

## ✅ Update Complete!

Your installation should now be at **v2.1.0** with:

✅ 140+ RSS feeds (52 new government CERTs)  
✅ Auto-update system with web interface  
✅ Update history tracking  
✅ Automatic database backups  

**Next Steps:**
1. Configure auto-update settings
2. Explore new government CERT feeds
3. Review CHANGELOG.md for all changes

---

**Enjoy the new features!** 🎉🔐
