---
name: Python 文档编写规范
description: This skill should be used when the user asks about "Python 文档", "docstring", "如何写文档字符串", "Google Style", "NumPy Style", "Sphinx", "API 文档生成", or mentions "pydoc", "pdoc", "文档注释". Provides comprehensive guidance on Python documentation standards and tools.
version: 0.1.0
---

# Python 文档编写规范

## 概述

本技能提供 Python 文档字符串（docstring）编写规范、文档生成工具使用指南和 API 文档最佳实践。帮助开发者编写清晰、专业的代码文档。

## 文档字符串基础

### 什么是 Docstring

文档字符串是紧跟在模块、类、函数或方法定义后的字符串字面量，用三引号包围。

**基本格式：**
```python
def function():
    """这是一个文档字符串"""
    pass
```

**访问文档字符串：**
```python
print(function.__doc__)
help(function)
```

### PEP 257 规范

PEP 257 定义了文档字符串的基本约定：

1. **所有公共模块、函数、类、方法都应该有文档字符串**
2. **使用三重双引号** `"""`（即使是单行）
3. **单行文档字符串**：摘要在同一行，结束引号在同一行
4. **多行文档字符串**：摘要行，空行，详细描述

**单行示例：**
```python
def add(a, b):
    """返回两个数的和"""
    return a + b
```

**多行示例：**
```python
def complex_function(arg1, arg2):
    """
    执行复杂操作的函数

    这里是详细描述，解释函数的功能、
    使用场景和注意事项。

    Args:
        arg1: 第一个参数
        arg2: 第二个参数

    Returns:
        操作结果
    """
    pass
```

## 文档风格

### Google Style（推荐）

Google Style 是最流行和易读的文档风格。

**函数文档：**
```python
def fetch_user_data(user_id: int, include_posts: bool = False) -> dict:
    """获取用户数据

    从数据库中获取指定用户的详细信息，可选择性地包含用户的文章列表。

    Args:
        user_id: 用户的唯一标识符
        include_posts: 是否包含用户的文章列表，默认为 False

    Returns:
        包含用户信息的字典，格式如下：
        {
            'id': int,
            'name': str,
            'email': str,
            'posts': list (可选)
        }

    Raises:
        ValueError: 如果 user_id 小于等于 0
        DatabaseError: 如果数据库连接失败

    Examples:
        >>> user = fetch_user_data(123)
        >>> print(user['name'])
        'Alice'

        >>> user_with_posts = fetch_user_data(123, include_posts=True)
        >>> len(user_with_posts['posts'])
        5

    Note:
        此函数会缓存结果 5 分钟，频繁调用不会造成性能问题。
    """
    if user_id <= 0:
        raise ValueError("user_id 必须大于 0")

    # 实现代码...
    return {}
```

**类文档：**
```python
class UserManager:
    """用户管理器

    负责用户的创建、查询、更新和删除操作。提供缓存机制以提高查询性能。

    Attributes:
        cache_timeout: 缓存超时时间（秒），默认 300
        max_cache_size: 最大缓存条目数，默认 1000

    Examples:
        >>> manager = UserManager(cache_timeout=600)
        >>> user = manager.get_user(123)
        >>> manager.create_user('Alice', 'alice@example.com')
    """

    def __init__(self, cache_timeout: int = 300):
        """初始化用户管理器

        Args:
            cache_timeout: 缓存超时时间（秒）
        """
        self.cache_timeout = cache_timeout
        self._cache = {}

    def get_user(self, user_id: int) -> dict:
        """获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            用户信息字典

        Raises:
            UserNotFoundError: 如果用户不存在
        """
        pass
```

**模块文档：**
```python
"""用户管理模块

此模块提供用户管理的核心功能，包括用户的 CRUD 操作、
认证和权限管理。

主要类：
    UserManager: 用户管理器
    User: 用户模型

主要函数：
    authenticate_user: 用户认证
    check_permission: 权限检查

使用示例：
    from myapp.users import UserManager

    manager = UserManager()
    user = manager.get_user(123)

作者：
    Your Name <your.email@example.com>

版本：
    1.0.0
"""

import logging
from typing import Optional

# 模块代码...
```

### NumPy Style

NumPy Style 使用更结构化的格式，适合科学计算项目。

**函数文档：**
```python
def calculate_statistics(data: list, method: str = 'mean') -> float:
    """
    计算数据的统计量

    对输入数据计算指定的统计量，支持均值、中位数、标准差等。

    Parameters
    ----------
    data : list of float
        输入数据列表
    method : {'mean', 'median', 'std'}, optional
        统计方法，默认为 'mean'

    Returns
    -------
    float
        计算得到的统计量

    Raises
    ------
    ValueError
        如果数据列表为空
    KeyError
        如果指定的方法不支持

    See Also
    --------
    numpy.mean : NumPy 的均值函数
    numpy.median : NumPy 的中位数函数

    Notes
    -----
    此函数使用 Welford 算法计算标准差，具有更好的数值稳定性。

    算法复杂度为 O(n)，其中 n 是数据点数量。

    References
    ----------
    .. [1] Welford, B. P. (1962). "Note on a method for calculating
           corrected sums of squares and products".

    Examples
    --------
    >>> data = [1, 2, 3, 4, 5]
    >>> calculate_statistics(data, method='mean')
    3.0

    >>> calculate_statistics(data, method='std')
    1.4142135623730951
    """
    pass
```

### Sphinx Style

Sphinx 是 Python 官方文档工具使用的风格。

**函数文档：**
```python
def process_data(input_file, output_file, format='json'):
    """
    处理数据文件

    读取输入文件，处理数据，并将结果写入输出文件。

    :param input_file: 输入文件路径
    :type input_file: str
    :param output_file: 输出文件路径
    :type output_file: str
    :param format: 输出格式，可选 'json' 或 'csv'
    :type format: str, optional
    :return: 处理的记录数
    :rtype: int
    :raises FileNotFoundError: 如果输入文件不存在
    :raises ValueError: 如果格式不支持

    .. note::
       此函数会自动创建输出目录（如果不存在）

    .. warning::
       大文件处理可能消耗大量内存

    示例::

        >>> count = process_data('input.txt', 'output.json')
        >>> print(f"处理了 {count} 条记录")
        处理了 100 条记录
    """
    pass
```

## 文档生成工具

### Sphinx

Sphinx 是最流行的 Python 文档生成工具，用于生成 Python 官方文档。

**安装：**
```bash
pip install sphinx sphinx-rtd-theme
```

**初始化项目：**
```bash
cd docs
sphinx-quickstart
```

**配置 conf.py：**
```python
# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'My Project'
author = 'Your Name'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',      # 自动从 docstring 生成文档
    'sphinx.ext.napoleon',     # 支持 Google/NumPy 风格
    'sphinx.ext.viewcode',     # 添加源代码链接
    'sphinx.ext.intersphinx',  # 链接到其他项目文档
]

html_theme = 'sphinx_rtd_theme'

# Napoleon 设置
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
```

**编写文档 (docs/index.rst)：**
```rst
Welcome to My Project
=====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api

API Reference
=============

.. automodule:: mypackage.users
   :members:
   :undoc-members:
   :show-inheritance:
```

**生成文档：**
```bash
cd docs
make html
```

**查看文档：**
```bash
open _build/html/index.html
```

### pdoc

pdoc 是一个轻量级的文档生成工具，无需配置。

**安装：**
```bash
pip install pdoc
```

**生成文档：**
```bash
# 生成 HTML 文档
pdoc --html mypackage

# 启动文档服务器
pdoc --http : mypackage

# 生成 Markdown 文档
pdoc --output-dir docs mypackage
```

**特点：**
- 零配置，开箱即用
- 自动识别 Google/NumPy 风格
- 支持 Markdown 输出
- 内置 HTTP 服务器

### pydoc

Python 内置的文档工具。

**使用：**
```bash
# 查看模块文档
python -m pydoc mymodule

# 启动 HTTP 服务器
python -m pydoc -b

# 生成 HTML 文件
python -m pydoc -w mymodule
```

## 最佳实践

### 1. 文档完整性

**必须编写文档的内容：**
- 所有公共模块
- 所有公共类
- 所有公共函数和方法
- 复杂的私有函数

**可以省略文档的内容：**
- 非常简单的私有方法
- 测试函数（但测试类应该有文档）
- 明显的 getter/setter

### 2. 文档内容

**好的文档应该包含：**
- **功能描述**：做什么
- **参数说明**：每个参数的含义、类型、默认值
- **返回值**：返回什么、什么类型
- **异常**：可能抛出的异常
- **示例**：如何使用
- **注意事项**：特殊情况、性能考虑

**示例：**
```python
def retry_on_failure(func, max_attempts=3, delay=1.0):
    """重试装饰器

    在函数执行失败时自动重试，适用于网络请求等可能临时失败的操作。

    Args:
        func: 要装饰的函数
        max_attempts: 最大重试次数，默认 3 次
        delay: 重试间隔（秒），默认 1.0 秒

    Returns:
        装饰后的函数

    Examples:
        >>> @retry_on_failure(max_attempts=5, delay=2.0)
        ... def fetch_data():
        ...     return requests.get('https://api.example.com/data')

    Note:
        - 每次重试之间会等待 delay 秒
        - 如果所有重试都失败，会抛出最后一次的异常
        - 不适用于幂等性要求高的操作

    Warning:
        使用此装饰器时要注意：
        - 确保被装饰的函数是幂等的
        - 避免在数据库写操作上使用
    """
    pass
```

### 3. 类型注解与文档

结合类型注解和文档字符串：

```python
from typing import List, Dict, Optional

def process_users(
    users: List[Dict[str, str]],
    filter_role: Optional[str] = None,
    limit: int = 100
) -> List[str]:
    """处理用户列表

    过滤并提取用户名。

    Args:
        users: 用户字典列表，每个字典包含 'name' 和 'role' 键
        filter_role: 可选的角色过滤器，仅返回匹配角色的用户
        limit: 返回的最大用户数

    Returns:
        用户名列表

    Examples:
        >>> users = [
        ...     {'name': 'Alice', 'role': 'admin'},
        ...     {'name': 'Bob', 'role': 'user'}
        ... ]
        >>> process_users(users, filter_role='admin')
        ['Alice']
    """
    pass
```

### 4. 文档维护

**保持文档同步：**
- 修改代码时同步更新文档
- 代码审查时检查文档
- 使用 CI/CD 自动生成文档

**文档测试：**
```python
def add(a, b):
    """
    返回两个数的和

    Examples:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
    """
    return a + b

# 运行文档测试
if __name__ == '__main__':
    import doctest
    doctest.testmod()
```

### 5. 项目文档结构

**推荐的文档目录结构：**
```
docs/
├── index.rst              # 首页
├── installation.rst       # 安装指南
├── quickstart.rst         # 快速开始
├── tutorial/              # 教程
│   ├── basic.rst
│   └── advanced.rst
├── api/                   # API 文档
│   ├── users.rst
│   └── posts.rst
├── guides/                # 使用指南
│   ├── configuration.rst
│   └── deployment.rst
└── changelog.rst          # 更新日志
```

## 文档模板

### 模块模板

```python
"""模块简短描述

详细描述模块的功能、用途和使用场景。

主要类：
    ClassName1: 类的简短描述
    ClassName2: 类的简短描述

主要函数：
    function_name: 函数的简短描述

使用示例：
    from mypackage import mymodule

    result = mymodule.function_name()

作者：
    Your Name <your.email@example.com>

版本：
    1.0.0

许可证：
    MIT License
"""
```

### 类模板

```python
class ClassName:
    """类的简短描述

    详细描述类的功能、职责和使用场景。

    Attributes:
        attr1: 属性1的描述
        attr2: 属性2的描述

    Examples:
        >>> obj = ClassName(param1, param2)
        >>> result = obj.method()
    """

    def __init__(self, param1, param2):
        """初始化类实例

        Args:
            param1: 参数1的描述
            param2: 参数2的描述
        """
        pass

    def method(self):
        """方法的简短描述

        详细描述方法的功能。

        Returns:
            返回值描述

        Raises:
            ExceptionType: 异常描述
        """
        pass
```

### 函数模板

```python
def function_name(param1: type1, param2: type2 = default) -> return_type:
    """函数的简短描述

    详细描述函数的功能、算法和使用场景。

    Args:
        param1: 参数1的描述
        param2: 参数2的描述，默认值为 default

    Returns:
        返回值的详细描述

    Raises:
        ValueError: 什么情况下抛出
        TypeError: 什么情况下抛出

    Examples:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output

    Note:
        重要的注意事项

    Warning:
        警告信息
    """
    pass
```

## 附加资源

### 参考文件

详细的文档编写指南，请参考：

- **`references/google-style-guide.md`** - Google Style 完整指南
- **`references/numpy-style-guide.md`** - NumPy Style 完整指南
- **`references/sphinx-tutorial.md`** - Sphinx 使用教程

### 示例文件

完整的文档示例：

- **`examples/documented-module.py`** - 完整的模块文档示例
- **`examples/documented-class.py`** - 完整的类文档示例

## 总结

编写优秀 Python 文档的关键：

1. **选择合适的风格** - Google Style 最易读（推荐）
2. **保持一致性** - 整个项目使用同一风格
3. **完整性** - 包含所有必要信息
4. **示例代码** - 提供实际使用示例
5. **类型注解** - 结合类型提示
6. **自动生成** - 使用 Sphinx/pdoc 生成文档
7. **持续维护** - 代码变更时同步更新文档

记住：好的文档是项目成功的关键，投入时间编写文档会大大提高代码的可维护性和可用性。
