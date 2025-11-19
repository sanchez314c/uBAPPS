#!/bin/bash
# uBTEMP Installer Script

set -e

APP_NAME="uBTEMP"
INSTALL_DIR="$HOME/.local/share/ubtemp"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing $APP_NAME..."

# Install system dependencies
echo "Checking dependencies..."

# Check for lm-sensors
if ! command -v sensors &> /dev/null; then
    echo "Installing lm-sensors..."
    sudo apt update
    sudo apt install -y lm-sensors
    echo ""
    echo "Running sensors-detect to configure sensors..."
    echo "Accept the defaults (press Enter) for each question."
    sudo sensors-detect --auto
fi

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
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$AUTOSTART_DIR"

# Copy application
echo "Installing application files..."
cp ubtemp.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/ubtemp.py"

# Copy icons
if [ -d "icons" ]; then
    echo "Installing icons..."
    mkdir -p "$INSTALL_DIR/icons"
    cp icons/*.svg "$INSTALL_DIR/icons/"
fi

# Create launcher script
cat > "$BIN_DIR/ubtemp" << 'EOF'
#!/bin/bash
exec /usr/bin/python3 "$HOME/.local/share/ubtemp/ubtemp.py" "$@"
EOF
chmod +x "$BIN_DIR/ubtemp"

# Create desktop entry
cat > "$DESKTOP_DIR/ubtemp.desktop" << EOF
[Desktop Entry]
Name=uBTEMP
Comment=Hardware temperature monitor
Exec=$BIN_DIR/ubtemp
Icon=$INSTALL_DIR/icons/temp-normal.svg
Terminal=false
Type=Application
Categories=System;Monitor;
Keywords=temperature;sensor;monitor;cpu;gpu;
EOF

# Create autostart entry
cat > "$AUTOSTART_DIR/ubtemp.desktop" << EOF
[Desktop Entry]
Name=uBTEMP
Comment=Hardware temperature monitor
Exec=$BIN_DIR/ubtemp
Icon=$INSTALL_DIR/icons/temp-normal.svg
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
echo "  1. Run 'ubtemp' from terminal"
echo "  2. Find 'uBTEMP' in your applications menu"
echo "  3. It will auto-start on login"
echo ""
echo "Tips:"
echo "  - Right-click any sensor to rename it"
echo "  - Click 'Switch to °F/°C' to change units"
echo "  - Settings are saved in ~/.config/ubtemp/"
echo ""
echo "To disable auto-start, remove:"
echo "  $AUTOSTART_DIR/ubtemp.desktop"
echo ""
