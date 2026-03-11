# Givore Video Assembly Pipeline

## Command
`/givore-video` — Automated video assembly from project folder assets.

## Flow
1. **Phase 0**: Project selection (validate folder has .mp3, .srt, .txt)
2. **Phase 1**: Analysis (parse script sections, ffprobe audio, parse subtitles, load catalogs)
3. **Phase 2**: Clip + SFX selection (map sections → clips, rotation rules, present plan for approval)
4. **Phase 3**: Assembly (generate JSON config → run `assemble_video.py`)
5. **Phase 4**: Draft render (540x960) + approval gate
6. **Phase 5**: Final render (1080x1920) + update VIDEO_HISTORY.md

## Key Files
- **Command**: `.claude/commands/givore-video.md`
- **Assembly script**: `scripts/assemble_video.py`
- **Config**: Written to `/tmp/givore_assembly_config.json`
- **Template**: `projects/template.kdenlive-cli.json` (profile: 1080x1920, 30fps, 9:16)
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

## Catalogs
- `videos/clips/CLIPS_CATALOG.md` — video clips with tags
- `Audio effects/SFX_CATALOG.md` — curated sound effects
- `scripts/VIDEO_HISTORY.md` — rotation tracking (avoid reuse in last 5 videos)
