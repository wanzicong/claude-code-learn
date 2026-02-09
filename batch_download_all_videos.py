# -*- coding: utf-8 -*-
"""
基于已有的视频列表，批量下载视频并生成笔记
使用现有的工具：yt-dlp + whisper + Claude
"""
import sys
import json
import subprocess
import time
from pathlib import Path

# 设置UTF-8编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置路径
VIDEO_LIST_FILE = Path(r"C:\Users\13608\.claude\skills\bilibili-uploader\docs\小天fotos_videos.json")
DOWNLOAD_DIR = Path(r"C:\Users\13608\.claude\skills\bilibili-download\downloads")
SUBTITLE_DIR = Path(r"C:\Users\13608\.claude\skills\local-video-notes\docs")
NOTES_DIR = Path("docs")

# 确保目录存在
NOTES_DIR.mkdir(parents=True, exist_ok=True)


def load_video_list():
    """加载视频列表"""
    if not VIDEO_LIST_FILE.exists():
        print(f"错误：视频列表文件不存在: {VIDEO_LIST_FILE}")
        return None

    with open(VIDEO_LIST_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def check_video_downloaded(bvid):
    """检查视频是否已下载"""
    video_files = list(DOWNLOAD_DIR.glob(f"*{bvid}*.mp4"))
    return len(video_files) > 0


def check_subtitle_extracted(bvid):
    """检查字幕是否已提取"""
    subtitle_files = list(SUBTITLE_DIR.glob(f"*{bvid}*_subtitle.json"))
    return len(subtitle_files) > 0


def check_note_generated(bvid):
    """检查笔记是否已生成"""
    note_files = list(NOTES_DIR.glob(f"*{bvid}*.md"))
    # 排除汇总文档
    note_files = [f for f in note_files if '汇总' not in f.name and 'UP主' not in f.name]
    return len(note_files) > 0


def download_video(bvid, title):
    """下载视频"""
    url = f"https://www.bilibili.com/video/{bvid}"
    print(f"\n  [1/3] 下载视频...")

    try:
        cmd = [
            'yt-dlp',
            url,
            '-o', str(DOWNLOAD_DIR / '%(title)s_%(id)s.%(ext)s'),
            '--merge-output-format', 'mp4',
            '-f', 'bestvideo+bestaudio/best'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, encoding='utf-8', errors='ignore')

        if result.returncode == 0:
            print(f"    ✓ 视频下载成功")
            return True
        else:
            print(f"    ✗ 视频下载失败")
            return False

    except Exception as e:
        print(f"    ✗ 下载出错: {e}")
        return False


def extract_subtitle(bvid):
    """提取字幕"""
    print(f"\n  [2/3] 提取字幕...")

    # 查找视频文件
    video_files = list(DOWNLOAD_DIR.glob(f"*{bvid}*.mp4"))
    if not video_files:
        print(f"    ✗ 找不到视频文件")
        return False

    video_path = str(video_files[0])

    try:
        cmd = [
            'python',
            r'C:\Users\13608\.claude\skills\local-video-notes\scripts\extract_subtitle.py',
            video_path,
            '--language', 'zh',
            '--model', 'base'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, encoding='utf-8', errors='ignore')

        if result.returncode == 0:
            print(f"    ✓ 字幕提取成功")
            return True
        else:
            print(f"    ✗ 字幕提取失败")
            return False

    except Exception as e:
        print(f"    ✗ 提取出错: {e}")
        return False


def main():
    """主函数"""
    print("=" * 80)
    print("批量下载视频并生成笔记")
    print("=" * 80)

    # 1. 加载视频列表
    data = load_video_list()
    if not data:
        return

    uploader = data.get('uploader', {})
    videos = data.get('videos', [])

    print(f"\nUP主: {uploader.get('name', '未知')}")
    print(f"视频总数: {len(videos)}")

    # 2. 统计状态
    downloaded = 0
    subtitled = 0
    noted = 0

    for v in videos:
        bvid = v['bvid']
        if check_video_downloaded(bvid):
            downloaded += 1
        if check_subtitle_extracted(bvid):
            subtitled += 1
        if check_note_generated(bvid):
            noted += 1

    print(f"\n当前状态:")
    print(f"  已下载视频: {downloaded}/{len(videos)}")
    print(f"  已提取字幕: {subtitled}/{len(videos)}")
    print(f"  已生成笔记: {noted}/{len(videos)}")

    # 3. 处理未完成的视频
    pending_videos = []
    for v in videos:
        bvid = v['bvid']
        if not check_note_generated(bvid):
            pending_videos.append(v)

    if not pending_videos:
        print(f"\n✓ 所有视频都已处理完成！")
        return

    print(f"\n待处理视频: {len(pending_videos)}")
    print("\n" + "=" * 80)

    # 4. 批量处理
    success_count = 0
    failed_videos = []

    for i, v in enumerate(pending_videos, 1):
        bvid = v['bvid']
        title = v['title']

        print(f"\n[{i}/{len(pending_videos)}] {title}")
        print(f"  BV号: {bvid}")
        print(f"  链接: https://www.bilibili.com/video/{bvid}")

        try:
            # 检查是否已下载
            if not check_video_downloaded(bvid):
                if not download_video(bvid, title):
                    failed_videos.append({'bvid': bvid, 'title': title, 'reason': '下载失败'})
                    continue
                time.sleep(2)
            else:
                print(f"\n  [1/3] 视频已下载，跳过")

            # 检查是否已提取字幕
            if not check_subtitle_extracted(bvid):
                if not extract_subtitle(bvid):
                    failed_videos.append({'bvid': bvid, 'title': title, 'reason': '字幕提取失败'})
                    continue
                time.sleep(2)
            else:
                print(f"\n  [2/3] 字幕已提取，跳过")

            # 笔记生成需要手动处理
            print(f"\n  [3/3] 笔记生成 - 待处理")
            print(f"    字幕文件: {list(SUBTITLE_DIR.glob(f'*{bvid}*_subtitle.json'))[0]}")

            success_count += 1

        except Exception as e:
            print(f"\n  ✗ 处理失败: {e}")
            failed_videos.append({'bvid': bvid, 'title': title, 'reason': str(e)})

        # 避免请求过快
        time.sleep(3)

    # 5. 输出统计
    print("\n" + "=" * 80)
    print("处理完成！")
    print("=" * 80)
    print(f"成功: {success_count}/{len(pending_videos)}")
    print(f"失败: {len(failed_videos)}/{len(pending_videos)}")

    if failed_videos:
        print(f"\n失败的视频:")
        for v in failed_videos:
            print(f"  - {v['title']} ({v['bvid']}) - {v['reason']}")

    print(f"\n下一步:")
    print(f"1. 运行 check_notes_status.py 查看待生成笔记的视频")
    print(f"2. 使用Claude为每个视频生成笔记")


if __name__ == '__main__':
    main()
