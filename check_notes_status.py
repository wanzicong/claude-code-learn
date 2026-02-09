# -*- coding: utf-8 -*-
"""
批量笔记生成辅助脚本
列出所有待处理的字幕文件，并提供笔记生成指引
"""
import json
import sys
from pathlib import Path

# 设置输出编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置路径
SUBTITLE_DIR = Path(r"C:\Users\13608\.claude\skills\local-video-notes\docs")
NOTES_DIR = Path("docs")
NOTES_DIR.mkdir(parents=True, exist_ok=True)

def list_pending_notes():
    """列出所有待生成笔记的视频"""
    subtitle_files = list(SUBTITLE_DIR.glob("*_subtitle.json"))

    pending = []
    completed = []

    for subtitle_file in subtitle_files:
        # 提取BV号
        bvid_match = subtitle_file.stem.split('_BV')
        if len(bvid_match) < 2:
            continue

        bvid = 'BV' + bvid_match[1].replace('_subtitle', '')

        # 检查是否已有笔记
        note_files = list(NOTES_DIR.glob(f"*{bvid}*.md"))

        # 读取字幕信息
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        video_info = {
            'bvid': bvid,
            'subtitle_file': subtitle_file,
            'video_name': data.get('video_name', ''),
            'duration': data.get('duration', 0),
            'segments_count': len(data.get('segments', [])),
            'has_note': len(note_files) > 0,
            'note_file': note_files[0] if note_files else None
        }

        if video_info['has_note']:
            completed.append(video_info)
        else:
            pending.append(video_info)

    return pending, completed

def format_duration(seconds):
    """格式化时长"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def main():
    print("\n" + "="*80)
    print("B站视频笔记生成状态")
    print("="*80 + "\n")

    pending, completed = list_pending_notes()

    print(f"✓ 已完成笔记：{len(completed)} 个")
    for video in completed:
        print(f"  - {video['video_name']}")
        print(f"    BV号: {video['bvid']} | 时长: {format_duration(video['duration'])} | 字幕: {video['segments_count']}条")
        print(f"    笔记: {video['note_file'].name}\n")

    print(f"\n⚠ 待生成笔记：{len(pending)} 个")
    for i, video in enumerate(pending, 1):
        print(f"\n{i}. {video['video_name']}")
        print(f"   BV号: {video['bvid']}")
        print(f"   时长: {format_duration(video['duration'])}")
        print(f"   字幕: {video['segments_count']}条")
        print(f"   字幕文件: {video['subtitle_file']}")
        print(f"   URL: https://www.bilibili.com/video/{video['bvid']}")

    if pending:
        print("\n" + "="*80)
        print("笔记生成指引")
        print("="*80)
        print("\n对于每个待处理的视频，请执行以下步骤：\n")
        print("1. 读取字幕文件（上面列出的路径）")
        print("2. 分析字幕内容，识别视频类型（教程/技术分享/产品评测等）")
        print("3. 生成结构化Markdown笔记，包含：")
        print("   - 视频概述（1-2句话总结）")
        print("   - 核心主题（3-5个要点）")
        print("   - 详细内容（按时间戳分段，提取关键信息）")
        print("   - 重要概念与术语（表格形式）")
        print("   - 关键要点（列表形式）")
        print("   - 总结与建议")
        print("4. 保存笔记到 docs/ 目录，文件名格式：笔记_[视频标题].md")
        print("\n" + "="*80 + "\n")

        # 生成第一个视频的处理命令示例
        if pending:
            first_video = pending[0]
            print("示例：处理第一个视频")
            print("="*80)
            print(f"视频：{first_video['video_name']}")
            print(f"字幕文件：{first_video['subtitle_file']}")
            print(f"\n请使用Claude读取字幕文件并生成笔记。")
            print("="*80 + "\n")
    else:
        print("\n✓ 所有视频的笔记都已生成完成！\n")

    print("="*80)
    print(f"统计：共 {len(pending) + len(completed)} 个视频")
    print(f"  - 已完成：{len(completed)} 个")
    print(f"  - 待处理：{len(pending)} 个")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
