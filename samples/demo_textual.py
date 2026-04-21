"""Textual demo — build terminal user interfaces (TUIs) in Python.

Run:  python samples/demo_textual.py

Textual is a framework for building rich, interactive terminal applications
with a CSS-like styling system, event handling, and a widget library. It runs
entirely in the terminal — no browser or GUI toolkit needed.

Install:  uv sync --group libs
Press 'q' to quit the app.
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Static,
)


# =============================================================================
# CUSTOM WIDGETS — subclass Static or Widget to make reusable components
# =============================================================================

class CounterDisplay(Static):
    """A widget that displays a counter with reactive updates.

    Reactive attributes automatically re-render the widget when their value
    changes. No manual refresh calls needed.
    """

    count: reactive[int] = reactive(0)

    def render(self) -> str:
        return f"Count: {self.count}"


# =============================================================================
# THE APP — the root of every Textual application
# =============================================================================

class DemoApp(App):
    """A demo Textual app showcasing core features.

    Key concepts demonstrated:
    - CSS styling (inline and via CSS property)
    - Widget composition via compose()
    - Event handling with on_<widget>_<event> methods
    - Reactive attributes for automatic UI updates
    - Key bindings
    - DataTable for tabular data
    - Input widget for text entry
    """

    # -------------------------------------------------------------------------
    # CSS — style your app like a web page. Textual supports a subset of CSS
    # including flexbox-like layout, colors, borders, padding, and margin.
    # -------------------------------------------------------------------------
    CSS = """
    Screen {
        layout: vertical;
    }

    #top-section {
        height: auto;
        padding: 1 2;
    }

    #counter-section {
        layout: horizontal;
        height: auto;
        padding: 1 2;
        align: center middle;
    }

    #counter-section Button {
        margin: 0 1;
    }

    CounterDisplay {
        width: auto;
        min-width: 16;
        padding: 0 2;
        text-align: center;
        background: $surface;
        border: solid $primary;
    }

    #input-section {
        height: auto;
        padding: 1 2;
    }

    #greeting-label {
        padding: 0 2;
        color: $success;
    }

    #table-section {
        height: 1fr;
        padding: 1 2;
    }

    DataTable {
        height: 1fr;
    }
    """

    # -------------------------------------------------------------------------
    # BINDINGS — map keyboard shortcuts to actions
    # -------------------------------------------------------------------------
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("r", "reset_counter", "Reset Counter"),
    ]

    TITLE = "Textual Demo App"

    def compose(self) -> ComposeResult:
        """Build the widget tree.

        compose() is called once when the app starts. It yields widgets in the
        order they should appear. Containers (Vertical, Horizontal) control
        layout.
        """
        # Header shows app title and clock
        yield Header()

        # Welcome section
        yield Static(
            "Welcome to the Textual demo! This showcases core Textual features.\n"
            "Use the buttons, type in the input, and check the key bindings below.",
            id="top-section",
        )

        # Counter section — demonstrates reactive attributes and button events
        yield Horizontal(
            Button("-1", id="decrement", variant="error"),
            CounterDisplay(id="counter"),
            Button("+1", id="increment", variant="success"),
            id="counter-section",
        )

        # Input section — demonstrates text input and dynamic label updates
        yield Vertical(
            Input(placeholder="Type your name and press Enter...", id="name-input"),
            Label("", id="greeting-label"),
            id="input-section",
        )

        # DataTable section — demonstrates tabular data display
        yield Vertical(
            Static("[bold]Sample Data:[/]"),
            DataTable(id="data-table"),
            id="table-section",
        )

        # Footer shows available key bindings automatically
        yield Footer()

    def on_mount(self) -> None:
        """Called after the app is mounted and ready.

        Use on_mount() to populate widgets with initial data, start timers,
        or perform any setup that requires the widget tree to exist.
        """
        # Populate the DataTable with sample data
        table = self.query_one("#data-table", DataTable)
        table.add_columns("Name", "Language", "Stars", "Category")
        table.add_rows([
            ("Textual", "Python", "25k", "TUI Framework"),
            ("Rich", "Python", "50k", "Terminal Formatting"),
            ("Click", "Python", "15k", "CLI Framework"),
            ("Ruff", "Rust/Python", "32k", "Linter"),
            ("uv", "Rust", "28k", "Package Manager"),
        ])

    # -------------------------------------------------------------------------
    # EVENT HANDLERS — respond to user interactions
    # -------------------------------------------------------------------------
    # Textual uses a naming convention: on_<widget_type>_<event_name>

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks by checking the button's ID."""
        counter = self.query_one("#counter", CounterDisplay)
        if event.button.id == "increment":
            counter.count += 1
        elif event.button.id == "decrement":
            counter.count -= 1

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in the input field."""
        label = self.query_one("#greeting-label", Label)
        if event.value.strip():
            label.update(f"Hello, {event.value}! 👋")
        else:
            label.update("")

    # -------------------------------------------------------------------------
    # ACTIONS — triggered by key bindings or programmatically
    # -------------------------------------------------------------------------

    def action_toggle_dark(self) -> None:
        """Toggle between dark and light mode."""
        self.dark = not self.dark

    def action_reset_counter(self) -> None:
        """Reset the counter to zero."""
        self.query_one("#counter", CounterDisplay).count = 0


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = DemoApp()
    app.run()
