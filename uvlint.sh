uvlint() {
    local target="${1:-src/}"

    echo "==> yapf (format)"
    yapf -i -r "$target"

    echo "==> ruff (lint + auto-fix)"
    ruff check --fix "$target"

    echo "==> pylint (deep lint)"
    pylint "$target"

    echo "==> mypy (type check)"
    mypy "$target"
}