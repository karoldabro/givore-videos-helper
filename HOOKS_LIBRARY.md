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
IF same hook used in last 3 videos → MUST use different hook
```

**STEP 3: Match to content emotion**
```
Exciting find → DISCOVERY or NUMERIC hooks
Casual ride → JOURNEY or LOCATION hooks
Community focus → QUESTION or DIRECT ADDRESS hooks
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

## Hook Rotation Rules

### MANDATORY ROTATION
1. **Never use the same hook template in consecutive videos**
2. **Track last 3 hooks used** - avoid all of them
3. **Rotate between categories** - don't use MYSTERY 3 times in a row

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
| Single item find | PROOF-FIRST, EMOTIONAL |
| Multiple items | NUMERIC, MYSTERY |
| Neighborhood exploration | JOURNEY, BOLD STATEMENT |
| App tutorial | PROOF-FIRST, DIRECT ADDRESS |
| Engagement/community | QUESTION, DIRECT ADDRESS, THREE-PART RELEVANCE |
| Long form (2+ min) | MYSTERY, JOURNEY, THREE-PART RELEVANCE |
| Short form (30s) | PROOF-FIRST, EMOTIONAL |
| Community + middle reveal | THREE-PART RELEVANCE |
| Serialized/episodic | DAY-X |

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
Hook style: mystery | proof-first | question | bold | numeric | journey | emotional | relevance-3part | day-x
```

If not specified, AI will select based on video structure using the decision tree above.
