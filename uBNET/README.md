# uBNET

Network bandwidth monitor for Ubuntu/Linux system tray.

## Features

- Combined throughput display in tray
- Per-interface RX/TX speeds
- Hide loopback/virtual interfaces
- Color-coded thresholds

## Quick Start

```bash
# Install
./install.sh

# Run
ubnet
```

## Requirements

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

## Data Source

Reads from `/sys/class/net/<interface>/statistics/` for network statistics.

## Configuration

File: `~/.config/ubnet/config.json`

```json
{
  "warning_threshold_mb": 10.0,
  "critical_threshold_mb": 50.0,
  "update_interval_ms": 1000,
  "show_loopback": false,
  "show_virtual": false
}
```

## License

MIT License
