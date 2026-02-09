---
name: local-video-notes
description: 从本地视频文件提取字幕并生成结构化笔记。支持中英文视频，自动检测视频内嵌字幕，无字幕时使用 Whisper 语音识别。生成包含标题、核心主题、详细摘要、关键时间戳、重要概念术语和总结的完整 Markdown 笔记。当用户提供本地视频路径并要求提取字幕、生成笔记、视频总结、视频转录时使用此技能。
---

# 本地视频字幕提取与笔记生成器

## 前置依赖

需要安装以下依赖：

```bash
# 字幕提取（Whisper 语音识别）
pip install openai-whisper

# 视频处理（ffmpeg）
# Windows: 从 https://ffmpeg.org/download.html 下载
# 或使用 choco: choco install ffmpeg
```

检查依赖：
```bash
whisper --version  # 或 python -c "import whisper; print('OK')"
ffmpeg -version
```

## 快速开始

用户提供本地视频路径后：

1. **提取字幕**
```bash
python scripts/extract_subtitle.py "<video-path>"
```

2. **生成笔记**
基于提取的字幕内容，分析并生成结构化 Markdown 笔记。

## 支持的视频格式

- MP4、MKV、AVI、MOV、WebM、FLV 等常见格式
- 支持内嵌字幕的视频
- 无字幕视频自动使用 Whisper 语音识别

## 字幕提取流程

```
1. 检查视频是否有内嵌字幕
   ├─ 有 → 直接提取内嵌字幕
   └─ 无 → 使用 Whisper 语音识别
       ├─ 自动检测语言（支持中英文）
       └─ 生成带时间戳的字幕
```

## 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `video_path` | 视频文件路径（必需） | - |
| `--language` | 指定语言：zh/en/auto | auto |
| `--model` | Whisper 模型大小 | base |
| `--output` | 输出目录 | docs/ |

## 模型选择

| 模型 | 大小 | 速度 | 准确度 | 适用场景 |
|------|------|------|--------|----------|
| tiny | ~39MB | 最快 | 较低 | 快速测试 |
| base | ~74MB | 快 | 良好 | **默认推荐** |
| small | ~244MB | 中等 | 更好 | 重要内容 |
| medium | ~769MB | 慢 | 很好 | 高质量需求 |
| large | ~1550MB | 最慢 | 最佳 | 最终版本 |

## 使用示例

```bash
# 自动模式（自动检测内嵌字幕和语言）
python scripts/extract_subtitle.py "C:/Videos/tutorial.mp4"

# 指定中文视频
python scripts/extract_subtitle.py "video.mp4" --language zh

# 使用更大模型提高准确度
python scripts/extract_subtitle.py "video.mp4" --model small

# 自定义输出目录
python scripts/extract_subtitle.py "video.mp4" --output "C:/Notes"
```

## 输出格式

字幕输出为 JSON 格式，包含：
- `segments`: 字幕段落数组，每项含 `start`、`end`、`text`
- `language`: 检测到的语言
- `duration`: 视频时长

```json
{
  "segments": [
    {"start": 0.0, "end": 3.5, "text": "大家好，欢迎来到我的频道"},
    {"start": 3.5, "end": 7.2, "text": "今天我们来讲解 Python 编程"}
  ],
  "language": "zh",
  "duration": 180.5
}
```

## 笔记生成流程

1. 提取字幕 JSON 数据
2. 分析字幕内容，识别视频类型（教程/演讲/技术/Vlog）
3. 根据视频类型选择对应笔记模板
4. 生成结构化 Markdown 笔记，保存到 `docs/` 目录

## 笔记结构（通用）

```markdown
# [视频标题]

> 来源：[视频文件路径] | 时长：[视频时长]

## 视频概述
[1-2句话总结视频核心内容]

## 核心主题
- 主题 1
- 主题 2

## 详细内容

### [时间戳] [章节/要点标题]
[该部分的详细内容摘要]

## 重要概念与术语
| 术语 | 解释 |
|------|------|
| 概念1 | 解释内容 |

## 关键要点
1. 要点一
2. 要点二

## 总结与建议
[视频的总结和可行的建议]
```

## 特殊情况处理

### 无内嵌字幕且 Whisper 识别失败
告知用户视频音频质量问题，建议：
1. 检查视频是否有清晰的语音内容
2. 尝试使用更大的 Whisper 模型
3. 手动提供字幕文件（SRT/VTT 格式）

### 长视频（>1小时）
Whisper 处理时间较长，建议：
1. 使用 `--model tiny` 快速处理
2. 或分段提取字幕后合并

### 多语言视频
指定主要语言以获得更好效果：
```bash
python scripts/extract_subtitle.py "video.mp4" --language en
```

## 注意事项

- Whisper 首次运行会自动下载模型文件，需要联网
- 长视频处理时间较长，请耐心等待
- 默认使用 base 模型平衡速度和准确度
- 笔记自动保存为中文，原视频为非中文时会翻译关键术语
