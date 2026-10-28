"""Offline contract checks for project evidence and protected Profile assets."""

import copy
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_profile import (  # noqa: E402
    ENGINEERING, PRODUCTION_ASSET_ROOT, PROJECTS, ROOT, README, check_live_asset_layout,
    check_repository_links, expected_engineering_links, expected_evidence_links,
    valid_readme_asset, validate_engineering_index,
)


class ProfileLinkTests(unittest.TestCase):
    def setUp(self):
        self.repositories = {"Python-Host-Application-Lab"}
        self.evidence = {
            "Python-Host-Application-Lab": {
                "source": "src/application.py",
                "tests": "tests/test_application.py",
                "ci": ".github/workflows/test.yml",
                "design": "docs/system-architecture.md",
            }
        }

    def test_repeated_repository_links_do_not_break_unique_inventory(self):
        roots = "[Project](https://github.com/REliasCheng/Python-Host-Application-Lab) " * 2
        deep = " ".join(f"[Evidence]({url})" for url in expected_evidence_links(self.evidence))
        self.assertEqual(check_repository_links(roots + deep, self.repositories, self.evidence)[-2:], [])

    def test_missing_or_wrong_owner_link_is_rejected(self):
        text = "[Project](https://github.com/SomeoneElse/Python-Host-Application-Lab)"
        errors = check_repository_links(text, self.repositories, self.evidence)
        self.assertTrue(any("Missing repository root" in error for error in errors))
        self.assertTrue(any("Unexpected GitHub" in error for error in errors))

    def test_unknown_evidence_path_is_rejected(self):
        roots = "[Project](https://github.com/REliasCheng/Python-Host-Application-Lab)"
        deep = " ".join(f"[Evidence]({url})" for url in expected_evidence_links(self.evidence))
        extra = "[Fake](https://github.com/REliasCheng/Python-Host-Application-Lab/blob/main/src/imaginary.py)"
        self.assertTrue(any("Unexpected GitHub" in error for error in check_repository_links(roots + deep + extra, self.repositories, self.evidence)))

    def test_manifest_rejects_escape(self):
        self.evidence["Python-Host-Application-Lab"]["source"] = "../private.txt"
        with self.assertRaises(ValueError):
            expected_evidence_links(self.evidence)

    def test_production_urls_are_exactly_allowlisted_when_enabled(self):
        valid = PRODUCTION_ASSET_ROOT + "snake-dark.svg"
        self.assertFalse(valid_readme_asset(valid))
        self.assertTrue(valid_readme_asset(valid, allow_production=True))
        for invalid in (
            "http://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/snake-dark.svg",
            "https://example.com/snake-dark.svg",
            PRODUCTION_ASSET_ROOT + "secrets.txt",
            PRODUCTION_ASSET_ROOT + "../main/README.md",
            PRODUCTION_ASSET_ROOT + "snake-dark.svg?token=x",
            "data:image/svg+xml;base64,PHN2Zz4=",
        ):
            with self.subTest(asset=invalid):
                self.assertFalse(valid_readme_asset(invalid, allow_production=True))

    def test_live_assets_have_exact_theme_motion_and_fallback_layout(self):
        readme = README.read_text(encoding="utf-8")
        self.assertEqual(check_live_asset_layout(readme), [])

    def test_live_assets_reject_removed_contribution_visual_reappearing(self):
        readme = README.read_text(encoding="utf-8")
        changed = readme + f'\n<img src="{PRODUCTION_ASSET_ROOT}snake-dark.svg">\n'
        self.assertTrue(any("contribution visual" in error for error in check_live_asset_layout(changed)))

    def test_live_assets_reject_missing_local_fallback_and_unapproved_raw_link(self):
        readme = README.read_text(encoding="utf-8")
        changed = readme.replace('assets/fallback/telemetry-dark.svg', 'assets/preview/telemetry-dark.svg', 1)
        changed += '\n[Unexpected](https://raw.githubusercontent.com/REliasCheng/REliasCheng/main/README.md)\n'
        errors = check_live_asset_layout(changed)
        self.assertTrue(any("fallback" in error for error in errors))
        self.assertTrue(any("full-size metrics links" in error for error in errors))


class EngineeringEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(PROJECTS.read_text(encoding="utf-8"))
        self.index = json.loads(ENGINEERING.read_text(encoding="utf-8"))
        self.verified = {p["repository"] for g in self.catalog["categories"]
                         if g["id"] == "verified" for p in g["projects"]}

    def test_real_index_is_complete_and_readme_links_are_derived(self):
        self.assertEqual(validate_engineering_index(self.catalog, self.index), [])
        self.assertEqual(len(self.verified), 7)
        self.assertEqual(len(expected_engineering_links(self.index, self.verified)), 21)
        readme = README.read_text(encoding="utf-8")
        for link in expected_engineering_links(self.index, self.verified):
            self.assertIn(f"({link})", readme)

    def test_wrong_ci_host_or_stale_head_is_rejected(self):
        index = copy.deepcopy(self.index)
        index["records"][0]["main_ci"] = "https://example.com/fake"
        self.assertTrue(any("main CI" in x for x in validate_engineering_index(self.catalog, index)))
        index = copy.deepcopy(self.index)
        index["records"][0]["main_ci_head_sha"] = "0" * 40
        self.assertTrue(any("main CI" in x for x in validate_engineering_index(self.catalog, index)))

    def test_path_escape_and_fabricated_foundations_ci_are_rejected(self):
        index = copy.deepcopy(self.index)
        index["records"][0]["source"] = "../private.py"
        self.assertTrue(any("source/test path" in x for x in validate_engineering_index(self.catalog, index)))
        index = copy.deepcopy(self.index)
        index["records"][-1]["main_ci"] = "https://github.com/REliasCheng/Embedded-Systems-Foundations/actions/runs/1"
        self.assertTrue(any("documentation-only" in x for x in validate_engineering_index(self.catalog, index)))

    def test_duplicate_record_or_unlisted_github_link_is_rejected(self):
        index = copy.deepcopy(self.index)
        index["records"][1]["repository"] = index["records"][0]["repository"]
        self.assertTrue(any("repository set" in x for x in validate_engineering_index(self.catalog, index)))
        readme = README.read_text(encoding="utf-8")
        readme += "\n[Unverified](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab/blob/main/fake.c)\n"
        featured = json.loads((ROOT / "data/featured-evidence.json").read_text(encoding="utf-8"))
        roots = {p["repository"] for g in self.catalog["categories"] for p in g["projects"]}
        errors = check_repository_links(readme, roots, featured, self.index, self.verified)
        self.assertTrue(any("Unexpected GitHub" in x for x in errors))

    def test_lookalike_domain_is_rejected(self):
        readme = README.read_text(encoding="utf-8")
        readme += "\n[Fake](https://github.com.evil.example/REliasCheng/FreeRTOS-Embedded-Lab)\n"
        featured = json.loads((ROOT / "data/featured-evidence.json").read_text(encoding="utf-8"))
        roots = {p["repository"] for g in self.catalog["categories"] for p in g["projects"]}
        errors = check_repository_links(readme, roots, featured, self.index, self.verified)
        self.assertTrue(any("Unexpected external" in x for x in errors))


if __name__ == "__main__":
    unittest.main()
