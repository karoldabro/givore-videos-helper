# Givore Video Assembly Pipeline

Automated video assembly from existing project folder: Clips + Audio + Subtitles + SFX → Draft → Approval → Final Render

## Constants

```
GIVORE_ROOT  = /media/kdabrow/Programy/givore
GIVORE_TOOLS = /media/kdabrow/Programy/givore/scripts/givore-tools.sh
GIVORE_DB    = /media/kdabrow/Programy/givore/scripts/givore_db.py
TEMPLATE     = /media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json
ASS_TEMPLATE = /media/kdabrow/Programy/givore/projects/template.kdenlive.ass
```

Profile: 1080x1920 vertical, 30fps, 9:16 (TikTok/Reels)

## CLI Tools (MANDATORY)

All bash commands MUST use `$GIVORE_TOOLS`. Do NOT use raw ffprobe, python scripts, or inline bash loops.

| Task | Command |
|------|---------|
| Audio duration | `$GIVORE_TOOLS duration <file>` |
| Clip search | `$GIVORE_TOOLS clips search <section>` |
| Clip filter | `$GIVORE_TOOLS clips list --section X --style Y --mood Z` |
| Duration validation | `$GIVORE_TOOLS clips plan <audio> <id1,id2,...>` |
| Pre-flight validation | `$GIVORE_TOOLS validate <config.json> [--strict]` |
| Post-render validation | `$GIVORE_TOOLS check-render <config.json> <video.mp4>` |
| Assemble | `$GIVORE_TOOLS assemble <config.json>` |
| Draft render | `$GIVORE_TOOLS render-draft <config.json>` |
| Final render | `$GIVORE_TOOLS render-final <config.json>` |
| Subtitles | `$GIVORE_TOOLS subs <audio> <captions>` |
| Create project folder | `$GIVORE_TOOLS init-project <slug>` |

Parallel execution is OK: multiple renders, multiple duration checks, etc. can run simultaneously.

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
$GIVORE_TOOLS duration "[AUDIO_FILE absolute path]"
```

### Step 1.4: Parse Subtitle Timing

Read `SUBTITLE_FILE` to get exact timing for each text block. Map subtitle blocks to script sections based on position.

### Step 1.5: Load Clip Database, SFX Catalog & Rotation History

Query the clip database and read SFX/history files:

```bash
# Get all clips available for this video (overview)
$GIVORE_TOOLS clips list
```

Also read (relative to GIVORE_ROOT):
- `Audio effects/SFX_GUIDELINES.md` — SFX placement rules and pool definitions (used by `place_sfx.py`)
- Run `$GIVORE_TOOLS video-recent-clips --last 5` for clip rotation history

---

## PHASE 2: CLIP + SFX SELECTION (AI-DRIVEN)

You are the video editor. Use the tools to gather information, then apply your judgment to create a compelling visual narrative.

### Step 2.1: Gather Available Clips & Rotation History

```bash
# See all available clips with descriptions, durations, and metadata
$GIVORE_TOOLS clips list

# See which clips were used recently (avoid reuse)
$GIVORE_TOOLS video-recent-clips --last 5
```

Read each clip's description carefully. The description tells you what the clip SHOWS:
- Camera motion (POV forward, looking up, turning)
- What's visible (street, stadium, bike lane, people)
- Energy level (calm cycling, dynamic turn, dramatic reveal)
- Special actions (hand gestures, near-miss, bridge transitions)
- Prefix tags: `[hook]` = attention-grabber, `[bridge]` = directional transition, `[end]` = closing motion, `[item]` = street-found item

Exclude recently used clips. If all clips of a needed type were recently used, prefer the least recently used.

### Step 2.2: Plan Visual Narrative

Read the script and subtitle timing. Plan a visual story that follows the narrative arc:

**Narrative arc — match clips to story energy:**
- **HOOK**: Grab attention — dynamic clips (reveals, gestures, unexpected motion). `[hook]` clips are ideal.
- **PROOF TEASE / PROBLEM**: Build tension — urban reality clips (traffic, crossings, obstacles, near-misses)
- **IMPORTANCE**: Weight of the issue — contemplative clips (paths, landmarks, shadows)
- **RE-HOOK**: Pattern interrupt — change visual energy abruptly (different angle, speed, or motion direction)
- **SOLUTION / PAYOFF**: Resolution — calmer, scenic clips (landmarks, open paths, pleasant cycling)
- **GRATITUDE**: Reflection — peaceful cycling, wide shots
- **CTA / ENDING**: Closure — use a clip with natural "ending" motion. Clips tagged `[end]` or `[hook | end]` show upward camera motion (sky, trees). Use exactly one, always last.

**Visual flow principles:**
1. **Vary the motion** — don't chain 5 straight-ahead POV clips. Alternate: forward POV → turn → landmark → POV → bridge
2. **Match energy to narration** — dramatic words need dynamic clips; reflective words need calm clips
3. **Prefer clips with personality** — "leaning to the right while taking a turn" has more character than generic "cycling on the street"
4. **Transitions make sense** — `[bridge]` clips (directional turns) should connect different visual contexts at section transitions, not appear randomly mid-section
5. **Ending clips close the video** — `[end]` or `[hook | end]` clips MUST be the very last clip, used at most once

**What to avoid:**
- Monotonous sequences (same style 3+ times in a row)
- Placing a high-energy clip during calm narration (or vice versa)
- Using `[bridge]` clips in the middle of a section
- Placing ending clips anywhere except the very last position

### Step 2.3: Select Clips

Use DB queries to find candidates, then select using your editorial judgment:

```bash
# Filter by section, style, mood as needed
$GIVORE_TOOLS clips list --section hook --style reveal
$GIVORE_TOOLS clips list --section body --style landmark --mood calm
```

For each clip:
- If clip is shorter than needed, extend its duration or slow down (0.8x-1.2x speed)
- If clip is longer, plan trim points (set `in_point`)

### Step 2.3b: MANDATORY Duration Validation

After selecting all clips, validate total duration:

```bash
$GIVORE_TOOLS clips plan "[AUDIO_FILE]" [id1],[id2],[id3],...
```

**RULE**: Clips total MUST be >= audio total. If gap exists:
1. Extend last clip's duration (preferred)
2. Slow down 1-2 clips (0.8x)
3. Add an additional clip from DB (must not already be in the plan)

**NEVER proceed to assembly with clips shorter than audio.**

### Step 2.4: Place SFX

Read `Audio effects/SFX_GUIDELINES.md` for available SFX pools and volume guidelines.

You decide where SFX go based on the narrative:

**Mandatory SFX (3):**
1. **Transition SFX** — place at the first major section change (e.g., HOOK → PROBLEM). Time it to the clip cut.
2. **Reveal SFX** — place when the script reveals something important (item shown, solution introduced). Time it to the narration word.
3. **Positive SFX** — place at the emotional peak (solution works, community benefit). Time it to match the sentiment.

**Optional SFX (0-2):**
- Impact/hit at RE-HOOK if the re-engagement is dramatic
- Ambient/texture during calm sections if the video feels too "dry"

**SFX timing principles:**
- Align SFX to narration beats (word emphasis) or clip cuts, not arbitrary timestamps
- Read the subtitle timing to find exact word positions for SFX triggers
- Minimum 1.5s spacing between SFX — they should punctuate, not clutter
- Volume: 0.10-0.25 (subtle enhancement, not distraction)

### Step 2.5: Generate Clip + SFX Plan

Create a structured plan:

```
CLIP PLAN — [project-name]
===============================
Section       | Clip                              | Duration | Effect          | Transition
HOOK (0-3s)   | [hook] camara view from down...   | 1.5s     | -               | cut
HOOK (1.5-3s) | [bridge] from left to sw...       | 1.5s     | -               | cut
PROBLEM (3-8s)| cycling a person crosses...        | 2.5s     | color_warm      | cut
...
CTA (45-50s)  | [end] camera moves to branches... | 2.0s     | -               | dissolve

SFX PLAN:
Timestamp  | SFX File                         | Category   | Why here
00:03.0    | Whoosh - Fast Short.MP3           | transition | HOOK→PROBLEM section cut
00:15.2    | Reveal - Musical.MP3              | reveal     | Item first mentioned in narration
00:22.0    | Correct - Synthetic Chime.MP3     | positive   | Solution introduced
```

**Present this plan to the user for review before assembly.**

---

### QUALITY CHECKLIST (MANDATORY — verify before assembly)

**Clip integrity:**
- [ ] No duplicate clips — each file appears exactly once
- [ ] Ending clip (`[end]`, `[hook | end]`, `[hook|ending]`) is LAST clip, used at most once
- [ ] Clips total duration >= audio duration (confirmed via `$GIVORE_TOOLS clips plan`)
- [ ] All clip paths are absolute (start with `/media/kdabrow/Programy/givore/`)

**SFX integrity:**
- [ ] SFX volume between 0.10-0.25 (subtle, not overpowering narration)
- [ ] Minimum 1.5s spacing between SFX
- [ ] All SFX paths are absolute
- [ ] 3 mandatory SFX present (transition, reveal, positive)

**Technical specs (from bugs-fixed history — do NOT deviate):**
- [ ] Template: `projects/template.kdenlive-cli.json` (1080x1920, 50fps, 9:16)
- [ ] ASS template: `projects/template.kdenlive.ass`
- [ ] Profile: vertical 9:16 (NOT 16:9 — causes miniaturized video)
- [ ] FPS: 50 (NOT 25 or 30 — causes 2x duration render bug)

**Run pre-flight validation:**
```bash
$GIVORE_TOOLS validate <config.json>
```
Must exit 0 before proceeding. Catches: relative paths, missing files, clips too short, duplicates, ending clip placement.

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

### Step 3.2: MANDATORY Pre-Assembly Validation

```bash
$GIVORE_TOOLS validate /tmp/givore_assembly_config.json
```

**This command MUST succeed (exit 0) before proceeding.** If it fails:
- `CLIPS_TOO_SHORT`: Go back to Step 2.3 and add clips or extend last clip
- `CLIP_FILE_MISSING` / `AUDIO_FILE_MISSING`: Fix file paths
- `RELATIVE_PATH`: Convert all paths to absolute (must start with `/media/kdabrow/Programy/givore/`)

**NEVER skip this step. NEVER proceed if validation fails.**

### Step 3.3: Run Assembly Script

```bash
$GIVORE_TOOLS assemble /tmp/givore_assembly_config.json
```

This single command handles all assembly: template copy, media import (with auto duration detection via ffprobe), track creation (V1, A1, A2-SFX, Subtitles), clip/SFX placement, subtitle import, and MLT XML export.

---

## PHASE 4: DRAFT RENDER + APPROVAL

### Step 4.1: Render Draft

```bash
$GIVORE_TOOLS render-draft /tmp/givore_assembly_config.json
```

### Step 4.1b: Post-Render Quality Check

```bash
$GIVORE_TOOLS check-render /tmp/givore_assembly_config.json [PROJECT_FOLDER]/draft.mp4
```

Verify all pass:
- [ ] Duration matches audio (within 0.5s tolerance) — `RENDER_DURATION_MISMATCH` means clips were shorter than audio
- [ ] Aspect ratio is 9:16 (540x960 for draft) — `RENDER_WRONG_ASPECT` means wrong template/profile
- [ ] File size is reasonable (not 0 bytes, not suspiciously small)
- [ ] No frozen last frame (symptom of clips shorter than audio — re-assemble with extended clips)

If any check fails, fix the issue and re-assemble + re-render before proceeding.

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
$GIVORE_TOOLS render-final /tmp/givore_assembly_config.json
```

### Step 5.2: Update Video History (DB)

Run `$GIVORE_TOOLS video-add` to record the clips used:

```bash
$GIVORE_TOOLS video-add \
  --date 2026-03-12 \
  --slug comunidad-ciudades-espana \
  --hook-clips "palms reveal,hop,black reveal" \
  --body-clips "pov2,cloudy day,pov1,..." \
  --bridge-clips "none" \
  --cta-clips "front wheel turn,unscrewing,setup camera"
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
│   ├─ Get audio duration ($GIVORE_TOOLS duration)
│   ├─ Parse subtitle timing
│   └─ Load clip DB + SFX catalog + video-recent-clips (DB)
│
├─ PHASE 2: Clip + SFX Selection
│   ├─ Map sections → clip types
│   ├─ Apply rotation rules
│   ├─ Select clips with variety
│   ├─ Select SFX (3 mandatory + 1-2 optional)
│   └─ APPROVAL GATE: Present clip + SFX plan for review
│
├─ PHASE 3: Assembly
│   ├─ Generate assembly config JSON (absolute paths!)
│   ├─ Run: $GIVORE_TOOLS validate config.json (MUST pass!)
│   └─ Run: $GIVORE_TOOLS assemble config.json
│       → template copy, media import, tracks, subtitles, SFX, MLT export
│
├─ PHASE 4: Draft Render
│   ├─ Run: $GIVORE_TOOLS render-draft config.json (540x960)
│   ├─ Run: $GIVORE_TOOLS check-render config.json draft.mp4 (verify duration)
│   ├─ Generate clip + SFX map
│   └─ APPROVAL GATE: Review draft
│
└─ PHASE 5: Final Render
    ├─ Run: $GIVORE_TOOLS render-final config.json (1080x1920)
    ├─ Update video history (DB: video-add)
    └─ Final summary
```

---

**START NOW**:
1. Check `$ARGUMENTS` — run Phase 0 (project selection)
2. Execute Phase 1 (Analysis)
3. Execute Phase 2 (Clip + SFX Selection) and present plan
4. After plan approval, execute Phases 3-5

$ARGUMENTS
