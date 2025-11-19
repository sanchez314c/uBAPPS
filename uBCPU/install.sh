#!/bin/bash
# uBCPU Installation Script
# Installs uBCPU - Ubuntu CPU Monitor

set -e

APP_NAME="uBCPU"
APP_ID="ubcpu"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directories
BIN_DIR="$HOME/.local/bin"
ICONS_DIR="$HOME/.local/share/$APP_ID/icons"
CONFIG_DIR="$HOME/.config/$APP_ID"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing $APP_NAME..."

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$ICONS_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$AUTOSTART_DIR"

# Copy main script
cp "$SCRIPT_DIR/ubcpu.py" "$BIN_DIR/ubcpu"
chmod +x "$BIN_DIR/ubcpu"

# Copy icons
if [ -d "$SCRIPT_DIR/icons" ]; then
    cp -r "$SCRIPT_DIR/icons/"* "$ICONS_DIR/" 2>/dev/null || true
fi

# Create default config if not exists
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "warning_threshold": 70.0,
  "critical_threshold": 90.0,
  "show_notifications": true,
  "update_interval_ms": 1000
}
EOF
fi

# Create autostart entry
cat > "$AUTOSTART_DIR/$APP_ID.desktop" << EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Comment=Ubuntu CPU Monitor
Exec=$BIN_DIR/ubcpu
Icon=cpu
Terminal=false
Categories=System;Monitor;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

# Create .desktop file for application menu
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
cat > "$APPS_DIR/$APP_ID.desktop" << EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Comment=Ubuntu CPU Monitor - System tray CPU usage monitor
Exec=$BIN_DIR/ubcpu
Icon=cpu
Terminal=false
Categories=System;Monitor;Utility;
Keywords=cpu;processor;usage;monitor;system;
EOF

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "NOTE: Add $BIN_DIR to your PATH by adding this to ~/.bashrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "=========================================="
echo "$APP_NAME installed successfully!"
echo "=========================================="
echo ""
echo "To start now:  ubcpu &"
echo "To stop:       killall ubcpu"
echo ""
echo "The app will auto-start on next login."
echo "Config file: $CONFIG_DIR/config.json"
echo ""
