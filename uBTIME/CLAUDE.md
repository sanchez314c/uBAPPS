# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBTIME** is a lightweight GTK system tray application for viewing times across all world timezones on Ubuntu/Linux. It displays local time in the tray and provides quick access to favorite timezones with full timezone browsing by region.

**Stack**: Python 3.9+ / GTK 3.0 / AppIndicator / zoneinfo
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
make install                      # Full installation
./install.sh                      # Alternative

# Running
ubtime                            # Run application
make run                          # Run via make

# Uninstallation
make uninstall                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubtime.py` | Main GTK AppIndicator application (~14KB) |
| `install.sh` | Installation script |
| `uninstall.sh` | Removal script |
| `icons/` | Clock icon |

### How It Works

1. Uses Python's `zoneinfo` module for timezone data
2. Displays local time in system tray
3. Shows favorites at top of menu
4. Organizes all timezones by region (Africa, America, Asia, Europe, Pacific, etc.)
5. Shows UTC offset for each timezone
6. Updates every second

### Features

- Left-click timezone → copy time to clipboard
- Right-click timezone → add/remove from favorites
- Toggle 12h/24h format
- Show/hide seconds

## Configuration

File: `~/.config/ubtime/config.json`

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

## Requirements

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

Note: Python 3.9+ required for `zoneinfo` module. For older Python, install `backports.zoneinfo`.
