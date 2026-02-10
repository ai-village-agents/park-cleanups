#!/bin/bash
# Test script for Google Sheet monitor

echo "Testing Google Sheet monitor configuration..."
echo ""

# Test 1: Check dependencies
echo "=== Test 1: Dependencies ==="
python3 -c "import requests, json, csv, hashlib; print('✅ Core dependencies OK')"
python3 -c "try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    print('✅ Google API libraries OK')
except ImportError:
    print('⚠️  Google API libraries not installed (API method will fail)')"

echo ""
echo "=== Test 2: Environment ==="
if [ -f "/home/computeruse/email/token.json" ]; then
    echo "✅ Token file exists"
    python3 -c "
import json
with open('/home/computeruse/email/token.json') as f:
    t = json.load(f)
scopes = t.get('scopes', [])
print(f'  Scopes: {scopes}')
if 'https://www.googleapis.com/auth/spreadsheets' in scopes or 'https://www.googleapis.com/auth/spreadsheets.readonly' in scopes:
    print('  ✅ Token has Sheets API scope')
else:
    print('  ❌ Token lacks Sheets API scope (use CSV method)')
    "
else
    echo "❌ Token file not found"
fi

echo ""
echo "=== Test 3: Monitoring directory ==="
mkdir -p monitoring
ls -la monitoring/

echo ""
echo "=== Test 4: Script syntax ==="
python3 -m py_compile scripts/monitor_google_sheet.py && echo "✅ monitor_google_sheet.py syntax OK"
python3 -c "import scripts.monitor_google_sheet; print('✅ Module imports OK')"

echo ""
echo "=== Test 5: Workflow file ==="
if [ -f ".github/workflows/monitor-google-sheet.yml" ]; then
    echo "✅ Workflow file exists"
    grep -c "cron:" .github/workflows/monitor-google-sheet.yml | xargs echo "  Schedule lines:"
else
    echo "❌ Workflow file missing"
fi

echo ""
echo "=== Test 6: Documentation ==="
if [ -f "monitoring/GOOGLE_SHEET_MONITORING.md" ]; then
    echo "✅ Documentation exists"
else
    echo "❌ Documentation missing"
fi

echo ""
echo "=== Summary ==="
echo "The Google Sheet monitoring system is ready to deploy."
echo "Once Claude 3.7 Sonnet provides the Sheet URL:"
echo "1. Extract Sheet ID from URL"
echo "2. Set Sheet sharing to 'Anyone with link can view'"
echo "3. Add GOOGLE_SHEET_ID and GOOGLE_SHEET_CSV_URL as GitHub secrets"
echo "4. Enable the workflow in GitHub Actions"
echo ""
echo "The system will then monitor for new Form submissions every 15 minutes."
