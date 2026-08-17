#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$BACKEND_DIR"

echo "Backend directory: $BACKEND_DIR"

echo "Running Ruff formatter..."
uv run ruff format .

echo "Running Ruff linter..."
uv run ruff check . --fix

echo "Verifying Ruff..."
uv run ruff check .

echo "Starting EagleEye..."
uv run uvicorn app.main:app --reload