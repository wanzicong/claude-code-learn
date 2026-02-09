# 插件示例集合

本文档提供各种类型插件的完整示例，帮助你快速上手。

## 目录

1. [简单技能示例](#简单技能示例)
2. [复杂技能示例](#复杂技能示例)
3. [TypeScript MCP 服务器示例](#typescript-mcp-服务器示例)
4. [Python MCP 服务器示例](#python-mcp-服务器示例)
5. [混合插件示例](#混合插件示例)

---

## 简单技能示例

### 示例：文本转换技能

一个简单的文本转换技能，提供大小写转换、反转等功能。

#### 目录结构

```
text-transform/
├── SKILL.md
├── LICENSE.txt
└── scripts/
    ├── transform.py
    └── requirements.txt
```

#### SKILL.md

```markdown
---
name: text-transform
description: 文本转换工具 - 提供大小写转换、反转、编码等文本处理功能。当用户需要转换文本格式、改变大小写、反转字符串或进行编码转换时使用此技能。
license: MIT
---

# 文本转换工具

## 概述

提供常用的文本转换功能，包括大小写转换、字符串反转、Base64 编码等。

## 快速开始

```bash
# 转换为大写
python scripts/transform.py --input "hello world" --mode upper

# 反转字符串
python scripts/transform.py --input "hello" --mode reverse

# Base64 编码
python scripts/transform.py --input "hello" --mode base64
```

## 支持的转换模式

- `upper` - 转换为大写
- `lower` - 转换为小写
- `title` - 转换为标题格式
- `reverse` - 反转字符串
- `base64` - Base64 编码
- `base64_decode` - Base64 解码

## 许可证

MIT License
```

#### scripts/transform.py

```python
#!/usr/bin/env python3
"""文本转换脚本"""

import argparse
import base64
import sys

def transform_text(text: str, mode: str) -> str:
    """转换文本"""
    if mode == 'upper':
        return text.upper()
    elif mode == 'lower':
        return text.lower()
    elif mode == 'title':
        return text.title()
    elif mode == 'reverse':
        return text[::-1]
    elif mode == 'base64':
        return base64.b64encode(text.encode()).decode()
    elif mode == 'base64_decode':
        return base64.b64decode(text.encode()).decode()
    else:
        raise ValueError(f"不支持的模式: {mode}")

def main():
    parser = argparse.ArgumentParser(description='文本转换工具')
    parser.add_argument('--input', required=True, help='输入文本')
    parser.add_argument('--mode', required=True,
                       choices=['upper', 'lower', 'title', 'reverse', 'base64', 'base64_decode'],
                       help='转换模式')
    args = parser.parse_args()

    try:
        result = transform_text(args.input, args.mode)
        print(result)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## 复杂技能示例

### 示例：数据分析技能

一个包含多个脚本、参考文档和资源的复杂技能。

#### 目录结构

```
data-analysis/
├── SKILL.md
├── LICENSE.txt
├── scripts/
│   ├── analyze.py
│   ├── visualize.py
│   ├── export.py
│   └── requirements.txt
├── references/
│   ├── workflows.md
│   ├── api_docs.md
│   └── examples.md
└── assets/
    └── templates/
        ├── report_template.html
        └── chart_config.json
```

#### SKILL.md

```markdown
---
name: data-analysis
description: 数据分析技能 - 提供数据加载、清洗、分析、可视化和报告生成功能。支持 CSV、Excel、JSON 等格式。当用户需要分析数据、生成图表、创建报告或进行统计分析时使用此技能。
license: MIT
---

# 数据分析技能

## 概述

全面的数据分析工具集，支持数据处理、统计分析和可视化。

## 快速开始

```bash
# 分析 CSV 文件
python scripts/analyze.py --input data.csv --output analysis.json

# 生成可视化
python scripts/visualize.py --input analysis.json --output charts/

# 导出报告
python scripts/export.py --input analysis.json --template assets/templates/report_template.html --output report.html
```

## 工作流程

详见 [workflows.md](references/workflows.md)

## API 文档

详见 [api_docs.md](references/api_docs.md)

## 示例

详见 [examples.md](references/examples.md)
```

#### scripts/analyze.py

```python
#!/usr/bin/env python3
"""数据分析脚本"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path

def analyze_data(input_file: str) -> dict:
    """分析数据文件"""
    # 读取数据
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    elif input_file.endswith('.json'):
        df = pd.read_json(input_file)
    else:
        raise ValueError("不支持的文件格式")

    # 基础统计
    analysis = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing': df.isnull().sum().to_dict(),
        'statistics': {}
    }

    # 数值列统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        analysis['statistics'][col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max())
        }

    return analysis

def main():
    parser = argparse.ArgumentParser(description='数据分析工具')
    parser.add_argument('--input', required=True, help='输入文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()

    try:
        analysis = analyze_data(args.input)

        # 保存结果
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(f"✓ 分析完成: {args.output}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## TypeScript MCP 服务器示例

### 示例：待办事项 MCP 服务器

一个简单的待办事项管理 MCP 服务器。

#### 目录结构

```
todo-mcp/
├── .claude-plugin/
│   ├── plugin.json
│   └── .mcp.json
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── tools/
│   │   ├── createTodo.ts
│   │   ├── listTodos.ts
│   │   └── completeTodo.ts
│   ├── storage.ts
│   └── types.ts
├── tests/
│   └── tools.test.ts
└── README.md
```

#### .claude-plugin/plugin.json

```json
{
  "name": "todo-mcp",
  "version": "1.0.0",
  "description": "待办事项管理 MCP 服务器",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT"
}
```

#### .claude-plugin/.mcp.json

```json
{
  "mcpServers": {
    "todo": {
      "type": "stdio",
      "command": "node",
      "args": ["dist/index.js"]
    }
  }
}
```

#### src/index.ts

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { createTodoTool } from './tools/createTodo.js';
import { listTodosTool } from './tools/listTodos.js';
import { completeTodoTool } from './tools/completeTodo.js';

const server = new Server(
  {
    name: 'todo-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'create_todo',
      description: '创建新的待办事项',
      inputSchema: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: '待办事项标题',
          },
          description: {
            type: 'string',
            description: '详细描述',
          },
          priority: {
            type: 'string',
            enum: ['low', 'medium', 'high'],
            description: '优先级',
          },
        },
        required: ['title'],
      },
    },
    {
      name: 'list_todos',
      description: '列出所有待办事项',
      inputSchema: {
        type: 'object',
        properties: {
          status: {
            type: 'string',
            enum: ['all', 'pending', 'completed'],
            description: '筛选状态',
          },
        },
      },
    },
    {
      name: 'complete_todo',
      description: '标记待办事项为完成',
      inputSchema: {
        type: 'object',
        properties: {
          id: {
            type: 'number',
            description: '待办事项 ID',
          },
        },
        required: ['id'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'create_todo':
      return await createTodoTool(args);
    case 'list_todos':
      return await listTodosTool(args);
    case 'complete_todo':
      return await completeTodoTool(args);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Todo MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
```

#### src/tools/createTodo.ts

```typescript
import { storage } from '../storage.js';
import { Todo } from '../types.js';

export async function createTodoTool(args: any) {
  const { title, description = '', priority = 'medium' } = args;

  const todo: Todo = {
    id: Date.now(),
    title,
    description,
    priority,
    completed: false,
    createdAt: new Date().toISOString(),
  };

  storage.addTodo(todo);

  return {
    content: [
      {
        type: 'text',
        text: `✓ 待办事项已创建\nID: ${todo.id}\n标题: ${todo.title}\n优先级: ${todo.priority}`,
      },
    ],
  };
}
```

#### src/storage.ts

```typescript
import { Todo } from './types.js';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

class TodoStorage {
  private todos: Todo[] = [];
  private filePath: string;

  constructor() {
    this.filePath = join(homedir(), '.todo-mcp', 'todos.json');
    this.load();
  }

  private load() {
    if (existsSync(this.filePath)) {
      const data = readFileSync(this.filePath, 'utf-8');
      this.todos = JSON.parse(data);
    }
  }

  private save() {
    writeFileSync(this.filePath, JSON.stringify(this.todos, null, 2));
  }

  addTodo(todo: Todo) {
    this.todos.push(todo);
    this.save();
  }

  getTodos(status?: 'all' | 'pending' | 'completed'): Todo[] {
    if (status === 'pending') {
      return this.todos.filter(t => !t.completed);
    } else if (status === 'completed') {
      return this.todos.filter(t => t.completed);
    }
    return this.todos;
  }

  completeTodo(id: number): boolean {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = true;
      this.save();
      return true;
    }
    return false;
  }
}

export const storage = new TodoStorage();
```

---

## Python MCP 服务器示例

### 示例：天气查询 MCP 服务器

使用 Python 实现的天气查询服务。

#### 目录结构

```
weather-mcp/
├── .claude-plugin/
│   ├── plugin.json
│   └── .mcp.json
├── pyproject.toml
├── src/
│   └── weather_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── get_weather.py
│       │   └── get_forecast.py
│       └── api_client.py
└── tests/
    └── test_server.py
```

#### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "weather-mcp"
version = "1.0.0"
description = "天气查询 MCP 服务器"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]
```

#### src/weather_mcp/server.py

```python
import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools.get_weather import get_weather_tool
from .tools.get_forecast import get_forecast_tool

app = Server("weather-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="获取指定城市的当前天气",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "description": "温度单位（metric=摄氏度，imperial=华氏度）"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_forecast",
            description="获取指定城市的天气预报",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "days": {
                        "type": "number",
                        "description": "预报天数（1-7）"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        return await get_weather_tool(arguments)
    elif name == "get_forecast":
        return await get_forecast_tool(arguments)
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

#### src/weather_mcp/tools/get_weather.py

```python
from mcp.types import TextContent
from ..api_client import WeatherAPIClient

async def get_weather_tool(arguments: dict) -> list[TextContent]:
    city = arguments.get("city")
    units = arguments.get("units", "metric")

    try:
        client = WeatherAPIClient()
        weather = await client.get_current_weather(city, units)

        temp_unit = "°C" if units == "metric" else "°F"
        result = f"""
🌤️ {city} 当前天气

温度: {weather['temp']}{temp_unit}
体感温度: {weather['feels_like']}{temp_unit}
天气: {weather['description']}
湿度: {weather['humidity']}%
风速: {weather['wind_speed']} m/s
"""

        return [TextContent(type="text", text=result.strip())]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"错误: {str(e)}\n建议: 请检查城市名称是否正确"
        )]
```

---

## 混合插件示例

### 示例：笔记管理混合插件

结合技能和 MCP 服务器的完整笔记管理系统。

#### 目录结构

```
notes-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── notes-skill/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── format_notes.py
│       └── references/
│           └── workflows.md
└── mcp/
    ├── .mcp.json
    ├── package.json
    └── src/
        └── index.ts
```

#### .claude-plugin/plugin.json

```json
{
  "name": "notes-plugin",
  "version": "1.0.0",
  "description": "完整的笔记管理系统，包含格式化技能和 API 集成",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "skills": ["./skills/notes-skill"],
  "mcpServers": {
    "notes": {
      "type": "stdio",
      "command": "node",
      "args": ["mcp/dist/index.js"]
    }
  }
}
```

---

## 使用生成器创建示例

使用插件生成器快速创建这些示例：

```bash
# 生成简单技能
python scripts/generate_plugin.py \
  --type skill \
  --name text-transform \
  --description "文本转换工具" \
  --output ./examples

# 生成 MCP 服务器
python scripts/generate_plugin.py \
  --type mcp \
  --name todo-mcp \
  --description "待办事项管理" \
  --language typescript \
  --output ./examples

# 生成混合插件
python scripts/generate_plugin.py \
  --type hybrid \
  --name notes-plugin \
  --description "笔记管理系统" \
  --output ./examples
```

## 总结

这些示例展示了：

1. **简单技能** - 单一功能，最小化结构
2. **复杂技能** - 多脚本、参考文档、资源文件
3. **TypeScript MCP** - 现代 JavaScript 实现
4. **Python MCP** - Python 异步实现
5. **混合插件** - 技能 + MCP 组合

选择适合你需求的模式，使用生成器快速开始！
