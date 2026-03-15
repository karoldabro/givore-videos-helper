# Givore Video Assembly Pipeline

## Command
`/givore-video` — Automated video assembly from project folder assets.

## Flow
1. **Phase 0**: Project selection (validate folder has .mp3, .srt, .txt)
2. **Phase 1**: Analysis (parse script sections, ffprobe audio, parse subtitles, load catalogs)
3. **Phase 2**: AI-driven clip + SFX selection (storytelling guidelines, NOT rigid lookup table)
4. **Phase 3**: Assembly (generate JSON config → run `assemble_video.py`) — with pre-flight validation
5. **Phase 4**: Draft render (540x960) + post-render quality check + approval gate
6. **Phase 5**: Final render (1080x1920) + update clip rotation via DB

## Architecture Principle (2026-03-15)
**Tools automate; AI decides.**
- Tools = query clips, filter by rotation, validate durations/paths, render video, check output
- AI = read clip descriptions, plan visual narrative, decide placement order, time SFX to narrative beats
- Assembly script (`assemble_video.py`) is a pure executor — places clips in the order given by config
- Quality enforcement via `validate_config()` safety nets + AI quality checklist in commands

## Key Files
- **Command**: `.claude/commands/givore-video.md`
- **Assembly script**: `scripts/assemble_video.py`
- **Config**: Written to `/tmp/givore_assembly_config.json`
- **Template**: `projects/template.kdenlive-cli.json` (profile: 1080x1920, 50fps, 9:16)
- **ASS template**: `projects/template.kdenlive.ass` (subtitle styles)
- **CLI harness**: `/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/`

## Assembly Config JSON Structure
```json
{
  "project_folder": "/absolute/path/to/project",
  "template": "/absolute/path/to/template.kdenlive-cli.json",
  "clips": [{"section": "HOOK", "file": "/abs/clip.mp4", "name": "hook_clip", "position": 0.0, "duration": 3.0, "in_point": 0.0}],
  "sfx": [{"file": "/abs/sfx.mp3", "name": "whoosh", "position": 2.8, "duration": 0.3, "volume": 0.4}],
  "audio": "/abs/narration.mp3",
  "subtitles": "/abs/subtitles.srt",
  "subtitle_template_ass": "/abs/template.kdenlive.ass"
}
```

**CRITICAL**: All paths MUST be absolute. Relative paths cause black video because melt runs from project subfolder.

## Script Sections (with timing)
HOOK (0-3s) → PROOF TEASE (3-6s) → PROBLEM (6-12s) → IMPORTANCE (12-18s) → RE-HOOK (18-21s) → SOLUTION (21-30s) → PAYOFF (30-40s) → GRATITUDE (40-45s) → CTA (45-50s)

## Tracks Generated
- V1: Video clips
- A1-Narration: Voiceover audio
- A2-SFX: Sound effects (with volume filters)
- Subtitles: kdenlivetitle text producers

## Render Settings
- Draft: 540x960, b=1000k, audio 128k
- Final: 1080x1920, CRF 18 + maxrate 8000k + preset slow, audio 192k
- Both: pix_fmt=yuv420p, SAR 1:1, progressive=1, r=50 (MUST match profile fps)
- Audio: ar=48000 channels=2

## Output Formats
- `project.json` — intermediate project format for automation pipeline
- `project.mlt` — MLT XML for melt rendering
- `project.kdenlive` — same MLT XML, openable in Kdenlive GUI for manual editing

## Catalogs
- `scripts/clips.db` — SQLite DB is single source of truth for clip metadata (CLIPS_CATALOG.md removed)
- `Audio effects/SFX_CATALOG.md` — curated sound effects
- `givore-tools.sh video-recent-clips --last 5` — rotation tracking (avoid clip reuse)

## CLI Tools (Added 2026-03-15)
- `givore-tools.sh generate-config --audio <mp3> --clips <ids> --project-folder <dir>` — auto-generate assembly_config.json from audio + ordered clip IDs (resolves paths/durations from DB, calculates sequential positions, extends last clip if needed, checks for duplicate IDs and ending clip placement)
- `givore-tools.sh render-all <project-dir> [draft|final]` — render all v1-v7 variants in one command
- `givore-tools.sh copy-finals <project-dir>` — copy all vN/*_final.mp4 to finals/ folder

## Validation Checks (Added 2026-03-15)
`validate_config()` in `assemble_video.py` enforces:
- `DUPLICATE_CLIP` — same clip file used twice in one video
- `END_CLIP_NOT_LAST` — ending clip (`[end]`, `[hook | end]`, `[hook|ending]`) not in last position
- `MULTIPLE_END_CLIPS` — more than one ending clip in a video
- `CLIPS_TOO_SHORT` — clips total duration < audio duration
- `RELATIVE_PATH` — non-absolute file paths
- `RENDER_DURATION_MISMATCH` / `RENDER_WRONG_ASPECT` — post-render checks

`cmd_generate_config()` in `givore_db.py` also checks for duplicate clip IDs and warns on ending clip misplacement.
