"""Build the NTH bootcamp plan and per-module stubs.

Style follows the Neurolight2 stim-deep-dive reference (kept locally in
`old/stim-deep-dive.html`, gitignored) so the family of documents reads
consistently.
"""
from __future__ import annotations

import html
from pathlib import Path
from textwrap import dedent

# Generator lives in <root>/build/; writes one level up into <root>/ and <root>/modules/.
BOOTCAMP_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BOOTCAMP_DIR / "modules"


# --- shared CSS -------------------------------------------------------------

SHARED_CSS = dedent("""
  :root{
    --ink:        #1c1c1a;
    --ink-2:      #3a3a36;
    --muted:      #6c6c66;
    --muted-2:    #9a9a93;
    --rule:       #d8d6cf;
    --rule-2:     #ebe9e2;
    --paper:      #ffffff;
    --paper-2:    #f8f8f6;
    --accent:     #d86f91;
    --accent-2:   #a83f63;
    --accent-wash:#fde7ef;
    --danger:     #8a3a1d;
    --code-bg:    #f7f7f4;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:var(--paper);color:var(--ink);
    font-family:'Inter',system-ui,-apple-system,Segoe UI,sans-serif;
    font-feature-settings:"ss01","cv11";
    -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
    font-size:16px;line-height:1.55}
  ::selection{background:var(--accent-wash);color:var(--ink)}

  .page{max-width:1180px;margin:0 auto;padding:64px 40px 120px}
  .col{max-width:720px}
  header.masthead{border-bottom:1px solid var(--rule);padding-bottom:32px;margin-bottom:40px}
  header.masthead .eyebrow{font-size:12px;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted);
    font-weight:500}
  header.masthead h1{font-size:38px;font-weight:600;letter-spacing:-0.02em;line-height:1.1;margin:14px 0 16px}
  header.masthead p.lede{color:var(--ink-2);font-size:17px;max-width:760px;margin:0}
  header.masthead .meta{display:flex;gap:24px;flex-wrap:wrap;margin-top:24px;font-size:13px;color:var(--muted);
    font-family:'JetBrains Mono',ui-monospace,monospace}
  header.masthead .meta strong{color:var(--ink);font-weight:600}

  h2{font-size:24px;font-weight:600;letter-spacing:-0.01em;margin:56px 0 14px;color:var(--ink)}
  h2 .num{color:var(--muted-2);font-variant-numeric:tabular-nums;margin-right:14px;font-weight:500}
  h3{font-size:14px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;color:var(--muted);
    margin:30px 0 10px}
  p{margin:0 0 14px;color:var(--ink-2)}
  p.kicker{color:var(--ink);font-size:17px;margin-bottom:16px}
  a{color:var(--accent-2);text-decoration:none;border-bottom:1px solid var(--rule)}
  a:hover{color:var(--accent);border-bottom-color:var(--accent)}
  code,.mono{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:0.92em}
  code{background:var(--code-bg);padding:1px 5px;border-radius:3px;color:var(--ink)}
  hr.div{border:0;border-top:1px solid var(--rule);margin:48px 0}
  ul.tight{margin:8px 0;padding-left:22px}
  ul.tight li{margin:3px 0;color:var(--ink-2)}

  nav.toc{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--rule);
    border-bottom:1px solid var(--rule);padding:18px 0;margin-bottom:40px}
  nav.toc a{padding:4px 18px 4px 0;border:0;font-family:'JetBrains Mono',monospace;font-size:12px;
    color:var(--muted);letter-spacing:0.02em;display:flex;align-items:baseline;gap:8px}
  nav.toc a:hover{color:var(--accent)}
  nav.toc a .n{color:var(--muted-2);font-variant-numeric:tabular-nums}

  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0}
  .grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0}
  .grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}
  .panel{border:1px solid var(--rule);background:#fff;border-radius:6px;padding:18px}
  .panel h4{margin:0 0 6px;font-size:13px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;
    color:var(--ink)}
  .panel .panel-sub{font-size:12px;color:var(--muted);font-family:'JetBrains Mono',monospace;margin-bottom:12px}
  .panel ul.tight{margin:6px 0 0}
  .panel ul.tight li{font-size:13.5px}

  table.t{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.5px}
  table.t th{text-align:left;font-weight:600;padding:10px 14px;border-bottom:1px solid var(--ink);
    color:var(--ink);font-size:12px;text-transform:uppercase;letter-spacing:0.05em}
  table.t td{padding:10px 14px;border-bottom:1px solid var(--rule-2);color:var(--ink-2);vertical-align:top}
  table.t tr:hover td{background:var(--paper-2)}
  table.t td.mono,table.t td .mono{font-family:'JetBrains Mono',monospace;color:var(--ink)}
  table.t td.time{font-family:'JetBrains Mono',monospace;color:var(--ink);white-space:nowrap}

  aside.callout{border-left:3px solid var(--accent);background:var(--paper-2);
    padding:14px 18px;margin:22px 0;font-size:14.5px;color:var(--ink-2);border-radius:0 4px 4px 0;max-width:820px}
  aside.callout strong{color:var(--ink)}
  aside.warn{border-left-color:var(--danger);background:#faf2ee}
  aside.warn strong{color:var(--danger)}
  aside.todo{border-left-color:var(--muted-2);background:#fff}
  aside.todo strong{color:var(--ink)}

  /* pipeline strip at the top of every module page */
  .pipeline{display:flex;align-items:stretch;gap:0;margin:0 0 28px;flex-wrap:wrap;
    max-width:920px}
  .pipeline .step{flex:1 1 0;min-width:120px;background:#fff;border:1px solid var(--rule);
    padding:10px 12px;border-radius:5px;font-size:13px;color:var(--ink-2)}
  .pipeline .step .lbl{font-family:'JetBrains Mono',monospace;font-size:10px;
    color:var(--muted);text-transform:uppercase;letter-spacing:0.06em}
  .pipeline .step .name{color:var(--ink);font-weight:600;margin-top:2px}
  .pipeline .arr{display:flex;align-items:center;justify-content:center;width:20px;
    color:var(--muted-2);font-family:'JetBrains Mono',monospace}
  .pipeline .step.active{border-color:var(--accent);background:var(--accent-wash)}
  .pipeline .step.active .lbl{color:var(--accent-2)}
  a.step{text-decoration:none;color:inherit;transition:border-color .15s}
  a.step:hover{border-color:var(--accent)}
  a.step:hover .name{color:var(--accent)}

  /* module navigation (prev / next) */
  .module-nav{display:flex;gap:12px;margin:0 0 24px;flex-wrap:wrap}
  .module-nav a{display:flex;flex-direction:column;gap:2px;padding:10px 16px;
    border:1px solid var(--rule);border-radius:6px;background:#fff;text-decoration:none;
    font-family:'JetBrains Mono',monospace;transition:border-color .15s}
  .module-nav a:hover{border-color:var(--accent)}
  .module-nav .mn-dir{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted-2)}
  .module-nav .mn-name{font-size:13px;color:var(--ink)}
  .module-nav a:hover .mn-name{color:var(--accent)}
  .module-nav .mn-next{margin-left:auto;text-align:right}

  /* tools & references block */
  .refs{margin-top:40px;font-size:13px}
  .refs h2{font-size:15px;margin-bottom:8px}
  .refs ul{list-style:none;padding:0;margin:0}
  .refs li{padding:6px 0;border-bottom:1px solid var(--rule-2);line-height:1.5}
  .refs li:last-child{border-bottom:none}
  .refs .rk{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);
    text-transform:uppercase;letter-spacing:.05em}

  /* numbered self-check prompts (Lefteris idiom) */
  details.prompt{background:#fff;border:1px solid var(--rule);border-radius:5px;
    padding:10px 14px 10px 14px;margin:8px 0;max-width:820px}
  details.prompt summary{cursor:pointer;font-weight:500;color:var(--ink);
    font-size:14px;line-height:1.45;list-style:none;
    display:flex;align-items:flex-start;gap:10px}
  details.prompt summary::-webkit-details-marker{display:none}
  details.prompt summary::marker{content:''}
  /* CSS-only chevron: right-pointing triangle from borders.
     Rotates 90deg around its own centre when [open] toggles. */
  details.prompt summary::before{
    content:'';flex:0 0 auto;display:inline-block;
    width:0;height:0;
    margin-top:6px;
    border-style:solid;
    border-width:5px 0 5px 7px;
    border-color:transparent transparent transparent var(--muted-2);
    transition:transform 0.15s ease, border-left-color 0.15s ease;
    transform-origin:2px center;
  }
  details.prompt[open] summary::before{
    transform:rotate(90deg);
    border-left-color:var(--accent);
  }
  details.prompt summary:hover::before{border-left-color:var(--accent)}
  details.prompt p{margin:8px 0 0;font-size:13.5px;color:var(--ink-2);line-height:1.55}
  details.prompt code{font-family:'JetBrains Mono',monospace;background:var(--code-bg);
    padding:1px 5px;border-radius:3px;font-size:0.92em;color:var(--ink)}

  .readout{display:inline-block;background:var(--ink);color:var(--paper);
    font-family:'JetBrains Mono',monospace;font-size:11px;padding:2px 7px;border-radius:3px;
    letter-spacing:0.01em}
  .readout.accent{background:var(--accent);color:#1c1c1a}
  .readout.muted{background:var(--muted-2);color:#1c1c1a}

  .role{display:inline-flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;
    font-size:11px;padding:3px 8px;border-radius:3px;background:var(--accent-wash);color:var(--accent-2);
    letter-spacing:0.02em;border:1px solid var(--rule)}
  .role.dual{background:#fff}
  .role.org{background:var(--paper-2);color:var(--muted)}

  /* --- module-specific: utah array demo ---------------------------- */
  .array-demo{border:1px solid var(--rule);background:#fff;border-radius:6px;
    padding:0;margin:24px 0;overflow:hidden}
  .array-body{display:grid;grid-template-columns:minmax(300px,1fr) minmax(340px,1.35fr) minmax(280px,1fr);
    gap:0;align-items:stretch}
  .array-body > div{padding:18px}
  .array-body > div + div{border-left:1px solid var(--rule)}
  .array-panel-h{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);
    letter-spacing:0.05em;text-transform:uppercase;margin:0 0 10px;
    display:flex;align-items:center;gap:8px}
  .array-svg-wrap{background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;
    padding:10px;position:relative;user-select:none}
  .array-svg-wrap svg{width:100%;height:auto;display:block;cursor:crosshair}
  .array-actions{margin-top:10px;display:flex;gap:6px;flex-wrap:wrap}
  .array-actions button{appearance:none;border:1px solid var(--rule);background:#fff;
    font:inherit;font-family:'JetBrains Mono',monospace;font-size:11px;
    letter-spacing:0.04em;text-transform:uppercase;padding:6px 10px;border-radius:4px;
    cursor:pointer;color:var(--ink)}
  .array-actions button:hover{border-color:var(--accent);color:var(--accent-2)}
  .array-actions button.primary{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .array-actions button.primary:hover{background:var(--accent-2);border-color:var(--accent-2);color:#fff}
  .array-actions .sel-count{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:11px;color:var(--muted);align-self:center;font-variant-numeric:tabular-nums}
  .array-params{display:grid;grid-template-columns:max-content 1fr max-content;
    gap:8px 12px;align-items:center}
  .array-params label{font-family:'JetBrains Mono',monospace;font-size:11.5px;
    color:var(--muted);white-space:nowrap}
  .array-params .v{font-family:'JetBrains Mono',monospace;font-size:11.5px;
    color:var(--ink);font-variant-numeric:tabular-nums;text-align:right;min-width:80px}
  .array-params input[type=range]{appearance:none;background:transparent;
    height:18px;width:100%;cursor:pointer;margin:0;padding:0}
  .array-params input[type=range]:focus{outline:none}
  .array-params input[type=range]:focus-visible{outline:2px solid var(--accent);
    outline-offset:2px;border-radius:3px}
  .array-params input[type=range]::-webkit-slider-runnable-track{height:2px;
    background:var(--rule);border-radius:1px}
  .array-params input[type=range]::-webkit-slider-thumb{appearance:none;
    height:12px;width:12px;background:var(--accent);border-radius:50%;
    margin-top:-5px;border:0}
  .array-params input[type=range]::-moz-range-track{height:2px;
    background:var(--rule);border-radius:1px}
  .array-params input[type=range]::-moz-range-thumb{height:12px;width:12px;
    background:var(--accent);border-radius:50%;border:0}
  .ad-live-tag{display:inline-block;margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:10px;letter-spacing:0.04em;
    color:var(--muted);background:transparent;padding:2px 8px;border-radius:3px;
    border:1px solid var(--rule);font-weight:500;text-transform:lowercase}
  .ad-live-tag.hot{color:var(--accent-2);background:var(--accent-wash);
    border-color:var(--accent)}
  .ad-preview{background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;
    padding:8px 10px;margin:0 0 14px}
  .ad-preview svg{width:100%;height:auto;display:block}
  .ad-commit{display:flex;align-items:center;gap:10px;margin-top:14px}
  .ad-commit button{appearance:none;border:1px solid var(--rule);background:#fff;
    font:inherit;font-family:'JetBrains Mono',monospace;font-size:11.5px;
    letter-spacing:0.04em;text-transform:uppercase;padding:8px 14px;border-radius:4px;
    cursor:pointer;color:var(--ink);font-weight:500}
  .ad-commit button:hover:not(:disabled){border-color:var(--accent);color:var(--accent-2)}
  .ad-commit button.primary{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .ad-commit button.primary:hover:not(:disabled){background:var(--accent-2);
    border-color:var(--accent-2);color:#fff}
  .ad-commit button:disabled{opacity:0.4;cursor:not-allowed}
  .ad-commit button.shake{animation:ad-shake 0.4s linear}
  @keyframes ad-shake{
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-4px); }
    50% { transform: translateX(4px); }
    75% { transform: translateX(-2px); }
  }
  .ad-commit .ad-hint{font-family:'JetBrains Mono',monospace;font-size:10.5px;
    color:var(--muted);font-weight:500}
  .ad-commit #surprise-hint{color:var(--accent-2);opacity:0;transition:opacity 0.2s}
  .ad-commit #surprise-hint.on{opacity:1}
  #ad-surprise.flash-hint{box-shadow:0 0 0 2px var(--accent-wash);transition:box-shadow 0.25s}
  .array-trains{background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;
    padding:8px;max-height:520px;overflow:auto}
  .array-trains .row{display:grid;grid-template-columns:48px 1fr;gap:8px;
    align-items:center;padding:4px 0;border-bottom:1px dotted var(--rule)}
  .array-trains .row:last-child{border-bottom:0}
  .array-trains .row .label{font-family:'JetBrains Mono',monospace;font-size:10.5px;
    color:var(--muted);white-space:nowrap}
  .array-trains .row svg{width:100%;height:36px;display:block}
  .array-trains .empty{font-family:'JetBrains Mono',monospace;font-size:11.5px;
    color:var(--muted);padding:14px;text-align:center}
  .array-trains .more{font-family:'JetBrains Mono',monospace;font-size:11px;
    color:var(--muted);padding:6px 0 0;text-align:center}
  .array-trains .row.added{grid-template-columns:54px 1fr 18px;gap:6px;
    padding:6px 8px;border:1px solid transparent;border-radius:4px;
    cursor:pointer;align-items:center;opacity:0.7}
  .array-trains .row.added:hover{background:var(--paper-2)}
  .array-trains .row.added.on{opacity:1;border-color:var(--accent);
    background:var(--accent-wash)}
  .array-trains .row.added .label{display:inline-block;padding:1px 6px;border-radius:3px;
    background:var(--paper-2);color:var(--ink);font-weight:500}
  .array-trains .row.added.on .label{background:var(--accent);color:#fff}
  .array-trains .row.added .summary{font-family:'JetBrains Mono',monospace;
    font-size:10px;color:var(--muted);line-height:1.3;grid-column:2 / 3;
    grid-row:1}
  .array-trains .row.added svg{grid-column:2 / 3;grid-row:2}
  .array-trains .row.added .rm{appearance:none;border:0;background:transparent;
    color:var(--muted-2);font-family:'JetBrains Mono',monospace;font-size:14px;
    cursor:pointer;padding:0;line-height:1;grid-row:1 / span 2}
  .array-trains .row.added .rm:hover{color:var(--danger)}
  .added-clear{appearance:none;border:1px solid var(--rule);background:#fff;
    font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.04em;
    text-transform:uppercase;color:var(--muted);padding:2px 8px;border-radius:3px;
    cursor:pointer;margin-left:auto;font-weight:500}
  .added-clear:hover{color:var(--danger);border-color:var(--danger)}
  @media (max-width:980px){
    .array-body{grid-template-columns:1fr}
    .array-body > div + div{border-left:0;border-top:1px solid var(--rule)}
  }

  /* --- module-specific: stimulator flow demo (M3 sect 04) ---------- */
  /* === CONDUCTOR layout: 2x2 quad + header + sliders + log ============= */
  .flow-demo.conductor{border:1px solid var(--rule);background:#fff;border-radius:6px;
    padding:0;margin:24px 0;overflow:hidden;display:flex;flex-direction:column}

  /* header pill row */
  .cond-header{display:flex;align-items:center;gap:10px;padding:10px 14px;
    border-bottom:1px solid var(--rule);background:var(--paper-2);flex-wrap:wrap}
  .cond-pills{display:flex;align-items:center;gap:4px}
  .cond-pill{appearance:none;border:1px solid var(--rule);background:#fff;
    font:inherit;font-family:'JetBrains Mono',monospace;font-size:11.5px;
    font-weight:600;letter-spacing:0.04em;text-transform:uppercase;
    padding:5px 11px;border-radius:4px;cursor:pointer;color:var(--muted);
    display:inline-flex;align-items:center;gap:6px;line-height:1}
  .cond-pill:not(:disabled):hover{border-color:var(--accent);color:var(--accent-2)}
  .cond-pill:disabled{opacity:0.45;cursor:not-allowed}
  .cond-pill .n{color:var(--muted-2);font-variant-numeric:tabular-nums;
    font-size:11px;font-weight:500;background:var(--paper-2);padding:0 5px;
    border-radius:2px}
  .cond-pill.armed{color:var(--accent-2);border-color:var(--accent);background:#fff}
  .cond-pill.armed .n{color:var(--accent-2);background:var(--accent-wash)}
  .cond-pill.done{color:var(--accent-2);border-color:var(--rule);opacity:0.7}
  .cond-pill.done .n{color:var(--accent-2);background:var(--accent-wash)}
  .cond-pill.active{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .cond-pill.active .n{color:var(--accent);background:#000}
  .cond-arrow{color:var(--muted-2);font-family:'JetBrains Mono',monospace;
    font-size:14px;line-height:1}
  .cond-state{font-family:'JetBrains Mono',monospace;font-size:11px;
    background:var(--accent-wash);color:var(--accent-2);padding:3px 10px;
    border-radius:3px;border:1px solid var(--rule);
    text-transform:lowercase;letter-spacing:0.02em}
  .cond-clock{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:12.5px;color:var(--ink);background:#fff;padding:3px 10px;
    border-radius:3px;border:1px solid var(--rule);
    font-variant-numeric:tabular-nums;font-weight:500}
  .cond-link{font-family:'JetBrains Mono',monospace;font-size:10.5px;
    color:var(--muted);border:0;border-bottom:1px dotted var(--rule)}
  .cond-link:hover{color:var(--accent);border-bottom-color:var(--accent)}

  /* 2x2 quad */
  .cond-quad{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);
    grid-template-rows:280px 220px;gap:0}
  .cond-cell{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);
    display:flex;flex-direction:column;min-width:0;min-height:0;background:#fff}
  .cond-cell:nth-child(2n){border-right:0}
  .cond-cell:nth-last-child(-n+2){border-bottom:0}
  .cond-h{display:flex;align-items:baseline;gap:8px;padding:8px 12px;
    border-bottom:1px solid var(--rule-2);background:var(--paper-2);
    font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--ink);
    letter-spacing:0.04em;text-transform:uppercase;font-weight:500}
  .cond-h .cond-tag{font-size:10px;background:#fff;color:var(--muted);
    padding:1px 6px;border-radius:3px;border:1px solid var(--rule);
    text-transform:none;letter-spacing:0.02em;font-weight:500}
  .cond-h .cond-sub{margin-left:auto;font-size:10.5px;color:var(--muted);
    text-transform:none;letter-spacing:0.02em;font-weight:500;
    text-overflow:ellipsis;overflow:hidden;white-space:nowrap;max-width:50%}

  /* TL: Utah-live */
  .cond-utah-body{flex:1;display:flex;align-items:center;justify-content:center;
    padding:8px;min-height:0}
  .cond-utah-body svg{display:block;width:100%;height:100%;
    max-width:240px;max-height:240px;
    background:var(--paper-2);border:1px solid var(--rule);border-radius:4px}

  /* TR: Carousel */
  .cond-strip-body{flex:1;padding:6px 10px 8px;overflow-y:auto;min-height:0}
  .cond-strip-body svg{display:block;width:100%;height:auto;min-height:240px}

  /* BL: Safety */
  .cond-safety-grid{display:grid;grid-template-columns:1fr 1fr 1fr;
    gap:6px;padding:8px 10px}
  .cond-safety .fd-safety-warn{margin:0 10px 8px;font-family:'JetBrains Mono',monospace;
    font-size:10.5px;color:var(--danger);line-height:1.5;display:none}
  .cond-safety .fd-safety-warn.on{display:block}
  .cond-safety .fd-safety-warn .chip{display:inline-block;background:#fff;
    border:1px solid var(--danger);color:var(--danger);padding:1px 6px;
    border-radius:3px;margin:2px 4px 2px 0;font-size:10px}

  /* BR: Power */
  .cond-power-body{flex:1;padding:6px 10px 8px;display:flex;align-items:stretch;
    min-height:0}
  .cond-power-body svg{display:block;width:100%;height:100%;min-height:140px}

  /* Controls (single row) */
  .cond-controls{padding:10px 14px;background:var(--paper-2);
    border-bottom:1px solid var(--rule)}
  .cond-sliders{display:grid;grid-template-columns:repeat(3, 1fr);gap:14px;
    align-items:center}
  .cond-knob{display:grid;grid-template-columns:max-content 1fr max-content;
    gap:8px 10px;align-items:center}
  .cond-knob label{font-family:'JetBrains Mono',monospace;font-size:11px;
    color:var(--muted);white-space:nowrap;letter-spacing:0.02em}
  .cond-knob .v{font-family:'JetBrains Mono',monospace;font-size:11px;
    color:var(--ink);text-align:right;min-width:60px;
    font-variant-numeric:tabular-nums;font-weight:500}
  .cond-knob input[type=range]{appearance:none;background:transparent;
    height:18px;width:100%;cursor:pointer;margin:0;padding:0}
  .cond-knob input[type=range]:focus{outline:none}
  .cond-knob input[type=range]:focus-visible{outline:2px solid var(--accent);
    outline-offset:2px;border-radius:3px}
  .cond-knob input[type=range]::-webkit-slider-runnable-track{height:2px;
    background:var(--rule);border-radius:1px}
  .cond-knob input[type=range]::-webkit-slider-thumb{appearance:none;
    height:12px;width:12px;background:var(--accent);border-radius:50%;
    margin-top:-5px;border:0}
  .cond-knob input[type=range]::-moz-range-track{height:2px;
    background:var(--rule);border-radius:1px}
  .cond-knob input[type=range]::-moz-range-thumb{height:12px;width:12px;
    background:var(--accent);border-radius:50%;border:0}

  /* Log: collapsible */
  .cond-log-wrap > summary{cursor:pointer;list-style:none;
    padding:8px 14px;background:#fff;
    font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--muted);
    text-transform:uppercase;letter-spacing:0.04em;font-weight:500;
    display:flex;align-items:center;gap:8px}
  .cond-log-wrap > summary::-webkit-details-marker{display:none}
  .cond-log-wrap > summary::before{content:'\25B8';color:var(--muted-2);
    font-size:11px;transition:transform 0.15s;display:inline-block;width:10px}
  .cond-log-wrap[open] > summary::before{transform:rotate(90deg)}
  .cond-log-wrap[open] > summary{border-top:1px solid var(--rule);
    border-bottom:1px solid var(--rule-2)}
  .cond-log-wrap > summary .added-clear{margin-left:auto}
  .cond-log-wrap .fd-log{height:180px}

  /* Responsive: at narrow widths, collapse the quad to one column */
  @media (max-width: 980px){
    .cond-quad{grid-template-columns:1fr;grid-template-rows:auto auto auto auto}
    .cond-cell{border-right:0}
    .cond-cell:nth-child(2n){border-right:0}
    .cond-cell:nth-last-child(-n+2){border-bottom:1px solid var(--rule)}
    .cond-cell:last-child{border-bottom:0}
    .cond-safety-grid{grid-template-columns:1fr 1fr}
    .cond-sliders{grid-template-columns:1fr}
  }

  /* Legacy classes kept for the now-hidden lifecycle diagram + back-compat */
  .flow-demo:not(.conductor){border:1px solid var(--rule);background:#fff;border-radius:6px;
    padding:0;margin:24px 0}
  .flow-log-wrap{border-top:1px solid var(--rule);padding:16px 18px;background:#fff}
  .flow-h{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);
    letter-spacing:0.05em;text-transform:uppercase;margin:0 0 10px;
    display:flex;align-items:center;gap:8px}
  .flow-svg-wrap{background:var(--paper-2);border:1px solid var(--rule);border-radius:4px;
    padding:10px}
  .flow-svg-wrap svg{width:100%;height:auto;display:block}
  .fd-node rect{fill:#fff;stroke:var(--ink);stroke-width:1}
  .fd-node .fd-title{font-family:'JetBrains Mono',monospace;font-size:9px;
    font-weight:600;fill:var(--ink);letter-spacing:0.04em}
  .fd-node .fd-sub{font-family:'Inter',sans-serif;font-size:8px;fill:var(--muted)}
  .fd-node.on rect{fill:var(--accent-wash);stroke:var(--accent-2);stroke-width:1.6}
  .fd-node.on .fd-title{fill:var(--accent-2)}
  .fd-node.on .fd-sub{fill:var(--accent-2)}
  .fd-arrow{stroke:var(--ink-2);stroke-width:1.2;fill:none}
  .fd-arrow.loop{stroke:var(--muted-2);stroke-dasharray:3 3;stroke-width:1}
  .fd-loop{font-family:'JetBrains Mono',monospace;font-size:8px;fill:var(--muted-2)}
  .fd-steps{display:flex;flex-direction:column;gap:6px;margin:14px 0 10px}
  .fd-step-btn{appearance:none;border:1px solid var(--rule);background:#fff;
    font:inherit;text-align:left;padding:10px 14px;border-radius:5px;cursor:pointer;
    color:var(--ink);display:grid;grid-template-columns:24px 1fr;
    grid-template-rows:auto auto;column-gap:10px;row-gap:0;
    transition:background 0.12s, border-color 0.12s, opacity 0.12s}
  .fd-step-btn .n{grid-row:1 / span 2;align-self:center;
    font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600;
    color:var(--muted-2);text-align:center;font-variant-numeric:tabular-nums}
  .fd-step-btn .lbl{font-family:'JetBrains Mono',monospace;font-size:12px;
    font-weight:600;letter-spacing:0.05em;text-transform:uppercase;
    color:var(--ink)}
  .fd-step-btn .sub{font-family:'Inter',sans-serif;font-size:11px;color:var(--muted);
    line-height:1.4}
  .fd-step-btn:not(:disabled):hover{border-color:var(--accent);background:var(--paper-2)}
  .fd-step-btn:not(:disabled):hover .n{color:var(--accent-2)}
  .fd-step-btn:disabled{opacity:0.45;cursor:not-allowed}
  .fd-step-btn.armed{border-color:var(--accent);background:var(--accent-wash)}
  .fd-step-btn.armed .n{color:var(--accent-2)}
  .fd-step-btn.done{border-color:var(--rule);background:#fff;opacity:0.65}
  .fd-step-btn.done .n{color:var(--accent-2)}
  .fd-step-btn.active{background:var(--ink);border-color:var(--ink);color:var(--paper)}
  .fd-step-btn.active .lbl{color:var(--paper)}
  .fd-step-btn.active .sub{color:#c5c2b6}
  .fd-step-btn.active .n{color:var(--accent)}
  .fd-step-btn.danger{background:var(--danger);border-color:var(--danger);color:#fff}
  .fd-step-btn.danger .lbl{color:#fff}
  .fd-step-btn.danger .sub{color:#fbe2d4}
  .fd-step-btn.danger .n{color:#fff}

  .flow-controls{margin-top:6px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
  .flow-controls .fd-state{font-family:'JetBrains Mono',monospace;
    font-size:11px;color:var(--accent-2);background:var(--accent-wash);
    padding:3px 8px;border-radius:3px;border:1px solid var(--rule)}

  /* log panel: wider, shorter, sits below everything */
  .fd-log{background:#ffffff;border:1px solid var(--rule);border-radius:4px;
    height:220px;overflow:auto;padding:8px 0;
    font-family:'JetBrains Mono',monospace;font-size:11.5px;line-height:1.45}
  .fd-log-row{display:grid;grid-template-columns:84px 1fr;gap:10px;
    padding:2px 14px;color:var(--ink-2)}
  .fd-log-row .ts{color:var(--muted-2);font-variant-numeric:tabular-nums}
  .fd-log-row .msg em{color:var(--accent-2);font-style:normal}
  .fd-log-row.muted{color:var(--muted-2)}
  .fd-log-row.info  .msg{color:var(--ink)}
  .fd-log-row.ok    .msg{color:var(--accent-2)}
  .fd-log-row.warn  .msg{color:var(--danger)}
  .fd-log-row.dim   .msg{color:var(--muted)}

  /* carousel column inside the top row */
  .flow-col-strip .fd-clock{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:13px;color:var(--ink);background:#fff;padding:3px 10px;
    border-radius:3px;border:1px solid var(--rule);font-variant-numeric:tabular-nums;
    text-transform:none;letter-spacing:0.02em;font-weight:500;padding-right:14px}
  .flow-strip-wrap{background:#fff;border:1px solid var(--rule);border-radius:4px;
    padding:0;max-height:520px;overflow-y:auto;margin-bottom:10px}
  .flow-strip-wrap svg{display:block;width:100%;height:auto;min-height:300px}
  .flow-power-wrap{background:#fff;border:1px solid var(--rule);border-radius:4px;
    padding:6px 8px 8px;margin-bottom:12px}
  .flow-power-wrap svg{display:block;width:100%;height:auto}
  .flow-power-label{display:flex;align-items:baseline;gap:10px;
    font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--muted);
    letter-spacing:0.04em;text-transform:uppercase;margin-bottom:3px}
  .flow-power-label .fd-power-now{margin-left:auto;color:var(--accent-2);
    font-size:11.5px;text-transform:none;letter-spacing:0.02em;
    font-variant-numeric:tabular-nums;font-weight:500}
  .flow-strip-controls{display:grid;grid-template-columns:1.4fr 1fr;gap:18px;
    padding:0;align-items:start}
  .flow-strip-controls .flow-params{display:grid;
    grid-template-columns:max-content 1fr max-content;gap:8px 12px;align-items:center}
  .flow-strip-controls .flow-params label{font-family:'JetBrains Mono',monospace;
    font-size:11.5px;color:var(--muted);white-space:nowrap}
  .flow-strip-controls .flow-params .v{font-family:'JetBrains Mono',monospace;
    font-size:11.5px;color:var(--ink);font-variant-numeric:tabular-nums;
    text-align:right;min-width:80px}
  .flow-strip-controls input[type=range]{appearance:none;background:transparent;
    height:18px;width:100%;cursor:pointer;margin:0;padding:0}
  .flow-strip-controls input[type=range]:focus{outline:none}
  .flow-strip-controls input[type=range]:focus-visible{outline:2px solid var(--accent);
    outline-offset:2px;border-radius:3px}
  .flow-strip-controls input[type=range]::-webkit-slider-runnable-track{height:2px;
    background:var(--rule);border-radius:1px}
  .flow-strip-controls input[type=range]::-webkit-slider-thumb{appearance:none;
    height:12px;width:12px;background:var(--accent);border-radius:50%;
    margin-top:-5px;border:0}
  .flow-strip-controls input[type=range]::-moz-range-track{height:2px;
    background:var(--rule);border-radius:1px}
  .flow-strip-controls input[type=range]::-moz-range-thumb{height:12px;width:12px;
    background:var(--accent);border-radius:50%;border:0}
  .flow-send{display:flex;flex-direction:column;gap:8px;align-items:flex-start;
    justify-content:center}
  .flow-send .fd-summary{font-family:'JetBrains Mono',monospace;font-size:11.5px;
    color:var(--muted);line-height:1.5}

  /* utah-live mini grid (left column) */
  .fd-utah-wrap{margin-top:14px;padding-top:14px;border-top:1px solid var(--rule)}
  .fd-utah-wrap .flow-h{display:flex;align-items:center;gap:8px}
  .fd-utah-sub{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:10.5px;color:var(--muted);text-transform:none;letter-spacing:0.02em;
    font-weight:500;background:#fff;border:1px solid var(--rule);
    padding:2px 8px;border-radius:3px}
  .fd-utah-wrap svg{display:block;width:100%;height:auto;
    background:var(--paper-2);border:1px solid var(--rule);border-radius:4px}

  /* compact safety panel (left column, stacked) */
  .fd-safety-compact{margin-top:14px;padding-top:14px;border-top:1px solid var(--rule)}
  .fd-safety-compact .flow-h{display:flex;align-items:center;gap:8px}
  .fd-safety-assump{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:10px;color:var(--muted);text-transform:none;letter-spacing:0.02em;
    font-weight:500;background:#fff;border:1px solid var(--rule);
    padding:2px 6px;border-radius:3px;white-space:nowrap}
  .fd-safety.vstack{display:flex;flex-direction:column;gap:6px;margin-top:8px}
  .fd-metric{background:#fff;border:1px solid var(--rule);border-radius:4px;
    padding:6px 10px;display:grid;grid-template-columns:1fr auto;
    grid-template-rows:auto auto;column-gap:10px;row-gap:0;align-items:baseline}
  .fd-metric-h{grid-column:1 / 2;grid-row:1;font-family:'JetBrains Mono',monospace;
    font-size:10px;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;
    font-weight:500}
  .fd-metric-v{grid-column:2 / 3;grid-row:1 / span 2;align-self:center;
    font-family:'JetBrains Mono',monospace;font-size:13.5px;color:var(--ink);
    font-weight:600;font-variant-numeric:tabular-nums;line-height:1.2;text-align:right}
  .fd-metric-sub{grid-column:1 / 2;grid-row:2;font-family:'JetBrains Mono',monospace;
    font-size:9.5px;color:var(--muted-2);line-height:1.3}
  .fd-metric.over{background:#faf2ee;border-color:var(--danger)}
  .fd-metric.over .fd-metric-v{color:var(--danger)}
  .fd-metric.over .fd-metric-h{color:var(--danger)}
  .fd-metric.caution{background:var(--accent-wash);border-color:var(--accent-2)}
  .fd-metric.caution .fd-metric-v{color:var(--accent-2)}
  .fd-metric.caution .fd-metric-h{color:var(--accent-2)}
  .fd-metric.live .fd-metric-v{color:var(--accent-2)}
  .fd-safety-warn{margin-top:10px;font-family:'JetBrains Mono',monospace;
    font-size:10.5px;color:var(--accent-2);line-height:1.5;display:none}
  .fd-safety-warn.on{display:block}
  .fd-safety-warn .chip{display:inline-block;background:#fff;border:1px solid var(--danger);
    color:var(--danger);padding:1px 6px;border-radius:3px;margin:2px 4px 2px 0;
    font-size:10px}
  @media (max-width:980px){
    .flow-body{grid-template-columns:1fr}
    .flow-body > div + div{border-left:0;border-top:1px solid var(--rule)}
    .flow-strip-controls{grid-template-columns:1fr}
  }

  /* --- module-specific: stim demo ---------------------------------- */
  .stim-demo{border:1px solid var(--rule);background:#fff;border-radius:6px;
    padding:0;margin:24px 0;overflow:hidden}
  .stim-tabs{display:flex;border-bottom:1px solid var(--rule);background:var(--paper-2)}
  .stim-tabs button{appearance:none;border:0;background:transparent;font:inherit;
    font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;
    text-transform:uppercase;color:var(--muted);padding:14px 18px;cursor:pointer;
    border-right:1px solid var(--rule);border-bottom:2px solid transparent;
    flex:1;text-align:left}
  .stim-tabs button:last-child{border-right:0}
  .stim-tabs button[aria-selected=true]{color:var(--ink);border-bottom-color:var(--accent);
    background:#fff}
  .stim-tabs button:hover:not([aria-selected=true]){color:var(--ink);background:#fff}
  .stim-tabs button .n{color:var(--muted-2);font-variant-numeric:tabular-nums;
    margin-right:8px;font-weight:500}
  .stim-tabs button[aria-selected=true] .n{color:var(--accent)}
  .stim-body{padding:24px;display:grid;grid-template-columns:1fr 1.3fr;gap:24px;
    align-items:start}
  .stim-explain h4{margin:0 0 8px;font-size:14px;font-weight:600;
    letter-spacing:0.04em;text-transform:uppercase;color:var(--ink)}
  .stim-explain p{margin:0 0 10px;font-size:13.5px;color:var(--ink-2)}
  .stim-explain .strategy{font-family:'JetBrains Mono',monospace;font-size:11px;
    color:var(--accent-2);background:var(--accent-wash);padding:2px 8px;
    border-radius:3px;display:inline-block;margin-bottom:10px;
    letter-spacing:0.02em;text-transform:uppercase}
  .stim-figure{background:var(--paper-2);border:1px solid var(--rule);
    border-radius:6px;padding:16px}
  .stim-figure svg{width:100%;height:auto;display:block}
  .stim-figure .legend{margin-top:8px;font-family:'JetBrains Mono',monospace;
    font-size:11px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
  .stim-figure .legend i{display:inline-block;width:12px;height:6px;
    margin-right:5px;vertical-align:middle;border-radius:1px}
  .stim-controls{margin-top:14px;display:grid;grid-template-columns:max-content 1fr max-content;
    gap:8px 14px;align-items:center;padding:12px 14px;background:var(--paper-2);
    border:1px solid var(--rule);border-radius:6px}
  .stim-controls label{font-family:'JetBrains Mono',monospace;font-size:12px;
    color:var(--muted);white-space:nowrap}
  .stim-controls .v{font-family:'JetBrains Mono',monospace;font-size:12px;
    color:var(--ink);font-variant-numeric:tabular-nums;text-align:right;min-width:90px}
  .stim-controls input[type=range]{appearance:none;background:transparent;
    height:20px;width:100%;cursor:pointer;margin:0;padding:0}
  .stim-controls input[type=range]:focus{outline:none}
  .stim-controls input[type=range]:focus-visible{outline:2px solid var(--accent);
    outline-offset:2px;border-radius:3px}
  .stim-controls input[type=range]::-webkit-slider-runnable-track{height:2px;
    background:var(--rule);border-radius:1px}
  .stim-controls input[type=range]::-webkit-slider-thumb{appearance:none;
    height:14px;width:14px;background:var(--accent);border-radius:50%;
    margin-top:-6px;border:0}
  .stim-controls input[type=range]::-moz-range-track{height:2px;
    background:var(--rule);border-radius:1px}
  .stim-controls input[type=range]::-moz-range-thumb{height:14px;width:14px;
    background:var(--accent);border-radius:50%;border:0}
  .stim-controls .runrow{grid-column:1 / -1;display:flex;gap:8px;
    align-items:center;border-top:1px dotted var(--rule);padding-top:10px}
  .stim-controls .runrow button{appearance:none;border:1px solid var(--rule);
    background:#fff;font:inherit;font-family:'JetBrains Mono',monospace;
    font-size:11px;letter-spacing:0.04em;text-transform:uppercase;
    padding:6px 12px;border-radius:4px;cursor:pointer;color:var(--ink)}
  .stim-controls .runrow button:hover{border-color:var(--accent);color:var(--accent-2)}
  .stim-controls .runrow .status{margin-left:auto;font-family:'JetBrains Mono',monospace;
    font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}
  @media (max-width:780px){
    .stim-body{grid-template-columns:1fr}
    .stim-tabs{flex-direction:column}
    .stim-tabs button{border-right:0;border-bottom:1px solid var(--rule)}
  }

  footer{margin-top:64px;padding-top:24px;border-top:1px solid var(--rule);
    font-size:12px;color:var(--muted);font-family:'JetBrains Mono',monospace}
  footer a{color:var(--muted);border-bottom:1px solid var(--rule-2)}
  footer a:hover{color:var(--accent);border-bottom-color:var(--accent)}

  @media (max-width:780px){
    .page{padding:32px 20px 80px}
    .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
    header.masthead h1{font-size:30px}
  }
""")


def esc(s: str) -> str:
    return html.escape(s)


# module index -> (file, short pipeline label, full nav title)
MODULE_FILES = {
    1: "M1-computer-vision.html",
    2: "M2-deepgaze-and-gaze.html",
    3: "M3-neuromod-and-stim.html",
    4: "M4-phosphene-simulation.html",
    5: "M5-decoding-and-closed-loop.html",
}
MODULE_NAV_TITLES = {
    1: "M1 &middot; Computer vision",
    2: "M2 &middot; Gaze &amp; DeepGaze",
    3: "M3 &middot; Neuromodulation &amp; stim",
    4: "M4 &middot; Phosphenes",
    5: "M5 &middot; Decoding &amp; closed loop",
}


def pipeline_strip(here_idx: int) -> str:
    """Renders the 5-module pipeline strip; `here_idx` is 1..5 marking the active one.
    Every non-active step links to its module page."""
    steps = [
        (1, "Camera + CV"),
        (2, "Gaze"),
        (3, "Stimulation"),
        (4, "Phosphenes"),
        (5, "Decoding"),
    ]
    out = ["<div class='pipeline' aria-label='Bootcamp pipeline progress'>"]
    for j, (n, name) in enumerate(steps):
        active = (n == here_idx)
        lbl = f"M{n}" + (" &middot; here" if active else "")
        inner = f"<div class='lbl'>{lbl}</div><div class='name'>{name}</div>"
        if active:
            out.append(f"<div class='step active'>{inner}</div>")
        else:
            out.append(f"<a class='step' href='{MODULE_FILES[n]}'>{inner}</a>")
        if j < len(steps) - 1:
            out.append("<div class='arr'>&rarr;</div>")
    out.append("</div>")
    return "".join(out)


def module_nav(here_idx: int) -> str:
    """Prev / next navigation bar for module page `here_idx` (1..5).
    Module 1's prev and module 5's next point at the bootcamp plan."""
    if here_idx <= 1:
        prev_href, prev_name = "../bootcamp-plan.html", "Bootcamp plan"
    else:
        prev_href, prev_name = MODULE_FILES[here_idx - 1], MODULE_NAV_TITLES[here_idx - 1]
    if here_idx >= 5:
        next_href, next_name = "../bootcamp-plan.html", "Bootcamp plan"
    else:
        next_href, next_name = MODULE_FILES[here_idx + 1], MODULE_NAV_TITLES[here_idx + 1]
    return (
        "<nav class='module-nav' aria-label='Module navigation'>"
        f"<a class='mn-prev' href='{prev_href}'>"
        f"<span class='mn-dir'>&larr; prev</span><span class='mn-name'>{prev_name}</span></a>"
        f"<a class='mn-next' href='{next_href}'>"
        f"<span class='mn-dir'>next &rarr;</span><span class='mn-name'>{next_name}</span></a>"
        "</nav>"
    )


def page(title: str, eyebrow: str, h1_html: str, lede: str,
         meta_html: str, toc_html: str, body_html: str,
         pipeline_html: str = "", footer_html: str = "",
         nav_html: str = "") -> str:
    default_footer = (
        'Internal planning document. '
        'Web to update once content is final: '
        '<a href="https://www.aanmelder.nl/aimdworkshop2026/bootcamp">'
        'aanmelder.nl/aimdworkshop2026/bootcamp</a>.'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{SHARED_CSS}</style>
</head>
<body>
<main class="page">

<header class="masthead">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1_html}</h1>
  <p class="lede">{lede}</p>
  <div class="meta">{meta_html}</div>
</header>

{nav_html}

{pipeline_html}

{toc_html}

{body_html}

{nav_html}

<footer>
  {footer_html or default_footer}
</footer>

</main>
</body>
</html>
"""


# --- roles ------------------------------------------------------------------

ROLES = {
    "antonio":  '<span class="role">Antonio</span>',
    "lefteris": '<span class="role">Lefteris &amp; Jorge</span>',
    "team":     '<span class="role dual">Antonio + Lefteris &amp; Jorge</span>',
    "nth":      '<span class="role org">NTH</span>',
}


# --- bootcamp plan content --------------------------------------------------

AGENDA_ROWS = [
    ("20 min", "Intro to the field",                  "Cortical neuroprosthesis framing. Slides only.",                                "antonio"),
    ("30 min", "Module intros",                       "Five module intros, ~6 min each.",                                              "team"),
    ("1 hour", "Guided exercises",                    "Run one exercise from each module. Self-paced.",                                "team"),
    ("1 hour", "Vibe coding / dev / experiments",     "Three parallel tracks. Pick one.",                                              "team"),
    ("15 min", "Upload demo to GitHub",               "Submit code + README + screenshot/video + track label.",                        "team"),
    ("flex",   "Demos &amp; networking",              "Voluntary demos. One prize per track.",                                         "nth"),
]

MODULES = [
    ("M1", "M1-computer-vision.html",          "Computer vision",                    "lefteris",
     ["Image input and preprocessing", "YOLO segmentation", "OpenCV edge detection"]),
    ("M2", "M2-deepgaze-and-gaze.html",        "Gaze &amp; DeepGaze",                "lefteris",
     ["DeepGaze III scanpath generation", "Extra gaze statistics", "Gaze dynamics simulation"]),
    ("M3", "M3-neuromod-and-stim.html",        "Neuromodulation &amp; stimulation",  "antonio",
     ["Neurolight stimulator and stim params", "Electrode coordinates and visual-field mapping", "Vimplant2 interactive electrode placement"]),
    ("M4", "M4-phosphene-simulation.html",     "Phosphene simulation",               "lefteris",
     ["Dynaphos phosphene maps", "Stimulation -> phosphene conversion", "Temporal dynamics"]),
    ("M5", "M5-decoding-and-closed-loop.html", "Decoding &amp; closed loop",         "antonio",
     ["Pretrained decoder demo", "Train your own decoder", "Minimal closed-loop demo"]),
]

TRACKS = [
    ("Experimental", "Build a fun, visually compelling demo. Punch, clarity, demo value.",
     ["Visual or short video output", "Reuse any module's building blocks", "No need to be performant"]),
    ("Developer", "Build or improve the real-time / closed-loop pipeline. Performance, device handling, structure.",
     ["Profiling and optimization", "Real-time or near-real-time target", "Clean code, tests welcome"]),
    ("Open neurotech", "Original neurotech application. Connect to the bootcamp theme however you like.",
     ["Original idea allowed", "Reuse any building blocks", "Define your own success criterion"]),
]

TOOLS = [
    ("Dynaphos",              "https://github.com/neuralcodinglab/dynaphos",
     "Phosphene maps, stim-to-phosphene, temporal dynamics."),
    ("Dynaphos-experiments",  "https://github.com/neuralcodinglab/dynaphos-experiments",
     "Use and modify for the demo and exercises."),
    ("DeepGaze",              "https://github.com/matthias-k/DeepGaze",
     "DeepGaze III scanpath simulation; extend with extra gaze statistics and dynamics."),
    ("YOLO",                  "https://github.com/ultralytics/ultralytics",
     "Object detection and segmentation."),
    ("OpenCV",                "https://opencv.org/",
     "Edge detection and general image processing."),
    ("Neurolight",            "",
     "Stimulator and parameter explanation (Antonio)."),
    ("Vimplant2",             "https://antonio-lozano.github.io/vimplant2/",
     "Interactive electrode-placement simulation (Antonio)."),
    ("Engram",                "",
     "Neural-recordings reference for the introduction talk (Antonio)."),
]


def render_agenda() -> str:
    rows = "".join(
        f"<tr><td class='time'>{esc(t)}</td><td><strong>{b}</strong></td>"
        f"<td>{d}</td><td>{ROLES[o]}</td></tr>"
        for t, b, d, o in AGENDA_ROWS
    )
    return (
        "<table class='t'><thead><tr>"
        "<th>Time</th><th>Block</th><th>Activity</th><th>Lead</th>"
        "</tr></thead><tbody>" + rows + "</tbody></table>"
    )


def render_module_grid() -> str:
    cards = []
    for mid, href, name, lead, bullets in MODULES:
        bullets_html = "<ul class='tight'>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
        cards.append(
            f"<div class='panel'>"
            f"<div class='panel-sub'><span class='readout muted'>{mid}</span> &nbsp; {ROLES[lead]}</div>"
            f"<h4><a href='modules/{href}'>{name}</a></h4>"
            f"{bullets_html}"
            f"</div>"
        )
    return "<div class='grid-2'>" + "".join(cards) + "</div>"


def render_tracks() -> str:
    cards = []
    for name, summary, bullets in TRACKS:
        bullets_html = "<ul class='tight'>" + "".join(f"<li>{esc(b)}</li>" for b in bullets) + "</ul>"
        cards.append(
            f"<div class='panel'>"
            f"<h4>{esc(name)}</h4>"
            f"<p style='margin:0 0 8px;color:var(--ink-2)'>{esc(summary)}</p>"
            f"{bullets_html}"
            f"</div>"
        )
    return "<div class='grid-3'>" + "".join(cards) + "</div>"


def render_tools() -> str:
    rows = []
    for name, url, desc in TOOLS:
        link = (
            f"<a href='{esc(url)}'>{esc(url)}</a>"
            if url else "<em style='color:var(--muted)'>tbd</em>"
        )
        rows.append(
            f"<tr><td><strong>{esc(name)}</strong></td>"
            f"<td>{esc(desc)}</td>"
            f"<td class='mono'>{link}</td></tr>"
        )
    return (
        "<table class='t'><thead><tr>"
        "<th>Tool</th><th>Use</th><th>Link</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def build_plan() -> None:
    toc = """<nav class='toc' aria-label='Sections'>
  <a href='#leads'><span class='n'>00</span> Leads</a>
  <a href='#summary'><span class='n'>01</span> Summary</a>
  <a href='#formats'><span class='n'>02</span> Content formats</a>
  <a href='#audience'><span class='n'>03</span> Audience</a>
  <a href='#agenda'><span class='n'>04</span> Agenda</a>
  <a href='#intro-field'><span class='n'>05</span> Intro to the field</a>
  <a href='#module-intros'><span class='n'>06</span> Module intros</a>
  <a href='#exercises'><span class='n'>07</span> Guided exercises</a>
  <a href='#tracks'><span class='n'>08</span> Tracks</a>
  <a href='#upload'><span class='n'>09</span> Upload &amp; prizes</a>
  <a href='#tools'><span class='n'>10</span> Tools</a>
  <a href='#followups'><span class='n'>11</span> Follow-ups</a>
</nav>"""

    body = f"""
<section id='leads'>
<h2><span class='num'>00</span>Leads</h2>
<p class='kicker'>Who's leading what.</p>
<div class='grid-3'>
  <div class='panel'>
    <h4>Antonio</h4>
    <div class='panel-sub'>{ROLES['antonio']}</div>
    <ul class='tight'>
      <li>Intro to the field (slides, incl. engram for neural recordings)</li>
      <li><a href='modules/M3-neuromod-and-stim.html'>M3 - Neuromodulation &amp; stimulation</a> (Neurolight + Vimplant2)</li>
      <li><a href='modules/M5-decoding-and-closed-loop.html'>M5 - Decoding &amp; closed loop</a></li>
    </ul>
  </div>
  <div class='panel'>
    <h4>Lefteris &amp; Jorge</h4>
    <div class='panel-sub'>{ROLES['lefteris']}</div>
    <ul class='tight'>
      <li><a href='modules/M1-computer-vision.html'>M1 - Computer vision</a> (YOLO + OpenCV)</li>
      <li><a href='modules/M2-deepgaze-and-gaze.html'>M2 - Gaze &amp; DeepGaze</a> (DeepGaze III + extras)</li>
      <li><a href='modules/M4-phosphene-simulation.html'>M4 - Phosphene simulation</a> (Dynaphos)</li>
    </ul>
  </div>
  <div class='panel'>
    <h4>Shared / NTH</h4>
    <div class='panel-sub'>{ROLES['team']} &middot; {ROLES['nth']}</div>
    <ul class='tight'>
      <li>Module intros - each module's lead presents (~6 min)</li>
      <li>Closed-loop integration demo - jointly</li>
      <li>Prize judging and demo session - NTH organises</li>
    </ul>
  </div>
</div>
<aside class='warn'><strong>Update the web.</strong> Once content is final, update <a href='https://www.aanmelder.nl/aimdworkshop2026/bootcamp'>aanmelder.nl/aimdworkshop2026/bootcamp</a> with the final schedule, prerequisites, and per-track descriptions.</aside>
</section>

<section id='summary'>
<h2><span class='num'>01</span>Summary</h2>
<p class='kicker'>A tutorial-driven bootcamp around cortical neuroprosthesis workflows. Five modules from camera to closed loop; one open hour to build something; demo upload and prizes at the end.</p>
<p>The closed-loop demo at the end ties the modules together. Each module also stands on its own and a participant can pick any of them as their entry point.</p>
</section>

<section id='formats'>
<h2><span class='num'>02</span>Content formats</h2>
<p class='kicker'>Each module ships content in three formats. Participants pick what fits their style.</p>
<div class='grid-3'>
  <div class='panel'>
    <h4>Interactive HTML demos</h4>
    <div class='panel-sub'>read &amp; explore in a browser</div>
    <p>Self-contained pages with figures, mini-interactives, and notes. Run nothing - just understand.</p>
  </div>
  <div class='panel'>
    <h4>Jupyter notebooks</h4>
    <div class='panel-sub'>run &amp; modify in Google Colab</div>
    <p>One notebook per module. Open in Colab; run cell-by-cell; tweak the parameters and re-run.</p>
  </div>
  <div class='panel'>
    <h4>Development repo</h4>
    <div class='panel-sub'>full code, optional OpenAI tokens</div>
    <p>The full codebase for developer-track participants. OpenAI API tokens if we get them, for vibe-coding workflows.</p>
  </div>
</div>
</section>

<section id='audience'>
<h2><span class='num'>03</span>Audience &amp; prerequisites</h2>
<div class='grid-3'>
  <div class='panel'>
    <h4>All participants</h4>
    <div class='panel-sub'>baseline</div>
    <ul class='tight'>
      <li>Python (basic)</li>
      <li>IDE with Jupyter-cell support (VS Code recommended)</li>
      <li>Comfortable running cells top-to-bottom</li>
    </ul>
  </div>
  <div class='panel'>
    <h4>Vibe-coding track</h4>
    <div class='panel-sub'>add-on</div>
    <ul class='tight'>
      <li>Free LLM account (OpenAI, Anthropic, or Mistral)</li>
      <li>Goal: rapidly prototype with AI support</li>
    </ul>
  </div>
  <div class='panel'>
    <h4>Developer track</h4>
    <div class='panel-sub'>add-on</div>
    <ul class='tight'>
      <li>VS Code, Cursor, Claude Code, Codex, or equivalent</li>
      <li>Goal: deeper work on code quality, performance, real-time</li>
    </ul>
  </div>
</div>
</section>

<section id='agenda'>
<h2><span class='num'>04</span>Agenda</h2>
{render_agenda()}
</section>

<section id='intro-field'>
<h2><span class='num'>05</span>Intro to the field (20 min)</h2>
<p>Slide-driven framing before any code. {ROLES['antonio']} on stage.</p>
<div class='grid-2'>
  <div class='panel'>
    <h4>What is a cortical visual prosthesis?</h4>
    <p>Direct electrical stimulation of visual cortex to produce phosphenes in blind users. Bypasses the eye and optic nerve.</p>
  </div>
  <div class='panel'>
    <h4>What is phosphene vision?</h4>
    <p>A phosphene is a spot of light evoked by stimulation. Simulating it lets us prototype the full pipeline end-to-end.</p>
  </div>
  <div class='panel'>
    <h4>Engram &amp; neural recordings</h4>
    <p>Short tour of the recording side - what an engram is and how neural data is gathered. Sets up why decoding matters later in M5.</p>
  </div>
  <div class='panel'>
    <h4>Bootcamp goal</h4>
    <p>Build small but meaningful pieces of a closed-loop cortical vision pipeline. Each participant ships one working demo by the end of the day.</p>
  </div>
</div>
</section>

<section id='module-intros'>
<h2><span class='num'>06</span>Module intros (30 min)</h2>
<p>Each module lead presents their own intro, ~6 min, slides plus one figure from the module page.</p>
{render_module_grid()}
</section>

<section id='exercises'>
<h2><span class='num'>07</span>Guided exercises (1 hour)</h2>
<p>One exercise per module. Self-paced; participants can skip ahead once they finish a block. Materials live in the corresponding module pages.</p>
<table class='t'>
<thead><tr><th>Module</th><th>Exercise</th><th>Lead</th></tr></thead>
<tbody>
<tr><td><strong>M1</strong> CV</td><td>Run YOLO segmentation and OpenCV edge detection on a scene; compare the resulting activation maps.</td><td>{ROLES['lefteris']}</td></tr>
<tr><td><strong>M2</strong> Gaze</td><td>Sample a DeepGaze III scanpath and overlay our extra gaze statistics and dynamics.</td><td>{ROLES['lefteris']}</td></tr>
<tr><td><strong>M3</strong> Stim</td><td>Configure stim parameters with Neurolight; place electrodes interactively in Vimplant2.</td><td>{ROLES['antonio']}</td></tr>
<tr><td><strong>M4</strong> Phosphenes</td><td>Use Dynaphos to convert a stimulation pattern into a phosphene render; observe temporal dynamics.</td><td>{ROLES['lefteris']}</td></tr>
<tr><td><strong>M5</strong> Decoding</td><td>Run a pretrained decoder on phosphene canvases; then train your own toy decoder on a small batch.</td><td>{ROLES['antonio']}</td></tr>
</tbody>
</table>
</section>

<section id='tracks'>
<h2><span class='num'>08</span>Vibe coding, development &amp; experiments (1 hour)</h2>
<p>Three parallel tracks. Participants pick one. No switching mid-hour.</p>
{render_tracks()}
</section>

<section id='upload'>
<h2><span class='num'>09</span>Upload demo &amp; prizes</h2>
<div class='grid-2'>
  <div class='panel'>
    <h4>Upload to GitHub</h4>
    <div class='panel-sub'>15 min slot</div>
    <p style='margin:0 0 8px;color:var(--ink-2)'>Submission location: <code>GITHUB/NTH/D-BOOTCAMP/submissions</code></p>
    <ul class='tight'>
      <li>Code or notebook</li>
      <li>Short README (what it does, how to run, who built it)</li>
      <li>Screenshot, video, or demo artifact</li>
      <li>Track label: experimental / developer / open neurotech</li>
    </ul>
  </div>
  <div class='panel'>
    <h4>Prizes</h4>
    <div class='panel-sub'>organised by NTH</div>
    <ul class='tight'>
      <li><strong>Experimental:</strong> punchy / visually compelling demo</li>
      <li><strong>Developer:</strong> real-time, optimized, or closed-loop pipeline</li>
      <li><strong>Open neurotech:</strong> most original application connected to the bootcamp theme</li>
    </ul>
  </div>
</div>
</section>

<section id='tools'>
<h2><span class='num'>10</span>Tools</h2>
{render_tools()}
</section>

<section id='followups'>
<h2><span class='num'>11</span>Follow-ups</h2>
<aside class='todo'><strong>Update the web.</strong> Once content is final, update <a href='https://www.aanmelder.nl/aimdworkshop2026/bootcamp'>aanmelder.nl/aimdworkshop2026/bootcamp</a> with the final schedule, prerequisites, per-track descriptions, and prize info.</aside>
<aside class='todo'><strong>Module content.</strong> Each lead fills in their module page. Keep the section structure consistent across modules so participants can navigate from one to the next without re-orienting.</aside>
<aside class='todo'><strong>Neurolight &amp; engram.</strong> Confirm versions / sources Antonio will use before the bootcamp.</aside>
<aside class='todo'><strong>OpenAI tokens.</strong> Confirm whether we get them. If yes, distribute via the development repo to the vibe-coding track.</aside>
<aside class='todo'><strong>Development repo.</strong> Set up the dev repo for the developer track. Same five modules, full code, deployable to Colab too.</aside>
</section>
"""

    meta = (
        '<span><strong>Date:</strong> 04 May 2026</span>'
        '<span><strong>Status:</strong> Draft</span>'
        '<span><strong>Contributors:</strong> Antonio, Lefteris, Jorge, Patricija, Cesc, Stijn, Samantha, Radovan</span>'
    )

    html_text = page(
        title="NTH Bootcamp - Plan",
        eyebrow="NTH / D-Bootcamp",
        h1_html="NTH Bootcamp <span style='color:var(--muted-2);font-weight:500'>plan</span>",
        lede="Internal plan for the leads. Five modules from camera to closed loop, one open hour, one demo upload.",
        meta_html=meta,
        toc_html=toc,
        body_html=body,
    )
    (BOOTCAMP_DIR / "bootcamp-plan.html").write_text(html_text, encoding="utf-8")


# --- module stubs -----------------------------------------------------------

MODULE_CONTENT = {
    "M1-computer-vision.html": dict(
        eyebrow="NTH / M1",
        h1='Computer vision',
        lead="lefteris",
        lede="Image input and preprocessing. YOLO for segmentation, OpenCV for edge detection. The first stage of the pipeline - what the prosthesis sees before any gaze logic kicks in.",
        sections=[
            ("01", "concept",    "Concept",
             "What this module covers and how it feeds the rest of the pipeline."),
            ("02", "inputs",     "Inputs &amp; outputs",
             "Image format conventions used throughout the bootcamp. Default size, default source image, what an activation map is."),
            ("03", "yolo",       "YOLO segmentation",
             "Pretrained YOLO segmentation on a scene. Object masks as candidate activation regions."),
            ("04", "opencv",     "OpenCV edge detection",
             "Sobel, Canny, threshold. When each is appropriate."),
            ("05", "exercise",   "Guided exercise",
             "Run YOLO segmentation and OpenCV edge detection on the same scene; compare the resulting activation maps."),
            ("06", "extensions", "Extensions",
             "Webcam input, batched preprocessing, custom edge operators, open-vocabulary detection."),
        ],
    ),
    "M2-deepgaze-and-gaze.html": dict(
        eyebrow="NTH / M2",
        h1='Gaze <span style="color:var(--muted-2);font-weight:500">&amp; DeepGaze</span>',
        lead="lefteris",
        lede="DeepGaze III scanpath model plus our extra gaze statistics and dynamics simulation. Simulated gaze as a proxy for where a prosthesis user would explore the scene.",
        sections=[
            ("01", "concept",    "Concept",
             "Why gaze matters for a prosthesis user. Saliency vs scanpath. Fixation history."),
            ("02", "deepgaze",   "DeepGaze III",
             "Pretrained model. Centerbias and fixation-history tensors. Sampling the next fixation from the log-density."),
            ("03", "trajectory", "Sampling a trajectory",
             "Looping the next-fixation sampler to build a multi-step scanpath."),
            ("04", "stats",      "Extra gaze statistics &amp; dynamics",
             "Layer added on top of DeepGaze III - distributions, dwell times, saccade dynamics."),
            ("05", "exercise",   "Guided exercise",
             "Sample a DeepGaze III scanpath and overlay the extra statistics and dynamics."),
            ("06", "extensions", "Extensions",
             "Custom centerbias, real eye-tracking input, gaze jitter modeling."),
        ],
    ),
    "M3-neuromod-and-stim.html": dict(
        eyebrow="NTH / M3 - Interactive companion",
        h1='Neuromodulation <span style="color:var(--muted-2);font-weight:500">&amp; stimulation</span>',
        lead="antonio",
        status="alpha",
        lede=("How a cortical prosthesis turns numbers into neuronal firing. "
              "Three live playgrounds &mdash; one biphasic pulse, one Utah-array configuration table, "
              "one real-time stimulator with safety chips and a cumulative-charge readout &mdash; let you build intuition "
              "before (or alongside) the notebook."),
        sections=[
            ("01", "concept",     "What is neuromodulation",
             "Neuromodulation is the act of choosing stimulation parameters that push neuronal firing in a chosen direction. "
             "The two main levers are <strong>amplitude modulation</strong> (more current per pulse recruits more tissue around the electrode &mdash; the radius of activated fibres grows roughly as &radic;(I/K)) "
             "and <strong>frequency modulation</strong> (more pulses per second means the recruited neurons are <em>driven</em> harder &mdash; but only up to the <strong>refractory ceiling</strong>: an axon can fire at most once per ~1&nbsp;ms absolute and ~5&nbsp;ms relative refractory period, so above ~200&ndash;300&nbsp;Hz the per-pulse recruitment probability falls off and the driven firing rate plateaus or even drops). "
             "Higher stim frequency is therefore not the same as a higher firing rate &mdash; only a higher <em>opportunity</em> to fire. "
             "Everything else &mdash; pulse width, interphase gap, number of pulses &mdash; shapes the train under those two levers."),
            ("02", "params",      "The five pulse parameters",
             "For a conventional rectangular, charge-balanced, biphasic pulse train on a single electrode, five numbers cover the geometry. "
             "Click the tabs below to isolate each one and see its effect. "
             "Real systems also vary pulse shape (asymmetric biphasic, triphasic, slow charge-recovery), waveform (non-rectangular ramps), and <strong>train period</strong> &mdash; the start-to-start interval between trains, which we expose in the simulator below."),
            ("03", "array",       "Configure a Utah array",
             "Research and early-clinical cortical arrays today drive anywhere from a handful to a few hundred electrodes &mdash; the Utah array used here has 96 shanks on a 10&times;10 grid; future high-density systems aim for thousands. "
             "Pick electrodes on the 10&times;10 array, tune the draft train in the middle, "
             "<strong>Add to list</strong> to commit them with their own parameters. "
             "Click a row to bring it back into the draft for editing."),
            ("04", "neurolight",  "Run the stimulator",
             "Once channels are configured, the Neurolight session walks through <em>configure</em> &rarr; <em>connect</em> &rarr; <em>stim</em> &rarr; <em>disconnect</em>. "
             "Press <em>Stim</em> to fire one finite trial (<code>reps</code> trains, each repeated every <code>train period</code> milliseconds, so trains of different lengths stay phase-locked) and watch the four live panels update in real time. "
             "All four can be read at a glance: <em>where</em> firing is happening (array), <em>when</em> it happens (carousel), <em>how safe</em> the parameters are (current limit + Shannon-k), and <em>how much</em> charge has been delivered so far (peak current per channel + cumulative charge trace)."),
            ("05", "self-check",  "Self-check",
             "Predict the answer first, then verify with the sliders or the live panels above."),
            ("06", "next",        "Where to next",
             "On to M4 &mdash; phosphenes &mdash; where these stimulation parameters become a perceived image. The notebook is an optional, self-guided way to revisit this material in Python."),
            ("07", "refs",        "Tools &amp; references",
             "The tools, papers, and APIs this module is built on."),
        ],
        extras={"concept": "M3_CONCEPT", "params": "STIM_DEMO", "array": "ARRAY_DEMO",
                "neurolight": "STIM_FLOW", "self-check": "M3_SELFCHECK",
                "next": "M3_NEXT", "refs": "M3_REFS"},
        footer=("NTH bootcamp &middot; M3 &middot; "
                '<a href="../bootcamp-plan.html">back to plan</a> &middot; '
                '<a href="M4-phosphene-simulation.html">next: M4 &rarr;</a> '
                "&middot; safety helpers implemented in vanilla JS below, no Python required."),
    ),
    "M4-phosphene-simulation.html": dict(
        eyebrow="NTH / M4",
        h1='Phosphene simulation',
        lead="lefteris",
        lede="Dynaphos phosphene maps, stimulation-to-phosphene conversion, and temporal dynamics. How a stimulus tensor becomes a perceived image. Dynaphos and dynaphos-experiments can be used and modified.",
        sections=[
            ("01", "concept",    "Concept",
             "What a phosphene basis map is. How overlapping receptive fields constrain the achievable percept."),
            ("02", "maps",       "Phosphene maps",
             "Individual basis maps and electrode centers."),
            ("03", "forward",    "Stimulation -> phosphenes",
             "End-to-end forward pass: activation_mask -> sample_stimulus -> GaussianSimulator -> phosphene canvas."),
            ("04", "temporal",   "Temporal dynamics",
             "Reset-per-frame vs state-preserving sequences. Brightness buildup and fade."),
            ("05", "exercise",   "Guided exercise",
             "Use Dynaphos to convert a stimulation pattern into a phosphene render; observe the temporal dynamics."),
            ("06", "extensions", "Extensions",
             "Custom electrode density, gaze jitter, electrode dropout - short sweeps over the same forward pass."),
        ],
    ),
    "M5-decoding-and-closed-loop.html": dict(
        eyebrow="NTH / M5",
        h1='Decoding <span style="color:var(--muted-2);font-weight:500">&amp; closed loop</span>',
        lead="antonio",
        lede="Pretrained decoder demo first, then train your own. End-to-end co-optimization through the differentiable simulator, and the minimal closed-loop demo.",
        sections=[
            ("01", "concept",    "Concept",
             "Why decoders close the loop. The basic question all closed-loop neurotech rests on: did stimulating channel X move my downstream metric?"),
            ("02", "pretrained", "Pretrained decoder",
             "Load a pretrained model and run it on phosphene canvases - see what a trained decoder recovers before you train your own."),
            ("03", "train",      "Train your own decoder",
             "Toy brightness decoder first; (stretch) train a small CNN on a few phosphene canvases."),
            ("04", "e2e",        "End-to-end co-optimization",
             "Dynaphos is fully differentiable. Train a learnable preprocessor and decoder jointly through the frozen simulator."),
            ("05", "closed",     "Minimal closed-loop demo",
             "Image -> gaze -> crop -> preprocessing -> stimulation -> phosphenes -> decoder -> feedback. One integrated figure."),
            ("06", "exercise",   "Guided exercise",
             "Run the pretrained decoder on phosphene canvases, then train your own toy decoder on a small batch."),
        ],
    ),
}


# --- Utah array multi-electrode demo (M3) ----------------------------------

ARRAY_DEMO_HTML = r"""
<div class='array-demo' id='array-demo'>
  <div class='array-body'>

    <!-- LEFT: array -->
    <div>
      <div class='array-panel-h'>10 x 10 Utah array</div>

      <div class='array-svg-wrap' id='ad-wrap'>
        <svg id='ad-svg' viewBox='0 0 320 320' aria-label='Utah array selector'></svg>
      </div>

      <div class='array-actions'>
        <button id='ad-all'>Select all</button>
        <button id='ad-none'>Clear selection</button>
        <span class='sel-count' id='ad-count'>0 selected &middot; 0 configured</span>
      </div>
      <p class='mono' style='font-size:11px;color:var(--muted);margin-top:10px;line-height:1.5'>
        click toggles an electrode &middot; drag paints (first electrode's state decides whether the drag selects or deselects)
      </p>
    </div>

    <!-- MIDDLE: draft train -->
    <div>
      <div class='array-panel-h'>Draft train
        <span class='ad-live-tag' id='ad-live-tag'>0 electrodes ready</span>
      </div>

      <div class='ad-preview' id='ad-preview'>
        <svg id='ad-preview-svg' viewBox='0 0 380 160' aria-label='Draft train preview'></svg>
      </div>

      <div class='array-params'>
        <label for='ad-amp'>amplitude</label>
        <input id='ad-amp' type='range' min='10'  max='200' step='5'  value='80'>
        <span class='v' id='ad-amp-v'>80 &micro;A</span>

        <label for='ad-pw'>pulse width</label>
        <input id='ad-pw'  type='range' min='50'  max='500' step='10' value='170'>
        <span class='v' id='ad-pw-v'>170 &micro;s</span>

        <label for='ad-ip'>interphase</label>
        <input id='ad-ip'  type='range' min='0'   max='200' step='5'  value='40'>
        <span class='v' id='ad-ip-v'>40 &micro;s</span>

        <label for='ad-fr'>frequency</label>
        <input id='ad-fr'  type='range' min='10'  max='300' step='5'  value='300'>
        <span class='v' id='ad-fr-v'>300 Hz</span>

        <label for='ad-np'>num pulses</label>
        <input id='ad-np'  type='range' min='1'   max='100' step='1'  value='50'>
        <span class='v' id='ad-np-v'>50</span>
      </div>

      <div class='ad-commit'>
        <button class='primary' id='ad-add'>Add to list →</button>
        <button id='ad-surprise' title='Random electrodes + params. Configure / Connect / Stim to run.'>Surprise me</button>
        <span class='ad-hint' id='ad-add-hint'>select electrodes first</span>
        <span class='ad-hint' id='surprise-hint'></span>
      </div>
    </div>

    <!-- RIGHT: committed list -->
    <div>
      <div class='array-panel-h'>
        <span>Configured electrodes</span>
        <button class='added-clear' id='ad-clear-list' title='Remove all'>clear</button>
      </div>
      <div class='array-trains' id='ad-list'>
        <div class='empty'>nothing configured yet &middot; pick electrodes, tune the draft, then add</div>
      </div>
    </div>

  </div>
</div>

<script>
(function(){
  const root = document.getElementById('array-demo');
  if(!root) return;
  const NS = 'http://www.w3.org/2000/svg';
  const COLS = 10, ROWS = 10, N = COLS*ROWS;

  const svg = root.querySelector('#ad-svg');
  const countEl = root.querySelector('#ad-count');
  const listEl = root.querySelector('#ad-list');
  const liveTag = root.querySelector('#ad-live-tag');
  const addBtn = root.querySelector('#ad-add');
  const addHint = root.querySelector('#ad-add-hint');
  const previewSvg = root.querySelector('#ad-preview-svg');

  // STATE
  // selected:  which electrodes the user has currently picked (intent)
  // committed: array length N; null = not configured; object = committed params
  const selected = new Set();
  const committed = new Array(N).fill(null);


  // sliders
  const s = {
    amp: root.querySelector('#ad-amp'),
    pw:  root.querySelector('#ad-pw'),
    ip:  root.querySelector('#ad-ip'),
    fr:  root.querySelector('#ad-fr'),
    np:  root.querySelector('#ad-np')
  };
  const sv = {
    amp: root.querySelector('#ad-amp-v'),
    pw:  root.querySelector('#ad-pw-v'),
    ip:  root.querySelector('#ad-ip-v'),
    fr:  root.querySelector('#ad-fr-v'),
    np:  root.querySelector('#ad-np-v')
  };

  function currentParams(){
    return { amp:+s.amp.value, pw:+s.pw.value, ip:+s.ip.value, fr:+s.fr.value, np:+s.np.value };
  }
  function fmtSliders(){
    const v = currentParams();
    sv.amp.innerHTML = v.amp + ' &micro;A';
    sv.pw.innerHTML  = v.pw  + ' &micro;s';
    sv.ip.innerHTML  = v.ip  + ' &micro;s';
    sv.fr.textContent = v.fr + ' Hz';
    sv.np.textContent = v.np;
  }
  function setSliders(p){
    s.amp.value = p.amp; s.pw.value = p.pw; s.ip.value = p.ip;
    s.fr.value  = p.fr;  s.np.value = p.np;
    fmtSliders();
  }

  // --- build array svg ---
  // bigger viewBox => bigger dots, room for in-dot numbers
  const VB = 320, PAD = 14;
  const cell = (VB - 2*PAD) / COLS;             // ~29.2
  const rDot = cell * 0.46;                     // larger dot

  for(let i=0;i<=COLS;i++){
    const x = PAD + cell*i;
    const ln = document.createElementNS(NS,'line');
    ln.setAttribute('x1', x); ln.setAttribute('x2', x);
    ln.setAttribute('y1', PAD); ln.setAttribute('y2', VB-PAD);
    ln.setAttribute('stroke', '#ebe9e2'); ln.setAttribute('stroke-width','0.5');
    svg.appendChild(ln);
  }
  for(let i=0;i<=ROWS;i++){
    const y = PAD + cell*i;
    const ln = document.createElementNS(NS,'line');
    ln.setAttribute('x1', PAD); ln.setAttribute('x2', VB-PAD);
    ln.setAttribute('y1', y); ln.setAttribute('y2', y);
    ln.setAttribute('stroke', '#ebe9e2'); ln.setAttribute('stroke-width','0.5');
    svg.appendChild(ln);
  }
  const box = document.createElementNS(NS,'rect');
  box.setAttribute('x', PAD); box.setAttribute('y', PAD);
  box.setAttribute('width', VB-2*PAD); box.setAttribute('height', VB-2*PAD);
  box.setAttribute('fill','none'); box.setAttribute('stroke','#d8d6cf');
  svg.appendChild(box);

  // electrode dots + numbers (1..100, row-major)
  const dots = [];
  const labels = [];
  for(let row=0; row<ROWS; row++){
    for(let c=0; c<COLS; c++){
      const i = row*COLS + c;
      const cx = PAD + cell*(c+0.5);
      const cy = PAD + cell*(row+0.5);
      const dot = document.createElementNS(NS,'circle');
      dot.setAttribute('cx', cx);
      dot.setAttribute('cy', cy);
      dot.setAttribute('r', rDot);
      dot.setAttribute('data-idx', i);
      dot.classList.add('e');
      svg.appendChild(dot);
      dots.push(dot);

      const tx = document.createElementNS(NS,'text');
      tx.setAttribute('x', cx);
      tx.setAttribute('y', cy + 3);
      tx.setAttribute('text-anchor', 'middle');
      tx.setAttribute('font-family', 'JetBrains Mono, monospace');
      tx.setAttribute('font-size', '8.5');
      tx.setAttribute('font-weight', '500');
      tx.setAttribute('pointer-events', 'none');
      tx.textContent = (i+1);
      svg.appendChild(tx);
      labels.push(tx);
    }
  }

  function paintDots(){
    dots.forEach((d,i) => {
      const isSel = selected.has(i);
      const isOn  = committed[i] != null;
      if(isSel && isOn){
        d.setAttribute('fill', '#d86f91');
        d.setAttribute('stroke', '#a83f63');
        d.setAttribute('stroke-width','1.4');
        labels[i].setAttribute('fill', '#fff');
      } else if(isSel){
        d.setAttribute('fill', '#fde7ef');
        d.setAttribute('stroke', '#a83f63');
        d.setAttribute('stroke-width','1.4');
        labels[i].setAttribute('fill', '#a83f63');
      } else if(isOn){
        d.setAttribute('fill', '#1c1c1a');
        d.setAttribute('stroke', '#1c1c1a');
        d.setAttribute('stroke-width','0.6');
        labels[i].setAttribute('fill', '#fff');
      } else {
        d.setAttribute('fill', '#fff');
        d.setAttribute('stroke', '#9a9a93');
        d.setAttribute('stroke-width','0.6');
        labels[i].setAttribute('fill', '#9a9a93');
      }
    });
    const configured = committed.reduce((a,p) => a + (p?1:0), 0);
    countEl.textContent = selected.size + ' selected · ' + configured + ' configured';

    // live tag and add button readiness
    const n = selected.size;
    liveTag.textContent = n === 0 ? '0 electrodes ready'
                        : (n === 1 ? '1 electrode ready' : n + ' electrodes ready');
    liveTag.classList.toggle('hot', n > 0);
    addBtn.disabled = (n === 0);
    addHint.textContent = (n === 0)
      ? 'select electrodes first'
      : 'will add ' + n + ' row' + (n>1?'s':'') + ' to the list';
  }

  // click toggles; drag = paint with mode chosen from the first electrode under the mouse
  let dragging = false;
  let dragMode = null;    // 'select' | 'deselect' | null (= unset, first hit decides)
  let lastIdx = -1;

  function dotIndexAtClientPoint(evt){
    const el = document.elementFromPoint(evt.clientX, evt.clientY);
    if(el && el.classList && el.classList.contains('e')){
      return +el.getAttribute('data-idx');
    }
    return -1;
  }
  function actOn(i){
    if(i < 0 || i === lastIdx) return;
    lastIdx = i;
    if(dragMode === null){
      // first hit: mode = opposite of current state, AND apply it
      dragMode = selected.has(i) ? 'deselect' : 'select';
    }
    if(dragMode === 'select') selected.add(i);
    else                       selected.delete(i);
    paintDots();
  }
  svg.addEventListener('mousedown', (e) => {
    e.preventDefault();
    const i = dotIndexAtClientPoint(e);
    if(i < 0) return;
    dragging = true; dragMode = null; lastIdx = -1;
    actOn(i);
  });
  window.addEventListener('mousemove', (e) => {
    if(!dragging) return;
    const i = dotIndexAtClientPoint(e);
    if(i >= 0) actOn(i);
  });
  window.addEventListener('mouseup', () => { dragging = false; dragMode = null; lastIdx = -1; });
  // touch
  svg.addEventListener('touchstart', (e) => {
    if(!e.touches.length) return;
    const i = dotIndexAtClientPoint(e.touches[0]);
    if(i < 0) return;
    e.preventDefault();
    dragging = true; dragMode = null; lastIdx = -1;
    actOn(i);
  }, { passive: false });
  window.addEventListener('touchmove', (e) => {
    if(!dragging || !e.touches.length) return;
    const i = dotIndexAtClientPoint(e.touches[0]);
    if(i >= 0) actOn(i);
  }, { passive: true });
  window.addEventListener('touchend', () => { dragging = false; dragMode = null; lastIdx = -1; });

  // bulk select actions
  root.querySelector('#ad-all').addEventListener('click', () => {
    for(let i=0;i<N;i++) selected.add(i);
    paintDots();
  });
  root.querySelector('#ad-none').addEventListener('click', () => {
    selected.clear();
    paintDots();
  });
  // clear the committed list (right panel)
  root.querySelector('#ad-clear-list').addEventListener('click', () => {
    for(let i=0;i<N;i++) committed[i] = null;
    paintDots(); renderList();
  });

  // --- live preview of the draft train (single waveform) ---
  function renderPreview(){
    const v = currentParams();
    const W = 380;
    const ampMax = 200;

    // helper: render a biphasic train into a given SVG box (top, bottom)
    function emitPanel(top, bottom, xMaxMs, label){
      const padL = 8, padR = 6;
      const plotW = W - padL - padR;
      const innerTop = top + 6;
      const innerBot = bottom - 18;       // leave room for x-axis label
      const plotH = innerBot - innerTop;
      const midY = innerTop + plotH/2;
      function xs(ms){ return padL + (ms / xMaxMs) * plotW; }
      function ys(uA){ return midY - (uA / ampMax) * (plotH/2 * 0.9); }
      let s = '';
      // panel border
      s += '<rect x="'+padL+'" y="'+innerTop+'" width="'+plotW+'" height="'+plotH+
           '" fill="#ffffff" stroke="#ebe9e2"/>';
      // baseline
      s += '<line x1="'+padL+'" x2="'+(padL+plotW)+'" y1="'+midY+'" y2="'+midY+
           '" stroke="#9a9a93" stroke-width="0.6" stroke-dasharray="2 3"/>';
      // x-axis label
      s += '<text x="'+(padL+plotW-2)+'" y="'+(bottom-4)+'" text-anchor="end" '+
           'font-family="JetBrains Mono, monospace" font-size="9" fill="#6c6c66">'+
           xMaxMs.toFixed(2)+' ms</text>';
      // small panel label top-left
      s += '<text x="'+(padL+4)+'" y="'+(innerTop+11)+'" '+
           'font-family="JetBrains Mono, monospace" font-size="9" fill="#a83f63" '+
           'letter-spacing="0.04em">'+label+'</text>';

      const periodMs = 1000 / v.fr;
      const phaseMs = v.pw / 1000;
      const ipMs    = v.ip / 1000;
      for(let i = 0; i < v.np; i++){
        const t0 = i*periodMs;
        if(t0 > xMaxMs) break;
        const cs = t0, ce = t0 + phaseMs;
        const as = ce + ipMs, ae = as + phaseMs;
        if(cs > xMaxMs) break;
        // cathodic (down) filled
        s += '<rect x="'+xs(cs)+'" y="'+midY+
             '" width="'+(xs(Math.min(ce,xMaxMs)) - xs(cs))+
             '" height="'+(ys(-v.amp) - midY)+
             '" fill="#1c1c1a" stroke="#1c1c1a" stroke-width="0.6"/>';
        if(ipMs > 0 && ce < xMaxMs){
          s += '<line x1="'+xs(ce)+'" x2="'+xs(Math.min(as,xMaxMs))+
               '" y1="'+midY+'" y2="'+midY+'" stroke="#9a9a93" stroke-width="1"/>';
        }
        if(as < xMaxMs){
          // anodic (up) filled
          s += '<rect x="'+xs(as)+'" y="'+ys(v.amp)+
               '" width="'+(xs(Math.min(ae,xMaxMs)) - xs(as))+
               '" height="'+(midY - ys(v.amp))+
               '" fill="#d86f91" stroke="#a83f63" stroke-width="0.6"/>';
        }
      }
      return s;
    }

    // Panel A: full train (top half of the svg, 0..76)
    const periodMs = 1000 / v.fr;
    const phaseMs = v.pw / 1000;
    const ipMs    = v.ip / 1000;
    const trainMs = Math.max(2*phaseMs + ipMs, (v.np-1)*periodMs + 2*phaseMs + ipMs);
    const fullXmax = trainMs * 1.05 + 0.05;
    // Panel B: zoomed first pulse (bottom half, 80..160)
    const onePulseMs = 2*phaseMs + ipMs;
    const zoomXmax = Math.max(onePulseMs * 1.6, 0.5);

    let out = '';
    out += emitPanel(0,   76,  fullXmax, 'FULL TRAIN ('+v.np+' pulses)');
    out += emitPanel(80, 160,  zoomXmax, 'ONE PULSE (zoomed)');
    previewSvg.innerHTML = out;
  }

  // slider changes: re-fmt + redraw preview, that's it
  Object.values(s).forEach(el => el.addEventListener('input', () => {
    fmtSliders(); renderPreview();
  }));
  fmtSliders();
  renderPreview();

  // --- ADD: commit current draft to selected electrodes ---
  addBtn.addEventListener('click', () => {
    if(selected.size === 0) return;
    const v = currentParams();
    selected.forEach(i => { committed[i] = Object.assign({}, v); });
    // deselect after commit so the user can pick a new set without losing context
    selected.clear();
    paintDots(); renderList();
  });

  // --- SURPRISE ME: random electrodes + per-electrode params, auto-run lifecycle ---
  const surpriseBtn = root.querySelector('#ad-surprise');
  function randInt(lo, hi){ return Math.floor(Math.random() * (hi - lo + 1)) + lo; }
  function randStep(lo, hi, step){
    const n = Math.floor((hi - lo) / step) + 1;
    return lo + step * Math.floor(Math.random() * n);
  }
  function randomParams(){
    return {
      amp: randStep(40, 160, 5),     // sensible amps, avoid the safety edge by default
      pw:  randStep(80, 300, 10),
      ip:  randStep(0,  100, 5),
      fr:  randStep(60, 300, 10),
      np:  randInt(5, 60)
    };
  }
  surpriseBtn.addEventListener('click', () => {
    // refuse if the lifecycle isn't at idle (configure must be available)
    const fd0 = document.getElementById('flow-demo');
    const cfgBtn0 = fd0 && fd0.querySelector('#fd-btn-configure');
    if(cfgBtn0 && cfgBtn0.disabled){
      surpriseBtn.classList.add('shake');
      setTimeout(() => surpriseBtn.classList.remove('shake'), 400);
      return;
    }
    // 1) clear current selection + committed
    selected.clear();
    for(let i=0;i<N;i++) committed[i] = null;
    // 2) pick a random count of electrodes, distinct indices
    const count = randInt(6, 20);
    const all = Array.from({length: N}, (_, i) => i);
    // Fisher-Yates partial shuffle
    for(let i = 0; i < count; i++){
      const j = i + Math.floor(Math.random() * (N - i));
      [all[i], all[j]] = [all[j], all[i]];
    }
    const picks = all.slice(0, count).sort((a,b) => a-b);
    picks.forEach(i => { committed[i] = randomParams(); });
    // also reflect the first pick's params in the draft so users can see them
    setSliders(committed[picks[0]]);
    // refresh visuals
    paintDots();
    renderList();
    renderPreview();
    // 3) populate-only: do NOT auto-run the lifecycle. The reviewer flagged
    // auto-start as un-intuitive; leave the stimulator in its current state
    // and surface a hint near the surprise button so users know what's next.
    surpriseBtn.classList.add('flash-hint');
    setTimeout(() => surpriseBtn.classList.remove('flash-hint'), 1400);
    const hintEl = document.getElementById('surprise-hint');
    if(hintEl){
      hintEl.textContent = 'Loaded ' + picks.length + ' random channels. Configure / Connect / Stim when ready.';
      hintEl.classList.add('on');
      setTimeout(() => hintEl.classList.remove('on'), 4500);
    }
  });

  // --- list / trains ---
  function trainDurationMs(v){
    const periodMs = 1000 / v.fr;
    const pulseMs = (2*v.pw + v.ip) / 1000;
    return Math.max(pulseMs, (v.np - 1) * periodMs + pulseMs);
  }
  function makeTrainSvg(v){
    const W = 360, H = 36;
    const padL = 6, padR = 4, padT = 4, padB = 4;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const midY = padT + plotH/2;
    const xMaxMs = trainDurationMs(v) * 1.1 + 0.5;
    const ampMax = 200;
    function xs(ms){ return padL + (ms / xMaxMs) * plotW; }
    function ys(uA){ return midY - (uA / ampMax) * (plotH/2 * 0.85); }

    let out = '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">';
    out += '<line x1="' + padL + '" x2="' + (padL+plotW) + '" y1="' + midY + '" y2="' + midY +
           '" stroke="#9a9a93" stroke-width="0.6" stroke-dasharray="2 3"/>';

    const periodMs = 1000 / v.fr;
    const phaseMs = v.pw / 1000;
    const ipMs    = v.ip / 1000;
    for(let i=0; i<v.np; i++){
      const t0 = i * periodMs;
      const cs = t0, ce = t0 + phaseMs;
      const as = ce + ipMs, ae = as + phaseMs;
      // cathodic filled - grows downward from baseline
      out += '<rect x="' + xs(cs) + '" y="' + midY +
             '" width="' + (xs(ce) - xs(cs)) +
             '" height="' + (ys(-v.amp) - midY) +
             '" fill="#1c1c1a" stroke="#1c1c1a" stroke-width="0.5"/>';
      if(ipMs > 0){
        out += '<line x1="' + xs(ce) + '" x2="' + xs(as) + '" y1="' + midY + '" y2="' + midY +
               '" stroke="#9a9a93" stroke-width="0.8"/>';
      }
      // anodic filled - grows upward from baseline
      out += '<rect x="' + xs(as) + '" y="' + ys(v.amp) +
             '" width="' + (xs(ae) - xs(as)) +
             '" height="' + (midY - ys(v.amp)) +
             '" fill="#d86f91" stroke="#a83f63" stroke-width="0.5"/>';
    }
    out += '</svg>';
    return out;
  }
  function labelFor(i){
    const c = i % COLS, r = Math.floor(i / COLS);
    return 'r' + String(r+1).padStart(2,'0') + 'c' + String(c+1).padStart(2,'0');
  }
  function paramSummary(p){
    return p.amp + ' µA · ' + p.pw + ' µs · ' +
           p.fr + ' Hz · ' + p.np + 'p';
  }

  const MAX_ROWS = 24;
  function renderList(){
    const configured = [];
    for(let i=0;i<N;i++) if(committed[i] != null) configured.push(i);
    if(configured.length === 0){
      listEl.innerHTML = '<div class="empty">nothing configured yet · pick electrodes, tune the draft, then add</div>';
      return;
    }
    const shown = configured.slice(0, MAX_ROWS);
    let html = '';
    shown.forEach(i => {
      const isSel = selected.has(i);
      const pAttr = JSON.stringify(committed[i]).replace(/"/g, '&quot;');
      html += '<div class="row added' + (isSel ? ' on' : '') +
              '" data-i="' + i + '" data-params="' + pAttr +
              '" tabindex="0" role="button" title="click to edit · × to remove">' +
              '<span class="label">e' + String(i+1).padStart(3,'0') + '</span>' +
              '<span class="summary">' + paramSummary(committed[i]) + '</span>' +
              makeTrainSvg(committed[i]) +
              '<button class="rm" aria-label="remove">×</button>' +
              '</div>';
    });
    if(configured.length > MAX_ROWS){
      html += '<div class="more">+ ' + (configured.length - MAX_ROWS) + ' more configured (not shown)</div>';
    }
    listEl.innerHTML = html;
    // bind row interactions
    listEl.querySelectorAll('.row.added').forEach(rowEl => {
      const i = +rowEl.dataset.i;
      rowEl.querySelector('.rm').addEventListener('click', (e) => {
        e.stopPropagation();
        committed[i] = null;
        selected.delete(i);
        paintDots(); renderList();
      });
      // click row body: load its params into the draft and select that electrode
      rowEl.addEventListener('click', () => {
        setSliders(committed[i]);
        selected.clear();
        selected.add(i);
        renderPreview();
        paintDots(); renderList();
      });
    });
  }

  paintDots();
  renderList();
})();
</script>
"""


# --- stimulator lifecycle + train-of-trains (M3) ---------------------------

STIM_FLOW_HTML = r"""
<div class='flow-demo conductor' id='flow-demo'>

  <!-- HEADER: lifecycle pill + state + clock + Surprise me proxy -->
  <div class='cond-header'>
    <div class='cond-pills' role='group' aria-label='Lifecycle steps'>
      <button class='cond-pill armed' data-step='0' id='fd-btn-configure'>
        <span class='n'>1</span><span class='lbl'>Configure</span>
      </button>
      <span class='cond-arrow'>&rsaquo;</span>
      <button class='cond-pill' data-step='1' id='fd-btn-connect' disabled>
        <span class='n'>2</span><span class='lbl'>Connect</span>
      </button>
      <span class='cond-arrow'>&rsaquo;</span>
      <button class='cond-pill' data-step='2' id='fd-btn-stim' disabled>
        <span class='n'>3</span><span class='lbl'>Stim</span>
      </button>
      <span class='cond-arrow'>&rsaquo;</span>
      <button class='cond-pill' data-step='3' id='fd-btn-disconnect' disabled>
        <span class='n'>4</span><span class='lbl'>Disconnect</span>
      </button>
    </div>
    <span class='cond-state' id='fd-state'>idle</span>
    <span class='cond-clock' id='fd-clock' title='wall clock'>00:00.000</span>
    <a href='#ad-surprise' class='cond-link' title='Jump to the Surprise me button (§03)'>Surprise me &uarr;</a>
  </div>

  <!-- 2x2 quad of live elements -->
  <div class='cond-quad'>

    <!-- TL: Utah-live (spatial / instant) -->
    <div class='cond-cell cond-utah'>
      <div class='cond-h'>
        <span>Array activity</span>
        <span class='cond-tag'>spatial &middot; live</span>
        <span class='cond-sub' id='fd-utah-sub'>idle</span>
      </div>
      <div class='cond-utah-body'>
        <svg id='fd-utah-svg' viewBox='0 0 200 200' aria-label='Live Utah array activity' preserveAspectRatio='xMidYMid meet'></svg>
      </div>
    </div>

    <!-- TR: Carousel (temporal / history) -->
    <div class='cond-cell cond-strip'>
      <div class='cond-h'>
        <span>Stimulator output</span>
        <span class='cond-tag'>temporal &middot; channels &times; time</span>
        <span class='cond-sub' id='fd-summary'>configure to allocate channels</span>
      </div>
      <div class='cond-strip-body'>
        <svg id='fd-strip-svg' viewBox='0 0 1000 300' aria-label='Real-time stimulator carousel' preserveAspectRatio='none'></svg>
      </div>
    </div>

    <!-- BL: Safety (instant summary) -->
    <div class='cond-cell cond-safety'>
      <div class='cond-h'>
        <span>Safety &amp; charge</span>
        <span class='cond-tag'>summary</span>
        <span class='cond-sub'>A = 2000 &micro;m<sup>2</sup> per electrode</span>
      </div>
      <div class='cond-safety-grid' id='fd-safety'>
        <div class='fd-metric'>
          <div class='fd-metric-h'>charge / phase</div>
          <div class='fd-metric-v' id='fd-mx-Q'>&mdash;</div>
          <div class='fd-metric-sub'>amp &times; pw</div>
        </div>
        <div class='fd-metric'>
          <div class='fd-metric-h'>charge density</div>
          <div class='fd-metric-v' id='fd-mx-Qd'>&mdash;</div>
          <div class='fd-metric-sub'>Q / area</div>
        </div>
        <div class='fd-metric'>
          <div class='fd-metric-h'>Shannon k</div>
          <div class='fd-metric-v' id='fd-mx-K'>&mdash;</div>
          <div class='fd-metric-sub'>limit 1.85</div>
        </div>
        <div class='fd-metric'>
          <div class='fd-metric-h'>duty cycle</div>
          <div class='fd-metric-v' id='fd-mx-D'>&mdash;</div>
          <div class='fd-metric-sub'>2&middot;pw&middot;fr</div>
        </div>
        <div class='fd-metric'>
          <div class='fd-metric-h'>avg current</div>
          <div class='fd-metric-v' id='fd-mx-I'>&mdash;</div>
          <div class='fd-metric-sub'>amp &times; duty</div>
        </div>
        <div class='fd-metric live'>
          <div class='fd-metric-h'>cumulative charge</div>
          <div class='fd-metric-v' id='fd-mx-P'>0.000 &micro;C</div>
          <div class='fd-metric-sub'>since stim start</div>
        </div>
      </div>
      <div class='fd-safety-warn' id='fd-safety-warn'></div>
    </div>

    <!-- BR: cumulative-charge trace -->
    <div class='cond-cell cond-power'>
      <div class='cond-h'>
        <span>Cumulative charge trace</span>
        <span class='cond-tag'>analytic, all channels</span>
        <span class='cond-sub' id='fd-power-now'>0.000 &micro;C</span>
      </div>
      <div class='cond-power-body'>
        <svg id='fd-power-svg' viewBox='0 0 1000 180' aria-label='Cumulative charge live chart' preserveAspectRatio='none'></svg>
      </div>
    </div>

  </div>

  <!-- Controls: sliders + log toggle -->
  <div class='cond-controls'>
    <div class='cond-sliders'>
      <div class='cond-knob'>
        <label for='fd-iti' title='Start-to-start interval between successive trains. Trains of different lengths stay phase-locked across channels.'>train period</label>
        <input id='fd-iti' type='range' min='10' max='1200' step='10' value='400'>
        <span class='v' id='fd-iti-v'>400 ms</span>
      </div>
      <div class='cond-knob'>
        <label for='fd-reps'>train repetitions</label>
        <input id='fd-reps' type='range' min='1' max='10' step='1' value='1'>
        <span class='v' id='fd-reps-v'>1</span>
      </div>
      <div class='cond-knob'>
        <label for='fd-window'>window</label>
        <input id='fd-window' type='range' min='100' max='2000' step='50' value='1000'>
        <span class='v' id='fd-window-v'>1.0 s</span>
      </div>
    </div>
  </div>

  <!-- Log: collapsed by default -->
  <details class='cond-log-wrap'>
    <summary>
      <span>Stimulator log</span>
      <button class='added-clear' id='fd-log-clear' title='Clear log' type='button'>clear</button>
    </summary>
    <div class='fd-log' id='fd-log'>
      <div class='fd-log-row muted'><span class='ts'>--:--.---</span><span class='msg'>stimulator idle &middot; allocate channels then press Configure</span></div>
    </div>
  </details>

  <!-- Hidden lifecycle diagram SVG (kept for code reuse; no longer rendered visually).
       The 'nodes' set is still updated by JS so the pill row classes stay coherent
       through the existing setNodes() function. -->
  <svg id='fd-svg' style='display:none' aria-hidden='true' viewBox='0 0 360 200'>
    <g data-step='0' class='fd-node'></g>
    <g data-step='1' class='fd-node'></g>
    <g data-step='2' class='fd-node'></g>
    <g data-step='3' class='fd-node'></g>
  </svg>

</div>

<script>
(function(){
  const root = document.getElementById('flow-demo');
  if(!root) return;

  // ----- refs -----
  const stateEl = root.querySelector('#fd-state');
  const nodes = root.querySelectorAll('.fd-node');
  const logEl = root.querySelector('#fd-log');
  const logClearBtn = root.querySelector('#fd-log-clear');
  const clockEl = root.querySelector('#fd-clock');
  const stripSvg = root.querySelector('#fd-strip-svg');
  const summaryEl = root.querySelector('#fd-summary');
  const iti = root.querySelector('#fd-iti');
  const reps = root.querySelector('#fd-reps');
  const win = root.querySelector('#fd-window');
  const itiV = root.querySelector('#fd-iti-v');
  const repsV = root.querySelector('#fd-reps-v');
  const winV  = root.querySelector('#fd-window-v');

  const btn = {
    cfg:   root.querySelector('#fd-btn-configure'),
    conn:  root.querySelector('#fd-btn-connect'),
    stim:  root.querySelector('#fd-btn-stim'),
    disc:  root.querySelector('#fd-btn-disconnect')
  };
  const LIFECYCLE = ['configure', 'connect', 'stim', 'disconnect'];

  // safety metric refs
  const mx = {
    Q:  root.querySelector('#fd-mx-Q'),
    Qd: root.querySelector('#fd-mx-Qd'),
    K:  root.querySelector('#fd-mx-K'),
    D:  root.querySelector('#fd-mx-D'),
    I:  root.querySelector('#fd-mx-I'),
    P:  root.querySelector('#fd-mx-P')
  };
  const safetyWarn = root.querySelector('#fd-safety-warn');
  // simulator assumptions
  const ELECTRODE_AREA_CM2 = 2000e-8;   // 2000 um^2 -> 2e-5 cm^2
  const SHANNON_K_LIMIT = 1.85;

  // metric helpers (per channel). Q is per-phase charge in microcoulombs (uC),
  // which is the Shannon-convention unit; uA*us = pC, so /1e6 gives uC.
  function chargePerPhaseUc(p){ return (p.amp * p.pw) / 1e6; }                 // uA*us / 1e6 = uC
  function chargeDensityUcCm2(p){ return chargePerPhaseUc(p) / ELECTRODE_AREA_CM2; }  // uC/cm^2
  function shannonK(p){
    const Q  = chargePerPhaseUc(p);
    const Qd = chargeDensityUcCm2(p);
    if(Q <= 0 || Qd <= 0) return -Infinity;
    return Math.log10(Q) + Math.log10(Qd);
  }
  function dutyCycle(p){ return (2 * p.pw / 1e6) * p.fr; }                  // unitless 0..1
  function avgCurrentUa(p){ return p.amp * dutyCycle(p); }
  // Total charge delivered by one biphasic pulse from one channel, in uC.
  // Both cathodic and anodic phases count (each phase has |amp| * pw of charge).
  function chargePerPulseUc(p){ return 2 * chargePerPhaseUc(p); }

  // ----- session state -----
  let phase = -1;            // -1 idle, 0..3 in lifecycle
  let channels = [];          // [{i, params}] populated at CONFIGURE
  let runStartMs = null;      // wall time STIM started; null if not running
  let runEndMs = null;        // wall time STIM is scheduled to finish
  let stimRunning = false;
  let stimFinishTimer = null;

  // ----- helpers -----
  function trainDurationMs(v){
    const periodMs = 1000 / v.fr;
    const pulseMs = (2*v.pw + v.ip) / 1000;
    return Math.max(pulseMs, (v.np - 1) * periodMs + pulseMs);
  }
  // Longest train across all configured channels. Train length is per-channel,
  // but the repetition period must be global so trains stay phase-locked.
  function maxTrainMs(){
    let m = 0;
    channels.forEach(ch => { const d = trainDurationMs(ch.params); if(d > m) m = d; });
    return m;
  }
  // The effective train period: one global start-to-start interval, never
  // shorter than the longest train, so every train finishes before the next
  // repetition begins on any channel.
  function effectiveTrainPeriodMs(){
    return Math.max(+iti.value, maxTrainMs());
  }
  function fmtTime(ms){
    const m = Math.floor(ms / 60000);
    const s = Math.floor((ms % 60000) / 1000);
    const ms3 = Math.floor(ms % 1000);
    return String(m).padStart(2,'0') + ':' +
           String(s).padStart(2,'0') + '.' +
           String(ms3).padStart(3,'0');
  }
  function eLabel(i){ return 'e' + String(i+1).padStart(3,'0'); }
  function paramSummaryStr(p){
    return 'amp ' + p.amp + ' uA, pw ' + p.pw + ' us, ip ' + p.ip + ' us, ' +
           p.fr + ' Hz, ' + p.np + ' pulses/train';
  }

  // ----- log -----
  const clockStart = performance.now();
  function logLine(text, cls){
    const now = performance.now() - clockStart;
    const row = document.createElement('div');
    row.className = 'fd-log-row' + (cls ? ' ' + cls : '');
    row.innerHTML = '<span class="ts">' + fmtTime(now) + '</span>' +
                    '<span class="msg">' + text + '</span>';
    const placeholder = logEl.querySelector('.fd-log-row.muted');
    if(placeholder && placeholder.querySelector('.msg').textContent.indexOf('idle') >= 0){
      placeholder.remove();
    }
    logEl.appendChild(row);
    logEl.scrollTop = logEl.scrollHeight;
  }
  logClearBtn.addEventListener('click', () => {
    logEl.innerHTML = '';
    logLine('log cleared', 'muted');
  });

  // ----- lifecycle visuals -----
  function setNodes(step){
    nodes.forEach((g, i) => g.classList.toggle('on', i === step));
    stateEl.textContent = step < 0 ? 'idle' : LIFECYCLE[step];
  }
  function setLbl(b, text){
    const e = b.querySelector('.lbl');
    if(e) e.textContent = text;
  }
  function setButtons(active){
    const order = ['cfg','conn','stim','disc'];
    order.forEach(name => {
      const b = btn[name];
      b.classList.remove('done','armed','active','danger');
      b.disabled = true;
    });
    // default labels
    setLbl(btn.cfg, 'Configure');
    setLbl(btn.conn, 'Connect');
    setLbl(btn.stim, 'Stim');
    setLbl(btn.disc, 'Disconnect');

    if(phase < 0){
      btn.cfg.disabled = false;
      btn.cfg.classList.add('armed');
      return;
    }
    order.forEach((name, idx) => {
      if(idx < phase) btn[name].classList.add('done');
    });
    if(stimRunning){
      btn.stim.disabled = false;
      btn.stim.classList.add('active');
      setLbl(btn.stim, 'Stop stim');
      btn.disc.disabled = false;
      btn.disc.classList.add('armed');
      return;
    }
    if(phase === 0){
      btn.conn.disabled = false; btn.conn.classList.add('armed');
    } else if(phase === 1){
      btn.stim.disabled = false; btn.stim.classList.add('armed');
    } else if(phase === 2){
      setLbl(btn.stim, 'Stim again');
      btn.stim.disabled = false; btn.stim.classList.add('armed');
      btn.disc.disabled = false; btn.disc.classList.add('armed');
    }
  }
  function updateState(){
    setNodes(phase);
    setButtons();
    if(phase < 0){
      summaryEl.innerHTML = 'configure to allocate channels';
    } else if(phase === 0){
      summaryEl.innerHTML = channels.length + ' channels allocated &middot; connect to arm';
    } else if(phase === 1){
      summaryEl.innerHTML = 'channels armed &middot; press stim to deliver';
    } else if(phase === 2 && stimRunning){
      summaryEl.innerHTML = 'delivering &middot; trial in progress';
    } else if(phase === 2){
      summaryEl.innerHTML = 'stim complete &middot; stim again or disconnect';
    } else if(phase === 3){
      summaryEl.innerHTML = 'disconnected &middot; idle';
    }
    fmtSliders();
  }

  // ----- slider readouts -----
  function fmtSliders(){
    const set = +iti.value, eff = effectiveTrainPeriodMs();
    if(eff > set + 0.5){
      itiV.innerHTML = set + ' ms &middot; <span style="color:var(--accent)">' +
        'clamped to ' + Math.ceil(eff) + ' ms (longest train)</span>';
    } else {
      itiV.textContent = set + ' ms';
    }
    repsV.textContent = (+reps.value);
    winV.textContent  = ((+win.value)/1000).toFixed(1) + ' s';
  }
  [iti, reps, win].forEach(el => el.addEventListener('input', fmtSliders));
  fmtSliders();

  // ----- read committed electrodes from §03 (with per-electrode params) -----
  function readChannels(){
    const arr = document.getElementById('array-demo');
    if(!arr) return [];
    const rows = arr.querySelectorAll('#ad-list .row.added');
    const out = [];
    rows.forEach(r => {
      const i = +r.dataset.i;
      let p = null;
      try { p = JSON.parse(r.dataset.params); } catch(e){}
      if(p) out.push({ i, params: p });
    });
    return out;
  }

  // ----- safety / power -----
  function fmtFix(n, d){ return (Math.round(n * Math.pow(10,d)) / Math.pow(10,d)).toFixed(d); }
  function renderSafety(){
    if(channels.length === 0){
      mx.Q.textContent = '—'; mx.Qd.textContent = '—';
      mx.K.textContent = '—'; mx.D.textContent  = '—';
      mx.I.textContent = '—';
      Object.values(mx).forEach(el => el.parentElement.classList.remove('over', 'caution'));
      safetyWarn.classList.remove('on');
      safetyWarn.innerHTML = '';
      return;
    }
    // aggregate ranges across channels
    let qMin = Infinity, qMax = -Infinity, qSum = 0;
    let qdMin = Infinity, qdMax = -Infinity;
    let kMin = Infinity, kMax = -Infinity;
    let dMin = Infinity, dMax = -Infinity;
    let iMin = Infinity, iMax = -Infinity, iSum = 0;
    const overK = [];
    channels.forEach(ch => {
      const p = ch.params;
      const q = chargePerPhaseUc(p);
      const qd = chargeDensityUcCm2(p);
      const k = shannonK(p);
      const d = dutyCycle(p);
      const i = avgCurrentUa(p);
      if(q < qMin) qMin = q; if(q > qMax) qMax = q; qSum += q;
      if(qd < qdMin) qdMin = qd; if(qd > qdMax) qdMax = qd;
      if(k < kMin) kMin = k; if(k > kMax) kMax = k;
      if(d < dMin) dMin = d; if(d > dMax) dMax = d;
      if(i < iMin) iMin = i; if(i > iMax) iMax = i; iSum += i;
      if(k > SHANNON_K_LIMIT) overK.push({i: ch.i, k});
    });
    function rng(lo, hi, d, unit){
      if(Math.abs(hi - lo) < Math.pow(10, -d) / 2){
        return fmtFix(lo, d) + ' ' + unit;
      }
      return fmtFix(lo, d) + '–' + fmtFix(hi, d) + ' ' + unit;
    }
    mx.Q.innerHTML  = rng(qMin, qMax, 3, 'µC') + ' <span style="color:var(--muted);font-size:11px;font-weight:500">&middot; sum ' + fmtFix(qSum,3) + ' µC</span>';
    mx.Qd.textContent = rng(qdMin, qdMax, 0, 'µC/cm²');
    mx.K.textContent  = rng(kMin, kMax, 2, '');
    mx.D.textContent  = rng(dMin * 100, dMax * 100, 1, '%');
    mx.I.innerHTML    = rng(iMin, iMax, 1, 'µA') + ' <span style="color:var(--muted);font-size:11px;font-weight:500">&middot; sum ' + fmtFix(iSum,1) + ' µA</span>';
    // caution styling on Shannon (sakura, not red — k is a flag, not a verdict)
    mx.K.parentElement.classList.toggle('caution', kMax > SHANNON_K_LIMIT);

    if(overK.length){
      const chips = overK.slice(0, 8).map(o =>
        '<span class="chip">'+ eLabel(o.i) +' &middot; k='+ fmtFix(o.k,2) +'</span>'
      ).join('');
      safetyWarn.innerHTML = '<strong>Above the classic Shannon line (k &gt; 1.85)</strong> on ' +
        overK.length + ' channel'+(overK.length>1?'s':'')+': ' + chips +
        (overK.length > 8 ? ' <span class="chip">+'+(overK.length-8)+' more</span>' : '') +
        '. The 1.85 cutoff is a conservative surface-electrode rule (Shannon 1992); ' +
        'for intracortical microelectrodes treat this as a caution flag, not a verdict — see references.';
      safetyWarn.classList.add('on');
    } else {
      safetyWarn.classList.remove('on');
      safetyWarn.innerHTML = '';
    }
  }
  // SVG handles for the cumulative-charge trace + summary readout.
  const powerSvg = root.querySelector('#fd-power-svg');
  const powerNowEl = root.querySelector('#fd-power-now');

  // ----- cumulative charge (replaces the old instant-power readout) -----
  // Real stim systems are current-controlled, not power-controlled, so the
  // diagnostic that matters is "how much charge have we put through the
  // tissue so far" and "what is the peak current per channel". We compute
  // total delivered charge analytically by counting pulse-starts.
  function nPulsesFired(ch, t){
    if(runStartMs == null) return 0;
    const p = ch.params;
    const trainMs = trainDurationMs(p);
    const trainPeriodMs = effectiveTrainPeriodMs();
    const n = +reps.value;
    const pulsePeriodMs = 1000 / p.fr;
    const runLen = (n - 1) * trainPeriodMs + trainMs;
    const tCap = Math.min(t, runStartMs + runLen);
    if(tCap <= runStartMs) return 0;
    const elapsed = tCap - runStartMs;
    const lastTrainIdx = Math.min(n - 1, Math.floor(elapsed / trainPeriodMs));
    let count = 0;
    for(let ri = 0; ri <= lastTrainIdx; ri++){
      const localT = Math.min(elapsed - ri * trainPeriodMs, trainMs);
      if(localT < 0) continue;
      const pi = Math.min(p.np - 1, Math.floor(localT / pulsePeriodMs));
      count += pi + 1;
    }
    return count;
  }
  function cumulativeChargeUc(t){
    if(channels.length === 0 || runStartMs == null) return 0;
    let sum = 0;
    for(const ch of channels){
      sum += nPulsesFired(ch, t) * chargePerPulseUc(ch.params);
    }
    return sum;
  }
  function peakChannelCurrentUa(){
    let m = 0;
    for(const ch of channels){ if(ch.params.amp > m) m = ch.params.amp; }
    return m;
  }

  // historical buffer for the cumulative-charge trace
  const traceBuf = []; // [{t, q}]   q in uC
  const TRACE_HISTORY_MS = 12000;
  // Fixed y-scale for the charge chart. Set once at stim start to the projected
  // end-of-run total so the trace climbs visibly instead of the axis rescaling
  // every frame as charge accumulates.
  let chartYMaxUc = 0.01;
  function niceCeil(x){
    if(x <= 0) return 1;
    const exp  = Math.floor(Math.log10(x));
    const base = Math.pow(10, exp);
    const f    = x / base;
    const nf   = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10;
    return nf * base;
  }

  function renderChargeChart(nowMs){
    const W = 1000, H = 180;
    const padL = 56, padR = 14, padT = 12, padB = 22;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const windowMs = +win.value;
    const tEnd = nowMs;
    const tStart = tEnd - windowMs;
    function xs(t){ return padL + ((t - tStart) / windowMs) * plotW; }

    // fixed y-scale, locked at stim start to the projected end-of-run total.
    const yMax = chartYMaxUc;
    function ys(q){ return padT + plotH - (q / yMax) * plotH; }

    let out = '';
    out += '<rect x="'+padL+'" y="'+padT+'" width="'+plotW+'" height="'+plotH+'" fill="#ffffff" stroke="#d8d6cf"/>';
    out += '<text x="'+(padL-8)+'" y="'+(padT+10)+'" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="10" fill="#6c6c66">'+ fmtFix(yMax,3) +' &#xB5;C</text>';
    out += '<text x="'+(padL-8)+'" y="'+(padT+plotH-2)+'" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="10" fill="#6c6c66">0</text>';

    // cumulative-charge polyline
    let pts = '';
    for(let i = 0; i < traceBuf.length; i++){
      const s = traceBuf[i];
      if(s.t < tStart) continue;
      if(s.t > tEnd)   break;
      pts += xs(s.t).toFixed(1) + ',' + ys(s.q).toFixed(1) + ' ';
    }
    if(pts){
      out += '<polyline points="'+pts+'" fill="none" stroke="#d86f91" stroke-width="2"/>';
    }

    // now line
    const xNow = padL + plotW;
    out += '<line x1="'+xNow+'" x2="'+xNow+'" y1="'+padT+'" y2="'+(padT+plotH)+
           '" stroke="#8a3a1d" stroke-width="1.2"/>';
    // axis label
    out += '<text x="'+(padL+plotW/2)+'" y="'+(H-4)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#6c6c66">'+
            (windowMs/1000).toFixed(2) + ' s window &middot; cumulative since stim start</text>';

    powerSvg.innerHTML = out;
  }

  function renderCumulativeCharge(nowMs){
    const qNow = cumulativeChargeUc(nowMs);
    traceBuf.push({t: nowMs, q: qNow});
    const cutoff = nowMs - TRACE_HISTORY_MS;
    while(traceBuf.length && traceBuf[0].t < cutoff) traceBuf.shift();
    mx.P.innerHTML = fmtFix(qNow, 3) + ' &micro;C';
    powerNowEl.innerHTML = fmtFix(qNow, 3) + ' &micro;C';
    renderChargeChart(nowMs);
  }

  // ----- utah-live mini grid -----
  const utahSvg = root.querySelector('#fd-utah-svg');
  const utahSubEl = root.querySelector('#fd-utah-sub');
  const UTAH_FLASH_MS = 80;
  // per-electrode flash-end timestamps (size 100). null = never fired.
  let flashEnd = new Array(100).fill(0);
  let lastTickMs = null;

  // build the utah-live svg structure once
  (function buildUtahGrid(){
    const NS = 'http://www.w3.org/2000/svg';
    const VB = 200, PAD = 8;
    const cell = (VB - 2*PAD) / 10;
    // border + faint grid
    const box = document.createElementNS(NS,'rect');
    box.setAttribute('x', PAD); box.setAttribute('y', PAD);
    box.setAttribute('width', VB - 2*PAD); box.setAttribute('height', VB - 2*PAD);
    box.setAttribute('fill','none'); box.setAttribute('stroke','#d8d6cf');
    utahSvg.appendChild(box);
    // dot per electrode
    for(let row=0; row<10; row++){
      for(let c=0; c<10; c++){
        const i = row*10 + c;
        const cx = PAD + cell*(c+0.5);
        const cy = PAD + cell*(row+0.5);
        const dot = document.createElementNS(NS,'circle');
        dot.setAttribute('cx', cx); dot.setAttribute('cy', cy);
        dot.setAttribute('r', cell * 0.36);
        dot.setAttribute('data-idx', i);
        dot.setAttribute('fill', '#ebe9e2');
        dot.setAttribute('stroke', '#d8d6cf');
        dot.setAttribute('stroke-width', '0.5');
        utahSvg.appendChild(dot);
      }
    }
  })();

  function paintUtah(nowMs){
    // pass 1: detect pulse fires in the interval (lastTickMs, nowMs] for each configured channel
    if(runStartMs != null && lastTickMs != null && channels.length){
      const t0 = lastTickMs, t1 = nowMs;
      const n     = +reps.value;
      channels.forEach(ch => {
        const p = ch.params;
        const trainMs = trainDurationMs(p);
        const pulsePeriodMs = 1000 / p.fr;
        const trainPeriodMs = effectiveTrainPeriodMs();
        const runLen = (n - 1) * trainPeriodMs + trainMs;
        const chFinish = (runEndMs != null && !stimRunning)
          ? Math.min(runEndMs, runStartMs + runLen)
          : (runStartMs + runLen);
        // any pulse-start time in (t0, t1]?
        // pulses are at runStartMs + ri*trainPeriodMs + pi*pulsePeriodMs, for ri in [0,n), pi in [0,np)
        const lo = Math.max(t0, runStartMs);
        const hi = Math.min(t1, chFinish);
        if(hi <= lo) return;
        // which train range overlaps?
        const tiLo = Math.max(0, Math.floor((lo - runStartMs) / trainPeriodMs));
        const tiHi = Math.min(n - 1, Math.floor((hi - runStartMs) / trainPeriodMs));
        for(let ri = tiLo; ri <= tiHi; ri++){
          const trialStart = runStartMs + ri * trainPeriodMs;
          for(let pi = 0; pi < p.np; pi++){
            const ts = trialStart + pi * pulsePeriodMs;
            if(ts > trialStart + trainMs) break;
            if(ts > lo && ts <= hi){
              flashEnd[ch.i] = nowMs + UTAH_FLASH_MS;
              break;
            }
          }
        }
      });
    }
    // pass 2: paint dots according to configured/flashing/safe state
    const dots = utahSvg.querySelectorAll('circle');
    const cfgSet = new Set(channels.map(c => c.i));
    const unsafeSet = new Set(channels.filter(c => shannonK(c.params) > SHANNON_K_LIMIT).map(c => c.i));
    dots.forEach(d => {
      const i = +d.getAttribute('data-idx');
      const configured = cfgSet.has(i);
      const unsafe = unsafeSet.has(i);
      const flashing = flashEnd[i] > nowMs;
      let fill, stroke, sw;
      if(flashing){
        const f = Math.max(0, (flashEnd[i] - nowMs) / UTAH_FLASH_MS); // 0..1
        if(unsafe){
          fill = '#8a3a1d';
          stroke = '#8a3a1d';
        } else {
          fill = '#d86f91';
          stroke = '#a83f63';
        }
        sw = (0.6 + 1.4 * f).toFixed(2);
      } else if(configured){
        fill = unsafe ? '#fadcd0' : '#fde7ef';
        stroke = unsafe ? '#8a3a1d' : '#a83f63';
        sw = '0.8';
      } else {
        fill = '#ebe9e2';
        stroke = '#d8d6cf';
        sw = '0.5';
      }
      d.setAttribute('fill', fill);
      d.setAttribute('stroke', stroke);
      d.setAttribute('stroke-width', sw);
    });
    // subline status
    if(channels.length === 0){
      utahSubEl.textContent = 'idle';
    } else if(runStartMs != null && stimRunning){
      utahSubEl.textContent = channels.length + ' active';
    } else if(channels.length){
      utahSubEl.textContent = channels.length + ' configured';
    }
  }

  // ----- carousel -----
  let rafId = null;
  let idleClockMs = 0;        // frozen clock display while idle
  function isIdle(){
    // truly idle: no stim is running and we're either pre-configure or
    // post-disconnect. configure/connect are short transient states; we
    // still tick during them so the user sees the live panel come alive.
    return !stimRunning && (phase === -1 || phase === 3);
  }
  function tick(){
    const now = performance.now();
    if(isIdle()){
      // freeze the clock, hide the now-line, skip live computation.
      clockEl.textContent = fmtTime(idleClockMs);
      rafId = requestAnimationFrame(tick);
      return;
    }
    const elapsed = now - clockStart;
    idleClockMs = elapsed;
    clockEl.textContent = fmtTime(elapsed);
    renderStrip(now);
    renderCumulativeCharge(now);
    paintUtah(now);
    lastTickMs = now;
    rafId = requestAnimationFrame(tick);
  }

  function renderStrip(nowMs){
    // Carousel shows ONLY configured channels (Conductor layout).
    // The strip auto-grows vertically when many channels are configured;
    // the cell's overflow:auto handles scrolling within the cell.
    const sorted = channels.slice().sort((a,b) => a.i - b.i);
    const W = 1000;
    const padL = 56, padR = 14, padT = 18, padB = 28;
    const plotW = W - padL - padR;
    const windowMs = +win.value;
    const tEnd = nowMs;
    const tStart = tEnd - windowMs;
    function xs(t){ return padL + ((t - tStart) / windowMs) * plotW; }

    let out = '';

    if(sorted.length === 0){
      // empty state — keep the cell tidy
      const H = 260;
      stripSvg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      const plotH = H - padT - padB;
      out += '<rect x="'+padL+'" y="'+padT+'" width="'+plotW+'" height="'+plotH+'" fill="#ffffff" stroke="#d8d6cf"/>';
      out += '<text x="'+(padL+plotW/2)+'" y="'+(padT+plotH/2+4)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" fill="#9a9a93">no channels configured</text>';
      // now line + time axis still render so the clock visibly moves
      const axisY = padT + plotH;
      const t0Sec = Math.floor(tStart/1000) * 1000;
      for(let t = t0Sec; t <= tEnd; t += 1000){
        if(t < tStart) continue;
        const x = xs(t);
        out += '<line x1="'+x+'" x2="'+x+'" y1="'+axisY+'" y2="'+(axisY+3)+'" stroke="#9a9a93"/>';
        out += '<text x="'+x+'" y="'+(axisY+14)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="#6c6c66">'+
                ((t - clockStart)/1000).toFixed(1)+'s</text>';
      }
      const xNow = padL + plotW;
      out += '<line x1="'+xNow+'" x2="'+xNow+'" y1="'+padT+'" y2="'+axisY+'" stroke="#8a3a1d" stroke-width="1.2"/>';
      out += '<text x="'+(xNow-3)+'" y="'+(padT-6)+'" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="9" fill="#8a3a1d">now</text>';
      stripSvg.innerHTML = out;
      return;
    }

    // configured-only rows, ample height per row
    const rowH = Math.max(20, Math.min(34, 220 / sorted.length));
    const plotH = sorted.length * rowH;
    const H = padT + plotH + padB;
    stripSvg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

    // outer frame
    out += '<rect x="'+padL+'" y="'+padT+'" width="'+plotW+'" height="'+plotH+'" fill="#ffffff" stroke="#d8d6cf"/>';

    sorted.forEach((ch, ri) => {
      const yTop = padT + ri * rowH;
      const yMid = yTop + rowH/2;
      // row separator
      if(ri > 0){
        out += '<line x1="'+padL+'" x2="'+(padL+plotW)+'" y1="'+yTop+'" y2="'+yTop+'" stroke="#ebe9e2" stroke-width="0.5"/>';
      }
      // label
      out += '<text x="'+(padL-8)+'" y="'+(yMid+4)+'" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="11" fill="#3a3a36" font-weight="500">'+ eLabel(ch.i) +'</text>';
      // baseline
      out += '<line x1="'+padL+'" x2="'+(padL+plotW)+'" y1="'+yMid+'" y2="'+yMid+
             '" stroke="#d8d6cf" stroke-width="0.6" stroke-dasharray="2 3"/>';

      if(runStartMs != null){
        const p = ch.params;
        const trainMs = trainDurationMs(p);
        const trainPeriodMs = effectiveTrainPeriodMs();
        const n = +reps.value;
        const tickH = (rowH/2) * 0.82;
        const pulsePeriodMs = 1000 / p.fr;
        const runLen = (n - 1) * trainPeriodMs + trainMs;
        const chFinish = (runEndMs != null && !stimRunning)
                        ? Math.min(runEndMs, runStartMs + runLen)
                        : (runStartMs + runLen);
        const unsafe = shannonK(p) > SHANNON_K_LIMIT;
        const tickColor = unsafe ? '#8a3a1d' : '#1c1c1a';
        const tickWidth = unsafe ? 2.0 : 1.6;

        for(let rj = 0; rj < n; rj++){
          const t0 = runStartMs + rj * trainPeriodMs;
          const t1 = Math.min(t0 + trainMs, chFinish);
          if(t1 < tStart) continue;
          if(t0 > tEnd)   break;
          if(t1 <= t0)    continue;
          for(let pi = 0; pi < p.np; pi++){
            const pStart = t0 + pi * pulsePeriodMs;
            if(pStart > t1) break;
            if(pStart < tStart || pStart > tEnd) continue;
            const x = xs(pStart);
            if(x < padL || x > padL + plotW) continue;
            out += '<line x1="'+x+'" x2="'+x+'" y1="'+(yMid - tickH)+'" y2="'+(yMid + tickH)+
                   '" stroke="'+tickColor+'" stroke-width="'+tickWidth+'" stroke-linecap="round"/>';
          }
        }
      }
    });

    // run start / end markers
    if(runStartMs != null){
      const marks = [['start', runStartMs]];
      if(!stimRunning && runEndMs != null) marks.push(['end', runEndMs]);
      marks.forEach(([lbl, t]) => {
        if(t < tStart || t > tEnd) return;
        out += '<line x1="'+xs(t)+'" x2="'+xs(t)+
               '" y1="'+padT+'" y2="'+(padT+plotH)+
               '" stroke="#d86f91" stroke-width="0.6" stroke-dasharray="2 3" opacity="0.6"/>';
        out += '<text x="'+(xs(t)+3)+'" y="'+(padT-4)+'" font-family="JetBrains Mono, monospace" font-size="9" fill="#a83f63">'+lbl+'</text>';
      });
    }

    // bottom time-axis
    const axisY = padT + plotH;
    const t0Sec = Math.floor(tStart/1000) * 1000;
    for(let t = t0Sec; t <= tEnd; t += 1000){
      if(t < tStart) continue;
      const x = xs(t);
      out += '<line x1="'+x+'" x2="'+x+'" y1="'+axisY+'" y2="'+(axisY+3)+'" stroke="#9a9a93"/>';
      out += '<text x="'+x+'" y="'+(axisY+14)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="#6c6c66">'+
              ((t - clockStart)/1000).toFixed(1)+'s</text>';
    }
    // now line
    const xNow = padL + plotW;
    out += '<line x1="'+xNow+'" x2="'+xNow+'" y1="'+padT+'" y2="'+axisY+
           '" stroke="#8a3a1d" stroke-width="1.2"/>';
    out += '<text x="'+(xNow-3)+'" y="'+(padT-6)+'" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="9" fill="#8a3a1d">now</text>';

    stripSvg.innerHTML = out;
  }

  // start the wall clock immediately
  tick();

  // ----- lifecycle button handlers -----
  btn.cfg.addEventListener('click', () => {
    const chs = readChannels();
    if(chs.length === 0){
      logLine('configure refused &middot; no electrodes in the list above', 'warn');
      return;
    }
    channels = chs;
    phase = 0;
    stimRunCount = 0;
    logLine('configure &middot; ' + chs.length + ' channel' + (chs.length>1?'s':'') + ' allocated', 'info');
    chs.slice(0, 6).forEach(ch => {
      logLine('  ' + eLabel(ch.i) + ' &middot; ' + paramSummaryStr(ch.params), 'dim');
    });
    if(chs.length > 6) logLine('  ... ' + (chs.length-6) + ' more channels', 'dim');
    // safety pass
    const overK = chs.filter(ch => shannonK(ch.params) > SHANNON_K_LIMIT);
    if(overK.length){
      logLine('caution &middot; ' + overK.length + ' channel' +
              (overK.length>1?'s':'') + ' above the classic Shannon line (k > 1.85)', 'warn');
      overK.slice(0,4).forEach(ch => {
        logLine('  ' + eLabel(ch.i) + ' &middot; k=' + fmtFix(shannonK(ch.params),2), 'warn');
      });
      if(overK.length > 4) logLine('  ... ' + (overK.length-4) + ' more', 'warn');
    }
    renderSafety();
    updateState();
  });

  btn.conn.addEventListener('click', () => {
    if(phase !== 0) return;
    phase = 1;
    logLine('connect &middot; channels armed &middot; impedance check ok', 'info');
    updateState();
  });

  function clearStimTimer(){
    if(stimFinishTimer){ clearTimeout(stimFinishTimer); stimFinishTimer = null; }
  }
  function trialDurationFor(p){
    const trainMs = trainDurationMs(p);
    const trainPeriodMs = effectiveTrainPeriodMs();
    const n = +reps.value;
    return (n - 1) * trainPeriodMs + trainMs;
  }
  function maxTrialMs(){
    let m = 0;
    channels.forEach(ch => { const d = trialDurationFor(ch.params); if(d > m) m = d; });
    return m;
  }

  let stimRunCount = 0;
  function startStimRun(){
    const dur = maxTrialMs();
    if(dur <= 0){
      logLine('stim refused &middot; trial duration is zero', 'warn');
      return;
    }
    stimRunCount++;
    phase = 2;
    stimRunning = true;
    runStartMs = performance.now() + 50;
    runEndMs = runStartMs + dur;
    // lock the charge-chart y-scale to the projected end-of-run total
    traceBuf.length = 0;
    chartYMaxUc = niceCeil(Math.max(1e-3, cumulativeChargeUc(runEndMs)));
    const n = +reps.value, trainPeriodMs = effectiveTrainPeriodMs();
    logLine('stim ' + stimRunCount + ' start &middot; ' + n + ' train' + (n>1?'s':'') +
            ' &middot; period ' + trainPeriodMs + ' ms &middot; duration ' +
            (dur/1000).toFixed(2) + ' s', 'ok');
    clearStimTimer();
    const myRun = stimRunCount;
    stimFinishTimer = setTimeout(() => {
      if(myRun !== stimRunCount) return; // a newer run superseded this one
      stimRunning = false;
      runEndMs = performance.now();
      stimFinishTimer = null;
      logLine('stim ' + myRun + ' complete &middot; ' + n + ' train' + (n>1?'s':'') +
              ' delivered &middot; ' + (dur/1000).toFixed(2) + ' s', 'ok');
      updateState();
    }, dur);
    updateState();
  }

  btn.stim.addEventListener('click', () => {
    if(phase === 1){
      // first stim after connect
      startStimRun();
    } else if(phase === 2 && stimRunning){
      // stop the current run early
      clearStimTimer();
      stimRunning = false;
      runEndMs = performance.now();
      logLine('stim ' + stimRunCount + ' stopped early', 'info');
      updateState();
    } else if(phase === 2 && !stimRunning){
      // fire another run with the current sliders
      startStimRun();
    }
  });

  btn.disc.addEventListener('click', () => {
    if(phase !== 2) return;
    if(stimRunning){
      clearStimTimer();
      stimRunning = false;
      runEndMs = performance.now();
      logLine('stim stopped early', 'info');
    }
    phase = 3;
    logLine('disconnect &middot; channels released', 'info');
    updateState();
    // settle back to idle after a short delay
    setTimeout(() => {
      phase = -1;
      channels = [];
      runStartMs = null;
      runEndMs = null;
      flashEnd.fill(0);
      renderSafety();
      updateState();
    }, 700);
  });

  updateState();
})();
</script>
"""


# --- M3 supplementary content blocks ---------------------------------------

M3_CONCEPT_HTML = r"""
<aside class="callout"><strong>The whole module in one sentence.</strong>
Picking the right amplitude, pulse width, interphase gap, frequency, and number of pulses turns
an inert electrode into a controllable knob on neuronal firing. The rest of the module is just
building intuition for what each knob does, scaling up from one electrode to a hundred, and
keeping an eye on safety while doing it.</aside>

<aside class="callout"><strong>The Shannon limit, in passing.</strong>
We compute <code>k = log10(Q) + log10(Qd)</code> per channel, where <code>Q</code> is charge per phase
in <strong>microcoulombs</strong> (uA &times; us / 10<sup>6</sup>) and <code>Qd</code> is charge density in
&micro;C/cm&sup2; (Q divided by the electrode area). Both terms must use the same charge unit for this formula
to make sense &mdash; Shannon (1992) reports it with Q in &micro;C.</aside>

<aside class="callout"><strong>...but read the fine print.</strong>
The <code>k &le; 1.85</code> rule comes from Shannon's 1992 fit to <em>large surface electrodes</em> in chronic
animal work &mdash; areas orders of magnitude bigger than the 2000&nbsp;&micro;m&sup2; intracortical site simulated
here. Applied to microelectrodes the line is widely understood to be <em>conservative and not directly
transferable</em>: penetrating microelectrodes routinely operate at charge densities well above it, and
modern reviews (Cogan 2008; Cogan, Ludwig, Welle &amp; Takmakov 2016) treat tissue-damage thresholds as
electrode-, waveform-, and duty-cycle-dependent rather than a single universal cutoff. So in this module
<code>k</code> is a <strong>caution flag, not a safety verdict</strong> &mdash; useful for spotting which
channels sit in the aggressive corner of the parameter space, not a pass/fail gate. See the references at
the foot of the page.</aside>
"""

M3_SELFCHECK_HTML = r"""
<details class="prompt">
  <summary>Q1. You halve the amplitude (pulse width and electrode unchanged). By how much does the Shannon factor <code>k</code> drop?</summary>
  <p>The charge per phase <code>Q = amp &times; pw</code> halves. Because the electrode area is unchanged,
  the charge density <code>Qd = Q / area</code> halves too. So both log terms in
  <code>k = log10(Q) + log10(Qd)</code> shrink by <code>log10(0.5) &approx; &minus;0.301</code>, and the total drop is
  <code>2 &times; 0.301 &approx; 0.60</code>. Note the distinction: Q itself drops by a factor of two
  (linear), while k drops by ~0.60 (additive, in log space).</p>
</details>
<details class="prompt">
  <summary>Q2. If you double frequency without touching amplitude, which changes &mdash; how many neurons are recruited per pulse, or how often each recruited neuron fires?</summary>
  <p>How often each recruited neuron fires. Recruitment is set per pulse by amplitude
  (the current radius around the electrode &mdash; the &radic;(I/K) thing from &sect;01); the same neurons
  get recruited each time, regardless of frequency. What frequency changes is the <em>rate</em>
  at which those same neurons get re-recruited, up to the refractory ceiling. In a cortical prosthesis
  this translates to phosphene <em>brightness</em>, not phosphene <em>size</em>.</p>
</details>
<details class="prompt">
  <summary>Q3. With <code>reps = 1</code>, the train period control has no effect on the trial. Why does the simulator still display it?</summary>
  <p>So the per-channel readouts stay coherent when other channels have <code>reps &gt; 1</code>, or when you
  sweep <code>reps</code>. The train period (start-to-start interval between trains) is what keeps trains
  of different lengths phase-locked across channels: with <code>reps = 1</code> nothing repeats, so the period
  has nowhere to apply, but the moment <code>reps</code> rises the scheduler needs it. Keeping the control
  visible (rather than hiding it conditionally) is a UX call &mdash; the safety calc itself is duty-cycle
  driven and depends only on pulse width and frequency.</p>
</details>
<details class="prompt">
  <summary>Q4. Your Surprise-me run sets one channel to <code>amp = 150 &micro;A</code>, <code>pw = 300 &micro;s</code>.
  The simulated electrode has area <code>A = 2000 &micro;m&sup2; = 2 &times; 10<sup>&minus;5</sup> cm&sup2;</code> (also visible
  in the Safety panel header). Is that channel inside the Shannon limit?</summary>
  <p><code>Q = 150 &micro;A &times; 300 &micro;s = 45000 &micro;A&middot;&micro;s = 0.045 &micro;C</code> (recall <code>1 &micro;A&middot;&micro;s = 1 pC</code>,
  so 45000 pC = 0.045 &micro;C). <code>Qd = 0.045 &micro;C / 2&times;10<sup>&minus;5</sup> cm&sup2; = 2250 &micro;C/cm&sup2;</code>.
  <code>k = log10(0.045) + log10(2250) &approx; &minus;1.347 + 3.352 = 2.005</code>. That is above the classic
  1.85 line, so the simulator flags it. But read that as a <em>caution</em>, not a verdict: the 1.85 cutoff
  is Shannon's conservative fit to large surface electrodes (see the callout in &sect;01), and a
  2000&nbsp;&micro;m&sup2; intracortical site is a very different regime. The honest answer is
  &ldquo;k&nbsp;&asymp;&nbsp;2.0 &mdash; in the aggressive corner of the space, worth a second look.&rdquo;</p>
</details>
"""

M3_NEXT_HTML = r"""
<p>Next module: <strong><a href="M4-phosphene-simulation.html">M4 &mdash; Phosphene simulation</a></strong>,
where the stimulation parameters you just tuned become a perceived image.</p>
<aside class="callout"><strong>Going deeper (optional).</strong>
The companion notebook <a href="M3-neuromod-and-stim/neuromod-and-stim.ipynb"><code>neuromod-and-stim.ipynb</code></a>
revisits this material in Python &mdash; driving the same parameters from code, pushing them through
the stimulator API, and inspecting the actual <code>(channels &times; time)</code> stimulation matrices,
with the charge-balance and Shannon checks exposed as importable functions. It is a self-guided
resource, not a workshop step: open it whenever you want the hands-on version.</aside>
"""

M3_REFS_HTML = r"""
<div class="refs">
<ul>
  <li><span class="rk">paper</span> Shannon, R.V. (1992), <em>A model of safe levels for electrical
  stimulation</em>, IEEE Transactions on Biomedical Engineering 39(4):424&ndash;426.
  <a href="https://doi.org/10.1109/10.126616" target="_blank" rel="noopener">doi:10.1109/10.126616</a>
  &mdash; origin of the <code>k &le; 1.85</code> charge / charge-density rule.</li>
  <li><span class="rk">review</span> Cogan, S.F. (2008), <em>Neural stimulation and recording
  electrodes</em>, Annual Review of Biomedical Engineering 10:275&ndash;309.
  <a href="https://doi.org/10.1146/annurev.bioeng.10.061807.160518" target="_blank" rel="noopener">doi:10.1146/annurev.bioeng.10.061807.160518</a>.</li>
  <li><span class="rk">review</span> Cogan, Ludwig, Welle &amp; Takmakov (2016), <em>Tissue damage
  thresholds during therapeutic electrical stimulation</em>, Journal of Neural Engineering
  13(2):021001 &mdash; why microelectrode safety limits are electrode-, waveform-, and
  duty-cycle-dependent rather than a single universal cutoff.</li>
  <li><span class="rk">tool</span> The stimulator panel is a mock modelled on real research
  stimulation APIs (e.g. <a href="https://rippleneuro.com/" target="_blank" rel="noopener">Ripple
  Neuro</a> systems); the parameters and the configure &rarr; connect &rarr; stim &rarr; disconnect
  lifecycle mirror a real device manual.</li>
</ul>
</div>
"""


# --- single-electrode stim demo (M3) ---------------------------------------

STIM_DEMO_HTML = """
<div class='stim-demo' id='stim-demo'>
  <div class='stim-tabs' role='tablist' aria-label='Pulse parameters'>
    <button role='tab' aria-selected='true'  data-tab='amp'><span class='n'>P1</span>Amplitude</button>
    <button role='tab' aria-selected='false' data-tab='pw' ><span class='n'>P2</span>Pulse width</button>
    <button role='tab' aria-selected='false' data-tab='ip' ><span class='n'>P3</span>Interphase</button>
    <button role='tab' aria-selected='false' data-tab='fr' ><span class='n'>P4</span>Frequency</button>
    <button role='tab' aria-selected='false' data-tab='np' ><span class='n'>P5</span>Num pulses</button>
  </div>

  <div class='stim-body'>
    <div class='stim-explain'>
      <div class='strategy' id='sd-strategy'>amplitude modulation</div>
      <h4 id='sd-title'>Amplitude</h4>
      <p id='sd-desc'>Current delivered per phase, in microamperes. Higher amplitude recruits more cortical tissue around the electrode. Together with pulse width it sets the charge per pulse.</p>
      <p class='mono' style='font-size:12px;color:var(--muted);margin-top:6px' id='sd-effect'>strategy: amplitude modulation. modulates: recruited tissue / firing probability.</p>
    </div>

    <div>
      <div class='stim-figure'>
        <svg viewBox='0 0 560 200' aria-label='Single-electrode biphasic pulse train' id='sd-svg'></svg>
        <div class='legend'>
          <span><i style='background:var(--ink)'></i>cathodic phase</span>
          <span><i style='background:var(--accent)'></i>anodic phase</span>
          <span><i style='background:var(--muted-2);height:2px;margin-top:3px'></i>baseline / interphase</span>
        </div>
      </div>

      <div class='stim-controls' id='sd-controls'>
        <label for='sd-amp'>amplitude</label>
        <input id='sd-amp' type='range' min='10'  max='200' step='5' value='80'>
        <span class='v' id='sd-amp-v'>80 &micro;A</span>

        <label for='sd-pw'>pulse width</label>
        <input id='sd-pw'  type='range' min='50'  max='500' step='10' value='170'>
        <span class='v' id='sd-pw-v'>170 &micro;s</span>

        <label for='sd-ip'>interphase</label>
        <input id='sd-ip'  type='range' min='0'   max='200' step='5' value='40'>
        <span class='v' id='sd-ip-v'>40 &micro;s</span>

        <label for='sd-fr'>frequency</label>
        <input id='sd-fr'  type='range' min='10'  max='300' step='5' value='300'>
        <span class='v' id='sd-fr-v'>300 Hz</span>

        <label for='sd-np'>num pulses</label>
        <input id='sd-np'  type='range' min='1'   max='100' step='1' value='50'>
        <span class='v' id='sd-np-v'>50</span>

        <div class='runrow'>
          <span class='status' id='sd-status'>charge / phase: 0.014 &micro;C &middot; train: 75 ms</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
(function(){
  const TABS = {
    amp: {
      title: 'Amplitude',
      strategy: 'amplitude modulation',
      desc: 'Current per phase, in microamperes. Sets the spatial reach of the pulse: as amplitude rises, the volume of tissue brought above firing threshold around the electrode grows (roughly as the square root of current density). That is recruitment &mdash; how many neurons fire on any given pulse. Selectivity (which neurons) trades against this: higher amplitude recruits more, but also less specifically.',
      effect: 'modulates: recruitment radius / number of neurons firing per pulse.'
    },
    pw: {
      title: 'Pulse width',
      strategy: 'charge per pulse',
      desc: 'Duration of each phase, in microseconds. The strength-duration curve (Lapicque, 1907) says a neuron will fire when amp &times; pw exceeds a threshold charge, with longer pulses needing less current and shorter pulses needing more &mdash; an axon\\'s rheobase is the minimum current it can ever respond to, and chronaxie is the pulse width at twice rheobase. Practical consequence: widening the pulse raises charge per phase even if you hold amplitude constant, which pushes you toward the Shannon limit faster than scaling amplitude alone.',
      effect: 'modulates: charge per phase along the strength-duration curve.'
    },
    ip: {
      title: 'Interphase gap',
      strategy: 'waveform shape',
      desc: 'Time between the cathodic and anodic phases, in microseconds. A short gap (close to zero) gives the cleanest charge balance; an intermediate gap (~50&ndash;200 &micro;s) is widely used because it lets the cathodic phase finish recruiting axons before the anodic reversal cuts the recruitment short, raising effective excitation per unit charge.',
      effect: 'modulates: how much of the cathodic recruitment survives the anodic reversal.'
    },
    fr: {
      title: 'Frequency',
      strategy: 'frequency modulation',
      desc: 'Pulse repetition rate, in hertz. Sets the <em>opportunity</em> rate to fire the recruited neurons. Real axons have a refractory period &mdash; ~1 ms absolute (no second spike possible) and ~5 ms relative (a second spike needs more current) &mdash; so above ~200&ndash;300 Hz, neurons cannot follow every pulse one-to-one and the driven firing rate plateaus. Below that, frequency translates roughly linearly to firing rate, and to phosphene brightness in cortical prostheses.',
      effect: 'modulates: driven firing rate per recruited neuron, up to the refractory ceiling.'
    },
    np: {
      title: 'Number of pulses',
      strategy: 'train duration',
      desc: 'How many biphasic pulses make up the train. Combined with frequency it sets the train duration (np &minus; 1 periods plus one pulse). Short trains probe acute, near-instantaneous response. Longer trains expose adaptation &mdash; the slow drop in firing rate that real cortex shows under sustained stim (Fern&aacute;ndez et al., 2021).',
      effect: 'modulates: train duration, total delivered charge, exposure to adaptation.'
    }
  };

  const root = document.getElementById('stim-demo');
  if(!root) return;

  const svg = root.querySelector('#sd-svg');
  const NS  = 'http://www.w3.org/2000/svg';

  const sliders = {
    amp: root.querySelector('#sd-amp'),
    pw:  root.querySelector('#sd-pw'),
    ip:  root.querySelector('#sd-ip'),
    fr:  root.querySelector('#sd-fr'),
    np:  root.querySelector('#sd-np')
  };
  const readouts = {
    amp: root.querySelector('#sd-amp-v'),
    pw:  root.querySelector('#sd-pw-v'),
    ip:  root.querySelector('#sd-ip-v'),
    fr:  root.querySelector('#sd-fr-v'),
    np:  root.querySelector('#sd-np-v')
  };
  const status = root.querySelector('#sd-status');
  const titleEl = root.querySelector('#sd-title');
  const stratEl = root.querySelector('#sd-strategy');
  const descEl  = root.querySelector('#sd-desc');
  const effEl   = root.querySelector('#sd-effect');

  let activeTab = 'amp';

  function values(){
    return {
      amp: +sliders.amp.value,   // uA
      pw:  +sliders.pw.value,    // us per phase
      ip:  +sliders.ip.value,    // us interphase
      fr:  +sliders.fr.value,    // Hz
      np:  +sliders.np.value
    };
  }

  function fmtReadouts(v){
    readouts.amp.innerHTML = v.amp + ' &micro;A';
    readouts.pw.innerHTML  = v.pw  + ' &micro;s';
    readouts.ip.innerHTML  = v.ip  + ' &micro;s';
    readouts.fr.textContent = v.fr + ' Hz';
    readouts.np.textContent = v.np;
  }

  function trainDurationMs(v){
    // train length = (np-1) periods + one pulse
    const periodMs = 1000 / v.fr;
    const pulseMs = (2*v.pw + v.ip) / 1000;
    return Math.max(pulseMs, (v.np - 1) * periodMs + pulseMs);
  }

  function chargePerPhaseUc(v){
    // amplitude in uA, pulse width in us -> charge in uC = uA * us / 1e6
    return (v.amp * v.pw) / 1e6;
  }

  function fmtStatus(v){
    const ch = chargePerPhaseUc(v).toFixed(3);
    const dur = trainDurationMs(v).toFixed(1);
    status.innerHTML = 'charge / phase: ' + ch + ' &micro;C &middot; train: ' + dur + ' ms';
  }

  // --- drawing ---
  function clear(node){ while(node.firstChild) node.removeChild(node.firstChild); }
  function el(tag, attrs){ const n=document.createElementNS(NS,tag);
    for(const k in attrs) n.setAttribute(k, attrs[k]); return n; }

  function draw(v, playMs){
    clear(svg);
    const W = 560, H = 200;
    const padL = 38, padR = 12, padT = 18, padB = 28;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const midY = padT + plotH/2;

    // x range = train duration + 10% headroom
    const xMaxMs = trainDurationMs(v) * 1.1 + 1;
    function xs(ms){ return padL + (ms / xMaxMs) * plotW; }

    // amplitude scale: 200 uA -> 80% of half-height
    const ampMax = 200;
    function ys(uA){ return midY - (uA / ampMax) * (plotH/2 * 0.8); }

    // grid
    const grid = el('g', {});
    // baseline
    grid.appendChild(el('line', {
      x1: padL, x2: padL+plotW, y1: midY, y2: midY,
      stroke: '#9a9a93', 'stroke-width': 1, 'stroke-dasharray':'2 3'
    }));
    // axis box
    grid.appendChild(el('rect', {
      x: padL, y: padT, width: plotW, height: plotH,
      fill: 'none', stroke: '#d8d6cf', 'stroke-width': 1
    }));
    // y ticks
    [-200, -100, 0, 100, 200].forEach(uA => {
      const y = ys(uA);
      grid.appendChild(el('line', { x1: padL-3, x2: padL, y1: y, y2: y, stroke:'#9a9a93' }));
      const t = el('text', { x: padL-6, y: y+3, 'text-anchor':'end',
        'font-family':'JetBrains Mono, monospace', 'font-size':'9px', fill:'#6c6c66' });
      t.textContent = uA;
      grid.appendChild(t);
    });
    const ylab = el('text', { x: 10, y: midY,
      'font-family':'JetBrains Mono, monospace', 'font-size':'10px', fill:'#6c6c66',
      transform: 'rotate(-90 10,' + midY + ')', 'text-anchor':'middle' });
    ylab.textContent = 'current (uA)';
    grid.appendChild(ylab);
    // x ticks
    const xMaxRound = Math.ceil(xMaxMs);
    const step = xMaxRound <= 20 ? 5 : (xMaxRound <= 60 ? 10 : (xMaxRound <= 150 ? 20 : 50));
    for(let ms=0; ms<=xMaxRound; ms+=step){
      const x = xs(ms);
      grid.appendChild(el('line', { x1: x, x2: x, y1: padT+plotH, y2: padT+plotH+3, stroke:'#9a9a93' }));
      const t = el('text', { x: x, y: padT+plotH+14, 'text-anchor':'middle',
        'font-family':'JetBrains Mono, monospace', 'font-size':'9px', fill:'#6c6c66' });
      t.textContent = ms;
      grid.appendChild(t);
    }
    const xlab = el('text', { x: padL+plotW/2, y: H-6, 'text-anchor':'middle',
      'font-family':'JetBrains Mono, monospace', 'font-size':'10px', fill:'#6c6c66' });
    xlab.textContent = 'time (ms)';
    grid.appendChild(xlab);
    svg.appendChild(grid);

    // pulses
    const periodMs = 1000 / v.fr;
    const phaseMs  = v.pw / 1000;
    const ipMs     = v.ip / 1000;
    const cathColor = '#1c1c1a';
    const anodColor = '#d86f91';

    // determine how many pulses to draw given playMs progression
    const np = v.np;
    const drawN = (playMs == null) ? np : Math.min(np, Math.floor(playMs / periodMs) + 1);

    for(let i = 0; i < drawN; i++){
      const t0 = i * periodMs;
      const cathStart = t0;
      const cathEnd   = t0 + phaseMs;
      const anodStart = cathEnd + ipMs;
      const anodEnd   = anodStart + phaseMs;

      // cathodic (down) filled
      // ys(-v.amp) is BELOW midY (larger y); rect grows downward from midY
      svg.appendChild(el('rect', {
        x: xs(cathStart),
        y: midY,
        width:  xs(cathEnd) - xs(cathStart),
        height: ys(-v.amp) - midY,
        fill: cathColor, stroke: cathColor, 'stroke-width': 0.6
      }));

      // interphase baseline
      if(ipMs > 0){
        svg.appendChild(el('line', {
          x1: xs(cathEnd), x2: xs(anodStart), y1: midY, y2: midY,
          stroke: '#9a9a93', 'stroke-width': 1.4
        }));
      }

      // anodic (up) filled
      svg.appendChild(el('rect', {
        x: xs(anodStart),
        y: ys(v.amp),
        width:  xs(anodEnd) - xs(anodStart),
        height: midY - ys(v.amp),
        fill: anodColor, stroke: '#a83f63', 'stroke-width': 0.6
      }));
    }

    // playhead
    if(playMs != null){
      const xh = xs(Math.min(playMs, xMaxMs));
      svg.appendChild(el('line', {
        x1: xh, x2: xh, y1: padT, y2: padT+plotH,
        stroke: '#d86f91', 'stroke-width': 1, 'stroke-dasharray': '2 2'
      }));
    }
  }

  function render(playMs){
    const v = values();
    fmtReadouts(v);
    fmtStatus(v);
    draw(v, playMs == null ? null : playMs);
  }

  // --- tabs ---
  const tabBtns = root.querySelectorAll('.stim-tabs button');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.setAttribute('aria-selected', b === btn ? 'true' : 'false'));
      activeTab = btn.dataset.tab;
      const info = TABS[activeTab];
      titleEl.textContent = info.title;
      stratEl.textContent = info.strategy;
      descEl.textContent  = info.desc;
      effEl.textContent   = info.effect;
    });
  });

  // --- sliders ---
  Object.keys(sliders).forEach(k => {
    sliders[k].addEventListener('input', () => render(null));
  });

  // initial render
  render(null);
})();
</script>
"""


def build_module(filename: str, spec: dict) -> None:
    sections_html = []
    toc_links = []
    extras = spec.get("extras", {})
    for num, anchor, title, blurb in spec["sections"]:
        toc_links.append(
            f"<a href='#{anchor}'><span class='n'>{num}</span> {title}</a>"
        )
        extra_key = extras.get(anchor)
        if extra_key == "STIM_DEMO":
            extra_html = STIM_DEMO_HTML
            todo_html = ""
        elif extra_key == "ARRAY_DEMO":
            extra_html = ARRAY_DEMO_HTML
            todo_html = ""
        elif extra_key == "STIM_FLOW":
            extra_html = STIM_FLOW_HTML
            todo_html = ""
        elif extra_key == "M3_SELFCHECK":
            extra_html = M3_SELFCHECK_HTML
            todo_html = ""
        elif extra_key == "M3_NEXT":
            extra_html = M3_NEXT_HTML
            todo_html = ""
        elif extra_key == "M3_REFS":
            extra_html = M3_REFS_HTML
            todo_html = ""
        elif extra_key == "M3_CONCEPT":
            extra_html = M3_CONCEPT_HTML
            todo_html = ""
        else:
            extra_html = ""
            todo_html = (
                f"<aside class='todo'><strong>To write.</strong> "
                f"{ROLES[spec['lead']]} - concept, optional figure or table, "
                f"optional code excerpt, exercise prompt where relevant.</aside>"
            )
        sections_html.append(f"""
<section id='{anchor}'>
<h2><span class='num'>{num}</span>{title}</h2>
<p class='kicker'>{blurb}</p>
{extra_html}
{todo_html}
</section>
""")
    toc_html = "<nav class='toc' aria-label='Sections'>" + "".join(toc_links) + "</nav>"
    if spec.get("status", "stub") == "stub":
        trailing = dedent(f"""
<hr class='div'/>
<section id='lead'>
<h3>Lead</h3>
<p>{ROLES[spec['lead']]} write this module. Edit this file directly; keep the section IDs stable so links from the plan don't break.</p>
</section>
""")
    else:
        trailing = ""
    body = "\n".join(sections_html) + trailing

    meta = (
        f"<span><strong>Lead:</strong> {ROLES[spec['lead']]}</span>"
        f"<span><strong>Status:</strong> {spec.get('status', 'stub')}</span>"
        '<span>part of the <a href="../bootcamp-plan.html">NTH bootcamp plan</a></span>'
    )

    # eyebrow looks like "NTH / M3" — parse the module index for the pipeline strip
    import re as _re
    m = _re.search(r"M(\d+)", spec["eyebrow"])
    idx = int(m.group(1)) if m else 0
    pipe = pipeline_strip(idx) if idx else ""
    nav = module_nav(idx) if idx else ""

    html_text = page(
        title=f"NTH Bootcamp - {spec['eyebrow']}",
        eyebrow=spec["eyebrow"],
        h1_html=spec["h1"],
        lede=spec["lede"],
        meta_html=meta,
        toc_html=toc_html,
        body_html=body,
        pipeline_html=pipe,
        footer_html=spec.get("footer", ""),
        nav_html=nav,
    )
    (MODULES_DIR / filename).write_text(html_text, encoding="utf-8")


# Modules this generator owns end-to-end. The other four
# (M1 CV, M2 Gaze, M4 Phosphene, M5 Decoding) are hand-authored playgrounds
# and must NOT be regenerated; this script refuses to overwrite them.
OWNED_MODULES = {
    "M3-neuromod-and-stim.html",         # M3 - ours
}


def main() -> None:
    build_plan()
    written = [BOOTCAMP_DIR / "bootcamp-plan.html"]
    for filename, spec in MODULE_CONTENT.items():
        if filename not in OWNED_MODULES:
            print(f"Skipping {filename} (hand-authored playground, not regenerated)")
            continue
        build_module(filename, spec)
        written.append(MODULES_DIR / filename)
    for path in written:
        size_kb = path.stat().st_size / 1024
        print(f"Wrote {path}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
