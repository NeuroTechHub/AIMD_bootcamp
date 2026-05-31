"""Capture per-module QR codes and HTML screenshots for the talk deck.

Output:
  build/assets/qrs/M{N}.png            — 600x600 QR codes
  build/assets/module_shots/M{N}.png   — 1600x900 viewport screenshots

Re-run anytime: `python build/_capture_module_assets.py`
(requires: `pip install qrcode[pil] playwright && playwright install chromium`)
"""

from __future__ import annotations

from pathlib import Path

import qrcode
from playwright.sync_api import sync_playwright


REPO = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO / "modules"
QRS_DIR = REPO / "build" / "assets" / "qrs"
SHOTS_DIR = REPO / "build" / "assets" / "module_shots"

BASE_URL = "https://neurotechhub.github.io/AIMD_bootcamp/modules"

MODULES = [
    ("M1", "M1-computer-vision.html"),
    ("M2", "M2-deepgaze-and-gaze.html"),
    ("M3", "M3-neuromod-and-stim.html"),
    ("M4", "M4-phosphene-simulation.html"),
    ("M5", "M5-decoding-and-closed-loop.html"),
]

# Per-module scroll offset (px from top) for the screenshot. Tuned to land
# on the most visually distinct interactive panel rather than the page header.
SCROLL = {
    "M1": 1750,  # operator picker + image canvas
    "M2": 1900,  # scanpath / heatmap demo with stat histograms
    "M3": 1100,  # past TOC into the pulse explorer
    "M4": 900,   # single-phosphene basis explorer
    "M5": 900,   # closed-loop diagram / live readout
}


def make_qrs() -> None:
    QRS_DIR.mkdir(parents=True, exist_ok=True)
    for code, html in MODULES:
        url = f"{BASE_URL}/{html}"
        img = qrcode.make(url, box_size=10, border=2)
        out = QRS_DIR / f"{code}.png"
        img.save(out)
        print(f"  QR  {code:3} -> {out.name}  ({url})")


def make_shots() -> None:
    SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900})
        page = ctx.new_page()
        for code, html in MODULES:
            local = (MODULES_DIR / html).resolve().as_uri()
            page.goto(local, wait_until="networkidle", timeout=30_000)
            # Give in-browser scripts (TF.js model load, canvas paint) a beat.
            page.wait_for_timeout(1500)
            page.evaluate(f"window.scrollTo(0, {SCROLL[code]})")
            page.wait_for_timeout(500)
            out = SHOTS_DIR / f"{code}.png"
            page.screenshot(path=str(out), full_page=False)
            print(f"  shot {code:3} -> {out.name}")
        browser.close()


if __name__ == "__main__":
    make_qrs()
    make_shots()
