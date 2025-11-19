#!/bin/bash
# uBWEAT Installer Script

set -e

APP_NAME="uBWEAT"
INSTALL_DIR="$HOME/.local/share/ubweat"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing $APP_NAME..."

# Check for AppIndicator
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
cp ubweat.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/ubweat.py"

# Copy icons
if [ -d "icons" ]; then
    echo "Installing icons..."
    cp icons/*.svg "$INSTALL_DIR/icons/"
fi

# Create launcher script
cat > "$BIN_DIR/ubweat" << 'EOF'
#!/bin/bash
exec /usr/bin/python3 "$HOME/.local/share/ubweat/ubweat.py" "$@"
EOF
chmod +x "$BIN_DIR/ubweat"

# Create desktop entry
cat > "$DESKTOP_DIR/ubweat.desktop" << EOF
[Desktop Entry]
Name=uBWEAT
Comment=Weather monitor - local temperature and conditions
Exec=$BIN_DIR/ubweat
Icon=$INSTALL_DIR/icons/weather-sunny.svg
Terminal=false
Type=Application
Categories=Utility;
Keywords=weather;temperature;forecast;
EOF

# Create autostart entry
cat > "$AUTOSTART_DIR/ubweat.desktop" << EOF
[Desktop Entry]
Name=uBWEAT
Comment=Weather monitor - local temperature and conditions
Exec=$BIN_DIR/ubweat
Icon=$INSTALL_DIR/icons/weather-sunny.svg
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF

echo ""
echo "========================================="
echo "$APP_NAME installed successfully!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Run 'ubweat' from terminal"
echo "  2. Find 'uBWEAT' in your applications menu"
echo "  3. It will auto-start on login"
echo ""
echo "Tips:"
echo "  - Click the menu to see weather details"
echo "  - Use 'Set Location' for a specific city"
echo "  - Toggle between °C and °F"
echo ""
