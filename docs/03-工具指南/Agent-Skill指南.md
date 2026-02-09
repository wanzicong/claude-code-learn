# Anthropic Agent Skill 完全指南

> 来源：[YouTube 视频](https://www.youtube.com/watch?v=yDc0_8emz7M) | 时长：约 17 分钟

## 视频概述

这是 Anthropic 于 2025 年 10 月正式发布的 **Agent Skill** 功能教程。Agent Skill 已成为 Claude AI 生态系统的通用模式，支持跨平台、跨产品使用。

## 核心主题

1. **Agent Skill 基础概念** - 什么是 Agent Skill 以及它解决的问题
2. **创建与使用** - 如何在 Claude Code 中创建和使用 Agent Skill
3. **高级功能** - Reference（参考）和 Script（脚本）的使用
4. **与 MCP 的区别** - Agent Skill 与 MCP 的对比和选择

---

## 详细内容

### 00:00 - 什么是 Agent Skill？

**定义**：Agent Skill 本质上是一个**提示词模板**，用于解决特定领域的问题。

**核心价值**：
- 避免每次对话都重复说明相同的背景和规则
- 将专业知识封装成可复用的技能
- 让 Claude 更专注于执行而非理解背景

**类比**：就像给 Claude 添加了一个"专家助手"，每次遇到相关问题时，这个助手会自动介入提供专业指导。

### 01:28 - Agent Skill 的目录结构

```
.claude/skills/
├── 技能名称（文件夹）
│   ├── skill.md          # 必需：技能配置文件
│   ├── reference/        # 可选：参考资料
│   └── script/           # 可选：可执行脚本
```

**skill.md 文件格式**（YAML 前置元数据）：

```yaml
---
name: 技能名称
description: 这个技能是用来做什么的
instruction: |
  这里写详细的指令，规定 AI 要遵循的规则
  - 要用中文输出
  - 输出格式要符合什么规范
  - 角色定位等
---
```

### 02:57 - 基础使用流程

1. **创建技能目录**：在用户目录下创建 `.claude/skills/技能名称/`
2. **编写 skill.md**：定义技能的元数据和指令
3. **使用触发词**：在对话中输入 `/技能名称` 或自然触发

**关键点**：
- 只有当模型判断用户输入与某个 Agent Skill 匹配时，才会加载该技能
- 按需加载，节省 Token 成本

### 04:30 - Reference（参考资料）功能

**用途**：提供大型文档、数据库等参考资料，避免每次都传输完整内容。

**示例场景**：
- 公司内部政策文档（500+ 页）
- 财务预算规则
- 法律合规要求

**工作流程**：
1. 将参考文档放入 `reference/` 目录
2. 在 skill.md 中指定何时读取哪些文档
3. Claude Code 只在需要时才读取相关文档

**节省 Token 的关键**：只在触发特定条件（如提到钱、合规等）时才加载。

### 07:42 - Script（可执行脚本）功能

**用途**：执行 Python 脚本完成复杂业务逻辑。

**示例**：文件上传功能
```python
# upload.py
import some_library
def upload_file(file_path):
    # 上传逻辑
    return upload_result
```

**工作流程**：
1. 用户触发上传需求
2. Claude Code 识别需要使用该 Skill
3. 执行 upload.py 脚本
4. 返回执行结果给用户

**特点**：
- 脚本内容不会被模型读取（节省 Token）
- 只执行脚本并获取输出结果
- 适合复杂的业务逻辑处理

### 09:47 - Agent Skill 的工作原理

```
用户输入
    ↓
模型路由（匹配 Skill）
    ↓
加载 skill.md（指令）
    ↓
判断是否需要 Reference → [是] → 读取参考文档
    ↓ [否]
判断是否需要 Script → [是] → 执行脚本获取结果
    ↓ [否]
模型根据指令生成响应
    ↓
返回给用户
```

**按需加载策略**：
- 初始阶段只获取 Skill 的名称和描述
- 只有选中某个 Skill 后，才加载完整的 skill.md 内容
- Reference 和 Script 只在需要时才加载/执行

### 13:23 - Agent Skill vs MCP

| 特性 | Agent Skill | MCP (Model Context Protocol) |
|------|------------|------------------------------|
| **作用** | 教模型如何处理数据 | 连接模型与外部数据源 |
| **功能** | 提示词模板 + 脚本执行 | API 调用 + 数据查询 |
| **适用场景** | 简单脚本、本地逻辑 | 外部服务、数据库查询 |
| **安全性** | 更安全（本地执行） | 需要外部连接 |
| **复杂度** | 简单 | 相对复杂 |

**官方观点**：
> "MCP connects Claude to data. Skills teach Claude what to do with that data."

**最佳实践**：两者可以结合使用，发挥各自优势。

---

## 重要概念与术语

| 术语 | 解释 |
|------|------|
| **Agent Skill** | Anthropic 推出的提示词模板系统，用于封装专业知识和工作流程 |
| **skill.md** | Agent Skill 的核心配置文件，包含元数据和指令 |
| **Reference** | 参考资料目录，存放大型文档供按需读取 |
| **Script** | 可执行脚本目录，存放 Python 脚本供执行 |
| **触发词** | 用于激活特定 Agent Skill 的关键词 |
| **按需加载** | 只在需要时才加载 Skill 内容，节省 Token |
| **MCP** | Model Context Protocol，用于连接 Claude 和外部数据源 |

---

## 关键要点

1. **Agent Skill = 提示词模板**：本质是封装专业知识的模板，让 Claude 更高效地完成任务

2. **三要素结构**：
   - `skill.md`：必需，定义技能行为
   - `reference/`：可选，提供参考资料
   - `script/`：可选，执行业务逻辑

3. **按需加载节省成本**：只在匹配时才加载 Skill 内容，Reference 和 Script 也按需使用

4. **与 MCP 互补**：Agent Skill 适合简单逻辑和本地执行，MCP 适合外部数据连接

5. **安全性更高**：Agent Skill 的脚本内容不会被模型读取，只执行并获取结果

---

## 实用建议

### 适合使用 Agent Skill 的场景

- 需要重复解释专业背景知识
- 有固定的输出格式要求
- 需要执行简单的本地脚本
- 有大量参考文档但不想每次都传输

### 不适合使用 Agent Skill 的场景

- 需要实时查询外部数据库
- 需要调用第三方 API
- 复杂的多步骤外部服务集成（这些场景更适合 MCP）

---

## 总结与建议

Agent Skill 是 Anthropic 生态系统中重要的功能扩展机制。它通过**提示词模板**的方式，让开发者能够：

1. **封装专业知识** - 将领域知识沉淀为可复用的 Skill
2. **节省 Token 成本** - 通过按需加载机制避免重复传输
3. **扩展 Claude 能力** - 通过 Script 执行复杂业务逻辑
4. **提高工作效率** - 减少重复性沟通，让 AI 更快上手

**建议**：
- 从简单的 Skill 开始实践
- 善用 Reference 处理大型文档
- 复杂逻辑考虑 Script 执行
- 与 MCP 配合使用发挥最大价值
