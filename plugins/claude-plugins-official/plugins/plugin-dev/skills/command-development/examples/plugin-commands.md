# 插件命令示例

为 Claude Code 插件设计的命令的实用示例，展示插件特定模式和功能。

## 目录

1. [简单插件命令](#1-简单插件命令)
2. [基于脚本的分析](#2-基于脚本的分析)
3. [基于模板的生成](#3-基于模板的生成)
4. [多脚本工作流](#4-多脚本工作流)
5. [配置驱动的部署](#5-配置驱动的部署)
6. [Agent 集成](#6-agent-集成)
7. [Skill 集成](#7-skill-集成)
8. [多组件工作流](#8-多组件工作流)
9. [验证输入命令](#9-验证输入命令)
10. [环境感知命令](#10-环境感知命令)

---

## 1. 简单插件命令

**用例：** 使用插件脚本的基本命令

**文件：** `commands/analyze.md`

```markdown
---
description: Analyze code quality using plugin tools
argument-hint: [file-path]
allowed-tools: Bash(node:*), Read
---

Analyze @$1 using plugin's quality checker:

!`node ${CLAUDE_PLUGIN_ROOT}/scripts/quality-check.js $1`

Review => the analysis output and provide:
1. Summary of findings
2. Priority issues to address
3. Suggested improvements
4. Code quality score interpretation
```

**关键特性：**
- 使用 `${CLAUDE_PLUGIN_ROOT}` 实现可移植路径
- 结合文件引用和脚本执行
- 简单的单目的命令

---

## 2. 基于脚本的分析

**用例：** 使用多个插件脚本进行全面分析

**文件：** `commands/full-audit.md`

```markdown
---
description: Complete code audit using plugin suite
argument-hint: [directory]
allowed-tools: Bash(*)
model: sonnet
---

Running complete audit on $1:

**Security scan:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh $1`

**Performance analysis:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/perf-analyze.sh $1`

**Best practices check:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/best-practices.sh $1`

Analyze all results and create comprehensive report including:
- Critical issues requiring immediate attention
- Performance optimization opportunities
- Security vulnerabilities and fixes
- Overall health score and recommendations
```

**关键特性：**
- 多个脚本执行
- 有组织的输出部分
- 全面工作流
- 清晰的报结构

---

## 3. 基于模板的生成

**用例：** 遵循插件模板生成文档

**文件：** `commands/gen-api-docs.md`

```markdown
---
description: Generate API documentation from template
argument-hint: [api-file]
---

Template structure: @${CLAUDE_PLUGIN_ROOT}/templates/api-documentation.md

API implementation: @$1

Generate complete API documentation following the template format above.

Ensure documentation includes:
- Endpoint descriptions with HTTP methods
- Request/response schemas
- Authentication requirements
- Error codes and handling
- Usage examples with curl commands
- Rate limiting information

Format output as markdown suitable for README or docs site.
```

**关键特性：**
- 使用插件模板
- 结合模板和源文件
- 标准化输出格式
- 清晰的文档结构

---

## 4. 多脚本工作流

**用例：** 协调构建、测试和部署工作流

**文件：** `commands/release.md`

```markdown
---
description: Execute complete release workflow
argument-hint: [version]
allowed-tools: Bash(*), Read
---

Executing release workflow for version $1:

**Step 1 - Pre-release validation:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/pre-release-check.sh $1`

**Step 2 - Build artifacts:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build-release.sh $1`

**Step 3 - Run test suite:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh`

**Step 4 - Package release:**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/package.sh $1`

Review all step outputs and report:
1. Any failures or warnings
2. Build artifacts location
3. Test results summary
4. Next steps for deployment
5. Rollback plan if needed
```

**关键特性：**
- 多步工作流
- 顺序脚本执行
- 清晰的步骤编号
- 全面报告

---

## 5. 配置驱动的部署

**用例：** 使用环境特定的插件配置进行部署

**文件：** `commands/deploy.md`

```markdown
---
description: Deploy application to environment
argument-hint: [environment]
allowed-tools: Read, Bash(*)
---

Deployment configuration for $1: @${CLAUDE_PLUGIN_ROOT}/config/$1-deploy.json

Current git state: !`git rev-parse --short HEAD`

Build info: !`cat package.json | grep -E '(name|version)'`

Execute deployment to $1 environment using configuration above.

Deployment checklist:
1. Validate configuration settings
2. Build application for $1
3. Run pre-deployment tests
4. Deploy to target environment
5. Run smoke tests
6. Verify deployment success
7. Update deployment log

Report deployment status and any issues encountered.
```

**关键特性：**
- 环境特定配置
- 动态配置文件加载
- 部署前验证
- 结构化检查清单

---

## 6. Agent 集成

**用例：** 启动插件 agent 完成复杂任务的命令

**文件：** `commands/deep-review.md`

```markdown
---
description: Deep code review using plugin agent
argument-hint: [file-or-directory]
---

Initiate comprehensive code review of @$1 using the code-reviewer agent.

The agent will perform:
1. **Static analysis** - Check for code smells and anti-patterns
2. **Security audit** - Identify potential vulnerabilities
3. **Performance review** - Find optimization opportunities
4. **Best practices** - Ensure code follows standards
5. **Documentation check** - Verify adequate documentation

The agent has access to:
- Plugin's linting rules: ${CLAUDE_PLUGIN_ROOT}/config/lint-rules.json
- Security checklist: ${CLAUDE_PLUGIN_ROOT}/checklists/security.md
- Performance guidelines: ${CLAUDE_PLUGIN_ROOT}/docs/performance.md

Note: This uses the Task tool to launch the plugin's code-reviewer agent for thorough analysis.
```

**关键特性：**
- 委托给插件 agent
- 记录 agent 功能
- 引用插件资源
- 清晰的范围定义

---

## 7. Skill 集成

**用例：** 利用插件 skill 获取专门知识的命令

**文件：** `commands/document-api.md`

```markdown
---
description: Document API following plugin standards
argument-hint: [api-file]
---

API source code: @$1

Generate API documentation following plugin's API documentation standards.

Use the api-documentation-standards skill to ensure:
- **OpenAPI compliance** - Follow OpenAPI 3.0 specification
- **Consistent formatting** - Use plugin's documentation style
- **Complete coverage** - Document all endpoints and schemas
- **Example quality** - Provide realistic usage examples
- **Error documentation** - Cover all error scenarios

The skill provides:
- Standard documentation templates
- API documentation best practices
- Common patterns for this codebase
- Quality validation criteria

Generate production-ready API docs.
```

**关键特性：**
- 按名称调用插件 skill
- 记录 skill 目的
- 清晰的期望
- 利用 skill 知识

---

## 8. 多组件工作流

**用例：** 使用 agents、skills 和 scripts 的复杂工作流

**文件：** `commands/complete-review.md`

```markdown
---
description: Comprehensive review using all plugin components
argument-hint: [file-path]
allowed-tools: Bash(node:*), Read
---

Target file: @$1

Execute comprehensive review workflow:

**Phase 1: Automated Analysis**
Run plugin analyzer: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js $1`

**Phase 2: Deep Review (Agent)**
Launch the code-quality-reviewer agent for detailed analysis.
Agent will examine:
- Code structure and organization
- Error handling patterns
- Testing coverage
- Documentation quality

**Phase 3: Standards Check (Skill)**
Use the coding-standards skill to validate:
- Naming conventions
- Code formatting
- Best practices adherence
- Framework-specific patterns

**Phase 4: Report Generation**
Template: @${CLAUDE_PLUGIN_ROOT}/templates/review-report.md

Compile all findings into comprehensive report following template.

**Phase 5: Recommendations**
Generate prioritized action items:
1. Critical issues (must fix)
2. Important improvements (should fix)
3. Nice-to-have enhancements (could fix)

Include specific file locations and suggested changes for each item.
```

**关键特性：**
- 多阶段工作流
- 结合 scripts、agents、skills
- 基于模板的报告
- 优先级输出

---

## 9. 验证输入命令

**用例：** 带有输入验证和错误处理的命令

**文件：** `commands/build-env.md`

```markdown
---
description: Build for specific environment with validation
argument-hint: [environment]
allowed-tools: Bash(*)
---

Validate environment argument: !`echo "$1" | grep -E "^(dev|staging|prod)$" && echo "VALID" || echo "INVALID"`

Check build script exists: !`test -x ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh && echo "EXISTS" || echo "MISSING"`

Verify configuration available: !`test -f ${CLAUDE_PLUGIN_ROOT}/config/$1.json && echo "FOUND" || echo "NOT_FOUND"`

If all validations pass:

**Configuration:** @${CLAUDE_PLUGIN_ROOT}/config/$1.json

**Execute build:** !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh $1 2>&1`

**Validation results:** !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-build.sh $1 2>&1`

Report build status and any issues.

If validations fail:
- Explain which validation failed
- Provide expected values/locations
- Suggest corrective actions
- Document troubleshooting steps
```

**关键特性：**
- 输入验证
- 资源存在检查
- 错误处理
- 有用的错误消息
- 优雅的失败处理

---

## 10. 环境感知命令

**用例：** 根据环境调整行为的命令

**文件：** `commands/run-checks.md`

```markdown
---
description: Run environment-appropriate checks
argument-hint: [environment]
allowed-tools: Bash(*), Read
---

Environment: $1

Load environment configuration: @${CLAUDE_PLUGIN_ROOT}/config/$1-checks.json

Determine check level: !`echo "$1" | grep -E "^prod$" && echo "FULL" || echo "BASIC"`

**For production environment:**
- Full test suite: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test-full.sh`
- Security scan: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh`
- Performance audit: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/perf-check.sh`
- Compliance check: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/compliance.sh`

**For non-production environments:**
- Basic tests: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test-basic.sh`
- Quick lint: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh`

Analyze results based on environment requirements:

**Production:** All checks must pass with zero critical issues
**Staging:** No critical issues, warnings acceptable
**Development:** Focus on blocking issues only

Report status and recommend proceed/block decision.
```

**关键特性：**
- 环境感知逻辑
- 条件执行
- 不同的验证级别
- 适合环境的报告

---

## 常见模式摘要

### 模式：插件脚本执行
```markdown
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/script-name.js $1`
```
用于：运行插件提供的 Node.js 脚本

### 模式：插件配置加载
```markdown
@${CLAUDE_PLUGIN_ROOT}/config/config-name.json
```
用于：加载插件配置文件

### 模式：插件模板使用
```markdown
@${CLAUDE_PLUGIN_ROOT}/templates/template-name.md
```
用于：使用插件模板进行生成

### 模式：Agent 调用
```markdown
Launch the [agent-name] agent for [task description].
```
用于：将复杂任务委派给插件 agents

### 模式：Skill 引用
```markdown
Use the [skill-name] skill to ensure [requirements].
```
用于：利用插件 skills 获取专门知识

### 模式：输入验证
```markdown
Validate input: !`echo "$1" | grep -E "^pattern$" && echo "OK" || echo "ERROR"`
```
用于：验证命令参数

### 模式：资源验证
```markdown
Check exists: !`test -f ${CLAUDE_PLUGIN_ROOT}/path/file && echo "YES" || echo "NO"`
```
用于：验证所需插件文件存在

---

## 开发技巧

### 测试插件命令

1. **使用插件安装进行测试：**
   ```bash
   cd /path/to/plugin
   claude /command-name args
   ```

2. **验证 ${CLAUDE_PLUGIN_ROOT} 展开：**
   ```bash
   # 向命令添加调试输出
   !`echo "Plugin root: ${CLAUDE_PLUGIN_ROOT}"`
   ```

3. **跨不同工作目录测试：**
   ```bash
   cd /tmp && claude /command-name
   cd /other/project && claude /command-name
   ```

4. **验证资源可用性：**
   ```bash
   # 检查所有插件资源存在
   !`ls -la ${CLAUDE_PLUGIN_ROOT}/scripts/`
   !`ls -la ${CLAUDE_PLUGIN_ROOT}/config/`
   ```

### 避免的常见错误

1. **使用相对路径而不是 ${CLAUDE_PLUGIN_ROOT}：**
   ```markdown
   # 错误
   !`node ./scripts/analyze.js`

   # 正确
   !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js`
   ```

2. **忘记允许所需工具：**
   ```markdown
   # 缺少 allowed-tools
   !`bash script.sh`  # 没有 Bash 权限会失败

   # 正确
   ---
   allowed-tools: Bash(*)
   ---
   !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh`
   ```

3. **不验证输入：**
   ```markdown
   # 有风险 - 没有验证
   Deploy to $1 environment

   # 更好 - 带有验证
   Validate: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`
   Deploy to $1 environment (if valid)
   ```

4. **硬编码插件路径：**
   ```markdown
   # 错误 - 在不同安装上中断
   @/home/user/.claude/plugins/my-plugin/config.json

   # 正确 - 到处工作
   @${CLAUDE_PLUGIN_ROOT}/config.json
   ```

---

有关详细的插件特定功能，请参阅 `references/plugin-features-reference.md`。
有关通用命令开发，请参阅主 `SKILL.md`。
