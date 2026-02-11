---
name: command-development
description: 当用户要求"创建斜杠命令"、"添加命令"、"编写自定义命令"、"定义命令参数"、"使用命令 frontmatter"、"组织命令"、"创建带有文件引用的命令"、"交互式命令"、"在命令中使用 AskUserQuestion"，或者需要有关 Claude Code 斜杠命令结构、YAML frontmatter 字段、动态参数、命令中的 bash 执行、用户交互模式或命令开发最佳实践的指导时，应使用此技能。
version: 0.2.0
---

# Claude Code 命令开发

## 概述

斜杠命令是定义为 Markdown 文件的常用提示，Claude 在交互式会话中执行这些提示。理解命令结构、frontmatter 选项和动态功能可以创建强大、可重用的工作流。

**关键概念：**
- 命令的 Markdown 文件格式
- 用于配置的 YAML frontmatter
- 动态参数和文件引用
- 用于上下文的 Bash 执行
- 命令组织和命名空间

## 命令基础

### 什么是斜杠命令？

斜杠命令是一个包含提示的 Markdown 文件，当被调用时 Claude 会执行该提示。命令提供：
- **可重用性**：一次定义，重复使用
- **一致性**：标准化常见工作流
- **共享**：在团队或项目之间分发
- **效率**：快速访问复杂提示

### 重要：命令是给 Claude 的指令

**命令是写给 agent 使用的，而不是给人使用的。**

当用户调用 `/command-name` 时，命令内容成为 Claude 的指令。将命令编写为给 Claude 关于要做什么的指令，而不是给用户的消息。

**正确的方法（给 Claude 的指令）：**
```markdown
Review this code for security vulnerabilities including:
- SQL injection
- XSS attacks
- Authentication issues

Provide specific line numbers and severity ratings.
```

**错误的方法（给用户的消息）：**
```markdown
This command will review your code for security issues.
You'll receive a report with vulnerability details.
```

第一个示例告诉 Claude 要做什么。第二个示例告诉用户将要发生什么，但没有指示 Claude。始终使用第一种方法。

### 命令位置

**项目命令**（与团队共享）：
- 位置：`.claude/commands/`
- 范围：在特定项目中可用
- 标签：在 `/help` 中显示为 "(project)"
- 用于：团队工作流、项目特定任务

**个人命令**（随处可用）：
- 位置：`~/.claude/commands/`
- 范围：在所有项目中可用
- 标签：在 `/help` 中显示为 "(user)"
- 用于：个人工作流、跨项目实用工具

**插件命令**（与插件捆绑）：
- 位置：`plugin-name/commands/`
- 范围：插件安装时可用
- 标签：在 `/help` 中显示为 "(plugin-name)"
- 用于：插件特定功能

## 文件格式

### 基本结构

命令是带有 `.md` 扩展名的 Markdown 文件：

```
.claude/commands/
├── review.md           # /review command
├── test.md             # /test command
└── deploy.md           # /deploy command
```

**简单命令：**
```markdown
Review this code for security vulnerabilities including:
- SQL injection
- XSS attacks
- Authentication bypass
- Insecure data handling
```

基本命令不需要 frontmatter。

### 带有 YAML Frontmatter

使用 YAML frontmatter 添加配置：

```markdown
---
description: Review code for security issues
allowed-tools: Read, Grep, Bash(git:*)
model: sonnet
---

Review this code for security vulnerabilities...
```

## YAML Frontmatter 字段

### description

**用途：** 在 `/help` 中显示的简短描述
**类型：** 字符串
**默认：** 命令提示的第一行

```yaml
---
description: Review pull request for code quality
---
```

**最佳实践：** 清晰、可操作的描述（60 个字符以下）

### allowed-tools

**用途：** 指定命令可以使用的工具
**类型：** 字符串或数组
**默认：** 继承自对话

```yaml
---
allowed-tools: Read, Write, Edit, Bash(git:*)
---
```

**模式：**
- `Read, Write, Edit` - 特定工具
- `Bash(git:*)` - 仅 git 命令的 Bash
- `*` - 所有工具（很少需要）

**使用时机：** 命令需要特定的工具访问

### model

**用途：** 指定用于命令执行的模型
**类型：** 字符串（sonnet、opus、haiku）
**默认：** 继承自对话

```yaml
---
model: haiku
---
```

**用例：**
- `haiku` - 快速、简单命令
- `sonnet` - 标准工作流
- `opus` - 复杂分析

### argument-hint

**用途：** 记录预期参数以供自动完成
**类型：** 字符串
**默认：** 无

```yaml
---
argument-hint: [pr-number] [priority] [assignee]
---
```

**好处：**
- 帮助用户理解命令参数
- 改进命令发现
- 记录命令接口

### disable-model-invocation

**用途：** 防止 SlashCommand 工具以编程方式调用命令
**类型：** 布尔值
**默认：** false

```yaml
---
disable-model-invocation: true
---
```

**使用时机：** 命令应仅手动调用

## 动态参数

### 使用 $ARGUMENTS

将所有参数捕获为单个字符串：

```markdown
---
description: Fix issue by number
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS following our coding standards and best practices.
```

**用法：**
```
> /fix-issue 123
> /fix-issue 456
```

**展开为：**
```
Fix issue #123 following our coding standards...
Fix issue #456 following our coding standards...
```

### 使用位置参数

使用 `$1`、`$2`、`$3` 等捕获各个参数：

```markdown
---
description: Review PR with priority and assignee
argument-hint: [pr-number] [priority] [assignee]
---

Review pull request #$1 with priority level $2.
After review, assign to $3 for follow-up.
```

**用法：**
```
> /review-pr 123 high alice
```

**展开为：**
```
Review pull request #123 with priority level high.
After review, assign to alice for follow-up.
```

### 组合参数

混合位置参数和剩余参数：

```markdown
Deploy $1 to $2 environment with options: $3
```

**用法：**
```
> /deploy api staging --force --skip-tests
```

**展开为：**
```
Deploy api to staging environment with options: --force --skip-tests
```

## 文件引用

### 使用 @ 语法

在命令中包含文件内容：

```markdown
---
description: Review specific file
argument-hint: [file-path]
---

Review @$1 for:
- Code quality
- Best practices
- Potential bugs
```

**用法：**
```
> /review-file src/api/users.ts
```

**效果：** Claude 在处理命令之前读取 `src/api/users.ts`

### 多文件引用

引用多个文件：

```markdown
Compare @src/old-version.js with @src/new-version.js

Identify:
- Breaking changes
- New features
- Bug fixes
```

### 静态文件引用

引用已知文件而无参数：

```markdown
Review @package.json and @tsconfig.json for consistency

Ensure:
- TypeScript version matches
- Dependencies are aligned
- Build configuration is correct
```

## 命令中的 Bash 执行

命令可以内联执行 bash 命令，以便在 Claude 处理命令之前动态收集上下文。这对于包含仓库状态、环境信息或项目特定的上下文很有用。

**使用时机：**
- 包含动态上下文（git 状态、环境变量等）
- 收集项目/仓库状态
- 构建上下文感知的工作流

**实现细节：**
有关完整语法、示例和最佳实践，请参阅 `references/plugin-features-reference.md` 中的 bash 执行部分。该参考资料包含确切的语法和多个可运行的示例，以避免执行问题

## 命令组织

### 扁平结构

用于小命令集的简单组织：

```
.claude/commands/
├── build.md
├── test.md
├── deploy.md
├── review.md
└── docs.md
```

**使用时机：** 5-15 个命令，没有清晰的类别

### 命名空间结构

在子目录中组织命令：

```
.claude/commands/
├── ci/
│   ├── build.md        # /build (project:ci)
│   ├── test.md         # /test (project:ci)
│   └── lint.md         # /lint (project:ci)
├── git/
│   ├── commit.md       # /commit (project:git)
│   └── pr.md           # /pr (project:git)
└── docs/
    ├── generate.md     # /generate (project:docs)
    └── publish.md      # /publish (project:docs)
```

**好处：**
- 按类别逻辑分组
- 在 `/help` 中显示命名空间
- 更容易找到相关命令

**使用时机：** 15+ 个命令，清晰的类别

## 最佳实践

### 命令设计

1. **单一职责：** 一个命令，一个任务
2. **清晰描述：** 在 `/help` 中不言自明
3. **显式依赖：** 需要时使用 `allowed-tools`
4. **记录参数：** 始终提供 `argument-hint`
5. **一致命名：** 使用动词-名词模式（review-pr、fix-issue）

### 参数处理

1. **验证参数：** 在提示中检查所需参数
2. **提供默认值：** 参数缺失时建议默认值
3. **记录格式：** 解释预期参数格式
4. **处理边缘情况：** 考虑缺失或无效的参数

```markdown
---
argument-hint: [pr-number]
---

$IF($1,
  Review PR #$1,
  Please provide a PR number. Usage: /review-pr [number]
)
```

### 文件引用

1. **显式路径：** 使用清晰的文件路径
2. **检查存在：** 优雅地处理缺失的文件
3. **相对路径：** 使用项目相对路径
4. **Glob 支持：** 考虑将 Glob 工具用于模式

### Bash 命令

1. **限制范围：** 使用 `Bash(git:*)` 而非 `Bash(*)`
2. **安全命令：** 避免破坏性操作
3. **处理错误：** 考虑命令失败
4. **保持快速：** 长时间运行的命令会减慢调用

### 文档

1. **添加注释：** 解释复杂逻辑
2. **提供示例：** 在注释中显示用法
3. **列出要求：** 记录依赖项
4. **版本命令：** 注明重大更改

```markdown
---
description: Deploy application to environment
argument-hint: [environment] [version]
---

<!--
Usage: /deploy [staging|production] [version]
Requires: AWS credentials configured
Example: /deploy staging v1.2.3
-->

Deploy application to $1 environment using version $2...
```

## 常见模式

### 审查模式

```markdown
---
description: Review code changes
allowed-tools: Read, Bash(git:*)
---

Files changed: !`git diff --name-only`

Review each file for:
1. Code quality and style
2. Potential bugs or issues
3. Test coverage
4. Documentation needs

Provide specific feedback for each file.
```

### 测试模式

```markdown
---
description: Run tests for specific file
argument-hint: [test-file]
allowed-tools: Bash(npm:*), Bash(jest:*)
---

Run tests: !`npm test $1`

Analyze results and suggest fixes for failures.
```

### 文档模式

```markdown
---
description: Generate documentation for file
argument-hint: [source-file]
---

Generate comprehensive documentation for @$1 including:
- Function/class descriptions
- Parameter documentation
- Return value descriptions
- Usage examples
- Edge cases and errors
```

### 工作流模式

```markdown
---
description: Complete PR workflow
argument-hint: [pr-number]
allowed-tools: Bash(gh:*), Read
---

PR #$1 Workflow:

1. Fetch PR: !`gh pr view $1`
2. Review changes
3. Run checks
4. Approve or request changes
```

## 故障排除

**命令不出现：**
- 检查文件是否在正确目录中
- 验证 `.md` 扩展名存在
- 确保有效的 Markdown 格式
- 重启 Claude Code

**参数不工作：**
- 验证 `$1`、`$2` 语法正确
- 检查 `argument-hint` 匹配用法
- 确保没有多余空格

**Bash 执行失败：**
- 检查 `allowed-tools` 包含 Bash
- 验证反引号中的命令语法
- 先在终端中测试命令
- 检查所需权限

**文件引用不工作：**
- 验证 `@` 语法正确
- 检查文件路径有效
- 确保允许 Read 工具
- 使用绝对或项目相对路径

## 插件特定功能

### CLAUDE_PLUGIN_ROOT 变量

插件命令可以访问 `${CLAUDE_PLUGIN_ROOT}`，这是一个解析为插件绝对路径的环境变量。

**用途：**
- 可移植地引用插件文件
- 执行插件脚本
- 加载插件配置
- 访访问插件模板

**基本用法：**

```markdown
---
description: Analyze using plugin script
allowed-tools: Bash(node:*)
---

Run analysis: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js $1`

Review results and report findings.
```

**常见模式：**

```markdown
# 执行插件脚本
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh`

# 加载插件配置
@${CLAUDE_PLUGIN_ROOT}/config/settings.json

# 使用插件模板
@${CLAUDE_PLUGIN_ROOT}/templates/report.md

# 访问插件资源
@${CLAUDE_PLUGIN_ROOT}/docs/reference.md
```

**为何使用它：**
- 在所有安装中工作
- 在系统之间可移植
- 无需硬编码路径
- 对于多文件插件必不可少

### 插件命令组织

从 `commands/` 目录自动发现插件命令：

```
plugin-name/
├── commands/
│   ├── foo.md              # /foo (plugin:plugin-name)
│   ├── bar.md              # /bar (plugin:plugin-name)
│   └── utils/
│       └helper.md       # /helper (plugin:plugin-name:utils)
└── plugin.json
```

**命名空间好处：**
- 逻辑命令分组
- 在 `/help` 输出中显示
- 避免名称冲突
- 组织相关命令

**命名约定：**
- 使用描述性操作名称
- 避免通用名称（test、run）
- 考虑插件特定前缀
- 使用连字符命名多词名称

### 插件命令模式

**基于配置的模式：**

```markdown
---
description: Deploy using plugin configuration
argument-hint: [environment]
allowed-tools: Read, Bash(*)
---

Load configuration: @${CLAUDE_PLUGIN_ROOT}/config/$1-deploy.json

Deploy to $1 using configuration settings.
Monitor deployment and report status.
```

**基于模板的模式：**

```markdown
---
description: Generate docs from template
argument-hint: [component]
---

Template: @${CLAUDE_PLUGIN_ROOT}/templates/docs.md

Generate documentation for $1 following template structure.
```

**多脚本模式：**

```markdown
---
description: Complete build workflow
allowed-tools: Bash(*)
---

Build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh`
Test: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test.sh`
Package: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/package.sh`

Review outputs and report workflow status.
```

**请参阅 `references/plugin-features-reference.md` 了解详细模式。**

## 与插件组件集成

命令可以与其他插件组件集成以实现强大的工作流。

### Agent 集成

启动插件代理以完成复杂任务：

```markdown
---
description: Deep code review
argument-hint: [file-path]
---

Initiate comprehensive review of @$1 using the code-reviewer agent.

The agent will analyze:
- Code structure
- Security issues
- Performance
- Best practices

Agent uses plugin resources:
- ${CLAUDE_PLUGIN_ROOT}/config/rules.json
- ${CLAUDE_PLUGIN_ROOT}/checklists/review.md
```

**关键点：**
- Agent 必须存在于 `plugin/agents/` 目录中
- Claude 使用 Task 工具启动 agent
- 记录 agent 功能
- 引用 agent 使用的插件资源

### Skill 集成

利用插件技能获取专门知识：

```markdown
---
description: Document API with standards
argument-hint: [api-file]
---

Document API in @$1 following plugin standards.

Use the api-docs-standards skill to ensure:
- Complete endpoint documentation
- Consistent formatting
- Example quality
- Error documentation

Generate production-ready API docs.
```

**关键点：**
- Skill 必须存在于 `plugin/skills/` 目录中
- 提及 skill 名称以触发调用
- 记录 skill 目的
- 解释 skill 提供的内容

### Hook 协调

设计与插件 hooks 一起工作的命令：
- 命令可以为 hooks 准备状态进行处理
- Hooks 在工具事件上自动执行
- 命令应记录预期的 hook 行为
- 指导 Claude 解释 hook 输出

请参阅 `references/plugin-features-reference.md` 了解与 hooks 协调的命令示例

### 多组件工作流

组合 agents、skills 和 scripts：

```markdown
---
description: Comprehensive review workflow
argument-hint: [file]
allowed-tools: Bash(node:*), Read
---

Target: @$1

Phase 1 - Static Analysis:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

Phase 2 - Deep Review:
Launch the code-quality-reviewer agent for detailed analysis.

Phase 3 - Standards Check:
Use the coding-standards skill for validation.

Phase 4 - Report:
Template: @${CLAUDE_PLUGIN_ROOT}/templates/review-report.md

Compile findings into report following template.
```

**使用时机：**
- 复杂的多步工作流
- 利用多个插件功能
- 需要专门分析
- 需要结构化输出

## 验证模式

命令应在处理之前验证输入和资源。

### 参数验证

```markdown
---
description: Deploy with validation
argument-hint: [environment]
---

Validate environment: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`

If $1 is valid environment:
  Deploy to $1
Otherwise:
  Explain valid environments: dev, staging, prod
  Show usage: /deploy [environment]
```

### 文件存在检查

```markdown
---
description: Process configuration
argument-hint: [config-file]
---

Check file exists: !`test -f $1 && echo "EXISTS" || echo "MISSING"`

If file exists:
  Process configuration: @$1
Otherwise:
  Explain where to place config file
  Show expected format
  Provide example configuration
```

### 插件资源验证

```markdown
---
description: Run plugin analyzer
allowed-tools: Bash(test:*)
---

Validate plugin setup:
- Script: !`test -x ${CLAUDE_PLUGIN_ROOT}/bin/analyze && echo "✓" || echo "✗"`
- Config: !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "✓" || echo "✗"`

If all checks pass, run analysis.
Otherwise, report missing components.
```

### 错误处理

```markdown
---
description: Build with error handling
allowed-tools: Bash(*)
---

Execute build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh 2>&1 || echo "BUILD_FAILED"`

If build succeeded:
  Report success and output location
If build failed:
  Analyze error output
  Suggest likely causes
  Provide troubleshooting steps
```

**最佳实践：**
- 尽早验证
- 提供有用的错误消息
- 建议纠正操作
- 优雅地处理边缘情况

---

有关详细的 frontmatter 字段规范，请参阅 `references/frontmatter-reference.md`。
有关插件特定功能和模式，请参阅 `references/plugin-features-reference.md`。
有关命令模式示例，请参阅 `examples/` 目录。
