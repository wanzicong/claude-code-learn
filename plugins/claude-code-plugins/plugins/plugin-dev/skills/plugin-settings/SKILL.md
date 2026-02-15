---
name: 插件设置
description: 当用户询问"插件设置"、"存储插件配置"、"用户可配置插件"、".local.md 文件"、"插件状态文件"、"读取 YAML frontmatter"、"每个项目的插件设置"，或想要使插件行为可配置时，应使用此技能。记录用于使用 YAML frontmatter 和 markdown 内容存储插件特定配置的 .claude/plugin-name.local.md 模式。
version: 0.1.0
---

# Claude Code 插件的插件设置模式

## 概述

插件可以在项目目录中的 `.claude/plugin-name.local.md` 文件中存储用户可配置的设置和状态。此模式使用 YAML frontmatter 进行结构化配置，使用 markdown 内容提供提示或附加上下文。

**关键特征:**
- 文件位置: 项目根目录中的 `.claude/plugin-name.local.md`
- 结构: YAML frontmatter + markdown 主体
- 目的: 每个项目的插件配置和状态
- 用法: 从钩子、命令和代理中读取
- 生命周期: 用户管理（不在 git 中，应在 `.gitignore` 中）

## 文件结构

### 基本模板

```markdown
---
enabled: true
setting1: value1
setting2: value2
numeric_setting: 42
list_setting: ["item1", "item2"]
---

# 附加上下文

此 markdown 主体可以包含:
- 任务描述
- 附加说明
- 反馈给 Claude 的提示
- 文档或注释
```

### 示例: 插件状态文件

**.claude/my-plugin.local.md:**
```markdown
---
enabled: true
strict_mode: false
max_retries: 3
notification_level: info
coordinator_session: team-leader
---

# 插件配置

此插件配置为标准验证模式。
有问题请联系 @team-lead。
```

## 读取设置文件

### 从钩子（Bash 脚本）

**模式: 检查存在性并解析 frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# Define state file path
STATE_FILE=".claude/my-plugin.local.md"

# Quick exit if file doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin not configured, skip
fi

# Parse YAML frontmatter (between --- markers)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extract individual fields
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//' | sed 's/^"\(.*\)"$/\1/')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Use configuration in hook logic
if [[ "$STRICT_MODE" == "true" ]]; then
  # Apply strict validation
  # ...
fi
```

请参阅 `examples/read-settings-hook.sh` 获取完整的工作示例。

### 从命令

命令可以读取设置文件以自定义行为:

```markdown
---
description: Process data with plugin
allowed-tools: ["Read", "Bash"]
---

# 处理命令

步骤:
1. 检查 `.claude/my-plugin.local.md` 是否存在设置
2. 使用 Read 工具读取配置
3. 解析 YAML frontmatter 以提取设置
4. 将设置应用于处理逻辑
5. 使用配置的行为执行
```

### 从代理

代理可以在其指令中引用设置:

```markdown
---
name: configured-agent
description: Agent that adapts to project settings
---

检查 `.claude/my-plugin.local.md` 中的插件设置。
如果存在，解析 YAML frontmatter 并根据以下内容调整行为:
- enabled: 插件是否激活
- mode: 处理模式（strict、standard、lenient）
- 其他配置字段
```

## 解析技术

### 提取 Frontmatter

```bash
# Extract everything between --- markers
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

### 读取单个字段

**字符串字段:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**布尔字段:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
# 比较: if [[ "$ENABLED" == "true" ]]; then
```

**数字字段:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')
# 使用: if [[ $MAX -gt 100 ]]; then
```

### 读取 Markdown 主体

提取第二个 `---` 之后的内容:

```bash
# Get everything after closing ---
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

## 常见模式

### 模式 1: 临时激活的钩子

使用设置文件控制钩子激活:

```bash
#!/bin/bash
STATE_FILE=".claude/security-scan.local.md"

# Quick exit if not configured
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Read enabled flag
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Run hook logic
# ...
```

**使用场景:** 在不编辑 hooks.json 的情况下启用/禁用钩子（需要重启）。

### 模式 2: 代理状态管理

存储代理特定的状态和配置:

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-agent
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
---

# 任务分配

为 API 实现 JWT 身份验证。

**成功标准:**
- 创建身份验证端点
- 测试通过
- 创建 PR 并且 CI 通过
```

从钩子读取以协调代理:

```bash
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//')
COORDINATOR=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//')

# Send notification to coordinator
tmux send-keys -t "$COORDINATOR" "Agent $AGENT_NAME completed task" Enter
```

### 模式 3: 配置驱动的行为

**.claude/my-plugin.local.md:**
```markdown
---
validation_level: strict
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
---

# 验证配置

为此项目启用严格模式。
所有写操作都根据安全策略进行验证。
```

在钩子或命令中使用:

```bash
LEVEL=$(echo "$FRONTMATTER" | grep '^validation_level:' | sed 's/validation_level: *//')

case "$LEVEL" in
  strict)
    # Apply strict validation
    ;;
  standard)
    # Apply standard validation
    ;;
  lenient)
    # Apply lenient validation
    ;;
esac
```

## 创建设置文件

### 从命令

命令可以创建设置文件:

```markdown
# 设置命令

步骤:
1. 询问用户配置首选项
2. 创建带有 YAML frontmatter 的 `.claude/my-plugin.local.md`
3. 根据用户输入设置适当的值
4. 通知用户设置已保存
5. 提醒用户重启 Claude Code 以使钩子识别更改
```

### 模板生成

在插件 README 中提供模板:

```markdown
## 配置

在您的项目中创建 `.claude/my-plugin.local.md`:

\`\`\`markdown
---
enabled: true
mode: standard
max_retries: 3
---

# 插件配置

您的设置已激活。
\`\`\`

创建或编辑后，重启 Claude Code 以使更改生效。
```

## 最佳实践

### 文件命名

✅ **应该做:**
- 使用 `.claude/plugin-name.local.md` 格式
- 准确匹配插件名称
- 对用户本地文件使用 `.local.md` 后缀

❌ **不应该做:**
- 使用不同的目录（非 `.claude/`）
- 使用不一致的命名
- 使用不带 `.local` 的 `.md`（可能被提交）

### Gitignore

始终添加到 `.gitignore`:

```gitignore
.claude/*.local.md
.claude/*.local.json
```

在插件 README 中记录此内容。

### 默认值

当设置文件不存在时提供合理的默认值:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  # Use defaults
  ENABLED=true
  MODE=standard
else
  # Read from file
  # ...
fi
```

### 验证

验证设置值:

```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# Validate numeric range
if ! [[ "$MAX" =~ ^[0-9]+$ ]] || [[ $MAX -lt 1 ]] || [[ $MAX -gt 100 ]]; then
  echo "⚠️  Invalid max_value in settings (must be 1-100)" >&2
  MAX=10  # Use default
fi
```

### 重启要求

**重要:** 设置更改需要重启 Claude Code。

在您的 README 中记录:

```markdown
## 更改设置

编辑 `.claude/my-plugin.local.md` 后:
1. 保存文件
2. 退出 Claude Code
3. 重启: `claude` 或 `cc`
4. 新设置将被加载
```

钩子无法在会话中热交换。

## 安全考虑

### 清理用户输入

从用户输入写入设置文件时:

```bash
# Escape quotes in user input
SAFE_VALUE=$(echo "$USER_INPUT" | sed 's/"/\\"/g')

# Write to file
cat > "$STATE_FILE" <<EOF
---
user_setting: "$SAFE_VALUE"
---
EOF
```

### 验证文件路径

如果设置包含文件路径:

```bash
FILE_PATH=$(echo "$FRONTMATTER" | grep '^data_file:' | sed 's/data_file: *//')

# Check for path traversal
if [[ "$FILE_PATH" == *".."* ]]; then
  echo "⚠️  Invalid path in settings (path traversal)" >&2
  exit 2
fi
```

### 权限

设置文件应该:
- 仅用户可读（`chmod 600`）
- 不提交到 git
- 不在用户之间共享

## 真实世界示例

### multi-agent-swarm 插件

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: Use JWT tokens, not sessions
---

# 任务: 实现身份验证

为 REST API 构建基于 JWT 的身份验证。
与 auth-agent 协调共享类型。
```

**钩子使用（agent-stop-notification.sh）:**
- 检查文件是否存在（第 15-18 行：如果不存在则快速退出）
- 解析 frontmatter 以获取 coordinator_session、agent_name、enabled
- 如果启用则向协调者发送通知
- 允许通过 `enabled: true/false` 快速激活/停用

### ralph-wiggum 插件

**.claude/ralph-loop.local.md:**
```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
---

修复项目中的所有 linting 错误。
确保每次修复后测试都通过。
```

**钩子使用（stop-hook.sh）:**
- 检查文件是否存在（第 15-18 行：如果未激活则快速退出）
- 读取迭代计数和 max_iterations
- 提取 completion_promise 用于循环终止
- 读取主体作为反馈的提示
- 每次循环更新迭代计数

## 快速参考

### 文件位置

```
project-root/
└── .claude/
    └── plugin-name.local.md
```

### Frontmatter 解析

```bash
# Extract frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Read field
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')
```

### 主体解析

```bash
# Extract body (after second ---)
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

### 快速退出模式

```bash
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # Not configured
fi
```

## 其他资源

### 参考文件

详细实现模式:

- **`references/parsing-techniques.md`** - 解析 YAML frontmatter 和 markdown 主体的完整指南
- **`references/real-world-examples.md`** - multi-agent-swarm 和 ralph-wiggum 实现的深入探讨

### 示例文件

`examples/` 中的工作示例:

- **`read-settings-hook.sh`** - 读取和使用设置的钩子
- **`create-settings-command.md`** - 创建设置文件的命令
- **`example-settings.md`** - 模板设置文件

### 实用脚本

`scripts/` 中的开发工具:

- **`validate-settings.sh`** - 验证设置文件结构
- **`parse-frontmatter.sh`** - 提取 frontmatter 字段

## 实施工作流程

向插件添加设置:

1. 设计设置架构（哪些字段、类型、默认值）
2. 在插件文档中创建模板文件
3. 为 `.claude/*.local.md` 添加 gitignore 条目
4. 在钩子/命令中实现设置解析
5. 使用快速退出模式（检查文件存在、检查 enabled 字段）
6. 在插件 README 中记录设置和模板
7. 提醒用户更改需要重启 Claude Code

专注于保持设置简单，并在设置文件不存在时提供良好的默认值。
