# Givore Metadata Generator

Generate multi-platform titles, descriptions, hashtags, and captions for Givore social media videos.

## Project Root

**All file paths in this command are relative to the project root: `/media/kdabrow/Programy/givore/`**

When using the Read tool or any file operation, always prepend this path. For example:
- `projects/[folder]/` → `/media/kdabrow/Programy/givore/projects/[folder]/`
- `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md` → `/media/kdabrow/Programy/givore/CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md`

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

Contains thumbnail title + all platform metadata in this order:
0. **THUMBNAIL** - Short hook title for thumbnail overlay (5-7 words, ALL UPPERCASE)
1. **FACEBOOK** - Community tone, 3-5 hashtags
2. **INSTAGRAM** - Caption-first (125 char keyword hook), @givore.app, 3-5 hashtags
3. **LINKEDIN** - Personal narrative, NO external links, 3 hashtags max
4. **TIKTOK** - Casual tone, emoji, no commercial terms ("gratis"), 3-5 hashtags
5. **YOUTUBE SHORTS** - Search-intent title (NO #Shorts in title, NO "GRATIS"), 3-5 hashtags

**THUMBNAIL title rules**:
- Max 5-7 words, ALL UPPERCASE
- Remove emojis, hashtags, platform-specific text
- Keep core curiosity/hook element from the script
- Use power words: GRATIS, TIRADO, MIRA ESTO, INCREIBLE, EN LA CALLE, TESORO
- Must be readable at small mobile thumbnail size (shorter = better)

**THUMBNAIL section format** (placed FIRST in descriptions.txt):
```
═══════════════════════════════════════════════════════════
                    THUMBNAIL
═══════════════════════════════════════════════════════════

MUEBLES GRATIS EN VALENCIA

```

### FILE 2: Captions
Save to: `projects/[folder]/captions.txt`

Formatted captions following these STRICT rules:
- **2-3 words per line MAXIMUM** (break sentences aggressively)
- Blank line between each caption
- DO NOT change the script text - only format it
- Single word lines are acceptable for emphasis
- Split at commas, periods, "Y", "Pero", "Porque", "Es que"
- Do NOT add any formatting markers (no asterisks, no bold, no special characters)
- Captions must be plain text only - the subs tool needs clean text for SRT generation

## After File Generation

After saving both files, run the subtitle generation command:

```bash
/media/kdabrow/Programy/givore/scripts/givore-tools.sh subs [audio-file.mp3] projects/[folder]/captions.txt
```

Ask the user for the audio file path if not provided. The audio file is typically saved in the same project folder.

This will generate: `[audio-file].srt`

## STEP: Keyword Verification (Before Generating)

After reading the script, before generating metadata:
1. Identify which Unified Keywords (from CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md) fit naturally
2. Ensure at least 1 Tier 1 keyword per platform in the first sentence
3. Select target city for hyperlocal hashtags (from video content, or rotate)
4. Verify NO "gratis" appears in any output

## Quality Checks

Before outputting, verify:
- [ ] THUMBNAIL section is FIRST in descriptions.txt with 5-7 word uppercase title
- [ ] Platform order is correct (Facebook → Instagram → LinkedIn → TikTok → YouTube)
- [ ] Each platform has unique title matching its tone
- [ ] Hashtag counts: FB 3-5, IG 3-5, LinkedIn 3, TikTok 3-5, YouTube 3-5
- [ ] Each platform has at least 1 Tier 1 keyword in first sentence
- [ ] No "gratis" in any platform output
- [ ] No zero-volume hashtags (#ReciclajeSocial, #StreetFinds, #TreasureHunting, #EcoFriendly)
- [ ] At least 1 hyperlocal city hashtag per platform
- [ ] Instagram: first 125 chars are keyword-rich hook, ends with DM-shareable statement
- [ ] LinkedIn: NO external links, personal narrative tone, 3 hashtags max
- [ ] YouTube: NO #Shorts in title, NO "GRATIS"
- [ ] Titles are nationally framed (not Valencia-locked) unless video shows specific city
- [ ] Captions are 2-3 words per line (MANDATORY)
- [ ] Captions are plain text (no asterisks or formatting markers)
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
10. Run: `/media/kdabrow/Programy/givore/scripts/givore-tools.sh subs [audio.mp3] projects/[folder]/captions.txt`
11. Confirm SRT file generated

---

**START NOW**:
1. List project folders and suggest the most recent one
2. If $ARGUMENTS specifies a folder, use that instead
3. Read the script from the project folder and proceed with generation

$ARGUMENTS
