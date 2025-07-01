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

## [1.0.0] - 2026-01-09

### Added
- Initial release
- System tray integration using GTK3 and AppIndicator
- Display local temperature in system tray
- Auto-detect location by IP geolocation
- Manual location setting via dialog
- Weather conditions display (sunny, cloudy, rain, snow, etc.)
- Dynamic weather icons that change with conditions
- Celsius/Fahrenheit toggle
- Detailed weather information:
  - Temperature and "feels like"
  - Humidity percentage
  - Wind speed and direction
  - Atmospheric pressure
  - UV index
  - Cloud cover
- Auto-refresh every 10 minutes
- Manual refresh option
- No API key required (uses wttr.in)
- Persistent configuration
- Install script with automatic dependency installation
- Uninstall script with optional config removal
- Auto-start on login support
- Desktop notifications for errors
