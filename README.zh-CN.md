# DraftGate

[English](README.md) | **简体中文**

[![Writing Workflow CI](https://github.com/ernestyu/DraftGate/actions/workflows/writing-workflow-ci.yml/badge.svg)](https://github.com/ernestyu/DraftGate/actions/workflows/writing-workflow-ci.yml)

一个基于 Git、按阶段执行的 AI 辅助长文编辑工作流。

DraftGate 把一篇 Markdown 文章变成一个有状态的 G1→G7 写作过程。语言模型负责判断与编辑，Git 记录文档版本，确定性的验证器负责检查 Gate 顺序、状态新鲜度和状态转移是否合法。

内置写作规则刻意保持语言中立。它关注论证、结构、证据边界、段落职责和机械化写作模式，而不是某一种作者风格。因此，同一套流程可以直接用于中文或英文写作。

## 设计原则

- **一次只执行一个 Gate。** 每一轮编辑只承担一种明确职责，完成后必须停止，不能顺手执行后面的 Gate。
- **人始终在流程中。** 讨论、判断和取舍属于正式流程的一部分，DraftGate 不把长文写作当成一次性生成任务。
- **把确定性验证移出模型。** Gate 顺序、状态新鲜度和合法状态转移由 Git 与验证器检查，而不是由 Agent 自己宣布“已经完成”。

## 为什么需要 DraftGate

复杂写作任务经常把主旨判断、范围控制、结构设计、证据边界、段落组织和最终语言清理一次性塞进一个大提示词。模型即使理解了所有要求，也很容易在一次执行中混淆职责、跳过步骤，或者在修改一个问题时破坏已经确定的部分。

DraftGate 把这些职责拆成窄而明确的 Gate，每个 Gate 只解决一类问题，并且有自己的允许范围和退出条件。

内置 Gate：

1. G1 — 主问题与 Thesis
2. G2 — 范围与支线控制
3. G3 — 论证结构与完整初稿展开
4. G4 — 读者可理解性
5. G5 — 判断与证据边界
6. G6 — 段落组织
7. G7 — 最终语言与机械模式检查

## 文件结构

```text
articles/
  20261005-example-topic/
    index.md

.writing-state/
  write-commentary/
    20261005-example-topic.json
```

DraftGate 不依赖 Hugo、CMS、front matter、封面图或任何发布系统。

## 环境要求

- Git
- Python 3.10+
- 可选：GitHub Actions，用于远端强制验证

不需要 Docker、数据库、模型服务器，也不需要 self-hosted runner。

## 快速开始

正常使用时，先在 GitHub 上 Fork 本仓库，把 Fork 后属于你自己的仓库链接交给能够读写 GitHub 的 ChatGPT 或其他 Agent。之后的文章、state、Custom Rules 和 CI 都发生在你的 Fork 中。

正式初始化 state 前，先做 **Pre-G1 brainstorm**。这一阶段只和 AI 发散讨论主题、动机、可能的问题和大致方向，没有 state，也没有 PASS / FAIL。等你已经大致知道为什么要写、想讨论什么，再进入 G1。


Clone 仓库后，先创建一篇文章：

```bash
./writing bootstrap --article-id 20261005-example-topic --title "暂定标题"
git add articles/20261005-example-topic/index.md
git commit -m "Bootstrap article"
```

初始化写作流程：

```bash
./writing init --article-id 20261005-example-topic
git add .writing-state/write-commentary/20261005-example-topic.json
git commit -m $'Initialize writing workflow\n\nWriting-Workflow: init\nWriting-Article: 20261005-example-topic'
```

之后让 AI Agent 每次只执行一个 Gate。

## 与 AI Agent 配合

能够读取仓库规则的 Agent 应先读取 `AGENTS.md`。如果 Agent 不会自动读取仓库说明，可以直接给它下面这段指令：

```text
Read AGENTS.md and docs/writing/commentary/workflow.md.
Work on article 20261005-example-topic.
Read its state file, load only the current gate and declared resources,
execute exactly that gate, update the article and state according to the workflow,
commit with the required Writing-* trailers, then stop.
```

每完成一个 Gate，再明确要求下一个：

```text
execute G1
execute G2
...
```

Agent 不应该预先执行后续 Gate。讨论、判断和取舍仍然是流程的一部分。DraftGate 是一个人机协作的编辑控制系统，不是一键生成文章的工具。

G3 还负责在需要时把 seed、outline 或 section skeleton 展开成可以连续阅读的完整初稿。只有标题和少量职责说明，不能因为结构正确就通过 G3。

## Persistent Custom Rules

DraftGate Core 保持语言和作者中立。用户长期形成的个人偏好放在第二层 Custom Rules 中：

```text
.writing-rules/G1.md
...
.writing-rules/G7.md
```

普通用户不需要手工编辑这些文件。只需要在和 Agent 的对话中明确说某条偏好要长期保留、修改或删除，Agent 负责维护对应 Gate 的规则。执行某个 Gate 时，只允许该 Gate 的 Custom Rules 参与；如果 Custom Rule 与 Core 冲突，以 Core 为准。

## 本地命令

```bash
./writing bootstrap --article-id <id> [--title "..."]
./writing init --article-id <id> [--from Gx]
./writing show --article-id <id>
./writing validate --article-id <id>
./writing advance --article-id <id>
./writing reopen --article-id <id>
./writing start-cycle --article-id <id> [--from Gx]
./writing reconcile --article-id <id>
./writing test
```

`advance` 会根据当前 working tree 中的文章更新 state。一个合法的 CHANGED Gate commit 必须同时包含文章修改和对应的 state transition。

如果当前 cycle 还没有完成，而你对刚完成的 Gate 不满意，可以在执行下一 Gate 前使用 `reopen`。G7 完成后，文章会释放为普通 Markdown，可以自由修改；如果希望再次系统检查，就从最早受影响的 Gate 开新 cycle，例如结构或正文展开不满意时使用 `start-cycle --from G3`。多轮 cycle 是正常用法。

Gate commit 使用类似下面的 trailers：

```text
Complete G1

Writing-Workflow: gate
Writing-Article: 20261005-example-topic
Writing-Gate: G1
```

## GitHub Actions

仓库内置的 workflow 使用 `ubuntu-latest`，检查：

- workflow registry 和声明的资源；
- 全部 writing unit tests；
- state 是否与当前文章版本一致；
- workflow-controlled commit 和 trailers 是否合法。

GitHub Actions 不是运行 DraftGate 的必要条件。本地也可以执行同样的验证：

```bash
./writing test
```

## 核心约束

- 一次 invocation 只执行一个 Gate；
- 从选定的 entry gate 开始后，不允许跳 Gate；
- in-progress state 过期时 fail closed；
- 完成一个 Gate 时只能前进一个 Gate；
- 有实质修改时，文章与 state 必须一起提交；
- NO_CHANGE 必须由对应 Gate 明确允许；
- reopen 只能恢复到紧邻的前一个 Gate；
- 已完成的 cycle 不会自动重新开始。

## 公开版规则的边界

公开版只保留能够跨语言、跨作者迁移的写作主干。它不会规定某种个人文风，也不包含语言特定的禁用词、固定段落长度、第一人称限制或特定句式黑名单。

这些内容如果有需要，应由使用者在自己的项目中扩展，而不是写进 DraftGate 的通用核心。

## License

MIT.
