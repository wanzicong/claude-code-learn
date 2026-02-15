# 命令 Frontmatter 参考

斜杠命令中 YAML frontmatter 字段的完整参考。

## Frontmatter 概述

YAML frontmatter 是命令文件开头的可选元数据:

```markdown
---
description: Brief description
allowed-tools: Read, Write
model: sonnet
argument-hint: [arg1] [arg2]
---

Command prompt content here...
```

所有字段都是可选的。命令可以在没有任何 frontmatter 的情况下工作。

## 字段规范

### description

**类型:** 字符串
**必需:** 否
**默认值:** 命令提示符的第一行
**最大长度:** 建议约60个字符以便在 `/help` 中显示

**目的:** 描述命令的功能，显示在 `/help` 输出中

**Examples:**
```yaml
description: Review code for security issues
```
```yaml
description: Deploy to staging environment
```
```yaml
description: Generate API documentation
```

**最佳实践:**
- 保持在60个字符以下以便清晰显示
- 以动词开头（审查、部署、生成）
- 明确说明命令的功能
- 避免冗余的 "command" 或 "slash command"

**良好示例:**
- ✅ "审查 PR 的代码质量和安全性"
- ✅ "将应用程序部署到指定环境"
- ✅ "生成全面的 API 文档"

**不好的示例:**
- ❌ "此命令审查 PR"（不必要的 "此命令"）
- ❌ "审查"（太模糊）
- ❌ "一个用于审查拉取请求的代码质量、安全问题和最佳实践的命令"（太长）

### allowed-tools

**类型:** 字符串或字符串数组
**必需:** 否
**默认值:** 从对话权限继承

**目的:** 限制或指定命令可以使用哪些工具

**格式:**

**单个工具:**
```yaml
allowed-tools: Read
```

**多个工具（逗号分隔）:**
```yaml
allowed-tools: Read, Write, Edit
```

**多个工具（数组）:**
```yaml
allowed-tools:
  - Read
  - Write
  - Bash(git:*)
```

**工具模式:**

**特定工具:**
```yaml
allowed-tools: Read, Grep, Edit
```

**带命令过滤器的 Bash:**
```yaml
allowed-tools: Bash(git:*)           # 仅 git 命令
allowed-tools: Bash(npm:*)           # 仅 npm 命令
allowed-tools: Bash(docker:*)        # 仅 docker 命令
```

**所有工具（不推荐）:**
```yaml
allowed-tools: "*"
```

**何时使用:**

1. **安全性:** 将命令限制为安全操作
   ```yaml
   allowed-tools: Read, Grep  # 只读命令
   ```

2. **清晰度:** 记录所需工具
   ```yaml
   allowed-tools: Bash(git:*), Read
   ```

3. **Bash 执行:** 启用 bash 命令输出
   ```yaml
   allowed-tools: Bash(git status:*), Bash(git diff:*)
   ```

**最佳实践:**
- 尽可能限制性强
- 对 Bash 使用命令过滤器（例如，`git:*` 而不是 `*`）
- 仅在与对话权限不同时指定
- 记录为什么需要特定工具

### model

**类型:** 字符串
**必需:** 否
**默认值:** 从对话继承
**值:** `sonnet`、`opus`、`haiku`

**目的:** 指定哪个 Claude 模型执行命令

**示例:**
```yaml
model: haiku    # 快速，适用于简单任务
```
```yaml
model: sonnet   # 平衡性能（默认）
```
```yaml
model: opus     # 复杂任务的最大能力
```

**何时使用:**

**使用 `haiku` 用于:**
- 简单、公式化的命令
- 需要快速执行
- 低复杂度任务
- 频繁调用

```yaml
---
description: Format code file
model: haiku
---
```

**使用 `sonnet` 用于:**
- 标准命令（默认）
- 平衡速度/质量
- 最常见的用例

```yaml
---
description: Review code changes
model: sonnet
---
```

**使用 `opus` 用于:**
- 复杂分析
- 架构决策
- 深入代码理解
- 关键任务

```yaml
---
description: Analyze system architecture
model: opus
---
```

**最佳实践:**
- 除非有特定需要否则省略
- 在可能的情况下使用 `haiku` 以获得速度
- 为真正复杂的任务保留 `opus`
- 测试不同模型以找到正确的平衡

### argument-hint

**类型:** 字符串
**必需:** 否
**默认值:** 无

**目的:** 为用户和自动完成记录预期参数

**格式:**
```yaml
argument-hint: [arg1] [arg2] [optional-arg]
```

**示例:**

**单个参数:**
```yaml
argument-hint: [pr-number]
```

**多个必需参数:**
```yaml
argument-hint: [environment] [version]
```

**可选参数:**
```yaml
argument-hint: [file-path] [options]
```

**描述性名称:**
```yaml
argument-hint: [source-branch] [target-branch] [commit-message]
```

**最佳实践:**
- 对每个参数使用方括号 `[]`
- 使用描述性名称（不是 `arg1`、`arg2`）
- 在描述中指示可选与必需
- 匹配命令中位置参数的顺序
- 保持简洁但清晰

**按模式的示例:**

**简单命令:**
```yaml
---
description: Fix issue by number
argument-hint: [issue-number]
---

Fix issue #$1...
```

**多参数:**
```yaml
---
description: Deploy to environment
argument-hint: [app-name] [environment] [version]
---

Deploy $1 to $2 using version $3...
```

**带选项:**
```yaml
---
description: Run tests with options
argument-hint: [test-pattern] [options]
---

Run tests matching $1 with options: $2
```

### disable-model-invocation

**类型:** 布尔值
**必需:** 否
**默认值:** false

**目的:** 防止 SlashCommand 工具以编程方式调用命令

**Examples:**
```yaml
disable-model-invocation: true
```

**何时使用:**

1. **仅手动命令:** 需要用户判断的命令
   ```yaml
   ---
   description: Approve deployment to production
   disable-model-invocation: true
   ---
   ```

2. **破坏性操作:** 具有不可逆影响的命令
   ```yaml
   ---
   description: Delete all test data
   disable-model-invocation: true
   ---
   ```

3. **交互式工作流:** 需要用户输入的命令
   ```yaml
   ---
   description: Walk through setup wizard
   disable-model-invocation: true
   ---
   ```

**默认行为 (false):**
- 命令可供 SlashCommand 工具使用
- Claude 可以编程方式调用
- 仍可手动调用

**当为 true 时:**
- 命令仅可由用户键入 `/command` 调用
- 不可供 SlashCommand 工具使用
- 对敏感操作更安全

**最佳实践:**
- 谨慎使用（限制 Claude 的自主权）
- 在命令注释中记录原因
- 考虑如果始终手动，命令是否应该存在

## 完整示例

### 最小命令

不需要 frontmatter:

```markdown
Review this code for common issues and suggest improvements.
```

### 简单命令

仅描述:

```markdown
---
description: Review code for issues
---

Review this code for common issues and suggest improvements.
```

### 标准命令

描述和工具:

```markdown
---
description: Review Git changes
allowed-tools: Bash(git:*), Read
---

Current changes: !`git diff --name-only`

Review each changed file for:
- Code quality
- Potential bugs
- Best practices
```

### 复杂命令

所有常见字段:

```markdown
---
description: Deploy application to environment
argument-hint: [app-name] [environment] [version]
allowed-tools: Bash(kubectl:*), Bash(helm:*), Read
model: sonnet
---

Deploy $1 to $2 environment using version $3

Pre-deployment checks:
- Verify $2 configuration
- Check cluster status: !`kubectl cluster-info`
- Validate version $3 exists

Proceed with deployment following deployment runbook.
```

### 仅手动命令

受限调用:

```markdown
---
description: Approve production deployment
argument-hint: [deployment-id]
disable-model-invocation: true
allowed-tools: Bash(gh:*)
---

<!--
MANUAL APPROVAL REQUIRED
This command requires human judgment and cannot be automated.
-->

Review deployment $1 for production approval:

Deployment details: !`gh api /deployments/$1`

Verify:
- All tests passed
- Security scan clean
- Stakeholder approval
- Rollback plan ready

Type "APPROVED" to confirm deployment.
```

## 验证

### 常见错误

**无效的 YAML 语法:**
```yaml
---
description: Missing quote
allowed-tools: Read, Write
model: sonnet
---  # ❌ 上面缺少结束引号
```

**修复:** 验证 YAML 语法

**错误的工具规范:**
```yaml
allowed-tools: Bash  # ❌ 缺少命令过滤器
```

**修复:** 使用 `Bash(git:*)` 格式

**无效的模型名称:**
```yaml
model: gpt4  # ❌ 不是有效的 Claude 模型
```

**修复:** 使用 `sonnet`、`opus` 或 `haiku`

### 验证检查清单

提交命令之前:
- [ ] YAML 语法有效（无错误）
- [ ] 描述少于60个字符
- [ ] allowed-tools 使用正确格式
- [ ] model 如果指定则为有效值
- [ ] argument-hint 与位置参数匹配
- [ ] disable-model-invocation 适当使用

## 最佳实践总结

1. **从最小开始:** 仅在需要时添加 frontmatter
2. **记录参数:** 总是在有参数时使用 argument-hint
3. **限制工具:** 使用最严格的有效 allowed-tools
4. **选择正确的模型:** 使用 haiku 获得速度，使用 opus 处理复杂性
5. **谨慎使用仅手动:** 仅在必要时使用 disable-model-invocation
6. **清晰的描述:** 使命令在 `/help` 中可发现
7. **彻底测试:** 验证 frontmatter 是否按预期工作
