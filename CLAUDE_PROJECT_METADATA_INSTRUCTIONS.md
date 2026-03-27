# Givore Multi-Platform Metadata Generator
## One Input → Five Platform Outputs (For Metricool)

---

## Task
Generate optimized titles, descriptions, and hashtags for 5 platforms from a single video script. Output is copy-paste ready for Metricool's multi-platform scheduling.

## Input
1. **Project**: Givore (default)
2. **Script**: Full transcription/speech from the video

---

## Project: GIVORE

**What**: Social recycling app - users share street finds, give away items, search for used things.
**Where**: Spain (founded in Valencia, expanding nationally)
**Content**: Cycling + street finds + community sharing + app demos
**Language**: Spanish (Spain)
**Core message**: "No es comprar ni vender. Es dar y encontrar."

---

## Unified Keyword Strategy (Web + App Store + Social)

Based on Keywords Everywhere data (Spain, March 2026). Use volume-backed terms across all platforms.

### Social Media Keywords (use in captions + hashtags)

**Tier 1 — ALWAYS include 1-2:**
- "segunda vida" (8,500/mo) — brand differentiator
- "consumo consciente" (34,000/mo) — HIGH VOLUME, underused
- "segunda mano" (65,000/mo nationally) — category term

**Tier 2 — ROTATE per video topic:**
- "se regala" (3,700/mo) — perfect for giveaway content
- "reciclaje creativo" (14,000/mo) — for upcycling/creative content
- "reciclar muebles" (15,000/mo) — for furniture-specific content

**Tier 3 — HYPERLOCAL (always include 1, rotate for expansion):**
- [target city] + optionally [barrio name] if shown in video
- Rotation: Madrid (250K) → Barcelona (170K) → Valencia (140K) → Sevilla (110K) → Málaga (93K) → Zaragoza (93K) → others
- When video shows a specific city, use that city. Otherwise, rotate target cities.

### Deprecated Terms (zero or near-zero search volume)
DO NOT prioritize in hashtags or captions:
- "reciclaje social" (0/mo) — keep as brand tagline in descriptions only, NOT as hashtag
- "hallazgos callejeros" (0/mo)
- "dar y encontrar" (0/mo) — tagline only, not hashtag
- "street finds" (0/mo in Spain)
- "eco friendly" (0/mo in Spain)
- "treasure hunting" (0/mo in Spain)
- "vida sostenible" (840/mo) — low volume, deprioritize

### WEB/SEO ONLY (never on social — commercial penalty risk)
- "gratis", "cosas gratis" (39K/mo), "muebles gratis" (3K/mo)
- Social platforms commercially deprioritize "gratis/free" content

### APP STORE ONLY
- "cosas gratis cerca", "donar objetos", "regalar cosas"

**Rule**: Each platform description must contain at least 1 Tier 1 keyword naturally in the first sentence.

---

## Geographic Framing (National Expansion)

Content presents the NATIONAL concept of social recycling / sharing culture across Spain.

- Titles/descriptions: General concept (works for any Spanish city), not city-locked
- Hashtags: Include target city name as hyperlocal tag (rotate cities for expansion)
- When video SHOWS a specific city, reference it naturally — but framing should work nationally
- City name goes in hashtags (hyperlocal targeting), not necessarily in hook/title

**Framing examples:**
| OLD (Valencia-locked) | NEW (nationally framed) |
|----------------------|------------------------|
| "Valencia esconde tesoros en cada esquina" | "Lo que la gente tira en España... y lo que otros encuentran" |
| "Paseando por Valencia encontré..." | "Salí en bici y mira lo que encontré en la calle..." |
| "En Valencia la gente tira muebles" | "En España se tiran miles de muebles que están perfectamente" |

---

## Output Format

Generate TWO separate files:

### FILE 1: Descriptions (metadata/[date]_[topic]-descriptions.txt)

```
═══════════════════════════════════════════════════════════
                       FACEBOOK
═══════════════════════════════════════════════════════════

{title}

{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       INSTAGRAM
═══════════════════════════════════════════════════════════

{title}

{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       LINKEDIN
═══════════════════════════════════════════════════════════

{title}

{description}

{hashtags}

═══════════════════════════════════════════════════════════
                        TIKTOK
═══════════════════════════════════════════════════════════

{title}

{description}

{hashtags}

═══════════════════════════════════════════════════════════
                    YOUTUBE SHORTS
═══════════════════════════════════════════════════════════

{title}

{description}

{hashtags}
```

### FILE 2: Captions (metadata/[date]_[topic]-captions.txt)

```
{formatted captions - 2-3 words per line, blank line between each}
```

---

## Platform-Specific Rules

### FACEBOOK
**Tone**: Community-focused, conversational, warm

**Title formula**: `[Community hook] + [Emotional angle]`
- Speak to community (not city-locked)
- Warmer, more personal

**Title examples**:
- "Mirad lo que me encontré hoy en la calle..."
- "¿Alguien más hace esto por el barrio?"
- "Esto es lo que pasa cuando compartes antes de tirar"

**Description**:
- Write 2 short paragraphs + engagement question (concise > long on Facebook)
- Paragraph 1: What happened — items found, condition, neighborhood if shown in video
- Paragraph 2: Givore connection — how sharing works, community angle
- End with question asking for personal experiences or stories
- First sentence must contain a Tier 1 keyword naturally
- Include specific details from the video (not generic copy)

**Hashtags**: 3-5
```
#SegundaVida #ConsumoConsciente #[target city] #[barrio if shown] #[contextual]
```

---

### INSTAGRAM
**Tone**: Aesthetic, lifestyle, inspirational — caption-first approach

**Title formula**: `[Keyword-rich hook within 125 chars] + [Emoji]`
- First 125 characters = PRIMARY discoverability (2026: captions outweigh hashtags)
- Must contain at least 1 Tier 1 keyword in first sentence
- Lifestyle angle, not city-locked

**Title examples**:
- "Segunda vida para lo que otros descartan ✨"
- "Consumo consciente empieza en tu barrio 🌱"
- "¿Por qué tiramos cosas que aún sirven? 🛋️"

**Description**:
- Write 3-4 paragraphs with storytelling approach
- Paragraph 1 (CRITICAL — first 125 chars): Keyword-rich hook with specific item details. This is the primary search/discovery surface.
- Paragraph 2: Emotional significance + how @givore.app works naturally
- Paragraph 3: Community impact — sharing connects people, real impact
- Paragraph 4: End with DM-worthy statement (DM shares = strongest IG algorithm signal in 2026). Example: "Envía esto a alguien que necesite saberlo" or a statement so relatable people forward it.
- Include specific details from the video (not generic copy)

**Hashtags**: 3-5 (2026: fewer hashtags, stronger captions)
```
#SegundaVida #ConsumoConsciente #[target city] #[barrio if shown] #[contextual Tier 2]
```
- ALWAYS: 1 Tier 1 + 1 hyperlocal city + 1-2 contextual
- NEVER: #StreetFinds, #TreasureHunting, #EcoFriendly, #VidaSostenible (0 or near-0 vol in Spain)

---

### LINKEDIN
**Tone**: Personal narrative, reflective, professional

**Title formula**: `[Personal observation] + [Professional reflection]`
- Lead with personal story or observation, NOT statistics
- Sustainability as human story, not corporate newsletter

**Title examples**:
- "Hoy encontré un mueble perfecto tirado en la acera. Y me hizo pensar..."
- "Algo está cambiando en cómo los vecinos comparten cosas"
- "Lo que aprendí montando una app de economía circular en España"

**Description**:
- Personal storytelling tone (first person, not corporate)
- NO EXTERNAL LINKS (LinkedIn penalizes external links with ~60% reach reduction in 2026)
- Frame as personal reflection or learning, not pitch
- Mention Givore naturally as part of the story
- End with thought-provoking question
- First sentence must contain a Tier 1 keyword naturally

**Hashtags**: 3 max (professional)
```
#EconomíaCircular #Sostenibilidad #[target city]
```
- NEVER: #Startups, #Innovación (generic/commercial, low engagement)

---

### TIKTOK
**Tone**: Casual, fun, emoji-heavy, direct

**Title formula**: `[Emoji] + [Emotional/Curiosity hook]`
- Max 100 characters
- 1-2 emojis
- Prioritize OUTRAGE/SURPRISE or URGENCY hooks (top-performing patterns)
- NOT city-locked in title

**Title examples**:
- "¿Por qué la gente tira cosas así de buenas? 🤯"
- "Todo esto me lo encontré en la calle 🛋️ ¡Flipante!"
- "🪑 Esto pasó AYER y no me lo puedo creer..."

**Description**:
- Write 3-4 paragraphs with energy and conversational tone
- Paragraph 1: What happened — items found, neighborhoods, reactions (specific details)
- Paragraph 2: The problem context — why things end up abandoned, what could be different
- Paragraph 3: How Givore fits — explained naturally, how the app works
- Paragraph 4: Engaging question for comments that invites personal stories
- Casual language (tú/vosotros), not salesy
- Include specific video details
- First sentence must contain a Tier 1 keyword naturally
- NO commercial terms ("gratis", "oferta", "descuento") in description, spoken audio, or on-screen text — TikTok AI scans all three layers

**Hashtags**: 3-5
```
#SegundaVida #ConsumoConsciente #[target city] #SeRegala #[contextual]
```
- NEVER: #ReciclajeSocial (0 vol), #CazaDeTesoros (0 vol), #gratis (commercial penalty)

---

### YOUTUBE SHORTS
**Tone**: Searchable, educational, clear

**Title formula**: `[SEO keyword phrase] + [Emoji]`
- Think: what would someone SEARCH for?
- Do NOT put #Shorts in title (YouTube auto-detects vertical Shorts; wastes characters)
- Do NOT use "GRATIS" in titles (commercially deprioritized)
- Not city-locked unless video shows specific location

**Title examples**:
- "Encontré muebles de segunda mano perfectos tirados en la calle 🛋️"
- "Consumo consciente: lo que otros tiran, tú lo aprovechas 🌱"
- "Así funciona el reciclaje entre vecinos en España ♻️"

**Description**:
- 1-2 sentences max (completion rate drives Shorts visibility, not metadata)
- Start with searchable summary containing Tier 1 keyword
- Explain what Givore is briefly (YouTube audience may not know)
- Include call to comment

**Hashtags**: 3-5 (SEO focused, lowercase)
```
#shorts #segundavida #consumoconsciente #[target city] #givore
```
- NEVER: #gratis (commercial penalty), excessive hashtags (dilutes signal)

---

## Caption Formatting Rules (Same for All Platforms)

### Requirements
1. DO NOT change the script text - only format it
2. Each line = one caption (2-3 words maximum)
3. Blank line between each caption
4. Break sentences aggressively for readability
5. Split at ANY natural pause point
6. Do NOT add any formatting markers - captions must be plain text only (no asterisks, no bold, no special characters). The subs tool needs clean text for SRT generation.

### Split at:
- Periods, question marks, exclamations
- Commas (always)
- Ellipsis (...)
- "Y", "Pero", "Porque", "Es que" (transition words)
- After 2-3 words regardless of punctuation

### Breaking rules:
- Prioritize short lines over complete thoughts
- 2-3 words per line is MANDATORY
- Break mid-sentence if needed for word count
- Single word lines are acceptable for emphasis

---

## Caption Example

**Input**: "¿Sabéis qué? Valencia está llena de tesoros y la gente pasa de largo."

**Output**:
```
¿Sabéis qué?

Valencia está llena

de tesoros...

y la gente

pasa de largo.
```

### Full Caption Example:

```
¿Sabéis qué?

Valencia está llena

de tesoros...

y la mayoría

de la gente

pasa de largo.

Mira,

todo esto

me lo encontré

en la calle.

Sillas, mesas...

hasta este mueble

tan guapo.

El problema es

que la gente

tira cosas

perfectamente bien.

Por eso

uso Givore.

Abro la app,

subo las fotos...

y en menos

de veinte segundos

cualquiera puede verlo.

Eso es

reciclaje social.

Dar y encontrar.
```

---

## Complete Example

### Input
```
Project: Givore
Script: ¿Sabéis qué? Valencia está llena de tesoros y la mayoría de la gente pasa de largo. Mira, todo esto me lo encontré en la calle. Sillas, mesas, hasta este mueble tan guapo. El problema es que la gente tira cosas perfectamente bien. Por eso uso Givore. Abro la app, subo las fotos, y en menos de veinte segundos cualquiera puede verlo. Eso es reciclaje social. Dar y encontrar.
```

### Output FILE 1: Descriptions (metadata/2026-01-16_hallazgos-calle-descriptions.txt)

```
═══════════════════════════════════════════════════════════
                       FACEBOOK
═══════════════════════════════════════════════════════════

Mirad lo que me encontré hoy tirado en la calle...

Sillas, mesas, un mueble precioso... todo con segunda vida posible, tirado en la acera. Salí en bici y me los encontré en Valencia, perfectamente bien. Con Givore los subí en segundos para que alguien del barrio los aproveche.

¿Vosotros habéis encontrado algo bueno alguna vez en la calle? ¡Contadme vuestra historia!

#SegundaVida #ConsumoConsciente #Valencia #Reciclaje

═══════════════════════════════════════════════════════════
                       INSTAGRAM
═══════════════════════════════════════════════════════════

Sillas, mesas y un mueble con segunda vida esperando en la acera ♻️

Todo esto estaba tirado en la calle. Perfectamente bien. La gente pasa de largo sin verlo, pero para alguien cercano puede ser justo lo que necesita.

Con @givore.app lo subes en segundos y conectas con quien lo quiere. Consumo consciente empieza así: compartiendo antes de tirar 🌱

Envía esto a alguien que necesite muebles — puede que encuentre lo que busca.

#SegundaVida #ConsumoConsciente #Valencia #SeRegala

═══════════════════════════════════════════════════════════
                       LINKEDIN
═══════════════════════════════════════════════════════════

Hoy encontré sillas, mesas y un mueble perfecto tirados en la acera. Y me hizo pensar.

Salí a dar una vuelta en bici y me encontré todo esto en la calle. Segunda mano, en buen estado, esperando a que alguien lo aprovechara. Nadie lo hacía.

Con Givore intentamos cambiar eso: subes lo que encuentras, alguien del barrio lo recoge. Sin intermediarios, sin dinero. Solo conectar a quien tiene con quien necesita. Economía circular en su forma más simple.

¿Creéis que la cultura de compartir puede escalar más allá de los barrios?

#EconomíaCircular #Sostenibilidad #Valencia

═══════════════════════════════════════════════════════════
                        TIKTOK
═══════════════════════════════════════════════════════════

¿Por qué la gente tira cosas así de buenas? 🤯

Muebles de segunda mano perfectos, tirados en la calle. Sillas, mesas, un mueble precioso... todo con segunda vida posible.

Lo subí a Givore en segundos y alguien del barrio vino a buscarlo. Así funciona el consumo consciente: compartir antes de tirar 🌱

¿Cuál es lo mejor que habéis encontrado en la calle? 👇

#SegundaVida #ConsumoConsciente #Valencia #SeRegala #ReciclajeCreativo

═══════════════════════════════════════════════════════════
                    YOUTUBE SHORTS
═══════════════════════════════════════════════════════════

Muebles de segunda mano perfectos tirados en la calle 🛋️

Sillas, mesas y un mueble precioso encontrados en la acera, todos en buen estado. Con Givore los subes en segundos y alguien cercano les da una segunda vida.

¿Habéis encontrado algo así? ¡Contadme!

#shorts #segundavida #consumoconsciente #valencia #givore
```

### Output FILE 2: Captions (metadata/2026-01-16_hallazgos-calle-captions.txt)

```
¿Sabéis qué?

Valencia está llena

de tesoros...

y la mayoría

de la gente

pasa de largo.

Mira,

todo esto

me lo encontré

en la calle.

Sillas, mesas...

hasta este mueble

tan guapo.

El problema es

que la gente

tira cosas

perfectamente bien.

Por eso

uso Givore.

Abro la app,

subo las fotos...

y en menos

de veinte segundos

cualquiera puede verlo.

Eso es

reciclaje social.

Dar y encontrar.
```

---

## Quality Checklist

Before outputting, verify:
- [ ] All 5 platforms have unique titles matching their tone
- [ ] Facebook: Community tone, 2 paragraphs + question, 3-5 hashtags
- [ ] Instagram: Caption-first (first 125 chars = keyword hook), @givore.app, 3-5 hashtags, ends with DM-shareable statement
- [ ] LinkedIn: Personal narrative, NO external links, 3 hashtags max
- [ ] TikTok: Casual + emoji, no commercial terms ("gratis"), 3-5 hashtags
- [ ] YouTube: Search-intent title (NO #Shorts in title, NO "GRATIS"), 3-5 hashtags
- [ ] No platform uses "gratis" in any form (commercially deprioritized)
- [ ] Each platform has at least 1 Tier 1 keyword ("segunda vida", "consumo consciente", "segunda mano") in first sentence
- [ ] Hashtags use volume-backed terms only (no #ReciclajeSocial, #StreetFinds, #TreasureHunting, #EcoFriendly)
- [ ] At least 1 hyperlocal city hashtag per platform
- [ ] Titles/descriptions are nationally framed (not Valencia-locked) unless video shows specific city
- [ ] Captions formatted correctly (2-3 words per line, no text changes)
- [ ] Captions are plain text only (no asterisks or formatting markers)
- [ ] Spanish is informal except LinkedIn (which can be either)
- [ ] Each description mentions Givore naturally
- [ ] Two separate files generated (descriptions + captions)

---

## Language Note
All outputs in **Spanish (Spain)** - peninsular expressions, "vosotros" form, avoid Latin American variations.

---

## SEO Keyword Tiers

Volume-backed keywords from keyword research (Spain, March 2026). Integrate these naturally into descriptions across all platforms to boost discoverability.

### Tier 0 — MEGA Keywords (670K+ combined — #1 keyword opportunity)

The "segunda mano [CIUDAD]" pattern is the single highest-volume keyword opportunity. Use the city matching the video content.

| Keyword | Monthly Volume | Use When |
|---------|---------------|----------|
| segunda mano Madrid | 250K | Any Madrid content or national framing |
| segunda mano Barcelona | 170K | Any Barcelona content |
| segunda mano Valencia | 140K | Any Valencia content |
| segunda mano Sevilla | 110K | Any Sevilla content |
| consumo responsable | 57K | Mission-driven, sustainability content |

**Rule**: When content is city-specific, ALWAYS include "segunda mano [CIUDAD]" in the description body (not necessarily first sentence — Tier 1 keywords still own the opening).

### Tier 1 — High Volume (use in FIRST sentence of every description)

At least ONE of these must appear naturally in the opening sentence:

| Keyword | Monthly Volume | Use When |
|---------|---------------|----------|
| muebles reciclados | 86K | Any furniture find content |
| muebles segunda mano | 65K | Any used furniture content |
| consumo responsable | 57K | Sustainability-angle content |
| restaurar muebles | 28K | Restoration, before/after content |
| reciclar muebles | 15K | Core recycling content |
| reciclaje creativo | 14K | Upcycling, creative transformation content |

### Tier 2 — Medium Volume (use 1-2 per description, rotate)

| Keyword | Monthly Volume | Use When |
|---------|---------------|----------|
| muebles vintage | 150K | Vintage/retro style finds (high volume — always use when applicable) |
| muebles con palets | 95K | Palet furniture, DIY content |
| rastro Madrid | 63K | Madrid flea market / secondhand culture content |
| economia colaborativa | 16K | App positioning, sharing economy angle |
| muebles restaurados | 13K | After restoration, transformation reveals |
| movilidad sostenible | 9.2K | Cycling + sustainability intersection |
| decoracion reciclada | 6.7K | Home decor angle content |
| vender muebles usados | 5.5K | Secondhand furniture market content |
| decoracion low cost | 4.5K | Budget living, affordable decor content |
| mesa reciclada | 7.4K | Table/furniture finds |
| restaurar muebles antiguos | 7.1K | Antique restoration content |
| app segunda mano | 3K | App discovery / Givore positioning content |
| carril bici [CIUDAD] | 10-15K | Cycling-focused content (substitute video's city) |
| [CIUDAD] en bici | 1-10K | Cycling discovery content |

### Tier 3 — City-Specific (use matching the video's location)

Use the city shown in the video. Rotate cities for national expansion.

**"Segunda mano [CIUDAD]" — MEGA pattern (670K combined):**
| Keyword | Monthly Volume |
|---------|---------------|
| segunda mano Madrid | 250K |
| segunda mano Barcelona | 170K |
| segunda mano Valencia | 140K |
| segunda mano Sevilla | 110K |

**Secondhand furniture by city:**
| Keyword | Monthly Volume |
|---------|---------------|
| muebles segunda mano Madrid | 15K |
| muebles segunda mano Barcelona | 10K |
| muebles segunda mano Valencia | 7.7K |
| muebles segunda mano Sevilla | 6.7K |
| muebles segunda mano Zaragoza | 5.5K |
| muebles segunda mano Malaga | 4.5K |
| muebles segunda mano Granada | 3K |
| muebles segunda mano Alicante | 2.5K |
| muebles segunda mano Palma | 1.1K |

**Mudanzas by city (moving = decluttering opportunity):**
| Keyword | Monthly Volume |
|---------|---------------|
| mudanzas Madrid | 41K |
| mudanzas Barcelona | 34K |
| mudanzas Valencia | 18K |

**Punto limpio by city (waste disposal = recycling content):**
| Keyword | Monthly Volume |
|---------|---------------|
| punto limpio Madrid | 18K |
| punto limpio Sevilla | 5.5K |

**Cycling by city:**
| Keyword | Monthly Volume |
|---------|---------------|
| carril bici Madrid | 15K |
| carril bici Barcelona | 12K |
| carril bici Valencia | 10K |
| en bici por Madrid | 10K |
| carril bici Sevilla | 5.5K |
| carril bici Zaragoza | 4.5K |
| rutas bici Madrid | 4.5K |
| carril bici Malaga | 3K |
| rutas bici Barcelona | 1.6K |
| rutas bici Valencia | 1.6K |
| rutas bici Sevilla | 1.1K |

**Neighborhoods by city:**
| Keyword | Monthly Volume |
|---------|---------------|
| barrios Madrid | 10K |
| barrios Barcelona | 7.7K |
| barrios Valencia | 3.7K |
| barrios Sevilla | 2.5K |

### Tier 4 — Related Long-Tail (use opportunistically)

- restaurar muebles de madera, restaurar muebles vintage, ideas para restaurar muebles viejos
- como pintar muebles de madera (2.5K)
- wallapop muebles [CIUDAD], muebles segunda mano particulares
- reciclaje creativo ideas, reciclar cosas viejas, reciclar objetos caseros
- gatos callejeros (3K), perros [CIUDAD] (2.5K) — for pet content

### WEB/SEO ONLY (never on social — commercial penalty risk)

These have real volume but are banned from social media descriptions. Use on website, app store, blog, SEO pages only.

| Keyword | Monthly Volume | Platform |
|---------|---------------|----------|
| cosas gratis | 39K | Web/SEO only |
| muebles gratis | 3K | Web/SEO only |
| muebles gratis Madrid | 1.3K | Web/SEO only |
| regalo muebles Madrid | 1.3K | Web/SEO only |
| muebles gratis Barcelona | 540 | Web/SEO only |

**Rule**: "gratis" is commercially deprioritized by all social platforms. Use "se regala", "compartido", "segunda vida" instead in social content.

### Integration Rules

1. **First sentence**: Must contain at least 1 Tier 1 keyword naturally
2. **City content**: Include "segunda mano [CIUDAD]" (Tier 0) in description body when city-specific
3. **Body**: Include 1-2 Tier 2 keywords where relevant
4. **Local content**: Add 1 Tier 3 keyword matching the city shown in the video (not always Valencia)
5. **Mudanzas/punto limpio angle**: When content relates to moving or waste disposal, reference these keywords naturally
6. **Never force keywords** — if it reads awkwardly, rephrase or skip
7. **Complement existing keyword strategy** — these Tiers work alongside the Unified Keyword Strategy above (segunda vida, consumo consciente, segunda mano)
