# Python 开发助手插件

Python 开发助手插件为 Claude Code 提供全面的 Python 开发支持，包括代码质量检查、项目脚手架生成、文档自动化和常用代码片段。

## 功能特性

### 🔍 代码质量检查
- 支持多种代码检查工具（ruff, black, pylint, flake8）
- 自动修复代码风格问题
- 保存前自动检查（可配置）

### 🚀 项目生成器
- **Django 项目**：支持基础版、API版、全栈版模板
- **Flask 项目**：支持基础版、REST API版、蓝图版模板
- 自动创建虚拟环境和安装依赖

### 📚 文档生成
- 自动生成 Python 文档（Sphinx）
- 支持 Google Style docstring
- 生成 HTML 格式文档

### 📝 代码片段
- 10+ 常用 Python 代码模板
- 交互式选择和插入
- 支持参数化替换

### 🤖 智能代码分析
- 自动分析代码质量
- 检查风格、复杂度、安全性、性能
- 提供详细改进建议

## 安装

### 前置要求

- Python 3.8+
- pip

### 推荐工具（可选）

```bash
pip install ruff black pylint flake8 sphinx
```

### 安装插件

```bash
# 从本地安装
cc plugin install ./python-dev-assistant

# 或从市场安装（如果已发布）
cc plugin install python-dev-assistant
```

## 使用指南

### 命令

#### `/py-check` - 代码风格检查

检查 Python 代码风格并提供修复建议。

```bash
# 使用默认工具（ruff）检查当前文件
/py-check

# 指定检查工具
/py-check --tool=black

# 自动修复问题
/py-check --fix

# 检查整个项目
/py-check --scope=project
```

#### `/py-django` - 创建 Django 项目

快速创建 Django 项目脚手架。

```bash
# 创建基础项目
/py-django myproject

# 创建 API 项目
/py-django myproject --template=api

# 创建全栈项目
/py-django myproject --template=fullstack
```

**模板说明：**
- `basic`: 基础 Django 项目（默认）
- `api`: Django REST Framework API 项目
- `fullstack`: 包含前端的全栈项目

#### `/py-flask` - 创建 Flask 项目

快速创建 Flask 项目脚手架。

```bash
# 创建基础项目
/py-flask myapp

# 创建 REST API 项目
/py-flask myapp --template=api

# 创建蓝图结构项目
/py-flask myapp --template=blueprint
```

**模板说明：**
- `basic`: 单文件 Flask 应用（默认）
- `api`: Flask REST API 项目
- `blueprint`: 使用蓝图的模块化项目

#### `/py-docs` - 生成文档

为 Python 代码生成文档。

```bash
# 为当前文件生成文档
/py-docs

# 为整个项目生成文档
/py-docs --scope=project

# 指定输出目录
/py-docs --output=docs/
```

#### `/py-snippet` - 插入代码片段

交互式选择并插入常用代码片段。

```bash
# 显示片段列表
/py-snippet

# 直接插入指定片段
/py-snippet --type=class
/py-snippet --type=decorator
/py-snippet --type=cli
```

**可用片段：**
- `class`: 类定义模板
- `dataclass`: 数据类模板
- `decorator`: 装饰器模板
- `context-manager`: 上下文管理器
- `cli`: 命令行工具模板
- `async-function`: 异步函数模板
- `test-case`: 单元测试模板
- `exception`: 自定义异常
- `property`: 属性装饰器
- `singleton`: 单例模式

### 技能

插件包含 3 个自动激活的技能：

1. **Python 最佳实践与代码风格指南** - 当你询问 Python 代码规范、PEP 8 等问题时自动激活
2. **Django/Flask 项目架构模式** - 当你询问项目结构、最佳实践时自动激活
3. **Python 文档编写规范** - 当你询问如何写 docstring、文档时自动激活

### 代理

**Python 代码质量分析器** - 自主分析代码质量并提供改进建议

当你说"分析这段代码"、"审查代码质量"时会自动触发。

### 钩子

**保存前代码检查** - 在保存 Python 文件前自动运行代码风格检查

- 仅对 `.py` 文件生效
- 使用 ruff 进行快速检查
- 显示警告但允许保存
- 可通过设置禁用

## 配置

创建 `.claude/python-dev-assistant.local.md` 文件来自定义配置：

```yaml
---
python_version: "3.11"
code_checker: "ruff"
auto_fix: false
doc_style: "google"
enable_hook: true
django_template: "basic"
flask_template: "basic"
---
```

### 配置项说明

- `python_version`: Python 版本（默认: "3.11"）
- `code_checker`: 代码检查工具，可选 ruff/black/pylint/flake8（默认: "ruff"）
- `auto_fix`: 是否自动修复代码风格问题（默认: false）
- `doc_style`: 文档风格，可选 google/numpy/sphinx（默认: "google"）
- `enable_hook`: 是否启用保存前检查钩子（默认: true）
- `django_template`: Django 默认模板（默认: "basic"）
- `flask_template`: Flask 默认模板（默认: "basic"）

## 依赖工具

插件会自动检查以下工具是否安装，并在需要时提供安装指南：

- **ruff**: 快速 Python 代码检查器（推荐）
- **black**: Python 代码格式化工具
- **pylint**: Python 代码静态分析工具
- **flake8**: Python 代码风格检查工具
- **sphinx**: Python 文档生成工具
- **django**: Django Web 框架
- **flask**: Flask Web 框架

### 安装推荐工具

```bash
# 安装所有推荐工具
pip install ruff black pylint flake8 sphinx django flask

# 或只安装必需工具
pip install ruff sphinx
```

## 示例工作流

### 1. 创建新的 Django 项目

```bash
# 创建 API 项目
/py-django blog-api --template=api

# Claude Code 会：
# - 创建项目目录结构
# - 创建虚拟环境
# - 安装 Django 和 DRF
# - 配置基础设置
# - 创建示例 API
```

### 2. 检查代码质量

```bash
# 检查当前文件
/py-check

# 自动修复问题
/py-check --fix
```

### 3. 生成文档

```bash
# 为项目生成文档
/py-docs --scope=project

# 文档将生成在 docs/ 目录
```

### 4. 使用代码片段

```bash
# 插入类定义模板
/py-snippet --type=class

# 插入测试用例模板
/py-snippet --type=test-case
```

## 故障排除

### 工具未找到

如果命令提示工具未安装，请运行：

```bash
pip install <tool-name>
```

### Hook 不工作

1. 检查配置文件中 `enable_hook` 是否为 `true`
2. 确保 ruff 已安装
3. 重启 Claude Code

### 项目生成失败

1. 确保 Python 3.8+ 已安装
2. 确保 pip 可用
3. 检查网络连接（需要下载依赖）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 更新日志

### 0.1.0 (2024-02-07)

- 初始版本
- 支持代码风格检查
- 支持 Django/Flask 项目生成
- 支持文档生成
- 支持代码片段
- 包含代码质量分析代理
- 包含保存前检查钩子
