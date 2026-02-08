# Claude Code 插件市场完全指南

> 本文档整合了 Claude Code 插件市场的创建、分发和使用的完整指南

## 目录

- [第一部分：发现和安装插件](#第一部分发现和安装插件)
- [第二部分：创建和分发插件市场](#第二部分创建和分发插件市场)

---

## 第一部分：发现和安装插件

### 概述

插件通过自定义命令、代理、钩子和 MCP 服务器扩展 Claude Code。插件市场是帮助您发现和安装这些扩展的目录，无需自己构建。

### 市场工作原理

市场是他人创建和共享的插件目录。使用市场是一个两步过程：

1. **添加市场**：向 Claude Code 注册目录，以便您可以浏览可用内容。尚未安装任何插件。
2. **安装单个插件**：浏览目录并安装您想要的插件。

可以将其视为添加应用商店：添加商店让您可以访问浏览其集合，但您仍然可以单独选择要下载的应用。

### 官方 Anthropic 市场

官方 Anthropic 市场 (`claude-plugins-official`) 在您启动 Claude Code 时自动可用。

**安装官方插件：**

```shell
/plugin install plugin-name@claude-plugins-official
```

#### 官方市场插件分类

##### 1. 代码智能插件

代码智能插件帮助 Claude 更深入地理解您的代码库。这些插件使用语言服务器协议 (LSP)。

| 语言         | 插件                  | 所需二进制文件                      |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

> **注意**：如果在安装插件后看到 `Executable not found in $PATH` 错误，请安装所需的二进制文件。

##### 2. 外部集成插件

这些插件捆绑预配置的 MCP 服务器，连接外部服务：

- **源代码控制**：`github`、`gitlab`
- **项目管理**：`atlassian`（Jira/Confluence）、`asana`、`linear`、`notion`
- **设计**：`figma`
- **基础设施**：`vercel`、`firebase`、`supabase`
- **通信**：`slack`
- **监控**：`sentry`

##### 3. 开发工作流插件

为常见开发任务添加命令和代理：

- **commit-commands**：Git 提交工作流
- **pr-review-toolkit**：PR 审查专用代理
- **agent-sdk-dev**：Agent SDK 构建工具
- **plugin-dev**：插件创建工具包

##### 4. 输出样式插件

自定义 Claude 的响应方式：

- **explanatory-output-style**：教育性实现见解
- **learning-output-style**：交互式学习模式

### 快速开始：添加演示市场

#### 步骤 1：添加市场

```shell
/plugin marketplace add anthropics/claude-code
```

#### 步骤 2：浏览可用插件

运行 `/plugin` 打开插件管理器，查看四个选项卡：

- **发现**：浏览所有市场的可用插件
- **已安装**：查看和管理已安装的插件
- **市场**：管理已添加的市场
- **错误**：查看插件加载错误

#### 步骤 3：安装插件

选择插件并选择安装范围：

- **用户范围**：在所有项目中使用
- **项目范围**：为所有协作者安装
- **本地范围**：仅在当前仓库中使用

**命令行安装示例：**

```shell
/plugin install commit-commands@anthropics-claude-code
```

#### 步骤 4：使用插件

安装后，插件命令立即可用：

```shell
/commit-commands:commit
```

### 添加市场的多种方式

#### 1. 从 GitHub 添加

使用 `owner/repo` 格式：

```shell
/plugin marketplace add anthropics/claude-code
```

#### 2. 从其他 Git 主机添加

**使用 HTTPS：**

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**使用 SSH：**

```shell
/plugin marketplace add git@gitlab.com:company/plugins.git
```

**添加特定分支或标签：**

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

#### 3. 从本地路径添加

```shell
/plugin marketplace add ./my-marketplace
```

或直接指定 marketplace.json 文件：

```shell
/plugin marketplace add ./path/to/marketplace.json
```

#### 4. 从远程 URL 添加

```shell
/plugin marketplace add https://example.com/marketplace.json
```

> **注意**：基于 URL 的市场有一些限制，可能遇到"路径未找到"错误。

### 安装和管理插件

#### 安装插件

```shell
/plugin install plugin-name@marketplace-name
```

#### 管理已安装的插件

**禁用插件：**

```shell
/plugin disable plugin-name@marketplace-name
```

**重新启用插件：**

```shell
/plugin enable plugin-name@marketplace-name
```

**卸载插件：**

```shell
/plugin uninstall plugin-name@marketplace-name
```

**指定安装范围：**

```shell
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### 管理市场

#### 使用 CLI 命令

**列出所有市场：**

```shell
/plugin marketplace list
```

**更新市场：**

```shell
/plugin marketplace update marketplace-name
```

**删除市场：**

```shell
/plugin marketplace remove marketplace-name
```

> **警告**：删除市场将卸载从中安装的所有插件。

#### 配置自动更新

Claude Code 可以在启动时自动更新市场及其已安装的插件。

**通过 UI 配置：**

1. 运行 `/plugin` 打开插件管理器
2. 选择**市场**选项卡
3. 选择市场
4. 选择**启用自动更新**或**禁用自动更新**

**环境变量配置：**

完全禁用所有自动更新：

```shell
export DISABLE_AUTOUPDATER=true
```

仅保持插件自动更新：

```shell
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

### 配置团队市场

团队管理员可以在 `.claude/settings.json` 中配置自动市场安装：

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

### 故障排除

#### /plugin 命令无法识别

1. **检查版本**：运行 `claude --version`（需要 1.0.33 或更高版本）
2. **更新 Claude Code**：
   - Homebrew：`brew upgrade claude-code`
   - npm：`npm update -g @anthropic-ai/claude-code`
3. **重启 Claude Code**

#### 常见问题

- **市场未加载**：验证 URL 可访问，检查 `.claude-plugin/marketplace.json` 是否存在
- **插件安装失败**：检查插件源 URL 可访问性和权限
- **安装后文件未找到**：插件被复制到缓存，外部路径引用将失效
- **插件技能未出现**：清除缓存 `rm -rf ~/.claude/plugins/cache`，重启并重新安装

---

## 第二部分：创建和分发插件市场

### 概述

插件市场是一个目录，让你能够将插件分发给他人。Marketplace 提供集中式发现、版本跟踪、自动更新以及对多种源类型的支持。

### 创建市场的步骤

1. **创建插件**：构建一个或多个插件
2. **创建 marketplace 文件**：定义 `marketplace.json`
3. **托管 marketplace**：推送到 GitHub、GitLab 或其他 git 主机
4. **与用户共享**：用户使用 `/plugin marketplace add` 添加

### 演练：创建本地市场

#### 步骤 1：创建目录结构

```bash
mkdir -p my-marketplace/.claude-plugin
mkdir -p my-marketplace/plugins/review-plugin/.claude-plugin
mkdir -p my-marketplace/plugins/review-plugin/skills/review
```

#### 步骤 2：创建 Skill

创建 `SKILL.md` 文件：

```markdown
<!-- my-marketplace/plugins/review-plugin/skills/review/SKILL.md -->
---
description: Review code for bugs, security, and performance
disable-model-invocation: true
---

Review the code I've selected or the recent changes for:
- Potential bugs or edge cases
- Security concerns
- Performance issues
- Readability improvements

Be concise and actionable.
```

#### 步骤 3：创建插件 Manifest

创建 `plugin.json` 文件：

```json
{
  "name": "review-plugin",
  "description": "Adds a /review skill for quick code reviews",
  "version": "1.0.0"
}
```

#### 步骤 4：创建 Marketplace 文件

创建 `marketplace.json`：

```json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "review-plugin",
      "source": "./plugins/review-plugin",
      "description": "Adds a /review skill for quick code reviews"
    }
  ]
}
```

#### 步骤 5：添加和安装

```shell
/plugin marketplace add ./my-marketplace
/plugin install review-plugin@my-plugins
```

#### 步骤 6：测试

```shell
/review
```

> **重要提示**：插件安装时会被复制到缓存位置，无法使用 `../shared-utils` 等路径引用外部文件。

### Marketplace 架构详解

#### 必需字段

| 字段        | 类型     | 描述                                    | 示例             |
| :-------- | :----- | :------------------------------------ | :------------- |
| `name`    | string | Marketplace 标识符（kebab-case，无空格）       | `"acme-tools"` |
| `owner`   | object | Marketplace 维护者信息                     |                |
| `plugins` | array  | 可用插件列表                                | 见下文            |

**保留名称**：以下名称为 Anthropic 官方保留：
- `claude-code-marketplace`
- `claude-code-plugins`
- `claude-plugins-official`
- `anthropic-marketplace`
- `anthropic-plugins`
- `agent-skills`
- `life-sciences`

#### Owner 字段

| 字段      | 类型     | 必需 | 描述         |
| :------ | :----- | :- | :--------- |
| `name`  | string | 是  | 维护者或团队的名称  |
| `email` | string | 否  | 维护者的联系电子邮件 |

#### 可选元数据

| 字段                     | 类型     | 描述                        |
| :--------------------- | :----- | :------------------------ |
| `metadata.description` | string | 简短的 marketplace 描述        |
| `metadata.version`     | string | Marketplace 版本            |
| `metadata.pluginRoot`  | string | 添加到相对插件源路径的基目录            |

### 插件条目配置

#### 必需字段

| 字段       | 类型             | 描述                      |
| :------- | :------------- | :---------------------- |
| `name`   | string         | 插件标识符（kebab-case，无空格）   |
| `source` | string\|object | 插件源位置                   |

#### 可选字段

**标准元数据：**

| 字段            | 类型      | 描述                                                |
| :------------ | :------ | :------------------------------------------------ |
| `description` | string  | 简短的插件描述                                           |
| `version`     | string  | 插件版本                                              |
| `author`      | object  | 插件作者信息（`name` 必需，`email` 可选）                       |
| `homepage`    | string  | 插件主页或文档 URL                                       |
| `repository`  | string  | 源代码仓库 URL                                         |
| `license`     | string  | SPDX 许可证标识符（例如，MIT、Apache-2.0）                    |
| `keywords`    | array   | 用于插件发现和分类的标签                                      |
| `category`    | string  | 插件类别                                              |
| `tags`        | array   | 用于可搜索性的标签                                         |
| `strict`      | boolean | 为 true 时，marketplace 字段与 plugin.json 合并；为 false 时完全定义 |

**组件配置：**

| 字段           | 类型             | 描述                  |
| :----------- | :------------- | :------------------ |
| `commands`   | string\|array  | 命令文件或目录的自定义路径       |
| `agents`     | string\|array  | agent 文件的自定义路径      |
| `hooks`      | string\|object | 自定义 hooks 配置或路径     |
| `mcpServers` | string\|object | MCP server 配置或路径   |
| `lspServers` | string\|object | LSP server 配置或路径   |

### 插件源配置

#### 1. 相对路径

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

> **注意**：相对路径仅在通过 Git 添加市场时有效，URL 方式不支持。

#### 2. GitHub 仓库

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

**固定到特定版本：**

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| 字段     | 类型     | 描述                        |
| :----- | :----- | :------------------------ |
| `repo` | string | 必需。`owner/repo` 格式        |
| `ref`  | string | 可选。Git 分支或标签              |
| `sha`  | string | 可选。完整的 40 字符 git 提交 SHA |

#### 3. Git 仓库

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

**固定到特定版本：**

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| 字段    | 类型     | 描述                           |
| :---- | :----- | :--------------------------- |
| `url` | string | 必需。完整的 git 仓库 URL（必须以 `.git` 结尾） |
| `ref` | string | 可选。Git 分支或标签                  |
| `sha` | string | 可选。完整的 40 字符 git 提交 SHA     |

### 高级插件条目示例

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": [
    "./agents/security-reviewer.md",
    "./agents/compliance-checker.md"
  ],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

**关键要点：**

- **`commands` 和 `agents`**：可以指定多个目录或单个文件
- **`${CLAUDE_PLUGIN_ROOT}`**：在 hooks 和 MCP server 配置中使用此变量引用插件安装目录
- **`strict: false`**：插件不需要自己的 `plugin.json`，marketplace 条目定义一切

### 托管和分发市场

#### 在 GitHub 上托管（推荐）

1. **创建仓库**：为市场设置新仓库
2. **添加 marketplace 文件**：创建 `.claude-plugin/marketplace.json`
3. **与团队共享**：用户使用 `/plugin marketplace add owner/repo` 添加

**优势**：内置版本控制、问题跟踪和团队协作。

#### 在其他 Git 服务上托管

支持 GitLab、Bitbucket 和自托管服务器：

```shell
/plugin marketplace add https://gitlab.com/company/plugins.git
```

#### 私有仓库

Claude Code 支持从私有仓库安装插件。

**手动安装和更新**：使用现有的 git 凭证助手。

**自动更新**：需要设置环境变量：

| 提供商       | 环境变量                        | 注释                    |
| :-------- | :-------------------------- | :-------------------- |
| GitHub    | `GITHUB_TOKEN` 或 `GH_TOKEN` | 个人访问令牌或 GitHub App 令牌 |
| GitLab    | `GITLAB_TOKEN` 或 `GL_TOKEN` | 个人访问令牌或项目令牌           |
| Bitbucket | `BITBUCKET_TOKEN`           | 应用密码或仓库访问令牌           |

**设置令牌：**

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

#### 本地测试

在分发前本地测试：

```shell
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

#### 为团队要求市场

在 `.claude/settings.json` 中配置：

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

### 托管市场限制

管理员可以使用 `strictKnownMarketplaces` 限制用户可添加的市场。

#### 限制行为

| 值        | 行为                      |
| -------- | ----------------------- |
| 未定义（默认）  | 无限制，用户可以添加任何 marketplace |
| 空数组 `[]` | 完全锁定，用户无法添加任何新 marketplace |
| 源列表      | 用户只能添加允许列表中的 marketplace |

#### 常见配置

**禁用所有市场添加：**

```json
{
  "strictKnownMarketplaces": []
}
```

**仅允许特定市场：**

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

**使用正则表达式模式：**

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

### 验证和测试

#### 验证 Marketplace JSON

```bash
claude plugin validate .
```

或从 Claude Code 内：

```shell
/plugin validate .
```

#### 测试流程

1. 添加市场进行测试：

```shell
/plugin marketplace add ./path/to/marketplace
```

2. 安装测试插件：

```shell
/plugin install test-plugin@marketplace-name
```

### 故障排除

#### Marketplace 未加载

**症状**：无法添加市场或看不到其中的插件

**解决方案**：
- 验证 marketplace URL 是否可访问
- 检查 `.claude-plugin/marketplace.json` 是否存在
- 使用 `claude plugin validate` 验证 JSON 语法
- 对于私有仓库，确认访问权限

#### Marketplace 验证错误

| 错误                                                | 原因               | 解决方案                                       |
| :------------------------------------------------ | :--------------- | :----------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | 缺少 manifest      | 创建 `.claude-plugin/marketplace.json`       |
| `Invalid JSON syntax: Unexpected token...`        | JSON 语法错误        | 检查缺少的逗号、多余的逗号或未引用的字符串                      |
| `Duplicate plugin name "x" found in marketplace`  | 两个插件共享相同名称       | 为每个插件提供唯一的 `name` 值                        |
| `plugins[0].source: Path traversal not allowed`   | 源路径包含 `..`       | 使用相对于 marketplace 根目录的路径，不包含 `..`          |

**警告（非阻止性）**：
- `Marketplace has no plugins defined`：添加至少一个插件
- `No marketplace description provided`：添加 `metadata.description`
- `Plugin "x" uses npm source which is not yet fully implemented`：改用 `github` 或本地路径源

#### 插件安装失败

**症状**：Marketplace 出现但插件安装失败

**解决方案**：
- 验证插件源 URL 是否可访问
- 检查插件目录是否包含必需的文件
- 对于 GitHub 源，确保仓库是公开的或有访问权限
- 通过手动克隆/下载来测试插件源

#### 私有仓库身份验证失败

**手动安装和更新：**
- 验证已使用 git 提供商进行身份验证（例如 `gh auth status`）
- 检查凭证助手配置：`git config --global credential.helper`
- 尝试手动克隆仓库验证凭证

**后台自动更新：**
- 设置适当的令牌：`echo $GITHUB_TOKEN`
- 检查令牌权限（对仓库的读取访问权限）
- 对于 GitHub，确保令牌具有 `repo` 范围
- 对于 GitLab，确保令牌具有 `read_repository` 范围
- 验证令牌未过期

#### 相对路径插件在基于 URL 的市场中失败

**症状**：通过 URL 添加市场，但相对路径源的插件安装失败。

**原因**：基于 URL 的市场仅下载 `marketplace.json` 文件本身，不下载插件文件。

**解决方案**：
- **使用外部源**：将插件条目更改为使用 GitHub、npm 或 git URL 源
  ```json
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
- **使用基于 Git 的市场**：在 Git 仓库中托管市场并使用 git URL 添加

#### 安装后文件未找到

**症状**：插件安装但对文件的引用失败

**原因**：插件被复制到缓存目录，引用插件目录外文件的路径（如 `../shared-utils`）将无法工作。

**解决方案**：使用符号链接或重组目录结构。

---

## 相关资源

- [创建插件](/zh-CN/plugins) - 创建自己的插件
- [插件参考](/zh-CN/plugins-reference) - 完整的技术规范和架构
- [插件设置](/zh-CN/settings#plugin-settings) - 插件配置选项
- [strictKnownMarketplaces 参考](/zh-CN/settings#strictknownmarketplaces) - 托管市场限制

---

## 快速参考

### 常用命令

```shell
# 市场管理
/plugin marketplace add <source>          # 添加市场
/plugin marketplace list                  # 列出所有市场
/plugin marketplace update <name>         # 更新市场
/plugin marketplace remove <name>         # 删除市场

# 插件管理
/plugin install <name>@<marketplace>      # 安装插件
/plugin enable <name>@<marketplace>       # 启用插件
/plugin disable <name>@<marketplace>      # 禁用插件
/plugin uninstall <name>@<marketplace>    # 卸载插件

# 验证和调试
/plugin validate .                        # 验证市场配置
/plugin                                   # 打开插件管理器 UI
```

### 快捷方式

- `/plugin market` = `/plugin marketplace`
- `/plugin market rm` = `/plugin marketplace remove`
- 使用 **Tab** 键在插件管理器选项卡间切换
- 使用 **Shift+Tab** 向后切换选项卡

---

**文档版本**：基于 Claude Code 官方文档整理
**最后更新**：2024年
