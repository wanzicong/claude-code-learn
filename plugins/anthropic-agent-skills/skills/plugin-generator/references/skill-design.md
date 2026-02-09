# 技能设计最佳实践

## 核心原则

### 1. 简洁性原则

**上下文窗口是公共资源** - 技能与其他内容共享上下文窗口，包括系统提示、对话历史和用户请求。

**假设 Claude 已经很聪明** - 只添加 Claude 不知道的内容。挑战每一条信息："Claude 真的需要这个解释吗？"

**优先使用简洁示例** - 用代码示例代替冗长的文字说明。

### 2. 自由度匹配原则

根据任务的脆弱性和可变性设置适当的自由度：

**高自由度（文本指令）**：
- 多种方法都有效
- 决策依赖上下文
- 启发式方法指导

**中自由度（伪代码/参数化脚本）**：
- 存在首选模式
- 允许一些变化
- 配置影响行为

**低自由度（特定脚本）**：
- 操作脆弱易错
- 一致性至关重要
- 必须遵循特定序列

### 3. 渐进式披露原则

技能使用三级加载系统管理上下文：

**第 1 级：元数据（名称 + 描述）** - 始终在上下文中（~100 词）
**第 2 级：SKILL.md 正文** - 技能触发时加载（<5k 词）
**第 3 级：捆绑资源** - 按需加载（无限制）

## SKILL.md 编写指南

### 前置元数据

```yaml
---
name: skill-name
description: 完整描述，包括功能和触发场景。这是主要触发机制，必须清晰全面。包括"何时使用"信息。
license: MIT (可选)
compatibility: 环境要求 (可选，很少需要)
---
```

**描述字段最佳实践**：
- 包含功能和使用场景
- 列出所有触发词和上下文
- 50-500 字符为宜
- 不要在正文中重复"何时使用"信息

### 正文结构

```markdown
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

### 编写风格

- **使用命令式/不定式形式** - "创建文件" 而非 "创建文件的方法"
- **保持简洁** - 正文控制在 500 行以内
- **使用代码示例** - 代码胜过千言万语
- **明确引用** - 引用文件时说明何时读取

## 目录结构设计

### 标准结构

```
skill-name/
├── SKILL.md                    # 必需
├── LICENSE.txt                 # 推荐
├── scripts/                    # 可选
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
├── references/                 # 可选
│   ├── workflows.md
│   ├── api_docs.md
│   └── examples.md
└── assets/                     # 可选
    ├── templates/
    └── config/
```

### 何时使用各个目录

**scripts/** - 可执行代码
- 重复编写的代码
- 需要确定性可靠性的操作
- 复杂的算法实现

**references/** - 参考文档
- API 文档
- 数据库模式
- 详细工作流程
- 领域知识

**assets/** - 输出资源
- 模板文件
- 图标和字体
- 样板代码
- 配置文件

## 渐进式披露模式

### 模式 1：高级指南 + 参考

适用于有多个高级功能的技能。

```markdown
# PDF 处理

## 快速开始
[核心示例]

## 高级功能
- **表单填充**: 详见 [FORMS.md](references/FORMS.md)
- **API 参考**: 详见 [REFERENCE.md](references/REFERENCE.md)
- **示例**: 详见 [EXAMPLES.md](references/EXAMPLES.md)
```

### 模式 2：域特定组织

适用于支持多个领域的��能。

```
bigquery-skill/
├── SKILL.md (概览和导航)
└── references/
    ├── finance.md (财务指标)
    ├── sales.md (销售数据)
    ├── product.md (产品使用)
    └── marketing.md (营销活动)
```

### 模式 3：框架/变体组织

适用于支持多个框架或实现方式的技能。

```
cloud-deploy/
├── SKILL.md (工作流 + 提供商选择)
└── references/
    ├── aws.md (AWS 部署模式)
    ├── gcp.md (GCP 部署模式)
    └── azure.md (Azure 部署模式)
```

### 模式 4：条件细节

适用于有基础和高级用法的技能。

```markdown
## 创建文档
使用 docx-js 创建新文档。详见 [DOCX-JS.md](references/DOCX-JS.md)。

## 编辑文档
简单编辑直接修改 XML。

**跟踪更改**: 详见 [REDLINING.md](references/REDLINING.md)
**OOXML 详情**: 详见 [OOXML.md](references/OOXML.md)
```

## 脚本设计指南

### 何时创建脚本

- 相同代码被重复编写
- 需要确定性执行
- 操作复杂易错
- 性能要求高

### 脚本最佳实践

```python
#!/usr/bin/env python3
"""
脚本用途的简短描述
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='脚本描述')
    parser.add_argument('--input', required=True, help='输入文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()

    # 验证输入
    if not Path(args.input).exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 执行主要逻辑
    try:
        result = process(args.input)
        save(result, args.output)
        print(f"成功: 输出已保存到 {args.output}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### 依赖管理

**requirements.txt**:
```
# 核心依赖
requests>=2.28.0
pyyaml>=6.0

# 可选依赖
pillow>=9.0.0  # 图像处理
```

## 参考文档设计

### 文档结构

**workflows.md** - 工作流程指南
```markdown
# 工作流程

## 基本工作流
1. 步骤 1
2. 步骤 2
3. 步骤 3

## 高级工作流
详细场景描述
```

**api_docs.md** - API 文档
```markdown
# API 文档

## 函数列表

### function_name(param1, param2)
功能描述

**参数**:
- param1: 参数说明
- param2: 参数说明

**返回**: 返回值说明

**示例**:
\`\`\`python
result = function_name("value1", "value2")
\`\`\`
```

**examples.md** - 使用示例
```markdown
# 使用示例

## 示例 1: 基本用法
[代码示例]

## 示例 2: 高级用法
[代码示例]
```

### 长文档组织

对于超过 100 行的参考文档，在顶部添加目录：

```markdown
# API 参考

## 目录
- [核心函数](#核心函数)
- [工具函数](#工具函数)
- [配置选项](#配置选项)

## 核心函数
...
```

## 资源文件设计

### 模板文件

将常用模板存储在 `assets/templates/`：

```
assets/
└── templates/
    ├── basic-template.html
    ├── advanced-template.html
    └── config-template.json
```

在 SKILL.md 中引用：
```markdown
使用基础模板：`assets/templates/basic-template.html`
```

### 配置文件

存储默认配置：

```
assets/
└── config/
    ├── default.json
    └── production.json
```

## 常见错误

### ❌ 错误做法

1. **描述过于简短**
```yaml
description: PDF 处理工具
```

2. **正文包含"何时使用"**
```markdown
## 何时使用此技能
当用户需要处理 PDF 时...
```

3. **过度解释基础概念**
```markdown
## 什么是 PDF
PDF 是便携式文档格式...
```

4. **深度嵌套引用**
```markdown
详见 A.md，其中引用 B.md，B.md 又引用 C.md
```

### ✅ 正确做法

1. **完整的描述**
```yaml
description: 全面的 PDF 处理工具，支持读取、编辑、合并、拆分、旋转、加水印、表单填充、加密解密和 OCR。当用户提到 .pdf 文件或要求处理 PDF 时使用。
```

2. **描述中包含触发信息**
```yaml
description: ... 当用户说"处理 PDF"、"合并文档"、"提取文本"或提供 .pdf 文件时使用此技能。
```

3. **简洁的正文**
```markdown
## 快速开始

提取文本：
\`\`\`python
python scripts/extract.py input.pdf output.txt
\`\`\`

详见 [REFERENCE.md](references/REFERENCE.md)
```

4. **扁平的引用结构**
```markdown
## 参考文档
- [workflows.md](references/workflows.md) - 工作流程
- [api_docs.md](references/api_docs.md) - API 文档
- [examples.md](references/examples.md) - 示例代码
```

## 性能优化

### 控制文件大小

- SKILL.md 正文 < 500 行
- 单个参考文档 < 1000 行
- 脚本文件 < 500 行

### 延迟加载

只在需要时加载大型参考文档：

```markdown
## 高级功能

**需要详细 API 文档时**: 读取 [API.md](references/API.md)
**需要完整示例时**: 读取 [EXAMPLES.md](references/EXAMPLES.md)
```

## 测试和验证

### 验证清单

- [ ] YAML 前置元数据格式正确
- [ ] 包含 name 和 description 字段
- [ ] 描述长度适中（50-500 字符）
- [ ] 正文结构清晰
- [ ] 脚本可执行且无错误
- [ ] 引用的文件都存在
- [ ] 目录结构符合规范

### 使用验证脚本

```bash
python scripts/validate_skill.py path/to/skill
```

## 版本控制

### 版本号规范

使用语义化版本：`MAJOR.MINOR.PATCH`

- MAJOR: 不兼容的 API 变更
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修正

### 更新日志

在 SKILL.md 中维护更新日志：

```markdown
## 更新日志

- **v1.2.0** (2026-02-07)
  - 新增功能 X
  - 改进功能 Y

- **v1.1.0** (2026-01-15)
  - 新增功能 Z

- **v1.0.0** (2026-01-01)
  - 初始版本
```

## 总结

优秀的技能设计遵循以下原则：

1. **简洁** - 只包含必要信息
2. **清晰** - 结构明确，易于理解
3. **实用** - 提供可执行的代码和工具
4. **高效** - 使用渐进式披露管理上下文
5. **可维护** - 良好的组织和文档

记住：技能是为 Claude 设计的，不是为人类设计的。专注于提供 Claude 需要的程序性知识和工具。
