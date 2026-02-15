---
name: warn-console-log
enabled: true
event: file
pattern: console\.log\(
action: warn
---

🔍 **检测到 Console.log**

您正在添加 console.log 语句。请考虑：
- 这是用于调试还是应该使用适当的日志记录？
- 这会发布到生产环境吗？
- 应该使用日志记录库吗？
