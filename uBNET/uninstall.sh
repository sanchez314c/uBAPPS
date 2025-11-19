#!/bin/bash
# uBNET Uninstallation Script

set -e

APP_NAME="uBNET"
APP_ID="ubnet"

echo "Uninstalling $APP_NAME..."

# Kill running instances
killall ubnet 2>/dev/null || true

# Remove files
rm -f "$HOME/.local/bin/ubnet"
rm -f "$HOME/.config/autostart/$APP_ID.desktop"
rm -f "$HOME/.local/share/applications/$APP_ID.desktop"
rm -rf "$HOME/.local/share/$APP_ID"

# Ask about config
read -p "Remove configuration? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.config/$APP_ID"
    echo "Configuration removed."
else
    echo "Configuration preserved at ~/.config/$APP_ID/"
fi

echo ""
echo "$APP_NAME uninstalled."
