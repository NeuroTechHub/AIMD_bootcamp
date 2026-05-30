"""One-shot builder for the M3 neuromod-and-stim notebooks (workshop + solution).

Emits two paired Jupyter notebooks:
  modules/neuromod-and-stim/neuromod-and-stim.ipynb            (stubs)
  modules/neuromod-and-stim/neuromod-and-stim-solution.ipynb   (filled)

Run from anywhere; idempotent. Mirrors the build/_build_m5_notebook.py pattern.
"""
from __future__ import annotations
import json
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "modules" / "neuromod-and-stim"
OUT_WORKSHOP = OUT_DIR / "neuromod-and-stim.ipynb"
OUT_SOLUTION = OUT_DIR / "neuromod-and-stim-solution.ipynb"

# Cross-file links in markdown cells use absolute GitHub URLs (not relative
# paths) so they survive Colab's flat /content/ mount. Works equally well in
# VS Code / Jupyter — clicks open a browser tab to the GitHub-rendered view.


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


WORKSHOP: list[dict] = []
SOLUTION: list[dict] = []


def both_md(text: str) -> None:
    WORKSHOP.append(md(text))
    SOLUTION.append(md(text))


def both_code(text: str) -> None:
    WORKSHOP.append(code(text))
    SOLUTION.append(code(text))


def split_code(stub: str, answer: str) -> None:
    WORKSHOP.append(code(stub))
    SOLUTION.append(code(answer))


def split_md(stub_md: str, answer_md: str) -> None:
    WORKSHOP.append(md(stub_md))
    SOLUTION.append(md(answer_md))


# ---------------------------------------------------------------------------
# Title + framing
# ---------------------------------------------------------------------------

split_md(
    r"""# M3 — Neuromodulation & stimulation

**NTH bootcamp · Module 3**

Before a cortical visual prosthesis can light up the brain, it has to shape a current waveform that is *safe*, *targetable*, and *audible* to the nervous system. This notebook is the code companion to [`neuromod-and-stim.html`](https://github.com/NeuroTechHub/AIMD_bootcamp/blob/main/modules/neuromod-and-stim.html):

1. Neuromodulation in one minute
2. The five pulse parameters
3. Configure a Utah array
4. Fire the stimulator (mock Ripple)
5. From electrodes to phosphenes — teaser

The HTML page is for moving sliders. This notebook is for the things sliders can't show: the µs↔30 kHz cycle quantisation the hardware actually does, the Shannon-k charge-density math behind every safety chip, the interleaving offsets that let multiple electrodes share a 300 Hz train, and a one-cell bridge into M4's phosphene model.

Exercises are tagged **`[easy]`**, **`[intermediate]`**, or **`[challenge]`**.
""",
    r"""# M3 — Neuromodulation & stimulation · **Solutions**

**NTH bootcamp · Module 3**

Before a cortical visual prosthesis can light up the brain, it has to shape a current waveform that is *safe*, *targetable*, and *audible* to the nervous system. This notebook is the code companion to [`neuromod-and-stim.html`](https://github.com/NeuroTechHub/AIMD_bootcamp/blob/main/modules/neuromod-and-stim.html):

1. Neuromodulation in one minute
2. The five pulse parameters
3. Configure a Utah array
4. Fire the stimulator (mock Ripple)
5. From electrodes to phosphenes — teaser

The HTML page is for moving sliders. This notebook is for the things sliders can't show: the µs↔30 kHz cycle quantisation the hardware actually does, the Shannon-k charge-density math behind every safety chip, the interleaving offsets that let multiple electrodes share a 300 Hz train, and a one-cell bridge into M4's phosphene model.

Exercises are tagged **`[easy]`**, **`[intermediate]`**, or **`[challenge]`**.
""",
)

both_md(r"""## Setup

Required packages:

```bash
pip install --user numpy matplotlib ipywidgets
```

The cell below installs them and defines a tiny **inline mock Ripple** stimulator whose API surface mirrors [`neurolight2.stim.base_stimulator.StimParams`](https://github.com/) and the `create_stimulator("mock_ripple")` driver. No hardware, no `xipppy`, no Trellis — but the call shape and field names are the same, so when you later open the real driver it will look familiar.
""")

both_code(r"""%pip install --user -q numpy matplotlib ipywidgets
""")

both_code(r"""# Imports + inline mock Ripple stimulator + plot_pulse helper.
# Mirror of neurolight2.stim.factory.create_stimulator("mock_ripple").
import math
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import matplotlib.pyplot as plt

CYCLE_US = 33.3           # Ripple Grapevine ticks at 30 kHz (1 cycle = 33.3 us)
SHANNON_K_LIMIT = 1.85    # conservative; microelectrodes routinely exceed
DEFAULT_UTAH_AREA_CM2 = 2.0e-5   # ~1900 um^2 Utah-array tip


@dataclass(frozen=True)
class StimParams:
    '''Per-trial stimulation parameters. All per-electrode lists must have the
    same length. Field names mirror neurolight2.stim.base_stimulator.StimParams.'''
    electrodes: List[int]
    amplitudes_ua: List[int]
    pulse_widths_us: List[float]
    frequencies_hz: List[float]
    num_pulses: List[int]
    interphase_us: float = 60.0
    offsets_us: List[float] = field(default_factory=list)

    def __post_init__(self):
        n = len(self.electrodes)
        for fname, v in [('amplitudes_ua', self.amplitudes_ua),
                         ('pulse_widths_us', self.pulse_widths_us),
                         ('frequencies_hz', self.frequencies_hz),
                         ('num_pulses', self.num_pulses)]:
            if len(v) != n:
                raise ValueError(f'{fname} length {len(v)} != electrodes length {n}')
        if self.offsets_us and len(self.offsets_us) != n:
            raise ValueError(f'offsets_us length {len(self.offsets_us)} != electrodes length {n}')

    def to_dict(self) -> dict:
        return {
            'electrodes': list(self.electrodes),
            'amplitudes_ua': list(self.amplitudes_ua),
            'pulse_widths_us': list(self.pulse_widths_us),
            'frequencies_hz': list(self.frequencies_hz),
            'num_pulses': list(self.num_pulses),
            'interphase_us': self.interphase_us,
            'offsets_us': list(self.offsets_us),
        }


@dataclass
class StimEvent:
    '''What stimulate() returns. Mirrors the safety fields of neurolight2.safety.stim_buffer.StimEvent.'''
    charge_per_phase_nc: float
    charge_density_uc_cm2: float
    shannon_k: float
    duration_ms: float
    safety_ok: bool
    is_executed: bool

    def __str__(self) -> str:
        ok = 'OK' if self.safety_ok else 'BLOCKED'
        return (f'StimEvent[{ok}] Q={self.charge_per_phase_nc:.2f} nC | '
                f'D={self.charge_density_uc_cm2:.0f} uC/cm^2 | '
                f'k={self.shannon_k:.2f} | dur={self.duration_ms:.1f} ms')


class MockRipple:
    '''Hardware-free stimulator with the same call signature as the real driver.

    >>> stim = MockRipple()
    >>> ev = stim.stimulate(params)
    >>> ev.safety_ok
    True
    '''
    def __init__(self, electrode_area_cm2: float = DEFAULT_UTAH_AREA_CM2,
                 shannon_k_limit: float = SHANNON_K_LIMIT):
        self.electrode_area_cm2 = electrode_area_cm2
        self.shannon_k_limit = shannon_k_limit
        self.history: List[StimEvent] = []

    def stimulate(self, params: StimParams) -> StimEvent:
        # Worst-case across electrodes — that's what the safety checker uses.
        worst = max(range(len(params.electrodes)),
                    key=lambda i: params.amplitudes_ua[i] * params.pulse_widths_us[i])
        amp_ua = params.amplitudes_ua[worst]
        pw_us  = params.pulse_widths_us[worst]

        q_nc = amp_ua * pw_us / 1000.0                          # uA * us -> pC * 1000 = nC
        d_uc_cm2 = (q_nc / 1000.0) / self.electrode_area_cm2    # convert nC->uC then per cm^2
        if q_nc > 0 and d_uc_cm2 > 0:
            k = math.log10(q_nc / 1000.0) + math.log10(d_uc_cm2)  # Shannon: log10(Q_uC) + log10(D_uC/cm^2)
        else:
            k = -math.inf

        duration_ms = max(
            (params.num_pulses[i] / params.frequencies_hz[i]) * 1000.0
            for i in range(len(params.electrodes))
        )

        safety_ok = (k <= self.shannon_k_limit)
        ev = StimEvent(
            charge_per_phase_nc=q_nc,
            charge_density_uc_cm2=d_uc_cm2,
            shannon_k=k,
            duration_ms=duration_ms,
            safety_ok=safety_ok,
            is_executed=safety_ok,
        )
        self.history.append(ev)
        return ev


def plot_pulse(amp_ua: float = 80, pw_us: float = 170, interphase_us: float = 60,
               freq_hz: Optional[float] = None, num_pulses: int = 1,
               title: Optional[str] = None, ax=None):
    '''Plot a biphasic train as current vs time (uA vs ms). Cathodic-first.'''
    period_us = 1e6 / freq_hz if freq_hz else 2 * pw_us + interphase_us + 200
    total_us  = period_us * num_pulses
    t = np.linspace(0, total_us, max(2000, int(total_us / 5)))
    i_ua = np.zeros_like(t)
    for k in range(num_pulses):
        t0 = k * period_us
        i_ua[(t >= t0) & (t < t0 + pw_us)] = -amp_ua
        i_ua[(t >= t0 + pw_us + interphase_us) &
             (t <  t0 + pw_us + interphase_us + pw_us)] = +amp_ua
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 2.4))
    ax.plot(t / 1000.0, i_ua, lw=1.3, color='#1c1c1a')
    ax.axhline(0, color='#888', lw=0.5)
    ax.set_xlabel('time (ms)'); ax.set_ylabel('current (uA)')
    ax.set_title(title or f'{num_pulses} biphasic pulse(s) at {amp_ua} uA / {pw_us} us')
    ax.set_xlim(0, total_us / 1000.0)
    ax.grid(True, alpha=0.2)
    if ax is None:
        plt.tight_layout(); plt.show()
    return ax


print('mock-ripple ready · numpy', np.__version__,
      '· Shannon-k limit', SHANNON_K_LIMIT,
      '· electrode area', DEFAULT_UTAH_AREA_CM2, 'cm^2')
""")

# ---------------------------------------------------------------------------
# Section 1 - Neuromodulation in one minute
# ---------------------------------------------------------------------------

both_md(r"""## 1 · Neuromodulation in one minute

Electrical stim modulates spike timing by injecting charge across an electrode. Two knobs everyone reaches for first are **amplitude** (how strong) and **frequency** (how often). A 1907 result by Lapicque says the minimum amplitude to fire a neuron falls with pulse width along a strength-duration curve — so amplitude and pulse width together set the *threshold for evoking a spike*.

| Knob | Unit | Typical | What it does |
|---|---|---|---|
| amplitude | µA | 10 – 250 | drives more neurons per pulse |
| pulse width | µs | 50 – 500 | longer phases lower the recruitment threshold |
| frequency | Hz | 10 – 300 | sets the driven firing rate (refractory ceiling ~250 Hz) |
| charge per phase | nC | 5 – 50 | amplitude × pulse width — what safety actually cares about |

The waveform we use is **biphasic, charge-balanced** — a cathodic phase, an interphase gap, then an equal-and-opposite anodic phase. Net DC delivered to the tissue: zero.
""")

both_code(r"""plot_pulse(amp_ua=80, pw_us=170, interphase_us=60,
           title='one biphasic pulse · 80 uA · 170 us · 60 us gap')
plt.tight_layout(); plt.show()
""")

# ---------------------------------------------------------------------------
# Section 2 - Five pulse parameters
# ---------------------------------------------------------------------------

both_md(r"""## 2 · The five pulse parameters

The mock — and the real driver — both take a `StimParams` dataclass with five per-electrode lists. The ranges below mirror the HTML page's §02 sliders.

| Parameter | Range | Notes |
|---|---|---|
| `amplitudes_ua` | 10 – 200 µA | per electrode; integer µA |
| `pulse_widths_us` | 50 – 500 µs | per phase, not total pulse |
| `interphase_us` | 0 – 200 µs | gap between the two phases |
| `frequencies_hz` | 10 – 300 Hz | one per electrode in normal mode |
| `num_pulses` | 1 – 100 | how many pulses make the train |

Charge per phase is the headline safety number: `Q_phase = amplitude × pulse_width / 1000` gives nC when the inputs are µA and µs.
""")

both_code(r"""params = StimParams(
    electrodes      = [42],
    amplitudes_ua   = [100],
    pulse_widths_us = [170.0],
    frequencies_hz  = [200.0],
    num_pulses      = [20],
)
print(params.to_dict())
""")

both_code(r"""plot_pulse(amp_ua=100, pw_us=170, interphase_us=60,
           freq_hz=200, num_pulses=4,
           title='train · 100 uA · 170 us · 200 Hz · 4 pulses')
plt.tight_layout(); plt.show()
""")

# Ex 2.1 - charge per phase
both_md(r"""### Exercise 2.1 — charge per phase `[easy]`

Compute the **charge per phase** for a given amplitude and pulse width, and check it against the **Shannon-k** safety inequality:

```
k = log10(Q_uC) + log10(D_uC_per_cm2)   should stay <= 1.85
```

where `Q_uC` is charge per phase in µC and `D_uC_per_cm2` is the same charge divided by the electrode tip area (Utah-array tip ≈ 1900 µm² → 2.0e-5 cm²). The 1.85 limit is the conservative macroelectrode line — microelectrodes routinely cross it.

1. Write `charge_per_phase_nc(amp_ua, pw_us)` returning nanocoulombs.
2. Write `shannon_k(amp_ua, pw_us, area_cm2=DEFAULT_UTAH_AREA_CM2)` returning k.
3. Print both for `(amp=80, pw=170)` and `(amp=200, pw=300)` — the first should be safely under 1.85, the second over.

> Hint: nC = µA × µs / 1000. µC = nC / 1000.
""")

split_code(
    r"""# Exercise 2.1 — charge per phase + Shannon k
# You have: DEFAULT_UTAH_AREA_CM2, SHANNON_K_LIMIT, math.log10
#
# def charge_per_phase_nc(amp_ua, pw_us) -> float: ...
# def shannon_k(amp_ua, pw_us, area_cm2=DEFAULT_UTAH_AREA_CM2) -> float: ...

# your code here

# Expected: (80, 170) -> Q ~ 13.6 nC, k ~ 1.05 -> safe
#           (200, 300) -> Q ~ 60.0 nC, k ~ 2.18 -> over limit
""",
    r"""# Exercise 2.1 — charge per phase + Shannon k
def charge_per_phase_nc(amp_ua, pw_us):
    return amp_ua * pw_us / 1000.0

def shannon_k(amp_ua, pw_us, area_cm2=DEFAULT_UTAH_AREA_CM2):
    q_uc = charge_per_phase_nc(amp_ua, pw_us) / 1000.0   # nC -> uC
    d    = q_uc / area_cm2                                # uC / cm^2
    return math.log10(q_uc) + math.log10(d)

for amp, pw in [(80, 170), (200, 300)]:
    q = charge_per_phase_nc(amp, pw)
    k = shannon_k(amp, pw)
    flag = 'SAFE' if k <= SHANNON_K_LIMIT else 'OVER LIMIT'
    print(f'amp={amp:3d} uA, pw={pw:3d} us  ->  Q={q:5.1f} nC, k={k:5.2f}  [{flag}]')
""",
)

# Ex 2.2 - us to 30 kHz cycles
both_md(r"""### Exercise 2.2 — µs to 30 kHz cycles `[intermediate]`

The Ripple Grapevine schedules everything on a **30,000 Hz tick** — every duration the hardware honours is rounded to the nearest **33.3 µs cycle**. That means you can't ask for a 170 µs pulse and get exactly 170 µs; you get whatever multiple of 33.3 µs is closest. This is the gap between what the slider says and what the electrode actually delivers.

1. Implement `us_to_cycles(us)` that returns the integer cycle count closest to `us` (with a minimum of 1, like the real driver).
2. Implement `cycles_to_us(c)` that goes the other way.
3. Round-trip 170, 60, and 500 µs through both functions; print the original µs, the cycle count, and the quantised µs.

> Hint: `round(us / CYCLE_US)` for the forward direction; multiply for the reverse. The minimum-1-cycle rule prevents zero-length phases.
""")

split_code(
    r"""# Exercise 2.2 — us to 30 kHz cycles
# Constant available: CYCLE_US = 33.3
#
# def us_to_cycles(us: float) -> int: ...        # round, min 1
# def cycles_to_us(c: int) -> float: ...

# your code here

# Expected (approx):
#   170 us -> 5 cycles -> 166.5 us
#    60 us -> 2 cycles ->  66.6 us
#   500 us -> 15 cycles -> 499.5 us
""",
    r"""# Exercise 2.2 — us to 30 kHz cycles
def us_to_cycles(us):
    return max(1, round(us / CYCLE_US))

def cycles_to_us(c):
    return c * CYCLE_US

for us in [170, 60, 500]:
    c   = us_to_cycles(us)
    rev = cycles_to_us(c)
    print(f'{us:5.1f} us -> {c:3d} cycles -> {rev:6.1f} us  '
          f'(error {abs(us - rev):4.1f} us)')
""",
)

# Ex 2.3 - interactive sweep
both_md(r"""### Exercise 2.3 — sweep amplitude × pulse width `[intermediate]`, **interactive**

Build a 2D map of charge per phase, with amplitude on the x-axis and pulse width on the y-axis. Overlay the **Shannon-k = 1.85** isoline so you can see at a glance which slider combinations would be blocked.

The `@interact` decorator below gives you sliders for the electrode area (changes the safety frontier — smaller electrodes hit the limit sooner) and the Shannon-k threshold. Fill in the body: build the meshgrid, compute `K` at every point, render `K` with `imshow`, and draw the isoline with `contour`.

> Hint: `A, P = np.meshgrid(amps, pws)` gives you (W, P) grids; `K = np.log10(A*P/1e6) + np.log10((A*P/1e6) / area)`. `ax.contour(A, P, K, levels=[k_limit])` draws the frontier.
""")

split_code(
    r"""# Exercise 2.3 — interactive amp x pw sweep
import ipywidgets as widgets
from ipywidgets import interact

amps = np.linspace(10, 250, 80)        # uA
pws  = np.linspace(40, 500, 80)        # us

@interact(area_um2=widgets.IntSlider(min=500, max=5000, step=100, value=1900,
                                     description='area (um^2)'),
          k_limit=widgets.FloatSlider(min=1.0, max=2.5, step=0.05, value=1.85,
                                      description='Shannon k'))
def _sweep(area_um2=1900, k_limit=1.85):
    area_cm2 = area_um2 * 1e-8
    # 1) Make the meshgrid of amplitude x pulse width
    # 2) Compute Q in uC and density in uC/cm^2
    # 3) Compute K = log10(Q) + log10(D)
    # 4) imshow(K) with origin='lower', extent=(amps.min, amps.max, pws.min, pws.max)
    # 5) contour(A, P, K, levels=[k_limit]) and label it
    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    # your code here

    ax.set_xlabel('amplitude (uA)'); ax.set_ylabel('pulse width (us)')
    ax.set_title(f'Shannon k  (area={area_um2} um^2, limit={k_limit:.2f})')
    plt.tight_layout(); plt.show()
""",
    r"""# Exercise 2.3 — interactive amp x pw sweep
import ipywidgets as widgets
from ipywidgets import interact

amps = np.linspace(10, 250, 80)
pws  = np.linspace(40, 500, 80)

@interact(area_um2=widgets.IntSlider(min=500, max=5000, step=100, value=1900,
                                     description='area (um^2)'),
          k_limit=widgets.FloatSlider(min=1.0, max=2.5, step=0.05, value=1.85,
                                      description='Shannon k'))
def _sweep(area_um2=1900, k_limit=1.85):
    area_cm2 = area_um2 * 1e-8
    A, P = np.meshgrid(amps, pws)
    Q_uC = A * P / 1e6
    D_uC = Q_uC / area_cm2
    K = np.log10(Q_uC) + np.log10(D_uC)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    im = ax.imshow(K, origin='lower', aspect='auto',
                   extent=(amps.min(), amps.max(), pws.min(), pws.max()),
                   cmap='magma')
    cs = ax.contour(A, P, K, levels=[k_limit], colors='#d86f91', linewidths=2)
    ax.clabel(cs, fmt=f'k={k_limit:.2f}')
    fig.colorbar(im, ax=ax, label='Shannon k')
    ax.set_xlabel('amplitude (uA)'); ax.set_ylabel('pulse width (us)')
    ax.set_title(f'Shannon k  (area={area_um2} um^2, limit={k_limit:.2f})')
    plt.tight_layout(); plt.show()
""",
)

# ---------------------------------------------------------------------------
# Section 3 - Utah array
# ---------------------------------------------------------------------------

both_md(r"""## 3 · Configure a Utah array

A Utah array is a 10×10 grid of microelectrodes — 96 active sites, 400 µm pitch — implanted in cortex. The mock indexes sites 1–96. The real driver maps each site to a Ripple channel via a fixed lookup (see [`neurolight2.stim.electrode_map`](https://github.com/) for the table). For workshop purposes we treat the site IDs as the addressable handle.

| Attribute | Value |
|---|---|
| sites | 96 active |
| layout | 10 × 10 (corners missing) |
| pitch | 400 µm |
| tip area | ~1900 µm² (= `DEFAULT_UTAH_AREA_CM2`) |
""")

both_code(r"""# Visualise the Utah grid. The four corners of a 10x10 layout are inactive on the
# standard Blackrock/Utah; here we just show the canonical 96 numbered sites.
def utah_grid_positions():
    positions = {}
    site = 1
    for r in range(10):
        for c in range(10):
            if (r, c) in {(0, 0), (0, 9), (9, 0), (9, 9)}:
                continue
            positions[site] = (c, 9 - r)   # x right, y up
            site += 1
    return positions

POS = utah_grid_positions()
xs, ys = zip(*POS.values())
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(xs, ys, s=120, facecolors='#fde7ef', edgecolors='#d86f91')
for sid, (x, y) in POS.items():
    ax.text(x, y, str(sid), ha='center', va='center', fontsize=7, color='#1c1c1a')
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-0.6, 9.6); ax.set_ylim(-0.6, 9.6)
ax.set_aspect('equal'); ax.set_title('Utah array · 96 sites')
plt.tight_layout(); plt.show()
""")

both_code(r"""# Three electrodes, three amplitudes, same train spec.
params3 = StimParams(
    electrodes      = [12, 45, 78],
    amplitudes_ua   = [80, 120, 60],
    pulse_widths_us = [170.0, 170.0, 170.0],
    frequencies_hz  = [200.0, 200.0, 200.0],
    num_pulses      = [10, 10, 10],
)
for i, e in enumerate(params3.electrodes):
    print(f'  site {e:3d}: {params3.amplitudes_ua[i]:3d} uA, '
          f'{params3.pulse_widths_us[i]:.0f} us, {params3.frequencies_hz[i]:.0f} Hz')
""")

# Ex 3.1 - paint a letter
both_md(r"""### Exercise 3.1 — paint a letter `[easy]`

Given a 10×10 boolean grid representing the letter "C", produce the list of `(site_id, amplitude_ua)` you would need to "draw" it at 100 µA. Use the same `utah_grid_positions()` mapping you saw above to translate grid cells to site IDs.

Sketch of the C pattern (1 = stimulate, 0 = off):

```
0 0 1 1 1 1 1 1 0 0
0 1 0 0 0 0 0 0 1 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0
0 0 1 1 1 1 1 1 0 0
```

1. Use the provided `letter_C()` to get a `(10, 10)` numpy boolean grid.
2. For each grid cell that is `True`, look up the matching site ID in `POS` (skip the four inactive corners).
3. Build `electrodes` and `amplitudes_ua` lists; wrap them in a `StimParams` with `pw=170`, `freq=200`, `num_pulses=10`.

> Hint: the grid's row 0 is at the top; `POS` puts `y = 9 - row` so y increases upward.
""")

both_code(r"""def letter_C():
    g = np.zeros((10, 10), dtype=bool)
    g[0, 2:8]   = True
    g[9, 2:8]   = True
    g[1, 1]    = g[1, 8] = True
    g[8, 1]    = g[8, 8] = True
    g[2:8, 0]   = True
    return g

C = letter_C()
plt.imshow(C, cmap='Pinks' if 'Pinks' in plt.colormaps() else 'pink_r')
plt.title('letter "C" pattern'); plt.axis('off'); plt.show()
""")

split_code(
    r"""# Exercise 3.1 — letter to StimParams
# Available: letter_C() -> (10,10) bool; POS: dict[site_id -> (x, y)] with y = 9 - row.
#
# Build a StimParams that stimulates every cell that is True, all at 100 uA,
# 170 us, 200 Hz, 10 pulses.

# your code here  ->  letter_params = StimParams(...)
""",
    r"""# Exercise 3.1 — letter to StimParams
C = letter_C()

# invert POS lookup: from (x, y) to site_id
xy_to_site = {(x, y): sid for sid, (x, y) in POS.items()}

active_sites = []
for r in range(10):
    for c in range(10):
        if not C[r, c]:
            continue
        y = 9 - r
        sid = xy_to_site.get((c, y))
        if sid is not None:
            active_sites.append(sid)

n = len(active_sites)
letter_params = StimParams(
    electrodes      = active_sites,
    amplitudes_ua   = [100] * n,
    pulse_widths_us = [170.0] * n,
    frequencies_hz  = [200.0] * n,
    num_pulses      = [10] * n,
)
print(f'letter "C" stimulates {n} sites: {active_sites}')
""",
)

# Ex 3.2 - interleaved offsets
both_md(r"""### Exercise 3.2 — interleaved multi-electrode timing `[intermediate]`

When several electrodes share the same frequency and pulse width, the controller staggers their start times so no two phases collide on the same 30 kHz cycle. The neurolight2 driver computes offsets equally spaced across one period of the train — see [`stim/interleaving.py`](file:///C:/Users/admin/neurolight2/neurolight2/stim/interleaving.py).

Implement `interleave_offsets(electrodes, freq_hz)`:

1. Compute the period: `period_us = 1e6 / freq_hz`.
2. Divide that period into `len(electrodes)` equal slots.
3. Assign offsets in **electrode-ID order** (lowest ID gets slot 0, next gets slot 1, etc), returned in **input order**.
4. The maximum offset must stay below one period.

> Hint: `sorted(range(n), key=lambda i: electrodes[i])` gives the ranks; place each rank at `rank * period / n`.
""")

split_code(
    r"""# Exercise 3.2 — interleave_offsets
# def interleave_offsets(electrodes: list[int], freq_hz: float) -> list[float]:
#     '''Per-electrode offsets in microseconds, returned in input order.'''
#     ...

# your code here

# Quick check (run after defining):
#   offsets = interleave_offsets([45, 12, 78], freq_hz=300)
#   site 12 is lowest -> rank 0 -> 0 us
#   site 45 -> rank 1 -> 1111 us  (period = 3333 us, /3 slots)
#   site 78 -> rank 2 -> 2222 us
#   returned in input order: [1111, 0, 2222]
""",
    r"""# Exercise 3.2 — interleave_offsets
def interleave_offsets(electrodes, freq_hz):
    n = len(electrodes)
    if n == 0:
        return []
    period_us = 1e6 / freq_hz
    slot_us = period_us / n
    ranks = sorted(range(n), key=lambda i: electrodes[i])
    offsets = [0.0] * n
    for rank, idx in enumerate(ranks):
        offsets[idx] = rank * slot_us
    return offsets

example = [45, 12, 78]
offsets = interleave_offsets(example, freq_hz=300)
print(f'electrodes {example} at 300 Hz -> offsets (us): '
      + ', '.join(f'{o:.1f}' for o in offsets))
print(f'max offset {max(offsets):.1f} us, period {1e6/300:.1f} us')
""",
)

both_md(r"""And a quick raster to confirm — each row is one electrode, each tick a pulse onset, over a 10 ms window. The staggered start times are what you'd see on a logic analyser tap of the Grapevine.""")

split_code(
    r"""# Visualise the interleaved raster (uses your interleave_offsets from 3.2).
# Plot pulse onsets for 6 electrodes at 300 Hz over a 10 ms window.
electrodes = [12, 45, 78, 33, 21, 60]
freq_hz = 300.0
window_ms = 10.0
n_pulses = int(window_ms / 1000 * freq_hz) + 1

# your code here:
#   1) call interleave_offsets(electrodes, freq_hz) -> offsets_us
#   2) for each electrode, compute pulse onsets: offset_us/1000 + k * (1000/freq_hz) for k in 0..n_pulses
#   3) eventplot or vlines over a (n_electrodes,) raster

# fig, ax = plt.subplots(figsize=(8, 3.2))
# ...
# plt.show()
""",
    r"""# Visualise the interleaved raster.
electrodes = [12, 45, 78, 33, 21, 60]
freq_hz = 300.0
window_ms = 10.0
n_pulses = int(window_ms / 1000 * freq_hz) + 1
offsets_us = interleave_offsets(electrodes, freq_hz)

fig, ax = plt.subplots(figsize=(8, 3.2))
for row, (e, off_us) in enumerate(zip(electrodes, offsets_us)):
    onsets_ms = [off_us / 1000 + k * (1000 / freq_hz) for k in range(n_pulses)]
    onsets_ms = [t for t in onsets_ms if t <= window_ms]
    ax.vlines(onsets_ms, row - 0.4, row + 0.4, color='#d86f91', lw=1.2)
ax.set_yticks(range(len(electrodes)))
ax.set_yticklabels([f'site {e}' for e in electrodes])
ax.set_xlabel('time (ms)'); ax.set_xlim(0, window_ms)
ax.set_title(f'interleaved onsets · {len(electrodes)} electrodes @ {freq_hz:.0f} Hz')
plt.tight_layout(); plt.show()
""",
)

# ---------------------------------------------------------------------------
# Section 4 - Fire the stimulator
# ---------------------------------------------------------------------------

both_md(r"""## 4 · Fire the stimulator

Everything above gets us to the call shape the real driver expects: `stim.stimulate(params) -> StimEvent`. The mock doesn't talk to any hardware, but it runs the same safety arithmetic — so a `safety_ok=True` here is a `safety_ok=True` on the real Grapevine too.
""")

both_code(r"""stim = MockRipple()
ev = stim.stimulate(StimParams(
    electrodes      = [42],
    amplitudes_ua   = [100],
    pulse_widths_us = [170.0],
    frequencies_hz  = [200.0],
    num_pulses      = [20],
))
print(ev)
print('history length:', len(stim.history))
""")

# Ex 4.1 - safety frontier
both_md(r"""### Exercise 4.1 — find the safety frontier `[intermediate]`

Sweep amplitude from 10 → 250 µA at fixed pw = 170 µs and num_pulses = 10. For each amplitude, call `stim.stimulate(...)` on a single-electrode trial and record `event.charge_per_phase_nc` and `event.safety_ok`. Plot charge vs amplitude, colouring points by safety status. Mark the amplitude at which the safety flag flips.

> Hint: instantiate a fresh `MockRipple()` so its history starts empty; `[ev.safety_ok for ev in stim.history]` will give you the boolean trace.
""")

split_code(
    r"""# Exercise 4.1 — safety frontier sweep
# 1) Make a fresh MockRipple.
# 2) Loop amp in range(10, 251, 10); for each amp call stim.stimulate(...).
# 3) Collect amp, charge_per_phase_nc, safety_ok arrays.
# 4) Scatter charge vs amp, colour by safety_ok.
# 5) Find and print the first amplitude where safety_ok flips False.

# your code here
""",
    r"""# Exercise 4.1 — safety frontier sweep
stim_sweep = MockRipple()
amps_sweep = list(range(10, 251, 10))
charges, oks = [], []
for amp in amps_sweep:
    ev = stim_sweep.stimulate(StimParams(
        electrodes=[1], amplitudes_ua=[amp],
        pulse_widths_us=[170.0], frequencies_hz=[200.0], num_pulses=[10],
    ))
    charges.append(ev.charge_per_phase_nc); oks.append(ev.safety_ok)

charges = np.array(charges); oks = np.array(oks)
amps_arr = np.array(amps_sweep)

flip = next((amp for amp, ok in zip(amps_sweep, oks) if not ok), None)
print(f'safety flips at amplitude = {flip} uA' if flip else 'never tripped under 250 uA')

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.scatter(amps_arr[oks], charges[oks], color='#1c1c1a', s=24, label='safe')
ax.scatter(amps_arr[~oks], charges[~oks], color='#8a3a1d', s=24, label='blocked')
if flip:
    ax.axvline(flip, color='#d86f91', lw=1.2, ls='--', label=f'frontier @ {flip} uA')
ax.set_xlabel('amplitude (uA)'); ax.set_ylabel('charge per phase (nC)')
ax.set_title('safety frontier · pw=170 us, freq=200 Hz, 10 pulses')
ax.legend(); ax.grid(True, alpha=0.2)
plt.tight_layout(); plt.show()
""",
)

# Ex 4.2 - multi-electrode trial
both_md(r"""### Exercise 4.2 — multi-electrode trial `[intermediate]`

Combine §3.1 (letter pattern) and §3.2 (interleaved offsets) into one `StimParams`, fire it through the mock, and confirm both `event.is_executed` and `event.safety_ok` are `True`. Print the returned event.

> Hint: `letter_params` from 3.1 already has the electrodes and amplitudes; just pass the offsets you compute with `interleave_offsets(letter_params.electrodes, freq_hz=200)` to a new `StimParams` constructor.
""")

split_code(
    r"""# Exercise 4.2 — multi-electrode trial
# Build a StimParams with the letter electrodes + interleaved offsets, fire it.

# your code here
""",
    r"""# Exercise 4.2 — multi-electrode trial
offsets = interleave_offsets(letter_params.electrodes, freq_hz=200.0)
letter_interleaved = StimParams(
    electrodes      = letter_params.electrodes,
    amplitudes_ua   = letter_params.amplitudes_ua,
    pulse_widths_us = letter_params.pulse_widths_us,
    frequencies_hz  = letter_params.frequencies_hz,
    num_pulses      = letter_params.num_pulses,
    offsets_us      = offsets,
)
stim_letter = MockRipple()
ev = stim_letter.stimulate(letter_interleaved)
print(ev)
print(f'is_executed={ev.is_executed} · safety_ok={ev.safety_ok}')
print(f'  {len(letter_interleaved.electrodes)} sites, '
      f'max offset {max(offsets):.0f} us, period {1e6/200.0:.0f} us')
""",
)

# ---------------------------------------------------------------------------
# Section 5 - Teaser
# ---------------------------------------------------------------------------

both_md(r"""## 5 · From electrodes to phosphenes — teaser

Each stimulated electrode produces one **phosphene** in the visual field. As a first sketch: brightness rises with frequency up to the refractory plateau (~250 Hz) and with amplitude above a threshold of ~30 µA. The full forward model lives in M4; this is just the bridge.

### Exercise 5.1 — drive M4's phosphene model `[challenge]`

1. Implement `phosphene_brightness(amp_ua, freq_hz)` returning a value in [0, 1]:
   - 0 below `amp_thresh = 30` µA
   - linear rise from threshold up to `amp_max = 200` µA
   - multiplied by `min(freq_hz / 250.0, 1.0)` to capture the refractory plateau
2. Render the 10×10 brightness map for your letter pattern.
3. Optional next step: open [`phosphene-simulation.ipynb`](https://github.com/NeuroTechHub/AIMD_bootcamp/blob/main/modules/phosphene-simulation/phosphene-simulation.ipynb) and feed your activations into the real dynaphos forward model.
""")

split_code(
    r"""# Exercise 5.1 — drive M4's phosphene model
# def phosphene_brightness(amp_ua: float, freq_hz: float) -> float: ...
# Then build a (10, 10) brightness array from letter_params + POS and imshow it.

# your code here
""",
    r"""# Exercise 5.1 — drive M4's phosphene model
def phosphene_brightness(amp_ua, freq_hz, amp_thresh=30, amp_max=200):
    amp_term  = max(0.0, min(1.0, (amp_ua - amp_thresh) / (amp_max - amp_thresh)))
    freq_term = min(freq_hz / 250.0, 1.0)
    return amp_term * freq_term

bright = np.zeros((10, 10), dtype=np.float32)
for i, sid in enumerate(letter_params.electrodes):
    x, y = POS[sid]
    row = 9 - y
    bright[row, x] = phosphene_brightness(
        letter_params.amplitudes_ua[i],
        letter_params.frequencies_hz[i],
    )

fig, ax = plt.subplots(figsize=(5, 5))
im = ax.imshow(bright, cmap='magma', vmin=0, vmax=1)
ax.set_title('letter "C" -> phosphene brightness map')
ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, ax=ax, label='brightness')
plt.tight_layout(); plt.show()
print(f'max brightness {bright.max():.2f} · active phosphenes {(bright > 0).sum()}')
""",
)

# ---------------------------------------------------------------------------
# Close
# ---------------------------------------------------------------------------

both_md(r"""---

**Done.** You've parameterised a biphasic train, quantised it to 30 kHz cycles, drawn a letter on a Utah array, staggered its electrodes to share a single 300 Hz slot, and fired the whole pattern through a Shannon-k safety checker. Swapping the inline mock for the real Grapevine is a one-line import: `from neurolight2.stim.factory import create_stimulator; stim = create_stimulator("mock_ripple")` — same `stimulate(params) -> StimEvent` contract, no other changes.

Module lead: see [`bootcamp-plan.html`](https://github.com/NeuroTechHub/AIMD_bootcamp/blob/main/bootcamp-plan.html). Edit this notebook directly; commit your additions to the bootcamp repo at the end of the day.
""")


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------

def _wrap(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_WORKSHOP.write_text(
        json.dumps(_wrap(WORKSHOP), indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OUT_SOLUTION.write_text(
        json.dumps(_wrap(SOLUTION), indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_WORKSHOP.relative_to(REPO)}  ({len(WORKSHOP)} cells)")
    print(f"wrote {OUT_SOLUTION.relative_to(REPO)}  ({len(SOLUTION)} cells)")


if __name__ == "__main__":
    main()
