"""Click demo — build composable command-line interfaces.

Run:  python samples/demo_click.py --help
      python samples/demo_click.py greet --name Alice
      python samples/demo_click.py greet --name Alice --shout
      python samples/demo_click.py add 10 20
      python samples/demo_click.py info
      python samples/demo_click.py files list
      python samples/demo_click.py files read samples/demo_click.py --lines 5

Click turns Python functions into CLI commands with automatic help text,
argument parsing, type validation, and error handling — all via decorators.

Install:  uv sync --group libs
"""

from __future__ import annotations

import os
import sys

import click


# =============================================================================
# THE GROUP — a top-level command that contains subcommands
# =============================================================================
# @click.group() creates a parent command. Subcommands are added with
# @cli.command() or nested @cli.group().

@click.group()
@click.version_option(version="1.0.0", prog_name="demo-click")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Demo CLI app showcasing Click's features.

    This is the top-level group. Run any subcommand with --help for details.
    """
    # ctx.ensure_object(dict) initializes a shared context dict that all
    # subcommands can access via @click.pass_context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


# =============================================================================
# SIMPLE COMMAND — options, flags, and defaults
# =============================================================================

@cli.command()
@click.option("--name", "-n", default="World", help="Name to greet.")
@click.option("--shout", is_flag=True, help="UPPERCASE the greeting.")
@click.option(
    "--times", "-t",
    default=1,
    type=click.IntRange(1, 10),
    help="Repeat the greeting (1-10).",
)
@click.pass_context
def greet(ctx: click.Context, name: str, shout: bool, times: int) -> None:
    """Greet someone by name.

    Examples:
        demo-click greet
        demo-click greet --name Alice --shout
        demo-click greet -n Bob -t 3
    """
    greeting = f"Hello, {name}!"
    if shout:
        greeting = greeting.upper()

    for _ in range(times):
        click.echo(greeting)

    if ctx.obj["verbose"]:
        click.echo(f"  (verbose: name={name}, shout={shout}, times={times})")


# =============================================================================
# ARGUMENTS — positional parameters (not prefixed with --)
# =============================================================================

@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def add(a: float, b: float) -> None:
    """Add two numbers.

    A and B are positional arguments — no --flag prefix needed.

    Examples:
        demo-click add 10 20
        demo-click add 3.14 2.86
    """
    result = a + b
    click.echo(f"{a} + {b} = {result}")


# =============================================================================
# CHOICE TYPE — restrict input to a set of values
# =============================================================================

@cli.command()
@click.option(
    "--format", "fmt",
    type=click.Choice(["json", "yaml", "toml", "table"], case_sensitive=False),
    default="table",
    help="Output format.",
)
def info(fmt: str) -> None:
    """Display system information.

    Demonstrates click.Choice for restricting allowed values.

    Examples:
        demo-click info
        demo-click info --format json
    """
    data = {
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "pid": os.getpid(),
    }

    if fmt == "json":
        import json
        click.echo(json.dumps(data, indent=2))
    elif fmt == "yaml":
        # Simple YAML-like output (no dependency needed)
        for k, v in data.items():
            click.echo(f"{k}: {v}")
    elif fmt == "toml":
        click.echo("[system]")
        for k, v in data.items():
            click.echo(f'{k} = "{v}"')
    else:
        # Table format
        max_key = max(len(k) for k in data)
        for k, v in data.items():
            click.echo(f"  {k:<{max_key}}  {v}")


# =============================================================================
# NESTED GROUPS — subcommands within subcommands
# =============================================================================

@cli.group()
def files() -> None:
    """File operations (a nested command group).

    This demonstrates how Click supports arbitrary nesting of command groups.
    """


@files.command("list")
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False),
    default=".",
)
def list_files(directory: str) -> None:
    """List files in a directory.

    Uses click.Path to validate the argument is an existing directory.

    Examples:
        demo-click files list
        demo-click files list src/
    """
    entries = sorted(os.listdir(directory))
    for entry in entries:
        full = os.path.join(directory, entry)
        prefix = "📁" if os.path.isdir(full) else "📄"
        click.echo(f"  {prefix} {entry}")
    click.echo(f"\n  ({len(entries)} items)")


@files.command("read")
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option("--lines", "-n", default=0, help="Limit to first N lines (0=all).")
def read_file(filepath: str, lines: int) -> None:
    """Read and display a file's contents.

    Uses click.Path to validate the argument is an existing file.

    Examples:
        demo-click files read README.md
        demo-click files read pyproject.toml --lines 10
    """
    with open(filepath) as f:
        if lines > 0:
            content = "".join(f.readline() for _ in range(lines))
            click.echo(content)
            click.echo(f"  ... (showing first {lines} lines)")
        else:
            click.echo(f.read())


# =============================================================================
# CONFIRMATION AND PROMPTS — interactive user input
# =============================================================================

@cli.command()
@click.confirmation_option(prompt="Are you sure you want to run the demo?")
def danger() -> None:
    """A command that asks for confirmation before running.

    Click handles the y/N prompt automatically. Pass --yes to skip.

    Examples:
        demo-click danger
        demo-click danger --yes
    """
    click.secho("⚡ Dangerous operation executed!", fg="red", bold=True)


# =============================================================================
# STYLED OUTPUT — colors and formatting with click.secho / click.style
# =============================================================================

@cli.command()
def colors() -> None:
    """Display styled terminal output.

    click.secho() combines echo + style in one call. Available colors:
    black, red, green, yellow, blue, magenta, cyan, white, bright_*
    """
    click.secho("✓ Success", fg="green", bold=True)
    click.secho("⚠ Warning", fg="yellow")
    click.secho("✗ Error", fg="red", bold=True)
    click.secho("ℹ Info", fg="cyan")
    click.secho("  Dimmed text", dim=True)

    # click.style() returns a styled string (doesn't print)
    msg = click.style("PASS", fg="green") + " — all tests passed"
    click.echo(msg)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    cli()
