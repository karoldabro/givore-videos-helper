# Content Formats Library

20 distinct content formats for the Givore channel. Each format sends a different algorithmic signal (pacing, text overlays, audio signature, engagement trigger). Parsed by `scripts/reference_pools.py`.

## Quick Reference

| ID | Name | Length | Narration | Batch | Viral |
|----|------|--------|-----------|-------|-------|
| 1 | El Ranking Callejero | 45-60s | full | yes | HIGH |
| 2 | 60 Segundos en... | 55-65s | full | yes | HIGH |
| 3 | Lo Que Nadie Ve | 30-40s | minimal | yes | HIGH |
| 4 | Bici vs Coche | 35-50s | full | no | VERY HIGH |
| 5 | El Iceberg | 60-90s | full | no | HIGH |
| 6 | Sonidos de la Calle | 25-40s | zero | yes | MEDIUM-HIGH |
| 7 | Pregunta del Dia | 20-30s | full | yes | MEDIUM |
| 8 | Timelapse Rutero | 30-45s | minimal | no | MEDIUM-HIGH |
| 9 | No Toqueis Eso | 35-50s | full | yes | HIGH |
| 10 | POV Eres Mi Bici | 25-35s | character | yes | HIGH |
| 11 | Antes Aqui Habia | 40-55s | full | no | HIGH |
| 12 | Lo Mas Raro de Hoy | 15-25s | minimal | yes | MEDIUM-HIGH |
| 13 | Tres Cosas | 40-55s | full | yes | MEDIUM-HIGH |
| 14 | El Mapa de Hallazgos | 45-60s | full | no | MEDIUM |
| 15 | Ruta Gastro en Bici | 45-65s | full | no | HIGH |
| 16 | El Que Tira Gana | 35-50s | full | no | MEDIUM-HIGH |
| 17 | Lluvia Noche Extremo | 25-40s | minimal | yes | MEDIUM-HIGH |
| 18 | Mi Setup | 40-55s | full | no | MEDIUM |
| 19 | Cuanto Cuesta | 20-35s | full | yes | VERY HIGH |
| 20 | Classic Street Finds | 40-60s | full | yes | MEDIUM |

---

### FORMAT 1: EL_RANKING_CALLEJERO

- **Name**: El Ranking Callejero
- **Length**: 45-60s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, ITEM_5, ITEM_4, ITEM_3, ITEM_2, ITEM_1, RECAP, CTA
- **Compatible structures**: COUNTDOWN, CLASSIC
- **Compatible personas**: ALL
- **Incompatible personas**: none
- **Clip guidance**: 5+ item clips ranked worst-to-best. Body/bridge clips for transitions between items. End with [end] clip after recap.
- **Content pillar**: CYCLING_POV, HIDDEN_SPOTS
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "Ranking de los hallazgos mas locos de esta semana -- del peor al mejor."
- **CTA approach**: ENGAGEMENT (comment with rating)
- **Algorithm signal**: list format + text overlays + countdown + comment bait = different from standard narration

### FORMAT 2: 60_SEGUNDOS_EN

- **Name**: 60 Segundos en...
- **Length**: 55-65s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, FIRST_SIGHT, HIDDEN_GEM, FOOD_SPOT, SURPRISE_FACT, STREET_FIND, CTA
- **Compatible structures**: CLASSIC, COUNTDOWN
- **Compatible personas**: ENERGETICO, REPORTERO, VECINA
- **Incompatible personas**: POETA
- **Clip guidance**: 5-6 clips per barrio (10s each), all cycling POV. Timer graphic overlay. Fast cuts. One barrio per episode.
- **Content pillar**: BARRIO_GUIDES, CYCLING_POV
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "60 segundos para ensenaros [BARRIO]. Empiezo YA."
- **CTA approach**: COMMUNITY (ask which barrio next)
- **Algorithm signal**: timer constraint + rapid cuts + geographic tags + urgency = different audio/visual rhythm

### FORMAT 3: LO_QUE_NADIE_VE

- **Name**: Lo Que Nadie Ve
- **Length**: 30-40s
- **Narration**: minimal
- **Batch compatible**: yes
- **Script sections**: HOOK, REVEAL_1, REVEAL_2, REVEAL_3, REFLECTION
- **Compatible structures**: COLD OPEN, LOOP
- **Compatible personas**: OBSERVADOR, POETA
- **Incompatible personas**: ENERGETICO
- **Clip guidance**: 3 reveal moments from cycling footage -- unexpected beauty, hidden courtyards, rooftop gardens, cat colonies. No text overlays except opening title. Ambient audio prominent.
- **Content pillar**: HIDDEN_SPOTS, DAILY_LIFE
- **Platform priority**: Instagram, TikTok
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "Esto solo lo ves si vas en bici por Valencia."
- **CTA approach**: SAVE (no in-video CTA, CTA in comments only)
- **Algorithm signal**: slow pacing + ambient audio + contemplative mood + minimal text = quiet flex aesthetic

### FORMAT 4: BICI_VS_COCHE

- **Name**: Bici vs Coche
- **Length**: 35-50s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, COMPARISON_1, COMPARISON_2, COMPARISON_3, SELF_DEPRECATION, CLOSE
- **Compatible structures**: CLASSIC, PSP
- **Compatible personas**: ENERGETICO, VECINA, REPORTERO
- **Incompatible personas**: POETA
- **Clip guidance**: Cycling POV clips contrasted with static/boring street-level shots. Split-screen or alternating cuts with text labels. Self-deprecating rain clip at the end if available.
- **Content pillar**: CYCLING_POV, CITY_COMPARISONS
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: VERY HIGH
- **Series**: no
- **Hook template**: "Lo que ves en coche vs lo que veo yo en bici por la misma calle."
- **CTA approach**: ENGAGEMENT (team bici vs team coche debate)
- **Algorithm signal**: comparison structure + debate trigger + humor + split format = high comment velocity

### FORMAT 5: EL_ICEBERG

- **Name**: El Iceberg
- **Length**: 60-90s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, SURFACE, MID_LEVEL, DEEP_LEVEL, ABYSS, SERIES_HOOK, CTA
- **Compatible structures**: COUNTDOWN, CLASSIC
- **Compatible personas**: OBSERVADOR, REPORTERO, POETA
- **Incompatible personas**: ENERGETICO
- **Clip guidance**: Clips sorted by obscurity level. Surface = well-known landmarks. Deep = ultra-specific observations. Iceberg graphic template as recurring overlay. Longer format needs strong visual variety.
- **Content pillar**: HIDDEN_SPOTS, BARRIO_GUIDES
- **Platform priority**: TikTok, Instagram
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "El iceberg de Valencia en bici. Cuanto mas abajo, menos gente lo sabe."
- **CTA approach**: ENGAGEMENT (comment what level you are)
- **Algorithm signal**: graphic-heavy + layered information + series hook + longer watch time

### FORMAT 6: SONIDOS_DE_LA_CALLE

- **Name**: Sonidos de la Calle
- **Length**: 25-40s
- **Narration**: zero
- **Batch compatible**: yes
- **Script sections**: OPENING_SOUND, SCENE_1, SCENE_2, SCENE_3, BLEND, CLOSE_TEXT
- **Compatible structures**: LOOP, COLD OPEN
- **Compatible personas**: OBSERVADOR, POETA
- **Incompatible personas**: ENERGETICO, VECINA, REPORTERO
- **Clip guidance**: Cycling footage with good ambient audio (not wind-blasted). Text overlays identify each sound. NO music. NO narration. Pure ambient sound is the format.
- **Content pillar**: CITY_SOUNDS
- **Platform priority**: TikTok, Instagram
- **Viral potential**: MEDIUM-HIGH
- **Series**: yes
- **Hook template**: (no voice) Text overlay: "SONIDOS DE [BARRIO] -- [HORA]"
- **CTA approach**: SAVE (calming content triggers saves)
- **Algorithm signal**: zero narration + ambient audio + ASMR pattern break + text-only overlays = completely different audio fingerprint

### FORMAT 7: PREGUNTA_DEL_DIA

- **Name**: Pregunta del Dia
- **Length**: 20-30s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK_QUESTION, PERSONAL_TAKE, VISUAL_TRIGGER, OPEN_END
- **Compatible structures**: MICRO, CLASSIC
- **Compatible personas**: VECINA, ENERGETICO, REPORTERO
- **Incompatible personas**: POETA
- **Clip guidance**: Throwaway cycling footage (any ride works). Big text overlay with the question. Footage of the thing that prompted the question in the middle. Short format, 40-60 words narration.
- **Content pillar**: DAILY_LIFE, COMMUNITY
- **Platform priority**: TikTok, Instagram
- **Viral potential**: MEDIUM
- **Series**: yes
- **Hook template**: "Pregunta seria mientras pedaleo: [pregunta provocadora]?"
- **CTA approach**: ENGAGEMENT (must comment with opinion)
- **Algorithm signal**: micro-format + question = high comment rate + duet/stitch bait = follower conversion engine

### FORMAT 8: TIMELAPSE_RUTERO

- **Name**: Timelapse Rutero
- **Length**: 30-45s
- **Narration**: minimal
- **Batch compatible**: no
- **Script sections**: HOOK_MAP, HYPERLAPSE, ARRIVAL, STATS, CLOSE
- **Compatible structures**: MICRO, COLD OPEN
- **Compatible personas**: OBSERVADOR, ENERGETICO
- **Incompatible personas**: VECINA
- **Clip guidance**: One long continuous cycling ride sped up 8-16x. Map graphic at start showing route. Text callouts for landmarks as they flash by. Normal speed bookends at start and arrival.
- **Content pillar**: CYCLING_POV
- **Platform priority**: TikTok, Instagram, YouTube Shorts
- **Viral potential**: MEDIUM-HIGH
- **Series**: yes
- **Hook template**: "Mi ruta diaria: 7 kilometros en 30 segundos."
- **CTA approach**: SAVE (practical route value)
- **Algorithm signal**: hyperlapse visual + speed transitions + map overlay + minimal narration = different pacing signature

### FORMAT 9: NO_TOQUEIS_ESO

- **Name**: No Toqueis Eso
- **Length**: 35-50s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, WARNING_1, WARNING_2, PIVOT, CRITERIA, CLOSE
- **Compatible structures**: PSP, CLASSIC, COLD OPEN
- **Compatible personas**: REPORTERO, VECINA, OBSERVADOR
- **Incompatible personas**: POETA
- **Clip guidance**: Cycling approach to problematic street items. Close-up shots of specific damage (water damage, structural issues). Pivot to a GOOD find nearby. Educational tone, not preachy.
- **Content pillar**: MINIMALISM, STREET_FINDS
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "Veis ese sofa en la calle? NO lo cojais. Os explico."
- **CTA approach**: ENGAGEMENT (debate: I would have taken it!)
- **Algorithm signal**: contrarian hook + educational content + pattern interrupt + controversy = high save + comment rate

### FORMAT 10: POV_ERES_MI_BICI

- **Name**: POV Eres Mi Bici
- **Length**: 25-35s
- **Narration**: character
- **Batch compatible**: yes
- **Script sections**: HOOK_POV, MONOLOGUE, DRAMA, DISCOVERY_REACTION, SIGN_OFF
- **Compatible structures**: MICRO, LOOP
- **Compatible personas**: ENERGETICO, VECINA
- **Incompatible personas**: REPORTERO, OBSERVADOR
- **Clip guidance**: Standard cycling footage with completely different narration treatment. Character voice (sarcastic, tired, dramatic bike). Subtitles are critical -- humor is in the text. Funny/quirky sound effects.
- **Content pillar**: CYCLING_POV, DAILY_LIFE
- **Platform priority**: TikTok, Instagram
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "POV: eres mi bici y hoy me toca ruta por [BARRIO]."
- **CTA approach**: SHARE (people send it saying "this is literally us")
- **Algorithm signal**: character voice + humor + POV format + different audio personality = completely new content signal

### FORMAT 11: ANTES_AQUI_HABIA

- **Name**: Antes Aqui Habia
- **Length**: 40-55s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, LOCATION_1_BEFORE, LOCATION_1_NOW, LOCATION_2, LOCATION_3, REFLECTION, CTA
- **Compatible structures**: CLASSIC, COLD OPEN
- **Compatible personas**: OBSERVADOR, VECINA, POETA
- **Incompatible personas**: ENERGETICO
- **Clip guidance**: Cycling past specific changed locations. Old photos if available (optional). 3 before/after locations per episode. Warm nostalgic music, not angry. Balanced narration -- observational, not political.
- **Content pillar**: BARRIO_GUIDES, HIDDEN_SPOTS, COMMUNITY
- **Platform priority**: Instagram, TikTok, Facebook
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "Antes aqui habia un bar que conocia todo el barrio. Ahora hay esto."
- **CTA approach**: COMMUNITY (what changed in YOUR barrio?)
- **Algorithm signal**: nostalgia trigger + local pride + debate (gentrification) + tag-a-friend = high share + comment velocity

### FORMAT 12: LO_MAS_RARO_DE_HOY

- **Name**: Lo Mas Raro de Hoy
- **Length**: 15-25s
- **Narration**: minimal
- **Batch compatible**: yes
- **Script sections**: HOOK, BUILDUP, REVEAL, REACTION
- **Compatible structures**: MICRO, COLD OPEN
- **Compatible personas**: ENERGETICO, VECINA
- **Incompatible personas**: POETA
- **Clip guidance**: Single weirdest moment from any ride. One hook, one reveal, one reaction. 30-40 words narration max. Funny/quirky sound effect or trending audio.
- **Content pillar**: DAILY_LIFE, CYCLING_POV
- **Platform priority**: TikTok, Instagram
- **Viral potential**: MEDIUM-HIGH
- **Series**: yes
- **Hook template**: "Lo mas raro que he visto hoy en bici por Valencia."
- **CTA approach**: SHARE (look at this! natural send-to-friend trigger)
- **Algorithm signal**: ultra-short + curiosity gap + single reveal = near 100% completion rate + replay value

### FORMAT 13: TRES_COSAS

- **Name**: Tres Cosas
- **Length**: 40-55s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, FACT_1, FACT_2, FACT_3, VOTE_CTA, SERIES_HOOK
- **Compatible structures**: COUNTDOWN, CLASSIC
- **Compatible personas**: REPORTERO, VECINA, ENERGETICO
- **Incompatible personas**: POETA
- **Clip guidance**: Cycling through the barrio showing relevant locations. 3 text overlays (one per fact). Facts escalate: interesting, surprising, mind-blowing. Informative but conversational narration.
- **Content pillar**: BARRIO_GUIDES, HIDDEN_SPOTS
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: MEDIUM-HIGH
- **Series**: yes
- **Hook template**: "3 cosas que no sabiais de [BARRIO]. La tercera os va a flipar."
- **CTA approach**: ENGAGEMENT (vote 1, 2 or 3)
- **Algorithm signal**: listicle + numbered structure + third-item tease + educational saves = proven completion driver

### FORMAT 14: EL_MAPA_DE_HALLAZGOS

- **Name**: El Mapa de Hallazgos
- **Length**: 45-60s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, CLUSTER_1, CLUSTER_2, SURPRISE_CLUSTER, PATTERNS, CTA
- **Compatible structures**: CLASSIC, PSP
- **Compatible personas**: REPORTERO, OBSERVADOR
- **Incompatible personas**: ENERGETICO, POETA
- **Clip guidance**: Map graphic of Valencia with pins. Zoom into barrio clusters with quick cycling clips from those finds. Monthly cadence. Data-driven narration (counts, patterns, day-of-week trends). Uses Givore DB location data.
- **Content pillar**: STREET_FINDS, BARRIO_GUIDES
- **Platform priority**: Instagram, TikTok, Facebook
- **Viral potential**: MEDIUM
- **Series**: yes
- **Hook template**: "He marcado TODOS los muebles que he encontrado en la calle este mes. Mirad el mapa."
- **CTA approach**: COMMUNITY (which barrio to investigate next)
- **Algorithm signal**: infographic + map + data visualization = completely different content type signal + high save rate

### FORMAT 15: RUTA_GASTRO_EN_BICI

- **Name**: Ruta Gastro en Bici
- **Length**: 45-65s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, STOP_1, STOP_2, STOP_3, TOTAL_MONTAGE, CTA
- **Compatible structures**: CLASSIC, COUNTDOWN
- **Compatible personas**: ENERGETICO, VECINA
- **Incompatible personas**: POETA, OBSERVADOR
- **Clip guidance**: Cycling approach + brief park at each food stop. Show the food/item with price text overlay. 3 stops per episode. Total calculation montage at end. Requires stopping and filming food (not just cycling past).
- **Content pillar**: STREET_FOOD, CYCLING_POV
- **Platform priority**: TikTok, Instagram, Facebook
- **Viral potential**: HIGH
- **Series**: yes
- **Hook template**: "Ruta gastro en bici por [BARRIO]. Todo por menos de 5 euros."
- **CTA approach**: COMMUNITY (ask which barrio/route next)
- **Algorithm signal**: food content + price challenge + cycling differentiator = crosses into food audience + high save rate

### FORMAT 16: EL_QUE_TIRA_GANA

- **Name**: El Que Tira Gana
- **Length**: 35-50s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, ITEM_BEFORE, BRIDGE_STORY, ITEM_AFTER, REFLECTION, UGC_CTA
- **Compatible structures**: CLASSIC, COLD OPEN, PSP
- **Compatible personas**: VECINA, OBSERVADOR, POETA
- **Incompatible personas**: ENERGETICO
- **Clip guidance**: Before footage from street-find cycling clips. After photos from community/users if available. Storytelling narration -- slower pace, warm. Uplifting music, not cycling beat.
- **Content pillar**: MINIMALISM, COMMUNITY
- **Platform priority**: Instagram, TikTok, Facebook
- **Viral potential**: MEDIUM-HIGH
- **Series**: yes
- **Hook template**: "Una persona dejo esto en la calle. Otra persona lo tiene en su salon. La historia."
- **CTA approach**: UGC (show us your rescue -- duets/stitches/comments with photos)
- **Algorithm signal**: story format (problem-journey-resolution) + before/after + emotional ROI + UGC invitation = high share + duet rate

### FORMAT 17: LLUVIA_NOCHE_EXTREMO

- **Name**: Lluvia Noche Extremo
- **Length**: 25-40s
- **Narration**: minimal
- **Batch compatible**: yes
- **Script sections**: AMBIENT_OPEN, SCENE_1, SCENE_2, BEAUTY_SHOT, CLOSE_TEXT
- **Compatible structures**: LOOP, COLD OPEN
- **Compatible personas**: OBSERVADOR, POETA
- **Incompatible personas**: ENERGETICO, REPORTERO
- **Clip guidance**: Rain/night/extreme-condition cycling footage. Rain on lens, wet street reflections, neon lights, empty streets. Minimal or zero narration -- visuals and ambient sound carry. Lo-fi or ambient music. Cinematic feel even from basic camera.
- **Content pillar**: WEATHER, NIGHT_CYCLING, CITY_SOUNDS
- **Platform priority**: Instagram, TikTok
- **Viral potential**: MEDIUM-HIGH
- **Series**: no
- **Hook template**: "Valencia con lluvia desde la bici. Hay gente que dice que estoy loco."
- **CTA approach**: SAVE (atmospheric content triggers saves)
- **Algorithm signal**: cinematic visuals + ambient audio + quiet flex aesthetic + zero/minimal voice = high save rate + different mood signal

### FORMAT 18: MI_SETUP

- **Name**: Mi Setup
- **Length**: 40-55s
- **Narration**: full
- **Batch compatible**: no
- **Script sections**: HOOK, CAMERA_MOUNT, PHONE_SETTINGS, FOOTAGE_PAYOFF, SECRET_TIP, CTA
- **Compatible structures**: CLASSIC, PSP
- **Compatible personas**: REPORTERO, VECINA
- **Incompatible personas**: POETA
- **Clip guidance**: Close-up of bike/camera setup. Demo of attachment. Cut to best POV clips as proof. Practical, direct tone. One-off or very rare format (1-2x total).
- **Content pillar**: BIKE_MAINTENANCE, DAILY_LIFE
- **Platform priority**: TikTok, Instagram, YouTube Shorts
- **Viral potential**: MEDIUM
- **Series**: no
- **Hook template**: "Me preguntan mucho: como grabas pedaleando? Os lo enseno."
- **CTA approach**: ENGAGEMENT (comment with questions for follow-up video)
- **Algorithm signal**: behind-the-scenes + gear content + how-to = attracts creator audience + high save rate

### FORMAT 19: CUANTO_CUESTA

- **Name**: Cuanto Cuesta
- **Length**: 20-35s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, ITEM_REVEAL, PRICE_GUESS, PRICE_SHOCK, CLOSE
- **Compatible structures**: MICRO, COLD OPEN, CLASSIC
- **Compatible personas**: ENERGETICO, VECINA, REPORTERO
- **Incompatible personas**: POETA
- **Clip guidance**: Cycling approach to a street-find item. Dramatic pause before price reveal. Text overlay with price. Short format for high completion rate. Can batch from existing item footage with price research added.
- **Content pillar**: STREET_FINDS, MINIMALISM
- **Platform priority**: TikTok, Instagram
- **Viral potential**: VERY HIGH
- **Series**: yes
- **Hook template**: "Esto lo he encontrado en la calle. Sabeis cuanto cuesta nuevo?"
- **CTA approach**: ENGAGEMENT (guess the price in comments)
- **Algorithm signal**: price shock reveal + guessing game + short format = extreme comment velocity + replay for the number

### FORMAT 20: CLASSIC_STREET_FINDS

- **Name**: Classic Street Finds
- **Length**: 40-60s
- **Narration**: full
- **Batch compatible**: yes
- **Script sections**: HOOK, PROBLEM, PROOF_TEASE, REHOOK, IMPORTANCE, SOLUTION, ITEM_INTRO, CTA
- **Compatible structures**: CLASSIC, COLD OPEN, LOOP, MICRO, PSP, COUNTDOWN
- **Compatible personas**: ALL
- **Incompatible personas**: none
- **Clip guidance**: Standard 8-section script structure. Cycling POV footage + item clips. Uses full rotation system (hooks, CTAs, phrases, problems, rehooks, importance, solutions, item intros). The original Givore format.
- **Content pillar**: CYCLING_POV, STREET_FINDS, MINIMALISM
- **Platform priority**: Instagram, TikTok, Facebook
- **Viral potential**: MEDIUM
- **Series**: no
- **Hook template**: (uses HOOKS_LIBRARY rotation -- no fixed template)
- **CTA approach**: (uses CTA_VARIATIONS rotation -- no fixed approach)
- **Algorithm signal**: standard narrated cycling POV -- the baseline format. Other formats exist to diversify away from this signal.
