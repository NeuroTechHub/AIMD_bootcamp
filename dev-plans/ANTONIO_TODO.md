# Antonio — outstanding

Personal punch list for the AIMD 2026 bootcamp tree. Update or strike through
as items land. Living doc — not generated.

## Visible TODOs

- **Replace M1 main figure (prosthesis system).**
  [modules/computer-vision.html:285-293](../modules/computer-vision.html#L285-L293)
  still wraps `assets/cortical_prosthesis_fig.jpg` (the de Ruyter van
  Steveninck 2022 schematic) in a loud dashed-red TODO banner. Swap the asset
  for the final overview figure, keep the figcaption / attribution accurate to
  whatever replaces it, then delete the banner block.

- ~~**Finish M5 (closed loop & decoding).**~~ Done. All nine sections wired
  per [M5_CLOSED_LOOP_PLAN_2026-05-28.md](./M5_CLOSED_LOOP_PLAN_2026-05-28.md):
  hero diagram, mean-pixel readout, PID demo, in-browser TF.js training,
  end-to-end comparison, live 2&times;2 loop quad, self-check, where to
  next, refs. **Notebook companion also done** &mdash; 24 cells covering
  linear/CNN decoders, PID against dynaphos, end-to-end joint training,
  and a closed-loop demo
  ([modules/decoding-and-closed-loop/decoding-and-closed-loop.ipynb](../modules/decoding-and-closed-loop/decoding-and-closed-loop.ipynb)
  rebuilt via [build/_build_m5_notebook.py](../build/_build_m5_notebook.py)).
  **Verification still owed:** open both in your environment and run
  end-to-end. §05 of the HTML still uses a hand-picked stand-in
  preprocessor &mdash; producing the real `modules/assets/m5_e2e_weights.json`
  is exercise 4.1 in the notebook.

## Don't forget

- **vimplant2** — remember to look at / hook in / mention (context TBD; flag
  to self).

## Lefteris handoff

Nothing pending. As of commit `c341eae`, Lefteris's three items are done:

- Main menu — [modules/index.html](../modules/index.html)
- Harmonized sakura+white palette across all 6 HTMLs (commit `58b42c8`)
- Simplification disclaimer on index + every module page

## Out of scope (for now)

- Web schedule update at <https://www.aanmelder.nl/aimdworkshop2026/bootcamp> —
  waits for content freeze.
- `old/stim-deep-dive.html` is reference-only; do not ship.
