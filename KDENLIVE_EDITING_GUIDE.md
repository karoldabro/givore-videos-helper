# Kdenlive Editing Guide for Givore TikTok Videos
## Compact Reference for Viral Content

---

## Quick Settings

### Project Profile
```
Resolution: 1080x1920 (9:16 vertical)
Frame rate: 30fps
```
*File → New → Custom Profile → 1080x1920, 30fps*

### Export Settings
```
Format: MP4 (H.264)
Resolution: 1080x1920
Bitrate: 8-12 Mbps (higher = better quality)
Audio: AAC, 48kHz, 192kbps
```

---

## Proven Viral Elements (200k+ Views Video)

**Source:** See VIRAL_VIDEO_ANALYSIS.md for complete breakdown

### POV Cycling Format (Critical for Engagement)

| Element | Execution | Why It Works |
|---------|-----------|--------------|
| Handlebars visible | Keep bike handles in bottom of frame | Creates "ride along" feeling |
| Constant motion | Never stop completely during filming | Maintains visual engagement |
| Discovery POV | Viewer sees items as creator discovers | Builds anticipation |

**Result:** 15.08s average watch time (above platform average)

### Caption Styling (Brand + Readability)

```
Font: Sans-serif italic
Color: Givore green (#00AA00 or similar)
Outline: 2-3px black
Position: Center, above bottom 20%
Sync: Match speech timing exactly
```

**Why:** High contrast against street backgrounds, professional but not corporate, readable at scroll speed.

### Pattern Interrupts (CRITICAL - Addresses 0:02 Dropoff)

**Problem:** Most viewers scroll at 0:02, but hook completes at 2.44s.

**Solution - Add visual interrupt at 2s:**

| Interrupt Type | How to Execute | When to Use |
|----------------|----------------|-------------|
| Quick zoom | 1.1-1.2x scale for 0.3s | On hook word landing |
| Sound effect | Pop/whoosh at 1.5-2s | All videos |
| Text flash | Key word appears briefly | Question hooks |
| Item preview | 0.5s flash of find | Before question |

**Implementation in Kdenlive:**
1. At 1.5-2s mark, add scale keyframe (100% → 110% → 100%)
2. Add "pop" SFX from track 2
3. Duration: 0.3-0.5s total
4. Don't overdo - one interrupt per video

### Golden Hour Lighting

| Aspect | Guideline |
|--------|-----------|
| Target time | 15:00-17:00 (Valencia) |
| Quality | Warm, natural, flattering |
| Effect | Makes city look inviting |
| Backup | Overcast works, midday harsh |

**In Post:** If not golden hour, add +5-10 warmth in color correction.

### Natural App Integration

**DO:**
- Show real Givore camera UI (buttons visible)
- Capture "in-the-moment" - not staged
- Let interface appear briefly, naturally

**DON'T:**
- Stage fake demos
- Hold on app screen too long
- Add arrows/highlights

**Why:** 90% of brand searches were for "Givore" - authenticity drives curiosity.

### Item Selection Impact

| Item Type | Share Potential | Examples |
|-----------|-----------------|----------|
| Unusual/quirky | HIGH | Clown painting, vintage art |
| Colorful furniture | HIGH | Checkered chair, painted table |
| Functional obvious | MEDIUM | Plain chair, table |
| Generic decor | LOW | Basic vase, picture frame |

**Viral video items:** Clown painting + colorful checkered armchair → 485 shares

---

## Timeline Structure

```
Track 1 (top):    Text overlays
Track 2:         Sound effects (whoosh, pop, ding)
Track 3:         Voiceover (ElevenLabs)
Track 4:         Background music (20-30% volume)
Track 5 (bottom): Video footage
```

---

## Pacing Rules

### Cut Rhythm by Section

| Section | Duration | Cut Length | In Kdenlive |
|---------|----------|------------|-------------|
| Hook | 0-3s | **Hold shot** (no cuts) | Single clip, no razor |
| Preview | 3-10s | 1-1.5s per cut | Razor tool, tight cuts |
| Main content | 10s+ | **3-5s per cut** | Let clips breathe |
| App demo | When showing | 2-3s per cut | Match to narration |
| Ending | Last 10s | Hold or slow | Single scenic shot |

### What This Means
Your current 0.7s cuts are **too fast** for main content. Reserve fast cuts (0.7-1.5s) for the preview section only.

---

## DO ✅

### Cutting
- **Start video with action** - First frame should have movement
- **Cut on motion** - Make cuts during movement, not static moments
- **Remove ALL dead space** - Waiting at lights, stopping, looking around
- **Use J and L cuts** - Audio starts before/after video cut for smoothness
- **Match action cuts** - When switching angles, continue the motion

### Audio
- **Voice at 0dB** (full volume)
- **Music at -12dB to -15dB** (20-30% perceived volume)
- **SFX at -6dB to -9dB** (subtle but present)
- **Fade music under voice** - Use keyframes to duck music when speaking
- **Add whoosh to EVERY transition** in preview section

### Color
- **Basic correction first**: Exposure → Contrast → White balance
- **Add slight warmth** (+5-10 on orange/yellow) for inviting feel
- **Increase saturation slightly** (+10-15) for TikTok pop
- **Apply same correction to all clips** (copy/paste effect)

### Text Overlays
- **Hook text in first frame** - Large, readable
- **Use Kdenlive Title Clip** - Bold sans-serif font
- **White text + black outline** (3-4px) for readability
- **Keep in safe zone** - Not in top 10% or bottom 20%

### Pacing
- **3-second rule** - Something must change every 3 seconds (cut, zoom, text, sound)
- **Speed ramps** - 1.2x-1.5x for cycling footage to add energy
- **Slow motion** (0.5x) for item reveals

---

## AVOID ❌

### Cutting
- ❌ **Static shots longer than 5 seconds** - Viewers will scroll
- ❌ **Jump cuts in same frame** - Jarring without zoom punch
- ❌ **Cutting mid-word** - Always cut at natural speech pauses
- ❌ **0.7s cuts for main content** - Too fast, feels anxious
- ❌ **Fancy transitions** (wipes, dissolves) - Look amateur on TikTok

### Audio
- ❌ **Music louder than voice** - Voice must dominate
- ❌ **Abrupt music starts/ends** - Always fade in/out (0.5-1s)
- ❌ **Silence gaps** - Fill every moment with music or ambient
- ❌ **Mismatched energy** - Chill music on exciting find, or vice versa

### Visual
- ❌ **Text in bottom 20%** - TikTok UI covers it
- ❌ **Small text** - Must be readable on phone
- ❌ **Over-saturated colors** - Looks cheap
- ❌ **Shaky footage without stabilization** - Use Kdenlive's stabilize effect

### Content
- ❌ **Long intros** - No "hey guys", no logos, no buildup
- ❌ **Showing yourself stopping/waiting** - Only movement
- ❌ **Multiple topics in one video** - One find = one video
- ❌ **Ending abruptly** - Always have closing shot + CTA

---

## Kdenlive Shortcuts to Learn

| Action | Shortcut | Use For |
|--------|----------|---------|
| Razor tool | X | Quick cuts |
| Selection tool | S | Moving clips |
| Split clip | Shift+R | Cut at playhead |
| Delete gap | Right-click → Remove Space | Remove silence |
| Add keyframe | Click on effect line | Volume automation |
| Render | Ctrl+Enter | Export |

---

## Sound Effects Workflow

### Setup (One Time)
1. Download SFX pack (whoosh, pop, click, ding, rise)
2. Create folder: `~/Videos/Givore/SFX/`
3. Add to Kdenlive Project Bin for easy access

### Per Video
1. After rough cut, add SFX track
2. Place **whoosh** on every cut in preview section (3-10s)
3. Place **pop/ding** on item reveals
4. Place **subtle rise** before CTA
5. Adjust volume: -6dB to -9dB

---

## Color Correction Workflow

### Quick Method (Effects Panel)
1. Select all video clips
2. Add effect: **Color Correction** (or "SOP/Sat")
3. Adjust:
   - Lift shadows slightly (if too dark)
   - Reduce highlights (if sky blown out)
   - Add warmth (shift toward orange)
   - Increase saturation (+10-15)
4. Copy effect → Paste to all clips

### Using LUT (Faster)
1. Download free GoPro/Action Cam LUT
2. Add effect: **LUT** to clip
3. Select LUT file
4. Apply to all clips

---

## Export Checklist

Before rendering:
- [ ] Video starts with action (no black frames)
- [ ] Hook text visible in first frame
- [ ] Voice starts within 0.5 seconds
- [ ] No dead space or waiting
- [ ] Music fades under voice
- [ ] SFX on transitions
- [ ] Ends on strong visual
- [ ] Total length matches plan

### Export Settings (TikTok Optimized)
```
Preset: Custom
Codec: H.264
Resolution: 1080x1920
Frame rate: 30fps
Bitrate: Variable, Target 10Mbps
Audio: AAC 48kHz 192kbps
```

---

## Quick Reference Card

```
┌────────────────────────────────────────────┐
│         KDENLIVE VIRAL EDITING             │
├────────────────────────────────────────────┤
│ STRUCTURE                                  │
│ 0-3s:   Hook (HOLD shot, text overlay)     │
│ 3-10s:  Preview (1-1.5s cuts + whoosh)     │
│ 10-45s: Main (3-5s cuts, let it breathe)   │
│ Last 10s: Ending (scenic hold + CTA)       │
├────────────────────────────────────────────┤
│ AUDIO LEVELS                               │
│ Voice:  0dB (full)                         │
│ Music:  -12 to -15dB (background)          │
│ SFX:    -6 to -9dB (subtle)                │
├────────────────────────────────────────────┤
│ DO                                         │
│ ✓ Whoosh on preview cuts                   │
│ ✓ 3-5s cuts for main content               │
│ ✓ Speed up cycling to 1.2-1.5x             │
│ ✓ Text in safe zone (not top/bottom)       │
│ ✓ Warm color grade                         │
├────────────────────────────────────────────┤
│ AVOID                                      │
│ ✗ 0.7s cuts throughout (too fast)          │
│ ✗ Fancy transitions                        │
│ ✗ Music louder than voice                  │
│ ✗ Static shots >5 seconds                  │
│ ✗ Text in bottom 20%                       │
└────────────────────────────────────────────┘
```

---

## Stabilization (If Footage is Shaky)

1. Select shaky clip
2. Effects → **Stabilize** (vidstab)
3. Settings:
   - Shakiness: 4-6 (higher = more correction)
   - Accuracy: 8-10
   - Smoothing: 10-15
4. Render analysis first, then apply
5. Note: Crops edges slightly - account for this

---

## Speed Adjustments

### Speed Up Cycling (More Energy)
- Right-click clip → **Change Speed**
- Set to **120-150%** for cycling footage
- Use for long stretches of road

### Slow Motion (Item Reveal)
- Right-click clip → **Change Speed**
- Set to **50%** for dramatic reveal
- Works best with 60fps source footage

### Speed Ramp (Dynamic)
- Use **Time Remap** effect
- Add keyframes for speed changes
- Example: Normal → Slow (reveal) → Normal

---

## Template Project Setup

Create a template project with:
1. Correct project settings (1080x1920, 30fps)
2. Track layout (5 tracks as described above)
3. SFX clips in bin
4. Color correction preset saved
5. Text template for hook

Save as: `Givore_Template.kdenlive`

Duplicate for each new video to save setup time.
