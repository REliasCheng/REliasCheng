"""SIGNALCORE V2 artwork: editorial identity and project-specific diagrams."""

from __future__ import annotations

import json
from pathlib import Path

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "assets/brand/tokens.json").read_text(encoding="utf-8"))


def hero(theme: str, animated: bool = True, mobile: bool = False) -> str:
    t = TOKENS[theme]
    style = ('<style>.signal{animation:travel 9s linear infinite}@keyframes travel{to{stroke-dashoffset:-120}}'
             '@media (prefers-reduced-motion:reduce){.signal{animation:none}}</style>') if animated else ''
    motion = ' class="signal"' if animated else ''
    if mobile:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="390" viewBox="0 0 640 390" role="img" aria-labelledby="title desc">
<title id="title">Elias Cheng — embedded software engineer</title><desc id="desc">SIGNALCORE mobile identity with a single signal and controller symbol.</desc>
{style}<rect width="640" height="390" rx="20" fill="{t['background']}"/>
<path d="M32 70H608" stroke="{t['border']}"/><path d="M32 330H608" stroke="{t['border']}"/>
<text x="32" y="48" fill="{t['signal']}" font-family="Consolas, monospace" font-size="22" letter-spacing="3">SIGNALCORE / 02</text>
<text x="32" y="151" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="64" font-weight="700">Elias Cheng</text>
<text x="34" y="201" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="29">Embedded software engineer</text>
<text x="34" y="246" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="25">Testable cores · hardware-aware design</text>
<path d="M35 292H170V275H212V306H254V286H337" fill="none" stroke="{t['border']}" stroke-width="3"/>
<path{motion} d="M35 292H170V275H212V306H254V286H337" fill="none" stroke="{t['signal']}" stroke-width="3" stroke-dasharray="54 66"/>
<g transform="translate(506 263)" fill="none" stroke="{t['signal']}" stroke-width="3"><rect x="0" y="0" width="72" height="58" rx="6"/><path d="M18 -12V0M36 -12V0M54 -12V0M18 58V70M36 58V70M54 58V70M-12 18H0M-12 39H0M72 18H84M72 39H84"/></g>
<text x="34" y="363" fill="{t['muted']}" font-family="Consolas, monospace" font-size="19">C / C++ / Python</text>
</svg>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
<title id="title">Elias Cheng — embedded software engineer</title><desc id="desc">SIGNALCORE identity with one precision controller illustration and restrained signal trace.</desc>
{style}<rect width="1200" height="330" rx="18" fill="{t['background']}"/>
<path d="M42 68H1158M42 276H1158" stroke="{t['border']}" stroke-width="1"/>
<text x="48" y="43" fill="{t['signal']}" font-family="Consolas, monospace" font-size="16" letter-spacing="3">SIGNALCORE  /  EMBEDDED SOFTWARE</text>
<text x="45" y="154" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="69" font-weight="700">Elias Cheng</text>
<text x="49" y="207" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="25">Testable software cores for hardware-aware systems.</text>
<text x="49" y="308" fill="{t['muted']}" font-family="Consolas, monospace" font-size="17">C / C++ / PYTHON     ·     HOST APPLICATIONS     ·     MCU ARCHITECTURE</text>
<g transform="translate(907 59)" fill="none"><rect width="204" height="196" rx="18" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
<rect x="50" y="47" width="104" height="102" rx="9" stroke="{t['signal']}" stroke-width="2"/>
<path d="M69 98H89V78H109V119H132" stroke="{t['signal']}" stroke-width="3"/>
<g stroke="{t['secondary']}" stroke-width="2"><path d="M70 32V47M102 32V47M134 32V47M70 149V164M102 149V164M134 149V164M35 70H50M35 100H50M35 130H50M154 70H169M154 100H169M154 130H169"/></g></g>
<path d="M600 228H706V205H770V241H834V228H897" fill="none" stroke="{t['border']}" stroke-width="2"/>
<path{motion} d="M600 228H706V205H770V241H834V228H897" fill="none" stroke="{t['signal']}" stroke-width="2" stroke-dasharray="48 72"/>
</svg>'''


def featured_card(theme: str, kind: str, mobile: bool = False) -> str:
    t = TOKENS[theme]
    w, h = (640, 306) if mobile else (1200, 240)
    small = mobile
    x = 30 if small else 38
    title_size = 31 if small else 36
    top = 47 if small else 51
    title_y = 97 if small else 109
    desc_y = 134 if small else 151
    title = {'python':'Python Host Application','embedded-cpp':'Embedded C/C++ Core','c51':'C51 Board Resource Planner'}[kind]
    kicker = {'python':'01 / HOST APPLICATION','embedded-cpp':'02 / PORTABLE CORE','c51':'03 / RESOURCE PLANNER'}[kind]
    subtitle = {'python':'GUI · application core · serial boundary','embedded-cpp':'Commands · ring buffer · state','c51':'GPIO · Timer · UART · I²C'}[kind]
    if kind == 'python':
        # A framed window and an explicit serial boundary make the host architecture visible.
        art = (f'<rect x="31" y="172" width="360" height="105" rx="9" fill="{t["background"]}" stroke="{t["border"]}"/><path d="M31 198H391" stroke="{t["border"]}"/>'
               f'<circle cx="48" cy="185" r="4" fill="{t["signal"]}"/><text x="50" y="237">GUI</text><path d="M121 231H165" stroke="{t["signal"]}" stroke-width="2"/>'
               f'<rect x="171" y="212" width="91" height="42" rx="5" fill="{t["panel"]}" stroke="{t["signal"]}"/><text x="188" y="238">CORE</text>'
               f'<path d="M267 231H305" stroke="{t["signal"]}" stroke-width="2"/><path d="M310 208V254" stroke="{t["secondary"]}" stroke-width="2" stroke-dasharray="5 5"/>'
               f'<text x="321" y="237">SERIAL</text>') if small else (
               f'<rect x="689" y="45" width="435" height="154" rx="9" fill="{t["background"]}" stroke="{t["border"]}"/>'
               f'<path d="M689 77H1124" stroke="{t["border"]}"/><circle cx="707" cy="61" r="4" fill="{t["signal"]}"/>'
               f'<text x="719" y="132">GUI</text><path d="M776 123H829" stroke="{t["signal"]}" stroke-width="2"/>'
               f'<rect x="834" y="99" width="97" height="45" rx="5" fill="{t["panel"]}" stroke="{t["signal"]}"/><text x="851" y="127">CORE</text>'
               f'<path d="M938 123H985" stroke="{t["signal"]}" stroke-width="2"/><path d="M989 95V152" stroke="{t["secondary"]}" stroke-width="2" stroke-dasharray="5 5"/>'
               f'<text x="1004" y="132">SERIAL</text><text x="704" y="184" fill="{t["muted"]}" font-size="15">MOCKABLE APPLICATION BOUNDARY</text>')
    elif kind == 'embedded-cpp':
        # A branching state path is distinct from the window and the planner matrix.
        base = 169 if small else 51
        ox = 34 if small else 731
        gap = 119 if small else 118
        labels = [('CMD',0),('BUFFER',1),('STATE',2)]
        art = ''.join(f'<rect x="{ox+i*gap}" y="{base+40}" width="103" height="55" rx="5" fill="none" stroke="{t["signal"] if i==1 else t["border"]}" stroke-width="2"/><text x="{ox+i*gap+14}" y="{base+74}">{label}</text>' for label,i in labels)
        art += f'<path d="M{ox+103} {base+67}H{ox+gap}M{ox+gap+103} {base+67}H{ox+2*gap}" stroke="{t["signal"]}" stroke-width="2"/>'
        art += f'<path d="M{ox+gap+51} {base+40}V{base+13}H{ox+2*gap+51}V{base+40}" fill="none" stroke="{t["secondary"]}" stroke-width="2"/>'
        art += f'<text x="{ox+2*gap+16}" y="{base+6}" fill="{t["muted"]}" font-size="15">NO PARTIAL COMMIT</text>'
    else:
        # A resource matrix makes allocation and conflict detection the subject.
        ox, oy = (33,143) if small else (726,49)
        cw = 73 if small else 90
        labels = ['GPIO','TIMER','UART','I²C']
        art = f'<text x="{ox}" y="{oy+22}" fill="{t["muted"]}" font-size="16">MODULE NEEDS</text>'
        for i,label in enumerate(labels):
            xx=ox+i*cw
            art += f'<rect x="{xx}" y="{oy+39}" width="{cw-4}" height="58" rx="4" fill="{t["background"]}" stroke="{t["border"]}"/><text x="{xx+7}" y="{oy+73}" font-size="{14 if small else 16}">{label}</text>'
        art += f'<path d="M{ox} {oy+115}H{ox+4*cw-4}" stroke="{t["signal"]}" stroke-width="2"/><text x="{ox}" y="{oy+142}" fill="{t["signal"]}" font-size="16">CONFLICT CHECK  →  REPORT</text>'
    art_y = ''
    if small and kind == 'embedded-cpp':
        desc_y = 134
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">Original {kind} architecture diagram; implementation scope and verification links follow in README text.</desc>
<rect width="{w}" height="{h}" rx="14" fill="{t['panel']}" stroke="{t['border']}"/>
<path d="M{x} 24H{w-x}" stroke="{t['border']}"/><text x="{x}" y="{top}" fill="{t['signal']}" font-family="Consolas, monospace" font-size="{19 if small else 17}" letter-spacing="2">{kicker}</text>
<text x="{x}" y="{title_y}" fill="{t['text']}" font-family="Segoe UI, Arial, sans-serif" font-size="{title_size}" font-weight="650">{title}</text>
<text x="{x}" y="{desc_y}" fill="{t['secondary']}" font-family="Segoe UI, Arial, sans-serif" font-size="{22 if small else 21}">{subtitle}</text>
<g font-family="Consolas, monospace" font-size="{18 if small else 18}" fill="{t['text']}">{art}</g>
</svg>'''


def featured_mobile_card(theme: str, kind: str) -> str:
    return featured_card(theme, kind, mobile=True)


def footer(theme: str) -> str:
    t = TOKENS[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="46" viewBox="0 0 1200 46" role="img" aria-label="SIGNALCORE closing line">
<path d="M0 15H1200" stroke="{t['border']}"/><path d="M0 15H70" stroke="{t['signal']}" stroke-width="2"/>
<text x="2" y="38" fill="{t['muted']}" font-family="Consolas, monospace" font-size="14">SIGNALCORE  /  ELIAS CHENG</text>
</svg>'''
