# Auto-Update Feature Guide

## Overview

The Cybersecurity News Dashboard includes an **Auto-Update** feature that automatically checks for and installs updates from the GitHub repository. This ensures your installation stays current with the latest features, security patches, and bug fixes.

## Features

✅ **Automatic Update Checking**: Configurable schedules (hourly, every 6 hours, daily, weekly)  
✅ **Manual Update Checks**: Check for updates anytime via web interface  
✅ **Safe Updates**: Automatic database backup before updates  
✅ **Git Integration**: Uses git pull to fetch latest changes  
✅ **Update History**: View past updates with commit information  
✅ **Web Interface**: Easy configuration through Settings page  
✅ **Conflict Handling**: Automatically stashes local changes  

---

## Quick Start

### 1. Access the Updates Page

Navigate to: **http://localhost:5000/updates**

Or click **"Updates"** in the main navigation menu.

### 2. Enable Auto-Updates

1. Scroll to **"Auto-Update Settings"**
2. Check **"Enable Automatic Updates"**
3. Select update schedule (e.g., "Daily")
4. Check **"Backup Database Before Update"** (recommended)
5. Click **"Save Settings"**

### 3. Manual Update Check

Click **"Check Now"** button to immediately check for available updates.

If updates are found, click **"Install Update"** to apply them.

---

## Configuration Options

### Update Schedule

Choose how often to check for updates:

- **Every Hour**: Checks every 60 minutes (good for development)
- **Every 6 Hours**: Checks 4 times daily
- **Daily**: Checks once per day at 00:30 (recommended for production)
- **Weekly**: Checks every Sunday at midnight

### Settings Explained

| Setting | Description | Recommended |
|---------|-------------|-------------|
| **Enable Automatic Updates** | Automatically check and install updates | ✅ Yes for production |
| **Update Check Schedule** | How often to check for updates | Daily |
| **Backup Database Before Update** | Create database backup before updating | ✅ Always recommended |
| **Restart After Update** | Attempt automatic restart (requires systemd) | Optional |
| **Log Update Notifications** | Write update logs to application log | ✅ Yes |

---

## How It Works

### Update Process

1. **Fetch**: Application runs `git fetch origin` to check for new commits
2. **Compare**: Compares local HEAD with remote branch
3. **Backup**: If enabled, backs up the database
4. **Stash**: Automatically stashes any local changes
5. **Pull**: Runs `git pull origin main` to update code
6. **Log**: Records update in update_history.json
7. **Notify**: Logs the update to application log

### Safety Mechanisms

✅ **Database Backup**: Automatic backup before each update  
✅ **Local Changes**: Automatically stashes uncommitted changes  
✅ **Git Validation**: Checks if repository is valid before updating  
✅ **Error Handling**: Graceful failure with detailed error messages  
✅ **Update History**: Tracks all updates with timestamps  

---

## Requirements

### System Requirements

1. **Git Installed**: Git must be available on the system
   ```bash
   git --version
   ```

2. **Git Repository**: Application must be in a git repository
   ```bash
   git status
   ```

3. **Remote Configured**: Remote 'origin' must point to GitHub
   ```bash
   git remote -v
   ```

4. **No Conflicts**: Local changes should be minimal or none

### Permissions

The application user (e.g., `www-data` for Apache) must have:
- Read/write access to the application directory
- Permission to run git commands
- Write access for database backups

---

## Manual Update Methods

### Method 1: Using Web Interface

1. Go to **Updates** page
2. Click **"Check Now"**
3. If updates available, click **"Install Update"**
4. Restart application:
   ```bash
   sudo systemctl restart cybersec-news  # systemd
   # OR
   sudo systemctl restart apache2  # Apache
   ```

### Method 2: Using Git Command Line

```bash
# Navigate to application directory
cd /path/to/SecurityNewWeb

# Check for updates
git fetch origin
git status

# Backup database (recommended)
cp cybersec_news.db cybersec_news.db.backup

# Pull updates
git pull origin main

# Restart application
sudo systemctl restart cybersec-news
```

### Method 3: Using Update Script

Create a shell script for easy updates:

```bash
#!/bin/bash
# update.sh - Update script

APP_DIR="/path/to/SecurityNewWeb"
cd "$APP_DIR"

echo "Checking for updates..."
git fetch origin

COMMITS_BEHIND=$(git rev-list --count HEAD..origin/main)

if [ "$COMMITS_BEHIND" -gt 0 ]; then
    echo "$COMMITS_BEHIND new commit(s) available"
    
    echo "Backing up database..."
    cp cybersec_news.db "cybersec_news.db.backup.$(date +%Y%m%d_%H%M%S)"
    
    echo "Pulling updates..."
    git pull origin main
    
    echo "Restarting application..."
    sudo systemctl restart cybersec-news
    
    echo "Update complete!"
else
    echo "Already up to date"
fi
```

Make executable:
```bash
chmod +x update.sh
./update.sh
```

---

## Troubleshooting

### Problem: "Git is not available"

**Solution**: Install git
```bash
sudo apt install -y git  # Ubuntu/Debian
sudo yum install -y git  # CentOS/RHEL
```

### Problem: "Not a git repository"

**Solution**: Clone from GitHub instead of downloading ZIP
```bash
cd /var/www
sudo rm -rf cybersec-news  # Remove if exists
sudo git clone https://github.com/boscolam/SecurityNewWeb.git cybersec-news
cd cybersec-news
# Continue with setup
```

### Problem: "Failed to fetch from remote"

**Solution**: Check internet connectivity and GitHub access
```bash
# Test connectivity
ping github.com

# Test repository access
git ls-remote https://github.com/boscolam/SecurityNewWeb.git
```

### Problem: "Local changes detected"

**Solution 1**: Let auto-update handle it (changes are stashed automatically)

**Solution 2**: Manually commit or stash changes
```bash
# View changes
git status

# Option A: Stash changes
git stash

# Option B: Commit changes
git add .
git commit -m "Local changes"
```

### Problem: "Permission denied"

**Solution**: Fix ownership and permissions
```bash
# For Apache/www-data user
sudo chown -R www-data:www-data /var/www/cybersec-news

# For your user
sudo chown -R $USER:$USER ~/SecurityNewWeb
```

### Problem: "Update succeeded but application not restarting"

**Solution**: Manually restart the application

For systemd service:
```bash
sudo systemctl restart cybersec-news
sudo systemctl status cybersec-news
```

For Apache:
```bash
sudo systemctl restart apache2
```

For direct Python:
```bash
# Stop current process (Ctrl+C)
# Then restart:
cd ~/SecurityNewWeb
source venv/bin/activate
python app.py
```

---

## Advanced Configuration

### Automatic Restart with Systemd

To enable automatic restart after updates, the application must run as a systemd service.

**1. Create systemd service** (see UBUNTU_INSTALL.md)

**2. Modify service to allow restart**:
```bash
sudo nano /etc/systemd/system/cybersec-news.service
```

Add to `[Service]` section:
```ini
Restart=always
RestartSec=10
```

**3. Reload and enable**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cybersec-news
```

### Custom Update Schedule

To add custom update times, edit `app.py` and add a new cron job:

```python
# Example: Update at 3 AM daily
scheduler.add_job(
    check_and_update_if_needed,
    'cron',
    hour=3, minute=0,
    id='auto_update',
    name='Daily auto-update at 3 AM'
)
```

### Email Notifications on Update

Modify `git_updater.py` to send email notifications:

```python
def send_update_notification(result):
    """Send email notification about update."""
    import smtplib
    from email.message import EmailMessage
    
    msg = EmailMessage()
    msg['Subject'] = 'CyberSec Dashboard Updated'
    msg['From'] = 'dashboard@yourserver.com'
    msg['To'] = 'admin@yourserver.com'
    msg.set_content(f"Update successful: {result['message']}")
    
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)

# Add to perform_update() function after successful update
if result['success']:
    send_update_notification(result)
```

---

## Security Considerations

### Best Practices

✅ **Backup Regularly**: Always enable database backup before updates  
✅ **Test First**: Test updates in development before enabling in production  
✅ **Monitor Logs**: Regularly check update logs for issues  
✅ **Verify Updates**: Review CHANGELOG.md before major updates  
✅ **Limited Auto-Update**: Consider disabling for critical production systems  

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking changes | Review CHANGELOG before enabling auto-update |
| Database corruption | Automatic backups before each update |
| Downtime | Schedule updates during maintenance windows |
| Failed updates | Manual rollback capability |
| Unauthorized changes | Use official GitHub repository only |

### Production Recommendations

For **production systems**:

1. **Disable automatic installation**: Only enable automatic *checking*
2. **Manual approval**: Review updates before installing
3. **Maintenance window**: Schedule updates during low-traffic periods
4. **Test environment**: Test updates in staging before production
5. **Monitoring**: Set up alerts for update failures

For **development/testing**:
- Auto-update can be safely enabled for convenience
- Hourly or daily checks recommended

---

## Update History

View update history on the Updates page:

- **Timestamp**: When update was performed
- **Commit Range**: Old commit → New commit
- **Status**: Success or failure
- **Message**: Update summary

History is stored in: `update_history.json` (last 50 updates)

---

## API Endpoints

For programmatic access:

### Check for Updates
```bash
curl http://localhost:5000/api/git/check-updates
```

Response:
```json
{
  "available": true,
  "commits_behind": 2,
  "current_commit": "abc123...",
  "branch": "main",
  "message": "2 new commit(s) available"
}
```

### Get Git Info
```bash
curl http://localhost:5000/api/git/info
```

### Perform Update
```bash
curl -X POST http://localhost:5000/api/git/update
```

### Get Update History
```bash
curl http://localhost:5000/api/git/history
```

---

## FAQ

**Q: Will auto-update overwrite my custom changes?**  
A: Local changes are automatically stashed. However, it's recommended to avoid modifying core files.

**Q: How do I disable auto-update?**  
A: Uncheck "Enable Automatic Updates" on the Updates page.

**Q: Can I rollback an update?**  
A: Yes, use git to revert:
```bash
git log  # Find commit hash
git reset --hard <commit-hash>
```

**Q: What happens if an update fails?**  
A: The application continues running with the previous version. Check logs for error details.

**Q: Do I need to restart after every update?**  
A: Yes, for code changes to take effect. Database-only changes may not require restart.

**Q: Can I update to a specific version?**  
A: Yes, manually:
```bash
git fetch --tags
git checkout v2.0.0  # Replace with desired version
```

---

## Support

- **Documentation**: Check README.md and CHANGELOG.md
- **Issues**: https://github.com/boscolam/SecurityNewWeb/issues
- **Logs**: Check application logs for update details

---

## Version Information

- **Feature Added**: v2.1.0
- **Last Updated**: 2026-09-21
- **Status**: Stable

---

**Happy Updating! 🚀**
