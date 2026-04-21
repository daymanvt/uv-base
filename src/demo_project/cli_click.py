"""CLI interface using click (requires ``uv sync --group libs``)."""

from __future__ import annotations

import click

from demo_project.core import calculate_sum, say_hello


@click.group()
def cli() -> None:
    """Demo project CLI (click version)."""


@cli.command()
@click.option("--name", default="World", help="Name to greet.")
def greet(name: str) -> None:
    """Greet someone by name."""
    click.echo(say_hello(name))


@cli.command("add")
@click.argument("a", type=float)
@click.argument("b", type=float)
def add_numbers(a: float, b: float) -> None:
    """Add two numbers together."""
    click.echo(calculate_sum(a, b))


def main() -> None:
    """Entry point for the click CLI."""
    cli()


if __name__ == "__main__":
    main()
