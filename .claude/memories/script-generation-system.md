# Script Generation System

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/givore-script` | Script generation only (standalone) |
| `/givore-create` | Unified pipeline: Script → Audio → Captions → Metadata |

**Files**:
- `.claude/commands/givore-script.md`
- `.claude/commands/givore-create.md` (orchestrator)

**Note**: `/givore-create` calls `/givore-script` logic internally, preserving all features.

## Required Inputs (10-field template)

### Mandatory (Must have before generating)
1. **Topic/Theme**: What happened, what was found
2. **Specific Items**: Exact items + condition (NEVER "didn't find anything")
3. **Video Structure**: When items appear, key timestamps
4. **Location**: Neighborhood found, ending spot if different

### Style Inputs
5. **Hook Style**: mystery | proof-first | question | bold | numeric | journey | emotional | relevance-3part | day-x
6. **Tone**: educational | exciting | community | emotional
7. **CTA Goal**: download | comment | share | follow | community | awareness
8. **Reveal Timing**: early (0-10s) | middle (10-30s) | late (30s+)

### Rotation Inputs
9. **Recent Hooks Used**: Last 2-3 hooks to avoid
10. **Recent CTAs Used**: Last 2-3 CTAs to avoid

## Script Structure (MANDATORY SEQUENCE)

```
[HOOK: 0-3 seconds]
- Max 15 words, start immediately (no "Hola")
- See HOOKS_LIBRARY.md decision tree

[PROOF TEASE: 3-8 seconds]
- Anticipation WITHOUT full reveal
- "Quedaos hasta el final" / "Al final vais a flipar"

[PROBLEM: 8-20 seconds]
- Focus on SITUATION, not PEOPLE blame
- Use empathy ("Te da pena") not judgment ("Es absurdo")

[IMPORTANCE: 20-25 seconds]
- Show OPPORTUNITY, not GUILT
- "Alguien lo aprovecharía" NOT "familias que necesitan"

[RE-HOOK: 25-28 seconds]
- Recapture with EMPOWERMENT
- "Pero eso se puede cambiar" / "Y os voy a enseñar cómo"

[SOLUTION: 28-45 seconds]
- Introduce Givore naturally
- Vary app demo phrasing (see PHRASE_VARIATIONS.md)

[PAYOFF: 45-60 seconds]
- Deliver on hook promise
- Reveal items if using mystery hook

[CLOSING + CTA: Last 5-10 seconds]
- Match to specified CTA Goal
- Max 2 sentences
```

## Word Count Guidelines (200 WPM)
| Duration | Words (Spanish) |
|----------|-----------------|
| 30 sec | 90-110 |
| 45 sec | 140-160 |
| 60 sec | 185-210 |
| 90 sec | 280-310 |
| 120 sec | 380-410 |

## Output
- Text optimized for ElevenLabs text-to-speech
- Creates project folder: `projects/[date]_[topic-slug]/`
- Saves script to: `projects/[date]_[topic-slug]/[topic-slug].txt`
- Updates `scripts/SCRIPT_HISTORY.md` with rotation data
- Use ellipsis for pauses, numbers as words
