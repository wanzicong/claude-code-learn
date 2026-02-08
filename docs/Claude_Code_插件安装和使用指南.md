# Claude Code 插件安装和使用指南

## 📚 目录

1. [插件安装方法](#插件安装方法)
2. [验证插件安装](#验证插件安装)
3. [启用和配置插件](#启用和配置插件)
4. [使用插件功能](#使用插件功能)
5. [插件管理命令](#插件管理命令)
6. [常见问题](#常见问题)

---

## 插件安装方法

### 方法一：复制到插件目录（推荐 - 已完成）

这是最简单直接的方法，适合本地开发和测试。

```powershell
# 1. 创建插件目录（如果不存在）
mkdir C:\Users\13608\.claude\plugins

# 2. 复制插件到目录
Copy-Item -Path "D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant" `
          -Destination "C:\Users\13608\.claude\plugins\python-dev-assistant" `
          -Recurse -Force
```

**✅ 优点**：
- 简单快速
- 不需要管理员权限
- 适合开发和测试

**❌ 缺点**：
- 需要手动同步更新
- 占用额外磁盘空间

---

### 方法二：创建符号链接（开发推荐）

符号链接可以让插件目录指向源代码目录，方便开发时实时更新。

```powershell
# 需要以管理员身份运行 PowerShell
New-Item -ItemType SymbolicLink `
         -Path "C:\Users\13608\.claude\plugins\python-dev-assistant" `
         -Target "D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant"
```

**✅ 优点**：
- 实时同步源代码
- 不占用额外空间
- 适合插件开发

**❌ 缺点**：
- 需要管理员权限
- Windows 需要开启开发者模式或管理员权限

**开启 Windows 开发者模式**：
1. 打开 `设置` → `更新和安全` → `开发者选项`
2. 启用 `开发人员模式`
3. 重启 PowerShell

---

### 方法三：使用 Git Clone（团队协作）

如果插件托管在 Git 仓库，可以直接克隆到插件目录。

```bash
# 克隆到插件目录
cd C:\Users\13608\.claude\plugins
git clone https://github.com/yourname/python-dev-assistant.git

# 或者克隆到其他位置后创建符号链接
git clone https://github.com/yourname/python-dev-assistant.git D:\plugins\python-dev-assistant
New-Item -ItemType SymbolicLink -Path "C:\Users\13608\.claude\plugins\python-dev-assistant" -Target "D:\plugins\python-dev-assistant"
```

---

### 方法四：从市场安装（未来支持）

当插件发布到 Claude Code 市场后，可以使用命令安装：

```bash
# 从官方市场安装
claude plugin install python-dev-assistant

# 从自定义市场安装
claude plugin install python-dev-assistant --marketplace https://your-marketplace.com
```

---

## 验证插件安装

### 1. 检查插件目录

```bash
# 查看插件目录
ls C:\Users\13608\.claude\plugins\python-dev-assistant

# 应该看到以下结构
python-dev-assistant/
├── .claude-plugin/
│   └── marketplace.json
├── agents/
├── commands/
├── hooks/
├── skills/
└── README.md
```

### 2. 验证插件配置

```bash
# 验证插件配置是否正确
claude plugin validate C:\Users\13608\.claude\plugins\python-dev-assistant

# 应该看到
✓ Validation successful
```

### 3. 查看已安装插件列表

```bash
# 列出所有已安装的插件
claude plugin list

# 应该看到
python-dev-assistant (1.0.0) - Python development assistant
```

### 4. 查看插件详情

```bash
# 查看插件详细信息
claude plugin info python-dev-assistant

# 输出示例
Name: python-dev-assistant
Version: 1.0.0
Description: Python development assistant
Skills: 3
Agents: 1
Hooks: 1
Commands: 5
```

---

## 启用和配置插件

### 1. 启用插件

插件复制到目录后会自动启用。如果需要手动启用：

```bash
# 启用插件
claude plugin enable python-dev-assistant

# 禁用插件
claude plugin disable python-dev-assistant

# 重新加载插件
claude plugin reload python-dev-assistant
```

### 2. 配置插件

#### 全局配置 (`~/.claude/settings.json`)

```json
{
  "plugins": {
    "python-dev-assistant": {
      "enabled": true,
      "config": {
        "defaultFramework": "fastapi",
        "pythonVersion": "3.11",
        "enableHooks": true
      }
    }
  }
}
```

#### 项目级配置 (`.claude/settings.json`)

```json
{
  "plugins": {
    "python-dev-assistant": {
      "config": {
        "defaultFramework": "django",
        "pythonVersion": "3.10"
      }
    }
  }
}
```

#### 插件本地配置 (`python-dev-assistant.local.md`)

```markdown
# Python Dev Assistant 本地配置

## 配置选项

- **enable_hook**: true
- **default_framework**: fastapi
- **python_version**: 3.11
- **auto_format**: true
- **linter**: ruff

## 项目特定设置

- **project_type**: web_api
- **use_async**: true
```

---

## 使用插件功能

### 1. 使用技能 (Skills)

技能会自动加载，Claude 会根据上下文自动使用。

```
你：帮我创建一个 FastAPI 项目

Claude：我会使用 python-dev-assistant 插件的技能来帮你创建...
[自动调用 django-flask-architecture 技能]
```

**手动触发技能**：
```
你：@python-best-practices 检查这段代码的最佳实践
```

### 2. 使用命令 (Commands)

```bash
# 使用 py-check 命令检查代码
/py-check app.py

# 使用 py-django 命令创建 Django 项目
/py-django create myproject

# 使用 py-flask 命令创建 Flask 项目
/py-flask create myapp

# 使用 py-docs 命令生成文档
/py-docs generate

# 使用 py-snippet 命令插入代码片段
/py-snippet fastapi-crud
```

### 3. 使用代理 (Agents)

```
你：@python-code-analyzer 分析这个 Python 项目的代码质量

Claude：我会启动 Python 代码分析代理来检查...
[启动 python-code-analyzer 代理]

## Python 代码分析

### 整体评价
- 代码质量: ⭐⭐⭐⭐
- PEP 8 符合度: 92%

### 问题清单
...
```

### 4. 钩子自动触发 (Hooks)

钩子会在特定事件时自动触发，无需手动调用。

```
你：帮我修改 app.py 文件

Claude：[准备写入文件]
[自动触发 pre-tool-use 钩子]
[检查 Python 代码质量]
[如果有问题，显示警告]
[继续写入文件]
```

---

## 插件管理命令

### 基本命令

```bash
# 列出所有插件
claude plugin list

# 查看插件信息
claude plugin info python-dev-assistant

# 启用插件
claude plugin enable python-dev-assistant

# 禁用插件
claude plugin disable python-dev-assistant

# 重新加载插件
claude plugin reload python-dev-assistant

# 卸载插件
claude plugin uninstall python-dev-assistant

# 更新插件
claude plugin update python-dev-assistant

# 验证插件
claude plugin validate python-dev-assistant
```

### 高级命令

```bash
# 查看插件日志
claude plugin logs python-dev-assistant

# 查看插件状态
claude plugin status python-dev-assistant

# 调试插件
claude plugin debug python-dev-assistant

# 导出插件配置
claude plugin export python-dev-assistant > config.json

# 导入插件配置
claude plugin import python-dev-assistant < config.json
```

---

## 插件目录结构

```
C:\Users\13608\.claude\
├── settings.json                    # 全局配置
├── CLAUDE.md                        # 全局记忆
├── plugins/                         # 插件目录
│   ├── python-dev-assistant/        # 你的插件 ✅
│   │   ├── .claude-plugin/
│   │   │   └── marketplace.json
│   │   ├── skills/
│   │   │   ├── python-best-practices/
│   │   │   ├── django-flask-architecture/
│   │   │   └── python-documentation/
│   │   ├── agents/
│   │   │   └── python-code-analyzer.md
│   │   ├── hooks/
│   │   │   └── hooks.json
│   │   ├── commands/
│   │   │   ├── py-check.md
│   │   │   ├── py-django.md
│   │   │   ├── py-flask.md
│   │   │   ├── py-docs.md
│   │   │   └── py-snippet.md
│   │   └── README.md
│   │
│   └── other-plugin/                # 其他插件
│
├── skills/                          # 全局技能
└── agents/                          # 全局代理
```

---

## 常见问题

### Q1: 插件安装后不生效？

**解决方法**：

1. **重启 Claude Code**
   ```bash
   # 完全退出 Claude Code 后重新打开
   ```

2. **重新加载插件**
   ```bash
   claude plugin reload python-dev-assistant
   ```

3. **检查插件是否启用**
   ```bash
   claude plugin list
   # 确认插件状态为 enabled
   ```

4. **验证插件配置**
   ```bash
   claude plugin validate C:\Users\13608\.claude\plugins\python-dev-assistant
   ```

---

### Q2: 如何更新插件？

**方法一：手动更新（复制方式）**
```powershell
# 删除旧版本
Remove-Item -Path "C:\Users\13608\.claude\plugins\python-dev-assistant" -Recurse -Force

# 复制新版本
Copy-Item -Path "D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant" `
          -Destination "C:\Users\13608\.claude\plugins\python-dev-assistant" `
          -Recurse -Force

# 重新加载
claude plugin reload python-dev-assistant
```

**方法二：自动更新（符号链接方式）**
```bash
# 如果使用符号链接，只需更新源代码
cd D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant
git pull

# 重新加载插件
claude plugin reload python-dev-assistant
```

**方法三：使用命令更新（Git 方式）**
```bash
cd C:\Users\13608\.claude\plugins\python-dev-assistant
git pull
claude plugin reload python-dev-assistant
```

---

### Q3: 插件冲突怎么办？

如果多个插件提供相同的功能：

1. **禁用冲突的插件**
   ```bash
   claude plugin disable conflicting-plugin
   ```

2. **调整插件优先级**（在 `settings.json` 中）
   ```json
   {
     "plugins": {
       "python-dev-assistant": {
         "priority": 10
       },
       "other-plugin": {
         "priority": 5
       }
     }
   }
   ```

3. **使用命名空间**
   ```
   @python-dev-assistant:python-best-practices
   ```

---

### Q4: 如何调试插件？

1. **启用调试日志**
   ```json
   {
     "env": {
       "CLAUDE_CODE_LOG_LEVEL": "debug",
       "CLAUDE_PLUGIN_DEBUG": "python-dev-assistant"
     }
   }
   ```

2. **查看插件日志**
   ```bash
   claude plugin logs python-dev-assistant
   ```

3. **使用调试模式**
   ```bash
   claude plugin debug python-dev-assistant
   ```

4. **检查插件状态**
   ```bash
   claude plugin status python-dev-assistant
   ```

---

### Q5: 插件占用太多资源？

1. **禁用不需要的钩子**
   ```json
   {
     "plugins": {
       "python-dev-assistant": {
         "config": {
           "enableHooks": false
         }
       }
     }
   }
   ```

2. **限制插件功能**
   ```json
   {
     "plugins": {
       "python-dev-assistant": {
         "enabledFeatures": ["skills", "commands"],
         "disabledFeatures": ["hooks", "agents"]
       }
     }
   }
   ```

3. **调整钩子触发条件**
   编辑 `hooks/hooks.json`，添加更严格的匹配条件。

---

### Q6: 如何卸载插件？

```bash
# 方法一：使用命令卸载
claude plugin uninstall python-dev-assistant

# 方法二：手动删除
Remove-Item -Path "C:\Users\13608\.claude\plugins\python-dev-assistant" -Recurse -Force

# 重启 Claude Code
```

---

### Q7: 插件在项目中不生效？

检查项目级配置 `.claude/settings.json`：

```json
{
  "plugins": {
    "python-dev-assistant": {
      "enabled": true  // 确保启用
    }
  }
}
```

---

### Q8: 如何分享插件给团队？

**方法一：Git 仓库**
```bash
# 1. 创建 Git 仓库
cd D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourname/python-dev-assistant.git
git push -u origin main

# 2. 团队成员安装
cd C:\Users\username\.claude\plugins
git clone https://github.com/yourname/python-dev-assistant.git
```

**方法二：打包分发**
```bash
# 1. 打包插件
cd D:\WorkeSpaceCoding\ai-agents\claude-code-learn
tar -czf python-dev-assistant.tar.gz python-dev-assistant/

# 2. 团队成员解压
cd C:\Users\username\.claude\plugins
tar -xzf python-dev-assistant.tar.gz
```

**方法三：内部市场**
```bash
# 配置内部市场
# ~/.claude/settings.json
{
  "marketplaces": [
    "https://internal-marketplace.company.com"
  ]
}

# 安装插件
claude plugin install python-dev-assistant --marketplace internal
```

---

## 最佳实践

### 1. 开发插件时使用符号链接

```powershell
# 以管理员身份运行
New-Item -ItemType SymbolicLink `
         -Path "C:\Users\13608\.claude\plugins\python-dev-assistant" `
         -Target "D:\WorkeSpaceCoding\ai-agents\claude-code-learn\python-dev-assistant"
```

### 2. 版本控制插件配置

```gitignore
# .gitignore
*.local.md
*.local.json
.claude/projects/
```

### 3. 使用项目级配置

```json
// .claude/settings.json
{
  "plugins": {
    "python-dev-assistant": {
      "config": {
        "defaultFramework": "django"
      }
    }
  }
}
```

### 4. 定期更新插件

```bash
# 每周检查更新
claude plugin update --all

# 或手动更新
cd C:\Users\13608\.claude\plugins\python-dev-assistant
git pull
claude plugin reload python-dev-assistant
```

### 5. 备份插件配置

```bash
# 导出配置
claude plugin export python-dev-assistant > backup.json

# 恢复配置
claude plugin import python-dev-assistant < backup.json
```

---

## 总结

### ✅ 插件已成功安装

你的 `python-dev-assistant` 插件已经成功安装到：
```
C:\Users\13608\.claude\plugins\python-dev-assistant
```

### 🎯 下一步

1. **重启 Claude Code** 使插件生效
2. **验证安装**：`claude plugin list`
3. **开始使用**：尝试使用插件的技能、命令和代理
4. **配置插件**：根据需要调整配置

### 📚 相关文档

- [Claude Code 配置文件完全指南](./Claude_Code_配置文件完全指南.md)
- [插件开发文档](../python-dev-assistant/README.md)
- [插件报告](../python-dev-assistant/PLUGIN_REPORT.md)

---

**文档版本**: 1.0
**最后更新**: 2024年2月
**适用版本**: Claude Code 0.7+
