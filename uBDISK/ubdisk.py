#!/usr/bin/python3
"""
uBDISK - Ubuntu Disk I/O Monitor
A system tray application for monitoring disk read/write bandwidth on Ubuntu/Linux.
"""

import gi

gi.require_version("Gtk", "3.0")

# Try Ayatana AppIndicator first (Ubuntu), fall back to regular AppIndicator
try:
    gi.require_version("AyatanaAppIndicator3", "0.1")
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
except (ValueError, ImportError):
    try:
        gi.require_version("AppIndicator3", "0.1")
        from gi.repository import AppIndicator3
    except (ValueError, ImportError):
        print("Error: Neither AyatanaAppIndicator3 nor AppIndicator3 found.")
        print("Install with: sudo apt install gir1.2-ayatanaappindicator3-0.1")
        import sys

        sys.exit(1)

from gi.repository import Gtk, GLib
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import time


@dataclass
class DiskStats:
    """Represents disk I/O statistics."""

    device: str
    read_bytes: int
    write_bytes: int
    read_speed: float = 0.0  # bytes/sec
    write_speed: float = 0.0  # bytes/sec

    @property
    def display_name(self) -> str:
        return self.device

    @property
    def total_speed(self) -> float:
        return self.read_speed + self.write_speed


@dataclass
class Config:
    """Application configuration."""

    warning_threshold_mb: float = 50.0  # MB/s
    critical_threshold_mb: float = 100.0  # MB/s
    update_interval_ms: int = 1000
    show_all_disks: bool = False  # Only show physical disks by default

    @classmethod
    def load(cls, path: Path) -> "Config":
        if path.exists():
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return cls(
                    warning_threshold_mb=data.get("warning_threshold_mb", 50.0),
                    critical_threshold_mb=data.get("critical_threshold_mb", 100.0),
                    update_interval_ms=data.get("update_interval_ms", 1000),
                    show_all_disks=data.get("show_all_disks", False),
                )
            except (json.JSONDecodeError, KeyError):
                pass
        return cls()

    def save(self, path: Path):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(
                    {
                        "warning_threshold_mb": self.warning_threshold_mb,
                        "critical_threshold_mb": self.critical_threshold_mb,
                        "update_interval_ms": self.update_interval_ms,
                        "show_all_disks": self.show_all_disks,
                    },
                    f,
                    indent=2,
                )
        except (OSError, IOError):
            pass


class DiskMonitor:
    """Handles disk I/O monitoring from /proc/diskstats."""

    SECTOR_SIZE = 512  # bytes

    def __init__(self, show_all: bool = False):
        self.show_all = show_all
        self.prev_stats: Dict[
            str, Tuple[int, int, float]
        ] = {}  # device -> (read, write, time)

    def get_disk_stats(self) -> List[DiskStats]:
        """Read disk I/O from /proc/diskstats and calculate bandwidth."""
        disks = []
        current_time = time.time()

        try:
            with open("/proc/diskstats", "r") as f:
                lines = f.readlines()
        except (PermissionError, FileNotFoundError):
            return disks

        for line in lines:
            parts = line.split()
            if len(parts) < 14:
                continue

            device = parts[2]

            # Filter devices - skip partitions and loop devices unless show_all
            if not self.show_all:
                # Skip loop devices, ram disks, and partitions (ending in numbers)
                if device.startswith(("loop", "ram", "dm-")):
                    continue
                # Skip partitions (e.g., sda1, nvme0n1p1)
                if device[-1].isdigit() and not device.startswith("nvme"):
                    # Check if it's a partition of a disk
                    if any(device.startswith(prefix) for prefix in ["sd", "hd", "vd"]):
                        continue
                # For NVMe, skip partitions (nvme0n1p1, etc.)
                if "nvme" in device and "p" in device:
                    continue

            try:
                # Fields: sectors read (index 5), sectors written (index 9)
                sectors_read = int(parts[5])
                sectors_written = int(parts[9])
            except (IndexError, ValueError):
                continue

            read_bytes = sectors_read * self.SECTOR_SIZE
            write_bytes = sectors_written * self.SECTOR_SIZE

            # Calculate speed based on delta from previous reading
            read_speed = 0.0
            write_speed = 0.0

            if device in self.prev_stats:
                prev_read, prev_write, prev_time = self.prev_stats[device]
                time_delta = current_time - prev_time

                if time_delta > 0:
                    read_speed = (read_bytes - prev_read) / time_delta
                    write_speed = (write_bytes - prev_write) / time_delta
                    # Clamp negative values (can happen on counter reset)
                    read_speed = max(0.0, read_speed)
                    write_speed = max(0.0, write_speed)

            # Store for next calculation
            self.prev_stats[device] = (read_bytes, write_bytes, current_time)

            disks.append(
                DiskStats(
                    device=device,
                    read_bytes=read_bytes,
                    write_bytes=write_bytes,
                    read_speed=read_speed,
                    write_speed=write_speed,
                )
            )

        # Sort by device name
        disks.sort(key=lambda d: d.device)

        return disks


def format_speed(bytes_per_sec: float) -> str:
    """Format bytes/sec to human readable string."""
    if bytes_per_sec >= 1024 * 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024 * 1024):.1f} GB/s"
    elif bytes_per_sec >= 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"
    elif bytes_per_sec >= 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec:.0f} B/s"


def format_speed_short(bytes_per_sec: float) -> str:
    """Format bytes/sec to short MB string for tray label."""
    mb_per_sec = bytes_per_sec / (1024 * 1024)
    if mb_per_sec >= 100:
        return f"{mb_per_sec:.0f}"
    else:
        return f"{mb_per_sec:.1f}"


class uBDISK:
    """Main application class for disk I/O monitoring."""

    APP_ID = "ubdisk"
    APP_NAME = "uBDISK"
    CONFIG_DIR = Path.home() / ".config" / "ubdisk"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubdisk" / "icons"

    def __init__(self):
        self.config = Config.load(self.CONFIG_FILE)
        self.disk_monitor = DiskMonitor(show_all=self.config.show_all_disks)
        self.disks: List[DiskStats] = []
        self.disk_labels: Dict[str, Gtk.Label] = {}
        self.total_read_speed = 0.0
        self.total_write_speed = 0.0
        self.menu = None
        self.current_icon = None

        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID,
            str(self.ICONS_DIR / "disk-normal.svg"),
            AppIndicator3.IndicatorCategory.HARDWARE,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)

        # Initial reading
        self.update_stats()
        self.build_menu()
        self.update_icon()

        # Update at configured interval
        GLib.timeout_add(self.config.update_interval_ms, self.auto_refresh)

    def get_total_speed_mb(self) -> float:
        """Get total disk speed in MB/s."""
        return (self.total_read_speed + self.total_write_speed) / (1024 * 1024)

    def get_usage_color(self, speed_mb: float) -> str:
        """Get color based on disk speed."""
        if speed_mb >= self.config.critical_threshold_mb:
            return "#FF4444"  # Red
        elif speed_mb >= self.config.warning_threshold_mb:
            return "#FFA500"  # Orange
        else:
            return "#44FF44"  # Green

    def get_icon_name(self, speed_mb: float) -> str:
        """Get icon name based on disk speed."""
        if speed_mb >= self.config.critical_threshold_mb:
            return "disk-critical"
        elif speed_mb >= self.config.warning_threshold_mb:
            return "disk-warning"
        else:
            return "disk-normal"

    def update_icon(self):
        """Update tray icon based on disk activity."""
        speed_mb = self.get_total_speed_mb()
        new_icon = self.get_icon_name(speed_mb)
        if new_icon != self.current_icon:
            icon_path = str(self.ICONS_DIR / f"{new_icon}.svg")
            if Path(icon_path).exists():
                self.indicator.set_icon_full(icon_path, "Disk I/O")
            self.current_icon = new_icon

    def update_stats(self):
        """Update disk I/O readings."""
        self.disks = self.disk_monitor.get_disk_stats()

        # Calculate totals
        self.total_read_speed = sum(d.read_speed for d in self.disks)
        self.total_write_speed = sum(d.write_speed for d in self.disks)

    def build_menu(self):
        """Build the indicator menu."""
        self.menu = Gtk.Menu()
        self.disk_labels.clear()

        # Total I/O header
        header = Gtk.MenuItem()
        label = Gtk.Label()
        label.set_markup("<b>━━ Disk I/O ━━</b>")
        label.set_xalign(0)
        header.add(label)
        header.set_sensitive(False)
        self.menu.append(header)

        # Total read/write
        total_item = Gtk.MenuItem()
        total_label = Gtk.Label()
        total_label.set_markup(
            f"<span foreground='#88CC88'>R: {format_speed(self.total_read_speed)}</span>  "
            f"<span foreground='#CC8888'>W: {format_speed(self.total_write_speed)}</span>"
        )
        total_label.set_xalign(0)
        total_item.add(total_label)
        total_item.set_sensitive(False)
        self.menu.append(total_item)
        self.disk_labels["total"] = total_label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Per-disk header
        disks_header = Gtk.MenuItem(label="━━ Devices ━━")
        disks_header.set_sensitive(False)
        self.menu.append(disks_header)

        # Individual disks
        for disk in self.disks:
            item = Gtk.MenuItem()
            label = Gtk.Label()
            label.set_markup(
                f"<span font_family='monospace'>{disk.device:<10}</span>  "
                f"<span foreground='#88CC88'>R: {format_speed(disk.read_speed):>10}</span>  "
                f"<span foreground='#CC8888'>W: {format_speed(disk.write_speed):>10}</span>"
            )
            label.set_xalign(0)
            label.set_margin_start(5)
            label.set_margin_end(5)
            item.add(label)
            item.set_sensitive(False)
            self.menu.append(item)
            self.disk_labels[disk.device] = label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Refresh option
        refresh_item = Gtk.MenuItem(label="↻ Refresh Now")
        refresh_item.connect("activate", self.on_refresh)
        self.menu.append(refresh_item)

        # About
        about_item = Gtk.MenuItem(label="About uBDISK")
        about_item.connect("activate", self.on_about)
        self.menu.append(about_item)

        # Quit
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Update tray label
        self.update_tray_label()

    def update_tray_label(self):
        """Update the tray label with current speeds in MB/s."""
        r = format_speed_short(self.total_read_speed)
        w = format_speed_short(self.total_write_speed)
        self.indicator.set_label(f"R{r} W{w} MB", "")

    def update_labels(self):
        """Update only the label text without rebuilding menu."""
        # Update total
        total_label = self.disk_labels.get("total")
        if total_label:
            total_label.set_markup(
                f"<span foreground='#88CC88'>R: {format_speed(self.total_read_speed)}</span>  "
                f"<span foreground='#CC8888'>W: {format_speed(self.total_write_speed)}</span>"
            )

        # Update individual disks
        for disk in self.disks:
            label = self.disk_labels.get(disk.device)
            if label:
                label.set_markup(
                    f"<span font_family='monospace'>{disk.device:<10}</span>  "
                    f"<span foreground='#88CC88'>R: {format_speed(disk.read_speed):>10}</span>  "
                    f"<span foreground='#CC8888'>W: {format_speed(disk.write_speed):>10}</span>"
                )

        # Update tray label and icon
        self.update_tray_label()
        self.update_icon()

    def auto_refresh(self) -> bool:
        """Auto-refresh callback."""
        self.update_stats()
        self.update_labels()
        return True

    def on_refresh(self, widget):
        """Manual refresh."""
        self.update_stats()
        self.update_labels()

    def on_about(self, widget):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("uBDISK")
        dialog.set_version("1.0.0")
        dialog.set_comments(
            "Ubuntu Disk I/O Monitor\n\n"
            "Monitors disk read/write bandwidth.\n"
            "Part of the uB Suite."
        )
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.run()
        dialog.destroy()

    def on_quit(self, widget):
        """Quit the application."""
        Gtk.main_quit()

    def run(self):
        """Start the GTK main loop."""
        Gtk.main()


def main():
    """Entry point."""
    app = uBDISK()
    app.run()


if __name__ == "__main__":
    main()
