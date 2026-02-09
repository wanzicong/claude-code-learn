#!/usr/bin/env python3
"""
YouTube 视频字幕和元数据提取器

使用方法：
    python get_transcript.py "<youtube-url>"

输出：
    JSON 格式的视频信息，包含标题、字幕、时间戳等
"""

import sys
import json
import re
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import JSONFormatter
except ImportError:
    print(json.dumps({
        "error": "youtube-transcript 库未安装",
        "solution": "请运行: pip install youtube-transcript-api"
    }))
    sys.exit(1)


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

    # 尝试从 URL 参数中解析
    try:
        parsed = urlparse(url)
        if 'youtube.com' in parsed.netloc:
            return parse_qs(parsed.query).get('v', [None])[0]
    except:
        pass

    return None


def get_video_info(video_id: str) -> dict:
    """获取视频字幕和元数据"""
    result = {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": "",
        "transcript": [],
        "duration": 0,
        "languages": []
    }

    try:
        # 创建 API 实例
        ytt_api = YouTubeTranscriptApi()

        # 获取可用的字幕列表
        transcript_list = ytt_api.list(video_id)

        # 尝试获取中文字幕，然后英文字幕，最后任何可用字幕
        # 注意：YouTube 语言代码通常是 zh-Hans, zh-Hant, zh-TW, zh-CN 等
        preferred_languages = ['zh-TW', 'zh-CN', 'zh-Hans', 'zh-Hant', 'zh', 'en', 'en-US', 'en-GB']

        transcript = None
        transcript_lang = None
        transcript_dict = {t.language_code: t for t in transcript_list}

        # 尝试获取首选语言的字幕
        for lang_code in preferred_languages:
            if lang_code in transcript_dict:
                try:
                    transcript = transcript_dict[lang_code].fetch()
                    transcript_lang = lang_code
                    break
                except Exception:
                    continue

        # 如果没有找到首选语言，获取第一个可用的
        if not transcript and transcript_list:
            try:
                transcript = transcript_list[0].fetch()
                transcript_lang = transcript_list[0].language_code
            except Exception as e:
                result["error"] = f"无法获取字幕: {str(e)}"
                result["error_type"] = "FetchError"
                return result

        if transcript:
            # 将字幕转换为可序列化的列表格式
            result["transcript"] = [
                {
                    "text": t.text,
                    "start": t.start,
                    "duration": t.duration
                }
                for t in transcript
            ]
            result["languages"] = [{"language_code": transcript_lang, "language": transcript_lang}]

            # 计算视频时长
            if transcript:
                last_segment = transcript[-1]
                result["duration"] = int(last_segment.start + last_segment.duration)

            result["title"] = f"YouTube Video ({video_id})"

    except Exception as e:
        result["error"] = str(e)
        result["error_type"] = type(e).__name__

    return result


def format_time(seconds: float) -> str:
    """将秒数格式化为时间戳 (HH:MM:SS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_transcript_for_display(transcript_data: list) -> str:
    """将字幕数据格式化为易读的文本"""
    if not transcript_data:
        return "无可用字幕"

    lines = []
    for entry in transcript_data:
        # 检查是否是对象类型
        if hasattr(entry, 'start'):
            timestamp = format_time(entry.start)
            text = entry.text.strip()
        else:
            # 字典类型
            timestamp = format_time(entry.get('start', 0))
            text = entry.get('text', '').strip()
        lines.append(f"[{timestamp}] {text}")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "请提供 YouTube 视频 URL",
            "usage": "python get_transcript.py \"<youtube-url>\""
        }))
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print(json.dumps({
            "error": "无法从 URL 中提取视频 ID",
            "url": url
        }))
        sys.exit(1)

    video_info = get_video_info(video_id)

    # 输出 JSON 格式
    print(json.dumps(video_info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
