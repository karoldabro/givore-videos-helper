# Renueva — AI Image Prompt Templates (Nano Banana Pro)

## Base Template
```
Photo of a [ITEM_AFTER], [STYLE_DETAILS], in a [SETTING].
The [ITEM] has been [TRANSFORMATION]. Realistic interior design
photography, warm natural lighting, shallow depth of field, magazine quality.
```

## Parameters

### ITEM_AFTER
Describe the item in its transformed state. Be specific about materials and finish.
- "restored wooden side table with sage green chalk paint and brass hairpin legs"
- "refinished oak bookshelf with natural oil finish and new black metal brackets"
- "upcycled dresser converted into a bathroom vanity with marble top"

### STYLE_DETAILS
Visual details that make the image compelling.
- "with a potted monstera plant on top and a stack of books"
- "styled with a ceramic vase and dried eucalyptus branches"
- "with a cozy knit throw draped over one arm"

### SETTING
Where the item lives in its new life. Match to item type.
- **Furniture**: "modern minimalist living room with white walls"
- **Furniture**: "bright Scandinavian bedroom with wooden floors"
- **Decor**: "bohemian living room shelf with warm lighting"
- **Decor**: "clean white gallery wall in a bright hallway"
- **Appliance**: "retro-styled kitchen counter with subway tiles"
- **Creative**: "sunny Mediterranean terrace with terracotta pots"
- **Outdoor**: "small urban balcony garden with string lights"

### TRANSFORMATION
What was done to the item. Active past tense.
- "carefully sanded, repainted in chalk paint, and fitted with new hairpin legs"
- "stripped of old varnish, oiled with tung oil, revealing beautiful grain"
- "converted into a planter by adding drainage holes and painting in terracotta"

## Category-Specific Templates

### FURNITURE
```
Photo of a [transformed furniture piece], [finish and hardware details],
in a [room type] with [decor context]. The piece has been [restoration steps].
Realistic interior design photography, warm natural lighting from a window,
shallow depth of field, magazine editorial quality.
```

### DECOR
```
Photo of a [transformed decor item], [finish details], displayed on
[surface/wall] in a [room setting]. The item has been [transformation steps].
Realistic interior photography, soft ambient lighting, styled vignette,
magazine quality.
```

### APPLIANCE
```
Photo of a [restored/repurposed appliance], [finish and functional details],
on a [surface] in a [room setting]. The appliance has been [restoration steps].
Realistic product photography, clean background, warm lighting, editorial quality.
```

### CREATIVE
```
Photo of a [upcycled creative item], [material and finish details],
in a [setting]. The item was originally a [original item] and has been
[transformation description]. Realistic photography, interesting angle,
warm natural lighting, artistic quality.
```

## Style Modifiers (append to any template)
- **Warm**: ", golden hour lighting, warm color palette"
- **Clean**: ", bright even lighting, white and neutral tones"
- **Moody**: ", soft dramatic lighting, dark background, spotlight on item"
- **Outdoor**: ", dappled sunlight, garden setting, natural backdrop"

## Quality Keywords (always include)
Always end prompts with: "Realistic photography style, [lighting], shallow depth of field, magazine quality."

## Anti-Patterns (avoid)
- Do NOT use "AI generated" or "digital art" in prompts
- Do NOT use cartoon/illustration styles
- Do NOT include people in the images
- Do NOT use overly perfect/sterile environments — keep them lived-in
- Do NOT use "hyper-realistic" — just "realistic" produces better results
