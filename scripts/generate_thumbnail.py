#!/usr/bin/env python3
"""Generate video thumbnails with text overlay using Pillow.

Usage:
    python3 generate_thumbnail.py <background_image> <title> [--output path] [--layout bottom|center] [--overlay 0-100]
    python3 generate_thumbnail.py --video <video.mp4> <title> [--timestamp 1.0] [--output path]

Creates a 1080x1920 (9:16) thumbnail with:
- Background image (resized/center-cropped to fit)
- Dark overlay for text readability
- Uppercase title with black outline + drop shadow
- Auto-sized font to fit within safe zone
"""
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


# --- Defaults ---
DEFAULT_SIZE = (1080, 1920)
DEFAULT_LAYOUT = "center"
DEFAULT_OVERLAY_OPACITY = 50  # percent
DEFAULT_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FALLBACK_FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MAX_FONT_SIZE = 120
MIN_FONT_SIZE = 60
TEXT_COLOR = (255, 215, 0)       # Gold #FFD700
OUTLINE_COLOR = (0, 0, 0)
OUTLINE_WIDTH = 7
SHADOW_OFFSET = 4
SHADOW_COLOR = (0, 0, 0, 128)
SAFE_MARGIN = 0.10  # 10% margin on each side


def get_font(size, font_path=None):
    """Load a TrueType font, falling back to defaults."""
    paths = [font_path, DEFAULT_FONT_PATH, FALLBACK_FONT_PATH]
    for p in paths:
        if p and os.path.isfile(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def load_and_resize_background(image_path, target_size):
    """Load image and center-crop to fill target size."""
    img = Image.open(image_path).convert("RGB")
    tw, th = target_size
    iw, ih = img.size
    target_ratio = tw / th
    img_ratio = iw / ih

    if abs(target_ratio - img_ratio) > 0.2:
        print(f"WARNING: Background aspect ratio ({img_ratio:.2f}) differs "
              f"significantly from target ({target_ratio:.2f}). Center-cropping.", file=sys.stderr)

    # Scale so the image fills the target (cover mode)
    if img_ratio > target_ratio:
        # Image is wider — scale by height, crop width
        scale = th / ih
        new_w = int(iw * scale)
        img = img.resize((new_w, th), Image.LANCZOS)
        left = (new_w - tw) // 2
        img = img.crop((left, 0, left + tw, th))
    else:
        # Image is taller — scale by width, crop height
        scale = tw / iw
        new_h = int(ih * scale)
        img = img.resize((tw, new_h), Image.LANCZOS)
        top = (new_h - th) // 2
        img = img.crop((0, top, tw, top + th))

    return img


def apply_vignette_overlay(image, opacity_pct):
    """Apply radial vignette gradient — dark edges, lighter center."""
    if opacity_pct <= 0:
        return image
    w, h = image.size
    max_alpha = opacity_pct / 100.0

    # Build radial gradient at reduced resolution for speed, then upscale
    scale = 4
    sw, sh = w // scale, h // scale
    cx, cy = sw / 2.0, sh / 2.0

    mask = Image.new("L", (sw, sh), 0)
    pixels = mask.load()
    for y_pos in range(sh):
        dy = (y_pos - cy) / cy
        dy2 = dy * dy
        for x_pos in range(sw):
            dx = (x_pos - cx) / cx
            dist = math.sqrt(dx * dx + dy2)
            # Smooth falloff: 0 at center, 1.0 at edges/corners
            t = min(dist / 1.1, 1.0)
            # Ease-in-out curve for natural vignette
            t = t * t * (3.0 - 2.0 * t)
            pixels[x_pos, y_pos] = int(255 * max_alpha * t)

    # Upscale mask with bilinear filtering for smooth gradient
    mask = mask.resize((w, h), Image.BILINEAR)

    # Composite: blend image with black using the mask
    black = Image.new("RGB", (w, h), (0, 0, 0))
    result = Image.composite(black, image.convert("RGB"), mask)
    return result


def punch_colors(image, saturation=1.3, contrast=1.15):
    """Boost saturation and contrast for punchier colors."""
    img = ImageEnhance.Color(image).enhance(saturation)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels. Returns list of lines."""
    words = text.split()
    lines = []
    current = []

    for word in words:
        test_line = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    return lines


def draw_text_with_outline(draw, xy, text, font, fill, outline_color, outline_width):
    """Draw text with outline by rendering offset copies."""
    x, y = xy
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # Draw main text
    draw.text(xy, text, font=font, fill=fill)


def render_title_text(image, title, layout="bottom", font_path=None):
    """Render title text with auto-sizing, outline, and shadow."""
    title = title.upper()
    w, h = image.size
    margin_x = int(w * SAFE_MARGIN)
    max_text_width = w - 2 * margin_x
    draw = ImageDraw.Draw(image)

    # Auto-size: find largest font that fits in safe zone
    font_size = MAX_FONT_SIZE
    font = get_font(font_size, font_path)
    lines = wrap_text(title, font, max_text_width, draw)

    while font_size > MIN_FONT_SIZE:
        if len(lines) <= 3:
            # Check total height fits in ~30% of canvas
            line_height = font_size * 1.3
            total_height = line_height * len(lines)
            if total_height < h * 0.30:
                break
        font_size -= 4
        font = get_font(font_size, font_path)
        lines = wrap_text(title, font, max_text_width, draw)

    line_height = int(font_size * 1.3)
    total_text_height = line_height * len(lines)

    # Calculate Y position
    if layout == "center":
        start_y = (h - total_text_height) // 2
    else:  # bottom
        start_y = int(h * 0.82) - total_text_height

    # Draw each line centered
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (w - text_w) // 2
        y = start_y + i * line_height

        # Shadow
        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), line,
                   font=font, fill=SHADOW_COLOR)
        # Outline + text
        draw_text_with_outline(draw, (x, y), line, font,
                                TEXT_COLOR, OUTLINE_COLOR, OUTLINE_WIDTH)

    return image


def extract_frame(video_path, timestamp=1.0):
    """Extract a single frame from video via ffmpeg. Returns temp PNG path."""
    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(timestamp), "-i", video_path,
             "-frames:v", "1", "-q:v", "2", tmp_path],
            capture_output=True, timeout=15, check=True
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"ERROR: Frame extraction failed: {e}", file=sys.stderr)
        os.unlink(tmp_path)
        sys.exit(1)
    return tmp_path


def generate_thumbnail(background_path, title, output_path=None,
                       size=None, layout=None, overlay_opacity=None,
                       font_path=None):
    """Main entry: create thumbnail from background + title. Returns output path."""
    size = size or DEFAULT_SIZE
    layout = layout or DEFAULT_LAYOUT
    overlay_opacity = overlay_opacity if overlay_opacity is not None else DEFAULT_OVERLAY_OPACITY

    if not output_path:
        base_dir = os.path.dirname(background_path)
        output_path = os.path.join(base_dir, "thumbnail.png")

    img = load_and_resize_background(background_path, size)
    img = punch_colors(img)
    img = apply_vignette_overlay(img, overlay_opacity)
    img = render_title_text(img, title, layout, font_path)
    img.save(output_path, quality=95)
    print(f"Generated: {output_path} ({size[0]}x{size[1]})")
    return output_path


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__, file=sys.stderr)
        sys.exit(0)

    # Parse arguments
    background = None
    title = None
    output = None
    layout = DEFAULT_LAYOUT
    overlay = DEFAULT_OVERLAY_OPACITY
    video = None
    timestamp = 1.0
    font_path = None

    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output = args[i + 1]; i += 2
        elif args[i] == "--layout" and i + 1 < len(args):
            layout = args[i + 1]; i += 2
        elif args[i] == "--overlay" and i + 1 < len(args):
            overlay = int(args[i + 1]); i += 2
        elif args[i] == "--video" and i + 1 < len(args):
            video = args[i + 1]; i += 2
        elif args[i] == "--timestamp" and i + 1 < len(args):
            timestamp = float(args[i + 1]); i += 2
        elif args[i] == "--font" and i + 1 < len(args):
            font_path = args[i + 1]; i += 2
        else:
            positional.append(args[i]); i += 1

    if video:
        # --video mode: extract frame, then use as background
        if len(positional) < 1:
            print("Usage: generate_thumbnail.py --video <video.mp4> <title> [--output ...]",
                  file=sys.stderr)
            sys.exit(1)
        title = positional[0]
        if not output:
            output = os.path.join(os.path.dirname(video), "thumbnail.png")
        background = extract_frame(video, timestamp)
        generate_thumbnail(background, title, output, layout=layout,
                           overlay_opacity=overlay, font_path=font_path)
        os.unlink(background)  # cleanup temp frame
    else:
        # Direct image mode
        if len(positional) < 2:
            print("Usage: generate_thumbnail.py <background_image> <title> [--output ...]",
                  file=sys.stderr)
            sys.exit(1)
        background = positional[0]
        title = positional[1]
        if not os.path.isfile(background):
            print(f"ERROR: Image not found: {background}", file=sys.stderr)
            sys.exit(1)
        generate_thumbnail(background, title, output, layout=layout,
                           overlay_opacity=overlay, font_path=font_path)


if __name__ == "__main__":
    main()
