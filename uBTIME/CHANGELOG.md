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
- Display all world timezones with city/location identifiers
- Timezones organized by region (Africa, America, Asia, Europe, etc.)
- Favorites system for quick access to preferred timezones
- Default favorites: New York, Los Angeles, London, Paris, Tokyo, Shanghai, Sydney, UTC
- 12h/24h time format toggle
- Show/hide seconds option
- Real-time updates (every second)
- Left-click to copy timezone time to clipboard
- Right-click to add/remove from favorites
- UTC offset display for each timezone
- Local time display in tray and menu header
- Persistent configuration:
  - Favorite timezones
  - Time format preference
  - Seconds display preference
- Configuration stored in ~/.config/ubtime/
- Install script with automatic dependency installation
- Uninstall script with optional config removal
- Auto-start on login support
- Custom clock icon for system tray
