# SIGNALCORE maintenance

V2.1 presents the three selected projects as linked Markdown headings with
tested outcomes. The Python desktop picture uses real, cropped Windows Qt
mock-session PNGs in `assets/evidence/`; 900 px and narrower uses independently
composed SVGs. The README collapses the unchanged published telemetry image
behind a native disclosure and relies on GitHub's own contribution graph below
Pinned repositories. The scheduled seven-file asset publication remains active
even though README no longer displays its snake. See
[design system](design-system.md) and [production assets](production-assets.md)
for the preserved implementation and publishing contracts.

The visual system is on the Profile default branch. This document distinguishes the historical checked-in preview from the active production asset branch. It grants no permission to change repository metadata, technical repositories, or the production workflow's permission boundary.

## Generate and validate artwork

From the Profile repository root, run `python scripts/generate_brand_assets.py`, `python -m unittest discover -s tests -v`, and `python scripts/validate_profile.py`. The generator writes brand/card/fallback SVGs deterministically from `assets/brand/tokens.json`; inspect the resulting diff and render both color modes at desktop and 320, 375, 390, 430 and 768 px. V2's desktop and narrow-column hero assets are separate compositions; README selects narrow artwork through 900 px because GitHub retains a profile sidebar at tablet widths. The V1 terminal and category SVGs remain historical generated files but are not used by README. Modify palette values in the token file, regenerate, and recheck contrast. Category labels and membership live in `data/projects.json`; update the README's text and links together with any catalog change, then rerun validation.

## Dated engineering evidence

`data/engineering-evidence.json` records all 14 non-Profile repositories at a dated, exact `main` SHA. Each executable project's PR, source/test paths and successful main CI run were checked against that SHA; Foundations has no invented CI. The README shows seven delivered software projects and three MCU projects with concise code, test and CI links. The other 11 projects retain the **2026-10-27** commit snapshot; the three MCU records were rechecked on **2026-10-28**. These are historical commit-bound results, not live check badges. The dynamic telemetry disclosure remains independently tied to its five monitored current-main workflows.

When a project advances, recheck its new remote `main`, source/test paths, merged PR and successful CI run whose `head_sha` matches that new main. Update the evidence record and catalog together; change the README text and links only after reviewing new behavior and hardware limits. If no matching run exists, say `UNVERIFIED` rather than carrying forward the prior SHA's success. `scripts/validate_profile.py` limits README GitHub links to the 14 roots, three original featured evidence sets and ten verified/MCU source/test/CI sets derived from the index. It pins the currently audited three MCU SHA/CI pairs so an older Host-only snapshot cannot replace the target evidence unnoticed; update these pins only after a new remote audit. The validator also rejects malformed repository paths and mismatched CI/SHA fields.

The MCU scope changed from Host-only to target-build evidence: STC8 has an SDCC MCS-51 compile/link/HEX result but no instruction simulation; STC89 and BlueBridge additionally have generic C52 target-instruction software simulations. All three still lack real board runtime, flashing and peripheral measurements. STC89's generic C52 model does not validate its STC-specific AUXR physical memory switch; BlueBridge's generic C52 model does not validate IAP15 on-chip debugger startup or CT107D wiring. Preserve these limits when editing public copy. The seven `verified` projects remain a separate catalog category from the three `mcu` projects.

## Metrics

Run `python scripts/generate_metrics.py` with public API access. On GitHub Actions the short-lived `github.token` can raise the API rate limit; never print or persist it. The script writes `assets/preview/telemetry-dark.svg`, `telemetry-light.svg`, and `telemetry.json`. It reads all public repository records and the current-main branch/workflow data for the five monitored host workflows. A matching successful workflow SHA is required for `PASS`. Check the `Last refreshed` label and the JSON's `sha` for each row; `STALE` and `UNAVAILABLE` are intentionally visible. If refresh fails, retain the last verified snapshot or switch the README sources to `assets/fallback/telemetry-{dark,light}.svg`; never fabricate current counts or tests.

The preview Metrics Action uploads an artifact only; its daily schedule was removed after production publication went live. It does not commit or publish. The [production asset guide](production-assets.md) describes the separately gated publisher, freshness checks, and failure recovery. Do not run `--publish` from a preview workflow.

## Contribution snake

The preview Snake Action runs Platane/snk `svg-only@v3` on the actual `REliasCheng` contribution graph. Check that both `snake-dark.svg` and `snake-light.svg` exist in the run artifact, parse as SVG, contain no external or executable resource references, and render in both themes before integrating. Use `python scripts/prepare_snake.py <downloaded-artifact-directory>` to add the branded background and reduced-motion rule while preserving the generated graph. The current README leaves the contribution graph to GitHub's native UI; the scheduled `signalcore-assets` contribution files and `assets/fallback/contribution-{dark,light}.svg` remain available but are not displayed in README. `scripts/validate_profile.py` enforces the approved production URLs and fallback files. Do not manually draw a fake contribution history.

After accepting a new real graph, run `python scripts/prepare_static_contribution.py` to regenerate the linked still dark/light graph from exactly those verified SVGs. Check both still files are non-animated and readable. Never hand-edit contribution cells. The preview Action does not update any checked-in README image automatically.

The Action's query-string options use a URL-encoded hash (`%23`) for each color and exactly five `color_dots` levels. The preview Snake Action has no daily schedule; manual dispatch and preview-branch push remain. If a production schedule is missed or fails, retain the last good published files and checked-in static fallback. Workflow dispatch is available on a branch only when GitHub exposes the workflow for manual invocation.

## Diagnose Actions failures

Read the failing job and identify which step failed: checkout/runtime, API access, SVG generation, validation, artifact upload, or production publication. For public API failure, inspect rate-limit and HTTP status without logging a token; leave previous images intact. For a mismatched SHA, show `STALE` rather than `PASS`. For snake failure, keep the static fallback and do not assert animation worked. For an invalid SVG, reject it before README linkage. Preview and validation jobs are read-only; only the production `publish` job has repository `contents: write`, and its publisher script targets `signalcore-assets`, not `main`.

## Restore static fallback

For a reviewed Profile fallback change, point the telemetry `<picture>` sources to `assets/fallback/telemetry-{dark,light}.svg` and contribution sources to `assets/fallback/contribution-{dark,light}.svg`; keep their existing `<img>` fallback. Run the validator and visual review. A production rollback requires a separately reviewed normal revert/forward commit after preserving the current branch state—never a force push or history rewrite.
