---
name: bilibili-video-notes
description: 从哔哩哔哩视频一键生成结构化笔记的完整工作流程。自动下载视频、提取字幕（支持CC字幕和Whisper语音识别）、生成Markdown笔记并自动清理临时文件。当用户提供B站视频链接(bilibili.com、b23.tv)或BV号并要求生成笔记、摘要、总结或提取视频内容时使用此技能。支持所有类型的B站视频（教程、知识分享、技术、Vlog、课程等），自动处理无字幕视频，生成包含标题、核心主题、详细摘要、关键时间戳、重要概念术语解释和总结的完整Markdown笔记。
---

# 哔哩哔哩视频笔记生成器

一键式工作流程：下载视频 → 提取字幕 → 生成笔记 → 自动清理

## 快速开始

用户提供B站视频链接后，执行以下完整流程：

### 第一步：检查视频信息

```bash
cd ~/.claude/skills/bilibili-download
python scripts/bilibili_download.py "<url>" --info
```

### 第二步：下载视频

```bash
python scripts/bilibili_download.py "<url>" --quality best
```

视频默认保存到 `downloads/` 目录。

### 第三步：提取字幕

**优先级**：CC字幕 > Whisper语音识别

```bash
cd ~/.claude/skills/bilibili-notes
python scripts/bilibili_subtitle.py "<video-path>" api
```

如果API方式无字幕，自动使用yt-dlp：
```bash
python scripts/bilibili_subtitle.py "<video-path>" ytdlp
```

如果视频完全无字幕，使用Whisper：
```bash
cd ~/.claude/skills/local-video-notes
python scripts/extract_subtitle.py "<video-path>" --language zh --model base
```

### 第四步：生成笔记

基于提取的字幕JSON，生成结构化Markdown笔记：

1. 读取字幕JSON文件
2. 分析视频类型（教程/演讲/技术/Vlog/课程）
3. 选择对应笔记模板
4. 生成包含以下内容的笔记：
   - 视频概述
   - 核心主题
   - 详细内容（带时间戳）
   - 重要概念与术语
   - 关键要点
   - 总结与建议

### 第五步：自动清理

笔记生成完成后，删除以下临时文件：

```bash
# 删除下载的视频文件
rm ~/.claude/skills/bilibili-download/downloads/"<video-name>.mp4"

# 删除字幕JSON文件
rm ~/.claude/skills/*/docs/*_subtitle.json
```

## 支持的URL格式

- `https://www.bilibili.com/video/BVxxxxxxxxxx`
- `https://b23.tv/xxxxxxx`（短链接）
- 直接BV号：`BV1xxxxxxxxxx`

## 笔记输出规范

### 文件命名

- 格式：`笔记_<视频标题>.md`
- 位置：`docs/` 目录
- 去除特殊字符，使用下划线替代

### 笔记结构

```markdown
# [视频标题]

> 来源：[B站链接] | UP主：[UP主名称] | 时长：[视频时长]

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

## 错误处理

### 视频下载失败

- 检查网络连接
- 尝试降低画质（`--quality 720p`）
- 检查B站是否需要登录

### 字幕提取失败

- CC字幕不可用时自动降级到Whisper
- Whisper需要先安装：`pip install openai-whisper`
- 长视频处理时间较长，请耐心等待

### 笔记生成问题

- 无字幕视频只能生成基于标题和简介的概要笔记
- 建议下载后使用Whisper获取完整内容

## 工作流程图

```
用户输入B站链接
       ↓
检查视频信息
       ↓
下载视频到downloads/
       ↓
提取字幕（CC/API → yt-dlp → Whisper）
       ↓
生成结构化Markdown笔记
       ↓
保存到docs/目录
       ↓
清理临时文件（视频+字幕JSON）
       ↓
完成
```

## 参考现有技能

本技能整合了以下现有技能的功能：

- `bilibili-download` - 视频下载
- `bilibili-notes` - 字幕提取
- `local-video-notes` - Whisper语音识别和笔记生成

## 注意事项

- 下载的视频文件较大，确保有足够磁盘空间
- Whisper首次运行会下载模型文件，需要联网
- 笔记自动保存为中文
- 临时文件自动清理，节省磁盘空间
