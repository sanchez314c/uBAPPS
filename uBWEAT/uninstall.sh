#!/bin/bash
# uBWEAT Uninstaller Script

set -e

APP_NAME="uBWEAT"
INSTALL_DIR="$HOME/.local/share/ubweat"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
CONFIG_DIR="$HOME/.config/ubweat"

echo "Uninstalling $APP_NAME..."

# Kill running instance
pkill -f "ubweat.py" 2>/dev/null || true

# Remove files
rm -f "$BIN_DIR/ubweat"
rm -f "$DESKTOP_DIR/ubweat.desktop"
rm -f "$AUTOSTART_DIR/ubweat.desktop"
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
