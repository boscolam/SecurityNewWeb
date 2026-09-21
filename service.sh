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
    install     Install systemd service
    uninstall   Remove systemd service

EXAMPLES:
    ./service.sh status
    ./service.sh restart
    ./service.sh logs

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
