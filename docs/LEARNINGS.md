# Learnings

## GTK4 Dropped AppIndicator Support

GTK4 removed the system tray API. AppIndicator3 only works with GTK3. This is why the entire suite is GTK3. There's no migration path to GTK4 for tray apps.

## GNOME Shell Hides Tray Icons by Default

Modern GNOME Shell doesn't show AppIndicator icons unless the `gnome-shell-extension-appindicator` extension is installed and enabled. This is the #1 support issue.

## GLib.timeout vs Threading

Using Python threads with GTK causes race conditions and crashes. `GLib.timeout_add_seconds()` runs the callback on the GTK main thread, which is safe. All data collection happens in these callbacks.

## procfs Is Faster Than subprocess

Reading `/proc/stat` directly is much faster than running `top` or `mpstat` via subprocess. Same for `/proc/diskstats` vs `iostat` and `/sys/class/net/` vs `ifconfig`. Direct file reads have zero process spawn overhead.

## Ayatana vs Legacy AppIndicator

Ubuntu switched from `AppIndicator3` to `AyatanaAppIndicator3`. The API is identical but the GIR package name changed. Install `gir1.2-ayatanaappindicator3-0.1` on modern Ubuntu.

## Single-File Apps Are Better for Tray Utilities

Each uB app is one Python file. This makes them trivial to install (copy one file), understand (read one file), and debug (run one file). No import chains, no package structure, no `__init__.py`.
