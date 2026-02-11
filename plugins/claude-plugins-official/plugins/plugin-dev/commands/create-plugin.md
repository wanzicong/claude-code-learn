---
description: 指导端到端插件创建工作流，包括组件设计、实现和验证
argument-hint: 可选的插件描述
allowed-tools: ["Read", "Write", "Grep", "Glob", "Bash", "TodoWrite", "AskUserQuestion", "Skill", "Task"]
---

# 插件创建工作流

指导用户从头开始创建完整的、高质量的 Claude Code 插件，从初始概念到经过测试的实现。遵循系统方法：理解需求、设计组件、澄清细节、按照最佳实践实现、验证和测试。

## 核心原则

- **提出澄清问题**：识别关于插件目的、触发、范围和组件的所有歧义。提出具体、具体的问题而不是做出假设。在继续实现之前等待用户回答。
- **加载相关技能**：在需要时使用 Skill 工具加载 plugin-dev 技能（plugin-structure、hook-development、agent-development 等）
- **使用专用代理**：利用 agent-creator、plugin-validator 和 skill-reviewer 代理进行 AI 辅助开发
- **遵循最佳实践**：应用 plugin-dev 自身实现中的模式
- **渐进式披露**：创建带有 references/examples 的精简技能
- **使用 TodoWrite**：在所有阶段跟踪所有进度

**初始请求：** $ARGUMENTS

---

## 阶段 1：发现

**目标**：了解需要构建什么插件以及它解决什么问题

**操作**：
1. 创建包含所有 7 个阶段的待办事项列表
2. 如果插件目的从参数中清晰：
   - 总结理解
   - 识别插件类型（integration、workflow、analysis、toolkit 等）
3. 如果插件目的不清楚，询问用户：
   - 此插件解决什么问题？
   - 谁将使用它以及何时使用？
   - 它应该做什么？
   - 有哪些类似的插件可以参考？
4. 在继续之前总结理解并与用户确认

**输出**：插件目的和目标用户的清晰声明

---

## 阶段 2：组件规划

**目标**：确定需要哪些插件组件

**在此阶段之前必须使用 Skill 工具加载 plugin-structure 技能。**

**操作**：
1. 加载 plugin-structure 技能以了解组件类型
2. 分析插件需求并确定所需组件：
   - **技能**：是否需要专门知识？（hooks API、MCP 模式等）
   - **命令**：用户发起的操作？（部署、配置、分析）
   - **代理**：自主任务？（验证、生成、分析）
   - **Hooks**：事件驱动的自动化？（验证、通知）
   - **MCP**：外部服务集成？（数据库、API）
   - **设置**：用户配置？（.local.md 文件）
3. 对于每种需要的组件类型，识别：
   - 每种类型需要多少个
   - 每个做什么
   - 大致的触发/使用模式
4. 以表格形式向用户展示组件计划：
   ```
   | 组件类型 | 数量 | 目的 |
   |----------------|-------|---------|
   | 技能         | 2     | Hook 模式、MCP 使用 |
   | 命令       | 3     | 部署、配置、验证 |
   | 代理         | 1     | 自主验证 |
   | Hooks          | 0     | 不需要 |
   | MCP            | 1     | 数据库集成 |
   ```
5. 获得用户确认或调整

**输出**：要创建的组件的确认列表

---

## 阶段 3：详细设计和澄清问题

**目标**：详细指定每个组件并解决所有歧义

**关键**：这是最重要的阶段之一。不要跳过。

**操作**：
1. 对于计划中的每个组件，识别未指定的方面：
   - **技能**：什么触发它们？它们提供什么知识？有多详细？
   - **命令**：什么参数？什么工具？交互式还是自动化？
   - **代理**：何时触发（主动/被动）？什么工具？输出格式？
   - **Hooks**：哪些事件？基于 prompt 还是命令？验证标准？
   - **MCP**：什么服务器类型？身份验证？哪些工具？
   - **设置**：什么字段？必填还是可选？默认值？

2. **以有组织的部分向用户展示所有问题**（每个组件类型一个部分）

3. **在继续实现之前等待答案**

4. 如果用户说"无论你认为什么最好"，提供具体建议并获得明确的确认

**技能示例问题**：
- 什么特定的用户查询应该触发此技能？
- 它是否应该包括实用脚本？什么功能？
- 核心的 SKILL.md 应该有多详细 vs references/？
- 有哪些真实的示例要包括？

**代理示例问题**：
- 此代理是否应该在特定操作后主动触发，还是仅在明确请求时？
- 它需要什么工具（Read、Write、Bash 等）？
- 输出格式应该是什么？
- 有什么特定的质量标准要强制执行？

**输出**：每个组件的详细规范

---

## 阶段 4：插件结构创建

**目标**：创建插件目录结构和 manifest

**操作**：
1. 确定插件名称（kebab-case，描述性）
2. 选择插件位置：
   - 询问用户："Where should I create plugin?"
   - 提供选项：当前目录、../new-plugin-name、自定义路径
3. 使用 bash 创建目录结构：
   ```bash
   mkdir -p plugin-name/.claude-plugin
   mkdir -p plugin-name/skills     # 如果需要
   mkdir -p plugin-name/commands   # 如果需要
   mkdir -p plugin-name/agents     # 如果需要
   mkdir -p plugin-name/hooks      # 如果需要
   ```
   - 使用 Write 工具创建 plugin.json manifest：
   ```json
   {
     "name": "plugin-name",
     "version": "0.1.0",
     "description": "[简要描述]",
     "author": {
       "name": "[来自用户或默认的作者]",
       "email": "[电子邮件或默认值]"
     }
   }
   ```
5. 创建 README.md 模板
6. 如果需要，创建 .gitignore（用于 .claude/*.local.md 等）
7. 如果创建新目录，初始化 git 仓库

**输出**：插件目录结构已创建并准备好接收组件

---

## 阶段 5：组件实现

**目标**：按照最佳实践创建每个组件

**在实现每种组件类型之前加载相关技能**：
- 技能：加载 skill-development 技能
- 命令：加载 command-development 技能
- 代理：加载 agent-development 技能
- Hooks：加载 hook-development 技能
- MCP：加载 mcp-integration 技能
- 设置：加载 plugin-settings 技能

**每个组件的操作**：

### 对于技能：
1. 使用 Skill 工具加载 skill-development 技能
2. 对于每个技能：
   - 询问用户具体的用例示例（或从阶段 3 使用）
   - 计划资源（scripts/、references/、examples/）
   - 创建技能目录结构
   - 编写 SKILL.md，其中包括：
     - 第三人称描述，带有特定触发短语
     - 精简的正文（1,500-2,000 字）采用命令形式
     -对支持文件的引用
   - 创建详细内容的参考文件
   - 创建可工作代码的示例文件
   - 如果需要，创建实用脚本
3. 使用 skill-reviewer 代理验证每个技能

### 对于命令：
1. 使用 Skill 工具加载 command-development 技能
2. 对于每个命令：
   - 编写带有 frontmatter 的命令 markdown
   - 包括清晰的描述和 argument-hint
   - 指定 allowed-tools（最小必要）
   - 编写给 Claude 的指令（而不是给用户）
   - 提供使用示例和提示
   - 如果适用，引用相关技能

### 对于代理：
1. 使用 Skill 工具加载 agent-development 技能
2. 对于每个代理，使用 agent-creator 代理：
   - 提供代理应该做什么的描述
   - Agent-creator 生成：identifier、whenToUse 带有示例、systemPrompt
   - 创建带有 frontmatter 和系统提示的代理 markdown 文件
   - 添加适当的模型、颜色和工具
   - 使用 validate-agent.sh 脚本验证

### 对于 Hooks：
1. 使用 Skill 工具加载 hook-development 技能
2. 对于每个 hook：
   - 使用 hook 配置创建 hooks/hooks.json
   - 对于复杂逻辑，首选基于 prompt 的 hooks
   - 使用 ${CLAUDE_PLUGIN_ROOT} 进行可移植性
   - 如果需要，创建 hook 脚本（在 examples/ 而不是 scripts/ 中）
   - 使用 validate-hook-schema.sh 和 test-hook.sh 工具进行测试

### 对于 MCP：
1. 使用 Skill 工具加载 mcp-integration 技能
2. 创建 .mcp.json 配置，其中包括：
   - 服务器类型（stdio 用于本地，SSE 用于托管）
   - 命令和参数（带有 ${CLAUDE_PLUGIN_ROOT}）
   - extensionToLanguage 映射（如果 LSP）
   - 根据需要的环境变量
3. 在 README 中记录所需的环境变量
4. 提供设置说明

### 对于设置：
1. 使用 Skill 工具加载 plugin-settings 技能
2. 在 README 中创建设置模板
3. 创建示例 .claude/plugin-name.local.md 文件（作为文档）
4. 根据需要在 hooks/commands 中实现设置读取
5. 添加到 .gitignore：`.claude/*.local.md`

**进度跟踪**：在每个组件完成后更新待办事项

**输出**：所有插件组件已实现

---

## 阶段 6：验证和质量检查

**目标**：确保插件符合质量标准并正常工作

**操作**：
1. **运行 plugin-validator 代理**：
   - 使用 plugin-validator 代理全面验证插件
   - 检查：manifest、结构、命名、组件、安全
   - 审查验证报告

2. **修复关键问题**：
   - 解决来自验证的任何关键错误
   - 修复任何指示真正问题的警告

3. **使用 skill-reviewer 审查**（如果插件有技能）：
   - 对于每个技能，使用 skill-reviewer 代理
   - 检查描述质量、渐进式披露、写作风格
   - 应用建议

4. **测试代理触发**（如果插件有代理）：
   - 对于每个代理，验证 <example> 块清晰
   - 检查触发条件具体
   - 在代理文件上运行 validate-agent.sh

5. **测试 hook 配置**（如果插件有 hooks）：
   - 在 hooks/hooks.json 上运行 validate-hook-schema.sh
   - 使用 test-hook.sh 测试 hook 脚本
   - 验证 ${CLAUDE_PLUGIN_ROOT} 使用

6. **展示发现**：
   - 验证结果摘要
   - 任何剩余问题
   - 总体质量评估

7. **询问用户**："Validation complete. Issues found: [count critical], [count warnings]. Would you like me to fix them now, or proceed to testing?"

**输出**：插件已验证并准备好测试

---

## 阶段 7：测试和验证

**目标**：测试插件在 Claude Code 中正常工作

**操作**：
1. **安装说明**：
   - 向用户展示如何本地测试：
     ```bash
     cc --plugin-dir /path/to/plugin-name
     ```
   - 或复制到 `.claude-plugin/` 进行项目测试

2. **用户执行的验证清单**：
   - [ ] 技能在触发时加载（使用描述中的触发短语提问）
   - [ ] 命令出现在 `/help` 中并正确执行
   - [ ] 代理在适当场景中触发
   - [ ] Hooks 在事件上激活（如果适用）
   - [ ] MCP 服务器连接（如果适用）
   - [ ] 设置文件工作（如果适用）

3. **测试建议**：
   - 对于技能：使用描述中的触发短语提问
   - 对于命令：使用各种参数运行 `/plugin-name:command-name`
   - 对于代理：创建匹配代理示例的场景
   - 对于 hooks：使用 `claude --debug` 查看 hook 执行
   - 对于 MCP：使用 `/mcp` 验证服务器和工具

4. **询问用户**："I've prepared the plugin for testing. Would you like me to guide you through testing each component, or do you want to test it yourself?"

5. **如果用户想要指导**，使用特定测试用例指导测试每个组件

**输出**：插件已测试并验证工作

---

## 阶段 8：文档和下一步

**目标**：确保插件文档齐全并准备好分发

**操作**：
1. **验证 README 完整性**：
   - 检查 README 具有：overview、features、installation、prerequisites、usage
   - 对于 MCP 插件：记录所需的环境变量
   - 对于 hook 插件：解释 hook 激活
   - 对于设置：提供配置模板

2. **添加 marketplace 条目**（如果发布）：
   - 向用户展示如何添加到 marketplace.json
   - 帮助起草 marketplace 描述
   - 建议类别和标签

3. **创建摘要**：
   - 标记所有待办事项完成
   - 列出创建的内容：
     - 插件名称和目的
     - 创建的组件（X 技能、Y 命令、Z 代理等）
     - 关键文件及其用途
     - 总文件数和结构
   - 下一步：
     - 测试建议
     - 发布到 marketplace（如果需要）
     - 基于使用情况的迭代

4. **建议改进**（可选）：
   - 可以增强插件的其他组件
   - 集成机会
   - 测试策略

**输出**：完整的、文档齐全的插件准备好使用或发布

---

## 重要说明

### 在所有阶段中

- **使用 TodoWrite** 在每个阶段跟踪进度
- **在使用特定组件类型时使用 Skill 工具加载技能**
- **使用专用代理**（agent-creator、plugin-validator、skill-reviewer）
- **在关键决策点请求用户确认**
- **遵循 plugin-dev 自身的模式作为参考示例**
- **应用最佳实践**：
  - 技能的第三人称描述
  - 技能正文中的命令形式
  - 给 Claude 编写的命令
  - 强触发短语
  - ${CLAUDE_PLUGIN_ROOT} 用于可移植性
  - 渐进式披露
  - 安全优先（HTTPS、无硬编码凭证）

### 关键决策点（等待用户）

1. 阶段 1 之后：确认插件目的
2. 阶段 2 之后：批准组件计划
3. 阶段 3 之后：继续实现
4. 阶段 6 之后：修复问题或继续
5. 阶段 7 之后：继续文档

### 按阶段加载技能

- **阶段 2**：plugin-structure
- **阶段 5**：skill-development、command-development、agent-development、hook-development、mcp-integration、plugin-settings（根据需要）
- **阶段 6**：（代理将自动使用技能）

### 质量标准

每个组件必须符合这些标准：
- 遵循 plugin-dev 经过验证的模式
- 使用正确的命名约定
- 具有强触发条件（skills/agents）
- 包括可工作的示例
- 正确记录
- 使用工具验证
- 在 Claude Code 中测试

---

## 示例工作流

### 用户请求
"Create a plugin for managing database migrations"

### 阶段 1：发现
- 了解：迁移管理、数据库模式版本控制
- 确认：用户想要创建、运行、回滚迁移

### 阶段 2：组件规划
- 技能：1（迁移最佳实践）
- 命令：3（create-migration、run-migrations、rollback）
- 代理：1（migration-validator）
- MCP：1（数据库连接）

### 阶段 3：澄清问题
- 哪些数据库？（PostgreSQL、MySQL 等）
- 迁移文件格式？（SQL、基于代码？）
- 代理是否应该在应用之前验证？
- 需要什么 MCP 工具？（query、execute、schema）

### 阶段 4-8：实现、验证、测试、文档

---

**从阶段 1 开始：发现**
