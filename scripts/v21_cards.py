"""SIGNALCORE V2.1 featured artwork built from verified host-side examples.

The drawings are explanatory diagrams, never screenshots or device traces.
Readable project names and validation boundaries live in README Markdown.
"""

from __future__ import annotations

from v2_brand import TOKENS


def featured_card(theme: str, kind: str, mobile: bool = False) -> str:
    t = TOKENS[theme]
    width = 640 if mobile else 1200
    height = (258 if kind == "python" else 220) if mobile else (232 if kind == "python" else 176)
    sans = "Segoe UI, Arial, sans-serif"
    mono = "Consolas, ui-monospace, monospace"
    edge = f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>'

    if kind == "python":
        title = "Mock serial exchange through the Python host application"
        if mobile:
            content = f'''
<text x="29" y="39" fill="{t['signal']}" font-family="{mono}" font-size="23">PYTHON / PYQT5</text>
<text x="29" y="84" fill="{t['text']}" font-family="{sans}" font-size="32" font-weight="650">A tested mock session</text>
<path d="M29 105H611" stroke="{t['border']}"/>
<text x="29" y="145" fill="{t['secondary']}" font-family="{sans}" font-size="27">GUI  →  Core  →  Mock serial</text>
<rect x="29" y="165" width="582" height="69" rx="7" fill="{t['background']}"/>
<text x="49" y="192" fill="{t['secondary']}" font-family="{mono}" font-size="24">TX  status</text>
<text x="49" y="222" fill="{t['signal']}" font-family="{mono}" font-size="24">RX  MOCK ACK: status</text>'''
        else:
            content = f'''
<path d="M38 42H1162" stroke="{t['border']}"/>
<text x="40" y="31" fill="{t['signal']}" font-family="{mono}" font-size="19">PYTHON / PYQT5 / VERIFIED MOCK SESSION</text>
<text x="40" y="93" fill="{t['text']}" font-family="{sans}" font-size="35" font-weight="650">GUI → Application Core → Serial Boundary</text>
<text x="41" y="128" fill="{t['secondary']}" font-family="{sans}" font-size="23">One flow exercised by the offscreen Qt test</text>
<rect x="40" y="148" width="1120" height="61" rx="7" fill="{t['background']}"/>
<text x="64" y="187" fill="{t['secondary']}" font-family="{mono}" font-size="27">TX  status</text>
<path d="M477 161V196" stroke="{t['border']}"/>
<text x="515" y="187" fill="{t['signal']}" font-family="{mono}" font-size="27">RX  MOCK ACK: status</text>'''
    elif kind == "embedded-cpp":
        title = "C command rejects undersized response without changing device state"
        if mobile:
            content = f'''
<text x="29" y="39" fill="{t['signal']}" font-family="{mono}" font-size="23">C11 / COMMAND FRAMEWORK</text>
<text x="29" y="82" fill="{t['text']}" font-family="{sans}" font-size="31" font-weight="650">No partial state commit</text>
<path d="M29 104H611" stroke="{t['border']}"/>
<text x="29" y="142" fill="{t['secondary']}" font-family="{mono}" font-size="24">INPUT   led off</text>
<text x="29" y="174" fill="{t['warning']}" font-family="{mono}" font-size="23">RESULT  RESPONSE_TOO_SMALL</text>
<text x="29" y="204" fill="{t['signal']}" font-family="{mono}" font-size="24">STATE   LED stays ON</text>'''
        else:
            content = f'''
<text x="39" y="35" fill="{t['signal']}" font-family="{mono}" font-size="19">C11 / COMMAND FRAMEWORK</text>
<text x="39" y="91" fill="{t['text']}" font-family="{sans}" font-size="35" font-weight="650">No partial state commit</text>
<text x="39" y="137" fill="{t['secondary']}" font-family="{mono}" font-size="24">led off</text>
<path d="M184 128H267" stroke="{t['border']}" stroke-width="2"/>
<text x="291" y="137" fill="{t['warning']}" font-family="{mono}" font-size="23">RESPONSE_TOO_SMALL</text>
<path d="M695 128H769" stroke="{t['border']}" stroke-width="2"/>
<text x="789" y="137" fill="{t['signal']}" font-family="{mono}" font-size="24">LED stays ON</text>'''
    elif kind == "c51":
        title = "8051 planner detects UART and keys sharing P3.0 and P3.1"
        if mobile:
            content = f'''
<text x="29" y="39" fill="{t['signal']}" font-family="{mono}" font-size="23">8051 / RESOURCE PLANNER</text>
<text x="29" y="82" fill="{t['text']}" font-family="{sans}" font-size="31" font-weight="650">Shared pins, explicit conflict</text>
<path d="M29 103H611" stroke="{t['border']}"/>
<text x="29" y="140" fill="{t['secondary']}" font-family="{mono}" font-size="24">UART   P3.0 / P3.1 + T1</text>
<text x="29" y="172" fill="{t['secondary']}" font-family="{mono}" font-size="24">KEYS   P3.0 / P3.1 + P3.2</text>
<text x="29" y="204" fill="{t['signal']}" font-family="{mono}" font-size="23">P3.0 / P3.1 → CONFLICT</text>'''
        else:
            content = f'''
<text x="39" y="35" fill="{t['signal']}" font-family="{mono}" font-size="19">8051 / RESOURCE PLANNER</text>
<text x="39" y="90" fill="{t['text']}" font-family="{sans}" font-size="35" font-weight="650">Shared pins, explicit conflict</text>
<rect x="41" y="112" width="355" height="42" rx="5" fill="{t['background']}"/>
<rect x="415" y="112" width="355" height="42" rx="5" fill="{t['background']}"/>
<text x="58" y="141" fill="{t['secondary']}" font-family="{mono}" font-size="21">UART  P3.0/P3.1 + T1</text>
<text x="432" y="141" fill="{t['secondary']}" font-family="{mono}" font-size="21">KEYS  P3.0/P3.1 + P3.2</text>
<text x="803" y="141" fill="{t['signal']}" font-family="{mono}" font-size="24">→ CONFLICT</text>'''
    else:
        raise ValueError(f"Unknown featured kind: {kind}")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">Diagram based on the linked source and host tests; no device output or board verification is implied.</desc>
{edge}{content}
</svg>'''


def featured_mobile_card(theme: str, kind: str) -> str:
    return featured_card(theme, kind, mobile=True)
