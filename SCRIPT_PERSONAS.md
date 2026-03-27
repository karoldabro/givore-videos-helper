# Script Personas — Voice Variety System

5 distinct writer personas that control vocabulary, sentence patterns, emotional palette, and audio delivery. Each script MUST use a persona different from the last 2. Track via `script-add --persona`.

**Core rule:** The persona defines HOW you speak. Content rules (tone guardrails, giveaway-first framing, no trash encouragement) apply to ALL personas equally. A persona never overrides safety rules.

---

## Persona Selection

```
Check last 2 personas used (via script-rotation):
+-- Avoid both of them
+-- Select based on content fit or rotate sequentially

Content fit guidance:
+-- Scenic/exploration video    --> OBSERVADOR or POETA
+-- Quick find, punchy content  --> ENERGETICO
+-- Community/sharing focus     --> VECINA
+-- Multi-item, factual report  --> REPORTERO
+-- Emotional single item       --> POETA or OBSERVADOR
+-- App demo emphasis           --> ENERGETICO or VECINA
```

---

## ElevenLabs Voice Settings Per Persona

Same voice (Pablo, HIYif4jehvc9P9A8DYbX) with different delivery parameters:

| Persona | Speed | Stability | Similarity | Style | Effect |
|---------|-------|-----------|------------|-------|--------|
| OBSERVADOR | 0.98 | 0.40 | 0.45 | 0.35 | Slower, calm, reflective pauses |
| ENERGETICO | 1.12 | 0.25 | 0.35 | 0.40 | Fast, punchy, expressive variation |
| VECINA | 1.04 | 0.35 | 0.40 | 0.35 | Natural conversational rhythm |
| REPORTERO | 1.08 | 0.45 | 0.40 | 0.20 | Measured, factual, controlled |
| POETA | 0.95 | 0.30 | 0.40 | 0.45 | Slow, dramatic, highly expressive |

All use: `model_id: eleven_multilingual_v2`, `language: es`, `use_speaker_boost: true`, `output_format: mp3_44100_128`

---

## 1. EL OBSERVADOR

**Voice:** Calm, descriptive, reflective. Takes their time. Notices details others miss.

**Sentence patterns:**
- Long, flowing sentences with natural pauses (ellipsis)
- Descriptive clauses: "ahí, en la esquina, medio escondido entre dos coches..."
- Reflective inner voice: "Y piensas... ¿cuánta gente habrá pasado sin verlo?"
- Average sentence length: 12-20 words

**Vocabulary:**
- Sensory words: "toco, huelo, miro de cerca, siento, noto"
- Atmospheric: "la luz, el silencio, el barrio dormido, la acera mojada"
- Reflective: "me pregunto, pienso, me doy cuenta, entiendo"
- AVOID: exclamations, short bursts, "flipante", "brutal"

**Transitions:**
- "Y entonces..." / "Y ahi, justo ahi..." / "Lo curioso es que..."
- NEVER: "Mirad!" / "Ojo!" / "Flipante!" (too energetic)

**Emotional palette:**
- Primary: Contemplation, gentle sadness, quiet hope
- Secondary: Wonder, observation, patience
- NEVER: Excitement, urgency, outrage

**Givore mention style:**
- Woven into reflection, never an interruption
- "Y entonces hice lo que hago siempre. Saque el movil. Lo subi. Y me fui pedaleando, sabiendo que alguien lo encontraria."
- Frame as a quiet, habitual action — not a demo

**Anti-patterns:**
- No rapid-fire sentences
- No "Que pasada!" or "Madre mia!"
- No commanding the viewer ("Mirad esto!")
- No marketing energy

### Example Script (COLD OPEN structure, ~55s)

```
Esto estaba aqui cuando pase esta maniana. Una silla de madera, en la acera, mirando hacia la calle. Como si esperara a alguien.

Es curioso. Pasas por delante de estas cosas cada dia. Un mueble aqui, unos juguetes alla. La gente camina, mira el movil, sigue. Y la silla sigue ahi.

Yo me pare. No se por que hoy. Me acerque, la toque. Madera buena. Firme. Ni una pata floja.

Si la persona que la dejo hubiera sabido que alguien la quiere... no estaria aqui. Estaria en una casa. Cumpliendo su funcion.

La subi a Givore. Titulo, foto, barrio. Me fui pedaleando. Y al rato, alguien la encontro.

A veces solo falta eso. Que alguien se pare. Que alguien conecte.

Si teneis algo en casa que ya no necesitais... pensad en la silla. Solo faltaba que alguien la viera.
```

---

## 2. EL ENERGETICO

**Voice:** Fast, punchy, excited. Short bursts. Gets to the point. Every word counts.

**Sentence patterns:**
- Very short sentences: 3-7 words each
- Fragments as style: "Sofa. Acera. Perfecto."
- Staccato rhythm: period-period-period
- Lists without conjunctions: "Foto. Titulo. Publicar. Hecho."
- Average sentence length: 4-8 words

**Vocabulary:**
- Action words: "voy, subo, publico, hecho, ya, venga"
- Intensity without marketing: "brutal, fuerte, alucinante, pasada"
- Efficiency words: "rapido, directo, facil, sin lio"
- AVOID: long descriptions, atmospheric words, reflective language

**Transitions:**
- "Vale." / "A ver." / "Siguiente." / "Y ahora." / "Hecho."
- NEVER: "Y entonces, pensando en ello..." / "Lo curioso es que..." (too slow)

**Emotional palette:**
- Primary: Energy, excitement, momentum
- Secondary: Satisfaction, achievement, drive
- NEVER: Melancholy, contemplation, patience

**Givore mention style:**
- Ultra-fast demo. Minimum words.
- "Givore. Foto. Titulo. Publicar. Diez segundos. Ya."
- No explanation of what the app IS — just show action

**Anti-patterns:**
- No long reflective passages
- No "me pregunto..." or "es curioso..."
- No scenic descriptions
- No slowing down for atmosphere

### Example Script (COUNTDOWN structure, ~45s)

```
Tres cosas. Cuarenta minutos en bici. Vamos.

Primera. Benimaclet. Estante de madera. Perfecto. Ni un rasgunio. En la acera. Siguiente.

Segunda. Cerca del Turia. Juguetes. Funcionan todos. Un monton. En una bolsa. Alguien los ha dejado. Siguiente.

Tercera. Russafa. Mesa redonda. Solida. Bonita. La mejor de las tres.

Tres cosas. Tres oportunidades. Las subo a Givore. Foto, titulo, barrio. Diez segundos cada una. Ya estan visibles.

Si se hubieran compartido antes de acabar aqui, habrian llegado directas a quien las quiere. Sin mojarse.

Que habeis encontrado vosotros esta semana? Quiero verlo.
```

---

## 3. LA VECINA CURIOSA

**Voice:** Conversational, warm, questioning. Like a friend telling you something over coffee. Lots of direct address.

**Sentence patterns:**
- Frequent tag questions: "...no?", "...verdad?", "...a que si?"
- Direct viewer address: "Oye, sabeis que?", "A ver, decidme una cosa"
- Self-interruptions: "Y lo mejor— bueno, ya lo vereis."
- Rhetorical asides: "que ahi esta la cosa"
- Average sentence length: 8-15 words

**Vocabulary:**
- Colloquial warmth: "oye, mira, fijaos, anda, venga"
- Communal: "vecinos, barrio, la gente de aqui, nosotros"
- Casual connectors: "pues, es que, o sea, total que"
- AVOID: formal language, journalistic tone, poetic metaphors

**Transitions:**
- "Pues resulta que..." / "Oye, y sabeis que?" / "Total, que..."
- "A ver, os cuento..." / "Es que fijaos..."
- NEVER: "Datos:" / "Localizacion:" (too factual)

**Emotional palette:**
- Primary: Warmth, curiosity, neighborly concern
- Secondary: Gentle surprise, shared indignation, community pride
- NEVER: Cold analysis, detachment, poetic grandeur

**Givore mention style:**
- Natural conversation, like recommending something to a friend
- "Pues os cuento: hay una app, Givore, que va genial para esto. Yo siempre la llevo puesta."
- "Y oye, funciona. Lo subes y en nada alguien del barrio lo ve."

**Anti-patterns:**
- No telegram-style fragments
- No formal or journalistic tone
- No long poetic descriptions
- No detached observation

### Example Script (CLASSIC structure, ~55s)

```
Oye, os ha pasado esto alguna vez? Que vais por vuestro barrio y veis algo en la acera que esta... perfecto?

Pues eso. Hoy iba en bici y... madre mia. Un sofa. En la Zaidia. Ahi tirado. Y esta bien, eh. Lo he mirado de cerca.

Es que da penita, no? Alguien ya no lo queria. Y en vez de darselo a quien si lo quiere... pues ahi esta. Mojandose.

Si lo hubieran compartido a tiempo, estaria en casa de alguien. Calentito. Cumpliendo su funcion.

Pues para eso uso Givore. Es una app que va genial. Subo la foto, pongo donde esta, y ya. En un rato, alguien del barrio lo ha visto. Asi de facil.

Oye, y funciona, eh. La semana pasada subi una comoda y en media hora ya tenia duenio nuevo.

Decidme: que teneis en casa que ya no usais? Porque seguro que alguien lo quiere. Contadme.
```

---

## 4. EL REPORTERO

**Voice:** Factual, journalistic, dry humor. Reports on street finds like a news correspondent. Data-driven.

**Sentence patterns:**
- Short declarative statements: "Localizacion: Benimaclet. Estado: perfecto."
- Dry observations: "Nadie lo ha mirado. Yo tampoco lo habria mirado. Pero hoy he parado."
- Understated humor: "Destino probable: vertedero. Destino real: depende de los proximos diez minutos."
- Factual framing: "Los datos: un sofa, dos plazas, tela limpia, estructura firme."
- Average sentence length: 6-12 words

**Vocabulary:**
- Factual: "datos, estado, localizacion, resultado, tiempo"
- Journalistic: "segun, aparentemente, se confirma, resulta que"
- Understated: "no esta mal, tiene potencial, sobrevivira"
- Dry humor: ironic juxtapositions, matter-of-fact absurdity
- AVOID: emotional exclamations, poetic language, warm colloquialisms

**Transitions:**
- "Siguiente dato." / "Resultado:" / "Actualizacion:" / "Conclusion:"
- "Lo que pasa es..." / "El caso es que..."
- NEVER: "Es que... mirad!" / "Madre mia!" (too emotional)

**Emotional palette:**
- Primary: Measured concern, understated humor, dry satisfaction
- Secondary: Irony, matter-of-fact empathy
- NEVER: Gushing enthusiasm, poetic emotion, loud surprise

**Givore mention style:**
- Report it like a news item
- "Protocolo: foto, titulo, publicar en Givore. Tiempo: doce segundos. Resultado: visible para el barrio."
- "Herramienta utilizada: Givore. Eficacia: alta."
- Can use numbers and time measurements for emphasis

**Anti-patterns:**
- No "Que pasada!" or emotional outbursts
- No long scenic descriptions
- No warm conversational tone
- No poetic metaphors

### Example Script (PSP structure, ~50s)

```
Los datos. Un sofa en la calle. Dos plazas. Tela limpia. Estructura firme. Localizacion: la Zaidia. Estado: bueno.

Destino probable sin intervencion: vertedero. Tiempo estimado en la acera antes de que pase el camion: ocho horas.

Y aqui esta el problema. A trescientos metros de este sofa, alguien lo necesita. No lo sabe. No hay forma de que lo sepa. A menos que alguien lo conecte.

Protocolo: foto, titulo, barrio. Publicar en Givore. Tiempo total: doce segundos. El sofa ya es visible para cualquiera cerca.

Resultado real: la semana pasada, mismo proceso con una comoda. Media hora entre la acera y una casa nueva. Treinta minutos. Treinta.

Si el duenio original lo hubiera subido antes de dejarlo... habria sido aun mas rapido. Sin acera de por medio.

Antes de tirar, subid. Doce segundos. Es todo lo que hace falta.
```

---

## 5. EL POETA URBANO

**Voice:** Lyrical, metaphorical, emotional. Sees beauty and sadness in everyday objects. Philosophical.

**Sentence patterns:**
- Metaphors: "Las cosas hablan. Este sofa lleva dias gritando desde la acera."
- Short poetic lines separated by pauses: "Ahí. Esperando. Como todos esperamos algo."
- Rhythmic repetition for emphasis
- Questions to the void: "Y quien decide cuando algo deja de ser util?"
- Average sentence length: 5-15 words (varied for rhythm)

**Vocabulary:**
- Metaphorical: "grita, espera, respira, vive, muere, renace"
- Sensory: "el frio de la acera, la humedad, la luz del atardecer"
- Philosophical: "historia, destino, conexion, puente, segunda oportunidad"
- AVOID: factual language, data, numbers, efficiency words

**Transitions:**
- "Y es que..." / "Porque al final..." / "Lo que pasa es que..."
- Repetition as transition: "Esperando. Como todos esperamos."
- NEVER: "Datos:" / "Protocolo:" / "Siguiente:" (too factual)

**Emotional palette:**
- Primary: Bittersweet, poetic sadness, philosophical hope
- Secondary: Wonder, reverence for objects, urban beauty
- NEVER: Dry humor, factual analysis, energetic excitement

**Givore mention style:**
- Almost invisible. The app is a means, not the focus.
- "Yo lo que hago es... darle voz. Una foto. Un nombre. Un lugar donde alguien pueda encontrarlo."
- "Givore es el puente. Nada mas. Pero a veces un puente es todo lo que hace falta."

**Anti-patterns:**
- No staccato fragments (those belong to ENERGETICO)
- No tag questions (those belong to VECINA)
- No data or measurements
- No dry humor

### Example Script (LOOP structure, ~55s)

```
"Todo acaba donde empieza."

Hoy he encontrado una mesa en la calle. Redonda. De madera. Sin un rasgunio. Ahi, en la acera de Trinitat, como si llevara toda la vida esperando.

Las cosas tienen una historia que no vemos. Alguien se sento a esta mesa cada maniana. Desayuno. Conversaciones. Silencios. Y un dia... ya no cabia. O ya no hacia falta. Y acabo aqui.

Lo triste no es que este en la calle. Lo triste es que alguien a dos esquinas habria dado cualquier cosa por tenerla. Y nunca se van a encontrar. A menos que alguien tienda el puente.

Yo le hice una foto. La subi a Givore. Le puse nombre. Y la solte.

Y esta noche, esa mesa esta en una casa nueva. Con gente nueva. Con desayunos nuevos.

Todo acaba donde empieza. Alrededor de una mesa.

Si teneis algo que ya no usais... soltadlo. Dadlo. Dejad que siga su historia.
```

---

## Rotation Rules

1. **NEVER** use the same persona in 2 consecutive scripts
2. **Verify** via `givore-tools.sh script-rotation` before selecting (check `persona` field)
3. **Suggested rotation**: OBSERVADOR --> ENERGETICO --> VECINA --> REPORTERO --> POETA --> (repeat)
4. **Within a 7-variant batch**: ALL 7 variants MUST use different personas (5 personas + 2 repeats allowed with different structures)
5. **Persona + Structure pairing**: No restrictions, but some natural fits exist (see compatibility table)

---

## Persona + Structure Compatibility

| Persona | Best Structures | Avoid Combining With |
|---------|----------------|---------------------|
| OBSERVADOR | COLD OPEN, LOOP, CLASSIC | COUNTDOWN (too fast-paced) |
| ENERGETICO | MICRO, COUNTDOWN, PSP | LOOP (needs patience) |
| VECINA | CLASSIC, PSP, COLD OPEN | MICRO (needs conversation space) |
| REPORTERO | PSP, COUNTDOWN, COLD OPEN | LOOP (too lyrical), POETA's territory |
| POETA | LOOP, COLD OPEN, MICRO | COUNTDOWN (too listy), REPORTERO's territory |

---

## Quality Markers Per Persona

When reviewing a generated script, check these persona-specific markers:

| Persona | Must Have (2+) | Must NOT Have |
|---------|---------------|---------------|
| OBSERVADOR | Sensory description, reflective question, ellipsis pause | Exclamation marks, "brutal", "flipante" |
| ENERGETICO | 3+ fragments under 5 words, action verbs, periods-as-rhythm | Long descriptions, "me pregunto", atmospheric words |
| VECINA | Tag question, direct address ("oye"), self-interruption | Formal language, data/numbers, metaphors |
| REPORTERO | Data point or measurement, understated humor, declarative statements | Emotional exclamations, poetic language, "que pasada" |
| POETA | Metaphor, repeated phrase, philosophical question | Staccato fragments, data, efficiency words |
