# Product Requirements Document — uB Suite (uBAPPS)

## 1. Overview

**uB Suite** is a collection of 7 standalone system tray utilities for Ubuntu/Linux. Each app is a single Python file that uses GTK3 AppIndicator to show live system data in the desktop panel. The apps are lightweight, native, and designed for zero-interaction monitoring.

**Repository**: uBAPPS
**Version**: 1.0.0
**License**: MIT
**Author**: sanchez314c

---

## 2. Problem Statement

Linux desktop environments lack lightweight, native system tray monitors. Existing solutions are either:

- **Heavy GUI apps** (System Monitor, htop-in-terminal) that require opening a window and take focus
- **CLI-only tools** (top, sensors, ip) that aren't glanceable from the desktop
- **Electron-based monitors** that consume 200+ MB RAM for a status icon

Users want quick, always-visible system data without opening anything. A glance at the panel should tell you CPU load, temperatures, network speed, and weather.

---

## 3. Solution

Seven independent system tray apps, each showing one metric in the panel area:

| App | Purpose | Data Source | Update Interval |
|-----|---------|-------------|-----------------|
| **uBCPU** | CPU usage (total + per-core) | `/proc/stat` | 1s |
| **uBDISK** | Disk I/O read/write bandwidth | `/proc/diskstats` | 1s |
| **uBNET** | Network upload/download bandwidth | `/proc/net/dev` | 1s |
| **uBRES** | Display resolution quick-switcher | `xrandr` | 5s (auto-detect changes) |
| **uBTEMP** | Hardware temperatures (CPU, GPU, NVMe, RAID) | hwmon sysfs, nvidia-smi, cli64 | 1s |
| **uBTIME** | World clock with favorites | `zoneinfo` stdlib | 1s |
| **uBWEAT** | Weather with auto-location | wttr.in API | 10min |

---

## 4. Target Users

- **Primary**: Linux desktop users (Ubuntu, Ubuntu Budgie, GNOME Shell) who want always-on system monitoring
- **Secondary**: System administrators who want quick glanceable hardware status
- **Tertiary**: Power users managing multi-monitor setups (uBRES), RAID arrays (uBTEMP), or bridged networks (uBNET)

---

## 5. Functional Requirements

### 5.1 Per-App Requirements

Every app must:

1. Show live data in the system tray icon label
2. Provide a dropdown menu with detailed info on click
3. Use color-coded status (green/orange/red) for threshold-based metrics
4. Support JSON config file in `~/.config/<app-id>/config.json`
5. Auto-start on login via `.desktop` file in `~/.config/autostart/`
6. Install via `./install.sh` to `~/.local/bin/` (no root required)
7. Run under 5 MB memory footprint
8. Work on both X11 and Wayland (except uBRES which requires X11)

### 5.2 uBCPU-Specific

- Total CPU percentage in tray label
- Per-core usage breakdown in menu
- System load averages (1, 5, 15 min)
- Desktop notification on critical threshold breach (default: 90%)
- Notification cooldown (30s) to prevent spam

### 5.3 uBDISK-Specific

- Combined read/write speed in tray label (MB/s)
- Per-device read/write breakdown
- Filter: physical disks only by default (skip loop, ram, dm- devices)
- NVMe partition filtering (skip `nvme0n1p*`)
- Human-readable speed formatting (B/s through GB/s)

### 5.4 uBNET-Specific

- Combined download/upload speed in tray label
- Per-interface RX/TX speeds
- Bridge member detection (via `/sys/class/net/*/master`) to avoid double-counting
- Bridge members shown dimmed with "(bridged)" annotation
- Session totals (cumulative bytes since app start)
- Filter: hide loopback, docker, virbr, veth by default

### 5.5 uBRES-Specific

- List all connected displays with resolutions from xrandr
- Show current resolution with checkmark
- Display aspect ratio (16:9, 16:10, 4:3, 21:9)
- Show refresh rates
- One-click resolution switching
- Desktop notification on change
- Auto-detect display hotplug (5s polling)
- Requires X11 (not Wayland compatible)

### 5.6 uBTEMP-Specific

- Highest temperature in tray label (color-coded)
- Sensors grouped by type: CPU, GPU, RAID, NVMe/SSD, HDD, Motherboard, Other
- Four sensor sources: hwmon sysfs, nvidia-smi, Areca cli64, thermal_zone
- Areca RAID controller cache (15s poll interval to avoid I2C bus hammering)
- Custom sensor naming (right-click to rename, persisted to config)
- Celsius/Fahrenheit toggle (persisted)
- Critical temperature notifications (60s cooldown per sensor)
- Automatic sensor list change detection (rebuild menu only when sensors appear/disappear)

### 5.7 uBTIME-Specific

- Local time in tray label
- Favorites list (default: NY, LA, London, Paris, Tokyo, Shanghai, Sydney, UTC)
- All timezones organized by region via submenus
- UTC offset display per timezone
- 12h/24h toggle (persisted)
- Show/hide seconds toggle
- Left-click: copy time to clipboard
- Right-click: add/remove from favorites
- Requires Python 3.9+ (for `zoneinfo`)

### 5.8 uBWEAT-Specific

- Temperature in tray label
- Auto-detect location via IP geolocation (wttr.in)
- Manual location override (dialog)
- Detailed info: temperature, feels-like, condition, humidity, wind, pressure, UV index
- Weather-appropriate tray icon (sunny, cloudy, rain, storm, snow, fog)
- Celsius/Fahrenheit toggle
- Background thread for HTTP requests (non-blocking GTK main loop)
- No API key required (uses wttr.in free API)

---

## 6. Non-Functional Requirements

### 6.1 Performance

- Each app: < 5 MB RSS memory
- CPU overhead: < 0.5% per app at 1s polling
- Startup time: < 1 second (except uBWEAT which does initial HTTP fetch)

### 6.2 Dependencies

- **Required**: Python 3.6+ (3.9+ for uBTIME), GTK 3.0, AppIndicator3 (Ayatana)
- **Optional**: lm-sensors (uBTEMP hwmon), nvidia-smi (uBTEMP GPU), xrandr (uBRES), cli64 (uBTEMP RAID)
- **System packages**: `python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`, `gir1.2-ayatanaappindicator3-0.1`, `libnotify-bin`

### 6.3 Compatibility

- Ubuntu 18.04+ (any GNOME, Budgie, or Unity desktop)
- GNOME Shell requires `gnome-shell-extension-appindicator`
- AppIndicator: Ayatana preferred, legacy fallback supported

### 6.4 Security

- No root required for installation or operation (except uBTEMP's `sudo -n cli64` for Areca RAID, which requires passwordless sudo configured)
- uBWEAT is the only app making network requests
- No telemetry, no analytics, no phone-home
- Config files are user-local (~/.config/)

---

## 7. Architecture

### 7.1 Common Pattern

All apps follow the same structure:

```
1. Import gi, require GTK 3.0
2. Import AppIndicator (Ayatana with legacy fallback)
3. Define data classes for readings
4. Define Config dataclass with load/save
5. Define Monitor class (data collection logic)
6. Define App class (GTK indicator + menu + update loop)
7. main() -> App().run() -> Gtk.main()
```

### 7.2 Update Strategy

Apps use `GLib.timeout_add()` for periodic updates. The callback:
1. Reads fresh data from the source
2. Updates label text in existing menu items (no menu rebuild)
3. Updates tray icon label
4. Updates tray icon (if threshold changed)

Menu is only rebuilt when the structure changes (new sensors, new interfaces). This avoids GTK widget creation overhead.

### 7.3 Install Structure

```
~/.local/bin/<appid>           # Executable Python script
~/.local/share/<appid>/icons/  # SVG tray icons
~/.config/<appid>/config.json  # User config
~/.config/autostart/<appid>.desktop  # Login autostart
~/.local/share/applications/<appid>.desktop  # App launcher
```

---

## 8. Non-Goals

- Graphical dashboards, charts, or historical graphs
- Data logging or persistence
- Remote monitoring or network-accessible API
- Windows or macOS support
- Shared code library between apps
- System-wide installation (always per-user in ~/.local)
- Wayland support for uBRES (xrandr is X11 only)

---

## 9. Technical Metrics

| Metric | Value |
|--------|-------|
| Total apps | 7 |
| Total Python LOC | ~3,476 |
| Largest app | uBTEMP (733 LOC) |
| Smallest app | uBRES (337 LOC) |
| Shared code between apps | 0 LOC (fully independent) |
| External API calls | 1 (uBWEAT -> wttr.in) |
| Test coverage | 0% (tests directory empty, to be addressed) |

---

## 10. Future Considerations

- Unit tests for data parsing logic (procfs parsers, xrandr parser, sensor readers)
- Shared AppIndicator base class to reduce boilerplate (~80 LOC duplicated per app)
- uBGPU: dedicated GPU monitor (utilization, VRAM, fan speed)
- uBBAT: battery monitor for laptops
- System-wide install option (`make install PREFIX=/usr/local`)
- Wayland support for resolution switching (wlr-randr)
- PPA packaging for apt-based installation

---

*Generated: 2026-03-28 | Updated: 2026-04-17 | Pipeline: repoprdgen*
