# MCP 服务器设计指南

## 什么是 MCP

Model Context Protocol (MCP) 是一个开放协议，使 LLM 能够通过标准化接口与外部服务交互。

### MCP 核心概念

**工具 (Tools)** - LLM 可以调用的函数
**资源 (Resources)** - LLM 可以读取的数据
**提示 (Prompts)** - 预定义的提示模板
**传输 (Transport)** - 通信机制（stdio 或 HTTP）

## 设计原则

### 1. 单一职责原则

每个 MCP 服务器应专注于一个特定服务或领域。

**✅ 好的设计**:
- `github-mcp` - 专注于 GitHub 操作
- `notion-mcp` - 专注于 Notion 集成
- `slack-mcp` - 专注于 Slack 通信

**❌ 不好的设计**:
- `all-in-one-mcp` - 试图集成所有服务

### 2. 工具粒度原则

工具应该是原子操作，可组合成复杂工作流。

**✅ 好的粒度**:
```typescript
// 细粒度工具
- create_issue
- update_issue
- close_issue
- add_comment
```

**❌ 不好的粒度**:
```typescript
// 过于粗粒度
- manage_issue  // 做太多事情
```

### 3. 错误处理原则

提供清晰的错误信息和恢复建议。

```typescript
try {
  const result = await apiCall();
  return { success: true, data: result };
} catch (error) {
  return {
    success: false,
    error: error.message,
    suggestion: "请检查 API 密钥是否有效"
  };
}
```

### 4. 文档完整性原则

每个工具必须有清晰的描述和输入模式。

```typescript
{
  name: "create_issue",
  description: "在 GitHub 仓库中创建新问题。需要仓库名称、问题标题和描述。",
  inputSchema: {
    type: "object",
    properties: {
      repo: {
        type: "string",
        description: "仓库名称，格式: owner/repo"
      },
      title: {
        type: "string",
        description: "问题标题"
      },
      body: {
        type: "string",
        description: "问题描述（支持 Markdown）"
      }
    },
    required: ["repo", "title"]
  }
}
```

## TypeScript 实现指南

### 项目结构

```
mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # 服务器入口
│   ├── tools/                # 工具实现
│   │   ├── tool1.ts
│   │   ├── tool2.ts
│   │   └── index.ts
│   ├── resources/            # 资源实现
│   │   └── index.ts
│   ├── types.ts              # 类型定义
│   └── utils.ts              # 工具函数
├── tests/
│   ├── tools.test.ts
│   └── integration.test.ts
└── README.md
```

### 基础服务器实现

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// 导入工具
import { createIssueTool, listIssuesTool } from './tools/index.js';

const server = new Server(
  {
    name: 'github-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 注册工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'create_issue',
      description: '创建 GitHub 问题',
      inputSchema: {
        type: 'object',
        properties: {
          repo: { type: 'string', description: '仓库名称' },
          title: { type: 'string', description: '问题标题' },
          body: { type: 'string', description: '问题描述' },
        },
        required: ['repo', 'title'],
      },
    },
    {
      name: 'list_issues',
      description: '列出仓库问题',
      inputSchema: {
        type: 'object',
        properties: {
          repo: { type: 'string', description: '仓库名称' },
          state: {
            type: 'string',
            enum: ['open', 'closed', 'all'],
            description: '问题状态'
          },
        },
        required: ['repo'],
      },
    },
  ],
}));

// 注册工具调用处理
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'create_issue':
      return await createIssueTool(args);
    case 'list_issues':
      return await listIssuesTool(args);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('GitHub MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
```

### 工具实现模式

```typescript
// src/tools/createIssue.ts
import { Octokit } from '@octokit/rest';

interface CreateIssueArgs {
  repo: string;
  title: string;
  body?: string;
}

export async function createIssueTool(args: CreateIssueArgs) {
  const { repo, title, body } = args;

  // 验证输入
  if (!repo.includes('/')) {
    return {
      content: [
        {
          type: 'text',
          text: '错误: 仓库名称格式应为 owner/repo',
        },
      ],
      isError: true,
    };
  }

  const [owner, repoName] = repo.split('/');

  try {
    // 调用 API
    const octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN,
    });

    const response = await octokit.issues.create({
      owner,
      repo: repoName,
      title,
      body: body || '',
    });

    // 返回结果
    return {
      content: [
        {
          type: 'text',
          text: `✓ 问题已创建: #${response.data.number}\nURL: ${response.data.html_url}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `错误: ${error.message}\n建议: 请检查 GITHUB_TOKEN 环境变量是否设置`,
        },
      ],
      isError: true,
    };
  }
}
```

### 类型定义

```typescript
// src/types.ts
export interface ToolResponse {
  content: Array<{
    type: 'text' | 'image' | 'resource';
    text?: string;
    data?: string;
    mimeType?: string;
  }>;
  isError?: boolean;
}

export interface GitHubIssue {
  number: number;
  title: string;
  body: string;
  state: 'open' | 'closed';
  html_url: string;
  created_at: string;
  updated_at: string;
}
```

### 配置管理

```typescript
// src/config.ts
export interface Config {
  apiKey: string;
  baseUrl: string;
  timeout: number;
}

export function loadConfig(): Config {
  const apiKey = process.env.API_KEY;
  if (!apiKey) {
    throw new Error('API_KEY environment variable is required');
  }

  return {
    apiKey,
    baseUrl: process.env.BASE_URL || 'https://api.example.com',
    timeout: parseInt(process.env.TIMEOUT || '30000'),
  };
}
```

## Python 实现指南

### 项目结构

```
mcp-server/
├── pyproject.toml
├── src/
│   └── mcp_server_name/
│       ├── __init__.py
│       ├── server.py         # 服务器入口
│       ├── tools/            # 工具实现
│       │   ├── __init__.py
│       │   ├── tool1.py
│       │   └── tool2.py
│       ├── resources/        # 资源实现
│       │   └── __init__.py
│       └── types.py          # 类型定义
├── tests/
│   └── test_server.py
└── README.md
```

### 基础服务器实现

```python
# src/mcp_server_name/server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools.create_issue import create_issue_tool
from .tools.list_issues import list_issues_tool

app = Server("github-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_issue",
            description="创建 GitHub 问题",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "仓库名称，格式: owner/repo"
                    },
                    "title": {
                        "type": "string",
                        "description": "问题标题"
                    },
                    "body": {
                        "type": "string",
                        "description": "问题描述"
                    }
                },
                "required": ["repo", "title"]
            }
        ),
        Tool(
            name="list_issues",
            description="列出仓库问题",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "仓库名称"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "description": "问题状态"
                    }
                },
                "required": ["repo"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "create_issue":
        return await create_issue_tool(arguments)
    elif name == "list_issues":
        return await list_issues_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### 工具实现模式

```python
# src/mcp_server_name/tools/create_issue.py
import os
from github import Github
from mcp.types import TextContent

async def create_issue_tool(arguments: dict) -> list[TextContent]:
    repo_name = arguments.get("repo")
    title = arguments.get("title")
    body = arguments.get("body", "")

    # 验证输入
    if "/" not in repo_name:
        return [TextContent(
            type="text",
            text="错误: 仓库名称格式应为 owner/repo"
        )]

    try:
        # 调用 API
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

        g = Github(token)
        repo = g.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)

        # 返回结果
        return [TextContent(
            type="text",
            text=f"✓ 问题已创建: #{issue.number}\nURL: {issue.html_url}"
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"错误: {str(e)}\n建议: 请检查 GITHUB_TOKEN 环境变量是否设置"
        )]
```

### 类型定义

```python
# src/mcp_server_name/types.py
from typing import TypedDict, Literal

class GitHubIssue(TypedDict):
    number: int
    title: str
    body: str
    state: Literal["open", "closed"]
    html_url: str
    created_at: str
    updated_at: str

class ToolResponse(TypedDict):
    content: list[dict]
    isError: bool
```

## 资源实现

### TypeScript 资源

```typescript
import { ListResourcesRequestSchema, ReadResourceRequestSchema } from '@modelcontextprotocol/sdk/types.js';

// 注册资源列表
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: 'github://issues/recent',
      name: '最近的问题',
      description: '最近创建的问题列表',
      mimeType: 'application/json',
    },
  ],
}));

// 注册资源读取
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === 'github://issues/recent') {
    const issues = await fetchRecentIssues();
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(issues, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Python 资源

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="github://issues/recent",
            name="最近的问题",
            description="最近创建的问题列表",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "github://issues/recent":
        issues = await fetch_recent_issues()
        return json.dumps(issues, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```

## 认证和安全

### 环境变量

```typescript
// 读取环境变量
const apiKey = process.env.API_KEY;
if (!apiKey) {
  throw new Error('API_KEY environment variable is required');
}
```

### OAuth 流程

```typescript
import { OAuth2Client } from 'google-auth-library';

const oauth2Client = new OAuth2Client(
  process.env.CLIENT_ID,
  process.env.CLIENT_SECRET,
  process.env.REDIRECT_URI
);

// 获取授权 URL
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: ['https://www.googleapis.com/auth/drive'],
});

// 交换授权码
const { tokens } = await oauth2Client.getToken(code);
oauth2Client.setCredentials(tokens);
```

### API 密钥管理

```typescript
// 从配置文件读取
import { readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

function loadApiKey(): string {
  const configPath = join(homedir(), '.config', 'mcp-server', 'config.json');
  const config = JSON.parse(readFileSync(configPath, 'utf-8'));
  return config.apiKey;
}
```

## 测试策略

### 单元测试

```typescript
// tests/tools.test.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { createIssueTool } from '../src/tools/createIssue';

describe('createIssueTool', () => {
  beforeEach(() => {
    process.env.GITHUB_TOKEN = 'test-token';
  });

  it('should create issue successfully', async () => {
    const result = await createIssueTool({
      repo: 'owner/repo',
      title: 'Test Issue',
      body: 'Test body',
    });

    expect(result.content[0].text).toContain('问题已创建');
  });

  it('should handle invalid repo format', async () => {
    const result = await createIssueTool({
      repo: 'invalid',
      title: 'Test',
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain('格式应为');
  });
});
```

### 集成测试

```typescript
// tests/integration.test.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';

describe('MCP Server Integration', () => {
  let server: Server;

  beforeEach(() => {
    server = createServer();
  });

  it('should handle tool call', async () => {
    const response = await server.request({
      method: 'tools/call',
      params: {
        name: 'create_issue',
        arguments: {
          repo: 'owner/repo',
          title: 'Test',
        },
      },
    });

    expect(response.content).toBeDefined();
  });
});
```

### MCP Inspector

使用官方 MCP Inspector 测试服务器：

```bash
# 安装 Inspector
npm install -g @modelcontextprotocol/inspector

# 测试服务器
mcp-inspector node dist/index.js
```

## 性能优化

### 缓存策略

```typescript
import { LRUCache } from 'lru-cache';

const cache = new LRUCache<string, any>({
  max: 100,
  ttl: 1000 * 60 * 5, // 5 分钟
});

async function fetchWithCache(key: string, fetcher: () => Promise<any>) {
  const cached = cache.get(key);
  if (cached) return cached;

  const data = await fetcher();
  cache.set(key, data);
  return data;
}
```

### 批量操作

```typescript
// 批量获取问题
async function batchGetIssues(issueNumbers: number[]) {
  const promises = issueNumbers.map(num =>
    octokit.issues.get({ owner, repo, issue_number: num })
  );
  return await Promise.all(promises);
}
```

### 速率限制

```typescript
import pLimit from 'p-limit';

const limit = pLimit(5); // 最多 5 个并发请求

const results = await Promise.all(
  items.map(item => limit(() => processItem(item)))
);
```

## 错误处理

### 错误类型

```typescript
class MCPError extends Error {
  constructor(
    message: string,
    public code: string,
    public suggestion?: string
  ) {
    super(message);
    this.name = 'MCPError';
  }
}

class AuthenticationError extends MCPError {
  constructor(message: string) {
    super(message, 'AUTH_ERROR', '请检查 API 密钥是否有效');
  }
}

class RateLimitError extends MCPError {
  constructor(message: string) {
    super(message, 'RATE_LIMIT', '请稍后重试');
  }
}
```

### 错误响应

```typescript
try {
  const result = await apiCall();
  return {
    content: [{ type: 'text', text: JSON.stringify(result) }],
  };
} catch (error) {
  if (error instanceof AuthenticationError) {
    return {
      content: [
        {
          type: 'text',
          text: `认证错误: ${error.message}\n${error.suggestion}`,
        },
      ],
      isError: true,
    };
  }

  throw error; // 重新抛出未知错误
}
```

## 部署和分发

### 本地部署

```json
// .mcp.json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### HTTP 部署

```typescript
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import express from 'express';

const app = express();

app.post('/mcp', async (req, res) => {
  const transport = new SSEServerTransport('/mcp/messages', res);
  await server.connect(transport);
});

app.listen(3000, () => {
  console.log('MCP server listening on port 3000');
});
```

### Docker 部署

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

CMD ["node", "dist/index.js"]
```

## 最佳实践总结

1. **保持简单** - 每个工具做一件事
2. **完整文档** - 清晰的描述和输入模式
3. **错误处理** - 提供有用的错误信息
4. **性能优化** - 使用缓存和批量操作
5. **安全第一** - 妥善管理凭证
6. **充分测试** - 单元测试和集成测试
7. **版本控制** - 使用语义化版本
8. **监控日志** - 记录关键操作

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP SDK (TypeScript)](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP SDK (Python)](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
