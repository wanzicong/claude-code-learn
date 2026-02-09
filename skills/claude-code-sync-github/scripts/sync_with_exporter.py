#!/usr/bin/env python3
"""
使用 claude-code-exporter 导出 Markdown，然后同步到 GitHub。

功能：
- 使用 claude-code-exporter 生成标准 Markdown 格式
- 使用本地机器码作为项目标识
- 支持增量/全量同步
- 使用 gh/git 命令推送到 GitHub

用法：
  python sync_with_exporter.py --mode full     # 全量同步
  python sync_with_exporter.py --mode incremental  # 增量同步（默认）
  python sync_with_exporter.py --init           # 初始化仓库
  python sync_with_exporter.py --status         # 查看同步状态
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# 配置
# ============================================================

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
SYNC_STATE_FILE = CLAUDE_DIR / ".sync-state-exporter.json"
DEFAULT_REPO_PREFIX = "claude-conversations"
TEMP_EXPORT_DIR = CLAUDE_DIR / ".temp-export"


# ============================================================
# 工具函数
# ============================================================

def run_cmd(cmd, cwd=None, check=True, capture=True):
    """执行命令并返回输出。"""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=capture, text=True,
        shell=(platform.system() == "Windows"), check=False
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\n{stderr}")
    return result


def get_machine_id():
    """获取本地机器唯一标识码。"""
    system = platform.system()
    try:
        if system == "Windows":
            r = run_cmd(
                ["powershell", "-Command",
                 "Get-CimInstance -ClassName Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"],
                check=True
            )
            return r.stdout.strip()
        elif system == "Darwin":
            r = run_cmd(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                check=True
            )
            for line in r.stdout.splitlines():
                if "IOPlatformUUID" in line:
                    return line.split('"')[-2]
        else:  # Linux
            uuid_path = Path("/sys/class/dmi/id/product_uuid")
            if uuid_path.exists():
                return uuid_path.read_text().strip()
            machine_id_path = Path("/etc/machine-id")
            if machine_id_path.exists():
                return machine_id_path.read_text().strip()
    except Exception:
        pass
    # 回退：用主机名生成哈希
    fallback = f"{platform.node()}-{platform.machine()}-{platform.system()}"
    return hashlib.sha256(fallback.encode()).hexdigest()[:36]


def get_machine_id_short(machine_id):
    """获取机器码的短标识（前8位）。"""
    return machine_id.replace("-", "")[:8].upper()


def gh_available():
    """检查 gh CLI 是否可用且已认证。"""
    try:
        r = run_cmd(["gh", "auth", "status"], check=False)
        return r.returncode == 0
    except FileNotFoundError:
        return False


def repo_exists_on_github(repo_name):
    """检查 GitHub 上是否已存在该仓库。"""
    r = run_cmd(["gh", "repo", "view", repo_name], check=False)
    return r.returncode == 0


def claude_exporter_available():
    """检查 claude-code-exporter 是否已安装。"""
    try:
        r = run_cmd(["claude-prompts", "--version"], check=False)
        return r.returncode == 0
    except FileNotFoundError:
        return False


# ============================================================
# 同步状态管理
# ============================================================

def load_sync_state():
    """加载同步状态。"""
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"synced_projects": {}, "last_sync": None}


def save_sync_state(state):
    """保存同步状态。"""
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_dir_hash(directory):
    """获取目录内所有文件的组合哈希值。"""
    h = hashlib.md5()
    for root, dirs, files in os.walk(directory):
        for fname in sorted(files):
            fpath = Path(root) / fname
            if fpath.is_file():
                h.update(fpath.name.encode())
                h.update(str(fpath.stat().st_mtime).encode())
    return h.hexdigest()


# ============================================================
# 项目扫描
# ============================================================

def scan_projects():
    """扫描所有项目目录。"""
    if not PROJECTS_DIR.exists():
        print(f"错误: 未找到 Claude Code 项目目录: {PROJECTS_DIR}")
        sys.exit(1)

    projects = []
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        jsonl_files = list(project_dir.glob("*.jsonl"))
        if not jsonl_files:
            continue

        projects.append({
            "name": project_dir.name,
            "path": project_dir,
            "session_count": len(jsonl_files)
        })

    return projects


# ============================================================
# 核心同步逻辑
# ============================================================

def init_repo(machine_id, repo_name=None):
    """初始化 GitHub 仓库。"""
    if not gh_available():
        print("错误: gh CLI 未安装或未认证。请先运行 'gh auth login'")
        sys.exit(1)

    short_id = get_machine_id_short(machine_id)
    if not repo_name:
        repo_name = f"{DEFAULT_REPO_PREFIX}-{short_id}"

    # 获取当前 GitHub 用户名
    r = run_cmd(["gh", "api", "user", "-q", ".login"])
    username = r.stdout.strip()
    full_repo = f"{username}/{repo_name}"

    print(f"机器码: {machine_id}")
    print(f"短标识: {short_id}")
    print(f"仓库名: {full_repo}")

    # 检查仓库是否已存在
    if repo_exists_on_github(full_repo):
        print(f"仓库已存在: {full_repo}")
        return full_repo

    # 创建私有仓库
    print(f"正在创建私有仓库: {full_repo}")
    run_cmd([
        "gh", "repo", "create", repo_name,
        "--private",
        "--description", f"Claude Code 对话记录 (claude-code-exporter) - 机器 {short_id}",
    ])
    print(f"仓库创建成功: {full_repo}")
    return full_repo


def export_with_claude_exporter(project_path, output_dir, mode="full"):
    """使用 claude-code-exporter 导出对话。"""
    if not claude_exporter_available():
        print("错误: claude-code-exporter 未安装")
        print("请运行: npm install -g claude-code-exporter")
        sys.exit(1)

    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建命令
    cmd = ["claude-prompts", str(project_path)]

    if mode == "full":
        cmd.append("--full")
    elif mode == "prompts":
        cmd.append("--prompts")
    elif mode == "outputs":
        cmd.append("--outputs")

    cmd.extend([
        "--markdown",
        "-o", str(output_dir)
    ])

    # 执行导出
    print(f"  使用 claude-code-exporter 导出: {project_path.name}")
    result = run_cmd(cmd, check=False)

    if result.returncode != 0:
        print(f"  警告: 导出失败 - {result.stderr}")
        return False

    return True


def sync(mode="incremental", repo_name=None, export_mode="full"):
    """执行同步操作。"""
    if not gh_available():
        print("错误: gh CLI 未安装或未认证。请先运行 'gh auth login'")
        sys.exit(1)

    machine_id = get_machine_id()
    short_id = get_machine_id_short(machine_id)

    if not repo_name:
        repo_name = f"{DEFAULT_REPO_PREFIX}-{short_id}"

    # 获取用户名
    r = run_cmd(["gh", "api", "user", "-q", ".login"])
    username = r.stdout.strip()
    full_repo = f"{username}/{repo_name}"

    # 确保仓库存在
    if not repo_exists_on_github(full_repo):
        print(f"仓库不存在，正在初始化...")
        init_repo(machine_id, repo_name)

    # 准备本地工作目录
    work_dir = CLAUDE_DIR / ".sync-workdir"
    repo_dir = work_dir / repo_name

    if not repo_dir.exists():
        print(f"正在克隆仓库...")
        work_dir.mkdir(parents=True, exist_ok=True)
        run_cmd(["gh", "repo", "clone", full_repo, str(repo_dir)], check=False)
        if not (repo_dir / ".git").exists():
            # 仓库为空，手动初始化
            repo_dir.mkdir(parents=True, exist_ok=True)
            run_cmd(["git", "init"], cwd=str(repo_dir))
            run_cmd(["git", "remote", "add", "origin",
                      f"https://github.com/{full_repo}.git"], cwd=str(repo_dir))
    else:
        # 拉取最新
        run_cmd(["git", "pull", "--rebase"], cwd=str(repo_dir), check=False)

    # 加载同步状态
    state = load_sync_state()
    synced_projects = state.get("synced_projects", {})

    # 扫描项目
    projects = scan_projects()
    print(f"发现 {len(projects)} 个项目")

    # 创建 README
    readme_path = repo_dir / "README.md"
    readme_content = _generate_readme(machine_id, short_id, projects)
    readme_path.write_text(readme_content, encoding="utf-8")

    # 处理每个项目
    synced_count = 0
    skipped_count = 0

    for project in projects:
        project_name = project["name"]
        project_path = project["path"]

        # 计算项目哈希
        project_hash = get_dir_hash(project_path)

        # 增量模式：跳过未变化的项目
        if mode == "incremental" and project_name in synced_projects:
            if synced_projects[project_name] == project_hash:
                skipped_count += 1
                continue

        # 使用 claude-code-exporter 导出
        temp_output = TEMP_EXPORT_DIR / project_name
        success = export_with_claude_exporter(project_path, temp_output, export_mode)

        if not success:
            continue

        # 复制导出的文件到仓库
        project_out_dir = repo_dir / project_name
        if project_out_dir.exists():
            shutil.rmtree(project_out_dir)

        if temp_output.exists() and any(temp_output.iterdir()):
            shutil.copytree(temp_output, project_out_dir)
            synced_projects[project_name] = project_hash
            synced_count += 1

        # 清理临时文件
        if temp_output.exists():
            shutil.rmtree(temp_output)

    print(f"\n同步: {synced_count} 个项目, 跳过: {skipped_count} 个未变化")

    if synced_count == 0 and mode == "incremental":
        print("没有新的变化需要同步。")
        save_sync_state(state)
        return

    # Git 提交并推送
    print("正在提交并推送到 GitHub...")
    run_cmd(["git", "add", "-A"], cwd=str(repo_dir))

    # 检查是否有变化
    r = run_cmd(["git", "status", "--porcelain"], cwd=str(repo_dir))
    if not r.stdout.strip():
        print("Git 仓库无变化。")
        save_sync_state(state)
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"同步对话记录 (claude-code-exporter) [{mode}] - {now_str}\n\n更新 {synced_count} 个项目"
    run_cmd(["git", "commit", "-m", commit_msg], cwd=str(repo_dir))

    # 推送
    r = run_cmd(["git", "push", "-u", "origin", "HEAD:main"], cwd=str(repo_dir), check=False)
    if r.returncode != 0:
        run_cmd(["git", "push", "-u", "origin", "HEAD:main"], cwd=str(repo_dir), check=False)

    # 保存同步状态
    state["synced_projects"] = synced_projects
    save_sync_state(state)

    print(f"\n同步完成! 仓库: https://github.com/{full_repo}")


def show_status():
    """显示同步状态。"""
    machine_id = get_machine_id()
    short_id = get_machine_id_short(machine_id)
    state = load_sync_state()
    projects = scan_projects()

    total_sessions = sum(p["session_count"] for p in projects)
    synced_count = len(state.get("synced_projects", {}))

    print(f"机器码: {machine_id}")
    print(f"短标识: {short_id}")
    print(f"上次同步: {state.get('last_sync', '从未同步')}")
    print(f"项目数: {len(projects)}")
    print(f"总对话数: {total_sessions}")
    print(f"已同步项目: {synced_count}")
    print(f"待同步项目: {len(projects) - synced_count}")
    print()
    print(f"claude-code-exporter: {'✓ 已安装' if claude_exporter_available() else '✗ 未安装'}")
    print()

    for project in projects:
        print(f"  📁 {project['name']} ({project['session_count']} 个对话)")


def _generate_readme(machine_id, short_id, projects):
    """生成仓库 README。"""
    total = sum(p["session_count"] for p in projects)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# Claude Code 对话记录",
        "",
        f"使用 [claude-code-exporter](https://github.com/githubsocialdark/claude-code-exporter) 导出的对话记录。",
        "",
        f"| 属性 | 值 |",
        f"|------|-----|",
        f"| 机器码 | `{machine_id}` |",
        f"| 短标识 | `{short_id}` |",
        f"| 项目数 | {len(projects)} |",
        f"| 对话总数 | {total} |",
        f"| 最后更新 | {now_str} |",
        "",
        "## 项目列表",
        "",
    ]

    for project in sorted(projects, key=lambda p: p["name"]):
        lines.append(f"- [{project['name']}]({project['name']}/) ({project['session_count']} 个对话)")

    lines.extend([
        "",
        "---",
        "",
        "*由 claude-code-sync-github 技能自动生成*",
    ])

    return "\n".join(lines)


# ============================================================
# 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="使用 claude-code-exporter 同步对话到 GitHub")
    parser.add_argument("--mode", choices=["full", "incremental"], default="incremental",
                        help="同步模式: full=全量, incremental=增量(默认)")
    parser.add_argument("--export-mode", choices=["full", "prompts", "outputs"], default="full",
                        help="导出模式: full=完整对话, prompts=仅提示词, outputs=仅输出")
    parser.add_argument("--init", action="store_true", help="仅初始化仓库")
    parser.add_argument("--status", action="store_true", help="查看同步状态")
    parser.add_argument("--repo", type=str, default=None, help="自定义仓库名")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    machine_id = get_machine_id()

    if args.init:
        init_repo(machine_id, args.repo)
        return

    sync(mode=args.mode, repo_name=args.repo, export_mode=args.export_mode)


if __name__ == "__main__":
    main()
