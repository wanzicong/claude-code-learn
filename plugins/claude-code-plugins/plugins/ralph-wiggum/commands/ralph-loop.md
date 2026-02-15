---
description: "Start Ralph Wiggum loop in current session"
argument-hint: "PROMPT [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh:*)"]
hide-from-slash-command-tool: "true"
---

# Ralph 循环命令

执行设置脚本以初始化 Ralph 循环：

```!
"${CLAUDE_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh" $ARGUMENTS
```

请处理任务。当你尝试退出时，Ralph 循环将把相同的提示词反馈给你进行下一次迭代。你将在文件和 git 历史记录中看到之前的工作，从而能够不断迭代和改进。

关键规则：如果设置了完成承诺，你只能在该陈述完全且毫不含糊地为真时才能输出它。即使你认为自己卡住了或应该因其他原因退出，也不要输出虚假承诺来逃避循环。该循环被设计为持续运行直到真正完成。
