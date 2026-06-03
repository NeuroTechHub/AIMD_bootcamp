# AIMD Workshop 2026 NTH bootcamp materials

Materials for the AIMD Workshop 2026 NeuroTechHub bootcamp: the organizers'
plan plus five standalone, browser-only interactive modules.

Open [bootcamp-plan.html](bootcamp-plan.html) to start. Each module is a single
HTML page that runs in any modern browser — no server, no install.

**Pipeline foundation.** The five modules walk through the cortical visual-prosthesis
pipeline described in Lozano A., Suárez J.S., Soto-Sánchez C., Garrigós J.,
Martínez-Alvarez J.J., Ferrández J.M., Fernández E. —
_Neurolight: A Deep Learning Neural Interface for Cortical Visual Prostheses_,
International Journal of Neural Systems **30**(09): 2050045 (2020).
[doi:10.1142/S0129065720500458](https://doi.org/10.1142/S0129065720500458).
Camera → vision (M1) → gaze (M2) → stimulation (M3) → phosphenes (M4) →
decoding/closed loop (M5) traces that paper one module at a time.

## Tree

```
AIMD_bootcamp/
├── bootcamp-plan.html              # the bootcamp plan (organizers' page)
├── README.md
├── .gitignore
├── .vscode/
│   └── settings.json               # pins Live Server port 5506
├── build/
│   └── _build_bootcamp.py          # regenerator for the plan + M3 + M5
├── dev-plans/
│   ├── NTH_BOOTCAMP_DEV_PLAN_2026-05-04.md
│   └── NTH_INTRO_MODULES_DEV_PLAN.md
└── modules/
    ├── M1-computer-vision.html        # M1 — Lefteris's playground (OpenCV.js + YOLO + webcam)
    ├── M2-deepgaze-and-gaze.html      # M2 — Lefteris's workshop (synthetic DeepGaze sim)
    ├── M3-neuromod-and-stim.html      # M3 — Antonio's playground (stim params + Conductor live)
    ├── M4-phosphene-simulation.html   # M4 — Lefteris's simulator (dynaphos in 400 lines JS)
    ├── M5-decoding-and-closed-loop.html  # M5 — closed-loop decoding playground
    └── assets/                     # M1's image + YOLO masks + base64 bundle
```

`old/` (gitignored) holds reference-only material — currently `stim-deep-dive.html`, the
Neurolight2 style reference. Keep it locally if you want to crib styling; nothing in the
shipped tree depends on it.

Open any module in a browser. None of them need a server. M1's YOLO download is
~25 MB on first use (in-browser, cached).

## Setup

By the end of this chapter you'll have **JupyterLab open in your browser**,
ready to run the M1 – M5 notebooks. Allow ~15 minutes if everything goes
smoothly, longer on the first PyTorch download.

If you've never coded before, follow every step. If you already have git and
Python tooling, skip to step 4.

### 1. Open a terminal

This is the window where you'll type commands. You don't need to understand it
yet — just keep it open through the setup.

- **macOS:** press `⌘`+`space`, type `Terminal`, press `enter`.
- **Windows:** press the Windows key, type `PowerShell`, press `enter`.
  (Use PowerShell, not the older "Command Prompt".)
- **Linux:** open your preferred terminal emulator.

A window opens with a blinking cursor next to a prompt. From here on,
"run X" means: type X, press `enter`.

### 2. Install git

Git is how you'll download (clone) the bootcamp materials. Check whether you
already have it:

```bash
git --version
```

If you see a version number, skip to step 3. Otherwise:

- **macOS:** run `xcode-select --install`. A dialog pops up — click
  **Install** and wait (~5 minutes).
- **Windows:** download the installer from <https://git-scm.com/download/win>,
  run it, and accept the defaults.
- **Linux:** `sudo apt install git` (Debian/Ubuntu) or your distro's
  equivalent (`dnf install git`, `pacman -S git`, …).

After install, **close the terminal and open a new one**, then re-run
`git --version` to confirm.

### 3. Install uv

`uv` is the Python tool we use. With one command it installs Python itself
_and_ every package the notebooks need — no virtualenv juggling, no
"which Python is on my PATH" headaches.

Follow the official install instructions for your OS:
<https://docs.astral.sh/uv/getting-started/installation/>

The quick versions are:

- **macOS / Linux:**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows (PowerShell):**

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

**Close the terminal and open a new one** so it picks up the new tool, then
confirm:

```bash
uv --version
```

### 4. Clone this repo

Pick a folder you can find later (your Desktop or a `Documents/` folder is
fine). `cd` into it, then:

```bash
git clone https://github.com/NeuroTechHub/AIMD_bootcamp.git
cd AIMD_bootcamp
```

You're now inside the project. All remaining commands run from here.

### 5. Install Python + every dependency

```bash
uv sync
```

What this does: uv reads `pyproject.toml`, downloads the right version of
Python if your machine doesn't have it, creates an isolated environment under
`.venv/`, and installs every package the notebooks need (NumPy, PyTorch,
OpenCV, DeepGaze, dynaphos, JupyterLab, …). Expect **5 – 10 minutes** the
first time — PyTorch alone is ~1 GB.

A wall of progress bars finishing without a red error at the bottom means
you're good.

### 6. Launch JupyterLab

```bash
uv run jupyter lab
```

A browser tab opens automatically at <http://localhost:8888>. In the file
panel on the left, navigate to `modules/M1-computer-vision-notebooks/` and
double-click `computer-vision.ipynb`.

To stop JupyterLab later: come back to the terminal and press `Ctrl`+`C`
twice.

### 7. Verify it works

In the open notebook, click the first code cell and press `Shift`+`Enter`.
If it prints output without a red error box, Python, the environment, and
the kernel are all wired up. You're ready for the workshop.

### Common problems

- **`command not found: git` or `uv` right after installing.** Close the
  terminal and open a new one. Installers update your shell's `PATH`, but
  not the session that's already running.
- **`uv sync` fails on `deepgaze-pytorch`.** That package is pulled straight
  from GitHub. Confirm step 2 worked (`git --version`) and retry.
- **JupyterLab doesn't open a browser.** Look at the terminal output — there's
  a line like `http://127.0.0.1:8888/lab?token=…`. Copy it into your browser
  manually.
- **Notebook says "kernel not found".** In JupyterLab use
  `Kernel → Change Kernel` and pick the one matching this project's `.venv`.

## For organizers

Repo validators (attendees don't need to run these):

```bash
uv run build/validate_notebooks.py                       # lightweight hygiene checks
uv run build/validate_notebooks.py --execute-solutions   # heavy: run M1/M3/M4/M5 solutions
uv run build/validate_notebooks.py --execute-all-solutions  # also run M2 DeepGaze
```

Each notebook also ships its own Colab-friendly `%pip install` cell (packages
listed inline), so notebooks open in Colab without any local setup.
`requirements-notebooks.txt` mirrors `pyproject.toml` for users who prefer
plain `pip install -r requirements-notebooks.txt` — keep the two in sync when
dependencies change.

## Who edits what

| File                                       | Owned by         | Source of truth                         |
| ------------------------------------------ | ---------------- | --------------------------------------- |
| `bootcamp-plan.html`                       | the team         | generated by `build/_build_bootcamp.py` |
| `modules/M1-computer-vision.html`          | Lefteris & Jorge | edit the HTML directly                  |
| `modules/M2-deepgaze-and-gaze.html`        | Lefteris & Jorge | edit the HTML directly                  |
| `modules/M3-neuromod-and-stim.html`        | Antonio          | generated by `build/_build_bootcamp.py` |
| `modules/M4-phosphene-simulation.html`     | Lefteris & Jorge | edit the HTML directly                  |
| `modules/M5-decoding-and-closed-loop.html` | Antonio          | edit the HTML directly                  |

The four hand-authored playgrounds (M1 CV, M2 Gaze, M4 Phosphene, M5
Decoding) live in HTML with bespoke JS. The generator **refuses to
overwrite** them — it only emits the plan and the M3 playground.

Notebook maintenance is mechanical:

```bash
uv run build/_prepare_notebooks.py
```

That clears outputs from workshop notebooks, removes stored error outputs from
solution notebooks, and rebuilds the M5 solution companion.

## Regenerating

```bash
uv run build/_build_bootcamp.py
```

That overwrites `bootcamp-plan.html` and `modules/M3-neuromod-and-stim.html`
from the generator's source. The four hand-authored playgrounds are left
untouched.

If you change Lefteris's playgrounds, just edit the HTML directly — no rebuild
needed.

## Module summaries

- **M1 Computer vision** — OpenCV.js pixel-level operators (Sobel, Canny,
  thresholding), in-browser YOLO via TensorFlow.js + COCO-SSD, live webcam loop
  with five processing modes. Self-check + Next pointing at
  `computer-vision.ipynb`.
- **M2 Gaze & DeepGaze** — four canvas demos: heatmap vs scanpath, inhibition
  of return, three-input DeepGaze pipeline diagram, scanpath sampler with stats
  histograms (with axis ticks and units). Synthetic toy model on the page; the
  real pretrained DeepGaze III lives in the notebook. Includes an explicit
  treatment of why gaze still applies in prosthesis users.
- **M3 Neuromodulation & stim** — single-electrode biphasic pulse demo with
  five parameter tabs; Utah-array configuration table with draft-and-Add model;
  real-time Conductor live view (2×2 quad: Utah-live spatial flash, carousel
  channels×time, safety chips with Shannon-k check in µC, cumulative-charge
  trace). Train scheduling is start-to-start (train period) so multi-train runs
  stay phase-locked. Surprise-me button populates random stim configs;
  Configure / Connect / Stim to run.
- **M4 Phosphene simulation** — single-phosphene basis explorer, electrode-
  population viewer with layout selector, image-to-phosphenes forward demo
  with an animate-drift option (dynamic stimulus), temporal-dynamics player
  with leaky integrator and adaptation trace. Self-check, Tools & references,
  and a deeper-dive pointer to `phosphene-simulation.ipynb`.
- **M5 Decoding & closed loop** — closed-loop pipeline diagram, single-electrode
  brightness readout with a mean-pixel decoder, classical PID controller on
  dynaphos's leaky integrator with target chooser (step/square/sine/ramp)
  and Kp/Ki/Kd sliders + presets, in-browser TF.js MLP trained on synthetic
  phosphene canvases, hand-tuned vs end-to-end preprocessor comparison, and
  a live 2×2 quad showing the whole loop end-to-end with an open/closed
  toggle. Self-check, Where to next, and Tools & references.

## Shared visual idiom

All five modules use the same palette (`--ink/--paper/--accent`), Inter +
JetBrains Mono fonts, a clickable pipeline strip (M1→M5 with current marked
`here`), numbered TOC, callout asides, Self-check section with
`<details class='prompt'>` blocks, prev/next module navigation (`.module-nav`)
at the top and bottom of every page, a `Tools & references` block, and a
`NTH bootcamp · Mn · back to plan` footer.

## Acknowledgements & references

The modules build on open tools and published work. Each module page carries
its own clickable `Tools & references` block; the full list:

- **OpenCV.js** — in-browser computer vision (M1 edge/threshold operators).
  <https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html>
- **TensorFlow.js + COCO-SSD** — in-browser object detection (M1 YOLO demo +
  webcam). <https://www.tensorflow.org/js> ·
  <https://github.com/tensorflow/tfjs-models/tree/master/coco-ssd>
- **YOLO** — Redmon, Divvala, Girshick & Farhadi (2016), _You Only Look Once_.
  doi:10.1109/CVPR.2016.91
- **DeepGaze** (`deepgaze_pytorch`) — Kümmerer et al. saliency/scanpath models
  (M2). <https://github.com/matthias-k/DeepGaze> · DeepGaze III:
  doi:10.1167/jov.22.5.7
- **Shannon limit** — Shannon (1992), doi:10.1109/10.126616; Cogan (2008),
  doi:10.1146/annurev.bioeng.10.061807.160518; Cogan, Ludwig, Welle & Takmakov
  (2016), _Tissue damage thresholds_, J. Neural Eng. 13(2):021001 (M3 safety).
- **Ripple Neuro** — research stimulation systems; the M3 mock stimulator API
  mirrors a real device manual. <https://rippleneuro.com/>
- **dynaphos** — van der Grinten et al. (2024), _Towards biologically plausible
  phosphene simulation_, eLife 13:e85812, doi:10.7554/eLife.85812 (M4 forward
  model). <https://github.com/neuralcodinglab/dynaphos>
- **Phosphene figure / clinical evidence** — de Ruyter van Steveninck et al.
  (2022), doi:10.1167/jov.22.2.20 (CC BY 4.0); Fernández et al. (2021),
  doi:10.1172/JCI151331.

## Vision-restoration field

Long-form reference for the broader vision-restoration field — every
active program by target tissue (retina · LGN · V1), with company /
consortium links and a primary-sources list. Useful for placing this
bootcamp's V1 / cortical scope in context:

- [docs/vision-restoration-field.md](docs/vision-restoration-field.md)

Linked from every module's `Further reading` block and from slides 7–9
of [presentations/bootcamp_talk_AL.pptx](presentations/bootcamp_talk_AL.pptx)
("Where to intervene", "Cortical landscape", "Who's building").

## Web to update

Once the content is final, update the public schedule page at
<https://www.aanmelder.nl/aimdworkshop2026/bootcamp> with the final agenda,
prerequisites, per-track descriptions, and prizes.
