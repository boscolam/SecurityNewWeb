# Permission Issues - Fix Guide

Common permission errors and how to fix them with automatic user/group detection.

---

## 🔍 **Common Permission Errors**

### Error 1: "Permission denied"
```
bash: ./setup.sh: Permission denied
bash: ./service.sh: Permission denied
```

### Error 2: "Unable to open database file"
```
sqlite3.OperationalError: unable to open database file
```

### Error 3: "Failed to locate executable"
```
Failed to locate executable /path/to/venv/bin/python3: No such file or directory
```

---

## ✅ **Automatic Fix (Recommended)**

The setup script now **automatically detects** your user, group, and installation path!

### **Step 1: Fix Permissions**

```bash
# Navigate to your installation directory
cd ~/SecurityNewWeb
# OR
cd /home/yourusername/news/SecurityNewWeb

# Fix ownership (auto-detects current user and group)
sudo chown -R $USER:$(id -gn) .

# Fix file permissions
chmod -R 755 .

# Make scripts executable
chmod +x setup.sh service.sh
```

### **Step 2: Reinstall Service (Automatic Detection)**

```bash
# The setup script will automatically detect:
# - Current user: $USER
# - Current group: $(id -gn)
# - Installation path: $(pwd)

# For user service (home directory)
./setup.sh --service

# OR for system service (production)
sudo ./setup.sh --system-service
```

The service file will be automatically configured with:
- **User**: Your current username (auto-detected)
- **Group**: Your current group (auto-detected)
- **Path**: Your installation directory (auto-detected)

---

## 🔧 **Manual Fix (If Needed)**

### **Check Current User & Group**

```bash
# Check your username
echo "User: $USER"
whoami

# Check your group
echo "Group: $(id -gn)"
id -gn

# Check current directory
pwd
```

### **Fix for Specific Path**

Replace `/path/to/SecurityNewWeb` with your actual path:

```bash
# Go to installation directory
cd /path/to/SecurityNewWeb

# Fix ownership with auto-detection
sudo chown -R $USER:$(id -gn) .

# Fix permissions
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# Make scripts executable
chmod +x setup.sh service.sh *.sh 2>/dev/null

# Reinstall service
./setup.sh --service
```

---

## 📊 **Verify Permissions**

After fixing permissions:

```bash
# Check directory ownership
ls -ld /path/to/SecurityNewWeb
# Should show: drwxr-xr-x ... username groupname

# Check files
ls -lh setup.sh service.sh
# Should show: -rwxr-xr-x ... username groupname

# Check if you can write
touch test.txt && rm test.txt && echo "✓ Write permission OK"

# Check service file
cat ~/.config/systemd/user/cybersec-news.service
# Should show your actual username and paths (no __INSTALL_PATH__ placeholders)
```

---

## 🎯 **Examples by Installation Location**

### **Example 1: Home Directory**

```bash
# Installation: /home/bosco/SecurityNewWeb
cd /home/bosco/SecurityNewWeb
sudo chown -R bosco:bosco .
chmod -R 755 .
./setup.sh --service

# Service will use:
# User: bosco (auto-detected)
# Group: bosco (auto-detected)
# Path: /home/bosco/SecurityNewWeb (auto-detected)
```

### **Example 2: Custom Directory**

```bash
# Installation: /home/username/news/SecurityNewWeb
cd /home/username/news/SecurityNewWeb
sudo chown -R $USER:$(id -gn) .
chmod -R 755 .
./setup.sh --service

# Service will use:
# User: username (auto-detected)
# Group: username (auto-detected)
# Path: /home/username/news/SecurityNewWeb (auto-detected)
```

### **Example 3: System Installation**

```bash
# Installation: /opt/cybersec-news
cd /opt/cybersec-news
sudo chown -R myuser:myuser .
chmod -R 755 .
sudo ./setup.sh --system-service

# Service will use:
# User: myuser (auto-detected)
# Group: myuser (auto-detected)
# Path: /opt/cybersec-news (auto-detected)
```

---

## 🔍 **Troubleshooting**

### **Issue: Service file still has placeholders**

Check if service file has unprocessed placeholders:

```bash
# For user service
cat ~/.config/systemd/user/cybersec-news.service | grep "__"

# For system service
sudo cat /etc/systemd/system/cybersec-news.service | grep "__"

# If you see __INSTALL_PATH__, __INSTALL_USER__, etc., reinstall:
./setup.sh --service
```

### **Issue: Wrong user in service file**

```bash
# Remove and reinstall service
./service.sh uninstall

# Reinstall (will auto-detect current user)
./setup.sh --service

# Verify
cat ~/.config/systemd/user/cybersec-news.service | grep "User="
```

### **Issue: Virtual environment not found**

```bash
# Check venv exists
ls -lh venv/bin/python3

# If missing, recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reinstall service
./setup.sh --service
```

---

## 📋 **Complete Fix Script**

Save this as `fix-permissions.sh`:

```bash
#!/bin/bash

echo "=== Permission Fix Script ==="
echo ""

# Detect current info
CURRENT_USER="${USER:-$(whoami)}"
CURRENT_GROUP=$(id -gn)
CURRENT_PATH=$(pwd)

echo "Detected configuration:"
echo "  User: $CURRENT_USER"
echo "  Group: $CURRENT_GROUP"
echo "  Path: $CURRENT_PATH"
echo ""

# Confirm
read -p "Fix permissions for this directory? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Fix ownership
echo "Fixing ownership..."
sudo chown -R $CURRENT_USER:$CURRENT_GROUP .

# Fix permissions
echo "Fixing permissions..."
find . -type d -exec chmod 755 {} \; 2>/dev/null
find . -type f -exec chmod 644 {} \; 2>/dev/null
chmod +x *.sh 2>/dev/null

# Test write permission
if touch test_write.txt 2>/dev/null; then
    rm test_write.txt
    echo "✓ Write permission OK"
else
    echo "✗ Still cannot write!"
    exit 1
fi

# Check venv
if [ ! -f venv/bin/python3 ]; then
    echo "Virtual environment missing, creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

echo ""
echo "✓ Permissions fixed!"
echo ""
echo "Next steps:"
echo "  1. Install service: ./setup.sh --service"
echo "  2. Check status: ./service.sh status"
echo "  3. View logs: ./service.sh logs"
```

Run it:

```bash
chmod +x fix-permissions.sh
./fix-permissions.sh
```

---

## 🎉 **Summary**

**What's Automatic:**
- ✅ User detection ($USER)
- ✅ Group detection ($(id -gn))
- ✅ Path detection ($(pwd))
- ✅ Service file configuration
- ✅ No hardcoded values

**What You Do:**
1. Fix ownership: `sudo chown -R $USER:$(id -gn) .`
2. Fix permissions: `chmod -R 755 .`
3. Run setup: `./setup.sh --service`

**Result:**
- Service runs as YOUR user
- Uses YOUR installation path
- No manual editing needed!

---

**No more hardcoded usernames or paths!** 🎊
