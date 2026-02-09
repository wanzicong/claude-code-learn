## plugins 目录说明

这个 `plugins` 目录是一个「Claude / Cursor 插件与技能学习与示例集合」，方便你学习、对照和扩展自己的开发助手能力。它目前主要包含三大部分：

- **`anthropic-agent-skills`**：官方/示例 Agent Skills 仓库  
  - 存放大量针对不同场景的 `SKILL.md` 与配套资源（脚本、字体、参考文档等）。  
  - 这些技能可以被 Claude/Cursor 的 Agent 调用，用来增强特定领域能力（如代码分析、写作风格、知识库等）。  

- **`claude-code-plugins`**：Claude Code 插件工程示例仓库  
  - 展示如何开发、组织和发布 Claude Code 插件。  
  - 关键结构：
    - `.claude/commands/`：通用命令工作流示例（如 `commit-push-pr.md`、`dedupe.md` 等）。  
    - `.claude-plugin/marketplace.json`：该工程在插件市场中的元数据示例。  
    - `plugins/`：一组内置插件示例，每个子目录通常包含：
      - `.claude-plugin/plugin.json`：插件入口与元数据。  
      - `commands/`：该插件提供的具体命令（Markdown 工作流）。  
      - `agents/` / `skills/`：可选的 Agent 定义和技能定义。  
      - `hooks/` / `scripts/`：用于自动化或扩展行为的脚本与 hook。  
  - 适合作为「如何写自己的 Claude Code 插件」的参考模板。  

- **`claude-plugins-official`**：官方插件与第三方服务配置示例  
  - `external_plugins/`：针对 Asana、GitHub、GitLab、Stripe、Slack、Supabase 等服务的示例插件配置：
    - `.claude-plugin/plugin.json`：描述插件在 Claude 中的表现形式。  
    - `.mcp.json`：对应的 MCP 服务器配置，用于连接外部服务 API。  
  - `plugins/`：一组官方插件示例（如 `code-review`、`commit-commands`、`plugin-dev`、各种 LSP 插件等），结构与 `claude-code-plugins/plugins` 类似。  
  - 适合用来学习如何接入第三方服务或语言服务器。  

- **`python-dev-assistant`**：Python 开发助手插件工程  
  - 一个针对 Python 项目的专用插件，用来做代码检查、框架指导和文档生成等。  
  - 主要结构：
    - `.claude-plugin/marketplace.json`：在插件市场中的展示与配置。  
    - `agents/python-code-analyzer.md`：定义 Python 代码分析 Agent。  
    - `commands/`：一组 Python 相关命令：
      - `py-check.md`：代码检查与风格校验。  
      - `py-django.md`：Django 相关开发辅助。  
      - `py-flask.md`：Flask 相关开发辅助。  
      - `py-docs.md`：文档与注释生成/改进。  
      - `py-snippet.md`：代码片段生成与重构。  
    - `skills/`：Python 相关技能：
      - `django-flask-architecture/SKILL.md`：Django/Flask 项目结构与最佳实践。  
      - `python-best-practices/`：PEP8 与 Python 代码规范示例与指南。  
      - `python-documentation/SKILL.md`：Python 文档与 docstring 编写规范。  
    - `hooks/`：如 `check-python-style.sh`，配合 `hooks.json` 实现自动风格检查。  
  - 这是你当前重点使用和可以二次开发的插件工程。  

## 如何使用与扩展

- **想学习插件开发**：优先参考 `claude-code-plugins` 和 `claude-plugins-official/plugins` 中的各个插件目录，看它们的 `.claude-plugin/plugin.json`、`commands`、`skills` 等是如何组织的。  
- **想强化 Python 工作流**：在 `python-dev-assistant/commands` 和 `skills` 里新增或修改命令、技能即可，结构沿用现有文件即可快速扩展。  
- **想接入第三方服务**：参考 `claude-plugins-official/external_plugins` 下的示例（如 `github`、`stripe` 等），仿照它们的 `.mcp.json` 与 `.claude-plugin/plugin.json`。  

你后续如果有新的自定义插件或技能，也可以直接在这个 `plugins` 目录下新建子文件夹，按上述结构组织，便于维护和复用。

