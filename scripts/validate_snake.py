"""Check preview contribution SVGs before they are considered for README use."""

from __future__ import annotations

import argparse
from pathlib import Path
from svg_safety import validate_svg


def validate(directory: Path) -> None:
    for theme in ("dark", "light"):
        path = directory / f"snake-{theme}.svg"
        validate_svg(path)
        print(f"Validated {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate(args.directory)
