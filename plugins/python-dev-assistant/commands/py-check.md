---
name: py-check
description: 检查 Python 代码风格和质量
argument-hint: "[--tool=ruff|black|pylint|flake8] [--fix] [--scope=file|dir|project]"
allowed-tools: ["Read", "Bash", "Grep", "Glob"]
---

# Python 代码风格检查命令

检查 Python 代码风格并提供修复建议。支持多种检查工具和自动修复。

## 使用方法

```bash
# 使用默认工具（ruff）检查当前文件
/py-check

# 指定检查工具
/py-check --tool=black
/py-check --tool=pylint
/py-check --tool=flake8

# 自动修复问题
/py-check --fix

# 检查整个目录
/py-check --scope=dir

# 检查整个项目
/py-check --scope=project
```

## 执行流程

1. **解析参数**：
   - 提取 `--tool` 参数（默认：ruff）
   - 提取 `--fix` 标志（默认：false）
   - 提取 `--scope` 参数（默认：file）

2. **读取配置**：
   - 检查 `.claude/python-dev-assistant.local.md` 配置文件
   - 如果存在，读取 `code_checker` 和 `auto_fix` 配置
   - 命令行参数优先于配置文件

3. **确定检查范围**：
   - `file`: 检查当前打开的文件或用户指定的文件
   - `dir`: 检查当前目录下的所有 Python 文件
   - `project`: 检查整个项目的所有 Python 文件

4. **检查工具是否安装**：
   - 运行 `which <tool>` 或 `<tool> --version` 检查工具是否可用
   - 如果工具未安装，提供安装指南

5. **执行代码检查**：
   - 根据选择的工具运行相应命令
   - 捕获输出和错误信息

6. **显示结果**：
   - 格式化输出检查结果
   - 如果有问题，显示问题列表和位置
   - 如果使用 `--fix`，显示修复的问题数量

## 工具命令映射

### Ruff
```bash
# 检查
ruff check <path>

# 自动修复
ruff check --fix <path>

# 格式化
ruff format <path>
```

### Black
```bash
# 检查
black --check <path>

# 格式化
black <path>
```

### Pylint
```bash
# 检查
pylint <path>

# 生成报告
pylint --output-format=json <path>
```

### Flake8
```bash
# 检查
flake8 <path>

# 指定配置
flake8 --config=.flake8 <path>
```

## 输出格式

### 成功（无问题）
```
✓ 代码检查通过！
  工具: ruff
  检查文件: 5 个
  问题数: 0
```

### 发现问题
```
✗ 发现 3 个问题：

file.py:10:5: E501 line too long (88 > 79 characters)
file.py:15:1: W293 blank line contains whitespace
file.py:20:10: F401 'os' imported but unused

建议：运行 /py-check --fix 自动修复这些问题
```

### 自动修复后
```
✓ 已修复 2 个问题

修复的问题：
  - E501: 1 处
  - W293: 1 处

仍需手动处理：
  - F401: 1 处（未使用的导入）

建议：检查并删除未使用的导入
```

## 错误处理

### 工具未安装
```
✗ 错误：ruff 未安装

安装方法：
  pip install ruff

或使用其他工具：
  /py-check --tool=black
  /py-check --tool=pylint
```

### 无 Python 文件
```
✗ 错误：当前目录没有 Python 文件

请确保：
  1. 当前目录包含 .py 文件
  2. 或使用 --scope=project 检查整个项目
```

## 配置文件支持

读取 `.claude/python-dev-assistant.local.md` 中的配置：

```yaml
---
code_checker: "ruff"
auto_fix: false
---
```

命令行参数会覆盖配置文件设置。

## 实现提示

使用 Bash 工具执行检查命令：

```python
# 伪代码示例
tool = args.get('tool', config.get('code_checker', 'ruff'))
fix = args.get('fix', config.get('auto_fix', False))
scope = args.get('scope', 'file')

# 确定检查路径
if scope == 'file':
    path = current_file
elif scope == 'dir':
    path = current_directory
else:
    path = project_root

# 检查工具是否安装
check_tool_installed(tool)

# 构建命令
if tool == 'ruff':
    cmd = f"ruff check {'--fix' if fix else ''} {path}"
elif tool == 'black':
    cmd = f"black {'--check' if not fix else ''} {path}"
# ... 其他工具

# 执行命令
result = bash(cmd)

# 格式化输出
format_output(result)
```

## 提示和技巧

1. **首次使用**：建议先不使用 `--fix`，查看会修复什么
2. **大型项目**：使用 `--scope=dir` 逐目录检查，避免一次性输出过多
3. **CI/CD 集成**：在提交前运行 `/py-check --scope=project` 确保代码质量
4. **配置优先级**：命令行参数 > 配置文件 > 默认值

## 相关命令

- `/py-docs` - 生成文档
- `/py-snippet` - 插入代码片段
