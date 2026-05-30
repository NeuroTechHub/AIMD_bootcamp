"""Validate notebook and HTML hygiene for the bootcamp repo.

Default checks are lightweight:
  python build/validate_notebooks.py

Heavy execution checks are explicit:
  python build/validate_notebooks.py --execute-solutions

Two failure modes:
  - **failures** (always block exit code 1): syntax errors, stored error
    outputs, workshop-output bleed-through, missing solution twins, broken
    local HTML links.
  - **warnings** (don't block by default; use --strict to elevate to failures):
    unexplained magic-number literals, workshop↔solution cell-count drift,
    orphan cell-metadata keys nobody reads, forward-reference of names not
    yet defined in earlier cells.

The warnings exist to surface drift introduced as code evolves; they're soft
on purpose so deferred modules don't gate CI on a one-pass cleanup.
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

# Each workshop ↔ solution pair, for parity checks. Order matches the lists above.
NOTEBOOK_PAIRS = list(zip(WORKSHOP_NOTEBOOKS, SOLUTION_NOTEBOOKS))

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


# ---------------------------------------------------------------------------
# Warning-level checks (don't fail unless --strict)
# ---------------------------------------------------------------------------

# Numeric literals we always allow without explanation. Powers of two and ten
# under 1024, single-digit values, common axis ranges/colour stops.
_LITERAL_ALLOWLIST: set[float] = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 32, 64, 100, 128, 200, 255, 256,
    360, 500, 512, 1000, 1024,
    0.0, 0.1, 0.2, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0,
    1e-3, 1e-6, 1e3, 1e6,
}


def _justified_by_context(src_lines: list[str], lineno: int) -> bool:
    """A literal is justified if its line carries a comment, is an assignment
    to a named constant (UPPER_SNAKE), is inside a docstring, or sits on a
    line containing `citation`/`see`/`from `<year>` (the M3-style provenance
    convention). Conservative: when in doubt, treat as justified."""
    if lineno <= 0 or lineno > len(src_lines):
        return True
    line = src_lines[lineno - 1]
    # comment anywhere on the line
    if "#" in line:
        return True
    # constant assignment: NAME = ... (NAME in upper-snake)
    m = re.match(r"\s*([A-Z][A-Z0-9_]+)\s*=", line)
    if m:
        return True
    # citation phrases (Shannon 1992, Cogan 2016, etc.)
    if re.search(r"\b(19|20)\d{2}\b", line):
        return True
    return False


def check_magic_numbers(path: Path) -> list[str]:
    """Warn about unexplained numeric literals (> 1 digit, not in allowlist,
    no contextual justification on the same line)."""
    warnings: list[str] = []
    nb = load_nb(path)
    for idx, cell in code_cells(nb):
        src = "".join(cell.get("source", []))
        try:
            tree = ast.parse(strip_magics(src))
        except SyntaxError:
            continue  # check_ast already reports this
        src_lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant):
                continue
            v = node.value
            if not isinstance(v, (int, float)):
                continue
            if isinstance(v, bool):  # bool is subclass of int
                continue
            if v in _LITERAL_ALLOWLIST:
                continue
            if isinstance(v, int) and abs(v) < 10:
                continue
            if _justified_by_context(src_lines, getattr(node, "lineno", 0)):
                continue
            warnings.append(
                f"{path.relative_to(REPO)} cell {idx} line {node.lineno}: "
                f"unexplained magic number {v!r} — add a comment or promote "
                f"to a named constant"
            )
    return warnings


def _cell_kinds(nb: dict) -> list[str]:
    return [c.get("cell_type", "?") for c in nb.get("cells", [])]


def check_workshop_solution_parity(workshop: Path, solution: Path) -> list[str]:
    """Warn if workshop and solution have a different number of cells, or if
    the cell-type sequence diverges (markdown vs code in different positions)."""
    if not (workshop.exists() and solution.exists()):
        return []
    w_kinds = _cell_kinds(load_nb(workshop))
    s_kinds = _cell_kinds(load_nb(solution))
    warnings: list[str] = []
    if len(w_kinds) != len(s_kinds):
        warnings.append(
            f"{workshop.relative_to(REPO)} has {len(w_kinds)} cells; "
            f"{solution.relative_to(REPO)} has {len(s_kinds)} — drift"
        )
        return warnings
    for i, (w, s) in enumerate(zip(w_kinds, s_kinds), start=1):
        if w != s:
            warnings.append(
                f"{workshop.relative_to(REPO)} cell {i} is {w}, "
                f"matching solution cell is {s} — drift"
            )
    return warnings


# Cell-metadata keys considered standard / consumed by Jupyter or Colab.
_KNOWN_METADATA_KEYS = {
    "id", "tags", "collapsed", "scrolled", "jupyter", "trusted",
    "vscode", "colab", "deletable", "editable", "name",
    "execution", "papermill", "executionInfo", "outputId",
    "slideshow",
}


def check_orphan_metadata(path: Path) -> list[str]:
    """Warn on cell metadata keys that aren't in the standard set — they're
    likely written by some builder but read by no consumer (e.g. M4's
    `exercise_hint` was orphaned this way)."""
    warnings: list[str] = []
    nb = load_nb(path)
    for idx, cell in enumerate(nb.get("cells", []), start=1):
        meta = cell.get("metadata", {})
        for key in meta:
            if key not in _KNOWN_METADATA_KEYS:
                warnings.append(
                    f"{path.relative_to(REPO)} cell {idx}: orphan metadata "
                    f"key {key!r} — no known consumer"
                )
    return warnings


_PY_BUILTINS = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
# Manual fallback so this works whether __builtins__ is a module or a dict.
_PY_BUILTINS |= {
    "print", "len", "range", "list", "dict", "set", "tuple", "str", "int", "float",
    "bool", "bytes", "None", "True", "False", "type", "isinstance", "issubclass",
    "open", "enumerate", "zip", "map", "filter", "sorted", "reversed", "sum",
    "min", "max", "abs", "round", "any", "all", "next", "iter", "object",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError", "RuntimeError",
    "StopIteration", "AttributeError", "FileNotFoundError", "ImportError",
    "NotImplementedError", "__name__", "__file__", "__doc__", "globals", "locals",
    "hasattr", "getattr", "setattr", "delattr", "vars", "dir", "id", "hash",
    "callable", "repr", "ord", "chr", "hex", "bin", "oct", "format", "input",
    "frozenset", "complex", "slice", "property", "classmethod", "staticmethod",
    "super", "exec", "eval", "compile", "memoryview", "bytearray",
    "self", "cls", "_", "__init__", "__main__", "__class__",
}


class _NameCollector(ast.NodeVisitor):
    """Collect names *defined* and names *loaded* at MODULE scope only.

    Function and class bodies are skipped entirely — Python lazy-resolves
    names inside function bodies at call time, not at definition time, so a
    function defined in cell 2 can legally reference a helper defined later
    in cell 5. The forward-reference linter only catches module-level loads,
    which would actually fail at import/eval time."""

    def __init__(self) -> None:
        self.defined: set[str] = set()
        self.loaded: list[tuple[str, int]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.defined.add(node.name)
        # Look at default-arg expressions (evaluated at def-time) but skip body.
        for default in node.args.defaults + node.args.kw_defaults:
            if default is not None:
                self.visit(default)
        # Decorators are evaluated at def-time too.
        for deco in node.decorator_list:
            self.visit(deco)

    visit_AsyncFunctionDef = visit_FunctionDef  # type: ignore[assignment]

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.defined.add(node.name)
        for base in node.bases:
            self.visit(base)
        for deco in node.decorator_list:
            self.visit(deco)
        # Class body is not visited — methods are functions, attribute
        # assignments would also reference names that resolve at instantiation.

    def visit_Lambda(self, node: ast.Lambda) -> None:
        # Same lazy-binding logic: don't descend into the body.
        for default in node.args.defaults + node.args.kw_defaults:
            if default is not None:
                self.visit(default)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comp(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comp(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comp(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comp(node)

    def _visit_comp(self, node: ast.AST) -> None:
        # Only the iterable of the FIRST generator is evaluated in the
        # enclosing scope; everything else uses comprehension-local names.
        gens = getattr(node, "generators", [])
        if gens:
            self.visit(gens[0].iter)
        # Don't descend further — comp-local names are out of scope.

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self._collect_target(target)
        # Visit the value to pick up loaded names on the RHS.
        self.visit(node.value)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._collect_target(node.target)
        self.visit(node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.target and isinstance(node.target, ast.Name):
            self.defined.add(node.target.id)
        if node.value is not None:
            self.visit(node.value)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]
            self.defined.add(name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            if name == "*":
                self.defined.add("*")
            else:
                self.defined.add(name)

    def visit_For(self, node: ast.For) -> None:
        self._collect_target(node.target)
        self.visit(node.iter)
        for stmt in node.body + node.orelse:
            self.visit(stmt)

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            self.visit(item.context_expr)
            if item.optional_vars is not None:
                self._collect_target(item.optional_vars)
        for stmt in node.body:
            self.visit(stmt)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self.loaded.append((node.id, node.lineno))

    def visit_Global(self, node: ast.Global) -> None:
        for name in node.names:
            self.defined.add(name)

    def _collect_target(self, target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            self.defined.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self._collect_target(elt)
        elif isinstance(target, ast.Starred):
            self._collect_target(target.value)


def check_forward_references(path: Path) -> list[str]:
    """Warn if a code cell loads a name not defined in any earlier cell of the
    same notebook. Catches the M4-Exercise-1.2-style bug where a hint or
    example references a helper that lives further down the notebook.

    Conservative — skips notebooks containing `from X import *` and skips
    names that shadow Python builtins."""
    warnings: list[str] = []
    nb = load_nb(path)
    cumulative_defined: set[str] = set()
    had_star_import = False
    for idx, cell in code_cells(nb):
        src = "".join(cell.get("source", []))
        try:
            tree = ast.parse(strip_magics(src))
        except SyntaxError:
            continue
        collector = _NameCollector()
        collector.visit(tree)
        if "*" in collector.defined:
            had_star_import = True
        if had_star_import:
            cumulative_defined |= collector.defined - {"*"}
            continue
        for name, lineno in collector.loaded:
            if name in cumulative_defined:
                continue
            if name in _PY_BUILTINS:
                continue
            if name in collector.defined:
                continue  # defined later in the same cell
            warnings.append(
                f"{path.relative_to(REPO)} cell {idx} line {lineno}: "
                f"forward reference to {name!r} — not defined in any "
                f"earlier cell"
            )
        cumulative_defined |= collector.defined - {"*"}
    return warnings


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


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
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings (magic numbers, parity drift, "
                             "orphan metadata, forward references) as failures")
    parser.add_argument("--no-warnings", action="store_true",
                        help="suppress the warning-level checks entirely")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
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

    if not args.no_warnings:
        for path in notebooks:
            if not path.exists():
                continue
            warnings.extend(check_magic_numbers(path))
            warnings.extend(check_orphan_metadata(path))
            warnings.extend(check_forward_references(path))
        for w_path, s_path in NOTEBOOK_PAIRS:
            warnings.extend(check_workshop_solution_parity(w_path, s_path))

    if args.execute_solutions or args.execute_all_solutions:
        execution_targets = SOLUTION_NOTEBOOKS if args.execute_all_solutions else CORE_EXECUTION_NOTEBOOKS
        for path in execution_targets:
            if path.exists():
                failures.extend(execute_solution(path, args.timeout))

    if args.strict:
        failures.extend(warnings)
        warnings = []

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(" -", failure)
        if warnings:
            print(f"\n{len(warnings)} warning(s) (not failing):")
            for w in warnings:
                print(" ~", w)
        return 1

    print("VALIDATION PASSED")
    print(f"checked {len(notebooks)} notebooks and local HTML links")
    if warnings:
        print(f"\n{len(warnings)} warning(s) (use --strict to elevate, "
              f"--no-warnings to suppress):")
        for w in warnings:
            print(" ~", w)
    if not (args.execute_solutions or args.execute_all_solutions):
        print("\nsolution execution skipped; add --execute-solutions for the heavy check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
