"""Core functionality for the demo project."""

from __future__ import annotations


def say_hello(name: str = "World") -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"


def calculate_sum(a: int | float, b: int | float) -> int | float:
    """Return the sum of two numbers."""
    return a + b
