# 插件推荐

插件是可安装的技能、命令、代理和 hooks 集合。通过 `/plugin install` 安装。

**注意**：这些是来自官方仓库的插件。使用网络搜索发现其他社区插件。

---

## 官方插件

### 开发与代码质量

| 插件 | 最适用于 | 主要功能 |
|--------|----------|--------------|
| **plugin-dev** | 构建 Claude Code 插件 | 用于创建技能、hooks、命令、代理的技能 |
| **pr-review-toolkit** | PR 审查工作流 | 专门的审查代理（代码、测试、类型） |
| **code-review** | 自动化代码审查 | 带置信度评分的多代理审查 |
| **code-simplifier** | 代码重构 | 在保持功能的同时简化代码 |
| **feature-dev** | 功能开发 | 带代理的端到端功能工作流 |

### Git 与工作流

| 插件 | 最适用于 | 主要功能 |
|--------|----------|--------------|
| **commit-commands** | Git 工作流 | /commit、/commit-push-pr 命令 |
| **hookify** | 自动化规则 | 从对话模式创建 hooks |

### 前端

| 插件 | 最适用于 | 主要功能 |
|--------|----------|--------------|
| **frontend-design** | UI 开发 | 生产级 UI，避免通用美学 |

### 学习与指导

| 插件 | 最适用于 | 主要功能 |
|--------|----------|--------------|
| **explanatory-output-style** | 学习 | 关于代码选择的教育见解 |
| **learning-output-style** | 交互式学习 | 在决策点请求贡献 |
| **security-guidance** | 安全意识 | 编辑时警告安全问题 |

### 语言服务器 (LSP)

| 插件 | 语言 |
|--------|----------|
| **typescript-lsp** | TypeScript/JavaScript |
| **pyright-lsp** | Python |
| **gopls-lsp** | Go |
| **rust-analyzer-lsp** | Rust |
| **clangd-lsp** | C/C++ |
| **jdtls-lsp** | Java |
| **kotlin-lsp** | Kotlin |
| **swift-lsp** | Swift |
| **csharp-lsp** | C# |
| **php-lsp** | PHP |
| **lua-lsp** | Lua |

---

## 快速参考：代码库 → 插件

| 代码库信号 | 推荐的插件 |
|-----------------|-------------------|
| 构建插件 | plugin-dev |
| 基于 PR 的工作流 | pr-review-toolkit |
| Git 提交 | commit-commands |
| React/Vue/Angular | frontend-design |
| 想要自动化规则 | hookify |
| TypeScript 项目 | typescript-lsp |
| Python 项目 | pyright-lsp |
| Go 项目 | gopls-lsp |
| 安全敏感代码 | security-guidance |
| 学习/入职 | explanatory-output-style |

---

## 插件管理

```bash
# 安装插件
/plugin install <插件名称>

# 列出已安装的插件
/plugin list

# 查看插件详情
/plugin info <插件名称>
```

---

## 何时推荐插件

**在以下情况下推荐插件安装：**
- 用户希望从 Anthropic 官方仓库或其他共享市场安装 Claude Code 自动化功能
- 用户需要多个相关功能
- 团队想要标准化工作流
- 首次设置 Claude Code
