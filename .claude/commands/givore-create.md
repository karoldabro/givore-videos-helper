# Givore Unified Content Pipeline

Complete content creation workflow: Script → Approval → Audio → Captions → SRT → Metadata

## Overview

This command orchestrates the full Givore content creation process by calling existing commands and adding ElevenLabs audio generation. All sophisticated logic from `/givore-script` and `/givore-metadata` is preserved.

---

## PHASE 1: SCRIPT GENERATION

**Execute the complete `/givore-script` workflow:**

1. Read `.claude/commands/givore-script.md` to get all instructions
2. Follow ALL steps from that command exactly:
   - STEP 0: Load SCRIPT_HISTORY.md for rotation
   - STEP 0.5: Validate & correct locations (Valenciano → Castellano)
   - STEP 1: Read all 8 reference files
   - Input collection (if $ARGUMENTS is incomplete)
   - Script generation with quality checks
   - Save to: `projects/[date]_[topic-slug]/[topic-slug].txt`
   - Update SCRIPT_HISTORY.md

**Store the project folder path** - you'll need it for subsequent phases.

---

## PHASE 2: APPROVAL GATE

After generating and saving the script, **STOP and ask the user**:

```
📝 Script generado y guardado en: projects/[folder]/[file].txt

[Display the complete script]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿Aprobar script para generar audio?

- Sí → Continuar con generación de audio
- No → Script guardado, puedes editarlo manualmente
- Editar → Haz cambios y vuelve a preguntar
```

**CRITICAL**: Do NOT proceed to audio generation without explicit user approval.

If user says "No":
- Inform them the script is saved
- Tell them to run `/givore-metadata` after manual edits
- **STOP HERE**

If user says "Editar":
- Let them provide changes
- Regenerate/edit the script
- Ask for approval again

If user says "Sí":
- Continue to Phase 3

---

## PHASE 3: AUDIO GENERATION (ElevenLabs MCP)

Generate audio from the script using ElevenLabs text_to_speech MCP tool.

### Voice Configuration (from elevenlabs-config.md)

```yaml
voice_id: "HIYif4jehvc9P9A8DYbX"  # Pablo - Deep, Confident and Clear
model_id: "eleven_multilingual_v2"
language: "es"
stability: 0.35
similarity_boost: 0.4
style: 0.3
use_speaker_boost: true
speed: 1.06
output_format: "mp3_44100_128"
```

### Steps

1. **Read the script** from `projects/[folder]/[topic-slug].txt`
2. **Call ElevenLabs MCP** `text_to_speech` tool:
   ```
   text_to_speech(
     text=[script content],
     voice_id="HIYif4jehvc9P9A8DYbX",
     model_id="eleven_multilingual_v2",
     language="es",
     stability=0.35,
     similarity_boost=0.4,
     style=0.3,
     use_speaker_boost=true,
     speed=1.06,
     output_directory="projects/[folder]/",
     output_format="mp3_44100_128"
   )
   ```
3. **Note the audio file path** returned by the tool
4. If audio generation fails:
   - Show error to user
   - Provide fallback: "Puedes generar el audio manualmente en elevenlabs.io"
   - Continue to Phase 4 anyway (metadata can still be generated)

---

## PHASE 4: METADATA & CAPTIONS

**Execute the complete `/givore-metadata` workflow:**

1. Read `.claude/commands/givore-metadata.md` to get all instructions
2. Follow ALL steps from that command:
   - Skip auto-detection (we already know the project folder)
   - Read the script
   - Read CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md
   - Generate 5-platform metadata → `descriptions.txt`
   - Generate captions (2-3 words/line) → `captions.txt`
   - Save both files to the project folder

---

## PHASE 5: SUBTITLE GENERATION

Generate SRT subtitles using the `subs` bash alias.

1. **Get file paths**:
   - Audio: `projects/[folder]/[topic-slug].mp3` (or the path from Phase 3)
   - Captions: `projects/[folder]/captions.txt`

2. **Run the subs command**:
   ```bash
   subs projects/[folder]/[topic-slug].mp3 projects/[folder]/captions.txt
   ```

3. **Output**: `[topic-slug].srt` (or similar, in the same folder)

4. If subs fails:
   - Show the manual command to user
   - Continue to final summary

---

## PHASE 6: FINAL SUMMARY

Display all generated files:

```
✅ CONTENIDO GIVORE GENERADO

📁 Carpeta: projects/[date]_[topic-slug]/

Archivos generados:
├── 📝 Script: [topic-slug].txt
├── 🎙️ Audio: [topic-slug].mp3
├── 📋 Metadatos: descriptions.txt
├── 💬 Captions: captions.txt
└── 🎬 Subtítulos: [topic-slug].srt

Próximo paso: Abrir template.kdenlive y editar el video

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Input Collection

Same as `/givore-script`. If `$ARGUMENTS` is empty or incomplete, collect:

### Mandatory Inputs
1. **Topic/Theme**: What happened, what was found
2. **Specific Items**: Exact items + condition
3. **Video Structure**: When items appear, timestamps
4. **Location**: Neighborhood (auto-corrected to Castellano)

### Style Inputs
5. **Hook Style**: mystery | proof-first | question | bold | numeric | journey | emotional
6. **Tone**: educational | exciting | community | emotional
7. **CTA Goal**: download | comment | share | follow | community | awareness
8. **Reveal Timing**: early (0-10s) | middle (10-30s) | late (30s+)

---

## Error Handling

| Phase | If Error | Action |
|-------|----------|--------|
| Script Generation | Fails | Stop, show error |
| User Approval | Says "No" | Stop, script saved |
| Audio Generation | Fails | Continue, show fallback |
| Metadata Generation | Fails | Continue, show error |
| Subtitle Generation | Fails | Show manual command |

---

## Example Usage

Full pipeline:
```
/givore-create Found 2 vintage chairs in Benimaclet, excellent condition, video shows cycling then reveal at 15s, mystery hook, exciting tone, download CTA
```

Minimal (will prompt for details):
```
/givore-create sillas vintage en Benimaclet
```

---

## Workflow Summary

```
/givore-create [inputs]
│
├─ PHASE 1: Execute /givore-script logic
│   └─ → projects/[date]_[topic]/[topic].txt
│
├─ PHASE 2: ⏸️ APPROVAL GATE
│   └─ User approves or stops
│
├─ PHASE 3: ElevenLabs audio generation
│   └─ → projects/[date]_[topic]/[topic].mp3
│
├─ PHASE 4: Execute /givore-metadata logic
│   └─ → descriptions.txt + captions.txt
│
├─ PHASE 5: Run subs command
│   └─ → [topic].srt
│
└─ PHASE 6: Final summary
```

---

**START NOW**:
1. Read /givore-script command and execute Phase 1
2. After script is saved, execute Phase 2 (approval)
3. Only proceed to Phase 3+ after approval

$ARGUMENTS
