---
description: 交互式启用或禁用 hookify 规则
allowed-tools: ["Glob", "Read", "Edit", "AskUserQuestion", "Skill"]
---

# 配置 Hookify 规则

**首先加载 hookify:writing-rules 技能** 以了解规则格式。

使用交互界面启用或禁用现有的 hookify 规则。

## 步骤

### 1. 查找现有规则

使用 Glob 工具查找所有 hookify 规则文件：
```
pattern: ".claude/hookify.*.local.md"
```

如果未找到规则，通知用户：
```
尚未配置 hookify 规则。使用 `/hookify` 创建您的第一个规则。
```

### 2. 读取当前状态

对于每个规则文件：
- 读取文件
- 从前置数据中提取 `name` 和 `enabled` 字段
- 构建包含当前状态的规则列表

### 3. 询问用户要切换哪些规则

使用 AskUserQuestion 让用户选择规则：

```json
{
  "questions": [
    {
      "question": "您想启用或禁用哪些规则？",
      "header": "配置",
      "multiSelect": true,
      "options": [
        {
          "label": "warn-dangerous-rm (当前已启用)",
          "description": "警告 rm -rf 命令"
        },
        {
          "label": "warn-console-log (当前已禁用)",
          "description": "警告代码中的 console.log"
        },
        {
          "label": "require-tests (当前已启用)",
          "description": "停止前要求测试"
        }
      ]
    }
  ]
}
```

**选项格式：**
- 标签：`{rule-name} (当前 {enabled|disabled})`
- 描述：来自规则消息或模式的简要描述

### 4. 解析用户选择

对于每个选定的规则：
- 从标签确定当前状态（enabled/disabled）
- 切换状态：enabled → disabled，disabled → enabled

### 5. 更新规则文件

对于每个要切换的规则：
- 使用 Read 工具读取当前内容
- 使用 Edit 工具将 `enabled: true` 更改为 `enabled: false`（反之亦然）
- 处理带引号和不带引号的情况

**启用编辑模式：**
```
old_string: "enabled: false"
new_string: "enabled: true"
```

**禁用编辑模式：**
```
old_string: "enabled: true"
new_string: "enabled: false"
```

### 6. 确认更改

向用户显示更改的内容：

```
## Hookify 规则已更新

**已启用：**
- warn-console-log

**已禁用：**
- warn-dangerous-rm

**未更改：**
- require-tests

更改立即生效 - 无需重启
```

## 重要说明

- 更改在下次工具使用时立即生效
- 您也可以手动编辑 .claude/hookify.*.local.md 文件
- 要永久删除规则，请删除其 .local.md 文件
- 使用 `/hookify:list` 查看所有已配置的规则

## 边缘情况

**没有规则可配置：**
- 显示首先使用 `/hookify` 创建规则的消息

**用户未选择规则：**
- 通知未进行任何更改

**文件读取/写入错误：**
- 通知用户具体错误
- 建议手动编辑作为后备方案
