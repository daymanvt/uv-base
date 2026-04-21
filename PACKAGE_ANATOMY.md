# Anatomy of a Python Package

Every file that matters in a modern Python package, what it does, and whether you need it.

---

## Top-Level Directory

### `pyproject.toml` — **Required**

The single source of truth for your project. Replaces the old `setup.py`, `setup.cfg`,
`requirements.txt`, and most tool-specific config files.

```
[project]           → name, version, description, dependencies
[build-system]      → which backend builds your package (hatchling, setuptools, etc.)
[project.scripts]   → CLI entry points (installed as shell commands)
[dependency-groups]  → dev/test/lint dependency groups
[tool.*]            → configuration for ruff, mypy, pytest, yapf, etc.
```

### `README.md` — Expected

Package indexes (PyPI) and GitHub render this as your project's front page. Referenced by
`readme = "README.md"` in `pyproject.toml`.

### `LICENSE` — Expected

A plain text license file. Without one, your code is technically "all rights reserved."
Common choices: MIT, Apache-2.0, BSD-3-Clause.

### `.gitignore` — Expected

Keeps build artifacts, caches, and virtual environments out of version control. At minimum:

```
__pycache__/
*.pyc
.venv/
dist/
*.egg-info/
.mypy_cache/
.ruff_cache/
.pytest_cache/
```

### `uv.lock` — Auto-generated

Created by `uv lock` or `uv sync`. This is the lockfile that pins exact dependency versions
for reproducible installs. Commit it to version control. Never edit it by hand.

### `.python-version` — Optional

Created by `uv python pin 3.10`. A single line containing the Python version. Tools like
`uv` and `pyenv` read this to auto-select the right interpreter.

---

## The `src/` Layout

The recommended way to organize package code. Prevents accidental imports from the working
directory instead of the installed package.

```
src/
└── your_package/
    ├── __init__.py
    ├── __main__.py
    ├── py.typed
    ├── core.py
    └── cli.py
```

### `src/your_package/__init__.py` — **Required**

Marks the directory as a Python package. This is what runs when someone writes
`import your_package`. Use it to:

- Define `__version__` (the canonical version string)
- Define `__all__` (controls what `from your_package import *` exposes)
- Re-export key public names for convenience

```python
"""Your package description."""

from __future__ import annotations

__all__ = ["say_hello", "__version__"]
__version__ = "0.1.0"

from your_package.core import say_hello
```

**Why `__all__`?** Without it, `import *` grabs everything in the namespace. With it, you
explicitly control the public API. Linters also use it to detect unused imports.

**Why `__version__`?** It lets users check `your_package.__version__` at runtime. Some tools
(like `importlib.metadata`) can also read the version from package metadata, but having it
here is the established convention.

### `src/your_package/__main__.py` — Optional

Enables running the package as a script with `python -m your_package`. Without this file,
that command fails with "No module named your_package.__main__".

```python
"""Allow running with ``python -m your_package``."""

from your_package.cli import main

if __name__ == "__main__":
    main()
```

The `if __name__ == "__main__"` guard isn't strictly needed here (this file only runs as
`__main__`), but it's a universal convention that signals intent.

### `src/your_package/py.typed` — Optional

An empty marker file defined by [PEP 561](https://peps.python.org/pep-0561/). Tells type
checkers (mypy, pyright) that your package ships inline type hints. Without it, type checkers
may ignore your annotations when your package is used as a dependency by other projects.

### Other modules (`core.py`, `cli.py`, `models.py`, etc.)

Your actual code. There are no magic names here — organize however makes sense. Common
patterns:

| Module       | Typical contents                          |
|--------------|-------------------------------------------|
| `core.py`    | Primary business logic                    |
| `cli.py`     | Command-line interface (argparse / click) |
| `models.py`  | Data classes, Pydantic models, types      |
| `utils.py`   | Shared helper functions                   |
| `config.py`  | Settings, constants, environment loading  |
| `exceptions.py` | Custom exception classes               |

---

## The `tests/` Directory

### `tests/__init__.py` — Recommended

An empty file that makes the test directory a package. Some pytest configurations need this
to correctly resolve imports. It's zero-cost to include.

### `tests/test_*.py` — Convention

Pytest auto-discovers files matching `test_*.py` (or `*_test.py`). Each file contains
functions starting with `test_`:

```python
from your_package.core import say_hello

def test_say_hello():
    assert say_hello("Alice") == "Hello, Alice!"
```

### `tests/conftest.py` — Optional

Pytest's plugin file for shared fixtures. Any fixture defined here is automatically
available to all test files in the same directory (and subdirectories) without importing it.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "role": "admin"}
```

---

## Build & Distribution Files (auto-generated)

These are created when you build your package (`uv build` or `python -m build`). Never edit
them by hand, and typically add them to `.gitignore`.

### `dist/` — Build output

Contains `.whl` (wheel) and `.tar.gz` (sdist) files after running `uv build`. These are
what get uploaded to PyPI with `uv publish`.

### `*.egg-info/` — Metadata cache

Legacy metadata directory created by setuptools. Hatchling and other modern backends may
create similar metadata directories. Always gitignored.

---

## Optional Top-Level Files

### `CHANGELOG.md` / `HISTORY.md`

Human-readable list of changes per version. Not required, but expected for published
packages.

### `CONTRIBUTING.md`

Guidelines for contributors. GitHub renders this when someone opens a new PR.

### `Makefile` / `justfile`

Shortcut commands for common tasks. Not Python-specific, but common:

```makefile
lint:
    uv run ruff check .
    uv run mypy src/

test:
    uv run pytest -v
```

### `Dockerfile`

Container definition. Only relevant if you deploy with Docker.

### `.env` / `.env.example`

Environment variables. `.env` should be gitignored (it may contain secrets). `.env.example`
is committed as a template showing which variables are needed.

### `pylintrc`

Pylint configuration. Kept as a standalone file because pylint configs tend to be very long
(400+ lines for Google's style). Most other tools use `[tool.*]` sections in
`pyproject.toml` instead.

---

## Files You No Longer Need

These are legacy files replaced by `pyproject.toml`:

| Old file              | Replaced by                              |
|-----------------------|------------------------------------------|
| `setup.py`            | `[project]` + `[build-system]`           |
| `setup.cfg`           | `[project]` + `[tool.*]`                 |
| `requirements.txt`    | `[project.dependencies]`                 |
| `requirements-dev.txt`| `[dependency-groups]`                    |
| `MANIFEST.in`         | Build backend auto-includes (hatchling)  |
| `.flake8`             | `[tool.ruff]` (ruff replaces flake8)     |
| `mypy.ini`            | `[tool.mypy]`                            |
| `pytest.ini`          | `[tool.pytest.ini_options]`              |
| `.isort.cfg`          | `[tool.ruff.lint.isort]`                 |
| `tox.ini`             | `uv run` + dependency groups             |

---

## Minimal vs. Complete

**Bare minimum** for an installable package:

```
mypackage/
├── pyproject.toml
└── src/
    └── mypackage/
        └── __init__.py
```

**Complete real-world** package:

```
mypackage/
├── pyproject.toml
├── README.md
├── LICENSE
├── pylintrc
├── .gitignore
├── .python-version
├── uv.lock
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── __main__.py
│       ├── py.typed
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_core.py
└── scripts/
    └── example.py
```
