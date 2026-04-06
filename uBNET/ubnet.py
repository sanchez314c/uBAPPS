#!/usr/bin/python3
"""
uBNET - Ubuntu Network Monitor
A system tray application for monitoring network upload/download bandwidth on Ubuntu/Linux.
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
class InterfaceStats:
    """Represents network interface statistics."""

    interface: str
    rx_bytes: int
    tx_bytes: int
    rx_speed: float = 0.0  # bytes/sec (download)
    tx_speed: float = 0.0  # bytes/sec (upload)
    is_bridge_member: bool = (
        False  # True if enslaved to a bridge (traffic counted via bridge)
    )

    @property
    def display_name(self) -> str:
        return self.interface

    @property
    def total_speed(self) -> float:
        return self.rx_speed + self.tx_speed


@dataclass
class Config:
    """Application configuration."""

    warning_threshold_mb: float = 10.0  # MB/s
    critical_threshold_mb: float = 50.0  # MB/s
    update_interval_ms: int = 1000
    show_loopback: bool = False
    show_virtual: bool = False

    @classmethod
    def load(cls, path: Path) -> "Config":
        if path.exists():
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return cls(
                    warning_threshold_mb=data.get("warning_threshold_mb", 10.0),
                    critical_threshold_mb=data.get("critical_threshold_mb", 50.0),
                    update_interval_ms=data.get("update_interval_ms", 1000),
                    show_loopback=data.get("show_loopback", False),
                    show_virtual=data.get("show_virtual", False),
                )
            except (json.JSONDecodeError, KeyError):
                pass
        return cls()

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(
                {
                    "warning_threshold_mb": self.warning_threshold_mb,
                    "critical_threshold_mb": self.critical_threshold_mb,
                    "update_interval_ms": self.update_interval_ms,
                    "show_loopback": self.show_loopback,
                    "show_virtual": self.show_virtual,
                },
                f,
                indent=2,
            )


class NetworkMonitor:
    """Handles network I/O monitoring from /proc/net/dev."""

    def __init__(self, show_loopback: bool = False, show_virtual: bool = False):
        self.show_loopback = show_loopback
        self.show_virtual = show_virtual
        self.prev_stats: Dict[
            str, Tuple[int, int, float]
        ] = {}  # interface -> (rx, tx, time)
        self.bridge_members: set = set()  # interfaces enslaved to a bridge

    def _detect_bridge_members(self):
        """Detect interfaces enslaved to a bridge to avoid double-counting.

        When a physical interface (e.g. enp0s31f6) is a member of a bridge (e.g. br0),
        both carry identical traffic. We detect members via /sys/class/net/<iface>/master
        and exclude them from totals, counting only the bridge interface.
        """
        members = set()
        net_dir = Path("/sys/class/net")
        try:
            for iface_dir in net_dir.iterdir():
                if (iface_dir / "master").exists():
                    members.add(iface_dir.name)
        except (PermissionError, FileNotFoundError):
            pass
        self.bridge_members = members

    def get_interface_stats(self) -> List[InterfaceStats]:
        """Read network I/O from /proc/net/dev and calculate bandwidth."""
        interfaces = []
        current_time = time.time()

        # Refresh bridge membership detection each cycle
        self._detect_bridge_members()

        try:
            with open("/proc/net/dev", "r") as f:
                lines = f.readlines()
        except (PermissionError, FileNotFoundError):
            return interfaces

        for line in lines[2:]:  # Skip header lines
            parts = line.split()
            if len(parts) < 10:
                continue

            interface = parts[0].rstrip(":")

            # Filter interfaces
            if not self.show_loopback and interface == "lo":
                continue

            if not self.show_virtual:
                # Skip virtual interfaces (docker, virbr, veth, br-, etc.)
                if any(
                    interface.startswith(prefix)
                    for prefix in [
                        "docker",
                        "virbr",
                        "veth",
                        "br-",
                        "vbox",
                        "vmnet",
                        "tun",
                        "tap",
                    ]
                ):
                    continue

            try:
                # Fields: rx_bytes (index 0 after interface), tx_bytes (index 8 after interface)
                rx_bytes = int(parts[1])
                tx_bytes = int(parts[9])
            except (IndexError, ValueError):
                continue

            # Skip interfaces with no traffic ever
            if rx_bytes == 0 and tx_bytes == 0:
                continue

            # Calculate speed based on delta from previous reading
            rx_speed = 0.0
            tx_speed = 0.0

            if interface in self.prev_stats:
                prev_rx, prev_tx, prev_time = self.prev_stats[interface]
                time_delta = current_time - prev_time

                if time_delta > 0:
                    rx_speed = (rx_bytes - prev_rx) / time_delta
                    tx_speed = (tx_bytes - prev_tx) / time_delta
                    # Clamp negative values (can happen on counter reset)
                    rx_speed = max(0.0, rx_speed)
                    tx_speed = max(0.0, tx_speed)

            # Store for next calculation
            self.prev_stats[interface] = (rx_bytes, tx_bytes, current_time)

            interfaces.append(
                InterfaceStats(
                    interface=interface,
                    rx_bytes=rx_bytes,
                    tx_bytes=tx_bytes,
                    rx_speed=rx_speed,
                    tx_speed=tx_speed,
                    is_bridge_member=interface in self.bridge_members,
                )
            )

        # Sort: physical interfaces first (eth, enp, wlan, wlp), then others
        def sort_key(iface):
            name = iface.interface
            if name.startswith(("eth", "enp", "ens")):
                return (0, name)
            elif name.startswith(("wlan", "wlp", "wls")):
                return (1, name)
            else:
                return (2, name)

        interfaces.sort(key=sort_key)

        return interfaces


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


def format_bytes(total_bytes: int) -> str:
    """Format total bytes to human readable string."""
    if total_bytes >= 1024 * 1024 * 1024 * 1024:
        return f"{total_bytes / (1024 * 1024 * 1024 * 1024):.1f} TB"
    elif total_bytes >= 1024 * 1024 * 1024:
        return f"{total_bytes / (1024 * 1024 * 1024):.1f} GB"
    elif total_bytes >= 1024 * 1024:
        return f"{total_bytes / (1024 * 1024):.1f} MB"
    elif total_bytes >= 1024:
        return f"{total_bytes / 1024:.1f} KB"
    else:
        return f"{total_bytes} B"


class uBNET:
    """Main application class for network monitoring."""

    APP_ID = "ubnet"
    APP_NAME = "uBNET"
    CONFIG_DIR = Path.home() / ".config" / "ubnet"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubnet" / "icons"

    def __init__(self):
        self.config = Config.load(self.CONFIG_FILE)
        self.network_monitor = NetworkMonitor(
            show_loopback=self.config.show_loopback,
            show_virtual=self.config.show_virtual,
        )
        self.interfaces: List[InterfaceStats] = []
        self.interface_labels: Dict[str, Gtk.Label] = {}
        self.total_rx_speed = 0.0
        self.total_tx_speed = 0.0
        self.menu = None
        self.current_icon = None

        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID,
            str(self.ICONS_DIR / "net-normal.svg"),
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
        """Get total network speed in MB/s."""
        return (self.total_rx_speed + self.total_tx_speed) / (1024 * 1024)

    def get_usage_color(self, speed_mb: float) -> str:
        """Get color based on network speed."""
        if speed_mb >= self.config.critical_threshold_mb:
            return "#FF4444"  # Red
        elif speed_mb >= self.config.warning_threshold_mb:
            return "#FFA500"  # Orange
        else:
            return "#44FF44"  # Green

    def get_icon_name(self, speed_mb: float) -> str:
        """Get icon name based on network activity."""
        if speed_mb >= self.config.critical_threshold_mb:
            return "net-critical"
        elif speed_mb >= self.config.warning_threshold_mb:
            return "net-warning"
        else:
            return "net-normal"

    def update_icon(self):
        """Update tray icon based on network activity."""
        speed_mb = self.get_total_speed_mb()
        new_icon = self.get_icon_name(speed_mb)
        if new_icon != self.current_icon:
            icon_path = str(self.ICONS_DIR / f"{new_icon}.svg")
            if Path(icon_path).exists():
                self.indicator.set_icon_full(icon_path, "Network I/O")
            self.current_icon = new_icon

    def update_stats(self):
        """Update network I/O readings."""
        self.interfaces = self.network_monitor.get_interface_stats()

        # Calculate totals — exclude bridge members to avoid double-counting
        # (bridge member traffic is already reflected in the bridge interface)
        self.total_rx_speed = sum(
            i.rx_speed for i in self.interfaces if not i.is_bridge_member
        )
        self.total_tx_speed = sum(
            i.tx_speed for i in self.interfaces if not i.is_bridge_member
        )

    def build_menu(self):
        """Build the indicator menu."""
        self.menu = Gtk.Menu()
        self.interface_labels.clear()

        # Network I/O header
        header = Gtk.MenuItem()
        label = Gtk.Label()
        label.set_markup("<b>━━ Network I/O ━━</b>")
        label.set_xalign(0)
        header.add(label)
        header.set_sensitive(False)
        self.menu.append(header)

        # Total download/upload
        total_item = Gtk.MenuItem()
        total_label = Gtk.Label()
        total_label.set_markup(
            f"<span foreground='#88CC88'>▼ {format_speed(self.total_rx_speed)}</span>  "
            f"<span foreground='#CC8888'>▲ {format_speed(self.total_tx_speed)}</span>"
        )
        total_label.set_xalign(0)
        total_item.add(total_label)
        total_item.set_sensitive(False)
        self.menu.append(total_item)
        self.interface_labels["total"] = total_label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Per-interface header
        ifaces_header = Gtk.MenuItem(label="━━ Interfaces ━━")
        ifaces_header.set_sensitive(False)
        self.menu.append(ifaces_header)

        # Individual interfaces
        for iface in self.interfaces:
            item = Gtk.MenuItem()
            label = Gtk.Label()
            # Dim bridge members and annotate them since they're excluded from totals
            if iface.is_bridge_member:
                label.set_markup(
                    f"<span font_family='monospace' foreground='#888888'>{iface.interface:<12}</span>  "
                    f"<span foreground='#557755'>▼ {format_speed(iface.rx_speed):>10}</span>  "
                    f"<span foreground='#775555'>▲ {format_speed(iface.tx_speed):>10}</span>"
                    f"  <span foreground='#666666' size='small'>(bridged)</span>"
                )
            else:
                label.set_markup(
                    f"<span font_family='monospace'>{iface.interface:<12}</span>  "
                    f"<span foreground='#88CC88'>▼ {format_speed(iface.rx_speed):>10}</span>  "
                    f"<span foreground='#CC8888'>▲ {format_speed(iface.tx_speed):>10}</span>"
                )
            label.set_xalign(0)
            label.set_margin_start(5)
            label.set_margin_end(5)
            item.add(label)
            item.set_sensitive(False)
            self.menu.append(item)
            self.interface_labels[iface.interface] = label

        # Session totals
        if self.interfaces:
            self.menu.append(Gtk.SeparatorMenuItem())
            session_header = Gtk.MenuItem(label="━━ Session Totals ━━")
            session_header.set_sensitive(False)
            self.menu.append(session_header)

            for iface in self.interfaces:
                item = Gtk.MenuItem()
                label = Gtk.Label()
                if iface.is_bridge_member:
                    label.set_markup(
                        f"<span font_family='monospace' foreground='#888888'>{iface.interface:<12}</span>  "
                        f"<span foreground='#888888'>▼ {format_bytes(iface.rx_bytes)}  ▲ {format_bytes(iface.tx_bytes)}</span>"
                        f"  <span foreground='#666666' size='small'>(bridged)</span>"
                    )
                else:
                    label.set_markup(
                        f"<span font_family='monospace'>{iface.interface:<12}</span>  "
                        f"▼ {format_bytes(iface.rx_bytes)}  ▲ {format_bytes(iface.tx_bytes)}"
                    )
                label.set_xalign(0)
                label.set_margin_start(5)
                item.add(label)
                item.set_sensitive(False)
                self.menu.append(item)
                self.interface_labels[f"{iface.interface}_total"] = label

        self.menu.append(Gtk.SeparatorMenuItem())

        # Refresh option
        refresh_item = Gtk.MenuItem(label="↻ Refresh Now")
        refresh_item.connect("activate", self.on_refresh)
        self.menu.append(refresh_item)

        # About
        about_item = Gtk.MenuItem(label="About uBNET")
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
        rx = format_speed_short(self.total_rx_speed)
        tx = format_speed_short(self.total_tx_speed)
        self.indicator.set_label(f"▼{rx} ▲{tx} MB", "")

    def update_labels(self):
        """Update only the label text without rebuilding menu."""
        # Update total
        total_label = self.interface_labels.get("total")
        if total_label:
            total_label.set_markup(
                f"<span foreground='#88CC88'>▼ {format_speed(self.total_rx_speed)}</span>  "
                f"<span foreground='#CC8888'>▲ {format_speed(self.total_tx_speed)}</span>"
            )

        # Update individual interfaces
        for iface in self.interfaces:
            label = self.interface_labels.get(iface.interface)
            if label:
                if iface.is_bridge_member:
                    label.set_markup(
                        f"<span font_family='monospace' foreground='#888888'>{iface.interface:<12}</span>  "
                        f"<span foreground='#557755'>▼ {format_speed(iface.rx_speed):>10}</span>  "
                        f"<span foreground='#775555'>▲ {format_speed(iface.tx_speed):>10}</span>"
                        f"  <span foreground='#666666' size='small'>(bridged)</span>"
                    )
                else:
                    label.set_markup(
                        f"<span font_family='monospace'>{iface.interface:<12}</span>  "
                        f"<span foreground='#88CC88'>▼ {format_speed(iface.rx_speed):>10}</span>  "
                        f"<span foreground='#CC8888'>▲ {format_speed(iface.tx_speed):>10}</span>"
                    )

            # Update session totals
            total_label = self.interface_labels.get(f"{iface.interface}_total")
            if total_label:
                total_label.set_markup(
                    f"<span font_family='monospace'>{iface.interface:<12}</span>  "
                    f"▼ {format_bytes(iface.rx_bytes)}  ▲ {format_bytes(iface.tx_bytes)}"
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
        dialog.set_program_name("uBNET")
        dialog.set_version("1.1.0")
        dialog.set_comments(
            "Ubuntu Network Monitor\n\n"
            "Monitors network upload/download bandwidth.\n"
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
    app = uBNET()
    app.run()


if __name__ == "__main__":
    main()
