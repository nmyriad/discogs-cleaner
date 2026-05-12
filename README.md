# discogs-cleaner

A web-based tool that looks up music releases on Discogs and renames your library folders to a consistent format.

```
[CAT001] Artist - Title (Year)
```

Built for large local libraries with mixed naming conventions — catalog-numbered releases, year-prefixed folders, underscore-separated file names, paren-wrapped catalog numbers, and everything in between.

> **Latest release: v1.5.0** — see [CHANGELOG.md](CHANGELOG.md) for full release notes.

---

## Quick start

### Windows

```
Double-click setup.bat
```

Checks for Python, installs it if missing, and launches the server. Your browser opens automatically at `http://localhost:7842`.

### Mac / Linux

```bash
chmod +x setup.sh
./setup.sh
```

---

## Manual start (if Python is already installed)

```powershell
python server.py
```

Then open `http://localhost:7842` in your browser.

To use the UI without the server (no disk integration), open `index.html` directly in your browser.

---

## Usage

### 1. Get Discogs API credentials

Go to [discogs.com/settings/developers](https://www.discogs.com/settings/developers) and create an app. You'll get a **Consumer Key** and **Consumer Secret**.

Enter them in the sidebar. They're stored only in memory — never saved to disk or sent anywhere except Discogs.

### 2. Load your folders

**With the server running:**
- Enter a folder path in the **Folder path on disk** field (e.g. `D:\Music\Labels\INHERIT`)
- Click **load subfolders** — the list auto-populates

**Without the server:**
- Paste folder names manually, one per line

### 3. Fetch & rename

Hit **fetch & rename**. The tool searches Discogs for each folder using the best available strategy:

| Input format | Strategy |
|---|---|
| `[IHT013] Out of Office` | Catalog number lookup |
| `[IHT014] Tino Machauer - Cesta (2024)` | Already correct — skipped |
| `(1997) Delerium - Karma` | Artist + title search |
| `Artist_Name-(CAT001)-WEB-2024-WAV` | Paren catalog extracted, format tags stripped |
| `delerium silence` | Title search |
| `INHERIT` | Skipped (short, no digits — likely a label folder) |

### 4. Review & apply

- Edit any proposed name inline before applying
- Click **dry run** to preview what would change on disk
- Click **apply on disk** to rename folders instantly

---

## Naming format

Everything is normalised to:

```
[CATALOG] Artist - Title (Year)
```

- Compilations / Various Artists → `[CATALOG] Title (Year)` (no artist prefix)
- If no catalog number is found on Discogs → `Artist - Title (Year)`

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Web UI — works standalone or via server |
| `server.py` | Local server enabling disk read/write from the UI |
| `rename.py` | Standalone CLI script for applying renames from a JSON export |
| `setup.bat` | Windows: checks for Python, installs if needed, starts server |
| `setup.sh` | Mac/Linux: checks for Python, installs if needed, starts server |
| `config.example` | Credentials template — never commit your real keys |
| `CHANGELOG.md` | Full version history and release notes |

---

## Automated releases

This repo uses a GitHub Actions workflow (`.github/workflows/release.yml`) that automatically creates a GitHub Release whenever a version tag is pushed. Release notes are pulled directly from `CHANGELOG.md`.

To cut a new release:

```powershell
git tag v1.3
git push origin main --tags
```

---

## Rate limiting

Discogs allows ~25 requests/minute with consumer key auth. The default delay is 500ms between requests. Adjust in the sidebar options if you hit 429 errors.

---

## Security

- Credentials are never stored — held in memory only while the page is open
- The local server binds to `127.0.0.1` only — not accessible from other machines
- Never commit your real Consumer Key/Secret to this repo
- `config.example` is a template only — keep real credentials out of git

---

## License

MIT

---

- nmyriad
