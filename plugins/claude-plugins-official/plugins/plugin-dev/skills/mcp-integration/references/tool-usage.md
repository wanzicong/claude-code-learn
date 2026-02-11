# 在命令和代理中使用 MCP 工具

在 Claude Code 插件命令和代理中有效使用 MCP 工具的完整指南。

## 概述

配置 MCP 服务器后，其工具将以前缀 `mcp__plugin_<插件名>_<服务器名>__<工具名>` 可用。在命令和代理中使用这些工具，就像使用 Claude Code 内置工具一样。

## 工具命名约定

### 格式

```
mcp__plugin_<插件名>_<服务器名>__<工具名>
```

### 示例

**带有 asana 服务器的 Asana 插件：**
- `mcp__plugin_asana_asana__asana_create_task`
- `mcp__plugin_asana_asana__asana_search_tasks`
- `mcp__plugin_asana_asana__asana_get_project`

**带有数据库服务器的自定义插件：**
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
- 工具架构和描述
- 用于配置的完整工具名称

## 在命令中使用工具

### 预允许工具

在命令 frontmatter 中指定 MCP 工具：

```markdown
---
description: 创建新的 Asana 任务
allowed-tools: [
  "mcp__plugin_asana_asana__asana_create_task"
]
---

# 创建任务命令

创建任务：
1. 从用户收集任务详细信息
2. 使用 mcp__plugin_asana_asana__asana_create_task 并附带详细信息
3. 向用户确认创建
```

### 多个工具

```markdown
---
allowed-tools: [
  "mcp__plugin_asana_asana__asana_create_task",
  "mcp__plugin_asana_asana__asana_search_tasks",
  "mcp__plugin_asana_asana__asana_get_project"
]
---
```

### 通配符（谨慎使用）

```markdown
---
allowed-tools: ["mcp__plugin_asana_asana__*"]
---
```

**注意：** 仅当命令确实需要访问服务器的所有工具时才使用通配符。

### 命令指令中的工具使用

**示例命令：**
```markdown
---
description: 搜索和创建 Asana 任务
allowed-tools: [
  "mcp__plugin_asana_asana__asana_search_tasks",
  "mcp__plugin_asana_asana__asana_create_task"
]
---

# Asana 任务管理

## 搜索任务

搜索任务：
1. 使用 mcp__plugin_asana_asana__asana_search_tasks
2. 提供搜索筛选器（分配者、项目等）
3. 向用户显示结果

## 创建任务

创建任务：
1. 收集任务详细信息：
   - 标题（必需）
   - 描述
   - 项目
   - 分配者
   - 截止日期
2. 使用 mcp__plugin_asana_asana__asana_create_task
3. 显示任务链接的确认
```

## 在代理中使用工具

### 代理配置

代理可以自主使用 MCP 工具而无需预允许：

```markdown
---
name: asana-status-updater
description: 当用户要求"更新 Asana 状态"、"生成项目报告"或"同步 Asana 任务"时使用此代理
model: inherit
color: blue
---

## 角色

用于生成 Asana 项目状态报告的自主代理。

## 过程

1. **查询任务**：使用 mcp__plugin_asana_asana__asana_search_tasks 获取所有任务
2. **分析进度**：计算完成率并识别阻塞项
3. **生成报告**：创建格式化的状态更新
4. **更新 Asana**：使用 mcp__plugin_asana_asana__asana_create_comment 发布报告

## 可用工具

该代理无需预批准即可访问所有 Asana MCP 工具。
```

### 代理工具访问

代理比命令具有更广泛的工具访问：
- 可以使用 Claude 认为必要的任何工具
- 不需要预允许列表
- 应记录它们通常使用的工具

## 工具调用模式

### 模式 1：简单工具调用

带验证的单个工具调用：

```markdown
步骤：
1. 验证用户提供的必需字段
2. 使用验证后的数据调用 mcp__plugin_api_server__create_item
3. 检查错误
4. 显示确认
```

### 模式 2：顺序工具调用

链式多个工具调用：

```markdown
步骤：
1. 搜索现有项：mcp__plugin_api_server__search
2. 如果未找到，则创建新项：mcp__plugin_api_server__create
3. 添加元数据：mcp__plugin_api_server__update_metadata
4. 返回最终项 ID
```

### 模式 3：批处理操作

使用同一工具的多次调用：

```markdown
步骤：
1. 获取要处理的项目列表
2. 对每个项目：
   - 调用 mcp__plugin_api_server__update_item
   - 跟踪成功/失败
3. 报告结果摘要
```

### 模式 4：错误处理

优雅的错误处理：

```markdown
步骤：
1. 尝试调用 mcp__plugin_api_server__get_data
2. 如果发生错误（速率限制、网络等）：
   - 等待并重试（最多 3 次尝试）
   - 如果仍然失败，通知用户
   - 建议检看配置
3. 成功时，处理数据
```

## 工具参数

### 理解工具架构

每个 MCP 工具都有定义其参数的架构。使用 `/mcp` 查看。

**示例架构：**
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
```

### 带参数调用工具

Claude 根据架构自动构建工具调用：

```typescript
// Claude 内部生成此内容
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

**在命令中，调用前验证：**

```markdown
步骤：
1. 检查必需参数：
   - 标题不为非空
   - 提供了工作区 ID
   - 截止日期为有效格式（YYYY-MM-DD）
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
   - 为用户显示进行格式化
   - 提供确认消息
   - 包含相关链接或 ID
```

### 错误响应

```markdown
步骤：
1. 调用 MCP 工具
2. 发生错误时：
   - 检查错误类型（身份验证、速率限制、验证等）
   - 提供有用的错误消息
   - 建议补救步骤
   - 不要向用户暴露内部错误详细信息
```

### 部分成功

```markdown
步骤：
1. 带有多个 MCP 调用的批处理操作
2. 分别跟踪成功和失败
3. 报告摘要：
   - "成功处理 10 个项目中的 8 个"
   - "失败的项目：[item1, item2]，原因：[原因]"
   - 建议重试或手动干预
```

## 性能优化

### 批处理请求

**好：带筛选器的单个查询**
```markdown
步骤：
1. 使用带筛选器的 mcp__plugin_api_server__search：
   - project_id: "123"
   - status: "active"
   - limit: 100
2. 处理所有结果
```

**避免：多个单独查询**
```markdown
步骤：
1. 对每个项 ID：
   - 调用 mcp__plugin_api_server__get_item
   - 处理项
```

### 缓存结果

```markdown
步骤：
1. 调用昂贵的 MCP 操作：mcp__plugin_api_server__analyze
2. 在变量中存储结果以供重用
3. 对后续操作使用缓存的结果
4. 仅在数据更改时重新获取
```

### 并行工具调用

当工具互不依赖时，并行调用：

```markdown
步骤：
1. 进行并行调用（Claude 自动处理）：
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
4. 展示结果
```

**处理长时间操作：**
```markdown
步骤：
1. 警告用户："这可能需要一分钟..."
2. 分解为带有更新的较小步骤
3. 显示增量进度
4. 完成后显示最终摘要
```

### 错误消息

**好的错误消息：**
```
❌ 无法创建任务。请检看：
   1. 您已登录 Asana
   2. 您有权访问工作区 'Engineering'
   3. 项目 'Q1 Goals' 存在
```

**差的错误消息：**
```
❌ 错误：MCP 工具返回 403
```

### 文档

**在命令中记录 MCP 工具使用：**
```markdown
## 使用的 MCP 工具

此命令使用以下 Asana MCP 工具：
- **asana_search_tasks**：搜索匹配条件的任务
- **asana_create_task**：附带详细信息创建新任务
- **asana_update_task**：更新现有任务属性

运行此命令前确保已对 Asana 进行身份验证。
```

## 测试工具使用

### 本地测试

1. 在 `.mcp.json` 中配置 MCP 服务器
2. 在 `.claude-plugin/` 中本地安装插件
3. 使用 `/mcp` 验证工具可用
4. 测试使用工具的命令
5. 检查调试输出：`claude --debug`

### 测试场景

**测试成功调用：**
```markdown
步骤：
1. 在外部服务中创建测试数据
2. 运行查询此数据的命令
3. 验证返回正确结果
```

**测试错误场景：**
```markdown
步骤：
1. 使用缺少的身份验证进行测试
2. 使用无效参数进行测试
3. 使用不存在的资源进行测试
4. 验证优雅的错误处理
```

**测试边界情况：**
```markdown
步骤：
1. 测试空结果
2. 测试最大结果
3. 测试特殊字符
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
使用 create_item 并附带必需字段...

## 读取
使用 read_item 并附带项 ID...

## 更新
使用 update_item 并附带项 ID 和更改...

## 删除
使用 delete_item 并附带项 ID（先请求确认）...
```

### 模式：搜索和处理

```markdown
步骤：
1. **搜索**：使用带筛选器的 mcp__plugin_api_server__search
2. **筛选**：如需要则应用额外的本地筛选
3. **转换**：处理每个结果
4. **展示**：格式化并向用户显示
```

### 模式：多步骤工作流

```markdown
步骤：
1. **设置**：收集所有必需信息
2. **验证**：检看数据完整性
3. **执行**：MCP 工具调用链：
   - 创建父资源
   - 创建子资源
   - 链接资源在一起
   - 添加元数据
4. **验证**：确认所有步骤成功
5. **报告**：向用户提供摘要
```

## 故障排除

### 工具不可用

**检看：**
- MCP 服务器配置正确
- 服务器已连接（检看 `/mcp`）
- 工具名称完全匹配（区分大小写）
- 配置更改后重启 Claude Code

### 工具调用失败

**检看：**
- 身份验证有效
- 参数匹配工具架构
- 提供了必需参数
- 检查 `claude --debug` 日志

### 性能问题

**检看：**
- 批处理查询而非单独调用
- 适当时缓存结果
- 不进行不必要的工具调用
- 可能时并行调用

## 结论

有效的 MCP 工具使用需要：
1. **通过 `/mcp` 理解工具架构**
2. **在命令中适当预允许工具**
3. **优雅地处理错误**
4. **通过批处理和缓存优化性能**
5. **通过反馈和清晰错误提供良好的用户体验**
6. **部署前彻底测试**

遵循这些模式以在插件命令和代理中实现稳健的 MCP 工具集成。
