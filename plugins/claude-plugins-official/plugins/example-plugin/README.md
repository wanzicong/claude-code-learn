# 示例插件

一个全面的示例插件，展示了 Claude Code 扩展选项。

## 结构

```
example-plugin/
├── .claude-plugin/
│   └── plugin.json        # 插件元数据
├── .mcp.json              # MCP 服务器配置
├── commands/
│   └── example-command.md # 斜杠命令定义
└── skills/
    └── example-skill/
        └── SKILL.md       # 技能定义
```

## 扩展选项

### 命令 (`commands/`)

斜杠命令通过用户使用 `/command-name` 调用。将它们定义为带有前置元数据的 markdown 文件：

```yaml
---
description: 用于 /help 的简短描述
argument-hint: <arg1> [可选参数]
allowed-tools: [Read, Glob, Grep]
---
```

### 技能 (`skills/`)

技能是由模型调用的功能。在子目录中创建 `SKILL.md`：

```yaml
---
name: skill-name
description: 此技能的触发条件
version: 1.0.0
---
```

### MCP 服务器 (`.mcp.json`)

通过模型上下文协议配置外部工具集成：

```json
{
  "server-name": {
    "type": "http",
    "url": "https://mcp.example.com/api"
  }
}
```

## 使用方法

- `/example-command [args]` - 运行示例斜杠命令
- 示例技能根据任务上下文激活
- 示例 MCP 根据任务上下文激活
