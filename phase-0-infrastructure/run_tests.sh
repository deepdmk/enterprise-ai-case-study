#!/bin/bash

# Script to run phase-0-infrastructure tests

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to script directory
cd "$SCRIPT_DIR"

# Run pytest
if [ $# -eq 0 ]; then
    # No arguments - run all tests
    python -m pytest tests/ -v
else
    # Pass arguments to pytest
    python -m pytest "$@"
fi
