# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBDISK** is a lightweight GTK system tray application for monitoring disk I/O bandwidth on Ubuntu/Linux. It displays read/write speeds in the tray with color-coded status based on activity levels.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
./install.sh                      # Install application

# Running
ubdisk &                          # Run in background

# Uninstallation
./uninstall.sh                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubdisk.py` | Main GTK AppIndicator application (~14KB) |
| `install.sh` | Installation script |
| `uninstall.sh` | Removal script |
| `icons/` | Status icons |

### How It Works

1. Reads disk stats from `/proc/diskstats`
2. Calculates read/write speed via delta between readings
3. Displays combined I/O speed in tray
4. Shows per-disk breakdown in dropdown menu
5. Color-codes based on thresholds (normal/warning/critical)
6. Updates every 1 second

### Data Classes

```python
@dataclass
class DiskStats:
    device: str
    read_bytes: int
    write_bytes: int
    read_speed: float   # bytes/sec
    write_speed: float  # bytes/sec
```

## Configuration

File: `~/.config/ubdisk/config.json`

```json
{
  "warning_threshold_mb": 50.0,
  "critical_threshold_mb": 100.0,
  "update_interval_ms": 1000,
  "show_all_disks": false
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `warning_threshold_mb` | 50.0 | MB/s for orange warning |
| `critical_threshold_mb` | 100.0 | MB/s for red critical |
| `show_all_disks` | false | Include virtual disks |

## Requirements

```bash
sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1
```
