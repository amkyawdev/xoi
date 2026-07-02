#!/bin/bash
# Test runner script

set -e

echo "Running tests..."

# Run pytest with coverage
pytest tests/ -v --cov=. --cov-report=term-missing

echo "Tests complete!"
