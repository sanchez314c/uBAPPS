#!/bin/bash
# uBTIME Installer Script

set -e

APP_NAME="uBTIME"
INSTALL_DIR="$HOME/.local/share/ubtime"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing $APP_NAME..."

# Check for AppIndicator (either Ayatana or regular)
if ! dpkg -s gir1.2-ayatanaappindicator3-0.1 &> /dev/null && ! dpkg -s gir1.2-appindicator3-0.1 &> /dev/null; then
    echo "Installing Ayatana AppIndicator3..."
    sudo apt update
    sudo apt install -y gir1.2-ayatanaappindicator3-0.1
fi

if ! dpkg -s python3-gi &> /dev/null; then
    echo "Installing Python GTK bindings..."
    sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/icons"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$AUTOSTART_DIR"

# Copy application
echo "Installing application files..."
cp ubtime.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/ubtime.py"

# Copy icons
if [ -d "icons" ]; then
    echo "Installing icons..."
    cp icons/*.svg "$INSTALL_DIR/icons/"
fi

# Create launcher script
cat > "$BIN_DIR/ubtime" << 'EOF'
#!/bin/bash
exec /usr/bin/python3 "$HOME/.local/share/ubtime/ubtime.py" "$@"
EOF
chmod +x "$BIN_DIR/ubtime"

# Create desktop entry
cat > "$DESKTOP_DIR/ubtime.desktop" << EOF
[Desktop Entry]
Name=uBTIME
Comment=World clock - view times across all timezones
Exec=$BIN_DIR/ubtime
Icon=$INSTALL_DIR/icons/clock.svg
Terminal=false
Type=Application
Categories=Utility;Clock;
Keywords=time;clock;timezone;world;
EOF

# Create autostart entry
cat > "$AUTOSTART_DIR/ubtime.desktop" << EOF
[Desktop Entry]
Name=uBTIME
Comment=World clock - view times across all timezones
Exec=$BIN_DIR/ubtime
Icon=$INSTALL_DIR/icons/clock.svg
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "NOTE: Add ~/.local/bin to your PATH by adding this to ~/.bashrc:"
    # shellcheck disable=SC2016  # Intentional: literal shell snippet for user to copy
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo ""
fi

echo ""
echo "========================================="
echo "$APP_NAME installed successfully!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Run 'ubtime' from terminal"
echo "  2. Find 'uBTIME' in your applications menu"
echo "  3. It will auto-start on login"
echo ""
echo "Tips:"
echo "  - Left-click a timezone to copy its time"
echo "  - Right-click a timezone to add/remove from favorites"
echo "  - Click time format to switch between 12h/24h"
echo ""
