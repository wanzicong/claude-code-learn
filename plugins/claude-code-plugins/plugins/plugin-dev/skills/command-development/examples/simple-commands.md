# 简单命令示例

常见用例的基本斜杠命令模式。

**重要：**以下所有示例都编写为给 Claude 的指令（代理使用），而不是给用户的消息。命令告诉 Claude 做什么，而不是告诉用户会发生什么。

## 示例 1：代码审查命令

**文件：**`.claude/commands/review.md`

```markdown
---
description: 审查代码质量和问题
allowed-tools: Read, Bash(git:*)
---

审查此代码库中的 代码以检查：

1. **代码质量：**
   - 可读性和可维护性
   - 一致的样式和格式
   - 适当的抽象级别

2. **潜的问题：**
   - 逻辑错误或 bug
   - 未处理的边缘情况
   - 性能问题

3. **最佳实践：**
   - 正确使用设计模式
   - 存在错误处理
   - 文档充分

提供带有文件和行引用的具体反馈。
```

**用法：**
```
> /review
```

---

## 示例 2：安全审查命令

**文件：**`.claude/commands/security-review.md`

```markdown
---
description: 审查代码的安全漏洞
allowed-tools: Read, Grep
model: sonnet
---

执行全面安全审查以检查：

**常见漏洞：**
- SQL 注入风险
- 跨站脚本攻击 (XSS)
- 身份验证/授权问题
- 不安全的数据处理
- 硬编码的密钥或凭据

**安全最佳实践：**
- 存在输入验证
- 输出编码正确
- 使用安全默认值
- 错误消息安全
- 日志记录适当（无敏感数据）

对于发现的每个问题：
- 文件和行号
- 严重性（严重/高/中/低）
- 漏洞描述
- 推荐的修复

按严重性对问题进行排序。
```

**用法：**
```
> /security-review
```

---

## 示例 3：带文件参数的测试命令

**文件：**`.claude/commands/test-file.md`

```markdown
---
description: 为特定文件运行测试
argument-hint: [test-file]
allowed-tools: Bash(npm:*), Bash(jest:*)
---

为 $1 运行测试：

测试执行：!`npm test $1`

分析结果：
- 测试通过/失败
- 代码覆盖率
- 性能问题
- 不稳定的测试

如果发现失败，根据错误消息建议修复。
```

**用法：**
```
> /test-file src/utils/helpers.test.ts
```

---

## 示例 4：文档生成器

**文件：**`.claude/commands/document.md`

```markdown
---
description: 为文件生成文档
argument-hint: [source-file]
---

为 @$1 生成综合文档

包括：

**概述：**
- 目的和职责
- 主要功能
- 依赖项

**API 文档：**
- 函数/方法签名
- 带有类型的参数描述
- 带有类型的返回值
- 抛出的异常/错误

**用法示例：**
- 基本用法
- 常见模式
- 边缘情况

**实现注释：**
- 算法复杂度
- 性能考虑
- 已知限制

格式为适合项目文档的 Markdown。
```

**用法：**
```
> /document src/api/users.ts
```

---

## 示例 5：Git 状态摘要

**文件：**`.claude/commands/git-status.md`

```markdown
---
description: 摘要 Git 存储库状态
allowed-tools: Bash(git:*)
---

存储库状态摘要：

**当前分支：**!`git branch --show-current`

**状态：**!`git status --short`

**最近提交：**!`git log --oneline -5`

**远程状态：**!`git fetch && git status -sb`

提供：
- 更改摘要
- 建议的下一步操作
- 任何警告或问题
```

**用法：**
```
> /git-status
```

---

## 示例 6：部署命令

**文件：**`.claude/commands/deploy.md`

```markdown
---
description: 部署到指定环境
argument-hint: [environment] [version]
allowed-tools: Bash(kubectl:*), Read
---

使用版本 $2 部署到 $1 环境

**部署前检查：**
1. 验证 $1 配置存在
2. 检查版本 $2 有效
3. 验证集群可访问性：!`kubectl cluster-info`

**部署步骤：**
1. 使用版本 $2 更新部署清单
2. 将配置应用到 $1
3. 监控推出状态
4. 验证 pod 健康
5. 运行烟雾测试

**回滚计划：**
文档化当前版本以供问题发生时回滚。

继续部署？（是/否）
```

**用法：**
```
> /deploy staging v1.2.3
```

---

## 示例 7：比较命令

**文件：**`.claude/commands/compare-files.md`

```markdown
---
description比较两个文件
argument-hint: [file1] [file2]
---

比较 @$1 与 @$2

**分析：**

1. **差异：**
   - 添加的行
   - 删除的行
   - 修改的行

2. **功能更改：**
   - 破坏性更改
   - 新功能
   - Bug 修复
   - 重构

3. **影响：**
   - 受影响的组件
   - 其他地方需要的更新
   - 迁移要求

4. **推荐：**
   - 代码审查重点区域
   - 测试要求
   - 需要的文档更新

作为结构化比较报告展示。
```

**用法：**
```
> /compare-files src/old-api.ts src/new-api.ts
```

---

## 示例 8：快速修复命令

**文件：**`.claude/commands/quick-fix.md`

```markdown
---
description: 常见问题的快速修复
argument-hint: [issue-description]
model: haiku
---

快速修复：$ARGUMENTS

**方法：**
1. 识别问题
2. 查找相关代码
3. 建议修复
4. 解释解决方案

专注于：
- 简单、直接的解决方案
- 最小更改
- 遵循现有模式
- 无破坏性更改

提供带有文件路径和行号的代码更改。
```

**用法：**
```
> /quick-fix 按钮不响应点击
> /quick-fix 错误消息中的拼写错误
```

---

## 示例 9：研究命令

**文件：**`.claude/commands/research.md`

```markdown
---
description: 研究主题的最佳实践
argument-hint: [topic]
model: sonnet
---

研究以下内容的最佳实践：$ARGUMENTS

**覆盖范围：**

1. **当前状态：**
   - 我们当前如何处理此问题
   - 现有实现

2. **行业标准：**
   - 常见模式
   - 推荐方法
   - 工具和库

3. **比较：**
   - 我们的方法与标准
   - 差距或需要改进
   - 迁移考虑

4. **推荐：**
   - 具体操作项
   - 优先级和工作量估计
   - 实现资源

根据研究提供可操作指导。
```

**用法：**
```
> /research 异步操作中的错误处理
> /research API 身份验证模式
```

---

## 示例 10：解释代码命令

**文件：**`.claude/commands/explain.md`

```markdown
---
description: 解释代码如何工作
argument-hint: [file-or-function]
---

详细解释 @$1

**解释结构：**

1. **概述：**
   - 它做什么
   - 为什么存在
   - 如何适配系统

2. **逐步：**
   - 逐行演练
   - 关键算法或逻辑
   - 重要细节

3. **输入和输出：**
   - 参数和类型
   - 返回值
   - 副作用

4. **边缘情况：**
   - 错误处理
   - 特殊情况
   - 限制

5. **用法用例：**
   - 如何调用它
   - 常见模式
   - 集成点

以适合初级工程师的水平进行解释。
```

**用法：**
```
> /explain src/utils/cache.ts
> /explain AuthService.login
```

---

## 关键模式

### 模式 1：仅读分析

```markdown
---
allowed-tools: Read, Grep
---

分析但不修改...
```

**用于：**代码审查、文档、分析

### 模式 2：Git 操作

```markdown
---
allowed-tools: Bash(git:*)
---

!`git status`
分析并建议...
```

**用于：**存储库状态、提交分析

### 模式 3：单个参数

```markdown
---
argument-hint: [target]
---

处理 $1...
```

**用于：**文件操作、目标操作

### 模式 4：多参数

```markdown
---
argument-hint: [source] [target] [options]
---

处理 $1 到 $2，使用 $3...
```

**用于：**工作流、部署、比较

### 模式 5：快速执行

```markdown
---
model: haiku
---

快速简单任务...
```

**用于：**简单、重复的命令

### 模式 6：文件比较

```markdown
比较 @$1 与 @$2...
```

**用于：**差异分析、迁移规划

### 模式7：上下文收集

```markdown
---
allowed-tools: Bash(git:*), Read
---

上下文：!`git status`
文件：@file1 @file2

分析...
```

**用于：**明智的决策制定

## 编写简单命令的提示

1. **从基本开始：**单一职责、明确目的
2. **逐渐增加复杂性：**从没有 frontmatter 开始
3. **增量测试：**验证每个功能工作
4. **使用描述性名称：**命令名称应指示目的
5. **文档化参数：**始终使用 argument-hint
6. **提供用例：**在注释中显示用法
7. **处理错误：**考虑缺失的参数或文件
