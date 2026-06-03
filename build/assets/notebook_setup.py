"""Install notebook dependencies, preferring uv over pip when available.

The bootcamp's notebooks were originally written for Colab or a local Anaconda
base: detect Colab, add `--user` everywhere else. That assumption breaks in
uv-created venvs because (a) `uv venv` ships without pip so `python -m pip`
fails outright, and (b) `--user` is refused inside any venv.

Path picked at runtime, best → worst:

  1. uv on PATH + kernel runs from `<project>/.venv` (project = nearest
     ancestor with `pyproject.toml`):
        `uv sync --project <project>` — declarative, pins from the lockfile,
        ignores the per-notebook pkg list (the project already declares deps).
  2. uv on PATH, anywhere else (bare venv, kernel outside project venv):
        `uv pip install --python <sys.executable> -q <pkgs>` — imperative,
        works in any venv with or without pip, doesn't touch pyproject.
  3. No uv (Colab, vanilla Anaconda base):
        `python -m pip install -q <pkgs> [--user]` — the original path,
        unchanged. `--user` only outside Colab.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def ensure(pkgs):
    if shutil.which('uv'):
        project = _find_uv_project()
        if project and _kernel_in_project_venv(project):
            cmd = ['uv', 'sync', '--project', str(project), '--quiet']
            subprocess.run(cmd, check=True)
            label = f'uv sync ({project.name})'
        else:
            cmd = ['uv', 'pip', 'install', '--python', sys.executable, '-q', *pkgs]
            subprocess.run(cmd, check=True)
            label = 'uv pip'
    else:
        in_colab = 'google.colab' in sys.modules
        cmd = [sys.executable, '-m', 'pip', 'install', '-q', *pkgs]
        if not in_colab:
            cmd.append('--user')
        subprocess.run(cmd, check=True)
        label = 'Colab' if in_colab else 'local, --user'
    print(f'install OK ({label})')


def _find_uv_project():
    p = Path.cwd().resolve()
    for parent in [p, *p.parents]:
        if (parent / 'pyproject.toml').exists():
            return parent
    return None


def _kernel_in_project_venv(project):
    try:
        return Path(sys.prefix).resolve() == (project / '.venv').resolve()
    except OSError:
        return False
