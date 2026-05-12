# discogs-cleaner

A web-based tool that looks up music releases on Discogs and renames your library folders to a consistent format.

```
[CAT001] Artist - Title (Year)
```

Built for large local libraries with mixed naming conventions — catalog-numbered releases, year-prefixed folders, bare artist/title combos, etc.

---

## Usage

### 1. Get Discogs API credentials

Go to [discogs.com/settings/developers](https://www.discogs.com/settings/developers) and create an app. You'll get a **Consumer Key** and **Consumer Secret**.

### 2. Open the web UI

Just open `index.html` in any browser — no server needed.

Paste your Consumer Key and Secret into the sidebar, then paste folder names (one per line) and hit **fetch & rename**.

### 3. Review & export

The UI shows every proposed rename. You can edit any name inline before exporting. When happy:

- **Copy rename list** — tab-separated old → new, for reference
- **Export JSON** — machine-readable, used by `rename.py`
- **Copy Python script** — standalone script with renames baked in, ready to run

### 4. Apply renames on disk

```bash
# Preview first (no changes)
python rename.py --path "D:/Music/Labels" --input discogs-cleaner-results.json --dry-run

# Apply
python rename.py --path "D:/Music/Labels" --input discogs-cleaner-results.json
```

---

## Folder name parsing

The tool auto-detects input format and chooses the best Discogs lookup strategy:

| Input format | Strategy |
|---|---|
| `[IHT013] Out of Office` | Catalog number lookup |
| `[IHT014] Tino Machauer - Cesta (2024)` | Already correct — skipped |
| `(1997) Delerium - Karma` | Artist + title search |
| `delerium silence` | Title search |
| `INHERIT` | Skipped (too short, likely a label folder) |

---

## Naming format

Everything is normalised to:

```
[CATALOG] Artist - Title (Year)
```

- Compilations / Various Artists → `[CATALOG] Title (Year)` (no artist prefix)
- If no catalog number is found → `Artist - Title (Year)`

---

## Rate limiting

Discogs allows ~25 unauthenticated requests/minute with consumer key auth. The default delay is 500ms between requests. Adjust in the sidebar options if you hit 429 errors.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Web UI — open in browser, no server needed |
| `rename.py` | Python script to apply renames on disk |
| `config.example` | Example credentials file (never commit real keys) |

---

## Security

- Credentials are never stored — only held in memory while the page is open
- Never commit your real Consumer Key/Secret to this repo
- The `config.example` file is a template only

---

## License

MIT
