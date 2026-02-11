# 真实世界插件设置示例

生产插件如何使用 `.claude/plugin-name.local.md` 模式的详细分析。

## multi-agent-swarmar 插件

### 设置文件结构

**.claude/multi-agent-ar-swarm.local.md:**

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

## 要求
- JWT 令牌生成和验证
- 刷新令牌流程
- 安全密码哈希

## 成功标准
- 已实现身份验证端点
- 测试通过（100% 覆盖率）
- PR 已创建且 CI 绿色
- 文档已更新

## 协调
依赖于 Task 3.4（用户模型）。
向协调器会话 'team-leader' 报告状态。
```

### 使用方式

**文件：** `hooks/agent-stop-notification.sh`

**目的：** 当代理变为空闲时向协调器发送通知

**实现：**

```bash
#!/bin/bash
set -euoaring pipefail

SWARM_STATE_FILE=".claude/multi-agent-swarm.local.md"

# 如果没有激活的 swar 则快速退出
if [[ ! -f "$SWARM_STATE_FILE" ]]; then
  exit 0
fi

# 解析 frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SWARM_STATE_FILE")

# 提取配置
COORDINATOR_SESSION=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//' | sed 's/^"\(.*\)"$/\1/')
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//' | sed 's/^"\(.*\)"$/\1/')
TASK_NUMBER=$(echo "$FRONTMATTER" | grep '^task_number:' | sed 's/task_number: *//' | sed 's/^"\(.*\)"$/\1/')
PR_NUMBER=$(echo "$FRONTMATTER" | grep '^pr_number:' | sed 's/pr_number: *//' | sed 's/^"\(.*\)"$/\1/')
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# 检查是否启用
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# 向协调器发送通知
NOTIFICATION="🤖 代理 ${AGENT_NAME}（任务 ${TASK_NUMBER}，PR #${PR_NUMBER}）处于空闲状态。"

if tmux has-session -t "$COORDINATOR_SESSION" 2>/dev/null; then
  tmux send-keys -t "$COORDINATOR_SESSION" "$NOTIFICATION" Enter
  sleep 0.5
  tmux send-keys -t "$COORDINATOR_SESSION" Enter
fi

exit 0
```

**主要模式：**
1. **快速退出**（第 7-9 行）：如果文件不存在则立即返回
2. **字段提取**（第 11-17 行）：解析每个 frontmatter 字段
3. **Enabled 检查**（第 19-21 行）：尊重 enabled 标志
4. **基于设置的操作**（第 23-29 行）：使用 coordinator_session 发送通知

### 创建

**文件：** `commands/launch-swar.md`

设置文件在 swar 启动期间创建：

```bash
cat > "$WORKTREE_PATH/.claude/multi-agent-swarm.local.md" <<EOF
---
agent_name: $AGENT_NAME
task_number: $TASK_ID
pr_number: TBD
coordinator_session: $COORDINATOR_SESSION
enabled: true
dependencies: [$DEPENDENCIES]
additional_instructions: "$EXTRA_INSTRUCTIONS"
---

# 任务：$TASK_DESCRIPTION

$TASK_DETAILS
EOF
```

### 更新

PR 创建后更新 PR 编号：

```bash
# 更新 pr_number 字段
sed "s/^pr_number: .*/pr_number: $PR_NUM/" \
  ".claude/multi-agent-swarm.local.md" > temp.md
mv temp.md ".claude/multi-agent-swarm.local.md"
```

## ralph-loop 插件

### 设置文件结构

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

### 使用方式

**文件：** `hooks/stop-hook.sh`

**目的：** 阻止会话退出并将 Claude 的输出循环回作为输入

**实现：**

```bash
#!/bin/bash
set -euoaring pipefail

RALPH_STATE_FILE=".claude/ralph-loop.local.md"

# 如果没有活动的循环则快速退出
if [[ ! -f "$RALPH_STATE_FILE" ]]; then
  exit 0
fi

# 解析 frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$RALPH_STATE_FILE")

# 提取配置
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')

# 检查最大迭代次数
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 Ralph 循环：达到最大迭代次数（$MAX_ITERATIONS）。"
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# 获取转录并检看完成承诺
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')
LAST_OUTPUT=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 | jq -r '.message.content | map(select(.type == "text")) | map(.text) | join("\n")')

# 检查完成
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g')

  if [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
    echo "✅ Ralph 循环：检测到完成"
    rm "$RALPH_STATE_FILE"
    exit 0
  fi
fi

# 继续循环 - 增加迭代
NEXT_ITERATION=$((ITERATION + 1))

# 从 markdown 正文提取提示
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# 更新迭代计数器
TEMP_FILE="${RALPH_STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$RALPH_STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$RALPH_STATE_FILE"

# 阻止退出并将提示反馈
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "🔄 Ralph 迭代 $NEXT_ITERATION" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
```

**主要模式：**
1. **快速退出**（第 7-9 行）：如未激活则跳过
2. **迭代跟踪**（第 11-20 行）：计数并强制最大迭代次数
3. **承诺检测**（第 25-33 行）：检看输出中的完成信号
4. **提示提取**（第 38 行）：将 markdown 正文作为下一个提示读取
5. **状态更新**（第 40-43 行）：原子的增加迭代
6. **循环继续**（第 45-53 行）：阻尼退出并反馈提示

### 创建

**文件：** `scripts/setup-ralph-loop.sh`

```bash
#!/bin/bash
PROMPT="$1"
MAX_ITERATIONS="${2:-0}"
COMPLETION_PROMISE="${3:-}"

# 创建状态文件
cat > ".claude/ralph-loop.local.md" <<EOF
---
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: "$COMPLETION_PROMISE"
started_at: "$(date -Iseconds)"
---

$PROMPT
EOF

echo "Ralph 循环已初始化：.claude/ralph-loop.local.md"
```

## 模式对比

| 功能 | multi-agent-ar-swarm | ralph-loop |
|---------|-------------------|--------------|
| **文件** | `.claude/multi-agentar-swarm.local.md` | `.claude/ralph-loop.local.md` |
| **目的** | 代理协调状态 | 循环迭代状态 |
| **Frontmatter** | 代理元数据 | 循环配置 |
| **正文** | 任务分配 | 要循环的提示 |
| **更新** | PR 编号、状态 | 迭代计数器 |
| **删除** | 手动或完成时 | 循环退出时 |
| **钩子** | 停止（通知） | 停止（循环控制） |

## 真实世界插件的最佳实践

### 1. 快速退出模式

两个插件都首先检看文件是否存在：

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # 未激活
fi
```

**原因：** 避免插件未配置时的错误，并且执行快速。

### 2. Enabled 标志

两者都使用 `enabled` 字段进行显式控制：

```yaml
enabled: true
```

**原因：** 允许在无需删除文件的情况下临时停用。

### 3. 原子更新

两者都使用临时文件 + 原子移动：

```bash
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^field: .*/field: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

**原因：** 如果进程中断则防止损坏。

### 4. 引号处理

两者都从 YAML 值去除周围引号：

```bash
sed 's/^"\(.*\)"$/\1/'
```

**原因：** YAML 允许 ``field: value` 和 `field: "value"`。

### 5. 错误处理

两者都优雅地处理缺失/损坏的文件：

```bash
if [[ ! -f "$FILE" ]]; then
  exit 0  # 无错误，只是未配置
fi

if [[ -z "$CRITICAL_FIELD" ]]; then
  echo "设置文件损坏" >&2
  rm "$FILE"  # 清理
  exit 0
fi
```

**原因：** 优雅地失败而非崩溃。

## 反模式

### ❌ 硬编码路径

```bash
# 不好
FILE="/Users/alice/.claude/my-plugin.local.md"

# 好
FILE=".claude/my-plugin.local.md"
```

### ❌ 未引用的变量

```bash
# 不好
echo $VALUE

# 好
echo "$VALUE"
```

### ❌ 非原子的更新

```bash
# 不好：如果中断则可能损坏文件
sed -i "s/field: .*/field: $VALUE/" "$FILE"

# 好：原子的
TEMP_FILE="${FILE}.tmp.$$"
sed "s/field: .*/field: $VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### ❌ 无默认值

```bash
# 不好：如果字段缺失则失败
if [[ $MAX -gt 100 ]]; then
  # MAX 可能为空！
fi

# 好：提供默认值
MAX=${MAX:-10}
```

### ❌ 忽略边界情况

```bash
# 不好：假设恰好 2 个 --- 标记
sed -n '/^---$/,/^---$/{ /^---$/d; p; }'

# 好：处理正文中的 ---
awk '/^---$/{i++; next} i>=2'  # 用于正文
```

## 结论

`.claude/plugin-name.local.md` 模式提供：
- 简单、人类可读的配置
- 版本控制友好（gitignored）
- 每项目设置
- 使用标准 bash 工具轻松解析
- 支持结构化配置（YAML）和自由格式内容（markdown）

使用此模式处理任何需要用户可配置行为或状态持久化的插件。
