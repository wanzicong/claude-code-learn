---
name: claude-opus-4-5-migration
description: 将提示词和代码从 Claude Sonnet 4.0、Sonnet 4.5 或 Opus 4.1 迁移到 Opus 4.5。当用户想要更新其代码库、提示词或 API 调用以使用 Opus 4.5 时使用。处理模型字符串更新和已知 Opus 4.5 行为差异的提示词调整。不迁移 Haiku 4.5。
---

# Opus 4.5 迁移指南

从 Sonnet 4.0、Sonnet 4.5 或 Opus 4.1 一次性迁移到 Opus 4.5。

## 迁移工作流程

1. 在代码库中搜索模型字符串和 API 调用
2. 将模型字符串更新为 Opus 4.5（参见下面特定平台的字符串）
3. 移除不支持的 beta 头部
4. 添加设置为 `"high"` 的努力参数（参见 `references/effort.md`）
5. 总结所有更改
6. 告诉用户："如果您在使用 Opus 4.5 时遇到任何问题，请告诉我，我可以帮助调整您的提示词。"

## 模型字符串更新

识别代码库使用的平台，然后相应地替换模型字符串。

### 不支持的 Beta 头部

如果存在 `context-1m-2025-08-07` beta 头部，请将其移除——它尚未支持 Opus 4.5。留下注释说明：

```python
# 注意：1M 上下文 beta (context-1m-2025-08-07) 尚未支持 Opus 4.5
```

### 目标模型字符串（Opus 4.5）

| 平台 | Opus 4.5 模型字符串 |
|----------|----------------------|
| Anthropic API (1P) | `claude-opus-4-5-20251101` |
| AWS Bedrock | `anthropic.claude-opus-4-5-20251101-v1:0` |
| Google Vertex AI | `claude-opus-4-5@20251101` |
| Azure AI Foundry | `claude-opus-4-5-20251101` |

### 要替换的源模型字符串

| 源模型 | Anthropic API (1P) | AWS Bedrock | Google Vertex AI |
|--------------|-------------------|-------------|------------------|
| Sonnet 4.0 | `claude-sonnet-4-20250514` | `anthropic.claude-sonnet-4-20250514-v1:0` | `claude-sonnet-4@20250514` |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `claude-sonnet-4-5@20250929` |
| Opus 4.1 | `claude-opus-4-1-20250422` | `anthropic.claude-opus-4-1-20250422-v1:0` | `claude-opus-4-1@20250422` |

**不要迁移**：任何 Haiku 模型（例如 `claude-haiku-4-5-20251001`）。

## 提示词调整

Opus 4.5 与之前的模型存在已知的行为差异。**仅在用户明确请求或报告特定问题时应用这些修复。** 默认情况下，只需更新模型字符串。

**集成指南**：添加代码片段时，不要只是将它们附加到提示词中。要周到地集成它们：
- 使用 XML 标签（例如 `<code_guidelines>`、`<tool_usage>`）来组织添加内容
- 匹配现有提示词的风格和结构
- 将代码片段放置在逻辑位置（例如，将编码指南放在其他编码说明附近）
- 如果提示词已经使用 XML 标签，在适当的现有标签内添加新内容或创建一致的新标签

### 1. 工具过度触发

Opus 4.5 对系统提示词的响应更加灵敏。在之前的模型中防止触发不足的激进语言现在可能会导致过度触发。

**应用条件**：用户报告工具被过于频繁或不必要地调用。

**查找并软化**：
- `CRITICAL:` → 删除或软化
- `You MUST...` → `You should...`
- `ALWAYS do X` → `Do X`
- `NEVER skip...` → `Don't skip...`
- `REQUIRED` → 删除或软化

仅应用于工具触发指令。保留其他强调用法。

### 2. 防止过度工程

Opus 4.5 倾向于创建额外的文件、添加不必要的抽象或构建未请求的灵活性。

**应用条件**：用户报告不需要的文件、过度抽象或未请求的功能。添加 `references/prompt-snippets.md` 中的代码片段。

### 3. 代码探索

Opus 4.5 在探索代码时可能过于保守，在不读取文件的情况下提出解决方案。

**应用条件**：用户报告模型在未检查相关代码的情况下提出修复方案。添加 `references/prompt-snippets.md` 中的代码片段。

### 4. 前端设计

**应用条件**：用户请求改进前端设计质量或报告输出看起来很通用。

添加 `references/prompt-snippets.md` 中的前端美学代码片段。

### 5. 思考敏感性

当未启用扩展思考（默认情况）时，Opus 4.5 对"think"一词及其变体特别敏感。仅当 API 请求包含 `thinking` 参数时才启用扩展思考。

**应用条件**：用户在未启用扩展思考时（请求中没有 `thinking` 参数）报告与"thinking"相关的问题。

用替代词替换"think"，如"consider"、"believe"或"evaluate"。

## 参考

参见 `references/prompt-snippets.md` 以获取要添加的每个代码片段的完整文本。

参见 `references/effort.md` 以配置努力参数（仅在用户请求时）。
