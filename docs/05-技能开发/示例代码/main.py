#!/usr/bin/env python3
"""
示例脚本：文件处理工具

用法：
    python main.py --input <输入文件> --output <输出文件> [选项]

示例：
    python main.py --input data.txt --output result.txt
    python main.py --input data.txt --output result.txt --verbose
    python main.py --input data.txt --output result.txt --format json

功能：
    - 读取输入文件
    - 处理文件内容
    - 保存到输出文件
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any

# 版本信息
__version__ = "1.0.0"
__author__ = "Your Name"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='文件处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 必需参数
    parser.add_argument(
        '--input',
        required=True,
        help='输入文件路径'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='输出文件路径'
    )

    # 可选参数
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='输出格式（默认：text）'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    # 验证输入
    input_path = Path(args.input)
    if not input_path.exists():
        error(f"输入文件不存在: {args.input}")

    if not input_path.is_file():
        error(f"输入路径不是文件: {args.input}")

    # 执行主要逻辑
    try:
        if args.verbose:
            info(f"读取文件: {args.input}")

        content = read_file(input_path)

        if args.verbose:
            info(f"处理内容（{len(content)} 字符）")

        result = process_content(content, args.format)

        if args.verbose:
            info(f"保存结果到: {args.output}")

        save_result(result, args.output, args.format)

        success(f"处理完成！输出已保存到 {args.output}")

    except Exception as e:
        error(f"处理失败: {e}")


def read_file(file_path: Path) -> str:
    """
    读取文件内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容字符串

    Raises:
        IOError: 文件读取失败
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(file_path, 'r', encoding='gbk') as f:
            return f.read()


def process_content(content: str, format_type: str) -> Any:
    """
    处理文件内容

    Args:
        content: 原始内容
        format_type: 输出格式类型

    Returns:
        处理后的内容
    """
    # 示例：转换为大写
    processed = content.upper()

    if format_type == 'json':
        return {
            'original_length': len(content),
            'processed_length': len(processed),
            'content': processed
        }
    elif format_type == 'csv':
        lines = processed.split('\n')
        return '\n'.join([f'"{line}"' for line in lines])
    else:
        return processed


def save_result(result: Any, output_path: str, format_type: str):
    """
    保存处理结果

    Args:
        result: 处理结果
        output_path: 输出文件路径
        format_type: 输出格式类型
    """
    output = Path(output_path)

    # 确保输出目录存在
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, 'w', encoding='utf-8') as f:
        if format_type == 'json':
            json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            f.write(str(result))


# 辅助函数：彩色输出
def error(message: str):
    """打印错误信息并退出"""
    print(f"\033[0;31m错误: {message}\033[0m", file=sys.stderr)
    sys.exit(1)


def success(message: str):
    """打印成功信息"""
    print(f"\033[0;32m✓ {message}\033[0m")


def info(message: str):
    """打印信息"""
    print(f"\033[0;34mℹ {message}\033[0m")


def warning(message: str):
    """打印警告信息"""
    print(f"\033[1;33m⚠ {message}\033[0m")


if __name__ == '__main__':
    main()
