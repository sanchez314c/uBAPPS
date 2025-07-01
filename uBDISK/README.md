# uBDISK

Disk I/O bandwidth monitor for Ubuntu/Linux system tray.

## Features

- Combined I/O speed display in tray
- Per-disk read/write breakdown
- Color-coded activity levels
- Filter physical vs virtual disks

## Quick Start

```bash
# Install
./install.sh
# or
make install

# Run
ubdisk
```

## Requirements

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

## Data Source

Reads from `/proc/diskstats` for disk I/O statistics.

## Configuration

File: `~/.config/ubdisk/config.json`

```json
{
  "warning_threshold_mb": 50.0,
  "critical_threshold_mb": 100.0,
  "update_interval_ms": 1000,
  "show_virtual": false
}
```

## License

MIT License
