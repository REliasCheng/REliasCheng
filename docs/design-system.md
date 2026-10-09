# SIGNALCORE design system

## Brand concept

SIGNALCORE is a compact embedded-engineering interface: routing traces, a signal waveform, restrained terminal language, and clear evidence labels. It is a visual identity for this Profile preview, not a claim of verified hardware. All artwork in `assets/brand`, `assets/cards`, and `assets/fallback` is generated from repository-authored vector geometry and tokens; no third-party image, font, logo, or course material is imported. The separately generated contribution animation uses Platane/snk and actual GitHub contribution data under that tool's own terms.

## Palette

`assets/brand/tokens.json` is authoritative. Dark uses background `#0B111B`, panel `#142235`, border `#25394C`, text `#F0F6FF`, signal `#61DCE6`, and verification green `#67D9C5`. Light uses background `#F5F8FC`, white panels, border `#D0DFEA`, text `#102033`, signal `#087F95`, and verification green `#0F765E`. Muted text is for secondary labels, never the sole expression of status. All semantic text colors meet at least 4.5:1 contrast against their panel background.

## Typography, spacing, and borders

Use system Segoe UI/Arial for readable narrative and Consolas/ui-monospace for terminal/status labels. No font download. The 8 px spacing unit yields 16 px card gaps and 32 px section intervals. Fine borders are 1 px, active signal strokes 2 px. Corners are restrained; no badges or decorative emoji.

## Component rules

- Hero: one identity statement and one schematic MCU/signal motif. It is not a hardware photograph.
- Terminal: a staged whoami/portfolio introduction with original-work and host-test labels, never simulated test output. The alternate static SVG contains all meaningful text without animation.
- Featured cards: three distinct abstract diagrams for the host app, portable C/C++ modules, and the 8051 planner. Each has a compact dark/light SVG selected below 600 px so labels do not become microscopic. Their linked Markdown text states each project's actual evidence boundary; the SVGs are not runtime screenshots.
- Category card: one visual heading per maturity group; details and evidence remain selectable text in the README.
- Metrics: dated public API snapshot in a compact mobile-readable panel. Show source, refresh time, current-main SHA relationship and failure/unavailable states. A count is not an engineering score.
- Contribution: actual GitHub data only. The preview snake was produced by Platane/snk from the public contribution graph, validated, and framed with these palette tokens. The default view is animated; linked still dark/light graphs are derived from that same verified SVG and contain no snake animation. A neutral `<img>` fallback also remains.
- Footer and dividers: quiet navigation, not a substitute for content.

## Dark and light policy

Each displayed component has dark and light SVG variants. GitHub `<picture>` sources select by `prefers-color-scheme`; its `<img>` points to a file that already exists on the preview branch. Standalone SVGs have their own background fill. No external image URL is needed. The default Profile page remains unchanged before a separately approved merge.

## Animation and accessibility

The hero route and signal sweep use low-amplitude CSS motion. The terminal reveals eight lines over roughly seven seconds, then shows a blinking prompt. In a GitHub README, SVG-internal motion media queries are not reliable enough alone: each animated `<picture>` places `prefers-reduced-motion: reduce` dark/light static sources **before** animated sources. This applies to hero, terminal and contribution graph. The snake is separate data-derived animation, visible by default, with both direct still-image links and a neutral `<img>` fallback. Essential identity, project categories, links, evidence boundaries and metrics labels are HTML/text. Every picture has alt text. The preview is checked at desktop and narrow widths in both color schemes; actual default-branch Profile playback requires release-stage confirmation.

## Project category system

`data/projects.json` is authoritative for group membership: featured engineering (3), current MCU work (3), architecture labs (5), exploration labs (2), foundations (1). Group membership reflects public implementation and evidence, not a score or ranking. Architecture labs remain documentation-first. Robotics includes third-party integration; foundations remains documentation. No listed project is called hardware-validated merely because its host tests pass.

## Status semantics

For a monitored host workflow, `PASS` means its successful run SHA matches the current `main` SHA. `FAIL` means the matching run concluded unsuccessfully. `PENDING` means the matching run is not complete. `STALE` means only an older successful run was found. `NOT VERIFIED` means no eligible success was found. `UNAVAILABLE` means the public API response could not be trusted. None establishes target build, runtime, hardware, security, or production quality.

## SVG generation and maintenance

Run `python scripts/generate_brand_assets.py` after token or geometry edits, then `python scripts/validate_profile.py` and visual review. `scripts/generate_metrics.py` reads public GitHub API data; it refuses an empty repository inventory and never substitutes zero for an API failure. Its output is a dated snapshot. The snake workflow uses the documented Platane/snk SVG-only v3 interface with five contribution colors. See [maintenance](maintenance.md) and [future production assets](production-assets.md) for update, failure, dry-run and fallback steps. A production asset branch or Pages site is not part of this preview.
