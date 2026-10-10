"""Root-tag insertion must preserve upstream animation text."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_snake import prepare, root_open_end  # noqa: E402


class SnakePreparationTests(unittest.TestCase):
    def test_root_tag_scanner_ignores_declaration_comments_and_quoted_angle(self):
        source = '<?xml version="1.0"?>\n<!-- a > b -->\n<svg xmlns="http://www.w3.org/2000/svg" aria-labelledby="a>b"><rect/></svg>'
        end = root_open_end(source)
        self.assertTrue(source[:end].endswith('aria-labelledby="a>b">'))
        self.assertEqual(source[end:], "<rect/></svg>")

    def test_prepare_accepts_declaration_without_losing_source_cells(self):
        with tempfile.TemporaryDirectory() as holder:
            source = Path(holder) / "source"
            output = Path(holder) / "output"
            source.mkdir()
            for theme in ("dark", "light"):
                original = (
                    '<?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
                    'viewBox="0 0 100 20"><desc>' + "real data " * 70 +
                    '</desc><rect class="c" x="1" y="1" width="10" height="10"/></svg>'
                )
                (source / f"snake-{theme}.svg").write_text(original, encoding="utf-8")
            prepare(source, output)
            for theme in ("dark", "light"):
                framed = (output / f"snake-{theme}.svg").read_text(encoding="utf-8")
                self.assertIn("real data " * 70, framed)
                self.assertIn("SIGNALCORE real GitHub contribution animation", framed)

    def test_unclosed_root_fails(self):
        with self.assertRaisesRegex(ValueError, "Unclosed"):
            root_open_end('<svg xmlns="http://www.w3.org/2000/svg"')


if __name__ == "__main__":
    unittest.main()
