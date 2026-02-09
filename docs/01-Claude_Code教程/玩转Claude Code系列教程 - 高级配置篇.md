# ⚙️ 玩转 Claude Code 系列教程 — 高级配置篇

> **一句话概括**：本篇深入讲解 CLAUDE.md 记忆系统、权限管理、设置层级和内存管理，让 Claude Code 完全按照你的方式工作。

---

## 一、总述

Claude Code 的强大之处不仅在于它的 AI 能力，更在于其 **高度可定制** 的配置系统。本篇将教你：

- 如何编写高效的 CLAUDE.md 文件
- 如何管理 Claude 的记忆系统
- 如何配置权限和安全策略
- 如何理解设置的层级和优先级

掌握这些配置后，Claude Code 将成为真正 **懂你** 的编程伙伴。

---

## 二、CLAUDE.md — Claude 的"记忆文件"

### 什么是 CLAUDE.md？

CLAUDE.md 是一个特殊的 Markdown 文件，Claude 会在 **每次对话开始时** 自动读取它。你可以在其中写入：

- Bash 命令
- 代码风格规范
- 工作流规则
- 项目特定的约定

这些是 Claude **无法从代码本身推断** 的持久化上下文。

### 快速创建 CLAUDE.md

```bash
# 使用 /init 命令自动生成
claude
> /init
```

`/init` 会分析你的代码库，检测构建系统、测试框架和代码模式，生成一个良好的起点。

### CLAUDE.md 示例

```markdown
# 代码风格
- 使用 ES modules (import/export) 语法，不用 CommonJS (require)
- 尽可能使用解构导入 (如 import { foo } from 'bar')
- 变量命名使用 camelCase，组件命名使用 PascalCase

# 工作流
- 完成一系列代码更改后务必进行类型检查
- 优先运行单个测试而非整个测试套件，以提高性能
- 提交前运行 `npm run lint` 检查

# 项目特定
- 数据库迁移使用 `npx prisma migrate dev`
- 开发服务器启动命令：`npm run dev`
- 测试命令：`npm run test -- --watch`
```

### CLAUDE.md 的放置位置

| 位置 | 作用范围 | 是否共享 |
|------|---------|---------|
| `~/.claude/CLAUDE.md` | 所有项目的全局设置 | 仅个人 |
| `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 当前项目（团队共享） | 通过 Git 共享 |
| `./CLAUDE.local.md` | 当前项目（个人偏好） | 仅个人（自动 gitignore） |
| 父目录的 `CLAUDE.md` | 适用于 monorepo | 取决于位置 |
| 子目录的 `CLAUDE.md` | 按需加载 | 取决于位置 |

### CLAUDE.md 编写原则

#### ✅ 应该包含的内容

| 内容类型 | 示例 |
|---------|------|
| Claude 猜不到的 Bash 命令 | `测试命令：npm run test:unit` |
| 与默认不同的代码风格规则 | `使用 2 空格缩进` |
| 测试指令和首选测试运行器 | `优先使用 vitest 而非 jest` |
| 仓库规范（分支命名、PR 约定） | `分支命名：feature/xxx` |
| 项目特定的架构决策 | `所有 API 使用 REST，不用 GraphQL` |
| 开发环境特殊配置 | `需要设置 DATABASE_URL 环境变量` |

#### ❌ 不应该包含的内容

| 内容类型 | 原因 |
|---------|------|
| Claude 通过读代码就能知道的信息 | 浪费上下文 |
| 标准语言约定 | Claude 已经知道 |
| 详细的 API 文档 | 改为链接到文档 |
| 经常变化的信息 | 维护成本高 |
| 逐文件的代码库描述 | 太冗长 |
| "写干净的代码"之类的废话 | 不言自明 |

### CLAUDE.md 导入语法

CLAUDE.md 支持使用 `@path/to/import` 语法导入其他文件：

```markdown
参见 @README.md 了解项目概览，@package.json 了解可用的 npm 命令。

# 额外指令
- Git 工作流：@docs/git-instructions.md
- 个人覆盖：@~/.claude/my-project-instructions.md
```

---

## 三、自动记忆（Auto Memory）

### 什么是自动记忆？

自动记忆是 Claude 在工作过程中 **自动保存** 的笔记目录。与你编写的 CLAUDE.md 不同，自动记忆是 Claude 根据发现的内容为自己写的笔记��

### Claude 会记住什么？

- **项目模式**：构建命令、测试约定、代码风格偏好
- **调试洞察**：棘手问题的解决方案、常见错误原因
- **架构笔记**：关键文件、模块关系、重要抽象
- **你的偏好**：沟通风格、工作流习惯、工具选择

### 存储位置

每个项目有自己的记忆目录：

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 简洁索引，每次会话加载
├── debugging.md       # 调试模式的详细笔记
├── api-conventions.md # API 设计决策
└── ...                # Claude 创建的其他主题文件
```

### 管理自动记忆

```bash
# 在会话中打开记忆文件选择器
> /memory

# 让 Claude 记住特定内容
> 记住我们使用 pnpm 而不是 npm
> 保存到记忆：API 测试需要本地 Redis 实例
```

### 启用/禁用自动记忆

```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # 强制开启
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # 强制关闭
```

---

## 四、模块化规则（.claude/rules/）

对于大型项目，可以将指令组织到多个文件中：

### 基本结构

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主项目指令
│   └── rules/
│       ├── code-style.md   # 代码风格指南
│       ├── testing.md      # 测试约定
│       └── security.md     # 安全要求
```

### 路径特定规则

规则可以使用 YAML frontmatter 限定到特定文件：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则
- 所有 API 端点必须包含输入验证
- 使用标准错误响应格式
- 包含 OpenAPI 文档注释
```

### Glob 模式参考

| 模式 | 匹配 |
|------|------|
| `**/*.ts` | 任何目录中的所有 TypeScript 文件 |
| `src/**/*` | src/ 目录下的所有文件 |
| `*.md` | 项目根目录的 Markdown 文件 |
| `src/**/*.{ts,tsx}` | 同时匹配 .ts 和 .tsx 文件 |

---

## 五、权限管理

### 权限层级

| 工具类型 | 示例 | 需要批准？ |
|---------|------|-----------|
| 只读工具 | 文件读取、Grep | 否 |
| Bash 命令 | Shell 执行 | 是 |
| 文件修改 | 编辑/写入文件 | 是 |

### 权限模式

| 模式 | 说明 |
|------|------|
| `default` | 标准行为：首次使用每个工具时提示 |
| `acceptEdits` | 自动接受文件编辑，命令仍需确认 |
| `plan` | 计划模式：只读分析，不修改文件 |
| `delegate` | 委托模式：仅通过团队成员协调工作 |
| `dontAsk` | 除非预先批准，否则自动拒绝 |
| `bypassPermissions` | 跳过所有权限提示（仅限安全环境） |

### 权限规则语法

在 `.claude/settings.json` 中配置：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(curl *)",
      "Read(./.env)"
    ]
  }
}
```

### 通配符规则

- `Bash(npm run *)` — 匹配所有以 `npm run` 开头的命令
- `Bash(* --version)` — 匹配所有以 `--version` 结尾的命令
- `Read(src/**)` — 递归匹配 src/ 下所有文件
- `WebFetch(domain:example.com)` — 匹配特定域名的请求

---

## 六、设置层级与优先级

Claude Code 使用分层设置系统（从高到低优先级）：

```
1. 托管策略（Managed）     — IT/DevOps 部署的系统级策略
   ↓
2. 命令行参数              — 临时会话覆盖
   ↓
3. 本地设置（Local）       — 个人项目特定设置
   ↓
4. 项目设置（Project）     — 团队共享设置
   ↓
5. 用户设置（User）        — 个人全局设置
```

### 关键配置文件

| 文件位置 | 用途 | 是否共享 |
|---------|------|---------|
| `~/.claude/settings.json` | 所有项目的用户偏好 | 否 |
| `.claude/settings.json` | 团队共享的项目设置 | 是（Git） |
| `.claude/settings.local.json` | 个人项目覆盖 | 否（gitignore） |
| `~/.claude.json` | 偏好、OAuth、MCP 服务器 | 否 |
| `.mcp.json` | 项目范围的 MCP 服务器 | 是（Git） |

---

## 七、扩展思考（Extended Thinking）

扩展思考默认开启，让 Claude 在回复前有空间逐步推理复杂问题。

### 配置方式

| 范围 | 方法 | 说明 |
|------|------|------|
| 努力级别 | `/model` 或 `CLAUDE_CODE_EFFORT_LEVEL` | low/medium/high（默认） |
| 切换快捷键 | `Option+T`（Mac）/ `Alt+T`（Win/Linux） | 当前会话开关 |
| 全局默认 | `/config` | 所有项目的默认设置 |
| 限制 Token 预算 | `MAX_THINKING_TOKENS` 环境变量 | 限制思考 Token 数量 |

### 查看思考过程

按 `Ctrl+O` 切换详细模式，可以看到灰色斜体的内部推理文本。

---

## 八、总结

本篇深入讲解了 Claude Code 的高级配置系统：

| 配置领域 | 核心要点 |
|---------|---------|
| **CLAUDE.md** | 项目级持久化指令，保持简洁、具体 |
| **自动记忆** | Claude 自动保存的项目洞察和模式 |
| **模块化规则** | `.claude/rules/` 目录下的分主题规则文件 |
| **权限管理** | 分层权限系统，支持通配符和精细控制 |
| **设置层级** | 5 级优先级，从托管策略到用户设置 |
| **扩展思考** | 可调节的推理深度，适应不同复杂度任务 |

**核心原则**：把 CLAUDE.md 当代码一样维护——定期审查、精简内容、测试效果。

接��来请阅读 **[MCP 与扩展篇]** 学习如何让 Claude Code 连接外部工具和服务！

---

> 📚 **参考资料**：[内存管理](https://code.claude.com/docs/en/memory) | [设置](https://code.claude.com/docs/en/settings) | [权限](https://code.claude.com/docs/en/permissions)
