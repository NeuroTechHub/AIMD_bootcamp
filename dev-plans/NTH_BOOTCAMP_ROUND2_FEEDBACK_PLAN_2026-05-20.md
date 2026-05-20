# NTH Bootcamp — Round-2 feedback implementation plan (2026-05-20)

Source: `feedback/FB_Bootcamp_round2.md` — the May 19, 2026 team meeting transcript
plus its "Decisions / Next steps" block. This plan strips logistics (VR goggles,
Wi-Fi, reimbursements, food sponsorship) and captures only the code/content work.

## Ground rules

- **M3** (`modules/neuromod-and-stim.html`) is **generated** by
  `build/_build_bootcamp.py`. All M3 fixes go in the Python generator, then
  `python build/_build_bootcamp.py` to rebuild. The generator also writes
  `bootcamp-plan.html` and the M5 stub.
- **M1 / M2 / M4** are hand-authored HTML — edit directly.
- **M5** decoding loop is excluded (Antonio/Leis own it).
- **Image assets** (M4 simulator face, M4 overview figure) are left to the user:
  mark with a clear `TODO` and do not attempt to author them.
- In-depth `<details>` text is **drafted from published literature with
  citations**; Francesc may later swap in thesis paragraphs.

Module order for navigation: plan → M1 → M2 → M3 → M4 → M5.

---

## A. Cross-cutting — all four modules + generator

### A1. Standardized navigation
- Add a `prev / next` button pair at the **top and bottom** of every module page.
- Make the existing `.pipeline` strip steps **clickable links** to each module
  (currently inert `<div>`s in M1; same pattern in M2/M4 and the generator).
- M3's nav lives in the generator. Keep one shared visual idiom.

### A2. Tools & references + attribution
- Per-module footer block "**Tools & references**" with clickable links:
  - M1 → OpenCV.js, TensorFlow.js + COCO-SSD, YOLO.
  - M2 → DeepGaze III (Kümmerer et al.) — currently used with no attribution.
  - M3 → Ripple/Blackrock stimulation API manual, Shannon 1992, Cogan 2008.
  - M4 → dynaphos (van der Grinten et al., eLife 2024).
- One-line inline tool intro where each tool first appears in the body.
- README: new "**Acknowledgements & references**" section aggregating all of it.

### A3. Notebook reframing
- Convert mid-module "open the notebook" *actions* into an end-of-module
  **reference callout** ("this notebook goes deeper on this topic") — not a task.
- Affects M1, M2, M4, and the generator's M3 / M5 text.

### A4. Self-test integrity re-audit
- Verify M1 and M4 self-check questions are answerable from the page body — no
  concept revealed only inside the answer. (Round 1 fixed M2/M3.)

### A5. Expandable in-depth text + disclaimers
- Wrap deeper explanation in optional `<details>` "in-depth" blocks so pages stay
  skimmable.
- Add explicit "this is the conventional ~90% case; real systems are more
  complex — see references" disclaimers, especially for stim parameters and the
  Shannon limit.

---

## B. M3 generator fixes — `build/_build_bootcamp.py` (then rebuild)

### B1. µC symbol bug
- `renderCumulativeCharge` (lines ~2258–2259) sets `mx.P.textContent` and
  `powerNowEl.textContent` to a string containing the HTML entity `&#xB5;C`.
  `.textContent` renders that literally.
- Fix: use the literal `µ` character (or `.innerHTML`).

### B2. Charge-chart Y-axis
- `renderChargeChart` (line ~2222) recomputes `yMax = qNow * 1.15` every frame,
  so the axis rescales continuously during a run.
- Fix: stable Y-scale — compute predicted end-of-run cumulative charge once at
  stim start, or step `yMax` up only in discrete "nice" increments, so the trace
  visibly climbs instead of staying pinned flat.

### B3. Shannon limit
- Reviewer: "all parameters render as a red dot." Math is correct, but with a
  2000 µm² electrode `k = 2·log10(Q) − log10(A)` pushes most plausible configs
  over 1.85; k=1.85 derives from 1990s macroelectrode/cat data, misapplied to
  microelectrodes.
- Fix: (a) diagnose default + surprise-me parameter ranges, recompute k across
  that space; (b) present k as an informational gauge with nuance, not a binary
  red alarm — keep the check, soften the framing; (c) add references (Shannon
  1992; Cogan 2008; Cogan et al. 2016 tissue-damage thresholds) and a disclaimer
  that microelectrode safety limits are an open area.

### B4. Repetition timing
- Round 1 added `trainPeriodMs = Math.max(iti.value, trainMs)` but clamps to
  *each channel's own* train length, so channels with different train durations
  get different effective periods and drift apart.
- Fix: one **global** train period clamped to the **max train duration across
  all configured channels**; surface the effective value in the UI and log
  (line ~2598 logs the raw unclamped value); warn when the user-set period is
  below it. Guarantees all trains finish before the next repetition.

---

## C. M1 — `modules/computer-vision.html`
- Apply A1–A5. Module is well-liked; mainly navigation, references block,
  notebook reframe, self-check audit.

## D. M2 — `modules/deepgaze-and-gaze.html`
- Apply A1–A5.
- Add DeepGaze tool intro + attribution (its biggest specific gap).

## E. M4 — `modules/phosphene-simulation.html`
- Apply A1–A5.
- Add a **lightweight dynamic-stimulus loop** to the phosphene simulator: a
  drifting/animated stimulus driven through the existing forward model so
  learners see dynamic phosphenes. No video/webcam pipeline.
- Verify the round-1 dynaphos callout credits its source.
- Mark the two image assets (simulator face, overview figure) with a clear
  `TODO` — user swaps in real assets.

## F. README — `README.md`
- Add "Acknowledgements & references" section.
- Refresh module summaries for the new navigation and M4 dynamic stimulus.

---

## G. Verification
1. `python build/_build_bootcamp.py` rebuilds plan + M3 + M5 stub with no warnings.
2. Open all four modules in a browser (no server):
   - µC renders correctly in the M3 cumulative-charge readout and chart.
   - M3 charge-chart Y-axis is stable during a run.
   - M3 Shannon check no longer flags every config.
   - M3 trains stay phase-locked across channels of different lengths.
   - prev/next navigation works top and bottom; pipeline steps are clickable.
   - Tools & references links resolve.
3. Re-read every round-2 next-step + decision; tick each against a change above.

## Status checklist
- [x] A1 navigation (M1, M2, M4, generator) — prev/next top+bottom; clickable pipeline
- [x] A2 tools & references (M1, M2, M4, generator §07, README)
- [x] A3 notebook reframing (M1, M2, M4, generator M3)
- [x] A4 self-test audit (M1 Q4 electrode-count softened; M4 Q4 reworded)
- [x] A5 in-depth text + disclaimers (M4 dynaphos disclaimer; Shannon nuance via B3)
- [x] B1 µC symbol bug (textContent+entity → innerHTML/&micro;)
- [x] B2 charge-chart Y-axis (fixed scale locked at stim start via niceCeil)
- [x] B3 Shannon limit (informational caution framing, amber not red, references)
- [x] B4 repetition timing (global effectiveTrainPeriodMs, clamp warning surfaced)
- [x] E dynamic-stimulus loop (M4 §03 animate-drift via shiftImageX + rAF)
- [x] F README updates (Acknowledgements & references section, summaries)
- [x] G verification + rebuild — generator rebuilds clean; marker checks pass.
      Browser smoke-test still pending (user to eyeball layout/interaction).
