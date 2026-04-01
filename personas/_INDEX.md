# Script Personas — Voice Variety System

5 distinct writer personas that control vocabulary, sentence patterns, emotional palette, and audio delivery. Each script MUST use a persona different from the last 2. Track via `script-add --persona`.

**Core rule:** The persona defines HOW you speak. Content rules (tone guardrails, giveaway-first framing, no trash encouragement) apply to ALL personas equally. A persona never overrides safety rules.

**Individual persona files:** `OBSERVADOR.md`, `ENERGETICO.md`, `VECINA.md`, `REPORTERO.md`, `POETA.md`

---

## Persona Selection

```
Check last 2 personas used (via script-rotation):
+-- Avoid both of them
+-- Select based on content fit or rotate sequentially

Content fit guidance:
+-- Scenic/exploration video    --> OBSERVADOR or POETA
+-- Quick find, punchy content  --> ENERGETICO
+-- Community/sharing focus     --> VECINA
+-- Multi-item, factual report  --> REPORTERO
+-- Emotional single item       --> POETA or OBSERVADOR
+-- App demo emphasis           --> ENERGETICO or VECINA
```

---

## ElevenLabs Voice Settings Per Persona

Same voice (Pablo, HIYif4jehvc9P9A8DYbX) with different delivery parameters:

| Persona | Speed | Stability | Similarity | Style | Effect |
|---------|-------|-----------|------------|-------|--------|
| OBSERVADOR | 0.98 | 0.40 | 0.45 | 0.35 | Slower, calm, reflective pauses |
| ENERGETICO | 1.12 | 0.25 | 0.35 | 0.40 | Fast, punchy, expressive variation |
| VECINA | 1.04 | 0.35 | 0.40 | 0.35 | Natural conversational rhythm |
| REPORTERO | 1.08 | 0.45 | 0.40 | 0.20 | Measured, factual, controlled |
| POETA | 0.95 | 0.30 | 0.40 | 0.45 | Slow, dramatic, highly expressive |

All use: `model_id: eleven_multilingual_v2`, `language: es`, `use_speaker_boost: true`, `output_format: mp3_44100_128`

---

## Rotation Rules

1. **NEVER** use the same persona in 2 consecutive scripts
2. **Verify** via `givore-tools.sh script-rotation` before selecting (check `persona` field)
3. **Suggested rotation**: OBSERVADOR --> ENERGETICO --> VECINA --> REPORTERO --> POETA --> (repeat)
4. **Within a 7-variant batch**: ALL 7 variants MUST use different personas (5 personas + 2 repeats allowed with different structures)
5. **Persona + Structure pairing**: No restrictions, but some natural fits exist (see compatibility table)

---

## Persona + Structure Compatibility

| Persona | Best Structures | Avoid Combining With |
|---------|----------------|---------------------|
| OBSERVADOR | COLD OPEN, LOOP, CLASSIC | COUNTDOWN (too fast-paced) |
| ENERGETICO | MICRO, COUNTDOWN, PSP | LOOP (needs patience) |
| VECINA | CLASSIC, PSP, COLD OPEN | MICRO (needs conversation space) |
| REPORTERO | PSP, COUNTDOWN, COLD OPEN | LOOP (too lyrical), POETA's territory |
| POETA | LOOP, COLD OPEN, MICRO | COUNTDOWN (too listy), REPORTERO's territory |

---

## Quality Markers Per Persona

When reviewing a generated script, check these persona-specific markers:

| Persona | Must Have (2+) | Must NOT Have |
|---------|---------------|---------------|
| OBSERVADOR | Sensory description, reflective question, ellipsis pause | Exclamation marks, "brutal", "flipante" |
| ENERGETICO | 3+ fragments under 5 words, action verbs, periods-as-rhythm | Long descriptions, "me pregunto", atmospheric words |
| VECINA | Tag question, direct address ("oye"), self-interruption | Formal language, data/numbers, metaphors |
| REPORTERO | Data point or measurement, understated humor, declarative statements | Emotional exclamations, poetic language, "que pasada" |
| POETA | Metaphor, repeated phrase, philosophical question | Staccato fragments, data, efficiency words |
