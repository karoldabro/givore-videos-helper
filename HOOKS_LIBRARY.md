# Givore Hook Library

Comprehensive hook system for viral TikTok scripts. Use this library to select and generate varied, non-repetitive hooks.

---

## Hook Selection Decision Tree

**STEP 1: Check video structure**
```
IF building a recurring series / episodic content → Go to DAY-X SERIALIZED HOOKS
IF items appear in first 5 seconds → Go to PROOF-FIRST HOOKS
IF video starts with recap montage → Go to MYSTERY HOOKS
IF items revealed after 30 seconds → Go to MYSTERY HOOKS
IF single impressive item → Go to NUMERIC or PROOF-FIRST
IF multiple items found → Go to NUMERIC or JOURNEY HOOKS
IF asking for engagement → Go to QUESTION HOOKS
IF community/connection focus + middle reveal → Go to THREE-PART RELEVANCE HOOKS
```

**STEP 2: Check recent hooks used**
```
IF last hook was MYSTERY → Use different category this time
IF same hook used in last 5 videos → MUST use different hook
```

**STEP 3: Match to content emotion**
```
Exciting find → DISCOVERY or NUMERIC hooks
Casual ride → JOURNEY, LOCATION, or POV hooks
Community focus → QUESTION, DIRECT ADDRESS, or DESTINY hooks
Sustainability message → TRANSFORMATION PROMISE or VALUE PROPOSITION hooks
High-value find → COMMAND, VALUE PROPOSITION, or FORBIDDEN KNOWLEDGE hooks
Trending format → POV or COMMAND hooks
```

---

## Hook Categories

### 1. MYSTERY HOOKS
**Use when:** Items appear LATE in video (after 30s), or you want maximum curiosity

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `[NÚMERO]. He encontrado [NÚMERO]... tiradas en la calle.` | Number of items | "Seis. He encontrado seis... tiradas en la calle." |
| `Lo que he encontrado hoy en [BARRIO]... no os lo vais a creer.` | Neighborhood name | "Lo que he encontrado hoy en Russafa... no os lo vais a creer." |
| `Quedaos hasta el final para ver lo que me he encontrado.` | None | Direct use |
| `Hoy he salido con la bici... y he vuelto con [NÚMERO] tesoros.` | Number | "Hoy he salido con la bici... y he vuelto con tres tesoros." |
| `Una hora en bici por [CIUDAD]... y lo que he encontrado es increíble.` | City | "Una hora en bici por Valencia... y lo que he encontrado es increíble." |
| `Os cuento lo que me pasó hoy en [BARRIO]...` | Neighborhood | "Os cuento lo que me pasó hoy en Benimaclet..." |
| `Esto empezó como un paseo normal...` | None | Direct use |

**Anti-patterns (NEVER do):**
- Don't reveal specific items in mystery hook
- Don't say "mesa", "silla", etc. - keep it vague
- Don't use "Nadie me va a creer" too often (overused)

---

### 2. PROOF-FIRST HOOKS
**Use when:** Video STARTS showing items immediately (0-5s)

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `[ITEM] perfectamente bien... tirado en [BARRIO].` | Item, Location | "Una cómoda de madera perfectamente bien... tirada en Torrefiel." |
| `Esto estaba en la calle hace diez minutos. Mirad.` | None | Direct use |
| `[ITEM] en la calle. ¡En la calle!` | Item | "Una secadora en la calle. ¡En la calle!" |
| `Mirad lo que me acabo de encontrar en [BARRIO].` | Location | "Mirad lo que me acabo de encontrar en el Cabanyal." |
| `Esto... estaba junto a la basura.` | None | Direct use (show item visually) |

**Anti-patterns:**
- Only use when video actually shows item in first 5 seconds
- Don't describe item in detail - let visual do the work

---

### 3. NUMERIC HOOKS
**Use when:** You found MULTIPLE items, or the quantity is impressive

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `[NÚMERO]. He encontrado [NÚMERO]... y mirad en qué estado.` | Number | "Seis. He encontrado seis... y mirad en qué estado." |
| `[NÚMERO] [ITEMS] en una mañana. Todo tirado.` | Number, Item type | "Tres muebles en una mañana. Todo tirado." |
| `[NÚMERO] barrios. Una bici. Y no os imagináis lo que he pillado.` | Number | "Seis barrios. Una bici. Y no os imagináis lo que he pillado." |
| `Una hora. [NÚMERO] hallazgos. Valencia.` | Number | "Una hora. Cuatro hallazgos. Valencia." |

**Best for:** Multiple item finds, neighborhood exploration videos

---

### 4. QUESTION HOOKS (Rhetorical)
**Use when:** You want to create shared indignation or curiosity

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `¿Por qué [SITUACIÓN]?` | Situation description | "¿Por qué tiramos cosas que funcionan perfectamente?" |
| `¿Sabéis qué he encontrado hoy en [BARRIO]?` | Location | "¿Sabéis qué he encontrado hoy en Patraix?" |
| `¿Quién tira [ITEM] así?` | Item | "¿Quién tira una trona de bebé así?" |
| `¿Cuántas veces habéis pasado de largo sin mirar?` | None | Direct use |
| `¿Qué haríais si encontrarais esto en la calle?` | None | Direct use |

**Important:** Question hooks work best when followed immediately by proof/visual

**Anti-patterns:**
- Avoid accusatory questions like "¿Por qué la gente...?" - too judgmental
- Frame questions as curiosity, not blame

---

### 5. BOLD STATEMENT HOOKS
**Use when:** Making a strong claim about Valencia/the area

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `[BARRIO/CIUDAD] está LLENA de tesoros.` | Location | "Valencia está LLENA de tesoros." |
| `Lo que para unos es basura, para otros es exactamente lo que necesitan.` | None | Direct use |
| `Esto no es basura... es un tesoro esperando a que lo encuentres.` | None | Direct use |
| `En [BARRIO] se tiran cosas increíbles cada día.` | Location | "En Russafa se tiran cosas increíbles cada día." |

**Best for:** Videos that showcase multiple finds or explore neighborhoods

---

### 6. DIRECT ADDRESS HOOKS
**Use when:** Targeting specific audience (Valencia residents, sustainability lovers)

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Si vivís en [CIUDAD], tenéis que ver esto.` | City | "Si vivís en Valencia, tenéis que ver esto." |
| `Esto es para todos los que odian el desperdicio.` | None | Direct use |
| `Si os gusta dar segunda vida a las cosas... quedaos.` | None | Direct use |
| `Vecinos de [BARRIO]... mirad lo que hay en vuestras calles.` | Neighborhood | "Vecinos de Benimaclet... mirad lo que hay en vuestras calles." |

---

### 7. JOURNEY/EXPLORATION HOOKS
**Use when:** Video is about the ride/exploration, not just the find

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Hoy me he recorrido [ZONA] en bici... y flipante lo que he encontrado.` | Area | "Hoy me he recorrido media Valencia en bici... y flipante lo que he encontrado." |
| `De [PUNTO A] a [PUNTO B]... buscando tesoros.` | Locations | "Del Turia a la playa... buscando tesoros." |
| `[NÚMERO] kilómetros en bici. ¿Habré encontrado algo?` | Number | "Diez kilómetros en bici. ¿Habré encontrado algo?" |
| `Otra vuelta por [BARRIO]... y otra vez he encontrado de todo.` | Neighborhood | "Otra vuelta por el Cabanyal... y otra vez he encontrado de todo." |

---

### 8. EMOTIONAL REACTION HOOKS
**Use when:** Your genuine reaction to the find is the hook

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `No me lo puedo creer. No me lo puedo creer.` | None | Direct use (show item) |
| `Esto es... esto es una pasada.` | None | Direct use |
| `¡Madre mía! ¿Esto estaba en la calle?` | None | Direct use |
| `Es que... mirad. Mirad esto.` | None | Direct use |

**Note:** These work best with genuine surprise in voice delivery

---

### 9. THREE-PART RELEVANCE HOOKS
**Use when:** You want to build a complete narrative arc in the hook itself: relevance → social proof → stakes

**Structure:** Three distinct parts that escalate commitment:
1. **Viewer-First Relevance** (~5s): Start with what matters to THEM - waste they've seen, disconnect they've felt
2. **Curiosity Gap / Social Proof** (~5-8s): Show that people are already solving this - growing community, real engagement
3. **Stakes / Solution Tease** (~3-5s): Promise a live demonstration or reveal

**Formulas:**

| Part | Template | Variables |
|------|----------|-----------|
| Part 1 (Relevance) | `Si alguna vez habéis visto [SITUACIÓN]... y os ha dado pena. Esto es para vosotros.` | Situation description |
| Part 1 (Relevance) | `Si [SITUACIÓN DEL VIEWER]... esto os va a interesar.` | Viewer's experience |
| Part 1 (Relevance) | `Todos hemos pasado por delante de [SITUACIÓN]... sin saber qué hacer.` | Common experience |
| Part 2 (Social Proof) | `Hay gente en Valencia que está cambiando eso. Compartiendo lo que sobra, rescatando lo que encuentran.` | Community action |
| Part 2 (Social Proof) | `Pues resulta que cada vez más gente está haciendo algo al respecto. Y funciona.` | Growth framing |
| Part 2 (Social Proof) | `En Valencia hay vecinos que ya han encontrado la manera. Y se suman más cada semana.` | Local community |
| Part 3 (Stakes) | `Hoy os voy a enseñar cómo funciona. En directo. Con lo que me acabo de encontrar.` | Live demo promise |
| Part 3 (Stakes) | `Y hoy os lo enseño con un ejemplo real. Mirad.` | Proof promise |
| Part 3 (Stakes) | `Os lo voy a demostrar ahora mismo.` | Direct stakes |

**Best for:** Videos where you want to establish emotional connection before showing content, middle-reveal timing, community-focused narratives

**Key principle:** Each part raises the viewer's commitment level:
- Part 1: "This is about ME" (stops scrolling)
- Part 2: "Others are doing it" (social validation)
- Part 3: "I'm about to see proof" (locks attention)

**Anti-patterns:**
- Don't mention specific quantities for community size (avoid "cientos", "miles" - keep it vague)
- Don't reveal items in any of the three parts
- Part 1 must be about the viewer's experience, not yours
- Don't make Part 2 sound like an ad - keep it organic

**Proof Tease:** SKIP when using this hook (the three parts already build enough anticipation)

**Duration:** ~15-20s total (longer than standard hooks - compensate by keeping PROBLEM section shorter)

---

### 10. DAY-X SERIALIZED HOOKS
**Use when:** Building a recurring series, episodic content, audience retention through repetition + variable reward

**Concept:** Serialized format ("Día X de...") creates a TV-show-like structure:
- **Repetitive format** = viewers know what to expect (familiar container)
- **Variable reward** = new content each episode (unknown discovery)
- This combination triggers dopamine through anticipation of novel content within a known framework

**Duration:** ~10-12 seconds maximum for the hook

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Día [X]... [ACTIVIDAD] por [ZONA]. A ver qué encontramos.` | Day number, Activity, Zone | "Día tres... buscando tesoros en bici por el centro. A ver qué encontramos." |
| `Día [X] de [MISIÓN]. Hoy me lanzo por [ZONA].` | Day number, Mission, Zone | "Día cinco de rescatar cosas de la basura. Hoy me lanzo por Ruzafa." |
| `Día [X]... [ACTIVIDAD]. Y lo que he encontrado hoy...` | Day number, Activity | "Día siete... recorriendo la ciudad en bici. Y lo que he encontrado hoy..." |
| `Día [X]. [ZONA]. Vamos a ver qué hay.` | Day number, Zone | "Día doce. Benimaclet. Vamos a ver qué hay." |

**Key principles:**
- Day number creates progress narrative (viewers want to follow the journey)
- Keep the activity description consistent across episodes (the "format")
- The discovery/content is the variable reward (what changes each episode)
- Can combine with curiosity build: "...y no os vais a creer lo que hay hoy"

**Anti-patterns:**
- Don't change the series description every episode (defeats the format purpose)
- Don't skip day numbers randomly (breaks the progression feeling)
- Don't reveal items in the hook (save for discovery section)
- Don't make the hook longer than 12 seconds (the format should be snappy)

**Proof Tease:** SKIP (the serialized format itself builds enough anticipation)

**Best for:** Regular content creators, building loyal audience, episodic series, exploration-style videos

---

### 11. DESTINY / FATE HOOKS
**Use when:** You want to create personal relevance and make the viewer feel this video was "meant for them"

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Si ves esto, es una señal de que tienes que hacer limpieza en casa.` | None | Direct use |
| `Si este video te ha llegado... algo tiene que cambiar.` | None | Direct use |
| `Si ves esto hoy, no es casualidad.` | None | Direct use |
| `El universo te está enviando este video por algo.` | None | Direct use |

**Best for:** Sustainability-minded audience, community-focused content, videos about decluttering or giving away items

**Key principles:**
- Leverages the "algorithm chose you" mentality common on TikTok/Reels
- Creates an emotional sense of personal relevance before showing any content
- Works particularly well with audience segments already interested in sustainability or minimalism

**Anti-patterns:**
- Don't overuse - this style loses power if repeated too often (max once every 10 videos)
- Don't combine with MYSTERY hooks - the destiny frame replaces curiosity with personal connection
- Avoid sounding too esoteric or spiritual - keep it grounded

---

### 12. COMMAND / DIRECT HOOKS
**Use when:** You want to interrupt scrolling with a direct, authoritative command

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Ya deja de guardar cosas que no usas.` | None | Direct use |
| `Para. Mira esto.` | None | Direct use |
| `Escúchame bien: esto te va a interesar.` | None | Direct use |
| `No pases de largo. Esto es importante.` | None | Direct use |
| `Deja lo que estés haciendo y mira.` | None | Direct use |

**Best for:** High-impact finds, videos with strong visual payoff, short-form content (under 30s)

**Key principles:**
- The command breaks the passive scroll pattern by addressing the viewer directly
- Must be followed immediately by something visually compelling - the command earns you 2 seconds of attention, no more
- Tone should be confident but friendly, not aggressive

**Anti-patterns:**
- Don't use if the payoff is weak - commands raise expectations
- Avoid combining multiple commands ("Para. Escucha. Mira.") - one is enough
- Don't sound angry or condescending - authoritative, not bossy

---

### 13. VALUE PROPOSITION HOOKS
**Use when:** Promising a specific, tangible benefit - especially "without cost"

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Cómo amueblar tu piso sin gastar un euro.` | None | Direct use |
| `El truco para renovar tu salón por cero euros.` | None | Direct use |
| `Cómo tener muebles de diseño sin pagar un céntimo.` | None | Direct use |
| `La forma más fácil de darle vida a tu casa.` | None | Direct use |

**Best for:** Videos showing high-value finds, furniture rescues, before/after transformations, app promotion content

**Key principles:**
- The "zero cost" angle is extremely powerful for younger demographics (students, first apartments)
- Frame it as a life hack or insider knowledge, not as scavenging
- Works best when the video actually delivers on the promise with impressive items

**Anti-patterns:**
- Don't promise what the video can't deliver - if you found a broken chair, don't promise "designer furniture"
- Avoid sounding like an ad or infomercial - keep it conversational
- Don't combine with MYSTERY hooks - value proposition hooks reveal the benefit upfront

---

### 14. FORBIDDEN KNOWLEDGE HOOKS
**Use when:** You want to create exclusivity and insider information framing

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Lo que nadie quiere que sepas sobre lo que tira tu vecino.` | None | Direct use |
| `Nadie te ha contado esto sobre la basura de tu barrio.` | None | Direct use |
| `Lo que los vecinos de [BARRIO] no quieren que veas.` | Neighborhood | "Lo que los vecinos de Ruzafa no quieren que veas." |
| `El secreto que nadie cuenta sobre las mudanzas.` | None | Direct use |

**Best for:** Videos revealing surprising finds, neighborhood exploration, content exposing waste culture

**Key principles:**
- Creates a "forbidden fruit" effect - people want to know what's being hidden
- The "nadie quiere que sepas" frame positions the creator as an insider sharing secrets
- Works well with shocking or surprising visual reveals

**Anti-patterns:**
- Don't be disrespectful toward specific neighbors or communities
- Avoid clickbait that doesn't deliver - the "secret" must be genuinely interesting
- Don't use accusatory language toward specific people or businesses
- Use sparingly - this hook style can feel manipulative if overused

---

### 15. POV HOOKS
**Use when:** Creating immersive first-person content, especially cycling POV footage

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `POV: vas en bici por Valencia y de repente ves esto.` | None | Direct use |
| `POV: tu vecino tira un mueble perfecto al contenedor.` | None | Direct use |
| `POV: descubres que tu basura es el tesoro de otro.` | None | Direct use |
| `POV: te mudas a Valencia y descubres lo que tira la gente.` | None | Direct use |
| `POV: cruzas el barrio del Carmen en bici un domingo por la mañana.` | None | Direct use |

**Best for:** Cycling POV footage, immersive street-level content, relatable everyday scenarios, trending format videos

**Key principles:**
- POV format is consistently trending on TikTok/Reels (2025-2026) and signals native platform content
- The "POV:" prefix is immediately recognizable and sets viewer expectations for immersive content
- Works perfectly with Givore's cycling POV footage - the format and content align naturally
- Can combine with any reveal type since the POV frame is about perspective, not content structure

**Anti-patterns:**
- Don't use "POV:" if the video isn't actually shot from first person perspective
- Avoid overly long POV descriptions - keep the scenario to one short sentence
- Don't mix POV with other hook styles in the same hook (e.g., "POV: ¿sabéis qué...?" - pick one)

---

### 16. TRANSFORMATION PROMISE HOOKS
**Use when:** You want to promise the viewer their perspective or understanding will change

**Formulas:**
| Template | Variables | Example |
|----------|-----------|---------|
| `Después de este vídeo, nunca volverás a mirar un contenedor igual.` | None | Direct use |
| `Esto cambiará tu forma de ver la basura.` | None | Direct use |
| `En 30 segundos vais a entender por qué hago esto.` | None | Direct use |
| `Un vídeo. Eso es lo que te falta para cambiar de opinión.` | None | Direct use |

**Best for:** Mission-driven content, sustainability messaging, videos with strong emotional payoff, community-building content

**Key principles:**
- Promises internal change rather than external benefit - appeals to curiosity about self
- Creates a before/after frame for the viewer's own mindset, not just the items
- Works best when the video genuinely delivers an "aha moment" or emotional shift
- Strong for building channel identity and long-term audience loyalty

**Anti-patterns:**
- Don't use for mundane finds - the promise of transformation requires a genuinely impactful video
- Avoid sounding preachy or self-righteous - the tone should be inviting, not lecturing
- Don't combine with NUMERIC hooks - transformation is qualitative, not quantitative

---

## Freshness Score

Before selecting a hook, calculate its freshness score. **Minimum score of 5 required to use a hook.** If nothing scores 5+, CREATE a new hook formula.

| Criterion | Points |
|-----------|--------|
| Hook TYPE not used in last 5 scripts | +3 |
| Hook TYPE not used in last 10 scripts | +5 |
| Specific TEMPLATE never used before | +5 |
| Different CATEGORY from last 2 scripts | +2 |
| Trend-inspired (from STEP 0.3 research) | +3 |

**How to apply:**
1. Check rotation history for the candidate hook type
2. Sum all applicable points
3. If score < 5, try a different hook or create a new formula
4. Log the selected hook's freshness score in metadata

---

## Hook Rotation Rules

### MANDATORY ROTATION
1. **Never use the same hook template in consecutive videos**
2. **Track last 5 hooks used** - avoid all of them
3. **Rotate between categories** - don't use the same category 3 times in a row

### Suggested Rotation Pattern
```
Video 1: MYSTERY hook
Video 2: PROOF-FIRST hook
Video 3: QUESTION hook
Video 4: NUMERIC hook
Video 5: BOLD STATEMENT hook
Video 6: JOURNEY hook
(Repeat with variations)
```

---

## Quick Reference by Video Type

| Video Type | Best Hook Categories |
|------------|---------------------|
| Single item find | PROOF-FIRST, EMOTIONAL, COMMAND |
| Multiple items | NUMERIC, MYSTERY |
| Neighborhood exploration | JOURNEY, BOLD STATEMENT, POV |
| App tutorial | PROOF-FIRST, DIRECT ADDRESS, VALUE PROPOSITION |
| Engagement/community | QUESTION, DIRECT ADDRESS, THREE-PART RELEVANCE, DESTINY |
| Long form (2+ min) | MYSTERY, JOURNEY, THREE-PART RELEVANCE, TRANSFORMATION PROMISE |
| Short form (30s) | PROOF-FIRST, EMOTIONAL, COMMAND, POV |
| Community + middle reveal | THREE-PART RELEVANCE |
| Serialized/episodic | DAY-X |
| Sustainability/mission | TRANSFORMATION PROMISE, DESTINY |
| High-value furniture find | VALUE PROPOSITION, FORBIDDEN KNOWLEDGE, COMMAND |
| Cycling POV footage | POV, JOURNEY |
| Trending format | POV, COMMAND, DESTINY |

---

## Overused Hooks to AVOID

These hooks have been used too frequently. Avoid or use sparingly:

| Overused Hook | Use Instead |
|---------------|-------------|
| "Nadie me va a creer lo que acabo de encontrar..." | "Lo que he encontrado hoy en [BARRIO]... increíble." |
| "Valencia está LLENA de tesoros" | "[BARRIO específico] está lleno de sorpresas" |
| "Todo esto me lo encontré en la calle. ¡En la calle!" | "Esto estaba en la calle hace diez minutos. Mirad." |
| "¿Por qué la gente tira cosas así de buenas?" | "¿Quién tira [item específico] así?" |

---

## Input Field for Script Generation

When requesting a script, specify:
```
Hook style: mystery | proof-first | question | bold | numeric | journey | emotional | relevance-3part | day-x | destiny | command | value-prop | forbidden | pov | transformation
```

If not specified, AI will select based on video structure using the decision tree above.

---

## Keyword-Optimized Hook Templates

Hooks built around high-volume Spanish search keywords. Use these to naturally incorporate terms people actually search for, boosting discoverability without sacrificing authenticity.

### Furniture / Cost Hooks
**Target keywords**: muebles baratos (230K), muebles vintage (150K), muebles reciclados (86K)

| Hook | Target Keyword |
|------|---------------|
| "Muebles vintage en la calle. Así. Gratis. Tirados." | muebles vintage (150K) |
| "¿Muebles baratos? No. Muebles que alguien dejó en perfecto estado." | muebles baratos (230K) |
| "Esto en una tienda vintage vale 200 euros. En la calle de mi barrio: cero." | muebles vintage (150K) |
| "Muebles reciclados que encuentro pedaleando por mi barrio." | muebles reciclados (86K) |
| "La gente tira muebles vintage como si nada. Mirad esto." | muebles vintage (150K) |

**Note**: "gratis" is OK in spoken audio hooks. BANNED from written descriptions/captions (algorithm penalty).

### Restoration / DIY Hooks
**Target keywords**: restaurar muebles (28K), muebles con palets (95K), pintar muebles (19K), muebles restaurados (13K), restaurar muebles antiguos (7.1K)

| Hook | Target Keyword |
|------|---------------|
| "Muebles con palets: lo que la gente tira en la calle." | muebles con palets (95K) |
| "Una mesa reciclada que encontré junto a la basura." | mesa reciclada (7.4K) |
| "Cómo pintar muebles de madera que encuentras en la calle." | como pintar muebles de madera (2.5K) |
| "Restaurar muebles antiguos: segunda vida desde la acera." | restaurar muebles antiguos (7.1K) |

| Hook | Target Keyword |
|------|---------------|
| "Antes de tirarlo... ¿y si lo pintas?" | pintar muebles (19K) |
| "Restaurar muebles de la calle: mi nueva obsesión." | restaurar muebles (28K) |
| "Ideas para restaurar muebles viejos que encuentro en bici." | restaurar muebles (28K) |
| "Muebles restaurados: de la basura a tu salón." | muebles restaurados (13K) |
| "Pintar muebles que encuentras en la calle. Así de fácil." | pintar muebles (19K) |

### City / Cycling Hooks
**Target keywords**: carril bici [CIUDAD] (Madrid 15K, Barcelona 12K, Valencia 10K, Sevilla 5.5K), rutas bici [CIUDAD] (Madrid 4.5K, Barcelona/Valencia 1.6K, Sevilla 1.1K)

Use `[CIUDAD]` placeholder — substitute the city matching the video content. Works for any Spanish city.

| Hook | Target Keyword |
|------|---------------|
| "Recorriendo el carril bici de [CIUDAD] y lo que me encuentro." | carril bici [CIUDAD] (10-15K) |
| "[CIUDAD] en bici: lo que los turistas nunca ven." | [CIUDAD] en bici |
| "Barrios de [CIUDAD] desde la bici — hoy: [BARRIO]." | barrios [CIUDAD] (Madrid 10K, Barcelona 7.7K, Valencia 3.7K) |
| "Rutas en bici por [CIUDAD] que no salen en las guías." | rutas bici [CIUDAD] (1.1-4.5K) |
| "Lo que descubres pedaleando por [BARRIO]." | [BARRIO] [CIUDAD] |

### Budget Living Hooks
**Target keywords**: amueblar piso barato (3K), decoracion low cost (4.5K), decoracion reciclada (6.7K)

| Hook | Target Keyword |
|------|---------------|
| "Amueblar tu piso sin gastar: lo que encuentras en la calle." | amueblar piso barato (3K) |
| "Decoración low cost nivel: pasear por tu barrio." | decoracion low cost (4.5K) |
| "Decoración reciclada con lo que la gente tira cada día." | decoracion reciclada (6.7K) |
| "Amueblar piso barato: la calle es tu tienda." | amueblar piso barato (3K) |

### Secondhand / Sharing Economy Hooks
**Target keywords**: segunda mano [CIUDAD] (Madrid 250K, Barcelona 170K, Valencia 140K, Sevilla 110K), consumo responsable (57K), economia colaborativa (16K), app segunda mano (3K)

| Hook | Target Keyword |
|------|---------------|
| "Segunda mano en [CIUDAD]: lo que la gente deja en la calle." | segunda mano [CIUDAD] (110-250K) |
| "Consumo responsable empieza aquí: en la acera de tu barrio." | consumo responsable (57K) |
| "Economía colaborativa nivel calle: yo encuentro, tú recoges." | economia colaborativa (16K) |
| "La mejor app de segunda mano es... tu barrio." | app segunda mano (3K) |
| "Segunda mano en perfecto estado. Tirado. En [BARRIO]." | segunda mano [CIUDAD] |

### Mudanzas / Punto Limpio Hooks
**Target keywords**: mudanzas [CIUDAD] (Madrid 41K, Barcelona 34K, Valencia 18K), punto limpio [CIUDAD] (Madrid 18K, Sevilla 5.5K)

| Hook | Target Keyword |
|------|---------------|
| "Después de cada mudanza en [CIUDAD]... esto aparece en la calle." | mudanzas [CIUDAD] (18-41K) |
| "Lo que la gente tira cuando se muda. En perfecto estado." | mudanzas [CIUDAD] |
| "Antes de llevarlo al punto limpio... ¿y si alguien lo quiere?" | punto limpio [CIUDAD] (5.5-18K) |
| "El punto limpio de mi barrio: la acera." | punto limpio [CIUDAD] |

### Niche / Lifestyle Hooks
**Target keywords**: reciclaje creativo (14K), reciclar muebles (15K), movilidad sostenible (9.2K), ordenar casa (840), gatos callejeros (3K)

| Hook | Target Keyword |
|------|---------------|
| "Reciclar muebles es más fácil de lo que piensas." | reciclar muebles (15K) |
| "Reciclaje creativo: lo que otros tiran, yo lo transformo." | reciclaje creativo (14K) |
| "Movilidad sostenible + reciclaje: mi combo diario en bici." | movilidad sostenible (9.2K) |
| "Ordenar casa y dar segunda vida a lo que sobra." | ordenar casa (840) |
| "Los gatos callejeros de mi ruta en bici por [CIUDAD]." | gatos callejeros (3K) |
| "Los perros que me encuentro cada día pedaleando." | perros [CIUDAD] (2.5K) |

### Keyword Hook Selection Rules

1. **Mix keyword hooks with non-keyword hooks** — max 50% keyword-optimized hooks per week
2. **Don't force keywords** — if a keyword hook doesn't fit the video content, skip it
3. **Rotate keyword targets** — don't hit the same keyword 2 videos in a row
4. **Spoken vs written**: "gratis" is fine in spoken hooks, NEVER in written descriptions
