# SIGNALCORE portfolio baseline

This is a historical pre-preview baseline, not a statement of current Profile content. The visual Profile merged to `main` through PR #1 on 2026-10-09; its checked-in dynamic images are still dated snapshots.

Read-only baseline recorded on 2026-10-09 (Asia/Shanghai), before preview-branch changes. GitHub listed 15 public repositories. All 15 local checkouts had clean worktrees and `HEAD` equal to GitHub `main` when inspected. Their root READMEs existed; 31 SVG files were tracked across the 15 current branches. This is a presentation audit, not a historical rights clearance or a new hardware validation.

| Role | Repositories | Evidence boundary |
| --- | --- | --- |
| Profile | `REliasCheng` | Existing hero SVG and README; project order was inconsistent with maturity |
| Featured engineering | `Python-Host-Application-Lab`, `Embedded-C-Cpp-Learning`, `C51-Board-Lab` | Original code and automated host verification; no device validation |
| Current MCU work | `STC8-MCU-Learning`, `stc89c52-learning`, `BlueBridgeCup-MCU` | Partial original cores/policies; target builds and board evidence not established here |
| Architecture labs | `ARM-Cortex-M-Development-Lab`, `FreeRTOS-Embedded-Lab`, `LVGL-Embedded-GUI-Lab`, `Wireless-IoT-Embedded-Lab`, `Embedded-OTA-Update-Lab` | Public default branches mainly document architecture, not completed firmware |
| Exploration labs | `Embodied-Robotics-Arm-Lab`, `ARM-Linux-Embedded-Lab` | Integration/source review or architecture study; robotics includes third-party code |
| Foundations | `Embedded-Systems-Foundations` | Documentation and knowledge navigation, not executable software |

## Findings

- Existing Profile places architecture-only labs before implemented work, repeats them in the roadmap, labels Python Host as exploration, and leaves the implemented STC8 communication core in a pure roadmap.
- Technical READMEs share an engineering snapshot and architecture idiom, but use many emoji headings and differently named snapshot tables. Their individual SVGs should be preserved; this preview does not rewrite those repositories.
- Five repositories have host CI workflows on current main: Embedded C/C++, C51 Board, STC89, STC8 and Python Host. A workflow's existence does not prove the latest main SHA passed. The dynamic monitor must compare run SHA with current branch SHA.
- BlueBridge, Foundations and architecture labs have no host CI workflow in this baseline. Documentation-only work must not receive a fabricated test status.
- Profile currently has one animated, dark-only SVG. A light-mode counterpart, static fallback, consistent project hierarchy and maintenance rules are missing.
- Repository descriptions and topics were read from GitHub; no metadata was changed. Proposals belong in `metadata-proposals.md` and require separate approval.

## Preservation decisions

Keep all existing repository SVGs and README content untouched during this Profile preview. Keep the Profile main README and existing hero unchanged until explicit merge approval. Do not import course, vendor, font or external image assets. Public README claims remain bounded by each repository's current implementation and tests; historical rights were not re-audited.
