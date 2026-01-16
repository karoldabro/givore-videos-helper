# Givore Hook Library

Comprehensive hook system for viral TikTok scripts. Use this library to select and generate varied, non-repetitive hooks.

---

## Hook Selection Decision Tree

**STEP 1: Check video structure**
```
IF items appear in first 5 seconds → Go to PROOF-FIRST HOOKS
IF video starts with recap montage → Go to MYSTERY HOOKS
IF items revealed after 30 seconds → Go to MYSTERY HOOKS
IF single impressive item → Go to NUMERIC or PROOF-FIRST
IF multiple items found → Go to NUMERIC or JOURNEY HOOKS
IF asking for engagement → Go to QUESTION HOOKS
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
| Engagement/community | QUESTION, DIRECT ADDRESS |
| Long form (2+ min) | MYSTERY, JOURNEY |
| Short form (30s) | PROOF-FIRST, EMOTIONAL |

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
Hook style: mystery | proof-first | question | bold | numeric | journey | emotional
```

If not specified, AI will select based on video structure using the decision tree above.
