"""One-shot builder for modules/M5-decoding-and-closed-loop/decoding-and-closed-loop.ipynb.

Run from anywhere; emits the notebook JSON in the canonical location.
Re-run when the notebook content changes. Idempotent.
"""
from __future__ import annotations
import json
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT  = REPO / "modules" / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop.ipynb"


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

The interactive companion page `M5-decoding-and-closed-loop.html` lets you
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

The §1 linear decoder works for absolute brightness, but it can't tell
you *where* the bright spot is. A small convnet can. We give the CNN
two heads at once: predict mean brightness *and* the centroid (cx, cy)
in normalised image coordinates. The two heads share the trunk; the
brightness head squashes through a sigmoid, the centroid head stays
linear.

We also split off a fixed held-out batch of 50 canvases before training
so the test curve lives next to the training curve, and we visualise
the eight learned first-layer filters at the end.
"""))

CELLS.append(code(r'''class TinyCNN(nn.Module):
    """Joint brightness + centroid decoder. Three conv layers, average-
    pool to a 32-d feature, two heads on top."""
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 8, 5, stride=2, padding=2)
        self.c2 = nn.Conv2d(8, 16, 5, stride=2, padding=2)
        self.c3 = nn.Conv2d(16, 32, 5, stride=2, padding=2)
        self.fc_b = nn.Linear(32, 1)
        self.fc_c = nn.Linear(32, 2)
    def forward(self, x):
        x = F.relu(self.c1(x)); x = F.relu(self.c2(x)); x = F.relu(self.c3(x))
        x = F.adaptive_avg_pool2d(x, 1).flatten(1)
        return torch.sigmoid(self.fc_b(x)), self.fc_c(x)

def synth_canvas2(I_amp_a, electrode_idx=None):
    """Like synth_canvas but also returns ground-truth electrode location
    in normalised (-1, 1) image coordinates."""
    sim.reset()
    amp = torch.zeros(N_ELEC)
    e = int(np.random.randint(N_ELEC)) if electrode_idx is None else electrode_idx
    amp[e] = float(I_amp_a)
    field = sim(amp).detach().cpu().numpy()
    va = params['run']['view_angle']
    coords_x = np.asarray(getattr(coords, 'x', getattr(coords, '_x')))
    coords_y = np.asarray(getattr(coords, 'y', getattr(coords, '_y')))
    cx = float(coords_x[e]) / (va / 2)
    cy = float(coords_y[e]) / (va / 2)
    return field, float(field.mean()), (cx, cy)

def make_batch_centroid(B):
    fields = np.zeros((B, 1, *RES), dtype=np.float32)
    ys_b = np.zeros((B, 1), dtype=np.float32)
    ys_c = np.zeros((B, 2), dtype=np.float32)
    Is = np.random.uniform(10e-6, 250e-6, B)
    for i in range(B):
        f, y, c = synth_canvas2(Is[i])
        fields[i, 0] = f
        ys_b[i, 0] = y
        ys_c[i] = c
    return (torch.from_numpy(fields).to(DEVICE),
            torch.from_numpy(ys_b).to(DEVICE),
            torch.from_numpy(ys_c).to(DEVICE))

# Held-out test batch — generated once with a fixed seed before training.
torch.manual_seed(123); np.random.seed(123)
xt, yt_b, yt_c = make_batch_centroid(50)
torch.manual_seed(0); np.random.seed(0)

net = TinyCNN().to(DEVICE)
opt = torch.optim.Adam(net.parameters(), lr=3e-3)
train_losses, test_marks = [], []
EPOCHS = 100
for step in range(EPOCHS):
    x, y_b, y_c = make_batch_centroid(32)
    pred_b, pred_c = net(x)
    loss = F.mse_loss(pred_b, y_b) + 0.5 * F.mse_loss(pred_c, y_c)
    opt.zero_grad(); loss.backward(); opt.step()
    train_losses.append(float(loss))
    if step % 5 == 0 or step == EPOCHS - 1:
        with torch.no_grad():
            pt_b, pt_c = net(xt)
            tl = float(F.mse_loss(pt_b, yt_b) + 0.5 * F.mse_loss(pt_c, yt_c))
        test_marks.append((step, tl))

net.eval()
with torch.no_grad():
    pt_b, pt_c = net(xt)
brightness_mae = float(F.l1_loss(pt_b, yt_b))
centroid_norm_mae = float(F.l1_loss(pt_c, yt_c))
centroid_pix_mae = centroid_norm_mae * RES[1] / 2

fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
axes[0].plot(train_losses, color='C0', alpha=0.8, label='train')
tx = [s for s, _ in test_marks]; ty = [v for _, v in test_marks]
axes[0].plot(tx, ty, 'o-', color='C3', mfc='white', label='test (held-out 50)')
axes[0].set_xlabel('step'); axes[0].set_ylabel('joint MSE')
axes[0].set_title(f'CNN training · final test brightness MAE {brightness_mae:.3f}')
axes[0].grid(alpha=0.3); axes[0].legend(fontsize=8)

pred_c_np = pt_c.cpu().numpy(); true_c_np = yt_c.cpu().numpy()
axes[1].scatter(true_c_np[:, 0], pred_c_np[:, 0], color='C0', label='cx', alpha=0.7)
axes[1].scatter(true_c_np[:, 1], pred_c_np[:, 1], color='C3', label='cy', alpha=0.7)
axes[1].plot([-1, 1], [-1, 1], 'k--', lw=0.7)
axes[1].set_xlim(-1, 1); axes[1].set_ylim(-1, 1)
axes[1].set_xlabel('ground truth (normalised)'); axes[1].set_ylabel('predicted')
axes[1].set_title(f'Centroid head · test MAE {centroid_pix_mae:.1f} px (image {RES[0]}×{RES[1]})')
axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)
plt.tight_layout(); plt.show()

filt = net.c1.weight.detach().cpu().numpy()[:, 0]
fmax = abs(filt).max() if abs(filt).max() > 0 else 1.0
fig, axes = plt.subplots(2, 4, figsize=(9, 4.5))
for k in range(8):
    ax = axes[k // 4, k % 4]
    ax.imshow(filt[k], cmap='RdBu_r', vmin=-fmax, vmax=fmax)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f'c1 filter {k}', fontsize=9)
fig.suptitle('learned first-layer 5×5 filters', fontsize=10)
plt.tight_layout(); plt.show()

print(f'final train loss : {train_losses[-1]:.5f}')
print(f'held-out test brightness MAE : {brightness_mae:.4f}')
print(f'held-out test centroid MAE   : {centroid_pix_mae:.2f} px')
'''))

CELLS.append(md(r"""### Exercise 3.1 — Read the filter grid `[easy]`

Look at the eight first-layer filters above. Some will look like local
edge detectors (positive/negative halves split along an axis); some will
look like centre-surround spots. Without re-running the cell, list which
filters you'd expect to fire for: a bright dot in the centre, a vertical
edge on the left, a horizontal edge at the top. There's no single right
answer — the network's filter labels are random.
"""))

CELLS.append(code(r"""# your notes here
# Tip: you can re-plot a single filter with:
#   plt.imshow(net.c1.weight.detach().cpu().numpy()[k, 0],
#              cmap='RdBu_r'); plt.colorbar(); plt.show()
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
    cx = np.asarray(getattr(coords, 'x', getattr(coords, '_x')))
    cy = np.asarray(getattr(coords, 'y', getattr(coords, '_y')))
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

# Capture (scene, preprocessed, phosphene field, reconstruction) at the
# chosen snapshot steps so learning shows up as four image rows below
# the loss curve.
SNAP_STEPS = [0, 50, 100, 199]
snapshots = []
losses_e2e = []
STEPS = 200
for step in range(STEPS):
    scenes = random_scene(8)
    pre = preproc(scenes)
    amps = sample_at_electrodes(pre)
    sim.reset()
    fields = torch.stack([sim(amps[i]) for i in range(amps.shape[0])], dim=0).unsqueeze(1)
    recovered = recon(fields)
    loss = F.mse_loss(recovered, scenes)
    opt_e2e.zero_grad(); loss.backward(); opt_e2e.step()
    losses_e2e.append(float(loss))
    if step in SNAP_STEPS:
        snapshots.append({
            'step':      step,
            'scene':     scenes[0].detach().cpu().numpy().squeeze(),
            'pre':       pre[0].detach().cpu().numpy().squeeze(),
            'field':     fields[0].detach().cpu().numpy().squeeze(),
            'recovered': recovered[0].detach().cpu().numpy().squeeze(),
        })
    if step % 20 == 0:
        print(f'step {step:3d} loss {loss.item():.4f}')

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(losses_e2e, color='C0'); ax.set_xlabel('step'); ax.set_ylabel('MSE')
ax.set_title('End-to-end preproc + decoder'); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
print(f'final loss: {losses_e2e[-1]:.5f}')

# Progression grid: 4 rows × 4 cols (scene | preproc | phosphenes | recon)
# per snapshot step. The reconstruction column should visibly sharpen.
fig, axes = plt.subplots(len(snapshots), 4, figsize=(10, 2.5*len(snapshots)))
col_titles = ['input scene', 'preprocessed', 'phosphenes', 'reconstruction']
for i, snap in enumerate(snapshots):
    rowdata = [snap['scene'], snap['pre'], snap['field'], snap['recovered']]
    for j, im in enumerate(rowdata):
        ax = axes[i, j]
        ax.imshow(im, cmap='gray', vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        if i == 0: ax.set_title(col_titles[j], fontsize=10)
    axes[i, 0].set_ylabel(f'step {snap["step"]}', fontsize=10)
plt.tight_layout(); plt.show()

# Out-of-distribution validation: training saw random overlapping blobs.
# Feed a structured grid pattern instead and see what survives.
H, W = RES
grid_pattern = np.zeros((H, W), dtype=np.float32)
for r in range(20, H-20, 24):
    grid_pattern[r-1:r+1, 20:W-20] = 1.0
for c in range(20, W-20, 24):
    grid_pattern[20:H-20, c-1:c+1] = 1.0
val_scene = torch.from_numpy(grid_pattern)[None, None].to(DEVICE)
with torch.no_grad():
    val_pre = preproc(val_scene)
    val_amps = sample_at_electrodes(val_pre)
    sim.reset()
    val_field = sim(val_amps[0]).unsqueeze(0).unsqueeze(0)
    val_rec = recon(val_field)
val_mse = float(F.mse_loss(val_rec, val_scene))

fig, ax = plt.subplots(1, 4, figsize=(11, 2.8))
panels = [val_scene.cpu().numpy().squeeze(),
          val_pre.cpu().numpy().squeeze(),
          val_field.cpu().numpy().squeeze(),
          val_rec.cpu().numpy().squeeze()]
titles = ['OOD input (grid)', 'preprocessed', 'phosphenes', 'reconstruction']
for a, im, t in zip(ax, panels, titles):
    a.imshow(im, cmap='gray', vmin=0, vmax=1); a.set_title(t, fontsize=10)
    a.set_xticks([]); a.set_yticks([])
fig.suptitle(f'Out-of-distribution validation · MSE {val_mse:.4f}', fontsize=10)
plt.tight_layout(); plt.show()
print(f'OOD grid-pattern MSE: {val_mse:.5f}')
'''))

CELLS.append(md(r"""### 4.1 · Export weights to the HTML page

The HTML page §05 ships a hand-picked stand-in by default. With the
trained `preproc` in hand we can write a small JSON the page picks up
on next load and shows side-by-side with Sobel under the blend slider.
The two `Conv2d` layers come out at shapes `(8, 1, 5, 5)` + bias `(8,)`
for `c1` and `(1, 8, 5, 5)` + bias `(1,)` for `c2` — under 5 KB total.
"""))

CELLS.append(code(r'''import json

# Resolve modules/assets/ whether the notebook runs from its own folder
# (modules/M5-decoding-and-closed-loop/) or from the repo root.
HERE = Path.cwd()
candidates = [
    HERE / 'modules' / 'assets',                       # from repo root
    HERE.parent / 'assets',                            # from module folder
    HERE / 'assets',                                   # fallback
]
ASSETS_DIR = next((c for c in candidates if c.exists()), candidates[0])
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
OUT_WEIGHTS = (ASSETS_DIR / 'm5_e2e_weights.json').resolve()

payload = {
    'arch': 'preproc-2conv-5x5-relu-sigmoid',
    'c1': {
        'w': preproc.c1.weight.detach().cpu().numpy().tolist(),
        'b': preproc.c1.bias.detach().cpu().numpy().tolist(),
    },
    'c2': {
        'w': preproc.c2.weight.detach().cpu().numpy().tolist(),
        'b': preproc.c2.bias.detach().cpu().numpy().tolist(),
    },
}
OUT_WEIGHTS.write_text(json.dumps(payload))
print(f'wrote {OUT_WEIGHTS} ({OUT_WEIGHTS.stat().st_size / 1024:.1f} KB)')
'''))

CELLS.append(md(r"""### 4.2 · Verify the export round-trips

The HTML page does the conv forward in JavaScript. We mirror it here in
numpy to confirm the JSON we just wrote produces the same output the
torch model does — a few digits of agreement is enough proof.
"""))

CELLS.append(code(r'''import json
reloaded = json.loads(OUT_WEIGHTS.read_text())

c1_w = np.asarray(reloaded['c1']['w'], dtype=np.float32)
c1_b = np.asarray(reloaded['c1']['b'], dtype=np.float32)
c2_w = np.asarray(reloaded['c2']['w'], dtype=np.float32)
c2_b = np.asarray(reloaded['c2']['b'], dtype=np.float32)
F_HID = c1_w.shape[0]  # number of hidden filters

def numpy_preproc(scene_2d):
    """Two-conv preproc forward in numpy, mirroring the JS side."""
    Hh, Ww = scene_2d.shape
    pad = 2
    xpad = np.pad(scene_2d, ((pad, pad), (pad, pad)), mode='constant')
    h1 = np.zeros((F_HID, Hh, Ww), dtype=np.float32)
    for f in range(F_HID):
        for di in range(5):
            for dj in range(5):
                h1[f] += c1_w[f, 0, di, dj] * xpad[di:di+Hh, dj:dj+Ww]
        h1[f] += c1_b[f]
    h1 = np.maximum(0.0, h1)  # ReLU
    h1pad = np.pad(h1, ((0, 0), (pad, pad), (pad, pad)), mode='constant')
    out = np.zeros((Hh, Ww), dtype=np.float32) + c2_b[0]
    for f in range(F_HID):
        for di in range(5):
            for dj in range(5):
                out += c2_w[0, f, di, dj] * h1pad[f, di:di+Hh, dj:dj+Ww]
    return 1.0 / (1.0 + np.exp(-out))  # sigmoid

torch.manual_seed(7); np.random.seed(7)
test_scene = random_scene(1)
np_in = test_scene.cpu().numpy().squeeze()
with torch.no_grad():
    torch_out = preproc(test_scene).cpu().numpy().squeeze()
np_out = numpy_preproc(np_in)
print(f'max abs diff (torch vs numpy reload): {float(np.abs(torch_out - np_out).max()):.3e}')

fig, ax = plt.subplots(1, 3, figsize=(9, 3))
ax[0].imshow(np_in,    cmap='gray', vmin=0, vmax=1); ax[0].set_title('input')
ax[1].imshow(torch_out, cmap='gray', vmin=0, vmax=1); ax[1].set_title('torch preproc')
ax[2].imshow(np_out,    cmap='gray', vmin=0, vmax=1); ax[2].set_title('numpy round-trip')
for a in ax: a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.show()
'''))

CELLS.append(md(r"""## 5 · Minimal closed-loop demo

Pan a rendered **OPEN** caption across the visual field, preprocess it
with the trained `preproc`, stim through dynaphos (with adaptation),
decode with the trained `recon`, and let a PID nudge the *global stim
scale* to hold the mean recovered brightness near a target.

Run twice: open loop (the PID's output is ignored), then closed loop.
Two payoffs to look for: the trace stays in band under feedback, and
the per-frame reconstruction holds its contrast through the run
instead of fading as adaptation builds.
"""))

CELLS.append(code(r'''try:
    from PIL import Image, ImageDraw, ImageFont
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

def _get_font(size=42):
    for candidate in [
        'arial.ttf',
        'DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/Library/Fonts/Arial.ttf',
        'C:/Windows/Fonts/arial.ttf',
    ]:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    return ImageFont.load_default()

H_RES, W_RES = RES

def render_text_panning(frame, total_frames):
    """1-channel float32 image of 'OPEN' panning across the visual field.
    Falls back to a drifting cross if PIL is unavailable."""
    if _HAS_PIL:
        canvas = Image.new('L', (W_RES * 2, H_RES), 0)
        draw = ImageDraw.Draw(canvas)
        font = _get_font(42)
        draw.text((W_RES * 0.2, H_RES // 2 - 24), 'OPEN', fill=255, font=font)
        shift = int((frame / max(1, total_frames - 1)) * (W_RES - 30))
        crop = canvas.crop((shift, 0, shift + W_RES, H_RES))
        return np.asarray(crop, dtype=np.float32) / 255.0
    arr = np.zeros((H_RES, W_RES), dtype=np.float32)
    cy = H_RES // 2
    cx = int(W_RES * 0.3 + (W_RES * 0.4) * frame / max(1, total_frames - 1))
    arr[max(0, cy-3):cy+3, max(0, cx-30):cx+30] = 1.0
    arr[max(0, cy-30):cy+30, max(0, cx-3):cx+3] = 1.0
    return arr

def contrast(field):
    fmax = float(field.max())
    if fmax <= 0: return 0.0
    return (fmax - float(field.mean())) / fmax

def run_closed_loop2(closed=True, frames=120, target=0.55):
    pid = PID(400e-6, 100e-6, 30e-6, 1.0 / params['run']['fps'])
    sim.reset()
    scenes_log, fields_log, recs_log = [], [], []
    targets, achieved, currents = [], [], []
    for f in range(frames):
        scene = render_text_panning(f, frames)
        x = torch.from_numpy(scene)[None, None].to(DEVICE)
        with torch.no_grad():
            pre = preproc(x)
        amps = sample_at_electrodes(pre).squeeze(0)
        if closed and f > 0:
            err = target - achieved[-1]
            factor = 1.0 + float(np.clip(pid(err) / 100e-6, -0.9, 4.0))
            amps = amps * max(0.05, factor)
        amps = torch.clamp(amps, 0, 280e-6)
        phos = sim(amps).detach()
        phos_np = phos.cpu().numpy()
        with torch.no_grad():
            rec = recon(phos.unsqueeze(0).unsqueeze(0)).cpu().numpy().squeeze()
        scenes_log.append(scene)
        fields_log.append(phos_np)
        recs_log.append(rec)
        achieved.append(float(phos_np.mean()))
        targets.append(target)
        currents.append(float(amps.mean()))
    return (np.array(targets), np.array(achieved), np.array(currents),
            scenes_log, fields_log, recs_log)

print('running open loop...')
tgt_o, ach_o, _, scenes_o, fields_o, recs_o = run_closed_loop2(closed=False)
print('running closed loop...')
tgt_c, ach_c, _, scenes_c, fields_c, recs_c = run_closed_loop2(closed=True)

fig, ax = plt.subplots(figsize=(7, 3.2))
t = np.arange(len(tgt_o)) / params['run']['fps']
ax.plot(t, tgt_o, '--', color='C3', label='target')
ax.plot(t, ach_o, color='gray',   label='open loop')
ax.plot(t, ach_c, color='black',  label='closed loop')
ax.set_xlabel('time (s)'); ax.set_ylabel('decoded brightness')
ax.set_title('Open vs closed loop · panning "OPEN" + adaptation')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# Six sampled frames: input | open phosphenes | open reconstruction |
# closed phosphenes | closed reconstruction. Watch the right pair stay
# legible while the left pair fades.
sample_idx = np.linspace(5, len(tgt_o) - 1, 6, dtype=int)
fig, axes = plt.subplots(6, 5, figsize=(11, 11))
col_titles = ['input', 'open phosphenes', 'open reconstruction',
              'closed phosphenes', 'closed reconstruction']
for i, k in enumerate(sample_idx):
    rowdata = [scenes_o[k], fields_o[k], recs_o[k], fields_c[k], recs_c[k]]
    for j, im in enumerate(rowdata):
        ax = axes[i, j]
        ax.imshow(im, cmap='gray', vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        if i == 0: ax.set_title(col_titles[j], fontsize=10)
    axes[i, 0].set_ylabel(f't = {k / params["run"]["fps"]:.1f}s', fontsize=9)
plt.tight_layout(); plt.show()

c_o = float(np.mean([contrast(f) for f in fields_o]))
c_c = float(np.mean([contrast(f) for f in fields_c]))
mae_o = float(np.abs(tgt_o - ach_o).mean())
mae_c = float(np.abs(tgt_c - ach_c).mean())
print()
print(f'open   loop · phosphene contrast {c_o*100:5.1f}% · MAE {mae_o:.4f}')
print(f'closed loop · phosphene contrast {c_c*100:5.1f}% · MAE {mae_c:.4f}')
print(f'closed-loop improvement: contrast +{(c_c-c_o)*100:.1f} pp  ·  MAE {(mae_o-mae_c)/max(mae_o,1e-6)*100:+.0f}%')
'''))

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
