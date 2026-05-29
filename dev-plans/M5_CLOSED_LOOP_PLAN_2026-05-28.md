# M5 — Closed loop & decoding · plan

**Status:** Working draft — 2026-05-28
**Author / lead:** Antonio
**Files:**
- HTML (live playground): [modules/decoding-and-closed-loop.html](../modules/decoding-and-closed-loop.html)
- Notebook (deeper dive): [modules/decoding-and-closed-loop/decoding-and-closed-loop.ipynb](../modules/decoding-and-closed-loop/decoding-and-closed-loop.ipynb)

## One sentence

The loop closes here: a decoder reads phosphene brightness back out, and the
system *uses* that readout to drive the next stim — first with a classical
PID controller on the dynamics, then with an end-to-end network trained
straight through the differentiable dynaphos simulator.

## Style contract — match M3 & M4

- Sakura + white palette (`--ink/--paper/--accent`), Inter + JetBrains Mono.
- Same chrome already in the stub: masthead → disclaimer → `.module-nav` →
  pipeline strip (M5 marked `here`) → numbered TOC → sections → bottom nav →
  footer.
- Per section: `<h2><span class='num'>NN</span>…` + `<p class='kicker'>` +
  optional `<aside class='callout'>` + interactive demo + (where useful)
  `<details class='prompt'>` self-check blocks.
- Each interactive demo gets a "Surprise me" button where it makes sense
  (mirrors M3's idiom).

## Section breakdown

### 01 · The loop in one picture
- Hero diagram (inline SVG, M3 style): camera → CV → gaze → stim → phosphenes
  → decoder → feedback arrow looping back into the preprocessor / stim.
- Kicker: "the loop *closes* when the decoder's output influences the next
  stim — not just the next plot."
- Three short callouts: **what is decoded?** (brightness, letter, scene
  category), **what is fed back?** (current, pulse-width, preprocessing
  weights), **what is the goal?** (track a target, recover an input, or both).
- Section anchor: `#concept`.

### 02 · Read brightness back out
- Smallest possible decoder, so the rest of the module makes sense.
- Interactive: one phosphene, slider for stim current → live dynaphos render
  on the left, decoded brightness on the right.
- Toy "decoder" = mean-pixel readout, then a 1-layer linear regressor fit
  in-browser on a few sample frames.
- Self-check: "shift the current — does the decoder track? where does it
  lag?" (answer: it lags whenever charge accumulation outpaces decay.)
- Anchor: `#read`.

### 03 · PID: control the dynamics
The fun demo. Classical control meets phosphene dynamics.

- Top half: target-brightness trace over time (chooser: step, square, sine,
  ramp). Dashed line = target, solid = achieved, filled = error band.
- Bottom half: three sliders (Kp, Ki, Kd) with micro-labels
  *"react / accumulate / dampen"* and three preset buttons: **P-only**, **PI**,
  **PID**.
- "Surprise me" randomises gains.
- The PID writes back into `stim_current[t+1]`; dynaphos integrates its
  temporal state forward; the decoder reads brightness; repeat.
- Two pre-built self-check prompts:
  - "Crank I to the max — what happens to overshoot? to steady-state error?"
  - "Why does pure P always undershoot for the ramp target?"
- Anchor: `#pid`.

### 04 · Train your own decoder
- TF.js MLP in-browser: tiny network reads a 32×32 phosphene canvas → digit
  (or brightness scalar — start with brightness).
- Synthetic phosphene canvases generated on the fly from random stim configs
  (no dataset download).
- One button: **Train 50 steps**. Loss bar updates live; weights heatmap
  redraws.
- Side-by-side: untrained vs trained predictions on the same fresh canvas.
- Notebook handles the full-fat CNN + real dataset.
- Anchor: `#train`.

### 05 · End-to-end through the simulator
Concept-first; the actual joint training is too heavy for the browser.

- One paragraph + diagram: preprocessor (learnable) → frozen dynaphos →
  decoder (learnable). Gradient flows back through dynaphos because the
  simulator is differentiable.
- Interactive comparison panel:
  - Two phosphene renders side-by-side from the *same* input: one driven by
    hand-tuned Sobel preprocessing, one driven by a precomputed
    end-to-end-trained preprocessor (weights baked in as static JSON).
  - Decoder runs on both; show the recovered image / readout under each.
  - One toggle: "score yourself — which one recovers the input better?"
- Pointer to the notebook for the actual training run.
- Anchor: `#e2e`.

### 06 · The whole loop, live
The climax. 2×2 quad in the style of M3's Conductor.

- TL: input image with gaze crop overlay.
- TR: preprocessed activation mask + per-electrode stim trace.
- BL: phosphene canvas with temporal state (charge accumulation visible).
- BR: decoder readout + PID error trace + target.
- Single **Play / Pause / Reset** row. One toggle: **open loop / closed
  loop** — same input, see the divergence between the two.
- Anchor: `#loop`.

### 07 · Self-check
4–5 `<details class='prompt'>` blocks, matching the M3/M4 idiom. Suggested
prompts:
- Why does open loop drift over time, even with a perfect preprocessor?
- When does PID over-correct, and what does the trace look like?
- After end-to-end training, what does the preprocessor learn that Sobel
  doesn't? (Hint: it cheats — but in a useful way.)
- Which loop ingredient matters most: a better decoder, a better controller,
  or a better preprocessor? (No single right answer; argue from the demos.)

Anchor: `#self-check`.

### 08 · Where to next
- Forward pointer to the notebook (real CNN, real dataset, real metrics).
- Pointer at the workshop's three tracks (experimental / developer / open
  neurotech) and concrete starter prompts for each.
- Anchor: `#next`.

### 09 · Tools & references
- TensorFlow.js (`@tensorflow/tfjs`) — in-browser training.
- dynaphos — van der Grinten et al. 2024, doi:10.7554/eLife.85812.
- End-to-end prosthetic vision — de Ruyter van Steveninck et al. 2022,
  doi:10.1167/jov.22.2.20.
- PID controllers — Åström & Murray, *Feedback Systems*, ch. 10–11
  (open-access book) as the "where to read more" pointer.
- Anchor: `#refs`.

## Implementation notes

- **Reuse from M4:** phosphene rendering math + the dynaphos temporal-state
  loop. Inline copy for now; consider extracting `assets/dynaphos-mini.js`
  later if the duplication starts to hurt.
- **New JS:**
  - PID controller (~30 LoC, plain JS).
  - TF.js MLP wrapper (~80 LoC including the loss-curve plot and the train
    button).
  - 2×2 quad layout (reuse `.cond-*` classes from M3 — already defined in
    the stub's CSS).
- **Section IDs to rename in the stub:**
  - `#concept` → keep
  - `#pretrained` → `#read`
  - `#train` → keep
  - `#e2e` → keep
  - `#closed` → `#loop`
  - `#exercise` → split into `#self-check` + `#next` (drop the standalone
    "Guided exercise" — the demos *are* the exercise)
  - Add `#refs`.
- **Heavy training stays in the notebook.** The HTML is the playground;
  anything that takes longer than ~5 s in-browser belongs in the `.ipynb`.

## Open questions

- PID controls **stim current** (simplest) or **pulse-width** (more
  M3-consistent)? Pick one; mention the other.
- PID is **single-channel** for the demo; **per-channel array PID** is a nice
  stretch goal but probably too busy for the page.
- For section 05, do we ship the end-to-end weights as static JSON in
  `modules/assets/`, or just describe the result? Static JSON is more honest;
  size budget: aim &lt; 200 KB.

## Out of scope

- Real CNN training in browser.
- Real dataset loading (use synthetic phosphene canvases generated on
  demand).
- Per-channel PID array.
- Anything that requires a GPU.
