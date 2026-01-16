# Metadata Generation System

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/givore-metadata` | Metadata + captions only (standalone) |
| `/givore-create` | Unified pipeline: Script → Audio → Captions → Metadata |

**Files**:
- `.claude/commands/givore-metadata.md`
- `.claude/commands/givore-create.md` (orchestrator)

**Note**: `/givore-create` calls `/givore-metadata` logic internally, preserving all features.

## Input
- Auto-detects most recent project folder in `projects/`
- Reads script from: `projects/[folder]/[topic-slug].txt`
- User confirms or specifies different project

## Output Files

Both files saved in the **same project folder** as the script:

### FILE 1: Descriptions
**Path**: `projects/[folder]/descriptions.txt`

Platform order: **Facebook → Instagram → LinkedIn → TikTok → YouTube**

### FILE 2: Captions
**Path**: `projects/[folder]/captions.txt`

Caption rules:
- **2-3 words per line MAXIMUM**
- Break sentences aggressively
- Blank line between each caption
- DO NOT change script text - only format

## Platform-Specific Rules

### FACEBOOK
- **Tone**: Community-focused, local, conversational
- **Title**: `[Community hook] + [Location]`
- **Description**: Longer (Facebook users read more), ask for stories
- **Hashtags**: 5

### INSTAGRAM
- **Tone**: Aesthetic, lifestyle, inspirational
- **Title**: `[Aesthetic statement] + [Emoji]`
- **Description**: Include "Guarda este post", tag @givore.app
- **Hashtags**: 7-10

### LINKEDIN
- **Tone**: Professional, business value, data-driven
- **Title**: `[Statistic or insight] + [Professional angle]`
- **Description**: Frame as innovation/sustainability story
- **Hashtags**: 5 (professional)

### TIKTOK
- **Tone**: Casual, fun, emoji-heavy, direct
- **Title**: `[Emoji] + [Curiosity hook]` (max 100 chars)
- **Description**: End with question for comments
- **Hashtags**: 5

### YOUTUBE SHORTS
- **Tone**: Searchable, educational, clear
- **Title**: `[SEO keyword phrase] + [Emoji] + #Shorts`
- **Description**: Explain Givore (YouTube audience may not know)
- **Hashtags**: 5-7 (SEO focused, lowercase)

## SRT Generation

After saving both files, run:
```bash
subs [audio-file.mp3] projects/[folder]/captions.txt
```

Generates: `[audio-file].srt`

## Caption Formatting Example

**Input**: "¿Sabéis qué? Valencia está llena de tesoros y la gente pasa de largo."

**Output**:
```
¿Sabéis qué?

Valencia está llena

de tesoros...

y la gente

pasa de largo.
```
