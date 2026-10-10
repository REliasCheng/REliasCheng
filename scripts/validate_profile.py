"""Validate the preview's project catalog, README paths, and self-contained SVGs."""

from __future__ import annotations

import json
from pathlib import Path
import re
from urllib.parse import quote, unquote
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROJECTS = ROOT / "data/projects.json"
TOKENS = ROOT / "assets/brand/tokens.json"
EVIDENCE = ROOT / "data/featured-evidence.json"
MD_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
HTML_ASSET = re.compile(r'(?:src|srcset)="([^"]+)"')
FORBIDDEN_SVG = re.compile(
    r'<\s*(?:script|foreignObject|image)\b|(?:href|src)\s*=\s*["\'](?:https?:|data:|javascript:)|url\(\s*["\']?https?:',
    re.I,
)
PRODUCTION_ASSET_ROOT = "https://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/"
PRODUCTION_ASSET_FILES = {
    "snake-dark.svg", "snake-light.svg", "contribution-static-dark.svg",
    "contribution-static-light.svg", "telemetry-dark.svg", "telemetry-light.svg",
}


def luminance(color: str) -> float:
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(first: str, second: str) -> float:
    upper, lower = sorted((luminance(first), luminance(second)), reverse=True)
    return (upper + 0.05) / (lower + 0.05)


def expected_evidence_links(evidence: dict) -> set[str]:
    links = set()
    for repository, paths in evidence.items():
        if set(paths) != {"source", "tests", "ci", "design"}:
            raise ValueError(f"Incomplete evidence manifest for {repository}")
        for kind, path in paths.items():
            if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
                raise ValueError(f"Invalid evidence path for {repository}: {path}")
            route = "actions/workflows/" + Path(path).name if kind == "ci" else "blob/main/" + quote(path, safe="/")
            links.add(f"https://github.com/REliasCheng/{repository}/{route}")
    return links


def check_repository_links(readme: str, repositories: set[str], evidence: dict) -> list[str]:
    errors = []
    markdown_urls = set(MD_LINK.findall(readme))
    github_urls = {url for url in markdown_urls if url.startswith("https://github.com/")}
    expected_roots = {f"https://github.com/REliasCheng/{repo}" for repo in repositories}
    expected_deep = expected_evidence_links(evidence)
    if not expected_roots <= github_urls:
        errors.append(f"Missing repository root links: {sorted(expected_roots - github_urls)}")
    if not expected_deep <= github_urls:
        errors.append(f"Missing featured evidence links: {sorted(expected_deep - github_urls)}")
    unexpected = github_urls - expected_roots - expected_deep
    if unexpected:
        errors.append(f"Unexpected GitHub README links: {sorted(unexpected)}")
    return errors


def valid_readme_asset(asset: str, *, allow_production: bool = False) -> bool:
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", asset):
        return allow_production and asset in {
            PRODUCTION_ASSET_ROOT + name for name in PRODUCTION_ASSET_FILES
        }
    path = (ROOT / unquote(asset)).resolve()
    return path.is_relative_to(ROOT.resolve()) and path.is_file()


def validate() -> list[str]:
    errors = []
    readme = README.read_text(encoding="utf-8")
    catalog = json.loads(PROJECTS.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    for theme in ("dark", "light"):
        palette = tokens[theme]
        for role in ("text", "secondary", "muted", "signal", "blue", "verified", "warning"):
            ratio = contrast(palette["panel"], palette[role])
            if ratio < 4.5:
                errors.append(f"{theme} {role}/panel contrast below 4.5:1: {ratio:.2f}")
    categories = catalog["categories"]
    repositories = [project["repository"] for group in categories for project in group["projects"]]
    if len(repositories) != 14 or len(set(repositories)) != 14:
        errors.append("Project catalog must contain each of the 14 non-profile repositories once")
    if set(evidence) != {"Python-Host-Application-Lab", "Embedded-C-Cpp-Learning", "C51-Board-Lab"}:
        errors.append("Featured evidence manifest must cover exactly the three featured repositories")
    errors.extend(check_repository_links(readme, set(repositories), evidence))
    for link in MD_LINK.findall(readme):
        if link.startswith(("http://", "https://", "#")):
            continue
        path = (ROOT / unquote(link.split("#", 1)[0])).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            errors.append(f"Missing or escaping Markdown link: {link}")
    for asset in HTML_ASSET.findall(readme):
        if not valid_readme_asset(asset):
            errors.append(f"Missing or escaping README asset: {asset}")
    if readme.count("<picture>") != readme.count("</picture>"):
        errors.append("Unbalanced picture elements")
    if readme.count("alt=") < readme.count("<picture>"):
        errors.append("Picture elements need text alternatives")
    if "<details>" in readme and "assets/preview/snake-" in readme:
        errors.append("Contribution graphic must be visible by default")
    if "assets/brand/terminal-static-dark.svg" not in readme:
        errors.append("Terminal needs a meaningful static image fallback")
    for prefix, static_names, animated_name in (
        ("hero", ("hero-static.svg", "hero-static-light.svg"), "hero-dark.svg"),
        ("terminal", ("terminal-static-dark.svg", "terminal-static-light.svg"), "terminal-dark.svg"),
        ("contribution", ("contribution-static-dark.svg", "contribution-static-light.svg"), "snake-dark.svg"),
    ):
        for name in static_names:
            marker = f'srcset="assets/{"preview" if prefix == "contribution" else "brand"}/{name}"'
            if marker not in readme or readme.index(marker) > readme.index(animated_name):
                errors.append(f"Reduced-motion static source absent or after animated {prefix}: {name}")
    for kind in ("python", "embedded-cpp", "c51"):
        for theme in ("dark", "light"):
            if f"assets/cards/featured-{kind}-{theme}.svg" not in readme:
                errors.append(f"Missing featured {kind} {theme} picture source")
            mobile = f"assets/cards/featured-{kind}-mobile-{theme}.svg"
            if mobile not in readme or readme.index(mobile) > readme.index(f"assets/cards/featured-{kind}-{theme}.svg"):
                errors.append(f"Missing or incorrectly ordered mobile featured {kind} {theme} source")
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
    print("Profile validation passed: 14 repository roots, featured evidence, local assets and safe SVGs")
