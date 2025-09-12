# TODO

## Known Issues

- [ ] GNOME Shell requires AppIndicator extension (no built-in tray support)
- [ ] uBTIME requires Python 3.9+ for zoneinfo (older Ubuntu uses 3.8)
- [ ] No automated tests

## Planned Features

- [x] Settings persistence (save polling interval, units, etc.) -- DONE: all apps save config to ~/.config/<app>/config.json
- [x] Notification alerts (e.g., CPU > 90%, temperature > 80C) -- DONE: uBCPU and uBTEMP have critical notifications
- [ ] Dark/light icon variants
- [ ] `.deb` packages for system-level installation
- [ ] uBMEM - Memory usage monitor
- [ ] uBBAT - Battery status indicator

## Technical Debt

- [x] Add per-app configuration files -- DONE: all monitoring apps have config.json
- [ ] Unify install script pattern across all apps (currently two patterns)
- [ ] Add shellcheck validation (CI has it but uses `|| true`)
- [ ] Add basic pytest tests for data parsing functions
- [ ] Document the AppIndicator pattern in a shared dev guide
