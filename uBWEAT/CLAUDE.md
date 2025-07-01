# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBWEAT** is a lightweight GTK system tray application for displaying local weather and temperature on Ubuntu/Linux. It uses the free wttr.in service (no API key required) with auto-location detection via IP geolocation.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator / wttr.in API
**Platform**: Ubuntu/Linux

## Commands

```bash
# Installation
make install                      # Full installation
./install.sh                      # Alternative

# Running
ubweat                            # Run application
make run                          # Run via make

# Uninstallation
make uninstall                    # Remove application
```

## Architecture

| File | Purpose |
|------|---------|
| `ubweat.py` | Main GTK AppIndicator application (~17KB) |
| `install.sh` | Installation script |
| `uninstall.sh` | Removal script |
| `icons/` | Weather condition icons (sunny, cloudy, rain, etc.) |

### How It Works

1. Fetches weather data from wttr.in (free, no API key)
2. Auto-detects location by IP (or uses manual setting)
3. Displays temperature + condition icon in tray
4. Shows detailed weather info in dropdown:
   - Temperature / feels like
   - Condition
   - Humidity, wind, pressure, UV index
5. Updates every 10 minutes

### Weather Icons

- `weather-sunny.svg`
- `weather-cloudy.svg`
- `weather-rain.svg`
- `weather-snow.svg`
- `weather-fog.svg`
- `weather-storm.svg`

## Configuration

File: `~/.config/ubweat/config.json`

```json
{
  "use_fahrenheit": false,
  "location": "",
  "refresh_minutes": 10,
  "show_condition": true
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `use_fahrenheit` | false | true = °F, false = °C |
| `location` | "" | City name (empty = auto-detect) |
| `refresh_minutes` | 10 | Update interval |
| `show_condition` | true | Show weather text in tray |

## Requirements

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

Internet connection required for weather data.
