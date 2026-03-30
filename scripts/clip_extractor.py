#!/usr/bin/env python3
"""
clip_extractor.py — Automated interesting-moment detection and clip extraction
for cycling POV footage. Uses CLIP + YOLO + optical flow to find and extract
2-5 second clips, outputting bulk-add compatible JSON for givore_db.py.

Usage:
    python3 scripts/clip_extractor.py <video> --location <name> [options]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
from scipy.signal import find_peaks

GIVORE_ROOT = Path(__file__).resolve().parent.parent
CLIPS_DIR = GIVORE_ROOT / "videos" / "clips"
DEFAULT_CONFIG = GIVORE_ROOT / "scripts" / "clip_extractor_config.json"
DEFAULT_REVIEW_JSON = Path("/tmp/clip_extractor_results.json")
LRF_EXTENSION = ".LRF"  # DJI low-res proxy


def find_proxy(video_path):
    """Find DJI LRF proxy file matching the video."""
    proxy = video_path.with_suffix(LRF_EXTENSION)
    if proxy.exists():
        return proxy
    proxy = video_path.with_suffix(LRF_EXTENSION.lower())
    if proxy.exists():
        return proxy
    return None


# YOLO COCO class names relevant for scoring
TRAFFIC_CLASSES = {"car", "truck", "bus", "motorcycle", "traffic light"}
INTEREST_BONUS_DEFAULTS = {
    "person": 0.10, "bicycle": 0.05, "dog": 0.15, "cat": 0.15,
    "potted plant": 0.05, "bench": 0.05, "chair": 0.08, "couch": 0.10,
}


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def get_video_duration(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(video_path)],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def extract_frames(video_path, fps, output_dir, start_time=0, end_time=0):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(output_dir / "frame_%06d.jpg")
    cmd = ["ffmpeg"]
    if start_time > 0:
        cmd += ["-ss", str(start_time)]
    if end_time > 0 and end_time > start_time:
        cmd += ["-to", str(end_time)]
    cmd += ["-i", str(video_path), "-vf", f"fps={fps}",
            "-q:v", "2", "-hide_banner", "-loglevel", "warning", pattern]
    subprocess.run(cmd, check=True)
    frames = sorted(output_dir.glob("frame_*.jpg"))
    return frames


def compute_motion_scores(frame_paths, verbose=False):
    """Compute optical flow magnitude between consecutive frames."""
    scores = []
    prev_gray = None
    for i, fp in enumerate(frame_paths):
        img = cv2.imread(str(fp))
        if img is None:
            scores.append(0.0)
            continue
        # Downscale for speed
        small = cv2.resize(img, (320, 568))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                pyr_scale=0.5, levels=3, winsize=15,
                iterations=3, poly_n=5, poly_sigma=1.2, flags=0
            )
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            scores.append(float(mag.mean()))
        else:
            scores.append(0.0)
        prev_gray = gray
        if verbose and (i + 1) % 100 == 0:
            print(f"  Motion: {i+1}/{len(frame_paths)} frames", flush=True)
    arr = np.array(scores)
    if arr.max() > 0:
        arr = arr / arr.max()
    return arr


def run_yolo_detection(frame_paths, config, device="cuda", batch_size=8, verbose=False):
    """Run YOLO object detection on frames. Returns list of per-frame dicts."""
    import torch
    from ultralytics import YOLO

    model_name = config.get("models", {}).get("yolo", "yolov8n.pt")
    model = YOLO(model_name)
    model.to(device)

    results_list = []
    for i in range(0, len(frame_paths), batch_size):
        batch = [str(fp) for fp in frame_paths[i:i+batch_size]]
        results = model(batch, verbose=False, device=device)
        for r in results:
            labels = []
            counts = {}
            if r.boxes is not None:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = r.names[cls_id]
                    labels.append(label)
                    counts[label] = counts.get(label, 0) + 1
            results_list.append({"labels": labels, "counts": counts})
        if verbose and (i + batch_size) % (batch_size * 10) == 0:
            print(f"  YOLO: {min(i+batch_size, len(frame_paths))}/{len(frame_paths)} frames", flush=True)

    # Cleanup GPU
    del model
    torch.cuda.empty_cache()
    return results_list


def run_clip_scoring(frame_paths, text_queries, config, device="cuda", batch_size=4, verbose=False):
    """Run CLIP scoring against text queries. Returns scores dict + embeddings."""
    import torch
    import open_clip

    model_name = config.get("models", {}).get("clip_model", "ViT-L-14")
    pretrained = config.get("models", {}).get("clip_pretrained", "openai")

    model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
    model = model.to(device)
    model.eval()
    tokenizer = open_clip.get_tokenizer(model_name)

    # Encode text queries once
    query_names = list(text_queries.keys())
    query_texts = list(text_queries.values())
    with torch.no_grad():
        text_tokens = tokenizer(query_texts).to(device)
        text_features = model.encode_text(text_tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # Encode images in batches
    from PIL import Image
    all_scores = {name: [] for name in query_names}
    all_embeddings = []

    for i in range(0, len(frame_paths), batch_size):
        batch_paths = frame_paths[i:i+batch_size]
        images = []
        for fp in batch_paths:
            try:
                img = Image.open(fp).convert("RGB")
                images.append(preprocess(img))
            except Exception:
                images.append(torch.zeros(3, 224, 224))

        batch_tensor = torch.stack(images).to(device)
        with torch.no_grad():
            img_features = model.encode_image(batch_tensor)
            img_features = img_features / img_features.norm(dim=-1, keepdim=True)
            similarities = (img_features @ text_features.T).cpu().numpy()
            all_embeddings.append(img_features.cpu().numpy())

        for j, name in enumerate(query_names):
            all_scores[name].extend(similarities[:, j].tolist())

        if verbose and (i + batch_size) % (batch_size * 10) == 0:
            print(f"  CLIP: {min(i+batch_size, len(frame_paths))}/{len(frame_paths)} frames", flush=True)

    # Convert to numpy
    for name in query_names:
        all_scores[name] = np.array(all_scores[name])

    embeddings = np.concatenate(all_embeddings, axis=0)

    # Cleanup GPU
    del model
    torch.cuda.empty_cache()

    return all_scores, embeddings


def compute_diversity_scores(embeddings):
    """Cosine distance between consecutive CLIP embeddings."""
    if len(embeddings) < 2:
        return np.zeros(len(embeddings))
    # Embeddings are already normalized
    dots = np.sum(embeddings[:-1] * embeddings[1:], axis=-1)
    distances = 1.0 - dots
    # Pad to match frame count
    return np.concatenate([[0.0], distances])


def compute_object_interest(yolo_results, config):
    """Score each frame based on detected objects."""
    obj_config = config.get("object_scoring", {})
    bonus_map = obj_config.get("bonus", INTEREST_BONUS_DEFAULTS)
    bonus_cap = obj_config.get("bonus_cap", 0.4)
    penalty_traffic = obj_config.get("penalty_traffic_only", -0.1)
    penalty_empty = obj_config.get("penalty_empty", -0.2)

    scores = []
    for det in yolo_results:
        counts = det["counts"]
        if not counts:
            scores.append(max(0.0, 0.5 + penalty_empty))
            continue

        score = 0.0
        has_non_traffic = False
        for label, count in counts.items():
            if label in bonus_map:
                score += min(bonus_map[label] * count, 0.3)
                has_non_traffic = True
            elif label not in TRAFFIC_CLASSES:
                has_non_traffic = True

        if not has_non_traffic and any(l in TRAFFIC_CLASSES for l in counts):
            score += penalty_traffic

        scores.append(0.5 + min(score, bonus_cap))

    arr = np.array(scores)
    if arr.max() > 0:
        arr = arr / arr.max()
    return arr


def compute_composite_scores(motion, clip_scores, diversity, object_interest, weights, fps, window_seconds=3):
    """Combine all signals into a single composite score per frame."""
    n_frames = len(motion)
    w = weights

    # Best CLIP query score per frame
    clip_max = np.zeros(n_frames)
    for name, scores in clip_scores.items():
        valid_len = min(len(scores), n_frames)
        clip_max[:valid_len] = np.maximum(clip_max[:valid_len], scores[:valid_len])

    # Normalize CLIP to 0-1
    if clip_max.max() > clip_max.min():
        clip_max = (clip_max - clip_max.min()) / (clip_max.max() - clip_max.min())

    # Motion: more motion = better score (stabilized camera, no jitter concern)
    motion_quality = motion

    # Normalize diversity
    div = diversity[:n_frames] if len(diversity) >= n_frames else np.pad(diversity, (0, n_frames - len(diversity)))
    if div.max() > 0:
        div = div / div.max()

    obj = object_interest[:n_frames] if len(object_interest) >= n_frames else np.pad(object_interest, (0, n_frames - len(object_interest)))

    # Weighted combination
    composite = (
        w.get("motion", 0.2) * motion_quality +
        w.get("clip_interest", 0.35) * clip_max +
        w.get("diversity", 0.2) * div +
        w.get("objects", 0.25) * obj
    )

    # Smooth with sliding window
    window = int(window_seconds * fps)
    if window > 1 and len(composite) > window:
        kernel = np.ones(window) / window
        composite = np.convolve(composite, kernel, mode="same")

    return composite


def find_clip_candidates(composite, fps, min_duration, max_duration, top_percent, min_gap=3.0):
    """Find peaks in composite score and define clip boundaries."""
    min_distance = max(int(min_duration * fps), 1)
    peak_indices, properties = find_peaks(
        composite,
        distance=min_distance,
        prominence=0.05,
        height=0.2
    )

    if len(peak_indices) == 0:
        return []

    # Rank by score, keep top percent
    scores_at_peaks = composite[peak_indices]
    n_keep = max(1, int(len(peak_indices) * top_percent / 100))
    top_indices = np.argsort(scores_at_peaks)[::-1][:n_keep]
    top_peaks = sorted(peak_indices[top_indices])

    # Convert to time-based candidates
    candidates = []
    half_min = min_duration / 2
    half_max = max_duration / 2

    for peak in top_peaks:
        center_sec = peak / fps
        start = max(0, center_sec - half_max)
        end = center_sec + half_max
        duration = end - start

        # Clamp duration
        if duration < min_duration:
            end = start + min_duration
        if duration > max_duration:
            end = start + max_duration

        # Check overlap with previous
        if candidates and start < candidates[-1]["end_sec"] + min_gap:
            continue

        candidates.append({
            "start_sec": round(start, 2),
            "end_sec": round(end, 2),
            "duration": round(end - start, 2),
            "score": round(float(composite[peak]), 4),
            "peak_frame": int(peak),
        })

    return candidates


def get_top_queries(clip_scores, peak_frame, n=2):
    """Find the top N CLIP text queries at the peak frame."""
    scored = []
    for name, scores in clip_scores.items():
        if peak_frame < len(scores):
            scored.append((name, float(scores[peak_frame])))
    scored.sort(key=lambda x: -x[1])
    return scored[:n]


def map_to_givore_metadata(candidate, yolo_results, clip_scores, motion_scores, fps, location, clip_index, total_frames=0, config=None):
    """Map detection results to Givore style/mood/sections with rich descriptions."""
    peak = candidate["peak_frame"]
    start_frame = max(0, int(candidate["start_sec"] * fps))
    end_frame = min(len(motion_scores), int(candidate["end_sec"] * fps))

    # Top CLIP queries
    top_queries = get_top_queries(clip_scores, peak)
    dominant_query = top_queries[0][0] if top_queries else "general"
    secondary_query = top_queries[1][0] if len(top_queries) > 1 else None

    # Aggregate YOLO detections in clip range
    all_labels = {}
    for i in range(start_frame, min(end_frame + 1, len(yolo_results))):
        for label, count in yolo_results[i]["counts"].items():
            all_labels[label] = all_labels.get(label, 0) + count

    # Average motion in clip range
    clip_motion = motion_scores[start_frame:end_frame + 1]
    avg_motion = float(clip_motion.mean()) if len(clip_motion) > 0 else 0.5

    # --- Motion tag and type prefix ---
    _config = config if config is not None else {}
    motion_tag = compute_motion_tag(motion_scores, start_frame, end_frame, _config)
    type_prefix = assign_type_prefix(
        motion_scores, start_frame, end_frame,
        total_frames, yolo_results, _config
    )

    # --- Style mapping ---
    style = "cycling_pov"
    if dominant_query in ("landmark", "architecture", "plaza"):
        style = "landmark"
    elif dominant_query == "park":
        style = "cycling_path"
    elif "chair" in all_labels or "couch" in all_labels or "bed" in all_labels:
        style = "item_shot"
    elif dominant_query == "street_art":
        style = "landmark"

    # --- Mood mapping ---
    mood = "calm"
    total_objects = sum(all_labels.values())
    n_people = all_labels.get("person", 0)
    if avg_motion > 0.6 and total_objects > 3:
        mood = "energetic"
    elif avg_motion > 0.7:
        mood = "energetic"
    elif style == "landmark" or dominant_query == "street_art":
        mood = "dramatic"
    elif n_people > 3 and avg_motion < 0.4:
        mood = "playful"

    # --- Sections mapping (type_prefix overrides style-based defaults) ---
    if type_prefix == "item":
        sections = ["body", "item"]
    elif type_prefix == "hook":
        sections = ["hook"]
    elif type_prefix == "end":
        sections = ["end"]
    elif type_prefix == "start":
        sections = ["start"]
    elif type_prefix == "bridge":
        sections = ["bridge"]
    elif style == "landmark":
        sections = ["body", "importance"]
    elif style == "item_shot":
        sections = ["body", "item"]
    else:
        sections = ["body"]

    # --- Rich description ---
    # Scene descriptor from CLIP
    scene_descs = {
        "landmark": ["past landmark building", "near historic facade", "alongside monument", "past ornate building"],
        "street_life": ["on busy street", "through crowded sidewalk", "past shops and cafes", "along commercial street"],
        "park": ["through green park", "along tree-lined path", "past garden area", "through shaded avenue"],
        "architecture": ["past architecture", "along building facades", "through old quarter", "past urban structures"],
        "street_art": ["past street art", "near colorful mural", "past graffiti wall", "along painted facade"],
        "dynamic_cycling": ["through narrow street", "on fast descent", "around sharp turn", "through tight lane"],
        "plaza": ["across open plaza", "through city square", "across public space", "past fountain area"],
        "waterfront": ["along waterfront", "beside the river", "along canal path", "past marina area"],
    }
    variants = scene_descs.get(dominant_query, ["on street"])
    scene = variants[clip_index % len(variants)]

    # Motion descriptor — omit "cycling" since ALL clips are cycling POV
    motion_desc = ""

    # Object context (pick at most 1 to keep filenames short)
    # Note: YOLO counts accumulate across all frames in clip (2-5s * 2fps = 4-10 frames)
    # so thresholds must account for multi-frame accumulation
    n_frames = max(end_frame - start_frame + 1, 1)
    avg_people = n_people / n_frames
    obj_part = ""
    if avg_people > 4:
        obj_part = "crowded with people"
    elif all_labels.get("dog", 0) or all_labels.get("cat", 0):
        obj_part = "with animals"
    elif all_labels.get("bicycle", 0) > n_frames:
        obj_part = "with cyclists"
    elif avg_people > 1.5:
        obj_part = "with pedestrians"

    # Secondary scene hint (from 2nd CLIP query)
    secondary_hints = {
        "park": "near greenery",
        "street_life": "on lively area",
        "landmark": "near landmark",
        "architecture": "with facades",
        "plaza": "near open space",
        "waterfront": "near water",
        "street_art": "with art nearby",
    }

    # Build description
    desc = scene.strip()
    if obj_part:
        desc += " " + obj_part
    elif secondary_query and secondary_query != dominant_query:
        hint = secondary_hints.get(secondary_query)
        if hint:
            desc += " " + hint

    # Build filename with prefix and motion tag
    prefix_str = f"[{type_prefix}] " if type_prefix else ""
    filename = f"{prefix_str}({motion_tag}) {desc} - {location}.mp4"
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    # visual_hook derived from type_prefix
    is_visual_hook = type_prefix in ("hook",)

    return {
        "filename": filename,
        "sections": sections,
        "style": style,
        "mood": mood,
        "desc": desc,
        "visual_hook": is_visual_hook,
        "motion_tag": motion_tag,
        "type_prefix": type_prefix,
        "_dominant_query": dominant_query,
        "_secondary_query": secondary_query,
        "_score": candidate["score"],
        "_avg_motion": round(avg_motion, 3),
        "_objects": dict(sorted(all_labels.items(), key=lambda x: -x[1])[:5]),
    }


def compute_motion_tag(motion_scores, start_frame, end_frame, config):
    """Classify clip motion as dynamic/sharp/slow/calm from optical flow data."""
    clip_motion = motion_scores[start_frame:end_frame + 1]
    if len(clip_motion) == 0:
        return "calm"

    avg_motion = float(clip_motion.mean())
    motion_var = float(clip_motion.var()) if len(clip_motion) > 1 else 0.0

    thresholds = config.get("motion_descriptors", {})
    dynamic_t = thresholds.get("dynamic_threshold", 0.6)
    sharp_var_t = thresholds.get("sharp_variance_threshold", 0.15)
    sharp_min_t = thresholds.get("sharp_motion_min", 0.3)
    calm_t = thresholds.get("calm_threshold", 0.25)

    if avg_motion > dynamic_t:
        return "dynamic"
    elif motion_var > sharp_var_t and avg_motion > sharp_min_t:
        return "sharp"
    elif avg_motion < calm_t:
        return "calm"
    else:
        return "slow"


def assign_type_prefix(motion_scores, start_frame, end_frame,
                       total_frames, yolo_results, config):
    """Auto-assign [hook], [item], [end], [start], [bridge] prefix based on signals."""
    thresholds = config.get("type_prefix", {})

    # Gather signals
    clip_motion = motion_scores[start_frame:end_frame + 1]
    avg_motion = float(clip_motion.mean()) if len(clip_motion) > 0 else 0.5
    motion_var = float(clip_motion.var()) if len(clip_motion) > 1 else 0.0

    # YOLO labels in clip range
    furniture_classes = {"chair", "couch", "bed", "dining table", "tv",
                         "refrigerator", "oven", "microwave", "sink", "toilet"}
    all_labels = {}
    for i in range(start_frame, min(end_frame + 1, len(yolo_results))):
        for label, count in yolo_results[i]["counts"].items():
            all_labels[label] = all_labels.get(label, 0) + count

    has_furniture = bool(furniture_classes & set(all_labels.keys()))
    has_phone = all_labels.get("cell phone", 0) > 0

    end_pos_threshold = thresholds.get("end_position_threshold", 0.90)
    start_pos_threshold = thresholds.get("start_position_threshold", 0.08)
    hook_motion_threshold = thresholds.get("hook_motion_threshold", 0.55)
    bridge_var_threshold = thresholds.get("bridge_variance_threshold", 0.20)

    # Position in source video (0.0 to 1.0)
    position = (start_frame + end_frame) / 2 / max(total_frames, 1)

    # Priority-ordered decision tree
    # 1. Item detection (furniture + phone, or furniture + stopped)
    if has_furniture and has_phone:
        return "item"
    if has_furniture and avg_motion < 0.3:  # Stopped near furniture
        return "item"

    # 2. End clip (last portion + low motion)
    if position > end_pos_threshold and avg_motion < 0.2:
        return "end"

    # 3. Start clip (first portion)
    if position < start_pos_threshold:
        return "start"

    # 4. Bridge (high motion variance = direction change)
    if motion_var > bridge_var_threshold and avg_motion > 0.3:
        return "bridge"

    # 5. Hook (high motion + dynamic)
    if avg_motion > hook_motion_threshold and motion_var > 0.1:
        return "hook"

    # 6. Default: no prefix
    return ""


MOONDREAM_PYTHON = Path.home() / ".venv" / "moondream" / "bin" / "python3"

CAPTION_SCRIPT = '''
import torch, cv2, json, sys
from transformers import AutoModelForCausalLM
from PIL import Image

config = json.loads(sys.argv[1])
clips = json.loads(sys.argv[2])
length = config.get("caption_length", "short")
use_query = config.get("use_query", False)
query_prompt = config.get("query_prompt", "")

model = AutoModelForCausalLM.from_pretrained(
    config.get("model", "vikhyatk/moondream2"),
    revision=config.get("revision", "2025-01-09"),
    trust_remote_code=True, torch_dtype=torch.float16
).to("cuda")

results = []
for clip_path in clips:
    cap = cv2.VideoCapture(clip_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        results.append("")
        continue
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if use_query and query_prompt:
        try:
            answer = model.query(image, query_prompt)["answer"]
            results.append(answer)
        except (AttributeError, TypeError):
            caption = model.caption(image, length=length)["caption"]
            results.append(caption)
    else:
        caption = model.caption(image, length=length)["caption"]
        results.append(caption)

print(json.dumps(results))
'''


def caption_clips(extracted, config, device="cuda", verbose=False):
    """Use Moondream2 (separate venv) to generate real descriptions of extracted clips."""
    caption_config = config.get("captioning", {})

    if not MOONDREAM_PYTHON.exists():
        print("WARNING: Moondream venv not found, skipping captioning")
        return extracted

    clip_paths = [item["path"] for item in extracted]
    caption_config_json = json.dumps(caption_config)
    clips_json = json.dumps(clip_paths)

    result = subprocess.run(
        [str(MOONDREAM_PYTHON), "-c", CAPTION_SCRIPT, caption_config_json, clips_json],
        capture_output=True, text=True, timeout=600
    )

    if result.returncode != 0:
        print(f"WARNING: Captioning failed: {result.stderr[-200:]}")
        return extracted

    captions = json.loads(result.stdout.strip())

    for i, (item, caption) in enumerate(zip(extracted, captions)):
        if not caption:
            continue

        # Clean up caption for filename use
        caption_clean = caption.lower().strip().rstrip(".")
        # Truncate to ~150 chars (ext4 supports 255; prefix+suffix use ~50)
        if len(caption_clean) > 150:
            caption_clean = caption_clean[:150].rsplit(" ", 1)[0]
        caption_clean = re.sub(r'[<>:"/\\|?*]', '', caption_clean)
        caption_clean = re.sub(r'\s+', ' ', caption_clean).strip()

        meta = item["metadata"]
        location = meta["filename"].rsplit(" - ", 1)[-1].replace(".mp4", "")

        # Preserve type prefix and motion tag from metadata
        existing_prefix = meta.get("type_prefix", "")
        existing_motion = meta.get("motion_tag", "calm")
        prefix_str = f"[{existing_prefix}] " if existing_prefix else ""
        motion_str = f"({existing_motion}) "

        meta["desc"] = caption_clean
        new_filename = f"{prefix_str}{motion_str}{caption_clean} - {location}.mp4"

        # Rename the clip file
        old_path = Path(item["path"])
        new_path = old_path.parent / new_filename
        suffix = 0
        while new_path.exists() and new_path != old_path:
            suffix += 1
            new_path = old_path.parent / f"{prefix_str}{motion_str}{caption_clean} ({suffix}) - {location}.mp4"
        if new_path != old_path:
            old_path.rename(new_path)
            item["path"] = str(new_path)
            meta["filename"] = new_path.name

        if verbose:
            print(f"  {i+1}. {meta['filename']}")

    return extracted


def extract_clips(video_path, candidates, metadata_list, output_dir, config):
    """Extract clip segments from video using ffmpeg."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ext_config = config.get("clip_extraction", {})
    width = ext_config.get("width", 1080)
    height = ext_config.get("height", 1920)
    codec = ext_config.get("codec", "libx264")
    preset = ext_config.get("preset", "fast")
    crf = ext_config.get("crf", 18)

    extracted = []
    for i, (cand, meta) in enumerate(zip(candidates, metadata_list)):
        filename = meta["filename"]
        out_path = output_dir / filename

        # Handle collisions
        suffix = 0
        while out_path.exists():
            suffix += 1
            stem = filename.rsplit(".", 1)[0]
            out_path = output_dir / f"{stem} ({suffix}).mp4"

        no_audio = ext_config.get("no_audio", False)
        cmd = [
            "ffmpeg", "-ss", str(cand["start_sec"]),
            "-i", str(video_path),
            "-t", str(cand["duration"]),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", codec, "-preset", preset, "-crf", str(crf),
            "-pix_fmt", "yuv420p10le",
            "-tag:v", "hvc1",
        ]
        if no_audio:
            cmd.append("-an")
        else:
            cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        cmd.extend(["-hide_banner", "-loglevel", "warning",
                     "-y", str(out_path)])
        subprocess.run(cmd, check=True)

        meta["filename"] = out_path.name
        extracted.append({"path": str(out_path), "metadata": meta})

    return extracted


def generate_review_json(extracted, output_path):
    """Generate bulk-add compatible JSON for givore_db.py."""
    bulk_add = []
    for item in extracted:
        meta = item["metadata"]
        bulk_add.append({
            "filename": meta["filename"],
            "sections": meta["sections"],
            "style": meta["style"],
            "mood": meta["mood"],
            "desc": meta["desc"],
            "visual_hook": meta["visual_hook"],
            "type_prefix": meta.get("type_prefix", ""),
            "motion_tag": meta.get("motion_tag", "calm"),
        })

    with open(output_path, "w") as f:
        json.dump(bulk_add, f, indent=2, ensure_ascii=False)
    return bulk_add


def print_summary(extracted):
    """Print a human-readable summary of extracted clips."""
    print(f"\n{'='*60}")
    print(f"  Extracted {len(extracted)} clips")
    print(f"{'='*60}")
    for i, item in enumerate(extracted):
        meta = item["metadata"]
        score = meta.get("_score", 0)
        print(f"  {i+1:2d}. {meta['filename']}")
        print(f"      style={meta['style']} mood={meta['mood']} sections={meta['sections']} score={score:.3f}")
        if meta.get("_objects"):
            objs = ", ".join(f"{k}:{v}" for k, v in list(meta["_objects"].items())[:3])
            print(f"      objects: {objs}")
    print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract interesting clips from cycling POV footage"
    )
    parser.add_argument("video", help="Path to source video file")
    parser.add_argument("--location", required=True, help="Location name for clip filenames")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config JSON path")
    parser.add_argument("--fps", type=float, default=0, help="Frame extraction rate (0=auto)")
    parser.add_argument("--device", default="auto", help="torch device (auto/cuda/cpu)")
    parser.add_argument("--batch-size", type=int, default=8, help="Inference batch size")
    parser.add_argument("--min-duration", type=float, default=2.0, help="Min clip duration (seconds)")
    parser.add_argument("--max-duration", type=float, default=5.0, help="Max clip duration (seconds)")
    parser.add_argument("--top-percent", type=float, default=30, help="Keep top N%% of peaks")
    parser.add_argument("--min-gap", type=float, default=3.0, help="Min gap between clips (seconds)")
    parser.add_argument("--max-clips", type=int, default=0, help="Max clips to extract (0=no limit)")
    parser.add_argument("--output-dir", default=str(CLIPS_DIR), help="Output directory for clips")
    parser.add_argument("--review-json", default=str(DEFAULT_REVIEW_JSON), help="Review JSON output path")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, don't extract clips")
    parser.add_argument("--keep-frames", action="store_true", help="Don't delete extracted frames")
    parser.add_argument("--no-caption", action="store_true", help="Skip VLM captioning (use CLIP-based descriptions)")
    parser.add_argument("--no-proxy", action="store_true", help="Don't use LRF proxy even if available")
    parser.add_argument("--start-time", type=float, default=0, help="Start analysis from this timestamp in seconds (skip earlier footage)")
    parser.add_argument("--end-time", type=float, default=0, help="End analysis at this timestamp in seconds")
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate inputs
    video_path = Path(args.video).resolve()
    if not video_path.exists():
        print(f"Error: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("Error: ffmpeg and ffprobe must be installed", file=sys.stderr)
        sys.exit(1)

    config = load_config(args.config)

    # Device selection
    import torch
    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    print(f"Device: {device}")

    # Video duration and FPS
    duration = get_video_duration(video_path)
    duration_min = duration / 60
    print(f"Video: {video_path.name} ({duration_min:.1f} min)")

    # Check for LRF proxy
    analysis_path = video_path
    if not args.no_proxy:
        proxy = find_proxy(video_path)
        if proxy:
            print(f"Proxy: {proxy.name} (using for analysis, extracting from original)")
            analysis_path = proxy

    fps = args.fps
    if fps <= 0:
        threshold = config.get("frame_extraction", {}).get("fps_auto_threshold_minutes", 10)
        fps = config["frame_extraction"]["fps_long"] if duration_min > threshold else config["frame_extraction"]["fps_short"]
    print(f"FPS: {fps}")

    # Stage 1: Frame extraction (from proxy if available)
    t0 = time.time()
    frames_dir = tempfile.mkdtemp(prefix="clip_extractor_")
    start_time = args.start_time
    end_time = args.end_time
    if start_time > 0:
        print(f"Start time: {start_time:.1f}s ({start_time/60:.1f} min)")
    if end_time > 0:
        print(f"End time: {end_time:.1f}s ({end_time/60:.1f} min)")
    print(f"\n[1/7] Extracting frames at {fps} FPS from {analysis_path.name}...", end=" ", flush=True)
    frame_paths = extract_frames(analysis_path, fps, frames_dir, start_time=start_time, end_time=end_time)
    print(f"{len(frame_paths)} frames [{time.time()-t0:.1f}s]")

    if len(frame_paths) < 3:
        print("Error: Too few frames extracted. Check video file.", file=sys.stderr)
        sys.exit(1)

    # Stage 2: Motion analysis
    t1 = time.time()
    print("[2/7] Computing motion scores...", end=" ", flush=True)
    motion_scores = compute_motion_scores(frame_paths, verbose=args.verbose)
    print(f"[{time.time()-t1:.1f}s]")

    # Stage 3: YOLO object detection
    t2 = time.time()
    print(f"[3/7] Running YOLO detection (batch={args.batch_size}, device={device})...", end=" ", flush=True)
    yolo_results = run_yolo_detection(frame_paths, config, device=device, batch_size=args.batch_size, verbose=args.verbose)
    print(f"[{time.time()-t2:.1f}s]")

    # Stage 4: CLIP interest scoring
    t3 = time.time()
    text_queries = config.get("text_queries", {})
    clip_batch = max(2, args.batch_size // 2)  # CLIP needs smaller batches
    print(f"[4/7] Running CLIP scoring (batch={clip_batch}, device={device})...", end=" ", flush=True)
    clip_scores, embeddings = run_clip_scoring(frame_paths, text_queries, config, device=device, batch_size=clip_batch, verbose=args.verbose)
    print(f"[{time.time()-t3:.1f}s]")

    # Stage 5: Visual diversity
    t4 = time.time()
    print("[5/7] Computing visual diversity...", end=" ", flush=True)
    diversity_scores = compute_diversity_scores(embeddings)
    print(f"[{time.time()-t4:.1f}s]")

    # Stage 6: Combined scoring + peak detection
    t5 = time.time()
    weights = config.get("scoring", {}).get("weights", {})
    object_interest = compute_object_interest(yolo_results, config)
    composite = compute_composite_scores(motion_scores, clip_scores, diversity_scores, object_interest, weights, fps)
    candidates = find_clip_candidates(composite, fps, args.min_duration, args.max_duration, args.top_percent, args.min_gap)

    # Apply start-time offset to candidate timestamps
    if start_time > 0:
        for cand in candidates:
            cand["start_sec"] = round(cand["start_sec"] + start_time, 2)
            cand["end_sec"] = round(cand["end_sec"] + start_time, 2)

    # Filter out candidates beyond end-time
    if end_time > 0:
        candidates = [c for c in candidates if c["end_sec"] <= end_time]

    if args.max_clips > 0:
        candidates = candidates[:args.max_clips]

    print(f"[6/7] Scoring + peak detection... {len(candidates)} clips found [{time.time()-t5:.1f}s]")

    if not candidates:
        print("\nNo interesting moments detected. Try lowering --top-percent or check your video.")
        if not args.keep_frames:
            shutil.rmtree(frames_dir, ignore_errors=True)
        sys.exit(0)

    # Generate metadata for each candidate
    total_frames = len(frame_paths)
    metadata_list = []
    for i, cand in enumerate(candidates):
        meta = map_to_givore_metadata(
            cand, yolo_results, clip_scores, motion_scores, fps,
            args.location, i, total_frames=total_frames, config=config
        )
        metadata_list.append(meta)

    if args.dry_run:
        print(f"\n[DRY RUN] Would extract {len(candidates)} clips:")
        for i, (cand, meta) in enumerate(zip(candidates, metadata_list)):
            print(f"  {i+1}. {meta['filename']} ({cand['start_sec']:.1f}s-{cand['end_sec']:.1f}s, score={cand['score']:.3f})")
        # Still generate review JSON for inspection
        generate_review_json([{"path": "", "metadata": m} for m in metadata_list], args.review_json)
        print(f"\nReview JSON: {args.review_json}")
    else:
        # Stage 7: Extract clips
        t6 = time.time()
        print(f"[7/7] Extracting {len(candidates)} clips...", end=" ", flush=True)
        extracted = extract_clips(video_path, candidates, metadata_list, args.output_dir, config)
        print(f"[{time.time()-t6:.1f}s]")

        # Stage 8: VLM captioning
        if not args.no_caption:
            t7 = time.time()
            print(f"[8/8] Captioning {len(extracted)} clips with VLM...", end=" ", flush=True)
            extracted = caption_clips(extracted, config, device=device, verbose=args.verbose)
            print(f"[{time.time()-t7:.1f}s]")

        # Generate review JSON
        bulk = generate_review_json(extracted, args.review_json)
        print_summary(extracted)
        print(f"Clips saved to: {args.output_dir}")
        print(f"Review JSON:    {args.review_json}")
        print(f"Import:         python3 scripts/givore_db.py bulk-add {args.review_json}")

    # Cleanup
    if not args.keep_frames:
        shutil.rmtree(frames_dir, ignore_errors=True)

    total_time = time.time() - t0
    print(f"\nTotal time: {total_time:.1f}s ({total_time/60:.1f} min)")


if __name__ == "__main__":
    main()
