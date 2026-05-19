# NTH Intro Modules Development Plan

**Status:** Working draft  
**Primary artifact:** `nth_intro_modules.py`  
**Companion artifact:** `deepgaze_dynaphos_tutorial.py`

## Goal

Build a fast, runnable module sampler for the NTH bootcamp. The sampler introduces the main blocks of a cortical visual neuroprosthesis pipeline before participants move into the deeper DeepGaze + Dynaphos flagship tutorial.

The file should use VS Code/Jupyter-compatible `#%%` cells. Each module should be small, visual, and hackable: participants should be able to change one or two constants and immediately see the effect.

## Teaching Shape

Each module cell should answer three questions:

- What is this module?
- What data goes in and out?
- What can participants change in two minutes?

The sampler should run without YOLO or other heavy optional packages. Optional cells should detect missing dependencies and provide a meaningful fallback instead of failing.

## Module Cells

1. **Setup and shared utilities**
   - Imports, output directory, device selection, image helpers, plotting helpers.
   - Print Python/Torch/device status.

2. **Computer vision input and preprocessing**
   - Load a bundled public image.
   - Show grayscale, blur, Sobel, Canny, and threshold masks.
   - Output: `activation_mask`.

3. **Object detection / segmentation placeholder**
   - Try optional `ultralytics` YOLO if installed.
   - Otherwise run contour-based mock object proposals.
   - Output: `detections`.

4. **Gaze simulation: natural-statistics baseline**
   - Sample a center-biased and edge-biased scanpath from simple probability maps.
   - Output: `baseline_scanpath`.

5. **Gaze simulation: DeepGaze III**
   - Try DeepGaze III if available.
   - Fall back to baseline scanpath if model loading fails.
   - Output: `scanpath`.

6. **Neuromodulation and electrode mapping**
   - Load Dynaphos config and electrode coordinates.
   - Show visual-field electrode positions.
   - Output: `simulator`, `coordinates_visual_field`.

7. **Stimulation trains**
   - Define pulse-width, frequency, and amplitude arrays.
   - Plot stimulation over time.
   - Output: `stim_train`.

8. **Amplitude and frequency modulation**
   - Compare low/high amplitude and frequency settings.
   - Render representative Dynaphos percepts.

9. **Mock stimulator control**
   - Validate and record stimulation commands.
   - Demonstrate configuration, recording, replay, and safety checks.
   - Output: `mock_stimulator`.

10. **Dynaphos phosphene maps**
    - Visualize individual phosphene basis maps and electrode centers.

11. **Stimulation to phosphenes**
    - Convert a gaze-centered crop into stimulation and then phosphenes.
    - Output: `phosphene_frame`.

12. **Temporal dynamics**
    - Compare resetting Dynaphos every frame versus preserving state.
    - Show brightness buildup/fade across a short sequence.

13. **Brightness decoding**
    - Use a simple decoder to estimate perceived brightness from phosphene frames.
    - Explain this as a toy neural/behavioral readout, not a validated model.

14. **Minimal closed-loop pipeline**
    - Connect image -> gaze -> crop -> preprocessing -> stimulation -> phosphenes -> brightness feedback.
    - Output: one integrated figure and a command log.

15. **Track prompts**
    - Experimental track: punchy Dynaphos demo ideas.
    - Developer track: real-time/optimization tasks.
    - Open neurotech track: original application prompts.

## Implementation Defaults

- Default image: `skimage.data.astronaut()`.
- Image size: `384 x 384` for speed.
- Dynaphos resolution: keep config default unless explicitly changed.
- Preprocessing method: Sobel for the main activation mask.
- Device mode: `NTH_DEVICE=auto|cpu|cuda`.
- Generated figures: `outputs/intro_modules_*.png`.
- Heavy dependencies: optional and guarded.

## Acceptance Criteria

- `nth_intro_modules.py` runs from top to bottom on CPU.
- `nth_intro_modules.py` runs from top to bottom on GPU when CUDA PyTorch is available.
- Missing `ultralytics` does not fail the tutorial.
- Missing or failing DeepGaze falls back to the baseline scanpath.
- Dynaphos cells produce electrode maps, stimulation plots, phosphene maps, and temporal dynamics figures.
- The final closed-loop cell creates one clear integrated figure.
- The file is readable as a tutorial, not just a script.

## Iteration Backlog

- Add real YOLO / YOLO-World install notes once the bootcamp environment is fixed.
- Add Neurolight if its role and API are confirmed.
- Add challenge cards as separate Markdown files if the bootcamp expands.
- Consider syncing this percent-cell script into an `.ipynb` once the lesson stabilizes.
