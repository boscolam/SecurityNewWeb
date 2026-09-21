# How to Restart the Application After Updates

When you pull new updates from GitHub, you need to restart the application to load the new routes and features.

## Quick Restart

### If Running as a Service:
```bash
# User service
./service.sh restart

# OR system service
sudo ./service.sh restart
```

### If Running Manually:
```bash
# Stop the current process
pkill -f "python.*app.py"

# Start again
source venv/bin/activate
python3 app.py
```

---

## Fix "Could not build url for endpoint" Errors

This error means Flask doesn't know about the new routes because the app wasn't restarted.

### Step 1: Pull Latest Changes
```bash
cd /path/to/SecurityNewWeb
git pull origin main
```

### Step 2: Restart Application
```bash
./service.sh restart
```

### Step 3: Verify
```bash
./service.sh health
```

---

## Common Issues

### Issue: Changes Not Taking Effect
**Solution**: Hard restart
```bash
# Stop everything
pkill -f "python.*app.py"
./service.sh stop

# Clear cache
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Restart
./service.sh start
```

### Issue: Service Won't Restart
**Solution**: Check logs first
```bash
./service.sh logs-tail
```

Common fixes:
```bash
# Fix permissions
chmod +x *.sh

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt

# Reinstall service
./service.sh uninstall
./setup.sh --service
```

### Issue: Port 5000 Already in Use
**Solution**: Kill the process
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill it
sudo kill -9 $(lsof -ti :5000)

# Or use pkill
pkill -f "python.*app.py"

# Restart
./service.sh start
```

---

## After Every Git Pull

**Always restart the application:**
```bash
git pull origin main
./service.sh restart
```

**Or use auto-update** (configured in web interface at /updates):
- Enable "Restart after update"
- Application will automatically restart after pulling updates
- No manual intervention needed

---

## Verify New Features Loaded

After restart, check available routes:
```bash
curl -s http://localhost:5000/ | grep -o 'href="/[^"]*"' | sort -u
```

Should include:
- `/logs` - Logs viewer (v2.3.0+)
- `/updates` - Auto-update (v2.1.0+)
- `/sources` - Feed sources
- `/priorities` - Priority rules
- `/settings` - Settings

---

## Quick Test

Test if new routes work:
```bash
# Test logs page
curl -I http://localhost:5000/logs

# Should return: HTTP/1.1 200 OK

# Test logs API
curl -s http://localhost:5000/api/logs/list | jq
```

If you get 404, the app needs to be restarted.

---

## Automated Restart Setup

Enable auto-restart in settings:

1. Go to http://localhost:5000/settings
2. Find "restart_after_update" setting
3. Set to "true"
4. Save

OR via command line:
```bash
sqlite3 cybersec_news.db "UPDATE settings SET value='true' WHERE key='restart_after_update';"
```

Now updates will automatically restart the service!
