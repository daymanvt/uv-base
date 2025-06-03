# src/demo_project/cli.py

import sys

def main():
    """
    Main entry point for the demo-project CLI utility.
    """
    print("Hello from the generic demo-project CLI!")
    print(f"Arguments passed: {sys.argv[1:]}")

    # You would typically add your CLI argument parsing and
    # command dispatching logic here (e.g., using `click` or `argparse`).

if __name__ == "__main__":
    main()