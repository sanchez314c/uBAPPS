# Quick Start

## Install Dependencies

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin

# GNOME Shell users also need:
sudo apt install gnome-shell-extension-appindicator
```

## Install Any App

```bash
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBAPPS/uBCPU
./install.sh
```

The app appears in your system tray automatically and will auto-start on login.

## Run From Source

```bash
# Single app
python3 uBCPU/ubcpu.py

# Or use the runner script
./run-source-linux.sh ubcpu

# Launch all apps at once
./run-source-linux.sh all
```

## Configuration

Each app stores config in `~/.config/<appid>/config.json`. Defaults are created on first install.
