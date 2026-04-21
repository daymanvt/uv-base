uvinit() {
    local project_name="${PWD##*/}"
    local pkg_name="${project_name//-/_}"

    # Copy base config
    cp "$UV_BASE_DIR/pylintrc" .

    # Create a README so hatchling doesn't fail on readme = "README.md"
    echo "# ${project_name}" > README.md

    # Copy sample files for tool validation
    cp -r "$UV_BASE_DIR/samples" .

    if [[ "$1" == "--full" ]]; then
        cp "$UV_BASE_DIR/pyproject.toml.full" pyproject.toml
        sed -i "s/demo-project/${project_name}/g" pyproject.toml
        sed -i "s/demo_project/${pkg_name}/g" pyproject.toml

        # Full package layout
        mkdir -p "src/${pkg_name}" tests

        cp "$UV_BASE_DIR"/src/demo_project/*.py "src/${pkg_name}/"
        cp "$UV_BASE_DIR"/src/demo_project/py.typed "src/${pkg_name}/"
        cp -r "$UV_BASE_DIR"/tests/* tests/ 2>/dev/null
        cp -r "$UV_BASE_DIR/scripts" .

        # Update imports in copied source files
        find src/ tests/ -name '*.py' -exec sed -i "s/demo_project/${pkg_name}/g" {} +

        echo "Created package: src/${pkg_name}/"
    else
        cp "$UV_BASE_DIR/pyproject.toml.simple" pyproject.toml
        sed -i "s/demo-project/${project_name}/g" pyproject.toml
        sed -i "s/demo_project/${pkg_name}/g" pyproject.toml

        cat > main.py << 'PYEOF'
"""Main script."""


def main() -> None:
    print("Hello, World!")


if __name__ == "__main__":
    main()
PYEOF
        echo "Created main.py"
    fi

    uv python pin 3.10
    if [[ "$1" == "--full" ]]; then
        uv sync --group libs --group test
    else
        uv sync
    fi
    echo "Done! Run: source .venv/bin/activate"
    echo ""
    echo "REMINDER: update these CHANGEME fields in pyproject.toml:"
    echo "  - description"
    echo "  - authors (name + email)"
}