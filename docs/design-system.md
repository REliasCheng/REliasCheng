# SIGNALCORE V2.1 design system

## Portfolio clarity polish

V2.1 keeps the V2 hero, palette and 900 px narrow-column switch. The desktop
Python feature now uses a **real Qt window capture** from the original host
application running with its in-memory mock backend. The capture shows the
`status` / `MOCK ACK: status` exchange; it is not a device screenshot. At narrow
widths, a separately composed SVG presents the same tested flow with larger
type. The C/C++ and C51 graphics show specific outcomes exercised by their
host tests: response-buffer failure without state mutation and UART/key pin
conflict. Project names, value and verification limits remain readable Markdown.

The README no longer repeats project names inside images. Public metrics remain
available in a native GitHub disclosure below the projects; the same production
telemetry SVG and JSON continue to publish. The README contribution snake is
retired because GitHub's native graph appears immediately below Pinned repos.
Snake generation, static fallbacks and all seven production assets remain intact.
The footer retains one maintenance entry and the license boundary.

The expanded 520 px telemetry SVG is small when scaled into a phone's README
column. The disclosure therefore keeps its status semantics next to the panel
and links to each original-size production SVG for zoomable inspection. Those
links share the same strict production-asset allowlist as the displayed image.

The GUI captures were taken from `Python-Host-Application-Lab` on Windows with
`DemoMockSerialBackend`, using its public `MainWindow`, `connect_serial`,
`send_command('status')` and `poll_serial` methods. The dark capture uses Qt's
Fusion palette with SIGNALCORE colors; neither image represents a physical
serial connection. The capture script and full-window evidence are in the
V2.1 audit directory; these checked-in PNGs are the top 900 × 160 pixels of
the real 900 × 560 window.

## Direction

SIGNALCORE V2 is an editorial embedded engineering portfolio. Identity and selected implementations lead; MCU work, architecture studies, public evidence and contribution activity follow. The controller drawing is original vector geometry, not a board photograph or runtime trace. The three featured diagrams describe architecture and are not application screenshots.

Two directions were considered before implementation:

- **Minimal Engineering:** monochrome editorial layout, maximum whitespace, little brand imagery. It reads quickly but loses some of the embedded identity established by SIGNALCORE.
- **Refined SIGNALCORE:** navy and controlled cyan with one controller symbol, compact project-specific diagrams and quiet Markdown sections. Selected for stronger identity with comparable reading speed and a dedicated mobile composition.

## Palette and type

`assets/brand/tokens.json` remains authoritative. Dark: background `#0B111B`, panel `#142235`, text `#F0F6FF`, signal `#61DCE6`. Light: background `#F5F8FC`, panel `#FFFFFF`, text `#102033`, signal `#087F95`. Other semantic colors retain their documented roles. The profile validator requires at least 4.5:1 panel contrast for text roles.

Segoe UI/Arial carries names, titles and narrative. Consolas/monospace is reserved for compact technical labels. The token spacing unit is 8 px. Fine borders use 1 px; signal paths use 2 px. The cards rely on a single restrained frame and internal architecture diagrams rather than bright full-card outlines.

## Components

- **Hero:** 1200 × 330 desktop and a separately composed 640 × 390 narrow-column asset. The narrow layout places the name and role above the signal and controller, avoiding desktop scaling. GitHub keeps a profile sidebar at tablet widths, so README selects narrow-column sources through a 900 px viewport. Both themes have animated and static files; animation is a slow signal path with a reduced-motion static source placed first in README `<picture>`.
- **Identity status:** one short Markdown paragraph after the hero. The V1 terminal animation is retired from the page; old terminal assets remain in the repository as historical artifacts.
- **Selected engineering:** three 1200 × 240 desktop and 640 × 306 mobile diagrams. Python uses an application window with a mockable serial boundary; C/C++ uses a command, buffer and state path; C51 uses a resource matrix and conflict check. Implementation and validation limits stay in readable Markdown alongside Source, Tests, CI and Design links.
- **MCU and research:** Markdown headings and concise linked lists replace large category banners. The V1 category assets remain historical and unused.
- **Public evidence:** the approved production telemetry image remains a dated public GitHub API snapshot. `PASS` is bound to the current `main` SHA for a monitored host workflow, not target or hardware validation.
- **Contribution:** the production snake and both data-derived static variants remain. Reduced-motion sources precede animated sources. The footer is a short Markdown navigation line.

## Evidence and production boundary

`data/projects.json` keeps the 14 non-profile repositories and maturity classification. `data/featured-evidence.json` keeps the exact Source, Tests, CI and Design paths. SVGs contain no remote image, script or executable content. The README keeps the six approved raw SVG sources and local fallback images. The `signalcore-assets` branch and its seven-file scheduled publication workflow are unchanged by V2. See [maintenance](maintenance.md) and [production assets](production-assets.md) for release behavior.

Generate with `python scripts/generate_brand_assets.py`; then run `python -m unittest discover -s tests -q` and `python scripts/validate_profile.py`. Review actual GitHub rendering in both themes and at 320, 375, 390, 430, 768 and desktop widths before merging.
