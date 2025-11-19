# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBTEMP** is a lightweight GTK system tray application for monitoring hardware temperatures on Ubuntu/Linux. It displays the highest temperature in the tray and shows all sensors organized by type (CPU, GPU, NVMe, etc.) in the dropdown menu.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator / lm-sensors
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
make install                      # Full installation
./install.sh                      # Alternative

# Running
ubtemp                            # Run application
make run                          # Run via make
make sensors                      # View raw sensor data

# Uninstallation
make uninstall                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubtemp.py` | Main GTK AppIndicator application (~22KB) |
| `install.sh` | Installation with lm-sensors setup |
| `uninstall.sh` | Removal script |
| `icons/` | Status icons (normal/warning/critical SVGs) |

### How It Works

1. Reads temperature sensors directly from `/sys/class/hwmon/` (hwmon sysfs)
2. Queries NVIDIA GPU temps via `nvidia-smi` subprocess
3. Queries Areca RAID controller temps via `cli64` subprocess (cached, 15s interval)
4. Reads thermal zone data from `/sys/class/thermal/`
5. Classifies sensors by type (CPU, GPU, NVMe, HDD, RAID, etc.)
6. Displays highest temp in tray (color-coded)
7. Shows organized sensor list in dropdown
8. Supports custom sensor naming (right-click to rename)
9. Updates every 1 second

### Temperature Thresholds

| Temperature | Color | Status |
|-------------|-------|--------|
| < 70°C | Green | Normal |
| 70-85°C | Orange | Warning |
| > 85°C | Red | Critical (+ notification) |

## Configuration

File: `~/.config/ubtemp/config.json`

```json
{
  "use_fahrenheit": false,
  "custom_names": {
    "coretemp-isa-0000::Core 0": "CPU Core 1",
    "nvme-pci-0100::Composite": "Main SSD"
  },
  "warning_threshold": 70.0,
  "critical_threshold": 85.0,
  "show_notifications": true
}
```

## Requirements

```bash
sudo apt install lm-sensors python3-gi gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1
sudo sensors-detect  # Configure sensors
```
