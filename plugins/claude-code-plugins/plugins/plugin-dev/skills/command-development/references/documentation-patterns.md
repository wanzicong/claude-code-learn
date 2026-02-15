# 命令文档模式

创建自说明、可维护且具有出色用户体验的命令的策略。

## 概述

文档完善的命令更易于使用、维护和分发。文档应嵌入在命令本身中，使用户和维护者可以立即访问。

## 自说明命令结构

### 完整命令模板

```markdown
---
description: Clear, actionable description under 60 chars
argument-hint: [arg1] [arg2] [optional-arg]
allowed-tools: Read, Bash(git:*)
model: sonnet
---

<!--
COMMAND: command-name
VERSION: 1.0.0
AUTHOR: Team Name
LAST UPDATED: 2025-01-15

PURPOSE:
Detailed explanation of what this command does and why it exists.

USAGE:
  /command-name arg1 arg2

ARGUMENTS:
  arg1: Description of first argument (required)
  arg2: Description of second argument (optional, defaults to X)

EXAMPLES:
  /command-name feature-branch main
    → Compares feature-branch with main

  /command-name my-branch
    → Compares my-branch with current branch

REQUIREMENTS:
  - Git repository
  - Branch must exist
  - Permissions to read repository

RELATED COMMANDS:
  /other-command - Related functionality
  /another-command - Alternative approach

TROUBLESHOOTING:
  - If branch not found: Check branch name spelling
  - If permission denied: Check repository access

CHANGELOG:
  v1.0.0 (2025-01-15): Initial release
  v0.9.0 (2025-01-10): Beta version
-->

# Command Implementation

[Command prompt content here...]

[Explain what will happen...]

[Guide user through steps...]

[Provide clear output...]
```

### 文档注释部分

**PURPOSE(目的)**: 命令存在的原因
- 解决的问题
- 使用场景
- 何时使用与何时不使用

**USAGE(用法)**: 基本语法
- 命令调用模式
- 必需参数与可选参数
- 默认值

**ARGUMENTS(参数)**: 详细的参数文档
- 每个参数的描述
- 类型信息
- 有效值/范围
- 默认值

**EXAMPLES(示例)**: 具体的使用示例
- 常见用例
- 边界情况
- 预期输出

**REQUIREMENTS(要求)**: 前置条件
- 依赖项
- 权限
- 环境设置

**RELATED COMMANDS(相关命令)**: 关联
- 类似命令
- 互补命令
- 替代方法

**TROUBLESHOOTING(故障排除)**: 常见问题
- 已知问题
- 解决方案
- 变通方法

**CHANGELOG(更新日志)**: 版本历史
- 何时更改了什么
- 突出重大更改
- 迁移指南

## 内联文档模式

### 带注释的部分

```markdown
---
description: Complex multi-step command
---

<!-- SECTION 1: VALIDATION -->
<!-- This section checks prerequisites before proceeding -->

Checking prerequisites...
- Git repository: !`git rev-parse --git-dir 2>/dev/null`
- Branch exists: [validation logic]

<!-- SECTION 2: ANALYSIS -->
<!-- Analyzes the differences between branches -->

Analyzing differences between $1 and $2...
[Analysis logic...]

<!-- SECTION 3: RECOMMENDATIONS -->
<!-- Provides actionable recommendations -->

Based on analysis, recommend:
[Recommendations...]

<!-- END: Next steps for user -->
```

### 内联说明

```markdown
---
description: Deployment command with inline docs
---

# Deploy to $1

## Pre-flight Checks

<!-- We check branch status to prevent deploying from wrong branch -->
Current branch: !`git branch --show-current`

<!-- Production deploys must come from main/master -->
if [ "$1" = "production" ] && [ "$(git branch --show-current)" != "main" ]; then
  ⚠️  WARNING: Not on main branch for production deploy
  This is unusual. Confirm this is intentional.
fi

<!-- Test status ensures we don't deploy broken code -->
Running tests: !`npm test`

✓ All checks passed

## Deployment

<!-- Actual deployment happens here -->
<!-- Uses blue-green strategy for zero-downtime -->
Deploying to $1 environment...
[Deployment steps...]

<!-- Post-deployment verification -->
Verifying deployment health...
[Health checks...]

Deployment complete!

## Next Steps

<!-- Guide user on what to do after deployment -->
1. Monitor logs: /logs $1
2. Run smoke tests: /smoke-test $1
3. Notify team: /notify-deployment $1
```

### 决策点文档

```markdown
---
description: Interactive deployment command
---

# Interactive Deployment

## Configuration Review

Target: $1
Current version: !`cat version.txt`
New version: $2

<!-- DECISION POINT: User confirms configuration -->
<!-- This pause allows user to verify everything is correct -->
<!-- We can't automatically proceed because deployment is risky -->

Review the above configuration.

**Continue with deployment?**
- Reply "yes" to proceed
- Reply "no" to cancel
- Reply "edit" to modify configuration

[Await user input before continuing...]

<!-- After user confirms, we proceed with deployment -->
<!-- All subsequent steps are automated -->

Proceeding with deployment...
```

## 帮助文本模式

### 内置帮助命令

为复杂命令创建帮助子命令:

```markdown
---
description: Main command with help
argument-hint: [subcommand] [args]
---

# Command Processor

if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  **Command Help**

  USAGE:
    /command [subcommand] [args]

  SUBCOMMANDS:
    init [name]       Initialize new configuration
    deploy [env]      Deploy to environment
    status            Show current status
    rollback          Rollback last deployment
    help              Show this help

  EXAMPLES:
    /command init my-project
    /command deploy staging
    /command status
    /command rollback

  For detailed help on a subcommand:
    /command [subcommand] --help

  Exit.
fi

[Regular command processing...]
```

### 上下文帮助

根据上下文提供帮助:

```markdown
---
description: Context-aware command
argument-hint: [operation] [target]
---

# Context-Aware Operation

if [ -z "$1" ]; then
  **No operation specified**

  Available operations:
  - analyze: Analyze target for issues
  - fix: Apply automatic fixes
  - report: Generate detailed report

  Usage: /command [operation] [target]

  Examples:
    /command analyze src/
    /command fix src/app.js
    /command report

  Run /command help for more details.

  Exit.
fi

[Command continues if operation provided...]
```

## 错误消息文档

### 有用的错误消息

```markdown
---
description: Command with good error messages
---

# Validation Command

if [ -z "$1" ]; then
  ❌ ERROR: Missing required argument

  The 'file-path' argument is required.

  USAGE:
    /validate [file-path]

  EXAMPLE:
    /validate src/app.js

  Try again with a file path.

  Exit.
fi

if [ ! -f "$1" ]; then
  ❌ ERROR: File not found: $1

  The specified file does not exist or is not accessible.

  COMMON CAUSES:
  1. Typo in file path
  2. File was deleted or moved
  3. Insufficient permissions

  SUGGESTIONS:
  - Check spelling: $1
  - Verify file exists: ls -la $(dirname "$1")
  - Check permissions: ls -l "$1"

  Exit.
fi

[Command continues if validation passes...]
```

### 错误恢复指南

```markdown
---
description: Command with recovery guidance
---

# Operation Command

Running operation...

!`risky-operation.sh`

if [ $? -ne 0 ]; then
  ❌ 操作失败

  操作遇到错误，无法完成。

  发生了什么:
  risky-operation.sh 脚本返回了非零退出代码。

  这意味着什么:
  - 更改可能部分应用
  - 系统可能处于不一致状态
  - 可能需要手动干预

  恢复步骤:
  1. 检查操作日志: cat /tmp/operation.log
  2. 验证系统状态: /check-state
  3. 如果需要，回滚: /rollback-operation
  4. 修复潜在问题
  5. 重试操作: /retry-operation

  需要帮助?
  - 查看故障排除指南: /help troubleshooting
  - 联系支持并提供错误代码: ERR_OP_FAILED_001

  Exit.
fi
```

## 使用示例文档

### 嵌入式示例

```markdown
---
description: Command with embedded examples
---

# Feature Command

This command performs feature analysis with multiple options.

## Basic Usage

\`\`\`
/feature analyze src/
\`\`\`

Analyzes all files in src/ directory for feature usage.

## Advanced Usage

\`\`\`
/feature analyze src/ --detailed
\`\`\`

Provides detailed analysis including:
- Feature breakdown by file
- Usage patterns
- Optimization suggestions

## Use Cases

**Use Case 1: Quick overview**
\`\`\`
/feature analyze .
\`\`\`
Get high-level feature summary of entire project.

**Use Case 2: Specific directory**
\`\`\`
/feature analyze src/components
\`\`\`
Focus analysis on components directory only.

**Use Case 3: Comparison**
\`\`\`
/feature analyze src/ --compare baseline.json
\`\`\`
Compare current features against baseline.

---

Now processing your request...

[Command implementation...]
```

### 示例驱动的文档

```markdown
---
description: Example-heavy command
---

# Transformation Command

## What This Does

Transforms data from one format to another.

## Examples First

### Example 1: JSON to YAML
**Input:** `data.json`
\`\`\`json
{"name": "test", "value": 42}
\`\`\`

**Command:** `/transform data.json yaml`

**Output:** `data.yaml`
\`\`\`yaml
name: test
value: 42
\`\`\`

### Example 2: CSV to JSON
**Input:** `data.csv`
\`\`\`csv
name,value
test,42
\`\`\`

**Command:** `/transform data.csv json`

**Output:** `data.json`
\`\`\`json
[{"name": "test", "value": "42"}]
\`\`\`

### Example 3: With Options
**Command:** `/transform data.json yaml --pretty --sort-keys`

**Result:** Formatted YAML with sorted keys

---

## Your Transformation

File: $1
Format: $2

[Perform transformation...]
```

## 维护文档

### 版本和更新日志

```markdown
<!--
VERSION: 2.1.0
LAST UPDATED: 2025-01-15
AUTHOR: DevOps Team

CHANGELOG:
  v2.1.0 (2025-01-15):
    - Added support for YAML configuration
    - Improved error messages
    - Fixed bug with special characters in arguments

  v2.0.0 (2025-01-01):
    - BREAKING: Changed argument order
    - BREAKING: Removed deprecated --old-flag
    - Added new validation checks
    - Migration guide: /migration-v2

  v1.5.0 (2024-12-15):
    - Added --verbose flag
    - Improved performance by 50%

  v1.0.0 (2024-12-01):
    - Initial stable release

MIGRATION NOTES:
  From v1.x to v2.0:
    Old: /command arg1 arg2 --old-flag
    New: /command arg2 arg1

  The --old-flag is removed. Use --new-flag instead.

DEPRECATION WARNINGS:
  - The --legacy-mode flag is deprecated as of v2.1.0
  - Will be removed in v3.0.0 (estimated 2025-06-01)
  - Use --modern-mode instead

KNOWN ISSUES:
  - #123: Slow performance with large files (workaround: use --stream flag)
  - #456: Special characters in Windows (fix planned for v2.2.0)
-->
```

### 维护说明

```markdown
<!--
MAINTENANCE NOTES:

CODE STRUCTURE:
  - Lines 1-50: Argument parsing and validation
  - Lines 51-100: Main processing logic
  - Lines 101-150: Output formatting
  - Lines 151-200: Error handling

DEPENDENCIES:
  - Requires git 2.x or later
  - Uses jq for JSON processing
  - Needs bash 4.0+ for associative arrays

PERFORMANCE:
  - Fast path for small inputs (< 1MB)
  - Streams large files to avoid memory issues
  - Caches results in /tmp for 1 hour

SECURITY CONSIDERATIONS:
  - Validates all inputs to prevent injection
  - Uses allowed-tools to limit Bash access
  - No credentials in command file

TESTING:
  - Unit tests: tests/command-test.sh
  - Integration tests: tests/integration/
  - Manual test checklist: tests/manual-checklist.md

FUTURE IMPROVEMENTS:
  - TODO: Add support for TOML format
  - TODO: Implement parallel processing
  - TODO: Add progress bar for large files

RELATED FILES:
  - lib/parser.sh: Shared parsing logic
  - lib/formatter.sh: Output formatting
  - config/defaults.yml: Default configuration
-->
```

## README 文档

命令应该有配套的 README 文件:

```markdown
# Command Name

Brief description of what the command does.

## Installation

This command is part of the [plugin-name] plugin.

Install with:
\`\`\`
/plugin install plugin-name
\`\`\`

## Usage

Basic usage:
\`\`\`
/command-name [arg1] [arg2]
\`\`\`

## Arguments

- `arg1`: Description (required)
- `arg2`: Description (optional, defaults to X)

## Examples

### Example 1: Basic Usage
\`\`\`
/command-name value1 value2
\`\`\`

Description of what happens.

### Example 2: Advanced Usage
\`\`\`
/command-name value1 --option
\`\`\`

Description of advanced feature.

## Configuration

Optional configuration file: `.claude/command-name.local.md`

\`\`\`markdown
---
default_arg: value
enable_feature: true
---
\`\`\`

## Requirements

- Git 2.x or later
- jq (for JSON processing)
- Node.js 14+ (optional, for advanced features)

## Troubleshooting

### Issue: Command not found

**Solution:** Ensure plugin is installed and enabled.

### Issue: Permission denied

**Solution:** Check file permissions and allowed-tools setting.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - See [LICENSE](LICENSE).

## Support

- Issues: https://github.com/user/plugin/issues
- Docs: https://docs.example.com
- Email: support@example.com
```

## 最佳实践

### 文档原则

1. **为未来的自己编写**: 假设你会忘记细节
2. **示例先于解释**: 先展示，再说明
3. **渐进式披露**: 基本信息优先，详细信息可用
4. **保持更新**: 代码更改时更新文档
5. **测试文档**: 验证示例确实有效

### 文档位置

1. **在命令文件中**: 核心用法、示例、内联说明
2. **README**: 安装、配置、故障排除
3. **单独文档**: 详细指南、教程、API 参考
4. **注释**: 维护者的实现细节

### 文档风格

1. **清晰简洁**: 没有多余的词
2. **主动语态**: "运行命令"而不是"命令可以被运行"
3. **术语一致**: 全文使用相同术语
4. **格式良好**: 使用标题、列表、代码块
5. **易于理解**: 假设读者是初学者

### 文档维护

1. **版本化所有内容**: 跟踪何时更改了什么
2. **优雅地弃用**: 在删除功能之前发出警告
3. **迁移指南**: 帮助用户升级
4. **归档旧文档**: 保持旧版本可访问
5. **定期审查**: 确保文档与实际情况匹配

## 文档检查清单

发布命令之前:

- [ ] frontmatter 中的描述清晰
- [ ] argument-hint 记录所有参数
- [ ] 注释中的使用示例
- [ ] 显示常见用例
- [ ] 错误消息有帮助
- [ ] 文档化的要求
- [ ] 列出相关命令
- [ ] 维护更新日志
- [ ] 更新版本号
- [ ] 创建/更新 README
- [ ] 示例确实有效
- [ ] 故障排除部分完整

有了良好的文档，命令变得可以自助使用，减少支持负担并改善用户体验。
