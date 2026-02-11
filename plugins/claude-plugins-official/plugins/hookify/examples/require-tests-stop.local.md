---
name: require-tests-run
enabled: false
event: stop
action: block
conditions:
  - field: transcript
    operator: not_contains
    pattern: npm test|pytest|cargo test
---

**未在对话记录中检测到测试！**

停止前，请运行测试以验证您的更改正常工作。

查找测试命令，例如：
- `npm test`
- `pytest`
- `cargo test`

**注意：** 如果对话记录中没有出现测试命令，此规则将阻止停止。
仅在您需要严格的测试执行时启用此规则。
