#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哔哩哔哩视频笔记生成器 - 一键式工作流程
整合现有技能：bilibili-download + bilibili-notes + local-video-notes
"""

import sys
import os
import json
import subprocess
from pathlib import Path
import re

# 确保stdout使用UTF-8编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置路径
SKILLS_BASE = Path.home() / ".claude" / "skills"
DOCS_DIR = Path.cwd() / "docs"


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_step(step, text):
    print(f"\n[步骤 {step}] {text}")
    print("-" * 60)


def run_skill(skill_name, script_name, args):
    """运行指定技能的脚本"""
    skill_path = SKILLS_BASE / skill_name
    script_path = skill_path / "scripts" / script_name

    if not script_path.exists():
        print(f"错误: 脚本不存在 - {script_path}")
        return None

    cmd = [sys.executable, str(script_path)] + args
    print(f"执行: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore',
        cwd=str(skill_path)
    )

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python bilibili_video_notes.py <B站URL或BV号>")
        print("示例: python bilibili_video_notes.py BV1G3FNznEiS")
        return 1

    url = sys.argv[1].strip()

    # 修复URL
    if not url.startswith("http"):
        url = f"https://www.bilibili.com/video/{url}"

    print_header("哔哩哔哩视频笔记生成器")
    print(f"视频链接: {url}")
    print(f"笔记保存位置: {DOCS_DIR}")

    try:
        # 步骤1: 下载视频
        print_step(1, "下载视频")
        result = run_skill("bilibili-download", "bilibili_download.py", [url, "--quality", "best"])

        if result and result.returncode != 0:
            print(f"下载失败: {result.stderr}")
            # 继续尝试，可能已经有视频了

        # 查找下载的视频
        download_dir = SKILLS_BASE / "bilibili-download" / "downloads"
        video_files = list(download_dir.glob("*.mp4"))

        if not video_files:
            print("错误: 未找到下载的视频文件")
            return 1

        video_path = max(video_files, key=lambda p: p.stat().st_mtime)
        print(f"✓ 视频文件: {video_path.name}")

        # 步骤2: 提取字幕
        print_step(2, "提取字幕")

        # 先尝试API方式
        result = run_skill("bilibili-notes", "bilibili_subtitle.py", [str(video_path), "api"])
        subtitle_data = None
        subtitle_json_path = None

        if result and result.returncode == 0:
            try:
                subtitle_data = json.loads(result.stdout)
                if not subtitle_data.get("transcript"):
                    subtitle_data = None
            except:
                pass

        # 如果API失败，尝试yt-dlp
        if not subtitle_data:
            result = run_skill("bilibili-notes", "bilibili_subtitle.py", [str(video_path), "ytdlp"])
            if result and result.returncode == 0:
                try:
                    subtitle_data = json.loads(result.stdout)
                    if not subtitle_data.get("transcript"):
                        subtitle_data = None
                except:
                    pass

        # 如果都没有字幕，使用Whisper
        if not subtitle_data:
            print_step(3, "使用Whisper语音识别（可能需要较长时间）")
            result = run_skill("local-video-notes", "extract_subtitle.py",
                              [str(video_path), "--language", "zh", "--model", "base"])

            if result and result.returncode == 0:
                print(result.stdout)
                # 查找生成的字幕文件
                subtitle_files = list(DOCS_DIR.glob("*_subtitle.json"))
                if subtitle_files:
                    subtitle_json_path = max(subtitle_files, key=lambda p: p.stat().st_mtime)
                    try:
                        with open(subtitle_json_path, 'r', encoding='utf-8') as f:
                            subtitle_data = json.load(f)
                    except:
                        pass

        if not subtitle_data or not subtitle_data.get("segments"):
            print("错误: 无法获取字幕内容")
            return 1

        segments = subtitle_data.get("segments", [])
        print(f"✓ 字幕条数: {len(segments)}")

        # 步骤3: 生成笔记
        print_step(4, "生成结构化笔记")

        title = subtitle_data.get("title", "未知标题")
        duration = subtitle_data.get("duration", 0)
        duration_str = f"{int(duration//60)}:{int(duration%60):02d}"

        # 清理文件名
        safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)
        notes_filename = f"笔记_{safe_title}.md"
        notes_path = DOCS_DIR / notes_filename

        # 生成笔记内容
        notes_content = generate_notes_content(subtitle_data, url, duration_str)

        # 保存笔记
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write(notes_content)

        print(f"✓ 笔记已保存: {notes_path}")

        # 步骤4: 清理临时文件
        print_step(5, "清理临时文件")

        try:
            video_path.unlink()
            print(f"✓ 已删除视频: {video_path.name}")
        except Exception as e:
            print(f"删除视频失败: {e}")

        if subtitle_json_path and subtitle_json_path.exists():
            try:
                subtitle_json_path.unlink()
                print(f"✓ 已删除字幕JSON: {subtitle_json_path.name}")
            except Exception as e:
                print(f"删除字幕文件失败: {e}")

        # 清理其他临时字幕文件
        for json_file in DOCS_DIR.glob("*_subtitle.json"):
            try:
                json_file.unlink()
                print(f"✓ 已清理: {json_file.name}")
            except:
                pass

        print_header("完成!")
        print(f"笔记已保存到: {notes_path}")
        print(f"共处理 {len(segments)} 条字幕")

        return 0

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


def generate_notes_content(data, url, duration_str):
    """生成笔记内容"""
    title = data.get("title", "未知标题")
    segments = data.get("segments", [])

    content = f"""# {title}

> **来源**：[{url}]({url}) | **时长**：{duration_str} | **生成时间**：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 视频概述

{generate_overview(segments)}

## 核心主题

{generate_themes(segments)}

## 详细内容

{generate_detailed_content(segments)}

## 重要概念与术语

{generate_concepts_table(segments)}

## 关键要点

{generate_key_points(segments)}

## 总结

{generate_summary(segments, len(segments))}

---

**生成方式**：哔哩哔哩视频笔记生成器 | **字幕条数**：{len(segments)}
"""
    return content


def generate_overview(segments):
    """生成概述"""
    if not segments:
        return "暂无概述信息"

    # 使用前几个字幕的内容
    sample_text = " ".join([s.get("text", "") for s in segments[:min(10, len(segments))]])
    return sample_text[:200] + "..." if len(sample_text) > 200 else sample_text


def generate_themes(segments):
    """生成主题列表"""
    themes = []
    for i in range(0, min(len(segments), 50), 10):
        text = segments[i].get("text", "").strip()
        if len(text) > 5:
            themes.append(f"- {text[:50]}..." if len(text) > 50 else f"- {text}")
    return "\n".join(themes[:5])


def generate_detailed_content(segments):
    """生成详细内容"""
    content = ""
    segment_count = len(segments)
    segments_per_section = max(20, segment_count // 5)

    for i in range(0, min(len(segments), 100), segments_per_section):
        start_time = segments[i].get("start", 0)
        time_str = f"{int(start_time//60)}:{int(start_time%60):02d}"

        section_text = " ".join([s.get("text", "") for s in segments[i:i+segments_per_section]])
        content += f"### [{time_str}] 内容片段 {(i//segments_per_section)+1}\n\n{section_text[:300]}...\n\n"

    return content


def generate_concepts_table(segments):
    """生成概念表格"""
    # 简单提取可能的术语
    concepts = []
    seen = set()

    for seg in segments[:30]:
        text = seg.get("text", "")
        # 查找全大写的缩写
        matches = re.findall(r'[A-Z]{2,}', text)
        for match in matches:
            if match not in seen and len(match) >= 2:
                concepts.append(f"| {match} | 视频中讲解 |")
                seen.add(match)
                if len(concepts) >= 5:
                    break
        if len(concepts) >= 5:
            break

    if concepts:
        return "| 术语 | 解释 |\n|------|------|\n" + "\n".join(concepts)
    return "| 术语 | 解释 |\n|------|------|\n| 暂无 | 暂无 |"


def generate_key_points(segments):
    """生成关键要点"""
    points = []
    keywords = ["重要", "关键", "注意", "核心", "要点"]

    for seg in segments:
        text = seg.get("text", "").strip()
        if any(kw in text for kw in keywords) and len(text) > 10:
            points.append(f"{len(points)+1}. {text}")
            if len(points) >= 5:
                break

    # 如果没有找到，按时间间隔取
    if not points and segments:
        interval = max(1, len(segments) // 5)
        for i in [0, interval, 2*interval, 3*interval, 4*interval]:
            if i < len(segments):
                text = segments[i].get("text", "").strip()
                if len(text) > 10:
                    points.append(f"{len(points)+1}. {text}")

    return "\n".join(points) if points else "1. 暂无关键要点提取"


def generate_summary(segments, count):
    """生成总结"""
    total_duration = segments[-1].get("end", 0) if segments else 0

    summary = f"本视频共识别 {count} 条字幕内容，"
    summary += f"时长约 {int(total_duration//60)} 分 {int(total_duration%60)} 秒。"

    if count > 200:
        summary += " 内容较为丰富，建议分段学习回顾。"
    elif count > 50:
        summary += " 内容适中，涵盖了主要知识点。"
    else:
        summary += " 内容精炼，适合快速了解。"

    return summary


if __name__ == "__main__":
    sys.exit(main())
