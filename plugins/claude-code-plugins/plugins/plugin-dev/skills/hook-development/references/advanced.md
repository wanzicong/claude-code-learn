# 高级 Hook 用例

本参考文档介绍了高级 hook 模式和技术，用于复杂的自动化工作流程。

## 多阶段验证

结合命令和 prompt hook 进行分层验证：

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/quick-check.sh",
          "timeout": 5
        },
        {
          "type": "prompt",
          "prompt": "bash 命令的深度分析：$TOOL_INPUT",
          "timeout": 15
        }
      ]
    }
  ]
}
```

**用例：** 快速确定性检查后进行智能分析

**示例 quick-check.sh.sh：**
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# 对安全命令立即批准
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami)$ ]]; then
  exit 0
fi

# 让 prompt hook 处理复杂情况
exit 0
```

命令 hook 快速批准明显安全的命令，而 prompt hook 分析其他所有内容。

## 条件 Hook 执行

根据环境或上下文执行 hook：

```bash
#!/bin/bash
# 仅在 CI 环境中运行
if [ -z "$CI" ]; then
  echo '{"continue": true}' # 在非 CI 环境中跳过
  exit 0
fi

# 在 CI 环境中运行验证逻辑
input=$(cat)
# ... 验证代码 ...
```

**用例：**
- CI 环境与本地开发环境的不同行为
- 项目特定验证
- 用户特定规则

**示例：为受信任用户跳过某些检查：**
```bash
#!/bin/bash
# 为管理员用户跳过详细检查
if [ "$USER" = "admin" ]; then
  exit 0
fi

# 为其他用户进行完整验证
input=$(cat)
# ... 验证代码 ...
```

## 通过状态链式调用 Hook

使用临时文件在 hook 之间共享状态：

```bash
# Hook 1：分析并保存状态
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# 分析命令
risk_level=$(calculate_risk "$command")
echo "$risk_level" > /tmp/hook-state-$$

exit 0
```

```bash
# Hook 2：使用保存的状态
#!/bin/bash
risk_level=$(cat /tmp/hook-state-$$ 2>/dev/null || echo "unknown")

if [ "$risk_level" = "high" ]; then
  echo "检测到高风险操作" >&2
  exit 2
fi
```

**重要：** 这仅适用于顺序 hook 事件（例如，PreToolUse 然后 PostToolUse），而不适用于并行 hook。

## 动态 Hook 配置

根据项目配置修改 hook 行为：

```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# 读取项目特定配置
if [ -f ".claude-hooks-config.json" ]; then
  strict_mode=$(jq -r '.strict_mode' .claude-hooks-config.json)

  if [ "$strict_mode" = "true" ]; then
    # 应用严格验证
    # ...
  else
    # 应用宽松验证
    # ...
  fi
fi
```

**示例 .claude-hooks-config.json：**
```json
{
  "strict_mode": true,
  "allowed_commands": ["ls", "pwd", "grep"],
  "forbidden_paths": ["/etc", "/sys"]
}
```

## 上下文感知 Prompt Hook

使用转录和会话上下文进行智能决策：

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "审查 $TRANSCRIPT_PATH 处的完整转录。检查：1) 代码更改后是否运行了测试？2) 构建是否成功？3) 是否回答了所有用户问题？4) 是否有未完成的工作？仅当所有操作完成时返回 'approve'。"
        }
      ]
    }
  ]
}
```

LLM 可以读取转录文件并做出上下文感知的决策。

## 性能优化

### 缓存验证结果

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
cache_key=$(echo -n "$file_path" | md5sum | cut -d' ' -f1)
cache_file="/tmp/hook-cache-$cache_key"

# 检查缓存
if [ -f "$cache_file" ]; then
  cache_age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file")))
  if [ "$cache_age" -lt 300 ]; then  # 5 分钟缓存
    cat "$cache_file"
    exit 0
  fi
fi

# 执行验证
result='{"decision": "approve"}'

# 缓存结果
echo "$result" > "$cache_file"
echo "$result"
```

### 并行执行优化

由于 hook 并行运行，请将它们设计为独立的：

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "bash check-size.sh",      // 独立
          "timeout": 2
        },
        {
          "type": "command",
          "command": "bash check-path.sh",      // 独立
          "timeout": 2
        },
        {
          "type": "prompt",
          "prompt": "检查内容安全性",     // 独立
          "timeout": 10
        }
      ]
    }
  ]
}
```

所有三个 hook 同时运行，从而减少总延迟。

## 跨事件工作流程

协调不同事件之间的 hook：

**SessionStart - 设置跟踪：**
```bash
#!/bin/bash
# 初始化会话跟踪
echo "0" > /tmp/test-count-$$
echo "0" > /tmp/build-count-$$
```

**PostToolUse - 跟踪事件：**
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

if [ "$tool_name" = "Bash" ]; then
  command=$(echo "$input" | jq -r '.tool_result')
  if [[ "$command" == *"test"* ]]; then
    count=$(cat /tmp/test-count-$$ 2>/dev/null || echo "0")
    echo $((count + 1)) > /tmp/test-count-$$
  fi
fi
```

**Stop - 基于跟踪验证：**
```bash
#!/bin/bash
test_count=$(cat /tmp/test-count-$$ 2>/dev/null || echo "0")

if [ "$test" -eq 0 ]; then
  echo '{"decision": "block", "reason": "没有运行测试"}' >&2
  exit 2
fi
```

## 与外部系统集成

### Slack 通知

```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
decision="blocked"

# 发送通知到 Slack
curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Hook ${decision} ${tool_name} 操作\"}" \
  2>/dev/null

echo '{"decision": "deny"}' >&2
exit 2
```

### 数据库记录

```bash
#!/bin/bash
input=$(cat)

# 记录到数据库
psql "$DATABASE_URL" -c "INSERT INTO hook_logs (event, data) VALUES ('PreToolUse', '$input')" \
  2>/dev/null

exit 0
```

### 指标收集

```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# 发送指标到监控系统
echo "hook.pretooluse.${tool_name}:1|c" | nc -u -w1 statsd.local 8125

exit 0
```

## 安全模式

### 速率限制

```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# 跟踪命令频率
rate_file="/tmp/hook-rate-$$"
current_minute=$(date +%Y%m%d%H%M)

if [ -f "$rate_file" ]; then
  last_minute=$(head -1 "$rate_file")
  count=$(tail -1 "$rate_file")

  if [ "$current_minute" = "$last_minute" ]; then
    if [ "$count" -gt 10 ]; then
      echo '{"decision": "deny", "reason": "超过速率限制"}' >&2
      exit 2
    fi
    count=$((count + 1))
  else
    count=1
  fi
else
  count=1
fi

echo "$current_minute" > "$rate_file"
echo "$count" >> "$rate_file"

exit 0
```

### 审计记录

```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
timestamp=$(date -Iseconds)

# 追加到审计日志
echo "$timestamp | $USER | $tool_name | $input" >> ~/.claude/audit.log

exit 0
```

### 密钥检测

```bash
#!/bin/bash
input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content')

# 检查常见密钥模式
if echo "$content" | grep -qE "(api[_-]?key|password|secret|token).{0,20}['\"]?[A-Za-z0-9]{20,}"; then
  echo '{"decision": "deny", "reason": "内容中检测到潜在密钥"}' >&2
  exit 2
fi

exit 0
```

## 测试高级 Hook

### 单元测试 Hook 脚本

```bash
# test-hook.sh
#!/bin/bash

# 测试 1：批准安全命令
result=$(echo '{"tool_input": {"command": "ls"}}' | bash validate-bash.sh)
if [ $? -eq 0 ]; then
  echo "✓ 测试 1 通过"
else
  echo "✗ 测试 1 失败"
fi

# 测试 2：阻止危险命令
result=$(echo '{"tool_input": {"command": "rm -rf /"}}' | bash validate-bash.sh)
if [ $? -eq 2 ]; then
  echo "✓ 测试 2 通过"
else
  echo "✗ 测试 2 失败"
fi
```

### 集成测试

创建测试场景以完整测试 hook 工作流程：

```bash
# integration-test.sh
#!/bin/bash

# 设置测试环境
export CLAUDE_PROJECT_DIR="/tmp/test-project"
export CLAUDE_PLUGIN_ROOT="$(pwd)"
mkdir -p "$CLAUDE_PROJECT_DIR"

# 测试 SessionStart hook
echo '{}' | bash hooks/session-start.sh
if [ -f "/tmp/session-initialized" ]; then
  echo "✓ SessionStart hook 工作"
else
  echo "✗ SessionStart hook 失败"
fi

# 清理
rm -rf "$CLAUDE_PROJECT_DIR"
```

## 高级 Hook 最佳实践

1. **保持 hook 独立：** 不要依赖执行顺序
2. **使用超时：** 为每种 hook 类型设置适当的限制
3. **优雅处理错误：** 提供清晰的错误消息
4. **记录复杂性：** 在 README 中解释高级模式
5. **彻底测试：** 覆盖边缘情况和失败模式
6. **监控性能：** 跟踪 hook 执行时间
7. **版本配置：** 对 hook 配置使用版本控制
8. **提供逃生机制：** 允许用户在需要时绕过 hook

## 常见陷阱

### ❌ 假设 Hook 顺序

```bash
# 坏：假设 hook 按特定顺序运行
# Hook 1 保存状态，Hook 2 读取它
# 这可能会失败，因为 hook 并行运行！
```

### ❌ 长时间运行的 Hook

```bash
# 坏：Hook 运行时间需要 2 分钟
sleep 120
# 这将超时并阻止工作流程
```

### ❌ 未捕获的异常

```bash
# 坏：脚本在意外输入时崩溃
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
cat "$file_path"  # 如果文件不存在则失败
```

### ✅ 正确的错误处理

```bash
# 好：优雅处理错误
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
if [ ! -f "$file_path" ]; then
  echo '{"continue": true, "systemMessage": "文件未找到，跳过检查"}' >&2
  exit 0
fi
```

## 结论

高级 hook 模式可以在保持可靠性和性能的同时实现复杂的自动化。当基本 hook 不足时使用这些技术，但始终优先考虑简单性和可维护性。
