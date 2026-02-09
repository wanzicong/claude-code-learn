# Anthropic Agent Skills 完整指南

> 全面掌握 Claude Code 技能系统：从入门到精通

## 📖 文档说明

本项目提供了一份详细的 Anthropic Agent Skills 使用指南和实战指南，帮助你从零开始掌握 Claude Code 技能系统。

## 📁 文件结构

```
docs/
├── anthropic-agent-skills-完整使用指南.md    # 主文档（推荐阅读）
├── 项目总结.md                              # 项目概览和统计
├── 技能模板/
│   └── SKILL.md                            # 技能模板文件
└── 示例代码/
    ├── main.py                             # Python 脚本示例
    ├── batch_process.sh                    # Bash 脚本示例
    ├── requirements.txt                    # Python 依赖
    └── README.md                           # 示例代码说明
```

## 🚀 快速开始

### 1. 阅读主文档

**推荐阅读顺序**：

**新手用户** 👶
```
第一章：技能系统基础
  ↓
第二章：配置和安装
  ↓
第三章 3.1-3.2：创建流程
  ↓
附录 B：技能模板
```

**开发者** 👨‍💻
```
第一章 1.2：工作原理
  ↓
第三章：完整流程
  ↓
第四章：核心技能
  ↓
第五章：实战案例
```

**高级用户** 🚀
```
第四章：核心技能详解
  ↓
第五章：实战案例
  ↓
第六章：最佳实践
  ↓
附录 A：FAQ
```

### 2. 使用技能模板

```bash
# 复制模板到你的技能目录
cp docs/技能模板/SKILL.md ~/.claude/skills/my-skill/

# 编辑模板
vim ~/.claude/skills/my-skill/SKILL.md

# 根据需要添加脚本和资源
mkdir -p ~/.claude/skills/my-skill/{scripts,references,assets}
```

### 3. 使用示例代码

```bash
# 复制示例脚本
cp docs/示例代码/main.py ~/.claude/skills/my-skill/scripts/

# 安装依赖
pip install -r docs/示例代码/requirements.txt

# 测试脚本
python ~/.claude/skills/my-skill/scripts/main.py --help
```

## 📚 文档内容

### 主文档章节

| 章节 | 内容 | 适合人群 |
|------|------|---------|
| **第一章** | 技能系统基础 | 所有用户 |
| **第二章** | 配置和安装 | 新手、开发者 |
| **第三章** | 技能创建流程 | 开发者 |
| **第四章** | 核心技能详解 | 开发者、高级用户 |
| **第五章** | 实战案例 | 开发者、高级用户 |
| **第六章** | 最佳实践 | 所有用户 |
| **附录** | FAQ、模板、示例 | 所有用户 |

### 核心内容

#### 🎯 三层按需加载架构

```
第1层：元数据（~100词）
  ├─ 始终在上下文中
  └─ 让 AI 知道技能存在

第2层：SKILL.md（<5k词）
  ├─ 技能触发时加载
  └─ 提供核心指导

第3层：资源（无限制）
  ├─ 按需加载
  └─ 详细文档和脚本
```

#### 🔧 6步创建流程

1. **理解需求** - 明确技能用途和场景
2. **规划内容** - 识别需要的脚本、文档和资源
3. **初始化技能** - 创建目录结构
4. **编写 SKILL.md** - 填写元数据和内容
5. **添加资源** - 实现脚本和文档
6. **测试迭代** - 验证和改进

#### 💡 实战案例

1. **餐厅物料创意生成技能**
   - 品牌规范应用
   - AI 图像生成集成
   - 实体和社交媒体物料

2. **Stripe 支付集成技能**
   - 最佳实践指导
   - 安全建议
   - 与 MCP 配合使用

3. **自定义 MCP 服务器**
   - 完整开发流程
   - TypeScript 实现
   - 工具设计和测试

## 📊 文档统计

| 指标 | 数值 |
|------|------|
| 总文档行数 | 1,352 行 |
| 文档大小 | 37 KB |
| 章节数量 | 6 章 + 附录 |
| 代码示例 | 20+ 个 |
| 实战案例 | 3 个 |
| FAQ 问题 | 10 个 |
| 技能模板 | 3 个 |
| 脚本示例 | 2 个 |

## 🎓 学习路径

### 路径 1：快速入门（1-2 小时）

```
1. 阅读第一章 1.1-1.2（理解概念）
2. 阅读第二章 2.1-2.2（安装配置）
3. 使用技能模板创建第一个技能
4. 测试技能是否工作
```

### 路径 2：深入学习（4-6 小时）

```
1. 完整阅读第一章到第三章
2. 学习第四章中的核心技能
3. 跟随第五章的实战案例
4. 参考第六章的最佳实践
```

### 路径 3：精通掌握（8-10 小时）

```
1. 完整阅读所有章节
2. 实践所有实战案例
3. 创建自己的技能
4. 开发 MCP 服务器
5. 优化和维护技能
```

## 💻 实践建议

### 创建第一个技能

```bash
# 1. 创建技能目录
mkdir -p ~/.claude/skills/hello-skill

# 2. 复制模板
cp docs/技能模板/SKILL.md ~/.claude/skills/hello-skill/

# 3. 编辑模板（修改 name 和 description）
vim ~/.claude/skills/hello-skill/SKILL.md

# 4. 在 Claude Code 中测试
# 输入："使用 hello-skill 技能"
```

### 添加脚本功能

```bash
# 1. 创建脚本目录
mkdir -p ~/.claude/skills/hello-skill/scripts

# 2. 复制示例脚本
cp docs/示例代码/main.py ~/.claude/skills/hello-skill/scripts/

# 3. 修改脚本逻辑
vim ~/.claude/skills/hello-skill/scripts/main.py

# 4. 测试脚本
python ~/.claude/skills/hello-skill/scripts/main.py --help
```

## 🔍 常见问题

### Q1：技能不被触发怎么办？

**A**：检查以下几点：
1. `description` 字段是否包含相关关键词
2. SKILL.md 文件格式是否正确
3. 技能目录位置是否正确（`~/.claude/skills/`）
4. 尝试显式调用：`/技能名称 任务描述`

### Q2：如何调试技能？

**A**：
1. 使用 `--verbose` 参数查看详细信息
2. 检查脚本是否有执行权限
3. 验证依赖是否已安装
4. 查看 Claude Code 日志

### Q3：技能和 MCP 有什么区别？

**A**：
- **技能**：教 Claude 如何处理数据（提示词 + 脚本）
- **MCP**：连接 Claude 与外部数据源（API + 数据库）

详见文档第一章 1.4 节。

## 📖 推荐阅读顺序

### 按角色

**产品经理/项目经理**
- 第一章：理解技能系统
- 第五章：了解实战案例
- 附录 A：常见问题

**前端/后端开发者**
- 第一章 + 第二章：基础知识
- 第三章：创建流程
- 第四章：核心技能
- 第五章：实战案例

**DevOps/系统管理员**
- 第二章：配置和安装
- 第三章 3.3：脚本管理
- 第六章：最佳实践

**技术写作/文档工程师**
- 第三章 3.2：SKILL.md 编写
- 第六章 6.1：设计原则
- 附录 B：技能模板

## 🔗 相关资源

### 官方文档
- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [MCP 协议文档](https://modelcontextprotocol.io)
- [Anthropic API 文档](https://docs.anthropic.com)

### 技能市场
- [Anthropic 官方技能](https://github.com/anthropics/anthropic-agent-skills)
- [社区技能](https://github.com/topics/claude-skills)

### 开发工具
- 技能验证工具：`validate_skill.py`
- 技能初始化工具：`init_skill.py`
- 技能打包工具：`package_skill.py`

## 🤝 贡献

欢迎贡献改进建议、错误修正或新的示例！

## 📄 许可证

MIT License - 可自由使用和修改

## 📮 反馈

如果你有任何问题或建议，欢迎：
- 提交 Issue
- 发起 Pull Request
- 分享你的技能创建经验

---

**文档版本**：1.0.0
**最后更新**：2024年
**总字数**：约 20,000 字

祝你在使用 Anthropic Agent Skills 的过程中取得成功！🎉
