"""No-network, no-write tests for future asset publication failure semantics."""

import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from publish_assets import (  # noqa: E402
    ASSETS, PublicationBlocked, PublicationVerificationUncertain, changed_assets,
    plan, publish, validate_source,
)


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.holder = tempfile.TemporaryDirectory()
        self.addCleanup(self.holder.cleanup)
        self.source = Path(self.holder.name) / "source"
        self.source.mkdir()
        for name in ASSETS:
            shutil.copyfile(ROOT / "assets/preview" / name, self.source / name)
        self.data = json.loads((self.source / "telemetry.json").read_text(encoding="utf-8"))
        self.shas = {item["repository"]: item["sha"] for item in self.data["ci"]}
        self.now = datetime(2026, 10, 9, 9, 0, tzinfo=timezone.utc)

    def fetch(self, path):
        if path.startswith("/users/"):
            languages = [language for language, amount in self.data["languages_by_repository"] for _ in range(amount)]
            return [{"private": False, "language": language} for language in languages] + [
                {"private": False, "language": None}
                for _ in range(self.data["public_repositories"] - len(languages))
            ]
        repository = path.split("/")[3]
        if "/actions/workflows/" in path:
            return {"workflow_runs": [{"head_sha": self.shas[repository], "status": "completed", "conclusion": "success"}]}
        return {"commit": {"sha": self.shas[repository]}}

    def test_valid_source_and_no_change(self):
        validated = validate_source(self.source, self.fetch)
        self.assertEqual(validated["public_repositories"], self.data["public_repositories"])
        result = plan(self.source, self.source, self.fetch, head="a" * 40, now=self.now)
        self.assertTrue(result["no_change"])
        self.assertEqual(result["changed"], [])

    def test_stale_snapshot_blocks_dry_run_but_old_artifact_remains_readable(self):
        with self.assertRaisesRegex(PublicationBlocked, "stale"):
            plan(self.source, self.source, self.fetch, head="a" * 40,
                 now=datetime(2026, 10, 12, 9, 0, tzinfo=timezone.utc))
        self.assertEqual(validate_source(self.source, self.fetch)["public_repositories"], 15)
        self.assertTrue(plan(self.source, self.source, self.fetch, head="a" * 40, now=self.now)["no_change"])

    def test_still_image_must_match_animated_source(self):
        target = self.source / "contribution-static-dark.svg"
        target.write_text(target.read_text(encoding="utf-8").replace("Static REliasCheng", "Old REliasCheng", 1),
                          encoding="utf-8")
        with self.assertRaisesRegex(PublicationBlocked, "does not match"):
            validate_source(self.source, self.fetch)

    def test_changed_file_only(self):
        destination = Path(self.holder.name) / "published"
        shutil.copytree(self.source, destination)
        (destination / "snake-dark.svg").write_text("old", encoding="utf-8")
        self.assertEqual(changed_assets(self.source, destination), ["snake-dark.svg"])

    def test_missing_dark_or_light(self):
        for name in ("snake-dark.svg", "contribution-static-light.svg", "telemetry-light.svg"):
            with self.subTest(name=name):
                target = self.source / name
                original = target.read_bytes()
                target.unlink()
                with self.assertRaises((PublicationBlocked, FileNotFoundError)):
                    validate_source(self.source, self.fetch)
                target.write_bytes(original)

    def test_invalid_svg_html_and_oversize(self):
        target = self.source / "snake-dark.svg"
        original = target.read_bytes()
        for content in (b"<svg", b"<html>Forbidden</html>", b"x" * 1_000_001):
            with self.subTest(content=content[:12]):
                target.write_bytes(content)
                with self.assertRaises((PublicationBlocked, ValueError)):
                    validate_source(self.source, self.fetch)
        target.write_bytes(original)

    def test_api_error_and_sha_mismatch(self):
        with self.assertRaises(PublicationBlocked):
            validate_source(self.source, lambda path: (_ for _ in ()).throw(OSError("API 403")))
        with self.assertRaises(PublicationBlocked):
            validate_source(self.source, lambda path: {"commit": {"sha": "0" * 40}})

    def test_ci_status_mismatch_is_blocked(self):
        def failure_fetch(path):
            if "/actions/workflows/" in path:
                repository = path.split("/")[3]
                return {"workflow_runs": [{"head_sha": self.shas[repository], "status": "completed", "conclusion": "failure"}]}
            return self.fetch(path)

        with self.assertRaisesRegex(PublicationBlocked, "CI status changed"):
            validate_source(self.source, failure_fetch)

    def test_inventory_mismatch_is_blocked(self):
        def changed_fetch(path):
            if path.startswith("/users/"):
                return [{"private": False, "language": "Python"}]
            return self.fetch(path)

        with self.assertRaisesRegex(PublicationBlocked, "inventory"):
            validate_source(self.source, changed_fetch)

    def test_missing_production_branch_is_reported_without_creation(self):
        result = plan(self.source, None, self.fetch, head="", now=self.now)
        self.assertEqual(result["branch_status"], "MISSING_REQUIRES_SEPARATE_APPROVAL")
        self.assertFalse(result["remote_changed"])

    def test_existing_branch_dry_run_compares_cloned_contents(self):
        def fake_command(*args, cwd=ROOT):
            if args[:3] == ("git", "remote", "get-url"):
                return "https://github.com/REliasCheng/REliasCheng.git"
            if args[:2] == ("git", "clone"):
                checkout = Path(args[-1])
                shutil.copytree(self.source, checkout)
                return ""
            raise AssertionError(f"Unexpected command: {args}")

        with patch("publish_assets.command", side_effect=fake_command):
            result = plan(self.source, None, self.fetch, head="a" * 40, now=self.now)
        self.assertTrue(result["no_change"])

    def test_approved_sha_mismatch_blocks_before_clone(self):
        with patch("publish_assets.branch_head", return_value="a" * 40):
            with self.assertRaisesRegex(PublicationBlocked, "Approved main SHA differs"):
                publish(self.source, "b" * 40)

    def test_checkout_remote_without_git_suffix(self):
        def head(remote, branch="signalcore-assets"):
            return "a" * 40 if branch == "main" else None

        with patch("publish_assets.branch_head", side_effect=head), patch(
            "publish_assets.command", return_value="https://github.com/REliasCheng/REliasCheng"
        ):
            with self.assertRaisesRegex(PublicationBlocked, "branch absent"):
                publish(self.source, "a" * 40)

    def test_missing_branch_blocks_before_clone(self):
        def head(remote, branch="signalcore-assets"):
            return "a" * 40 if branch == "main" else None

        with patch("publish_assets.branch_head", side_effect=head), patch(
            "publish_assets.command", return_value="https://github.com/REliasCheng/REliasCheng.git"
        ):
            with self.assertRaisesRegex(PublicationBlocked, "branch absent"):
                publish(self.source, "a" * 40)

    def test_non_fast_forward_is_blocked_without_force(self):
        calls = []

        def fake_command(*args, cwd=ROOT):
            calls.append(args)
            if args[:2] == ("git", "remote"):
                return "https://github.com/REliasCheng/REliasCheng.git"
            if args[:2] == ("git", "push"):
                raise PublicationBlocked("non-fast-forward")
            if args[:2] == ("git", "rev-parse"):
                return "b" * 40
            if args[:2] == ("git", "clone"):
                checkout = Path(args[-1])
                checkout.mkdir()
                return ""
            return ""

        with patch("publish_assets.branch_head", return_value="a" * 40), patch(
            "publish_assets.validate_source", return_value=self.data
        ), patch("publish_assets.command", side_effect=fake_command):
            with self.assertRaisesRegex(PublicationBlocked, "non-fast-forward"):
                publish(self.source, "a" * 40)
        self.assertFalse(any("--force" in part for call in calls for part in call))

    def test_successful_push_followed_by_remote_advance_is_not_reported_as_no_change(self):
        calls = []

        def fake_command(*args, cwd=ROOT):
            calls.append(args)
            if args[:3] == ("git", "remote", "get-url"):
                return "https://github.com/REliasCheng/REliasCheng.git"
            if args[:2] == ("git", "clone"):
                Path(args[-1]).mkdir()
            if args[:3] == ("git", "rev-parse", "HEAD"):
                return "b" * 40
            return ""

        with patch("publish_assets.branch_head", side_effect=["a" * 40, "a" * 40, "c" * 40]), patch(
            "publish_assets.validate_source", return_value=self.data
        ), patch("publish_assets.command", side_effect=fake_command):
            with self.assertRaises(PublicationVerificationUncertain) as result:
                publish(self.source, "a" * 40)
        self.assertEqual(result.exception.committed_sha, "b" * 40)
        self.assertEqual(result.exception.observed_head, "c" * 40)
        self.assertTrue(any(call[:2] == ("git", "push") for call in calls))
        self.assertFalse(any("--force" in part for call in calls for part in call))

    def test_successful_push_followed_by_unavailable_remote_read_is_uncertain(self):
        def fake_command(*args, cwd=ROOT):
            if args[:3] == ("git", "remote", "get-url"):
                return "https://github.com/REliasCheng/REliasCheng.git"
            if args[:2] == ("git", "clone"):
                Path(args[-1]).mkdir()
            if args[:3] == ("git", "rev-parse", "HEAD"):
                return "b" * 40
            return ""

        with patch("publish_assets.branch_head", side_effect=["a" * 40, "a" * 40, PublicationBlocked("read failed")]), patch(
            "publish_assets.validate_source", return_value=self.data
        ), patch("publish_assets.command", side_effect=fake_command):
            with self.assertRaises(PublicationVerificationUncertain) as result:
                publish(self.source, "a" * 40)
        self.assertIsNone(result.exception.observed_head)


if __name__ == "__main__":
    unittest.main()
