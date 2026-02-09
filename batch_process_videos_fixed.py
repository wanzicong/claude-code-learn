# -*- coding: utf-8 -*-
"""
批量处理B站视频：下载 -> Whisper识别 -> 生成笔记
"""
import json
import subprocess
import time
import sys
from pathlib import Path

# 设置输出编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# 配置
BILIBILI_DOWNLOAD_DIR = r"C:\Users\13608\.claude\skills\bilibili-download"
BILIBILI_NOTES_DIR = r"C:\Users\13608\.claude\skills\bilibili-notes"
LOCAL_VIDEO_NOTES_DIR = r"C:\Users\13608\.claude\skills\local-video-notes"
DOWNLOAD_DIR = Path(BILIBILI_DOWNLOAD_DIR) / "downloads"
DOCS_DIR = Path("docs")

# 读取视频列表
with open(r"C:\Users\13608\.claude\skills\bilibili-uploader\docs\小天fotos_videos.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
    videos = data['videos']

print(f"共找到 {len(videos)} 个视频")
print(f"将处理剩余的 {len(videos)-1} 个视频\n")

# 跳过第一个已处理的视频
videos_to_process = videos[1:]

success_count = 0
failed_videos = []

for i, video in enumerate(videos_to_process, 2):
    bvid = video['bvid']
    title = video['title']
    url = f"https://www.bilibili.com/video/{bvid}"

    print(f"\n{'='*80}")
    print(f"[{i}/{len(videos)}] 处理视频: {title}")
    print(f"BV号: {bvid}")
    print(f"链接: {url}")
    print(f"{'='*80}")

    try:
        # 步骤1：检查是否有CC字幕
        print("\n[1/4] 检查CC字幕...")
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
                    print("OK 找到CC字幕，跳过下载和Whisper")
                    success_count += 1
                    continue
            except json.JSONDecodeError:
                pass

        print("注意 无CC字幕，需要下载视频并使用Whisper")

        # 步骤2：下载视频
        print("\n[2/4] 下载视频...")
        download_cmd = [
            'python',
            str(Path(BILIBILI_DOWNLOAD_DIR) / 'scripts' / 'bilibili_download.py'),
            url,
            '--quality', 'best'
        ]
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=600, cwd=BILIBILI_DOWNLOAD_DIR, encoding='utf-8')

        if result.returncode != 0:
            print(f"失败 下载失败")
            failed_videos.append({'bvid': bvid, 'title': title, 'reason': '下载失败'})
            continue

        print("OK 视频下载成功")

        # 步骤3：查找下载的视频文件
        print("\n[3/4] 查找视频文件...")
        video_files = list(DOWNLOAD_DIR.glob(f"*{bvid}*.mp4"))
        if not video_files:
            print("失败 找不到下载的视频文件")
            failed_videos.append({'bvid': bvid, 'title': title, 'reason': '找不到视频文件'})
            continue

        video_path = str(video_files[0])
        print(f"OK 找到视频: {video_files[0].name}")

        # 步骤4：使用Whisper识别
        print("\n[4/4] 使用Whisper语音识别...")
        whisper_cmd = [
            'python',
            str(Path(LOCAL_VIDEO_NOTES_DIR) / 'scripts' / 'extract_subtitle.py'),
            video_path,
            '--language', 'zh',
            '--model', 'base'
        ]
        result = subprocess.run(whisper_cmd, capture_output=True, text=True, timeout=1800, cwd=LOCAL_VIDEO_NOTES_DIR, encoding='utf-8')

        if result.returncode != 0:
            print(f"失败 Whisper识别失败")
            failed_videos.append({'bvid': bvid, 'title': title, 'reason': 'Whisper失败'})
            continue

        print("OK Whisper识别完成")
        print(f"OK 视频 {i}/{len(videos)} 处理完成")
        success_count += 1

        # 避免请求过快
        time.sleep(3)

    except subprocess.TimeoutExpired:
        print(f"失败 处理超时")
        failed_videos.append({'bvid': bvid, 'title': title, 'reason': '超时'})
    except Exception as e:
        print(f"失败 错误: {str(e)}")
        failed_videos.append({'bvid': bvid, 'title': title, 'reason': str(e)})

# 输出统计
print(f"\n\n{'='*80}")
print("批量处理完成！")
print(f"{'='*80}")
print(f"成功: {success_count+1}/{len(videos)} (包括第1个已处理)")
print(f"失败: {len(failed_videos)}/{len(videos)}")

if failed_videos:
    print("\n失败的视频列表：")
    for v in failed_videos:
        print(f"  - {v['title']} ({v['bvid']}) - {v['reason']}")

print("\n所有视频的字幕已提取完成，接下来需要为每个视频生成笔记。")
