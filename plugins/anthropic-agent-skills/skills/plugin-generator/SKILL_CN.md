---
name: plugin-generator
description: Claude Code 插件生成器 - 智能生成 Claude Code 技能(.skill)和 MCP 服务器插件。支持完整的插件开发工作流：需求分析、架构设计、代码生成、测试和打包。当用户说"创建插件"、"生成技能"、"开发 MCP 服务器"、"制作 Claude Code 插件"、"plugin"、"skill"、"MCP"或提供插件需求描述时使用此技能。自动识别插件类型（技能/MCP/混合），生成完整的项目结构、配置文件、实现代码、文档和测试。
---

# Claude Code 插件生成器

## 概述

这是一个智能插件生成器，能够为 Claude Code 创建高质量的技能和 MCP 服务器插件。支持完整的开发生命周期，从需求分析到打包分发。

## 核心功能

1. **智能需求分析** - 通过对话理解用户需求，自动识别插件类型
2. **架构设计** - 基于最佳实践设计插件结构
3. **代码生成** - 生成完整的实现代码、配置和文档
4. **自动测试** - 生成测试用例并验证功能
5. **打包分发** - 创建可分发的 .skill 文件或 MCP 服务器包

## 工作流程

### 阶段 1: 需求理解

通过以下问题理解用户需求：

1. **插件目的** - 这个插件要解决什么问题？
2. **使用场景** - 用户会在什么情况下使用？提供 2-3 个具体示例
3. **输入输出** - 需要什么输入？产生什么输出？
4. **外部依赖** - 是否需要调用外部 API 或服务？
5. **特殊要求** - 是否有性能、安全或兼容性要求？

### 阶段 2: 插件类型识别

基于需求自动识别插件类型：

**技能 (Skill)**:
- 提供工作流程指导和领域知识
- 包含脚本、参考文档和资源
- 示例：文档处理、代码生成、设计工具

**MCP 服务器**:
- 集成外部服务和 API
- 提供工具接口供 Claude 调用
- 示例：GitHub、Notion、Slack 集成

**混合插件**:
- 同时包含技能和 MCP 服务器
- 技能提供工作流，MCP 提供工具
- 示例：Notion 插件（技能 + MCP 服务器）

### 阶段 3: 架构设计

根据插件类型设计架构：

#### 技能架构

```
skill-name/
├── SKILL.md                    # 技能定义
├── LICENSE.txt                 # 许可证
├── scripts/                    # 可执行脚本
│   ├── main.py                 # 主要功能脚本
│   ├── utils.py                # 工具函数
│   └── requirements.txt        # Python 依赖
├── references/                 # 参考文档
│   ├── api_docs.md            # API 文档
│   ├── workflows.md           # 工作流程
│   └── examples.md            # 示例代码
└── assets/                     # 输出资源
    ├── templates/             # 模板文件
    └── config/                # 配置文件
```

#### MCP 服务器架构

**TypeScript (推荐)**:
```
mcp-server-name/
├── .claude-plugin/
│   ├── plugin.json            # 插件元数据
│   └── .mcp.json              # MCP 配置
├── package.json               # Node.js 配置
├── tsconfig.json              # TypeScript 配置
├── src/
│   ├── index.ts               # 入口文件
│   ├── tools/                 # 工具实现
│   │   ├── tool1.ts
│   │   └── tool2.ts
│   ├── resources/             # 资源实现
│   └── types.ts               # 类型定义
├── tests/                     # 测试文件
│   ├── tools.test.ts
│   └── integration.test.ts
├── README.md                  # 使用文档
└── LICENSE                    # 许可证
```

**Python**:
```
mcp-server-name/
├── .claude-plugin/
│   ├── plugin.json
│   └── .mcp.json
├── pyproject.toml             # Python 项目配置
├── src/
│   └── mcp_server_name/
│       ├── __init__.py
│       ├── server.py          # 服务器实现
│       ├── tools/             # 工具实现
│       └── resources/         # 资源实现
├── tests/
│   └── test_server.py
├── README.md
└── LICENSE
```

### 阶段 4: 实现生成

使用 `scripts/generate_plugin.py` 生成完整实现：

```bash
python scripts/generate_plugin.py --type [skill|mcp|hybrid] --name <plugin-name> --output <output-dir>
```

生成内容包括：

1. **配置文件** - package.json, SKILL.md, plugin.json 等
2. **核心代码** - 完整的功能实现
3. **测试代码** - 单元测试和集成测试
4. **文档** - README, API 文档, 使用示例
5. **资源文件** - 模板、配置、资源

### 阶段 5: 测试验证

#### 技能测试

1. **语法验证** - 检查 SKILL.md 格式
2. **脚本测试** - 运行所有脚本确保无错误
3. **文档检查** - 验证参考文档完整性

使用验证脚本：
```bash
python scripts/validate_skill.py <skill-path>
```

#### MCP 服务器测试

1. **构建测试** - 编译/构建项目
2. **单元测试** - 测试各个工具函数
3. **集成测试** - 测试完整工作流
4. **MCP Inspector** - 使用官方工具验证

使用测试脚本：
```bash
# TypeScript
npm test
npm run build

# Python
pytest tests/
python -m build
```

### 阶段 6: 打包分发

#### 技能打包

使用官方打包工具：
```bash
python scripts/package_skill.py <skill-path> <output-dir>
```

输出：`<skill-name>.skill` 文件

#### MCP 服务器打包

**TypeScript**:
```bash
npm run build
npm pack
```

**Python**:
```bash
python -m build
```

### 阶段 7: 安装和发布

#### 本地安装

**技能**:
```bash
# 复制到本地市场
cp <skill-name>.skill ~/.claude/plugins/marketplaces/local-skills/
```

**MCP 服务器**:
```bash
# 添加到 MCP 配置
# 编辑 ~/.claude/mcp_config.json
```

#### 发布到市场

1. **创建 GitHub 仓库**
2. **添加市场元数据** - 创建 `.claude-plugin/marketplace.json`
3. **提交 PR** - 提交到官方市场仓库
4. **等待审核** - 官方团队审核后合并

详见 `references/publishing.md`

## 快速开始

### 示例 1: 创建简单技能

```bash
# 生成 PDF 水印技能
python scripts/generate_plugin.py \
  --type skill \
  --name pdf-watermark \
  --description "为 PDF 文件添加水印" \
  --output ./output
```

### 示例 2: 创建 MCP 服务器

```bash
# 生成 Jira 集成 MCP 服务器
python scripts/generate_plugin.py \
  --type mcp \
  --name jira-mcp \
  --description "Jira 问题跟踪集成" \
  --language typescript \
  --output ./output
```

### 示例 3: 创建混合插件

```bash
# 生成数据分析插件（技能 + MCP）
python scripts/generate_plugin.py \
  --type hybrid \
  --name data-analysis \
  --description "数据分析和可视化" \
  --output ./output
```

## 高级功能

### 自定义模板

在 `assets/templates/` 中创建自定义模板：

- `skill-template/` - 技能模板
- `mcp-typescript-template/` - TypeScript MCP 模板
- `mcp-python-template/` - Python MCP 模板

### 插件配置

使用 `references/plugin-config.md` 了解所有配置选项。

### 最佳实践

参考 `references/best-practices.md` 了解：

- 技能设计原则
- MCP 服务器设计模式
- 性能优化建议
- 安全性考虑
- 错误处理策略

## 参考文档

- **[workflows.md](references/workflows.md)** - 详细工作流程指南
- **[skill-design.md](references/skill-design.md)** - 技能设计最佳实践
- **[mcp-design.md](references/mcp-design.md)** - MCP 服务器设计指南
- **[plugin-config.md](references/plugin-config.md)** - 插件配置参考
- **[testing.md](references/testing.md)** - 测试策略和工具
- **[publishing.md](references/publishing.md)** - 发布到市场指南
- **[examples.md](references/examples.md)** - 完整示例集合

## 故障排除

### 常见问题

1. **SKILL.md 验证失败** - 检查 YAML 前置元数据格式
2. **脚本执行错误** - 确保安装了所有依赖
3. **MCP 服务器无法启动** - 检查配置文件和端口
4. **打包失败** - 验证目录结构和文件完整性

详见 `references/troubleshooting.md`

## 支持的插件类型

### 技能类型

- **文档处理** - PDF, DOCX, XLSX, PPTX
- **代码生成** - 前端、后端、全栈
- **设计工具** - UI/UX、图形设计
- **数据分析** - 数据处理、可视化
- **工作流程** - 自动化、集成

### MCP 服务器类型

- **项目管理** - Jira, Linear, Asana
- **版本控制** - GitHub, GitLab, Bitbucket
- **通信** - Slack, Discord, Teams
- **数据库** - Supabase, Firebase, MongoDB
- **云服务** - AWS, GCP, Azure
- **设计** - Figma, Sketch
- **支付** - Stripe, PayPal
- **监控** - Sentry, DataDog

## 许可证

MIT License - 详见 LICENSE.txt

## 贡献

欢迎贡献！请参考 `references/contributing.md`

## 更新日志

- **v1.0.0** (2026-02-07) - 初始版本
  - 支持技能和 MCP 服务器生成
  - 完整的测试和打包工具
  - 丰富的模板和示例
