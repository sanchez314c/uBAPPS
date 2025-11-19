# Contributing to uBTEMP

Thank you for your interest in contributing to uBTEMP! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Your environment (Ubuntu version, desktop environment, Python version)
   - Output of `sensors` command
   - Contents of `~/.config/ubtemp/config.json` (if relevant)

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - A clear description of the feature
   - Why it would be useful
   - How it might be implemented (optional)

Ideas for features:
- Support for additional sensor types
- Graphical temperature history
- Custom warning thresholds per sensor
- Export temperature logs
- System tray graph/sparkline

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sanchez314c/uBAPPS.git
   cd uBTEMP
   ```

2. Install dependencies:
   ```bash
   sudo apt install lm-sensors python3-gi python3-gi-cairo \
       gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
   ```

3. Run sensor detection (if not done):
   ```bash
   sudo sensors-detect
   ```

4. Run the application:
   ```bash
   /usr/bin/python3 ubtemp.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where practical
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use dataclasses for structured data

## Testing

Before submitting a PR, please test:

1. Application starts without errors
2. All sensors are detected and displayed
3. Temperature updates work (wait a few seconds)
4. Right-click rename works
5. Custom names persist after restart
6. Celsius/Fahrenheit toggle works
7. Color coding appears correctly
8. Critical temperature notification works (if testable)

### Testing Checklist

- [ ] App starts with `make run`
- [ ] Sensors display correctly
- [ ] Temperatures update every second
- [ ] Right-click rename dialog opens
- [ ] Renamed sensors save to config
- [ ] Temperature unit toggle works
- [ ] Unit preference saves to config
- [ ] Colors match temperature thresholds
- [ ] No console errors during operation

## Adding New Sensor Types

To add support for a new sensor type:

1. Add the type to the `SensorType` enum
2. Update `SensorManager.classify_sensor()` with detection logic
3. Add the type to `uBTEMP.TYPE_ORDER` for sorting
4. Test with actual hardware if possible

Example:
```python
class SensorType(Enum):
    # ... existing types ...
    WATER_COOLING = "Water Cooling"  # New type

# In classify_sensor():
if 'aqua' in chip_lower or 'water' in sensor_lower:
    return SensorType.WATER_COOLING
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
