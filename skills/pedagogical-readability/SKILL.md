---
name: pedagogical-readability
description: 降低教学型复习手册、mini textbook、重新学习资料的认知跳跃，并改善整章连续阅读体验。普通总结、报告、API 文档、cheatsheet、研究资料和一般 PDF/Word 整理不默认启用。
---

# Pedagogical readability

本发布副本保留原共享工作流依赖。使用前将 `SHARED_WORKFLOW_ROOT` 指向已安装的外部
shared workflow 根目录；本文中的 `${SHARED_WORKFLOW_ROOT}` 是路径约定，不是 Agent
自动展开的配置项。本包不附带该运行时，也没有公共下载地址；仅安装 Skill 不会安装或
执行审查门禁。首次使用或外部安装变更时，先读随包的
[工作流接入说明](references/workflow-integration.md)并完成依赖检查，再执行教学任务。

仅在明确的教学目的或用户显式调用时使用。将教学意图写入现有 job 的
`traits.document_purpose: teaching`，或 `traits.skills: [pedagogical_readability]`。
自然语言“教学型手册”“mini textbook”“用于重新学习”“面向学习者讲解”可以由
Orchestrator 转成上述结构化字段；“总结”“两页以内核心结论”“公式速查表”不自动转换。
运行时不做关键词猜测。沿用 `${SHARED_WORKFLOW_ROOT}/../bin/workflow` 的 PDF lane。

目的：显式补足作者省略的理解连接，保留专业性与正式数学表达，同时让整章可以连续读完。
默认读者学过基础课，但忘了为什么、何时用、第一步、分情况与检查。
先读外部 `${SHARED_WORKFLOW_ROOT}/../AGENTS.md`、`${SHARED_WORKFLOW_ROOT}/README.md` 与项目 AGENTS.md。

## 三条互相独立的验收轴

Correctness（A）、Inferential Completeness（B）、Reading Fluency（C）互相独立。
数学正确、文字流畅都不代表 B 通过；B 通过也不代表整章读起来不费劲。
A 沿用现有技术审查；B 在现有 Reader 和修补后的 Teach-back 中执行独立 Hidden Inference Audit；
C 复用现有 naturalness 节点与 `naturalness_reviewer` 角色，作为一次
Readability / Continuous-Reading Review。不新增节点、角色、agent、投票方案或评分公式，
也不增加第二次付费 C 调用。

一次成功的推理缺口修补不会自动要求再补一轮解释。只有新的、有证据的缺口才进入修补。

## 作者脚手架与读者正文分离

识别条件、第一步、理由、分叉、易错点、其他做法、回看清单，是全章的内部完整性检查：
它们确保作者一侧没有漏项。它们不需要在读者正文里以可见的六问块出现，
也不要在正文里反复贴“方法”“为什么”“验收”“第一反应”之类的标签。

读者正文使用行动优先、具体优先的普通语言，保留必要的专业术语和推理桥梁。
一段只承担一个主要认知任务，用渐进披露给出清楚的主路径和自然停顿点。
不要把工作流、作者、审查或验收语言写进正文。
不要为满足外观而改写自然通顺的散文，也不要施加字符数或公式数硬上限。

每个例题有一个主要教学目标；只有该目标或练习题明确要求时才做完整构造，
其余只展示该目标所需的环节。

### Writer Advisory

既有前置连接、具体优先、单段任务与表征桥梁规则继续适用，不重复追加。
Writer 可按当前内容的收益，从原有问题的操作需求进入方法、推导与应用；
知识分类顺序不必作为讲解顺序。优先重排已有解释，避免靠加字改善外观。
恢复操作链时，可在原例题内逐渐从完整示范转为关键提示，不增练习模块。
直接推导更清楚或策略造成重复、拖沓时不采用，不必套用统一结构。
本段仅为 Advisory，不改变硬性约束，不增加 reviewer 清单、阶段或评分。

## 核心规则：推理桥梁完整性

- 新符号首次出现，检查对象身份、对象还是表示、相关空间/参考系、与前项关系、引入目的。
  只解释理解所需的维度；禁止只命名符号就让它进入来源不明的关键公式。
- 同一对象多种表示易混时显式区分对象与坐标/参数化/表示矩阵；不强制到处用完整 notation。
- 一跳一动作：相邻关键步骤只作一个主要认知操作；多个非显然独立操作拆开。
- Reviewer 对每个关键公式、结论、新变量、转折、方法切换实际尝试一句逆向解释：
  “只凭前式、相邻文字、此前明示关系及允许前置知识，下一步为什么成立？”
  若必须脑补未写事实，标记 TG-16，找最小必要桥梁，不用专家直觉替作者补全。
- H1：短暂停顿可恢复，默认 advisory；H2：须恢复关系/公式/规则而中断理解；
  H3：符号/对象/公式来源不明，无法继续。H2/H3 必修，不能用 optional 降级。
  缺少定位、严重度或修复字段的隐藏推理报告阻塞审查，不静默丢弃。
- 每个隐藏推理给出 severity、problem_location、hidden_inference、why_reader_may_fail、
  minimal_bridge、suggested_revision，保留现有精确段号与引文；跨段证据分别引用。
  Repair 验证候选桥梁，只补一句关系/定义/条件/转换规则或一个中间等式。
- 新概念、符号、表示切换、对象身份、新定理、叠加操作、非显然条件倾向展开。
  单步机械代数、已允许前置计算、刚解释或连续重复的规则不重复展开；
  说明负担大于收益时保持简洁。关键词只触发检查，不直接判错。
  “已解释同一规则”的压缩仅适用于已明示的对象/表示关系；首次将规则用于输出或新对象，
  仍须写出对应关系。能从通用定义自行推出不等于教材已承担桥梁，不能据此降为 optional。

高风险位置包括“显然、容易得到、于是、因此、故、由定义、类似地、同理、可得、不难发现”，
以及输入/输出、基底/坐标系、局部/全局、向量/坐标向量、映射/矩阵、曲线/参数方程、
曲面/参数域或投影面、随机变量/取值或样本、原函数/变换后函数、连续/离散、物理量/拉氏域切换。
这些位置只是检查触发器，不是自动判错规则。

示例（仅说明“最小桥梁”的粒度，不构成对本 skill 的学科要求）：已有 x=Py、Ax=APy，
不能直接“输出新坐标为 z，故 Pz=APy”。最小修补：“z 是同一输出向量的新基坐标，
Ax 是其旧基坐标；同一换基规则给出 Ax=Pz。结合前式得 Pz=APy。”无需重写整个证明。

## Readability / Continuous-Reading Review（C）

C 复用现有 naturalness 节点与 `naturalness_reviewer` 角色，审查对象是一整章的连续阅读体验，
不是逐句润色。只审查：节奏与句长起伏、语域一致性、名词化与抽象名词堆叠、认知密度
（同一句或同一段同时维持的新对象、新目标、新条件、新方法、新义务数量）、段落是否只承担
一个主要认知任务、主次层级与推进顺序、作者脚手架或验收语言外泄、渐进披露、自然停顿点，
以及例题目标漂移（用完整构造解决只需展示含义的例题，或反之）。
C 不裁决数学正确性，不报告 TG-16，也不报告推理桥梁缺口。

只有显式启用的教学 job 默认开启 C；`traits.naturalness_review: false` 显式关闭。
非教学路径（总结、报告、cheatsheet、研究资料）保持现状。`naturalness_review` 必须是布尔值，
在教学审查分支的付费模型调用之前校验；非法值直接失败。有效开关与结果记录在既有 pedagogical dict
（`readability_enabled`、`readability_status`、`readability_gaps`、`readability_report`）中，
不新增 graph summary 字段或逐段元数据。

C 先按显式 `READABILITY_TYPES` allowlist 过滤，再驱动修补：
TG-13 语言过度书面化、TG-14 名词化过重、TG-15 认知密度过高（不止句长，还包括同一句或
同一段同时维持过多对象、目标、条件、方法或义务）、TG-17 层级或推进顺序混乱、
TG-18 作者脚手架或例题目标外泄。数学类 finding 或 TG-16 不能成为 C 的修补驱动，
只能留在 advisory。

C 必须给出一个小的 readability 完成记录（`completed: true`），以及 0..5 条 first_friction
首批摩擦观察，每条包含精确段号与逐字 `quote`。没有摩擦时也要显式给出空列表，
不能省略整个记录。记录缺失、`completed` 不为 true、段号越界或引文不匹配，都按失败处理，
不能静默当作“无问题”。该记录是模型自述，不是学生理解或可用性的证明。
first_friction 关注首次需要重读、失去主路径、想跳过、同时维持对象过多，
以及“正确但不自然”的表达；可选建议保持 advisory。

对 C 而言，`missing_information` 写的是需要的阅读调整（动作化措辞、拆分任务、减少重复、
给出优先次序），不一定是缺失知识。

## 执行约束

- 正文仍由现有强 Writer 负责；不要降级 Writer 或替代现有 correctness review。
  `WRITER_GUIDANCE` 已注入初稿和修订 Writer，它区分作者脚手架与读者正文。
- Naive Reader 只接收当前章节正文、标题、目标、读者画像、允许前置知识。
  不给完整 plan、作者意图、答案、rationale、repair 报告或内部推理。
- Reader 不是数学审稿人。作者未写出的概念连接、识别理由视为不存在，即使 Reader 能补出来。
  允许用明确前置知识执行正文已给的代入/计算；例如已给 A、Q、B=AQ 且允许矩阵乘法，
  计算 B 不算脑补。只给“选合适 Q”却要教构造 Q，才需要报告构造连接缺失。
- Reader 输出定位到原文片段的 Teaching Gap Report；不直接改数学正文。
- Orchestrator 区分定位证据与教学必要性：缺口须阻碍本章明确目标，先查本章是否已有解释。
  合并同根问题；更一般证明、更多分叉、额外例子或已允许前置知识的展开不自动成为缺口。
  运行时去除相同位置/引文/缺失信息的重复报告，显式 optional 建议留 advisory；
  这不等于自动完成语义裁决，不得宣称每个剩余建议均合理。Repair 只做必要的小修改。
  H2/H3 的必要性进入既有修补门禁；候选关系仍由强 Writer 和 technical guard 核实。
- 抽象概念、新方法与易混关系优先先给直觉，再给正式表达。
  用低维实例或操作前后对比避免抽象解释抽象。
- 作者规划例题时检查识别、起手理由、判断、分叉、易错点和回看。这是内部清单，
  不要求正文逐项回答，即使去掉标签也不能把整张清单变成读者必读段落。
  正文按例题的主要教学目标，只呈现眼前推进所需的步骤和理由；必要条件与推理桥梁保留。
- Repair 按 finding 来源区分。origin=comprehension（B）补最小必要的关系、等式、条件或一个
  中间步骤；origin=naturalness（C）优先动作化措辞、拆分任务、减少重复、给出优先次序，
  不通过新增例子、定义或总结块来修补阅读节奏。两者都必须保留全部假设、变量身份、公式来源、
  对象与表示的关系以及变换方向。需要跨段搬移内容才能完成的修补超出本所有权与预算，
  返回诚实的 bounded failure，不得整篇替换。
- 局部 repair 只拥有单个证据段落：唯一逐字替换、最多两轮、累计增长预算、独立候选 gate、
  没有 guard 不发布。
- 自测、独立练习及隐藏答案的 Review Mode 保留原教学设计：没有预先给答案不是缺口，
  不把 reader 的请求变成题干中的解答泄露。
- 一轮 reader、默认 C（可显式关闭）、局部 repair、teach-back、technical guard；当 teach-back 仍有证据缺口
  或首个提案被确定性检查拒绝时，最多再修一次。禁止无限循环。
- Teach-back 保留独立 B audit 与精确逐字证据；C 启用时同一次调用额外返回一个紧凑的候选
  连续阅读确认（`readability_confirmation`，含未解决的 C 问题）。这不新增模型阶段或调用。
  较早的 C 报告（`readability_report` / `readability_gaps`）在 teach-back 更新 gaps/advisory
  时仍作为历史证据保留。
- Repair 候选在独立 .workflow 目录验证；guard 不通过不覆盖正式正文。
  修补过的 readability 候选仍要经过 B 和最终 guard；内部问题没有印进正文时，干净正文保持不变。
- 技术 guard 检查修补差异：前提、量词、范围、公式、定义、结论与类比边界。
  禁止把“通常”升级为“必然”、把特例推广、用直觉替代定义。
  Guard 必须拒绝删除仍然必要的关系或推理桥梁，即使保留下来的等式本身为真；
  必须检查被移动或重排的条件在正文主路径使用它之前仍然可得。
- 默认教学路径的实际调用上限：Reader 家族最多 3 次（首次 Reader 加最多两次 Teach-back）、
  Repair 最多 2 次、Guard 1 次；启用 C 只复用既有 naturalness 调用 1 次，
  不新增第二次付费 C 调用、投票或评分阶段，也不新增节点或角色。
  Codex 订阅额度不是可观测的 API 账单。

## 路由与证据

角色与 provider/model/effort 只在 `${SHARED_WORKFLOW_ROOT}/config/models.example.yaml` 或显式本地配置中定义。
槽位是 `pedagogical_reader`、`naturalness_reviewer`、`pedagogical_repair`、`technical_guard`。
Reader 的模型选择是可替换的实验假设，不能因为便宜就自动视为合适。
DeepSeek 只承担 comprehension/readability，不裁决教学修补的最终数学正确性。
所有调用与模型、usage、原文、报告、候选、验证结果保留在项目 `.workflow`。

准确的执行 prompt 与 JSON schema 位于
`${SHARED_WORKFLOW_ROOT}/src/lanes/pedagogical.py`，不得在 job 中复制模型默认值。
详细调用与 A/B 方法参见 `${SHARED_WORKFLOW_ROOT}/docs/PEDAGOGICAL_READABILITY.md`。
复述测试按章节选择问题：解决什么、何时用、第一反应、第一步及原因、分叉、禁用条件、
易混关系、能否仅据正文重建操作链。无法从正文支持的回答标记 gap；评分不作为验收标准。
直观小例子不承担通用算法的全部分叉；证明段检查论证连接，练习段检查能否用已教方法起手。
正文式子和明确前置知识支撑的计算可以作为复述，不要求计算结果逐字出现。
Teach-back evidence 可以是一个逐字连续引文，或非空逐字引文列表；远隔正文位置分开列出。
禁止拼接、改写引文、删除 LaTeX 命令/标签或用省略号替代原文；每项单独验证。

整章运行时给出实际读者前置能力及具体目标，不要只截一句后要求恢复整套通用算法。
已有源使用 `existing_source_file`，前置内容只能以明确能力清单提供，不能给内部 plan/预期答案。
目标可指定“优先最多六个独立、影响起手的缺口”，这是该任务的审查范围，不是所有章节统一上限。
具体配置示例及实验边界见上述使用文档。仍最多两次 repair，不能用扩大目标来开启无限补课。
`traits.pedagogical_max_repair_rounds` 可显式设为整数 0..2，默认 2，实际额度记录在状态中。
0 是教学分支的只读验收：任何必要 B 缺口阻塞，不调用 Repair；没有必要缺口时仍执行 C
（若 C 启用）再做 Teach-back；C 因 B fail-fast 被跳过时记录 skip，不宣称完成了完整审查。
可用新冻结 job 对已修补副本验证引文格式，但不得借此重新获得 prose 修补额度。
与 `existing_source_file` 配合跳过初稿；此前候选相对原基线的数学检查仍须独立保留，
新 job 把候选视作原文不能替代该差异 guard。既有技术审查不因此被绕过。

## 回归保护

确定性覆盖在 `${SHARED_WORKFLOW_ROOT}/tests/test_readability_architecture.py`，并保留
`${SHARED_WORKFLOW_ROOT}/tests/test_hidden_inference.py` 的隐藏推理门禁测试。已有 B-only mock 可以显式
`naturalness_review: false`，但不能因此全局关闭默认 C 路径覆盖。
离线测试只验证确定性行为与 prompt 隔离，不证明学生可用性或文字质量。
现有 A/B 实验是小样本探索，不能据此宣称已证明人类可读性；不要声称学生可用性已实验证明。
