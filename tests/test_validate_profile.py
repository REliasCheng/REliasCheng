"""Offline contract checks for repository and featured-evidence links."""

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_profile import (  # noqa: E402
    PRODUCTION_ASSET_ROOT, README, check_live_asset_layout, check_repository_links, expected_evidence_links,
    valid_readme_asset,
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

    def test_live_assets_reject_animated_source_before_still_source(self):
        readme = README.read_text(encoding="utf-8")
        still = f'<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="{PRODUCTION_ASSET_ROOT}contribution-static-dark.svg">'
        animated = f'<source media="(prefers-color-scheme: dark)" srcset="{PRODUCTION_ASSET_ROOT}snake-dark.svg">'
        changed = readme.replace(still + '\n  ', '', 1).replace(animated, animated + '\n  ' + still, 1)
        self.assertTrue(any("reduced-motion" in error for error in check_live_asset_layout(changed)))

    def test_live_assets_reject_missing_local_fallback_and_unapproved_raw_link(self):
        readme = README.read_text(encoding="utf-8")
        changed = readme.replace('assets/fallback/contribution-dark.svg', 'assets/preview/snake-dark.svg', 1)
        changed += '\n[Unexpected](https://raw.githubusercontent.com/REliasCheng/REliasCheng/main/README.md)\n'
        errors = check_live_asset_layout(changed)
        self.assertTrue(any("fallback" in error for error in errors))
        self.assertTrue(any("still-image links" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
