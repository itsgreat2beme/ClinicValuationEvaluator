from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Iterable

from .scoring import ClinicRecord, score_records


FIELDNAMES = [
    "name",
    "area",
    "population",
    "median_income",
    "wellness_interest",
    "competitor_count",
    "avg_rating",
    "review_count",
    "avg_price",
    "parking_score",
    "transit_score",
]


def parse_float(row: dict[str, str], field: str) -> float:
    try:
        return float(row[field])
    except KeyError as exc:
        raise ValueError(f"Missing required column: {field}") from exc
    except ValueError as exc:
        raise ValueError(f"Column {field} must be numeric for row {row.get('name', '<unknown>')}") from exc


def read_records(path: Path) -> list[ClinicRecord]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            ClinicRecord(
                name=row["name"],
                area=row["area"],
                population=parse_float(row, "population"),
                median_income=parse_float(row, "median_income"),
                wellness_interest=parse_float(row, "wellness_interest"),
                competitor_count=parse_float(row, "competitor_count"),
                avg_rating=parse_float(row, "avg_rating"),
                review_count=parse_float(row, "review_count"),
                avg_price=parse_float(row, "avg_price"),
                parking_score=parse_float(row, "parking_score"),
                transit_score=parse_float(row, "transit_score"),
            )
            for row in reader
        ]


def write_rows(path: Path, rows: Iterable[dict[str, float | str]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            handle.write("")
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def analyze(args: argparse.Namespace) -> None:
    records = read_records(Path(args.input))
    scored = score_records(records)
    write_rows(Path(args.output), scored)
    print(f"Wrote {len(scored)} ranked rows to {args.output}")
    if scored:
        top = scored[0]
        print(f"Top opportunity: {top['name']} in {top['area']} ({top['opportunity_score']})")


def fetch_places(args: argparse.Namespace) -> None:
    try:
        import requests
    except ImportError as exc:
        raise SystemExit("Install dependencies with: pip install -r requirements.txt") from exc

    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set GOOGLE_PLACES_API_KEY before using fetch-places.")

    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={
            "query": f"IV therapy clinic near {args.area}",
            "key": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    rows = []
    for place in payload.get("results", []):
        rows.append(
            {
                "name": place.get("name", ""),
                "area": args.area,
                "population": "",
                "median_income": "",
                "wellness_interest": "",
                "competitor_count": len(payload.get("results", [])),
                "avg_rating": place.get("rating", ""),
                "review_count": place.get("user_ratings_total", ""),
                "avg_price": "",
                "parking_score": "",
                "transit_score": "",
            }
        )

    write_rows(Path(args.output), rows)
    print(f"Wrote {len(rows)} Google Places rows to {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate IV therapy clinic opportunities in an area.")
    subparsers = parser.add_subparsers(required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Rank clinic opportunities from a CSV file.")
    analyze_parser.add_argument("--input", required=True, help="Input clinic CSV path.")
    analyze_parser.add_argument("--output", required=True, help="Output ranked CSV path.")
    analyze_parser.set_defaults(func=analyze)

    fetch_parser = subparsers.add_parser("fetch-places", help="Fetch IV clinic listings from Google Places.")
    fetch_parser.add_argument("--area", required=True, help='Area to search, for example "Austin, TX".')
    fetch_parser.add_argument("--output", required=True, help="Output CSV path.")
    fetch_parser.set_defaults(func=fetch_places)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
