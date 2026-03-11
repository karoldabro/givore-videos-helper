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
import sys

# Add cli-anything-kdenlive to path
CLI_HARNESS = "/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness"
sys.path.insert(0, CLI_HARNESS)

from cli_anything.kdenlive.core import project as proj_mod
from cli_anything.kdenlive.core import bin as bin_mod
from cli_anything.kdenlive.core import timeline as tl_mod
from cli_anything.kdenlive.core import subtitles as sub_mod
from cli_anything.kdenlive.core import filters as filt_mod
from cli_anything.kdenlive.utils.mlt_xml import build_mlt_xml


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

    # Step 3: Import video clips to bin
    for clip_info in config.get("clips", []):
        bin_mod.import_clip(
            proj,
            source=clip_info["file"],
            name=clip_info.get("name", None),
            clip_type="video",
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

    # Step 7: Place video clips on V1
    bin_clips = bin_mod.list_clips(proj)
    video_clips = [c for c in bin_clips if c["type"] == "video"]

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

    # Step 8: Place narration on A1
    narration_clips = [c for c in bin_clips if c["name"] == "narration"]
    if narration_clips:
        narration = narration_clips[0]
        tl_mod.add_clip_to_track(
            proj, a_track["id"], narration["id"],
            position=0.0,
            in_point=0.0,
            out_point=narration["duration"],
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
            # Set volume
            volume = sfx_info.get("volume", 0.4)
            clip_idx = len([c for c in proj["tracks"]
                           if c["id"] == sfx_track["id"]][0]["clips"]) - 1
            filt_mod.add_filter(proj, sfx_track["id"], clip_idx, "volume",
                                params={"gain": str(volume)})

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

    # Summary
    track_count = len(proj.get("tracks", []))
    clip_count = sum(len(t.get("clips", [])) for t in proj.get("tracks", []))
    print(f"Project assembled: {project_json}")
    print(f"MLT XML exported: {project_mlt}")
    print(f"Tracks: {track_count}, Clips on timeline: {clip_count}")

    return {
        "project_json": project_json,
        "project_mlt": project_mlt,
        "tracks": track_count,
        "clips": clip_count,
    }


def render(mlt_path: str, output_path: str, width: int = 1080, height: int = 1920,
           bitrate: str = "8000k", audio_bitrate: str = "192k", timeout: int = 600) -> dict:
    """Render an MLT project to video.

    Returns dict with output path and file size.
    """
    from cli_anything.kdenlive.utils.melt_backend import render_mlt

    result = render_mlt(
        mlt_path,
        output_path,
        vcodec="libx264",
        acodec="aac",
        overwrite=True,
        timeout=timeout,
        extra_args=[f"width={width}", f"height={height}", f"b={bitrate}", f"ab={audio_bitrate}", "ar=48000", "channels=2"],
    )
    print(f"Rendered: {result['output']} ({result['file_size']} bytes)")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assemble_video.py <config.json> [--render-draft|--render-final]")
        sys.exit(1)

    config_path = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "--assemble"

    if action == "--render-draft":
        # Render draft at reduced quality
        with open(config_path, 'r') as f:
            config = json.load(f)
        mlt_path = os.path.join(config["project_folder"], "project.mlt")
        draft_path = os.path.join(config["project_folder"], "draft.mp4")
        render(mlt_path, draft_path, width=540, height=960, bitrate="1000k",
               audio_bitrate="128k", timeout=300)
    elif action == "--render-final":
        # Render final at full quality
        with open(config_path, 'r') as f:
            config = json.load(f)
        mlt_path = os.path.join(config["project_folder"], "project.mlt")
        slug = os.path.basename(config["project_folder"])
        final_path = os.path.join(config["project_folder"], f"{slug}_final.mp4")
        render(mlt_path, final_path, width=1080, height=1920, bitrate="8000k",
               audio_bitrate="192k", timeout=600)
    else:
        assemble(config_path)
