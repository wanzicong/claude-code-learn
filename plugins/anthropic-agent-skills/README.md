# Anthropic Agent Skills - 完整指南

> **注意：** 本仓库包含 Anthropic 官方实现的 Claude 技能集。关于 Agent Skills 标准的更多信息，请访问 [agentskills.io](http://agentskills.io)。

## 目录

- [什么是技能（Skills）](#什么是技能skills)
- [关于本仓库](#关于本仓库)
- [快速开始](#快速开始)
- [技能分类](#技能分类)
- [使用指南](#使用指南)
- [创建自定义技能](#创建自定义技能)
- [实战笔记](#实战笔记)
- [合作伙伴技能](#合作伙伴技能)
- [第三方许可声明](#第三方许可声明)

---

## 什么是技能（Skills）

技能是包含指令、脚本和资源的文件夹，Claude 可以动态加载这些内容以提高在专业任务上的表现。技能教会 Claude 如何以可重复的方式完成特定任务，无论是使用公司品牌指南创建文档、使用组织特定工作流分析数据，还是自动化个人任务。

### 更多信息

- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [为真实世界的代理配备 Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## 关于本仓库

### 仓库定位

本仓库是 Anthropic 官方维护的 Agent Skills 示例库，展示了 Claude 技能系统的各种可能性。这些技能涵盖从创意应用（艺术、音乐、设计）到技术任务（测试 Web 应用、MCP 服务器生成）再到企业工作流（沟通、品牌等）的广泛领域。

**三重角色：**

1. **官方示例技能库**：展示如何用 Skills 系统为 Claude 增强特定领域能力
2. **插件市场源**：通过 `.claude-plugin/marketplace.json` 在 Claude Code 中作为插件市场使用
3. **最佳实践参考**：每个 `skills/*/SKILL.md` 都是高质量的 Skill 设计范例

### 目录结构

```
anthropic-agent-skills/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
├── skills/                        # 技能目录
│   ├── docx/                     # Word 文档处理
│   ├── pdf/                      # PDF 处理
│   ├── pptx/                     # PowerPoint 处理
│   ├── xlsx/                     # Excel 处理
│   ├── webapp-testing/           # Web 应用测试
│   ├── mcp-builder/              # MCP 服务器构建
│   ├── skill-creator/            # 技能创建指南
│   └── ...                       # 更多技能
├── spec/
│   └── agent-skills-spec.md      # Agent Skills 规范
├── template/
│   └── SKILL.md                  # 技能模板
├── README.md                      # 本文档
├── NOTES.md                       # 使用笔记
└── THIRD_PARTY_NOTICES.md        # 第三方许可
```

每个技能的基本结构：
- `SKILL.md`：必需。包含 YAML frontmatter 和使用说明
- `scripts/`（可选）：Python/Bash 等脚本
- `references/`（可选）：参考文档
- `assets/`、`templates/`、`themes/` 等（可选）：资源文件

### 免责声明

**这些技能仅用于演示和教育目的。** 虽然其中一些功能可能在 Claude 中可用，但您从 Claude 获得的实现和行为可能与这些技能中显示的不同。这些技能旨在说明模式和可能性。在将它们用于关键任务之前，请务必在您自己的环境中彻底测试技能。

### 许可说明

本仓库中的许多技能是开源的（Apache 2.0）。我们还包含了为 [Claude 文档功能](https://www.anthropic.com/news/create-files)提供支持的��档创建和编辑技能，位于 `skills/docx`、`skills/pdf`、`skills/pptx` 和 `skills/xlsx` 子文件夹中。这些是源代码可用的，但不是开源的，我们希望与开发者分享这些作为更复杂技能的参考，这些技能在生产 AI 应用程序中被积极使用。

---

## 快速开始

### 在 Claude Code 中使用

#### 1. 注册插件市场源

```bash
/plugin marketplace add anthropics/skills
```

#### 2. 安装插件集合

**方式一：通过 UI**
1. 选择 `Browse and install plugins`
2. 选择 `anthropic-agent-skills`
3. 选择 `document-skills` 或 `example-skills`
4. 选择 `Install now`

**方式二：命令行安装**
```bash
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

#### 3. 使用技能

安装插件后，只需在对话中提及技能即可使用。例如：

```
使用 PDF 技能从 path/to/some-file.pdf 中提取表单字段
```

### 在 Claude.ai 中使用

这些示例技能已经在 Claude.ai 的付费计划中可用。

要使用本仓库中的任何技能或上传自定义技能，请按照[在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b)中的说明操作。

### 通过 Claude API 使用

您可以通过 Claude API 使用 Anthropic 的预构建技能并上传自定义技能。有关更多信息，请参阅 [Skills API 快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)。

---

## 技能分类

### 文档与办公类（Document Skills）

| 技能 | 描述 | 典型用途 |
|------|------|----------|
| **docx** | Word 文档生成、编辑、结构化处理 | 批量生成报告、修改文档模板 |
| **pdf** | PDF 表单/结构解析、字段提取、填表 | 解析和填充合同表单 |
| **pptx** | PPT 幻灯片生成、编辑、缩略图、校验 | 自动生成演示文稿 |
| **xlsx** | Excel 表格校验、结构化数据读写、重算 | 数据分析、报表生成 |

### 开发与技术工作流类（Dev / Technical）

| 技能 | 描述 | 典型用途 |
|------|------|----------|
| **webapp-testing** | Web 应用测试策略与脚本设计 | 自动化测试、端到端测试 |
| **mcp-builder** | MCP 服务器设计和实现 | 工具集成、API 设计 |
| **web-artifacts-builder** | Web demo / 前端工件打包 | 生成可分享的前端包 |
| **frontend-design** | 前端 UI/UX 设计与组件结构 | 界面设计、组件架构 |
| **skill-creator** | 创建高质量 Skill 的指南 | 自建技能工作流 |

### 品牌、沟通与内容创作类（Brand / Comms）

| 技能 | 描述 | 典型用途 |
|------|------|----------|
| **brand-guidelines** | 统一品牌语气、用词和视觉风格 | 对外文案统一风格 |
| **internal-comms** | 公司内部沟通（公告、FAQ、Newsletter） | 内部变更说明 |
| **doc-coauthoring** | 文档协同创作 | 长文档协同撰写 |

### 设计、主题与创意类（Design / Themes / Creative）

| 技能 | 描述 | 典型用途 |
|------|------|----------|
| **algorithmic-art** | 算法艺术（基于代码/规则的视觉效果） | UI 视觉探索 |
| **canvas-design** | 画布与版式设计（海报、封面布局） | 品牌主题设计 |
| **theme-factory** | 应用/网站主题工厂 | 主题设计系统 |
| **slack-gif-creator** | 生成 Slack/GIF 表情 | 社交媒体素材 |

---

## 使用指南

### 在 Claude Code 中调用技能

安装后，只需在需求中**点名技能或场景**，Claude 会自动决定是否触发。

**示例：**

```
使用 pdf 技能，从 docs/contract.pdf 中提取所有表单字段为 JSON
```

```
用 webapp-testing 帮我为当前前端项目设计端到端测试计划，并生成示例脚本
```

```
按照 skill-creator 的原则，帮我写一个团队内部 Python 代码审查 Skill
```

### 技能集合说明

本仓库提供两个主要插件集合：

1. **document-skills**：文档处理套件
   - 包含：`docx`、`pdf`、`pptx`、`xlsx`
   - 适用于：文档自动化、数据处理、报表生成

2. **example-skills**：各类示例技能集合
   - 包含：测试、设计、品牌、Skill 构建等
   - 适用于：学习参考、工作流优化

---

## 创建自定义技能

### 基础技能结构

技能创建非常简单 - 只需一个包含 `SKILL.md` 文件的文件夹，该文件包含 YAML frontmatter 和指令。您可以使用本仓库中的 **template-skill** 作为起点：

```markdown
---
name: my-skill-name
description: 清晰描述此技能的功能以及何时使用它
---

# 我的技能名称

[在此添加 Claude 激活此技能时将遵循的指令]

## 示例
- 示例用法 1
- 示例用法 2

## 指南
- 指南 1
- 指南 2
```

### 必需字段

frontmatter 只需要两个字段：
- `name` - 技能的唯一标识符（小写，空格用连字符）
- `description` - 技能功能和使用时机的完整描述

下面的 markdown 内容包含 Claude 将遵循的指令、示例和指南。有关更多详细信息，请参阅[如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

### 自定义技能实战套路

1. **选择模板技能**
   - 从本仓库中挑选一个接近需求的技能作为参考
   - 例如：`webapp-testing`、`skill-creator`

2. **复制结构到自己项目**
   - 在自己的插件目录下新建 `my-skill/`
   - 包含 `SKILL.md` 和必要的 `scripts/`、`references/` 等

3. **编写/优化 `SKILL.md`**
   - 使用 `skill-creator` 这类元技能，请 Claude 帮你起草与润色
   - 明确写清：做什么、何时触发、输出格式、工作流步骤

4. **在 Claude Code 中加载并使用**
   - 确保工作区包含你的 Skill 目录
   - 在对话中以 "使用 `my-skill` 技能……" 的方式调用
   - 观察行为并迭代调整

---

## 实战笔记

### 核心概念

**简单记忆：** `anthropic-agent-skills` = 官方技能「示例库 + 规范 + 模板 + 插件市场源」，既可直接用，也适合作为你自建技能体系的参考蓝本。

### 技能设计原则

1. **明确触发条件**
   - 在 `description` 中清晰说明何时使用此技能
   - 提供具体的使用场景和关键词

2. **结构化指令**
   - 使用清晰的标题和列表
   - 提供具体的步骤和示例
   - 包含边界情况的处理说明

3. **模块化设计**
   - 将复杂逻辑拆分到 `scripts/` 中
   - 将长文档放到 `references/` 中按需加载
   - 保持 `SKILL.md` 简洁明了

4. **可测试性**
   - 提供测试用例和预期输出
   - 包含验证步骤
   - 考虑错误处理

### 最佳实践

- **从简单开始**：先创建基础版本，逐步迭代
- **参考现有技能**：学习本仓库中的优秀示例
- **测试充分**：在实际场景中验证技能行为
- **文档完善**：提供清晰的使用说明和示例
- **版本控制**：使用 Git 管理技能的演进

---

## 合作伙伴技能

技能是教 Claude 如何更好地使用特定软件的绝佳方式。随着我们看到来自合作伙伴的出色示例技能，我们可能会在此处重点介绍其中一些：

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)

---

## 第三方许可声明

本产品的部分内容可能包含第三方软件。以下列出了归属声明。

### BSD 2-Clause License

以下组件根据 BSD 2-Clause License 授权：

- **imageio 2.37.0**，版权所有 (c) 2014-2022, imageio developers
- **imageio-ffmpeg 0.6.0**，版权所有 (c) 2019-2025, imageio

**许可文本：**

在满足以下条件的情况下，允许以源代码和二进制形式重新分发和使用，无论是否经过修改：

1. 源代码的重新分发必须保留上述版权声明、此条件列表和以下免责声明。
2. 二进制形式的重新分发必须在随分发提供的文档和/或其他材料中复制上述版权声明、此条件列表和以下免责声明。

本软件由版权持有者和贡献者"按原样"提供，不提供任何明示或暗示的保证，包括但不限于对适销性和特定用途适用性的暗示保证。在任何情况下，版权持有者或贡献者均不对任何直接、间接、偶然、特殊、惩戒性或后果性损害（包括但不限于替代商品或服务的采购；使用、数据或利润的损失；或业务中断）负责，无论是在合同、严格责任或侵权（包括疏忽或其他）的任何责任理论下，即使已被告知此类损害的可能性。

### GNU General Public License v3.0

以下组件根据 GNU General Public License v3.0 授权：

- **FFmpeg 7.0.2**，版权所有 (c) 2000-2024 the FFmpeg developers
- 源代码：[https://ffmpeg.org/releases/ffmpeg-7.0.2.tar.xz](https://ffmpeg.org/releases/ffmpeg-7.0.2.tar.xz)

完整的 GPL v3.0 许可文本请参见原始 THIRD_PARTY_NOTICES.md 文件。

### MIT-CMU License (HPND)

以下组件根据 MIT-CMU License (HPND) 授权：

- **Pillow 11.3.0**，版权所有 © 1997-2011 by Secret Labs AB, © 1995-2011 by Fredrik Lundh and contributors, © 2010 by Jeffrey A. Clark and contributors

### SIL Open Font License v1.1

以下字体根据 SIL Open Font License v1.1 授权：

Arsenal SC, Big Shoulders, Boldonse, Bricolage Grotesque, Crimson Pro, DM Mono, Erica One, Geist Mono, Gloock, IBM Plex Mono, Instrument Sans, Italiana, JetBrains Mono, Jura, Libre Baskerville, Lora, National Park, Nothing You Could Do, Outfit, Pixelify Sans, Poiret One, Red Hat Mono, Silkscreen, Smooch Sans, Tektur, Work Sans, Young Serif

完整的许可文本和版权信息请参见原始 THIRD_PARTY_NOTICES.md 文件。

---

## 技能集合

- [./skills](./skills)：创意与设计、开发与技术、企业与沟通、文档技能的示例
- [./spec](./spec)：Agent Skills 规范
- [./template](./template)：技能模板

---

## 相关资源

- [Agent Skills 官方网站](http://agentskills.io)
- [Claude 支持文档](https://support.claude.com)
- [Anthropic 工程博客](https://anthropic.com/engineering)
- [Claude API 文档](https://docs.claude.com)

---

## 贡献

欢迎贡献！如果您创建了有趣的技能或改进了现有技能，请考虑提交 Pull Request。

## 许可证

本仓库中的大多数技能采用 Apache 2.0 许可证。文档处理技能（docx、pdf、pptx、xlsx）是源代码可用的，但不是开源的。详细信息请参见各个技能目录中的 LICENSE 文件。

---

**最后更新：** 2025年

**维护者：** Anthropic

**问题反馈：** 请通过 GitHub Issues 提交
