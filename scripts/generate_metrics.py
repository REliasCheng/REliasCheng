"""Build a dated, public-data-only SIGNALCORE metrics preview.

No output is replaced if the repository inventory request fails. CI status is
valid for CURRENT MAIN only when a run's head SHA equals that branch's SHA.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/brand/tokens.json").read_text(encoding="utf-8"))
OWNER = "REliasCheng"
API = "https://api.github.com"
MONITORED = (
    ("Python Host", "Python-Host-Application-Lab", "test.yml", "Host app"),
    ("Embedded C/C++", "Embedded-C-Cpp-Learning", "host-tests.yml", "Portable core"),
    ("C51 Planner", "C51-Board-Lab", "host-tests.yml", "Planner core"),
    ("STC89 Terminal", "stc89c52-learning", "host-tests.yml", "Portable core"),
    ("STC8 UART", "STC8-MCU-Learning", "host-tests.yml", "Portable core"),
)


def fetch_json(path: str) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "SIGNALCORE-public-metrics"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(API + path, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in {502, 503, 504} or attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(1 + attempt)
    raise RuntimeError("Unreachable API retry state")


def classify_ci(head_sha: str, runs: list[dict]) -> str:
    for run in runs:
        if run.get("head_sha") == head_sha:
            if run.get("status") != "completed":
                return "PENDING"
            if run.get("conclusion") == "success":
                return "PASS"
            return "FAIL"
    if any(run.get("conclusion") == "success" for run in runs):
        return "STALE"
    return "NOT VERIFIED"


def collect(now: datetime, fetch=fetch_json) -> dict:
    repos = fetch(f"/users/{OWNER}/repos?per_page=100&type=owner")
    if not isinstance(repos, list):
        raise ValueError("GitHub repository response is not a list")
    public = [repo for repo in repos if not repo.get("private")]
    if not public:
        raise ValueError("No public repository inventory returned; refusing to render zero")
    languages = Counter(repo.get("language") for repo in public if repo.get("language"))
    results = []
    for label, repository, workflow, scope in MONITORED:
        try:
            branch = fetch(f"/repos/{OWNER}/{repository}/branches/main")
            sha = branch["commit"]["sha"]
            runs_response = fetch(
                f"/repos/{OWNER}/{repository}/actions/workflows/{workflow}/runs?branch=main&per_page=10"
            )
            runs = runs_response["workflow_runs"]
            status = classify_ci(sha, runs)
        except (KeyError, TypeError, ValueError, urllib.error.URLError, TimeoutError):
            sha = None
            status = "UNAVAILABLE"
        results.append({"label": label, "repository": repository, "scope": scope, "status": status, "sha": sha})
    return {
        "owner": OWNER,
        "refreshed_utc": now.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "public_repositories": len(public),
        "languages_by_repository": languages.most_common(3),
        "ci": results,
        "source": "GitHub public REST API",
    }


def render_svg(data: dict, theme: str) -> str:
    t = TOKENS[theme]
    count = data["public_repositories"]
    languages = ", ".join(f"{name} {amount}" for name, amount in data["languages_by_repository"]) or "Unavailable"
    rows = []
    for index, item in enumerate(data["ci"]):
        y = 222 + index * 46
        status = item["status"]
        color = t["verified"] if status == "PASS" else t["warning"] if status in {"STALE", "PENDING"} else t["secondary"]
        sha = item["sha"][:8] if item["sha"] else "unavailable"
        rows.append(
            f'<path d="M28 {y + 12}H1172" stroke="{t["border"]}"/>'
            f'<text x="40" y="{y}" fill="{t["text"]}" font-size="17">{escape(item["label"])}</text>'
            f'<text x="452" y="{y}" fill="{t["secondary"]}" font-size="15">{escape(item["scope"])}</text>'
            f'<text x="780" y="{y}" fill="{t["muted"]}" font-size="15">{sha}</text>'
            f'<text x="1004" y="{y}" fill="{color}" font-size="16" font-weight="700">{status}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-labelledby="title desc">
  <title id="title">SIGNALCORE public GitHub telemetry</title>
  <desc id="desc">Public repository count, repository-language counts and current-main host CI states. Activity is not engineering quality; host CI is not hardware validation.</desc>
  <rect width="1200" height="480" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <text x="34" y="48" fill="{t['signal']}" font-family="Consolas, ui-monospace, monospace" font-size="17" letter-spacing="2">SIGNALCORE / PUBLIC GITHUB METRICS</text>
  <text x="34" y="87" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="26" font-weight="650">{count} public repositories</text>
  <text x="34" y="117" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="15">Primary language by repository: {escape(languages)}</text>
  <text x="34" y="145" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="14">Last refreshed: {escape(data['refreshed_utc'])}</text>
  <path d="M28 162H1172" stroke="{t['border']}" stroke-width="2"/>
  <g font-family="Consolas, ui-monospace, monospace">
    <text x="40" y="190" fill="{t['muted']}" font-size="14">PROJECT</text>
    <text x="452" y="190" fill="{t['muted']}" font-size="14">HOST SCOPE</text>
    <text x="780" y="190" fill="{t['muted']}" font-size="14">MAIN SHA</text>
    <text x="1004" y="190" fill="{t['muted']}" font-size="14">HOST CI</text>
    {''.join(rows)}
    <text x="34" y="461" fill="{t['muted']}" font-size="13">PASS requires this workflow's successful run at current main. No target-build or hardware claim.</text>
  </g>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets/preview")
    parser.add_argument("--input-json", type=Path, help="Re-render a previously captured public snapshot without an API call")
    args = parser.parse_args()
    data = json.loads(args.input_json.read_text(encoding="utf-8")) if args.input_json else collect(datetime.now(timezone.utc))
    outputs = {theme: render_svg(data, theme) for theme in ("dark", "light")}
    for content in outputs.values():
        ElementTree.fromstring(content)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for theme, content in outputs.items():
        (args.output_dir / f"telemetry-{theme}.svg").write_text(content + "\n", encoding="utf-8")
    (args.output_dir / "telemetry.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Generated dated public metrics for {data['public_repositories']} repositories; no hardware claims")


if __name__ == "__main__":
    main()
