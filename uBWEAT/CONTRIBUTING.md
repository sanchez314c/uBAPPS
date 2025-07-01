# Contributing to uBWEAT

Thank you for your interest in contributing to uBWEAT!

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Include:
   - Ubuntu/Linux version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Network configuration if relevant

### Suggesting Features

1. Check existing feature requests
2. Describe the feature clearly
3. Explain the use case

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a Pull Request

## Development Setup

```bash
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBWEAT

sudo apt install python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1

/usr/bin/python3 ubweat.py
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for classes and functions

## Testing

- Test with different locations
- Test with network disconnected
- Test both °C and °F modes
- Verify icon changes with weather conditions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
