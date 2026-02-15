---
name: block-dangerous-rm
enabled: true
event: bash
pattern: rm\s+-rf
action: block
---

⚠️ **检测到危险的 rm 命令！**

此命令可能会删除重要文件。请：
- 验证路径是否正确
- 考虑使用更安全的方法
- 确保您有备份
