# Claude Code 插件生成器

智能生成 Claude Code 技能和 MCP 服务器插件的完整工具集。

## 功能特性

- 🎯 **智能需求分析** - 自动识别插件类型和架构
- 🏗️ **完整代码生成** - 生成可直接使用的实现代码
- 📝 **自动文档生成** - 创建完整的文档和示例
- ✅ **内置验证工具** - 确保插件质量
- 📦 **一键打包** - 生成可分发的插件包
- 🔧 **支持多种类型** - 技能、MCP 服务器、混合插件

## 支持的插件类型

### 技能 (Skills)
- 文档处理
- 代码生成
- 数据分析
- 工作流自动化

### MCP 服务器
- API 集成
- 数据库连接
- 外部服务集成
- 自定义工具

### 混合插件
- 技能 + MCP 服务器组合
- 完整的功能生态系统

## 快速开始

### 生成简单技能

```bash
python scripts/generate_plugin.py \
  --type skill \
  --name my-skill \
  --description "我的技能描述" \
  --output ./output
```

### 生成 MCP 服务器

```bash
# TypeScript
python scripts/generate_plugin.py \
  --type mcp \
  --name my-mcp \
  --description "我的 MCP 服务器" \
  --language typescript \
  --output ./output

# Python
python scripts/generate_plugin.py \
  --type mcp \
  --name my-mcp \
  --description "我的 MCP 服务器" \
  --language python \
  --output ./output
```

### 生成混合插件

```bash
python scripts/generate_plugin.py \
  --type hybrid \
  --name my-plugin \
  --description "我的混合插件" \
  --output ./output
```

## 命令行选项

```
--type          插件类型 (skill|mcp|hybrid)
--name          插件名称
--output        输出目录
--description   插件描述 (可选)
--language      MCP 服务器语言 (typescript|python，默认: typescript)
--author        作者名称 (可选)
--license       许可证 (默认: MIT)
```

## 验证插件

```bash
# 验证技能
python scripts/validate_skill.py path/to/skill

# 验证 MCP 服务器
cd path/to/mcp-server
npm test  # TypeScript
pytest    # Python
```

## 目录结构

```
plugin-generator/
├── SKILL.md                    # 技能定义
├── LICENSE.txt                 # 许可证
├── README.md                   # 本文件
├── scripts/                    # 生成和验证脚本
│   ├── generate_plugin.py      # 主生成脚本
│   └── validate_skill.py       # 验证脚本
├── references/                 # 参考文档
│   ├── skill-design.md         # 技能设计指南
│   ├── mcp-design.md           # MCP 设计指南
│   ├── publishing.md           # 发布指南
│   └── examples.md             # 示例集合
└── assets/                     # 模板和资源
    └── templates/              # 插件模板
```

## 工作流程

1. **需求分析** - 理解插件目的和功能
2. **类型识别** - 自动识别最适合的插件类型
3. **架构设计** - 基于最佳实践设计结构
4. **代码生成** - 生成完整的实现代码
5. **测试验证** - 运行测试确保质量
6. **打包分发** - 创建可分发的包

## 参考文档

- [技能设计最佳实践](references/skill-design.md)
- [MCP 服务器设计指南](references/mcp-design.md)
- [发布到市场指南](references/publishing.md)
- [完整示例集合](references/examples.md)

## 示例

查看 [examples.md](references/examples.md) 获取完整的示例代码。

## 贡献

欢迎贡献！请提交 Issue 或 Pull Request。

## 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)

## 支持

- 📖 [文档](references/)
- 💬 [GitHub Issues](https://github.com/your-repo/issues)
- 📧 联系作者

## 更新日志

### v1.0.0 (2026-02-07)
- 初始版本
- 支持技能、MCP 服务器和混合插件生成
- 完整的验证和测试工具
- 丰富的文档和示例
