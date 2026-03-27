#!/usr/bin/env python3
"""Automated quality validation for Givore video scripts.

Runs 8 checks on a script file, each returning PASS/WARN/FAIL.
Compares against previous scripts for repetition and uniqueness.

Usage:
    python3 quality_check.py <script.txt> [--last-scripts <paths...>] [--batch-manifest <path>]

Exit codes: 0=all PASS, 1=has WARNs, 2=has FAILs
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Check 2: Marketing red flags
MARKETING_RED_FLAGS = [
    "te conecta",
    "nuestra plataforma",
    "descarga ahora",
    "segunda vida a objetos que merecen",
    "con nuestra plataforma",
    "descubre cómo",
    "únete a la comunidad",
    "forma parte de",
    "no te lo pierdas",
    "haz click",
    "haz clic",
    "suscríbete ya",
    "aprovecha ahora",
    "oferta exclusiva",
    "solución perfecta",
    "la mejor app",
    "increíble oportunidad",
    "transforma tu vida",
    "cambia el mundo",
    "revolucionario",
    "innovador sistema",
]

# Authentic voice markers (regex patterns)
AUTHENTIC_MARKERS = [
    r"\.\.\.",                    # Ellipsis / incomplete sentences
    r"—",                         # Self-interruptions (em-dash)
    r"\beh\b",                    # Casual aside "eh"
    r"\bmadre mía\b",             # Genuine reaction
    r"\bjoder\b",                 # Genuine reaction
    r"\btío\b",                   # Casual address
    r"\btía\b",                   # Casual address
    r"\bflipa\b",                 # Genuine surprise
    r"\bmola\b",                  # Casual approval
    r"\bmirad\b",                 # Direct address
    r"\ba ver\b",                 # Casual aside
    r"\bbueno\b",                 # Filler
    r"\bpues\b",                  # Filler
    r"\bvenga\b",                 # Casual
    r"\bostras\b",                # Surprise
    r"\bala\b",                   # Surprise (interjection)
    r"\bno sé\b",                 # Uncertainty marker
    r"¿no\?",                     # Tag question
    r"¿verdad\?",                 # Tag question
    r"\ben plan\b",               # Casual filler
    r"¿sabes\?",                  # Casual tag
]

# Check 7: Trash encouragement phrases
TRASH_ENCOURAGEMENT = [
    "recógelo",
    "recogelo",
    "llévatelo",
    "llevatelo",
    "rescátalo",
    "rescatalo",
    "coge esto",
    "cógelo",
    "cogelo",
    "no lo dejes ahí",
    "no lo dejes ahi",
    "llévalo a casa",
    "llevalo a casa",
    "llévatelo a casa",
    "llevatelo a casa",
    "hazte con",
    "quédatelo",
    "quedatelo",
    "recoge esto",
    "sal a buscar",
    "ve a buscarlo",
    "pilla esto",
    "píllalo",
    "pillalo",
]

# Check 8: Treasure-hunting language
TREASURE_HUNTING = [
    "tesoro",
    "hallazgo increíble",
    "hallazgo increible",
    "me lo llevo",
    "qué suerte",
    "que suerte",
    "qué hallazgo",
    "que hallazgo",
    "mi botín",
    "mi botin",
    "mira lo que encontré",
    "mira lo que encontre",
    "vaya joya",
    "pedazo de hallazgo",
]

# Check 8: Giveaway-first framing phrases
GIVEAWAY_PHRASES = [
    "si alguien lo hubiera dado",
    "esto no tendría que estar aquí",
    "esto no tendria que estar aqui",
    "se hubieran compartido",
    "se hubiera compartido",
    "alguien podría usarlo",
    "alguien podria usarlo",
    "si alguien lo necesita",
    "esto sigue aquí",
    "esto sigue aqui",
    "no tendría que acabar así",
    "no tendria que acabar asi",
    "si el dueño hubiera sabido",
    "si el dueno hubiera sabido",
    "antes de tirarlo",
    "en vez de tirarlo",
    "podría haberse dado",
    "podria haberse dado",
    "podría haberse compartido",
    "podria haberse compartido",
]

# Script section markers
SECTION_MARKERS = [
    "HOOK", "GANCHO",
    "PROBLEM", "PROBLEMA",
    "IMPORTANCE", "IMPORTANCIA",
    "RE-HOOK", "REHOOK", "RE HOOK",
    "SOLUTION", "SOLUCIÓN", "SOLUCION",
    "PAYOFF", "RECOMPENSA",
    "CTA",
]


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize Spanish text for comparison: lowercase, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def strip_accents(text: str) -> str:
    """Remove accents for fuzzy matching while keeping ñ."""
    result = []
    for ch in text:
        if ch == 'ñ' or ch == 'Ñ':
            result.append(ch)
            continue
        nfkd = unicodedata.normalize('NFKD', ch)
        result.append(''.join(c for c in nfkd if not unicodedata.combining(c)))
    return ''.join(result)


def extract_words(text: str) -> List[str]:
    """Extract words from text, stripping punctuation."""
    text = normalize_text(text)
    # Remove punctuation except hyphens within words
    text = re.sub(r'[¿¡"\'«»()…]', '', text)
    text = re.sub(r'[.,!?;:]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split()


def extract_ngrams(text: str, n: int) -> List[str]:
    """Extract n-grams (phrases of n words) from text."""
    words = extract_words(text)
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def word_overlap_ratio(text_a: str, text_b: str) -> float:
    """Calculate word overlap ratio between two texts (Jaccard-like)."""
    words_a = set(extract_words(text_a))
    words_b = set(extract_words(text_b))
    if not words_a or not words_b:
        return 0.0
    # Remove very common Spanish stop words for meaningful comparison
    stop_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'en', 'y', 'a', 'que', 'es', 'por', 'con',
        'para', 'se', 'lo', 'no', 'al', 'su', 'este', 'esta',
        'esto', 'más', 'mas', 'pero', 'o', 'como', 'si', 'ya',
        'te', 'me', 'le', 'nos', 'os', 'les',
    }
    words_a -= stop_words
    words_b -= stop_words
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 0.0


def get_first_sentence(text: str) -> str:
    """Extract the first sentence from script text (skipping section headers)."""
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip section headers (lines that are all caps or start with ## etc)
        if re.match(r'^[\s]*(?:#{1,3}\s|HOOK|GANCHO|PROBLEMA|PROBLEM|SECTION|---)', line, re.IGNORECASE):
            continue
        # Skip lines that look like metadata (key: value)
        if re.match(r'^[A-Za-záéíóúñÁÉÍÓÚÑ\s]+:', line) and len(line) < 60:
            continue
        return line
    return ""


def get_last_sentences(text: str, n: int = 2) -> str:
    """Extract last n non-empty content sentences from script text."""
    lines = text.strip().split('\n')
    content_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[\s]*(?:#{1,3}\s|---)', line):
            continue
        if re.match(r'^[A-Za-záéíóúñÁÉÍÓÚÑ\s]+:', line) and len(line) < 60:
            continue
        content_lines.append(line)
    return ' '.join(content_lines[-n:]) if content_lines else ""


def parse_sections(text: str) -> dict:
    """Parse script into sections, returning word counts per section."""
    sections = {}
    current_section = "PREAMBLE"
    current_words = []

    for line in text.split('\n'):
        line_stripped = line.strip().upper()
        matched = False
        for marker in SECTION_MARKERS:
            if marker in line_stripped and len(line_stripped) < 40:
                # Save previous section
                if current_words:
                    sections[current_section] = len(current_words)
                current_section = marker
                current_words = []
                matched = True
                break
        if not matched:
            current_words.extend(extract_words(line))

    if current_words:
        sections[current_section] = len(current_words)

    return sections


def read_file_safe(path: str) -> str:
    """Read file contents, return empty string on error."""
    try:
        return Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        print(f"WARNING: Could not read {path}: {e}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_phrase_repetition(script: str, last_scripts: List[str]) -> Tuple[str, str]:
    """Check 1: Extract 3+ word phrases and compare against last scripts."""
    if not last_scripts:
        return "PASS", "0 repeated phrases (no previous scripts to compare)"

    # Extract 3-grams, 4-grams, 5-grams from current script
    current_phrases = set()
    for n in range(3, 6):
        current_phrases.update(extract_ngrams(script, n))

    # Extract same from previous scripts
    prev_phrases = set()
    for prev in last_scripts:
        for n in range(3, 6):
            prev_phrases.update(extract_ngrams(prev, n))

    repeated = current_phrases & prev_phrases
    # Filter out very common Spanish phrases
    common_filler = {
        'y no es', 'lo que es', 'que no se', 'en la calle',
        'hay que ver', 'no sé qué', 'es que no', 'y es que',
    }
    repeated -= common_filler

    count = len(repeated)
    examples = sorted(repeated)[:5]
    detail = f"{count} repeated phrase{'s' if count != 1 else ''}"
    if examples:
        detail += ": " + ", ".join(f'"{p}"' for p in examples)

    if count == 0:
        return "PASS", detail
    elif count <= 2:
        return "WARN", detail
    else:
        return "FAIL", detail


def check_marketing_tone(script: str) -> Tuple[str, str, List[str]]:
    """Check 2: Scan for marketing red flags and verify authentic markers."""
    text_lower = normalize_text(script)
    text_no_accents = strip_accents(text_lower)

    # Find red flags
    found_flags = []
    for flag in MARKETING_RED_FLAGS:
        flag_lower = flag.lower()
        flag_no_accents = strip_accents(flag_lower)
        if flag_lower in text_lower or flag_no_accents in text_no_accents:
            found_flags.append(flag)

    # Count authentic markers
    marker_count = 0
    for pattern in AUTHENTIC_MARKERS:
        if re.search(pattern, script, re.IGNORECASE):
            marker_count += 1

    action_items = []
    flag_count = len(found_flags)

    if flag_count == 0 and marker_count >= 2:
        status = "PASS"
        detail = f"0 red flags, {marker_count} authentic markers"
    elif flag_count == 0 and marker_count < 2:
        status = "WARN"
        detail = f"0 red flags but only {marker_count} authentic marker{'s' if marker_count != 1 else ''} (need 2+)"
        action_items.append("Add more authentic voice markers (ellipsis, self-interruptions, casual asides)")
    elif flag_count <= 2:
        status = "WARN"
        detail = f"{flag_count} red flag{'s' if flag_count != 1 else ''}: " + ", ".join(f'"{f}"' for f in found_flags)
        for f in found_flags:
            action_items.append(f'Replace "{f}" with authentic phrasing')
    else:
        status = "FAIL"
        detail = f"{flag_count} red flags: " + ", ".join(f'"{f}"' for f in found_flags)
        for f in found_flags:
            action_items.append(f'Replace "{f}" with authentic phrasing')

    return status, detail, action_items


def check_hook_uniqueness(script: str, last_scripts: List[str]) -> Tuple[str, str]:
    """Check 3: Compare first sentence against last scripts' first sentences."""
    if not last_scripts:
        return "PASS", "no previous scripts to compare"

    current_hook = get_first_sentence(script)
    if not current_hook:
        return "WARN", "could not extract hook sentence"

    max_overlap = 0.0
    for prev in last_scripts:
        prev_hook = get_first_sentence(prev)
        if prev_hook:
            overlap = word_overlap_ratio(current_hook, prev_hook)
            max_overlap = max(max_overlap, overlap)

    pct = int(max_overlap * 100)
    detail = f"{pct}% overlap with previous hooks"

    if max_overlap < 0.30:
        return "PASS", detail
    elif max_overlap <= 0.50:
        return "WARN", detail
    else:
        return "FAIL", detail


def check_cta_freshness(script: str, last_scripts: List[str]) -> Tuple[str, str]:
    """Check 4: Compare last 2 sentences against last scripts' CTAs."""
    if not last_scripts:
        return "PASS", "no previous scripts to compare"

    current_cta = get_last_sentences(script, 2)
    if not current_cta:
        return "WARN", "could not extract CTA sentences"

    max_overlap = 0.0
    for prev in last_scripts:
        prev_cta = get_last_sentences(prev, 2)
        if prev_cta:
            overlap = word_overlap_ratio(current_cta, prev_cta)
            max_overlap = max(max_overlap, overlap)

    pct = int(max_overlap * 100)
    detail = f"{pct}% overlap with previous CTAs"

    if max_overlap < 0.30:
        return "PASS", detail
    elif max_overlap <= 0.50:
        return "WARN", detail
    else:
        return "FAIL", detail


def check_structure_variety(script: str, last_scripts: List[str]) -> Tuple[str, str]:
    """Check 5: Compare section word-count proportions against last 3 scripts."""
    if not last_scripts:
        return "PASS", "no previous scripts to compare"

    current_sections = parse_sections(script)
    if not current_sections:
        return "WARN", "could not parse sections"

    # Calculate proportions for current script
    total = sum(current_sections.values())
    if total == 0:
        return "WARN", "script appears empty"

    current_proportions = {k: v / total for k, v in current_sections.items()}

    # Compare against last 3
    comparison_scripts = last_scripts[:3]
    structural_diffs = 0

    for prev in comparison_scripts:
        prev_sections = parse_sections(prev)
        prev_total = sum(prev_sections.values())
        if prev_total == 0:
            structural_diffs += 1
            continue

        prev_proportions = {k: v / prev_total for k, v in prev_sections.items()}

        # Count significant proportion differences (>15%)
        all_keys = set(list(current_proportions.keys()) + list(prev_proportions.keys()))
        diff_count = 0
        for key in all_keys:
            curr_val = current_proportions.get(key, 0)
            prev_val = prev_proportions.get(key, 0)
            if abs(curr_val - prev_val) > 0.15:
                diff_count += 1

        # Also count section presence/absence differences
        curr_keys = set(current_sections.keys()) - {"PREAMBLE"}
        prev_keys = set(prev_sections.keys()) - {"PREAMBLE"}
        section_diff = len(curr_keys.symmetric_difference(prev_keys))

        if diff_count + section_diff > 0:
            structural_diffs += 1

    detail = f"{structural_diffs} structural difference{'s' if structural_diffs != 1 else ''} vs last {len(comparison_scripts)}"

    if structural_diffs >= 2:
        return "PASS", detail
    elif structural_diffs >= 1:
        return "WARN", detail
    else:
        return "FAIL", detail + " (script structure too similar)"


def check_clip_diversity(manifest_path: Optional[str]) -> Tuple[str, str, List[str]]:
    """Check 6: Parse clip usage from batch manifest and check reuse limits."""
    if not manifest_path:
        return "N/A", "no manifest provided", []

    manifest_text = read_file_safe(manifest_path)
    if not manifest_text:
        return "N/A", f"could not read manifest: {manifest_path}", []

    # Try JSON format first
    clip_usage = {}  # clip_id -> list of variants
    action_items = []

    try:
        manifest = json.loads(manifest_text)
        # Handle JSON manifest with clip usage data
        if isinstance(manifest, dict) and "clip_usage" in manifest:
            clip_usage = manifest["clip_usage"]
    except (json.JSONDecodeError, KeyError):
        # Parse markdown CLIP_USAGE table
        in_table = False
        for line in manifest_text.split('\n'):
            if 'CLIP_USAGE' in line.upper() or 'clip' in line.lower() and '|' in line:
                in_table = True
                continue
            if in_table and '|' in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2 and not parts[0].startswith('-'):
                    clip_id = parts[0]
                    variants = [v.strip() for v in parts[1].split(',') if v.strip()]
                    if clip_id and variants and not clip_id.lower().startswith('clip'):
                        clip_usage[clip_id] = variants
            elif in_table and line.strip() == '':
                in_table = False

    if not clip_usage:
        return "N/A", "no clip usage data found in manifest", []

    # Check limits: hooks=1, body=3, bridge=4
    violations = []
    for clip_id, variants in clip_usage.items():
        count = len(variants) if isinstance(variants, list) else variants
        clip_lower = clip_id.lower()

        if '[hook]' in clip_lower or 'hook' in clip_lower:
            if count > 1:
                violations.append(f"Hook clip {clip_id} used in {count} variants (max 1)")
        elif '[bridge]' in clip_lower or 'bridge' in clip_lower:
            if count > 4:
                violations.append(f"Bridge clip {clip_id} used in {count} variants (max 4)")
        else:
            if count > 3:
                violations.append(f"Body clip {clip_id} used in {count} variants (max 3)")

    if not violations:
        return "PASS", f"{len(clip_usage)} clips tracked, all within limits", []
    else:
        action_items = violations
        if len(violations) <= 2:
            return "WARN", f"{len(violations)} clip reuse violation{'s' if len(violations) != 1 else ''}", action_items
        else:
            return "FAIL", f"{len(violations)} clip reuse violations", action_items


def check_trash_encouragement(script: str) -> Tuple[str, str, List[str]]:
    """Check 7: Scan for phrases that encourage taking things from the street."""
    text_lower = normalize_text(script)
    text_no_accents = strip_accents(text_lower)

    found = []
    for phrase in TRASH_ENCOURAGEMENT:
        phrase_lower = phrase.lower()
        phrase_no_accents = strip_accents(phrase_lower)
        if phrase_lower in text_lower or phrase_no_accents in text_no_accents:
            found.append(phrase)

    action_items = []
    if not found:
        return "PASS", "no matches", action_items
    else:
        detail = f"{len(found)} match{'es' if len(found) != 1 else ''}: " + ", ".join(f'"{f}"' for f in found)
        for f in found:
            action_items.append(
                f'Remove "{f}" — Givore connects people, it does not instruct to scavenge'
            )
        return "FAIL", detail, action_items


def check_giveaway_framing(script: str) -> Tuple[str, str, List[str]]:
    """Check 8: Verify giveaway-first framing, flag treasure-hunting language."""
    text_lower = normalize_text(script)
    text_no_accents = strip_accents(text_lower)

    # Check for treasure-hunting language
    treasure_found = []
    for phrase in TREASURE_HUNTING:
        phrase_lower = phrase.lower()
        phrase_no_accents = strip_accents(phrase_lower)
        if phrase_lower in text_lower or phrase_no_accents in text_no_accents:
            treasure_found.append(phrase)

    # Check for giveaway-first framing
    giveaway_count = 0
    for phrase in GIVEAWAY_PHRASES:
        phrase_lower = phrase.lower()
        phrase_no_accents = strip_accents(phrase_lower)
        if phrase_lower in text_lower or phrase_no_accents in text_no_accents:
            giveaway_count += 1

    action_items = []

    if treasure_found:
        detail = f"treasure-hunting language: " + ", ".join(f'"{t}"' for t in treasure_found)
        for t in treasure_found:
            action_items.append(
                f'Replace "{t}" with giveaway-first framing '
                '(e.g., "esto no tendria que estar aqui")'
            )
        return "FAIL", detail, action_items

    if giveaway_count == 0:
        return "WARN", "no giveaway-first framing phrases found", [
            "Add at least 1 giveaway-first phrase (e.g., "
            '"si alguien lo hubiera dado", "esto no tendria que estar aqui")'
        ]

    return "PASS", f"{giveaway_count} giveaway phrase{'s' if giveaway_count != 1 else ''} found", []


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def find_line_number(script: str, phrase: str) -> Optional[int]:
    """Find the line number where a phrase appears in the script."""
    phrase_lower = phrase.lower()
    phrase_no_accents = strip_accents(phrase_lower)
    for i, line in enumerate(script.split('\n'), 1):
        line_lower = line.lower()
        if phrase_lower in line_lower or phrase_no_accents in strip_accents(line_lower):
            return i
    return None


def run_quality_check(
    script_path: str,
    last_script_paths: List[str],
    batch_manifest_path: Optional[str],
) -> int:
    """Run all 8 checks and print report. Returns exit code."""
    script = read_file_safe(script_path)
    if not script:
        print(f"ERROR: Could not read script file: {script_path}", file=sys.stderr)
        return 2

    last_scripts = [read_file_safe(p) for p in last_script_paths]
    last_scripts = [s for s in last_scripts if s]  # filter empty

    # Run all checks
    results = []
    all_action_items = []

    # 1. Phrase Repetition
    status, detail = check_phrase_repetition(script, last_scripts)
    results.append(("Phrase Repetition", status, detail))

    # 2. Marketing Tone
    status, detail, items = check_marketing_tone(script)
    results.append(("Marketing Tone", status, detail))
    for item in items:
        # Try to find line number for flagged phrases
        # Extract the quoted phrase from the action item
        match = re.search(r'"([^"]+)"', item)
        if match:
            line_no = find_line_number(script, match.group(1))
            if line_no:
                all_action_items.append(f"Line {line_no}: {item}")
            else:
                all_action_items.append(item)
        else:
            all_action_items.append(item)

    # 3. Hook Uniqueness
    status, detail = check_hook_uniqueness(script, last_scripts)
    results.append(("Hook Uniqueness", status, detail))

    # 4. CTA Freshness
    status, detail = check_cta_freshness(script, last_scripts)
    results.append(("CTA Freshness", status, detail))

    # 5. Structure Variety
    status, detail = check_structure_variety(script, last_scripts)
    results.append(("Structure Variety", status, detail))

    # 6. Clip Diversity
    status, detail, items = check_clip_diversity(batch_manifest_path)
    results.append(("Clip Diversity", status, detail))
    all_action_items.extend(items)

    # 7. Trash Encouragement
    status, detail, items = check_trash_encouragement(script)
    results.append(("Trash Encouragement", status, detail))
    for item in items:
        match = re.search(r'"([^"]+)"', item)
        if match:
            line_no = find_line_number(script, match.group(1))
            if line_no:
                all_action_items.append(f"Line {line_no}: {item}")
            else:
                all_action_items.append(item)
        else:
            all_action_items.append(item)

    # 8. Giveaway-First Framing
    status, detail, items = check_giveaway_framing(script)
    results.append(("Giveaway-First", status, detail))
    for item in items:
        match = re.search(r'"([^"]+)"', item)
        if match:
            line_no = find_line_number(script, match.group(1))
            if line_no:
                all_action_items.append(f"Line {line_no}: {item}")
            else:
                all_action_items.append(item)
        else:
            all_action_items.append(item)

    # Print report
    warn_count = sum(1 for _, s, _ in results if s == "WARN")
    fail_count = sum(1 for _, s, _ in results if s == "FAIL")

    print("QUALITY REPORT")
    print("==============")
    for name, status, detail in results:
        print(f"{name + ':':23s} {status} ({detail})")

    print()
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    print(f"Overall: {overall} ({warn_count} warning{'s' if warn_count != 1 else ''}, "
          f"{fail_count} failure{'s' if fail_count != 1 else ''})")

    if all_action_items:
        print("Action items:")
        for item in all_action_items:
            print(f"  - {item}")

    # Exit code
    if fail_count > 0:
        return 2
    elif warn_count > 0:
        return 1
    else:
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Automated quality validation for Givore video scripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit codes:
  0  All checks PASS
  1  Has WARNings (no failures)
  2  Has FAILures

Examples:
  python3 quality_check.py script.txt
  python3 quality_check.py script.txt --last-scripts prev1.txt prev2.txt
  python3 quality_check.py script.txt --batch-manifest BATCH_MANIFEST.md
        """,
    )
    parser.add_argument(
        "script",
        help="Path to the script text file to validate",
    )
    parser.add_argument(
        "--last-scripts",
        nargs="+",
        default=[],
        metavar="PATH",
        help="Paths to the last N script files for comparison (up to 5 recommended)",
    )
    parser.add_argument(
        "--batch-manifest",
        default=None,
        metavar="PATH",
        help="Path to BATCH_MANIFEST.md for clip diversity check",
    )

    args = parser.parse_args()

    # Validate script file exists
    if not Path(args.script).is_file():
        print(f"ERROR: Script file not found: {args.script}", file=sys.stderr)
        sys.exit(2)

    # Validate last-scripts exist
    for p in args.last_scripts:
        if not Path(p).is_file():
            print(f"WARNING: Previous script not found, skipping: {p}", file=sys.stderr)

    valid_last = [p for p in args.last_scripts if Path(p).is_file()]

    exit_code = run_quality_check(args.script, valid_last, args.batch_manifest)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
