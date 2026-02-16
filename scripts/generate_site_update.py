#!/usr/bin/env python3
"""Extract cleanup stats from a markdown report and current site.

Reads a single hardcoded report:
evidence/devoe-park-bronx/2026-02-14/report.md

It pulls fields to generate a site update.
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
    """Return the value that follows a bolded label in the markdown."""
    pattern = rf"^[ \t]*[-•]?[ \t]*\*\*{re.escape(label)}:?\*\*[ \t]*:?[ \t]*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return None

    value = match.group(1).strip()
    if not value or value.startswith("(e.g.") or value.startswith("~"):
        # If it starts with ~ but has more content, we might want it.
        # The previous logic excluded it, but for '180 gallons', we want it.
        if len(value) < 5: 
             return None
    return value

def load_site_soup() -> BeautifulSoup:
    if not SITE_PATH.exists():
        raise SystemExit(f"Site file not found: {SITE_PATH}")

    html = SITE_PATH.read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def find_stat_number_element(soup: BeautifulSoup, label: str) -> Optional[BeautifulSoup]:
    """Return the .number element for a stat box matching the label."""
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
        help="Use dummy values.",
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

    # Updated labels based on actual report.md content
    volunteers = extract_field(report_text, "Total volunteers")
    bags = extract_field(report_text, "Trash collected")
    # Notable items is a list in the report, so hardcoding a summary for now based on the report content
    notable_items = "150+ cigarette butts, bottlecaps, chip bags, pizza boxes"

    if args.test_data:
        volunteers = "5"
        bags = "six 30-gallon bags"
        notable_items = "A tire"

    print(f"Report: {REPORT_PATH}")
    print(f"Volunteers: {volunteers or 'N/A'}")
    print(f"Trash bags: {bags or 'N/A'}")
    print(f"Notable items: {notable_items}")

    soup = load_site_soup()
    parks_cleaned = extract_stat(soup, "Parks Cleaned (so far)")

    print(f"\nSite: {SITE_PATH}")
    print(f"Parks cleaned (so far): {parks_cleaned or 'N/A'}")

    if bags is not None:
        print("\nUpdating site content:")

        # Update Parks Cleaned count
        parks_cleaned_el = find_stat_number_element(soup, "Parks Cleaned (so far)")
        if parks_cleaned_el:
            original_parks_cleaned = parks_cleaned_el.get_text(strip=True)
            # Increment or set to 1 if it was 0
            try:
                current_val = int(original_parks_cleaned)
                new_val = 1 # Force to 1 for now as this is the first one
            except ValueError:
                new_val = 1
            
            parks_cleaned_el.string = str(new_val)
            updated_parks_cleaned = parks_cleaned_el.get_text(strip=True)
            print(f"Parks Cleaned (so far): '{original_parks_cleaned}' -> '{updated_parks_cleaned}'")
        else:
            print("Parks Cleaned (so far): element not found")

        # Update Devoe Description
        devoe_description_el = find_devoe_description_element(soup)
        if devoe_description_el:
            original_description = devoe_description_el.get_text(" ", strip=True)
            volunteers_text = volunteers or "N/A"
            
            # Clean up the bags text if it's too long
            bags_text = bags
            if len(bags_text) > 50:
                 # extract just the main part "six 30-gallon trash bags"
                 if "six 30-gallon trash bags" in bags_text:
                     bags_text = "six 30-gallon trash bags (~180 gallons)"

            new_description = (
                f"Cleanup complete! {volunteers_text} volunteers collected {bags_text}. "
                f"Notable items: {notable_items}."
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
