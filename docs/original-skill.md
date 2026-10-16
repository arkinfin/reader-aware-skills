# Original teaching skill: dependency and preservation record

The formal source name is **pedagogical-readability**, with the structured trigger
`pedagogical_readability`. The requested spelling `pedagogic-readability` was not
the actual source entry. The original name and `agents/openai.yaml` are retained.

This is a dependency-preserving distribution of the existing teaching skill.
It is usable only with the owner's existing shared workflow installation. That
runtime is **not distributed in this repository**, and no public download URL is
currently available. Installing this skill does not install its runtime, execute
its gates, or establish compatibility with other agents. The standalone
`reader-aware-writing` skill does not have this dependency.

## Dependency setup and verification

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

## Source and behavior preservation

The owner confirmed full copyright ownership and authorized MIT distribution of
the skill text on 2026-10-16. This permission is not a license grant for the
external workflow code or any third-party source. Hashes below identify the local
baseline audited before packaging; source paths are relative to its workspace.
The source skill was not Git tracked, so its hash is the primary version identity.

| Baseline source | SHA256 |
| --- | --- |
| `workflow/skills/pedagogical-readability/SKILL.md` | `2d066e9c57d5b5270901ff8807dc89aea8159ead95e7f42d1ca2ac4d0fcdfe7f` |
| `workflow/skills/pedagogical-readability/agents/openai.yaml` | `8a2a46743c931836fe9f4f673f56efdd87b60dff40f90fc2f1629eed2049cef8` |
| `workflow/src/lanes/pedagogical.py` | `cdf6e275fe4063af877529e10ac86cc5228ed478563e74bb5048dbf30ea7ed99` |
| `workflow/docs/PEDAGOGICAL_READABILITY.md` | `8fe5f81bffaa288e19605baeb9219145f5ad10bc29e3adf34169ddced7fda9ce` |
| `workflow/config/models.example.yaml` | `b572f16dea8776002dac41136ff85455dc80067a3dce6c897e9161e7c9894ab8` |
| `workflow/tests/test_readability_architecture.py` | `deecded165412062090084eb4f78bd09d9d274b65e3ff38fc0672598936080fd` |
| `workflow/tests/test_hidden_inference.py` | `fa5e113b052e1353479a12c4bfe9539241ac705b60db8a9a4a7509d1a8305379` |

The packaged metadata is byte-for-byte identical to its baseline. The skill body
has only the dependency notice and the seven path substitutions shown below.
All other text is byte-for-byte preserved after reversing those substitutions
and removing the notice. Trigger conditions, required H2/H3 repairs, all three
acceptance axes, Writer Advisory status, default C review, review allowlists,
evidence rules, ownership limits, repair budgets, technical guard and model
routing policy are unchanged. This package does not depend on the new skill.

The dependency notice links to the bundled
`skills/pedagogical-readability/references/workflow-integration.md`, which stays
available when only the skill directory is installed. Read it before first use
or after the external workflow installation changes. The reference adds setup
documentation only; it does not add gates or alter the original rules.

The paths are adapted so copying into `skills/` does not silently turn external
references into broken local ones. The notice documents the pre-existing runtime
requirement; it does not implement or replace any review behavior.

## Exact entry-point diff

```diff
--- original/SKILL.md
+++ packaged/SKILL.md
@@ -5,15 +5,21 @@
 
 # Pedagogical readability
 
+本发布副本保留原共享工作流依赖。使用前将 `SHARED_WORKFLOW_ROOT` 指向已安装的外部
+shared workflow 根目录；本文中的 `${SHARED_WORKFLOW_ROOT}` 是路径约定，不是 Agent
+自动展开的配置项。本包不附带该运行时，也没有公共下载地址；仅安装 Skill 不会安装或
+执行审查门禁。首次使用或外部安装变更时，先读随包的
+[工作流接入说明](references/workflow-integration.md)并完成依赖检查，再执行教学任务。
+
 仅在明确的教学目的或用户显式调用时使用。将教学意图写入现有 job 的
 `traits.document_purpose: teaching`，或 `traits.skills: [pedagogical_readability]`。
 自然语言“教学型手册”“mini textbook”“用于重新学习”“面向学习者讲解”可以由
 Orchestrator 转成上述结构化字段；“总结”“两页以内核心结论”“公式速查表”不自动转换。
-运行时不做关键词猜测。沿用 `/home/samsa/projects/bin/workflow` 的 PDF lane。
+运行时不做关键词猜测。沿用 `${SHARED_WORKFLOW_ROOT}/../bin/workflow` 的 PDF lane。
 
 目的：显式补足作者省略的理解连接，保留专业性与正式数学表达，同时让整章可以连续读完。
 默认读者学过基础课，但忘了为什么、何时用、第一步、分情况与检查。
-先读共享 workspace 的 AGENTS.md、workflow/README.md 与项目 AGENTS.md。
+先读外部 `${SHARED_WORKFLOW_ROOT}/../AGENTS.md`、`${SHARED_WORKFLOW_ROOT}/README.md` 与项目 AGENTS.md。
 
 ## 三条互相独立的验收轴
 
@@ -158,15 +164,15 @@
 
 ## 路由与证据
 
-角色与 provider/model/effort 只在 `workflow/config/models.example.yaml` 或显式本地配置中定义。
+角色与 provider/model/effort 只在 `${SHARED_WORKFLOW_ROOT}/config/models.example.yaml` 或显式本地配置中定义。
 槽位是 `pedagogical_reader`、`naturalness_reviewer`、`pedagogical_repair`、`technical_guard`。
 Reader 的模型选择是可替换的实验假设，不能因为便宜就自动视为合适。
 DeepSeek 只承担 comprehension/readability，不裁决教学修补的最终数学正确性。
 所有调用与模型、usage、原文、报告、候选、验证结果保留在项目 `.workflow`。
 
 准确的执行 prompt 与 JSON schema 位于
-`../../src/lanes/pedagogical.py`，不得在 job 中复制模型默认值。
-详细调用与 A/B 方法参见 `../../docs/PEDAGOGICAL_READABILITY.md`。
+`${SHARED_WORKFLOW_ROOT}/src/lanes/pedagogical.py`，不得在 job 中复制模型默认值。
+详细调用与 A/B 方法参见 `${SHARED_WORKFLOW_ROOT}/docs/PEDAGOGICAL_READABILITY.md`。
 复述测试按章节选择问题：解决什么、何时用、第一反应、第一步及原因、分叉、禁用条件、
 易混关系、能否仅据正文重建操作链。无法从正文支持的回答标记 gap；评分不作为验收标准。
 直观小例子不承担通用算法的全部分叉；证明段检查论证连接，练习段检查能否用已教方法起手。
@@ -187,8 +193,8 @@
 
 ## 回归保护
 
-确定性覆盖在 `../../tests/test_readability_architecture.py`，并保留
-`../../tests/test_hidden_inference.py` 的隐藏推理门禁测试。已有 B-only mock 可以显式
+确定性覆盖在 `${SHARED_WORKFLOW_ROOT}/tests/test_readability_architecture.py`，并保留
+`${SHARED_WORKFLOW_ROOT}/tests/test_hidden_inference.py` 的隐藏推理门禁测试。已有 B-only mock 可以显式
 `naturalness_review: false`，但不能因此全局关闭默认 C 路径覆盖。
 离线测试只验证确定性行为与 prompt 隔离，不证明学生可用性或文字质量。
 现有 A/B 实验是小样本探索，不能据此宣称已证明人类可读性；不要声称学生可用性已实验证明。
```

## Validation scope

Packaging validation reverses all documented adaptations and checks exact equality
with the baseline, checks metadata byte equality, checks every named dependency
against the existing local runtime, and validates the packaged skill structure.
These are static preservation checks. No full teaching-job regression or paid
review is implied by them; runtime tests and actual job outcomes must be reported
separately. Local paths used to inspect the baseline are not installation defaults.
