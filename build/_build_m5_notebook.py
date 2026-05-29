"""One-shot builder for modules/decoding-and-closed-loop/decoding-and-closed-loop.ipynb.

Run from anywhere; emits the notebook JSON in the canonical location.
Re-run when the notebook content changes. Idempotent.
"""
from __future__ import annotations
import json
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT  = REPO / "modules" / "decoding-and-closed-loop" / "decoding-and-closed-loop.ipynb"


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


CELLS = []

CELLS.append(md(r"""# M5 — Decoding & closed loop

**NTH bootcamp · Module 5**

The interactive companion page `decoding-and-closed-loop.html` lets you
move sliders, train a tiny MLP in your browser, and watch the whole
closed loop tick at 30 fps. This notebook does the same thing in Python
against the *real* [`dynaphos`](https://github.com/neuralcodinglab/dynaphos)
simulator, with one bigger payoff: you actually train a small CNN
through dynaphos end-to-end and export its preprocessor weights into
the HTML page's §05 comparison.

1. Setup
2. Brightness readout (mean-pixel + linear decoder)
3. PID controller — close the loop on a non-linear, adapting plant
4. Train a CNN decoder
5. End-to-end co-optimization (learnable preproc + frozen sim + decoder)
6. Minimal closed loop — everything together

Exercises are tagged **`[easy]`**, **`[intermediate]`**, or **`[challenge]`**.
"""))

CELLS.append(md(r"""## 0 · Setup

Required packages:

```bash
pip install numpy matplotlib torch dynaphos
```

The cell below installs them in-place if missing, picks the best
available compute backend (CUDA / MPS / CPU), and writes a small
`params.yaml` matching the M5 HTML page's dynaphos defaults.
"""))

CELLS.append(code(r"""%pip install -q numpy matplotlib torch dynaphos
"""))

CELLS.append(code(r"""import json, re
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

ASSETS = Path('assets')
ASSETS.mkdir(exist_ok=True)

if torch.cuda.is_available():
    DEVICE = 'cuda'
elif getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
    DEVICE = 'mps'
else:
    DEVICE = 'cpu'
print('versions: numpy', np.__version__, '· torch', torch.__version__, '· device', DEVICE)
torch.manual_seed(0); np.random.seed(0)
"""))

CELLS.append(code(r'''PARAMS_YAML = """run:
  resolution: [128, 128]
  view_angle: 16
  origin: [0, 0]
  min_angle: 0.001
  fps: 30
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

PARAMS_PATH = ASSETS / 'params.yaml'
PARAMS_PATH.write_text(PARAMS_YAML)
if DEVICE != 'cuda':
    PARAMS_PATH.write_text(re.sub(r'^(\s*gpu:).*', r'\1 -1',
                                  PARAMS_PATH.read_text(),
                                  flags=re.MULTILINE))

from dynaphos.utils import load_params
from dynaphos.cortex_models import get_visual_field_coordinates_probabilistically
from dynaphos.simulator import GaussianSimulator

params = load_params(str(PARAMS_PATH))
rng = np.random.default_rng(0)
N_ELEC = 600
coords = get_visual_field_coordinates_probabilistically(params, N_ELEC, rng=rng)
sim = GaussianSimulator(params, coords)
RES = tuple(params['run']['resolution'])
print(f'simulator: {sim.num_phosphenes} electrodes, render {RES} px')
'''))

CELLS.append(md(r"""## 1 · Brightness readout

The simplest closed-loop signal is a single number per frame:
"how bright did the phosphene field end up?" That's all PID needs as a
measurement.

The HTML page used **mean pixel intensity** as a baseline decoder.
That's hard to beat for absolute brightness — but for any task that
needs to *localise* the percept (count, recognise, navigate), it
underweights the bright centre and overweights the dim halo. We'll
train a 1-layer linear decoder to fix that and compare.
"""))

CELLS.append(code(r'''def synth_canvas(I_amp_a, electrode_idx=None):
    """Render one phosphene canvas at a random electrode for current I_amp_a.
    Returns (HxW float32 in [0,1], scalar ground-truth mean brightness)."""
    sim.reset()
    amp = torch.zeros(N_ELEC)
    e = int(np.random.randint(N_ELEC)) if electrode_idx is None else electrode_idx
    amp[e] = float(I_amp_a)
    field = sim(amp).detach().cpu().numpy()
    return field, float(field.mean())

def make_dataset(n):
    Is = np.random.uniform(10e-6, 250e-6, n).astype(np.float32)
    fields = np.zeros((n, RES[0]*RES[1]), dtype=np.float32)
    ys = np.zeros(n, dtype=np.float32)
    for i, I in enumerate(Is):
        f, y = synth_canvas(I)
        fields[i] = f.ravel()
        ys[i] = y
    return fields, ys

X, y = make_dataset(200)

# Linear decoder via ridge-regularised normal equations.
Xd = X.astype(np.float64); yd = y.astype(np.float64)
A = Xd.T @ Xd + 1e-3 * np.eye(Xd.shape[1])
w_lin = np.linalg.solve(A, Xd.T @ yd).astype(np.float32)

mean_pred = X.mean(axis=1)
lin_pred  = X @ w_lin
err_mean = np.abs(y - mean_pred).mean()
err_lin  = np.abs(y - lin_pred).mean()
print(f'mean-pixel decoder MAE: {err_mean:.4f}')
print(f'linear decoder    MAE: {err_lin:.4f}')

fig, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].plot(y, mean_pred, '.', label=f'mean-pixel (MAE {err_mean:.3f})', alpha=0.5)
axes[0].plot(y, lin_pred,  '.', label=f'linear (MAE {err_lin:.3f})', alpha=0.5)
axes[0].plot([0, y.max()], [0, y.max()], 'k--', lw=0.7)
axes[0].set_xlabel('ground truth'); axes[0].set_ylabel('predicted')
axes[0].set_title('Decoder predictions'); axes[0].legend(fontsize=8)
axes[1].imshow(w_lin.reshape(RES), cmap='RdBu_r',
               vmin=-abs(w_lin).max(), vmax=abs(w_lin).max())
axes[1].set_title('Linear weights w (spatial)'); axes[1].axis('off')
plt.tight_layout(); plt.show()
'''))

CELLS.append(md(r"""### Exercise 1.1 — Where does the linear decoder put its weights? `[easy]`

Look at the weight map. Compute the *centre-weighted* fraction: the sum
of `|w|` in the central 32×32 crop divided by the sum over the whole
map. Compare to what you'd expect from mean-pixel (every pixel weighted
equally).
"""))

CELLS.append(code(r"""# your code here
# Hint:
#   wmap = w_lin.reshape(RES)
#   ctr = wmap[RES[0]//2-16:RES[0]//2+16, RES[1]//2-16:RES[1]//2+16]
#   frac = np.abs(ctr).sum() / np.abs(wmap).sum()
#   uniform_baseline = (32*32) / (RES[0]*RES[1])
#   print(frac, 'vs uniform baseline', uniform_baseline)
"""))

CELLS.append(md(r"""## 2 · PID controller

Now the loop. Drive the simulator at 30 fps for 4 seconds with a fixed
electrode subset, but adjust the per-frame current with a PID controller
that reads mean brightness and tries to track a sinusoidal target.

What makes this interesting: dynaphos has *state* (an adaptation trace
that builds while the electrode is being stimulated and leaks slowly),
and the brightness-from-activation map is *non-linear*. Even the
simplest P-only controller has a non-trivial plant to deal with.
"""))

CELLS.append(code(r'''class PID:
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp; self.Ki = Ki; self.Kd = Kd; self.dt = dt
        self.integral = 0.0; self.prev_err = 0.0
    def __call__(self, err):
        self.integral = float(np.clip(self.integral + err*self.dt, -2.0, 2.0))
        derivative = (err - self.prev_err) / self.dt
        self.prev_err = err
        return self.Kp*err + self.Ki*self.integral + self.Kd*derivative

def run_pid(Kp, Ki, Kd, frames=120, target_fn=None, electrode_subset=None):
    """Run a PID-controlled stimulation sequence. Gains are in microamperes
    per unit error so the numbers stay friendly."""
    fps = params['run']['fps']
    dt = 1.0 / fps
    if target_fn is None:
        target_fn = lambda t: 0.5 + 0.3*np.sin(2*np.pi*t/2.0)
    if electrode_subset is None:
        electrode_subset = list(range(0, N_ELEC, 6))

    pid = PID(Kp*1e-6, Ki*1e-6, Kd*1e-6, dt)
    sim.reset()
    targets, achieved, currents = [], [], []
    phos = sim(torch.zeros(N_ELEC)).detach().cpu().numpy()
    for f in range(frames):
        t = f * dt
        m = float(phos.mean())
        tgt = float(target_fn(t))
        err = tgt - m
        I = float(np.clip(pid(err), 0.0, 280e-6))
        amp = torch.zeros(N_ELEC)
        for e in electrode_subset:
            amp[e] = I
        phos = sim(amp).detach().cpu().numpy()
        targets.append(tgt); achieved.append(float(phos.mean())); currents.append(I)
    return np.array(targets), np.array(achieved), np.array(currents)

tgt, ach, cur = run_pid(Kp=400, Ki=200, Kd=40, frames=120)

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(7, 4.5))
t = np.arange(len(tgt)) / params['run']['fps']
axes[0].plot(t, tgt, '--', label='target', color='C3')
axes[0].plot(t, ach, label='achieved', color='black')
axes[0].set_ylabel('brightness'); axes[0].legend(fontsize=8)
axes[0].set_title('PID tracking with dynaphos adaptation')
axes[1].plot(t, cur*1e6, color='C0')
axes[1].set_xlabel('time (s)'); axes[1].set_ylabel('stim (µA)')
plt.tight_layout(); plt.show()
print(f'mean |err|: {np.abs(tgt-ach).mean():.4f}')
'''))

CELLS.append(md(r"""### Exercise 2.1 — Find a useful PID tuning `[intermediate]`

Tune `Kp`, `Ki`, `Kd` to minimise mean absolute error against a constant
`0.8` step target sustained for the whole window. There's no single
right answer; tinker. Start at `(200, 0, 0)`, then add `I` and `D`
incrementally and watch what each one fixes.
"""))

CELLS.append(code(r"""# your code here
# Hint:
#   gains = [(200, 0, 0), (200, 200, 0), (200, 100, 40), (400, 150, 30)]
#   results = []
#   for Kp, Ki, Kd in gains:
#       tgt, ach, _ = run_pid(Kp, Ki, Kd, target_fn=lambda t: 0.8)
#       results.append((Kp, Ki, Kd, np.abs(tgt - ach).mean(), ach))
#   for Kp, Ki, Kd, mae, _ in results:
#       print(f'Kp={Kp:3d} Ki={Ki:3d} Kd={Kd:3d}  MAE={mae:.4f}')
"""))

CELLS.append(md(r"""## 3 · Train a CNN decoder

The §1 linear decoder works, but it can't represent "the bright spot is
*here*" — only "the bright spot is *somewhere*". A small convnet can.

We'll train a 3-layer CNN on synthetic phosphene canvases to predict
mean brightness. Same setup as the HTML §04 MLP, but the network gets a
spatial receptive field. On CPU this should finish in well under a
minute.
"""))

CELLS.append(code(r"""class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 8, 5, stride=2, padding=2)
        self.c2 = nn.Conv2d(8, 16, 5, stride=2, padding=2)
        self.c3 = nn.Conv2d(16, 32, 5, stride=2, padding=2)
        self.fc = nn.Linear(32, 1)
    def forward(self, x):
        x = F.relu(self.c1(x)); x = F.relu(self.c2(x)); x = F.relu(self.c3(x))
        x = F.adaptive_avg_pool2d(x, 1).flatten(1)
        return torch.sigmoid(self.fc(x))

def make_batch(B):
    fields = np.zeros((B, 1, *RES), dtype=np.float32)
    ys = np.zeros((B, 1), dtype=np.float32)
    Is = np.random.uniform(10e-6, 250e-6, B)
    for i in range(B):
        f, y = synth_canvas(Is[i])
        fields[i, 0] = f
        ys[i, 0] = y
    return torch.from_numpy(fields).to(DEVICE), torch.from_numpy(ys).to(DEVICE)

net = TinyCNN().to(DEVICE)
opt = torch.optim.Adam(net.parameters(), lr=3e-3)
losses = []
EPOCHS = 80
for step in range(EPOCHS):
    x, y_ = make_batch(32)
    pred = net(x)
    loss = F.mse_loss(pred, y_)
    opt.zero_grad(); loss.backward(); opt.step()
    losses.append(float(loss))

plt.plot(losses); plt.xlabel('step'); plt.ylabel('MSE')
plt.title('CNN brightness decoder training'); plt.show()
print(f'final loss: {losses[-1]:.5f}')
"""))

CELLS.append(md(r"""### Exercise 3.1 — CNN vs linear, head to head `[easy]`

Use the trained CNN and the §1 `w_lin` on a fresh batch of canvases.
Compare MAE side-by-side. The CNN should win on brightness too — but
the bigger win shows up on tasks the linear decoder *can't* do (e.g.,
predicting the centroid of the phosphene). If you have time, add
"predict centroid x" as a second output head.
"""))

CELLS.append(code(r"""# your code here
# Hint:
#   net.eval()
#   maes_cnn, maes_lin = [], []
#   with torch.no_grad():
#       for _ in range(16):
#           x, yb = make_batch(32)
#           p = net(x).cpu().numpy().squeeze()
#           lin_p = x.cpu().numpy().reshape(32, -1) @ w_lin
#           yb = yb.cpu().numpy().squeeze()
#           maes_cnn.append(np.abs(p - yb).mean())
#           maes_lin.append(np.abs(lin_p - yb).mean())
#   print('CNN MAE:', np.mean(maes_cnn), 'Linear MAE:', np.mean(maes_lin))
"""))

CELLS.append(md(r"""## 4 · End-to-end co-optimization

The headline. Because dynaphos is differentiable, you can train a
learnable preprocessor + learnable decoder *jointly*, with gradients
flowing through the frozen simulator. The preprocessor learns to encode
for the decoder, not for human perception.

We train two small 2-layer convnets sandwiching a single dynaphos
forward pass. Loss = L2 between the *recovered image* and the original
input — the decoder reconstructs the input from phosphenes. The final
cell exports the preprocessor weights to
`modules/assets/m5_e2e_weights.json` for the HTML §05 comparison.
"""))

CELLS.append(code(r'''class Preproc(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 8, 5, padding=2)
        self.c2 = nn.Conv2d(8, 1, 5, padding=2)
    def forward(self, x):
        return torch.sigmoid(self.c2(F.relu(self.c1(x))))

class Recon(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 8, 5, padding=2)
        self.c2 = nn.Conv2d(8, 1, 5, padding=2)
    def forward(self, x):
        return torch.sigmoid(self.c2(F.relu(self.c1(x))))

def random_scene(B):
    """Synthesise B simple natural-looking inputs: 3–5 overlapping bright blobs."""
    H, W = RES
    x = np.zeros((B, 1, H, W), dtype=np.float32)
    for b in range(B):
        for _ in range(np.random.randint(3, 6)):
            cy, cx = np.random.randint(20, H-20), np.random.randint(20, W-20)
            r = np.random.uniform(4, 12)
            amp = np.random.uniform(0.4, 1.0)
            ys, xs = np.ogrid[:H, :W]
            x[b, 0] = np.minimum(1.0, x[b, 0] + amp*np.exp(-((ys-cy)**2 + (xs-cx)**2)/(2*r*r)))
    return torch.from_numpy(x).to(DEVICE)

def sample_at_electrodes(image):
    """B,1,H,W image -> B,N_ELEC sampled amplitudes via bilinear grid_sample.
    Maps view-angle coordinates to normalised [-1, 1] for grid_sample."""
    B, _, H, W = image.shape
    cx = sim.coordinates_visual_field.x
    cy = sim.coordinates_visual_field.y
    xs = torch.as_tensor(np.asarray(cx.detach().cpu() if hasattr(cx, 'detach') else cx),
                         dtype=torch.float32, device=DEVICE)
    ys = torch.as_tensor(np.asarray(cy.detach().cpu() if hasattr(cy, 'detach') else cy),
                         dtype=torch.float32, device=DEVICE)
    va = params['run']['view_angle']
    grid = torch.stack([xs / (va/2), ys / (va/2)], dim=-1).view(1, 1, -1, 2)
    grid = grid.expand(B, 1, -1, 2)
    sampled = F.grid_sample(image, grid, mode='bilinear',
                            padding_mode='zeros', align_corners=False)
    return 10e-6 + sampled.squeeze(1).squeeze(1) * 240e-6

preproc = Preproc().to(DEVICE)
recon   = Recon().to(DEVICE)
opt_e2e = torch.optim.Adam(list(preproc.parameters()) + list(recon.parameters()), lr=3e-3)

losses_e2e = []
STEPS = 200
for step in range(STEPS):
    scenes = random_scene(8)
    pre = preproc(scenes)
    amps = sample_at_electrodes(pre)
    sim.reset()
    # one dynaphos call per batch item — sim is single-batch
    fields = torch.stack([sim(amps[i]) for i in range(amps.shape[0])], dim=0).unsqueeze(1)
    recovered = recon(fields)
    loss = F.mse_loss(recovered, scenes)
    opt_e2e.zero_grad(); loss.backward(); opt_e2e.step()
    losses_e2e.append(float(loss))
    if step % 20 == 0:
        print(f'step {step:3d} loss {loss.item():.4f}')

plt.plot(losses_e2e); plt.xlabel('step'); plt.ylabel('MSE')
plt.title('End-to-end preproc + decoder'); plt.show()
print(f'final loss: {losses_e2e[-1]:.5f}')
'''))

CELLS.append(md(r"""### Exercise 4.1 — Export weights to the HTML page `[challenge]`

The HTML page §05 currently uses a hand-picked "trained-looking"
preprocessor stand-in. Export the *real* trained preprocessor weights
into a small JSON the HTML page can load.

1. Extract `preproc.c1.weight` (shape `(8,1,5,5)`) + bias, and
   `preproc.c2.weight` (shape `(1,8,5,5)`) + bias.
2. Save as `modules/assets/m5_e2e_weights.json` with a round-trippable
   schema.
3. Wire the HTML `e2ePreproc()` function to load the JSON on demand
   instead of using the gamma-boost stand-in. (HTML wiring is left to
   you; the export is the easy bit.)
"""))

CELLS.append(code(r"""# your code here
# Hint:
#   import json
#   payload = {
#       'c1': {'w': preproc.c1.weight.detach().cpu().numpy().tolist(),
#              'b': preproc.c1.bias.detach().cpu().numpy().tolist()},
#       'c2': {'w': preproc.c2.weight.detach().cpu().numpy().tolist(),
#              'b': preproc.c2.bias.detach().cpu().numpy().tolist()},
#   }
#   out = Path('../assets/m5_e2e_weights.json')
#   out.write_text(json.dumps(payload))
#   print('wrote', out, '(', out.stat().st_size // 1024, 'KB )')
"""))

CELLS.append(md(r"""## 5 · Minimal closed-loop demo

Everything together. Pan a small scene horizontally, preprocess it with
the trained `preproc`, stim through dynaphos (with adaptation), decode
with the trained `recon`, and use a PID to nudge the *global stim scale*
so the mean recovered brightness tracks a target.

Run twice: open loop (the PID's output is ignored), then closed loop.
The closed-loop trace should hold the target through the adaptation
roll-off; open loop drifts.
"""))

CELLS.append(code(r"""def run_closed_loop(closed=True, frames=120, target=0.55):
    pid = PID(400e-6, 100e-6, 30e-6, 1.0/params['run']['fps'])
    sim.reset()
    targets, achieved, currents = [], [], []
    H, W = RES
    ys, xs = np.ogrid[:H, :W]
    for f in range(frames):
        cx = int((f * 3) % W)
        scene = np.exp(-((xs-cx)**2)/(2*8*8)).astype(np.float32)
        x = torch.from_numpy(scene)[None, None].to(DEVICE)
        with torch.no_grad():
            pre = preproc(x)
        amps = sample_at_electrodes(pre).squeeze(0)
        if closed and f > 0:
            err = target - achieved[-1]
            factor = 1.0 + float(np.clip(pid(err) / 100e-6, -0.9, 4.0))
            amps = amps * max(0.05, factor)
        amps = torch.clamp(amps, 0, 280e-6)
        phos = sim(amps).detach().cpu().numpy()
        achieved.append(float(phos.mean()))
        targets.append(target)
        currents.append(float(amps.mean()))
    return np.array(targets), np.array(achieved), np.array(currents)

tgt_o, ach_o, _ = run_closed_loop(closed=False)
tgt_c, ach_c, _ = run_closed_loop(closed=True)

fig, ax = plt.subplots(figsize=(7, 3.2))
t = np.arange(len(tgt_o)) / params['run']['fps']
ax.plot(t, tgt_o, '--', color='C3', label='target')
ax.plot(t, ach_o, color='gray',   label='open loop')
ax.plot(t, ach_c, color='black',  label='closed loop')
ax.set_xlabel('time (s)'); ax.set_ylabel('decoded brightness')
ax.set_title('Open vs closed loop · drifting input + adaptation')
ax.legend(fontsize=8); plt.tight_layout(); plt.show()
print(f'open   MAE: {np.abs(tgt_o-ach_o).mean():.4f}')
print(f'closed MAE: {np.abs(tgt_c-ach_c).mean():.4f}')
"""))

CELLS.append(md(r"""---

**Done.** You decoded brightness with a linear model, closed the loop
with PID, trained a CNN decoder, co-optimised a preprocessor + decoder
end-to-end through the dynaphos simulator, and ran a minimal closed
loop with adaptation. The workshop tracks pick up here:

* **Experimental.** Pick a target image; compare phosphene renders from
  hand-tuned vs end-to-end preprocessors; collect subjective ratings.
* **Developer.** Port §2 PID to per-channel control on the M3 Utah
  array; investigate where channel coupling breaks it.
* **Open neurotech.** Re-cast the same closed-loop pattern on a
  different prosthesis (BCI cursor, DBS, neurofeedback). The loop is
  the unit of design.

Module lead: Antonio. Edit this notebook directly.
"""))


NB = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(NB, indent=1), encoding="utf-8")
size_kb = OUT.stat().st_size / 1024
print(f"wrote {OUT}  ({size_kb:.1f} KB, {len(CELLS)} cells)")
