# Givore Script Agent Improvements (January 2026)

## Summary
Implemented automatic rotation tracking and reduced repetitive content in script generation.

## Changes Made

### New Files Created
1. **scripts/SCRIPT_HISTORY.md** - Tracks last 10 scripts with metadata:
   - Hook Type, CTA Type, Proof Tease decision
   - Problem Angle, Rehook Style
   - Auto-updated after each script generation

2. **PROBLEM_VARIATIONS.md** - 5 problem angle categories:
   - SYSTEM-WASTE (default)
   - MISSED-CONNECTION
   - URBAN-TREASURE
   - TIME-SENSITIVE
   - NEIGHBOR-UNKNOWN

3. **IMPORTANCE_VARIATIONS.md** - 5 importance angle categories:
   - PROXIMITY-OPPORTUNITY (default)
   - WASTE-PREVENTION
   - COMMUNITY-MAGIC
   - PERSONAL-WIN
   - CIRCULAR-LIFE

4. **REHOOK_VARIATIONS.md** - 5 re-hook style categories:
   - SOLUTION-TEASE (default)
   - CURIOSITY-BUILD
   - ACTION-PIVOT
   - COMMUNITY-BRIDGE
   - DIRECT-REVEAL

### Updated Files
- **.claude/commands/givore-script.md** - Major updates:
  - STEP 0: Auto-read SCRIPT_HISTORY.md before generation
  - Proof tease now OPTIONAL with decision tree
  - References to new variation files
  - Mandatory history update after saving script
  - Removed manual "recent hooks/CTAs" input requirement

## Key Improvements
1. **Automatic tracking** - No manual input needed for rotation avoidance
2. **Optional proof tease** - "Quedaos hasta el final" no longer mandatory
3. **Varied sections** - Problem, Importance, Rehook now have 5 categories each
4. **Decision trees** - Clear logic for when to use/skip elements

### Location Validation (2026-01-16)
- **STEP 0.5: Validate & Correct Location** added to givore-script.md
- Auto-corrects misspellings (e.g., "Ruzaffa" → "Ruzafa")
- Converts Valenciano to Castellano (e.g., "Russafa" → "Ruzafa", "El Carme" → "El Carmen")
- Uses web search to validate locations exist in Valencia
- Shows corrections to user: "📍 Ubicación corregida: [original] → [corrected]"
- Asks for clarification only if location cannot be identified
- Quality check added: "Location name(s) verified and corrected to Castellano"

**Valenciano → Castellano conversions table included:**
| Valenciano | Castellano |
|------------|------------|
| Russafa | Ruzafa |
| El Carme | El Carmen |
| El Cabanyal | El Cabañal |
| La Saïdia | La Zaidía |
| Poblats Marítims | Poblados Marítimos |

## Usage
The command now works fully automatically:
1. Run `/givore-script` with topic details
2. Command validates and auto-corrects location names to Castellano
3. Command reads history, avoids last 3 of each element
4. Generates varied script
5. Saves script + updates history
