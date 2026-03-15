# Video Pipeline — Bugs Fixed & Lessons Learned

## Bug: Miniaturized Video (Round 1)
**Symptom**: Video rendered at tiny size in center of frame
**Root Cause**: DAR was 16:9 for a 1080x1920 vertical video → SAR distortion
**Fix**: Changed template `dar_num: 9, dar_den: 16` (9:16 for vertical)
**File**: `projects/template.kdenlive-cli.json`

## Bug: Miniaturized Video (Round 2 — 2026-03-14)
**Symptom**: Video still rendered as tiny thumbnail despite correct DAR in template
**Root Cause**: THREE converging issues:
1. `aspect=@9:16` in melt consumer args (assemble_video.py:224) — `@` prefix sets PAR not DAR, corrupting SAR to 16:1 and DAR to 9:1
2. No `aspect_ratio=1` / `set.force_aspect_ratio=1.0` on video producers in mlt_xml.py — clips not scaled to fill frame
3. No explicit `sample_aspect_num=1/sample_aspect_den=1` in melt consumer
**Fix**:
- Removed `aspect=@9:16` from render extra_args
- Added `sample_aspect_num=1`, `sample_aspect_den=1`, `progressive=1`, `pix_fmt=yuv420p` to render
- Added `aspect_ratio=1` + `set.force_aspect_ratio=1.0` to video producers in mlt_xml.py
- Refactored render() to use quality_args (CRF 18 + maxrate for final, fixed bitrate for draft)
**Files**: `assemble_video.py`, `mlt_xml.py`

## Bug: Bad Audio Quality / Noise on Every Word
**Symptom**: Crackling/noise layered over narration
**Root Cause**: Ambient audio from video clips playing simultaneously with narration
**Fix**: Added `hide="audio"` attribute on video track entries in tractor
**File**: `mlt_xml.py` line ~219

## Bug: Subtitles Not Appearing
**Symptom**: No text visible in rendered video
**Root Cause**: kdenlivetitle reads XML from `xmldata` property, not `resource`
**Fix**: Changed `<property name="resource">` → `<property name="xmldata">`
**File**: `mlt_xml.py` line ~149

## Bug: Subtitles Render as Black Text
**Symptom**: Text appears but always black regardless of color settings
**Root Cause**: kdenlivetitle expects RGBA decimal colors (`255,255,255,255`), not hex (`#ffffff`). Also uses `font-pixel-size` not `font-size`.
**Fix**: Added `_hex_to_rgba_str()` helper, updated `_build_title_xml()` content line
**File**: `mlt_xml.py` — `_build_title_xml()` function

## Bug: Subtitles Not Centered
**Symptom**: Text left-aligned instead of centered
**Root Cause**: `alignment="1"` is left in Kdenlive. Center = `4`.
**Fix**: Changed to `alignment="4"` + `box-width` spanning frame + `x=5`
**File**: `mlt_xml.py` — `_build_title_xml()` function

## Bug: Subtitle Outline Too Thin
**Symptom**: Outline barely visible compared to template
**Root Cause**: ASS outline values are in different scale than kdenlivetitle pixels
**Fix**: Scale ASS outline by 2x in `parse_ass_styles()`
**File**: `subtitles.py` — `parse_ass_styles()` function

## Bug: 2x Duration Render (2026-03-15)
**Symptom**: Draft video renders at 101.2s instead of expected 50.6s (exactly 2x)
**Root Cause**: `render()` in `assemble_video.py` didn't pass frame rate to melt consumer. MLT profile is 50fps, but melt output defaulted to 25fps → 2530 frames / 25fps = 101.2s
**Fix**: Added `"r=50"`, `"frame_rate_num=50"`, `"frame_rate_den=1"` to the `extra` list in `render()` function
**File**: `scripts/assemble_video.py` — `render()` function, `extra` list
**Verification**: `ffprobe` output shows `r_frame_rate=50/1` and correct duration after fix

## Bug: ASS Styles Not Applied
**Symptom**: Subtitles ignore template.kdenlive.ass styles
**Root Cause**: No ASS style parsing existed; config used hardcoded `subtitle_style`
**Fix**: Added `parse_ass_styles()`, `_ass_color_to_hex()`, `subtitle_template_ass` config key
**Files**: `subtitles.py`, `assemble_video.py`, `givore-video.md`

## Bug: Duplicate Clips in Videos (2026-03-15)
**Symptom**: Same clip file appears 2+ times in a single video (confirmed in 2026-03-12 batch v2-v7)
**Root Cause**: No uniqueness check anywhere — not in commands, not in validate_config(), not in generate-config. When AI fills duration gaps ("add additional clip from DB"), it picks clips already in the plan.
**Fix**:
- Added `DUPLICATE_CLIP` check in `validate_config()` (assemble_video.py)
- Added duplicate ID check in `cmd_generate_config()` (givore_db.py)
- Added "must not already be in the plan" rule to command instructions
**Files**: `assemble_video.py`, `givore_db.py`, `givore-video.md`, `givore-batch.md`

## Bug: Ending Clips in Middle of Video (2026-03-15)
**Symptom**: Clips with upward camera motion (sky, trees) — natural video endings — placed mid-video
**Root Cause**: TWO issues:
1. No enforcement of ending clip placement — commands had no rules, validation had no checks
2. Clip #46 "cycling near to statuim mestalla camara goes up..." had ending behavior but no `[end]` prefix
**Fix**:
- Added `END_CLIP_NOT_LAST` and `MULTIPLE_END_CLIPS` checks in `validate_config()`
- Added `_is_end_clip()` helper function
- Renamed clip #46 to add `[end]` prefix, re-imported to DB
- Added ending clip placement rules to command instructions
**Files**: `assemble_video.py`, `givore_db.py`, `givore-video.md`, `givore-batch.md`, clip renamed

## Architecture: AI-Driven Assembly (2026-03-15)
**Problem**: Rigid section-to-clip lookup table produced random-feeling videos — AI had no creative control
**Root Cause**: Commands prescribed exact clip styles per section, automated SFX via place_sfx.py — removed AI judgment
**Fix**: Replaced prescriptive table with visual storytelling guidelines. AI reads clip descriptions, plans narrative arc, decides SFX timing at narrative beats. Tools provide data; AI makes creative decisions.
**Files**: `givore-video.md` (Phase 2 rewritten), `givore-batch.md` (Steps B.6, D.5 updated)
