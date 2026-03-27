# Givore Batch Variant Pipeline

Generate 7 variants of one topic in a single session. Variant 1 = full pipeline with approvals. Variants 2-7 = delta generation from v1 base. Each variant gets unique script, audio, metadata, and video assembly.

## APPROVAL GATES (only 3 — everything else runs automatically)

Only pause for user input at these 3 gates. Between gates, execute ALL steps automatically:
1. **Gate 1**: v1 script approval (Step B.3)
2. **Gate 2**: v1 clip/video plan approval (Step B.7)
3. **Gate 3**: v1 final confirmation + v2-v7 already rendered as finals (Step E.2)

All other steps (audio generation, captions, subtitles, metadata, clip selection, assembly, rendering) run without pausing. Use batch commands (`batch-captions`, `batch-subs`, `rename-audio`, `render-all`) to process all variants in single commands.

## AUTOMATION RULES

- Between gates, execute ALL steps without pausing for confirmation
- NEVER ask "should I proceed?" or "continuo?" between steps within a phase
- NEVER ask permission to run CLI tools — they are pre-approved
- Only pause at the 3 defined gates above
- All `$GIVORE_TOOLS` commands, ElevenLabs TTS, and file writes are pre-approved
- If a step fails, fix it and continue — do NOT ask the user unless the fix requires creative input

## Project Root

**All file paths in this command are relative to the project root: `/media/kdabrow/Programy/givore/`**

When using the Read tool or any file operation, always prepend this path. For example:
- Rotation history: `$GIVORE_TOOLS script-rotation` / `trial-rotation` / `video-recent-clips` (DB queries)
- Clip DB queries: `$GIVORE_TOOLS clips list` (see CLI Tools table below)

## Constants

```
GIVORE_ROOT     = /media/kdabrow/Programy/givore
GIVORE_TOOLS    = /media/kdabrow/Programy/givore/scripts/givore-tools.sh
GIVORE_DB       = /media/kdabrow/Programy/givore/scripts/givore_db.py
TEMPLATE        = /media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json
ASS_TEMPLATE    = /media/kdabrow/Programy/givore/projects/template.kdenlive.ass
```

Profile: 1080x1920 vertical, 30fps, 9:16 (TikTok/Reels)

## CLI Tools (MANDATORY)

All bash commands MUST use `$GIVORE_TOOLS` or `$GIVORE_DB`. Do NOT use raw ffprobe, python scripts, or inline bash loops.

| Task | Command |
|------|---------|
| Audio duration (single) | `$GIVORE_TOOLS duration <file.mp3>` |
| Audio duration (all 7) | `$GIVORE_TOOLS duration-all <project-dir>` |
| Video info (single) | `$GIVORE_TOOLS video-info <file.mp4>` |
| Video info (all 7) | `$GIVORE_TOOLS video-info-all <project-dir>` |
| Clip search | `$GIVORE_TOOLS clips search <section>` |
| Clip filter | `$GIVORE_TOOLS clips list --section X --style Y --mood Z` |
| Duration validation | `$GIVORE_TOOLS clips plan <audio> <id1,id2,...>` |
| Generate variant matrix | `$GIVORE_TOOLS batch-plan --mode <mode> --variant-count 7 --project-dir <dir>` |
| Validate plan | `$GIVORE_TOOLS batch-validate-plan <batch_plan.json>` |
| Generate config with SFX | `$GIVORE_TOOLS generate-config --audio <mp3> --clips <ids> --sfx "WHOOSH@2.8,DING@15.0" --project-folder <dir>` |
| Generate assembly config | `$GIVORE_TOOLS generate-config --audio <mp3> --clips <ids> --project-folder <dir>` |
| Pre-flight validation | `$GIVORE_TOOLS validate <config.json> [--strict]` |
| Post-render validation | `$GIVORE_TOOLS check-render <config.json> <video.mp4>` |
| Assemble project | `$GIVORE_TOOLS assemble <config.json>` |
| Draft render | `$GIVORE_TOOLS render-draft <config.json>` |
| Final render | `$GIVORE_TOOLS render-final <config.json>` |
| Subtitles (single) | `$GIVORE_TOOLS subs <audio.mp3> <captions.txt>` |
| Captions from script | `$GIVORE_TOOLS captions <script.txt> [output.txt]` |
| Batch captions (all 7) | `$GIVORE_TOOLS batch-captions <project-dir>` |
| Batch subtitles (all 7) | `$GIVORE_TOOLS batch-subs <project-dir>` |
| Rename ElevenLabs audio | `$GIVORE_TOOLS rename-audio <project-dir> <slug>` |
| Create batch folders | `$GIVORE_TOOLS init-batch <slug>` |
| Batch thumbnails (all 7) | `$GIVORE_TOOLS batch-thumbnails <project-dir>` |
| Batch status | `$GIVORE_TOOLS batch-status <project-dir>` |
| Validate all configs | `$GIVORE_TOOLS validate-all <project-dir> [--strict]` |
| Assemble all variants | `$GIVORE_TOOLS assemble-all <project-dir>` |
| Check all renders | `$GIVORE_TOOLS check-render-all <project-dir>` |
| Render all variants | `$GIVORE_TOOLS render-all <project-dir> [draft\|final]` |
| Thumbnail history | `$GIVORE_TOOLS thumbnail-add --date X --slug X --bg "1.png"` |
| Recent backgrounds | `$GIVORE_TOOLS thumbnail-recent-bgs [--last N]` |

Use `generate-config --sfx` to create assembly_config.json with SFX positions already embedded. Use `render-all` to render all v1-v7 in one command.

---

## MODE DETECTION

Detect content mode from `$ARGUMENTS`:

**Street-finds mode** (default): Topic mentions found items, cycling, street, location
- Folder prefix: `projects/[date]_[topic-slug]/`
- History: `$GIVORE_TOOLS script-rotation` (DB query)
- Reference files: 9 script refs + metadata instructions

**Trial mode**: Arguments contain trial keywords (audience names like RENOVATING, NEW-HOUSE, OLD-ITEMS, MOVING, CLUTTER, SEASONAL, or explicit "trial")
- Folder prefix: `projects/trial-[date]_[topic-slug]/`
- History: `$GIVORE_TOOLS trial-rotation` (DB query)
- Reference files: 7 trial refs + metadata instructions

Set `MODE = street-finds | trial` and use throughout.

---

## FOLDER STRUCTURE

```
projects/[prefix][date]_[topic-slug]/
├── batch_plan.json
├── v1/
│   ├── [slug].txt
│   ├── [slug].mp3
│   ├── [slug].srt
│   ├── captions.txt
│   ├── descriptions.txt
│   ├── clip_map.txt
│   ├── assembly_config.json
│   ├── project.json
│   ├── project.mlt
│   ├── draft.mp4
│   └── thumbnail.png
├── v2/ ... v7/  (same file structure, final renders stay in vN/ folders)
```

---

## PHASE A: GENERATE PLAN (AUTOMATED)

1. Create folders: `$GIVORE_TOOLS init-batch [prefix][date]_[topic-slug]`
2. Run: `$GIVORE_TOOLS batch-plan --mode [detected] --variant-count 7 --project-dir [parent]`
   Add `--exclude-hooks`, `--exclude-ctas`, `--location-filter` if user specified
3. Run: `$GIVORE_TOOLS batch-validate-plan [parent]/batch_plan.json`
4. Read `batch_plan.json` — this is your variant matrix. Each variant's assignments are pre-computed:
   - hook_type, cta_type, problem_angle, rehook_style, importance_angle
   - proof_tease_style, solution_approach, item_intro_style
   - structure, persona, persona_voice_settings
   - visual_hook_clip_id
   - clip_budget (cross-variant reuse limits)
5. Read the creative brief for v1's assigned persona and structure (see Phase B)

---

## PHASE B: VARIANT 1 — FULL PIPELINE

All reference files are loaded via batch_plan.json constraints. DO NOT read variation files manually.

### Step B.1: Collect Inputs (if not in $ARGUMENTS)

**Street-finds** — collect same inputs as `/givore-script`:
- Mandatory: Topic, Items + condition, Video structure, Location (auto-correct Valenciano to Castellano)
- Style: Hook style, Tone, CTA goal, Reveal timing
- Optional: User gratitude, Visual style, Lighting, Item category

**Trial** — collect same inputs as `/givore-trial`:
- Mandatory: Audience, Tone
- Style: Format, Marketing approach, Duration

### Step B.2: Generate v1 Script

Read your v1 assignments from `batch_plan.json`. Read `givore-batch-creative.md` for writing rules. Generate the script in the assigned persona's voice following the assigned structure.

**Street-finds**: Apply STEP 0.5 (location correction), STEP 0.8 (performance patterns), all quality checks from `/givore-script`. Generate the 8-section script.

**Trial**: Apply compatibility check, all quality checks from `/givore-trial`. Generate the script in the chosen format.

Save to: `[parent]/v1/[slug].txt`

### Step B.2b: AI Quality Check (AUTOMATED)

Spawn a quality check agent (model: haiku, fast+cheap) that receives ONLY the script + rules. It checks for issues AI can catch but regex cannot.

```
Agent(
  subagent_type: "quality-engineer",
  model: "haiku",
  mode: "bypassPermissions",
  prompt: [AI_QUALITY_PROMPT below] + script text + persona name
)
```

**AI_QUALITY_PROMPT:**
```
You are a script quality reviewer for Givore, a social recycling app in Spain.
Givore connects people who HAVE items with people who WANT them — through the app.
It is NOT about finding, collecting, or scavenging items from the street.

Review this script. Return PASS, WARN, or FAIL for each check:

## 1. LEGAL RISK — Trash encouragement (CRITICAL)
FAIL if the script implies finding, collecting, rescuing, or picking up street items.
FAIL: "para que alguien lo encuentre" (encourages taking), "alguien lo va a aprovechar" (implies taking), "rescatar de la basura", "salvar cosas"
OK: "alguien que lo necesita puede verlo en Givore" (app connection), "la gente cerca lo ve" (visibility), "conectar a quien lo tiene con quien lo quiere" (sharing)

## 2. FABRICATED FACTS (CRITICAL)
FAIL if the script claims specific past events that weren't provided as confirmed facts.
FAIL: "la semana pasada subí una cómoda y alguien la recogió", "a los diez minutos vino alguien", "una vecina del tercero lo recogió"
OK: "la gente lo usa", "funciona", "las cosas encuentran su camino"

## 3. MARKETING TONE
WARN if it sounds like an ad, pitch deck, or nonprofit newsletter. Givore should appear ONCE, briefly.

## 4. GIVEAWAY-FIRST FRAMING
WARN if missing "share before discard" messaging. FAIL if it blames anyone for leaving items.

## 5. ACCUSATORY LANGUAGE
FAIL: "nadie hace nada", "la gente no piensa", "es absurdo"

## 6. PERSONA COMPLIANCE — [PERSONA_NAME]
Check if the script matches the assigned persona's voice markers.

Return format:
Legal Risk: PASS/WARN/FAIL — [specific lines if issues]
Fabricated Facts: PASS/WARN/FAIL — [specific lines if issues]
Marketing Tone: PASS/WARN/FAIL
Giveaway Framing: PASS/WARN/FAIL
Accusatory Language: PASS/WARN/FAIL
Persona Compliance: PASS/WARN/FAIL
Overall: PASS/WARN/FAIL
```

**If FAIL on Legal Risk or Fabricated Facts**: Fix the script and re-check.
**If WARN**: Note issues, proceed to Gate 1.
**If PASS**: Proceed to Gate 1.

### Step B.3: APPROVAL GATE 1 — Script

```
Script generado: v1/[slug].txt

[Display complete script]

Aprobar script base para el batch?

- Si -> Continuar (este script sera la base para variantes 2-7)
- Editar -> Hacer cambios antes de continuar
- No -> Cancelar batch
```

**CRITICAL**: Do NOT proceed without explicit approval. This script is the foundation for all 7 variants.

### Step B.4: Generate v1 Audio (ElevenLabs)

Use `persona_voice_settings` from `batch_plan.json` for v1's assigned persona. All personas use the same base voice:

```
voice_id: "HIYif4jehvc9P9A8DYbX"
model_id: "eleven_multilingual_v2"
language: "es"
use_speaker_boost: true
output_format: "mp3_44100_128"
output_directory: "[parent]/v1/"
```

The persona-specific parameters (speed, stability, similarity_boost, style) come from `batch_plan.json`.

**Trial voice config** — use tone-specific settings from batch_plan.json (overrides persona settings).

### Step B.5: Generate v1 Metadata + Captions + Subtitles

1. Generate `descriptions.txt` (THUMBNAIL title + 5 platforms: FB, IG, LinkedIn, TikTok, YouTube)
   - THUMBNAIL section FIRST: 5-7 word uppercase hook title
   - Follow rules from `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`
   - For trial INDIRECT mode: no brand mentions in descriptions
2. Generate `captions.txt` (2-3 words/line, plain text)
3. Run subtitles: `$GIVORE_TOOLS subs [parent]/v1/[slug].mp3 [parent]/v1/captions.txt`

Save all to `[parent]/v1/`

### Step B.6: v1 Clip + SFX Selection (AI-Driven)

**You are the video editor.** Read clip descriptions and select clips that tell a visual story matching the script's narrative arc.

1. Parse script sections + get audio duration (`$GIVORE_TOOLS duration`) + parse subtitle timing
2. Query clip catalog (`$GIVORE_TOOLS clips list`) and rotation history (`$GIVORE_TOOLS video-recent-clips --last 10`)
3. Select clips matching the narrative arc:
   - **HOOK**: Dynamic clips (reveals, gestures, unexpected motion)
   - **PROBLEM/IMPORTANCE**: Urban reality clips (traffic, crossings, obstacles)
   - **RE-HOOK**: Pattern interrupt (change visual energy)
   - **SOLUTION/PAYOFF**: Calmer, scenic clips (landmarks, open paths)
   - **CTA/ENDING**: Closure — `[end]` clip last, always
4. Place SFX using Basic Tier + subtitle timing (see `/givore-video` Step 2.4 for SFX placement principles)
5. Validate duration: `$GIVORE_TOOLS clips plan "[AUDIO_FILE]" [id1],[id2],...` — clips total MUST be >= audio total
6. After deciding clips + SFX positions, generate config:
   ```bash
   $GIVORE_TOOLS generate-config --audio [parent]/v1/[slug].mp3 --clips [id1],[id2],... --sfx "WHOOSH@2.8,DING@15.0" --project-folder [parent]/v1/
   ```

### QUALITY CHECKLIST (MANDATORY — verify before assembly)

**Clip integrity:**
- [ ] No duplicate clips — each file appears exactly once
- [ ] Ending clip (`[end]`, `[hook | end]`, `[hook|ending]`) is LAST clip, used at most once
- [ ] Clips total duration >= audio duration (confirmed via `$GIVORE_TOOLS clips plan`)
- [ ] All clip paths are absolute (start with `/media/kdabrow/Programy/givore/`)

**SFX integrity:**
- [ ] ONLY Basic Tier SFX used (WHOOSH, DING, CHIME, POP, SWOOSH)
- [ ] ALL SFX volume = 0.03 (NEVER above 0.04)
- [ ] 2-4 SFX total (not more)
- [ ] Each SFX position matches a subtitle timestamp (not arbitrary)
- [ ] Minimum 1.5s spacing between SFX
- [ ] All SFX paths are absolute

**Technical specs (do NOT deviate):**
- [ ] Template: `projects/template.kdenlive-cli.json` (1080x1920, 50fps, 9:16)
- [ ] ASS template: `projects/template.kdenlive.ass`
- [ ] Profile: vertical 9:16 (NOT 16:9 — causes miniaturized video)
- [ ] FPS: 50 (NOT 25 or 30 — causes 2x duration render bug)

**NEVER proceed to assembly with clips shorter than audio** — this causes frozen last frame.

### Step B.7: APPROVAL GATE 2 — Clip Plan

```
Plan de clips y SFX:

[Display clip plan table]
[Display SFX plan table]

Aprobar plan de video?
- Si -> Ensamblar y renderizar borrador
- Cambiar -> Especifica cambios
```

### Step B.8: v1 Assembly + Draft Render

1. **MANDATORY**: Run pre-flight validation:
   ```bash
   $GIVORE_TOOLS validate [parent]/v1/assembly_config.json
   ```
   If validation fails, fix issues before proceeding.
2. Run assembly: `$GIVORE_TOOLS assemble [parent]/v1/assembly_config.json`
3. Render draft: `$GIVORE_TOOLS render-draft [parent]/v1/assembly_config.json`
4. **MANDATORY**: Run post-render validation:
   ```bash
   $GIVORE_TOOLS check-render [parent]/v1/assembly_config.json [parent]/v1/draft.mp4
   ```
   If `RENDER_DURATION_MISMATCH`, re-check clips and re-assemble.
5. Generate `clip_map.txt` in `[parent]/v1/`

### Assembly Config JSON Format

**CRITICAL**: The `sfx` array MUST follow this exact format for SFX to be audible:

```json
{
  "project_folder": "/absolute/path/to/vN/",
  "template": "$TEMPLATE",
  "clips": [
    {"section": "HOOK", "file": "/abs/path/clip.mp4", "name": "hook_clip",
     "position": 0.0, "duration": 3.0, "in_point": 0.0}
  ],
  "sfx": [
    {
      "file": "/media/kdabrow/Programy/givore/Audio effects/Whoosh - Fast Short.MP3",
      "name": "transition_whoosh",
      "position": 2.8,
      "duration": 0.3,
      "volume": 0.03
    },
    {
      "file": "/media/kdabrow/Programy/givore/Audio effects/Ding - Single - Bright.MP3",
      "name": "reveal_ding",
      "position": 4.5,
      "duration": 2.1,
      "volume": 0.03
    }
  ],
  "audio": "/abs/path/narration.mp3",
  "subtitles": "/abs/path/subtitles.srt",
  "subtitle_template_ass": "$ASS_TEMPLATE"
}
```

- All file paths MUST be absolute
- `volume`: 0.03 recommended (NEVER above 0.04 — SFX source files are loud)
- `position`: seconds from timeline start
- `duration`: how long to play (can be shorter than source file)

---

## VARIANT MATRIX DISPLAY (informational — no approval gate)

After v1 is complete, display the planned matrix for v2-v7 from `batch_plan.json` as information only, then proceed directly:

```
VARIANT MATRIX — v2-v7 planned (proceeding automatically)

| Element | v1 (done) | v2 | v3 | v4 | v5 | v6 | v7 |
|---------|-----------|----|----|----|----|----|----|
| Hook Type | ... | ... | ... | ... | ... | ... | ... |
| CTA Type | ... | ... | ... | ... | ... | ... | ... |
| Persona | ... | ... | ... | ... | ... | ... | ... |
| Structure | ... | ... | ... | ... | ... | ... | ... |

Generando variantes 2-7 automaticamente...
```

**DO NOT pause here.** Proceed directly to Phase D.

---

## PHASE D: BATCH GENERATE v2-v7 (DELTA GENERATION)

For each variant N = 2, 3, 4, 5, 6, 7 — execute ALL steps below. DO NOT re-read any reference files. Work from v1 base + `batch_plan.json` assignments.

### Step D.1: Full Rewrite Script Generation

Read v[N] assignments from `batch_plan.json`. Write a COMPLETE NEW SCRIPT in the assigned persona's voice. Do NOT copy-paste from v1 and edit. Read `givore-batch-creative.md` for writing rules.

**KEEP CONSTANT (facts only):**
- The item(s) found and their actual condition (factually accurate)
- The location/neighborhood name
- The 8-section order if using CLASSIC structure (or the assigned structure's order)

**MUST CHANGE (every variant uses its matrix assignments):**

1. **HOOK**: New hook type + wording from matrix — 1-2 new opening sentences, under 15 words, no "Hola"
2. **PROOF TEASE**: Use assigned style — if SKIP, go directly to problem section
3. **PROBLEM**: Use assigned Problem Angle — if angle repeats, rewrite with 50%+ different vocabulary
4. **IMPORTANCE**: Use assigned Importance Angle — if angle repeats, use COMPLETELY DIFFERENT template
5. **RE-HOOK**: Use assigned Rehook Style (skip if structure lacks it)
6. **SOLUTION**: Use assigned Solution Approach — use DIFFERENT app intro and demo phrasing
7. **ITEM DESCRIPTION**: Use assigned Item Intro Style — same items, DIFFERENT literary approach
8. **PAYOFF**: Rewrite completely. Same emotional conclusion, different words and sentence structure.
9. **CTA**: New CTA type + wording from matrix
10. **PERSONA**: Write in the assigned persona's voice — follow sentence length, vocabulary, transitions, emotional palette

**SENTENCE-LEVEL RULE:** No sentence from v1 (or any previous variant) may appear verbatim in this variant. If you find yourself writing a sentence that appeared before, STOP and rewrite it.

**PHRASE-LEVEL RULE:** No 4+ word phrase should appear in more than 2 out of 7 variants. Watch list:
- "lo comparto en Givore" -> vary: "lo subo" / "lo publico" / "lo dejo en Givore"
- "alguien del barrio" -> vary: "gente cerca" / "vecinos" / "alguien de por aqui"
- "en buen estado" -> vary: "perfectamente bien" / "aprovechable" / "con vida por delante"
- "esto no tendria que estar aqui" -> use ONCE maximum across 7 variants
- "Quedaos hasta el final" -> each variant needs a DIFFERENT proof tease

Save to: `[parent]/vN/[slug].txt`

### Step D.2: Audio Generation

Call ElevenLabs `text_to_speech` with the new script text. Use `persona_voice_settings` from `batch_plan.json` for variant N's assigned persona.
- `output_directory: "[parent]/vN/"`

### Step D.1b: AI Quality Check (AUTOMATED)

Same agent check as Step B.2b but for this variant's script and persona.
If FAIL on Legal Risk or Fabricated Facts: regenerate the script with specific issues noted.
If WARN or PASS: proceed.

### Step D.3: Metadata Generation (Unique per variant)

Generate `descriptions.txt` for THUMBNAIL + 5 platforms using the NEW script:
- THUMBNAIL section FIRST: 5-7 word uppercase hook title unique to this variant
- Adapt hook/CTA references to match the variant's actual hook/CTA
- Ensure at least 1 Tier 1 keyword per platform

Generate `captions.txt` (2-3 words/line from new script). Save to `[parent]/vN/`

### Step D.4: Subtitles

Run: `$GIVORE_TOOLS subs [parent]/vN/[slug].mp3 [parent]/vN/captions.txt`

### Step D.5: Clip + SFX Selection (AI-Driven)

**You are the video editor.** Apply these changes from v1's clip plan:

1. **Visual hook clips (first 1-2)**: SWAP to assigned clip from `batch_plan.json`
2. **Body clips**: SHUFFLE order of 3-5 clips AND replace 1-2 with unused alternatives from catalog
3. **Ending clip**: Keep an `[end]` clip as the very last clip
4. **SFX**: Place 2-4 Basic Tier SFX at narrative moments using subtitle timing (see `/givore-video` Step 2.4). Same sounds CAN repeat across variants.
5. **Validate duration**: `$GIVORE_TOOLS clips plan "[AUDIO_FILE]" [id1],[id2],...`
6. **Generate config with SFX**:
   ```bash
   $GIVORE_TOOLS generate-config --audio [parent]/vN/[slug].mp3 --clips [id1],[id2],... --sfx "WHOOSH@X.X,DING@Y.Y" --project-folder [parent]/vN/
   ```

Respect `clip_budget` from `batch_plan.json` — check cross-variant reuse limits before selecting.

Same QUALITY CHECKLIST from Step B.6 applies — no duplicates, ending clips last only, clips >= audio, all paths absolute.

### Step D.6: Assembly + Final Render (direct finals for v2-v7)

1. **MANDATORY**: Run pre-flight validation:
   ```bash
   $GIVORE_TOOLS validate [parent]/vN/assembly_config.json
   ```
   If validation fails, fix clips/paths before assembly.
2. Run assembly: `$GIVORE_TOOLS assemble [parent]/vN/assembly_config.json`
3. Render **final** (not draft): `$GIVORE_TOOLS render-final [parent]/vN/assembly_config.json`
   **Final render quality**: CRF 15, preset slow, maxrate 40Mbps, audio 192k
4. **MANDATORY**: Run post-render validation:
   ```bash
   $GIVORE_TOOLS check-render [parent]/vN/assembly_config.json [parent]/vN/[slug]_final.mp4
   ```
5. Generate `clip_map.txt` in `[parent]/vN/`

### Step D.6b: Thumbnail Generation (AUTOMATIC — no approval gate)

After all v1-v7 drafts are rendered, generate thumbnails:

```bash
$GIVORE_TOOLS batch-thumbnails [parent-dir]
```

### Step D.8: Cross-Variant Diversity Check (AUTOMATIC)

After ALL v2-v7 scripts are generated, run batch quality check:

```bash
python3 scripts/quality_check.py --batch-dir [parent-dir]
```

- **PASS**: proceed
- **WARN**: proceed but note areas to improve
- **FAIL**: regenerate worst-scoring variant from scratch using Step D.1, re-run check

### Progress Updates

After each variant, show brief status:

```
v[N] generada: [hook type] hook, [cta type] CTA, [persona]
   Script: vN/[slug].txt | Audio: vN/[slug].mp3 | Final: vN/[slug]_final.mp4
```

---

## PHASE E: REVIEW & FINALIZE

### Step E.0b: Cross-Variant Duration Verification

```bash
$GIVORE_TOOLS batch-status [parent-dir]
```

Review the DURATION CHECK table. All variants should show "OK".

### Step E.1: Present All 7 Drafts

```
BATCH COMPLETO — 7 variantes generadas

| # | Hook | CTA | Persona | Visual Hook | Render |
|---|------|-----|---------|-------------|--------|
| v1 | ... | ... | ... | ... | draft.mp4 |
| v2 | ... | ... | ... | ... | final.mp4 |
...
```

### Step E.2: APPROVAL GATE 3 — v1 Final Confirmation

v2-v7 are already rendered as finals. This gate only concerns v1:

```
BATCH COMPLETO

v2-v7 ya renderizados en calidad final (CRF 15, 40Mbps).
v1 tiene borrador listo para revision.

Renderizar v1 en calidad final tambien?
- Si -> Renderizar v1 final (1080x1920)
- Cambiar v1 -> Especifica cambios al video de v1
- No -> Mantener v1 como borrador
```

### Step E.3: Final Render v1

If approved: `$GIVORE_TOOLS render-final [parent]/v1/assembly_config.json`

### Step E.4: Update Global Histories (v1 ONLY)

**IMPORTANT**: Only v1 updates the global rotation histories. This prevents polluting the rotation system with 7 same-topic entries.

**Street-finds**: Run `$GIVORE_TOOLS script-add` with v1's metadata.
**Trial**: Run `$GIVORE_TOOLS trial-add` with v1's metadata.
**Both modes**: Run `$GIVORE_TOOLS video-add` with v1's clip data.
**Thumbnails**: Run `$GIVORE_TOOLS thumbnail-add --date X --slug X --bg "filename.png"` with v1's thumbnail background.

### Step E.5: Final Summary

```
BATCH GIVORE COMPLETADO

Carpeta: [parent folder]
Variantes: 7 generadas, [N] finalizadas

Finals renderizados:
  v1/[slug]_final.mp4
  v2/[slug]_final.mp4
  ...
  v7/[slug]_final.mp4

Historiales actualizados (DB):
- script-add / trial-add (solo v1)
- video-add (solo v1)
- thumbnail-add (solo v1)
```

---

## CLIP SELECTION GUIDELINES (Reference — from /givore-video Phase 2)

Use the visual storytelling principles from `/givore-video` Phase 2. You are the video editor — read clip descriptions and match them to the script's narrative arc:
- **HOOK**: Dynamic clips (reveals, gestures, unexpected motion)
- **PROBLEM/IMPORTANCE**: Urban reality clips (traffic, crossings, obstacles)
- **RE-HOOK**: Pattern interrupt (change visual energy)
- **SOLUTION/PAYOFF**: Calmer, scenic clips (landmarks, open paths)
- **CTA/ENDING**: Closure — `[end]` clip last, always

Vary motion, match energy to narration, prefer clips with personality over generic filler.

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
| Phase A (Plan) | batch-plan fails | Fix args, retry |
| Phase B (v1 Script) | Generation fails | Stop, show error |
| Phase B (v1 Approval) | User says No | Cancel entire batch |
| Phase B (v1 Audio) | ElevenLabs fails | Continue, show fallback |
| Phase B (v1 Video) | Assembly fails | Debug, retry once |
| Phase D (vN Script) | Delta fails | Skip variant, continue |
| Phase D (vN Audio) | ElevenLabs fails | Skip audio, continue |
| Phase D (vN Assembly) | Assembly fails | Skip render, log error |
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
- **location_filter**: Filter clips by location

---

## WORKFLOW SUMMARY

```
/givore-batch [inputs]
|
+- PHASE A: Generate Plan (AUTOMATED)
|   +- Create folders
|   +- batch-plan -> batch_plan.json (variant matrix + constraints)
|   +- batch-validate-plan
|
+- PHASE B: Variant 1 (Full Pipeline)
|   +- Collect inputs (if needed)
|   +- Read batch_plan.json + givore-batch-creative.md
|   +- Generate script -> APPROVAL GATE 1
|   +- Audio (ElevenLabs) + Metadata + Captions + Subtitles
|   +- Clip + SFX selection (AI-driven) -> APPROVAL GATE 2
|   +- Assembly + Draft render (generate-config --sfx)
|
+- VARIANT MATRIX DISPLAY (informational — no gate)
|
+- PHASE D: Batch Generate v2-v7 (no approvals, FINAL renders)
|   +- For each: Script -> Audio -> Metadata -> Subtitles -> Clips+SFX -> generate-config --sfx -> Assembly -> Final render
|
+- PHASE E: Review & Finalize
    +- v2-v7 already finals -> APPROVAL GATE 3 (v1 final confirmation)
    +- Final render v1 if approved
    +- Update global histories via DB (v1 only)
    +- Final summary
```

---

**START NOW**:
1. Detect mode from $ARGUMENTS (street-finds vs trial)
2. Execute Phase A: batch-plan + validate
3. Execute Phase B: Generate v1 with full pipeline (3 gates only)
4. After v1 approved, display matrix (informational) -> proceed directly to Phase D
5. Batch generate v2-v7 with FINAL renders (Phase D — no approvals)
6. Gate 3: Confirm v1 final render (Phase E)

$ARGUMENTS
