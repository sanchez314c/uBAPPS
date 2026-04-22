#!/usr/bin/env python3
"""
uBWEAT - Ubuntu Weather
A system tray application for displaying local weather and temperature.
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
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import urllib.request
import urllib.error
import urllib.parse
import subprocess
import threading


@dataclass
class WeatherData:
    """Weather information."""

    location: str
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    feels_like_f: float
    condition: str
    condition_code: int
    humidity: int
    wind_speed_kmh: float
    wind_speed_mph: float
    wind_dir: str
    pressure_mb: float
    visibility_km: float
    uv_index: float
    cloud_cover: int
    last_updated: str

    @classmethod
    def from_wttr(cls, data: Dict[str, Any], location: str) -> "WeatherData":
        """Create WeatherData from wttr.in response."""
        current = data.get("current_condition", [{}])[0]

        return cls(
            location=location,
            temperature_c=float(current.get("temp_C", 0)),
            temperature_f=float(current.get("temp_F", 32)),
            feels_like_c=float(current.get("FeelsLikeC", 0)),
            feels_like_f=float(current.get("FeelsLikeF", 32)),
            condition=current.get("weatherDesc", [{"value": "Unknown"}])[0].get(
                "value", "Unknown"
            ),
            condition_code=int(current.get("weatherCode", 0)),
            humidity=int(current.get("humidity", 0)),
            wind_speed_kmh=float(current.get("windspeedKmph", 0)),
            wind_speed_mph=float(current.get("windspeedMiles", 0)),
            wind_dir=current.get("winddir16Point", "N"),
            pressure_mb=float(current.get("pressure", 0)),
            visibility_km=float(current.get("visibility", 0)),
            uv_index=float(current.get("uvIndex", 0)),
            cloud_cover=int(current.get("cloudcover", 0)),
            last_updated=current.get("observation_time", ""),
        )


class Config:
    """Configuration manager for uBWEAT."""

    CONFIG_DIR = Path.home() / ".config" / "ubweat"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        self.use_fahrenheit: bool = False
        self.location: str = ""  # Empty = auto-detect
        self.refresh_minutes: int = 10
        self.show_condition: bool = True
        self.load()

    def load(self):
        """Load configuration from file."""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.use_fahrenheit = data.get("use_fahrenheit", False)
                    self.location = data.get("location", "")
                    self.refresh_minutes = data.get("refresh_minutes", 10)
                    self.show_condition = data.get("show_condition", True)

                    # Migration: location must be 5-digit US ZIP or empty (auto-detect).
                    # Legacy city-name values are cleared so next fetch uses IP auto-detect.
                    if self.location and not (
                        self.location.isdigit() and len(self.location) == 5
                    ):
                        self.location = ""
                        self.save()
        except (json.JSONDecodeError, OSError, IOError, KeyError):
            pass

    def save(self):
        """Save configuration to file."""
        try:
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(
                    {
                        "use_fahrenheit": self.use_fahrenheit,
                        "location": self.location,
                        "refresh_minutes": self.refresh_minutes,
                        "show_condition": self.show_condition,
                    },
                    f,
                    indent=2,
                )
        except (OSError, IOError):
            pass


class WeatherService:
    """Fetches weather data from wttr.in."""

    @staticmethod
    def get_weather(location: str = "") -> Optional[WeatherData]:
        """Fetch weather data for location (empty = auto-detect by IP)."""
        try:
            # wttr.in API - free, no key required
            loc = urllib.parse.quote(location, safe="") if location else ""
            url = f"https://wttr.in/{loc}?format=j1"

            req = urllib.request.Request(
                url, headers={"User-Agent": "uBWEAT/1.0", "Accept": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

                if not isinstance(data, dict):
                    return None

                # Get location name from response
                nearest = data.get("nearest_area", [{}])[0]
                area = nearest.get("areaName", [{"value": "Unknown"}])[0].get(
                    "value", "Unknown"
                )
                country = nearest.get("country", [{"value": ""}])[0].get("value", "")
                loc_name = f"{area}, {country}" if country else area

                return WeatherData.from_wttr(data, loc_name)

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            json.JSONDecodeError,
            OSError,
            ValueError,
            KeyError,
            IndexError,
            TypeError,
        ) as e:
            print(f"Weather fetch error: {e}")
            return None


class UBWeatApp:
    """Main application class."""

    APP_ID = "com.ubweat.indicator"
    APP_NAME = "uBWEAT"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubweat" / "icons"

    # Weather condition to icon mapping
    CONDITION_ICONS = {
        "sunny": "weather-sunny",
        "clear": "weather-sunny",
        "partly cloudy": "weather-cloudy",
        "cloudy": "weather-cloudy",
        "overcast": "weather-cloudy",
        "mist": "weather-fog",
        "fog": "weather-fog",
        "rain": "weather-rain",
        "light rain": "weather-rain",
        "heavy rain": "weather-rain",
        "drizzle": "weather-rain",
        "shower": "weather-rain",
        "thunderstorm": "weather-storm",
        "thunder": "weather-storm",
        "snow": "weather-snow",
        "light snow": "weather-snow",
        "heavy snow": "weather-snow",
        "sleet": "weather-snow",
        "blizzard": "weather-snow",
    }

    def __init__(self):
        self.config = Config()
        self.weather: Optional[WeatherData] = None
        self.menu = None
        self.weather_items: Dict[str, Gtk.MenuItem] = {}
        self.fetching = False

        # Create indicator
        icon_path = str(self.ICONS_DIR / "weather-sunny.svg")
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID, icon_path, AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)
        self.indicator.set_label("--°", "999°F")

        self.build_menu()

        # Initial fetch
        self.fetch_weather_async()

        # Refresh timer (default 10 minutes)
        GLib.timeout_add(self.config.refresh_minutes * 60 * 1000, self.auto_refresh)

    def get_icon_for_condition(self, condition: str) -> str:
        """Get icon name based on weather condition."""
        condition_lower = condition.lower()
        for key, icon in self.CONDITION_ICONS.items():
            if key in condition_lower:
                return icon
        return "weather-sunny"

    def get_temp_display(self) -> str:
        """Get temperature string for display."""
        if not self.weather:
            return "--°"

        if self.config.use_fahrenheit:
            return f"{int(self.weather.temperature_f)}°F"
        else:
            return f"{int(self.weather.temperature_c)}°C"

    def build_menu(self):
        """Build the dropdown menu."""
        self.menu = Gtk.Menu()
        self.weather_items = {}

        # Location header
        loc_item = Gtk.MenuItem()
        loc_label = Gtk.Label()
        if self.weather:
            loc_label.set_markup(f"<b>{self.weather.location}</b>")
        else:
            loc_label.set_markup("<b>Loading...</b>")
        loc_label.set_halign(Gtk.Align.START)
        loc_item.add(loc_label)
        loc_item.set_sensitive(False)
        self.menu.append(loc_item)
        self.weather_items["location"] = loc_item

        self.menu.append(Gtk.SeparatorMenuItem())

        # Temperature
        temp_item = Gtk.MenuItem()
        temp_label = Gtk.Label()
        temp_label.set_halign(Gtk.Align.START)
        temp_item.add(temp_label)
        temp_item.set_sensitive(False)
        self.menu.append(temp_item)
        self.weather_items["temperature"] = temp_item

        # Feels like
        feels_item = Gtk.MenuItem()
        feels_label = Gtk.Label()
        feels_label.set_halign(Gtk.Align.START)
        feels_item.add(feels_label)
        feels_item.set_sensitive(False)
        self.menu.append(feels_item)
        self.weather_items["feels_like"] = feels_item

        # Condition
        cond_item = Gtk.MenuItem()
        cond_label = Gtk.Label()
        cond_label.set_halign(Gtk.Align.START)
        cond_item.add(cond_label)
        cond_item.set_sensitive(False)
        self.menu.append(cond_item)
        self.weather_items["condition"] = cond_item

        self.menu.append(Gtk.SeparatorMenuItem())

        # Humidity
        humid_item = Gtk.MenuItem()
        humid_label = Gtk.Label()
        humid_label.set_halign(Gtk.Align.START)
        humid_item.add(humid_label)
        humid_item.set_sensitive(False)
        self.menu.append(humid_item)
        self.weather_items["humidity"] = humid_item

        # Wind
        wind_item = Gtk.MenuItem()
        wind_label = Gtk.Label()
        wind_label.set_halign(Gtk.Align.START)
        wind_item.add(wind_label)
        wind_item.set_sensitive(False)
        self.menu.append(wind_item)
        self.weather_items["wind"] = wind_item

        # Pressure
        press_item = Gtk.MenuItem()
        press_label = Gtk.Label()
        press_label.set_halign(Gtk.Align.START)
        press_item.add(press_label)
        press_item.set_sensitive(False)
        self.menu.append(press_item)
        self.weather_items["pressure"] = press_item

        # UV Index
        uv_item = Gtk.MenuItem()
        uv_label = Gtk.Label()
        uv_label.set_halign(Gtk.Align.START)
        uv_item.add(uv_label)
        uv_item.set_sensitive(False)
        self.menu.append(uv_item)
        self.weather_items["uv"] = uv_item

        self.menu.append(Gtk.SeparatorMenuItem())

        # Last updated
        updated_item = Gtk.MenuItem()
        updated_label = Gtk.Label()
        updated_label.set_halign(Gtk.Align.START)
        updated_item.add(updated_label)
        updated_item.set_sensitive(False)
        self.menu.append(updated_item)
        self.weather_items["updated"] = updated_item

        self.menu.append(Gtk.SeparatorMenuItem())

        # Refresh
        refresh_item = Gtk.MenuItem(label="↻ Refresh Now")
        refresh_item.connect("activate", lambda w: self.fetch_weather_async())
        self.menu.append(refresh_item)

        # Toggle units
        units_item = Gtk.MenuItem(
            label=f"Switch to {'°C' if self.config.use_fahrenheit else '°F'}"
        )
        units_item.connect("activate", self.toggle_units)
        self.menu.append(units_item)

        # Set location
        location_item = Gtk.MenuItem(label="Set Location...")
        location_item.connect("activate", self.set_location_dialog)
        self.menu.append(location_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # About
        about_item = Gtk.MenuItem(label="About uBWEAT")
        about_item.connect("activate", self.show_about)
        self.menu.append(about_item)

        # Quit
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_app)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Update display
        self.update_display()

    def update_display(self):
        """Update all weather displays."""
        if not self.weather:
            self.indicator.set_label("--°", "999°F")
            return

        # Update tray
        self.indicator.set_label(self.get_temp_display(), "999°F")

        # Update icon
        icon_name = self.get_icon_for_condition(self.weather.condition)
        icon_path = str(self.ICONS_DIR / f"{icon_name}.svg")
        self.indicator.set_icon_full(icon_path, self.weather.condition)

        # Update menu items
        w = self.weather
        use_f = self.config.use_fahrenheit

        def set_label(key: str, text: str):
            item = self.weather_items.get(key)
            if item:
                for child in item.get_children():
                    if isinstance(child, Gtk.Label):
                        child.set_markup(text)

        set_label("location", f"<b>{w.location}</b>")

        if use_f:
            set_label("temperature", f"Temperature: <b>{int(w.temperature_f)}°F</b>")
            set_label("feels_like", f"Feels like: {int(w.feels_like_f)}°F")
            set_label("wind", f"Wind: {w.wind_dir} {int(w.wind_speed_mph)} mph")
        else:
            set_label("temperature", f"Temperature: <b>{int(w.temperature_c)}°C</b>")
            set_label("feels_like", f"Feels like: {int(w.feels_like_c)}°C")
            set_label("wind", f"Wind: {w.wind_dir} {int(w.wind_speed_kmh)} km/h")

        set_label("condition", f"Condition: {w.condition}")
        set_label("humidity", f"Humidity: {w.humidity}%")
        set_label("pressure", f"Pressure: {int(w.pressure_mb)} mb")
        set_label("uv", f"UV Index: {int(w.uv_index)}")
        set_label("updated", f"<small>Updated: {w.last_updated}</small>")

    def fetch_weather_async(self):
        """Fetch weather in background thread."""
        if self.fetching:
            return

        self.fetching = True

        def fetch():
            weather = WeatherService.get_weather(self.config.location)
            GLib.idle_add(self.on_weather_fetched, weather)

        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    def on_weather_fetched(self, weather: Optional[WeatherData]):
        """Called when weather data is fetched."""
        self.fetching = False

        if weather:
            self.weather = weather
            self.update_display()
        else:
            self.show_notification("Failed to fetch weather data")

    def auto_refresh(self) -> bool:
        """Auto-refresh callback."""
        self.fetch_weather_async()
        return True

    def toggle_units(self, widget):
        """Toggle between Celsius and Fahrenheit."""
        self.config.use_fahrenheit = not self.config.use_fahrenheit
        self.config.save()
        self.build_menu()

    def set_location_dialog(self, widget):
        """Show dialog to set location — US ZIP code or leave empty for auto-detect by IP."""
        dialog = Gtk.Dialog(title="Set Location", flags=Gtk.DialogFlags.MODAL)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.set_default_size(340, 140)

        content = dialog.get_content_area()
        content.set_spacing(10)
        content.set_margin_start(12)
        content.set_margin_end(12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)

        label = Gtk.Label(label="Enter US ZIP code (leave empty for auto-detect by IP):")
        label.set_halign(Gtk.Align.START)
        label.set_line_wrap(True)
        content.add(label)

        entry = Gtk.Entry()
        entry.set_text(self.config.location)
        entry.set_placeholder_text("e.g., 28117")
        entry.set_max_length(5)
        entry.set_width_chars(10)
        content.add(entry)

        hint = Gtk.Label()
        hint.set_markup(
            "<small>Empty = auto-detect via IP geolocation. "
            "ZIP is most precise for US locations.</small>"
        )
        hint.set_halign(Gtk.Align.START)
        hint.set_line_wrap(True)
        content.add(hint)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            value = entry.get_text().strip()
            if value and not (value.isdigit() and len(value) == 5):
                err = Gtk.MessageDialog(
                    transient_for=dialog,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Invalid ZIP code",
                )
                err.format_secondary_text(
                    "Enter exactly 5 digits (e.g., 28117), or leave blank for auto-detect."
                )
                err.run()
                err.destroy()
            else:
                self.config.location = value
                self.config.save()
                self.fetch_weather_async()

        dialog.destroy()

    def show_notification(self, message: str):
        """Show a desktop notification."""
        try:
            subprocess.run(
                ["notify-send", self.APP_NAME, message, "-t", "3000"],
                capture_output=True,
            )
        except FileNotFoundError:
            pass

    def show_about(self, widget):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(self.APP_NAME)
        dialog.set_version("1.0.0")
        dialog.set_comments("Weather monitor for Ubuntu\nPowered by wttr.in")
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
    app = UBWeatApp()
    app.run()


if __name__ == "__main__":
    main()
