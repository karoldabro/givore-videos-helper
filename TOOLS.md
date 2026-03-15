# Givore CLI Tools Reference

All reusable CLI tools for the givore content pipeline. These wrap recurring operations so they can be approved once per session.

## givore-tools.sh

**Location**: `scripts/givore-tools.sh`
**Purpose**: Single entry point for all pipeline operations — media queries, video assembly, subtitles, batch status, and clip database.

### Media Queries

| Command | Description |
|---------|-------------|
| `givore-tools.sh duration <file>` | Get audio/video duration in seconds |
| `givore-tools.sh duration-all <project-dir>` | Duration of all .mp3 files across v1-v7 subdirs |
| `givore-tools.sh video-info <file>` | Video dimensions (WxH) + duration |
| `givore-tools.sh video-info-all <project-dir>` | Dimensions + duration for all drafts/finals in v1-v7 |

**Use cases**:
- After audio generation: check narration length before clip selection
- After rendering: verify all 7 variants rendered correctly with right dimensions
- Quick overview: compare audio lengths across all batch variants

**Examples**:
```bash
# Check one audio file
givore-tools.sh duration projects/2026-03-11_mesita/v1/mesita.mp3

# Compare all 7 variant audio lengths
givore-tools.sh duration-all projects/2026-03-11_mesita/

# Verify all drafts rendered at correct resolution
givore-tools.sh video-info-all projects/2026-03-11_mesita/
```

### Project Setup

| Command | Description |
|---------|-------------|
| `givore-tools.sh init-project <slug>` | Create single project folder (`projects/<slug>/`) |
| `givore-tools.sh init-batch <slug>` | Create batch folders (`projects/<slug>/v1-v7/` + `finals/`) |

**Use cases**:
- `/givore-create` or `/givore-trial-create`: create the project folder before saving files
- `/givore-batch`: create parent + v1-v7 + finals before batch generation

**Examples**:
```bash
# Single project (street-finds or trial)
givore-tools.sh init-project 2026-03-13_sillas-benimaclet

# Batch project with 7 variant folders
givore-tools.sh init-batch 2026-03-13_mesita-cafe-mestalla
```

### Video Pipeline

| Command | Description |
|---------|-------------|
| `givore-tools.sh assemble <config.json>` | Assemble project (JSON -> project.json + .mlt) |
| `givore-tools.sh render-draft <config.json>` | Assemble + render draft (540x960, 1000k) |
| `givore-tools.sh render-final <config.json>` | Assemble + render final (1080x1920, 8000k) |
| `givore-tools.sh render-all <project-dir> [draft\|final]` | Render all v1-v7 variants in one go |
| `givore-tools.sh generate-config --audio <mp3> --clips <ids> --project-folder <dir>` | Auto-generate assembly_config.json from audio + clip IDs |
| `givore-tools.sh place-sfx [args]` | Smart SFX placement from clip plan + subtitles |

### Quality Checks

| Command | Description |
|---------|-------------|
| `givore-tools.sh validate <config.json> [--strict]` | Pre-flight validation: checks files exist, paths are absolute, clips >= audio duration |
| `givore-tools.sh check-render <config.json> <video.mp4>` | Post-render validation: checks duration matches, aspect ratio, file size |

**Use cases**:
- Before assembly: verify config is valid (files exist, clips cover audio)
- After draft render: confirm rendered video matches expected duration
- `--strict` mode: treat warnings as errors (missing subtitles, SFX files)

**Exit codes**: 0 = pass, 1 = validation failure, 2 = usage error

**Examples**:
```bash
# Pre-flight check (recommended before every assembly)
givore-tools.sh validate /tmp/givore_assembly_config.json

# Strict mode (all warnings become errors)
givore-tools.sh validate /tmp/givore_assembly_config.json --strict

# Post-render check (recommended after every render)
givore-tools.sh check-render /tmp/givore_assembly_config.json projects/v1/draft.mp4
```

**Use cases (video pipeline)**:
- Phase B.8 / D.6: assemble and render each variant
- Phase E.3: final render of selected variants
- SFX placement: auto-generate SFX array from clip plan, SRT, and audio duration

**Examples**:
```bash
# Assemble without rendering
givore-tools.sh assemble /tmp/givore_assembly_config.json

# Draft render (fast, low quality for review)
givore-tools.sh render-draft /tmp/givore_assembly_config.json

# Final render (full quality for publishing)
givore-tools.sh render-final /tmp/givore_assembly_config.json

# Auto-place SFX based on clip plan and subtitles
givore-tools.sh place-sfx --clips /tmp/clip_plan.json --srt project/v1/video.srt \
  --audio-duration 34.5 --sfx-dir "Audio effects/" --tone energetic \
  --output /tmp/sfx_plan.json
```

### Subtitles & Captions

| Command | Description |
|---------|-------------|
| `givore-tools.sh captions <script.txt> [output.txt]` | Generate 2-3 word/line captions from script text |
| `givore-tools.sh batch-captions <project-dir>` | Generate captions for all v1-v7 variants |
| `givore-tools.sh subs <audio.mp3> <captions.txt> [output.srt]` | Generate SRT subtitles from audio + captions |
| `givore-tools.sh batch-subs <project-dir>` | Generate subtitles for all v1-v7 variants |

**Use cases**:
- After scripts written: `batch-captions` generates all caption files automatically
- After audio generated: `batch-subs` generates all subtitle files automatically
- Single variant: `captions` + `subs` for one file at a time

### Audio

| Command | Description |
|---------|-------------|
| `givore-tools.sh rename-audio <project-dir> <slug>` | Rename `tts_*.mp3` to `<slug>.mp3` in all v1-v7 |

**Use case**: After ElevenLabs audio generation, rename auto-generated filenames to pipeline-expected `[slug].mp3`.

### Batch Operations

| Command | Description |
|---------|-------------|
| `givore-tools.sh batch-status <project-dir>` | File checklist for all 7 variants |
| `givore-tools.sh copy-finals <project-dir>` | Copy all vN/*_final.mp4 to finals/ folder |

**Use case**: Quick overview of which variants have script, audio, captions, subtitles, draft, and final renders.

**Example output**:
```
VAR  SCRIPT   AUDIO    CAPTS    SUBS     DRAFT    FINAL
---  ------   -----    -----    ----     -----    -----
v1   YES      YES      YES      YES      YES      YES
v2   YES      YES      YES      YES      YES      --
...
```

---

## givore_db.py (Clip Database)

**Location**: `scripts/givore_db.py`
**DB Location**: `scripts/clips.db`
**Purpose**: SQLite repository for video clip metadata with accurate ffprobe-based durations. DB is the single source of truth for clip metadata.

**Access via givore-tools.sh**: `givore-tools.sh clips <subcommand> [args]`

### Setup

DB is already initialized. To add new clips, use the AI-driven workflow: `new` → AI categorizes → `bulk-add` (see Clip Management below).

**Clip filename prefixes**:
- `[hook]` — gesture/action clips (visual hooks); usable in hook, rehook, bridge sections
- `[bridge]` — directional transitions (e.g., "from left to sw"); connects clips by direction
- `[item]` — street-found items (approach, photograph, submit)
- `[end]` — ending clips (camera lift to sky, etc.)
- `[hook | end]` / `[hook|ending]` — dual-purpose clips
- No prefix — general cycling POV / street footage

### Query Commands

| Command | Description |
|---------|-------------|
| `givore_db.py list [--section X] [--style X] [--mood X] [--visual-hooks]` | List clips with optional filters |
| `givore_db.py search <section>` | Find all clips matching a section type |
| `givore_db.py info <id>` | Full details for one clip |

**Use cases**:
- Phase B.6 / D.5: find clips suitable for each script section
- Clip selection: filter by style + mood for variety

**Examples**:
```bash
# Find all clips usable for hook sections
givore_db.py search hook

# Find energetic cycling POV clips for hooks
givore_db.py list --section hook --style cycling_pov --mood energetic

# Find calm landmark clips for importance/solution sections
givore_db.py list --section body --style landmark --mood calm

# Show only visual hook clips
givore_db.py list --visual-hooks

# Get full details for a specific clip
givore_db.py info 12
```

### Duration Planning

| Command | Description |
|---------|-------------|
| `givore_db.py plan <audio_file> <id1,id2,...>` | Compare total clip duration vs audio duration |

**Use case**: The critical validation step. After selecting clips for a variant, verify total clip duration covers the audio. Shows exact gap or surplus.

**Example**:
```bash
givore_db.py plan projects/2026-03-11_mesita/v1/mesita.mp3 4,5,6,13,22,33,43,50,55

# Output:
# Clips total:  18.64s
# Audio total:  34.72s
# Gap:          -16.08s  *** NEED 16.08s MORE CLIPS ***
```

### Clip Management

| Command | Description |
|---------|-------------|
| `givore_db.py new` | List files not yet in DB (one filename per line) |
| `givore_db.py bulk-add <json>` | Import clips from JSON with AI-categorized metadata |
| `givore_db.py add <file> [--section X,Y] [--style X] [--mood X] [--desc "..."]` | Add single clip, auto-detect duration |
| `givore_db.py update <id> [--section X,Y] [--style X] [--mood X] [--desc "..."]` | Update metadata |
| `givore_db.py delete <id>` | Remove clip from DB |

**Use cases**:
- New clips filmed: `new` → AI categorizes → `bulk-add` (preferred workflow)
- Single clip: `add` with manual metadata
- Reclassify a clip: update section/style/mood
- Remove broken clip: delete from DB

**Examples**:
```bash
# List new clips not yet in DB
givore_db.py new

# AI-driven bulk import: AI categorizes → writes JSON → import
givore_db.py bulk-add /tmp/new_clips.json
# JSON format: [{"filename": "clip.mp4", "sections": ["body"], "style": "cycling_pov",
#                "mood": "calm", "desc": "description", "visual_hook": false}]

# Add single clip with full metadata
givore_db.py add "/media/kdabrow/Programy/givore/videos/clips/new clip.mp4" \
  --section hook,body --style cycling_pov --mood energetic --desc "New POV cycling clip"

# Reclassify clip's mood
givore_db.py update 5 --mood dramatic

# Change which sections a clip belongs to
givore_db.py update 12 --section body,bridge,problem
```

### Maintenance

| Command | Description |
|---------|-------------|
| `givore_db.py refresh` | Re-scan all files, update durations via ffprobe |
| `givore_db.py sync` | Compare DB vs filesystem, find orphans |

**Use cases**:
- After re-encoding clips: refresh to get updated durations
- After adding/removing clip files: sync to detect mismatches

---

## History Database (givore_db.py)

**Location**: `scripts/givore_db.py`
**DB Location**: `scripts/clips.db` (shared with clip data)
**Purpose**: SQLite-backed rotation tracking for scripts, trials, and video assemblies. Replaces manual SCRIPT_HISTORY.md, TRIAL_HISTORY.md, and VIDEO_HISTORY.md.

**Access via givore-tools.sh**: `givore-tools.sh <subcommand> [args]`

### Script History

| Command | Description |
|---------|-------------|
| `givore-tools.sh script-add --date X --slug X [--hook-type X] ...` | Add script history entry |
| `givore-tools.sh script-list [--last N]` | List recent script history (default 10) |
| `givore-tools.sh script-rotation [--last N]` | Compact rotation constraints (default last 3) |
| `givore-tools.sh script-delete <id>` | Delete script history entry |

**Key command**: `script-rotation` outputs all rotation constraints in ~500 bytes, replacing the need to read the full SCRIPT_HISTORY.md (~4K tokens).

### Trial History

| Command | Description |
|---------|-------------|
| `givore-tools.sh trial-add --date X --slug X [--audience X] ...` | Add trial history entry |
| `givore-tools.sh trial-list [--last N]` | List recent trial history |
| `givore-tools.sh trial-rotation [--last N]` | Compact rotation constraints |
| `givore-tools.sh trial-delete <id>` | Delete trial history entry |

### Video History

| Command | Description |
|---------|-------------|
| `givore-tools.sh video-add --date X --slug X [--clips "1,2,3"] ...` | Add video history with clips used (flat or by role) |
| `givore-tools.sh video-list [--last N]` | List recent video history with clips by role |
| `givore-tools.sh video-recent-clips [--last N]` | Unique clips used in last N videos (for exclusion) |
| `givore-tools.sh video-delete <id>` | Delete video history entry |

### Migration (one-time)

| Command | Description |
|---------|-------------|
| `givore-tools.sh migrate-all` | Import all 3 history MDs into DB |
| `givore-tools.sh migrate-scripts` | Import SCRIPT_HISTORY.md only |
| `givore-tools.sh migrate-trials` | Import TRIAL_HISTORY.md only |
| `givore-tools.sh migrate-videos` | Import VIDEO_HISTORY.md only |

---

## Pipeline Integration

How these tools map to `/givore-video` and `/givore-batch` pipeline phases:

| Pipeline Phase | Tool Command | Purpose |
|---------------|--------------|---------|
| Project setup (single) | `givore-tools.sh init-project <slug>` | Create project folder |
| Project setup (batch) | `givore-tools.sh init-batch <slug>` | Create v1-v7 + finals folders |
| B.4 / D.2: Audio generated | `givore-tools.sh duration <audio.mp3>` | Get audio length for clip planning |
| B.4 / D.2: Audio rename | `givore-tools.sh rename-audio <dir> <slug>` | Rename ElevenLabs tts_*.mp3 files |
| B.5 / D.3: Captions | `givore-tools.sh batch-captions <dir>` | Generate captions for all variants |
| B.5 / D.4: Subtitles | `givore-tools.sh batch-subs <dir>` | Generate SRT for all variants |
| B.6 / D.5: Clip selection | `givore_db.py search <section>` | Find candidate clips per section |
| B.6 / D.5: Duration validation | `givore_db.py plan <audio> <ids>` | Verify clips >= audio |
| B.8 / D.6: Pre-flight check | `givore-tools.sh validate <config>` | MANDATORY before assembly |
| B.8 / D.6: Assembly | `givore-tools.sh render-draft <config>` | Assemble + draft render |
| B.8 / D.6: Post-render check | `givore-tools.sh check-render <config> <draft.mp4>` | MANDATORY after render |
| E.2: Review | `givore-tools.sh batch-status <dir>` | Check all variants complete |
| E.2: Review | `givore-tools.sh video-info-all <dir>` | Verify all drafts rendered |
| E.3: Final render | `givore-tools.sh render-final <config>` | Full quality render (single variant) |
| E.3: Final render (all) | `givore-tools.sh render-all <dir> final` | Render all v1-v7 at full quality |
| E.3: Copy finals | `givore-tools.sh copy-finals <dir>` | Copy all finals to finals/ folder |
| B.8 / D.6: Config generation | `givore-tools.sh generate-config --audio <mp3> --clips <ids> --project-folder <dir>` | Auto-generate assembly_config.json |
| Post-batch | `givore-tools.sh duration-all <dir>` | Compare all variant lengths |
| Script rotation | `givore-tools.sh script-rotation` | Get rotation constraints before script gen |
| Trial rotation | `givore-tools.sh trial-rotation` | Get rotation constraints before trial gen |
| Clip exclusion | `givore-tools.sh video-recent-clips --last 5` | Get clips to avoid during selection |
| After script gen | `givore-tools.sh script-add --date ... --slug ...` | Record script metadata |
| After trial gen | `givore-tools.sh trial-add --date ... --slug ...` | Record trial metadata |
| After video gen | `givore-tools.sh video-add --date ... --slug ...` | Record video clips used |
