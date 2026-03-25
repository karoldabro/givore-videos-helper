#!/usr/bin/env python3
"""DEPRECATED: SFX placement is now AI-driven.

The AI reads the script, subtitles, and SFX_CATALOG.md Basic Tier (5 sounds),
then places SFX directly in the assembly config JSON. See SFX_GUIDELINES.md.

This script is kept for reference only. Use the Basic Tier approach instead:
  1. Read subtitles for timing
  2. Pick from 5 basic sounds (WHOOSH, DING, CHIME, POP, SWOOSH)
  3. Place 2-4 SFX at narrative moments, volume = 0.03

Old description:
Smart SFX placement for Givore video pipeline.
Reads clip plan (with section labels), subtitles, and SFX library directory,
then deterministically places sound effects based on section boundaries,
subtitle timing, and narrative keywords.
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Keyword maps — Spanish trigger words per SFX category
# ---------------------------------------------------------------------------
KEYWORD_MAP = {
    "tension": [
        "pierden", "acaban", "abandonados", "tiramos", "desperdicio",
        "basura", "problema", "malgastar", "contaminar", "vertedero",
        "nadie", "triste", "tirar", "perder", "acabar", "abandonar",
    ],
    "positive": [
        "givore", "solucion", "publicar", "compartir", "dar",
        "segunda vida", "reutilizar", "aprovechar", "funciona",
        "conectar", "regalar", "solucionar", "resolver",
    ],
    "cta": [
        "seguidme", "descarga", "comenta", "comparte", "enlace",
        "link", "bio", "seguir", "unete", "prueba", "app",
    ],
    "reveal": [
        "mira", "encontrado", "aqui", "increible", "hallazgo",
        "descubierto", "sorpresa", "fijaos", "mirad",
    ],
}

# Volume ranges per category (min, max)
VOLUME = {
    "transition": (0.03, 0.04),
    "reveal":     (0.025, 0.035),
    "tension":    (0.02, 0.03),
    "positive":   (0.025, 0.035),
    "impact":     (0.03, 0.04),
    "cta":        (0.025, 0.035),
    "ambient":    (0.015, 0.02),
}

# Max duration caps per category (seconds)
MAX_DURATION = {
    "transition": 0.7,
    "reveal":     2.6,
    "tension":    2.8,
    "positive":   1.5,
    "impact":     1.1,
    "cta":        0.5,
    "ambient":    3.0,
}

# Filename patterns for pool classification
POOL_PATTERNS = {
    "transition": [r"^Whoosh", r"^Swoosh", r"^Swish"],
    "reveal":     [r"^Reveal", r"^Shimmer", r"^Sparkle", r"^Harp", r"^Ding"],
    "tension":    [r"^Dramatic", r"^Braam", r"^Suspense", r"^Stinger", r"^Heartbeat", r"^Rumble"],
    "positive":   [r"^Celebratory", r"^Alert - Positive", r"^Correct", r"^Chime", r"^Jingle", r"^Chimes - Mel", r"^Chimes - Mus"],
    "impact":     [r"^Impact", r"^Hit", r"^Drop", r"^Drum Hit"],
    "cta":        [r"^Pop", r"^Click", r"^Notification"],
    "ambient":    [r"^Ambient", r"^Bird", r"^Cricket"],
}

# Keywords for energy estimation from filename
HIGH_ENERGY_WORDS = {"fast", "short", "sharp", "crisp", "powerful", "single", "quick", "bright"}
LOW_ENERGY_WORDS = {"slow", "soft", "distant", "gentle", "low", "long", "creepy", "echo"}

# Tone → preferred energy
TONE_ENERGY = {
    "energetic":     "high",
    "provocative":   "high",
    "dramatic":      "high",
    "sarcastic":     "medium",
    "calm":          "low",
    "contemplative": "low",
    "humorous":      "medium",
    "informative":   "medium",
}

MIN_SPACING = 1.5  # seconds between SFX


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_srt(path):
    """Parse SRT file into list of {index, start, end, text}."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\n+", content.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not time_match:
            continue
        g = time_match.groups()
        start = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
        end = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000
        text = " ".join(lines[2:]).strip()
        entries.append({"start": start, "end": end, "text": text})
    return entries


def get_duration_ffprobe(path):
    """Get audio file duration via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=5,
        )
        return float(result.stdout.strip())
    except Exception:
        return 1.0  # fallback


def estimate_energy(filename):
    """Estimate energy level from filename keywords."""
    name_lower = filename.lower()
    words = set(re.split(r"[\s\-_.]+", name_lower))
    high_score = len(words & HIGH_ENERGY_WORDS)
    low_score = len(words & LOW_ENERGY_WORDS)
    if high_score > low_score:
        return "high"
    if low_score > high_score:
        return "low"
    return "medium"


def scan_sfx_library(sfx_dir):
    """Scan directory, classify files into category pools."""
    pools = {cat: [] for cat in POOL_PATTERNS}
    sfx_path = Path(sfx_dir)

    seen_basenames = set()
    for f in sorted(sfx_path.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() not in (".mp3",):
            continue
        # Skip .MP3.mp3 duplicates
        basename = f.name
        if basename.endswith(".MP3.mp3"):
            continue
        if basename in seen_basenames:
            continue
        seen_basenames.add(basename)

        # Classify into pool
        for category, patterns in POOL_PATTERNS.items():
            if any(re.match(pat, basename, re.IGNORECASE) for pat in patterns):
                duration = get_duration_ffprobe(str(f))
                pools[category].append({
                    "filename": basename,
                    "path": str(f.resolve()),
                    "duration": duration,
                    "energy": estimate_energy(basename),
                })
                break

    return pools


def detect_section_boundaries(clips):
    """Find where section labels change in clip plan."""
    boundaries = []
    prev_section = None
    for clip in clips:
        section = clip.get("section", "").upper()
        if prev_section and section != prev_section:
            boundaries.append({
                "from_section": prev_section,
                "to_section": section,
                "time": clip.get("position", 0.0),
            })
        prev_section = section
    return boundaries


def detect_keywords(subtitles, keyword_map):
    """Scan subtitle text for trigger keywords."""
    hits = []
    for sub in subtitles:
        text_lower = sub["text"].lower()
        for category, keywords in keyword_map.items():
            for kw in keywords:
                if kw in text_lower:
                    hits.append({
                        "keyword": kw,
                        "category": category,
                        "time": sub["start"],
                        "end": sub["end"],
                    })
    return hits


def pick_from_pool(pool, tone, excluded_filenames, rng):
    """Pick an SFX from pool, weighted by energy match to tone."""
    preferred_energy = TONE_ENERGY.get(tone, "medium")

    # Filter excluded
    candidates = [s for s in pool if s["filename"] not in excluded_filenames]
    if not candidates:
        candidates = pool  # fallback if all excluded

    if not candidates:
        return None

    # Sort: matching energy first, then random
    def sort_key(s):
        if s["energy"] == preferred_energy:
            return 0
        if preferred_energy == "high" and s["energy"] == "medium":
            return 1
        if preferred_energy == "low" and s["energy"] == "medium":
            return 1
        return 2

    candidates.sort(key=sort_key)

    # Pick randomly from top tier (same sort key as best)
    best_tier = sort_key(candidates[0])
    top = [c for c in candidates if sort_key(c) == best_tier]
    return rng.choice(top)


# ---------------------------------------------------------------------------
# Placement logic
# ---------------------------------------------------------------------------

def find_section_boundary(boundaries, to_sections):
    """Find first boundary targeting one of the given sections."""
    for b in boundaries:
        if any(s in b["to_section"] for s in to_sections):
            return b
    return None


def find_keyword_hit(keyword_hits, category, after_time=0.0, before_time=float("inf")):
    """Find first keyword hit for category within time range."""
    for h in keyword_hits:
        if h["category"] == category and after_time <= h["time"] <= before_time:
            return h
    return None


def place_mandatory(boundaries, keyword_hits, pools, tone, excluded, rng, audio_dur):
    """Place 3 mandatory SFX: transition, reveal, positive."""
    placements = []

    # 1. Transition at first major section boundary
    # Prefer boundaries like HOOK->PROBLEM, HOOK_P1->HOOK_P2, etc.
    boundary = (
        find_section_boundary(boundaries, ["PROBLEM", "HOOK_P2", "PROOF"])
        or (boundaries[0] if boundaries else None)
    )
    if boundary and pools["transition"]:
        sfx = pick_from_pool(pools["transition"], tone, excluded, rng)
        if sfx:
            vol_min, vol_max = VOLUME["transition"]
            placements.append({
                "file": sfx["path"],
                "name": f"transition_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                "position": max(0.0, boundary["time"] - 0.15),
                "duration": min(sfx["duration"], MAX_DURATION["transition"]),
                "volume": round(rng.uniform(vol_min, vol_max), 2),
                "category": "transition",
                "trigger": f"{boundary['from_section']}->{boundary['to_section']}",
            })
            excluded.add(sfx["filename"])

    # 2. Reveal at discovery/bridge moment
    # Look for a bridge-type boundary or reveal keyword
    reveal_boundary = find_section_boundary(boundaries, ["HOOK_P3", "BRIDGE"])
    reveal_kw = find_keyword_hit(keyword_hits, "reveal")
    reveal_time = None
    if reveal_boundary:
        reveal_time = reveal_boundary["time"] + 0.05
    elif reveal_kw:
        reveal_time = reveal_kw["time"] + 0.05
    elif boundaries:
        # Fallback: midpoint of second boundary
        mid_idx = min(1, len(boundaries) - 1)
        reveal_time = boundaries[mid_idx]["time"] + 0.05

    if reveal_time is not None and pools["reveal"]:
        sfx = pick_from_pool(pools["reveal"], tone, excluded, rng)
        if sfx:
            vol_min, vol_max = VOLUME["reveal"]
            placements.append({
                "file": sfx["path"],
                "name": f"reveal_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                "position": min(reveal_time, audio_dur - 1.0),
                "duration": min(sfx["duration"], MAX_DURATION["reveal"]),
                "volume": round(rng.uniform(vol_min, vol_max), 2),
                "category": "reveal",
                "trigger": "bridge_reveal" if reveal_boundary else "keyword_reveal",
            })
            excluded.add(sfx["filename"])

    # 3. Positive at SOLUTION start
    solution_boundary = find_section_boundary(boundaries, ["SOLUTION"])
    positive_kw = find_keyword_hit(keyword_hits, "positive")
    positive_time = None
    if solution_boundary:
        # If a keyword is near the boundary, use keyword time
        if positive_kw and abs(positive_kw["time"] - solution_boundary["time"]) < 3.0:
            positive_time = positive_kw["time"] - 0.1
        else:
            positive_time = solution_boundary["time"]
    elif positive_kw:
        positive_time = positive_kw["time"] - 0.1

    if positive_time is not None and pools["positive"]:
        sfx = pick_from_pool(pools["positive"], tone, excluded, rng)
        if sfx:
            vol_min, vol_max = VOLUME["positive"]
            placements.append({
                "file": sfx["path"],
                "name": f"positive_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                "position": max(0.0, positive_time),
                "duration": min(sfx["duration"], MAX_DURATION["positive"]),
                "volume": round(rng.uniform(vol_min, vol_max), 2),
                "category": "positive",
                "trigger": "solution_start",
            })
            excluded.add(sfx["filename"])

    return placements


def place_optional(boundaries, keyword_hits, pools, tone, excluded, rng, budget, audio_dur, clips=None):
    """Place optional SFX based on tone and triggers found."""
    clips = clips or []
    placements = []
    if budget <= 0:
        return placements

    # Priority 1: Impact at RE-HOOK
    if tone in ("energetic", "dramatic", "provocative", "sarcastic"):
        rehook = find_section_boundary(boundaries, ["REHOOK", "RE-HOOK", "RE_HOOK"])
        if rehook and pools["impact"]:
            sfx = pick_from_pool(pools["impact"], tone, excluded, rng)
            if sfx:
                vol_min, vol_max = VOLUME["impact"]
                placements.append({
                    "file": sfx["path"],
                    "name": f"impact_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                    "position": rehook["time"],
                    "duration": min(sfx["duration"], MAX_DURATION["impact"]),
                    "volume": round(rng.uniform(vol_min, vol_max), 2),
                    "category": "impact",
                    "trigger": "rehook",
                })
                excluded.add(sfx["filename"])
                if len(placements) >= budget:
                    return placements

    # Priority 2: Tension at PROBLEM (keyword must be within PROBLEM section)
    if tone in ("dramatic", "provocative", "sarcastic", "energetic"):
        # Find PROBLEM section time range from boundaries
        problem_start = None
        problem_end = None
        for b in boundaries:
            if "PROBLEM" in b["to_section"]:
                problem_start = b["time"]
            elif problem_start is not None and b["from_section"] and "PROBLEM" in b["from_section"]:
                problem_end = b["time"]
                break
        if problem_start is None:
            # Check if PROBLEM appears in clips directly
            for c in clips:
                if "PROBLEM" in c.get("section", "").upper():
                    problem_start = c.get("position", 0)
                    break
        tension_kw = find_keyword_hit(
            keyword_hits, "tension",
            after_time=problem_start or 0.0,
            before_time=problem_end or audio_dur,
        ) if problem_start else None
        if tension_kw and pools["tension"]:
            sfx = pick_from_pool(pools["tension"], tone, excluded, rng)
            if sfx:
                vol_min, vol_max = VOLUME["tension"]
                placements.append({
                    "file": sfx["path"],
                    "name": f"tension_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                    "position": max(0.0, tension_kw["time"] - 0.4),
                    "duration": min(sfx["duration"], MAX_DURATION["tension"]),
                    "volume": round(rng.uniform(vol_min, vol_max), 2),
                    "category": "tension",
                    "trigger": f"keyword:{tension_kw['keyword']}",
                })
                excluded.add(sfx["filename"])
                if len(placements) >= budget:
                    return placements

    # Priority 3: CTA notification
    cta_kw = find_keyword_hit(keyword_hits, "cta")
    if cta_kw and pools["cta"]:
        sfx = pick_from_pool(pools["cta"], tone, excluded, rng)
        if sfx:
            vol_min, vol_max = VOLUME["cta"]
            placements.append({
                "file": sfx["path"],
                "name": f"cta_{sfx['filename'].split('.')[0].lower().replace(' ', '_')}",
                "position": max(0.0, cta_kw["time"] - 0.05),
                "duration": min(sfx["duration"], MAX_DURATION["cta"]),
                "volume": round(rng.uniform(vol_min, vol_max), 2),
                "category": "cta",
                "trigger": f"keyword:{cta_kw['keyword']}",
            })
            excluded.add(sfx["filename"])

    return placements


def apply_constraints(placements, subtitles, audio_dur):
    """Enforce spacing, subtitle alignment, and boundary constraints."""
    # Sort by position
    placements.sort(key=lambda p: p["position"])

    # Clamp positions to valid range
    for p in placements:
        p["position"] = max(0.0, min(p["position"], audio_dur - 0.3))

    # Enforce minimum spacing — drop lower-priority duplicates
    # Priority: transition > reveal > positive > impact > tension > cta > ambient
    priority = {"transition": 0, "reveal": 1, "positive": 2, "impact": 3,
                "tension": 4, "cta": 5, "ambient": 6}

    # Sort by priority first so higher-priority SFX get placed first
    placements.sort(key=lambda p: priority.get(p["category"], 9))

    filtered = []
    for p in placements:
        too_close = False
        for existing in filtered:
            if abs(p["position"] - existing["position"]) < MIN_SPACING:
                too_close = True
                break
        if not too_close:
            filtered.append(p)

    # Subtitle alignment — shift SFX to nearest subtitle boundary if within 0.5s
    for p in filtered:
        nearest_sub = None
        nearest_dist = float("inf")
        for sub in subtitles:
            dist = abs(sub["start"] - p["position"])
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_sub = sub
        if nearest_sub and 0.1 < nearest_dist <= 0.5:
            # Only shift if it doesn't break spacing
            new_pos = nearest_sub["start"] - 0.1
            if all(abs(new_pos - e["position"]) >= MIN_SPACING for e in filtered if e is not p):
                p["position"] = round(max(0.0, new_pos), 3)

    # Round positions
    for p in filtered:
        p["position"] = round(p["position"], 2)
        p["duration"] = round(p["duration"], 2)

    return filtered


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_plan(placements, audio_dur):
    """Run quality checks, return list of (severity, code, message)."""
    warnings = []
    categories_present = {p["category"] for p in placements}

    # Missing mandatory
    for mandatory in ("transition", "reveal", "positive"):
        if mandatory not in categories_present:
            warnings.append(("ERROR", "MISSING_MANDATORY",
                             f"Mandatory {mandatory} SFX not placed"))

    # Budget
    if len(placements) > 6:
        warnings.append(("ERROR", "BUDGET_EXCEEDED",
                         f"{len(placements)} SFX placed, max 6"))
    if len(placements) < 3:
        warnings.append(("INFO", "BUDGET_UNDER",
                         f"Only {len(placements)} SFX placed, expected 3+"))

    # Overlap check
    sorted_p = sorted(placements, key=lambda p: p["position"])
    for i in range(1, len(sorted_p)):
        gap = sorted_p[i]["position"] - sorted_p[i - 1]["position"]
        if gap < 0.5:
            warnings.append(("ERROR", "SFX_OVERLAP",
                             f"{sorted_p[i-1]['name']} and {sorted_p[i]['name']} "
                             f"overlap ({gap:.2f}s apart)"))

    # Past audio end
    for p in placements:
        if p["position"] > audio_dur - 0.3:
            warnings.append(("ERROR", "SFX_PAST_AUDIO",
                             f"{p['name']} at {p['position']:.1f}s past audio end {audio_dur:.1f}s"))

    # No SFX in first 3s
    if not any(p["position"] < 3.0 for p in placements):
        warnings.append(("WARNING", "NO_SFX_FIRST_3S",
                         "No SFX in first 3 seconds — consider retention hook"))

    # Volume out of range
    for p in placements:
        if p["volume"] < 0.01:
            warnings.append(("WARNING", "VOLUME_TOO_LOW",
                             f"{p['name']} volume {p['volume']} may be inaudible"))
        if p["volume"] > 0.08:
            warnings.append(("WARNING", "VOLUME_TOO_HIGH",
                             f"{p['name']} volume {p['volume']} may fight narration"))

    # Consecutive same category
    for i in range(1, len(sorted_p)):
        if sorted_p[i]["category"] == sorted_p[i - 1]["category"]:
            warnings.append(("WARNING", "CONSECUTIVE_SAME_CATEGORY",
                             f"Two {sorted_p[i]['category']} SFX in sequence"))

    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Smart SFX placement for Givore videos")
    parser.add_argument("--clips", required=True, help="Clip plan JSON (with section labels)")
    parser.add_argument("--srt", required=True, help="Subtitle file (.srt)")
    parser.add_argument("--audio-duration", required=True, type=float, help="Audio duration in seconds")
    parser.add_argument("--sfx-dir", required=True, help="Path to Audio effects/ directory")
    parser.add_argument("--tone", default="energetic", help="Video tone (energetic|dramatic|calm|...)")
    parser.add_argument("--exclude", default="", help="Comma-separated SFX filenames to exclude")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", default=None, help="Output JSON path (default: stdout)")
    parser.add_argument("--force", action="store_true",
                        help="Continue despite validation errors")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    # 1. Build SFX pools
    print("Scanning SFX library...", file=sys.stderr)
    pools = scan_sfx_library(args.sfx_dir)
    for cat, items in pools.items():
        print(f"  {cat}: {len(items)} files", file=sys.stderr)

    # 2. Parse inputs
    with open(args.clips) as f:
        clip_plan = json.load(f)
    clips = clip_plan if isinstance(clip_plan, list) else clip_plan.get("clips", [])

    subtitles = parse_srt(args.srt)
    audio_dur = args.audio_duration

    # 3. Detect boundaries and keywords
    boundaries = detect_section_boundaries(clips)
    keyword_hits = detect_keywords(subtitles, KEYWORD_MAP)

    print(f"\nTimeline: {audio_dur:.1f}s, {len(clips)} clips, "
          f"{len(boundaries)} section boundaries, {len(keyword_hits)} keyword hits",
          file=sys.stderr)

    # 4. Calculate budget
    if audio_dur <= 30:
        budget = 4
    elif audio_dur <= 45:
        budget = 5
    else:
        budget = 6

    # 5. Excluded filenames
    excluded = set()
    if args.exclude:
        excluded = set(args.exclude.split(","))

    # 6. Place mandatory (3)
    mandatory = place_mandatory(boundaries, keyword_hits, pools, args.tone, excluded, rng, audio_dur)
    print(f"\nMandatory SFX: {len(mandatory)}/3", file=sys.stderr)

    # 7. Place optional
    optional_budget = budget - len(mandatory)
    optional = place_optional(boundaries, keyword_hits, pools, args.tone, excluded, rng,
                              optional_budget, audio_dur, clips)
    print(f"Optional SFX: {len(optional)}/{optional_budget}", file=sys.stderr)

    # 8. Combine and apply constraints
    all_placements = mandatory + optional
    all_placements = apply_constraints(all_placements, subtitles, audio_dur)

    # 9. Validate
    warnings = validate_plan(all_placements, audio_dur)
    if warnings:
        print("\nQuality checks:", file=sys.stderr)
        for severity, code, msg in warnings:
            print(f"  [{severity}] {code}: {msg}", file=sys.stderr)

    errors = [w for w in warnings if w[0] == "ERROR"]
    if errors and not args.force:
        print(f"\n{len(errors)} ERROR(s) in SFX plan. Use --force to override.",
              file=sys.stderr)
        sys.exit(1)

    # 10. Output — strip internal fields
    output = []
    for p in all_placements:
        output.append({
            "file": p["file"],
            "name": p["name"],
            "position": p["position"],
            "duration": p["duration"],
            "volume": p["volume"],
        })

    print(f"\nSFX plan: {len(output)} effects", file=sys.stderr)
    for i, s in enumerate(output):
        print(f"  [{i+1}] {s['name']} at {s['position']:.1f}s, "
              f"dur={s['duration']:.1f}s, vol={s['volume']}", file=sys.stderr)

    # Write output
    json_str = json.dumps(output, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"\nWritten to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
