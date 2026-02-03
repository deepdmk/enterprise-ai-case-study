#!/bin/bash

# Script to run phase-0-infrastructure tests
# This script handles the logging module conflict by temporarily renaming the directory

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to script directory
cd "$SCRIPT_DIR"

# Check if logging directory exists
if [ -d "logging" ]; then
    echo "Temporarily renaming logging directory to avoid module conflict..."
    mv logging logging_backup
    RENAMED=true
else
    RENAMED=false
fi

# Function to restore logging directory on exit
cleanup() {
    if [ "$RENAMED" = true ]; then
        echo "Restoring logging directory..."
        mv logging_backup logging
    fi
}

# Set trap to always restore directory, even on error
trap cleanup EXIT

# Run pytest
if [ $# -eq 0 ]; then
    # No arguments - run all tests
    python -m pytest tests/ -v
else
    # Pass arguments to pytest
    python -m pytest "$@"
fi
