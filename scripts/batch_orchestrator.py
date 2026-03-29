#!/usr/bin/env python3
"""Givore Batch Orchestrator — generates a complete variant matrix (batch_plan.json).

Replaces manual reading of 9 pool files + tracking 31 constraints.
Produces a deterministic plan for N variants with one command.

Usage:
    python3 batch_orchestrator.py batch-plan \\
        --mode street-finds \\
        --variant-count 7 \\
        --project-dir /path/to/projects/2026-03-27_slug/ \\
        [--exclude-hooks "MYSTERY,BOLD"] \\
        [--exclude-ctas "DOWNLOAD"] \\
        [--location-filter "benimaclet,trinitat"] \\
        [--seed 42]
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

GIVORE_ROOT = Path("/media/kdabrow/Programy/givore")
SCRIPTS_DIR = GIVORE_ROOT / "scripts"
DB_PATH = SCRIPTS_DIR / "clips.db"

# Structures that skip PROOF TEASE (force to SKIP)
PROOF_TEASE_SKIP_STRUCTURES = {"COLD OPEN", "MICRO", "PSP", "COUNTDOWN"}

# Structures that skip RE-HOOK (set to null)
REHOOK_SKIP_STRUCTURES = {"COLD OPEN", "MICRO", "PSP", "COUNTDOWN"}


# ---------------------------------------------------------------------------
# Step 1: Load rotation constraints from DB via subprocess
# ---------------------------------------------------------------------------

def load_rotation_constraints(last_n: int = 5) -> dict[str, Any]:
    """Call givore_db.py script-rotation-json and parse the result."""
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "givore_db.py"),
        "script-rotation-json",
        "--last", str(last_n),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"WARNING: script-rotation-json failed: {result.stderr.strip()}", file=sys.stderr)
        return {"last_n": 0, "avoid": {}, "recent_clips": [], "recent_clip_names": []}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"WARNING: Failed to parse rotation JSON: {exc}", file=sys.stderr)
        return {"last_n": 0, "avoid": {}, "recent_clips": [], "recent_clip_names": []}


# ---------------------------------------------------------------------------
# Step 2: Load available pools via reference_pools.py (direct import)
# ---------------------------------------------------------------------------

def load_pools() -> dict[str, Any]:
    """Import reference_pools and return all pool data."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    import reference_pools as rp

    # Content formats (batch-compatible only)
    all_formats = rp.get_content_formats()
    batch_formats = [f for f in all_formats if f.get("batch_compatible")]

    return {
        "hooks": [h["name"] for h in rp.get_hook_types()],
        "ctas": [c["name"] for c in rp.get_cta_types()],
        "problems": [p["name"] for p in rp.get_problem_angles()],
        "rehooks": [r["name"] for r in rp.get_rehook_styles()],
        "importance": [i["name"] for i in rp.get_importance_angles()],
        "proof_tease": [p["name"] for p in rp.get_proof_tease_styles()],
        "solutions": [s["name"] for s in rp.get_solution_approaches()],
        "structures": [s["name"] for s in rp.get_structures()],
        "personas": [p["name"] for p in rp.get_personas()],
        "persona_voices": {p["name"]: p["voice"] for p in rp.get_personas()},
        "item_intros": [i["name"] for i in rp.get_item_intro_styles()],
        "compatibility": rp.PERSONA_STRUCTURE_COMPATIBILITY,
        "formats": [f["id"] for f in batch_formats],
        "format_details": {f["id"]: f for f in batch_formats},
    }


# ---------------------------------------------------------------------------
# Step 3: Filter pools by constraints
# ---------------------------------------------------------------------------

# Map from pool key to the rotation constraint field name
_CONSTRAINT_FIELD_MAP: dict[str, str] = {
    "hooks": "hook_type",
    "ctas": "cta_type",
    "problems": "problem_angle",
    "rehooks": "rehook_style",
    "proof_tease": "proof_tease",
    "structures": "structure_type",
    "personas": "persona",
}


def filter_pool(
    pool: list[str],
    avoid_values: list[str],
    extra_excludes: list[str] | None = None,
) -> list[str]:
    """Remove avoided and explicitly excluded values from a pool.

    Matching is case-insensitive to be forgiving with user input.
    """
    avoid_upper = {v.upper() for v in avoid_values}
    if extra_excludes:
        avoid_upper.update(v.strip().upper() for v in extra_excludes if v.strip())
    return [v for v in pool if v.upper() not in avoid_upper]


# ---------------------------------------------------------------------------
# Step 4: Select N unique values per element with cycling
# ---------------------------------------------------------------------------

def select_values(pool: list[str], count: int, rng: random.Random) -> list[str]:
    """Select *count* values from *pool*.

    If pool >= count, use random.sample (all unique).
    If pool < count, use all unique values first, then cycle from the start
    (shuffled to avoid predictable repeats).
    """
    if not pool:
        return ["UNKNOWN"] * count

    if len(pool) >= count:
        return rng.sample(pool, count)

    # Cycle: repeat the pool until we have enough, shuffling each round
    selected: list[str] = []
    while len(selected) < count:
        batch = list(pool)
        rng.shuffle(batch)
        selected.extend(batch)
    return selected[:count]


# ---------------------------------------------------------------------------
# Step 5: Clip selection helpers
# ---------------------------------------------------------------------------

def load_clips_from_db() -> list[dict[str, Any]]:
    """Read clip data directly from SQLite for reliable structured access."""
    if not DB_PATH.exists():
        print(f"WARNING: Database not found at {DB_PATH}", file=sys.stderr)
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT c.id, c.filename, c.duration_seconds, c.style, c.mood,
                  c.is_visual_hook, c.description,
                  GROUP_CONCAT(cs.section, ',') as sections
           FROM clips c
           LEFT JOIN clip_sections cs ON c.id = cs.clip_id
           GROUP BY c.id ORDER BY c.id"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def select_visual_hook_clips(
    clips: list[dict[str, Any]],
    recent_clip_ids: list[int],
    location_filters: list[str],
    count: int,
    rng: random.Random,
) -> list[int]:
    """Select *count* unique visual hook clip IDs, avoiding recent ones."""
    candidates = [
        c for c in clips
        if c["is_visual_hook"]
        and c["id"] not in recent_clip_ids
    ]

    if location_filters:
        candidates = [
            c for c in candidates
            if any(loc in c["filename"].lower() for loc in location_filters)
        ]

    if len(candidates) < count:
        print(
            f"WARNING: Only {len(candidates)} visual hook clips available "
            f"(need {count}). Will use what's available.",
            file=sys.stderr,
        )
        count = min(count, len(candidates))

    if not candidates:
        return []

    selected = rng.sample(candidates, count)
    return [c["id"] for c in selected]


def compute_clip_pools(
    clips: list[dict[str, Any]],
    visual_hook_ids: list[int],
    recent_clip_ids: list[int],
) -> dict[str, list[int]]:
    """Compute body and end clip pools (excluding visual hooks and recent clips)."""
    excluded_ids = set(visual_hook_ids) | set(recent_clip_ids)

    body_pool: list[int] = []
    end_pool: list[int] = []

    for c in clips:
        if c["id"] in excluded_ids:
            continue

        sections = (c.get("sections") or "").lower()
        filename = c["filename"].lower()

        # End clips: filename starts with [end] or sections contain "end"
        if filename.startswith("[end]") or "[end]" in filename or "end" in sections.split(","):
            end_pool.append(c["id"])
        else:
            body_pool.append(c["id"])

    return {"body_pool": sorted(body_pool), "end_pool": sorted(end_pool)}


# ---------------------------------------------------------------------------
# Core planning logic
# ---------------------------------------------------------------------------

def build_batch_plan(
    mode: str,
    variant_count: int,
    project_dir: str,
    exclude_hooks: list[str],
    exclude_ctas: list[str],
    location_filters: list[str],
    seed: int | None = None,
    mixed_formats: bool = True,
    forced_format: str | None = None,
) -> dict[str, Any]:
    """Build the complete batch plan JSON structure."""

    # --- Seed ---
    if seed is None:
        today = datetime.date.today().isoformat()
        seed = int(today.replace("-", ""))
    rng = random.Random(seed)

    # --- Step 1: Rotation constraints ---
    constraints = load_rotation_constraints(last_n=5)
    avoid = constraints.get("avoid", {})
    recent_clip_ids = set(constraints.get("recent_clips", []))

    print(f"Loaded constraints: {constraints.get('last_n', 0)} recent scripts, "
          f"{len(recent_clip_ids)} recent clips to avoid", file=sys.stderr)

    # --- Step 2: Load pools ---
    pools = load_pools()

    # --- Step 3: Filter pools (with relaxation for small pools) ---
    # Per-dimension avoidance windows: structures/personas avoid last 2,
    # everything else avoids last 5. This prevents over-filtering small pools.
    _AVOID_WINDOW: dict[str, int] = {
        "structures": 2,
        "personas": 0,  # Never filter personas — batch needs all 5
        "rehooks": 2,
        "problems": 2,
    }

    filtered: dict[str, list[str]] = {}
    actual_avoided: dict[str, list[str]] = {}  # Track what we actually filtered

    for pool_key, constraint_field in _CONSTRAINT_FIELD_MAP.items():
        avoided_all = avoid.get(constraint_field, [])
        # Use per-dimension window to limit avoidance
        window = _AVOID_WINDOW.get(pool_key, 5)
        avoided = avoided_all[:window] if window > 0 else []
        extra = []
        if pool_key == "hooks":
            extra = exclude_hooks
        elif pool_key == "ctas":
            extra = exclude_ctas
        result = filter_pool(pools[pool_key], avoided, extra)
        # Safety: if filtering is too aggressive, relax to last 2 only
        if len(result) < 3 and len(avoided) > 2:
            avoided = avoided_all[:2]
            result = filter_pool(pools[pool_key], avoided, extra)
        filtered[pool_key] = result
        actual_avoided[constraint_field] = avoided

    # importance, solutions, item_intros: no DB constraint field, pass through
    filtered["importance"] = list(pools["importance"])
    filtered["solutions"] = list(pools["solutions"])
    filtered["item_intros"] = list(pools["item_intros"])

    # Report pool sizes
    for key, pool in filtered.items():
        available = len(pool)
        total = len(pools.get(key, pool))
        if available < variant_count:
            print(
                f"WARNING: Pool '{key}' has {available} values after filtering "
                f"(from {total} total, need {variant_count}). Will cycle values.",
                file=sys.stderr,
            )

    # --- Step 4: Select values per element ---
    hook_selections = select_values(filtered["hooks"], variant_count, rng)
    cta_selections = select_values(filtered["ctas"], variant_count, rng)
    problem_selections = select_values(filtered["problems"], variant_count, rng)
    importance_selections = select_values(filtered["importance"], variant_count, rng)
    solution_selections = select_values(filtered["solutions"], variant_count, rng)
    item_intro_selections = select_values(filtered["item_intros"], variant_count, rng)

    # --- Personas: special handling (5 available -> all 5 + repeat 2) ---
    persona_pool = filtered["personas"]
    if len(persona_pool) >= variant_count:
        persona_selections = rng.sample(persona_pool, variant_count)
    else:
        # Use all unique personas first
        base_personas = list(persona_pool)
        rng.shuffle(base_personas)
        repeats_needed = variant_count - len(base_personas)
        repeat_candidates = list(persona_pool)
        rng.shuffle(repeat_candidates)
        persona_selections = base_personas + repeat_candidates[:repeats_needed]

    # --- Structures: select with persona compatibility in mind ---
    structure_pool = filtered["structures"]
    structure_selections: list[str] = select_values(structure_pool, variant_count, rng)

    # For repeated personas (indices >= len(unique personas)), ensure different structure
    # and check compatibility
    compatibility = pools["compatibility"]
    seen_persona_structure: dict[str, str] = {}  # persona -> first structure assigned

    for i in range(variant_count):
        persona = persona_selections[i]
        structure = structure_selections[i]

        # Check avoid list from compatibility
        persona_avoid = compatibility.get(persona, {}).get("avoid", [])

        if structure in persona_avoid:
            # Try to swap with another variant that doesn't have this conflict
            swapped = False
            for j in range(variant_count):
                if j == i:
                    continue
                other_persona = persona_selections[j]
                other_avoid = compatibility.get(other_persona, {}).get("avoid", [])
                # Can we swap structures without creating new conflicts?
                if (structure_selections[j] not in persona_avoid
                        and structure not in other_avoid):
                    structure_selections[i], structure_selections[j] = (
                        structure_selections[j], structure_selections[i]
                    )
                    swapped = True
                    break
            if not swapped:
                # Pick a non-avoided structure from pool
                valid = [s for s in structure_pool if s not in persona_avoid]
                if valid:
                    structure_selections[i] = rng.choice(valid)

        # Track persona -> structures used for repeat check
        if persona not in seen_persona_structure:
            seen_persona_structure[persona] = [structure_selections[i]]
        else:
            # This persona is repeated — MUST get a DIFFERENT structure
            used_structs = seen_persona_structure[persona]
            persona_avoid = compatibility.get(persona, {}).get("avoid", [])
            if structure_selections[i] in used_structs:
                alternatives = [
                    s for s in structure_pool
                    if s not in used_structs
                    and s not in persona_avoid
                ]
                if alternatives:
                    structure_selections[i] = rng.choice(alternatives)
                else:
                    # Fallback: any structure not yet used by this persona
                    fallback = [s for s in structure_pool if s not in used_structs]
                    if fallback:
                        structure_selections[i] = rng.choice(fallback)
            seen_persona_structure[persona].append(structure_selections[i])

    # --- Proof tease: include 1-2 SKIPs, force SKIP for certain structures ---
    proof_tease_pool = filtered["proof_tease"]
    proof_tease_selections = select_values(proof_tease_pool, variant_count, rng)

    # Count non-forced SKIPs
    skip_count = 0
    target_skips = rng.randint(1, 2)

    for i in range(variant_count):
        struct = structure_selections[i]
        if struct in PROOF_TEASE_SKIP_STRUCTURES:
            proof_tease_selections[i] = "SKIP"
        elif proof_tease_selections[i] == "SKIP":
            skip_count += 1

    # If we need more SKIPs and none were naturally placed
    if skip_count < target_skips:
        # Find candidates: non-forced, non-SKIP indices
        candidates = [
            i for i in range(variant_count)
            if structure_selections[i] not in PROOF_TEASE_SKIP_STRUCTURES
            and proof_tease_selections[i] != "SKIP"
        ]
        rng.shuffle(candidates)
        for idx in candidates[:target_skips - skip_count]:
            proof_tease_selections[idx] = "SKIP"

    # --- Rehook: null for structures that skip it ---
    rehook_selections = select_values(filtered["rehooks"], variant_count, rng)
    for i in range(variant_count):
        if structure_selections[i] in REHOOK_SKIP_STRUCTURES:
            rehook_selections[i] = None

    # --- Content formats ---
    format_pool = pools["formats"]
    format_details = pools["format_details"]
    DEFAULT_FORMAT = "CLASSIC_STREET_FINDS"

    format_selections: list[str] = [""] * variant_count

    if not mixed_formats:
        # All variants use the same format
        v1_format = forced_format if forced_format else DEFAULT_FORMAT
        format_selections = [v1_format] * variant_count
    else:
        # v1 always gets default (or forced)
        v1_format = forced_format if forced_format else DEFAULT_FORMAT
        format_selections[0] = v1_format

        # v2-v7 get diversified formats from batch-compatible pool
        # Remove v1's format to maximize diversity, but allow it back if pool is small
        diversify_pool = [f for f in format_pool if f != v1_format]
        if not diversify_pool:
            diversify_pool = list(format_pool)

        # Select with compatibility filtering
        remaining = variant_count - 1
        if remaining > 0:
            candidates = select_values(diversify_pool, remaining, rng)
            format_selections[1:] = candidates

    # Enforce max-2 rule: no format repeated more than twice in a batch
    format_counts: dict[str, int] = {}
    for i, fmt in enumerate(format_selections):
        format_counts[fmt] = format_counts.get(fmt, 0) + 1
        if format_counts[fmt] > 2:
            # Replace with a less-used format from the pool
            used_twice = {f for f, c in format_counts.items() if c >= 2}
            alternatives = [f for f in format_pool if f not in used_twice]
            if alternatives:
                replacement = rng.choice(alternatives)
                format_selections[i] = replacement
                format_counts[fmt] -= 1
                format_counts[replacement] = format_counts.get(replacement, 0) + 1

    # Validate format-persona compatibility
    for i in range(variant_count):
        fmt_id = format_selections[i]
        fmt_info = format_details.get(fmt_id, {})
        incompatible = fmt_info.get("incompatible_personas", [])
        persona = persona_selections[i]

        if incompatible and persona in incompatible:
            # Try to swap persona with another variant that has no conflict
            swapped = False
            for j in range(variant_count):
                if j == i:
                    continue
                other_persona = persona_selections[j]
                other_fmt_info = format_details.get(format_selections[j], {})
                other_incompatible = other_fmt_info.get("incompatible_personas", [])
                # Can we swap without creating new conflicts?
                if (other_persona not in incompatible
                        and persona not in other_incompatible):
                    persona_selections[i], persona_selections[j] = (
                        persona_selections[j], persona_selections[i]
                    )
                    # Also swap voice settings
                    swapped = True
                    break
            if not swapped:
                print(
                    f"WARNING: v{i+1} format {fmt_id} incompatible with persona "
                    f"{persona}, no swap available",
                    file=sys.stderr,
                )

    # Validate format-structure compatibility
    for i in range(variant_count):
        fmt_id = format_selections[i]
        fmt_info = format_details.get(fmt_id, {})
        compatible_structures = fmt_info.get("compatible_structures", [])
        structure = structure_selections[i]

        # Empty list or ["ALL"] means any structure is fine
        if (compatible_structures
                and compatible_structures != ["ALL"]
                and structure not in compatible_structures):
            # Try to swap structure to a compatible one
            persona = persona_selections[i]
            persona_avoid = compatibility.get(persona, {}).get("avoid", [])
            valid = [
                s for s in compatible_structures
                if s in structure_pool and s not in persona_avoid
            ]
            if valid:
                structure_selections[i] = rng.choice(valid)
            else:
                print(
                    f"WARNING: v{i+1} format {fmt_id} prefers structures "
                    f"{compatible_structures}, but none compatible with "
                    f"persona {persona}",
                    file=sys.stderr,
                )

    # --- Step 5: Visual hook clips ---
    all_clips = load_clips_from_db()
    visual_hook_ids = select_visual_hook_clips(
        all_clips, recent_clip_ids, location_filters, variant_count, rng,
    )

    clip_pools = compute_clip_pools(all_clips, visual_hook_ids, list(recent_clip_ids))

    # --- Step 6: Assemble output ---
    persona_voices = pools["persona_voices"]

    variants: list[dict[str, Any]] = []
    for i in range(variant_count):
        persona = persona_selections[i]
        fmt_id = format_selections[i]
        fmt_info = format_details.get(fmt_id, {})
        variant: dict[str, Any] = {
            "variant": i + 1,
            "hook_type": hook_selections[i],
            "cta_type": cta_selections[i],
            "problem_angle": problem_selections[i],
            "rehook_style": rehook_selections[i],
            "importance_angle": importance_selections[i],
            "proof_tease_style": proof_tease_selections[i],
            "solution_approach": solution_selections[i],
            "item_intro_style": item_intro_selections[i],
            "structure": structure_selections[i],
            "persona": persona,
            "persona_voice_settings": persona_voices.get(persona),
            "visual_hook_clip_id": visual_hook_ids[i] if i < len(visual_hook_ids) else None,
            "content_format": fmt_id,
            "format_length_target": fmt_info.get("length", "45-60s"),
            "format_narration_style": fmt_info.get("narration", "full"),
            "format_script_sections": fmt_info.get("script_sections", []),
            "format_clip_guidance": fmt_info.get("clip_guidance", ""),
            "format_platform_priority": fmt_info.get("platform_priority", []),
        }
        variants.append(variant)

    plan: dict[str, Any] = {
        "mode": mode,
        "date": datetime.date.today().isoformat(),
        "variant_count": variant_count,
        "seed": seed,
        "rotation_constraints": {
            "avoid_hooks": actual_avoided.get("hook_type", []),
            "avoid_ctas": actual_avoided.get("cta_type", []),
            "avoid_problems": actual_avoided.get("problem_angle", []),
            "avoid_rehooks": actual_avoided.get("rehook_style", []),
            "avoid_structures": actual_avoided.get("structure_type", []),
            "avoid_personas": actual_avoided.get("persona", []),
            "avoid_proof_tease": actual_avoided.get("proof_tease", []),
            "recent_clips": sorted(recent_clip_ids),
        },
        "variants": variants,
        "clip_budget": {
            "visual_hooks": visual_hook_ids,
            "body_pool": clip_pools["body_pool"],
            "end_pool": clip_pools["end_pool"],
        },
    }

    return plan


# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------

def print_summary(plan: dict[str, Any]) -> None:
    """Print a human-readable summary to stderr."""
    variants = plan["variants"]
    n = len(variants)

    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"  BATCH PLAN: {plan['mode']} | {n} variants | {plan['date']}", file=sys.stderr)
    print(f"  Seed: {plan['seed']}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

    # Constraints summary
    rc = plan["rotation_constraints"]
    if rc["avoid_hooks"]:
        print(f"  Avoided hooks:    {', '.join(rc['avoid_hooks'])}", file=sys.stderr)
    if rc["avoid_ctas"]:
        print(f"  Avoided CTAs:     {', '.join(rc['avoid_ctas'])}", file=sys.stderr)
    if rc["avoid_structures"]:
        print(f"  Avoided structs:  {', '.join(rc['avoid_structures'])}", file=sys.stderr)
    if rc["avoid_personas"]:
        print(f"  Avoided personas: {', '.join(rc['avoid_personas'])}", file=sys.stderr)
    if rc["recent_clips"]:
        print(f"  Recent clips:     {len(rc['recent_clips'])} IDs excluded", file=sys.stderr)

    print(f"\n  {'V':>2} | {'Hook':<22} | {'CTA':<14} | {'Structure':<11} | {'Persona':<12} | {'Format':<24} | {'Proof Tease':<16} | {'VH Clip':>7}", file=sys.stderr)
    print(f"  {'--':>2} | {'-' * 22} | {'-' * 14} | {'-' * 11} | {'-' * 12} | {'-' * 24} | {'-' * 16} | {'-' * 7}", file=sys.stderr)

    for v in variants:
        rehook = v.get("rehook_style") or "(skipped)"
        vh = str(v["visual_hook_clip_id"]) if v["visual_hook_clip_id"] else "-"
        fmt = v.get("content_format", "CLASSIC_STREET_FINDS")
        print(
            f"  {v['variant']:>2} | {v['hook_type']:<22} | {v['cta_type']:<14} | "
            f"{v['structure']:<11} | {v['persona']:<12} | {fmt:<24} | "
            f"{v['proof_tease_style']:<16} | {vh:>7}",
            file=sys.stderr,
        )

    # Uniqueness checks
    hooks_set = set(v["hook_type"] for v in variants)
    personas_list = [v["persona"] for v in variants]
    persona_set = set(personas_list)
    vh_clips = [v["visual_hook_clip_id"] for v in variants if v["visual_hook_clip_id"]]
    formats_list = [v.get("content_format", "CLASSIC_STREET_FINDS") for v in variants]
    formats_set = set(formats_list)

    print(f"\n  Uniqueness checks:", file=sys.stderr)
    print(f"    Hook types:     {len(hooks_set)}/{n} unique", file=sys.stderr)
    print(f"    Personas:       {len(persona_set)}/{n} unique ({len(persona_set)} distinct)", file=sys.stderr)
    print(f"    Formats:        {len(formats_set)}/{n} unique", file=sys.stderr)
    print(f"    VH clips:       {len(set(vh_clips))}/{len(vh_clips)} unique", file=sys.stderr)

    # Check repeated persona structures
    persona_structs: dict[str, list[str]] = {}
    for v in variants:
        persona_structs.setdefault(v["persona"], []).append(v["structure"])
    for persona, structs in persona_structs.items():
        if len(structs) > 1:
            if len(set(structs)) < len(structs):
                print(f"    WARNING: {persona} repeated with SAME structure: {structs}", file=sys.stderr)
            else:
                print(f"    OK: {persona} repeated with different structures: {structs}", file=sys.stderr)

    clip_budget = plan["clip_budget"]
    print(f"\n  Clip budget:", file=sys.stderr)
    print(f"    Visual hooks:   {len(clip_budget['visual_hooks'])} clips", file=sys.stderr)
    print(f"    Body pool:      {len(clip_budget['body_pool'])} clips", file=sys.stderr)
    print(f"    End pool:       {len(clip_budget['end_pool'])} clips", file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Givore Batch Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    plan_parser = subparsers.add_parser("batch-plan", help="Generate a batch variant plan")
    plan_parser.add_argument("--mode", choices=["street-finds", "trial"], default="street-finds")
    plan_parser.add_argument("--variant-count", type=int, default=7)
    plan_parser.add_argument("--project-dir", required=True, help="Output directory for batch_plan.json")
    plan_parser.add_argument("--exclude-hooks", default="", help="Comma-separated hook types to exclude")
    plan_parser.add_argument("--exclude-ctas", default="", help="Comma-separated CTA types to exclude")
    plan_parser.add_argument("--location-filter", default="", help="Comma-separated location substrings for clip filtering")
    plan_parser.add_argument("--seed", type=int, default=None, help="Random seed (default: date-based)")
    plan_parser.add_argument("--mixed-formats", action="store_true", default=True,
                             help="Enable format diversity across variants (default: on)")
    plan_parser.add_argument("--no-mixed-formats", action="store_false", dest="mixed_formats",
                             help="Force all variants to use the same format")
    plan_parser.add_argument("--format", default=None, metavar="FORMAT_ID",
                             help="Force v1's content format (default: CLASSIC_STREET_FINDS)")

    args = parser.parse_args()

    if args.command != "batch-plan":
        parser.print_help()
        sys.exit(1)

    exclude_hooks = [h.strip() for h in args.exclude_hooks.split(",") if h.strip()]
    exclude_ctas = [c.strip() for c in args.exclude_ctas.split(",") if c.strip()]
    location_filters = [loc.strip().lower() for loc in args.location_filter.split(",") if loc.strip()]

    plan = build_batch_plan(
        mode=args.mode,
        variant_count=args.variant_count,
        project_dir=args.project_dir,
        exclude_hooks=exclude_hooks,
        exclude_ctas=exclude_ctas,
        location_filters=location_filters,
        seed=args.seed,
        mixed_formats=args.mixed_formats,
        forced_format=args.format,
    )

    # Write JSON to file
    project_path = Path(args.project_dir)
    project_path.mkdir(parents=True, exist_ok=True)
    output_path = project_path / "batch_plan.json"
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Print summary to stderr
    print_summary(plan)

    print(f"Plan written to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
