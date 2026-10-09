# SIGNALCORE maintenance

This document describes the **preview branch**. It grants no permission to update the default branch, repository metadata, other repositories, or a production asset branch.

## Generate and validate artwork

From the Profile repository root, run `python scripts/generate_brand_assets.py`, `python -m unittest discover -s tests -v`, and `python scripts/validate_profile.py`. The generator writes the original brand/card/fallback SVGs deterministically from `assets/brand/tokens.json`; inspect the resulting diff and render both color modes at desktop and narrow widths. Modify palette values in the token file, regenerate, and recheck contrast. Category labels and membership live in `data/projects.json`; update the README's text and links together with any catalog change, then rerun validation.

## Metrics

Run `python scripts/generate_metrics.py` with public API access. On GitHub Actions the short-lived `github.token` can raise the API rate limit; never print or persist it. The script writes `assets/preview/telemetry-dark.svg`, `telemetry-light.svg`, and `telemetry.json`. It reads all public repository records and the current-main branch/workflow data for the five monitored host workflows. A matching successful workflow SHA is required for `PASS`. Check the `Last refreshed` label and the JSON's `sha` for each row; `STALE` and `UNAVAILABLE` are intentionally visible. If refresh fails, retain the last verified snapshot or switch the README sources to `assets/fallback/telemetry-{dark,light}.svg`; never fabricate current counts or tests.

The preview Metrics Action uploads an artifact only. It does not commit generated data or publish to a production branch. A future daily production publication flow requires separate review of permissions, stale-data handling, and release approval.

## Contribution snake

The preview Snake Action runs Platane/snk `svg-only@v3` on the actual `REliasCheng` contribution graph. Check that both `snake-dark.svg` and `snake-light.svg` exist in the run artifact, parse as SVG, contain no external or executable resource references, and render in both themes before integrating. The README currently uses `assets/fallback/contribution-{dark,light}.svg` intentionally. After a verified preview artifact is committed on the preview branch and the README links are changed, `scripts/validate_profile.py` enforces their existence. Do not manually draw a fake contribution history.

The Action's query-string options use a URL-encoded hash (`%23`) for each color and exactly five `color_dots` levels. If a scheduled run is missed or fails, retain the last good preview files or the static fallback. Workflow dispatch is available on a branch only when GitHub exposes the workflow for manual invocation; the preview branch push is the initial trigger.

## Diagnose Actions failures

Read the failing job and identify which step failed: checkout/runtime, API access, SVG generation, validation, or artifact upload. For public API failure, inspect rate-limit and HTTP status without logging a token; leave previous images intact. For a mismatched SHA, show `STALE` rather than `PASS`. For snake failure, keep the static fallback and do not assert animation worked. For an invalid SVG, reject it before README linkage. Validation uses read-only `contents` permission; preview generators upload artifacts only, so no Action is authorized to push into main.

## Restore static fallback

On the preview branch, point the telemetry `<picture>` sources to `assets/fallback/telemetry-{dark,light}.svg` and contribution sources to `assets/fallback/contribution-{dark,light}.svg`; keep their existing `<img>` fallback. Run the validator and visual review. A production rollback, if later approved, is a normal revert/forward commit after preserving the current branch state—never a force push or history rewrite.
