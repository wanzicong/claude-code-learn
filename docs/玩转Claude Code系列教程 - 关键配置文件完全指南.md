# 📁 玩转 Claude Code 系列教程 — 关键配置文件完全指南

> **一句话概括**：本篇全面介绍 Claude Code 安装后的所有关键文件和目录结构，帮你深入理解每个配置文件的作用、格式和最佳实践。

---

## 一、总述

Claude Code 的强大之处在于其 **高度可配置** 的设计。安装后，会在多个位置创建配置文件和目录，理解这些文件的结构和作用，是掌握 Claude Code 的关键。

### 配置文件全景图

```
系统级
├── macOS:     /Library/Application Support/ClaudeCode/
├── Linux/WSL: /etc/claude-code/
└── Windows:   C:\Program Files\ClaudeCode\
           (managed-settings.json) ← IT 部署的策略

用户级
├── ~/.claude/                    # 主配置目录
│   ├── settings.json             # 全局设置
│   ├── CLAUDE.md                 # 全局记忆文件
│   ├── skills/                   # 个人技能目录
│   │   └── <skill-name>/SKILL.md
│   ├── agents/                   # 子代理配置
│   │   └── <agent-name>.md
│   └── projects/                 # 项目记忆和会话
│       └── <project>/
│           ├── memory/
│           └── sessions/
│
├── ~/.claude.json                # 主配置文件
│                                 # (主题、OAuth、MCP 服务器)
│
项目级
└── your-project/
    ├── .claude/                  # 项目配置目录
    │   ├── settings.json         # 项目设置
    │   ├── settings.local.json   # 本地覆盖(不提交)
    │   ├── CLAUDE.md             # 项目记忆文件
    │   ├── CLAUDE.local.md       # 本地覆盖(不提交)
    │   ├── skills/               # 项目技能
    │   ├── agents/               # 项目子代理
    │   └── rules/                # 模块化规则
    │       ├── code-style.md
    │       └── testing.md
    │
    └── .mcp.json                 # 项目 MCP 服务器
```

---

## 二、用户级配置目录 `~/.claude/`

### 目录结构

```
~/.claude/
├── settings.json              # 全局设置（权限、环境变量等）
├── CLAUDE.md                  # 全局记忆文件
├── skills/                    # 个人技能（所有项目共享）
│   └── <skill-name>/
│       └── SKILL.md
├── agents/                    # 子代理配置
│   └── <agent-name>.md
└── projects/                  # 项目记忆和会话存储
    └── <project-hash>/
        ├── memory/            # 自动记忆
        │   ├── MEMORY.md
        │   ├── debugging.md
        │   └── api-conventions.md
        └── sessions/          # 会话历史
            └── <session-id>/
```

### settings.json — 全局设置文件

**位置**：`~/.claude/settings.json`

**作用**：控制 Claude Code 的全局行为，包括权限、环境变量、模型选择等。

**完整示例**：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm run test *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git commit *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(curl *)",
      "Bash(rm *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "WebFetch(domain:internal-api.com)"
    ],
    "ask": [
      "Bash(git push origin main)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "40000",
    "DISABLE_COST_WARNINGS": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "sudo"],
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "api.github.com"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  },
  "attribution": {
    "commit": {
      "prefix": "🤖 Generated with",
      "suffix": "Co-Authored-By: Claude <noreply@anthropic.com>"
    },
    "pr": {
      "prefix": "[Claude Code]"
    }
  },
  "outputStyle": "Explanatory",
  "language": "chinese",
  "alwaysThinkingEnabled": true,
  "maxThinkingTokens": 200000,
  "hooks": {
    "tool.after:Edit": "npm run lint -- --fix"
  }
}
```

**配置项详解**：

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 默认模型名称 |
| `permissions` | object | 权限规则（allow/deny/ask） |
| `env` | object | 环境变量 |
| `sandbox` | object | 沙箱配置 |
| `attribution` | object | Git 提交/PR 署名 |
| `outputStyle` | string | 输出风格（Concise/Explanatory） |
| `language` | string | 响应语言 |
| `alwaysThinkingEnabled` | boolean | 启用扩展思考 |
| `maxThinkingTokens` | number | 最大思考 Token 数 |
| `hooks` | object | 生命周期钩子 |

---

## 三、主配置文件 `~/.claude.json`

**位置**：`~/.claude.json`

**作用**：存储用户偏好、OAuth 令牌、MCP 服务器配置和缓存。

**典型结构**：

```json
{
  "preferences": {
    "theme": "dark",
    "fontSize": 14,
    "fontFamily": "JetBrains Mono"
  },
  "oauth": {
    "accessToken": "...",
    "refreshToken": "...",
    "expiresAt": "2025-01-01T00:00:00Z"
  },
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "scope": "user"
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub"],
      "env": {
        "DSN": "postgresql://..."
      },
      "scope": "local"
    }
  }
}
```

---

## 四、项目级配置目录 `.claude/`

### 目录结构

```
your-project/
├── .claude/
│   ├── settings.json           # 项目设置（提交到 Git）
│   ├── settings.local.json     # 本地覆盖（不提交）
│   ├── CLAUDE.md               # 项目记忆（提交到 Git）
│   ├── CLAUDE.local.md         # 本地覆盖（不提交）
│   ├── skills/                 # 项目技能
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   ├── agents/                 # 项目子代理
│   │   └── <agent-name>.md
│   └── rules/                  # 模块化规则
│       ├── code-style.md
│       ├── testing.md
│       └── security.md
│
└── .mcp.json                   # 项目 MCP 服务器
```

### settings.json vs settings.local.json

| 文件 | 提交到 Git | 用途 |
|------|-----------|------|
| `.claude/settings.json` | ✅ 是 | 团队共享的项目设置 |
| `.claude/settings.local.json` | ❌ 否（自动 gitignore） | 个人偏好覆盖 |

**settings.json 示例**（团队共享）：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test)",
      "Bash(npm run lint)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

**settings.local.json 示例**（个人）：

```json
{
  "model": "claude-opus-4-20250514",
  "outputStyle": "Concise"
}
```

---

## 五、CLAUDE.md — 记忆文件

### 位置与优先级

| 位置 | 作用范围 | 是否共享 |
|------|---------|---------|
| `~/.claude/CLAUDE.md` | 所有项目 | 否 |
| `CLAUDE.md` | 当前项目（根目录） | 是 |
| `.claude/CLAUDE.md` | 当前项目 | 是 |
| `CLAUDE.local.md` | 当前项目 | 否 |
| 父目录的 `CLAUDE.md` | 子目录继承 | 取决于位置 |
| 子目录的 `CLAUDE.md` | 按需加载 | 取决于位置 |

### CLAUDE.md 示例

```markdown
# 项目：电商后台管理系统

## 技术栈
- 前端：React + TypeScript + Tailwind CSS
- 后端：Node.js + Express + PostgreSQL
- ORM：Prisma
- 测试：Jest + Playwright

## 代码风格
- 使用 2 空格缩进
- 组件使用 PascalCase，函数使用 camelCase
- 优先使用函数式组件和 Hooks
- 所有 API 调用必须包含错误处理

## 开发命令
```bash
npm run dev          # 启动开发服务器
npm run build        # 生产构建
npm run test         # 运行测试
npm run lint         # 代码检查
npm run db:migrate   # 数据库迁移
npm run db:seed      # 数据库种子
```

## 工作流
1. 创建功能分支：`feature/功能名称`
2. 编写代码并测试
3. 运行 `npm run lint` 检查
4. 提交并创建 PR
5. PR 标题格式：`[功能/修复/重构] 简短描述`

## 架构约定
- 所有 API 路由在 `src/api/` 目录
- 数据模型在 `prisma/schema.prisma`
- 工具函数在 `src/utils/`
- 类型定义在 `src/types/`

## 安全要求
- 所有用户输入必须验证
- 敏感数据使用环境变量
- API 响应不暴露内部结构
```

---

## 六、Skills 技能目录

### 目录结构

```
.claude/skills/<skill-name>/
├── SKILL.md           # 必需：主技能文件
├── template.md        # 可选：模板
├── examples/          # 可选：示例
│   └── sample.md
└── scripts/           # 可选：脚本
    └── helper.py
```

### SKILL.md 示例

```yaml
---
name: deploy-staging
description: 部署应用到预发布环境
argument-hint: [commit-hash]
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(npm run *)
context: fork
agent: general-purpose
---

# 部署到预发布环境

部署指定提交到预发布环境。

## 步骤

1. **验证测试通过**
   ```bash
   npm run test
   ```

2. **构建应用**
   ```bash
   npm run build
   ```

3. **部署到预发布**
   ```bash
   git push staging $ARGUMENTS
   ```

4. **验证部署**
   ```bash
   curl https://staging.example.com/health
   ```

## 参数

- `$ARGUMENTS`：要部署的 commit hash 或 branch name
```

---

## 七、Subagents 子代理配置

### 位置

```
~/.claude/agents/<agent-name>.md      # 全局子代理
.claude/agents/<agent-name>.md        # 项目子代理
```

### 子代理配置示例

```markdown
---
name: security-reviewer
description: 审查代码中的安全漏洞
model: opus
tools: Read, Grep, Glob, Bash
---

你是一名高级安全工程师。审查代码时关注：

## 安全漏洞类型

1. **注入漏洞**
   - SQL 注入
   - XSS（跨站脚本）
   - 命令注入
   - LDAP 注入

2. **认证和授权**
   - 弱密码策略
   - 会话管理不当
   - 权限提升漏洞
   - JWT/TOKEN 处理错误

3. **敏感数据暴露**
   - 代码中的密钥或凭证
   - 不安全的数据存储
   - 日志中的敏感信息

4. **配置问题**
   - CORS 配置不当
   - 缺少安全头
   - 调试模式开启

## 输出格式

对每个问题提供：
- 🔴 严重级别（Critical/High/Medium/Low）
- 📍 具体位置（文件:行号）
- 📝 问题描述
- ✅ 修复建议
- 📚 参考链接（如适用）
```

---

## 八、MCP 服务器配置

### 配置位置

| 位置 | 作用范围 |
|------|---------|
| `~/.claude.json` | 个人（所有项目） |
| `.mcp.json` | 项目（团队共享） |

### .mcp.json 示例

```json
{
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "scope": "project"
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub"],
      "env": {
        "DSN": "postgresql://user:pass@localhost:5432/mydb"
      },
      "scope": "local"
    },
    "slack": {
      "transport": "sse",
      "url": "https://mcp.slack.com/sse",
      "headers": {
        "Authorization": "Bearer xoxp-your-token"
      },
      "scope": "user"
    }
  }
}
```

### MCP 服务器传输方式

| 传输方式 | 说明 | 适用场景 |
|---------|------|---------|
| `http` | HTTP/HTTPS 连接 | 云端服务、API |
| `sse` | Server-Sent Events | 实时数据流 |
| `stdio` | 标准输入输出 | 本地进程 |

---

## 九、Hooks 钩子配置

### 在 settings.json 中配置

```json
{
  "hooks": {
    "tool.before:Edit": [
      {
        "command": "echo 'About to edit: $TOOL_INPUT_FILE'"
      }
    ],
    "tool.after:Edit": [
      {
        "command": "npm run lint -- --fix $TOOL_INPUT_FILE",
        "runInBackground": true
      },
      {
        "command": "npx prettier --write $TOOL_INPUT_FILE"
      }
    ],
    "session.start": [
      {
        "command": "echo 'Starting new session'"
      }
    ],
    "git.after:commit": [
      {
        "command": "npm run test"
      }
    ]
  }
}
```

### 可用的钩子事件

| 事件 | 触发时机 |
|------|---------|
| `session.start` | 会话开始 |
| `tool.before:<tool>` | 工具调用前 |
| `tool.after:<tool>` | 工具调用后 |
| `git.before:commit` | Git 提交前 |
| `git.after:commit` | Git 提交后 |

---

## 十、模块化规则 `.claude/rules/`

### 目录结构

```
.claude/rules/
├── code-style.md        # 代码风格规则
├── testing.md           # 测试约定
├── security.md          # 安全要求
└── api-conventions.md   # API 设计规范
```

### 规则文件示例（带路径限定）

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则

## 请求验证
- 所有 API 端点必须包含输入验证
- 使用 zod 进行 schema 验证
- 验证失败返回 400 和清晰的错误消息

## 响应格式
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}
```

## 文档
- 所有端点包含 JSDoc 注释
- 使用 OpenAPI 规范
- 示例请求和响应

## 安全
- 敏感操作需要认证
- 实施速率限制
- 记录所有 API 调用
```

### Glob 模式参考

| 模式 | 匹配 |
|------|------|
| `**/*.ts` | 任何目录中的所有 TypeScript 文件 |
| `src/**/*` | src/ 目录下的所有文件 |
| `*.md` | 项目根目录的 Markdown 文件 |
| `src/**/*.{ts,tsx}` | 同时匹配 .ts 和 .tsx 文件 |
| `!**/*.test.ts` | 排除测试文件 |

---

## 十一、环境变量配置

### 在 settings.json 中配置

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "40000",
    "CLAUDE_CODE_EFFORT_LEVEL": "high",
    "DISABLE_COST_WARNINGS": "1",
    "NODE_ENV": "development",
    "DATABASE_URL": "postgresql://localhost:5432/mydb"
  }
}
```

### 关键环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | API 密钥 | - |
| `ANTHROPIC_MODEL` | 模型名称 | - |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | 启用遥测 | `1` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 最大输出 Token | `32000` |
| `CLAUDE_CODE_EFFORT_LEVEL` | 努力级别 | `medium` |
| `MAX_THINKING_TOKENS` | 扩展思考 Token | `200000` |
| `DISABLE_TELEMETRY` | 禁用遥测 | - |
| `DISABLE_AUTOUPDATER` | 禁用自动更新 | - |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | 技能字符预算 | 动态（2% 上下文） |

---

## 十二、配置优先级

### 设置层级（从高到低）

```
1. Managed（托管策略）
   └── 系统级管理设置（IT/DevOps 部署）
   ↓
2. 命令行参数
   └── 临时会话覆盖（claude --model xxx）
   ↓
3. Local（本地设置）
   └── .claude/settings.local.json
   ↓
4. Project（项目设置）
   └── .claude/settings.json
   ↓
5. User（用户设置）
   └── ~/.claude/settings.json
```

### 合并规则

- `allow` 规则：**并集**（所有允许的操作都被允许）
- `deny` 规则：**优先于 allow**（拒绝优先于允许）
- `env` 变量：**后者覆盖前者**
- 其他配置：**深层合并**

---

## 十三、.gitignore 建议

```gitignore
# Claude Code 本地配置
.claude/settings.local.json
.claude/CLAUDE.local.md
CLAUDE.local.md

# MCP 本地配置（如果有敏感信息）
.mcp.json.local

# 自动生成的文件
.claude/projects/
```

---

## 十四、快速参考卡片

### 常用配置文件位置

| 配置类型 | 位置 | 用途 |
|---------|------|------|
| 全局设置 | `~/.claude/settings.json` | 所有项目的默认设置 |
| 项目设置 | `.claude/settings.json` | 团队共享的项目设置 |
| 本地覆盖 | `.claude/settings.local.json` | 个人偏好 |
| 全局记忆 | `~/.claude/CLAUDE.md` | 所有项目的持久化指令 |
| 项目记忆 | `CLAUDE.md` 或 `.claude/CLAUDE.md` | 项目特定指令 |
| MCP 配置 | `~/.claude.json` 或 `.mcp.json` | MCP 服务器 |
| 主配置 | `~/.claude.json` | 主题、OAuth、缓存 |

### 配置管理命令

```bash
# 打开全局设置
> /config

# 查看当前配置
> /settings

# 管理权限
> /permissions

# 管理技能
> /skills

# 管理 MCP
> /mcp

# 管理子代理
> /agents

# 管理钩子
> /hooks

# 初始化项目
> /init

# 诊断问题
> /doctor
```

---

## 十五、总结

本篇全面介绍了 Claude Code 的关键配置文件：

| 配置领域 | 关键文件 | 核心作用 |
|---------|---------|---------|
| **设置系统** | settings.json | 权限、环境变量、模型选择 |
| **记忆系统** | CLAUDE.md | 项目指令和约定 |
| **技能系统** | skills/*/SKILL.md | 可复用工作流 |
| **子代理** | agents/*.md | 专业任务代理 |
| **MCP 集成** | .mcp.json | 外部工具连接 |
| **自动化** | hooks | 生命周期钩子 |
| **模块化规则** | rules/*.md | 按路径限定规则 |

**最佳实践**：
1. 团队共享的配置放在 `.claude/` 并提交到 Git
2. 个人偏好用 `*.local.*` 文件，自动 gitignore
3. CLAUDE.md 保持简洁，只放 Claude 猜不到的内容
4. 使用模块化规则组织大型项目的配置
5. 定期审查和更新配置文件

掌握这些配置文件后，你就能将 Claude Code 定制成完全符合你和团队需求的编程助手！

---

> 📚 **参考资料**：[设置文档](https://code.claude.com/docs/en/settings) | [权限管理](https://code.claude.com/docs/en/permissions) | [内存管理](https://code.claude.com/docs/en/memory)
