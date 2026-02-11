# Diff 审查模板

当 playground 是关于审查代码 diff 时使用此模板：git 提交、拉取请求、带有交互式逐行评论功能的代码更改，用于提供反馈。

## 布局

```
+-------------------+----------------------------------+
|                   |                                  |
|  提交头部:        |  Diff 内容                       |
|  • 哈希值         |  (文件和 hunks)                  |
|  • 消息           |  带有行号                       |
|  • 作者/日期      |  和 +/- 指示器                   |
|                   |                                  |
+-------------------+----------------------------------+
|  提示词输出面板（固定在右下角）                      |
|  [ 复制全部 ]                                          |
|  显示所有格式化为提示词的评论                           |
+------------------------------------------------------+
```

Diff 审查 playground 显示带有语法高亮的 git diff。用户点击行以添加评论，这些评论将成为用于代码审查反馈的生成提示词的一部分。

## Diff 审查的控件类型

| 功能 | 控件 | 行为 |
|---|---|---|
| 行评论 | 点击任何 diff 行 | 在行下方打开文本区域 |
| 评论指示器 | 已评论行上的徽章 | 显示哪些行有反馈 |
| 保存/取消 | 评论框中的按钮 | 保留或丢弃评论 |
| 复制提示词 | 提示词面板中的按钮 | 将所有评论复制到剪贴板 |

## Diff 渲染

将 diff 数据解析为结构化格式用于渲染：

```javascript
const diffData = [
  {
    file: "path/to/file.py",
    hunks: [
      {
        header: "@@ -41,13 +41,13 @@ function context",
        lines: [
          { type: "context", oldNum: 41, newNum: 41, content: "unchanged line" },
          { type: "deletion", oldNum: 42, newNum: null, content: "removed line" },
          { type: "addition", oldNum: null, newNum: 42, content: "added line" },
        ]
      }
    ]
  }
];
```

## 行类型样式

| 类型 | 背景 | 文本颜色 | 前缀 |
|---|---|---|---|
| `context` | 透明 | 默认 | ` ` (空格) |
| `addition` | 绿色调 (#dafbe1 浅色 / rgba(46,160,67,0.15) 深色) | 绿色 (#1a7f37 浅色 / #7ee787 深色) | `+` |
| `deletion` | 红色调 (#ffebe9 浅色 / rgba(248,81,73,0.15) 深色) | 红色 (#cf222e 浅色 / #f85149 深色) | `-` |
| `hunk-header` | 蓝色调 (#ddf4ff 浅色) | 蓝色 (#0969da 浅色) | `@@` |

## 评论系统

每条 diff 行获得一个唯一标识符用于评论跟踪：

```javascript
const comments = {}; // { lineId: commentText }

function selectLine(lineId, lineEl) {
  // 取消选择上一个
  document.querySelectorAll('.diff-line.selected').forEach(el =>
    el.classList.remove('selected'));
  document.querySelectorAll('.comment-box.active').forEach(el =>
    el.classList.remove('active'));

  // 选择新的
  lineEl.classList.add('selected');
  document.getElementById(`comment-box-${lineId}`).classList.add('active');
}

function saveComment(lineId) {
  const textarea = document.getElementById(`textarea-${lineId}`);
  const comment = textarea.value.trim();

  if (comment) {
    comments[lineId] = comment;
  } else {
    delete comments[lineId];
  }

  renderDiff(); // 重新渲染以显示评论指示器
  updatePromptOutput();
}
```

## 提示词输出格式

生成结构化代码审查格式：

```javascript
function updatePromptOutput() {
  const commentKeys = Object.keys(comments);

  if (commentKeys.length === 0) {
    promptContent.innerHTML = '<span class="no-comments">Click on any line to add a comment...</span>';
    return;
  }

  let output = 'Code Review Comments:\n\n';

  commentKeys.forEach(lineId => {
    const lineEl = document.querySelector(`[data-line-id="${lineId}"]`);
    const file = lineEl.dataset.file;
    const lineNum = lineEl.dataset.lineNum;
    const content = lineEl.dataset.content;

    output += `📍 ${file}:${lineNum}\n`;
    output += `   Code: ${content.trim()}\n`;
    output += `   Comment: ${comments[lineId]}\n\n`;
  });

  promptContent.textContent = output;
}
```

## 行元素的数据属性

在每个行元素上存储元数据用于提示词生成：

```html
<div class="diff-line addition"
     data-line-id="0-1-5"
     data-file="src/utils/handler.py"
     data-line-num="45"
     data-content="subagent_id = tracker.register()">
```

## 使用真实数据预填充

要为特定提交创建 diff 查看器：

1. 运行 `git show <commit> --format="%H%n%s%n%an%n%ad" -p`
2. 将输出解析为 `diffData` 结构
3. 在头部包含提交元数据

## 主题支持

支持浅色和深色模式：

```css
/* 浅色模式 */
body { background: #f6f8fa; color: #1f2328; }
.file-card { background: #ffffff; border: 1px solid #d0d7de; }
.diff-line.addition { background: #dafbe1; }
.diff-line.deletion { background: #ffebe9; }

/* 深色模式 */
body { background: #0d1117; color: #c9d1d9; }
.file-card { background: #161b22; border: 1px solid #30363d; }
.diff-line.addition { background: rgba(46, 160, 67, 0.15); }
.diff-line.deletion { background: rgba(248, 81, 73, 0.15); }
```

## 交互功能

- **悬停提示：** 在行悬停时显示" "点击评论"工具提示
- **评论指示器：** 带有保存评论的行上的徽章 (💬)
- **Toast 通知：** 复制时"已复制到剪贴板!"反馈
- **编辑现有：** 允许编辑之前保存的评论

## 示例主题

- Git 提交审查（单个提交 diff 和行评论）
- 拉取请求审查（多个提交、文件级别和行级别评论）
- 代码 diff 比较（重构前/后）
- 合并冲突解决（显示两个版本带注释）
- 代码审计（每行发现的安全审查）
