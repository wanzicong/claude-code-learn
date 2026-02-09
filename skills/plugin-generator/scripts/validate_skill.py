#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能验证脚本
验证技能结构和内容的完整性
"""

import sys
import io
import yaml
from pathlib import Path
from typing import List, Tuple

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class SkillValidator:
    """技能验证器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """执行完整验证"""
        print(f"验证技能: {self.skill_path}")

        # 检查目录存在
        if not self.skill_path.exists():
            self.errors.append(f"技能目录不存在: {self.skill_path}")
            return False

        # 验证 SKILL.md
        self._validate_skill_md()

        # 验证目录结构
        self._validate_structure()

        # 验证脚本
        self._validate_scripts()

        # 输出结果
        self._print_results()

        return len(self.errors) == 0

    def _validate_skill_md(self):
        """验证 SKILL.md"""
        skill_md = self.skill_path / 'SKILL.md'

        if not skill_md.exists():
            self.errors.append("缺少 SKILL.md 文件")
            return

        try:
            content = skill_md.read_text(encoding='utf-8')

            # 检查 YAML 前置元数据
            if not content.startswith('---'):
                self.errors.append("SKILL.md 缺少 YAML 前置元数据")
                return

            # 提取 YAML
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append("YAML 前置元数据格式错误")
                return

            yaml_content = parts[1].strip()
            try:
                metadata = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                self.errors.append(f"YAML 解析错误: {e}")
                return

            # 验证必需字段
            if 'name' not in metadata:
                self.errors.append("YAML 缺少 'name' 字段")
            if 'description' not in metadata:
                self.errors.append("YAML 缺少 'description' 字段")

            # 验证描述长度
            if 'description' in metadata:
                desc = metadata['description']
                if len(desc) < 50:
                    self.warnings.append("描述过短，建议至少 50 字符")
                if len(desc) > 500:
                    self.warnings.append("描述过长，建议不超过 500 字符")

            # 验证正文
            body = parts[2].strip()
            if len(body) < 100:
                self.warnings.append("SKILL.md 正文内容过少")

            print("  ✓ SKILL.md 格式正确")

        except Exception as e:
            self.errors.append(f"读取 SKILL.md 失败: {e}")

    def _validate_structure(self):
        """验证目录结构"""
        # 检查推荐目录
        recommended_dirs = ['scripts', 'references', 'assets']
        found_dirs = []

        for dir_name in recommended_dirs:
            dir_path = self.skill_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                found_dirs.append(dir_name)

        if not found_dirs:
            self.warnings.append("未找到推荐目录 (scripts, references, assets)")
        else:
            print(f"  ✓ 找到目录: {', '.join(found_dirs)}")

    def _validate_scripts(self):
        """验证脚本"""
        scripts_dir = self.skill_path / 'scripts'

        if not scripts_dir.exists():
            return

        # 查找 Python 脚本
        py_files = list(scripts_dir.glob('*.py'))

        if py_files:
            print(f"  ✓ 找到 {len(py_files)} 个 Python 脚本")

            # 检查 requirements.txt
            requirements = scripts_dir / 'requirements.txt'
            if not requirements.exists():
                self.warnings.append("建议添加 requirements.txt")

    def _print_results(self):
        """输出验证结果"""
        print("\n" + "="*50)

        if self.errors:
            print("❌ 错误:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("✅ 验证通过！技能结构完整。")
        elif not self.errors:
            print("\n✅ 验证通过（有警告）")
        else:
            print("\n❌ 验证失败")

        print("="*50)

def main():
    if len(sys.argv) < 2:
        print("用法: python validate_skill.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path)

    success = validator.validate()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
