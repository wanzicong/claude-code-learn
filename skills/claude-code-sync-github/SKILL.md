---
name: claude-code-sync-github
description: 将 Claude Code 对话记录同步到 GitHub 仓库。当用户要求同步对话记录、备份对话历史、上传对话到 GitHub、查看同步状态时使用此技能。支持增量和全量同步模式，使用本地机器码作为项目标识，自动创建私有仓库，将 JSONL 对话记录转换为结构化 Markdown 文件。触发词包括："同步对话"、"备份对话"、"上传对话到GitHub"、"sync conversations"、"对话记录同步"。
---

# Claude Code 对话记录同步到 GitHub

从 `~/.claude/projects/` 读取 JSONL 对话记录，转换为结构化 Markdown，通过 `gh` + `git` 同步到 GitHub 私有仓库。

## 前置条件

- `gh` CLI 已安装且已认证（`gh auth login`）
- `git` 已安装
- Python 3.8+

检查认证状态：

```bash
gh auth status
```

## 仓库结构

```
claude-conversations-{机器码前8位}/
├── README.md                    # 仓库总览（机器信息、项目列表）
├── Users-13608/                 # 项目文件夹（按工作目录分组）
│   ├── 索引.md                  # 项目内对话列表
│   ├── {session-uuid-1}.md      # 单个对话（结构化 Markdown）
│   └── {session-uuid-2}.md
├── WorkeSpaceCoding-python/
│   ├── 索引.md
│   └── ...
└── ...
```

每个对话 Markdown 文件包含：
- 元信息表（会话ID、项目路径、模型、时间、Token用量）
- 用户消息（带时间戳和编号）
- 助手回复（含思考过程折叠、工具调用折叠）

## 工作流程

### 1. 查看同步状态

```bash
python {SKILL_DIR}/scripts/sync_conversations.py --status
```

输出机器码、项目数、对话数、已同步/待同步数量。

### 2. 初始化仓库（首次使用）

```bash
python {SKILL_DIR}/scripts/sync_conversations.py --init
```

自动获取机器码，在 GitHub 上创建私有仓库 `claude-conversations-{短标识}`。

### 3. 增量同步（默认）

```bash
python {SKILL_DIR}/scripts/sync_conversations.py
```

仅同步自上次以来有变化的对话文件。通过 MD5 哈希比对检测变化。

### 4. 全量同步

```bash
python {SKILL_DIR}/scripts/sync_conversations.py --mode full
```

重新处理所有对话文件并推送。

### 5. 自定义仓库名

```bash
python {SKILL_DIR}/scripts/sync_conversations.py --repo my-custom-repo
```

## 关键设计

- **机器码标识**：Windows 使用 `Win32_ComputerSystemProduct UUID`，macOS 使用 `IOPlatformUUID`，Linux 使用 `/sys/class/dmi/id/product_uuid` 或 `/etc/machine-id`
- **增量检测**：同步状态保存在 `~/.claude/.sync-state.json`，记录每个文件的 MD5 哈希
- **工作目录**：本地 git 仓库克隆在 `~/.claude/.sync-workdir/` 下
- **仓库权限**：默认创建私有仓库

## 注意事项

- 脚本中 `{SKILL_DIR}` 指本技能的安装目录，执行时替换为实际路径
- 首次同步大量对话时，git push 可能需要较长时间
- 对话内容可能包含敏感信息，仓库默认为私有
- 同步状态文件丢失后，下次增量同步会重新处理所有文件（等同全量）
