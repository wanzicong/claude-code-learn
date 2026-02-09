# -*- coding: utf-8 -*-
"""
B站UP主视频批量处理完整工作流
功能：获取视频列表 → 下载视频 → 提取字幕 → 生成笔记
"""
import json
import subprocess
import time
import sys
import re
from pathlib import Path
from datetime import datetime

# 设置输出编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# 配置路径
BILIBILI_UPLOADER_DIR = r"C:\Users\13608\.claude\skills\bilibili-uploader"
BILIBILI_DOWNLOAD_DIR = r"C:\Users\13608\.claude\skills\bilibili-download"
BILIBILI_NOTES_DIR = r"C:\Users\13608\.claude\skills\bilibili-notes"
LOCAL_VIDEO_NOTES_DIR = r"C:\Users\13608\.claude\skills\local-video-notes"
DOWNLOAD_DIR = Path(BILIBILI_DOWNLOAD_DIR) / "downloads"
SUBTITLE_DIR = Path(LOCAL_VIDEO_NOTES_DIR) / "docs"
NOTES_DIR = Path("docs")

def get_uploader_videos(uid, limit=999):
    """获取UP主的视频列表"""
    print(f"\n{'='*80}")
    print(f"步骤1：获取UP主视频列表 (UID: {uid})")
    print(f"{'='*80}\n")

    cmd = [
        'python',
        str(Path(BILIBILI_UPLOADER_DIR) / 'scripts' / 'bilibili_uploader.py'),
        uid,
        str(limit),
        '--sort', 'pubtime',
        '--order', 'desc'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=BILIBILI_UPLOADER_DIR, encoding='utf-8')

    if result.returncode != 0:
        print(f"错误：获取视频列表失败")
        return None

    # 读取生成的JSON文件
    json_files = list(Path(BILIBILI_UPLOADER_DIR / "docs").glob("*_videos.json"))
    if not json_files:
        print("错误：找不到视频列表JSON文件")
        return None

    with open(json_files[0], 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ 成功获取 {len(data['videos'])} 个视频")
    return data

def download_and_extract_subtitles(videos):
    """下载视频并提取字幕"""
    print(f"\n{'='*80}")
    print(f"步骤2：批量下载视频并提取字幕")
    print(f"{'='*80}\n")

    success_count = 0
    failed_videos = []

    for i, video in enumerate(videos, 1):
        bvid = video['bvid']
        title = video['title']
        url = f"https://www.bilibili.com/video/{bvid}"

        print(f"\n[{i}/{len(videos)}] {title}")
        print(f"BV号: {bvid}")

        try:
            # 检查是否已有字幕文件
            subtitle_files = list(SUBTITLE_DIR.glob(f"*{bvid}*_subtitle.json"))
            if subtitle_files:
                print("✓ 字幕文件已存在，跳过")
                success_count += 1
                continue

            # 检查CC字幕
            print("  [1/3] 检查CC字幕...")
            subtitle_cmd = [
                'python',
                str(Path(BILIBILI_NOTES_DIR) / 'scripts' / 'bilibili_subtitle.py'),
                url,
                'api'
            ]
            result = subprocess.run(subtitle_cmd, capture_output=True, text=True, timeout=60, cwd=BILIBILI_NOTES_DIR, encoding='utf-8')

            has_cc_subtitle = False
            if result.returncode == 0 and result.stdout:
                try:
                    output_data = json.loads(result.stdout)
                    if output_data.get('transcript') and len(output_data['transcript']) > 0:
                        has_cc_subtitle = True
                        print("  ✓ 找到CC字幕")
                        success_count += 1
                        continue
                except json.JSONDecodeError:
                    pass

            print("  ⚠ 无CC字幕，需要下载视频")

            # 下载视频
            print("  [2/3] 下载视频...")
            video_files = list(DOWNLOAD_DIR.glob(f"*{bvid}*.mp4"))
            if not video_files:
                download_cmd = [
                    'python',
                    str(Path(BILIBILI_DOWNLOAD_DIR) / 'scripts' / 'bilibili_download.py'),
                    url,
                    '--quality', 'best'
                ]
                result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=600, cwd=BILIBILI_DOWNLOAD_DIR, encoding='utf-8')

                if result.returncode != 0:
                    print("  ✗ 下载失败")
                    failed_videos.append({'bvid': bvid, 'title': title, 'reason': '下载失败'})
                    continue

                video_files = list(DOWNLOAD_DIR.glob(f"*{bvid}*.mp4"))

            if not video_files:
                print("  ✗ 找不到视频文件")
                failed_videos.append({'bvid': bvid, 'title': title, 'reason': '找不到视频文件'})
                continue

            print("  ✓ 视频已准备")

            # Whisper识别
            print("  [3/3] Whisper语音识别...")
            video_path = str(video_files[0])
            whisper_cmd = [
                'python',
                str(Path(LOCAL_VIDEO_NOTES_DIR) / 'scripts' / 'extract_subtitle.py'),
                video_path,
                '--language', 'zh',
                '--model', 'base'
            ]
            result = subprocess.run(whisper_cmd, capture_output=True, text=True, timeout=1800, cwd=LOCAL_VIDEO_NOTES_DIR, encoding='utf-8')

            if result.returncode != 0:
                print("  ✗ Whisper识别失败")
                failed_videos.append({'bvid': bvid, 'title': title, 'reason': 'Whisper失败'})
                continue

            print("  ✓ 字幕提取完成")
            success_count += 1
            time.sleep(2)

        except Exception as e:
            print(f"  ✗ 错误: {str(e)}")
            failed_videos.append({'bvid': bvid, 'title': title, 'reason': str(e)})

    print(f"\n{'='*80}")
    print(f"字幕提取完成：成功 {success_count}/{len(videos)}")
    if failed_videos:
        print(f"失败 {len(failed_videos)} 个：")
        for v in failed_videos:
            print(f"  - {v['title']} ({v['bvid']}): {v['reason']}")
    print(f"{'='*80}\n")

    return success_count, failed_videos

def generate_notes_for_all_videos():
    """为所有已提取字幕的视频生成笔记"""
    print(f"\n{'='*80}")
    print(f"步骤3：生成结构化笔记")
    print(f"{'='*80}\n")

    # 获取所有字幕文件
    subtitle_files = list(SUBTITLE_DIR.glob("*_subtitle.json"))
    print(f"找到 {len(subtitle_files)} 个字幕文件\n")

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    generated_count = 0

    for i, subtitle_file in enumerate(subtitle_files, 1):
        print(f"[{i}/{len(subtitle_files)}] 处理: {subtitle_file.stem}")

        # 检查是否已有笔记
        note_name = subtitle_file.stem.replace('_subtitle', '')
        note_file = NOTES_DIR / f"笔记_{note_name}.md"

        if note_file.exists():
            print("  ✓ 笔记已存在，跳过\n")
            continue

        # 读取字幕
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            subtitle_data = json.load(f)

        # 这里需要调用Claude来生成笔记
        # 由于这是自动化脚本，实际使用时需要集成Claude API
        print("  ⚠ 需要Claude生成笔记（请手动处理或集成API）\n")

    print(f"{'='*80}")
    print(f"笔记生成提示：")
    print(f"  - 已提取 {len(subtitle_files)} 个视频的字幕")
    print(f"  - 字幕文件位置: {SUBTITLE_DIR}")
    print(f"  - 请使用Claude为每个字幕文件生成结构化笔记")
    print(f"  - 笔记保存位置: {NOTES_DIR}")
    print(f"{'='*80}\n")

def main():
    """主函数"""
    print("\n" + "="*80)
    print("B站UP主视频批量处理完整工作流")
    print("="*80)

    # 配置
    UID = "28554995"  # UP主UID
    LIMIT = 999  # 获取视频数量

    # 步骤1：获取视频列表
    data = get_uploader_videos(UID, LIMIT)
    if not data:
        print("错误：无法获取视频列表")
        return

    uploader = data['uploader']
    videos = data['videos']

    print(f"\nUP主：{uploader['name']}")
    print(f"签名：{uploader['sign']}")
    print(f"视频数：{len(videos)}")

    # 步骤2：下载并提取字幕
    success_count, failed_videos = download_and_extract_subtitles(videos)

    # 步骤3：生成笔记提示
    generate_notes_for_all_videos()

    # 总结
    print("\n" + "="*80)
    print("工作流完成！")
    print("="*80)
    print(f"视频总数：{len(videos)}")
    print(f"字幕提取成功：{success_count}")
    print(f"字幕提取失败：{len(failed_videos)}")
    print(f"\n下一步：使用Claude为每个字幕文件生成结构化笔记")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
