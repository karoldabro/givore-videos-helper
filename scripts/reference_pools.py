#!/usr/bin/env python3
"""Parse Givore markdown reference files into structured data.

Markdown files remain the source of truth (human-editable).
This module parses them on demand and returns structured dicts/lists.

Usage:
    python3 reference_pools.py hooks       # print hook types as JSON
    python3 reference_pools.py personas    # print personas as JSON
    python3 reference_pools.py all         # print all pools as JSON
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

GIVORE_ROOT = Path("/media/kdabrow/Programy/givore")

# ---------------------------------------------------------------------------
# Persona <-> Structure compatibility (hardcoded from SCRIPT_PERSONAS.md)
# ---------------------------------------------------------------------------
PERSONA_STRUCTURE_COMPATIBILITY: dict[str, dict[str, list[str]]] = {
    "OBSERVADOR": {"best": ["COLD OPEN", "LOOP", "CLASSIC"], "avoid": ["COUNTDOWN"]},
    "ENERGETICO": {"best": ["MICRO", "COUNTDOWN", "PSP"], "avoid": ["LOOP"]},
    "VECINA": {"best": ["CLASSIC", "PSP", "COLD OPEN"], "avoid": ["MICRO"]},
    "REPORTERO": {"best": ["PSP", "COUNTDOWN", "COLD OPEN"], "avoid": ["LOOP"]},
    "POETA": {"best": ["LOOP", "COLD OPEN", "MICRO"], "avoid": ["COUNTDOWN"]},
}

# ---------------------------------------------------------------------------
# Module-level cache
# ---------------------------------------------------------------------------
_cache: dict[str, Any] = {}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_md(path: Path) -> str:
    """Read a markdown file, returning empty string if missing."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _extract_field(lines: list[str], prefix: str) -> str | None:
    """Find the first line starting with **prefix** and return its value."""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return None


def _split_sections(
    text: str,
    header_pattern: str,
) -> list[tuple[str, list[str]]]:
    """Split markdown into (header_name, body_lines) by regex on header lines.

    *header_pattern* must contain a named group ``name``.
    """
    regex = re.compile(header_pattern)
    sections: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        m = regex.match(line)
        if m:
            if current_name is not None:
                sections.append((current_name, current_lines))
            current_name = m.group("name").strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        sections.append((current_name, current_lines))

    return sections


# ---------------------------------------------------------------------------
# Public pool functions
# ---------------------------------------------------------------------------

def get_hook_types(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse HOOKS_LIBRARY.md -> list of hook type dicts."""
    key = "hooks"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "HOOKS_LIBRARY.md"
    text = _read_md(path)

    # Headers: ### 1. MYSTERY HOOKS  /  ### 16. TRANSFORMATION PROMISE HOOKS
    pattern = r"^### \d+\.\s+(?P<name>.+)$"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        # Strip trailing "HOOKS" / "HOOK" and parenthetical notes
        clean = re.sub(r"\s+HOOKS?\b.*$", "", name).strip()
        use_when = _extract_field(body, "**Use when:**")
        results.append({"name": clean, "use_when": use_when})

    _cache[key] = results
    return results


def get_cta_types(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse CTA_VARIATIONS.md -> list of CTA type dicts."""
    key = "ctas"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "CTA_VARIATIONS.md"
    text = _read_md(path)

    # Headers: ## 1. ENGAGEMENT CTAs (Comments/Interaction)
    pattern = r"^## \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        goal = _extract_field(body, "**Goal:**")
        results.append({"name": name, "goal": goal})

    _cache[key] = results
    return results


def get_problem_angles(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse PROBLEM_VARIATIONS.md -> list of problem angle dicts."""
    key = "problems"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "PROBLEM_VARIATIONS.md"
    text = _read_md(path)

    # ### 1. SYSTEM-WASTE (Default actual)  ->  name = SYSTEM-WASTE
    pattern = r"^### \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        focus = _extract_field(body, "**Enfoque**:")
        results.append({"name": name, "focus": focus})

    _cache[key] = results
    return results


def get_rehook_styles(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse REHOOK_VARIATIONS.md -> list of rehook style dicts."""
    key = "rehooks"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "REHOOK_VARIATIONS.md"
    text = _read_md(path)

    pattern = r"^### \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        focus = _extract_field(body, "**Enfoque**:")
        results.append({"name": name, "focus": focus})

    _cache[key] = results
    return results


def get_importance_angles(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse IMPORTANCE_VARIATIONS.md -> list of importance angle dicts."""
    key = "importance"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "IMPORTANCE_VARIATIONS.md"
    text = _read_md(path)

    pattern = r"^### \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        focus = _extract_field(body, "**Enfoque**:")
        results.append({"name": name, "focus": focus})

    _cache[key] = results
    return results


def get_proof_tease_styles(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse PROOF_TEASE_VARIATIONS.md -> list of proof tease style dicts."""
    key = "proof_tease"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "PROOF_TEASE_VARIATIONS.md"
    text = _read_md(path)

    pattern = r"^### \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        focus = _extract_field(body, "**Enfoque**:")
        results.append({"name": name, "focus": focus})

    _cache[key] = results
    return results


def get_solution_approaches(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse SOLUTION_VARIATIONS.md -> list of solution approach dicts."""
    key = "solutions"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "SOLUTION_VARIATIONS.md"
    text = _read_md(path)

    # ## 1. SPEED-DEMO
    pattern = r"^## \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, body in sections:
        tone_energy = _extract_field(body, "**Tone/energy:**")
        results.append({"name": name, "tone_energy": tone_energy})

    _cache[key] = results
    return results


def get_structures(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse SCRIPT_STRUCTURES.md -> list of structure dicts with sections and duration."""
    key = "structures"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "SCRIPT_STRUCTURES.md"
    text = _read_md(path)

    # ## 1. CLASSIC  /  ## 6. COUNTDOWN / LIST
    pattern = r"^## \d+\.\s+(?P<name>.+)$"
    sections = _split_sections(text, pattern)

    # Duration lookup from the quick-reference table at end of file
    # Table keys: CLASSIC, COLD OPEN, LOOP, MICRO, PSP, COUNTDOWN
    duration_map: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(.+?)\s*\|.*\|\s*(\d+-\d+s)\s*\|", line)
        if m:
            tkey = m.group(1).strip().upper()
            if tkey and tkey != "STRUCTURE":
                duration_map[tkey] = m.group(2)

    # Map from raw header name to canonical name used downstream
    _structure_canonical: dict[str, str] = {
        "CLASSIC": "CLASSIC",
        "COLD OPEN": "COLD OPEN",
        "LOOP FORMAT": "LOOP",
        "MICRO-NARRATIVE": "MICRO",
        "PSP (Problem-Solution-Proof)": "PSP",
        "COUNTDOWN / LIST": "COUNTDOWN",
    }

    # Map canonical name to table lookup key
    _duration_key: dict[str, str] = {
        "CLASSIC": "CLASSIC",
        "COLD OPEN": "COLD OPEN",
        "LOOP": "LOOP",
        "MICRO": "MICRO",
        "PSP": "PSP",
        "COUNTDOWN": "COUNTDOWN",
    }

    results: list[dict[str, Any]] = []
    for name, body in sections:
        # Extract section order from the code block after **Section order:**
        section_list: list[str] = []
        in_code = False
        for line in body:
            stripped = line.strip()
            if stripped.startswith("```") and in_code:
                break
            if in_code and "-->" in stripped:
                # Parse "HOOK (0-3s) --> PROOF TEASE (3-8s) --> ..."
                parts = re.split(r"\s*-->\s*", stripped)
                for part in parts:
                    sec_name = re.sub(r"\s*\(.*?\)\s*$", "", part).strip()
                    if sec_name:
                        section_list.append(sec_name)
            if stripped.startswith("```") and not in_code:
                in_code = True

        canonical = _structure_canonical.get(name, name.split("/")[0].strip())
        dk = _duration_key.get(canonical, canonical.split()[0].upper())
        duration = duration_map.get(dk)

        results.append({
            "name": canonical,
            "sections": section_list if section_list else None,
            "duration": duration,
        })

    _cache[key] = results
    return results


def get_personas(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse SCRIPT_PERSONAS.md -> list of persona dicts with voice settings."""
    key = "personas"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "SCRIPT_PERSONAS.md"
    text = _read_md(path)

    # Parse voice settings table first
    # | OBSERVADOR | 0.98 | 0.40 | 0.45 | 0.35 | ... |
    voice_map: dict[str, dict[str, float]] = {}
    for line in text.splitlines():
        m = re.match(
            r"^\|\s*(\w+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|",
            line,
        )
        if m and m.group(1) not in ("Persona", "---"):
            voice_map[m.group(1).upper()] = {
                "speed": float(m.group(2)),
                "stability": float(m.group(3)),
                "similarity_boost": float(m.group(4)),
                "style": float(m.group(5)),
            }

    # Parse persona sections: ## 1. EL OBSERVADOR -> name "OBSERVADOR"
    pattern = r"^## \d+\.\s+(?:EL\s+|LA\s+)?(?P<name>.+)$"
    sections = _split_sections(text, pattern)

    results: list[dict[str, Any]] = []
    for name, _body in sections:
        # "OBSERVADOR" / "ENERGETICO" / "VECINA CURIOSA" / "REPORTERO" / "POETA URBANO"
        canonical = name.split()[0].upper()
        voice = voice_map.get(canonical)
        results.append({"name": canonical, "voice": voice})

    _cache[key] = results
    return results


def get_item_intro_styles(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse PHRASE_VARIATIONS.md Section 9 -> list of item intro style dicts."""
    key = "item_intros"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "PHRASE_VARIATIONS.md"
    text = _read_md(path)

    # Only look at content after "## 9. Item Introduction Styles"
    marker = "## 9. Item Introduction Styles"
    idx = text.find(marker)
    if idx == -1:
        _cache[key] = []
        return []

    section_text = text[idx:]

    # ### 1. FACTUAL  ...  ### 8. EMOTIONAL
    pattern = r"^### \d+\.\s+(?P<name>\S+)"
    sections = _split_sections(section_text, pattern)

    results: list[dict[str, Any]] = []
    for name, _body in sections:
        results.append({"name": name})

    _cache[key] = results
    return results


def get_content_formats(md_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Parse CONTENT_FORMATS.md -> list of content format dicts with all fields."""
    key = "formats"
    if key in _cache:
        return _cache[key]

    path = Path(md_path) if md_path else GIVORE_ROOT / "CONTENT_FORMATS.md"
    text = _read_md(path)

    # Headers: ### FORMAT 1: EL_RANKING_CALLEJERO
    pattern = r"^### FORMAT \d+:\s+(?P<name>\S+)\s*$"
    sections = _split_sections(text, pattern)

    # Field mapping: markdown label prefix -> dict key
    _field_map: list[tuple[str, str]] = [
        ("- **Name**:", "display_name"),
        ("- **Length**:", "length"),
        ("- **Narration**:", "narration"),
        ("- **Batch compatible**:", "batch_compatible"),
        ("- **Script sections**:", "script_sections"),
        ("- **Compatible structures**:", "compatible_structures"),
        ("- **Compatible personas**:", "compatible_personas"),
        ("- **Incompatible personas**:", "incompatible_personas"),
        ("- **Clip guidance**:", "clip_guidance"),
        ("- **Content pillar**:", "content_pillar"),
        ("- **Platform priority**:", "platform_priority"),
        ("- **Viral potential**:", "viral_potential"),
        ("- **Series**:", "series"),
        ("- **Hook template**:", "hook_template"),
        ("- **CTA approach**:", "cta_approach"),
        ("- **Algorithm signal**:", "algorithm_signal"),
    ]

    results: list[dict[str, Any]] = []
    for format_id, body in sections:
        entry: dict[str, Any] = {"id": format_id}

        for prefix, dict_key in _field_map:
            value = _extract_field(body, prefix)
            if value is None:
                entry[dict_key] = None
                continue

            # Boolean fields
            if dict_key in ("batch_compatible", "series"):
                entry[dict_key] = value.lower() in ("yes", "true")
            # List fields (comma-separated)
            elif dict_key in (
                "script_sections",
                "compatible_structures",
                "compatible_personas",
                "incompatible_personas",
                "content_pillar",
                "platform_priority",
            ):
                if value.lower() in ("none", "all"):
                    entry[dict_key] = value.upper()
                else:
                    entry[dict_key] = [
                        v.strip() for v in value.split(",") if v.strip()
                    ]
            else:
                entry[dict_key] = value

        results.append(entry)

    _cache[key] = results
    return results


# ---------------------------------------------------------------------------
# Pool registry for CLI
# ---------------------------------------------------------------------------

POOLS: dict[str, Any] = {
    "hooks": get_hook_types,
    "ctas": get_cta_types,
    "problems": get_problem_angles,
    "rehooks": get_rehook_styles,
    "importance": get_importance_angles,
    "proof_tease": get_proof_tease_styles,
    "solutions": get_solution_approaches,
    "structures": get_structures,
    "personas": get_personas,
    "item_intros": get_item_intro_styles,
    "formats": get_content_formats,
    "compatibility": lambda: PERSONA_STRUCTURE_COMPATIBILITY,
}


def get_all() -> dict[str, Any]:
    """Return all pools as a single dict."""
    return {name: fn() for name, fn in POOLS.items()}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <pool_name|all>")
        print(f"Available pools: {', '.join(POOLS.keys())}, all")
        sys.exit(1)

    pool_name = sys.argv[1].lower()

    if pool_name == "all":
        data = get_all()
    elif pool_name in POOLS:
        data = POOLS[pool_name]()
    else:
        print(f"Unknown pool: {pool_name}", file=sys.stderr)
        print(f"Available: {', '.join(POOLS.keys())}, all", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
