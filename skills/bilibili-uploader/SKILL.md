---
name: bilibili-uploader
description: 获取哔哩哔哩UP主信息和视频列表。当用户提供B站UP主主页链接、UID或用户名并要求查看UP主信息、获取视频列表、查看投稿、批量下载/生成笔记时使用此技能。支持获取UP主基本信息（昵称、头像、粉丝数、签名等）、视频列表（标题、BV号、播放量、点赞、时间等），支持按播放量/时间排序筛选，可自定义获取视频数量，支持批量生成笔记。
---

# 哔哩哔哩 UP 主信息与视频列表获取器

## 快速开始

用户提供 B站 UP 主信息后：

1. **获取 UP 主信息和视频列表**
```bash
python scripts/bilibili_uploader.py "<uploader-url>" [limit]
```

2. **筛选排序**
```bash
python scripts/bilibili_uploader.py "<uploader-url>" [limit] --sort plays
```

3. **批量生成笔记**
```bash
python scripts/bilibili_uploader.py "<uploader-url>" [limit] --notes
```

## 支持的输入格式

- UP 主主页链接：`https://space.bilibili.com/123456789`
- 直接 UID：`123456789`（纯数字）
- 短链接：`https://b23.tv/xxxxxx`

## 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `uploader_url` | UP 主链接或UID（必需） | - |
| `limit` | 获取视频数量 | 30 |
| `sort` | 排序方式：plays/pubtime | pubtime |
| `order` | 排序顺序：desc/asc | desc |
| `output` | 输出目录 | docs/ |
| `notes` | 批量生成笔记 | - |
| `json` | 只输出JSON格式 | - |
| `cookie` | B站Cookie（绕过反爬虫） | - |

## 使用示例

```bash
# 获取UP主信息和最新30个视频
python scripts/bilibili_uploader.py "https://space.bilibili.com/385670211"

# 获取最新50个视频
python scripts/bilibili_uploader.py "385670211" 50

# 按播放量排序获取热门视频
python scripts/bilibili_uploader.py "385670211" 30 --sort plays

# 按发布时间升序（最早发布）
python scripts/bilibili_uploader.py "385670211" 30 --sort pubtime --order asc

# 只输出JSON格式
python scripts/bilibili_uploader.py "385670211" --json

# 批量生成视频笔记
python scripts/bilibili_uploader.py "385670211" 10 --notes
```

## 输出格式

### UP 主信息

| 字段 | 说明 |
|------|------|
| `mid` | UP主 UID |
| `name` | 昵称 |
| `face` | 头像URL |
| `sign` | 个人签名 |
| `level` | 等级 |
| `follower` | 粉丝数 |
| `following` | 关注数 |
| `video_count` | 投稿数 |

### 视频列表信息

| 字段 | 说明 |
|------|------|
| `bvid` | 视频 BV 号 |
| `aid` | 视频 AV 号 |
| `title` | 视频标题 |
| `description` | 视频简介 |
| `duration` | 视频时长（秒） |
| `pubtime` | 发布时间 |
| `plays` | 播放量 |
| `likes` | 点赞数 |
| `coins` | 投币数 |
| `favorites` | 收藏数 |
| `comments` | 评论数 |
| `pic` | 封面URL |

## 批量生成笔记

使用 `--notes` 参数后，脚本会：
1. 获取视频列表
2. 对每个视频调用 `bilibili_notes` 脚本生成笔记
3. 笔记保存到 `docs/` 目录

**注意**：批量生成需要较长时间，建议先少量测试（如 3-5 个视频）

## 筛选排序

### 按播放量排序 (`--sort plays`)
- `desc`（默认）：播放量从高到低
- `asc`：播放量从低到高

### 按发布时间排序 (`--sort pubtime`)
- `desc`（默认）：最新发布
- `asc`：最早发布

## API 限制

- B站 API 有请求频率限制
- 建议单次获取不超过 100 个视频
- 大量视频建议分批获取

## Cookie 获取方法

**重要**：B站 API 需要登录 Cookie 才能正常访问，否则会返回 401 反爬虫错误。

### 获取步骤：

1. 登录 [bilibili.com](https://www.bilibili.com)
2. 按 F12 打开开发者工具
3. 切换到 **Application** 标签（或 **存储**）
4. 左侧展开 **Cookies** → 选择 `https://www.bilibili.com`
5. 找到以下两个关键 Cookie：
   - `SESSDATA` （会话凭证）
   - `bili_jct` （跨站请求令牌）
6. 复制它们的值

### 使用格式：

```bash
python scripts/bilibili_uploader.py "UID" --cookie "SESSDATA=你的值; bili_jct=你的值;"
```

### 示例：

```bash
# 使用 Cookie 获取 UP 主信息
python scripts/bilibili_uploader.py "385670211" 10 --cookie "SESSDATA=xxxxx; bili_jct=yyyyy;"
```

**注意**：
- Cookie 包含你的登录凭证，请勿泄露给他人
- Cookie 有有效期，过期后需重新获取
- 可以将 Cookie 保存到环境变量中避免每次输入

## 工作流程

1. 解析 UP 主 UID
2. 调用 B站 API 获取 UP 主信息
3. 调用 B站 API 获取视频列表
4. 按指定方式排序
5. 输出 JSON 和可读格式
6. （可选）批量生成笔记
