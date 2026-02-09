#!/usr/bin/env python3
"""
YouTube 视频字幕和元数据提取器 (yt-dlp 版本)

使用 yt-dlp 作为备用方案，支持更多网站和字幕格式。

使用方法：
    python get_transcript_ytdlp.py "<youtube-url>"

输出：
    JSON 格式的视频信息，包含标题、字幕、时间戳等
"""

import sys
import json
import re
import subprocess
from urllib.parse import urlparse, parse_qs

# 修复Windows控制台编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def extract_video_id(url: str) -> str:
    """从 YouTube URL 中提取视频 ID"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    try:
        parsed = urlparse(url)
        if 'youtube.com' in parsed.netloc:
            return parse_qs(parsed.query).get('v', [None])[0]
    except:
        pass

    return None


def check_ytdlp_installed() -> bool:
    """检查 yt-dlp 是否已安装"""
    try:
        result = subprocess.run(['yt-dlp', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_video_info_with_ytdlp(url: str) -> dict:
    """使用 yt-dlp 获取视频信息"""
    result = {
        "url": url,
        "title": "",
        "description": "",
        "uploader": "",
        "duration": 0,
        "transcript": [],
        "chapters": []
    }

    try:
        # 获取视频基本信息
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-playlist',
            url
        ]

        process = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                encoding='utf-8',
                                errors='replace')

        if process.returncode != 0:
            result["error"] = process.stderr
            return result

        video_info = json.loads(process.stdout)

        result["title"] = video_info.get('title', '')
        result["description"] = video_info.get('description', '')
        result["uploader"] = video_info.get('uploader', '')
        result["duration"] = video_info.get('duration', 0)
        result["video_id"] = video_info.get('id', '')

        # 获取章节信息
        if 'chapters' in video_info and video_info['chapters']:
            for chapter in video_info['chapters']:
                result["chapters"].append({
                    "start_time": chapter.get('start_time', 0),
                    "end_time": chapter.get('end_time', 0),
                    "title": chapter.get('title', '')
                })

        # 尝试获取字幕
        # 优先获取中文字幕，然后英文字幕
        subtitles = video_info.get('subtitles', {})
        automatic_captions = video_info.get('automatic_captions', {})

        lang_priority = ['zh-Hans', 'zh-Hant', 'zh-CN', 'zh-TW', 'zh', 'en', 'en-US', 'en-GB']

        transcript_data = None
        transcript_lang = None

        # 检查手动字幕
        for lang in lang_priority:
            if lang in subtitles and subtitles[lang]:
                transcript_data = subtitles[lang]
                transcript_lang = lang
                break

        # 如果没有手动字幕，检查自动字幕
        if not transcript_data:
            for lang in lang_priority:
                if lang in automatic_captions and automatic_captions[lang]:
                    transcript_data = automatic_captions[lang]
                    transcript_lang = lang
                    break

        # 如果有字幕，下载第一个可用格式
        if transcript_data and len(transcript_data) > 0:
            sub_url = transcript_data[0].get('url', '')
            if sub_url:
                # 下载字幕内容
                import urllib.request
                try:
                    with urllib.request.urlopen(sub_url, timeout=10) as response:
                        sub_content = response.read().decode('utf-8')

                    # 解析字幕格式（通常是 SRT 或 VTT）
                    result["transcript"] = parse_subtitle_content(sub_content)
                    result["subtitle_lang"] = transcript_lang
                except Exception as e:
                    result["subtitle_error"] = str(e)

    except subprocess.TimeoutExpired:
        result["error"] = "获取视频信息超时"
    except json.JSONDecodeError:
        result["error"] = "解析视频信息失败"
    except Exception as e:
        result["error"] = str(e)

    return result


def parse_subtitle_content(content: str) -> list:
    """解析字幕内容（支持 SRT 和 VTT 格式）"""
    entries = []

    lines = content.strip().split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # SRT 格式：数字索引
        if line.isdigit():
            if i + 1 < len(lines):
                time_line = lines[i + 1].strip()
                # 解析时间戳 (e.g., "00:00:01,000 --> 00:00:04,000")
                time_match = re.search(
                    r'(\d+):(\d+):(\d+)[,\.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,\.](\d+)',
                    time_line
                )

                if time_match:
                    start_h, start_m, start_s, start_ms = map(int, time_match.groups()[:4])
                    end_h, end_m, end_s, end_ms = map(int, time_match.groups()[4:])

                    start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
                    duration = (end_h * 3600 + end_m * 60 + end_s + end_ms / 1000) - start_time

                    # 获取文本内容
                    text_lines = []
                    i += 2
                    while i < len(lines) and lines[i].strip() != '':
                        text_lines.append(lines[i].strip())
                        i += 1

                    text = ' '.join(text_lines)
                    # 移除 VTT 标签
                    text = re.sub(r'<[^>]+>', '', text)

                    if text:
                        entries.append({
                            'start': start_time,
                            'duration': duration,
                            'text': text
                        })

        i += 1

    return entries


def format_time(seconds: float) -> str:
    """将秒数格式化为时间戳 (HH:MM:SS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "请提供 YouTube 视频 URL",
            "usage": "python get_transcript_ytdlp.py \"<youtube-url>\""
        }))
        sys.exit(1)

    url = sys.argv[1]

    # 检查 yt-dlp 是否安装
    if not check_ytdlp_installed():
        print(json.dumps({
            "error": "yt-dlp 未安装",
            "solution": "请安装 yt-dlp: pip install yt-dlp 或访问 https://github.com/yt-dlp/yt-dlp"
        }))
        sys.exit(1)

    video_info = get_video_info_with_ytdlp(url)

    # 输出 JSON 格式
    print(json.dumps(video_info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
