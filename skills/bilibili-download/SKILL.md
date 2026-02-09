---
name: bilibili-download
description: 下载哔哩哔哩(B站)视频。当用户提供B站视频链接(bilibili.com、b23.tv)或BV号并要求下载视频时使用此技能。支持选择画质（最高画质/1080p/720p等），自动合并音视频为MP4格式。用户说"下载这个B站视频"、"帮我下载bilibili视频"、"保存这个视频"等均触发此技能。
---

# 哔哩哔哩视频下载器

## 前置依赖

需要 yt-dlp 工具。检查是否安装：

```bash
yt-dlp --version
```

未安装则执行：`pip install yt-dlp`

## 快速开始

用户提供B站视频链接后：

1. **查看视频信息**（可选）
```bash
python scripts/bilibili_download.py "<url>" --info
```

2. **下载视频**
```bash
python scripts/bilibili_download.py "<url>"
```

## 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | B站视频URL或BV号（必需） | - |
| `--quality` | 画质：best/1080p/720p/480p/360p | best |
| `--output` | 输出目录 | downloads/ |
| `--info` | 仅显示视频信息，不下载 | - |
| `--page` | 下载指定分P（从1开始） | 全部 |

## 支持的URL格式

- `https://www.bilibili.com/video/BVxxxxxxxxxx`
- `https://b23.tv/xxxxxxx`
- 直接BV号：`BV1xxxxxxxxxx`

## 使用示例

```bash
# 最高画质下载
python scripts/bilibili_download.py "https://www.bilibili.com/video/BV1xxxxxx"

# 指定1080p画质
python scripts/bilibili_download.py "BV1xxxxxx" --quality 1080p

# 自定义保存目录
python scripts/bilibili_download.py "<url>" --output "C:/Videos"

# 下载分P视频的第2P
python scripts/bilibili_download.py "<url>" --page 2

# 仅查看视频信息和可用画质
python scripts/bilibili_download.py "<url>" --info
```

## 工作流程

1. 用户提供B站链接
2. 运行 `--info` 获取视频信息，告知用户视频标题、时长、可用画质
3. 确认后运行下载命令
4. 下载完成后告知用户文件位置和大小

## 注意事项

- 默认保存到当前工作目录的 `downloads/` 文件夹
- 自动合并音视频为 MP4 格式
- 大文件下载需要等待，注意设置足够的超时时间（建议 timeout=600000）
- 分P视频默认只下载第一P，需要用 `--page` 指定或提示用户选择
