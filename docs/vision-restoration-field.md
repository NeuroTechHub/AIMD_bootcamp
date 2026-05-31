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

| Program             | Org                                          | Tissue          | Status                                                                                              |
|---------------------|----------------------------------------------|-----------------|-----------------------------------------------------------------------------------------------------|
| **PRIMA**           | Pixium (FR) → **Science Corp** (US)          | subretinal      | **Photovoltaic, 2×2 mm chip, 378 pixels (100 µm each), 30 µm thick. Wireless — NIR glasses.**       |
|                     | Daniel Palanker, Stanford                    |                 | **PRIMAvera trial — NEJM Oct 2025: 38 GA patients, 80% gained meaningful acuity.**                  |
|                     |                                              |                 | CE expected mid-2026, Germany first market. Series C $230M closed March 2026 ($1.5B valuation).     |
| Argus II            | Second Sight → **Cortigent** (Valencia, CA)  | epi-retinal     | First HDE-approved retinal implant. FDA HDE Feb 2013; CE 2011. **>350 implanted, $150K each.**      |
|                     | Founded by Alfred Mann; CEO Robert Greenberg |                 | **Discontinued 2019** (support ended 2020). IP → Cortigent 2023, repurposed for cortex (Orion).     |
|                     |                                              |                 | Most patients no longer using the device per 2024 follow-up — cognitive load + cessation of support.|
| **BVT** / Bionic    | Bionic Vision Technologies (AU)              | suprachoroidal  | **44-channel second-gen prosthesis; 2-year safety + efficacy in advanced RP (Allen 2025, CEO).**    |
| Vision Australia    |                                              |                 | 4-pt pilot; functional vision + ADL improvements. FDA path next.                                    |
| Alpha IMS / AMS     | Retina Implant AG                            | subretinal      | Discontinued 2019.                                                                                  |
| **GenSight GS030**  | GenSight Biologics (FR)                      | retina (gene)   | **Optogenetic — AAV2.7m8 + ChrimsonR + light-stim goggles. PIONEER Phase I/II ongoing 2025.**       |
|                     | José-Alain Sahel                             |                 | Nature Medicine 2021 — first optogenetic vision restoration in a human (single-pt case).            |
| Bionic Sight        | Sheila Nirenberg (US)                        | retina (gene)   | Optogenetic + encoder approach.                                                                     |

Note: Pixium roots back to Palanker's Stanford lab. Diego Ghezzi (EPFL → ophthalmology) has
parallel photovoltaic work but not on PRIMA directly (open per chat — needs confirmation).

### LGN

| Program            | Org                                                   | Status                                                                                                                                                       |
|--------------------|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SIGHTED**        | **Phosphoenix** (NL co.; NIN spin-off) + EU partners  | EIC Transition, 2025– . Targets LGN with >1000 electrodes. Builds on NeuraViPeR (concluded 2/2025). Preclinical → preparing first-in-human.                  |

### V1 cortex

| Program                  | Org                                                 | Approach                              | Status                                                                                                                                                                              |
|--------------------------|-----------------------------------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **CORTIVIS**             | **Eduardo Fernández, UMH Elche** + IMED, EU         | Penetrating Utah, 96–100 ch           | **Active first-in-human. Bernadeta Gómez (NEJM 2021). Sci Adv 2025 — real-time bidirectional implant in 2 volunteers.**                                                             |
| **Orion**                | **Cortigent** (ex–Second Sight, Valencia CA)        | Subdural surface, 60 ch               | EFS (NCT03344848). Mike Beauchamp (Baylor) — *drawing on cortex*: dynamic sequential stim for shape recognition (Cell 2020). Argus stack repurposed; needs ~mA → large phosphenes.* |
| **Neuralink Blindsight** | **Neuralink** (US)                                  | Penetrating threads (N1-style)        | **FDA Breakthrough Device designation, Sept 2024. First human trials planned 2026** (pending IDE). Initially low-resolution. Requires intact V1; targets patients without eyes + optic nerve. Musk has stated congenital-blind candidates. IEEE Spectrum notes likely-modest early acuity. |
| **ReVision Implant**     | **ReVision Implant** (Leuven, BE; KU Leuven spin-off) | Penetrating, ultra-thin-film flexible | **FDA Breakthrough Device, 2026.** Founded 2020 by Frederik Ceyssens (microelectronics) + Peter Janssen (neurophysiology). **€4M oversubscribed seed.** Short-term clinical trial during scheduled brain surgery planned **Q3–Q4 2026**; FIH in blind volunteers targeted summer 2027. Product name **Occular**. |
| NeuraViPeR (H2020)       | 7-org EU consortium                                 | Penetrating, flexible probes          | Concluded Feb 2025. Antonio's NIN work fed dynaphos here. SIGHTED is the LGN follow-on.                                                                                              |
| Utah Sci Adv (CORTIVIS)  | UMH Elche (Soto-Sánchez, Fernández)                 | Penetrating Utah                      | A blind volunteer **spontaneously regained partial natural vision** ~3 yr after stim; unrelated to the implant (Nov 2025 press).                                                     |

\* The "Argus to Orion" lineage is a tech-transfer story: epi-retinal hardware
on a different organ. Per Cesc, currents and electrode size are mismatched
for the cortex — the drawing-on-cortex trick is the workaround.

#### What's different across the V1 programs

| Axis                    | Orion              | CORTIVIS              | Neuralink Blindsight   | ReVision Occular        |
|-------------------------|--------------------|-----------------------|------------------------|-------------------------|
| Approach                | Surface            | Penetrating Utah      | Penetrating threads    | Penetrating thin-film   |
| Channel count           | 60                 | 96                    | thousands (claimed)    | high (thin-film array)  |
| Tissue damage profile   | Lowest (surface)   | Moderate (rigid)      | Low (flex threads)     | Lowest (thin-film)      |
| Phosphene size          | Large (mA)         | Small (µA)            | Small (µA)             | Small (µA)              |
| Clinical stage 2026-05  | EFS                | FIH                   | IDE pending → FIH 2026 | Acute peri-surgical Q4 26 |

Trend: every newcomer post-Orion bets on **penetrating, higher-density,
lower-current** stim, with electrode flexibility as the lever for chronic
viability.

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
- **Pixium IP → Science Corp** (Max Hodak, ex-Neuralink co-founder) in April 2024.
  Science also has a biohybrid BCI sensor (skull-mounted, sits on top of brain)
  — Murat Günel (Yale) leading first US human trials, planned 2027.
- **CORTIVIS is alive.** The "expired?" question in the chat — no, it's
  the active first-in-human European cortical program (Sci Adv 2025).
- **Second Sight → Cortigent.** Not Vivani. Cortigent took over Argus II
  support in 2023 and runs Orion.
- **Neuralink Blindsight is a V1 program, not a generic BCI.** Different
  from the N1 motor BCI in human trials now. Blindsight uses the same
  threads platform but with V1 as the target.
- **ReVision Implant Occular is the European answer to Blindsight.**
  Belgian, thin-film penetrating, FDA Breakthrough 2026, more clinical-near
  than Neuralink in some pathways (peri-surgical Q4 2026).

## Where this bootcamp lives

The deck is built around the **V1 cortical** column. Module pipeline
(M1–M5) mirrors a cortical prosthesis end-to-end: image processing →
gaze → safe stimulation → phosphene simulation → closed-loop decoding.
CORTIVIS (UMH) and NeuraViPeR/SIGHTED (Phosphoenix) are the partner
programs whose real device parameters inform M3 (Utah geometry, Ripple
ticks) and M4 (dynaphos forward model).

## Primary sources

### Retinal
- PRIMA NEJM 2025 — Palanker, Cusumano et al.: <https://www.nejm.org/doi/full/10.1056/NEJMoa2501396>
- PRIMA acquisition (April 2024) — Science Corp: <https://www.businesswire.com/news/home/20240425683676/en/>
- Science Corp Series C $230M (March 2026): <https://science.xyz/news/series-c/>
- Argus II history — Wikipedia: <https://en.wikipedia.org/wiki/Argus_retinal_prosthesis>
- Argus II long-term outcomes 2024: <https://pmc.ncbi.nlm.nih.gov/articles/PMC12496445/>
- Cortigent Argus II page: <https://www.cortigent.com/argus-ii>
- BVT 44-ch suprachoroidal — Allen 2025 (Clin & Exp Ophthalmol): <https://onlinelibrary.wiley.com/doi/10.1111/ceo.14502>
- GenSight GS030 Nature Med 2021 (Sahel et al.): <https://www.gensight-biologics.com/2021/05/25/>

### LGN
- SIGHTED — CORDIS: <https://cordis.europa.eu/project/id/101212687>

### V1 cortex
- Orion "drawing on cortex" — Beauchamp et al. *Cell* 2020: <https://www.sciencedirect.com/science/article/pii/S0092867420304967>
- Cortigent Orion page: <https://www.cortigent.com/orion>
- CORTIVIS NEJM 2021 — Fernández et al.: <https://www.nejm.org/doi/10.1056/NEJMc2034731>
- CORTIVIS Sci Adv 2025 — UMH press: <https://www.eurekalert.org/news-releases/1104900>
- CORTIVIS spontaneous recovery (Nov 2025): <https://www.eurekalert.org/news-releases/1114969>
- Neuralink Blindsight — Neuralink trials page: <https://neuralink.com/trials/visual-prosthesis/>
- Neuralink Blindsight IEEE Spectrum (acuity caveats): <https://spectrum.ieee.org/neuralink-blindsight>
- ReVision Implant — site: <https://www.revision-implant.com/>
- ReVision Implant €4M round: <https://techfundingnews.com/the-bionic-eye-revision-implant-lands-e4m-for-a-vision-device-that-feeds-directly-into-your-brain/>
- ReVision Implant FDA Breakthrough (March 2026): <https://eyewire.news/news/belgian-neurotech-startup-revision-implant-secures-fda-breakthrough-status-for-brain-implant-vision-technology>
- NeuraViPeR — CORDIS: <https://cordis.europa.eu/project/id/899287>
- Phosphoenix — <https://www.phosphoenix.nl/>
