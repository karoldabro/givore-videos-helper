# Givore Batch Variant Pipeline

Generate 7 variants of one topic in a single session. Variant 1 = full pipeline with approvals. Variants 2-7 = delta generation from v1 base. Each variant gets unique script, audio, metadata, and video assembly.

## Project Root

**All file paths in this command are relative to the project root: `/media/kdabrow/Programy/givore/`**

When using the Read tool or any file operation, always prepend this path. For example:
- `scripts/SCRIPT_HISTORY.md` → `/media/kdabrow/Programy/givore/scripts/SCRIPT_HISTORY.md`
- `videos/clips/CLIPS_CATALOG.md` → `/media/kdabrow/Programy/givore/videos/clips/CLIPS_CATALOG.md`

## Constants

```
GIVORE_ROOT     = /media/kdabrow/Programy/givore
CLI_PYTHON      = /media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3
ASSEMBLY_SCRIPT = /media/kdabrow/Programy/givore/scripts/assemble_video.py
TEMPLATE        = /media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json
ASS_TEMPLATE    = /media/kdabrow/Programy/givore/projects/template.kdenlive.ass
```

Profile: 1080x1920 vertical, 30fps, 9:16 (TikTok/Reels)

---

## MODE DETECTION

Detect content mode from `$ARGUMENTS`:

**Street-finds mode** (default): Topic mentions found items, cycling, street, location
- Folder prefix: `projects/[date]_[topic-slug]/`
- History: `scripts/SCRIPT_HISTORY.md`
- Reference files: 9 script refs + metadata instructions

**Trial mode**: Arguments contain trial keywords (audience names like RENOVATING, NEW-HOUSE, OLD-ITEMS, MOVING, CLUTTER, SEASONAL, or explicit "trial")
- Folder prefix: `projects/trial-[date]_[topic-slug]/`
- History: `scripts/TRIAL_HISTORY.md`
- Reference files: 7 trial refs + metadata instructions

Set `MODE = street-finds | trial` and use throughout.

---

## FOLDER STRUCTURE

```
projects/[prefix][date]_[topic-slug]/
├── BATCH_MANIFEST.md
├── v1/
│   ├── [slug].txt
│   ├── [slug].mp3
│   ├── [slug].srt
│   ├── captions.txt
│   ├── descriptions.txt
│   ├── clip_map.txt
│   ├── project.json
│   ├── project.mlt
│   └── draft.mp4
├── v2/ ... v7/  (same file structure)
└── finals/
    └── vN_[slug]_final.mp4  (only approved variants)
```

---

## PHASE A: BASE ANALYSIS (run once — DO NOT re-read these files later)

### Step A.1: Read History & Recent Scripts

**Street-finds**:
1. Read `scripts/SCRIPT_HISTORY.md`
2. Read last 3 script texts from paths in history (for repetition avoidance)
3. Read `scripts/VIDEO_HISTORY.md`

**Trial**:
1. Read `scripts/TRIAL_HISTORY.md`
2. Read last 2 trial script texts from paths in history
3. Read `scripts/VIDEO_HISTORY.md`

### Step A.2: Read ALL Reference Files (ONE TIME ONLY)

**Street-finds** — read all 9:
1. `CLAUDE_PROJECT_INSTRUCTIONS.md`
2. `HOOKS_LIBRARY.md`
3. `TONE_GUARDRAILS.md`
4. `CTA_VARIATIONS.md`
5. `PHRASE_VARIATIONS.md`
6. `PROBLEM_VARIATIONS.md`
7. `IMPORTANCE_VARIATIONS.md`
8. `REHOOK_VARIATIONS.md`
9. `GRATITUDE_VARIATIONS.md`

**Trial** — read all 7:
1. `trial/TRIAL_AUDIENCES.md`
2. `trial/TRIAL_FORMATS.md`
3. `trial/TRIAL_TONES.md`
4. `trial/TRIAL_MARKETING.md`
5. `trial/TRIAL_HOOKS.md`
6. `trial/TRIAL_CTAS.md`
7. `trial/TRIAL_QUALITY.md`

**Shared (both modes)**:
- `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`
- `videos/clips/CLIPS_CATALOG.md`
- `Audio effects/SFX_CATALOG.md`

### Step A.3: Compute Rotation Constraints

From history files, extract:
- Last 3 hook types → AVOID these
- Last 3 CTA types → AVOID these
- Last 3 problem angles → AVOID these (street-finds)
- Last 3 rehook styles → AVOID these (street-finds)
- Last 5 video clips used → AVOID these
- Last 3 SFX sets → AVOID these

### Step A.4: Pre-Plan Variant Matrix

Assign 7 DISTINCT values for each varying element. Select from available pools (excluding rotation constraints):

**Street-finds variant elements:**
- 7 different Hook Types (from HOOKS_LIBRARY)
- 7 different CTA Types (from CTA_VARIATIONS)
- 7 different Problem Angles (from PROBLEM_VARIATIONS)
- 7 different Rehook Styles (from REHOOK_VARIATIONS)
- 7 different Visual Hook Clips (from CLIPS_CATALOG, section=hook)
- 7 different SFX sets (transition + reveal + positive, from SFX_CATALOG)

**Trial variant elements:**
- 7 different Hook approaches (from TRIAL_HOOKS)
- 7 different CTA approaches (from TRIAL_CTAS)
- 7 different tone/wording angles
- 7 different Visual Hook Clips
- 7 different SFX sets

If fewer than 7 unique options exist for any element, cycle back to least-recently-used.

### Step A.5: Create Folder Structure + BATCH_MANIFEST.md

1. Create parent folder: `projects/[prefix][date]_[topic-slug]/`
2. Create subfolders: `v1/` through `v7/` and `finals/`
3. Write initial `BATCH_MANIFEST.md` (template below)

### BATCH_MANIFEST.md Template

```markdown
# Batch: [topic-slug]
Date: [date]
Mode: [street-finds | trial]
Topic: [full topic description]
Items: [specific items + condition]
Location: [neighborhood(s)]

## Variant Matrix

| Element | v1 | v2 | v3 | v4 | v5 | v6 | v7 |
|---------|----|----|----|----|----|----|-----|
| Hook Type | | | | | | | |
| Hook Wording (first line) | | | | | | | |
| CTA Type | | | | | | | |
| CTA Wording (last line) | | | | | | | |
| Problem Angle | | | | | | | |
| Rehook Style | | | | | | | |
| Visual Hook Clip | | | | | | | |
| Body Clip Order | | | | | | | |
| SFX: Transition | | | | | | | |
| SFX: Reveal | | | | | | | |
| SFX: Positive | | | | | | | |

## Used Elements (updated after each variant)
Hook Types: []
CTA Types: []
Problem Angles: []
Rehook Styles: []
Visual Hook Clips: []
Transition SFX: []
Reveal SFX: []
Positive SFX: []
```

---

## PHASE B: VARIANT 1 — FULL PIPELINE

Generate variant 1 using the full logic from `/givore-create` (street-finds) or `/givore-trial-create` (trial). All reference files are already loaded from Phase A — DO NOT re-read them.

### Step B.1: Collect Inputs (if not in $ARGUMENTS)

**Street-finds** — collect same inputs as `/givore-script`:
- Mandatory: Topic, Items + condition, Video structure, Location (auto-correct Valenciano → Castellano)
- Style: Hook style, Tone, CTA goal, Reveal timing
- Optional: User gratitude, Visual style, Lighting, Item category

**Trial** — collect same inputs as `/givore-trial`:
- Mandatory: Audience, Tone
- Style: Format, Marketing approach, Duration

### Step B.2: Generate v1 Script

Follow the FULL script generation logic from the respective command:

**Street-finds**: Apply STEP 0.5 (location correction), STEP 0.8 (performance patterns), all quality checks from `/givore-script`. Generate the 8-section script.

**Trial**: Apply compatibility check, all quality checks from `/givore-trial`. Generate the script in the chosen format.

Save to: `[parent]/v1/[slug].txt`

### Step B.3: APPROVAL GATE 1 — Script

```
📝 VARIANTE 1 — Script generado: v1/[slug].txt

[Display complete script]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Aprobar script base para el batch?

- Sí → Continuar (este script será la base para variantes 2-7)
- Editar → Hacer cambios antes de continuar
- No → Cancelar batch
```

**CRITICAL**: Do NOT proceed without explicit approval. This script is the foundation for all 7 variants.

### Step B.4: Generate v1 Audio (ElevenLabs)

**Street-finds voice config:**
```
voice_id: "HIYif4jehvc9P9A8DYbX"
model_id: "eleven_multilingual_v2"
language: "es"
stability: 0.35
similarity_boost: 0.4
style: 0.3
use_speaker_boost: true
speed: 1.06
output_format: "mp3_44100_128"
output_directory: "[parent]/v1/"
```

**Trial voice config** — use tone-specific settings:

| Tone | Speed | Stability | Style |
|------|-------|-----------|-------|
| HUMORISTIC | 1.10 | 0.30 | 0.35 |
| EMPATHETIC | 1.02 | 0.40 | 0.35 |
| PROVOCATIVE | 1.08 | 0.30 | 0.40 |
| DRAMATIC | 0.98 | 0.35 | 0.45 |
| RELATABLE | 1.06 | 0.35 | 0.30 |
| SARCASTIC | 1.08 | 0.25 | 0.35 |

### Step B.5: Generate v1 Metadata + Captions + Subtitles

1. Generate `descriptions.txt` (5 platforms: FB → IG → LinkedIn → TikTok → YouTube)
   - Follow rules from `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md` (already loaded)
   - For trial INDIRECT mode: no brand mentions in descriptions
2. Generate `captions.txt` (2-3 words/line, plain text)
3. Run subtitles: `subs [parent]/v1/[slug].mp3 [parent]/v1/captions.txt`

Save all to `[parent]/v1/`

### Step B.6: v1 Clip + SFX Selection

Follow the FULL clip/SFX selection logic from `/givore-video`:

1. Parse script sections + get audio duration (ffprobe) + parse subtitle timing
2. Map sections → clip types (see section-to-clip table in `/givore-video`)
3. Apply rotation rules (avoid last 5 videos from VIDEO_HISTORY)
4. Select clips with variety
5. Select SFX: 3 mandatory (transition, reveal, positive) + 1-2 optional
6. Generate clip + SFX plan

### Step B.7: APPROVAL GATE 2 — Clip Plan

```
🎬 VARIANTE 1 — Plan de clips y SFX:

[Display clip plan table]
[Display SFX plan table]

¿Aprobar plan de video?
- Sí → Ensamblar y renderizar borrador
- Cambiar → Especifica cambios
```

### Step B.8: v1 Assembly + Draft Render

1. Generate assembly config JSON → `/tmp/givore_batch_v1_config.json`
   - **CRITICAL**: All paths MUST be absolute
2. Run assembly: `$CLI_PYTHON $ASSEMBLY_SCRIPT /tmp/givore_batch_v1_config.json`
3. Render draft: `$CLI_PYTHON $ASSEMBLY_SCRIPT /tmp/givore_batch_v1_config.json --render-draft`
4. Generate `clip_map.txt` → save to `[parent]/v1/`

### Step B.9: Update BATCH_MANIFEST v1

Fill in the v1 column in the Variant Matrix table and update Used Elements lists.

---

## PHASE C: VARIANT MATRIX APPROVAL

### Step C.1: Display Planned Matrix

Present the full variant matrix showing what will change for v2-v7:

```
📊 VARIANT MATRIX — Planned differences for v2-v7

| Element | v1 (done) | v2 | v3 | v4 | v5 | v6 | v7 |
|---------|-----------|----|----|----|----|----|----|
| Hook Type | OUTRAGE | COMMUNITY | URGENCY | QUESTION | JOURNEY | BOLD | EMOTIONAL |
| CTA Type | COMMUNITY | ENGAGEMENT | DOWNLOAD | SAVE-SHARE | FOLLOW | AWARENESS | SHARING |
| Problem Angle | SYSTEM-WASTE | MISSED-CONN | URBAN-TREAS | TIME-SENS | NEIGHBOR-UNK | COULD-SHARE | SYSTEM-WASTE |
| Visual Hook | [clip1] | [clip2] | [clip3] | [clip4] | [clip5] | [clip6] | [clip7] |
| SFX Trans | [sfx1] | [sfx2] | [sfx3] | [sfx4] | [sfx5] | [sfx6] | [sfx7] |
...

Cada variante tendrá: script único, audio único, metadatos únicos, video diferente.
```

### Step C.2: APPROVAL GATE 3 — Matrix

```
¿Aprobar la matriz de variantes?

- Sí → Generar variantes 2-7 automáticamente
- Modificar → Cambiar asignaciones específicas
```

After approval, proceed to batch generation. No further approval gates until all 7 drafts are ready.

---

## PHASE D: BATCH GENERATE v2-v7 (DELTA GENERATION)

For each variant N = 2, 3, 4, 5, 6, 7 — execute ALL steps below. DO NOT re-read any reference files. Work from v1 base + BATCH_MANIFEST assignments.

### Step D.1: Delta Script Generation

Start from v1 script text and apply these substitutions:

1. **HOOK section**: Replace with new hook type + wording from matrix assignment
   - Write 1-2 new opening sentences matching the assigned hook type
   - Keep under 15 words, no "Hola"

2. **CTA section**: Replace with new CTA type + wording from matrix assignment
   - Write new closing matching the assigned CTA type

3. **RE-HOOK section** (street-finds): Replace with new rehook style
   - Write new re-engagement line

4. **PROBLEM section** (street-finds): Reframe using assigned problem angle
   - Same facts, different emotional framing

5. **Body wording**: Tweak 2-3 sentences in IMPORTANCE/SOLUTION/PAYOFF
   - Different word choices, varied sentence structure
   - Ensure no repeated phrases across variants

6. **Keep constant**: Core message, items, condition, location, section structure

Save to: `[parent]/vN/[slug].txt`

### Step D.2: Audio Generation

Call ElevenLabs `text_to_speech` with the new script text.
- Use same voice config as v1 (same mode-specific settings)
- `output_directory: "[parent]/vN/"`

### Step D.3: Metadata Generation (Unique per variant)

Generate `descriptions.txt` for 5 platforms using the NEW script:
- Adapt hook/CTA references to match the variant's actual hook/CTA
- Follow same platform rules (already internalized from Phase A)
- Ensure at least 1 Tier 1 keyword per platform
- NO re-reading `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`

Generate `captions.txt` (2-3 words/line from new script).

Save to `[parent]/vN/`

### Step D.4: Subtitles

Run: `subs [parent]/vN/[slug].mp3 [parent]/vN/captions.txt`

### Step D.5: Video Delta — Clip + SFX Selection

Apply these changes from v1's clip plan:

1. **Visual hook clips (first 1-2)**: SWAP to assigned clip from matrix
2. **Body clips**: SHUFFLE order of 3-5 clips AND replace 1-2 with unused alternatives from catalog
3. **SFX**: Use different effects from each mandatory category per matrix assignment
4. **Keep**: Same section-to-clip-type mapping, same transition logic

Generate new clip + SFX plan (no approval gate — matrix was already approved).

### Step D.6: Assembly + Draft Render

1. Write assembly config → `/tmp/givore_batch_vN_config.json`
   - Point `project_folder` to `[parent]/vN/`
   - All paths absolute
2. Run assembly: `$CLI_PYTHON $ASSEMBLY_SCRIPT /tmp/givore_batch_vN_config.json`
3. Render draft: `$CLI_PYTHON $ASSEMBLY_SCRIPT /tmp/givore_batch_vN_config.json --render-draft`
4. Generate `clip_map.txt` → save to `[parent]/vN/`

### Step D.7: Update BATCH_MANIFEST

Fill in vN column in Variant Matrix and update Used Elements lists.

### Progress Updates

After each variant, show brief status:

```
✅ v[N] generada: [hook type] hook, [cta type] CTA, [visual hook clip]
   Script: vN/[slug].txt | Audio: vN/[slug].mp3 | Draft: vN/draft.mp4
```

---

## PHASE E: REVIEW & FINALIZE

### Step E.1: Present All 7 Drafts

```
📊 BATCH COMPLETO — 7 variantes generadas

| # | Hook | CTA | Visual Hook | Draft |
|---|------|-----|-------------|-------|
| v1 | OUTRAGE: "¿En serio..." | COMMUNITY | red bus clip | v1/draft.mp4 |
| v2 | COMMUNITY: "Vecinos..." | ENGAGEMENT | pov street 2 | v2/draft.mp4 |
| v3 | URGENCY: "Hoy..." | DOWNLOAD | pov street 3 | v3/draft.mp4 |
| v4 | QUESTION: "¿Sabéis...?" | SAVE-SHARE | bus passing | v4/draft.mp4 |
| v5 | JOURNEY: "Pedaleando..." | FOLLOW | pov torre | v5/draft.mp4 |
| v6 | BOLD: "Una lavadora..." | AWARENESS | steering cross | v6/draft.mp4 |
| v7 | EMOTIONAL: "Cada hallazgo..." | SHARING | pov street 5 | v7/draft.mp4 |

Todos los borradores están en: [parent folder]
```

### Step E.2: APPROVAL GATE 4 — Select Finals

```
¿Qué variantes renderizar en calidad final?

- Todas → Renderizar las 7 (1080x1920)
- Seleccionar → Indica números (ej: 1,3,5)
- Ninguna → Solo mantener borradores
```

### Step E.3: Final Render (Selected Variants)

For each selected variant:
1. Run: `$CLI_PYTHON $ASSEMBLY_SCRIPT /tmp/givore_batch_vN_config.json --render-final`
2. Move/copy final to: `[parent]/finals/vN_[slug]_final.mp4`

### Step E.4: Update Global Histories (v1 ONLY)

**IMPORTANT**: Only v1 updates the global rotation histories. This prevents polluting the rotation system with 7 same-topic entries.

**Street-finds**: Update `scripts/SCRIPT_HISTORY.md` with v1's data (shift rows, add v1 as row 1, keep 10 max).

**Trial**: Update `scripts/TRIAL_HISTORY.md` with v1's data.

**Both modes**: Update `scripts/VIDEO_HISTORY.md` with v1's clip/SFX data.

### Step E.5: Final Summary

```
✅ BATCH GIVORE COMPLETADO

📁 Carpeta: [parent folder]
📊 Variantes: 7 generadas, [N] finalizadas

Finals renderizados:
├── finals/v1_[slug]_final.mp4
├── finals/v3_[slug]_final.mp4
└── finals/v5_[slug]_final.mp4

Manifest: BATCH_MANIFEST.md (detalle de todas las variantes)

Historiales actualizados:
- SCRIPT_HISTORY.md (solo v1)
- VIDEO_HISTORY.md (solo v1)
```

---

## SECTION-TO-CLIP MAPPING (Reference — from /givore-video)

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

## AVAILABLE EFFECTS (Reference — from /givore-video)

| Effect | Filter | Use For |
|--------|--------|---------|
| ken_burns_slow | affine | Static shots |
| color_warm | colorbalance | Emotional sections |
| color_cool | colorbalance | Problem/serious |
| brightness_up | brightness | Dark clips |
| vignette | vignette | Focus attention |
| speed_up | timewarp 1.2 | Energize |
| speed_down | timewarp 0.8 | Dramatic |

## TRANSITIONS

| Type | Duration | Use For |
|------|----------|---------|
| cut | 0s | Energetic changes |
| dissolve | 0.5s | Smooth transitions |
| wipe | 0.3s | Dynamic transitions |

---

## ERROR HANDLING

| Phase | Error | Action |
|-------|-------|--------|
| Phase A (Analysis) | Missing ref file | Warn, continue with available |
| Phase B (v1 Script) | Generation fails | Stop, show error |
| Phase B (v1 Approval) | User says No | Cancel entire batch |
| Phase B (v1 Audio) | ElevenLabs fails | Continue, show fallback |
| Phase B (v1 Video) | Assembly fails | Debug, retry once |
| Phase D (vN Script) | Delta fails | Skip variant, continue |
| Phase D (vN Audio) | ElevenLabs fails | Skip audio, continue |
| Phase D (vN Assembly) | Assembly fails | Skip render, log in manifest |
| Phase E (Final Render) | Render fails | Show error, try next |

If ElevenLabs rate-limits during batch: pause 30 seconds between calls.

---

## INPUT COLLECTION

Same inputs as `/givore-create` (street-finds) or `/givore-trial-create` (trial).

If `$ARGUMENTS` is empty or incomplete, collect all mandatory inputs first.

### Optional Batch-Specific Inputs:
- **variant_count**: Number of variants (default: 7, range: 2-7)
- **exclude_hooks**: Hook types to exclude from matrix
- **exclude_ctas**: CTA types to exclude from matrix

---

## WORKFLOW SUMMARY

```
/givore-batch [inputs]
│
├─ PHASE A: Base Analysis (ONE-TIME file reads)
│   ├─ Read history + last scripts
│   ├─ Read ALL reference files (9 or 7 depending on mode)
│   ├─ Read catalogs (clips + SFX)
│   ├─ Compute rotation constraints
│   ├─ Pre-plan variant matrix (7 hooks, 7 CTAs, 7 clips, 7 SFX)
│   └─ Create folder structure + BATCH_MANIFEST.md
│
├─ PHASE B: Variant 1 (Full Pipeline)
│   ├─ Collect inputs (if needed)
│   ├─ Generate script → ⏸ APPROVAL GATE 1
│   ├─ Audio (ElevenLabs) + Metadata + Captions + Subtitles
│   ├─ Clip + SFX selection → ⏸ APPROVAL GATE 2
│   └─ Assembly + Draft render
│
├─ PHASE C: Variant Matrix Approval
│   └─ Display matrix → ⏸ APPROVAL GATE 3
│
├─ PHASE D: Batch Generate v2-v7 (no approvals)
│   └─ For each: Delta script → Audio → Metadata → Subtitles → Video delta → Assembly → Draft
│
└─ PHASE E: Review & Finalize
    ├─ Present all 7 drafts → ⏸ APPROVAL GATE 4 (select finals)
    ├─ Final render selected variants
    ├─ Update global histories (v1 only)
    └─ Final summary
```

---

**START NOW**:
1. Detect mode from $ARGUMENTS (street-finds vs trial)
2. Execute Phase A: Read ALL reference files, compute constraints, plan matrix
3. Execute Phase B: Generate v1 with full pipeline
4. After v1 approval, present matrix (Phase C)
5. Batch generate v2-v7 (Phase D)
6. Review and finalize (Phase E)

$ARGUMENTS
