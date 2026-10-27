"""Validate the profile catalog, README assets, and self-contained SVGs."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import re
from urllib.parse import quote, unquote
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROJECTS = ROOT / "data/projects.json"
TOKENS = ROOT / "assets/brand/tokens.json"
EVIDENCE = ROOT / "data/featured-evidence.json"
ENGINEERING = ROOT / "data/engineering-evidence.json"
PROJECT_REPOSITORIES = {
    "Embedded-OTA-Update-Lab", "ARM-Cortex-M-Development-Lab", "FreeRTOS-Embedded-Lab",
    "LVGL-Embedded-GUI-Lab", "Wireless-IoT-Embedded-Lab", "ARM-Linux-Embedded-Lab",
    "Embodied-Robotics-Arm-Lab", "Python-Host-Application-Lab", "Embedded-C-Cpp-Learning",
    "C51-Board-Lab", "STC8-MCU-Learning", "stc89c52-learning", "BlueBridgeCup-MCU",
    "Embedded-Systems-Foundations",
}
VERIFIED_REPOSITORIES = {
    "Embedded-OTA-Update-Lab", "ARM-Cortex-M-Development-Lab", "FreeRTOS-Embedded-Lab",
    "LVGL-Embedded-GUI-Lab", "Wireless-IoT-Embedded-Lab", "ARM-Linux-Embedded-Lab",
    "Embodied-Robotics-Arm-Lab",
}
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


def _safe_repo_path(path: str) -> bool:
    return (isinstance(path, str) and bool(path) and not path.startswith("/")
            and "\\" not in path and not any(char in path for char in ("?", "#", "%", ":"))
            and all(part not in ("", ".", "..") for part in path.split("/")))


def validate_engineering_index(catalog: dict, index: dict) -> list[str]:
    """Validate a dated, commit-bound index without treating it as live CI telemetry."""
    errors = []
    if (not isinstance(index, dict) or set(index) != {"schema_version", "description", "records"}
            or index["schema_version"] != 1):
        return ["Invalid engineering evidence envelope"]
    records = index["records"]
    if not isinstance(records, list) or len(records) != 14:
        return ["Engineering evidence must contain 14 records"]
    projects = {p["repository"]: p for g in catalog["categories"] for p in g["projects"]}
    names = [r.get("repository") for r in records if isinstance(r, dict)]
    if any(not isinstance(name, str) for name in names):
        return ["Engineering evidence contains an invalid repository identifier"]
    if len(names) != 14 or len(set(names)) != 14 or set(names) != set(projects):
        return ["Engineering evidence repository set differs from the 14-project catalog"]
    required = {"repository", "display_name", "implementation_class", "verification_scope",
                "main_sha", "pr", "main_ci", "main_ci_head_sha", "main_ci_conclusion",
                "source", "tests", "documentation", "unverified", "verified_on"}
    for record in records:
        repo = record["repository"]
        if set(record) != required:
            errors.append(f"Incomplete engineering evidence: {repo}")
            continue
        if record["display_name"] != projects[repo]["display_name"] or record["implementation_class"] != projects[repo]["implementation_status"]:
            errors.append(f"Catalog/evidence description mismatch: {repo}")
        sha = record["main_sha"]
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
            errors.append(f"Invalid main SHA: {repo}")
        try:
            date.fromisoformat(record["verified_on"])
        except (TypeError, ValueError):
            errors.append(f"Invalid verification date: {repo}")
        if not isinstance(record["unverified"], list) or not record["unverified"] or not all(isinstance(x, str) and x for x in record["unverified"]):
            errors.append(f"Missing verification boundary: {repo}")
        root = f"https://github.com/REliasCheng/{repo}"
        if repo == "Embedded-Systems-Foundations":
            if any(record[k] is not None for k in ("pr", "main_ci", "main_ci_head_sha", "source", "tests")) or record["main_ci_conclusion"] != "not_applicable" or record["documentation"] != "README.md":
                errors.append("Foundations must remain documentation-only without invented CI")
        else:
            if (not isinstance(record["pr"], str)
                    or not re.fullmatch(re.escape(root) + r"/pull/[1-9][0-9]*", record["pr"])):
                errors.append(f"Invalid PR URL: {repo}")
            if (not isinstance(record["main_ci"], str)
                    or not re.fullmatch(re.escape(root) + r"/actions/runs/[1-9][0-9]*", record["main_ci"])
                    or record["main_ci_head_sha"] != sha or record["main_ci_conclusion"] != "success"):
                errors.append(f"Invalid commit-bound main CI: {repo}")
            if not _safe_repo_path(record["source"]) or not _safe_repo_path(record["tests"]) or record["documentation"] is not None:
                errors.append(f"Invalid source/test path: {repo}")
    return errors


def expected_engineering_links(index: dict, verified_repositories: set[str]) -> set[str]:
    records = {r["repository"]: r for r in index["records"]}
    links = set()
    for repo in verified_repositories:
        record = records[repo]
        root = f"https://github.com/REliasCheng/{repo}"
        for kind in ("source", "tests"):
            links.add(root + "/blob/main/" + quote(record[kind], safe="/"))
        links.add(record["main_ci"])
    return links


def check_repository_links(readme: str, repositories: set[str], evidence: dict,
                           engineering_index: dict | None = None,
                           verified_repositories: set[str] | None = None) -> list[str]:
    errors = []
    markdown_urls = set(MD_LINK.findall(readme))
    github_urls = {url for url in markdown_urls if url.startswith("https://github.com/")}
    expected_roots = {f"https://github.com/REliasCheng/{repo}" for repo in repositories}
    expected_deep = expected_evidence_links(evidence)
    if engineering_index is not None and verified_repositories is not None:
        expected_deep |= expected_engineering_links(engineering_index, verified_repositories)
    if not expected_roots <= github_urls:
        errors.append(f"Missing repository root links: {sorted(expected_roots - github_urls)}")
    if not expected_deep <= github_urls:
        errors.append(f"Missing evidence links: {sorted(expected_deep - github_urls)}")
    unexpected = github_urls - expected_roots - expected_deep
    if unexpected:
        errors.append(f"Unexpected GitHub README links: {sorted(unexpected)}")
    approved_raw = {PRODUCTION_ASSET_ROOT + f"telemetry-{theme}.svg" for theme in ("dark", "light")}
    unexpected_external = {url for url in markdown_urls if url.startswith(("http://", "https://"))
                           and not url.startswith("https://github.com/") and url not in approved_raw}
    if unexpected_external:
        errors.append(f"Unexpected external README links: {sorted(unexpected_external)}")
    return errors


def valid_readme_asset(asset: str, *, allow_production: bool = False) -> bool:
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", asset):
        return allow_production and asset in {
            PRODUCTION_ASSET_ROOT + name for name in PRODUCTION_ASSET_FILES
        }
    path = (ROOT / unquote(asset)).resolve()
    return path.is_relative_to(ROOT.resolve()) and path.is_file()


def check_live_asset_layout(readme: str) -> list[str]:
    """Keep telemetry live while the native GitHub graph supplies contribution UI."""
    errors = []
    pictures = re.findall(r"<picture>.*?</picture>", readme, re.S)
    expected = {
        "telemetry": [
            (f"(prefers-color-scheme: {theme})", PRODUCTION_ASSET_ROOT + f"telemetry-{theme}.svg")
            for theme in ("dark", "light")
        ],
    }
    for kind, sources in expected.items():
        matches = [picture for picture in pictures if sources[-1][1] in picture]
        fallback = 'assets/fallback/telemetry-dark.svg'
        if len(matches) != 1:
            errors.append(f"Expected exactly one live {kind} picture")
            continue
        actual = re.findall(r'<source media="([^"]+)" srcset="([^"]+)">', matches[0])
        if actual != sources:
            errors.append(f"Live {kind} picture has incorrect theme or reduced-motion sources")
        if f'<img src="{fallback}"' not in matches[0]:
            errors.append(f"Live {kind} picture lacks its local static fallback")
    approved_sources = {url for sources in expected.values() for _, url in sources}
    actual_sources = {asset for asset in HTML_ASSET.findall(readme) if asset.startswith(PRODUCTION_ASSET_ROOT)}
    if actual_sources != approved_sources:
        errors.append("README production SVG inventory differs from the two approved telemetry assets")
    raw_links = {link for link in MD_LINK.findall(readme) if link.startswith("https://raw.githubusercontent.com/")}
    expected_full_size = {PRODUCTION_ASSET_ROOT + f"telemetry-{theme}.svg" for theme in ("dark", "light")}
    if raw_links != expected_full_size:
        errors.append("README full-size metrics links differ from approved production assets")
    if not re.search(r"<details>\s*<summary>[^<]+</summary>.*?" + re.escape(PRODUCTION_ASSET_ROOT + "telemetry-dark.svg") + r".*?</details>", readme, re.S):
        errors.append("Telemetry disclosure is missing or no longer contains the live picture")
    if any(name in readme for name in ("snake-dark.svg", "snake-light.svg", "contribution-static-dark.svg", "contribution-static-light.svg")):
        errors.append("README contribution visual duplicates GitHub's native graph")
    if any(f"assets/preview/{name}" in readme for name in PRODUCTION_ASSET_FILES):
        errors.append("README still references a preview dynamic asset")
    return errors


def validate() -> list[str]:
    errors = []
    readme = README.read_text(encoding="utf-8")
    catalog = json.loads(PROJECTS.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    engineering = json.loads(ENGINEERING.read_text(encoding="utf-8"))
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    for theme in ("dark", "light"):
        palette = tokens[theme]
        for role in ("text", "secondary", "muted", "signal", "blue", "verified", "warning"):
            ratio = contrast(palette["panel"], palette[role])
            if ratio < 4.5:
                errors.append(f"{theme} {role}/panel contrast below 4.5:1: {ratio:.2f}")
    categories = catalog["categories"]
    repositories = [project["repository"] for group in categories for project in group["projects"]]
    if len(repositories) != 14 or len(set(repositories)) != 14 or set(repositories) != PROJECT_REPOSITORIES:
        errors.append("Project catalog must contain each of the 14 non-profile repositories once")
    if set(evidence) != {"Python-Host-Application-Lab", "Embedded-C-Cpp-Learning", "C51-Board-Lab"}:
        errors.append("Featured evidence manifest must cover exactly the three featured repositories")
    counts = {group["id"]: len(group["projects"]) for group in categories}
    if counts != {"featured": 3, "verified": 7, "mcu": 3, "foundations": 1}:
        errors.append("Project categories must preserve three featured, seven verified, three MCU and one foundations repository")
    membership = {group["id"]: {p["repository"] for p in group["projects"]} for group in categories}
    if (membership.get("verified") != VERIFIED_REPOSITORIES
            or membership.get("featured") != set(evidence)
            or membership.get("foundations") != {"Embedded-Systems-Foundations"}):
        errors.append("Project categories contain an unexpected repository")
    engineering_errors = validate_engineering_index(catalog, engineering)
    errors.extend(engineering_errors)
    if not engineering_errors and "verified" in counts:
        verified = {p["repository"] for g in categories if g["id"] == "verified" for p in g["projects"]}
        errors.extend(check_repository_links(readme, set(repositories), evidence, engineering, verified))
        if not all(r["verified_on"] in readme for r in engineering["records"]):
            errors.append("README lacks dated evidence snapshot label")
    for link in MD_LINK.findall(readme):
        if link.startswith(("http://", "https://", "#")):
            continue
        path = (ROOT / unquote(link.split("#", 1)[0])).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            errors.append(f"Missing or escaping Markdown link: {link}")
    for asset in HTML_ASSET.findall(readme):
        if not valid_readme_asset(asset, allow_production=True):
            errors.append(f"Missing or escaping README asset: {asset}")
    errors.extend(check_live_asset_layout(readme))
    if readme.count("<picture>") != readme.count("</picture>"):
        errors.append("Unbalanced picture elements")
    if readme.count("alt=") < readme.count("<picture>"):
        errors.append("Picture elements need text alternatives")
    for prefix, static_names, animated_name in (
        ("hero", ("hero-static.svg", "hero-static-light.svg"), "hero-dark.svg"),
    ):
        for name in static_names:
            asset = f"assets/brand/{name}"
            marker = f'srcset="{asset}"'
            if marker not in readme or animated_name not in readme or readme.index(marker) > readme.index(animated_name):
                errors.append(f"Reduced-motion static source absent or after animated {prefix}: {name}")
    if "assets/brand/terminal-dark.svg" in readme or "<h1" in readme or "# Elias Cheng" in readme:
        errors.append("V2 must not repeat the hero identity with a terminal or large heading")
    if readme.count("(max-width: 900px)") != 10:
        errors.append("V2 hero and featured cards need narrow-column sources through the GitHub tablet layout")
    for theme in ("dark", "light"):
        mobile_static = f"assets/brand/hero-mobile-static-{theme}.svg"
        mobile_animated = f"assets/brand/hero-mobile-{theme}.svg"
        desktop = f"assets/brand/hero-{theme}.svg"
        if mobile_static not in readme or mobile_animated not in readme or readme.index(mobile_static) > readme.index(mobile_animated) or readme.index(mobile_animated) > readme.index(desktop):
            errors.append(f"Mobile hero missing or incorrectly ordered: {theme}")
    for removed_banner in ("mcu", "architecture", "exploration"):
        if f"assets/cards/{removed_banner}-dark.svg" in readme:
            errors.append(f"Redundant {removed_banner} banner remains in README")
    for kind in ("python", "embedded-cpp", "c51"):
        for theme in ("dark", "light"):
            desktop = (f"assets/evidence/python-host-mock-gui-{theme}.png" if kind == "python"
                       else f"assets/cards/featured-{kind}-{theme}.svg")
            if desktop not in readme:
                errors.append(f"Missing featured {kind} {theme} picture source")
            mobile = f"assets/cards/featured-{kind}-mobile-{theme}.svg"
            if mobile not in readme or readme.index(mobile) > readme.index(desktop):
                errors.append(f"Missing or incorrectly ordered mobile featured {kind} {theme} source")
    for theme in ("dark", "light"):
        png = ROOT / "assets/evidence" / f"python-host-mock-gui-{theme}.png"
        header = png.read_bytes()[:24] if png.is_file() else b""
        if header[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" or int.from_bytes(header[16:20], "big") != 900 or int.from_bytes(header[20:24], "big") != 160:
            errors.append(f"Invalid or missing real GUI capture: {png}")
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
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("Profile validation passed: 14 repository roots, commit-bound engineering evidence, featured evidence, approved live assets and safe local SVGs")
