---
name: py-snippet
description: 插入 Python 代码片段
argument-hint: "[--type=class|dataclass|decorator|cli|async|test|...]"
allowed-tools: ["Write", "Read", "Edit"]
---

# Python 代码片段命令

快速插入常用的 Python 代码模板和片段。

## 使用方法

```bash
# 显示可用片段列表
/py-snippet

# 插入指定类型的片段
/py-snippet --type=class
/py-snippet --type=decorator
/py-snippet --type=cli
```

## 可用片段类型

### 1. class - 类定义
标准类定义模板，包含文档字符串和常用方法。

### 2. dataclass - 数据类
使用 @dataclass 装饰器的数据类模板。

### 3. decorator - 装饰器
函数装饰器模板，支持参数。

### 4. context-manager - 上下文管理器
使用 @contextmanager 的上下文管理器。

### 5. cli - 命令行工具
使用 argparse 的命令行工具模板。

### 6. async-function - 异步函数
异步函数和协程模板。

### 7. test-case - 单元测试
unittest/pytest 测试用例模板。

### 8. exception - 自定义异常
自定义异常类模板。

### 9. property - 属性装饰器
使用 @property 的属性模板。

### 10. singleton - 单例模式
单例模式实现。

### 11. factory - 工厂模式
工厂模式实现。

### 12. api-endpoint - API 端点
Flask/Django API 端点模板。

## 代码片段详情

### 1. Class（类定义）

```python
class ClassName:
    """类的简短描述

    详细描述类的功能和用途。

    Attributes:
        attr1: 属性1的描述
        attr2: 属性2的描述

    Examples:
        >>> obj = ClassName(param1, param2)
        >>> result = obj.method()
    """

    def __init__(self, param1: type1, param2: type2):
        """初始化类实例

        Args:
            param1: 参数1的描述
            param2: 参数2的描述
        """
        self.attr1 = param1
        self.attr2 = param2

    def method(self) -> return_type:
        """方法的简短描述

        Returns:
            返回值描述
        """
        pass

    def __str__(self) -> str:
        """字符串表示"""
        return f"ClassName({self.attr1}, {self.attr2})"

    def __repr__(self) -> str:
        """开发者友好的表示"""
        return f"ClassName(attr1={self.attr1!r}, attr2={self.attr2!r})"
```

### 2. Dataclass（数据类）

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class DataClassName:
    """数据类的简短描述

    Attributes:
        field1: 字段1的描述
        field2: 字段2的描述
        field3: 字段3的描述（带默认值）
    """
    field1: str
    field2: int
    field3: List[str] = field(default_factory=list)

    def method(self) -> str:
        """方法描述"""
        return f"{self.field1}: {self.field2}"
```

### 3. Decorator（装饰器）

```python
from functools import wraps
from typing import Callable, Any

def decorator_name(param: Any = None) -> Callable:
    """装饰器的简短描述

    Args:
        param: 装饰器参数描述

    Returns:
        装饰后的函数

    Examples:
        >>> @decorator_name(param="value")
        ... def my_function():
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 前置处理
            print(f"Calling {func.__name__} with param={param}")

            # 调用原函数
            result = func(*args, **kwargs)

            # 后置处理
            print(f"Finished {func.__name__}")

            return result
        return wrapper
    return decorator
```

### 4. Context Manager（上下文管理器）

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def context_manager_name(param: Any) -> Generator:
    """上下文管理器的简短描述

    Args:
        param: 参数描述

    Yields:
        资源对象

    Examples:
        >>> with context_manager_name(param) as resource:
        ...     # 使用资源
        ...     pass
    """
    # 设置资源
    resource = setup_resource(param)

    try:
        yield resource
    finally:
        # 清理资源
        cleanup_resource(resource)
```

### 5. CLI（命令行工具）

```python
import argparse
import sys
from typing import List, Optional

def main(argv: Optional[List[str]] = None) -> int:
    """主函数

    Args:
        argv: 命令行参数列表

    Returns:
        退出码（0 表示成功）
    """
    parser = argparse.ArgumentParser(
        description='程序描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='使用示例和额外信息'
    )

    parser.add_argument(
        'input',
        help='输入文件路径'
    )

    parser.add_argument(
        '-o', '--output',
        default='output.txt',
        help='输出文件路径（默认: output.txt）'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args(argv)

    # 处理逻辑
    try:
        process(args.input, args.output, args.verbose)
        return 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

def process(input_file: str, output_file: str, verbose: bool) -> None:
    """处理逻辑"""
    if verbose:
        print(f"处理 {input_file} -> {output_file}")
    # 实现处理逻辑

if __name__ == '__main__':
    sys.exit(main())
```

### 6. Async Function（异步函数）

```python
import asyncio
from typing import List

async def async_function_name(param: str) -> dict:
    """异步函数的简短描述

    Args:
        param: 参数描述

    Returns:
        返回值描述

    Examples:
        >>> result = await async_function_name("value")
    """
    # 异步操作
    await asyncio.sleep(1)

    # 返回结果
    return {'result': param}

async def fetch_multiple(items: List[str]) -> List[dict]:
    """并发获取多个项目"""
    tasks = [async_function_name(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# 运行异步函数
if __name__ == '__main__':
    result = asyncio.run(async_function_name("test"))
    print(result)
```

### 7. Test Case（单元测试）

**Pytest 风格：**
```python
import pytest
from mymodule import MyClass

class TestMyClass:
    """MyClass 测试类"""

    @pytest.fixture
    def instance(self):
        """创建测试实例"""
        return MyClass(param1="value1", param2="value2")

    def test_initialization(self, instance):
        """测试初始化"""
        assert instance.attr1 == "value1"
        assert instance.attr2 == "value2"

    def test_method(self, instance):
        """测试方法"""
        result = instance.method()
        assert result == expected_value

    def test_edge_case(self, instance):
        """测试边界情况"""
        with pytest.raises(ValueError):
            instance.method_that_raises()

    @pytest.mark.parametrize("input,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
        ("input3", "output3"),
    ])
    def test_multiple_inputs(self, instance, input, expected):
        """测试多个输入"""
        result = instance.process(input)
        assert result == expected
```

**Unittest 风格：**
```python
import unittest
from mymodule import MyClass

class TestMyClass(unittest.TestCase):
    """MyClass 测试类"""

    def setUp(self):
        """每个测试前运行"""
        self.instance = MyClass(param1="value1", param2="value2")

    def tearDown(self):
        """每个测试后运行"""
        pass

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.instance.attr1, "value1")
        self.assertEqual(self.instance.attr2, "value2")

    def test_method(self):
        """测试方法"""
        result = self.instance.method()
        self.assertEqual(result, expected_value)

    def test_edge_case(self):
        """测试边界情况"""
        with self.assertRaises(ValueError):
            self.instance.method_that_raises()

if __name__ == '__main__':
    unittest.main()
```

### 8. Exception（自定义异常）

```python
class CustomError(Exception):
    """自定义异常基类

    所有自定义异常的基类。

    Attributes:
        message: 错误消息
        code: 错误代码
    """

    def __init__(self, message: str, code: int = None):
        """初始化异常

        Args:
            message: 错误消息
            code: 可选的错误代码
        """
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

class ValidationError(CustomError):
    """验证错误"""
    def __init__(self, message: str):
        super().__init__(message, code=400)

class NotFoundError(CustomError):
    """资源未找到错误"""
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", code=404)
```

### 9. Property（属性装饰器）

```python
class PropertyExample:
    """属性装饰器示例"""

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        """获取值

        Returns:
            当前值
        """
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        """设置值

        Args:
            new_value: 新值

        Raises:
            ValueError: 如果值无效
        """
        if new_value < 0:
            raise ValueError("值不能为负数")
        self._value = new_value

    @value.deleter
    def value(self) -> None:
        """删除值"""
        del self._value
```

### 10. Singleton（单例模式）

```python
class Singleton:
    """单例模式实现

    确保类只有一个实例。

    Examples:
        >>> instance1 = Singleton()
        >>> instance2 = Singleton()
        >>> assert instance1 is instance2
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化（只在第一次创建时执行）"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # 初始化代码
```

### 11. Factory（工厂模式）

```python
from abc import ABC, abstractmethod
from typing import Dict, Type

class Product(ABC):
    """产品抽象基类"""

    @abstractmethod
    def operation(self) -> str:
        """产品操作"""
        pass

class ConcreteProductA(Product):
    """具体产品 A"""
    def operation(self) -> str:
        return "Product A"

class ConcreteProductB(Product):
    """具体产品 B"""
    def operation(self) -> str:
        return "Product B"

class Factory:
    """工厂类"""

    _products: Dict[str, Type[Product]] = {
        'A': ConcreteProductA,
        'B': ConcreteProductB,
    }

    @classmethod
    def create(cls, product_type: str) -> Product:
        """创建产品

        Args:
            product_type: 产品类型

        Returns:
            产品实例

        Raises:
            ValueError: 如果产品类型不支持
        """
        product_class = cls._products.get(product_type)
        if not product_class:
            raise ValueError(f"Unknown product type: {product_type}")
        return product_class()
```

### 12. API Endpoint（API 端点）

**Flask 风格：**
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('resource', __name__)

@bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    """获取资源列表"""
    # 查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 获取数据
    resources = Resource.query.paginate(page=page, per_page=per_page)

    return jsonify({
        'items': [r.to_dict() for r in resources.items],
        'total': resources.total,
        'page': page,
        'per_page': per_page
    })

@bp.route('/resources/<int:resource_id>', methods=['GET'])
@jwt_required()
def get_resource(resource_id):
    """获取单个资源"""
    resource = Resource.query.get_or_404(resource_id)
    return jsonify(resource.to_dict())

@bp.route('/resources', methods=['POST'])
@jwt_required()
def create_resource():
    """创建资源"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # 验证数据
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # 创建资源
    resource = Resource(name=data['name'], user_id=user_id)
    db.session.add(resource)
    db.session.commit()

    return jsonify(resource.to_dict()), 201
```

## 执行流程

1. **解析参数**：
   - 如果没有 `--type` 参数，显示可用片段列表
   - 如果有 `--type`，插入对应的代码片段

2. **确定插入位置**：
   - 当前光标位置
   - 或文件末尾

3. **参数化替换**：
   - 提示用户输入类名、函数名等
   - 替换模板中的占位符

4. **插入代码**：
   - 使用 Write 或 Edit 工具插入代码
   - 保持正确的缩进

5. **格式化**：
   - 可选：运行 `/py-check --fix` 格式化代码

## 输出示例

### 显示片段列表
```
可用的 Python 代码片段：

基础结构：
  class          - 类定义模板
  dataclass      - 数据类模板
  function       - 函数模板

设计模式：
  decorator      - 装饰器模板
  context-manager - 上下文管理器
  singleton      - 单例模式
  factory        - 工厂模式

功能模块：
  cli            - 命令行工具
  async-function - 异步函数
  test-case      - 单元测试
  exception      - 自定义异常
  property       - 属性装饰器
  api-endpoint   - API 端点

使用方法：
  /py-snippet --type=<类型>

示例：
  /py-snippet --type=class
  /py-snippet --type=decorator
```

### 插入片段
```
✓ 已插入代码片段：class

请根据需要修改以下内容：
  - ClassName: 类名
  - param1, param2: 参数名
  - type1, type2: 类型注解
  - 文档字符串

建议：
  运行 /py-check 检查代码风格
```

## 实现提示

1. **片段存储**：
   - 将片段存储在 `scripts/snippets/` 目录
   - 每个片段一个文件

2. **参数化**：
   - 使用占位符：`{ClassName}`, `{param1}` 等
   - 提示用户输入替换值

3. **智能插入**：
   - 检测当前文件类型
   - 保持正确的缩进
   - 添加必要的导入语句

## 提示和技巧

1. **自定义片段**：
   - 在项目中创建 `.claude/snippets/` 目录
   - 添加自定义片段文件

2. **快速访问**：
   - 记住常用片段的类型名
   - 使用 Tab 补全

3. **组合使用**：
   - 插入片段后使用 `/py-check --fix` 格式化
   - 使用 `/py-docs` 生成文档

## 相关命令

- `/py-check` - 检查代码质量
- `/py-docs` - 生成文档
