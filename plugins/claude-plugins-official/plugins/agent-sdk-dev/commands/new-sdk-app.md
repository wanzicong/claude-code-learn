---
description: 创建和设置新的 Claude Agent SDK 应用程序
argument-hint: [project-name]
---

你的任务是帮助用户创建新的 Claude Agent SDK 应用程序。请仔细遵循以下步骤：

## 参考文档

在开始之前，查看官方文档以确保你提供准确和最新的指导。使用 WebFetch 阅读这些页面：

1. **首先从概述开始**：https://docs.claude.com/en/api/agent-sdk/overview
2. **根据用户的语言选择，阅读适当的 SDK 参考**：
   - TypeScript：https://docs.claude.com/en/api/agent-sdk/typescript
   - Python：https://docs.claude.com/en/api/agent-sdk/python
3. **阅读概述中提到的相关指南**，例如：
   - 流式与单次模式
   - 权限
   - 自定义工具
   - MCP 集成
   - 子代理
   - 会话
   - 根据用户需求的其他相关指南

**重要**：始终检查并使用最新版本的软件包。在安装前使用 WebSearch 或 WebFetch 验证当前版本。

## 收集需求

重要：一次问一个问题。在问下一个问题之前等待用户的回答。这样用户更容易回答。

按此顺序询问问题（跳过用户已通过参数提供的任何问题）：

1. **语言**（首先问）："您想使用 TypeScript 还是 Python？"

   - 在继续之前等待回答

2. **项目名称**（第二问）："您想给您的项目起什么名字？"

   - 如果提供了 $ARGUMENTS，则将其用作项目名称并跳过此问题
   - 在继续之前等待回答

3. **代理类型**（第三问，但如果 #2 已经足够详细则跳过）："您正在构建什么类型的代理？一些示例：

   - 编码代理（SRE、安全审查、代码审查）
   - 业务代理（客户支持、内容创建）
   - 自定义代理（描述您的用例）"
   - 在继续之前等待回答

4. **起点**（第四问）："您想要：

   - 一个最小的 'Hello World' 示例来开始
   - 一个具有常用功能的基本代理
   - 基于您的用例的特定示例"
   - 在继续之前等待回答

5. **工具选择**（第五问）：让用户知道您将使用哪些工具，并确认这些是他们想要使用的工具（例如，他们可能更喜欢 pnpm 或 bun 而不是 npm）。在执行需求时尊重用户的偏好。

在所有问题都回答后，继续创建设置计划。

## 设置计划

根据用户的回答，创建一个包含以下内容的计划：

1. **项目初始化**：

   - 创建项目目录（如果不存在）
   - 初始化包管理器：
     - TypeScript：`npm init -y` 并设置 `package.json`，包含 type: "module" 和脚本（包括 "typecheck" 脚本）
     - Python：创建 `requirements.txt` 或使用 `poetry init`
   - 添加必要的配置文件：
     - TypeScript：创建具有 SDK 正确设置的 `tsconfig.json`
     - Python：如果需要，可选地创建配置文件

2. **检查最新版本**：

   - 在安装之前，使用 WebSearch 或检查 npm/PyPI 查找最新版本
   - 对于 TypeScript：检查 https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
   - 对于 Python：检查 https://pypi.org/project/claude-agent-sdk/
   - 通知用户您正在安装的版本

3. **SDK 安装**：

   - TypeScript：`npm install @anthropic-ai/claude-agent-sdk@latest`（或指定最新版本）
   - Python：`pip install claude-agent-sdk`（pip 默认安装最新版本）
   - 安装后，验证安装的版本：
     - TypeScript：检查 package.json 或运行 `npm list @anthropic-ai/claude-agent-sdk`
     - Python：运行 `pip show claude-agent-sdk`

4. **创建起始文件**：

   - TypeScript：创建带有基本查询示例的 `index.ts` 或 `src/index.ts`
   - Python：创建带有基本查询示例的 `main.py`
   - 包含正确的导入和基本错误处理
   - 使用最新 SDK 版本的现代、最新语法和模式

5. **环境设置**：

   - 创建包含 `ANTHROPIC_API_KEY=your_api_key_here` 的 `.env.example` 文件
   - 将 `.env` 添加到 `.gitignore`
   - 解释如何从 https://console.anthropic.com/ 获取 API 密钥

6. **可选：创建 .claude 目录结构**：
   - 提议为代理、命令和设置创建 `.claude/` 目录
   - 询问他们是否想要任何示例子代理或斜杠命令

## 实施

在收集需求并获得用户对计划的确认后：

1. 使用 WebSearch 或 WebFetch 检查最新软件包版本
2. 执行设置步骤
3. 创建所有必要的文件
4. 安装依赖项（始终使用最新的稳定版本）
5. 验证安装的版本并通知用户
6. 根据他们的代理类型创建工作示例
7. 在代码中添加有用的注释，解释每个部分的作用
8. **在完成之前验证代码工作**：
   - 对于 TypeScript：
     - 运行 `npx tsc --noEmit` 检查类型类型错误
     - 修复所有类型错误，直到类型完全通过
     - 确保导入和类型正确
     - 只有在类型检查通过无错误时才继续
   - 对于 Python：
     - 验证导入正确
     - 检查基本语法错误
   - **不要认为设置完成，直到代码成功验证**

## 验证

在创建所有文件并安装依赖项后，使用适当的验证器代理来验证 Agent SDK 应用程序是否正确配置并准备使用：

1. **对于 TypeScript 项目**：启动 **agent-sdk-verifier-ts** 代理来验证设置
2. **对于 Python 项目**：启动 **agent-sdk-verifier-py** 代理来验证设置
3. 代理将检查 SDK 使用、配置、功能以及是否遵循官方文档
4. 查看验证报告并解决任何问题

## 入门指南

设置和验证完成后，为用户提供：

1. **后续步骤**：

   - 如何设置他们的 API 密钥
   - 如何运行他们的代理：
     - TypeScript：`npm start` 或 `node --loader ts-node/esm index.ts`
     - Python：`python main.py`

2. **有用资源**：

   - 链接到 TypeScript SDK 参考：https://docs.claude.com/en/api/agent-sdk/typescript
   - 链接到 Python SDK 参考：https://docs.claude.com/en/api/agent-sdk/python
   - 解释关键概念：系统提示、权限、工具、MCP 服务器

3. **常见后续步骤**：
   - 如何自定义系统提示
   - 如何通过 MCP 添加自定义工具
   - 如何配置权限
   - 如何创建子代理

## 重要说明

- **始终使用最新版本**：在安装任何软件包之前，使用 WebSearch 或直接检查 npm/PyPI 查找最新版本
- **验证代码正确运行**：
  - 对于 TypeScript：在完成前运行 `npx tsc --noEmit` 并修复所有类型错误
  - 对于 Python：验证语法和导入正确
  - 不要认为任务完成，直到代码通过验证
- 安装后验证安装的版本并通知用户
- 检查官方文档是否有任何特定版本要求（Node.js 版本、Python 版本等）
- 在创建目录/文件之前始终检查它们是否已存在
- 使用用户首选的包管理器（TypeScript 用 npm、yarn、pnpm；Python 用 pip、poetry）
- 确保所有代码示例都功能正常且包含适当的错误处理
- 使用与最新 SDK 版本兼容的现代语法和模式
- 使体验具有互动性和教育性
- **一次问一个问题** - 不要在单个回答中问多个问题

首先只问第一个需求问题。在继续下一个问题之前等待用户的回答。
