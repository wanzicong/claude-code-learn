# jdtls-lsp

Java 语言服务器 (Eclipse JDT.LS)，用于 Claude Code，提供代码智能和重构功能。

## 支持的扩展名
`.java`

## 安装

### 通过 Homebrew (macOS)
```bash
brew install jdtls
```

### 通过包管理器 (Linux)
```bash
# Arch Linux (AUR)
yay -S jdtls

# 其他发行版：需要手动安装
```

### 手动安装
1. 从 [Eclipse JDT.LS releases](https://download.eclipse.org/jdtls/snapshots/) 下载
2. 解压到一个目录（例如 `~/.local/share/jdtls`）
3. 在你的 PATH 中创建一个名为 `jdtls` 的包装脚本

## 系统要求
- Java 17 或更高版本（需要 JDK，而不仅仅是 JRE）

## 更多信息
- [Eclipse JDT.LS GitHub](https://github.com/eclipse-jdtls/eclipse.jdt.ls)
- [VSCode Java 扩展](https://github.com/redhat-developer/vscode-java)（使用 JDT.LS）
