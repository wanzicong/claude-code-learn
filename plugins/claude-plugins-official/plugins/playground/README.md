# Playground Plugin

创建交互式 HTML playground —— 自包含的单文件探索器，让用户通过控件可视化地配置内容、查看实时预览，并复制生成的提示词。

## 什么是 Playground?

Playground 是一个自包含的 HTML 文件，具有以下特点：
- 一侧是交互式控件
- 另一侧是实时预览
- 底部是带有复制按钮的提示词输出

用户调整控件，进行可视化探索，然后将生成的提示词复制回 Claude。

## 何时使用

当用户要求为某个主题创建交互式 playground、探索器或可视化工具时使用此插件 —— 尤其是当输入空间很大、可视化或结构化，且难以用纯文本表达时。

## 模板

该技能包含常见 playground 类型的模板：
- **design-playground** — 视觉设计决策（组件、布局、间距、颜色、排版）
- **data-explorer** — 数据和查询构建（SQL、API、管道、正则表达式）
- **concept-map** — 学习和探索（概念图、知识缺口、范围映射）
- **document-critique** — 文档审查（带有批准/拒绝/评论工作流的建议）

## 安装

将此插件添加到您的 Claude Code 配置中以启用 playground 技能。
