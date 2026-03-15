# MLT XML Technical Details for Kdenlive

## Key File
`/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/cli_anything/kdenlive/utils/mlt_xml.py`

## Profile (Vertical Video)
- Resolution: 1080x1920
- DAR: 9:16 (NOT 16:9 — that causes miniaturized video)
- SAR: 1:1 (computed as dar_num*height / dar_den*width)
- FPS: 50/1 (NOT 30 — clips are 50fps, template is 50fps)
- Template: `projects/template.kdenlive-cli.json`

## Video Track — hide="audio"
Video track entries in the tractor MUST have `hide="audio"` to mute ambient audio from video clips. Without this, ambient audio plays over narration creating noise.
```xml
<track producer="playlist0" hide="audio"/>
```

## Mix/Composite Transitions (Auto-Generated)
For multi-track playback, `build_mlt_xml()` auto-generates:
- **mix** transitions: make audio from all tracks audible (a_track=0, b_track=i)
- **frei0r.cairoblend** transitions: make video/subtitle tracks visible

## Subtitle System — kdenlivetitle

### Producer Structure
Subtitles use `kdenlivetitle` MLT service with inline XML in the `xmldata` property (NOT `resource`).
```xml
<producer id="sub0" in="0" out="59">
  <property name="mlt_service">kdenlivetitle</property>
  <property name="xmldata">[escaped title XML]</property>
  <property name="kdenlive:clip_type">4</property>
  <property name="length">60</property>
</producer>
```

### Color Format — RGBA Decimal (NOT Hex)
Kdenlive's kdenlivetitle uses **comma-separated RGBA decimal** format, NOT hex colors.
- **WRONG**: `font-color="#ffffff"` → renders as black
- **RIGHT**: `font-color="255,255,255,255"`

Helper function `_hex_to_rgba_str()` converts `#RRGGBB` → `R,G,B,255`.

### Font Size Attribute
Use `font-pixel-size` NOT `font-size`.
- **WRONG**: `font-size="65"`
- **RIGHT**: `font-pixel-size="65"`

### Text Alignment
Kdenlive alignment values: `4` = center (NOT `1`).
For centered subtitles: `alignment="4"` + `box-width="[frame_width-10]"` + `x="5"`.

### Outline Scaling
ASS outline values need 2x scaling for kdenlivetitle pixel rendering.
- ASS `Outline: 7` → kdenlivetitle `font-outline="14"`
- Real Kdenlive projects use `font-outline="13"` for similar visual result.

### Complete Content Tag Example (from real Kdenlive project)
```xml
<content alignment="4" box-width="1070" font="Arial" font-color="255,255,255,255"
  font-italic="0" font-outline="14" font-outline-color="43,93,39,255"
  font-pixel-size="65" font-underline="0" font-weight="700"
  letter-spacing="2" line-spacing="0" shadow="0;#64000000;3;3;3">
  Subtitle text here
</content>
```

### Title XML Structure
```xml
<kdenlivetitle width="1080" height="1920">
  <item type="QGraphicsTextItem" z-index="0">
    <position x="5" y="[y_pos]">
      <transform>1,0,0,0,1,0,0,0,1</transform>
    </position>
    <content ...>text</content>
  </item>
  <startviewport rect="0,0,1080,1920"/>
  <endviewport rect="0,0,1080,1920"/>
  <background color="0,0,0,0"/>
</kdenlivetitle>
```

## ASS Subtitle Parsing
- Colors: `&HAABBGGRR` format (BGR order) → convert to `#RRGGBB` via `_ass_color_to_hex()`
- Styles parsed from `[V4+ Styles]` section by `parse_ass_styles()` in `subtitles.py`
- MarginV from ASS used for vertical positioning: `y_pos = height - margin_v`

## Render Settings
- Draft: 540x960, bitrate 1000k, audio 128k
- Final: 1080x1920, bitrate 8000k, audio 192k
- Audio: `ar=48000 channels=2` (forced for clean audio)
- **CRITICAL**: Must include `r=50`, `frame_rate_num=50`, `frame_rate_den=1` in render extra_args — without these, melt defaults to 25fps causing 2x duration
- Flatpak melt needs `--filesystem=` flags for media access
