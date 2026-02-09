#!/usr/bin/env python3
"""
哔哩哔哩视频下载器
使用 yt-dlp 下载 B站视频，支持选择画质、输出目录等功能。
"""

import sys
import json
import subprocess
import argparse
import os
from pathlib import Path

# 修复Windows控制台编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(description='哔哩哔哩视频下载器')
    parser.add_argument('url', help='B站视频URL或BV号')
    parser.add_argument('--quality', '-q', default='best',
                        choices=['best', '1080p', '720p', '480p', '360p'],
                        help='画质选择 (默认: best)')
    parser.add_argument('--output', '-o', default='downloads',
                        help='输出目录 (默认: downloads/)')
    parser.add_argument('--info', '-i', action='store_true',
                        help='仅显示视频信息，不下载')
    parser.add_argument('--page', '-p', type=int, default=None,
                        help='下载指定分P (从1开始)')
    return parser.parse_args()


def get_quality_format(quality):
    """画质对应的 yt-dlp 格式"""
    quality_map = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    }
    return quality_map.get(quality, 'best')


def build_ytdlp_args(args):
    """构建 yt-dlp 命令参数"""
    ytdlp_args = [
        'yt-dlp',
        '--no-warnings',
        '--encoding', 'utf-8',
    ]

    if args.info:
        # 仅获取信息
        ytdlp_args.extend([
            '--dump-json',
            '--skip-download',
        ])
    else:
        # 下载视频
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 输出文件名模板
        output_template = str(output_dir / '%(title)s_%(id)s.%(ext)s')

        ytdlp_args.extend([
            '-f', get_quality_format(args.quality),
            '--merge-output-format', 'mp4',
            '-o', output_template,
        ])

        # 指定分P
        if args.page is not None:
            ytdlp_args.extend(['--playlist-items', str(args.page)])

    ytdlp_args.append(args.url)
    return ytdlp_args


def get_video_info(url):
    """获取视频信息"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-warnings', '--encoding', 'utf-8', url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout:
            info = json.loads(result.stdout)
            return info
        return None
    except Exception as e:
        return None


def format_duration(seconds):
    """格式化时长"""
    if not seconds:
        return "未知"
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_filesize(bytes_size):
    """格式化文件大小"""
    if not bytes_size:
        return "未知"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def main():
    args = parse_args()

    # 如果只是查看信息
    if args.info:
        info = get_video_info(args.url)
        if info:
            print("\n" + "="*50)
            print(f"标题: {info.get('title', '未知')}")
            print(f"UP主: {info.get('uploader', '未知')}")
            print(f"时长: {format_duration(info.get('duration'))}")
            print(f"播放量: {info.get('view_count', '未知'):,}")
            print(f"发布时间: {info.get('upload_date', '未知')}")
            print(f"\n描述: {info.get('description', '无')[:100]}...")

            # 显示可用画质
            formats = info.get('formats', [])
            heights = set()
            for f in formats:
                if f.get('vcodec') != 'none':
                    h = f.get('height')
                    if h:
                        heights.add(h)
            if heights:
                print(f"\n可用画质: {', '.join(sorted(str(h) + 'p' for h in heights))}")

            # 分P信息
            if info.get('entries'):
                print(f"\n合集/分P数量: {len(info['entries'])} 个视频")

            print("="*50 + "\n")
        else:
            print("无法获取视频信息，请检查URL是否正确")
            sys.exit(1)
        return

    # 执行下载
    ytdlp_args = build_ytdlp_args(args)

    print(f"\n开始下载: {args.url}")
    print(f"画质: {args.quality}")
    print(f"输出目录: {args.output}/")
    print("-" * 40)

    result = subprocess.run(ytdlp_args)

    if result.returncode == 0:
        print("\n下载完成！")
    else:
        print("\n下载失败，请检查网络或URL")
        sys.exit(1)


if __name__ == '__main__':
    main()
