# NTH Bootcamp Development Plan

**Date:** 04 May 2026  
**Status:** Draft AL  
**Feedback & Update:** AL, FV, PB

## Summary

Create a high-quality, tutorial-driven NTH bootcamp plan around cortical neuroprosthesis workflows, using Dynaphos and DeepGaze as the central educational pipeline. The bootcamp combines conceptual grounding, module introductions, guided exercises, and open-ended development tracks.

The DeepGaze + Dynaphos tutorial is the flagship exercise: a polished percent-cell Python tutorial showing how gaze prediction, image preprocessing, electrode mapping, stimulation dynamics, and phosphene simulation connect into an educational closed-loop neurotech prototype.

## Audience And Prerequisites

### General Prerequisites

- Python.
- Preferred IDE compatible with Jupyter notebooks; VS Code recommended.
- Basic comfort running Python scripts or notebook-style cells.

### Vibe-Coding Track

- Free LLM account or access to an assistant, for example OpenAI, Anthropic, or Mistral.
- Goal: rapidly prototype creative neurotech ideas with guided AI support.

### Developer Track

- Preferred IDE: VS Code, Cursor, Claude Code Desktop, Codex, or equivalent.
- Goal: work deeper on code quality, performance, real-time behavior, and pipeline integration.

## Bootcamp Schedule

### 1. Introduction To Cortical Neuroprosthesis, 20 Min

- Explain visual cortical prostheses at a high level.
- Introduce phosphene vision: what is simulated, what is simplified, and why it matters.
- Frame the bootcamp goal: build small but meaningful pieces of a closed-loop cortical vision pipeline.

### 2. Introduction To The Modules, 30 Min

**Computer vision and gaze tracking**

- Image understanding.
- Saliency and scanpath prediction.
- Simulated gaze as a proxy for user exploration.

**Neuromodulation and electrode mapping**

- Electrode coordinates.
- Visual-field mapping.
- Stimulation parameters and perceptual consequences.

**Stimulator control and safety, optional**

- Mock stimulation interfaces.
- Configuration, logging, and guardrails.
- Why real stimulation requires strict safety constraints.

**Phosphene simulation**

- Dynaphos concepts.
- Phosphene maps.
- Temporal dynamics and brightness evolution.

**Decoding and closed loop**

- Neural simulation and brightness decoding.
- Feedback-driven stimulation.
- Conceptual closed-loop neuroprosthesis.

### 3. Guided Exercises, 1 Hour

**Deep learning image processing**

- Object detection and segmentation with YOLO.
- Open/world detection with YOLO-World.
- Edge detection and parameter changes.

**Gaze tracking**

- Deep-learning gaze tracking overview.
- Gaze tracking simulation.
- Natural statistics models.
- DeepGaze III scanpath generation.

**Neuromodulation**

- Define stimulation trains.
- Explore amplitude modulation.
- Explore frequency modulation.
- Map electrodes to visual-field coordinates.

**Stimulation control**

- Use a mock stimulator.
- Configure, record, and simulate stimulation.
- Compare stimulation settings to simulated percepts.

**Phosphene simulation**

- Dynaphos phosphene maps.
- Convert stimulation to phosphenes.
- Demonstrate phosphene temporal dynamics.

**Neural simulation**

- Brightness decoding exercise.

**Closed-loop neural stimulation**

- Combine gaze, image processing, stimulation, and phosphene simulation into a minimal closed-loop demo.

### 4. Vibe Coding, Development, And Experiments, 1 Hour

Run three parallel tracks.

**Experimental track**

- Build a fun, visually compelling Dynaphos experiment.
- Optimize for punch, clarity, and demo value.

**Developer track**

- Build or improve the full real-time / closed-loop pipeline.
- Optimize performance, device handling, caching, and code structure.

**Open neurotech track**

- Create an original neurotech application.
- The idea can be completely different from the provided examples as long as it connects to the bootcamp theme.

### 5. Upload Demo To GitHub, 15 Min

Submission location: `GITHUB/NTH/D-BOOTCAMP/submissions`.

Each team uploads:

- Code or notebook.
- Short README.
- Screenshot, video, or demo artifact.
- Track label: experimental, developer, or open neurotech.

### 6. Demonstrations And Networking

- Voluntary demos.
- Network/show-off session.
- Optional winner selection.

### Prizes

One prize per track:

- Experimental track.
- Developer track.
- Open neurotech track.

## Core Tools

- **Dynaphos:** https://github.com/neuralcodinglab/dynaphos  
  Use for phosphene maps, stimulation-to-phosphene conversion, and temporal dynamics.
- **DeepGaze:** https://github.com/matthias-k/DeepGaze  
  Use for saliency and DeepGaze III scanpath simulation.
- **Neurolight:** evaluate role and availability before finalizing exercises.
- **Optional:** Vimplant2, https://antonio-lozano.github.io/vimplant2/

## Flagship Tutorial: DeepGaze + Dynaphos

Use `deepgaze_dynaphos_test.py` as the scratchpad prototype and `deepgaze_dynaphos_tutorial.py` as the polished percent-cell tutorial.

## Intro Modules Tutorial

Use `nth_intro_modules.py` as the fast module sampler for the 30-minute module introduction and the first part of the guided exercises. It introduces image preprocessing, optional object detection, gaze simulation, DeepGaze III, electrode mapping, stimulation trains, mock stimulation control, Dynaphos phosphene maps, temporal dynamics, brightness decoding, and a minimal closed-loop pipeline.

Use `NTH_INTRO_MODULES_DEV_PLAN.md` as the iteration plan for this sampler.

### Tutorial Goal

Teach how a visual neuroprosthesis pipeline can combine:

- Computer vision / image preprocessing.
- DeepGaze III simulated visual exploration.
- Gaze-contingent image crops.
- Dynaphos electrode sampling.
- Stimulation dynamics.
- Phosphene percept simulation.
- Video export and multi-image batch examples.

### Tutorial Structure

- Setup, device selection, reproducible public input image.
- Dynaphos-only: image crop to activation mask to phosphene percept.
- DeepGaze-only: centerbias, fixation history, and next-fixation density.
- Coupled pipeline: DeepGaze scanpath to gaze-contingent Dynaphos crops.
- Temporal simulation: fixation dwell, saccades, and Dynaphos state over time.
- Batch demo: multiple images, batched DeepGaze forwards, final Dynaphos percepts.

### Tutorial Improvement Priorities

- Replace hardcoded local image paths with bundled public images.
- Keep optional user-image override.
- Move configuration into one clear top-level block.
- Explain methodology before each important cell.
- Keep GPU support and explain `auto`, `cpu`, and `cuda` modes.
- Save figures and videos under an `outputs/` directory.
- Keep `deepgaze_dynaphos_test.py` as the scratchpad until the tutorial version is complete.
- Keep the transparent phosphene overlay because it is visually effective.
- Keep the batch DeepGaze demo because it shows performance and scale.

### Conceptual Notes To Teach Explicitly

- DeepGaze III is a scanpath model, not just a saliency map.
- Centerbias affects predicted fixation density.
- Dynaphos simulates prosthetic visual percepts, not ordinary image filters.
- Gaze-contingent crops are conceptually closer to active vision than feeding the whole image at once.
- Resetting Dynaphos makes independent stills; preserving state shows temporal percept dynamics.
- Sobel/Canny/gray preprocessing are tutorial choices, not biological truths.

## Implementation Plan

- Maintain this file as the bootcamp development plan.
- Use `nth_intro_modules.py` for the bootcamp intro modules sampler.
- Use `deepgaze_dynaphos_tutorial.py` as the tutorial artifact.
- Keep `deepgaze_dynaphos_test.py` as the scratchpad until the tutorial version is complete.
- Write generated figures and videos to `outputs/`.
- Add a `docs/` directory later if the bootcamp grows beyond one plan file.

## Test And Acceptance Criteria

- Bootcamp plan is readable as a standalone Markdown document.
- The agenda fits the intended timing: 20 min + 30 min + 1 hour + 1 hour + 15 min + demos.
- The tutorial runs from public bundled data without local absolute paths.
- The DeepGaze + Dynaphos tutorial works on CPU and GPU.
- The tutorial produces at least one strong visual output suitable for a demo.
- Participants can complete a minimal exercise even without GPU.
- Developer-track participants have clear extension points for optimization and closed-loop work.
- Vibe-coding participants have enough structure to create a demo without needing deep codebase knowledge.

## Assumptions

- `04/05/2026` means 04 May 2026.
- The primary tutorial format remains a VS Code/Jupyter-compatible percent-cell Python script.
- The bootcamp targets new users first, with optional depth for developers and researchers.
- "Three prices" means three prizes, one per track.
- Neurolight is listed as a candidate tool but needs confirmation before being made a required dependency.
