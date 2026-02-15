---
name: Writing Hookify Rules
description: 当用户要求"创建 hookify 规则"、"编写钩子规则"、"配置 hookify"、"添加 hookify 规则"或需要有关 hookify 规则语法和模式的指导时，应使用此技能。
version: 0.1.0
---

# 编写 Hookify 规则

## 概述

Hookify 规则是带有 YAML 前置内容的 markdown 文件，用于定义要监视的模式和匹配这些模式时显示的消息。规则存储在 `.claude/hookify.{rule-name}.local.md` 文件中。

## 规则文件格式

### 基本结构

```markdown
---
name: rule-identifier
enabled: true
event: bash|file|stop|prompt|all
pattern: regex-pattern-here
---

此规则触发时向 Claude 显示的消息。
可以包含 markdown 格式、警告、建议等。
```

### 前置内容字段

**name**（必需）：规则的唯一标识符
- 使用 kebab-case：`warn-dangerous-rm`、`block-console-log`
- 要具有描述性和行动导向性
- 以动词开头：warn、prevent、block、require、check

**enabled**（必需）：布尔值以激活/停用
- `true`：规则处于活动状态
- `false`：规则已禁用（不会触发）
- 可以在不删除规则的情况下切换

**event**（必需）：要触发的钩子事件
- `bash`：Bash 工具命令
- `file`：Edit、Write、MultiEdit 工具
- `stop`：当代理想要停止时
- `prompt`：当用户提交提示时
- `all`：所有事件

**action**（可选）：规则匹配时要执行的操作
- `warn`：显示消息但允许操作（默认）
- `block`：阻止操作（PreToolUse）或停止会话（Stop 事件）
- If omitted, defaults to `warn`

**pattern** (simple format): Regex pattern to match
- Used for simple single-condition rules
- Matches against command (bash) or new_text (file)
- Python regex syntax

**Example:**
```yaml
event: bash
pattern: rm\s+-rf
```

### Advanced Format (Multiple Conditions)

For complex rules with multiple conditions:

```markdown
---
name: warn-env-file-edits
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
---

You're adding an API key to a .env file. Ensure this file is in .gitignore!
```

**Condition fields:**
- `field`: Which field to check
  - For bash: `command`
  - For file: `file_path`, `new_text`, `old_text`, `content`
- `operator`: How to match
  - `regex_match`: Regex pattern matching
  - `contains`: Substring check
  - `equals`: Exact match
  - `not_contains`: Substring must NOT be present
  - `starts_with`: Prefix check
  - `ends_with`: Suffix check
- `pattern`: Pattern or string to match

**All conditions must match for rule to trigger.**

## Message Body

The markdown content after frontmatter is shown to Claude when the rule triggers.

**Good messages:**
- Explain what was detected
- Explain why it's problematic
- Suggest alternatives or best practices
- Use formatting for clarity (bold, lists, etc.)

**Example:**
```markdown
⚠️ **Console.log detected!**

You're adding console.log to production code.

**Why this matters:**
- Debug logs shouldn't ship to production
- Console.log can expose sensitive data
- Impacts browser performance

**Alternatives:**
- Use a proper logging library
- Remove before committing
- Use conditional debug builds
```

## Event Type Guide

### bash Events

Match Bash command patterns:

```markdown
---
event: bash
pattern: sudo\s+|rm\s+-rf|chmod\s+777
---

Dangerous command detected!
```

**Common patterns:**
- Dangerous commands: `rm\s+-rf`, `dd\s+if=`, `mkfs`
- Privilege escalation: `sudo\s+`, `su\s+`
- Permission issues: `chmod\s+777`, `chown\s+root`

### file Events

Match Edit/Write/MultiEdit operations:

```markdown
---
event: file
pattern: console\.log\(|eval\(|innerHTML\s*=
---

Potentially problematic code pattern detected!
```

**Match on different fields:**
```markdown
---
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.tsx?$
  - field: new_text
    operator: regex_match
    pattern: console\.log\(
---

Console.log in TypeScript file!
```

**Common patterns:**
- Debug code: `console\.log\(`, `debugger`, `print\(`
- Security risks: `eval\(`, `innerHTML\s*=`, `dangerouslySetInnerHTML`
- Sensitive files: `\.env$`, `credentials`, `\.pem$`
- Generated files: `node_modules/`, `dist/`, `build/`

### stop Events

Match when agent wants to stop (completion checks):

```markdown
---
event: stop
pattern: .*
---

Before stopping, verify:
- [ ] Tests were run
- [ ] Build succeeded
- [ ] Documentation updated
```

**Use for:**
- Reminders about required steps
- Completion checklists
- Process enforcement

### prompt Events

Match user prompt content (advanced):

```markdown
---
event: prompt
conditions:
  - field: user_prompt
    operator: contains
    pattern: deploy to production
---

Production deployment checklist:
- [ ] Tests passing?
- [ ] Reviewed by team?
- [ ] Monitoring ready?
```

## Pattern Writing Tips

### Regex Basics

**Literal characters:** Most characters match themselves
- `rm` matches "rm"
- `console.log` matches "console.log"

**Special characters need escaping:**
- `.` (any char) → `\.` (literal dot)
- `(` `)` → `\(` `\)` (literal parens)
- `[` `]` → `\[` `\]` (literal brackets)

**Common metacharacters:**
- `\s` - whitespace (space, tab, newline)
- `\d` - digit (0-9)
- `\w` - word character (a-z, A-Z, 0-9, _)
- `.` - any character
- `+` - one or more
- `*` - zero or more
- `?` - zero or one
- `|` - OR

**Examples:**
```
rm\s+-rf         Matches: rm -rf, rm  -rf
console\.log\(   Matches: console.log(
(eval|exec)\(    Matches: eval( or exec(
chmod\s+777      Matches: chmod 777, chmod  777
API_KEY\s*=      Matches: API_KEY=, API_KEY =
```

### Testing Patterns

Test regex patterns before using:

```bash
python3 -c "import re; print(re.search(r'your_pattern', 'test text'))"
```

Or use online regex testers (regex101.com with Python flavor).

### Common Pitfalls

**Too broad:**
```yaml
pattern: log    # Matches "log", "login", "dialog", "catalog"
```
Better: `console\.log\(|logger\.`

**Too specific:**
```yaml
pattern: rm -rf /tmp  # Only matches exact path
```
Better: `rm\s+-rf`

**Escaping issues:**
- YAML quoted strings: `"pattern"` requires double backslashes `\\s`
- YAML unquoted: `pattern: \s` works as-is
- **Recommendation**: Use unquoted patterns in YAML

## File Organization

**Location:** All rules in `.claude/` directory
**Naming:** `.claude/hookify.{descriptive-name}.local.md`
**Gitignore:** Add `.claude/*.local.md` to `.gitignore`

**Good names:**
- `hookify.dangerous-rm.local.md`
- `hookify.console-log.local.md`
- `hookify.require-tests.local.md`
- `hookify.sensitive-files.local.md`

**Bad names:**
- `hookify.rule1.local.md` (not descriptive)
- `hookify.md` (missing .local)
- `danger.local.md` (missing hookify prefix)

## Workflow

### Creating a Rule

1. Identify unwanted behavior
2. Determine which tool is involved (Bash, Edit, etc.)
3. Choose event type (bash, file, stop, etc.)
4. Write regex pattern
5. Create `.claude/hookify.{name}.local.md` file in project root
6. Test immediately - rules are read dynamically on next tool use

### Refining a Rule

1. Edit the `.local.md` file
2. Adjust pattern or message
3. Test immediately - changes take effect on next tool use

### Disabling a Rule

**Temporary:** Set `enabled: false` in frontmatter
**Permanent:** Delete the `.local.md` file

## Examples

See `${CLAUDE_PLUGIN_ROOT}/examples/` for complete examples:
- `dangerous-rm.local.md` - Block dangerous rm commands
- `console-log-warning.local.md` - Warn about console.log
- `sensitive-files-warning.local.md` - Warn about editing .env files

## Quick Reference

**Minimum viable rule:**
```markdown
---
name: my-rule
enabled: true
event: bash
pattern: dangerous_command
---

Warning message here
```

**Rule with conditions:**
```markdown
---
name: my-rule
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.ts$
  - field: new_text
    operator: contains
    pattern: any
---

Warning message
```

**Event types:**
- `bash` - Bash commands
- `file` - File edits
- `stop` - Completion checks
- `prompt` - User input
- `all` - All events

**Field options:**
- Bash: `command`
- File: `file_path`, `new_text`, `old_text`, `content`
- Prompt: `user_prompt`

**Operators:**
- `regex_match`, `contains`, `equals`, `not_contains`, `starts_with`, `ends_with`
