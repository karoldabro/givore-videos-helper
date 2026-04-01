#!/usr/bin/env python3
"""Gemini-based video content extractor for Givore.

Uploads cycling POV footage to Google Gemini API and runs multiple
specialized analysis passes to detect street finds, scenic moments,
barrio character, and action/hook clips.

Usage:
    gemini-extract <video> --location <name> [options]

Requires GEMINI_API_KEY environment variable.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Gemini video content extractor")
    sub = p.add_subparsers(dest="command", help="Command to run")

    # Default: analyze mode (no subcommand needed for backwards compat)
    p.add_argument("video", nargs="?", help="Path to video file (MP4 or LRF)")
    p.add_argument("--location", help="Location name for this ride")
    p.add_argument("--model", default="gemini-2.5-flash", help="Gemini model")
    p.add_argument("--trim-start", type=int, default=0, help="Seconds to trim from start")
    p.add_argument("--scale", type=int, default=0, help="Downscale to this height (e.g. 480)")
    p.add_argument("--passes", default="street_finds,scenic,barrio,action",
                   help="Comma-separated pass names to run")
    p.add_argument("--output", default="/tmp/gemini_extractor_results.json",
                   help="Output JSON path")
    p.add_argument("--dry-run", action="store_true",
                   help="Prepare video but don't upload or analyze")
    p.add_argument("--keep-temp", action="store_true",
                   help="Don't delete temporary prepared video")

    # Cut subcommand
    cut = sub.add_parser("cut", help="Cut clips from original video using results JSON")
    cut.add_argument("results_json", help="Path to gemini_extractor_results.json")
    cut.add_argument("--source", help="Override source video path (default: from JSON)")
    cut.add_argument("--clips-dir", default="/media/kdabrow/Programy/givore/videos/clips",
                     help="Output directory for clips")
    cut.add_argument("--min-confidence", type=float, default=0.0,
                     help="Only cut clips with confidence >= this value")
    cut.add_argument("--min-hook", type=float, default=0.0,
                     help="Only cut clips with hook_potential >= this value")
    cut.add_argument("--clip-types", default="",
                     help="Comma-separated clip types to include (empty = all)")
    cut.add_argument("--bulk-add-only", action="store_true",
                     help="Only generate bulk-add JSON, don't cut clips")

    return p.parse_args()


# ---------------------------------------------------------------------------
# Video preparation
# ---------------------------------------------------------------------------

def get_video_duration(path):
    """Get video duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def prepare_video(video_path, trim_start=0, scale=0):
    """Remux/trim/scale video to a Gemini-compatible MP4. Returns temp path."""
    src = Path(video_path)
    suffix = src.suffix.lower()

    # Build ffmpeg command
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", prefix="gemini_extract_",
                                      dir="/tmp", delete=False)
    tmp.close()
    out_path = tmp.name

    cmd = ["ffmpeg", "-y"]

    # Trim from start (fast seek before input)
    if trim_start > 0:
        cmd += ["-ss", str(trim_start)]

    cmd += ["-i", str(src)]

    # Video filters
    vf_parts = []
    if scale > 0:
        vf_parts.append(f"scale=-2:{scale}")

    if vf_parts:
        cmd += ["-vf", ",".join(vf_parts)]
        cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "23"]
    elif suffix == ".lrf":
        # LRF remux: just copy streams
        cmd += ["-c:v", "copy"]
    else:
        cmd += ["-c:v", "copy"]

    cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd += ["-movflags", "+faststart"]
    cmd += [out_path]

    print(f"[PREPARE] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    duration = get_video_duration(out_path)
    print(f"[PREPARE] Output: {out_path}")
    print(f"[PREPARE] Size: {size_mb:.1f} MB, Duration: {duration:.0f}s ({duration/60:.1f} min)")

    if size_mb > 2000:
        print(f"[WARNING] File is {size_mb:.0f} MB — exceeds Gemini 2GB limit!", file=sys.stderr)

    return out_path, duration


# ---------------------------------------------------------------------------
# Gemini upload & analysis
# ---------------------------------------------------------------------------

def upload_video(client, video_path):
    """Upload video to Gemini File API and wait for processing."""
    print(f"[UPLOAD] Uploading {video_path}...")
    video_file = client.files.upload(file=video_path)
    print(f"[UPLOAD] File name: {video_file.name}, state: {video_file.state}")

    # Wait for processing
    while video_file.state.name == "PROCESSING":
        print(f"[UPLOAD] Processing... (waiting 10s)")
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        print(f"[ERROR] File processing failed: {video_file.state}", file=sys.stderr)
        sys.exit(1)

    print(f"[UPLOAD] Ready! State: {video_file.state.name}")
    return video_file


def run_pass(client, model_name, video_file, pass_name, pass_prompt, max_retries=3):
    """Run a single analysis pass against the uploaded video."""
    from google.genai import types

    print(f"\n[PASS:{pass_name}] Starting analysis...")
    start = time.time()

    # gemini-2.5-pro minimum thinking_budget is 128, Flash can use 0
    thinking_budget = 128 if "pro" in model_name else 0

    config = types.GenerateContentConfig(
        max_output_tokens=65536,
        response_mime_type="application/json",
        thinking_config=types.ThinkingConfig(
            thinking_budget=thinking_budget
        ),
    )

    # Retry with backoff for rate limits
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[video_file, pass_prompt],
                config=config,
            )
            break
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                wait = 60 * (attempt + 1)
                print(f"[PASS:{pass_name}] Rate limited. Waiting {wait}s before retry {attempt+2}/{max_retries}...")
                time.sleep(wait)
                if attempt == max_retries - 1:
                    print(f"[ERROR] Rate limit exceeded after {max_retries} retries", file=sys.stderr)
                    return []
            else:
                raise

    elapsed = time.time() - start
    print(f"[PASS:{pass_name}] Completed in {elapsed:.1f}s")

    # Parse JSON response
    text = response.text.strip()
    try:
        results = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[PASS:{pass_name}] JSON parse error: {e}", file=sys.stderr)
        print(f"[PASS:{pass_name}] Raw response saved to /tmp/gemini_raw_{pass_name}.txt")
        Path(f"/tmp/gemini_raw_{pass_name}.txt").write_text(text)
        results = []

    count = len(results) if isinstance(results, list) else 0
    print(f"[PASS:{pass_name}] Found {count} detections")

    # Post-process: fix invalid clip_types and tag with pass name
    valid_clip_types = {"hook", "start", "end", "bridge", "item", "body"}
    valid_paces = {"dynamic", "moderate", "slow", "calm", "sharp"}
    if isinstance(results, list):
        for r in results:
            r["pass"] = pass_name
            if r.get("clip_type") not in valid_clip_types:
                r["clip_type"] = "body"
            if r.get("pace") not in valid_paces:
                r["pace"] = "moderate"

    return results


# ---------------------------------------------------------------------------
# Prompt definitions
# ---------------------------------------------------------------------------

PREAMBLE = """You are analyzing cycling POV footage from Valencia, Spain.
The camera is chest-mounted on the cyclist, pointing forward. Handlebars are usually
visible at the bottom of frame. Sometimes other camera angles are used (handlebar mount,
rear-facing, etc.) — note when the perspective differs from standard forward chest-mount.

This footage is used to create short-form social media content (TikTok/Instagram Reels).

CLIP LENGTH RULES:
- Hooks: 1-3 seconds ONLY (short, punchy, attention-grabbing)
- All other clips: 2-5 seconds maximum. NEVER longer than 5 seconds.

QUALITY THRESHOLD: Be VERY SELECTIVE. For a 30-minute video, return only 10-30 of the BEST
moments for this pass. Skip generic cycling, empty streets, and unremarkable scenes.
If a scene continues for a long stretch (e.g., cycling along a beach avenue for 3 minutes),
flag it as ONE clip at the most visually interesting point — do NOT create multiple entries
for the same continuous scene. Each detection must be DISTINCT from all others.

CLIP TYPE — you MUST use exactly one of these 6 values. NO OTHER VALUES ARE ALLOWED:
- "hook": 1-3 seconds. Unexpected event, dramatic movement, visual surprise, something
  extraordinary that would stop a viewer scrolling. Must be short and punchy.
- "start": natural video opening — camera descends from sky to handlebars, cyclist
  begins riding, establishing wide shot before motion
- "end": natural video closing — camera lifts to sky/trees/rooftops, cyclist stops
- "bridge": SPECIFICALLY a horizontal camera pan (left-to-right or right-to-left) that
  can be used to join two scenes together. NOT a turn or street change.
- "item": street find — discarded furniture/object on sidewalk being approached.
  Often found next to trash bins or against building walls.
- "body": any other interesting content worth using in a video

STRICT RULE: The clip_type field MUST be one of exactly these 6 strings:
"hook", "start", "end", "bridge", "item", "body"
Any other value like "camera_movement", "high_energy", "atmospheric", "calm",
"traffic_contrast" etc. is INVALID. Use "body" for all general content.
If you use an invalid clip_type, the entire entry will be rejected.

PACE — you MUST use exactly one of these 5 values:
- "dynamic": fast cycling, sharp turns, high energy
- "moderate": normal cruising speed, steady movement
- "slow": approaching something, stopping, narrow street
- "calm": very slow or stationary, contemplative
- "sharp": sudden speed/direction changes

HOOK POTENTIAL (0.0-1.0): How well this clip would work as the FIRST clip to stop scrolling.

JSON SCHEMA — each object MUST have exactly these fields:
- "timestamp_start": string, MM:SS format
- "timestamp_end": string, MM:SS format (hooks: 1-3s, others: 2-5s max)
- "clip_type": string, ONLY one of: "hook", "start", "end", "bridge", "item", "body"
- "pace": string, one of: "dynamic", "moderate", "slow", "calm", "sharp"
- "hook_potential": number, 0.0 to 1.0
- "category": string, from the pass-specific list below
- "description": string, 10-30 words in English
- "confidence": number, 0.0 to 1.0
- "suggested_formats": array of strings (format IDs)
- "notes": string, additional editing context

Return ONLY a valid JSON array. No markdown, no code fences, no explanation.
"""

PASSES = {
    "street_finds": {
        "description": "Street Finds & Items",
        "prompt": PREAMBLE + """
PASS FOCUS: Detect any discarded items on sidewalks/streets.

Categories (use one for the "category" field):
- "street_find_furniture": chairs, tables, shelves, sofas, beds, wardrobes
- "street_find_appliance": electronics, lamps, kitchen items, small appliances
- "street_find_decor": frames, mirrors, decorative objects, plants/pots
- "street_find_textile": mattresses, rugs, curtains, clothing piles
- "street_find_other": boxes, bags of items, miscellaneous discarded goods

For EACH item also include these extra fields:
- "item_condition": one of:
  - "good": the item is useful, just cleaning needed
  - "to_renovation": the item needs some work but can be rescued or repurposed
  - "bad": the item is destroyed or has parts missing
- "estimated_size": "small" / "medium" / "large"
- "renueva_potential": true or false (could this be upcycled/renovated?)

IMPORTANT: Only flag items ABANDONED ON THE STREET (next to dumpsters, on sidewalks,
against walls). NOT items in shop windows, on terraces, or being used normally.
Items near gray/green containers (contenedores) are almost always discarded.

This pass typically finds 0-10 items depending on the route. Quality over quantity —
only flag items you can clearly identify. If unsure whether something is discarded, skip it.

Suggested formats to use:
- "FORMAT_9" (No Toqueis Eso — damaged/problematic items)
- "FORMAT_14" (El Mapa de Hallazgos — mapping finds)
- "FORMAT_16" (El Que Tira Gana — before/after rescue stories)
- "FORMAT_19" (Cuanto Cuesta — price shock reveal)
- "FORMAT_20" (Classic Street Finds — standard find content)
""",
    },
    "scenic": {
        "description": "Scenic & Atmospheric",
        "prompt": PREAMBLE + """
PASS FOCUS: Hidden beauty, atmospheric moments, audio-quality segments.

Categories (use one for the "category" field):
- "hidden_beauty": unexpected courtyards, rooftop gardens, cat colonies, tucked-away plazas
- "architecture": interesting facades, historic buildings, unique doorways, tile work
- "street_art": murals, graffiti, installations, creative expressions
- "atmospheric": rain, wet street reflections, golden hour light, long shadows, fog
- "night_scene": neon lights, empty streets at night, city lights
- "nature_in_city": trees, flowers, parks, gardens, urban wildlife

Also include these extra fields where applicable:
- "lighting": "harsh" / "soft" / "golden" / "dramatic" / "flat" / "night"

SELECTIVITY: Only flag scenes that are visually STRIKING or have distinctive atmosphere.
A normal tree-lined street is NOT interesting. A hidden courtyard glimpsed through a gate IS.
Normal daylight cycling is NOT atmospheric. Golden hour shadows on a baroque facade IS.
Skip generic parks, standard streets, and ordinary buildings.

CRITICAL: If you cycle along a scenic avenue, beach, or park for several minutes, that is
ONE clip at the single most beautiful moment — NOT 10+ entries every 15 seconds.
Aim for 10-15 genuinely remarkable scenic moments from a 30-minute ride.

DO NOT flag: ambient audio/sound moments, street finds, food spots, community activity,
or action/hooks. Focus ONLY on visual beauty and atmosphere.

Suggested formats to use:
- "FORMAT_3" (Lo Que Nadie Ve — hidden beauty reveals)
- "FORMAT_6" (Sonidos de la Calle — ambient sound content, zero narration)
- "FORMAT_17" (Lluvia Noche Extremo — rain/night cinematic)
""",
    },
    "barrio": {
        "description": "Barrio & Community",
        "prompt": PREAMBLE + """
PASS FOCUS: Neighborhood character, community life, food, and local identity.

Categories (use one for the "category" field):
- "landmark": recognizable buildings, churches, monuments, plazas with names
- "local_business": interesting shops, traditional stores, artisan workshops
- "food_spot": bars, restaurants, bakeries, food vendors, market stalls
- "community_activity": people gathering, market day, street events, kids playing
- "changed_location": closed/boarded shops, construction, visible gentrification signs
- "signage": interesting street signs, barrio names, historic plaques
- "lively_street": busy pedestrian areas, terrace culture, street vendors

If you can identify the barrio or street name from visible signs, include it in "notes".

SELECTIVITY: Only flag locations with real CHARACTER — a distinctive landmark, a visibly
closed/changed shop, an actual food spot you can see, a genuinely bustling street scene.
Do NOT flag: generic residential streets, standard intersections, ordinary shops with
nothing distinctive, empty plazas. Each detection should be a place worth showing on camera.

CRITICAL: If cycling through a long street or area, flag ONE clip at the most interesting
point — NOT multiple entries for the same continuous stretch. Aim for 10-20 total.

DO NOT flag: items on street, scenic beauty without neighborhood context, high-energy
cycling action. Focus on PLACE IDENTITY.

Suggested formats to use:
- "FORMAT_2" (60 Segundos en... — 60-second barrio tour)
- "FORMAT_11" (Antes Aqui Habia — before/after changed locations)
- "FORMAT_13" (Tres Cosas — 3 interesting facts about a barrio)
- "FORMAT_15" (Ruta Gastro en Bici — food stops by bike)
""",
    },
    "action": {
        "description": "Action, Hooks & Transitions",
        "prompt": PREAMBLE + """
PASS FOCUS: Energy, movement quality, weird moments, and structural clips (hooks/bridges/endings).

Categories (use one for the "category" field):
- "high_energy": fast cycling, dodging, tight spaces, near-misses (safe ones)
- "weird_unusual": anything unexpected — strange objects, funny situations, odd scenes
- "smooth_ride": long uninterrupted stretches good for timelapse or bridges
- "traffic_contrast": moments showing bike vs car advantage (bike lanes, shortcuts)
- "camera_movement": interesting camera angles, looking around, perspective shifts
- "sky_shot": camera pointing up at sky, tree canopy, rooftops — good for start/end clips
- "establishing": wide shots of intersections, plazas, streets — good opening/closing material
- "pet_spotted": dogs, cats, birds — animals encountered during ride

Pay special attention to HOOK POTENTIAL here — but be selective. A "hook" must be
something a viewer has NOT seen before in cycling content. Normal fast cycling is NOT
a hook. A near-miss with a pedestrian IS. Normal traffic is NOT a hook. A bus passing
dangerously close IS.

SELECTIVITY: Aim for 10-20 high-quality action/structural clips. Every detection should
be something you'd genuinely use in a video edit. Skip: normal cycling at any speed,
standard turns, ordinary traffic, generic intersections.

DO NOT flag: items on street (that's the street_finds pass), scenic beauty (that's scenic),
or neighborhood identity (that's barrio). Focus ONLY on action, energy, weird moments,
and structural clips (hooks/bridges/starts/ends).

Suggested formats to use:
- "FORMAT_1" (El Ranking Callejero — ranked list of finds)
- "FORMAT_4" (Bici vs Coche — bike vs car contrast)
- "FORMAT_8" (Timelapse Rutero — hyperlapse route)
- "FORMAT_10" (POV Eres Mi Bici — character voice format)
- "FORMAT_12" (Lo Mas Raro de Hoy — weirdest thing today)
""",
    },
}


# ---------------------------------------------------------------------------
# Timestamp utilities
# ---------------------------------------------------------------------------

def mmss_to_seconds(mmss):
    """Convert MM:SS string to seconds."""
    try:
        parts = mmss.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except (ValueError, AttributeError):
        pass
    return 0


def adjust_timestamps(results, trim_offset):
    """Add trim offset to all timestamps, compute original_*_seconds."""
    for r in results:
        start_s = mmss_to_seconds(r.get("timestamp_start", "0:00"))
        end_s = mmss_to_seconds(r.get("timestamp_end", "0:00"))
        r["original_start_seconds"] = start_s + trim_offset
        r["original_end_seconds"] = end_s + trim_offset
    return results


def deduplicate(results, overlap_threshold=5):
    """Remove overlapping detections across all passes. Keep the best per time window."""
    if not results:
        return results

    results.sort(key=lambda r: r.get("original_start_seconds", 0))
    deduped = [results[0]]

    for r in results[1:]:
        prev = deduped[-1]
        overlap = prev.get("original_end_seconds", 0) >= r.get("original_start_seconds", 0) - overlap_threshold

        if overlap:
            # Same time window — keep the one with higher confidence, or higher hook_potential as tiebreak
            prev_score = prev.get("confidence", 0) + prev.get("hook_potential", 0) * 0.5
            r_score = r.get("confidence", 0) + r.get("hook_potential", 0) * 0.5

            # If the new one is a different clip_type and both are high quality, keep both
            different_type = r.get("clip_type") != prev.get("clip_type")
            both_good = prev_score >= 1.0 and r_score >= 1.0
            if different_type and both_good:
                deduped.append(r)
            elif r_score > prev_score:
                deduped[-1] = r
        else:
            deduped.append(r)

    return deduped


# ---------------------------------------------------------------------------
# Clip cutting
# ---------------------------------------------------------------------------

# Map clip_type to filename prefix
TYPE_PREFIX_MAP = {
    "hook": "[hook]",
    "item": "[item]",
    "bridge": "[bridge]",
    "end": "[end]",
    "start": "[start]",
    "body": "",
}

# Map pace to motion_tag
PACE_TO_MOTION = {
    "dynamic": "dynamic",
    "sharp": "sharp",
    "moderate": "moderate",
    "slow": "slow",
    "calm": "calm",
}

# Map clip_type to sections
TYPE_TO_SECTIONS = {
    "hook": ["hook"],
    "item": ["body", "item"],
    "bridge": ["bridge"],
    "end": ["end"],
    "start": ["hook"],
    "body": ["body"],
}


def make_clip_filename(detection, location):
    """Generate a clip filename from detection metadata."""
    prefix = TYPE_PREFIX_MAP.get(detection.get("clip_type", ""), "")
    motion = detection.get("pace", "moderate")
    desc = detection.get("description", "unknown scene")
    # Truncate and clean description for filename
    desc = desc[:60].strip().rstrip(".")
    # Remove characters invalid in filenames
    for ch in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        desc = desc.replace(ch, '')

    parts = []
    if prefix:
        parts.append(prefix)
    parts.append(f"({motion})")
    parts.append(f"{desc} - {location}.mp4")
    return " ".join(parts)


def cut_clip(source_video, detection, output_path):
    """Cut a single clip from the source video using ffmpeg."""
    start = detection.get("original_start_seconds", 0)
    end = detection.get("original_end_seconds", start + 3)
    duration = end - start

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", str(source_video),
        "-t", str(duration),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx265", "-preset", "slow", "-crf", "15",
        "-pix_fmt", "yuv420p10le",
        "-tag:v", "hvc1",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] ffmpeg failed: {result.stderr[:200]}", file=sys.stderr)
        return False
    return True


def generate_bulk_add_json(detections, location):
    """Convert Gemini detections to bulk-add compatible format."""
    entries = []
    for d in detections:
        clip_type = d.get("clip_type", "body")
        filename = make_clip_filename(d, location)
        entry = {
            "filename": filename,
            "sections": TYPE_TO_SECTIONS.get(clip_type, ["body"]),
            "style": "item_shot" if clip_type == "item" else "cycling_pov",
            "mood": _map_mood(d),
            "desc": d.get("description", ""),
            "visual_hook": clip_type == "hook" or d.get("hook_potential", 0) >= 0.7,
            "type_prefix": TYPE_PREFIX_MAP.get(clip_type, "").strip("[]"),
            "motion_tag": PACE_TO_MOTION.get(d.get("pace", "moderate"), "moderate"),
        }
        # Preserve Gemini metadata for reference
        entry["_gemini"] = {
            "category": d.get("category"),
            "confidence": d.get("confidence"),
            "hook_potential": d.get("hook_potential"),
            "suggested_formats": d.get("suggested_formats"),
            "pass": d.get("pass"),
            "original_start_seconds": d.get("original_start_seconds"),
            "original_end_seconds": d.get("original_end_seconds"),
        }
        # Item-specific fields
        if clip_type == "item":
            entry["_gemini"]["item_condition"] = d.get("item_condition")
            entry["_gemini"]["estimated_size"] = d.get("estimated_size")
            entry["_gemini"]["renueva_potential"] = d.get("renueva_potential")
        entries.append(entry)
    return entries


def _map_mood(detection):
    """Map pace + hook_potential to mood."""
    pace = detection.get("pace", "moderate")
    hook = detection.get("hook_potential", 0)
    if pace in ("dynamic", "sharp") or hook >= 0.8:
        return "energetic"
    if pace == "calm":
        return "calm"
    if hook >= 0.6:
        return "playful"
    return "calm"


def cmd_cut(args):
    """Cut clips from original video using analysis results."""
    # Load results
    results_path = Path(args.results_json)
    if not results_path.exists():
        print(f"[ERROR] Results file not found: {results_path}", file=sys.stderr)
        sys.exit(1)

    with open(results_path) as f:
        data = json.load(f)

    merged = data.get("merged", [])
    location = data.get("location", "unknown")
    source_video = Path(args.source) if args.source else Path(data.get("source_video", ""))

    # Find the original MP4 (not LRF) for cutting
    if source_video.suffix.lower() == ".lrf":
        mp4_path = source_video.with_suffix(".MP4")
        if mp4_path.exists():
            source_video = mp4_path
            print(f"[CUT] Using original MP4: {source_video}")
        else:
            print(f"[CUT] No MP4 found, using LRF: {source_video}")

    if not source_video.exists():
        print(f"[ERROR] Source video not found: {source_video}", file=sys.stderr)
        sys.exit(1)

    clips_dir = Path(args.clips_dir)
    clips_dir.mkdir(parents=True, exist_ok=True)

    # Filter detections
    filtered = merged
    if args.min_confidence > 0:
        filtered = [d for d in filtered if d.get("confidence", 0) >= args.min_confidence]
    if args.min_hook > 0:
        filtered = [d for d in filtered if d.get("hook_potential", 0) >= args.min_hook]
    if args.clip_types:
        allowed = set(args.clip_types.split(","))
        filtered = [d for d in filtered if d.get("clip_type") in allowed]

    print(f"[CUT] Source: {source_video}")
    print(f"[CUT] Output dir: {clips_dir}")
    print(f"[CUT] Clips to cut: {len(filtered)} (from {len(merged)} total)")

    # Generate bulk-add JSON
    bulk_entries = generate_bulk_add_json(filtered, location)
    bulk_path = "/tmp/gemini_extractor_bulk_add.json"
    with open(bulk_path, "w") as f:
        json.dump(bulk_entries, f, indent=2, ensure_ascii=False)
    print(f"[CUT] Bulk-add JSON: {bulk_path}")

    if args.bulk_add_only:
        print(f"[CUT] Bulk-add only mode — skipping clip extraction")
        for i, entry in enumerate(bulk_entries):
            print(f"  {i+1:3d}. {entry['filename']}")
        return

    # Cut clips
    success = 0
    for i, (detection, entry) in enumerate(zip(filtered, bulk_entries)):
        filename = entry["filename"]
        output_path = clips_dir / filename
        orig_s = detection.get("original_start_seconds", 0)
        orig_e = detection.get("original_end_seconds", 0)

        print(f"  [{i+1}/{len(filtered)}] {orig_s}s-{orig_e}s → {filename}")

        if output_path.exists():
            print(f"    [SKIP] Already exists")
            success += 1
            continue

        if cut_clip(source_video, detection, output_path):
            success += 1
        else:
            # Remove failed output
            output_path.unlink(missing_ok=True)

    print(f"\n[CUT] Done: {success}/{len(filtered)} clips extracted")
    print(f"[CUT] Clips in: {clips_dir}")
    print(f"[CUT] Bulk-add JSON: {bulk_path}")
    print(f"\nTo import to DB:")
    print(f"  python3 scripts/givore_db.py bulk-add {bulk_path}")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_summary(merged, passes_data):
    """Print a summary table to terminal."""
    print("\n" + "=" * 80)
    print("GEMINI EXTRACTION RESULTS")
    print("=" * 80)

    # Stats by pass
    by_pass = {}
    by_clip_type = {}
    by_pace = {}
    high_hooks = 0

    for r in merged:
        p = r.get("pass", "unknown")
        by_pass[p] = by_pass.get(p, 0) + 1

        ct = r.get("clip_type", "unknown")
        by_clip_type[ct] = by_clip_type.get(ct, 0) + 1

        pace = r.get("pace", "unknown")
        by_pace[pace] = by_pace.get(pace, 0) + 1

        if r.get("hook_potential", 0) >= 0.7:
            high_hooks += 1

    print(f"\nTotal detections: {len(merged)}")
    print(f"By pass: {json.dumps(by_pass)}")
    print(f"By clip type: {json.dumps(by_clip_type)}")
    print(f"By pace: {json.dumps(by_pace)}")
    print(f"High hook potential (>=0.7): {high_hooks}")

    # Top hooks
    hooks = sorted(merged, key=lambda r: r.get("hook_potential", 0), reverse=True)[:5]
    if hooks:
        print(f"\nTop 5 hooks:")
        for h in hooks:
            orig_s = h.get('original_start_seconds', 0)
            orig_e = h.get('original_end_seconds', 0)
            sm, ss = divmod(orig_s, 60)
            em, es = divmod(orig_e, 60)
            print(f"  {sm:02d}:{ss:02d}-{em:02d}:{es:02d} [{h.get('clip_type','?'):6s}] "
                  f"hook={h.get('hook_potential',0):.2f} "
                  f"{h.get('category','?'):25s} {h.get('description','')[:60]}")

    # All detections timeline
    print(f"\nFull timeline:")
    for r in merged:
        orig_s = r.get('original_start_seconds', 0)
        orig_e = r.get('original_end_seconds', 0)
        sm, ss = divmod(orig_s, 60)
        em, es = divmod(orig_e, 60)
        print(f"  {sm:02d}:{ss:02d}-{em:02d}:{es:02d} "
              f"[{r.get('clip_type','?'):6s}] {r.get('pace','?'):8s} "
              f"hook={r.get('hook_potential',0):.1f} "
              f"{r.get('category','?'):25s} {r.get('description','')[:50]}")

    print("=" * 80)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    # Handle cut subcommand
    if args.command == "cut":
        cmd_cut(args)
        return

    # Analyze mode — need video argument
    if not args.video:
        print("[ERROR] Video path required for analysis mode", file=sys.stderr)
        sys.exit(1)
    if not args.location:
        print("[ERROR] --location required for analysis mode", file=sys.stderr)
        sys.exit(1)

    # Check API key (not needed for dry-run)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("[ERROR] GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("Get one at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)

    # Check video exists
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"[ERROR] Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    orig_duration = get_video_duration(video_path)
    print(f"[INFO] Source: {video_path}")
    print(f"[INFO] Duration: {orig_duration:.0f}s ({orig_duration/60:.1f} min)")
    print(f"[INFO] Model: {args.model}")
    print(f"[INFO] Location: {args.location}")
    print(f"[INFO] Trim start: {args.trim_start}s, Scale: {args.scale or 'original'}")

    # Step 1: Prepare video
    prepared_path, prepared_duration = prepare_video(
        video_path, trim_start=args.trim_start, scale=args.scale
    )

    if args.dry_run:
        print(f"\n[DRY-RUN] Video prepared at {prepared_path}")
        print(f"[DRY-RUN] Would upload and run passes: {args.passes}")
        if not args.keep_temp:
            os.unlink(prepared_path)
            print(f"[DRY-RUN] Cleaned up temp file")
        return

    # Step 2: Upload to Gemini
    from google import genai
    client = genai.Client(api_key=api_key)

    video_file = upload_video(client, prepared_path)

    # Step 3: Run analysis passes
    selected_passes = [p.strip() for p in args.passes.split(",")]
    all_results = {}

    for pass_name in selected_passes:
        if pass_name not in PASSES:
            print(f"[WARNING] Unknown pass '{pass_name}', skipping", file=sys.stderr)
            continue

        pass_info = PASSES[pass_name]
        print(f"\n{'─' * 60}")
        print(f"[PASS] {pass_info['description']} ({pass_name})")
        print(f"{'─' * 60}")

        results = run_pass(client, args.model, video_file, pass_name, pass_info["prompt"])
        all_results[pass_name] = results if isinstance(results, list) else []

    # Step 4: Merge & adjust timestamps
    merged = []
    for pass_name, results in all_results.items():
        merged.extend(results)

    merged = adjust_timestamps(merged, args.trim_start)
    merged = deduplicate(merged)
    merged.sort(key=lambda r: r.get("original_start_seconds", 0))

    # Step 5: Output
    output = {
        "source_video": str(video_path),
        "location": args.location,
        "model": args.model,
        "trim_offset_seconds": args.trim_start,
        "prepared_duration_seconds": prepared_duration,
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "passes": all_results,
        "merged": merged,
        "stats": {
            "total_detections": len(merged),
            "by_pass": {p: len(r) for p, r in all_results.items()},
            "by_clip_type": {},
            "by_pace": {},
            "high_hook_potential": 0,
        },
    }

    # Compute stats
    for r in merged:
        ct = r.get("clip_type", "unknown")
        output["stats"]["by_clip_type"][ct] = output["stats"]["by_clip_type"].get(ct, 0) + 1
        pace = r.get("pace", "unknown")
        output["stats"]["by_pace"][pace] = output["stats"]["by_pace"].get(pace, 0) + 1
        if r.get("hook_potential", 0) >= 0.7:
            output["stats"]["high_hook_potential"] += 1

    # Save JSON
    out_path = args.output
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n[OUTPUT] Results saved to {out_path}")

    # Print summary
    print_summary(merged, all_results)

    # Cleanup
    try:
        client.files.delete(name=video_file.name)
        print(f"[CLEANUP] Deleted uploaded file from Gemini")
    except Exception as e:
        print(f"[CLEANUP] Could not delete uploaded file: {e}")

    if not args.keep_temp:
        os.unlink(prepared_path)
        print(f"[CLEANUP] Deleted temp video {prepared_path}")


if __name__ == "__main__":
    main()
