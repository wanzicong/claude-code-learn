# 视频字幕提取器 (Video Subtitle Extractor)

从本地英文视频文件中提取英文字幕和台词信息的技能。

## 功能

- ✅ 从视频中提取英文字幕和台词
- ✅ 支持多种视频格式 (MP4, MKV, AVI, MOV, WebM 等)
- ✅ 输出多种格式 (纯文本, SRT, JSON)
- ✅ 自动生成时间戳
- ✅ 支持短视频和长电影
- ✅ 使用 Whisper AI 进行高精度语音识别

## 安装依赖

```bash
pip install openai-whisper ffmpeg-python
```

**注意**: 还需要安装 ffmpeg 系统工具:
- **Windows**: 从 https://ffmpeg.org/download.html 下载并添加到 PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 使用方法

### 方式 1: 使用 Python 脚本

```bash
# 基本使用 - 输出带时间戳的纯文本
python subtitle_extractor.py movie.mp4

# 输出 SRT 字幕格式
python subtitle_extractor.py movie.mp4 --format srt

# 使用更准确的模型
python subtitle_extractor.py movie.mp4 --model small

# 指定输出文件名
python subtitle_extractor.py movie.mp4 -o subtitles.txt

# 显示详细处理信息
python subtitle_extractor.py movie.mp4 -v
```

### 方式 2: 在 Python 代码中使用

```python
from subtitle_extractor import extract_subtitles

# 提取字幕
transcript = extract_subtitles(
    video_path="movie.mp4",
    model_size="base",
    output_format="txt",
    language="en"
)

# 保存到文件
with open("subtitles.txt", "w", encoding="utf-8") as f:
    f.write(transcript)
```

### 方式 3: 在 Claude Code 中使用

在 Claude Code 对话中,直接告诉 Claude 你需要提取视频字幕:

```
请帮我从 video.mp4 中提取英文字幕
```

Claude 会自动加载这个技能并帮你完成字幕提取。

## 模型选择

| 模型 | 大小 | 速度 | 准确度 | 适用场景 |
|------|------|------|--------|----------|
| tiny | ~39MB | 最快 | 较低 | 快速预览 |
| base | ~74MB | 快 | 良好 | **默认推荐** |
| small | ~244MB | 中等 | 更好 | 重要内容 |
| medium | ~769MB | 慢 | 很高 | 精确转录 |
| large | ~1550MB | 最慢 | 最高 | 最终版本 |

## 输出格式

### TXT 格式 (默认)
```
[0:00:15] Hello, welcome to the show.
[0:00:18] Today we're discussing AI technology.
[0:00:22] Let's get started.
```

### SRT 格式
```
1
00:00:15,000 --> 00:00:18,500
Hello, welcome to the show.

2
00:00:18,500 --> 00:00:22,000
Today we're discussing AI technology.
```

### JSON 格式
```json
{
  "segments": [
    {
      "start": 15.0,
      "end": 18.5,
      "text": "Hello, welcome to the show."
    }
  ]
}
```

## 性能参考

- **短视频 (5分钟)**: 使用 base 模型约需 1-2 分钟
- **长电影 (2小时)**: 使用 base 模型约需 20-30 分钟
- **准确度**: Whisper base 模型在清晰英语语音上可达 ~90% 词准确率

## 故障排除

| 问题 | 解决方法 |
|------|----------|
| `RuntimeError: Failed to load audio` | 安装 ffmpeg 系统工具 |
| 转录很慢 | 使用更小的模型 (tiny/base) |
| 准确度不高 | 使用更大的模型,检查音频质量 |
| 内存不足 | 使用更小的模型或分段处理 |
| 语言识别错误 | 添加 `--language en` 参数 |

## 技术说明

- 使用 **OpenAI Whisper** 模型进行语音识别
- 支持 99 种语言,本技能专注于英语字幕提取
- 完全本地处理,无需网络连接
- 自动处理音频提取和语音识别

## 参考

- [Whisper GitHub](https://github.com/openai/whisper)
- [FFmpeg 文档](https://ffmpeg.org/documentation.html)
