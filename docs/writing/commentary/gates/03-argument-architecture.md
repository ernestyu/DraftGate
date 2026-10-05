# G3 — Argument Architecture + Draft Construction

## Goal

按读者理解问题的顺序组织章节和论证，而不是按作者研究过程排列。

G3 先完成 human-in-the-loop Narrative Mode Decision，再基于用户选择完成正式 argument architecture。Architecture 稳定后，G3 还必须判断当前文章是否已经构成 substantive first draft；如果仍然只是 seed、outline、section skeleton 或 materially incomplete draft，则继续完成 Draft Construction 后才能 PASS。

Narrative mode 负责决定文章如何推进；central explanatory frame / narrative anchor 只是其中一种可选结构工具，不是所有文章的默认写法。

## Reader outcome

普通读者能清楚知道文章由什么驱动、为什么按当前顺序推进，以及每类材料承担什么职责。

中层读者不仅能复述因果链，还能区分：

~~~text
Primary narrative driver
Primary mechanism
Supporting evidence
Local analogy
Removable / demoted material
~~~

## Narrative Mode Decision

G3 在正式 architecture 前，必须根据已经冻结的 G1 main question 和 G2 scope，向用户提出 1–3 个适合当前文章的 narrative-mode candidates。

候选可以包括：

~~~text
question-driven
frame-driven
case-driven
hybrid
other / no special narrative mode
~~~

这些不是固定模板，也不是必须全部展示的枚举。

Agent 可以组合、细化或提出更适合当前文章的模式，但不得机械给出所有选项。

每个候选必须简要说明：

1. 为什么适合当前文章；
2. 文章如何推进；
3. 什么材料成为主线；
4. 什么材料降为 supporting evidence；
5. 主要风险是什么。

### Explicit user selection

Narrative Mode Decision 是 G3 的 human-in-the-loop writing decision。

Agent 不得自动替用户选择。

如果用户尚未明确选择某个候选，或明确提出并选择另一个可行模式：

~~~text
G3 state 保持不变
不得 advance
不得标记 G3 PASS
不得产生 gate completion transaction
~~~

等待用户选择不是 Gate completion。

Narrative mode 不进入 persistent state，不新增 state field，也不新增 runtime status。

## Mode contracts

这些 contract 定义基本推进原则，不是固定目录模板。

### question-driven

Primary driver 是 main question。

典型推进：

~~~text
main question
→ progressively deeper explanation
→ mechanism
→ implication / boundary / judgment
~~~

要求：

- 通过问题逐层深入；
- 不强制 central frame；
- Central frame decision 可以是 NOT NEEDED；
- 各 section 必须继续推进同一个问题，而不是变成互不相干的小文章；
- example / evidence 服务于某一解释步骤，不得形成竞争主线。

### frame-driven

Primary driver 是 central explanatory frame。

典型推进：

~~~text
central frame
→ frame 内部机制
→ 映射到现实问题
→ 主机制展开
→ competing explanation / boundary
→ 回到 frame
~~~

要求：

- Central frame decision 必须是 USED；
- frame 必须贯穿多个主要部分；
- frame 必须承担真实分析功能，而不只是 opening hook；
- frame 必须帮助解释 mechanism；
- 不服务于 frame 或 primary mechanism 的材料应降级或删除；
- G1 / G2 仍然具有更高 authority。

### case-driven

Primary driver 是 case / observable situation 本身。

典型推进：

~~~text
case / phenomenon
→ case 内部发生了什么
→ mechanism
→ controlled generalization
→ boundary / implication
~~~

要求：

- case 本身是研究对象；
- generalization 逐步展开；
- 不得把案例偷偷改成 unrelated metaphor；
- 不得从单一 case 直接跳到普遍规律；
- local analogy 与 case 必须保持职责区分。

### hybrid

Hybrid 可以组合两个或以上 narrative devices，但必须明确一个 primary driver。

例如：

~~~text
primary driver = question-driven
secondary device = frame
~~~

或：

~~~text
primary driver = case-driven
secondary device = question progression
~~~

不得出现两个竞争主线。

如果读者可以合理地把两组不同材料都理解成全文主轴，architecture 尚未稳定，G3 不能 PASS。

### other / no special narrative mode

如果上述模式都不合适，可以使用其它明确描述的 architecture，或者 no special narrative mode。

要求：

- 明确 primary driver；
- 明确文章的 progression rule；
- 不得因为缺少特殊叙事装置而强行制造 frame / case。

## Conditional phenomenon-first architecture

对于 frame-driven / case-driven，如果存在具体、可观察且真正有解释价值的现象，可以优先：

~~~text
phenomenon
→ mechanism
→ main question / larger implication
~~~

phenomenon-first 只是条件性选择，不是全局 opening 要求。

以下情况不得强制 phenomenon-first：

- phenomenon 只是 decorative hook；
- main question 必须先建立才能理解后续内容；
- 文章主要是 question-driven；
- phenomenon 会延迟真正的 analytical problem；
- opening 会因此变成 anecdotal storytelling。

## Explanatory Spine Check

Narrative Mode Decision 完成后、正式 architecture PASS 之前，G3 必须建立 Explanatory Spine。

定义：

~~~text
Explanatory Spine
=
全文持续推进的一条 mechanism / relationship / contradiction / constraint chain
~~~

它回答：

~~~text
文章为什么能从第一步推到最后一步？
~~~

Explanatory Spine 必须体现 causal、logical 或 structural progression，不能只是 section topic list。

### Narrative Mode != Explanatory Spine

Narrative Mode 回答：

~~~text
文章怎么讲？
~~~

Explanatory Spine 回答：

~~~text
文章为什么能从第一步推到最后一步？
~~~

因此：

~~~text
Narrative Mode != Explanatory Spine
~~~

question-driven、frame-driven、case-driven、hybrid、other / no special narrative mode 都必须有 Explanatory Spine。

### Central Frame != Explanatory Spine

Central Frame 是可选 narrative device。

Explanatory Spine 是所有文章都必须存在的解释链。

因此：

~~~text
Central Frame != Explanatory Spine
~~~

frame 可以帮助展示 spine，但不能替代 spine。

frame-driven 文章如果读者只能记住 frame，却说不清 mechanism chain，G3 不能 PASS。

case-driven 文章如果只描述 case 发生了什么，却没有推出 mechanism、relationship、constraint 或 implication chain，G3 不能 PASS。

### Required spine output

G3 必须明确输出：

~~~text
Explanatory spine:
<用 1–3 句话表达>
~~~

1–3 句话是 reasoning compression artifact，不进入 persistent state，也不写入 workflow JSON。

一个合格 spine 通常应能看出：

~~~text
starting condition
→ core mechanism / relationship
→ intermediate implication
→ final structural judgment
~~~

这不是固定公式，要求的是 continuity。

### Section binding

每个 major section 都必须能够回答：

~~~text
本节如何推进 Explanatory Spine？
~~~

只回答：

~~~text
本节和主问题有关
~~~

不够。

major section 至少应承担一个清楚的 spine function，例如：

- establish starting condition；
- explain primary mechanism；
- introduce required intermediate link；
- test / qualify the mechanism；
- derive implication；
- expose structural contradiction；
- move from mechanism to final judgment。

如果某节有趣，但没有推进或支持 spine，则必须：

~~~text
demote
remove
or rewrite its role
~~~

这属于现有 Material Hierarchy，不新增 parallel structure。

## Material Hierarchy

完成 Narrative Mode Decision 后，G3 必须对主要材料做职责分层。

至少包括：

~~~text
Primary narrative driver
Primary mechanism
Supporting evidence
Local analogy
Removable / demoted material
~~~

如果是 frame-driven，还必须明确：

~~~text
Central frame role
~~~

Material Hierarchy 属于 G3 reasoning / architecture artifact，不进入 persistent state。

### Primary narrative driver

决定读者如何从文章开头走到结尾的唯一主驱动。

全文只能有一个 primary narrative driver。

### Primary mechanism

回答 G1 主问题的核心解释机制。

叙事装置可以帮助展示 mechanism，但不得替代 mechanism。

### Supporting evidence

事实、案例、数据、观察或例子，只承担清楚的辅助职责。

每一组 supporting evidence 都必须能够回答：

~~~text
它具体支持哪个 claim / mechanism step？
~~~

Supporting evidence 不得形成竞争 narrative spine。

### Local analogy

只服务于局部理解的 analogy / concrete scenario。

Local analogy 不得在没有重新完成 G3 architecture decision 的情况下升级为全文 central frame。

### Removable / demoted material

材料本身可能正确、精彩或有趣，但如果不服务于 primary narrative driver、primary mechanism 或明确 supporting role，就应：

~~~text
remove
/
shorten
/
demote
~~~

核心规则：

~~~text
good example != suitable example
~~~

一个例子“很好”不等于它适合当前文章。

## Compression Test

G3 Exit 前必须执行 Compression Test：

~~~text
去掉标题、案例、数据、小节和修辞后，
能否用 3–4 句话完整表达文章独特的推理链？
~~~

3–4 句话必须保留：

~~~text
starting point
core mechanism
key intermediate inference
final judgment
~~~

句数是 reasoning test，不是正文格式限制。

### PASS

PASS 时，压缩后仍能看出：

- reasoning 从哪里开始；
- 哪个 mechanism / relationship 承担主要解释工作；
- 哪个 key intermediate inference 把 mechanism 推向下一步；
- final judgment 为什么由前面推出。

### FAIL

以下至少属于 FAIL：

- 只能列出几个观点；
- 只能列出几个 section topic；
- 只能复述 main question；
- 压缩后只剩主题词，看不出 mechanism；
- key intermediate inference 消失；
- final judgment 突然出现，看不出 reasoning path；
- 只有恢复 examples / rhetoric 后文章才显得连贯。

Compression Test 不要求正文只有 3–4 个观点。

它只检查全文是否存在一条可压缩的 unified reasoning skeleton。

## Draft Construction

Architecture 完成后，G3 进入 Draft Construction Check。

核心目标：

~~~text
major section responsibility
→ substantive prose that performs that responsibility
~~~

### When expansion is required

如果当前文章仍然属于以下任一种状态：

- seed draft；
- outline；
- section skeleton；
- placeholder-heavy draft；
- major section 只有一两句职责说明；
- materially incomplete draft；

G3 必须把 major sections 展开成可连续阅读的 complete first draft，不能以 outline-only 状态 PASS。

以下内容不能被视为完成 section responsibility：

- one-line placeholder；
- section-purpose note；
- outline bullets；
- “本节将解释……”一类只描述未来内容的句子；
- heading 下没有 substantive development。

不得使用固定 word count、paragraph count、sentence count 或 character threshold 判断 draft completeness。

### Existing substantive prose

如果已有正文已经完成其 section responsibility，应尽量保留。

G3 只做满足当前 architecture 和 Draft Construction Check 所必需的修改，不得因为进入 G3 就重新生成整篇文章。

### Allowed Draft Construction work

G3 可以为了构造完整正文：

- 展开已经由 G1 / G2 / G3 授权的解释；
- 展开 scope 内已经存在的 mechanism；
- 把 section responsibility 写成 substantive prose；
- 使用用户已经提供或文章已经包含的事实、例子和材料；
- 写必要的段落、正常句子和过渡；
- 让 major sections 与 Explanatory Spine 连续衔接；
- 应用 G3 Custom Rules。

### Downstream authority boundary

核心边界：

~~~text
draft construction necessity
!=
downstream Gate responsibility
~~~

G3 可以为了构造 complete first draft 写解释、段落、过渡和正常句子。

但 G3 不得以独立目标执行：

- G4 accessibility audit；
- G5 adversarial / evidence pressure test；
- G6 paragraph audit / restructuring；
- G7 language / pattern / AI-trace cleanup。

如果 G3 看见这些 downstream 问题，除非修正是产生 coherent substantive draft 所严格必需，否则留给对应 Gate。

G3 还不得：

- 发明事实、数据、quotation、source 或 evidence；
- 把 unsupported factual claim 当作已验证事实；
- 为增加长度而扩写；
- 越过 G2 scope；
- silently rewrite G1 thesis。

## Central frame decision

Narrative Mode Decision 完成后，G3 继续保留：

~~~text
Central frame decision:
USED
or
NOT NEEDED
~~~

这个决定不进入 persistent state。

不同 narrative mode 下：

~~~text
question-driven
→ central frame 可为 NOT NEEDED

frame-driven
→ central frame 必须为 USED

case-driven
→ case 是 driver；通常不需要再制造另一个 metaphorical central frame

hybrid
→ 由已声明的 primary driver 决定 central frame 是否 USED
~~~

### USED

只有当某个 frame 同时满足以下条件时才使用：

- 与 G1 主问题直接相关
- 服务于 G2 已冻结主线
- 能承担机制解释，而不只是制造故事感
- 能在文章后部继续产生分析价值
- 可以在至少两个以上文章阶段 / 章节中持续发挥作用
- 不会把读者带向另一篇文章

frame 必须服从文章主问题，不能为了适应 frame 反过来修改 G1 thesis 或 G2 scope。

### NOT NEEDED

如果不存在天然合适的 central frame，就使用 NOT NEEDED。

不得为了满足 G3、传播性或“更好看”而强行制造故事。不得为了通过 G3 强行增加 frame。

## Frame quality check

G3 采用 central frame 前必须问：

1. 这个 frame 是否真正帮助解释主问题？
2. 它是否只是一个漂亮 hook，还是能持续承担分析功能？
3. 开头引入后，中段还能否继续推进机制？
4. 结尾能否自然回到它？
5. 它是否会抢夺主线或诱导文章迁就类比？
6. 如果没有它，文章是否反而更清楚？

不合格 frame 包括：

- 只负责吸引眼球的历史故事
- 与主问题弱相关的名人 / 战争 / 电影 / 文学隐喻
- 开头出现、后文完全不用的 disconnected hook
- 为了“宏大感”添加的场景
- 无法继续承载机制解释的记忆点

## G3 / G4 boundary

G3 负责：

~~~text
whole-article frame / narrative architecture
/
primary narrative driver
/
central frame decision
~~~

G4 负责：

~~~text
local explanatory analogy
/
concrete scenario
/
局部直觉解释
~~~

如果 G3 已经采用 central frame，G4 可以补足局部映射、具体解释和必要边界说明，但不得重新发明一个新的全文主框架，也不得把局部类比升级成新的 central frame。

## G5 challenge boundary

Central frame 和 narrative mode 都不是不可触碰的修辞核心。

后续 G5 仍必须能够挑战：

- frame 是否过度类比
- 映射是否成立
- competing mechanism 是否存在
- 哪些地方不再相似
- case 是否支持当前 generalization

如果 G5 发现 frame / case 导致 claim 失真，按现有 G5 / reopen / correction semantics 处理。

不得因为 frame “写得漂亮”而保留错误映射。

## Allowed

- 提出 1–3 个当前文章适用的 narrative-mode candidates
- 在用户明确选择后完成 architecture
- 建立并输出 Explanatory Spine
- 对 major sections 执行 spine binding
- 执行 Compression Test
- 重排章节
- 合并或拆分章节
- 明确每节唯一任务
- 调整必要过渡，使递进关系成立
- 建立 Material Hierarchy
- 判断 central frame 是否 USED / NOT NEEDED
- 删除或降级会制造竞争主线的 supporting material
- 在需要时把 seed / outline / incomplete draft 展开成 complete first draft
- 为 Draft Construction 写必要的解释、段落、过渡和正常句子

## Forbidden

- Agent 自动替用户决定 narrative mode
- 用户尚未选择时 advance G3
- 用 Narrative Mode 或 Central Frame 冒充 Explanatory Spine
- 让 major section 只“和主问题有关”却不推进 spine
- 在 G3 silently rewrite G1 thesis
- 改变 G1 已冻结的主问题
- 把 G2 已降级的支线重新抬成主线
- 为了传播性强行制造故事
- 使用与主问题弱相关的历史类比
- 让 supporting evidence 形成竞争 narrative
- 为了保住 frame 修改 G1 thesis 或 G2 scope
- 引入只在开头出现、后文不再承担功能的 decorative hook
- 把 phenomenon-first 当成全局要求
- 把 G4 accessibility audit 当作 G3 独立目标
- 把 G5 adversarial / evidence pressure test 当作 G3 独立目标
- 把 G6 paragraph audit / restructuring 当作 G3 独立目标
- 把 G7 language / pattern / AI-trace cleanup 当作 G3 独立目标
- 做逐句语言润色作为独立 cleanup 任务
- 做 AI trace cleanup

## G1 / G3 authority boundary

G1 负责：

~~~text
发现并冻结值得写的 core insight / thesis
~~~

G3 负责：

~~~text
把 frozen insight 展开成 coherent Explanatory Spine
→ 再组织成 narrative architecture
~~~

G3 可以澄清 thesis 的 implication，但不得 silently replace or rewrite G1 thesis。

如果无法形成 coherent spine，而根因来自 frozen G1 thesis：

~~~text
STOP
→ report G1 conflict
→ do not advance G3
→ do not silently rewrite thesis
~~~

用户继续使用现有 reopen / correction / start-cycle semantics。

不得新增 rollback mechanism。

如果 architecture 检查暴露出 claim 本身存在证据或强度问题：

~~~text
STOP
→ report conflict
~~~

不得在 G3 顺手修改 G5 claim boundary。

## Conditional resource

读取 `../structure-rules.md`。

## Exit

G3 PASS 前必须全部满足：

1. 用户已明确选择或批准 narrative mode；
2. Primary narrative driver 唯一且清楚；
3. Primary mechanism 清楚；
4. Explanatory Spine 已明确用 1–3 句话表达；
5. 每个 major section 都推进或支持 Explanatory Spine；
6. Supporting evidence 均有明确辅助职责；
7. Supporting evidence 不形成 competing narrative；
8. Local analogy 保持局部职责；
9. 必要时已识别 Removable / demoted material；
10. section progression 与选定 mode 一致；
11. Central frame decision 与 narrative mode 一致；
12. Compression Test = PASS；
13. G1 thesis unchanged；
14. G2 scope unchanged；
15. Draft Construction Check = PASS；
16. 每个 major section 已有 substantive prose 完成其 section responsibility；
17. 文章可作为 complete first draft 连续阅读，而不是 outline / placeholder skeleton；
18. 已有足够正文已尽量保留，只做必要修改；
19. G4–G7 downstream responsibilities 未被 G3 作为独立目标执行。

如果等待用户选择：

~~~text
G3 = WAITING FOR USER
state unchanged
no advance
~~~

WAITING FOR USER 只是 conversational execution condition，不是新的 runtime state status。

标记 G3 PASS 后停止。
