# 哔哩哔哩视频笔记生成器 - 详细使用说明

## 完整工作流程

本技能提供一键式工作流程，自动完成从B站视频到结构化笔记的全部过程：

```
用户输入B站链接
       ↓
1. 检查视频信息
       ↓
2. 下载视频到 downloads/
       ↓
3. 尝试CC字幕提取
       ↓
4. 尝试yt-dlp字幕提取
       ↓
5. 使用Whisper语音识别
       ↓
6. 生成结构化Markdown笔记
       ↓
7. 清理临时文件（视频+字幕JSON）
       ↓
完成
```

## 命令行使用

### 基本用法

```bash
python scripts/bilibili_video_notes.py "https://www.bilibili.com/video/BV1G3FNznEiS"
```

### 高级参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | B站视频URL或BV号（必需） | - |
| `--quality` | 视频画质 | best |
| `--language` | Whisper识别语言 | zh |
| `--model` | Whisper模型大小 | base |
| `--keep-files` | 保留视频和字幕文件 | False |
| `--skip-download` | 跳过下载，使用已有视频 | False |

### 示例

```bash
# 指定720p画质
python scripts/bilibili_video_notes.py "BV1G3FNznEiS" --quality 720p

# 使用更大的Whisper模型（更准确但更慢）
python scripts/bilibili_video_notes.py "BV1G3FNznEiS" --model small

# 保留视频和字幕文件用于调试
python scripts/bilibili_video_notes.py "BV1G3FNznEiS" --keep-files

# 使用已下载的视频重新生成笔记
python scripts/bilibili_video_notes.py "BV1G3FNznEiS" --skip-download
```

## 笔记输出结构

生成的笔记包含以下部分：

### 1. 视频概述
- 一句话总结视频核心内容

### 2. 核心主题
- 提取5个主要主题
- 基于字幕内容的关键词

### 3. 详细内容
- 按时间段组织的分段内容
- 每段包含时间戳和摘要
- 最多5个主要段落

### 4. 重要概念与术语
- 提取专业术语（全大写缩写、驼峰命名等）
- 表格形式展示

### 5. 关键要点
- 提取包含关键词的字幕
- 或按时间间隔选取代表性内容

### 6. 总结
- 视频时长和字幕统计
- 学习建议

## 字幕提取策略

### 优先级顺序

1. **B站API** - 最快，获取CC字幕
2. **yt-dlp** - 备选，需要安装 `pip install yt-dlp`
3. **Whisper** - 最终方案，语音识别

### Whisper模型选择

| 模型 | 大小 | 速度 | 准确度 | 适用场景 |
|------|------|------|--------|----------|
| tiny | ~39MB | 最快 | 较低 | 快速测试 |
| base | ~74MB | 快 | 良好 | **默认推荐** |
| small | ~244MB | 中等 | 更好 | 重要内容 |
| medium | ~769MB | 慢 | 很好 | 高质量需求 |
| large | ~1550MB | 最慢 | 最佳 | 最终版本 |

## 错误处理

### 视频下载失败

**可能原因**：
- 网络连接问题
- B站需要登录
- 视频不存在或已删除

**解决方案**：
- 检查网络连接
- 尝试降低画质
- 检查视频链接是否有效

### 字幕提取失败

**可能原因**：
- 视频无CC字幕
- yt-dlp未安装
- Whisper未安装或模型未下载

**解决方案**：
- 安装依赖：`pip install openai-whisper yt-dlp`
- 检查视频是否有语音内容
- 尝试使用更大的Whisper模型

### 笔记质量问题

**可能原因**：
- Whisper识别准确度不够
- 视频音质较差
- 语速过快

**解决方案**：
- 使用更大的Whisper模型
- 检查视频音质
- 手动调整笔记内容

## 文件路径说明

### 输入文件

- **B站视频URL**：用户提供
- **BV号**：可从URL提取

### 输出文件

- **笔记文件**：`docs/笔记_<视频标题>.md`
- **视频文件**：`~/.claude/skills/bilibili-download/downloads/<视频标题>.mp4`（自动清理）
- **字幕JSON**：`docs/<视频标题>_subtitle.json`（自动清理）

### 临时文件

默认自动清理以下临时文件：
- 下载的视频文件
- Whisper生成的字幕JSON文件

使用 `--keep-files` 参数可保留这些文件用于调试。

## 依赖要求

### 必需依赖

```bash
# 视频下载
pip install yt-dlp

# 字幕提取和语音识别
pip install openai-whisper
```

### 可选依赖

- **ffmpeg**：用于视频处理（Whisper需要）
  - Windows: 从 https://ffmpeg.org/download.html 下载
  - 或使用 `choco install ffmpeg`

## 性能考虑

### 处理时间

| 视频长度 | base模型 | small模型 | large模型 |
|---------|---------|----------|-----------|
| 10分钟 | ~2分钟 | ~5分钟 | ~15分钟 |
| 20分钟 | ~4分钟 | ~10分钟 | ~30分钟 |
| 1小时 | ~12分钟 | ~30分钟 | ~90分钟 |

### 磁盘空间

- **视频文件**：约100-500MB（取决于画质）
- **Whisper模型**：74MB-1.5GB（首次下载）
- **字幕JSON**：约1-5MB

## 最佳实践

1. **首次使用**：先用短视频测试，确保流程正常
2. **模型选择**：默认base模型平衡速度和准确度
3. **批量处理**：建议一次处理一个视频
4. **保留文件**：调试时使用 `--keep-files`
5. **检查质量**：生成后检查笔记，必要时手动调整

## 故障排除

### 问题：脚本找不到

**解决**：确保在正确的目录执行脚本，或使用绝对路径

```bash
cd ~/.claude/skills/bilibili-video-notes
python scripts/bilibili_video_notes.py "BV1G3FNznEiS"
```

### 问题：Whisper模型下载失败

**解决**：检查网络连接，或手动下载模型到 `~/.cache/whisper/`

### 问题：笔记生成失败

**解决**：检查字幕JSON文件是否存在，查看错误信息

## 与其他技能的关系

本技能整合了以下技能的功能：

- **bilibili-download**：视频下载
- **bilibili-notes**：字幕提取
- **local-video-notes**：Whisper语音识别和笔记生成

如果只需要单独功能，可以直接使用对应技能。
