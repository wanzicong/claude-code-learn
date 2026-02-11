---
name: writing-hookify-rules
description: 当用户要求"创建 hookify 规则"、"编写钩子规则"、"配置 hookify"、"添加 hookify 规则"或需要 hookify 规则语法和模式的指导时，应使用此技能。
version: 0.1.0
---

# 编写 Hookify 规则

## 概述

Hookify 规则是带有 YAML 前置数据的 markdown 文件，定义要监视的模式以及当这些模式匹配时显示的消息。规则存储在 `.claude/hookify.{rule-name}.local.md` 文件中。

## 规则文件格式

### 基本结构

```markdown
---
name: rule-identifier
enabled: true
event: bash|file|stop|prompt|all
pattern: regex-pattern-here
---

当此规则触发时向 Claude 显示的消息。
可以包括 markdown 格式、警告、建议等。
```

### 前置数据字段

**name**（必需）：规则的唯一标识符
- 使用 kebab-case：`warn-dangerous-rm`、`block-console-log`
- 具有描述性和以动作为导向
- 以动词开头：warn、prevent、block、require、check

**enabled**（必需）：布尔值以激活/停用
- `true`：规则是活跃的
- `false`：规则已禁用（不会触发）
- 可以切换而无需删除规则

**event**（必需）：在哪个钩子事件上触发
- `bash`：Bash 工具命令
- `file`：Edit、Write、MultiEdit 工具
- `stop`：当代理想要停止时
- `prompt`：当用户提交提示时
- `all`：所有事件

**action**（可选）：规则匹配时做什么
- `warn`：显示消息但允许操作（默认）
- `block`：阻止操作（PreToolUse）或停止会话（Stop 事件）
- 如果省略，默认为 `warn`

**pattern**（简单格式）：要匹配的正则表达式模式
- 用于简单的单条件规则
- 匹配 command（bash）或 new_text（file）
- Python 正则表达式语法

**示例：**
```yaml
event: bash
pattern: rm\s+-rf
```

### 高级格式（多个条件）

对于具有多个条件的复杂规则：

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

您正在向 .env 文件添加 API 密钥。确保此文件在 .gitignore 中！
```

**条件字段：**
- `field`：检查哪个字段
  - 对于 bash：`command`
  - 对于 file：`file_path`、`new_text`、`old_text`、`content`
- `operator`：如何匹配
  - `regex_match`：正则表达式模式匹配
  - `contains`：子字符串检查
  - `equals`：精确匹配
  - `not_contains`：子字符串必须不存在
  - `starts_with`：前缀检查
  - `ends_with`：后缀检查
- `pattern`：要匹配的模式或字符串

**所有条件必须匹配规则才会触发。**

## 消息正文

前置数据后的 markdown 内容在规则触发时显示给 Claude。

**好的消息：**
- 解释检测到的内容
- 解释为什么有问题
- 建议替代方案或最佳实践
- 使用格式以提高清晰度（粗体、列表等）

**示例：**
```markdown
⚠️ **检测到 Console.log！**

您正在向生产代码添加 console.log。

**为什么这很重要：**
- 调试日志不应发送到生产
- Console.log 可能暴露敏感数据
- 影响浏览器性能

**替代方案：**
- 使用适当的日志库
- 提交前删除
- 使用条件调试构建
```

## 事件类型指南

### bash 事件

匹配 Bash 命令模式：

```markdown
---
event: bash
pattern: sudo\s+|rm\s+-rf|chmod\s+777
---

检测到危险命令！
```

**常见模式：**
- 危险命令：`rm\s+-rf`、`dd\s+if=`、`mkfs`
- 权限提升：`sudo\s+`、`su\s+`
- 权限问题：`chmod\s+777`、`chown\s+root`

### file 事件

匹配 Edit/Write/MultiEdit 操作：

```markdown
---
event: file
pattern: console\.log\(|eval\(|innerHTML\s*=
---

检测到可能有问题的代码模式！
```

**匹配不同字段：**
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

TypeScript 文件中的 Console.log！
```

**常见模式：**
- 调试代码：`console\.log\(`、`debugger`、`print\(`
- 安全风险：`eval\(`、`innerHTML\s*=`、`dangerouslySetInnerHTML`
- 敏感文件：`\.env$`、`credentials`、`\.pem$`
- 生成的文件：`node_modules/`、`dist/`、`build/`

### stop 事件

匹配代理想要停止时（完成检查）：

```markdown
---
event: stop
pattern: .*
---

停止前，验证：
- [ ] 已运行测试
- [ ] 构建成功
- [ ] 文档已更新
```

**用于：**
- 关于所需步骤的提醒
- 完成检查清单
- 流程执行

### prompt 事件

匹配用户提示内容（高级）：

```markdown
---
event: prompt
conditions:
  - field: user_prompt
    operator: contains
    pattern: deploy to production
---

生产部署检查清单：
- [ ] 测试通过？
- [ ] 团队审查？
- [ ] 监控准备？
```

## 模式编写提示

### 正则表达式基础

**字面字符：** 大多数字符匹配自身
- `rm` 匹配 "rm"
- `console.log` 匹配 "console.log"

**特殊字符需要转义：**
- `.`（任何字符）→ `\.`（字面量点）
- `(` `)` → `\(` `\)`（字面量括号）
- `[` `]` → `\[` `\]`（字面量方括号）

**常见元字符：**
- `\s` - 空白字符（空格、制表符、换行符）
- `\d` - 数字（0-9）
- `\w` - 单词字符（a-z、A-Z、0-9、_）
- `.` - 任何字符
- `+` - 一个或多个
- `*` - 零个或多个
- `?` - 零个或一个
- `|` - OR

**示例：**
```
rm\s+-rf         匹配：rm -rf、rm  -rf
console\.log\(   匹配：console.log(
(eval|exec)\(    匹配：eval( 或 exec(
chmod\s+777      匹配：chmod 777、chmod  777
API_KEY\s*=      匹配：API_KEY=、API_KEY =
```

### 测试模式

使用前测试正则表达式模式：

```bash
python3 -c "import re; print(re.search(r'your_pattern', 'test text'))"
```

或使用在线正则表达式测试器（regex101.com 使用 Python 风格）。

### 常见陷阱

**太宽泛：**
```yaml
pattern: log    # 匹配 "log"、"login"、"dialog"、"catalog"
```
更好：`console\.log\(|logger\.`

**太具体：**
```yaml
pattern: rm -rf /tmp  # 只匹配精确路径
```
更好：`rm\s+-rf`

**转义问题：**
- YAML 引用字符串：`"pattern"` 需要双反斜杠 `\\s`
- YAML 未引用：`pattern: \s` 按原样工作
- **建议**：在 YAML 中使用未引用的模式

## 文件组织

**位置：** 所有规则在 `.claude/` 目录中
**命名：** `.claude/hookify.{descriptive-name}.local.md`
**Gitignore：** 将 `.claude/*.local.md` 添加到 `.gitignore`

**好的名称：**
- `hookify.dangerous-rm.local.md`
- `hookify.console-log.local.md`
- `hookify.require-tests.local.md`
- `hookify.sensitive-files.local.md`

**坏的名称：**
- `hookify.rule1.local.md`（不具有描述性）
- `hookify.md`（缺少 .local）
- `danger.local.md`（缺少 hookify 前缀）

## 工作流程

### 创建规则

1. 识别不良行为
2. 确定涉及哪个工具（Bash、Edit 等）
3. 选择事件类型（bash、file、stop 等）
4. 编写正则表达式模式
5. 在项目根目录创建 `.claude/hookify.{name}.local.md` 文件
6. 立即测试 - 规则在下次工具使用时动态读取

### 完善规则

1. 编辑 `.local.md` 文件
2. 调整模式或消息
3. 立即测试 - 更改在下次工具使用时生效

### 禁用规则

**临时：** 在前置数据中设置 `enabled: false`
**永久：** 删除 `.local.md` 文件

## 示例

查看 `${CLAUDE_PLUGIN_ROOT}/examples/` 获取完整示例：
- `dangerous-rm.local.md` - 阻止危险的 rm 命令
- `console-log-warning.local.md` - 警告 console.log
- `sensitive-files-warning.local.md` - 警告编辑 .env 文件

## 快速参考

**最小可行规则：**
```markdown
---
name: my-rule
enabled: true
event: bash
pattern: dangerous_command
---

警告消息在此
```

**带条件的规则：**
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

警告消息
```

**事件类型：**
- `bash` - Bash 命令
- `file` - 文件编辑
- `stop` - 完成检查
- `prompt` - 用户输入
- `all` - 所有事件

**字段选项：**
- Bash：`command`
- File：`file_path`、`new_text`、`old_text`、`content`
- Prompt：`user_prompt`

**操作符：**
- `regex_match`、`contains`、`equals`、`not_contains`、`starts_with`、`ends_with`
