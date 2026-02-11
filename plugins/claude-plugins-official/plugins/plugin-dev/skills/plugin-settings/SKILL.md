---
name: plugin-settings
description: 当用户询问"插件设置"、"存储插件配置"、"用户可配置插件"、".local.md 文件"、"插件状态文件"、"读取 YAML frontmatter"、"每项目插件设置"，或希望使插件行为可配置时，应使用此技能。记录 .claude/plugin-name.local.md 模式，用于使用 YAML frontmatter 和 markdown 内容存储插件特定配置。
version: 0.1.0
---

# Claude Code 插件的插件设置模式

## 概述

插件可以在项目目录内的 `.claude/plugin-name.local.md` 文件中存储用户可配置的设置和状态。此模式使用 YAML frontmatter 进行结构化配置，使用 markdown 内容作为提示或附加上下文。

**主要特性：**
- 文件位置：项目根目录中的 `.claude/plugin-name.local.md`
- 结构：YAML frontmatter + markdown 正文
- 用途：每项目插件配置和状态
- 使用方式：从钩子、命令和代理读取
- 生命周期：用户管理（不在 git 中，应在 `.gitignore` 中）

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

此 markdown 正文可以包含：
- 任务描述
- 附加指令
- 反馈给 Claude 的提示
- 文档或说明
```

### 示例：插件状态文件

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

**模式：检看是否存在并解析 frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# 定义状态文件路径
STATE_FILE=".claude/my-plugin.local.md"

# 如果文件不存在则快速退出
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # 插件未配置，跳过
fi

# 解析 YAML frontmatter（在 --- 标记之间）
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# 提取各个字段
ENABLED=$(echo "$FRONTMATTER" | grep '^'enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//' | sed 's/^"\(.*\)"$/\1/')

# 检查是否启用
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # 已禁用
fi

# 在钩子逻辑中使用配置
if [[ "$STRICT_MODE" == "true" ]]; then
  # 应用严格验证
  # ...
fi
```

请参阅 `examples/read-settings-hook.sh` 查看完整的工作示例。

### 从命令

命令可以读取设置文件以自定义行为：

```markdown
---
description: 使用插件处理数据
allowed-tools: ["Read", "Bash"]
---

# 处理命令

步骤：
1. 检查设置是否存在于 `.claude/my-plugin.local.md`
2. 使用 Read 工具读取配置
3. 解析 YAML frontmatter 以提取设置
4. 将设置应用于处理逻辑
5. 使用配置的行为执行
```

### 从代理

代理可以在其指令中引用设置：

```markdown
---
name: configured-agent
description: 根据项目设置进行调整的代理
---

检看插件设置是否位于 `.claude/my-plugin.local.md`。
如果存在，解析 YAML frontmatter 并根据以下调整行为：
- enabled：插件是否活动
- mode：处理模式（strict、standard、lenient）
- 附加配置字段
```

## 解析技术

### 提取 Frontmatter

```bash
# 提取 --- 标记之间的所有内容
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

### 读取各个字段

**字符串字段：**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**布尔字段：**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
# 比较：if [[ "$ENABLED" == "true" ]]; then
```

**数字字段：**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')
# 使用：if [[` $MAX -gt 100 ]]; then
```

### 读取 Markdown 正文

提取第二个 `---` 之后的内容：

```bash
# 获取结束 --- 之后的所有内容
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

## 常见模式

### 模式 1：临时激活的钩子

使用设置文件控制钩子激活：

```bash
#!/bin/bash
STATE_FILE=".claude/security-scan.local.md"

# 如果未配置则快速退出
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# 读取 enabled 标志
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # 已禁用
fi

# 运行钩子逻辑
# ...
```

**使用场景：** 启用/禁用钩子而无需编辑 hooks.json（需要重启）。

### 模式 2：代理状态管理

存储代理特定状态和配置：

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: "使用 JWT 令牌，而非会话"
---

# 任务分配：实现身份验证

为 REST API 构建 JWT 基于身份验证。

**成功标准：**
- 身份验证端点已创建
- 测试通过（100% 覆盖率）
- PR 已创建且 CI 绿色
- 文档已更新

## 协调

依赖于 Task 3.4（用户模型）。
向协调器会话 'team-leader' 报告状态。
```

从钩子读取以协调代理：

```bash
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//' | sed 's/^"\(.*\)"$/\1/')
COORDINATOR=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//' | sed 's/^"\(.*\)"$/\1/')

# 向协调器发送通知
tmux send-keys -t "$COORDINATOR" "代理 $AGENT_NAME 完成任务" Enter
```

### 模式 3：配置驱动的行为

**.claude/my-plugin.local.md:**
```markdown
---
validation_level: strict
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
---

# 验证配置

此项目启用严格模式。
所有写入均根据安全策略进行验证。
```

在钩子或命令中使用：

```bash
LEVEL=$(echo "$FRONTMATTER" | grep '^validation_level:' | sed 's/validation_level: *//')

case "$LEVEL" in
  strict)
    # 应用严格验证
    ;;
  standard)
    # 应用标准验证
    ;;
  lenient)
    # 应用宽松验证
    ;;
esac
```

## 创建设置文件

### 从命令

命令可以创建设置文件：

```markdown
# 设置命令

步骤：
1. 询问用户的配置偏好
2. 使用 YAML frontmatter 创建 `.claude/my-plugin.local.md`
3. 根据用户输入设置适当的值
4. 通知用户设置已保存
5. 提醒用户重启 Claude Code 以使钩子识别更改
```

### 模板生成

在插件 README 中提供模板：

```markdown
## 配置

在项目中创建 `.claude/my-plugin.local.md`：

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

✅ **应该：**
- 使用 `.claude/plugin-name.local.md` 格式
- 完全匹配插件名称
- 对用户本地文件使用 `.local.md` 后缀

❌ **不应该：**
- 使用不同目录（而非 `.claude/`）
- 使用不一致的命名
- 使用不带 `.local` 的 `.md`（可能会被提交）

### Gitignore

始终添加到 `.gitignore`：

```gitignore
.claude/*.local.md
.claude/*.local.json
```

在插件 README 中记录此内容。

### 默认值

当设置文件不存在时提供合理的默认值：

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  # 使用默认值
  ENABLED=true
  MODE=standard
else
  # 从文件读取
  # ...
fi
```

### 验证

验证设置值：

```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# 验证数字范围
if ! [[ "$MAX" =~ ^[0-9]+$ ]] || [[ $MAX -lt 1 ]] || [[ $MAX -gt 100 ]]; then
  echo "⚠  设置中的 max_value 无效（必须为 1-100）" >&2
  MAX=10  # 使用默认值
fi
```

### 重启要求

**重要：** 设置更改需要 Claude Code 重启。

在您的 README 中记录：

```markdown
## 更改设置

编辑 `.claude/my-plugin.local.md` 后：
1. 保存文件
2. 退出 Claude Code
3. 重启：`claude` 或 `cc`
4. 将加载新设置
```

钩子无法在会话内热交换。

## 安全考虑

### 清理用户输入

从用户输入写入设置文件时：

```bash
# 转义用户输入中的引号
SAFE_VALUE=$(echo "$USER_INPUT" | sed 's/"/\\"/g')

# 写入文件
cat > "$STATE_FILE" <<EOF
---
user_setting: "$SAFE_VALUE"
---
EOF
```

### 验证文件路径

如果设置包含文件路径：

```bash
FILE_PATH=$(echo "$FRONTMATTER" | grep '^data_file:' | sed 's/data_file: *//')

# 检查路径遍历
if [[ "$FILE_PATH" == *".."* ]]; then
  echo "⚠  设置中的路径无效（路径遍历）" >&2
  exit 2
fi
```

### 权限

设置文件应该是：
- 仅用户可读（`chmod 600`）
- 不提交到 git
- 不在用户之间共享

## 真实世界示例

### multi-agent-swarmar 插件

**.claude/multi-agentar-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: "使用 JWT 令牌，而非会话"
---

# 任务：实现身份验证

为 REST API 构建 JWT 基于身份验证。

**要求：**
- JWT 令牌生成和验证
- 刷新令牌流程
- 安全密码哈希

**成功标准：**
- 已实现身份验证端点
- 测试通过（100% 覆盖率）
- PR 已创建且 CI 绿色
- 文档已更新

## 协调

依赖于 Task 3.4（用户模型）。
向协调器会话 'team-leader' 报告状态。
```

**钩子使用（agent-stop-notification.sh）：**
- 检查文件是否存在（第 15-18 行：如不存在则快速退出）
- 解析 frontmatter 以获取 coordinator_session、agent_name、enabled
- 如果启用则向协调器发送通知
- 允许通过 `enabled: true/false` 快速激活/停用

### ralph-loop 插件

**.claude/ralph-loop.local.md:**
```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "所有测试通过且构建成功"
started_at: "2025-01-15T14:30:00Z"
---

修复项目中的所有 linting 错误。
确保每次修复后测试通过。
在 CLAUDE.md 中记录所需的任何更改。
```

**钩子使用（stop-hook.sh）：**
- 检查文件是否存在（第 15-18 行：如未激活则快速退出）
- 读取迭代计数和 max_iterations
- 提取 completion_promise 以用于循环终止
- 将正文作为提示反馈
- 每次循环时更新迭代计数

## 快速参考

### 文件位置

```
project-root/
└── .claude/
    └── plugin-name.local.md
```

### Frontmatter 解析

```bash
# 提取 frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# 读取字段
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')
```

### 正文解析

```bash
# 提取正文（在第二个 --- 之后）
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

### 快速退出模式

```bash
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # 未配置
fi
```

## 其他资源

### 参考文件

有关详细实现模式：

- **`references/parsing-techniques.md`** - 解析 YAML frontmatter 和 markdown 正文的完整指南
- **`references/real-world-examples.md`** - multi-agent-ar-swarm 和 ralph-loop 实现的深入解析

### 示例文件

`examples/` 中的工作示例：

- **`read-settings-hook.sh`** - 读取并使用设置的钩子
- **`create-settings-command.md`** - 创建设置文件的命令
- **`example-settings.md`** - 模板设置文件

### 实用脚本

`scripts/` 中的开发工具：

- **`validate-settings.sh`** - 验证设置文件结构
- **`parse-frontmatter.sh`** - 提取 frontmatter 字段

## 实现工作流

将设置添加到插件：

1. 设计设置架构（哪些字段、类型、默认值）
2. 在插件文档中创建模板文件
3. 将 `.gitignore` 条目添加到 `.claude/*.local.md`
4. 在钩子/命令中实现设置解析
5. 使用快速退出模式（检看文件是否存在、检看 enabled 字段）
6. 在插件 README 中记录设置并附带模板
7. 提醒用户更改需要 Claude Code 重启

专注于保持设置简单，并在设置文件不存在时提供良好的默认值。
