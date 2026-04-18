#!/usr/bin/env python3
"""
uBTIME - Ubuntu World Clock
A system tray application for viewing times across all timezones.
"""

import gi

gi.require_version("Gtk", "3.0")
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
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List
import json
import subprocess
from zoneinfo import ZoneInfo, available_timezones


@dataclass
class TimezoneInfo:
    """Represents a timezone with its current time."""

    zone_id: str  # e.g., "America/New_York"
    region: str  # e.g., "America"
    city: str  # e.g., "New York"

    def get_current_time(self, use_24h: bool = True) -> str:
        """Get current time in this timezone."""
        try:
            tz = ZoneInfo(self.zone_id)
            now = datetime.now(tz)
            if use_24h:
                return now.strftime("%H:%M:%S")
            else:
                return now.strftime("%I:%M:%S %p")
        except (KeyError, ValueError, OSError):
            return "--:--:--"

    def get_current_datetime(self, use_24h: bool = True) -> str:
        """Get current date and time in this timezone."""
        try:
            tz = ZoneInfo(self.zone_id)
            now = datetime.now(tz)
            if use_24h:
                return now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return now.strftime("%Y-%m-%d %I:%M:%S %p")
        except (KeyError, ValueError, OSError):
            return "----"

    def get_offset(self) -> str:
        """Get UTC offset string."""
        try:
            tz = ZoneInfo(self.zone_id)
            now = datetime.now(tz)
            offset = now.strftime("%z")
            # Format as UTC+HH:MM
            if offset:
                return f"UTC{offset[:3]}:{offset[3:]}"
            return "UTC"
        except (KeyError, ValueError, OSError):
            return "UTC"


class Config:
    """Configuration manager for uBTIME."""

    CONFIG_DIR = Path.home() / ".config" / "ubtime"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        self.use_24h: bool = True
        self.favorites: List[str] = [
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney",
            "UTC",
        ]
        self.show_seconds: bool = True
        self.load()

    def load(self):
        """Load configuration from file."""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.use_24h = data.get("use_24h", True)
                    self.favorites = data.get("favorites", self.favorites)
                    self.show_seconds = data.get("show_seconds", True)
        except (json.JSONDecodeError, OSError, IOError, KeyError):
            pass

    def save(self):
        """Save configuration to file."""
        try:
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(
                    {
                        "use_24h": self.use_24h,
                        "favorites": self.favorites,
                        "show_seconds": self.show_seconds,
                    },
                    f,
                    indent=2,
                )
        except (OSError, IOError):
            pass


class TimezoneManager:
    """Manages timezone information."""

    # Region display order
    REGION_ORDER = [
        "Favorites",
        "UTC",
        "America",
        "Europe",
        "Asia",
        "Africa",
        "Australia",
        "Pacific",
        "Atlantic",
        "Indian",
        "Antarctica",
        "Arctic",
        "Etc",
    ]

    @staticmethod
    def get_all_timezones() -> List[TimezoneInfo]:
        """Get all available timezones."""
        timezones = []

        for zone_id in sorted(available_timezones()):
            # Skip some special zones
            if zone_id.startswith(("posix/", "right/")):
                continue

            parts = zone_id.split("/")
            if len(parts) >= 2:
                region = parts[0]
                city = "/".join(parts[1:]).replace("_", " ")
            else:
                region = "Other"
                city = zone_id.replace("_", " ")

            timezones.append(TimezoneInfo(zone_id=zone_id, region=region, city=city))

        return timezones

    @staticmethod
    def get_timezones_by_region(
        timezones: List[TimezoneInfo],
    ) -> Dict[str, List[TimezoneInfo]]:
        """Group timezones by region."""
        by_region: Dict[str, List[TimezoneInfo]] = {}

        for tz in timezones:
            if tz.region not in by_region:
                by_region[tz.region] = []
            by_region[tz.region].append(tz)

        # Sort cities within each region
        for region in by_region:
            by_region[region].sort(key=lambda t: t.city)

        return by_region


class UBTimeApp:
    """Main application class."""

    APP_ID = "com.ubtime.indicator"
    APP_NAME = "uBTIME"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubtime" / "icons"

    def __init__(self):
        self.config = Config()
        self.all_timezones = TimezoneManager.get_all_timezones()
        self.by_region = TimezoneManager.get_timezones_by_region(self.all_timezones)

        self.menu = None
        self.time_labels: Dict[str, Gtk.MenuItem] = {}
        self.local_time_item = None

        # Create indicator
        icon_path = str(self.ICONS_DIR / "clock.svg")
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID, icon_path, AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)

        self.build_menu()
        self.update_times()

        # Update every second
        GLib.timeout_add(1000, self.auto_refresh)

    def get_local_time_display(self) -> str:
        """Get local time for tray display."""
        now = datetime.now()
        if self.config.use_24h:
            if self.config.show_seconds:
                return now.strftime("%H:%M:%S")
            return now.strftime("%H:%M")
        else:
            if self.config.show_seconds:
                return now.strftime("%I:%M:%S %p")
            return now.strftime("%I:%M %p")

    def build_menu(self):
        """Build the dropdown menu."""
        self.menu = Gtk.Menu()
        self.time_labels = {}

        # Local time header
        self.local_time_item = Gtk.MenuItem()
        local_label = Gtk.Label()
        local_label.set_markup(f"<b>Local: {self.get_local_time_display()}</b>")
        local_label.set_halign(Gtk.Align.START)
        self.local_time_item.add(local_label)
        self.local_time_item.set_sensitive(False)
        self.menu.append(self.local_time_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Favorites section
        if self.config.favorites:
            fav_header = Gtk.MenuItem(label="── Favorites ──")
            fav_header.set_sensitive(False)
            self.menu.append(fav_header)

            for zone_id in self.config.favorites:
                tz_info = next(
                    (t for t in self.all_timezones if t.zone_id == zone_id), None
                )
                if tz_info:
                    self._add_timezone_item(tz_info)

            self.menu.append(Gtk.SeparatorMenuItem())

        # All timezones submenu
        all_tz_item = Gtk.MenuItem(label="All Timezones")
        all_tz_menu = Gtk.Menu()
        all_tz_item.set_submenu(all_tz_menu)

        # Add regions in order
        for region in TimezoneManager.REGION_ORDER:
            if region in self.by_region and region != "Favorites":
                self._add_region_submenu(all_tz_menu, region, self.by_region[region])

        # Add any remaining regions
        for region in sorted(self.by_region.keys()):
            if region not in TimezoneManager.REGION_ORDER:
                self._add_region_submenu(all_tz_menu, region, self.by_region[region])

        self.menu.append(all_tz_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Settings
        time_format_item = Gtk.MenuItem(
            label=f"Switch to {'12h' if self.config.use_24h else '24h'} format"
        )
        time_format_item.connect("activate", self.toggle_time_format)
        self.menu.append(time_format_item)

        seconds_item = Gtk.MenuItem(
            label=f"{'Hide' if self.config.show_seconds else 'Show'} seconds"
        )
        seconds_item.connect("activate", self.toggle_seconds)
        self.menu.append(seconds_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # About
        about_item = Gtk.MenuItem(label="About uBTIME")
        about_item.connect("activate", self.show_about)
        self.menu.append(about_item)

        # Quit
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_app)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def _add_region_submenu(
        self, parent_menu: Gtk.Menu, region: str, timezones: List[TimezoneInfo]
    ):
        """Add a region submenu with its timezones."""
        region_item = Gtk.MenuItem(label=region)
        region_menu = Gtk.Menu()
        region_item.set_submenu(region_menu)

        for tz in timezones:
            self._add_timezone_item(tz, parent_menu=region_menu)

        parent_menu.append(region_item)

    def _add_timezone_item(
        self,
        tz_info: TimezoneInfo,
        parent_menu: Gtk.Menu = None,
    ):
        """Add a timezone menu item."""
        menu = parent_menu if parent_menu else self.menu

        item = Gtk.MenuItem()

        # Create label with city and time
        time_str = tz_info.get_current_time(self.config.use_24h)
        offset = tz_info.get_offset()

        label = Gtk.Label()
        display_name = tz_info.city
        label.set_markup(
            f"{display_name}  <span foreground='#888888'>{offset}</span>  <b>{time_str}</b>"
        )
        label.set_halign(Gtk.Align.START)
        item.add(label)

        # Right-click to add/remove from favorites
        item.connect(
            "button-press-event",
            lambda w, e, z=tz_info: self.on_timezone_click(w, e, z),
        )

        menu.append(item)

        # Track for updates
        self.time_labels[tz_info.zone_id] = item

    def on_timezone_click(self, widget, event, tz_info: TimezoneInfo):
        """Handle click on timezone item."""
        if event.button == 3:  # Right click
            if tz_info.zone_id in self.config.favorites:
                self.config.favorites.remove(tz_info.zone_id)
                self.show_notification(f"Removed {tz_info.city} from favorites")
            else:
                self.config.favorites.append(tz_info.zone_id)
                self.show_notification(f"Added {tz_info.city} to favorites")
            self.config.save()
            self.build_menu()
        elif event.button == 1:  # Left click - copy to clipboard
            time_str = tz_info.get_current_datetime(self.config.use_24h)
            clipboard = Gtk.Clipboard.get_default(widget.get_display())
            clipboard.set_text(f"{tz_info.zone_id}: {time_str}", -1)
            self.show_notification(f"Copied {tz_info.city} time to clipboard")

    def show_notification(self, message: str):
        """Show a desktop notification."""
        try:
            subprocess.run(
                ["notify-send", self.APP_NAME, message, "-t", "2000"],
                capture_output=True,
            )
        except FileNotFoundError:
            pass

    def update_times(self):
        """Update all time displays."""
        # Update tray label
        self.indicator.set_label(self.get_local_time_display(), "")

        # Update local time header
        if self.local_time_item:
            for child in self.local_time_item.get_children():
                if isinstance(child, Gtk.Label):
                    child.set_markup(f"<b>Local: {self.get_local_time_display()}</b>")

        # Update timezone labels
        for zone_id, item in self.time_labels.items():
            tz_info = next(
                (t for t in self.all_timezones if t.zone_id == zone_id), None
            )
            if tz_info:
                for child in item.get_children():
                    if isinstance(child, Gtk.Label):
                        time_str = tz_info.get_current_time(self.config.use_24h)
                        offset = tz_info.get_offset()
                        child.set_markup(
                            f"{tz_info.city}  <span foreground='#888888'>{offset}</span>  <b>{time_str}</b>"
                        )

    def auto_refresh(self) -> bool:
        """Auto-refresh callback."""
        self.update_times()
        return True

    def toggle_time_format(self, widget):
        """Toggle between 12h and 24h format."""
        self.config.use_24h = not self.config.use_24h
        self.config.save()
        self.build_menu()

    def toggle_seconds(self, widget):
        """Toggle showing seconds."""
        self.config.show_seconds = not self.config.show_seconds
        self.config.save()
        self.build_menu()

    def show_about(self, widget):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(self.APP_NAME)
        dialog.set_version("1.0.0")
        dialog.set_comments("World clock for Ubuntu\nView times across all timezones")
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.set_website("https://github.com/sanchez314c/uBAPPS")
        dialog.run()
        dialog.destroy()

    def quit_app(self, widget):
        """Quit the application."""
        Gtk.main_quit()

    def run(self):
        """Run the application."""
        Gtk.main()


def main():
    app = UBTimeApp()
    app.run()


if __name__ == "__main__":
    main()
