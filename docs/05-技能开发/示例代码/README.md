# Anthropic Agent Skills 示例代码

本目录包含用于 Claude Code 技能开发的示例脚本和工具。

## 📁 文件说明

### Python 脚本

- **main.py** - 完整的 Python 脚本模板
  - 命令行参数解析
  - 文件读写处理
  - 错误处理和日志
  - 多种输出格式支持

### Bash 脚本

- **batch_process.sh** - 批量文件处理脚本
  - 批量处理目录中的文件
  - 彩色终端输出
  - 错误处理和统计

### 依赖文件

- **requirements.txt** - Python 依赖列表

## 🚀 使用方法

### Python 脚本

```bash
# 安装依赖
pip install -r requirements.txt

# 查看帮助
python main.py --help

# 基本用法
python main.py --input input.txt --output output.txt

# 指定输出格式
python main.py --input data.txt --output result.json --format json

# 详细模式
python main.py --input data.txt --output result.txt --verbose
```

### Bash 脚本

```bash
# 添加执行权限
chmod +x batch_process.sh

# 查看帮助
./batch_process.sh --help

# 基本用法
./batch_process.sh input_dir/ output_dir/

# 指定文件扩展名
./batch_process.sh -e csv input_dir/ output_dir/

# 详细模式
./batch_process.sh --verbose input_dir/ output_dir/
```

## 📝 脚本特性

### main.py 特性

- ✅ 完整的参数解析
- ✅ 输入验证
- ✅ 多种输出格式（text, json, csv）
- ✅ 彩色终端输出
- ✅ 详细的错误信息
- ✅ 版本信息
- ✅ 帮助文档

### batch_process.sh 特性

- ✅ 批量文件处理
- ✅ 进度统计
- ✅ 错误处理
- ✅ 彩色输出
- ✅ 详细模式
- ✅ 灵活的参数

## 🔧 自定义修改

### 修改 Python 脚本

1. **修改处理逻辑**：编辑 `process_content()` 函数
2. **添加新格式**：在 `--format` 参数中添加新选项
3. **修改输出**：编辑 `save_result()` 函数

### 修改 Bash 脚本

1. **修改处理逻辑**：编辑 `process_file()` 函数
2. **添加新参数**：在参数解析部分添加
3. **修改输出格式**：编辑输出部分

## 📚 集成到技能

### 在 SKILL.md 中引用

```markdown
## 使用脚本

处理单个文件：
```bash
python scripts/main.py --input file.txt --output result.txt
```

批量处理：
```bash
bash scripts/batch_process.sh input/ output/
```
```

### 目录结构

```
your-skill/
├── SKILL.md
├── scripts/
│   ├── main.py
│   ├── batch_process.sh
│   └── requirements.txt
├── references/
└── assets/
```

## 🧪 测试

### 测试 Python 脚本

```bash
# 创建测试文件
echo "hello world" > test_input.txt

# 运行脚本
python main.py --input test_input.txt --output test_output.txt

# 检查输出
cat test_output.txt
# 应该输出: HELLO WORLD
```

### 测试 Bash 脚本

```bash
# 创建测试目录和文件
mkdir -p test_input
echo "test content" > test_input/file1.txt
echo "more content" > test_input/file2.txt

# 运行脚本
./batch_process.sh test_input/ test_output/

# 检查输出
ls test_output/
cat test_output/file1.txt
```

## 💡 最佳实践

1. **错误处理** - 始终验证输入并提供清晰的错误信息
2. **日志输出** - 使用彩色输出提高可读性
3. **参数验证** - 检查所有必需参数
4. **文档完整** - 提供详细的帮助信息
5. **代码注释** - 为关键函数添加文档字符串

## 🔗 相关资源

- [Python argparse 文档](https://docs.python.org/3/library/argparse.html)
- [Bash 脚本指南](https://www.gnu.org/software/bash/manual/)
- [Claude Code 技能文档](../anthropic-agent-skills-完整指南.md)

## 📄 许可证

MIT License - 可自由使用和修改
