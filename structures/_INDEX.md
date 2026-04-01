# Script Structures — Rotatable Narrative Formats

6 alternative script structures to prevent cross-session monotony. Each video MUST use a structure different from the last 2 scripts. Track via `script-add --structure-type`.

**Core rule:** The structure defines SECTION ORDER and PACING. Content rules (tone guardrails, giveaway-first framing, no trash encouragement) apply to ALL structures equally.

---

## Structure Selection Decision Tree

```
What type of content is this?
|
+-- Multiple items found          --> COUNTDOWN or CLASSIC
+-- Single impressive item        --> COLD OPEN or MICRO-NARRATIVE
+-- Community/sharing focus       --> LOOP or PSP
+-- Quick find, simple story      --> MICRO-NARRATIVE
+-- App demo is important         --> CLASSIC or PSP
+-- Exploration/journey video     --> CLASSIC or COLD OPEN
|
Check last 2 structures used:
+-- Same as either? --> Pick a different one
+-- All different?  --> Free choice based on content fit
```

---

## Rotation Rules

1. **NEVER** use the same structure in 2 consecutive scripts
2. **Verify** via `givore-tools.sh script-rotation` before selecting
3. **Suggested rotation**: CLASSIC --> COLD OPEN --> LOOP --> MICRO --> PSP --> COUNTDOWN --> (repeat)
4. **Within a 7-variant batch**: v1 sets the structure. v2-v7 CAN use the same structure (they differentiate via other matrix dimensions). But if the batch includes MICRO variants, use at most 2 MICROs.

---

## Timing Guidelines (NOT Rules)

Each structure has suggested timing. Adapt to your content:

- If the item is visually stunning --> Front-load the reveal (COLD OPEN timing)
- If the story has a twist --> Save it (LOOP timing)
- If the find is simple --> Keep it short (MICRO timing)
- If you have proof/results --> Allocate time for evidence (PSP timing)

**NEVER force content to fit timing.** Let the story decide.

---

## Emotional Arc Variety

| Structure | Primary Emotions | Secondary |
|-----------|-----------------|-----------|
| CLASSIC | Curiosity, empathy, hope | Community pride |
| COLD OPEN | Surprise, understanding | Connection |
| LOOP | Confusion, discovery, "aha!" | Satisfaction |
| MICRO | One dominant emotion (varies) | None — keep pure |
| PSP | Concern, hope, conviction | Evidence-based trust |
| COUNTDOWN | Anticipation, surprise x3 | Cumulative impact |

**Rule:** If your last 3 scripts all used empathy+hope, pick a structure with a DIFFERENT emotional arc.

---

## Structure Compatibility with Content Pillars

| Content Pillar | Best Structures |
|---------------|----------------|
| Cycling POV / exploration | CLASSIC, COLD OPEN, COUNTDOWN |
| Single item find | COLD OPEN, MICRO, PSP |
| Multiple items | COUNTDOWN, CLASSIC |
| Community/sharing message | LOOP, PSP |
| Quick daily find | MICRO, COLD OPEN |
| App demo/tutorial | CLASSIC, PSP |
| Minimalism/decluttering | LOOP, PSP |
| Neighborhood guide | COUNTDOWN, CLASSIC |

---

## Quick Reference

| Structure | Sections | Duration | App mention | Best for |
|-----------|----------|----------|-------------|----------|
| CLASSIC | 8 | 45-60s | Dedicated section | Full narrative |
| COLD OPEN | 6 | 40-55s | Woven in | Single impressive find |
| LOOP | 6 | 45-60s | Mid-story | Story with twist |
| MICRO | 4 | 20-35s | Minimal (1 sentence) | Quick punchy content |
| PSP | 5 | 45-60s | In Solution beat | Persuasion + proof |
| COUNTDOWN | 7 | 50-60s | Compressed mini-version | Multi-item finds |
