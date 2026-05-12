# Changelog

---

## v1.2 — parser overhaul

### Fixed
- **False "too short" skips** — folders like `JSPRV35-Kyoto_EP-GP02-WEB-2024-WAV` were being incorrectly flagged as label folders because the word count was measured on raw text. The check now only skips names with no digits and no recognizable structure — real label folders like `INHERIT` or `A7A` are unaffected.
- **Paren-wrapped catalog numbers missed** — formats like `Augusto_Taito-Antibero_EP-(SOIL001)-WEB-2026-PTC` and `Pornbugs-M_9.12.4.-(SLM045)-WEB-2024-AFO` were not being parsed. Catalog detection now covers both `[CAT001]` and `(CAT001)` patterns anywhere in the folder name.
- **Underscore/dot file-naming conventions** — folder names using `_` as word separators (common in scene/download naming) are now normalized to spaces before searching, significantly improving Discogs match quality.
- **Format suffix noise** — tags like `WEB`, `WAV`, `FLAC`, `MP3`, `AFO`, `PTC` are stripped from search queries so they don't confuse Discogs results.
- **Skip reason always shown** — previously skipped folders showed no explanation in the log. Every skip now logs exactly why: `short name with no numbers`, `could not extract searchable terms`, or `already correctly named`.

### Improved
- **Two-stage fallback search** — if a catalog lookup returns no results, the tool now tries catalog + cleaned name, then name only before marking as not found. Reduces false errors on releases with less common catalog numbers.
- **Parse reason logged** — the log now shows how each folder was interpreted (e.g. `catalog in parens: SOIL001`, `normalized from: raw_name`) making it easier to spot patterns that need further tuning.

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
