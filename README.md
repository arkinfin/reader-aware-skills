# reader-aware-skills

**Correct reasoning is not the same as comprehensible explanation.**

Two skills address different goals and can be selected independently or used
together. They are not basic and advanced editions of one tool.

| Skill | Primary purpose | Runtime |
| --- | --- | --- |
| [pedagogical-readability](skills/pedagogical-readability/SKILL.md) | Pedagogical material production and rigorous quality control | Requires the existing shared PDF workflow; not bundled here |
| [reader-aware-writing](skills/reader-aware-writing/SKILL.md) | Reader-centered explanation and comprehensibility | Self-contained instructions |

`reader-aware-writing` helps choose knowledge starting points, conceptual order,
motivation, representation changes and useful explanation forms. It favors
targeted connections over unnecessary expansion, respects expert knowledge and
length constraints, and can leave tasks requiring no explanation alone.

It is explanation guidance, not a persona, roleplay, AI humanizer or a general
prose-polishing pass. It does not guarantee factual accuracy or learning gains.
Effects depend on the model, task and reader. Fact checking and proof review
remain separate responsibilities.

The original teaching skill keeps its mandatory inference, technical and reading
review rules, advisory guidance, bounded repairs and teaching-specific triggers.
Its actual formal name is `pedagogical-readability`; `pedagogic-readability` was
the spelling used in the initial project request. [Preservation details and exact
path adaptation](docs/original-skill.md) explain this distinction.

## Install for local Codex use

The folders use the Codex `SKILL.md` convention. These steps install selected
skills into an existing project's `.agents/skills` directory. They do not modify
your global configuration. Other agents have not been verified.

From this repository's checkout, set an existing target project and run:

```bash
set -eu
skill_repo="$PWD"
target_project="/absolute/path/to/your/project"
test -d "$target_project"
test -f "$skill_repo/skills/reader-aware-writing/SKILL.md"
mkdir -p "$target_project/.agents/skills"
test ! -e "$target_project/.agents/skills/reader-aware-writing"
cp -R "$skill_repo/skills/reader-aware-writing" "$target_project/.agents/skills/"
```

Launch Codex in that target project. Invoke explicitly, for example:

> Use $reader-aware-writing to explain why a KV cache can reuse previous keys
> and values. I know matrix multiplication and softmax; keep it concise.

To install the teaching skill instead, replace `reader-aware-writing` in the
commands with `pedagogical-readability`. **That skill requires the owner's
existing shared workflow installation**, which has no public download location
at present. Read its bundled [integration instructions](skills/pedagogical-readability/references/workflow-integration.md)
and resolve `SHARED_WORKFLOW_ROOT` before using it. Installing the folder alone
does not install or execute the reviewers, gates or PDF workflow.

Use either skill alone. For a teaching job that needs both, explicitly select
both while retaining the original workflow's technical review. The new skill
adds no review stages and is not a dependency of the original one. Codex can
consider skills automatically; a skill should not add an explanation to a
final-answer-only or strictly structured-output request.

These local installation conventions follow the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).
No global agent compatibility or automatic-trigger performance is claimed.

## Experience and evaluation

The maintainer reports positive feedback from a small informal review group.
No standardized questionnaire results or controlled learning outcomes are
available for this feedback. It is encouraging feedback for sharing these skills;
measured learning gains and a general comprehensibility benefit remain unverified.

The [protocol](evaluations/methodology.md) distinguishes correctness,
comprehensibility and learning gain. The completed exploration comprises 36
mathematics outputs (Rigor × Comprehensibility) and 24 control/ML outputs
(Baseline vs Readability), followed by independent anonymous model evaluation.
The combined mathematics condition uses only the two intervention modules,
not the full teaching skill.

**The experiment did not establish a consistent comprehensibility benefit.**
Mathematics overall-score contrasts were ΔR=0, ΔC=0 and I=0. The C−A difference
was +0.167 in control theory and 0 in ML; 46 of 48 pair comparisons tied.
Fifty-nine of 60 overall ratings were already 5/5, so the evaluation has a severe
ceiling and cannot establish that the skill has no effect either.

Read the [results and limitations](evaluations/results.md),
[all numeric tables](evaluations/results-data.md), and
[validation scope](docs/validation.md). Examples include fixed tied pairs in
[mathematics](examples/mathematics/math-concept-r1.md),
[control](examples/control-theory/control-crossover-r1.md) and
[ML](examples/machine-learning/ml-kv-cache-r1.md), plus a
[local preference](examples/control-theory/control-state-transfer-r3.md) and
[disputed accuracy flags](examples/mathematics/math-method-r1.md).

Generation uses a fixed configured model and reasoning effort without fallback.
The shared platform's remaining common skill catalog and global working rules
are disclosed in the protocol. Temperature, provider sampling seed and immutable
model revision are not exposed. No human learning experiment is planned.

The primary judge marked no major errors and five minor flags; independent
adjudication accepted two minor errors, classified two as wording cautions, and
rejected one. Raw ratings remain unchanged. A separate preselected anonymous
technical check covered 14 texts. These checks also used the same model family.

Offline replay needs only Python's standard library and the included records:

```bash
python3 evaluations/analyze.py --evidence-dir evaluations/records
python3 scripts/validate_release.py
```

See [reproduction instructions](evaluations/reproduction.md) for evidence scope
and the distinction between offline replay and new model calls. This is an
experimental release; incremental benefit remains
unconfirmed. No skill changes were made after seeing these results.

## Rights and distribution

MIT covers the skill text and original project material included here. The owner
confirmed full rights to the existing skill on 2026-10-16. The external shared
workflow, third-party papers and documentation retain their own rights and are
not redistributed. Task packs restate facts in original wording; no full handbook
or private conversation is included.

The owner has authorized public distribution of this experimental version.
Informal review feedback and automated evaluation results are reported separately.

[中文项目交付报告](docs/project-report.zh-CN.md) covers the assets, mechanism
questions, limitations and release recommendation.
