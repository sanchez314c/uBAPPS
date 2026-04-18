# FORENSIC AUDIT REPORT - uBAPPS (uB Suite)

**Audit Date:** 2026-04-17
**Previous Audit:** 2026-03-14 (see git history for full report)
**Auditor:** Master Control (Claude GLM-5.1)
**Scope:** Re-audit of all 7 Python files + shell scripts + CI workflow

---

## EXECUTIVE SUMMARY

Follow-up audit on the codebase after the 2026-03-14 remediation pass. The previous audit fixed 23 issues including bare except clauses, missing error handling, documentation drift, and placeholder URLs. This pass focuses on security, correctness, compatibility, and quality of the current code state.

**Verdict:** Codebase is clean. Previous fixes held. Found 6 new issues (0 security, 3 correctness, 3 quality). All auto-fixed.

---

## FINDINGS & FIXES

### Issues Found: 6 (0 security / 3 correctness / 3 quality)

| # | Category | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | Correctness | `uBCPU/ubcpu.py:198` | `core_labels` typed `Dict[int, Gtk.Label]` but stores string key `"load"` | Changed to `Dict[object, Gtk.Label]` |
| 2 | Correctness | `uBRES/ubres.py:134` | `subprocess.check_call` discards output, error message prints `e` which has no useful details | Changed to `subprocess.run(capture_output=True, check=True)`, decode stderr in error handler |
| 3 | Correctness | `uBNET/ubnet.py:491-497` | Bridge member session totals lose dimmed markup in `update_labels()` vs `build_menu()` | Added bridge member check in update path to match build markup |
| 4 | Quality | `uBCPU/ubcpu.py:83-95` | `Config.save()` unhandled OSError on write (disk full, permissions) | Wrapped in `try/except (OSError, IOError)` |
| 5 | Quality | `uBDISK/ubdisk.py:78-90` | Same - `Config.save()` unhandled OSError | Same fix |
| 6 | Quality | `uBNET/ubnet.py:83-96` | Same - `Config.save()` unhandled OSError | Same fix |
| 7 | Quality | `uBTEMP/ubtemp.py:94-107` | Same - `Config.save()` unhandled OSError | Same fix |
| 8 | Quality | `uBRES/ubres.py:54-55` | `xrandr --query` subprocess has no timeout (can hang on broken display) | Added `timeout=5`, added `TimeoutExpired` handler |
| 9 | Quality | `uBRES/ubres.py:134` | `set_resolution` has no timeout | Added `timeout=5` to subprocess.run |
| 10 | Quality | `uBRES/ubres.py:326-327` | `which xrandr` check missing `TimeoutExpired` in catch | Added to except tuple |

### Files Changed: 5

- `uBCPU/ubcpu.py` - Config.save() OSError handling, type hint fix
- `uBDISK/ubdisk.py` - Config.save() OSError handling
- `uBNET/ubnet.py` - Config.save() OSError handling, bridge member label fix
- `uBRES/ubres.py` - subprocess timeout + error reporting, TimeoutExpired handling
- `uBTEMP/ubtemp.py` - Config.save() OSError handling

---

## VERIFICATION

- **py_compile**: All 7 Python files compile cleanly
- **ruff check**: All checks passed (no lint errors)
- **TODO/FIXME/HACK/XXX markers**: None found
- **Bare except**: None found (all fixed in previous audit)

---

## ITEMS NOT CHANGED (intentional)

- **Shell scripts**: All install scripts have `set -e`. Uninstall scripts have `set -e` (fixed in previous audit). No `set -u` or `set -o pipefail` — acceptable for simple install/uninstall scripts that don't rely on unset variables or pipes.
- **CI workflow**: `flake8 --ignore=E501,W503` is fine. ShellCheck with `-e SC2086` exclusion is reasonable (variables in install paths are controlled). Python 3.10 CI target is fine.
- **uBWEAT threading**: Correctly uses `GLib.idle_add()` for UI updates from background thread. No issue.
- **uBTEMP Areca sudo**: `sudo -n cli64` (non-interactive) is intentional and documented.

---

## PREVIOUS AUDIT REFERENCE

The 2026-03-14 audit found and fixed 23 issues across 27 findings. All fixes verified intact:
- URL injection in uBWEAT (urllib.parse.quote) - present
- Bare except clauses - none remain
- Dead code removal - verified
- AppIndicator fallback in uBTIME/uBWEAT - proper try/except with sys.exit(1)
- All placeholder URLs updated to actual repo URL

END OF LINE.
