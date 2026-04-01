# Video Analysis API Research — 2026-03-31

**Use case**: Analyze 6-10 min cycling POV footage in Valencia to identify interesting moments (discarded furniture, scenic spots, transitions, street scenes). Replace/augment local CLIP+YOLO+optical flow pipeline.

**Volume**: ~5-10 videos per week, each 6-10 minutes.

---

## 1. GEMINI 2.5 FLASH (Google) — BEST OPTION

**How it works**: Upload video file via File API (up to 2GB, 48h retention). Send with custom prompt to `generateContent`. Native video understanding — no frame extraction needed. Samples at 1 fps by default (configurable). Supports timestamps in both prompts and responses.

**What it returns**: Free-form text responses guided by your prompt. Can return timestamped descriptions, scene labels, object identification, activity detection — whatever you ask for. Example prompt: *"Describe key events in this video with timestamps. Flag any discarded furniture, items on sidewalks, scenic spots, interesting transitions."*

**Pricing** (Gemini 2.5 Flash, via AI Studio or Vertex):
- Input: $0.30/1M tokens (under 200K context)
- Output: $2.50/1M tokens
- Video: 258 tokens/second at 1 fps
- Audio: 25 tokens/second (included with video)
- Context window: 1M tokens

**Cost for 10-minute video**:
- Video tokens: 600s x 258 = 154,800 tokens
- Audio tokens: 600s x 25 = 15,000 tokens
- Total input: 169,800 tokens = **$0.051**
- Output (assume ~2,000 tokens response): **$0.005**
- **TOTAL: ~$0.056 per 10-min video**
- Weekly (10 videos): **~$0.56**
- Monthly: **~$2.24**

**Custom prompts**: YES — full custom prompting. Can ask specifically about discarded furniture, street finds, scenic spots. Can request timestamped JSON output.

**Limitations**:
- Max ~1 hour of video per request (within 1M token context)
- One video per prompt recommended
- File upload max 2GB, retained 48 hours
- Free tier: 0 cost for low volume (rate-limited)

**Verdict**: By far the cheapest and most capable option. Native video understanding with custom prompts, timestamped output, and pennies per video.

---

## 2. GEMINI 2.5 FLASH-LITE (Google) — CHEAPEST POSSIBLE

**How it works**: Same as Gemini 2.5 Flash but lighter/faster model.

**Pricing**:
- Input: $0.10/1M tokens
- Output: $0.40/1M tokens
- Video tokenization: likely same 258 tokens/second (not confirmed separately)

**Cost for 10-minute video**:
- Input: 169,800 tokens x $0.10/1M = **$0.017**
- Output: 2,000 tokens x $0.40/1M = **$0.001**
- **TOTAL: ~$0.018 per 10-min video**
- Weekly (10 videos): **~$0.18**
- Monthly: **~$0.72**

**Limitations**: Less capable than full Flash. May miss nuanced context. Worth testing.

---

## 3. GEMINI 2.5 PRO (Google) — PREMIUM OPTION

**How it works**: Same upload flow. Most capable Gemini model.

**Pricing**:
- Input: $1.25/1M tokens (under 200K), $2.50/1M (over 200K)
- Output: $10.00/1M tokens

**Cost for 10-minute video**:
- Input: 169,800 tokens x $1.25/1M = **$0.212**
- Output: 2,000 tokens x $10/1M = **$0.020**
- **TOTAL: ~$0.23 per 10-min video**
- Weekly (10 videos): **~$2.30**

**Verdict**: 4x more expensive than Flash. Only worth it if Flash quality is insufficient.

---

## 4. GPT-4o / GPT-4.1 (OpenAI) — NO NATIVE VIDEO

**How it works**: Does NOT accept video files natively. Must extract frames as images and send individually. Lose audio, temporal context, and motion between frames. Typical approach: extract at 1-2 fps, resize to 512-768px, send as base64.

**Token cost per frame**:
- Low detail mode: 85 tokens/image (very cheap but low quality)
- High detail mode: ~765 tokens for 1024x1024 image (170 tokens per 512x512 tile + 85 base)
- For 720p resized frames: ~600-800 tokens per frame

**Pricing** (GPT-4o):
- Input: $2.50/1M tokens
- Output: $10.00/1M tokens

**Cost for 10-minute video** (1 fps, high detail ~765 tokens/frame):
- 600 frames x 765 tokens = 459,000 tokens
- Input cost: 459,000 x $2.50/1M = **$1.15**
- Output: ~2,000 tokens x $10/1M = **$0.02**
- **TOTAL: ~$1.17 per 10-min video**
- Weekly (10 videos): **~$11.70**

**Pricing** (GPT-4.1):
- Input: $2.00/1M tokens
- Output: $8.00/1M tokens
- **TOTAL: ~$0.93 per 10-min video**

**Pricing** (GPT-4.1 mini):
- Input: $0.40/1M tokens
- Output: $1.60/1M tokens
- **TOTAL: ~$0.19 per 10-min video** (but frame-only, no audio/temporal)

**Custom prompts**: YES — can prompt each batch of frames.

**Limitations**:
- No native video upload — requires frame extraction pipeline
- Loses audio, motion, temporal context between frames
- Context window pressure with many frames (4.1 has 1M context)
- Must build/maintain frame extraction code
- No timestamps returned natively (must calculate from frame index)

**Verdict**: Expensive, complex, and loses critical context. Not competitive with Gemini for video.

---

## 5. CLAUDE (Anthropic) — NO VIDEO SUPPORT

**How it works**: Claude accepts images but does NOT support video input at all (as of March 2026). Would require the same frame extraction approach as GPT-4o.

**Pricing** (Claude Sonnet 4.6):
- Input: $3.00/1M tokens
- Output: $15.00/1M tokens

**Cost for 10-minute video** (frame extraction at 1 fps):
- Similar token count to GPT-4o: ~459,000 input tokens
- Input: $1.38 + Output: $0.03 = **~$1.41 per 10-min video**

**Verdict**: More expensive than GPT-4o, same frame-extraction limitations, no video understanding. Not suitable.

---

## 6. TWELVE LABS — SPECIALIZED VIDEO UNDERSTANDING

**How it works**: Upload video to their platform. AI indexes the video with multimodal understanding (visual, audio, text on screen). Query via search API or generate descriptions.

**What it returns**: Semantic search results with timestamps, generated text descriptions, scene understanding. Built specifically for video — understands temporal context, actions, objects.

**Pricing**:
- Free tier: 600 minutes free
- Paid: starts at $0.033/minute indexed
- Enterprise: $5K-15K+/month for high volume

**Cost for 10-minute video**:
- Indexing: 10 min x $0.033 = **$0.33**
- Plus query/generate API costs (not clearly published)
- **Estimated TOTAL: ~$0.33-0.50 per 10-min video**
- Weekly (10 videos): **~$3.30-5.00**

**Custom prompts**: YES — semantic search queries and generate API support custom questions.

**Limitations**:
- Pricing not fully transparent beyond indexing
- Vendor lock-in (proprietary platform)
- Less flexible than Gemini's free-form prompting
- May require re-indexing if you change what you're looking for

**Verdict**: Good specialized tool but 6-10x more expensive than Gemini Flash for this use case.

---

## 7. GOOGLE VIDEO INTELLIGENCE API — TRADITIONAL ML

**How it works**: Upload video to GCS or send inline. Pre-trained ML models detect labels, shots, objects, text, faces. Returns structured JSON with timestamped annotations.

**What it returns**: Structured JSON with:
- Label detection (objects, activities, locations) with timestamps
- Shot change detection (scene boundaries)
- Object tracking with bounding boxes
- Text/OCR detection
- Explicit content detection

**Pricing per feature** (per minute, 1000 free minutes/month):
| Feature | Price/min |
|---------|-----------|
| Label detection | $0.10 |
| Shot detection | FREE (with label detection) |
| Explicit content | $0.10 |
| Speech transcription | $0.048 |
| Object tracking | $0.15 |
| Text detection | $0.15 |
| Logo detection | $0.15 |
| Person detection | $0.15 |

**Cost for 10-minute video** (label + shot + object tracking):
- Label: 10 x $0.10 = $1.00
- Shot: FREE
- Object tracking: 10 x $0.15 = $1.50
- **TOTAL: $2.50 per 10-min video**
- Weekly (10 videos): **~$25.00**
- Free tier covers first 100 min/month (10 videos)

**Custom prompts**: NO — fixed ML models, no custom queries. Returns generic labels like "bicycle", "road", "furniture" but cannot specifically look for "discarded furniture on sidewalks."

**Limitations**:
- No custom prompting — generic labels only
- No contextual understanding (can't distinguish "furniture in a store" from "discarded furniture on a curb")
- Expensive at scale
- Pre-trained models — cannot adapt to specific domain
- Being somewhat superseded by Gemini's capabilities

**Verdict**: Too expensive, too generic. Cannot distinguish "discarded item" from "item in a store." Not suitable for this use case.

---

## 8. AMAZON REKOGNITION VIDEO — TRADITIONAL ML

**How it works**: Upload to S3, call detection APIs. Similar to Google Video Intelligence.

**Pricing**:
| Feature | Price/min |
|---------|-----------|
| Label detection | $0.10 |
| Shot detection | $0.05 |
| Content moderation | $0.10 |
| Face detection | $0.10 |
| Text detection | $0.10 |
| Free tier | 60 min/month (12 months) |

**Cost for 10-minute video** (label + shot):
- **$1.50 per video**
- Weekly: **~$15.00**

**Custom prompts**: NO — same limitations as Google Video Intelligence.

**Verdict**: Slightly cheaper than Google Video Intelligence but same fundamental limitation: no custom prompting, no contextual understanding.

---

## 9. AZURE VIDEO INDEXER — RICHEST TRADITIONAL API

**How it works**: Upload video, get comprehensive analysis (transcription, OCR, objects, scenes, topics, sentiment, speaker indexing).

**Pricing**:
- Free trial: 10 hours (website) / 40 hours (API)
- Video indexing: ~$0.042/min
- Specific rates not fully public

**Cost for 10-minute video**:
- ~$0.42 per video (indexing only)
- Weekly: **~$4.20**

**Custom prompts**: LIMITED — pre-built analysis, no free-form prompting.

**Verdict**: Rich feature set but no custom semantic understanding. Middle-ground pricing.

---

## COMPARISON TABLE

| Provider | Native Video | Custom Prompts | Timestamps | Cost/10min | Cost/Week (10 videos) | Best For |
|----------|-------------|----------------|------------|-----------|----------------------|----------|
| **Gemini 2.5 Flash** | YES | YES | YES | **$0.056** | **$0.56** | BEST OVERALL |
| **Gemini 2.5 Flash-Lite** | YES | YES | YES | **$0.018** | **$0.18** | CHEAPEST |
| **Gemini 2.5 Pro** | YES | YES | YES | $0.23 | $2.30 | Highest quality |
| GPT-4.1 mini | NO (frames) | YES | Manual | $0.19 | $1.90 | Budget OpenAI |
| GPT-4.1 | NO (frames) | YES | Manual | $0.93 | $9.30 | OpenAI ecosystem |
| GPT-4o | NO (frames) | YES | Manual | $1.17 | $11.70 | Legacy |
| Claude Sonnet | NO (frames) | YES | Manual | $1.41 | $14.10 | Not suitable |
| Twelve Labs | YES | YES | YES | $0.33-0.50 | $3.30-5.00 | Video search |
| Azure Video Indexer | YES | LIMITED | YES | $0.42 | $4.20 | Enterprise |
| Google Video Intelligence | YES | NO | YES | $2.50 | $25.00 | Structured labels |
| Amazon Rekognition | YES | NO | YES | $1.50 | $15.00 | AWS ecosystem |

---

## RECOMMENDATION

### Winner: Gemini 2.5 Flash

**Why**:
1. **Cheapest by far**: $0.056 per 10-min video vs $0.33+ for next best (Twelve Labs)
2. **Native video upload**: No frame extraction pipeline needed
3. **Custom prompts**: Can ask specifically "find discarded furniture on sidewalks, scenic barrios, interesting transitions"
4. **Timestamped output**: Returns MM:SS timestamps in responses
5. **Audio understanding**: Hears ambient sounds, street noise (adds context)
6. **1M context window**: Can process up to ~1 hour of video
7. **Free tier available**: Rate-limited but free for testing
8. **Simple integration**: Upload file, send prompt, get response

### Suggested Implementation

```python
# Pseudocode for Gemini video analysis
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY")

# Upload video
video_file = genai.upload_file("cycling_footage.mp4")

# Wait for processing
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = genai.get_file(video_file.name)

# Analyze with custom prompt
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content([
    video_file,
    """Analyze this cycling POV footage from Valencia, Spain.
    For each interesting moment, provide:
    1. Timestamp (MM:SS)
    2. Category: one of [street-find, scenic-spot, transition, street-scene, interesting-moment]
    3. Description of what's visible
    4. Interest score (1-10)

    Focus especially on:
    - Discarded furniture or items on sidewalks (chairs, tables, shelves, appliances)
    - Scenic urban views (plazas, architecture, narrow streets)
    - Good transition moments (turns, speed changes, interesting visual flows)
    - Street life scenes (markets, people, pets, street art)

    Return as JSON array."""
])
```

### Cost Projection
- 10 videos/week x $0.056 = $0.56/week
- Monthly: ~$2.24
- Yearly: ~$29

### Testing Strategy
1. Start with Gemini 2.5 Flash-Lite ($0.018/video) to validate approach
2. Compare results with Gemini 2.5 Flash ($0.056/video)
3. If quality insufficient, try Gemini 2.5 Pro ($0.23/video)
4. All three share the same API — just change the model name

---

## Sources

- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini Video Understanding Docs](https://ai.google.dev/gemini-api/docs/video-understanding)
- [Gemini 2.5 Flash Pricing (PricePerToken)](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-flash)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Video Processing Cookbook](https://cookbook.openai.com/examples/gpt_with_vision_for_video_understanding)
- [GPT-4o Vision Guide](https://getstream.io/blog/gpt-4o-vision-guide/)
- [OpenAI Video Input Feature Request](https://github.com/openai/openai-node/issues/1778)
- [Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude Vision Docs](https://platform.claude.com/docs/en/build-with-claude/vision)
- [Twelve Labs Pricing](https://www.twelvelabs.io/pricing)
- [Google Video Intelligence Pricing](https://cloud.google.com/video-intelligence/pricing)
- [Amazon Rekognition Pricing](https://www.saasworthy.com/product/amazon-rekognition/pricing)
- [Azure Video Indexer Pricing](https://azure.microsoft.com/en-us/pricing/details/video-indexer/)
- [Best Video Analysis APIs 2026 (Eden AI)](https://www.edenai.co/post/best-video-analysis-apis)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
