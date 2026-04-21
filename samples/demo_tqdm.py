"""tqdm demo — fast, extensible progress bars for Python.

Run:  python samples/demo_tqdm.py

tqdm wraps any iterable with a progress bar. It's the simplest way to add
visual feedback to loops, downloads, data processing, or any long-running
operation. The name comes from the Arabic "taqaddum" (تقدّم) meaning "progress."

Install:  tqdm is a runtime dependency (always available after uv sync)
"""

from __future__ import annotations

import time

from tqdm import tqdm, trange


# =============================================================================
# BASIC USAGE — wrap any iterable
# =============================================================================

print("=" * 60)
print("BASIC: wrap any iterable with tqdm()")
print("=" * 60)

# tqdm() wraps an iterable and displays a progress bar
items = range(80)
results = []
for item in tqdm(items, desc="Processing"):
    results.append(item * 2)
    time.sleep(0.01)

print(f"  → Processed {len(results)} items\n")


# =============================================================================
# TRANGE — shortcut for tqdm(range(...))
# =============================================================================

print("=" * 60)
print("TRANGE: shortcut for tqdm(range(n))")
print("=" * 60)

# trange(n) is equivalent to tqdm(range(n))
total = 0
for i in trange(50, desc="Summing"):
    total += i
    time.sleep(0.01)

print(f"  → Sum: {total}\n")


# =============================================================================
# CUSTOM FORMATTING — control what the bar shows
# =============================================================================

print("=" * 60)
print("CUSTOM FORMAT: bar_format, unit, unit_scale")
print("=" * 60)

# Custom units — show "files" instead of "it"
for _ in tqdm(range(30), desc="Uploading", unit="file"):
    time.sleep(0.02)

# Custom units with scaling — shows KB, MB, GB automatically
for _ in tqdm(range(50), desc="Downloading", unit="B", unit_scale=True, total=50 * 1024):
    time.sleep(0.01)

# Fully custom bar format
# Available variables: l_bar, bar, r_bar, n, total, percentage, elapsed, remaining, rate
fmt = "{l_bar}{bar:30}{r_bar}"
for _ in tqdm(range(40), bar_format=fmt, desc="Custom bar"):
    time.sleep(0.01)

print()


# =============================================================================
# MANUAL UPDATE — for non-iterable progress
# =============================================================================

print("=" * 60)
print("MANUAL UPDATE: use update() for non-iterable operations")
print("=" * 60)

# When you can't wrap an iterable, create a bar and call update() manually
with tqdm(total=100, desc="Manual progress") as pbar:
    for _ in range(10):
        time.sleep(0.05)
        pbar.update(10)                # advance by 10 each step

print()


# =============================================================================
# NESTED BARS — progress within progress
# =============================================================================

print("=" * 60)
print("NESTED: progress bars inside progress bars")
print("=" * 60)

# Outer bar tracks epochs, inner bar tracks batches within each epoch
for epoch in tqdm(range(3), desc="Epochs", position=0):
    for batch in tqdm(range(20), desc=f"  Epoch {epoch + 1}", position=1, leave=False):
        time.sleep(0.01)

# Extra newline to clean up after nested bars
print()
print()


# =============================================================================
# TQDM.WRITE — print without breaking the progress bar
# =============================================================================

print("=" * 60)
print("TQDM.WRITE: print messages without breaking the bar")
print("=" * 60)

# Regular print() inside a tqdm loop breaks the bar display.
# Use tqdm.write() instead — it prints above the bar cleanly.
for i in tqdm(range(30), desc="Processing"):
    time.sleep(0.02)
    if i == 10:
        tqdm.write("  ℹ Checkpoint reached at step 10")
    if i == 20:
        tqdm.write("  ℹ Almost done at step 20")

print()


# =============================================================================
# WORKING WITH LISTS AND GENERATORS
# =============================================================================

print("=" * 60)
print("LISTS AND GENERATORS")
print("=" * 60)

# Lists — tqdm auto-detects length
words = ["apple", "banana", "cherry", "date", "elderberry"] * 6
for word in tqdm(words, desc="Words"):
    time.sleep(0.01)

# When length is unknown (generators), provide total= if you know it
def generate_items(n):
    for i in range(n):
        yield i

count = 40
for _ in tqdm(generate_items(count), total=count, desc="Generator"):
    time.sleep(0.01)

print()


# =============================================================================
# DYNAMIC DESCRIPTIONS — update desc/postfix during iteration
# =============================================================================

print("=" * 60)
print("DYNAMIC: update description and postfix mid-loop")
print("=" * 60)

statuses = ["connecting", "authenticating", "downloading", "processing", "finalizing"]
pbar = tqdm(statuses, desc="Starting")
for status in pbar:
    pbar.set_description(f"[{status}]")
    # set_postfix adds key=value pairs after the bar
    pbar.set_postfix(step=status, refresh=True)
    time.sleep(0.3)

print()


# =============================================================================
# COLOR — colored progress bars (requires colorama on Windows)
# =============================================================================

print("=" * 60)
print("COLOR: colored progress bars")
print("=" * 60)

# The colour parameter works on most terminals
for _ in tqdm(range(40), desc="Green bar", colour="green"):
    time.sleep(0.01)

for _ in tqdm(range(40), desc="Cyan bar", colour="#00FFFF"):
    time.sleep(0.01)

print()
print("✓ tqdm demo complete!")
