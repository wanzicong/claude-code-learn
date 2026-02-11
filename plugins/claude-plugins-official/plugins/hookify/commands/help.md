---
description: 获取 hookify 插件的帮助
allowed-tools: ["Read"]
---

# Hookify 插件帮助

解释 hookify 插件的工作原理以及如何使用它。

## 概述

hookify 插件使创建自定义钩子变得简单，以防止不良行为。用户无需编辑 `hooks.json` 文件，而是创建简单的 markdown 配置文件来定义要监视的模式。

## 工作原理

### 1. 钩子系统

Hookify 安装在这些事件上运行的通用钩子：
- **PreToolUse**：在任何工具执行之前（Bash、Edit、Write 等）
- **PostToolUse**：在工具执行之后
- **Stop**：当 Claude 想要停止工作时
- **UserPromptSubmit**：当用户提交提示时

这些钩子从 `.claude/hookify.*.local.md` 读取配置文件，并检查是否有任何规则与当前操作匹配。

### 2. 配置文件

用户在 `.claude/hookify.{rule-name}.local.md` 文件中创建规则：

```markdown
---
name: warn-dangerous-rm
enabled: true
event: bash
pattern: rm\s+-rf
---

⚠️ **检测到危险的 rm 命令！**

此命令可能删除重要文件。请验证路径。
```

**关键字段：**
- `name`：规则的唯一标识符
- `enabled`：true/false 以激活/停用
- `event`：bash、file、stop、prompt 或 all
- `pattern`：要匹配的正则表达式模式

消息正文是规则触发时 Claude 看到的内容。

### 3. 创建规则

**选项 A：使用 /hookify 命令**
```
/hookify 不要在生产文件中使用 console.log
```

这会分析您的请求并创建适当的规则文件。

**选项 B：手动创建**
使用上述格式创建 `.claude/hookify.my-rule.local.md`。

**选项 C：分析对话**
```
/hookify
```

不带参数，hookify 会分析最近的对话以发现您想要防止的行为。

## 可用命令

- **`/hookify`** - 从对话分析或明确指令创建钩子
- **`/hookify:help`** - 显示此帮助（您现在正在阅读的内容）
- **`/hookify:list`** - 列出所有已配置的钩子
- **`/hookify:configure`** - 交互式启用/禁用现有钩子

## 示例用例

**防止危险命令：**
```markdown
---
name: block-chmod-777
enabled: true
event: bash
pattern: chmod\s+777
---

不要使用 chmod 777 - 这是一个安全风险。使用特定权限代替。
```

**警告调试代码：**
```markdown
---
name: warn-console-log
enabled: true
event: file
pattern: console\.log\(
---

检测到 Console.log。记得在提交前删除调试日志。
```

**停止前要求测试：**
```markdown
---
name: require-tests
enabled: true
event: stop
pattern: .*
---

完成前是否运行了测试？确保执行了 `npm test` 或等效命令。
```

## 模式语法

使用 Python 正则表达式语法：
- `\s` - 空白字符
- `\.` - 字面量点
- `|` - OR
- `+` - 一个或多个
- `*` - 零个或多个
- `\d` - 数字
- `[abc]` - 字符类

**示例：**
- `rm\s+-rf` - 匹配 "rm -rf"
- `console\.log\(` - 匹配 "console.log("
- `(eval|exec)\(` - 匹配 "eval(" 或 "exec("
- `\.env$` - 匹配以 .env 结尾的文件

## 重要说明

**无需重启**：Hookify 规则（`.local.md` 文件）在下次工具使用时立即生效。Hookify 钩子已加载并动态读取您的规则。

**阻止或警告**：规则可以 `block`（阻止）操作（阻止执行）或 `warn`（警告）（显示消息但允许）。在规则的前置数据中设置 `action: block` 或 `action: warn`。

**规则文件**：将规则保存在 `.claude/hookify.*.local.md` 中 - 它们应被 git 忽略（如需要，添加到 .gitignore）。

**禁用规则**：在前置数据中设置 `enabled: false` 或删除文件。

## 故障排除

**钩子未触发：**
- 检查规则文件是否在 `.claude/` 目录中
- 验证前置数据中有 `enabled: true`
- 确认模式是有效的正则表达式
- 测试模式：`python3 -c "import re; print(re.search('your_pattern', 'test_text'))"`
- 规则立即生效 - 无需重启

**导入错误：**
- 检查 Python 3 可用：`python3 --version`
- 验证 hookify 插件安装正确

**模式不匹配：**
- 单独测试正则表达式
- 检查转义问题（在 YAML 中使用未引用的模式）
- 先尝试更简单的模式，然后改进

## 入门指南

1. 创建您的第一个规则：
   ```
   /hookify 当我尝试使用 rm -rf 时警告我
   ```

2. 尝试触发它：
   - 要求 Claude 运行 `rm -rf /tmp/test`
   - 您应该看到警告

4. 通过编辑 `.claude/hookify.warn-rm.local.md` 完善规则

5. 当遇到不良行为时创建更多规则

更多示例，请查看 `${CLAUDE_PLUGIN_ROOT}/examples/` 目录。
