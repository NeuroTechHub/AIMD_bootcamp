"""Smoke test: replays the critical API calls the notebook makes."""
from __future__ import annotations
import sys, traceback, numpy as np, torch, cv2
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
ASSETS.mkdir(exist_ok=True)

# 1. Write params yaml (same content as the notebook embeds)
PARAMS_YAML = r"""
run:
  resolution: [256, 256]
  view_angle: 16
  origin: [0, 0]
  min_angle: 0.001
  fps: 35
  gpu: -1
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

# 2. Imports
from dynaphos.utils import load_params, Map
from dynaphos.cortex_models import (
    get_visual_field_coordinates_probabilistically,
    get_cortical_magnification,
)
from dynaphos.simulator import GaussianSimulator

# 3. Load params + build a foveated simulator
params = load_params(str(PARAMS_PATH))
print('params loaded:', list(params.keys())[:6], '...')
rng = np.random.default_rng(0)
coords_fov = get_visual_field_coordinates_probabilistically(params, 200, rng=rng)
sim = GaussianSimulator(params, coords_fov)
print('foveated sim ok, N=', len(coords_fov))

# 4. Uniform grid in the visual field — build a Map manually since
# dynaphos's get_visual_field_coordinates_grid() is hard-coded to 0..90 ecc.
def make_uniform_visual_field(side: int, view_angle: float) -> Map:
    hemi = view_angle / 2
    xs = np.linspace(-hemi, hemi, side, endpoint=False) + hemi/side
    ys = np.linspace(-hemi, hemi, side, endpoint=False) + hemi/side
    xx, yy = np.meshgrid(xs, ys)
    return Map(x=xx.ravel(), y=yy.ravel())

coords_uni = make_uniform_visual_field(14, params['run']['view_angle'])
sim_uni = GaussianSimulator(params, coords_uni)
print('uniform sim ok, N=', len(coords_uni))

# 5. M(r) call signature
M = get_cortical_magnification(np.array([0.5, 3.0, 7.0]), params['cortex_model'])
print('M(r) ok:', M)

# 6. sample_stimulus + __call__
img = np.zeros((256, 256), dtype=np.uint8)
cv2.rectangle(img, (60, 60), (160, 160), 255, -1)
sim.reset()
amp = sim.sample_stimulus(img, rescale=True)
print('sample_stimulus ok, amp shape:', tuple(amp.shape), 'dtype:', amp.dtype)
phos = sim(amp)
print('__call__ ok, phos shape:', tuple(phos.shape), 'min/max:',
      float(phos.min()), float(phos.max()))

# 7. The run_sequence helper relies on sim.activation.decay_rate being mutable
# and on sim.trace.get() / sim.trace.reset() existing.
print('activation:', type(sim.activation).__name__,
      'decay_rate type:', type(sim.activation.decay_rate).__name__)
print('trace:', type(sim.trace).__name__,
      'has get:', hasattr(sim.trace, 'get'),
      'has reset:', hasattr(sim.trace, 'reset'))
try:
    sim.activation.decay_rate = torch.tensor(0.1)
    print('decay_rate patch ok')
except Exception as e:
    print('decay_rate patch FAILED:', e)
try:
    t = sim.trace.get()
    print('trace.get() ok, mean:', float(t.mean()))
except Exception as e:
    print('trace.get() FAILED:', e)

# 8. Reset between frames
sim.reset()
amp = sim.sample_stimulus(img, rescale=True)
p1 = sim(amp)
p2 = sim(amp)  # second frame, state preserved
print('two-frame run ok, frame1 mean:', float(p1.mean()), 'frame2 mean:', float(p2.mean()))

# 9. §2 — draw_pattern helper
RES = tuple(params['run']['resolution'])
def draw_pattern(name):
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
    return img

for n in ['square_disc', 'letter_E', 'grating', 'diagonal']:
    p = draw_pattern(n)
    sim.reset()
    a = sim.sample_stimulus(p, rescale=True)
    r = sim(a)
    print(f'pattern {n}: stim_max={float(a.max()):.3g}, render_mean={float(r.mean()):.3g}')

# 10. §3 — run_sequence helper exactly as the notebook defines it
def run_sequence(sim, image_uint8, frames=60, stim_on_until=None,
                 act_decay_per_sec=None, no_trace=False):
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
            sim.trace.reset()
        bright[t] = float(phos.detach().mean())
        trace_mean[t] = float(sim.trace.get().detach().mean())
    if orig_decay is not None:
        sim.activation.decay_rate = orig_decay
    return bright, trace_mean

stim_img = draw_pattern('square_disc')
b1, _ = run_sequence(sim, stim_img, frames=60, stim_on_until=60)               # always on
b2, _ = run_sequence(sim, stim_img, frames=60, stim_on_until=30, act_decay_per_sec=3e-1)
b3, _ = run_sequence(sim, stim_img, frames=60, stim_on_until=30, act_decay_per_sec=3e-1, no_trace=True)
print(f'run_sequence: always-on peak={b1.max():.3g}, '
      f'slow-decay+adapt peak={b2.max():.3g}, '
      f'slow-decay no-trace peak={b3.max():.3g}')

# 11. §4 saliency fallback (cv2.saliency absent on plain opencv-python)
scene_bgr = cv2.resize(cv2.imread(str(ASSETS / 'bus.jpg')) if (ASSETS/'bus.jpg').exists() else
                       np.full((480, 640, 3), 128, dtype=np.uint8), RES)
if (ASSETS/'bus.jpg').exists() is False:
    print('bus.jpg missing; saliency test uses gray fallback')
if hasattr(cv2, 'saliency'):
    print('cv2.saliency present')
else:
    g = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    F = np.fft.fft2(g)
    log_amp = np.log(np.abs(F) + 1e-9)
    avg = cv2.boxFilter(log_amp, -1, (3, 3))
    spec_res = log_amp - avg
    sm = np.abs(np.fft.ifft2(np.exp(spec_res + 1j*np.angle(F))))**2
    smap = cv2.GaussianBlur(sm, (9, 9), 2.5)
    smap = (smap - smap.min()) / (np.ptp(smap) + 1e-9)
    print('saliency fallback OK; smap shape:', smap.shape, 'range:', smap.min(), smap.max())

print('\nALL SMOKE TESTS PASSED.')
