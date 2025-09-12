# Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.6+ (3.9+ for uBTIME) | Core language |
| GTK 3.0 | 3.x | Widget toolkit |
| AppIndicator3 | Ayatana | System tray icon support |
| GLib | (GTK built-in) | Event loop, timeout polling |
| procfs | (kernel) | CPU stats, disk stats |
| sysfs | (kernel) | Network interface counters |
| xrandr | (X11) | Display resolution management |
| lm-sensors | (system) | Hardware temperature readings |
| zoneinfo | (Python 3.9+ stdlib) | Timezone data for world clock |
| wttr.in | (web API) | Weather data |

## Why These Choices

- **Python**: Simplest language for GTK bindings, pre-installed on Ubuntu
- **GTK3**: Last GTK version with AppIndicator support
- **AppIndicator3 (Ayatana)**: The only way to get system tray icons on modern GNOME
- **GLib.timeout**: GTK-safe polling that doesn't need threading
- **procfs/sysfs**: Direct kernel data, no external dependencies, zero overhead
- **Single-file apps**: Maximum simplicity, no imports between apps, easy to understand and modify
