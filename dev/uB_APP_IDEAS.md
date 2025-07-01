# uB Suite - Ubuntu System Tray Utilities

## Overview

**uB Suite** is a collection of lightweight, focused system tray applications designed specifically for Ubuntu and Linux desktop environments. Each app follows the Unix philosophy: do one thing and do it well.

The "uB" prefix stands for **Ubuntu** - these tools are built from the ground up for the Linux desktop experience, living quietly in your system tray and providing instant access to essential system information and controls with a single click.

---

## Philosophy

### Lightweight by Design
Every uB app is a single Python file with minimal dependencies. No bloated frameworks, no electron wrappers, no gigabytes of RAM consumed. Just clean, efficient code that runs quietly in the background.

### Always Accessible
Information should be one click away. uB apps live in your system tray - the most accessible real estate on your desktop. Glance at your CPU temperature, check network speeds, or switch display resolutions without opening a single window.

### Consistent Experience
All uB apps share a unified design language:
- Clean dropdown menus with organized sections
- Real-time updates without manual refresh
- Right-click for additional options
- Persistent settings that survive reboots
- Professional appearance that fits any desktop theme

### No Account Required
uB apps don't phone home, don't require accounts, and don't harvest data. They use local system resources and free public APIs where needed. Your system, your data, your control.

---

## The Suite

The uB Suite covers five essential categories:

### System Monitoring
Keep an eye on what matters. CPU load, memory pressure, disk space, temperatures, and network activity - all visible at a glance without opening resource-heavy system monitors.

### Utilities
Everyday tools that save time. Clipboard history, quick notes, calculations, screenshots - the small conveniences that add up to a smoother workflow.

### Connectivity
Manage your connections. WiFi networks, Bluetooth devices, VPN tunnels - quick toggles and status indicators for staying connected.

### Hardware Control
Direct access to hardware settings. Screen brightness, volume levels, battery status - adjust on the fly without diving into system settings.

### Information
World clock, weather conditions, system information - stay informed about what's happening around you and inside your machine.

---

## Target Audience

- **Power users** who want quick access to system information
- **Developers** who need to monitor resources while working
- **Linux enthusiasts** who appreciate lightweight, native tools
- **Anyone** tired of bloated system monitors and utility suites

---

## Technical Foundation

| Component | Technology |
|-----------|------------|
| Language | Python 3.6+ |
| GUI Framework | GTK 3.0 |
| System Tray | AppIndicator3 (Ayatana) |
| Configuration | JSON (~/.config/) |
| Installation | Single script, no sudo required |
| Auto-start | XDG autostart standard |

All apps are:
- Open source (MIT License)
- Self-contained (single .py file + icons)
- Dependency-light (uses system Python and GTK)
- Fully documented (README, CHANGELOG, etc.)

---

## Project Status

| Status | Count | Apps |
|--------|-------|------|
| Completed | 7 | uBCPU, uBDISK, uBNET, uBRES, uBTEMP, uBTIME, uBWEAT |
| Planned | 12 | See detailed list below |
| **Total** | **19** | |

---

## Completed Apps

| App | Description | Status |
|-----|-------------|--------|
| **uBCPU** | CPU usage monitor | ✅ Done |
| **uBDISK** | Disk I/O bandwidth monitor | ✅ Done |
| **uBNET** | Network bandwidth monitor | ✅ Done |
| **uBRES** | Display resolution switcher | ✅ Done |
| **uBTEMP** | Hardware temperature monitor | ✅ Done |
| **uBTIME** | World clock / timezone viewer | ✅ Done |
| **uBWEAT** | Local weather & temperature | ✅ Done |

---

## System Monitoring Apps

### uBNET - Network Monitor
- Upload/download speed in real-time
- Current IP address (local & public)
- Connection status (connected/disconnected)
- Network interface info
- Data usage stats

### uBCPU - CPU Monitor
- Overall CPU usage percentage
- Per-core usage stats
- CPU frequency
- Load average
- Top processes by CPU

### uBMEM - Memory Monitor
- RAM usage (used/total/percentage)
- Swap usage
- Memory breakdown (cached, buffers, available)
- Top processes by memory

### uBDISK - Disk Space Monitor
- Space usage for all mounted drives
- Percentage used/free
- Read/write activity
- Warning when disk is nearly full

### uBPROC - Process Monitor
- Top processes by CPU usage
- Top processes by memory usage
- Process count
- Quick kill process option
- System load overview

---

## Utility Apps

### uBCLIP - Clipboard Manager
- Clipboard history (last N items)
- Search clipboard history
- Pin frequently used items
- Clear clipboard option
- Support for text and images

### uBNOTE - Quick Notes
- Create quick notes from tray
- Persistent notes storage
- Organize with tags/categories
- Search notes
- Timestamp on notes

### uBCALC - Quick Calculator
- Calculator in dropdown menu
- Basic operations (+, -, *, /)
- Scientific functions
- History of calculations
- Copy result to clipboard

### uBCOLOR - Color Picker
- Pick color from screen
- Show HEX, RGB, HSL values
- Color history
- Copy color code to clipboard
- Color palette storage

### uBSCREEN - Screenshot Tool
- Full screen capture
- Window capture
- Region selection
- Delay timer option
- Save to file or clipboard

---

## Connectivity Apps

### uBBLUE - Bluetooth Manager
- List paired devices
- Connect/disconnect devices
- Battery level for connected devices
- Quick toggle Bluetooth on/off
- Pairing mode

### uBVPN - VPN Manager
- VPN connection status
- Quick connect/disconnect
- Multiple VPN profiles
- Connection time display
- IP address when connected

### uBWIFI - WiFi Manager
- Available networks list
- Signal strength indicator
- Quick connect to saved networks
- Current connection info
- Network speed

---

## Hardware Control Apps

### uBBAT - Battery Monitor
- Battery percentage
- Charging status
- Time remaining
- Battery health
- Power mode switching
- (For laptops/portable devices)

### uBBRIGHT - Brightness Control
- Screen brightness slider
- Quick brightness presets
- Auto-brightness toggle
- Night light / blue light filter
- Per-monitor control

### uBVOL - Volume Control
- Master volume control
- Per-application volume
- Input/output device selection
- Mute toggle
- Audio visualizer

---

## Build Order (Suggested)

### Priority 1 - High Utility
1. uBNET - Network speeds are always useful
2. uBCLIP - Clipboard history is essential
3. uBCPU - System load monitoring

### Priority 2 - System Monitoring
4. uBMEM - Memory monitoring
5. uBDISK - Disk space tracking
6. uBPROC - Process management

### Priority 3 - Utilities
7. uBNOTE - Quick notes
8. uBCALC - Calculator
9. uBSCREEN - Screenshots
10. uBCOLOR - Color picker

### Priority 4 - Connectivity
11. uBWIFI - WiFi management
12. uBBLUE - Bluetooth management
13. uBVPN - VPN control

### Priority 5 - Hardware
14. uBBAT - Battery (if laptop)
15. uBBRIGHT - Brightness
16. uBVOL - Volume control

---

## Technical Notes

### Common Stack
- Python 3
- GTK 3.0
- AppIndicator3 (Ayatana)
- System Python (/usr/bin/python3)

### Common Features
- System tray integration
- Persistent configuration (~/.config/ubXXX/)
- Auto-start on login
- Install/uninstall scripts
- Full GitHub repo structure

### Data Sources
| App | Data Source |
|-----|-------------|
| uBNET | /sys/class/net/, psutil |
| uBCPU | /proc/stat, psutil |
| uBMEM | /proc/meminfo, psutil |
| uBDISK | df, /proc/mounts |
| uBPROC | /proc/, psutil |
| uBCLIP | GTK Clipboard |
| uBBLUE | bluetoothctl, D-Bus |
| uBWIFI | nmcli, NetworkManager |
| uBBAT | /sys/class/power_supply/ |
| uBBRIGHT | xrandr, /sys/class/backlight/ |
| uBVOL | pactl, PulseAudio |

---

## Archive Location
All completed apps archived in: `~/archive/`

---

*Last updated: 2026-01-09*
