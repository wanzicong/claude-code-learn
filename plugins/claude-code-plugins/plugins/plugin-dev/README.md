# 插件开发工具包

一个用于开发 Claude Code 插件的综合工具包，提供有关钩子、MCP 集成、插件结构和市场发布的专家指导。

## 概述

plugin-dev 工具包提供七个专门技能，帮助您构建高质量的 Claude Code 插件：

1. **钩子开发** - 高级钩子 API 和事件驱动的自动化
2. **MCP 集成** - Model Context Protocol 服务器集成
3. **插件结构** - 插件组织和清单配置
4. **插件设置** - 使用 .claude/plugin-name.local.md 文件的配置模式
5. **命令开发** - 使用 frontmatter 和参数创建斜杠命令
6. **代理开发** - 使用 AI 辅助创建自主代理
7. **技能开发** - 创建具有渐进式披露和强触发器的技能

每个技能都遵循最佳实践和渐进式披露原则：精简的核心文档、详细的参考资料、工作示例和实用脚本。

## 引导式工作流命令

### /plugin-dev:create-plugin

一个全面的、端到端的工作流命令，用于从零开始创建插件，类似于 feature-dev 工作流。

**8 阶段流程：**
1. **发现** - 了解插件目的和需求
2. **组件规划** - 确定所需的技能、命令、代理、钩子、MCP
3. **详细设计** - 指定每个组件并解决歧义
4. **结构创建** - 设置目录和清单
5. **组件实现** - 使用 AI 辅助代理创建每个组件
6. **验证** - 运行 plugin-validator 和特定组件检查
7. **测试** - 验证插件在 Claude Code 中工作
8. **文档** - 完成 README 并准备分发

**功能：**
- 在每个阶段提出澄清问题
- 自动加载相关技能
- 使用 agent-creator 进行 AI 辅助代理生成
- 运行验证实用程序（validate-agent.sh、validate-hook-schema.sh 等）
- 遵循 plugin-dev 自身的经过验证的模式
- 指导测试和进行验证

**用法：**
```bash
/plugin-dev:create-plugin [可选描述]

# 示例：
/plugin-dev:create-plugin
/plugin-dev:create-plugin 用于管理数据库迁移的插件
```

使用此工作流进行结构化、高质量的插件开发，从概念到完成。

## 技能

### 1. 钩子开发

**触发短语：** "create a hook"、"add a PreToolUse hook"、"validate tool use"、"implement prompt-based hooks"、"${CLAUDE_PLUGIN_ROOT}"、"block dangerous commands"

**涵盖内容：**
- 基于提示的钩子（推荐），具有 LLM 决策能力
- 用于确定性验证的命令钩子
- 所有钩子事件：PreToolUse、PostToolUse、Stop、SubagentStop、SessionStart、SessionEnd、UserPromptSubmit、PreCompact、Notification
- 钩子输出格式和 JSON 模式
- 安全最佳实践和输入验证
- 用于可移植路径的 ${CLAUDE_PLUGIN_ROOT}

**资源：**
- 核心 SKILL.md（1,619 字）
- 3 个示例钩子脚本（validate-write、validate-bash、load-context）
- 3 个参考文档：模式、迁移、高级技术
- 3 个实用脚本：validate-hook-schema.sh、test-hook.sh、hook-linter.sh

**何时使用：** 在插件中创建事件驱动的自动化、验证操作或实施策略时。

### 2. MCP 集成

**触发短语：** "add MCP server"、"integrate MCP"、"configure .mcp.json"、"Model Context Protocol"、"stdio/SSE/HTTP server"、"connect external service"

**涵盖内容：**
- MCP 服务器配置（.mcp.json vs plugin.json）
- 所有服务器类型：stdio（本地）、SSE（托管/OAuth）、HTTP（REST）、WebSocket（实时）
- 环境变量扩展（${CLAUDE_PLUGIN_ROOT}、用户变量）
- 命令/代理中的 MCP 工具命名和用法
- 身份验证模式：OAuth、令牌、环境变量
- 集成模式和性能优化

**资源：**
- 核心 SKILL.md（1,666 字）
- 3 个示例配置（stdio、SSE、HTTP）
- 3 个参考文档：server-types（~3,200字）、authentication（~2,800字）、tool-usage（~2,600字）

**何时使用：** 将外部服务、API、数据库或工具集成到插件中时。

### 3. 插件结构

**触发短语：** "plugin structure"、"plugin.json manifest"、"auto-discovery"、"component organization"、"plugin directory layout"

**涵盖内容：**
- 标准插件目录结构和自动发现
- plugin.json 清单格式和所有字段
- 组件组织（commands、agents、skills、hooks）
- 全程使用 ${CLAUDE_PLUGIN_ROOT}
- 文件命名约定和最佳实践
- 最小化、标准和高级插件模式

**资源：**
- 核心 SKILL.md（1,619 字）
- 3 个示例结构（最小化、标准、高级）
- 2 个参考文档：component-patterns、manifest-reference

**何时使用：** 启动新插件、组织组件或配置插件清单时。

### 4. 插件设置

**触发短语：** "plugin settings"、"store plugin configuration"、".local.md files"、"plugin state files"、"read YAML frontmatter"、"per-project plugin settings"

**涵盖内容：**
- 用于配置的 .claude/plugin-name.local.md 模式
- YAML frontmatter + markdown body 结构
- bash 脚本的解析技术（sed、awk、grep 模式）
- 临时活动的钩子（标志文件和快速退出）
- 来自 multi-agent-swarm 和 ralph-wiggum 插件的真实示例
- 原子文件更新和验证
- Gitignore 和生命周期管理

**资源：**
- 核心 SKILL.md（1,623 字）
- 3 个示例（read-settings hook、create-settings command、templates）
- 2 个参考文档：parsing-techniques、real-world-examples
- 2 个实用脚本：validate-settings.sh、parse-frontmatter.sh

**何时使用：** 使插件可配置、存储每个项目的状态或实施用户偏好时。

### 5. 命令开发

**触发短语：** "create a slash command"、"add a command"、"command frontmatter"、"define command arguments"、"organize commands"

**涵盖内容：**
- 斜杠命令结构和 markdown 格式
- YAML frontmatter 字段（description、argument-hint、allowed-tools）
- 动态参数和文件引用
- 用于上下文的 Bash 执行
- 命令组织和命名空间
- 命令开发最佳实践

**资源：**
- 核心 SKILL.md（1,535 字）
- 示例和参考文档
- 命令组织模式

**何时使用：** 创建斜杠命令、定义命令参数或组织插件命令时。

### 6. 代理开发

**触发短语：** "create an agent"、"add an agent"、"write a subagent"、"agent frontmatter"、"when to use description"、"agent examples"、"autonomous agent"

**涵盖内容：**
- 代理文件结构（YAML frontmatter + system prompt）
- 所有 frontmatter 字段（name、description、model、color、tools）
- 描述格式，带有用于可靠触发的 <example> 块
- 系统提示设计模式（分析、生成、验证、编排）
- 使用 Claude Code 经过验证的提示进行 AI 辅助代理生成
- 验证规则和最佳实践
- 完整的生产就绪代理示例

**资源：**
- 核心 SKILL.md（1,438 字）
- 2 个示例：agent-creation-prompt（AI 辅助工作流）、complete-agent-examples（4 个完整代理）
- 3 个参考文档：agent-creation-system-prompt（来自 Claude Code）、system-prompt-design（~4,000字）、triggering-examples（~2,500字）
- 1 个实用脚本：validate-agent.sh

**何时使用：** 创建自主代理、定义代理行为或实施 AI 辅助代理生成时。

### 7. 技能开发

**触发短语：** "create a skill"、"add a skill to plugin"、"write a new skill"、"improve skill description"、"organize skill content"

**涵盖内容：**
- 技能结构（带有 YAML frontmatter 的 SKILL.md）
- 渐进式披露原则（metadata → SKILL.md → resources）
- 具有特定短语的有力触发器描述
- 写作风格（命令式/不定式形式、第三人称）
- 捆绑的资源组织（references/、examples/、scripts/）
- 技能创建工作流
- 基于 skill-creator 方法论，为 Claude Code 插件进行了调整

**资源：**
- 核心 SKILL.md（1,232 字）
- 参考资料：skill-creator 方法论、plugin-dev 模式
- 示例：将 plugin-dev 自身的技能作为模板进行研究

**何时使用：** 为插件创建新技能或提高现有技能质量时。

## 安装

从 claude-code-marketplace 安装：

```bash
/plugin install plugin-dev@claude-code-marketplace
```

或用于开发，直接使用：

```bash
cc --plugin-dir /path/to/plugin-dev
```

## 快速入门

### 创建您的第一个插件

1. **规划您的插件结构：**
   - 询问："What's best directory structure for a plugin with commands and MCP integration?"
   - plugin-structure 技能将指导您

2. **添加 MCP 集成（如果需要）：**
   - 询问："How do I add an MCP server for database access?"
   - mcp-integration 技能提供示例和模式

3. **实施钩子（如果需要）：**
   - 询问："Create a PreToolUse hook that validates file writes"
   - hook-development 技能提供工作示例和实用程序

## 开发工作流

plugin-dev 工具包支持您的整个插件开发生命周期：

```
┌─────────────────────┐
│  Design Structure   │  → plugin-structure skill
│  (manifest, layout) │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Add Components     │
│  (commands, agents, │  → All skills provide guidance
│   skills, hooks)    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Integrate Services │  → mcp-integration skill
│  (MCP servers)      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Add Automation     │  → hook-development skill
│  (hooks, validation)│     + utility scripts
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Test & Validate    │  → hook-development utilities
│                     │     validate-hook-schema.sh
└──────────┬──────────┘     test-hook.sh
           │                 hook-linter.sh
```

## 功能

### 渐进式披露

每个技能使用三级披露系统：
1. **Metadata**（始终加载）：具有强触发器的简明描述
2. **Core SKILL.md**（触发时加载）：基本 API 参考（~1,500-2,000 字）
3. **References/Examples**（按需加载）：详细指南、模式和工作代码

这使 Claude Code 的上下文保持专注，同时在需要时提供深入知识。

### 实用脚本

hook-development 技能包括生产就绪的实用程序：

```bash
# 验证 hooks.json 结构
./validate-hook-schema.sh hooks/hooks.json

# 部署前测试钩子
./test-hook.sh my-hook.sh test-input.json

# 对钩子脚本进行 lint 检查以遵循最佳实践
./hook-linter.sh my-hook.sh
```

### 工作示例

每个技能都提供工作示例：
- **钩子开发**：3 个完整的钩子脚本（bash、write 验证、context 加载）
- **MCP 集成**：3 个服务器配置（stdio、SSE、HTTP）
- **插件结构**：3 个插件布局（最小化、标准、高级）
- **插件设置**：3 个示例（read-settings hook、create-settings command、templates）
- **命令开发**：10 个完整的命令示例（review、test、deploy、docs 等）

## 文档标准

所有技能都遵循一致的标准：
- 第三人称描述（"This skill should be used when..."）
- 用于可靠加载的强触发器短语
- 全程使用命令式/不定式形式
- 基于官方 Claude Code 文档
- 安全优先的方法和最佳实践

## 总内容

- **核心技能**：7 个 SKILL.md 文件共约 11,065 字
- **参考文档**：约 10,000+ 字的详细指南
- **示例**：12+ 个工作示例（钩子脚本、MCP 配置、插件布局、设置文件）
- **实用程序**：6 个生产就绪的验证/测试/解析脚本

## 用例

### 构建数据库插件

```
1. "What's structure for a plugin with MCP integration?"
   → plugin-structure 技能提供布局

2. "How do I configure an stdio MCP server for PostgreSQL?"
   → mcp-integration 技能显示配置

3. "Add a Stop hook to ensure connections close properly"
   → hook-development 技能提供模式

```

### 创建验证插件

```
1. "Create hooks that validate all file writes for security"
   → hook-development 技能及示例

2. "Test my hooks before deploying"
   → 使用 validate-hook-schema.sh 和 test-hook.sh

3. "Organize my hooks and configuration files"
   → plugin-structure 技能显示最佳实践

```

### 集成外部服务

```
1. "Add Asana MCP server with OAuth"
   → mcp-integration 技能涵盖 SSE 服务器

2. "Use Asana tools in my commands"
   → mcp-integration tool-usage 参考

3. "Structure my plugin with commands and MCP"
   → plugin-structure 技能提供模式

```

## 最佳实践

所有技能都强调：

✅ **安全优先**
- 钩子中的输入验证
- MCP 服务器使用 HTTPS/WSS
- 用于凭证的环境变量
- 最小权限原则

✅ **可移植性**
- 全程使用 ${CLAUDE_PLUGIN_ROOT}
- 仅使用相对路径
- 环境变量替换

✅ **测试**
- 部署前验证配置
- 使用示例输入测试钩子
- 使用调试模式（`claude --debug`）

✅ **文档**
- 清晰的 README 文件
- 记录的环境变量
- 使用示例

## 贡献

此插件是 claude-code-marketplace 的一部分。要贡献改进：

1. Fork 市场 repository
2. 对 plugin-dev/ 进行更改
3. 使用 `cc --plugin-dir` 本地测试
4. 按照市场发布指南创建 PR

## 版本

0.1.0 - 初始版本，包含七个综合技能和三个验证代理

## 作者

Daisy Hollman (daisy@anthropic.com)

## 许可证

MIT 许可证 - 详见 repository

---

**注意：** 此工具包旨在帮助您构建高质量的插件。当您询问相关问题、在您需要时提供专家指导时，技能会自动加载。
