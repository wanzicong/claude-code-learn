# 常见 Hook 模式

本参考文档提供了常见且经过验证的 Claude Code hook 实现模式。使用这些模式作为典型 hook 用例的起点。

## 模式 1：安全验证

使用基于 prompt 的 hook 阻止危险的文件写入：

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "文件路径：$TOOL_INPUT.file_path。验证：1) 不在 /etc 或系统目录中 2) 不是 .env 或凭据 3) 路径不包含 '..' 遍历。返回 'approve' 或 'deny'。"
        }
      ]
    }
  ]
}
```

**用于：** 防止写入敏感文件或系统目录。

## 模式 2：测试强制执行

确保在停止前运行测试：

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "审查转录。如果修改了代码（使用了 Write/Edit 工具），验证已执行测试。如果未运行测试，则以原因 '代码更改后必须运行测试' 阻止。"
        }
      ]
    }
  ]
}
```

**用于：** 强制执行质量标准并防止未完成的工作。

## 模式 3：上下文加载

在会话开始时加载项目特定上下文：

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

**示例脚本（load-context.sh）：**
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# 检测项目类型
if [ -f "package.json" ]; then
  echo "Node.js 项目检测"
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
elif [ -f "Cargo.toml" ]; then
  echo "Rust 项目检测"
  echo "export PROJECT_TYPE=rust" >> "$CLAUDE_ENV_FILE"
fi
```

**用于：** 自动检测和配置项目特定设置。

## 模式 4：通知记录

记录所有通知以进行审计或分析：

```json
{
  "Notification": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/log-notification.sh"
        }
      ]
    }
  ]
}
```

**用于：** 跟踪用户通知或与外部记录系统集成。

## 模式 5：MCP 工具监控

监控和验证 MCP 工具使用：

```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__.*__delete.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "检测到删除操作。验证：此删除是否为有意操作？可以撤消吗？是否有备份？仅在安全时返回 'approve'。"
        }
      ]
    }
  ]
}
```

**用于：** 防止破坏性 MCP 操作。

## 模式 6：构建验证

确保代码更改后项目能够构建：

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "检查是否修改了代码。如果使用了 Write/Edit 工具，验证项目已构建（npm run build、cargo build 等）。如果未构建，则阻止并请求构建。"
        }
      ]
    }
  ]
}
```

**用于：** 在提交或停止工作之前捕获构建错误。

## 模式 7：权限确认

在危险操作之前询问用户：

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "命令：$TOOL_INPUT.command。如果命令包含 'rm'、'delete'、'drop' 或其他破坏性操作，返回 'ask' 以向用户确认。否则返回 'approve'。"
        }
      ]
    }
  ]
}
```

**用于：** 对潜在破坏性命令进行用户确认。

## 模式 8：代码质量检查

在文件编辑上运行 linter 或 formatter：

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-quality.sh"
        }
      ]
    }
  ]
}
```

**示例脚本（check-quality.sh）：**
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# 如果适用，运行 linter
if [[ "$file_path" == *.js ]] || [[ "$file_path" == *.ts ]]; then
  npx eslint "$file_path" 2>&1 || true
fi
```

**用于：** 自动代码质量强制执行。

## 模式组合

组合多个模式以实现全面保护：

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
    },
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证 bash 命令安全性"
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
          "prompt": "验证已运行测试且构建成功"
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
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

这提供了多层保护和自动化。

## 模式 9：临时激活的 Hook

通过标志文件创建仅在明确启用时运行的 hook：

```bash
#!/bin/bash
# Hook 仅在标志文件存在时激活
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-security-scan"

if [ ! -f "$FLAG_FILE" ]; then
  # 禁用时快速退出
  exit 0
fi

# 标志存在，运行验证
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# 运行安全扫描
security-scanner "$file_path"
```

**激活：**
```bash
# 启用 hook
touch .enable-security-scan

# 禁用 hook
rm .enable-security-scan
```

**用于：**
- 临时调试 hook
- 开发功能标志
- 选择性加入的项目特定验证
- 仅在需要时进行性能密集检查

**注意：** 在创建/删除标志文件后必须重启 Claude Code，hook 才能识别更改。

## 模式 10：配置驱动的 Hook

使用 JSON 配置来控制 hook 行为：

```bash
#!/bin/bash
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/my-plugin.local.json"

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
  strict_mode=$(jq -r '.strictMode // false' "$CONFIG_FILE")
  max_file_size=$(jq -r '.maxFileSize // 1000000' "$CONFIG_FILE")
else
  # 默认值
  strict_mode=false
  max_file_size=1000000
fi

# 如果未处于严格模式则跳过
if [ "$strict_mode" != "true" ]; then
  exit 0
fi

# 应用配置的限制
input=$(cat)
file_size=$(echo "$input" | jq -r '.tool_input.content | length')

if [ "$file_size" -gt "$max_file_size" ]; then
  echo '{"decision": "deny", "reason": "文件超过配置的大小限制"}' >&2
  exit 2
fi
```

**配置文件（.claude/my-plugin.local.json）：**
```json
{
  "strictMode": true,
  "maxFileSize": 500000,
  "allowedPaths": ["/tmp", "/home/user/projects"]
}
```

**用于：**
- 用户可配置的 hook 行为
- 每项目设置
- 团队特定规则
- 动态验证标准
