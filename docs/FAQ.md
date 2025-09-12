# FAQ

### Why can't I see the tray icon on GNOME?

GNOME Shell doesn't show AppIndicator icons by default. Install the extension:

```bash
sudo apt install gnome-shell-extension-appindicator
```

Then enable it in GNOME Extensions and log out/in.

### Can I install just one app?

Yes. Each app is completely independent. Just `cd` into the app folder and run `./install.sh`.

### Do these apps use a lot of CPU?

No. They use GLib.timeout polling at intervals (typically 1-5 seconds). Between polls, they use zero CPU. The data reads from procfs/sysfs are essentially free.

### Does uBWEAT need an API key?

No. It uses wttr.in which is a free weather API that requires no registration or API key.

### Why GTK3 instead of GTK4?

GTK4 dropped support for AppIndicator3 (system tray icons). GTK3 is the last version with native tray support. Since the whole point of these apps is system tray integration, GTK3 is required.

### Do the apps auto-start on login?

Yes. The install scripts create autostart entries in `~/.config/autostart/`. To disable auto-start, delete the `.desktop` file there.

### Can I change the polling interval?

Edit the app's Python script and change the `GLib.timeout_add_seconds()` interval value. Then reinstall or restart the app.
