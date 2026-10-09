"""Small allowlist for externally generated, self-contained profile SVGs."""

from pathlib import Path
import re
from xml.etree import ElementTree


SVG = "{http://www.w3.org/2000/svg}"
ALLOWED_TAGS = {"svg", "title", "desc", "rect", "path", "text", "g", "style"}
ALLOWED_ATTRIBUTES = {
    "width", "height", "viewBox", "x", "y", "rx", "ry", "fill", "stroke",
    "stroke-width", "d", "class", "id", "role", "aria-labelledby",
    "font-size", "font-weight", "font-family", "letter-spacing",
}
UNSAFE_CSS = re.compile(
    r"@import\b|@font-face\b|@namespace\b|url\s*\(|expression\s*\(|"
    r"javascript\s*:|data\s*:|behavior\s*:|-moz-binding\b|<",
    re.I,
)
UNSAFE_VALUE = re.compile(r"url\s*\(|(?:https?|data|javascript|file)\s*:|[\x00-\x08\x0b\x0c\x0e-\x1f]", re.I)


def validate_svg(path: Path, *, minimum: int = 500, maximum: int = 1_000_000) -> str:
    """Return UTF-8 SVG text only when it uses the approved local-only subset."""
    if not path.is_file() or not (minimum < path.stat().st_size < maximum):
        raise ValueError(f"Missing, empty, or oversized SVG: {path}")
    content = path.read_text(encoding="utf-8")
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", content, re.I):
        raise ValueError(f"DTD or entity is not allowed: {path}")
    remainder = content.lstrip()
    if remainder.startswith("<?xml"):
        marker = remainder.find("?>")
        if marker < 0:
            raise ValueError(f"Malformed XML declaration: {path}")
        remainder = remainder[marker + 2:]
    if "<?" in remainder:
        raise ValueError(f"Processing instruction is not allowed: {path}")
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Invalid SVG XML: {path}") from exc
    if root.tag != SVG + "svg":
        raise ValueError(f"Root is not an SVG element: {path}")
    for element in root.iter():
        if element.tag not in {SVG + tag for tag in ALLOWED_TAGS}:
            raise ValueError(f"Disallowed SVG element {element.tag}: {path}")
        for attribute, value in element.attrib.items():
            if attribute not in ALLOWED_ATTRIBUTES or UNSAFE_VALUE.search(value):
                raise ValueError(f"Disallowed SVG attribute or reference {attribute}: {path}")
        if element.tag == SVG + "style" and UNSAFE_CSS.search(element.text or ""):
            raise ValueError(f"Disallowed SVG CSS: {path}")
    return content
