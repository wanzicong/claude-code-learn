# 设置文件解析技术

在 bash 脚本中解析 `.claude/plugin-name.local.md` 文件的完整指南。

## 文件结构

设置文件使用带 YAML frontmatter 的 markdown:

```markdown
---
field1: value1
field2: "value with spaces"
numeric_field: 42
boolean_field: true
list_field: ["item1", "item2", "item3"]
---

# Markdown 内容

此主体内容可以单独提取。
它对提示、文档或附加上下文很有用。
```

## 解析 Frontmatter

### 提取 Frontmatter 块

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# 提取 --- 标记之间的所有内容（不包括标记本身）
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

**工作原理:**
- `sed -n` - 抑制自动打印
- `/^---$/,/^---$/` - 从第一个 `---` 到第二个 `---` 的范围
- `{ /^---$/d; p; }` - 删除 `---` 行，打印其他所有内容

### 提取单个字段

**字符串字段:**
```bash
# 简单值
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//')

# 带引号的值（删除周围的引号）
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**Boolean fields:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# 在条件中使用
if [[ "$ENABLED" == "true" ]]; then
  # 已启用
fi
```

**Numeric fields:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# 验证它是一个数字
if [[ "$MAX" =~ ^[0-9]+$ ]]; then
  # 在数字比较中使用
  if [[ $MAX -gt 100 ]]; then
    # 太大
  fi
fi
```

**List fields (simple):**
```bash
# YAML: list: ["item1", "item2", "item3"]
LIST=$(echo "$FRONTMATTER" | grep '^list:' | sed 's/list: *//')
# 结果: ["item1", "item2", "item3"]

# 用于简单检查:
if [[ "$LIST" == *"item1"* ]]; then
  # 列表包含 item1
fi
```

**List fields (proper parsing with jq):**
```bash
# 对于正确的列表处理，使用 yq 或转换为 JSON
# 这需要安装 yq (brew install yq)

# 提取列表为 JSON 数组
LIST=$(echo "$FRONTMATTER" | yq -o json '.list' 2>/dev/null)

# 迭代项目
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "处理: $item"
done
```

## 解析 Markdown 主体

### 提取主体内容

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"

# 提取关闭 --- 之后的所有内容
# 计数 --- 标记：第一个是开头，第二个是结尾，之后的都是主体
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

**工作原理:**
- `/^---$/` - 匹配 `---` 行
- `{i++; next}` - 增加计数器并跳过 `---` 行
- `i>=2` - 打印第二个 `---` 之后的所有行

**处理边缘情况:** 如果 `---` 出现在 markdown 主体中，它仍然有效，因为我们只计算开头的前两个 `---`。

### 使用主体作为提示

```bash
# Extract body
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$RALPH_STATE_FILE")

# Feed back to Claude
echo '{"decision": "block", "reason": "'"$PROMPT"'"}' | jq .
```

**Important:** Use `jq -n --arg` for safer JSON construction with user content:

```bash
PROMPT=$(awk '/^---$/{i++; next} i>=2' "$FILE")

# Safe JSON construction
jq -n --arg prompt "$PROMPT" '{
  "decision": "block",
  "reason": $prompt
}'
```

## Common Parsing Patterns

### Pattern: Field with Default

```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')

# Use default if empty
if [[ -z "$VALUE" ]]; then
  VALUE="default_value"
fi
```

### Pattern: Optional Field

```bash
OPTIONAL=$(echo "$FRONTMATTER" | grep '^optional_field:' | sed 's/optional_field: *//' | sed 's/^"\(.*\)"$/\1/')

# Only use if present
if [[ -n "$OPTIONAL" ]] && [[ "$OPTIONAL" != "null" ]]; then
  # Field is set, use it
  echo "Optional field: $OPTIONAL"
fi
```

### Pattern: Multiple Fields at Once

```bash
# Parse all fields in one pass
while IFS=': ' read -r key value; do
  # Remove quotes if present
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

## Updating Settings Files

### Atomic Updates

Always use temp file + atomic move to prevent corruption:

```bash
#!/bin/bash
FILE=".claude/my-plugin.local.md"
NEW_VALUE="updated_value"

# Create temp file
TEMP_FILE="${FILE}.tmp.$$"

# Update field using sed
sed "s/^field_name: .*/field_name: $NEW_VALUE/" "$FILE" > "$TEMP_FILE"

# Atomic replace
mv "$TEMP_FILE" "$FILE"
```

### Update Single Field

```bash
# Increment iteration counter
CURRENT=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
NEXT=$((CURRENT + 1))

# Update file
TEMP_FILE="${FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT/" "$FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILE"
```

### Update Multiple Fields

```bash
# Update several fields at once
TEMP_FILE="${FILE}.tmp.$$"

sed -e "s/^iteration: .*/iteration: $NEXT_ITERATION/" \
    -e "s/^pr_number: .*/pr_number: $PR_NUMBER/" \
    -e "s/^status: .*/status: $NEW_STATUS/" \
    "$FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$FILE"
```

## Validation Techniques

### Validate File Exists and Is Readable

```bash
FILE=".claude/my-plugin.local.md"

if [[ ! -f "$FILE" ]]; then
  echo "Settings file not found" >&2
  exit 1
fi

if [[ ! -r "$FILE" ]]; then
  echo "Settings file not readable" >&2
  exit 1
fi
```

### Validate Frontmatter Structure

```bash
# Count --- markers (should be exactly 2 at start)
MARKER_COUNT=$(grep -c '^---$' "$FILE" 2>/dev/null || echo "0")

if [[ $MARKER_COUNT -lt 2 ]]; then
  echo "Invalid settings file: missing frontmatter markers" >&2
  exit 1
fi
```

### Validate Field Values

```bash
MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//')

case "$MODE" in
  strict|standard|lenient)
    # Valid mode
    ;;
  *)
    echo "Invalid mode: $MODE (must be strict, standard, or lenient)" >&2
    exit 1
    ;;
esac
```

### Validate Numeric Ranges

```bash
MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')

if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
  echo "max_size must be a number" >&2
  exit 1
fi

if [[ $MAX_SIZE -lt 1 ]] || [[ $MAX_SIZE -gt 10000000 ]]; then
  echo "max_size out of range (1-10000000)" >&2
  exit 1
fi
```

## Edge Cases and Gotchas

### Quotes in Values

YAML allows both quoted and unquoted strings:

```yaml
# These are equivalent:
field1: value
field2: "value"
field3: 'value'
```

**Handle both:**
```bash
# Remove surrounding quotes if present
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\\(.*\\)'$/\\1/")
```

### --- in Markdown Body

If the markdown body contains `---`, the parsing still works because we only match the first two:

```markdown
---
field: value
---

# Body

Here's a separator:
---

More content after the separator.
```

The `awk '/^---$/{i++; next} i>=2'` pattern handles this correctly.

### Empty Values

Handle missing or empty fields:

```yaml
field1:
field2: ""
field3: null
```

**Parsing:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
# VALUE will be empty string

# Check for empty/null
if [[ -z "$VALUE" ]] || [[ "$VALUE" == "null" ]]; then
  VALUE="default"
fi
```

### Special Characters

Values with special characters need careful handling:

```yaml
message: "Error: Something went wrong!"
path: "/path/with spaces/file.txt"
regex: "^[a-zA-Z0-9_]+$"
```

**Safe parsing:**
```bash
# Always quote variables when using
MESSAGE=$(echo "$FRONTMATTER" | grep '^message:' | sed 's/message: *//' | sed 's/^"\(.*\)"$/\1/')

echo "Message: $MESSAGE"  # Quoted!
```

## Performance Optimization

### Cache Parsed Values

If reading settings multiple times:

```bash
# Parse once
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Extract multiple fields from cached frontmatter
FIELD1=$(echo "$FRONTMATTER" | grep '^field1:' | sed 's/field1: *//')
FIELD2=$(echo "$FRONTMATTER" | grep '^field2:' | sed 's/field2: *//')
FIELD3=$(echo "$FRONTMATTER" | grep '^field3:' | sed 's/field3: *//')
```

**Don't:** Re-parse file for each field.

### Lazy Loading

Only parse settings when needed:

```bash
#!/bin/bash
input=$(cat)

# Quick checks first (no file I/O)
tool_name=$(echo "$input" | jq -r '.tool_name')
if [[ "$tool_name" != "Write" ]]; then
  exit 0  # Not a write operation, skip
fi

# Only now check settings file
if [[ -f ".claude/my-plugin.local.md" ]]; then
  # Parse settings
  # ...
fi
```

## Debugging

### Print Parsed Values

```bash
#!/bin/bash
set -x  # Enable debug tracing

FILE=".claude/my-plugin.local.md"

if [[ -f "$FILE" ]]; then
  echo "Settings file found" >&2

  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
  echo "Frontmatter:" >&2
  echo "$FRONTMATTER" >&2

  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  echo "Enabled: $ENABLED" >&2
fi
```

### Validate Parsing

```bash
# Show what was parsed
echo "Parsed values:" >&2
echo "  enabled: $ENABLED" >&2
echo "  mode: $MODE" >&2
echo "  max_size: $MAX_SIZE" >&2

# Verify expected values
if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
  echo "⚠️  Unexpected enabled value: $ENABLED" >&2
fi
```

## Alternative: Using yq

For complex YAML, consider using `yq`:

```bash
# Install: brew install yq

# Parse YAML properly
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Extract fields with yq
ENABLED=$(echo "$FRONTMATTER" | yq '.enabled')
MODE=$(echo "$FRONTMATTER" | yq '.mode')
LIST=$(echo "$FRONTMATTER" | yq -o json '.list_field')

# Iterate list properly
echo "$LIST" | jq -r '.[]' | while read -r item; do
  echo "Item: $item"
done
```

**Pros:**
- Proper YAML parsing
- Handles complex structures
- Better list/object support

**Cons:**
- Requires yq installation
- Additional dependency
- May not be available on all systems

**Recommendation:** Use sed/grep for simple fields, yq for complex structures.

## Complete Example

```bash
#!/bin/bash
set -euo pipefail

# Configuration
SETTINGS_FILE=".claude/my-plugin.local.md"

# Quick exit if not configured
if [[ ! -f "$SETTINGS_FILE" ]]; then
  # Use defaults
  ENABLED=true
  MODE=standard
  MAX_SIZE=1000000
else
  # Parse frontmatter
  FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SETTINGS_FILE")

  # Extract fields with defaults
  ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
  ENABLED=${ENABLED:-true}

  MODE=$(echo "$FRONTMATTER" | grep '^mode:' | sed 's/mode: *//' | sed 's/^"\(.*\)"$/\1/')
  MODE=${MODE:-standard}

  MAX_SIZE=$(echo "$FRONTMATTER" | grep '^max_size:' | sed 's/max_size: *//')
  MAX_SIZE=${MAX_SIZE:-1000000}

  # Validate values
  if [[ "$ENABLED" != "true" ]] && [[ "$ENABLED" != "false" ]]; then
    echo "⚠️  Invalid enabled value, using default" >&2
    ENABLED=true
  fi

  if ! [[ "$MAX_SIZE" =~ ^[0-9]+$ ]]; then
    echo "⚠️  Invalid max_size, using default" >&2
    MAX_SIZE=1000000
  fi
fi

# Quick exit if disabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# Use configuration
echo "Configuration loaded: mode=$MODE, max_size=$MAX_SIZE" >&2

# Apply logic based on settings
case "$MODE" in
  strict)
    # Strict validation
    ;;
  standard)
    # Standard validation
    ;;
  lenient)
    # Lenient validation
    ;;
esac
```

This provides robust settings handling with defaults, validation, and error recovery.
