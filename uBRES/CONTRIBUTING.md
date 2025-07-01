# Contributing to uBRES

Thank you for your interest in contributing to uBRES! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Your environment (Ubuntu version, desktop environment, Python version)
   - Output of `xrandr --query`

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - A clear description of the feature
   - Why it would be useful
   - How it might be implemented (optional)

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
   cd uBRES
   ```

2. Install dependencies:
   ```bash
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
       gir1.2-ayatanaappindicator3-0.1 x11-xserver-utils
   ```

3. Run the application:
   ```bash
   /usr/bin/python3 ubres.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Testing

Before submitting a PR, please test:

1. Application starts without errors
2. All connected displays are detected
3. Resolution switching works correctly
4. The menu updates after switching
5. Notifications appear (if enabled)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
