"""CLI interface using argparse (stdlib — no extra dependencies)."""

from __future__ import annotations

import argparse
import sys

from demo_project.core import calculate_sum, say_hello


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="demo-cli",
        description="Demo project CLI (argparse version)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    greet = subparsers.add_parser("greet", help="Greet someone")
    greet.add_argument("--name", default="World", help="Name to greet")

    add = subparsers.add_parser("add", help="Add two numbers")
    add.add_argument("a", type=float, help="First number")
    add.add_argument("b", type=float, help="Second number")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the argparse CLI."""
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.command == "greet":
        print(say_hello(args.name))
    elif args.command == "add":
        print(calculate_sum(args.a, args.b))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
