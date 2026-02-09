---
name: Python 最佳实践与代码风格指南
description: This skill should be used when the user asks about "Python 代码规范", "PEP 8", "Python 最佳实践", "如何写好 Python 代码", "Python 代码风格", "代码质量检查工具", or mentions tools like "black", "ruff", "pylint", "flake8". Provides comprehensive guidance on Python coding standards and best practices.
version: 0.1.0
---

# Python 最佳实践与代码风格指南

## 概述

本技能提供 Python 代码规范、最佳实践和代码质量工具的完整指南。帮助开发者编写清晰、可维护、符合社区标准的 Python 代码。

## 核心原则

### PEP 8 代码风格

PEP 8 是 Python 官方代码风格指南，定义了代码格式化的标准。

**关键规则：**

1. **缩进**：使用 4 个空格，不使用 Tab
2. **行长度**：每行最多 79 字符（文档字符串/注释 72 字符）
3. **空行**：
   - 顶层函数和类定义之间空 2 行
   - 类内方法定义之间空 1 行
4. **导入**：
   - 每个导入独立一行
   - 按标准库、第三方库、本地模块分组
   - 每组之间空一行

**示例：**
```python
# 标准库
import os
import sys

# 第三方库
import requests
from django.db import models

# 本地模块
from .utils import helper_function
```

### 命名规范

**遵循以下命名约定：**

- **模块名**：`lowercase_with_underscores.py`
- **类名**：`CapitalizedWords`（驼峰命名）
- **函数名**：`lowercase_with_underscores`
- **常量**：`UPPERCASE_WITH_UNDERSCORES`
- **私有属性**：`_leading_underscore`
- **特殊方法**：`__double_leading_and_trailing_underscore__`

**示例：**
```python
# 常量
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# 类
class UserManager:
    def __init__(self):
        self._cache = {}  # 私有属性

    def get_user(self, user_id):  # 公共方法
        return self._fetch_from_cache(user_id)

    def _fetch_from_cache(self, key):  # 私有方法
        return self._cache.get(key)
```

### 代码组织

**模块结构顺序：**

1. Shebang 行（如果需要）
2. 模块文档字符串
3. 导入语句
4. 模块级常量
5. 模块级函数
6. 类定义
7. 主程序入口（if __name__ == '__main__'）

**示例：**
```python
#!/usr/bin/env python3
"""
用户管理模块

提供用户创建、查询、更新和删除功能。
"""

import logging
from typing import Optional

# 常量
DEFAULT_ROLE = 'user'
ADMIN_ROLE = 'admin'

# 函数
def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    return '@' in email

# 类
class User:
    """用户类"""
    pass

# 主程序
if __name__ == '__main__':
    pass
```

## 代码质量工具

### Ruff（推荐）

最快的 Python 代码检查器和格式化工具，用 Rust 编写。

**安装：**
```bash
pip install ruff
```

**使用：**
```bash
# 检查代码
ruff check .

# 自动修复
ruff check --fix .

# 格式化代码
ruff format .
```

**配置文件 `pyproject.toml`：**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # 忽略行长度检查
```

**优势：**
- 速度极快（比 pylint 快 10-100 倍）
- 集成多种工具功能（flake8, isort, pyupgrade 等）
- 自动修复大部分问题
- 配置简单

### Black

严格的代码格式化工具，"无妥协"的风格。

**安装：**
```bash
pip install black
```

**使用：**
```bash
# 格式化文件
black file.py

# 格式化目录
black .

# 检查但不修改
black --check .
```

**特点：**
- 行长度默认 88 字符
- 自动处理字符串引号
- 统一的代码风格
- 无需配置

### Pylint

全面的静态代码分析工具。

**安装：**
```bash
pip install pylint
```

**使用：**
```bash
# 检查文件
pylint file.py

# 检查目录
pylint src/

# 生成配置文件
pylint --generate-rcfile > .pylintrc
```

**检查内容：**
- 代码风格
- 代码复杂度
- 潜在错误
- 代码异味
- 重复代码

**评分系统：**
- 0-10 分评分
- 提供详细的改进建议

### Flake8

轻量级代码风格检查工具。

**安装：**
```bash
pip install flake8
```

**使用：**
```bash
# 检查代码
flake8 .

# 指定配置
flake8 --max-line-length=88 .
```

**配置文件 `.flake8`：**
```ini
[flake8]
max-line-length = 88
exclude = .git,__pycache__,venv
ignore = E203,W503
```

## 最佳实践

### 1. 使用类型提示

从 Python 3.5+ 开始支持类型提示，提高代码可读性和可维护性。

**示例：**
```python
from typing import List, Dict, Optional, Union

def process_users(
    users: List[Dict[str, str]],
    filter_role: Optional[str] = None
) -> List[str]:
    """
    处理用户列表

    Args:
        users: 用户字典列表
        filter_role: 可选的角色过滤器

    Returns:
        用户名列表
    """
    result = []
    for user in users:
        if filter_role is None or user.get('role') == filter_role:
            result.append(user['name'])
    return result
```

### 2. 编写文档字符串

为所有公共模块、类、函数编写文档字符串。

**Google Style（推荐）：**
```python
def calculate_total(items: List[float], tax_rate: float = 0.1) -> float:
    """计算总价（含税）

    Args:
        items: 商品价格列表
        tax_rate: 税率，默认 0.1（10%）

    Returns:
        含税总价

    Raises:
        ValueError: 如果税率为负数

    Examples:
        >>> calculate_total([10.0, 20.0], 0.1)
        33.0
    """
    if tax_rate < 0:
        raise ValueError("税率不能为负数")

    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### 3. 使用上下文管理器

使用 `with` 语句管理资源，确保正确清理。

**示例：**
```python
# 文件操作
with open('data.txt', 'r') as f:
    content = f.read()

# 数据库连接
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

# 自定义上下文管理器
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """计时上下文管理器"""
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"{name} 耗时: {end - start:.2f}秒")

with timer("数据处理"):
    # 执行耗时操作
    process_data()
```

### 4. 异常处理

明确捕获特定异常，避免使用裸 `except`。

**好的做法：**
```python
try:
    result = int(user_input)
except ValueError:
    print("输入必须是数字")
except KeyboardInterrupt:
    print("用户取消操作")
    raise
```

**避免：**
```python
try:
    result = int(user_input)
except:  # 不要这样做！
    pass
```

### 5. 使用列表推导式

简洁高效的列表生成方式。

**示例：**
```python
# 基础列表推导
squares = [x**2 for x in range(10)]

# 带条件
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# 字典推导
user_ages = {user['name']: user['age'] for user in users}

# 集合推导
unique_roles = {user['role'] for user in users}
```

### 6. 使用生成器

处理大数据集时使用生成器节省内存。

**示例：**
```python
def read_large_file(file_path: str):
    """逐行读取大文件"""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# 使用
for line in read_large_file('huge_file.txt'):
    process_line(line)
```

### 7. 函数设计原则

**单一职责原则：**
```python
# 好的做法：每个函数只做一件事
def validate_email(email: str) -> bool:
    return '@' in email and '.' in email

def send_email(to: str, subject: str, body: str):
    # 发送邮件逻辑
    pass

# 避免：一个函数做太多事
def validate_and_send_email(email: str, subject: str, body: str):
    # 既验证又发送
    pass
```

**保持函数简短：**
- 理想情况下不超过 20-30 行
- 如果函数太长，考虑拆分

### 8. 避免魔法数字

使用命名常量代替硬编码的数字。

**示例：**
```python
# 好的做法
MAX_RETRY_ATTEMPTS = 3
TIMEOUT_SECONDS = 30

def fetch_data(url: str) -> dict:
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS)
            return response.json()
        except requests.Timeout:
            if attempt == MAX_RETRY_ATTEMPTS - 1:
                raise

# 避免
def fetch_data(url: str) -> dict:
    for attempt in range(3):  # 3 是什么意思？
        try:
            response = requests.get(url, timeout=30)  # 30 是什么意思？
            return response.json()
        except requests.Timeout:
            if attempt == 2:
                raise
```

## 工具选择建议

### 快速开始（推荐）

使用 **Ruff** 作为一站式解决方案：

```bash
pip install ruff
ruff check --fix .
ruff format .
```

### 严格检查

组合使用多个工具：

```bash
pip install ruff pylint mypy
ruff check .
pylint src/
mypy src/
```

### CI/CD 集成

在 `.github/workflows/lint.yml` 中：

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install ruff
      - run: ruff check .
```

## 工作流程

### 开发时

1. 编写代码
2. 运行 `ruff check --fix .` 自动修复
3. 运行 `ruff format .` 格式化
4. 提交代码

### 代码审查前

1. 运行完整检查：`ruff check .`
2. 运行类型检查：`mypy .`
3. 运行测试：`pytest`
4. 确保所有检查通过

### 项目初始化

1. 创建 `pyproject.toml` 配置文件
2. 配置 pre-commit hooks
3. 在 CI/CD 中集成检查
4. 团队统一工具和配置

## 附加资源

### 参考文件

详细的代码示例和模式，请参考：

- **`references/pep8-guide.md`** - PEP 8 完整指南
- **`references/tool-comparison.md`** - 工具对比和选择
- **`references/advanced-patterns.md`** - 高级编程模式

### 示例文件

工作示例代码：

- **`examples/good-code.py`** - 符合规范的代码示例
- **`examples/bad-code.py`** - 常见错误示例
- **`examples/refactoring.py`** - 重构前后对比

## 总结

编写高质量 Python 代码的关键：

1. **遵循 PEP 8** - 统一的代码风格
2. **使用工具** - Ruff/Black/Pylint 自动化检查
3. **类型提示** - 提高代码可读性
4. **文档字符串** - 清晰的文档
5. **最佳实践** - 上下文管理器、异常处理、生成器等
6. **持续改进** - 代码审查和重构

记住：好的代码不仅能运行，还要易读、易维护、易扩展。
