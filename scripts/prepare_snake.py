"""Frame a verified Platane/snk preview artifact in SIGNALCORE colors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree

from validate_snake import validate


ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/brand/tokens.json").read_text(encoding="utf-8"))


def root_open_end(text: str) -> int:
    """Find the end of the real root tag, not an XML declaration or quoted >."""
    position = 0
    while True:
        while position < len(text) and text[position].isspace():
            position += 1
        if text.startswith("<?xml", position):
            marker = text.find("?>", position)
            if marker < 0:
                raise ValueError("Unclosed XML declaration")
            position = marker + 2
        elif text.startswith("<!--", position):
            marker = text.find("-->", position)
            if marker < 0:
                raise ValueError("Unclosed leading XML comment")
            position = marker + 3
        else:
            break
    if not text.startswith("<svg", position) or text[position + 4:position + 5] not in {" ", "\t", "\n", "\r", ">"}:
        raise ValueError("Expected an unprefixed SVG root")
    quote = None
    for index in range(position + 4, len(text)):
        char = text[index]
        if quote:
            if char == quote:
                quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == ">":
            return index + 1
    raise ValueError("Unclosed SVG root tag")


def prepare(source: Path, output: Path) -> None:
    validate(source)
    output.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        text = (source / f"snake-{theme}.svg").read_text(encoding="utf-8")
        svg = ElementTree.fromstring(text)
        x, y, width, height = svg.attrib["viewBox"].split()
        t = TOKENS[theme]
        addition = (
            f'<title>SIGNALCORE real GitHub contribution animation for REliasCheng ({theme})</title>'
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" '
            f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="2"/>'
            '<style>@media (prefers-reduced-motion: reduce) '
            '{ .c, .s, .u { animation: none !important; } }</style>'
        )
        tag_end = root_open_end(text)
        framed = text[:tag_end] + addition + text[tag_end:]
        ElementTree.fromstring(framed)
        target = output / f"snake-{theme}.svg"
        target.write_text(framed + "\n", encoding="utf-8")
        print(f"Prepared {target} from verified public-contribution artifact")
    validate(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets/preview")
    args = parser.parse_args()
    prepare(args.source, args.output_dir)
