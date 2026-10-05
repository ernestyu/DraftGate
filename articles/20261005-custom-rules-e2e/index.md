# Custom Rules E2E Test

主问题：怎样验证 G3 Custom Rule 能持久化、只在 G3 生效，并且不能覆盖 Core？

## 1. 持久化

已保存长期 G3 偏好到 `.writing-rules/G3.md`：在合适时优先使用 case-driven secondary device，同时保持 primary driver 明确。这里的 secondary device 是辅助整篇文章推进的叙事方式，它可以影响结构偏好，但不能取代 primary driver。

## 2. Human-in-the-loop 仍然生效

G3 给出了两个 narrative-mode candidates，用户明确选择了 `question-driven primary + case-driven secondary`。因此 Custom Rule 影响了候选和结构偏好，但没有替用户自动选择 narrative mode。

## 3. 本次 G3 architecture

Primary driver 是 question-driven；secondary device 是本次真实 E2E case；central frame 为 NOT NEEDED。

Explanatory Spine：Custom Rule 只有在实际影响对应 Gate 时才有意义，但这种影响必须局限在当前 Gate；Core 始终拥有更高 authority。这里的 Core 是 DraftGate 自带、所有用户共同遵守的 Gate contract；Custom Rule 只是用户额外添加的长期偏好，因此不能改变 workflow 的基本约束。

## 4. 后续验证

G3 完成后进入 G4。G4 应只使用 G4 Core 和 G4 Custom Rules，不应使用 G3 Custom Rule。之后再测试一条与 G3 Core 冲突的 Custom Rule，确认 Core 生效、冲突被告知、state 不因冲突本身改变。
