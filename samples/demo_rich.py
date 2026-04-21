"""Rich demo — beautiful terminal output for Python.

Run:  python samples/demo_rich.py

Rich turns your terminal into a canvas with styled text, tables, trees,
progress bars, syntax highlighting, markdown rendering, and more. It's a
drop-in replacement for print() that makes everything look better.

Install:  uv sync --group libs
"""

import time

from rich import print as rprint
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, track
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

console = Console()


# =============================================================================
# STYLED TEXT — colors, bold, italic, and markup syntax
# =============================================================================

console.print(Rule("[bold cyan]Styled Text"))

# Rich uses a BBCode-like markup syntax for inline styling
rprint("[bold red]Error:[/bold red] Something went wrong")
rprint("[green]Success![/green] All checks passed")
rprint("[bold yellow]Warning:[/] Disk space low")
rprint("[italic magenta]Note:[/] This is informational")
rprint("[underline]Underlined[/] and [strikethrough]struck through[/]")

# You can nest styles
rprint("[bold][blue]Bold blue[/blue] and [red]bold red[/red][/bold]")

# Links (terminal must support them)
rprint("[link=https://docs.python.org]Python Docs[/link]")

# The Text object gives fine-grained control
text = Text("Hello, World!")
text.stylize("bold", 0, 5)            # "Hello" is bold
text.stylize("red", 7, 12)            # "World" is red
console.print(text)
print()


# =============================================================================
# PRETTY-PRINTING DATA STRUCTURES
# =============================================================================

console.print(Rule("[bold cyan]Pretty Printing"))

# rprint() auto-formats dicts, lists, sets, tuples with colors and indentation
rprint({
    "name": "Alice",
    "age": 30,
    "active": True,
    "roles": ["admin", "user"],
    "metadata": {"last_login": "2025-01-15", "logins": 142},
})

# console.log() adds a timestamp — great for event tracing
console.log("Application started")
console.log("User logged in", log_locals=False)
print()


# =============================================================================
# TABLES — structured data with alignment, borders, and colors
# =============================================================================

console.print(Rule("[bold cyan]Tables"))

table = Table(title="Server Status", show_lines=True)
table.add_column("Host", style="cyan", no_wrap=True)
table.add_column("Status", justify="center")
table.add_column("CPU %", justify="right", style="green")
table.add_column("Memory", justify="right")

table.add_row("web-01", "[green]● UP[/]", "23.4", "4.2 GB")
table.add_row("web-02", "[green]● UP[/]", "67.8", "7.1 GB")
table.add_row("db-01", "[red]● DOWN[/]", "—", "—")
table.add_row("cache-01", "[yellow]● WARN[/]", "91.2", "15.8 GB")

console.print(table)
print()


# =============================================================================
# PANELS — boxed content with titles and borders
# =============================================================================

console.print(Rule("[bold cyan]Panels"))

console.print(Panel(
    "Panels wrap content in a box with an optional title and subtitle.\n"
    "They're useful for drawing attention to important information.",
    title="What are Panels?",
    subtitle="rich.panel.Panel",
    border_style="green",
    padding=(1, 2),
))
print()


# =============================================================================
# TREES — hierarchical data like file systems or org charts
# =============================================================================

console.print(Rule("[bold cyan]Trees"))

tree = Tree("[bold]my-project/", guide_style="bold bright_blue")

src = tree.add("[blue]src/[/]")
pkg = src.add("[blue]my_package/[/]")
pkg.add("[green]__init__.py[/]")
pkg.add("[green]core.py[/]")
pkg.add("[green]cli.py[/]")

tests = tree.add("[blue]tests/[/]")
tests.add("[green]test_core.py[/]")

tree.add("[yellow]pyproject.toml[/]")
tree.add("[yellow]README.md[/]")

console.print(tree)
print()


# =============================================================================
# COLUMNS — render items in auto-sized columns
# =============================================================================

console.print(Rule("[bold cyan]Columns"))

items = [f"[cyan]item-{i:02d}[/]" for i in range(20)]
console.print(Columns(items, equal=True, expand=True))
print()


# =============================================================================
# SYNTAX HIGHLIGHTING — display code with colors
# =============================================================================

console.print(Rule("[bold cyan]Syntax Highlighting"))

code = '''\
def fibonacci(n: int) -> list[int]:
    """Return the first n Fibonacci numbers."""
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq[:n]
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
print()


# =============================================================================
# MARKDOWN — render markdown in the terminal
# =============================================================================

console.print(Rule("[bold cyan]Markdown"))

md = Markdown("""\
# Rich Markdown

Rich can render **Markdown** directly in your terminal:

- Bullet lists
- *Italic* and **bold** text
- `inline code`

> Blockquotes work too!

```python
print("Even code blocks!")
```
""")
console.print(md)


# =============================================================================
# PROGRESS BARS — track() for simple loops, Progress for complex ones
# =============================================================================

console.print(Rule("[bold cyan]Progress Bars"))

# Simple: wrap any iterable with track()
for _ in track(range(30), description="[green]Downloading..."):
    time.sleep(0.02)

# Advanced: multiple tasks with a Progress context manager
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
) as progress:
    task1 = progress.add_task("[red]Compiling...", total=50)
    task2 = progress.add_task("[cyan]Linking...", total=50)

    while not progress.finished:
        progress.update(task1, advance=1)
        progress.update(task2, advance=0.7)
        time.sleep(0.02)

print()


# =============================================================================
# STATUS SPINNER — for indeterminate operations
# =============================================================================

console.print(Rule("[bold cyan]Status Spinner"))

with console.status("[bold green]Connecting to database...") as status:
    time.sleep(1)
    status.update("[bold yellow]Running migrations...")
    time.sleep(1)
    status.update("[bold cyan]Seeding data...")
    time.sleep(0.5)

console.print("[green]✓[/] Database ready!")
print()


# =============================================================================
# INSPECT — explore any Python object
# =============================================================================

console.print(Rule("[bold cyan]Inspect"))

# Inspect shows an object's attributes, methods, and docs
console.print("[dim]Inspecting a list object:[/]")
rich_list = [1, 2, 3]
from rich import inspect  # noqa: E402
inspect(rich_list, methods=True, title="list object")
print()


# =============================================================================
# LAYOUTS — divide the terminal into regions
# =============================================================================

console.print(Rule("[bold cyan]Layout"))

layout = Layout()
layout.split_row(
    Layout(Panel("Left pane", border_style="blue"), name="left"),
    Layout(Panel("Right pane", border_style="green"), name="right"),
)
console.print(layout)
print()


console.print(Rule("[bold green]✓ Rich demo complete!"))
