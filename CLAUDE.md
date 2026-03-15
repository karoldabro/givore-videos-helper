## CLI Tools

See [TOOLS.md](TOOLS.md) for all available CLI helpers (`givore-tools.sh`, `givore_db.py`) with usage examples and pipeline integration guide.

- **`scripts/givore-tools.sh`** — Wrapper for media queries, video assembly, subtitles, batch status, clip DB, and history DB
- **`scripts/givore_db.py`** — Unified SQLite DB for clips + content history (scripts, trials, videos)
- **DB**: `scripts/clips.db` — Source of truth for clip metadata AND rotation history (run `givore_db.py new` + `bulk-add` to import new clips, `givore_db.py migrate-all` to import history)
