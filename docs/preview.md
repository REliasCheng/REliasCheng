# SIGNALCORE preview

Preview branch: `design/signalcore-profile-preview`, based on the previously clean, aligned `main`. Browse its [README](https://github.com/REliasCheng/REliasCheng/blob/design/signalcore-profile-preview/README.md) or the PR after push. GitHub's actual public Profile continues to use the default branch until a separately approved merge. Do not infer the default Profile rendering from the branch preview.

## Implemented here

- Original dark/light/static vector identity, category cards, terminal, footer, tokens, and reproducible generator.
- Evidence-based classification of all 14 non-profile repositories and a revised README hierarchy.
- Public API metrics snapshot with current-main CI-SHA checks, dated labels and explicit unavailable states.
- Static contribution fallback and a preview-only Platane/snk workflow that produces actual data-derived SVG artifacts.
- Asset/link validation, metrics semantics tests, preview Actions with read-only repository permission, and maintenance documentation.

## Preview limitations

- Animation in GitHub's README/PR renderer may differ from local SVG rendering. Reduced-motion mode intentionally disables decorative movement. Default-branch Profile playback has not been deployed or asserted.
- The metrics image is a checked-in, dated preview snapshot; it does not automatically become live in the Profile. Preview Actions upload artifacts and have no write permission.
- The contribution snake remains a static fallback until the preview Action artifact is verified and linked. No production resource branch, GitHub Pages site, metadata change, pinned-repository change, or edits to technical repositories are included.
- Repository maturity decisions reflect public default-branch evidence inspected for this preview, not a new copyright clearance or hardware test.

## Review gate

Before merge approval, inspect both themes and narrow layouts in the actual GitHub branch/PR renderer, check the SVG and link validator, confirm Action results and CI-state semantics, and review each project category. Separately decide if/how daily assets should be published. Only then consider a normal merge into main. Do not use a force push or rewrite history.
