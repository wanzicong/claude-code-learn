# Hook 开发实用脚本

这些脚本有助于在部署之前验证、测试和检查 hook 实现。

## validate-hook-schema.sh

验证 `hooks.json` 配置文件的结构和常见问题。

**用法：**
```bash
./validate-hook-schema.sh path/to/hooks.json
```

**检查：**
- 有效的 JSON 语法
- 存在必需字段
- 有效的 hook 事件名称
- 正确的 hook 类型（command/prompt）
- 有效的超时值范围
- 硬编码路径检测
- Prompt hook 事件兼容性

**示例：**
```bash
cd my-plugin
./validate-hook-schema.sh hooks/hooks.json
```

## test-hook.sh

在部署到 Claude Code 之前，使用示例输入测试单个 hook 脚本。

**用法：**
```bash
./test-hook.sh [options] <hook-script> <test-input.json>
```

**选项：**
- `-v, --verbose` - 显示详细执行信息
- `-t, --timeout N` - 设置超时时间（秒）（默认：60）
- `--create-sample <event-type>` - 生成示例测试输入

**示例：**
```bash
# 创建示例测试输入
./test-hook.sh --create-sample PreToolUse > test-input.json

# 测试 hook 脚本
./test-hook.sh my-hook.sh test-input.json

# 使用详细输出和自定义超时进行测试
./test-hook.sh -v -t 30 my-hook.sh test-input.json
```

**功能：**
- 设置正确的环境变量（CLAUDE_PROJECT_DIR、CLAUDE_PLUGIN_ROOT）
- 测量执行时间
- 验证输出 JSON
- 显示退出码及其含义
- 捕获环境文件输出

## hook-linter.sh

检查 hook 脚本是否存在常见问题和最佳实践违规。

**用法：**
```bash
./hook-linter.sh <hook-script.sh> [hook-script2.sh ... ...]
```

**检查：**
- Shebang 存在性
- `set -euo pipefail` 使用情况
- Stdin 输入读取
- 正确的错误处理
- 变量引用（注入预防）
- 退出码使用情况
- 硬编码路径
- 长时间运行的代码检测
- 错误输出到 stderr
- 输入验证

**示例：**
```bash
# 检查单个脚本
./hook-linter.sh ../examples/validate-write.sh

# 检查多个脚本
./hook-linter.sh ../examples/*.sh
```

## 典型工作流程

1. **编写你的 hook 脚本**
   ```bash
   vim my-plugin/scripts/my-hook.sh
   ```

2. **检查脚本**
   ```bash
   ./hook-linter.sh my-plugin/scripts/my-hook.sh
   ```

3. **创建测试输入**
   ```bash
   ./test-hook.sh --create-sample PreToolUse > test-input.json
   # 根据需要编辑 test-input.json
   ```

4. **测试 hook**
   ```bash
   ./test-hook.sh -v my-plugin/scripts/my-hook.sh test-input.json
   ```

5. **添加到 hooks.json**
   ```bash
   # 编辑 my-plugin/hooks/hooks.json
   ```

6. **验证配置**
   ```bash
   ./validate-hook-schema.sh my-plugin/hooks/hooks.json
   ```

7. **在 Claude Code 中测试**
   ```bash
   claude --debug
   ```

## 提示

- 始终在部署之前测试 hook，以避免破坏用户工作流程
- 使用详细模式（`-v`）来调试 hook 行为
- 检查检查器输出以获取安全和最佳实践问题
- 在任何更改后验证 hooks.json
- 为各种场景创建不同的测试输入（安全操作、危险操作、边缘情况）

## 常见问题

### Hook 不执行

检查：
- 脚本具有 shebang（`#!/bin/bash`）
- 脚本是可执行的（`chmod +x`）
- hooks.json 中的路径正确（使用 `${CLAUDE_PLUGIN_ROOT}`）

### Hook 超时

- 在 hooks.json 中减少超时
- 优化 hook 脚本性能
- 删除长时间运行的操作

### Hook 静默失败

- 检查退出码（应该为 0 或 2）
- 确保错误转到 stderr（`>&2`）
- 验证 JSON 输出结构

### 注入漏洞

- 始终引用变量：`"$variable"`
- 使用 `set -euo pipefail`
- 验证所有输入字段
- 运行检查器以捕获问题
