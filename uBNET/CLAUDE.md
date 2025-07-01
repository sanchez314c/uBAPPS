# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBNET** is a lightweight GTK system tray application for monitoring network upload/download bandwidth on Ubuntu/Linux. It displays network throughput in the tray with per-interface breakdown.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
./install.sh                      # Install application

# Running
ubnet &                           # Run in background

# Uninstallation
./uninstall.sh                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubnet.py` | Main GTK AppIndicator application (~16KB) |
| `install.sh` | Installation script |
| `uninstall.sh` | Removal script |
| `icons/` | Status icons |

### How It Works

1. Reads network stats from `/proc/net/dev`
2. Calculates RX/TX speed via delta between readings
3. Displays combined throughput in tray
4. Shows per-interface breakdown (eth0, wlan0, etc.)
5. Color-codes based on thresholds
6. Updates every 1 second

### Data Classes

```python
@dataclass
class InterfaceStats:
    interface: str
    rx_bytes: int        # Download total
    tx_bytes: int        # Upload total
    rx_speed: float      # bytes/sec download
    tx_speed: float      # bytes/sec upload
```

## Configuration

File: `~/.config/ubnet/config.json`

```json
{
  "warning_threshold_mb": 10.0,
  "critical_threshold_mb": 50.0,
  "update_interval_ms": 1000,
  "show_loopback": false,
  "show_virtual": false
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `warning_threshold_mb` | 10.0 | MB/s for orange warning |
| `critical_threshold_mb` | 50.0 | MB/s for red critical |
| `show_loopback` | false | Show lo interface |
| `show_virtual` | false | Show docker/veth interfaces |

## Requirements

```bash
sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1
```
