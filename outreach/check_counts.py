#!/usr/bin/env python3
"""
Check claimed vs actual character counts for post copy blocks.

The script scans feb13-posting-copy-blocks.md for patterns like:
**Post A1 — Description (267 chars):**
followed by a fenced code block. It compares the claimed count,
actual content length, and the platform limit for the post ID.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple


POST_LIMITS: Dict[str, int] = {
    # 300 char platforms
    "A1": 300,
    "A2": 300,
    "C1": 300,
    "D1": 300,
    "D2": 300,
    # 500 char platforms
    "A3": 500,
    "C2": 500,
    "D3": 500,
    "D4": 500,
    # LinkedIn
    "B1": 3000,
}

PATTERN = re.compile(r"\*\*Post\s+([A-Z]\d)\s+—.*\(([\d,]+)\s*chars?\)\s*:\*\*")


def parse_posts(markdown: str) -> List[Tuple[str, int, str]]:
    """
    Return a list of tuples (post_id, claimed_count, content).
    """
    lines = markdown.splitlines()
    results: List[Tuple[str, int, str]] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        match = PATTERN.search(line)
        if not match:
            i += 1
            continue

        post_id = match.group(1)
        claimed = int(match.group(2).replace(",", ""))

        # Find the opening fence following the matched line.
        j = i + 1
        while j < len(lines) and lines[j].strip() != "```":
            j += 1
        if j >= len(lines):
            raise ValueError(f"No opening code fence found for post {post_id}")

        # Collect content until the closing fence.
        content_lines: List[str] = []
        k = j + 1
        while k < len(lines) and lines[k].strip() != "```":
            content_lines.append(lines[k])
            k += 1
        if k >= len(lines):
            raise ValueError(f"No closing code fence found for post {post_id}")

        content = "\n".join(content_lines)
        results.append((post_id, claimed, content))
        i = k + 1

    return results


def format_table(rows: List[Tuple[str, int, int, str, str]]) -> str:
    """
    Format rows into a simple aligned text table.
    Each row: (id, claimed, actual, limit_str, flags)
    """
    headers = ("ID", "Claimed", "Actual", "Limit", "Flags")
    col_widths = [
        max(len(headers[0]), *(len(r[0]) for r in rows)),
        max(len(headers[1]), *(len(str(r[1])) for r in rows)),
        max(len(headers[2]), *(len(str(r[2])) for r in rows)),
        max(len(headers[3]), *(len(r[3]) for r in rows)),
        max(len(headers[4]), *(len(r[4]) for r in rows)),
    ]

    def fmt_row(row: Tuple[str, int, int, str, str]) -> str:
        return (
            f"{row[0]:<{col_widths[0]}}  "
            f"{row[1]:>{col_widths[1]}}  "
            f"{row[2]:>{col_widths[2]}}  "
            f"{row[3]:>{col_widths[3]}}  "
            f"{row[4]:<{col_widths[4]}}"
        )

    header_line = (
        f"{headers[0]:<{col_widths[0]}}  "
        f"{headers[1]:>{col_widths[1]}}  "
        f"{headers[2]:>{col_widths[2]}}  "
        f"{headers[3]:>{col_widths[3]}}  "
        f"{headers[4]:<{col_widths[4]}}"
    )
    divider = "-".join("-" * w for w in col_widths)
    lines = [header_line, divider]
    lines.extend(fmt_row(r) for r in rows)
    return "\n".join(lines)


def main() -> None:
    md_path = Path(__file__).resolve().parent / "feb13-posting-copy-blocks.md"
    markdown = md_path.read_text(encoding="utf-8")

    posts = parse_posts(markdown)
    rows: List[Tuple[str, int, int, str, str]] = []
    warnings: List[str] = []

    for post_id, claimed, content in posts:
        actual = len(content)
        limit = POST_LIMITS.get(post_id)
        limit_str = str(limit) if limit is not None else "—"
        flags: List[str] = []

        if limit is not None and actual > limit:
            flags.append("over limit")
            warnings.append(
                f"WARNING: {post_id} over limit ({actual} > {limit})"
            )

        if actual != claimed:
            flags.append("claimed mismatch")
            warnings.append(
                f"WARNING: {post_id} claimed {claimed}, actual {actual}"
            )

        rows.append((post_id, claimed, actual, limit_str, ", ".join(flags) or "ok"))

    print(format_table(rows))
    if warnings:
        print("\n".join(warnings))


if __name__ == "__main__":
    main()
