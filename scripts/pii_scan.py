#!/usr/bin/env python3
"""
Lightweight PII scanner for this repository.

Scans tracked files for likely email addresses and US phone numbers.
- Allows only the following domains: agentvillage.org, example.com, example.org, example.net, localhost, sfgov.org, parks.nyc.gov, sanitationfoundation.org.
- Redacts findings in output to avoid leaking PII.
- Exits 0 when clean, 1 when PII is found, 2 on errors.

Usage:
  python scripts/pii_scan.py --all
  python scripts/pii_scan.py --paths-from-nul /tmp/changed_files.txt
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Iterable, List, Sequence, Tuple

# Domains that are allowed to appear in email addresses.
ALLOWLIST_DOMAINS = {
    "agentvillage.org",
    "example.com",
    "example.org",
    "example.net",
    "localhost",
    "sfgov.org",
    "parks.nyc.gov",
    "sanitationfoundation.org",
}

# Paths where public agency phone numbers are expected and should not count as findings.
PHONE_ALLOWED_PATHS = {
    "guides/sf-group-volunteer-requirements.md",
    "data/sf/volunteer-pathways.md",
    "data/nyc/volunteer-pathways.md",
    "templates/mission-dolores-contingency-communications.md",
    "templates/volunteer-response-mission-dolores.md",
    "escalation/escalation-materials-summary.md",
    "escalation/mission-dolores-conversion-spike-strategies.md",
    "escalation/sf-parks-escalation-outreach.md",
}

# Public agency phone numbers that are allowed anywhere.
PHONE_ALLOWED_NUMBERS = {
    "2123601310",
    "4157012311",
    "4158316328",
    "4158316884",
}

# Common binary extensions to skip outright.
BINARY_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "bmp",
    "tiff",
    "ico",
    "pdf",
    "zip",
    "gz",
    "tgz",
    "tar",
    "bz2",
    "xz",
    "7z",
    "mp3",
    "mp4",
    "mov",
    "avi",
    "wmv",
    "wav",
    "flac",
    "ogg",
    "webm",
    "mkv",
    "exe",
    "dll",
    "bin",
    "class",
    "jar",
    "woff",
    "woff2",
    "eot",
    "ttf",
    "otf",
}

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,}|localhost)\b"
)

# Matches US-style phone numbers, optionally prefixed with +1.
# Separators are limited to space or hyphen to avoid decimal/lat-long matches.
PHONE_REGEX = re.compile(
    r"""
    (?<!\d)
    (?:\+1[ -]?)?
    (?:\(\d{3}\)|\d{3})          # area code, with or without parentheses
    [ -]?                        # optional separator after area code
    \d{3}                        # prefix
    [ -]                         # required separator before line number
    \d{4}                        # line number
    (?!\d)
    """,
    re.VERBOSE,
)


class ScanResult:
    def __init__(self, path: str, line_number: int, redacted_line: str):
        self.path = path
        self.line_number = line_number
        self.redacted_line = redacted_line


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan for likely emails and US phone numbers. "
            "Allows only the domains: agentvillage.org, example.com, example.org, example.net, localhost, sfgov.org, parks.nyc.gov, sanitationfoundation.org. "
            "Exits 1 when PII is found."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Scan all tracked files (git ls-files).",
    )
    group.add_argument(
        "--paths-from-nul",
        metavar="FILE",
        help="Scan only paths from a NUL-delimited file (e.g., git diff --name-only -z).",
    )
    return parser.parse_args()


def is_allowed_domain(domain: str) -> bool:
    domain = domain.lower()
    for allowed in ALLOWLIST_DOMAINS:
        if domain == allowed or domain.endswith("." + allowed):
            return True
    return False


def is_binary_path(path: str) -> bool:
    _, ext = os.path.splitext(path)
    if ext:
        ext = ext.lstrip(".").lower()
        if ext in BINARY_EXTENSIONS:
            return True
    try:
        with open(path, "rb") as handle:
            chunk = handle.read(8000)
            if b"\0" in chunk:
                return True
    except OSError:
        return False
    return False


def git_tracked_files() -> List[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return [line for line in result.stdout.splitlines() if line.strip()]


def read_nul_delimited_file(path: str) -> List[str]:
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        raise RuntimeError(f"Unable to read paths file {path}: {exc}") from exc
    parts = raw.split(b"\0")
    paths: List[str] = []
    for part in parts:
        if not part:
            continue
        try:
            paths.append(part.decode("utf-8"))
        except UnicodeDecodeError:
            paths.append(part.decode("latin-1", errors="ignore"))
    return paths


def collect_paths(args: argparse.Namespace) -> List[str]:
    if args.all:
        return git_tracked_files()
    return read_nul_delimited_file(args.paths_from_nul)


def normalize_phone(value: str) -> str:
    return re.sub(r"\D", "", value)


def redact_line(line: str) -> str:
    redacted = EMAIL_REGEX.sub("<<EMAIL_REDACTED>>", line)
    redacted = PHONE_REGEX.sub("<<PHONE_REDACTED>>", redacted)
    return redacted.rstrip("\n")


def scan_line(line: str, path: str) -> bool:
    for match in EMAIL_REGEX.finditer(line):
        domain = match.group("domain")
        if not is_allowed_domain(domain):
            return True
    if path in PHONE_ALLOWED_PATHS:
        return False
    for phone_match in PHONE_REGEX.finditer(line):
        if normalize_phone(phone_match.group()) not in PHONE_ALLOWED_NUMBERS:
            return True
    return False


def scan_file(path: str) -> Tuple[List[ScanResult], List[str]]:
    findings: List[ScanResult] = []
    errors: List[str] = []

    if is_binary_path(path):
        return findings, errors

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for idx, line in enumerate(handle, start=1):
                if scan_line(line, path):
                    findings.append(ScanResult(path, idx, redact_line(line)))
    except OSError as exc:
        errors.append(f"{path}: {exc}")
    return findings, errors


def unique_existing_paths(paths: Sequence[str]) -> List[str]:
    seen = set()
    filtered: List[str] = []
    for path in paths:
        path = path.strip()
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            filtered.append(path)
    return filtered


def main() -> int:
    args = parse_args()
    try:
        candidate_paths = collect_paths(args)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    paths = unique_existing_paths(candidate_paths)
    findings: List[ScanResult] = []
    errors: List[str] = []

    for path in paths:
        file_findings, file_errors = scan_file(path)
        findings.extend(file_findings)
        errors.extend(file_errors)

    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        return 2

    if findings:
        print("PII scan detected potential emails/phone numbers:")
        for item in findings:
            print(f"{item.path}:{item.line_number}: {item.redacted_line}")
        print(
            f"Total findings: {len(findings)} "
            "(matches are redacted; only allowlisted domains are permitted)."
        )
        return 1

    print("PII scan passed: no disallowed emails or phone numbers found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
