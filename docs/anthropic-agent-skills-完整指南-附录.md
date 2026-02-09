# Anthropic Agent Skills 完整指南 - 附录部分

## 附录

### A. 常见问题 FAQ

#### Q1：技能和 MCP 有什么区别？

**A**：
- **Agent Skill**：教模型如何处理数据（提示词模板 + 脚本执行）
- **MCP**：连接模型与外部数据源（API 调用 + 数据查询）

**官方观点**：
> "MCP connects Claude to data. Skills teach Claude what to do with that data."

**选择指南**：
- 使用 Skill：简单脚本、本地逻辑、本地执行
- 使用 MCP：外部服务、数据库查询、实时数据

#### Q2：如何让技能自动触发？

**A**：
1. 编写清晰具体的 `description` 字段
2. 包含用户可能使用的关键词
3. 说明何时应该使用该技能
4. 使用第三人称："This skill should be used when..."

**示例**：
```yaml
description: |
  全面的 PDF 处理工具，支持读取、编辑、合并、拆分、旋转、
  加水印、表单填充、加密解密和 OCR。当用户提到 .pdf 文件
  或要求处理 PDF 时使用。
```

#### Q3：技能文件应该放在哪里？

**A**：
- **用户级**：`~/.claude/skills/技能名称/`
- **项目级**：`your-project/.claude/skills/技能名称/`

**优先级**：项目级技能 > 用户级技能

#### Q4：如何在技能中使用大型文档？

**A**：
1. 将文档放在 `references/` 目录
2. 在 SKILL.md 中指定何时读取
3. 使用条件加载避免不必要的 Token 消耗

**示例**：
```markdown
## 财务规则

如果用户提到预算或成本，读取 [财务规则](references/finance.md)
```

#### Q5：脚本内容会被模型读取吗？

**A**：不会。脚本只会被执行，内容不会被加载到上下文中，这样可以节省 Token。

#### Q6：如何测试技能是否正常工作？

**A**：
1. 使用验证脚本：`python validate_skill.py /path/to/skill`
2. 在 Claude Code 中手动测试
3. 检查技能是否自动触发
4. 验证输出是否符合预期

#### Q7：技能可以调用其他技能吗？

**A**：可以。Claude 会根据需要自动选择和组合多个技能。

#### Q8：如何更新已有的技能？

**A**：
1. 编辑 SKILL.md 文件
2. 更新 references/ 或 scripts/ 中的内容
3. 更新版本号（可选）
4. 运行验证脚本确保格式正确
5. 重新加载 Claude Code

#### Q9：技能的 Token 消耗如何计算？

**A**：
- **元数据层**：所有技能的 name + description（~2k tokens，始终加载）
- **指令层**：单个技能的 SKILL.md（~3-5k tokens，触发时加载）
- **资源层**：references/（按需加载，脚本不计入）

#### Q10：如何调试技能不触发的问题？

**A**：
1. 检查 `description` 是否包含相关关键词
2. 验证 SKILL.md 文件格式是否正确
3. 确认技能目录位置正确
4. 使用显式调用测试：`/技能名称 任务描述`
5. 查看 Claude Code 日志

---

### B. 技能模板

#### 基础技能模板

```markdown
---
name: skill-name
description: |
  技能的完整描述，包括功能、使用场景和触发关键词。
  当用户提到 [关键词] 时使用此技能。
version: 1.0.0
license: MIT
---

# 技能标题

## 概述
简要说明技能用途（1-2 段）

## 快速开始
最常见用例的简洁示例

```bash
# 命令示例
command --option value
```

## 核心功能
- 功能 1：说明
- 功能 2：说明
- 功能 3：说明

## 高级用法
复杂场景的处理方法

## 参考文档
- [API 文档](references/api.md)
- [示例代码](references/examples.md)
```

#### 带脚本的技能模板

```markdown
---
name: skill-with-scripts
description: |
  包含可执行脚本的技能示例。
---

# 技能标题

## 使用脚本

执行主��本：
```bash
python scripts/main.py --input file.txt --output result.txt
```

查看帮助：
```bash
python scripts/main.py --help
```

## 脚本说明
- `main.py`：主要功能
- `utils.py`：工具函数
- `requirements.txt`：依赖列表
```

#### 复杂技能模板

```markdown
---
name: complex-skill
description: |
  复杂技能示例，包含多个模块和详细文档。
---

# 技能标题

## 导航
- [快速开始](#快速开始)
- [核心概念](#核心概念)
- [使用指南](#使用指南)
- [参考文档](#参考文档)

## 快速开始
5 分钟入门指南

## 核心概念
必须理解的关键概念

## 使用指南

### 场景 1：基础用法
基础场景说明

### 场景 2：高级用法
**需要详细文档时**：读取 [高级指南](references/advanced.md)

## 参考文档
- [API 参考](references/api.md)
- [工作流程](references/workflows.md)
- [示例代码](references/examples.md)
- [最佳实践](references/best_practices.md)
```

---

### C. 脚本示例

#### Python 脚本模板

```python
#!/usr/bin/env python3
"""
脚本用途的简短描述

用法：
    python script.py --input file.txt --output result.txt

示例：
    python script.py --input data.csv --output report.pdf
"""

import argparse
import sys
from pathlib import Path

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='脚本描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 参数定义
    parser.add_argument(
        '--input',
        required=True,
        help='输入文件路径'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='输出文件路径'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )

    args = parser.parse_args()

    # 验证输入
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 执行主要逻辑
    try:
        result = process(input_path, args.verbose)
        save_result(result, args.output)
        print(f"成功：输出已保存到 {args.output}")
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

def process(input_path, verbose=False):
    """处理逻辑"""
    if verbose:
        print(f"处理文件: {input_path}")

    # 实现处理逻辑
    with open(input_path, 'r') as f:
        content = f.read()

    # 处理内容
    result = content.upper()  # 示例：转换为大写

    return result

def save_result(result, output_path):
    """保存结果"""
    with open(output_path, 'w') as f:
        f.write(result)

if __name__ == '__main__':
    main()
```

#### Bash 脚本模板

```bash
#!/bin/bash
# 脚本用途的简短描述

set -e  # 遇到错误立即退出
set -u  # 使用未定义变量时报错

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：打印错误信息
error() {
    echo -e "${RED}错误: $1${NC}" >&2
    exit 1
}

# 函数：打印成功信息
success() {
    echo -e "${GREEN}成功: $1${NC}"
}

# 函数：打印警告信息
warning() {
    echo -e "${YELLOW}警告: $1${NC}"
}

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <input_file> <output_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

# 验证输入文件
if [ ! -f "$INPUT_FILE" ]; then
    error "输入文件不存在: $INPUT_FILE"
fi

# 执行主要逻辑
echo "处理文件: $INPUT_FILE"

# 示例：复制文件
cp "$INPUT_FILE" "$OUTPUT_FILE" || error "复制文件失败"

success "输出已保存到 $OUTPUT_FILE"
```

---

### D. 参考资源

#### 官方文档

- **Claude Code 文档**：https://docs.anthropic.com/claude-code
- **MCP 协议文档**：https://modelcontextprotocol.io
- **Anthropic API 文档**：https://docs.anthropic.com

#### 技能市场

- **Anthropic 官方技能**：https://github.com/anthropics/anthropic-agent-skills
- **社区技能**：https://github.com/topics/claude-skills

#### 开发工具

- **技能验证工具**：validate_skill.py
- **技能初始化工具**：init_skill.py
- **技能打包工具**：package_skill.py

#### 相关库和框架

**Python**：
- `pypdf`：PDF 处理
- `python-docx`：Word 文档处理
- `openpyxl`：Excel 处理
- `pyyaml`：YAML 解析

**JavaScript/TypeScript**：
- `docx`：Word 文档创建
- `pptxgenjs`：PowerPoint 创建
- `pdf-lib`：PDF 处理

**MCP 开发**：
- `@modelcontextprotocol/sdk`：TypeScript MCP SDK
- `fastmcp`：Python MCP 框架

#### 学习资源

- **技能创建指南**：skill-creator 技能
- **MCP 开发指南**：mcp-builder 技能
- **插件生成器**：plugin-generator 技能

---

### E. 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| **技能** | Skill | 为 Claude 添加专业知识和工作流程的扩展 |
| **MCP** | Model Context Protocol | 连接 LLM 与外部数据源的开放协议 |
| **提示词** | Prompt | 给 AI 的指令和上下文 |
| **上下文窗口** | Context Window | AI 一次能处理的文本量 |
| **Token** | Token | 文本的基本单位，用于计算成本 |
| **元数据** | Metadata | 描述数据的数据（如技能的 name 和 description） |
| **YAML** | YAML | 一种人类可读的数据序列化格式 |
| **Markdown** | Markdown | 一种轻量级标记语言 |
| **渐进式披露** | Progressive Disclosure | 按需显示信息的设计原则 |
| **按需加载** | Lazy Loading | 只在需要时加载资源 |
| **工作流程** | Workflow | 完成任务的步骤序列 |
| **脚本** | Script | 可执行的程序文件 |
| **参考文档** | Reference | 详细的技术文档 |
| **资源** | Asset | 静态文件（模板、图片、配置等） |
| **触发词** | Trigger | 激活技能的关键词 |
| **自由度** | Degree of Freedom | 任务执行的灵活性程度 |

---

## 总结

Anthropic Agent Skills 是一个强大的扩展机制，通过以下特点实现高效的 AI 增强：

### 核心优势

1. **三层按需加载** ✅
   - 元信息 → 指令 → 资源
   - 节省 Token，提高效率

2. **自动触发机制** ✅
   - 基于 description 的智能匹配
   - 无需手动调用

3. **模块化设计** ✅
   - 清晰的目录结构
   - 易于维护和扩展

4. **灵活扩展** ✅
   - 支持脚本、文档和资源
   - 可与 MCP 配合使用

### 最佳实践总结

1. **简洁性** - 只包含必要信息
2. **自由度匹配** - 根据任务选择合适的实现方式
3. **渐进式披露** - 分层组织内容
4. **性能优化** - 控制文件大小，延迟加载
5. **安全考虑** - 验证输入，保护敏感数据
6. **持续维护** - 定期更新，收集反馈

### 快速参考

**创建技能**：
```bash
mkdir -p ~/.claude/skills/my-skill
# 创建 SKILL.md
# 添加脚本和资源
# 测试和验证
```

**安装技能**：
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**调用技能**：
```
# 自动触发
"帮我处理这个 PDF 文件"

# 显式调用
/pdf 合并这两个文档
```

### 下一步

1. **探索现有技能** - 学习官方技能的设计
2. **创建自己的技能** - 从简单技能开始
3. **分享技能** - 贡献到社区
4. **持续学习** - 关注最新的最佳实践

---

**文档版本**：1.0.0
**最后更新**：2024年
**作者**：基于 Anthropic Agent Skills 探索整理
**许可证**：MIT

---

## 反馈和贡献

如果你发现文档中的错误或有改进建议，欢迎：
- 提交 Issue
- 发起 Pull Request
- 分享你的技能创建经验

祝你在使用 Anthropic Agent Skills 的过程中取得成功！🎉
