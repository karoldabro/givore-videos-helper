#!/usr/bin/env python3
"""Givore Video Assembly Script.

Assembles a Kdenlive project from a JSON config file containing clip selections,
SFX choices, audio, and subtitle references. Produces project.json + project.mlt
ready for rendering.

Usage:
    python3 assemble_video.py <config.json>

Config format:
{
  "project_folder": "/absolute/path/to/project",
  "template": "/absolute/path/to/template.kdenlive-cli.json",
  "clips": [
    {"section": "HOOK", "file": "/abs/path/clip.mp4", "name": "hook_clip",
     "position": 0.0, "duration": 3.0, "in_point": 0.0}
  ],
  "sfx": [
    {"file": "/abs/path/sfx.mp3", "name": "whoosh", "position": 2.8,
     "duration": 0.3, "volume": 0.4}
  ],
  "audio": "/abs/path/to/narration.mp3",
  "subtitles": "/abs/path/to/subtitles.srt",
  "subtitle_style": {"font": "Arial", "size": 65, "color": "#ffffff",
                      "bold": true, "outline_color": "#00aa00", "outline_width": 3}
}
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Add cli-anything-kdenlive to path
CLI_HARNESS = "/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness"
sys.path.insert(0, CLI_HARNESS)

from cli_anything.kdenlive.core import project as proj_mod
from cli_anything.kdenlive.core import bin as bin_mod
from cli_anything.kdenlive.core import timeline as tl_mod
from cli_anything.kdenlive.core import subtitles as sub_mod
from cli_anything.kdenlive.core import filters as filt_mod
from cli_anything.kdenlive.utils.mlt_xml import build_mlt_xml


def get_media_duration(filepath: str) -> float:
    """Get media file duration in seconds via ffprobe. Returns 0.0 on error."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", filepath],
            capture_output=True, text=True, timeout=10
        )
        return float(result.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):
        return 0.0


def _is_end_clip(basename: str) -> bool:
    """Check if a clip filename indicates an ending clip."""
    lower = basename.lower()
    return (lower.startswith("[end]") or
            "[hook | end]" in lower or
            "[hook|ending" in lower)


def validate_config(config: dict, strict: bool = False) -> list:
    """Pre-flight validation of assembly config.

    Returns list of (severity, code, message) tuples.
    Severities: ERROR (always fatal), WARNING (fatal in strict mode), INFO.
    """
    issues = []

    # Check project folder
    pf = config.get("project_folder", "")
    if pf and not os.path.isabs(pf):
        issues.append(("ERROR", "PROJECT_FOLDER_RELATIVE",
                        f"project_folder must be absolute: {pf}"))

    # Check template
    tmpl = config.get("template", "")
    if tmpl:
        if not os.path.isabs(tmpl):
            issues.append(("ERROR", "RELATIVE_PATH", f"Template path not absolute: {tmpl}"))
        elif not os.path.isfile(tmpl):
            issues.append(("ERROR", "TEMPLATE_MISSING", f"Template not found: {tmpl}"))

    # Check audio
    audio = config.get("audio", "")
    audio_dur = 0.0
    if audio:
        if not os.path.isabs(audio):
            issues.append(("ERROR", "RELATIVE_PATH", f"Audio path not absolute: {audio}"))
        elif not os.path.isfile(audio):
            issues.append(("ERROR", "AUDIO_FILE_MISSING", f"Audio not found: {audio}"))
        else:
            audio_dur = get_media_duration(audio)

    # Check clips
    clips_total = 0.0
    for i, clip in enumerate(config.get("clips", [])):
        cf = clip.get("file", "")
        if cf and not os.path.isabs(cf):
            issues.append(("ERROR", "RELATIVE_PATH", f"Clip {i} path not absolute: {cf}"))
        elif cf and not os.path.isfile(cf):
            issues.append(("ERROR", "CLIP_FILE_MISSING", f"Clip {i} not found: {cf}"))
        clips_total += clip.get("duration", 0.0)

    # Check for duplicate clip files (keyed by file+in_point to allow
    # same source at different in_points, e.g. screen recordings in renueva)
    seen = {}
    for i, clip in enumerate(config.get("clips", [])):
        cf = clip.get("file", "")
        in_pt = clip.get("in_point", 0.0)
        dedup_key = (cf, in_pt)
        if cf and dedup_key in seen:
            issues.append(("ERROR", "DUPLICATE_CLIP",
                            f"Clip {i} duplicates clip {seen[dedup_key]}: "
                            f"{os.path.basename(cf)} (in_point={in_pt})"))
        elif cf:
            seen[dedup_key] = i

    # Check ending clips placement and count
    clips_list = config.get("clips", [])
    end_clip_indices = []
    for i, clip in enumerate(clips_list):
        basename = os.path.basename(clip.get("file", ""))
        if _is_end_clip(basename):
            end_clip_indices.append(i)
            if i != len(clips_list) - 1:
                issues.append(("ERROR", "END_CLIP_NOT_LAST",
                                f"Ending clip at position {i}/{len(clips_list)-1}, "
                                f"must be last: {basename}"))
    if len(end_clip_indices) > 1:
        positions = ", ".join(str(p) for p in end_clip_indices)
        issues.append(("ERROR", "MULTIPLE_END_CLIPS",
                        f"Ending clips used {len(end_clip_indices)} times "
                        f"at positions: {positions}. Use at most once, always last."))

    # CRITICAL: clips total vs audio duration
    if audio_dur > 0 and clips_total > 0 and clips_total < audio_dur:
        gap = audio_dur - clips_total
        issues.append(("ERROR", "CLIPS_TOO_SHORT",
                        f"Clips total ({clips_total:.1f}s) < audio ({audio_dur:.1f}s) "
                        f"by {gap:.1f}s. Add clips or extend last clip."))

    # Check SFX files
    for i, sfx in enumerate(config.get("sfx", [])):
        sf = sfx.get("file", "")
        if sf and not os.path.isabs(sf):
            issues.append(("WARNING", "RELATIVE_PATH", f"SFX {i} path not absolute: {sf}"))
        elif sf and not os.path.isfile(sf):
            issues.append(("WARNING", "SFX_FILE_MISSING", f"SFX {i} not found: {sf}"))
        vol = sfx.get("volume")
        if vol is not None:
            if vol > 0.10:
                issues.append(("WARNING", "SFX_VOLUME_HIGH",
                                f"SFX {i} volume {vol} exceeds safe range (0.02-0.04)"))
            if vol < 0.005:
                issues.append(("WARNING", "SFX_VOLUME_LOW",
                                f"SFX {i} volume {vol} may be inaudible"))

    # Check subtitles
    sub = config.get("subtitles", "")
    if sub:
        if not os.path.isabs(sub):
            issues.append(("WARNING", "RELATIVE_PATH", f"Subtitle path not absolute: {sub}"))
        elif not os.path.isfile(sub):
            issues.append(("WARNING", "SUBTITLE_FILE_MISSING", f"Subtitles not found: {sub}"))

    return issues


def validate_render(video_path: str, expected_duration: float,
                    tolerance: float = 0.5) -> list:
    """Post-render validation of output video.

    Args:
        video_path: Path to rendered video file.
        expected_duration: Expected duration in seconds (max of clips, audio).
        tolerance: Acceptable difference in seconds.

    Returns list of (severity, code, message) tuples.
    """
    issues = []

    if not os.path.isfile(video_path):
        issues.append(("ERROR", "RENDER_FILE_MISSING",
                        f"Rendered file not found: {video_path}"))
        return issues

    size = os.path.getsize(video_path)
    if size == 0:
        issues.append(("ERROR", "RENDER_EMPTY", "Rendered file is empty (0 bytes)"))
        return issues
    if size < 100_000:
        issues.append(("WARNING", "RENDER_TOO_SMALL",
                        f"Rendered file suspiciously small: {size} bytes"))

    # Duration check
    actual_dur = get_media_duration(video_path)
    if actual_dur > 0 and expected_duration > 0:
        diff = abs(actual_dur - expected_duration)
        if diff > tolerance:
            issues.append(("ERROR", "RENDER_DURATION_MISMATCH",
                            f"Rendered duration {actual_dur:.1f}s != expected "
                            f"{expected_duration:.1f}s (diff: {diff:.1f}s)"))

    # Aspect ratio check
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    if probe.stdout.strip():
        dims = probe.stdout.strip().split(",")
        if len(dims) == 2:
            w, h = int(dims[0]), int(dims[1])
            ratio = w / h
            if abs(ratio - 9 / 16) > 0.01:
                issues.append(("WARNING", "RENDER_WRONG_ASPECT",
                                f"Aspect ratio {ratio:.4f} != 9:16. Actual: {w}x{h}"))

    return issues


def assemble(config_path: str) -> dict:
    """Assemble a video project from config JSON.

    Returns dict with paths to generated files.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    project_folder = config["project_folder"]
    template_path = config["template"]
    project_json = os.path.join(project_folder, "project.json")
    project_mlt = os.path.join(project_folder, "project.mlt")

    # Step 1: Copy template
    os.makedirs(project_folder, exist_ok=True)
    shutil.copy(template_path, project_json)

    # Step 2: Open project
    proj = proj_mod.open_project(project_json)

    # Step 3: Import video/image clips to bin
    for clip_info in config.get("clips", []):
        clip_type = clip_info.get("type", "video")
        bin_mod.import_clip(
            proj,
            source=clip_info["file"],
            name=clip_info.get("name", None),
            clip_type=clip_type,
        )

    # Step 4: Import narration audio to bin
    audio_path = config.get("audio", "")
    if audio_path and os.path.isfile(audio_path):
        bin_mod.import_clip(proj, source=audio_path, name="narration", clip_type="audio")

    # Step 5: Import SFX to bin
    for sfx_info in config.get("sfx", []):
        bin_mod.import_clip(
            proj,
            source=sfx_info["file"],
            name=sfx_info.get("name", None),
            clip_type="audio",
        )

    # Step 6: Create tracks
    v_track = tl_mod.add_track(proj, name="V1", track_type="video")
    a_track = tl_mod.add_track(proj, name="A1-Narration", track_type="audio")

    # Step 7: Place video/image clips on V1
    bin_clips = bin_mod.list_clips(proj)
    video_clips = [c for c in bin_clips if c["type"] in ("video", "image")]

    for i, clip_info in enumerate(config.get("clips", [])):
        if i >= len(video_clips):
            break
        clip_id = video_clips[i]["id"]
        duration = clip_info.get("duration", video_clips[i].get("duration", 2.0))
        in_point = clip_info.get("in_point", 0.0)
        tl_mod.add_clip_to_track(
            proj, v_track["id"], clip_id,
            position=clip_info.get("position", 0.0),
            in_point=in_point,
            out_point=in_point + duration,
        )

    # Step 7b: Validate video coverage vs audio
    clip_configs = config.get("clips", [])
    if clip_configs:
        last = clip_configs[-1]
        video_end = last.get("position", 0) + last.get("duration", 2.0)
    else:
        video_end = 0.0

    # Step 8: Place narration on A1
    narration_clips = [c for c in bin_clips if c["name"] == "narration"]
    if narration_clips:
        narration = narration_clips[0]
        audio_dur = narration["duration"]
        if video_end > 0 and video_end < audio_dur:
            gap = audio_dur - video_end
            print(f"ERROR: Video clips ({video_end:.1f}s) shorter than audio ({audio_dur:.1f}s) by {gap:.1f}s")
            print(f"  FATAL: This will cause frozen last frame. Add clips or extend last clip.")
            sys.exit(1)
        tl_mod.add_clip_to_track(
            proj, a_track["id"], narration["id"],
            position=0.0,
            in_point=0.0,
            out_point=audio_dur,
        )

    # Step 9: Place SFX on A2 (if any)
    sfx_configs = config.get("sfx", [])
    if sfx_configs:
        sfx_track = tl_mod.add_track(proj, name="A2-SFX", track_type="audio")
        sfx_clips = [c for c in bin_clips if c["type"] == "audio" and c["name"] != "narration"]

        for i, sfx_info in enumerate(sfx_configs):
            if i >= len(sfx_clips):
                break
            sfx_id = sfx_clips[i]["id"]
            sfx_dur = sfx_info.get("duration", sfx_clips[i].get("duration", 1.0))
            tl_mod.add_clip_to_track(
                proj, sfx_track["id"], sfx_id,
                position=sfx_info.get("position", 0.0),
                in_point=0.0,
                out_point=sfx_dur,
            )
            # Set volume (safe default 0.03; clamp to prevent blasting)
            volume = sfx_info.get("volume", 0.03)
            if volume > 0.10:
                print(f"  WARNING: SFX volume {volume} too high, clamping to 0.04")
                volume = 0.04
            elif volume < 0.005:
                print(f"  WARNING: SFX volume {volume} too low, clamping to 0.02")
                volume = 0.02
            clip_idx = len([c for c in proj["tracks"]
                           if c["id"] == sfx_track["id"]][0]["clips"]) - 1
            filt_mod.add_filter(proj, sfx_track["id"], clip_idx, "volume",
                                params={"level": str(volume)})

        print(f"SFX: placed {len(sfx_configs)} effects on A2 track")
        for i, s in enumerate(sfx_configs):
            print(f"  [{i+1}] {s.get('name', 'unnamed')} at {s.get('position', 0)}s, vol={s.get('volume', 0.03)}")

    # Step 10: Import subtitles
    subtitle_path = config.get("subtitles", "")
    if subtitle_path and os.path.isfile(subtitle_path):
        s_track = sub_mod.add_subtitle_track(proj, name="Subtitles")

        # Load styles from ASS template if provided, else use config subtitle_style
        ass_template = config.get("subtitle_template_ass", "")
        if ass_template and os.path.isfile(ass_template):
            ass_styles = sub_mod.parse_ass_styles(ass_template)
            default_style = ass_styles.get("Default", {})
            if default_style:
                sub_mod.set_track_style(proj, s_track["id"], **default_style)
        else:
            style = config.get("subtitle_style", {})
            if style:
                sub_mod.set_track_style(proj, s_track["id"], **style)

        if subtitle_path.endswith(".ass"):
            sub_mod.import_ass(proj, s_track["id"], subtitle_path)
        else:
            sub_mod.import_srt(proj, s_track["id"], subtitle_path)

    # Step 11: Save project JSON
    proj_mod.save_project(proj, project_json)

    # Step 12: Generate MLT XML
    xml = build_mlt_xml(proj)
    with open(project_mlt, "w", encoding="utf-8") as f:
        f.write(xml)

    # Step 12b: Save as .kdenlive (same MLT XML, Kdenlive-compatible for GUI editing)
    project_kdenlive = os.path.join(project_folder, "project.kdenlive")
    shutil.copy(project_mlt, project_kdenlive)

    # Summary
    track_count = len(proj.get("tracks", []))
    clip_count = sum(len(t.get("clips", [])) for t in proj.get("tracks", []))
    print(f"Project assembled: {project_json}")
    print(f"MLT XML exported: {project_mlt}")
    print(f"Kdenlive project: {project_kdenlive}")
    print(f"Tracks: {track_count}, Clips on timeline: {clip_count}")

    return {
        "project_json": project_json,
        "project_mlt": project_mlt,
        "project_kdenlive": project_kdenlive,
        "tracks": track_count,
        "clips": clip_count,
    }


def render(mlt_path: str, output_path: str, width: int = 1080, height: int = 1920,
           quality_args: list = None, audio_bitrate: str = "192k",
           timeout: int = 600) -> dict:
    """Render an MLT project to video.

    Args:
        quality_args: List of codec quality params (e.g. ["crf=18", "preset=slow"]).
                      Defaults to ["b=8000k"] if not provided.

    Returns dict with output path and file size.
    """
    from cli_anything.kdenlive.utils.melt_backend import render_mlt

    if quality_args is None:
        quality_args = ["b=8000k"]

    extra = [
        f"s={width}x{height}",
        f"width={width}",
        f"height={height}",
        "progressive=1",
        "sample_aspect_num=1",
        "sample_aspect_den=1",
        "r=50",
        "frame_rate_num=50",
        "frame_rate_den=1",
        f"ab={audio_bitrate}",
        "ar=48000",
        "channels=2",
        "pix_fmt=yuv420p",
    ]
    extra.extend(quality_args)

    result = render_mlt(
        mlt_path,
        output_path,
        vcodec="libx264",
        acodec="aac",
        overwrite=True,
        timeout=timeout,
        extra_args=extra,
    )
    print(f"Rendered: {result['output']} ({result['file_size']} bytes)")

    # Verify output dimensions
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", output_path],
        capture_output=True, text=True
    )
    if probe.stdout.strip():
        dims = probe.stdout.strip().split(",")
        if len(dims) == 2:
            w, h = int(dims[0]), int(dims[1])
            ratio = w / h
            if abs(ratio - 9/16) > 0.01:
                print(f"WARNING: Output aspect ratio {ratio:.4f} != 9:16 (0.5625). Actual: {w}x{h}")

    # Post-render duration
    actual_dur = get_media_duration(output_path)
    if actual_dur > 0:
        print(f"Render duration: {actual_dur:.1f}s")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assemble_video.py <config.json> [--render-draft|--render-final|--validate-only|--check-render <video>]")
        sys.exit(2)

    config_path = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "--assemble"

    if action == "--validate-only":
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        strict = "--strict" in sys.argv
        issues = validate_config(cfg, strict=strict)

        for severity, code, msg in issues:
            print(f"[{severity}] {code}: {msg}")

        errors = [i for i in issues if i[0] == "ERROR"]
        warnings = [i for i in issues if i[0] == "WARNING"]
        fatal = errors + warnings if strict else errors

        if fatal:
            print(f"\nVALIDATION FAILED: {len(fatal)} issue(s)")
            sys.exit(1)
        else:
            print(f"\nVALIDATION PASSED ({len(warnings)} warning(s))")
            sys.exit(0)

    elif action == "--check-render":
        video_path = sys.argv[3] if len(sys.argv) > 3 else None
        if not video_path:
            print("Usage: assemble_video.py <config.json> --check-render <video.mp4>")
            sys.exit(2)
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        audio_dur = get_media_duration(cfg.get("audio", ""))
        clips_dur = sum(c.get("duration", 0) for c in cfg.get("clips", []))
        expected = max(audio_dur, clips_dur)
        issues = validate_render(video_path, expected)

        for severity, code, msg in issues:
            print(f"[{severity}] {code}: {msg}")

        errors = [i for i in issues if i[0] == "ERROR"]
        if errors:
            print(f"\nRENDER CHECK FAILED: {len(errors)} issue(s)")
            sys.exit(1)
        else:
            print(f"\nRENDER CHECK PASSED")
            sys.exit(0)

    elif action == "--render-draft":
        # Render draft at reduced quality
        with open(config_path, 'r') as f:
            config = json.load(f)
        mlt_path = os.path.join(config["project_folder"], "project.mlt")
        draft_path = os.path.join(config["project_folder"], "draft.mp4")
        render(mlt_path, draft_path, width=540, height=960,
               quality_args=["b=1000k"], audio_bitrate="128k", timeout=300)
    elif action == "--render-final":
        # Render final at full quality
        with open(config_path, 'r') as f:
            config = json.load(f)
        mlt_path = os.path.join(config["project_folder"], "project.mlt")
        slug = os.path.basename(config["project_folder"])
        final_path = os.path.join(config["project_folder"], f"{slug}_final.mp4")
        render(mlt_path, final_path, width=1080, height=1920,
               quality_args=["crf=18", "preset=slow", "vb=0",
                             "maxrate=8000k", "bufsize=16000k"],
               audio_bitrate="192k", timeout=600)
    else:
        assemble(config_path)
