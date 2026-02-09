#!/usr/bin/env python3
"""
视频字幕提取工具
Video Subtitle Extractor

使用 Whisper AI 从本地视频文件中提取英文字幕和台词。

依赖安装:
    pip install openai-whisper ffmpeg-python

使用示例:
    python subtitle_extractor.py movie.mp4
    python subtitle_extractor.py movie.mp4 --format srt --model small
"""

import argparse
import json
import os
import sys
from datetime import timedelta
from pathlib import Path


def check_dependencies():
    """检查必要的依赖是否安装"""
    try:
        import whisper
        return True, "whisper"
    except ImportError:
        return False, "whisper"


def format_srt_time(seconds):
    """将秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def format_timestamp(seconds):
    """将秒数转换为可读时间戳 (HH:MM:SS)"""
    return str(timedelta(seconds=int(seconds)))


def generate_srt(segments):
    """生成 SRT 格式字幕"""
    srt_content = []
    for i, segment in enumerate(segments, 1):
        start_time = format_srt_time(segment["start"])
        end_time = format_srt_time(segment["end"])
        text = segment["text"].strip()
        srt_content.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
    return "\n".join(srt_content)


def generate_txt(segments):
    """生成纯文本格式带时间戳的台词"""
    output = []
    for segment in segments:
        timestamp = format_timestamp(segment["start"])
        text = segment["text"].strip()
        output.append(f"[{timestamp}] {text}")
    return "\n".join(output)


def generate_json(result):
    """生成 JSON 格式的完整转录结果"""
    return json.dumps(result, indent=2, ensure_ascii=False)


def extract_subtitles(video_path, model_size="base", output_format="txt",
                     language="en", verbose=False):
    """
    从视频中提取字幕

    参数:
        video_path: 视频文件路径
        model_size: Whisper 模型大小 (tiny/base/small/medium/large)
        output_format: 输出格式 (txt/srt/json)
        language: 视频语言代码 (默认: en 表示英语)
        verbose: 是否显示详细输出

    返回:
        提取的字幕内容
    """
    import whisper

    if verbose:
        print(f"加载 Whisper 模型 ({model_size})...")
        print(f"视频文件: {video_path}")

    # 加载模型
    model = whisper.load_model(model_size)

    if verbose:
        print("开始转录...")
        print("(这可能需要一些时间,取决于视频长度)")

    # 执行转录
    result = model.transcribe(
        video_path,
        language=language,
        task="transcribe",
        word_timestamps=True,
        verbose=verbose
    )

    # 根据格式生成输出
    if output_format == "srt":
        return generate_srt(result["segments"])
    elif output_format == "json":
        return generate_json(result)
    else:  # txt (默认)
        return generate_txt(result["segments"])


def main():
    parser = argparse.ArgumentParser(
        description="从视频中提取英文字幕和台词",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s movie.mp4                    # 基本使用,输出 TXT 格式
  %(prog)s movie.mp4 --format srt       # 输出 SRT 字幕格式
  %(prog)s movie.mp4 --model small      # 使用更准确的模型
  %(prog)s movie.mp4 -o subs.srt        # 指定输出文件名
  %(prog)s movie.mp4 -v                 # 显示详细处理信息

模型大小比较:
  tiny   ~39MB   最快   准确度较低
  base   ~74MB   快     准确度良好 (推荐)
  small  ~244MB  中等   准确度更好
  medium ~769MB  慢     准确度很高
  large  ~1550MB 最慢   准确度最高
        """
    )

    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("-f", "--format", choices=["txt", "srt", "json"],
                       default="txt", help="输出格式 (默认: txt)")
    parser.add_argument("-m", "--model", choices=["tiny", "base", "small", "medium", "large"],
                       default="base", help="Whisper 模型大小 (默认: base)")
    parser.add_argument("-l", "--language", default="en",
                       help="视频语言 (默认: en 表示英语)")
    parser.add_argument("-o", "--output", help="输出文件路径 (默认: 视频同名)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="显示详细处理信息")

    args = parser.parse_args()

    # 检查视频文件是否存在
    if not os.path.exists(args.video):
        print(f"错误: 找不到视频文件 '{args.video}'", file=sys.stderr)
        sys.exit(1)

    # 检查依赖
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print(f"错误: 缺少依赖库 '{missing}'", file=sys.stderr)
        print("请运行: pip install openai-whisper ffmpeg-python", file=sys.stderr)
        sys.exit(1)

    # 确定输出文件路径
    if args.output:
        output_path = args.output
    else:
        video_stem = Path(args.video).stem
        ext_map = {"txt": "txt", "srt": "srt", "json": "json"}
        output_path = f"{video_stem}_subtitles.{ext_map[args.format]}"

    try:
        # 提取字幕
        content = extract_subtitles(
            video_path=args.video,
            model_size=args.model,
            output_format=args.format,
            language=args.language,
            verbose=args.verbose
        )

        # 保存到文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n[OK] 字幕已提取并保存到: {output_path}")

        # 显示统计信息
        lines = content.count("\n") + 1
        print(f"[OK] 共提取 {lines} 行字幕")

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
