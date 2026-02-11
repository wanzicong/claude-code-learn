---
description: 清理所有标记为 [gone] 的 git 分支（已在远程删除但在本地仍存在的分支），包括删除关联的工作树。
---

## 您的任务

您需要执行以下 bash 命令来清理已从远程仓库删除的过时本地分支。

## 要执行的命令

1. **首先，列出分支以识别任何具有 [gone] 状态的分支**
   执行此命令：
   ```bash
   git branch -v
   ```

   注意：带有 '+' 前缀的分支有关联的工作树，必须在删除之前删除其工作树。

2. **接下来，识别需要为 [gone] 分支删除的工作树**
   执行此命令：
   ```bash
   git worktree list
   ```

3. **最后，删除工作树并删除 [gone] 分支（处理常规分支和工作树分支）**
   执行此命令：
   ```bash
   # 处理所有 [gone] 分支，如果存在则删除 '+' 前缀
   git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
     echo "Processing branch: $branch"
     # 查找并删除工作树（如果存在）
     worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
     if [ ! -z "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
       echo "  Removing worktree: $worktree"
       git worktree remove --force "$worktree"
     fi
     # 删除分支
     echo "  Deleting branch: $branch"
     git branch -D "$branch"
   done
   ```

## 预期行为

执行这些命令后，您将：

- 看到所有本地分支及其状态的列表
- 识别并删除与 [gone] 分支关联的任何工作树
- 删除所有标记为 [gone] 的分支
- 提供关于已删除的工作树和分支的反馈

如果没有分支标记为 [gone]，则报告无需清理。
