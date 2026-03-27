## CLI Tools

See [TOOLS.md](TOOLS.md) for all available CLI helpers (`givore-tools.sh`, `givore_db.py`) with usage examples and pipeline integration guide.

- **`scripts/givore-tools.sh`** — Wrapper for media queries, video assembly, subtitles, batch status, clip DB, and history DB
- **`scripts/givore_db.py`** — Unified SQLite DB for clips + content history (scripts, trials, videos, renueva)
- **DB**: `scripts/clips.db` — Source of truth for clip metadata AND rotation history (run `givore_db.py new` + `bulk-add` to import new clips, `givore_db.py migrate-all` to import history)
- **`CONTENT_PILLARS.md`** — 15 broad top-of-funnel content pillars (cycling POV, daily life, minimalism, hidden spots, pets, barrios, etc.) with hooks, formats, and Givore mention guidelines
- **`KEYWORDS_RESEARCH.md`** — Comprehensive keyword research for Spain (40+ keywords with volumes, 7 clusters, city-level data for 9 cities, application guide for hooks/thumbnails/descriptions/web)
- **`scripts/quality_check.py`** — Automated pre-human quality gate for scripts (phrase repetition, marketing tone, hook uniqueness, CTA freshness, structure variety, clip diversity, trash encouragement check, giveaway-first framing)

## Renueva Channel

Second content channel: female voice narrating item reuse/renovation/upcycling ideas, using screen recordings + AI-generated "after" images.

- **Commands**: `/givore-renueva` (single pipeline), `/givore-renueva-batch` (N variants)
- **Reference files**: `renueva/` directory (6 files: instructions, categories, hooks, CTAs, image prompts, metadata)
- **DB tracking**: `renueva-add`, `renueva-list`, `renueva-rotation`, `renueva-delete`
- **Image generation**: Manual (Nano Banana Pro web UI) — pipeline pauses for user to generate
- **Assembly**: Supports `"type": "image"` clips for AI-generated stills alongside video clips
- **Voice**: Female ElevenLabs voice (TBD — to be selected)
- **Project folders**: `projects/renueva-[date]_[item-slug]/`
