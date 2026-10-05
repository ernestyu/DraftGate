# DraftGate 使用说明（暂定）

很多人第一次用 AI 写文章时，会觉得事情应该很简单：把自己的想法、材料和要求告诉模型，它就应该能够直接给出一篇完整文章。对于需要多轮判断、结构控制和证据边界的长文，这种做法很容易暴露问题。主旨可能漂移，结构可能松散，例子和论点之间的关系也可能不稳定；让模型修改一个地方，它还可能顺手改动已经确定的部分。

于是另一种做法出现了：不断增加 prompt、writing skill 和写作规则，希望靠一套更复杂的说明，让 AI 一次把文章写好。但规则变多，并不会自动让复杂写作变得可控。模型仍然需要同时处理“这篇文章真正要回答什么”“哪些材料应该保留”“结构应该怎样推进”“哪些判断写得过强”“段落怎样组织”“最后的语言是否自然”等不同问题。把这些职责塞进同一次执行，本身就容易互相干扰。

本文要回答的问题是：**怎样用 DraftGate，把 AI 辅助写作从一次难以控制的“整篇生成”，变成一个人可以逐步讨论、判断、修改和验证的过程？**

核心判断是：对于需要反复判断、修改和核查的复杂长文，human-in-the-loop 仍然很重要，也就是人在整个写作过程中持续参与关键判断，而不是把主题交给 AI 后等待最终成品。AI 可以参与讨论、提出思路、寻找反例、核查事实和证据，也可以帮助组织结构和修改表达，但文章的关键判断仍然需要人持续参与。DraftGate 做的事情，是把这些不同性质的写作职责拆成 G1–G7 七个阶段，每个 Gate 只处理一种问题。它再用 Git state 记录文章当前进行到哪一步，并用 CI 在每次提交后自动验证 Gate 顺序、state 是否匹配以及状态转移是否合法。

本文重点是 DraftGate 的实际使用，而不是展开一套抽象的 AI 写作理论。下面会从最开始的准备讲起，并且用这篇文章自己的生成过程作为贯穿案例：我们怎样从一个很模糊的“写一篇 DraftGate 教程”开始，经过 Pre-G1、G1、G2、G3，一直到后面的检查与修订；中间遇到什么问题，state 怎样变化，什么时候应该 reopen，什么时候应该重新开一个 cycle。

## 1. 为什么需要把写作拆成多个阶段

DraftGate 的出发点不是“AI 不会写”，而是复杂写作里同时存在很多不同层次的判断。比如，文章的主问题是否准确，是 G1 层面的事情；某个例子是否跑题，是 G2 层面的事情；整篇怎样推进，是 G3；某个概念普通读者能不能理解，是 G4；一个判断有没有写过头，是 G5；段落是否承担清楚的论证职责，是 G6；最终语言有没有机械重复，则属于 G7。

这些问题当然可以一次全部告诉模型，但那样会带来两个麻烦。第一，模型必须同时记住大量不同层级的约束；第二，修改一个层级时，很容易顺手动到已经确定的另一个层级。例如你只是想改一段语言，模型却顺便换了论点；你只是想补一个例子，它又重新安排了文章结构。

DraftGate 的处理方式是把这些责任拆开。一次 invocation 只执行一个 Gate；当前 Gate 完成后，文章和 state 一起提交，然后停止。下一步是否继续，由用户明确决定。这样做的目的不是把写作变成流水线，而是让人的判断有清楚的落点：现在是在讨论 thesis，就只讨论 thesis；现在是在做结构，就不要同时把语言和证据全部重做。

这也是 human-in-the-loop 在 DraftGate 里的实际含义。人不是最后才来“验收”AI 写出的文章，而是在每一个重要节点上参与决定。

## 2. 使用前准备

最简单的使用方式是先准备一个自己的 GitHub 仓库副本。

打开 DraftGate 仓库：

```text
https://github.com/ernestyu/DraftGate
```

在 GitHub 页面右上方选择 **Fork**，把仓库复制到自己的 GitHub 账户。之后会得到一个类似下面的地址：

```text
https://github.com/<your-name>/DraftGate
```

后面的文章、state、Custom Rules 和 GitHub Actions 都发生在这个 fork 中，不会修改原始 DraftGate 仓库。

接下来需要一个能够读取和修改 GitHub 仓库的 AI Agent。它可以是能够连接 GitHub 的 ChatGPT，也可以是其它可以读文件、改文件、提交 Git commit 的 Agent。把你自己的 fork 地址交给它，并明确告诉它先读取仓库里的：

```text
AGENTS.md
docs/writing/commentary/workflow.md
```

这两个文件告诉 Agent：一次只能执行一个 Gate、应该读哪些规则、什么时候必须停止、文章和 state 怎样一起提交。

如果你在本地使用，也可以直接 clone 自己的 fork。DraftGate 本身只需要 Git 和 Python 3.10+，不需要 Docker、数据库或 self-hosted runner。仓库自带的 GitHub Actions 使用 GitHub-hosted runner，因此普通用户不需要自己维护服务器。

开始一篇新文章时，先创建 Markdown：

```bash
./writing bootstrap --article-id 20261005-example-topic --title "暂定标题"
```

它会创建：

```text
articles/20261005-example-topic/index.md
```

这里有一个容易忽略的点：**不要刚创建文件就立刻冲进 G1。** DraftGate 正式 state control 之前，还有一个很重要的 Pre-G1。

## 3. Pre-G1：先把想法讨论清楚

Pre-G1 可以理解为 brainstorm。它不属于 state machine，没有 Gate ID，也没有 PASS / FAIL。这个阶段就是允许你和 AI 发散讨论。

你可以说：“我想写一篇关于 AI 写作的文章，但还没想清楚角度。”也可以继续追问：“这个题目真正值得写的地方是什么？”“我不满意现有 AI 写作工具的到底是哪一点？”“这个问题是不是太宽？”

Pre-G1 的目标不是得到一篇文章，而是让你自己逐渐弄清楚：为什么想写、想讨论什么、可能要回答什么问题。

这篇教程本身就是一个例子。我们最开始只有一句话：“写一篇 DraftGate 使用教程。”如果直接进入 G1，得到的主问题很可能只是“DraftGate 怎么用”，文章也容易变成 README 的扩写。经过几轮开放讨论后，才逐渐明确这篇教程真正要解释的是：为什么一次性生成和复杂 writing skill 仍然容易失控，以及 DraftGate 怎样把人的判断拆到一个个可控制的步骤里。

等方向大致清楚后，再初始化 state：

```bash
./writing init --article-id 20261005-example-topic
```

从这一刻起，文章才正式进入 G1→G7 的受控流程。

## 4. G1 — Main Question & Thesis

G1 解决的是最上层的问题：**这篇文章到底在回答什么，以及核心判断是什么。** 它不负责排目录，也不负责润色。如果主问题本身错了，后面的结构再完整，也只是把错误的问题写得更完整。

这篇教程进入 G1 时，我们已经通过 Pre-G1 知道自己不只是想写一个“软件说明”。最后冻结的主问题是：“怎样用 DraftGate，把 AI 辅助写作从一次难以控制的整篇生成，变成一个人可以逐步讨论、判断、修改和验证的过程？”

同时冻结的核心判断是：对于需要反复判断、修改和核查的复杂长文，human-in-the-loop 仍然很重要；DraftGate 通过 G1–G7 把不同职责拆开，再用 Git state 和 CI 把执行顺序与验证放到模型之外。

G1 完成后，state 会从 `current_gate = G1` 推进到 `current_gate = G2`，并把 G1 写入 completed。此时最好停下来确认：这个问题真的是你想写的吗？如果不是，就不要进入 G2。

## 5. G2 — Scope & Branch Control

G2 控制的是文章边界。很多文章的问题不是没有内容，而是什么都想写。在这一 Gate，需要把材料分成几类：哪些属于主线，哪些只是 supporting branch，哪些虽然有意思，但不应该进入这篇文章。

这篇教程在 G2 明确冻结了三块主线内容：使用前准备、Pre-G1 brainstorm、G1–G7 的真实执行过程。同时把更广的 Prompt Engineering、Agent 架构、CMS 和发布系统排除在外。这些内容并非不重要，只是如果全部加入，教程会从“怎样使用 DraftGate”滑向“AI 写作系统设计综述”。

G2 完成后，文章已经知道“要回答什么”和“哪些东西属于本文”，但还没有决定怎样讲，也可能还没有完整正文。

## 6. G3 — Argument Architecture + Draft Construction

G3 是这套系统里非常关键的一步，而且也是我们第一次 dogfood 后修改最多的一步。

第一部分是 Argument Architecture。Agent 会根据 G1 的主问题和 G2 的 scope，提出 1–3 个适合的 narrative mode，例如 question-driven、case-driven、frame-driven 或 hybrid。这个选择不能由 Agent 自动决定，用户必须明确批准。

这篇教程选择的是 question-driven 作为 primary driver，同时把这篇教程自己的生成过程作为 case-driven secondary device。也就是说，文章主要围绕“怎样把 AI 写作变成可控过程”这个问题推进，同时用真实 dogfood 过程不断落地。

接着，G3 需要建立 Explanatory Spine。它不是目录，而是整篇文章真正的推理链。本文的 spine 可以压缩成：一次性生成把多种写作职责同时交给模型，因此难以稳定控制；human-in-the-loop 需要把人的判断拆成连续阶段；DraftGate 再用 state 和 CI 把这些阶段变成可执行、可验证的流程。

第二部分是 Draft Construction。这个部分是在第一次 dogfood 后补进去的。第一次运行时，G3 虽然搭出了完整结构，但很多 section 只有一两句话。随后 G4–G7 都严格按照自己的职责工作，最后所有 Gate 都 PASS，文章却仍然只是一个“结构正确的 outline”。这暴露出一个很实际的问题：没有任何 Gate 明确负责把 skeleton 展开成完整 first draft。

现在 G3 明确承担这个责任。如果文章还是 seed、outline、section skeleton 或 placeholder-heavy draft，G3 不能 PASS。每个 major section 都必须有 substantive prose，真正完成这一节的职责。

这并不意味着 G3 要顺手完成所有后续工作。它可以写正文、解释和过渡，但不能把 G4 的可理解性 audit、G5 的证据压力测试、G6 的段落整理或 G7 的最终语言清理提前做掉。

我们现在正在进行的第二轮 dogfood，就是从 G3 重新进入，专门验证这个改动。第一轮留下的结构被保留，但原来过薄的 sections 被展开成完整教程正文。

## 7. G4 — Reader Accessibility

G4 不再决定文章“讲什么”，而是检查读者能不能跟上。比如，文章里出现 fork、state、CI、Gate、human-in-the-loop 这些词时，技术用户可能觉得很自然，但普通读者未必知道它们分别是什么意思。G4 要检查的是这种理解门槛。

在这篇教程的第一轮里，G4 就补过这些解释：fork 是把仓库复制到自己的 GitHub 账户；state 是记录当前 Gate、已完成 Gate 和文章 revision 的 JSON 文件；CI 是每次提交后自动执行的验证；Agent 指能够读写仓库并提交 Git 变更的 AI 工具。

G4 的判断标准不是“术语越少越好”，而是读者第一次遇到重要概念时，有没有足够的解释可以继续往下读。

## 8. G5 — Claim & Evidence Boundary

G5 负责的是判断强度和证据边界。它会问：文章里的结论有没有写得太绝对？有没有合理的替代解释？最强反驳是什么？哪些话需要加条件？

这篇教程第一轮就遇到过一个典型问题。原文一开始写的是“好文章仍然需要 human-in-the-loop”。这个判断太宽，因为简单、格式固定、低风险的写作任务，完全可能一次生成就够用。

G5 最后把它收紧成：“对于需要反复判断、修改和核查的复杂长文，human-in-the-loop 仍然很重要。”这种修改看起来只是加了几个限定词，但它改变的是 claim boundary，而不是语言风格。

## 9. G6 — Paragraph Organization

G6 只看段落职责。它不规定“一个段落应该多少字”，也不规定“一句话一段一定错误”。真正的标准是：一个段落是不是承担一个相对完整的 semantic / argumentative responsibility。

如果两段实际上只完成一个论证动作，就应该考虑合并；如果一个段落同时塞进了几个不同职责，就应该考虑拆分。第一轮里，我们发现“这是一篇教程”和“教程范围限定”原本分成两个相邻段落，但其实都在完成同一个 framing action，所以把它们合并了。

这一点很重要，因为 DraftGate 的公开 Core 不应该规定某个作者喜欢长段还是短段。段落审美属于 Custom Rules，而不是 Core。

## 10. G7 — Final Language & Pattern Audit

G7 是最后的语言和机械模式检查。到这里，主问题、scope、architecture、claim boundary、paragraph organization 都已经冻结，G7 不应该重新设计文章。

它主要检查重复的 meta-signposting、连续使用同一种句式、模板化 section opening、固定强结尾、机械平行以及其它 AI trace。第一轮里，G7 清理过连续出现的“这一部分……”“这里的……”“最后回看……”等说明性壳子，但没有重新改变结构。

G7 完成后，current_gate 变成 null，status 变成 complete。这意味着当前 cycle 结束，DraftGate 释放文章控制权。

## 11. 不满意怎么办：reopen 和新 cycle

DraftGate 并不假设一次 G1→G7 就一定得到永远不需要再改的文章。

第一种情况是当前 cycle 还没完成，你刚做完一个 Gate 就发现不满意。例如刚完成 G4，state 已经走到 G5，但你觉得 G4 的解释方式有问题。这时可以执行：

```bash
./writing reopen --article-id 20261005-example-topic
```

reopen 只能退回最近完成的一个 Gate。它不会自动修改文章，只是把 state 恢复到那个 Gate，然后你再和 Agent 重新讨论、重新执行。

第二种情况是 G1–G7 已经全部 complete，但你读完后仍然觉得文章需要系统性重做。这时启动新的 cycle：

```bash
./writing start-cycle --article-id 20261005-example-topic --from G3
```

原则是从最早受到影响的 Gate 开始：主问题变了从 G1，范围变了从 G2，结构或正文展开有问题从 G3，读者理解问题从 G4，证据问题从 G5，段落问题从 G6，只是语言问题从 G7。

这篇教程就是一个真实例子。第一轮 G1→G7 全部 PASS，但我们发现文章结构完整、正文却太薄。问题属于 architecture / draft development，所以没有从 G1 重来，而是开启 cycle 2，从 G3 进入。

多轮 cycle 不是失败，而是 DraftGate 的正常使用方式。每一轮都以当时的文章作为新 baseline，再从最早需要重做的位置往后检查。

## 12. 怎样形成自己的写作风格：Persistent Custom Rules

DraftGate Core 有意保持作者中立。它不会规定你必须使用第一人称还是第三人称，也不会规定段落必须多长、标题必须是什么格式，更不会内置某个作者自己的禁用词表。

但用户长期使用后一定会形成自己的偏好。例如你可以告诉 Agent：“以后 G6 尽量保留完整的长段落，不要为了视觉节奏频繁拆段。”如果你明确说这是长期规则，Agent 可以把它保存到对应 Gate 的 Custom Rules，例如 `.writing-rules/G6.md`。

普通用户不需要自己打开这些文件维护。你只需要在对话中说“这条以后保留”“把刚才那条长期规则删掉”，Agent 负责维护。

这里有一个严格边界：执行 Gx 时，只允许 Gx 的 Custom Rules 参与。G3 的个人偏好不能偷偷进入 G4，G6 的段落偏好也不能影响 G5 的证据判断。

而且 Core 的优先级高于 Custom Rules。如果个人规则和 Core 冲突，Core 生效，冲突的 Custom Rule 在本次执行中被忽略，Agent 应该明确告诉你发生了冲突，同时不能因为冲突本身去改变 workflow state。

这样 DraftGate 可以一边保持一个通用、可开源的核心，一边让每个用户通过长期使用逐渐形成自己的写作系统。

## 13. complete 以后仍然可以自由修改

当 state 已经是 `status = complete`，DraftGate 会释放文章。这时候你完全可以继续和 Agent 普通对话，例如要求某一段再短一点、补一个例子、换标题或者修改结尾。这些修改不需要 state，也不会自动变成 Custom Rules。

如果只是局部修改，直接改就可以。如果改着改着发现文章的结构或论证又发生了明显变化，再开一个新的 cycle，从最早受到影响的 Gate 重新进入。

## 14. 回看：DraftGate 实际控制了什么

完整流程可以概括为：准备 GitHub / Fork / Agent → Pre-G1 brainstorm → G1 主问题与 Thesis → G2 Scope → G3 Architecture + Draft Construction → G4 Reader Accessibility → G5 Claim & Evidence Boundary → G6 Paragraph Organization → G7 Final Language & Pattern Audit → complete。

如果当前 Gate 不满意，可以 reopen；如果整个 cycle 已经结束但还想系统修改，可以 start-cycle --from Gx；如果只是局部改动，complete 后直接编辑即可。与此同时，长期风格偏好可以逐步沉淀到对应 Gate 的 Custom Rules。

可以把这套系统分成三种角色：人负责关键判断，AI 负责讨论和编辑，Git/state/CI 负责记录和验证。DraftGate 的价值不在于替你自动写完一篇文章，而在于把 AI 辅助写作变成一个可以暂停、检查、重做和逐步改进的过程。

这篇教程本身也是这套方法的一次验证。第一轮我们成功走完 G1–G7，却发现“结构正确”并不等于“正文已经完成”；于是修改 G3，让它承担 Draft Construction，再从 G3 开启第二轮。这个过程本身说明了一件事：写作系统也需要在真实写作里被检验，而不是只看规则是否在纸面上完整。
