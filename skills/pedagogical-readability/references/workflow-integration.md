# Shared workflow integration

Read this before first use, or after changing the external workflow installation.
This skill requires the owner's existing shared workflow. That runtime is not
included in this skill package, and no public download address is available.
Installing this skill alone cannot execute its review gates. If you do not have
the runtime, report that dependency as unavailable; do not claim an equivalent
teaching review from prompt-only use. This does not affect the standalone
`reader-aware-writing` skill.

Set `SHARED_WORKFLOW_ROOT` to the existing shared workflow directory on your
machine. This variable is a documentation and shell convention; skill hosts are
not expected to expand it automatically. Resolve its paths when reading files.
The existing layout must include a sibling `bin/workflow` launcher and parent
workspace `AGENTS.md` as well as the workflow itself. Follow that installation's
own setup and its model registry; no new model defaults are introduced here.

```bash
export SHARED_WORKFLOW_ROOT="/absolute/path/to/existing/workspace/workflow"
test -f "$SHARED_WORKFLOW_ROOT/../AGENTS.md"
test -x "$SHARED_WORKFLOW_ROOT/../bin/workflow"
test -f "$SHARED_WORKFLOW_ROOT/README.md"
test -f "$SHARED_WORKFLOW_ROOT/src/lanes/pedagogical.py"
test -f "$SHARED_WORKFLOW_ROOT/docs/PEDAGOGICAL_READABILITY.md"
test -f "$SHARED_WORKFLOW_ROOT/config/models.example.yaml"
test -f "$SHARED_WORKFLOW_ROOT/tests/test_readability_architecture.py"
test -f "$SHARED_WORKFLOW_ROOT/tests/test_hidden_inference.py"
"$SHARED_WORKFLOW_ROOT/../bin/workflow" --help
```

These checks verify file availability and the CLI entry point only. They do not
prove the runtime has dependencies, credentials or model capacity for real jobs.
Read the external workspace instructions, workflow README and invocation guide,
and the owning project's instructions before executing jobs. Select the PDF lane
and enable `traits.document_purpose: teaching` or
`traits.skills: [pedagogical_readability]` in the existing job. Use the existing
workflow schema and command documentation for complete job configuration.

The runtime owns the actual prompts, JSON schemas, Reader, continuous-reading
review, repair, teach-back, technical guard, checkpoints and bounded retries.
`config/models.example.yaml` or an explicit local configuration owns model routes.
The two external tests protect continuous-reading and hidden-inference gates;
they remain dependencies, not tests supplied by this skill repository. The
workflow's own environment must run them. No runtime code or historical
experiment/chat archives were copied into this package.
