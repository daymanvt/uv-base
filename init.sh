#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [--310 | --latest] [--full | --simple]"
    echo "Options:"
    echo "  --310     Use Python 3.10"
    echo "  --latest  Use latest Python version"
    echo "  --full    Full configuration"
    echo "  --simple  Simple configuration"
    exit 1
}

# Function to copy template
copy_template() {
    local version=$1
    local mode=$2
    local template_name="pyproject.${version}.${mode}.toml"
    local template_path="_templates/${template_name}"

    if [ ! -f "$template_path" ]; then
        echo "Error: Template ${template_name} not found in _templates directory"
        exit 1
    fi

    cp "$template_path" "pyproject.toml"
    echo "Copied ${template_name} to pyproject.toml"
}

# Function to run uv sync
run_uv_sync() {
    if ! command -v uv &> /dev/null; then
        echo "Error: uv command not found. Please ensure uv is installed and in your PATH"
        exit 1
    fi

    if ! uv sync; then
        echo "Error: Failed to run uv sync"
        exit 1
    fi

    echo "Successfully ran uv sync"
}

# Parse arguments
PYTHON_VERSION=""
MODE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --310)
            PYTHON_VERSION="310"
            shift
            ;;
        --latest)
            PYTHON_VERSION="latest"
            shift
            ;;
        --full)
            MODE="full"
            shift
            ;;
        --simple)
            MODE="simple"
            shift
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Validate arguments
if [ -z "$PYTHON_VERSION" ] || [ -z "$MODE" ]; then
    echo "Error: Both Python version and mode must be specified"
    usage
fi

# Main execution
copy_template "$PYTHON_VERSION" "$MODE"
run_uv_sync