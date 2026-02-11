# clangd-lsp

C/C++ 语言服务器 (clangd)，用于 Claude Code，提供代码智能、诊断和格式化功能。

## 支持的扩展名
`.c`, `.h`, `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`, `.C`, `.H`

## 安装

### 通过 Homebrew (macOS)
```bash
brew install llvm
# 添加到 PATH: export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
```

### 通过包管理器 (Linux)
```bash
# Ubuntu/Debian
sudo apt install clangd

# Fedora
sudo dnf install clang-tools-extra

# Arch Linux
sudo pacman -S clang
```

### Windows
从 [LLVM releases](https://github.com/llvm/llvm-project/releases) 下载，或通过以下方式安装：
```bash
winget install LLVM.LLVM
```

## 更多信息
- [clangd 官网](https://clangd.llvm.org/)
- [入门指南](https://clangd.llvm.org/installation)
