"""Derive a still contribution graph from verified public snk output, not drawn data."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from validate_snake import validate


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "assets/preview"
SVG = "{http://www.w3.org/2000/svg}"


def prepare(directory: Path = PREVIEW) -> None:
    validate(directory)
    ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    for theme in ("dark", "light"):
        source = directory / f"snake-{theme}.svg"
        root = ElementTree.fromstring(source.read_text(encoding="utf-8"))
        for node in list(root):
            classes = node.get("class", "").split()
            if "s" in classes or "u" in classes:
                root.remove(node)
        ElementTree.SubElement(root, SVG + "style").text = ".c { animation: none !important; }"
        for node in root.findall(SVG + "title"):
            node.text = f"Static REliasCheng contribution graph ({theme}) from public GitHub data"
        target = directory / f"contribution-static-{theme}.svg"
        target.write_text(ElementTree.tostring(root, encoding="unicode") + "\n", encoding="utf-8")
        ElementTree.parse(target)
        print(f"Derived {target} from validated real contribution graph")


if __name__ == "__main__":
    prepare()
