"""Demo project package — a template for uv-managed Python projects."""

from __future__ import annotations

__all__ = ["say_hello", "calculate_sum", "__version__"]
__version__ = "0.1.0"

from demo_project.core import calculate_sum, say_hello
