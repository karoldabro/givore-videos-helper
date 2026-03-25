# Givore Clip Extraction Pipeline

Automated extraction of interesting clips from cycling POV footage using CLIP + YOLO + optical flow analysis.

## Constants

```
GIVORE_ROOT  = /media/kdabrow/Programy/givore
GIVORE_TOOLS = /media/kdabrow/Programy/givore/scripts/givore-tools.sh
GIVORE_DB    = /media/kdabrow/Programy/givore/scripts/givore_db.py
EXTRACTOR    = /home/kdabrow/.venv/clip_extractor/bin/python3 /media/kdabrow/Programy/givore/scripts/clip_extractor.py
CLIPS_DIR    = /media/kdabrow/Programy/givore/videos/clips
REVIEW_JSON  = /tmp/clip_extractor_results.json
```

## CLI Tools (MANDATORY)

| Task | Command |
|------|---------|
| Extract clips (dry run) | `$GIVORE_TOOLS extract-clips <video> --location <name> --dry-run` |
| Extract clips (full) | `$GIVORE_TOOLS extract-clips <video> --location <name>` |
| Import clips to DB | `python3 $GIVORE_DB bulk-add $REVIEW_JSON` |
| Check recent clips | `$GIVORE_TOOLS video-recent-clips --last 5` |
| List clips | `python3 $GIVORE_DB list` |

---

## PHASE 0: INPUT COLLECTION

### Parse `$ARGUMENTS`

Expected format: `<video_path> <location>` or `<video_path> --location <location>`

Examples:
- `/givore-extract /media/kdabrow/Programy/givore/videos/20260314/DJI_20260314184522_0014_D.MP4 ayora`
- `/givore-extract /media/kdabrow/Programy/givore/videos/20260314/DJI_20260314184522_0014_D.MP4 --location ayora`

### If arguments incomplete, ask:

```
Video path and location needed.

1. Video file path (absolute path to .MP4)
2. Location name for clip filenames (e.g., ayora, trinitat, zaidia)
```

### Validate:
- Video file exists
- Location is provided (lowercase, no spaces — use hyphens)
- If video has `.LRF` sibling, note it will be used as proxy (automatic)

---

## PHASE 1: DRY RUN ANALYSIS

Run the extractor in dry-run mode to preview what will be extracted:

```bash
$GIVORE_TOOLS extract-clips <video> --location <location> --dry-run
```

### Present results to user:

Show the clip list with timestamps and descriptions. Format as a table:

```
| # | Time Range | Description | Score |
|---|------------|-------------|-------|
| 1 | 2:30-2:35  | cycling past shops and cafes with pedestrians | 0.681 |
| 2 | 3:11-3:16  | cycling through narrow street crowded with people | 0.663 |
...
```

Also note:
- Total clips found
- Processing time
- Whether LRF proxy was used

---

## PHASE 2: APPROVAL GATE

Ask the user:

```
Found N clips from the video. Options:

1. Extract all N clips (default)
2. Extract with different settings (e.g., --top-percent 50, --min-gap 2)
3. Abort
```

### If user wants different settings:
Re-run dry run with the adjusted parameters. Common adjustments:
- `--top-percent <N>` — keep more/fewer clips (default 30)
- `--min-gap <N>` — minimum seconds between clips (default 3)
- `--max-clips <N>` — hard limit on clip count
- `--min-duration <N>` / `--max-duration <N>` — clip length bounds (default 2-5s)

### If user approves → proceed to Phase 3

---

## PHASE 3: FULL EXTRACTION

Run the extractor without `--dry-run`:

```bash
$GIVORE_TOOLS extract-clips <video> --location <location>
```

This will:
1. Analyze video (using LRF proxy if available)
2. Extract clips from the **original** video (not proxy)
3. Scale to 1080x1920 (from 2K source)
4. Save clips to `$CLIPS_DIR`
5. Generate `$REVIEW_JSON` (bulk-add compatible)

---

## PHASE 4: REVIEW & METADATA ADJUSTMENT

Read the generated review JSON:

```bash
cat /tmp/clip_extractor_results.json
```

Present the clips with their auto-generated metadata to the user:

```
| # | Filename | Style | Mood | Sections |
|---|----------|-------|------|----------|
| 1 | cycling past shops... - ayora.mp4 | cycling_pov | playful | body |
...
```

Ask user:

```
Review the auto-generated metadata above.

1. Import as-is (default)
2. Let me adjust metadata before import (I'll edit the JSON)
3. Let me rename specific clips
```

### If user wants adjustments:
- Edit the JSON at `$REVIEW_JSON` based on user feedback
- Valid styles: cycling_pov, cycling_path, landmark, item_shot, reveal, setup, transition
- Valid moods: calm, dramatic, energetic, playful
- Valid sections: hook, body, bridge, cta, end, problem, importance, solution, proof, rehook, setup, item, start

---

## PHASE 5: IMPORT TO DATABASE

```bash
python3 $GIVORE_DB bulk-add $REVIEW_JSON
```

Report the imported clip IDs and confirm success.

---

## PHASE 6: CLEANUP SUMMARY

Report final summary:

```
Extraction complete:
- Source: <video filename>
- Proxy used: yes/no
- Clips extracted: N
- Clip IDs: #X - #Y
- Location: <location>
- Processing time: X min
- Clips saved to: videos/clips/
```

---

## Optional Parameters Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--fps N` | auto (2 for >10min, 3 for shorter) | Frame extraction rate |
| `--top-percent N` | 30 | Keep top N% of detected peaks |
| `--min-duration N` | 2.0 | Minimum clip length in seconds |
| `--max-duration N` | 5.0 | Maximum clip length in seconds |
| `--min-gap N` | 3.0 | Minimum gap between clips in seconds |
| `--max-clips N` | unlimited | Hard limit on number of clips |
| `--no-proxy` | false | Skip LRF proxy, analyze original |
| `--batch-size N` | 8 | GPU inference batch size |

## Config Tuning

Text queries and scoring weights are in `scripts/clip_extractor_config.json`. Edit to:
- Add new CLIP text queries for different scene types
- Adjust scoring weights (motion, CLIP interest, diversity, objects)
- Change object bonus/penalty values
