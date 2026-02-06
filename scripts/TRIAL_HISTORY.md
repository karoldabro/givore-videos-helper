# Trial Script History (Auto-Updated)

This file is automatically read by the givore-trial command to track experiments and avoid repetition.
After each trial script generation, update this file with the new script metadata.

## Last 10 Trial Scripts (newest first)

| # | Date | File | Audience | Format | Tone | Marketing | Duration | Item Focus | Pain Point |
|---|------|------|----------|--------|------|-----------|----------|------------|------------|
| 1 | 2026-02-05 | trial-2026-02-05_casa-llena/casa-llena.txt | CLUTTER | QUESTION-BARRAGE | HUMORISTIC | SOFT | 30 | GENERAL | SPACE |

---

## Column Definitions

| Column | Values | Description |
|--------|--------|-------------|
| **Audience** | RENOVATING, NEW-HOUSE, OLD-ITEMS, MOVING, CLUTTER, SEASONAL | Target audience segment (from TRIAL_AUDIENCES.md) |
| **Format** | QUESTION-BARRAGE, SCENARIO-STORY, PROBLEM-ESCALATION, DIRECT-ADDRESS, HUMOR-SKIT | Script structure template (from TRIAL_FORMATS.md) |
| **Tone** | HUMORISTIC, EMPATHETIC, PROVOCATIVE, DRAMATIC, RELATABLE, SARCASTIC | Emotional register (from TRIAL_TONES.md) |
| **Marketing** | INDIRECT, SOFT, DIRECT | How/if Givore is mentioned (from TRIAL_MARKETING_MATRIX.md) |
| **Duration** | 15, 30, 45, 60 | Target duration in seconds |
| **Item Focus** | FURNITURE, ART, APPLIANCES, CLOTHING, GENERAL, NONE | Specific item category if applicable |
| **Pain Point** | SPACE, GUILT, LAZINESS, COST, ATTACHMENT, GENERAL | Primary emotional driver |

---

## Rotation Rules

When generating a new trial script, the command MUST:

1. **Read this file first** to get recent trial metadata
2. **Don't repeat** the same Audience + Format + Tone combination as any of the last 3 scripts
3. **Vary Marketing approach**: if last 2 were the same approach, switch
4. **Vary Duration**: don't produce 3 scripts of the same length in a row
5. **Vary questions**: read last 2 script texts and avoid reusing the same questions
6. **After generation**: shift all rows down and add new script at row 1
7. **Delete row 11** if it exists (keep only 10)

---

## Update Instructions

After generating a trial script, update this file:

```
1. Move row 1 → row 2
2. Move row 2 → row 3
3. ... (shift all down)
4. Delete row 11 if exists
5. Add new script data to row 1 (include all columns)
```

Example:
```markdown
| 1 | 2026-02-06 | trial-2026-02-06_reforma-cocina/reforma-cocina.txt | RENOVATING | QUESTION-BARRAGE | HUMORISTIC | INDIRECT | 30 | FURNITURE | SPACE |
```
