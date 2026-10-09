"""Validate the preview's project catalog, README paths, and self-contained SVGs."""

from __future__ import annotations

import json
from pathlib import Path
import re
from urllib.parse import unquote
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROJECTS = ROOT / "data/projects.json"
REPO_LINK = re.compile(r"https://github\.com/REliasCheng/([A-Za-z0-9_.-]+)")
MD_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
HTML_ASSET = re.compile(r'(?:src|srcset)="([^"]+)"')
FORBIDDEN_SVG = re.compile(
    r'<\s*(?:script|foreignObject|image)\b|(?:href|src)\s*=\s*["\'](?:https?:|data:|javascript:)|url\(\s*["\']?https?:',
    re.I,
)


def validate() -> list[str]:
    errors = []
    readme = README.read_text(encoding="utf-8")
    catalog = json.loads(PROJECTS.read_text(encoding="utf-8"))
    categories = catalog["categories"]
    repositories = [project["repository"] for group in categories for project in group["projects"]]
    if len(repositories) != 14 or len(set(repositories)) != 14:
        errors.append("Project catalog must contain each of the 14 non-profile repositories once")
    linked = REPO_LINK.findall(readme)
    if len(linked) != 14 or set(linked) != set(repositories):
        errors.append(f"README repository links do not match catalog: {linked}")
    for link in MD_LINK.findall(readme):
        if link.startswith(("http://", "https://", "#")):
            continue
        path = (ROOT / unquote(link.split("#", 1)[0])).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            errors.append(f"Missing or escaping Markdown link: {link}")
    for asset in HTML_ASSET.findall(readme):
        path = (ROOT / unquote(asset)).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            errors.append(f"Missing or escaping README asset: {asset}")
    if readme.count("<picture>") != readme.count("</picture>"):
        errors.append("Unbalanced picture elements")
    if readme.count("alt=") < readme.count("<picture>"):
        errors.append("Picture elements need text alternatives")
    for path in (ROOT / "assets").rglob("*.svg"):
        content = path.read_text(encoding="utf-8")
        try:
            ElementTree.fromstring(content)
        except ElementTree.ParseError as exc:
            errors.append(f"Invalid SVG XML {path}: {exc}")
        if FORBIDDEN_SVG.search(content):
            errors.append(f"Potential external or executable SVG content: {path}")
        if path.stat().st_size > 1_000_000:
            errors.append(f"SVG exceeds 1 MB: {path}")
    if "assets/preview/snake-" in readme and not all(
        (ROOT / "assets/preview" / f"snake-{theme}.svg").is_file() for theme in ("dark", "light")
    ):
        errors.append("README references missing contribution-snake files")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("Profile validation passed: 14 unique links, local assets, SVG XML and safe references")
