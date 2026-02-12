#!/usr/bin/env python3
"""Audit evidence directory for cleanup events and summarize findings."""

import re
from pathlib import Path
from typing import List, Optional, Tuple

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".tif", ".tiff"}


def count_files(folder: Path) -> int:
    """Count files directly within a folder."""
    return sum(1 for entry in folder.iterdir() if entry.is_file())


def collect_events(base: Path) -> List[Tuple[str, str, Path]]:
    """Return list of (location, date, path) tuples for events."""
    events = []
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}$")

    def looks_like_date(name: str) -> bool:
        return bool(date_pattern.match(name))

    def has_event_content(directory: Path) -> bool:
        """Heuristic to determine if a folder is an event when flat."""
        for child in directory.iterdir():
            if child.is_file():
                if child.suffix.lower() in IMAGE_EXTENSIONS:
                    return True
                if child.name.lower() in {"report.md", "readme.md", "retrospective.md"}:
                    return True
            if child.is_dir() and child.name.lower() in {"before", "during", "after"}:
                return True
        return False

    def parse_flat_event(name: str) -> Tuple[str, str]:
        match = re.match(r"(.+)-(\d{4})-(\d{2})-(\d{2})$", name)
        if match:
            location, year, month, day = match.groups()
            return location, f"{year}-{month}-{day}"
        return name, "unknown"

    for candidate in sorted(p for p in base.iterdir() if p.is_dir()):
        subdirs = [d for d in candidate.iterdir() if d.is_dir()]
        date_subdirs = sorted(d for d in subdirs if looks_like_date(d.name))

        if date_subdirs:
            for date_dir in date_subdirs:
                events.append((candidate.name, date_dir.name, date_dir))
            continue

        if has_event_content(candidate):
            location, date = parse_flat_event(candidate.name)
            events.append((location, date, candidate))

    return events


def print_report(events: List[Tuple[str, str, Path]], base: Path) -> None:
    if not events:
        print(f"No events found under '{base}'.")
        return

    print(f"Found {len(events)} event(s) under '{base}':")
    for location, date, event_dir in events:
        before_dir = event_dir / "before"
        during_dir = event_dir / "during"
        after_dir = event_dir / "after"
        retrospective_file = event_dir / "retrospective.md"

        def find_report_file(directory: Path) -> Optional[Path]:
            for name in ("report.md", "README.md", "readme.md"):
                candidate = directory / name
                if candidate.is_file():
                    return candidate
            return None

        def dir_status(directory: Path) -> Tuple[bool, int]:
            exists = directory.is_dir()
            return exists, count_files(directory) if exists else 0

        def count_images(directory: Path) -> int:
            return sum(
                1
                for entry in directory.iterdir()
                if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS
            )

        before_exists, before_count = dir_status(before_dir)
        during_exists, during_count = dir_status(during_dir)
        after_exists, after_count = dir_status(after_dir)

        before_images = count_images(before_dir) if before_exists else 0
        during_images = count_images(during_dir) if during_exists else 0
        after_images = count_images(after_dir) if after_exists else 0
        root_images = sum(
            1
            for entry in event_dir.iterdir()
            if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS
        )

        report_file = find_report_file(event_dir)

        print(f"- {location} / {date}")
        print("  Directories:")
        print(
            f"    before: {'present' if before_exists else 'missing'} "
            f"(files: {before_count}, images: {before_images})"
        )
        print(
            f"    during: {'present' if during_exists else 'missing'} "
            f"(files: {during_count}, images: {during_images})"
        )
        print(
            f"    after:  {'present' if after_exists else 'missing'} "
            f"(files: {after_count}, images: {after_images})"
        )
        print("  Files:")
        report_label = f"found ({report_file.name})" if report_file else "missing"
        print(f"    report:           {report_label}")
        print(f"    retrospective.md: {'found' if retrospective_file.is_file() else 'missing'}")
        print("  Images:")
        print(
            f"    root:   {'found' if root_images else 'none'} "
            f"(images in event folder root: {root_images})"
        )
        print(
            "    detail: "
            f"before={before_images}, during={during_images}, after={after_images}"
        )
        print()


def main() -> None:
    base = Path("evidence")
    if not base.exists() or not base.is_dir():
        print(f"Evidence directory not found at '{base}'.")
        return

    events = collect_events(base)
    print_report(events, base)


if __name__ == "__main__":
    main()
