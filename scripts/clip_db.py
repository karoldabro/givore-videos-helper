#!/usr/bin/env python3
"""Givore Clip Database — SQLite repository for video clip metadata.

Replaces manual CLIPS_CATALOG.md with accurate ffprobe-based durations
and queryable metadata for the video assembly pipeline.

Usage:
    clip_db.py init                              Import clips from filesystem + catalog
    clip_db.py list [--section X] [--style X] [--mood X] [--visual-hooks]
    clip_db.py search <section>                  Shortcut for list --section
    clip_db.py info <id>                         Full details for one clip
    clip_db.py add <file> [--section X,Y] [--style X] [--mood X] [--desc "..."]
    clip_db.py update <id> [--section X,Y] [--style X] [--mood X] [--desc "..."]
    clip_db.py delete <id>                       Remove clip from DB
    clip_db.py refresh                           Re-scan all files, update durations
    clip_db.py sync                              Find orphan files / missing DB entries
    clip_db.py plan <audio_file> <id1,id2,...>   Compare clips vs audio duration
    clip_db.py export                            Regenerate CLIPS_CATALOG.md from DB
"""

import argparse
import glob
import os
import re
import sqlite3
import subprocess
import sys

GIVORE_ROOT = "/media/kdabrow/Programy/givore"
CLIPS_DIR = os.path.join(GIVORE_ROOT, "videos", "clips")
VISUAL_HOOKS_DIR = os.path.join(CLIPS_DIR, "visual hooks")
CATALOG_PATH = os.path.join(CLIPS_DIR, "CLIPS_CATALOG.md")
DB_PATH = os.path.join(GIVORE_ROOT, "scripts", "clips.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS clips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    duration_seconds REAL NOT NULL,
    style TEXT,
    mood TEXT,
    description TEXT,
    is_visual_hook INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS clip_sections (
    clip_id INTEGER NOT NULL,
    section TEXT NOT NULL,
    PRIMARY KEY (clip_id, section),
    FOREIGN KEY (clip_id) REFERENCES clips(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_clip_sections_section ON clip_sections(section);
CREATE INDEX IF NOT EXISTS idx_clips_style ON clips(style);
CREATE INDEX IF NOT EXISTS idx_clips_mood ON clips(mood);
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def get_duration(filepath):
    """Get media duration in seconds via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", filepath],
            capture_output=True, text=True, timeout=10
        )
        return float(result.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired):
        return 0.0


def parse_catalog(catalog_path):
    """Parse CLIPS_CATALOG.md into list of dicts."""
    entries = []
    if not os.path.isfile(catalog_path):
        return entries

    with open(catalog_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_visual_hooks = False
    for line in lines:
        line = line.strip()
        if line.startswith("## Visual Hooks"):
            in_visual_hooks = True
            continue
        if not line.startswith("|") or line.startswith("| Filename") or line.startswith("|---"):
            continue

        parts = [p.strip() for p in line.split("|")]
        # Split produces empty strings at start/end due to leading/trailing |
        parts = [p for p in parts if p]
        if len(parts) < 6:
            continue

        filename_raw = parts[0]
        duration_str = parts[1]
        sections_str = parts[2]
        style = parts[3]
        mood = parts[4]
        description = parts[5] if len(parts) > 5 else ""

        # Strip 'visual hooks/' prefix if present
        filename = filename_raw
        if filename.startswith("visual hooks/"):
            filename = filename[len("visual hooks/"):]

        # Parse duration
        dur_match = re.search(r"([\d.]+)", duration_str)
        catalog_duration = float(dur_match.group(1)) if dur_match else 0.0

        # Parse sections
        sections = [s.strip() for s in sections_str.split(",") if s.strip()]

        entries.append({
            "filename": filename,
            "catalog_duration": catalog_duration,
            "sections": sections,
            "style": style,
            "mood": mood,
            "description": description,
            "catalog_visual_hook": in_visual_hooks,
        })

    return entries


def discover_files():
    """Find all .mp4 files in clips directories. Returns {basename: abspath}."""
    files = {}
    for f in glob.glob(os.path.join(CLIPS_DIR, "*.mp4")):
        files[os.path.basename(f)] = os.path.abspath(f)
    for f in glob.glob(os.path.join(VISUAL_HOOKS_DIR, "*.mp4")):
        files[os.path.basename(f)] = os.path.abspath(f)
    return files


def insert_clip(conn, path, filename, duration, style, mood, description, is_vh, sections):
    """Insert a clip and its sections into the DB."""
    cur = conn.execute(
        "INSERT INTO clips (filename, path, duration_seconds, style, mood, description, is_visual_hook) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (filename, path, duration, style, mood, description, 1 if is_vh else 0)
    )
    clip_id = cur.lastrowid
    for sec in sections:
        conn.execute(
            "INSERT OR IGNORE INTO clip_sections (clip_id, section) VALUES (?, ?)",
            (clip_id, sec)
        )
    return clip_id


# --- Commands ---

def cmd_init(args):
    """Scan clips dirs, import catalog metadata, populate DB with real durations."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing DB: {DB_PATH}")

    conn = create_db()
    files = discover_files()
    catalog = parse_catalog(CATALOG_PATH)

    # Build catalog lookup by filename
    catalog_by_name = {}
    for entry in catalog:
        catalog_by_name[entry["filename"]] = entry

    matched = 0
    unmatched_catalog = 0
    new_files = 0
    duration_fixes = 0
    matched_filenames = set()

    # Match catalog entries to files
    for entry in catalog:
        fname = entry["filename"]
        if fname in files:
            real_path = files[fname]
            real_duration = get_duration(real_path)
            is_vh = "visual hooks" in real_path
            insert_clip(conn, real_path, fname, real_duration,
                        entry["style"], entry["mood"], entry["description"],
                        is_vh, entry["sections"])
            matched += 1
            matched_filenames.add(fname)

            diff = abs(real_duration - entry["catalog_duration"])
            if diff > 0.3:
                print(f"  DURATION FIX: {fname}: catalog={entry['catalog_duration']}s, actual={real_duration:.2f}s")
                duration_fixes += 1
        else:
            print(f"  WARNING: Catalog entry has no file: {fname}")
            unmatched_catalog += 1

    # Add files not in catalog
    for basename, path in sorted(files.items()):
        if basename not in matched_filenames:
            real_duration = get_duration(path)
            is_vh = "visual hooks" in path
            insert_clip(conn, path, basename, real_duration,
                        None, None, None, is_vh, [])
            new_files += 1
            print(f"  NEW (no catalog metadata): {basename} ({real_duration:.2f}s)")

    conn.commit()
    conn.close()

    total = matched + new_files
    print(f"\nInit complete: {total} clips imported")
    print(f"  Matched from catalog: {matched}")
    print(f"  New (uncataloged): {new_files}")
    print(f"  Duration corrections: {duration_fixes}")
    if unmatched_catalog:
        print(f"  Catalog entries without files: {unmatched_catalog}")
    print(f"DB: {DB_PATH}")


def cmd_list(args):
    """List clips with optional filters."""
    conn = get_db()

    query = """
        SELECT c.id, c.filename, c.duration_seconds, c.style, c.mood,
               c.is_visual_hook, c.description,
               GROUP_CONCAT(cs.section, ',') as sections
        FROM clips c
        LEFT JOIN clip_sections cs ON c.id = cs.clip_id
    """
    conditions = []
    params = []

    if args.section:
        conditions.append("c.id IN (SELECT clip_id FROM clip_sections WHERE section = ?)")
        params.append(args.section)
    if args.style:
        conditions.append("c.style = ?")
        params.append(args.style)
    if args.mood:
        conditions.append("c.mood = ?")
        params.append(args.mood)
    if args.visual_hooks:
        conditions.append("c.is_visual_hook = 1")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY c.id ORDER BY c.id"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        print("No clips found matching filters.")
        return

    print(f"{'ID':>4} | {'Dur':>6} | {'Sections':<20} | {'Style':<14} | {'Mood':<14} | {'Filename'}")
    print(f"{'----':>4} | {'------':>6} | {'--------------------':<20} | {'--------------':<14} | {'--------------':<14} | {'--------'}")
    for r in rows:
        sections = r["sections"] or "-"
        style = r["style"] or "-"
        mood = r["mood"] or "-"
        vh = " [VH]" if r["is_visual_hook"] else ""
        print(f"{r['id']:>4} | {r['duration_seconds']:>5.2f}s | {sections:<20} | {style:<14} | {mood:<14} | {r['filename']}{vh}")

    print(f"\n{len(rows)} clip(s)")


def cmd_search(args):
    """Shortcut for list --section."""
    args.style = None
    args.mood = None
    args.visual_hooks = False
    cmd_list(args)


def cmd_info(args):
    """Show full details for one clip."""
    conn = get_db()
    row = conn.execute("SELECT * FROM clips WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Clip ID {args.id} not found.")
        conn.close()
        return

    sections = conn.execute(
        "SELECT section FROM clip_sections WHERE clip_id = ? ORDER BY section",
        (args.id,)
    ).fetchall()
    conn.close()

    print(f"ID:          {row['id']}")
    print(f"Filename:    {row['filename']}")
    print(f"Path:        {row['path']}")
    print(f"Duration:    {row['duration_seconds']:.2f}s")
    print(f"Sections:    {', '.join(s['section'] for s in sections) or '-'}")
    print(f"Style:       {row['style'] or '-'}")
    print(f"Mood:        {row['mood'] or '-'}")
    print(f"Description: {row['description'] or '-'}")
    print(f"Visual Hook: {'Yes' if row['is_visual_hook'] else 'No'}")
    print(f"Created:     {row['created_at']}")


def cmd_add(args):
    """Add a new clip with auto-detected duration."""
    filepath = os.path.abspath(args.file)
    if not os.path.isfile(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    conn = get_db()
    existing = conn.execute("SELECT id FROM clips WHERE path = ?", (filepath,)).fetchone()
    if existing:
        print(f"ERROR: File already in DB as clip ID {existing['id']}")
        conn.close()
        sys.exit(1)

    duration = get_duration(filepath)
    is_vh = "visual hooks" in filepath
    sections = [s.strip() for s in args.section.split(",")] if args.section else []

    clip_id = insert_clip(conn, filepath, os.path.basename(filepath), duration,
                          args.style, args.mood, args.desc, is_vh, sections)
    conn.commit()
    conn.close()

    print(f"Added clip ID {clip_id}: {os.path.basename(filepath)} ({duration:.2f}s)")


def cmd_update(args):
    """Update clip metadata."""
    conn = get_db()
    row = conn.execute("SELECT * FROM clips WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Clip ID {args.id} not found.")
        conn.close()
        return

    updates = []
    params = []
    if args.style is not None:
        updates.append("style = ?")
        params.append(args.style)
    if args.mood is not None:
        updates.append("mood = ?")
        params.append(args.mood)
    if args.desc is not None:
        updates.append("description = ?")
        params.append(args.desc)

    if updates:
        params.append(args.id)
        conn.execute(f"UPDATE clips SET {', '.join(updates)} WHERE id = ?", params)

    if args.section is not None:
        conn.execute("DELETE FROM clip_sections WHERE clip_id = ?", (args.id,))
        for sec in [s.strip() for s in args.section.split(",") if s.strip()]:
            conn.execute("INSERT INTO clip_sections (clip_id, section) VALUES (?, ?)",
                         (args.id, sec))

    conn.commit()
    conn.close()
    print(f"Updated clip ID {args.id}")


def cmd_delete(args):
    """Remove clip from DB."""
    conn = get_db()
    row = conn.execute("SELECT filename FROM clips WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Clip ID {args.id} not found.")
        conn.close()
        return

    conn.execute("DELETE FROM clips WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted clip ID {args.id}: {row['filename']}")


def cmd_refresh(args):
    """Re-scan all files and update durations via ffprobe."""
    conn = get_db()
    rows = conn.execute("SELECT id, path, duration_seconds FROM clips").fetchall()
    updated = 0
    missing = 0

    for row in rows:
        if not os.path.isfile(row["path"]):
            print(f"  MISSING: ID {row['id']} — {row['path']}")
            missing += 1
            continue
        new_dur = get_duration(row["path"])
        if abs(new_dur - row["duration_seconds"]) > 0.01:
            conn.execute("UPDATE clips SET duration_seconds = ? WHERE id = ?",
                         (new_dur, row["id"]))
            print(f"  UPDATED: ID {row['id']} {row['duration_seconds']:.2f}s → {new_dur:.2f}s")
            updated += 1

    conn.commit()
    conn.close()
    print(f"\nRefresh complete: {updated} updated, {missing} missing files, {len(rows) - updated - missing} unchanged")


def cmd_sync(args):
    """Find orphan files and missing DB entries."""
    conn = get_db()
    db_paths = set()
    for row in conn.execute("SELECT path FROM clips").fetchall():
        db_paths.add(row["path"])
    conn.close()

    files = discover_files()
    file_paths = set(files.values())

    orphan_files = file_paths - db_paths
    missing_files = db_paths - file_paths

    if orphan_files:
        print(f"Files NOT in DB ({len(orphan_files)}):")
        for p in sorted(orphan_files):
            print(f"  + {os.path.basename(p)}")
    else:
        print("All files are in DB.")

    if missing_files:
        print(f"\nDB entries WITHOUT files ({len(missing_files)}):")
        for p in sorted(missing_files):
            print(f"  - {os.path.basename(p)}")
    else:
        print("All DB entries have files.")

    if not orphan_files and not missing_files:
        print("\nDB and filesystem are in sync.")


def cmd_plan(args):
    """Compare total clip duration vs audio duration."""
    audio_file = args.audio_file
    if not os.path.isfile(audio_file):
        print(f"ERROR: Audio file not found: {audio_file}")
        sys.exit(1)

    audio_dur = get_duration(audio_file)

    clip_ids = [int(x.strip()) for x in args.clip_ids.split(",") if x.strip()]
    if not clip_ids:
        print("ERROR: No clip IDs provided.")
        sys.exit(1)

    conn = get_db()
    total_clip_dur = 0.0

    print("CLIP PLAN vs AUDIO")
    print("=" * 60)
    print(f"Audio: {os.path.basename(audio_file)} ({audio_dur:.2f}s)")
    print()
    print(f"{'ID':>4} | {'Duration':>8} | {'Filename'}")
    print(f"{'----':>4} | {'--------':>8} | {'--------'}")

    for cid in clip_ids:
        row = conn.execute("SELECT id, filename, duration_seconds FROM clips WHERE id = ?",
                           (cid,)).fetchone()
        if row:
            print(f"{row['id']:>4} | {row['duration_seconds']:>7.2f}s | {row['filename']}")
            total_clip_dur += row["duration_seconds"]
        else:
            print(f"{cid:>4} | {'???':>8} | NOT FOUND IN DB")

    conn.close()

    diff = total_clip_dur - audio_dur
    print()
    print(f"Clips total:  {total_clip_dur:.2f}s")
    print(f"Audio total:  {audio_dur:.2f}s")

    if diff >= 0:
        print(f"Surplus:      +{diff:.2f}s  OK")
    else:
        print(f"Gap:          {diff:.2f}s  *** NEED {abs(diff):.2f}s MORE CLIPS ***")
        if getattr(args, 'strict', False):
            sys.exit(1)


def cmd_export(args):
    """Regenerate CLIPS_CATALOG.md from DB."""
    conn = get_db()

    main_clips = conn.execute("""
        SELECT c.id, c.filename, c.duration_seconds, c.style, c.mood, c.description,
               GROUP_CONCAT(cs.section, ',') as sections
        FROM clips c
        LEFT JOIN clip_sections cs ON c.id = cs.clip_id
        WHERE c.is_visual_hook = 0
        GROUP BY c.id ORDER BY c.filename
    """).fetchall()

    vh_clips = conn.execute("""
        SELECT c.id, c.filename, c.duration_seconds, c.style, c.mood, c.description,
               GROUP_CONCAT(cs.section, ',') as sections
        FROM clips c
        LEFT JOIN clip_sections cs ON c.id = cs.clip_id
        WHERE c.is_visual_hook = 1
        GROUP BY c.id ORDER BY c.filename
    """).fetchall()

    conn.close()

    lines = []
    lines.append("# Clips Catalog")
    lines.append("")
    lines.append("Video clips for automated assembly. Used by `/givore-video` for intelligent clip selection.")
    lines.append("")
    lines.append("## Fields")
    lines.append("")
    lines.append("- **Section**: Script sections this clip fits — hook, proof, problem, rehook, body, bridge, cta, setup")
    lines.append("- **Style**: Visual category — cycling_pov, cycling_wheel, cycling_path, location, reveal, setup, transition, landmark")
    lines.append("- **Mood**: Energy level — energetic, calm, dramatic, playful, urgent, contemplative")
    lines.append("- **Duration**: Clip length in seconds")
    lines.append("")
    lines.append("## Clips")
    lines.append("")
    lines.append("| Filename | Duration | Section | Style | Mood | Description |")
    lines.append("|----------|----------|---------|-------|------|-------------|")

    for r in main_clips:
        sections = r["sections"] or ""
        style = r["style"] or ""
        mood = r["mood"] or ""
        desc = r["description"] or ""
        lines.append(f"| {r['filename']} | {r['duration_seconds']:.1f}s | {sections} | {style} | {mood} | {desc} |")

    lines.append("")
    lines.append("## Visual Hooks")
    lines.append("")
    lines.append("| Filename | Duration | Section | Style | Mood | Description |")
    lines.append("|----------|----------|---------|-------|------|-------------|")

    for r in vh_clips:
        sections = r["sections"] or ""
        style = r["style"] or ""
        mood = r["mood"] or ""
        desc = r["description"] or ""
        lines.append(f"| visual hooks/{r['filename']} | {r['duration_seconds']:.1f}s | {sections} | {style} | {mood} | {desc} |")

    lines.append("")

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Exported {len(main_clips)} main + {len(vh_clips)} visual hook clips to {CATALOG_PATH}")


def main():
    parser = argparse.ArgumentParser(description="Givore Clip Database")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Import clips from filesystem + catalog")

    p_list = sub.add_parser("list", help="List clips with filters")
    p_list.add_argument("--section", help="Filter by section (hook, body, etc.)")
    p_list.add_argument("--style", help="Filter by style (cycling_pov, etc.)")
    p_list.add_argument("--mood", help="Filter by mood (energetic, calm, etc.)")
    p_list.add_argument("--visual-hooks", action="store_true", help="Show only visual hooks")

    p_search = sub.add_parser("search", help="Search by section (shortcut)")
    p_search.add_argument("section", help="Section to search for")

    p_info = sub.add_parser("info", help="Show full details for one clip")
    p_info.add_argument("id", type=int, help="Clip ID")

    p_add = sub.add_parser("add", help="Add a new clip")
    p_add.add_argument("file", help="Path to .mp4 file")
    p_add.add_argument("--section", help="Sections (comma-separated)")
    p_add.add_argument("--style", help="Visual style")
    p_add.add_argument("--mood", help="Mood/energy")
    p_add.add_argument("--desc", help="Description")

    p_update = sub.add_parser("update", help="Update clip metadata")
    p_update.add_argument("id", type=int, help="Clip ID")
    p_update.add_argument("--section", help="New sections (comma-separated, replaces all)")
    p_update.add_argument("--style", help="New style")
    p_update.add_argument("--mood", help="New mood")
    p_update.add_argument("--desc", help="New description")

    p_delete = sub.add_parser("delete", help="Remove clip from DB")
    p_delete.add_argument("id", type=int, help="Clip ID")

    sub.add_parser("refresh", help="Re-scan all files, update durations")
    sub.add_parser("sync", help="Check filesystem vs DB consistency")

    p_plan = sub.add_parser("plan", help="Compare clips vs audio duration")
    p_plan.add_argument("audio_file", help="Path to audio file")
    p_plan.add_argument("clip_ids", help="Comma-separated clip IDs")
    p_plan.add_argument("--strict", action="store_true",
                        help="Exit 1 if clips shorter than audio")

    sub.add_parser("export", help="Regenerate CLIPS_CATALOG.md from DB")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "init": cmd_init,
        "list": cmd_list,
        "search": cmd_search,
        "info": cmd_info,
        "add": cmd_add,
        "update": cmd_update,
        "delete": cmd_delete,
        "refresh": cmd_refresh,
        "sync": cmd_sync,
        "plan": cmd_plan,
        "export": cmd_export,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
