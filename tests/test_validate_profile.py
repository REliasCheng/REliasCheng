"""Offline contract checks for repository and featured-evidence links."""

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_profile import check_repository_links, expected_evidence_links  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
