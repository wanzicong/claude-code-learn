# 插件特定命令功能参考

本参考资料涵盖 Claude Code 插件中捆绑的命令所特有的功能和模式。

## 目录

- [插件命令发现](#插件命令发现)
- [CLAUDE_PLUGIN_ROOT 环境变量](#claudelpluginroot-环境变量)
- [插件命令模式](#插件命令模式)
- [与插件组件的集成](#与插件组件的集成)
- [验证模式](#验证模式)

## 插件命令发现

### 自动发现

Claude Code 使用以下位置从插件中自动发现命令：

```
plugin-name/
├── commands/              # 自动发现的命令
│   ├── foo.md            # /foo (plugin:plugin-name)
│   └── bar.md            # /bar (plugin:plugin-name)
└── plugin.json           # 插件清单
```

**关键点：**
- 命令在插件加载时发现
- 无需手动注册
- 命令在 `/help` 中以 "(plugin:plugin-name)" 标签显示
- 子目录创建命名空间

### 命名空间的插件命令

在子目录中组织命令以实现逻辑分组：

```
plugin-name/
└── commands/
    ├── review/
    │   ├── security.md    # /security (plugin:plugin-name:review)
    │   └── style.md       # /style (plugin:plugin-name:review)
    └── deploy/
        ├── staging.md     # /staging (plugin:plugin-name:deploy)
        └── prod.md        # /prod (plugin:plugin-name:deploy)
```

**命名空间行为：**
- 子目录名称成为命名空间
- 在 `/help` 中显示为 "(plugin:plugin-name:namespace)"
- 帮助组织相关命令
- 当插件有 5+ 个命令时使用

### 命令命名约定

**插件命令名称应该：**
1. 是描述性和面向操作的
2. 避免与常见命令名称冲突
3. 使用连字符命名多词名称
4. 考虑使用插件名称前缀以保证唯一性

**示例：**
```
好的：
- /mylyn-sync          （插件特定前缀）
- /analyze-performance （描述性操作）
- /docker-compose-up   （清晰的目的）

避免：
- /test               （与常见名称冲突）
- /run                （太通用）
- /do-stuff           （不具描述性）
```

## CLAUDE_PLUGIN_ROOT 环境变量

### 用途

`${CLAUDE_PLUGIN_ROOT}` 是一个特殊的环境变量，在插件命令中可用，解析为插件目录的绝对路径。

**为什么重要：**
- 允许插件内的可移植路径
- 允许引用插件文件和脚本
- 在不同安装之间工作
- 对于多文件插件操作必不可少

### 基本用法

在插件中引用文件：

```markdown
---
description: Analyze using plugin script
allowed-tools: Bash(node:*), Read
---

Run analysis: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js`

Read template: @${CLAUDE_PLUGIN_ROOT}/templates/report.md
```

**展开为：**
```
Run analysis: !`node /path/to/plugins/plugin-name/scripts/analyze.js`
Read template: @/path/to/plugins/plugin-name/templates/report.md
```

### 常见模式

#### 1. 执行插件脚本

```markdown
---
description: Run custom linter from plugin
allowed-tools: Bash(node:*)
---

Lint results: !`node ${CLAUDE_PLUGIN_ROOT}/bin/lint.js $1`

Review => => linting output and suggest fixes.
```

#### 2. 加载配置文件

```markdown
---
description: Deploy using plugin configuration
allowed-tools: Read, Bash(*)
---

Configuration: @${CLAUDE_PLUGIN_ROOT}/config/deploy-config.json

Deploy application using => => configuration above for $1 environment.
```

#### 3. 访问插件资源

```markdown
---
description: Generate report from template
---

Use this template: @${CLAUDE_PLUGIN_ROOT}/templates/api-report.md

Generate a report for @$1 following => => template format.
```

#### 4. 多步插件工作流

```markdown
---
description: Complete plugin workflow
allowed-tools: Bash(*), Read
---

Step 1 - Prepare: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/prepare.sh $1`
Step 2 - Config: @${CLAUDE_PLUGIN_ROOT}/config/$1.json
Step 3 - Execute: !`${CLAUDE_PLUGIN_ROOT}/bin/execute $1`

Review results and report status.
```

### 最佳实践

1. **始终使用 ${CLAUDE_PLUGIN_ROOT} 获取插件内部路径：**
   ```markdown
   # 好的
   @${CLAUDE_PLUGIN_ROOT}/templates/foo.md

   # 不好的
   @./templates/foo.md  # 相对于当前目录，而非插件
   ```

2. **验证文件存在：**
   ```markdown
   ---
   description: Use plugin config if exists
   allowed-tools: Bash(test:*), Read
   ---

   !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "exists" || echo "missing"`

   If config exists, load it: @${CLAUDE_PLUGIN_ROOT}/config.json
   Otherwise, use defaults...
   ```

3. **记录插件文件结构：**
   ```markdown
   <!--
   插件结构：
   ${CLAUDE_PLUGIN_ROOT}/
   ├── scripts/analyze.js  （分析脚本）
   ├── templates/          （报告模板）
   └── config/             （配置文件）
   -->
   ```

4. **与参数结合：**
   ```markdown
   Run: !`${CLAUDE_PLUGIN_ROOT}/bin/process.sh $1 $2`
   ```

###   故障排除

**变量未展开：**
- 确保命令从插件加载
- 检查是否允许 bash 执行
- 验证语法完全正确：`${CLAUDE_PLUGIN_ROOT}`

**未找到文件错误：**
- 验证文件存在于插件目录中
- 检查文件路径相对于插件根目录正确
- 确保文件权限允许读取/执行

**路径包含空格：**
- Bash 命令自动处理空格
- 文件引用在包含空格的路径下工作
- 不需要特殊引号

## 插件命令模式

### 模式 1：基于配置的命令

加载插件特定配置的命令：

```markdown
---
description: Deploy using plugin settings
allowed-tools: Read, Bash(*)
---

Load configuration: @${CLAUDE_PLUGIN_ROOT}/deploy-config.json

Deploy to $1 environment using:
1. Configuration settings above
2. Current git branch: !`git branch --show-current`
3. Application version: !`cat package.json | grep version`

Execute deployment and monitor progress.
```

**使用时机：** 需要在调用之间保持一致设置的命令

### 模式 2：基于模板的生成

使用插件模板的命令：

```markdown
---
description: Generate documentation from template
argument-hint: [component-name]
---

Template: @${CLAUDE_PLUGIN_ROOT}/templates/component-docs.md

Generate documentation for $1 component following => => template structure.

Include:
- Component purpose and usage
- API reference
- Examples
- Testing guidelines
```

**使用时机：** 标准化输出生成

### 模式 3：多脚本工作流

编排多个插件脚本的命令：

```markdown
---
description: Complete build and test workflow
allowed-tools: Bash(*)
---

Build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh`
Validate: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh`
Test: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test.sh`

Review all outputs and report:
1. Build status
2. Validation results
3. Test results
4. Recommended next steps
```

**使用时机：** 具有多个步骤的复杂插件工作流

### 模式 4：环境感知命令

根据环境适应的命令：

```markdown
---
description: Deploy based on environment
argument-hint: [dev|staging|prod]
---

Environment config: @${CLAUDE_PLUGIN_ROOT}/config/$1.json

Environment check: !`echo "Deploying to: $1"`

Deploy application using $1 environment configuration.
Verify deployment and run smoke tests.
```

**使用时机：** 在不同环境表现不同的命令

### 模式 5：插件数据管理

管理插件特定数据的命令：

```markdown
---
description: Save analysis results to plugin cache
allowed-tools: Bash(*), Read, Write
---

Cache directory: ${CLAUDE_PLUGIN_ROOT}/cache/

Analyze @$1 and save results to cache:
!`mkdir -p ${CLAUDE_PLUGIN_ROOT}/cache && date > ${CLAUDE_PLUGIN_ROOT}/cache/last-run.txt`

Store analysis for future reference and comparison.
```

**使用时机：** 需要持久化数据存储的命令

## 与插件组件的集成

### 调用插件代理

命令可以使用 Task 工具触发插件代理：

```markdown
---
description: Deep analysis using plugin agent
argument-hr: [file-path]
---

Initiate deep code analysis of @$1 using => => code-analyzer agent.

The agent will:
1. Analyze code structure
2. Identify patterns
3. Suggest improvements
4. Generate detailed report

Note: This uses => => Task tool to launch plugin's code-analyzer agent.
```

**关键点：**
- Agent 必须在插件的 `agents/` 目录中定义
- Claude 将自动使用 Task 工具启动 agent
- Agent 拥有访问相同插件资源

### 调用插件技能

命令可以引用插件技能以获取专门知识：

```markdown
---
description: API documentation with best practices
argument-hr: [api-file]
---

Document API in @$1 following our API documentation standards.

Use => => api-docs-standards skill to ensure documentation includes:
- Endpoint descriptions
- Parameter specifications
- Response formats
- Error codes
- Usage examples

Note: This leverages => => plugin's api-docs-standards skill for consistency.
```

**关键点：**
- Skill 必须在插件的 `skills/` 目录中定义
- 提及 skill 名称以提示 Claude 应该调用它
- Skills 提供专门的领域知识

### 与插件钩子协调

命令可以设计为与插件钩子一起工作：

```markdown
---
description: Commit with pre-commit validation
allowed-tools: Bash(git:*)
---

Stage changes: !\`git add $1\`

Commit changes: !\`git commit -m "$2"\`

Note: This commit will trigger => => plugin's pre-commit hook for validation.
Review hook output for any issues.
```

**关键点：**
- Hooks 在事件上自动执行
- 命令可以为 hooks 准备状态
- 在命令中记录 hook 交互
- 指导 Claude 解释 hook 输出

### 多组件插件命令

协调多个插件组件的命令：

```markdown
---
description: Comprehensive code review workflow
argument-hr: [file-path]
---

File to review: @$1

Execute comprehensive review:

1. **Static Analysis** (via plugin scripts)
   !`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

2. **Deep Review** (via plugin agent)
   Launch => => code-reviewer agent for detailed analysis.

3. **Best Practices** (via plugin skill)
   Use => => code-standards skill to ensure compliance.

4. **Documentation** (via plugin template)
   Template: @${CLAUDE_PLUGIN_ROOT}/templates/review-report.md

Generate final report combining all outputs.
```

**使用时机：** 利用多个插件功能的复杂工作流

## 验证模式

### 输入验证

命令应在处理之前验证输入：

```markdown
---
description: Deploy to environment with validation
argument-hr: [environment]
---

Validate environment: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`

$IF($1 in [dev, staging, prod],
  Deploy to $1 environment using validated configuration,
  ERROR: Invalid environment '$1'. Must be one of: dev, staging, prod
)
```

**验证方法：**
1. 使用 grep/test 进行 Bash 验证
2. 在提示中进行内联验证
3. 基于脚本的验证

### 文件存在检查

验证所需文件存在：

```markdown
---
description: Process configuration file
argument-hr: [config-file]
---

Check file: !`test -f $1 && echo "EXISTS" || echo "MISSING"`

Process configuration if file exists: @$1

If file doesn't exist, explain:
- Expected location
- Required format
- How to create it
```

### 必需参数

验证提供了所需参数：

```markdown
---
description: Create deployment with version
argument-hr: [environment] [version]
---

Validate inputs: !`test -n "$1" -a -n "$2" && echo "OK" || echo "MISSING"`

$IF($1 AND $2,
  Deploy version $2 to $1 environment,
  ERROR: Both environment and version required. Usage: /deploy [env] [version]
)
```

### 插件资源验证

验证插件资源可用：

```markdown
---
description: Run analysis with plugin tools
allowed-tools: Bash(test:*)
---

Validate plugin setup:
- Config exists: !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "✓" || echo "✗"`
- Scripts exist: !`test -d ${CLAUDE_PLUGIN_ROOT}/scripts && echo "✓" || echo "✗"`
- Tools available: !`test -x ${CLAUDE_PLUGIN_ROOT}/bin/analyze && echo "✓" || echo "✗"`

If all checks pass, proceed with analysis.
Otherwise, report missing components and installation steps.
```

### 输出验证

验证命令执行结果：

```markdown
---
description: Build and validate output
allowed-tools: Bash(*)
---

Build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh`

Validate output:
- Exit code: !`echo $?`
- Output exists: !`test -d dist && echo "✓" || echo "✗"`
- File count: !`find dist -type f | wc -l`

Report build status and any validation failures.
```

### 优雅的错误处理

使用有用的消息优雅地处理错误：

```markdown
---
description: Process file with error handling
argument-hr: [file-path]
---

Try processing: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/process.js $1 2>&1 || echo "ERROR: $?"`

If processing succeeded:
- Report results
- Suggest next steps

If processing failed:
- Explain likely causes
- Provide troubleshooting steps
- Suggest alternative approaches
```

## 最佳实践摘要

### 插件命令应该：

1. **对所有插件内部路径使用 ${CLAUDE_PLUGIN_ROOT}**
   - 脚本、配置、资源
2. **尽早验证输入**
   - 检查所需参数
   - 验证文件存在
   - 验证参数格式
3. **记录插件结构**
   - 解释所需文件
   - 记录脚本目的
   - 澄清依赖关系
4. **与插件组件集成**
   - 引用 agents 处理复杂任务
   - 使用 skills 获取专门知识
   - 与 hooks 协调相关内容
5. **提供有用的错误消息**
   - 解释什么出错了
   - 建议如何修复
   - 提供替代方案
6. **处理边缘情况**
   - 缺失的文件
   - 无效的参数
   - 脚本执行失败
   - 缺少依赖
7. **保持命令专注**
   - 每个命令有清晰的目的
   - 将复杂逻辑委派给脚本
   - 使用 agents 处理多步工作流
8. **跨安装测试**
   - 验证路径在任何地方工作
   - 使用不同参数测试
   - 验证错误情况

---

有关通用命令开发，请参阅主 SKILL.md。
有关命令示例，请参阅 examples/ 目录。
