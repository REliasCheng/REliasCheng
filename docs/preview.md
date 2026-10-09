# SIGNALCORE preview

Historical preview: `design/signalcore-profile-preview` was merged through [PR #1](https://github.com/REliasCheng/REliasCheng/pull/1) on 2026-10-09. The current public Profile is served from `main`. The notes below record the preview stage; they are not a claim that later GitHub rendering or production asset publication has been verified. Dynamic assets remain checked-in snapshots, not a live updater.

## Implemented here

- Original dark/light/static vector identity, three distinct featured project cards, category cards, staged typing terminal with reduced-motion/static fallback, footer, tokens, and reproducible generator.
- Evidence-based classification of all 14 non-profile repositories and a revised README hierarchy.
- Public API metrics snapshot with current-main CI-SHA checks, dated labels and explicit unavailable states.
- A Platane/snk contribution animation generated from the actual public graph in [preview run 37899433686](https://github.com/REliasCheng/REliasCheng/actions/runs/37899433686), validated and checked into the preview branch with a static fallback.
- Asset/link validation, metrics semantics tests, preview Actions with read-only repository permission, and maintenance documentation.
- A visible-by-default contribution graphic, compact metrics panel, and [future production publication design](production-assets.md) with a dry-run and failure tests. Production publication is not active.

## Preview limitations

- Animation in GitHub's README renderer may differ from local SVG rendering. Reduced-motion mode intentionally disables decorative movement. A completed browser QA of default-branch playback has not yet been recorded.
- The metrics image is a checked-in, dated preview snapshot; it does not automatically become live in the Profile. Preview Actions upload artifacts and have no write permission.
- The contribution snake is a checked-in preview artifact, not a daily-updating production asset. No production resource branch, GitHub Pages site, metadata change, pinned-repository change, or edits to technical repositories are included.
- Repository maturity decisions reflect public default-branch evidence inspected for this preview, not a new copyright clearance or hardware test.

## Review gate

The preview merge is complete. For subsequent changes, inspect both themes and narrow layouts in the GitHub renderer, check the SVG/link validator, confirm Actions at the changed SHA and CI-state semantics, and review each project category. Daily asset publication remains a separate gated decision. Do not use a force push or rewrite history.
