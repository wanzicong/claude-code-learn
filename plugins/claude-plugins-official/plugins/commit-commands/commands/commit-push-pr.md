---
allowed-tools: Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*)
description: 提交、推送并打开一个 PR
---

## 上下文

- 当前 git 状态：!`git status`
- 当前 git diff（已暂存和未暂存的更改）：!`git diff HEAD`
- 当前分支：!`git branch --show-current`

## 您的任务

基于以上更改：

1. 如果在 main 上，创建一个新分支
2. 使用适当的消息创建单个提交
3. 将分支推送到 origin
4. 使用 `gh pr create` 创建拉取请求
5. 您有能力在单个响应中调用多个工具。您必须在单个消息中完成上述所有操作。不要使用任何其他工具或做任何其他事情。除了这些工具调用外，不要发送任何其他文本或消息。
