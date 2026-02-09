#!/usr/bin/env python3
"""
本地视频字幕提取器
支持内嵌字幕提取和 Whisper 语音识别
"""

import sys
import json
import argparse
import subprocess
import os
from pathlib import Path

# 修复Windows控制台编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(description='本地视频字幕提取器')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('--language', '-l', default='auto',
                        choices=['auto', 'zh', 'en'],
                        help='语言选择 (默认: auto)')
    parser.add_argument('--model', '-m', default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper 模型大小 (默认: base)')
    parser.add_argument('--output', '-o', default='docs',
                        help='输出目录 (默认: docs/)')
    return parser.parse_args()


def has_embedded_subtitles(video_path):
    """检查视频是否有内嵌字幕"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', video_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def extract_embedded_subtitles(video_path):
    """使用 ffmpeg 提取内嵌字幕"""
    temp_srt = Path('temp_subs.srt')
    try:
        # 提取第一个字幕轨道
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-map', '0:s:0', '-c:s', 'srt', str(temp_srt), '-y'],
            capture_output=True,
            timeout=60
        )

        if temp_srt.exists():
            return parse_srt(temp_srt)
    except Exception as e:
        print(f"提取内嵌字幕失败: {e}", file=sys.stderr)
    finally:
        if temp_srt.exists():
            temp_srt.unlink()
    return None


def parse_srt(srt_file):
    """解析 SRT 字幕文件"""
    segments = []
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        # 跳过序号
        if lines[i].strip().isdigit():
            i += 1
            if i >= len(lines):
                break
            # 解析时间戳
            time_line = lines[i].strip()
            if '-->' in time_line:
                start_end = time_line.split('-->')
                start = parse_srt_time(start_end[0].strip())
                end = parse_srt_time(start_end[1].strip().split()[0])
                i += 1
                # 读取文本
                text_lines = []
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                text = ' '.join(text_lines)
                if text:
                    segments.append({
                        'start': start,
                        'end': end,
                        'text': text
                    })
        i += 1

    return segments


def parse_srt_time(time_str):
    """解析 SRT 时间格式 HH:MM:SS,mmm"""
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_parts = parts[2].split(',')
    seconds = int(seconds_parts[0])
    millis = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def get_video_duration(video_path):
    """获取视频时长"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', video_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return float(info.get('format', {}).get('duration', 0))
    except Exception:
        pass
    return 0


def transcribe_with_whisper(video_path, language='auto', model_size='base'):
    """使用 Whisper 进行语音识别"""
    try:
        import whisper
    except ImportError:
        print("错误: 未安装 whisper，请运行: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"使用 Whisper {model_size} 模型进行语音识别...")

    # 加载模型
    model = whisper.load_model(model_size)

    # 语言参数映射
    lang_param = None if language == 'auto' else language

    # 转录
    result = model.transcribe(
        video_path,
        language=lang_param,
        task='transcribe',
        word_timestamps=False
    )

    segments = []
    for seg in result.get('segments', []):
        segments.append({
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text'].strip()
        })

    detected_language = result.get('language', 'unknown')

    return segments, detected_language


def main():
    args = parse_args()
    video_path = Path(args.video_path)

    if not video_path.exists():
        print(f"错误: 视频文件不存在: {video_path}", file=sys.stderr)
        sys.exit(1)

    # 获取视频时长
    duration = get_video_duration(str(video_path))

    # 检查是否有内嵌字幕
    print("检查内嵌字幕...")
    has_embedded = has_embedded_subtitles(str(video_path))

    segments = None
    language = args.language
    source = "unknown"

    if has_embedded:
        print("发现内嵌字幕，正在提取...")
        segments = extract_embedded_subtitles(str(video_path))
        if segments:
            source = "embedded"
            language = language if language != 'auto' else 'zh'

    if not segments:
        print("使用 Whisper 语音识别...")
        try:
            segments, detected_lang = transcribe_with_whisper(
                str(video_path),
                language=args.language,
                model_size=args.model
            )
            source = "whisper"
            if language == 'auto':
                language = detected_lang
        except Exception as e:
            print(f"Whisper 识别失败: {e}", file=sys.stderr)
            sys.exit(1)

    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建输出
    output = {
        'video_path': str(video_path),
        'video_name': video_path.stem,
        'duration': duration,
        'segments': segments,
        'language': language,
        'source': source
    }

    # 保存到文件
    output_file = output_dir / f"{video_path.stem}_subtitle.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 输出摘要
    print(f"\n提取完成!")
    print(f"视频: {video_path.name}")
    print(f"时长: {int(duration // 60)}:{int(duration % 60):02d}")
    print(f"语言: {language}")
    print(f"来源: {source}")
    print(f"字幕条数: {len(segments)}")
    print(f"输出文件: {output_file}")


if __name__ == '__main__':
    main()
