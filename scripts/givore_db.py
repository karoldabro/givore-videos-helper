#!/usr/bin/env python3
"""Givore Database — Unified SQLite repository for clips and content history.

Manages video clip metadata (formerly clip_db.py) plus rotation history
for scripts, trials, and video assemblies.

Usage:
    ## Clip commands
    givore_db.py list [--section X] [--style X] [--mood X] [--visual-hooks]
    givore_db.py search <section>                  Shortcut for list --section
    givore_db.py info <id>                         Full details for one clip
    givore_db.py add <file> [--section X,Y] [--style X] [--mood X] [--desc "..."]
    givore_db.py update <id> [--section X,Y] [--style X] [--mood X] [--desc "..."]
    givore_db.py delete <id>                       Remove clip from DB
    givore_db.py refresh                           Re-scan all files, update durations
    givore_db.py sync                              Find orphan files / missing DB entries
    givore_db.py new                               List files not yet in DB (one per line)
    givore_db.py bulk-add <json_file>              Import clips from JSON with AI-categorized metadata
    givore_db.py plan <audio_file> <id1,id2,...>   Compare clips vs audio duration

    ## Script history
    givore_db.py script-add --date X --slug X [--file X] [--hook-type X] ...
    givore_db.py script-list [--last N]
    givore_db.py script-rotation [--last N]        Compact rotation constraints
    givore_db.py script-rotation-json [--last N]   JSON rotation constraints (machine-readable)
    givore_db.py script-delete <id>

    ## Trial history
    givore_db.py trial-add --date X --slug X [--file X] [--audience X] ...
    givore_db.py trial-list [--last N]
    givore_db.py trial-rotation [--last N]         Compact rotation constraints
    givore_db.py trial-delete <id>

    ## Video history
    givore_db.py video-add --date X --slug X [--hook-clips "a,b"] [--body-clips "c,d"] ...
    givore_db.py video-list [--last N]
    givore_db.py video-recent-clips [--last N]     Clips used in last N videos
    givore_db.py video-delete <id>

    ## Renueva history
    givore_db.py renueva-add --date X --slug X [--item-category X] ...
    givore_db.py renueva-list [--last N]
    givore_db.py renueva-rotation [--last N]       Compact rotation constraints
    givore_db.py renueva-delete <id>

    ## Thumbnail history
    givore_db.py thumbnail-add --date X --slug X --bg "1.png"
    givore_db.py thumbnail-list [--last N]
    givore_db.py thumbnail-recent-bgs [--last N]   Backgrounds used in last N thumbnails
    givore_db.py thumbnail-delete <id>

    ## Migration
    givore_db.py migrate-scripts                   Import SCRIPT_HISTORY.md
    givore_db.py migrate-trials                    Import TRIAL_HISTORY.md
    givore_db.py migrate-videos                    Import VIDEO_HISTORY.md
    givore_db.py migrate-all                       Import all three
"""

import argparse
import glob
import os
import sqlite3
import subprocess
import sys

GIVORE_ROOT = "/media/kdabrow/Programy/givore"
CLIPS_DIR = os.path.join(GIVORE_ROOT, "videos", "clips")
DB_PATH = os.path.join(GIVORE_ROOT, "scripts", "clips.db")
SCRIPTS_DIR = os.path.join(GIVORE_ROOT, "scripts")

CLIP_SCHEMA = """
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

HISTORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS script_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project_slug TEXT NOT NULL,
    file_path TEXT,
    hook_type TEXT,
    cta_type TEXT,
    proof_tease TEXT,
    problem_angle TEXT,
    rehook_style TEXT,
    visual_style TEXT,
    lighting TEXT,
    item_category TEXT,
    structure_type TEXT,
    persona TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS trial_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project_slug TEXT NOT NULL,
    file_path TEXT,
    audience TEXT,
    format TEXT,
    tone TEXT,
    marketing TEXT,
    duration TEXT,
    item_focus TEXT,
    pain_point TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS video_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project_slug TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS video_clips_used (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER NOT NULL,
    clip_name TEXT NOT NULL,
    role TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video_history(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS renueva_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project_slug TEXT NOT NULL,
    file_path TEXT,
    item_category TEXT,
    item_description TEXT,
    transformation_ideas TEXT,
    hook_type TEXT,
    cta_type TEXT,
    num_ideas INTEGER DEFAULT 1,
    source_type TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_script_history_date ON script_history(date);
CREATE INDEX IF NOT EXISTS idx_trial_history_date ON trial_history(date);
CREATE INDEX IF NOT EXISTS idx_video_history_date ON video_history(date);
CREATE INDEX IF NOT EXISTS idx_video_clips_used_video ON video_clips_used(video_id);
CREATE INDEX IF NOT EXISTS idx_renueva_history_date ON renueva_history(date);

CREATE TABLE IF NOT EXISTS thumbnail_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    project_slug TEXT NOT NULL,
    bg_filename TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_thumbnail_history_date ON thumbnail_history(date);
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema():
    """Create all tables if they don't exist (non-destructive)."""
    conn = get_db()
    conn.executescript(CLIP_SCHEMA + HISTORY_SCHEMA)
    conn.commit()
    conn.close()


def create_db():
    conn = get_db()
    conn.executescript(CLIP_SCHEMA + HISTORY_SCHEMA)
    conn.commit()
    return conn


# ============================================================
# Clip helpers (unchanged from clip_db.py)
# ============================================================

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


def discover_files():
    """Find all .mp4 files in clips directory. Returns {basename: abspath}."""
    files = {}
    for f in glob.glob(os.path.join(CLIPS_DIR, "*.mp4")):
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


# ============================================================
# Clip commands
# ============================================================



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
    sections = [s.strip() for s in args.section.split(",")] if args.section else []
    is_vh = getattr(args, 'visual_hook', False)

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


def cmd_new(args):
    """List files on disk not yet in DB (one filename per line)."""
    conn = get_db()
    db_paths = set()
    for row in conn.execute("SELECT path FROM clips").fetchall():
        db_paths.add(row["path"])
    conn.close()

    files = discover_files()
    new_files = sorted(f for f, p in files.items() if p not in db_paths)

    if not new_files:
        print("No new clips found.")
        return

    for f in new_files:
        print(f)


def cmd_bulk_add(args):
    """Import clips from a JSON file with pre-categorized metadata.

    JSON format: list of objects with keys:
      filename (required), sections (list), style, mood, desc, visual_hook (bool)
    Duration is auto-detected via ffprobe. Duplicates are skipped.
    """
    import json

    json_path = os.path.abspath(args.file)
    if not os.path.isfile(json_path):
        print(f"ERROR: JSON file not found: {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    if not isinstance(entries, list):
        print("ERROR: JSON must be a list of clip objects")
        sys.exit(1)

    conn = get_db()
    added = 0
    skipped = 0

    for entry in entries:
        filename = entry.get("filename")
        if not filename:
            print(f"  SKIP: entry missing 'filename': {entry}")
            skipped += 1
            continue

        filepath = os.path.join(CLIPS_DIR, filename)
        if not os.path.isfile(filepath):
            print(f"  SKIP: file not found: {filename}")
            skipped += 1
            continue

        existing = conn.execute("SELECT id FROM clips WHERE path = ?", (filepath,)).fetchone()
        if existing:
            print(f"  SKIP: already in DB (ID {existing['id']}): {filename}")
            skipped += 1
            continue

        duration = get_duration(filepath)
        sections = entry.get("sections", ["body"])
        style = entry.get("style", "cycling_pov")
        mood = entry.get("mood", "calm")
        desc = entry.get("desc", "")
        is_vh = entry.get("visual_hook", False)

        clip_id = insert_clip(conn, filepath, filename, duration, style, mood, desc, is_vh, sections)
        added += 1
        vh_tag = " [VH]" if is_vh else ""
        print(f"  #{clip_id} {filename} ({duration:.2f}s) [{','.join(sections)}] {style}/{mood}{vh_tag}")

    conn.commit()
    conn.close()
    print(f"\nBulk add complete: {added} added, {skipped} skipped")


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


def cmd_generate_config(args):
    """Generate assembly_config.json from audio file + ordered clip IDs."""
    import json as _json

    audio_file = os.path.abspath(args.audio)
    if not os.path.isfile(audio_file):
        print(f"ERROR: Audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)

    audio_dur = get_duration(audio_file)

    project_folder = os.path.abspath(args.project_folder)
    if not os.path.isdir(project_folder):
        os.makedirs(project_folder, exist_ok=True)

    # Defaults
    template = args.template or os.path.join(GIVORE_ROOT, "projects", "template.kdenlive-cli.json")
    ass_template = args.ass_template or os.path.join(GIVORE_ROOT, "projects", "template.kdenlive.ass")

    # Auto-detect SRT
    srt_path = args.srt
    if not srt_path:
        base = os.path.splitext(os.path.basename(audio_file))[0]
        candidate = os.path.join(project_folder, base + ".srt")
        if os.path.isfile(candidate):
            srt_path = candidate
        else:
            print(f"WARNING: No .srt found, subtitles will be empty", file=sys.stderr)
            srt_path = ""

    # Resolve clip IDs
    clip_ids = [int(x.strip()) for x in args.clips.split(",") if x.strip()]
    if not clip_ids:
        print("ERROR: No clip IDs provided.", file=sys.stderr)
        sys.exit(1)

    # Check for duplicate clip IDs
    seen_ids = {}
    for i, cid in enumerate(clip_ids):
        if cid in seen_ids:
            print(f"ERROR: Duplicate clip ID {cid} at positions {seen_ids[cid]} and {i}",
                  file=sys.stderr)
            sys.exit(1)
        seen_ids[cid] = i

    conn = get_db()
    clips = []
    position = 0.0

    for i, cid in enumerate(clip_ids):
        row = conn.execute(
            "SELECT id, filename, path, duration_seconds FROM clips WHERE id = ?",
            (cid,)
        ).fetchone()
        if not row:
            print(f"ERROR: Clip ID {cid} not found in DB", file=sys.stderr)
            conn.close()
            sys.exit(1)

        dur = row["duration_seconds"]
        clips.append({
            "section": "BODY",
            "file": row["path"],
            "name": f"clip_{i:02d}",
            "position": round(position, 3),
            "duration": round(dur, 3),
            "in_point": 0.0,
        })
        position += dur

    conn.close()

    # Check ending clip placement
    def _is_end_clip(basename):
        lower = basename.lower()
        return (lower.startswith("[end]") or
                "[hook | end]" in lower or
                "[hook|ending" in lower)

    end_positions = [i for i, c in enumerate(clips)
                     if _is_end_clip(os.path.basename(c["file"]))]
    for pos in end_positions:
        if pos != len(clips) - 1:
            name = os.path.basename(clips[pos]["file"])
            print(f"WARNING: Ending clip at position {pos}/{len(clips)-1}, "
                  f"should be last: {name}", file=sys.stderr)
    if len(end_positions) > 1:
        print(f"WARNING: Multiple ending clips at positions: "
              f"{', '.join(str(p) for p in end_positions)}", file=sys.stderr)

    total_clip_dur = position

    # Extend last clip if needed to cover audio
    if total_clip_dur < audio_dur and clips:
        gap = audio_dur - total_clip_dur
        clips[-1]["duration"] = round(clips[-1]["duration"] + gap, 3)
        total_clip_dur = audio_dur
        print(f"Extended last clip by {gap:.2f}s to cover audio")

    # Parse --sfx shorthand into SFX array
    sfx_list = []
    if args.sfx:
        BASIC_SFX = {
            "WHOOSH": {"file": "Whoosh - Fast Short.MP3", "duration": 0.3, "volume": 0.035},
            "DING":   {"file": "Ding - Single - Bright.MP3", "duration": 2.1, "volume": 0.03},
            "CHIME":  {"file": "Correct - Synthetic Chime.MP3", "duration": 0.9, "volume": 0.03},
            "POP":    {"file": "Pop 1.MP3", "duration": 0.2, "volume": 0.03},
            "SWOOSH": {"file": "Swoosh - Fast 1.MP3", "duration": 0.7, "volume": 0.03},
        }
        sfx_dir = os.path.join(GIVORE_ROOT, "Audio effects")
        for entry in args.sfx.split(","):
            entry = entry.strip()
            if "@" not in entry:
                print(f"ERROR: SFX entry missing @position: {entry}", file=sys.stderr)
                sys.exit(1)
            name, pos_str = entry.split("@", 1)
            name = name.strip().upper()
            if name not in BASIC_SFX:
                print(f"ERROR: Unknown SFX '{name}'. Use: {', '.join(BASIC_SFX.keys())}",
                      file=sys.stderr)
                sys.exit(1)
            sfx_info = BASIC_SFX[name]
            sfx_list.append({
                "file": os.path.join(sfx_dir, sfx_info["file"]),
                "name": name.lower(),
                "position": float(pos_str),
                "duration": sfx_info["duration"],
                "volume": sfx_info["volume"],
            })
        print(f"SFX: {len(sfx_list)} Basic Tier effects added")

    config = {
        "project_folder": project_folder + "/",
        "template": os.path.abspath(template),
        "clips": clips,
        "sfx": sfx_list,
        "audio": audio_file,
        "subtitles": os.path.abspath(srt_path) if srt_path else "",
        "subtitle_template_ass": os.path.abspath(ass_template),
    }

    out_path = os.path.join(project_folder, "assembly_config.json")
    with open(out_path, "w") as f:
        _json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Config written: {out_path}")
    print(f"Clips: {len(clips)} | Clips total: {total_clip_dur:.2f}s | Audio: {audio_dur:.2f}s")


# ============================================================
# Script history commands
# ============================================================

SCRIPT_FIELDS = ["hook_type", "cta_type", "proof_tease", "problem_angle",
                 "rehook_style", "visual_style", "lighting", "item_category",
                 "structure_type", "persona"]


def cmd_script_add(args):
    """Add a script history entry."""
    ensure_schema()
    conn = get_db()
    conn.execute(
        """INSERT INTO script_history
           (date, project_slug, file_path, hook_type, cta_type, proof_tease,
            problem_angle, rehook_style, visual_style, lighting, item_category,
            structure_type, persona)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (args.date, args.slug, args.file, args.hook_type, args.cta_type,
         args.proof_tease, args.problem_angle, args.rehook_style,
         args.visual_style, args.lighting, args.item_category,
         args.structure_type, args.persona)
    )
    conn.commit()
    conn.close()
    print(f"Added script history: {args.date} {args.slug}")


def cmd_script_list(args):
    """List recent script history entries."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 10
    rows = conn.execute(
        "SELECT * FROM script_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No script history entries.")
        return

    print(f"{'ID':>4} | {'Date':<12} | {'Slug':<30} | {'Hook':<16} | {'CTA':<12} | {'Proof':<6} | {'Problem':<20} | {'Rehook':<18} | {'Visual':<12} | {'Light':<12} | {'Item':<10}")
    print("-" * 170)
    for r in rows:
        print(f"{r['id']:>4} | {r['date']:<12} | {r['project_slug']:<30} | {r['hook_type'] or '-':<16} | {r['cta_type'] or '-':<12} | {r['proof_tease'] or '-':<6} | {r['problem_angle'] or '-':<20} | {r['rehook_style'] or '-':<18} | {r['visual_style'] or '-':<12} | {r['lighting'] or '-':<12} | {r['item_category'] or '-':<10}")

    print(f"\n{len(rows)} entry(ies)")


def cmd_script_rotation(args):
    """Show compact rotation constraints for script generation."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 3
    rows = conn.execute(
        "SELECT * FROM script_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No script history — no rotation constraints.")
        return

    print(f"SCRIPT ROTATION CONSTRAINTS (last {len(rows)}):")
    for field in SCRIPT_FIELDS:
        values = [r[field] or "-" for r in rows]
        values_str = ", ".join(values)
        # Determine advice
        if field == "proof_tease":
            if all(v == values[0] for v in values) and len(values) >= 2:
                opposite = "YES" if values[0].lower() == "no" else "NO"
                advice = f"use {opposite} next"
            else:
                advice = "any OK"
        else:
            advice = "avoid these"
        print(f"  {field:<16} {values_str:<50} -> {advice}")


def cmd_script_rotation_json(args):
    """Output script rotation constraints as machine-readable JSON."""
    import json
    ensure_schema()
    conn = get_db()
    limit = args.last or 5

    # --- Script history fields ---
    rows = conn.execute(
        "SELECT * FROM script_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()

    avoid = {}
    if rows:
        for field in SCRIPT_FIELDS:
            values = [r[field] for r in rows if r[field]]
            if field == "proof_tease":
                # Keep raw values (not deduplicated) so consumer sees the pattern
                avoid[field] = values
            else:
                avoid[field] = sorted(set(values))

    # --- Recently used clips (same logic as video-recent-clips, last 10 videos) ---
    clip_limit = 10
    clip_rows = conn.execute(
        """SELECT DISTINCT vc.clip_name
           FROM video_clips_used vc
           JOIN video_history vh ON vc.video_id = vh.id
           WHERE vh.id IN (SELECT id FROM video_history ORDER BY date DESC, id DESC LIMIT ?)""",
        (clip_limit,)
    ).fetchall()

    recent_clip_names = sorted(r["clip_name"] for r in clip_rows) if clip_rows else []

    # Resolve clip names to DB IDs where possible
    recent_clip_ids = []
    if recent_clip_names:
        placeholders = ",".join("?" for _ in recent_clip_names)
        id_rows = conn.execute(
            f"SELECT id FROM clips WHERE filename IN ({placeholders})",
            recent_clip_names,
        ).fetchall()
        recent_clip_ids = sorted(r["id"] for r in id_rows)

    conn.close()

    result = {
        "last_n": len(rows),
        "avoid": avoid,
        "recent_clips": recent_clip_ids,
        "recent_clip_names": recent_clip_names,
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_script_delete(args):
    """Delete a script history entry."""
    ensure_schema()
    conn = get_db()
    row = conn.execute("SELECT project_slug FROM script_history WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Script history ID {args.id} not found.")
        conn.close()
        return
    conn.execute("DELETE FROM script_history WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted script history ID {args.id}: {row['project_slug']}")


# ============================================================
# Trial history commands
# ============================================================

TRIAL_FIELDS = ["audience", "format", "tone", "marketing", "duration",
                "item_focus", "pain_point"]


def cmd_trial_add(args):
    """Add a trial history entry."""
    ensure_schema()
    conn = get_db()
    conn.execute(
        """INSERT INTO trial_history
           (date, project_slug, file_path, audience, format, tone,
            marketing, duration, item_focus, pain_point)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (args.date, args.slug, args.file, args.audience, args.format,
         args.tone, args.marketing, args.duration, args.item_focus,
         args.pain_point)
    )
    conn.commit()
    conn.close()
    print(f"Added trial history: {args.date} {args.slug}")


def cmd_trial_list(args):
    """List recent trial history entries."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 10
    rows = conn.execute(
        "SELECT * FROM trial_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No trial history entries.")
        return

    print(f"{'ID':>4} | {'Date':<12} | {'Slug':<30} | {'Audience':<12} | {'Format':<20} | {'Tone':<14} | {'Mktg':<8} | {'Dur':<5} | {'Item':<12} | {'Pain':<12}")
    print("-" * 150)
    for r in rows:
        print(f"{r['id']:>4} | {r['date']:<12} | {r['project_slug']:<30} | {r['audience'] or '-':<12} | {r['format'] or '-':<20} | {r['tone'] or '-':<14} | {r['marketing'] or '-':<8} | {r['duration'] or '-':<5} | {r['item_focus'] or '-':<12} | {r['pain_point'] or '-':<12}")

    print(f"\n{len(rows)} entry(ies)")


def cmd_trial_rotation(args):
    """Show compact rotation constraints for trial generation."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 3
    rows = conn.execute(
        "SELECT * FROM trial_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No trial history — no rotation constraints.")
        return

    print(f"TRIAL ROTATION CONSTRAINTS (last {len(rows)}):")
    for field in TRIAL_FIELDS:
        values = [r[field] or "-" for r in rows]
        values_str = ", ".join(values)
        if field in ("marketing", "duration"):
            if all(v == values[0] for v in values) and len(values) >= 2:
                advice = "switch next"
            else:
                advice = "any OK"
        else:
            advice = "avoid these"
        print(f"  {field:<16} {values_str:<50} -> {advice}")


def cmd_trial_delete(args):
    """Delete a trial history entry."""
    ensure_schema()
    conn = get_db()
    row = conn.execute("SELECT project_slug FROM trial_history WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Trial history ID {args.id} not found.")
        conn.close()
        return
    conn.execute("DELETE FROM trial_history WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted trial history ID {args.id}: {row['project_slug']}")


# ============================================================
# Video history commands
# ============================================================

def cmd_video_add(args):
    """Add a video history entry with clips used."""
    ensure_schema()
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO video_history (date, project_slug) VALUES (?, ?)",
        (args.date, args.slug)
    )
    video_id = cur.lastrowid

    # Insert clips by role
    if args.clips:
        # Flat list: all clips as role "body"
        for clip_name in [c.strip() for c in args.clips.split(",") if c.strip()]:
            conn.execute(
                "INSERT INTO video_clips_used (video_id, clip_name, role) VALUES (?, ?, ?)",
                (video_id, clip_name, "body")
            )
    else:
        for role, clips_str in [("hook", args.hook_clips), ("body", args.body_clips),
                                 ("bridge", args.bridge_clips), ("cta", args.cta_clips)]:
            if clips_str:
                for clip_name in [c.strip() for c in clips_str.split(",") if c.strip()]:
                    conn.execute(
                        "INSERT INTO video_clips_used (video_id, clip_name, role) VALUES (?, ?, ?)",
                        (video_id, clip_name, role)
                    )

    conn.commit()
    conn.close()
    print(f"Added video history ID {video_id}: {args.date} {args.slug}")


def cmd_video_list(args):
    """List recent video history entries."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 10
    rows = conn.execute(
        "SELECT * FROM video_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()

    if not rows:
        print("No video history entries.")
        conn.close()
        return

    for r in rows:
        clips = conn.execute(
            "SELECT clip_name, role FROM video_clips_used WHERE video_id = ? ORDER BY role, clip_name",
            (r["id"],)
        ).fetchall()

        clips_by_role = {}
        for c in clips:
            clips_by_role.setdefault(c["role"], []).append(c["clip_name"])

        print(f"ID {r['id']:>3} | {r['date']} | {r['project_slug']}")
        for role in ["hook", "body", "bridge", "cta"]:
            if role in clips_by_role:
                print(f"        {role:<8}: {', '.join(clips_by_role[role])}")
        print()

    conn.close()
    print(f"{len(rows)} entry(ies)")


def cmd_video_recent_clips(args):
    """Show clips used in the last N videos (for exclusion during selection)."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 5
    rows = conn.execute(
        """SELECT DISTINCT vc.clip_name, vc.role, vh.date, vh.project_slug
           FROM video_clips_used vc
           JOIN video_history vh ON vc.video_id = vh.id
           WHERE vh.id IN (SELECT id FROM video_history ORDER BY date DESC, id DESC LIMIT ?)
           ORDER BY vh.date DESC, vc.role, vc.clip_name""",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No recent clips used.")
        return

    # Unique clip names for exclusion list
    unique_clips = sorted(set(r["clip_name"] for r in rows))

    print(f"CLIPS USED IN LAST {limit} VIDEOS (exclude from selection):")
    print(f"  {', '.join(unique_clips)}")
    print(f"\n{len(unique_clips)} unique clip(s) to avoid")


def cmd_video_delete(args):
    """Delete a video history entry."""
    ensure_schema()
    conn = get_db()
    row = conn.execute("SELECT project_slug FROM video_history WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Video history ID {args.id} not found.")
        conn.close()
        return
    conn.execute("DELETE FROM video_clips_used WHERE video_id = ?", (args.id,))
    conn.execute("DELETE FROM video_history WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted video history ID {args.id}: {row['project_slug']}")


# ============================================================
# Renueva history commands
# ============================================================

RENUEVA_FIELDS = ["item_category", "hook_type", "cta_type", "num_ideas",
                  "source_type", "transformation_ideas"]


def cmd_renueva_add(args):
    """Add a renueva history entry."""
    ensure_schema()
    conn = get_db()
    conn.execute(
        """INSERT INTO renueva_history
           (date, project_slug, file_path, item_category, item_description,
            transformation_ideas, hook_type, cta_type, num_ideas, source_type)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (args.date, args.slug, args.file, args.item_category,
         args.item_description, args.transformation_ideas,
         args.hook_type, args.cta_type, args.num_ideas, args.source_type)
    )
    conn.commit()
    conn.close()
    print(f"Added renueva history: {args.date} {args.slug}")


def cmd_renueva_list(args):
    """List recent renueva history entries."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 10
    rows = conn.execute(
        "SELECT * FROM renueva_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No renueva history entries.")
        return

    print(f"{'ID':>4} | {'Date':<12} | {'Slug':<30} | {'Category':<12} | {'Hook':<16} | {'CTA':<12} | {'Ideas':<6} | {'Source':<14} | {'Transformation':<30}")
    print("-" * 160)
    for r in rows:
        ideas_str = (r['transformation_ideas'] or '-')[:30]
        print(f"{r['id']:>4} | {r['date']:<12} | {r['project_slug']:<30} | {r['item_category'] or '-':<12} | {r['hook_type'] or '-':<16} | {r['cta_type'] or '-':<12} | {r['num_ideas'] or 1:<6} | {r['source_type'] or '-':<14} | {ideas_str:<30}")

    print(f"\n{len(rows)} entry(ies)")


def cmd_renueva_rotation(args):
    """Show compact rotation constraints for renueva generation."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 3
    rows = conn.execute(
        "SELECT * FROM renueva_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No renueva history — no rotation constraints.")
        return

    print(f"RENUEVA ROTATION CONSTRAINTS (last {len(rows)}):")
    for field in RENUEVA_FIELDS:
        values = [str(r[field]) if r[field] else "-" for r in rows]
        values_str = ", ".join(values)
        advice = "avoid these"
        print(f"  {field:<24} {values_str:<50} -> {advice}")


def cmd_renueva_delete(args):
    """Delete a renueva history entry."""
    ensure_schema()
    conn = get_db()
    row = conn.execute("SELECT project_slug FROM renueva_history WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Renueva history ID {args.id} not found.")
        conn.close()
        return
    conn.execute("DELETE FROM renueva_history WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted renueva history ID {args.id}: {row['project_slug']}")


# ============================================================
# Thumbnail history commands
# ============================================================

def cmd_thumbnail_add(args):
    """Add a thumbnail history entry recording which background was used."""
    ensure_schema()
    conn = get_db()
    conn.execute(
        "INSERT INTO thumbnail_history (date, project_slug, bg_filename) VALUES (?, ?, ?)",
        (args.date, args.slug, args.bg)
    )
    conn.commit()
    conn.close()
    print(f"Added thumbnail history: {args.date} {args.slug} bg={args.bg}")


def cmd_thumbnail_list(args):
    """List recent thumbnail history entries."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 10
    rows = conn.execute(
        "SELECT * FROM thumbnail_history ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No thumbnail history entries.")
        return

    print(f"{'ID':>4} | {'Date':<12} | {'Slug':<30} | {'Background':<30}")
    print("-" * 80)
    for r in rows:
        print(f"{r['id']:>4} | {r['date']:<12} | {r['project_slug']:<30} | {r['bg_filename']:<30}")
    print(f"\n{len(rows)} entry(ies)")


def cmd_thumbnail_recent_bgs(args):
    """Show backgrounds used in last N thumbnails (for exclusion during selection)."""
    ensure_schema()
    conn = get_db()
    limit = args.last or 5
    rows = conn.execute(
        """SELECT DISTINCT bg_filename FROM thumbnail_history
           WHERE id IN (SELECT id FROM thumbnail_history ORDER BY date DESC, id DESC LIMIT ?)
           ORDER BY bg_filename""",
        (limit,)
    ).fetchall()
    conn.close()

    if not rows:
        print("No recent thumbnail backgrounds.")
        return

    bgs = [r["bg_filename"] for r in rows]
    print(f"BACKGROUNDS USED IN LAST {limit} THUMBNAILS (exclude from selection):")
    print(f"  {', '.join(bgs)}")
    print(f"\n{len(bgs)} background(s) to avoid")


def cmd_thumbnail_delete(args):
    """Delete a thumbnail history entry."""
    ensure_schema()
    conn = get_db()
    row = conn.execute("SELECT project_slug FROM thumbnail_history WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"Thumbnail history ID {args.id} not found.")
        conn.close()
        return
    conn.execute("DELETE FROM thumbnail_history WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Deleted thumbnail history ID {args.id}: {row['project_slug']}")


# ============================================================
# Migration commands
# ============================================================

def _parse_md_table(filepath):
    """Parse a markdown table file, return list of cell-lists for data rows."""
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip header and separator rows
        if line.startswith("|---") or line.startswith("| #") or line.startswith("| **"):
            continue

        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]

        # Skip rows that look like headers (contain "Date", "Filename", etc.)
        if parts and (parts[0] == "#" or parts[0] == "Column"):
            continue

        rows.append(parts)

    return rows


def cmd_migrate_scripts(args):
    """Import SCRIPT_HISTORY.md into script_history table."""
    ensure_schema()
    filepath = os.path.join(SCRIPTS_DIR, "SCRIPT_HISTORY.md")
    rows = _parse_md_table(filepath)

    conn = get_db()
    imported = 0

    for parts in rows:
        if len(parts) < 10:
            continue
        try:
            # | # | Date | File | Hook Type | CTA Type | Proof Tease | Problem Angle | Rehook Style | Visual Style | Lighting | Item Category |
            row_num = parts[0]
            if not row_num.isdigit():
                continue

            date = parts[1]
            file_path = parts[2]
            hook_type = parts[3]
            cta_type = parts[4]
            proof_tease = parts[5]
            problem_angle = parts[6]
            rehook_style = parts[7]
            visual_style = parts[8]
            lighting = parts[9]
            item_category = parts[10] if len(parts) > 10 else None

            # Derive slug from file_path (e.g. "2026-03-12_comunidad/file.txt" -> "comunidad")
            slug = file_path.split("/")[0] if "/" in file_path else file_path

            conn.execute(
                """INSERT INTO script_history
                   (date, project_slug, file_path, hook_type, cta_type, proof_tease,
                    problem_angle, rehook_style, visual_style, lighting, item_category)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, slug, file_path, hook_type, cta_type, proof_tease,
                 problem_angle, rehook_style, visual_style, lighting, item_category)
            )
            imported += 1
        except (IndexError, ValueError) as e:
            print(f"  SKIP row: {parts} ({e})")

    conn.commit()
    conn.close()
    print(f"Migrated {imported} script history entries from {filepath}")


def cmd_migrate_trials(args):
    """Import TRIAL_HISTORY.md into trial_history table."""
    ensure_schema()
    filepath = os.path.join(SCRIPTS_DIR, "TRIAL_HISTORY.md")
    rows = _parse_md_table(filepath)

    conn = get_db()
    imported = 0

    for parts in rows:
        if len(parts) < 9:
            continue
        try:
            # | # | Date | File | Audience | Format | Tone | Marketing | Duration | Item Focus | Pain Point |
            row_num = parts[0]
            if not row_num.isdigit():
                continue

            date = parts[1]
            file_path = parts[2]
            audience = parts[3]
            fmt = parts[4]
            tone = parts[5]
            marketing = parts[6]
            duration = parts[7]
            item_focus = parts[8] if len(parts) > 8 else None
            pain_point = parts[9] if len(parts) > 9 else None

            slug = file_path.split("/")[0] if "/" in file_path else file_path

            conn.execute(
                """INSERT INTO trial_history
                   (date, project_slug, file_path, audience, format, tone,
                    marketing, duration, item_focus, pain_point)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, slug, file_path, audience, fmt, tone,
                 marketing, duration, item_focus, pain_point)
            )
            imported += 1
        except (IndexError, ValueError) as e:
            print(f"  SKIP row: {parts} ({e})")

    conn.commit()
    conn.close()
    print(f"Migrated {imported} trial history entries from {filepath}")


def cmd_migrate_videos(args):
    """Import VIDEO_HISTORY.md into video_history + video_clips_used tables."""
    ensure_schema()
    filepath = os.path.join(SCRIPTS_DIR, "VIDEO_HISTORY.md")
    rows = _parse_md_table(filepath)

    conn = get_db()
    imported = 0

    for parts in rows:
        if len(parts) < 7:
            continue
        try:
            # | # | Date | Project | Hook Clip | Body Clips | Bridge Clip | CTA Clip | Transitions | Effects | SFX |
            row_num = parts[0]
            if not row_num.isdigit():
                continue

            date = parts[1]
            project_slug = parts[2]
            hook_clips_str = parts[3]
            body_clips_str = parts[4]
            bridge_clips_str = parts[5]
            cta_clips_str = parts[6]

            cur = conn.execute(
                "INSERT INTO video_history (date, project_slug) VALUES (?, ?)",
                (date, project_slug)
            )
            video_id = cur.lastrowid

            for role, clips_str in [("hook", hook_clips_str), ("body", body_clips_str),
                                     ("bridge", bridge_clips_str), ("cta", cta_clips_str)]:
                if clips_str and clips_str.strip() and clips_str.strip().lower() != "none":
                    for clip_name in [c.strip() for c in clips_str.split(",") if c.strip()]:
                        conn.execute(
                            "INSERT INTO video_clips_used (video_id, clip_name, role) VALUES (?, ?, ?)",
                            (video_id, clip_name, role)
                        )

            imported += 1
        except (IndexError, ValueError) as e:
            print(f"  SKIP row: {parts} ({e})")

    conn.commit()
    conn.close()
    print(f"Migrated {imported} video history entries from {filepath}")


def cmd_migrate_all(args):
    """Run all migrations."""
    cmd_migrate_scripts(args)
    cmd_migrate_trials(args)
    cmd_migrate_videos(args)
    print("\nAll migrations complete.")


# ============================================================
# Main CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Givore Database — clips + content history")
    sub = parser.add_subparsers(dest="command")

    # --- Clip commands ---
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
    p_add.add_argument("--visual-hook", action="store_true", help="Mark as visual hook")

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
    sub.add_parser("new", help="List files not yet in DB (one per line)")

    p_bulk = sub.add_parser("bulk-add", help="Import clips from JSON with pre-categorized metadata")
    p_bulk.add_argument("file", help="Path to JSON file")

    p_plan = sub.add_parser("plan", help="Compare clips vs audio duration")
    p_plan.add_argument("audio_file", help="Path to audio file")
    p_plan.add_argument("clip_ids", help="Comma-separated clip IDs")
    p_plan.add_argument("--strict", action="store_true",
                        help="Exit 1 if clips shorter than audio")

    p_gc = sub.add_parser("generate-config", help="Generate assembly_config.json from audio + clip IDs")
    p_gc.add_argument("--audio", required=True, help="Path to audio file")
    p_gc.add_argument("--clips", required=True, help="Comma-separated clip IDs in order")
    p_gc.add_argument("--project-folder", required=True, help="Output project folder (abs path)")
    p_gc.add_argument("--template", default=None, help="Template JSON path")
    p_gc.add_argument("--ass-template", default=None, help="ASS subtitle template path")
    p_gc.add_argument("--srt", default=None, help="SRT file path (auto-detected if omitted)")
    p_gc.add_argument("--sfx", default=None,
                      help='SFX shorthand: "WHOOSH@2.8,DING@15.2,CHIME@22.0,POP@45.1"')

    # --- Script history ---
    p_sa = sub.add_parser("script-add", help="Add script history entry")
    p_sa.add_argument("--date", required=True)
    p_sa.add_argument("--slug", required=True)
    p_sa.add_argument("--file", default=None)
    p_sa.add_argument("--hook-type", default=None)
    p_sa.add_argument("--cta-type", default=None)
    p_sa.add_argument("--proof-tease", default=None)
    p_sa.add_argument("--problem-angle", default=None)
    p_sa.add_argument("--rehook-style", default=None)
    p_sa.add_argument("--visual-style", default=None)
    p_sa.add_argument("--lighting", default=None)
    p_sa.add_argument("--item-category", default=None)
    p_sa.add_argument("--structure-type", default=None)
    p_sa.add_argument("--persona", default=None)

    p_sl = sub.add_parser("script-list", help="List recent script history")
    p_sl.add_argument("--last", type=int, default=10)

    p_sr = sub.add_parser("script-rotation", help="Show script rotation constraints")
    p_sr.add_argument("--last", type=int, default=3)

    p_srj = sub.add_parser("script-rotation-json", help="Script rotation constraints as JSON")
    p_srj.add_argument("--last", type=int, default=5)

    p_sd = sub.add_parser("script-delete", help="Delete script history entry")
    p_sd.add_argument("id", type=int)

    # --- Trial history ---
    p_ta = sub.add_parser("trial-add", help="Add trial history entry")
    p_ta.add_argument("--date", required=True)
    p_ta.add_argument("--slug", required=True)
    p_ta.add_argument("--file", default=None)
    p_ta.add_argument("--audience", default=None)
    p_ta.add_argument("--format", default=None)
    p_ta.add_argument("--tone", default=None)
    p_ta.add_argument("--marketing", default=None)
    p_ta.add_argument("--duration", default=None)
    p_ta.add_argument("--item-focus", default=None)
    p_ta.add_argument("--pain-point", default=None)

    p_tl = sub.add_parser("trial-list", help="List recent trial history")
    p_tl.add_argument("--last", type=int, default=10)

    p_tr = sub.add_parser("trial-rotation", help="Show trial rotation constraints")
    p_tr.add_argument("--last", type=int, default=3)

    p_td = sub.add_parser("trial-delete", help="Delete trial history entry")
    p_td.add_argument("id", type=int)

    # --- Video history ---
    p_va = sub.add_parser("video-add", help="Add video history entry")
    p_va.add_argument("--date", required=True)
    p_va.add_argument("--slug", required=True)
    p_va.add_argument("--clips", default=None, help="All clips as flat list (role=body)")
    p_va.add_argument("--hook-clips", default=None)
    p_va.add_argument("--body-clips", default=None)
    p_va.add_argument("--bridge-clips", default=None)
    p_va.add_argument("--cta-clips", default=None)

    p_vl = sub.add_parser("video-list", help="List recent video history")
    p_vl.add_argument("--last", type=int, default=10)

    p_vr = sub.add_parser("video-recent-clips", help="Clips used in last N videos")
    p_vr.add_argument("--last", type=int, default=5)

    p_vd = sub.add_parser("video-delete", help="Delete video history entry")
    p_vd.add_argument("id", type=int)

    # --- Renueva history ---
    p_ra = sub.add_parser("renueva-add", help="Add renueva history entry")
    p_ra.add_argument("--date", required=True)
    p_ra.add_argument("--slug", required=True)
    p_ra.add_argument("--file", default=None)
    p_ra.add_argument("--item-category", default=None)
    p_ra.add_argument("--item-description", default=None)
    p_ra.add_argument("--transformation-ideas", default=None)
    p_ra.add_argument("--hook-type", default=None)
    p_ra.add_argument("--cta-type", default=None)
    p_ra.add_argument("--num-ideas", type=int, default=1)
    p_ra.add_argument("--source-type", default=None)

    p_rl = sub.add_parser("renueva-list", help="List recent renueva history")
    p_rl.add_argument("--last", type=int, default=10)

    p_rr = sub.add_parser("renueva-rotation", help="Show renueva rotation constraints")
    p_rr.add_argument("--last", type=int, default=3)

    p_rd = sub.add_parser("renueva-delete", help="Delete renueva history entry")
    p_rd.add_argument("id", type=int)

    # --- Thumbnail history ---
    p_ta = sub.add_parser("thumbnail-add", help="Add thumbnail history entry")
    p_ta.add_argument("--date", required=True)
    p_ta.add_argument("--slug", required=True)
    p_ta.add_argument("--bg", required=True, help="Background image filename")

    p_tl = sub.add_parser("thumbnail-list", help="List recent thumbnail history")
    p_tl.add_argument("--last", type=int, default=10)

    p_tb = sub.add_parser("thumbnail-recent-bgs", help="Backgrounds used in last N thumbnails")
    p_tb.add_argument("--last", type=int, default=5)

    p_tde = sub.add_parser("thumbnail-delete", help="Delete thumbnail history entry")
    p_tde.add_argument("id", type=int)

    # --- Migration ---
    sub.add_parser("migrate-scripts", help="Import SCRIPT_HISTORY.md")
    sub.add_parser("migrate-trials", help="Import TRIAL_HISTORY.md")
    sub.add_parser("migrate-videos", help="Import VIDEO_HISTORY.md")
    sub.add_parser("migrate-all", help="Import all history files")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        # Clips
        "list": cmd_list,
        "search": cmd_search,
        "info": cmd_info,
        "add": cmd_add,
        "update": cmd_update,
        "delete": cmd_delete,
        "refresh": cmd_refresh,
        "sync": cmd_sync,
        "new": cmd_new,
        "bulk-add": cmd_bulk_add,
        "plan": cmd_plan,
        "generate-config": cmd_generate_config,
        # Script history
        "script-add": cmd_script_add,
        "script-list": cmd_script_list,
        "script-rotation": cmd_script_rotation,
        "script-rotation-json": cmd_script_rotation_json,
        "script-delete": cmd_script_delete,
        # Trial history
        "trial-add": cmd_trial_add,
        "trial-list": cmd_trial_list,
        "trial-rotation": cmd_trial_rotation,
        "trial-delete": cmd_trial_delete,
        # Video history
        "video-add": cmd_video_add,
        "video-list": cmd_video_list,
        "video-recent-clips": cmd_video_recent_clips,
        "video-delete": cmd_video_delete,
        # Renueva history
        "renueva-add": cmd_renueva_add,
        "renueva-list": cmd_renueva_list,
        "renueva-rotation": cmd_renueva_rotation,
        "renueva-delete": cmd_renueva_delete,
        # Thumbnail history
        "thumbnail-add": cmd_thumbnail_add,
        "thumbnail-list": cmd_thumbnail_list,
        "thumbnail-recent-bgs": cmd_thumbnail_recent_bgs,
        "thumbnail-delete": cmd_thumbnail_delete,
        # Migration
        "migrate-scripts": cmd_migrate_scripts,
        "migrate-trials": cmd_migrate_trials,
        "migrate-videos": cmd_migrate_videos,
        "migrate-all": cmd_migrate_all,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
