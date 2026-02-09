# Claude Code 配置文件完全指南

## 📚 目录

1. [配置文件概览](#配置文件概览)
2. [settings.json 详解](#settingsjson-详解)
3. [.claude.json 详解](#claudejson-详解)
4. [配置优先级](#配置优先级)
5. [实用配置示例](#实用配置示例)
6. [最佳实践](#最佳实践)

---

## 配置文件概览

### 配置文件层级结构

Claude Code 使用多层级配置系统，从系统级到项目级逐层覆盖：

```
系统级配置
├── macOS:     /Library/Application Support/ClaudeCode/
├── Linux/WSL: /etc/claude-code/
└── Windows:   C:\Program Files\ClaudeCode/
           └── managed-settings.json  # IT 管理员部署的策略

用户级配置
├── ~/.claude/                        # 主配置目录
│   ├── settings.json                 # 全局用户设置 ⭐
│   ├── CLAUDE.md                     # 全局记忆文件
│   ├── skills/                       # 个人技能目录
│   ├── agents/                       # 子代理配置
│   └── projects/                     # 项目记忆和会话
│
├── ~/.claude.json                    # 主配置文件 ⭐
│                                     # (主题、OAuth、MCP 服务器)

项目级配置
└── your-project/
    ├── .claude/                      # 项目配置目录
    │   ├── settings.json             # 项目设置
    │   ├── settings.local.json       # 本地覆盖(不提交到 Git)
    │   ├── CLAUDE.md                 # 项目记忆文件
    │   ├── CLAUDE.local.md           # 本地覆盖(不提交到 Git)
    │   ├── skills/                   # 项目专用技能
    │   ├── agents/                   # 项目子代理
    │   └── rules/                    # 模块化规则文件
    │
    └── .mcp.json                     # 项目 MCP 服务器配置
```

### 两个核心配置文件的区别

| 特性 | `settings.json` | `.claude.json` |
|------|----------------|----------------|
| **主要作用** | 控制 Claude 行为和权限 | 配置 UI、OAuth、MCP 服务器 |
| **位置** | `~/.claude/settings.json` 或项目 `.claude/settings.json` | `~/.claude.json` |
| **配置内容** | 权限、环境变量、模型、沙箱 | 主题、认证、MCP 服务器列表 |
| **项目级** | ✅ 支持 | ❌ 仅用户级 |
| **版本控制** | 可提交（团队共享） | 不提交（个人配置） |

---

## settings.json 详解

### 作用

`settings.json` 是 Claude Code 的核心配置文件，用于：
- 🔒 **权限控制**：定义 Claude 可以执行的操作
- 🌍 **环境变量**：设置运行时环境
- 🤖 **模型选择**：指定使用的 AI 模型
- 🛡️ **沙箱配置**：控制安全执行环境
- 📝 **输出风格**：定制 Claude 的回复方式

### 完整配置示例

#### 用户级配置 (`~/.claude/settings.json`)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  // 模型选择
  "model": "claude-sonnet-4-5-20250929",

  // 权限控制
  "permissions": {
    // 自动允许的操作
    "allow": [
      "Bash(npm run *)",
      "Bash(npm run test *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git commit *)",
      "Read(~/.zshrc)",
      "Read(package.json)",
      "Read(tsconfig.json)"
    ],

    // 自动拒绝的操作
    "deny": [
      "Bash(git push *)",
      "Bash(curl *)",
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.ssh/*)",
      "WebFetch(domain:internal-api.com)"
    ],

    // 需要询问的操作
    "ask": [
      "Bash(git push origin main)",
      "Bash(npm publish)",
      "Write(.github/workflows/*)"
    ]
  },

  // 环境变量
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "40000",
    "DISABLE_COST_WARNINGS": "1",
    "NODE_ENV": "development"
  },

  // 沙箱配置
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "sudo", "systemctl"],
    "network": {
      "allowedDomains": [
        "github.com",
        "*.npmjs.org",
        "api.github.com",
        "registry.npmjs.org"
      ],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  },

  // Git 归属配置
  "attribution": {
    "commit": {
      "prefix": "🤖 AI 生成:",
      "suffix": "Co-Authored-By: Claude <noreply@anthropic.com>"
    },
    "pr": {
      "prefix": "[Claude Code]",
      "suffix": "由 Claude Code 辅助生成"
    }
  },

  // 输出风格
  "outputStyle": "Explanatory",

  // 语言偏好
  "language": "zh-CN",

  // 自动保存
  "autoSave": true,

  // 技能目录
  "skillsDirectories": [
    "~/.claude/skills",
    "./.claude/skills"
  ]
}
```

#### 项目级配置 (`.claude/settings.json`)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  // 项目特定模型
  "model": "claude-opus-4-20250514",

  // 项目权限
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm run build)",
      "Bash(npm test)",
      "Read(src/**)",
      "Write(src/**)",
      "Read(tests/**)",
      "Write(tests/**)"
    ],
    "deny": [
      "Read(.env.production)",
      "Bash(npm run deploy)"
    ]
  },

  // 项目环境变量
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "app:*"
  },

  // 项目输出风格
  "outputStyle": "Concise"
}
```

### 配置项详解

#### 1. 权限控制 (permissions)

权限使用 **glob 模式** 匹配：

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",           // 精确匹配
      "Bash(npm run *)",            // 通配符匹配
      "Read(src/**/*.ts)",          // 递归匹配
      "Write(!src/config.ts)",      // 排除特定文件
      "WebFetch(domain:github.com)" // 域名限制
    ]
  }
}
```

**支持的工具类型**：
- `Bash()` - Shell 命令
- `Read()` - 读取文件
- `Write()` - 写入文件
- `Edit()` - 编辑文件
- `WebFetch()` - 网络请求
- `Grep()` - 搜索文件
- `Glob()` - 文件匹配

#### 2. 沙箱配置 (sandbox)

```json
{
  "sandbox": {
    // 启用沙箱
    "enabled": true,

    // 沙箱中自动允许 Bash
    "autoAllowBashIfSandboxed": true,

    // 排除的命令（即使在沙箱中也不允许）
    "excludedCommands": ["docker", "sudo", "systemctl"],

    // 网络配置
    "network": {
      // 允许的域名
      "allowedDomains": [
        "github.com",
        "*.npmjs.org"
      ],

      // 允许的 Unix Socket
      "allowUnixSockets": ["/var/run/docker.sock"],

      // 允许本地端口绑定
      "allowLocalBinding": true
    }
  }
}
```

#### 3. 输出风格 (outputStyle)

```json
{
  "outputStyle": "Explanatory"  // 或 "Concise"
}
```

- **Explanatory**（详细）：提供详细解释和上下文
- **Concise**（简洁）：简短直接的回复

#### 4. 环境变量 (env)

```json
{
  "env": {
    // Claude Code 特定变量
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "40000",
    "DISABLE_COST_WARNINGS": "1",

    // 项目环境变量
    "NODE_ENV": "development",
    "DEBUG": "app:*",
    "API_BASE_URL": "http://localhost:3000"
  }
}
```

---

## .claude.json 详解

### 作用

`.claude.json` 是用户级配置文件，主要用于：
- 🎨 **UI 主题**：配置界面外观
- 🔐 **OAuth 认证**：管理第三方服务认证
- 🔌 **MCP 服务器**：配置 Model Context Protocol 服务器

### 完整配置示例

```json
{
  "$schema": "https://json.schemastore.org/claude-config.json",

  // UI 主题配置
  "theme": {
    "mode": "dark",
    "accentColor": "#8B5CF6",
    "fontFamily": "JetBrains Mono, Consolas, monospace",
    "fontSize": 14
  },

  // OAuth 配置
  "oauth": {
    "github": {
      "clientId": "your-github-client-id",
      "scopes": ["repo", "read:user"]
    },
    "notion": {
      "clientId": "your-notion-client-id",
      "scopes": ["read_content", "update_content"]
    }
  },

  // MCP 服务器配置
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"],
      "env": {
        "NODE_ENV": "production"
      }
    },

    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },

    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/mcp-server-notion"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    },

    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
      "env": {
        "PGPASSWORD": "${DB_PASSWORD}"
      }
    },

    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "env": {}
    }
  },

  // 编辑器配置
  "editor": {
    "tabSize": 2,
    "insertSpaces": true,
    "wordWrap": "on",
    "minimap": {
      "enabled": true
    }
  },

  // 遥测配置
  "telemetry": {
    "enabled": true,
    "crashReports": true
  }
}
```

### MCP 服务器配置详解

MCP (Model Context Protocol) 服务器为 Claude 提供额外的能力：

#### 常用 MCP 服务器

1. **文件系统服务器**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
    "env": {}
  }
}
```

2. **GitHub 服务器**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

3. **Notion 服务器**
```json
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/mcp-server-notion"],
    "env": {
      "NOTION_API_KEY": "${NOTION_API_KEY}"
    }
  }
}
```

4. **数据库服务器**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
    "env": {
      "PGPASSWORD": "${DB_PASSWORD}"
    }
  }
}
```

5. **浏览器自动化服务器**
```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
    "env": {}
  }
}
```

#### 环境变量引用

使用 `${VAR_NAME}` 语法引用系统环境变量：

```json
{
  "mcpServers": {
    "myserver": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

---

## 配置优先级

配置文件按以下优先级加载（后者覆盖前者）：

```
1. 系统级配置 (managed-settings.json)
   ↓
2. 用户级配置 (~/.claude/settings.json)
   ↓
3. 项目级配置 (.claude/settings.json)
   ↓
4. 本地覆盖配置 (.claude/settings.local.json)
```

### 示例：配置合并

**用户级配置** (`~/.claude/settings.json`):
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": ["Bash(git status)"]
  }
}
```

**项目级配置** (`.claude/settings.json`):
```json
{
  "model": "claude-opus-4-20250514",
  "permissions": {
    "allow": ["Bash(npm run dev)"]
  }
}
```

**最终生效配置**:
```json
{
  "model": "claude-opus-4-20250514",  // 项目级覆盖
  "permissions": {
    "allow": [
      "Bash(git status)",              // 用户级
      "Bash(npm run dev)"              // 项目级（合并）
    ]
  }
}
```

---

## 实用配置示例

### 1. 前端开发项目

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(yarn *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read(src/**)",
      "Write(src/**)",
      "Read(public/**)",
      "Write(public/**)",
      "Read(package.json)",
      "Write(package.json)"
    ],
    "deny": [
      "Read(.env.production)",
      "Bash(npm publish)",
      "Bash(git push *)"
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "VITE_API_URL": "http://localhost:3000"
  },
  "outputStyle": "Explanatory"
}
```

### 2. 后端 API 项目

```json
{
  "model": "claude-opus-4-20250514",
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm test)",
      "Bash(docker-compose up -d)",
      "Read(src/**)",
      "Write(src/**)",
      "Read(tests/**)",
      "Write(tests/**)",
      "Read(prisma/**)",
      "Write(prisma/**)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.production)",
      "Bash(npm run migrate:prod)",
      "Bash(kubectl *)"
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "DATABASE_URL": "postgresql://localhost:5432/dev"
  },
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["localhost", "*.docker.internal"],
      "allowLocalBinding": true
    }
  }
}
```

### 3. 数据科学项目

```json
{
  "model": "claude-opus-4-20250514",
  "permissions": {
    "allow": [
      "Bash(python *)",
      "Bash(jupyter *)",
      "Bash(pip install *)",
      "Read(notebooks/**)",
      "Write(notebooks/**)",
      "Read(data/**)",
      "Write(output/**)"
    ],
    "deny": [
      "Write(data/**)",
      "Bash(rm -rf *)"
    ]
  },
  "env": {
    "PYTHONPATH": "./src",
    "JUPYTER_CONFIG_DIR": "./.jupyter"
  }
}
```

### 4. 严格安全项目

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": [
      "Read(src/**/*.ts)",
      "Read(tests/**/*.test.ts)"
    ],
    "deny": [
      "Bash(*)",
      "Write(*)",
      "WebFetch(*)"
    ],
    "ask": [
      "Write(src/**)",
      "Bash(npm test)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": false,
    "network": {
      "allowedDomains": []
    }
  },
  "outputStyle": "Concise"
}
```

---

## 最佳实践

### 1. 版本控制策略

#### 应该提交到 Git 的文件：
```gitignore
# 提交团队共享配置
.claude/settings.json
.claude/CLAUDE.md
.claude/skills/
.mcp.json
```

#### 不应该提交的文件：
```gitignore
# .gitignore
.claude/settings.local.json
.claude/CLAUDE.local.md
.claude/projects/
~/.claude.json
~/.claude/settings.json
```

### 2. 团队协作配置

**项目配置** (`.claude/settings.json`) - 团队共享：
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm test)",
      "Read(src/**)",
      "Write(src/**)"
    ]
  },
  "outputStyle": "Explanatory"
}
```

**本地覆盖** (`.claude/settings.local.json`) - 个人使用：
```json
{
  "model": "claude-opus-4-20250514",
  "env": {
    "DEBUG": "app:*"
  }
}
```

### 3. 安全配置建议

#### ✅ 推荐做法：

1. **使用白名单而非黑名单**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm test)"
    ]
    // 默认拒绝其他所有操作
  }
}
```

2. **敏感文件明确拒绝**
```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(secrets/**)",
      "Read(~/.ssh/*)",
      "Read(~/.aws/*)"
    ]
  }
}
```

3. **危险操作需要确认**
```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(npm publish)",
      "Bash(rm -rf *)",
      "Write(.github/workflows/*)"
    ]
  }
}
```

4. **启用沙箱**
```json
{
  "sandbox": {
    "enabled": true,
    "excludedCommands": ["sudo", "docker", "systemctl"]
  }
}
```

#### ❌ 避免做法：

```json
{
  "permissions": {
    "allow": ["Bash(*)", "Read(*)", "Write(*)"]  // 过于宽松
  },
  "sandbox": {
    "enabled": false  // 禁用安全保护
  }
}
```

### 4. 环境变量管理

使用环境变量而非硬编码：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"  // ✅ 引用环境变量
      }
    }
  }
}
```

在 shell 配置文件中设置：
```bash
# ~/.zshrc 或 ~/.bashrc
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export NOTION_API_KEY="secret_xxxxxxxxxxxx"
```

### 5. 模块化配置

使用 `.claude/rules/` 目录组织复杂规则：

```
.claude/
├── settings.json
├── CLAUDE.md
└── rules/
    ├── security.md      # 安全规则
    ├── coding-style.md  # 代码风格
    └── testing.md       # 测试规范
```

**settings.json** 引用规则：
```json
{
  "rulesDirectories": [".claude/rules"]
}
```

### 6. 项目模板

创建项目模板快速初始化：

```bash
# 创建模板目录
mkdir -p ~/.claude/templates/web-app/.claude

# 模板配置
cat > ~/.claude/templates/web-app/.claude/settings.json << 'EOF'
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Read(src/**)",
      "Write(src/**)"
    ]
  }
}
EOF

# 使用模板
cp -r ~/.claude/templates/web-app/.claude ./my-new-project/
```

---

## 常见问题

### Q1: 配置不生效怎么办？

1. 检查 JSON 语法是否正确
2. 重启 Claude Code
3. 查看配置优先级是否被覆盖
4. 检查文件路径是否正确

### Q2: 如何调试权限问题？

启用详细日志：
```json
{
  "env": {
    "CLAUDE_CODE_LOG_LEVEL": "debug"
  }
}
```

### Q3: MCP 服务器无法连接？

1. 检查命令是否可执行：`npx -y @modelcontextprotocol/server-filesystem`
2. 验证环境变量是否设置
3. 查看 MCP 服务器日志

### Q4: 如何在多个项目间共享配置？

使用符号链接：
```bash
ln -s ~/.claude/shared-settings.json ./project/.claude/settings.json
```

---

## 总结

### settings.json 核心要点

- 📍 **位置**：`~/.claude/settings.json` (用户级) 或 `.claude/settings.json` (项目级)
- 🎯 **作用**：控制 Claude 的行为、权限、环境
- 🔑 **关键配置**：permissions, env, sandbox, model
- 📦 **版本控制**：项目级可提交，用户级不提交

### .claude.json 核心要点

- 📍 **位置**：`~/.claude.json` (仅用户级)
- 🎯 **作用**：UI 配置、OAuth、MCP 服务器
- 🔑 **关键配置**：theme, oauth, mcpServers
- 📦 **版本控制**：不提交（包含个人凭证）

### 配置建议

1. ✅ 使用白名单权限策略
2. ✅ 敏感文件明确拒绝访问
3. ✅ 启用沙箱保护
4. ✅ 环境变量外部化
5. ✅ 项目配置版本控制
6. ✅ 本地覆盖个人配置

---

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [MCP 协议规范](https://modelcontextprotocol.io)
- [JSON Schema 验证](https://json.schemastore.org/claude-code-settings.json)

---

**文档版本**: 1.0
**最后更新**: 2024年
**适用版本**: Claude Code 0.7+
