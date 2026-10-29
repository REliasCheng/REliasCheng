"""Keep the interview documents tied to the audited repository commits."""

import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / "docs" / name for name in (
    "engineering-evidence-quality-review.md",
    "technical-interview-evidence.md",
    "technical-interview-review-questions.md",
)]
INDEX = {record["repository"]: record for record in json.loads(
    (ROOT / "data/engineering-evidence.json").read_text(encoding="utf-8")
)["records"]}


class RecruitmentLinksTest(unittest.TestCase):
    def test_links_are_local_or_commit_bound_to_known_repositories(self):
        for document in DOCS:
            body = document.read_text(encoding="utf-8")
            for raw in re.findall(r"\]\(([^)]+)\)", body):
                with self.subTest(document=document.name, url=raw):
                    parsed = urlparse(raw)
                    if not parsed.scheme:
                        target = (document.parent / unquote(parsed.path)).resolve()
                        self.assertTrue(target.is_relative_to(ROOT))
                        self.assertTrue(target.is_file())
                        continue
                    self.assertEqual((parsed.scheme, parsed.netloc), ("https", "github.com"))
                    parts = unquote(parsed.path).strip("/").split("/")
                    self.assertGreaterEqual(len(parts), 2)
                    self.assertEqual(parts[0], "REliasCheng")
                    record = INDEX[parts[1]]
                    if len(parts) == 2:
                        continue
                    if parts[2] == "blob":
                        self.assertGreaterEqual(len(parts), 5)
                        self.assertEqual(parts[3], record["main_sha"])
                        self.assertNotIn("..", parts[4:])
                    else:
                        self.assertEqual(parts[2:4], ["actions", "runs"])
                        self.assertEqual(
                            raw, record["main_ci"],
                            "CI links must identify the audited main run",
                        )

    def test_review_inventory_and_interview_scope(self):
        review = DOCS[0].read_text(encoding="utf-8")
        evidence = DOCS[1].read_text(encoding="utf-8")
        questions = DOCS[2].read_text(encoding="utf-8")
        self.assertEqual(len(INDEX), 14)
        for name, record in INDEX.items():
            with self.subTest(repository=name):
                self.assertIn(f"| [{name}](https://github.com/REliasCheng/{name}) |", review)
                self.assertIn(f"`{record['main_sha']}`", review)
        self.assertEqual(len(re.findall(r"^## [1-8]\. ", evidence, re.M)), 8)
        self.assertEqual(len(re.findall(r"^\d+\. \*\*", questions, re.M)), 12)
        self.assertIn("REPRODUCTION_COMMAND_REVIEWED", evidence)
        self.assertIn("P0: 0 · P1: 0 · P2: 2", review)


if __name__ == "__main__":
    unittest.main()
