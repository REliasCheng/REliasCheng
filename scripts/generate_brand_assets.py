"""Generate original, self-contained SIGNALCORE SVG assets from brand tokens."""

from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree

from v2_brand import hero, featured_card, featured_mobile_card, footer



ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/brand/tokens.json").read_text(encoding="utf-8"))
BRAND = ROOT / "assets/brand"
CARDS = ROOT / "assets/cards"
FALLBACK = ROOT / "assets/fallback"


def save(path: Path, source: str) -> None:
    ElementTree.fromstring(source)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source.rstrip() + "\n", encoding="utf-8")


def terminal(theme: str, animated: bool = True) -> str:
    t = TOKENS[theme]
    motion = """<style>
    .typed { animation-name: reveal; animation-timing-function: steps(30,end); animation-fill-mode: both; }
    @keyframes reveal { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
    .cursor { opacity: 0; animation: blink 1.1s step-end 7.35s infinite; }
    @keyframes blink { 0%,49% { opacity: 1; } 50%,100% { opacity: 0; } }
    @media (prefers-reduced-motion: reduce) {
      .typed { animation: none; clip-path: none; }
      .cursor { animation: none; opacity: 1; }
    }
  </style>""" if animated else ""

    def line(y: int, content: str, color: str, delay: float, duration: float) -> str:
        effect = (
            f' class="typed" style="animation-delay:{delay}s;animation-duration:{duration}s"'
            if animated else ""
        )
        return f'<text x="34" y="{y}" fill="{color}"{effect}>{content}</text>'

    lines = (
        line(90, "signalcore@elias:~$ whoami", t["signal"], .2, .9),
        line(122, "Elias Cheng", t["text"], 1.2, .35),
        line(152, "Embedded systems / firmware / low-level software", t["secondary"], 1.75, .55),
        line(198, "signalcore@elias:~$ load --portfolio", t["signal"], 2.85, .9),
        line(232, "[CODE] Original host software", t["text"], 4.0, .55),
        line(260, "[CHECK] Host-side tests on implemented work", t["verified"], 4.8, .55),
        line(288, "[STUDY] MCU / RTOS / system architecture", t["secondary"], 5.6, .65),
        line(325, "signalcore@elias:~$", t["signal"], 6.7, .55),
    )
    cursor_class = ' class="cursor"' if animated else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
  <title id="title">SIGNALCORE portfolio terminal</title>
  <desc id="desc">A staged whoami and portfolio command sequence introducing original software, host tests and architecture studies; these are not hardware status messages.</desc>
{motion}
  <rect width="1200" height="360" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <path d="M0 45H1200" stroke="{t['border']}"/><circle cx="27" cy="22" r="5" fill="{t['signal']}"/><circle cx="47" cy="22" r="5" fill="{t['blue']}"/><circle cx="67" cy="22" r="5" fill="{t['muted']}"/>
  <text x="94" y="28" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="15">signalcore / portfolio interface</text>
  <path d="M29 173H775M29 305H775" stroke="{t['border']}" stroke-width="1"/>
  <path d="M865 94H928L949 117H1128M865 272H928L949 249H1128" fill="none" stroke="{t['border']}" stroke-width="2"/>
  <path d="M935 133H1082V200H1040V218H984V200H935Z" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <path d="M954 165H977V150H1001V183H1026V165H1061" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <text x="952" y="245" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="13" letter-spacing="2">CORE / HOST</text>
  <g font-family="Consolas, ui-monospace, monospace" font-size="19">
    {''.join(lines)}
    <rect{cursor_class} x="288" y="307" width="10" height="22" fill="{t['signal']}"/>
  </g>
</svg>'''


def divider(theme: str) -> str:
    t = TOKENS[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="34" viewBox="0 0 1200 34" role="img" aria-label="SIGNALCORE signal divider">
  <path d="M0 17H418L436 17L445 5L456 29L469 10L481 17H1200" fill="none" stroke="{t['border']}" stroke-width="2"/>
  <path d="M418 17H436L445 5L456 29L469 10L481 17" fill="none" stroke="{t['signal']}" stroke-width="2"/>
</svg>'''


def category_card(theme: str, label: str, code: str, subtitle: str, accent: str) -> str:
    t = TOKENS[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="132" viewBox="0 0 1200 132" role="img" aria-labelledby="title desc">
  <title id="title">{label}</title><desc id="desc">SIGNALCORE section marker for {subtitle}.</desc>
  <rect width="1200" height="132" rx="13" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <rect x="0" y="0" width="8" height="132" rx="4" fill="{accent}"/>
  <text x="35" y="44" fill="{accent}" font-family="Consolas, ui-monospace, monospace" font-size="15" letter-spacing="3">SIGNALCORE / {code}</text>
  <text x="35" y="87" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="31" font-weight="650">{label}</text>
  <text x="810" y="84" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="15">{subtitle}</text>
  <path d="M1034 29H1110V50H1157M1034 104H1082V80H1157" fill="none" stroke="{accent}" stroke-opacity=".6" stroke-width="2"/>
</svg>'''


def fallback(theme: str, kind: str) -> str:
    t = TOKENS[theme]
    caption = "Contribution animation requires a verified generated image" if kind == "contribution" else "Public metrics are temporarily unavailable"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150" role="img" aria-labelledby="title desc">
  <title id="title">SIGNALCORE {kind} fallback</title><desc id="desc">Static fallback. It contains no fabricated activity or metric value.</desc>
  <rect width="1200" height="150" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <path d="M30 104H211L236 70L260 115L290 88H1170" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <text x="30" y="47" fill="{t['signal']}" font-family="Consolas, ui-monospace, monospace" font-size="16" letter-spacing="2">SIGNALCORE / {kind.upper()}</text>
  <text x="316" y="99" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="21">{caption}</text>
</svg>'''


def main() -> None:
    for theme in ("dark", "light"):
        t = TOKENS[theme]
        save(BRAND / f"hero-{theme}.svg", hero(theme))
        save(BRAND / f"hero-mobile-{theme}.svg", hero(theme, mobile=True))
        save(BRAND / f"hero-mobile-static-{theme}.svg", hero(theme, animated=False, mobile=True))
        save(BRAND / f"terminal-{theme}.svg", terminal(theme))
        save(BRAND / f"terminal-static-{theme}.svg", terminal(theme, animated=False))
        save(BRAND / f"divider-{theme}.svg", divider(theme))
        save(BRAND / f"footer-{theme}.svg", footer(theme))
        for label, code, subtitle, accent in (
            ("Featured engineering", "01", "ORIGINAL / TESTABLE", t["signal"]),
            ("Current MCU work", "02", "PORTABLE CORE / TARGET PENDING", t["blue"]),
            ("Architecture labs", "03", "DOCUMENTED / NOT IMPLEMENTED", t["warning"]),
            ("Exploration + foundations", "04", "STUDY / KNOWLEDGE", t["muted"]),
        ):
            filename = {"01": "featured", "02": "mcu", "03": "architecture", "04": "exploration"}[code]
            save(CARDS / f"{filename}-{theme}.svg", category_card(theme, label, code, subtitle, accent))
        for kind in ("python", "embedded-cpp", "c51"):
            save(CARDS / f"featured-{kind}-{theme}.svg", featured_card(theme, kind))
            save(CARDS / f"featured-{kind}-mobile-{theme}.svg", featured_mobile_card(theme, kind))
        save(FALLBACK / f"contribution-{theme}.svg", fallback(theme, "contribution"))
        save(FALLBACK / f"telemetry-{theme}.svg", fallback(theme, "telemetry"))
    save(BRAND / "hero-static.svg", hero("dark", animated=False))
    save(BRAND / "hero-static-light.svg", hero("light", animated=False))
    print("Generated 40 original SVG assets from assets/brand/tokens.json")


if __name__ == "__main__":
    main()
