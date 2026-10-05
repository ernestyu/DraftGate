# G1 — Main Question & Thesis

## Goal

只确定文章的唯一主问题、核心判断和必要边界。

在冻结 thesis 之前，必须执行 Insight Test，确认核心判断不仅正确，而且具有足够的 explanatory value，值得支撑一篇完整文章。

## Reader outcome

普通读者应能用一句话说明：这篇文章到底在回答什么。

同时，核心判断应让读者看见一个此前不明显、但能帮助解释主问题的 mechanism、relationship、constraint、structural role 或 structural change，而不是只看到一组常识性后果。

## Correct observation vs explanatory insight

G1 必须区分：

~~~text
correct observation
!=
worth-writing explanatory insight
~~~

正确材料不自动等于值得冻结的 thesis。

例如：

~~~text
AI 大量替代工作
→ 收入下降
→ 税收变化
→ 身份受影响
~~~

这些都可能是正确观察，但如果只是把显而易见的 consequences 串在一起，本身未必构成足够强的 explanatory insight。

更强的 insight 应指出一个能够把这些现象连接起来的 mechanism、relationship、constraint、structural role 或 structural change。

核心标准：

~~~text
non-obvious enough to add explanatory value
~~~

不是：

~~~text
novel at all costs
~~~

## Insight Test

G1 PASS 前必须至少回答：

1. thesis 是否只是 visible phenomena 或 downstream consequences 的汇总？
2. thesis 是否指出一个不只停留在表面的 mechanism、relationship、constraint、structural role 或 structural change？
3. 这个 insight 是否真正帮助解释 G1 main question？
4. 去掉这个 insight 后，文章是否会退化成 common observations 的集合？
5. 这个 insight 是否有足够依据，还是只是为了显得“深刻”而被拔高？

Insight Test 不要求 thesis 必须原创，也不要求提出新理论。

目标是 explanatory value，而不是 originality prestige。

## Weak insight handling

如果 thesis 技术上正确，但仍然主要是 obvious、descriptive 或 consequence-list based：

~~~text
G1 must not automatically PASS
~~~

必须：

~~~text
指出当前 insight 为什么仍弱
→ 与用户继续讨论
→ refine or replace thesis
→ G1 state unchanged
→ do not advance
~~~

这是 conversational waiting condition。

不得新增 WAITING_INSIGHT、NEEDS_INSIGHT 或其它 runtime state/status。

## Insight boundaries

G1 明确禁止：

- 为了显得新颖而制造 contrarian claim；
- 为了“有洞见”夸大 claim strength；
- 要求 thesis 必须 historically original；
- 要求文章必须提出 new theory；
- 用 concept naming 代替真实 explanation；
- 把 uncertainty 写成 certainty 以制造“深度”；
- 因为某个 mechanism 听起来更有意思，就保留 evidence 不足的说法。

允许：

- 用更有解释力的方式重述已知 mechanism；
- 指出读者未必已经连接起来的 structural relationship；
- 用一个 underlying constraint 解释多个熟悉 consequences；
- 在 evidence 只支持 modest claim 时，冻结 modest but useful insight。

forced profundity forbidden。

novelty is not required。

## Allowed

- 从选题、材料或旧稿中提炼唯一主问题
- 用 1–2 句话写核心判断
- 标注明显事实 / 判断 / 推断边界
- 执行 Insight Test
- 在 insight 仍弱时与用户继续讨论，不 advance
- 在缺少会改变主问题的信息时向用户做最小澄清

## Forbidden

- 重排章节
- 改写整篇正文
- 处理段落
- 做语言润色或 AI trace cleanup
- 扩展支线
- 把 consequence aggregation 当成足够的 thesis
- 为了“深刻”制造 unsupported mechanism
- 把概念命名当成解释本身

## Exit

G1 PASS 必须同时满足：

~~~text
unique main question
+
core thesis
+
necessary boundary
+
Insight Test = PASS
~~~

Insight Test PASS 表示：

- thesis 不只是 consequence list；
- thesis 提供真实 explanatory value；
- insight materially helps answer main question；
- removing the insight would materially weaken the article and expose a common-observation collection；
- claim strength remains supported。

如果 Insight Test FAIL：

~~~text
no G1 PASS
state unchanged
no advance
~~~

输出主问题、核心判断、必要边界和 Insight Test 结果；满足全部条件后标记 G1 PASS 并停止。
