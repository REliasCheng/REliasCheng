"""Negative tests for the profile's external SVG ingestion boundary."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from svg_safety import validate_svg  # noqa: E402


class SvgSafetyTests(unittest.TestCase):
    def test_existing_snake_and_metrics_are_accepted(self):
        for name in ("snake-dark.svg", "telemetry-light.svg", "contribution-static-dark.svg"):
            self.assertIn("<svg", validate_svg(ROOT / "assets/preview" / name))

    def test_active_or_external_content_is_rejected(self):
        base = '<svg xmlns="http://www.w3.org/2000/svg"><desc>' + "x" * 550 + "</desc>"
        cases = (
            base + '<script>alert(1)</script></svg>',
            base + '<foreignObject><p>bad</p></foreignObject></svg>',
            base + '<image xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://example.com/a.png"/></svg>',
            base + '<rect xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="file:///private"/></svg>',
            base + '<rect onload="alert(1)"/></svg>',
            base + '<style>@import "https://example.com/x.css";</style></svg>',
            base + '<style>.a {fill:url(data:image/svg+xml,abc)}</style></svg>',
            '<!DOCTYPE svg [<!ENTITY ext SYSTEM "file:///etc/passwd">]>' + base + "</svg>",
            '<?xml version="1.0"?><!----><?evil x?>' + base + "</svg>",
            base + "<rect></svg>",
        )
        with tempfile.TemporaryDirectory() as holder:
            path = Path(holder) / "input.svg"
            for content in cases:
                with self.subTest(content=content[-60:]):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        validate_svg(path)

    def test_oversize_is_rejected(self):
        with tempfile.TemporaryDirectory() as holder:
            path = Path(holder) / "too-large.svg"
            path.write_text("<svg>" + "x" * 1_000_000 + "</svg>", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_svg(path)

    def test_invalid_utf8_is_rejected(self):
        with tempfile.TemporaryDirectory() as holder:
            path = Path(holder) / "invalid.svg"
            path.write_bytes(b"<svg>" + b"x" * 550 + b"\xff</svg>")
            with self.assertRaises(ValueError):
                validate_svg(path)


if __name__ == "__main__":
    unittest.main()
