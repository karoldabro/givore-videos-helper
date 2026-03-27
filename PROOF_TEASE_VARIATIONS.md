# Proof Tease Section Variations

El PROOF TEASE aparece justo despues del hook (3-8s) y construye anticipacion.
Debe dar una razon para quedarse viendo, NUNCA revelar el desenlace.

---

## 8 Proof Tease Styles

### 1. STAY-TO-SEE
**Enfoque**: Clasico "quedaos hasta el final" con variedad de expresiones

**Templates**:
- "No os lo perdais al final."
- "Quedaos, que lo mejor viene ahora."
- "Si os vais antes del final, os lo perdeis."

**Tono**: 60% urgencia + 40% complicidad

**Mejor para**: Videos con reveal fuerte al final (item valioso, reaccion inesperada)

**Anti-patterns**:
- "Quedaos hasta el final" literal (quemado, prohibido)
- Sonar suplicante o desesperado
- Usar en videos sin payoff real al final

---

### 2. PROMISE-PAYOFF
**Enfoque**: Prometer algo concreto que el video entrega

**Templates**:
- "Al final os enseno lo que hice con esto."
- "Esperad a ver donde acaba esto."
- "Os voy a demostrar que esto tiene solucion."

**Tono**: 70% promesa concreta + 30% confianza

**Mejor para**: Videos donde hay una transformacion o accion clara (subir item, entregarlo, restaurarlo)

**Anti-patterns**:
- Prometer algo que el video no cumple
- Ser demasiado vago ("os enseno algo")
- Repetir la misma promesa que el hook ya implico

---

### 3. QUESTION-TEASE
**Enfoque**: Plantear una pregunta que el video responde

**Templates**:
- "La pregunta es... ha sobrevivido a la calle?"
- "Lo que no se es si alguien lo querra."
- "La duda es: esto se puede salvar o no?"

**Tono**: 60% curiosidad + 40% incertidumbre

**Mejor para**: Items en estado dudoso (danados, sucios, raros), situaciones con resultado incierto

**Anti-patterns**:
- Preguntas retoricas obvias ("es bonito, no?")
- Preguntas que el espectador no le importa responder
- Usar si el hook ya fue una pregunta (doble pregunta mata el ritmo)

---

### 4. CONTRAST-TEASE
**Enfoque**: Crear expectativa de antes/despues o primera impresion vs realidad

**Templates**:
- "Cuando lo vi, pensaba una cosa. Cuando me acerque... otra."
- "De lejos parecia basura. De cerca... ya vereis."
- "Lo primero que pense fue tirarlo. Menos mal que no lo hice."

**Tono**: 50% sorpresa + 50% cambio de perspectiva

**Mejor para**: Items que mejoran al acercarse, hallazgos inesperados, cosas que parecen peores de lo que son

**Anti-patterns**:
- Spoilear el contraste ("de lejos parecia malo pero es bueno")
- Usar sin que haya un contraste real en el video
- Forzar el giro cuando el item es claramente bueno o malo desde el principio

---

### 5. CHALLENGE-VIEWER
**Enfoque**: Retar al espectador, involucrarle activamente

**Templates**:
- "A ver si adivinais que hice."
- "Decidme en comentarios que hariais vosotros."
- "Apuesto a que no os imaginais como acaba esto."

**Tono**: 70% reto + 30% juego

**Mejor para**: Videos con desenlace sorprendente, items inusuales, situaciones con multiples opciones

**Anti-patterns**:
- Retar sin que haya algo que adivinar realmente
- Sonar condescendiente ("seguro que no lo sabeis")
- Usar en videos con desenlace predecible

---

### 6. SKIP
**Enfoque**: Sin proof tease. Del hook directo al problema/contenido.

**Templates**:
- (Sin texto. Transicion directa del hook a la siguiente seccion.)

**Duracion**: 0 segundos

**Tono**: 100% ritmo rapido

**Mejor para**: Estructuras COLD OPEN y MICRO, videos muy cortos (<30s), hooks que ya contienen suficiente anticipacion

**Anti-patterns**:
- Usar SKIP por pereza cuando el video necesita anticipacion
- Combinar con hooks debiles que no sostienen atencion solos
- Abusar: maximo 1 de cada 5 videos

---

### 7. MYSTERY-DROP
**Enfoque**: Soltar un misterio que deja al espectador enganchado

**Templates**:
- "Pero lo mejor no es lo que encontre... es lo que paso despues."
- "Y eso no es ni la mitad de la historia."
- "Esto tiene un giro que no os esperais."

**Tono**: 80% misterio + 20% emocion

**Mejor para**: Videos con narrativa fuerte, historias con giro, interacciones con personas

**Anti-patterns**:
- Prometer misterio sin entregarlo (clickbait vacio)
- Usar en videos puramente visuales sin historia
- Sonar como trailer de pelicula ("lo que paso a continuacion os dejara sin palabras")

---

### 8. NUMBER-TEASE
**Enfoque**: Anclar la atencion con un dato numerico concreto

**Templates**:
- "Tres minutos. Eso es lo que tarde en cambiar la historia de esto."
- "Un euro. Eso es lo que vale salvar algo asi."
- "Doscientos metros. Eso habia entre la basura y su nueva vida."

**Tono**: 60% dato concreto + 40% impacto emocional

**Mejor para**: Videos donde hay un dato real impactante (distancia, tiempo, valor), items con precio conocido

**Anti-patterns**:
- Inventar numeros sin base real
- Numeros que no impresionan ("veinte minutos" no es impactante)
- Usar si el hook ya tenia un numero (fatiga numerica)

---

## Decision Tree

```
Que tipo de video es?
|-- Muy corto / COLD OPEN / MICRO --> SKIP
|-- Video con reveal fuerte al final --> STAY-TO-SEE o MYSTERY-DROP
|-- Item con transformacion/accion clara --> PROMISE-PAYOFF
|-- Item en estado dudoso / resultado incierto --> QUESTION-TEASE
|-- Item que sorprende al acercarse --> CONTRAST-TEASE
|-- Desenlace sorprendente / item raro --> CHALLENGE-VIEWER
|-- Historia con giro narrativo --> MYSTERY-DROP
+-- Dato numerico impactante disponible --> NUMBER-TEASE

Que uso el HOOK?
|-- Hook fue pregunta --> NO usar QUESTION-TEASE (doble pregunta)
|-- Hook fue numerico --> NO usar NUMBER-TEASE (fatiga numerica)
|-- Hook ya genera mucha anticipacion --> SKIP es valido
+-- Hook fue debil / corto --> Necesita proof tease fuerte (MYSTERY-DROP, CONTRAST-TEASE)

Cual use en los ultimos 3 videos?
|-- Mismo estilo 2+ veces --> CAMBIAR obligatorio
+-- Todos diferentes --> Libre eleccion
```

---

## Rotation Rules

1. **NUNCA** usar el mismo estilo en videos consecutivos
2. **Verificar** via `givore-tools.sh script-rotation` antes de elegir
3. **NUNCA** repetir palabras clave del HOOK en el proof tease
4. **SKIP** maximo 1 de cada 5 videos (no abusar de la ausencia)
5. **Sugerir rotacion**: STAY-TO-SEE --> PROMISE-PAYOFF --> QUESTION-TEASE --> CONTRAST-TEASE --> CHALLENGE-VIEWER --> MYSTERY-DROP --> NUMBER-TEASE --> SKIP --> (repetir)
6. **Combinar con hook**: Si el hook ya es fuerte, permitir estilos suaves (SKIP, STAY-TO-SEE). Si el hook es debil, forzar estilos fuertes (MYSTERY-DROP, CONTRAST-TEASE, NUMBER-TEASE).

---

## Duration Guidance

| Estilo | Duracion | Notas |
|--------|----------|-------|
| STAY-TO-SEE | 2-4s | Breve, directo |
| PROMISE-PAYOFF | 3-5s | Necesita completar la promesa |
| QUESTION-TEASE | 3-5s | Dejar la pregunta flotar un segundo |
| CONTRAST-TEASE | 4-6s | Necesita dos tiempos (antes/despues) |
| CHALLENGE-VIEWER | 3-5s | Reto rapido, no alargar |
| SKIP | 0s | Sin pausa, transicion directa |
| MYSTERY-DROP | 3-6s | Dejar que el misterio pese |
| NUMBER-TEASE | 3-5s | El numero necesita un segundo para aterrizar |

**Rango general**: 3-8 segundos (excepto SKIP = 0s)

---

## Anti-Patterns Generales (NO usar)

**Proof teases que revelan el final**:
- "Al final resulta que era nuevo" --> Spoiler, mata la anticipacion
- "Y si, alguien lo quiso" --> Ya no hay razon para quedarse

**Proof teases clickbait vacios**:
- "No os vais a creer lo que paso" sin que pase nada especial
- "Esto es increible" sin nada increible detras
- Prometer giros que el video no entrega

**Proof teases que repiten el hook**:
- Si hook fue "Mirad lo que encontre" --> NO usar "Esperad a ver lo que encontre"
- Si hook fue numerico --> NO usar otro numero
- Si hook fue pregunta --> NO usar otra pregunta

**Proof teases con tono de teletienda**:
- "Pero esperad, que hay mas"
- "Y eso no es todo"
- Cualquier frase que suene a venta

---

## Emotional Formula

El PROOF TEASE debe seguir:
- 100% anticipacion genuina
- 0% spoiler del desenlace
- 0% marketing o venta
- 0% repeticion del hook

El espectador debe sentir: "Necesito ver como acaba esto" o "Ahora me ha picado la curiosidad".
