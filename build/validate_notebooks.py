"""Validate notebook and HTML hygiene for the bootcamp repo.

Default checks are lightweight:
  python build/validate_notebooks.py

Heavy execution checks are explicit:
  python build/validate_notebooks.py --execute-solutions
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import urllib.parse
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
    MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop-solution.ipynb",
]

CORE_EXECUTION_NOTEBOOKS = [
    MODULES / "M1-computer-vision-notebooks" / "computer-vision-solution.ipynb",
    MODULES / "M3-neuromod-and-stim" / "neuromod-and-stim-solution.ipynb",
    MODULES / "M4-phosphene-simulation" / "phosphene-simulation-solution.ipynb",
    MODULES / "M5-decoding-and-closed-loop" / "decoding-and-closed-loop-solution.ipynb",
]


def load_nb(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def code_cells(nb: dict):
    for idx, cell in enumerate(nb.get("cells", []), start=1):
        if cell.get("cell_type") == "code":
            yield idx, cell


def strip_magics(src: str) -> str:
    clean = []
    for line in src.splitlines():
        s = line.lstrip()
        if s.startswith(("%", "!", "?")):
            clean.append("")
        else:
            clean.append(line)
    return "\n".join(clean) + "\n"


def check_ast(path: Path) -> list[str]:
    errors: list[str] = []
    nb = load_nb(path)
    for idx, cell in code_cells(nb):
        src = "".join(cell.get("source", []))
        try:
            ast.parse(strip_magics(src))
        except SyntaxError as exc:
            line = exc.lineno or 0
            errors.append(f"{path.relative_to(REPO)} cell {idx}: syntax error line {line}: {exc.msg}")
    return errors


def check_error_outputs(path: Path) -> list[str]:
    errors: list[str] = []
    nb = load_nb(path)
    for idx, cell in code_cells(nb):
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                ename = output.get("ename", "Error")
                evalue = output.get("evalue", "")
                errors.append(f"{path.relative_to(REPO)} cell {idx}: stored error output {ename}: {evalue}")
    return errors


def check_workshop_outputs(path: Path) -> list[str]:
    errors: list[str] = []
    nb = load_nb(path)
    for idx, cell in code_cells(nb):
        if cell.get("execution_count") is not None or cell.get("outputs"):
            errors.append(f"{path.relative_to(REPO)} cell {idx}: workshop notebook should not ship outputs")
    return errors


def check_solution_exists() -> list[str]:
    return [f"missing solution notebook: {p.relative_to(REPO)}" for p in SOLUTION_NOTEBOOKS if not p.exists()]


def check_local_html_links() -> list[str]:
    errors: list[str] = []
    html_paths = [REPO / "bootcamp-plan.html", *MODULES.glob("*.html")]
    attr_re = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.I)
    templated = re.compile(r"\$\{[^}]+\}")
    skip_prefixes = ("http:", "https:", "mailto:", "#", "data:", "javascript:")

    for path in html_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw in attr_re.findall(text):
            if raw.startswith(skip_prefixes) or templated.search(raw):
                continue
            local = raw.split("#", 1)[0].split("?", 1)[0]
            if not local:
                continue
            target = (path.parent / urllib.parse.unquote(local)).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(REPO)} -> missing local link {raw}")
    return errors


def execute_solution(path: Path, timeout: int) -> list[str]:
    try:
        import nbformat
        from nbclient import NotebookClient
    except Exception as exc:  # pragma: no cover - dependency guard
        return [f"cannot execute notebooks; install nbformat nbclient: {exc}"]

    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    except Exception as exc:
        return [f"{path.relative_to(REPO)} execution failed: {exc}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-solutions", action="store_true",
                        help="execute core solution notebooks with nbclient: M1, M3, M4, M5")
    parser.add_argument("--execute-all-solutions", action="store_true",
                        help="also execute the heavyweight M2 DeepGaze solution notebook")
    parser.add_argument("--timeout", type=int, default=900,
                        help="per-cell timeout for --execute-solutions")
    args = parser.parse_args()

    failures: list[str] = []
    notebooks = WORKSHOP_NOTEBOOKS + SOLUTION_NOTEBOOKS

    failures.extend(check_solution_exists())
    for path in notebooks:
        if not path.exists():
            continue
        failures.extend(check_ast(path))
        failures.extend(check_error_outputs(path))
    for path in WORKSHOP_NOTEBOOKS:
        if path.exists():
            failures.extend(check_workshop_outputs(path))
    failures.extend(check_local_html_links())

    if args.execute_solutions or args.execute_all_solutions:
        execution_targets = SOLUTION_NOTEBOOKS if args.execute_all_solutions else CORE_EXECUTION_NOTEBOOKS
        for path in execution_targets:
            if path.exists():
                failures.extend(execute_solution(path, args.timeout))

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(" -", failure)
        return 1

    print("VALIDATION PASSED")
    print(f"checked {len(notebooks)} notebooks and local HTML links")
    if not (args.execute_solutions or args.execute_all_solutions):
        print("solution execution skipped; add --execute-solutions for the heavy check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
