# uBWEAT - Ubuntu Weather Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)]()
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)]()

A lightweight system tray application for displaying local weather and temperature on Ubuntu/Linux.

---

## Features

- **Local temperature** - Displays current temperature in system tray
- **Auto-detect location** - Uses IP geolocation by default
- **Custom location** - Set any city manually
- **Weather conditions** - Shows current weather (sunny, cloudy, rain, etc.)
- **Dynamic icons** - Icon changes based on weather conditions
- **Celsius/Fahrenheit** - Toggle between temperature units
- **Detailed info** - Humidity, wind, pressure, UV index
- **Auto-refresh** - Updates every 10 minutes
- **No API key required** - Uses free wttr.in service

## Screenshots

The application appears in your system tray showing current temperature:

```
☀️ 72°F
────────────────────────────
Los Angeles, United States
────────────────────────────
Temperature: 72°F
Feels like: 70°F
Condition: Sunny
────────────────────────────
Humidity: 45%
Wind: W 8 mph
Pressure: 1015 mb
UV Index: 6
────────────────────────────
Updated: 02:30 PM
────────────────────────────
↻ Refresh Now
Switch to °C
Set Location...
────────────────────────────
About uBWEAT
Quit
```

## Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu/Linux | 18.04+ |
| Python | 3.6+ |
| GTK | 3.0 |
| AppIndicator | Ayatana or legacy |
| Internet | Required for weather data |

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/uBWEAT.git
cd uBWEAT
make install
```

Or without make:

```bash
chmod +x install.sh
./install.sh
```

### Manual Install

1. Install dependencies:
```bash
sudo apt install python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

2. Run directly:
```bash
/usr/bin/python3 ubweat.py
```

## Usage

### Basic Usage

| Action | Result |
|--------|--------|
| Click tray icon | Opens weather details menu |
| ↻ Refresh Now | Fetch latest weather |
| Switch to °C/°F | Toggle temperature units |
| Set Location | Enter custom city |

### Setting Location

1. Click the tray icon
2. Select "Set Location..."
3. Enter city name (e.g., "New York", "London", "Tokyo")
4. Click OK

Leave empty to auto-detect location by IP.

### Command Line

```bash
# Run directly
ubweat

# Or with make
make run
```

## Configuration

Settings are stored in `~/.config/ubweat/config.json`:

```json
{
  "use_fahrenheit": false,
  "location": "",
  "refresh_minutes": 10,
  "show_condition": true
}
```

| Setting | Description |
|---------|-------------|
| use_fahrenheit | true = °F, false = °C |
| location | City name (empty = auto-detect) |
| refresh_minutes | Update interval |
| show_condition | Show weather text in tray |

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
uBWEAT/
├── ubweat.py          # Main application
├── icons/             # Weather icons
│   ├── weather-sunny.svg
│   ├── weather-cloudy.svg
│   ├── weather-rain.svg
│   ├── weather-snow.svg
│   ├── weather-fog.svg
│   └── weather-storm.svg
├── install.sh         # Installation script
├── uninstall.sh       # Uninstallation script
├── Makefile           # Build automation
├── README.md          # This file
├── LICENSE            # MIT License
├── CHANGELOG.md       # Version history
├── CONTRIBUTING.md    # Contribution guidelines
├── requirements.txt   # Dependencies
└── screenshots/       # Application screenshots
```

## How It Works

uBWEAT uses the free [wttr.in](https://wttr.in) weather service:
1. Fetches weather data via HTTP (no API key needed)
2. Auto-detects location by IP if not specified
3. Updates every 10 minutes
4. Displays temperature in system tray
5. Shows detailed weather info in dropdown menu

## Troubleshooting

### No weather data

- Check internet connection
- Try setting location manually
- Check if wttr.in is accessible: `curl wttr.in`

### Wrong location detected

- Use "Set Location..." to specify your city manually

### Tray icon not showing

Install the AppIndicator GNOME extension:
```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable it in GNOME Extensions, then log out/in.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Weather data provided by [wttr.in](https://wttr.in)

## Related Projects

- [uBRES](https://github.com/yourusername/uBRES) - Ubuntu resolution switcher
- [uBTEMP](https://github.com/yourusername/uBTEMP) - Ubuntu temperature monitor
- [uBTIME](https://github.com/yourusername/uBTIME) - Ubuntu world clock
