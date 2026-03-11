# Video Pipeline — Bugs Fixed & Lessons Learned

## Bug: Miniaturized Video
**Symptom**: Video rendered at tiny size in center of frame
**Root Cause**: DAR was 16:9 for a 1080x1920 vertical video → SAR distortion
**Fix**: Changed template `dar_num: 9, dar_den: 16` (9:16 for vertical)
**File**: `projects/template.kdenlive-cli.json`

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

## Bug: ASS Styles Not Applied
**Symptom**: Subtitles ignore template.kdenlive.ass styles
**Root Cause**: No ASS style parsing existed; config used hardcoded `subtitle_style`
**Fix**: Added `parse_ass_styles()`, `_ass_color_to_hex()`, `subtitle_template_ass` config key
**Files**: `subtitles.py`, `assemble_video.py`, `givore-video.md`
