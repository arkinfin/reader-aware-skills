# Validation scope and execution notes

The owner authorized retaining the original shared-workflow dependency and
confirmed full copyright ownership of the skill text before MIT packaging.
No remote or public release action is part of these checks.

## Checks already executed

- Both skill folders passed the skill-creator frontmatter/scaffold validator.
- Reversing the recorded packaging edits reproduces the exact original skill
  SHA256; its agent metadata is byte-identical. The seven baseline source files
  were also checked against their recorded hashes.
- The external workflow's `test_readability_architecture.py` and
  `test_hidden_inference.py` passed **57 offline tests**, exit 0. These tests use
  deterministic/mock behavior and do not demonstrate student learning or a
  successful paid runtime job.
- README installation commands were executed for both skills in temporary
  projects. All copied files matched the source bytes. This tests installation
  mechanics, not automatic selection in every agent host.
- Two independent native-session scope checks produced only `42` and
  `{"count":3}` for final-only and strict-JSON requests. See
  [the records](../evaluations/functional-checks.json). These are compatibility
  smoke checks, excluded from experimental effect estimates.
- An independent Sol Medium code review identified deterministic provenance,
  cache-resume and evidence-validation defects. They were corrected before
  judging. A targeted re-review confirmed the accepted findings resolved.
- Synthetic fixtures tested factor contrasts, pair direction, usage aggregation,
  missing data, duplicate IDs, changed hashes, fabricated quotations, unsupported
  redundancy ratings, actual-attempt matching and infrastructure amendments.
  They were never reported as real model observations.

The final static release scan is reproducible with:

```bash
python3 scripts/validate_release.py
```

The complete published evidence was also replayed in a temporary copy excluding
both `.workflow/` and `.git/`. It required no shared runtime or model call and
produced an identical summary object and byte-identical numeric Markdown table.

An owner with the original installation can additionally run:

```bash
python3 scripts/validate_release.py --source-workspace /absolute/path/to/workspace
```

The output distinguishes passed checks, skipped runtime checks and limitations.
Credential patterns and file inventories cannot prove absence of all private or
copyrighted information; source scope and the candidate file list were reviewed
as well. No complete handbook, chat archive, authentication file or external
workflow implementation is included.

## Failed preflight operations and recovery

These occurred before the 60-output experiment and are not hidden replacement
generations:

| Operation | Status | Resolution |
| --- | --- | --- |
| Initial strict CLI preflight using `tools.view_image` | CLI and wrapper exit 1: unsupported configuration key | Used the feature key recognized by installed CLI |
| Sandboxed CLI initialization | CLI and wrapper exit 1: read-only filesystem | Requested and received escalation for the existing authenticated CLI transport |
| First external preflight with feature warnings | CLI exit 0; wrapper exit 1: warnings classified as forbidden event items | Allowed only the two identified warning prefixes, retaining failure for other error/tool items |
| Explicit skill-disable probe | Exit 0, but the common platform catalog remained visible | Disclosed the observed common background rather than claiming switches removed it |
| Initial README patch | Patch tool rejected duplicate target operations; no file mutation | Reissued one update operation |
| Initial package-link scan before `docs/` existed | `rg` exit 2 | Created the owned documentation, then verified links |
| Initial static-validator prototype | Exit 1: a historical fenced diff was treated as a live link | Limited live Markdown-link checks to prose; rechecked genuine broken links with negative fixtures |
| Final staged whitespace check | Exit 2: valid unified-diff blank-context markers plus an ordinary extra EOF blank line | Preserved exact diff evidence with two file-scoped `.gitattributes` exceptions and removed the integration guide's extra EOF blank line |

The independent asset audit also reported missing-path searches with exit 2,
no-license searches with exit 1, and `git log` on an uncommitted historical
project with exit 128. Existing files, content hashes, actual diffs and application
manifests supplied the version evidence instead. Absence of a prior license was
resolved by the owner's explicit copyright confirmation, not by assuming public
material was freely reusable.

## Limits

The teaching runtime is external and lacks a public download location. Its model
calls and full end-to-end teaching job were not rerun; no paid external service
was authorized. Preservation, offline gates and declared integration prerequisites
are the regression evidence supplied here. The standalone skill has no such
runtime dependency.

Experiment findings concern short explanation quality in one configured model
family with model-based judges. They cannot establish learning gain, cross-model
robustness, universal compatibility or reliable automatic skill triggering.
