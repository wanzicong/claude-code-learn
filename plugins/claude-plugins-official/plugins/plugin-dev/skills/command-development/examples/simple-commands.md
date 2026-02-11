# 简单命令示例

常见用例的基本斜杠命令模式。

**重要：** 下面的所有示例都是写给 Claude 使用的指令（agent 使用），而不是给用户的消息。命令告诉 Claude 要做什么，而不是告诉用户将要发生什么。

## 示例 1：代码审查命令

**文件：** `.claude/commands/review.md`

```markdown
---
description: Review code for quality and issues
allowed-tools: Read, Bash(git:*)
---

Review
 代码，检查：

1. **Code Quality:**
   - Readability and maintainability
   - Consistent style and formatting
   - Appropriate abstraction levels

2. **Potential Issues:**
   - Logic errors or bugs
   - Edge cases not handled
   - Performance concerns

3. **Best Practices:**
   - Design patterns used correctly
   - Error handling present
   - Documentation adequate

Provide specific feedback with file and line references.
```

**用法：**
```
> /review
```

---

## 示例 2：安全审查命令

**文件：** `.claude/commands/security-review.md`

```markdown
---
description: Review code for security vulnerabilities
allowed-tools: Read, Grep
model: sonnet
---

Perform comprehensive security review checking for:

**Common Vulnerabilities:**
- SQL injection risks
- Cross-site scripting (XSS)
- Authentication/authorization issues
- Insecure data handling
- Hardcoded secrets or credentials

**Security Best Practices:**
- Input validation present
- Output encoding correct
- Secure defaults used
- Error messages safe
- Logging appropriate (no sensitive data)

For each issue found:
- File and line number
- Severity (Critical/High/Medium/Low)
- Description of vulnerability
- Recommended fix

Prioritize issues by severity.
```

**用法：**
```
> /security-review
```

---

## 示例 3：带文件参数的测试命令

**文件：** `.claude/commands/test-file.md`

```markdown
---
description: Run tests for specific file
argument-hint: [test-file]
allowed-tools: Bash(npm:*), Bash(jest:*)
---

Run tests for $1:

Test execution: !`npm test $1`

Analyze results:
- Tests passed/failed
- Code coverage
- Performance issues
- Flaky tests

If failures found, suggest fixes based on error messages.
```

**用法：**
```
> /test-file src/utils/helpers.test.ts
```

---

## 示例 4：文档生成器

**文件：** `.claude/commands/document.md`

```markdown
---
description: Generate documentation for file
argument-hint: [source-file]
---

Generate comprehensive documentation for @$1

Include:

**Overview:**
- Purpose and responsibility
- Main functionality
- Dependencies

**API Documentation:**
- Function/method signatures
- Parameter descriptions with types
- Return values with types
- Exceptions/errors thrown

**Usage Examples:**
- Basic usage
- Common patterns
- Edge cases

**Implementation Notes:**
- Algorithm complexity
- Performance considerations
- Known limitations

Format as Markdown suitable for project documentation.
```

**用法：**
```
> /document src/api/users.ts
```

---

## 示例 5：Git 状态摘要

**文件：** `.claude/commands/git-status.md`

```markdown
---
description: Summarize Git repository status
allowed-tools: Bash(git:*)
---

Repository Status Summary:

**Current Branch:** !`git branch --show-current`

**Status:** !`git status --short`

**Recent Commits:** !`git log --oneline -5`

**Remote Status:** !`git fetch && git status -sb`

Provide:
- Summary of changes
- Suggested next actions
- Any warnings or issues
```

**用法：**
```
> /git-status
```

---

## 示例 6：部署命令

**文件：** `.claude/commands/deploy.md`

```markdown
---
description: Deploy to specified environment
argument-hint: [environment] [version]
allowed-tools: Bash(kubectl:*), Read
---

Deploy to $1 environment using version $2

**Pre-deployment Checks:**
1. Verify $1 configuration exists
2. Check version $2 is valid
3. Verify cluster accessibility: !`kubectl cluster-info`

**Deployment Steps:**
1. Update deployment manifest with version $2
2. Apply configuration to $1
3. Monitor rollout status
4. Verify pod health
5. Run smoke tests

**Rollback Plan:**
Document current version for rollback if issues occur.

Proceed with deployment? (yes/no)
```

**用法：**
```
> /deploy staging v1.2.3
```

---

## 示例 7：比较命令

**文件：** `.claude/commands/compare-files.md`

```markdown
---
description: Compare two files
argument-hint: [file1] [file2]
---

Compare @$1 with @$2

**Analysis:**

1. **Differences:**
   - Lines added
   - Lines removed
   - Lines modified

2. **Functional Changes:**
   - Breaking changes
   - New features
   - Bug fixes
   - Refactoring

3. **Impact:**
   - Affected components
   - Required updates elsewhere
   - Migration requirements

4. **Recommendations:**
   - Code review focus areas
   - Testing requirements
   - Documentation updates needed

Present as structured comparison report.
```

**用法：**
```
> /compare-files src/old-api.ts src/new-api.ts
```

---

## 示例 8：快速修复命令

**文件：** `.claude/commands/quick-fix.md`

```markdown
---
description: Quick fix for common issues
argument-hint: [issue-description]
model: haiku
---

Quickly fix: $ARGUMENTS

**Approach:**
1. Identify the issue
2. Find relevant code
3. Propose a fix
4. Explain solution

Focus on:
- Simple, direct solution
- Minimal changes
- Following existing patterns
- No breaking changes

Provide code changes with file paths and line numbers.
```

**用法：**
```
> /quick-fix button not responding to clicks
> /quick-fix typo in error message
```

---

## 示例 9：研究命令

**文件：** `.claude/commands/research.md`

```markdown
---
description: Research best practices for topic
argument-hint: [topic]
model: sonnet
---

Research best practices for: $ARGUMENTS

**Coverage:**

1. **Current State:**
   - How we currently handle this
   - Existing implementations

2. **Industry Standards:**
   - Common patterns
   - Recommended approaches
   - Tools and libraries

3. **Comparison:**
   - Our approach vs standards
   - Gaps or improvements needed
   - Migration considerations

4. **Recommendations:**
   - Concrete action items
   - Priority and effort estimates
   - Resources for implementation

Provide actionable guidance based on research.
```

**用法：**
```
> /research error handling in async operations
> /research API authentication patterns
```

---

## 示例 10：解释代码命令

**文件：** `.claude/commands/explain.md`

```markdown
---
description: Explain how code works
argument-hint: [file-or-function]
---

Explain @$1 in detail

**Explanation Structure:**

1. **Overview:**
   - What it does
   - Why it exists
   - How it fits in system

2. **Step-by-Step:**
   - Line-by-line walkthrough
   - Key algorithms or logic
   - Important details

3. **Inputs and Outputs:**
   - Parameters and types
   - Return values
   - Side effects

4. **Edge Cases:**
   - Error handling
   - Special cases
   - Limitations

5. **Usage Examples:**
   - How to call it
   - Common patterns
   - Integration points

Explain at level appropriate for junior engineer.
```

**用法：**
```
> /explain src/utils/cache.ts
> /explain AuthService.login
```

---

## 关键模式

### 模式 1：只读分析

```markdown
---
allowed-tools: Read, Grep
---

Analyze but don't modify...
```

**用于：** 代码审查、文档、分析

### 模式 2：Git 操作

```markdown
---
allowed-tools: Bash(git:*)
---

!`git status`
Analyze and suggest...
```

**用于：** 仓库状态、提交分析

### 模式 3：单个参数

```markdown
---
argument-hint: [target]
---

Process $1...
```

**用于：** 文件操作、目标操作

### 模式 4：多个参数

```markdown
---
argument-hint: [source] [target] [options]
---

Process $1 to $2 with $3...
```

**用于：** 工作流、部署、比较

### 模式 5：快速执行

```markdown
---
model: haiku
---

Quick simple task...
```

**用于：** 简单、重复的命令

### 模式 6：文件比较

```markdown
Compare @$1 with @$2...
```

**用于：** 差异分析、迁移规划

### 模式 7：上下文收集

```markdown
---
allowed-tools: Bash(git:*), Read
---

Context: !`git status`
Files: @file1 @file2

Analyze...
```

**用于：** 知情决策

## 编写简单命令的技巧

1. **从简单开始：** 单一职责，清晰目的
2. **逐渐增加复杂性：** 从无 frontmatter 开始
3. **增量测试：** 验证每个功能工作
4. **使用描述性名称：** 命令名称应表示目的
5. **记录参数：** 始终使用 argument-hint
6. **提供示例：** 在注释中显示用法
7. **处理错误：** 考虑缺失的参数或文件
