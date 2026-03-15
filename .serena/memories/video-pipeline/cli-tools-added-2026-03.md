# CLI Tools Added — 2026-03-15 Session

## New givore_db.py Command

### generate-config
**Purpose**: Auto-generate `assembly_config.json` from audio file + ordered clip IDs.
**Location**: `scripts/givore_db.py` → `cmd_generate_config()`

**Usage**:
```bash
givore_db.py generate-config \
  --audio /abs/path/narration.mp3 \
  --clips 19,1,43,92,82,60,... \
  --project-folder /abs/path/to/vN/
```

**What it does**:
1. Resolves clip IDs → absolute paths + durations from DB
2. Calculates sequential positions (each = prev.position + prev.duration)
3. If clips total < audio: extends last clip duration to cover gap
4. Checks for duplicate clip IDs (error)
5. Auto-detects SRT file (same basename as audio in project folder)
6. Writes `assembly_config.json` with `"sfx": []`

**Optional args**: `--template`, `--ass-template`, `--srt`

## New givore-tools.sh Commands

### render-all
**Purpose**: Render all v1-v7 variants in one command.
```bash
givore-tools.sh render-all <project-dir> [draft|final]
```
Loops through v1-v7, renders each that has an assembly_config.json.

### copy-finals
**Purpose**: Copy all `*_final.mp4` from vN/ folders to `finals/`.
```bash
givore-tools.sh copy-finals <project-dir>
```
Names them `vN_[slug]_final.mp4`.

## Typical Batch Workflow (post-session)
```bash
# 1. Generate configs for all variants
for v in v2 v3 v4 v5 v6 v7; do
  givore-tools.sh generate-config --audio "$BASE/$v/audio.mp3" --clips "19,1,43,..." --project-folder "$BASE/$v"
done

# 2. Validate all
for v in v2 v3 v4 v5 v6 v7; do
  givore-tools.sh validate "$BASE/$v/assembly_config.json"
done

# 3. Render all drafts (one command)
givore-tools.sh render-all "$BASE" draft

# 4. After review, render all finals (one command)
givore-tools.sh render-all "$BASE" final

# 5. Collect finals
givore-tools.sh copy-finals "$BASE"
```

## Bug Fix: Framerate
Added `r=50`, `frame_rate_num=50`, `frame_rate_den=1` to render() extra_args in `assemble_video.py`. Without this, melt defaults to 25fps causing 2x duration.
