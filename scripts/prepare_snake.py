"""Frame a verified Platane/snk preview artifact in SIGNALCORE colors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree

from validate_snake import validate


ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/brand/tokens.json").read_text(encoding="utf-8"))


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
        tag_end = text.index(">") + 1
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
