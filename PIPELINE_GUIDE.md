# Pipeline Guide — End-to-End Content Production

From a bike ride to posted videos. This guide covers every step of the Givore content pipeline.

---

## Overview

```
FILM (bike ride, 30-60 min)
  |
  v
EXTRACT clips (/givore-extract or givore-tools.sh extract-clips)
  |
  v
REVIEW & IMPORT to DB (givore_db.py bulk-add)
  |
  v
GENERATE batch (/givore-batch — 7 variants, mixed formats)
  |
  v
RENDER videos (automated, max 2 concurrent)
  |
  v
POST according to schedule (1 video every 2 days)
```

---

## Step 1: Film

Follow [FILMING_GUIDE.md](FILMING_GUIDE.md) for detailed filming instructions.

**Summary**:
- One 30-60 min ride through 2-3 barrios
- Vary speed: fast riding, slow approaches, full stops at items
- Linger 3-5 seconds on interesting moments
- Photograph found items with phone (triggers detection signals)
- Tilt camera up at the end for closing shot
- Keep camera running continuously

**Output**: One or more `.MP4` files (with `.LRF` proxy if using DJI camera).

---

## Step 2: Extract Clips

### Dry Run (Preview)

Always preview before full extraction:

```bash
givore-tools.sh extract-clips /path/to/DJI_20260328.MP4 --location ayora --dry-run
```

This runs the full analysis (CLIP + YOLO + optical flow) but only prints proposed clips without extracting them. Review the output table for clip count, timestamps, descriptions, and scores.

### Full Extraction

```bash
givore-tools.sh extract-clips /path/to/DJI_20260328.MP4 --location ayora
```

Extracted clips go to `videos/clips/`, scaled to 1080x1920 (9:16 vertical).

### Options

| Flag | Purpose | Default |
|------|---------|---------|
| `--dry-run` | Preview only, no file extraction | Off |
| `--top-percent N` | Keep top N% of detected peaks | 20 |
| `--location <name>` | Location tag for clip filenames | Required |
| `--start-time <sec>` | Skip footage before this timestamp | 0 |
| `--end-time <sec>` | Stop analysis at this timestamp | End of video |

### LRF Proxy (Automatic)

If a `.LRF` file exists alongside the `.MP4`, the pipeline uses it for analysis automatically. No flags needed. Processing time drops from ~14 min to ~2.7 min for a 6-minute video.

---

## Step 3: Review and Import

### Review Extracted Clips

The extractor writes results to `/tmp/clip_extractor_results.json`. Review the clips:

1. **Watch the extracted clips** in `videos/clips/` — verify they capture the intended moments
2. **Check auto-generated descriptions** — Moondream2 captions are used as filenames
3. **Assign type prefixes** by renaming clips that serve specific roles:

| Prefix | When to Add | Signal to Look For |
|--------|------------|-------------------|
| `[hook]` | Clip has a dramatic reveal or motion change | Sharp pan, corner turn, scene entry |
| `[item]` | Clip shows a discarded item being discovered | Approach + stop near furniture/object |
| `[end]` | Clip shows upward camera tilt or sky | Final moments, upward motion |
| `[start]` | Clip is a wide establishing shot | First moments of ride, recognizable location |
| `[bridge]` | Clip is a clear directional transition | Intersection crossing, tunnel passage |

Clips without a prefix remain as general cycling POV footage.

### Import to Database

```bash
python3 scripts/givore_db.py bulk-add /tmp/clip_extractor_results.json
```

The import auto-detects clip durations and skips duplicates already in the database.

### Verify Import

```bash
# List all clips
python3 scripts/givore_db.py list

# Check recently used clips (to avoid repetition)
givore-tools.sh video-recent-clips --last 10
```

---

## Step 4: Generate Batch

The batch pipeline generates 7 content variants from a single topic in one session.

### Run the Batch Pipeline

```
/givore-batch [topic] [items found] [location]
```

Example:
```
/givore-batch "hallazgos variados" "silla, mesita, lámpara" "benimaclet, ayora"
```

### What the Pipeline Does

1. Reads all reference files once (~12K tokens)
2. Generates v1 with full pipeline (script, audio, clip plan, assembly, render)
3. Generates v2-v7 as deltas from v1 (~7K tokens each)
4. Each variant gets: unique script, audio, metadata, video assembly

### Approval Gates (3 Only)

| Gate | When | What You Review |
|------|------|----------------|
| **v1 script** | After script generation | Script text, hook, CTA, structure |
| **v1 clip plan** | After clip selection | Clip assignments, SFX placement |
| **v1 final** | After v1 render | Watch the rendered draft video |

After v1 approval, v2-v7 generate and render without additional gates.

### Output Structure

```
projects/2026-03-28_hallazgos-variados/
  v1/
    hallazgos-variados.mp3      # Narration audio
    assembly_config.json         # Clip + SFX plan
    project.json                 # Kdenlive project data
    project.mlt                  # MLT render file
    project.kdenlive             # Kdenlive project file
    hallazgos-variados.srt       # Subtitles
    descriptions.txt             # Metadata (title, description, hashtags)
  v2/ ... v7/                    # Same structure, different content
  BATCH_MANIFEST.md              # Variant matrix (hooks, CTAs, clips per variant)
```

---

## Step 5: Render

### Automatic Rendering

The batch pipeline handles rendering. Key constraints:

- **Max 2 concurrent renders** — 7 in parallel causes duration corruption
- **v1 renders as draft first** (540x960) for review, then as final after approval
- **v2-v7 render directly as finals** (1080x1920, CRF 15, 40Mbps) — no draft step

### Manual Rendering

If you need to render or re-render outside the pipeline:

```bash
# Render all variants as finals
givore-tools.sh render-all projects/2026-03-28_hallazgos-variados/ final

# Render all variants as drafts
givore-tools.sh render-all projects/2026-03-28_hallazgos-variados/ draft

# Render a single variant
givore-tools.sh render-final /tmp/givore_assembly_config.json
```

### Post-Render Validation

```bash
# Check all rendered videos
givore-tools.sh check-render-all projects/2026-03-28_hallazgos-variados/

# Check a single render
givore-tools.sh check-render /tmp/givore_assembly_config.json projects/v1/draft.mp4
```

---

## Step 6: Post

- Follow `POSTING_SCHEDULE.md` for timing
- Spread 7 variants across 10-14 days (1 video every 2 days)
- Use Metricool for scheduling
- Metadata (title, description, hashtags) is in each variant's `descriptions.txt`

---

## Quick Reference — All Commands

### Claude Slash Commands

| Command | Purpose |
|---------|---------|
| `/givore-extract` | Extract clips from cycling footage |
| `/givore-batch` | Generate 7 content variants (street-finds or trial) |
| `/givore-create` | Single video — full pipeline (script + audio + video) |
| `/givore-video` | Video assembly only (clips + audio + subtitles) |
| `/givore-metadata` | Metadata generation only (title, description, hashtags) |
| `/givore-script` | Script generation only |
| `/givore-trial` | Trial script generation |
| `/givore-trial-create` | Trial full pipeline |
| `/givore-renueva` | Renueva single pipeline (item reuse/renovation) |
| `/givore-renueva-batch` | Renueva batch pipeline (N variants) |

### CLI Tools (givore-tools.sh)

| Command | Purpose |
|---------|---------|
| `extract-clips <video> --location <name>` | Extract clips from footage |
| `clips list` | Browse clip database |
| `video-recent-clips --last 10` | Check clip rotation (avoid reuse) |
| `script-rotation` | Check script hook/CTA rotation |
| `trial-rotation` | Check trial script rotation |
| `batch-captions <dir>` | Generate 2-3 word/line captions for all v1-v7 |
| `batch-subs <dir>` | Generate SRT subtitles for all v1-v7 |
| `batch-thumbnails <dir>` | Generate thumbnails for all v1-v7 |
| `render-all <dir> [draft\|final]` | Render all v1-v7 variants |
| `assemble-all <dir>` | Assemble (no render) all v1-v7 |
| `rename-audio <dir> <slug>` | Rename TTS `tts_*.mp3` files to `<slug>.mp3` |
| `validate <config.json>` | Pre-flight config validation |
| `validate-all <dir>` | Validate all v1-v7 configs |
| `check-render <config> <video>` | Post-render duration/aspect check |
| `check-render-all <dir>` | Post-render check for all v1-v7 |
| `duration <file>` | Get audio/video duration in seconds |
| `duration-all <dir>` | Durations for all .mp3 in v1-v7 |
| `video-info <file>` | Video dimensions + duration |
| `init-batch <slug>` | Create batch project folders (v1-v7) |
| `init-project <slug>` | Create single project folder |
| `generate-config --audio <mp3> --clips <ids> --project-folder <dir>` | Auto-generate assembly config |
| `thumbnail <args>` | Generate single thumbnail |
| `thumbnail-from-video <args>` | Generate thumbnail from video frame |

### Database Commands (givore_db.py)

| Command | Purpose |
|---------|---------|
| `python3 scripts/givore_db.py list` | List all clips in database |
| `python3 scripts/givore_db.py new` | List clip files not yet in database |
| `python3 scripts/givore_db.py bulk-add <json>` | Import clips from JSON (auto-detects durations) |
| `python3 scripts/givore_db.py script-add <args>` | Record script to rotation history |
| `python3 scripts/givore_db.py video-add --clips <ids>` | Record video + clips used |

### Quality Checks

| Command | Purpose |
|---------|---------|
| `python3 scripts/quality_check.py --batch-dir <dir>` | Validate batch diversity (8 checks) |
| `givore-tools.sh quality-check <script.txt>` | Single script quality gate |

---

## Weekly Workflow

| Day | Activity | Time Estimate |
|-----|----------|---------------|
| **Monday** | Film 1 ride (30-60 min through 2-3 barrios) | 1 hour |
| **Monday evening** | Extract clips, review, rename prefixes, import to DB | 30 min |
| **Tuesday** | Run `/givore-batch` with topic from the ride | 1-2 hours (with AI) |
| **Tuesday-Wednesday** | Review 3 approval gates, render all variants | 1 hour |
| **Thursday onward** | Post 1 video every 2 days via Metricool | 10 min per post |

This produces 7 videos per week from a single bike ride.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Clip extraction finds too few clips** | Lower `--top-percent` (default 20, try 30-40), or ride longer with more speed variation |
| **Clip extraction finds too many low-quality clips** | Lower `--top-percent` (try 10-15) to keep only the highest-scoring peaks |
| **LRF proxy not detected** | Verify `.LRF` file is in the same directory as `.MP4` with matching filename |
| **Batch diversity check fails** | Re-run `/givore-batch` — the pipeline randomizes hook/CTA/clip selection per variant |
| **Render fails with missing audio** | Check that the `.mp3` file exists in the variant folder. Run `rename-audio` if TTS output has wrong name |
| **Render fails with missing clip** | Verify all clip paths in `assembly_config.json` are absolute. Run `validate` to catch path issues |
| **Rendered video has wrong duration** | Check `check-render` output. Common cause: audio file shorter than expected (re-generate TTS) |
| **Rendered video looks over-compressed** | Finals must use CRF 15, maxrate 40Mbps. Source clips are ~45Mbps. Check render mode is `final` not `draft` |
| **TTS voice sounds wrong** | Verify persona voice settings. Pablo voice uses `eleven_multilingual_v2` model, specific stability/style per persona |
| **7 parallel renders corrupt duration** | Always max 2 concurrent renders. Use `render-all` which handles sequencing |
| **Clips all from same location** | Film across 2-3 barrios per ride. The pipeline tags clips by `--location` flag |
| **Quality check warns about phrase repetition** | Review `BATCH_MANIFEST.md` — each variant should have unique hooks and CTAs |
