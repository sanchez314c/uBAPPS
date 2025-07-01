# uBNET Changelog

## [1.1.0] - 2026-02-05 21:15 CST

### Fixed
- **Bridge interface double-counting**: When a physical interface (e.g. `enp0s31f6`) is enslaved to a bridge (e.g. `br0`), both carried identical traffic but were summed in Network I/O totals, reporting ~2x the actual throughput. Now detects bridge membership via `/sys/class/net/<iface>/master` and excludes bridge members from totals.

### Added
- Bridge member detection via sysfs (`/sys/class/net/`)
- `is_bridge_member` field on `InterfaceStats` dataclass
- Visual distinction for bridged interfaces: dimmed colors with `(bridged)` annotation in Interfaces and Session Totals sections
- Bridge members still shown for informational purposes but excluded from Network I/O total and tray label

## [1.0.0] - 2025-01-12

### Initial Release
- System tray network bandwidth monitor
- Per-interface breakdown (physical, wireless)
- Configurable thresholds (warning/critical)
- Color-coded speed indicators
- Session total tracking
- Auto-start on login
