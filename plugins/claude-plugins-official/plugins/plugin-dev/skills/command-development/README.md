# 命令开发技能

关于创建 Claude Code 斜杠命令的全面指南，包括文件格式、frontmatter 选项、动态参数和最佳实践。

## 概述

此技能提供以下知识：
- 斜杠命令文件格式和结构
- YAML frontmatter 配置字段
- 动态参数（$ARGUMENTS、$1、$2 等）
- 使用 @ 语法的文件引用
- 使用 !` 语法的 Bash 执行
- 命令组织和命名空间
- 命令开发最佳实践
- 插件特定功能（${CLAUDE_PLUGIN_ROOT}、插件模式）
- 与插件组件的集成（agents、skills、hooks）
- 验证模式和错误处理

## 技能结构

### SKILL.md（约 2,470 字）

核心技能内容涵盖：

**基础知识：**
- 命令基础和位置
- 文件格式（带有可选 frontmatter 的 Markdown）
- YAML frontmatter 字段概述
- 动态参数（$ARGUMENTS 和位置参数）
- 文件引用（@ 语法）
- Bash 执行（!` 语法）
- 命令组织模式
- 最佳实践和常见模式
- 故障排除

**插件特定：**
- ${CLAUDE_PLUGIN_ROOT} 环境变量
- 插件命令发现和组织
- 插件命令模式（配置、模板、多脚本）
- 与插件组件的集成（agents、skills、hooks）
- 验证模式（参数、文件、资源、错误处理）

### 参考资料

详细文档：

- **frontmatter-reference.md**：完整的 YAML frontmatter 字段规范
  - 所有字段描述及类型和默认值
  - 何时使用每个字段
  - 示例和最佳实践
  - 验证和常见错误

- **plugin-features-reference.md**：插件特定命令功能
  - 插件命令发现和组织
  - ${CLAUDE_PLUGIN_ROOT} 环境变量使用
  - 插件命令模式（配置、模板、多脚本）
  - 与插件 agents、skills 和 hooks 的集成
  - 验证模式和错误处理

### 示例

实用的命令示例：

- **simple-commands.md**：10 个完整命令示例
  - 代码审查命令
  - 测试命令
  - 部署命令
  - 文档生成器
  - Git 集成命令
  - 分析和研究命令

- **plugin-commands.md**：10 个插件特定命令示例
  - 带有脚本的简单插件命令
  - 多脚本工作流
  - 基于模板的生成
  - 配置驱动的部署
  - Agent 和 skill 集成
  - 多组件工作流
  - 验证输入的命令
  - 环境感知的命令

## 技能触发时机

当用户执行以下操作时，Claude Code 会激活此技能：
- 要求"创建斜杠命令"或"添加命令"
- 需要"编写自定义命令"
- 想要"定义命令参数"
- 询问"命令 frontmatter"或 YAML 配置
- 需要"组织命令"或使用命名空间
- 想要创建带有文件引用的命令
- 询问"命令中的 bash 执行"
- 需要命令开发最佳实践

## 渐进式披露

该技能使用渐进式披露：

1. **SKILL.md**（约 2,470 字）：核心概念、常见模式和插件功能概述
2. **参考资料**（总计约 13,500 字）：详细规范
   - frontmatter-reference.md（约 1,200 字）
   - plugin-features-reference.md（约 1,800 字）
   - interactive-commands.md（约 2,500 字）
   - advanced-workflows.md（约 1,700 字）
   - testing-strategies.md（约 2,200 字）
   - documentation-patterns.md（约 2,000 字）
   - marketplace-considerations.md（约 2,200 字）
3. **示例**（总计约 6,000 字）：完整可运行的命令示例
   - simple-commands.md
   - plugin-commands.md

Claude 根据任务需要加载参考资料和示例。

## 命令基础快速参考

### 文件格式

```markdown
---
description: 简要描述
argument-hint: [arg1] [arg2]
allowed-tools: Read, Bash(git:*)
---

命令提示内容，包含：
- 参数：$1、$2 或 $ARGUMENTS
- 文件：@path/to/file
- Bash：!`command here`
```

### 位置

- **项目**：`.claude/commands/`（与团队共享）
- **个人**：`~/.claude/commands/`（您的命令）
- **插件**：`plugin-name/commands/`（插件特定）

### 关键功能

**动态参数：**
- `$ARGUMENTS` - 所有参数作为单个字符串
- `$1`、`$2`、`$3` - 位置参数

**文件引用：**
- `@path/to/file` - 包含文件内容

**Bash 执行：**
- `!`command`` - 执行并包含输出

## Frontmatter 字段快速参考

| 字段 | 用途 | 示例 |
|-------|---------|---------|
| `description` | /help 中的简短描述 | `"Review code for issues"` |
| `allowed-tools` | 限制工具访问 | `ARead, Bash(git:*)` |
| `model` | 指定模型 | `sonnet`、`opus`、`haiku` |
| `argument-hint` | 记录参数 | `[pr-number] [priority]` |
| `disable-model-invocation` | 仅手动命令 | `true` |

## 常见模式

### 简单审查命令

```markdown
---
description: Review code for issues
---

Review this code for quality and potential bugs.
```

### 带有参数的命令

```markdown
---
description: Deploy to environment
argument-hint: [environment] [version]
---

Deploy to $1 environment using version $2
```

### 带有文件引用的命令

```markdown
---
description: Document file
argument-hint: [file-path]
---

Generate documentation for @$1
```

### 带有 Bash 执行的命令

```markdown
---
description: Show Git status
allowed-tools: Bash(git:*)
---

Current status: !`git status`
Recent commits: !`git log --oneline -5`
```

## 开发工作流

1. **设计命令：**
   - 定义目的和范围
   - 确定所需参数
   - 识别所需工具

2. **创建文件：**
   - 选择适当的位置
   - 创建带有命令名称的 `.md` 文件
   - 编写基本提示

3. **添加 frontmatter：**
   - 从最小开始（仅 description）
   - 根据需要添加字段（allowed-tools 等）
   - 使用 argument-hint 记录参数

4. **测试命令：**
   - 使用 `/command-name` 调用
   - 验证参数工作
   - 检查 bash 执行
   - 测试文件引用

5. **优化：**
   - 改进提示清晰度
   - 处理边缘情况
   - 在注释中添加示例
   - 记录要求

## 最佳实践摘要

1. **单一职责**：一个命令，一个明确的目的
2. **清晰描述**：在 `/help` 中可被发现
3. **记录参数**：始终使用 argument-hint
4. **最小工具**：使用最严格的 allowed-tools
5. **彻底测试**：验证所有功能工作
6. **添加注释**：解释复杂逻辑
7. **处理错误**：考虑缺失的参数/文件

## 状态

**完成的增强：**
- ✓ 插件命令模式（${CLAUDE_PLUGIN_ROOT}、发现、组织）
- ✓ 集成模式（agents、skills、hooks 协调）
- ✓ 验证模式（输入、文件、资源验证、错误处理）

**剩余的增强（进行中）：**
- 高级工作流（多步命令序列）
- 测试策略（如何有效测试命令）
- 文档模式（命令文档最佳实践）
- 市场考虑（发布和分发）

## 维护

要更新此技能：
1. 保持 SKILL.md 专注于核心基础知识
2. 将详细规范移至 references/
3. 为不同用例添加新的 examples/
4. 添加新字段时更新 frontmatter
5. 确保全程使用命令式/不定式形式
6. 测试示例与当前 Claude Code 兼容

## 版本历史

**v0.1.0** (2025-01-15):
- 包含基本命令基础的初始版本
- Frontmatter 字段参考
- 10 个简单命令示例
- 准备添加插件特定模式
