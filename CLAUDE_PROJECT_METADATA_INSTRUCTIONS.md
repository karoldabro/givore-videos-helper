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
**Where**: Valencia, Spain
**Content**: Cycling + treasure hunting + app demos
**Language**: Spanish (Spain)
**Core message**: "No es comprar ni vender. Es dar y encontrar."

---

## Output Format

Generate this EXACT structure for easy copy-paste to Metricool:

```
═══════════════════════════════════════════════════════════
                        TIKTOK
═══════════════════════════════════════════════════════════

TÍTULO:
{title}

DESCRIPCIÓN:
{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       INSTAGRAM
═══════════════════════════════════════════════════════════

TÍTULO:
{title}

DESCRIPCIÓN:
{description}

{hashtags}

═══════════════════════════════════════════════════════════
                    YOUTUBE SHORTS
═══════════════════════════════════════════════════════════

TÍTULO:
{title}

DESCRIPCIÓN:
{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       FACEBOOK
═══════════════════════════════════════════════════════════

TÍTULO:
{title}

DESCRIPCIÓN:
{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       LINKEDIN
═══════════════════════════════════════════════════════════

TÍTULO:
{title}

DESCRIPCIÓN:
{description}

{hashtags}

═══════════════════════════════════════════════════════════
                       SUBTÍTULOS
═══════════════════════════════════════════════════════════

{formatted captions - same for all platforms}
```

---

## Platform-Specific Rules

### TIKTOK
**Tone**: Casual, fun, emoji-heavy, direct

**Title formula**: `[Emoji] + [Curiosity hook] + [Optional location]`
- Max 100 characters
- 1-2 emojis
- Create curiosity gap

**Title examples**:
- "Todo esto me lo encontré en la calle 🛋️ ¡Flipante!"
- "🪑 Mirad lo que tira la gente en Valencia..."
- "¿Por qué la gente tira cosas así de buenas? 🤯"

**Description**:
- 2-3 short paragraphs
- Casual language (tú/vosotros)
- End with question for comments
- Givore mention natural, not salesy

**Hashtags**: Exactly 5
```
#Givore #SegundaVida #ReciclajeSocial #Valencia #[contextual]
```

---

### INSTAGRAM
**Tone**: Aesthetic, lifestyle, inspirational

**Title formula**: `[Aesthetic statement] + [Emoji]`
- Slightly more polished than TikTok
- Lifestyle angle

**Title examples**:
- "Valencia esconde tesoros en cada esquina ✨"
- "Reciclaje social en acción 🌱"
- "Lo bonito de dar una segunda vida 🛋️"

**Description**:
- 2-3 paragraphs
- Lifestyle/aesthetic tone
- Include "Guarda este post" or save CTA
- Tag @givore.app

**Hashtags**: 7-10 (mix popular + niche)
```
#SegundaVida #Valencia #Sostenibilidad #StreetFinds #ReciclajeSocial #VidaSostenible #ConsumoConsciente #Givore #[neighborhood] #[contextual]
```

---

### YOUTUBE SHORTS
**Tone**: Searchable, educational, clear

**Title formula**: `[SEO keyword phrase] + [Emoji] + #Shorts`
- Think: what would someone SEARCH for?
- Include location for local SEO

**Title examples**:
- "Cómo encontrar muebles GRATIS en Valencia 🛋️ #Shorts"
- "Encontré esto TIRADO en la calle | Valencia #Shorts"
- "Reciclaje social: qué es y cómo funciona 🌱 #Shorts"

**Description**:
- Start with searchable summary sentence
- Explain what Givore is (YouTube audience may not know)
- Include call to comment

**Hashtags**: 5-7 (SEO focused, lowercase)
```
#shorts #valencia #reciclaje #muebles #gratis #sostenibilidad #givore
```

---

### FACEBOOK
**Tone**: Community-focused, local, conversational

**Title formula**: `[Community hook] + [Location]`
- Speak to local community
- Warmer, more personal

**Title examples**:
- "Mirad lo que me encontré hoy por Valencia..."
- "¿Alguien más hace esto por el barrio?"
- "Esto es lo que encontré paseando por Russafa"

**Description**:
- Can be longer (Facebook users read more)
- Community angle strong
- Ask for experiences/stories
- Explain Givore for older audience

**Hashtags**: 5
```
#Valencia #Reciclaje #SegundaVida #Sostenibilidad #[neighborhood]
```

---

### LINKEDIN
**Tone**: Professional, business value, data-driven

**Title formula**: `[Statistic or insight] + [Professional angle]`
- Lead with data or business insight
- Sustainability as business opportunity

**Title examples**:
- "El 40% de los muebles desechados en España están en perfecto estado"
- "Economía circular: de problema a oportunidad"
- "Cómo la tecnología está transformando el reciclaje urbano"

**Description**:
- Professional tone (usted acceptable, but vosotros also OK)
- Frame as innovation/business/sustainability story
- Mention Givore as solution/startup
- End with thought-provoking question

**Hashtags**: 5 (professional)
```
#EconomíaCircular #Sostenibilidad #Innovación #Valencia #Startups
```

---

## Caption Formatting Rules (Same for All Platforms)

### Requirements
1. DO NOT change the script text - only format it
2. Each line = one caption (5-8 words ideal)
3. Blank line between each caption
4. Keep complete thoughts together
5. Split at natural pauses, punctuation, breath points

### Split at:
- Periods, question marks, exclamations
- Commas (when natural pause)
- Ellipsis (...)
- "Y", "Pero", "Porque" (transition words)

### Never split:
- Mid-sentence without punctuation
- Subject from verb
- Verb from object
- Short phrases under 4 words

### Example:
**Input**: "¿Sabéis qué? Valencia está llena de tesoros y la gente pasa de largo."

**Output**:
```
¿Sabéis qué?

Valencia está llena de tesoros...

y la gente pasa de largo.
```

---

## Complete Example

### Input
```
Project: Givore
Script: ¿Sabéis qué? Valencia está llena de tesoros y la mayoría de la gente pasa de largo. Mira, todo esto me lo encontré en la calle. Sillas, mesas, hasta este mueble tan guapo. El problema es que la gente tira cosas perfectamente bien. Por eso uso Givore. Abro la app, subo las fotos, y en menos de veinte segundos cualquiera puede verlo. Eso es reciclaje social. Dar y encontrar.
```

### Output

```
═══════════════════════════════════════════════════════════
                        TIKTOK
═══════════════════════════════════════════════════════════

TÍTULO:
Todo esto me lo encontré en la calle 🛋️ ¡Valencia está llena de tesoros!

DESCRIPCIÓN:
Hoy salí a dar una vuelta por Valencia y mirad lo que me encontré tirado: sillas, mesas, ¡hasta un mueble precioso! Todo perfectamente bien.

El problema es que la gente tira cosas que todavía sirven. Por eso uso Givore - subo lo que encuentro y cualquiera cerca puede darle una segunda vida. Reciclaje social en acción 🌱

¿Cuál es el mejor hallazgo que habéis encontrado en la calle? 👇

#Givore #SegundaVida #ReciclajeSocial #Valencia #CazaDeTesoros

═══════════════════════════════════════════════════════════
                       INSTAGRAM
═══════════════════════════════════════════════════════════

TÍTULO:
Valencia esconde tesoros en cada esquina ✨

DESCRIPCIÓN:
Sillas, mesas, muebles preciosos... todo esto estaba tirado en la calle. La gente pasa de largo sin verlo, pero para mí son auténticos tesoros esperando una segunda vida ♻️

Lo bonito es poder compartirlo. Con @givore.app subo lo que encuentro para que otra persona lo aproveche. No es comprar ni vender - es dar y encontrar. Eso es reciclaje social 🌱

Guarda este post si te mola la idea 📌

#SegundaVida #Valencia #Sostenibilidad #StreetFinds #ReciclajeSocial #VidaSostenible #ConsumoConsciente #Givore #TreasureHunting #EcoFriendly

═══════════════════════════════════════════════════════════
                    YOUTUBE SHORTS
═══════════════════════════════════════════════════════════

TÍTULO:
Cómo encontrar muebles GRATIS en Valencia 🛋️ #Shorts

DESCRIPCIÓN:
En Valencia la gente tira muebles, sillas y cosas que están perfectamente bien. En este video te enseño cómo encontrarlos y qué hacer con ellos.

Uso Givore, una app de reciclaje social donde subes lo que encuentras para que otros lo aprovechen. En menos de 20 segundos cualquiera cerca puede verlo y recogerlo.

¿Conocíais este truco? ¡Contadme en los comentarios!

#shorts #valencia #muebles #gratis #reciclaje #sostenibilidad #givore

═══════════════════════════════════════════════════════════
                       FACEBOOK
═══════════════════════════════════════════════════════════

TÍTULO:
Mirad lo que me encontré hoy paseando por Valencia...

DESCRIPCIÓN:
Hoy salí a dar una vuelta en bici por Valencia y no me lo podía creer: sillas, mesas, un mueble precioso... ¡todo tirado en la calle! Y estaba perfectamente bien.

Es una pena que la gente tire cosas así cuando hay quien las necesita. Por eso uso Givore - una app donde puedes compartir lo que encuentras para que otra persona le dé una segunda vida. Sin comprar ni vender, solo dar y encontrar. Así funciona el reciclaje social.

¿Vosotros habéis encontrado algo bueno alguna vez en la calle? ¡Contadme vuestra experiencia, me encanta leer vuestras historias!

#Valencia #Reciclaje #SegundaVida #Sostenibilidad #ComunidadValencia

═══════════════════════════════════════════════════════════
                       LINKEDIN
═══════════════════════════════════════════════════════════

TÍTULO:
El 40% de los muebles desechados en España están en perfecto estado

DESCRIPCIÓN:
Cada día se tiran toneladas de muebles, electrodomésticos y objetos que funcionan perfectamente. Es un problema medioambiental, pero también una oportunidad.

En Givore estamos abordando este reto con tecnología. Nuestra plataforma de reciclaje social conecta a quienes encuentran objetos útiles en la calle con quienes los necesitan. El proceso es simple: subes una foto, la ubicación se añade automáticamente, y en menos de 20 segundos el objeto está disponible para quien lo busque.

No es compraventa. Es economía circular en su forma más pura: dar y encontrar.

¿Qué papel creéis que puede jugar la tecnología en la transición hacia una economía más circular?

#EconomíaCircular #Sostenibilidad #Innovación #Valencia #Startups

═══════════════════════════════════════════════════════════
                       SUBTÍTULOS
═══════════════════════════════════════════════════════════

¿Sabéis qué?

Valencia está llena de tesoros...

y la mayoría de la gente pasa de largo.

Mira, todo esto me lo encontré en la calle.

Sillas, mesas...

hasta este mueble tan guapo.

El problema es que la gente

tira cosas perfectamente bien.

Por eso uso Givore.

Abro la app, subo las fotos...

y en menos de veinte segundos

cualquiera puede verlo.

Eso es reciclaje social.

Dar y encontrar.
```

---

## Quality Checklist

Before outputting, verify:
- [ ] All 5 platforms have unique titles matching their tone
- [ ] TikTok: Casual + emoji + 5 hashtags
- [ ] Instagram: Aesthetic + @givore.app + 7-10 hashtags
- [ ] YouTube: SEO title + #Shorts + 5-7 hashtags
- [ ] Facebook: Community tone + 5 hashtags
- [ ] LinkedIn: Professional/data + 5 hashtags
- [ ] Captions formatted correctly (no text changes)
- [ ] Spanish is informal except LinkedIn (which can be either)
- [ ] Each description mentions Givore naturally

---

## Language Note
All outputs in **Spanish (Spain)** - peninsular expressions, "vosotros" form, avoid Latin American variations.
