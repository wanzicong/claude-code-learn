---
name: py-django
description: 创建 Django 项目脚手架
argument-hint: "<project_name> [--template=basic|api|fullstack]"
allowed-tools: ["Bash", "Write", "Read", "Glob"]
---

# Django 项目生成命令

快速创建 Django 项目脚手架，支持多种项目模板。

## 使用方法

```bash
# 创建基础项目
/py-django myproject

# 创建 API 项目（Django REST Framework）
/py-django myproject --template=api

# 创建全栈项目（包含前端）
/py-django myproject --template=fullstack
```

## 项目模板

### Basic（基础版）
- Django 核心功能
- 基础应用结构
- SQLite 数据库
- 管理后台
- 静态文件配置

### API（REST API 版）
- Django + Django REST Framework
- JWT 认证
- CORS 支持
- API 文档（drf-yasg）
- PostgreSQL 配置
- 示例 API 端点

### Fullstack（全栈版）
- Django 后端
- React/Vue 前端（可选）
- Webpack 配置
- 前后端分离架构
- 完整的用户认证系统

## 执行流程

1. **验证项目名称**：
   - 检查项目名称是否合法（字母、数字、下划线）
   - 检查目录是否已存在

2. **读取配置**：
   - 检查 `.claude/python-dev-assistant.local.md`
   - 读取 `django_template` 配置（如果存在）
   - 命令行参数优先于配置

3. **检查依赖**：
   - 检查 Python 版本（需要 3.8+）
   - 检查 pip 是否可用
   - 检查 virtualenv 或 venv

4. **创建项目目录**：
   ```bash
   mkdir myproject
   cd myproject
   ```

5. **创建虚拟环境**：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

6. **安装依赖**：
   根据模板安装相应的包：

   **Basic:**
   ```bash
   pip install django
   ```

   **API:**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers drf-yasg psycopg2-binary python-dotenv
   ```

   **Fullstack:**
   ```bash
   pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv
   # 前端依赖通过 npm 安装
   ```

7. **创建 Django 项目**：
   ```bash
   django-admin startproject config .
   ```

8. **创建应用结构**：
   根据模板创建相应的应用：
   ```bash
   python manage.py startapp users
   python manage.py startapp api  # API 模板
   ```

9. **配置项目**：
   - 修改 `settings.py`
   - 配置数据库
   - 添加 INSTALLED_APPS
   - 配置中间件
   - 设置静态文件

10. **创建配置文件**：
    - `.env` - 环境变量
    - `.gitignore` - Git 忽略文件
    - `requirements.txt` - 依赖列表
    - `README.md` - 项目说明

11. **初始化数据库**：
    ```bash
    python manage.py migrate
    ```

12. **创建超级用户**（可选）：
    ```bash
    python manage.py createsuperuser
    ```

## 项目结构

### Basic 模板
```
myproject/
├── venv/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── tests.py
├── static/
├── media/
├── templates/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### API 模板
```
myproject/
├── venv/
├── config/
│   ├── settings/
│   │   ���── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── api/
│       ├── v1/
│       │   ├── urls.py
│       │   └── views.py
│       └── permissions.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 生成的配置示例

### .env 文件
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=myproject_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
```

### requirements.txt（API 模板）
```
Django==4.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
django-cors-headers==4.0.0
drf-yasg==1.21.5
psycopg2-binary==2.9.6
python-dotenv==1.0.0
```

### README.md
```markdown
# MyProject

Django project created with python-dev-assistant plugin.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints (API template)

- `/api/v1/users/` - User management
- `/api/v1/auth/login/` - Login
- `/api/v1/auth/refresh/` - Refresh token
- `/api/docs/` - API documentation
```

## 输出示例

### 成功创建
```
✓ Django 项目创建成功！

项目信息：
  名称: myproject
  模板: api
  位置: /path/to/myproject

已创建：
  ✓ 虚拟环境
  ✓ Django 项目
  ✓ 应用: users, api
  ✓ 配置文件
  ✓ 数据库迁移

下一步：
  1. cd myproject
  2. source venv/bin/activate
  3. python manage.py createsuperuser
  4. python manage.py runserver

访问：
  - 应用: http://127.0.0.1:8000/
  - 管理后台: http://127.0.0.1:8000/admin/
  - API 文档: http://127.0.0.1:8000/api/docs/
```

### 错误处理
```
✗ 错误：项目目录已存在

目录 'myproject' 已经存在。

建议：
  1. 使用不同的项目名称
  2. 删除现有目录：rm -rf myproject
  3. 或进入现有目录继续开发
```

## 实现提示

1. **使用 Bash 工具**执行所有命令
2. **使用 Write 工具**创建配置文件
3. **使用 Read 工具**读取模板文件
4. **错误处理**：捕获所有可能的错误并提供友好提示

## 配置文件支持

读取 `.claude/python-dev-assistant.local.md`：

```yaml
---
django_template: "api"
python_version: "3.11"
---
```

## 提示和技巧

1. **首次使用**：建议使用 basic 模板熟悉结构
2. **API 开发**：使用 api 模板快速搭建 REST API
3. **生产部署**：修改 `.env` 文件中的配置
4. **数据库**：API 模板默认使用 PostgreSQL，可改为 SQLite

## 相关命令

- `/py-flask` - 创建 Flask 项目
- `/py-check` - 检查代码质量
- `/py-docs` - 生成文档
