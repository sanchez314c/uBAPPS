# uB Suite - Ubuntu System Tray Utilities

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)]()
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)]()

A collection of lightweight system tray utilities for Ubuntu/Linux. Each app is standalone, minimal, and follows a consistent design pattern using GTK AppIndicator.

---

## Applications

| App | Description | Data Source |
|-----|-------------|-------------|
| [**uBCPU**](#ubcpu) | CPU usage monitor | `/proc/stat` |
| [**uBDISK**](#ubdisk) | Disk I/O bandwidth monitor | `/proc/diskstats` |
| [**uBNET**](#ubnet) | Network bandwidth monitor | `/proc/net/dev` |
| [**uBRES**](#ubres) | Display resolution switcher | `xrandr` |
| [**uBTEMP**](#ubtemp) | Hardware temperature monitor | `lm-sensors` |
| [**uBTIME**](#ubtime) | World clock & timezones | `zoneinfo` |
| [**uBWEAT**](#ubweat) | Weather display | `wttr.in` |

---

## Quick Install

Each app can be installed independently:

```bash
cd uBAPPS/<app-name>
./install.sh
```

Or with make (where available):

```bash
cd uBAPPS/<app-name>
make install
```

---

## System Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu/Linux | 18.04+ |
| Python | 3.6+ (3.9+ for uBTIME) |
| GTK | 3.0 |
| AppIndicator | Ayatana or legacy |

### Common Dependencies

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

### GNOME Shell AppIndicator Extension

If tray icons don't appear, install the extension:

```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable it in GNOME Extensions, then log out/in.

---

## Application Details

### uBCPU

**CPU Usage Monitor** - Real-time CPU monitoring with per-core breakdown.

```
┌─────────────────────────┐
│ CPU: 45%                │
├─────────────────────────┤
│ Total CPU    45.2%  🟢  │
│ Core 0       52.1%      │
│ Core 1       41.3%      │
│ Core 2       48.7%      │
│ Core 3       38.6%      │
├─────────────────────────┤
│ Load: 1.24 1.15 1.08    │
└─────────────────────────┘
```

**Features:**
- Total CPU % in tray (color-coded)
- Per-core usage breakdown
- Load averages (1, 5, 15 min)
- Configurable warning/critical thresholds
- Desktop notifications on critical

**Config:** `~/.config/ubcpu/config.json`

---

### uBDISK

**Disk I/O Monitor** - Monitor read/write bandwidth across all disks.

```
┌─────────────────────────┐
│ Disk: 125 MB/s          │
├─────────────────────────┤
│ sda    R: 45 MB/s       │
│        W: 80 MB/s       │
│ nvme0  R: 120 MB/s      │
│        W: 5 MB/s        │
└─────────────────────────┘
```

**Features:**
- Combined I/O speed in tray
- Per-disk read/write breakdown
- Color-coded activity levels
- Filter physical vs virtual disks

**Config:** `~/.config/ubdisk/config.json`

---

### uBNET

**Network Monitor** - Track upload/download bandwidth per interface.

```
┌─────────────────────────┐
│ Net: ↓ 2.5 MB/s         │
├─────────────────────────┤
│ eth0   ↓ 2.1 MB/s       │
│        ↑ 0.4 MB/s       │
│ wlan0  ↓ 0.4 MB/s       │
│        ↑ 0.1 MB/s       │
└─────────────────────────┘
```

**Features:**
- Combined throughput in tray
- Per-interface RX/TX speeds
- Hide loopback/virtual interfaces
- Color-coded thresholds

**Config:** `~/.config/ubnet/config.json`

---

### uBRES

**Resolution Switcher** - Quick access to all available display resolutions.

```
┌─────────────────────────────────┐
│ ── DP-0 (Primary) ──            │
│ ✓ 3840 × 2160  @60Hz  [16:9]    │
│   2560 × 1440  @60Hz  [16:9]    │
│   1920 × 1080  @60Hz  [16:9]    │
├─────────────────────────────────┤
│ ↻ Refresh Displays              │
└─────────────────────────────────┘
```

**Features:**
- All available resolutions from EDID
- Multi-monitor support
- Aspect ratio display (16:9, 16:10, 4:3)
- Refresh rate info
- One-click switching

**Inspired by:** RDM (Retina Display Menu) for macOS

---

### uBTEMP

**Temperature Monitor** - Hardware temperature monitoring via lm-sensors.

```
┌─────────────────────────┐
│ 🌡️ 52°C                 │
├─────────────────────────┤
│ ── CPU ──               │
│ Package id 0    52°C 🟢 │
│ Core 0          48°C    │
│ Core 1          51°C    │
│ ── NVMe/SSD ──          │
│ Main SSD        45°C    │
├─────────────────────────┤
│ Switch to °F            │
└─────────────────────────┘
```

**Features:**
- Highest temp in tray (color-coded)
- Sensors organized by type (CPU, GPU, NVMe, HDD)
- Custom sensor naming (right-click to rename)
- Celsius/Fahrenheit toggle
- Critical temperature notifications

**Requires:** `lm-sensors` (`sudo sensors-detect` to configure)

**Config:** `~/.config/ubtemp/config.json`

---

### uBTIME

**World Clock** - View times across all world timezones.

```
┌─────────────────────────────────┐
│ Local: 14:32:45                 │
├─────────────────────────────────┤
│ ── Favorites ──                 │
│ New York      UTC-05  09:32:45  │
│ Los Angeles   UTC-08  06:32:45  │
│ London        UTC+00  14:32:45  │
│ Tokyo         UTC+09  23:32:45  │
├─────────────────────────────────┤
│ All Timezones  >                │
├─────────────────────────────────┤
│ Switch to 12h format            │
└─────────────────────────────────┘
```

**Features:**
- Local time in tray
- Favorites quick access
- All timezones by region
- UTC offset display
- 12h/24h toggle
- Copy time to clipboard (left-click)
- Add/remove favorites (right-click)

**Requires:** Python 3.9+ (for `zoneinfo`)

**Config:** `~/.config/ubtime/config.json`

---

### uBWEAT

**Weather Display** - Current weather with auto-location detection.

```
┌─────────────────────────────────┐
│ ☀️ 72°F                         │
├─────────────────────────────────┤
│ Los Angeles, United States      │
├─────────────────────────────────┤
│ Temperature: 72°F               │
│ Feels like: 70°F                │
│ Condition: Sunny                │
├─────────────────────────────────┤
│ Humidity: 45%                   │
│ Wind: W 8 mph                   │
│ UV Index: 6                     │
├─────────────────────────────────┤
│ ↻ Refresh Now                   │
│ Switch to °C                    │
│ Set Location...                 │
└─────────────────────────────────┘
```

**Features:**
- Temperature + condition in tray
- Auto-detect location (IP geolocation)
- Manual location setting
- Detailed weather info (humidity, wind, pressure, UV)
- Celsius/Fahrenheit toggle
- No API key required (uses wttr.in)

**Config:** `~/.config/ubweat/config.json`

---

## Configuration

All apps store configuration in `~/.config/<app-name>/config.json`.

### Common Config Options

| Option | Apps | Description |
|--------|------|-------------|
| `warning_threshold` | CPU, DISK, NET, TEMP | Threshold for orange warning |
| `critical_threshold` | CPU, DISK, NET, TEMP | Threshold for red critical |
| `update_interval_ms` | CPU, DISK, NET | Refresh rate in milliseconds |
| `show_notifications` | CPU, TEMP | Enable desktop notifications |
| `use_fahrenheit` | TEMP, WEAT | Temperature unit toggle |

---

## Uninstallation

Each app can be uninstalled independently:

```bash
cd uBAPPS/<app-name>
./uninstall.sh
# or
make uninstall
```

---

## Project Structure

```
uBAPPS/
├── README.md              # This file
├── CLAUDE.md              # AI context
├── docs/                  # Full documentation
│
├── uBCPU/                 # CPU monitor
│   ├── ubcpu.py
│   ├── install.sh
│   └── icons/
│
├── uBDISK/                # Disk I/O monitor
│   ├── ubdisk.py
│   ├── install.sh
│   └── icons/
│
├── uBNET/                 # Network monitor
│   ├── ubnet.py
│   ├── install.sh
│   └── icons/
│
├── uBRES/                 # Resolution switcher
│   ├── ubres.py
│   └── install.sh
│
├── uBTEMP/                # Temperature monitor
│   ├── ubtemp.py
│   ├── install.sh
│   └── icons/
│
├── uBTIME/                # World clock
│   ├── ubtime.py
│   ├── install.sh
│   └── icons/
│
└── uBWEAT/                # Weather display
    ├── ubweat.py
    ├── install.sh
    └── icons/
```

---

## Design Philosophy

- **Lightweight** - Single Python file per app, minimal dependencies
- **Consistent** - All apps follow the same GTK AppIndicator pattern
- **Standalone** - Each app is independent, install only what you need
- **Configurable** - JSON config files with sensible defaults
- **Native** - Uses system APIs and tools (no electron, no web views)

---

## Troubleshooting

### Tray icon not showing

```bash
# Install GNOME AppIndicator extension
sudo apt install gnome-shell-extension-appindicator

# Enable it and restart GNOME Shell
# Alt+F2 → type 'r' → Enter
```

### Python/gi module not found

Use system Python instead of conda/pyenv:

```bash
/usr/bin/python3 <app>.py
```

### X11 vs Wayland

uBRES and res-tweaker require X11. Check your session:

```bash
echo $XDG_SESSION_TYPE
```

---

## License

MIT License - See individual app LICENSE files for details.

---

## Contributing

Contributions welcome! Each app has its own CONTRIBUTING.md with guidelines.

---

**Built for Ubuntu/Linux users who want lightweight, native system monitoring.**
