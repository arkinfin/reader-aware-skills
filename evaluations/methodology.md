# Exploratory evaluation protocol

This protocol is written before experimental generation or scoring. Correctness,
comprehensibility, and learning gain are different outcomes. This evaluation
addresses the first two through model judgment; it does not measure learning.
Earlier informal positive feedback motivates the design and is not A/B evidence.

## Design and frozen inputs

The mathematics study uses three tasks (concept, method choice, formal derivation)
and a 2×2 design: A common task only, B common task plus rigor guidance, C common
task plus reader-aware writing, D both modules. D does not load the full teaching
skill. Rigor guidance checks valid reasoning and necessary inference bridges;
those bridges may also improve comprehension. This is an operational prompt
intervention, not an identification of psychologically pure mechanisms.

The generalization study uses two control-theory tasks and two machine-learning
tasks, comparing A and C only. Three repetitions produce 36 mathematics and 24
cross-domain outputs. Each repetition is a balanced 20-output batch; only a
whole balanced batch may define a reduced completed sample, with the decision
made before reading scores. A failed batch is retained and resumed, not silently
discarded. No result-dependent stopping or subgroup regeneration is permitted.

All conditions receive the same task JSON, reader, facts, goal and soft length
target. Knowledge packs are newly written fact inventories, not rewrites of
finished textbook prose. The mathematics topics come from actual Math I source;
no textbook chapter, private conversation, or third-party exposition is included.
The packs intentionally retain conditions and definitions. This may create a
correctness ceiling; facts will not be removed to manufacture a rigor advantage.

The R module is in `prompts/rigor.txt`. C uses the complete frozen standalone
`reader-aware-writing/SKILL.md`, including its scope limits. Modules follow the
common task and facts, with R before C in D. Both factors act within a single
generation; B and D do not receive another review or revision call. Prompt length
and instruction salience are therefore potential confounds, not separately
controlled variables. The full original teaching skill is preserved separately.

## Execution and recovery

`run.py prepare` freezes hashes, exact prompts, configured model, effort and
random order. Seed 20261016 controls scheduling; a separate deterministic stream
controls blind aliases and pair order. This is not the provider's sampling seed.
Temperature, sampling seed, and immutable backend revision are not exposed.
The CLI model label reflects the request, not independent backend attestation.

Generation and evaluation use the existing authenticated Codex CLI through the
shared workflow's adapter. Model selection comes from its authoritative registry;
the orchestrator uniformly sets generation effort to Medium because the tasks
require technical dependency and derivation reasoning. No model fallback is
allowed. Quota exhaustion saves the state; it does not authorize a weaker model
or a paid external service.

The PDF graph is deliberately not executed for these experimental texts: its
automatic writer guidance, revisions, teaching reviewers and supply fallback
would alter the treatment conditions. The shared `bin/workflow` entry point and
configuration were inspected; this experiment is a controlled adapter-level
study, not a claim that a complete PDF or coding lane was run. Checkpoints,
frozen prompts, finite retries and actual attempts are stored locally under
`.workflow/experiment-v1/`. The existing runtime is not bundled with this repo.

Every call uses a fresh ephemeral context and empty temporary working directory,
read-only sandbox, ignored user configuration, and explicit isolation overrides.
Preflight records what these switches actually achieve; flags alone are not
proof. Actual tool calls fail the protocol. Common platform instructions and any
remaining skill catalog must be disclosed, and the study must stop if treatment
loading or carry-over prevents comparable conditions. No global configuration is
modified, and no authentication files are copied into the repository.

Preflight on this host found a remaining common catalog of six unrelated skills
and the user's global working rules even after explicit disable switches. Neither
target skill is in that catalog. These instructions are a common platform
background, so A means no *experimental* R/C module, not an instruction-free
model. Tool definitions also remain visible; actual tool invocations are rejected
from execution events. The disable switches are recorded as requested settings,
not claimed as effective removal. The study estimates an incremental intervention
in this environment; hidden platform influence and residual automatic skill
behavior cannot be ruled out. The empty working directory, ephemeral CLI launch
without resume, and a separate context probe are evidence against prior-output
carry-over, rather than proof of a sterile system prompt.

Each cell records task, factor condition, repetition, requested model and effort,
prompt hash, UTC start/end, duration, raw text, total characters, Han characters,
usage when reported, and status. Private attempt records retain CLI events and
diagnostics. Public artifacts omit transport IDs and local temporary paths.
Only explicit transient transport failure permits one retry (two attempts total).
All attempts survive. Poor text, refusal, length misses and technical errors are
outcomes, not execution failures. Nontransient errors and protocol violations
stop execution. Resume uses the same frozen inputs.

## Independent blinded judgment

After all generation is locked, 21 independent packets contain one task and one
repetition: four anonymous texts for mathematics, two for other domains. The judge
receives facts, goal, reader, texts and randomized pairs. It sees no conditions,
skill names, generation prompts, development conversation, or expected outcome.
Anonymous IDs do not encode group. Text content can still reveal style; blinding
cannot prevent a judge from inferring differences from the text itself.

Each text gets correctness and seven comprehension scores: prior-knowledge
alignment, conceptual sequencing, motivation, explanatory coherence, cognitive
load, transfer support, and overall comprehensibility. Scores range from 1
(substantial failure) to 5 (fully adequate for this task and reader), with 3
meaning usable but containing specific gaps. Major factual/technical errors are
recorded separately. Transfer support concerns text structure only. Redundancy
uses 1 (none) to 5 (severe). Length alone is not a quality score.

The judge also compares A/B, A/C, B/D and C/D for each mathematics block and A/C
for every cross-domain block: 48 pairs total. Display order and left/right order
are randomized; ties are allowed. Ratings and comparisons require exact quotes
and concrete reasons, including accuracy costs. A deterministic validator checks
IDs, numeric ranges, comparison membership and verbatim quote existence. It does
not prove the interpretation of that evidence. Malformed judgments are retained
and block analysis; they are not selectively regenerated until favorable.

The primary judge uses a fresh context independent of development and generation,
but the same model family. This can favor its own style and is explicitly a
limitation. Different packets are separate sessions; within-packet observations
are correlated. An independent technical review of the anonymized evidence is
required before promoting model flags to accepted findings. A second model is
optional and must not introduce an unauthorized paid service.

## Analysis and examples

Only after validated judgments are locked are anonymous IDs joined to conditions.
For overall comprehensibility and, separately, correctness, report group means,
per-task and per-repetition variation, and the descriptive contrasts:

`ΔR = ((B−A)+(D−C))/2`; `ΔC = ((C−A)+(D−B))/2`;
`I = D−B−C+A`.

Report cross-domain A/C differences separately by domain and task, pairwise
wins/ties/losses, major errors, redundancy, text length, duration and available
usage. Do not compute an API bill from subscription token counts, or interpret
these ordinal small-sample contrasts as population causal estimates.

Primary examples are fixed before scoring: repetition 1 of `math-concept`,
`control-crossover`, and `ml-kv-cache` (A/C). In addition, show the weakest A/C
improvement by overall score (including a tie or negative result), breaking ties
by task ID then repetition. Failure analysis must discuss no-effect, redundancy,
bad analogy, surface-only changes and potential R/C conflicts where observed;
an unobserved failure type must be marked unobserved, not invented.

Any skill revision after this evaluation is a new version. Do not present old
outputs as tests of a revised version. This is an exploratory single-model study,
not a human learner trial, proof of learning gain, or universal generalization.
