#!/usr/bin/env python3
"""Generate a counts-only volunteer signup verification file.

This script reads the Google Sheet linked to our volunteer signup
Form, filters out known AI Village agent submissions, buckets
remaining responses by park, and writes a strictly aggregate JSON
artifact:

  monitoring/volunteer_counts_verification.json

The output is designed to be privacy-preserving:
- No names, emails, or free-text fields
- No per-row hashes or fingerprints
- Only per-park aggregate counts plus a hash over those counts

Configuration
-------------
The script can be configured via environment variables (the same ones
used by the Sheet monitor) or via command-line arguments.

Environment variables:
  GOOGLE_SHEET_ID       Sheet ID from the URL
  GOOGLE_SHEET_NAME     Worksheet name (default: "Form Responses 1")
  GOOGLE_SHEET_CSV_URL  Optional explicit CSV export URL

  AI_VILLAGE_AGENT_EMAILS  Comma-separated list of agent emails to ignore

Command-line arguments (all optional; env vars win when both set):
  --sheet-id SHEET_ID
  --sheet-name SHEET_NAME
  --csv-url CSV_URL
  --output PATH

If no output path is provided, the file is written to:
  monitoring/volunteer_counts_verification.json

"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# Repository-relative paths
REPO_DIR = Path(__file__).parent.parent
MONITORING_DIR = REPO_DIR / "monitoring"
DEFAULT_OUTPUT_PATH = MONITORING_DIR / "volunteer_counts_verification.json"

# Default AI agent emails to ignore (kept in sync with monitor_google_sheet.py)
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


@dataclass
class SheetConfig:
    sheet_id: str
    sheet_name: str
    csv_url: Optional[str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def get_agent_emails() -> List[str]:
    """Return lowercase agent emails to ignore."""
    env_emails = os.environ.get("AI_VILLAGE_AGENT_EMAILS")
    if env_emails:
        emails = [e.strip().lower() for e in env_emails.split(",") if e.strip()]
        if emails:
            return emails
    return [e.lower() for e in DEFAULT_AGENT_EMAILS]


def resolve_config(args: argparse.Namespace) -> SheetConfig:
    # Environment takes precedence if set
    sheet_id = os.environ.get("GOOGLE_SHEET_ID") or args.sheet_id
    if not sheet_id:
        raise SystemExit("GOOGLE_SHEET_ID env var or --sheet-id argument is required")

    sheet_name = os.environ.get("GOOGLE_SHEET_NAME") or os.environ.get("GOOGLE_SHEET_NAME".upper())
    if not sheet_name:
        sheet_name = args.sheet_name or "Form Responses 1"

    csv_url = os.environ.get("GOOGLE_SHEET_CSV_URL") or args.csv_url

    return SheetConfig(sheet_id=sheet_id, sheet_name=sheet_name, csv_url=csv_url)


def fetch_rows(config: SheetConfig) -> List[List[str]]:
    """Fetch sheet data via CSV.

    We deliberately *only* support CSV here, not the Sheets API, to
    keep the script simple and avoid handling OAuth tokens.
    """
    if config.csv_url:
        url = config.csv_url
    else:
        # Use the same gviz CSV export pattern as the monitor
        url = f"https://docs.google.com/spreadsheets/d/{config.sheet_id}/gviz/tq?tqx=out:csv&sheet={config.sheet_name}"

    print(f"[counts-verification] Fetching CSV from: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        raise SystemExit(f"Failed to fetch CSV (status {resp.status_code}). Check sharing settings and URL.")

    content = resp.content.decode("utf-8")
    rows = list(csv.reader(content.splitlines()))
    if not rows or len(rows) < 2:
        print("[counts-verification] No data rows found in sheet (header only or empty).")
    return rows


def filter_external_rows(rows: List[List[str]], agent_emails: List[str]) -> Tuple[List[str], List[List[str]]]:
    """Filter out rows submitted by known agent emails.

    Returns (header, filtered_rows).
    """
    if not rows or len(rows) < 2:
        return (rows[0] if rows else [], [])

    header = rows[0]
    data_rows = rows[1:]

    # Locate email column (first header that mentions "email")
    email_idx = -1
    for idx, col in enumerate(header):
        if "email" in str(col).lower():
            email_idx = idx
            break

    filtered: List[List[str]] = []
    for row in data_rows:
        if email_idx >= 0 and len(row) > email_idx:
            email = row[email_idx].strip().lower()
            if email and email in agent_emails:
                # Skip agent/test submissions
                continue
        filtered.append(row)

    return header, filtered


def detect_park_column(header: List[str]) -> int:
    """Best-effort detection of the "which park" column.

    Looks for the first column whose header contains "park".
    Returns -1 if not found (rows will be bucketed as other/unspecified).
    """
    for idx, col in enumerate(header):
        if "park" in str(col).lower():
            return idx
    return -1


def bucket_park(value: str) -> str:
    """Map a free-text park value to a stable slug.

    This is intentionally fuzzy and robust to small wording changes.
    """
    v = (value or "").strip().lower()
    if not v:
        return "other_or_unspecified"

    if "mission" in v and "dolores" in v:
        return "mission_dolores"

    if "devoe" in v or "bronx" in v:
        return "devoe_park_bronx"

    return "other_or_unspecified"


def aggregate_counts(header: List[str], rows: List[List[str]]) -> Dict[str, Dict[str, int]]:
    """Aggregate external responses into per-park counts."""
    # Initialize known parks so they always appear, even with zero count
    counts: Dict[str, Dict[str, int]] = {
        "mission_dolores": {
            "label": "Mission Dolores Park",
            "external_responses": 0,
        },
        "devoe_park_bronx": {
            "label": "Devoe Park (Bronx, NYC)",
            "external_responses": 0,
        },
        "other_or_unspecified": {
            "label": "Other or unspecified park",
            "external_responses": 0,
        },
    }

    park_idx = detect_park_column(header)

    for row in rows:
        park_value = ""
        if park_idx >= 0 and len(row) > park_idx:
            park_value = row[park_idx]
        slug = bucket_park(park_value)
        if slug not in counts:
            # In case we ever add new park types dynamically
            counts[slug] = {"label": slug.replace("_", " ").title(), "external_responses": 0}
        counts[slug]["external_responses"] += 1

    return counts


def compute_integrity_hash(counts: Dict[str, Dict[str, int]]) -> Dict[str, str]:
    """Compute a SHA-256 hash over the aggregate counts only.

    This is intentionally based *solely* on total counts per park,
    not on any per-row data, to avoid membership inference links.
    """
    # Deterministic ordering by slug
    parts: List[str] = []
    total = 0
    for slug in sorted(counts.keys()):
        n = int(counts[slug].get("external_responses", 0))
        parts.append(f"{slug}:{n}")
        total += n
    parts.append(f"total:{total}")

    hash_over = "|".join(parts)
    digest = hashlib.sha256(hash_over.encode("utf-8")).hexdigest()

    return {
        "version": "1",
        "hash_algorithm": "sha256",
        "hash_over": hash_over,
        "hash_value": digest,
    }


def write_verification_file(
    output_path: Path,
    config: SheetConfig,
    counts: Dict[str, Dict[str, int]],
) -> None:
    total = sum(int(v.get("external_responses", 0)) for v in counts.values())

    integrity = compute_integrity_hash(counts)

    # We intentionally do NOT expose the raw sheet ID; instead we
    # include a one-way hash that can be compared by collaborators
    # who know the ID, without revealing it to the world.
    sheet_id_hash = hashlib.sha256(config.sheet_id.encode("utf-8")).hexdigest()

    payload = {
        "generated_at": utc_now_iso(),
        "source": {
            "type": "google_sheet_csv_export",
            "sheet_id_hash": sheet_id_hash,
            "sheet_tab": config.sheet_name,
        },
        "counts": counts,
        "total_external_responses": total,
        "integrity": integrity,
        "note": (
            "Counts-only verification artifact generated from the volunteer "
            "signup sheet. This file contains only per-park aggregate counts "
            "and a hash over those counts, with no per-row fingerprints or PII."
        ),
    }

    MONITORING_DIR.mkdir(exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)

    print(f"[counts-verification] Wrote counts-only verification file to: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate counts-only volunteer verification JSON.")
    parser.add_argument("--sheet-id", help="Google Sheet ID (overridden by GOOGLE_SHEET_ID env var if set)")
    parser.add_argument("--sheet-name", help="Worksheet name (overridden by GOOGLE_SHEET_NAME env var if set)")
    parser.add_argument("--csv-url", help="Explicit CSV export URL (overridden by GOOGLE_SHEET_CSV_URL env var if set)")
    parser.add_argument("--output", help="Output path for verification JSON (default: monitoring/volunteer_counts_verification.json)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = resolve_config(args)

    output_path = Path(args.output) if args.output else DEFAULT_OUTPUT_PATH

    agent_emails = get_agent_emails()
    rows = fetch_rows(config)
    header, filtered_rows = filter_external_rows(rows, agent_emails)

    counts = aggregate_counts(header, filtered_rows)
    write_verification_file(output_path, config, counts)


if __name__ == "__main__":  # pragma: no cover
    main()
