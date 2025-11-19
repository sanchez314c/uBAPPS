#!/bin/bash
# uBRES Installer Script

set -e

APP_NAME="uBRES"
INSTALL_DIR="$HOME/.local/share/ubres"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing $APP_NAME..."

# Install system dependencies
echo "Checking dependencies..."

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

if ! command -v xrandr &> /dev/null; then
    echo "Installing xrandr..."
    sudo apt install -y x11-xserver-utils
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$AUTOSTART_DIR"

# Copy application
echo "Installing application files..."
cp ubres.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/ubres.py"

# Create launcher script
cat > "$BIN_DIR/ubres" << 'EOF'
#!/bin/bash
exec /usr/bin/python3 "$HOME/.local/share/ubres/ubres.py" "$@"
EOF
chmod +x "$BIN_DIR/ubres"

# Create desktop entry
cat > "$DESKTOP_DIR/ubres.desktop" << EOF
[Desktop Entry]
Name=uBRES
Comment=Quick display resolution switcher
Exec=$BIN_DIR/ubres
Icon=video-display
Terminal=false
Type=Application
Categories=Settings;HardwareSettings;
Keywords=resolution;display;monitor;screen;
EOF

# Create autostart entry
cat > "$AUTOSTART_DIR/ubres.desktop" << EOF
[Desktop Entry]
Name=uBRES
Comment=Quick display resolution switcher
Exec=$BIN_DIR/ubres
Icon=video-display
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "NOTE: Add ~/.local/bin to your PATH by adding this to ~/.bashrc:"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo ""
fi

echo ""
echo "========================================="
echo "$APP_NAME installed successfully!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Run 'ubres' from terminal"
echo "  2. Find 'uBRES' in your applications menu"
echo "  3. It will auto-start on login"
echo ""
echo "To disable auto-start, remove:"
echo "  $AUTOSTART_DIR/ubres.desktop"
echo ""
