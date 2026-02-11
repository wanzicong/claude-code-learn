---
description: 演示命令前置元数据选项的示例斜杠命令
argument-hint: <必需参数> [可选参数]
allowed-tools: [Read, Glob, Grep, Bash]
---

# 示例命令

此命令演示斜杠命令结构和前置元数据选项。

## 参数

用户使用以下参数调用了此命令：$ARGUMENTS

## 指令

当调用此命令时：

1. 解析用户提供的参数
2. 使用允许的工具执行请求的操作
3. 向用户报告结果

## 前置元数据选项参考

命令支持以下前置元数据字段：

- **description**：在 /help 中显示的简短描述
- **argument-hint**：向用户显示的命令参数提示
- **allowed-tools**：此命令的预批准工具（减少权限提示）
- **model**：覆盖模型（例如 "haiku"、"sonnet"、"opus"）

## 使用示例

```
/example-command my-argument
/example-command arg1 arg2
```
