# Technology Stack

## uB Suite - Common Technology

All uB Suite applications share a common technology stack and design pattern.

## Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.6+ (3.9+ for uBTIME) | Primary language |
| GTK | 3.0 | GUI toolkit |
| AppIndicator | Ayatana/Legacy | System tray integration |
| GObject | Introspection | Python-GTK bindings |

## Architecture Pattern

All uB apps follow the same architectural pattern:

```
┌──────────────────────────────────────────────┐
│              AppIndicator App                 │
├──────────────────────────────────────────────┤
│                                              │
│  ┌─────────────┐     ┌─────────────────┐    │
│  │  Indicator  │────▶│   Dropdown Menu │    │
│  │  (Tray Icon)│     │   (GTK Menu)    │    │
│  └─────────────┘     └─────────────────┘    │
│         │                                    │
│         ▼                                    │
│  ┌─────────────────────────────────────┐    │
│  │         GLib.timeout_add()          │    │
│  │      (Periodic Update Loop)         │    │
│  └─────────────────────────────────────┘    │
│         │                                    │
│         ▼                                    │
│  ┌─────────────────────────────────────┐    │
│  │        Data Source                  │    │
│  │  (/proc, /sys, xrandr, API, etc.)   │    │
│  └─────────────────────────────────────┘    │
│                                              │
└──────────────────────────────────────────────┘
```

## App Data Sources

| App | Data Source | Update Interval |
|-----|-------------|-----------------|
| uBCPU | `/proc/stat` | 1 second |
| uBDISK | `/proc/diskstats` | 1 second |
| uBNET | `/sys/class/net/` | 1 second |
| uBRES | `xrandr` | On-demand |
| uBTEMP | `lm-sensors` | 1 second |
| uBTIME | `zoneinfo` | 1 second |
| uBWEAT | `wttr.in` API | 10 minutes |

## Common Dependencies

```bash
# Required for all apps
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

## GNOME Extension Requirement

For tray icons to appear in GNOME Shell:
```bash
sudo apt install gnome-shell-extension-appindicator
```

## Design Principles

1. **Lightweight**: Single Python file per app
2. **Consistent**: All apps follow the same GTK AppIndicator pattern
3. **Standalone**: Each app is independent
4. **Configurable**: JSON config files in `~/.config/<app>/`
5. **Native**: Uses system APIs, no Electron/web views

## Configuration Pattern

All apps store configuration in `~/.config/<app-name>/config.json`:

```json
{
  "warning_threshold": 70,
  "critical_threshold": 85,
  "update_interval_ms": 1000,
  "show_notifications": true
}
```

## Color Coding Convention

| Status | Color | Meaning |
|--------|-------|---------|
| Normal | Green | Below warning threshold |
| Warning | Orange | Between warning and critical |
| Critical | Red | Above critical threshold |
