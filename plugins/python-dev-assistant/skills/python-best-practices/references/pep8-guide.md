# PEP 8 完整指南

## 代码布局

### 缩进

- 使用 4 个空格进行缩进
- 不要使用 Tab
- 续行应该垂直对齐，或使用悬挂缩进

**垂直对齐：**
```python
# 与左括号对齐
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# 字典
my_dict = {
    'key1': 'value1',
    'key2': 'value2',
}
```

**悬挂缩进：**
```python
# 悬挂缩进应该增加一级
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

### 最大行长度

- 代码行：79 字符
- 文档字符串/注释：72 字符
- 长表达式可以使用括号换行

**示例：**
```python
# 使用括号换行
result = (some_function(arg1, arg2) +
          another_function(arg3, arg4))

# 长字符串
message = (
    "这是一个很长的消息，"
    "需要分成多行来保持可读性。"
)
```

### 空行

- 顶层函数和类定义之间：2 个空行
- 类内方法定义之间：1 个空行
- 函数内逻辑段落之间：1 个空行（谨慎使用）

```python
class MyClass:
    """类定义"""

    def method_one(self):
        """第一个方法"""
        pass

    def method_two(self):
        """第二个方法"""
        pass


def top_level_function():
    """顶层函数"""
    pass


class AnotherClass:
    """另一个类"""
    pass
```

### 导入

**导入顺序：**
1. 标准库导入
2. 相关第三方库导入
3. 本地应用/库导入

每组之间空一行。

```python
# 标准库
import os
import sys
from typing import List, Dict

# 第三方库
import numpy as np
import pandas as pd
from django.db import models

# 本地模块
from myapp.models import User
from myapp.utils import helper
```

**导入规则：**
- 每个导入独立一行
- 避免使用通配符导入（`from module import *`）
- 使用绝对导入优于相对导入

```python
# 好的做法
import os
import sys

# 避免
import os, sys

# 避免通配符
from module import *

# 推荐绝对导入
from mypackage.subpackage import module

# 相对导入（仅在包内使用）
from . import sibling
from .. import parent
```

## 表达式和语句中的空格

### 避免多余的空格

**括号内：**
```python
# 好
spam(ham[1], {eggs: 2})

# 坏
spam( ham[ 1 ], { eggs: 2 } )
```

**逗号、分号、冒号前：**
```python
# 好
if x == 4: print(x, y); x, y = y, x

# 坏
if x == 4 : print(x , y) ; x , y = y , x
```

**切片：**
```python
# 好
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]

# 坏
ham[1: 9], ham[1 :9], ham[1:9 :3]
```

**函数调用：**
```python
# 好
spam(1)

# 坏
spam (1)
```

**索引：**
```python
# 好
dct['key'] = lst[index]

# 坏
dct ['key'] = lst [index]
```

### 其他建议

**赋值运算符周围：**
```python
# 好
x = 1
y = 2
long_variable = 3

# 坏（不要为了对齐而添加空格）
x             = 1
y             = 2
long_variable = 3
```

**关键字参数和默认值：**
```python
# 好
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# 坏
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

**类型注解：**
```python
# 好
def munge(input: str) -> str:
    pass

def munge(sep: str = None):
    pass

# 坏
def munge(input:str)->str:
    pass

def munge(sep : str = None):
    pass
```

## 注释

### 块注释

- 与代码同级缩进
- 每行以 `#` 和一个空格开始
- 段落之间用只包含 `#` 的行分隔

```python
# 这是一个块注释
# 它可以跨越多行
#
# 段落之间用空行分隔
def function():
    pass
```

### 行内注释

- 与语句至少间隔两个空格
- 以 `#` 和一个空格开始
- 谨慎使用

```python
x = x + 1  # 增加计数器
```

### 文档字符串

- 所有公共模块、函数、类、方法都应该有文档字符串
- 单行文档字符串：`"""单行描述"""`
- 多行文档字符串：首行摘要，空行，详细描述

```python
def simple_function():
    """这是一个简单的函数"""
    pass

def complex_function(arg1, arg2):
    """
    这是一个复杂的函数

    详细描述函数的功能、参数和返回值。

    Args:
        arg1: 第一个参数
        arg2: 第二个参数

    Returns:
        返回值描述
    """
    pass
```

## 命名约定

### 命名风格

- `lowercase` - 小写
- `lower_case_with_underscores` - 小写加下划线
- `UPPERCASE` - 大写
- `UPPER_CASE_WITH_UNDERSCORES` - 大写加下划线
- `CapitalizedWords` - 首字母大写（驼峰）
- `mixedCase` - 混合大小写（不推荐）
- `_single_leading_underscore` - 单前导下划线（弱内部使用）
- `single_trailing_underscore_` - 单后置下划线（避免关键字冲突）
- `__double_leading_underscore` - 双前导下划线（名称修饰）
- `__double_leading_and_trailing_underscore__` - 魔术方法

### 规定性命名约定

**模块名：**
- 短小写名称
- 可以使用下划线

```python
# 好
mymodule.py
my_module.py

# 避免
MyModule.py
```

**类名：**
- 使用 CapitalizedWords 约定

```python
class MyClass:
    pass

class HTTPServer:
    pass
```

**异常名：**
- 使用 CapitalizedWords
- 如果是错误，添加 "Error" 后缀

```python
class ValidationError(Exception):
    pass

class NetworkError(Exception):
    pass
```

**函数和变量名：**
- 小写，单词之间用下划线分隔

```python
def my_function():
    pass

my_variable = 10
```

**函数和方法参数：**
- 实例方法第一个参数：`self`
- 类方法第一个参数：`cls`

```python
class MyClass:
    def instance_method(self, arg):
        pass

    @classmethod
    def class_method(cls, arg):
        pass

    @staticmethod
    def static_method(arg):
        pass
```

**常量：**
- 全大写，单词之间用下划线分隔
- 通常定义在模块级别

```python
MAX_OVERFLOW = 100
TOTAL_COUNT = 0
```

**私有属性和方法：**
- 单前导下划线：弱内部使用
- 双前导下划线：名称修饰（避免子类冲突）

```python
class MyClass:
    def __init__(self):
        self._internal_var = 1  # 弱私有
        self.__private_var = 2  # 强私有

    def _internal_method(self):
        pass

    def __private_method(self):
        pass
```

## 编程建议

### 比较

**None 比较：**
```python
# 好
if x is None:
    pass

if x is not None:
    pass

# 坏
if x == None:
    pass
```

**布尔值比较：**
```python
# 好
if greeting:
    pass

# 坏
if greeting == True:
    pass

if greeting is True:
    pass
```

**序列为空：**
```python
# 好
if not seq:
    pass

if seq:
    pass

# 坏
if len(seq) == 0:
    pass

if len(seq):
    pass
```

### 异常

**捕获特定异常：**
```python
# 好
try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None

# 坏
try:
    import platform_specific_module
except:
    platform_specific_module = None
```

**异常链：**
```python
# 好
try:
    process_data()
except ValueError as e:
    raise DataProcessingError("处理失败") from e

# 保留原始异常
try:
    process_data()
except ValueError:
    raise  # 重新抛出原始异常
```

### 返回语句

**一致性：**
```python
# 好
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

# 或
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    return None

# 坏（不一致）
def foo(x):
    if x >= 0:
        return math.sqrt(x)
```

### 字符串

**字符串拼接：**
```python
# 好
result = ''.join(['a', 'b', 'c'])
result = f"Hello, {name}!"

# 避免（在循环中）
result = ''
for item in items:
    result += item  # 效率低
```

**字符串前缀：**
```python
# 好
r'raw string'
f'formatted {string}'
b'bytes'

# 坏
'raw string'  # 应该使用 r''
```

### 类型注解

**使用类型注解：**
```python
from typing import List, Dict, Optional, Union

def process_items(items: List[str]) -> Dict[str, int]:
    """处理项目列表"""
    return {item: len(item) for item in items}

def get_user(user_id: int) -> Optional[User]:
    """获取用户，可能返回 None"""
    return User.objects.filter(id=user_id).first()
```

## 工具配置

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
]
ignore = [
    "E501",  # line too long
]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### .flake8

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist
```

### .pylintrc

```ini
[MASTER]
ignore=CVS,.git,__pycache__,.venv

[FORMAT]
max-line-length=88

[MESSAGES CONTROL]
disable=C0111,  # missing-docstring
        C0103,  # invalid-name
```

## 参考资源

- **PEP 8 官方文档**: https://peps.python.org/pep-0008/
- **PEP 257 文档字符串**: https://peps.python.org/pep-0257/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **Real Python PEP 8**: https://realpython.com/python-pep8/
