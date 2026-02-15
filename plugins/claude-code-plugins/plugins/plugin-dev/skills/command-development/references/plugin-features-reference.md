# 插件特定命令功能参考

本参考涵盖了 Claude Code 插件中捆绑的命令特定的功能和模式。

## 目录

- [插件命令发现](#plugin-command-discovery)
- [CLAUDE_PLUGIN_ROOT 环境变量](#claude_plugin_root-environment-variable)
- [插件命令模式](#plugin-command-patterns)
- [与插件组件的集成](#integration-with-plugin-components)
- [验证模式](#validation-patterns)

## 插件命令发现

### 自动发现

Claude Code 使用以下位置自动发现插件中的命令:

```
plugin-name/
├── commands/              # Auto-discovered commands
│   ├── foo.md            # /foo (plugin:plugin-name)
│   └── bar.md            # /bar (plugin:plugin-name)
└── plugin.json           # Plugin manifest
```

**关键点:**
- 命令在插件加载时发现
- 无需手动注册
- 命令在 `/help` 中显示为 "(plugin:plugin-name)" 标签
- 子目录创建命名空间

### 命名空间插件命令

在子目录中组织命令以进行逻辑分组:

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

**命名空间行为:**
- 子目录名称成为命名空间
- 在 `/help` 中显示为 "(plugin:plugin-name:namespace)"
- 帮助组织相关命令
- 当插件有5个以上命令时使用

### 命令命名约定

**插件命令名称应该:**
1. 具有描述性和面向操作
2. 避免与常见命令名称冲突
3. 对多词名称使用连字符
4. 考虑使用插件名称前缀以确保唯一性

**Examples:**
```
Good:
- /mylyn-sync          (plugin-specific prefix)
- /analyze-performance (descriptive action)
- /docker-compose-up   (clear purpose)

Avoid:
- /test               (conflicts with common name)
- /run                (too generic)
- /do-stuff           (not descriptive)
```

## CLAUDE_PLUGIN_ROOT 环境变量

### 目的

`${CLAUDE_PLUGIN_ROOT}` 是插件命令中可用的特殊环境变量，解析为插件目录的绝对路径。

**为什么重要:**
- 在插件内启用可移植路径
- 允许引用插件文件和脚本
- 跨不同安装工作
- 对多文件插件操作至关重要

### 基本用法

引用插件内的文件:

```markdown
---
description: Analyze using plugin script
allowed-tools: Bash(node:*), Read
---

Run analysis: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js`

Read template: @${CLAUDE_PLUGIN_ROOT}/templates/report.md
```

**Expands to:**
```
Run analysis: !`node /path/to/plugins/plugin-name/scripts/analyze.js`

Read template: @/path/to/plugins/plugin-name/templates/report.md
```

### Common Patterns

#### 1. Executing Plugin Scripts

```markdown
---
description: Run custom linter from plugin
allowed-tools: Bash(node:*)
---

Lint results: !`node ${CLAUDE_PLUGIN_ROOT}/bin/lint.js $1`

Review the linting output and suggest fixes.
```

#### 2. Loading Configuration Files

```markdown
---
description: Deploy using plugin configuration
allowed-tools: Read, Bash(*)
---

Configuration: @${CLAUDE_PLUGIN_ROOT}/config/deploy-config.json

Deploy application using the configuration above for $1 environment.
```

#### 3. Accessing Plugin Resources

```markdown
---
description: Generate report from template
---

Use this template: @${CLAUDE_PLUGIN_ROOT}/templates/api-report.md

Generate a report for @$1 following the template format.
```

#### 4. Multi-Step Plugin Workflows

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

### Best Practices

1. **Always use for plugin-internal paths:**
   ```markdown
   # Good
   @${CLAUDE_PLUGIN_ROOT}/templates/foo.md

   # Bad
   @./templates/foo.md  # Relative to current directory, not plugin
   ```

2. **Validate file existence:**
   ```markdown
   ---
   description: Use plugin config if exists
   allowed-tools: Bash(test:*), Read
   ---

   !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "exists" || echo "missing"`

   If config exists, load it: @${CLAUDE_PLUGIN_ROOT}/config.json
   Otherwise, use defaults...
   ```

3. **Document plugin file structure:**
   ```markdown
   <!--
   Plugin structure:
   ${CLAUDE_PLUGIN_ROOT}/
   ├── scripts/analyze.js  (analysis script)
   ├── templates/          (report templates)
   └── config/             (configuration files)
   -->
   ```

4. **Combine with arguments:**
   ```markdown
   Run: !`${CLAUDE_PLUGIN_ROOT}/bin/process.sh $1 $2`
   ```

### Troubleshooting

**Variable not expanding:**
- Ensure command is loaded from plugin
- Check bash execution is allowed
- Verify syntax is exact: `${CLAUDE_PLUGIN_ROOT}`

**File not found errors:**
- Verify file exists in plugin directory
- Check file path is correct relative to plugin root
- Ensure file permissions allow reading/execution

**Path with spaces:**
- Bash commands automatically handle spaces
- File references work with spaces in paths
- No special quoting needed

## Plugin Command Patterns

### Pattern 1: Configuration-Based Commands

Commands that load plugin-specific configuration:

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

**When to use:** Commands that need consistent settings across invocations

### Pattern 2: Template-Based Generation

Commands that use plugin templates:

```markdown
---
description: Generate documentation from template
argument-hint: [component-name]
---

Template: @${CLAUDE_PLUGIN_ROOT}/templates/component-docs.md

Generate documentation for $1 component following the template structure.
Include:
- Component purpose and usage
- API reference
- Examples
- Testing guidelines
```

**When to use:** Standardized output generation

### Pattern 3: Multi-Script Workflow

Commands that orchestrate multiple plugin scripts:

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

**When to use:** Complex plugin workflows with multiple steps

### Pattern 4: Environment-Aware Commands

Commands that adapt to environment:

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

**When to use:** Commands that behave differently per environment

### Pattern 5: Plugin Data Management

Commands that manage plugin-specific data:

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

**When to use:** Commands that need persistent data storage

## Integration with Plugin Components

### Invoking Plugin Agents

Commands can trigger plugin agents using the Task tool:

```markdown
---
description: Deep analysis using plugin agent
argument-hint: [file-path]
---

Initiate deep code analysis of @$1 using the code-analyzer agent.

The agent will:
1. Analyze code structure
2. Identify patterns
3. Suggest improvements
4. Generate detailed report

Note: This uses the Task tool to launch the plugin's code-analyzer agent.
```

**Key points:**
- Agent must be defined in plugin's `agents/` directory
- Claude will automatically use Task tool to launch agent
- Agent has access to same plugin resources

### Invoking Plugin Skills

Commands can reference plugin skills for specialized knowledge:

```markdown
---
description: API documentation with best practices
argument-hint: [api-file]
---

Document the API in @$1 following our API documentation standards.

Use the api-docs-standards skill to ensure documentation includes:
- Endpoint descriptions
- Parameter specifications
- Response formats
- Error codes
- Usage examples

Note: This leverages the plugin's api-docs-standards skill for consistency.
```

**Key points:**
- Skill must be defined in plugin's `skills/` directory
- Mention skill by name to hint Claude should invoke it
- Skills provide specialized domain knowledge

### Coordinating with Plugin Hooks

Commands can be designed to work with plugin hooks:

```markdown
---
description: Commit with pre-commit validation
allowed-tools: Bash(git:*)
---

Stage changes: !\`git add $1\`

Commit changes: !\`git commit -m "$2"\`

Note: This commit will trigger the plugin's pre-commit hook for validation.
Review hook output for any issues.
```

**Key points:**
- Hooks execute automatically on events
- Commands can prepare state for hooks
- Document hook interaction in command

### Multi-Component Plugin Commands

Commands that coordinate multiple plugin components:

```markdown
---
description: Comprehensive code review workflow
argument-hint: [file-path]
---

File to review: @$1

Execute comprehensive review:

1. **Static Analysis** (via plugin scripts)
   !`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

2. **Deep Review** (via plugin agent)
   Launch the code-reviewer agent for detailed analysis.

3. **Best Practices** (via plugin skill)
   Use the code-standards skill to ensure compliance.

4. **Documentation** (via plugin template)
   Template: @${CLAUDE_PLUGIN_ROOT}/templates/review-report.md

Generate final report combining all outputs.
```

**When to use:** Complex workflows leveraging multiple plugin capabilities

## Validation Patterns

### Input Validation

Commands should validate inputs before processing:

```markdown
---
description: Deploy to environment with validation
argument-hint: [environment]
---

Validate environment: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`

$IF($1 in [dev, staging, prod],
  Deploy to $1 environment using validated configuration,
  ERROR: Invalid environment '$1'. Must be one of: dev, staging, prod
)
```

**Validation approaches:**
1. Bash validation using grep/test
2. Inline validation in prompt
3. Script-based validation

### File Existence Checks

Verify required files exist:

```markdown
---
description: Process configuration file
argument-hint: [config-file]
---

Check file: !`test -f $1 && echo "EXISTS" || echo "MISSING"`

Process configuration if file exists: @$1

If file doesn't exist, explain:
- Expected location
- Required format
- How to create it
```

### Required Arguments

Validate required arguments provided:

```markdown
---
description: Create deployment with version
argument-hint: [environment] [version]
---

Validate inputs: !`test -n "$1" -a -n "$2" && echo "OK" || echo "MISSING"`

$IF($1 AND $2,
  Deploy version $2 to $1 environment,
  ERROR: Both environment and version required. Usage: /deploy [env] [version]
)
```

### Plugin Resource Validation

Verify plugin resources available:

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

### Output Validation

Validate command execution results:

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

### Graceful Error Handling

Handle errors gracefully with helpful messages:

```markdown
---
description: Process file with error handling
argument-hint: [file-path]
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

## Best Practices Summary

### Plugin Commands Should:

1. **Use ${CLAUDE_PLUGIN_ROOT} for all plugin-internal paths**
   - Scripts, templates, configuration, resources

2. **Validate inputs early**
   - Check required arguments
   - Verify file existence
   - Validate argument formats

3. **Document plugin structure**
   - Explain required files
   - Document script purposes
   - Clarify dependencies

4. **Integrate with plugin components**
   - Reference agents for complex tasks
   - Use skills for specialized knowledge
   - Coordinate with hooks when relevant

5. **Provide helpful error messages**
   - Explain what went wrong
   - Suggest how to fix
   - Offer alternatives

6. **Handle edge cases**
   - Missing files
   - Invalid arguments
   - Failed script execution
   - Missing dependencies

7. **Keep commands focused**
   - One clear purpose per command
   - Delegate complex logic to scripts
   - Use agents for multi-step workflows

8. **Test across installations**
   - Verify paths work everywhere
   - Test with different arguments
   - Validate error cases

---

For general command development, see main SKILL.md.
For command examples, see examples/ directory.
