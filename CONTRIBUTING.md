# Contributing to uB Suite

Thank you for your interest in contributing to the uB Suite!

## Development Setup

### Prerequisites

- Ubuntu 22.04+ or GNOME-based Linux
- Python 3.6+ (3.9+ for uBTIME)
- GTK 3.0

### Installation

```bash
# Install system dependencies
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1 libnotify-bin

# Clone repository
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBAPPS

# Run any app directly
python3 uBCPU/ubcpu.py
```

## Code Style

- Follow PEP 8 guidelines
- Use 4-space indentation
- Maximum line length: 100 characters
- Add docstrings to functions and classes

## Project Structure

Each app follows a consistent structure:

```
uBAPP/
├── ubapp.py        # Main application
├── install.sh      # Installation script
├── uninstall.sh    # Removal script
├── icons/          # Status icons
├── screenshots/    # App screenshots
├── requirements.txt
├── Makefile
├── README.md
├── CLAUDE.md
├── LICENSE
└── .gitignore
```

## Adding a New App

1. Create folder with `uB` prefix: `uBNEW/`
2. Follow the existing app structure
3. Use the AppIndicator pattern from other apps
4. Include all standard files
5. Add entry to main README.md
6. Update CHANGELOG.md

## Testing

```bash
# Run app directly
python3 uBAPP/ubapp.py

# Test installation
cd uBAPP && ./install.sh

# Verify running
pgrep -f ubapp.py
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Follow existing code patterns
4. Test on Ubuntu/GNOME
5. Update documentation
6. Submit pull request

### Commit Messages

```
feat(uBCPU): Add per-core temperature display
fix(uBNET): Handle missing network interfaces
docs(uBTIME): Update timezone configuration
```

## Areas for Contribution

- New monitoring apps (battery, GPU, memory)
- UI improvements
- Performance optimizations
- Documentation
- Icon design
- Bug fixes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
