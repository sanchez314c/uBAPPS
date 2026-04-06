#!/usr/bin/env python3
"""
uBRES - Ubuntu Resolution Switcher
A system tray application for quick display resolution switching on Ubuntu/Linux.
Inspired by RDM for macOS.
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
import subprocess
import re
import sys
from math import gcd


class Display:
    """Represents a connected display with its available resolutions."""

    def __init__(self, name, is_primary=False):
        self.name = name
        self.is_primary = is_primary
        self.resolutions = []  # List of (width, height, refresh_rates, is_current)
        self.current_resolution = None
        self.current_refresh = None


class ResolutionManager:
    """Handles xrandr queries and resolution changes."""

    @staticmethod
    def get_displays():
        """Parse xrandr output to get all connected displays and their resolutions."""
        displays = []

        try:
            output = subprocess.check_output(
                ["xrandr", "--query"], stderr=subprocess.STDOUT, universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running xrandr: {e}")
            return displays
        except FileNotFoundError:
            print("xrandr not found. Please install x11-xserver-utils.")
            return displays

        current_display = None

        for line in output.split("\n"):
            # Match display line: "HDMI-1 connected primary 1920x1080+0+0 ..."
            display_match = re.match(
                r"^(\S+)\s+connected\s*(primary)?\s*(?:(\d+)x(\d+)\+\d+\+\d+)?", line
            )

            if display_match:
                name = display_match.group(1)
                is_primary = display_match.group(2) is not None
                current_display = Display(name, is_primary)
                displays.append(current_display)

                # If resolution is shown on this line, it's the current one
                if display_match.group(3) and display_match.group(4):
                    current_display.current_resolution = (
                        int(display_match.group(3)),
                        int(display_match.group(4)),
                    )
                continue

            # Match resolution line: "   1920x1080     60.00*+  59.94  "
            if current_display and line.startswith("   "):
                res_match = re.match(r"^\s+(\d+)x(\d+)\s+([\d\.\s\*\+]+)", line)

                if res_match:
                    width = int(res_match.group(1))
                    height = int(res_match.group(2))
                    refresh_str = res_match.group(3)

                    # Parse refresh rates
                    refresh_rates = []
                    is_current = False
                    current_refresh = None

                    for rate in re.findall(r"([\d\.]+)([\*\+]*)", refresh_str):
                        refresh = float(rate[0])
                        flags = rate[1]
                        refresh_rates.append(refresh)

                        if "*" in flags:
                            is_current = True
                            current_refresh = refresh
                            current_display.current_resolution = (width, height)
                            current_display.current_refresh = refresh

                    if refresh_rates:
                        current_display.resolutions.append(
                            {
                                "width": width,
                                "height": height,
                                "refresh_rates": refresh_rates,
                                "is_current": is_current,
                                "current_refresh": current_refresh,
                            }
                        )

        return displays

    @staticmethod
    def set_resolution(display_name, width, height, refresh=None):
        """Set the resolution for a display using xrandr."""
        mode = f"{width}x{height}"
        cmd = ["xrandr", "--output", display_name, "--mode", mode]

        if refresh:
            cmd.extend(["--rate", str(refresh)])

        try:
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting resolution: {e}")
            return False


class uBRES:
    """Main application class for the system tray resolution switcher."""

    APP_ID = "ubres"
    APP_NAME = "uBRES"

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID,
            "video-display",
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)

        self.build_menu()

        # Auto-refresh every 5 seconds to detect display changes
        GLib.timeout_add_seconds(5, self.auto_refresh)

    def build_menu(self):
        """Build the indicator menu with all displays and resolutions."""
        menu = Gtk.Menu()

        displays = ResolutionManager.get_displays()

        if not displays:
            item = Gtk.MenuItem(label="No displays detected")
            item.set_sensitive(False)
            menu.append(item)
        else:
            for display in displays:
                # Display header
                display_label = display.name
                if display.is_primary:
                    display_label += " (Primary)"

                header = Gtk.MenuItem(label=f"── {display_label} ──")
                header.set_sensitive(False)
                menu.append(header)

                # Group resolutions by aspect ratio for cleaner display
                for res in display.resolutions:
                    width = res["width"]
                    height = res["height"]
                    is_current = res["is_current"]

                    # Calculate aspect ratio
                    divisor = gcd(width, height)
                    aspect_w = width // divisor
                    aspect_h = height // divisor

                    # Common aspect ratio names
                    aspect_name = ""
                    if (aspect_w, aspect_h) == (16, 9):
                        aspect_name = "16:9"
                    elif (aspect_w, aspect_h) == (16, 10):
                        aspect_name = "16:10"
                    elif (aspect_w, aspect_h) == (4, 3):
                        aspect_name = "4:3"
                    elif (aspect_w, aspect_h) == (21, 9) or (aspect_w, aspect_h) == (
                        64,
                        27,
                    ):
                        aspect_name = "21:9"
                    else:
                        aspect_name = f"{aspect_w}:{aspect_h}"

                    # Build label
                    label = f"  {width} × {height}"

                    # Add refresh rate info
                    if res["refresh_rates"]:
                        primary_refresh = res["refresh_rates"][0]
                        label += f"  @{primary_refresh:.0f}Hz"

                    # Add aspect ratio
                    label += f"  [{aspect_name}]"

                    # Mark current resolution
                    if is_current:
                        label = (
                            "✓ " + label[2:]
                        )  # Replace leading spaces with checkmark

                    item = Gtk.MenuItem(label=label)

                    if not is_current:
                        # Connect click handler
                        item.connect(
                            "activate",
                            self.on_resolution_selected,
                            display.name,
                            width,
                            height,
                            res["refresh_rates"][0] if res["refresh_rates"] else None,
                        )
                    else:
                        item.set_sensitive(False)

                    menu.append(item)

                # Add separator between displays
                menu.append(Gtk.SeparatorMenuItem())

        # Refresh option
        refresh_item = Gtk.MenuItem(label="↻ Refresh Displays")
        refresh_item.connect("activate", self.on_refresh)
        menu.append(refresh_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # About
        about_item = Gtk.MenuItem(label="About uBRES")
        about_item.connect("activate", self.on_about)
        menu.append(about_item)

        # Quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def on_resolution_selected(self, widget, display_name, width, height, refresh):
        """Handle resolution selection."""
        success = ResolutionManager.set_resolution(display_name, width, height, refresh)

        if success:
            # Rebuild menu to reflect new current resolution
            self.build_menu()
            self.show_notification(
                "Resolution Changed", f"{display_name}: {width}×{height}"
            )
        else:
            self.show_notification(
                "Error", f"Failed to set resolution {width}×{height}", is_error=True
            )

    def on_refresh(self, widget):
        """Manually refresh the display list."""
        self.build_menu()

    def auto_refresh(self):
        """Auto-refresh callback for detecting display changes."""
        self.build_menu()
        return True  # Continue the timeout

    def show_notification(self, title, message, is_error=False):
        """Show a desktop notification."""
        try:
            icon = "dialog-error" if is_error else "video-display"
            subprocess.call(["notify-send", "-i", icon, title, message])
        except FileNotFoundError:
            pass  # notify-send not available

    def on_about(self, widget):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("uBRES")
        dialog.set_version("1.0.0")
        dialog.set_comments(
            "Ubuntu Resolution Switcher\n\nA quick resolution changer for Ubuntu/Linux.\nInspired by RDM for macOS."
        )
        dialog.set_website("https://github.com/avibrazil/RDM")
        dialog.set_website_label("Inspired by RDM")
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
    # Check for required dependencies
    try:
        subprocess.check_output(["which", "xrandr"], stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: xrandr is required but not installed.")
        print("Install it with: sudo apt install x11-xserver-utils")
        sys.exit(1)

    app = uBRES()
    app.run()


if __name__ == "__main__":
    main()
