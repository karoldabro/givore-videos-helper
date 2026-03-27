#!/usr/bin/env python3
"""Automated quality validation for Givore video scripts.

Runs 8 checks on a script file, each returning PASS/WARN/FAIL.
Compares against previous scripts for repetition and uniqueness.

Usage:
    python3 quality_check.py <script.txt> [--last-scripts <paths...>] [--batch-manifest <path>]
    python3 quality_check.py --batch-dir <project-dir>
    python3 quality_check.py --validate-plan <batch_plan.json>

Exit codes: 0=all PASS, 1=has WARNs, 2=has FAILs
"""
import argparse
import glob as glob_mod
import json
import re
import sys
import unicodedata
from itertools import combinations
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


# ---------------------------------------------------------------------------
# Batch diversity checking (cross-variant within a batch)
# ---------------------------------------------------------------------------

def discover_batch_scripts(batch_dir: str) -> dict:
    """Find all v*/[slug].txt scripts in a batch directory. Returns {variant: text}."""
    batch_path = Path(batch_dir)
    scripts = {}
    for v_dir in sorted(batch_path.iterdir()):
        if not v_dir.is_dir() or not re.match(r'^v\d+$', v_dir.name):
            continue
        txt_files = list(v_dir.glob("*.txt"))
        # Find the script (not captions.txt, not clip_map.txt, not descriptions.txt)
        for tf in txt_files:
            if tf.name in ('captions.txt', 'clip_map.txt', 'descriptions.txt'):
                continue
            text = read_file_safe(str(tf))
            if text:
                scripts[v_dir.name] = text
                break
    return scripts


def extract_sentences(text: str, min_words: int = 5) -> List[str]:
    """Extract content sentences from a script (min_words+ words, no headers)."""
    sentences = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[\s]*(?:#{1,3}\s|HOOK|GANCHO|PROBLEMA|PROBLEM|SECTION|---)', line, re.IGNORECASE):
            continue
        words = extract_words(line)
        if len(words) >= min_words:
            sentences.append(normalize_text(line))
    return sentences


def check_batch_diversity(scripts: dict) -> tuple:
    """Check diversity across all batch variants.

    Returns (overall_status, report_lines, action_items).
    """
    variant_names = sorted(scripts.keys())
    n = len(variant_names)
    if n < 2:
        return "PASS", ["Only 1 variant — no cross-variant comparison needed."], []

    report = []
    action_items = []
    worst_status = "PASS"

    # --- 1. Pairwise word overlap ---
    overlaps = {}
    worst_pair = ("", "", 0.0)
    for va, vb in combinations(variant_names, 2):
        ratio = word_overlap_ratio(scripts[va], scripts[vb])
        overlaps[f"{va}-{vb}"] = ratio
        if ratio > worst_pair[2]:
            worst_pair = (va, vb, ratio)

    avg_overlap = sum(overlaps.values()) / len(overlaps) if overlaps else 0
    report.append("Pairwise word overlap:")
    # Show in rows of 4
    items = list(overlaps.items())
    for i in range(0, len(items), 4):
        chunk = items[i:i+4]
        line = "  " + "  ".join(f"{k}: {v:.0%}" for k, v in chunk)
        report.append(line)
    report.append(f"  Worst pair: {worst_pair[0]}-{worst_pair[1]} ({worst_pair[2]:.0%})")
    report.append(f"  Average overlap: {avg_overlap:.0%}")

    if worst_pair[2] > 0.60:
        worst_status = "FAIL"
        action_items.append(f"Regenerate {worst_pair[1]} — {worst_pair[2]:.0%} overlap with {worst_pair[0]}")
    elif worst_pair[2] > 0.40:
        if worst_status != "FAIL":
            worst_status = "WARN"
        action_items.append(f"High overlap: {worst_pair[0]}-{worst_pair[1]} ({worst_pair[2]:.0%})")

    # --- 2. Shared n-gram detection (4-grams in 3+ variants) ---
    report.append("")
    ngram_counts = {}  # {ngram: [variants]}
    for vname, text in scripts.items():
        for ng in set(extract_ngrams(text, 4)):  # unique per variant
            ngram_counts.setdefault(ng, []).append(vname)

    shared_ngrams = {ng: vs for ng, vs in ngram_counts.items() if len(vs) >= 3}
    # Sort by frequency desc
    shared_sorted = sorted(shared_ngrams.items(), key=lambda x: -len(x[1]))[:10]

    if shared_sorted:
        report.append(f"Shared phrases (4+ words in 3+ variants): {len(shared_ngrams)}")
        for ng, vs in shared_sorted[:5]:
            report.append(f'  "{ng}" ({",".join(vs)})')
    else:
        report.append("Shared phrases (4+ words in 3+ variants): 0")

    if len(shared_ngrams) >= 5:
        if worst_status != "FAIL":
            worst_status = "FAIL" if len(shared_ngrams) >= 8 else "WARN"
        action_items.append(f"{len(shared_ngrams)} phrases repeated in 3+ variants — rewrite with different vocabulary")
    elif len(shared_ngrams) >= 3:
        if worst_status == "PASS":
            worst_status = "WARN"
        action_items.append(f"{len(shared_ngrams)} shared phrases across variants")

    # --- 3. Identical sentence detection ---
    report.append("")
    sentence_map = {}  # {normalized_sentence: [variants]}
    for vname, text in scripts.items():
        for sent in extract_sentences(text, min_words=5):
            stripped = strip_accents(sent)
            sentence_map.setdefault(stripped, []).append(vname)

    identical = {s: vs for s, vs in sentence_map.items() if len(vs) >= 2}
    identical_sorted = sorted(identical.items(), key=lambda x: -len(x[1]))[:5]

    report.append(f"Identical sentences (5+ words, 2+ variants): {len(identical)}")
    for sent, vs in identical_sorted[:3]:
        display = sent[:60] + "..." if len(sent) > 60 else sent
        report.append(f'  "{display}" ({",".join(vs)})')

    if len(identical) >= 3:
        if worst_status != "FAIL":
            worst_status = "FAIL" if len(identical) >= 5 else "WARN"
        action_items.append(f"{len(identical)} identical sentences across variants — rewrite each uniquely")

    # --- 4. Overall batch diversity score ---
    report.append("")
    diversity = 1.0 - avg_overlap  # Simple: inverse of average overlap
    diversity_pct = diversity * 100
    report.append(f"Overall batch diversity: {diversity_pct:.0f}%")

    if diversity_pct < 60:
        worst_status = "FAIL"
        action_items.append(f"Batch diversity {diversity_pct:.0f}% below 60% threshold")
    elif diversity_pct < 70:
        if worst_status == "PASS":
            worst_status = "WARN"
        action_items.append(f"Batch diversity {diversity_pct:.0f}% below 70% target")

    return worst_status, report, action_items


def run_batch_check(batch_dir: str) -> int:
    """Run batch diversity check on all variant scripts in a directory."""
    scripts = discover_batch_scripts(batch_dir)

    if not scripts:
        print(f"ERROR: No variant scripts found in {batch_dir}", file=sys.stderr)
        return 2

    print("BATCH DIVERSITY REPORT")
    print("======================")
    print(f"Variants analyzed: {len(scripts)} ({', '.join(sorted(scripts.keys()))})")
    print()

    status, report, action_items = check_batch_diversity(scripts)

    for line in report:
        print(line)

    print()
    print(f"Overall: {status}")

    if action_items:
        print("\nAction items:")
        for item in action_items:
            print(f"  - {item}")

    # Also run individual checks on each variant (using others as last-scripts)
    print("\n" + "=" * 50)
    print("PER-VARIANT CHECKS")
    print("=" * 50)

    variant_names = sorted(scripts.keys())
    per_variant_worst = "PASS"

    for vname in variant_names:
        # Find the actual script path
        v_dir = Path(batch_dir) / vname
        txt_files = [f for f in v_dir.glob("*.txt")
                     if f.name not in ('captions.txt', 'clip_map.txt', 'descriptions.txt')]
        if not txt_files:
            continue

        script_path = str(txt_files[0])
        # Use other variants as "last scripts" for comparison
        other_scripts = [str(Path(batch_dir) / ov / txt_files[0].name)
                         for ov in variant_names if ov != vname]
        other_scripts = [p for p in other_scripts if Path(p).is_file()]

        print(f"\n--- {vname} ---")
        exit_code = run_quality_check(script_path, other_scripts, None)

        if exit_code == 2:
            per_variant_worst = "FAIL"
        elif exit_code == 1 and per_variant_worst != "FAIL":
            per_variant_worst = "WARN"

    # Final verdict
    if status == "FAIL" or per_variant_worst == "FAIL":
        return 2
    elif status == "WARN" or per_variant_worst == "WARN":
        return 1
    return 0


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
# Plan validation
# ---------------------------------------------------------------------------

ALL_PERSONAS = {"OBSERVADOR", "ENERGETICO", "VECINA", "REPORTERO", "POETA"}

PERSONA_STRUCTURE_AVOID = {
    "OBSERVADOR": {"COUNTDOWN"},
    "ENERGETICO": {"LOOP"},
    "VECINA": {"MICRO"},
    "REPORTERO": {"LOOP"},
    "POETA": {"COUNTDOWN"},
}

# Structures where proof_tease should be SKIP/null and rehook should be null
NO_PROOF_TEASE_STRUCTURES = {"COLD OPEN", "MICRO", "PSP", "COUNTDOWN"}
NO_REHOOK_STRUCTURES = {"COLD OPEN", "MICRO", "PSP", "COUNTDOWN"}


def validate_plan(plan_path: str) -> int:
    """Validate a batch_plan.json for constraint compliance.

    Returns exit code: 0=all PASS, 1=has WARNs, 2=has FAILs.
    """
    try:
        with open(plan_path, encoding="utf-8") as f:
            plan = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not read plan: {e}", file=sys.stderr)
        return 2

    variants = plan.get("variants", [])
    constraints = plan.get("rotation_constraints", {})
    n = len(variants)

    if n == 0:
        print("ERROR: No variants found in plan.", file=sys.stderr)
        return 2

    results = []  # (name, status, detail)
    warn_count = 0
    fail_count = 0

    def record(name: str, status: str, detail: str):
        nonlocal warn_count, fail_count
        results.append((name, status, detail))
        if status == "WARN":
            warn_count += 1
        elif status == "FAIL":
            fail_count += 1

    # --- 1. Hook uniqueness ---
    hooks = [v.get("hook_type") for v in variants]
    unique_hooks = len(set(hooks))
    if unique_hooks == n:
        record("Hook uniqueness", "PASS", f"{unique_hooks}/{n} unique")
    else:
        dupes = [h for h in set(hooks) if hooks.count(h) > 1]
        # WARN if pool was too small (cycling expected), FAIL otherwise
        avoid_count = len(constraints.get("avoid_hooks", []))
        available = 16 - avoid_count  # 16 known hook types
        severity = "WARN" if available < n else "FAIL"
        record("Hook uniqueness", severity,
               f"{unique_hooks}/{n} unique — duplicates: {', '.join(dupes)}"
               + (f" (pool={available}, cycling expected)" if severity == "WARN" else ""))

    # --- 2. CTA uniqueness ---
    ctas = [v.get("cta_type") for v in variants]
    unique_ctas = len(set(ctas))
    if unique_ctas == n:
        record("CTA uniqueness", "PASS", f"{unique_ctas}/{n} unique")
    else:
        dupes = [c for c in set(ctas) if ctas.count(c) > 1]
        avoid_count = len(constraints.get("avoid_ctas", []))
        available = 9 - avoid_count  # 9 known CTA categories
        severity = "WARN" if available < n else "FAIL"
        record("CTA uniqueness", severity,
               f"{unique_ctas}/{n} unique — duplicates: {', '.join(dupes)}"
               + (f" (pool={available}, cycling expected)" if severity == "WARN" else ""))

    # --- 3. Visual hook clip uniqueness (NO exceptions) ---
    clip_ids = [v.get("visual_hook_clip_id") for v in variants]
    unique_clips = len(set(clip_ids))
    if unique_clips == n:
        record("Visual hook uniqueness", "PASS", f"{unique_clips}/{n} unique")
    else:
        dupes = [str(c) for c in set(clip_ids) if clip_ids.count(c) > 1]
        record("Visual hook uniqueness", "FAIL",
               f"{unique_clips}/{n} unique — duplicates: {', '.join(dupes)}")

    # --- 4. Persona coverage ---
    used_personas = {v.get("persona") for v in variants}
    missing = ALL_PERSONAS - used_personas
    if not missing:
        record("Persona coverage", "PASS",
               f"{len(ALL_PERSONAS)}/{len(ALL_PERSONAS)} personas used")
    else:
        record("Persona coverage", "FAIL",
               f"{len(used_personas)}/{len(ALL_PERSONAS)} — missing: {', '.join(sorted(missing))}")

    # --- 5. Persona+structure avoidance ---
    avoid_violations = []
    for v in variants:
        persona = v.get("persona", "")
        structure = v.get("structure", "")
        avoid_set = PERSONA_STRUCTURE_AVOID.get(persona, set())
        if structure in avoid_set:
            avoid_violations.append(f"v{v.get('variant')}: {persona}+{structure}")
    if not avoid_violations:
        record("Persona+structure compat", "PASS", "no conflicts")
    else:
        record("Persona+structure compat", "FAIL",
               f"{len(avoid_violations)} conflict(s): {'; '.join(avoid_violations)}")

    # --- 6. Persona repeat structures ---
    persona_structures = {}  # {persona: [(variant, structure), ...]}
    for v in variants:
        persona = v.get("persona", "")
        structure = v.get("structure", "")
        persona_structures.setdefault(persona, []).append(
            (v.get("variant"), structure))
    repeat_violations = []
    for persona, entries in persona_structures.items():
        if len(entries) < 2:
            continue
        structures = [s for _, s in entries]
        if len(structures) != len(set(structures)):
            duped = [s for s in set(structures) if structures.count(s) > 1]
            vids = [str(vid) for vid, s in entries if s in duped]
            repeat_violations.append(
                f"{persona} repeats {', '.join(duped)} in v{', v'.join(vids)}")
    if not repeat_violations:
        record("Persona repeat structures", "PASS",
               "all repeats have different structures")
    else:
        record("Persona repeat structures", "FAIL",
               "; ".join(repeat_violations))

    # --- 7. Proof tease + structure ---
    proof_violations = []
    for v in variants:
        structure = v.get("structure", "")
        proof = v.get("proof_tease_style")
        if structure in NO_PROOF_TEASE_STRUCTURES:
            if proof is not None and proof != "SKIP":
                proof_violations.append(
                    f"v{v.get('variant')}: {structure} has proof_tease={proof}")
    if not proof_violations:
        record("Proof tease + structure", "PASS",
               "SKIPs aligned with structures")
    else:
        record("Proof tease + structure", "FAIL",
               "; ".join(proof_violations))

    # --- 8. Rehook + structure ---
    rehook_violations = []
    for v in variants:
        structure = v.get("structure", "")
        rehook = v.get("rehook_style")
        if structure in NO_REHOOK_STRUCTURES:
            if rehook is not None:
                rehook_violations.append(
                    f"v{v.get('variant')}: {structure} has rehook={rehook}")
    if not rehook_violations:
        record("Rehook + structure", "PASS",
               "nulls aligned with structures")
    else:
        record("Rehook + structure", "FAIL",
               "; ".join(rehook_violations))

    # --- 9. Constraint compliance ---
    constraint_map = {
        "hook_type": "avoid_hooks",
        "cta_type": "avoid_ctas",
        "problem_angle": "avoid_problems",
        "rehook_style": "avoid_rehooks",
        "structure": "avoid_structures",
        "persona": "avoid_personas",
    }
    constraint_violations = []
    for v in variants:
        vid = v.get("variant", "?")
        for field, avoid_key in constraint_map.items():
            avoid_list = constraints.get(avoid_key, [])
            value = v.get(field)
            if value and value in avoid_list:
                constraint_violations.append(
                    f"v{vid}: {field}={value} is in {avoid_key}")
    if not constraint_violations:
        record("Constraint compliance", "PASS", "no avoided values used")
    else:
        record("Constraint compliance", "FAIL",
               f"{len(constraint_violations)} violation(s): "
               + "; ".join(constraint_violations))

    # --- Print report ---
    plan_name = Path(plan_path).name
    print(f"PLAN VALIDATION: {plan_name}")
    print("=" * (18 + len(plan_name)))
    for name, status, detail in results:
        print(f"{name + ':':30s} {status} ({detail})")

    print()
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    print(f"Overall: {overall} ({warn_count} warning{'s' if warn_count != 1 else ''}, "
          f"{fail_count} failure{'s' if fail_count != 1 else ''})")

    if fail_count > 0:
        return 2
    elif warn_count > 0:
        return 1
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
  python3 quality_check.py --batch-dir projects/2026-03-27_topic/
  python3 quality_check.py --validate-plan batch_plan.json
        """,
    )
    parser.add_argument(
        "script",
        nargs="?",
        default=None,
        help="Path to the script text file to validate (not needed with --batch-dir)",
    )
    parser.add_argument(
        "--batch-dir",
        default=None,
        metavar="PATH",
        help="Path to batch project directory for cross-variant diversity check",
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
    parser.add_argument(
        "--validate-plan",
        default=None,
        metavar="PATH",
        help="Path to batch_plan.json for pre-script constraint validation",
    )

    args = parser.parse_args()

    # Plan validation mode: validate batch_plan.json and exit
    if args.validate_plan:
        if not Path(args.validate_plan).is_file():
            print(f"ERROR: Plan file not found: {args.validate_plan}", file=sys.stderr)
            sys.exit(2)
        exit_code = validate_plan(args.validate_plan)
        sys.exit(exit_code)

    # Batch-dir mode: cross-variant diversity check
    if args.batch_dir:
        if not Path(args.batch_dir).is_dir():
            print(f"ERROR: Batch directory not found: {args.batch_dir}", file=sys.stderr)
            sys.exit(2)
        exit_code = run_batch_check(args.batch_dir)
        sys.exit(exit_code)

    # Single-script mode (original behavior)
    if not args.script:
        print("ERROR: Either <script> or --batch-dir is required.", file=sys.stderr)
        parser.print_usage(sys.stderr)
        sys.exit(2)

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
