---
name: bilibili-search-download
description: 哔哩哔哩(B站)视频搜索和下载工具。支持关键词搜索B站视频、查看搜索结果、使用BBDown下载视频。无需额外依赖，直接使用B站API。当用户要求搜索B站视频、查找特定主题的B站内容、或搜索后下载时使用此技能。用户说"搜索B站视频"、"找一下关于xx的视频"、"B站搜索xxx"等均触发此技能。
---

# 哔哩哔哩视频搜索和下载器

## 功能概述

本技能提供 B站视频搜索和下载的一体化解决方案：
1. **搜索功能** - 直接使用 B站 API 搜索视频（无需额外依赖）
2. **结果展示** - 展示搜索结果（标题、UP主、播放量、时长等）
3. **视频下载** - 使用 BBDown 下载选中的视频

## 前置依赖

### 1. BBDown 工具（必需）

检查是否安装：

```bash
"C:\Users\13608\Downloads\BBDown\BBDown.exe" --version
```

如需自定义 BBDown 路径，请修改脚本中的 `BBDOWN_PATH` 变量。

### 2. Python 标准库

本脚本使用 Python 标准库（urllib, json, subprocess），无需安装额外依赖！

## 快速开始

### 搜索视频

用户提供搜索关键词后：

```bash
python scripts/bilibili_search.py "<关键词>"
```

### 下载视频

获取 BV 号后：

```bash
python scripts/bilibili_search.py "<BV号>" --download
```

或直接使用 BBDown：

```bash
"C:\Users\13608\Downloads\BBDown\BBDown.exe" <BV号> -tv
```

## 脚本参数

### 搜索模式

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `keyword` | 搜索关键词（必需） | - |
| `--limit` | 返回结果数量 | 10 |

### 下载模式

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `BV号` | 视频BV号（必需） | - |
| `--download` | 下载模式 | - |
| `--quality` | 画质：tv/app/web | tv |
| `--output` | 输出目录 | downloads/ |

### 其他

| 参数 | 说明 |
|------|------|
| `--info` | 查看视频信息 |

## 工作流程

### 搜索视频

1. 用户提供搜索关键词
2. 执行搜索命令
3. 展示搜索结果列表（序号、标题、UP主、播放、时长、BV号）
4. 用户选择序号
5. 返回对应的 BV 号

### 下载视频

1. 用户选择搜索结果中的某个视频
2. 使用 BBDown 下载视频
3. 下载完成后告知用户文件位置

## 使用示例

```bash
# 搜索关于"Python教程"的视频
python scripts/bilibili_search.py "Python教程"

# 搜索20条结果
python scripts/bilibili_search.py "AI" --limit 20

# 下载指定BV号视频
python scripts/bilibili_search.py "BV1xxxxxxxxxx" --download

# 下载到指定目录
python scripts/bilibili_search.py "BV1xxxxxxxxxx" --download --output "C:/Videos"

# 查看视频信息
python scripts/bilibili_search.py "BV1xxxxxxxxxx" --info
```

## 搜索结果格式

```
搜索关键词: Python教程

  [1] Python零基础教程 - 从入门到精通
      UP主: 编程之魂  |  播放: 123万  |  时长: 45:20  |  BV: BV1xx411c7mM

  [2] 【Python】10分钟学会爬虫
      UP主: 代码实战  |  播放: 45万   |  时长: 12:30  |  BV: BV1yy411c7mN
...
```

## BBDown 下载参数

下载时支持的 BBDown 参数：

| 参数 | 说明 |
|------|------|
| `-tv` | 使用 TV API（画质更高，默认） |
| `-app` | 使用 APP API |
| `-ia` | 交互式选择清晰度 |
| `-p 1` | 下载指定分P |
| `-p ALL` | 下载全部分P |
| `--info` | 仅查看视频信息 |

## 技术实现

- **搜索**: 直接调用 B站公开 API (`https://api.bilibili.com/x/web-interface/search/type`)
- **下载**: 调用 BBDown 命令行工具
- **依赖**: 仅使用 Python 标准库，无需 pip install

## 注意事项

- 搜索需要网络连接访问 B站 API
- 下载速度取决于网络环境和视频大小
- 大会员内容需要 BBDown 登录后才可下载
- 搜索结果数量建议设置合理值（10-50）
- 下载的默认保存位置取决于 BBDown 配置

## 技巧

1. **精确搜索** - 使用具体关键词减少无关结果
2. **复制 BV 号** - 从搜索结果中复制 BV 号进行下载
3. **使用 BBDown 高级参数** - 如需更多下载选项，直接使用 BBDown

## 文件结构

```
skills/bilibili-search-download/
├── SKILL.md                    # 本文件
└── scripts/
    └── bilibili_search.py      # 主程序
```
