# Givore Viral Script Generator - Project Overview

## Purpose
Marketing content generation system for **Givore** - a social recycling (upcycling) app in Valencia, Spain where users share street finds, give away items, and search for used things.

## Core Message
"No es comprar ni vender. Es dar y encontrar." (It's not buying or selling. It's giving and finding.)

## Content Type
- TikTok/social media short videos (21-120 seconds)
- Indirect marketing through engaging, authentic content
- Language: Spanish (Spain) - peninsular expressions, "vosotros" form

## Project Structure

```
givore/
├── CLAUDE_PROJECT_INSTRUCTIONS.md    # Main script generation instructions
├── CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md  # Multi-platform metadata
├── HOOKS_LIBRARY.md                  # 8 hook categories with decision tree
├── TONE_GUARDRAILS.md                # Positive framing, avoid accusations
├── CTA_VARIATIONS.md                 # 6 CTA goal types
├── PHRASE_VARIATIONS.md              # Avoid repetitive language
├── .claude/
│   ├── commands/
│   │   ├── givore-create.md          # /givore-create - Unified pipeline
│   │   ├── givore-script.md          # /givore-script command
│   │   └── givore-metadata.md        # /givore-metadata command
│   └── memories/                     # Project knowledge base
│       └── elevenlabs-config.md      # ElevenLabs voice settings
├── scripts/
│   └── SCRIPT_HISTORY.md             # Rotation tracking (hook types, CTAs)
├── projects/                         # Self-contained project folders
│   ├── .gitignore                    # Ignores *.mp3 files
│   ├── template.kdenlive             # KDEnlive template
│   └── [date]_[topic-slug]/          # Per-video project folder
│       ├── [topic-slug].txt          # Script
│       ├── [topic-slug].mp3          # Audio (via ElevenLabs MCP)
│       ├── [topic-slug].srt          # Subtitles (via subs)
│       ├── descriptions.txt          # Platform metadata
│       └── captions.txt              # For SRT generation
└── examples/                         # Example conversations
```

## Available Commands

| Command | Purpose | Use When |
|---------|---------|----------|
| `/givore-create` | Full pipeline: Script → Audio → Captions → SRT → Metadata | Complete content creation |
| `/givore-script` | Script generation only | Planning content, no audio yet |
| `/givore-metadata` | Metadata + captions only | After manual script edit |

## Unified Workflow (`/givore-create`)

```
/givore-create [inputs]
│
├─ Script generation (via /givore-script logic)
├─ ⏸️ APPROVAL GATE
├─ Audio generation (ElevenLabs MCP)
├─ Metadata + captions (via /givore-metadata logic)
├─ SRT subtitles (subs command)
└─ Final summary
```

## Key Success Factors (Research-Based)
- 71% of viewers decide to keep watching within 3 seconds - Hook is everything
- Videos with proof/payoff outperform promises by 10x
- Emotional triggers increase shares by 5x
- Completion rate determines distribution
