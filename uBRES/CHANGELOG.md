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

## [1.0.0] - 2025-01-09

### Added
- Initial release
- System tray integration using GTK3 and AppIndicator
- Multi-monitor support with automatic detection
- Display of all available resolutions per monitor
- One-click resolution switching via xrandr
- Current resolution indicator (checkmark)
- Refresh rate display for each resolution
- Aspect ratio labels (16:9, 16:10, 4:3, 21:9, etc.)
- Auto-refresh every 5 seconds for display hotplug detection
- Desktop notifications on resolution change
- Install script with dependency management
- Uninstall script for clean removal
- Desktop entry for application menu
- Autostart entry for login startup
- Support for both Ayatana AppIndicator and legacy AppIndicator3
