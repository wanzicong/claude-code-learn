# CLAUDE.md 模板

## 关键原则

- **简洁**：密集、可读的内容；可能的话每行一个概念
- **可执行**：命令应该可以复制粘贴
- **项目特定**：记录此项目特有的模式，而非通用建议
- **最新**：所有信息应反映实际代码库状态

---

## 推荐部分

仅使用与项目相关的部分。并非所有部分都是必需的。

### 命令

记录使用项目的基本命令。

```markdown
## 命令

| 命令 | 描述 |
|---------|-------------|
| `<install command>` | 安装依赖 |
| `<dev command>` | 启动开发服务器 |
| `<build command>` | 生产构建 |
| `<test command>` | 运行测试 |
| `<lint command>` | Lint/格式化代码 |
```

### 架构

描述项目结构，以便 Claude 理解各部分的位置。

```markdown
## 架构

```
<root>/
  <dir>/    # <purpose>
  <dir>/    # <purpose>
  <dir>/    # <purpose>
```
```

### 关键文件

列出 Claude 应该知道的重要文件。

```markdown
## 关键文件

- `<path>` - <purpose>
- `<path>` - <purpose>
```

### 代码风格

记录项目特定的编码约定。

```markdown
## 代码风格

- <convention>
- <convention>
- <preference over alternative>
```

### 环境

记录所需的环境变量和设置。

```markdown
## 环境

必需：
- `<VAR_NAME>` - <purpose>
- `<VAR_NAME>` - <purpose>

设置：
- <setup step>
```

### 测试

记录测试方法和命令。

```markdown
## 测试

- `<test command>` - <what it tests>
- <testing convention or pattern>
```

### 注意事项

记录非显而易见的模式、特殊之处和警告。

```markdown
## 注意事项

- <non-obvious thing that causes issues>
- <ordering dependency or prerequisite>
- <common mistake to avoid>
```

### 工作流程

记录开发工作流程模式。

```markdown
## 工作流程

- <when to do X>
- <preferred approach for Y>
```

---

## 模板：项目根目录（最小版）

```markdown
# <Project Name>

<One-line description>

## 命令

| 命令 | 描述 |
|---------|-------------|
| `<command>` | <description> |

## 架构

```
<structure>
```

## 注意事项

- <gotcha>
```

---

## 模板：项目根目录（完整版）

```markdown
# <Project Name>

<One-line description>

## 命令

| 命令 | 描述 |
|---------|-------------|
| `<command>` | <description> |

## 架构

```
<structure with descriptions>
```

## 关键文件

- `<path>` - <purpose>

## 代码风格

- <convention>

## 环境

- `<VAR>` - <purpose>

## 测试

- `<command>` - <scope>

## 注意事项

- <gotcha>
```

---

## 模板：包/模块

用于 monorepo 中的包或独立模块。

```markdown
# <Package Name>

<此包的目的>

## 使用方法

```
<import/usage example>
```

## 关键导出

- `<export>` - <purpose>

## 依赖

- `<dependency>` - <why needed>

## 备注

- <important note>
```

---

## 模板：Monorepo 根目录

```markdown
# <Monorepo Name>

<Description>

## 包

| 包 | 描述 | 路径 |
|---------|-------------|------|
| `<name>` | <purpose> | `<path>` |

## 命令

| 命令 | 描述 |
|---------|-------------|
| `<command>` | <description> |

## 跨包模式

- <shared pattern>
- <generation/sync pattern>
```

---

## 更新原则

更新任何 CLAUDE.md 时：

1. **具体**：使用实际的文件路径、来自此项目的真实命令
2. **最新**：根据实际代码库验证信息
3. **简洁**：可能的话每行一个概念
4. **有用**：这会帮助新的 Claude 会话理解项目吗？
