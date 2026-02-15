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

**在记录中未检测到测试！**

在停止之前，请运行测试以验证您的更改是否正常工作。

查找测试命令，如：
- `npm test`
- `pytest`
- `cargo test`

**注意：** 如果记录中没有出现测试命令，此规则会阻止停止。
仅在需要严格的测试执行时启用此规则。
