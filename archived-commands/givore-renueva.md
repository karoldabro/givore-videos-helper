# Givore Renueva Content Pipeline

Complete content creation for the Renueva channel: Item Analysis → Script + AI Image Prompts → Approval → Manual Image Gen → Audio → Captions → SRT → Metadata → Video Assembly

## Project Root

**All file paths relative to: `/media/kdabrow/Programy/givore/`**

Tool alias: `$GIVORE_TOOLS` = `/media/kdabrow/Programy/givore/scripts/givore-tools.sh`

---

## PHASE 0: INPUT COLLECTION

Collect from `$ARGUMENTS` or ask the user:

### Mandatory
1. **Item description**: What was found, what it looks like, its condition
2. **Item category**: FURNITURE | DECOR | APPLIANCE | TEXTILE | CREATIVE
3. **Source material**: Paths to screen recording(s) and optional street clip(s)
4. **Source type**: `screen-only` | `screen+street`
5. **Number of transformation ideas**: 1 (default), 2, or 3

### Optional (will use defaults)
6. **Hook style**: QUESTION | SURPRISE | VISUAL | CHALLENGE | REVEAL_TEASE (default: auto-select based on category)
7. **CTA style**: COMMENT | SAVE | FOLLOW | SHARE | QUESTION_BACK (default: auto-select)

### Project Setup
```bash
$GIVORE_TOOLS init-renueva [date]_[item-slug]
```
Store path as `$PROJECT_FOLDER`.

---

## PHASE 1: SCRIPT + IDEA + IMAGE PROMPT GENERATION

### Step 1.1: Load Context (ONE-TIME reads)
1. Read rotation constraints: `$GIVORE_TOOLS renueva-rotation --last 3`
2. Read reference files:
   - `renueva/RENUEVA_INSTRUCTIONS.md` — script structure, voice identity, branding rules
   - `renueva/RENUEVA_CATEGORIES.md` — transformation idea banks per category
   - `renueva/RENUEVA_HOOKS.md` — hook variations
   - `renueva/RENUEVA_CTAS.md` — micro-CTA variations
   - `renueva/RENUEVA_IMAGE_PROMPTS.md` — Nano Banana Pro prompt templates

### Step 1.2: Generate Transformation Idea(s)
Based on item category, condition, and RENUEVA_CATEGORIES idea banks:
- For 1 idea: Pick the BEST transformation for this specific item
- For 2-3 ideas: Pick DIFFERENT approaches (e.g., restore vs upcycle vs modernize)
- Each idea needs: technique, materials, target style, expected result

### Step 1.3: Generate Script
Follow the structure from RENUEVA_INSTRUCTIONS.md:

**Single idea (15-25s, ~85 words):**
```
[GANCHO] — Hook about the item (~10 words)
[PROBLEMA] — Found discarded, condition (~15 words)
[IDEA] — Transformation concept (~35 words)
[REVELA] — AI image reveal reaction (~20 words)
[CIERRE] — Micro-CTA (~15 words)
```

**Multi-idea (25-45s):**
```
[GANCHO] → [PROBLEMA] → [IDEA 1 + REVELA 1] → [IDEA 2 + REVELA 2] → [CIERRE]
```

**Quality checks:**
- Word count matches target (200 WPM Spanish)
- Hook type differs from last 2 entries in rotation
- CTA type differs from last 2 entries in rotation
- Item category avoids repeating last entry
- NO Givore mentions (unless this is the 1-in-5 soft mention video)
- Language: Spanish peninsular, vosotros form

Save to: `$PROJECT_FOLDER/[slug].txt`

### Step 1.4: Generate AI Image Prompt(s)
Using RENUEVA_IMAGE_PROMPTS.md templates, generate one prompt per idea:

```
Photo of a [ITEM_AFTER], [STYLE_DETAILS], in a [SETTING].
The [ITEM] has been [TRANSFORMATION]. Realistic interior design
photography, warm natural lighting, shallow depth of field, magazine quality.
```

Save prompts to: `$PROJECT_FOLDER/image_prompts.txt`

---

## PHASE 2: APPROVAL GATE 1 — Script + Ideas + Prompts

**STOP and present to user:**

```
Script generado: $PROJECT_FOLDER/[slug].txt

[Display complete script]

Idea(s) de transformacion:
1. [Idea description]

Prompt(s) para Nano Banana Pro:
[Display each prompt]

Aprobar para continuar?
- Si → Continuar con generacion de imagenes
- Editar → Cambiar script/ideas/prompts
- No → Parar aqui
```

**CRITICAL**: Do NOT proceed without explicit approval.

---

## PHASE 3: MANUAL IMAGE GENERATION (PIPELINE PAUSES)

Display clearly for the user to copy-paste:

```
GENERA LAS IMAGENES EN NANO BANANA PRO:

Prompt 1:
[Full prompt text — ready to copy]

Guarda como: $PROJECT_FOLDER/[slug]_idea1.png

[If multi-idea:]
Prompt 2:
[Full prompt text]

Guarda como: $PROJECT_FOLDER/[slug]_idea2.png

Cuando las imagenes esten guardadas, escribe "listo" para continuar.
```

**APPROVAL GATE 2**: Wait for user to confirm images are saved.

After confirmation, verify image files exist:
```bash
ls $PROJECT_FOLDER/*_idea*.png
```

---

## PHASE 4: AUDIO GENERATION (ElevenLabs)

### Voice Configuration
```yaml
voice_id: "TBD"  # Female Spanish voice — to be selected
model_id: "eleven_multilingual_v2"
language: "es"
stability: 0.45
similarity_boost: 0.75
style: 0.30
use_speaker_boost: true
speed: 1.05
output_format: "mp3_44100_128"
```

### Steps
1. Read script from `$PROJECT_FOLDER/[slug].txt`
2. Call ElevenLabs `text_to_speech` with voice config above
3. Rename audio: if generated as `tts_*.mp3`, rename to `$PROJECT_FOLDER/[slug].mp3`
4. Log duration:
   ```bash
   $GIVORE_TOOLS duration $PROJECT_FOLDER/[slug].mp3
   ```

---

## PHASE 5: CAPTIONS + SUBTITLES + METADATA

### Captions
```bash
$GIVORE_TOOLS captions $PROJECT_FOLDER/[slug].txt $PROJECT_FOLDER/captions.txt
```

### Subtitles
```bash
$GIVORE_TOOLS subs $PROJECT_FOLDER/[slug].mp3 $PROJECT_FOLDER/captions.txt
```

### Metadata
Read `renueva/RENUEVA_METADATA.md` for hashtag strategy.

Generate 3-platform metadata → `$PROJECT_FOLDER/descriptions.txt`:
1. **TikTok**: Short hook + 5-8 hashtags (mixed tiers)
2. **Instagram Reels**: Hook + 1-2 sentences + question + 8-12 hashtags
3. **YouTube Shorts**: Descriptive title + description + #shorts + 2-3 hashtags

**Givore hashtag rule**: Include #givore only if this is the ~1-in-5 soft mention video.

---

## PHASE 6: VIDEO ASSEMBLY

### Step 6.1: Build Clip Plan

Plan the visual timeline matching script sections to source material:

| Time | Section | Visual | Type | Source |
|------|---------|--------|------|--------|
| 0-3s | GANCHO | App showing item | video | screen_recording |
| 3-7s | PROBLEMA | Item detail / street | video | screen_recording or street_clip |
| 7-18s | IDEA | Item close-up | video | screen_recording |
| 18-25s | REVELA | AI image (transformed) | image | [slug]_idea1.png |
| 25-30s | CIERRE | Back to app / AI image | video/image | screen_recording |

For multi-idea: alternate between screen recording and AI image reveals.

**IMPORTANT**: The same screen recording CAN appear multiple times with different `in_point` values (different segments). This is expected.

### APPROVAL GATE 3: Clip Plan
Present the clip plan to user for approval before assembly.

### Step 6.2: Generate Assembly Config

Write config to `$PROJECT_FOLDER/assembly_config.json`:
```json
{
  "project_folder": "/absolute/path/to/project/",
  "template": "/media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json",
  "clips": [
    {"section": "GANCHO", "file": "/abs/screen_rec.mp4", "type": "video", "position": 0.0, "duration": 3.0, "in_point": 5.0},
    {"section": "REVELA", "file": "/abs/slug_idea1.png", "type": "image", "position": 18.0, "duration": 5.0}
  ],
  "sfx": [
    {"file": "/abs/path/reveal_sfx.mp3", "name": "reveal", "position": 18.0, "duration": 1.5, "volume": 0.03}
  ],
  "audio": "/abs/path/slug.mp3",
  "subtitles": "/abs/path/slug.srt",
  "subtitle_template_ass": "/media/kdabrow/Programy/givore/projects/template.kdenlive.ass"
}
```

**CRITICAL**: All paths MUST be absolute.

### Step 6.3: Validate + Assemble + Draft Render
```bash
$GIVORE_TOOLS validate $PROJECT_FOLDER/assembly_config.json
$GIVORE_TOOLS assemble $PROJECT_FOLDER/assembly_config.json
$GIVORE_TOOLS render-draft $PROJECT_FOLDER/assembly_config.json
$GIVORE_TOOLS check-render $PROJECT_FOLDER/assembly_config.json $PROJECT_FOLDER/draft.mp4
```

### SFX Guidelines (Basic Tier ONLY)
- Use 1-2 SFX for 15-30s videos (fewer than street-finds videos)
- MANDATORY: DING (Ding - Single - Bright.MP3) when AI image appears (the reveal moment)
- Optional: WHOOSH (Whoosh - Fast Short.MP3) at transition between screen recording and image
- Volume: 0.03 for ALL SFX (NEVER above 0.04)
- ONLY use Basic Tier sounds from `Audio effects/SFX_CATALOG.md`: WHOOSH, DING, CHIME, POP, SWOOSH
- Each SFX position must match a subtitle timestamp (not arbitrary placement)

---

## PHASE 7: FINAL RENDER + HISTORY

After user approves the draft:

```bash
$GIVORE_TOOLS render-final $PROJECT_FOLDER/assembly_config.json
```

Update history:
```bash
$GIVORE_TOOLS renueva-add \
  --date [YYYY-MM-DD] \
  --slug [item-slug] \
  --file $PROJECT_FOLDER/[slug].txt \
  --item-category [CATEGORY] \
  --item-description "[brief description]" \
  --transformation-ideas "[idea1, idea2]" \
  --hook-type [HOOK_TYPE] \
  --cta-type [CTA_TYPE] \
  --num-ideas [N] \
  --source-type [screen-only|screen+street]
```

### Final Summary
```
CONTENIDO RENUEVA GENERADO

Carpeta: $PROJECT_FOLDER/

Archivos:
  Script: [slug].txt
  Audio: [slug].mp3
  Imagenes AI: [slug]_idea1.png [slug]_idea2.png
  Metadatos: descriptions.txt
  Captions: captions.txt
  Subtitulos: [slug].srt
  Video draft: draft.mp4
  Video final: [slug]_final.mp4
```

---

## Error Handling

| Phase | If Error | Action |
|-------|----------|--------|
| Script Generation | Fails | Stop, show error |
| User Approval | Says "No" | Stop, script saved |
| Image Generation | User can't generate | Pause, retry later |
| Audio Generation | ElevenLabs fails | Show fallback (manual generation) |
| Metadata/Captions | Fails | Continue, show error |
| Subtitles | Fails | Show manual subs command |
| Assembly | Validation fails | Fix config, retry |
| Render | Fails | Show error, check MLT |

---

## Example Usage

Full pipeline:
```
/givore-renueva Mesita de madera con patas rotas, encontrada en Russafa. Screen recording: /path/to/screen.mp4. 2 ideas.
```

Minimal (will prompt):
```
/givore-renueva mesita de madera
```

---

**START NOW**:
1. Collect inputs (Phase 0)
2. Read reference files + rotation (Phase 1, Step 1.1)
3. Generate script + ideas + image prompts (Phase 1, Steps 1.2-1.4)
4. Present for approval (Phase 2)

$ARGUMENTS
