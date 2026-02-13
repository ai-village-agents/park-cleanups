from pathlib import Path

from audit_evidence import collect_events


def test_collect_events_with_nested_structure(tmp_path: Path) -> None:
    base = tmp_path / "evidence"
    location_dir = base / "central-park"
    date_dir = location_dir / "2024-01-15"

    date_dir.mkdir(parents=True)

    events = collect_events(base)

    assert events == [("central-park", "2024-01-15", date_dir)]


def test_collect_events_with_empty_directories(tmp_path: Path) -> None:
    base = tmp_path / "evidence"
    (base / "placeholder").mkdir(parents=True)

    events = collect_events(base)

    assert events == []


def test_collect_events_ignores_non_event_directories(tmp_path: Path) -> None:
    base = tmp_path / "evidence"
    base.mkdir()

    event_dir = base / "lakeview-2024-05-10"
    event_dir.mkdir()
    (event_dir / "before").mkdir()
    (event_dir / "before" / "photo.jpg").touch()

    (base / "docs").mkdir()
    (base / "temp").mkdir()
    other = base / "misc"
    (other / "notes").mkdir(parents=True)
    (other / "notes" / "todo.txt").touch()

    events = collect_events(base)

    assert events == [("lakeview", "2024-05-10", event_dir)]
