#!/bin/bash
# ============================================================
# Service Management Script for Cybersecurity News Dashboard
# ============================================================
# Helper script to manage the systemd service
#
# Usage:
#   ./service.sh status    # Check service status
#   ./service.sh start     # Start service
#   ./service.sh stop      # Stop service
#   ./service.sh restart   # Restart service
#   ./service.sh logs      # View logs (live)
#   ./service.sh health    # Comprehensive health check
#   ./service.sh analyze   # Detailed analysis with recommendations
#   ./service.sh install   # Install service
#   ./service.sh uninstall # Remove service
# ============================================================

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Detect service mode
SERVICE_NAME="cybersec-news"

# Check if running as system service
if [ -f "/etc/systemd/system/${SERVICE_NAME}.service" ]; then
    SERVICE_MODE="system"
    SYSTEMCTL="sudo systemctl"
    JOURNALCTL="sudo journalctl"
# Check if running as user service
elif [ -f "$HOME/.config/systemd/user/${SERVICE_NAME}.service" ]; then
    SERVICE_MODE="user"
    SYSTEMCTL="systemctl --user"
    JOURNALCTL="journalctl --user"
else
    SERVICE_MODE="none"
fi

# Print colored message
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Show help
show_help() {
    cat << EOF
Service Management Script for Cybersecurity News Dashboard

USAGE:
    ./service.sh COMMAND

COMMANDS:
    status      Show service status
    start       Start the service
    stop        Stop the service
    restart     Restart the service
    reload      Reload service configuration
    enable      Enable service (start on boot)
    disable     Disable service (don't start on boot)
    logs        View service logs (live, Ctrl+C to exit)
    logs-tail   View last 100 log lines
    health      Comprehensive system health check (NEW!)
    analyze     Detailed analysis with recommendations (NEW!)
    verify      Verify service file integrity (NEW!)
    install     Install systemd service
    uninstall   Remove systemd service

EXAMPLES:
    ./service.sh status          # Quick status check
    ./service.sh health          # Full health check (recommended!)
    ./service.sh analyze         # Detailed analysis
    ./service.sh verify          # Verify service file integrity
    ./service.sh restart         # Restart service
    ./service.sh logs            # View live logs

CURRENT SERVICE MODE:
EOF

    if [ "$SERVICE_MODE" = "system" ]; then
        echo "    System service (runs as www-data, starts on boot)"
    elif [ "$SERVICE_MODE" = "user" ]; then
        echo "    User service (runs as $USER)"
    else
        echo "    No service installed"
        echo ""
        echo "To install:"
        echo "    ./service.sh install"
        echo "    OR"
        echo "    ./setup.sh --service"
    fi
    echo ""
}

# Check if service is installed
check_service() {
    if [ "$SERVICE_MODE" = "none" ]; then
        print_error "Service not installed"
        echo ""
        echo "Install service with:"
        echo "  ./setup.sh --service           # User service"
        echo "  sudo ./setup.sh --system-service  # System service"
        echo "  ./service.sh install           # Interactive installation"
        exit 1
    fi
}

# Status command
cmd_status() {
    check_service
    echo "Service: $SERVICE_NAME ($SERVICE_MODE mode)"
    echo ""
    $SYSTEMCTL status $SERVICE_NAME
}

# Start command
cmd_start() {
    check_service
    print_info "Starting $SERVICE_NAME..."
    $SYSTEMCTL start $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_success "Service started"
        echo ""
        echo "Access dashboard at: http://localhost:5000"
    else
        print_error "Failed to start service"
        exit 1
    fi
}

# Stop command
cmd_stop() {
    check_service
    print_info "Stopping $SERVICE_NAME..."
    $SYSTEMCTL stop $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_success "Service stopped"
    else
        print_error "Failed to stop service"
        exit 1
    fi
}

# Restart command
cmd_restart() {
    check_service
    print_info "Restarting $SERVICE_NAME..."
    $SYSTEMCTL restart $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_success "Service restarted"
        echo ""
        echo "Access dashboard at: http://localhost:5000"
    else
        print_error "Failed to restart service"
        exit 1
    fi
}

# Reload command
cmd_reload() {
    check_service
    print_info "Reloading systemd configuration..."
    if [ "$SERVICE_MODE" = "system" ]; then
        sudo systemctl daemon-reload
    else
        systemctl --user daemon-reload
    fi
    print_success "Configuration reloaded"
}

# Enable command
cmd_enable() {
    check_service
    print_info "Enabling $SERVICE_NAME..."
    $SYSTEMCTL enable $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_success "Service will start on boot"
    else
        print_error "Failed to enable service"
        exit 1
    fi
}

# Disable command
cmd_disable() {
    check_service
    print_info "Disabling $SERVICE_NAME..."
    $SYSTEMCTL disable $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_success "Service will not start on boot"
    else
        print_error "Failed to disable service"
        exit 1
    fi
}

# Logs command (live)
cmd_logs() {
    check_service
    print_info "Showing live logs (Ctrl+C to exit)..."
    echo ""
    $JOURNALCTL -u $SERVICE_NAME -f
}

# Logs tail command
cmd_logs_tail() {
    check_service
    print_info "Last 100 log entries:"
    echo ""
    $JOURNALCTL -u $SERVICE_NAME -n 100 --no-pager
}

# Install command
cmd_install() {
    if [ "$SERVICE_MODE" != "none" ]; then
        print_warning "Service already installed ($SERVICE_MODE mode)"
        echo ""
        read -p "Reinstall? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi

    echo ""
    echo "Install Cybersecurity News Dashboard as a service"
    echo ""
    echo "Choose installation mode:"
    echo "  1) User service (runs under your account, recommended for home directory)"
    echo "  2) System service (runs as www-data, starts on boot, requires sudo)"
    echo ""
    read -p "Enter choice (1 or 2): " -n 1 -r
    echo ""

    if [[ $REPLY == "1" ]]; then
        print_info "Installing user service..."
        ./setup.sh --service
    elif [[ $REPLY == "2" ]]; then
        print_info "Installing system service..."
        sudo ./setup.sh --system-service
    else
        print_error "Invalid choice"
        exit 1
    fi
}

# Uninstall command
cmd_uninstall() {
    check_service

    print_warning "This will remove the $SERVICE_NAME service"
    read -p "Continue? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi

    # Stop service
    print_info "Stopping service..."
    $SYSTEMCTL stop $SERVICE_NAME 2>/dev/null

    # Disable service
    print_info "Disabling service..."
    $SYSTEMCTL disable $SERVICE_NAME 2>/dev/null

    # Remove service file
    if [ "$SERVICE_MODE" = "system" ]; then
        sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service
        sudo systemctl daemon-reload
    else
        rm -f ~/.config/systemd/user/${SERVICE_NAME}.service
        systemctl --user daemon-reload
    fi

    print_success "Service uninstalled"
    echo ""
    echo "The application files are still in: $(pwd)"
    echo "You can still run manually with: python app.py"
}

# Health check command
cmd_health() {
    echo "============================================"
    echo "  System Health Check"
    echo "============================================"
    echo ""

    ISSUES=0
    WARNINGS=0

    # 1. Check service installation
    echo "[1/10] Service Installation"
    if [ "$SERVICE_MODE" != "none" ]; then
        print_success "Service installed ($SERVICE_MODE mode)"
    else
        print_error "Service not installed"
        ISSUES=$((ISSUES + 1))
        echo "       Run: ./setup.sh --service"
    fi
    echo ""

    # 2. Check service status
    echo "[2/10] Service Status"
    if [ "$SERVICE_MODE" != "none" ]; then
        # Get the actual service state
        SERVICE_STATE=$($SYSTEMCTL is-active $SERVICE_NAME 2>/dev/null || echo "unknown")

        if [ "$SERVICE_STATE" = "active" ]; then
            print_success "Service is running"
        elif [ "$SERVICE_STATE" = "activating" ]; then
            print_info "Service is starting..."
        elif [ "$SERVICE_STATE" = "inactive" ]; then
            print_error "Service is stopped"
            ISSUES=$((ISSUES + 1))
            echo "       Run: ./service.sh start"
        elif [ "$SERVICE_STATE" = "failed" ]; then
            print_error "Service failed to start"
            ISSUES=$((ISSUES + 1))
            echo "       Run: ./service.sh logs-tail to see errors"
            echo "       Run: ./service.sh restart to try again"
        else
            print_error "Service state: $SERVICE_STATE"
            ISSUES=$((ISSUES + 1))
            echo "       Run: ./service.sh status for details"
        fi
    else
        print_info "No service installed"
    fi
    echo ""

    # 3. Check process
    echo "[3/10] Application Process"
    if pgrep -f "python.*app.py" > /dev/null; then
        PID=$(pgrep -f "python.*app.py")
        print_success "Process running (PID: $PID)"
    else
        print_error "Application process not found"
        ISSUES=$((ISSUES + 1))
    fi
    echo ""

    # 4. Check port availability
    echo "[4/10] Port 5000 Availability"
    if command -v lsof >/dev/null 2>&1; then
        if sudo lsof -i :5000 >/dev/null 2>&1; then
            print_success "Port 5000 is in use (application listening)"
        else
            print_warning "Port 5000 not in use"
            WARNINGS=$((WARNINGS + 1))
            echo "       Application may not be listening"
        fi
    else
        if netstat -tuln 2>/dev/null | grep -q ":5000 "; then
            print_success "Port 5000 is in use"
        else
            print_warning "Port 5000 not in use"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
    echo ""

    # 5. Check virtual environment
    echo "[5/10] Virtual Environment"
    if [ -f "venv/bin/python3" ]; then
        print_success "Virtual environment exists"
        VENV_PYTHON=$(venv/bin/python3 --version 2>&1)
        echo "       $VENV_PYTHON"
    else
        print_error "Virtual environment missing"
        ISSUES=$((ISSUES + 1))
        echo "       Run: python3 -m venv venv"
    fi
    echo ""

    # 6. Check database
    echo "[6/10] Database"
    if [ -f "cybersec_news.db" ]; then
        DB_SIZE=$(du -h cybersec_news.db | cut -f1)
        print_success "Database exists ($DB_SIZE)"

        # Check if database is accessible
        if command -v sqlite3 >/dev/null 2>&1; then
            SOURCE_COUNT=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM sources;" 2>/dev/null || echo "0")
            NEWS_COUNT=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM news;" 2>/dev/null || echo "0")
            echo "       Sources: $SOURCE_COUNT, News: $NEWS_COUNT"
        fi
    else
        print_warning "Database not found"
        WARNINGS=$((WARNINGS + 1))
        echo "       Will be created on first run"
    fi
    echo ""

    # 7. Check Python dependencies
    echo "[7/10] Python Dependencies"
    if [ -f "venv/bin/pip" ]; then
        INSTALLED_PKGS=$(venv/bin/pip list 2>/dev/null | wc -l)
        if [ "$INSTALLED_PKGS" -gt 5 ]; then
            print_success "Dependencies installed ($INSTALLED_PKGS packages)"
        else
            print_error "Dependencies missing"
            ISSUES=$((ISSUES + 1))
            echo "       Run: source venv/bin/activate && pip install -r requirements.txt"
        fi
    else
        print_error "Cannot check dependencies (no venv)"
        ISSUES=$((ISSUES + 1))
    fi
    echo ""

    # 8. Check logs for errors
    echo "[8/10] Recent Error Logs"
    if [ "$SERVICE_MODE" != "none" ]; then
        ERROR_COUNT=$($JOURNALCTL -u $SERVICE_NAME --since "1 hour ago" -p err 2>/dev/null | grep -c "error" || echo "0")
        if [ "$ERROR_COUNT" -eq 0 ]; then
            print_success "No errors in last hour"
        else
            print_warning "$ERROR_COUNT error(s) in last hour"
            WARNINGS=$((WARNINGS + 1))
            echo "       Run: ./service.sh logs-tail"
        fi
    else
        print_info "No service logs to check"
    fi
    echo ""

    # 9. Check disk space
    echo "[9/10] Disk Space"
    DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -lt 90 ]; then
        print_success "Disk space OK (${DISK_USAGE}% used)"
    else
        print_warning "Disk space low (${DISK_USAGE}% used)"
        WARNINGS=$((WARNINGS + 1))
    fi
    echo ""

    # 10. Check web access
    echo "[10/10] Web Access"
    if command -v curl >/dev/null 2>&1; then
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200"; then
            print_success "Dashboard accessible (HTTP 200)"
        else
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)
            print_warning "Dashboard returned HTTP $HTTP_CODE"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        print_info "curl not available, skipping web check"
    fi
    echo ""

    # Summary
    echo "============================================"
    echo "  Health Check Summary"
    echo "============================================"
    if [ "$ISSUES" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
        echo -e "${GREEN}✓ ALL SYSTEMS OPERATIONAL${NC}"
        echo ""
        echo "Your Cybersecurity News Dashboard is healthy!"
        return 0
    elif [ "$ISSUES" -eq 0 ]; then
        echo -e "${YELLOW}⚠ OPERATIONAL WITH WARNINGS${NC}"
        echo "Warnings: $WARNINGS"
        echo ""
        echo "The system is running but has minor issues."
        return 0
    else
        echo -e "${RED}✗ ISSUES DETECTED${NC}"
        echo "Critical Issues: $ISSUES"
        echo "Warnings: $WARNINGS"
        echo ""
        echo "Run: ./service.sh analyze for detailed recommendations"
        return 1
    fi
}

# Analyze command with recommendations
cmd_analyze() {
    echo "============================================"
    echo "  System Analysis & Recommendations"
    echo "============================================"
    echo ""

    # Check if service exists
    if [ "$SERVICE_MODE" = "none" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Issue: Service Not Installed"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "The systemd service is not installed."
        echo ""
        echo "Recommendation:"
        echo "  ./setup.sh --service           # User service"
        echo "  sudo ./setup.sh --system-service  # System service"
        echo ""
    fi

    # Check service status and analyze
    if [ "$SERVICE_MODE" != "none" ]; then
        SERVICE_STATE=$($SYSTEMCTL is-active $SERVICE_NAME 2>/dev/null || echo "unknown")

        if [ "$SERVICE_STATE" != "active" ]; then
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Issue: Service Not Running Properly"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

            # Get detailed status
            FAILED_REASON=$($SYSTEMCTL status $SERVICE_NAME 2>&1 | grep "Active:" || echo "Unknown")
            echo "Status: $FAILED_REASON"
            echo "State: $SERVICE_STATE"
            echo ""

            # Check recent logs for errors
            echo "Recent Errors:"
            $JOURNALCTL -u $SERVICE_NAME -n 20 -p err --no-pager 2>/dev/null || echo "No error logs available"
            echo ""

            # Check if it's a service file issue
            if [ "$SERVICE_MODE" = "system" ]; then
                SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
            else
                SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"
            fi

            # Check for corrupted service file
            if [ -f "$SERVICE_FILE" ]; then
                if grep -q "__INSTALL_" "$SERVICE_FILE"; then
                    echo "⚠ CORRUPTED SERVICE FILE DETECTED!"
                    echo "   Service file contains unreplaced placeholders"
                    echo ""
                fi
            fi

            echo "Recommendation:"
            echo "  1. Check logs: ./service.sh logs-tail"
            echo "  2. Check service file: $SERVICE_FILE"
            echo "  3. Reinstall service: ./service.sh uninstall && ./setup.sh --service"
            echo "  4. Check permissions: ls -la venv/bin/python3"
            echo "  5. Manual test: source venv/bin/activate && python3 app.py"
            echo ""
        else
            print_success "Service is running normally"
            echo ""
        fi
    fi

    # Check for common issues
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Configuration Check"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Virtual environment
    if [ ! -f "venv/bin/python3" ]; then
        print_error "Virtual environment missing"
        echo "  Fix: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        echo ""
    else
        print_success "Virtual environment OK"
    fi

    # Database
    if [ ! -f "cybersec_news.db" ]; then
        print_warning "Database not initialized"
        echo "  Note: Will be created on first run"
        echo ""
    else
        print_success "Database exists"

        # Check database health
        if command -v sqlite3 >/dev/null 2>&1; then
            INTEGRITY=$(sqlite3 cybersec_news.db "PRAGMA integrity_check;" 2>/dev/null || echo "error")
            if [ "$INTEGRITY" = "ok" ]; then
                print_success "Database integrity OK"
            else
                print_error "Database integrity check failed"
                echo "  Fix: Restore from backup or reinitialize"
            fi
        fi
        echo ""
    fi

    # Permissions
    OWNER=$(stat -c '%U' . 2>/dev/null || stat -f '%Su' . 2>/dev/null)
    CURRENT_USER=$(whoami)
    if [ "$OWNER" = "$CURRENT_USER" ]; then
        print_success "Permissions OK (owner: $OWNER)"
    else
        print_warning "Directory owned by $OWNER, you are $CURRENT_USER"
        echo "  Fix: sudo chown -R $CURRENT_USER:$(id -gn) ."
    fi
    echo ""

    # Performance metrics
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Performance Metrics"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if pgrep -f "python.*app.py" > /dev/null; then
        PID=$(pgrep -f "python.*app.py")

        # Memory usage
        if command -v ps >/dev/null 2>&1; then
            MEM=$(ps -p $PID -o rss= 2>/dev/null | awk '{print int($1/1024)}')
            echo "Memory Usage: ${MEM}MB"

            if [ "$MEM" -lt 100 ]; then
                print_success "Memory usage normal"
            elif [ "$MEM" -lt 300 ]; then
                print_info "Memory usage moderate"
            else
                print_warning "Memory usage high"
                echo "  Consider: Reduce news retention or restart service"
            fi
        fi

        # CPU usage
        if command -v top >/dev/null 2>&1; then
            CPU=$(top -b -n 1 -p $PID 2>/dev/null | tail -1 | awk '{print $9}' || echo "N/A")
            echo "CPU Usage: $CPU%"
        fi

        # Uptime
        if command -v ps >/dev/null 2>&1; then
            UPTIME=$(ps -p $PID -o etime= 2>/dev/null || echo "N/A")
            echo "Uptime: $UPTIME"
        fi
    else
        print_info "Application not running - no metrics available"
    fi
    echo ""

    # News feed stats
    if [ -f "cybersec_news.db" ] && command -v sqlite3 >/dev/null 2>&1; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "News Feed Statistics"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        TOTAL_SOURCES=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM sources;" 2>/dev/null || echo "0")
        ENABLED_SOURCES=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM sources WHERE enabled=1;" 2>/dev/null || echo "0")
        TOTAL_NEWS=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM news;" 2>/dev/null || echo "0")
        RECENT_NEWS=$(sqlite3 cybersec_news.db "SELECT COUNT(*) FROM news WHERE datetime(fetched_date) > datetime('now', '-24 hours');" 2>/dev/null || echo "0")

        echo "Total Sources: $TOTAL_SOURCES"
        echo "Enabled Sources: $ENABLED_SOURCES"
        echo "Total News Articles: $TOTAL_NEWS"
        echo "News (Last 24h): $RECENT_NEWS"

        if [ "$RECENT_NEWS" -gt 0 ]; then
            print_success "Feeds are being updated"
        else
            print_warning "No recent news fetched"
            echo "  Check: Feed fetching may not be working"
            echo "  Action: Check logs for feed errors"
        fi
    fi
    echo ""

    # Recommendations
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Recommendations"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ "$SERVICE_MODE" != "none" ] && $SYSTEMCTL is-active --quiet $SERVICE_NAME; then
        echo "✓ System appears healthy"
        echo ""
        echo "Maintenance tips:"
        echo "  • Monitor logs: ./service.sh logs"
        echo "  • Check updates: http://localhost:5000/updates"
        echo "  • View dashboard: http://localhost:5000"
        echo "  • Backup database: cp cybersec_news.db cybersec_news.db.backup"
    else
        echo "⚠ Action required - see issues above"
        echo ""
        echo "Quick fixes:"
        echo "  • Restart service: ./service.sh restart"
        echo "  • View logs: ./service.sh logs-tail"
        echo "  • Reinstall: ./setup.sh --service"
    fi
    echo ""
}

# Verify service file integrity
cmd_verify() {
    echo "============================================"
    echo "  Service File Verification"
    echo "============================================"
    echo ""

    if [ "$SERVICE_MODE" = "none" ]; then
        print_error "No service installed"
        echo ""
        echo "Install service with:"
        echo "  ./setup.sh --service           # User service"
        echo "  sudo ./setup.sh --system-service  # System service"
        exit 1
    fi

    # Get service file path
    if [ "$SERVICE_MODE" = "system" ]; then
        SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    else
        SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"
    fi

    echo "Service Mode: $SERVICE_MODE"
    echo "Service File: $SERVICE_FILE"
    echo ""

    if [ ! -f "$SERVICE_FILE" ]; then
        print_error "Service file not found!"
        echo ""
        echo "Fix: Reinstall service with ./setup.sh --service"
        exit 1
    fi

    # Check for unreplaced placeholders
    ISSUES_FOUND=0

    echo "Checking for configuration issues..."
    echo ""

    if grep -q "__INSTALL_USER__" "$SERVICE_FILE"; then
        print_error "Found unreplaced __INSTALL_USER__ placeholder"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if grep -q "__INSTALL_GROUP__" "$SERVICE_FILE"; then
        print_error "Found unreplaced __INSTALL_GROUP__ placeholder"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if grep -q "__INSTALL_PATH__" "$SERVICE_FILE"; then
        print_error "Found unreplaced __INSTALL_PATH__ placeholder"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check for proper Description field
    DESCRIPTION=$(grep "^Description=" "$SERVICE_FILE" | cut -d'=' -f2-)
    if [ -z "$DESCRIPTION" ]; then
        print_error "Missing Description field"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    elif [ "$DESCRIPTION" != "Cybersecurity News Dashboard" ] && [ "$DESCRIPTION" != "Cybersecurity News Dashboard (User Service)" ]; then
        print_error "Incorrect Description: $DESCRIPTION"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        print_success "Description field OK"
    fi

    # Check ExecStart path
    EXEC_START=$(grep "^ExecStart=" "$SERVICE_FILE" | cut -d'=' -f2-)
    if [ -n "$EXEC_START" ]; then
        PYTHON_PATH=$(echo "$EXEC_START" | awk '{print $1}')
        if [ -f "$PYTHON_PATH" ]; then
            print_success "Python executable exists: $PYTHON_PATH"
        else
            print_error "Python executable not found: $PYTHON_PATH"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        fi
    fi

    # Check WorkingDirectory
    WORK_DIR=$(grep "^WorkingDirectory=" "$SERVICE_FILE" | cut -d'=' -f2-)
    if [ -n "$WORK_DIR" ]; then
        if [ -d "$WORK_DIR" ]; then
            print_success "Working directory exists: $WORK_DIR"
        else
            print_error "Working directory not found: $WORK_DIR"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        fi
    fi

    echo ""
    echo "============================================"
    echo "  Verification Summary"
    echo "============================================"

    if [ "$ISSUES_FOUND" -eq 0 ]; then
        print_success "Service file is valid"
        echo ""
        echo "Your service file is correctly configured."
    else
        print_error "Found $ISSUES_FOUND issue(s) in service file"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "FIX INSTRUCTIONS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "The service file has configuration issues."
        echo "Reinstall the service to fix:"
        echo ""
        echo "  1. Uninstall: ./service.sh uninstall"
        echo "  2. Reinstall: ./setup.sh --service"
        echo ""
        echo "Or manually reinstall:"
        if [ "$SERVICE_MODE" = "system" ]; then
            echo "  sudo ./setup.sh --system-service"
        else
            echo "  ./setup.sh --service"
        fi
        echo ""
        exit 1
    fi
}

# Main command handler
COMMAND=${1:-help}

case $COMMAND in
    status)
        cmd_status
        ;;
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    reload)
        cmd_reload
        ;;
    enable)
        cmd_enable
        ;;
    disable)
        cmd_disable
        ;;
    logs)
        cmd_logs
        ;;
    logs-tail|tail)
        cmd_logs_tail
        ;;
    health|check)
        cmd_health
        ;;
    analyze|diag|diagnose)
        cmd_analyze
        ;;
    verify|check-service)
        cmd_verify
        ;;
    install)
        cmd_install
        ;;
    uninstall|remove)
        cmd_uninstall
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac
