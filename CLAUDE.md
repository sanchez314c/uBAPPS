# CLAUDE.md

## Project Overview

**uB Suite (uBAPPS)** is a collection of 7 lightweight system tray utilities for Ubuntu/Linux. Each app is standalone, uses GTK3 AppIndicator, and follows a consistent design pattern.

**Stack**: Python 3.6+, GTK3, AppIndicator (Ayatana), systemd (for procfs/sysfs)

## Apps

| App | Purpose | Data Source |
|-----|---------|-------------|
| uBCPU | CPU usage monitor | `/proc/stat` |
| uBDISK | Disk I/O monitor | `/proc/diskstats` |
| uBNET | Network bandwidth | `/proc/net/dev` |
| uBRES | Resolution switcher | `xrandr` |
| uBTEMP | Temperature monitor | `lm-sensors` |
| uBTIME | World clock | `zoneinfo` |
| uBWEAT | Weather display | `wttr.in` API |

## Structure

Each app follows the same pattern:
```
uB<NAME>/
├── uB<NAME>.py      # Main Python script
├── install.sh        # Installer (copies to ~/.local, creates autostart)
├── icons/            # Tray icons
├── CLAUDE.md         # Per-app AI context
└── LICENSE           # MIT
```

## Common Pattern

All apps use:
1. `Gtk.main()` event loop
2. `AppIndicator3` for system tray icon
3. `GLib.timeout_add_seconds()` for polling interval
4. Menu with status display and Quit option

## Commands

```bash
# Install any app
cd uB<NAME>
./install.sh

# Run from source
python3 uB<NAME>/uB<NAME>.py
```

## Gotchas

- GNOME Shell requires `gnome-shell-extension-appindicator` for tray icons
- AppIndicator must be Ayatana variant on modern Ubuntu
- uBWEAT is the only app that makes network requests
- Each app installs independently, no shared dependencies between apps
