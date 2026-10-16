# Project instructions

Shared workspace: /home/samsa/projects
Read /home/samsa/projects/AGENTS.md and /home/samsa/projects/workflow/README.md before workflow tasks. This project owns its source, jobs and artifacts.
Use the shared workflow command; keep its model registry authoritative.
Inspect Git status before editing and verify outputs before acceptance.

This project packages two skills and a controlled explanation experiment. The
original teaching skill retains its external shared-workflow dependency. Run
`python3 scripts/validate_release.py` after packaging changes; use
`--source-workspace` only when that external installation is available.

Experimental generation is an adapter-level measurement, not a production PDF
job. Follow `evaluations/methodology.md`: running the full PDF graph on any group
would add unassigned teaching guidance and invalidate the comparison. Production
PDF or coding jobs still use the shared command and explicit lane normally.

Resume `.workflow/experiment-v1` with its frozen inputs. Do not overwrite the run
or regenerate poor texts. Do not change the skill and claim prior outputs tested
the revision. Published `evaluations/records` support offline replay without
model calls. Keep private transport diagnostics and authentication out of Git.

The owner authorized local commits and MIT licensing of the skill text, then
explicitly authorized public GitHub publication of this version. Preserve the
distinction between positive informal review feedback and inconclusive automated
evaluation. Do not publish private transport logs, chats or handbook source files.
