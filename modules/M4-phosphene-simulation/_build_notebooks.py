"""Build the M4 M4-phosphene-simulation exercise + solution notebooks.

Both notebooks share content; the only difference is that "exercise" cells
ship blank in `phosphene-simulation.ipynb` and full in
`phosphene-simulation-solution.ipynb`.

Run:  python _build_notebooks.py
"""

from __future__ import annotations
import json
import os
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- cell helpers

def _src(text: str) -> list[str]:
    """nbformat stores sources as list-of-lines with trailing '\\n'."""
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + ([lines[-1]] if lines[-1] else [])


def _cell_id() -> str:
    return uuid.uuid4().hex[:8]


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": _cell_id(),
        "metadata": {},
        "source": _src(text.strip("\n") + "\n"),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "id": _cell_id(),
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": _src(text.strip("\n") + "\n"),
    }


def ex(solution: str, hint: str) -> dict:
    """An exercise cell: full code in the solution notebook, hint in the
    exercise notebook. Tagged with metadata so the splitter can find it."""
    cell = code(solution)
    cell["metadata"] = {"tags": ["exercise"], "exercise_hint": hint}
    return cell


# --------------------------------------------------------- shared yaml string

# dynaphos config/params.yaml (mirrors the version pinned by the HTML page,
# 0.1.3). We embed it so the notebook is self-contained: no pip-installed
# resource discovery, no separate download.
PARAMS_YAML = r"""
run:
  resolution: [256, 256]
  view_angle: 16
  origin: [0, 0]
  min_angle: 0.001
  fps: 35
  gpu: 0
  print_stats: False
  seed: 42
  dtype: float32
  use_gaussian_lut: False
  batch_size: 0
display:
  screen_resolution: [1920, 1080]
  screen_diagonal: 13.3
  dist_to_screen: 600
sampling:
  sampling_method: receptive_fields
  RF_size: 0.5
  stimulus_scale: 1.0e-4
cortex_model:
  model: dipole
  k: 17.3
  a: 0.75
  b: 120
  alpha: 0.95
  dropout_rate: 0.0
  noise_scale: 0.0
temporal_dynamics:
  trace_increase_rate: 13.95528162
  activation_decay_per_second: 0.00012340980408667956
  trace_decay_per_second: 0.99949191
size:
  size_equation: sqrt
  MD: 0.7
  I_half: 40
  radius_to_sigma: 0.5
  current_spread: 675.0e-6
thresholding:
  use_threshold: True
  activation_threshold: 9.141886e-08
  activation_threshold_sd: 0.0
  rheobase: 23.9e-6
default_stim:
  pw_default: 170.0e-6
  freq_default: 300
  relative_stim_duration: 1.0
brightness_saturation:
  use_brightness_saturation: True
  slope_brightness: 1.9152642500946816e+7
  cps_half: 1.057631e-07
gabor:
  gabor_filtering: False
  gamma: 0.5
"""


# ============================================================== build cells

CELLS: list[dict] = []


# --------------------------------------------------------------- title / intro

CELLS.append(md(r"""
# M4 — Phosphene simulation

**NTH bootcamp · Module 4**

The interactive companion page `M4-phosphene-simulation.html` lets you move
sliders and watch phosphenes change shape. This notebook does the same
thing in Python, against the *real* [`dynaphos`](https://github.com/neuralcodinglab/dynaphos)
library, and then takes one step further: it drives the simulator from
the output of computer-vision models you already met in M1 (YOLO
segmentation, depth estimation, saliency, open-vocabulary detection). The
goal is to see — with your own eyes — how the *upstream representation*
chosen by the engineer changes what a prosthesis user would actually
perceive.

1. Phosphene basis (single phosphene, populations)
2. Image → phosphenes (the classical forward pass)
3. Temporal dynamics (trace, adaptation, threshold)
4. **AI-driven stimulus** (YOLO, depth, saliency, open-vocab)
5. Dynamic stimulus loop (a moving scene through the simulator)

Exercises are tagged **`[easy]`**, **`[intermediate]`**, or **`[challenge]`**.
The challenges are genuinely hard; do not feel obliged to finish them in
the guided hour.
"""))


# --------------------------------------------------------------------- §0 setup

CELLS.append(md(r"""
## 0 · Setup

Required packages:

```bash
pip install numpy opencv-contrib-python matplotlib torch dynaphos ultralytics
```

We use `opencv-contrib-python` (not the smaller `opencv-python`) because §4
exercises rely on `cv2.saliency`, which ships only in the contrib build.
If you already have `opencv-python` installed, uninstall it first
(`pip uninstall -y opencv-python`) — the two cannot coexist.

The cell below imports everything, downloads `bus.jpg` and a kitten
photo if they aren't already in `assets/`, picks the best available
compute backend (GPU when present, else CPU), and defines a small
`show()` helper used throughout. Run it once.
"""))

CELLS.append(code(r"""
# Install all packages this notebook needs. Run once per kernel; skip if already installed.
%pip install -q numpy opencv-contrib-python matplotlib torch dynaphos ultralytics
"""))

CELLS.append(code(r"""
import os, sys, json, urllib.request, tempfile, textwrap, warnings
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch

ASSETS = Path('assets')
ASSETS.mkdir(exist_ok=True)

# bus.jpg — same image M1 uses (Ultralytics demo image, redistributable)
BUS = ASSETS / 'bus.jpg'
if not BUS.exists():
    urllib.request.urlretrieve('https://ultralytics.com/images/bus.jpg', BUS)
    print(f'downloaded {BUS}')

# cat.jpg — Wikimedia (André Karwath / "Aka", CC BY-SA 2.5), same source as the
# HTML §03 face preset. Cute kitten with strong silhouette + rich short-range
# edges (eyes, whiskers, fur boundaries) — ideal for the Canny demo below.
PORTRAIT = ASSETS / 'cat.jpg'
if not PORTRAIT.exists():
    url = ('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/'
           'Six_weeks_old_cat_%28aka%29.jpg/330px-Six_weeks_old_cat_%28aka%29.jpg')
    try:
        urllib.request.urlretrieve(url, PORTRAIT)
        print(f'downloaded {PORTRAIT}')
    except Exception as e:
        print("cat download failed (we'll generate a synthetic blob instead):", e)

print('versions:', 'numpy', np.__version__, '· cv2', cv2.__version__, '· torch', torch.__version__)
"""))

CELLS.append(code(r"""
# Pick the best available compute backend. GPU by default; CPU fallback.
if torch.cuda.is_available():
    DEVICE = 'cuda'
elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
    DEVICE = 'mps'      # Apple Silicon
else:
    DEVICE = 'cpu'
print('using device:', DEVICE)
"""))

CELLS.append(code(r"""
def show(*imgs, titles=None, cmap='gray', figsize=None, cols=None):
    '''Plot one or more images side-by-side. BGR images are auto-converted to RGB.'''
    if len(imgs) == 1 and isinstance(imgs[0], (list, tuple)):
        imgs = imgs[0]
    n = len(imgs)
    cols = cols or n
    rows = int(np.ceil(n / cols))
    figsize = figsize or (4*cols, 4*rows)
    fig, axes = plt.subplots(rows, cols, figsize=figsize, squeeze=False)
    for i, ax in enumerate(axes.flat):
        ax.axis('off')
        if i >= n: continue
        im = imgs[i]
        if hasattr(im, 'detach'):           # torch tensor
            im = im.detach().cpu().numpy()
        if im.ndim == 3 and im.shape[2] == 3:
            ax.imshow(cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2RGB))
        else:
            vmax = im.max() if im.dtype != np.uint8 else 255
            ax.imshow(im, cmap=cmap, vmin=0, vmax=vmax if vmax > 0 else 1)
        if titles and i < len(titles):
            ax.set_title(titles[i], fontsize=10)
    plt.tight_layout(); plt.show()
"""))


# --------------------------------------------------------- dynaphos params yaml

CELLS.append(md(r"""
We pin a copy of `dynaphos`'s `config/params.yaml` to a local file so the
rest of the notebook is reproducible. These are the same defaults the
HTML page is built against (rheobase 23.9 µA, current_spread 675 µA/mm²,
view angle 16°, fps 35, cortical dipole k=17.3 / a=0.75 / b=120). All
numbers come from the dynaphos repo. We tell dynaphos to use GPU 0 when
CUDA is available; otherwise its internal device picker falls back to
CPU.
"""))

CELLS.append(code(f"""
PARAMS_YAML = r'''{PARAMS_YAML.strip()}'''

PARAMS_PATH = ASSETS / 'params.yaml'
PARAMS_PATH.write_text(PARAMS_YAML)

# Patch the device hint based on the DEVICE we picked above. dynaphos reads
# params['run']['gpu'] internally and uses it to decide where to put tensors.
import re
if DEVICE != 'cuda':
    txt = PARAMS_PATH.read_text()
    txt = re.sub(r'^(\\s*gpu:).*$', r'\\1 -1', txt, flags=re.MULTILINE)
    PARAMS_PATH.write_text(txt)
print('wrote', PARAMS_PATH)
"""))


# ============================================================== §1 basis

CELLS.append(md(r"""
## 1 · Phosphene basis

Every phosphene is a **2-D Gaussian** sitting on the visual field. Its
*centre* comes from the retinotopic map (eccentricity + polar angle);
its *size* is set jointly by the current and the local **cortical
magnification** $M(r)$ — the millimetres of cortex devoted to one
degree of visual angle. The fovea has high magnification, so the same
current spreads over fewer degrees and produces a small, sharp dot. The
periphery has low magnification, so the same current paints a much
larger blob.

$$\sigma(\text{deg}) \;=\; s \cdot \frac{\sqrt{I/K}}{M(r)}, \qquad
  M(r) \;=\; \frac{k\,(b-a)}{(r+a)(r+b)}$$

with $s$ = `radius_to_sigma`, $K$ = `current_spread`. We will build a
population of electrodes and visualise this directly.
"""))

CELLS.append(code(r"""
from dynaphos.utils import load_params, Map
from dynaphos.cortex_models import (
    get_visual_field_coordinates_probabilistically,
    get_cortical_magnification,
)
from dynaphos.simulator import GaussianSimulator

params = load_params(str(PARAMS_PATH))
rng = np.random.default_rng(params['run']['seed'])

# Foveated population: probability of placing an electrode is proportional to M(r).
N = 600
coords = get_visual_field_coordinates_probabilistically(params, N, rng=rng)
sim = GaussianSimulator(params, coords)
print(f'simulator has {len(coords)} electrodes; phosphenes rendered as '
      f'{tuple(params["run"]["resolution"])} pixel image, '
      f'{params["run"]["view_angle"]}° wide field')
"""))

CELLS.append(code(r"""
# Render the whole population once — fire every electrode at the same current.
amp = torch.full((len(coords),), 80e-6)   # 80 µA per electrode
sim.reset()
phosphenes = sim(amp).detach().cpu().numpy()
show(phosphenes, titles=[f'{len(coords)} phosphenes, 80 µA each (foveated layout)'],
     figsize=(5, 5))
"""))

CELLS.append(md(r"""
The dynaphos library ships a probabilistic foveated sampler
(`get_visual_field_coordinates_probabilistically`) but no parameterised
uniform-grid sampler in the visual field. We build one ourselves with a
tiny helper that wraps the `Map` class.
"""))

CELLS.append(code(r"""
def make_uniform_visual_field(side: int, view_angle: float) -> Map:
    '''Side×side electrodes spaced evenly inside [-view_angle/2, +view_angle/2].'''
    hemi = view_angle / 2
    step = view_angle / side
    xs = np.linspace(-hemi + step/2, hemi - step/2, side)
    ys = np.linspace(-hemi + step/2, hemi - step/2, side)
    xx, yy = np.meshgrid(xs, ys)
    return Map(x=xx.ravel(), y=yy.ravel())
"""))

CELLS.append(md(r"""
### Exercise 1.1 — phosphene size grows with eccentricity `[easy]`

Use the magnification function directly to plot how the phosphene size
$\sigma_{\text{deg}}$ scales with eccentricity at a fixed current.

1. Pick `I = 80e-6` (Amperes) and `K = params['size']['current_spread']`.
2. Compute `radius_mm = np.sqrt(I / K)` (the diameter of activated cortex
   per Bosking et al.'s sqrt law).
3. Sweep eccentricity `r` from `0.5°` to `7.5°`. For each `r`, use
   `get_cortical_magnification(r, params['cortex_model'])` and compute
   `sigma_deg = s * radius_mm / M(r)` with `s = params['size']['radius_to_sigma']`.
4. Plot `sigma_deg` vs `r`. It should curve upward — small at the fovea,
   large at the periphery.
"""))

CELLS.append(ex(
    solution=r"""
I_amp = 80e-6
K = params['size']['current_spread']
s = params['size']['radius_to_sigma']
radius_mm = np.sqrt(I_amp / K)

rs = np.linspace(0.5, 7.5, 80)
Ms = np.array([float(get_cortical_magnification(np.array([r]), params['cortex_model'])[0])
               for r in rs])
sigma_deg = s * radius_mm / Ms

plt.figure(figsize=(5, 3.2))
plt.plot(rs, sigma_deg)
plt.xlabel('eccentricity r (deg)')
plt.ylabel('phosphene σ (deg)')
plt.title(f'σ_deg vs eccentricity at I = {I_amp*1e6:.0f} µA')
plt.grid(alpha=0.3); plt.tight_layout(); plt.show()
""",
    hint=r"""
# your code here
# Hint: K = params['size']['current_spread']
#       s = params['size']['radius_to_sigma']
#       radius_mm = np.sqrt(I / K)
#       For each r in np.linspace(0.5, 7.5, 80):
#           M = get_cortical_magnification(np.array([r]), params['cortex_model'])[0]
#           sigma_deg = s * radius_mm / M
""",
))

CELLS.append(md(r"""
### Exercise 1.2 — foveated vs uniform electrode layout `[intermediate]`

With the same N electrodes, two layout strategies give very different
percepts. Build them both and render the max-projection basis map for each.

1. Build a foveated population with `get_visual_field_coordinates_probabilistically(params, N, rng=rng)`.
2. Build a uniform population with `get_visual_field_coordinates_grid(params, N_x, N_y, view_angle)`.
   (`N_x = N_y ≈ sqrt(N)` so the total matches.)
3. Wrap each in a `GaussianSimulator(params, coords)`.
4. Fire every electrode at 80 µA and render. Plot side-by-side.
5. Look at the centre vs the edge — which layout gives finer central
   detail, which finer peripheral detail?
"""))

CELLS.append(ex(
    solution=r"""
N = 600
side = int(round(np.sqrt(N)))   # 24×24 ≈ 576, close enough to 600

rng = np.random.default_rng(params['run']['seed'])
coords_fov = get_visual_field_coordinates_probabilistically(params, N, rng=rng)
coords_uni = make_uniform_visual_field(side, params['run']['view_angle'])

sim_fov = GaussianSimulator(params, coords_fov)
sim_uni = GaussianSimulator(params, coords_uni)

amp_fov = torch.full((len(coords_fov),), 80e-6)
amp_uni = torch.full((len(coords_uni),), 80e-6)

sim_fov.reset(); sim_uni.reset()
ph_fov = sim_fov(amp_fov).detach().cpu().numpy()
ph_uni = sim_uni(amp_uni).detach().cpu().numpy()

show(ph_fov, ph_uni,
     titles=[f'foveated (N={len(coords_fov)})',
             f'uniform grid ({side}×{side}={len(coords_uni)})'],
     cols=2, figsize=(9, 4.5))
""",
    hint=r"""
# your code here
# Hint: side = int(round(np.sqrt(N)))
#       coords_fov = get_visual_field_coordinates_probabilistically(params, N, rng=rng)
#       coords_uni = make_uniform_visual_field(side, params['run']['view_angle'])
#       Wrap each in GaussianSimulator(params, coords_...) and fire 80 µA on every electrode.
""",
))


# ============================================================== §2 forward pass

CELLS.append(md(r"""
## 2 · Image → phosphenes (forward pass)

This is the engineer's job: turn an image into a set of stimulation
amplitudes, one per electrode. The simulator's `sample_stimulus(image)`
does this by sampling the image intensity at each electrode's receptive
field. Then `simulator(amplitudes)` runs the physics and renders the
phosphene image.

The signature you'll use over and over:

```python
amplitudes = simulator.sample_stimulus(image, rescale=True)   # (N_electrodes,)
phosphenes = simulator(amplitudes)                            # (H, W), in [0, 1]
```

Input `image` is a `(H, W)` uint8 or float array at the resolution
declared in the params file (256×256 here). `rescale=True` maps the
image's [0, max] range to a reasonable stim amplitude band.
"""))

CELLS.append(code(r"""
RES = tuple(params['run']['resolution'])   # (W, H) — 256, 256

def draw_pattern(name: str) -> np.ndarray:
    '''Return a 256×256 grayscale uint8 image for one of the abstract presets.'''
    img = np.zeros(RES[::-1], dtype=np.uint8)
    h, w = img.shape
    if name == 'square_disc':
        cv2.rectangle(img, (60, 60), (160, 160), 255, -1)
        cv2.circle(img, (190, 190), 40, 255, -1)
    elif name == 'letter_E':
        cv2.putText(img, 'E', (40, 210), cv2.FONT_HERSHEY_SIMPLEX, 8.0, 255, 18, cv2.LINE_AA)
    elif name == 'grating':
        for x in range(0, w, 16):
            cv2.rectangle(img, (x, 0), (x+8, h), 255, -1)
    elif name == 'diagonal':
        cv2.line(img, (20, 20), (w-20, h-20), 255, 6, cv2.LINE_AA)
    else:
        raise ValueError(name)
    return img

# Rebuild a fresh simulator that we'll use for §2-§4. Foveated, 1000 electrodes
# so the abstract shapes have something to bind to.
N = 1000
coords = get_visual_field_coordinates_probabilistically(params, N, rng=np.random.default_rng(0))
sim = GaussianSimulator(params, coords)

def render(image_uint8: np.ndarray) -> np.ndarray:
    '''image_uint8 -> phosphene render (H, W) float in [0, 1].'''
    sim.reset()
    amp = sim.sample_stimulus(image_uint8, rescale=True)
    return sim(amp).detach().cpu().numpy()

target = draw_pattern('square_disc')
show(target, render(target), titles=['target', 'phosphene render'], cols=2, figsize=(8, 4))
"""))

CELLS.append(md(r"""
### Exercise 2.1 — abstract patterns survive coarse sampling `[easy]`

Loop over the four preset patterns and render each through the
simulator. Display a 2×4 grid: top row = targets, bottom row = phosphene
renders. Which ones stay recognisable, which fall apart?

> Hint: the patterns are `['square_disc', 'letter_E', 'grating', 'diagonal']`.
> Build two lists (`targets`, `renders`) and call
> `show(*(targets + renders), titles=..., cols=4)`.
"""))

CELLS.append(ex(
    solution=r"""
names = ['square_disc', 'letter_E', 'grating', 'diagonal']
targets = [draw_pattern(n) for n in names]
renders = [render(t) for t in targets]
show(*(targets + renders),
     titles=names + [f'{n} → phosphenes' for n in names],
     cols=4, figsize=(14, 7))
""",
    hint=r"""
# your code here
# Hint:
#   names = ['square_disc', 'letter_E', 'grating', 'diagonal']
#   targets = [draw_pattern(n) for n in names]
#   renders = [render(t) for t in targets]
#   show(*(targets + renders), titles=..., cols=4)
""",
))

CELLS.append(md(r"""
### Exercise 2.2 — natural photos: blobs, then edges `[intermediate]`

Now try a real photo. First push the cat through the simulator raw
(just resized to 256×256, grayscale). You should get a featureless
bright blob — the silhouette of the kitten's head and body. Then
preprocess with `cv2.Canny` first, and pass the edge map through the
same simulator.

1. Load `PORTRAIT` with `cv2.imread(str(PORTRAIT), cv2.IMREAD_GRAYSCALE)`. If
   the download failed, fall back to a synthetic blob:
   `face = np.zeros(RES[::-1], np.uint8); cv2.ellipse(face, (128,128), (60,80), 0, 0, 360, 255, -1)`.
2. Resize to `RES`, render. Plot input + render.
3. `edges = cv2.Canny(cv2.GaussianBlur(face, (5,5), 1.4), 50, 150)`. Render
   the edges instead. Plot input + edges + edge-render.
4. Which carries more recognisable cat-ness through the prosthesis — the
   raw intensity or the edges?
"""))

CELLS.append(ex(
    solution=r"""
face = cv2.imread(str(PORTRAIT), cv2.IMREAD_GRAYSCALE)
if face is None:
    face = np.zeros(RES[::-1], np.uint8)
    cv2.ellipse(face, (128, 128), (60, 80), 0, 0, 360, 255, -1)
face = cv2.resize(face, RES)

raw_render = render(face)
edges = cv2.Canny(cv2.GaussianBlur(face, (5, 5), 1.4), 50, 150)
edge_render = render(edges)

show(face, raw_render, edges, edge_render,
     titles=['kitten', 'raw → phosphenes', 'Canny edges', 'edges → phosphenes'],
     cols=4, figsize=(14, 4))
""",
    hint=r"""
# your code here
# Hint:
#   face = cv2.imread(str(PORTRAIT), cv2.IMREAD_GRAYSCALE)
#   if face is None: <fallback to a synthetic ellipse>
#   face = cv2.resize(face, RES)
#   raw_render = render(face)
#   edges = cv2.Canny(cv2.GaussianBlur(face, (5,5), 1.4), 50, 150)
#   edge_render = render(edges)
#   show(face, raw_render, edges, edge_render, titles=[...], cols=4)
""",
))


# ============================================================== §3 temporal

CELLS.append(md(r"""
## 3 · Temporal dynamics

Until now we have been treating the simulator as a one-shot image
operator: stimulus in, phosphene image out. In real cortex, the percept
*evolves*. Two effects dominate:

* **Activation build-up + decay** — when stimulation starts the cell
  takes a few frames to integrate charge; when it stops the activation
  leaks back to zero. With the dynaphos defaults this is nearly
  instantaneous, but we can slow it down with the `activation_decay`
  slider for visualisation.
* **Adaptation (trace)** — a slow "fatigue" state $B$ accumulates while
  the cell is being driven. It adds to the leak, so the effective
  current shrinks and the percept fades within ~1 s even when the
  stimulation has not moved.

The cell below runs the simulator for 140 frames at 35 fps (= 4 s),
holding the current constant. We plot the brightness curve so you can
see the adaptation bend it down.

> **Speed tip.** Each frame is a full forward pass through every
> electrode. The N=1000 simulator from §2 makes that slow on CPU, and §3
> only needs a *temporal* readout (mean brightness vs time), not a fine
> spatial render — so we build a smaller, fast `sim_t` here with
> N=200 electrodes. On a typical laptop CPU the demo should finish in
> under 10 seconds; the two exercises that follow each run two or three
> of these sweeps, so budget ~30 seconds for §3 total. If it is still
> too slow, drop `frames` to 70.
"""))

CELLS.append(code(r"""
# Dedicated small simulator for §3 — temporal dynamics only need a
# mean-brightness readout, not a full 1000-electrode spatial render.
sim_t = GaussianSimulator(
    params,
    get_visual_field_coordinates_probabilistically(
        params, 200, rng=np.random.default_rng(7)),
)
print(f'sim_t has {sim_t.num_phosphenes} electrodes (fast path for §3)')
"""))

CELLS.append(code(r"""
def run_sequence(sim, image_uint8, frames=140, stim_on_until=None,
                 act_decay_per_sec=None, no_trace=False):
    '''Run a sustained-stim sequence and return (mean_brightness_per_frame,
    mean_trace_per_frame).

    `act_decay_per_sec` uses the same semantics as the dynaphos yaml field
    `activation_decay_per_second` and as the M4 HTML slider: smaller values
    = faster decay (sharp on/off edges); larger values = slower decay
    (rounded ramps). The helper converts to the internal decay_rate.

    `no_trace=True` suppresses the trace (adaptation) state.'''
    if stim_on_until is None:
        stim_on_until = frames // 2
    sim.reset()

    orig_decay = None
    if act_decay_per_sec is not None:
        orig_decay = sim.activation.decay_rate.clone()
        sim.activation.decay_rate = torch.tensor(-float(np.log(act_decay_per_sec)))

    n_e = sim.num_phosphenes
    bright = np.zeros(frames)
    trace_mean = np.zeros(frames)
    for t in range(frames):
        if t < stim_on_until:
            amp = sim.sample_stimulus(image_uint8, rescale=True)
        else:
            amp = torch.zeros(n_e)
        phos = sim(amp)
        if no_trace:
            sim.trace.reset()       # zero the trace each frame
        bright[t] = float(phos.detach().mean())
        trace_mean[t] = float(sim.trace.get().detach().mean())

    if orig_decay is not None:
        sim.activation.decay_rate = orig_decay
    return bright, trace_mean

# A small bright square as the sustained stimulus.
stim_img = draw_pattern('square_disc')
FRAMES = 140
bright, trace = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=FRAMES)

t = np.arange(FRAMES) / params['run']['fps']
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(t, bright, label='mean phosphene brightness', color='C0')
ax2 = ax.twinx()
ax2.plot(t, trace, '--', label='mean trace B', color='C1', alpha=0.7)
ax.set_xlabel('time (s)'); ax.set_ylabel('brightness'); ax2.set_ylabel('trace')
ax.set_title('Sustained stim, constant current — brightness fades while trace climbs')
ax.legend(loc='upper left'); ax2.legend(loc='upper right')
plt.tight_layout(); plt.show()
"""))

CELLS.append(md(r"""
### Exercise 3.1 — softer ramp with slower activation `[easy]`

The yaml default for `activation_decay_per_second` is `1.23e-4`, which
makes the activation integrator essentially instantaneous: brightness
jumps to peak in one frame. Slowing it down rounds the corners of the
brightness curve.

Sweep three values of `act_decay_per_sec` — `1e-3`, `1e-1`, `3e-1` — and overlay
the three resulting brightness curves on the same plot. Use
`stim_on_until=40` so the stim turns off mid-window and you can see the
tail too. Use the fast `sim_t` from the demo.
"""))

CELLS.append(ex(
    solution=r"""
plt.figure(figsize=(7, 3))
for d in [1e-3, 1e-1, 3e-1]:
    b, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=d)
    plt.plot(np.arange(FRAMES) / params['run']['fps'], b, label=f'act_decay={d:g}')
plt.axvspan(0, 40/params['run']['fps'], color='C0', alpha=0.08, label='stim ON')
plt.xlabel('time (s)'); plt.ylabel('brightness')
plt.title('activation decay controls how sharp the on/off edges are')
plt.legend(); plt.tight_layout(); plt.show()
""",
    hint=r"""
# your code here
# Hint:
#   for d in [1e-3, 1e-1, 3e-1]:
#       b, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=d)
#       plt.plot(np.arange(FRAMES) / params['run']['fps'], b, label=f'act_decay={d:g}')
#   Use plt.axvspan to shade the stim-ON window.
""",
))

CELLS.append(md(r"""
### Exercise 3.2 — adaptation vs. activation leak `[intermediate]`

Set `stim_on_until=40`, `act_decay_per_sec=3e-1`, and a constant current. Run
the sequence **twice** (using `sim_t`): once normally (with adaptation),
once with `no_trace=True` (adaptation disabled). Plot the two brightness
curves on the same axes.

The brightness drop in the first half of the *normal* curve is
trace-driven adaptation; the drop in the second half (after stim turns
off) is the activation integrator leaking out. With `no_trace=True` you
should see a flat plateau followed by the same leak tail — confirming
that the bend in the middle is the trace's doing, not the integrator's.
"""))

CELLS.append(ex(
    solution=r"""
b_norm, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=3e-1)
b_flat, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=3e-1, no_trace=True)
t = np.arange(FRAMES) / params['run']['fps']

plt.figure(figsize=(7, 3))
plt.plot(t, b_norm, label='trace ON (adaptation)')
plt.plot(t, b_flat, label='trace suppressed')
plt.axvspan(0, 40/params['run']['fps'], color='C0', alpha=0.08, label='stim ON')
plt.xlabel('time (s)'); plt.ylabel('brightness')
plt.title('the mid-window bend is the trace; the tail is the integrator')
plt.legend(); plt.tight_layout(); plt.show()
""",
    hint=r"""
# your code here
# Hint:
#   b_norm, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=3e-1)
#   b_flat, _ = run_sequence(sim_t, stim_img, frames=FRAMES, stim_on_until=40, act_decay_per_sec=3e-1, no_trace=True)
#   Plot both curves on one axis and shade the stim-ON window.
""",
))


# ========================================================== §4 AI-driven

CELLS.append(md(r"""
## 4 · AI-driven stimulus

Up to here, the stimulus was either an abstract shape or a raw photo
intensity sampled at each electrode. Real prostheses don't have to work
that way — the input to `sim.sample_stimulus(...)` can be **anything**
you can compute from the camera. This section drives the same simulator
from the outputs of four computer-vision models and compares the resulting
phosphene renders.

* **4.1** YOLOv8n-seg — class-weighted object masks
* **4.2** MiDaS — monocular depth, near = bright
* **4.3** OpenCV spectral-residual saliency — "where the user would look"
* **4.4** YOLO-World — open-vocabulary detection from a free-text class list

We run all of them on `bus.jpg` (the M1 image) so the renders are
visually comparable.
"""))

CELLS.append(code(r"""
# Load and resize bus.jpg to the simulator's resolution.
bgr = cv2.imread(str(BUS))
scene_gray = cv2.resize(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), RES)
scene_bgr  = cv2.resize(bgr, RES)
show(scene_bgr, render(scene_gray),
     titles=['scene (raw intensity input)', 'phosphenes from raw intensity'],
     cols=2, figsize=(8, 4))
"""))

CELLS.append(md(r"""
### YOLO segmentation → phosphenes

YOLOv8n-seg returns one binary mask per detection. We collapse them into
a single "objects vs background" activation map and feed *that* in
instead of raw pixels. Things that aren't objects (sky, pavement) go
dark; people, vehicles, etc. light up.
"""))

CELLS.append(code(r"""
yolo_ok = False
try:
    from ultralytics import YOLO
    yolo_model = YOLO('yolov8n-seg.pt')
    yolo_res = yolo_model.predict(str(BUS), device=DEVICE, verbose=False)[0]
    yolo_ok = True
    print(f'YOLO ran on {DEVICE}. {len(yolo_res.boxes)} detections.')
except Exception as e:
    print('YOLO unavailable, will fall back to brightness threshold:', e)

def get_yolo_masks_resized(out_shape):
    '''Return (masks (N,H,W) uint8, class_ids (N,), names dict).'''
    if not yolo_ok:
        # Fallback: split bright-vs-dim regions of the scene as a 1-class "mask"
        m = (scene_gray > 110).astype(np.uint8)
        return m[None, :, :], np.array([0]), {0: 'bright'}
    raw = yolo_res.masks.data.cpu().numpy()
    H, W = out_shape
    masks = np.stack([
        (cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR) > 0.5).astype(np.uint8)
        for m in raw
    ])
    cls = yolo_res.boxes.cls.cpu().numpy().astype(int)
    return masks, cls, yolo_res.names

masks, cls, names = get_yolo_masks_resized(RES[::-1])
union = (np.any(masks.astype(bool), axis=0).astype(np.uint8) * 255)
show(scene_bgr, union, render(union),
     titles=['scene', 'YOLO object union', 'phosphenes from YOLO union'],
     cols=3, figsize=(12, 4))
"""))

CELLS.append(md(r"""
### Exercise 4.1 — class-weighted activation `[easy]`

Not every class is equally informative for a prosthesis user. Build a
single `(H, W)` float map where each pixel takes the **largest** weight
of any object covering it, using
`weights = {'person': 1.0, 'bus': 0.5, 'skateboard': 0.2}`. Multiply by
255, cast to uint8, and feed through `render(...)`. People should be the
brightest blobs in the resulting phosphene render.

Variables already in scope: `masks` `(N, H, W)`, `cls` `(N,)`,
`names` `dict[int,str]`.
"""))

CELLS.append(ex(
    solution=r"""
weights = {'person': 1.0, 'bus': 0.5, 'skateboard': 0.2}
canvas = np.zeros(RES[::-1], dtype=np.float32)
for m, c in zip(masks, cls):
    w = weights.get(names[int(c)], 0.0)
    if w > 0:
        canvas = np.maximum(canvas, w * m.astype(np.float32))
weighted = (canvas * 255).astype(np.uint8)

show(scene_bgr, weighted, render(weighted),
     titles=['scene', 'class-weighted map', 'phosphenes (weighted)'],
     cols=3, figsize=(12, 4))
""",
    hint=r"""
# your code here
# Hint:
#   weights = {'person': 1.0, 'bus': 0.5, 'skateboard': 0.2}
#   canvas = np.zeros(RES[::-1], dtype=np.float32)
#   for m, c in zip(masks, cls):
#       w = weights.get(names[int(c)], 0.0)
#       canvas = np.maximum(canvas, w * m.astype(np.float32))
#   weighted = (canvas * 255).astype(np.uint8)
#   show(...); render(weighted)
""",
))

CELLS.append(md(r"""
### Exercise 4.2 — monocular depth → phosphenes `[intermediate]`

A prosthesis built for **navigation** cares about *what's close*, not
*what's bright*. Use the MiDaS small monocular-depth model to estimate
relative depth, then make a "near = bright" activation map.

1. Load MiDaS via `torch.hub`:
   `midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small').to(DEVICE).eval()`
2. Get its preprocessing transform:
   `transform = torch.hub.load('intel-isl/MiDaS', 'transforms').small_transform`
3. Run on `cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2RGB)`, getting a `(H, W)`
   depth map. (MiDaS returns inverse depth: larger = closer.)
4. Normalise to `[0, 255]` uint8 (already near = bright since it's inverse
   depth), resize to `RES`, render.
5. Display the depth map alongside its phosphene render.

If MiDaS isn't available, fall back to `cv2.applyColorMap`-free
brightness inversion as a stand-in (`(255 - scene_gray)`).
"""))

CELLS.append(ex(
    solution=r"""
depth_ok = False
try:
    midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small', trust_repo=True).to(DEVICE).eval()
    transforms = torch.hub.load('intel-isl/MiDaS', 'transforms', trust_repo=True)
    transform = transforms.small_transform
    rgb = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2RGB)
    inp = transform(rgb).to(DEVICE)
    with torch.no_grad():
        pred = midas(inp)
        pred = torch.nn.functional.interpolate(
            pred.unsqueeze(1), size=RES[::-1], mode='bicubic', align_corners=False
        ).squeeze().cpu().numpy()
    depth = pred
    depth_ok = True
except Exception as e:
    print('MiDaS unavailable, falling back to brightness inversion:', e)
    depth = (255.0 - scene_gray).astype(np.float32)

depth_u8 = ((depth - depth.min()) / (np.ptp(depth) + 1e-9) * 255).astype(np.uint8)
show(scene_bgr, depth_u8, render(depth_u8),
     titles=['scene', 'near = bright (MiDaS)' if depth_ok else 'near = bright (fallback)',
             'phosphenes from depth'], cols=3, figsize=(12, 4))
""",
    hint=r"""
# your code here
# Hint (MiDaS):
#   midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small', trust_repo=True).to(DEVICE).eval()
#   transform = torch.hub.load('intel-isl/MiDaS', 'transforms', trust_repo=True).small_transform
#   rgb = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2RGB)
#   inp = transform(rgb).to(DEVICE)
#   with torch.no_grad():
#       pred = midas(inp)
#       pred = torch.nn.functional.interpolate(pred.unsqueeze(1), size=RES[::-1],
#                                              mode='bicubic', align_corners=False).squeeze()
#   depth = pred.cpu().numpy()
#   depth_u8 = normalise depth to uint8
# Fallback: depth = (255.0 - scene_gray).astype(np.float32)
""",
))

CELLS.append(md(r"""
### Exercise 4.3 — saliency → phosphenes `[intermediate]`

A "where would the user actually look?" model. OpenCV ships a static
spectral-residual saliency detector that runs on CPU and needs no
weights download.

1. `sal = cv2.saliency.StaticSaliencySpectralResidual_create()`
2. `ok, smap = sal.computeSaliency(scene_bgr)` — `smap` is a float32
   `(H, W)` in `[0, 1]`.
3. Threshold + scale to uint8 (e.g. `(smap > 0.4).astype(np.uint8) * 255`),
   resize to `RES`, render.
4. Display the saliency map alongside the phosphene render.

What does the prosthesis "show" the user under this regime?
"""))

CELLS.append(ex(
    solution=r"""
if hasattr(cv2, 'saliency'):
    sal = cv2.saliency.StaticSaliencySpectralResidual_create()
    _, smap = sal.computeSaliency(scene_bgr)
else:
    # opencv-python (no contrib) — fall back to a pure-numpy spectral residual.
    g = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    F = np.fft.fft2(g)
    log_amp = np.log(np.abs(F) + 1e-9)
    avg = cv2.boxFilter(log_amp, -1, (3, 3))
    spec_res = log_amp - avg
    sm = np.abs(np.fft.ifft2(np.exp(spec_res + 1j*np.angle(F))))**2
    smap = cv2.GaussianBlur(sm, (9, 9), 2.5)
    smap = (smap - smap.min()) / (np.ptp(smap) + 1e-9)
    print('using numpy spectral-residual fallback (no cv2.saliency available)')

smap_u8 = cv2.resize((smap * 255).astype(np.uint8), RES)
# threshold to emphasise the top-attended regions
sal_stim = ((smap_u8 > 100).astype(np.uint8) * 255)

show(scene_bgr, smap_u8, sal_stim, render(sal_stim),
     titles=['scene', 'saliency map (raw)', 'saliency (thresholded)', 'phosphenes from saliency'],
     cols=4, figsize=(16, 4))
""",
    hint=r"""
# your code here
# Hint:
#   sal = cv2.saliency.StaticSaliencySpectralResidual_create()
#   _, smap = sal.computeSaliency(scene_bgr)           # float32 in [0,1]
#   smap_u8 = cv2.resize((smap * 255).astype(np.uint8), RES)
#   sal_stim = (smap_u8 > 100).astype(np.uint8) * 255
#   show(scene_bgr, smap_u8, sal_stim, render(sal_stim), titles=..., cols=4)
""",
))

CELLS.append(md(r"""
### Exercise 4.4 — open-vocabulary prompts `[challenge]`

YOLOv8 sees only the 80 COCO classes. **YOLO-World** accepts a free-text
class list and finds whatever you ask for — "stop sign", "crosswalk",
"door". The challenge is authoring the class list so the resulting
phosphene render is **legible**: pick few large objects, not many small
ones.

```python
from ultralytics import YOLO
ovw = YOLO('yolov8s-world.pt')                              # downloads ~50 MB on first run
ovw.set_classes(['bus', 'person', 'door'])
ov_res = ovw.predict(str(BUS), device=DEVICE, verbose=False)[0]
```

1. Get the boxes from `ov_res.boxes.xyxy.cpu().numpy()`. (YOLO-World
   gives bounding boxes; for segmentation masks you'd swap in
   `yoloe-11s-seg.pt`.)
2. Build a binary mask: for each box, paint a filled rectangle of 255
   into a zeros canvas of shape `RES[::-1]`.
3. Render and display.

Try a few class lists. What happens to the render as you add more, smaller objects?
"""))

CELLS.append(ex(
    solution=r"""
ov_ok = False
try:
    from ultralytics import YOLO
    ovw = YOLO('yolov8s-world.pt')
    ovw.set_classes(['bus', 'person', 'door'])
    ov_res = ovw.predict(str(BUS), device=DEVICE, verbose=False)[0]
    ov_ok = True
    print(f'YOLO-World ran on {DEVICE}. {len(ov_res.boxes)} detections for the prompt list.')
except Exception as e:
    print('YOLO-World unavailable, reusing YOLO seg as a stand-in:', e)

if ov_ok:
    h_in, w_in = bgr.shape[:2]
    sx, sy = RES[0]/w_in, RES[1]/h_in
    canvas = np.zeros(RES[::-1], dtype=np.uint8)
    for x1, y1, x2, y2 in ov_res.boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = int(x1*sx), int(y1*sy), int(x2*sx), int(y2*sy)
        cv2.rectangle(canvas, (x1, y1), (x2, y2), 255, -1)
else:
    canvas = (np.any(masks.astype(bool), axis=0).astype(np.uint8) * 255)

show(scene_bgr, canvas, render(canvas),
     titles=['scene', 'open-vocab boxes' if ov_ok else 'YOLO union (fallback)',
             'phosphenes from open-vocab'],
     cols=3, figsize=(12, 4))
""",
    hint=r"""
# your code here
# Hint:
#   from ultralytics import YOLO
#   ovw = YOLO('yolov8s-world.pt')
#   ovw.set_classes(['bus', 'person', 'door'])
#   ov_res = ovw.predict(str(BUS), device=DEVICE, verbose=False)[0]
#   boxes = ov_res.boxes.xyxy.cpu().numpy()
#   Build a uint8 canvas of shape RES[::-1] and draw filled rectangles for each box
#   (remember to rescale the boxes from the original image size to RES).
#   render(canvas) and show().
""",
))


# =========================================================== §5 dynamic loop

CELLS.append(md(r"""
## 5 · Dynamic stimulus loop

So far §3 watched what one electrode does over time *with a constant
stimulus*, and §4 watched what happens with *one image*. The real world
has both at once: the camera moves, objects move, and adaptation
accumulates while the content underneath the electrodes changes.

The interactive HTML page added a "drifting image" loop after round-2
feedback to make this visible. The challenge below is the Python
equivalent.
"""))

CELLS.append(md(r"""
### Exercise 5.1 — pan a scene through the simulator `[challenge]`

Take any §4 stimulus (the YOLO union is the simplest), pan it
horizontally by 2 px per frame for 60 frames, and run the *same*
simulator across the sequence **without** resetting between frames.

1. Pick a stimulus image, e.g. `stim = union.copy()` (uint8, shape `RES[::-1]`).
2. Build a `frames` list. For each `t` in `range(60)`:
   * `shifted = np.roll(stim, shift=t*2, axis=1)`
   * `amp = sim.sample_stimulus(shifted, rescale=True)`
   * `phos = sim(amp)` — **do not** call `sim.reset()` inside the loop
   * append `phos.detach().cpu().numpy()` to `frames`
3. Display every 10th frame in a row, plus a brightness-over-time plot.

Compare to a reset-every-frame run (call `sim.reset()` inside the loop).
Which is more faithful to a real implant?
"""))

CELLS.append(ex(
    solution=r"""
def run_pan(reset_each_frame: bool):
    sim.reset()
    frames, bright = [], []
    stim = union.copy()
    for t in range(60):
        if reset_each_frame:
            sim.reset()
        shifted = np.roll(stim, shift=t*2, axis=1)
        amp = sim.sample_stimulus(shifted, rescale=True)
        phos = sim(amp)
        frames.append(phos.detach().cpu().numpy())
        bright.append(float(phos.detach().mean()))
    return frames, np.array(bright)

frames_seq, b_seq   = run_pan(reset_each_frame=False)
frames_iid, b_iid   = run_pan(reset_each_frame=True)

picks = [0, 10, 20, 30, 40, 50]
show(*[frames_seq[i] for i in picks],
     titles=[f'frame {i}, state kept' for i in picks], cols=6, figsize=(18, 3))
show(*[frames_iid[i] for i in picks],
     titles=[f'frame {i}, reset/frame' for i in picks], cols=6, figsize=(18, 3))

t = np.arange(60) / params['run']['fps']
plt.figure(figsize=(7, 3))
plt.plot(t, b_seq, label='state kept (sequential)')
plt.plot(t, b_iid, label='reset each frame (i.i.d.)', alpha=0.7)
plt.xlabel('time (s)'); plt.ylabel('mean phosphene brightness')
plt.title('Sequential state captures adaptation; i.i.d. does not')
plt.legend(); plt.tight_layout(); plt.show()
""",
    hint=r"""
# your code here
# Hint:
#   def run_pan(reset_each_frame):
#       sim.reset()
#       frames, bright = [], []
#       stim = union.copy()
#       for t in range(60):
#           if reset_each_frame: sim.reset()
#           shifted = np.roll(stim, shift=t*2, axis=1)
#           amp = sim.sample_stimulus(shifted, rescale=True)
#           phos = sim(amp)
#           frames.append(phos.detach().cpu().numpy())
#           bright.append(float(phos.detach().mean()))
#       return frames, np.array(bright)
#   Run twice (reset True / False), show every 10th frame, plot brightness vs time.
""",
))

# ============================================================ §6 vimplant2

CELLS.append(md(r"""
## 6 · Bring your own implant *(optional)*

Up to here the electrode layout was hard-coded inside this notebook.
[`vimplant2`](https://antonio-lozano.github.io/vimplant2/) is a browser
tool (no install) that lets you place implant patches on a real cortical
surface and export the resulting visual-field coverage as CSV. Drop the
file next to this notebook and feed it into the same `dynaphos`
simulator from §2.

We ship one example, `vimplant2-rfs-example.csv`, generated with the
same Schwartz log-polar wedge-dipole the HTML §02.1 preview uses. Once
the pipeline is clear, replace it with your own export.
"""))

CELLS.append(md(r"""
**Expected CSV columns** — exactly what vimplant2's *Export RFs (CSV)*
button writes:

| column | meaning |
|---|---|
| `source_app` | always `web_explorer` for vimplant2 web exports |
| `dataset` | which retinotopic atlas the RFs came from (NHP / human) |
| `prf_source` | which subject / parcellation produced the RFs |
| `implant_id` | which implant the row belongs to (multi-implant scenes) |
| `electrode_index` | per-implant index, 0-based |
| `x_deg`, `y_deg` | visual-field coordinates in degrees |
| `polar_deg`, `ecc_deg` | same point, polar form |

`load_vimplant2_csv` reads the file, sanity-checks the schema, and
returns an `(N, 2)` array of `(x_deg, y_deg)` ready to feed into
`GaussianSimulator`.
"""))

CELLS.append(code(r"""
import csv
import warnings

def load_vimplant2_csv(path: str) -> np.ndarray:
    '''Read a vimplant2 RF-export CSV and return (N, 2) (x_deg, y_deg) coords.'''
    required = {'x_deg', 'y_deg'}
    coords, seen_app = [], None
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'CSV is missing required column(s): {missing}')
        for row in reader:
            if seen_app is None:
                seen_app = (row.get('source_app') or '').strip()
            try:
                coords.append((float(row['x_deg']), float(row['y_deg'])))
            except (TypeError, ValueError):
                continue
    if seen_app and seen_app != 'web_explorer':
        warnings.warn(
            f"CSV's source_app is {seen_app!r}, expected 'web_explorer'. "
            'Proceeding anyway, but double-check the file came from vimplant2.'
        )
    if not coords:
        raise ValueError(f'No rows with finite x_deg/y_deg in {path}')
    return np.asarray(coords, dtype=np.float32)
"""))

CELLS.append(code(r"""
EXAMPLE_CSV = Path('vimplant2-rfs-example.csv')
coords_vimplant = load_vimplant2_csv(str(EXAMPLE_CSV))
ecc_vimplant = np.hypot(coords_vimplant[:, 0], coords_vimplant[:, 1])
print(f'loaded {len(coords_vimplant)} electrodes from {EXAMPLE_CSV.name}')
print(f'  mean ecc {ecc_vimplant.mean():.2f}°  ·  max ecc {ecc_vimplant.max():.2f}°')
"""))

CELLS.append(md(r"""
### Exercise 6.1 — visualise the layout `[easy]`

Scatter the loaded electrodes on a square axes spanning ±8°. Overlay
eccentricity guide rings at 2°, 5°, and 10° so a peripheral cluster is
obviously peripheral, and mark the fovea at the origin.

> Hint: `plt.scatter(coords_vimplant[:, 0], coords_vimplant[:, 1], s=14)`.
> For each `e` in `[2, 5, 10]`, add `plt.Circle((0, 0), e, fill=False)`
> via `ax.add_patch(...)`. Set `ax.set_aspect('equal')`.
"""))

CELLS.append(ex(
    solution=r"""
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(coords_vimplant[:, 0], coords_vimplant[:, 1], s=14, c='C0', alpha=0.85)
for e in [2, 5, 10]:
    ax.add_patch(plt.Circle((0, 0), e, fill=False, color='C3', alpha=0.5, lw=1))
    ax.annotate(f'{e}°', (e, 0.25), color='C3', fontsize=9)
ax.axhline(0, color='0.7', lw=0.5); ax.axvline(0, color='0.7', lw=0.5)
ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_aspect('equal')
ax.set_xlabel('x (deg)'); ax.set_ylabel('y (deg)')
ax.set_title(f'vimplant2 layout — {len(coords_vimplant)} electrodes')
plt.tight_layout(); plt.show()
""",
    hint=r"""
# your code here
# Hint:
#   fig, ax = plt.subplots(figsize=(5, 5))
#   ax.scatter(coords_vimplant[:, 0], coords_vimplant[:, 1], s=14)
#   for e in [2, 5, 10]:
#       ax.add_patch(plt.Circle((0, 0), e, fill=False, color='C3'))
#   ax.set_aspect('equal'); ax.set_xlim(-8, 8); ax.set_ylim(-8, 8)
""",
))

CELLS.append(md(r"""
### Exercise 6.2 — render through dynaphos `[intermediate]`

Feed the vimplant2 coordinates straight into a fresh `GaussianSimulator`
— same call signature as §2, just with the layout coming from the CSV
instead of the procedural foveated sampler. Render the same
`target = draw_pattern('square_disc')` through both simulators and
display them side by side.

> Hint: wrap the loaded coords as `Map(x=coords_vimplant[:, 0], y=coords_vimplant[:, 1])`
> and build `sim_v = GaussianSimulator(params, coords_map)`. Then
> `sim_v.reset(); ph = sim_v(sim_v.sample_stimulus(target, rescale=True)).detach().cpu().numpy()`.
"""))

CELLS.append(ex(
    solution=r"""
coords_map = Map(x=coords_vimplant[:, 0], y=coords_vimplant[:, 1])
sim_v = GaussianSimulator(params, coords_map)

target = draw_pattern('square_disc')
ph_procedural = render(target)
sim_v.reset()
ph_vimplant = sim_v(
    sim_v.sample_stimulus(target, rescale=True)
).detach().cpu().numpy()

show(target, ph_procedural, ph_vimplant,
     titles=['target',
             f'§2 procedural ({len(coords)} electrodes)',
             f'vimplant2 layout ({len(coords_vimplant)} electrodes)'],
     cols=3, figsize=(12, 4))
""",
    hint=r"""
# your code here
# Hint:
#   coords_map = Map(x=coords_vimplant[:, 0], y=coords_vimplant[:, 1])
#   sim_v = GaussianSimulator(params, coords_map)
#   target = draw_pattern('square_disc')
#   sim_v.reset()
#   ph_v = sim_v(sim_v.sample_stimulus(target, rescale=True)).detach().cpu().numpy()
#   show(target, render(target), ph_v, titles=[...], cols=3)
""",
))

CELLS.append(md(r"""
**Your own implant.** Open
[vimplant2](https://antonio-lozano.github.io/vimplant2/), place a patch
wherever you like, click **Export RFs (CSV)**, save the file alongside
this notebook (e.g. `vimplant2-rfs-mine.csv`), and re-run the two cells
above with `path='vimplant2-rfs-mine.csv'`. Every other cell in §6 is
agnostic to where the layout came from.
"""))


CELLS.append(md(r"""
---

**Done.** You drove the same dynaphos simulator from five different
upstream representations (intensity, edges, YOLO masks, depth,
saliency, open-vocab boxes) and watched what each one looks like under
sequential temporal dynamics. Bring whichever stimulus path you found
most legible into M5 — it becomes the input to the decoding-and-closed-
loop module.

Module lead: Lefteris & Jorge. Edit this notebook directly; commit your
additions to the bootcamp repo at the end of the day.
"""))


# ============================================================== writer

NB_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {
        "name": "python", "version": "3.10",
        "mimetype": "text/x-python", "file_extension": ".py",
    },
}


def _strip_exercise(cell: dict) -> dict:
    """Return a copy of an exercise cell with the body replaced by its hint."""
    if cell.get("metadata", {}).get("tags") == ["exercise"]:
        hint = cell["metadata"]["exercise_hint"]
        out = {
            "cell_type": "code",
            "id": cell["id"],
            "metadata": {"tags": ["exercise"]},
            "execution_count": None,
            "outputs": [],
            "source": _src(hint.strip("\n") + "\n"),
        }
        return out
    return cell


def _clean(cell: dict) -> dict:
    """Strip our exercise_hint metadata from the solution version too."""
    if "exercise_hint" in cell.get("metadata", {}):
        c = json.loads(json.dumps(cell))
        c["metadata"].pop("exercise_hint", None)
        return c
    return cell


def write_notebook(path: Path, cells: list[dict]):
    nb = {"cells": cells, "metadata": NB_METADATA, "nbformat": 4, "nbformat_minor": 5}
    path.write_text(json.dumps(nb, indent=1) + "\n", encoding="utf-8")
    print(f'wrote {path}  ({len(cells)} cells)')


def _write_example_csv(path: Path):
    """Emit a 10x10 Utah-array example CSV in the vimplant2 web-exporter format.

    Grid is placed at (cx, cy) = (10 mm, 2 mm) on V1 and projected through
    the same Schwartz log-polar wedge-dipole the HTML §02.1 preview uses
    (a = 0.75, k = 15). Header and `source_app` value mirror the live
    vimplant2 `web_explorer` CSV exporter.
    """
    import csv as _csv
    import math as _math

    WD_A, WD_K = 0.75, 15.0
    # Place the patch so its visual-field projection lands inside the §2
    # `square_disc` target's bright square (x_deg in [-4.25, 2.0], y_deg in
    # [-2.0, 4.25]) — that way §6.2 produces a non-empty phosphene render
    # with no extra alignment work from the student.
    cx_mm, cy_mm = 15.0, 4.0
    side, pitch = 10, 0.4
    half = (side - 1) / 2

    header = ['source_app', 'dataset', 'prf_source', 'implant_id',
              'electrode_index', 'x_deg', 'y_deg', 'polar_deg', 'ecc_deg']
    rows = []
    idx = 0
    for i in range(side):
        for j in range(side):
            xc = cx_mm + (i - half) * pitch
            yc = cy_mm + (j - half) * pitch
            ecc = max(0.0, WD_A * (_math.exp(xc / WD_K) - 1))
            polar = yc / WD_K  # radians
            rows.append([
                'web_explorer', 'example', 'wedge_dipole_schwartz', 'example',
                idx,
                f'{ecc * _math.cos(polar):.6f}',
                f'{ecc * _math.sin(polar):.6f}',
                f'{_math.degrees(polar):.6f}',
                f'{ecc:.6f}',
            ])
            idx += 1

    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = _csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f'wrote {path}  ({len(rows)} electrodes)')


def main():
    sol_cells  = [_clean(c) for c in CELLS]
    ex_cells   = [_strip_exercise(c) for c in CELLS]
    write_notebook(HERE / 'phosphene-simulation-solution.ipynb', sol_cells)
    write_notebook(HERE / 'phosphene-simulation.ipynb', ex_cells)
    _write_example_csv(HERE / 'vimplant2-rfs-example.csv')


if __name__ == '__main__':
    main()
