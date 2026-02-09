#!/bin/bash
# Wrapper script for issue monitoring

set -e

cd "$(dirname "$0")/.."

# Ensure monitoring directory exists
mkdir -p monitoring

# Run the Python monitor
python3 scripts/monitor_issues_v2.py

# Check exit code and flag file
if [ $? -eq 1 ] || [ -f monitoring/CHANGES_DETECTED ]; then
    echo "CHANGES DETECTED"
    exit 1
else
    echo "NO CHANGES DETECTED"
    exit 0
fi
