#!/bin/bash
# Wrapper script for Google Sheet monitoring

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
cd "$REPO_DIR"

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Run the Python monitor
python3 scripts/monitor_google_sheet.py "$@"

# Check for changes detected flag
FLAG_FILE="monitoring/sheet_changes_detected.flag"
if [ -f "$FLAG_FILE" ]; then
    echo "Changes detected in Google Sheet"
    exit 1
else
    echo "No changes detected"
    exit 0
fi
