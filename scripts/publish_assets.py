"""Plan or (after separate approval) fast-forward publish validated dynamic assets.

This script does not create the asset branch. The current preview uses dry-run
only; no workflow invokes --publish and no write credentials are required.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.error
from xml.etree import ElementTree

from generate_metrics import MONITORED, classify_ci, fetch_json, public_inventory, OWNER
from validate_metrics import validate as validate_metrics
from validate_snake import validate as validate_snake


BRANCH = "signalcore-assets"
ASSETS = ("snake-dark.svg", "snake-light.svg", "telemetry-dark.svg", "telemetry-light.svg", "telemetry.json")
ROOT = Path(__file__).resolve().parents[1]


class PublicationBlocked(RuntimeError):
    """Any validation or concurrency failure leaves published assets unchanged."""


def command(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        raise PublicationBlocked(f"Git operation failed: {' '.join(args[:2])}: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_source(directory: Path, fetch=fetch_json) -> dict:
    try:
        validate_snake(directory)
        validate_metrics(directory)
        data = json.loads((directory / "telemetry.json").read_text(encoding="utf-8"))
        public = public_inventory(fetch)
        languages = Counter(repo.get("language") for repo in public if repo.get("language"))
        if len(public) != data["public_repositories"] or languages.most_common(3) != [tuple(x) for x in data["languages_by_repository"]]:
            raise PublicationBlocked("Public inventory or language summary changed; regenerate metrics")
        workflows = {repository: workflow for _, repository, workflow, _ in MONITORED}
        for item in data["ci"]:
            repository = item["repository"]
            if repository not in workflows or item["status"] == "UNAVAILABLE":
                raise PublicationBlocked(f"Unpublishable CI evidence for {repository}")
            response = fetch(f"/repos/{OWNER}/{repository}/branches/main")
            current = response["commit"]["sha"]
            if current != item["sha"]:
                raise PublicationBlocked(f"Current-main SHA changed for {repository}; regenerate metrics")
            run_response = fetch(
                f"/repos/{OWNER}/{repository}/actions/workflows/{workflows[repository]}/runs?branch=main&per_page=10"
            )
            if classify_ci(current, run_response["workflow_runs"]) != item["status"]:
                raise PublicationBlocked(f"Current host CI status changed for {repository}; regenerate metrics")
        for name in ASSETS:
            path = directory / name
            if not path.is_file() or path.stat().st_size > 1_000_000:
                raise PublicationBlocked(f"Missing or oversized asset: {name}")
        return data
    except (OSError, ValueError, KeyError, TypeError, ElementTree.ParseError, urllib.error.URLError) as exc:
        raise PublicationBlocked(f"Source validation failed: {exc}") from exc


def changed_assets(source: Path, published: Path | None) -> list[str]:
    def digest(path: Path) -> str | None:
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

    return [name for name in ASSETS if published is None or digest(source / name) != digest(published / name)]


def branch_head(remote: str = "origin", branch: str = BRANCH) -> str | None:
    lines = command("git", "ls-remote", "--heads", remote, f"refs/heads/{branch}")
    return lines.split("\t", 1)[0] if lines else None


def plan(source: Path, published: Path | None = None, fetch=fetch_json, remote: str = "origin", head=None) -> dict:
    data = validate_source(source, fetch)
    current_head = branch_head(remote) if head is None else head
    if published is None and current_head:
        remote_url = command("git", "remote", "get-url", remote)
        with tempfile.TemporaryDirectory(prefix="signalcore-dry-run-") as temporary:
            checkout = Path(temporary) / "assets"
            command("git", "clone", "--single-branch", "--branch", BRANCH, remote_url, str(checkout))
            changes = changed_assets(source, checkout)
    else:
        changes = changed_assets(source, published)
    return {
        "mode": "DRY_RUN", "branch": BRANCH, "branch_head": current_head,
        "branch_status": "EXISTS" if current_head else "MISSING_REQUIRES_SEPARATE_APPROVAL",
        "changed": changes, "no_change": not changes,
        "source_refreshed_utc": data["refreshed_utc"], "remote_changed": False,
    }


def publish(source: Path, approved_main_sha: str, remote: str = "origin") -> str:
    """Future-only: clone existing branch, commit changed files, normal push.

    A concurrent push is rejected by Git as non-fast-forward; never retry with
    force. The temporary clone preserves the last published assets on failure.
    """
    if len(approved_main_sha) != 40:
        raise PublicationBlocked("Explicit approved 40-character main SHA required")
    current_main = branch_head(remote, "main")
    if current_main != approved_main_sha:
        raise PublicationBlocked("Approved main SHA differs from remote main")
    remote_url = command("git", "remote", "get-url", remote)
    if remote_url not in {
        f"https://github.com/{OWNER}/{OWNER}.git",
        f"git@github.com:{OWNER}/{OWNER}.git",
    }:
        raise PublicationBlocked("Unexpected remote URL")
    if not branch_head(remote):
        raise PublicationBlocked("Production asset branch absent; initialization requires separate approval")
    validate_source(source)
    with tempfile.TemporaryDirectory(prefix="signalcore-publish-") as temporary:
        checkout = Path(temporary) / "assets"
        command("git", "clone", "--single-branch", "--branch", BRANCH, remote_url, str(checkout))
        changes = changed_assets(source, checkout)
        if not changes:
            return "NO_CHANGE"
        for name in changes:
            shutil.copyfile(source / name, checkout / name)
        command("git", "add", "--", *changes, cwd=checkout)
        command("git", "-c", "user.name=signalcore-assets", "-c", "user.email=signalcore-assets@users.noreply.github.com",
                "commit", "-m", "chore: refresh validated public profile assets", cwd=checkout)
        committed = command("git", "rev-parse", "HEAD", cwd=checkout)
        command("git", "push", "origin", f"HEAD:refs/heads/{BRANCH}", cwd=checkout)
        if branch_head(remote) != committed:
            raise PublicationBlocked("Remote branch verification failed after normal push")
        return committed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--publish", action="store_true", help="future approval only; never invoked by preview Actions")
    parser.add_argument("--source", type=Path, default=ROOT / "assets/preview")
    parser.add_argument("--published-dir", type=Path, help="read-only comparison fixture for dry-run")
    parser.add_argument("--approved-main-sha", help="required only for a separately approved future publication")
    args = parser.parse_args()
    try:
        if args.dry_run:
            print(json.dumps(plan(args.source, args.published_dir), indent=2))
        else:
            if not args.approved_main_sha:
                raise PublicationBlocked("--publish requires --approved-main-sha and separate release approval")
            print(publish(args.source, args.approved_main_sha))
    except PublicationBlocked as exc:
        parser.exit(2, f"PUBLICATION_BLOCKED: {exc}\n")


if __name__ == "__main__":
    main()
