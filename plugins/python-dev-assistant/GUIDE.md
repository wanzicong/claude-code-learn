# Python 开发助手插件 - 使用指南

## 🎯 插件目的

为 Python 开发者提供全方位的开发支持，包括代码质量检查、项目生成、文档生成和代码片段管理。

## 📋 功能清单

### 1. 代码质量检查
- **命令**: `/py-check`
- **代理**: `python-code-analyzer`
- **技能**: `python-best-practices`
- **Hook**: 保存时自动检查

### 2. 项目生成
- **命令**: `/py-django`, `/py-flask`
- **技能**: `django-flask-architecture`

### 3. 文档生成
- **命令**: `/py-docs`
- **技能**: `python-documentation`

### 4. 代码片段
- **命令**: `/py-snippet`

## 🚀 快速开始

### 第一次使用

1. **安装推荐工具**：
   ```bash
   pip install ruff black pylint sphinx
   ```

2. **创建配置文件**（可选）：
   ```bash
   mkdir -p .claude
   cp python-dev-assistant.local.md .claude/
   ```

3. **测试插件**：
   ```bash
   /py-check
   ```

### 典型工作流

#### 创建新项目
```bash
# 1. 创建项目
/py-django myproject --template=api

# 2. 进入项目
cd myproject
source venv/bin/activate

# 3. 开始开发
# 编写代码...

# 4. 检查代码
/py-check --fix

# 5. 生成文档
/py-docs --scope=project
```

#### 代码审查
```bash
# 1. 快速检查
/py-check

# 2. 深度分析
"帮我分析一下这段代码的质量"

# 3. 根据建议改进代码
```

## 💡 使用技巧

### 1. 自动化代码检查
启用 Hook 后，每次保存 Python 文件都会自动检查代码风格。

### 2. 自定义配置
创建 `.claude/python-dev-assistant.local.md` 自定义默认行为：
```yaml
---
code_checker: "ruff"
auto_fix: true
enable_hook: true
---
```

### 3. 学习最佳实践
遇到 Python 问题时，直接询问：
- "Python 代码规范是什么？"
- "Django 项目结构怎么组织？"
- "如何写好的 docstring？"

### 4. 快速插入代码
使用 `/py-snippet` 快速插入常用代码模板：
```bash
/py-snippet --type=class
/py-snippet --type=decorator
/py-snippet --type=test-case
```

## 🔧 配置说明

### 配置文件位置
`.claude/python-dev-assistant.local.md`

### 可配置项
```yaml
---
# Python 版本
python_version: "3.11"

# 代码检查工具（ruff/black/pylint/flake8）
code_checker: "ruff"

# 是否自动修复
auto_fix: false

# 文档风格（google/numpy/sphinx）
doc_style: "google"

# 是否启用保存前检查
enable_hook: true

# Django 默认模板（basic/api/fullstack）
django_template: "basic"

# Flask 默认模板（basic/api/blueprint）
flask_template: "basic"
---
```

## 📚 命令参考

### /py-check
检查 Python 代码风格和质量。

**参数**：
- `--tool=<tool>`: 指定检查工具（ruff/black/pylint/flake8）
- `--fix`: 自动修复问题
- `--scope=<scope>`: 检查范围（file/dir/project）

**示例**：
```bash
/py-check
/py-check --tool=black --fix
/py-check --scope=project
```

### /py-django
创建 Django 项目脚手架。

**参数**：
- `<project_name>`: 项目名称（必需）
- `--template=<template>`: 项目模板（basic/api/fullstack）

**示例**：
```bash
/py-django myproject
/py-django blog-api --template=api
```

### /py-flask
创建 Flask 项目脚手架。

**参数**：
- `<project_name>`: 项目名称（必需）
- `--template=<template>`: 项目模板（basic/api/blueprint）

**示例**：
```bash
/py-flask myapp
/py-flask api-server --template=api
```

### /py-docs
生成 Python 文档。

**参数**：
- `--scope=<scope>`: 文档范围（file/module/project）
- `--tool=<tool>`: 文档工具（sphinx/pdoc）
- `--output=<dir>`: 输出目录

**示例**：
```bash
/py-docs
/py-docs --scope=project --tool=sphinx
/py-docs --output=documentation/
```

### /py-snippet
插入 Python 代码片段。

**参数**：
- `--type=<type>`: 片段类型

**可用类型**：
- `class`: 类定义
- `dataclass`: 数据类
- `decorator`: 装饰器
- `context-manager`: 上下文管理器
- `cli`: 命令行工具
- `async-function`: 异步函数
- `test-case`: 单元测试
- `exception`: 自定义异常
- `property`: 属性装饰器
- `singleton`: 单例模式
- `factory`: 工厂模式
- `api-endpoint`: API 端点

**示例**：
```bash
/py-snippet
/py-snippet --type=class
/py-snippet --type=test-case
```

## 🤖 代理使用

### python-code-analyzer
全面分析 Python 代码质量。

**触发方式**：
- "帮我分析一下这段代码的质量"
- "审查这个 Python 文件"
- "检查代码有没有问题"

**分析维度**：
- 代码风格（PEP 8）
- 复杂度（圈复杂度）
- 安全性（SQL 注入、XSS 等）
- 性能（循环优化、内存使用）
- 文档（docstring 完整性）

**输出格式**：
- 总体评分（0-10 分）
- 关键问题列表（Critical/Warning/Info）
- 代码指标统计
- 改进建议
- 优秀实践

## 🎓 技能使用

### python-best-practices
Python 最佳实践与代码风格指南。

**触发词**：
- "Python 代码规范"
- "PEP 8"
- "代码风格"
- "black/ruff/pylint"

**内容**：
- PEP 8 规范
- 命名约定
- 代码组织
- 工具使用（ruff/black/pylint/flake8）
- 最佳实践

### django-flask-architecture
Django/Flask 项目架构模式。

**触发词**：
- "Django 项目结构"
- "Flask 架构"
- "最佳实践"
- "Django REST Framework"

**内容**：
- 项目结构
- 应用组织
- 配置管理
- 模型设计
- API 设计

### python-documentation
Python 文档编写规范。

**触发词**：
- "docstring"
- "文档字符串"
- "Google Style"
- "Sphinx"

**内容**：
- 文档风格（Google/NumPy/Sphinx）
- 文档生成工具
- 最佳实践
- 模板示例

## 🪝 Hook 说明

### PreToolUse Hook
在保存 Python 文件前自动检查代码风格。

**触发条件**：
- Write 或 Edit Python 文件（.py 扩展名）
- `enable_hook` 配置为 true（默认）

**行为**：
- 使用 ruff 快速检查代码
- 显示警告但允许保存
- 不会阻止文件保存

**禁用方法**：
在配置文件中设置：
```yaml
enable_hook: false
```

## 🐛 故障排除

### 工具未安装
**问题**：命令提示工具未安装

**解决**：
```bash
pip install ruff black pylint flake8 sphinx
```

### Hook 不工作
**问题**：保存文件时没有代码检查

**解决**：
1. 检查配置：`enable_hook: true`
2. 确保 ruff 已安装
3. 重启 Claude Code

### 命令执行失败
**问题**：命令返回错误

**解决**：
1. 检查命令参数是否正确
2. 查看错误信息
3. 参考命令文档

## 📞 获取帮助

- 查看 README.md 了解详细信息
- 查看 PLUGIN_REPORT.md 了解创建过程
- 使用 `/help` 查看 Claude Code 帮助
- 在 GitHub 提交 Issue

## 🎉 开始使用

现在你已经了解了插件的所有功能，开始使用吧！

```bash
# 创建你的第一个项目
/py-django my-first-project --template=api

# 或者检查现有代码
/py-check --fix

# 或者学习 Python 最佳实践
"Python 代码规范是什么？"
```

祝你开发愉快！🚀
