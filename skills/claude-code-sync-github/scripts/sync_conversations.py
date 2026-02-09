#!/usr/bin/env python3
"""
Claude Code 对话记录同步到 GitHub 的核心脚本。

功能：
- 从 ~/.claude/projects/ 读取 JSONL 对话记录
- 使用本地机器码作为项目标识
- 结构化输出为 Markdown 文件
- 支持增量/全量同步
- 使用 gh/git 命令推送到 GitHub

用法：
  python sync_conversations.py --mode full     # 全量同步
  python sync_conversations.py --mode incremental  # 增量同步（默认）
  python sync_conversations.py --init           # 初始化仓库
  python sync_conversations.py --status         # 查看同步状态
"""

import argparse
import json
import os
import platform
import re
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
SYNC_STATE_FILE = CLAUDE_DIR / ".sync-state.json"
DEFAULT_REPO_PREFIX = "claude-conversations"


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


# ============================================================
# 对话解析
# ============================================================

def parse_jsonl_file(filepath):
    """解析单个 JSONL 对话文件，返回结构化消息列表。"""
    messages = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            record_type = record.get("type", "")

            if record_type == "user":
                msg = record.get("message", {})
                content = msg.get("content", "")
                tool_results = []
                if isinstance(content, list):
                    text_parts = []
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        itype = item.get("type", "")
                        if itype == "text":
                            text_parts.append(item.get("text", ""))
                        elif itype == "tool_result":
                            tr_content = item.get("content", "")
                            if isinstance(tr_content, list):
                                tr_text = "\n".join(
                                    sub.get("text", "") for sub in tr_content
                                    if isinstance(sub, dict) and sub.get("type") == "text"
                                )
                            else:
                                tr_text = str(tr_content) if tr_content else ""
                            if tr_text:
                                is_err = item.get("is_error", False)
                                tool_results.append({
                                    "content": tr_text[:500] + ("..." if len(tr_text) > 500 else ""),
                                    "is_error": is_err,
                                })
                    content = "\n".join(text_parts)
                messages.append({
                    "type": "user",
                    "uuid": record.get("uuid", ""),
                    "timestamp": record.get("timestamp", ""),
                    "content": content,
                    "tool_results": tool_results,
                    "cwd": record.get("cwd", ""),
                })

            elif record_type == "assistant":
                msg = record.get("message", {})
                content_parts = msg.get("content", [])
                text_parts = []
                tool_uses = []
                thinking = []

                if isinstance(content_parts, str):
                    text_parts.append(content_parts)
                elif isinstance(content_parts, list):
                    for part in content_parts:
                        if not isinstance(part, dict):
                            continue
                        ptype = part.get("type", "")
                        if ptype == "text":
                            text_parts.append(part.get("text", ""))
                        elif ptype == "thinking":
                            thinking.append(part.get("thinking", ""))
                        elif ptype == "tool_use":
                            tool_uses.append({
                                "name": part.get("name", ""),
                                "input_summary": _summarize_tool_input(part.get("input", {}))
                            })
                        elif ptype == "server_tool_use":
                            tool_uses.append({
                                "name": part.get("name", ""),
                                "input_summary": _summarize_tool_input(part.get("input", {}))
                            })

                messages.append({
                    "type": "assistant",
                    "uuid": record.get("uuid", ""),
                    "timestamp": record.get("timestamp", ""),
                    "model": msg.get("model", "unknown"),
                    "content": "\n".join(text_parts),
                    "tool_uses": tool_uses,
                    "thinking_summary": thinking[0][:200] + "..." if thinking and len(thinking[0]) > 200 else (thinking[0] if thinking else ""),
                    "usage": msg.get("usage", {}),
                })

            elif record_type == "summary":
                messages.append({
                    "type": "summary",
                    "summary": record.get("summary", ""),
                    "timestamp": record.get("timestamp", ""),
                })

    return messages


def _summarize_tool_input(input_data):
    """简要概述工具调用的输入参数。"""
    if not input_data:
        return ""
    if isinstance(input_data, str):
        return input_data[:100]
    if isinstance(input_data, dict):
        parts = []
        for k, v in input_data.items():
            v_str = str(v)
            if len(v_str) > 80:
                v_str = v_str[:80] + "..."
            parts.append(f"{k}: {v_str}")
        return "; ".join(parts[:5])
    return str(input_data)[:200]


def format_conversation_md(session_id, messages, project_path):
    """将对话消息格式化为 Markdown 文件内容。"""
    lines = []

    # 提取元信息
    first_ts = ""
    last_ts = ""
    model = "unknown"
    summary_text = ""
    total_input_tokens = 0
    total_output_tokens = 0

    for m in messages:
        ts = m.get("timestamp", "")
        if ts and not first_ts:
            first_ts = ts
        if ts:
            last_ts = ts
        if m.get("type") == "assistant" and m.get("model", "unknown") != "unknown":
            model = m["model"]
        if m.get("type") == "summary":
            summary_text = m.get("summary", "")
        usage = m.get("usage", {})
        total_input_tokens += usage.get("input_tokens", 0)
        total_output_tokens += usage.get("output_tokens", 0)

    # 标题
    title = summary_text if summary_text else f"对话 {session_id[:8]}"
    lines.append(f"# {title}")
    lines.append("")

    # 元信息表
    lines.append("| 属性 | 值 |")
    lines.append("|------|-----|")
    lines.append(f"| 会话ID | `{session_id}` |")
    lines.append(f"| 项目路径 | `{project_path}` |")
    lines.append(f"| 模型 | `{model}` |")
    lines.append(f"| 开始时间 | {_format_ts(first_ts)} |")
    lines.append(f"| 结束时间 | {_format_ts(last_ts)} |")
    if total_input_tokens or total_output_tokens:
        lines.append(f"| Token用量 | 输入: {total_input_tokens:,} / 输出: {total_output_tokens:,} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 对话内容
    msg_count = 0
    for m in messages:
        if m["type"] == "user":
            content = m.get("content", "")
            tool_results = m.get("tool_results", [])

            # 跳过既没有文本也没有工具结果的空消息
            if not content.strip() and not tool_results:
                continue

            msg_count += 1
            lines.append(f"## 👤 用户 #{msg_count}")
            lines.append(f"*{_format_ts(m.get('timestamp', ''))}*")
            lines.append("")

            if content.strip():
                lines.append(content)
                lines.append("")

            # 工具返回结果
            if tool_results:
                lines.append("<details>")
                lines.append(f"<summary>📋 工具返回结果 ({len(tool_results)}条)</summary>")
                lines.append("")
                for tr in tool_results:
                    err_tag = " ❌ 错误" if tr.get("is_error") else ""
                    lines.append(f"**结果{err_tag}:**")
                    lines.append("```")
                    lines.append(tr.get("content", ""))
                    lines.append("```")
                    lines.append("")
                lines.append("</details>")
                lines.append("")

        elif m["type"] == "assistant":
            lines.append(f"## 🤖 助手")
            lines.append(f"*{_format_ts(m.get('timestamp', ''))} | 模型: {m.get('model', 'unknown')}*")
            lines.append("")

            # 思考过程（折叠）
            if m.get("thinking_summary"):
                lines.append("<details>")
                lines.append("<summary>💭 思考过程</summary>")
                lines.append("")
                lines.append(m["thinking_summary"])
                lines.append("")
                lines.append("</details>")
                lines.append("")

            # 回复内容
            if m.get("content"):
                lines.append(m["content"])
                lines.append("")

            # 工具调用（折叠）
            if m.get("tool_uses"):
                lines.append("<details>")
                lines.append(f"<summary>🔧 工具调用 ({len(m['tool_uses'])}次)</summary>")
                lines.append("")
                for tu in m["tool_uses"]:
                    lines.append(f"- **{tu['name']}**: {tu.get('input_summary', '')}")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        elif m["type"] == "summary":
            pass  # 已在标题中使用

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _format_ts(ts_str):
    """格式化 ISO 时间戳为可读格式。"""
    if not ts_str:
        return "未知"
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (ValueError, TypeError):
        return ts_str


# ============================================================
# 同步状态管理
# ============================================================

def load_sync_state():
    """加载同步状态。"""
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"synced_files": {}, "last_sync": None}


def save_sync_state(state):
    """保存同步状态。"""
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_file_hash(filepath):
    """获取文件的 MD5 哈希值。"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================
# 项目扫描
# ============================================================

def scan_projects():
    """扫描所有项目和对话文件。"""
    if not PROJECTS_DIR.exists():
        print(f"错误: 未找到 Claude Code 项目目录: {PROJECTS_DIR}")
        sys.exit(1)

    projects = {}
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        project_name = project_dir.name
        jsonl_files = list(project_dir.glob("*.jsonl"))

        if not jsonl_files:
            continue

        # 收集项目级别的额外文件（json 索引等）
        extra_files = []
        for jf in project_dir.glob("*.json"):
            extra_files.append(jf)

        # 收集 subagents 目录
        subagents_dir = project_dir / "subagents"

        projects[project_name] = {
            "path": project_dir,
            "sessions": [],
            "extra_files": extra_files,
            "has_subagents": subagents_dir.exists() and subagents_dir.is_dir(),
        }

        for jf in jsonl_files:
            session_id = jf.stem
            # 检查该会话是否有子目录（tool-results 等）
            session_subdir = project_dir / session_id
            projects[project_name]["sessions"].append({
                "id": session_id,
                "file": jf,
                "size": jf.stat().st_size,
                "mtime": jf.stat().st_mtime,
                "has_subdir": session_subdir.exists() and session_subdir.is_dir(),
            })

    return projects


def decode_project_path(encoded_name):
    """将编码的项目目录名还原为原始路径。"""
    # C--Users-13608 -> C:\Users\13608
    path = encoded_name
    # 还原驱动器号: C-- -> C:
    path = re.sub(r'^([A-Za-z])--', r'\1:/', path)
    # 还原路径分隔符
    path = path.replace("-", "/")
    return path


def sanitize_dirname(name):
    """将项目路径转为安全的目录名。"""
    # 移除驱动器号前缀，保留有意义的路径
    name = re.sub(r'^[A-Za-z]--', '', name)
    # 替换不安全字符
    name = re.sub(r'[<>:"/\\|?*]', '-', name)
    # 合并连续的连字符
    name = re.sub(r'-+', '-', name)
    return name.strip('-') or "default"


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
        "--description", f"Claude Code 对话记录 - 机器 {short_id}",
    ])
    print(f"仓库创建成功: {full_repo}")
    return full_repo


def sync(mode="incremental", repo_name=None):
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
    synced_files = state.get("synced_files", {})

    # 扫描项目
    projects = scan_projects()
    total_sessions = sum(len(p["sessions"]) for p in projects.values())
    print(f"发现 {len(projects)} 个项目，共 {total_sessions} 个对话")

    # 创建 README
    readme_path = repo_dir / "README.md"
    readme_content = _generate_readme(machine_id, short_id, projects)
    readme_path.write_text(readme_content, encoding="utf-8")

    # 处理每个项目
    synced_count = 0
    skipped_count = 0

    for project_name, project_info in projects.items():
        project_display = sanitize_dirname(project_name)
        project_out_dir = repo_dir / project_display
        project_out_dir.mkdir(parents=True, exist_ok=True)

        # 原始文件存放目录
        raw_dir = project_out_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        # 复制项目级别的额外文件（sessions-index.json 等）
        for ef in project_info.get("extra_files", []):
            dst = raw_dir / ef.name
            shutil.copy2(ef, dst)

        # 复制 subagents 目录
        if project_info.get("has_subagents"):
            src_subagents = project_info["path"] / "subagents"
            dst_subagents = raw_dir / "subagents"
            if dst_subagents.exists():
                shutil.rmtree(dst_subagents)
            shutil.copytree(src_subagents, dst_subagents)

        # 项目索引文件
        index_lines = [
            f"# 项目: {decode_project_path(project_name)}",
            "",
            f"| 会话ID | 大小 | 最后修改 |",
            f"|--------|------|----------|",
        ]

        for session in sorted(project_info["sessions"], key=lambda s: s["mtime"], reverse=True):
            session_id = session["id"]
            file_key = f"{project_name}/{session_id}"
            file_hash = get_file_hash(session["file"])

            # 增量模式：跳过未变化的文件
            if mode == "incremental" and file_key in synced_files:
                if synced_files[file_key] == file_hash:
                    skipped_count += 1
                    # 仍然添加到索引
                    mtime_str = datetime.fromtimestamp(session["mtime"]).strftime("%Y-%m-%d %H:%M")
                    size_kb = session["size"] / 1024
                    index_lines.append(
                        f"| [{session_id[:8]}...]({session_id}.md) | {size_kb:.1f}KB | {mtime_str} |"
                    )
                    continue

            # 解析并转换
            print(f"  处理: {project_display}/{session_id[:8]}...")
            messages = parse_jsonl_file(session["file"])

            if not messages:
                continue

            md_content = format_conversation_md(
                session_id, messages, decode_project_path(project_name)
            )

            # 写入 Markdown 文件
            out_file = project_out_dir / f"{session_id}.md"
            out_file.write_text(md_content, encoding="utf-8")

            # 复制原始 JSONL 文件
            shutil.copy2(session["file"], raw_dir / f"{session_id}.jsonl")

            # 复制会话子目录（tool-results 等）
            if session.get("has_subdir"):
                src_subdir = project_info["path"] / session_id
                dst_subdir = raw_dir / session_id
                if dst_subdir.exists():
                    shutil.rmtree(dst_subdir)
                shutil.copytree(src_subdir, dst_subdir)

            # 更新同步状态
            synced_files[file_key] = file_hash
            synced_count += 1

            # 添加到索引
            mtime_str = datetime.fromtimestamp(session["mtime"]).strftime("%Y-%m-%d %H:%M")
            size_kb = session["size"] / 1024
            index_lines.append(
                f"| [{session_id[:8]}...]({session_id}.md) | {size_kb:.1f}KB | {mtime_str} |"
            )

        # 写入项目索引
        index_file = project_out_dir / "索引.md"
        index_file.write_text("\n".join(index_lines), encoding="utf-8")

    print(f"\n同步: {synced_count} 个对话, 跳过: {skipped_count} 个未变化")

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
    commit_msg = f"同步对话记录 [{mode}] - {now_str}\n\n更新 {synced_count} 个对话"
    run_cmd(["git", "commit", "-m", commit_msg], cwd=str(repo_dir))

    # 推送（处理空仓库首次推送）
    r = run_cmd(["git", "push", "-u", "origin", "HEAD:main"], cwd=str(repo_dir), check=False)
    if r.returncode != 0:
        # 尝试 master 分支
        run_cmd(["git", "push", "-u", "origin", "HEAD:main"], cwd=str(repo_dir), check=False)

    # 保存同步状态
    state["synced_files"] = synced_files
    save_sync_state(state)

    print(f"\n同步完成! 仓库: https://github.com/{full_repo}")


def show_status():
    """显示同步状态。"""
    machine_id = get_machine_id()
    short_id = get_machine_id_short(machine_id)
    state = load_sync_state()
    projects = scan_projects()

    total_sessions = sum(len(p["sessions"]) for p in projects.values())
    synced_count = len(state.get("synced_files", {}))

    print(f"机器码: {machine_id}")
    print(f"短标识: {short_id}")
    print(f"上次同步: {state.get('last_sync', '从未同步')}")
    print(f"项目数: {len(projects)}")
    print(f"总对话数: {total_sessions}")
    print(f"已同步数: {synced_count}")
    print(f"待同步数: {total_sessions - synced_count}")
    print()

    for pname, pinfo in projects.items():
        display = decode_project_path(pname)
        print(f"  📁 {display} ({len(pinfo['sessions'])} 个对话)")


def _generate_readme(machine_id, short_id, projects):
    """生成仓库 README。"""
    total = sum(len(p["sessions"]) for p in projects.values())
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# Claude Code 对话记录",
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

    for pname, pinfo in sorted(projects.items()):
        display = decode_project_path(pname)
        dirname = sanitize_dirname(pname)
        lines.append(f"- [{display}]({dirname}/索引.md) ({len(pinfo['sessions'])} 个对话)")

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
    parser = argparse.ArgumentParser(description="Claude Code 对话记录同步到 GitHub")
    parser.add_argument("--mode", choices=["full", "incremental"], default="incremental",
                        help="同步模式: full=全量, incremental=增量(默认)")
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

    sync(mode=args.mode, repo_name=args.repo)


if __name__ == "__main__":
    main()
