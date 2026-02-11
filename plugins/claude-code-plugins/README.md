# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code 是一个代理式编码工具，驻留在您的终端中，理解您的代码库，并通过执行常规任务、解释复杂代码和处理 git 工作流来帮助您更快地编码——所有这些都通过自然语言命令完成。您可以在终端、IDE 中使用它，或在 Github 上标记 @claude。

**在[官方文档](https://code.claude.com/docs/en/overview)中了解更多信息。**

<img src="./demo.gif" />

## 入门指南

> [!NOTE]
> 通过 npm 安装已被弃用。请使用以下推荐方法之一。

如需更多安装选项、卸载步骤和故障排除，请参阅[设置文档](https://code.claude.com/docs/en/setup)。

1. 安装 Claude Code：

    **MacOS/Linux（推荐）：**
    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Homebrew (MacOS/Linux):**
    ```bash
    brew install --cask claude-code
    ```

    **Windows（推荐）：**
    ```powershell
    irm https://claude.ai/install.ps1 | iex
    ```

    **WinGet (Windows):**
    ```powershell
    winget install Anthropic.ClaudeCode
    ```

    **NPM（已弃用）：**
    ```bash
    npm install -g @anthropic-ai/claude-code
    ```

2. 导航到您的项目目录并运行 `claude`。

## 插件

此存储库包含多个 Claude Code 插件，通过自定义命令和代理扩展功能。请参阅[插件目录](./plugins/README.md)了解可用插件的详细文档。

## 报告 Bug

我们欢迎您的反馈。使用 `/bug` 命令直接在 Claude Code 中报告问题，或提交 [GitHub issue](https://github.com/anthropics/claude-code/issues)。

## 在 Discord 上连接

加入 [Claude Developers Discord](https://anthropic.com/discord) 与其他使用 Claude Code 的开发者建立联系。获取帮助、分享反馈并讨论您的项目。

## 数据收集、使用和保留

当您使用 Claude Code 时，我们会收集反馈，包括使用数据（例如代码接受或拒绝）、相关的对话数据以及通过 `/bug` 命令提交的用户反馈。

### 我们如何使用您的数据

请参阅我们的[数据使用政策](https://code.claude.com/docs/en/data-usage)。

### 隐私保护措施

我们实施了多项保护措施来保护您的数据，包括敏感信息的有限保留期限、对用户会话数据的访问限制，以及禁止将反馈用于模型训练的明确政策。

如需完整详情，请查阅我们的[商业服务条款](https://www.anthropic.com/legal/commercial-terms)和[隐私政策](https://www.anthropic.com/legal/privacy)。
