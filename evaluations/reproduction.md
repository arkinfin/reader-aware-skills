# Replay and new studies

## Offline replay

From the repository root, with Python 3.10 or later:

```bash
python3 evaluations/analyze.py --evidence-dir evaluations/records
python3 scripts/validate_release.py
```

No model, API key, network, or shared workflow is needed for this replay. The
first command verifies all 60 outputs, 21 judgments, 48 comparisons, frozen
inputs, anonymous mapping, successful attempts and the infrastructure amendment
before writing `summary.json` and `results-data.md`. It recomputes scores; it does
not generate new explanations or decide whether the judge's reasoning is true.
The second command performs static package and candidate-file checks with
explicit skipped checks for the external runtime. It does not validate learning.

`records/` contains the exact generation/evaluation prompts, blind packets,
randomized mapping/order, locked manifest and successful attempt records.
Transport event streams, thread IDs and temporary command paths were removed
from public attempts. Final texts, hashes, timestamps, usage and request labels
remain. See `records/publication.json` for the publication transformation.
Private preflight logs, global guidance text, authentication, original workflow
code, full handbooks and conversation archives are excluded. Original local
workspace paths remain in exact provenance records; they are not installation
requirements for the standalone writing skill.

The runner was amended after generation and before any judging to close
deterministic validation defects. The original runner, manifest, protocol and
exact patch are in `records/infrastructure/`. The analyzer verifies that cells,
task/prompt hashes and generation configuration stayed unchanged. It also checks
each parsed judgment against its actual raw successful response. Primary scores
were not adjusted by later technical adjudication.

## New model execution

The live `run.py` is an owner-environment experiment tool. It reuses the external
shared workflow's authenticated Codex CLI adapter and authoritative model
registry. It expects this project under that workspace's `repos/` directory and
uses its installed Python dependencies. That runtime has no public download
location and is not bundled here. This is not a claim of one-command live
reproduction on arbitrary machines.

The original run remains under `.workflow/experiment-v1/` on the owner's machine.
Resuming it uses the same frozen inputs; `prepare` refuses to overwrite it.
For a genuinely new study, use a separate project/run with fresh output and
judgment directories. Published prior outputs must not be treated as a new run.
Register new task/skill/rubric revisions before generation or scoring and retain
the old evidence. Do not lower the model or change effort after quota failure.

For an appropriately prepared fresh owner-environment project, the stages are:

```bash
python3 evaluations/run.py preflight
python3 evaluations/run.py prepare
python3 evaluations/run.py generate
python3 evaluations/run.py blind
python3 evaluations/run.py evaluate
python3 evaluations/analyze.py
```

These commands spend the existing model subscription quota. They do not authorize
a paid external service. Preflight must be inspected and its actual common
background accepted in a local `isolation-accepted.json` before generation.
Flags are not proof of successful context isolation. The measured study retains
the observed common catalog and global rules as a disclosed shared background.

Do not run the production PDF graph on experimental groups: its writer guidance,
revisions, teaching review and model fallback would change the interventions.
Production teaching work still uses the existing `bin/workflow` PDF lane normally.
The original teaching skill's live workflow and the simplified experimental
rigor module are different interventions.
