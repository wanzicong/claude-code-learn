# 从基本 Hook 迁移到高级 Hook

本指南展示了如何从基本命令 hook 迁移到高级基于 prompt 的 hook，以提高可维护性和灵活性。

## 为什么要迁移？

基于 prompt 的 hook 提供了几个优势：

- **自然语言推理**：LLM 理解上下文和意图
- **更好的边缘情况处理**：适应意外场景
- **无需 bash 脚本**：更易于编写和维护
- **更灵活的验证**：无需编码即可处理复杂逻辑

## 迁移示例：Bash 命令验证

### 之前（基本命令 Hook）

**配置：**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash validate-bash.sh"
        }
      ]
    }
  ]
}
```

**脚本（validate-bash.sh）：**
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# 硬编码的验证逻辑
if [[ "$command" == *"rm -rf"* ]]; then
  echo "检测到危险命令" >&2
  exit 2
fi
```

**问题：**
- 仅检查精确的 "rm -rf" 模式
- 不会捕获 `rm -fr` 或 `rm -r -f` 等变体
- 错过其他危险命令（`dd`、`mkfs` 等）
- 无上下文感知
- 需要 bash 脚本知识

### 之后（高级 Prompt Hook）

**配置：**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "命令：$TOOL_INPUT.command。分析：1) 破坏性操作（rm -rf、dd、mkfs 等）2) 权限提升（sudo）3) 未经用户同意的网络操作。返回 'approve' 或 'deny' 并附带说明。",
          "timeout": 15
        }
      ]
    }
  ]
}
```

**优势：**
- 捕获所有变体和模式
- 理解意图，而不仅仅是字面字符串
- 无需脚本文件
- 易于使用新标准进行扩展
- 上下文感知决策
- 拒绝时的自然语言解释

## 迁移示例：文件写入验证

### 之前（基本命令 Hook）

**配置：**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "bash validate-write.sh"
        }
      ]
    }
  ]
}
```

**脚本（validate-write.sh）：**
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# 检查路径遍历
if [[ "$file_path" == *".."* ]]; then
  echo '{"decision": "deny", "reason": "检测到路径遍历"}' >&2
  exit 2
fi

# 检查系统路径
if [[ "$file_path" == "/etc/"* ]] || [[ "$file_path" == "/sys/"* ]]; then
  echo '{"decision": "deny", "reason": "系统文件"}' >&2
  exit 2
fi
```

**问题：**
- 硬编码的路径模式
- 不理解符号链接
- 缺少边缘情况（例如，`/etc` 与 `/etc/`）
- 未考虑文件内容

### 之后（高级 Prompt Hook）

**配置：**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "文件路径：$TOOL_INPUT.file_path。内容预览：$TOOL_INPUT.content（前 200 个字符）。验证：1) 不在 /etc 或系统目录中 2) 不是 .env 或凭据 3) 路径不包含 '..' 遍历 4) 内容不泄露密钥。返回 'approve' 或 'deny'。"
        }
      ]
    }
  ]
}
```

**优势：**
- 上下文感知（也考虑内容）
- 处理符号链接和边缘情况
- 自然理解"系统目录"
- 可以检测内容中的密钥
- 易于扩展标准

## 何时保留命令 Hook

命令 hook 仍有其用武之地：

### 1. 确定性性能检查

```bash
#!/bin/bash
# 快速检查文件大小
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
size=$(stat -f%z "$file_path" 2>/dev/null || stat -c%s "$file_path" 2>/dev/null)

if [ "$size" -gt 10000000 ]; then
  echo '{"decision": "deny", "reason": "文件太大"}' >&2
  exit 2
fi
```

**使用命令 hook，当：** 验证纯粹是数学或确定性的。

### 2. 外部工具集成

```bash
#!/bin/bash
# 运行安全扫描器
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
scan_result=$(security-scanner "$file_path")

if [ "$?" -ne 0 ]; then
  echo "安全扫描失败：$scan_result" >&2
  exit 2
fi
```

**使用命令 hook，当：** 集成提供是/否答案的外部工具。

### 3. 非常快速的检查（< 50ms）

```bash
#!/bin/bash
# 快速正则表达式检查
command=$(echo "$input" | jq -r '.tool_input.command')

if [[ "$command" =~ ^(ls|pwd|echo)$ ]]; then
  exit 0  # 安全命令
fi
```

**使用命令 hook，当：** 性能至关重要且逻辑简单。

## 混合方法

结合两者进行多阶段验证：

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

命令 hook 进行快速确定性检查，而 prompt hook 处理复杂推理。

## 迁移检查清单

迁移 hook 时：

- [ ] 识别命令 hook 中的验证逻辑
- [ ] 将硬编码模式转换为自然语言标准
- [ ] 使用旧 hook 错过的边缘情况进行测试
- [ ] 验证 LLM 理解意图
- [ ] 设置适当的超时（prompt hook 通常为 15-30s）
- [ ] 在 README 中记录新 hook
- [ ] 删除或归档旧脚本文件

## 迁移技巧

1. **从一个 hook 开始**：不要一次性迁移所有内容
2. **彻底测试**：验证 prompt hook 捕获了命令 hook 捕获的内容
3. **寻找改进机会**：将迁移作为增强验证的机会
4. **保留脚本以供参考**：归档旧脚本，以防需要参考逻辑
5. **记录推理过程**：在 README 中解释为什么 prompt hook 更好

## 完整迁移示例

### 原始插件结构

```
my-plugin/
├── .claude-plugin/plugin.json
├── hooks/hooks.json
└── scripts/
    ├── validate-bash.sh
    ├── validate-write.sh
    └── check-tests.sh
```

### 迁移后

```
my-plugin/
├── .claude-plugin/plugin.json
├── hooks/hooks.json      # 现在使用 prompt hook
└── scripts/              # 归档或删除
    └── archive/
        ├── validate-bash.sh
        ├── validate-write.sh
        └── check-tests.sh
```

### 更新的 hooks.json

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证 bash 命令安全性：破坏性操作、权限提升、网络访问"
        }
      ]
    },
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证文件写入安全性：系统路径、凭据、路径遍历、内容密钥"
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
          "prompt": "如果代码被修改，验证已运行测试"
        }
      ]
    }
  ]
}
```

**结果：** 更简单、更可维护、更强大。

## 常见迁移模式

### 模式：字符串包含 → 自然语言

**之前：**
```bash
if [[ "$command" == *"sudo"* ]]; then
  echo "权限提升" >&2
  exit 2
fi
```

**之后：**
```
"检查权限提升（sudo、su 等）"
```

### 模式：正则表达式 → 意图

**之前：**
```bash
if [[ "$file" =~ \.(env|secret|key|token)$ ]]; then
  echo "凭据文件" >&2
  exit 2
fi
```

**之后：**
```
"验证未写入凭据文件（.env、secrets、keys、tokens）"
```

### 模式：多个条件 → 标准列表

**之前：**
```bash
if [ condition1 ] || [ condition2 ] || [ condition3 ]; then
  echo "无效" >&2
  exit 2
fi
```

**之后：**
```
"检查：1) condition1 2) condition2 3) conditionally。如果任何条件失败则拒绝。"
```

## 结论

迁移到基于 prompt 的 hook 使插件更可维护、更灵活、更强大。保留命令 hook 用于确定性检查和外部工具集成。
