# Changelog

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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-09

### Added
- Custom lightning bolt tray icons that change color based on temperature
  - Green bolt: Normal temperatures
  - Orange bolt: Warning temperatures (70°C+)
  - Red bolt: Critical temperatures (85°C+)
- Icons directory with SVG icons

### Changed
- Tray icon now dynamically updates color based on highest temperature
- Smooth label updates instead of full menu rebuild (reduces flickering)
- Install script now copies icons folder

## [1.0.0] - 2026-01-09

### Added
- Initial release
- System tray integration using GTK3 and AppIndicator
- Real-time temperature monitoring (1 second refresh)
- Support for multiple sensor types:
  - CPU (coretemp, k10temp)
  - GPU (nvidia, amdgpu)
  - NVMe/SSD drives
  - HDD drives (drivetemp)
  - Motherboard sensors
- Sensors organized by type in menu
- Color-coded temperature display:
  - Green: Normal (< 70°C)
  - Orange: Warning (70-85°C)
  - Red: Critical (> 85°C)
- Desktop notifications for critical temperatures
- Celsius/Fahrenheit toggle
- Right-click to rename any sensor
- Persistent configuration:
  - Custom sensor names
  - Temperature unit preference
  - Warning/critical thresholds
- Configuration stored in ~/.config/ubtemp/
- Install script with automatic dependency installation
- Uninstall script with optional config removal
- Auto-start on login support
- Tray icon shows highest temperature
- Support for both Ayatana AppIndicator and legacy AppIndicator3
