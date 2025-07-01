# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBCPU** is a lightweight GTK system tray application for monitoring CPU usage on Ubuntu/Linux. It displays total CPU percentage in the tray with color-coded status and per-core breakdown in the dropdown menu.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
./install.sh                      # Install application

# Running
ubcpu &                           # Run in background
killall ubcpu                     # Stop application

# Uninstallation
./uninstall.sh                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubcpu.py` | Main GTK AppIndicator application (~15KB) |
| `install.sh` | Installation with autostart setup |
| `uninstall.sh` | Clean removal |
| `icons/` | Status icons (normal/warning/critical) |

### How It Works

1. Reads CPU stats from `/proc/stat`
2. Calculates usage via delta method (comparing consecutive readings)
3. Displays total CPU % in tray (color-coded)
4. Shows per-core breakdown in dropdown menu
5. Updates every 1 second (configurable)
6. Sends notifications on critical threshold

### CPU Calculation

```
usage = (total_delta - idle_delta) / total_delta * 100
```

Accounts for: user, system, nice, iowait, irq, softirq, steal time

## Configuration

File: `~/.config/ubcpu/config.json`

```json
{
  "warning_threshold": 70.0,
  "critical_threshold": 90.0,
  "show_notifications": true,
  "update_interval_ms": 1000
}
```

## Requirements

```bash
sudo apt install python3 python3-gi gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```
