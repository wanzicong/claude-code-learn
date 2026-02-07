# OpenClaw 爆火的 AI 自动化神器！本地部署 Clawdbot，对接 Telegram / WhatsApp 最新教程

> 来源：[YouTube 链接](https://www.youtube.com/watch?v=dpFSzPiYwac) | 频道：零度解说 | 时长：13:05

> ⚠️ **注意**：该视频字幕被禁用，以下笔记基于视频元数据及UP主博客教程（freedidi.com）内容生成。

## 视频概述

零度解说介绍了近期爆火的 AI 自动化工具 OpenClaw 及其 Clawdbot 组件，手把手演示如何在本地部署，并对接 Telegram、WhatsApp 等即时通讯平台，实现 AI 自动化任务执行。

## 核心主题

- OpenClaw 是什么以及为什么它会爆火
- 本地部署 OpenClaw / Clawdbot 的完整流程
- 对接 Telegram 机器人
- 对接 WhatsApp
- AI 自动化的实际应用场景

## 详细内容

### 环境准备

**前置要求：**
- 安装 Git（下载地址：git-scm.com）
- Windows 或 Mac 系统
- OpenAI API 密钥（从 platform.openai.com/api-keys 生成）

### 安装 OpenClaw

**Windows PowerShell 安装：**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Windows CMD 安装：**
```cmd
curl -fsSL https://openclaw.ai/install.cmd -o install.cmd && install.cmd
```

**权限配置（必需）：**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 初始配置流程

1. 同意条款协议
2. 选择 AI 模型
3. 配置 OpenAI API 密钥
4. 选择要对接的第三方应用（Telegram、WhatsApp、Discord 等）

### 对接 Telegram 机器人

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 设置机器人名称和用户名
4. 获取 Bot Token
5. 在 Clawdbot 中配置 Token
6. 使用配对码完成连接：
```bash
openclaw pairing approve telegram [配对码]
```

### 对接 WhatsApp

视频中同样演示了 WhatsApp 的对接流程，具体步骤类似 Telegram。

### 管理命令

| 命令 | 功能 |
|------|------|
| `openclaw onboard` | 重新配置 |
| `openclaw uninstall` | 卸载 OpenClaw |
| `npm uninstall -g openclaw` | 完全移除 |

## 重要概念与术语

| 术语 | 解释 |
|------|------|
| **OpenClaw** | 一个开源的 AI 自动化平台，能够执行命令、操作系统、调度任务 |
| **Clawdbot** | OpenClaw 的机器人组件，用于对接各种即时通讯平台 |
| **BotFather** | Telegram 官方的机器人管理工具，用于创建和管理 Telegram Bot |
| **API Key** | OpenAI 的 API 密钥，用于调用 AI 模型能力 |
| **配对码** | 用于将 Clawdbot 与第三方平台（如 Telegram）建立连接的验证码 |

## 关键要点

1. OpenClaw 是一个本地部署的 AI 自动化工具，可以执行系统命令和调度任务
2. 安装过程相对简单，Windows 和 Mac 都有一键安装脚本
3. 需要 OpenAI API 密钥来驱动 AI 能力
4. 支持对接多个平台：Telegram、WhatsApp、Discord 等
5. Telegram 对接需要通过 BotFather 创建机器人并获取 Token
6. 提供 UI 控制面板方便管理

## 相关资源

- **OpenClaw 部署详细教程**：https://www.freedidi.com/22680.html
- **零度博客**：https://www.freedidi.com
- **零度电报群**：https://t.me/lingdujie

## 总结与建议

OpenClaw 是一个将 AI 能力与即时通讯平台结合的自动化工具，适合需要通过聊天界面控制 AI 执行任务的用户。部署过程较为简单，但需要注意：

1. 需要自备 OpenAI API 密钥（会产生 API 调用费用）
2. Windows 用户需要注意 PowerShell 执行策略的配置
3. 建议先在 Telegram 上测试，流程最为成熟
4. 详细的图文教程可参考零度博客的文章

---

*笔记生成时间：基于视频元数据 + 博客教程内容生成（视频字幕不可用）*
