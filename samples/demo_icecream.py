"""Icecream demo — a better print() for debugging.

Run:  python samples/demo_icecream.py

Icecream's ic() function replaces print() during debugging. It automatically
prints the expression AND its value, so you never have to write
`print(f"x = {x}")` again.

Install:  uv sync --group libs
"""

from icecream import ic


# =============================================================================
# BASIC USAGE — ic() prints variable name + value
# =============================================================================

x = 42
ic(x)                                  # ic| x: 42

name = "Alice"
ic(name)                               # ic| name: 'Alice'

pi = 3.14159
ic(pi)                                 # ic| pi: 3.14159


# =============================================================================
# EXPRESSIONS — ic() evaluates and labels any expression
# =============================================================================

ic(1 + 2)                             # ic| 1 + 2: 3
ic(name.upper())                       # ic| name.upper(): 'ALICE'
ic(len(name))                          # ic| len(name): 5
ic([i ** 2 for i in range(5)])         # ic| [i ** 2 for i in range(5)]: [0, 1, 4, 9, 16]


# =============================================================================
# DATA STRUCTURES — dicts, lists, nested objects
# =============================================================================

user = {"name": "Alice", "age": 30, "roles": ["admin", "user"]}
ic(user)                               # ic| user: {'name': 'Alice', ...}
ic(user["roles"])                      # ic| user['roles']: ['admin', 'user']
ic(user.get("email", "N/A"))          # ic| user.get('email', 'N/A'): 'N/A'


# =============================================================================
# NO-ARG CALLS — ic() with no arguments prints file, line, and function
# =============================================================================
# Useful as a "was this code reached?" check, like a smarter breakpoint.

def process_order(item):
    ic()                               # ic| demo_icecream.py:57 in process_order()
    return f"Processing {item}"

process_order("widget")


# =============================================================================
# RETURN VALUE — ic() returns its argument, so you can inline it
# =============================================================================
# This means you can wrap any expression without changing behavior.

result = ic(sum([10, 20, 30]))         # ic| sum([10, 20, 30]): 60
# result is now 60

doubled = [ic(n * 2) for n in range(3)]
# prints each value as it's computed, doubled = [0, 2, 4]


# =============================================================================
# FUNCTIONS AND CLASSES — ic() works with any callable result
# =============================================================================

def add(a, b):
    return a + b

ic(add(3, 4))                          # ic| add(3, 4): 7


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
ic(p)                                  # ic| p: Point(1, 2)
ic(p.x)                               # ic| p.x: 1


# =============================================================================
# ENABLE / DISABLE — silence ic() globally without removing calls
# =============================================================================
# Perfect for leaving ic() calls in code but silencing them in production.

ic.disable()
ic("this will NOT print")             # (nothing — ic is disabled)

ic.enable()
ic("this WILL print")                 # ic| 'this WILL print': 'this WILL print'


# =============================================================================
# CUSTOM OUTPUT — change prefix, add context, redirect output
# =============================================================================

# Add file/line/function context to every ic() call
ic.configureOutput(includeContext=True)
ic(x)                                  # ic| demo_icecream.py:101 in <module>- x: 42

# Change the prefix from "ic| " to something custom
ic.configureOutput(prefix="DEBUG >>> ", includeContext=False)
ic(x)                                  # DEBUG >>> x: 42

# Reset to defaults
ic.configureOutput(prefix="ic| ", includeContext=False)


# =============================================================================
# COMMON PATTERNS
# =============================================================================

# Pattern 1: Debug a conditional branch
value = 15
if value > 10:
    ic("took the > 10 branch")
else:
    ic("took the <= 10 branch")

# Pattern 2: Inspect loop iterations
for i, letter in enumerate("abc"):
    ic(i, letter)

# Pattern 3: Quick function tracing
def fetch_data(url):
    ic(url)                            # see what URL was passed
    data = {"status": 200}
    ic(data)                           # see what came back
    return data

fetch_data("https://api.example.com/users")

print("\n✓ Icecream demo complete!")
