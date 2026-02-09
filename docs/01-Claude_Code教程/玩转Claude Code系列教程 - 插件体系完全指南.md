# 🔌 玩转 Claude Code 系列教程 — 插件体系完全指南

> **一句话概括**：本篇全面深入地介绍 Claude Code 插件体系，从理论基础到实战开发，从使用技巧到高级定制，助你掌握插件开发的方方面面。

---

## 一、总述

Claude Code 插件系统是一种将 **Skills、Hooks、Subagents、MCP 服务器** 打包成可分发单元的机制。通过插件，你可以：

- 📦 **打包分发**：将相关功能打包，一键安装
- 🔄 **版本管理**：独立的版本控制和更新
- 👥 **团队共享**：团队内部发布和复用
- 🌐 **公开发布**：发布到插件市场
- ⚡ **按需加载**：只在需要时激活

### 插件 vs 扩展机制对比

| 特性 | Skills | Hooks | Subagents | MCP | 插件 |
|------|--------|-------|-----------|-----|------|
| 可打包 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 版本管理 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 命名空间 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 依赖管理 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 一键安装 | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 二、插件理论基础

### 2.1 插件架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Claude Code                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   插件系统核心                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │  │
│  │  │ 插件加载器   │  │ 命名空间管理 │  │ 依赖解析器     │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                      插件实例                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │ Skills/      │  │ Hooks/       │  │ Subagents/  │  │  │
│  │  │ commands/    │  │ settings.json │  │ *.md        │  │  │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │  │
│  │  ┌──────────────┐                                       │  │
│  │  │ plugin.json  │ ← 插件清单文件                        │  │
│  │  └──────────────┘                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 插件目录结构

```
my-plugin/
├── plugin.json              # 插件清单（必需）
├── README.md                # 插件文档
├── CHANGELOG.md             # 变更日志
├── skills/                  # 技能目录
│   └── <skill-name>/
│       └── SKILL.md
├── commands/                # 命令目录（兼容旧版）
│   └── <command-name>.md
├── agents/                  # 子代理目录
│   └── <agent-name>.md
├── hooks/                   # 钩子目录
│   └── settings.json        # 钩子配置
├── mcp/                     # MCP 配置
│   └── mcp-servers.json     # MCP 服务器列表
├── rules/                   # 规则目录
│   └── <rule-name>.md
├── resources/               # 资源目录
│   ├── templates/           # 模板文件
│   ├── examples/            # 示例文件
│   └── scripts/             # 脚本文件
└── package.json             # NPM 包信息（可选）
```

### 2.3 plugin.json 清单文件

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin",
  "name": "my-plugin",
  "version": "1.0.0",
  "displayName": "我的插件",
  "description": "这是一个示例插件",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "publisher": "your-publisher",
  "license": "MIT",
  "homepage": "https://github.com/yourname/my-plugin",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourname/my-plugin.git"
  },
  "bugs": {
    "url": "https://github.com/yourname/my-plugin/issues"
  },
  "keywords": ["claude-code", "plugin", "example"],
  "categories": ["Development Tools", "Productivity"],
  "icon": "icon.png",
  "preview": false,
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "contributes": {
    "skills": ["skills/*"],
    "agents": ["agents/*"],
    "hooks": "hooks/settings.json",
    "mcpServers": "mcp/mcp-servers.json",
    "rules": ["rules/*"]
  },
  "activation": {
    "events": ["onLanguage:typescript", "onCommand:my-plugin.activate"]
  },
  "dependencies": {
    "another-plugin": "^1.0.0"
  },
  "settings": {
    "myPlugin.apiKey": {
      "type": "string",
      "description": "API 密钥",
      "secret": true,
      "default": ""
    },
    "myPlugin.maxRetries": {
      "type": "number",
      "description": "最大重试次数",
      "default": 3,
      "minimum": 1,
      "maximum": 10
    }
  }
}
```

---

## 三、插件开发实战

### 3.1 创建第一个插件

#### 插件构思

创建一个 **Python 开发助手插件**，包含以下功能：
- Python 代码风格检查
- Django/Flask 项目生成器
- Python 文档生成
- 常用代码片段

#### 创建项目结构

```bash
# 创建插件目录
mkdir python-dev-assistant
cd python-dev-assistant

# 创建目录结构
mkdir -p skills agents hooks mcp resources/templates

# 初始化 npm 包（用于版本管理）
npm init -y
```

#### 编写 plugin.json

```json
{
  "name": "python-dev-assistant",
  "version": "1.0.0",
  "displayName": "Python 开发助手",
  "description": "Python 开发必备工具集：代码检查、项目生成、文档生成",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["python", "django", "flask", "development"],
  "categories": ["Programming Languages", "Development Tools"],
  "contributes": {
    "skills": ["skills/*"],
    "agents": ["agents/*"]
  },
  "settings": {
    "pythonDevAssistant.defaultFramework": {
      "type": "string",
      "enum": ["django", "fastapi", "flask"],
      "description": "默认框架",
      "default": "fastapi"
    },
    "pythonDevAssistant.pythonVersion": {
      "type": "string",
      "description": "Python 版本",
      "default": "3.11"
    }
  }
}
```

#### 创建技能：代码风格检查

```yaml
# skills/pylint-check/SKILL.md
---
name: pylint-check
description: 使用 pylint 检查 Python 代码风格和质量
argument-hint: [file-or-directory]
allowed-tools: Bash(pylint *), Read, Glob
---

# Python 代码风格检查

使用 pylint 检查 $ARGUMENTS 的代码质量。

## 检查内容

1. **代码风格**：PEP 8 规范
2. **错误检测**：语法错误、未定义变量
3. **代码异味**：重复代码、过于复杂
4. **命名规范**：变量、函数、类命名

## 执行步骤

1. 运行 pylint 分析
2. 解析输出结果
3. 按严重级别分类
4. 提供修复建议

## 输出格式

```markdown
## Pylint 检查报告

### 总体评分
- 代码评分: X.X / 10

### 问题统计
- 🔴 严重错误: 0
- 🟠 警告: 0
- 🟡 约定: 0
- 🔵 信息: 0

### 详细问题
<!-- 按文件列出问题 -->

### 修复建议
<!-- 提供针对性建议 -->
```
```

#### 创建技能：Django 项目生成器

```yaml
# skills/django-create/SKILL.md
---
name: django-create
description: 创建 Django 项目结构
argument-hint: [project-name]
disable-model-invocation: true
allowed-tools: Bash(django-admin *), Bash(python *), Bash(mkdir *)
---

# Django 项目生成器

创建名为 $ARGUMENTS 的 Django 项目。

## 项目结构

```
project-name/
├── manage.py
├── project_name/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # 基础配置
│   │   ├── development.py   # 开发配置
│   │   ├── production.py    # 生产配置
│   │   └── test.py          # 测试配置
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── core/                # 核心应用
├── config/                  # 配置文件
├── static/                  # 静态文件
├── media/                   # 媒体文件
├── templates/               # 模板文件
├── locale/                  # 国际化
├── tests/                   # 测试目录
├── docs/                    # 文档
├── scripts/                 # 脚本
├── requirements/            # 依赖文件
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── .env.example             # 环境变量示例
```

## 生成步骤

1. 创建 Django 项目
2. 配置分离的 settings
3. 创建 apps 目录
4. 配置静态文件和媒体文件
5. 设置基础中间件
6. 创建 .env 文件模板
7. 配置 requirements/
8. 创建基础目录结构
9. 初始化 Git
10. 生成 README.md
```

#### 创建子代理：Python 代码审查者

```markdown
# agents/python-reviewer.md
---
name: python-reviewer
description: Python 代码专家，专注于 Python 最佳实践
model: sonnet
---

# Python 代码审查代理

你是资深的 Python 开发者，精通 Python 最佳实践、设计模式、性能优化。

## 审查重点

### 1. PEP 8 遵循
- 缩进使用 4 空格
- 行长度不超过 79 字符
- 导入顺序：标准库 → 第三方 → 本地
- 空行使用规范

### 2. Pythonic 代码
- 使用列表推导式
- 使用上下文管理器 (with)
- 使用生成器处理大数据
- 利用装饰器
- 避免反模式

### 3. 类型提示
- 函数添加类型提示
- 使用 Type Hints
- 利用 mypy 检查

### 4. 异常处理
- 具体异常类型
- 适当的异常捕获范围
- 资源清理
- 异常链 (raise from)

### 5. 性能优化
- 避免全局变量
- 使用 __slots__
- 缓存优化 (lru_cache)
- 异步编程 (async/await)
- 数据库查询优化

### 6. 安全问题
- SQL 注入防护
- XSS 防护
- 密码处理 (hashlib/bcrypt)
- 敏感信息保护

### 7. 测试覆盖
- 单元测试 (pytest)
- Mock 使用
- 测试覆盖率 > 80%

### 8. 文档
- Docstring 规范 (Google/NumPy)
- 复杂逻辑注释
- README 更新

## 输出格式

```markdown
## Python 代码审查

### 整体评价
- 代码质量: ⭐⭐⭐⭐⭐
- PEP 8 符合度: 95%

### 问题清单

#### 🔴 必须修复
1. **位置**: `app/views.py:45`
   - **问题**: 未处理异常
   - **建议**: ...

#### 🟡 建议改进
1. **位置**: `app/models.py:23`
   - **问题**: 缺少类型提示
   - **建议**: ...

### 最佳实践建议
1. 使用 dataclass 替代普通类
2. 添加异步支持
3. 使用 pydantic 进行数据验证

### 参考资源
- PEP 8: https://peps.python.org/pep-0008/
- Python Guide: https://docs.python-guide.org/
```
```

#### 创建钩子配置

```json
// hooks/settings.json
{
  "hooks": {
    "tool.after:Edit": [
      {
        "command": "black --quiet $TOOL_INPUT_FILE",
        "runInBackground": true,
        "condition": "echo $TOOL_INPUT_FILE | grep -q '\\.py$'"
      }
    ],
    "session.start": [
      {
        "command": "python --version"
      },
      {
        "command": "echo 'Python Dev Assistant 插件已加载'"
      }
    ]
  }
}
```

### 3.2 高级插件功能

#### 条件激活

```json
{
  "activation": {
    "events": [
      "onLanguage:python",
      "onFilePattern:**/*.py",
      "onCommand:python-dev-assistant.activate",
      "onSetting:pythonDevAssistant.enabled=true"
    ]
  }
}
```

#### 插件间通信

```yaml
# skills/notify/SKILL.md
---
name: notify
description: 通知其他插件
---

# 插件间通信示例

通知 django-generator 插件：
```

#### 资源文件

```python
# resources/scripts/setup_env.py
#!/usr/bin/env python3
"""Python 环境设置脚本"""

import os
import sys
from pathlib import Path

def setup_python_env(project_path: str, version: str = "3.11"):
    """设置 Python 环境"""
    path = Path(project_path)

    # 创建 .env 文件
    env_file = path / ".env"
    env_content = f"""# Python 环境配置
PYTHON_VERSION={version}
DEBUG=True
SECRET_KEY=change-this-in-production
DATABASE_URL=postgresql://user:pass@localhost/db
"""
    env_file.write_text(env_content)

    print(f"✅ Python 环境已配置: {env_file}")

if __name__ == "__main__":
    setup_python_env(sys.argv[1] if len(sys.argv) > 1 else ".")
```

---

## 四、插件打包与分发

### 4.1 本地打包

```bash
# 创建插件包
claude plugin pack python-dev-assistant

# 生成结构
python-dev-assistant-1.0.0.claude-plugin/
├── plugin.json
├── skills/
├── agents/
└── ...
```

### 4.2 发布到 NPM

```bash
# 登录 NPM
npm login

# 发布插件
npm publish

# 或使用 Claude Code CLI
claude plugin publish
```

### 4.3 发布到插件市场

```bash
# 提交到官方市场
claude plugin submit --marketplace official

# 提交到企业市场
claude plugin submit --marketplace https://marketplace.company.com
```

### 4.4 版本管理

```json
{
  "version": "1.0.0",
  "releaseNotes": {
    "1.0.0": "初始版本发布",
    "1.1.0": "新增 FastAPI 支持",
    "1.2.0": "添加异步代码审查",
    "2.0.0": "重大更新：重构审查逻辑"
  }
}
```

---

## 五、插件使用指南

### 5.1 安装插件

#### 从市场安装

```bash
# 交互式安装
> /plugin
# 选择插件并安装

# 命令行安装
claude plugin install python-dev-assistant

# 指定版本
claude plugin install python-dev-assistant@1.0.0

# 从 GitHub 安装
claude plugin install github:user/repo
```

#### 从本地安装

```bash
# 安装本地插件
claude plugin install ./python-dev-assistant

# 链接本地插件（开发模式）
claude plugin link ./python-dev-assistant
```

### 5.2 管理插件

```bash
# 列出已安装插件
claude plugin list

# 查看插件详情
claude plugin info python-dev-assistant

# 更新插件
claude plugin update python-dev-assistant

# 更新所有插件
claude plugin update --all

# 卸载插件
claude plugin uninstall python-dev-assistant

# 禁用插件
claude plugin disable python-dev-assistant

# 启用插件
claude plugin enable python-dev-assistant
```

### 5.3 配置插件

```json
// ~/.claude/plugin-settings.json
{
  "python-dev-assistant": {
    "enabled": true,
    "settings": {
      "defaultFramework": "fastapi",
      "pythonVersion": "3.11",
      "autoFormatOnSave": true,
      "lintOnEdit": true
    }
  }
}
```

### 5.4 使用插件技能

```
> /django-create my-awesome-project
# 调用插件的 django-create 技能

> /pylint-check src/
# 调用插件的 pylint-check 技能
```

---

## 六、插件修改与定制

### 6.1 Fork 插件

```bash
# Fork 插件到本地
claude plugin fork python-dev-assistant

# 编辑 fork 的插件
cd ~/.claude/plugins/forked/python-dev-assistant
vim skills/pylint-check/SKILL.md
```

### 6.2 覆盖插件配置

```json
// .claude/plugin-overrides.json
{
  "python-dev-assistant": {
    "settings": {
      "pythonVersion": "3.12",
      "defaultFramework": "django"
    },
    "skills": {
      "pylint-check": {
        "disabled": false,
        "priority": 100
      }
    }
  }
}
```

### 6.3 扩展插件技能

```yaml
# .claude/skills/pylint-check-custom/SKILL.md
---
name: pylint-check-custom
extends: "python-dev-assistant:pylint-check"
---

# 自定义 Pylint 检查

基于原版 pylint-check，添加自定义规则：
1. 检查公司特定的命名规范
2. 检查安全相关的代码模式
3. 添加自定义评分规则
```

---

## 七、插件开发进阶技巧

### 7.1 命名空间管理

```yaml
# skills/feature/SKILL.md
---
name: my-plugin:feature
description: 使用插件命名空间的技能
---

# 技能内容

调用方式：
- `/my-plugin:feature`
- `/feature`（当命名空间唯一时）
```

### 7.2 技能组合

```yaml
# skills/combo/SKILL.md
---
name: combo
description: 组合多个技能
---

# 组合技能

依次调用：
1. @python-dev-assistant:pylint-check
2. @python-dev-assistant:type-check
3. @my-plugin:security-check

生成综合报告。
```

### 7.3 动态配置

```yaml
# skills/dynamic/SKILL.md
---
name: dynamic
description: 根据配置动态调整行为
---

# 动态配置技能

读取插件配置：
```yaml
defaultFramework: !`cat ~/.claude/plugin-settings.json | jq -r '."python-dev-assistant".settings.defaultFramework'`
pythonVersion: !`cat ~/.claude/plugin-settings.json | jq -r '."python-dev-assistant".settings.pythonVersion'`
```

根据配置调整生成代码的框架和版本。
```

### 7.4 事件驱动

```json
// hooks/settings.json
{
  "hooks": {
    "plugin.after:activate": [
      {
        "command": "echo '插件已激活，执行初始化...'"
      }
    ],
    "plugin.before:deactivate": [
      {
        "command": "echo '插件即将停用，执行清理...'"
      }
    ]
  }
}
```

### 7.5 依赖管理

```json
{
  "dependencies": {
    "python-base": "^1.0.0",
    "code-quality-tools": "^2.0.0"
  },
  "optionalDependencies": {
    "enterprise-features": "^1.0.0"
  },
  "peerDependencies": {
    "claude-code": ">=1.5.0"
  }
}
```

---

## 八、调试与测试

### 8.1 本地测试

```bash
# 开发模式加载插件
claude --dev-plugin ./python-dev-assistant

# 查看插件日志
claude --log-level debug

# 测试单个技能
echo "测试输入" | claude -p "/pylint-check test.py"
```

### 8.2 插件测试框架

```yaml
# tests/skills/pylint-check_test.yaml
---
name: pylint-check 测试
tests:
  - name: 基本功能测试
    input: "/pylint-check tests/sample.py"
    expected:
      contains: ["代码评分", "问题统计"]

  - name: 错误处理测试
    input: "/pylint-check nonexistent.py"
    expected:
      contains: ["文件不存在"]
```

```bash
# 运行测试
claude plugin test python-dev-assistant
```

### 8.3 调试技巧

```yaml
# skills/debug/SKILL.md
---
name: debug-skill
---

# 调试技能

添加调试输出：
```bash
echo "DEBUG: 变量值 = $VARIABLE" >&2
```

查看完整上下文：
```
> /context
```

查看加载的技能：
```
> /skills
```
```

---

## 九、常见插件模式

### 9.1 语言支持插件

```
language-support/
├── skills/
│   ├── create-file/          # 创建新文件
│   ├── code-format/          # 代码格式化
│   ├── lint/                 # 代码检查
│   └── test-runner/          # 测试运行
└── agents/
    └── code-reviewer.md      # 代码审查
```

### 9.2 框架支持插件

```
framework-boilerplate/
├── skills/
│   ├── create-project/       # 创建项目
│   ├── add-component/        # 添加组件
│   ├── add-route/            # 添加路由
│   └── generate-api/         # 生成 API
└── resources/
    └── templates/            # 模板文件
```

### 9.3 工具集成插件

```
tool-integration/
├── mcp/
│   └── mcp-servers.json      # MCP 服务器配置
├── skills/
│   ├── query-tool/           # 查询工具
│   └── sync-data/            # 同步数据
└── hooks/
    └── settings.json         # 钩子配置
```

### 9.4 团队规范插件

```
team-standards/
├── CLAUDE.md                 # 团队规范
├── rules/                    # 代码规则
│   ├── naming.md
│   ├── structure.md
│   └── security.md
├── skills/
│   ├── code-review/          # 代码审查
│   └── pr-checklist/         # PR 检查清单
└── agents/
    └── compliance-checker.md # 合规检查
```

---

## 十、插件市场与生态

### 10.1 官方插件市场

```
https://marketplace.claude.ai/

分类：
- 编程语言
- 框架支持
- 开发工具
- 团队协作
- 企业功能
- 社区精选
```

### 10.2 企业插件市场

```bash
# 配置企业市场
claude config set marketplace.url https://marketplace.company.com

# 安装企业插件
claude plugin install @company/internal-tools
```

### 10.3 插件发现

```bash
# 搜索插件
claude plugin search python

# 按类别浏览
claude plugin browse --category "Programming Languages"

# 查看热门插件
claude plugin trending

# 查看推荐插件
claude plugin recommended
```

---

## 十一、最佳实践

### 11.1 插件设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **单一职责** | 每个插件专注一个领域 | Python 插件只处理 Python 相关 |
| **可组合** | 插件之间可以组合使用 | 代码审查 + 格式化 |
| **可配置** | 提供配置选项 | 框架版本、样式偏好 |
| **向后兼容** | 保持 API 稳定 | 版本升级不破坏现有功能 |
| **文档完善** | 提供清晰文档 | README、示例、API 文档 |

### 11.2 性能优化

```yaml
# 技能优化
---
name: optimized-skill
description: 优化后的技能
---

# 性能优化技巧

1. **懒加载**：只在需要时加载资源
2. **缓存**：缓存重复计算结果
3. **并行**：使用子代理并行处理
4. **限制**：限制搜索范围
5. **索引**：使用 Glob 索引文件
```

### 11.3 安全考虑

```json
{
  "security": {
    "contentSecurityPolicy": {
      "allowedDomains": ["*.python.org"],
      "allowedCommands": ["python*", "pip*"]
    },
    "dataHandling": {
      "noTelemetry": false,
      "localDataOnly": true
    },
    "permissions": {
      "required": ["Read", "Bash(python *)"],
      "optional": ["WebFetch"]
    }
  }
}
```

### 11.4 版本策略

```json
{
  "versioning": {
    "scheme": "semantic",
    "compatibility": {
      "backward": "minor",
      "forward": "patch"
    },
    "deprecation": {
      "duration": "2 versions",
      "warning": true
    }
  }
}
```

---

## 十二、实战案例

### 案例 1：企业内部插件

```json
{
  "name": "@acme/internal-tools",
  "version": "2.1.0",
  "displayName": "ACME 内部工具集",
  "description": "ACME 公司内部开发工具",
  "private": true,
  "registry": "https://npm.acme.com",
  "contributes": {
    "skills": [
      "create-ticket",      // 创建 JIRA 票据
      "deploy-internal",    // 内部部署
      "security-scan"       // 安全扫描
    ],
    "mcpServers": [
      "jira",               // JIRA 集成
      "confluence",         // Confluence 集成
      "artifactory"         // Artifactory 集成
    ]
  }
}
```

### 案例 2：开源社区插件

```json
{
  "name": "vue-dev-helper",
  "version": "3.2.0",
  "displayName": "Vue 开发助手",
  "description": "Vue 3 开发必备工具",
  "license": "MIT",
  "repository": "https://github.com/vue-community/vue-dev-helper",
  "contributes": {
    "skills": [
      "create-component",
      "create-composable",
      "add-router",
      "add-pinia-store"
    ],
    "agents": [
      "vue-code-reviewer"
    ]
  },
  "settings": {
    "vueDevHelper.scriptSetup": {
      "type": "boolean",
      "default": true,
      "description": "使用 <script setup>"
    },
    "vueDevHelper.typescript": {
      "type": "boolean",
      "default": true,
      "description": "使用 TypeScript"
    }
  }
}
```

### 案例 3：插件组合

```bash
# 安装多个互补插件
claude plugin install \
  python-dev-assistant \    # Python 基础支持
  code-quality-pro \        # 代码质量工具
  security-scanner \        # 安全扫描
  doc-generator            # 文档生成

# 这些插件协同工作：
# 1. python-dev-assistant 提供 Python 特定功能
# 2. code-quality-pro 提供通用代码检查
# 3. security-scanner 添加安全检查
# 4. doc-generator 自动生成文档
```

---

## 十三、故障排除

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 插件无法加载 | plugin.json 格式错误 | 使用 `claude plugin validate` 检查 |
| 技能不显示 | description 不匹配 | 优化技能描述 |
| 命名冲突 | 多个插件同名技能 | 使用命名空间 |
| 性能问题 | 插件加载过多内容 | 使用懒加载 |
| 权限错误 | permissions 配置不当 | 检查 allow/deny 规则 |

### 调试命令

```bash
# 验证插件
claude plugin validate ./my-plugin

# 查看插件状态
claude plugin status

# 查看插件日志
claude plugin logs my-plugin

# 重载插件
claude plugin reload my-plugin

# 重置插件
claude plugin reset my-plugin
```

---

## 十四、总结

Claude Code 插件体系核心要点：

### 插件核心概念

| 概念 | 说明 |
|------|------|
| **plugin.json** | 插件清单文件 |
| **命名空间** | `plugin-name:skill-name` |
| **贡献点** | skills, agents, hooks, mcp, rules |
| **激活条件** | onLanguage, onCommand, onSetting |
| **版本管理** | 语义化版本控制 |

### 插件开发流程

```
1. 设计插件 → 确定功能和边界
2. 创建结构 → plugin.json + 目录
3. 实现功能 → skills/agents/hooks
4. 测试调试 → 本地测试
5. 打包发布 → npm/marketplace
6. 维护更新 → 版本迭代
```

### 最佳实践

- ✅ 单一职责原则
- ✅ 使用命名空间
- ✅ 提供配置选项
- ✅ 编写完整文档
- ✅ 保持向后兼容
- ✅ 性能优化
- ✅ 安全考虑
- ✅ 社区友好

掌握插件体系后，你可以：
- 🛠️ 创建自定义工具
- 📦 打包团队规范
- 🌐 贡献开源社区
- 🏢 构建企业插件库

---

> 📚 **参考资料**：[插件开发](https://code.claude.com/docs/en/plugins) | [插件参考](https://code.claude.com/docs/en/plugins-reference) | [插件市场](https://marketplace.claude.ai)
