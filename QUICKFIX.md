# Quick Fix Guide - Common Update Issues

Quick solutions for common problems when updating the Cybersecurity News Dashboard.

---

## ⚡ Common Issue #1: Git Pull Merge Conflict

### Error Message:
```
error: Your local changes to the following files would be overwritten by merge:
    setup.sh
Please commit your changes or stash them before you merge.
Aborting
```

### 🔧 **Quick Fix (One Command)**

```bash
git stash && git pull origin main && chmod +x setup.sh service.sh
```

This command will:
1. ✅ Save your local changes temporarily
2. ✅ Pull the latest version
3. ✅ Make new scripts executable

### 📋 **Step-by-Step Fix**

```bash
# 1. Navigate to your installation
cd ~/SecurityNewWeb

# 2. Stash local changes
git stash
# Output: Saved working directory and index state...

# 3. Pull updates
git pull origin main
# Output: Updating ab8fef0..7981291...

# 4. Make scripts executable
chmod +x setup.sh service.sh

# 5. Verify update
git log --oneline -1
# Should show the latest version commit

# 6. Restart application
./service.sh restart
```

### ✅ **What Gets Preserved**

Your important files are **automatically safe**:
- ✅ `cybersec_news.db` - Your database
- ✅ `venv/` - Virtual environment  
- ✅ `.env` - Environment variables
- ✅ All news, settings, and history

---

## ⚡ Common Issue #2: Permission Denied

### Error Message:
```
bash: ./setup.sh: Permission denied
```

### 🔧 **Quick Fix**

```bash
chmod +x setup.sh service.sh
./setup.sh
```

---

## ⚡ Common Issue #3: Service Won't Start

### Error Message:
```
Failed to start cybersec-news.service
```

### 🔧 **Quick Fix**

```bash
# Check status and logs
./service.sh status
./service.sh logs-tail

# Common fixes:
# 1. Fix permissions
sudo chown -R $USER:$USER ~/SecurityNewWeb

# 2. Reinstall service
./service.sh uninstall
./setup.sh --service

# 3. Check Python dependencies
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚡ Common Issue #4: Port 5000 Already in Use

### Error Message:
```
Address already in use
OSError: [Errno 98] Address already in use
```

### 🔧 **Quick Fix**

```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process (replace PID)
kill -9 <PID>

# Or kill all Python processes
pkill -f app.py

# Then restart
./service.sh restart
```

---

## ⚡ Common Issue #5: Database Locked

### Error Message:
```
sqlite3.OperationalError: database is locked
```

### 🔧 **Quick Fix**

```bash
# Stop the service
./service.sh stop

# Wait 5 seconds
sleep 5

# Check for lock files
ls -lh cybersec_news.db*

# Remove stale lock files (if needed)
rm cybersec_news.db-shm cybersec_news.db-wal

# Restart
./service.sh start
```

---

## ⚡ Common Issue #6: Module Not Found After Update

### Error Message:
```
ModuleNotFoundError: No module named 'git_updater'
```

### 🔧 **Quick Fix**

```bash
# Verify file exists
ls -lh git_updater.py

# If missing, pull again
git pull origin main

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Restart service
./service.sh restart
```

---

## ⚡ Common Issue #7: Updates Page Shows 404

### Error Message:
```
404 Not Found - The requested URL was not found
```

### 🔧 **Quick Fix**

```bash
# Verify template exists
ls -lh templates/updates.html

# If missing, pull again
git pull origin main

# Restart with cache clear
./service.sh stop
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
./service.sh start
```

---

## ⚡ Common Issue #8: Git Not Installed

### Error Message:
```
git: command not found
```

### 🔧 **Quick Fix**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y git

# Verify installation
git --version

# Then update
git pull origin main
```

---

## ⚡ Common Issue #9: Virtual Environment Issues

### Error Message:
```
No module named 'flask'
bash: pip: command not found
```

### 🔧 **Quick Fix**

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv

# Activate and reinstall
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Restart
python app.py
```

---

## ⚡ Common Issue #10: Service Logs Full of Errors

### Error Message:
```
Multiple error messages in logs
```

### 🔧 **Quick Fix**

```bash
# View recent errors
./service.sh logs-tail | grep -i error

# Common solutions:
# 1. Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 2. Check database
sqlite3 cybersec_news.db "PRAGMA integrity_check;"

# 3. Restart fresh
./service.sh restart
```

---

## 📋 **General Troubleshooting Steps**

When something goes wrong, try these in order:

### 1. **Check Version**
```bash
git log --oneline -1
cat VERSION
```

### 2. **Check Service Status**
```bash
./service.sh status
```

### 3. **View Recent Logs**
```bash
./service.sh logs-tail
```

### 4. **Verify Files Exist**
```bash
ls -lh *.py *.service *.sh
```

### 5. **Check Permissions**
```bash
ls -lh setup.sh service.sh
# Should show: -rwxr-xr-x (executable)
```

### 6. **Restart Service**
```bash
./service.sh restart
```

### 7. **Reinstall Service**
```bash
./service.sh uninstall
./setup.sh --service
```

---

## 🆘 **Nuclear Option: Clean Reinstall**

If all else fails, reinstall (preserves your database):

```bash
# 1. Backup database
cp cybersec_news.db ~/cybersec_news.db.backup

# 2. Stop service
./service.sh stop 2>/dev/null || pkill -f app.py

# 3. Remove installation
cd ~
rm -rf SecurityNewWeb

# 4. Fresh clone
git clone https://github.com/boscolam/SecurityNewWeb.git
cd SecurityNewWeb

# 5. Setup
./setup.sh --service

# 6. Restore database
cp ~/cybersec_news.db.backup cybersec_news.db

# 7. Start
./service.sh start
```

---

## 🔄 **Update Command Reference**

### Standard Update
```bash
git stash && git pull origin main && chmod +x *.sh && ./service.sh restart
```

### Update with Clean
```bash
git stash && git pull origin main && \
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null && \
chmod +x *.sh && ./service.sh restart
```

### Update and Reinstall Service
```bash
git stash && git pull origin main && chmod +x *.sh && \
./service.sh uninstall && ./setup.sh --service
```

---

## 💡 **Prevention Tips**

1. **Don't Edit Core Files**: Avoid modifying `app.py`, `setup.sh`, etc.
2. **Use Git**: Keep installation as git repository for easy updates
3. **Regular Backups**: Backup database before major updates
4. **Check Logs**: Monitor logs for issues: `./service.sh logs`
5. **Use Service Mode**: Run as service for reliability

---

## 📞 **Still Having Issues?**

1. **Check Logs**:
   ```bash
   ./service.sh logs-tail
   ```

2. **View Full Documentation**:
   - `UPDATE_INSTRUCTIONS.md` - Update guide
   - `AUTO_UPDATE_GUIDE.md` - Auto-update help
   - `UBUNTU_INSTALL.md` - Installation help

3. **Report Issue**:
   - GitHub Issues: https://github.com/boscolam/SecurityNewWeb/issues
   - Include: Error message, OS version, git log output

---

## ✅ **Verification Checklist**

After fixing issues, verify:

- [ ] `git log --oneline -1` shows latest commit
- [ ] `./service.sh status` shows active/running
- [ ] `curl http://localhost:5000` returns HTML
- [ ] Updates page works: http://localhost:5000/updates
- [ ] No errors in logs: `./service.sh logs-tail`

---

**Most Common Solution**: `git stash && git pull origin main && ./service.sh restart`

That fixes 90% of update issues! 🎯
