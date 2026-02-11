# 文档审查模板

当 playground 帮助审查和批评文档时使用此模板：SKILL.md 文件、README、规范、提案或任何需要带有批准/拒绝/评论工作流的结构化反馈的文本。

## 布局

```
+---------------------------+--------------------+
|                           |                    |
|  文档内容                 |  建议面板          |
|  带有行号                |  (可过滤列表)      |
|  和建议高亮              |  • 批准            |
|                           |  • 拒绝            |
|                           |  • 评论            |
|                           |                    |
+---------------------------+--------------------+
|  提示词输出（已批准 + 评论的项目）                   |
|  [ 复制提示词 ]                                        |
+------------------------------------------------+
```

## 关键组件

### 文档面板（左侧）
- 显示带有行号的完整文档
- 使用彩色左边框高亮带有建议的行
- 按状态着色：待处理（琥珀色）、已批准（绿色）、已拒绝（带透明度的红色）
- 点击建议卡片滚动到相关行

### 建议面板（右侧）
- 过滤器选项卡：全部 / 待处理 / 已批准 / 已拒绝
- 头部显示每个状态计数的统计
- 每个建议卡片显示：
  - 行引用（例如，"第 3 行"或"第 17-24 行"）
  - 建议文本
  - 操作按钮：批准 / 拒绝 / 评论（或如果已决定则重置）
  - 用于用户评论的可选文本区域

### 提示词输出（底部）
- 仅从已批准的建议和用户评论生成提示词
- 按以下分组：已批准的改进、额外反馈、已拒绝（用于上下文）
- 带有"已复制!"反馈的复制按钮

## 状态结构

```javascript
const suggestions = [
  {
    id: 1,
    lineRef: "Line 3",
    targetText: "description: Creates interactive...",
    suggestion: "The description is too long. Consider shortening.",
    category: "clarity",  // clarity、completeness、performance、accessibility、ux
    status: "pending",    // pending、approved、rejected
    userComment: ""
  },
  // ... 更多建议
];

let state = {
  suggestions: [...],
  activeFilter: "all",
  activeSuggestionId: null
};
```

## 建议与行匹配

通过解析 lineRef 将建议与文档行匹配：

```javascript
const suggestion = state.suggestions.find(s => {
  const match = s.lineRef.match(/Line[s]?\s*(\d+)/);
  if (match) {
    const targetLine = parseInt(match[1]);
    return Math.abs(targetLine - lineNum) <= 2; // 模糊匹配附近的行
  }
  return false;
});
```

## 文档渲染

内联处理 markdown 样式格式：

```javascript
// 跳过 ``` 行，将内容包装在 code-block-wrapper 中
if (line.startsWith('```')) {
  inCodeBlock = !inCodeBlock;
  // 打开或关闭包装器 div
}

// 标题
if (line.startsWith('# ')) renderedLine = `<h1>...</h1>`;
if (line.startsWith('## ')) renderedLine = `<h2>...</h2>`;

// 内联格式（代码块外）
renderedLine = renderedLine.replace(/`([^`]+)`/g, '<code>$1</code>');
renderedLine = renderedLine.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
```

## 提示词输出生成

仅包含可操作的项目：

```javascript
function updatePrompt() {
  const approved = state.suggestions.filter(s => s.status === 'approved');
  const withComments = state.suggestions.filter(s => s.userComment?.trim());

  if (approved.length === 0 && withComments.length === 0) {
    // 显示占位符
    return;
  }

  let prompt = 'Please update [DOCUMENT] with following changes:\n\n';

  if (approved.length > 0) {
    prompt += '## Approved Improvements\n\n';
    for (const s of approved) {
      prompt += `**${s.lineRef}:** ${s.suggestion}`;
      if (s.userComment?.trim()) {
        prompt += `\n  → User note: ${s.userComment.trim()}`;
      }
      prompt += '\n\n';
    }
  }

  // 来自非批准项目的额外反馈（带评论）
  // 已拒绝项目仅列出于上下文
}
```

## 样式高亮

```css
.doc-line.has-suggestion {
  border-left: 3px solid #bf8700;  /* 待处理的琥珀色 */
  background: rgba(191, 135, 0, 0.08);
}

.doc-line.approved {
  border-left-color: #1a7f37;  /* 绿色 */
  background: rgba(26, 127, 55, 0.08);
}

.doc-line.rejected {
  border-left-color: #cf222e;  /* 红色 */
  background: rgba(207, 34, 46, 0.08);
  opacity: 0.6;
}
```

## 预填充建议

为特定文档构建审查 playground 时：

1. 读取文档内容
2. 分析并生成建议，包括：
   - 具体行引用
   - 清晰、可操作的建议文本
   - 类别标签（clarity、completeness、performance、accessibility、ux）
3. 在 HTML 中嵌入文档内容和建议数组

## 示例用例

- SKILL.md 审查（技能定义质量、完整性、清晰度）
- README 批评（文档质量、缺失章节、不清楚的解释）
- 规范审查（需求清晰度、缺失边缘情况、歧义）
- 提案反馈（结构、论证、缺失上下文）
- 代码注释审查（文档字符串质量、内联注释有用性）
