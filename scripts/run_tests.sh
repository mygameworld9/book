#!/bin/bash
# Run all tests and quality checks

set -e

echo "Running code quality checks..."
echo ""

echo "1. Ruff (linting)..."
uv run ruff check src tests
echo "✓ Ruff passed"
echo ""

echo "2. MyPy (type checking)..."
uv run mypy src
echo "✓ MyPy passed"
echo ""

echo "3. Pytest (unit tests)..."
uv run pytest tests/unit -v --cov=src
echo "✓ Unit tests passed"
echo ""

echo "4. Pytest (integration tests)..."
uv run pytest tests/integration -v
echo "✓ Integration tests passed"
echo ""

echo "All checks passed! ✓"
