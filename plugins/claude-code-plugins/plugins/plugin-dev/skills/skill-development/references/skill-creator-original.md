---
name: skill-creator
description: 用于创建有效技能的指南。当用户想要创建新技能（或更新现有技能）以扩展 Claude 的能力，提供专门知识、工作流或工具集成时，应使用此技能。
license: 请参阅 LICENSE.txt 中的完整条款
---

# Skill Creator

此技能为创建有效技能提供指导。

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
- "我可以想象用户会要求诸如'Remove red-eye from this image'或'rotate this image'之类的内容。你能想象出此技能被使用的其他方式吗？"
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

### 步骤 3：初始化技能

此时，实际上是时候创建技能。

仅在技能被开发已经存在，并且需要迭代或打包时才跳过此步骤。在这种情况下，继续到下一步。

从头开始创建新技能时，始终运行 `init_skill.py` 脚本。该脚本方便地生成一个新的模板技能目录，自动包含技能所需的所有内容，使技能创建过程更加高效和可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

该脚本将：
- 在指定路径创建技能目录
- 生成具有适当 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可以自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 步骤 4：编辑技能

在编辑（新生成或现有）技能时，请记住技能是为另一个 Claude 实例使用而创建。专注于包括对 Claude 有益且非显而易见的信息。考虑什么过程知识、特定于领域的细节或可复用资产将帮助另一个 Claude 实例更有效地执行这些任务。

#### 从可复用的技能内容开始

要开始实现，从上面确定的可复用资源开始：`scripts/`、`references/` 和 `assets/` 文件。请注意，此步骤可能需要用户输入。例如，在实现 `brand-guidelines` 技能时，用户可能需要提供要存储在 `assets/` 中的品牌资产或模板，或要存储在 `references/` 中的文档。

此外，删除技能不需要的任何示例文件和目录。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数技能不会需要它们全部。

#### 更新 SKILL.md

**写作风格：** 使用**命令式/不定式形式**（动词优先指令）编写整个技能，而非第二人称。使用客观、指导性语言（例如"To accomplish X, do Y"而非"You should do X"或"If you need to do X"）。这为 AI 消费维持了一致性和清晰度。

要完成 SKILL.md，回答以下问题：

1. 技能的目的是什么，用几句话？
2. 何时应该使用技能？
3. 在实践中，Claude 应该如何使用技能？上面开发的所有可复用技能内容都应被引用，以便 Claude 知道如何使用它们。

### 步骤 5：打包技能

一旦技能就绪，应将其打包为可分发的 zip 文件，与用户共享。打包过程自动首先验证技能，以确保它满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选的输出目录规范：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **验证** 技能自动，检查：
   - YAML frontmatter 格式和必需字段
   - 技能命名约定和目录结构
   - 描述完整性和质量
   - 文件组织和资源引用

2. **打包** 技能（如果验证通过），创建以技能命名的 zip 文件（例如，`my-skill.zip`），该文件包含所有文件并保持正确的目录结构以供分发。

如果验证失败，脚本将报告错误并退出而不创建包。修复任何验证错误并再次运行打包命令。

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
