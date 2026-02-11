# 高级工作流模式

多步骤命令序列和复杂工作流的组合模式。

## 概述

高级工作流组合多个命令、协调调用之间的状态，并创建复杂的自动化序列。这些模式能够从简单命令构建块构建复杂功能。

## 多步骤命令模式

### 顺序工作流命令

指导用户通过多步骤流程的命令：

```markdown
---
description: 完整 PR 审查工作流
argument-hint: [pr-number]
allowed-tools: Bash(gh:*), Read, Grep
---

# PR 审查工作流，针对 #$1

## 步骤 1：获取 PR 详细信息
!`gh pr view $1 --json title,body,author,files`

## 步骤 2：审查文件
更改的文件：!`gh pr diff $1 --name-only`

对于每个文件：
- 检查代码质量
- 验证测试存在
- 审查文档

## 步骤 3：运行检查
测试状态：!`gh pr checks $1`

验证：
- 所有测试通过
- 无合并冲突
- CI/CD 成功

## 步骤 4：提供反馈

总结：
- 发现的问题（关键/次要）
- 改进建议
- 批准推荐

您想要：
1. 批准 PR
2. 请求更改
3. 仅留下注释

回复您的选择，我将帮助完成操作。
```

**关键功能：**
- 清晰编号的步骤
- 用于上下文的 Bash 执行
- 用于用户输入的决策点
- 下一步操作建议

### 状态携带工作流

在调用之间维护状态的命令：

```markdown
---
description: 初始化部署工作流
allowed-tools: Write, Bash(git:*)
---

# 初始化部署

创建部署跟踪文件...

当前分支：!`git branch --show-current`
最新提交：!`git log -1 --format=%H`

部署状态保存到 `.claude/deployment-state.local.md`：

\`\`\`markdown
---
initialized: true
branch: $(git branch --show-current)
commit: $(git log -1 --format=%H)
timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
status: initialized
---

# 部署跟踪

分支：$(git branch --show-current)
启动：$(date)

下一步：
1. 运行测试：/deploy-test
2. 构建：/deploy-build
3. 部署：/deploy-execute
\`\`\`

状态已保存。运行 `/deploy-test` 继续。
```

**下个命令** (`/deploy-test`)：
```markdown
---
description: 运行部署测试
allowed-tools: Read, Bash(npm:*)
---

从 `.claude/deployment-state.local.md` 读取部署状态...

运行测试：!`npm test`

将状态更新为 'tested'...

测试完成。运行 `/deploy-build` 继续。
```

**模式好处：**
- 命令间的持久状态
- 清晰的工作流进展
- 安全检查点
- 恢复能力

### 条件工作流分支

根据条件适应的命令：

```markdown
---
description: 智能部署工作流
argument-hint: [environment]
allowed-tools: Bash(git:*), Bash(npm:*), Read
---

# 部署到 $1

## 部署前检查

分支：!`git branch --show-current`
状态：!`git status --short`

**检查条件：**

1. 分支状态：
   - 如果 main/master：需要批准
   - 如果功能分支：关于目标的警告
   - 如果热修复：快通道程

2. 测试：
   !`npm test`
   - 如果测试失败：停止 - 首先修复测试
   - 如果测试通过：继续

3. 环境：
   - 如果 $1 = 'production'：额外验证
   - 如果 $1 = 'staging'：标准流程
   - 如果 $1 = 'dev'：最小检查

**工作流决策：**
基于以上，继续进行：[确定的工作流]

[根据环境和状态的条件的步骤]

准备部署？（是/否）
```

## 命令组合模式

### 命令链

设计协同工作的命令：

```markdown
---
description: 准备代码审查
---

# 准备代码审查

运行准备序列：

1. 格式化代码：/format-code
2. 运行 linter：/lint-code
3. 运行测试：/test-all
4. 生成覆盖率：/coverage-report
5. 创建审查摘要：/review-summary

这是一个元命令。完成以上每个步骤后，
我将编译结果并准备全面的审查材料。

开始序列...
```

**单个命令**很简单：
- `/format-code` - 仅格式化
- `/lint-code` - 仅 lint
- `/test-all` - 仅测试

**组合命令**编排它们。

### 管道模式

处理来自先前命令输出的命令：

```markdown
---
description: 分析测试失败
---

# 分析测试失败

## 步骤 1：获取测试结果
（如果未完成，首先运行 /test-all）

读取测试输出...

## 步骤 2：分类失败
- 不稳定的测试（随机失败）
- 一致的失败
- 新失败 vs 现有

## 步骤 3：优先级排序
按以下标准排序：
- 影响（关键路径 vs 边缘情况）
- 频率（总是失败 vs 有时失败）
- 工作量（快速修复 vs 主要工作）

## 步骤 4：生成修复计划
对于每个失败：
- 根本原因假设
- 建议的修复方法
- 估计工作量

您想要我：
1. 修复最高优先级失败
2. 为所有失败生成详细修复计划
3. 为每个创建 GitHub 问题
```

### 并行执行模式

协调多个同时操作的命令：

```markdown
---
description: 运行全面验证
allowed-tools: Bash(*), Read
---

# 全面验证

并行运行验证...

启动：
- 代码质量检查
- 安全扫描
- 依赖项审计
- 性能分析

这将需要 2-3 分钟。我将监控所有进程
并在完成时报告。

[轮询每个进程并报告进度]

所有验证完成。摘要：
- 质量：通过（0 个问题）
- 安全：警告（2 个次要问题）
- 依赖项：通过
- 性能：通过（达到基线）

详情：
[从所有检查汇总的结果]
```

## 工作流状态管理

### 使用 .local.md 文件

在插件特定文件中存储工作流状态：

```markdown
.claude/plugin-name-workflow.local.md:

---
workflow: deployment
stage: testing
started: 2025-01-15T10:30:00Z
environment: staging
branch: feature/new-api
commit: abc123def
tests_passed: false
build_complete: false
---

# 部署工作流状态

当前阶段：测试
启动：2025-01-15 10:30 UTC

完成的步骤：
- ✅ 验证
- ✅ 分支检查
- ⏳ 测试（进行中）

待处理步骤：
- 构建
- 部署
- 烟雾测试
```

**在命令中读取状态：**

```markdown
---
description: 继续部署工作流
allowed-tools: Read, Write
---

从 .claude/plugin-name-workflow.local.md 读取工作流状态...

当前阶段：@.claude/plugin-name-workflow.local.md

[解析 YAML frontmatter 以确定下一步]

基于状态的下个操作：[确定操作]
```

### 工作流恢复

处理中断的工作流：

```markdown
---
description: 恢复部署工作流
allowed-tools: Read
---

# 恢复部署

检查中断的工作流...

状态文件：@.claude/plugin-name-workflow.local.md

**找到工作流：**
- 启动：[时间戳]
- 环境：[env]
- 最后完成：[步骤]

**恢复选项：**
1. 从最后一步恢复
2. 从开始重新启动
3. 中止并清理

您想要？（1/2/3）
```

## 工作流协调模式

### 跨命令通信

相互发送信号的命令：

```markdown
---
description: 标记功能完成
allowed-tools: Write
---

# 标记功能完成

写入完成标记...

创建：.claude/feature-complete.flag

这向其他命令发出信号功能已准备好用于：
- 集成测试（/integration-test 将自动检测）
- 文档生成（/docs-generate 将包含）
- 发布说明（/release-notes 将添加）

功能已标记完成。
```

**其他命令检查标记：**

```markdown
---
description: 生成发布说明
allowed-tools: Read, Bash(git:*)
---

检查完成的功能...

if [ -f .claude/feature-complete.flag ]; then
  功能准备好发布说明
fi

[包含在发布说明中]
```

### 工作流锁定

防止并发工作流执行：

```markdown
---
description: 开始部署
allowed-tools: Read, Write, Bash
---

# 开始部署

检查活动的部署...

if [ -f .claude/deployment.lock ]; then
  错误：部署已在进行中
  启动：[来自锁定文件的时间戳]

  无法启动并发部署。
  等待完成或运行 /deployment-abort

  退出。
fi

创建部署锁定...

部署已启动。创建锁定。
[继续部署]
```

**锁定清理：**

```markdown
---
description: 完成部署
allowed-tools: Write, Bash
---

部署完成。

删除部署锁定...
rm .claude/deployment.lock

准备好下一个部署。
```

## 高级参数处理

### 带有默认值的可选参数

```markdown
---
description: 带有可选版本的部署
argument-hint: [environment] [version]
---

环境：${1:-staging}
版本：${2:-latest}

部署 ${2:-latest} 到 ${1:-staging}...

注意：对缺失参数使用默认值：
- 环境默认为 'staging'
- 版本默认为 'latest'
```

### 参数验证

```markdown
---
description: 部署到验证的环境
argument-hint: [environment]
---

环境：$1

验证环境...

valid_envs="dev staging production"
if ! echo "$valid_envs" | grep -w "$1" > /dev/null; then
  错误：无效环境 '$1'
  有效选项：dev、staging、production
  退出。
fi

环境已验证。继续...
```

### 参数转换

```markdown
---
description: 带有简写的部署
argument-hint: [env-shorthand]
---

输入：$1

扩展简写：
- d/dev → development
- s/stg → staging
- p/prod → production

case "$1" in
  d|dev) ENV="development";;
  s|stg) ENV="staging";;
  p|prod) ENV="production";;
  *) ENV="$1";;
esac

部署到：$ENV
```

## 工作流中的错误处理

### 优雅失败

```markdown
---
description: 弹性部署工作流
---

# 部署工作流

运行带有错误处理的步骤...

## 步骤 1：测试
!`npm test`

if [ $? -ne 0 ]; then
  错误：测试失败

  选项：
  1. 修复测试并重试
  2. 跳过测试（不推荐）
  3. 中止部署

  您想要做什么？

  [在继续之前等待用户输入]
fi

## 步骤 2：构建
[仅当步骤 1 成功时继续]
```

### 失败时回滚

```markdown
---
description: 带有回滚的部署
---

# 带有回滚的部署

保存当前状态以供回滚...
上一个版本：!`current-version.sh`

部署新版本...

!`deploy.sh`

if [ $? -ne 0 ]; then
  部署失败

  启动自动回滚...
  !`rollback.sh`

  已回滚到上一个版本。
  检查日志以获取失败详情。
fi

部署完成。
```

### 检查点恢复

```markdown
---
description: 带有检查点的工作流
---

# 多阶段部署

## 检查点 1：验证
!`validate.sh`
echo "checkpoint:validation" >> .claude/deployment-checkpoints.log

## 检查点 2：构建
!`build.sh`
echo "checkpoint:build" >> .claude/deployment-checkpoints.log

## 检查点 3：部署
!`deploy.sh`
echo "checkpoint:deploy" >> .claude/deployment-checkpoints.log

如果任何步骤失败，使用以下恢复：
/deployment-resume [最后成功的检查点]
```

## 最佳实践

### 工作流设计

1. **清晰进展**：编号步骤，显示当前位置
2. **明确状态**：不依赖隐式状态
3. **用户控制**：提供决策点
4. **错误恢复**：优雅处理失败
5. **进度指示**：显示已完成、待处理的内容

### 命令组合

1. **单一职责**：每个命令做好一件事
2. **可组合设计**：命令容易协同工作
3. **标准接口**：一致的输入/输出格式
4. **松散耦合**：命令不依赖彼此的内部

### 状态管理

1. **持久状态**：使用 .local.md 文件
2. **原子更新**：原子性地编写完整状态文件
3. **状态验证**：检查状态文件格式/完整性
4. **清理**：删除过时状态文件
5. **文档化**：文档化状态文件格式

### 错误处理

1. **快速失败**：尽早检测错误
2. **清晰消息**：解释什么出错
3. **恢复选项**：提供清晰的下一步
4. **状态保留**：保留状态以供恢复
5. **回滚能力**：支持撤销更改

## 示例：完整部署工作流

### 初始化命令

```markdown
---
description: 初始化部署
argument-hint: [environment]
allowed-tools: Write, Bash(git:*)
---

# 初始化部署到 $1

创建工作流状态...

\`\`\`yaml
---
workflow: deployment
environment: $1
branch: !`git branch --show-current`
commit: !`git rev-parse HEAD`
stage: initialized
timestamp: !`date -u +%Y-%m-%dT%H:%M:%SZ`
---
\`\`\`

写入到 .claude/deployment-state.local.md

下一步：运行 /deployment-validate
```

### 验证命令

```markdown
---
description: 验证部署
allowed-tools: Read, Bash
---

读取状态：@.claude/deployment-state.local.md

运行验证...
- 分支检查：通过
- 测试：通过
- 构建：通过

将状态更新为 'validated'...

下一步：运行 /deployment-execute
```

### 执行命令

```markdown
---
description: 执行部署
allowed-tools: Read, Bash, Write
---

读取状态：@.claude/deployment-state.local.md

执行部署到 [环境]...

!`deploy.sh [environment]`

部署完成。
将状态更新为 'completed'...

清理：/deployment-cleanup
```

### 清理命令

```markdown
---
description: 清理部署
allowed-tools: Bash
---

删除部署状态...
rm .claude/deployment-state.local.md

部署工作流完成。
```

此完整工作流展示了状态管理、顺序执行、错误处理以及跨多个命令的清晰关注点分离。
