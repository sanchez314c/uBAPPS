#!/bin/bash
# uBTIME Uninstaller Script

set -e

APP_NAME="uBTIME"
INSTALL_DIR="$HOME/.local/share/ubtime"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
CONFIG_DIR="$HOME/.config/ubtime"

echo "Uninstalling $APP_NAME..."

# Kill running instance
pkill -f "ubtime.py" 2>/dev/null || true

# Remove files
rm -f "$BIN_DIR/ubtime"
rm -f "$DESKTOP_DIR/ubtime.desktop"
rm -f "$AUTOSTART_DIR/ubtime.desktop"
rm -rf "$INSTALL_DIR"

# Ask about config
if [ -d "$CONFIG_DIR" ]; then
    read -p "Remove configuration files? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$CONFIG_DIR"
        echo "Configuration removed."
    else
        echo "Configuration kept at $CONFIG_DIR"
    fi
fi

echo ""
echo "$APP_NAME has been uninstalled."
