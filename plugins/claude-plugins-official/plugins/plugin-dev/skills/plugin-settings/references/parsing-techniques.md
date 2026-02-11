# 设置文件解析技术

在 bash 脚本中解析 `.claude/plugin-name.local.md` 文件的完整指南。

## 文件结构

设置文件使用带有 YAML frontmatter 的 markdown：

```markdown
---
field1: value1
field2: "value with spaces"
numeric_field: 42
boolean_field: true
list_field: ["item1", "item2", "item3"]
---

# Markdown 内容

此正文内容可以单独提取。
适用于提示、文档或附加上下文。
```

## 解析 Frontmatter

### 提取 Frontmatter 块

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# 提取 --- 标记之间的所有内容（排除标记本身）
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

**工作原理：**
- `sed -n` - 禁止自动打印
- `/^---$/,/^---$/` - 从第一个 `---` 到第二个 `---` 的范围
- `{ /^---$/d; p; }` - 删除 `---` 行，打印其他所有内容

### 提取各个字段

**字符串字段：**
```bash
# 简单值
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//')

# 带引号的值（去除周围引号）
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**布尔字段：**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# 在条件中使用
if [[ "$ENABLED" == "true" ]]; then
  # 已启用
fi
```

**数字字段：**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# 验证它是一个数字
if [[ "$MAX" =~ ^[0-9]+$ ]]; then
  # 在数字比较中使用
  if [[ $MAX -gt 100 ]]; then
    # 过大
  fi
fi
```

**列表字段（简单）：**
```bash
# YAML: list: ["item1", "item2", "item3"]
LIST=$(echo "$FRONTMATTER" | grep '^list:' | sed 's/list: *//')
# 结果: ["item1", "item2", "item3"]

# 简单检看：
if [[ "$LIST" == *"item1"* ]]; then
  # 列表包含 item1
fi
```

**列表字段（使用 jq 进行正确解析）：**
```bash
# 对于正确的列表处理，使用 yq 或转换为 JSON
# 这需要安装 yq（brew install yq）

# 将列表提取为 JSON 数组
LIST=$(echo "$FRONTMATTER" | yq -o json '.list' 2>/dev/null)

# 迭代项目
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "处理：$item"
done
```

## 解析 Markdown 正文

### 提取正文内容

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# 提取结束 --- 之后的所有内容
# 计算 --- 标记：第一个是开始，第二个是结束，之后的所有是正文
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

**工作原理：**
- `/^---$/` - 匹配 `---` 行
- `{i++; next}` - 增加计数器并跳过 `---` 行
- `i>=2` - 打印第二个 `---` 之后的所有行

**处理边界情况：** 如果 markdown 正文包含 `---`，仍然有效，因为我们只匹配开头的两个 `---`

### 将正文作为提示使用

```bash
# 提取正文
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# 反馈给 Claude
echo '{"decision": "block", "reason": "'"$PROMPT"'"}' | jq .
```

**重要：** 使用 `jq -n --arg` 对带有用户内容进行更安全的 JSON 构建：

```bash
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$FILE")

# 安全的 JSON 构建
jq -n --arg prompt "$PROMPT" '{
  "decision": "block",
  "reason": $prompt
}'
```

## 常见解析模式

### 模式：带默认值的字段

```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')

# 如果为非则使用默认值
if [[ -z "$VALUE" ]]; then
  VALUE="default_value"
fi
```

### 模式：可选字段

```bash
OPTIONAL=$(echo "$FRONTMATTER" | grep '^optional_field:' | sed 's/optional_field: *//' | sed 's/^"\(.*\)"$/\1/')

# 仅在存在时使用
if [[ -n "$OPTIONAL" ]] && [[ "$OPTIONAL" != "null" ]]; then
  # 字段已设置，使用它
  echo "可选字段：$OPTIONAL"
fi
```

### 模式：一次性读取多个字段

```bash
# 在一次传递中解析所有字段
while IFS=': ' read -r key value; do
  # 如果存在则去除引号
  value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/')

  case "$key" in
    enabled)
      ENABLED="$value"
      ;;
    mode)
      MODE="$value"
      ;;
    max_size)
      MAX_SIZE="$value"
      ;;
  esac
done <<< "$FRONTMATTER"
```

## 更新设置文件

### 原子更新

始终使用临时文件 + 原子移动以防止损坏：

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"
NEW_VALUE="updated_value"

# 创建临时文件
TEMP_FILE="${FILE}.tmp.$$"

# 使用 sed 更新字段
sed "s/^field_name: .*/field_name: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"

# 原子替换
mv "$TEMP_FILE" "$FILE"
```

### 更新单个字段

```bash
# 增加迭代计数器
CURRENT=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
NEXT=$((CURRENT + 1))

# 更新文件
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### 更新多个字段

```bash
# 一次性更新多个字段
TEMP_FILE="${FILE}.tmp.$$"

sed -e "s/^iteration: .*/iteration: $NEXT_ITERATION/" \
    -e "s/^pr_number: .*/pr_number: $PR_NUMBER/" \
    -e "s/^status: .*/status: $NEW_STATUS/" \
    "$FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$FILE"
```

## 验证技术

### 验证文件存在且可读

```bash
FILE=".claude/my-plugin.local.md"

if [[ ! -f "$FILE" ]]; then
  echo "未找到设置文件" >&2
  exit 1
fi

if [[ ! -r "$FILE" ]]; then
  echo "设置文件不可读" >&2
  exit 1
fi
```

### 验证 Frontmatter 结构

```bash
# 计算开头的 --- 标记（应该正好 2 个）
MARKER_COUNT=$(grep -c '^---$' "$FILE" 2>/dev/null || echo "0")

if [[ $MARKER_COUNT -lt 2 ]]; then
  echo "无效的设置文件：缺少 frontmatter 标记" >&2
  exit 1
fi
```

### 验证字段值

```bash
MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//')

case "$MODE" in
  strict|standard|lenient)
    # 有效模式
    ;;
  *)
    echo "无效模式：$MODE（必须为 strict、standard 或 lenient）" >&2
    exit 1
    ;;
esac
```

### 验证数字范围

```bash
MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')

if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
  echo "max_size 必须为数字" >&2
  exit 1
fi

if [[ $MAX_SIZE -lt 1 ]] || [[ $MAX_SIZE -gt 10000000 ]]; then
  echo "max_size 超出范围（1-10000000）" >&2
  exit 1
fi
```

## 边界情况和注意事项

### 值中的引号

YAML 允许带引号和不带引号的字符串：

```yaml
# 这些是等效的：
field1: value
field2: "value"
field3: 'value'
```

**处理两者：**
```bash
# 如果存在则去除周围引号
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/'/' | sed "s/^'\\(.*\\)'$/\\1/")
```

### Markdown 正文中的 ---

如果 markdown 正文包含 `---`，解析仍然有效，因为我们只匹配开头的两个：

```markdown
---
field: value
---

# 正文

这里有一个分隔线：
---

分隔线之后有更多内容。
```

`awk '/^---$/{i++; next} i>=2'` 模式正确处理此情况。

### 空值

处理缺失或空的字段：

```yaml
field1:
field2: ""
field3: null
```

**解析：**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
# VALUE 将为空字符串

# 检查空/null
if [[ -z "$VALUE" ]] || [[ "$VALUE" == "null" ]]; then
  VALUE="default"
fi
```

### 特殊字符

包含特殊字符的值需要小心处理：

```yaml
message: "错误：：出现问题！"
path: "/path/with spaces/file.txt"
regex: "^[a-zA-Z0-9_]+$"
```

**安全解析：**
```bash
# 使用时始终引用变量
MESSAGE=$(echo "$FRONTMATTER" | grep '^message:' | sed 's/message: *//' | sed 's/^"\(.*\)"$/\1/')

echo "消息：$MESSAGE"  # 已引用！
```

## 性能优化

### 缓存解析的值

如果多次读取设置：

```bash
# 解析一次
FRONTMATTER=$(sed -n '/^---$/,/^---`{ /^---$/d; p; }' "$FILE")

# 从缓存的 frontmatter 提取多个字段
FIELD1=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
FIELD2=$(echo "$FRONTMATTER" | grep '^field2:' | sed 's/field2: *//')
FIELD3=$(echo "$FRONTMATTER" | grep '^field3:' | sed 's/field3: *//')
```

**不要：** 为每个字段重新解析文件。

### 延迟加载

仅在需要时解析设置：

```bash
#!/bin/bash
input=$(cat)

# 首先进行快速检看（无文件 I/O）
tool_name=$(echo "$input" | jq -r '.tool_name')
if [[ "$tool_name" != "Write" ]]; then
  exit 0  # 不是写入操作，跳过
fi

# 只有现在检看设置文件
if [[ -f ".claude/my-plugin.local.md"` ]]; then
  # 解析设置
  # ...
fi
```

## 调试

### 打印解析的值

```bash
#!/bin/bash
set -x  # 启用调试跟踪

FILE=".claude/my-plugin.local.md"

if [[ -f "$FILE" ]]; then
  echo "找到设置文件" >&2

  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
  echo "Frontmatter：" >&2
  echo "$FRONTMATTER" >&2

  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  echo "Enabled：$ENABLED" >&2
fi
```

### 验证解析

```bash
# 显示解析的内容
echo "解析的值：" >&2
echo "  enabled：$ENABLED" >&2
echo "  mode：$MODE" >&2
echo "  max_size：$MAX_SIZE" >&2

# 验证预期值
if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
  echo "⚠  意外的 enabled 值：$ENABLED" >&2
fi
```

## 替代方案：使用 yq

对于复杂 YAML，考虑使用 `yq`：

```bash
# 安装：brew install yq

# 正确解析 YAML
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# 使用 yq 提取字段
ENABLED=$(echo "$FRONTMATTER" | yq '.enabled')
MODE=$(echo "$FRONTMATTER" | yq '.mode')
LIST=$(echo "$FRONTMATTER" | yq -o json '.list_field')

# 正确地迭代列表
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "项：$item"
done
```

**优点：**
- 正确的 YAML 解析
- 处理复杂结构
- 更好的列表/对象支持

**缺点：**
- 需要 yq 安装
- 额外依赖
- 可能并非在所有系统上可用

**建议：** 对简单字段使用 sed/grep，对复杂结构使用 yq。

## 完整示例

```bash
#!/bin/bash
set -euo pipefail

# 配置
SETTINGS_FILE=".claude/my-plugin.local.md"

# 如果未配置则快速退出
if [[ ! -f "$SETTINGS_FILE" ]]; then
  # 使用默认值
  ENABLED=true
  MODE=standard
  MAX_SIZE=1000000
else
  # 解析 frontmatter
  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SETTINGS_FILE")

  # 提取带默认值的字段
  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  ENABLED=${ENABLED:-true}

  MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//' | sed 's/^"\(.*\)"$/\1/')
  MODE=${MODE:-standard}

  MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')
  MAX_SIZE=${MAX_SIZE:-1000000}

  # 验证值
  if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
    echo "⚠  无效的 enabled 值，使用默认值" >&2
    ENABLED=true
  fi

  if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
    echo "⚠  无效的 max_size，使用默认值" >&2
    MAX_SIZE=1000000
  fi
fi

# 如果已禁用则快速退出
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# 使用配置
echo "配置已加载：mode=$MODE，max_size=$MAX_SIZE" >&2

# 根据设置应用逻辑
case "$MODE" in
  strict)
    # 严格验证
    ;;
  standard)
    # 标准验证
    ;;
  lenient)
    # 宽松验证
    ;;
esac
```

这提供了带有默认值、验证和错误恢复的稳健设置处理。
