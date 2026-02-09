"""
符合 PEP 8 规范的 Python 代码示例

展示了良好的代码风格和最佳实践。
"""

import os
import sys
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from contextlib import contextmanager

# 模块级常量
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_VERSION = "v1"


@dataclass
class User:
    """用户数据类

    Attributes:
        id: 用户ID
        name: 用户名
        email: 邮箱地址
        role: 用户角色
    """
    id: int
    name: str
    email: str
    role: str = "user"

    def is_admin(self) -> bool:
        """检查用户是否为管理员"""
        return self.role == "admin"

    def __str__(self) -> str:
        """字符串表示"""
        return f"User({self.name}, {self.email})"


class UserManager:
    """用户管理器

    负责用户的创建、查询、更新和删除操作。
    """

    def __init__(self, db_connection: Optional[object] = None):
        """初始化用户管理器

        Args:
            db_connection: 数据库连接对象，可选
        """
        self._db = db_connection
        self._cache: Dict[int, User] = {}

    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户

        首先从缓存中查找，如果不存在则从数据库查询。

        Args:
            user_id: 用户ID

        Returns:
            User 对象，如果不存在返回 None

        Examples:
            >>> manager = UserManager()
            >>> user = manager.get_user(1)
            >>> print(user.name)
            'Alice'
        """
        # 先检查缓存
        if user_id in self._cache:
            return self._cache[user_id]

        # 从数据库查询
        user = self._fetch_from_db(user_id)
        if user:
            self._cache[user_id] = user

        return user

    def create_user(
        self,
        name: str,
        email: str,
        role: str = "user"
    ) -> User:
        """创建新用户

        Args:
            name: 用户名
            email: 邮箱地址
            role: 用户角色，默认为 "user"

        Returns:
            创建的 User 对象

        Raises:
            ValueError: 如果邮箱格式无效
        """
        if not self._validate_email(email):
            raise ValueError(f"无效的邮箱地址: {email}")

        user_id = self._generate_user_id()
        user = User(id=user_id, name=name, email=email, role=role)

        self._save_to_db(user)
        self._cache[user_id] = user

        return user

    def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[User]:
        """更新用户信息

        Args:
            user_id: 用户ID
            **kwargs: 要更新的字段

        Returns:
            更新后的 User 对象，如果用户不存在返回 None
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # 更新字段
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self._save_to_db(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """删除用户

        Args:
            user_id: 用户ID

        Returns:
            删除成功返回 True，用户不存在返回 False
        """
        if user_id not in self._cache:
            return False

        del self._cache[user_id]
        self._delete_from_db(user_id)
        return True

    def list_users(
        self,
        role: Optional[str] = None,
        limit: int = 100
    ) -> List[User]:
        """列出用户

        Args:
            role: 按角色过滤，可选
            limit: 返回数量限制

        Returns:
            用户列表
        """
        users = list(self._cache.values())

        if role:
            users = [u for u in users if u.role == role]

        return users[:limit]

    # 私有方法
    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        return '@' in email and '.' in email.split('@')[1]

    def _generate_user_id(self) -> int:
        """生成新的用户ID"""
        if not self._cache:
            return 1
        return max(self._cache.keys()) + 1

    def _fetch_from_db(self, user_id: int) -> Optional[User]:
        """从数据库获取用户"""
        # 模拟数据库查询
        return None

    def _save_to_db(self, user: User) -> None:
        """保存用户到数据库"""
        # 模拟数据库保存
        pass

    def _delete_from_db(self, user_id: int) -> None:
        """从数据库删除用户"""
        # 模拟数据库删除
        pass


def process_users(
    users: List[User],
    filter_role: Optional[str] = None
) -> Dict[str, List[str]]:
    """处理用户列表

    按角色分组用户名。

    Args:
        users: 用户列表
        filter_role: 可选的角色过滤器

    Returns:
        角色到用户名列表的字典
    """
    result: Dict[str, List[str]] = {}

    for user in users:
        if filter_role and user.role != filter_role:
            continue

        if user.role not in result:
            result[user.role] = []

        result[user.role].append(user.name)

    return result


@contextmanager
def timer(name: str):
    """计时上下文管理器

    Args:
        name: 操作名称

    Yields:
        None

    Examples:
        >>> with timer("数据处理"):
        ...     process_data()
        数据处理 耗时: 1.23秒
    """
    import time
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{name} 耗时: {end - start:.2f}秒")


def read_large_file(file_path: str):
    """逐行读取大文件

    使用生成器避免一次性加载整个文件到内存。

    Args:
        file_path: 文件路径

    Yields:
        文件的每一行（去除首尾空白）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()


def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """计算统计信息

    Args:
        numbers: 数字列表

    Returns:
        包含统计信息的字典

    Raises:
        ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("数字列表不能为空")

    return {
        'mean': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'count': len(numbers),
    }


def main():
    """主程序入口"""
    # 创建用户管理器
    manager = UserManager()

    # 创建用户
    alice = manager.create_user("Alice", "alice@example.com", "admin")
    bob = manager.create_user("Bob", "bob@example.com")

    # 查询用户
    user = manager.get_user(alice.id)
    print(f"找到用户: {user}")

    # 列出所有用户
    users = manager.list_users()
    print(f"总共 {len(users)} 个用户")

    # 按角色分组
    grouped = process_users(users)
    for role, names in grouped.items():
        print(f"{role}: {', '.join(names)}")

    # 使用计时器
    with timer("用户处理"):
        manager.list_users()


if __name__ == '__main__':
    main()
