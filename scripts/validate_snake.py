"""Check preview contribution SVGs before they are considered for README use."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from xml.etree import ElementTree


UNSAFE = re.compile(
    r'<\s*(?:script|foreignObject|image)\b|(?:href|src)\s*=\s*["\'](?:https?:|data:|javascript:)|url\(\s*["\']?https?:',
    re.I,
)


def validate(directory: Path) -> None:
    for theme in ("dark", "light"):
        path = directory / f"snake-{theme}.svg"
        if not path.is_file() or not (500 < path.stat().st_size < 1_000_000):
            raise ValueError(f"Missing, empty, or oversized contribution SVG: {path}")
        content = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(content)
        if not root.tag.endswith("svg") or UNSAFE.search(content):
            raise ValueError(f"Unsafe or invalid contribution SVG: {path}")
        print(f"Validated {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    validate(args.directory)
