---
name: Skill Development
description: 当用户想要"创建技能"、"向插件添加技能"、"编写新技能"、"改进技能描述"、"组织技能内容"或需要有关技能结构、渐进式披露或 Claude Code 插件技能开发最佳实践指导时，应使用此技能。
version: 0.1.0
---

# Claude Code 插件的技能开发

此技能为创建有效的 Claude Code 插件技能提供指导。

## 关于此技能

技能是模块化、自包含的包，通过提供专门知识、工作流和工具来扩展 Claude 的能力。将它们视为特定领域或任务的"入职指南"——它们将 Claude 从通用代理转变为装备了任何模型都无法完全具备的过程知识的专门代理。

### 技能提供的内容

1. 专门工作流 - 特定领域的多步骤过程
2. 工具集成 - 使用特定文件格式或 API 的说明
3. 领域专业知识 - 公司特定知识、架构、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考和资产

### 技能的组成部分

每个技能由必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter 元数据 (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown 指令 (required)
└── 捆绑资源 (optional)
    ├── scripts/          - 可执行代码 (Python/Bash/等)
    ├── references/       - 打算需要时加载到上下文的文档
    └── assets/           - Claude 在输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md (required)

**元数据质量：** YAML frontmatter 中的 `name` 和 `description` 决定 Claude 何时使用技能。具体说明技能做什么以及何时使用它。使用第三人称（例如"This skill should be used when..."而非"Use this skill when..."）。

#### 捆绑资源 (optional)

##### 脚本 (`scripts/`)

需要确定性可靠性或被重复重写的任务的可执行代码（Python/Bash/等）。

- **何时包括：** 相同代码被重复重写或需要确定性可靠性时
- **示例：** 用于 PDF 旋转任务的 `scripts/rotate_pdf.py`
- **好处：** 令牌高效、确定性，可以加载到上下文中执行
- **注意：** 脚本可能仍需要由 Claude 读取，以便进行补丁或环境特定调整

##### 参考 (`references/`)

旨在按需加载到上下文中以通知 Claude 过程和思考的文档和参考材料。

- **何时包括：** Claude 在工作时应该参考的文档
- **示例：** `references/finance.md` 用于财务架构、`references/nda.md` 用于公司 NDA 模板、`references/policies.md` 用于公司策略、`references/api_docs.md` 用于 API 规范
- **用例：** 数据库架构、API 文档、领域知识、公司策略、详细的工作流指南
- **好处：** 保持 SKILL.md 精简，仅在 Claude 确定需要时加载
- **最佳实践：** 如果文件较大（>10k 字），请在 SKILL.md 中包含 grep 搜索模式
- **避免重复：** 信息应该存在于 SKILL.md 或参考文件中，而非两者。除非对技能真正核心，否则更倾向于参考文件中的详细信息——这使 SKILL.md 保持精简，同时使信息可发现而不占用上下文窗口。仅在 SKILL.md 中保留基本的过程指令和工作流指导；将详细参考材料、架构和示例移至参考文件。

##### 资产 (`assets/`)

不打算加载到上下文中，而是在 Claude 产生的输出中使用的文件。

- **何时包括：** 当技能需要将在最终输出中使用的文件时
- **示例：** `assets/logo.png` 用于品牌资产、`assets/slides.pptx` 用于 PowerPoint 模板、`assets/frontend-template/` 用于 HTML/React 样板、`assets/font.ttf` 用于排版
- **用例：** 模板、图像、图标、样板代码、字体、被复制或修改的示例文档
- **好处：** 将输出资源与文档分离，使 Claude 能够在不加载它们到上下文的情况下使用文件

### 渐进式披露设计原则

技能使用三级加载系统来高效管理上下文：

1. **元数据 (name + description)** - 始终在上下文中 (~100 字)
2. **SKILL.md body** - 当技能触发时 (<5k 字)
3. **捆绑资源** - 按 Claude 需要（无限制*）

*无限制，因为脚本可以在不读取到上下文窗口的情况下执行

## 技能创建流程

要创建技能，按顺序遵循"技能创建流程"，仅在有不适用它们的明确原因时才跳过步骤。

### 步骤 1：通过具体示例理解技能

仅在技能的使用模式已经清楚理解时才跳过此步骤。即使是使用现有技能，它仍然有价值。

要创建有效的技能，清楚地了解技能将如何使用的具体示例。这种理解可以来自直接用户示例或经过用户反馈验证的生成示例。

例如，在构建 image-editor 技能时，相关问题包括：

- "image-editor 技能应该支持什么功能？编辑、旋转，还是其他？"
- "你能给我一些此技能将如何使用的示例吗？"
- "我可以想象用户会要求诸如'从此图像中移除红眼'或'旋转此图像'之类的内容。你能想象出此技能被使用的其他方式吗？"
- "用户应该说什么来触发此技能？"

为避免让用户不知所措，避免在单个消息中询问太多问题。从最重要的问题开始，根据需要跟进以提高效果。

当清楚了解技能应该支持的功能时，完成此步骤。

### 步骤 2：规划可复用的技能内容

要将具体示例转化为有效的技能，通过以下方式分析每个示例：

1. 考虑如何从头开始执行每个示例
2. 确定什么脚本、参考和资产在重复执行这些工作流时会很有帮助

示例：在构建 `pdf-editor` 技能以处理诸如"Help me rotate this PDF"之类的查询时，分析显示：

1. 旋转 PDF 需要每次重写相同的代码
2. `scripts/rotate_pdf.py` 脚本将有助于存储在技能中

示例：在设计 `frontend-webapp-builder` 技能以处理诸如"Build me a todo app"或"Build me a dashboard to track my steps"之类的查询时，分析显示：

1. 编写前端 webapp 需要每次相同的样板 HTML/React
2. 包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板将有助于存储在技能中

示例：在构建 `bigquery` 技能以处理诸如"How many users have logged in today?"之类的查询时，分析显示：

1. 查询 BigQuery 需要每次重新发现表架构和关系
2. 记录表架构的 `references/schema.md` 文件将有助于存储在技能中

**对于 Claude Code 插件：** 在构建 hooks 技能时，分析显示：
1. 开发人员需要重复验证 hooks.json 并测试钩子脚本
2. `scripts/validate-hook-schema.sh` 和 `scripts/test-hook.sh` 实用程序将很有帮助
3. `references/patterns.md` 用于详细的钩子模式以避免膨胀 SKILL.md

要建立技能的内容，分析每个具体示例以创建要包括的可复用资源列表：脚本、参考和资产。

### 步骤 3：创建技能结构

对于 Claude Code 插件，创建技能目录结构：

```bash
mkdir -p plugin-name/skills/skill-name/{references,examples,scripts}
touch plugin-name/skills/skill-name/SKILL.md
```

**注意：** 与使用 `init_skill.py` 的通用 skill-creator 不同，插件技能是直接在插件的 `skills/` 目录中使用更简单的手动结构创建。

### 步骤 4：编辑技能

在编辑（新创建或现有）技能时，请记住技能是为另一个 Claude 实例使用而创建。专注于包括对 Claude 有益且非显而易见的信息。考虑什么过程知识、特定于领域的细节或可复用资产将帮助另一个 Claude 实例更有效地执行这些任务。

#### 从可复用的技能内容开始

要开始实现，从上面确定的可复用资源开始：`scripts/`、`references/` 和 `assets/` 文件。请注意，此步骤可能需要用户输入。例如，在实现 `brand-guidelines` 技能时，用户可能需要提供要存储在 `assets/` 中的品牌资产或模板，或要存储在 `references/` 中的文档。

此外，删除技能不需要的任何示例文件和目录。仅创建您实际需要的目录（references/、examples/、scripts/）。

#### 更新 SKILL.md

**写作风格：** 使用**命令式/不定式形式**（动词优先指令）编写整个技能，而非第二人称。使用客观、指导性语言（例如"To accomplish X, do Y"而非"You should do X"或"If you need to do X"）。这为 AI 消费维持了一致性和清晰度。

**描述（Frontmatter）：** 使用带有特定触发器短语的第三人称格式：

```yaml
---
name: Skill Name
description: This skill should be used when user asks to "specific phrase 1", "specific phrase 2", "specific phrase 3". Include exact phrases users would say that should trigger this skill. Be concrete and specific.
version: 0.1.0
---
```

**好的描述示例：**
```yaml
description: This skill should be used when user asks to "create a hook", "add a PreToolUse hook", "validate tool use", "implement prompt-based hooks", or mentions hook events (PreToolUse, PostToolUse, Stop).
```

**坏的描述示例：**
```yaml
description: Use this skill when working with hooks.  # 错误的人称，模糊
description: Load when user needs hook help.  # 非第三人称
description: Provides hook guidance.  # 无触发器短语
```

要完成 SKILL.md 正文，回答以下问题：

1. 技能的目的是什么，用几句话？
2. 何时应该使用技能？（在 frontmatter description 中包含特定触发器）
3. 在实践中，Claude 应该如何使用技能？上面开发的所有可复用技能内容都应被引用，以便 Claude 知道如何使用它们。

**保持 SKILL.md 精简：** 正文的目标字数为 1,500-2,000。将详细内容移至 references/：
- 详细模式 → `references/patterns.md`
- 高级技术 → `references/advanced.md`
- 迁移指南 → `references/migration.md`
- API 参考 → `references/api-reference.md`

**在 SKILL.md 中引用资源：**
```markdown
## 其他资源

### 参考文件

对于详细模式和技术，请参考：
- **`references/patterns.md`** - 常见模式
- **`references/advanced.md`** - 高级用例

### 示例文件

`examples/` 中的工作示例：
- **`example-script.sh`** - 工作示例
```

### 步骤 5：验证和测试

**对于插件技能，验证与通用技能不同：**

1. **检查结构**：`plugin-name/skills/skill-name/` 中的技能目录
2. **验证 SKILL.md**：具有 name 和 description 的 frontmatter
3. **检查触发器短语**：描述包括特定用户查询
4. **验证写作风格**：正文使用命令式/不定式形式，而非第二人称
5. **测试渐进式披露**：SKILL.md 是精简的 (~1,500-2,000 字)，详细内容在 references/ 中
6. **检查参考**：所有引用的文件都存在
7. **验证示例**：示例是完整且正确的
8. **测试脚本**：脚本可执行且工作正常

**使用 skill-reviewer 代理：**
```
Ask: "Review my skill and check if it follows best practices"
```

skill-reviewer 代理将检查描述质量、内容组织和渐进式披露。

### 步骤 6：迭代

测试技能后，用户可能请求改进。通常这就在使用技能后立即发生，具有技能执行方式的上下文。

**迭代工作流：**
1. 在真实任务上使用技能
2. 注意困难或低效
3. 识别 SKILL.md 或捆绑资源应该如何更新
4. 实现更改并再次测试

**常见改进：**
- 增强描述中的触发器短语
- 将长章节从 SKILL.md 移至 references/
- 添加缺失的示例或脚本
- 澄清模糊的指令
- 添加边缘情况处理

## 插件特定考虑

### 插件中的技能位置

插件技能位于插件的 `skills/` 目录中：

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
└── skills/
    └── my-skill/
        ├── SKILL.md
        ├── references/
        ├── examples/
        └── scripts/
```

### 自动发现

Claude Code 自动发现技能：
- 扫描 `skills/` 目录
- 查找包含 `SKILL.md` 的子目录
- 始终加载技能元数据 (name + description)
- 技能触发时加载 SKILL.md 正文
- 按需加载 references/examples

### 无需打包

插件技能作为插件的一部分分发，而非作为单独的 ZIP 文件。用户在安装插件时获得技能。

### 在插件中测试

通过本地安装插件来测试技能：

```bash
# 使用 --plugin-dir 测试
cc --plugin-dir /path/to/plugin

# 询问应该触发技能的问题
# 验证技能正确加载
```

## 来自 Plugin-Dev 的示例

研究此插件中的技能作为最佳实践的示例：

**hook-development skill:**
- 优秀的触发器短语："create a hook"、"add a PreToolUse hook"等。
- 精简的 SKILL.md (1,651 字)
- 3 个 references/ 文件用于详细内容
- 3 个 examples/ 的工作钩子
- 3 个 scripts/ 实用程序

**agent-development skill:**
- 强烈的触发器："create an agent"、"agent frontmatter"等。
- 专注的 SKILL.md (1,438 字)
- 参考包括来自 Claude Code 的 AI 生成提示
- 完整的代理示例

**plugin-settings skill:**
- 特定的触发器："plugin settings"、".local.md files"、"YAML frontmatter"
- 参考显示真实实现（multi-agent-swarm、ralph-wiggum）
- 工作的解析脚本

每个都展示了渐进式披露和强触发。

## 实践中的渐进式披露

### SKILL.md 中包含什么

**始终在技能触发时包含（始终加载）：**
- 核心概念和概述
- 基本过程和工作流
- 快速参考表
- 指向 references/examples/scripts
- 最常见的用例

**保持在 3,000 字以下，理想为 1,500-2,000 字**

### references/ 中包含什么

**移至 references/（按需加载）：**
- 详细模式和高级技术
- 全面的 API 文档
- 迁移指南
- 边缘情况和故障排除
- 详尽的示例和演练

**每个参考文件可以很大（2,000-5,000+ 字）**

### examples/ 中包含什么

**工作代码示例：**
- 完整、可运行的脚本
- 配置文件
- 模板文件
- 真实世界的用例

**用户可以直接复制和改编这些**

### scripts/ 中包含什么

**实用程序脚本：**
- 验证工具
- 测试帮助程序
- 解析实用程序
- 自动化脚本

**应该可执行且有文档**

## 写作风格要求

### 命令式/不定式形式

使用动词优先指令编写，而非第二人称：

**正确（命令式）：**
```
要创建钩子，定义事件类型。
使用身份验证配置 MCP 服务器。
在使用前验证设置。
```

**不正确（第二人称）：**
```
You should create a hook by defining the event type.
You need to configure the MCP server.
You must validate settings before use.
```

### 描述中的第三人称

frontmatter 描述必须使用第三人称：

**正确：**
```yaml
description: This skill should be used when user asks to "create X", "configure Y"...
```

**不正确：**
```yaml
description: Use this skill when you want to create X...
description: Load this skill when user asks...
```

### 客观、指导性语言

专注于做什么，而非谁应该做它：

**正确：**
```
使用 sed 解析 frontmatter。
使用 grep 提取字段。
在使用前验证值。
```

**不正确：**
```
You can parse the frontmatter...
Claude should extract fields...
The user might validate values...
```

## 验证检查清单

在完成技能之前：

**结构：**
- [ ] SKILL.md 文件存在，具有有效的 YAML frontmatter
- [ ] Frontmatter 具有 `name` 和 `description` 字段
- [ ] Markdown 正文存在且实质
- [ ] 引用的文件实际存在

**描述质量：**
- [ ] 使用第三人称 ("This skill should be used when...")
- [ ] 包括用户会说的特定触发器短语
- [ ] 列出具体场景 ("create X"、"configure Y"）
- [ ] 不模糊或通用

**内容质量：**
- [ ] SKILL.md 正文使用命令式/不定式形式
- [ ] 正文专注且精简（理想为 1,500-2,000 字，最多 <5k）
- [ ] 详细内容移至 references/
- [ ] 示例完整且工作
- [ ] 脚本可执行且有文档

**渐进式披露：**
- [ ] SKILL.md 中的核心概念
- [ ] references/ 中的详细文档
- [ ] examples/ 中的工作代码
- [ ] scripts/ 中的实用程序
- [ ] SKILL.md 引用这些资源

**测试：**
- [ ] 技能在预期的用户查询上触发
- [ ] 内容对于预期任务有帮助
- [ ] 文件之间没有重复信息
- [ ] 按需加载引用

## 需要避免的常见错误

### 错误 1：弱触发器描述

❌ **坏的：**
```yaml
description: Provides guidance for working with hooks.
```

**为什么坏：** 模糊，没有特定触发器短语，非第三人称

✅ **好的：**
```yaml
description: This skill should be used when user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events. Provides comprehensive hooks API guidance.
```

**为什么好：** 第三人称，特定短语，具体场景

### 错误 2：SKILL.md 中内容太多

❌ **坏的：**
```
skill-name/
└── SKILL.md  (8,000 字 - 所有内容在一个文件中)
```

**为什么坏：** 技能加载时膨胀上下文，详细内容始终加载

✅ **好的：**
```
skill-name/
├── SKILL.md  (1,800 字 - 核心必需项)
└── references/
    ├── patterns.md (2,500 字)
    └── advanced.md (3,700 字)
```

**为什么好：** 渐进式披露，仅在需要时加载详细内容

### 错误 3：第二人称写作

❌ **坏的：**
```markdown
You should start by reading the configuration file.
You need to validate the input.
You can use grep tool to search.
```

**为什么坏：** 第二人称，非命令式形式

✅ **好的：**
```markdown
Start by reading the configuration file.
Validate input before processing.
Use grep tool to search for patterns.
```

**为什么好：** 命令式形式，直接指令

### 错误 4：缺少资源引用

❌ **坏的：**
```markdown
# SKILL.md

[核心内容]

[没有提及 references/ 或 examples/]
```

**为什么坏：** Claude 不知道引用存在

✅ **好的：**
```markdown
# SKILL.md

[核心内容]

## 其他资源

### 参考文件
- **`references/patterns.md`** - 详细模式
- **`references/advanced.md`** - 高级技术

### 示例
- **`examples/script.sh`** - 工作示例
```

**为什么好：** Claude 知道在哪里找到额外信息

## 快速参考

### 最小技能

```
skill-name/
└── SKILL.md
```

适用于：简单知识，不需要复杂资源

### 标准技能（推荐）

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

适用于：大多数插件技能，具有详细文档

### 完整技能

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

适用于：具有验证实用程序的复杂领域

## 最佳实践摘要

✅ **做：**
- 在描述中使用第三人称 ("This skill should be used when...")
- 包括特定触发器短语 ("create X"、"configure Y"）
- 保持 SKILL.md 精简（1,500-2,000 字）
- 使用渐进式披露（将详细信息移至 references/）
- 使用命令式/不定式形式编写
- 清楚地引用支持文件
- 提供工作示例
- 为常见操作创建实用程序脚本
- 以 plugin-dev 的技能为模板进行研究

❌ **不要：**
- 在任何地方使用第二人称
- 有模糊的触发条件
- 将所有内容放在 SKILL.md 中 (>3,000 字而没有 references/)
- 用第二人称编写 ("You should..."）
- 让资源未被引用
- 包含损坏或不完整的示例
- 跳过验证

## 其他资源

### 研究这些技能

Plugin-dev 的技能展示了最佳实践：
- `../hook-development/` - 渐进式披露、实用程序
- `../agent-development/` - AI 辅助创建、参考
- `../mcp-integration/` - 全面的参考
- `../plugin-settings/` - 真实世界的示例
- `../command-development/` - 清晰的核心概念
- `../plugin-structure/` - 良好的组织

### 参考文件

对于完整的 skill-creator 方法论：
- **`references/skill-creator-original.md`** - 完整的原始 skill-creator 内容

## 实现工作流

要为插件创建技能：

1. **了解用例**：识别技能使用的具体示例
2. **规划资源**：确定需要什么脚本/参考/示例
3. **创建结构**：`mkdir -p skills/skill-name/{references,examples,scripts}`
4. **编写 SKILL.md**：
   - 具有第三人称描述和触发器短语的 frontmatter
   - 命令式形式的精简正文（1,500-2,000 字）
   - 引用支持文件
5. **添加资源**：按要求创建 references/、examples/、scripts/
6. **验证**：检查描述、写作风格、组织
7. **测试**：验证技能在预期触发器上加载
8. **迭代**：根据使用进行改进

专注于强触发器描述、渐进式披露和命令式写作风格，以创建有效技能，在需要时加载并提供针对性指导。
