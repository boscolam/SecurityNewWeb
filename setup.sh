#!/bin/bash
# ============================================================
# CyberSec News Dashboard - Setup Script v2.1
# ============================================================
# Automated setup for the Cybersecurity News Dashboard
# Supports development and production configurations
#
# Usage:
#   ./setup.sh                    # Interactive setup
#   ./setup.sh --service          # Install as systemd service
#   ./setup.sh --production       # Production setup (Apache)
#   ./setup.sh --help             # Show help
# ============================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
INSTALL_PATH=$(pwd)
SERVICE_USER="www-data"
SERVICE_MODE="user"  # user or system

# Print colored message
print_msg() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Show help
show_help() {
    cat << EOF
Cybersecurity News Dashboard - Setup Script

USAGE:
    ./setup.sh [OPTIONS]

OPTIONS:
    --help              Show this help message
    --service           Install as systemd user service
    --system-service    Install as system-wide service (requires sudo)
    --production        Production setup with Apache
    --dev               Development setup (default)

EXAMPLES:
    # Basic development setup
    ./setup.sh

    # Install as user service (runs on login)
    ./setup.sh --service

    # Install as system service (runs on boot, requires sudo)
    sudo ./setup.sh --system-service

    # Production setup with Apache
    sudo ./setup.sh --production

NOTES:
    - User service: Runs under your user account
    - System service: Runs as www-data, starts on boot
    - Production: Sets up Apache with mod_wsgi

For more information, see INSTALL.md or UBUNTU_INSTALL.md
EOF
    exit 0
}

# Parse arguments
INSTALL_SERVICE=false
SYSTEM_SERVICE=false
PRODUCTION=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --service)
            INSTALL_SERVICE=true
            SERVICE_MODE="user"
            shift
            ;;
        --system-service)
            INSTALL_SERVICE=true
            SYSTEM_SERVICE=true
            SERVICE_MODE="system"
            shift
            ;;
        --production)
            PRODUCTION=true
            SYSTEM_SERVICE=true
            SERVICE_MODE="system"
            shift
            ;;
        --dev)
            # Default mode
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo ""
echo "============================================"
echo "  CyberSec News Dashboard - Setup v2.1"
echo "============================================"
echo ""

# Check if running as root (needed for system service)
if [ "$SYSTEM_SERVICE" = true ] && [ "$EUID" -ne 0 ]; then
    print_error "System service installation requires sudo/root"
    echo "Run: sudo ./setup.sh --system-service"
    exit 1
fi

# Step 1: Check Python
echo "[1/7] Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    print_error "Python 3 is required but not found"
    echo "Install: sudo apt install -y python3 python3-venv python3-pip"
    exit 1
fi

PY_VERSION=$($PYTHON --version 2>&1)
print_msg "Found: $PY_VERSION"

# Step 2: Check Git (for auto-update feature)
echo ""
echo "[2/7] Checking Git installation..."
if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version)
    print_msg "Found: $GIT_VERSION"

    # Check if in git repository
    if git rev-parse --git-dir > /dev/null 2>&1; then
        print_msg "Git repository detected - auto-update will work"
    else
        print_warning "Not a git repository - auto-update feature will not work"
        print_info "To enable: git init && git remote add origin https://github.com/boscolam/SecurityNewWeb.git"
    fi
else
    print_warning "Git not found - auto-update feature will not work"
    echo "Install: sudo apt install -y git"
fi

# Step 3: Create virtual environment
echo ""
echo "[3/7] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    print_msg "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Step 4: Install dependencies
echo ""
echo "[4/7] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
print_msg "Dependencies installed successfully"

# Step 5: Initialize database
echo ""
echo "[5/7] Initializing database..."
if [ -f "cybersec_news.db" ]; then
    print_info "Database already exists, skipping initialization"
else
    $PYTHON << EOF
from database import init_db
init_db()
print("Database initialized with 140+ RSS feeds")
EOF
    print_msg "Database created at ./cybersec_news.db"
fi

# Step 6: Set permissions
echo ""
echo "[6/7] Setting permissions..."
if [ "$SYSTEM_SERVICE" = true ]; then
    chown -R $SERVICE_USER:$SERVICE_USER "$INSTALL_PATH"
    chmod -R 755 "$INSTALL_PATH"
    chmod 600 "$INSTALL_PATH/cybersec_news.db" 2>/dev/null || true
    print_msg "Permissions set for $SERVICE_USER"
else
    chmod +x "$INSTALL_PATH/setup.sh"
    chmod 644 "$INSTALL_PATH/cybersec_news.db" 2>/dev/null || true
    print_msg "Permissions configured"
fi

# Step 7: Install service (if requested)
echo ""
echo "[7/7] Service configuration..."

if [ "$INSTALL_SERVICE" = true ]; then
    # Detect current user and group
    CURRENT_USER="${USER:-$(whoami)}"
    CURRENT_GROUP=$(id -gn)

    print_info "Detected user: $CURRENT_USER, group: $CURRENT_GROUP"
    print_info "Installation path: $INSTALL_PATH"

    if [ "$SERVICE_MODE" = "system" ]; then
        # System-wide service
        print_info "Installing system-wide service..."

        # Create service file from template with proper substitutions
        sed -e "s|__INSTALL_USER__|$CURRENT_USER|g" \
            -e "s|__INSTALL_GROUP__|$CURRENT_GROUP|g" \
            -e "s|__INSTALL_PATH__|$INSTALL_PATH|g" \
            cybersec-news.service > /tmp/cybersec-news.service

        # Copy service file
        cp /tmp/cybersec-news.service /etc/systemd/system/cybersec-news.service

        # Clean up temp file
        rm -f /tmp/cybersec-news.service

        # Reload systemd
        systemctl daemon-reload

        # Enable service
        systemctl enable cybersec-news

        # Start service
        systemctl start cybersec-news

        print_msg "System service installed and started"
        echo ""
        echo "Configuration:"
        echo "  User: $CURRENT_USER"
        echo "  Group: $CURRENT_GROUP"
        echo "  Path: $INSTALL_PATH"
        echo ""
        echo "Service management commands:"
        echo "  sudo systemctl status cybersec-news"
        echo "  sudo systemctl restart cybersec-news"
        echo "  sudo systemctl stop cybersec-news"
        echo "  sudo journalctl -u cybersec-news -f"

    else
        # User service
        print_info "Installing user service..."

        # Create user systemd directory
        mkdir -p ~/.config/systemd/user/

        # Create service file from template with proper substitutions
        sed -e "s|__INSTALL_PATH__|$INSTALL_PATH|g" \
            cybersec-news-user.service > ~/.config/systemd/user/cybersec-news.service

        # Reload systemd
        systemctl --user daemon-reload

        # Enable service
        systemctl --user enable cybersec-news

        # Start service
        systemctl --user start cybersec-news

        # Enable linger (service runs on boot)
        sudo loginctl enable-linger $USER 2>/dev/null || print_warning "Could not enable linger (service won't start on boot)"

        print_msg "User service installed and started"
        echo ""
        echo "Configuration:"
        echo "  User: $CURRENT_USER"
        echo "  Path: $INSTALL_PATH"
        echo ""
        echo "Service management commands:"
        echo "  systemctl --user status cybersec-news"
        echo "  systemctl --user restart cybersec-news"
        echo "  systemctl --user stop cybersec-news"
        echo "  journalctl --user -u cybersec-news -f"
    fi
else
    print_info "Service not installed (use --service flag to install)"
fi

# Production Apache setup
if [ "$PRODUCTION" = true ]; then
    echo ""
    print_info "Production mode - Installing Apache configuration..."

    # Check if Apache is installed
    if ! command -v apache2 &>/dev/null; then
        print_error "Apache not found. Installing..."
        apt update
        apt install -y apache2 libapache2-mod-wsgi-py3
    fi

    # Copy installation to /var/www if not already there
    if [ "$INSTALL_PATH" != "/var/www/cybersec-news" ]; then
        print_info "Copying files to /var/www/cybersec-news..."
        mkdir -p /var/www/cybersec-news
        cp -r "$INSTALL_PATH"/* /var/www/cybersec-news/
        INSTALL_PATH="/var/www/cybersec-news"
        chown -R www-data:www-data /var/www/cybersec-news
    fi

    # Create Apache config
    cat > /etc/apache2/sites-available/cybersec-news.conf << EOF
<VirtualHost *:80>
    ServerName localhost
    ServerAdmin admin@localhost

    DocumentRoot $INSTALL_PATH

    WSGIDaemonProcess cybersec_news python-home=$INSTALL_PATH/venv python-path=$INSTALL_PATH
    WSGIProcessGroup cybersec_news
    WSGIScriptAlias / $INSTALL_PATH/wsgi.py

    Alias /static $INSTALL_PATH/static
    <Directory $INSTALL_PATH/static>
        Require all granted
    </Directory>

    <Directory $INSTALL_PATH>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/cybersec-news-error.log
    CustomLog \${APACHE_LOG_DIR}/cybersec-news-access.log combined
</VirtualHost>
EOF

    # Enable site and mod_wsgi
    a2enmod wsgi
    a2ensite cybersec-news.conf
    a2dissite 000-default.conf 2>/dev/null || true

    # Restart Apache
    systemctl restart apache2

    print_msg "Apache configuration complete"
    echo ""
    echo "Access the dashboard at: http://localhost/"
fi

# Final summary
echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""

if [ "$INSTALL_SERVICE" = true ]; then
    echo "✓ Application installed as service"
    if [ "$SERVICE_MODE" = "system" ]; then
        echo "✓ Running as: system service (www-data)"
        echo "✓ Access at: http://localhost:5000"
    else
        echo "✓ Running as: user service ($USER)"
        echo "✓ Access at: http://localhost:5000"
    fi
    echo ""
    echo "The application is now running in the background."
elif [ "$PRODUCTION" = true ]; then
    echo "✓ Production installation complete"
    echo "✓ Running with Apache on port 80"
    echo "✓ Access at: http://localhost/"
else
    echo "To start the application:"
    echo "  source venv/bin/activate"
    echo "  python app.py"
    echo ""
    echo "Then open: http://localhost:5000"
    echo ""
    echo "To install as a service:"
    echo "  ./setup.sh --service           # User service"
    echo "  sudo ./setup.sh --system-service  # System service"
fi

echo ""
echo "Documentation:"
echo "  README.md           - Features and overview"
echo "  UBUNTU_INSTALL.md   - Installation guide"
echo "  AUTO_UPDATE_GUIDE.md - Auto-update feature"
echo "============================================"
echo ""
