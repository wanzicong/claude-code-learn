---
description: 从对话分析或明确指令创建钩子以防止不良行为
argument-hint: 可选的特定行为以解决
allowed-tools: ["Read", "Write", "AskUserQuestion", "Task", "Grep", "TodoWrite", "Skill"]
---

# Hookify - 从不良行为创建钩子

**首先：使用 Skill 工具加载 hookify:writing-rules 技能** 以了解规则文件格式和语法。

通过分析对话或根据明确的用户指令创建钩子规则以防止有问题行为。

## 您的任务

您将帮助用户创建 hookify 规则以防止不良行为。按照以下步骤：

### 步骤 1：收集行为信息

**如果提供了 $ARGUMENTS：**
- 用户给出了明确的指令：`$ARGUMENTS`
- 仍然分析最近的对话（最后 10-15 条用户消息）以获取额外上下文
- 查找行为发生的示例

**如果 $ARGUMENTS 为空：**
- 启动 conversation-analyzer 代理以发现有问题的行为
- 代理将扫描用户提示以查找挫折信号
- 代理将返回结构化发现

**分析对话：**
使用 Task 工具启动 conversation-analyzer 代理：
```
{
  "subagent_type": "general-purpose",
  "description": "分析对话以查找不良行为",
  "prompt": "您正在分析 Claude Code 对话以查找用户想要防止的行为。

读取当前对话中的用户消息并识别：
1. 明确避免某事的请求（\"不要做 X\"，\"停止做 Y\"）
2. 更正或恢复（用户修复 Claude 的操作）
3. 沮丧的反应（\"为什么你做了 X？\"，\"我没有要求那个\"）
4. 重复问题（同一问题多次）

对于每个发现的问题，提取：
- 使用了什么工具（Bash、Edit、Write 等）
- 特定模式或命令
- 为什么有问题
- 用户陈述的原因

以结构化列表返回发现，包含：
- category：问题类型
- tool：涉及哪个工具
- pattern：正则表达式或字面量模式以匹配
- context：发生了什么
- severity：high/medium/low

专注于最近的问题（最后 20-30 条消息）。除非明确要求，否则不要回溯更远。"
}
```

### 步骤 2：向用户展示发现

收集行为（来自参数或代理）后，使用 AskUserQuestion 向用户展示：

**问题 1：要 hookify 哪些行为？**
- 标题："创建规则"
- multiSelect：true
- 选项：列出每个检测到的行为（最多 4 个）
  - 标签：简短描述（例如，"阻止 rm -rf"）
  - 描述：为什么有问题

**问题 2：对于每个选定的行为，询问操作：**
- "这应该阻止操作还是只是警告？"
- 选项：
  - "只是警告"（action: warn - 显示消息但允许）
  - "阻止操作"（action: block - 阻止执行）

**问题 3：询问示例模式：**
- "什么模式应该触发此规则？"
- 显示检测到的模式
- 允许用户完善或添加更多

### 步骤 3：生成规则文件

对于每个确认的行为，创建一个 `.claude/hookify.{rule-name}.local.md` 文件：

**规则命名约定：**
- 使用 kebab-case
- 具有描述性：`block-dangerous-rm`、`warn-console-log`、`require-tests-before-stop`
- 以动作动词开头：block、warn、prevent、require

**文件格式：**
```markdown
---
name: {rule-name}
enabled: true
event: {bash|file|stop|prompt|all}
pattern: {regex pattern}
action: {warn|block}
---

{规则触发时向 Claude 显示的消息}
```

**操作值：**
- `warn`：显示消息但允许操作（默认）
- `block`：阻止操作或停止会话

**对于更复杂的规则（多个条件）：**
```markdown
---
name: {rule-name}
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

{警告消息}
```

### 步骤 4：创建文件并确认

**重要**：规则文件必须在当前工作目录的 `.claude/` 文件夹中创建，而不是插件目录。

使用当前工作目录（启动 Claude Code 的地方）作为基本路径。

1. 检查当前工作目录中是否存在 `.claude/` 目录
   - 如果不存在，首先创建：`mkdir -p .claude`

2. 使用 Write 工具创建每个 `.claude/hookify.{name}.local.md` 文件
   - 使用从当前工作目录的相对路径：`.claude/hookify.{name}.local.md`
   - 路径应解析到项目的 .claude 目录，而不是插件的

3. 向用户显示创建的内容：
   ```
   已创建 3 个 hookify 规则：
   - .claude/hookify.dangerous-rm.local.md
   - .claude/hookify.console-log.local.md
   - .claude/hookify.sensitive-files.local.md

   这些规则将在以下情况触发：
   - dangerous-rm: 匹配 "rm -rf" 的 Bash 命令
   - console-log: 添加 console.log 语句的编辑
   - sensitive-files: 对 .env 或凭据文件的编辑
   ```

4. 通过列出文件来验证文件是否在正确位置创建

5. 通知用户：**"规则立即生效 - 无需重启！"**

   Hookify 钩子已加载，将在下次工具使用时读取您的新规则。

## 事件类型参考

- **bash**：匹配 Bash 工具命令
- **file**：匹配 Edit、Write、MultiEdit 工具
- **stop**：匹配代理想要停止时（用于完成检查）
- **prompt**：匹配用户提交提示时
- **all**：匹配所有事件

## 模式编写提示

**Bash 模式：**
- 匹配危险命令：`rm\s+-rf|chmod\s+777|dd\s+if=`
- 匹配特定工具：`npm\s+install\s+|pip\s+install`

**文件模式：**
- 匹配代码模式：`console\.log\(|eval\(|innerHTML\s*=`
- 匹配文件路径：`\.env$|\.git/|node_modules/`

**停止模式：**
- 检查缺失的步骤：（检查对话记录或完成条件）

## 示例工作流程

**用户说**："/hookify 不要未经先询问就使用 rm -rf"

**您的响应**：
1. 分析：用户想要防止 rm -rf 命令
2. 询问："我是应该阻止此命令还是只是警告您？"
3. 用户选择："只是警告"
4. 创建 `.claude/hookify.dangerous-rm.local.md`：
   ```markdown
   ---
   name: warn-dangerous-rm
   enabled: true
   event: bash
   pattern: rm\s+-rf
   ---

   ⚠️ **检测到危险的 rm 命令**

   您请求在使用 rm -rf 之前收到警告。
   请验证路径是否正确。
   ```
5. 确认："已创建 hookify 规则。它立即生效 - 尝试触发它！"

## 重要说明

- **无需重启**：规则在下次工具使用时立即生效
- **文件位置**：在项目的 `.claude/` 目录（当前工作目录）中创建文件，而不是插件的 .claude/
- **正则表达式语法**：使用 Python 正则表达式语法（原始字符串，无需在 YAML 中转义）
- **操作类型**：规则可以 `warn`（默认）或 `block` 操作
- **测试**：创建规则后立即测试

## 故障排除

**如果规则文件创建失败：**
1. 使用 pwd 检查当前工作目录
2. 确保 `.claude/` 目录存在（如需要，使用 mkdir 创建）
3. 如需要，使用绝对路径：`{cwd}/.claude/hookify.{name}.local.md`
4. 使用 Glob 或 ls 验证文件已创建

**如果创建后规则未触发：**
1. 验证文件在项目 `.claude/` 而不是插件 `.claude/` 中
2. 使用 Read 工具检查文件以确保模式正确
3. 使用以下测试模式：`python3 -c "import re; print(re.search(r'pattern', 'test text'))"`
4. 验证前置数据中有 `enabled: true`
5. 记住：规则立即生效，无需重启

**如果阻止似乎太严格：**
1. 将规则文件中的 `action: block` 更改为 `action: warn`
2. 或者调整模式以更具体
3. 更改在下次工具使用时生效

使用 TodoWrite 跟踪您在步骤中的进度。
