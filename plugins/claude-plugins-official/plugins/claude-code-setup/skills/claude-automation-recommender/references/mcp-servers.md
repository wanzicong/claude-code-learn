# MCP 服务器推荐

MCP（模型上下文协议）服务器通过连接到外部工具和服务来扩展 Claude 的功能。

**注意**：这些是常见的 MCP 服务器。使用网络搜索找到代码库服务和集成特定的 MCP 服务器。

## 设置与团队共享

**连接方式：**
1. **项目配置**（`.mcp.json`） - 仅在该目录中可用
2. **全局配置**（`~/.claude.json`） - 在所有项目中可用
3. **检入的 `.mcp.json`** - 整个团队可用（推荐！）

**提示**：将 `.mcp.json` 检入 git，这样整个团队都能获得相同的 MCP 服务器。

**调试**：使用 `claude --mcp-debug` 识别配置问题。

## 文档与知识

### context7
**最适用于**：使用流行库/SDK 的项目，希望 Claude 使用最新的文档进行编码

| 推荐时机 | 示例 |
|----------------|----------|
| 使用 React、Vue、Angular | 前端框架 |
| 使用 Express、FastAPI、Django | 后端框架 |
| 使用 Prisma、Drizzle | ORM |
| 使用 Stripe、Twilio、SendGrid | 第三方 API |
| 使用 AWS SDK、Google Cloud | 云 SDK |
| 使用 LangChain、OpenAI SDK | AI/ML 库 |

**价值**：Claude 获取实时文档，而不是依赖训练数据，减少幻觉 API 和过时的模式。

---

## 浏览器与前端

### Playwright MCP
**最适用于**：需要浏览器自动化、测试或截图的前端项目

| 推荐时机 | 示例 |
|----------------|----------|
| React/Vue/Angular 应用 | UI 组件测试 |
| 需要 E2E 测试 | 用户流程验证 |
| 视觉回归测试 | 截图比较 |
| 调试 UI 问题 | 看到用户看到的内容 |
| 表单测试 | 多步骤工作流 |

**价值**：Claude 可以与您运行的应用程序交互、截图、填写表单并验证 UI 行为。

### Puppeteer MCP
**最适用于**：无头浏览器自动化、网页抓取

| 推荐时机 | 示例 |
|----------------|----------|
| 从 HTML 生成 PDF | 报告生成 |
| 网页抓取任务 | 数据提取 |
| 无头测试 | CI 环境 |

---

## 数据库

### Supabase MCP
**最适用于**：使用 Supabase 进行后端/数据库的项目

| 推荐时机 | 示例 |
|----------------|----------|
| 检测到 Supabase 项目 | deps 中的 `@supabase/supabase-js` |
| 认证 + 数据库需求 | 用户管理应用 |
| 实时功能 | 实时数据同步 |

**价值**：Claude 可以直接查询表、管理认证并与 Supabase 存储交互。

### PostgreSQL MCP
**最适用于**：直接 PostgreSQL 数据库访问

| 推荐时机 | 示例 |
|----------------|----------|
| 使用原始 PostgreSQL | 无 ORM 层 |
| 数据库迁移 | 架构管理 |
| 数据分析任务 | 复杂查询 |
| 调试数据问题 | 检查实际数据 |

### Neon MCP
**最适用于**：Neon 无服务器 Postgres 用户

### Turso MCP
**最适用于**：Turso/libSQL 边缘数据库用户

---

## 版本控制与 DevOps

### GitHub MCP
**最适用于**：需要问题/PR 集成的 GitHub 托管仓库

| 推荐时机 | 示例 |
|----------------|----------|
| GitHub 仓库 | 带有 GitHub 远程的 `.git` |
| 问题驱动开发 | 在提交中引用问题 |
| PR 工作流 | 审查、合并操作 |
| GitHub Actions | CI/CD 流水线访问 |
| 发布管理 | 标签和发布自动化 |

**价值**：Claude 可以创建问题、审查 PR、检查工作流运行和管理发布。

### GitLab MCP
**最适用于**：GitLab 托管的仓库

### Linear MCP
**最适用于**：使用 Linear 进行问题跟踪的团队

| 推荐时机 | 示例 |
|----------------|----------|
| Linear 工作区 | 像 `ABC-123` 这样的问题引用 |
| Sprint 规划 | 待办事项管理 |
| 从代码创建问题 | 为 TODO 自动创建问题 |

---

## 云基础设施

### AWS MCP
**最适用于**：AWS 基础设施管理

| 推荐时机 | 示例 |
|----------------|----------|
| 依赖项中的 AWS SDK | `@aws-sdk/*` 包 |
| 基础设施即代码 | Terraform、CDK、SAM |
| Lambda 开发 | 无服务器函数 |
| S3、DynamoDB 使用 | 云数据服务 |

### Cloudflare MCP
**最适用于**：Cloudflare Workers、Pages、R2、D1

| 推荐时机 | 示例 |
|----------------|----------|
| Cloudflare Workers | 边缘函数 |
| Pages 部署 | 静态站点托管 |
| R2 存储 | 对象存储 |
| D1 数据库 | 边缘 SQL 数据库 |

### Vercel MCP
**最适用于**：Vercel 部署和配置

---

## 监控与可观测性

### Sentry MCP
**最适用于**：错误跟踪和调试

| 推荐时机 | 示例 |
|----------------|----------|
| 配置了 Sentry | deps 中的 `@sentry/*` |
| 生产调试 | 调查错误 |
| 错误模式 | 对类似问题进行分组 |
| 发布跟踪 | 将部署与错误关联 |

**价值**：Claude 可以调查 Sentry 问题、找到根本原因并建议修复。

### Datadog MCP
**最适用于**：APM、日志和指标

---

## 通信

### Slack MCP
**最适用于**：Slack 工作区集成

| 推荐时机 | 示例 |
|----------------|----------|
| 团队使用 Slack | 发送通知 |
| 部署通知 | 警报频道 |
| 事件响应 | 发布更新 |

### Notion MCP
**最适用于**：用于文档的 Notion 工作区

| 推荐时机 | 示例 |
|----------------|----------|
| 使用 Notion 编写文档 | 读取/更新页面 |
| 知识库 | 搜索文档 |
| 会议笔记 | 创建摘要 |

---

## 文件与数据

### Filesystem MCP
**最适用于**：超越内置工具的增强文件操作

| 推荐时机 | 示例 |
|----------------|----------|
| 复杂文件操作 | 批处理 |
| 文件监视 | 监控更改 |
| 高级搜索 | 自定义模式 |

### Memory MCP
**最适用于**：跨会话的持久记忆

| 推荐时机 | 示例 |
|----------------|----------|
| 长期运行的项目 | 记住上下文 |
| 用户偏好 | 存储设置 |
| 学习模式 | 构建知识 |

**价值**：Claude 记住跨对话的项目上下文、决策和模式。

---

## 容器与 DevOps

### Docker MCP
**最适用于**：容器管理

| 推荐时机 | 示例 |
|----------------|----------|
| Docker Compose 文件 | 容器编排 |
| 存在 Dockerfile | 构建镜像 |
| 容器调试 | 检查日志、执行 |

### Kubernetes MCP
**最适用于**：Kubernetes 集群管理

| 推荐时机 | 示例 |
|----------------|----------|
| K8s 清单 | 部署、扩缩 Pod |
| Helm 图表 | 包管理 |
| 集群调试 | Pod 日志、状态 |

---

## AI 与 ML

### Exa MCP
**最适用于**：网络搜索和研究

| 推荐时机 | 示例 |
|----------------|----------|
| 研究任务 | 查找最新信息 |
| 竞争分析 | 市场研究 |
| 文档缺口 | 查找示例 |

---

## 快速参考：检测模式

| 查找内容 | 建议 MCP 服务器 |
|----------|-------------------|
| 流行的 npm 包 | context7 |
| React/Vue/Next.js | Playwright MCP |
| `@supabase/supabase-js` | Supabase MCP |
| `pg` 或 `postgres` | PostgreSQL MCP |
| GitHub 远程 | GitHub MCP |
| `.linear` 或 Linear 引用 | Linear MCP |
| `@aws-sdk/*` | AWS MCP |
| `@sentry/*` | Sentry MCP |
| `docker-compose.yml` | Docker MCP |
| Slack Webhook URL | Slack MCP |
| `@anthropic-ai/sdk` | context7 用于 Anthropic 文档 |
