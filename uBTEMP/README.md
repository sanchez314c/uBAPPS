# uBTEMP - Ubuntu Temperature Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)]()
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)]()

A lightweight system tray application for monitoring hardware temperatures on Ubuntu/Linux.

---

## Features

- **Real-time monitoring** - Updates every 1 second
- **System tray integration** - Lives in your panel with temperature display
- **Dynamic tray icon** - Color changes based on temperature status (green/orange/red)
- **Multi-sensor support** - CPU, GPU, NVMe, HDD, motherboard sensors
- **Organized by type** - Sensors grouped by category (CPU, GPU, Storage, etc.)
- **Celsius/Fahrenheit toggle** - Switch units with one click
- **Custom sensor names** - Right-click any sensor to rename it
- **Color-coded temperatures**:
  - Green: Normal (< 70°C)
  - Orange: Warning (70-85°C)
  - Red: Critical (> 85°C)
- **Desktop notifications** - Alerts when temperatures reach critical levels
- **Persistent settings** - Saves custom names and preferences
- **Lightweight** - Single Python file, minimal resource usage

## Screenshots

The application appears in your system tray showing the highest temperature. Clicking it shows:

```
── CPU ──
  Package id 0      46.0°C
  Core 0            41.0°C
  Core 1            39.0°C
  Core 2            38.0°C
  Core 3            40.0°C
────────────────────────────
── NVMe/SSD ──
  Composite         47.9°C
  Composite         40.9°C
────────────────────────────
Switch to °F
────────────────────────────
↻ Refresh Now
About uBTEMP
Quit
```

Temperatures are color-coded:
- **Green** = Normal
- **Orange** = Warning
- **Red** = Critical

## Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu/Linux | 18.04+ |
| Python | 3.6+ |
| GTK | 3.0 |
| lm-sensors | Any |
| AppIndicator | Ayatana or legacy |

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/yourusername/uBTEMP.git
cd uBTEMP
make install
```

Or without make:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. Install lm-sensors if needed
2. Run `sensors-detect` to configure sensors
3. Install required Python/GTK packages
4. Copy the application to `~/.local/share/ubtemp/`
5. Create launcher and desktop entries
6. Enable auto-start on login

### Manual Install

1. Install dependencies:
```bash
sudo apt install lm-sensors python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
sudo sensors-detect
```

2. Run directly:
```bash
/usr/bin/python3 ubtemp.py
```

## Usage

### Basic Usage

| Action | Result |
|--------|--------|
| Click tray icon | Opens temperature menu |
| Right-click sensor | Rename the sensor |
| Click temperature unit | Toggle °C / °F |
| ↻ Refresh Now | Force immediate update |

### Renaming Sensors

1. Open the menu by clicking the tray icon
2. Right-click on any sensor
3. Enter a custom name (e.g., "Main SSD" instead of "Composite")
4. Click OK to save

Custom names persist across restarts.

### Temperature Thresholds

| Temperature | Color | Status |
|-------------|-------|--------|
| < 70°C | Green | Normal |
| 70-85°C | Orange | Warning |
| > 85°C | Red | Critical (+ notification) |

### Command Line

```bash
# Run directly
ubtemp

# Or with make
make run

# View raw sensor data
make sensors
```

## Configuration

Settings are stored in `~/.config/ubtemp/config.json`:

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
uBTEMP/
├── ubtemp.py          # Main application
├── icons/             # Tray icons (SVG)
│   ├── temp-normal.svg    # Green circle (normal)
│   ├── temp-warning.svg   # Orange circle (warning)
│   └── temp-critical.svg  # Red circle (critical)
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

uBTEMP uses `lm-sensors` to:
1. Query all hardware temperature sensors (via `sensors -j`)
2. Parse JSON output for temperature readings
3. Classify sensors by type (CPU, GPU, NVMe, etc.)
4. Display in organized menu with color coding
5. Send notifications for critical temperatures

The application runs as a GTK AppIndicator, updating every second.

## Troubleshooting

### No sensors detected

Run sensor detection:
```bash
sudo sensors-detect
```

Accept defaults, then reload modules or reboot.

### Missing sensors

Some sensors require kernel modules. After `sensors-detect`, you may need to:
```bash
sudo modprobe <module_name>
```

Add modules to `/etc/modules` for persistence.

### Tray icon not showing

Install the AppIndicator GNOME extension:
```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable it in GNOME Extensions, then log out/in.

### Python/gi module not found

Use system Python instead of conda/pyenv:
```bash
/usr/bin/python3 ubtemp.py
```

### GPU temperatures not showing

For NVIDIA GPUs, temperatures may appear via `nvidia-smi` instead of lm-sensors. Consider checking:
```bash
nvidia-smi --query-gpu=temperature.gpu --format=csv
```

For AMD GPUs, ensure `amdgpu` driver is loaded.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Related Projects

- [lm-sensors](https://github.com/lm-sensors/lm-sensors) - Linux hardware monitoring
- [psensor](https://github.com/chinf/psensor) - Graphical hardware temperature monitor
