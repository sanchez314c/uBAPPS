# Deployment

## Installation

Each app installs independently via its `install.sh`:

```bash
cd uBAPPS/uBCPU && ./install.sh
cd uBAPPS/uBTEMP && ./install.sh
```

## Distribution

### Git Clone (Primary)

```bash
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBAPPS/<app-name>
./install.sh
```

### Individual App Download

Each app is self-contained. Users can download just the app folder they need.

## Platform Support

| Platform | Status |
|----------|--------|
| Ubuntu 18.04+ | Supported |
| Ubuntu 22.04+ | Supported |
| Fedora (GNOME) | Should work (untested) |
| Arch (GNOME) | Should work (untested) |
| KDE Plasma | Supported (native tray support) |
| macOS | Not supported |
| Windows | Not supported |

## Auto-Start

The install scripts create `.desktop` files in `~/.config/autostart/` so apps launch automatically on login.

## Uninstall

```bash
rm ~/.local/bin/uB<NAME>.py
rm -r ~/.local/share/icons/uB<NAME>/
rm ~/.config/autostart/uB<NAME>.desktop
rm ~/.local/share/applications/uB<NAME>.desktop
```
