# 在命令和代理中使用 MCP 工具

在 Claude Code 插件命令和代理中有效使用 MCP 工具的完整指南。

## 概述

配置 MCP 服务器后，其工具将以 `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` 前缀形式可用。像使用内置 Claude Code 工具一样在命令和代理中使用这些工具。

## 工具命名约定

### 格式

```
mcp__plugin_<plugin-name>_<server-name>__<tool-name>
```

### 示例

**使用 Asana 插件中的 asana 服务器：**
- `mcp__plugin_asana_asana__asana_create_task`
- `mcp__plugin_asana_asana__asana_search_tasks`
- `mcp__plugin_asana_asana__asana_get_project`

**使用数据库服务器的自定义插件：**
- `mcp__plugin_myplug_database__query`
- `mcp__plugin_myplug_database__execute`
- `mcp__plugin_myplug_database__list_tables`

### 发现工具名称

**使用 `/mcp` 命令：**
```bash
/mcp
```

这会显示：
- 所有可用的 MCP 服务器
- 每个服务器提供的工具
- 工具模式和描述
- 在配置中使用的完整工具名称

## 在命令中使用工具

### 预先允许工具

在命令 frontmatter 中指定 MCP 工具：

```markdown
---
description: 创建新的 Asana 任务
allowed-tools: [
  "mcp__plugin_asana_asana__asana_create_task"
]
---
```

# 创建任务命令

要创建任务：
1. 从用户收集任务详细信息
2. 使用 mcp__plugin_asana_asana__asana_create_task 及详细信息
3. 向用户确认创建

### 多个工具

```markdown
---
description: 搜索和创建 Asana 任务
allowed-tools: [
  "mcp__plugin_asana_asana__asana_search_tasks",
  "mcp__plugin_asana_asana__asana_create_task"
]
---
```

### 通配符（谨慎使用）

```markdown
---
allowed-tools: ["mcp__plugin_asana_asana__*"]
---
```

**警告：** 仅当命令真正需要访问服务器所有工具时才使用通配符。

## 搜索任务

要搜索任务：
1. 使用 mcp__plugin_asana_asana__asana_search_tasks
2. 提供搜索过滤器（受理人、项目等）
3. 向用户显示结果

## 创建任务

要创建任务：
1. 收集任务详细信息：
   - 标题（必需）
   - 描述
   - 项目
   - 受理人
   - 截止日期
2. 使用 mcp__plugin_asana_asana__asana_create_task 及详细信息
3. 向用户显示确认并附带任务链接

## 在代理中使用工具

### 代理配置

代理可以在不需要预先允许的情况下自主使用 MCP 工具：

```markdown
---
name: asana-status-updater
description: 当用户请求"更新 Asana 状态"、"生成项目报告"或"同步 Asana 任务"时使用此代理
model: inherit
color: blue
---

自主代理用于生成 Asana 项目状态报告。

## 流程

1. **查询任务**：使用 mcp__plugin_asana_asana__asana_search_tasks 获取所有任务
2. **分析进度**：计算完成率并识别阻塞因素
3. **生成报告**：创建格式化的状态更新
4. **更新 Asana**：使用 mcp__plugin_asana_asana__asana_create_comment 发布报告

## 可用工具

该代理可以无限制地访问所有 Asana MCP 工具。

### 代理工具访问

代理比命令有更广泛的工具访问：
- 可以确定 Claude 认为必要的任何工具
- 不需要预先允许列表
- 应该记录它们通常使用的工具

## 工具调用模式

### 模式 1：简单工具调用

单个工具调用及验证：

```markdown
步骤：
1. 验证用户提供的必需字段
2. 使用 mcp__plugin_api_server__create_item 使用经过验证的数据调用
3. 检查错误
4. 显示确认
```

### 模式 2：顺序工具

链多个工具调用：

```markdown
步骤：
1. 搜索现有项：mcp__plugin_api_server__search
2. 如果未找到，创建新的：mcp__plugin_api_server__create
3. 添加元数据：mcp__plugin_api_server__update_metadata
4. 返回最终的项 ID
```

### 模式 3：批量操作

使用同一工具的多个调用：

```markdown
步骤：
1. 获取要处理的项列表
2. 对于每个项：
   - 调用 mcp__plugin_api_server__update_item 调用
   - 追踪成功/失败
3. 报告结果摘要：
   - "成功处理 10 个项中的 8 个"
   - "因 [原因] 失败的项：[item1, item2]"
   - 建议重试或手动干预
```

### 模式 4：错误处理

优雅的错误处理：

```markdown
步骤：
1. 尝试调用 mcp__plugin_api_server__get_data
2. 如果错误（速率限制、网络等）：
   - 等待并重试（最多 3 次）
   - 如果仍然失败，通知用户
   - 建议检查配置
3. 成功时，处理数据
```

## 工具参数

### 理解工具模式

每个 MCP 工具都有一个定义其参数的模式。使用 `/mcp` 查看。

**示例模式：**
```json
{
  "name": "asana_create_task",
  "description": "创建新的 Asana 任务",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "任务标题"
      },
      "notes": {
        "type": "string",
        "description": "任务描述"
      },
      "workspace": {
        "type": "string",
        "description": "工作区 GID"
      }
    },
    "required": ["name", "workspace"]
  }
  }
}
```

### 调用参数调用工具

Claude 根据模式自动构建工具调用：

```typescript
// Claude 内部生成此代码
{
  toolName: "mcp__plugin_asana_asana__asana_create_task",
  input: {
    name: "审查 PR #123",
    notes: "新功能的代码审查",
    workspace: "12345",
    assignee: "67890",
    due_on: "2025-01-15"
  }
}
```

### 参数验证

**在命令中验证参数：**

```markdown
步骤：
1. 检查必需参数：
   - 标题不为空
   - 提供供了工作区 ID
   - 截止日期有效格式 (YYYY-MM-DD)
2. 如果验证失败，要求用户提供缺失数据
3. 如果验证通过，调用 MCP 工具
4. 优雅地处理工具错误
```

## 响应处理

### 成功响应

```markdown
步骤：
1. 调用 MCP 工具
2. 成功时：
   - 从响应中提取相关数据
   - 为用户显示格式化
   - 提供确认消息
   - 包含相关链接或 ID
```

### 错误响应

```markdown
步骤：
1. 调用 MCP 工具
2. 出错时：
   - 检查错误类型（认证、速率限制、验证等）
   - 提供有用的错误消息
   - 建议补救步骤
   - 不向用户暴露内部错误详情
```

### 部分成功

```markdown
步骤：
1. 批量操作包含多个 MCP 调用
2. 分别跟踪成功和失败
3. 报告摘要：
   - "成功处理 10 个项中的 8 个"
   - "因 [原因] 失败的项：[item1, item2]"
   - 建议重试或手动干预
```

## 性能优化

### 批处理请求

**好的：** 单个查询加过滤器

```markdown
步骤：
1. 使用过滤器调用 mcp__plugin_asana_asana__asana_search_tasks：
   - project_id: "123"
   - status: "active"
   - limit: 100
2. 处理所有结果
```

**避免：** 多个单独查询

```markdown
步骤：
1. 对于每个项 ID：
   - 调用 mcp__plugin_api_server__get_item
   - 处理项
```

### 缓存结果

```markdown
步骤：
1. 调用昂贵的 MCP 操作：mcp__plugin_api_server__analyze
2. 将结果存储在变量中以供重用
3. 对后续操作使用缓存的结果
4. 仅在数据更改时重新获取
```

### 并行工具调用

当工具之间不相互依赖时，并行调用：

```markdown
步骤：
1. 并行调用（Claude 自动处理）：
   - mcp__plugin_api_server__get_project
   - mcp__plugin_api_server__get_users
   - mcp__plugin_api_server__get_tags
2. 等待所有完成
3. 合并结果
```

## 集成最佳实践

### 用户体验

**提供反馈：**

```markdown
步骤：
1. 通知用户："正在搜索 Asana 任务..."
2. 调用 mcp__plugin_asana_asana__asana_search_tasks
3. 显示进度："找到 15 个任务，分析中..."
4. 向用户展示结果
```

**处理长时间操作：**

```markdown
步骤：
1. 警告用户："这可能需要一分钟..."
2. 分解为更小的步骤并更新
3. 显示增量进度
4. 完成成时的最终摘要
```

### 错误消息

**好的错误消息：**
```
❌ "无法创建任务。请检查：
   - 您已登录到 Asana
   - 您有权访问工作区 'Engineering'
   - 项目 'Q1 Goals' 存在
```

**差的错误消息：**
```
❌ "错误：MCP 工具返回 403"
```

### 文档化

**在命令中文档化 MCP 工具使用：**

```markdown
## 使用的 MCP 工具

此命令使用以下 Asana MCP 工具：
- **asana_search_tasks**：搜索符合条件的任务
- **asana_create_task**：使用详细信息创建新任务
- **asana_update_task**：更新现有任务属性

运行此命令前，确保已向 Asana 认证。
```

## 测试工具使用

### 本地测试

```markdown
步骤：
1. 在 `.mcp.json` 中配置 MCP 服务器
2. 在 `.claude-plugin/` 本地安装插件
3. 使用 `/mcp` 验证工具可用
4. 测试使用工具的命令
5. 检查调试输出：`claude --debug`
```

### 测试成功调用

```markdown
步骤：
1. 在外部服务中创建测试数据
2. 运行使用该数据的命令
3. 验证返回了正确结果
```

### 测试错误情况

```markdown
步骤：
1. 测试缺少认证
2. 测试无效参数
3. 测试不存在的资源
4. 验证优雅的错误处理
```

### 测试边缘情况

```markdown
步骤：
1. 测试空结果
2. 测试最大结果
3. 测试包含特殊字符
4. 测试并发访问
```

## 常见模式

### 模式：CRUD 操作

```markdown
---
allowed-tools: [
  "mcp__plugin_api_server__create_item",
  "mcp__plugin_api_server__read_item",
  "mcp__plugin_api_server__update_item",
  "mcp__plugin_api_server__delete_item"
]
---

# 项目管理

## 创建
使用 create_item 及必需字段...

## 读取
使用 read_item 及项 ID...

## 更新
使用 update_item 及项 ID 和更改...

## 删除
使用 delete_item 及项 ID（首先询问确认）...
```

### 模式：搜索和处理

```markdown
步骤：
1. **搜索**：使用带有过滤器的 mcp__plugin_api_server__search
2. **筛选**：如果需要，应用额外的本地筛选
3. **转换**：处理每个结果
4. **展示**：为用户格式化并展示
```

### 模式：多步骤工作流

```markdown
步骤：
1. **设置**：收集所有必需信息
2. **验证**：检查数据完整性
3. **执行**：MCP 工具调用链：
   - 创建父资源
   - 创建子资源
   - 链接资源
   - 添加元数据
4. **验证**：确认所有步骤成功
5. **报告**：向用户提供摘要
```

## 故障排除

### 工具不可用

**检查：**
- MCP 服务器配置正确
-  服务器已连接（检查 `/mcp`）
- 工具名称完全匹配（区分大小写）
- 检查 `claude --debug` 日志

**工具调用失败：**
- 认证已通过
- 参数匹配工具模式
- 检查所需权限
- 检查 `claude --debug` 日志

**性能问题：**
- 批处理请求而不是单个查询
- 在适当时缓存结果
- 在可能时并行调用

### 结论

有效的 MCP 工具使用需要：
1. **理解工具模式**：通过 `/mcp`
2. **在命令中预先允许工具**：明确指定需要
3. **优雅处理错误**：提供有用的错误消息
4. **优化性能**：使用批处理和缓存
5. **提供良好的用户体验**：反馈和清晰的错误
6. **测试彻底**：在部署前测试所有场景

遵循这些模式以在您的插件命令和代理中实现强大的 MCP 工具集成。
