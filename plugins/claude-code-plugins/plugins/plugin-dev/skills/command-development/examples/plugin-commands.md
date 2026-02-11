# 插件命令示例

为 Claude Code 插件设计的实用命令示例，展示插件特定模式和功能。

## 目录

1. [简单插件命令](#1-simple-plugin-command)
2. [基于脚本的分析](#2-script-based-analysis)
3. [基于模板的生成](#3-template-based-generation)
4. [多脚本工作流](#4-multi-script-workflow)
5. [配置驱动的部署](#5-configuration-driven-deployment)
6. [代理集成](#6-agent-integration)
7. [技能集成](#7-skill-integration)
8. [多组件工作流](#8-multi-component-workflow)
9. [验证输入命令](#9-validated-input-command)
10. [环境感知命令](#10-environment-aware-command)

---

## 1. 简单插件命令

**用例：**使用插件脚本的基本命令

**文件：**`commands/analyze.md`

```markdown
---
description: 使用插件工具分析代码质量
argument-hint: [file-path]
allowed-tools: Bash(node:*), Read
---

使用插件的质量检查器分析 @$1：

!`node ${CLAUDE_PLUGIN_ROOT}/scripts/quality-check.js $1`

审查分析输出并提供：
1. 发现摘要
2. 需要解决的关键问题
3. 建议的改进
4. 代码质量评分解释
```

**关键功能：**
- 使用 `${CLAUDE_PLUGIN_ROOT}` 进行可移植路径
- 结合文件引用和脚本执行
- 简单单的命令

---

## 2. 基于脚本的分析

**用例：**使用多个插件脚本运行全面分析

**文件：**`commands/full-audit.md`

```markdown
---
description: 使用插件套件进行完整代码审计
argument-hint: [directory]
allowed-tools: Bash(*)
model: sonnet
---

在 $1 上运行完整审计：

**安全扫描：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh $1`

**性能分析：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/perf-analyze.sh $1`

**最佳实践检查：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/best-practices.sh $1`

分析所有结果并创建综合报告，包括：
- 需要立即关注的关键问题
- 性能优化机会
- 安全漏洞和修复
- 整体健康评分和推荐
```

**关键功能：**
- 多个脚本执行
- 有组织的输出部分
- 全面工作流
- 清晰的报告结构

---

## 3. 基于模板的生成

**用例：**遵循插件模板生成文档

**文件：**`commands/gen-api-docs.md`

```markdown
---
description: 从模板生成 API 文档
argument-hint: [api-file]
---

模板结构：@${CLAUDE_PLUGIN_ROOT}/templates/api-documentation.md

API 实现：@$1

遵循上述模板格式生成完整的 API 文档。

确保文档包括：
- 带有 HTTP 方法的端点描述
- 请求/响应模式
- 身份验证要求
- 错误代码和处理
- 带有 curl 命令的用例
- 速率限制信息

格式化为适合 README 或文档站点的 Markdown。
```

**关键功能：**
- 使用插件模板
- 结合模板和源文件
- 标准化输出格式
- 清晰的文档结构

---

## 4. 多脚本工作流

**用例：**编排构建、测试和部署工作流

**文件：**`commands/release.md`

```markdown
---
description: 执行完整发布工作流
argument-hint: [version]
allowed-tools: Bash(*), Read
---

为版本 $1 执行发布工作流：

**步骤 1 - 发布前验证：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/pre-release-check.sh $1`

**步骤 2 - 构建工件：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build-release.sh $1`

**步骤 3 - 运行测试套件：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh`

**步骤 4 - 打包发布：**
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/package.sh $1`

审查所有步骤输出并报告：
1. 任何失败或警告
2. 构建工件位置
3. 测试结果摘要
4. 部署的下一步
5. 需要时的回滚计划
```

**关键功能：**
- 多步骤工作流
- 顺序脚本执行
- 清晰的步骤编号
- 全面报告

---

## 5. 配置驱动的部署

**用例：**使用环境特定插件配置部署

**文件：**`commands/deploy.md`

```markdown
---
description: 部署应用到环境
argument-hint: [environment]
allowed-tools: Read, Bash(*)
---

$1 的部署配置：@${CLAUDE_PLUGIN_ROOT}/config/$1-deploy.json

当前 git 状态：!`git rev-parse --short HEAD`

构建信息：!`cat package.json | grep -E '(name|version)'`

使用上述配置执行到 $1 环境的部署。

部署检查清单：
1. 验证配置设置
2. 为 $1 构建应用
3. 运行部署前测试
4. 部署到目标环境
5. 运行烟雾测试
6. 验证部署成功
7. 更新部署日志

报告部署状态和遇到的任何问题。
```

**关键功能：**
- 环境特定配置
- 动态配置文件加载
- 部署前验证
- 结构化检查清单

---

## 6. 代理集成

**用例：**为复的任务启动插件代理的命令

**文件：**`commands/deep-review.md`

```markdown
---
description: 使用插件代理进行深度代码审查
argument-hint: [file-or-directory]
---

使用 code-reviewer 代理对 @$1 启动全面代码审查。

代理将执行：
1. **静态分析** - 检查代码异味和反模式
2. **安全审计** - 识别潜在漏洞
3. **性能审查** - 查找优化机会
4. **最佳实践** - 确保代码遵循标准
5. **文档检查** - 验证充分文档

代理可以访问：
- 插件的 linting 规则：${CLAUDE_PLUGIN_ROOT}/config/lint-rules.json
- 安全检查清单：${CLAUDE_PLUGIN_ROOT}/checklists/security.md
- 性能指导：${CLAUDE_PLUGIN_ROOT}/docs/performance.md

注意：这使用 Task 工具启动插件的 code-reviewer 代理以进行彻底分析。
```

**关键功能：**
- 委托给插件代理
- 文档化代理能力
- 引用插件资源
- 清晰的范围定义

---

## 7. 技能集成

**用例：**利用插件技能获取专门知识的命令

**文件：**`commands/document-api.md`

```markdown
---
description: 遵循插件标准文档化 API
argument-hint: [api-file]
---

API 源代码：@$1

遵循插件的 API 文档标准生成 API 文档。

使用 api-documentation-standards 技能确保：
- **OpenAPI 合规性** - 遵循 OpenAPI 3.0 规范
- **一致格式** - 使用插件的文档样式
- **完整覆盖** - 文档化所有端点和模式
- **示例质量** - 提供现实的用例
- **错误文档** - 覆盖所有错误场景

该技能提供：
- 标准文档模板
- API 文档最佳实践
- 此代码库的常见模式
- 质量验证标准

生成生产就绪的 API 文档。
```

**关键功能：**
- 按名称调用插件技能
- 文档化技能目的
- 清晰的期望
- 利用技能知识

---

## 8. 多组件工作流

**用例：**使用代理、技能和脚本的复工作流

**文件：**`commands/complete-review.md`

```markdown
---
description: 使用所有插件组件进行全面审查
argument-hint: [file-path]
allowed-tools: Bash(node:*), Read
---

目标文件：@$1

执行全面审查工作流：

**阶段 1：自动分析**
运行插件分析器：!`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js $1`

**阶段 2：深度审查（代理）**
启动 code-quality-reviewer 代理进行详细分析。
代理将检查：
- 代码结构和组织
- 错误处理模式
- 测试覆盖率
- 文档质量

**阶段 3：标准检查（技能）**
使用 coding-standards 技能验证：
- 命名约定
- 代码格式
- 最佳实践遵守
- 框架特定模式

**阶段 4：报告生成**
模板：@${CLAUDE_PLUGIN_ROOT}/templates/review-report.md

按照模板将所有发现编译到综合报告中。

**阶段 5：推荐**
生成优先操作项：
1. 关键问题（必须修复）
2. 重要改进（应该修复）
3. 理想的增强（可以修复）

为每个项目包含具体的文件位置和建议更改。
```

**关键功能：**
- 多阶段工作流
- 结合脚本、代理、技能
- 基于模板的报告
- 优先级输出

---

## 9. 验证输入命令

**用例：**带有输入验证和错误处理的命令

**文件：**`commands/build-env.md`

```markdown
---
description: 为特定环境构建并带验证
argument-hint: [environment]
allowed-tools: Bash(*)
---

验证环境参数：!`echo "$1" | grep -E "^(dev|staging|prod)$" && echo "VALID" || echo "INVALID"`

检查构建脚本存在：!`test -x ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh && echo "EXISTS" || echo "MISSING`

验证配置可用：!`test -f ${CLAUDE_PLUGIN_ROOT}/config/$1.json && echo "FOUND" || echo "NOT_FOUND"`

如果所有验证通过：

**配置：**@${CLAUDE_PLUGIN_ROOT}/config/$1.json

**执行构建：**!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh $1 2>&1`

**验证结果：**!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-build.sh $1 2>&1`

报告构建状态和任何问题。

如果验证失败：
- 解释哪个验证失败
- 提供预期值/位置
- 建议纠正操作
- 文档化故障排除步骤
```

**关键功能：**
- 输入验证
- 资源存在检查
- 错误处理
- 有用的错误消息
- 优雅的失败处理

---

## 10. 环境感知命令

**用例：**根据环境适应行为的命令

**文件：**`commands/run-checks.md`

```markdown
---
description: 运行适当环境的检查
argument-hint: [environment]
allowed-tools: Bash(*), Read
---

环境：$1

加载环境配置：@${CLAUDE_PLUGIN_ROOT}/config/$1-checks.json

确定检查级别：!`echo "$1" | grep -E "^prod$" && echo "FULL" || echo "BASIC"`

**对于生产环境：**
- 完整测试套件：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test-full.sh`
- 安全扫描：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.sh`
- 性能审计：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/perf-check.sh`
- 合规检查：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/compliance.sh`

**对于非生产环境：**
- 基本测试：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test-basic.sh`
- 快速 lint：!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh`

根据环境要求分析结果：

**生产：**所有检查必须通过且零关键问题
**预发布：**无关键问题，警告可接受
**开发：**仅关注阻塞问题

报告状态并推荐继续/阻止决策。
```

**关键功能：**
- 环境感知逻辑
- 条件执行
- 不同的验证级别
- 每个环境的适当报告

---

## 常见模式摘要

### 模式：插件脚本执行
```markdown
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/script-name.js $1`
```
用于：运行插件提供的 Node.js 脚本

### 模式：插件配置加载
```markdown
@${CLAUDE_PLUGIN_ROOT}/config/config-name.json
```
用于：加载插件配置文件

### 模式：插件模板使用
```markdown
@${CLAUDE_PLUGIN_ROOT}/templates/template-name.md
```
用于：使用插件模板进行生成

### 模式：代理调用
```markdown
启动 [agent-name] 代理进行 [task description]。
```
用于：将复任务委托给插件代理

### 模式：技能引用
```markdown
使用 [skill-name] 技能确保 [requirements]。
```
用于：利用插件技能获取专门知识

### 模式：输入验证
```markdown
验证输入：!`echo "$1" | grep -E "^pattern$" && echo "OK" || echo "ERROR"`
```
用于：验证命令参数

### 模式：资源验证
```markdown
检查存在：!`test -f ${CLAUDE_PLUGIN_ROOT}/path/file && echo "YES" || echo "NO"`
```
用于：验证所需插件文件存在

---

## 开发提示

### 测试插件命令

1. **在插件安装时测试：**
   ```bash
   cd /path/to/plugin
   claude /command-name args
   ```

2. **验证 ${CLAUDE_PLUGIN_ROOT} 扩展：**
   ```bash
   # 向命令添加调试输出
   !`echo "插件根：${CLAUDE_PLUGIN_ROOT}"`
   ```

3. **在不同工作目录中测试：**
   ```bash
   cd /tmp && claude /command-name
   cd /other/project && claude /command-name
   ```

4. **验证资源可用性：**
   ```bash
   # 检查所有插件资源存在
   !`ls -la ${CLAUDE_PLUGIN_ROOT}/scripts/`
   !`ls -la ${CLAUDE_PLUGIN_ROOT}/config/`
   ```

### 需要避免的常见错误

1. **使用相对路径而不是 ${CLAUDE_PLUGIN_ROOT}：**
   ```markdown
   # 错误
   !`node ./scripts/analyze.js`

   # 正确
   !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js`
   ```

2. **忘记允许所需工具：**
   ```markdown
   # 缺少 allowed-tools
   !`bash script.sh`  # 将在没有 Bash 权限时失败

   # 正确
   ---
   allowed-tools: Bash(*)
   ---
   !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh`
   ```

3. **不验证输入：**
   ```markdown
   # 有风险 - 没有验证
   部署到 $1 环境

   # 更好 - 带有验证
   验证：!`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`
   部署到 $1 环境（如果有效）
   ```

4. **硬编码插件路径：**
   ```markdown
   # 错误 - 在不同安装上失败
   @/home/user/.claude/plugins/my-plugin/config.json

   # 正确 - 到处工作
   @${CLAUDE_PLUGIN_ROOT}/config.json
   ```

---

有关详细的插件特定功能，请参阅 `references/plugin-features-reference.md`。
有关一般命令开发，请参阅主 `SKILL.md`。
