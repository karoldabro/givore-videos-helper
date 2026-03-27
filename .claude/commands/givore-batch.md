# Givore Batch Variant Pipeline

Generate 7 variants of one topic in a single session. Variant 1 = full pipeline with approvals. Variants 2-7 = delta generation from v1 base.

## APPROVAL GATES (only 3)

1. **Gate 1**: v1 script approval (Step B.3)
2. **Gate 2**: v1 clip/video plan approval (Step B.7)
3. **Gate 3**: v1 final confirmation (Step E.2)

## AUTOMATION RULES

- Between gates, execute ALL steps without pausing
- NEVER ask "should I proceed?" between steps
- NEVER ask permission to run CLI tools — they are pre-approved
- All `$GIVORE_TOOLS` commands, ElevenLabs TTS, and file writes are pre-approved
- If a step fails, fix and continue — only ask the user if the fix requires creative input

## Constants

```
GIVORE_ROOT     = /media/kdabrow/Programy/givore
GIVORE_TOOLS    = /media/kdabrow/Programy/givore/scripts/givore-tools.sh
GIVORE_DB       = /media/kdabrow/Programy/givore/scripts/givore_db.py
TEMPLATE        = /media/kdabrow/Programy/givore/projects/template.kdenlive-cli.json
ASS_TEMPLATE    = /media/kdabrow/Programy/givore/projects/template.kdenlive.ass
```

Profile: 1080x1920 vertical, 50fps, 9:16 (TikTok/Reels)

## CLI Tools (MANDATORY)

All bash commands MUST use `$GIVORE_TOOLS`. No raw ffprobe, python, or inline bash.

| Task | Command |
|------|---------|
| **Generate variant matrix** | `$GIVORE_TOOLS batch-plan --mode <mode> --variant-count 7 --project-dir <dir>` |
| **Validate plan** | `$GIVORE_TOOLS batch-validate-plan <batch_plan.json>` |
| **Generate config with SFX** | `$GIVORE_TOOLS generate-config --audio <mp3> --clips <ids> --sfx "WHOOSH@2.8,DING@15.0" --project-folder <dir>` |
| Audio duration | `$GIVORE_TOOLS duration <file.mp3>` |
| Duration all 7 | `$GIVORE_TOOLS duration-all <project-dir>` |
| Clip search | `$GIVORE_TOOLS clips list [--section X --style Y --mood Z --visual-hooks]` |
| Duration validation | `$GIVORE_TOOLS clips plan <audio> <id1,id2,...>` |
| Pre-flight validation | `$GIVORE_TOOLS validate <config.json>` |
| Post-render validation | `$GIVORE_TOOLS check-render <config.json> <video.mp4>` |
| Assemble | `$GIVORE_TOOLS assemble <config.json>` |
| Draft render | `$GIVORE_TOOLS render-draft <config.json>` |
| Final render | `$GIVORE_TOOLS render-final <config.json>` |
| Batch captions | `$GIVORE_TOOLS batch-captions <project-dir>` |
| Batch subtitles | `$GIVORE_TOOLS batch-subs <project-dir>` |
| Rename audio | `$GIVORE_TOOLS rename-audio <project-dir> <slug>` |
| Batch thumbnails | `$GIVORE_TOOLS batch-thumbnails <project-dir>` |
| Batch status | `$GIVORE_TOOLS batch-status <project-dir>` |
| Validate all | `$GIVORE_TOOLS validate-all <project-dir>` |
| Assemble all | `$GIVORE_TOOLS assemble-all <project-dir>` |
| Render all | `$GIVORE_TOOLS render-all <project-dir> [draft\|final]` |
| Check all renders | `$GIVORE_TOOLS check-render-all <project-dir>` |
| Init batch folders | `$GIVORE_TOOLS init-batch <slug>` |
| Script rotation | `$GIVORE_TOOLS script-rotation` |
| Recent clips | `$GIVORE_TOOLS video-recent-clips --last 10` |
| Script add (v1 only) | `$GIVORE_TOOLS script-add [args]` |
| Video add (v1 only) | `$GIVORE_TOOLS video-add [args]` |
| Thumbnail add (v1 only) | `$GIVORE_TOOLS thumbnail-add [args]` |

---

## MODE DETECTION

**Street-finds** (default): Topic mentions found items, cycling, street
- Folder: `projects/[date]_[topic-slug]/`

**Trial**: Arguments contain trial keywords (RENOVATING, NEW-HOUSE, etc.)
- Folder: `projects/trial-[date]_[topic-slug]/`

---

## PHASE A: GENERATE PLAN (AUTOMATED)

### Step A.1: Create folders
```bash
$GIVORE_TOOLS init-batch [prefix][date]_[topic-slug]
```

### Step A.2: Generate variant matrix
```bash
$GIVORE_TOOLS batch-plan --mode [detected] --variant-count 7 --project-dir [parent]
```
Add `--exclude-hooks "X,Y"`, `--exclude-ctas "X,Y"`, `--location-filter "benimaclet"` if user specified.

### Step A.3: Validate plan
```bash
$GIVORE_TOOLS batch-validate-plan [parent]/batch_plan.json
```
If FAIL, re-run batch-plan with `--seed [different]`. If WARN (cycling expected), proceed.

### Step A.4: Read the plan
Read `batch_plan.json`. Each variant has pre-computed assignments:
- hook_type, cta_type, problem_angle, rehook_style, importance_angle
- proof_tease_style, solution_approach, item_intro_style
- structure, persona, persona_voice_settings
- visual_hook_clip_id

### Step A.5: Read creative rules
Read `givore-batch-creative.md` ONCE. This has all writing rules, persona markers, and uniqueness constraints.

Also read: `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`, `Audio effects/SFX_CATALOG.md`

---

## PHASE B: VARIANT 1 — FULL PIPELINE

### Step B.1: Collect Inputs (if not in $ARGUMENTS)

**Street-finds**: Topic, Items + condition, Location, Hook style, Tone, CTA goal, Reveal timing
**Trial**: Audience, Tone, Format, Marketing approach

### Step B.2: Generate v1 Script

Read v1's assignments from `batch_plan.json` (persona, structure, hook_type, etc.).
Write the script in the assigned persona's voice following the assigned structure.
Apply all rules from `givore-batch-creative.md`.

Run quality check: `python3 scripts/quality_check.py [parent]/v1/[slug].txt`

Save to: `[parent]/v1/[slug].txt`

### Step B.3: APPROVAL GATE 1 — Script

Display script. Ask: Aprobar / Editar / Cancelar.

### Step B.4: Generate Audio (ElevenLabs)

Use persona_voice_settings from batch_plan.json:
```
voice_id: "HIYif4jehvc9P9A8DYbX"
model_id: "eleven_multilingual_v2"
language: "es"
stability: [from plan]
similarity_boost: [from plan]
style: [from plan]
use_speaker_boost: true
speed: [from plan]
output_format: "mp3_44100_128"
output_directory: "[parent]/v1/"
```

### Step B.5: Metadata + Captions + Subtitles

1. Generate `descriptions.txt` (THUMBNAIL title first, then 5 platforms)
   - THUMBNAIL format: plain `THUMBNAIL\nTITLE TEXT` (no separator bars around it)
   - Follow `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`
2. Generate `captions.txt` (2-3 words/line)
3. Run: `$GIVORE_TOOLS subs [parent]/v1/[slug].mp3 [parent]/v1/captions.txt`

### Step B.6: Clip + SFX Selection (AI-DRIVEN)

**You are the video editor.** Read clip descriptions and select clips matching the narrative arc.

1. Get audio duration: `$GIVORE_TOOLS duration [parent]/v1/[slug].mp3`
2. Read SRT for subtitle timestamps
3. Query clips: `$GIVORE_TOOLS clips list` + `$GIVORE_TOOLS video-recent-clips --last 10`
4. **Select clips matching narrative energy:**
   - HOOK: Dynamic clips (reveals, gestures) — use visual_hook_clip_id from plan
   - PROBLEM: Urban reality (traffic, crossings, obstacles)
   - IMPORTANCE: Contemplative (paths, landmarks)
   - SOLUTION/PAYOFF: Calmer, scenic clips
   - CTA/ENDING: `[end]` clip MUST be last, used once only
5. **Place 2-4 SFX** using subtitle timestamps:
   - Read script to identify narrative moments (transition, reveal, solution, CTA)
   - Match to subtitle START TIME for precise positioning
   - Basic Tier only: WHOOSH, DING, CHIME, POP, SWOOSH
   - All volume = 0.03 (NEVER above 0.04)
6. Validate: `$GIVORE_TOOLS clips plan "[AUDIO]" [id1],[id2],...`

### QUALITY CHECKLIST

- [ ] No duplicate clips
- [ ] Ending clip is LAST, used once
- [ ] Clips total >= audio duration
- [ ] ONLY Basic Tier SFX, volume 0.03
- [ ] 2-4 SFX, each at a subtitle timestamp
- [ ] Min 1.5s spacing between SFX

### Step B.7: APPROVAL GATE 2 — Clip Plan

Display clip + SFX plan. Ask: Aprobar / Cambiar.

### Step B.8: Assembly + Draft Render

Generate config using the `--sfx` shorthand:
```bash
$GIVORE_TOOLS generate-config --audio [mp3] --clips [id1,id2,...] --sfx "WHOOSH@6.1,DING@37.5,POP@47.2" --project-folder [parent]/v1/
$GIVORE_TOOLS validate [parent]/v1/assembly_config.json
$GIVORE_TOOLS assemble [parent]/v1/assembly_config.json
$GIVORE_TOOLS render-draft [parent]/v1/assembly_config.json
$GIVORE_TOOLS check-render [parent]/v1/assembly_config.json [parent]/v1/draft.mp4
```

---

## PHASE D: BATCH GENERATE v2-v7 (NO APPROVALS, FINAL RENDERS)

For each variant N = 2..7:

### Step D.1: Generate Script

Read vN assignments from `batch_plan.json`. Write a COMPLETE NEW SCRIPT (not copy-paste from v1).

**KEEP CONSTANT**: Items found (factual), location name
**MUST CHANGE**: Hook (new type+wording), CTA (new type+wording), problem angle, rehook, importance, solution approach, item intro style, proof tease style. Write in assigned persona voice.

**SENTENCE-LEVEL RULE**: No sentence from any previous variant may appear verbatim.
**PHRASE-LEVEL RULE**: No 4+ word phrase in more than 2/7 variants.
**GIVEAWAY PHRASE**: Each variant uses a DIFFERENT giveaway-first phrase (see `givore-batch-creative.md`).

### Step D.2: Audio

Use persona_voice_settings from batch_plan.json for this variant's persona.

### Step D.3: Metadata

Generate descriptions.txt unique to this variant's hook/CTA. THUMBNAIL title must be unique.
THUMBNAIL format: plain `THUMBNAIL\nTITLE TEXT` (no separator bars).

### Step D.4: Captions + Subtitles

Use batch commands after all scripts are written:
```bash
$GIVORE_TOOLS batch-captions [parent]
$GIVORE_TOOLS batch-subs [parent]
```

### Step D.5: Clip + SFX Selection (AI-DRIVEN)

Same AI-driven process as B.6:
1. SWAP visual hook clip to vN's assigned clip from plan
2. SHUFFLE body clips, replace 1-2 with alternatives
3. Place 2-4 SFX at narrative moments using subtitle timing
4. Validate: `$GIVORE_TOOLS clips plan "[AUDIO]" [ids]`

### Step D.6: Assembly + FINAL Render

```bash
$GIVORE_TOOLS generate-config --audio [mp3] --clips [ids] --sfx "WHOOSH@X,DING@Y" --project-folder [parent]/vN/
$GIVORE_TOOLS validate [parent]/vN/assembly_config.json
$GIVORE_TOOLS assemble [parent]/vN/assembly_config.json
$GIVORE_TOOLS render-final [parent]/vN/assembly_config.json
$GIVORE_TOOLS check-render [parent]/vN/assembly_config.json [parent]/vN/[slug]_final.mp4
```

### Step D.7: Batch Quality Check

After ALL v2-v7 scripts written:
```bash
python3 scripts/quality_check.py --batch-dir [parent]
```
If FAIL: regenerate worst variant. If WARN: proceed.

### Step D.8: Thumbnails
```bash
$GIVORE_TOOLS batch-thumbnails [parent]
```

---

## PHASE E: REVIEW & FINALIZE

### Step E.1: Batch Status
```bash
$GIVORE_TOOLS batch-status [parent]
$GIVORE_TOOLS check-render-all [parent]
```

### Step E.2: APPROVAL GATE 3 — v1 Final

v2-v7 already rendered as finals. This gate is for v1 only:
```
v2-v7 ya renderizados en calidad final.
¿Renderizar v1 en calidad final también?
- Sí / Cambiar v1 / No (mantener borrador)
```

### Step E.3: Final Render v1

```bash
$GIVORE_TOOLS render-final [parent]/v1/assembly_config.json
```

### Step E.4: Update DB (v1 ONLY)

```bash
$GIVORE_TOOLS script-add --date X --slug X --hook-type X --cta-type X --proof-tease X --problem-angle X --rehook-style X --visual-style POV-CYCLING --lighting VARIED --item-category X --structure-type X --persona X
$GIVORE_TOOLS video-add --date X --slug X --clips [ids]
$GIVORE_TOOLS thumbnail-add --date X --slug X --bg "filename.png"
```

### Step E.5: Summary

Show folder, variants count, finals list, DB updates.

---

## SFX REFERENCE (Basic Tier)

| Name | Shorthand | Duration | Use For |
|------|-----------|----------|---------|
| WHOOSH | `WHOOSH@pos` | 0.3s | Section transitions |
| DING | `DING@pos` | 2.1s | Reveals, discoveries |
| CHIME | `CHIME@pos` | 0.9s | Positive moments |
| POP | `POP@pos` | 0.2s | CTA, app mentions |
| SWOOSH | `SWOOSH@pos` | 0.7s | Smoother transitions |

All at volume 0.03. Pass to generate-config as: `--sfx "WHOOSH@2.8,DING@15.0,POP@45.1"`

---

## CLIP SELECTION GUIDELINES

**Narrative arc — match clips to story energy:**
- **HOOK**: Dynamic clips (reveals, gestures, unexpected motion). `[hook]` clips ideal.
- **PROBLEM**: Urban reality (traffic, crossings, obstacles, near-misses)
- **IMPORTANCE**: Contemplative (paths, landmarks, shadows)
- **RE-HOOK**: Pattern interrupt — change energy abruptly
- **SOLUTION/PAYOFF**: Calmer, scenic clips (landmarks, open paths)
- **CTA/ENDING**: `[end]` clip last, always

**Visual flow:**
1. Vary motion — don't chain 5 straight-ahead POV clips
2. Match energy to narration
3. Prefer clips with personality over generic filler
4. `[bridge]` clips at section transitions, not mid-section
5. `[end]` clips MUST be last, used once

---

## ERROR HANDLING

| Phase | Error | Action |
|-------|-------|--------|
| A (Plan) | batch-plan fails | Fix args, retry |
| B (Script) | User says No | Cancel batch |
| B (Audio) | ElevenLabs fails | Show fallback |
| B (Assembly) | Validation fails | Fix clips, retry |
| D (vN) | Script quality fails | Regenerate |
| D (vN) | Assembly fails | Skip variant, log |
| E (Final) | Render fails | Show error |

---

## WORKFLOW SUMMARY

```
/givore-batch [inputs]
│
├─ PHASE A: Plan (AUTOMATED — 3 commands)
│   ├─ init-batch → batch-plan → batch-validate-plan
│   └─ Read batch_plan.json + givore-batch-creative.md
│
├─ PHASE B: Variant 1
│   ├─ Generate script (from plan assignments) → GATE 1
│   ├─ Audio + Metadata + Captions + Subtitles (AUTOMATED)
│   ├─ AI clip + SFX selection → GATE 2
│   └─ generate-config --sfx → validate → assemble → render-draft
│
├─ PHASE D: v2-v7 (NO APPROVALS, FINAL renders)
│   └─ For each: script → audio → metadata → captions → subs →
│       AI clips+SFX → generate-config --sfx → validate → assemble → render-final
│
└─ PHASE E: Finalize
    ├─ batch-status + check-render-all → GATE 3
    ├─ render-final v1
    ├─ DB updates (v1 only)
    └─ batch-thumbnails + summary
```
