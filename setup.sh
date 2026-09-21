#!/bin/bash
# ============================================================
# CyberSec News Dashboard - Quick Setup Script
# ============================================================
# This script automates the initial setup of the application.
# Run it once after cloning/extracting the project files.
#
# Usage: chmod +x setup.sh && ./setup.sh
# ============================================================

set -e

echo "============================================"
echo "  CyberSec News Dashboard - Setup"
echo "============================================"
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "ERROR: Python 3 is required but not found."
    echo "Please install Python 3.8 or later."
    exit 1
fi

PY_VERSION=$($PYTHON --version 2>&1)
echo "  Found: $PY_VERSION"

# Create virtual environment
echo ""
echo "[2/5] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    echo "  Virtual environment created at ./venv"
else
    echo "  Virtual environment already exists."
fi

# Activate virtual environment and install dependencies
echo ""
echo "[3/5] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "  Dependencies installed successfully."

# Initialize the database
echo ""
echo "[4/5] Initializing the database..."
$PYTHON -c "from database import init_db; init_db()"
echo "  Database initialized at ./cybersec_news.db"

# Create necessary directories
echo ""
echo "[5/5] Setting up directory structure..."
mkdir -p static/css static/js templates
echo "  Directory structure verified."

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "To start the application:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
echo "For Apache deployment, see INSTALL.md"
echo "============================================"
