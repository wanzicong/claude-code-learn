---
name: Plugin Structure
description: 当用户请求"创建插件"、"搭建插件"、"了解插件结构"、"组织插件组件"、"设置 plugin.json"、"使用 ${CLAUDE_PLUGIN_ROOT}"、"添加 commands/agents/skills/hooks"、"配置自动发现"或需要关于插件目录布局、清单配置、组件组织、文件命名约定或 Claude Code 插件架构最佳实践的指导时，应使用此技能。
version: 0.1.0
---

# Claude Code 插件结构

## 概述

Claude Code 插件遵循标准化的目录结构，具有自动组件发现。理解此结构可以创建组织良好、可维护的插件，与 Claude Code 无缝集成。

**核心概念**
- 用于自动发现的约定目录布局
- `.claude-plugin/plugin.json` 中的清单驱动配置
- 基于组件的组织（commands、agents、skills、hooks）
- 使用 `${CLAUDE_PLUGIN_ROOT}` 的可移植路径引用
- 显式与自动发现组件加载

## 目录结构

每个 Claude Code 插件都遵循此组织模式：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 必需：插件清单
├── commands/                 # 斜杠命令（.md 文件）
├── agents/                   # 子代理定义（.md 文件）
├── skills/                   # 代理技能（子目录）
│   └── skill-name/
│       └── SKILL.md         # 每个技能必需
├── hooks/
│   └── hooks.json           # 事件处理器配置
├── .mcp.json                # MCP 服务器定义
└── scripts/                 # 辅助脚本和实用工具
```

**关键规则：**

1. **清单位置**：`plugin.json` 清单必须在 `.claude-plugin/` 目录中
2. **组件位置**：所有组件目录（commands、agents、skills、hooks）必须在插件根级别，不能嵌套在 `.claude-plugin/` 内
3. **可选组件**：仅为插件实际使用的组件创建目录
4. **命名约定**：所有目录和文件名使用 kebab-case

## 插件清单（plugin.json）

清单定义插件元数据和配置。位于 `.claude-plugin/plugin.json`：

### 必需字段

```json
{
  "name": "plugin-name"
}
```

**名称要求：**
- 使用 kebab-case 格式（小写字母加连字符）
- 在已安装插件中必须唯一
- 无空格或特殊字符
- 示例：`code-review-assistant`、`test-runner`、`api-docs`

### 推荐的元数据

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件用途的简要说明",
  "author": {
    "name": "作者姓名",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation", "ci-cd"]
}
```

**版本格式**：遵循语义化版本（MAJOR.MINOR.PATCH）
**关键词**：用于插件发现和分类

### 组件路径配置

为组件指定自定义路径（补充默认目录）：

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**重要**：自定义路径补充默认路径——它们不替换默认路径。默认目录和自定义路径中的组件都会加载。

**路径规则：**
- 必须相对于插件根目录
- 必须以 `./` 开头
- 不能使用绝对路径
- 支持数组以指定多个位置

## 组件组织

### 命令

**位置**：`commands/` 目录
**格式**：具有 YAML frontmatter 的 Markdown 文件
**自动发现**：`commands/` 中的所有 `.md` 文件自动加载

**示例结构**：
```
commands/
├── review.md        # /review 命令
├── test.md          # /test 命令
└── deploy.md        # /deploy 命令
```

**文件格式**：
```markdown
---
name: command-name
description: 命令描述
---

命令实现说明...
```

**用途**：命令作为 Claude Code 中的原生斜杠命令集成

### 代理

**位置**：`agents/` 目录
**格式**：具有 YAML frontmatter 的 Markdown 文件
**自动发现**：`agents/` 中的所有 `.md` 文件自动加载

**示例结构**：
```
agents/
├── code-reviewer.md
├── test-generator.md
└── refactorer.md
```

**文件格式**：
```markdown
---
description: 代理角色和专业能力
capabilities:
  - 特定任务 1
  - 特定任务 2
---

详细的代理指令和知识...
```

**用途**：用户可以手动调用代理，或 Claude Code 根据任务上下文自动选择代理

### 技能

**位置**：`skills/` 目录，每个技能一个子目录
**格式**：每个技能在自己的目录中，包含 `SKILL.md` 文件
**自动发现**：技能子目录中的所有 `SKILL.md` 文件自动加载

**示例结构**：
```
skills/
├── api-testing/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── test-runner.py
│   └── references/
│       └── api-spec.md
└── database-migrations/
    ├── SKILL.md
    └── examples/
        └── migration-template.sql
```

**SKILL.md 格式**：
```markdown
---
name: 技能名称
description: 何时使用此技能
version: 1.0.0
---

技能指令和指导...
```

**支持文件**：技能可以在子目录中包含 scripts、references、examples 或资源

**用途**：Claude Code 根据任务上下文匹配描述自主激活技能

### Hooks

**位置**：`hooks/hooks.json` 或内联在 `plugin.json` 中
**格式**：定义事件处理器的 JSON 配置
**注册**：hooks 在插件启用时自动注册

**示例结构**：
```
hooks/
├── hooks.json           # Hook 配置
└── scripts/
    ├── validate.sh      # Hook 脚本
    └── check-style.sh   # Hook 脚本
```

**配置格式**：
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
      "timeout":ver 30
    }]
  }]
}
```

**可用事件**：PreToolUse、PostToolUse、Stop、SubagentStop、SessionStart、SessionEnd、UserPromptSubmit、PreCompact、Notification

**用途**：hooks 作为响应 Claude Code 事件自动执行

### MCP 服务器

**位置**：插件根目录的 `.mcp.json` 或内联在 `plugin.json` 中
**格式**：MCP 服务器定义的 JSON 配置
**自动启动**：服务器在插件启用时自动启动

**示例格式**：
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**用途**：MCP 服务器与 Claude Code 的工具系统无缝集成

## 可移植路径引用

### ${CLAUDE_PLUGIN_ROOT}

对所有插件内路径引用使用 `${CLAUDE_PLUGIN_ROOT}` 环境变量：

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**为什么重要**：插件根据以下因素安装在不同位置：
- 用户安装方式（marketplace、本地、npm）
- 操作系统约定
- 用户偏好

**在哪里使用它**：
- Hook 命令路径
- MCP 服务器命令参数
- 脚本执行引用
- 资源文件路径

**永远不要使用**：
- 硬编码的绝对路径（`/Users/name/plugins/...`）
- 从工作目录的相对路径（commands 中的 `./scripts/...`）
- 主目录快捷方式（`~/plugins/...`）

### 路径解析规则

**在清单 JSON 字段中**（hooks、MCP 服务器）：
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/tool.sh"
```

**在组件文件中**（commands、agents、skills）：
```markdown
引用脚本：${CLAUDE_PLUGIN_ROOT}/scripts/helper.py
```

**在执行的脚本中**：
```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} 作为环境变量可用
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

## 文件命名约定

### 组件文件

**命令**：使用 kebab-case `.md` 文件
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`
- `api-docs.md` → `/api-docs`

**代理**：使用描述角色的 kebab-case `.md` 文件
- `test-generator.md`
- `code-reviewer.md`
- `performance-analyzer.md`

**技能**：使用 kebab-case 目录名
- `api-testing/`
- `database-migrations/`
- `error-handling/`

### 支持文件

**脚本**：使用描述性 kebab-case 名称和适当的扩展名
- `validate-input.sh`
- `generate-report.py`
- `process-data.js`

**文档**：使用 kebab-case markdown 文件
- `api-reference.md`
- `migration-guide.md`
- `best-practices.md`

**配置**：使用标准名称
- `hooks.json`
- `.mcp.json`
- `plugin.json`

## 自动发现机制

Claude Code 自动发现和加载组件：

1. **插件清单**：插件启用时读取 `.claude-plugin/plugin.json`
2. **命令**：扫描 `commands/` 目录以查找 `.md` 文件
3. **代理**：扫描 `agents/` 目录以查找 `.md` 文件
4. **技能**：扫描 `skills/` 以查找包含 `SKILL.md` 的子目录
5. **Hooks**：从 `hooks/hooks.json` 或清单加载配置
6. **MCP 服务器**：从 `.mcp.json` 或清单加载配置

**发现时机**：
- 插件安装：组件向 Claude Code 注册
- 插件启用：组件变为可用
- 无需重启：更改在下一个 Claude Code 会话时生效

**覆盖行为**：`plugin.json` 中的自定义路径补充（不替换）默认目录

## 最佳实践

### 组织

1. **逻辑分组**：将相关组件组合在一起
   - 将测试相关的命令、代理和技能放在一起
   - 在 `scripts/` 中为不同目的创建子目录

2. **最小化清单**：保持 `plugin.json` 精简
   - 仅在必要时指定自定义路径
   - 依赖自动发现以实现标准布局
   - 仅在简单情况下使用内联配置

3. **文档**：包含 README 文件
   - 插件根目录：总体用途和使用
   - 组件目录：特定指导
   - 脚本目录：使用和需求

### 命名

1. **一致性**：在组件之间使用一致的命名
   - 如果命令是 `test-runner`，将相关代理命名为 `test-runner-agent`
   - 匹配技能目录名称与其用途

2. **清晰度**：使用指示用途的描述性名称
   - 好：`api-integration-testing/`、`code-quality-checker.md`
   - 避免：`utils/`、`misc.md`、`temp.sh`

3. **长度**：平衡简洁性与清晰度
   - 命令：2-3 个词（`review-pr`、``run-ci`）
   - 代理：清晰描述角色（`code-reviewer`、`test-generator`）
   - 技能：专注于主题（`error-handling`、`api-design`）

### 可移植性

1. **始终使用 ${CLAUDE_PLUGIN_ROOT}**：永不安编码路径
2. **在多个系统上测试**：在 macOS、Linux、Windows 上验证
3. **记录依赖关系**：列出所需工具和版本
4. **避免系统特定功能**：使用可移植的 bash/Python 构造

### 维护

1. **一致版本控制**：在插件发布时更新版本
2. **优雅弃用**：在删除之前清楚地标记旧组件
3. **记录破坏性更改**：记录影响现有用户的更改
4. **彻底测试**：验证更改后所有组件工作

## 常见模式

### 最小化插件

单个命令，无依赖：
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json    # 仅名称字段
└── commands/
    └── hello.md       # 单个命令
```

### 全功能插件

包含所有组件类型的完整插件：
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/          # 用户面向的命令
├── agents/            # 专门的子代理
├── skills/            # 自动激活的技能
├── hooks/             # 事件处理器
│   ├── hooks.json
│   └── scripts/
├── .mcp.json          # 外部集成
└── scripts/           # 共享实用工具
```

### 技能专注的插件

仅提供技能的插件：
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

## 故障排除

**组件未加载**：
- 验证文件在具有正确扩展名的正确目录中
- 检查 YAML frontmatter 语法（commands、agents、skills）
- 确保技能有 `SKILL.md`（而不是 `README.md` 或其他名称）
- 确认插件在 Claude Code 设置中已启用

**路径解析错误**：
- 用 `${CLAUDE_PLUGIN_ROOT}` 替换所有硬编码路径
- 验证路径是相对的并在清单中以 `./` 开头
- 检查引用的文件在指定路径处存在
- 用 `echo $CLAUDE_PLUGIN_ROOT` 在 hook 脚本中测试

**自动发现不工作**：
- 确认目录在插件根目录（不在 `.claude-plugin/` 中）
- 检查文件命名遵循约定（kebab-case、正确扩展名）
- 验证清单中的自定义路径正确
- 重启 Claude Code 以重新加载插件配置

**插件之间的冲突**：
- 使用唯一的、描述性组件名称
- 如有必要，使用插件名称命名空间命令
- 在插件 README 中记录潜在冲突
- 为相关功能考虑命令前缀

---

对于详细示例和高级模式，请参阅 `references/` 和 `examples/` 目录中的文件。
