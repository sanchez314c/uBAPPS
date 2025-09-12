# Installation

## Prerequisites

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

### GNOME Shell Users

Install the AppIndicator extension for tray icon support:

```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable it in GNOME Extensions, then log out and back in.

### Per-App Dependencies

| App | Extra Dependencies |
|-----|--------------------|
| uBTEMP | `sudo apt install lm-sensors` then `sudo sensors-detect` |
| uBRES | `xrandr` (usually pre-installed) |
| uBWEAT | Internet connection for wttr.in |

## Installing Apps

Each app installs independently:

```bash
cd uBAPPS/uBCPU
./install.sh

cd uBAPPS/uBTEMP
./install.sh
```

The installer copies the script to `~/.local/bin/`, icons to `~/.local/share/icons/`, and creates autostart entries so the app launches on login.

## Verifying

After install, the app should appear in your system tray. If not:
1. Check that AppIndicator extension is enabled (GNOME)
2. Log out and back in
3. Run manually: `python3 ~/.local/bin/uBCPU.py`

## Uninstalling

Each app has an uninstall script:

```bash
cd uBAPPS/uBCPU
./uninstall.sh
```

Or remove manually:

```bash
rm ~/.local/bin/<appid>
rm -rf ~/.local/share/<appid>/
rm ~/.config/autostart/<appid>.desktop
rm ~/.local/share/applications/<appid>.desktop
rm -rf ~/.config/<appid>/
```

Where `<appid>` is the lowercase app name: `ubcpu`, `ubdisk`, `ubnet`, `ubres`, `ubtemp`, `ubtime`, `ubweat`.
