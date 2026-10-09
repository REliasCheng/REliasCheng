"""Original design components retain accessibility and reduced-motion fallbacks."""

import sys
from pathlib import Path
import shutil
import tempfile
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_brand_assets import featured_card, featured_mobile_card, terminal  # noqa: E402
from prepare_static_contribution import prepare  # noqa: E402


class BrandAssetTests(unittest.TestCase):
    def test_terminal_has_staged_typing_and_static_fallback(self):
        for theme in ("dark", "light"):
            animated = terminal(theme)
            static = terminal(theme, animated=False)
            ElementTree.fromstring(animated)
            ElementTree.fromstring(static)
            self.assertEqual(animated.count('class="typed"'), 8)
            self.assertIn("@media (prefers-reduced-motion: reduce)", animated)
            self.assertIn("animation-fill-mode: both", animated)
            self.assertNotIn('class="typed"', static)
            self.assertNotIn("<style>", static)
            self.assertIn("Original host software", static)
            self.assertIn("Host-side tests", static)

    def test_distinct_featured_cards_in_both_themes(self):
        for theme in ("dark", "light"):
            contents = [featured_card(theme, kind) for kind in ("python", "embedded-cpp", "c51")]
            mobile = [featured_mobile_card(theme, kind) for kind in ("python", "embedded-cpp", "c51")]
            for content in contents:
                ElementTree.fromstring(content)
                self.assertIn("<title", content)
                self.assertIn("<desc", content)
                self.assertIn('viewBox="0 0 1200 190"', content)
                self.assertNotIn("<image", content)
            self.assertEqual(len(set(contents)), 3)
            self.assertEqual(len(set(mobile)), 3)
            for content in mobile:
                ElementTree.fromstring(content)
                self.assertIn('viewBox="0 0 540 220"', content)
                self.assertIn("<title", content)
                self.assertIn("<desc", content)

    def test_still_graph_is_derived_without_snake_or_animation(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for theme in ("dark", "light"):
                shutil.copyfile(ROOT / "assets/preview" / f"snake-{theme}.svg", directory / f"snake-{theme}.svg")
            prepare(directory)
            for theme in ("dark", "light"):
                root = ElementTree.parse(directory / f"contribution-static-{theme}.svg").getroot()
                classes = [node.get("class", "").split() for node in root]
                self.assertFalse(any("s" in group or "u" in group for group in classes))
                self.assertTrue(any("c" in group for group in classes))


if __name__ == "__main__":
    unittest.main()
