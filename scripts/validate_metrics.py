"""Validate a generated public metrics artifact without modifying the repo."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from xml.etree import ElementTree

from validate_snake import UNSAFE
from generate_metrics import MONITORED, OWNER, render_svg


def validate(directory: Path) -> None:
    data = json.loads((directory / "telemetry.json").read_text(encoding="utf-8"))
    if data.get("owner") != OWNER:
        raise ValueError("Metrics owner mismatch")
    try:
        datetime.strptime(data["refreshed_utc"], "%Y-%m-%d %H:%M UTC")
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Metrics require an explicit UTC refresh timestamp") from exc
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
        if not path.is_file() or not (500 < path.stat().st_size < 1_000_000):
            raise ValueError(f"Missing, empty, or oversized metrics SVG: {path}")
        content = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(content)
        if not root.tag.endswith("svg") or UNSAFE.search(content):
            raise ValueError(f"Unsafe or invalid metrics SVG: {path}")
        if content != render_svg(data, theme) + "\n":
            raise ValueError(f"Metrics SVG does not match its JSON source: {path}")
        print(f"Validated {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate(args.directory)
