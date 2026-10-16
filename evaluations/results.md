# Exploratory results

**This study did not establish an independent comprehensibility benefit from
reader-aware-writing.** The mathematics contrasts were zero, the control result
was a small localized difference, and ML showed no overall difference. This is
not proof of no effect: 59 of 60 overall ratings were already at the maximum.

All 60 planned texts and 21 independent anonymous evaluation packets completed,
with 48 paired comparisons. There were no experimental transport failures,
quality-based retries or model substitutions. Generation and primary judging
requested `gpt-6.1-sol`, Medium, through CLI 0.162.1. The backend's immutable model
revision was not exposed. No human learning outcome was measured.

The [protocol](methodology.md), [complete numeric tables](results-data.md),
[machine-readable summary](summary.json), [raw outputs](outputs/),
[anonymous judgments](judgments/) and [replay evidence](records/) are retained.

## Mathematics: 2×2 intervention

Each group has nine texts: three tasks × three repetitions. These are ordinal
model ratings on a 1–5 scale, summarized descriptively.

| Group | Correctness | Overall comprehensibility | Mean Han characters |
| --- | ---: | ---: | ---: |
| A: common task | 5.000 | 5.000 | 449.7 |
| B: rigor module | 4.889 | 5.000 | 430.9 |
| C: reader-aware writing | 4.889 | 5.000 | 456.0 |
| D: both modules | 4.889 | 5.000 | 422.6 |

For overall comprehensibility, **ΔR=0, ΔC=0, I=0**. These are also zero for each
mathematics task and each repetition. For raw correctness ratings, ΔR=−0.056,
ΔC=−0.056 and I=+0.111. Those tiny differences are driven by disputed local
method-language flags, including one subsequently rejected flag; they do not
demonstrate that rigor harms correctness.

All A/B, A/C and C/D comparisons tied. B/D tied in eight of nine cases; D was
preferred once because a concrete `x³=o(x)` example made an order distinction
easier to inspect. Both texts still received overall 5/5. This single relative
preference is not evidence of aggregate complementarity. D contained only the
experimental R/C modules, not the complete original teaching skill.

## Cross-domain comparisons

Each domain has six texts per condition: two tasks × three repetitions.

| Domain | A overall | C overall | C−A | C wins / ties / A wins |
| --- | ---: | ---: | ---: | --- |
| Control theory | 4.833 | 5.000 | +0.167 | 1 / 5 / 0 |
| Machine learning | 5.000 | 5.000 | 0.000 | 0 / 6 / 0 |

The only overall A/C difference was `control-state-transfer`, repetition 3. A
said “只有在 \(x_0=0\) 时，才直接得到” the zero-state input/output relation.
That exclusive wording is too strong: a nonzero unobservable initial state can
also contribute zero output. C stated the hidden-mode initial-condition example
more carefully. The independent technical checks agreed with this local issue.
The crossover task showed no overall difference in any repetition.

ML correctness means were A=4.833, C=5.000, but its sole primary minor flag was
later classified as terminology caution, not a gradient-calculation error.
The raw overall scores and all six paired comparisons remained tied. There is
no consistent cross-domain evidence of improved comprehension in this sample.

Across all 48 comparisons there were **46 ties and two preferences**: the one
control A/C case and one mathematics B/D case. No other non-tie was recorded.

## Accuracy and independent checks

The primary judge marked zero major errors and five minor flags. A separate,
fresh anonymous adjudication of all five flags produced:

| Text | Primary flag | Secondary verdict |
| --- | --- | --- |
| control-state-transfer A r3 | Zero initial state presented as necessary | Accepted minor error |
| math-method C r1 | Must keep seeking a nonzero term even when `o(x³)` already settles the limit | Accepted minor error |
| math-method D r1 | General advice to seek the first nonzero term | Wording caution |
| ml-residual-gradient A r1 | Calls an ordinary layer's map a residual branch | Wording caution |
| math-method B r1 | “可以” continue expanding to a nonzero term | Rejected: an optional sufficient route was misread as a necessity |

The original five flags and primary scores are unchanged. Secondary decisions
are recorded separately in [technical-adjudication.json](technical-adjudication.json).
The numerical results above always use the original primary ratings.

A second independent context checked **14 texts in five preselected anonymous
packets**, with sampling fixed before evaluation. It identified the same control
minor error and no other material error in its sample. Its
[coverage and evidence](technical-review-independent.json) do not constitute an
independent verification of all 60 texts. Both secondary reviewers used the same
model family, so correlated blind spots remain. All reported finding quotations
were checked against the original texts.

## Length, redundancy and execution cost

| Domain | A mean Han characters | C mean Han characters | Change |
| --- | ---: | ---: | ---: |
| Mathematics | 449.7 | 456.0 | +6.3 (+1.4%) |
| Control theory | 534.5 | 532.2 | −2.3 (−0.4%) |
| Machine learning | 592.3 | 616.0 | +23.7 (+4.0%) |

There was no overall comprehension gain accompanying the extra ML length.
That is a cost observation, not proof that the extra wording was meaningless.
All primary redundancy ratings were 1/5, where 1 means none identified; this
uniform result may itself reflect limited evaluator discrimination.

Adding C increased reported input usage by roughly **716–718 tokens per call**
in this environment. The generation means ranged from about 30 to 32 seconds;
parallel scheduling, caching and platform load prevent interpreting those means
as intrinsic speed effects. [Cost breakdowns](cost-breakdown.json) retain input,
cache, output and reasoning fields separately. Subscription usage is not an API
bill, and overlapping fields must not be added as separate charges.

The common target was a soft 600–900 Chinese-character explanation, excluding
formulas. Actual Han-character counts ranged from 345 to 651; 54/60 were below
600. Han count is a proxy, not a formula-aware word count. No short output was
replaced. The shorter-than-planned texts limit conclusions about sustained or
chapter-length reading.

## Success, no-effect and failure examples

The three fixed examples all tied: [mathematical concepts](../examples/mathematics/math-concept-r1.md),
[gain crossover](../examples/control-theory/control-crossover-r1.md), and
[KV cache](../examples/machine-learning/ml-kv-cache-r1.md). They show different
explanation routes without a rated advantage. The preregistered weakest A/C rule
also selected the crossover example: its difference of zero was shared by many
cases, not a unique failure.

The [state-space example](../examples/control-theory/control-state-transfer-r3.md)
was selected after scoring to illustrate the only local A/C preference. It is
explicitly a post-hoc illustration, alongside the fixed no-effect cases.
The [four-condition limit example](../examples/mathematics/math-method-r1.md)
exposes a treatment accuracy cost and disagreement in model judgment. The
requested numerical limits were correct; the defect concerns overgeneralized
method advice. No raw text was corrected for the examples.

No erroneous analogy or systematic R/C interference was identified. That is an
observation about the checked material, not a guarantee. The evaluation also
does not establish that more natural prose alone improved explanation structure:
the fixed cases often use different, already coherent routes. No additional
success cases or failure types have been invented.

## What the hypotheses permit us to say

1. **Rigor mainly improves correctness?** Not demonstrated here. A was already
   highly correct, and the R module was in-generation self-check guidance rather
   than the complete production review workflow.
2. **Readability independently improves comprehension?** Not established. One
   local control preference is insufficient, and the primary scale saturated.
3. **Complementarity?** No aggregate interaction in the mathematics overall
   scores; one B/D relative preference is weak, localized evidence only.
4. **Interference?** No systematic comprehension interference was detected.
   Neither module guaranteed technically safe generalization in every text.
5. **Cross-domain benefit?** No robust generalization signal: control +0.167,
   ML 0, with only one non-tied A/C comparison.
6. **Costs?** A longer intervention prompt, mixed text-length changes, and a
   small ML length increase without an overall-score improvement.

## Limitations and release recommendation

This is a small, single-model-family, model-judged study. Ratings are ordinal,
within-packet observations are correlated, and means/contrasts are descriptive,
not well-powered population causal estimates. Fifty-nine maximum overall scores,
rich factual scaffolding, capable baseline writing and task brevity all limit
sensitivity. Fixed common platform instructions and skill descriptions remained
visible; actual tool calls were prohibited. Temperature, sampling seed and
immutable backend revision were unavailable. No independent human comprehension,
retention, transfer or learning gain was measured.

The deterministic runner received a documented provenance-gate amendment between
generation and evaluation, after an independent code review and before any
judging. Original code/manifest and the exact patch survive in
`records/infrastructure/`. Stimulus hashes, task facts, scheduling, generation
configuration and all outputs were unchanged. Offline analysis checks both
versions and actual successful attempts before deblinding.

The repository is suitable for review as an **experimental, honestly documented
release candidate**, not as an empirically validated improvement. The new skill
is independently usable by design, while its incremental benefit remains
unconfirmed in this study. The original skill's runtime dependency is retained
with the owner's approval. No post-result skill tuning was performed to make
the numbers favorable. Future work can calibrate evaluation discrimination and
use more demanding reader-dependency tasks or natural human feedback; it must be
a newly registered study, not a rewrite of these results. Public release still
requires separate owner authorization.
