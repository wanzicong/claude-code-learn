## anthropic-agent-skills 使用与实战笔记（中文）

### 1. 仓库整体定位

- **官方示例技能库**：Anthropic 官方维护的 Agent Skills 示例仓库，展示如何用 Skills 系统为 Claude 增强特定领域能力。
- **同时是插件市场源**：通过 `.claude-plugin/marketplace.json`，在 Claude Code 中作为插件市场使用，提供两个主要插件集合：
  - `document-skills`：文档处理套件（Word/Excel/PPT/PDF）。
  - `example-skills`：各类示例技能集合（测试、设计、品牌、Skill 构建等）。
- **也是最佳实践参考**：每个 `skills/*/SKILL.md` 都是高质量的 Skill 设计范例，可直接拷贝+修改，快速建立自己的技能库。

### 2. 主要目录结构速览

- `README.md`：英文总说明，含 Skills 概念、官方文档与 API 链接。
- `.claude-plugin/marketplace.json`：定义插件市场，包含：
  - `document-skills`：聚合 `skills/xlsx`, `skills/docx`, `skills/pptx`, `skills/pdf`。
  - `example-skills`：聚合一批示例技能（见下文分类）。
- `skills/`：真正的技能目录，每个子目录一个技能，基本结构：
  - `SKILL.md`：必需。包含 YAML frontmatter（`name`、`description`）和正文说明（使用指南、示例、工作流等）。
  - `scripts/`（可选）：Python / Bash 等脚本，用于复杂或需要确定性的操作。
  - `references/`（可选）：较长的参考文档，按需加载进上下文。
  - `assets/` / `templates/` / `themes/` 等（可选）：模板、字体、图片等产出资源。
- `spec/agent-skills-spec.md`：Agent Skills 规范说明，定义 Skill 的结构与设计原则。
- `template/SKILL.md`：最小 Skill 模板，适合作为自定义技能的起点。

### 3. 技能分类（便于记忆）

#### 3.1 文档与办公类（Document Skills）

- `docx`：Word 文档生成、编辑、结构化处理。
- `pdf`：PDF 表单/结构解析、字段提取、填表等。
- `pptx`：PPT 幻灯片生成、编辑、缩略图、校验。
- `xlsx`：Excel 表格校验、结构化数据读写、重算。

**典型用途**：批量生成报告、解析和填充合同表单、批量修改文档模板等。

#### 3.2 开发与技术工作流类（Dev / Technical）

- `webapp-testing`：为 Web 应用设计测试策略与脚本，有示例 Python 代码。
- `mcp-builder`：帮助设计和实现 MCP 服务器（接口设计、评估脚本等）。
- `web-artifacts-builder`：打包 Web demo / 前端工件，生成可分享的包。
- `frontend-design`：前端 UI/UX 设计与组件结构建议。
- `skill-creator`：指导如何创建高质量 Skill（结构、长度控制、脚本/引用拆分等）。

**典型用途**：自动化测试、工具集成、代码结构设计、自建 Skill 工作流。

#### 3.3 品牌、沟通与内容创作类（Brand / Comms）

- `brand-guidelines`：统一品牌语气、用词和视觉风格。
- `internal-comms`：公司内部沟通（公告、FAQ、Newsletter 等），自带 examples 模板。
- `doc-coauthoring`：文档协同创作，把 Claude 当成写作搭档。

**典型用途**：对外文案统一风格、内部变更说明、长文档协同撰写。

#### 3.4 设计、主题与创意类（Design / Themes / Creative）

- `algorithmic-art`：算法艺术（生成基于代码/规则的视觉效果）。
- `canvas-design`：画布与版式设计（海报、封面布局等）。
- `theme-factory`：应用/网站主题工厂，提供多套主题示例与说明。
- `slack-gif-creator`：生成 Slack/GIF 表情，目录含生成脚本与核心逻辑。

**典型用途**：UI 视觉探索、品牌主题设计、社交媒体与动效素材。

### 4. 在 Claude Code 中的使用步骤（重点）

1. **注册插件市场源**
   ```text
   /plugin marketplace add anthropics/skills
   ```
2. **安装插件集合**
   - 通过 UI：`Browse and install plugins` → 选择 `anthropic-agent-skills` → 安装 `document-skills` 或 `example-skills`。
   - 或在对话中直接安装：
     ```text
     /plugin install document-skills@anthropic-agent-skills
     /plugin install example-skills@anthropic-agent-skills
     ```
3. **在对话中调用技能**
   - 安装后，只需在需求中**点名技能或场景**，Claude 会自动决定是否触发。例如：
     - “使用 `pdf` 技能，从 `docs/contract.pdf` 中提取所有表单字段为 JSON。”
     - “用 `webapp-testing` 帮我为当前前端项目设计端到端测试计划，并生成示例脚本。”
     - “按照 `skill-creator` 的原则，帮我写一个团队内部 Python 代码审查 Skill。”

### 5. 自定义技能的实战套路

1. **选模板 Skill**：从本仓库中挑一个接近需求的技能（如 `webapp-testing`、`skill-creator`）作为参考。
2. **复制结构到自己项目**：在自己的插件目录下新建 `my-skill/`，包含 `SKILL.md` 和必要的 `scripts/`、`references/` 等。
3. **编写/优化 `SKILL.md`**：
   - 使用 `skill-creator` 这类元技能，请 Claude 帮你起草与润色。
   - 明确写清：做什么、何时触发、输出格式、工作流步骤。
4. **在 Claude Code 中加载并使用**：
   - 确保工作区包含你的 Skill 目录。
   - 在对话中以 “使用 `my-skill` 技能……” 的方式调用，观察行为并迭代调整。

> 简单记忆：`anthropic-agent-skills` = 官方技能「示例库 + 规范 + 模板 + 插件市场源」，既可直接用，也适合作为你自建技能体系的参考蓝本。

