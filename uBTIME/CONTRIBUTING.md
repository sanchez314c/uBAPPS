# Contributing to uBTIME

Thank you for your interest in contributing to uBTIME! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Ubuntu/Linux version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. Check existing feature requests
2. Describe the feature clearly
3. Explain the use case
4. Consider implementation complexity

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/sanchez314c/uBAPPS.git
cd uBTIME

# Install dependencies
sudo apt install python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1

# Run directly for testing
/usr/bin/python3 ubtime.py
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings for classes and functions
- Keep functions focused and small
- Comment complex logic

## Testing

- Test on multiple Ubuntu versions if possible
- Test with both 12h and 24h formats
- Test favorites add/remove functionality
- Verify timezone calculations are correct
- Check memory usage over time

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
