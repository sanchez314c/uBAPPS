#!/usr/bin/env python3
"""
uBTEMP - Ubuntu Temperature Monitor
A system tray application for monitoring hardware temperatures on Ubuntu/Linux.
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
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
import time as _time


class SensorType(Enum):
    """Categories for sensor types."""

    CPU = "CPU"
    GPU = "GPU"
    NVME = "NVMe/SSD"
    HDD = "HDD"
    RAID = "RAID Controller"
    MOTHERBOARD = "Motherboard"
    OTHER = "Other"


@dataclass
class Sensor:
    """Represents a temperature sensor."""

    chip_id: str
    sensor_id: str
    adapter: str
    temperature: float
    high_threshold: Optional[float] = None
    critical_threshold: Optional[float] = None
    sensor_type: SensorType = SensorType.OTHER

    @property
    def unique_id(self) -> str:
        return f"{self.chip_id}::{self.sensor_id}"


@dataclass
class Config:
    """Application configuration."""

    use_fahrenheit: bool = False
    custom_names: Dict[str, str] = field(default_factory=dict)
    warning_threshold: float = 70.0
    critical_threshold: float = 85.0
    show_notifications: bool = True

    @classmethod
    def load(cls, path: Path) -> "Config":
        if path.exists():
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return cls(
                    use_fahrenheit=data.get("use_fahrenheit", False),
                    custom_names=data.get("custom_names", {}),
                    warning_threshold=data.get("warning_threshold", 70.0),
                    critical_threshold=data.get("critical_threshold", 85.0),
                    show_notifications=data.get("show_notifications", True),
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
                        "use_fahrenheit": self.use_fahrenheit,
                        "custom_names": self.custom_names,
                        "warning_threshold": self.warning_threshold,
                        "critical_threshold": self.critical_threshold,
                        "show_notifications": self.show_notifications,
                    },
                    f,
                    indent=2,
                )
        except (OSError, IOError):
            pass


class SensorManager:
    """Handles sensor discovery and reading from ALL sources."""

    # Areca cache: cli64 talks to the controller over I2C/PCIe which is slow.
    # Poll at most every 15 seconds to avoid hammering the controller.
    _areca_cache: List[Sensor] = []
    _areca_cache_time: float = 0.0
    _areca_poll_interval: float = 15.0

    @staticmethod
    def get_all_sensors() -> List[Sensor]:
        """Get temperature sensors from all available sources."""
        sensors = []
        sensors.extend(SensorManager._get_hwmon_sensors())
        sensors.extend(SensorManager._get_nvidia_sensors())
        sensors.extend(SensorManager._get_areca_sensors())
        sensors.extend(SensorManager._get_thermal_zones())
        return sensors

    @staticmethod
    def _get_hwmon_sensors() -> List[Sensor]:
        """Read sensors from /sys/class/hwmon/"""
        sensors = []
        hwmon_path = Path("/sys/class/hwmon")

        if not hwmon_path.exists():
            return sensors

        for hwmon_dir in sorted(hwmon_path.iterdir()):
            try:
                name_file = hwmon_dir / "name"
                if name_file.exists():
                    chip_name = name_file.read_text().strip()
                else:
                    chip_name = hwmon_dir.name

                if chip_name in ["hidpp_battery_0", "power_meter"]:
                    continue

                sensor_type = SensorType.OTHER
                if "coretemp" in chip_name or "k10temp" in chip_name:
                    sensor_type = SensorType.CPU
                elif "nvme" in chip_name:
                    sensor_type = SensorType.NVME
                elif "amdgpu" in chip_name or "radeon" in chip_name:
                    sensor_type = SensorType.GPU
                elif "drivetemp" in chip_name:
                    sensor_type = SensorType.HDD

                for temp_file in sorted(hwmon_dir.glob("temp*_input")):
                    try:
                        temp_num = re.search(r"temp(\d+)_input", temp_file.name)
                        if not temp_num:
                            continue

                        num = temp_num.group(1)
                        temp_raw = int(temp_file.read_text().strip())
                        temp_c = temp_raw / 1000.0

                        if temp_c < -50 or temp_c > 150:
                            continue

                        label_file = hwmon_dir / f"temp{num}_label"
                        if label_file.exists():
                            sensor_name = label_file.read_text().strip()
                        else:
                            if sensor_type == SensorType.CPU:
                                if num == "1":
                                    sensor_name = "Package"
                                else:
                                    sensor_name = f"Core {int(num) - 2}"
                            elif sensor_type == SensorType.NVME:
                                if num == "1":
                                    sensor_name = f"NVMe {hwmon_dir.name[-1]} Composite"
                                else:
                                    sensor_name = (
                                        f"NVMe {hwmon_dir.name[-1]} Sensor {num}"
                                    )
                            else:
                                sensor_name = f"Temp {num}"

                        high_thresh = None
                        crit_thresh = None

                        max_file = hwmon_dir / f"temp{num}_max"
                        if max_file.exists():
                            try:
                                val = int(max_file.read_text().strip()) / 1000.0
                                if 0 < val < 150:
                                    high_thresh = val
                            except (ValueError, PermissionError, FileNotFoundError):
                                pass

                        crit_file = hwmon_dir / f"temp{num}_crit"
                        if crit_file.exists():
                            try:
                                val = int(crit_file.read_text().strip()) / 1000.0
                                if 0 < val < 150:
                                    crit_thresh = val
                            except (ValueError, PermissionError, FileNotFoundError):
                                pass

                        sensors.append(
                            Sensor(
                                chip_id=f"hwmon-{chip_name}",
                                sensor_id=sensor_name,
                                adapter="hwmon",
                                temperature=temp_c,
                                high_threshold=high_thresh,
                                critical_threshold=crit_thresh,
                                sensor_type=sensor_type,
                            )
                        )

                    except (ValueError, PermissionError, FileNotFoundError):
                        continue

            except (PermissionError, FileNotFoundError):
                continue

        return sensors

    @staticmethod
    def _get_nvidia_sensors() -> List[Sensor]:
        """Get NVIDIA GPU temperatures via nvidia-smi."""
        sensors = []

        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=index,name,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
                stderr=subprocess.DEVNULL,
                universal_newlines=True,
                timeout=5,
            )

            for line in output.strip().split("\n"):
                if not line.strip():
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 3:
                    idx = parts[0]
                    name = parts[1]
                    try:
                        temp = float(parts[2])
                        display_name = name.replace("NVIDIA ", "").replace(
                            "GeForce ", ""
                        )

                        sensors.append(
                            Sensor(
                                chip_id=f"nvidia-gpu-{idx}",
                                sensor_id=f"{display_name}",
                                adapter="nvidia-smi",
                                temperature=temp,
                                high_threshold=83.0,
                                critical_threshold=90.0,
                                sensor_type=SensorType.GPU,
                            )
                        )
                    except (ValueError, IndexError):
                        continue

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            pass

        return sensors

    @staticmethod
    def _get_areca_sensors() -> List[Sensor]:
        """Get Areca RAID controller temperatures via cli64.

        The Areca ARC-1882 (and similar) controllers expose CPU and board
        temperatures only through their proprietary cli64 tool. These temps
        are invisible to lm-sensors, hwmon, and thermal_zone interfaces.
        Results are cached to avoid hammering the controller bus.
        """
        now = _time.monotonic()
        if (now - SensorManager._areca_cache_time) < SensorManager._areca_poll_interval:
            return list(SensorManager._areca_cache)

        sensors = []
        try:
            output = subprocess.check_output(
                ["sudo", "-n", "cli64", "hw", "info"],
                stderr=subprocess.DEVNULL,
                universal_newlines=True,
                timeout=10,
            )

            for line in output.split("\n"):
                line = line.strip()

                if "CPU Temperature" in line:
                    match = re.search(r":\s*(\d+)\s*C", line)
                    if match:
                        temp = float(match.group(1))
                        sensors.append(
                            Sensor(
                                chip_id="areca-raid",
                                sensor_id="RAID CPU",
                                adapter="cli64",
                                temperature=temp,
                                high_threshold=85.0,
                                critical_threshold=95.0,
                                sensor_type=SensorType.RAID,
                            )
                        )

                elif "Controller Temp" in line:
                    match = re.search(r":\s*(\d+)\s*C", line)
                    if match:
                        temp = float(match.group(1))
                        sensors.append(
                            Sensor(
                                chip_id="areca-raid",
                                sensor_id="RAID Board",
                                adapter="cli64",
                                temperature=temp,
                                high_threshold=70.0,
                                critical_threshold=85.0,
                                sensor_type=SensorType.RAID,
                            )
                        )

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            pass

        SensorManager._areca_cache = sensors
        SensorManager._areca_cache_time = now
        return list(sensors)

    @staticmethod
    def _get_thermal_zones() -> List[Sensor]:
        """Get thermal zone temperatures."""
        sensors = []
        tz_path = Path("/sys/class/thermal")

        if not tz_path.exists():
            return sensors

        for tz_dir in sorted(tz_path.glob("thermal_zone*")):
            try:
                type_file = tz_dir / "type"
                temp_file = tz_dir / "temp"

                if not temp_file.exists():
                    continue

                tz_type = (
                    type_file.read_text().strip() if type_file.exists() else "unknown"
                )

                if "x86_pkg" in tz_type or "cpu" in tz_type.lower():
                    continue

                temp_raw = int(temp_file.read_text().strip())
                temp_c = temp_raw / 1000.0

                if temp_c < -50 or temp_c > 150:
                    continue

                sensors.append(
                    Sensor(
                        chip_id=f"thermal-{tz_dir.name}",
                        sensor_id=tz_type,
                        adapter="thermal_zone",
                        temperature=temp_c,
                        sensor_type=SensorType.OTHER,
                    )
                )

            except (ValueError, PermissionError, FileNotFoundError):
                continue

        return sensors


class RenameDialog(Gtk.Dialog):
    """Dialog for renaming a sensor."""

    def __init__(self, parent, current_name: str, sensor_id: str):
        super().__init__(title="Rename Sensor", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_default_size(300, 100)

        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        label = Gtk.Label(label=f"Enter new name for:\n{sensor_id}")
        box.pack_start(label, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text(current_name)
        self.entry.set_activates_default(True)
        box.pack_start(self.entry, False, False, 0)

        reset_btn = Gtk.Button(label="Reset to Default")
        reset_btn.connect("clicked", lambda w: self.entry.set_text(""))
        box.pack_start(reset_btn, False, False, 0)

        self.set_default_response(Gtk.ResponseType.OK)
        self.show_all()

    def get_new_name(self) -> str:
        return self.entry.get_text().strip()


class uBTEMP:
    """Main application class."""

    APP_ID = "ubtemp"
    APP_NAME = "uBTEMP"
    CONFIG_DIR = Path.home() / ".config" / "ubtemp"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    ICONS_DIR = Path.home() / ".local" / "share" / "ubtemp" / "icons"

    TYPE_ORDER = [
        SensorType.CPU,
        SensorType.GPU,
        SensorType.RAID,
        SensorType.NVME,
        SensorType.HDD,
        SensorType.MOTHERBOARD,
        SensorType.OTHER,
    ]

    def __init__(self):
        self.config = Config.load(self.CONFIG_FILE)
        self.sensors: List[Sensor] = []
        self.sensor_labels: Dict[str, Gtk.Label] = {}  # Track labels for updates
        self.last_sensor_ids: List[str] = []  # Track sensor list for changes
        self.last_critical_notification: Dict[str, float] = {}
        self.notification_cooldown = 60
        self.highest_temp = 0.0
        self.menu = None
        self.current_icon = None

        # Create indicator with full icon path
        self.indicator = AppIndicator3.Indicator.new(
            self.APP_ID,
            str(self.ICONS_DIR / "temp-normal.svg"),
            AppIndicator3.IndicatorCategory.HARDWARE,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title(self.APP_NAME)

        self.update_sensors()
        self.build_menu()
        self.update_icon()

        # Update every 1 second
        GLib.timeout_add(1000, self.auto_refresh)

    def celsius_to_fahrenheit(self, celsius: float) -> float:
        return (celsius * 9 / 5) + 32

    def format_temp(self, celsius: float) -> str:
        if self.config.use_fahrenheit:
            return f"{self.celsius_to_fahrenheit(celsius):.1f}°F"
        return f"{celsius:.1f}°C"

    def get_temp_color(self, celsius: float) -> str:
        if celsius >= self.config.critical_threshold:
            return "#FF4444"
        elif celsius >= self.config.warning_threshold:
            return "#FFA500"
        else:
            return "#44FF44"

    def get_icon_name(self, celsius: float) -> str:
        """Get icon name based on temperature."""
        if celsius >= self.config.critical_threshold:
            return "temp-critical"
        elif celsius >= self.config.warning_threshold:
            return "temp-warning"
        else:
            return "temp-normal"

    def update_icon(self):
        """Update tray icon based on highest temperature."""
        new_icon = self.get_icon_name(self.highest_temp)
        if new_icon != self.current_icon:
            icon_path = str(self.ICONS_DIR / f"{new_icon}.svg")
            if Path(icon_path).exists():
                self.indicator.set_icon_full(icon_path, "Temperature")
            self.current_icon = new_icon

    def get_display_name(self, sensor: Sensor) -> str:
        return self.config.custom_names.get(sensor.unique_id, sensor.sensor_id)

    def update_sensors(self):
        """Update all sensor readings."""
        self.sensors = SensorManager.get_all_sensors()

        def sort_key(s: Sensor) -> Tuple[int, str]:
            type_idx = (
                self.TYPE_ORDER.index(s.sensor_type)
                if s.sensor_type in self.TYPE_ORDER
                else 999
            )
            return (type_idx, self.get_display_name(s).lower())

        self.sensors.sort(key=sort_key)

        if self.sensors:
            self.highest_temp = max(s.temperature for s in self.sensors)

        self.check_critical_temps()

    def check_critical_temps(self):
        if not self.config.show_notifications:
            return

        current_time = _time.time()

        for sensor in self.sensors:
            if sensor.temperature >= self.config.critical_threshold:
                last_notif = self.last_critical_notification.get(sensor.unique_id, 0)
                if current_time - last_notif > self.notification_cooldown:
                    self.show_notification(
                        "Critical Temperature Warning",
                        f"{self.get_display_name(sensor)}: {self.format_temp(sensor.temperature)}",
                        is_critical=True,
                    )
                    self.last_critical_notification[sensor.unique_id] = current_time

    def show_notification(self, title: str, message: str, is_critical: bool = False):
        try:
            urgency = "critical" if is_critical else "normal"
            subprocess.call(
                ["notify-send", "-u", urgency, "-i", "dialog-warning", title, message]
            )
        except FileNotFoundError:
            pass

    def update_labels(self):
        """Update only the label text without rebuilding menu."""
        for sensor in self.sensors:
            label = self.sensor_labels.get(sensor.unique_id)
            if label:
                display_name = self.get_display_name(sensor)
                temp_str = self.format_temp(sensor.temperature)
                color = self.get_temp_color(sensor.temperature)
                label.set_markup(
                    f"<span font_family='monospace'>{display_name:<20}</span>  "
                    f"<span foreground='{color}' weight='bold'>{temp_str}</span>"
                )

        # Update tray label and icon
        self.indicator.set_label(self.format_temp(self.highest_temp), "999.9°F")
        self.update_icon()

    def sensors_changed(self) -> bool:
        """Check if the sensor list has changed."""
        current_ids = [s.unique_id for s in self.sensors]
        if current_ids != self.last_sensor_ids:
            self.last_sensor_ids = current_ids
            return True
        return False

    def build_menu(self):
        """Build the indicator menu."""
        self.menu = Gtk.Menu()
        self.sensor_labels.clear()

        if not self.sensors:
            item = Gtk.MenuItem(label="No sensors detected")
            item.set_sensitive(False)
            self.menu.append(item)
        else:
            current_type = None

            for sensor in self.sensors:
                if sensor.sensor_type != current_type:
                    current_type = sensor.sensor_type
                    if self.menu.get_children():
                        self.menu.append(Gtk.SeparatorMenuItem())
                    header = Gtk.MenuItem(label=f"━━ {current_type.value} ━━")
                    header.set_sensitive(False)
                    self.menu.append(header)

                display_name = self.get_display_name(sensor)
                temp_str = self.format_temp(sensor.temperature)
                color = self.get_temp_color(sensor.temperature)

                item = Gtk.MenuItem()
                label = Gtk.Label()
                label.set_markup(
                    f"<span font_family='monospace'>{display_name:<20}</span>  "
                    f"<span foreground='{color}' weight='bold'>{temp_str}</span>"
                )
                label.set_xalign(0)
                label.set_margin_start(5)
                label.set_margin_end(5)
                item.add(label)

                # Store label reference for updates
                self.sensor_labels[sensor.unique_id] = label

                item.sensor = sensor
                item.connect("button-press-event", self.on_sensor_click)
                self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        unit_label = "Switch to °C" if self.config.use_fahrenheit else "Switch to °F"
        unit_item = Gtk.MenuItem(label=unit_label)
        unit_item.connect("activate", self.on_toggle_unit)
        self.menu.append(unit_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        refresh_item = Gtk.MenuItem(label="↻ Refresh Now")
        refresh_item.connect("activate", self.on_refresh)
        self.menu.append(refresh_item)

        about_item = Gtk.MenuItem(label="About uBTEMP")
        about_item.connect("activate", self.on_about)
        self.menu.append(about_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Store current sensor IDs
        self.last_sensor_ids = [s.unique_id for s in self.sensors]

        self.indicator.set_label(self.format_temp(self.highest_temp), "999.9°F")

    def on_sensor_click(self, widget, event):
        if event.button == 3:
            sensor = getattr(widget, "sensor", None)
            if sensor:
                self.show_rename_dialog(sensor)
                return True
        return False

    def show_rename_dialog(self, sensor: Sensor):
        current_name = self.get_display_name(sensor)
        dialog = RenameDialog(None, current_name, sensor.sensor_id)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            new_name = dialog.get_new_name()
            if new_name:
                self.config.custom_names[sensor.unique_id] = new_name
            elif sensor.unique_id in self.config.custom_names:
                del self.config.custom_names[sensor.unique_id]
            self.config.save(self.CONFIG_FILE)
            self.build_menu()

        dialog.destroy()

    def on_toggle_unit(self, widget):
        self.config.use_fahrenheit = not self.config.use_fahrenheit
        self.config.save(self.CONFIG_FILE)
        self.build_menu()

    def on_refresh(self, widget):
        self.update_sensors()
        self.build_menu()

    def auto_refresh(self):
        """Auto-refresh - only update labels, don't rebuild menu."""
        self.update_sensors()

        # Only rebuild menu if sensors changed (added/removed)
        if self.sensors_changed():
            self.build_menu()
        else:
            # Just update the temperature labels
            self.update_labels()

        return True

    def on_about(self, widget):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("uBTEMP")
        dialog.set_version("1.0.0")
        dialog.set_comments(
            "Ubuntu Temperature Monitor\n\n"
            "Monitors CPU, GPU, NVMe, and other sensors.\n"
            "Right-click any sensor to rename it."
        )
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.run()
        dialog.destroy()

    def on_quit(self, widget):
        Gtk.main_quit()

    def run(self):
        Gtk.main()


def main():
    app = uBTEMP()
    app.run()


if __name__ == "__main__":
    main()
