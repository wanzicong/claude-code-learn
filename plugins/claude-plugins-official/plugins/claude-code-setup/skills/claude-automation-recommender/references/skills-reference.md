# Skills 推荐

Skills 是带有工作流、参考资料和最佳实践的封装专业知识。在 `.claude/skills/<name>/SKILL.md` 中创建它们。Skills 可以在相关时由 Claude 自动调用，或者由用户直接使用 `/skill-name` 调用。

某些预构建的技能可通过官方插件获得（通过 `/plugin install` 安装）。

**注意**：这些是常见模式。使用网络搜索找到针对代码库工具和框架的具体技能思路。

---

## 可从官方插件获得

### 插件开发 (plugin-dev)

| 技能 | 最适用于 |
|-------|----------|
| **skill-development** | 使用正确结构创建新技能 |
| **hook-development** | 构建自动化 hooks |
| **command-development** | 创建斜杠命令 |
| **agent-development** | 构建专门的 subagents |
| **mcp-integration** | 将 MCP 服务器集成到插件中 |
| **plugin-structure** | 理解插件架构 |

### Git 工作流 (commit-commands)

| 技能 | 最适用于 |
|-------|----------|
| **commit** | 使用适当的消息创建 git 提交 |
| **commit-push-pr** | 完整的提交、推送和 PR 工作流 |

### 前端 (frontend-design)

| 技能 | 最适用于 |
|-------|----------|
| **frontend-design** | 创建精美的 UI 组件 |

**价值**：创建独特、高质量的 UI，而不是通用的 AI 美学。

### 自动化规则 (hookify)

| 技能 | 最适用于 |
|-------|----------|
| **writing-rules** | 创建 hookify 自动化规则 |

### 功能开发 (feature-dev)

| 技能 | 最适用于 |
|-------|----------|
| **feature-dev** | 端到端功能开发工作流 |

---

## 快速参考：官方插件技能

| 代码库信号 | 技能 | 插件 |
|-----------------|-------|--------|
| 构建插件 | skill-development | plugin-dev |
| Git 提交 | commit | commit-commands |
| React/Vue/Angular | frontend-design | frontend-design |
| 自动化规则 | writing-rules | hookify |
| 功能规划 | feature-dev | feature-dev |

---

## 自定义项目技能

在 `.claude/skills/<name>/SKILL.md` 中创建项目特定的技能。

### 技能结构

```
.claude/skills/
└── my-skill/
    ├── SKILL.md           # 主要指令（必需）
    ├── template.yaml      # 要应用的模板
    ├── scripts/
    │   └── validate.sh    # 要运行的脚本
    └── examples/          # 参考示例
```

### Frontmatter 参考

```yaml
---
name: skill-name
description: 此技能的功能以及何时使用它
disable-model-invocation: true  # 仅用户可以调用（用于副作用）
user-invocable: false           # 仅 Claude 可以调用（用于背景知识）
allowed-tools: Read, Grep, Glob # 限制工具访问
context: fork                   # 在隔离的子代理中运行
agent: Explore                  # fork 时使用的代理类型
---
```

### 调用控制

| 设置 | 用户 | Claude | 用于 |
|---------|------|--------|---------|
| （默认） | ✓✓ | ✓✓ | 通用技能 |
| `disable-model-invocation: true` | ✓✓ | ✗ | 副作用（部署、发送） |
| `user-invocable: false` | ✗ | ✓✓ | 背景知识 |

---

## 自定义技能示例

### 带有 OpenAPI 模板的 API 文档

应用 YAML 模板以生成一致的 API 文档：

```
.claude/skills/api-doc/
├── SKILL.md
└── openapi-template.yaml
```

**SKILL.md:**
```yaml
---
name: api-doc
description: 为端点生成 OpenAPI 文档。记录 API 路由时使用。
---

为 $ARGUMENTS 处的端点生成 OpenAPI 文档。

使用 [openapi-template.yaml](openapi-template.yaml) 中的模板作为结构。

1. 读取端点代码
2. 提取路径、方法、参数、请求/响应架构
3. 用实际值填写模板
4. 输出完成的 YAML
```

**openapi-template.yaml:**
```yaml
paths:
  /{path}:
    {method}:
      summary: ""
      description: ""
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
      responses:
        "200":
          description: ""
          content:
            application/json:
              schema: {}
```

---

### 带有脚本的数据库迁移生成器

使用捆绑的脚本生成并验证迁移：

```
.claude/skills/create-migration/
├── SKILL.md
└── scripts/
    └── validate-migration.sh
```

**SKILL.md:**
```yaml
---
name: create-migration
description: 创建数据库迁移文件
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

创建迁移：$ARGUMENTS

1. 在 `migrations/` 中生成带有时间戳前缀的迁移文件
2. 包含 up 和 down 函数
3. 运行验证：`bash ~/.claude/skills/create-migration/scripts/validate-migration.sh`
4. 报告发现的任何问题
```

**scripts/validate-migration.sh:**
```bash
#!/bin/bash
# 验证迁移语法
npx prisma validate 2>&1 || echo "验证失败"
```

---

### 带有示例的测试生成器

遵循项目模式生成测试：

```
.claude/skills/gen-test/
├── SKILL.md
└── examples/
    ├── unit-test.ts
    └── integration-test.ts
```

**SKILL.md:**
```yaml
---
name: gen-test
description: 为文件生成遵循项目约定的测试
disable-model-invocation: true
---

为以下内容生成测试：$ARGUMENTS

参考这些示例以了解预期模式：
- 单元测试：[examples/unit-test.ts](examples/unit-test.ts)
- 集成测试：[examples/integration-test.ts](examples/integration-test.ts)

1. 分析源文件
2. 识别要测试的函数/方法
3. 生成匹配项目约定的测试
4. 放在适当的测试目录中
```

---

### 带有模板的组件生成器

从模板搭建新组件：

```
.claude/skills/new-component/
├── SKILL.md
└── templates/
    ├── component.tsx.template
    ├── component.test.tsx.template
    └── component.stories.tsx.template
```

**SKILL.md:**
```yaml
---
name: new-component
description: 搭建带有测试和 stories 的新 React 组件
disable-model-invocation: true
---

创建组件：$ARGUMENTS

使用 [templates/](templates/) 目录中的模板：
1. 从 component.tsx.template 生成组件
2. 从 component.test.tsx.template 生成测试
3. 从 component.stories.tsx.template 生成 Storybook story

将 {{ComponentName}} 替换为 PascalCase 名称。
将 {{component-name}} 替换为 kebab-case 名称。
```

---

### 带有检查清单的 PR 审查

根据项目特定检查清单审查 PR：

```
.claude/skills/pr-check/
├── SKILL.md
└── checklist.md
```

**SKILL.md:**
```yaml
---
name: pr-check
description: 根据项目检查清单审查 PR
disable-model-invocation: true
context: fork
---

## PR 上下文
- 差异：!`gh pr diff`
- 描述：!`gh pr view`

根据 [checklist.md](checklist.md) 进行审查。

对于每个项目，用解释标记 ✅ 或 ❌。
```

**checklist.md:**
```markdown
## PR 检查清单

- [ ] 为新功能添加了测试
- [ ] 没有 console.log 语句
- [ ] 错误处理包含面向用户的消息
- [ ] API 更改向后兼容
- [ ] 数据库迁移可逆
```

---

### 发布说明生成器

从 git 历史生成发布说明：

**SKILL.md:**
```yaml
---
name: release-notes
descriptiondescription: 从自上次标记以来的提交生成发布说明
disable-model-invocation: true
---

## 最近更改
- 自上次标记以来的提交：!`git log $(git describe --tags -- --abbrev=0)..HEAD --oneline`
- 上次标记：!`git describe --tags --abbrev=0`

生成发布说明：
1. 按类型分组提交（feat、fix、docs 等）
2. 编写用户友好的描述
3. 突出显示破坏性更改
4. 格式化为 markdown
```

---

### 项目约定（仅 Claude）

Claude 自动应用的背景知识：

**SKILL.md:**
```yaml
---
name: project-conventions
description: 此项目的代码风格和模式。编写或审查代码时应用。
user-invocable: false
---

## 命名约定
- React 组件：PascalCase
- 工具：camelCase
- 常量：UPPER_SNAKE_CASE
- 文件：kebab-case

## 模式
- 使用 `Result<T, E>` 进行可能失败的操作，而不是异常
- 优先使用组合而不是继承
- 所有 API 响应使用 `{ data, error, meta }` 形状

## 禁止事项
- 没有 `any` 类型
- 生产代码中没有 `console.log`
- 没有同步文件 I/O
```

---

### 环境设置

使用设置脚本为新开发者入职设置：

```
.claude/skills/setup-dev/
├── SKILL.md
└── scripts/
    └── check-prerequisites.sh
```

**SKILL.md:**
```yaml
---
name: setup-dev
description: 为新贡献者设置开发环境
disable-model-invocation: true
---

设置开发环境：

1. 检查先决条件：`bash scripts/check-prerequisites.sh`
2. 安装依赖项：`npm install`
3. 复制环境模板：`cp .env.example .env`
4. 设置数据库：`npm run db:setup`
5. 验证设置：`npm test`

报告遇到的任何问题。
```

---

## 参数模式

| 模式 | 含义 | 示例 |
|---------|---------|---------|
| `$ARGUMENTS` | 所有参数作为字符串 | `/deploy staging` → "staging" |

如果技能中没有 `$ARGUMENTS`，参数将作为 `ARGUMENTS: <value>` 附加。

## 动态上下文注入

使用 `!`command`` 在技能运行之前注入实时数据：

```yaml
## 当前状态
- 分支：!`git branch --show-current`
- 状态：!`git status --short`
```

命令输出在 Claude 看到技能内容之前替换占位符。
