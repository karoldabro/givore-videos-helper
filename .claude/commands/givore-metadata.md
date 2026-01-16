# Givore Metadata Generator

Generate multi-platform titles, descriptions, hashtags, and captions for Givore social media videos.

## Instructions

You are a metadata generator for Givore social media videos. Generate optimized content for 5 platforms in the correct order: Facebook → Instagram → LinkedIn → TikTok → YouTube.

**CRITICAL**: Before generating ANY metadata, you MUST read:
- `CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md` for platform rules, tone guidelines, and output format

## Input

The user will provide a video script (the speech/transcription from the video).

If `$ARGUMENTS` is empty, ask the user to paste the script.

## Output Files

Generate TWO separate files:

### FILE 1: Descriptions
Save to: `metadata/[date]_[topic-slug]-descriptions.txt`

Contains all platform metadata in this order:
1. **FACEBOOK** - Community tone, 5 hashtags
2. **INSTAGRAM** - Aesthetic tone, @givore.app, 7-10 hashtags
3. **LINKEDIN** - Professional tone, 5 hashtags
4. **TIKTOK** - Casual tone, emoji, 5 hashtags
5. **YOUTUBE SHORTS** - SEO title, #Shorts, 5-7 hashtags

### FILE 2: Captions
Save to: `metadata/[date]_[topic-slug]-captions.txt`

Formatted captions following these STRICT rules:
- **2-3 words per line MAXIMUM** (break sentences aggressively)
- Blank line between each caption
- DO NOT change the script text - only format it
- Single word lines are acceptable for emphasis
- Split at commas, periods, "Y", "Pero", "Porque", "Es que"

## After File Generation

After saving both files, run the subtitle generation command:

```bash
subs [audio-file.mp3] metadata/[date]_[topic-slug]-captions.txt
```

Ask the user for the audio file path if not provided.

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

1. Parse script from `$ARGUMENTS` or ask for it
2. Read CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md
3. Generate descriptions for all 5 platforms
4. Format captions (2-3 words per line)
5. Save FILE 1: descriptions
6. Save FILE 2: captions
7. Ask for audio file path
8. Run: `subs [audio.mp3] [captions.txt]`
9. Confirm SRT file generated

---

**START NOW**: If $ARGUMENTS contains script text, proceed with generation. Otherwise, ask for the script.

$ARGUMENTS
