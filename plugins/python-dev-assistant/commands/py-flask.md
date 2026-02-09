---
name: py-flask
description: 创建 Flask 项目脚手架
argument-hint: "<project_name> [--template=basic|api|blueprint]"
allowed-tools: ["Bash", "Write", "Read", "Glob"]
---

# Flask 项目生成命令

快速创建 Flask 项目脚手架，支持多种项目模板。

## 使用方法

```bash
# 创建基础项目（单文件）
/py-flask myapp

# 创建 REST API 项目
/py-flask myapp --template=api

# 创建蓝图结构项目（模块化）
/py-flask myapp --template=blueprint
```

## 项目模板

### Basic（基础版）
- 单文件 Flask 应用
- 简单路由
- 模板支持
- 静态文件
- 适合小型项目和学习

### API（REST API 版）
- Flask + Flask-RESTful
- JWT 认证（Flask-JWT-Extended）
- CORS 支持
- SQLAlchemy ORM
- API 文档（Flask-RESTX）
- 应用工厂模式

### Blueprint（蓝图版）
- 模块化架构
- 蓝图组织
- 应用工厂模式
- 数据库迁移（Flask-Migrate）
- 完整的项目结构
- 适合大型项目

## 执行流程

1. **验证项目名称**：
   - 检查项目名称是否合法
   - 检查目录是否已存在

2. **读取配置**：
   - 检查 `.claude/python-dev-assistant.local.md`
   - 读取 `flask_template` 配置
   - 命令行参数优先

3. **检查依赖**：
   - Python 3.8+
   - pip 可用性

4. **创建项目目录**：
   ```bash
   mkdir myapp
   cd myapp
   ```

5. **创建虚拟环境**：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

6. **安装依赖**：

   **Basic:**
   ```bash
   pip install flask python-dotenv
   ```

   **API:**
   ```bash
   pip install flask flask-restful flask-jwt-extended flask-cors flask-sqlalchemy flask-migrate python-dotenv
   ```

   **Blueprint:**
   ```bash
   pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf python-dotenv
   ```

7. **创建项目结构**：
   根据模板创建相应的文件和目录

8. **生成配置文件**：
   - `.env`
   - `.gitignore`
   - `requirements.txt`
   - `README.md`
   - `config.py`

9. **初始化数据库**（API 和 Blueprint 模板）：
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## 项目结构

### Basic 模板
```
myapp/
├── venv/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**app.py 示例：**
```python
from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/hello')
def hello():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    app.run(debug=True)
```

### API 模板
```
myapp/
├── venv/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── models.py            # 数据模型
│   ├── extensions.py        # 扩展初始化
│   ├── config.py            # 配置
│   └── api/
│       ├── __init__.py
│       ├── auth.py          # 认证端点
│       ├── users.py         # 用户端点
│       └── resources.py     # 其他资源
├── migrations/
├── tests/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**应用工厂 (app/__init__.py)：**
```python
from flask import Flask
from .extensions import db, migrate, jwt, cors
from .config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # 注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
```

### Blueprint 模板
```
myapp/
├── venv/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── extensions.py
│   ├── config.py
│   ├── main/                # 主蓝图
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── forms.py
│   ├── auth/                # 认证蓝图
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── forms.py
│   ├── api/                 # API 蓝图
│   │   ├── __init__.py
│   │   └── views.py
│   └── templates/
│       ├── base.html
│       ├── main/
│       └── auth/
├── migrations/
├── tests/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 生成的配置示例

### .env 文件
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///app.db
# 或 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT (API 模板)
JWT_SECRET_KEY=your-jwt-secret-key
```

### config.py（API/Blueprint 模板）
```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### requirements.txt（API 模板）
```
Flask==2.3.0
Flask-RESTful==0.3.10
Flask-JWT-Extended==4.5.2
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.4
python-dotenv==1.0.0
```

### run.py（API/Blueprint 模板）
```python
from app import create_app, db
from app.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run()
```

## 示例代码

### API 端点示例 (app/api/users.py)
```python
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import User
from ..extensions import db

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

### 认证端点示例 (app/api/auth.py)
```python
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from . import api_bp
from ..models import User

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    return jsonify({'error': 'Invalid credentials'}), 401
```

## 输出示例

### 成功创建
```
✓ Flask 项目创建成功！

项目信息：
  名称: myapp
  模板: api
  位置: /path/to/myapp

已创建：
  ✓ 虚拟环境
  ✓ Flask 应用
  ✓ 应用工厂
  ✓ API 蓝图
  ✓ 配置文件
  ✓ 数据库迁移

下一步：
  1. cd myapp
  2. source venv/bin/activate
  3. flask db upgrade
  4. flask run

访问：
  - 应用: http://127.0.0.1:5000/
  - API: http://127.0.0.1:5000/api/

开发提示：
  - 使用 flask shell 进入交互式环境
  - 使用 flask db migrate 创建迁移
  - 查看 README.md 了解更多信息
```

### 错误处理
```
✗ 错误：Python 版本过低

当前版本: Python 3.7.0
需要版本: Python 3.8+

建议：
  1. 升级 Python: https://www.python.org/downloads/
  2. 使用 pyenv 管理多个 Python 版本
```

## 实现提示

1. **模板选择逻辑**：
   ```python
   template = args.get('template', config.get('flask_template', 'basic'))
   ```

2. **目录创建**：
   ```bash
   mkdir -p myapp/app/api
   mkdir -p myapp/app/templates
   mkdir -p myapp/tests
   ```

3. **文件生成**：
   使用 Write 工具创建所有必要的文件

4. **依赖安装**：
   ```bash
   pip install -r requirements.txt
   ```

## 配置文件支持

读取 `.claude/python-dev-assistant.local.md`：

```yaml
---
flask_template: "api"
python_version: "3.11"
---
```

## 提示和技巧

1. **选择模板**：
   - 学习/原型：使用 basic
   - REST API：使用 api
   - 大型应用：使用 blueprint

2. **数据库**：
   - 开发环境使用 SQLite
   - 生产环境使用 PostgreSQL/MySQL

3. **扩展**：
   - 根据需要添加更多 Flask 扩展
   - 参考 Flask 官方文档

4. **测试**：
   - 使用 pytest 编写测试
   - 运行 `pytest tests/`

## 相关命令

- `/py-django` - 创建 Django 项目
- `/py-check` - 检查代码质量
- `/py-docs` - 生成文档
