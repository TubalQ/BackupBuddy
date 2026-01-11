#!/bin/bash
# BackupBuddy Installation Script

set -e

echo "========================================"
echo "BackupBuddy Installation"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

echo "Installing BackupBuddy..."
echo ""

# Install Python3 if not present
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    apt update
    apt install -y python3 python3-pip
fi

# Create symbolic link for easy access
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ln -sf "$INSTALL_DIR/backupbuddy.py" /usr/local/bin/backupbuddy

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "You can now run BackupBuddy by typing:"
echo "  backupbuddy"
echo ""
echo "Or directly with:"
echo "  python3 $INSTALL_DIR/backupbuddy.py"
echo ""
echo "First run will install required dependencies (rclone, pigz, tar, pv, cron)"
echo ""

