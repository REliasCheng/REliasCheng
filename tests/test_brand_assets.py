"""Original design components retain accessibility and reduced-motion fallbacks."""

import sys
import re
from pathlib import Path
import shutil
import tempfile
import unittest
from urllib.parse import parse_qs
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_brand_assets import featured_card, featured_mobile_card, terminal  # noqa: E402
from prepare_static_contribution import prepare  # noqa: E402


def contrast(first: str, second: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                  for value in channels]
        return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


class BrandAssetTests(unittest.TestCase):
    def test_snake_production_and_preview_palettes_match_and_remain_distinct(self):
        palettes = []
        for workflow in ("publish-assets.yml", "snake.yml"):
            content = (ROOT / ".github/workflows" / workflow).read_text(encoding="utf-8")
            theme_palettes = {}
            for theme in ("dark", "light"):
                match = re.search(rf"dist/snake-{theme}\.svg\?([^\s]+)", content)
                self.assertIsNotNone(match)
                params = parse_qs(match.group(1))
                snake = params["color_snake"][0]
                dots = params["color_dots"][0].split(",")
                self.assertEqual(len(dots), 5)
                self.assertNotIn(snake.lower(), [dot.lower() for dot in dots])
                self.assertGreaterEqual(contrast(snake, dots[-1]), 2.0)
                theme_palettes[theme] = (snake, dots)
            palettes.append(theme_palettes)
        self.assertEqual(palettes[0], palettes[1])

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
