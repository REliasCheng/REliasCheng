"""Validate a generated public metrics artifact without modifying the repo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree


def validate(directory: Path) -> None:
    data = json.loads((directory / "telemetry.json").read_text(encoding="utf-8"))
    if data["public_repositories"] < 1 or data["source"] != "GitHub public REST API":
        raise ValueError("Invalid repository inventory or data source")
    if len(data["ci"]) != 5:
        raise ValueError("Five monitored host workflows are expected")
    for entry in data["ci"]:
        if entry["status"] not in {"PASS", "FAIL", "PENDING", "STALE", "NOT VERIFIED", "UNAVAILABLE"}:
            raise ValueError(f"Unknown CI status: {entry['status']}")
        if entry["status"] == "PASS" and not entry["sha"]:
            raise ValueError("PASS requires a current-main SHA")
    for theme in ("dark", "light"):
        path = directory / f"telemetry-{theme}.svg"
        root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
        if not root.tag.endswith("svg"):
            raise ValueError(f"Not SVG: {path}")
        print(f"Validated {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate(args.directory)
