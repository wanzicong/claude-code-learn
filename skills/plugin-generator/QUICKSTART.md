# 快速使用指南

## 通过 Claude Code 使用插件生成器

### 方式 1: 使用 /plugin 命令

当插件生成器技能已安装后，你可以直接通过对话使用：

```
用户: 帮我创建一个 PDF 水印技能
Claude: [自动调用 plugin-generator 技能生成]
```

### 方式 2: 直接命令行

```bash
# 进入技能目录
cd ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/plugin-generator

# 生成技能
python scripts/generate_plugin.py \
  --type skill \
  --name pdf-watermark \
  --description "为 PDF 文件添加水印的技能" \
  --output ~/my-plugins

# 验证技能
python scripts/validate_skill.py ~/my-plugins/pdf-watermark
```

## 常见使用场景

### 场景 1: 创建文档处理技能

```bash
python scripts/generate_plugin.py \
  --type skill \
  --name markdown-converter \
  --description "Markdown 格式转换工具，支持转换为 HTML、PDF、DOCX" \
  --output ./output
```

### 场景 2: 创建 API 集成 MCP 服务器

```bash
python scripts/generate_plugin.py \
  --type mcp \
  --name jira-integration \
  --description "Jira 问题跟踪系统集成" \
  --language typescript \
  --author "Your Name" \
  --output ./output
```

### 场景 3: 创建完整的混合插件

```bash
python scripts/generate_plugin.py \
  --type hybrid \
  --name data-pipeline \
  --description "数据处理管道，包含数据清洗技能和数据库 MCP 服务器" \
  --output ./output
```

## 生成后的步骤

### 1. 查看生成的文件

```bash
cd output/your-plugin-name
ls -la
```

### 2. 自定义实现

编辑生成的文件，添加你的具体实现：

**技能**:
- 编辑 `scripts/*.py` 添加功能代码
- 更新 `references/*.md` 添加详细文档
- 在 `assets/` 中添加模板和资源

**MCP 服务器**:
- 编辑 `src/tools/*.ts` 或 `src/tools/*.py` 实现工具
- 更新 `README.md` 添加使用说明
- 添加测试用例

### 3. 测试

**技能**:
```bash
python scripts/validate_skill.py path/to/skill
python scripts/main.py --input test.txt --output result.txt
```

**MCP 服务器**:
```bash
# TypeScript
npm install
npm run build
npm test

# Python
pip install -e .
pytest
```

### 4. 安装到本地

**技能**:
```bash
# 复制到本地市场
cp -r your-skill ~/.claude/plugins/marketplaces/local-skills/
```

**MCP 服务器**:
```bash
# 添加到 MCP 配置
# 编辑 ~/.claude/mcp_config.json
```

### 5. 发布（可选）

参考 [publishing.md](references/publishing.md) 发布到官方市场。

## 技巧和最佳实践

### 技巧 1: 使用描述性名称

```bash
# 好的名称
--name user-authentication
--name pdf-watermark
--name github-issue-tracker

# 不好的名称
--name tool1
--name my-plugin
--name test
```

### 技巧 2: 编写完整的描述

```bash
# 好的描述
--description "用户认证技能 - 提供 JWT、OAuth2、Session 等多种认证方式。当用户需要实现登录、注册、权限验证时使用。"

# 不好的描述
--description "认证工具"
```

### 技巧 3: 选择合适的类型

- **技能** - 提供工作流程、脚本、文档
- **MCP 服务器** - 集成外部 API 和服务
- **混合** - 需要两者结合时使用

### 技巧 4: 渐进式开发

1. 先生成基础结构
2. 实现核心功能
3. 添加测试
4. 完善文档
5. 优化性能

## 故障排除

### 问题 1: 生成失败

```bash
# 检查输出目录是否存在
mkdir -p output

# 检查 Python 版本
python --version  # 需要 3.7+

# 检查依赖
pip install -r scripts/requirements.txt
```

### 问题 2: 验证失败

```bash
# 查看详细错误
python scripts/validate_skill.py path/to/skill

# 常见问题：
# - YAML 前置元数据格式错误
# - 缺少必需字段
# - 文件引用不存在
```

### 问题 3: MCP 服务器无法启动

```bash
# TypeScript
npm install  # 安装依赖
npm run build  # 构建项目
node dist/index.js  # 测试运行

# Python
pip install -e .  # 安装包
python -m your_package  # 测试运行
```

## 示例项目

查看 [examples.md](references/examples.md) 获取完整的示例项目。

## 获取帮助

- 📖 阅读 [skill-design.md](references/skill-design.md) 了解技能设计
- 📖 阅读 [mcp-design.md](references/mcp-design.md) 了解 MCP 设计
- 📖 阅读 [publishing.md](references/publishing.md) 了解发布流程
- 💬 在 GitHub 上提交 Issue

## 下一步

1. 生成你的第一个插件
2. 自定义实现
3. 测试验证
4. 分享给社区

祝你开发愉快！🚀
