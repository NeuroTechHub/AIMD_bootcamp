"""Time run_sequence on the new sim_t to confirm §3 is fast enough."""
import time, numpy as np, torch, cv2
from pathlib import Path

PARAMS_PATH = Path('phosphene-simulation/assets/params.yaml')
from dynaphos.utils import load_params
from dynaphos.cortex_models import get_visual_field_coordinates_probabilistically
from dynaphos.simulator import GaussianSimulator

params = load_params(str(PARAMS_PATH))

def build_sim(N, seed):
    return GaussianSimulator(
        params,
        get_visual_field_coordinates_probabilistically(
            params, N, rng=np.random.default_rng(seed)))

def run_sequence(sim, image_uint8, frames=140, stim_on_until=None,
                 act_decay_per_sec=None, no_trace=False):
    if stim_on_until is None:
        stim_on_until = frames // 2
    sim.reset()
    if act_decay_per_sec is not None:
        sim.activation.decay_rate = torch.tensor(-float(np.log(act_decay_per_sec)))
    n_e = sim.num_phosphenes
    bright = np.zeros(frames)
    for t in range(frames):
        amp = sim.sample_stimulus(image_uint8, rescale=True) if t < stim_on_until else torch.zeros(n_e)
        phos = sim(amp)
        if no_trace:
            sim.trace.reset()
        bright[t] = float(phos.detach().mean())
    return bright

img = np.zeros((256, 256), dtype=np.uint8)
cv2.rectangle(img, (60, 60), (160, 160), 255, -1)

for N in (200, 500, 1000):
    sim = build_sim(N, 7)
    t0 = time.time()
    b = run_sequence(sim, img, frames=140, stim_on_until=140)
    dt = time.time() - t0
    print(f'N={N:4d}  140 frames in {dt:6.2f}s  ({dt*1000/140:.1f} ms/frame)')
