# 插件设置文件示例

## 模板: 基本配置

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
mode: standard
---

# 我的插件配置

插件在标准模式下处于激活状态。
```

## 模板: 高级配置

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
strict_mode: false
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
notification_level: info
retry_attempts: 3
timeout_seconds: 60
custom_path: "/path/to/data"
---

# 我的插件高级配置

此项目使用自定义插件配置:
- 标准验证模式
- 1MB 文件大小限制
- 允许 JavaScript/TypeScript 文件
- Info 级别日志记录
- 3 次重试尝试

## 附加说明

有关此配置的问题请联系 @team-lead。
```

## 模板: 代理状态文件

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: database-implementation
task_number: 4.2
pr_number: 5678
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.5", "Task 4.1"]
additional_instructions: "Use PostgreSQL, not MySQL"
---

# 任务分配: 数据库架构实现

为新功能模块实现数据库架构。

## 要求

- 创建迁移文件
- 添加性能索引
- 为约束编写测试
- 在 README 中记录架构

## 成功标准

- 迁移成功运行
- 所有测试通过
- 创建 PR 并且 CI 通过
- 架构已记录

## 协调

依赖于:
- 任务 3.5: API 端点定义
- 任务 4.1: 数据模型设计

向协调者会话 'team-leader' 报告状态。
```

## 模板: 功能标志模式

**.claude/experimental-features.local.md:**

```markdown
---
enabled: true
features:
  - ai_suggestions
  - auto_formatting
  - advanced_refactoring
experimental_mode: false
---

# 实验功能配置

当前启用的功能:
- AI 驱动的代码建议
- 自动代码格式化
- 高级重构工具

实验模式已关闭（仅稳定功能）。
```

## 在钩子中使用

这些模板可以被钩子读取:

```bash
# Check if plugin is configured
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # Not configured, skip hook
fi

# Read settings
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' ".claude/my-plugin.local.md")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Apply settings
if [[ "$ENABLED" == "true" ]]; then
  # Hook is active
  # ...
fi
```

## Gitignore

始终添加到项目 `.gitignore`:

```gitignore
# Plugin settings (user-local, not committed)
.claude/*.local.md
.claude/*.local.json
```

## 编辑设置

用户可以手动编辑设置文件:

```bash
# Edit settings
vim .claude/my-plugin.local.md

# Changes take effect after restart
exit  # Exit Claude Code
claude  # Restart
```

更改需要重启 Claude Code - 钩子无法热交换。
