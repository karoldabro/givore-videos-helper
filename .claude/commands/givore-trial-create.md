# Givore Trial Content Pipeline

Complete trial content creation workflow: Script → Approval → Audio → Captions → SRT → Metadata

## Project Root

**All file paths in this command are relative to the project root: `/media/kdabrow/Programy/givore/`**

When using the Read tool or any file operation, always prepend this path. For example:
- `scripts/TRIAL_HISTORY.md` → `/media/kdabrow/Programy/givore/scripts/TRIAL_HISTORY.md`
- `trial/TRIAL_AUDIENCES.md` → `/media/kdabrow/Programy/givore/trial/TRIAL_AUDIENCES.md`
- `projects/trial-[folder]/` → `/media/kdabrow/Programy/givore/projects/trial-[folder]/`

## Overview

This command orchestrates the full trial content creation process by calling trial script logic and adding ElevenLabs audio generation with tone-specific voice settings. All sophisticated logic from `/givore-trial` is preserved.

---

## PHASE 1: TRIAL SCRIPT GENERATION

**Execute the complete `/givore-trial` workflow:**

1. Read `.claude/commands/givore-trial.md` to get all instructions
2. Follow ALL steps from that command exactly:
   - STEP 0: Load TRIAL_HISTORY.md for rotation
   - STEP 0.5: Read and analyze last 2 trial script texts
   - STEP 1: Read all 7 trial reference files
   - Input collection (if $ARGUMENTS is incomplete)
   - Compatibility check (tone + format + marketing)
   - Script generation with quality checks
   - Save to: `projects/trial-[date]_[topic-slug]/[topic-slug].txt`
   - Update TRIAL_HISTORY.md

**Store the project folder path and the chosen TONE** - you'll need both for subsequent phases.

---

## PHASE 2: APPROVAL GATE

After generating and saving the script, **STOP and ask the user**:

```
📝 Trial script generado y guardado en: projects/trial-[folder]/[file].txt

[Display the complete script]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configuración:
- Audiencia: [AUDIENCE]
- Tono: [TONE]
- Formato: [FORMAT]
- Marketing: [MARKETING]
- Duración: [DURATION]s

¿Aprobar script para generar audio?

- Sí → Continuar con generación de audio
- No → Script guardado, puedes editarlo manualmente
- Editar → Haz cambios y vuelve a preguntar
```

**CRITICAL**: Do NOT proceed to audio generation without explicit user approval.

If user says "No":
- Inform them the script is saved
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

### Tone-Specific Voice Configuration

Base voice: Pablo (HIYif4jehvc9P9A8DYbX) with eleven_multilingual_v2 model.

**Select parameters based on the script's TONE:**

| Tone | Speed | Stability | Style |
|------|-------|-----------|-------|
| HUMORISTIC | 1.10 | 0.30 | 0.35 |
| EMPATHETIC | 1.02 | 0.40 | 0.35 |
| PROVOCATIVE | 1.08 | 0.30 | 0.40 |
| DRAMATIC | 0.98 | 0.35 | 0.45 |
| RELATABLE | 1.06 | 0.35 | 0.30 |
| SARCASTIC | 1.08 | 0.25 | 0.35 |

### Steps

1. **Read the script** from `projects/trial-[folder]/[topic-slug].txt`
2. **Determine voice parameters** from the tone table above
3. **Call ElevenLabs MCP** `text_to_speech` tool:
   ```
   text_to_speech(
     text=[script content],
     voice_id="HIYif4jehvc9P9A8DYbX",
     model_id="eleven_multilingual_v2",
     language="es",
     stability=[tone-specific],
     similarity_boost=0.4,
     style=[tone-specific],
     use_speaker_boost=true,
     speed=[tone-specific],
     output_directory="projects/trial-[folder]/",
     output_format="mp3_44100_128"
   )
   ```
4. **Note the audio file path** returned by the tool
5. If audio generation fails:
   - Show error to user
   - Provide fallback: "Puedes generar el audio manualmente en elevenlabs.io"
   - Continue to Phase 4 anyway

---

## PHASE 4: METADATA & CAPTIONS (Trial-Specific)

Generate trial-specific metadata and captions.

### Metadata Generation

Create `descriptions.txt` with 5-platform metadata in this order:

**1. FACEBOOK**
- Community tone
- Reference the pain point/audience, not Givore (for INDIRECT) or briefly mention Givore (for SOFT/DIRECT)
- 5 audience-relevant hashtags

**2. INSTAGRAM**
- Aesthetic tone, @givore.app mention (only for SOFT/DIRECT)
- For INDIRECT: no brand mention, focus on relatable content
- 7-10 audience-relevant hashtags (see TRIAL_MARKETING_MATRIX.md for hashtag strategy)

**3. LINKEDIN**
- Professional tone about circular economy / sustainability
- 5 hashtags

**4. TIKTOK**
- Casual tone with relevant emoji
- For INDIRECT: hook the audience without mentioning Givore
- 5 audience-relevant hashtags

**5. YOUTUBE SHORTS**
- SEO-friendly title
- #Shorts
- 5-7 hashtags

### Hashtag Strategy by Marketing Approach

**INDIRECT**: Use ONLY audience-relevant hashtags (no #givore):
- RENOVATING: #reforma #reformas #obrasencasa #antesydespues #hogar
- NEW-HOUSE: #casanueva #mudanza #decoracion #hogar #nuevaetapa
- OLD-ITEMS: #declutter #minimalism #orden #organizar #segundamano
- MOVING: #mudanza #mudarme #cambio #nuevaetapa #empaquetar
- CLUTTER: #orden #konmari #minimalistaespañol #limpiar #organizacion
- SEASONAL: #cambiodetemporada #primavera #otoño #armariolimpio #hogar

**SOFT**: Audience-relevant hashtags + #givore (at the end)

**DIRECT**: Audience-relevant hashtags + #givore #reciclaje #reciclajesocial #darencontrar

### Captions Generation

Create `captions.txt` following the same rules as street-finds:
- 2-3 words per line MAXIMUM
- Plain text (no formatting markers like [HOOK], bold, etc.)
- Based on the script content

Save both files to the project folder.

---

## PHASE 5: SUBTITLE GENERATION

Generate SRT subtitles using the `subs` bash alias.

1. **Get file paths**:
   - Audio: `projects/trial-[folder]/[topic-slug].mp3` (or the path from Phase 3)
   - Captions: `projects/trial-[folder]/captions.txt`

2. **Run the subs command**:
   ```bash
   subs projects/trial-[folder]/[topic-slug].mp3 projects/trial-[folder]/captions.txt
   ```

3. **Output**: `[topic-slug].srt` in the same folder

4. If subs fails:
   - Show the manual command to user
   - Continue to final summary

---

## PHASE 6: FINAL SUMMARY

Display all generated files:

```
✅ TRIAL CONTENT GENERADO

📁 Carpeta: projects/trial-[date]_[topic-slug]/

Configuración:
├── Audiencia: [AUDIENCE]
├── Tono: [TONE]
├── Formato: [FORMAT]
├── Marketing: [MARKETING]
└── Duración: [DURATION]s

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

Same as `/givore-trial`. If `$ARGUMENTS` is empty or incomplete, collect:

### Mandatory Inputs
1. **Audience**: RENOVATING | NEW-HOUSE | OLD-ITEMS | MOVING | CLUTTER | SEASONAL
2. **Tone**: HUMORISTIC | EMPATHETIC | PROVOCATIVE | DRAMATIC | RELATABLE | SARCASTIC

### Style Inputs
3. **Format**: QUESTION-BARRAGE | SCENARIO-STORY | PROBLEM-ESCALATION | DIRECT-ADDRESS | HUMOR-SKIT
4. **Marketing Approach**: INDIRECT | SOFT | DIRECT
5. **Duration**: 15 | 30 | 45 | 60

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
/givore-trial-create RENOVATING audience, HUMORISTIC tone, QUESTION-BARRAGE, INDIRECT, 30s
```

Minimal (will prompt for details):
```
/givore-trial-create mudanza empático
```

---

## Workflow Summary

```
/givore-trial-create [inputs]
│
├─ PHASE 1: Execute /givore-trial logic
│   └─ → projects/trial-[date]_[topic]/[topic].txt
│
├─ PHASE 2: ⏸️ APPROVAL GATE
│   └─ User approves or stops
│
├─ PHASE 3: ElevenLabs audio (tone-specific settings)
│   └─ → projects/trial-[date]_[topic]/[topic].mp3
│
├─ PHASE 4: Trial-specific metadata + captions
│   └─ → descriptions.txt + captions.txt
│
├─ PHASE 5: Run subs command
│   └─ → [topic].srt
│
└─ PHASE 6: Final summary
```

---

**START NOW**:
1. Read /givore-trial command and execute Phase 1
2. After script is saved, execute Phase 2 (approval)
3. Only proceed to Phase 3+ after approval

$ARGUMENTS
