# Troubleshooting

## Tray Icon Not Visible (GNOME)

Install and enable the AppIndicator extension:

```bash
sudo apt install gnome-shell-extension-appindicator
```

Enable in GNOME Extensions app, then log out and back in.

## "No module named gi" Error

Install GTK Python bindings:

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

## "No module named AppIndicator3" Error

Install the Ayatana AppIndicator:

```bash
sudo apt install gir1.2-ayatanaappindicator3-0.1
```

## uBTEMP Shows No Temperatures

1. Install lm-sensors: `sudo apt install lm-sensors`
2. Detect sensors: `sudo sensors-detect` (answer YES to all)
3. Verify: `sensors` should show temperature readings
4. Restart uBTEMP

## uBWEAT Shows No Weather

Check internet connectivity. uBWEAT needs HTTP access to `wttr.in`. If behind a proxy, it may not work.

## App Crashes on Startup

Run manually from terminal to see the error:

```bash
# For apps installed via direct copy (uBCPU, uBDISK, uBNET):
python3 ~/.local/bin/ubcpu

# For apps installed via wrapper (uBRES, uBTEMP, uBTIME, uBWEAT):
python3 ~/.local/share/ubtemp/ubtemp.py
```

Common causes:
- Missing GTK dependencies
- Wrong Python version (uBTIME needs 3.9+ for zoneinfo)
- AppIndicator extension not enabled

## Multiple Instances Running

If you see duplicate tray icons, kill all instances:

```bash
pkill -f uBCPU.py
```

Then restart. The autostart entry launches one instance on login.
