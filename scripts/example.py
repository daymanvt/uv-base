"""Standalone script example — for when you just need a single file.

Run from the project root with your virtualenv activated:
    python scripts/example.py
"""

from __future__ import annotations

import time

from tqdm import tqdm


def main() -> None:
    """Demonstrate basic script with tqdm progress bar."""
    print("Running standalone script example...\n")

    items = list(range(50))
    results = []
    for item in tqdm(items, desc="Processing"):
        results.append(item * 2)
        time.sleep(0.02)

    print(f"\nProcessed {len(results)} items.")
    print(f"First 5 results: {results[:5]}")


if __name__ == "__main__":
    main()
