---
name: playground
description: 创建交互式 HTML playground —— 自包含的单文件探索器，让用户通过控件可视化地配置内容、查看实时预览，并复制生成的提示词。当用户要求为某个主题创建 playground、探索器或交互式工具时使用。
---

# Playground 构建器

Playground 是一个自包含的 HTML 文件，一侧是交互式控件，另一侧是实时预览，底部是带有复制按钮的提示词输出。用户调整控件，进行可视化探索，然后将生成的提示词复制回 Claude。

## 何时使用此技能

当用户要求为某个主题创建交互式 playground、探索器或可视化工具时使用 —— 尤其是当输入空间很大、可视化或结构化，且难以用纯文本表达时。

## 如何使用此技能

1. **从用户请求中识别 playground 类型**
2. **从 `templates/` 加载匹配的模板**：
   - `templates/design-playground.md` — 视觉设计决策（组件、布局、间距、颜色、排版）
   - `templates/data-explorer.md` — 数据和查询构建（SQL、API、管道、正则表达式）
   - `templates/concept-map.md` — 学习和探索（概念图、知识缺口、范围映射）
   - `templates/document-critique.md` — 文档审查（带有批准/拒绝/评论工作流的建议）
   - `templates/diff-review.md` — 代码审查（git diff、提交、PR，带逐行评论）
   - `templates/code-map.md` — 代码库架构（组件关系、数据流、层级图）
3. **按照模板构建 playground**。如果主题不能完全匹配任何模板，使用最接近的并进行调整。
4. **在浏览器中打开**。编写 HTML 文件后，运行 `open <filename>.html` 在用户的默认浏览器中启动它。

## 核心要求（每个 playground）

- **单一 HTML 文件**。内联所有 CSS 和 JS。无外部依赖。
- **实时预览**。每次控件更改时立即更新。无需"应用"按钮。
- **提示词输出**。自然语言，而非数值转储。仅提及非默认选项。包含足够的上下文以便在没有看到 playground 的情况下执行操作。实时更新。
- **复制按钮**。剪贴板复制，带有简短的"已复制!"反馈。
- **合理的默认值 + 预设**。首次加载时显示良好。包含 3-5 个命名预设，将所有控件快速切换到一致的组合。
- **深色主题**。UI 使用系统字体，代码/值使用等宽字体。最小化装饰。

## 状态管理模式

保持单个状态对象。每个控件向其写入，每个渲染从中读取。

```javascript
const state = { /* 所有可配置的值 */ };

function updateAll() {
  renderPreview(); // 更新视觉效果
  updatePrompt();  // 重新构建提示词文本
}
// 每个控件在更改时调用 updateAll()
```

## 提示词输出模式

```javascript
function updatePrompt() {
  const parts = [];

  // 仅提及非默认值
  if (state.borderRadius !== DEFAULTS.borderRadius) {
    parts.push(`border-radius of ${state.borderRadius}px`);
  }

  // 在数字旁边使用定性语言
  if (state.shadowBlur > 16) parts.push('a pronounced shadow');
  else if (state.shadowBlur > 0) parts.push('a subtle shadow');

  prompt.textContent = `Update the card to use ${parts.join(', ')}.`;
}
```

## 避免常见错误

- 提示词输出只是数值转储 → 将其编写为自然指令
- 一次有太多控件 → 按关注点分组，将高级选项隐藏在可折叠部分中
- 预览不立即更新 → 每个控件更改都必须触发立即重新渲染
- 没有默认值或预设 → 加载时为空或损坏
- 外部依赖 → 如果 CDN 宕机，playground 将无法使用
- 提示词缺乏上下文 → 包含足够的上下文，使其在没有 playground 的情况下也可执行
