#!/usr/bin/env python3
"""Generate simple PNG charts from the repo's 311 CSV extracts.

Outputs go to assets/charts/.

Design goals:
- Simple, readable, low-dependency (matplotlib + pandas)
- Works headless (Agg backend)
- Deterministic filenames suitable for embedding in README/Issues
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "assets" / "charts"


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def _barh_counts(series: pd.Series, title: str, xlabel: str, outpath: Path, top_n: int = 12) -> None:
    counts = series.fillna("(blank)").astype(str).value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, 0.45 * max(6, len(counts))))
    counts.sort_values().plot(kind="barh", ax=ax, color="#4a7c28")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    for i, v in enumerate(counts.sort_values()):
        ax.text(v + max(0.02 * counts.max(), 0.1), i, str(v), va="center", fontsize=9)
    ax.grid(axis="x", alpha=0.25)
    _save(fig, outpath)


def _pie_counts(series: pd.Series, title: str, outpath: Path, min_pct_label: float = 0.06) -> None:
    counts = series.fillna("(blank)").astype(str).value_counts()

    def autopct(pct):
        return f"{pct:.0f}%" if pct >= (min_pct_label * 100) else ""

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.pie(counts.values, labels=counts.index, autopct=autopct, startangle=90, textprops={"fontsize": 9})
    ax.set_title(title)
    ax.axis("equal")
    _save(fig, outpath)


def _daily_counts(dt: pd.Series, title: str, outpath: Path) -> None:
    # Parse timestamps robustly; keep date only.
    d = pd.to_datetime(dt, errors="coerce", utc=True).dt.date
    daily = pd.Series(d).value_counts().sort_index()

    # Fill gaps for a continuous x-axis.
    if len(daily) == 0:
        return

    idx = pd.date_range(start=min(daily.index), end=max(daily.index), freq="D").date
    daily = daily.reindex(idx, fill_value=0)

    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(list(daily.index), daily.values, marker="o", linewidth=2, color="#2d5016")
    ax.fill_between(list(daily.index), daily.values, alpha=0.12, color="#2d5016")
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("311 requests")
    ax.grid(alpha=0.25)
    fig.autofmt_xdate(rotation=30, ha="right")
    _save(fig, outpath)


@dataclass(frozen=True)
class DatasetSpec:
    slug: str
    csv_path: Path
    dt_col: str
    category_col: str
    status_col: str
    title_prefix: str


def generate(spec: DatasetSpec) -> list[Path]:
    df = pd.read_csv(spec.csv_path)

    outputs: list[Path] = []

    # 1) Daily timeline
    out = OUTDIR / f"{spec.slug}_daily_counts.png"
    _daily_counts(df[spec.dt_col], f"{spec.title_prefix}: requests per day (last 30 days extract)", out)
    outputs.append(out)

    # 2) Category/service breakdown
    out = OUTDIR / f"{spec.slug}_categories.png"
    _barh_counts(
        df[spec.category_col],
        f"{spec.title_prefix}: top categories (last 30 days extract)",
        xlabel="Count",
        outpath=out,
        top_n=12,
    )
    outputs.append(out)

    # 3) Status breakdown
    out = OUTDIR / f"{spec.slug}_status.png"
    _pie_counts(df[spec.status_col], f"{spec.title_prefix}: status breakdown (last 30 days extract)", out)
    outputs.append(out)

    return outputs


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    specs = [
        DatasetSpec(
            slug="sf_mission_dolores_last30",
            csv_path=ROOT / "data" / "sf" / "311_mission_dolores_last30.csv",
            dt_col="requested_datetime",
            category_col="service_name",
            status_col="status_description",
            title_prefix="SF — Mission Dolores Park area",
        ),
        DatasetSpec(
            slug="nyc_devoe_park_last30",
            csv_path=ROOT / "data" / "nyc" / "311_devoe_park_area_last30.csv",
            dt_col="created_date",
            category_col="complaint_type",
            status_col="status",
            title_prefix="NYC — Devoe Park area (Bronx)",
        ),
    ]

    all_out = []
    for s in specs:
        if not s.csv_path.exists():
            raise SystemExit(f"Missing CSV: {s.csv_path}")
        all_out.extend(generate(s))

    # Write a small manifest to make it easy to see what was generated.
    manifest = OUTDIR / "MANIFEST.txt"
    with manifest.open("w", encoding="utf-8") as f:
        for p in all_out:
            f.write(str(p.relative_to(ROOT)) + "\n")

    print(f"Wrote {len(all_out)} charts to {OUTDIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
