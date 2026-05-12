# Changelog

---

## v1.1 — patch (unreleased)

### Fixed
- **Buttons not responding** — the `copyPython()` function contained Python f-string syntax (`${}` inside backtick template literals) which JavaScript was incorrectly interpreting as template substitutions, silently breaking the entire script block on page load. All buttons (fetch & rename, reset, apply on disk, dry run, copy list, export JSON) were affected. Rewrote the full JS in standard ES5 to eliminate the conflict.
- **Tab switching crash** — `switchTab()` was reading `event.target` from a stale event reference; now receives the element directly as a parameter.

### Known issues being tracked
- **Discogs match quality** — first result is not always the correct release, especially for releases with common titles or multiple pressings. A result-picker UI (letting you choose from the top 5 hits before confirming) is planned for v1.2.
- **Server required for disk ops** — apply on disk and load subfolders require `server.py` to be running. A future version may bundle this as a small executable so no terminal is needed.
- **No batch/label-level processing** — currently processes one label folder at a time. Recursive mode (walk an entire Labels directory) is planned.
- **Windows PATH delay after Python install** — after `setup.bat` installs Python via winget, the shell must be restarted before `python` is available. The script now notifies the user of this, but it's an unavoidable Windows limitation.

---

## v1.0 — initial release

- Web UI for Discogs folder renaming — no server required for basic use
- Auto-detect input format: catalog numbers, year-prefix, artist-title, raw names
- Local server bridge (`server.py`) for disk read/write from the UI
- Load subfolders directly from a directory path
- Apply on disk with dry run preview
- Inline name editing before applying
- Tabbed results: All / Changed / Errors / Skipped
- Export JSON for use with standalone `rename.py`
- Setup scripts for Windows (`setup.bat`) and Mac/Linux (`setup.sh`) with auto Python install

---

- nmyriad
