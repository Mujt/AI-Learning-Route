# 第1周 第2课：从 Prompt Engineering 到 Agent 工程体系

> **本课面向双轨受众**：💼 企业管理者/投资人 + 🎓 零基础学习者。
> **本课定位**：上半部分建立AI工程的完整技术栈视野（Prompt→Context→Harness→Hermes→Loop→Graph），下半部分深入 Prompt Engineering 实操。

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **课程名称** | AI 时代能力培养 |
| **周次** | 第1周 |
| **课次** | 第2课 |
| **课程主题** | 从 Prompt Engineering 到 Agent 工程体系 + Prompt Engineering 深入 |
| **课程时长** | 3 小时（1.5 小时讲解 + 1.5 小时实操） |
| **前置课程** | 第1课：AI 的发展与未来（已注册 AI 工具账号） |
| **适合人群** | 💼 科技中小企业/大厂管理者、投资人、股东 · 🎓 零基础、非计算机专业大学生 |

---

## 二、学习目标

完成本节课后，你应该能够：

**💼 企业决策者**：
- 理解完整的 AI 工程技术栈：Prompt Engineering → Context Engineering → Harness Engineering → Hermes Engineering → Loop Engineering → Graph Engineering
- 知道 Claude Code 属于哪一层技术，Agent 到底是什么概念，以及各层代表了什么样的企业级能力
- 理解 Prompt Engineering 作为企业"精准管理能力"的战略价值
- 掌握 RCTE 框架，并能将其转化为企业内部的 Prompt 标准化模板
- 能够在本地搭建 VSCode + Claude + DeepSeek 的开发环境
- 了解如何基于 Prompt Engineering 安全地操作企业数据库

**🎓 零基础学习者**：
- 理解从 Prompt 到 Agent 的完整技术演进逻辑
- 掌握 RCTE 提示词框架和至少 6 种常见 Prompt 技巧
- 独立完成用 AI 辅助论文写作、代码编写、方案设计等实际任务
- 能够搭建 AI 编码环境并完成数据库操作实操

---

## 三、课前准备

| 准备事项 | 说明 |
|----------|------|
| AI 工具账号 | 已注册 ChatGPT、Claude、DeepSeek 中至少 2 个（第1课已完成） |
| 本地环境 | 安装 VSCode、Python 3.9+、MySQL 8.0+（课上会统一指导） |
| 专业相关素材 | 准备一个自己专业领域的场景，课堂实操会用 |
| 心态准备 | 前半部分建立认知框架，后半部分动手实操 |
| **企业学员附加** | 准备 1-2 个企业中使用 AI 的实际场景案例 |

---

## 四、第一部分：AI 工程体系全景 —— 从 Prompt 到 Agent

> 在深入学习 Prompt Engineering 之前，我们首先需要建立完整的 AI 工程体系认知。当前（2026年）的 AI 技术已经从"写好提示词"进化到了"构建自主运行的智能系统"。以下六层工程体系，从底层到顶层，逐层代表了 AI 能力的递进。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI 工程体系六层金字塔                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                        ┌──────────────┐                              │
│                        │ Graph        │  ← 状态图编排（LangGraph）     │
│                        │ Engineering  │     Agent流程可恢复、可审计     │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Loop         │  ← Agent 循环引擎             │
│                        │ Engineering  │     observe→think→act        │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Hermes       │  ← 个人长运行 Agent           │
│                        │ Engineering  │     记忆+Skills+消息入口       │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Harness      │  ← Agent 运行时基础设施        │
│                        │ Engineering  │     工具注册+权限+会话+追踪     │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Context      │  ← 信息环境工程                │
│                        │ Engineering  │     上下文设计+组装+管理        │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Prompt       │  ← 指令设计工程                │
│                        │ Engineering  │     最基础、最核心的起点         │
│                        └──────────────┘                              │
│                                                                     │
│   关键工具: Claude Code 横跨 Context/Harness/Loop/Graph 四层          │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.0.1 第一层：Prompt Engineering（提示词工程）—— 怎么和 AI 说话

**定义**：Prompt Engineering 是设计精准、高效的自然语言指令，让大语言模型产出高质量、可预期输出的工程实践。

**技术原理**：

大语言模型本质上是"下一个 Token 预测器"。当你输入一段 Prompt，模型并非"理解"你的意图，而是在其训练数据的统计规律中，找到最可能的续写方向。**Prompt 的作用，就是对这个续写方向施加精确的约束和引导。**

```
无 Prompt（纯续写）：
  输入："人工智能的未来"
  输出："将会非常美好，人类将与机器和谐共处..." (不可控的续写)

有 Prompt（精准引导）：
  输入："请用200字，从三个维度（技术/商业/社会）分析人工智能的未来。格式：每段用标题开头。"
  输出：
  技术维度：...
  商业维度：...
  社会维度：...                (可控、结构化的输出)
```

**核心组件**：

| 组件 | 作用 | 示例 |
|------|------|------|
| **Role（角色）** | 设定 AI 的身份和专业领域 | "你是一位资深 Python 后端工程师" |
| **Context（上下文）** | 提供背景信息和约束条件 | "项目使用 FastAPI + PostgreSQL" |
| **Task（任务）** | 清晰描述要完成的输出 | "请实现一个用户登录接口" |
| **Format（格式）** | 指定输出的结构 | "用 JSON 格式输出，包含 username/password/email" |
| **Constraints（约束）** | 明确边界 | "不使用第三方库，代码注释用中文" |
| **Examples（示例）** | 提供参考范例 | "参考以下格式：[示例]" |

**代表工具**：ChatGPT、Claude、Gemini、DeepSeek 等所有对话式 AI —— Prompt Engineering 是所有 AI 交互的基础。

> 📊 **企业视角**：Prompt Engineering 是 ROI 最快见效的 AI 能力。一个优化后的 Prompt 可以将客服回复准确率从 60% 提升到 90%，而不需要任何技术开发。

---

### 4.0.2 第二层：Context Engineering（上下文工程）—— 给 AI 看什么、看多少、怎么看

**定义**：Context Engineering 是设计和管理 AI 在执行任务过程中能"看到"的完整信息环境的工程实践，从"写指令"升级为"设计信息架构"。

**技术原理**：

Prompt Engineering 只关心"指令怎么写"，但模型在每一步推理时依赖的不只是指令——还有对话历史、工具定义、检索结果、记忆提取、用户偏好等全部信息。Context Engineering 的核心挑战是：**模型的上下文窗口有限（通常 200K Token），但 Agent 运行过程中会产生大量信息**。如何在此限制内，让模型每一步都拥有做出正确判断所需的全部信息？

```
Prompt Engineering 只管理 "System Prompt" 方块
Context Engineering 管理的是整个信息环境：

┌─────────────────────────────────────────────────────────┐
│                 Context Window (200K Token)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ System       │  │ Conversation │  │ Tool         │   │
│  │ Prompt       │  │ History      │  │ Definitions  │   │
│  │ 角色+规则    │  │ 多轮对话历史  │  │ 工具名+描述  │   │
│  │ ~2K Token    │  │ ~5-50K Token │  │ ~2-10K Token │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Retrieved    │  │ Memory       │  │ Structured   │   │
│  │ Context      │  │ Retrieval    │  │ Instructions │   │
│  │ RAG检索结果  │  │ 长期记忆提取  │  │ 输出格式约束  │   │
│  │ ~3-10K Token │  │ ~1-5K Token  │  │ ~1K Token    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**三大核心策略**：

| 策略 | 原理 | 技术手段 | 解决什么问题 |
|------|------|----------|-------------|
| **上下文压缩** (Compaction) | 将冗长的对话历史或工具输出"压缩"为精炼摘要，保留关键信息 | LLM 自动摘要、滑动窗口截断、关键信息提取 | 对话过长超出窗口时不会"失忆" |
| **上下文选择** (Selection) | 根据当前任务从所有可用上下文中只选择最相关的部分 | 语义相似度匹配、优先级排序、RAG 检索 | 不是所有信息都值得占 Token（成本+注意力） |
| **上下文结构化** (Structuring) | 用 XML 标签、Markdown 标题、优先级标记组织上下文 | `<system>...</system>` 标签分层、frontmatter元数据 | 模型能快速定位关键信息而非迷失在海量文本中 |

**上下文结构化的实际示例**：

```
<system_instructions>
  你是一个数据分析助手。始终先理解数据再给出建议。
  安全规则：不要执行 DROP/TRUNCATE 操作，不要暴露数据库连接串。
</system_instructions>

<tool_definitions>
  <tool name="query_database">
    <description>执行SELECT查询</description>
    <parameters>sql: string</parameters>
  </tool>
</tool_definitions>

<conversation_history>
  <user>帮我分析上个月的销售趋势</user>
  <assistant>好的，我先查询数据库...</assistant>
  <tool_result>rows: 350, avg_sale: ¥1,250</tool_result>
</conversation_history>

<retrieved_context priority="high">
  上个月销售数据摘要：总销售额 ¥437,500，环比增长 12.3%...
</retrieved_context>

<current_task>
  基于上述分析结果，生成一份 CEO 级别的销售趋势报告
</current_task>
```

**代表工具/系统**：
- **Claude Code**：内置了 Context Compaction 机制，会自动将冗长的工具输出压缩为摘要再送入模型
- **mem0 / Letta**：提供独立的记忆层，将对话中的重要信息提取存储，跨会话复用
- **LangChain Hub**：提供 Prompt + Context 的模板管理和版本控制

> 📊 **企业视角**：Context Engineering 直接决定企业 RAG 系统的质量天花板。好的 Chunking 策略 + 上下文结构化可以让检索准确率从 60% 提升到 95%。这也是为什么"买了 RAG 工具但效果不好"的瓶颈往往不在模型、不在向量库，而在上下文设计。

---

### 4.0.3 第三层：Harness Engineering（根基工程）—— Agent 的身体

**定义**：Harness Engineering 是构建 Agent 运行时基础设施的工程实践，为 Agent 提供工具注册、权限控制、会话管理、上下文压缩、钩子拦截、追踪日志等"身体能力"。

**技术原理**：

裸 Agent Loop（一个 while 循环 + LLM + 工具列表）可以跑出令人印象深刻的 Demo，但一到生产环境就会暴露出无数问题：工具调用失败无重试、模型输出未校验、API Key 暴露在日志中、Token 消耗失控…… Harness Engineering 的核心思想是：**Agent 的能力很大一部分来自它的 harness（底座），而不是模型本身**。

```
裸 Agent Loop                 Agent Harness（完整运行时）
──────────────────────        ──────────────────────────────
用户输入                       用户输入
  ↓                              ↓
LLM 思考                   ┌── Permission Gate ── 权限校验
  ↓                        │
调用工具            →       │   Tool Registry ── 注册/发现/版本管理
  ↓                        │
工具执行                    │   Hook System ── 调用前/后/错误拦截
  ↓                        │
LLM 回答                    │   Context Compaction ── 超出窗口时自动压缩
  ↓                        │
输出                         │   Session Store ── 状态持久化/断点续执行
                            │
代码量: ~100行                │   Trace/Log ── 每一步的可审计追踪
                            │
                            └── Agent Loop Engine
                            
                            代码量: 数千到数万行 (Claude Code级别)
```

**六大核心组件详解**：

| 组件 | 技术原理 | 重要技术改进 | 没有它会怎样 |
|------|----------|-------------|-------------|
| **Tool Registry** | 统一注册、发现、版本管理所有工具，支持 MCP 协议标准接入 | MCP 协议：工具不再硬编码，而是通过标准化接口动态发现和调用 | 工具散落各处，换一个 AI 模型就需要重写所有工具集成 |
| **Permission Gate** | 在敏感操作（删文件/发邮件/调用支付）前拦截，请求用户确认 | Claude Code 的四级权限模型：Allow/Ask/Deny/AskOnce | Agent 可能擅自删除文件、发送错误邮件、超支 API 费用 |
| **Session Store** | 持久化 Agent 的完整会话状态（上下文/工具调用记录/中间结果） | Redis/PostgreSQL 持久化 + 断点恢复，支持跨设备续执行 | Agent 崩溃后所有上下文丢失，无法恢复 |
| **Context Compaction** | 当对话历史超出模型上下文窗口时，自动压缩/摘要，保留关键信息 | 分层压缩策略：先压缩工具输出，再压缩早期对话，最后压缩当前任务 | 多轮对话后模型"失忆"或 API 费用暴涨 |
| **Hook System** | 在 Agent 执行关键节点（调用前/后/错误/会话结束）插入自定义逻辑 | Claude Code Hooks：PreToolUse/PostToolUse/Notification/Stop | 无法实现日志审计、合规检查、自定义安全策略 |
| **Trace/Log** | 记录每一步的输入、输出、工具调用、Token 消耗、耗时 | OpenTelemetry 标准集成、结构化日志（JSON 格式，非纯文本） | 出问题时无法排查，无法评估 Agent 行为质量 |

**代表工具/系统**：

| 系统 | 定位 | 关键 Harness 能力 |
|------|------|------------------|
| **Claude Code** | Anthropic 官方 Coding Agent CLI | Tool Registry (MCP)、Permission Gate (四级权限)、Hooks、Context Compaction、Subagents |
| **Codex (OpenAI)** | OpenAI 编程 Agent 平台 | Sandbox 执行、Approval 流程、MCP 支持、多入口 (App/CLI/Web) |
| **DeerFlow (字节跳动)** | 通用 SuperAgent Runtime | Sandbox、Memory、Skills、Subagents、Message Gateway |
| **LangGraph** | 状态图编排框架 | Checkpointing、状态持久化、可恢复执行、人工审批节点 |

> 📊 **企业视角**：Harness Engineering 是区分"能做 Demo"和"能上生产"的分水岭。2025 年 Harness Engineering 论文 (arXiv:2605.13357) 首次将其定义为一门独立工程学科。企业采购 AI 工具时，应重点评估其 Harness 成熟度——权限控制、审计日志、错误恢复——而非只看模型能力。

---

### 4.0.4 第四层：Hermes Engineering（信使工程）—— 长运行的记忆型个人 Agent

**定义**：Hermes Engineering 是以 Hermes Agent（NousResearch 开源项目）为代表的长运行、本地优先、具备长期记忆和跨应用能力的个人 Agent 工程范式。名称来源于古希腊神话中的信使之神赫尔墨斯。

**技术原理**：

前三层（Prompt/Context/Harness）构建了 Agent 的"单次任务执行能力"。但一个真正有用的个人 Agent 需要：**在数天、数周甚至数月内持续运行，记住用户偏好，跨不同应用和平台完成任务，并在离线时仍能收到消息并响应**。这需要一套全新的能力层：

```
传统 Harness Agent                    Hermes-style Personal Agent
──────────────────                    ─────────────────────────────
单次会话执行                         长运行 (Always-On)
启动 → 执行 → 结束                   持续监听 → 自主触发 → 后台执行
                                     (类似操作系统的守护进程)
                                    
短期上下文 (当前对话)                 长期记忆 (Long-term Memory)
重启后丢失                           跨会话/跨设备记住用户偏好
                                    记忆系统持续更新和蒸馏

单一入口 (CLI/Web)                   多消息入口 (Multi-Platform Gateway)
只能从固定界面交互                    WhatsApp/Telegram/Slack/飞书/微信
                                     用户在任何平台发消息都能触发 Agent

工具限于当前环境                     跨应用能力 (Cross-App Skills)
只能调用本地或API工具                 Skills 系统：可复用的操作手册
                                     一次编写，多场景复用
```

**核心组件**：

| 组件 | 技术原理 | 代表实现 |
|------|----------|----------|
| **长期记忆系统** | 将对话中的重要信息提取为结构化记忆（偏好/事实/关系），存储至向量数据库；每次新任务时检索相关记忆注入上下文 | Hermes Agent 的三层记忆：短期(会话上下文)→工作(当前任务)→长期(跨会话持久化) |
| **Skills 系统** | 每个 Skill 是一份小型操作手册（SKILL.md），包含何时使用、步骤、脚本、验收标准。Agent 按需加载 Skills 作为操作指导 | Claude Code Skills、OpenClaw Skills、Hermes Agent Skills |
| **多平台消息网关** | 统一的消息路由层，将 WhatsApp/Telegram/Slack/Discord/飞书等消息统一转换为 Agent 输入，Agent 回复由网关分发到对应平台 | OpenClaw Channel System、Hermes Message Gateway |
| **心跳与恢复** | 定期心跳检测 + 任务状态持久化。如果 Agent 进程崩溃，重启后能从上次中断点继续执行 | CyberClaw 心跳机制、OpenClaw State Recovery |

**代表工具/系统**：

| 系统 | 定位 | 关键 Hermes 能力 |
|------|------|-----------------|
| **OpenClaw** | 本地优先个人 Agent | Skills、消息入口、系统工具、本地长运行 |
| **Hermes Agent** | 自托管个人 Agent | 长期记忆、Skills、Toolsets、多平台消息网关 |
| **CyberClaw** | 透明可控 Agent | 全行为审计、两段式安全调用、双水位记忆、心跳任务 |

> 📊 **企业视角**：Hermes Engineering 代表了 AI 从"生产力工具"向"个人操作系统"的进化。对企业而言，这意味着每个知识工作者未来都会拥有一个"数字影子"——它记住你的所有工作上下文，在你休假时能代替你回答 80% 的日常问题。

---

### 4.0.5 第五层：Loop Engineering（循环工程）—— Agent 如何思考和决策

**定义**：Loop Engineering 是设计 Agent 核心推理循环的工程实践，决定了 Agent 在每一步如何观察状态、思考选项、做出决策、执行行动、评估结果。

**技术原理**：

Agent 的本质区别在于"循环"——不是一问一答，而是**不断迭代直到完成任务**。Loop Engineering 决定了这个循环的质量和可靠性。

```
标准 Agent Loop：

┌─────────────────────────────────────────────────────┐
│                                                     │
│  1. 观察 (Observe)                                   │
│     └─ 读取当前状态：用户说了什么？上一步结果是什么？    │
│                                                     │
│  2. 思考 (Think)                                     │
│     └─ LLM 推理：我需要什么信息？应该调用哪个工具？     │
│                                                     │
│  3. 决策 (Decide)                                    │
│     ├─ 如果信息充足 → 生成最终答案                     │
│     ├─ 如果需要更多信息 → 选择工具，构造参数            │
│     └─ 如果超出能力 → 请求人工介入                     │
│                                                     │
│  4. 执行 (Act)                                       │
│     ├─ 调用工具                                       │
│     └─ 等待工具返回结果                                │
│                                                     │
│  5. 反馈 (Feedback)                                   │
│     └─ 工具结果重新注入上下文 → 回到步骤1               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Loop 设计的关键参数**：

| 参数 | 作用 | 典型值 | 调优原则 |
|------|------|--------|----------|
| **max_steps** | 最大循环步数，防止无限循环 | 10-50 | 简单任务设低，复杂任务设高。超过限制时强制输出当前状态 |
| **timeout** | 单步超时（秒） | 30-120s | 工具调用可能很慢（数据库查询/文件处理），需要合理超时 |
| **tool_call_limit** | 单次可调用的工具数量上限 | 1-5 | 过多工具调用会增加 Token 消耗，且可能导致模型注意力分散 |
| **retry_on_error** | 工具失败时重试次数 | 1-3 | 网络抖动导致的临时失败值得重试，但逻辑错误不应重试 |
| **human_in_the_loop** | 在哪些节点插入人工审批 | 敏感操作前 | 删除/付款/发送邮件 → 必须审批。查询/读取 → 可自动 |

**Loop 范式演进**：

| 范式 | 全称 | 核心思路 | 代表实现 | 适用场景 |
|------|------|----------|----------|----------|
| **ReAct** | Reasoning + Acting | 推理和行动交替：Think → Act → Observe → Think | 最基础的 Agent Loop | 通用任务 |
| **Plan-and-Execute** | 先规划再执行 | 先完整规划所有步骤，再逐步执行。执行中发现偏差回到规划 | LangGraph 预规划模式 | 步骤明确的任务 |
| **Reflexion** | 自我反思 | 每次执行后做"事后分析"，将反思结果存入长期记忆供未来参考 | 带 Evaluator 的 Agent | 需要持续改进的任务 |
| **ReWOO** | Reason WithOut Observation | 先一次性规划全部工具调用，再并行执行。减少 LLM 调用次数（省钱提速） | smolagents CodeAgent | 工具调用间不依赖彼此结果的场景 |

**Claude Code 中的 Loop Engineering**：
Claude Code 使用了一个高度优化的 Agent Loop，包含以下关键设计：
- **条件性工具选择**：不是每次都列出所有工具，而是根据任务类型动态激活工具子集
- **上下文感知的停止条件**：当检测到任务已实际完成（而非 LLM 说"完成了"），自动终止循环
- **子代理分发**：复杂任务自动拆分为子任务，分发到独立子代理并行执行
- **渐进式权限**：第一步先以只读模式运行，确认理解任务后才开放写入权限

> 📊 **企业视角**：Loop Engineering 是 Agent 可靠性工程的核心。企业场景中最怕的就是 Agent 进入死循环或做出错误决策后继续滚雪球。一个好的 loop 设计 = 设置合理的 max_steps + 关键节点 human_in_the_loop + 异常检测与熔断。

---

### 4.0.6 第六层：Graph Engineering（图工程）—— Agent 工作流的可编排化

**定义**：Graph Engineering 是使用状态图（State Graph）来编排 Agent 工作流的工程实践——将 Agent 的工作流建模为节点（Node）+ 边（Edge）+ 条件分支（Conditional Edge），使 Agent 的行为可预测、可恢复、可审计。

**技术原理**：

Agent Loop 是线性的（while 循环），但真实企业工作流往往需要**分支、并行、回退、暂停审批**。Graph Engineering 用"图"来建模这些复杂流程。

```
Agent Loop 模式                        Graph Engineering 模式
────────────────                       ──────────────────────
                                      
  START → Agent → Tools → Agent ...    [条件分支示例]
               ↻ 循环                     START
                                          ↓
                                       ┌──────┐
                                       │Router│ ← 第一步：路由判断
                                       └──┬───┘
                              ┌───────────┼───────────┐
                              ↓           ↓           ↓
                         ┌────────┐ ┌────────┐ ┌────────┐
                         │Research│ │Analysis│ │Execute │
                         │ 研究   │ │ 分析   │ │ 执行   │
                         └───┬────┘ └───┬────┘ └───┬────┘
                             │          │          │
                             └──────────┼──────────┘
                                        ↓
                                   ┌──────────┐
                                   │ Reviewer │ ← 审核节点
                                   └────┬─────┘
                                  ┌─────┴─────┐
                                  ↓           ↓
                             通过          驳回 (回到上游)
                                  ↓           ↓
                               ┌──────┐  重新执行
                               │ END  │
                               └──────┘
```

**核心概念**：

| 概念 | 技术含义 | 商业含义 |
|------|----------|----------|
| **State（状态）** | 图中流转的数据对象，每个节点读取/修改 State | 一个"数字工单"，记录工作流中所有已产生的信息和决策 |
| **Node（节点）** | 一个独立的处理单元（LLM思考/工具调用/人工审批） | 一个"工作步骤"，映射到企业流程中的岗位或操作 |
| **Edge（边）** | 节点间的固定流转路径 | 工作流中的必经流程（如：合同生成后 → 必须法务审批） |
| **Conditional Edge（条件边）** | 根据条件动态选择下一个节点 | 审批通过 → 执行；审批驳回 → 退回修改 |
| **Checkpoint（检查点）** | 在每个节点后自动保存 State | 工作流可随时暂停/恢复/回放——企业合规审计的刚需 |
| **Human-in-the-loop** | 某节点执行前等待人工确认 | 关键决策的人类审批阀 |

**核心技术改进**：

- **断点续执行（Persistence）**：LangGraph 的 Checkpointer API。Agent 在任意步骤崩溃或暂停后，可以从最近的 Checkpoint 恢复，而非从头开始。
- **并行扇出（Fan-out）**：一个 Supervisor 节点同时触发多个 Worker 节点并行执行，然后通过 Fan-in 节点收集结果。多 Agent 协作的核心编排机制。
- **流式事件（Streaming Events）**：每个节点的执行状态以事件流方式实时推送，前端可展示"当前正在执行步骤 3/7：合同审查中..."。

**代表工具**：

| 工具 | 核心能力 | 适用场景 |
|------|----------|----------|
| **LangGraph** | 完整的 StateGraph 框架，支持 Checkpoint/Human-in-the-loop/Streaming | 复杂企业工作流的 Agent 编排 |
| **Claude Code Subagents + Hooks** | 子代理分发 + Hook 拦截 = 隐式的工作流图 | Coding Agent 工作流 |
| **n8n + AI** | 可视化的低代码工作流编排 + LLM 节点 | 企业内部自动化 |

> 📊 **企业视角**：Graph Engineering 是最接近"企业流程数字化"的 AI 工程层。它把 AI 的"黑箱决策"变成了"可审计的流转图"。对于金融、医疗、法律等强监管行业，Graph Engineering 是 AI 落地的必要条件——监管机构需要看到的是可以被审计的工作流，而不是一个无法解释的 AI 输出。

---

### 4.0.7 六层体系总结：Claude Code 横跨了哪些层？

```
Claude Code 在六层体系中的定位：

  Prompt Engineering     ✅ 用户通过 System Prompt/Hooks 定义行为
  Context Engineering    ✅ 自动 Tool Output 压缩、对话历史管理
  Harness Engineering    ✅ Tool Registry (MCP)、Permission Gate (四级)
                            Hook System、Session持久化、Subagents
  Hermes Engineering     ❌ 不包含长期记忆、多消息平台网关
                            （Claude Code 是按需启动的 CLI，非常驻）
  Loop Engineering       ✅ 高性能 Agent Loop、条件工具激活
                            Subagent 分发、渐进式权限
  Graph Engineering      ✅ (部分) Subagents + Hooks 构成隐式工作流图
                            Pipeline 模式（多个 subagent 链式协作）

  核心定位：Claude Code 主要覆盖 Context / Harness / Loop 三层。
  它是目前最好的 Agent Harness 学习样本。
```

**Agent 到底是什么？—— 结合六层体系回答**：

> **Agent（智能体）不是一个技术、不是一种模型、不是一个框架。Agent 是一个系统——它整合了 Prompt Engineering（理解任务）、Context Engineering（信息环境）、Harness Engineering（运行时能力）、Hermes Engineering（记忆和持久化）、Loop Engineering（自主推理循环）、Graph Engineering（可编排工作流）的完整系统。**
>
> 简单说：**当 Prompt Engineering 写出了指令，Context Engineering 提供了信息，Harness Engineering 给了它手脚，Hermes Engineering 给了它记忆，Loop Engineering 给了它大脑，Graph Engineering 让它可以被编排——这六者合在一起，才构成了一个真正可用的 Agent。**

---

以上是 AI 工程体系的完整技术栈。初学者从 Prompt Engineering 入手（本节课的核心），企业决策者需要了解整个金字塔以评估技术成熟度和投资方向，开发者则可以沿着这个金字塔逐层攀登。

---

## 五、第二部分：Prompt Engineering 深入详解

> 以下内容基于原有讲义深入展开。在第 4.0 节建立了完整的六层技术栈认知后，现在回到最基础也最核心的一层：Prompt Engineering。

### 5.1 什么是 Prompt Engineering？

#### 5.1.1 基本定义

**Prompt（提示词）** 是你与 AI 对话时输入的指令。**Prompt Engineering（提示词工程）** 是设计有效指令的方法论。

> 💡 **一句话理解**：好的 Prompt 像一个精准的任务说明书，差的 Prompt 像一个模糊的口头交代。

#### 5.1.2 为什么 Prompt Engineering 如此重要？

```
❌ 差的 Prompt：
"帮我写个方案"

✅ 好的 Prompt：
"你是一位资深建筑设计师（Role），
我要在大学城旁开一个面向学生的现代风格咖啡馆（Context），
面积200平米，预算50万（Constraints）。
请为我设计一份完整的咖啡馆方案（Task），包括：
1. 空间布局规划 2. 设计风格说明 3. 材料选择 4. 灯光设计
参考Manner Coffee的简约工业风（Examples）。"
```

两个 Prompt 针对同一个 AI 模型，输出质量的天壤之别，就是 Prompt Engineering 要解决的问题。

> 📊 **企业视角**：Prompt Engineering 是企业 AI 投入中 ROI 最快的环节。一个经过优化的客户服务 Prompt 可以直接将自动回复准确率从 60% 提升到 90%，而成本几乎为零——你不需要训练新模型，不需要接入新工具，只需要更好的 Prompt。

---

### 5.2 RCTE 框架详解

> RCTE 是 Prompt Engineering 中最核心、最实用的框架。所有复杂 Prompt 都基于此构建。

```
┌─────────────────────────────────────────┐
│  R — Role       你希望AI扮演什么角色     │
│  C — Context    提供什么背景信息         │
│  T — Task       要完成什么具体任务       │
│  E — Example    给出什么示例参考         │
└─────────────────────────────────────────┘
```

**R — Role（角色）**：设定 AI 的身份、专业领域、语气风格。

| 角色设定 | 效果 | 适用场景 |
|----------|------|----------|
| "你是一位资深建筑设计师" | AI 使用建筑专业术语和设计思维 | 设计类任务 |
| "你是一位有10年经验的 Python 工程师" | AI 写出更规范、更有工程感的代码 | 编程任务 |
| "你是一位麦肯锡咨询顾问" | AI 使用结构化分析框架（MECE/金字塔原理） | 商业分析 |
| 不设定角色 | AI 用最通用的方式回答，缺乏专业深度 | 简单查询 |

**C — Context（上下文）**：提供任务的背景信息、目标受众、限制条件。

```
好的 Context 包括：
  • 目标受众是谁？（写给 CEO 看 vs 写给技术团队看，风格完全不同）
  • 使用场景是什么？（内部备忘录 vs 对外发布稿，语气完全不同）
  • 有什么限制？（字数/预算/时间/技术栈/合规要求）
  • 已经尝试过什么？（避免 AI 给出重复的方案）
```

**T — Task（任务）**：要输出的具体内容，越精确越好。

| 模糊的 Task | 精确的 Task |
|------------|------------|
| "帮我分析这个方案" | "从成本、工期、安全性三个维度评估这个施工方案，每个维度给出0-5分的评分和具体改进建议" |
| "写一篇关于AI的文章" | "写一篇面向中小型企业CEO的800字文章，主题是'2026年AI落地的5个关键决策'" |
| "做个PPT" | "生成一个10页的季度汇报PPT大纲，每页包含标题+3个要点+建议的图表类型" |

**E — Example（示例）**：提供一个或多个参考范例，帮助 AI 精确理解你的期望格式和风格。

```
Task: 写一份竞品分析报告

提供 Example：
"参考以下格式：

## 竞品名称
### 一句话定位
### 核心优势（3个要点）
### 核心劣势（3个要点）
### 对我方的威胁等级（1-5）
### 应对策略建议"

效果：AI 会严格按照这个模板输出，而非自由发挥。
```

> 📊 **企业视角**：RCTE 框架是企业 Prompt 标准化的核心工具。建议为每个高频场景（周报/客户邮件/竞品分析/内部通知）建立 RCTE 模板，新人直接套用，确保全公司 Prompt 质量和输出一致性。

---

### 5.3 常见 Prompt 技巧大全

| 技巧 | 说明 | 示例 |
|------|------|------|
| **分步提问** | 把大任务拆成小步骤 | "首先…然后…最后…" |
| **设定格式** | 明确输出格式 | "请用表格形式输出" / "请用 Markdown 格式" |
| **思维链 (Chain-of-Thought)** | 要求 AI 展示推理过程 | "请一步步思考，先分析问题，再给出结论" |
| **Few-shot** | 提供 2-3 个示例 | "参考以下两个案例的风格…" |
| **负面约束** | 明确不要什么 | "不要使用过于专业的术语" / "不使用第三方库" |
| **角色扮演** | 给 AI 设定专业身份 | "你是一位有10年经验的 Python 工程师" |
| **迭代优化** | 根据回答持续调整 Prompt | "上一个版本太简略了，请展开第三部分" |
| **结构化输出** | 强制 JSON/XML/Markdown 格式 | "输出严格合法的 JSON，不要有其他文字" |

---

### 5.4 不同任务的 Prompt 模板

**写作类**：
```
Role: 你是一位 [领域] 的资深专家
Context: 目标读者是 [读者特征]，他们关心 [核心关切]
Task: 请写一篇关于 [主题] 的 [文体类型]
要求：字数 [800-1000字]，风格 [学术严谨/轻松易读/实操性强]，
      结构 [引言-正文3部分-结论]，包含 [数据/案例/实操建议]
```

**编程类**：
```
Role: 你是一位资深 Python 后端工程师
Context: 项目使用 [框架/库]，运行在 [环境]
Task: 请实现 [功能描述]
要求：代码注释用中文，处理边缘情况（空值、超时等），遵循 PEP 8
```

**分析类**：
```
Role: 你是一位数据分析师
Context: 这是一份 [数据说明]，包含 [字段说明]
Task: 请分析这份数据，找出主要趋势、异常值、可行的优化建议
输出格式：用要点列表，每个要点不超过2行
```

**企业高管摘要类**：
```
Role: 你是一位 CEO 战略顾问
Context: 目标读者是公司董事会（5分钟阅读时间）
Task: 将以下 [技术报告/市场分析] 转化为 CEO 级别的一页摘要
格式：标题（10字以内）+ 3个核心发现（每项30字）+ 决策建议（50字）
```

---

### 5.5 Prompt 优化的 8 个技巧

| 技巧 | 优化前 | 优化后 |
|------|--------|--------|
| **具体化** | "写一个好方案" | "写一个2000字的XX项目方案，包含市场分析、技术路线、财务预测三部分" |
| **结构化** | 一大段文字描述需求 | 用编号/分层/表格组织需求 |
| **给例子** | "写一个专业的邮件" | "参考这个邮件模板：[粘贴示例]" |
| **设约束** | 不提限制条件 | "不使用第三方库" / "控制在500字以内" |
| **定角色** | 直接提需求 | "你是一个XX专家，现在帮我..." |
| **迭代** | 一次 Prompt 不满意就放弃 | "第三点不够具体，请展开并举例说明" |
| **给反馈** | 说"不对" | "这个方案的问题在于XX，请从YY角度重新思考" |
| **链式提问** | 一次性提所有要求 | 分3-5轮：先大纲→逐节展开→最后润色 |

---

## 六、第三部分：VSCode + Claude + DeepSeek 开发环境搭建

> 本节指导你搭建一个高效的 AI 辅助开发环境。无论你是零基础学习者还是企业管理者，拥有这个环境意味着你可以直接让 AI 帮你写代码、分析数据、操作数据库。

### 6.1 环境总览

```
┌─────────────────────────────────────────────────────┐
│                AI 开发环境架构                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐                                   │
│  │   VSCode     │  ← 代码编辑器 + AI 插件            │
│  │   (IDE)      │     GitHub Copilot / Cline /       │
│  │              │     Continue (开源AI助手)           │
│  └──────┬───────┘                                   │
│         │                                           │
│    ┌────┴────┐                                      │
│    │         │                                      │
│    ▼         ▼                                      │
│  ┌───────┐ ┌─────────┐                              │
│  │Claude │ │DeepSeek │  ← AI 模型（通过 API 连接）     │
│  │ API   │ │API      │     Claude: 代码/长文本/推理    │
│  │       │ │         │     DeepSeek: 中文/低成本/备份   │
│  └───┬───┘ └────┬────┘                              │
│      │          │                                    │
│      ▼          ▼                                    │
│  ┌─────────────────────────┐                        │
│  │   你的项目               │                        │
│  │   Python / MySQL / ...  │                        │
│  └─────────────────────────┘                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 6.2 步骤一：安装 VSCode

**Windows/macOS/Linux 全平台**：

1. 浏览器打开 https://code.visualstudio.com
2. 下载对应系统的安装包
3. Windows 用户：双击安装，勾选"添加到 PATH"
4. macOS 用户：拖入 Applications 文件夹
5. 安装完成后打开 VSCode

**必装插件**（打开 VSCode → 左侧扩展图标 → 搜索安装）：

| 插件名称 | 用途 | 必装程度 |
|----------|------|----------|
| **Cline** (原名 Claude Dev) | 在 VSCode 中直接与 Claude/DeepSeek 对话，AI 可以读文件、写代码、执行终端命令 | ⭐⭐⭐ |
| **Continue** | 开源 AI 编程助手，支持多模型切换（Claude/DeepSeek/本地模型） | ⭐⭐⭐ |
| **Python** (Microsoft) | Python 语法高亮、调试、虚拟环境管理 | ⭐⭐⭐ |
| **GitHub Copilot** (可选) | GitHub 官方 AI 补全插件，$10/月 | ⭐⭐ |

### 6.3 步骤二：配置 Cline 插件（连接 Claude + DeepSeek）

**Cline** 是目前 VSCode 中最强的 AI 编码助手。它不只是聊天——它能读你的项目文件、写代码、执行终端命令、帮你 Debug。

**配置 Claude API**：

1. 打开 VSCode → 左侧 Cline 图标（机器人图标）
2. 点击设置图标 → 选择 **API Provider: Anthropic**
3. 填入你的 Anthropic API Key（在 https://console.anthropic.com 申请）
4. Model 选择 **Claude Sonnet 5**（性价比最高）或 **Claude Opus 5**（最强推理）
5. 点击 Done

**配置 DeepSeek API**（国内直连、极低成本）：

1. Cline 设置 → **API Provider: OpenAI Compatible**
2. Base URL：`https://api.deepseek.com`
3. API Key：你的 DeepSeek API Key（在 https://platform.deepseek.com 申请，新用户有免费额度）
4. Model ID：`deepseek-chat`

**配置 Continue 插件（双模型切换方案）**：

Continue 的优势在于可以在同一个对话中自由切换模型——复杂任务用 Claude，批量处理用 DeepSeek。

1. 安装 Continue 插件后，按 `Ctrl+Shift+P` → `Continue: Open Config`
2. 编辑 `config.json`：

```json
{
  "models": [
    {
      "title": "Claude Sonnet 5",
      "provider": "anthropic",
      "model": "claude-sonnet-5-20251001",
      "apiKey": "sk-ant-xxx"
    },
    {
      "title": "DeepSeek V3",
      "provider": "openai",
      "model": "deepseek-chat",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "sk-xxx"
    }
  ]
}
```

### 6.4 备选方案：WorkBuddy + 大模型

**WorkBuddy** 是另一款 AI 工作助手桌面应用，与 VSCode 插件路线互补：

| 对比维度 | VSCode + Cline/Continue | WorkBuddy |
|----------|------------------------|-----------|
| 定位 | 编码场景为主 | 通用工作场景（桌面助手） |
| 安装方式 | VSCode 插件 | 独立桌面应用 |
| 文件操作 | 直接读/写项目文件 | 可操作桌面文件和常用应用 |
| 模型支持 | Claude/DeepSeek/OpenAI | 支持多模型 API |
| 适合人群 | 需要写代码的开发者 | 需要通用 AI 助手的管理者 |

**WorkBuddy 配置步骤**（如有兴趣）：

1. 浏览器打开 https://workbuddy.ai 下载桌面应用
2. 安装后打开 → Settings → API Configuration
3. 填入 DeepSeek API Key（国内可用，低成本）或 Claude API Key
4. 选择默认模型

> **推荐方案**：开发者使用 **VSCode + Cline**（编码场景最强），管理者使用 **ChatGPT/Claude/DeepSeek 网页版**（日常任务），有额外预算可加 **WorkBuddy**（桌面通用助手）。

### 6.5 验证环境

在 VSCode 中新建文件 `test_ai.py`，用 Cline 发送以下 Prompt：

```
请用 Python 写一个简单的函数，功能是输入一个数字列表，返回平均值和中位数。
代码要有中文注释，并附带一个测试用例。
```

如果 AI 能正确生成代码，说明你的环境配置成功。你还可以在 Cline 中继续发送：

```
帮我在终端中运行这段代码，看看输出是否正确。
```

Cline 会直接在你的终端中执行 `python test_ai.py` 并展示结果——这就是 Agent 的核心能力：**从"说"到"做"**。

---

## 七、第四部分：实操 —— 基于 Prompt Engineering 操作 MySQL 数据库

> 本节是一个完整的实操项目：通过 Prompt Engineering 让 AI 安全地操作 MySQL 数据库。**核心教学目标**：理解 Prompt Engineering 在实际开发中的威力 + 掌握数据库权限隔离的安全最佳实践。

### 7.1 实操架构

```
┌──────────┐     Prompt      ┌──────────┐     SQL      ┌──────────┐
│   You    │ ──────────────→ │   AI     │ ──────────→ │  MySQL   │
│ (写Prompt)│ ←────────────── │ (Claude/ │ ←────────── │ Database │
│          │    结果+SQL      │ DeepSeek)│   查询结果   │          │
└──────────┘                 └──────────┘             └──────────┘
                                                          │
                              ┌────────────────────────────┘
                              │  权限隔离设计：
                              │  ┌─────────────┐
                              │  │ ai_readonly  │ ← 只能 SELECT
                              │  │ ai_writer    │ ← 可 INSERT/UPDATE/DELETE
                              │  │ ai_admin     │ ← 可 CREATE/ALTER (慎用)
                              │  │ root         │ ← 仅DBA持有，绝不交给AI
                              │  └─────────────┘
```

### 7.2 步骤一：安装 MySQL 并创建测试数据库

**安装 MySQL**：

- Windows：下载 MySQL Installer (https://dev.mysql.com/downloads/installer)，选择 MySQL Server 8.0
- macOS：`brew install mysql`
- Linux：`sudo apt install mysql-server`

**安装 Python MySQL 驱动**：

```bash
pip install mysql-connector-python
```

**创建测试数据库和权限隔离用户**：

```sql
-- 以 root 身份登录 MySQL
mysql -u root -p

-- 创建测试数据库
CREATE DATABASE ai_test_company;
USE ai_test_company;

-- 创建测试表
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    performance_score INT DEFAULT 0
);

-- 插入测试数据
INSERT INTO employees (name, department, salary, hire_date, performance_score) VALUES
('张三', '技术部', 25000, '2023-03-15', 92),
('李四', '市场部', 18000, '2022-07-01', 85),
('王五', '技术部', 28000, '2021-01-10', 95),
('赵六', '人事部', 15000, '2024-01-20', 78),
('钱七', '市场部', 20000, '2023-09-05', 88),
('孙八', '技术部', 32000, '2020-06-15', 97),
('周九', '财务部', 22000, '2022-11-01', 82),
('吴十', '技术部', 26000, '2023-12-01', 91);

-- 创建权限隔离用户
-- 1. ai_readonly：只能 SELECT（最安全，日常查询用）
CREATE USER 'ai_readonly'@'localhost' IDENTIFIED BY 'ReadOnly123!';
GRANT SELECT ON ai_test_company.* TO 'ai_readonly'@'localhost';

-- 2. ai_writer：可增删改查（中等权限，数据操作需人工确认）
CREATE USER 'ai_writer'@'localhost' IDENTIFIED BY 'Writer456!';
GRANT SELECT, INSERT, UPDATE, DELETE ON ai_test_company.* TO 'ai_writer'@'localhost';

-- 3. 绝不创建 root 级别的 AI 用户！

FLUSH PRIVILEGES;
```

### 7.3 步骤二：编写 AI 数据库操作 Agent

创建文件 `ai_db_agent.py`：

```python
#!/usr/bin/env python3
"""
AI 数据库操作 Agent —— 基于 Prompt Engineering 安全操作 MySQL
核心理念：AI 生成 SQL → 人类审核 → 权限隔离执行
"""

import mysql.connector
from openai import OpenAI
import os

# ==========================================
# 配置区
# ==========================================
# 使用 deepseek（国内直连 + 低成本）
LLM_CLIENT = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key"),
    base_url="https://api.deepseek.com"
)
LLM_MODEL = "deepseek-chat"

# 数据库连接配置 —— 默认使用最安全的只读账户
DB_CONFIG_READONLY = {
    "host": "localhost",
    "user": "ai_readonly",
    "password": "ReadOnly123!",
    "database": "ai_test_company"
}

DB_CONFIG_WRITER = {
    "host": "localhost",
    "user": "ai_writer",
    "password": "Writer456!",
    "database": "ai_test_company"
}

# ==========================================
# Prompt 设计 —— 核心：通过 Prompt 约束 AI 行为
# ==========================================
SYSTEM_PROMPT = """你是一个 MySQL 数据库助手。你的任务是根据用户的自然语言问题生成正确的 SQL 查询。

## 安全规则（硬约束，不可违反）：
1. 你只能生成 SELECT / INSERT / UPDATE / DELETE 语句。绝不生成 DROP / TRUNCATE / ALTER / CREATE 语句。
2. 所有 INSERT / UPDATE / DELETE 语句在生成后，必须要求人类确认后才执行。
3. 如果用户要求删除数据，先建议用户使用 SELECT 查看要删除的数据范围。
4. 生成的 SQL 必须使用参数化查询格式（避免 SQL 注入）。

## 当前数据库结构：
数据库名：ai_test_company
表名：employees
列：
  - id: INT, 主键, 自增
  - name: VARCHAR(100), 员工姓名
  - department: VARCHAR(50), 部门
  - salary: DECIMAL(10,2), 月薪
  - hire_date: DATE, 入职日期
  - performance_score: INT, 绩效评分 (0-100)

## 输出格式：
当用户提出查询需求时，请按以下格式输出：
1. 理解确认：用一句话复述你理解的需求
2. SQL语句：用 ```sql 代码块包裹生成的 SQL
3. 说明：解释这个SQL会返回什么结果
4. 安全提醒：如果是写操作（INSERT/UPDATE/DELETE），标注安全提醒
"""

# ==========================================
# 核心函数
# ==========================================
def ai_generate_sql(user_request: str) -> str:
    """让 AI 根据用户自然语言生成 SQL"""
    response = LLM_CLIENT.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ],
        temperature=0.1  # 低温 = 输出更确定，适合 SQL 生成
    )
    return response.choices[0].message.content


def execute_sql(sql: str, use_writer: bool = False):
    """执行 SQL，自动选择合适的权限级别"""
    config = DB_CONFIG_WRITER if use_writer else DB_CONFIG_READONLY
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(sql)
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return {"affected_rows": cursor.rowcount, "status": "success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()


# ==========================================
# 主交互循环
# ==========================================
def main():
    print("=" * 60)
    print("  🤖 AI 数据库操作助手")
    print("  基于 Prompt Engineering + MySQL 权限隔离")
    print("=" * 60)
    print("\n📋 当前数据库：ai_test_company.employees")
    print("🔒 默认连接账户：ai_readonly (只读)")
    print("📊 已有数据：8 条员工记录")
    print("\n示例查询：")
    print("  · 技术部有哪些员工？平均薪资是多少？")
    print("  · 列出绩效评分高于90的员工")
    print("  · 按部门统计员工人数和平均薪资")
    print("  · 市场部最近入职的员工是谁？")
    print("\n输入 'quit' 退出")
    print("-" * 60)

    while True:
        user_input = input("\n🙋 你的查询：").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue

        # Step 1: AI 生成 SQL
        print("\n🧠 AI 正在分析你的需求...")
        ai_response = ai_generate_sql(user_input)
        print(ai_response)

        # Step 2: 提取 SQL 语句
        import re
        sql_match = re.search(r'```sql\s*(.*?)\s*```', ai_response, re.DOTALL)
        if not sql_match:
            print("❌ AI 未能生成有效的 SQL 语句，请重新描述你的需求")
            continue
        sql = sql_match.group(1).strip()

        # Step 3: 检查是否写操作
        is_write = any(sql.upper().startswith(op) for op in 
                      ["INSERT", "UPDATE", "DELETE"])

        if is_write:
            print(f"\n⚠️  检测到写操作：{sql[:80]}...")
            confirm = input("确认执行此操作？(输入 yes 确认 / no 取消)：").strip()
            if confirm.lower() != "yes":
                print("❌ 操作已取消")
                continue

        # Step 4: 执行 SQL（自动选择权限级别）
        print(f"\n⚡ 执行 SQL (账户：{'ai_writer' if is_write else 'ai_readonly'})...")
        result = execute_sql(sql, use_writer=is_write)

        # Step 5: 展示结果
        if isinstance(result, dict) and "error" in result:
            print(f"❌ 执行失败：{result['error']}")
        elif isinstance(result, list):
            print(f"\n✅ 查询结果（{len(result)} 条记录）：")
            for row in result:
                print(f"  {row}")
        else:
            print(f"\n✅ 操作完成：{result}")


if __name__ == "__main__":
    main()
```

### 7.4 步骤三：运行与测试

**测试用例 1：简单查询**
```
🙋 你的查询：技术部有哪些员工？按薪资从高到低排列
```

AI 应生成类似 SQL：
```sql
SELECT name, salary, hire_date, performance_score 
FROM employees 
WHERE department = '技术部' 
ORDER BY salary DESC;
```
执行后输出技术部员工列表。

**测试用例 2：聚合统计**
```
🙋 你的查询：按部门统计员工人数和平均薪资，只显示平均薪资高于18000的部门
```

AI 应生成：
```sql
SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 18000;
```

**测试用例 3：写操作（触发权限隔离）**
```
🙋 你的查询：给技术部所有绩效高于90的员工加薪10%
```

AI 此时应该：
1. 先生成 SELECT 语句让你查看哪些员工将被加薪
2. 生成 UPDATE 语句，要求你确认
3. 你确认后切换到 `ai_writer` 账户执行

**测试用例 4：权限验证——确保 AI 没有 root 权限**

尝试让 AI 执行 `DROP TABLE employees;` —— 你会看到两个保护层：
1. AI 的 System Prompt 约束：拒绝生成 DROP 语句
2. MySQL 权限隔离：即使 AI 生成了 DROP，`ai_writer` 账户也没有 DROP 权限

### 7.5 实操要点总结

| 环节 | Prompt Engineering 起到的作用 | 安全机制 |
|------|------------------------------|----------|
| **用户输入 → SQL 生成** | 结构化 System Prompt 约束 AI 行为（不生成危险SQL、使用参数化查询、输出特定格式） | Prompt 层面的行为约束 |
| **写操作确认** | AI 识别到写操作时主动标注安全提醒 | 人机协作的决策确认 |
| **SQL 执行** | 根据操作类型自动选择权限账户 | MySQL 三层账户权限隔离 |
| **错误处理** | Prompt 要求 AI 给出"发生了什么"的说明 | 明确错误信息便于排查 |

### 7.6 Prompt Engineering 在数据库操作中的关键原则

1. **硬约束写在 System Prompt 最前面**（"绝不生成 DROP/TRUNCATE"）——这些规则 AI 必须遵守
2. **用结构化的输出格式**（```sql 代码块 + 字段解释）——确保下游系统能可靠解析
3. **低温参数（temperature=0.1）**——SQL 生成需要确定性，不需要创意
4. **先查后改原则**——所有写操作前必须先用 SELECT 确认影响范围
5. **最小权限原则**——AI 永远不应该获得 root 数据库权限

---

## 八、课后作业

### 作业1：RCTE 框架实战（必做）

用 RCTE 框架写 5 个不同场景的 Prompt（学习/生活/工作/编程/企业场景各至少 1 个），在至少 2 个不同的 AI 工具中测试效果，写一篇不少于 400 字的对比笔记。

### 作业2：搭建本地 AI 开发环境（必做）

完成 VSCode + Cline + DeepSeek 的环境搭建，在 Cline 中发送至少 3 条编程相关的 Prompt，截图留证。

### 作业3：数据库操作 Agent 扩展（选做，强烈推荐）

在第七节的 `ai_db_agent.py` 基础上，增加以下功能之一：
- 让 AI 生成数据可视化代码（Matplotlib 图表）
- 增加多表查询支持
- 增加自然语言到 API 调用的转换

### 💼 企业版作业

1. **Prompt 模板审计**：列出你企业中最常用的 5 个 AI 使用场景，为每个场景创建 RCTE 标准模板
2. **权限隔离方案**：参照第七节的 MySQL 权限设计，为你企业的关键系统设计一套 AI 访问权限分级方案

**截止时间**：下次上课前一天晚上 22:00。

---

## 九、拓展阅读

### 🎓 学习者推荐

| 资源 | 链接 | 说明 |
|------|------|------|
| Anthropic Prompt Engineering 指南 | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | 官方权威 |
| OpenAI Prompt Engineering 指南 | https://platform.openai.com/docs/guides/prompt-engineering | 官方指南 |
| Learn Prompting | https://learnprompting.org | 免费系统课程 |
| Cline 官方文档 | https://docs.cline.bot | VSCode AI 插件指南 |

### 💼 企业决策者推荐

| 资源 | 说明 |
|------|------|
| Building Effective Agents (Anthropic) | Agent 设计的纲领性文章 |
| AI Harness Engineering (arXiv:2605.13357) | Harness Engineering 定义性论文 |
| Claude Code 架构分析 | 理解真实 Agent 系统的设计 |
| MCP 官方文档 (modelcontextprotocol.io) | AI 工具连接标准协议 |

---

## 十、常见问题（FAQ）

**Q1: Prompt Engineering → Context → Harness → Hermes → Loop → Graph，我应该从哪一层开始学？**
Prompt Engineering。这是所有上层工程的基础。先学会"怎么和 AI 说话"，再逐层深入。

**Q2: Claude Code 属于哪一层？**
Claude Code 横跨 Context / Harness / Loop / Graph 四层，是目前最完整的 Agent 工程学习样本。

**Q3: Agent 到底是什么？**
Agent 不是一个技术、一个模型或一个框架。它是整合了 Prompt（指令）、Context（信息）、Harness（运行时）、Hermes（记忆）、Loop（循环）、Graph（编排）六层能力的完整系统。简单说：**能自主规划并使用工具完成任务的 AI 系统**。

**Q4: 企业应该从哪一层开始投入？**
Prompt Engineering（ROI最快）→ Context Engineering（RAG系统）→ Harness Engineering（Agent生产化）。大多数企业90%的AI价值在前两层就能实现。

**Q5: 同一个 Prompt 在不同的 AI 工具中效果一样吗？**
不一样。不同模型对 Prompt 的敏感度不同。Claude 对角色设定敏感，GPT 对格式要求敏感，DeepSeek 对中文 Prompt 理解最好。建议同一 Prompt 在 2-3 个工具中交叉验证。

**Q6: AI 能记住我之前跟它说过的话吗？**
同一会话中可以记住上下文（直到超出上下文窗口）。不同会话之间不共享记忆——除非使用了 Hermes Engineering 层的长期记忆系统。

---

## 附录：六层工程体系速查表

| 层级 | 核心问题 | 代表工具/系统 | 企业成熟度 |
|------|----------|-------------|-----------|
| **Prompt Engineering** | 怎么和AI说话 | ChatGPT / Claude / DeepSeek | ★★★★★ 高度成熟 |
| **Context Engineering** | 给AI看什么信息 | Claude Code / mem0 / RAG | ★★★★☆ 快速成熟中 |
| **Harness Engineering** | Agent的身体 | Claude Code / Codex / DeerFlow | ★★★☆☆ 2025年成为焦点 |
| **Hermes Engineering** | 长运行个人Agent | OpenClaw / Hermes Agent | ★★☆☆☆ 早期阶段 |
| **Loop Engineering** | Agent如何思考 | LangGraph / Claude Code | ★★★★☆ 范式已成熟 |
| **Graph Engineering** | Agent流程编排 | LangGraph / n8n+AI | ★★★★☆ 快速成熟中 |

---

> **本节讲义结束。下次课将学习 AI 办公自动化，将 Prompt Engineering 技巧应用到日常文档、表格和演示文稿中。**
>
> **课后作业请在下次上课前一天 22:00 前提交。有任何疑问，在课程群中提问，或直接用 Cline/DeepSeek 搜索答案！**
