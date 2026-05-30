# `bootcamp_talk_AL.pptx` — content enrichment plan

User signal: *"feels too dead and contentless, but is going well."* Polish (typography, layout, accent) is done — see [SLIDES_POLISH_PLAN.md](SLIDES_POLISH_PLAN.md). This pass is about **what's on the slides**, not how they look.

## Current state (after polish passes)

25 slides, but the layout count tells the story:

- **10 text-only bullet slides** (1, 3, 4, 5, 6, 8, 9, 10, 11, 15) — over a third of the deck
- 4 section dividers (2, 7, 13, 16)
- 5 bullets+image (14, 19, 21, 22, 23) — these are the strongest
- 3 image-focus (12, 17, 24)
- 1 pipeline (18), 1 module-typography (20), 1 closing (25)

The opening 6 slides (About me → What is neurotech → Neural engineering → BCIs → Where the field is → section divider) is pure exposition with zero figures. Same for slides 8–11 (problem → pathway → why intracortical → clinical landscape). The audience doesn't see a real image until **slide 7** and then again at **slide 12**.

## Three professional takes

### 1. The senior scientist (Fernández-style)
> *"Where's the evidence? You have real percepts from the Moran cohort, Roelfsema's NHP data, Maureen's diff-sim, Granley's HILO — you cite them but don't show them. Slides 8–11 read like a Wikipedia summary. The audience didn't come for an undergrad lecture; they came for **you**."*

**Implication:** every claim slide should carry the figure that backs it. The repo already has 100+ extracted source images.

### 2. The communication coach (TED-style)
> *"Open on a phosphene, a face, or a question — not a bio. Six bullets about your CV is a LinkedIn page, not a hook. Trim the definition slides; let the pipeline diagram and the module screenshots earn the room. The 'Let's build' close is great. Everything before it should sprint toward it."*

**Implication:** front-load energy. Cut or merge slides 3–6 into one definition slide. The 4 walls framework from the original talk is a stronger spine than "What is neurotechnology / Neural engineering / BCIs / Where the field is."

### 3. The bootcamp student (target audience)
> *"I don't know any of these names. Show me what I'll build today. The phosphene render slide and the module screenshots made me lean forward — those are the only ones that did. Make me want the next 4 hours."*

**Implication:** the module spotlight stretch (19–23) is doing the heaviest lifting. Pull a hint of that energy forward — show one phosphene render or one module screenshot in the first 5 slides so the audience sees the payoff early.

## Asset inventory (already in repo, ready to use)

- **`presentations/sources/brain_chip_2024/images/`** — 100+ extracted source images from your previous talk, indexed by slide (`s01_*` through `s60_*`). Manifest in `transcript.txt`.
- **`modules/M4-phosphene-simulation/assets/`** — 5 phosphene-evolution **GIFs** (`fade_all_active`, `fade_edges`, `phosphene_growth`, `raster_checker`, `raster_horizontal`). PPTX supports GIFs.
- **`modules/assets/cortical_prosthesis_fig.png`** — labeled full-pipeline schematic.
- **`presentations/sources/brain_chip_2024/transcript.txt`** — your own narrative beats from the prior talk: *4 walls to break* (surgical planning, neural phosphene mapping, computer-vision in real scenes, HILO stim).

## The plan — P0 (do these)

**Goal:** drop the text-only slide count from 10 → 4 by swapping in figures you already have, and tighten the opening.

### Opening tighten (slides 1, 3–6 → 3 slides max)

- **Slide 1 "About me"** — keep, but add one face/portrait or one phosphene render to the right side. Six bullets at size 18 + a single image is still calmer than six bullets alone. *(If no portrait is fair game, use `s33_p06_*.gif` — phosphene dynamics — as a single visual anchor and shrink bullets to 4.)*
- **Merge slides 3–6** ("What is neurotechnology" / "Neural engineering" / "BCIs" / "Where the field is") → **one slide**: *"Neurotechnology in 2026"* with three columns (Deployed · Emerging · Frontiers) and a small icon or screenshot per column. Saves 3 slides without losing the framing.
- **Net:** 6 opening slides → 2 opening slides. Audience sees the pipeline earlier.

### Mid-deck figure-ification (slides 8–11)

These are the worst dead-zone. Each can absorb one image from `brain_chip_2024/images/`:

| Slide | Current | Add (proposed) |
|---|---|---|
| 8 "The problem" | text-only | `s04_p01_*` or `s07_p01_*` (eye/anatomy or pathway image from your old talk's "challenges" slide) — supports the "upstream pathway is broken" line |
| 9 "The visual pathway" | text-only | `s15_p01_*` (cortical magnification visual) — your most-needed missing figure per pass 1 |
| 10 "Why intracortical" | text-only | `s14_p01_*` or `s12_p01_*` (electrode-array hardware photo) — show the actual implant being compared, not just words |
| 11 "Clinical landscape" | text-only | Programme-logo collage OR `s25_p01_*` (Fernández/Moran patient setup) — gives the names a face |

Each becomes `slide_bullets_image` (4 bullets + image), not `slide_image_focus` — keep the bullets, just stop them from being alone.

### One narrative borrow from "Brain and the Chip 2024"

Your previous talk had a tight **"4 walls to break"** spine (surgical planning · neural phosphene mapping · computer-vision in real scenes · HILO stim — see transcript slides 10–11). It maps almost 1:1 onto the module pipeline (M1+M2 ≈ CV in real scenes, M3 ≈ HILO stim, M4 ≈ phosphene sim, M5 ≈ closed loop, with surgical planning as an honorable mention via vimplant2). **Add one slide between 11 and 12** titled *"Four walls between us and a real vision implant"* that names the 4 walls and then immediately segues into *"…this bootcamp gives you a working pipeline for each."* This is the bridge the current deck is missing.

### One animated GIF

Slide 12 ("What patients actually see") is currently a static image. Swap or supplement with `modules/M4-phosphene-simulation/assets/phosphene_growth.gif` — phosphenes don't just *appear*, they *fade in*. A 2-second loop sells the *"sparse, punctate, dynamic"* caption in a way no still can.

## P1 — nice to have (skip if time-boxed)

- **Slide 15 "Safety limits"** is text-only and stays text-only (formulas are fine without imagery) — but consider a small inset Shannon-k chart from `s28_p01_*` if it exists.
- **M2 spotlight image** (deferred from pass 1) — still needs your eye to nominate a saliency/heatmap figure from `brain_chip_2024/images/` or rendered from the M2 HTML widget.
- **Slide 20 (M2 module)** currently uses `slide_module` (typography-only). Same fix as M2-spotlight — pick one figure, switch to `slide_bullets_image`.

## Out of scope

- Re-writing actual bullet content (you've already done this in polish pass 1; the words are fine).
- Adding video.
- Re-doing the closing — it works.

## Verification

Same as polish passes: regenerate PPTX, regenerate PDF via PowerPoint COM, visually scan all 24-ish slides. Specifically check that the figures chosen don't overflow the body box (the slide_bullets_image layout reserves bottom half for the image; tall portrait images get cropped).

## Order of operations (lean)

1. **Merge 3–6 into one slide** (delete-heavy, low-risk).
2. **Add figures to slides 8, 9, 10, 11** (one builder edit per slide, swap `slide_bullets` → `slide_bullets_image`).
3. **Insert "Four walls" bridge slide** between 11 and 12.
4. **Swap slide 12 image for the GIF** (if PPTX accepts the animation cleanly — fallback: keep PNG).
5. **Add visual to slide 1** (portrait or anchor GIF).

That's ~6 builder edits. Should reduce text-only slide count from 10 → 4 and total slide count from 25 → ~22 without losing content. Each step is independently committable.
