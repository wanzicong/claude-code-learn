# Plugin Structure 技能

关于 Claude Code 插件架构、目录布局和最佳实践的综合指导。

## 概述

此技能提供关于以下内容的详细知识：
- 插件目录结构和组织
- `plugin.json` 清单配置
- 组件组织（commands、agents、skills、hooks）
- 自动发现机制
- 使用 `${CLAUDE_PLUGIN_ROOT}` 的可移植路径引用
- 文件命名约定

## 技能结构

### SKILL.md (1,619 字)

核心技能内容涵盖：
- 目录结构概述
- 插件清单（plugin.json）字段
- 组件组织模式
- ${CLAUDE_PLUGIN_ROOT} 使用
- 文件命名约定
- 自动发现机制
- 最佳实践
- 常见模式
- 故障排除

### 参考资料

用于深入了解的详细文档：

- **manifest-reference.md**：完整的 `plugin.json` 字段参考
  - 所有字段描述和示例
  - 路径解析规则
  - 验证指南
  - 最小化与完整清单示例

- **component-patterns.md**：高级组织模式
  - 组件生命周期（发现、激活）
  - 命令组织模式
  - 代理组织模式
  - 技能组织模式
  - Hook 组织模式
  - 脚本组织模式
  - 跨组件模式
  - 可扩展性的最佳实践

### 示例

三个完整的插件示例：

- **minimal-plugin.md**：最简单的可能插件
  - 单个命令
  - 最小化清单
  - 何时使用此模式

- **standard-plugin.md**：结构良好的生产插件
  - 多个组件（commands、agents、skills、hooks）
  - 带元数据的完整清单
  - 丰富的技能结构
  - 组件之间的集成

- **advanced-plugin.md**：企业级插件
  - 多级组织
  - MCP 服务器集成
  - 共享库
  - 配置管理
  - 安全自动化
  - 监控集成

## 此技能何时触发

当用户执行以下操作时，Claude Code 激活此技能：
- 请求"创建插件"或"搭建插件"
- 需要"了解插件结构"
- 想要"组织插件组件"
- 需要"设置 plugin.json"
- 询问关于"${CLAUDE_PLUGIN_ROOT}" 的使用
- 想要"添加 commands/agents/skills/hooks"
- 需要"配置自动发现"帮助
- 询问关于插件架构或最佳实践

## 渐进式披露

该技能使用渐进式披露来管理上下文：

1. **SKILL.md**（约 1600 字）：核心概念和工作流程
2. **参考资料**（约 6000 字）：详细字段引用和模式
3. **示例**（约 8000 字）：完整的工作示例

Claude 仅根据任务需要加载参考资料和示例。

## 相关技能

此技能与以下内容配合良好：
- **hook-development**：用于创建插件 hooks
- **mcp-integration**：用于集成 MCP 服务器（如果可用）
- **marketplace-publishing**：用于发布插件（如果可用）

## 维护

要更新此技能：
1. 保持 SKILL.md �精简，专注于核心概念
2. 将详细信息移动到 references/
3. 为常见模式添加新的 examples/
4. 更新 SKILL.md frontmatter 中的版本
5. 确保所有文档使用祈使语/不定式
