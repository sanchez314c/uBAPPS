# Development

## Environment Setup

```bash
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBAPPS
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1
```

## Running From Source

```bash
python3 uBCPU/uBCPU.py
python3 uBTEMP/uBTEMP.py
# etc.
```

## Project Structure

Each app follows the same layout:

```
uB<NAME>/
├── uB<NAME>.py      # Main script (single file)
├── install.sh        # Installer
├── icons/            # Tray icons (various states)
├── CLAUDE.md         # AI context
├── CHANGELOG.md      # Per-app changes
├── LICENSE           # MIT
└── CONTRIBUTING.md   # (some apps)
```

## Creating a New App

1. Create `uB<NAME>/` directory
2. Write `uB<NAME>.py` following the AppIndicator pattern:
   - Import gi, Gtk, AppIndicator3
   - Create indicator with icon
   - Add menu items
   - Use `GLib.timeout_add_seconds()` for polling
   - Call `Gtk.main()`
3. Create `install.sh` copying the pattern from existing apps
4. Add icons to `icons/`
5. Add entry to root `README.md`

## Code Conventions

- Single Python file per app (keep it simple)
- No external pip dependencies (only system packages)
- GTK3 + AppIndicator3 (Ayatana)
- Polling via GLib.timeout (not threading)
- Menu-based UI (no separate windows unless necessary)
