---
name: Hook Development
description: 当用户请求"创建 hook"、"添加 PreToolUse/PostToolUse/Stop hook"、"验证工具使用"、"实现基于提示词的 hook"、"使用 ${CLAUDE_PLUGIN_ROOT}"、"设置事件驱动的自动化"、"阻止危险命令"或提及 hook 事件（PreToolUse、PostToolUse、Stop、SubagentStop、SessionStart、SessionEnd、UserPromptSubmit、PreCompact、Notification）时，应使用此技能。为创建和实现 Claude Code 插件 hook 提供全面指导，重点关注高级基于提示词的 hook API。
version: 0.1.0
---

# Claude Code 插件的 Hook 开发

## 概述

Hook 是响应 Claude Code 事件执行的事件驱动自动化脚本。使用 hook 来验证操作、强制执行策略、添加上下文，并将外部工具集成到工作流程中。

**核心功能：**
- 在执行前验证工具调用（PreToolUse）
- 响应工具结果（PostToolUse）
- 强制执行完成标准（Stop、SubagentStop）
- 加载项目上下文（SessionStart）
- 在开发生命周期中自动化工作流程

## Hook 类型

### 基于 Prompt 的 Hook（推荐）

使用 LLM 驱动的决策制定来实现上下文感知的验证：

```json
{
  "type": "prompt",
  "prompt": "评估此工具使用是否合适：$TOOL_INPUT",
  "timeout": 30
}
```

**支持的事件：** Stop、SubagentStop、UserPromptSubmit、PreToolUse

**优势：**
- 基于自然语言推理的上下文感知决策
- 灵活的评估逻辑，无需 bash 脚本
- 更好的边缘情况处理
- 更易于维护和扩展

### 命令 Hook

执行 bash 命令进行确定性检查：

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**用于：**
- 快速确定性验证
- 文件系统操作
- 外部工具集成
- 性能关键检查

## Hook 配置格式

### 插件 hooks.json 格式

**对于插件 hook**，在 `hooks/hooks.json` 中使用包装格式：

```json
{
  "description": "hook 的简要说明（可选）",
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

**关键点：**
- `description` 字段是可选的
- `hooks` 字段是必需的包装器，包含实际的 hook 事件
- 这是**插件专用格式**

**示例：**
```json
{
  "description": "代码质量验证 hook",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### 设置格式（直接）

**对于用户设置**，在 `.claude/settings.json` 中使用直接格式：

```json
{
  "PreToolUse": [...],
  "Stop": [...],
  "SessionStart": [...]
}
```

**关键点：**
- 无包装器 - 事件直接在顶层
- 无 description 字段
- 这是**设置格式**

**重要：** 下面的示例显示的是进入任一格式的 hook 事件结构。对于插件 hooks.json，将这些包装在 `{"hooks": {...}}` 中。

## Hook 事件

### PreToolUse

在任何工具运行前执行。用于批准、拒绝或修改工具调用。

**示例（基于 prompt）：**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证文件写入安全性。检查：系统路径、凭据、路径遍历、敏感内容。返回 'approve' 或 'deny'。"
        }
      ]
    }
  ]
}
```

**PreToolUse 的输出：**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "给 Claude 的解释"
}
```

### PostToolUse

在工具完成后执行。用于响应结果、提供反馈或记录日志。

**示例：**
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "分析编辑结果是否存在潜在问题：语法错误、安全漏洞、破坏性更改。提供反馈。"
        }
      ]
    }
  ]
}
```

**输出行为：**
- 退出码 0：stdout 显示在转录中
- 退出码 2：stderr 反馈给 Claude
- systemMessage 包含在上下文中

### Stop

当主代理考虑停止时执行。用于验证完整性。

**示例：**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证任务完成：测试运行、构建成功、问题已回答。返回 'approve' 以停止或返回 'block' 并给出原因以继续。"
        }
      ]
    }
  ]
}
```

**决策输出：**
```json
{
  "decision": "approve|block",
  "reason": "解释",
  "systemMessage": "附加上下文"
}
```

### SubagentStop

当子代理考虑停止时执行。用于确保子代理完成了其任务。

与 Stop hook 类似，但用于子代理。

### UserPromptSubmit

当用户提交提示词时执行。用于添加上下文、验证或阻止提示词。

**示例：**
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "检查提示词是否需要安全指导。如果讨论 auth、权限或 API 安全，返回相关警告。"
        }
      ]
    }
  ]
}
```

### SessionStart

当 Claude Code 会话开始时执行。用于加载上下文和设置环境。

**示例：**
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

**特殊功能：** 使用 `$CLAUDE_ENV_FILE` 持久化环境变量：
```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

参见 `examples/load-context.sh` 获取完整示例。

### SessionEnd

当会话结束时执行。用于清理、记录和状态保留。

### PreCompact

在上下文压缩前执行。用于添加要保留的关键信息。

### Notification

当 Claude 发送通知时执行。用于响应用户通知。

## Hook 输出格式

### 标准输出（所有 Hook）

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "给 Claude 的消息"
}
```

- `continue`：如果为 false，停止处理（默认为 true）
- `suppressOutput`：从转录中隐藏输出（默认为 false）
- `systemMessage`：显示给 Claude 的消息

### 退出码

- `0` - 成功（stdout 显示在转录中）
- `2` - 阻止错误（stderr 反馈给 Claude）
- 其他 - 非阻止错误

## Hook 输入格式

所有 hook 通过 stdin 接收 JSON，包含通用字段：

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

**事件特定字段：**

- **PreToolUse/PostToolUse：** `tool_name`、`tool_input`、`tool_result`
- **UserPromptSubmit：** `user_prompt`
- **Stop/SubagentStop：** `reason`

在 prompt 中使用 `$TOOL_INPUT`、`$TOOL_RESULT`、`$USER_PROMPT` 等访问字段。

## 环境变量

在所有命令 hook 中可用：

- `$CLAUDE_PROJECT_DIR` - 项目根路径
- `$CLAUDE_PLUGIN_ROOT` - 插件目录（用于可移植路径）
- `$CLAUDE_ENV_FILE` - 仅 SessionStart：在此持久化环境变量
- `$CLAUDE_CODE_REMOTE` - 如果在远程上下文中运行则设置

**始终在 hook 命令中使用 ${CLAUDE_PLUGIN_ROOT} 以确保可移植性：**

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

## 插件 Hook 配置

在插件中，在 `hooks/hooks.json` 中定义 hook：

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证文件写入安全性"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证任务完成"
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
          "timeout": 10
        }
      ]
    }
 }
}
```

插件 hook 与用户的 hook 合并并并行运行。

## 匹配器

### 工具名称匹配

**精确匹配：**
```json
"matcher": "Write"
```

**多个工具：**
```json
"matcher": "Read|Write|Edit"
```

**通配符（所有工具）：**
```json
"matcher": "*"
```

**正则表达式模式：**
```json
"matcher": "mcp__.*__delete.*"  // 所有 MCP 删除工具
```

**注意：** 匹配器区分大小写。

### 常见模式

```json
// 所有 MCP 工具
"matcher": "mcp__.*"

// 特定插件的 MCP 工具
"matcher": "mcp__plugin_asana_.*"

// 所有文件操作
"matcher": "Read|Write|Edit"

// 仅 Bash 命令
"matcher": "Bash"
```

## 安全最佳实践

### 输入验证

始终在命令 hook 中验证输入：

```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# 验证工具名称格式
if [[ ! "$tool_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo '{"decision": "deny", "reason": "无效的工具名称"}' >&2
  exit 2
fi
```

### 路径安全

检查路径遍历和敏感文件：

```bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# 拒绝路径遍历
if [[ "$file_path" == *".."* ]]; then
  echo '{"decision": "deny", "reason": "检测到路径遍历"}' >&2
  exit 2
fi

# 拒绝敏感文件
if [[ "$file_path" == *".env"* ]]; then
  echo '{"decision": "deny", "reason": "敏感文件"}' >&2
  exit 2
fi
```

参见 `examples/validate-write.sh` 和 `examples/validate-bash.sh` 获取完整示例。

### 引用所有变量

```bash
# 好：已引用
echo "$file_path"
cd "$CLAUDE_PROJECT_DIR"

# 坏：未引用（注入风险）
echo $file_path
cd $CLAUDE_PROJECT_DIR
```

### 设置适当的超时

```json
{
  "type": "command",
  "command": "bash script.sh",
  "timeout": 10
}
```

**默认值：** 命令 hook（60s），Prompt hook（30s）

## 性能考虑

### 并行执行

所有匹配的 hook **并行运行**：

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {"type": "command", "command": "check1.sh"},  // 并行
        {"type": "command", "command": "check2.sh"},  // 并行
        {"type": "prompt", "prompt": "验证..."}   // 并行
      ]
    }
  ]
}
```

**设计影响：**
- Hook 看不到彼此的输出
- 非确定性顺序
- 设计为独立

### 优化

1. 使用命令 hook 进行快速确定性检查
2. 使用 prompt hook 进行复杂推理
3. 在临时文件中缓存验证结果
4. 最小化热路径中的 I/O

## 临时激活的 Hook

通过检查标志文件或配置来创建条件激活的 hook：

**模式：标志文件激活**
```bash
#!/bin/bash
# 仅当标志文件存在时才激活
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"

if [ ! -f "$FLAG_FILE" ]; then
  # 标志不存在，跳过验证
  exit 0
fi

# 标志存在，运行验证
input=$(cat)
# ... 验证逻辑 ...
```

**模式：基于配置的激活**
```bash
#!/bin/bash
# 检查配置以进行激活
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/plugin-config.json"

if [ -f "$CONFIG_FILE" ]; then
  enabled=$(jq -r '.strictMode // false' "$CONFIG_FILE")
  if [ "$enabled" != "true" ]; then
    exit 0  # 未启用，跳过
  fi
fi

# 已启用，运行 hook 逻辑
input=$(cat)
# ... hook 逻辑 ...
```

**用例：**
- 仅在需要时启用严格验证
- 临时调试 hook
- 项目特定的 hook 行为
- Hook 的功能标志

**最佳实践：** 在插件 README 中记录激活机制，以便用户知道如何启用/禁用临时 hook。

## Hook 生命周期和限制

### Hook 在会话开始时加载

**重要：** Hook 在 Claude Code 会话启动时加载。更改 hook 配置需要重启 Claude Code。

**无法热交换 hook：**
- 编辑 `hooks/hooks.json` 不会影响当前会话
- 添加新的 hook 脚本不会被识别
- 更改 hook 命令/prompt 不会更新
- 必须重启 Claude Code：退出并再次运行 `claude`

**测试 hook 更改：**
1. 编辑 hook 配置或脚本
2. 退出 Claude Code 会话
3. 重启：`claude` 或 `cc`
4. 新的 hook 配置加载
5. 使用 `claude --debug` 测试 hook

### 启动时的 Hook 验证

Hook 在 Claude Code 启动时验证：
- hooks.json 中的无效 JSON 导致加载失败
- 缺失脚本导致警告
- 在调试模式下报告语法错误

使用 `/hooks` 命令查看当前会话中加载的 hook。

## 调试 Hook

### 启用调试模式

```bash
claude --debug
```

查找 hook 注册、执行日志、输入/输出 JSON 和时序信息。

### 测试 Hook 脚本

直接测试命令 hook：

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "/test"}}' | \
  bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh

echo "退出码：$?"
```

### 验证 JSON 输出

确保 hook 输出有效的 JSON：

```bash
output=$(./your-hook.sh < test-input.json)
echo "$output" | jq .
```

## 快速参考

### Hook 事件摘要

| 事件 | 何时 | 用于 |
|-------|------|---------|
| PreToolUse | 工具之前 | 验证、修改 |
| PostToolUse | 工具之后 | 反馈、记录 |
| UserPromptSubmit | 用户输入 | 上下文、验证 |
| Stop | 代理停止 | 完整性检查 |
| SubagentStop | 子代理完成 | 任务验证 |
| SessionStart | 会话开始 | 上下文加载 |
| SessionEnd | 会话结束 | 清理、记录 |
| PreCompact | 压缩之前 | 保留上下文 |
| Notification | 用户通知 | 记录、响应 |

### 最佳实践

**应该：**
- ✅ 对于复杂逻辑使用基于 prompt 的 hook
- ✅ 使用 ${CLAUDE_PLUGIN_ROOT} 确保可移植性
- ✅ 在命令 hook 中验证所有输入
- ✅ 引用所有 bash 变量
- ✅ 设置适当的超时
- ✅ 返回结构化的 JSON 输出
- ✅ 彻底测试 hook

**不应：**
- ❌ 使用硬编码路径
- ❌ 未经验证信任用户输入
- ❌ 创建长时间运行的 hook
- ❌ 依赖 hook 执行顺序
- ❌ 不可预测地修改全局状态
- ❌ 记录敏感信息

## 其他资源

### 参考文件

有关详细模式和高级技术，请查阅：

- **`references/patterns.md`** - 常见 hook 模式（8+ 已验证模式）
- **`references/migration.md`** - 从基本 hook 迁移到高级 hook
- **`references/advanced.md`** - 高级用例和技术

### 示例 Hook 脚本

`examples/` 中的工作示例：

- **`validate-write.sh`** - 文件写入验证示例
- **`validate-bash.sh`** - Bash 命令验证示例
- **`load-context.sh`** - SessionStart 上下文加载示例

### 实用脚本

`scripts/` 中的开发工具：

- **`validate-hook-schema.sh`** - 验证 hooks.json 结构和语法
- **`test-hook.sh`** - 在部署前使用示例输入测试 hook
- **`hook-linter.sh`** - 检查 hook 脚本的常见问题和最佳实践

### 外部资源

- **官方文档**: https://docs.claude.com/en/docs/claude-code/hooks
- **示例**: 参见市场中的 security-guidance 插件
- **测试**: 使用 `claude --debug` 获取详细日志
- **验证**: 使用 `jq` 验证 hook JSON 输出

## 实现工作流程

要在插件中实现 hook：

1. 确定要 hook 的事件（PreToolUse、Stop、SessionStart 等）
2. 在基于 prompt（灵活）或命令（确定性）hook 之间做决定
3. 在 `hooks/hooks.json` 中编写 hook 配置
4. 对于命令 hook，创建 hook 脚本
5. 使用 ${CLAUDE_PLUGIN_ROOT} 进行所有文件引用
6. 使用 `scripts/validate-hook-schema.sh hooks/hooks.json` 验证配置
7. 使用 `scripts/test-hook.sh` 在部署前测试 hook
8. 使用 `claude --debug` 在 Claude Code 中测试
9. 在插件 README 中记录 hook

对于大多数用例，专注于基于 prompt 的 hook。保留命令 hook 用于性能关键或确定性检查。
