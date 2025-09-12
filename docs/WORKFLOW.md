# Development Workflow

## Branching

```
main ─── stable
  └── feature/<app-name>/<description>
  └── fix/<app-name>/<description>
```

## Development Cycle

1. Branch from `main`
2. Edit the app's Python script
3. Run from source: `python3 uB<NAME>/uB<NAME>.py`
4. Verify tray icon appears and updates correctly
5. Test install/uninstall cycle
6. Commit with conventional format (`feat(uBCPU):`, `fix(uBTEMP):`)
7. Open PR

## Release

1. Update app's `CHANGELOG.md`
2. Update root `CHANGELOG.md`
3. Tag: `git tag v1.x.x`
4. Push: `git push origin main --tags`
