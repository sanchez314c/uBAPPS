#!/bin/bash
# uBTEMP Uninstaller Script

set -e

APP_NAME="uBTEMP"
INSTALL_DIR="$HOME/.local/share/ubtemp"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
CONFIG_DIR="$HOME/.config/ubtemp"

echo "Uninstalling $APP_NAME..."

# Remove files
rm -f "$BIN_DIR/ubtemp"
rm -f "$DESKTOP_DIR/ubtemp.desktop"
rm -f "$AUTOSTART_DIR/ubtemp.desktop"
rm -rf "$INSTALL_DIR"

# Ask about config
read -p "Remove configuration files? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$CONFIG_DIR"
    echo "Configuration removed."
else
    echo "Configuration kept at: $CONFIG_DIR"
fi

echo "$APP_NAME has been uninstalled."
