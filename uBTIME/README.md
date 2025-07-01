# uBTIME - Ubuntu World Clock

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9%2B-green.svg)]()
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)]()

A lightweight system tray application for viewing times across all world timezones on Ubuntu/Linux.

---

## Features

- **All timezones** - Every timezone with city/location identifier
- **System tray integration** - Lives in your panel showing local time
- **Organized by region** - Africa, America, Asia, Europe, Pacific, etc.
- **Favorites** - Quick access to your most-used timezones
- **12h/24h format** - Toggle between time formats
- **Show/hide seconds** - Customize time display
- **Copy to clipboard** - Left-click to copy timezone time
- **UTC offsets** - Shows offset from UTC for each timezone
- **Real-time updates** - Time updates every second
- **Persistent settings** - Saves favorites and preferences

## Screenshots

The application appears in your system tray showing local time. Clicking it shows:

```
Local: 14:32:45
────────────────────────────
── Favorites ──
  New York      UTC-05:00  09:32:45
  Los Angeles   UTC-08:00  06:32:45
  London        UTC+00:00  14:32:45
  Paris         UTC+01:00  15:32:45
  Tokyo         UTC+09:00  23:32:45
────────────────────────────
All Timezones  >
────────────────────────────
Switch to 12h format
Hide seconds
────────────────────────────
About uBTIME
Quit
```

## Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu/Linux | 20.04+ |
| Python | 3.9+ (for zoneinfo) |
| GTK | 3.0 |
| AppIndicator | Ayatana or legacy |

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/uBTIME.git
cd uBTIME
make install
```

Or without make:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. Install required Python/GTK packages
2. Copy the application to `~/.local/share/ubtime/`
3. Create launcher and desktop entries
4. Enable auto-start on login

### Manual Install

1. Install dependencies:
```bash
sudo apt install python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

2. Run directly:
```bash
/usr/bin/python3 ubtime.py
```

## Usage

### Basic Usage

| Action | Result |
|--------|--------|
| Click tray icon | Opens timezone menu |
| Left-click timezone | Copy time to clipboard |
| Right-click timezone | Add/remove from favorites |
| Click time format | Toggle 12h / 24h |
| Click seconds option | Show/hide seconds |

### Favorites

Your favorite timezones appear at the top of the menu for quick access. Default favorites:
- New York
- Los Angeles
- London
- Paris
- Tokyo
- Shanghai
- Sydney
- UTC

Right-click any timezone to add or remove it from favorites.

### All Timezones

Expand "All Timezones" to see every timezone organized by region:
- Africa
- America
- Antarctica
- Arctic
- Asia
- Atlantic
- Australia
- Europe
- Indian
- Pacific

### Command Line

```bash
# Run directly
ubtime

# Or with make
make run
```

## Configuration

Settings are stored in `~/.config/ubtime/config.json`:

```json
{
  "use_24h": true,
  "show_seconds": true,
  "favorites": [
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Australia/Sydney",
    "UTC"
  ]
}
```

## Uninstallation

```bash
make uninstall
```

Or:

```bash
./uninstall.sh
```

You'll be asked whether to keep or remove configuration files.

## Project Structure

```
uBTIME/
├── ubtime.py          # Main application
├── icons/             # Application icons
│   └── clock.svg      # Tray icon
├── install.sh         # Installation script
├── uninstall.sh       # Uninstallation script
├── Makefile           # Build automation
├── README.md          # This file
├── LICENSE            # MIT License
├── CHANGELOG.md       # Version history
├── CONTRIBUTING.md    # Contribution guidelines
├── requirements.txt   # Dependencies documentation
└── screenshots/       # Application screenshots
```

## How It Works

uBTIME uses Python's `zoneinfo` module (Python 3.9+) to:
1. Get all available system timezones
2. Calculate current time for each timezone
3. Display organized by region with UTC offsets
4. Update every second

The application runs as a GTK AppIndicator in the system tray.

## Troubleshooting

### Tray icon not showing

Install the AppIndicator GNOME extension:
```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable it in GNOME Extensions, then log out/in.

### Python/gi module not found

Use system Python instead of conda/pyenv:
```bash
/usr/bin/python3 ubtime.py
```

### zoneinfo not available

Python 3.9+ is required. On older systems:
```bash
pip install backports.zoneinfo
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Related Projects

- [GNOME Clocks](https://wiki.gnome.org/Apps/Clocks) - GNOME clock application
- [uBRES](https://github.com/yourusername/uBRES) - Ubuntu resolution switcher
- [uBTEMP](https://github.com/yourusername/uBTEMP) - Ubuntu temperature monitor
