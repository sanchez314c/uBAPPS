# Changelog

## [2026-04-09 23:50:00] - Pipeline v2: Lint, Audit, Security Fixes

### Security
- **uBWEAT**: Fixed URL injection vulnerability in location parameter (replaced naive string replace with `urllib.parse.quote`)
- **uBWEAT**: Added response validation for wttr.in JSON data (`isinstance` check before accessing keys)

### Fixed
- **All 7 apps**: Narrowed all bare `except Exception` clauses to specific exception types
- **uBCPU**: Narrowed `get_load_average()` exception to `(OSError, IOError)`, added `len(parts)` guard
- **uBDISK**: Removed dead `get_usage_color()` call in `build_menu()`
- **uBRES**: Added `FileNotFoundError` handling in `main()` xrandr check
- **uBTIME**: Narrowed 4 bare excepts to specific types (`json.JSONDecodeError`, `OSError`, `KeyError`, etc.)
- **uBWEAT**: Narrowed 3 bare excepts to specific types, removed dead `get_full_display()` method
- **All 7 apps**: Removed 5 unused `import os` statements, 3 unused imports, 1 unused variable

### Documentation
- Fixed README.md: removed nonexistent "res-tweaker" app references and section
- Fixed uBNET data source documentation in README, CLAUDE.md, AGENTS.md (was `/sys/class/net/`, actual is `/proc/net/dev`)
- Fixed VERSION_MAP.md: uBNET version corrected from 1.0.0 to 1.1.0

### Added
- `ruff.toml` with E402 per-file suppressions for mandatory GTK `gi.require_version()` pattern

### Code Quality
- All 7 Python files reformatted with ruff format (consistent quoting, trailing commas, whitespace)
- Zero ruff violations, zero py_compile errors, zero shellcheck warnings

---

## [2026-03-14 17:30:00] - Forensic Audit Remediation

### Fixed
- **uBTIME/uBWEAT**: Added graceful exit with error message when neither AppIndicator variant is available (was crashing with unhandled ValueError)
- **uBCPU**: Changed bare `except:` to `except Exception:` in `get_load_average()` to avoid swallowing KeyboardInterrupt/SystemExit
- **uBTEMP**: Changed two bare `except:` clauses to specific `except (ValueError, PermissionError, FileNotFoundError):` in hwmon threshold reading
- **uBTEMP**: Fixed redundant `import time` inside method; now uses module-level `_time` alias
- **uBTEMP**: Added icon file existence check in `update_icon()` (consistent with uBCPU/uBDISK/uBNET)
- **uBRES**: Moved `from math import gcd` from inside loop to top-level import
- **uBRES**: Added `pkill` and `set -e` to uninstall script (was missing both)
- **uBDISK/uBNET**: Removed redundant identical branches in `format_speed_short()`
- **uBTIME**: Removed redundant conditional assignment (`city if favorite else city`)
- **All uninstall scripts**: Added `set -e` for proper error handling
- **CI**: ShellCheck step now enforces results (removed `|| true` bypass)
- **SECURITY.md**: Corrected claim about sudo requirements (uBTEMP Areca sensors need sudo)

### Added
- **uBDISK**: Added Makefile (was missing, all other apps had one)
- **uBNET**: Added Makefile (was missing, all other apps had one)
- **uBDISK**: Added requirements.txt (was missing)
- **uBNET**: Added requirements.txt (was missing)

### Documentation
- Fixed uBNET CLAUDE.md: data source is `/proc/net/dev`, not `/sys/class/net/`
- Fixed uBTEMP CLAUDE.md: updated data collection method to match actual hwmon/nvidia-smi/cli64 implementation
- Fixed docs/ARCHITECTURE.md: corrected uBTEMP data source documentation
- Fixed docs/TROUBLESHOOTING.md: corrected installed file path references
- Fixed docs/TODO.md: marked already-implemented features as complete
- Fixed dev/uB_APP_IDEAS.md: updated project status to show all 7 completed apps
- Fixed CHANGELOG.md: removed duplicate `# Changelog` header
- Fixed uBCPU CLAUDE.md: Python version from 3.8+ to 3.6+ (consistent with others)
- Fixed placeholder URLs in uBTIME, uBWEAT about dialogs and 4 CONTRIBUTING.md files

---

## [2026-02-22 11:35:00] - uBTEMP: Areca RAID Controller Sensor Support

### Added
- **Areca RAID controller temperature monitoring** via `cli64 hw info`
  - RAID CPU temperature (threshold: warn 85°C / critical 95°C)
  - RAID Board temperature (threshold: warn 70°C / critical 85°C)
- New `SensorType.RAID` category with dedicated "RAID Controller" section in menu
- Intelligent 15-second polling cache for Areca sensors (controller bus is slow)
- Sudoers NOPASSWD entry for `/usr/local/bin/cli64` to allow unprivileged reads

### Context
- Areca ARC-1882IX-12 controller does NOT expose temps via hwmon, lm-sensors, or thermal_zone
- Controller CPU was running at 90°C+ with no visibility in any monitoring tool
- The Areca's onboard piezo buzzer was firing thermal alarms independent of motherboard BIOS

---

## [2026-02-07 22:02:52] - Repository Compliance Fixes

### Added
- Created CLAUDE.md from AGENTS.md for consistency
- Added .gitkeep to protected empty folders (archive/, docs/, resources/, tests/, config/, logs/)
- Created resources/icons/ with placeholder icon where missing
- Created missing package.json for multiplicity

### Fixed  
- Renamed build_resources/ to resources/ (standard naming)
- Removed OS junk files (.DS_Store, Thumbs.db, ._*, Desktop.ini)
- Removed runtime artifacts (.pid files, logs) from presence-ai
- Added *.pid to .gitignore in presence-ai

### Structure
- All protected folders now have .gitkeep to prevent deletion
- Standard resources/ structure enforced
- Documentation synced (CLAUDE.md created where missing)

---

## [Unreleased]

### Planned
- Unified installer for all apps
- System tray menu to manage all uB apps
- Dark/light theme support

---

## uBCPU

### [1.0.0] - 2025-01-12
- Initial release
- CPU usage monitoring with per-core breakdown
- Load average display
- Configurable warning/critical thresholds
- Desktop notifications

## uBDISK

### [1.0.0] - 2025-01-12
- Initial release
- Disk I/O bandwidth monitoring
- Per-disk read/write breakdown
- Physical vs virtual disk filtering

## uBNET

### [1.0.0] - 2025-01-12
- Initial release
- Network bandwidth monitoring per interface
- Combined throughput display
- Loopback/virtual interface filtering

## uBRES

### [1.0.0] - 2025-01-09
- Initial release
- Resolution switching via xrandr
- Multi-monitor support
- Aspect ratio display
- Refresh rate information

## uBTEMP

### [1.0.0] - 2025-01-09
- Initial release
- Hardware temperature monitoring via lm-sensors
- Sensor organization by type (CPU, GPU, NVMe)
- Custom sensor naming
- Celsius/Fahrenheit toggle

## uBTIME

### [1.0.0] - 2025-01-09
- Initial release
- World clock with all timezones
- Favorites quick access
- 12h/24h format toggle
- Copy time to clipboard

## uBWEAT

### [1.0.0] - 2025-01-09
- Initial release
- Weather display via wttr.in
- Auto-location detection
- Celsius/Fahrenheit toggle
- Detailed weather info
