# API Reference

## Data Sources

### uBCPU - `/proc/stat`

Reads CPU jiffies (user, nice, system, idle, iowait, irq, softirq). Calculates percentage from delta between two readings.

### uBDISK - `/proc/diskstats`

Reads sector read/write counts per device. Converts to bytes/sec from delta between readings (512 bytes per sector).

### uBNET - `/sys/class/net/*/statistics/`

Reads `rx_bytes` and `tx_bytes` counters per interface. Calculates bandwidth from delta.

### uBRES - `xrandr`

Runs `xrandr --query` to list available resolutions and current setting. Uses `xrandr --output <display> --mode <resolution>` to change.

### uBTEMP - `lm-sensors`

Runs `sensors -j` for JSON output. Parses temperature readings per sensor chip.

### uBTIME - Python stdlib

Uses `datetime` + `zoneinfo` (Python 3.9+) or `pytz` for timezone conversions. No external data source.

### uBWEAT - wttr.in

HTTP GET to `wttr.in/<location>?format=<format>`. Returns weather data as formatted string. No API key required.

## GTK AppIndicator Pattern

All apps use the same initialization:

```python
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

indicator = AppIndicator3.Indicator.new(
    "uB<NAME>",
    icon_path,
    AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_menu(build_menu())
indicator.set_label("data", "")

GLib.timeout_add_seconds(interval, update_callback)
Gtk.main()
```

## Install Script Pattern

```bash
# Copy script
cp uB<NAME>.py ~/.local/bin/

# Copy icons
cp -r icons/ ~/.local/share/icons/uB<NAME>/

# Create autostart entry
cat > ~/.config/autostart/uB<NAME>.desktop << EOF
[Desktop Entry]
Type=Application
Name=uB<NAME>
Exec=python3 $HOME/.local/bin/uB<NAME>.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```
