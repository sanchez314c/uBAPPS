#!/usr/bin/python3
"""
uBCPU - Ubuntu CPU Monitor
A system tray application for monitoring CPU usage on Ubuntu/Linux.
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
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import time


@dataclass
class CPUCore:
    """Represents a CPU core with its usage statistics."""

    core_id: int
    usage_percent: float
    user: int = 0
    nice: int = 0
    system: int = 0
    idle: int = 0
    iowait: int = 0
    irq: int = 0
    softirq: int = 0
    steal: int = 0

    @property
    def display_name(self) -> str:
        if self.core_id == -1:
            return "Total"
        return f"Core {self.core_id}"


@dataclass
class Config:
    """Application configuration."""

    warning_threshold: float = 70.0
    critical_threshold: float = 90.0
    show_notifications: bool = True
    update_interval_ms: int = 1000

    @classmethod
    def load(cls, path: Path) -> "Config":
        if path.exists():
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return cls(
                    warning_threshold=data.get("warning_threshold", 70.0),
                    critical_threshold=data.get("critical_threshold", 90.0),
                    show_notifications=data.get("show_notifications", True),
                    update_interval_ms=data.get("update_interval_ms", 1000),
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
                        "warning_threshold": self.warning_threshold,
                        "critical_threshold": self.critical_threshold,
                        "show_notifications": self.show_notifications,
                        "update_interval_ms": self.update_interval_ms,
                    },
                    f,
                    indent=2,
                )
        except (OSError, IOError):
            pass


class CPUMonitor:
    """Handles CPU usage monitoring from /proc/stat."""

    def __init__(self):
        self.prev_stats: Dict[int, Tuple[int, int]] = {}  # core_id -> (total, idle)

    def get_cpu_usage(self) -> List[CPUCore]:
        """Read CPU usage from /proc/stat and calculate percentages."""
        cores = []

        try:
            with open("/proc/stat", "r") as f:
                lines = f.readlines()
        except (PermissionError, FileNotFoundError):
            return cores

        for line in lines:
            if not line.startswith("cpu"):
                continue

            parts = line.split()
            cpu_id = parts[0]

            # Parse the CPU line
            if cpu_id == "cpu":
                core_id = -1  # Total CPU
            elif cpu_id.startswith("cpu"):
                try:
                    core_id = int(cpu_id[3:])
                except ValueError:
                    continue
            else:
                continue

            # Parse stats: user, nice, system, idle, iowait, irq, softirq, steal
            try:
                user = int(parts[1])
                nice = int(parts[2])
                system = int(parts[3])
                idle = int(parts[4])
                iowait = int(parts[5]) if len(parts) > 5 else 0
                irq = int(parts[6]) if len(parts) > 6 else 0
                softirq = int(parts[7]) if len(parts) > 7 else 0
                steal = int(parts[8]) if len(parts) > 8 else 0
            except (IndexError, ValueError):
                continue

            # Calculate totals
            idle_total = idle + iowait
            non_idle = user + nice + system + irq + softirq + steal
            total = idle_total + non_idle

            # Calculate usage percentage based on delta from previous reading
            usage_percent = 0.0
            if core_id in self.prev_stats:
                prev_total, prev_idle = self.prev_stats[core_id]
                total_delta = total - prev_total
                idle_delta = idle_total - prev_idle

                if total_delta > 0:
                    usage_percent = ((total_delta - idle_delta) / total_delta) * 100.0
                    usage_percent = max(0.0, min(100.0, usage_percent))

            # Store for next calculation
            self.prev_stats[core_id] = (total, idle_total)

            cores.append(
                CPUCore(
                    core_id=core_id,
                    usage_percent=usage_percent,
                    user=user,
                    nice=nice,
                    system=system,
                    idle=idle,
                    iowait=iowait,
                    irq=irq,
                    softirq=softirq,
                    steal=steal,
                )
            )

        # Sort: Total first, then cores by ID
        cores.sort(key=lambda c: (c.core_id != -1, c.core_id))

        return cores


class uBCPU:
    """Main application class for CPU monitoring."""

    APP_ID = "ubcpu"
    APP_NAME = "uBCPU"
    CONFIG_DIR = Path.home() / ".config" / "ubcpu"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubcpu" / "icons"

    def __init__(self):
        self.config = Config.load(self.CONFIG_FILE)
        self.cpu_monitor = CPUMonitor()
        self.cores: List[CPUCore] = []
        self.core_labels: Dict[object, Gtk.Label] = {}
        self.total_usage = 0.0
        self.menu = None
        self.current_icon = None
        self.last_critical_notification = 0
        self.notification_cooldown = 30  # seconds

        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID,
            str(self.ICONS_DIR / "cpu-normal.svg"),
            AppIndicator3.IndicatorCategory.HARDWARE,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)

        # Initial reading (will show 0% until second reading)
        self.update_cpu()
        self.build_menu()
        self.update_icon()

        # Update at configured interval
        GLib.timeout_add(self.config.update_interval_ms, self.auto_refresh)

    def get_usage_color(self, percent: float) -> str:
        """Get color based on CPU usage percentage."""
        if percent >= self.config.critical_threshold:
            return "#FF4444"  # Red
        elif percent >= self.config.warning_threshold:
            return "#FFA500"  # Orange
        else:
            return "#44FF44"  # Green

    def get_icon_name(self, percent: float) -> str:
        """Get icon name based on CPU usage."""
        if percent >= self.config.critical_threshold:
            return "cpu-critical"
        elif percent >= self.config.warning_threshold:
            return "cpu-warning"
        else:
            return "cpu-normal"

    def update_icon(self):
        """Update tray icon based on CPU usage."""
        new_icon = self.get_icon_name(self.total_usage)
        if new_icon != self.current_icon:
            icon_path = str(self.ICONS_DIR / f"{new_icon}.svg")
            if Path(icon_path).exists():
                self.indicator.set_icon_full(icon_path, "CPU Usage")
            self.current_icon = new_icon

    def update_cpu(self):
        """Update CPU usage readings."""
        self.cores = self.cpu_monitor.get_cpu_usage()

        # Find total CPU usage
        for core in self.cores:
            if core.core_id == -1:
                self.total_usage = core.usage_percent
                break

        self.check_critical_usage()

    def check_critical_usage(self):
        """Check for critical CPU usage and show notification."""
        if not self.config.show_notifications:
            return

        current_time = time.time()

        if self.total_usage >= self.config.critical_threshold:
            if (
                current_time - self.last_critical_notification
                > self.notification_cooldown
            ):
                self.show_notification(
                    "High CPU Usage Warning",
                    f"CPU usage at {self.total_usage:.1f}%",
                    is_critical=True,
                )
                self.last_critical_notification = current_time

    def show_notification(self, title: str, message: str, is_critical: bool = False):
        """Show a desktop notification."""
        try:
            urgency = "critical" if is_critical else "normal"
            subprocess.call(["notify-send", "-u", urgency, "-i", "cpu", title, message])
        except FileNotFoundError:
            pass

    def format_usage(self, percent: float) -> str:
        """Format usage percentage for display."""
        return f"{percent:.1f}%"

    def build_menu(self):
        """Build the indicator menu."""
        self.menu = Gtk.Menu()
        self.core_labels.clear()

        if not self.cores:
            item = Gtk.MenuItem(label="Reading CPU...")
            item.set_sensitive(False)
            self.menu.append(item)
        else:
            # Total CPU header
            total_core = next((c for c in self.cores if c.core_id == -1), None)
            if total_core:
                header = Gtk.MenuItem()
                label = Gtk.Label()
                color = self.get_usage_color(total_core.usage_percent)
                label.set_markup(
                    f"<b>━━ CPU Total: "
                    f"<span foreground='{color}'>{self.format_usage(total_core.usage_percent)}</span> ━━</b>"
                )
                label.set_xalign(0)
                header.add(label)
                header.set_sensitive(False)
                self.menu.append(header)
                self.core_labels[-1] = label

            self.menu.append(Gtk.SeparatorMenuItem())

            # Individual cores header
            cores_header = Gtk.MenuItem(label="━━ Cores ━━")
            cores_header.set_sensitive(False)
            self.menu.append(cores_header)

            # Individual cores
            for core in self.cores:
                if core.core_id == -1:
                    continue  # Skip total, already shown

                item = Gtk.MenuItem()
                label = Gtk.Label()
                color = self.get_usage_color(core.usage_percent)
                label.set_markup(
                    f"<span font_family='monospace'>{core.display_name:<10}</span>  "
                    f"<span foreground='{color}' weight='bold'>{self.format_usage(core.usage_percent):>6}</span>"
                )
                label.set_xalign(0)
                label.set_margin_start(5)
                label.set_margin_end(5)
                item.add(label)
                item.set_sensitive(False)
                self.menu.append(item)

                self.core_labels[core.core_id] = label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Load average
        load_item = Gtk.MenuItem()
        load_label = Gtk.Label()
        load_avg = self.get_load_average()
        load_label.set_markup(f"Load Avg: {load_avg}")
        load_label.set_xalign(0)
        load_item.add(load_label)
        load_item.set_sensitive(False)
        self.menu.append(load_item)
        self.core_labels["load"] = load_label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Refresh option
        refresh_item = Gtk.MenuItem(label="↻ Refresh Now")
        refresh_item.connect("activate", self.on_refresh)
        self.menu.append(refresh_item)

        # About
        about_item = Gtk.MenuItem(label="About uBCPU")
        about_item.connect("activate", self.on_about)
        self.menu.append(about_item)

        # Quit
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Update tray label
        self.indicator.set_label(self.format_usage(self.total_usage), "")

    def get_load_average(self) -> str:
        """Get system load average."""
        try:
            with open("/proc/loadavg", "r") as f:
                parts = f.read().split()
                if len(parts) >= 3:
                    return f"{parts[0]} {parts[1]} {parts[2]}"
                return "N/A"
        except (OSError, IOError):
            return "N/A"

    def update_labels(self):
        """Update only the label text without rebuilding menu."""
        for core in self.cores:
            label = self.core_labels.get(core.core_id)
            if label:
                color = self.get_usage_color(core.usage_percent)
                if core.core_id == -1:
                    # Total CPU
                    label.set_markup(
                        f"<b>━━ CPU Total: "
                        f"<span foreground='{color}'>{self.format_usage(core.usage_percent)}</span> ━━</b>"
                    )
                else:
                    # Individual core
                    label.set_markup(
                        f"<span font_family='monospace'>{core.display_name:<10}</span>  "
                        f"<span foreground='{color}' weight='bold'>{self.format_usage(core.usage_percent):>6}</span>"
                    )

        # Update load average
        load_label = self.core_labels.get("load")
        if load_label:
            load_avg = self.get_load_average()
            load_label.set_markup(f"Load Avg: {load_avg}")

        # Update tray label and icon
        self.indicator.set_label(self.format_usage(self.total_usage), "")
        self.update_icon()

    def auto_refresh(self) -> bool:
        """Auto-refresh callback."""
        self.update_cpu()
        self.update_labels()
        return True

    def on_refresh(self, widget):
        """Manual refresh."""
        self.update_cpu()
        self.update_labels()

    def on_about(self, widget):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("uBCPU")
        dialog.set_version("1.0.0")
        dialog.set_comments(
            "Ubuntu CPU Monitor\n\n"
            "Monitors CPU usage for all cores.\n"
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
    app = uBCPU()
    app.run()


if __name__ == "__main__":
    main()
