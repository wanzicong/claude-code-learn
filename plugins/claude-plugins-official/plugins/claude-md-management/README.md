# CLAUDE.md 管理插件

用于维护和改进 CLAUDE.md 文件的工具 - 审核质量、捕获会话学习内容、保持项目记忆更新。

## 功能

两个互补的工具用于不同目的：

| | claude-md-improver (技能) | /revise-claude-md (命令) |
|---|---|---|
| **目的** | 保持 CLAUDE.md 与代码库同步 | 捕获会话学习内容 |
| **触发时机** | 代码库变更 | 会话结束时 |
| **使用场景** | 定期维护 | 会话发现缺失的上下文 |

## 使用方法

### 技能：claude-md-improver

根据当前代码库状态审核 CLAUDE.md 文件：

```
"审核我的 CLAUDE.md 文件"
"检查我的 CLAUDE.md 是否是最新的"
```

<img src="claude-md-improver-example.png" alt="CLAUDE.md 改进器显示质量评分和推荐更新" width="600">

### 命令：/revise-claude-md

捕获当前会话的学习内容：

```
/revise-claude-md
```

<img src="revise-claude-md-example.png" alt="修订命令将会话学习内容捕获到 CLAUDE.md" width="600">

## 作者

Isabella He (isabella@anthropic.com)
