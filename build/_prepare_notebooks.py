"""Mechanical notebook cleanup and paired-solution generation.

This keeps JSON edits out of hand-written patches:
  python build/_prepare_notebooks.py
"""
from __future__ import annotations

import copy
import json
import uuid
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MODULES = REPO / "modules"

WORKSHOP_NOTEBOOKS = [
    MODULES / "M1-computer-vision-notebooks" / "computer-vision.ipynb",
    MODULES / "M2-deepgaze-and-gaze" / "gaze_workshop.ipynb",
    MODULES / "M3-neuromod-and-stim" / "neuromod-and-stim.ipynb",
    MODULES / "M4-phosphene-simulation" / "phosphene-simulation.ipynb",
    MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop.ipynb",
]

SOLUTION_NOTEBOOKS = [
    MODULES / "M1-computer-vision-notebooks" / "computer-vision-solution.ipynb",
    MODULES / "M2-deepgaze-and-gaze" / "gaze_workshop_solutions.ipynb",
    MODULES / "M3-neuromod-and-stim" / "neuromod-and-stim-solution.ipynb",
    MODULES / "M4-phosphene-simulation" / "phosphene-simulation-solution.ipynb",
]


def read_nb(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_nb(path: Path, nb: dict) -> None:
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def clear_code_outputs(nb: dict) -> None:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []


def clear_error_outputs(nb: dict) -> None:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = [
                output for output in cell.get("outputs", [])
                if output.get("output_type") != "error"
            ]


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    cell["source"] = text.splitlines(keepends=True)


def md_cell(text: str, tag: str | None = None) -> dict:
    cell = {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "source": (text.rstrip() + "\n").splitlines(keepends=True),
    }
    if tag:
        cell["metadata"]["tags"] = [tag]
    return cell


def code_cell(text: str, tag: str | None = None) -> dict:
    cell = {
        "cell_type": "code",
        "id": uuid.uuid4().hex[:12],
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": (text.rstrip() + "\n").splitlines(keepends=True),
    }
    if tag:
        cell["metadata"]["tags"] = [tag]
    return cell


SELF_CHECK_TAG = "notebook-self-check"


SELF_CHECKS = {
    MODULES / "M1-computer-vision-notebooks" / "computer-vision.ipynb": r"""checks = []
if 'gray224' in globals():
    assert gray224.shape == (224, 224), f'gray224 shape is {gray224.shape}, expected (224, 224)'
    checks.append('1.1 gray224 shape')
if 'as_float' in globals() and 'as_uint8' in globals():
    f = as_float(np.array([0, 128, 255], dtype=np.uint8))
    assert f.dtype.kind == 'f' and np.all((0 <= f) & (f <= 1)), 'as_float should return float values in [0, 1]'
    assert as_uint8(f).dtype == np.uint8, 'as_uint8 should return uint8'
    checks.append('1.2 dtype conversion')
if 'Kx' in globals() and 'Ky' in globals():
    assert np.asarray(Kx).shape == (3, 3) and np.asarray(Ky).shape == (3, 3), 'Sobel kernels should be 3x3'
    checks.append('2.2 Sobel kernels')
if 'people_mask' in globals():
    assert people_mask.ndim == 2 and people_mask.max() <= 1, 'people_mask should be a 2D binary mask'
    checks.append('3.2 people mask')
if 'activation' in globals():
    assert activation.ndim == 2 and activation.max() <= 255, 'activation should be a 2D image-like map'
    checks.append('4.2 activation map')
print('Self-checks passed:', ', '.join(checks) if checks else 'nothing to check yet')
""",
    MODULES / "M2-deepgaze-and-gaze" / "gaze_workshop.ipynb": r"""checks = []
if 'prob' in globals():
    assert np.isfinite(prob).all(), 'prob should be finite'
    assert abs(float(prob.sum()) - 1.0) < 1e-3, f'prob should sum to 1, got {prob.sum()}'
    checks.append('DeepGaze probability map')
if 'pts' in globals():
    assert len(pts) == 20, 'Exercise 1.2 asks for 20 sampled fixations'
    checks.append('sampled fixations')
if 'lengths' in globals():
    assert np.asarray(lengths).size > 0 and np.all(np.asarray(lengths) >= 0), 'saccade lengths must be non-negative'
    checks.append('saccade lengths')
if 'hist_dg' in globals():
    assert len(hist_dg) >= 15, 'cumulative reconstruction should include at least 15 fixations'
    checks.append('cumulative reconstruction history')
if 'cumulative_similarity' in globals():
    out = cumulative_similarity(dg_path[:3], face_gray, sim, fov_radius=56)
    assert len(out) == 2, 'cumulative_similarity should return (pearson, ssim)'
    checks.append('cumulative_similarity return shape')
print('Self-checks passed:', ', '.join(checks) if checks else 'nothing to check yet')
""",
    MODULES / "M3-neuromod-and-stim" / "neuromod-and-stim.ipynb": r"""checks = []
if 'charge_per_phase_nc' in globals() and 'shannon_k' in globals():
    assert abs(charge_per_phase_nc(80, 170) - 13.6) < 0.2, '80 uA x 170 us should be about 13.6 nC'
    assert shannon_k(80, 170) < SHANNON_K_LIMIT, '80 uA x 170 us should be under the conservative k limit'
    checks.append('2.1 charge and Shannon-k')
if 'us_to_cycles' in globals() and 'cycles_to_us' in globals():
    assert us_to_cycles(170) == 5, '170 us should quantize to 5 cycles at 30 kHz'
    assert abs(cycles_to_us(5) - 166.5) < 0.5, '5 cycles should be about 166.5 us'
    checks.append('2.2 cycle quantization')
if 'letter_params' in globals():
    assert isinstance(letter_params, StimParams) and len(letter_params.electrodes) > 0, 'letter_params should be a populated StimParams'
    checks.append('3.1 letter StimParams')
if 'interleave_offsets' in globals():
    offs = interleave_offsets([45, 12, 78], 300)
    assert len(offs) == 3 and min(offs) == 0 and max(offs) < 1e6/300, 'offsets should fit within one train period'
    checks.append('3.2 interleaving')
print('Self-checks passed:', ', '.join(checks) if checks else 'nothing to check yet')
""",
    MODULES / "M4-phosphene-simulation" / "phosphene-simulation.ipynb": r"""checks = []
if 'RES' in globals():
    assert tuple(RES) in [(256, 256), (128, 128)], f'unexpected simulator resolution {RES}'
    checks.append('simulator resolution')
if 'coords_fov' in globals() and 'coords_uni' in globals():
    assert len(coords_fov.x) == len(coords_uni.x), 'compare foveated and uniform layouts with the same electrode count'
    checks.append('1.2 matched layouts')
if 'renders' in globals():
    assert len(renders) >= 4, 'Exercise 2.1 should render the four preset patterns'
    checks.append('2.1 preset renders')
if 'weighted' in globals():
    assert weighted.ndim == 2 and weighted.max() <= 255, 'weighted activation should be a 2D uint8-like map'
    checks.append('4.1 weighted activation')
if 'frames' in globals():
    assert len(frames) >= 10, 'dynamic loop should produce multiple frames'
    checks.append('5.1 dynamic frames')
print('Self-checks passed:', ', '.join(checks) if checks else 'nothing to check yet')
""",
    MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop.ipynb": r"""checks = []
if 'wmap' in globals() and 'frac' in globals():
    assert wmap.shape == RES and 0 <= frac <= 1, 'weight map should match RES and centre fraction should be in [0, 1]'
    checks.append('1.1 linear decoder weights')
if 'results' in globals():
    assert len(results) >= 2, 'try at least two PID gain settings'
    checks.append('2.1 PID sweep')
if 'net' in globals():
    assert hasattr(net, 'c1') and net.c1.weight.shape[-2:] == (5, 5), 'CNN first layer should expose 5x5 filters'
    checks.append('3.1 CNN filters')
if 'OUT_WEIGHTS' in globals():
    assert OUT_WEIGHTS.exists(), f'expected exported weights at {OUT_WEIGHTS}'
    checks.append('4.1 exported weights')
print('Self-checks passed:', ', '.join(checks) if checks else 'nothing to check yet')
""",
}


def add_self_check(nb: dict, code_text: str) -> None:
    cells = []
    for cell in nb.get("cells", []):
        tags = cell.get("metadata", {}).get("tags", [])
        if SELF_CHECK_TAG not in tags:
            cells.append(cell)
    cells.append(md_cell(
        """## Notebook self-check

Run this after you have filled the exercise cells. It only checks variables that
exist in your kernel, so a fresh blank notebook prints `nothing to check yet`.
When a check fires, it catches shape/range mistakes before you compare against
the solution notebook.""",
        SELF_CHECK_TAG,
    ))
    cells.append(code_cell(code_text, SELF_CHECK_TAG))
    nb["cells"] = cells


def make_m5_solution() -> None:
    src_path = MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop.ipynb"
    out_path = MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop-solution.ipynb"
    nb = read_nb(src_path)
    solution = copy.deepcopy(nb)

    first = solution["cells"][0]
    first_src = source(first)
    first_src = first_src.replace("# M5 — Decoding & closed loop", "# M5 — Decoding & closed loop · **Solutions**")
    set_source(first, first_src)

    replacements = {
        "# your code here\n# Hint:\n#   wmap = w_lin.reshape(RES)": """# Exercise 1.1 — solution
wmap = w_lin.reshape(RES)
ctr = wmap[RES[0]//2-16:RES[0]//2+16, RES[1]//2-16:RES[1]//2+16]
frac = float(np.abs(ctr).sum() / np.abs(wmap).sum())
uniform_baseline = (32*32) / (RES[0]*RES[1])
print(f'centre-weighted fraction: {frac:.3f}')
print(f'uniform 32x32 baseline : {uniform_baseline:.3f}')
assert 0.0 <= frac <= 1.0
assert uniform_baseline < 0.1
""",
        "# your code here\n# Hint:\n#   gains = [(200, 0, 0)": """# Exercise 2.1 — solution
gains = [(200, 0, 0), (200, 200, 0), (200, 100, 40), (400, 150, 30)]
results = []
for Kp, Ki, Kd in gains:
    tgt, ach, cur = run_pid(Kp, Ki, Kd, target_fn=lambda t: 0.8)
    results.append((Kp, Ki, Kd, float(np.abs(tgt - ach).mean()), ach, cur))

for Kp, Ki, Kd, mae, _, _ in results:
    print(f'Kp={Kp:3d} Ki={Ki:3d} Kd={Kd:3d}  MAE={mae:.4f}')

best = min(results, key=lambda row: row[3])
assert best[3] < results[0][3] or best[3] < 0.25

t = np.arange(len(best[4])) / params['run']['fps']
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(t, np.full_like(t, 0.8), '--', color='C3', label='target')
ax.plot(t, best[4], color='black', label=f'best K=({best[0]}, {best[1]}, {best[2]})')
ax.set_xlabel('time (s)'); ax.set_ylabel('brightness')
ax.set_title(f'best step-target MAE {best[3]:.4f}')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",
        "# your notes here\n# Tip: you can re-plot": """# Exercise 3.1 — solution notes
print('Look for filters with adjacent positive/negative lobes: those behave like edge detectors.')
print('Filters with a bright centre and darker surround respond to compact dots or local blobs.')
print('The exact filter IDs vary because training is stochastic, so reason from the displayed pattern.')
""",
    }

    for cell in solution.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = source(cell)
        for needle, repl in replacements.items():
            if src.startswith(needle):
                set_source(cell, repl)
                break

    write_nb(out_path, solution)


def main() -> None:
    for path in WORKSHOP_NOTEBOOKS:
        nb = read_nb(path)
        clear_code_outputs(nb)
        check_code = SELF_CHECKS.get(path)
        if check_code:
            add_self_check(nb, check_code)
        write_nb(path, nb)
        print(f"cleared workshop outputs: {path.relative_to(REPO)}")

    for path in SOLUTION_NOTEBOOKS:
        nb = read_nb(path)
        clear_error_outputs(nb)
        write_nb(path, nb)
        print(f"cleared stored error outputs: {path.relative_to(REPO)}")

    make_m5_solution()
    print("wrote modules/M5-decoding-and-closed-loop/decoding-and-closed-loop-solution.ipynb")


if __name__ == "__main__":
    main()
