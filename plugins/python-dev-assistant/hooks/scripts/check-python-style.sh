#!/bin/bash
# Python 代码风格检查脚本
# 在保存 Python 文件前运行

set -euo pipefail

# 读取输入
input=$(cat)

# 提取文件路径
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# 如果没有文件路径，允许操作
if [ -z "$file_path" ]; then
  echo '{"continue": true}'
  exit 0
fi

# 检查是否是 Python 文件
if [[ ! "$file_path" =~ \.py$ ]]; then
  echo '{"continue": true}'
  exit 0
fi

# 检查配置是否启用钩子
config_file="$CLAUDE_PROJECT_DIR/.claude/python-dev-assistant.local.md"
enable_hook=true

if [ -f "$config_file" ]; then
  # 读取 enable_hook 配置
  enabled=$(grep -E "^enable_hook:" "$config_file" | awk '{print $2}' || echo "true")
  if [ "$enabled" = "false" ]; then
    echo '{"continue": true}'
    exit 0
  fi
fi

# 检查 ruff 是否安装
if ! command -v ruff &> /dev/null; then
  echo '{"continue": true, "systemMessage": "提示: 安装 ruff 以启用自动代码检查: pip install ruff"}'
  exit 0
fi

# 运行 ruff 检查
output=$(ruff check "$file_path" 2>&1 || true)

# 如果有问题，显示警告但允许保存
if [ -n "$output" ]; then
  message="⚠ 代码风格检查发现问题:\n\n$output\n\n建议: 运行 /py-check --fix 自动修复"
  echo "{\"continue\": true, \"systemMessage\": \"$message\"}"
else
  echo '{"continue": true, "systemMessage": "✓ 代码风格检查通过"}'
fi

exit 0
