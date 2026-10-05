# Custom Rules E2E Test

这是一篇专门用于验证 DraftGate Persistent Custom Rules 行为的最小测试文章。

主问题：怎样验证某个长期 G3 偏好能够被持久化、只在 G3 生效，并且不能覆盖 Core contract？

核心判断：Custom Rules 应该影响当前 Gate 的允许范围内行为，但不能跨 Gate 泄漏，也不能改变 Core authority。
