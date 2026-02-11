# 示例插件设置文件

## 模板：基本配置

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
mode: standard
---

# 我的插件配置

插件在标准模式下激活。
```

## 模板：高级配置

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

此项目使用自定义插件配置，包含：
- 标准验证模式
- 1MB 文件大小限制
- JavaScript/TypeScript 文件允许
- 信息级日志
- 3 次重试尝试

## 附加说明

如有问题请联系 @team-lead。
```

## 模板：代理状态文件

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: database-implementation
task_number: 4.2
pr_number: 5678
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.5", "Task 4.1"]
additional_instructions: "使用 PostgreSQL，而非 MySQL"
---

# 任务分配：数据库架构实现

为新功能模块实现数据库架构。

## 要求

- 创建迁移文件
- 为性能添加索引
- 为约束编写测试
- 在 README 中记录架构

## 成功标准

- 迁移成功运行
- 所有测试通过
- PR 已创建且 CI 绿色
- 已记录架构

## 协调

依赖于：
- 任务 3.5：API 端点定义
- 任务 4.1：数据模型设计

向协调器会话 'team-leader' 报告状态。
```

## 模板：功能标志模式

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

当前启用的功能：
- AI 驱动的代码建议
- 自动代码格式化
- 高级重构工具

实验模式关闭（仅稳定功能）。
```

## 在钩子中使用

这些模板可由钩子读取：

```bash
# 检查插件是否已配置
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # 未配置，跳过钩子
fi

# 读取设置
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' ".claude/my-plugin.local.md")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# 应用设置
if [[ "$ENABLED" == "true" ]]; then
  # 钩子激活
  # ...
fi
```

## Gitignore

始终添加到项目 `.gitignore`：

```gitignore
# 插件设置（用户本地，不提交）
.claude/*.local.md
.claude/*.local.json
```

## 编辑设置

用户可以手动编辑设置文件：

```bash
# 编辑设置
vim .claude/my-plugin.local.md

# 更改后生效
exit  # 退出 Claude Code
claude  # 重启
```

更改需要 Claude Code 重启 - 钩子无法热交换。
