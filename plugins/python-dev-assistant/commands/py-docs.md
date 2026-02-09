---
name: py-docs
description: 生成 Python 文档
argument-hint: "[--scope=file|module|project] [--tool=sphinx|pdoc] [--output=<dir>]"
allowed-tools: ["Read", "Bash", "Write", "Glob", "Grep"]
---

# Python 文档生成命令

为 Python 代码自动生成文档，支持多种文档工具和输出格式。

## 使用方法

```bash
# 为当前文件生成文档
/py-docs

# 为整个模块生成文档
/py-docs --scope=module

# 为整个项目生成文档
/py-docs --scope=project

# 指定文档工具
/py-docs --tool=sphinx
/py-docs --tool=pdoc

# 指定输出目录
/py-docs --output=docs/
```

## 执行流程

1. **解析参数**：
   - `--scope`: file（默认）| module | project
   - `--tool`: sphinx（默认）| pdoc
   - `--output`: 输出目录（默认：docs/）

2. **读取配置**：
   - 检查 `.claude/python-dev-assistant.local.md`
   - 读取 `doc_style` 配置（google/numpy/sphinx）

3. **检查工具是否安装**：
   ```bash
   sphinx-build --version
   # 或
   pdoc --version
   ```

4. **确定文档范围**：
   - **file**: 当前打开的 Python 文件
   - **module**: 当前模块（目录）
   - **project**: 整个项目

5. **生成文档**：
   根据选择的工具执行相应命令

6. **显示结果**：
   - 文档位置
   - 如何查看文档
   - 下一步建议

## 文档工具

### Sphinx

最流行的 Python 文档工具，用于生成 Python 官方文档。

**初始化（首次使用）**：
```bash
cd docs
sphinx-quickstart
```

**配置 conf.py**：
```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

napoleon_google_docstring = True
html_theme = 'sphinx_rtd_theme'
```

**生成文档**：
```bash
cd docs
make html
```

**输出**：`docs/_build/html/index.html`

### pdoc

轻量级文档工具，零配置。

**生成 HTML**：
```bash
pdoc --html mypackage -o docs/
```

**启动服务器**：
```bash
pdoc --http : mypackage
```

**输出**：`docs/mypackage/index.html`

## 项目结构

### Sphinx 文档结构
```
docs/
├── conf.py              # Sphinx 配置
├── index.rst            # 首页
├── installation.rst     # 安装指南
├── quickstart.rst       # 快速开始
├── api/                 # API 文档
│   ├── index.rst
│   ├── users.rst
│   └── models.rst
├── _static/             # 静态文件
├── _templates/          # 模板
└── _build/              # 生成的文档
    └── html/
```

### pdoc 输出结构
```
docs/
└── mypackage/
    ├── index.html
    ├── module1.html
    ├── module2.html
    └── subpackage/
        └── index.html
```

## 生成的文档示例

### index.rst（Sphinx）
```rst
Welcome to MyProject Documentation
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index

Introduction
------------

MyProject is a Python library for...

Installation
------------

.. code-block:: bash

   pip install myproject

Quick Start
-----------

.. code-block:: python

   from myproject import MyClass

   obj = MyClass()
   result = obj.method()

API Reference
=============

.. automodule:: myproject.users
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

### API 文档（自动生成）
```rst
myproject.users module
======================

.. automodule:: myproject.users
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

.. autoclass:: UserManager
   :members:
   :special-members: __init__

Functions
---------

.. autofunction:: authenticate_user
.. autofunction:: check_permission
```

## 输出示例

### 成功生成（Sphinx）
```
✓ 文档生成成功！

文档工具: Sphinx
范围: project
输出目录: docs/_build/html/

生成的文档：
  - 首页: docs/_build/html/index.html
  - API 文档: docs/_build/html/api/index.html
  - 模块数: 5
  - 页面数: 12

查看文档：
  在浏览器中打开: file:///path/to/docs/_build/html/index.html

  或启动本地服务器：
  cd docs/_build/html && python -m http.server

下一步：
  - 编辑 docs/index.rst 自定义首页
  - 添加更多 .rst 文件扩展文档
  - 部署到 Read the Docs: https://readthedocs.org/
```

### 成功生成（pdoc）
```
✓ 文档生成成功！

文档工具: pdoc
范围: project
输出目录: docs/

生成的文档：
  - 入口: docs/mypackage/index.html
  - 模块数: 5

查看文档：
  在浏览器中打开: file:///path/to/docs/mypackage/index.html

  或启动 pdoc 服务器：
  pdoc --http : mypackage

下一步：
  - 完善代码中的 docstring
  - 使用 /py-check 检查文档完整性
```

### 警告（缺少 docstring）
```
⚠ 文档生成完成，但发现问题：

缺少文档字符串的项目：
  - mypackage/users.py:UserManager.get_user (line 45)
  - mypackage/models.py:User (line 10)
  - mypackage/utils.py:helper_function (line 23)

建议：
  为这些项目添加文档字符串以改善文档质量

参考：
  使用 Google Style 编写文档字符串
  运行 /py-snippet --type=docstring 插入模板
```

## 实现提示

### 检查工具安装
```python
def check_tool_installed(tool):
    if tool == 'sphinx':
        result = bash("sphinx-build --version")
        if result.exit_code != 0:
            show_install_guide('sphinx')
    elif tool == 'pdoc':
        result = bash("pdoc --version")
        if result.exit_code != 0:
            show_install_guide('pdoc')
```

### Sphinx 初始化
```python
def init_sphinx(project_name):
    if not os.path.exists('docs/conf.py'):
        # 首次使用，需要初始化
        bash("mkdir -p docs")
        bash("cd docs && sphinx-quickstart --quiet --project='{}' --author='Author'".format(project_name))
        # 修改 conf.py 添加扩展
        update_sphinx_config()
```

### 生成文档
```python
def generate_docs(tool, scope, output):
    if tool == 'sphinx':
        bash("cd docs && make html")
        return "docs/_build/html/index.html"
    elif tool == 'pdoc':
        if scope == 'file':
            bash(f"pdoc --html {current_file} -o {output}")
        else:
            bash(f"pdoc --html {package_name} -o {output}")
        return f"{output}/{package_name}/index.html"
```

## 文档风格检查

检查代码中的文档字符串是否符合规范：

```python
def check_docstring_style(file_path, style='google'):
    """检查文档字符串风格"""
    # 使用 pydocstyle 检查
    result = bash(f"pydocstyle --convention={style} {file_path}")
    return parse_pydocstyle_output(result)
```

## 配置文件支持

读取 `.claude/python-dev-assistant.local.md`：

```yaml
---
doc_style: "google"
python_version: "3.11"
---
```

## 高级功能

### 1. 自动生成 API 文档

为所有模块自动生成 API 文档：

```bash
sphinx-apidoc -o docs/api mypackage
```

### 2. 部署到 Read the Docs

创建 `.readthedocs.yml`：

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: requirements.txt
```

### 3. 文档测试

测试文档中的示例代码：

```bash
cd docs
make doctest
```

### 4. 多语言文档

生成多语言文档：

```bash
sphinx-intl update -p _build/gettext -l zh_CN
```

## 提示和技巧

1. **首次使用**：
   - 使用 pdoc 快速预览
   - 使用 Sphinx 生成专业文档

2. **文档质量**：
   - 确保所有公共 API 都有文档字符串
   - 使用 Google Style 提高可读性
   - 添加使用示例

3. **持续集成**：
   - 在 CI/CD 中自动生成文档
   - 检查文档构建是否成功
   - 自动部署到文档托管平台

4. **文档维护**：
   - 代码变更时同步更新文档
   - 定期检查文档链接
   - 收集用户反馈改进文档

## 相关命令

- `/py-check` - 检查代码质量（包括文档）
- `/py-snippet` - 插入文档字符串模板
