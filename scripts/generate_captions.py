#!/usr/bin/env python3
"""Generate 2-3 word per line caption files from script text.

Usage: python3 generate_captions.py <script.txt> [output.txt]

Splits script text into short caption lines (2-3 words each) with blank
lines between them, suitable for subtitle generation via aeneas.
"""
import re
import sys


BREAK_AFTER_CHARS = {'.', ',', '!', '?', ':', ';'}
BREAK_BEFORE_WORDS = {'Y', 'Pero', 'Porque', 'Pues', 'Con', 'Sin',
                      'Esto', 'Cada', 'Antes', 'Para', 'Así', 'Si',
                      'Hay', 'Cuando', 'Hasta', 'Por', 'Que', 'No',
                      'Lo', 'Un', 'Una', 'En', 'De', 'Es', 'Gente',
                      'Vero,', 'Personas', 'Mirad.', 'Compartidlo.'}
MAX_WORDS = 3

def generate_captions(text: str) -> str:
    # Strip [SECTION: X] markers (new pipeline format)
    text = re.sub(r'\[SECTION:\s*[A-Z_0-9]+\]', '', text)
    # Strip stage directions in parentheses (e.g., "(2-3s pure visual — ...)")
    text = re.sub(r'\([^)]*\)', '', text)
    # Safety net: strip lines that are just section labels (e.g., "HOOK:", "FACT_1:")
    text = re.sub(r'(?m)^\s*[A-Z][A-Z_0-9]*\s*:\s*$', '', text)
    text = text.strip()
    # Collapse all whitespace/newlines into single spaces
    text = re.sub(r'\s+', ' ', text)

    tokens = text.split()
    lines = []
    current = []

    for i, token in enumerate(tokens):
        # Check if this token starts a new phrase (break BEFORE)
        bare = re.sub(r'[¿¡"\'«»]', '', token)
        if current and bare in BREAK_BEFORE_WORDS:
            lines.append(' '.join(current))
            current = []

        current.append(token)

        ends_with_punct = token[-1] in BREAK_AFTER_CHARS if token else False
        ends_with_ellipsis = token.endswith('...')

        should_break = False
        if len(current) >= MAX_WORDS:
            should_break = True
        elif len(current) >= 2 and (ends_with_punct or ends_with_ellipsis):
            should_break = True
        elif len(current) == 1 and ends_with_ellipsis:
            should_break = True

        if should_break:
            lines.append(' '.join(current))
            current = []

    if current:
        if lines and len(current) == 1:
            lines[-1] += ' ' + current[0]
        else:
            lines.append(' '.join(current))

    return '\n\n'.join(lines) + '\n'


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_captions.py <script.txt> [output.txt]", file=sys.stderr)
        sys.exit(1)

    script_path = sys.argv[1]
    with open(script_path, 'r', encoding='utf-8') as f:
        text = f.read()

    result = generate_captions(text)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        import os
        output_path = os.path.join(os.path.dirname(script_path), 'captions.txt')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    line_count = len([l for l in result.strip().split('\n') if l.strip()])
    print(f"Generated: {output_path} ({line_count} caption lines)")


if __name__ == '__main__':
    main()
