# SIGNALCORE preview

Historical preview: `design/signalcore-profile-preview` was merged through [PR #1](https://github.com/REliasCheng/REliasCheng/pull/1) on 2026-10-09. The notes below describe that preview stage, not the current release state. The public Profile now reads the independent `signalcore-assets` branch; a [real scheduled production run](https://github.com/REliasCheng/REliasCheng/actions/runs/38042558639) succeeded on 2026-10-10. Dark-theme and reduced-motion automatic selection in a browser remain unverified.

## Implemented here

- Original dark/light/static vector identity, three distinct featured project cards, category cards, staged typing terminal with reduced-motion/static fallback, footer, tokens, and reproducible generator.
- Evidence-based classification of all 14 non-profile repositories and a revised README hierarchy.
- Public API metrics snapshot with current-main CI-SHA checks, dated labels and explicit unavailable states.
- A Platane/snk contribution animation generated from the actual public graph in [preview run 37899433686](https://github.com/REliasCheng/REliasCheng/actions/runs/37899433686), validated and checked into the preview branch with a static fallback.
- Asset/link validation, metrics semantics tests, preview Actions with read-only repository permission, and maintenance documentation.
- A visible-by-default contribution graphic, compact metrics panel, and the then-future [production publication design](production-assets.md) with a dry-run and failure tests. Publication was not active at this preview stage.

## Preview limitations

- Animation in GitHub's README renderer may differ from local SVG rendering. Reduced-motion mode intentionally disables decorative movement. A completed browser QA of default-branch playback has not yet been recorded.
- At the preview stage, the metrics image was a checked-in, dated snapshot; preview Actions uploaded artifacts and had no write permission. The current Profile uses a separately published live asset branch.
- At the preview stage, the contribution snake was checked in, not a daily-updating asset. That preview did not create a production resource branch, GitHub Pages site, metadata change, pinned-repository change, or technical-repository edit; later reviewed work activated the resource branch.
- Repository maturity decisions reflect public default-branch evidence inspected for this preview, not a new copyright clearance or hardware test.

## Review gate

The preview merge is complete. For subsequent changes, inspect both themes and narrow layouts in the GitHub renderer, check the SVG/link validator, confirm Actions at the changed SHA and CI-state semantics, and review each project category. Daily asset publication was separately approved and activated after this preview; any new scope still needs review. Do not use a force push or rewrite history.
