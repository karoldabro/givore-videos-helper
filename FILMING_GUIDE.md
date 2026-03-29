# Filming Guide — Cycling POV Footage for Clip Extraction

Practical guide for filming cycling POV footage that maximizes the quality and variety of clips extracted by the automated pipeline (`scripts/clip_extractor.py`).

---

## How the Pipeline Sees Your Footage

The clip extractor analyzes every frame of your video using four AI systems:

| System | What It Does | What It Looks For |
|--------|-------------|-------------------|
| **CLIP** (ViT-L-14) | Scores frames against 8 text queries | Landmarks, street life, parks, architecture, street art, dynamic cycling, plazas, waterfront |
| **YOLO** (YOLOv8n) | Detects objects in each frame | People, furniture (chair, couch, bed), dogs, cats, bicycles, plants |
| **Optical flow** | Measures motion speed and direction | Speed changes, direction shifts, stops |
| **Moondream2** | Generates scene descriptions | Overall scene content for clip naming |

The pipeline produces a **composite score** per frame (motion 20%, CLIP interest 35%, visual diversity 20%, object detection 25%) and extracts 2-5 second clips around the highest-scoring moments.

Your physical behavior while filming directly controls what the pipeline detects and how it classifies clips.

---

## Camera Signals for Each Clip Type

After extraction, you manually assign a filename prefix (`[hook]`, `[item]`, `[end]`, `[start]`, `[bridge]`) during the review step. The pipeline provides the detection signals that make classification straightforward.

### [item] — Street-Found Objects

**What to do**: Slow down or stop near a discarded item. Pull out your phone to photograph it.

**Why it works**:
- The motion drop (dynamic to calm) creates a score peak
- YOLO detects furniture objects (chair, couch, bed) with bonus scores: chair +0.08, couch +0.10
- Phone in hand triggers additional object detection
- The contenedores grises (gray trash containers) in the background reinforce the scene context

**Minimum duration**: Linger for at least 4 seconds. The pipeline extracts clips of 2-5 seconds, but 3-4 seconds of lingering gives enough frames for a clean selection.

**Keep camera running** while you photograph the item with your phone. Stopping the recording loses the approach-and-discover moment.

### [hook] — Opening Shots

**What to do**: Make a deliberate camera movement — pan to reveal a scene, look up then down quickly, enter a narrow street from a wide one, or turn a corner to reveal something unexpected.

**Why it works**:
- Sharp motion changes create high optical flow peaks
- Scene transitions score high on visual diversity (cosine distance between consecutive CLIP embeddings)
- CLIP queries for "dynamic cycling through narrow streets" and "landmark buildings" produce high interest scores

**Best moments**: Entering a narrow alley, crossing from shade to sun, passing under an arch, revealing a plaza.

### [end] — Closing Shots

**What to do**: At the end of your ride, tilt the camera slowly upward toward the sky, trees, or building tops.

**Why it works**:
- Upward motion in the final portion of the video
- CLIP detects sky, canopy, or architectural tops
- Position in the last section of the footage

**Duration**: 3-5 seconds of smooth upward tilt.

### [start] — Establishing Shots

**What to do**: Film a few seconds of wide establishing view at the beginning of your ride — a recognizable street, a landmark, a barrio entrance sign.

**Why it works**:
- Being in the first 8% of the video marks it as an opening candidate
- CLIP queries for landmarks and plazas score high on wide establishing views
- Low initial motion (just starting the ride) combined with an interesting scene

**Duration**: 5-8 seconds of a wide, recognizable view before you start moving fast.

### [bridge] — Transitions Between Scenes

**What to do**: Make a clear directional transition — turn a corner sharply, cross an intersection, pass through a tunnel or underpass.

**Why it works**:
- Direction change in optical flow creates a distinctive motion signature
- Visual diversity spikes when the scene changes completely (different buildings, different lighting)
- CLIP embedding distance between consecutive frames jumps at scene boundaries

**Best moments**: Sharp turns at intersections, entering/exiting a park, crossing a bridge.

---

## General Filming Tips

### Linger on Interesting Things (3-5 Seconds)

The pipeline needs enough frames to identify a peak and extract a clean clip. A quick glance (under 2 seconds) may not register. When you see something worth capturing, hold steady for 3-5 seconds.

### Vary Your Speed

Constant speed produces flat motion curves with no peaks. The pipeline finds clips at **score peaks** — moments where something changes. Alternate between:
- Fast riding through streets (dynamic baseline)
- Slowing down near interesting scenes (creates motion dip + interest peak)
- Brief stops at items or views (creates the strongest peaks)

### Film Multiple Barrios Per Session

Each clip gets tagged with a location name. A 30-60 minute ride through 2-3 barrios produces clips tagged to different areas, which prevents location repetition across videos.

### Capture Ambient Audio Moments

For "Sonidos de la Calle" format content, pause near:
- Market stalls with vendor calls
- Fountains or water features
- Street musicians
- Bird-heavy trees or plazas

Note: the clip extractor strips audio from extracted clips (`-an` flag), but the original video retains audio for manual extraction later.

### Weather Is Content

Rain, wind, golden hour, overcast skies — all create distinctive visual conditions that CLIP scores differently from normal sunny footage. Atmospheric footage scores well on diversity because it looks different from your typical clips.

### Keep the Camera Running When Photographing Items

The moment you stop, pull out your phone, and photograph a discarded item is the highest-signal sequence for the pipeline: motion drop + furniture detection + phone detection. Stopping the recording before this moment loses the best frames.

---

## What NOT to Do

| Mistake | Why It Hurts |
|---------|-------------|
| Wave or gesture randomly | Confuses hook detection — creates motion peaks without interesting scene content, producing low-quality clips |
| Cover lens or point at ground | Empty frames get a -0.20 penalty in object scoring. Extended ground-pointing wastes analysis time |
| Film only handlebars/bike | YOLO sees "bicycle" (+0.05 bonus only) but nothing else interesting. Low composite scores |
| Ride at constant speed the entire time | Flat motion curve = no peaks = fewer clips extracted. The pipeline relies on score variation |
| Film very short glances at items (under 2 seconds) | Below minimum clip duration. The pipeline may skip the moment entirely |
| Film in extremely dark conditions | CLIP and YOLO accuracy drops significantly. Moondream2 captions become generic |

---

## Format-Specific Filming Checklist

Each content format needs different types of footage. Plan your ride accordingly.

| Format | What to Film | Suggested Ride Duration | Key Signals for Pipeline |
|--------|-------------|------------------------|--------------------------|
| **El Ranking** | 5+ distinct discarded items in one ride | 20+ min | Multiple stop-and-photograph sequences; furniture YOLO hits |
| **60 Segundos en...** | Fast tour of one barrio — food spots, art, corners, people | 10-15 min in one area | High CLIP diversity; street_life and architecture queries |
| **Cuanto Cuesta** | One impressive item, close-up + price lookup on phone | 30 sec lingering at item | Strong furniture detection + phone object; long dwell time |
| **Lo Que Nadie Ve** | Hidden corner, quiet moment, unexpected beauty | 5-10 sec slow lingering | Low motion + high CLIP landmark/architecture score |
| **Sonidos de la Calle** | Market, fountain, street musician, birds | 15-30 sec ambient per source | Note: audio not extracted by pipeline; use original video |
| **Ruta Gastro** | Stop at 2-3 food spots, film the food and surroundings | Planned route, 15-20 min | street_life query peaks; people detection near food spots |
| **Lluvia/Noche/Extremo** | Atmospheric condition riding | Any duration | High diversity scores (unusual lighting); distinctive CLIP matches |
| **Classic Street Finds** | Multiple items across multiple barrios | 30-60 min ride | Mix of item stops, transitions between areas, establishing shots |
| **Cycling POV** | Pure riding footage, scenic routes | 15-30 min | dynamic_cycling query; varied speed; park and waterfront queries |
| **Barrio Guide** | Systematic coverage of one neighborhood | 15-20 min in one area | Landmarks, architecture, plazas, street art — all CLIP queries active |

---

## One Ride = Multiple Formats

A single 30-60 minute ride naturally produces footage for 7+ content formats simultaneously. You do not need separate filming sessions for each format.

**What a typical ride includes by default**:

1. **[start]** — You begin somewhere recognizable (establishing shot)
2. **[hook]** — You enter a narrow street or turn a corner (reveals happen naturally)
3. **Cycling POV** — You ride through streets (continuous baseline footage)
4. **[item]** — You spot and photograph a discarded item (stop-and-discover moment)
5. **[bridge]** — You cross an intersection to the next area (transitions happen between items)
6. **Barrio content** — You pass landmarks, street art, plazas (CLIP catches these)
7. **[end]** — You tilt up toward the sky at ride's end (deliberate closing gesture)

**Example**: A 40-minute ride through Benimaclet and Ayora yields:
- 2-3 item clips (street finds content)
- 3-4 cycling POV clips (pure riding content)
- 1-2 landmark/architecture clips (barrio guide content)
- 1 start clip, 1 end clip (reusable across any format)
- 1-2 bridge clips (transitions for assembled videos)
- Ambient audio in the original video (market sounds, if you passed one)

The batch pipeline (`/givore-batch`) then uses different combinations of these clips across 7 video variants, each with a different script, format, and hook.

---

## Equipment Notes

- **Camera**: DJI action camera on helmet or handlebar mount. Produces `.MP4` files with `.LRF` low-resolution proxy files (the pipeline auto-detects LRF for 6x faster analysis)
- **Phone**: For photographing items (also triggers YOLO phone/hand detection)
- **No special equipment needed**: No external mic, no gimbal, no lighting. The camera's built-in stabilization and the natural motion of cycling are the content

### DJI LRF Proxy Files

The DJI camera creates a low-resolution `.LRF` file alongside each `.MP4`. The clip extractor automatically detects and uses the LRF for frame analysis (6x faster processing), then extracts the final clips from the original high-resolution MP4. You do not need to do anything — just keep both files in the same directory.

| File | Resolution | Used For |
|------|-----------|----------|
| `DJI_*.MP4` | Full resolution | Final clip extraction |
| `DJI_*.LRF` | Low resolution proxy | Frame analysis (CLIP, YOLO, optical flow) |

Processing time: ~2.7 min for a 6-min video with LRF proxy, ~14 min without.
