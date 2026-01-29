# Implementation Notes - uB Suite (uBAPPS)

## Project Overview

A collection of 7 lightweight system tray utilities for Ubuntu/Linux. Each app is standalone, uses GTK3 AppIndicator, and follows a consistent design pattern.

## Completed Apps

1. **uBCPU** - CPU usage monitor (reads /proc/stat)
2. **uBDISK** - Disk I/O bandwidth monitor (reads /proc/diskstats)
3. **uBNET** - Network bandwidth monitor (reads /proc/net/dev)
4. **uBRES** - Display resolution switcher (uses xrandr)
5. **uBTEMP** - Hardware temperature monitor (hwmon sysfs, nvidia-smi, cli64)
6. **uBTIME** - World clock and timezones (Python zoneinfo)
7. **uBWEAT** - Weather display (wttr.in API)

## Planned Apps (from dev/uB_APP_IDEAS.md)

- uBMEM - Memory usage monitor
- uBBAT - Battery status indicator
- uBPROC - Process monitor
- uBCLIP - Clipboard manager
- uBNOTE - Quick notes
- uBCALC - Quick calculator
- uBCOLOR - Color picker
- uBSCREEN - Screenshot tool
- uBBLUE - Bluetooth manager
- uBVPN - VPN manager
- uBWIFI - WiFi manager
- uBBRIGHT - Brightness control
- uBVOL - Volume control

## Build Instructions

Each app is a single Python file with no pip dependencies. System packages required:

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

Run from source: `./run-source-linux.sh <appname>`
Install individual app: `cd uB<NAME> && ./install.sh`

## Technical Decisions

- No shared code between apps (standalone design)
- Two install patterns exist (direct copy vs. wrapper script) - documented in AUDIT_REPORT.md
- Python 3.6+ minimum, 3.9+ required for uBTIME (zoneinfo module)
- Uses system Python, not conda/pyenv
