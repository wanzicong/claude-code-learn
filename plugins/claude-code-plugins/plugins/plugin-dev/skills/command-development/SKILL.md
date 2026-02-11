---
name: 命令开发
description: 当用户要求"创建斜杠命令"、"添加命令"、"编写自定义命令"、"定义命令参数"、"组织命令"、或需要关于 Claude Code 插件的命令结构、YAML frontmatter、动态参数、命令开发最佳实践指导时，应使用此技能。
version: 0.1.0
---

# Claude Code 命令开发

## 概述

此技能提供关于以下内容的知识：

- 斜杠命令文件格式和结构
- 用于配置的 YAML frontmatter
- 动态参数（$ARGUMENTS、$1、$2 等）
- 使用 @ 语法的文件引用
- 使用 !` 语法的 Bash 执行
- 命令组织和命名空间
- 命令开发最佳实践
- 插件特定功能（${CLAUDE_PLUGIN_ROOT}、插件模式）
- 与插件组件的集成（代理、技能、钩子）
- 验证模式和错误处理

## 技能结构

### SKILL.md（约 2,470 字）

核心技能内容涵盖：

**基础知识：**

- 斜杠命令基础和位置
- 文件格式（带有可选 frontmatter 的 Markdown）
- YAML frontmatter 字段概述
- 动态参数（$ARGUMENTS 和位置参数）
- 文件引用（@ 语法）
- Bash 执行（!` 语法）
- 命令组织和命名空间
- 最佳实践和常见模式
- 故障排除

**插件特定：**

- ${CLAUDE_PLUGIN_ROOT} 环境变量
- 插件命令发现和组织
- 插件命令模式（配置、模板、多脚本）
- 与插件组件的集成（代理、技能、钩子）
- 验证模式和错误处理

### 参考资料

详细文档：

- **frontmatter-reference.md**（约 1,200 字）：
  - 包含类型和默认值的所有字段描述
  - 何时使用每个字段
  - 示例和最佳实践
  - 验证和常见错误

- **plugin-features-reference.md**（约 1,800 字）：
  - 插件命令发现和组织
  - ${CLAUDE_PLUGIN_ROOT} 环境变量使用
  - 插件命令模式（配置、模板、多脚本）
  - 与插件代理、技能和钩子的集成
  - 验证模式和错误处理

- **interactive-commands.md**（约 2,500 字）：
  - 交互式命令模式
  - 使用 AskUserQuestion 工具
  - 使用交互式参数文档

- **advanced-workflows.md**（约 1,700 字）：
  - 高级工作流模式

- **testing-strategies.md**（约 2,200 字）：
  - 测试策略

- **documentation-patterns.md**（约 2,000 字）：
  - 文档模式

- **marketplace-considerations.md**（约 2,200 字）：
  - 市场发布考虑事项

### 示例

实用的命令示例：

- **simple-commands.md**（10 个完整命令示例）
  - 代码审查命令
  - 测试命令
  - 部署命令
  - 文档生成器
  - Git 集成命令
  - 分析和研究命令

- **plugin-commands.md**（10 个插件特定命令示例）
  - 带脚本的简单插件命令
  - 多脚本工作流
  - 基于模板的生成
  - 配置驱动的部署
  - 代理和技能集成
  - 多组件工作流
  - 验证输入命令
  - 环境感知命令

## 此技能何时触发

Claude Code 在用户以下情况时激活此技能：

- 请求"创建斜杠命令"或"添加命令"
- 需要"编写自定义命令"
- 想要"定义命令参数"
- 询问"命令 frontmatter"或 YAML 配置
- 需要"组织命令"或使用命名空间
- 想要创建带文件引用的命令"
- 询问"命令中的 bash 执行"
- 需要命令开发最佳实践

## 渐进式披露

该技能使用渐进式披露：

1. **Metadata**（始终加载）：具有强触发器的简明描述
2. **Core SKILL.md**（触发时加载）：基本 API 参考（~1,500-2,000 字）
3. **References/Examples**（按需加载）：详细指南、模式和工作代码

Claude 根据任务按需加载参考资料和示例。

## 命令基础快速参考

### 文件格式

```markdown
---
description: 简要描述
argument-hint: [arg1] [arg2]
allowed-tools: Read, Bash(git:*)
---
```
命令提示内容包含：

- 参数：$1、$2 或 $ARGUMENTS
- 文件：@path/to/file
- Bash：!`command here`

```

### 位置

- **项目**：`.claude/commands/`（与团队共享）
  - 范围：在特定项目中可用
  - 范围：在 `/help` 中显示为"(project)"
  - 用途：团队工作流、项目特定任务
  - 命名：在 `/help` 中显示为"(project)"

- **个人**：`~/.claude/commands/`（到处可用）
  - 范围：在 `/help` 中显示为"(user)"
  - 用途：个人工作流、跨项目工具
  - 范名：在 `/help` 中显示为"(user)"

- **插件**：`plugin-name/commands/`（插件特定）
  - 范围：插件安装时可用
  - 范围：在 `/help` 中显示为"(plugin-name)"
  - 用途：插件特定功能

### 关键功能

**动态参数：**

- `$ARGUMENTS` - 所有参数作为单个字符串
- `$1`、`$2`、`$3` - 位置参数

**文件引用：**

- `@path/to/file` - 包含文件内容
- `@path/to/file` - 包含文件内容

**Bash 执行：**

```
- `!`command`` - 执行并包含输出

### 前置元数据字段快速参考

| 字段 | 必需的 | 示例 |
|-------|----------|---------|---------|
| `description` | /help 中显示的简要描述 | `"审查代码问题"` |
| `allowed-tools` | 限制工具访问 | `Read, Bash(git:*)` |
| `model` | 指定模型 | `sonnet`、`opus`、`haiku` |
| `argument-hint` | 文档化参数 | `[pr-number] [priority] [assignee]` |
| `disable-model-invocation` | 仅手动命令 | `true` |
| `argument-hint` | 文档化参数 | `[pr-number] [priority] [assignee]` |
