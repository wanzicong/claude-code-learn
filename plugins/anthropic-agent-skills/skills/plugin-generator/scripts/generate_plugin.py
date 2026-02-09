#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 插件生成器主脚本
支持生成技能、MCP 服务器和混合插件
"""

import os
import sys
import io
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class PluginGenerator:
    """插件生成器核心类"""

    def __init__(self, plugin_type: str, name: str, output_dir: str, **kwargs):
        self.plugin_type = plugin_type
        self.name = name
        self.output_dir = Path(output_dir)
        self.description = kwargs.get('description', '')
        self.language = kwargs.get('language', 'typescript')
        self.author = kwargs.get('author', 'Claude Code User')
        self.license = kwargs.get('license', 'MIT')

        # 获取模板目录
        script_dir = Path(__file__).parent
        self.templates_dir = script_dir.parent / 'assets' / 'templates'

    def generate(self):
        """生成插件"""
        print(f"正在生成 {self.plugin_type} 插件: {self.name}")

        if self.plugin_type == 'skill':
            self._generate_skill()
        elif self.plugin_type == 'mcp':
            self._generate_mcp()
        elif self.plugin_type == 'hybrid':
            self._generate_hybrid()
        else:
            raise ValueError(f"不支持的插件类型: {self.plugin_type}")

        print(f"✓ 插件生成完成: {self.output_dir / self.name}")

    def _generate_skill(self):
        """生成技能插件"""
        skill_dir = self.output_dir / self.name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 创建目录结构
        (skill_dir / 'scripts').mkdir(exist_ok=True)
        (skill_dir / 'references').mkdir(exist_ok=True)
        (skill_dir / 'assets').mkdir(exist_ok=True)

        # 生成 SKILL.md
        self._create_skill_md(skill_dir)

        # 生成 LICENSE
        self._create_license(skill_dir)

        # 生成示例脚本
        self._create_example_script(skill_dir / 'scripts')

        # 生成参考文档
        self._create_reference_docs(skill_dir / 'references')

        print(f"  ✓ 技能结构已创建")

    def _generate_mcp(self):
        """生成 MCP 服务器插件"""
        mcp_dir = self.output_dir / self.name
        mcp_dir.mkdir(parents=True, exist_ok=True)

        if self.language == 'typescript':
            self._generate_typescript_mcp(mcp_dir)
        elif self.language == 'python':
            self._generate_python_mcp(mcp_dir)
        else:
            raise ValueError(f"不支持的语言: {self.language}")

    def _generate_typescript_mcp(self, mcp_dir: Path):
        """生成 TypeScript MCP 服务器"""
        # 创建目录结构
        (mcp_dir / '.claude-plugin').mkdir(exist_ok=True)
        (mcp_dir / 'src' / 'tools').mkdir(parents=True, exist_ok=True)
        (mcp_dir / 'src' / 'resources').mkdir(exist_ok=True)
        (mcp_dir / 'tests').mkdir(exist_ok=True)

        # 生成配置文件
        self._create_plugin_json(mcp_dir / '.claude-plugin')
        self._create_mcp_json(mcp_dir / '.claude-plugin')
        self._create_package_json(mcp_dir)
        self._create_tsconfig(mcp_dir)

        # 生成源代码
        self._create_typescript_index(mcp_dir / 'src')
        self._create_typescript_tool(mcp_dir / 'src' / 'tools')
        self._create_typescript_types(mcp_dir / 'src')

        # 生成测试
        self._create_typescript_tests(mcp_dir / 'tests')

        # 生成文档
        self._create_readme(mcp_dir, 'typescript')
        self._create_license(mcp_dir)

        print(f"  ✓ TypeScript MCP 服务器已创建")

    def _generate_python_mcp(self, mcp_dir: Path):
        """生成 Python MCP 服务器"""
        # 创建目录结构
        (mcp_dir / '.claude-plugin').mkdir(exist_ok=True)
        src_dir = mcp_dir / 'src' / self.name.replace('-', '_')
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / 'tools').mkdir(exist_ok=True)
        (src_dir / 'resources').mkdir(exist_ok=True)
        (mcp_dir / 'tests').mkdir(exist_ok=True)

        # 生成配置文件
        self._create_plugin_json(mcp_dir / '.claude-plugin')
        self._create_mcp_json(mcp_dir / '.claude-plugin')
        self._create_pyproject_toml(mcp_dir)

        # 生成源代码
        self._create_python_server(src_dir)
        self._create_python_tool(src_dir / 'tools')
        self._create_python_init(src_dir)

        # 生成测试
        self._create_python_tests(mcp_dir / 'tests')

        # 生成文档
        self._create_readme(mcp_dir, 'python')
        self._create_license(mcp_dir)

        print(f"  ✓ Python MCP 服务器已创建")

    def _generate_hybrid(self):
        """生成混合插件（技能 + MCP）"""
        hybrid_dir = self.output_dir / self.name
        hybrid_dir.mkdir(parents=True, exist_ok=True)

        # 生成技能部分
        skill_dir = hybrid_dir / 'skills'
        skill_dir.mkdir(exist_ok=True)
        self.output_dir = skill_dir
        self._generate_skill()

        # 生成 MCP 部分
        mcp_dir = hybrid_dir / 'mcp'
        mcp_dir.mkdir(exist_ok=True)
        self.output_dir = mcp_dir
        self._generate_mcp()

        # 生成混合插件配置
        (hybrid_dir / '.claude-plugin').mkdir(exist_ok=True)
        self._create_hybrid_plugin_json(hybrid_dir / '.claude-plugin')

        print(f"  ✓ 混合插件已创建")

    def _create_skill_md(self, skill_dir: Path):
        """创建 SKILL.md"""
        content = f"""---
name: {self.name}
description: {self.description or f'{self.name} 技能 - 提供专业的工作流程和工具支持'}
license: {self.license}
---

# {self.name.replace('-', ' ').title()}

## 概述

{self.description or '这是一个专业的 Claude Code 技能，提供特定领域的工作流程指导和工具支持。'}

## 功能特性

- 功能 1: 描述主要功能
- 功能 2: 描述次要功能
- 功能 3: 描述辅助功能

## 使用方法

### 快速开始

```bash
# 示例命令
python scripts/main.py --input example.txt --output result.txt
```

### 高级用法

详见 [references/workflows.md](references/workflows.md)

## 脚本说明

- **main.py** - 主要功能脚本
- **utils.py** - 工具函数库

## 参考文档

- [workflows.md](references/workflows.md) - 详细工作流程
- [api_docs.md](references/api_docs.md) - API 文档
- [examples.md](references/examples.md) - 使用示例

## 许可证

{self.license} License - 详见 LICENSE.txt

## 作者

{self.author}

## 更新日志

- **v1.0.0** ({datetime.now().strftime('%Y-%m-%d')}) - 初始版本
"""
        (skill_dir / 'SKILL.md').write_text(content, encoding='utf-8')

    def _create_example_script(self, scripts_dir: Path):
        """创建示例脚本"""
        main_py = """#!/usr/bin/env python3
\"\"\"
主要功能脚本
\"\"\"

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='主要功能')
    parser.add_argument('--input', required=True, help='输入文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()

    # 实现主要功能
    print(f"处理输入: {args.input}")
    print(f"生成输出: {args.output}")

    # TODO: 添加实际功能实现

    print("完成!")

if __name__ == '__main__':
    main()
"""
        (scripts_dir / 'main.py').write_text(main_py, encoding='utf-8')

        utils_py = """#!/usr/bin/env python3
\"\"\"
工具函数库
\"\"\"

def helper_function(data):
    \"\"\"辅助函数示例\"\"\"
    return data

def validate_input(input_path):
    \"\"\"验证输入\"\"\"
    from pathlib import Path
    return Path(input_path).exists()
"""
        (scripts_dir / 'utils.py').write_text(utils_py, encoding='utf-8')

        requirements = """# Python 依赖
# 根据需要添加依赖包
"""
        (scripts_dir / 'requirements.txt').write_text(requirements, encoding='utf-8')

    def _create_reference_docs(self, references_dir: Path):
        """创建参考文档"""
        workflows = f"""# {self.name} 工作流程

## 基本工作流

1. 准备输入数据
2. 执行处理
3. 验证输出
4. 完成

## 高级工作流

详细描述复杂场景的处理流程。
"""
        (references_dir / 'workflows.md').write_text(workflows, encoding='utf-8')

        api_docs = """# API 文档

## 函数列表

### main()
主要功能函数

### helper_function(data)
辅助函数
"""
        (references_dir / 'api_docs.md').write_text(api_docs, encoding='utf-8')

    def _create_plugin_json(self, plugin_dir: Path):
        """创建 plugin.json"""
        plugin_json = {
            "name": self.name,
            "version": "1.0.0",
            "description": self.description or f"{self.name} plugin",
            "author": {"name": self.author},
            "license": self.license
        }
        (plugin_dir / 'plugin.json').write_text(
            json.dumps(plugin_json, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _create_mcp_json(self, plugin_dir: Path):
        """创建 .mcp.json"""
        mcp_json = {
            "mcpServers": {
                self.name: {
                    "type": "stdio",
                    "command": "node" if self.language == 'typescript' else "python",
                    "args": ["dist/index.js"] if self.language == 'typescript' else ["-m", self.name.replace('-', '_')]
                }
            }
        }
        (plugin_dir / '.mcp.json').write_text(
            json.dumps(mcp_json, indent=2),
            encoding='utf-8'
        )

    def _create_package_json(self, mcp_dir: Path):
        """创建 package.json"""
        package_json = {
            "name": self.name,
            "version": "1.0.0",
            "description": self.description or f"{self.name} MCP server",
            "main": "dist/index.js",
            "type": "module",
            "scripts": {
                "build": "tsc",
                "test": "jest",
                "dev": "tsx src/index.ts"
            },
            "dependencies": {
                "@modelcontextprotocol/sdk": "^1.0.0"
            },
            "devDependencies": {
                "@types/node": "^20.0.0",
                "typescript": "^5.0.0",
                "tsx": "^4.0.0",
                "jest": "^29.0.0",
                "@types/jest": "^29.0.0"
            }
        }
        (mcp_dir / 'package.json').write_text(
            json.dumps(package_json, indent=2),
            encoding='utf-8'
        )

    def _create_tsconfig(self, mcp_dir: Path):
        """创建 tsconfig.json"""
        tsconfig = {
            "compilerOptions": {
                "target": "ES2022",
                "module": "Node16",
                "moduleResolution": "Node16",
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist", "tests"]
        }
        # 转换 Python 布尔值为 JSON 布尔值
        tsconfig_str = json.dumps(tsconfig, indent=2).replace('True', 'true').replace('False', 'false')
        (mcp_dir / 'tsconfig.json').write_text(
            tsconfig_str,
            encoding='utf-8'
        )

    def _create_typescript_index(self, src_dir: Path):
        """创建 TypeScript 入口文件"""
        index_ts = f"""import {{ Server }} from '@modelcontextprotocol/sdk/server/index.js';
import {{ StdioServerTransport }} from '@modelcontextprotocol/sdk/server/stdio.js';
import {{
  CallToolRequestSchema,
  ListToolsRequestSchema,
}} from '@modelcontextprotocol/sdk/types.js';
import {{ exampleTool }} from './tools/exampleTool.js';

const server = new Server(
  {{
    name: '{self.name}',
    version: '1.0.0',
  }},
  {{
    capabilities: {{
      tools: {{}},
    }},
  }}
);

// 注册工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => ({{
  tools: [
    {{
      name: 'example_tool',
      description: '示例工具',
      inputSchema: {{
        type: 'object',
        properties: {{
          input: {{
            type: 'string',
            description: '输入参数',
          }},
        }},
        required: ['input'],
      }},
    }},
  ],
}}));

// 注册工具调用处理
server.setRequestHandler(CallToolRequestSchema, async (request) => {{
  const {{ name, arguments: args }} = request.params;

  switch (name) {{
    case 'example_tool':
      return await exampleTool(args);
    default:
      throw new Error(`Unknown tool: ${{name}}`);
  }}
}});

// 启动服务器
async function main() {{
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('{self.name} MCP server running on stdio');
}}

main().catch((error) => {{
  console.error('Server error:', error);
  process.exit(1);
}});
"""
        (src_dir / 'index.ts').write_text(index_ts, encoding='utf-8')

    def _create_typescript_tool(self, tools_dir: Path):
        """创建 TypeScript 工具实现"""
        tool_ts = """export async function exampleTool(args: any) {
  const { input } = args;

  // 实现工具逻辑
  const result = `处理结果: ${input}`;

  return {
    content: [
      {
        type: 'text',
        text: result,
      },
    ],
  };
}
"""
        (tools_dir / 'exampleTool.ts').write_text(tool_ts, encoding='utf-8')

    def _create_typescript_types(self, src_dir: Path):
        """创建 TypeScript 类型定义"""
        types_ts = """export interface ExampleInput {
  input: string;
}

export interface ExampleOutput {
  result: string;
}
"""
        (src_dir / 'types.ts').write_text(types_ts, encoding='utf-8')

    def _create_typescript_tests(self, tests_dir: Path):
        """创建 TypeScript 测试"""
        test_ts = """import { exampleTool } from '../src/tools/exampleTool';

describe('exampleTool', () => {
  it('should process input correctly', async () => {
    const result = await exampleTool({ input: 'test' });
    expect(result.content[0].text).toContain('test');
  });
});
"""
        (tests_dir / 'tools.test.ts').write_text(test_ts, encoding='utf-8')

    def _create_pyproject_toml(self, mcp_dir: Path):
        """创建 pyproject.toml"""
        content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{self.name}"
version = "1.0.0"
description = "{self.description or f'{self.name} MCP server'}"
authors = [
    {{name = "{self.author}"}}
]
license = {{text = "{self.license}"}}
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]

[tool.setuptools.packages.find]
where = ["src"]
"""
        (mcp_dir / 'pyproject.toml').write_text(content, encoding='utf-8')

    def _create_python_server(self, src_dir: Path):
        """创建 Python 服务器实现"""
        server_py = f"""import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools.example_tool import example_tool

app = Server("{self.name}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="example_tool",
            description="示例工具",
            inputSchema={{
                "type": "object",
                "properties": {{
                    "input": {{
                        "type": "string",
                        "description": "输入参数"
                    }}
                }},
                "required": ["input"]
            }}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "example_tool":
        return await example_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {{name}}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
"""
        (src_dir / 'server.py').write_text(server_py, encoding='utf-8')

    def _create_python_tool(self, tools_dir: Path):
        """创建 Python 工具实现"""
        tool_py = """from mcp.types import TextContent

async def example_tool(arguments: dict) -> list[TextContent]:
    input_data = arguments.get("input", "")

    # 实现工具逻辑
    result = f"处理结果: {input_data}"

    return [TextContent(type="text", text=result)]
"""
        (tools_dir / 'example_tool.py').write_text(tool_py, encoding='utf-8')
        (tools_dir / '__init__.py').write_text('', encoding='utf-8')

    def _create_python_init(self, src_dir: Path):
        """创建 Python __init__.py"""
        (src_dir / '__init__.py').write_text('', encoding='utf-8')

    def _create_python_tests(self, tests_dir: Path):
        """创建 Python 测试"""
        test_py = """import pytest
from src.tools.example_tool import example_tool

@pytest.mark.asyncio
async def test_example_tool():
    result = await example_tool({"input": "test"})
    assert len(result) > 0
    assert "test" in result[0].text
"""
        (tests_dir / 'test_server.py').write_text(test_py, encoding='utf-8')
        (tests_dir / '__init__.py').write_text('', encoding='utf-8')

    def _create_readme(self, mcp_dir: Path, language: str):
        """创建 README"""
        install_cmd = "npm install" if language == 'typescript' else "pip install -e ."
        build_cmd = "npm run build" if language == 'typescript' else "python -m build"
        test_cmd = "npm test" if language == 'typescript' else "pytest"

        readme = f"""# {self.name}

{self.description or f'{self.name} MCP 服务器'}

## 安装

```bash
{install_cmd}
```

## 构建

```bash
{build_cmd}
```

## 测试

```bash
{test_cmd}
```

## 使用

将以下配置添加到 Claude Code 的 MCP 配置文件：

```json
{{
  "mcpServers": {{
    "{self.name}": {{
      "type": "stdio",
      "command": "{'node' if language == 'typescript' else 'python'}",
      "args": [{"dist/index.js" if language == 'typescript' else f'-m {self.name.replace("-", "_")}'}]
    }}
  }}
}}
```

## 工具列表

- **example_tool** - 示例工具

## 许可证

{self.license}

## 作者

{self.author}
"""
        (mcp_dir / 'README.md').write_text(readme, encoding='utf-8')

    def _create_license(self, dir_path: Path):
        """创建 LICENSE 文件"""
        if self.license == 'MIT':
            license_text = f"""MIT License

Copyright (c) {datetime.now().year} {self.author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        else:
            license_text = f"{self.license} License\n\nCopyright (c) {datetime.now().year} {self.author}\n"

        (dir_path / 'LICENSE.txt').write_text(license_text, encoding='utf-8')

    def _create_hybrid_plugin_json(self, plugin_dir: Path):
        """创建混合插件配置"""
        plugin_json = {
            "name": self.name,
            "version": "1.0.0",
            "description": self.description or f"{self.name} hybrid plugin",
            "author": {"name": self.author},
            "license": self.license,
            "skills": ["./skills"],
            "mcpServers": {
                self.name: {
                    "type": "stdio",
                    "command": "node" if self.language == 'typescript' else "python",
                    "args": ["mcp/dist/index.js"] if self.language == 'typescript' else ["-m", f"mcp.{self.name.replace('-', '_')}"]
                }
            }
        }
        (plugin_dir / 'plugin.json').write_text(
            json.dumps(plugin_json, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

def main():
    parser = argparse.ArgumentParser(description='Claude Code 插件生成器')
    parser.add_argument('--type', required=True, choices=['skill', 'mcp', 'hybrid'],
                       help='插件类型')
    parser.add_argument('--name', required=True, help='插件名称')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--description', help='插件描述')
    parser.add_argument('--language', default='typescript', choices=['typescript', 'python'],
                       help='MCP 服务器语言 (默认: typescript)')
    parser.add_argument('--author', default='Claude Code User', help='作者名称')
    parser.add_argument('--license', default='MIT', help='许可证 (默认: MIT)')

    args = parser.parse_args()

    try:
        generator = PluginGenerator(
            plugin_type=args.type,
            name=args.name,
            output_dir=args.output,
            description=args.description,
            language=args.language,
            author=args.author,
            license=args.license
        )
        generator.generate()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
