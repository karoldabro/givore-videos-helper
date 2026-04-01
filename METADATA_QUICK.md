# Metadata Quick Reference
<!-- Condensed from CLAUDE_PROJECT_METADATA_INSTRUCTIONS.md — update both files together -->

## Keyword Tiers

**Tier 1 (ALWAYS include 1-2):**
- "segunda vida" (8.5K/mo), "consumo consciente" (34K/mo), "segunda mano" (65K/mo)

**Tier 2 (ROTATE per topic):**
- "se regala" (3.7K), "reciclaje creativo" (14K), "reciclar muebles" (15K)

**Tier 3 (HYPERLOCAL — always 1):**
- [target city] + [barrio if shown]. Rotate: Madrid > Barcelona > Valencia > Sevilla > others

**Deprecated (zero volume — never hashtag):**
- "reciclaje social", "hallazgos callejeros", "dar y encontrar", "street finds", "eco friendly"

**WEB/SEO ONLY (never social):**
- "gratis", "cosas gratis", "muebles gratis" — social platforms penalize commercially

**Rule**: Each platform description must contain at least 1 Tier 1 keyword in the first sentence.

## Geographic Framing

- Frame nationally, not city-locked
- City name in hashtags (hyperlocal), not necessarily in hook/title
- When video shows a specific city, reference naturally but framing works for any Spanish city

## Platform Rules

### FACEBOOK
- **Tone**: Community, conversational, warm
- **Title**: Community hook + emotional angle
- **Description**: 2 short paragraphs + engagement question. First sentence = Tier 1 keyword.
- **Hashtags**: 3-5: `#SegundaVida #ConsumoConsciente #[city] #[barrio] #[contextual]`

### INSTAGRAM
- **Tone**: Aesthetic, lifestyle, inspirational
- **Title**: Keyword-rich hook within 125 chars + emoji. First 125 chars = primary discovery surface (2026: captions > hashtags).
- **Description**: 3-4 paragraphs. P1: keyword hook with item details. P2: @givore.app mention. P3: community impact. P4: DM-worthy statement.
- **Hashtags**: 3-5: 1 Tier 1 + 1 city + 1-2 contextual. NEVER: #StreetFinds, #EcoFriendly

### LINKEDIN
- **Tone**: Personal narrative, reflective, professional
- **Title**: Personal observation + professional reflection
- **Description**: First person storytelling. NO external links (60% reach penalty). End with question. Tier 1 keyword in first sentence.
- **Hashtags**: 3 max: `#EconomiaCircular #Sostenibilidad #[city]`

### TIKTOK
- **Tone**: Casual, emoji-heavy, direct
- **Title**: Max 100 chars. 1-2 emojis. Outrage/surprise/urgency hooks.
- **Description**: 3-4 paragraphs, casual (tu/vosotros). NO "gratis"/"oferta"/"descuento" anywhere. Tier 1 keyword first sentence.
- **Hashtags**: 3-5: `#SegundaVida #ConsumoConsciente #[city] #SeRegala #[contextual]`. NEVER: #gratis

### YOUTUBE SHORTS
- **Tone**: Searchable, educational, clear
- **Title**: SEO keyword phrase + emoji. NO #Shorts in title. NO "GRATIS".
- **Description**: 1-2 sentences max. Searchable summary with Tier 1 keyword. Brief Givore explanation.
- **Hashtags**: 3-5: `#shorts #segundavida #consumoconsciente #[city] #givore`

## Caption Rules

1. **Plain text only** — no asterisks, bold, formatting
2. **2-3 words per line** — mandatory, break mid-sentence if needed
3. **Blank line between each caption group**
4. **Split at**: periods, commas, ellipsis, "Y"/"Pero"/"Porque"/"Es que"
5. **Strip section labels** — no [SECTION:], HOOK:, CTA: etc.
6. **Preserve script words exactly** — only reformat, don't change text

## Thumbnail

- 5-7 words, ALL CAPS, Spanish
- Power words: GRATIS, MIRA, ENCUENTRA, SECRETO, NUEVO
- No punctuation
- Must capture the video's main hook

## Output Files

Write to VARIANT_FOLDER:
- `descriptions.txt` — THUMBNAIL + 5 platforms (Facebook, Instagram, LinkedIn, TikTok, YouTube)
- `captions.txt` — 2-3 word/line formatted script
