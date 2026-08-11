# KB8: 课程总结与作业

---

## 知识块信息表

| 字段 | 内容 |
|------|------|
| **知识块编号** | KB8 |
| **知识块名称** | 课程总结、课后作业、拓展阅读、FAQ、附录 |
| **所属课程** | AI 时代能力培养 / 第1周 / 第2课 |
| **所属章节** | 八（课后作业）、九（拓展阅读）、十（FAQ）、附录 |
| **建议时长** | 10 分钟 |
| **难度等级** | 初级（阅读+作业指导） |
| **前置知识** | KB1-KB7（全课内容） |

---

## 1. 本课核心回顾

本课从"AI 工程体系全景"出发，建立了六层技术栈认知，然后深入 Prompt Engineering 实操，最后完成了 AI 数据库操作的完整实战项目。

**六个核心要点**：

| # | 要点 | 关键内容 |
|---|------|----------|
| 1 | **六层工程体系** | Prompt(指令) → Context(信息) → Harness(运行时) → Hermes(记忆) → Loop(循环) → Graph(编排) 构成完整 AI 工程技术栈 |
| 2 | **Agent 的本质** | Agent 不是一个技术/模型/框架，而是六层能力整合的系统——能自主规划并使用工具完成任务 |
| 3 | **Prompt Engineering 深入** | RCTE 框架（Role/Context/Task/Example）+ 8 种技巧 + 4 类场景模板 + 8条优化原则 |
| 4 | **VSCode 开发环境搭建** | VSCode + Cline/Continue + Claude/DeepSeek API 的完整配置方案 |
| 5 | **MySQL 实操** | 完整的 AI 数据库操作 Agent：System Prompt 安全约束 + 三层权限隔离 + 先查后改原则 |
| 6 | **双轨定位** | 前半部分面向企业决策者（技术栈认知+投资决策），后半部分面向零基础学习者（动手实操+场景模板） |

---

## 2. 关键概念速查表

| 概念 | 一句话解释 | 企业含义 |
|------|-----------|----------|
| **Prompt Engineering** | 设计精准的 AI 指令以获得高质量输出 | ROI 最快的 AI 能力——优化 Prompt 可将客服准确率从 60% 提升到 90%，无需技术开发 |
| **RCTE 框架** | Role + Context + Task + Example——Prompt 的标准结构 | 企业 Prompt 标准化的核心工具，确保全公司 AI 输出一致 |
| **System Prompt** | 在对话开始前设定的 AI 持久行为规则 | Prompt 审计和质量控制的基础——所有对外 AI 系统必须审计其 System Prompt |
| **Context Engineering** | 管理 AI "看到"的完整信息环境（不只是指令） | 决定 RAG 系统的质量天花板——瓶颈不在模型，在上下文设计 |
| **Harness Engineering** | Agent 的运行时基础设施（权限/会话/工具注册/追踪） | 区分"能做 Demo"和"能上生产"的分水岭——采购 AI 工具应重点评估 Harness 成熟度 |
| **Hermes Engineering** | 长运行、有记忆、多消息入口的个人 Agent | 每个知识工作者未来的"数字影子"——跨会话记忆 + 多平台接入 |
| **Loop Engineering** | Agent 的"observe→think→act→feedback"推理循环 | Agent 可靠性工程的核心——防止死循环和错误滚雪球 |
| **Graph Engineering** | 用状态图编排 Agent 工作流（节点/边/条件/检查点） | 强监管行业 AI 落地的必要条件——可审计流转图替代黑箱决策 |
| **Agent** | 整合六层能力的自主任务完成系统 | 企业 AI 建设的终局目标——不是买一个工具，而是构建一个系统 |
| **MCP** | Model Context Protocol——AI 工具连接的开放标准协议 | 解决 AI 工具集成的"N x M"问题——一次开发，多模型复用 |
| **权限隔离** | 按 AI 操作类型授予不同的数据库账户权限 | 企业数据库安全的最低要求——AI 永远不该持有 root 密码 |
| **temperature** | 控制 AI 输出确定性的参数（0 确定 ↔ 1 创意） | SQL/代码生成用低温(0.1-0.3)，创意写作用高温(0.7-0.9) |

---

## 3. 课后作业

### 学生版作业

#### 作业 1：RCTE 框架实战（必做）

**任务**：用 RCTE 框架写 5 个不同场景的 Prompt，在至少 2 个不同的 AI 工具中测试效果。

| 场景编号 | 场景类型 | 示例主题参考 |
|----------|----------|-------------|
| 1 | 学习场景 | 用 RCTE 请 AI 解释一个本专业的概念 |
| 2 | 生活场景 | 用 RCTE 让 AI 规划一次出行/活动 |
| 3 | 工作场景 | 用 RCTE 让 AI 写一封工作邮件 |
| 4 | 编程场景 | 用 RCTE 让 AI 写一段代码 |
| 5 | 企业场景 | 用 RCTE 让 AI 分析一个商业问题 |

**提交要求**：写一篇不少于 400 字的对比笔记，包含每个 Prompt 在两个工具中的效果差异分析。

**评分标准**：

| 评分项 | 权重 | 满分标准 |
|--------|------|----------|
| RCTE 四要素完整性 | 40% | 5 个 Prompt 均包含完整的 Role/Context/Task/Example |
| 跨工具对比深度 | 30% | 具体描述了不同工具的响应差异并给出分析 |
| 场景多样性 | 20% | 覆盖 5 个不同场景，每个场景针对性强 |
| 笔记质量 | 10% | 结构清晰，有具体的观察和改进建议 |

#### 作业 2：搭建本地 AI 开发环境（必做）

**任务**：完成 VSCode + Cline + DeepSeek 的环境搭建。

**环境搭建清单**：

| 步骤 | 检查项 | 完成 |
|------|--------|:----:|
| 1 | VSCode 安装完成，可在终端中启动 | ☐ |
| 2 | Cline 插件安装并配置 DeepSeek API | ☐ |
| 3 | Continue 插件安装（可选，加分项） | ☐ |
| 4 | 在 Cline 中成功发送 1 条编程相关 Prompt | ☐ |
| 5 | AI 生成的代码能在终端中成功运行 | ☐ |

**提交要求**：发送至少 3 条编程相关的 Prompt，截图留证（含 VSCode 界面 + AI 响应）。

#### 作业 3：数据库操作 Agent 扩展（选做，强烈推荐）

**任务**：在 `ai_db_agent.py` 基础上增加功能。

**扩展方向**（任选其一）：

| # | 扩展方向 | 具体内容 | 难度 |
|---|----------|----------|:----:|
| A | **数据可视化** | 增加 Matplotlib 图表生成功能：用户说"画一张各部门薪资柱状图"，AI 自动查询数据并生成图表 | ⭐⭐⭐ |
| B | **多表支持** | 在 `ai_test_company` 中增加 `departments` 表和 `projects` 表，在 System Prompt 中添加多表结构描述，支持 JOIN 查询 | ⭐⭐⭐ |
| C | **自然语言转 API** | 让 Agent 支持"查询 DeepSeek API 本月消耗"这类自然语言 → API 调用的转换 | ⭐⭐⭐⭐ |

---

### 企业版作业

#### 作业 1：Prompt 模板审计（必做）

**任务**：列出企业中 AI 使用频率最高的 5 个场景，为每个场景创建 RCTE 标准模板。

**模板格式要求**：

```
场景名称：[邮件撰写/周报生成/竞品分析/客服回复/合同审查/...]
使用频率：[每天/每周/每月]
当前痛点：[无标准模板导致输出不一致/新人不会用/...]
RCTE 模板:
  Role:    [角色设定]
  Context: [背景+受众+限制]
  Task:    [具体任务描述]
  Example: [参考范例]
预期效果：[量化指标，如 回复准确率提升至 XX% / 输出时间缩短至 X 分钟]
```

**提交要求**：5 个模板 + 一个实施计划（如何推广到团队）。

#### 作业 2：权限隔离方案设计（选做）

**任务**：参照 KB7 的 MySQL 三层权限设计，为你企业的关键系统设计 AI 访问权限分级方案。

**方案要求**：

| 要求 | 说明 |
|------|------|
| **系统选择** | 选择一个企业的关键系统（数据库/CRM/ERP/文件服务器等） |
| **权限分级** | 至少设计 3 个层级（如 只读/受限写入/管理员），定义每层可执行的操作 |
| **AI 接入策略** | 明确 AI Agent 可以持有哪一层的凭据，哪些操作必须人工执行 |
| **审计机制** | 描述如何记录和审查 AI 的操作日志 |
| **应急预案** | 如果 AI 生成的 SQL/操作出现异常，如何回滚和止损 |

**输出格式**：一份 500 字以上的方案文档，包含权限矩阵表 + 流程图。

---

### 作业提交

| 项目 | 内容 |
|------|------|
| **截止时间** | 下次上课前一天 22:00 |
| **提交方式** | 课程群内提交 / 课程平台上传 |
| **命名规范** | `姓名_第2课_作业1` / `姓名_第2课_作业2` |

---

## 4. 拓展阅读

### 学习者推荐

| 资源 | 链接 | 说明 | 阅读时间 |
|------|------|------|----------|
| **Anthropic Prompt Engineering 指南** | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | 官方权威，涵盖 System Prompt 设计、Few-shot、Chain-of-Thought 等核心技巧 | 2 小时 |
| **OpenAI Prompt Engineering 指南** | https://platform.openai.com/docs/guides/prompt-engineering | 六大策略：写清指令、提供参考文本、拆分复杂任务、给模型"思考"时间、使用外部工具、系统测试 | 1.5 小时 |
| **Learn Prompting** | https://learnprompting.org | 免费的从零到高级的系统课程，含交互式练习 | 3-5 小时 |
| **Cline 官方文档** | https://docs.cline.bot | VSCode AI 插件完整指南：安装、配置、MCP、自定义指令 | 1 小时 |
| **DeepSeek API 文档** | https://platform.deepseek.com/docs | API 接入、计费说明、最佳实践（国内直连 + 极低成本） | 30 分钟 |
| **MySQL 官方文档** | https://dev.mysql.com/doc/refman/8.0/en/ | 官方参考手册：SQL 语法、账户管理、安全最佳实践 | 按需查阅 |

### 企业决策者推荐

| 资源 | 说明 | 核心价值 |
|------|------|----------|
| **Building Effective Agents (Anthropic)** | Agent 设计的纲领性文章，阐述了"简单优先、渐进增强"的 Agent 构建哲学 | 建立 Agent 投资决策的技术判断力 |
| **AI Harness Engineering (arXiv:2605.13357)** | Harness Engineering 的定义性学术论文。首次将 Agent 运行时基础设施定义为一门独立工程学科 | 理解 Agent 基础设施的技术深度和采购评估维度 |
| **Claude Code 架构分析** | 真实生产级 Agent 系统的架构设计剖析——权限模型、Hook 系统、MCP 集成、子代理机制 | 用真实案例理解六层体系的工程实现 |
| **MCP 官方文档** (modelcontextprotocol.io) | AI 工具连接的开放标准协议，解决"N 个模型 x M 个工具"的集成爆炸问题 | 企业 AI 工具投资避免被单一厂商锁定 |
| **LangGraph 文档** | 状态图编排框架：Checkpoint 机制、Human-in-the-loop、流式事件 | 强监管行业（金融/医疗/法律）AI 落地的技术基础 |
| **OpenClaw / Hermes Agent 项目** | 长运行个人 Agent 的开源实现范例 | 理解"数字影子"型 AI 的技术架构 |

---

## 5. 常见问题 (FAQ)

### Q1: Prompt → Context → Harness → Hermes → Loop → Graph，我应该从哪一层开始学？

**Prompt Engineering。** 这是所有上层工程的基础。先学会"怎么和 AI 说话"（1-2 周），再逐步理解"给 AI 看什么信息"（Context），然后才是"给 AI 装上手和脚"（Harness）。

零基础路径：Prompt Engineering（2周）→ 环境搭建实践（1周）→ Context Engineering（2周）→ Harness Engineering（4周+，需要编程基础）

### Q2: Claude Code 属于六层体系中的哪一层？

Claude Code 横跨 **Context / Harness / Loop / Graph** 四层：

- Context 层：自动压缩工具输出、对话历史管理
- Harness 层：Tool Registry (MCP)、Permission Gate (四级权限)、Hook System、Session 持久化
- Loop 层：高性能 Agent Loop、条件工具激活、子代理分发
- Graph 层：Subagents + Hooks 构成隐式工作流图，Pipeline 模式链式协作

不包含 Hermes 层（无长期记忆、不是常驻后台进程、无多消息平台网关）。

### Q3: Agent 到底是什么？跟普通 AI 对话有什么区别？

**Agent 是能自主规划并使用工具完成任务的 AI 系统。** 普通 AI 对话是"一问一答"；Agent 是"给一个目标 → 自主分析 → 拆解步骤 → 调用工具 → 验证结果 → 循环直到完成"。

技术定义：Agent = LLM（大脑）+ Loop（循环推理）+ Tools（工具调用）+ Harness（运行时保障）+ Hermes（可选，持久记忆）。不是一个"产品品类"，而是一个"系统范式"。

### Q4: 企业应该从哪一层开始投入？

| 阶段 | 投入层 | 典型动作 | 预期 ROI 周期 |
|------|--------|----------|:------------:|
| **第一阶段** | Prompt Engineering | 建立企业 Prompt 模板库，培训员工 RCTE 框架 | 1-2 周见效 |
| **第二阶段** | Context Engineering | 搭建 RAG 知识库系统，设计信息检索架构 | 1-3 个月 |
| **第三阶段** | Harness Engineering | Agent 基础设施采购/自建，权限体系和审计 | 3-6 个月 |
| **第四阶段** | Graph Engineering | 复杂工作流编排，多 Agent 协作 | 6-12 个月 |

大多数企业 90% 的 AI 价值在前两层就能实现。

### Q5: 同一个 Prompt 在不同的 AI 工具中效果一样吗？

**不一样。** 不同模型对 Prompt 的敏感度差异显著：

| 模型 | 对角色设定敏感度 | 对格式要求敏感度 | 中文理解能力 | 最佳实践 |
|------|:---------------:|:---------------:|:-----------:|----------|
| Claude (Anthropic) | 高 | 中 | 良好 | 详细的 System Prompt + 结构化标签 |
| GPT (OpenAI) | 中 | 高 | 良好 | 明确的输出格式约束 + Few-shot |
| DeepSeek | 中 | 中 | 最佳 | 中文优先 + 低成本批量场景 |

**建议**：同一 Prompt 在 2-3 个工具中交叉验证，找到最适合你场景的模型。

### Q6: AI 能记住我之前跟它说过的话吗？

**同一会话内可以**（受上下文窗口限制，通常 200K Token）。**不同会话之间不共享记忆** —— 除非使用了 Hermes Engineering 层的长期记忆系统（如 mem0、Letta、Hermes Agent 等）。

企业场景中，"跨会话记忆"是 RAG + 用户画像系统的核心场景——将用户在 CRM 中的历史交互、偏好、合同信息注入每次 AI 交互的上下文。

---

## 6. 附录：六层工程体系速查表

| 层级 | 核心问题 | 代表工具/系统 | 企业成熟度 | 学习优先级 |
|------|----------|-------------|:----------:|:----------:|
| **Prompt Engineering** | 怎么和 AI 说话 | ChatGPT / Claude / DeepSeek | ★★★★★ 高度成熟 | 🔴 第1优先级 |
| **Context Engineering** | 给 AI 看什么信息 | Claude Code / mem0 / RAG 框架 | ★★★★☆ 快速成熟中 | 🔴 第2优先级 |
| **Harness Engineering** | Agent 的身体（运行时） | Claude Code / Codex / DeerFlow | ★★★☆☆ 2025年成为焦点 | 🟡 第3优先级 |
| **Hermes Engineering** | 长运行个人 Agent | OpenClaw / Hermes Agent | ★★☆☆☆ 早期阶段 | 🟢 关注即可 |
| **Loop Engineering** | Agent 如何思考和决策 | Agent Loop / LangGraph | ★★★★☆ 范式已成熟 | 🟡 第4优先级 |
| **Graph Engineering** | Agent 流程编排 | LangGraph / n8n+AI | ★★★★☆ 快速成熟中 | 🟡 第5优先级 |

**企业成熟度说明**：
- ★★★★★：有成熟的工具市场和最佳实践，可直接采购使用
- ★★★★☆：工具成熟，但需要专业团队集成和定制
- ★★★☆☆：工具在快速迭代中，需要技术评估和前瞻布局
- ★★☆☆☆：前沿研究阶段，适合技术储备，不适合生产投入

---

## 7. 下次课预告

| 项目 | 内容 |
|------|------|
| **课程主题** | AI 办公自动化 —— 将 Prompt Engineering 应用到日常文档、表格和演示文稿 |
| **核心内容** | 用 AI 辅助 Word 文档撰写 / Excel 数据分析 / PPT 大纲生成 / 邮件撰写与润色 |
| **前置准备** | 确保 VSCode + Cline + DeepSeek 环境可用（本次作业2），准备日常办公中的文档/表格/PPT 素材 |
