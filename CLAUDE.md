## Video Creator Pipeline (NEW)

Agent-based video generation system. Replaces monolithic `/givore-batch` with atomic agents.

- **Command**: `/video-creator` — orchestrates 9 specialized agents
- **Flow**: Format Planner → Clip Assembler → Keyword Extractor → Script Writer → Script Validator → Audio Generator → Metadata Generator → SFX Planner → Video Assembler
- **Key difference from old pipeline**: Clips are selected BEFORE script writing (script is written TO the footage)
- **Approval**: One gate per variant (after clips + script), not just v1
- **Variants**: User chooses X (flexible, not hardcoded to 7)
- **DB tracking**: ALL variants update history with `--content-format` and `--variant` flags
- **Format rotation**: `script-rotation --format CUANTO_CUESTA` filters by specific format

### Reference file structure
- **`formats/`** — 20 individual format files + `_INDEX.md` (split from CONTENT_FORMATS.md)
- **`structures/`** — 6 structure files + `_INDEX.md` (split from SCRIPT_STRUCTURES.md)
- **`personas/`** — 5 persona files + `_INDEX.md` (split from SCRIPT_PERSONAS.md)
- **`.claude/commands/agents/`** — 9 agent prompt files (format-planner, clip-assembler, keyword-extractor, script-writer, script-validator, audio-generator, metadata-generator, sfx-planner, video-assembler)

### Legacy pipeline
- `/givore-batch` — old monolithic pipeline, kept during transition

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
