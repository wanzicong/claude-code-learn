---
name: warn-sensitive-files
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$|\.env\.|credentials|secrets
---

🔐 **检测到敏感文件**

您正在编辑可能包含敏感数据的文件：
- 确保凭据未硬编码
- 对密钥使用环境变量
- 验证此文件在 .gitignore 中
- 考虑使用密钥管理器
