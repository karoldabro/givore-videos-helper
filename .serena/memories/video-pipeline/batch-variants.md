# Batch Variant Pipeline

## Command
`/givore-batch` — `.claude/commands/givore-batch.md`
Added: 2026-03-11

## Purpose
Generate 7 variants of one topic in a single session. Optimizes context usage by reading reference files once and delta-generating variants 2-7 from variant 1 base.

## Token Budget
- Phase A (base analysis, one-time reads): ~12K tokens
- Phase B (variant 1, full pipeline): ~18K tokens
- Phase D (variants 2-7, delta each): ~7K tokens × 6 = ~42K tokens
- Total: ~72K tokens vs ~203K naive (65% savings)

## Modes
- **Street-finds**: Auto-detected (default). Uses 9 ref files + `givore-tools.sh script-rotation`
- **Trial**: Detected by audience keywords (RENOVATING, NEW-HOUSE, etc.). Uses 7 trial ref files + `givore-tools.sh trial-rotation`
- Both modes share: CLIPS_CATALOG, SFX_CATALOG, `givore-tools.sh video-recent-clips`, METADATA_INSTRUCTIONS

## Folder Structure
```
projects/[prefix][date]_[slug]/
├── BATCH_MANIFEST.md    # Variant matrix + used elements tracking
├── v1/ .. v7/           # Each has: .txt, .mp3, .srt, captions.txt, descriptions.txt, clip_map.txt, project.json, project.mlt, draft.mp4
└── finals/              # vN_[slug]_final.mp4 (only approved)
```

## Phases
1. **A: Base Analysis** — read all ref files ONCE, compute rotation constraints, pre-plan variant matrix (7 hooks, 7 CTAs, 7 clips, 7 SFX)
2. **B: Variant 1** — full pipeline (script→approval→audio→metadata→clips→approval→assembly→draft)
3. **C: Matrix Approval** — display planned v2-v7 differences, user approves or modifies
4. **D: Batch v2-v7** — delta generation (no approvals): swap hook/CTA/rehook/problem, tweak wording, swap visual hook clips, shuffle body clips, different SFX
5. **E: Review & Finalize** — present all 7 drafts, user selects which to final-render, update global histories (v1 only)

## Key Design Decisions
- Only v1 updates global rotation DB (script-rotation / video-recent-clips / trial-rotation via `givore-tools.sh`) — prevents rotation pollution
- BATCH_MANIFEST.md handles intra-batch rotation (no duplicate elements across variants)
- Assembly configs written to `project-folder/vN/assembly_config.json` (absolute paths required)
- Use `givore-tools.sh generate-config` to auto-create configs from audio + clip IDs
- Use `givore-tools.sh render-all <dir> draft` / `final` to batch-render all variants
- Use `givore-tools.sh copy-finals <dir>` to collect finals
- Draft-first: all 7 drafts before any final render
- SFX temporarily disabled (set `"sfx": []` in configs) — to be fixed in separate session
- Each variant gets unique: script, ElevenLabs audio, 5-platform metadata, video assembly

## Delta Rules (v2-v7)
What changes: Hook type+wording, CTA type+wording, Re-hook style, Problem angle framing, 2-3 body sentences, visual hook clips (first 1-2), body clip order+replacements, SFX set
What stays: Core message, items, condition, location, section structure, voice settings, video profile
