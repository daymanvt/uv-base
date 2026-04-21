# Samples

Runnable demo scripts for every library in this template. Each file is heavily
commented — read the source, run it, and copy what you need into your project.

## Running

Make sure your venv is activated and the `libs` group is installed:

```shell
source .venv/bin/activate
uv sync --group libs
```

Then run any demo:

```shell
python samples/demo_icecream.py
python samples/demo_rich.py
python samples/demo_textual.py       # interactive TUI — press 'q' to quit
python samples/demo_click.py --help  # CLI — try the subcommands
python samples/demo_tqdm.py
```

## Library Overview

### icecream (`demo_icecream.py`)

A drop-in replacement for `print()` during debugging. Instead of writing
`print(f"x = {x}")`, you write `ic(x)` and it prints both the expression and
its value automatically. Supports expressions, data structures, no-arg calls
for tracing, global enable/disable, and custom output formatting.

### rich (`demo_rich.py`)

A comprehensive library for beautiful terminal output. Provides styled text
with markup syntax, auto-formatted data structures, tables, panels, trees,
columns, syntax highlighting, markdown rendering, progress bars, status
spinners, object inspection, and terminal layouts. Acts as a drop-in
replacement for `print()` via `from rich import print`.

### textual (`demo_textual.py`)

A framework for building full terminal user interfaces (TUIs). Uses a CSS-like
styling system for layout and appearance, a widget library (buttons, inputs,
data tables, labels), reactive attributes for automatic UI updates, event
handling, and key bindings. Applications run entirely in the terminal with
mouse support.

### click (`demo_click.py`)

A library for building composable command-line interfaces using decorators.
Supports options (`--name`), flags (`--verbose`), positional arguments, type
validation, choice constraints, nested command groups, confirmation prompts,
colored output, and automatic `--help` generation. An alternative to stdlib
`argparse` with a more declarative API.

### tqdm (`demo_tqdm.py`)

Fast, extensible progress bars for any iterable. Wrap a loop with `tqdm()` and
get an automatic progress bar with ETA, speed, and percentage. Supports custom
units, manual updates for non-iterable operations, nested bars, dynamic
descriptions, colored output, and safe printing via `tqdm.write()`. Available
as a runtime dependency (no `--group` flag needed).

## Tool Validation

### lint_sample.py

A file with intentional code quality and formatting issues. Run each tool
against it to verify your development environment is working:

```shell
ruff check samples/lint_sample.py       # unused imports, naming, old typing
mypy samples/lint_sample.py             # type errors, missing annotations
pylint samples/lint_sample.py           # docstrings, too many args
yapf --diff samples/lint_sample.py      # formatting: spacing, line length
```
