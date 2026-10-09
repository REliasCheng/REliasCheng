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


def featured_card(theme: str, kind: str) -> str:
    """Three original diagrams of existing work, not simulated runtime screenshots."""
    t = TOKENS[theme]
    cases = {
        "python": (
            "PYTHON / HOST APPLICATION", "Host application architecture",
            "GUI  →  application core  →  serial boundary", "HOST TESTED / NO DEVICE CLAIM",
            f'''<rect x="823" y="42" width="126" height="114" rx="9" fill="none" stroke="{t['blue']}" stroke-width="2"/>
  <path d="M823 72H949M842 93H916M842 112H902M842 132H923" stroke="{t['blue']}" stroke-width="2"/>
  <path d="M949 98H988M1060 98H1095" stroke="{t['signal']}" stroke-width="2"/>
  <rect x="988" y="68" width="72" height="60" rx="6" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <text x="1001" y="104" fill="{t['signal']}" font-size="13">CORE</text>
  <path d="M1095 75V121M1104 75V121" stroke="{t['muted']}" stroke-width="3"/>''',
        ),
        "embedded-cpp": (
            "C11 / C++11 / PORTABLE CORE", "Embedded software structure",
            "commands  →  state  →  testable modules", "HOST TESTED / NO MCU CLAIM",
            f'''<path d="M810 100H855M938 100H970M1055 100H1090" stroke="{t['signal']}" stroke-width="3"/>
  <rect x="855" y="63" width="83" height="75" rx="7" fill="none" stroke="{t['blue']}" stroke-width="2"/>
  <rect x="970" y="63" width="85" height="75" rx="7" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <rect x="1090" y="63" width="72" height="75" rx="7" fill="none" stroke="{t['blue']}" stroke-width="2"/>
  <text x="867" y="105" fill="{t['blue']}" font-size="14">CMD</text><text x="983" y="105" fill="{t['signal']}" font-size="14">TASK</text><text x="1106" y="105" fill="{t['blue']}" font-size="14">TEST</text>''',
        ),
        "c51": (
            "8051 / BOARD RESOURCE PLANNER", "Resource mapping and conflicts",
            "module needs  →  GPIO / Timer / UART / I2C", "HOST TESTED / NO BOARD CLAIM",
            f'''<rect x="822" y="58" width="115" height="83" rx="7" fill="none" stroke="{t['blue']}" stroke-width="2"/>
  <text x="840" y="105" fill="{t['blue']}" font-size="14">MODULE</text>
  <path d="M937 99H990" stroke="{t['signal']}" stroke-width="3"/>
  <rect x="990" y="51" width="149" height="96" rx="7" fill="none" stroke="{t['signal']}" stroke-width="2"/>
  <path d="M990 82H1139M990 114H1139M1064 51V147" stroke="{t['border']}" stroke-width="2"/>
  <text x="1004" y="73" fill="{t['signal']}" font-size="13">GPIO</text><text x="1075" y="73" fill="{t['signal']}" font-size="13">TIMER</text>
  <text x="1004" y="104" fill="{t['signal']}" font-size="13">UART</text><text x="1075" y="104" fill="{t['signal']}" font-size="13">I2C</text>
  <text x="1004" y="136" fill="{t['warning']}" font-size="13">CONFLICT?</text>''',
        ),
    }
    code, title, flow, boundary, diagram = cases[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="190" viewBox="0 0 1200 190" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title><desc id="desc">Original abstract diagram for {code}. {boundary}.</desc>
  <rect width="1200" height="190" rx="13" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
  <rect width="7" height="190" rx="3" fill="{t['signal']}"/>
  <text x="30" y="40" fill="{t['signal']}" font-family="Consolas, ui-monospace, monospace" font-size="15" letter-spacing="2">{code}</text>
  <text x="30" y="84" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="29" font-weight="650">{title}</text>
  <text x="30" y="119" fill="{t['secondary']}" font-family="Consolas, ui-monospace, monospace" font-size="17">{flow}</text>
  <path d="M30 143H765" stroke="{t['border']}"/>
  <text x="30" y="169" fill="{t['muted']}" font-family="Consolas, ui-monospace, monospace" font-size="14" letter-spacing="1">{boundary}</text>
  <g font-family="Consolas, ui-monospace, monospace">{diagram}</g>
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
        save(FALLBACK / f"contribution-{theme}.svg", fallback(theme, "contribution"))
        save(FALLBACK / f"telemetry-{theme}.svg", fallback(theme, "telemetry"))
    save(BRAND / "hero-static.svg", hero("dark", animated=False))
    print("Generated 29 original SVG assets from assets/brand/tokens.json")


if __name__ == "__main__":
    main()
