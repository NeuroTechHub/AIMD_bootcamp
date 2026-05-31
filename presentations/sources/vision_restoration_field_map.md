# Vision restoration — field map (May 2026)

Companion reference for `bootcamp_talk_AL.pptx`. Captures who is doing what,
where in the visual pathway, with what status, so the talk slides can cite
accurately. Sourced from a 2026-05-31 review chat (Antonio Lozano, Cesc
Varkevisser, Jorge Sanmartin, Radovan Vodila) cross-checked against primary
sources listed at the bottom.

## Where can you intervene? (anatomical map)

```
RETINA ──► OPTIC NERVE ──► LGN (thalamus) ──► V1 (cortex) ──► higher visual
   ▲                                              ▲
   │                                              │
   PRIMA, Argus, Bionic Eye          CORTIVIS, Orion, NeuraViPeR / SIGHTED*
   (* SIGHTED actually targets LGN, see below)
```

Each tissue target reaches a different patient population.

| Target          | Reaches blindness from              | Skips                       |
|-----------------|-------------------------------------|-----------------------------|
| Retina          | photoreceptor death (AMD, RP)       | needs intact optic nerve+   |
| LGN (thalamus)  | retina + optic-nerve damage         | needs intact V1             |
| V1 cortex       | everything upstream                 | only needs intact V1+higher |

Retinal reaches the largest *count* of patients (AMD alone) but only those
whose downstream pathway is intact. Cortical reaches the broadest *spectrum*
of causes — the only option for glaucoma, optic-nerve atrophy, end-stage RP.

## Active programs (2026-05)

### Retinal

| Program            | Org                                  | Tissue        | Status                                                                                          |
|--------------------|--------------------------------------|---------------|-------------------------------------------------------------------------------------------------|
| **PRIMA**          | Pixium (FR) → **Science Corp** (US)  | subretinal    | **Photovoltaic; PRIMAvera trial NEJM Oct 2025; 38 GA patients; CE/FDA path through 2026.**     |
|                    | Daniel Palanker, Stanford            |               | 2x2 mm chip, 378 photovoltaic pixels (100 µm each), 30 µm thick. Wireless — NIR glasses.        |
| Argus II           | Second Sight                         | epi-retinal   | Discontinued 2019; ~350 implanted. Patients largely unsupported.                                |
| Alpha IMS / AMS    | Retina Implant AG                    | subretinal    | Discontinued 2019.                                                                              |
| Optogenetic        | GenSight (FR), Bionic Sight (US)     | retina (gene) | Sahel 2021 NEJM — first optogenetic vision restoration in a human.                              |

Note: Pixium also has roots in Palanker's Stanford lab. Diego Ghezzi
(EPFL → ophthalmology) has parallel photovoltaic work but is not directly
on the PRIMA program (open per chat — needs confirmation).

### LGN

| Program            | Org                                                   | Status                                                                                                                                                       |
|--------------------|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SIGHTED**        | **Phosphoenix** (NL co.; NIN spin-off) + EU partners  | EIC Transition, 2025– . Targets LGN with >1000 electrodes. Builds on NeuraViPeR (concluded 2/2025). Preclinical → preparing first-in-human.                  |

### V1 cortex

| Program            | Org                                          | Approach                       | Status                                                                                                            |
|--------------------|----------------------------------------------|--------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **CORTIVIS**       | **Eduardo Fernández, UMH Elche** + IMED, EU  | Penetrating Utah, 96–100 ch    | **Active first-in-human. Bernadeta Gómez (2021 NEJM). Sci Adv 2025: real-time bidirectional implant in 2 volunteers.** |
| **Orion**          | **Cortigent** (ex–Second Sight, CA)          | Subdural surface, 60 ch        | EFS (NCT03344848). Mike Beauchamp (Baylor) — "drawing on cortex" approach: dynamic sequential stim for shape recognition (Cell 2020). Argus stack repurposed for cortex; needs mA currents → large phosphenes, occasional seizures.* |
| NeuraViPeR (H2020) | 7-org EU consortium                          | Penetrating, flexible probes   | Concluded Feb 2025. Antonio's NIN work fed dynaphos here.                                                          |

\* The "Argus to Orion" lineage is a tech-transfer story: epi-retinal hardware
on a different organ. Per Cesc, currents and electrode size are mismatched
for the cortex — the drawing-on-cortex trick is the workaround.

### Adjacent (non-electrical)

| Approach              | Example                                         | Status                                                |
|-----------------------|-------------------------------------------------|-------------------------------------------------------|
| Gene therapy          | Luxturna (Spark/Roche) — RPE65 LCA              | Approved 2017.                                        |
| Stem cell             | Lineage / Astellas (RPE replacement)            | Clinical trials.                                      |
| Sonogenetics          | Various academic                                | Pre-clinical.                                         |

## Common confusions resolved

- **Phosphoenix ≠ a program.** Phosphoenix BV is a Dutch *company* (NIN
  spin-off; Roelfsema, Chen, Monna). It coordinates the SIGHTED consortium.
- **PRIMA ≠ Argus successor.** PRIMA is photovoltaic, ex-Pixium, now
  Science Corp. Argus → Cortigent → Orion is the other lineage entirely.
- **Pixium IP → Science Corp** (Max Hodak, ex-Neuralink co-founder) in 2024.
- **CORTIVIS is alive.** The "expired?" question in the chat — no, it's
  the active first-in-human European cortical program.
- **Second Sight → Vivani is wrong.** The Argus/Orion IP went to **Cortigent**.

## Where this bootcamp lives

The deck is built around the **V1 cortical** column. Module pipeline
(M1–M5) mirrors a cortical prosthesis end-to-end: image processing →
gaze → safe stimulation → phosphene simulation → closed-loop decoding.
CORTIVIS (UMH) and NeuraViPeR/SIGHTED (Phosphoenix) are the partner
programs whose real device parameters inform M3 (Utah geometry, Ripple
ticks) and M4 (dynaphos forward model).

## Primary sources

- PRIMA — Palanker, Cusumano et al. *NEJM* 2025: <https://www.nejm.org/doi/full/10.1056/NEJMoa2501396>
- PRIMA acquisition — Science Corp press release 2024-04-25: <https://science.xyz/news/>
- Orion "drawing on cortex" — Beauchamp et al. *Cell* 2020: <https://www.sciencedirect.com/science/article/pii/S0092867420304967>
- CORTIVIS NEJM — Fernández et al. 2021: <https://www.nejm.org/doi/10.1056/NEJMc2034731>
- CORTIVIS Sci Adv 2025 — UMH press: <https://www.eurekalert.org/news-releases/1104900>
- CORTIVIS recent partial recovery — UMH press: <https://www.eurekalert.org/news-releases/1114969>
- SIGHTED — CORDIS: <https://cordis.europa.eu/project/id/101212687>
- NeuraViPeR — CORDIS: <https://cordis.europa.eu/project/id/899287>
- Phosphoenix — <https://www.phosphoenix.nl/>
