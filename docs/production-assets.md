# Future SIGNALCORE dynamic-asset publication

This is a design and dry-run specification, **not a release authorization**. The current Profile still reads checked-in preview SVGs. `signalcore-assets` does not exist and this branch does not create it. No preview workflow has `contents: write`.

## Branch and first publication gate

1. Obtain separate approval for production publication and confirm the exact approved `main` SHA, repository URL, and branch-protection policy.
2. Initialize `signalcore-assets` as an independent resource branch under a separately reviewed, normal Git operation. Do not alter `main` or rewrite any history. Preserve its first committed asset set as a recoverable version.
3. Generate both snake modes from the real contribution graph and both metrics modes from the public API in one job. The metrics JSON is part of the published set. Validate XML, safety, sizes, fresh branch SHAs, and every required file before any commit.
4. Run `python scripts/publish_assets.py --dry-run --source <validated-directory>` and review its output. It needs only read access. Missing branch is reported as a gate, never created by the script.
5. Only after separate release approval, run the publisher's gated `--publish --approved-main-sha <exact-40-character-SHA>` path. It clones the **existing** resource branch into a temporary directory, changes only the five validated assets, commits only if bytes changed, and performs a normal fast-forward push. A remote race/non-fast-forward fails closed; no force/rebase/retry-overwrite.
6. Confirm both published asset URLs return SVG/JSON with correct MIME and payload, then switch README references in a separately reviewed normal commit. Until that URL check passes, keep the checked-in preview and static fallbacks. The first approved Profile merge is a separate decision.

The future production workflow should be a single serial publishing job with a repository-scoped concurrency group. Scheduled Actions run from the default branch; a `schedule` key present only on this preview branch does **not** provide daily production updates. The future job should receive `contents: write` only after validation and an approval gate. Preview generation and PR validation retain `contents: read`; never use `pull_request_target` to execute untrusted PR code with write credentials.

## Failure behavior

An API timeout, error page, empty inventory, missing dark/light file, invalid or oversized SVG, stale CI SHA, unexpected remote, absent resource branch, or concurrent non-fast-forward stops the publication. The last good branch commit and its timestamp remain intact. A failed run must not refresh the displayed date or claim `PASS`. A normal forward/revert commit can restore a previous good set after reviewing its contents; do not force-push.

The dated metrics panel reports public repository count, primary language **by repository**, and five host-CI workflows matched to their respective current `main` SHA. It is not real-time telemetry, a language-byte ratio, a hardware-validation result, or an engineering-quality score. The contribution animation is generated from the public graph, not invented activity. Keep static fallbacks permanently. Reduced-motion users should be offered a static contribution fallback if the third-party animation cannot be reliably suppressed in GitHub's renderer.
