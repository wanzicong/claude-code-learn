# Hooks 推荐

Hooks 在响应 Claude Code 事件时自动运行命令。它们非常适合应该一致执行的强制和自动化。

**注意**：这些是常见模式。使用网络搜索找到此处未列出的工具/框架的 hooks，以为用户推荐最佳 hooks。

## 自动格式化 Hooks

### Prettier (JavaScript/TypeScript)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `.prettierrc`、`.prettierrc.json`、`prettier.config.js` | ✓✓ |

**推荐**：Edit/Write 上的 PostToolUse hook 以自动格式化
**价值**：代码保持格式化，无需费心

### ESLint (JavaScript/TypeScript)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `.eslintrc`、`.eslintrc.json`、`eslint.config.js` | ✓✓ |

**推荐**：Edit/Write 上的 PostToolUse hook 以自动修复
**价值**：Lint 错误自动修复

### Black/isort (Python)
| 检测方式 | 文件存在 |
|-----------|-------------|
| 带有 black/isort 的 `pyproject.toml`、`.black`、`setup.cfg` | ✓✓ |

**推荐**：格式化 Python 文件的 PostToolUse hook
**价值**：一致的 Python 格式化

### Ruff (Python - 现代化)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `ruff.toml`、带有 `[tool.ruff]` 的 `pyproject.toml` | ✓✓ |

**推荐**：Lint + 格式化的 PostToolUse hook
**价值**：快速、全面的 Python Lint

### gofmt (Go)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `go.mod` | ✓✓ |

**推荐**：运行 gofmt 的 PostToolUse hook
**价值**：标准的 Go 格式化

### rustfmt (Rust)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `Cargo.toml` | ✓✓ |

**推荐**：运行 rustfmt 的 PostToolUse hook
**价值**：标准的 Rust 格式化

---

## 类型检查 Hooks

### TypeScript
| 检测方式 | 文件存在 |
|-----------|-------------|
| `tsconfig.json` | ✓✓ |

**推荐**：运行 tsc --noEe mit 的 PostToolUse hook
**价值**：立即捕获类型错误

### mypy/pyright (Python)
| 检测方式 | 文件存在 |
|-----------|-------------|
| `mypy.ini`、`pyrightconfig.json`、带有 mypy 的 pyproject.toml | ✓✓ |

**推荐**：类型检查的 PostToolUse hook
**价值**：捕获 Python 中的类型错误

---

## 保护 Hooks

### 阻止敏感文件编辑
| 检测方式 | 存在 |
|-----------|-------------|
| `.env`、`.env.local`、`.env.production` | 环境文件 |
| `credentials.json`、`secrets.yaml` | 秘密文件 |
| `.git/` 目录 | Git 内部文件 |

**推荐**：阻止对这些路径的 Edit/Write 的 PreToolUse hook
**价值**：防止意外泄露秘密或损坏 git

### 阻止锁定文件编辑
| 检测方式 | 存在 |
|-----------|-------------|
| `package-lock.json`、`yarn.lock`、`pnpm-lock.yaml` | JS 锁定文件 |
| `Cargo.lock`、`poetry.lock`、`Pipfile.lock` | 其他锁定文件 |

**推荐**：阻止直接编辑的 PreToolUse hook
**价值**：锁定文件应仅通过包管理器更改

---

## 测试运行器 Hooks

### Jest (JavaScript/TypeScript)
| 检测方式 | 存在 |
|-----------|-------------|
| `jest.config.js`、package.json 中的 jest | 已配置 Jest |
| `__tests__/`、`*.test.ts`、`*.spec.ts` | 测试文件存在 |

**推荐**：编辑后运行相关测试的 PostToolUse hook
**价值**：更改的即时测试反馈

### pytest (Python)
| 检测方式 | 存在 |
|-----------|-------------|
| `pytest.ini`、带有 pytest 的 pyproject.toml | 已配置 pytest |
| `tests/`、`test_*.py` | 测试文件存在 |

**推荐**：在更改的文件上运行 pytest 的 PostToolUse hook
**价值**：即时测试反馈

---

## 快速参考：检测 → 推荐

| 如果看到 | 推荐此 Hook |
|------------|-------------------|
| Prettier 配置 | Edit/Write 时自动格式化 |
| ESLint 配置 | Edit/Write 时自动 Lint |
| Ruff/Black 配置 | 自动格式化 Python |
| tsconfig.json | Edit 时类型检查 |
| 测试目录 | Edit 时运行相关测试 |
| .env 文件 | 阻止 .env 编辑 |
| 锁定文件 | 阻止锁定文件编辑 |
| Go 项目 | Edit 时 gofmt |
| Rust 项目 | Edit 时 rustfmt |

---

## 通知 Hooks

通知 hooks 在 Claude Code 发送通知时运行。使用匹配器按通知类型过滤。

### 权限警报
| 匹配器 | 用例 |
|---------|----------|
| `permission_prompt` | Claude 请求权限时发出警报 |

**推荐**：播放声音、发送桌面通知或记录权限请求
**价值**：多任务处理时永远不会错过权限提示

### 空闲通知
| 匹配器 | 用例 |
|---------|----------|
| `idle_prompt` | Claude 等待输入时发出警报（空闲 60+ 秒） |

**推荐**：Claude 需要注意时播放声音或发送通知
**价值**：知道 Claude 何时准备好接收您的输入

### 示例配置

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Ping.aiff"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude is waiting\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 可用匹配器

| 匹配器 | 触发时机 |
|---------|---------------|
| `permission_prompt` | Claude 需要工具权限 |
| `idle_prompt` | Claude 等待输入（60+ 秒） |
| `auth_success` | 身份验证成功 |
| `elicitation_dialog` | MCP 工具需要输入 |

---

## 快速参考：检测 → 推荐

| 如果看到 | 推荐此 Hook |
|------------|-------------------|
| Prettier 配置 | Edit/Write 时自动格式化 |
| ESLint 配置 | Edit/Write 时自动 Lint |
| Ruff/Black 配置 | 自动格式化 Python |
| tsconfig.json | Edit 时类型检查 |
| 测试目录 | Edit 时运行相关测试 |
| .env 文件 | 阻止 .env 编辑 |
| 锁定文件 | 阻止锁定文件编辑 |
| Go 项目 | Edit 时 gofmt |
| Rust 项目 | Edit 时 rustfmt |
| 多任务工作流 | 用于警报的通知 hooks |

---

## Hook 位置

Hooks 放在 `.claude/settings.json` 中：

```
.claude/
└── settings.json  ← Hook 配置在此处
```

推荐创建 `.claude/` 目录（如果不存在）。
