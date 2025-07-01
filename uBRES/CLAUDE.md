# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**uBRES** is a lightweight GTK system tray application for switching display resolutions on Ubuntu/Linux. It shows all available resolutions reported by the display and allows one-click switching. Inspired by RDM (Retina Display Menu) for macOS.

**Stack**: Python 3.6+ / GTK 3.0 / AppIndicator
**Platform**: Ubuntu/Linux (X11)

## Commands

```bash
# Installation
make install                      # Full installation
./install.sh                      # Alternative install

# Running
ubres                             # Run the application
make run                          # Run via make

# Uninstallation
make uninstall                    # Remove application
./uninstall.sh                    # Alternative uninstall
```

## Architecture

| File | Purpose |
|------|---------|
| `ubres.py` | Main GTK AppIndicator application (~12KB) |
| `install.sh` | Installation script with dependency handling |
| `uninstall.sh` | Clean removal script |
| `Makefile` | Build automation |

### How It Works

1. Queries connected displays via `xrandr`
2. Parses available resolutions with refresh rates
3. Displays organized menu with aspect ratios (16:9, 16:10, etc.)
4. Applies resolution changes via `xrandr --output <display> --mode <resolution>`
5. Auto-refreshes every 5 seconds to detect display changes

### Menu Structure

```
── DP-0 (Primary) ──
✓ 3840 × 2160  @60Hz  [16:9]
  2560 × 1440  @60Hz  [16:9]
────────────────────────────
↻ Refresh Displays
About uBRES
Quit
```

## Requirements

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 x11-xserver-utils
```

## Configuration

No persistent configuration - shows all resolutions reported by display EDID.
