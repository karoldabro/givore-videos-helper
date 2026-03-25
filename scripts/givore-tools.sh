#!/usr/bin/env bash
# givore-tools.sh — Reusable CLI helpers for givore content pipelines
# Wraps ffprobe, assemble_video.py, subs, and batch operations
# so Claude Code can call one script instead of many individual commands.
set -euo pipefail

CLI_PYTHON="/media/kdabrow/Programy/cli-anything-kdenlive/agent-harness/.venv/bin/python3"
ASSEMBLY_SCRIPT="/media/kdabrow/Programy/givore/scripts/assemble_video.py"

usage() {
    cat <<'EOF'
givore-tools.sh <command> [args]

Media queries:
  duration <file>             Audio/video duration in seconds
  duration-all <project-dir>  Duration of all .mp3 in v1-v7 subdirs
  video-info <file>           Video dimensions (WxH) + duration
  video-info-all <project-dir> Video info for all drafts in v1-v7

Video pipeline:
  generate-config [args]      Generate assembly_config.json from audio + clip IDs
  assemble <config.json>      Assemble project (JSON -> project.json + .mlt)
  render-draft <config.json>  Assemble + render draft (540x960)
  render-final <config.json>  Assemble + render final (1080x1920)
  render-all <project-dir> [draft|final]  Render all v1-v7 variants
  assemble-all <project-dir>  Assemble all v1-v7 variants
  place-sfx [args]            DEPRECATED: SFX placement is now AI-driven (see SFX_GUIDELINES.md)

Quality checks:
  validate <config.json> [--strict]         Pre-flight validation (files, durations, paths)
  validate-all <project-dir> [--strict]    Validate all v1-v7 assembly configs
  check-render <config.json> <video.mp4>    Post-render validation (duration, aspect ratio)
  check-render-all <project-dir>           Post-render validation for all v1-v7

Subtitles & captions:
  subs <audio.mp3> <captions.txt> [output.srt]  Generate SRT from audio + captions
  captions <script.txt> [output.txt]  Generate 2-3 word/line captions from script
  batch-captions <project-dir>     Generate captions for all v1-v7 variants
  batch-subs <project-dir>         Generate subtitles for all v1-v7 variants

Audio:
  rename-audio <project-dir> <slug>  Rename tts_*.mp3 to <slug>.mp3 in all v1-v7

Project setup:
  init-project <slug>         Create project folder (projects/<slug>/)
  init-batch <slug>           Create batch folders (v1-v7)
  init-renueva <slug>         Create renueva project folder (projects/renueva-<slug>/)
  init-renueva-batch <slug> <N>  Create N variant folders for renueva batch

Thumbnails:
  thumbnail <image> <title> [output.png]    Generate thumbnail from image + title
  thumbnail-from-video <video> <title> [output.png] [timestamp]  Extract frame + generate thumbnail
  batch-thumbnails <project-dir>            Generate thumbnails for all v1-v7

Batch:
  batch-status <project-dir>  Show file status for all 7 variants

Clip extraction:
  extract-clips <video> --location <name> [opts]  Extract interesting clips from cycling POV video (CLIP+YOLO+motion)

Clip database:
  clips <subcommand> [args]   Clip DB operations (init, list, search, plan, sync, etc.)

History database:
  script-add [args]           Add script history entry
  script-list [--last N]      List recent script history
  script-rotation [--last N]  Show script rotation constraints
  script-delete <id>          Delete script history entry
  trial-add [args]            Add trial history entry
  trial-list [--last N]       List recent trial history
  trial-rotation [--last N]   Show trial rotation constraints
  trial-delete <id>           Delete trial history entry
  video-add [args]            Add video history entry
  video-list [--last N]       List recent video history
  video-recent-clips [--last N] Clips used in last N videos
  video-delete <id>           Delete video history entry
  renueva-add [args]          Add renueva history entry
  renueva-list [--last N]     List recent renueva history
  renueva-rotation [--last N] Show renueva rotation constraints
  renueva-delete <id>         Delete renueva history entry
  thumbnail-add [args]        Add thumbnail history entry
  thumbnail-list [--last N]   List recent thumbnail history
  thumbnail-recent-bgs [--last N] Backgrounds used in last N thumbnails
  thumbnail-delete <id>       Delete thumbnail history entry
  migrate-all                 Import all history MDs into DB
EOF
}

cmd_duration() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "ERROR: File not found: $file" >&2
        return 1
    fi
    ffprobe -v error -show_entries format=duration -of csv=p=0 "$file"
}

cmd_duration_all() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        for mp3 in "$vdir"/*.mp3; do
            [[ -f "$mp3" ]] || continue
            local dur
            dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$mp3" 2>/dev/null || echo "ERROR")
            printf "%-4s %-50s %s\n" "$v" "$(basename "$mp3")" "${dur}s"
        done
    done
}

cmd_video_info() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "ERROR: File not found: $file" >&2
        return 1
    fi
    local dims dur
    dims=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$file" 2>/dev/null || echo "ERROR")
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file" 2>/dev/null || echo "ERROR")
    echo "${dims} ${dur}s"
}

cmd_video_info_all() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi
    printf "%-4s %-40s %-12s %s\n" "VAR" "FILE" "DIMS" "DURATION"
    printf "%-4s %-40s %-12s %s\n" "---" "----" "----" "--------"
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        for mp4 in "$vdir"/draft.mp4 "$vdir"/*_final.mp4; do
            [[ -f "$mp4" ]] || continue
            local dims dur
            dims=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$mp4" 2>/dev/null || echo "?")
            dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$mp4" 2>/dev/null || echo "?")
            printf "%-4s %-40s %-12s %s\n" "$v" "$(basename "$mp4")" "$dims" "${dur}s"
        done
    done
}

cmd_assemble() {
    local config="$1"
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Config not found: $config" >&2
        return 1
    fi
    "$CLI_PYTHON" "$ASSEMBLY_SCRIPT" "$config"
}

cmd_render_draft() {
    local config="$1"
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Config not found: $config" >&2
        return 1
    fi
    "$CLI_PYTHON" "$ASSEMBLY_SCRIPT" "$config" --render-draft
}

cmd_render_final() {
    local config="$1"
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Config not found: $config" >&2
        return 1
    fi
    "$CLI_PYTHON" "$ASSEMBLY_SCRIPT" "$config" --render-final
}

cmd_render_all() {
    local project_dir="$1"
    local mode="${2:-draft}"
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local config="$project_dir/$v/assembly_config.json"
        [[ -f "$config" ]] || continue
        echo "=== $v: RENDER ($mode) ==="
        if [[ "$mode" == "final" ]]; then
            cmd_render_final "$config"
        else
            cmd_render_draft "$config"
        fi
        echo ""
    done
}

cmd_validate_all() {
    local project_dir="$1"
    shift
    local extra_args=("$@")
    local pass=0 fail=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local config="$project_dir/$v/assembly_config.json"
        [[ -f "$config" ]] || continue
        echo "=== $v ==="
        if cmd_validate "$config" "${extra_args[@]+"${extra_args[@]}"}"; then
            pass=$((pass + 1))
        else
            fail=$((fail + 1))
        fi
    done
    echo ""
    echo "Validate-all: $pass passed, $fail failed"
    [[ $fail -eq 0 ]]
}

cmd_assemble_all() {
    local project_dir="$1"
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local config="$project_dir/$v/assembly_config.json"
        [[ -f "$config" ]] || continue
        echo "=== $v: ASSEMBLE ==="
        cmd_assemble "$config"
        echo ""
    done
}

cmd_check_render_all() {
    local project_dir="$1"
    local pass=0 fail=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local config="$project_dir/$v/assembly_config.json"
        [[ -f "$config" ]] || continue
        # Auto-detect video: prefer _final.mp4, fall back to draft.mp4
        local video=""
        for candidate in "$project_dir/$v/"*_final.mp4 "$project_dir/$v/draft.mp4"; do
            [[ -f "$candidate" ]] && { video="$candidate"; break; }
        done
        [[ -z "$video" ]] && { echo "=== $v: SKIP (no video found) ==="; continue; }
        echo "=== $v: CHECK $(basename "$video") ==="
        if cmd_check_render "$config" "$video"; then
            pass=$((pass + 1))
        else
            fail=$((fail + 1))
        fi
    done
    echo ""
    echo "Check-render-all: $pass passed, $fail failed"
    [[ $fail -eq 0 ]]
}

cmd_subs() {
    local audio="$1"
    local captions="$2"
    local output="${3:-${audio%.*}.srt}"
    if [[ ! -f "$audio" ]]; then
        echo "ERROR: Audio not found: $audio" >&2
        return 1
    fi
    if [[ ! -f "$captions" ]]; then
        echo "ERROR: Captions not found: $captions" >&2
        return 1
    fi
    ~/.venv/aeneas/bin/python -m aeneas.tools.execute_task \
        "$audio" "$captions" \
        "task_language=spa|is_text_type=subtitles|os_task_file_format=srt" \
        "$output"
    echo "Created: $output"
}

cmd_batch_subs() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi
    local count=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        local mp3=""
        for f in "$vdir"/*.mp3; do
            [[ -f "$f" ]] && mp3="$f" && break
        done
        local caps="$vdir/captions.txt"
        if [[ -n "$mp3" && -f "$caps" ]]; then
            echo "=== $v: generating subtitles ==="
            cmd_subs "$mp3" "$caps"
            count=$((count + 1))
        fi
    done
    echo "Done: $count subtitle(s) generated"
}

cmd_rename_audio() {
    local dir="$1"
    local slug="$2"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi
    local count=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        local tts_files=()
        while IFS= read -r -d '' f; do
            tts_files+=("$f")
        done < <(find "$vdir" -maxdepth 1 -name "tts_*.mp3" -print0 2>/dev/null)
        if [[ ${#tts_files[@]} -eq 1 ]]; then
            mv "${tts_files[0]}" "$vdir/$slug.mp3"
            echo "$v: renamed $(basename "${tts_files[0]}") -> $slug.mp3"
            count=$((count + 1))
        elif [[ ${#tts_files[@]} -gt 1 ]]; then
            echo "$v: SKIPPED (multiple tts_*.mp3 found)" >&2
        fi
    done
    echo "Done: $count file(s) renamed"
}

cmd_captions() {
    local script_file="$1"
    local output="${2:-$(dirname "$script_file")/captions.txt}"
    if [[ ! -f "$script_file" ]]; then
        echo "ERROR: Script not found: $script_file" >&2
        return 1
    fi
    python3 "/media/kdabrow/Programy/givore/scripts/generate_captions.py" "$script_file" "$output"
}

cmd_batch_captions() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi
    local count=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        # Find script .txt (not captions/descriptions/clip_map)
        local script_file=""
        for f in "$vdir"/*.txt; do
            [[ -f "$f" ]] || continue
            local base
            base=$(basename "$f")
            if [[ "$base" != "captions.txt" && "$base" != "descriptions.txt" && "$base" != "clip_map.txt" ]]; then
                script_file="$f"
                break
            fi
        done
        if [[ -n "$script_file" ]]; then
            echo "=== $v: generating captions ==="
            cmd_captions "$script_file" "$vdir/captions.txt"
            count=$((count + 1))
        fi
    done
    echo "Done: $count caption file(s) generated"
}

GIVORE_PROJECTS="/media/kdabrow/Programy/givore/projects"

cmd_init_project() {
    local slug="$1"
    local dir="$GIVORE_PROJECTS/$slug"
    if [[ -d "$dir" ]]; then
        echo "Project already exists: $dir"
        return 0
    fi
    mkdir -p "$dir"
    echo "Created: $dir"
}

cmd_init_batch() {
    local slug="$1"
    local dir="$GIVORE_PROJECTS/$slug"
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        echo "Created: $dir"
    fi
    for v in v1 v2 v3 v4 v5 v6 v7; do
        mkdir -p "$dir/$v"
    done
    echo "Created: v1-v7 in $dir"
}

cmd_init_renueva() {
    local slug="$1"
    local dir="$GIVORE_PROJECTS/renueva-$slug"
    if [[ -d "$dir" ]]; then
        echo "Project already exists: $dir"
        return 0
    fi
    mkdir -p "$dir"
    echo "Created: $dir"
}

cmd_init_renueva_batch() {
    local slug="$1"
    local count="${2:-3}"
    local dir="$GIVORE_PROJECTS/renueva-$slug"
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        echo "Created: $dir"
    fi
    for i in $(seq 1 "$count"); do
        mkdir -p "$dir/v$i"
    done
    echo "Created: v1-v${count} in $dir"
}

cmd_thumbnail() {
    local image="$1"
    local title="$2"
    local output="${3:-$(dirname "$image")/thumbnail.png}"
    if [[ ! -f "$image" ]]; then
        echo "ERROR: Image not found: $image" >&2
        return 1
    fi
    python3 "/media/kdabrow/Programy/givore/scripts/generate_thumbnail.py" \
        "$image" "$title" --output "$output"
}

cmd_thumbnail_from_video() {
    local video="$1"
    local title="$2"
    local output="${3:-$(dirname "$video")/thumbnail.png}"
    local timestamp="${4:-1.0}"
    if [[ ! -f "$video" ]]; then
        echo "ERROR: Video not found: $video" >&2
        return 1
    fi
    python3 "/media/kdabrow/Programy/givore/scripts/generate_thumbnail.py" \
        --video "$video" --timestamp "$timestamp" "$title" --output "$output"
}

cmd_batch_thumbnails() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi

    # Collect background images from thumbnail/ library
    local thumb_dir="/media/kdabrow/Programy/givore/thumbnail"
    local -a all_images=()
    for img in "$thumb_dir"/*.png "$thumb_dir"/*.jpg "$thumb_dir"/*.jpeg; do
        [[ -f "$img" ]] && all_images+=("$img")
    done
    if [[ ${#all_images[@]} -eq 0 ]]; then
        echo "ERROR: No background images found in $thumb_dir/" >&2
        return 1
    fi

    # Get recently used backgrounds to avoid
    local -a avoid_bgs=()
    local avoid_output
    avoid_output=$(python3 "/media/kdabrow/Programy/givore/scripts/givore_db.py" thumbnail-recent-bgs --last 5 2>/dev/null || true)
    if [[ -n "$avoid_output" ]]; then
        while IFS=, read -ra items; do
            for item in "${items[@]}"; do
                item=$(echo "$item" | xargs)
                [[ -n "$item" ]] && avoid_bgs+=("$item")
            done
        done <<< "$(echo "$avoid_output" | grep '^ ' | head -1)"
    fi

    # Filter: prefer unused images, fall back to all if all recently used
    local -a images=()
    for img in "${all_images[@]}"; do
        local base
        base=$(basename "$img")
        local is_recent=false
        for ab in "${avoid_bgs[@]}"; do
            [[ "$base" == "$ab" ]] && { is_recent=true; break; }
        done
        $is_recent || images+=("$img")
    done
    if [[ ${#images[@]} -eq 0 ]]; then
        images=("${all_images[@]}")  # all recently used, cycle back
    fi
    echo "Background images: ${#images[@]} available (${#avoid_bgs[@]} recently used)"

    local count=0
    local img_idx=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        # Extract thumbnail title from descriptions.txt (first non-empty line after THUMBNAIL header)
        local desc="$vdir/descriptions.txt"
        local title=""
        if [[ -f "$desc" ]]; then
            title=$(awk '/THUMBNAIL/{found=1; next} found && /^═/{exit} found && NF{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); print; exit}' "$desc")
        fi
        if [[ -z "$title" ]]; then
            echo "$v: SKIPPED (no thumbnail title in descriptions.txt)" >&2
            continue
        fi
        # Rotate through available background images
        local bg="${images[$((img_idx % ${#images[@]}))]}"
        img_idx=$((img_idx + 1))
        echo "=== $v: generating thumbnail (bg: $(basename "$bg")) ==="
        cmd_thumbnail "$bg" "$title" "$vdir/thumbnail.png"
        count=$((count + 1))
    done
    echo "Done: $count thumbnail(s) generated"
}

cmd_batch_status() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi

    printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s %-8s\n" "VAR" "SCRIPT" "AUDIO" "CAPTS" "SUBS" "DRAFT" "THUMB" "FINAL"
    printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s %-8s\n" "---" "------" "-----" "-----" "----" "-----" "-----" "-----"

    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        local script="" audio="" capts="" subs="" draft="" thumb="" final=""

        if [[ -d "$vdir" ]]; then
            # Script: any .txt that isn't captions/descriptions/clip_map
            for f in "$vdir"/*.txt; do
                [[ -f "$f" ]] || continue
                local base
                base=$(basename "$f")
                if [[ "$base" != "captions.txt" && "$base" != "descriptions.txt" && "$base" != "clip_map.txt" ]]; then
                    script="YES"
                    break
                fi
            done

            [[ -n $(find "$vdir" -maxdepth 1 -name "*.mp3" -print -quit 2>/dev/null) ]] && audio="YES"
            [[ -f "$vdir/captions.txt" ]] && capts="YES"
            [[ -n $(find "$vdir" -maxdepth 1 -name "*.srt" -print -quit 2>/dev/null) ]] && subs="YES"
            [[ -f "$vdir/draft.mp4" ]] && draft="YES"
            [[ -f "$vdir/thumbnail.png" ]] && thumb="YES"
            [[ -n $(find "$vdir" -maxdepth 1 -name "*_final.mp4" -print -quit 2>/dev/null) ]] && final="YES"
        fi

        printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s %-8s\n" \
            "$v" "${script:---}" "${audio:---}" "${capts:---}" "${subs:---}" "${draft:---}" "${thumb:---}" "${final:---}"
    done

    # Duration check table
    echo ""
    echo "DURATION CHECK:"
    printf "%-4s %-10s %-10s %-10s\n" "VAR" "AUDIO" "DRAFT" "STATUS"
    printf "%-4s %-10s %-10s %-10s\n" "---" "-----" "-----" "------"
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        [[ -d "$vdir" ]] || continue
        local audio_dur="--" draft_dur="--" status="--"
        # Find audio
        for mp3 in "$vdir"/*.mp3; do
            [[ -f "$mp3" ]] || continue
            audio_dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$mp3" 2>/dev/null || echo "?")
            break
        done
        # Find draft
        if [[ -f "$vdir/draft.mp4" ]]; then
            draft_dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vdir/draft.mp4" 2>/dev/null || echo "?")
        fi
        # Compare
        if [[ "$audio_dur" != "--" && "$draft_dur" != "--" && "$audio_dur" != "?" && "$draft_dur" != "?" ]]; then
            local diff
            diff=$(echo "$draft_dur - $audio_dur" | bc 2>/dev/null || echo "?")
            if [[ "$diff" != "?" ]]; then
                if (( $(echo "$diff < 0" | bc -l 2>/dev/null) )); then
                    status="SHORT(${diff}s)"
                elif (( $(echo "$diff > 5.0" | bc -l 2>/dev/null) )); then
                    status="LONG(+${diff}s)"
                else
                    status="OK(+${diff}s)"
                fi
            fi
        fi
        printf "%-4s %-10s %-10s %-10s\n" "$v" "${audio_dur:0:8}s" "${draft_dur:0:8}s" "$status"
    done
}

cmd_validate() {
    local config="$1"
    shift
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Config not found: $config" >&2
        return 1
    fi
    "$CLI_PYTHON" "$ASSEMBLY_SCRIPT" "$config" --validate-only "$@"
}

cmd_check_render() {
    local config="$1"
    local video="$2"
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Config not found: $config" >&2
        return 1
    fi
    if [[ ! -f "$video" ]]; then
        echo "ERROR: Video not found: $video" >&2
        return 1
    fi
    "$CLI_PYTHON" "$ASSEMBLY_SCRIPT" "$config" --check-render "$video"
}

cmd_place_sfx() {
    echo "WARNING: place-sfx is deprecated. SFX placement is now AI-driven." >&2
    echo "The AI reads subtitles + SFX_CATALOG.md Basic Tier and places SFX in assembly config." >&2
    echo "See Audio effects/SFX_GUIDELINES.md for the new approach." >&2
    python3 "/media/kdabrow/Programy/givore/scripts/place_sfx.py" "$@"
}

# --- Main dispatch ---
case "${1:-help}" in
    duration)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh duration <file>" >&2; exit 1; }
        cmd_duration "$2"
        ;;
    duration-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh duration-all <project-dir>" >&2; exit 1; }
        cmd_duration_all "$2"
        ;;
    video-info)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh video-info <file>" >&2; exit 1; }
        cmd_video_info "$2"
        ;;
    video-info-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh video-info-all <project-dir>" >&2; exit 1; }
        cmd_video_info_all "$2"
        ;;
    generate-config)
        shift
        python3 "/media/kdabrow/Programy/givore/scripts/givore_db.py" generate-config "$@"
        ;;
    assemble)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh assemble <config.json>" >&2; exit 1; }
        cmd_assemble "$2"
        ;;
    render-draft)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh render-draft <config.json>" >&2; exit 1; }
        cmd_render_draft "$2"
        ;;
    render-final)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh render-final <config.json>" >&2; exit 1; }
        cmd_render_final "$2"
        ;;
    render-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh render-all <project-dir> [draft|final]" >&2; exit 1; }
        cmd_render_all "$2" "${3:-draft}"
        ;;
    assemble-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh assemble-all <project-dir>" >&2; exit 1; }
        cmd_assemble_all "$2"
        ;;
    validate-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh validate-all <project-dir> [--strict]" >&2; exit 1; }
        _va_dir="$2"; shift 2
        cmd_validate_all "$_va_dir" "$@"
        ;;
    check-render-all)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh check-render-all <project-dir>" >&2; exit 1; }
        cmd_check_render_all "$2"
        ;;
    thumbnail)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh thumbnail <image> <title> [output.png]" >&2; exit 1; }
        cmd_thumbnail "$2" "$3" "${4:-}"
        ;;
    thumbnail-from-video)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh thumbnail-from-video <video> <title> [output.png] [timestamp]" >&2; exit 1; }
        cmd_thumbnail_from_video "$2" "$3" "${4:-}" "${5:-}"
        ;;
    batch-thumbnails)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh batch-thumbnails <project-dir>" >&2; exit 1; }
        cmd_batch_thumbnails "$2"
        ;;
    subs)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh subs <audio.mp3> <captions.txt> [output.srt]" >&2; exit 1; }
        cmd_subs "$2" "$3" "${4:-}"
        ;;
    batch-subs)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh batch-subs <project-dir>" >&2; exit 1; }
        cmd_batch_subs "$2"
        ;;
    rename-audio)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh rename-audio <project-dir> <slug>" >&2; exit 1; }
        cmd_rename_audio "$2" "$3"
        ;;
    captions)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh captions <script.txt> [output.txt]" >&2; exit 1; }
        cmd_captions "$2" "${3:-}"
        ;;
    batch-captions)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh batch-captions <project-dir>" >&2; exit 1; }
        cmd_batch_captions "$2"
        ;;
    init-project)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh init-project <date_slug>" >&2; exit 1; }
        cmd_init_project "$2"
        ;;
    init-batch)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh init-batch <date_slug>" >&2; exit 1; }
        cmd_init_batch "$2"
        ;;
    init-renueva)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh init-renueva <date_slug>" >&2; exit 1; }
        cmd_init_renueva "$2"
        ;;
    init-renueva-batch)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh init-renueva-batch <date_slug> <N>" >&2; exit 1; }
        cmd_init_renueva_batch "$2" "$3"
        ;;
    batch-status)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh batch-status <project-dir>" >&2; exit 1; }
        cmd_batch_status "$2"
        ;;
    validate)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh validate <config.json> [--strict]" >&2; exit 1; }
        shift
        cmd_validate "$@"
        ;;
    check-render)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh check-render <config.json> <video.mp4>" >&2; exit 1; }
        cmd_check_render "$2" "$3"
        ;;
    place-sfx)
        shift
        cmd_place_sfx "$@"
        ;;
    extract-clips)
        shift
        "$HOME/.venv/clip_extractor/bin/python3" "/media/kdabrow/Programy/givore/scripts/clip_extractor.py" "$@"
        ;;
    clips)
        shift
        python3 "/media/kdabrow/Programy/givore/scripts/givore_db.py" "$@"
        ;;
    script-add|script-list|script-rotation|script-delete|\
    trial-add|trial-list|trial-rotation|trial-delete|\
    video-add|video-list|video-recent-clips|video-delete|\
    renueva-add|renueva-list|renueva-rotation|renueva-delete|\
    thumbnail-add|thumbnail-list|thumbnail-recent-bgs|thumbnail-delete|\
    migrate-scripts|migrate-trials|migrate-videos|migrate-all)
        python3 "/media/kdabrow/Programy/givore/scripts/givore_db.py" "$@"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Unknown command: $1" >&2
        usage >&2
        exit 1
        ;;
esac
