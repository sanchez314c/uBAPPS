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

All notable changes to uBCPU will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-12

### Added
- Initial release
- Real-time CPU usage monitoring from /proc/stat
- System tray indicator with usage percentage label
- Per-core CPU usage breakdown in dropdown menu
- Color-coded status indicators (green/orange/red)
- Desktop notifications for critical CPU usage
- Configurable warning and critical thresholds
- Configurable update interval
- Load average display (1, 5, 15 minute)
- Install and uninstall scripts
- Autostart on login support
- JSON configuration file support
- SVG icons for normal, warning, and critical states
