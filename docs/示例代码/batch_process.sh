#!/bin/bash
# 示例 Bash 脚本：批量文件处理

set -e  # 遇到错误立即退出
set -u  # 使用未定义变量时报错

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本信息
SCRIPT_NAME=$(basename "$0")
VERSION="1.0.0"

# 函数：打印错误信息
error() {
    echo -e "${RED}错误: $1${NC}" >&2
    exit 1
}

# 函数：打印成功信息
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# 函数：打印警告信息
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 函数：打印信息
info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 函数：显示帮助信息
show_help() {
    cat << EOF
用法: $SCRIPT_NAME [选项] <输入目录> <输出目录>

批量处理目录中的文件

选项:
    -h, --help          显示此帮助信息
    -v, --version       显示版本信息
    -e, --extension     文件扩展名（默认：txt）
    --verbose           显示详细信息

示例:
    $SCRIPT_NAME input/ output/
    $SCRIPT_NAME -e csv input/ output/
    $SCRIPT_NAME --verbose input/ output/

EOF
}

# 函数：显示版本信息
show_version() {
    echo "$SCRIPT_NAME version $VERSION"
}

# 函数：处理单个文件
process_file() {
    local input_file="$1"
    local output_file="$2"
    local verbose="$3"

    if [ "$verbose" = true ]; then
        info "处理文件: $input_file"
    fi

    # 示例：转换为大写
    tr '[:lower:]' '[:upper:]' < "$input_file" > "$output_file"

    if [ "$verbose" = true ]; then
        success "已保存: $output_file"
    fi
}

# 默认参数
EXTENSION="txt"
VERBOSE=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--version)
            show_version
            exit 0
            ;;
        -e|--extension)
            EXTENSION="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            error "未知选项: $1"
            ;;
        *)
            break
            ;;
    esac
done

# 检查参数数量
if [ $# -lt 2 ]; then
    error "缺少必需参数。使用 -h 查看帮助信息。"
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# 验证输入目录
if [ ! -d "$INPUT_DIR" ]; then
    error "输入目录不存在: $INPUT_DIR"
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR" || error "无法创建输出目录: $OUTPUT_DIR"

# 统计信息
TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0

# 处理文件
info "开始处理文件..."

for input_file in "$INPUT_DIR"/*."$EXTENSION"; do
    # 检查文件是否存在
    if [ ! -f "$input_file" ]; then
        continue
    fi

    TOTAL_FILES=$((TOTAL_FILES + 1))

    # 获取文件名
    filename=$(basename "$input_file")
    output_file="$OUTPUT_DIR/$filename"

    # 处理文件
    if process_file "$input_file" "$output_file" "$VERBOSE"; then
        PROCESSED_FILES=$((PROCESSED_FILES + 1))
    else
        FAILED_FILES=$((FAILED_FILES + 1))
        warning "处理失败: $filename"
    fi
done

# 显示统计信息
echo ""
echo "处理完成！"
echo "总文件数: $TOTAL_FILES"
echo "成功: $PROCESSED_FILES"
if [ $FAILED_FILES -gt 0 ]; then
    echo "失败: $FAILED_FILES"
fi

if [ $PROCESSED_FILES -eq $TOTAL_FILES ]; then
    success "所有文件处理成功"
    exit 0
else
    warning "部分文件处理失败"
    exit 1
fi
