---
python_version: "3.11"
code_checker: "ruff"
auto_fix: false
doc_style: "google"
enable_hook: true
django_template: "basic"
flask_template: "basic"
---

# Python 开发助手配置

这是 Python 开发助手插件的配置文件示例。

## 配置项说明

- **python_version**: 目标 Python 版本
- **code_checker**: 代码检查工具（ruff/black/pylint/flake8）
- **auto_fix**: 是否自动修复代码风格问题
- **doc_style**: 文档风格（google/numpy/sphinx）
- **enable_hook**: 是否启用保存前检查钩子
- **django_template**: Django 项目默认模板（basic/api/fullstack）
- **flask_template**: Flask 项目默认模板（basic/api/blueprint）

## 使用方法

将此文件复制到项目的 `.claude/` 目录：

```bash
cp python-dev-assistant.local.md .claude/
```

然后根据需要修改配置值。
