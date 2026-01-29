# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |

## Security Model

uB Suite apps are lightweight system tray indicators. They read system data but do not write to system files or require elevated privileges.

### Data Access Per App

| App | Data Source | Access Level |
|-----|-----------|--------------|
| uBCPU | `/proc/stat` | Read-only |
| uBDISK | `/proc/diskstats` | Read-only |
| uBNET | `/sys/class/net/`, `/proc/net/dev` | Read-only |
| uBRES | `xrandr` (user session) | Read + display settings |
| uBTEMP | `/sys/class/hwmon/`, `nvidia-smi`, `cli64` | Read-only (see note below) |
| uBTIME | `zoneinfo` (stdlib) | Read-only |
| uBWEAT | `wttr.in` API | Outbound HTTP GET only |

### Network Access

Only uBWEAT makes network requests (HTTP GET to `wttr.in` for weather data). No authentication tokens, no POST requests, no data sent.

### Elevated Privileges

Most uB apps do not require root or sudo. The exception is **uBTEMP**, which optionally runs `sudo -n cli64 hw info` to read Areca RAID controller temperatures. This requires a NOPASSWD sudoers entry for `cli64` and only activates if an Areca controller is present. All other system data is read from procfs, sysfs, or user-session tools.

## Reporting a Vulnerability

1. **Email**: software@jasonpaulmichaels.co
2. **GitHub**: Open a [security advisory](https://github.com/sanchez314c/uBAPPS/security/advisories/new)

Response time: within 48 hours.
