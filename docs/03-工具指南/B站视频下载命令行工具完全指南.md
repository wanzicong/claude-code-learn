# GitHub 哔哩哔哩(B站)视频下载命令行工具完全指南

## 概述

本文档总结了 GitHub 上主流的哔哩哔哩视频下载命令行工具，帮助开发者选择合适的工具进行视频下载和处理。

---

## 最受欢迎的工具

### 1. BBDown ⭐ 推荐

- **项目地址**: [nilaoda/BBDown](https://github.com/nilaoda/BBDown)
- **开发语言**: C#
- **特点**: 最热门，功能全面
- **版本**: 1.6.3

**主要功能**:
- 支持多线程下载
- 支持 aria2c 加速
- 支持 TV/APP/INTL API（更高画质）
- 交互式选择清晰度
- 支持分P下载、番剧、课程
- 扫码登录支持
- 字幕下载、弹幕下载
- 只下载视频/音频/封面

**基本用法**:
```bash
# 下载视频
BBDown <BV号>

# 使用TV API（通常画质更高）
BBDown <BV号> -tv

# 使用APP API
BBDown <BV号> -app

# 交互式选择清晰度
BBDown <BV号> -ia

# 下载指定分P
BBDown <BV号> -p 1,3,5
BBDown <BV号> -p 3-5
BBDown <BV号> -p ALL
BBDown <BV号> -p LAST

# 只下载视频（不含音频）
BBDown <BV号> --video-only

# 只下载音频
BBDown <BV号> --audio-only

# 下载弹幕
BBDown <BV号> --danmaku-only
BBDown <BV号> -dd

# 使用 aria2c 加速
BBDown <BV号> -aria2

# 扫码登录
BBDown login

# 查看视频信息
BBDown <BV号> --info

# 自定义文件名格式
BBDown <BV号> -F "<videoTitle>_<pageNumber>"
```

**下载链接**: https://github.com/nilaoda/BBDown/releases

---

### 2. bili-get

- **项目地址**: [kamikat/bilibili-get](https://github.com/kamikat/bilibili-get)
- **开发语言**: Rust
- **特点**: YouTube-dl 风格

**主要功能**:
- 视频质量选择
- 自动合并视频片段
- 大会员支持

---

### 3. bili-cli-rs

- **项目地址**: [niuhuan/bili-cli-rs](https://github.com/niuhuan/bili-cli-rs)
- **开发语言**: Rust
- **特点**: Rust 开发，功能丰富

**主要功能**:
- 用户登录支持
- 个人信息查看
- BV号或URL下载

---

### 4. biliup-rs

- **项目地址**: [biliup/biliup-rs](https://github.com/biliup/biliup-rs)
- **开发语言**: Rust
- **特点**: 投稿+下载双功能

**主要功能**:
- 多种登录方式（短信、密码、扫码、浏览器、Cookie）
- 视频投稿
- 视频下载

---

## Node.js/JavaScript 工具

### 1. bili-cli

- **项目地址**: [renmu123/bili-cli](https://github.com/renmu123/bili-cli)
- **安装方式**: npm
- **特点**: 支持订阅备份

**主要功能**:
- 视频订阅下载备份
- 命令行交互界面

---

### 2. Bili.TV-Downloader

- **项目地址**: [jjaruna/Bili.TV-Downloader](https://github.com/jjaruna/Bili.TV-Downloader)
- **开发语言**: JavaScript
- **特点**: 自动合并视频片段
- **默认画质**: 视频1080p，番剧720p

---

### 3. Lighting-bilibili-download

- **项目地址**: [MarySueTeam/Lighting-bilibili-download](https://github.com/MarySueTeam/Lighting-bilibili-download)
- **特点**: 轻量快速

**主要功能**:
- 进度通知
- 支持投稿、番剧、电视剧、视频片段、音频

---

### 4. bldl

- **项目地址**: [samuraime/bldl](https://github.com/samuraime/bldl)
- **特点**: 专注流媒体下载

---

## Go 语言工具

### bili-go

- **项目地址**: [mouxiaohui/bili-go](https://github.com/mouxiaohui/bili-go)
- **开发语言**: Go
- **特点**: 简单易用，需 FFmpeg

---

## 其他 CLI 工具

| 工具名称 | 项目地址 | 说明 |
|---------|---------|------|
| Bili23 CLI | [ScottSloan/Bili23-Downloader-CLI](https://github.com/ScottSloan/Bili23-Downloader-CLI) | 指定下载目录/线程数 |
| bili_dl | [urkbio/bili_dl](https://github.com/urkbio/bili_dl) | 简单下载器，Cursor编写 |
| bilibili-download | [lecepin/bilibili-download](https://github.com/lecepin/bilibili-download) | 免登录，默认1080P |

---

## 图形界面工具（供参考）

虽然本文聚焦命令行工具，但以下 GUI 工具也值得关注：

| 工具名称 | 项目地址 | Stars |
|---------|---------|-------|
| downkyi | [leiurayer/downkyi](https://github.com/leiurayer/downkyi) | 20k+ |
| downkyicore | [yaobiao131/downkyicore](https://github.com/yaobiao131/downkyicore) | 跨平台版 |
| BilibiliDown | [nICEnnnnnnnLee/BilibiliDown](https://github.com/nICEnnnnnnnLee/BilibiliDown) | GUI多平台 |
| bilibili-video-downloader | [lanyeeee/bilibili-video-downloader](https://github.com/lanyeeee/bilibili-video-downloader) | 支持番剧/课程/字幕 |

---

## Python API 库

### bilibili-api

- **项目地址**: [Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api)
- **开发语言**: Python
- **特点**: 400+ API 接口

**主要功能**:
- 视频、音频、直播、动态、专栏、用户、番剧
- 代理支持
- BV/AV 兼容
- 简洁易用
- 轻量级设计

**安装方式**:
```bash
pip install bilibili-api
```

---

## 功能对比

| 功能 | BBDown | bili-get | bili-cli-rs | Lighting |
|------|--------|---------|-------------|----------|
| 多P下载 | ✅ | ✅ | ✅ | ✅ |
| 番剧/课程 | ✅ | ✅ | ✅ | ✅ |
| 账号登录 | ✅ | ✅ | ✅ | - |
| 多线程 | ✅ | ✅ | ✅ | ✅ |
| 字幕下载 | ✅ | ✅ | - | - |
| 弹幕下载 | ✅ | - | - | - |
| TV API | ✅ | - | - | - |

---

## 推荐选择

根据不同需求选择合适的工具：

- **功能全面** → [BBDown](https://github.com/nilaoda/BBDown)（最推荐）
- **Rust 爱好** → [bili-cli-rs](https://github.com/niuhuan/bili-cli-rs)
- **简单易用** → [Lighting-bilibili-download](https://github.com/MarySueTeam/Lighting-bilibili-download)
- **Node.js** → [bili-cli](https://github.com/renmu123/bili-cli)
- **开发集成** → [bilibili-api](https://github.com/Nemo2011/bilibili-api) Python库

---

## BBDown 详细参数说明

### API 模式选择

```bash
-tv, --use-tv-api      # 使用TV端登录模式（推荐，画质更高）
-app, --use-app-api    # 使用APP端登录模式
-intl, --use-intl-api  # 使用国际版（港澳台）API模式
```

### 编码优先级

```bash
-e, --encoding-priority "hevc,av1,avc"  # 视频编码选择优先级
```

### 清晰度优先级

```bash
-q, --dfn-priority "8K 超高清, 1080P 高清, HDR 杜比, 视界之外"
```

### 下载选项

```bash
--video-only           # 只下载视频
--audio-only           # 只下载音频
--danmaku-only         # 只下载弹幕
--sub-only             # 只下载字幕
--cover-only           # 只下载封面
```

### 其他选项

```bash
-info, --only-show-info # 仅展示视频信息
--show-all             # 展示所有分P信息
-aria2, --use-aria2c   # 调用aria2c多线程下载
-ia, --interactive     # 交互式选择要下载的流
-hs, --hide-streams    # 不展示所有可用的视频流
-mt, --multi-thread    # 使用多线程下载（默认开启）
--skip-mux             # 跳过音视频混流
--skip-subtitle        # 跳过字幕下载
--skip-cover           # 跳过封面下载
```

---

## 使用建议

1. **个人使用**: 推荐使用 BBDown，功能全面且活跃维护
2. **开发集成**: 推荐使用 bilibili-api Python 库
3. **简单下载**: 可使用 Lighting-bilibili-download 或 bilibili-download
4. **批量订阅**: 可使用 bili-cli

---

## 注意事项

### ⚠️ 重要提醒

- 这些工具仅供**个人学习和研究**使用
- 请遵守哔哩哔哩服务条款
- 请遵守相关版权法律法规
- 不得用于商业用途

### 使用技巧

1. **高画质下载**: 使用 `-tv` 参数通常能获得更高画质
2. **登录后下载**: 大会员内容需要先登录 (`BBDown login`)
3. **音视频分离**: 某些情况下视频和音频是分开下载的，需要 FFmpeg 合并
4. **网络问题**: 遇到下载失败可尝试更换 API 模式或使用代理

---

## 参考资源

### 工具项目

- [nilaoda/BBDown](https://github.com/nilaoda/BBDown)
- [Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api)
- [renmu123/bili-cli](https://github.com/renmu123/bili-cli)
- [niuhuan/bili-cli-rs](https://github.com/niuhuan/bili-cli-rs)
- [biliup/biliup-rs](https://github.com/biliup/biliup-rs)
- [kamikat/bilibili-get](https://github.com/kamikat/bilibili-get)
- [MarySueTeam/Lighting-bilibili-download](https://github.com/MarySueTeam/Lighting-bilibili-download)
- [samuraime/bldl](https://github.com/samuraime/bldl)
- [jjaruna/Bili.TV-Downloader](https://github.com/jjaruna/Bili.TV-Downloader)
- [mouxiaohui/bili-go](https://github.com/mouxiaohui/bili-go)
- [urkbio/bili_dl](https://github.com/urkbio/bili_dl)
- [lecepin/bilibili-download](https://github.com/lecepin/bilibili-download)
- [ScottSloan/Bili23-Downloader-CLI](https://github.com/ScottSloan/Bili23-Downloader-CLI)

### GUI 工具

- [leiurayer/downkyi](https://github.com/leiurayer/downkyi) - 20k+ stars
- [yaobiao131/downkyicore](https://github.com/yaobiao131/downkyicore) - 跨平台版
- [nICEnnnnnnnLee/BilibiliDown](https://github.com/nICEnnnnnnnLee/BilibiliDown) - GUI多平台
- [lanyeeee/bilibili-video-downloader](https://github.com/lanyeeee/bilibili-video-downloader) - 支持Emby

---

*文档生成时间: 2026-02-09*
*最后更新: BBDown v1.6.3*
