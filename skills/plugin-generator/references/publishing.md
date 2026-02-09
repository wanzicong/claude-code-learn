# 发布到 Claude Code 市场指南

## 概述

本指南介绍如何将你的插件发布到 Claude Code 官方市场或第三方市场。

## 发布前准备

### 1. 完整性检查

确保你的插件包含所有必要文件：

**技能插件**:
- [ ] SKILL.md（包含正确的 YAML 前置元数据）
- [ ] LICENSE.txt
- [ ] 所有引用的脚本和资源文件
- [ ] README.md（可选但推荐）

**MCP 服务器插件**:
- [ ] .claude-plugin/plugin.json
- [ ] .claude-plugin/.mcp.json
- [ ] 源代码文件
- [ ] package.json 或 pyproject.toml
- [ ] README.md
- [ ] LICENSE

### 2. 质量验证

**技能验证**:
```bash
python scripts/validate_skill.py path/to/skill
```

**MCP 服务器验证**:
```bash
# TypeScript
npm run build
npm test

# Python
python -m build
pytest
```

**MCP Inspector 测试**:
```bash
mcp-inspector node dist/index.js
# 或
mcp-inspector python -m your_package
```

### 3. 文档完善

确保 README.md 包含：
- 清晰的功能描述
- 安装说明
- 使用示例
- 配置说明
- 故障排除

### 4. 版本号

使用语义化版本号：`MAJOR.MINOR.PATCH`

```json
{
  "version": "1.0.0"
}
```

## 发布到官方市场

### 方式 1: 提交到现有市场

#### Claude 官方市场

1. **Fork 仓库**
```bash
# Fork https://github.com/anthropics/claude-plugins-official
git clone https://github.com/YOUR_USERNAME/claude-plugins-official.git
cd claude-plugins-official
```

2. **添加插件**
```bash
# 创建插件目录
mkdir -p plugins/your-plugin-name

# 复制插件文件
cp -r /path/to/your/plugin/* plugins/your-plugin-name/
```

3. **更新市场元数据**

编辑 `.claude-plugin/marketplace.json`：

```json
{
  "name": "claude-plugins-official",
  "plugins": [
    {
      "name": "your-plugin-name",
      "description": "你的插件描述",
      "version": "1.0.0",
      "author": {
        "name": "你的名字",
        "email": "your@email.com"
      },
      "source": "./plugins/your-plugin-name",
      "category": "development",
      "tags": ["github", "git", "version-control"],
      "homepage": "https://github.com/your/repo"
    }
  ]
}
```

4. **提交 Pull Request**
```bash
git checkout -b add-your-plugin
git add .
git commit -m "Add your-plugin-name plugin"
git push origin add-your-plugin
```

然后在 GitHub 上创建 Pull Request。

#### Anthropic Skills 市场

类似流程，但提交到：
```bash
git clone https://github.com/anthropics/skills.git
```

### 方式 2: 创建独立仓库

如果你的插件较大或需要独立维护：

1. **创建 GitHub 仓库**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/your-plugin.git
git push -u origin main
```

2. **添加市场元数据**

创建 `.claude-plugin/marketplace.json`：

```json
{
  "name": "your-marketplace",
  "owner": {
    "name": "你的名字",
    "email": "your@email.com"
  },
  "metadata": {
    "description": "你的插件市场",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "your-plugin",
      "description": "插件描述",
      "version": "1.0.0",
      "author": {
        "name": "你的名字"
      },
      "source": "./",
      "license": "MIT"
    }
  ]
}
```

3. **发布 Release**

在 GitHub 上创建 Release：
- Tag: `v1.0.0`
- Title: `v1.0.0 - Initial Release`
- Description: 更新日志

4. **提交到官方市场列表**

创建 PR 将你的仓库添加到官方市场列表。

## 发布到第三方市场

### Superpowers Marketplace

1. **Fork 仓库**
```bash
git clone https://github.com/obra/superpowers-marketplace.git
```

2. **添加插件**

按照市场的目录结构添加你的插件。

3. **提交 PR**

## 本地市场发布

### 创建本地市场

1. **创建市场目录**
```bash
mkdir -p ~/.claude/plugins/marketplaces/my-local-market
cd ~/.claude/plugins/marketplaces/my-local-market
```

2. **创建市场配置**

创建 `.claude-plugin/marketplace.json`：

```json
{
  "name": "my-local-market",
  "owner": {
    "name": "Local User"
  },
  "metadata": {
    "description": "我的本地插件市场",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "我的插件",
      "source": "./plugins/my-plugin",
      "version": "1.0.0"
    }
  ]
}
```

3. **添加插件**
```bash
mkdir -p plugins/my-plugin
cp -r /path/to/plugin/* plugins/my-plugin/
```

4. **注册市场**

编辑 `~/.claude/plugins/known_marketplaces.json`：

```json
{
  "my-local-market": {
    "source": {
      "source": "local",
      "path": "/Users/username/.claude/plugins/marketplaces/my-local-market"
    },
    "installLocation": "/Users/username/.claude/plugins/marketplaces/my-local-market",
    "lastUpdated": "2026-02-07T00:00:00.000Z"
  }
}
```

## 插件打包

### 技能打包

使用官方打包工具：

```bash
python scripts/package_skill.py path/to/skill output/directory
```

输出：`skill-name.skill` 文件（实际上是 ZIP 文件）

### MCP 服务器打包

**TypeScript**:
```bash
npm run build
npm pack
```

输出：`package-name-1.0.0.tgz`

**Python**:
```bash
python -m build
```

输出：`dist/package-name-1.0.0.tar.gz` 和 `.whl` 文件

## 版本管理

### 语义化版本

- **MAJOR** (1.0.0): 不兼容的 API 变更
- **MINOR** (0.1.0): 向后兼容的功能新增
- **PATCH** (0.0.1): 向后兼容的问题修正

### 更新日志

在 README.md 或 CHANGELOG.md 中维护：

```markdown
## 更新日志

### [1.1.0] - 2026-02-07
#### 新增
- 添加批量处理功能
- 支持自定义配置

#### 改进
- 优化性能
- 改进错误提示

#### 修复
- 修复文件路径问题
- 修复编码错误

### [1.0.0] - 2026-01-01
- 初始版本
```

## 持续集成

### GitHub Actions

创建 `.github/workflows/test.yml`：

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Test
        run: npm test

      - name: Validate
        run: npm run validate
```

### 自动发布

创建 `.github/workflows/release.yml`：

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Package
        run: npm pack

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false

      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./package.tgz
          asset_name: package.tgz
          asset_content_type: application/gzip
```

## 推广和维护

### 文档网站

使用 GitHub Pages 创建文档网站：

1. 创建 `docs/` 目录
2. 添加 `docs/index.md`
3. 在仓库设置中启用 GitHub Pages

### 社区支持

- 创建 GitHub Discussions
- 添加 CONTRIBUTING.md
- 设置 Issue 模板
- 回应用户反馈

### 监控使用

跟踪插件使用情况：
- GitHub Stars
- 下载次数
- Issue 和 PR 数量
- 用户反馈

## 审核标准

官方市场的审核标准：

### 功能性
- [ ] 插件功能正常工作
- [ ] 没有明显的 bug
- [ ] 错误处理完善

### 代码质量
- [ ] 代码结构清晰
- [ ] 遵循最佳实践
- [ ] 有适当的注释

### 文档
- [ ] README 完整
- [ ] 使用示例清晰
- [ ] API 文档完善

### 安全性
- [ ] 没有安全漏洞
- [ ] 凭证管理安全
- [ ] 输入验证完善

### 许可证
- [ ] 包含许可证文件
- [ ] 许可证与依赖兼容

## 常见问题

### Q: 插件被拒绝了怎么办？

A: 查看审核反馈，修复问题后重新提交。

### Q: 如何更新已发布的插件？

A: 更新版本号，提交新的 PR 或创建新的 Release。

### Q: 可以发布私有插件吗？

A: 可以，使用本地市场或私有 GitHub 仓库。

### Q: 如何处理用户反馈？

A: 在 GitHub Issues 中跟踪，及时回应和修复。

## 检查清单

发布前最终检查：

- [ ] 所有测试通过
- [ ] 文档完整
- [ ] 版本号正确
- [ ] 许可证文件存在
- [ ] README 包含安装和使用说明
- [ ] 没有敏感信息（API 密钥等）
- [ ] 代码格式化
- [ ] 依赖版本固定
- [ ] 更新日志完整
- [ ] 示例代码可运行

## 资源链接

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [官方插件市场](https://github.com/anthropics/claude-plugins-official)
- [官方技能市场](https://github.com/anthropics/skills)
- [Superpowers 市场](https://github.com/obra/superpowers-marketplace)
- [MCP 协议文档](https://modelcontextprotocol.io)

## 总结

发布插件的关键步骤：

1. **准备** - 确保插件完整且经过测试
2. **验证** - 使用验证工具检查质量
3. **文档** - 编写清晰的文档
4. **提交** - 选择合适的市场提交
5. **维护** - 持续改进和支持用户

祝你的插件发布成功！
