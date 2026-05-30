# Slides polish plan — `bootcamp_talk_AL.pptx`

Audit target: [build/_build_slides.py](../build/_build_slides.py) (531 lines) which generates [presentations/bootcamp_talk_AL.pptx](../presentations/bootcamp_talk_AL.pptx). Style intentionally mirrors `presentations/Neurotech Bootcamp prelude.pptx` (dark header, white body, teal accent bar).

## Overall

The visual baseline is strong: dark `#3A3A3A` header, white body, teal `#4A8D7E` accent bar, Calibri text, ●/○ bullets. Layout is balanced and reads well in 16:9. Two real polish problems plus a few minor drifts.

## P0 — must do before this gets shown

- **Six visible `[TODO ...]` brackets render verbatim in the rendered deck** (slides "What is neurotechnology", "The problem", "The visual pathway", "Clinical landscape"). Eyesores during a live talk. Replace with safe directional copy or drop the offending bullet. Refs: [_build_slides.py:371](../build/_build_slides.py#L371), [:399](../build/_build_slides.py#L399), [:406](../build/_build_slides.py#L406), [:415-418](../build/_build_slides.py#L415-L418).
- **Six TODO bracket replacements suggested** (none are authoritative — Antonio should verify before delivery):
  - "Today: ~$15B field, growing fast [TODO confirm 2026 number]" → drop the bracket: "Today: ~$15B field, growing fast" (number is widely cited; if outdated, replace later).
  - "Profound blindness — scale & unmet need [TODO numbers]" → "Profound blindness — ~40M worldwide; no treatment for late-stage retinal or post-chiasmal causes" (drop if numbers are unverified; just "Profound blindness — large unmet need across many causes" is also safe).
  - "Receptive fields and cortical magnification [TODO figure]" → "Receptive fields and cortical magnification — foveal patches dominate V1 area" (drop the figure note; figure can be added later as a slide_image_focus).
  - "Second Sight / Orion — cortical surface program [TODO status]" → "Second Sight / Orion — cortical surface program (Second Sight ceased ops 2022; Vivani holds IP)".
  - "Cortivis — penetrating array, EU trial [TODO status]" → "Cortivis — penetrating array, EU/UMH effort (Fernández cohort, ongoing)".
  - "Where the field is in 2026 [TODO one-line summary]" → "2026: small but real human-subject programs; the bottleneck has shifted from electrode hardware to mapping, decoding, and closed-loop control".

## P1 — alignment with HTML polish

- **Slide-pipeline label drift**: pipeline-strip uses "Neuromod & stim" ([:271](../build/_build_slides.py#L271)) — jargony. Other modules use full words ("Computer vision", "Phosphene simulation", "Decoding & closed loop"). Recommend "Neuromodulation & stim" or just "Stimulation" to match. **Fix:** change to "Neuromodulation\n& stim".
- **Module spotlight title for M3**: ([:476](../build/_build_slides.py#L476)) "M3 — Neuromodulation & stim" → "M3 — Neuromodulation & stimulation" (matches the HTML's `M3 · Neuromodulation & stimulation` title).
- **Add the Neurolight pipeline-foundation citation** that the HTMLs now carry in their footers. Best location: the closing slide ("Let's build.") OR a credit on "Today's pipeline" / "Where this is heading". **Fix:** add it as a small muted credit on `slide_closing()`.

## P2 — minor

- **`slide_program()` and `slide_tracks()` are defined but never called** ([:237-258](../build/_build_slides.py#L237-L258), [:300-324](../build/_build_slides.py#L300-L324)). Comment says they're covered in the prelude. **Fix:** delete the dead helpers OR mark them with a `# kept for live re-use` comment. Recommend delete to reduce noise.
- **M2 spotlight is the only module slide without a supporting image** — every other M-slide uses `slide_bullets_image`. M2 uses `slide_module` (typography-only). Reads cleanly but breaks pattern. **Fix:** either add an M2-appropriate image from `presentations/sources/brain_chip_2024/images/` (a saliency/heatmap) or formally accept the typography-only layout. **Skip for now** unless Antonio nominates an image — picking the wrong figure is worse than no figure.
- **Title-case separator**: slides use ` — ` (em dash) on titles ("M1 — Computer vision"), HTMLs now use ` · ` (middle dot) ("M1 · Computer vision"). Both legitimate; keep slides on em dash (it reads cleaner at 30pt). No fix.

## Out of scope

- Adding content for the genuinely-missing TODO items (real blindness scale numbers, exact 2026 program statuses, the cortical-magnification figure) — Antonio's call.
- Switching the accent from teal to anything else — the teal intentionally mirrors the prelude deck.

## Verification

1. Run `python build/_build_slides.py` — should regenerate `presentations/bootcamp_talk_AL.pptx` cleanly.
2. Open the resulting PPTX (or convert to PDF) and visually confirm: no `[TODO ...]` strings visible; M3 title reads "Neuromodulation & stimulation"; closing slide carries the Neurolight credit.
