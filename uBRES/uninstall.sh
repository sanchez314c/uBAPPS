#!/bin/bash
# uBRES Uninstaller Script

set -e

APP_NAME="uBRES"
INSTALL_DIR="$HOME/.local/share/ubres"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Uninstalling $APP_NAME..."

# Kill running instances
pkill -f "ubres.py" 2>/dev/null || true

# Remove files
rm -f "$BIN_DIR/ubres"
rm -f "$DESKTOP_DIR/ubres.desktop"
rm -f "$AUTOSTART_DIR/ubres.desktop"
rm -rf "$INSTALL_DIR"

echo "$APP_NAME has been uninstalled."
