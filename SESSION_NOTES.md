# SESSION_NOTES.md
# discogs-cleaner — project continuity doc
# Last updated: 2026-05-12

---

## Project overview

Two repos:
- **discogs-cleaner** (web UI) → github.com/nmyriad/discogs-cleaner
- **discogs-cleaner-desktop** (Electron wrapper) → github.com/nmyriad/discogs-cleaner-desktop

Stack: HTML/JS frontend, Python (server.py) backend, Electron desktop wrapper.
The desktop repo uses discogs-cleaner as a git submodule.
GitHub Actions auto-builds the Windows installer and publishes to Releases on every version tag.

---

## Current versions

| Repo | Latest version | Notes |
|---|---|---|
| discogs-cleaner | v1.6.0 | Web UI, fully working |
| discogs-cleaner-desktop | v1.5.3 | Native Windows app, auto-updates working |

---

## Environment

- **James is on Mac** — web repo work (index.html, server.py) can be done on Mac
- **Desktop builds require Windows** — `python build.py` and `npm run build` must be run on the Windows laptop
- **Windows laptop path**: `C:\Users\JamesHermann\`
- **Discogs app**: "Folder Builder" at discogs.com/settings/developers (regenerate keys after sharing in chat)

---

## Repo structure

```
discogs-cleaner/
├── index.html          # Web UI — all features
├── server.py           # Python local server — disk ops, config, stats
├── rename.py           # Standalone CLI rename script
├── setup.bat           # Windows: checks Python, starts server
├── setup.sh            # Mac/Linux: checks Python, starts server
├── config.example      # Credentials template
├── CHANGELOG.md        # Full version history
└── README.md           # Docs

discogs-cleaner-desktop/
├── main.js             # Electron main process
├── preload.js          # IPC bridge
├── package.json        # Version + build config (current: 1.5.3)
├── build.py            # One-command build: PyInstaller + electron-builder
├── assets/
│   ├── icon.ico        # Rowroad artwork icon
│   └── tray.png        # Tray icon
├── .github/workflows/
│   └── release.yml     # Auto-build + publish on version tag
├── discogs-cleaner/    # Git submodule (currently @ 74c6106)
└── CHANGELOG.md
```

---

## How to push updates

### Web repo
```powershell
cd C:\Users\JamesHermann\discogs-cleaner
git add -A
git commit -m "your message"
git push origin main
git tag v1.X.X
git push origin v1.X.X
```

### Desktop repo
```powershell
cd C:\Users\JamesHermann\discogs-cleaner-desktop

# Bump submodule if web repo changed
cd discogs-cleaner
git pull origin main
cd ..

git add -A
git commit -m "your message"
git push origin main
git tag v1.X.X
git push origin v1.X.X
```

GitHub Actions builds and publishes the installer automatically on tag push.
GH_TOKEN secret is set in discogs-cleaner-desktop repo settings.

### To rebuild desktop locally
```powershell
cd C:\Users\JamesHermann\discogs-cleaner-desktop
python build.py
# Installer → dist\discogs-cleaner Setup X.X.X.exe
```

---

## Next session TODO

### Priority 1 — Desktop v1.5.2 stats bar fix
The stats bar (session + lifetime rename counter) and key caching UI are in index.html (v1.6.0)
but the desktop app bundles an old index.html inside server.exe.
Fix: bump submodule to latest, rebuild.
```powershell
cd discogs-cleaner && git pull origin main && cd ..
git add discogs-cleaner
git commit -m "chore: bump submodule to v1.6.0"
git push origin main
git tag v1.5.2
git push origin v1.5.2
```
Then GitHub Actions builds the new installer automatically.

### Priority 2 — Reddit post
Drafted and ready. Target: r/discogs (text post, no link post).
Post leads with "89,000 releases, tired of renaming by hand" angle.
Add screenshots before posting — best shot is the before/after rename table.

### Priority 3 — Result picker
When Discogs returns multiple hits, show top 5 options in the UI so user can
pick the correct one before applying. Reduces wrong matches.
Implementation: after fetch, if confidence is low (no catalog match, common title),
show a mini modal with 5 options — artwork thumbnail, label, year, catalog number.

### Priority 4 — Track verification
After a Discogs match is found, scan audio files inside the folder and cross-reference:
- Track count matches Discogs tracklist
- Track titles fuzzy-match
Flags low-confidence matches in amber before user applies.
Requires server.py to read directory contents and audio metadata (mutagen library).

### Priority 5 — Recursive label mode
Currently processes one label folder at a time.
Add a "recursive" toggle: walk an entire Labels directory, process each sublabel's
releases automatically. Needs progress tracking and per-label logs.

---

## Known issues

- **[IHT] style catalog numbers with spaces** — `[KLANG  01]` (double space) appearing in some
  renames. Parser issue with how Discogs returns catno for some labels.
- **Title case edge cases** — artist names like `RZA`, `DJ` getting lowercased incorrectly.
  Need a proper noun exception list or a "preserve all-caps words" rule.
- **Discogs rate limiting on large batches** — auto-backoff works but 50+ folders still
  occasionally hit errors at the end. Consider pre-emptive delay scaling for batches > 30.

---

## Config & credentials

- Discogs API keys stored at `~/.discogs-cleaner/config.json` (never in repo)
- Desktop state (last seen version for changelog dialog) at `~/.discogs-cleaner/desktop-state.json`
- Never commit real keys — config.example is the template

---

## Style notes

- James moves fast, trusts the process, wants things explained not just done
- Prefers screenshots early, pastes error output directly
- Cares about clean repo structure, good docs, consistent naming
- MIT license, open source, community-first philosophy
- Signs all READMEs and changelogs with `— nmyriad`
- Rowroad artwork is the project icon

---

- nmyriad
