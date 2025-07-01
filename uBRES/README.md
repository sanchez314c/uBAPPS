# uBRES - Ubuntu Resolution Switcher

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)]()
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)]()

A lightweight system tray application for quickly changing display resolution on Ubuntu/Linux.

Inspired by [RDM (Retina Display Menu)](https://github.com/avibrazil/RDM) for macOS.

---

## Features

- **System tray integration** - Lives in your panel for quick access
- **Multi-monitor support** - Handles all connected displays
- **One-click resolution switching** - Select any available resolution from the menu
- **Auto-refresh** - Automatically detects display changes every 5 seconds
- **Shows current resolution** - Marked with a checkmark (✓)
- **Aspect ratio display** - Shows aspect ratio for each resolution (16:9, 16:10, 4:3, etc.)
- **Refresh rate info** - Displays refresh rate for each resolution
- **Desktop notifications** - Confirms resolution changes
- **Auto-start on login** - Optional autostart support
- **Lightweight** - Single Python file, minimal dependencies

## Screenshots

The application appears as a display icon in your system tray. Clicking it shows a menu with:

```
── DP-0 (Primary) ──
✓ 3840 × 2160  @60Hz  [16:9]
  2560 × 1440  @60Hz  [16:9]
  1920 × 1080  @60Hz  [16:9]
  1680 × 1050  @60Hz  [16:10]
  1280 × 720   @60Hz  [16:9]
────────────────────────────
── DP-1 ──
  1920 × 1080  @60Hz  [16:9]
  1280 × 720   @60Hz  [16:9]
────────────────────────────
↻ Refresh Displays
────────────────────────────
About uBRES
Quit
```

## Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu/Linux | 18.04+ |
| Python | 3.6+ |
| GTK | 3.0 |
| AppIndicator | Ayatana or legacy |
| xrandr | Any |

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/uBRES.git
cd uBRES
make install
```

Or without make:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. Install required system packages (if needed)
2. Copy the application to `~/.local/share/ubres/`
3. Create a launcher in `~/.local/bin/ubres`
4. Add a desktop entry to your applications menu
5. Enable auto-start on login

### Manual Install

1. Install dependencies:
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 x11-xserver-utils
```

2. Run directly:
```bash
/usr/bin/python3 ubres.py
```

## Usage

| Action | Result |
|--------|--------|
| Click tray icon | Opens resolution menu |
| Select a resolution | Switches to that resolution |
| ✓ marked item | Current resolution (greyed out) |
| ↻ Refresh Displays | Manually detect monitor changes |

### Command Line

```bash
# Run directly
ubres

# Or with make
make run
```

## Uninstallation

```bash
make uninstall
```

Or:

```bash
./uninstall.sh
```

## Project Structure

```
uBRES/
├── ubres.py          # Main application
├── install.sh        # Installation script
├── uninstall.sh      # Uninstallation script
├── Makefile          # Build automation
├── README.md         # This file
├── LICENSE           # MIT License
├── CHANGELOG.md      # Version history
├── CONTRIBUTING.md   # Contribution guidelines
├── requirements.txt  # Dependencies documentation
└── screenshots/      # Application screenshots
```

## How It Works

uBRES uses `xrandr` to:
1. Query connected displays and available resolutions
2. Detect the current resolution for each display
3. Apply resolution changes when selected

The application runs as a GTK AppIndicator in the system tray, providing a simple dropdown menu interface.

## Troubleshooting

### Tray icon not showing

On some GNOME Shell versions, you may need the AppIndicator extension:

```bash
sudo apt install gnome-shell-extension-appindicator
```

Then enable it in GNOME Extensions or Tweaks, and log out/in.

### Resolution not available

The resolutions shown are those reported by your display via EDID. If a resolution is missing:
- It may not be supported by your monitor
- Your GPU driver may not support it
- You may need to add a custom modeline

### Changes don't persist after reboot

xrandr changes are temporary by default. To make them permanent:
1. Use `xrandr` commands in your `~/.profile` or `~/.xprofile`
2. Create a custom xorg.conf
3. Use your desktop environment's display settings

### Python/gi module not found

If using conda/pyenv, the system GTK bindings may not be available. Run with system Python:

```bash
/usr/bin/python3 ubres.py
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Inspired by [RDM](https://github.com/avibrazil/RDM) by Avi Alkalay
- Built with [GTK 3](https://www.gtk.org/) and [Python](https://www.python.org/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
