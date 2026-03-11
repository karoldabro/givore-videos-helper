# Givore Video Assembly Pipeline

Automated video assembly from existing project folder: Clips + Audio + Subtitles + SFX → Draft → Approval → Final Render

## Constants

```
GIVORE_ROOT = /media/kdabrow/Programy/givore
CLI_PYTHON  = /media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3
ASSEMBLY_SCRIPT = /media/kdabrow/Programy/givore/scripts/assemble_video.py
TEMPLATE    = /media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json
```

Profile: 1080x1920 vertical, 30fps, 9:16 (TikTok/Reels)

---

## PHASE 0: PROJECT SELECTION

### If `$ARGUMENTS` points to an existing project folder:

Verify it contains:
- At least one `.mp3` audio file
- At least one `.srt` or `.ass` subtitle file
- At least one `.txt` script file

If all present → set `PROJECT_FOLDER` to the absolute path and proceed to Phase 1.

### If `$ARGUMENTS` is empty or the folder is missing/incomplete:

Ask the user:

```
No hay proyecto completo. Opciones:

1. Dar la ruta a un proyecto existente (ej: projects/2026-02-08_muebles-cabanal)
2. Crear uno nuevo con /givore-create primero

¿Qué prefieres?
```

If user chooses option 2:
→ Execute `/givore-create` (handles script + audio + subtitles)
→ Use the resulting project folder path as `PROJECT_FOLDER`
→ Continue to Phase 1

---

## PHASE 1: ANALYSIS

**No user interaction needed.**

### Step 1.1: Validate Project Folder

Read `PROJECT_FOLDER`. Identify:
- The `.mp3` audio file → `AUDIO_FILE`
- The `.srt` or `.ass` subtitle file → `SUBTITLE_FILE`
- The `.txt` script file → `SCRIPT_FILE`

### Step 1.2: Parse Script Sections

Read `SCRIPT_FILE` and identify sections by their markers:
- **HOOK** (0-3s): Opening hook
- **PROOF TEASE** (3-6s): Tease what's coming
- **PROBLEM** (6-12s): Problem/context
- **IMPORTANCE** (12-18s): Why it matters
- **RE-HOOK** (18-21s): Re-engage viewer
- **SOLUTION** (21-30s): Present Givore/solution
- **PAYOFF** (30-40s): Show result
- **GRATITUDE** (40-45s): Thank community
- **CTA** (45-50s): Call to action

Use section markers in the script text (e.g., `[HOOK]`, `## HOOK`, or `GANCHO:`) to identify boundaries. If no explicit markers, estimate sections from the script structure.

### Step 1.3: Get Audio Duration

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "[AUDIO_FILE absolute path]"
```

### Step 1.4: Parse Subtitle Timing

Read `SUBTITLE_FILE` to get exact timing for each text block. Map subtitle blocks to script sections based on position.

### Step 1.5: Load Catalogs & Rotation History

Read these files (all relative to GIVORE_ROOT):
- `videos/clips/CLIPS_CATALOG.md` — available video clips with tags
- `Audio effects/SFX_CATALOG.md` — curated sound effects with categories
- `scripts/VIDEO_HISTORY.md` — recently used clips and SFX (for rotation)

---

## PHASE 2: CLIP + SFX SELECTION

### Step 2.1: Map Sections to Clip Types

For each script section, determine the ideal clip type:

| Script Section | Preferred Clip Style | Mood | Fallback Style |
|---------------|---------------------|------|----------------|
| HOOK | cycling_pov, reveal | energetic, dramatic | cycling_wheel |
| PROOF TEASE | cycling_pov | playful, energetic | cycling_path |
| PROBLEM | cycling_pov, transition | dramatic, contemplative | cycling_path |
| IMPORTANCE | cycling_path, landmark | calm, contemplative | cycling_wheel |
| RE-HOOK | cycling_pov, reveal | energetic, dramatic | cycling_wheel |
| SOLUTION | cycling_path, landmark | calm, energetic | cycling_pov |
| PAYOFF | landmark, cycling_path | calm, playful | cycling_pov |
| GRATITUDE | cycling_path, landmark | calm, contemplative | cycling_wheel |
| CTA | setup | calm, playful | cycling_wheel |

### Step 2.2: Apply Rotation Rules

From `scripts/VIDEO_HISTORY.md`, identify clips used in the last 5 videos. Avoid reusing those clips. If all clips of a needed type were recently used, prefer the least recently used.

### Step 2.3: Select Clips

For each section:
1. Filter catalog by matching Section tag
2. Filter by preferred Style + Mood
3. Exclude recently used clips
4. Select best match considering variety (don't use same style twice in a row)
5. If clip is shorter than section, plan to loop or slow down (0.8x-1.2x speed)
6. If clip is longer, plan trim points

### Step 2.4: Select SFX

Using `Audio effects/SFX_CATALOG.md`, select sound effects for the video:

**Mandatory SFX (always include):**
1. **Transition whoosh** at HOOK → PROOF boundary — pick from "Transition SFX" category
2. **Reveal sound** at PROOF TEASE — pick from "Reveal SFX" category
3. **Positive sound** at SOLUTION start — pick from "Positive SFX" category

**Optional SFX (pick 1-2 based on script mood):**
4. **Tension buildup** during PROBLEM — if script is dramatic
5. **Impact hit** at RE-HOOK — for energy boost
6. **CTA pop** at CTA — when app is mentioned

**Rotation rules:**
- Check `scripts/VIDEO_HISTORY.md` SFX column
- Don't reuse the same SFX in last 3 videos
- Vary energy levels (don't use all "high" energy SFX)

**Timing:**
- Place each SFX **0.1-0.2s before** the section boundary for perceived sync
- Short SFX (< 0.5s) work best for transitions
- Longer SFX (1-3s) work for reveals and buildups

### Step 2.5: Generate Clip + SFX Plan

Create a structured plan:

```
CLIP PLAN — [project-name]
===============================
Section       | Clip                              | Duration | Effect          | Transition
HOOK (0-3s)   | cyclig pov on the street 2.mp4    | 2.0s     | ken_burns_slow  | cut
PROOF (3-6s)  | cycling turning left showing...   | 1.7s     | speed_1.1x      | dissolve
PROBLEM (6-12s)| cycling beteen cars...            | 2.5s     | color_warm      | cut
...

SFX PLAN:
Timestamp  | SFX File                         | Category   | Trigger
00:02.8    | Whoosh - Fast Short.MP3           | transition | HOOK→PROOF cut
00:04.5    | Reveal - Musical.MP3              | reveal     | Item first shown
00:21.0    | Correct - Synthetic Chime.MP3     | positive   | Solution start
00:18.0    | Hit - Single.MP3                  | impact     | Re-hook (optional)
```

**Present this plan to the user for review before assembly.**

---

## PHASE 3: ASSEMBLY

After user approves the clip + SFX plan, generate an assembly config JSON and run the assembly script.

### Step 3.1: Generate Assembly Config

Write a JSON config file to `/tmp/givore_assembly_config.json`:

```json
{
  "project_folder": "/media/kdabrow/Programy/givore/projects/[folder]",
  "template": "/media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json",
  "clips": [
    {
      "section": "HOOK",
      "file": "/media/kdabrow/Programy/givore/videos/clips/[selected_clip].mp4",
      "name": "hook_clip",
      "position": 0.0,
      "duration": 3.0,
      "in_point": 0.0
    }
  ],
  "sfx": [
    {
      "file": "/media/kdabrow/Programy/givore/Audio effects/[selected_sfx].MP3",
      "name": "whoosh",
      "position": 2.8,
      "duration": 0.3,
      "volume": 0.4
    }
  ],
  "audio": "/media/kdabrow/Programy/givore/projects/[folder]/[audio_file].mp3",
  "subtitles": "/media/kdabrow/Programy/givore/projects/[folder]/[subtitle_file].srt",
  "subtitle_template_ass": "/media/kdabrow/Programy/givore/projects/template.kdenlive.ass"
}
```

**CRITICAL**: All paths MUST be absolute (starting with `/media/kdabrow/Programy/givore/`). Relative paths will cause black video output because melt runs from the project subfolder.

### Step 3.2: Run Assembly Script

```bash
/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3 /media/kdabrow/Programy/givore/scripts/assemble_video.py /tmp/givore_assembly_config.json
```

This single command handles all assembly: template copy, media import (with auto duration detection via ffprobe), track creation (V1, A1, A2-SFX, Subtitles), clip/SFX placement, subtitle import, and MLT XML export.

---

## PHASE 4: DRAFT RENDER + APPROVAL

### Step 4.1: Render Draft

```bash
/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3 /media/kdabrow/Programy/givore/scripts/assemble_video.py /tmp/givore_assembly_config.json --render-draft
```

### Step 4.2: Generate Clip Map

Save a text file showing exactly what's in the draft:

```
DRAFT CLIP MAP — [project-name]
================================
Timestamp    Section      Clip                                  Effects         Transition
00:00-00:03  [HOOK]       cyclig pov on the street 2.mp4        ken_burns_slow  cut
00:03-00:06  [PROOF]      cycling turning left showing...       speed_1.1x      dissolve
00:06-00:12  [PROBLEM]    cycling beteen cars...                 color_warm      cut
00:12-00:18  [IMPORTANCE] cycling path shadow mestalla.mp4       -               dissolve
00:18-00:21  [RE-HOOK]    public bus passing...                  -               cut
00:21-00:30  [SOLUTION]   cycling on the cycling path...         color_cool      dissolve
00:30-00:40  [PAYOFF]     stadium from left to right...          -               cut
00:40-00:45  [GRATITUDE]  cycling in the shadows...              -               dissolve
00:45-00:50  [CTA]        stittin on the bicycle.mp4             -               cut

Audio: narration_audio.mp3 (50.2s)
Subtitles: 12 entries from subtitles.srt

SFX (A2 track):
  00:02.8  Whoosh - Fast Short.MP3           [HOOK→PROOF transition]   vol: 40%
  00:04.5  Reveal - Musical.MP3              [Item reveal]             vol: 35%
  00:18.0  Hit - Single.MP3                  [Re-hook impact]          vol: 40%
  00:21.0  Correct - Synthetic Chime.MP3     [Solution start]          vol: 35%
```

Save to: `projects/[folder]/clip_map.txt`

### Step 4.3: Present for Approval

```
BORRADOR RENDERIZADO

Draft: projects/[folder]/draft.mp4
Mapa de clips: projects/[folder]/clip_map.txt

[Display clip map contents]

Aprobar video para render final?

- Si → Renderizar en calidad final (1080x1920)
- Cambiar clip → Especifica seccion y nuevo clip
- Cambiar efecto → Especifica seccion y efecto
- No → Draft guardado, puedes editarlo en Kdenlive
```

**CRITICAL**: Do NOT proceed to final render without explicit user approval.

If user requests changes:
1. Update the assembly config JSON with changes
2. Re-run assembly script
3. Re-render draft
4. Ask for approval again

---

## PHASE 5: FINAL RENDER

### Step 5.1: Render Final

```bash
/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3 /media/kdabrow/Programy/givore/scripts/assemble_video.py /tmp/givore_assembly_config.json --render-final
```

### Step 5.2: Update VIDEO_HISTORY.md

Append a new row to `scripts/VIDEO_HISTORY.md`:

```markdown
| [next#] | [date] | [project-slug] | [hook_clip] | [body_clips] | [bridge_clip] | [cta_clip] | [transitions_used] | [effects_used] | [sfx_used] |
```

### Step 5.3: Final Summary

```
VIDEO GIVORE GENERADO

Carpeta: projects/[date]_[topic-slug]/

Archivos:
- Script: [topic-slug].txt
- Audio: [topic-slug].mp3
- Subtitulos: [topic-slug].srt
- Mapa de clips: clip_map.txt
- Borrador: draft.mp4
- Video final: [topic-slug]_final.mp4
- Proyecto: project.json + project.mlt

Clips usados: [list]
SFX usados: [list with timestamps]
Duracion: [duration]s
Resolucion: 1080x1920 (9:16 vertical)
Pistas: V1 (video) + A1 (narracion) + A2 (SFX) + S1 (subtitulos)
```

---

## AVAILABLE EFFECTS

### Video Effects (via filter module)

| Effect Name | Filter | Params | Use For |
|-------------|--------|--------|---------|
| ken_burns_slow | affine | ox, oy, scale | Slow zoom on static shots |
| color_warm | avfilter.colorbalance | rs=0.1, gs=0.05, bs=-0.1 | Emotional/warm sections |
| color_cool | avfilter.colorbalance | rs=-0.1, gs=0.0, bs=0.1 | Problem/serious sections |
| brightness_up | brightness | level=1.15 | Brighten dark clips |
| vignette | vignette | - | Focus attention |
| speed_up | timewarp | speed=1.2 | Energize transitions |
| speed_down | timewarp | speed=0.8 | Dramatic moments |

### Transitions

| Type | MLT Service | Duration | Use For |
|------|-------------|----------|---------|
| cut | (none) | 0s | Energetic section changes |
| dissolve | luma | 0.5s | Smooth section transitions |
| wipe | luma | 0.3s | Dynamic transitions |

---

## INPUT

The command expects a project folder path as argument:

```
/givore-video projects/2026-02-08_muebles-cabanal
```

Or if `$ARGUMENTS` is empty, ask the user (see Phase 0).

---

## WORKFLOW SUMMARY

```
/givore-video [project-folder]
│
├─ PHASE 0: Project Selection
│   ├─ Existing folder? → Validate & continue
│   └─ Missing? → Offer /givore-create first
│
├─ PHASE 1: Analysis
│   ├─ Validate folder contents
│   ├─ Parse script sections
│   ├─ Get audio duration (ffprobe)
│   ├─ Parse subtitle timing
│   └─ Load clip catalog + SFX catalog + rotation history
│
├─ PHASE 2: Clip + SFX Selection
│   ├─ Map sections → clip types
│   ├─ Apply rotation rules
│   ├─ Select clips with variety
│   ├─ Select SFX (3 mandatory + 1-2 optional)
│   └─ APPROVAL GATE: Present clip + SFX plan for review
│
├─ PHASE 3: Assembly (1 command)
│   ├─ Generate assembly config JSON (absolute paths!)
│   └─ Run: assemble_video.py config.json
│       → template copy, media import, tracks, subtitles, SFX, MLT export
│
├─ PHASE 4: Draft Render
│   ├─ Run: assemble_video.py config.json --render-draft (540x960)
│   ├─ Generate clip + SFX map
│   └─ APPROVAL GATE: Review draft
│
└─ PHASE 5: Final Render
    ├─ Run: assemble_video.py config.json --render-final (1080x1920)
    ├─ Update VIDEO_HISTORY.md
    └─ Final summary
```

---

**START NOW**:
1. Check `$ARGUMENTS` — run Phase 0 (project selection)
2. Execute Phase 1 (Analysis)
3. Execute Phase 2 (Clip + SFX Selection) and present plan
4. After plan approval, execute Phases 3-5

$ARGUMENTS
