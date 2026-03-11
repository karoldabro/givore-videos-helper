# CLI-Anything-Kdenlive Tool

## Location
`/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/`

## Purpose
Python library for programmatically creating Kdenlive projects via JSON → MLT XML pipeline.

## Architecture
```
cli_anything/kdenlive/
├── core/
│   ├── project.py      # open_project(), save_project()
│   ├── bin.py           # import_clip(), list_clips() — media bin management
│   ├── timeline.py      # add_track(), add_clip_to_track() — timeline operations
│   ├── subtitles.py     # add_subtitle_track(), import_srt(), import_ass(), parse_ass_styles()
│   └── filters.py       # add_filter() — volume, effects
├── utils/
│   ├── mlt_xml.py       # build_mlt_xml() — JSON project → MLT XML generation
│   └── melt_backend.py  # render_mlt() — melt rendering wrapper
└── tests/               # 155 tests, pytest
```

## Key Functions

### mlt_xml.py
- `build_mlt_xml(project)` — Main entry: converts project dict → complete MLT XML string
- `_build_title_xml(text, font, size, color, ...)` — Generates kdenlivetitle inline XML for subtitles
- `_hex_to_rgba_str(hex_color)` — Converts `#RRGGBB` → `R,G,B,255` for kdenlivetitle
- `_hex_to_mlt_color(hex_color)` — Converts `#RRGGBB` → `0xRRGGBBff` for other MLT uses
- `seconds_to_frames(seconds, fps_num, fps_den)` — Time to frame conversion

### subtitles.py
- `add_subtitle_track(project)` — Creates subtitle track with default style
- `import_srt(project, track_id, path)` — Imports .srt subtitles
- `import_ass(project, track_id, path)` — Imports .ass subtitles
- `parse_ass_styles(ass_path)` — Parses ASS [V4+ Styles] → dict of style properties
- `set_track_style(project, track_id, **kwargs)` — Sets track default style
- `_ass_color_to_hex(ass_color)` — Converts ASS `&HAABBGGRR` (BGR) → `#RRGGBB`

### assemble_video.py (in givore/scripts/)
- `assemble(config_path)` — Full assembly: template → import → tracks → clips → subtitles → MLT
- `render(mlt_path, output_path, ...)` — Renders MLT to video via melt

## Running Tests
```bash
cd /media/kdabrow/Programy/cli-anything-kdenlive/agent-harness
.venv/bin/python3 -m pytest cli_anything/kdenlive/tests/ -x -q
```

## Project JSON Format
The intermediate format between user config and MLT XML:
- `profile`: width, height, fps_num, fps_den, dar_num, dar_den
- `bin`: array of clip objects (id, source, name, type, duration)
- `tracks`: array of track objects (id, name, type, clips[], style{} for subtitles)
- `transitions`: manual transitions
- `guides`: timeline markers
