#!/usr/bin/env python3
"""
Monitor Google Sheet for new volunteer responses from Google Form.

This script checks a Google Sheet (linked to Google Form) for new rows.
It can work in two modes:
1. Via Google Sheets API with OAuth token (requires proper scope)
2. Via CSV export (if sheet is shared with "Anyone with link can view")

The script compares current rows with previously stored state and detects new submissions.
Alerts are generated similar to issue monitoring.

Configuration:
- SHEET_ID: from Google Sheets URL
- SHEET_NAME: worksheet name (default "Form Responses 1")
- SHEET_URL: optional, if using CSV export
- TOKEN_PATH: path to OAuth token with sheets scope
- STATE_FILE: where to store previous row count/hash
- FLAG_FILE: flag to indicate changes detected

Usage:
  python3 scripts/monitor_google_sheet.py

Environment variables:
  GOOGLE_SHEET_ID: The sheet ID from the URL
  GOOGLE_SHEET_NAME: Worksheet name (default "Form Responses 1")
  GOOGLE_SHEET_CSV_URL: Full CSV export URL (if using CSV method)
  AI_VILLAGE_AGENT_EMAILS: Comma-separated list of agent emails to ignore
"""

import os
import sys
import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime
import requests
import re
import tempfile

# Configuration defaults
REPO_DIR = Path(__file__).parent.parent
MONITORING_DIR = REPO_DIR / "monitoring"
STATE_FILE = MONITORING_DIR / "sheet_state.json"
FLAG_FILE = MONITORING_DIR / "sheet_changes_detected.flag"
CHANGES_TEXT_FILE = MONITORING_DIR / "SHEET_CHANGES_DETECTED"
LOG_FILE = MONITORING_DIR / "sheet_monitor.log"

# Default AI agent emails to ignore (from internal memory)
DEFAULT_AGENT_EMAILS = [
    "gpt-5.1@agentvillage.org",
    "gpt-5.2@agentvillage.org",
    "claude-3.7@agentvillage.org",
    "claude-opus-4.6@agentvillage.org",
    "gemini-2.5-pro@agentvillage.org",
    "gemini-3-pro@agentvillage.org",
    "deepseek-v3.2@agentvillage.org",
    "claude-sonnet-4.5@agentvillage.org",
    "claude-opus-4.5@agentvillage.org",
    "claude-haiku-4.5@agentvillage.org",
    "gpt-5@agentvillage.org",
    "opus-4.5-claude-code@agentvillage.org",
]

def ensure_monitoring_dir():
    """Create monitoring directory if it doesn't exist."""
    MONITORING_DIR.mkdir(exist_ok=True)
    # Clear flag files at start
    if FLAG_FILE.exists():
        FLAG_FILE.unlink()
    if CHANGES_TEXT_FILE.exists():
        CHANGES_TEXT_FILE.unlink()

def load_previous_state():
    """Load previous monitoring state from JSON file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {
        "last_check": None,
        "row_count": 0,
        "row_hashes": [],
        "last_row_hash": None,
        "last_timestamp": None
    }

def save_state(state):
    """Save current monitoring state to JSON file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_agent_emails():
    """Get list of AI Village agent emails to ignore."""
    env_emails = os.environ.get("AI_VILLAGE_AGENT_EMAILS")
    if env_emails:
        return [email.strip() for email in env_emails.split(",")]
    return DEFAULT_AGENT_EMAILS

def log_message(message):
    """Log message to log file and print to stdout."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def get_sheet_id_from_url(url):
    """Extract sheet ID from Google Sheets URL."""
    # Pattern for https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
    patterns = [
        r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
        r'/d/([a-zA-Z0-9-_]+)',
        r'^([a-zA-Z0-9-_]+)$'  # Just the ID itself
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Assume it's already the ID

def fetch_sheet_via_csv(sheet_id, sheet_name="Form Responses 1"):
    """Fetch sheet data via CSV export (requires public sharing)."""
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    log_message(f"Fetching CSV from: {csv_url}")
    
    response = requests.get(csv_url)
    if response.status_code != 200:
        log_message(f"CSV fetch failed with status {response.status_code}")
        if response.status_code == 403:
            log_message("Sheet may not be publicly shared. Need 'Anyone with link can view' permission.")
        return None
    
    # Parse CSV
    content = response.content.decode('utf-8')
    rows = list(csv.reader(content.splitlines()))
    return rows

def fetch_sheet_via_api(sheet_id, sheet_name="Form Responses 1", token_path=None):
    """Fetch sheet data using Google Sheets API (requires OAuth token with sheets scope)."""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        log_message("Google Sheets API libraries not available. Install: pip install google-api-python-client google-auth-oauthlib")
        return None
    
    if token_path is None:
        token_path = os.environ.get("GOOGLE_TOKEN_PATH", "/home/computeruse/email/token.json")
    
    if not os.path.exists(token_path):
        log_message(f"Token file not found at {token_path}")
        return None
    
    try:
        creds = Credentials.from_authorized_user_file(token_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
        service = build('sheets', 'v4', credentials=creds)
        
        # Get spreadsheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        values = result.get('values', [])
        
        return values
    except Exception as e:
        log_message(f"Google Sheets API error: {e}")
        # Check if token lacks sheets scope
        if "insufficient authentication scopes" in str(e):
            log_message("Token lacks Sheets API scope. Use CSV export method or get new token with sheets scope.")
        return None

def process_rows(rows, agent_emails):
    """Process rows and filter out agent submissions."""
    if not rows:
        return []
    
    # Assume first row is header
    if len(rows) < 2:
        return []
    
    header = rows[0]
    data_rows = rows[1:]
    
    # Find email column index
    email_col_idx = -1
    for i, col in enumerate(header):
        if 'email' in col.lower():
            email_col_idx = i
            break
    
    # Filter out rows from agent emails
    filtered = []
    for row in data_rows:
        if email_col_idx >= 0 and len(row) > email_col_idx:
            email = row[email_col_idx].strip().lower()
            if email in agent_emails:
                log_message(f"Ignoring agent submission from {email}")
                continue
        filtered.append(row)
    
    return filtered

def create_row_hash(row):
    """Create a hash for a row to detect changes."""
    row_str = "|".join(str(cell) for cell in row)
    return hashlib.md5(row_str.encode()).hexdigest()

def detect_new_rows(current_rows, previous_state):
    """Compare current rows with previous state and detect new rows."""
    previous_hashes = previous_state.get("row_hashes", [])
    previous_count = previous_state.get("row_count", 0)
    
    current_hashes = [create_row_hash(row) for row in current_rows]
    new_rows = []
    
    for i, row_hash in enumerate(current_hashes):
        if row_hash not in previous_hashes:
            new_rows.append((i + 1, current_rows[i]))  # i+1 for 1-indexed row number
    
    return new_rows, current_hashes

def format_new_row_details(row_data, row_number):
    """Format details of a new row for reporting."""
    # Basic formatting: show first few columns
    preview = " | ".join(str(cell)[:50] for cell in row_data[:3])
    if len(row_data) > 3:
        preview += " ..."
    return f"Row {row_number}: {preview}"

def main():
    ensure_monitoring_dir()
    log_message("Starting Google Sheet monitor")
    
    # Get configuration
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    sheet_name = os.environ.get("GOOGLE_SHEET_NAME", "Form Responses 1")
    csv_url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    token_path = os.environ.get("GOOGLE_TOKEN_PATH", "/home/computeruse/email/token.json")
    
    if not sheet_id and csv_url:
        sheet_id = get_sheet_id_from_url(csv_url)
    
    if not sheet_id:
        log_message("ERROR: No GOOGLE_SHEET_ID or GOOGLE_SHEET_CSV_URL provided")
        sys.exit(1)
    
    # Load previous state
    previous_state = load_previous_state()
    
    # Fetch sheet data
    rows = None
    
    # Try API first if token has sheets scope
    rows = fetch_sheet_via_api(sheet_id, sheet_name, token_path)
    
    # Fall back to CSV export
    if rows is None:
        rows = fetch_sheet_via_csv(sheet_id, sheet_name)
    
    if rows is None:
        log_message("ERROR: Could not fetch sheet data via any method")
        sys.exit(1)
    
    # Process rows
    agent_emails = [email.lower() for email in get_agent_emails()]
    filtered_rows = process_rows(rows, agent_emails)
    
    # Detect new rows
    new_rows, current_hashes = detect_new_rows(filtered_rows, previous_state)
    
    # Update state
    new_state = {
        "last_check": datetime.utcnow().isoformat() + "Z",
        "row_count": len(filtered_rows),
        "row_hashes": current_hashes,
        "last_row_hash": current_hashes[-1] if current_hashes else None,
        "last_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_state(new_state)
    
    # Handle changes
    if new_rows:
        log_message(f"Detected {len(new_rows)} new row(s)")
        
        # Create flag file
        flag_data = {
            "changes_detected": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "new_row_count": len(new_rows),
            "details": [f"New Google Form response: {format_new_row_details(row, row_num)}" 
                       for row_num, row in new_rows]
        }
        with open(FLAG_FILE, 'w') as f:
            json.dump(flag_data, f)
        
        # Create human-readable changes file
        with open(CHANGES_TEXT_FILE, 'w') as f:
            f.write(f"Google Sheet changes detected at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"New rows: {len(new_rows)}\n")
            for row_num, row in new_rows:
                f.write(f"- Row {row_num}: {' | '.join(str(cell) for cell in row[:3])}\n")
        
        log_message("Change flag files created")
        
        # Also log to main issue monitor log for consistency
        with open(MONITORING_DIR / "issue_monitor.log", 'a') as f:
            f.write(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] Google Sheet: {len(new_rows)} new responses\n")
        
        sys.exit(0)  # Exit with success, changes detected
    else:
        log_message("No new rows detected")
        # Ensure flag files are cleared
        if FLAG_FILE.exists():
            FLAG_FILE.unlink()
        if CHANGES_TEXT_FILE.exists():
            CHANGES_TEXT_FILE.unlink()
    
    log_message("Google Sheet monitor completed")

if __name__ == "__main__":
    main()
