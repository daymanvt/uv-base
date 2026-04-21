# uv-base

A template for bootstrapping Python projects with [uv](https://docs.astral.sh/uv/).

---

## Quick Setup

### 1. One-time setup: Install global tools

These linting/formatting tools are installed once and available across all projects. Each
gets its own isolated environment under `~/.local/share/uv/tools/` — they never pollute
your system Python or project venvs.

```shell
uv tool install ruff
uv tool install pylint
uv tool install yapf
```

They still read `pyproject.toml` and `pylintrc` from whichever directory you run them in,
so per-project config works automatically.

**Why not mypy and pytest?** These tools need access to your project's installed
dependencies to resolve imports and run tests. They belong in the project's dependency
groups instead (see [Dependency Groups](#dependency-groups)).

### 2. Add shell functions to `~/.zshrc` from `uvlint.sh` and `uvinit.sh`, then reload your shell


### 3. Create a new project

```shell
mkdir my-project && cd my-project

uvinit            # Simple: main.py + pyproject.toml + pylintrc
uvinit --full     # Full:   src/my_project/ package + tests/ + config
```

After either command, activate the virtualenv:

```shell
source .venv/bin/activate
```

### 4. Update CHANGEME fields

The generated `pyproject.toml` has placeholder values marked with `CHANGEME` that you
should update immediately:

| Field         | Location          | What to change                   |
|---------------|-------------------|----------------------------------|
| `description` | `[project]`       | One-line summary of your project |
| `authors`     | `[project]`       | Your name and email              |

The `name` and `known-first-party` fields are automatically set by `uvinit` based on the
directory name. In `--full` mode, `[project.scripts]` entry points are also set.

`uvinit` uses two separate templates (`pyproject.toml.full` and `pyproject.toml.simple`)
so the simple variant never includes `[build-system]` or `[project.scripts]`.

### 5. Changing Python version

The template defaults to Python 3.10. To use a different version, update these three places
in `pyproject.toml` and then re-sync:

1. `requires-python = ">=3.10"` — in `[project]`
2. `target-version = "py310"` — in `[tool.ruff]`
3. `python_version = "3.10"` — in `[tool.mypy]`

Then run:

```shell
uv python pin 3.13    # or whatever version you want
uv sync
```

---

## Project Structure

After `uvinit`, you always get:

```
my-project/
├── pyproject.toml            # Project config + all tool settings
├── pylintrc                  # Pylint config (Google style, kept separate due to size)
├── README.md                 # Auto-generated with project name
├── main.py                   # Entry point (simple mode only)
└── samples/
    ├── README.md             # Overview of all sample scripts
    ├── lint_sample.py        # Intentionally broken file for tool validation
    ├── demo_icecream.py      # icecream debugging demo
    ├── demo_rich.py          # rich terminal output demo
    ├── demo_textual.py       # textual TUI demo
    ├── demo_click.py         # click CLI demo
    └── demo_tqdm.py          # tqdm progress bar demo
```

After `uvinit --full`, you get the above plus:

```
my-project/
├── ...                       # (same base files, minus main.py)
├── src/
│   └── my_project/
│       ├── __init__.py       # Package root — __all__, __version__
│       ├── __main__.py       # Enables: python -m my_project
│       ├── py.typed          # PEP 561 marker for type hint consumers
│       ├── core.py           # Core business logic
│       ├── cli_argparse.py   # CLI using argparse (stdlib, no extra deps)
│       └── cli_click.py      # CLI using click (delete whichever you don't need)
├── tests/
│   ├── __init__.py
│   └── test_core.py
└── scripts/
    └── example.py            # Standalone script (tqdm demo)
```

> **Tip:** Delete `cli_click.py` or `cli_argparse.py` depending on which CLI framework
> you prefer for your project. Update the `[project.scripts]` entry point in
> `pyproject.toml` accordingly.

---

## Dependency Groups

```shell
uv sync                                        # runtime deps only (tqdm)
uv sync --group libs                           # + icecream, rich, click, textual
uv sync --group test                           # + pytest, pytest-mock, mypy
uv sync --group libs --group test              # everything
```

| Group  | Packages                           | Purpose                        |
|--------|------------------------------------|--------------------------------|
| `libs` | icecream, rich, click, textual     | Libraries you import in code   |
| `test` | pytest, pytest-mock, mypy          | Testing + type checking        |

Linting/formatting tools (ruff, pylint, yapf) are installed globally via
`uv tool install` and are available in every project without adding them as dependencies.

---

## Tool Usage

All commands below assume your venv is activated (`source .venv/bin/activate`) and global
tools are installed (see [One-time setup](#1-one-time-setup-install-global-tools)).

### Recommended workflow

Run everything in order with a single command:

```shell
uvlint                    # defaults to src/
uvlint scripts/           # specific directory
uvlint file.py            # single file
```

The order is: **format** (yapf) -> **lint + auto-fix** (ruff) -> **deep lint** (pylint) ->
**type check** (mypy). Format first so linters don't flag style issues, fast lint next
to clean up trivials, deep lint for design feedback, type check last since it's slowest.

### Or run tools individually

#### yapf — Code formatter (Google style)

```shell
yapf --diff file.py              # preview formatting changes
yapf -i file.py                  # format in-place
yapf -i -r src/                  # format entire directory
```

#### ruff — Fast linter and formatter

```shell
ruff check file.py               # lint a single file
ruff check --fix .               # lint + auto-fix everything
ruff format .                    # format all files (black-compatible style)
ruff format --check .            # check formatting without changing
```

> **Note:** `ruff format` and `yapf` are both formatters with different styles. Pick one
> per project. This template uses yapf (Google style) by default.

#### pylint — Comprehensive linter

```shell
pylint file.py                   # lint a single file
pylint src/my_package/           # lint the whole package
```

#### mypy — Static type checker

```shell
mypy file.py                     # check a single file
mypy src/                        # check the whole package
```

#### pytest — Testing framework

```shell
pytest                           # run all tests
pytest -v                        # verbose output
pytest tests/test_core.py        # specific file
pytest -k "test_say_hello"       # filter by name
```

### Validating tools with the sample file

The `samples/lint_sample.py` file (copied to every new project by `uvinit`) contains
intentional issues. Use it to confirm each tool is working:

```shell
ruff check samples/lint_sample.py       # unused imports, naming, old typing
mypy samples/lint_sample.py             # type errors, missing annotations
pylint samples/lint_sample.py           # docstrings, too many args, unused imports
yapf --diff samples/lint_sample.py      # formatting: spacing, line length
```

See `samples/README.md` for runnable demos of every library in the `libs` group.

---

## Quick Reference

```shell
# --- Project setup ---
uvinit                             # simple project (main.py)
uvinit --full                      # full package (src/ layout)
source .venv/bin/activate          # activate the virtualenv
uvlint                             # format + lint + type-check src/
uvlint file.py                     # same, on a single file

# --- Dependency management ---
uv sync                            # install/update dependencies
uv sync --group libs --group test  # install all groups
uv add <package>                   # add a runtime dependency
uv add --group test <package>      # add to a specific group
uv remove <package>                # remove a dependency
uv lock --upgrade                  # upgrade all locked versions
uv tree                            # show dependency tree

# --- Global tool management ---
uv tool install <tool>             # install a tool globally
uv tool list                       # see installed tools
uv tool upgrade --all              # upgrade all global tools
uv tool upgrade <tool>             # upgrade a specific tool
uv tool uninstall <tool>           # remove a tool
uv tool update-shell               # ensure ~/.local/bin is on PATH

# --- Running code ---
python script.py                   # run a script (venv activated)
python -m my_package               # run package as module
demo-cli greet                     # run a CLI entry point

# --- Python versions ---
uv python list                     # available versions
uv python pin 3.13                 # pin project to a version
uv python install 3.12             # install a specific version
```
