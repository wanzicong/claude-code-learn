# Claude Code 插件

此目录包含一些官方 Claude Code 插件，通过自定义命令、代理和工作流扩展功能。这些是 Claude Code 插件系统可能性的示例——通过社区市场可以找到更多插件。

## 什么是 Claude Code 插件？

Claude Code 插件是扩展，通过自定义斜杠命令、专用代理、钩子和 MCP 服务器增强 Claude Code。插件可以在项目和团队之间共享，提供一致的工具和工作流。

在[官方插件文档](https://docs.claude.com/en/docs/claude-code/plugins)中了解更多。

## 此目录中的插件

| 名称 | 描述 | 内容 |
|------|-------------|----------|
| [agent-sdk-dev](./agent-sdk-dev/) | 用于使用 Claude Agent SDK 的开发工具包 | **命令：** `/new-sdk-app` - 新 Agent SDK 项目的交互式设置<br>**代理：** `agent-sdk-verifier-py`、`agent-sdk-verifier-ts` - 根据最佳实践验证 SDK 应用程序 |
| [claude-opus-4-5-migration](./claude-opus-4-5-migration/) | 将代码和提示从 Sonnet 4.x 和 Opus 4.1 迁移到 Opus 4.5 | **技能：** `claude-opus-4-5-migration` - 自动迁移模型字符串、beta 标头和提示调整 |
| [code-review](./code-review/) | 使用多个专用代理进行自动化 PR 代码审查，通过基于置信度的评分过滤误报 | **命令：** `/code-review` - 自动化 PR 审查工作流<br>**代理：** 5 个并行 Sonnet 代理，用于 CLAUDE.md 合规性、Bug 检测、历史上下文、PR 历史和代码注释 |
| [commit-commands](./commit-commands/) | Git 工作流自动化，用于提交、推送和创建拉取请求 | **命令：** `/commit`、`/commit-push-pr`、`/clean_gone` - 简化的 Git 操作 |
| [explanatory-output-style](./explanatory-output-style/) | 添加关于实现选择和代码库模式的教育见解（模仿已弃用的 Explanatory 输出样式） | **钩子：** SessionStart - 在每个会话开始时注入教育上下文 |
| [feature-dev](./feature-dev/) | 具有结构化 7 阶段方法的综合功能开发工作流 | **命令：** `/feature-dev` - 引导式功能开发工作流<br>**代理：** `code-ex`、`code-architect`、`code-reviewer` - 用于代码库分析、架构设计和质量审查 |
| [frontend-design](./frontend-design/) | 创建独特的生产级前端界面，避免通用的 AI 美学 | **技能：** `frontend-design` - 为前端工作自动调用，提供关于大胆设计选择、排版、动画和视觉细节的指导 |
| [hookify](./hookify/) | 轻松创建自定义钩子，通过分析对话模式或显式指令来防止不良行为 | **命令：** `/hookify`、`/hookify:list`、`/hookify:configure`、`/hookify:help`<br>**代理：** `conversation-analyzer` - 分析对话中的问题行为<br>**技能：** `writing-rules` - 关于 hookify 规则语法的指导 |
| [learning-output-style](./learning-output-style/)) | 交互式学习模式，在决策点要求有意义的代码贡献（模仿未发布的 Learning 输出样式） | **钩子：** SessionStart - 鼓励用户在决策点编写有意义的代码（5-10 行），同时获得教育见解 |
| [plugin-dev](./plugin-dev/) | 开发 Claude Code 插件的综合工具包，包含 7 个专家技能和 AI 辅助创建 | **命令：** `/plugin-dev:create-plugin` - 构建插件的 8 阶段引导工作流<br>**代理：** `agent-creator`、`plugin-validator`、`skill-reviewer`<br>**技能：** 钩子开发、MCP 集成、插件结构、设置、命令、代理和技能开发 |
| [pr-review-toolkit](./pr-review-toolkit/)) | 专用于注释、测试、错误处理、类型设计、代码质量和代码简化的综合 PR 审查代理 | **命令：** `/pr-review-toolkit:review-pr` - 使用可选审查方面运行（注释、测试、错误、类型、代码、简化、全部）<br>**代理：** `comment-analyzer`、`pr-test-analyzer`、`silent-failure-hunter`、`type-design-analyzer`、`code-reviewer`、`code-simplifier` |
| [ralph-wiggum](./ralph-wiggum/) | 用于迭代开发的交互式自引用 AI 循环。Claude 重复处理同一任务直到完成 | **命令：** `/ralph-loop`、`/cancel-ralph` - 启动/停止自主迭代循环<br>**钩子：** Stop - 拦截退出尝试以继续迭代 |
| [security-guidance](./security-guidance/)) | 安全提醒钩子，在编辑文件时警告潜在的安全问题 | **钩子：** PreToolUse - 监控 9 种安全模式，包括命令注入、XSS、eval 使用、危险的 HTML、pickle 反序列化和 os.system 调用 |

## 安装

这些插件包含在 Claude Code 仓库中。要在您自己的项目中使用它们：

1. 全局安装 Claude Code：
```bash
npm install -g @anthropic-ai/claude-code
```

2. 导航到您的项目并运行 Claude Code：
```bash
claude
```

3. 使用 `/plugin` 命令从市场安装插件，或在项目的 `.claude/settings.json` 中配置它们。

有关详细的插件安装和配置，请参阅[官方文档](https://docs.claude.com/en/docs/claude-code/plugins)。

## 插件结构

每个插件都遵循标准的 Claude Code 插件结构：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据
├── commands/                # 斜杠命令（可选）
├── agents/                  # 专用代理（可选）
├── skills/                  # 代理技能（可选）
├── hooks/                   # 事件处理器（可选）
├── .mcp.json                # 外部工具配置（可选）
└── README.md                # 插件文档
```

## 贡献

向此目录添加新插件时：

1. 遵循标准插件结构
2. 包含全面的 README.md
3. 在 `.claude-plugin/plugin.json` 中添加插件元数据
4. 记录所有命令和代理
5. 提供使用示例

## 了解更多

- [Claude Code 文档](https://docs.claude.com/en/docs/claude-code/overview)
- [插件系统文档](https://docs.claude.com/en/docs/claude-code/plugins)
- [Agent SDK 文档](https://docs.claude.com/en/api/agent-sdk/overview)
