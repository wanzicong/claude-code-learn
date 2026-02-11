# MCP 身份验证模式

Claude Code 插件中 MCP 服务器身份验证方法的完整指南。

## 概述

MCP 服务器根据服务器类型和服务需求支持多种身份验证方法。选择最符合您用例和安全要求的方法。

## OAuth（自动）

### 工作原理

Claude Code 自动为 SSE 和 HTTP 服务器处理完整的 OAuth 2.0 流程：

1. 用户尝试使用 MCP 工具
2. Claude Code 检测到需要身份验证
3. 打开浏览器以获取 OAuth 同意
4. 用户在浏览器中授权
5. Claude Code 安全地存储令牌
6. 自动令牌刷新

### 配置

```json
{
  "service": {
    "type": "sse",
    "url": "https://mcp.example.com/sse"
  }
}
```

无需额外的身份验证配置！Claude Code 处理一切。

### 支持的服务

**已知的支持 OAuth 的 MCP 服务器：**
- Asana：`https://mcp.asana.com/sse`
- GitHub（如果可用）
- Google 服务（如果可用）
- 自定义 OAuth 服务器

### OAuth 范围

OAuth 范围由 MCP 服务器确定。用户在同意思步期间看到所需的范围。

**在您的 README 中记录所需的范围：**
```markdown
## 身份验证

此插件需要以下 Asana 权限：
- 读取任务和项目
- 创建和更新任务
- 访问工作空间数据
```

### 令牌存储

令牌由 Claude Code 安全存储：
- 插件无法访问
- 加密存储
- 自动刷新
- 登出时清除

### OAuth 故障排除

**身份验证循环：**
- 清除缓存的令牌（登出并重新登录）
- 检查 OAuth 重定向 URL
- 验证服务器 OAuth 配置

**范围问题：**
- 用户可能需要为新范围重新授权
- 检查服务器文档所需的范围

**令牌过期：**
- Claude Code 自动刷新
- 如果刷新失败，提示重新验证

## 基于令牌的身份验证

### Bearer 令牌

HTTP 和 WebSocket 服务器最常用。

**配置：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

**环境变量：**
```bash
export API_TOKEN="your-secret-token-here"
```

### API 密钥

Bearer 令牌的替代方案，常用于自定义标头。

**配置：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "X-API-Key": "${API_KEY}",
      "X-API-Secret": "${API_SECRET}"
    }
  }
}
```

### 自定义标头

服务可能使用自定义身份验证标头。

**配置：**
```json
{
  "service": {
    "type": "sse",
    "url": "https://mcp.example.com/sse",
    "headers": {
      "X-Auth-Token": "${AUTH_TOKEN}",
      "X-User-ID": "${USER_ID}",
      "X-Tenant-ID": "${TENANT_ID}"
    }
  }
}
```

### 记录令牌要求

始终在您的 README 中记录：

```markdown
## 设置

### 所需环境变量

在使用插件之前设置这些环境变量：

```bash
export API_TOKEN="your-token-here"
export API_SECRET="your-secret-here"
```

### 获取令牌

1. 访问 https://api.example.com/tokens
2. 创建新的 API 令牌
3. 复制令牌和密钥
4. 按所示设置环境变量

### 令牌权限

API 令牌需要以下权限：
- 资源的读取访问
- 创建项目的写入访问
- 删除访问（可选，用于清理操作）
```

## 环境变量身份验证（stdio）

### 将凭据传递给服务器

对于 stdio 服务器，通过环境变量传递凭据：

```json
{
  "database": {
    "command": "python",
    "args": ["-m", "mcp_server_db"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}",
      "DB_USER": "${DB_USER}",
      "DB_PASSWORD": "${DB_PASSWORD}"
    }
  }
}
```

### 用户环境变量

```bash
# 用户在其 shell 中设置这些
export DATABASE_URL="postgresql://localhost/mydb"
export DB_USER="myuser"
export DB_PASSWORD="mypassword"
```

### 文档模板

```markdown
## 数据库配置

设置这些环境变量：

```bash
export DATABASE_URL="postgresql://host:port/database"
export DB_USER="username"
export DB_PASSWORD="password"
```

或创建 `.env` 文件（添加到 `.gitignore`）：

```
DATABASE_URL=postgresql://localhost:5432/mydb
DB_USER=myuser
DB_PASSWORD=mypassword
```

使用 \`source .env\` 或 \`export $(cat .env | xargs)\` 加载
```

## 动态标头

### 标头帮助程序脚本

对于会更改或过期的令牌，使用帮助程序脚本：

```json
{
  "api": {
    "type": "sse",
    "url": "https://api.example.com",
    "headersHelper": "${CLAUDE_PLUGIN_ROOT}/scripts/get-headers.sh"
  }
}
```

**脚本 (get-headers.sh)：**
```bash
#!/bin/bash
# 生成动态身份验证标头

# 获取新令牌
TOKEN=$(get-fresh-token-from-somewhere)

# 输出 JSON 标头
cat <<EOF
{
  "Authorization": "Bearer $TOKEN",
  "X-Timestamp": "$(date -Iseconds)"
}
EOF
```

### 动态标头的用例

- 短期存活的令牌，需要刷新
- 具有 HMAC 签名的令牌
- 基于时间的身份验证
- 动态租户/工作空间选择

## 安全最佳实践

### 做

✅ **使用环境变量：**
```json
{
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

✅ **在 README 中记录所需的变量**

✅ **始终使用 HTTPS/WSS**

✅ **实施令牌轮换**

✅ **安全地存储令牌（环境变量，而非文件）**

✅ **让 OAuth 处理可用时的身份验证**

### 不要做

❌ **硬编码令牌：**
```json
{
  "headers": {
    "Authorization": "Bearer sk-abc123..."  // 永不！
  }
}
```

❌ **将令牌提交到 git**

❌ **在文档中分享令牌**

❌ **使用 HTTP 而非 HTTPS**

❌ **将令牌存储在插件文件中**

❌ **记录令牌或敏感标头**

## 多租户模式

### 工作空间/租户选择

**通过环境变量：**
```json
{
  "api": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}",
      "X-Workspace-ID": "${WORKSPACE_ID}"
    }
  }
}
```

**通过 URL：**
```json
{
  "api": {
    "type": "http",
    "url": "https://${TENANT_ID}.api.example.com/mcp"
  }
}
```

### 每用户配置

用户设置自己的工作空间：

```bash
export WORKSPACE_ID="my-workspace-123"
export TENANT_ID="my-company"
```

## 身份验证故障排除

### 常见问题

**401 未授权：**
- 检查令牌是否正确设置
- 验证令牌未过期
- 检查令牌具有所需权限
- 确保标头格式正确

**403 禁止：**
- 令牌有效但缺少权限
- 检查范围/权限
- 验证工作空间/租户 ID
- 可能需要管理员批准

**未找到令牌：**
```bash
# 检查环境变量是否设置
echo $API_TOKEN

# 如果为空，设置它
export API_TOKEN="your-token"
```

**令牌格式错误：**
```json
// 正确
"Authorization": "Bearer sk-abc123"

// 错误
"Authorization": "sk-abc123"
```

### 调试身份验证

**启用调试模式：**
```bash
claude --debug
```

查找：
- 身份验证标头值（已清理）
- OAuth 流程进度
- 令牌刷新尝试
- 身份验证错误

**分别测试身份验证：**
```bash
# 测试 HTTP端点
curl -H "Authorization: Bearer $API_TOKEN" \
     https://api.example.com/mcp/health

# 应该返回 200 OK
```

## 迁移模式

### 从硬编码到环境变量

**之前：**
```json
{
  "headers": {
    "Authorization": "Bearer sk-hardcoded-token"
  }
}
```

**之后：**
```json
{
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

**迁移步骤：**
1. 在插件 README 中添加环境变量
2. 更新配置以使用 ${VAR}
3. 使用设置的变量进行测试
4. 移除硬编码值
5. 提交更改

### 从 Basic Auth 到 OAuth

**之前：**
```json
{
  "headers": {
    "Authorization": "Basic ${BASE64_CREDENTIALS}"
  }
}
```

**之后：**
```json
{
  "type": "sse",
  "url": "https://mcp.example.com/sse"
}
```

**好处：**
- 更好的安全性
- 无凭据管理
- 自动令牌刷新
- 限制的范围

## 高级身份验证

### 双向 TLS (mTLS)

一些企业服务需要客户端证书。

**MCP 配置中不直接支持。**

**变通方法：** 将其包装在处理 mTLS 的 stdio 服务器中：

```json
{
  "secure-api": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/mtls-wrapper",
    "args": ["--cert", "${CLIENT_CERT}", "--key", "${CLIENT_KEY}"],
    "env": {
      "API_URL": "https://secure.example.com"
    }
  }
}
```

### JWT 令牌

使用标头帮助程序动态生成 JWT 令牌：

```bash
#!/bin/bash
# generate-jwt.sh

# 生成 JWT（使用库或 API 调用）
JWT=$(generate-jwt-token)

echo "{\"Authorization\": \"Bearer $JWT\"}"
```

```json
{
  "headersHelper": "${CLAUDE_PLUGIN_ROOT}/scripts/generate-jwt.sh"
}
```

### HMAC 签名

对于需要请求签名的 API：

```bash
#!/bin/bash
# generate-hmac.sh

TIMESTAMP=$(date - -Iseconds)
SIGNATURE=$(echo -n "$TIMESTAMP" | openssl dgst -sha256 -hmac "$SECRET_KEY" | cut -d' ' -f2)

cat <<EOF
{
  "X-Timestamp": "$TIMESTAMP",
  "X-Signature": "$SIGNATURE",
  "X-API-Key": "$API_KEY"
}
EOF
```

## 最佳实践摘要

### 对于插件开发者

1. **当服务支持时，首选 OAuth**
2. **令牌使用环境变量**
3. **在 README 中记录所有所需变量**
4. **提供带有示例的设置说明**
5. **永不提交凭据**
6. **仅使用 HTTPS/WSS**
7. **彻底测试身份验证**

### 对于插件用户

1. **在使用插件之前设置环境变量**
2. **安全地保护令牌并保持私密**
3. **定期轮换令牌**
4. **为开发/生产使用不同的令牌**
5. **不要将 .env 文件提交到 git**
6. **授权前审查 OAuth 范围**

##根据您的 MCP 服务器的需求选择身份验证方法：

- **OAuth** 用于云服务（对用户最简单）
- **Bearer 令牌** 用于 API 服务
- **环境变量** 用于 stdio 服务器
- **动态标头** 用于复杂身份验证流

始终优先考虑安全性并提供清晰的用户设置文档。
