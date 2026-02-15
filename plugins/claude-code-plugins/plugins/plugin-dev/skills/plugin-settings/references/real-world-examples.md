# 真实世界的插件设置示例

详细分析生产插件如何使用 `.claude/plugin-name.local.md` 模式。

## multi-agent-swarm 插件

### 设置文件结构

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: "Use JWT tokens, not sessions"
---

# Task: Implement Authentication

Build JWT-based authentication for the REST API.

## Requirements
- JWT token generation and validation
- Refresh token flow
- Secure password hashing

## Success Criteria
- Auth endpoints implemented
- Tests passing (100% coverage)
- PR created and CI green
- Documentation updated

## Coordination
Depends on Task 3.4 (user model).
Report status to 'team-leader' session.
```

### 如何使用

**文件:** `hooks/agent-stop-notification.sh`

**目的:** 当代理变为空闲时向协调器发送通知

**实现:**

```bash
#!/bin/bash
set -euo pipefail

SWARM_STATE_FILE=".claude/multi-agent-swarm.local.md"

# Quick exit if no swarm active
if [[ ! -f "$SWARM_STATE_FILE" ]]; then
  exit 0
fi

# Parse frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SWARM_STATE_FILE")

# Extract configuration
COORDINATOR_SESSION=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//' | sed 's/^"\(.*\)"$/\1/')
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//' | sed 's/^"\(.*\)"$/\1/')
TASK_NUMBER=$(echo "$FRONTMATTER" | grep '^task_number:' | sed 's/task_number: *//' | sed 's/^"\(.*\)"$/\1/')
PR_NUMBER=$(echo "$FRONTMATTER" | grep '^pr_number:' | sed 's/pr_number: *//' | sed 's/^"\(.*\)"$/\1/')
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# Send notification to coordinator
NOTIFICATION="🤖 Agent ${AGENT_NAME} (Task ${TASK_NUMBER}, PR #${PR_NUMBER}) is idle."

if tmux has-session -t "$COORDINATOR_SESSION" 2>/dev/null; then
  tmux send-keys -t "$COORDINATOR_SESSION" "$NOTIFICATION" Enter
  sleep 0.5
  tmux send-keys -t "$COORDINATOR_SESSION" Enter
fi

exit 0
```

**关键模式:**
1. **快速退出** (第7-9行): 如果文件不存在立即返回
2. **字段提取** (第11-17行): 解析每个 frontmatter 字段
3. **启用检查** (第19-21行): 尊重启用标志
4. **基于设置的操作** (第23-29行): 使用 coordinator_session 发送通知

### 创建

**文件:** `commands/launch-swarm.md`

设置文件在集群启动期间创建:

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

# Task: $TASK_DESCRIPTION

$TASK_DETAILS
EOF
```

### 更新

PR 创建后更新 PR 编号:

```bash
# Update pr_number field
sed "s/^pr_number: .*/pr_number: $PR_NUM/" \
  ".claude/multi-agent-swarm.local.md" > temp.md
mv temp.md ".claude/multi-agent-swarm.local.md"
```

## ralph-wiggum 插件

### 设置文件结构

**.claude/ralph-loop.local.md:**

```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
started_at: "2025-01-15T14:30:00Z"
---

Fix all the linting errors in the project.
Make sure tests pass after each fix.
Document any changes needed in CLAUDE.md.
```

### How It's Used

**File:** `hooks/stop-hook.sh`

**Purpose:** Prevent session exit and loop Claude's output back as input

**Implementation:**

```bash
#!/bin/bash
set -euo pipefail

RALPH_STATE_FILE=".claude/ralph-loop.local.md"

# Quick exit if no active loop
if [[ ! -f "$RALPH_STATE_FILE" ]]; then
  exit 0
fi

# Parse frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$RALPH_STATE_FILE")

# Extract configuration
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')

# Check max iterations
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "🛑 Ralph loop: Max iterations ($MAX_ITERATIONS) reached."
  rm "$RALPH_STATE_FILE"
  exit 0
fi

# Get transcript and check for completion promise
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')
LAST_OUTPUT=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 | jq -r '.message.content | map(select(.type == "text")) | map(.text) | join("\n")')

# Check for completion
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g')

  if [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
    echo "✅ Ralph loop: Detected completion"
    rm "$RALPH_STATE_FILE"
    exit 0
  fi
fi

# Continue loop - increment iteration
NEXT_ITERATION=$((ITERATION + 1))

# Extract prompt from markdown body
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# Update iteration counter
TEMP_FILE="${RALPH_STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$RALPH_STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$RALPH_STATE_FILE"

# Block exit and feed prompt back
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "🔄 Ralph iteration $NEXT_ITERATION" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
```

**Key patterns:**
1. **Quick exit** (line 7-9): Skip if not active
2. **Iteration tracking** (lines 11-20): Count and enforce max iterations
3. **Promise detection** (lines 25-33): Check for completion signal in output
4. **Prompt extraction** (line 38): Read markdown body as next prompt
5. **State update** (lines 40-43): Increment iteration atomically
6. **Loop continuation** (lines 45-53): Block exit and feed prompt back

### Creation

**File:** `scripts/setup-ralph-loop.sh`

```bash
#!/bin/bash
PROMPT="$1"
MAX_ITERATIONS="${2:-0}"
COMPLETION_PROMISE="${3:-}"

# Create state file
cat > ".claude/ralph-loop.local.md" <<EOF
---
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: "$COMPLETION_PROMISE"
started_at: "$(date -Iseconds)"
---

$PROMPT
EOF

echo "Ralph loop initialized: .claude/ralph-loop.local.md"
```

## 模式比较

| Feature | multi-agent-swarm | ralph-wiggum |
|---------|-------------------|--------------|
| **File** | `.claude/multi-agent-swarm.local.md` | `.claude/ralph-loop.local.md` |
| **Purpose** | Agent coordination state | Loop iteration state |
| **Frontmatter** | Agent metadata | Loop configuration |
| **Body** | Task assignment | Prompt to loop |
| **Updates** | PR number, status | Iteration counter |
| **Deletion** | Manual or on completion | On loop exit |
| **Hook** | Stop (notifications) | Stop (loop control) |

## 真实插件的最佳实践

### 1. 快速退出模式

两个插件都先检查文件存在性:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Not active
fi
```

**Why:** Avoids errors when plugin isn't configured and performs fast.

### 2. Enabled Flag

Both use an `enabled` field for explicit control:

```yaml
enabled: true
```

**Why:** Allows temporary deactivation without deleting file.

### 3. Atomic Updates

Both use temp file + atomic move:

```bash
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^field: .*/field: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

**Why:** Prevents corruption if process is interrupted.

### 4. Quote Handling

Both strip surrounding quotes from YAML values:

```bash
sed 's/^"\(.*\)"$/\1/'
```

**Why:** YAML allows both `field: value` and `field: "value"`.

### 5. Error Handling

Both handle missing/corrupt files gracefully:

```bash
if [[ ! -f "$FILE" ]]; then
  exit 0  # No error, just not configured
fi

if [[ -z "$CRITICAL_FIELD" ]]; then
  echo "Settings file corrupt" >&2
  rm "$FILE"  # Clean up
  exit 0
fi
```

**Why:** Fails gracefully instead of crashing.

## 要避免的反模式

### ❌ 硬编码路径

```bash
# BAD
FILE="/Users/alice/.claude/my-plugin.local.md"

# GOOD
FILE=".claude/my-plugin.local.md"
```

### ❌ Unquoted Variables

```bash
# BAD
echo $VALUE

# GOOD
echo "$VALUE"
```

### ❌ Non-Atomic Updates

```bash
# BAD: Can corrupt file if interrupted
sed -i "s/field: .*/field: $VALUE/" "$FILE"

# GOOD: Atomic
TEMP_FILE="${FILE}.tmp.$$"
sed "s/field: .*/field: $VALUE/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### ❌ No Default Values

```bash
# BAD: Fails if field missing
if [[ $MAX -gt 100 ]]; then
  # MAX might be empty!
fi

# GOOD: Provide default
MAX=${MAX:-10}
```

### ❌ Ignoring Edge Cases

```bash
# BAD: Assumes exactly 2 --- markers
sed -n '/^---$/,/^---$/{ /^---$/d; p; }'

# GOOD: Handles --- in body
awk '/^---$/{i++; next} i>=2'  # For body
```

## 结论

`.claude/plugin-name.local.md` 模式提供:
- 简单、人类可读的配置
- 版本控制友好（gitignored）
- 每个项目的设置
- 使用标准 bash 工具轻松解析
- 支持结构化配置 (YAML) 和自由格式内容 (markdown)

对于任何需要用户可配置行为或状态持久化的插件，使用此模式。
