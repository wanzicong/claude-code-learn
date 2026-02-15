# 交互式命令模式

通过 AskUserQuestion 工具创建收集用户反馈和做出决策的命令的综合指南。

## 概述

某些命令需要用户输入，而简单的参数不太适用。例如：
- 在多个复杂选项之间进行权衡选择
- 从列表中选择多个项目
- 做出需要解释的决策
- 交互式收集偏好或配置

对于这些情况，请在命令执行中使用 **AskUserQuestion 工具**，而不是依赖命令参数。

## 何时使用 AskUserQuestion

### 在以下情况使用 AskUserQuestion:

1. **多项选择决策** 需要解释
2. **复杂选项** 需要上下文来选择
3. **多选场景**（选择多个项目）
4. **偏好收集** 用于配置
5. **交互式工作流** 根据答案进行调整

### 在以下情况使用命令参数:

1. **简单值**（文件路径、数字、名称）
2. **已知输入** 用户已经拥有
3. **可脚本化的工作流** 应该是可自动化的
4. **快速调用** 提示会减慢速度的情况

## AskUserQuestion 基础

### 工具参数

```typescript
{
  questions: [
    {
      question: "Which authentication method should we use?",
      header: "Auth method",  // Short label (max 12 chars)
      multiSelect: false,     // true for multiple selection
      options: [
        {
          label: "OAuth 2.0",
          description: "Industry standard, supports multiple providers"
        },
        {
          label: "JWT",
          description: "Stateless, good for APIs"
        },
        {
          label: "Session",
          description: "Traditional, server-side state"
        }
      ]
    }
  ]
}
```

**关键点:**
- 用户始终可以选择 "Other" 提供自定义输入（自动）
- `multiSelect: true` 允许选择多个选项
- 选项应为2-4个选择（不超过）
- 每次工具调用可以询问1-4个问题

## 用户交互的命令模式

### 基本交互式命令

```markdown
---
description: Interactive setup command
allowed-tools: AskUserQuestion, Write
---

# Interactive Plugin Setup

This command will guide you through configuring the plugin with a series of questions.

## Step 1: Gather Configuration

Use the AskUserQuestion tool to ask:

**Question 1 - Deployment target:**
- header: "Deploy to"
- question: "Which deployment platform will you use?"
- options:
  - AWS (Amazon Web Services with ECS/EKS)
  - GCP (Google Cloud with GKE)
  - Azure (Microsoft Azure with AKS)
  - Local (Docker on local machine)

**Question 2 - Environment strategy:**
- header: "Environments"
- question: "How many environments do you need?"
- options:
  - Single (Just production)
  - Standard (Dev, Staging, Production)
  - Complete (Dev, QA, Staging, Production)

**Question 3 - Features to enable:**
- header: "Features"
- question: "Which features do you want to enable?"
- multiSelect: true
- options:
  - Auto-scaling (Automatic resource scaling)
  - Monitoring (Health checks and metrics)
  - CI/CD (Automated deployment pipeline)
  - Backups (Automated database backups)

## Step 2: Process Answers

Based on the answers received from AskUserQuestion:

1. Parse the deployment target choice
2. Set up environment-specific configuration
3. Enable selected features
4. Generate configuration files

## Step 3: Generate Configuration

Create `.claude/plugin-name.local.md` with:

\`\`\`yaml
---
deployment_target: [answer from Q1]
environments: [answer from Q2]
features:
  auto_scaling: [true if selected in Q3]
  monitoring: [true if selected in Q3]
  ci_cd: [true if selected in Q3]
  backups: [true if selected in Q3]
---

# Plugin Configuration

Generated: [timestamp]
Target: [deployment_target]
Environments: [environments]
\`\`\`

## Step 4: Confirm and Next Steps

Confirm configuration created and guide user on next steps.
```

### 多阶段交互式工作流

```markdown
---
description: Multi-stage interactive workflow
allowed-tools: AskUserQuestion, Read, Write, Bash
---

# Multi-Stage Deployment Setup

此命令分阶段引导部署设置，根据您的答案进行调整。

## 阶段 1: 基本配置

使用 AskUserQuestion 询问部署基础信息。

根据答案，确定要询问哪些其他问题。

## 阶段 2: 高级选项（条件性）

如果用户在阶段 1 中选择了 "Advanced" 部署:

使用 AskUserQuestion 询问:
- 负载均衡策略
- 缓存配置
- 安全加固选项

如果用户选择了 "Simple" 部署:
- 跳过高级问题
- 使用合理的默认值

## 阶段 3: 确认

显示所有选择的摘要。

使用 AskUserQuestion 进行最终确认:
- header: "Confirm"
- question: "此配置看起来正确吗?"
- options:
  - Yes (继续设置)
  - No (重新开始)
  - Modify (让我调整特定设置)

如果选择 "Modify"，询问要更改哪个具体设置。

## 阶段 4: 执行设置

根据确认的配置，执行设置步骤。
```

## 交互式问题设计

### 问题结构

**良好的问题:**
```markdown
Question: "Which database should we use for this project?"
Header: "Database"
Options:
  - PostgreSQL (Relational, ACID compliant, best for complex queries)
  - MongoDB (Document store, flexible schema, best for rapid iteration)
  - Redis (In-memory, fast, best for caching and sessions)
```

**不好的问题:**
```markdown
Question: "Database?"  // Too vague
Header: "DB"  // Unclear abbreviation
Options:
  - Option 1  // Not descriptive
  - Option 2
```

### 选项设计最佳实践

**清晰的标签:**
- 使用1-5个词
- 具体且描述性
- 没有上下文不使用行话

**有用的描述:**
- 解释选项的含义
- 提及关键优势或权衡
- 帮助用户做出明智的决定
- 保持在1-2句话

**适当的数量:**
- 每个问题2-4个选项
- 不要用太多选择让用户不知所措
- 分组相关选项
- "Other" 自动提供

### 多选问题

**何时使用 multiSelect:**

```markdown
Use AskUserQuestion for enabling features:

Question: "Which features do you want to enable?"
Header: "Features"
multiSelect: true  // Allow selecting multiple
Options:
  - Logging (Detailed operation logs)
  - Metrics (Performance monitoring)
  - Alerts (Error notifications)
  - Backups (Automatic backups)
```

用户可以选择任意组合: 无、部分或全部。

**何时不使用 multiSelect:**

```markdown
Question: "Which authentication method?"
multiSelect: false  // Only one auth method makes sense
```

互斥选择不应使用 multiSelect。

## 使用 AskUserQuestion 的命令模式

### 模式 1: 简单的是/否决策

```markdown
---
description: Command with confirmation
allowed-tools: AskUserQuestion, Bash
---

# Destructive Operation

This operation will delete all cached data.

Use AskUserQuestion to confirm:

Question: "This will delete all cached data. Are you sure?"
Header: "Confirm"
Options:
  - Yes (Proceed with deletion)
  - No (Cancel operation)

If user selects "Yes":
  Execute deletion
  Report completion

If user selects "No":
  Cancel operation
  Exit without changes
```

### 模式 2: 多个配置问题

```markdown
---
description: Multi-question configuration
allowed-tools: AskUserQuestion, Write
---

# Project Configuration Setup

Gather configuration through multiple questions.

Use AskUserQuestion with multiple questions in one call:

**Question 1:**
- question: "Which programming language?"
- header: "Language"
- options: Python, TypeScript, Go, Rust

**Question 2:**
- question: "Which test framework?"
- header: "Testing"
- options: Jest, PyTest, Go Test, Cargo Test
  (Adapt based on language from Q1)

**Question 3:**
- question: "Which CI/CD platform?"
- header: "CI/CD"
- options: GitHub Actions, GitLab CI, CircleCI

**Question 4:**
- question: "Which features do you need?"
- header: "Features"
- multiSelect: true
- options: Linting, Type checking, Code coverage, Security scanning

Process all answers together to generate cohesive configuration.
```

### 模式 3: 条件性问题流程

```markdown
---
description: Conditional interactive workflow
allowed-tools: AskUserQuestion, Read, Write
---

# Adaptive Configuration

## Question 1: Deployment Complexity

Use AskUserQuestion:

Question: "How complex is your deployment?"
Header: "Complexity"
Options:
  - Simple (Single server, straightforward)
  - Standard (Multiple servers, load balancing)
  - Complex (Microservices, orchestration)

## Conditional Questions Based on Answer

If answer is "Simple":
  - No additional questions
  - Use minimal configuration

If answer is "Standard":
  - Ask about load balancing strategy
  - Ask about scaling policy

If answer is "Complex":
  - Ask about orchestration platform (Kubernetes, Docker Swarm)
  - Ask about service mesh (Istio, Linkerd, None)
  - Ask about monitoring (Prometheus, Datadog, CloudWatch)
  - Ask about logging aggregation

## Process Conditional Answers

Generate configuration appropriate for selected complexity level.
```

### 模式 4: 迭代收集

```markdown
---
description: Collect multiple items iteratively
allowed-tools: AskUserQuestion, Write
---

# Collect Team Members

We'll collect team member information for the project.

## Question: How many team members?

Use AskUserQuestion:

Question: "How many team members should we set up?"
Header: "Team size"
Options:
  - 2 people
  - 3 people
  - 4 people
  - 6 people

## Iterate Through Team Members

For each team member (1 to N based on answer):

Use AskUserQuestion for member details:

Question: "What role for team member [number]?"
Header: "Role"
Options:
  - Frontend Developer
  - Backend Developer
  - DevOps Engineer
  - QA Engineer
  - Designer

Store each member's information.

## Generate Team Configuration

After collecting all N members, create team configuration file with all members and their roles.
```

### 模式 5: 依赖项选择

```markdown
---
description: Select dependencies with multi-select
allowed-tools: AskUserQuestion
---

# Configure Project Dependencies

## Question: Required Libraries

Use AskUserQuestion with multiSelect:

Question: "Which libraries does your project need?"
Header: "Dependencies"
multiSelect: true
Options:
  - React (UI framework)
  - Express (Web server)
  - TypeORM (Database ORM)
  - Jest (Testing framework)
  - Axios (HTTP client)

User can select any combination.

## Process Selections

For each selected library:
- Add to package.json dependencies
- Generate sample configuration
- Create usage examples
- Update documentation
```

## 交互式命令的最佳实践

### 问题设计

1. **清晰具体**: 问题应该明确无误
2. **简洁的标题**: 最多12个字符以便清晰显示
3. **有用的选项**: 标签清晰，描述解释权衡
4. **适当的数量**: 每个问题2-4个选项，每次调用1-4个问题
5. **逻辑顺序**: 问题自然流畅

### 错误处理

```markdown
# Handle AskUserQuestion Responses

After calling AskUserQuestion, verify answers received:

If answers are empty or invalid:
  Something went wrong gathering responses.

  Please try again or provide configuration manually:
  [Show alternative approach]

  Exit.

If answers look correct:
  Process as expected
```

### 渐进式披露

```markdown
# Start Simple, Get Detailed as Needed

## Question 1: Setup Type

Use AskUserQuestion:

Question: "How would you like to set up?"
Header: "Setup type"
Options:
  - Quick (Use recommended defaults)
  - Custom (Configure all options)
  - Guided (Step-by-step with explanations)

If "Quick":
  Apply defaults, minimal questions

If "Custom":
  Ask all available configuration questions

If "Guided":
  Ask questions with extra explanation
  Provide recommendations along the way
```

### 多选指南

**良好的多选使用:**
```markdown
Question: "Which features do you want to enable?"
multiSelect: true
Options:
  - Logging
  - Metrics
  - Alerts
  - Backups

Reason: User might want any combination
```

**不好的多选使用:**
```markdown
Question: "Which database engine?"
multiSelect: true  // ❌ Should be single-select

Reason: Can only use one database engine
```

## 高级模式

### 验证循环

```markdown
---
description: Interactive with validation
allowed-tools: AskUserQuestion, Bash
---

# Setup with Validation

## Gather Configuration

Use AskUserQuestion to collect settings.

## Validate Configuration

Check if configuration is valid:
- Required dependencies available?
- Settings compatible with each other?
- No conflicts detected?

If validation fails:
  Show validation errors

  Use AskUserQuestion to ask:

  Question: "Configuration has issues. What would you like to do?"
  Header: "Next step"
  Options:
    - Fix (Adjust settings to resolve issues)
    - Override (Proceed despite warnings)
    - Cancel (Abort setup)

  Based on answer, retry or proceed or exit.
```

### 增量构建配置

```markdown
---
description: Incremental configuration builder
allowed-tools: AskUserQuestion, Write, Read
---

# Incremental Setup

## Phase 1: Core Settings

Use AskUserQuestion for core settings.

Save to `.claude/config-partial.yml`

## Phase 2: Review Core Settings

Show user the core settings:

Based on these core settings, you need to configure:
- [Setting A] (because you chose [X])
- [Setting B] (because you chose [Y])

Ready to continue?

## Phase 3: Detailed Settings

Use AskUserQuestion for settings based on Phase 1 answers.

Merge with core settings.

## Phase 4: Final Review

Present complete configuration.

Use AskUserQuestion for confirmation:

Question: "Is this configuration correct?"
Options:
  - Yes (Save and apply)
  - No (Start over)
  - Modify (Edit specific settings)
```

### 基于上下文的动态选项

```markdown
---
description: Context-aware questions
allowed-tools: AskUserQuestion, Bash, Read
---

# Context-Aware Setup

## Detect Current State

Check existing configuration:
- Current language: !`detect-language.sh`
- Existing frameworks: !`detect-frameworks.sh`
- Available tools: !`check-tools.sh`

## Ask Context-Appropriate Questions

Based on detected language, ask relevant questions.

If language is TypeScript:

  Use AskUserQuestion:

  Question: "Which TypeScript features should we enable?"
  Options:
    - Strict Mode (Maximum type safety)
    - Decorators (Experimental decorator support)
    - Path Mapping (Module path aliases)

If language is Python:

  Use AskUserQuestion:

  Question: "Which Python tools should we configure?"
  Options:
    - Type Hints (mypy for type checking)
    - Black (Code formatting)
    - Pylint (Linting and style)

Questions adapt to project context.
```

## 实际示例: 多代理集群启动

**来自 multi-agent-swarm 插件:**

```markdown
---
description: Launch multi-agent swarm
allowed-tools: AskUserQuestion, Read, Write, Bash
---

# Launch Multi-Agent Swarm

## Interactive Mode (No Task List Provided)

If user didn't provide task list file, help create one interactively.

### Question 1: Agent Count

Use AskUserQuestion:

Question: "How many agents should we launch?"
Header: "Agent count"
Options:
  - 2 agents (Best for simple projects)
  - 3 agents (Good for medium projects)
  - 4 agents (Standard team size)
  - 6 agents (Large projects)
  - 8 agents (Complex multi-component projects)

### Question 2: Task Definition Approach

Use AskUserQuestion:

Question: "How would you like to define tasks?"
Header: "Task setup"
Options:
  - File (I have a task list file ready)
  - Guided (Help me create tasks interactively)
  - Custom (Other approach)

If "File":
  Ask for file path
  Validate file exists and has correct format

If "Guided":
  Enter iterative task creation mode (see below)

### Question 3: Coordination Mode

Use AskUserQuestion:

Question: "How should agents coordinate?"
Header: "Coordination"
Options:
  - Team Leader (One agent coordinates others)
  - Collaborative (Agents coordinate as peers)
  - Autonomous (Independent work, minimal coordination)

### Iterative Task Creation (If "Guided" Selected)

For each agent (1 to N from Question 1):

**Question A: Agent Name**
Question: "What should we call agent [number]?"
Header: "Agent name"
Options:
  - auth-agent
  - api-agent
  - ui-agent
  - db-agent
  (Provide relevant suggestions based on common patterns)

**Question B: Task Type**
Question: "What task for [agent-name]?"
Header: "Task type"
Options:
  - Authentication (User auth, JWT, OAuth)
  - API Endpoints (REST/GraphQL APIs)
  - UI Components (Frontend components)
  - Database (Schema, migrations, queries)
  - Testing (Test suites and coverage)
  - Documentation (Docs, README, guides)

**Question C: Dependencies**
Question: "What does [agent-name] depend on?"
Header: "Dependencies"
multiSelect: true
Options:
  - [List of previously defined agents]
  - No dependencies

**Question D: Base Branch**
Question: "Which base branch for PR?"
Header: "PR base"
Options:
  - main
  - staging
  - develop

Store all task information for each agent.

### Generate Task List File

After collecting all agent task details:

1. Ask for project name
2. Generate task list in proper format
3. Save to `.daisy/swarm/tasks.md`
4. Show user the file path
5. Proceed with launch using generated task list
```

## 最佳实践

### 问题编写

1. **要具体**: "哪个数据库?" 而不是 "选择选项?"
2. **解释权衡**: 在选项描述中描述优缺点
3. **提供上下文**: 问题文本应该独立存在
4. **引导决策**: 帮助用户做出明智的选择
5. **保持简洁**: 标题最多12个字符，描述1-2句话

### 选项设计

1. **有意义的标签**: 具体、清晰的名称
2. **信息丰富的描述**: 解释每个选项的作用
3. **显示权衡**: 帮助用户理解影响
4. **一致的细节**: 所有选项同等程度地解释
5. **2-4个选项**: 不太少，也不太多

### 流程设计

1. **逻辑顺序**: 问题自然流畅
2. **基于之前的**: 后面的问题使用之前的答案
3. **最小化问题**: 只询问所需的内容
4. **分组相关**: 一起询问相关问题
5. **显示进度**: 指示在流程中的位置

### 用户体验

1. **设定期望**: 告诉用户期待什么
2. **解释原因**: 帮助用户理解目的
3. **提供默认值**: 建议推荐选项
4. **允许退出**: 让用户取消或重新开始
5. **确认操作**: 在执行之前总结

## 常见模式

### 模式: 功能选择

```markdown
Use AskUserQuestion:

Question: "Which features do you need?"
Header: "Features"
multiSelect: true
Options:
  - Authentication
  - Authorization
  - Rate Limiting
  - Caching
```

### 模式: 环境配置

```markdown
Use AskUserQuestion:

Question: "Which environment is this?"
Header: "Environment"
Options:
  - Development (Local development)
  - Staging (Pre-production testing)
  - Production (Live environment)
```

### 模式: 优先级选择

```markdown
Use AskUserQuestion:

Question: "What's the priority for this task?"
Header: "Priority"
Options:
  - Critical (Must be done immediately)
  - High (Important, do soon)
  - Medium (Standard priority)
  - Low (Nice to have)
```

### 模式: 范围选择

```markdown
Use AskUserQuestion:

Question: "What scope should we analyze?"
Header: "Scope"
Options:
  - Current file (Just this file)
  - Current directory (All files in directory)
  - Entire project (Full codebase scan)
```

## 结合参数和问题

### 适当使用两者

**已知值使用参数:**
```markdown
---
argument-hint: [project-name]
allowed-tools: AskUserQuestion, Write
---

Setup for project: $1

Now gather additional configuration...

Use AskUserQuestion for options that require explanation.
```

**复杂选择使用问题:**
```markdown
Project name from argument: $1

Now use AskUserQuestion to choose:
- Architecture pattern
- Technology stack
- Deployment strategy

These require explanation, so questions work better than arguments.
```

## 故障排除

**问题未出现:**
- 验证 allowed-tools 中有 AskUserQuestion
- 检查问题格式是否正确
- 确保选项数组有2-4个项目

**用户无法进行选择:**
- 检查选项标签是否清晰
- 验证描述是否有帮助
- 考虑是否选项太多
- 确保 multiSelect 设置正确

**流程感觉混乱:**
- 减少问题数量
- 分组相关问题
- 在阶段之间添加解释
- 通过工作流显示进度

使用 AskUserQuestion，命令成为交互式向导，引导用户完成复杂决策，同时保持简单参数为直接输入提供的清晰度。
