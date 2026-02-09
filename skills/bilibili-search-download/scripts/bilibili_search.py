#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哔哩哔哩视频搜索和下载工具 (简化版)
直接使用 B站 API 搜索，无需 bilibili-api 依赖
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
import urllib.parse
import urllib.request
from typing import List, Dict


# BBDown 路径（根据实际情况修改）
BBDOWN_PATH = r"C:\Users\13608\Downloads\BBDown\BBDown.exe"


def format_number(num):
    """格式化数字显示"""
    if num >= 100000000:
        return f"{num/100000000:.1f}亿"
    elif num >= 10000:
        return f"{num/10000:.1f}万"
    else:
        return str(num)


def format_duration(seconds):
    """格式化时长显示"""
    minutes = seconds // 60
    secs = seconds % 60
    if minutes >= 60:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def search_videos(keyword: str, limit: int = 10) -> List[Dict]:
    """
    使用 B站 API 搜索视频

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量

    Returns:
        搜索结果列表
    """
    print(f"\n{'='*60}")
    print(f"搜索关键词: {keyword}")
    print(f"{'='*60}\n")

    # B站搜索 API
    api_url = "https://api.bilibili.com/x/web-interface/search/type"

    # 构建请求参数
    params = {
        "search_type": "video",  # 搜索类型：视频
        "keyword": keyword,
        "page": 1,
    }

    try:
        # 构建 URL
        url = f"{api_url}?{urllib.parse.urlencode(params)}"

        # 发送请求
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.bilibili.com"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        # 检查响应状态
        if data.get("code") != 0:
            print(f"API 错误: {data.get('message', '未知错误')}")
            return []

        videos = data.get("data", {}).get("result", [])

        if not videos:
            print("未找到相关视频")
            return []

        # 解析视频信息（B站 API 返回的是 JSON 字符串）
        results = []
        for i, video in enumerate(videos[:limit], 1):
            # 解析嵌套的 JSON 字符串
            try:
                video_data = json.loads(video.get("lit_title", "{}"))
            except:
                video_data = {}

            title = video.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", "")
            # 去除 HTML 标签
            import re
            title = re.sub(r'<[^>]+>', '', title)

            author = video.get("author", "未知UP主")
            play = format_number(int(video.get("play", 0)))
            duration = video.get("duration", "0:00")
            bvid = video.get("bvid", "")

            print(f"  [{i}] {title}")
            print(f"      UP主: {author:15s}  |  播放: {play:>6s}  |  时长: {duration:>8s}  |  BV: {bvid}")
            print()

            results.append({
                "index": i,
                "title": title,
                "author": author,
                "play": play,
                "duration": duration,
                "bvid": bvid,
                "url": f"https://www.bilibili.com/video/{bvid}"
            })

        return results

    except urllib.error.URLError as e:
        print(f"网络请求失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return []
    except Exception as e:
        print(f"搜索出错: {e}")
        return []


def download_video(bvid: str, quality: str = "tv", output: str = "downloads/"):
    """
    使用 BBDown 下载视频

    Args:
        bvid: 视频BV号
        quality: 画质 (tv/app/web)
        output: 输出目录
    """
    # 检查 BBDown 是否存在
    if not Path(BBDOWN_PATH).exists():
        print(f"\n错误: 找不到 BBDown.exe")
        print(f"预期路径: {BBDOWN_PATH}")
        print("请修改脚本中的 BBDOWN_PATH 变量")
        return False

    print(f"\n{'='*60}")
    print(f"开始下载: {bvid}")
    print(f"{'='*60}\n")

    # 构建 BBDown 命令
    cmd = [BBDOWN_PATH, bvid]

    # 添加画质参数
    if quality == "tv":
        cmd.append("-tv")
    elif quality == "app":
        cmd.append("-app")

    # 添加工作目录参数
    if output:
        cmd.extend(["--work-dir", output])

    try:
        # 执行下载
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=600  # 10分钟超时
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"\n✅ 下载完成!")
            print(f"文件位置: {output}")
            return True
        else:
            print(f"\n❌ 下载失败 (返回码: {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print("\n❌ 下载超时 (10分钟)")
        return False
    except Exception as e:
        print(f"\n❌ 下载出错: {e}")
        return False


def show_video_info(bvid: str):
    """显示视频信息"""
    if not Path(BBDOWN_PATH).exists():
        print(f"错误: 找不到 BBDown.exe")
        return

    cmd = [BBDOWN_PATH, bvid, "--info"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30
        )
        print(result.stdout)
    except Exception as e:
        print(f"获取视频信息失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="哔哩哔哩视频搜索和下载工具 (简化版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  搜索视频:     python bilibili_search.py "Python教程"
  搜索20条:     python bilibili_search.py "AI" --limit 20
  下载视频:     python bilibili_search.py "BV1xx411c7mM" --download
  查看信息:     python bilibili_search.py "BV1xx411c7mM" --info

注意: 本工具直接使用 B站 API 搜索，无需安装 bilibili-api
        """
    )

    parser.add_argument("input", help="搜索关键词或BV号")
    parser.add_argument("--limit", type=int, default=10, help="返回结果数量 (默认: 10)")
    parser.add_argument("--download", action="store_true", help="下载模式（输入为BV号）")
    parser.add_argument("--info", action="store_true", help="查看视频信息")
    parser.add_argument("--quality", default="tv", choices=["tv", "app", "web"],
                       help="下载画质: tv(最高)/app/web")
    parser.add_argument("--output", default="downloads/", help="输出目录")

    args = parser.parse_args()

    # 判断是搜索还是下载
    if args.input.startswith("BV"):
        # BV号模式
        if args.info:
            show_video_info(args.input)
        elif args.download:
            download_video(args.input, args.quality, args.output)
        else:
            print("检测到BV号，请使用 --download 下载或 --info 查看信息")
    else:
        # 搜索模式
        results = search_videos(
            keyword=args.input,
            limit=args.limit
        )

        if results:
            print(f"\n提示: 使用以下命令下载视频")
            print(f'python bilibili_search.py "{results[0]["bvid"]}" --download')
            print(f"\n或直接使用 BBDown:")
            print(f'"{BBDOWN_PATH}" {results[0]["bvid"]} -tv')


if __name__ == "__main__":
    main()
