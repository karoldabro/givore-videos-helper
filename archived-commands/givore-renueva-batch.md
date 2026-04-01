# Givore Renueva Batch Pipeline

Generate N variants of one item in a single session. Same item, different transformation ideas, different AI images, different scripts.

## Project Root

**All file paths relative to: `/media/kdabrow/Programy/givore/`**

Tool alias: `$GIVORE_TOOLS` = `/media/kdabrow/Programy/givore/scripts/givore-tools.sh`

---

## PHASE A: BASE ANALYSIS (ONE-TIME)

### Step A.1: Collect Inputs
From `$ARGUMENTS` or ask:
1. **Item description**: What, condition, where found
2. **Item category**: FURNITURE | DECOR | APPLIANCE | TEXTILE | CREATIVE
3. **Source material**: Screen recording path(s), optional street clip(s)
4. **Source type**: `screen-only` | `screen+street`
5. **Number of variants (N)**: How many variants to generate (default: 3)

### Step A.2: Create Project Structure
```bash
$GIVORE_TOOLS init-renueva-batch [date]_[item-slug] [N]
```
Store path as `$BATCH_DIR`.

### Step A.3: Read Reference Files (ONCE — saves ~12K tokens)
Read ALL of these once, reuse across all variants:
- `renueva/RENUEVA_INSTRUCTIONS.md`
- `renueva/RENUEVA_CATEGORIES.md`
- `renueva/RENUEVA_HOOKS.md`
- `renueva/RENUEVA_CTAS.md`
- `renueva/RENUEVA_IMAGE_PROMPTS.md`
- `renueva/RENUEVA_METADATA.md`
- `Audio effects/SFX_CATALOG.md`

### Step A.4: Load Rotation Constraints
```bash
$GIVORE_TOOLS renueva-rotation --last 3
```

### Step A.5: Pre-Plan Variant Matrix
Plan ALL N variants upfront to ensure diversity:

| Element | v1 | v2 | v3 | ... | vN |
|---------|----|----|----|----|-----|
| Transformation idea | [unique per variant] | | | | |
| Hook type | [rotate across variants] | | | | |
| CTA type | [rotate across variants] | | | | |
| SFX (1-2 Basic Tier) | [vary] | | | | |

**Rules:**
- Each variant gets a DIFFERENT transformation idea (the creative core)
- Hook types rotate (no two consecutive variants share hook type)
- CTA types rotate similarly
- All variants share: item description, source material, voice config

Generate ALL N image prompts now (one per variant).

---

## PHASE B: VARIANT 1 (FULL PIPELINE)

### Step B.1: Script + Ideas
Generate v1 script following RENUEVA_INSTRUCTIONS structure.
Save to: `$BATCH_DIR/v1/[slug].txt`
Save image prompt to: `$BATCH_DIR/v1/image_prompts.txt`

### >>> GATE 1: Script Approval
Present v1 script + all N image prompts for approval.

### Step B.2: Image Generation (SINGLE PAUSE FOR ALL N VARIANTS)

Display ALL N prompts at once for the user to generate:

```
GENERA TODAS LAS IMAGENES EN NANO BANANA PRO:

=== VARIANTE 1 ===
Prompt: [full prompt]
Guarda como: $BATCH_DIR/v1/[slug]_idea1.png

=== VARIANTE 2 ===
Prompt: [full prompt]
Guarda como: $BATCH_DIR/v2/[slug]_idea1.png

[... for all N variants]

Cuando TODAS las imagenes esten guardadas, escribe "listo".
```

### >>> GATE 2: Images Ready
Wait for user confirmation. Verify all image files exist.

### Step B.3: Audio + Captions + Subs + Metadata for v1
```bash
# Audio (ElevenLabs)
# [same voice config as givore-renueva.md]

# Captions
$GIVORE_TOOLS captions $BATCH_DIR/v1/[slug].txt $BATCH_DIR/v1/captions.txt

# Subtitles
$GIVORE_TOOLS subs $BATCH_DIR/v1/[slug].mp3 $BATCH_DIR/v1/captions.txt

# Metadata → $BATCH_DIR/v1/descriptions.txt
```

### Step B.4: Video Assembly for v1
Build clip plan for v1. Present for approval.

### >>> GATE 3: Video Plan Approval

Assemble + draft render:
```bash
$GIVORE_TOOLS validate $BATCH_DIR/v1/assembly_config.json
$GIVORE_TOOLS assemble $BATCH_DIR/v1/assembly_config.json
$GIVORE_TOOLS render-draft $BATCH_DIR/v1/assembly_config.json
```

---

## PHASE C: VARIANT MATRIX APPROVAL

### >>> GATE 4: Matrix Approval

Present the full variant matrix:

```
MATRIZ DE VARIANTES (N variantes):

| # | Idea | Hook | CTA | Diferencias clave |
|---|------|------|-----|-------------------|
| v1 | [idea] | [hook] | [cta] | [base version] |
| v2 | [idea] | [hook] | [cta] | [what changes from v1] |
| v3 | [idea] | [hook] | [cta] | [what changes from v1] |
| ... | | | | |

Aprobar matriz? (Si / Editar / Cancelar)
```

Save matrix as `$BATCH_DIR/BATCH_MANIFEST.md`.

---

## PHASE D: BATCH GENERATE v2-vN (NO APPROVALS)

For each variant v2 through vN, automatically:

### Delta Rules (what changes from v1)
- **ALWAYS changes**: Transformation idea (the core creative concept), AI image, hook wording, CTA wording
- **MAY change**: 2-3 body sentences adapted to the new idea, problem angle framing, SFX choice (Basic Tier only: WHOOSH, DING, CHIME, POP, SWOOSH; volume 0.03; 1-2 per video)
- **NEVER changes**: Item description, source material, voice config, section structure, video profile

### Per Variant (automated, ~7K tokens each):
1. **Generate delta script**: Swap IDEA + REVELA sections, adjust GANCHO and CIERRE for new hook/CTA type
2. **Save script**: `$BATCH_DIR/vN/[slug].txt`
3. **Generate audio**: ElevenLabs with same voice config
4. **Rename audio**: If needed, to `$BATCH_DIR/vN/[slug].mp3`
5. **Generate captions**: `$GIVORE_TOOLS captions $BATCH_DIR/vN/[slug].txt $BATCH_DIR/vN/captions.txt`
6. **Generate subtitles**: `$GIVORE_TOOLS subs $BATCH_DIR/vN/[slug].mp3 $BATCH_DIR/vN/captions.txt`
7. **Generate metadata**: Adapted for variant's specific idea
8. **Build clip plan**: Same source material structure, AI image swapped for this variant's image
9. **Assemble + draft render**:
   ```bash
   $GIVORE_TOOLS validate $BATCH_DIR/vN/assembly_config.json
   $GIVORE_TOOLS assemble $BATCH_DIR/vN/assembly_config.json
   $GIVORE_TOOLS render-draft $BATCH_DIR/vN/assembly_config.json
   ```

### Progress Tracking
After each variant, show:
```
v2: Script + Audio + Video DONE
v3: Script + Audio + Video DONE
...
```

---

## PHASE E: REVIEW + FINALIZE

### Step E.1: Check All Drafts
```bash
$GIVORE_TOOLS batch-status $BATCH_DIR
```

Note: `batch-status` iterates v1-v7 by default. For N > 7 or N < 7, verify manually.

### Step E.2: Present All Drafts

```
TODAS LAS VARIANTES GENERADAS:

v1: [slug] — Idea: [brief] — Hook: [type] — Draft: draft.mp4
v2: [slug] — Idea: [brief] — Hook: [type] — Draft: draft.mp4
...

Cuales quieres renderizar como finales? (ej: "v1, v3, v5" o "todas")
```

### >>> GATE 5: Final Selection

### Step E.3: Final Render
For each selected variant:
```bash
$GIVORE_TOOLS render-final $BATCH_DIR/vN/assembly_config.json
```

Or render all at once:
```bash
$GIVORE_TOOLS render-all $BATCH_DIR final
```

### Step E.4: Update History (v1 ONLY)
Only v1 updates global rotation to prevent pollution:
```bash
$GIVORE_TOOLS renueva-add \
  --date [YYYY-MM-DD] \
  --slug [item-slug] \
  --file $BATCH_DIR/v1/[slug].txt \
  --item-category [CATEGORY] \
  --item-description "[description]" \
  --transformation-ideas "[v1 idea]" \
  --hook-type [V1_HOOK] \
  --cta-type [V1_CTA] \
  --num-ideas 1 \
  --source-type [type]
```

### Final Summary
```
BATCH RENUEVA COMPLETADO

Carpeta: $BATCH_DIR/
Variantes: N
Finales: [count] renderizados en carpetas vN/

Archivos por variante:
  [slug].txt, [slug].mp3, [slug]_idea1.png,
  captions.txt, descriptions.txt, [slug].srt,
  assembly_config.json, draft.mp4, [slug]_final.mp4
```

---

## Token Budget Estimate
- Phase A (one-time reads): ~12K tokens
- Phase B (v1 full pipeline): ~18K tokens
- Phase D (v2-vN delta, each): ~7K tokens
- Total for N=3: ~12K + 18K + 14K = ~44K tokens
- Total for N=5: ~12K + 18K + 28K = ~58K tokens

---

## Example Usage

```
/givore-renueva-batch Mesita auxiliar de madera con aranazos, Russafa. Screen: /path/screen.mp4. 4 variantes.
```

Minimal:
```
/givore-renueva-batch mesita madera 3
```

---

**START NOW**:
1. Collect inputs (Phase A.1)
2. Create project structure (Phase A.2)
3. Read ALL reference files once (Phase A.3)
4. Plan variant matrix (Phase A.5)
5. Begin v1 full pipeline (Phase B)

$ARGUMENTS
