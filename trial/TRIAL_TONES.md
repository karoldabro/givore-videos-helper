# Trial Tone Definitions

6 tones for trial content with guardrails, Spanish humor notes, example phrases, and ElevenLabs voice adjustments.

---

## Core Rule: Tone Serves Recognition

Every tone -- whether humoristic, dramatic, or sarcastic -- must make the viewer feel **recognized**, not attacked. The humor, drama, or provocation is about the **situation**, never about the person.

---

## 1. HUMORISTIC (Humorístico)

**Voice:** A funny friend making observations about everyday life. Recognition humor, slight exaggeration, self-aware.

**Spanish humor notes:**
- Works through recognition ("eso me pasa a mí")
- Slight exaggeration of real situations (not absurdist fantasy)
- "Cuñado" energy -- the friend who states the obvious in a funny way
- Self-deprecation works ("Yo también tengo un trastero que parece un almacén")
- Comparisons to relatable things ("Más trastos que un Ikea")

**Guardrails:**
- Humor at the SITUATION, never at the person
- Never mock the viewer directly
- Self-deprecation is acceptable and encouraged
- Absurd comparisons should be grounded in truth
- The laugh should come from recognition, not ridicule

**Compatible formats:** Question Barrage, Problem Escalation, Humor Skit

**Example phrases:**
- "Tu trastero tiene más capas que una lasaña... y ninguna huele bien."
- "Esa bici estática que usas de perchero. No te juzgo. Yo tengo una igual."
- "Llevas tres mudanzas arrastrando una caja que nunca has abierto. ¿Qué hay dentro? Ni tú lo sabes."
- "Tu garaje tiene más cosas que el Carrefour pero nada está a la venta."
- "Tienes un cajón de cables que parece una obra de arte contemporáneo."

**Red flags (avoid):**
- Humor that requires intelligence-shaming
- Slapstick or cringe humor
- Jokes that only work written (needs to land spoken)
- Cultural references too narrow for broad audience

**ElevenLabs settings:**
```yaml
speed: 1.10        # Faster for comedic timing
stability: 0.30    # More expressive, playful variation
style: 0.35        # Subtle emotional range
```

---

## 2. EMPATHETIC (Empático)

**Voice:** An understanding friend who has been there. Warm, validating, no judgment. "We've all been there" energy.

**Spanish expression notes:**
- "Es normal" is the core phrase
- "Todos hemos pasado por ahí" -- inclusive, not condescending
- Soft transitions: "Y bueno...", "A ver...", "La verdad es que..."
- Focus on emotional relief, not obligation
- Warm pacing, not rushed

**Guardrails:**
- Validate the viewer's situation BEFORE suggesting any change
- Never preach or lecture
- The emotional relief of sharing is the reward (not sustainability)
- Acknowledge that keeping things is human nature
- Make sharing feel like self-care, not obligation

**Compatible formats:** Scenario Story, Direct Address

**Example phrases:**
- "Es normal. Todos tenemos cosas que guardamos 'por si acaso'. Pero ocupan espacio. Y también espacio mental."
- "No pasa nada. Es humano querer conservar las cosas. Pero a veces, soltar es lo mejor que puedes hacer."
- "Sé que da pereza. Que parece mucho trabajo. Pero y si te digo que es más fácil de lo que piensas?"
- "Ese mueble... te costó. Lo elegiste con ilusión. Normal que cueste desprenderse."
- "Oye, no eres el único. Todos tenemos ese rincón de la casa que preferimos no mirar."

**Red flags (avoid):**
- Condescension disguised as empathy
- "Deberías..." or any prescriptive language
- Pity tone (poor you) -- empathy is peer-to-peer
- Sustainability guilt

**ElevenLabs settings:**
```yaml
speed: 1.02        # Slightly slower, warmer pace
stability: 0.40    # Steadier, more consistent
style: 0.35        # Warm but not overly emotional
```

---

## 3. PROVOCATIVE (Provocador)

**Voice:** "Hot take" energy. Challenging assumptions playfully. "Unpopular opinion" style. Confident but not aggressive.

**Spanish expression notes:**
- "Opinión impopular:" as a hook format
- "A ver, os voy a decir una cosa..." -- direct but not hostile
- Bold statements that make you stop scrolling
- Conversational debate energy, not argument energy
- Works with "¿sabéis qué?" as a setup

**Guardrails:**
- Challenge a BELIEF, not a person
- Stay playful, never angry or aggressive
- The provocation should make them think, not feel attacked
- Back up the bold claim with a relatable truth
- Should feel like a friend giving you a reality check, not a lecture

**Compatible formats:** Direct Address, Question Barrage

**Example phrases:**
- "Opinión impopular: si algo lleva más de un año sin moverse del trastero, ya no es tuyo. Es del trastero."
- "A ver, os voy a decir una cosa. Guardar cosas 'por si acaso' es guardar miedo."
- "Sabéis qué pasa? Que tenéis más cosas de las que necesitáis. Y lo sabéis."
- "El trastero no es un plan de pensiones. Lo que hay ahí dentro no va a subir de valor."
- "Provocación del día: tu casa tiene más cosas que espacio. Y eso no es un problema de metros."

**Red flags (avoid):**
- Personal attacks or shaming
- Aggressive or hostile tone
- Elitism or class-related provocations
- Anything that could be read as mean-spirited

**ElevenLabs settings:**
```yaml
speed: 1.08        # Punchy delivery
stability: 0.30    # Confident variation
style: 0.40        # More assertive emotional range
```

---

## 4. DRAMATIC (Dramático)

**Voice:** Telenovela energy. Over-the-top storytelling about mundane household situations. The drama is in the DELIVERY, not reality.

**Spanish expression notes:**
- Dramatic pauses (ellipsis in script: "...")
- "Todo empezó con..." as a setup
- Telenovela-style narration of everyday situations
- Emphatic phrasing: "NADIE lo vio venir" (about a cluttered closet)
- The contrast between dramatic delivery and mundane reality IS the humor

**Guardrails:**
- Clearly comedic/theatrical exaggeration
- The viewer should know it's playful drama, not real distress
- Works best with voiceover pacing (pauses, emphasis, crescendo)
- The mundane subject + dramatic delivery = the comedic engine
- Never cross into actual anxiety-inducing territory

**Compatible formats:** Scenario Story, Problem Escalation

**Example phrases:**
- "Todo empezó... con un cajón que no cerraba." (pausa dramática) "Nadie imaginó... lo que vendría después."
- "Era una casa normal. Una familia normal. Hasta que un día... abrieron el trastero."
- "Lo que iba a ser una limpieza de sábado... se convirtió en una guerra."
- "Pensaban que lo tenían todo controlado. Pero el armario... tenía otros planes."
- "Tres años. Tres años guardando esa caja. Y cuando por fin la abrieron... vacía."

**Red flags (avoid):**
- Genuine anxiety or stress triggers
- Making fun of people with actual hoarding problems
- Drama so over-the-top it loses the connection to reality
- Dramatic framing of serious issues (financial stress, etc.)

**ElevenLabs settings:**
```yaml
speed: 0.98        # Slower for dramatic pauses
stability: 0.35    # Natural variation for drama
style: 0.45        # Higher emotional expression
```

---

## 5. RELATABLE (Cercano)

**Voice:** "This is SO me" content. Maximum recognition factor. First person plural. The viewer feels like you're reading their mind.

**Spanish expression notes:**
- "Dime que no..." as a hook ("Dime que no tienes un cajón así")
- "Todos hacemos esto" -- inclusive first person
- Extremely specific observations that feel universal
- "¿A que sí?" / "¿Verdad?" as confirmation hooks
- Natural, conversational pacing -- like talking to a friend

**Guardrails:**
- Zero judgment, pure recognition
- The humor comes from truth, not exaggeration
- Should feel like overhearing your own thoughts
- Hyper-specific details create the "that's me" moment
- Never makes the viewer feel weird or wrong for relating

**Compatible formats:** Question Barrage, Direct Address

**Example phrases:**
- "Dime que no tienes una bolsa llena de bolsas. O un cajón que no sabes qué tiene pero SABES que no puedes tirarlo."
- "Ese cable. No sabes de qué es. Pero si lo tiras, seguro que era importante. ¿A que sí?"
- "Todos tenemos ese mueble que 'ya lo cambio' desde hace cuatro años."
- "Esa silla del comedor que ya no usas para sentarte. Ahora es perchero. Y lo sabes."
- "Tienes una caja de mudanza de hace tres mudanzas que nunca has abierto. Lo sé porque yo también."

**Red flags (avoid):**
- Being too generic (loses the recognition magic)
- Observations that only apply to a small group
- Judgmental undertone disguised as relatability

**ElevenLabs settings:**
```yaml
speed: 1.06        # Natural conversational pace (same as default)
stability: 0.35    # Natural variation
style: 0.30        # Subtle, conversational emotion
```

---

## 6. SARCASTIC (Sarcástico)

**Voice:** Dry wit. Eye-roll delivery. Think Spanish Twitter humor. Flat delivery of sharp observations.

**Spanish expression notes:**
- "Ah sí, eso..." -- dry acknowledgment
- "Claro, claro..." -- mock agreement
- Understated delivery with sharp punchlines
- "Lo típico" -- dismissive irony
- Works best in short form (15-30s) -- sarcasm loses power if it goes too long

**Guardrails:**
- Sarcasm at SITUATIONS and BEHAVIORS, never at specific people
- Light sarcasm, not bitter or mean
- Should feel clever, not cruel
- Danger zone: can alienate if too aggressive -- keep it playful
- The target of sarcasm should be something the viewer does too (self-inclusive)

**Compatible formats:** Question Barrage, Problem Escalation

**Example phrases:**
- "Ah sí, la silla rota. La de 'ya la arreglo'. La misma que llevas prometiendo arreglar desde que Rajoy era presidente."
- "Claro, el trastero. Ese sitio donde las cosas van a morir con dignidad."
- "Lo típico. Guardas un router del dos mil dieciséis 'por si acaso'. Por si acaso qué. ¿Viajas en el tiempo?"
- "Ah, la caja de cables. El museo de tecnología que nadie pidió."
- "Sí, sí, 'algún día lo ordeno'. Ese algún día lleva tres años en lista de espera."

**Red flags (avoid):**
- Bitter or cynical sarcasm
- Targeting specific demographics
- Sarcasm that requires cultural context most viewers won't have
- Going too long -- sarcasm works in bursts, not paragraphs

**ElevenLabs settings:**
```yaml
speed: 1.08        # Slightly faster, dry delivery
stability: 0.25    # Lower stability for flat/dry variation
style: 0.35        # Understated emotional range
```

---

## Tone Selection Decision Tree

```
¿Qué efecto quieres crear?

├─ Hacer reír → HUMORISTIC o SARCASTIC
│   ├─ Risa por reconocimiento → HUMORISTIC
│   └─ Risa por ingenio seco → SARCASTIC
├─ Crear conexión emocional → EMPATHETIC o RELATABLE
│   ├─ Validar y acompañar → EMPATHETIC
│   └─ "Eso me pasa a mí" → RELATABLE
├─ Provocar una reacción → PROVOCATIVE o DRAMATIC
│   ├─ Desafiar una creencia → PROVOCATIVE
│   └─ Exagerar lo cotidiano → DRAMATIC
└─ No tengo claro → RELATABLE (más versátil)
```

---

## Tone Compatibility Matrix

| Tone | Question Barrage | Scenario Story | Problem Escalation | Direct Address | Humor Skit |
|------|:---:|:---:|:---:|:---:|:---:|
| HUMORISTIC | ++ | + | ++ | + | ++ |
| EMPATHETIC | - | ++ | - | ++ | - |
| PROVOCATIVE | ++ | - | + | ++ | - |
| DRAMATIC | - | ++ | ++ | + | + |
| RELATABLE | ++ | + | + | ++ | + |
| SARCASTIC | ++ | - | ++ | + | + |

`++` = ideal combination | `+` = works | `-` = avoid
