---
name: Django/Flask 项目架构模式
description: This skill should be used when the user asks about "Django 项目结构", "Flask 项目架构", "Django 最佳实践", "Flask 最佳实践", "Web 框架设计", "Django 应用组织", "Flask 蓝图", or mentions "Django REST Framework", "Flask-SQLAlchemy". Provides comprehensive guidance on Django and Flask project architecture and best practices.
version: 0.1.0
---

# Django/Flask 项目架构模式

## 概述

本技能提供 Django 和 Flask Web 框架的项目架构设计、最佳实践和常见模式指南。帮助开发者构建可维护、可扩展的 Web 应用。

## Django 项目架构

### 标准项目结构

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   └── blog/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       └── ...
├── static/
├── media/
├── templates/
├── requirements.txt
└── .env
```

### 应用组织原则

**按功能模块划分应用：**

每个应用应该是一个独立的功能模块，遵循单一职责原则。

```python
# 好的应用划分
apps/
├── users/          # 用户管理
├── blog/           # 博客功能
├── comments/       # 评论系统
├── notifications/  # 通知系统
└── api/            # API 接口

# 避免
apps/
├── models/         # 不要按技术层划分
├── views/
└── serializers/
```

### 设置文件组织

**使用多环境配置：**

```
myproject/settings/
├── __init__.py
├── base.py          # 基础配置
├── development.py   # 开发环境
├── production.py    # 生产环境
└── testing.py       # 测试环境
```

**base.py 示例：**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方应用
    'rest_framework',
    'corsheaders',
    # 本地应用
    'apps.users',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# 静态文件
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**development.py 示例：**
```python
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 开发环境使用 SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 邮件后端（控制台输出）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 模型设计最佳实践

**使用抽象基类：**

```python
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """时间戳抽象基类"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    """软删除抽象基类"""
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """软删除"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """硬删除"""
        super().delete()

# 使用抽象基类
class Article(TimeStampedModel, SoftDeleteModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['author', 'created_at']),
        ]

    def __str__(self):
        return self.title
```

**使用 Manager 和 QuerySet：**

```python
from django.db import models

class PublishedQuerySet(models.QuerySet):
    """已发布文章查询集"""
    def published(self):
        return self.filter(status='published')

    def by_author(self, author):
        return self.filter(author=author)

class ArticleManager(models.Manager):
    """文章管理器"""
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='draft')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    objects = ArticleManager()

    def __str__(self):
        return self.title

# 使用
Article.objects.published()
Article.objects.published().by_author(user)
```

### Django REST Framework 架构

**序列化器组织：**

```python
from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'created_at']
        read_only_fields = ['created_at']

class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器（简化版）"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'author_name', 'created_at', 'comment_count']

class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器（完整版）"""
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'comments', 'created_at', 'updated_at']

class ArticleCreateSerializer(serializers.ModelSerializer):
    """文章创建序列化器"""
    class Meta:
        model = Article
        fields = ['title', 'content']

    def create(self, validated_data):
        # 自动设置作者
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
```

**视图集组织：**

```python
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class ArticleViewSet(viewsets.ModelViewSet):
    """文章视图集"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """根据用户权限返回不同的查询集"""
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.published()

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'create':
            return ArticleCreateSerializer
        return ArticleDetailSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布文章"""
        article = self.get_object()
        article.status = 'published'
        article.save()
        return Response({'status': 'published'})

    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        """获取当前用户的文章"""
        articles = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
```

## Flask 项目架构

### 应用工厂模式

**推荐的项目结构：**

```
myapp/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── models.py            # 数据模型
│   ├── extensions.py        # 扩展初始化
│   ├── config.py            # 配置
│   ├── api/                 # API 蓝图
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── posts.py
│   ├── auth/                # 认证蓝图
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── forms.py
│   └── templates/
├── migrations/              # 数据库迁移
├── tests/
├── requirements.txt
├── config.py
└── run.py
```

**应用工厂 (app/__init__.py)：**

```python
from flask import Flask
from .extensions import db, migrate, jwt, cors
from .config import config

def create_app(config_name='development'):
    """应用工厂函数"""
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

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 注册错误处理器
    register_error_handlers(app)

    # 注册 CLI 命令
    register_commands(app)

    return app

def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500

def register_commands(app):
    """注册 CLI 命令"""
    @app.cli.command()
    def init_db():
        """初始化数据库"""
        db.create_all()
        print('Database initialized.')
```

**扩展初始化 (app/extensions.py)：**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 创建扩展实例（不初始化）
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
```

**配置文件 (app/config.py)：**

```python
import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### 蓝图组织

**API 蓝图 (app/api/__init__.py)：**

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import users, posts
```

**用户 API (app/api/users.py)：**

```python
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import User
from ..extensions import db

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取用户列表"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取单个用户"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.get_json()

    # 验证数据
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400

    # 检查用户是否存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    # 创建用户
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户"""
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'email' in data:
        user.email = data['email']

    db.session.commit()
    return jsonify(user.to_dict())
```

### 模型设计

**基础模型 (app/models.py)：**

```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class TimestampMixin:
    """时间戳混入类"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(db.Model, TimestampMixin):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)

    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model, TimestampMixin):
    """文章模型"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<Post {self.title}>'
```

## 通用最佳实践

### 1. 环境变量管理

使用 `.env` 文件管理敏感配置：

```bash
# .env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
JWT_SECRET_KEY=your-jwt-secret
DEBUG=True
```

使用 `python-dotenv` 加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. 数据库迁移

**Django：**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Flask：**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. 测试组织

**Django 测试：**
```python
from django.test import TestCase
from .models import Article

class ArticleModelTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content"
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
```

**Flask 测��：**
```python
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
```

### 4. API 文档

使用 Swagger/OpenAPI 文档化 API：

**Django REST Framework：**
```python
# settings.py
INSTALLED_APPS += ['drf_yasg']

# urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger')),
]
```

**Flask：**
```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
app.register_blueprint(swaggerui_blueprint)
```

## 附加资源

### 参考文件

详细的架构模式和示例，请参考：

- **`references/django-patterns.md`** - Django 设计模式
- **`references/flask-patterns.md`** - Flask 设计模式
- **`references/api-design.md`** - RESTful API 设计指南

### 示例文件

完整的项目示例：

- **`examples/django-project/`** - Django 项目示例
- **`examples/flask-project/`** - Flask 项目示例

## 总结

构建优秀 Web 应用的关键：

1. **清晰的项目结构** - 按功能模块组织
2. **配置管理** - 多环境配置分离
3. **数据库设计** - 使用抽象基类和 Manager
4. **API 设计** - RESTful 规范，版本控制
5. **测试覆盖** - 单元测试和集成测试
6. **文档完善** - API 文档和代码注释
7. **安全性** - 认证授权，输入验证

选择 Django 还是 Flask 取决于项目需求：
- **Django**：功能完整，适合大型项目
- **Flask**：轻量灵活，适合小型项目和微服务
