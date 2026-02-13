#!/usr/bin/env python3
"""Extract cleanup stats from a markdown report and current site.

Reads a single hardcoded report:
evidence/devoe-park-bronx/2026-02-14/report.md

It pulls three fields:
- Approximate total volunteers who actually showed up (humans)
- Number of bags
- Notable items

Parsing is intentionally light-weight (regex over the markdown) so it
can tolerate small formatting changes. The extracted values are printed
to stdout for inspection or for piping into other tools later.

The script also inspects the static site (park-cleanup-site/index.html)
using BeautifulSoup to pull current stats like "Parks Cleaned (so far)"
and the Devoe Park evidence box.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup  # type: ignore


REPO_ROOT = Path(__file__).parent.parent
REPORT_PATH = REPO_ROOT / "evidence" / "devoe-park-bronx" / "2026-02-14" / "report.md"
SITE_PATH = REPO_ROOT / "park-cleanup-site" / "index.html"


def extract_field(text: str, label: str) -> Optional[str]:
    """Return the value that follows a bolded label in the markdown.

    Matches patterns like:
      - **Label:** value here
      - **Label** value here
    """
    pattern = rf"^[ \t]*[-•]?[ \t]*\*\*{re.escape(label)}:?\*\*[ \t]*:?[ \t]*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return None

    value = match.group(1).strip()
    if not value or value.startswith("(e.g.") or value.startswith("~"):
        # Treat placeholders/empty guidance as missing.
        return None
    return value


def load_site_soup() -> BeautifulSoup:
    if not SITE_PATH.exists():
        raise SystemExit(f"Site file not found: {SITE_PATH}")

    html = SITE_PATH.read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def find_stat_number_element(soup: BeautifulSoup, label: str) -> Optional[BeautifulSoup]:
    """Return the `.number` element for a stat box matching the label."""
    label_lower = label.lower()
    for stat in soup.select(".stat-box"):
        label_el = stat.select_one(".label")
        if not label_el:
            continue
        if label_el.get_text(strip=True).lower() != label_lower:
            continue

        return stat.select_one(".number")
    return None


def extract_stat(soup: BeautifulSoup, label: str) -> Optional[str]:
    """Return the number value for a stat box matching the label."""
    label_lower = label.lower()
    for stat in soup.select(".stat-box"):
        label_el = stat.select_one(".label")
        if not label_el:
            continue
        if label_el.get_text(strip=True).lower() != label_lower:
            continue

        number_el = stat.select_one(".number")
        return number_el.get_text(strip=True) if number_el else None
    return None


def extract_devoe_evidence(soup: BeautifulSoup) -> Optional[tuple[str, Optional[str]]]:
    """Locate the Devoe Park evidence box and return heading + description."""
    before_after_header = soup.find("h2", string=lambda s: s and "Before" in s and "After" in s)
    section = before_after_header.find_parent("section") if before_after_header else None
    if not section:
        return None

    for box in section.find_all("div", class_="evidence-box"):
        if "devoe park" not in box.get_text(" ", strip=True).lower():
            continue

        heading_el = box.find("strong")
        heading = heading_el.get_text(" ", strip=True) if heading_el else "Devoe Park"

        paragraphs = box.find_all("p")
        description = paragraphs[1].get_text(" ", strip=True) if len(paragraphs) > 1 else None
        return heading, description

    return None


def find_devoe_description_element(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """Return the second paragraph of the Devoe Park evidence box."""
    before_after_header = soup.find("h2", string=lambda s: s and "Before" in s and "After" in s)
    section = before_after_header.find_parent("section") if before_after_header else None
    if not section:
        return None

    for box in section.find_all("div", class_="evidence-box"):
        if "devoe park" not in box.get_text(" ", strip=True).lower():
            continue

        paragraphs = box.find_all("p")
        if len(paragraphs) > 1:
            return paragraphs[1]
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract cleanup stats and preview site updates.")
    parser.add_argument(
        "--test-data",
        action="store_true",
        help="Use dummy values (volunteers=5, bags=10, notable items='A tire').",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated site HTML back to park-cleanup-site/index.html.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not REPORT_PATH.exists():
        raise SystemExit(f"Report file not found: {REPORT_PATH}")

    report_text = REPORT_PATH.read_text(encoding="utf-8")

    volunteers = extract_field(report_text, "Approximate total volunteers who actually showed up (humans)")
    bags = extract_field(report_text, "Number of bags")
    notable_items = extract_field(report_text, "Notable items")

    if args.test_data:
        volunteers = "5"
        bags = "10"
        notable_items = "A tire"

    print(f"Report: {REPORT_PATH}")
    print(f"Volunteers: {volunteers or 'N/A'}")
    print(f"Trash bags: {bags or 'N/A'}")
    print(f"Notable items: {notable_items or 'N/A'}")

    soup = load_site_soup()
    parks_cleaned = extract_stat(soup, "Parks Cleaned (so far)")
    devoe_evidence = extract_devoe_evidence(soup)

    print(f"\nSite: {SITE_PATH}")
    print(f"Parks cleaned (so far): {parks_cleaned or 'N/A'}")
    if devoe_evidence:
        heading, description = devoe_evidence
        print("Devoe Park evidence box:")
        print(f"  Heading: {heading}")
        if description:
            print(f"  Description: {description}")
        else:
            print("  Description: N/A")
    else:
        print("Devoe Park evidence box: not found")

    if bags is not None:
        print("\nUpdating site content:")

        parks_cleaned_el = find_stat_number_element(soup, "Parks Cleaned (so far)")
        if parks_cleaned_el:
            original_parks_cleaned = parks_cleaned_el.get_text(strip=True)
            parks_cleaned_el.string = "1"
            updated_parks_cleaned = parks_cleaned_el.get_text(strip=True)
            print(f"Parks Cleaned (so far): '{original_parks_cleaned}' -> '{updated_parks_cleaned}'")
        else:
            print("Parks Cleaned (so far): element not found")

        devoe_description_el = find_devoe_description_element(soup)
        if devoe_description_el:
            original_description = devoe_description_el.get_text(" ", strip=True)
            volunteers_text = volunteers or "N/A"
            notable_items_text = notable_items or "N/A"
            new_description = (
                f"Cleanup complete! {volunteers_text} volunteers collected {bags}. "
                f"Notable items: {notable_items_text}."
            )
            devoe_description_el.string = new_description
            print(f"Devoe Park description: '{original_description}' -> '{new_description}'")
        else:
            print("Devoe Park description: element not found")

        if args.write:
            SITE_PATH.write_text(str(soup), encoding="utf-8")
            print(f"\nWrote updated HTML to {SITE_PATH}")


if __name__ == "__main__":
    main()
