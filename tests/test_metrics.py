"""Contract tests for current-SHA CI semantics and fixture-based metrics rendering."""

import sys
from datetime import datetime, timezone
from pathlib import Path
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_metrics import classify_ci, collect, render_svg  # noqa: E402


class MetricsTests(unittest.TestCase):
    def test_current_success(self):
        self.assertEqual(classify_ci("current", [{"head_sha": "current", "status": "completed", "conclusion": "success"}]), "PASS")

    def test_old_success_is_stale(self):
        self.assertEqual(classify_ci("current", [{"head_sha": "old", "status": "completed", "conclusion": "success"}]), "STALE")

    def test_current_failure_and_pending(self):
        self.assertEqual(classify_ci("x", [{"head_sha": "x", "status": "completed", "conclusion": "failure"}]), "FAIL")
        self.assertEqual(classify_ci("x", [{"head_sha": "x", "status": "in_progress", "conclusion": None}]), "PENDING")

    def test_absent_run_is_not_verified(self):
        self.assertEqual(classify_ci("x", []), "NOT VERIFIED")

    def test_fixture_render_and_unavailable(self):
        def fake_fetch(path):
            if path.startswith("/users/"):
                return [{"name": "example", "private": False, "language": "Python"}]
            if "/branches/main" in path:
                return {"commit": {"sha": "c" * 40}}
            if "C51-Board-Lab" in path:
                raise KeyError("fixture failure")
            return {"workflow_runs": [{"head_sha": "c" * 40, "status": "completed", "conclusion": "success"}]}

        data = collect(datetime(2026, 10, 9, tzinfo=timezone.utc), fake_fetch)
        self.assertEqual(data["public_repositories"], 1)
        self.assertEqual(data["ci"][2]["status"], "UNAVAILABLE")
        for theme in ("dark", "light"):
            root = ElementTree.fromstring(render_svg(data, theme))
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_newer_failure_overrides_older_pass_regardless_of_api_order(self):
        runs = [
            {"head_sha": "x", "status": "completed", "conclusion": "failure", "created_at": "2026-10-09T11:00:00Z", "id": 2},
            {"head_sha": "x", "status": "completed", "conclusion": "success", "created_at": "2026-10-09T10:00:00Z", "id": 1},
        ]
        self.assertEqual(classify_ci("x", runs), "FAIL")
        self.assertEqual(classify_ci("x", list(reversed(runs))), "FAIL")

    def test_api_inventory_failure_never_becomes_zero(self):
        with self.assertRaises(ValueError):
            collect(datetime(2026, 10, 9, tzinfo=timezone.utc), lambda path: [])

    def test_incomplete_main_sha_is_unavailable(self):
        def fake_fetch(path):
            if path.startswith("/users/"):
                return [{"private": False, "language": "C"}]
            return {"commit": {"sha": "not-a-sha"}}

        data = collect(datetime(2026, 10, 9, tzinfo=timezone.utc), fake_fetch)
        self.assertTrue(all(item["status"] == "UNAVAILABLE" for item in data["ci"]))


if __name__ == "__main__":
    unittest.main()
