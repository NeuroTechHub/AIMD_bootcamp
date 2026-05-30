"""Shared loud-fallback banner for notebooks.

Several notebooks (M1's YOLO cache, M4's YOLO/MiDaS/saliency chain) silently
swap real models for cached or heuristic stand-ins when the real model
fails to download. The original "silent fallback" was a UX win at the cost
of a pedagogical disaster: students walked away thinking they ran the
real network when they ran a brightness threshold.

The helper here gives every such fallback the same loud banner so the
student can never mistake one for the other. Use it like::

    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path("../../build/assets").resolve()))
    from fallback_banner import loud_fallback

    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")  # downloads on first run
        ...
    except Exception as exc:
        loud_fallback(
            real="YOLO v8n object detection",
            stand_in="brightness threshold mask",
            reason=str(exc),
            losing="per-class object identity, mask quality on cluttered scenes",
        )
        ...  # build the stand-in here

The banner deliberately uses plain ASCII '=' so it survives every locale
and stdout encoding (Colab, VS Code, classic Jupyter, Windows cp1252) —
no Unicode box-drawing or colour codes. Loud in every frontend including
a printed PDF export.
"""
from __future__ import annotations


_BANNER = "=" * 68


def loud_fallback(
    *,
    real: str,
    stand_in: str,
    reason: str = "",
    losing: str = "",
) -> None:
    """Print a high-contrast banner announcing a model fallback.

    Args:
        real: human-readable name of the model that failed.
        stand_in: what's being substituted (be specific: not "heuristic",
            but "brightness threshold mask").
        reason: short failure description; the exception message is fine.
        losing: one-sentence description of what the student loses by
            running the stand-in instead of the real thing.
    """
    print()
    print(_BANNER)
    print(f"  [FALLBACK] {real}  ->  {stand_in}")
    if reason:
        # Truncate long stack-trace-style strings so the banner stays scannable.
        short = reason.strip().splitlines()[0][:120]
        print(f"  reason: {short}")
    if losing:
        print(f"  what you're losing: {losing}")
    print(_BANNER)
    print()


__all__ = ["loud_fallback"]
