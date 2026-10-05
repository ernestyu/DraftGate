# G5 — Claim & Evidence Boundary

## Goal

检查并收紧事实、证据、因果、类比、外推和不确定性边界，并对主要 thesis / major claims 执行 adversarial / counterfactual pressure test。

## Reader outcome

专业读者能够看清作者知道“证据证明到了哪里”，也能看出核心判断经受过合理反驳、竞争机制和失败条件的压力测试。

## Required pressure test

对主要 thesis / major claims，G5 必须至少回答：

1. 最强的合理反驳是什么？
2. 是否存在另一种机制或解释，可以解释同一组事实而不依赖本文核心机制？
3. 什么事实、条件或观察如果成立，会明显削弱或推翻该 claim？
4. 经历压力测试后，claim 应保持、收窄、降低强度、增加条件、增加竞争解释，还是删除？

### Strongest reasonable objection

反驳必须是信息充分、逻辑成立、与实际 claim 相关、专业读者可能真实提出的 objection。

不得用以下内容完成检查：

- strawman objection
- 明显错误的反方
- 与文章无关的极端情况
- 为了方便反驳而人为简化的对方观点

如果存在多个合理反驳，优先处理最可能改变核心 claim 的那个。

### Alternative mechanism

必须主动检查同样的事实是否可以由另一种合理机制解释。

如果存在合理竞争解释，不得把本文机制继续写成唯一原因，除非现有证据确实支持唯一性。

可采用的 G5 内修复包括：

- 收紧因果语言
- 增加适用边界
- 明确只是一个解释
- 增加最小必要的竞争机制说明
- 说明为什么竞争解释不足，但前提是正文已有证据支持

### Counterfactual / falsification condition

主要 claim 应尽可能具有可理解的失败条件或适用边界。

必须能够回答：

“什么观察、条件或事实如果成立，会让这个 claim 明显变弱或失败？”

不得接受“无论发生什么都说明本文正确”这类 self-sealing 结构。

## Narrative-compatible adversarial expression

G5 的 rigor 语义保持不变，但表达方式可以与文章已经建立的 mechanism / narrative frame 兼容。

如果不损失精度，strongest reasonable objection、boundary、counterfactual / falsification condition 可以优先通过现有 mechanism 或 narrative frame 表达。

例如：

- frame-driven 文章可以让 strongest objection 直接作用于 central frame，说明 frame 在哪里失效；
- case-driven 文章可以通过 case 中哪些事实不足以支持 generalization 来表达 boundary；
- question-driven 文章可以通过“什么条件下这个 answer 不再解释 observed pattern”表达 falsification condition。

这样做可以避免机械增加论文式 limitation 段。

但优先级必须明确：

~~~text
precision > narrative elegance
~~~

如果既有 frame / mechanism 无法准确表达 objection、boundary 或 falsification condition，必须继续使用直接、抽象、技术性的表述。

Narrative compatibility 不得降低：

- objection strength；
- evidence boundary；
- causal uncertainty；
- alternative mechanism；
- falsification condition；
- scope limitation。

不得为了保持叙事顺滑而把 uncertainty 藏进 metaphor，也不得为了保留 frame 而弱化真实反驳。

## Pressure-test outcomes

允许的 G5 outcome：

- KEEP
- NARROW_SCOPE
- LOWER_STRENGTH
- ADD_CONDITION
- ADD_COMPETING_EXPLANATION
- REMOVE_UNSUPPORTED_CLAIM
- STOP_CONFLICT

KEEP 表示完整 pressure test 已通过，核心 claim 不需要调整。

KEEP 不等于强制 NO_CHANGE。

如果 KEEP 之后仍有真实且属于 G5 scope 的必要修改，例如补充限制条件、收紧一句因果表述或补一个必要边界，则走 CHANGED。

如果完整 adversarial / counterfactual pressure test 已执行，并且：

- strongest reasonable objection 已评估
- alternative mechanism 已评估
- falsification / weakening condition 已评估
- 主要 claims 已满足 G5 exit contract
- 不存在任何必要的 G5-authorized article modification

则允许：

~~~text
KEEP
→ G5-authorized NO_CHANGE
~~~

仅仅“没有发现问题”但没有完成完整 pressure test，不构成合法 NO_CHANGE。

## Allowed

- 区分事实 / 相关性 / 机制解释 / 推断
- 收紧过强因果
- 给类比增加适用边界
- 补充主要竞争解释或限制
- 降低超过证据范围的 claim 强度
- 增加必要条件
- 删除无法站住的过强判断
- 增加最小必要的边界说明

如果 outcome 需要正文修改，必须走现有 CHANGED gate transaction。

如果 KEEP 且正文已经完全满足 G5 contract、无需修改，允许通过已冻结的 NO_CHANGE infrastructure 完成 G5。

## Forbidden

- 为了力度把推断升级成事实
- 把单一案例写成普遍规律
- 对没有证据的问题补写确定结论
- 为了保住 thesis 而忽略合理竞争解释
- 构造弱 strawman 来“完成”反驳检查
- 做段落美化或 AI trace cleanup
- 改变 G1 主问题
- 重新选择 thesis
- 重做 G2 scope
- 重做 G3 argument architecture
- 大规模重排章节
- 做 G6 paragraph restructuring
- 做 G7 language cleanup
- 做 workflow complete 后的最终传播标题设计

## STOP_CONFLICT

如果压力测试发现核心 thesis 本身无法成立，或者修复需要回到 G1–G3：

~~~text
STOP_CONFLICT
→ 不 advance G5
→ 不使用 NO_CHANGE
→ 不修改 state
→ 不自动回退 G1–G3
~~~

由用户决定是否开启新 cycle / correction。

NO_CHANGE 不得替代：

- STOP
- NEEDS_USER
- 无法判断
- 未完成 pressure test
- STATE STALE

## No mandatory opposition section

Counterfactual / adversarial check 不要求新增“反方观点”章节。

如果现有正文已经覆盖 objection，可不增加任何反方段落。

如果只需要收紧一句 claim，只做最小修改。

如果确实需要向读者说明竞争解释，只增加最小必要内容。

不得为了展示“考虑全面”机械加入：

- “有人可能会说……”
- “另一种观点认为……”
- “当然也有人反对……”

## NO_CHANGE semantic condition

G5 允许 NO_CHANGE，仅当：

~~~text
完整执行 adversarial / counterfactual pressure test
+
所有主要 claim 已满足 G5 exit contract
+
不存在需要的 G5-authorized article modification
~~~

此时：

~~~text
article blob unchanged
article_revision unchanged
exactly one G5 → G6 transition
state-only gate commit
~~~

并继续使用：

~~~text
Writing-Workflow: gate
Writing-Article: <article_id>
Writing-Gate: G5
~~~

validator branch 由 repository facts 决定：

~~~text
article blob changed → CHANGED
article blob unchanged → NO_CHANGE
~~~

不得由 Agent 自报 outcome 决定。

## Exit

G5 PASS 前必须能回答：

1. major claim 的最强合理反驳是什么？
2. 是否存在合理竞争解释？
3. 什么条件会削弱该 claim？
4. 经检查后，claim strength 是否与证据和反事实压力相匹配？

只有主要 claims 经压力测试后仍有清楚、可辩护的边界，G5 才能 PASS。

如果需要 G5-authorized article change，则按 CHANGED 完成。

如果完整检查后无需任何正文修改，则 KEEP 可按 G5-authorized NO_CHANGE 完成。

如果为 STOP_CONFLICT，则不得 PASS、不得推进 state。
