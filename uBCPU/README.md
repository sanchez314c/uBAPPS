# uBCPU - Ubuntu CPU Monitor

A lightweight system tray application for monitoring CPU usage on Ubuntu/Linux. Part of the uB Suite.

## Features

- **Real-time CPU Monitoring**: Displays total CPU usage in the system tray
- **Per-Core Breakdown**: Click to see individual core usage percentages
- **Color-Coded Status**: Green (normal), Orange (warning), Red (critical)
- **Desktop Notifications**: Alerts when CPU usage exceeds critical threshold
- **Load Average Display**: Shows 1, 5, and 15 minute load averages
- **Configurable Thresholds**: Customize warning and critical levels
- **Auto-Start**: Optionally starts on login

## Screenshot

The indicator displays total CPU usage in the tray. Clicking reveals:
- Total CPU percentage with color indicator
- Individual core usage (Core 0, Core 1, etc.)
- System load averages
- Refresh and Quit options

## Requirements

- Ubuntu 20.04+ or compatible Linux distribution
- Python 3.8+
- GTK 3.0
- AppIndicator3 (Ayatana or standard)

### Install Dependencies

```bash
sudo apt install python3 python3-gi gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

## Installation

```bash
git clone https://github.com/yourusername/uBCPU.git
cd uBCPU
./install.sh
```

The installer will:
1. Copy the application to `~/.local/bin/ubcpu`
2. Install icons to `~/.local/share/ubcpu/icons/`
3. Create default configuration at `~/.config/ubcpu/config.json`
4. Add autostart entry for login

## Usage

### Start the Application

```bash
ubcpu &
```

### Stop the Application

```bash
killall ubcpu
```

Or right-click the tray icon and select "Quit".

## Configuration

Configuration file: `~/.config/ubcpu/config.json`

```json
{
  "warning_threshold": 70.0,
  "critical_threshold": 90.0,
  "show_notifications": true,
  "update_interval_ms": 1000
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `warning_threshold` | 70.0 | CPU % to trigger orange warning state |
| `critical_threshold` | 90.0 | CPU % to trigger red critical state |
| `show_notifications` | true | Show desktop notifications on critical |
| `update_interval_ms` | 1000 | Refresh interval in milliseconds |

## Uninstallation

```bash
cd uBCPU
./uninstall.sh
```

## How It Works

uBCPU reads CPU statistics from `/proc/stat` and calculates usage percentages by comparing consecutive readings. The delta calculation method provides accurate real-time usage:

1. Read current CPU time values (user, system, idle, etc.)
2. Compare with previous reading
3. Calculate: `usage = (total_delta - idle_delta) / total_delta * 100`

This approach accounts for all CPU time components including:
- User processes
- System/kernel processes
- Nice (low priority) processes
- I/O wait
- Hardware/software interrupts
- Steal time (virtualization)

## Part of the uB Suite

uBCPU is part of the uB Suite of lightweight Ubuntu utilities:

- **uBRES** - Screen resolution manager
- **uBTEMP** - CPU temperature monitor
- **uBTIME** - World clock and time zones
- **uBWEAT** - Weather indicator
- **uBCPU** - CPU usage monitor (this app)

## License

MIT License - See [LICENSE](LICENSE) file.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
