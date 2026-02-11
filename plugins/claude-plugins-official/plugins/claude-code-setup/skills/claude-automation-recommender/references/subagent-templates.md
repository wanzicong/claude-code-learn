# Subagent 推荐

Subagents 是并行运行的专门 Claude 实例，每个都有自己的上下文窗口和工具访问权限。它们非常适合专注的审查、分析或生成任务。

**注意**：这些是常见模式。基于代码库的特定审查和分析需求设计自定义 subagents。

## 代码审查代理

### code-reviewer
**最适用于**：大型代码库的自动化代码质量检查

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 大型代码库（>500 个文件） | 文件计数 |
| 频繁的代码更改 | 活跃开发 |
| 团队想要一致的审查 | 质量重点 |

**价值**：在您继续工作时并行运行代码审查
**模型**：sonnet（平衡质量/速度）
**工具**：Read、Grep、Glob、Bash

---

### security-reviewer
**最适用于**：专注于安全的代码审查

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 存在认证代码 | `auth/`、`login`、`session` 模式 |
| 支付处理 | `stripe`、`payment`、`billing` 模式 |
| 用户数据处理 | `user`、`profile`、`pii` 模式 |
| 代码中的 API 密钥 | 环境变量模式 |

**价值**：捕获 OWASP 漏洞、认证问题、数据泄露
**模型**：sonnet
**工具**：Read、Grep、Glob（为了安全只读）

---

### test-writer
**最适用于**：生成全面的测试覆盖率

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 测试覆盖率低 | 测试文件与源文件数量相比很少 |
| 存在测试套件 | 存在 `tests/`、`__tests__/` |
| 配置了测试框架 | deps 中有 jest、pytest、vitest |

**价值**：生成匹配项目约定的测试
**模型**：sonnet
**工具**：Read、Write、Grep、Glob

---

## 专门代理

### api-documenter
**最适用于**：API 文档生成

| 推荐时机 | 检测方式 |
|----------------|-----------|
| REST 端点 | Express 路由、FastAPI 路径 |
| GraphQL 架构 | `.graphql` 文件 |
| 存在 OpenAPI | `openapi.yaml`、`swagger.json` |
| 未记录的 API | 没有文档的路由 |

**价值**：生成 OpenAPI 规范、端点文档
**模型**：sonnet
**工具**：Read、Write、Grep、Glob

---

### performance-analyzer
**最适用于**：查找性能瓶颈

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 数据库查询 | ORM 使用、原始 SQL |
| 高流量代码 | API 端点、热路径 |
| 性能投诉 | 用户报告缓慢 |
| 复杂算法 | 嵌套循环、递归 |

**价值**：查找 N+1 查询、O(n²) 算法、内存泄漏
**模型**：sonnet
**工具**：Read、Grep、Glob、Bash

---

### ui-reviewer
**最适用于**：前端可访问性和 UX 审查

| 推荐时机 | 检测方式 |
|----------------|-----------|
| React/Vue/Angular | 检测到前端框架 |
| 组件库 | `components/` 目录 |
| 面向用户的 UI | 不仅仅是 API 项目 |

**价值**：捕获可访问性问题、UX 问题、响应式设计差距
**模型**：sonnet
**工具**：Read、Grep、Glob

---

## 实用代理

### dependency-updater
**最适用于**：安全的依赖项更新

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 过时的依赖项 | `npm outdated` 有结果 |
| 安全公告 | `npm audit` 警告 |
| 主版本落后 | 重大版本差距 |

**价值**：增量更新依赖项并进行测试
**模型**：sonnet
**工具**：Read、Write、Bash、Grep

---

### migration-helper
**最适用于**：框架/版本迁移

| 推荐时机 | 检测方式 |
|----------------|-----------|
| 需要主要升级 | 框架版本非常旧 |
| 即将出现破坏性更改 | 弃用警告 |
| 计划重构 | 架构更改 |

**价值**：增量规划和执行迁移
**模型**：opus（需要复杂推理）
**工具**：Read、Write、Grep、Glob、Bash

---

## 快速参考：检测 → 推荐

| 如果看到 | 推荐 Subagent |
|------------|-------------------|
| 大型代码库 | code-reviewer |
| 认证/支付代码 | security-reviewer |
| 测试很少 | test-writer |
| API 路由 | api-documenter |
| 数据库密集 | performance-analyzer |
| 前端组件 | ui-reviewer |
| 过时的包 | dependency-updater |
| 旧框架版本 | migration-helper |

---

## Subagent 位置

Subagents 放在 `.claude/agents/` 中：

```
.claude/
└── agents/
    ├── code-reviewer.md
    ├── security-reviewer.md
    └── test-writer.md
```

---

## 模型选择指南

| 模型 | 最适用于 | 权衡 |
|-------|----------|-----------|
| **haiku** | 简单、重复的检查 | 快速、便宜、不太彻底 |
| **sonnet** | 大多数审查/分析任务 | 平衡（推荐默认） |
| |opus** | 复杂迁移、架构 | 彻底、较慢、更昂贵 |

---

## 工具访问指南

| 访问级别 | 工具 | 用例 |
|--------------|-------|----------|
| 只读 | Read、Grep、Glob | 审查、分析 |
| 写入 | + Write | 代码生成、文档 |
| 完全 | + Bash | 迁移、测试 |
