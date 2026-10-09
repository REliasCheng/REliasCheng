"""Validate a generated public metrics artifact without modifying the repo."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from svg_safety import validate_svg
from generate_metrics import MONITORED, OWNER, render_svg


MAX_SNAPSHOT_AGE = timedelta(hours=48)
MAX_FUTURE_SKEW = timedelta(minutes=5)


def snapshot_freshness(value: str, now: datetime) -> str:
    """Classify API collection time; historical display may be stale, publishing may not."""
    if now.tzinfo is None:
        raise ValueError("Freshness comparison requires timezone-aware current time")
    try:
        collected = datetime.strptime(value, "%Y-%m-%d %H:%M UTC").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as exc:
        raise ValueError("Metrics require an explicit UTC refresh timestamp") from exc
    age = now.astimezone(timezone.utc) - collected
    if age < -MAX_FUTURE_SKEW:
        return "FUTURE"
    if age > MAX_SNAPSHOT_AGE:
        return "STALE"
    return "FRESH"


def validate(directory: Path, *, now: datetime | None = None) -> None:
    data = json.loads((directory / "telemetry.json").read_text(encoding="utf-8"))
    if data.get("owner") != OWNER:
        raise ValueError("Metrics owner mismatch")
    if snapshot_freshness(data["refreshed_utc"], now or datetime.now(timezone.utc)) == "FUTURE":
        raise ValueError("Metrics refresh timestamp is unreasonably in the future")
    if data["public_repositories"] < 1 or data["source"] != "GitHub public REST API":
        raise ValueError("Invalid repository inventory or data source")
    expected = {(repository, label, scope) for label, repository, _, scope in MONITORED}
    actual = [(entry["repository"], entry["label"], entry["scope"]) for entry in data["ci"]]
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("CI rows must exactly match the five unique monitored repositories, labels and scopes")
    for entry in data["ci"]:
        if entry["status"] not in {"PASS", "FAIL", "PENDING", "STALE", "NOT VERIFIED", "UNAVAILABLE"}:
            raise ValueError(f"Unknown CI status: {entry['status']}")
        if entry["status"] != "UNAVAILABLE" and not entry["sha"]:
            raise ValueError("Available CI evidence requires a current-main SHA")
    for theme in ("dark", "light"):
        path = directory / f"telemetry-{theme}.svg"
        content = validate_svg(path)
        if content != render_svg(data, theme) + "\n":
            raise ValueError(f"Metrics SVG does not match its JSON source: {path}")
        print(f"Validated {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate(args.directory)
