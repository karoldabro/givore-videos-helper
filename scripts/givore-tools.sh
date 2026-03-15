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
  video-info-all <project-dir> Video info for all drafts/finals in v1-v7

Video pipeline:
  generate-config [args]      Generate assembly_config.json from audio + clip IDs
  assemble <config.json>      Assemble project (JSON -> project.json + .mlt)
  render-draft <config.json>  Assemble + render draft (540x960)
  render-final <config.json>  Assemble + render final (1080x1920)
  render-all <project-dir> [draft|final]  Render all v1-v7 variants
  place-sfx [args]            Smart SFX placement (see place_sfx.py --help)

Quality checks:
  validate <config.json> [--strict]         Pre-flight validation (files, durations, paths)
  check-render <config.json> <video.mp4>    Post-render validation (duration, aspect ratio)

Subtitles:
  subs <audio.mp3> <captions.txt>  Generate SRT from audio + captions

Project setup:
  init-project <slug>         Create project folder (projects/<slug>/)
  init-batch <slug>           Create batch folders (v1-v7 + finals/)

Batch:
  batch-status <project-dir>  Show file status for all 7 variants
  copy-finals <project-dir>   Copy all vN/*_final.mp4 to finals/ folder

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
    # Also check finals/ directory
    local finals="$dir/finals"
    if [[ -d "$finals" ]]; then
        for mp4 in "$finals"/*.mp4; do
            [[ -f "$mp4" ]] || continue
            local dims dur
            dims=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$mp4" 2>/dev/null || echo "?")
            dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$mp4" 2>/dev/null || echo "?")
            printf "%-4s %-40s %-12s %s\n" "fin" "$(basename "$mp4")" "$dims" "${dur}s"
        done
    fi
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

cmd_copy_finals() {
    local project_dir="$1"
    local finals_dir="$project_dir/finals"
    mkdir -p "$finals_dir"
    local count=0
    for v in v1 v2 v3 v4 v5 v6 v7; do
        local final
        final=$(find "$project_dir/$v" -maxdepth 1 -name "*_final.mp4" -print -quit 2>/dev/null)
        [[ -z "$final" ]] && continue
        local slug
        slug=$(basename "$project_dir")
        cp "$final" "$finals_dir/${v}_${slug}_final.mp4"
        echo "Copied: ${v}_${slug}_final.mp4"
        count=$((count + 1))
    done
    echo "Done: $count final(s) copied to $finals_dir/"
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

cmd_subs() {
    local audio="$1"
    local captions="$2"
    if [[ ! -f "$audio" ]]; then
        echo "ERROR: Audio not found: $audio" >&2
        return 1
    fi
    if [[ ! -f "$captions" ]]; then
        echo "ERROR: Captions not found: $captions" >&2
        return 1
    fi
    subs "$audio" "$captions"
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
    mkdir -p "$dir/finals"
    echo "Created: v1-v7 + finals/ in $dir"
}

cmd_batch_status() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Directory not found: $dir" >&2
        return 1
    fi

    printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s\n" "VAR" "SCRIPT" "AUDIO" "CAPTS" "SUBS" "DRAFT" "FINAL"
    printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s\n" "---" "------" "-----" "-----" "----" "-----" "-----"

    for v in v1 v2 v3 v4 v5 v6 v7; do
        local vdir="$dir/$v"
        local script="" audio="" capts="" subs="" draft="" final=""

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
            [[ -n $(find "$vdir" -maxdepth 1 -name "*_final.mp4" -print -quit 2>/dev/null) ]] && final="YES"
        fi

        printf "%-4s %-8s %-8s %-8s %-8s %-8s %-8s\n" \
            "$v" "${script:---}" "${audio:---}" "${capts:---}" "${subs:---}" "${draft:---}" "${final:---}"
    done

    # Check finals directory
    local finals_count=0
    if [[ -d "$dir/finals" ]]; then
        finals_count=$(find "$dir/finals" -name "*.mp4" 2>/dev/null | wc -l)
    fi
    echo ""
    echo "Finals directory: ${finals_count} video(s)"

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
                local abs_diff=${diff#-}
                if (( $(echo "$abs_diff > 1.0" | bc -l 2>/dev/null) )); then
                    status="MISMATCH(${diff}s)"
                else
                    status="OK"
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
    copy-finals)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh copy-finals <project-dir>" >&2; exit 1; }
        cmd_copy_finals "$2"
        ;;
    subs)
        [[ $# -lt 3 ]] && { echo "Usage: givore-tools.sh subs <audio.mp3> <captions.txt>" >&2; exit 1; }
        cmd_subs "$2" "$3"
        ;;
    init-project)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh init-project <date_slug>" >&2; exit 1; }
        cmd_init_project "$2"
        ;;
    init-batch)
        [[ $# -lt 2 ]] && { echo "Usage: givore-tools.sh init-batch <date_slug>" >&2; exit 1; }
        cmd_init_batch "$2"
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
    clips)
        shift
        python3 "/media/kdabrow/Programy/givore/scripts/givore_db.py" "$@"
        ;;
    script-add|script-list|script-rotation|script-delete|\
    trial-add|trial-list|trial-rotation|trial-delete|\
    video-add|video-list|video-recent-clips|video-delete|\
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
