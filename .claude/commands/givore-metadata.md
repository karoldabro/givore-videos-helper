# Givore Metadata Generator

Generate multi-platform titles, descriptions, hashtags, and captions for Givore social media videos.

## Instructions

You are a metadata generator for Givore social media videos. Generate optimized content for 5 platforms in the correct order: Facebook → Instagram → LinkedIn → TikTok → YouTube.

**CRITICAL**: Before generating ANY metadata, you MUST read:
- `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md` for platform rules, tone guidelines, and output format

## STEP 0: Detect Project Folder (AUTOMATIC)

Before asking for input, detect the most recent project folder:

1. **List project folders**: Scan `projects/` directory
2. **Filter**: Skip `template.kdenlive` and non-directory files
3. **Sort**: By modification time (newest first)
4. **Suggest**: Show the most recent project folder to the user

```
📁 Proyecto detectado: projects/2026-01-16_marmol-silla-russafa/
   Script: marmol-silla-russafa.txt

¿Es este el proyecto correcto? (Y/n o especifica otro)
```

If user confirms, read the script from that folder. If user specifies different folder, use that instead.

## Input

Read the script from the detected project folder: `projects/[folder]/[topic-slug].txt`

If `$ARGUMENTS` specifies a project folder or script, use that instead of auto-detection.

## Output Files

Generate TWO separate files in the **same project folder** as the script:

### FILE 1: Descriptions
Save to: `projects/[folder]/descriptions.txt`

Contains all platform metadata in this order:
1. **FACEBOOK** - Community tone, 5 hashtags
2. **INSTAGRAM** - Aesthetic tone, @givore.app, 7-10 hashtags
3. **LINKEDIN** - Professional tone, 5 hashtags
4. **TIKTOK** - Casual tone, emoji, 5 hashtags
5. **YOUTUBE SHORTS** - SEO title, #Shorts, 5-7 hashtags

### FILE 2: Captions
Save to: `projects/[folder]/captions.txt`

Formatted captions following these STRICT rules:
- **2-3 words per line MAXIMUM** (break sentences aggressively)
- Blank line between each caption
- DO NOT change the script text - only format it
- Single word lines are acceptable for emphasis
- Split at commas, periods, "Y", "Pero", "Porque", "Es que"

## After File Generation

After saving both files, run the subtitle generation command:

```bash
subs [audio-file.mp3] projects/[folder]/captions.txt
```

Ask the user for the audio file path if not provided. The audio file is typically saved in the same project folder.

This will generate: `[audio-file].srt`

## Quality Checks

Before outputting, verify:
- [ ] Platform order is correct (Facebook → Instagram → LinkedIn → TikTok → YouTube)
- [ ] Each platform has unique title matching its tone
- [ ] Hashtag counts are correct per platform
- [ ] Captions are 2-3 words per line (MANDATORY)
- [ ] Two separate files saved
- [ ] Spanish (Spain) language with "vosotros" form
- [ ] Each description mentions Givore naturally

## Example Usage

```
/givore-metadata ¿Sabéis qué? Valencia está llena de tesoros y la mayoría de la gente pasa de largo. Mira, todo esto me lo encontré en la calle...
```

Or without arguments to be prompted:
```
/givore-metadata
```

## Workflow

1. **Detect project folder**: List `projects/` folders, suggest most recent
2. **Confirm with user**: Ask if detected folder is correct
3. **Read script**: From `projects/[folder]/[topic-slug].txt`
4. Read CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md
5. Generate descriptions for all 5 platforms
6. Format captions (2-3 words per line)
7. Save FILE 1: `projects/[folder]/descriptions.txt`
8. Save FILE 2: `projects/[folder]/captions.txt`
9. Ask for audio file path (likely in same project folder)
10. Run: `subs [audio.mp3] projects/[folder]/captions.txt`
11. Confirm SRT file generated

---

**START NOW**:
1. List project folders and suggest the most recent one
2. If $ARGUMENTS specifies a folder, use that instead
3. Read the script from the project folder and proceed with generation

$ARGUMENTS
