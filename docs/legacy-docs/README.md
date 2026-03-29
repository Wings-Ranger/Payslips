# Legacy Docs - Archived Reference

This folder contains documentation snapshots that were superseded by the GUI and packaging refactor.

These files are kept for historical/reference purposes only. They should not be treated as current implementation guidance.

## Archive Scope

- Source snapshot: pre-GUI documentation from commit `f7d6fcf`
- Reason archived: the application moved from a console-first flow to a GUI-first flow with a reusable processing service and packaged-config support

## Contents

- [readme-history/README.md](readme-history/README.md): commit-by-commit archive of historical README snapshots.
- [pre-gui/root-README.md](pre-gui/root-README.md): old root project README
- [pre-gui/README.md](pre-gui/README.md): old technical overview
- [pre-gui/coding-techniques/README.md](pre-gui/coding-techniques/README.md): old coding-techniques index
- [pre-gui/code-blocks/README.md](pre-gui/code-blocks/README.md): old code-block index
- [pre-gui/code-blocks/config-json.md](pre-gui/code-blocks/config-json.md): old config schema note
- [pre-gui/code-blocks/load-config.md](pre-gui/code-blocks/load-config.md): old config-loading note
- [pre-gui/code-blocks/process-payslips-bat.md](pre-gui/code-blocks/process-payslips-bat.md): old console-launcher note
- [pre-gui/code-blocks/run-entrypoint.md](pre-gui/code-blocks/run-entrypoint.md): old run() orchestration note
- [pre-gui/coding-techniques/config-driven-paths-and-behavior.md](pre-gui/coding-techniques/config-driven-paths-and-behavior.md): old config technique note
- [pre-gui/coding-techniques/dataframe-transformation-pipeline.md](pre-gui/coding-techniques/dataframe-transformation-pipeline.md): old pipeline technique note
## Beginner Ramp-Up

This is a legacy document. For beginner-friendly foundations, start with [../building-blocks/README.md](../building-blocks/README.md).
Then return here only if you specifically need the pre-GUI historical implementation details.

## When This Is Not The Best Fit

- This file documents an older architecture and may not match the current app flow.
- Prefer current docs in docs/code-blocks and docs/coding-techniques for active implementation work.
- Use this as reference context, not as a copy-paste template.
