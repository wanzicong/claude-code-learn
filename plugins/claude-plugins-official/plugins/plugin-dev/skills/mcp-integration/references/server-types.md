# MCP 服务器类型深入解析

Claude Code 插件支持的所有 MCP 服务器类型的完整参考。

## stdio（标准输入/输出）

### 概述

通过 stdin/stdout 通信以子进程方式执行本地 MCP 服务器。最适合本地工具、自定义服务器和 NPM 包。

### 配置

**基本配置：**
```json
{
  "my-server": {
    "command": "npx",
    "args": ["-y", "my-mcp-server"]
  }
}
```

**带环境变量：**
```json
{
  "my-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/custom-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "API_KEY": "${MY_API_KEY}",
      "LOG_LEVEL": "debug",
      "DATABASE_URL": "${DB_URL}"
    }
  }
}
```

### 进程生命周期

1. **启动**：Claude Code 使用 `command` 和 `args` 生成进程
2. **通信**：通过 stdin/stdout 进行 JSON-RPC 消息传递
3. **生命周期**：进程在整个 Claude Code 会话期间运行
4. **关闭**：Claude Code 退出时终止进程

### 使用场景

**NPM 包：**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
  }
}
```

**自定义脚本：**
```json
{
  "custom": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server.js",
    "args": ["--verbose"]
  }
}
```

**Python 服务器：**
```json
{
  "python-server": {
    "command": "python",
    "args": ["-m", "my_mcp_server"],
    "env": {
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

### 最佳实践

1. **使用绝对路径或 ${CLAUDE_PLUGIN_ROOT}**
2. **为 Python 服务器设置 PYTHONUNBUFFERED**
3. **通过 args 或 env 传递配置，而非 stdin**
4. **优雅地处理服务器崩溃**
5. **记录到 stderr，而非 stdout（stdout 用于 MCP 协议）**

### 故障排除

**服务器无法启动：**
- 检查命令存在且可执行
- 验证文件路径正确
- 检查权限
- 查看 `claude --debug` 日志

**通信失败：**
- 确保服务器正确使用 stdin/stdout
- 检查是否有杂散的 print/console.log 语句
- 验证 JSON-RPC 格式

## SSE（服务器发送事件）

### 概述

通过 HTTP 和服务器发送事件以流方式连接到托管的 MCP 服务器。最适合云服务和 OAuth 身份验证。

### 配置

**基本配置：**
```json
{
  "hosted-service": {
    "type": "sse",
    "url": "https://mcp.example.com/sse"
  }
}
```

**带请求头：**
```json
{
  "service": {
    "type": "sse",
    "url": "https://mcp.example.com/sse",
    "headers": {
      "X-API-Version": "v1",
      "X-Client-ID": "${CLIENT_ID}"
    }
  }
}
```

### 连接生命周期

1. **初始化**：建立到 URL 的 HTTP 连接
2. **握手**：MCP 协议协商
3. **流式传输**：服务器通过 SSE 发送事件
4. **请求**：客户端发送 HTTP POST 进行工具调用
5. **重连**：断开连接时自动重连

### 身份验证

**OAuth（自动）：**
```json
{
  "asana": {
    "type": "sse",
    "url": "https://mcp.asana.com/sse"
  }
}
```

Claude Code 处理 OAuth 流程：
1. 首次使用时提示用户进行身份验证
2. 打开浏览器进行 OAuth 流程
3. 安全存储令牌
4. 自动令牌刷新

**自定义请求头：**
```json
{
  "service": {
    "type": "sse",
    "url": "https://mcp.example.com/sse",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

### 使用场景

**官方服务：**
- Asana：`https://mcp.asana.com/sse`
- GitHub：`https://mcp.github.com/sse`
- 其他托管的 MCP 服务器

**自定义托管服务器：**
部署您自己的 MCP 服务器并通过 HTTPS + SSE 暴露。

### 最佳实践

1. **始终使用 HTTPS，不要使用 HTTP**
2. **在可用时让 OAuth 处理身份验证**
3. **对令牌使用环境变量**
4. **优雅地处理连接失败**
5. **记录所需的 OAuth 范围**

### 故障排除

**连接拒绝：**
- 检查 URL 正确且可访问
- 验证 HTTPS 证书有效
- 检查网络连接性
- 查看防火墙设置

**OAuth 失败：**
- 清除缓存的令牌
- 检查 OAuth 范围
- 验证重定向 URL
- 重新进行身份验证

## HTTP（REST API）

### 概述

通过标准 HTTP 请求连接到 RESTful MCP 服务器。最适合基于令牌的身份验证和无状态交互。

### 配置

**基本配置：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp"
  }
}
```

**带身份验证：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}",
      "Content-Type": "application/json",
      "X-API-Version": "2024-01-01"
    }
  }
}
```

### 请求/响应流程

1. **工具发现**：GET 以发现可用工具
2. **工具调用**：POST 并带有工具名称和参数
3. **响应**：包含结果或错误的 JSON 响应
4. **无状态**：每个请求独立

### 身份验证

**基于令牌：**
```json
{
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

**API 密钥：**
```json
{
  "headers": {
    "X-API-Key": "${API_KEY}"
  }
}
```

**自定义身份验证：**
```json
{
  "headers": {
    "X-Auth-Token": "${AUTH_TOKEN}",
    "X-User-ID": "${USER_ID}"
  }
}
```

### 使用场景

- REST API 后端
- 内部服务
- 微服务
- 无服务器函数

### 最佳实践

1. **对所有连接使用 HTTPS**
2. **将令牌存储在环境变量中**
3. **为瞬时故障实现重试逻辑**
4. **处理速率限制**
5. **设置适当的超时**

### 故障排除

**HTTP 错误：**
- 401：检看身份验证请求头
- 403：验证权限
- 429：实现速率限制
- 500：检看服务器日志

**超时问题：**
- 如需要则增加超时
- 检查服务器性能
- 优化工具实现

## WebSocket（实时）

### 概述

通过 WebSocket 连接到 MCP 服务器以实现实时双向通信。最适合流式传输和低延迟应用。

### 配置

**基本配置：**
```json
{
  "realtime": {
    "type": "ws",
    "url": "wss://mcp.example.com/ws"
  }
}
```"

**带身份验证：**
```json
{
  "realtime": {
    "type": "ws",
    "url": "wss://mcp.example.com/ws",
    "headers": {
      "Authorization": "Bearer ${TOKEN}",
      "X-Client-ID": "${CLIENT_ID}"
    }
  }
}
```

### 连接生命周期

1. **握手**：WebSocket 升级请求
2. **连接**：持久双向通道
3. **消息**：通过 WebSocket 进行 JSON-RPC
4. **心跳**：保持活动消息
5. **重连**：断开连接时自动

### 使用场景

- 实时数据流传输
- 实时更新和通知
- 协作编辑
- 低延迟工具调用
- 来自服务器的推送通知

### 最佳实践

1. **使用 WSS（安全 WebSocket），不要使用 WS**
2. **实现心跳/ping-pong**
3. **处理重连逻辑**
4. **断开连接期间缓冲消息**
5. **设置连接超时**

### 故障排除

**连接掉线：**
- 实现重连逻辑
- 检查网络稳定性
- 验证服务器支持 WebSocket
- 查看防火墙设置

**消息传递：**
- 实现消息确认
- 处理乱序消息
- 断开连接期间缓冲

## 对比矩阵

| 功能 | stdio | SSE | HTTP | WebSocket |
|---------|-------|-----|------|-----------|
| **传输** | 进程 | HTTP/SSE | HTTP | WebSocket |
| **方向** | 双向 | 服务器→客户端 | 请求/响应 | 双向 |
| **状态** | 有状态 | 有状态 | 无状态 | 有`状态 |
| **身份验证** | 环境变量 | OAuth/请求头 | 请求头 | 请求头 |
| **使用场景** | 本地工具 | 云服务 | REST API | 实时 |
| **延迟** | 最低 | 中等 | 中等 | 低 |
| **设置** | 容易 | 中等 | 容易 | 中等 |
| **重连** | 进程重启 | 自动 | 不适用 | 自动 |

## 选择正确的类型

**使用 stdio 当：**
- 运行本地工具或自定义服务器
- 需要最低延迟
- 使用文件系统或本地数据库
- 随插件分发服务器

**使用 SSE 当：**
- 连接到托管服务
- 需要 OAuth 身份验证
- 使用官方 MCP 服务器（Asana、GitHub）
- 希望自动重连

`**使用 HTTP 当：**
- 与 REST API 集成
- 需要无状态交互
- 使用基于令牌的身份验证
- 简单的请求/响应模式

**使用 WebSocket 当：**
- 需要实时更新
- 构建协作功能
- 低延迟至关重要
- 需要双向流式传输

## 类型之间迁移

### 从 stdio 到 SSE

**之前（stdio）：**
```json
{
  "local-server": {
    "command": "node",
    "args": ["server.js"]
  }
}
```

**之后（SSE - 部署服务器）：**
```json
{
  "hosted-server": {
    "type": "sse",
    "url": "https://mcp.example.com/sse"
  }
}
```

### 从 HTTP 到 WebSocket

**之前（HTTP）：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp"
  }
}
```

**之后（WebSocket）：**
```json
{
  "realtime": {
    "type": "ws",
    "url": "wss://api.example.com/ws"
  }
}
```

优点：实时更新、更低延迟、双向通信。

## 高级配置

### 多个服务器

组合不同类型：

```json
{
  "local-db": {
    "command": "npx",
    "args": ["-y", "mcp-server-sqlite", "./data.db"]
  },
  "cloud-api": {
    "type": "sse",
    "url": "https://mcp.example.com/sse"
  },
  "internal-service": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

### 条件配置

使用环境变量切换服务器：

```json
{
  "api": {
    "type": "http",
    "url": "${API_URL}",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

为开发/生产环境设置不同的值：
- 开发：`API_URL=http://localhost:8080/mcp`
- 生产：`API_URL=https://api.production.com/mcp`

## 安全考虑

### Stdio 安全

- 验证命令路径
- 不执行用户提供的命令
- 限制环境变量访问
- 限制文件系统访问

### 网络安全

- 始终使用 HTTPS/WSS
- 验证 SSL 证书
- 不要跳过证书验证
- 使用安全令牌存储

### 令牌管理

- 永远不硬编码令牌
- 使用环境变量
- 定期轮换令牌
- 实现令牌刷新
- 记录所需的范围

## 结论

根据您的用例选择 MCP 服务器类型：
- **stdio** 用于本地、自定义或 NPM 打包的服务器
- **SSE** 用于具有 OAuth 的托管服务
- **HTTP** 用于具有令牌认证的 REST API
- **WebSocket** 用于实时双向通信

彻底测试并优雅地处理错误以实现稳健的 MCP 集成。
