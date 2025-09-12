# Architecture

## Suite Structure

uBAPPS is a monorepo containing 7 independent system tray utilities. Each app is self-contained with no shared code between apps.

```
uBAPPS/
├── uBCPU/       # CPU monitor (451 LOC)
├── uBDISK/      # Disk I/O monitor (416 LOC)
├── uBNET/       # Network bandwidth (513 LOC)
├── uBRES/       # Resolution switcher (334 LOC)
├── uBTEMP/      # Temperature monitor (695 LOC)
├── uBTIME/      # World clock (431 LOC)
└── uBWEAT/      # Weather display (519 LOC)
```

## Common App Pattern

Every app follows the same architecture:

```
GTK Main Loop (Gtk.main())
    |
    v
AppIndicator3.Indicator (system tray icon + label)
    |
    v
GLib.timeout_add(interval_ms, callback)
    |
    v
Data Collection (procfs / sysfs / subprocess / API)
    |
    v
Update Strategy:
  - First load: build_menu() creates full GTK menu structure
  - Subsequent: update_labels() modifies existing label text only
  - Structural change: rebuild menu (new sensors, new interfaces)
```

## Data Sources

| App | Source | Method | Threading |
|-----|--------|--------|-----------|
| uBCPU | `/proc/stat` | File read, parse CPU jiffies, delta calculation | No |
| uBDISK | `/proc/diskstats` | File read, parse sector counts, speed from delta | No |
| uBNET | `/proc/net/dev` + `/sys/class/net/*/master` | File read + bridge detection | No |
| uBRES | `xrandr --query` | Subprocess, regex parse output | No |
| uBTEMP | `/sys/class/hwmon/`, `nvidia-smi`, `cli64`, `/sys/class/thermal/` | sysfs read + subprocess | No (15s cache for Areca cli64) |
| uBTIME | `datetime` + `zoneinfo` | Python stdlib | No |
| uBWEAT | `wttr.in` API | `urllib.request` via `threading.Thread` | Yes (background fetch) |

## Class Hierarchy (per app)

```
Config (dataclass)          - JSON load/save, default values
  |
Monitor/Manager class       - Data collection logic (stateful, tracks deltas)
  |
App class                   - GTK indicator, menu builder, update loop
  ├── build_menu()          - Creates full GTK menu structure
  ├── update_labels()       - Updates label text in existing widgets
  ├── auto_refresh()        - GLib timeout callback
  ├── on_about()            - GTK AboutDialog
  └── on_quit()             - Gtk.main_quit()
```

## AppIndicator Pattern

All apps use the Ayatana-first import pattern:

```python
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
except (ValueError, ImportError):
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
```

This supports both modern Ubuntu (Ayatana) and older systems (legacy AppIndicator).

## Threshold System

Four monitoring apps (CPU, DISK, NET, TEMP) use a two-tier threshold:

- **Warning** (orange): configurable, default varies per app
- **Critical** (red): configurable, triggers desktop notification (CPU, TEMP)

Color codes: `#44FF44` (green) / `#FFA500` (orange) / `#FF4444` (red)

## Per-App Install Layout

Each `install.sh` creates:

```
~/.local/bin/<appid>                          # Executable (copied from <appid>.py)
~/.local/share/<appid>/icons/*.svg            # Tray icons
~/.config/<appid>/config.json                 # User config (created if absent)
~/.config/autostart/<appid>.desktop           # Login autostart
~/.local/share/applications/<appid>.desktop   # Application menu entry
```

## No Shared Dependencies

Apps don't import from each other. This is intentional: users install any single app without the rest of the suite. The trade-off is ~80 LOC of duplicated boilerplate per app (AppIndicator import, Config pattern, color logic).

---

*Last updated: 2026-03-28*
