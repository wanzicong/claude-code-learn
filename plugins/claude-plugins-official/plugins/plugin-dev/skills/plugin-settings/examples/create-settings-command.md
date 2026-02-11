---
description: "使用用户偏好创建插件设置文件"
allowed-tools: ["Write", "AskUserQuestion"]
---

# 创建插件设置

此命令帮助用户创建 `.claude/my-plugin.local.md` 设置文件。

## 步骤

### 步骤 1：询问用户偏好

使用 AskUserQuestion 收集配置：

```json
{
  "questions": [
    {
      "question": "为此项目启用插件？",
      "header": "启用插件",
      "multiSelect": false,
      "options": [
        {
          "label": "是",
          "description": "插件将激活"
        },
        {
          "label": "否",
          "description": "插件将禁用"
        }
      ]
    },
    {
      "question": "验证模式？",
      "header": "模式",
      "multiSelect": false,
      "options": [
        {
          "label": "严格",
          "description": "最大验证和安全检查"
        },
        {
          "label": "标准",
          "description": "平衡验证（推荐）"
        },
        {
          "label": "宽松",
          "description": "仅最小验证"
        }
      ]
    }
  ]
}
```

### 步骤 2：解析答案

从 AskUserQuestion 结果提取答案：

- answers["0"]: enabled（是/否）
- answers["1"]: mode（严格/标准/宽松）

### 步骤 3：创建设置文件

使用 Write 工具创建 `.claude/my-plugin.local.md`：

```markdown
---
enabled: <true 如果是，否则 false>
validation_mode: <strict、standard 或 lenient>
max_file_size: 1000000
notify_on_errors: true
---

# 插件配置

您的插件配置为 <mode> 验证模式。

如需修改设置，编辑此文件并重启 Claude Code。
```

### 步骤 4：通知用户

通知用户：
- 设置文件已创建于 `.claude/my-plugin.local.md`
- 当前配置摘要
- 如需则如何手动编辑
- 提醒：重启 Claude Code 以使更改生效
- 设置文件已 gitignored（不会被提交）

## 实现说明

写入前始终验证用户输入：
- 检查模式有效
- 验证数字字段为数字
- 确保路径没有遍历尝试
- 清理任何自由文本字段
