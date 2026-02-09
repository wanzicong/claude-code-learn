---
name: bilibili-notes
description: 从哔哩哔哩(B站)视频生成结构化笔记。当用户提供B站视频链接(bilibili.com、b23.tv)或BV号并要求生成笔记、摘要、总结或提取视频内容时使用此技能。自动获取视频字幕/转录文本，生成包含标题、核心主题、详细摘要、关键时间戳、重要概念术语解释和总结的完整 Markdown 笔记。支持所有类型的B站视频（教程、知识分享、技术、Vlog、课程等）。
---

# 哔哩哔哩视频笔记生成器

## 快速开始

用户提供B站视频链接后，按以下步骤生成笔记：

1. **提取视频信息** — 运行 `scripts/bilibili_subtitle.py` 获取视频标题、字幕和元数据
2. **生成结构化笔记** — 分析字幕内容，按视频类型选择合适模板生成笔记
3. **保存笔记** — 以 `.md` 文件保存到 `docs/` 目录

## 获取视频信息

提供两种获取方式，自动模式会按顺序尝试：

### 方式一：B站API（推荐，无需额外依赖）

```bash
python scripts/bilibili_subtitle.py "<bilibili-url>" api
```

无需安装额外库，直接调用B站公开API。

### 方式二：yt-dlp（备选，功能更强）

```bash
python scripts/bilibili_subtitle.py "<bilibili-url>" ytdlp
```

需安装依赖：`pip install yt-dlp`

### 自动模式（默认）

```bash
python scripts/bilibili_subtitle.py "<bilibili-url>"
```

先尝试API，失败时自动回退到yt-dlp。

### 支持的URL格式

- `https://www.bilibili.com/video/BVxxxxxxxxxx`
- `https://b23.tv/xxxxxxx`（短链接）
- 直接传入BV号：`BV1xxxxxxxxxx`

### 脚本输出格式

JSON格式，包含以下字段：
- `title`: 视频标题
- `uploader`: UP主名称
- `duration`: 视频时长（秒）
- `description`: 视频简介
- `transcript`: 字幕数组，每项含 `text`、`start`、`duration`
- `pages`: 分P信息（如有）

## 笔记生成流程

1. 运行脚本获取JSON数据
2. 检查 `transcript` 是否有内容
   - **有字幕**：基于字幕内容生成详细笔记
   - **无字幕**：基于 `title` + `description` 生成概要笔记，并告知用户字幕不可用
3. 根据视频内容判断类型（教程/演讲/技术/Vlog/课程），选择对应笔记结构
4. 不同视频类型的笔记模板详见 `references/笔记模板.md`

## 笔记结构（通用）

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

## 输出规范

- 笔记语言：中文
- 文件名格式：`笔记_[视频标题].md`（去除特殊字符）
- 保存位置：`docs/` 目录
- 时间戳格式：`[MM:SS]` 或 `[HH:MM:SS]`

## 特殊情况处理

### 无字幕视频
告知用户该视频无可用字幕，基于视频标题和简介生成概要笔记。

### 分P视频
提示用户选择具体分P，或逐P生成笔记。修改脚本中的 `cid` 参数获取不同分P的字幕。

### 长视频（>1小时）
生成分段笔记，提供章节导航。

### 非中文字幕
保留原始语言的关键术语，笔记主体使用中文。
