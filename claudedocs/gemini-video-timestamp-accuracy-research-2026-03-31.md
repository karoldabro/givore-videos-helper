# Gemini API Video Timestamp Accuracy: Deep Research Report

**Date**: 2026-03-31
**Confidence Level**: HIGH (based on 15+ developer reports, official docs, and GitHub issues)

---

## Executive Summary

Gemini's video timestamp accuracy is **approximate at best, and frequently unreliable**. The fundamental constraint is that the File API samples video at **1 frame per second (FPS)**, creating an inherent ~1-second precision ceiling. In practice, developers report accuracy issues ranging from minor offsets to complete timestamp hallucination, with the problem being significantly worse for audio-only content than for video. Across all Gemini model generations (1.5, 2.0, 2.5, 3.0, 3.1), timestamp accuracy has been a persistent, unresolved pain point.

**Bottom line for the Givore clip extraction use case**: Gemini timestamps should NOT be trusted for frame-accurate clip extraction. They can serve as rough guidance (+-2-5 seconds) for scene identification, but any clip boundary must be validated and refined by other means (e.g., CLIP scoring, motion analysis, or manual review).

---

## 1. Timestamp Precision: Technical Architecture

### How Gemini Processes Video Internally

- **Frame sampling**: 1 FPS via the File API (subject to future changes per Google)
- **Audio processing**: 1 Kbps, single channel
- **Timestamp injection**: Added every 1 second
- **Token consumption**:
  - Default resolution: ~258 tokens/frame (~300 tokens/second of video)
  - Low resolution (`media_resolution=low`): ~66 tokens/frame (~100 tokens/second)
  - Audio: 32 tokens/second additional

### Precision Ceiling

The 1 FPS sampling rate creates a **hard floor of ~1-second precision**. The model cannot identify events between frames. For a 50fps source video (like Givore cycling footage), this means 49 out of every 50 frames are never seen by the model.

### Timestamp Format

- Gemini was trained to output timestamps in **MM:SS** format
- Gemini 2.5+ also supports **H:MM:SS** for longer videos
- No sub-second precision is available from the model
- The `videoMetadata` API supports `startOffset`/`endOffset` with seconds and nanoseconds for INPUT clipping, but model OUTPUT is limited to whole seconds

---

## 2. Known Issues: Developer Reports (Chronological)

### Gemini 1.5 Flash (2024)
- **Issue**: Hallucinates timestamps when transcribing audio
- **Source**: [GitHub Issue #269](https://github.com/google-gemini/deprecated-generative-ai-js/issues/269)

### Gemini 2.0 Flash / Flash Lite (Early 2025)
- **Issue**: After GA release, timestamps for audio became completely hallucinated. Video timestamps remained relatively accurate.
- **Critical workaround discovered**: Converting audio to MP4 (with solid color background) restores timestamp accuracy, at ~10x token cost
- **Source**: [Forum: Gemini 2.0 Flash Lite timestamp hallucinations](https://discuss.ai.google.dev/t/gemini-2-0-flash-lite-timestamp-hallucinations-for-audio-but-not-video-since-going-into-ga/69370)
- **Source**: [GitHub Issue #426](https://github.com/google-gemini/deprecated-generative-ai-js/issues/426)
- **Source**: [GitHub Cookbook Issue #733](https://github.com/google-gemini/cookbook/issues/733) - "Refer to timestamps" feature returns transcriptions for random portions of audio, not respecting MM:SS boundaries

### Gemini 2.0 Production Models (Mid 2025)
- **Issue**: Forced alignment / timestamp generation still broken
- **Source**: [Forum: Timestamp generation on 2.0 production models is still broken](https://discuss.ai.google.dev/t/timestamp-generation-forced-alignment-on-2-0-production-models-is-still-broken/79553)
- **Source**: [Forum: Audio timestamp accuracy issue in Gemini 2.0 GA models](https://discuss.ai.google.dev/t/audio-timestamp-accuracy-issue-in-gemini-2-0-ga-models/72114)

### Gemini 2.5 Pro (Mid-Late 2025)
- **Issue**: Severe timecode jumping in video transcription. Timestamps don't align with actual video content.
- **Use case affected**: Video editing applications requiring high precision for splitting clips and syncing audio/video
- **Source**: [Forum: Severe Timestamp/Timecode Jumping Issues](https://discuss.ai.google.dev/t/gemini-2-5-pro-severe-timestamp-timecode-jumping-issues-in-video-transcription-need-workarounds/87242)
- **Source**: [Forum: Improve timestamp accuracy on video understanding](https://discuss.ai.google.dev/t/improve-timestamp-accuracy-on-video-understanding/95356)

### Gemini 3.0 Pro Preview / 2.5 Pro (December 10, 2025)
- **Issue**: SRT transcription timestamps became "wildly inaccurate" overnight, despite NO changes to prompt or model selection
- **Impact**: Production systems broke without any user-side changes
- **Source**: [Forum: Gemini API SRT Transcription Suddenly Broken](https://discuss.ai.google.dev/t/gemini-api-srt-transcription-suddenly-broken-timestamps-are-wildly-inaccurate-since-yesterday-despite-no-prompt-model-change/111846)

### Gemini 3.0 (Early 2026)
- **Issue**: Lost audio data interpretation capabilities, especially regarding time. Produces "nonsensical" subtitle/timestamp results where Gemini 2.5 Pro was accurate.
- **Source**: [Forum: Gemini 3 has lost audio time capabilities](https://discuss.ai.google.dev/t/it-seems-gemini-3-has-lost-its-audio-data-interpretation-capabilities-especially-regarding-time/110751)

### Gemini 3 Flash / 3.1 Pro (March 2026)
- **Issue**: Progressive timestamp drift in audio transcription. Benchmarked on 11:49 Arabic audio clip with serious drift.
- **Reporter**: CTO of edtech startup (language learning platform requiring synchronized text)
- **Source**: [Forum: Progressive timestamp drift in audio transcription](https://discuss.ai.google.dev/t/bug-gemini-3-flash-and-3-1-pro-progressive-timestamp-drift-in-audio-transcription/129501)

### Pattern Summary
| Model | Audio Timestamps | Video Timestamps | Severity |
|-------|-----------------|------------------|----------|
| 1.5 Flash | Hallucinated | Not reported | High |
| 2.0 Flash/Lite GA | Hallucinated | Relatively OK | High |
| 2.0 Production | Broken | Better than audio | High |
| 2.5 Pro | Jumping/drifting | Jumping/drifting | Medium-High |
| 3.0 Pro Preview | Wildly inaccurate | Less severe | High |
| 3.0 Flash | Nonsensical | Not reported | High |
| 3 Flash / 3.1 Pro | Progressive drift | Unknown | Medium-High |

**Key observation**: Video timestamps are consistently MORE accurate than audio timestamps across all model versions, but neither is reliable enough for production clip extraction.

---

## 3. Resolution Mode Impact

### Does `media_resolution=low` affect timestamp accuracy?

Based on the research, **timestamp accuracy does NOT appear to be directly affected by the media_resolution setting**. The timestamps are tied to the 1 FPS frame extraction, which happens regardless of resolution. The resolution setting affects:

- **Token count per frame**: 66 (low) vs 258 (default) vs 280 (high, Gemini 3)
- **Visual detail recognition**: Fine text, small objects
- **Context window capacity**: Low = 3 hours of video; Default = 1 hour

However, lower resolution means less visual information per frame, which could indirectly impact the model's ability to accurately identify WHEN specific visual events occur, since it has less detail to distinguish between similar-looking frames.

### Gemini 3 Resolution Tiers
| Setting | Tokens/Frame | Max Video Length (1M context) |
|---------|-------------|-------------------------------|
| Low | 66-70 | ~3 hours |
| Medium | 70 | ~3 hours |
| Default/High | 258-280 | ~1 hour |

---

## 4. Techniques to Improve Accuracy

### Confirmed Workarounds

1. **Audio-to-video conversion**: If processing audio, convert to MP4 with solid background. Restores timestamp accuracy at ~10x token cost.

2. **Use MM:SS format in prompts**: Gemini was specifically trained on this format. Using it in both input references and output requests aligns with the model's training.

3. **Process shorter segments**: Use `videoMetadata` with `startOffset`/`endOffset` to analyze specific segments rather than entire videos. This reduces drift accumulation.

4. **External timestamp calculation**: Use PySRT or similar tools to calculate timestamps independently per segment, then compile. Do not rely solely on Gemini's generated timestamps.

5. **Custom FPS override**: Pass a higher `fps` argument in `videoMetadata` for finer temporal granularity. Note: this increases token consumption proportionally.

6. **Structured output / JSON mode**: Use `responseSchema` to enforce strict timestamp output format. While this doesn't improve the model's temporal perception, it prevents format-related parsing errors.

### Prompt Engineering Tips

- Ask for timestamps explicitly: "Provide timestamps in MM:SS format for each scene change"
- Request both start and end timestamps for events
- For long videos, ask the model to process in segments
- Include temporal anchoring: "The video is X minutes long. Identify events with their timestamps."
- Ask for confidence levels alongside timestamps

### What Does NOT Help

- Asking for frame numbers (model doesn't have frame-level access)
- Requesting sub-second precision (not supported)
- Relying on model consistency across runs (timestamps can vary between calls for the same video)
- Trusting timestamps for audio-only content without the video workaround

---

## 5. Comparison with Alternatives

### Google Video Intelligence API
- **Approach**: Deterministic computer vision, not LLM-based
- **Shot/scene detection**: Frame-level analysis with explicit timestamp segments (seconds + nanoseconds)
- **Strength**: Consistent, reproducible results; frame-accurate for shot boundaries
- **Weakness**: No semantic understanding, no natural language queries
- **Timestamp precision**: Frame-accurate (sub-second)
- **Verdict**: Far more reliable for timestamp-dependent operations like clip extraction

### Twelve Labs (Pegasus)
- **Approach**: Purpose-built video-language model with native temporal grounding
- **Strength**: "Exceptional temporal understanding" - can localize and ground answers based on timestamps
- **Timestamp precision**: Sub-second accuracy for temporal grounding tasks
- **Weakness**: Slower for generating long-form text content
- **Verdict**: More reliable for temporal tasks than Gemini; purpose-built for video search/understanding

### Gemini vs Competitors Summary
| Feature | Gemini | Video Intelligence API | Twelve Labs |
|---------|--------|----------------------|-------------|
| Timestamp precision | ~1-2 seconds (unreliable) | Frame-accurate | Sub-second |
| Semantic understanding | Strong | None | Strong |
| Natural language queries | Yes | No | Yes |
| Consistency | Poor (varies between runs) | Deterministic | Good |
| Audio integration | Yes (buggy timestamps) | Separate API | Yes |
| Cost efficiency | Good (esp. Flash) | Per-feature pricing | Higher |
| Long video support | Up to 3 hours | Varies | Varies |

---

## 6. Flash vs Pro: Temporal Accuracy Differences

### Available Evidence

There is **no definitive benchmark** comparing Flash vs Pro timestamp accuracy in isolation. However, from developer reports:

- **Gemini 2.5 Pro**: Documented timecode jumping issues for video transcription
- **Gemini 2.5 Flash**: Google claims "similar results" to Pro for video understanding
- **Gemini 3 Flash**: Progressive timestamp drift reported
- **Gemini 3.1 Pro**: Progressive timestamp drift reported (same bug report as 3 Flash)

### Processing Speed Difference
- Flash: ~80-85 seconds per video
- Pro: ~120 seconds per video

The longer processing time of Pro does NOT appear to translate into better timestamp accuracy. Both model tiers suffer from the same fundamental 1 FPS sampling limitation.

### Practical Recommendation

For timestamp-dependent use cases, **neither Flash nor Pro offers reliable precision**. If choosing between them for video analysis where timestamps matter:
- Use **Flash** for cost efficiency (timestamps will be equally unreliable)
- Use **Pro** only if you need superior semantic understanding of video content (not for temporal precision)

---

## 7. Implications for Givore Clip Extraction

### Current Pipeline (CLIP + YOLO + Optical Flow)
The current `clip_extractor.py` approach using CLIP scoring, YOLO object detection, and optical flow analysis is **fundamentally more reliable** for clip boundary detection than Gemini timestamps would be, because:

1. It operates at full frame rate (not 1 FPS)
2. It uses deterministic computer vision (not probabilistic LLM output)
3. Results are reproducible across runs
4. Sub-second precision is achievable

### Where Gemini Could Add Value
Despite timestamp limitations, Gemini could complement the current pipeline for:
- **Semantic scene description**: Understanding WHAT is in each clip (not WHEN)
- **Content categorization**: Classifying clip types (cycling, item discovery, bridge, etc.)
- **Script-to-clip matching**: Suggesting which clips match which script sections (using content understanding, not timestamps)
- **Batch content analysis**: Describing multiple clips for DB metadata

### Where Gemini Should NOT Be Used
- Frame-accurate clip boundary detection
- Automated clip splitting based on scene changes
- Any workflow requiring sub-second or even reliable second-level temporal precision
- Production SRT/subtitle generation (unless validated by external alignment tools)

---

## Sources

### Google AI Developers Forum
- [Improve timestamp accuracy on video understanding](https://discuss.ai.google.dev/t/improve-timestamp-accuracy-on-video-understanding/95356)
- [Gemini 2.5 Pro Severe Timestamp/Timecode Jumping Issues](https://discuss.ai.google.dev/t/gemini-2-5-pro-severe-timestamp-timecode-jumping-issues-in-video-transcription-need-workarounds/87242)
- [Gemini API SRT Transcription Suddenly Broken](https://discuss.ai.google.dev/t/gemini-api-srt-transcription-suddenly-broken-timestamps-are-wildly-inaccurate-since-yesterday-despite-no-prompt-model-change/111846)
- [Gemini 2.0 Flash Lite timestamp hallucinations](https://discuss.ai.google.dev/t/gemini-2-0-flash-lite-timestamp-hallucinations-for-audio-but-not-video-since-going-into-ga/69370)
- [Timestamp generation on 2.0 production models still broken](https://discuss.ai.google.dev/t/timestamp-generation-forced-alignment-on-2-0-production-models-is-still-broken/79553)
- [Audio timestamp accuracy issue in Gemini 2.0 GA](https://discuss.ai.google.dev/t/audio-timestamp-accuracy-issue-in-gemini-2-0-ga-models/72114)
- [Gemini Pro Timestamp Accuracy Issues in Audio Transcription](https://discuss.ai.google.dev/t/gemini-pro-timestamp-accuracy-issues-in-audio-transcription/52587)
- [Bug: Gemini 3 Flash and 3.1 Pro Progressive timestamp drift](https://discuss.ai.google.dev/t/bug-gemini-3-flash-and-3-1-pro-progressive-timestamp-drift-in-audio-transcription/129501)
- [Gemini 3 lost audio time capabilities](https://discuss.ai.google.dev/t/it-seems-gemini-3-has-lost-its-audio-data-interpretation-capabilities-especially-regarding-time/110751)
- [Best practices for video pre-processing with media_resolution](https://discuss.ai.google.dev/t/best-practices-for-video-pre-processing-resolution-with-media-resolution-parameter-in-gemini-3-0/109808)

### GitHub Issues
- [Gemini 2.0 Flash hallucinates timestamps (JS SDK)](https://github.com/google-gemini/deprecated-generative-ai-js/issues/426)
- [Gemini 1.5 Flash hallucinates timestamps](https://github.com/google-gemini/deprecated-generative-ai-js/issues/269)
- [Refer to timestamps feature broken (Cookbook)](https://github.com/google-gemini/cookbook/issues/733)
- [PySRT timestamp workaround](https://github.com/jianchang512/pyvideotrans/issues/624)

### Official Documentation
- [Video understanding - Gemini API](https://ai.google.dev/gemini-api/docs/video-understanding)
- [Media resolution - Gemini API](https://ai.google.dev/gemini-api/docs/media-resolution)
- [Vertex AI Video Understanding](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding)

### Blog Posts & Articles
- [Advancing video understanding with Gemini 2.5 (Google Developers Blog)](https://developers.googleblog.com/en/gemini-2-5-video-understanding/)
- [Lessons from Using Google Gemini for Video Analysis (Decipher)](https://getdecipher.com/blog/lessons-from-using-google-gemini-for-video-analysis)
- [Unlocking Multimodal Video Transcription with Gemini (Towards Data Science)](https://towardsdatascience.com/unlocking-multimodal-video-transcription-with-gemini/)
- [Building Vision AI with Gemini 3 (GetStream)](https://getstream.io/blog/gemini-vision-ai-capabilities/)
- [Scene detection with timestamps from videos using Gemini](https://thomaschang.me/blog/video-to-gif)
- [Pegasus 1.2: Industry-Grade Video Language Model (Twelve Labs)](https://www.twelvelabs.io/blog/introducing-pegasus-1-2)
