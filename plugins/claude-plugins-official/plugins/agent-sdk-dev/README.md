# Agent SDK 开发插件

用于创建和验证 Python 和 TypeScript Claude Agent SDK 应用程序的综合插件。

## 概述

Agent SDK 开发插件简化了构建 Agent SDK 应用程序的整个生命周期，从初始脚手架到根据最佳实践进行验证。它帮助您使用最新的 SDK 版本快速启动新项目，并确保您的应用程序遵循官方文档模式。

## 功能

### 命令：`/new-sdk-app`

交互式命令，引导您创建新的 Claude Agent SDK 应用程序。

**它的作用：**
- 询问有关您项目的澄清问题（语言、名称、代理类型、起点）
- 检查并安装最新的 SDK 版本
- 创建所有必要的项目文件和配置
- 设置正确的环境文件（.env.example、.）
- 提供适合您用例的工作示例
- 运行类型检查（TypeScript）或语法验证（Python）
- 使用适当的验证器代理自动验证设置

**用法：**
```bash
/new-sdk-app my-project-name
```

或者简单地：
```bash
/new-sdk-app
```

该命令将交互式地问您：
1. 语言选择（TypeScript 或 Python）
2. 项目名称（如果未提供）
3. 代理类型（编码、业务、自定义）
4. 起点（最小、基本或特定示例）
5. 工具偏好（npm/yarn/pnpm 或 pip/poetry）

**示例：**
```bash
/new-sdk-app customer-support-agent
# → 为客户支持代理创建新的 Agent SDK 项目
# → 设置 TypeScript 或 Python 环境
# → 安装最新 SDK 版本
# → 自动验证设置
```

### 代理：`agent-sdk-verifier-py`

彻底验证 Python Agent SDK 应用程序的正确设置和最佳实践。

**验证检查：**
- SDK 安装和版本
- Python 环境设置（requirements.txt、pyproject.toml）
- 正确的 SDK 使用和模式
- 代理初始化和配置
- 环境和安全（.env、API 密钥）
- 错误处理和功能
- 文档完整性

**何时使用：**
- 创建新的 Python SDK 项目后
- 修改现有的 Python SDK 应用程序后
- 部署 Python SDK 应用程序之前

**用法：**
该代理在 `/new-sdk-app` 创建 Python 项目后自动运行，或者您可以通过以下方式触发它：
```
"验证我的 Python Agent SDK 应用程序"
"检查我的 SDK 应用程序是否遵循最佳实践"
```

**输出：**
提供综合报告，包括：
- 总体状态（通过 / 通过但有警告 / 失败）
- 阻止功能的关键问题
- 关于次优模式的警告
- 通过的检查列表

- 带有 SDK 文档参考的具体建议

### 代理：`agent-sdk-verifier-ts`

彻底验证 TypeScript Agent SDK 应用程序的正确设置和最佳实践。

**验证检查：**
- SDK 安装和版本
- TypeScript 配置（tsconfig.json）
- 正确的 SDK 使用和模式
- 类安全和导入
- 代理初始化和配置
- 环境和安全（.env、API 密钥）
- 错误处理和功能
- 文档完整性

**何时使用：**
- 创建新的 TypeScript SDK 项目后
- 修改现有的 TypeScript SDK 应用程序后
- 部署 TypeScript SDK 应用程序之前

**用法：**
该代理在 `/new-sdk-app` 创建 TypeScript 项目后自动运行，或者您可以通过以下方式触发它：
```
"验证我的 TypeScript Agent SDK 应用程序"
"检查我的 SDK 应用程序是否遵循最佳实践"
```

**输出：**
提供综合报告，包括：
- 总体状态（通过 / 通过但有警告 / 失败）
- 阻止功能的关键问题
- 关于次优模式的警告
- 通过的检查列表
- 带有 SDK 文档参考的具体建议

## 工作流程示例

以下是使用此插件的典型工作流程：

1. **创建新项目：**
```bash
/new-sdk-app code-reviewer-agent
```

2. **回答交互式问题：**
```
语言：TypeScript
代理类型：编码代理（代码审查）
起点：具有常用功能的基本代理
```

3. **自动验证：**
该命令自动运行 `agent-sdk-verifier-ts` 以确保一切正确设置。

4. **开始开发：**
```bash
# 设置您的 API 密钥
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 运行您的代理
npm
```

5. **更改后验证：**
```
"验证我的 SDK 应用程序"
```

## 安装

此插件包含在 Claude Code 存储库中。要使用它：

1. 确保 Claude Code 已安装
2. 插件命令和代理自动可用

## 最佳实践

- **始终使用最新的 SDK 版本**：`/new-sdk-app` 检查并安装最新版本
- **部署前验证**：部署到生产环境之前运行验证器代理
- **保护 API 密钥安全**：永远不要提交 `.env` 文件或硬编码 API 密钥
- **遵循 SDK 文档**：验证器代理检查官方模式
- **类型检查 TypeScript 项目**：定期运行 `npx tsc --noEmit`
- **测试您的代理**：为您的代理功能创建测试用例

## 资源

- [Agent SDK 概述](https://docs.claude.com/en/api/agent-sdk/overview)
- [TypeScript SDK 参考](https://docs.claude.com/en/api/agent-sdk/typescript)
- [Python SDK 参考](https://docs.claude.com/en/api/agent-sdk/python)
- [Agent SDK 示例](https://docs.claude.com/en/api/agent-sdk/examples)

## 故障排除

### TypeScript 项目中的类型错误

**问题**：创建后 TypeScript 项目有类型错误

**解决方案**：
- `/new-sdk-app` 命令自动运行类型检查
- 如果错误持续，检查您是否使用最新的 SDK 版本
- 验证您的 `tsconfig.json` 是否符合 SDK 要求

### Python 导入错误

**问题**：无法从 `claude_agent_sdk` 导入

**解决方案**：
- 确保您已安装依赖项：`pip install -r requirements.txt`
- 如果使用虚拟环境，请激活它
- 检查 SDK 是否已安装：`pip show claude-agent-sdk`

### 验证失败并显示警告

**问题**：验证器代理报告警告

**解决方案**：
- 查看报告中的具体警告
- 检查提供的 SDK 文档参考
- 警告不会阻止功能，但指示需要改进的区域

## 作者

Ashwin Bhat (ashwin@anthropic.com)

## 版本

1.0.0
