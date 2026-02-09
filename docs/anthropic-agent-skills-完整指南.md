# Anthropic Agent Skills 完整使用指南和实战指南

> 全面掌握 Claude Code 技能系统：从入门到精通

---

## 📚 目录

- [第一章：技能系统基础](#第一章技能系统基础)
  - [1.1 什么是 Agent Skills](#11-什么是-agent-skills)
  - [1.2 技能的工作原理](#12-技能的工作原理)
  - [1.3 技能文件格式](#13-技能文件格式)
  - [1.4 与其他功能的区别](#14-与其他功能的区别)
- [第二章：配置和安装](#第二章配置和安装)
  - [2.1 技能目录结构](#21-技能目录结构)
  - [2.2 安装技能](#22-安装技能)
  - [2.3 配置技能](#23-配置技能)
  - [2.4 验证安装](#24-验证安装)
- [第三章：技能创建完整流程](#第三章技能创建完整流程)
  - [3.1 创建流程概览](#31-创建流程概览)
  - [3.2 SKILL.md 编写指南](#32-skillmd-编写指南)
  - [3.3 脚本和资源管理](#33-脚本和资源管理)
  - [3.4 测试和调试](#34-测试和调试)
  - [3.5 打包和分发](#35-打包和分发)
- [第四章：核心技能详解](#第四章核心技能详解)
  - [4.1 文档处理技能](#41-文档处理技能)
  - [4.2 开发工具技能](#42-开发工具技能)
  - [4.3 设计工具技能](#43-设计工具技能)
- [第五章：实战案例](#第五章实战案例)
  - [5.1 案例1：餐厅物料创意生成技能](#51-案例1餐厅物料创意生成技能)
  - [5.2 案例2：Stripe 支付集成技能](#52-案例2stripe-支付集成技能)
  - [5.3 案例3：自定义 MCP 服务器](#53-案例3自定义-mcp-服务器)
- [第六章：最佳实践](#第六章最佳实践)
  - [6.1 设计原则](#61-设计原则)
  - [6.2 性能优化](#62-性能优化)
  - [6.3 安全考虑](#63-安全考虑)
  - [6.4 维护和更新](#64-维护和更新)
- [附录](#附录)
  - [A. 常见问题 FAQ](#a-常见问题-faq)
  - [B. 技能模板](#b-技能模板)
  - [C. 脚本示例](#c-脚本示例)
  - [D. 参考资源](#d-参考资源)
  - [E. 术语表](#e-术语表)

---

## 第一章：技能系统基础

### 1.1 什么是 Agent Skills

#### 定义

**Agent Skills（代理技能）** 是 Claude Code 的核心扩展机制，本质上是一个**提示词模板系统**，用于为 Claude 添加专业知识、工作流程和领域专长。

简单来说，技能就是：
- 📝 **提示词模板** - 预定义的指令和知识
- 🔧 **可执行脚本** - 自动化的工具和脚本
- 📚 **参考文档** - 详细的规范和示例
- 🎨 **静态资源** - 模板、配置和素材

#### 核心价值

技能系统解决了以下问题：

1. **避免重复说明** ✅
   - 不需要每次对话都重复相同的背景和规则
   - 一次定义，多次使用

2. **封装专业知识** 🎓
   - 将领域专长封装成可复用的技能
   - 让 Claude 成为特定领域的专家

3. **提高执行效率** ⚡
   - Claude 更专注于执行而非理解背景
   - 减少理解偏差，提高准确性

4. **节省 Token 成本** 💰
   - 按需加载机制，只在需要时加载内容
   - 避免无关内容占用上下文窗口

#### 类比理解

可以把技能系统类比为：

```
技能系统 = 专家助手团队

你（用户）
  ↓ 提出需求
Claude（主管）
  ↓ 识别需要哪个专家
技能（专家助手）
  ↓ 提供专业指导和工具
Claude（主管）
  ↓ 执行任务
结果输出
```

**示例**：
- 当你说"帮我处理这个 PDF 文件"
- Claude 识别到需要 PDF 处理专家
- 自动加载 `pdf` 技能的知识和工具
- 按照专业流程完成任务

### 1.2 技能的工作原理

#### 三层按需加载架构

技能系统采用**三层渐进式加载**机制，实现高效的上下文管理：

```
┌────────────────────────���────────────────────────────┐
│              第一层：元信息层（Metadata）             │
│  ┌───────────────────────────────────────────────┐  │
│  │  ✓ 始终加载，AI 每次对话都会看到               │  │
│  │  ✓ 内容：name + description                   │  │
│  │  ✓ Token 消耗：极低（~100 词）                │  │
│  │  ✓ 用途：让 AI 知道自己有哪些技能可用          │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ 触发技能后
┌─────────────────────────────────────────────────────┐
│              第二层：指令层（SKILL.md）              │
│  ┌───────────────────────────────────────────────┐  │
│  │  ✓ 只有 AI 决定使用该技能时才加载              │  │
│  │  ✓ 内容：完整的 SKILL.md 指令部分             │  │
│  │  ✓ Token 消耗：按需（<5k 词）                │  │
│  │  ✓ 用途：告诉 AI 具体如何执行任务             │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ 进一步需要时
┌─────────────────────────────────────────────────────┐
│              第三层：资源层（References/Scripts）    │
│  ┌───────────────────────────────────────────────┐  │
│  │  ✓ 按需加载，只在需要详细资料或执行脚本时用    │  │
│  │  ✓ 内容：references/scripts/assets            │  │
│  │  ✓ Token 消耗：无限制（脚本不读取）           │  │
│  │  ✓ 用途：提供详细规范、执行脚本、静态资源      │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

#### 触发机制

技能有两种触发方式：

**1. 自动触发（推荐）** 🤖

基于 `description` 字段的智能匹配：

```
用户输入：帮我处理这个 PDF 文件，合并两个文档
         ↓
Claude 分析输入，匹配到关键词 "PDF"
         ↓
自动加载 "pdf" 技能
         ↓
应用技能指令执行任务
```

**2. 显式调用（可选）** 👤

用户使用斜杠命令：

```bash
/技能名称 具体任务描述
```

**示例**：
```bash
/pdf 帮我旋转这个 PDF 文件
/stripe-best-practices 我要实现一个订阅支付系统
```

#### 工作流程详解

```
┌─────────────┐
│  用户输入    │
└──────┬──────┘
       ↓
┌─────────────────────────────────────┐
│  Claude 分析输入                     │
│  - 提取关键词                        │
│  - 匹配技能 description              │
│  - 评估相关性                        │
└──────┬──────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  加载技能（第二层）                  │
│  - 读取 SKILL.md 内容                │
│  - 理解工作流程和规则                │
└──────┬──────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  判断是否需要额外资源                │
│  ├─ 需要参考文档？→ 读取 references/ │
│  ├─ 需要执行脚本？→ 运行 scripts/    │
│  └─ 需要模板文件？→ 使用 assets/     │
└──────┬──────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  执行任务                            │
│  - 应用技能指令                      │
│  - 调用工具和脚本                    │
│  - 生成输出                          │
└──────┬──────────────────────────────┘
       ↓
┌─────────────┐
│  返回结果    │
└─────────────┘
```

#### 上下文管理

技能系统的智能之处在于**上下文窗口的高效利用**：

| 阶段 | 加载内容 | Token 消耗 | 何时加载 |
|------|---------|-----------|---------|
| **待机** | 所有技能的 name + description | 低（~2k tokens） | 始终 |
| **激活** | 单个技能的 SKILL.md | 中（~3-5k tokens） | 技能触发时 |
| **深入** | 特定的 references/scripts | 高（按需） | 明确需要时 |

**优势**：
- ✅ 可以同时拥有 50+ 个技能而不影响性能
- ✅ 只有相关技能会占用上下文
- ✅ 详细文档按需加载，不浪费 Token
- ✅ 脚本执行不占用上下文窗口

### 1.3 技能文件格式

#### SKILL.md 文件结构

每个技能的核心是 `SKILL.md` 文件，采用 **YAML 前置元数据 + Markdown 内容** 的格式：

```markdown
---
name: skill-name                    # 必需：技能唯一标识符
description: |                      # 必需：触发条件和功能说明
  完整描述技能做什么和何时使用。
  包括所有"何时使用"信息。
  包括具体的触发关键词。
version: 1.0.0                      # 可选：版本号
license: MIT                        # 可选：许可证
compatibility: Claude Code 1.0+     # 可选：兼容性要求
---

# 技能标题

## 概述
简要说明技能用途（1-2 段）

## 快速开始
最常见用例的简洁示例

## 核心功能
主要功能列表

## 高级用法
复杂场景的处理方法

## 参考文档
链接到 references/ 中的详细文档
```

#### YAML 前置元数据字段详解

| 字段 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `name` | ✅ | 技能标识符，小写，用连字符分隔 | `pdf-editor` |
| `description` | ✅ | 触发条件和功能说明（50-500字符） | "处理 PDF 文件，支持读取、编辑、合并..." |
| `version` | ❌ | 语义化版本号 | `1.2.0` |
| `license` | ❌ | 许可证信息 | `MIT`, `Apache 2.0` |
| `compatibility` | ❌ | 环境要求 | `Claude Code 1.0+` |

#### description 字段最佳实践

**❌ 错误示例**：
```yaml
description: PDF 处理工具
```

**问题**：
- 太简短，无法准确匹配
- 没有说明何时使用
- 缺少触发关键词

**✅ 正确示例**：
```yaml
description: |
  全面的 PDF 处理工具，支持读取、编辑、合并、拆分、旋转、
  加水印、表单填充、加密解密和 OCR。当用户提到 .pdf 文件
  或要求处理 PDF 时使用。触发词包括：PDF、pdf、合并文档、
  拆分页面、提取文本、填写表单。
```

**关键要点**：
- ✅ 列出所有主要功能
- ✅ 明确说明何时使用
- ✅ 包含触发关键词
- ✅ 50-500 字符为宜
- ✅ 使用第三人称："This skill should be used when..."

#### 技能目录结构

```
skill-name/                         # 技能根目录
├── SKILL.md                        # ⭐ 必需：技能定义文件
├── LICENSE.txt                     # 推荐：许可证文件
├── scripts/                        # 可选：可执行脚本
│   ├── main.py                     # 主要功能脚本
│   ├── utils.py                    # 工具函数
│   └── requirements.txt            # Python 依赖
├── references/                     # 可选：参考文档
│   ├── api_docs.md                 # API 文档
│   ├── workflows.md                # 工作流程
│   └── examples.md                 # 示例代码
└── assets/                         # 可选：静态资源
    ├── templates/                  # 模板文件
    ├── config/                     # 配置文件
    └── images/                     # 图片资源
```

#### 各目录的用途

| 目录 | 何时使用 | 示例 |
|------|---------|------|
| **scripts/** | 重复编写的代码、需要确定性可靠性的操作 | PDF 旋转脚本、数据处理脚本 |
| **references/** | API 文档、数据库模式、详细工作流程、领域知识 | Stripe API 文档、SQL 模式定义 |
| **assets/** | 模板文件、图标和字体、样板代码、配置文件 | HTML 模板、logo 文件、配置 JSON |


### 1.4 与其他功能的区别

#### Agent Skills vs MCP vs Commands vs Agents

| 功能 | Agent Skill | MCP | Command | Agent |
|------|------------|-----|---------|-------|
| **作用** | 教模型如何处理数据 | 连接模型与外部数据源 | 用户主动调用 | 自主执行任务 |
| **触发方式** | 自动匹配 | 自动可用 | 用户输入 `/command` | 自主决策 |
| **适用场景** | 简单脚本、本地逻辑 | 外部服务、数据库查询 | 快速操作 | 复杂工作流 |
| **安全性** | 更安全（本地执行） | 需要外部连接 | 用户控制 | 需要监督 |
| **Token 消耗** | 按需加载 | 工具定义始终加载 | 无 | 高 |
| **开发难度** | 低（Markdown + 脚本） | 中（需要服务器） | 低（配置） | 高（复杂逻辑） |

#### 官方观点

> "MCP connects Claude to data. Skills teach Claude what to do with that data."

**简单理解**：
- **MCP**：连接外部数据（如 Jira、GitHub、数据库）
- **Skills**：教 Claude 如何使用这些数据（如最佳实践、工作流程）

#### 选择指南

**使用 Agent Skill 当**：
- 需要封装领域知识和最佳实践
- 有重复的工作流程需要标准化
- 需要本地脚本执行
- 想要节省 Token 成本

**使用 MCP 当**：
- 需要连接外部服务（API、数据库）
- 需要实时数据查询
- 需要多个客户端共享数据源
- 需要认证和权限管理

---

## 第二章：配置和安装

### 2.1 技能目录结构

#### 技能存放位置

Claude Code 支持两个级别的技能目录：

**1. 用户级技能目录**

```bash
~/.claude/skills/
├── pdf-editor/
├── stripe-best-practices/
└── my-custom-skill/
```

**特点**：
- 全局可用，所有项目都能使用
- 适合通用技能
- 个人定制技能

**2. 项目级技能目录**

```bash
your-project/
└── .claude/
    └── skills/
        ├── project-specific-skill/
        └── team-shared-skill/
```

**特点**：
- 仅在当前项目可用
- 适合项目特定技能
- 可以提交到版本控制
- 团队共享

### 2.2 安装技能

#### 方法一：从市场安装（推荐）

```bash
# 添加 Anthropic 技能市场
/plugin marketplace add anthropics/skills

# 安装文档处理技能包
/plugin install document-skills@anthropic-agent-skills

# 安装示例技能包
/plugin install example-skills@anthropic-agent-skills
```

#### 方法二：手动安装

```bash
# 创建技能目录
mkdir -p ~/.claude/skills/my-skill

# 创建 SKILL.md 文件
cat > ~/.claude/skills/my-skill/SKILL.md << 'INNEREOF'
---
name: my-skill
description: 我的自定义技能，用于处理特定任务
---

# 我的技能

## 概述
这是一个自定义技能示例。
INNEREOF
```

### 2.3 配置技能

#### 启用和禁用技能

**启用技能**：将技能目录放在 `~/.claude/skills/` 或 `.claude/skills/`

**禁用技能**：
```bash
# 重命名目录
mv ~/.claude/skills/my-skill ~/.claude/skills/my-skill.disabled
```

### 2.4 验证安装

```bash
# 检查 SKILL.md 是否存在
ls ~/.claude/skills/my-skill/SKILL.md

# 检查目录结构
tree ~/.claude/skills/my-skill/
```


---

## 第三章：技能创建完整流程

### 3.1 创建流程概览

#### 6步创建流程

创建一个高质量的技能需要经过以下6个步骤：

```
步骤 1: 理解需求
  ├─ 明确技能的用途
  ├─ 收集具体使用示例（2-3个）
  ├─ 确定输入输出
  └─ 识别外部依赖

步骤 2: 规划内容
  ├─ 分析每个使用示例
  ├─ 识别可复用的代码 → scripts/
  ├─ 识别需要的文档 → references/
  └─ 识别需要的资源 → assets/

步骤 3: 初始化技能
  ├─ 创建技能目录结构
  ├─ 生成 SKILL.md 模板
  └─ 创建子目录

步骤 4: 编写 SKILL.md
  ├─ 填写 YAML 前置元数据
  ├─ 编写清晰的 description
  ├─ 组织主要内容
  └─ 添加参考链接

步骤 5: 添加资源
  ├─ 实现脚本功能
  ├─ 编写参考文档
  ├─ 准备资源文件
  └─ 测试所有组件

步骤 6: 测试和迭代
  ├─ 验证技能格式
  ├─ 在实际场景中测试
  ├─ 收集反馈
  └─ 持续改进
```

### 3.2 SKILL.md 编写指南

#### YAML 前置元数据详解

**必需字段**：

```yaml
---
name: skill-name
description: |
  完整描述...
---
```

#### description 字段编写技巧

**公式**：description = 功能说明 + 使用场景 + 触发关键词

**关键要点**：
1. 具体而全面 - 列出所有主要功能
2. 场景导向 - 说明何时使用
3. 关键词丰富 - 包含用户可能使用的词汇
4. 长度适中 - 50-500 字符

### 3.3 脚本和资源管理

#### 何时创建脚本

**创建脚本的场景**：
1. 重复代码 - 相同代码被多次编写
2. 确定性操作 - 需要精确执行的步骤
3. 复杂逻辑 - 多步骤的复杂流程
4. 性能要求 - 需要高效执行

### 3.4 测试和调试

#### 验��技能格式

```bash
# 检查 SKILL.md 存在
ls ~/.claude/skills/my-skill/SKILL.md

# 测试脚本执行
python ~/.claude/skills/my-skill/scripts/main.py --help
```

### 3.5 打包和分发

#### 打包技能

```bash
# 创建压缩包
cd ~/.claude/skills/
tar -czf my-skill.tar.gz my-skill/
```


---

## 第四章：核心技能详解

### 4.1 文档处理技能

#### docx - Word 文档处理

**功能概述**：
- 创建、读取、编辑 Word 文档
- 支持追踪更改和注释
- 处理复杂格式和样式
- XML 级别的精确控制

**核心工具**：

| 任务 | 方法 | 工具 |
|------|------|------|
| 读取内容 | pandoc 或解包 XML | pandoc / unpack.py |
| 创建文档 | docx-js 库 | JavaScript |
| 编辑文档 | 解包 → 编辑 → 打包 | unpack.py / pack.py |
| 转换图像 | LibreOffice | soffice.py |

**使用示例**：

```bash
# 读取 Word 文档
pandoc document.docx -o output.md

# 编辑现有文档（3步）
python scripts/office/unpack.py document.docx unpacked/
# 编辑 unpacked/ 中的 XML 文件
python scripts/office/pack.py unpacked/ output.docx --original document.docx

# 创建新文档（使用 docx-js）
node create-document.js
```

#### pdf - PDF 文件处理

**功能概述**：
- 读取和提取文本、表格
- 合并、拆分、旋转页面
- 添加水印和注释
- 表单填充和 OCR

**核心库**：

```python
# pypdf - 基本操作
from pypdf import PdfReader, PdfWriter

# 合并 PDF
writer = PdfWriter()
for pdf in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)
writer.write("merged.pdf")

# pdfplumber - 提取内容
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    tables = pdf.pages[0].extract_tables()
```

#### pptx - PowerPoint 演示文稿

**功能概述**：
- 创建和编辑幻灯片
- 处理布局和主题
- 添加图表和媒体
- 演讲者备注

**使用示例**：

```bash
# 读取内容
python -m markitdown presentation.pptx

# 可视化预览
python scripts/thumbnail.py presentation.pptx

# 创建演示文稿
npm install -g pptxgenjs
node create-slides.js
```

#### xlsx - Excel 电子表格

**功能概述**：
- 创建和编辑电子表格
- 公式和数据分析
- 图表和可视化
- 数据导入导出

**核心库**：

```python
# openpyxl - Excel 操作
from openpyxl import Workbook, load_workbook

# 创建工作簿
wb = Workbook()
ws = wb.active
ws['A1'] = '标题'
ws['A2'] = 100
wb.save('data.xlsx')

# 读取工作簿
wb = load_workbook('data.xlsx')
ws = wb.active
value = ws['A2'].value
```

### 4.2 开发工具技能

#### skill-creator - 技能创建指南

**核心原则**：

1. **简洁性原则**
   - 上下文窗口是公共资源
   - 只添加 Claude 不知道的内容
   - 优先使用简洁示例

2. **自由度匹配原则**
   - 高自由度：文本指导
   - 中自由度：伪代码/参数化脚本
   - 低自由度：特定脚本

3. **渐进式披露原则**
   - 第1层：元数据（始终加载）
   - 第2层：SKILL.md（技能触发时）
   - 第3层：资源（按需加载）

**技能结构**：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML 前置元数据
│   └── Markdown 指导
└── 捆绑资源 (可选)
    ├── scripts/
    ├── references/
    └── assets/
```

#### mcp-builder - MCP 服务器开发

**MCP 开发4阶段**：

```
阶段 1: 深度研究和规划
  ├─ 理解 MCP 设计模式
  ├─ 学习 MCP 协议
  ├─ 研究框架文档
  └─ 规划实现

阶段 2: 实现
  ├─ 设置项目结构
  ├─ 实现核心基础设施
  ├─ 实现工具
  └─ 添加注解

阶段 3: 审查和测试
  ├─ 代码质量检查
  ├─ 构建和测试
  └─ 使用 MCP Inspector

阶段 4: 创建评估
  ├─ 创建评估��题
  ├─ 验证答案
  └─ 输出格式
```

**技术栈选择**：

| 语言 | 框架 | 传输 | 适用场景 |
|------|------|------|---------|
| TypeScript | MCP SDK | stdio/HTTP | 推荐，生态完善 |
| Python | FastMCP | stdio/HTTP | 快速开发 |

**工具命名规范**：

```
格式：{service}_{action}_{resource}

示例：
- slack_send_message
- github_create_issue
- jira_update_ticket
```

#### plugin-generator - 插件生成器

**支持的插件类型**：

1. **技能 (Skill)** - 工作流程和领域知识
2. **MCP 服务器** - 外部服务集成
3. **混合插件** - 技能 + MCP 服务器

**生成流程**：

```bash
# 生成简单技能
python scripts/generate_plugin.py   --type skill   --name my-skill   --description "技能描述"

# 生成 MCP 服务器
python scripts/generate_plugin.py   --type mcp   --name my-mcp   --language typescript

# 生成混合插件
python scripts/generate_plugin.py   --type hybrid   --name my-plugin
```

### 4.3 设计工具技能

#### theme-factory - 主题工厂

**10个预设主题**：

1. **arctic-frost** - 冰雪主题
2. **botanical-garden** - 植物主题
3. **desert-rose** - 沙漠主题
4. **forest-canopy** - 森林主题
5. **golden-hour** - 黄金时刻
6. **midnight-galaxy** - 午夜星空
7. **modern-minimalist** - 现代简约
8. **ocean-depths** - 海洋深处
9. **sunset-boulevard** - 日落大道
10. **tech-innovation** - 科技创新

**主题结构**：

```markdown
# 主题名称

## 颜色调色板
- 主色：#HEX - 用途
- 辅色：#HEX - 用途
- 强调色：#HEX - 用途

## 排版
- 标题字体：字体名称
- 正文字体：字体名称

## 最佳用途
适用场景列表
```

#### brand-guidelines - 品牌指南

**Anthropic 品牌色**：

**主要颜色**：
- Dark: `#141413` - 主要文本和深色背景
- Light: `#faf9f5` - 浅色背景
- Mid Gray: `#b0aea5` - 次要元素
- Light Gray: `#e8e6dc` - 细微背景

**强调色**：
- Orange: `#d97757` - 主要强调
- Blue: `#6a9bcc` - 次要强调
- Green: `#788c5d` - 第三强调

**字体**：
- 标题：Poppins（备用 Arial）
- 正文：Lora（备用 Georgia）

#### frontend-design - 前端设计

**设计原则**：

1. **独特性** - 创造独特的视觉风格
2. **生产级质量** - 高质量的代码和设计
3. **响应式** - 适配各种屏幕尺寸
4. **可访问性** - 符合 WCAG 标准

**技术栈**：
- React + TypeScript
- Tailwind CSS
- shadcn/ui 组件
- 现代 CSS 特性

