# Polish plan — NTH Bootcamp HTMLs

Goal: ship a consistent, polished design across all six top-level HTML pages:

- [bootcamp-plan.html](../bootcamp-plan.html) — the landing page (organizers' plan)
- [modules/M1-computer-vision.html](../modules/M1-computer-vision.html)
- [modules/M2-deepgaze-and-gaze.html](../modules/M2-deepgaze-and-gaze.html)
- [modules/M3-neuromod-and-stim.html](../modules/M3-neuromod-and-stim.html)
- [modules/M4-phosphene-simulation.html](../modules/M4-phosphene-simulation.html)
- [modules/M5-decoding-and-closed-loop.html](../modules/M5-decoding-and-closed-loop.html)
- [modules/index.html](../modules/index.html) — the modules-index landing (216 lines, found during audit — must be kept in scope)

Every observation here is **anchored at file:line** so the work can be done as a single mechanical pass.

## Progress

**Round 1 (2026-05-30)** — Quick-wins shortlist + Dim 1 + Dim 11 + Dim 12 (.refs) + Dim 10 partial:

- ✅ Quick-win 1: canonical mn-name "M3 · Stimulation" (was "M3 · Neuromodulation & stim") on M2 top + bottom
- ✅ Quick-win 2: M4 mn-prev "back" → "prev"
- ✅ Quick-win 3: `aside.callout` standardised on all 6 files (`padding:14px 18px; margin:22px 0; font-size:14.5px; max-width:820px`)
- ✅ Quick-win 4: `hr.div{margin:48px 0}` on M1, M2, M4 (was 40/42/42)
- ✅ Quick-win 5: `nav.toc a{border:0}` on M1, M2, M4 (index has no TOC)
- ✅ Dim 1: `font-feature-settings:"ss01","cv11"` added to M1, M2, M4 body rule
- ✅ Dim 1: `::selection` added to M2 and M4 (M1 already had it)
- ✅ Dim 1: `.col{max-width:720px}` added to M1, M2, M4
- ✅ Dim 11: pipeline `aria-label="Bootcamp pipeline"` on all 5 modules (was missing on M1/M2, "Bootcamp pipeline progress" on M3/M4/M5)
- ✅ Dim 12: `.refs` markup standardised to `<section id="refs" class="refs" aria-label="Tools and references">` on all 5 modules (M3 was div, M4 was id="references")
- ✅ Dim 12: `details.prompt` migrated from `?`-glyph to canonical chevron on M2 and M4
- ✅ Dim 10: `footer a{text-decoration:none}` added to M1, M3, M5, plan (M2, M4, index already had it)

**Audit-was-wrong corrections**: every file already had `footer{}` and `@media` declarations — the original audit overstated those gaps. Remaining drift is breakpoint values (680/780/880/900/980) and footer-copy paradigm, both lower priority.

**Round 2 (2026-05-30)** — additional safe edits:

- ✅ Dim 3: M4 `.lab` sidebar 340 → 320 px (matches M2)
- ✅ Dim 7: dropped M5's unused `aside.warn` / `aside.todo` CSS rules
- ✅ Dim 9: added M4 bottom `<nav class="module-nav">` (was missing — only module without one)
- ✅ P2: `<title>NTH Bootcamp - Plan>` → `· Plan` (matches the middle-dot separator used in module titles)

**Round 3 (2026-05-30)** — user-directed:

- ✅ Dim 11: dropped the `<h3 style="margin-top:0">The pipeline at a glance</h3>` heading on all 6 files (M1, M2, M3, M4, M5, index). **Audit-correction:** the original audit claimed M1/M2/M4 had no h3 and M3/M5 did — actually all six had it. The strip now stands on its own at the top of every page.
- ✅ Dim 10: added implementation-note line to M1 and M5 footers, matching the M2/M3/M4 idiom (M1: "OpenCV.js + TF.js (COCO-SSD)…"; M5: "PID controller and TF.js MLP…").
- ✅ Dim 12: **M1 audit-correction.** M1 already has 3 `details.prompt` self-check blocks ([:473-486](../modules/M1-computer-vision.html#L473-L486)) — original audit was wrong (gloss-count was off by one because M1's CSS had no `details.prompt{}` rule of its own, but the prompts were rendering via the global `details` defaults). README claim is correct. No action needed.

**Round 4 (in progress, 2026-05-30)** — CSS extraction:

- ✅ `modules/_shared.css` written (150 lines: tokens + page-shell + nav.toc + asides + pipeline + module-nav + .refs + details.prompt + footer).
- ✅ `modules/M2-deepgaze-and-gaze.html` migrated: dropped from 989 → 892 lines (97 lines moved into shared). Inline `<style>` now only carries M2-specific widget rules (`em.term`, `.lab`, `.diagram`/`.dbox`, `.grid-3`, `.card`, `.hist`, mobile media query).
- ⏳ M1, M3, M4, M5, modules/index.html still inline their CSS. Apply the same pattern (add `<link rel="stylesheet" href="_shared.css">`, keep only file-specific rules inline).
- ⏳ bootcamp-plan.html similar but with `<link rel="stylesheet" href="modules/_shared.css">` and plan-specific scale overrides (h1 38px, h2 24px, h3 14px, kicker 17px, `.page` 64/40/120 padding, h2 56px top, h3 30px top — all in plan's remaining inline `<style>` as last-wins overrides).
- ⏳ `build/_build_bootcamp.py` still emits inline CSS for the plan page and M3. **Before re-running the builder**, factor the builder's inline CSS the same way, otherwise M3 and plan-page will regenerate with the old inline copy and the link will be missing.

Verification step: open each migrated file in a browser after the extraction; confirm fonts/tokens/spacing still match the pre-extraction render.

**Deliberately skipped (low value):**

- Dim 2 small-mono-caption unification — the 11 / 11.5 / 12 px diff maps to distinct semantic roles (caption / spec / sub-title); not actually drift
- Dim 5 inline `<h3 style="margin-top:0">` — single line on two files, factoring to CSS isn't a net win
- Dim 13 responsive breakpoint drift (680/780/880/900/980 px) — every file does have media queries, just at slightly different breakpoints; not worth churning all files for 20 px diff
- P2 inline `style="color:inherit"` on footer links — works correctly under both the explicit and inherited cascade; harmless

---



Items are tagged by priority:

- **[P0]** breaks consistency immediately (visible-at-a-glance harmony killer); must do before polish ships
- **[P1]** noticeable on direct comparison; do in the same pass for full effect
- **[P2]** subtle / nice-to-have; pick up if budget remains

---

## Tier summary

| Tier | Count | Theme |
|---|---|---|
| **P0** | 6 | Canonical idioms (small-caption sizes, module-name copy, details.prompt visual style, .refs markup, responsive fallback, CSS extraction) |
| **P1** | 17 | Token-level alignment of spacing, callouts, footers, font-features, TOC borders, pipeline aria-label/placement, module-nav, refs structure |
| **P2** | 10 | Plan-vs-modules scale parity, token promotion (amber vars), missing self-checks, quoting, minor copy |

See **Tier summary (final)** at end of doc, and **Quick-wins shortlist** for the 5 highest-ROI fixes.

---

## Dimension 1 — Page-shell CSS (root vars, fonts, body)

**Source-of-truth comparison** (first 30 lines of each `<style>` block):

| File | `.page` padding | font-feature-settings | `::selection` | `.col{max-width:720px}` | h1 size | h2 size | h3 size | kicker size | hr.div margin | h2 margin-top |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | `48px 36px 100px` | ✗ | ✓ | ✗ | 34px | 22px | 13px | 16px | 40px | 52px |
| M2 | `48px 36px 100px` | ✗ | ✗ (missing) | ✗ | 34px | 22px | 13px | 16px | 42px | 52px |
| M3 | `48px 36px 100px` | ✓ ss01,cv11 | ✓ | ✓ | 34px | 22px | 13px | 16px | 48px | 52px |
| M4 | `48px 36px 100px` | ✗ | ✗ (missing) | ✗ | 34px | 22px | 13px | 16px | 42px | 52px |
| M5 | `48px 36px 100px` | ✓ ss01,cv11 | ✓ | ✓ | 34px | 22px | 13px | 16px | 48px | 52px |
| plan | `64px 40px 120px` | ✓ ss01,cv11 | ✓ | ✓ | 38px | 24px | 14px | 17px | 48px | 56px |

### Findings

- **[P1]** `font-feature-settings:"ss01","cv11"` is set on M3, M5, plan but missing on M1, M2, M4. Inter's stylistic-set `ss01` swaps `a` for the single-storey form and `cv11` is curved-tail accent — the inconsistency is subtle but readable across pages once you notice it. Refs: [M3:29](../modules/M3-neuromod-and-stim.html#L29), [M5:30](../modules/M5-decoding-and-closed-loop.html#L30), [plan:29](../bootcamp-plan.html#L29) vs. missing in [M1:18-21](../modules/M1-computer-vision.html#L18-L21), [M2:19-22](../modules/M2-deepgaze-and-gaze.html#L19-L22), [M4:52-55](../modules/M4-phosphene-simulation.html#L52-L55). **Fix:** add the same `font-feature-settings` line to M1/M2/M4 body rule.
- **[P1]** `::selection{background:var(--accent-wash);color:var(--ink)}` present on M1/M3/M5/plan but missing on M2 and M4. Refs: [M2:22](../modules/M2-deepgaze-and-gaze.html#L22) (no rule), [M4:55](../modules/M4-phosphene-simulation.html#L55) (no rule). **Fix:** add the same rule.
- **[P1]** `.col{max-width:720px}` defined on M3/M5/plan but missing on M1/M2/M4, even though M3/M5/plan use it to constrain prose-only sections. M1, M2, M4 have no equivalent and their full-width prose runs to ~1108 px on a 1180 px page — too long a measure. Refs: [M3:35](../modules/M3-neuromod-and-stim.html#L35), [M5:36](../modules/M5-decoding-and-closed-loop.html#L36), [plan:35](../bootcamp-plan.html#L35). **Fix:** add `.col` rule to M1/M2/M4, and wrap pure-text paragraphs in `<div class="col">…</div>` where the line length currently exceeds ~95ch.
- **[P1]** `hr.div` vertical rhythm diverges: 40px (M1) → 42px (M2, M4) → 48px (M3, M5, plan). Refs: [M1:39](../modules/M1-computer-vision.html#L39), [M2:42](../modules/M2-deepgaze-and-gaze.html#L42), [M3:55](../modules/M3-neuromod-and-stim.html#L55), [M4:72](../modules/M4-phosphene-simulation.html#L72), [M5:56](../modules/M5-decoding-and-closed-loop.html#L56). **Fix:** unify to **48px** (the value 3 of 6 already share, and which reads best as a section break).
- **[P2]** Plan-page slightly larger scale (h1 38px vs 34px, h2 24px vs 22px, h3 14px vs 13px, kicker 17px vs 16px, `.page` padding 64/40/120 vs 48/36/100): this is *intentional* — the landing page should feel slightly larger and grander than a module. Keep as-is, but document the deliberate scale step in a top-of-file CSS comment.
- **[P2]** Inter weights loaded (400/500/600/700) are identical across all 6 files; JetBrains Mono weights (400/500) identical too. No drift here — confirmed good.

---

## Dimension 2 — Typography (small-text classes for the same role)

The same UX role — *small mono caption directly under a widget panel* — uses **five different selectors and three different font-sizes** across the modules.

| Selector | Where defined | font-size | Use site |
|---|---|---|---|
| `.canvas-wrap .cap` | [M1:92](../modules/M1-computer-vision.html#L92) | 11px | caption below each in-canvas image |
| `.cam-wrap .cap` | [M1:156](../modules/M1-computer-vision.html#L156) | 11px | webcam panel caption (duplicate of above) |
| `.lab .caption` | [M2:80](../modules/M2-deepgaze-and-gaze.html#L80), [M4:100](../modules/M4-phosphene-simulation.html#L100) | 11px | caption below `.lab` widget |
| `.panel .panel-sub` | [M3:72](../modules/M3-neuromod-and-stim.html#L72), [M5:73](../modules/M5-decoding-and-closed-loop.html#L73), [plan:72](../bootcamp-plan.html#L72) | 12px | subtitle in `.panel` |
| `.paintlab .panel .ttl` | [M4:188](../modules/M4-phosphene-simulation.html#L188) | 11px | M4 §05 paintlab panel title |
| `.lab .controls .spec` | [M2:75](../modules/M2-deepgaze-and-gaze.html#L75) | 11.5px | M2 widget-readout chip |
| `.spec` (free) | [M4:148](../modules/M4-phosphene-simulation.html#L148) | 11.5px | M4 spec readout |
| `.paintlab .readout` | [M4:196](../modules/M4-phosphene-simulation.html#L196) | 11.5px | M4 §05 status readout |
| `figure.illust figcaption .cite` | [M1:57](../modules/M1-computer-vision.html#L57) | 12px | image-credit cite below illust |

### Findings

- **[P0]** Three sizes (11 / 11.5 / 12 px) used for *what looks like the same small monospace caption* — visible on screen as inconsistent kerning under widget panels. **Fix:** standardise on **11.5 px** for all small mono "caption / spec / readout / sub-title" roles. Introduce a single CSS class `.mono-cap` (or alias the existing `.caption` for it) and either reskin the five selectors above to inherit the shared rule, or alias-merge them where the markup permits.
- **[P1]** No shared selector for "small caption under a widget" — every module reinvents one. The CSS we already share lives in CSS vars; we should also share at least one utility class for this monospace caption pattern. **Fix:** add `.mono-cap{font-family:'JetBrains Mono',monospace;font-size:11.5px;color:var(--muted);letter-spacing:0.04em}` to all 7 files, then progressively migrate.
- **[P1]** M4 has both a free-floating `.spec` rule [M4:148](../modules/M4-phosphene-simulation.html#L148) **and** the nested `.lab .controls .spec` rule from M2 — confusing scoping. Merge or rename. **Fix:** keep `.spec` as a single global utility scoped from `.lab` upwards; remove the M2 nested duplicate.
- **[P2]** h1 sizing is consistent at 34px on all five modules and `index.html` (good), 38px on `bootcamp-plan.html` (deliberate). h2 / h3 are also consistent across all six modules+index (22/13). Plan-page is 24/14 — deliberate scale step, keep.
- **[P2]** `.refs h2 = 15px; margin-bottom:8px` is identical across every file that has a refs block. Good — no fix.
- **[P2]** Body line-height 1.55 unanimous. Letter-spacing on h1 -0.02em / h2 -0.01em consistent. Keep.

---

## Dimension 3 — Widget panel layout (.lab / .controls / .stage / .twin / .panel)

There are **three coexisting widget-shell idioms** in the repo, none of them shared by all modules.

| Idiom | Defined on | Layout |
|---|---|---|
| **`.lab` two-column** (320–340 px controls + 1fr stage) | M2 [.lab:62](../modules/M2-deepgaze-and-gaze.html#L62), M4 [.lab:81](../modules/M4-phosphene-simulation.html#L81) | grid `<sidebar><stage>` with `.twin` for stage's two side-by-side canvases |
| **`.canvas-row` + `.controls` grid** | M1 [.controls:71](../modules/M1-computer-vision.html#L71), [.canvas-row:90](../modules/M1-computer-vision.html#L90) | `.controls` is `auto-fit minmax(220px,1fr)` row above; `.canvas-row` is a 2-col grid below |
| **`.panel` + `.grid-2 / .grid-3 / .grid-4`** | M3 [:66-75](../modules/M3-neuromod-and-stim.html#L66-L75), M5 [:67-75](../modules/M5-decoding-and-closed-loop.html#L67-L75), plan [:66-75](../bootcamp-plan.html#L66-L75) | independent boxes laid out in a grid; no controls/stage split |

### Findings

- **[P1]** Sidebar width drifts: M2 uses 320px, M4 uses 340px — visible misalignment when reading both pages back-to-back. **Fix:** unify to **320px** (M2's value); M4 is the outlier because of its longer `pitch` slider label.
- **[P2]** The two-column `.lab` and the row-stacked `.canvas-row + .controls` are *both legitimate* (M1's vision pipeline has 2 wide canvases per row + tabbed control bar above; M2/M4 widgets are control-bar-on-left, stage-on-right). Don't unify. **Document the convention** in the CSS file comment so authors choose deliberately.
- **[P1]** `@media (max-width:880px)` mobile fallback only declared in M4 [:156](../modules/M4-phosphene-simulation.html#L156). M2's `.lab` will overflow on mobile because there's no equivalent break. **Fix:** copy M4's mobile rule into M2 (and add to M1's `.controls` / `.canvas-row` if not already responsive — to verify in Dimension 13).
- **[P2]** `.lab .stage` has different vertical-rhythm: M2 has `gap:8px` [:78](../modules/M2-deepgaze-and-gaze.html#L78), M4 has `gap:8px` [:98](../modules/M4-phosphene-simulation.html#L98). Consistent. Good.
- **[P2]** `image-rendering: pixelated` in M4 [.lab canvas:99](../modules/M4-phosphene-simulation.html#L99) — intentional (low-res phosphene grid). M2 `.lab canvas` doesn't have it [:79](../modules/M2-deepgaze-and-gaze.html#L79). Keep both — the difference is content-driven.

---

## Dimension 4 — Spacing rhythm

Vertical-rhythm constants (a smaller table to spot the drift fast):

| Rule | M1 | M2 | M3 | M4 | M5 | plan | index |
|---|---|---|---|---|---|---|---|
| `.page` top-padding | 48px | 48px | 48px | 48px | 48px | 64px | 48px |
| `.page` bottom-padding | 100px | 100px | 100px | 100px | 100px | 120px | 100px |
| `header.masthead` margin-bottom | 32px | 32px | 32px | 32px | 32px | 40px | 32px |
| `h2` margin-top | 52px | 52px | 52px | 52px | 52px | 56px | 52px |
| `h3` margin-top | 24px | 24px | 24px | 24px | 24px | 30px | 24px |
| `hr.div` margin | 40px | 42px | 48px | 42px | 48px | 48px | – |
| `aside.callout` margin | 20px | 18px | 22px | 18px | 22px | 22px | – |

### Findings

- **[P1]** Modules are mostly aligned on 48/52/24/32 cadence, but `hr.div` and `aside.callout` margins jitter (40/42/48 px and 18/20/22 px). The plan-page is the cleaner outlier (48 hr, 22 callout). **Fix:** unify the five modules + index on **hr.div=48px** and **aside.callout=22px 0** (matches M3, M5, plan). The 2-4 px diffs read as a visible "step" when paging M1 → M2 → M3.
- **[P2]** Plan-page's larger spacing (64/40/120 page-padding, 56 h2-top) is the *intentional grandeur step* — keep, but document.
- **[P2]** Per-section internal padding inside widgets is fine — varies per widget legitimately (M3 stim panels, M4 paint lab, M2 lab, M1 canvas-row).

---

## Dimension 5 — Section number badges (.num) and h2 layout

`h2 .num` defined identically as `color:var(--muted-2);font-variant-numeric:tabular-nums;margin-right:12px;font-weight:500` on every modules file; **14px on plan** (margin-right:14px). All section headers use `<h2><span class="num">NN</span>Title</h2>` with zero-padded two-digit numbers.

Counts of section badges per file (`<h2><span class='num'>` occurrences):

| File | Sections (`.num` h2s) |
|---|---|
| index | 1 |
| M1 | 6 |
| M2 | 8 |
| M3 | 7 |
| M4 | 8 |
| M5 | 8 |
| plan | 10 |

### Findings

- **[P2]** Section count diverges (M1=6, M3=7, others=8) — *legitimate* differences in content depth. No fix needed.
- **[P2]** `.num` styling is uniform across all 7 files (margin-right and color identical, only plan steps up to margin-right:14 to match its larger h2). Good.
- **[P2]** The numbering is always 2-digit zero-padded (`01`, `02`, …) — uniform.
- **[P1]** M5's bottom-of-page `<h3 style="margin-top:0">The pipeline at a glance</h3>` ([M5:693](../modules/M5-decoding-and-closed-loop.html#L693)) and M3's identical line ([M3:692](../modules/M3-neuromod-and-stim.html#L692)) use **inline style** `margin-top:0` — should move into the shared CSS. The other modules either don't show a pipeline at the bottom or do but the h3 differs.

---

## Dimension 6 — TOC structure

`nav.toc` CSS identical across all five module files; plan uses 18px padding (vs 16px).

### Findings

- **[P1]** `nav.toc a` rule missing `border:0` on M1 [:203](../modules/M1-computer-vision.html#L203), M2 [:57](../modules/M2-deepgaze-and-gaze.html#L57), M4 [:76](../modules/M4-phosphene-simulation.html#L76), index [:62](../modules/index.html#L62) — meaning the global `a{…border-bottom:1px solid var(--rule)}` rule **adds an unwanted underline** under each TOC entry on those pages. **Fix:** add `border:0` (or `border-bottom:0`) to `nav.toc a` on those four files. M3 [:61](../modules/M3-neuromod-and-stim.html#L61) and M5 [:62](../modules/M5-decoding-and-closed-loop.html#L62) and plan [:61](../bootcamp-plan.html#L61) already do this correctly.
- **[P1]** TOC `padding:16px 0` on M1/M2/M3/M4/M5/index; plan steps to 18px to match its larger scale step — keep. No fix.
- **[P2]** M3 [:695](../modules/M3-neuromod-and-stim.html#L695) and M5 [:696](../modules/M5-decoding-and-closed-loop.html#L696) ship the TOC as **two different markup styles** (M3 inline, M5 one-link-per-line). Functionally identical. Pick one. **Fix:** prefer M5's per-line markup (more diff-friendly).
- **[P2]** All TOCs use `aria-label='Sections'`. Consistent. Good.

---

## Dimension 7 — Callouts and asides

| Selector | M1 | M2 | M3 | M4 | M5 | plan | index |
|---|---|---|---|---|---|---|---|
| `aside.callout` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| `aside.warn` (red) | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ |
| `aside.todo` (muted) | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ |
| `aside.disclaimer` (amber) | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |

### Findings

- **[P1]** `aside.callout` font-size and padding drifts: **14.5px / 14px / 12px or 14px padding / 18px or 16px padding / 22px or 20px or 18px margin** depending on file (see Dimension 4). **Fix:** standardise on the M3-M5-plan canonical: `padding:14px 18px; margin:22px 0; font-size:14.5px; max-width:820px`.
- **[P1]** `aside.warn` and `aside.todo` are defined but **only used** on M3 and plan. M5 defines them but doesn't use them — dead CSS rules. **Fix:** if no warn/todo content is planned for M5, drop those rules; else inventory the missing call-sites.
- **[P1]** `aside.disclaimer` is **defined and used on 6 of 7** files (everywhere except plan-page). Six near-duplicate rule blocks. **Fix:** factor `aside.disclaimer` to a single rule and consider keeping a copy on plan for parity (or formally exempt the plan page in the rule's CSS comment).
- **[P2]** Color tokens for warn (`--danger:#8a3a1d`, `#faf2ee` background) and todo (`--muted-2` border) are derived from the shared root vars. Good — no hard-coded colors except the amber disclaimer trio (`#c89a3a`, `#fbf3df`, `#5a4513`). Consider promoting amber to root vars (`--warn:#c89a3a; --warn-bg:#fbf3df; --warn-ink:#5a4513`).

---

## Dimension 8 — Widget panel layout (recap from Dim 3)

Already audited (see Dimension 3). Net items: unify M2/M4 `.lab` sidebar width at 320px; copy M4's `@media (max-width:880px)` rule into M2; merge `.spec` duplicates on M4.

---

## Dimension 9 — Module-nav bars (top + bottom)

Every module HTML has a top `.module-nav` directly under the masthead and a bottom one above the footer. CSS is identical across all five modules (`.module-nav` and `.mn-*` rules byte-equal: ref [M3:117-126](../modules/M3-neuromod-and-stim.html#L117-L126)).

### Findings — copy drift

| Module | mn-prev label text | mn-next label text |
|---|---|---|
| M1 | "← back" + "Modules" | "next →" + "M2 · Gaze & DeepGaze" |
| M2 | "← prev" + "M1 · Computer vision" | "next →" + "M3 · Neuromodulation & stim" |
| M3 | "← prev" + "M2 · Gaze & DeepGaze" | "next →" + "M4 · Phosphenes" |
| M4 | "← back" + "M3 · Stimulation" | "next →" + "M5 · Decoding" |
| M5 | "← prev" + "M4 · Phosphenes" | "next →" + "Modules" |

- **[P0]** **"back" vs "prev"** mixed: M1 and M4 say *back*, M2/M3/M5 say *prev*. M1's "back" is semantically meaningful (going up to the index, not sideways), but **M4 uses "back" to go to M3** — a sideways move that should be "prev". **Fix:** rename M4 [:244](../modules/M4-phosphene-simulation.html#L244) to "prev". Keep M1 "back" → index and M5 "next → Modules" (both up-the-tree moves are fine as is).
- **[P0]** **Module display-name drift in nav copy**:
  - M3's mn-next reads `M4 · Phosphenes`; M5's mn-prev reads `M4 · Phosphenes`; but M4's title is `M4 · Phosphene simulation` — shortened in nav.
  - M2's mn-next reads `M3 · Neuromodulation & stim`; M4's mn-prev reads `M3 · Stimulation`; M3's title is `M3 · Neuromodulation & stimulation` — two different abbreviations.
  - M5's mn-prev says `M4 · Phosphenes` (matches the pipeline `.name`).
  **Fix:** define a single canonical short name per module and use it everywhere:
  - M1 = `Computer vision` (or `CV`)
  - M2 = `Gaze & DeepGaze`
  - M3 = `Stimulation` (per pipeline)
  - M4 = `Phosphenes` (per pipeline)
  - M5 = `Decoding` (per pipeline)
  Then update mn-name and pipeline `.name` to match.
- **[P1]** Top-of-page module-nav present on all five modules. Bottom-of-page module-nav present on all five. The duplication is intentional (prev/next at both ends of long pages). Keep, but ensure the **text matches byte-for-byte** between top and bottom on the same page (currently does, but easy to drift).

---

## Dimension 10 — Footers

Every module HTML ends with a `<footer>` styled via the shared rule (defined locally per file). The Neurolight citation was just added consistently across all five module footers. Plan and index footers don't carry the citation.

### Findings

- **[P1]** `footer{}` style is defined separately in every file. M4 explicitly declares `footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--rule);font-size:12px;color:var(--muted);font-family:'JetBrains Mono',monospace}` at [M4:151-154](../modules/M4-phosphene-simulation.html#L151-L154). M1/M2/M3/M5/plan/index have **no explicit `<footer>` rule** in CSS — relying on default styling + inline ` style="color:inherit"` in the link. Visible regression: M4 footer is rendered in monospace 12px muted; the others fall back to body styling (Inter 16px, ink-2). **Fix:** lift M4's `<footer>` rule to all 7 files (and review where else style="..." is inlined to be replaced).
- **[P1]** Footer copy contents diverge:
  - M1 footer: `NTH bootcamp · M1 · next: M2 → · Pipeline foundation: …`
  - M2 footer: `NTH bootcamp · M2 · next: M3 → · demos on this page use a synthetic scene… · Pipeline foundation: …`
  - M3 footer: `NTH bootcamp · M3 · next: M4 → · safety helpers implemented in vanilla JS below, no Python required. · Pipeline foundation: …`
  - M4 footer: `NTH bootcamp · M4 · all physics implemented in ~400 lines of vanilla JS below. Built against dynaphos 0.1.3 (…) · Pipeline foundation: …`
  - M5 footer: `NTH bootcamp · M5 · back to modules → · Pipeline foundation: …`
  Mixed paradigms: M1/M5 brief, M2/M3/M4 include implementation notes. **Fix:** pick one model. Recommend: keep the implementation note (it's useful for code-reading users) on **all** modules — short one-line each.
- **[P2]** `· back to modules →` and `· next: M2 →` are duplicating the bottom `.module-nav` info that sits directly above the footer. Consider dropping the link from the footer text entirely, since the module-nav above already serves that role.

---

## Dimension 11 — Pipeline strip

CSS is identical across all 7 files. Markup divergence:

| File | aria-label | `step active` here label | `step active` name |
|---|---|---|---|
| M1 [:257](../modules/M1-computer-vision.html#L257) | *(none)* | `M1 · here` | `Camera + CV` |
| M2 [:192](../modules/M2-deepgaze-and-gaze.html#L192) | *(none)* | `M2 · here` | `Gaze` |
| M3 [:693](../modules/M3-neuromod-and-stim.html#L693) | `Bootcamp pipeline progress` | `M3 · here` | `Stimulation` |
| M4 [:249](../modules/M4-phosphene-simulation.html#L249) | `Bootcamp pipeline progress` | `M4 · here` | `Phosphenes` |
| M5 [:694](../modules/M5-decoding-and-closed-loop.html#L694) | `Bootcamp pipeline progress` | `M5 · here` | `Decoding` |
| index [:141](../modules/index.html#L141) | `Bootcamp pipeline` | *(none)* | – |

### Findings

- **[P1]** Aria-label inconsistency (`Bootcamp pipeline progress` × 3, `Bootcamp pipeline` × 1, *none* × 2). **Fix:** standardise on `aria-label="Bootcamp pipeline"` everywhere (the "progress" suffix is misleading on a static link strip).
- **[P1]** **Pipeline placement diverges**:
  - M3 and M5 put the pipeline-strip *below* the module-nav, prefixed by an `<h3>The pipeline at a glance</h3>` ([M3:692](../modules/M3-neuromod-and-stim.html#L692), [M5:693](../modules/M5-decoding-and-closed-loop.html#L693)).
  - M1, M2, M4 put it *above* the TOC near the top, with no preceding h3.
  - index uses it as the hero element with no preceding h3.
  **Fix:** pick one placement convention. Recommend: top-of-page (M1/M2/M4 style), drop the `<h3>` introductory heading, and let the strip stand on its own. Update M3/M5 to match.
- **[P2]** `step.name` text for M3 is `Stimulation` in M5's strip and M3's own here-marker — consistent. M3's M3-mn-next in other files reads `Phosphenes`. Need to align with the canonical short-name table from Dimension 9.

---

## Dimension 12 — Self-check (`details.prompt`) + Tools-and-references (`.refs`) blocks

**`details.prompt`** CSS is **two different visual designs**:
- M2/M4 use the `?` / `✓` glyph idiom (defined at [M2:101-105](../modules/M2-deepgaze-and-gaze.html#L101-L105), [M4:143-145](../modules/M4-phosphene-simulation.html#L143-L145))
- M3/M5/plan use a CSS-only triangle/chevron idiom (defined at [M3:147-156](../modules/M3-neuromod-and-stim.html#L147-L156), [M5:147-156](../modules/M5-decoding-and-closed-loop.html#L147-L156), [plan:138-152](../bootcamp-plan.html#L138-L152))
- M1 has **no `details.prompt`** declared at all (uses regular `details` if any)

**`.refs`** markup divergence:

| File | Element | id | aria-label |
|---|---|---|---|
| M1 [:500](../modules/M1-computer-vision.html#L500) | `<section class="refs">` | *(none)* | `Tools and references` |
| M2 [:599](../modules/M2-deepgaze-and-gaze.html#L599) | `<section class="refs">` | *(none)* | `Tools and references` |
| M3 [:2622](../modules/M3-neuromod-and-stim.html#L2622) | `<div class="refs">` | *(none)* | *(none)* |
| M4 [:929](../modules/M4-phosphene-simulation.html#L929) | `<section class="refs">` | `references` | *(none)* |
| M5 [:2751](../modules/M5-decoding-and-closed-loop.html#L2751) | `<section class="refs">` | `refs` | *(none)* |

### Findings

- **[P0]** **Two visual designs for `details.prompt`**: the `?` glyph (M2, M4) vs the chevron (M3, M5, plan). Direct A/B comparison across pages shows a clear style break. **Fix:** pick one. Recommend the **chevron** (M3/M5/plan) — it's more conventional, the `?` looks like a placeholder. Migrate M2 and M4 to the chevron rule, then drop their old rules.
- **[P1]** M1 has **no self-check blocks** despite the README claiming one. **Fix:** either author 3-4 self-check prompts for M1, or update README to reflect M1's omission.
- **[P0]** **`.refs` block markup is inconsistent across 5 files**: element (`section` vs `div`), id (`#refs` vs `#references` vs none), aria-label (set on M1/M2 only). **Fix:** standardise on `<section id="refs" class="refs" aria-label="Tools and references">` everywhere.
- **[P1]** `.refs h2{font-size:15px}` consistent — good.
- **[P2]** Refs block ordering: M4 carries a longer, multi-h3 reference block (Pipeline foundation, Simulator, Cortex model, Temporal dynamics, Clinical evidence) — that's the canonical model for refs sections. Smaller modules should match the structure where applicable.

---

## Dimension 13 — Image / figure / canvas sizing + responsive behavior

### Findings

- **[P0]** `@media (max-width:880px)` only declared on M4 ([:155-158](../modules/M4-phosphene-simulation.html#L155-L158) and [:198](../modules/M4-phosphene-simulation.html#L198) for paintlab). M2's `.lab` will collapse-overflow on narrow screens because no media query rewrites its `grid-template-columns:320px 1fr` to a single column. M1's `.canvas-row{grid-template-columns:repeat(2,1fr)}` ([M1:90](../modules/M1-computer-vision.html#L90)) also lacks a small-screen fallback. **Fix:** add a shared mobile-fallback CSS block to M1, M2 (and probably M3, M5 for grid-2/-3/-4) at the same breakpoint.
- **[P1]** `figure.illust` (image + figcaption + cite) is only defined on M1 [:54-59](../modules/M1-computer-vision.html#L54-L59). M4 carries large embedded figures (cortex panels, phosphene canvases) inline in `<canvas>` without a shared figure idiom. Modules that have static images (M2 saliency demos, M4 cortex model) would benefit from sharing `figure.illust`. **Fix:** move `figure.illust` to a shared block; document its expected use.
- **[P2]** Canvas `image-rendering:pixelated` used on M4 `.lab canvas` and `.paintlab .panel canvas` (intentionally low-res phosphene grid). M2's `.lab canvas` doesn't have it (DeepGaze viz is smooth). Keep both; content-driven.
- **[P2]** Image sizing for `figure.illust img` is `max-width:780px` — fits inside `.col` line length (720px) plus margin. Reasonable. Keep.

---

## Dimension 14 — Cross-cutting items not covered above

- **[P0]** Five `<style>` blocks duplicate 80%+ of the same root-vars and reset code (same Inter + JetBrains Mono import, same `:root` vars, same body rule). 6 files × ~150 lines of shared CSS = ~900 lines of pure duplication. **Fix (not P0 design-wise but P0 for maintainability):** extract to a single `modules/_shared.css` and `<link rel="stylesheet" href="_shared.css">` in each file. The bootcamp-plan and index reference it with `../` adjustments.
- **[P1]** `<title>` text on plan-page is `NTH Bootcamp - Plan` ([plan:6](../bootcamp-plan.html#L6)) — uses ASCII `-` while every module title uses `·` (middle dot). **Fix:** rename to `NTH Bootcamp · Plan`.
- **[P1]** Inline `style="..."` attributes appear in several places: e.g. the `<h3 style="margin-top:0">` repeat on M3, M5 (Dim 5), `<a style="color:inherit">` in every footer's Neurolight citation. **Fix:** factor to shared rules — `.refs a{color:inherit}` and `footer .pipeline-h3{margin-top:0}`.
- **[P2]** Quote-style mixed: M3, M5, plan use `'single quotes'` for HTML attributes; M1, M2, M4 use `"double quotes"`. Cosmetic; not user-visible. Skip unless the build tool normalizes.

---

## Quick-wins shortlist (Recommended order of operations)

If you only do five things, do these — they take ~30 minutes total and remove the most visible inconsistency:

1. **Unify module display names everywhere** (Dim 9) — pick `M1 · CV`, `M2 · Gaze & DeepGaze`, `M3 · Stimulation`, `M4 · Phosphenes`, `M5 · Decoding`; sed-replace across all mn-name and pipeline `.name` strings.
2. **Fix M4's "back" → "prev"** (Dim 9), single token swap at [M4:244](../modules/M4-phosphene-simulation.html#L244).
3. **Standardise `aside.callout`** to `padding:14px 18px; margin:22px 0; font-size:14.5px; max-width:820px` everywhere (Dim 7).
4. **Standardise `hr.div` to `margin:48px 0`** everywhere (Dim 4).
5. **Add `border:0` to `nav.toc a`** on M1, M2, M4, index (Dim 6).

## Tier summary (final)

| Tier | Approximate item count | Theme |
|---|---|---|
| **P0** | 6 | Pick canonical idiom and apply: small-caption sizes (Dim 2); module-name copy + "back/prev" (Dim 9); details.prompt visual style (Dim 12); `.refs` markup (Dim 12); responsive fallback (Dim 13); CSS extraction for maintainability (Dim 14). |
| **P1** | 17 | Token-level alignment of spacing, callouts, footers, font-features, TOC borders, pipeline aria-label/placement, module-nav consistency, refs structure. |
| **P2** | 10 | Subtle scale-step parity (plan vs modules), token promotion (amber vars), self-check authoring, quoting consistency, minor copy. |

**Total auditable items: ~33** across 14 design dimensions.

## Out of scope

This plan does not cover:
- Content / copy rewrites beyond label normalization
- New widget interaction patterns
- Notebook (`.ipynb`) styling
- Build-script (`build/_build_bootcamp.py`) consolidation, except where it can replace the duplicated CSS heads

---

*Next concrete action when polish work begins: create `modules/_shared.css` with the canonical tokens (Dim 14 + Dim 4), then apply the Quick-wins list as a single PR.*

