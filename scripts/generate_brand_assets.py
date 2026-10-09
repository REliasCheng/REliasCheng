"""Generate original, self-contained SIGNALCORE SVG assets from brand tokens."""

from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "assets/brand/tokens.json").read_text(encoding="utf-8"))
BRAND = ROOT / "assets/brand"
CARDS = ROOT / "assets/cards"
FALLBACK = ROOT / "assets/fallback"


def save(path: Path, source: str) -> None:
    ElementTree.fromstring(source)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source.rstrip() + "\n", encoding="utf-8")


def hero(theme: str, animated: bool = True) -> str:
    t = TOKENS[theme]
    dark = theme == "dark"
    glow = "#164C60" if dark else "#D7EDF3"
    grid = "#4D7790" if dark else "#8BB4C7"
    motion = """<style>
      .pulse { animation: route 7s linear infinite; }
      .sweep { animation: sweep 7s ease-in-out infinite; transform-origin: 1260px 254px; }
      @keyframes route { to { stroke-dashoffset: -180; } }
      @keyframes sweep { 50% { opacity: .92; } }
      @media (prefers-reduced-motion: reduce) { .pulse, .sweep { animation: none; } }
    </style>""" if animated else ""
    pulse = 'class="pulse"' if animated else ""
    sweep = 'class="sweep"' if animated else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="480" viewBox="0 0 1600 480" role="img" aria-labelledby="title desc">
  <title id="title">SIGNALCORE — Elias Cheng</title>
  <desc id="desc">Original circuit-inspired banner with an abstract controller, routed signals and a waveform. Decorative motion is not live hardware data.</desc>
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{grid}" stroke-opacity=".13"/></pattern>
    <linearGradient id="trace" x1="0" x2="1"><stop stop-color="{t['signal']}" stop-opacity="0"/><stop offset=".55" stop-color="{t['signal']}"/><stop offset="1" stop-color="{t['signal']}" stop-opacity="0"/></linearGradient>
{motion}
  </defs>
  <rect width="1600" height="480" rx="20" fill="{t['background']}"/>
  <rect width="1600" height="480" rx="20" fill="url(#grid)"/>
  <path d="M0 77H104L146 119H494M0 404H146L202 348H512M1600 72H1507L1457 122H1408M1600 409H1517L1467 359H1413" fill="none" stroke="{t['border']}" stroke-width="2"/>
  <path {pulse} d="M0 97H96L145 146H529M1600 387H1512L1460 335H1400" fill="none" stroke="url(#trace)" stroke-width="3" stroke-dasharray="30 24"/>
  <circle cx="146" cy="119" r="5" fill="{t['signal']}"/><circle cx="1460" cy="335" r="5" fill="{t['signal']}"/>

  <text x="112" y="91" fill="{t['signal']}" font-family="Consolas, ui-monospace, monospace" font-size="17" letter-spacing="4">SIGNALCORE  /  EMBEDDED ENGINEERING INTERFACE</text>
  <rect x="112" y="112" width="64" height="3" fill="{t['signal']}"/>
  <text x="108" y="230" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="72" font-weight="700" letter-spacing="2">ELIAS CHENG</text>
  <text x="112" y="278" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="23">Embedded systems · low-level software · hardware-aware design</text>
  <path d="M112 323H610" stroke="{t['border']}" stroke-width="2"/>
  <path d="M112 361H187V339H262V382H337V350H412V361H517" fill="none" stroke="{t['signal']}" stroke-width="3"/>
  <text x="544" y="367" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="15" letter-spacing="2">SIGNAL / 01</text>
  <text x="112" y="435" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="13" letter-spacing="2">PROFILE INTERFACE  ·  DESIGN VISUALIZATION, NOT DEVICE TELEMETRY</text>

  <g transform="translate(1036 69)">
    <rect x="-18" y="-18" width="440" height="374" rx="22" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
    <path d="M0 42H50L82 74M0 292H48L83 258M405 42H355L323 74M405 292H357L322 258" fill="none" stroke="{t['signal']}" stroke-opacity=".38" stroke-width="2"/>
    <rect x="87" y="63" width="232" height="214" rx="16" fill="{glow}" stroke="{t['signal']}" stroke-width="2"/>
    <rect x="112" y="88" width="182" height="164" rx="9" fill="{t['background']}" stroke="{t['border']}"/>
    <path d="M133 143H158V117H185V170H212V132H242V151H273" fill="none" stroke="{t['signal']}" stroke-width="3"/>
    <path {sweep} d="M133 183H272" fill="none" stroke="url(#trace)" stroke-width="5"/>
    <text x="134" y="218" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="14" letter-spacing="2">CORE / SIGNAL</text>
    <g stroke="{t['muted']}" stroke-width="2"><path d="M62 94H87M62 132H87M62 170H87M62 208H87M62 246H87M319 94H344M319 132H344M319 170H344M319 208H344M319 246H344"/></g>
    <text x="17" y="324" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="12" letter-spacing="2">INPUT  →  CORE  →  PLATFORM  →  OUTPUT</text>
  </g>
</svg>'''


def terminal(theme: str) -> str:
    t = TOKENS[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="236" viewBox="0 0 1200 236" role="img" aria-labelledby="title desc">
  <title id="title">SIGNALCORE portfolio terminal</title>
  <desc id="desc">Visual identity terminal. READY and STUDY describe portfolio categories, not hardware status.</desc>
  <style>.cursor {{ animation: blink 1.5s step-end infinite; }} @keyframes blink {{ 50% {{ opacity: 0; }} }} @media (prefers-reduced-motion: reduce) {{ .cursor {{ animation: none; }} }}</style>
  <rect width="1200" height="236" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <path d="M0 44H1200" stroke="{t['border']}"/><circle cx="27" cy="22" r="5" fill="{t['signal']}"/><circle cx="47" cy="22" r="5" fill="{t['blue']}"/><circle cx="67" cy="22" r="5" fill="{t['muted']}"/>
  <text x="94" y="28" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="15">signalcore / portfolio interface</text>
  <g font-family="Consolas, ui-monospace, monospace" font-size="18">
    <text x="30" y="85" fill="{t['signal']}">signalcore@elias:~$ identity</text>
    <text x="30" y="116" fill="{t['text']}">NAME     Elias Cheng</text>
    <text x="30" y="146" fill="{t['text']}">FOCUS    Embedded systems / firmware / integration</text>
    <text x="30" y="181" fill="{t['signal']}">signalcore@elias:~$ load portfolio</text>
    <text x="30" y="211" fill="{t['secondary']}">[BUILD] Original host-tested software    [STUDY] Architecture and systems</text>
    <rect class="cursor" x="947" y="192" width="10" height="21" fill="{t['signal']}"/>
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


def footer(theme: str) -> str:
    t = TOKENS[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="105" viewBox="0 0 1200 105" role="img" aria-label="SIGNALCORE footer terminal">
  <rect width="1200" height="105" rx="12" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <text x="30" y="42" fill="{t['signal']}" font-family="Consolas, ui-monospace, monospace" font-size="17">signalcore@elias:~$ status</text>
  <text x="30" y="73" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="16">PORTFOLIO  ACTIVE    ·    FOCUS  EMBEDDED ENGINEERING    ·    SOURCE  github.com/REliasCheng</text>
</svg>'''


def main() -> None:
    for theme in ("dark", "light"):
        t = TOKENS[theme]
        save(BRAND / f"hero-{theme}.svg", hero(theme))
        save(BRAND / f"terminal-{theme}.svg", terminal(theme))
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
        save(FALLBACK / f"contribution-{theme}.svg", fallback(theme, "contribution"))
        save(FALLBACK / f"telemetry-{theme}.svg", fallback(theme, "telemetry"))
    save(BRAND / "hero-static.svg", hero("dark", animated=False))
    print("Generated 21 original SVG assets from assets/brand/tokens.json")


if __name__ == "__main__":
    main()
