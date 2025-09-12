# Build & Compile

## No Build Required

uB Suite apps are pure Python scripts. No compilation or build step needed. Each app is a single `.py` file that runs directly with `python3`.

## Dependencies

System packages only (no pip):

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin
```

Per-app extras:
- **uBTEMP**: `sudo apt install lm-sensors`
- **uBRES**: `xrandr` (usually pre-installed)

## Packaging

No packaging system currently. Each app is installed by its `install.sh` script which copies files to `~/.local/`.

Future: `.deb` packages could be created for system-level installation.
