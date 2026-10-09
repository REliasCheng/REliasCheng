"""Reject valid-looking telemetry that is inconsistent with its JSON."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_metrics import snapshot_freshness, validate  # noqa: E402


class MetricsValidationTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.directory = Path(holder.name)
        for name in ("telemetry.json", "telemetry-dark.svg", "telemetry-light.svg"):
            shutil.copyfile(ROOT / "assets/preview" / name, self.directory / name)
        self.data = json.loads((self.directory / "telemetry.json").read_text(encoding="utf-8"))

    def write_data(self):
        (self.directory / "telemetry.json").write_text(json.dumps(self.data), encoding="utf-8")

    def test_checked_in_snapshot_is_consistent(self):
        validate(self.directory)

    def test_duplicate_repository_is_rejected_even_with_five_rows(self):
        self.data["ci"][1] = dict(self.data["ci"][0])
        self.write_data()
        with self.assertRaisesRegex(ValueError, "five unique"):
            validate(self.directory)

    def test_changed_json_with_old_svg_is_rejected(self):
        self.data["public_repositories"] += 1
        self.write_data()
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate(self.directory)

    def test_changed_svg_with_same_json_is_rejected(self):
        target = self.directory / "telemetry-light.svg"
        target.write_text(target.read_text(encoding="utf-8").replace("PASS", "FAIL", 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate(self.directory)

    def test_utc_label_required(self):
        self.data["refreshed_utc"] = "yesterday"
        self.write_data()
        with self.assertRaisesRegex(ValueError, "UTC refresh"):
            validate(self.directory)

    def test_fresh_stale_future_and_timezone_contract(self):
        collected = "2026-10-09 08:45 UTC"
        baseline = datetime(2026, 10, 9, 9, 0, tzinfo=timezone.utc)
        self.assertEqual(snapshot_freshness(collected, baseline), "FRESH")
        self.assertEqual(snapshot_freshness(collected, baseline + timedelta(hours=49)), "STALE")
        self.assertEqual(snapshot_freshness(collected, baseline - timedelta(hours=2)), "FUTURE")
        self.assertEqual(snapshot_freshness(collected, baseline.astimezone(timezone(timedelta(hours=8)))), "FRESH")
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            snapshot_freshness(collected, datetime(2026, 10, 9, 9, 0))


if __name__ == "__main__":
    unittest.main()
