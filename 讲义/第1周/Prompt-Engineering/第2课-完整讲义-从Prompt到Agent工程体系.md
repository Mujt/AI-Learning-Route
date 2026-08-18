# 第2课：从 Prompt Engineering 到 Agent 工程体系 —— 完整讲义

> **文档说明**：本文档由原 KB1-KB8 八个知识块合并整理而成，可作为本课完整讲义使用（总时长约 180 分钟）。
>
> **合并整理内容**：
> 1. 按教学顺序合为一册：体系全景 → Prompt/Context → Harness → Loop/Graph → Prompt 实战 → 环境搭建 → 数据库实操 → 总结与作业。
> 2. 修正了原文中的不一致论述：统一为"本课共 8 个 KB"（原文 KB3/KB4 误写"共 4 个 KB"）；修正 KB3 前置知识块与实际内容不符的问题；统一 Claude Code 覆盖层数的前后矛盾表述。
> 3. 工程体系由六层调整为**五层**：**Prompt → Context → Harness → Loop → Graph**。跨会话长期记忆不再作为独立工程学科，归入 Context Engineering 的延伸能力（Harness 的 Session Store 会话持久化 + mem0/Letta 等记忆层工具）。

**目录**

| 部分 | 标题 | 原知识块 |
|------|------|----------|
| 第一部分 | AI 工程体系全景（五层金字塔） | KB1 |
| 第二部分 | Prompt Engineering 与 Context Engineering 深入 | KB2 |
| 第三部分 | Harness Engineering 深度解析 | KB3 |
| 第四部分 | Loop Engineering 与 Graph Engineering 深入 | KB4 |
| 第五部分 | Prompt Engineering 实战详解 | KB5 |
| 第六部分 | 开发环境搭建（VSCode + Claude + DeepSeek） | KB6 |
| 第七部分 | MySQL 数据库操作实操 | KB7 |
| 第八部分 | 课程总结与作业 | KB8 |

---


# 第一部分：AI 工程体系全景（五层金字塔）

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB1 / 本课共8个KB |
| **知识块标题** | 五层AI工程体系概览 |
| **预计时长** | 15分钟 |
| **教学形式** | 理论讲解 |
| **适合人群** | 💼 企业管理者/投资人 + 🎓 零基础学习者 |
| **核心目标** | 建立AI工程的完整技术栈认知框架，理解五层金字塔的层次关系，掌握 Claude Code 在体系中的定位，建立"Agent是五层整合系统"的核心认知 |

---

## 二、五层金字塔总览

当前（2026年）的 AI 技术已经从"写好提示词"进化到了"构建自主运行的智能系统"。以下五层工程体系，从底层到顶层，逐层代表了 AI 能力的递进。每一层建立在下层之上，不可跳跃。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI 工程体系五层金字塔                               │
│                    从"会说话"到"会做事"的完整技术栈                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                        ┌──────────────┐                              │
│                        │ Graph        │  ← 状态图编排（LangGraph）     │
│                        │ Engineering  │     Agent流程可恢复、可审计     │
│                        │ 图工程        │     企业流程数字化的最终形态    │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Loop         │  ← Agent 循环引擎             │
│                        │ Engineering  │     observe→think→act        │
│                        │ 循环工程      │     Agent的"大脑"如何运转      │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Harness      │  ← Agent 运行时基础设施        │
│                        │ Engineering  │     工具注册+权限+会话+追踪     │
│                        │ 根基工程      │     Agent的"身体"——能做什么    │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Context      │  ← 信息环境工程                │
│                        │ Engineering  │     上下文设计+组装+管理        │
│                        │ 上下文工程    │     AI"看到什么、看多少、怎么看" │
│                        └──────┬───────┘                              │
│                               │                                      │
│                        ┌──────┴───────┐                              │
│                        │ Prompt       │  ← 指令设计工程                │
│                        │ Engineering  │     最基础、最核心的起点         │
│                        │ 提示词工程    │     一切AI交互的入口            │
│                        └──────────────┘                              │
│                                                                     │
│   关键工具定位:                                                       │
│   Claude Code 覆盖 Context / Harness / Loop 三层，并在 Graph 层        │
│   提供部分能力（Subagents + Hooks 隐式工作流图）                        │
│   ChatGPT/Claude/DeepSeek 网页版运行在 Prompt Engineering 层           │
└─────────────────────────────────────────────────────────────────────┘
```

### 金字塔解读原则

- **自底向上构建**：每一层的能力依赖下一层提供的基础
- **不可跳跃**：跳过 Context 直接做 Loop，Agent 必然"失忆"
- **入门从底层开始**：Prompt Engineering 是 ROI 最高的入口
- **企业评估从上往下看**：顶层（Graph）代表最成熟的企业级能力

---

## 三、为什么需要理解这五层？—— 从"会用AI"到"构建AI系统"的认知升级

### 3.1 当前 AI 学习的主要误区

| 常见误区 | 实际情况 |
|----------|----------|
| "AI 就是写 Prompt" | Prompt 只是第一层。真正强大的 AI 系统涉及五层整合 |
| "Agent 就是一个 while 循环调 LLM" | 裸 Loop 只有 ~100 行代码，但生产级 Agent 需要五层完备支撑（数千到数万行） |
| "买个 RAG 工具就能做好企业 AI" | RAG 只是 Context Engineering 的一个子集。上下文设计不当，RAG 效果远低于预期 |
| "用最好的模型就够了" | 模型能力只是上限，五层工程决定了实际能达到的下限 |

### 3.2 认知升级路径

```
会用 AI                   懂 AI 原理                构建 AI 系统
────────────────────── ────────────────────── ──────────────────────
使用 ChatGPT 网页版       理解 Prompt 设计原理       搭建企业 Prompt 模板库
问一个问题 → 得到一个答案   理解 Context 管理策略      构建 RAG 检索增强系统
                          理解 Agent 运行时机制      部署生产级 Agent 应用
                          理解 Loop 推理循环         设计多 Agent 协作编排
                          
认知层级: Prompt           认知层级: Prompt→Context    认知层级: 五层全覆盖
```

### 3.3 五层体系的来源：为什么是这五层？

这个五层体系并非凭空设计，而是总结了 2024-2026 年 AI 工程领域的多个独立趋势后归纳而成的认知框架：

| 趋势来源 | 对应的层 | 触发事件 |
|----------|---------|----------|
| Prompt Engineering 最佳实践文档化 | Layer 1 | Anthropic/OpenAI Prompt Engineering Guide (2024) |
| RAG 系统的广泛部署和"效果不好"的反思 | Layer 2 | 企业 RAG 部署潮 + Context Engineering 概念提出 (2024-2025) |
| AI Harness Engineering 论文发表 | Layer 3 | arXiv:2605.13357 "AI Harness Engineering" 定义性论文 (2025.05) |
| Claude Code / LangGraph Agent Loop 实践 | Layer 5 | Claude Code 发布 + LangGraph 成熟 (2025) |
| 企业级 Agent 编排需求爆发 | Layer 6 | LangGraph Checkpoint/HITL 机制成熟 (2025-2026) |

### 3.4 每一层的"升维"：从上一层到下一层解决了什么问题

```
Prompt (L1) ──→ Context (L2)
  解决了："AI 不知道背景信息"
  升维方式：从"写指令"升级为"设计信息环境"

Context (L2) ──→ Harness (L3)
  解决了："AI 只能生成文本，不能执行操作"
  升维方式：从"信息管理"升级为"运行时基础设施"

Harness (L3) ──→ Loop (L4)
  解决了："AI 只能被一问一答驱动，不能自主规划"
  升维方式：从"被动响应"升级为"自主推理循环"

Loop (L4) ──→ Graph (L5)
  解决了："AI 的决策过程是一个黑箱，无法审计和恢复"
  升维方式：从"线性循环"升级为"可编排的状态图"
```

### 3.5 五层体系的实践意义

| 角色 | 需要重点关注的层 | 为什么 |
|------|-----------------|--------|
| **普通用户** | Prompt Engineering | 日常使用 AI 只需要写好 Prompt |
| **高级用户/超级个体** | Prompt + Context | 管理复杂的多轮对话和长文档任务 |
| **AI 应用开发者** | Prompt + Context + Harness | 构建可部署的 AI 应用 |
| **Agent 系统架构师** | 全部五层 | 设计完整的自主智能系统 |
| **企业技术决策者** | 五层全景 + Harness/Graph | 评估技术成熟度和采购决策 |

---

## 四、五层速览表

| 层级 | 核心问题 | 技术本质 | 代表工具/系统 | 企业成熟度 |
|------|----------|----------|-------------|-----------|
| **Prompt Engineering** (提示词工程) | 怎么和 AI 说话？ | 设计精准的自然语言指令，对 Token 预测方向施加约束 | ChatGPT、Claude、DeepSeek、Gemini | ★★★★★ 高度成熟 |
| **Context Engineering** (上下文工程) | 给 AI 看什么信息？看多少？怎么看？ | 管理模型在推理时可用的完整信息环境，在有限上下文窗口内最大化信息密度 | Claude Code、mem0、RAG 系统 | ★★★★☆ 快速成熟中 |
| **Harness Engineering** (根基工程) | Agent 的"身体"长什么样？ | 构建 Agent 运行时基础设施：工具注册、权限控制、会话管理、追踪日志 | Claude Code、Codex(OpenAI)、DeerFlow(字节) | ★★★☆☆ 2025年成为独立学科 |
| **Loop Engineering** (循环工程) | Agent 如何思考和做决策？ | 设计 Agent 核心推理循环：Observe→Think→Decide→Act→Feedback | LangGraph、Claude Code | ★★★★☆ 范式已成熟 |
| **Graph Engineering** (图工程) | 如何编排复杂的 Agent 工作流？ | 用状态图建模 Agent 工作流：节点+边+条件分支+Checkpoint | LangGraph、n8n+AI、Claude Code Subagents | ★★★★☆ 快速成熟中 |

### 企业成熟度评级标准

| 星级 | 含义 |
|------|------|
| ★★★★★ | 有成熟的工具、最佳实践和行业标准，企业可直接采用 |
| ★★★★☆ | 工具和范式已成熟，但最佳实践仍在演化 |
| ★★★☆☆ | 学科定义刚确立（2025年），工具仍在快速迭代 |
| ★★☆☆☆ | 早期探索阶段，开源项目为主，商业产品很少 |

---

## 五、Claude Code 在五层中的定位详解

Claude Code 是 Anthropic 官方推出的命令行 AI 编码 Agent。它不是"一个模型"或"一个框架"，而是五层体系的一个完整实例。理解 Claude Code 覆盖了哪些层、没覆盖哪些层，是理解五层体系最好的方式。

### 5.1 逐层分析

```
Claude Code 在五层体系中的定位：

  Prompt Engineering     ✅ 用户通过 System Prompt / CLAUDE.md / Hooks 定义 Agent 行为
                             支持自定义指令注入，所有对话都在 Prompt 约束下进行

  Context Engineering    ✅ 自动 Tool Output 压缩 —— 工具返回的大量内容自动摘要
                             对话历史管理 —— 超出窗口时自动压缩早期对话
                             结构化上下文 —— 系统指令/工具定义/对话历史分层组织
                             关键创新：对用户透明——你感受不到压缩在发生

  Harness Engineering    ✅ Tool Registry (MCP协议) —— 工具通过标准接口动态发现
                             Permission Gate (四级权限) —— Allow/Ask/Deny/AskOnce
                             Hook System —— PreToolUse/PostToolUse/Notification/Stop
                             Session 持久化 —— 会话状态可恢复
                             Subagents —— 子代理分发，独立上下文执行
                             结构化日志 —— 每步可追踪审计

  Loop Engineering       ✅ 高性能 Agent Loop —— 条件性工具激活，非全部列出
                             上下文感知停止 —— 检测任务完成自动终止
                             Subagent 分发 —— 复杂任务并行执行
                             渐进式权限 —— 先只读确认理解，再开放写入

  Graph Engineering      ✅ (部分) Subagents + Hooks 构成隐式工作流图
                             Pipeline 模式 —— 多个 Subagent 链式协作
                             Hook 拦截实现条件分支 —— 类似 Conditional Edge
                             但不具备完整的 State Graph 显式编排能力

  核心定位：Claude Code 主要覆盖 Context / Harness / Loop 三层。
  它是目前最完整、最易获取的 Agent Harness 学习样本。
```

### 5.2 Claude Code 的核心技术贡献

| 特性 | 技术原理 | 对应的工程层 | 为什么重要 |
|------|----------|-------------|-----------|
| **自动 Context Compaction** | 工具输出 → 摘要 → 注入上下文；对用户完全透明 | Context Engineering | 解决了 Agent 长任务中"对话越来越长、成本越来越高"的核心问题 |
| **四级权限模型** | Allow(始终允许) / Ask(每次询问) / Deny(始终拒绝) / AskOnce(本次允许) | Harness Engineering | 在安全性和便利性之间提供可调节的平衡 |
| **MCP 协议集成** | 工具通过标准化接口动态发现和调用，而非硬编码 | Harness Engineering | 定义了 AI 工具连接的事实标准，正在成为行业协议 |
| **Subagent 分发** | 复杂任务拆分为子任务，分发到独立子代理并行执行 | Loop/Graph Engineering | 实现了多 Agent 协作的实用模式 |
| **Hooks 系统** | 在关键节点（工具调用前后/错误/停止）插入自定义逻辑 | Harness Engineering | 企业级合规检查、日志审计、自定义安全策略的入口 |

### 5.3 Claude Code 未覆盖的层及替代

| 缺失层 | Claude Code 的局限 | 补全方案 |
|--------|-------------------|----------|
| Graph Engineering（完整） | 无显式 State Graph 编排、无 Checkpoint | LangGraph（补充完整图编排能力） |

---

## 六、"Agent 到底是什么？"—— 结合五层体系的完整回答

### 6.1 一句话定义

> **Agent（智能体）不是一个技术、不是一种模型、不是一个框架。Agent 是一个系统——它整合了 Prompt Engineering（理解任务）、Context Engineering（信息环境）、Harness Engineering（运行时能力）、Loop Engineering（自主推理循环）、Graph Engineering（可编排工作流）的完整系统。**

### 6.2 逐层拆解：Agent 的五层构成

```
"Agent" 这个概念的五层拆解：

一层一层问自己——如果缺少这一层，它还是 Agent 吗？

Layer 1 — Prompt Engineering:
  Q: 没有 Prompt，Agent 怎么知道要做什么？
  A: 不知道。Prompt 是 Agent 的任务输入层。没有任务输入 → 不是 Agent，只是程序。

Layer 2 — Context Engineering:
  Q: 没有 Context 管理，Agent 怎么在长对话中不"失忆"？
  A: 会失忆。超过上下文窗口后，最前面的对话被截断。Context 是 Agent 的记忆边界管理。

Layer 3 — Harness Engineering:
  Q: 没有 Harness，Agent 怎么调用工具？怎么控制权限？怎么追踪行为？
  A: 不能。裸 LLM 只能生成文本。Harness 给了 Agent "手脚"（工具调用能力）。

Layer 4 — Loop Engineering:
  Q: 没有 Loop，Agent 怎么自主完成多步任务？
  A: 只能一问一答。Loop 给了 Agent 自主推理和迭代的能力——"大脑"。

Layer 5 — Graph Engineering:
  Q: 没有 Graph，Agent 怎么被编排到企业工作流中？
  A: 只能独立运行。Graph 让 Agent 可以被编排、被审计、被恢复——"企业级"。

结论：只有五层齐全，才是一个"完全体的 Agent"。
     但实际应用中，大多数"Agent"只具备其中 3-4 层。
```

### 6.3 Agent 分级：从 L1 到 L5

| 级别 | 具备的层 | 典型表现 | 实例 |
|------|---------|----------|------|
| **L1 Chatbot** | Prompt only | 一问一答，无工具调用，无记忆 | ChatGPT 基础对话 |
| **L2 RAG Bot** | Prompt + Context | 能检索知识库回答，但无自主行动 | 企业客服机器人 |
| **L3 Tool Agent** | Prompt + Context + Harness | 能调用工具，有权限控制 | Cline + 简单配置 |
| **L4 Autonomous Agent** | + Loop | 能自主规划多步任务，自我纠错 | Claude Code、Devin |
| **L5 Orchestrated Agent** | + Graph | 可编排到企业工作流，可审计可恢复 | LangGraph 企业部署 |

**注**：跨会话长期记忆属于 Context Engineering 的延伸能力（记忆检索注入上下文窗口），不属于独立工程层——任何级别的 Agent 都可以通过 mem0/Letta 等记忆层工具获得跨会话记忆。这里的级别划分主要依据"自主性与编排能力"。

### 6.4 关键澄清

| 常见说法 | 准确理解 |
|----------|----------|
| "这是一个 AI Agent" | 不精确。应该说"这是一个具备 L3 能力的 Agent"——明确了具备哪些层 |
| "Agent = LLM + Tools" | 不完整。这只是 L3。缺少 Context/Loop/Graph |
| "用 LangChain 就能做 Agent" | LangChain 提供了 Harness 的一部分（工具注册），但不是完整 Harness |
| "Claude Code 是一个 Agent" | Claude Code 是一个 L4 Agent（具备 Context+Harness+Loop，并在 Graph 层有部分能力） |

---

## 七、关键结论

### 7.1 本知识块的 5 个核心记忆点

1. **五层金字塔结构**：Prompt → Context → Harness → Loop → Graph，底层是基础，顶层是编排
2. **不能跳跃**：每一层建立在下层之上，跳过 Context 做 Loop 必然导致 Agent "失忆"
3. **Agent 是系统，不是技术**：Agent = 五层能力的整合，不是单一模型或框架
4. **Claude Code 覆盖 Context/Harness/Loop 三层，并在 Graph 层提供部分能力**，是目前最好的 Agent 学习样本
5. **入门从 Prompt 开始**：Prompt Engineering 是所有上层能力的入口和基础

### 7.2 不同角色的行动建议

| 角色 | 本课后续应重点关注 | 课后行动 |
|------|------------------|----------|
| 🎓 零基础学习者 | KB2（Prompt+Context）+ KB5（Prompt实战） | 动手写 20 个不同场景的 Prompt |
| 💼 企业管理者 | 五层速览表 + Claude Code 定位 + Agent 分级 | 评估企业当前处于哪一层，差距在哪 |
| 🔧 开发者 | 全部五层详解（KB2-KB4） | 搭建 Claude Code/Codex 环境深入体验 Harness 层 |

### 7.3 过渡到下一知识块

五层金字塔的最底层——Prompt Engineering 和 Context Engineering——是 ROI 最高、学习门槛最低的入口。下一知识块将深入这两层：Token 预测的数学原理、Prompt 的六组件构成、Context 的三大管理策略。

---

> **本知识块核心记忆点**：五层金字塔（Prompt→Context→Harness→Loop→Graph）；Agent 是五层整合系统；Claude Code 覆盖三层并在 Graph 层提供部分能力。

---

# 第二部分：Prompt Engineering 与 Context Engineering 深入

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB2 / 本课共8个KB |
| **知识块标题** | Prompt Engineering 与 Context Engineering 深入 |
| **预计时长** | 25分钟 |
| **教学形式** | 深度讲解 |
| **适合人群** | 💼 企业管理者/投资人 + 🎓 零基础学习者 |
| **前置知识** | KB1：五层AI工程体系概览 |
| **核心目标** | 深入理解 Prompt Engineering 的技术原理与六组件体系；掌握 Context Engineering 的三大核心策略（压缩/选择/结构化）；建立"Prompt 解决怎么说，Context 解决看什么"的清晰认知 |

---

## 二、Prompt Engineering 深度解析

### 2.1 技术原理：Token 预测模型与 Prompt 约束机制

#### 2.1.1 大语言模型的本质

大语言模型本质上是**"下一个 Token 预测器"**。当你输入一段文本，模型并非"理解"你的意图，而是在其训练数据的统计规律中，计算最可能的下一个 Token（词元），然后逐 Token 生成。

```
模型推理过程（简化）：

输入 Prompt: "人工智能的未来"
    ↓
Token 化: [人工, 智能, 的, 未来]
    ↓
模型计算: P(下一个Token | [人工, 智能, 的, 未来])
         = 基于海量训练数据的条件概率分布
    ↓
采样输出: "将会" (概率最高) / "充满" (次高) / ...
    ↓
继续: P(下一个Token | [人工, 智能, 的, 未来, 将会])
    ↓
... 逐 Token 生成，直到遇到终止符
```

#### 2.1.2 Prompt 如何改变输出

Prompt 的作用，就是对"下一个 Token 预测"的方向施加**精确的约束和引导**。

```
┌─────────────────────────────────────────────────────────────────┐
│              Prompt 约束机制 —— 对比实验                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  无 Prompt（纯续写模式）：                                        │
│    输入："人工智能的未来"                                          │
│    模型行为：从训练数据中找到"人工智能的未来"后最常见的续写           │
│    输出："将会非常美好，人类将与机器和谐共处..."                     │
│    ↑ 不可控 —— 模型在"自由续写"，方向完全由训练数据决定              │
│                                                                 │
│  有 Prompt（精准引导模式）：                                       │
│    输入："请用200字，从三个维度（技术/商业/社会）分析                │
│           人工智能的未来。格式：每段用标题开头。"                     │
│    模型行为：受到"200字"+"三个维度"+"标题格式"三重约束              │
│    输出：                                                       │
│    技术维度：大模型参数规模持续增长...                              │
│    商业维度：AI原生应用重塑企业运营...                              │
│    社会维度：人机协作成为新常态...                                  │
│    ↑ 可控 —— 格式、内容、长度都在 Prompt 约束范围内                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.1.3 Prompt 约束的数学直觉

```
P(输出 | Prompt) = P(Token_1 | Prompt)
                 × P(Token_2 | Prompt, Token_1)
                 × P(Token_3 | Prompt, Token_1, Token_2)
                 × ...
                 × P(Token_n | Prompt, Token_1, ..., Token_{n-1})

Prompt 的作用是：
  1. 缩小采样空间 —— 把"所有可能的续写"限制到"符合指令的续写"
  2. 条件化输出分布 —— 让符合要求的 Token 序列概率大幅提高
  3. 提供格式锚点 —— 通过Few-shot示例锚定输出格式
```

---

### 2.2 核心组件体系

一个完整的、高质量的 Prompt 由六个组件构成。这六个组件层层递进，覆盖了从"AI 是谁"到"AI 输出什么"的全部控制维度。

```
┌─────────────────────────────────────────────────────────────┐
│                  Prompt 六组件模型                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Role       →  AI 的身份定位                            │  │
│  │  "你是谁"      设定专业领域、语气风格、认知水平             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Context    →  背景信息环境                              │  │
│  │  "在什么情境下" 项目信息、目标受众、限制条件、已有尝试       │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Task       →  具体任务描述                              │  │
│  │  "做什么"      要输出的内容、精确度决定输出质量             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Format     →  输出结构要求                              │  │
│  │  "怎么呈现"    JSON/Markdown/表格/特定模板                │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Constraints→  边界条件                                  │  │
│  │  "什么不能做"   字数限制/禁用技术/合规要求/安全红线         │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Examples   →  参考范例                                  │  │
│  │  "像这样"      Few-shot示例，锚定输出格式和风格             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 各组件详解

| 组件 | 英文 | 技术作用 | 缺失后果 | 优化优先级 |
|------|------|----------|----------|-----------|
| **Role** | 角色 | 激活模型在特定领域的训练数据分布，提升专业术语准确率 | AI 用最通用的方式回答，缺乏专业深度 | ★★★★ |
| **Context** | 上下文 | 提供约束条件，缩小模型的"自由发挥"空间 | AI 给出看似合理但不适用的答案 | ★★★★★ |
| **Task** | 任务 | 定义输出目标，是模型生成的核心方向锚点 | 输出偏离意图，"答非所问" | ★★★★★ |
| **Format** | 格式 | 指定输出的语法结构，确保下游系统可解析 | 输出自由文本，无法被程序处理 | ★★★★ |
| **Constraints** | 约束 | 显式排除不希望出现的输出模式 | 生成不安全/不合规内容 | ★★★★★ |
| **Examples** | 示例 | 通过 Few-shot 学习锚定输出分布，比文字描述更精确 | 格式和风格偏差，需要多轮纠正 | ★★★ |

#### 组件对比：好 Prompt vs 差 Prompt

```
┌─────────────────────────────────────────────────────────────────┐
│ 差 Prompt（缺少大部分组件）：                                      │
│                                                                 │
│   "帮我写个方案"                                                  │
│                                                                 │
│   缺失: Role ❌ | Context ❌ | Task (模糊) ⚠️ |                    │
│         Format ❌ | Constraints ❌ | Examples ❌                   │
│                                                                 │
│   模型行为: 完全不确定你想要什么 → 随机输出                         │
├─────────────────────────────────────────────────────────────────┤
│ 好 Prompt（六组件齐全）：                                          │
│                                                                 │
│   Role:        你是一位资深建筑设计师                              │
│   Context:     我要在大学城旁开一个面向学生的现代风格咖啡馆           │
│                面积200平米，预算50万                               │
│   Task:        请为我设计一份完整的咖啡馆方案                        │
│   Format:      包括：1.空间布局 2.设计风格 3.材料选择 4.灯光设计      │
│   Constraints: 控制在2000字以内，使用中文专业术语                    │
│   Examples:    参考Manner Coffee的简约工业风                       │
│                                                                 │
│   模型行为: 六组件精确约束 → 高质量、可预期的输出                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.3 代表工具

| 工具 | 定位 | Prompt Engineering 特色能力 |
|------|------|--------------------------|
| **ChatGPT** | 通用对话 AI | System Prompt 自定义、GPTs（预设 Prompt + 工具）、Prompt 模板市场 |
| **Claude** | 长文本推理 AI | CLAUDE.md 文件级 System Prompt、Projects 知识库 + 自定义指令 |
| **DeepSeek** | 高性价比推理 AI | 中文 Prompt 理解能力最强、API 价格极低（约 Claude 的 1/50） |
| **Gemini** | Google 多模态 AI | System Instruction 自定义、Google Search Grounding |
| **Cline (VSCode)** | 编程 Agent | Custom Instructions 自定义 System Prompt、.clinerules 项目级规则 |

---

### 2.4 企业视角

> 📊 **企业视角：Prompt Engineering 的战略价值**
>
> Prompt Engineering 是企业 AI 投入中 ROI 最快见效的环节。原因：
>
> | 维度 | 数据 |
> |------|------|
> | **见效速度** | 优化一个 Prompt 需要 30 分钟到 2 小时，无需任何技术开发 |
> | **准确率提升** | 优化后的客服 Prompt 可将自动回复准确率从 60% 提升到 90%+ |
> | **一致性保障** | 标准化 Prompt 模板确保全国各地分公司输出的客户邮件风格统一 |
> | **知识沉淀** | 优质 Prompt 模板成为企业可复用的数字资产，而非依赖个人经验 |
> | **边际成本** | 接近于零——不需要训练新模型，不需要接入新工具，只需要更好的 Prompt |
>
> **企业行动建议**：
> 1. 建立高频场景的 Prompt 模板库（客服回复、周报、竞品分析、内部通知）
> 2. 设立 Prompt 审查机制——所有对外 AI 产出的 Prompt 模板需经过审核
> 3. 将 Prompt Engineering 纳入新员工 AI 素养培训的必修内容

---

## 三、Context Engineering 深度解析

### 3.1 技术原理：上下文窗口管理

#### 3.1.1 从 Prompt 到 Context —— 视角升级

```
Prompt Engineering vs Context Engineering：

Prompt Engineering 关心的:
  "System Prompt 写什么？"
  → 一个方块的优化

Context Engineering 关心的:
  "模型在每一步推理时能'看到'的全部信息是什么？"
  → 整个信息环境的设计

升级的本质：
  Prompt  →  指令怎么写
  Context →  信息怎么组织、怎么管理、怎么在有限窗口内最大化价值
```

#### 3.1.2 上下文窗口的本质约束

模型的上下文窗口（Context Window）是有限的——通常 200K Token（约 15 万汉字）。Agent 运行过程中会产生大量信息，包括：

- 系统指令
- 多轮对话历史
- 工具定义
- 工具调用结果（可能很冗长——一次数据库查询可能返回数百行）
- 检索增强结果（RAG）
- 记忆提取
- 用户偏好

**核心挑战**：如何在这 200K Token 的限制内，让模型每一步都拥有做出正确判断所需的全部信息？

---

### 3.2 完整信息环境架构

```
┌──────────────────────────────────────────────────────────────┐
│              Context Window (200K Token)                      │
│              模型每一步推理时能"看到"的全部信息                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ System Prompt      │  │ Conversation       │              │
│  │ 系统指令层           │  │ History            │              │
│  │                    │  │ 对话历史层           │              │
│  │ · 角色定义          │  │                    │              │
│  │ · 安全规则          │  │ · 用户消息序列       │              │
│  │ · 输出格式约束      │  │ · AI 回复序列        │              │
│  │ · 禁止行为清单      │  │ · 工具调用记录       │              │
│  │                    │  │ · 工具输出记录       │              │
│  │ ~2K Token          │  │ ~5-50K Token        │              │
│  └────────────────────┘  └────────────────────┘              │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ Tool Definitions   │  │ Retrieved Context  │              │
│  │ 工具定义层           │  │ 检索增强层           │              │
│  │                    │  │                    │              │
│  │ · 工具名称          │  │ · RAG 检索结果      │              │
│  │ · 功能描述          │  │ · 知识库片段        │              │
│  │ · 参数 Schema      │  │ · 相关文档          │              │
│  │ · 返回格式          │  │ · 数据摘要          │              │
│  │                    │  │                    │              │
│  │ ~2-10K Token       │  │ ~3-10K Token        │              │
│  └────────────────────┘  └────────────────────┘              │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ Memory Retrieval   │  │ Structured         │              │
│  │ 记忆提取层           │  │ Instructions       │              │
│  │                    │  │ 结构化指令层         │              │
│  │ · 用户偏好记忆      │  │                    │              │
│  │ · 历史决策记录      │  │ · XML/MD 分层标签   │              │
│  │ · 任务上下文        │  │ · 优先级标记        │              │
│  │                    │  │ · 输出 Schema       │              │
│  │ ~1-5K Token        │  │ ~1K Token           │              │
│  └────────────────────┘  └────────────────────┘              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  问题：当 Agent 运行 50 轮对话 + 100 次工具调用后，              │
│        对话历史可能占用 150K+ Token，还剩下多少空间给新信息？       │
│                                                              │
│  解决：Context Engineering 的三大核心策略                        │
└──────────────────────────────────────────────────────────────┘
```

---

### 3.3 三大核心策略详解

```
┌─────────────────────────────────────────────────────────────────┐
│            Context Engineering 三大核心策略                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  策略1: 压缩 (Compaction)                                        │
│  ─────────────────────                                          │
│  核心思想：把冗长内容"压缩"为精炼摘要，保留关键信息                    │
│  解决的问题：对话过长超出窗口 → Agent "失忆"                       │
│                                                                 │
│  策略2: 选择 (Selection)                                         │
│  ─────────────────────                                          │
│  核心思想：根据当前任务，只选择最相关的上下文片段注入模型               │
│  解决的问题：不是所有信息都值得占 Token（成本+注意力分散）             │
│                                                                 │
│  策略3: 结构化 (Structuring)                                      │
│  ─────────────────────                                          │
│  核心思想：用 XML 标签、Markdown 层级、优先级标记组织上下文            │
│  解决的问题：模型在海量文本中迷失，无法快速定位关键信息                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 策略1：上下文压缩 (Compaction)

| 维度 | 说明 |
|------|------|
| **技术原理** | 当对话历史超出预设阈值时，自动将早期对话/工具输出"压缩"为摘要，释放 Token 空间 |
| **压缩粒度** | 分层压缩策略——先压缩工具输出（最冗长），再压缩早期对话，最后才压缩当前任务上下文 |
| **压缩方法** | ① LLM 自动摘要：用一次额外的 LLM 调用总结历史；② 滑动窗口截断：只保留最近 N 轮；③ 关键信息提取：只保留决策点、错误信息、重要数据 |
| **Claude Code 实现** | 内置 Context Compaction，自动将冗长的工具输出（如 `cat` 一个 500 行文件）压缩为摘要再送入模型 |
| **权衡** | 压缩 = 信息损失 vs Token 空间的权衡。过度压缩会丢失细节，不压缩则成本失控 |

```
压缩过程的示意：

压缩前（工具输出，~5000 Token）：
  "文件内容：
  line 1: import os
  line 2: import sys
  line 3: ...
  line 500: return result"

压缩后（摘要，~200 Token）：
  "[File Summary: main.py, 500 lines, Python.
    Imports: os, sys, json, requests.
    Key functions: process_data(), validate_input(), export_results().
    Error handling: try/except on lines 120-145.]"
```

#### 策略2：上下文选择 (Selection)

| 维度 | 说明 |
|------|------|
| **技术原理** | 从所有可用上下文中，根据当前任务的语义相关性，只选择最相关的片段注入模型上下文窗口 |
| **核心手段** | ① 语义相似度匹配（Embedding → 向量检索）；② 优先级排序（System Prompt > 当前任务 > 相关历史 > 无关历史）；③ RAG 检索（从外部知识库检索相关文档） |
| **关键挑战** | 选择过度 → 丢失关键上下文；选择不足 → 浪费 Token 在无关信息上 |
| **Token 经济** | 每个 Token 都有成本（API 费用 + 模型注意力分散）。好的 Selection 策略 = 用最少的 Token 传递最大的信息量 |

```
Selection 的决策逻辑：

当前任务："查询张三的薪资"
    ↓
可用上下文评估：
  ✅ 注入：employees 表结构定义         — 高度相关
  ✅ 注入：最近的数据库查询结果          — 高度相关
  ✅ 注入：安全规则（禁止泄露薪资）       — 高度相关
  ❌ 排除：3轮前的市场分析对话            — 无关
  ❌ 排除：10分钟前的 Python 代码讨论     — 无关
  ❌ 排除：上周的会议纪要                 — 无关
    ↓
精选上下文 → 5K Token（而非全部 50K Token）→ 模型注意力集中在关键信息上
```

#### 策略3：上下文结构化 (Structuring)

| 维度 | 说明 |
|------|------|
| **技术原理** | 用明确的、可解析的结构标记（XML/Markdown/JSON schema）组织上下文，使模型能快速定位和区分不同类别的信息 |
| **核心手段** | ① XML 标签分层（`<system>...</system>`、`<task>...</task>`）；② Markdown 层级（标题→子标题→内容）；③ 优先级元数据（`priority="high"`）；④ 信息类型标记（`<tool_result>` vs `<conversation>`） |
| **为什么有效** | LLM 在训练时看过大量结构化文档（HTML/XML/JSON），"理解"标签的含义——它能区分 `<system>` 里的规则和 `<user_input>` 里的请求 |
| **行业标准** | Anthropic 官方推荐 XML 结构化 Prompt；OpenAI 推荐 Markdown 结构；两者均可，关键是"一致使用" |

---

### 3.4 上下文结构化 XML 标准示例

```xml
<!-- 完整的上下文结构化示例 —— 可直接用于生产级 Agent -->
<agent_context>

  <system_instructions priority="highest">
    你是一个数据分析助手。遵循以下原则：
    1. 始终先理解数据结构和含义，再给出分析建议
    2. 安全规则（硬约束，不可违反）：
       - 不执行 DROP / TRUNCATE / ALTER 操作
       - 不暴露数据库连接字符串、密码、API Key
       - 涉及删除/修改操作时需要用户显式确认
    3. 输出原则：先给出结论，再展开分析过程——方便 CEO 快速阅读
  </system_instructions>

  <tool_definitions priority="high">
    <tool name="query_database">
      <description>执行只读 SELECT 查询，返回结果集</description>
      <parameters>
        <param name="sql" type="string" required="true">
          合法的 SELECT 语句。禁止包含 INSERT/UPDATE/DELETE/DROP
        </param>
      </parameters>
      <returns>JSON 数组，每行一个对象</returns>
    </tool>
    <tool name="generate_chart">
      <description>根据数据生成可视化图表</description>
      <parameters>
        <param name="data" type="array">图表数据</param>
        <param name="chart_type" type="string">line | bar | pie | scatter</param>
        <param name="title" type="string">图表标题</param>
      </parameters>
    </tool>
  </tool_definitions>

  <conversation_history>
    <turn id="1">
      <user>帮我分析上个月的销售趋势</user>
      <assistant>好的，我先查询数据库获取上个月的销售数据...</assistant>
      <tool_call name="query_database">
        SELECT date, product, amount FROM sales
        WHERE date BETWEEN '2026-07-01' AND '2026-07-31'
      </tool_call>
      <tool_result>
        <summary>返回 350 行记录，日期范围 07-01 至 07-31</summary>
        <stats>
          总销售额: ¥437,500 | 日均: ¥14,112
          最高单日: 07-15 (¥32,800) | 最低单日: 07-02 (¥3,200)
        </stats>
      </tool_result>
    </turn>
    <turn id="2">
      <user>7月15号为什么销售特别高？</user>
      <assistant>让我查看7月15日的销售明细...</assistant>
      <tool_call name="query_database">
        SELECT product, SUM(amount) as total
        FROM sales WHERE date = '2026-07-15'
        GROUP BY product ORDER BY total DESC LIMIT 5
      </tool_call>
      <tool_result>
        <summary>7月15日销售额分布：新品上线贡献 ¥18,500，占总销售额 56.4%</summary>
      </tool_result>
      <assistant>7月15日销售高峰的主要驱动力是新产品的上线发布...
      以下是对此次活动的详细分析...</assistant>
    </turn>
  </conversation_history>

  <retrieved_context priority="high" source="rag_pipeline">
    <document id="doc_1" relevance_score="0.94">
      <title>2026年7月市场分析报告</title>
      <summary>上个月整体市场环比增长 12.3%，主要受暑期消费季驱动</summary>
    </document>
    <document id="doc_2" relevance_score="0.87">
      <title>竞品分析：同类产品 Q2 表现</title>
      <summary>竞品 A 增长了 8%，竞品 B 下降了 3%</summary>
    </document>
  </retrieved_context>

  <user_preferences>
    <pref key="language">中文输出，专业术语保留英文原名</pref>
    <pref key="detail_level">先给结论（适合 CEO 阅读），再附分析过程</pref>
    <pref key="data_privacy">薪资数据只显示范围，不显示个人精确值</pref>
  </user_preferences>

  <current_task priority="highest">
    基于上述分析结果，生成一份 CEO 级别的销售趋势报告。
    包含：核心发现（3条）、趋势判断、风险预警、下周行动建议。
  </current_task>

</agent_context>
```

---

### 3.5 代表工具/系统

| 工具/系统 | 定位 | 核心 Context Engineering 能力 | 成熟度 |
|-----------|------|------------------------------|--------|
| **Claude Code** | Anthropic 官方 Coding Agent CLI | 内置 Context Compaction（自动压缩工具输出）；结构化上下文组织；对话历史管理 | ★★★★☆ |
| **mem0** | 开源记忆层 | 自动提取对话中的关键信息为结构化记忆；跨会话记忆检索和注入 | ★★★☆☆ |
| **Letta** | 开源 Agent 记忆框架 | 三层记忆模型（短期/工作/长期）；记忆的自动更新和蒸馏 | ★★★☆☆ |
| **LangChain Hub** | Prompt 模板管理平台 | Prompt + Context 的模板版本控制；团队协作和共享 | ★★★★☆ |
| **RAG 系统 (RAGFlow/Weaviate)** | 检索增强生成 | Chunking 策略、向量检索、Re-ranking、上下文拼接 | ★★★☆☆ |

---

### 3.6 企业视角

> 📊 **企业视角：Context Engineering 决定 RAG 系统的质量天花板**
>
> 大量企业买了 RAG 工具但效果不好的根本原因：
>
> ```
>   问题表象                         真正原因
> ────────────                    ────────────
> "RAG 检索不准确"        →       Chunking 策略不合理（Context Structuring 问题）
> "模型回答不相关"        →       检索到的上下文质量差（Context Selection 问题）
> "长文档处理很差"        →       上下文超出窗口被截断（Context Compaction 问题）
> "回答质量不稳定"        →       上下文组织方式不一致（Context Structuring 问题）
> ```
>
> | 维度 | 数据 |
> |------|------|
> | **准确率影响** | 好的 Chunking 策略 + 上下文结构化可将检索准确率从 60% 提升到 95% |
> | **成本影响** | 合理的上下文选择策略可减少 40-60% 的 Token 消耗（=API 费用） |
> | **瓶颈定位** | 90% 的 RAG 效果问题不在模型、不在向量库，而在上下文设计 |
>
> **企业行动建议**：
> 1. 优先投资上下文结构化——标准化的 XML/Markdown 标签体系
> 2. Chunking 策略不要用默认值——根据文档类型（技术文档/法律合同/客服对话）定制
> 3. 上下文压缩策略是控制 API 成本的关键杠杆

---

## 四、Prompt vs Context 的关系对比

| 对比维度 | Prompt Engineering | Context Engineering |
|----------|-------------------|---------------------|
| **核心问题** | 怎么和 AI 说话？ | 给 AI 看什么信息？ |
| **管理对象** | System Prompt 指令文本 | 整个上下文窗口内的全部信息 |
| **技术难度** | 低（纯文本设计） | 中高（涉及信息检索、压缩算法、结构化设计） |
| **ROI 速度** | 极快（30分钟见效） | 较快（需要系统化设计） |
| **工具依赖** | 无（任何对话式 AI 都支持） | 有（需要 RAG/Compaction/Memory 等系统支持） |
| **优化重点** | 指令的精确性、完整性 | 信息的相关性、密度、结构 |
| **技能类型** | 语言表达 + 逻辑设计 | 信息架构 + 系统工程 |
| **典型产出** | Prompt 模板、RCTE 结构化指令 | Chunking 策略、XML 标签体系、Memory Schema |
| **适用场景** | 所有 AI 交互 | Agent 系统、RAG 应用、长文档处理 |
| **失败表现** | "答非所问" | Agent "失忆"、成本失控、回答不一致 |

### 4.1 两者协同关系

```
┌─────────────────────────────────────────────────────────────────┐
│               Prompt + Context 协同模型                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   用户任务                                                       │
│      │                                                          │
│      ├──→ Prompt Engineering 设计层:                              │
│      │      "这个任务需要 AI 以什么角色、什么格式、什么约束来回答？" │
│      │      产出: System Prompt + Task Description               │
│      │                                                          │
│      └──→ Context Engineering 设计层:                             │
│             "这个任务需要 AI 看到哪些信息才能做出正确判断？"         │
│             产出: 结构化上下文（检索结果+记忆+历史+工具定义）         │
│                                                                 │
│   两者合并 → 组装为完整的 Context Window → 送入 LLM → 得到输出     │
│                                                                 │
│   ┌──────────────────────────────────────┐                      │
│   │  Prompt (指令) + Context (信息)       │                      │
│   │  = 模型知道的 + 模型看到的             │                      │
│   │  = 高质量输出的充分条件                │                      │
│   └──────────────────────────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、关键结论

### 5.1 本知识块的 5 个核心记忆点

1. **LLM 本质**：下一个 Token 预测器。Prompt 的作用是对预测方向施加约束
2. **六组件模型**：Role + Context + Task + Format + Constraints + Examples —— 每个组件解决一类输出质量问题
3. **Context vs Prompt**：Prompt 决定"指令怎么写"，Context 决定"信息怎么管"
4. **三大核心策略**：Compaction（压缩节省空间）、Selection（选择提升相关性）、Structuring（结构化提升可定位性）
5. **Context 是瓶颈**：企业 RAG 效果不好的原因 90% 在上下文设计，不在模型

### 5.2 不同角色的行动建议

| 角色 | 关注重点 | 下一步行动 |
|------|----------|-----------|
| 🎓 零基础学习者 | Prompt 六组件模型 | 用 RCTE 框架重写日常使用的 Prompt |
| 💼 企业管理者 | 上下文结构化对企业 RAG 系统的价值 | 审计企业现有 RAG 的 Chunking 策略和上下文设计 |
| 🔧 开发者 | 三大核心策略的实现细节 | 研究 Claude Code 的 Compaction 机制；尝试 mem0/Letta |

### 5.3 过渡到下一知识块

Prompt 解决了"AI 理解任务"，Context 解决了"AI 获取信息"。但理解和获取信息后，AI 要真正"做事情"，还需要一套完整的运行时基础设施——工具怎么注册？权限怎么控制？会话怎么管理？这就是第三层：Harness Engineering。

---

> **本知识块核心记忆点**：LLM = Token 预测器；Prompt 六组件（R+C+T+F+C+E）；Context 三策略（Compaction / Selection / Structuring）；Prompt 管指令，Context 管信息。

---

# 第三部分：Harness Engineering 深度解析

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI 时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB3 / 本课共8个KB |
| **知识块标题** | Harness Engineering 深度解析 |
| **前置知识块** | KB1（五层AI工程体系概览）、KB2（Prompt 与 Context 工程深入） |
| **预计时长** | 25分钟 |
| **知识块类型** | 技术讲授 |
| **适用对象** | 💼 企业管理者/投资人 + 🎓 零基础学习者（技术深度分级标注） |
| **核心议题** | 1. Agent 运行时基础设施（Harness）的六大组件<br>2. 裸 Agent Loop 与生产级 Harness 的差距<br>3. 代表系统对比与企业视角 |

---

## 二、Harness Engineering 深度解析

### 2.1 定义

**Harness Engineering（根基工程）** 是构建 Agent 运行时基础设施的工程实践。它不为 Agent 提供"智能"（那是模型的事），而是为 Agent 提供"身体能力"——工具调用、权限控制、会话持久化、日志追踪等生产环境必需的基础服务。

类比：大语言模型（LLM）相当于"大脑"，Harness 相当于"身体"——没有身体的大脑只是一团能思考的神经元，无法在现实世界中执行任何操作。

### 2.2 技术原理：裸 Agent Loop vs Agent Harness

裸 Agent Loop（一个 `while` 循环 + LLM + 工具列表）可以在 Demo 中跑出令人印象深刻的效果。但一到生产环境，问题会逐层暴露：

```
裸 Agent Loop（~100行代码）            Agent Harness（完整运行时，数千~数万行）
──────────────────────────────        ─────────────────────────────────────────────

      用户输入                                     用户输入
         │                                           │
         ▼                                    ┌──────┴──────┐
      ┌──────┐                                │ Permission  │  权限校验
      │ LLM  │ 思考                            │    Gate     │  Allow/Ask/Deny/AskOnce
      └──┬───┘                                └──────┬──────┘
         │                                           │
         ▼                                           ▼
      ┌──────┐                                ┌──────────────┐
      │ 工具  │ 执行                            │    Tool      │  工具注册/发现/
      │ 调用  │ (无注册/无校验)                   │  Registry    │  版本管理/MCP接入
      └──┬───┘                                └──────┬───────┘
         │                                           │
         ▼                                           ▼
      ┌──────┐                                ┌──────────────┐
      │ LLM  │ 回答                            │    Hook      │  调用前/后/错误/
      └──┬───┘                                │   System     │  会话结束 拦截
         │                                    └──────┬───────┘
         │                                           │
    无持久化存储                                     ▼
    无日志追踪                                ┌──────────────┐
    无断点恢复                                │   Context    │  超出窗口时自动
    无权限控制                                │  Compaction  │  压缩/摘要
                                              └──────┬───────┘
                                                     │
                                                     ▼
                                              ┌──────────────┐
                                              │   Session    │  状态持久化/
                                              │    Store     │  断点恢复
                                              └──────┬───────┘
                                                     │
                                                     ▼
                                              ┌──────────────┐
                                              │  Trace/Log   │  每步可审计追踪/
                                              │              │  OpenTelemetry
                                              └──────┬───────┘
                                                     │
                                                     ▼
                                              ┌──────────────┐
                                              │ Agent Loop   │  高度优化的循环引擎
                                              │   Engine     │  可选子代理并行分发
                                              └──────────────┘

  问题全景：                                      Harness 解决：
  · 工具调用失败 → 无重试/无降级                     · 工具注册中心 + 版本管理
  · 模型输出 → 未校验直接执行                        · 权限门控：敏感操作必须人工确认
  · API Key → 暴露在日志中                           · Hook 拦截：脱敏/审计/合规
  · Token 消耗 → 失控                               · Context Compaction：智能压缩
  · Agent 崩溃 → 全部上下文丢失                       · Session Store：断点续执行
  · 出问题 → 无法排查                                · Trace/Log：结构化全链路追踪
```

**核心思想**：Agent 的能力很大一部分来自它的 Harness（底座），而不是模型本身。换一个模型（GPT-4 → Claude → DeepSeek），Harness 不变；如果 Harness 设计不当，换什么模型都没用。

### 2.3 六大核心组件详解

#### 2.3.1 Tool Registry（工具注册中心）

**技术原理**：将所有外部能力（API、数据库、文件系统、浏览器）统一抽象为"工具"，并提供标准化的注册、发现、调用和版本管理机制。工具不再硬编码在 Agent 代码中，而是通过标准化接口动态接入。

**MCP 协议（Model Context Protocol）** 是当前最重要的工具标准化协议：

```
传统工具集成                       MCP 标准化工具接入
──────────────────                ──────────────────────

每个工具独立编写适配代码             ┌─────────────────────────┐
                              ┌────│ MCP Server: Filesystem  │
                              │    │ - read_file             │
Agent ───┬── 工具A集成代码     │    │ - write_file            │
        ├── 工具B集成代码     │    │ - list_directory        │
        ├── 工具C集成代码     │    └─────────────────────────┘
        └── 工具D集成代码     │
                              │    ┌─────────────────────────┐
换模型 ≈ 重写全部集成代码        ├────│ MCP Server: Database    │
                              │    │ - query                 │
                              │    │ - describe_schema       │
                              │    └─────────────────────────┘
                              │
                              │    ┌─────────────────────────┐
                              ├────│ MCP Server: GitHub       │
                              │    │ - create_pr              │
Agent ─── MCP Client ─────────┤    │ - search_code           │
         (统一接口)            │    └─────────────────────────┘
                              │
                              │    统一 JSON-RPC over stdio/SSE
                              │    工具自动发现 + 版本协商
```

**Tool Registry 的核心能力**：

| 能力 | 说明 | 代表性技术 |
|------|------|-----------|
| **工具注册** | 每个工具向 Registry 注册名称、描述、参数 Schema、版本号 | MCP `tools/list` |
| **工具发现** | Agent 根据任务语义动态查询可用工具，而非全量暴露 | 语义匹配 / RAG 检索 |
| **参数校验** | 调用前验证参数类型、必填项、取值范围 | JSON Schema Validation |
| **版本管理** | 同一工具的多个版本共存，平滑迁移 | 语义化版本号 (v1.2.3) |
| **能力协商** | Agent 和工具间协商协议版本、超时设置、重试策略 | MCP `initialize` |

#### 2.3.2 Permission Gate（权限门控）

**技术原理**：在 Agent 执行敏感操作（删除文件、发送邮件、调用支付接口、修改数据库）前，由权限门控层拦截并请求用户确认。这是在"Agent 自主性"和"安全可控"之间的关键平衡点。

**Claude Code 的四级权限模型**：

```
用户触发操作
    │
    ▼
┌─────────────────────────────────────────────────────┐
│              Permission Gate 决策流程                  │
│                                                     │
│  操作类型: rm -rf /project/temp/                     │
│  风险等级: HIGH (不可逆文件删除)                        │
│                                                     │
│  ┌───────────────────────────────────────────┐      │
│  │            四级决策矩阵                      │      │
│  │                                           │      │
│  │  Allow    → 自动放行    (白名单操作)         │      │
│  │  例: 读取公开文件、执行 SELECT 查询          │      │
│  │                                           │      │
│  │  Ask      → 每次询问    (默认级别)           │      │
│  │  例: 修改代码文件、创建 PR                  │      │
│  │                                           │      │
│  │  Deny     → 直接拒绝    (黑名单操作)         │      │
│  │  例: 访问 ~/.ssh/、执行 DROP DATABASE       │      │
│  │                                           │      │
│  │  AskOnce  → 仅首次询问  (会话级缓存)         │      │
│  │  例: 同目录下的批量文件操作                  │      │
│  └───────────────────────────────────────────┘      │
│                                                     │
│  输出: Ask → 弹出确认对话框 → 用户选择 Allow/Deny      │
└─────────────────────────────────────────────────────┘
```

**企业级 Permission Gate 的扩展维度**：

| 维度 | 说明 | 示例 |
|------|------|------|
| **角色** | 不同角色有不同的权限集合 | 开发者可写代码 / 审计者只能读 |
| **环境** | 开发/测试/生产环境的权限分离 | 生产环境禁用删除、要求双重审批 |
| **时间窗口** | 特定时间段内自动放行 | 工作时间自动 / 非工作时间必须审批 |
| **预算限制** | API 调用费用的硬上限 | 单次任务 Token 消耗 ≤ $5 |

#### 2.3.3 Session Store（会话持久化）

**技术原理**：将 Agent 的完整会话状态（对话历史、工具调用记录、中间结果、当前任务上下文）持久化到外部存储（Redis/PostgreSQL/SQLite），支持断点恢复和跨设备继续执行。

```
会话生命周期：

┌────────────────────────────────────────────────────────────┐
│                                                            │
│  [1] 创建会话                                              │
│      session_id = uuid4()                                  │
│      state = { messages: [], tools: {}, status: "active" } │
│                            │                               │
│                            ▼                               │
│  [2] 执行中 — 每秒保存快照                                   │
│      ┌──────────────────────────────────────┐              │
│      │ Step 1: LLM 推理  → 保存 state       │              │
│      │ Step 2: Tool Call  → 保存 state      │              │
│      │ Step 3: Tool Result → 保存 state      │              │
│      │ Step 4: LLM 推理  → 保存 state       │              │
│      │ ...                                 │              │
│      │ Step N: Final Output → 保存 state    │              │
│      └──────────────────────────────────────┘              │
│                            │                               │
│                            ▼                               │
│  [3] 异常中断 — 崩溃 / 用户关闭 / 网络断开                     │
│      状态已持久化 → 不丢失                                    │
│                            │                               │
│                            ▼                               │
│  [4] 恢复执行                                              │
│      agent.resume(session_id)                              │
│      从最近 Checkpoint 的 state 继续                        │
│      用户感知: "什么都没丢，接着往下做"                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**存储选型对比**：

| 存储方案 | 适用场景 | 优点 | 缺点 |
|----------|----------|------|------|
| **SQLite** | 本地单机 | 零配置、嵌入式 | 不支持并发写入 |
| **Redis** | 高并发在线服务 | 内存级速度、TTL 自动清理 | 内存成本、持久化需额外配置 |
| **PostgreSQL** | 企业级多租户 | 强一致性、复杂查询、审计日志 | 延迟相对较高 |
| **文件存储 (JSON)** | 开发调试 | 最简单、人类可读 | 不可扩展、无查询能力 |

#### 2.3.4 Context Compaction（上下文压缩）

**技术原理**：当 Agent 的对话历史 + 工具输出超出模型上下文窗口限制时，自动执行压缩/摘要，保留关键信息、丢弃冗余细节，确保模型始终拥有做出正确判断所需的完整信息。

**分层压缩策略**（优先级从高到低）：

```
┌────────────────────────────────────────────────────────────┐
│                     分层压缩优先级                             │
│                                                            │
│  第 1 优先保留区 (永不压缩):                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ System Prompt (角色+核心规则)                          │  │
│  │ 当前任务描述                                           │  │
│  │ 最近的 2-3 轮对话                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  第 2 层 — 轻度压缩 (提取摘要 + 保留关键数据):                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 工具输出的详细日志 → 压缩为 "工具X返回350行数据，          │  │
│  │                       关键: avg_price=¥1,250,          │  │
│  │                       总记录=350条"                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  第 3 层 — 中度压缩 (保留决策链，丢弃中间推理):                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 早期对话历史 → 压缩为 "此前我们确认了:                     │  │
│  │                   1. 数据源为MySQL sales表              │  │
│  │                   2. 分析维度为按月+按品类               │  │
│  │                   3. CEO受众, 需要可视化建议"            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  第 4 层 — 激进压缩 (可丢弃，需要时重新检索):                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 已完成的旧任务的完整对话 → 提取知识存入记忆系统           │  │
│  │                             原对话可完全丢弃             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**压缩触发策略**：

| 策略 | 触发条件 | 效果 |
|------|----------|------|
| **阈值触发** | Token 使用量 > 窗口的 80% | 自动启动压缩，压缩至 50% 以下 |
| **步数触发** | 每 N 轮对话后 | 固定节奏压缩，避免突发 |
| **被动压缩** | API 返回 context_length_exceeded 错误 | 激进压缩后重试 |
| **手动触发** | 用户指令 `/compact` | 用户掌控时机 |

#### 2.3.5 Hook System（钩子系统）

**技术原理**：在 Agent 执行的关键生命周期节点（工具调用前/后、会话开始/结束、错误发生）插入用户自定义逻辑。Hook 是 Agent 可扩展性的核心机制——不需要修改 Agent 代码就可以增加审计、合规、安全等能力。

**Claude Code Hooks 四大事件类型**：

```
Agent 生命周期中的 Hook 注入点：

会话开始
    │
    ▼
┌─────────────────┐
│   Notification  │  ← "会话已启动" → 初始化资源/预热缓存
└────────┬────────┘
         │
    ┌────▼────┐
    │  LLM    │  思考/推理
    │  Think  │
    └────┬────┘
         │
         │  决定调用工具
         │
    ┌────▼────────────┐
    │  PreToolUse     │  ← 工具调用前拦截
    │                 │     · 参数校验/脱敏
    │  Hook 触发      │     · 权限二次确认
    │                 │     · 预算检查
    └────┬────────────┘
         │
    ┌────▼────┐
    │  Tool   │  执行
    │  Execute│
    └────┬────┘
         │
    ┌────▼────────────┐
    │  PostToolUse    │  ← 工具调用后拦截
    │                 │     · 结果脱敏
    │  Hook 触发      │     · 日志记录
    │                 │     · 输出校验
    └────┬────────────┘
         │
         │  (循环直到任务完成)
         │
    ┌────▼────────────┐
    │   Stop          │  ← 会话结束
    │                 │     · 清理临时资源
    │  Hook 触发      │     · 生成摘要报告
    │                 │     · 通知用户
    └─────────────────┘
```

**Hook 系统架构**：

```
┌──────────────────────────────────────────────────┐
│                  Hook Manager                     │
│                                                  │
│  hooks: [                                         │
│    {                                              │
│      "event": "PreToolUse",                       │
│      "matcher": "Bash",                           │
│      "command": "python audit.py",                │
│      "timeout": 5000                              │
│    },                                             │
│    {                                              │
│      "event": "PostToolUse",                      │
│      "matcher": "Write|Edit",                     │
│      "command": "npx prettier --check ${file}"    │
│    }                                              │
│  ]                                                │
│                                                  │
│  匹配逻辑: event 匹配 + matcher 正则 → 执行 command   │
│  超时保护: 每个 hook 最长执行 timeout 毫秒            │
│  错误处理: hook 失败 → 可配置 [阻塞/告警/忽略]         │
└──────────────────────────────────────────────────┘
```

#### 2.3.6 Trace/Log（追踪与日志）

**技术原理**：记录 Agent 每一步执行的完整信息——输入、输出、工具调用、Token 消耗、耗时、错误——形成可审计的完整追踪链。采用结构化日志（JSON 格式）而非纯文本日志，支持机器可读和自动分析。

**OpenTelemetry 标准集成**：

```
一次 Agent 执行的完整 Trace：

Trace ID: abc123-def456-ghi789
├── Span: Agent.Run (duration: 45.2s)
│   ├── Span: LLM.Think (step=1, tokens_in=3200, tokens_out=150, duration: 2.1s)
│   ├── Span: Tool.Call (name="read_file", params={path:"..."}, permission=Allow)
│   │   └── Span: Tool.Execute (duration: 0.3s, result_size: 1200 bytes)
│   ├── Span: LLM.Think (step=2, tokens_in=4500, tokens_out=80, duration: 1.8s)
│   ├── Span: Tool.Call (name="edit_file", params={...}, permission=Ask→Approved)
│   │   └── Span: Tool.Execute (duration: 0.1s, result: success)
│   ├── Span: LLM.Think (step=3, tokens_in=4800, tokens_out=200, duration: 2.5s)
│   └── Span: Agent.Complete (total_steps=3, total_tokens=12930, total_cost=$0.04)
│
└── Metadata:
    session_id: sess-xyz
    model: claude-sonnet-4-20250514
    tools_used: [read_file, edit_file]
    permission_decisions: {Allow: 1, Ask: 1}
    compaction_events: 0
```

**结构化日志字段定义**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `trace_id` | UUID | 一次 Agent 运行的全局唯一标识 |
| `span_id` | UUID | 单个操作的标识 |
| `parent_span_id` | UUID | 父操作标识，构建调用链 |
| `event.type` | Enum | `llm.call` / `tool.call` / `hook.fire` / `compaction.start` |
| `event.input` | JSON | 操作的输入参数 |
| `event.output` | JSON | 操作的输出结果 |
| `metrics.tokens_in` | int | 输入 Token 数 |
| `metrics.tokens_out` | int | 输出 Token 数 |
| `metrics.duration_ms` | int | 操作耗时（毫秒） |
| `security.permission` | Enum | `allow/ask/deny/askonce` |
| `error` | JSON\|null | 错误信息（如有） |

### 2.4 代表系统对比

| 维度 | Claude Code | Codex (OpenAI) | DeerFlow (字节跳动) | LangGraph |
|------|------------|----------------|---------------------|-----------|
| **定位** | CLI Coding Agent | 全平台编程 Agent | 通用 SuperAgent Runtime | 状态图编排框架 |
| **Tool Registry** | MCP 协议 | MCP + 内置沙箱工具 | Sandbox 内工具注册 | 自定义 Node |
| **Permission Gate** | Allow/Ask/Deny/AskOnce 四级 | Approval 流程 | 分级权限 | Human-in-the-loop 节点 |
| **Context Compaction** | 自动分层压缩 | 摘要压缩 | 记忆蒸馏 | Checkpoint 状态快照 |
| **Hook System** | PreToolUse/PostToolUse/Notification/Stop | Webhook 回调 | 事件监听器 | 节点前后 Hook |
| **Trace/Log** | 结构化 JSON 日志 | 内置追踪面板 | 全链路 Trace | LangSmith 集成 |
| **Session Store** | 本地文件 | 云端持久化 | Redis + PostgreSQL | Checkpointer API |
| **开源** | 否 (CLI 免费) | 部分开源 (SDK) | 开源 | 开源 (Apache 2.0) |

### 2.5 企业视角

> 📊 **企业视角**：Harness Engineering 是区分"能做 Demo"和"能上生产"的分水岭。2025 年 Harness Engineering 论文 (arXiv:2605.13357) 首次将其定义为一门独立工程学科。企业采购 AI 工具时，应重点评估其 Harness 成熟度——权限控制（谁来审批）、审计日志（做了什么、谁批准的）、错误恢复（崩了怎么办）——而非只看模型能力。一个 Harness 不成熟的 Agent 系统，上线后第一个生产事故就可能在几秒内造成无法挽回的损失（误删数据库、群发错误邮件、超支数万美元 API 费用）。

---

## 三、关键结论

1. **Harness Engineering 是 Agent 进入生产环境的必要条件**。没有 Harness 的 Agent 只是 Demo 玩具——缺乏权限控制、会话持久化、日志审计和错误恢复能力。

2. **Harness 的六个组件构成一个完整的运行时闭环**：Tool Registry（能力）→ Permission Gate（安全）→ Hook System（扩展）→ Context Compaction（效率）→ Session Store（可靠性）→ Trace/Log（可观测性）。缺少任何一个，生产环境都会出现致命短板。

3. **Agent 的"记忆"不是独立工程学科，而是 Context Engineering 的延伸能力**。短期记忆由上下文窗口承载，会话持久化由 Harness 的 Session Store 提供，跨会话的长期记忆则通过 mem0/Letta 等记忆层工具实现——记忆的本质是"把相关信息组织进上下文"。构建 Agent 时，应把记忆作为上下文管理的一部分来设计，而不是单独构建一套"记忆工程"。

4. **Skill / Tool / Prompt / MCP 四者不是竞争关系，而是互补关系**。Skill 定义操作知识（怎么做），Tool 提供执行能力（能做什么），Prompt 传达任务意图（要做什么），MCP 标准化通信协议（怎么连）。一个成熟的 Agent 系统需要四者协同。

5. **对企业而言，Harness 是"安全底线"，也是当前投入的重点**。先保证 Agent 的安全可控（权限、审计、恢复），再逐步演进到复杂编排（Loop/Graph）。采购 AI 工具时，应重点评估其 Harness 成熟度，而非只看模型能力。

---

# 第四部分：Loop Engineering 与 Graph Engineering 深度解析

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI 时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB4 / 本课共8个KB |
| **知识块标题** | Loop Engineering 与 Graph Engineering 深度解析 |
| **前置知识块** | KB3（Harness Engineering） |
| **预计时长** | 20分钟 |
| **知识块类型** | 技术讲授 |
| **适用对象** | 💼 企业管理者/投资人 + 🎓 零基础学习者（技术深度分级标注） |
| **核心议题** | 1. Agent 核心推理循环（Loop）的四代范式演进<br>2. 状态图编排（Graph）的六大核心概念<br>3. Loop vs Graph 的关系与协同 |

---

## 二、Loop Engineering 深度解析

### 2.1 定义

**Loop Engineering（循环工程）** 是设计 Agent 核心推理循环的工程实践。它决定了 Agent 在每一步如何观察状态、思考选项、做出决策、执行行动、评估结果——也就是 Agent "自主思考与行动"的完整过程。

Agent 与普通 Chatbot 的本质区别在于"循环"：Chatbot 是一问一答的线性交互；Agent 是**不断迭代、反复观察和调整，直到任务完成**的自主执行系统。

### 2.2 标准 Agent Loop 五步详解

```
┌─────────────────────────────────────────────────────────────────┐
│                   标准 Agent Loop (Observe→Think→Decide→Act→Feedback) │
│                                                                 │
│   ┌─────────────────────────────────────────────────────┐       │
│   │                                                     │       │
│   │   ① Observe (观察)                                   │       │
│   │   ┌───────────────────────────────────────────┐    │       │
│   │   │ 读取当前状态:                                │    │       │
│   │   │  · 用户说了什么?                             │    │       │
│   │   │  · 上一步工具调用返回了什么?                   │    │       │
│   │   │  · 环境状态有无变化? (文件系统/数据库/API)      │    │       │
│   │   │                                            │    │       │
│   │   │ 输入来源: 用户消息 + 工具输出 + 环境状态快照    │    │       │
│   │   └───────────────────────────────────────────┘    │       │
│   │                          │                          │       │
│   │                          ▼                          │       │
│   │   ② Think (思考)                                    │       │
│   │   ┌───────────────────────────────────────────┐    │       │
│   │   │ LLM 推理过程:                                │    │       │
│   │   │  · 我是否已经拥有完成任务所需的所有信息?        │    │       │
│   │   │  · 如果有缺口, 我需要什么信息?                 │    │       │
│   │   │  · 哪个工具可以获取这些信息?                   │    │       │
│   │   │  · 如果信息充足, 最佳答案是什么?               │    │       │
│   │   │                                            │    │       │
│   │   │ 关键能力: Chain-of-Thought (思维链)           │    │       │
│   │   └───────────────────────────────────────────┘    │       │
│   │                          │                          │       │
│   │                          ▼                          │       │
│   │   ③ Decide (决策)                                   │       │
│   │   ┌───────────────────────────────────────────┐    │       │
│   │   │          ┌── 信息充足? ──→ 生成最终答案       │    │       │
│   │   │ 决策点 ──┤                                  │    │       │
│   │   │          ├── 需要更多信息? ──→ 选择工具+构造参数│    │       │
│   │   │          │                                  │    │       │
│   │   │          └── 超出能力/权限? ──→ 请求人工介入   │    │       │
│   │   └───────────────────────────────────────────┘    │       │
│   │                          │                          │       │
│   │       ┌──────────────────┼──────────────────┐       │
│   │       │ 最终答案          │ 工具调用           │       │
│   │       ▼                  ▼                   │       │
│   │   ④ Act (执行)                                 │       │
│   │   ┌──────────────────────────────────────┐    │       │
│   │   │  如果是工具调用:                        │    │       │
│   │   │    1. 权限校验 (Permission Gate)       │    │       │
│   │   │    2. 执行工具 (API/Shell/DB/...)     │    │       │
│   │   │    3. 捕获结果/超时/错误               │    │       │
│   │   │    4. 格式化工具输出                  │    │       │
│   │   │                                       │    │       │
│   │   │  如果是最终答案:                        │    │       │
│   │   │    输出 → 退出循环 → 返回用户           │    │       │
│   │   └──────────────────────────────────────┘    │       │
│   │                          │                       │       │
│   │                          ▼                       │       │
│   │   ⑤ Feedback (反馈)                               │       │
│   │   ┌──────────────────────────────────────┐       │       │
│   │   │  工具输出重新注入上下文窗口:             │       │       │
│   │   │                                       │       │       │
│   │   │  Context += ToolOutput                │       │       │
│   │   │  判断: 是否触发 Compaction?            │       │       │
│   │   │  判断: 是否达到 max_steps?             │       │       │
│   │   │                                       │       │       │
│   │   │  循环继续 → 回到 ① Observe              │       │       │
│   │   └──────────────────────────────────────┘       │       │
│   │                                                     │       │
│   └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**五步之间的关系**：

```
Observe ──→ Think ──→ Decide ──→ Act ──→ Feedback ──┐
   ▲                                                  │
   └──────────────────────────────────────────────────┘

核心循环: 每一步的 Act/Feedback 产生新信息
         → Observe 读取新信息
         → Think 重新评估
         → Decide 重新决策
         → 直到任务完成或达到停止条件
```

### 2.3 Loop 设计的关键参数

| 参数 | 作用 | 典型值 | 调优原则 |
|------|------|--------|----------|
| **max_steps** | 最大循环步数，防止无限循环 | 10-50 | 简单任务设低 (10-15)，复杂任务设高 (30-50)。超过限制时强制输出当前状态，不做无意义的继续循环 |
| **timeout** | 单步超时（秒） | 30-120s | 工具调用可能很慢（数据库查询、大文件处理），需合理设置。设太短 = 正常的慢操作被误杀；设太长 = 异常卡死时浪费资源 |
| **tool_call_limit** | 单次 LLM 响应可调用的工具数量上限 | 1-5 | 过多工具调用增加 Token 消耗，且模型注意力分散。默认 1（一次一个工具）最稳定 |
| **retry_on_error** | 工具调用失败时的重试次数 | 1-3 | 网络抖动/临时超时值得重试（retryable errors）；逻辑错误/参数错误不应重试（non-retryable errors），应直接反馈给 LLM 重新决策 |
| **human_in_the_loop** | 在哪些节点插入人工审批 | 敏感操作前 | 删除/付款/发送邮件 → 必须审批。查询/读取 → 可自动。原则: 不可逆操作一律需要人工确认 |
| **early_stop** | 任务完成时提前停止 | enabled | 当 LLM 明确输出最终答案（而非工具调用）时立即退出循环，不等 max_steps |
| **loop_detection** | 检测死循环（重复调用同一工具+同一参数） | 3次重复触发 | 连续 3 次以相同参数调用同一工具 → 强制中断 → 请求人工介入 |

**参数配置示例**：

```json
{
  "max_steps": 30,
  "timeout_ms": 60000,
  "tool_call_limit": 1,
  "retry": {
    "max_retries": 2,
    "retryable_errors": ["timeout", "rate_limit", "connection_error"],
    "non_retryable_errors": ["validation_error", "permission_denied", "not_found"]
  },
  "human_in_the_loop": {
    "nodes": ["before_delete_file", "before_send_email", "before_payment"],
    "mode": "interrupt_and_wait"
  },
  "stop_conditions": {
    "early_stop_enabled": true,
    "loop_detection_threshold": 3
  }
}
```

### 2.4 Loop 范式演进

Agent Loop 并非只有一种形态。从 2022 年至今，学术界和工业界不断演化出更高效、更可靠的 Loop 范式。

```
Loop 范式演进时间线:

2022 Q4    2023 Q1        2023 Q3         2024 Q1
   │          │              │               │
ReAct ────→ Plan-and ────→ Reflexion ───→  ReWOO
            -Execute                       (最省钱)
(最基础)
```

#### 2.4.1 ReAct（Reasoning + Acting）— 推理与行动交替

**核心思路**：每一步先推理（Think），再行动（Act），然后观察结果（Observe），循环往复。

```
ReAct Loop:

┌──────────────────────────────────────────┐
│                                          │
│  Think: "用户问上个月销售情况，             │
│         我需要先查询数据库"                 │
│         ↓                                │
│  Act:  query_database("SELECT ...")      │
│         ↓                                │
│  Observe: "返回了 350 行数据，             │
│           平均销售额 ¥1,250"              │
│         ↓                                │
│  Think: "数据量太大，需要按品类汇总，        │
│         调用分析工具"                       │
│         ↓                                │
│  Act:  analyze_by_category(data)         │
│         ↓                                │
│  ... 直到任务完成                          │
│                                          │
│  特点: 灵活、通用                          │
│  缺点: 步骤多时 LLM 调用次数多 ($$)        │
│        每一步都要等待上一步结果，无法并行      │
│  代表: LangChain ReAct Agent             │
│  适用: 通用任务，工具调用间有依赖关系         │
└──────────────────────────────────────────┘
```

#### 2.4.2 Plan-and-Execute — 先完整规划，再逐步执行

**核心思路**：第一步先让 LLM 生成完整的执行计划（包含所有步骤和工具调用），然后按计划逐步执行。执行过程中发现偏差时，回到规划步骤重新规划。

```
Plan-and-Execute Loop:

┌──────────────────────────────────────────────┐
│                                              │
│  Phase 1: Plan (规划)                         │
│  ┌──────────────────────────────────────┐    │
│  │ LLM 分析任务 → 生成完整步骤列表:        │    │
│  │                                      │    │
│  │ Plan:                                 │    │
│  │   1. 查询 sales 表获取原始数据          │    │
│  │   2. 按品类分组计算 SUM                │    │
│  │   3. 按月份分组计算趋势                │    │
│  │   4. 生成可视化图表                    │    │
│  │   5. 基于数据写分析报告                │    │
│  │                                      │    │
│  │ 输出: 结构化 Plan Object              │    │
│  └──────────────┬───────────────────────┘    │
│                 │                             │
│  Phase 2: Execute (执行)                       │
│  ┌──────────────┴───────────────────────┐    │
│  │ 逐步执行 Plan 中的每个步骤:             │    │
│  │                                      │    │
│  │ Step 1: query_database → ✓          │    │
│  │ Step 2: group_by_category → ✓       │    │
│  │ Step 3: trend_by_month → ✓          │    │
│  │ Step 4: 发现: 图表库不可用 → ✗        │    │
│  │                                      │    │
│  │ 检测到偏差 → 回到 Phase 1 重新规划      │    │
│  │ → 新 Plan: 用文字描述替代图表           │    │
│  │                                      │    │
│  │ Step 4': 生成文字版趋势描述 → ✓       │    │
│  │ Step 5: 写分析报告 → ✓               │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  特点: 步骤明确、可审查                        │
│  缺点: 初始规划可能不准确 (计划赶不上变化)       │
│  代表: LangGraph Plan-and-Execute 模式        │
│  适用: 步骤明确、结构化的任务                    │
└──────────────────────────────────────────────┘
```

#### 2.4.3 Reflexion — 执行后自我反思，存入长期记忆

**核心思路**：在每次执行任务后增加一个"反思"步骤——评估做得好的地方、做得差的地方、下次可以改进的地方。反思结果被存入长期记忆，供未来的任务参考。

```
Reflexion Loop:

┌──────────────────────────────────────────────────────┐
│                                                      │
│  标准执行循环 (ReAct / Plan-and-Execute)               │
│       │                                               │
│       ▼                                               │
│  ┌──────────────────────────────────────┐            │
│  │ 任务完成                               │            │
│  └──────────────────┬───────────────────┘            │
│                     │                                │
│                     ▼                                │
│  ┌──────────────────────────────────────┐            │
│  │ Reflexion 反思阶段                     │            │
│  │                                      │            │
│  │ LLM 作为 Evaluator:                   │            │
│  │   输入: 完整的执行轨迹 (所有步骤+结果)    │            │
│  │   输出:                               │            │
│  │   · 成功之处: 用了异步查询, 速度快      │            │
│  │   · 失败之处: 第一次 SQL 语法错误,      │            │
│  │              浪费了一次 LLM 调用       │            │
│  │   · 改进建议: 下次先用 EXPLAIN 验证SQL  │            │
│  │                                      │            │
│  │ 反思结果 → 写入长期记忆                 │            │
│  │ {                                     │            │
│  │   "lesson": "SQL查询前先EXPLAIN验证",   │            │
│  │   "context": "数据库查询任务",           │            │
│  │   "confidence": 0.9                    │            │
│  │ }                                     │            │
│  └──────────────────┬───────────────────┘            │
│                     │                                │
│                     ▼                                │
│  下一次类似任务时:                                     │
│    检索到此反思记忆 → 自动在第一步执行 EXPLAIN           │
│                                                      │
│  特点: 越用越聪明、持续改进                              │
│  缺点: 增加一次额外的 LLM 调用（反思阶段）                 │
│  代表: Reflexion Agent (Shinn et al., 2023)           │
│  适用: 需要持续改进的重复性任务                          │
└──────────────────────────────────────────────────────┘
```

#### 2.4.4 ReWOO（Reason WithOut Observation）— 一次性规划，并行执行

**核心思路**：LLM 一次性生成所有工具调用的完整计划，然后并行执行所有互不依赖的工具调用，最后再让 LLM 基于所有工具结果一次性生成最终答案。核心创新：**去掉了中间的"观察→思考"循环环节**。

```
ReWOO Loop:

┌────────────────────────────────────────────────────────┐
│                                                        │
│  传统 ReAct (6 次 LLM 调用):                             │
│  LLM(Think1) → Tool1 → LLM(Think2) → Tool2 → ...       │
│  串行, 总耗时 = 6 × LLM延迟 + 工具总耗时                 │
│                                                        │
│  ─────────────────────────────────────────────────────  │
│                                                        │
│  ReWOO (2 次 LLM 调用):                                 │
│                                                        │
│  第 1 次 LLM: 生成完整执行计划                             │
│  ┌────────────────────────────────────────────┐       │
│  │ Plan:                                       │       │
│  │   #E1 = query_database("SELECT * ...")     │       │
│  │   #E2 = fetch_api("https://api.market...") │       │
│  │   #E3 = read_file("/docs/sales_report.md") │       │
│  │                                             │       │
│  │  依赖分析: #E1, #E2, #E3 互不依赖 → 可并行    │       │
│  └──────────────┬─────────────────────────────┘       │
│                 │                                      │
│                 ▼                                      │
│  ┌────────────────────────────────────────────┐       │
│  │ 并行执行 (同时触发 3 个工具):                  │       │
│  │                                             │       │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐      │       │
│  │  │ #E1     │  │ #E2     │  │ #E3     │      │       │
│  │  │ 数据库   │  │ API调用  │  │ 文件读取 │      │       │
│  │  │ 查询    │  │         │  │         │      │       │
│  │  └────┬────┘  └────┬────┘  └────┬────┘      │       │
│  │       │            │            │            │       │
│  │       └────────────┼────────────┘            │       │
│  │                    ▼                         │       │
│  │              收集所有结果                      │       │
│  └──────────────┬─────────────────────────────┘       │
│                 │                                      │
│                 ▼                                      │
│  第 2 次 LLM: 基于所有工具结果一次性生成最终答案           │
│                                                        │
│  总耗时 = 2 × LLM延迟 + max(工具耗时) 并行执行           │
│  Token 消耗远低于 ReAct                                │
│                                                        │
│  特点: 省钱 (LLM 调用少)、提速 (并行执行)                  │
│  缺点: 工具调用间有依赖时无法使用;                         │
│        如果初始规划错误, 无法中途调整                      │
│  代表: smolagents CodeAgent                           │
│  适用: 工具调用间无依赖关系, 且步骤可预见的场景            │
└────────────────────────────────────────────────────────┘
```

**四种范式对比总结**：

| 范式 | LLM 调用次数 | 并行能力 | 适应性 | 成本 | 最佳场景 |
|------|-------------|---------|--------|------|----------|
| **ReAct** | 最多 (每步1次) | 无 | 最强 (实时调整) | 最高 | 工具调用间有强依赖 |
| **Plan-and-Execute** | 中等 (规划+调整) | 有限 | 较强 (可重新规划) | 中高 | 步骤明确的结构化任务 |
| **Reflexion** | ReAct/Plan + 1次反思 | 取决于基底范式 | 最强 (越用越聪明) | 最高+ | 需持续改进的重复任务 |
| **ReWOO** | 最少 (2次) | 强 (全部可并行) | 最弱 (无法中途调整) | 最低 | 工具调用互不依赖 |

### 2.5 Claude Code 中的 Loop 设计特色

Claude Code 的 Agent Loop 引入了几个独特的设计选择：

| 设计特点 | 实现方式 | 带来的优势 |
|----------|----------|-----------|
| **条件性工具激活** | 不是每次都列出全部工具，根据任务类型动态激活工具子集 | 减少 Token 浪费，避免模型注意力分散 |
| **上下文感知停止条件** | 检测任务是否"实际完成"（而非 LLM 说"完成了"），例如代码已修改且测试通过 | 避免假性完成任务（LLM 声称完成但实际未做） |
| **子代理分发** | 复杂任务自动拆分为独立子任务，分发到独立子代理 | 并行处理、独立错误隔离、更清晰的推理 |
| **渐进式权限** | 第一步只读模式运行，确认理解任务后才开放写入权限 | 防止 Agent 误解任务后批量破坏文件 |
| **自动回退** | 检测到操作未产生预期效果时，自动撤销并尝试替代方案 | 减少人工干预，提高自主成功率 |

### 2.6 企业视角

> 📊 **企业视角**：Loop Engineering 是 Agent 可靠性工程的核心。企业场景中最怕的三种情况——(1) Agent 进入死循环烧 Token、(2) Agent 做出错误决策后继续滚雪球、(3) Agent 声称完成但实际未做——都可以通过 Loop 设计来解决。一个好的 Loop 设计 = 合理的 max_steps + 关键节点 human_in_the_loop + 异常检测与熔断 + early_stop。从成本角度看，选择正确的 Loop 范式（ReAct vs ReWOO）可以在不影响质量的情况下将 API 费用降低 40-60%。

---

## 三、Graph Engineering 深度解析

### 3.1 定义

**Graph Engineering（图工程）** 是使用状态图（State Graph）来编排 Agent 工作流的工程实践。它将 Agent 的工作流建模为节点（Node）+ 边（Edge）+ 条件分支（Conditional Edge），使 Agent 的行为可预测、可恢复、可审计。

Agent Loop 是**线性的**（一个 while 循环），但真实的企业工作流往往需要**分支、并行、回退、暂停审批**。Graph Engineering 用"图"来建模这些复杂流程。

### 3.2 Agent Loop vs Graph Engineering

```
Agent Loop 模式                              Graph Engineering 模式
(线性循环)                                    (有向状态图)
──────────────────                          ──────────────────────────

     START                                       ┌──────┐
       │                                         │ START│
       ▼                                         └──┬───┘
  ┌─────────┐                                       │
  │  Agent  │←─────────────┐                    ┌───▼───┐
  │  (LLM)  │              │                    │ Router│  路由判断
  └────┬────┘              │                    └───┬───┘
       │                   │              ┌─────────┼─────────┐
       ▼                   │              │         │         │
  ┌─────────┐              │          ┌───▼──┐  ┌───▼──┐  ┌───▼──┐
  │  Tools  │              │          │Research│ │Analyze│ │Execute│
  └────┬────┘              │          └───┬───┘  └───┬───┘  └───┬───┘
       │                   │              │         │         │
       ▼                   │              └────┬────┘    ┌────┘
  ┌─────────┐              │                   │         │
  │  Done?  │──── 否 ──────┘                   └────┬────┘
  └────┬────┘                                       │
       │ 是                                    ┌────▼─────┐
       ▼                                       │ Reviewer  │  人工审核节点
      END                                      └────┬─────┘
                                              ┌─────┴─────┐
  优点: 简单、通用                               │           │
  缺点: 无法表达分支/并行/审批                   ▼           ▼
       无法暂停/恢复                           ┌──┐      ┌────┐
       无法审计每一步                        通过│  │ 驳回 │重新│
                                               └──┘      │执行│
                                               │         └──┬─┘
                                               ▼            │
                                              END  ←────────┘
                                                      (回到上游节点)

                                          优点: 分支/并行/回退/审批全部可建模
                                               每步自动保存 → 可暂停/恢复
                                               每步可追踪 → 可审计
```

### 3.3 六大核心概念详解

```
┌─────────────────────────────────────────────────────────────────┐
│                     Graph Engineering 六大核心概念                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ① State (状态)                                               ││
│  │                                                             ││
│  │ State 是图中流转的共享数据对象，每个 Node 读取 State,          ││
│  │ 执行处理后修改 State。State 的完整历史形成审计链。              ││
│  │                                                             ││
│  │ 技术形态: TypedDict (LangGraph) / Pydantic Model             ││
│  │                                                             ││
│  │ 示例:                                                        ││
│  │ class AgentState(TypedDict):                                ││
│  │     messages: List[Message]    # 对话历史                    ││
│  │     current_step: str          # 当前在哪个节点              ││
│  │     tool_results: Dict         # 工具调用结果                ││
│  │     final_output: Optional[str] # 最终输出                   ││
│  │     approval_status: Literal["pending","approved","denied"] ││
│  │                                                             ││
│  │ 商业含义: 一个"数字工单"，记录工作流中全部已产生的信息和决策     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ② Node (节点)                                                ││
│  │                                                             ││
│  │ Node 是一个独立的处理单元。常见的 Node 类型:                    ││
│  │                                                             ││
│  │ · LLM Node: 调用 LLM 进行推理/生成                            ││
│  │ · Tool Node: 执行外部工具调用                                 ││
│  │ · Human Node: 等待人工输入/审批                               ││
│  │ · Router Node: 纯逻辑判断，不调用 LLM (省钱)                   ││
│  │ · Parallel Node: 并行分发到多个子 Node                        ││
│  │                                                             ││
│  │ 每个 Node 的接口:                                             ││
│  │   node(state: State) → Dict[StateUpdate]                    ││
│  │   (读取 State → 处理 → 返回 State 更新)                       ││
│  │                                                             ││
│  │ 商业含义: 一个"工作步骤"，映射到企业流程中的岗位或操作          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ③ Edge (边)                                                  ││
│  │                                                             ││
│  │ Edge 定义节点间的固定流转路径:                                  ││
│  │   Node_A ────Edge────→ Node_B                               ││
│  │                                                             ││
│  │ 静态边: graph.add_edge("node_a", "node_b")                  ││
│  │ 商业含义: 工作流中的必经流程 (如: 合同生成后 → 必须法务审批)     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ④ Conditional Edge (条件边)                                  ││
│  │                                                             ││
│  │ 根据 State 中的条件动态选择下一个节点:                          ││
│  │                                                             ││
│  │               ┌── 条件A为真? → Node_X                        ││
│  │   Node_A ────┤                                              ││
│  │               └── 条件A为假? → Node_Y                        ││
│  │                                                             ││
│  │ 路由函数:                                                     ││
│  │   def route(state):                                         ││
│  │       if state["approval"] == "approved":                   ││
│  │           return "execute"                                  ││
│  │       else:                                                  ││
│  │           return "revise"                                   ││
│  │                                                             ││
│  │ 商业含义: 审批通过 → 执行; 审批驳回 → 退回修改                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ⑤ Checkpoint (检查点)                                        ││
│  │                                                             ││
│  │ 每个 Super-step (Node 执行 + 状态更新) 后自动保存 State 快照:   ││
│  │                                                             ││
│  │ Step 0: State{ messages:[] }             ← Checkpoint[0]    ││
│  │ Step 1: State{ messages:[...], ... }     ← Checkpoint[1]    ││
│  │ Step 2: State{ messages:[...], ... }     ← Checkpoint[2]    ││
│  │   ... (Agent 崩溃)                                          ││
│  │                                                             ││
│  │ 恢复: state = checkpointer.load(checkpoint_id=2)            ││
│  │       graph.resume(state)  # 从 Step 3 继续                  ││
│  │                                                             ││
│  │ 商业含义: 工作流可随时暂停/恢复/回溯 —— 企业合规审计的刚需       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ⑥ Human-in-the-loop (人机协同)                                ││
│  │                                                             ││
│  │ 在关键节点设置 interrupt point, 等待人工确认后才能继续:         ││
│  │                                                             ││
│  │  # 到达审核节点时自动暂停                                      ││
│  │  graph.add_node("review", interrupt=True)                   ││
│  │                                                             ││
│  │  # 人工审核 → 更新 State → 继续执行                            ││
│  │  graph.update_state(                                        ││
│  │      config,                                                ││
│  │      {"approval": "approved", "comment": "LGTM"}            ││
│  │  )                                                          ││
│  │                                                             ││
│  │ 商业含义: 关键决策的人类审批阀 —— AI 准备, 人做决定              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 三大核心技术改进

#### 3.4.1 断点续执行（Persistence）

LangGraph Checkpointer API 是 Graph Engineering 最核心的基础设施。**每个 Super-step 自动保存 State**，Agent 无论在哪个步骤崩溃，都可以从最近的 Checkpoint 恢复，而非从头开始。

```
LangGraph Checkpointer API:

┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  初始化：                                                       │
│  from langgraph.checkpoint.postgres import PostgresSaver      │
│  checkpointer = PostgresSaver(conn_string)                     │
│  graph = builder.compile(checkpointer=checkpointer)            │
│                                                               │
│  配置执行线程：                                                  │
│  config = {"configurable": {"thread_id": "task-001"}}         │
│                                                               │
│  首次执行：                                                     │
│  for event in graph.stream(                                    │
│      {"messages": [user_message]},                             │
│      config                                                    │
│  ):                                                           │
│      # 每个 event 对应一个 Checkpoint 被保存                    │
│                                                               │
│  # 如果在此处崩溃/暂停...                                       │
│                                                               │
│  恢复执行：                                                     │
│  # 不需要重新传 user_message，Checkpointer 知道上次执行到哪了    │
│  for event in graph.stream(                                    │
│      None,                     # ← 传入 None!                 │
│      config                                                   │
│  ):                                                           │
│      # 自动从最近的 Checkpoint 继续                             │
│                                                               │
│  查看历史：                                                     │
│  history = list(graph.get_state_history(config))               │
│  # 按时间倒序返回所有 Checkpoint                                │
│  # 可回溯到任意历史 Checkpoint 并重新执行                        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**三种恢复模式**：

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| **从最后 Checkpoint 继续** | 像什么都没发生过一样继续 | 网络中断、进程崩溃 |
| **回溯到特定 Checkpoint** | 回退到某个历史点，丢弃之后的执行 | 发现之前的决策错误，重新来 |
| **Fork 新分支** | 从某个 Checkpoint 创建独立分支 | A/B 测试不同策略 |

#### 3.4.2 并行扇出（Fan-out / Fan-in）

将复杂任务拆分为多个并行子任务，由多个 Worker 同时执行，然后由一个 Collector 汇总结果。

```
Fan-out / Fan-in 模式 (Supervisor → Workers → Collector):

                         ┌──────────┐
                         │Supervisor│  分析任务 → 拆分为 N 个子任务
                         └────┬─────┘
                              │
                    Fan-out   │  (并行分发)
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │ Worker A │       │ Worker B │       │ Worker C │
    │ 研究竞品A │       │ 研究竞品B │       │ 研究竞品C │
    └────┬─────┘       └────┬─────┘       └────┬─────┘
         │                   │                   │
         │  各自独立执行       │                   │
         │  互不依赖           │                   │
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    Fan-in   │  (汇总收集)
                             ▼
                      ┌────────────┐
                      │ Collector  │  汇总所有 Worker 输出
                      │            │  去重/合并/评优
                      └──────┬─────┘
                             │
                             ▼
                      ┌────────────┐
                      │ Synthesizer│  LLM 综合 → 最终报告
                      └────────────┘

  性能对比：
  · 串行执行: 5min + 5min + 5min = 15min
  · 并行执行: max(5min, 5min, 5min) = 5min (3x 加速)
```

**三种 Fan-out 策略**：

| 策略 | 触发方式 | 适用场景 |
|------|----------|----------|
| **静态 Fan-out** | 图编译时 N 个 Worker 已固定 | Worker 数量可预见的场景 |
| **动态 Fan-out** | Supervisor 运行时决定生成几个 Worker | 根据任务复杂度灵活分配 |
| **递归 Fan-out** | Worker 发现子任务后继续 Fan-out 到更细粒度的 Worker | 树状分解任务（如代码库分析） |

#### 3.4.3 流式事件（Streaming Events）

每个 Node 的执行状态以事件流方式实时推送，前端可实时展示工作流进度。

```
Streaming Events 架构:

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  for event in graph.stream(input, config, stream_mode="updates"):
│      #                                                       │
│      # 事件流输出:                                            │
│      #                                                       │
│      # { "router": { "next": "research" } }                  │
│      #   → UI 更新: "正在路由..."                             │
│      #                                                       │
│      # { "research": { "status": "searching", "query": "..." }}│
│      #   → UI 更新: "正在搜索相关资料..."                      │
│      #                                                       │
│      # { "research": { "status": "done", "results": 15 }}    │
│      #   → UI 更新: "找到15条相关资料"                         │
│      #                                                       │
│      # { "analysis": { "status": "analyzing", "chunk": "3/15" }}│
│      #   → UI 更新: "正在分析第3/15条..."                      │
│      #                                                       │
│      # { "reviewer": { "status": "waiting_approval" }}        │
│      #   → UI 更新: "⚠️ 等待人工审批..."                       │
│      #                                                       │
│      # { "execute": { "status": "done" }}                     │
│      #   → UI 更新: "执行完成"                                 │
│                                                              │
│  用户看到的 UI:                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  任务: 竞品分析报告                                        │ │
│  │  ✅ 路由判断 (0.1s)                                       │ │
│  │  ✅ 搜集竞品A资料 (2.1s)                                   │ │
│  │  ✅ 搜集竞品B资料 (1.8s)                                   │ │
│  │  ⏳ 正在分析... (第 3/15 条)                               │ │
│  │  ⏸️ 等待审批                                               │ │
│  │  ⬜ 生成报告                                               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Streaming 的四种模式 (LangGraph)**：

| 模式 | 输出粒度 | 用途 |
|------|----------|------|
| `values` | 每个 Super-step 后的完整 State | 调试、审计 |
| `updates` | 每个 Node 对 State 的增量更新 | 前端进度展示 |
| `messages` | LLM 的 Token 级流式输出 | 打字机效果 |
| `debug` | 包含所有内部执行细节 | 开发调试 |

### 3.5 代表工具

| 工具 | 核心能力 | 实现方式 | 适用场景 |
|------|----------|----------|----------|
| **LangGraph** | 完整 StateGraph 框架：State/Node/Edge/Conditional Edge/Checkpoint/Human-in-the-loop/Streaming | Python 库，声明式图定义 + Checkpointer API | 复杂企业工作流的 Agent 编排 |
| **Claude Code Subagents + Hooks** | 子代理分发 + Hook 拦截 = 隐式的工作流图 | Subagent 并行执行 + Pipe 串联 | Coding Agent 工作流（编译→测试→lint→修复） |
| **n8n + AI** | 可视化低代码工作流编排 + LLM Node 连接 | 拖拽式 UI + 内置 LLM/AI 节点 | 企业内部自动化（非技术人员可操作） |
| **LangGraph Cloud** | 托管版 LangGraph + 持久化 + 监控面板 | SaaS 部署 + LangSmith 监控 | 不想自建基础设施的企业团队 |

### 3.6 企业视角

> 📊 **企业视角**：Graph Engineering 是最接近"企业流程数字化"的 AI 工程层。它把 AI 的"黑箱决策"变成了"可审计的流转图"——这在金融、医疗、法律等强监管行业是 AI 落地的必要条件。监管机构需要的不是"AI 做得对"的承诺，而是可以被审计的工作流记录——每一步谁做了什么、基于什么信息、做出的什么决策、决策结果如何。
>
> Graph Engineering 的 ROI 体现在三个层面：
> 1. **合规成本**：自动化生成审计报告，减少 80% 的手工合规文档准备时间
> 2. **流程弹性**：Checkpoint 机制让长时间运行的工作流不怕中断，减少因系统故障导致的重做成本
> 3. **流程优化**：基于 Trace 数据分析工作流瓶颈（哪个 Node 耗时最长？哪个决策点错误率最高？），驱动持续优化

---

## 四、Loop vs Graph 的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                    Loop 与 Graph 的关系                          │
│                                                                 │
│  不是竞争关系，而是不同维度的互补:                                  │
│                                                                 │
│  Loop Engineering:  决定 Agent "每一步怎么想、怎么做"              │
│                     (微观 —— 单步推理的质量和效率)                  │
│                                                                 │
│  Graph Engineering: 决定 Agent "整体流程怎么走"                    │
│                     (宏观 —— 多步工作流的编排和控制)                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  形象的类比：                                                     │
│                                                                 │
│  Loop   = 一个工人的思维过程                                     │
│          "我应该先做什么? 这个工具好用吗? 结果对吗?"                 │
│                                                                 │
│  Graph  = 工厂的生产流水线                                        │
│          "订单进来 → A工位 → B工位 → 质检 → 打包 → 发货"          │
│                                                                 │
│  一个工厂 (Graph) 里有许多工人 (Loop)，                             │
│  每个工人有自己的思维过程，流水线定义了工人之间的协作方式。              │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  技术关系：                                                       │
│                                                                 │
│  ┌─────────┐                                                    │
│  │  Graph  │  编排层 (在哪里执行、什么顺序、什么条件)                │
│  └────┬────┘                                                    │
│       │  Graph 中的每个 LLM/Agent Node                           │
│       │  内嵌一个 Loop 引擎                                      │
│       ▼                                                         │
│  ┌─────────┐                                                    │
│  │  Loop   │  执行层 (每一步怎么思考、怎么调用工具)                  │
│  └─────────┘                                                    │
│                                                                 │
│  一个 Graph 工作流 = N 个 Node                                   │
│  其中 LLM/Agent Node = 一个完整的 Loop 引擎                       │
│                                                                 │
│  例: LangGraph Agent Node → 内部使用 ReAct Loop                  │
│      Graph 定义了"何时启动 Agent"、"Agent 完成后去哪"、            │
│      "Agent 失败时怎么办"，而 Loop 定义了 Agent 在"                 │
│      每一轮推理周期内如何运作。                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、关键结论

1. **Loop Engineering 是 Agent "智能"的微观体现**。从 ReAct 到 ReWOO，Loop 范式在不断进化——核心趋势是从"串行 + 多轮 LLM 调用"走向"并行 + 最少 LLM 调用"，在保障质量的同时大幅降低成本。

2. **四种 Loop 范式是工具，不是教条**。实际工程中，复杂 Agent 会根据任务类型动态切换 Loop 范式：明确的步骤用 Plan-and-Execute，互不依赖的工具调用用 ReWOO 并行，需要灵活应变的用 ReAct 串行。

3. **Graph Engineering 解决的是 Loop 无法解决的问题**：分支逻辑、并行执行、人工审批、断点恢复。Loop 处理"怎么做"，Graph 处理"怎么编排做"。

4. **Checkpoint 是 Graph Engineering 最被低估的核心能力**。它不仅支持断点续执行（可靠性），还支持历史回溯（调试/审计）、Fork 分支（A/B 测试）、状态回放（合规）。在金融、医疗等强监管行业，Checkpoint 链就是合规审计的"数字证据链"。

5. **Streaming Events 改变了 Agent 的用户体验**。从"黑箱等待"变成"实时可见的进度条"——用户可以实时看到 Agent 在做什么、卡在哪一步、需要什么决策。这让用户从"焦虑的等待者"变为"有掌控感的监督者"。

6. **Loop + Graph 的结合是 Agent 工程化的终极形态**。Graph 编排工作流（宏观可控），Loop 驱动每步推理（微观智能），两者分层协作，构成了从"单个 Agent 任务"到"企业级多 Agent 工作流"的完整技术栈。

---

# 第五部分：Prompt Engineering 实战详解

---

## 1. 知识块信息表

| 属性 | 内容 |
|------|------|
| **知识块编号** | KB5 |
| **知识块名称** | Prompt Engineering 实战详解 |
| **所属章节** | 五（Prompt Engineering 深入）第 5.1 ~ 5.5 节 |
| **建议时长** | 25 分钟 |
| **前置知识** | KB1 ~ KB4（AI 基础认知），AI 工程体系五层金字塔 |
| **知识类型** | 概念 + 实操 |
| **适用对象** | 零基础学习者 / 企业管理者 |
| **核心能力目标** | 掌握 RCTE 框架 + 8 种 Prompt 技巧 + 4 类任务模板，能独立写出高质量 Prompt |

---

## 2. Prompt Engineering 基本定义与技术原理

### 2.1 核心定义

**Prompt（提示词）** 是用户与大语言模型（LLM）交互时输入的文本指令。
**Prompt Engineering（提示词工程）** 是系统化设计、优化和管理这些文本指令的工程方法论。

从技术底层看，大语言模型的本质是**自回归下一个 Token 预测器（Autoregressive Next-Token Predictor）**。模型在接收到输入序列后，基于训练数据中习得的概率分布，逐个预测最可能的下一个 Token。

**Prompt 的技术作用 = 对模型的"续写概率分布"施加精确的方向性约束。**

```
模型内部机制（简化）：

输入 Token 序列 → Embedding → Transformer Layers → 
Softmax 概率分布（词汇表中每个 Token 的概率）→ 采样 → 输出 Token

Prompt 的约束作用发生在输入端：
  - 差的 Prompt → 概率分布在广泛的语义空间上分散 → 输出不可控
  - 好的 Prompt → 概率分布集中在目标语义空间 → 输出可预期
```

### 2.2 有 Prompt vs 无 Prompt 对比

```
═══════════════════════════════════════════════════════════════════════════

【无 Prompt（纯续写模式）】
  输入：
    "人工智能的未来"

  模型行为：
    模型将此视为一段未完成文本的开头，按照训练语料的统计规律续写。
    输出方向完全由模型训练数据中的最常见后续决定，用户无控制权。

  实际输出示例：
    "人工智能的未来将会非常美好，人类将与机器和谐共处，
     共同创造一个前所未有的文明时代。在这个时代中，智能机器
     将成为人类最忠实的伙伴..."

  问题分析：
    - 输出方向不可控（泛泛而谈的未来畅想）
    - 长度不可控（可能 50 字也可能 5000 字）
    - 格式不可控（散文式叙述）
    - 深度不可控（停留在表面论述）

───────────────────────────────────────────────────────────────────────────

【有 Prompt（精确引导模式）】
  输入：
    "请用 200 字，从技术、商业、社会三个维度分析人工智能的未来发展趋势。
     每个维度分两段：现状（1句）和 3 年内预测（2句）。用数字序号标注。"

  模型行为：
    Prompt 中的约束（字数、维度、结构、格式）大幅缩小了模型在
    每个预测位置的合理 Token 选择范围。模型被"强制"沿着用户
    规划的方向续写。

  实际输出示例：
    1. 技术维度
       现状：当前大模型在推理能力和多模态融合方面持续突破，
            但幻觉问题和推理成本仍是核心瓶颈。
       预测：未来3年，模型参数效率将提升10倍以上，通过MoE架构
            和知识蒸馏实现端侧部署；Agent自主编程能力将达到
            中级工程师水平，但完全自主仍需人工监督。

    2. 商业维度
       现状：AI应用正从"Copilot辅助"向"Agent自主执行"过渡，
            SaaS行业面临根本性重构。
       预测：每家企业将拥有至少3个专职AI Agent处理客服、数据
            分析和代码审查；按Token付费的AI成本模型将向按任务
            价值定价迁移。

    3. 社会维度
       现状：AI素养差距成为新的社会不平等来源，各国监管框架
           仍在追赶技术发展速度。
       预测：AI技能将从"竞争优势"转变为"基础就业门槛"；
            AI生成内容的标识和水印将成为法律强制要求。

  对比分析：
    - 输出方向精确可控（技术/商业/社会三维）
    - 长度精确（约200字）
    - 结构规整（编号 + 两段式）
    - 深度可控（现状 + 预测）
```

### 2.3 为什么同样模型、不同 Prompt 质量天差地别

```
═══════════════════════════════════════════════════════════════════════════

同一模型（Claude Sonnet 5），同一主题，不同 Prompt 质量 → 不同输出

┌───────────────────────────────────────────────────────────────────────┐
│ 对比维度          │ 差 Prompt               │ 好 Prompt               │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ 信息密度          │ 低，大量通用套话        │ 高，句句有信息量        │
│ 结构清晰度        │ 平铺直叙，无层次        │ 标题/编号/表格/分层     │
│ 专业深度          │ 浅层常识                │ 基于角色设定的深度      │
│ 可操作性          │ 抽象建议                │ 具体可执行的步骤        │
│ 针对性            │ 通用回答                │ 针对具体场景定制        │
│ Token 效率        │ 长文低效                │ 每 Token 信息量大       │
│ 格式一致性        │ 不可预期                │ 严格按指定格式输出      │
└───────────────────────────────────────────────────────────────────────┘

技术原因（从模型角度）：
  1. 注意力聚焦：高质量 Prompt 通过角色设定和约束条件，将模型的
     注意力机制聚焦在特定的知识子空间上。
  2. 采样路径约束：格式要求和示例缩小了每步采样的 Token 候选集，
     减少了模型"跑偏"的概率。
  3. 知识激活精准度：明确的 Context 让模型激活更相关的训练知识，
     而非依赖通用的高频知识模式。
```

### 2.4 Prompt Engineering 与上下文窗口的关系

```
上下文窗口内各元素的 Token 分配策略：

┌─────────────────────────────────────────────────────────────┐
│                  Context Window（典型：200K Token）           │
│                                                             │
│  System Prompt（角色 + 规则 + 格式约束）    ← 消耗 ~1-3K     │
│  用户 Prompt（RCTE 框架）                   ← 消耗 ~0.5-2K   │
│  对话历史（多轮上下文）                     ← 消耗 ~5-50K    │
│  工具定义/检索结果/附件                     ← 消耗 ~3-30K    │
│  剩余 Token 空间（模型输出的舞台）          ← ~150K+         │
│                                                             │
│  原则：Prompt 越精准，越能为真正的工作内容节省 Token 空间。    │
│       臃肿的 Prompt 不仅浪费 Token，还会稀释模型注意力。       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. RCTE 框架详解

> RCTE 是 Prompt Engineering 领域最基础、最通用的结构化框架，由 Role（角色）、Context（上下文）、Task（任务）、Example（示例）四个维度组成。所有高级 Prompt 技巧都可以看作 RCTE 框架的延伸和深化。

```
┌─────────────────────────────────────────────────────────────────┐
│                    RCTE Prompt 框架                              │
│                                                                 │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│   │  Role    │   │ Context  │   │  Task    │   │ Example  │    │
│   │  角色    │ → │  上下文  │ → │  任务    │ → │  示例    │    │
│   │          │   │          │   │          │   │          │    │
│   │ 定义     │   │ 提供     │   │ 描述     │   │ 展示     │    │
│   │ "谁"    │   │ "在哪/   │   │ "做什么" │   │ "做成    │    │
│   │ 来回答  │   │  什么    │   │          │   │  什么样" │    │
│   │          │   │  条件"   │   │          │   │          │    │
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘    │
│                                                                 │
│   复杂度递进关系：R < R+C < R+C+T < R+C+T+E                      │
│   基础版只需 R+T，完整版四要素齐全。                              │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 R (Role) — 角色设定

**定义**：通过自然语言为模型设定一个特定的"专业身份"，从而激活模型中与该身份相关的知识分布和语言风格模式。

**技术原理**：大模型在训练过程中学习了大量带身份标签的文本（如论文作者、技术博客写手、咨询报告撰稿人等）。设定 Role 本质上是将模型的"输出风格概率分布"向该身份对应的写作习惯偏移。

**角色设定效果对比表**：

```
┌────────────────────────────────────────────────────────────────────┐
│ 任务：分析一家咖啡店的经营问题并提出改善方案                           │
├────────────────────┬────────────────────┬───────────────────────────┤
│ 不设定角色          │ "你是一位资深连锁    │ "你是一位麦肯锡咨询顾问"  │
│                    │  餐饮行业顾问"       │                          │
├────────────────────┼────────────────────┼───────────────────────────┤
│ 输出特征：          │ 输出特征：           │ 输出特征：                │
│ • 通用建议          │ • 行业术语精准       │ • 结构化分析框架          │
│ • 浅层分析          │ • 涉及供应链/坪效    │ • MECE分解                │
│ • 无数据框架        │ • 竞品对比           │ • "以数据为导向"         │
│   "可以考虑提升     │   "建议优化SKU组合，  │   "基于五力模型分析，     │
│    服务质量"        │    将坪效从2000提升   │    当前竞争格局呈现..."  │
│                    │    至3500元/平米"     │                          │
├────────────────────┼────────────────────┼───────────────────────────┤
│ 适用场景            │ 行业深度分析         │ 高层战略决策              │
│ 不适合场景          │ 所有需要专业输出的   │ 需要细粒度技术方案时      │
│                    │ 场景                │                          │
└────────────────────┴────────────────────┴───────────────────────────┘
```

**Role 设定规范**：

```
标准 Role 描述结构：
  "你是一位 [行业/领域] 的 [职级/经验年限] [具体专业方向] [专家/从业者]"

示例：
  ✅ "你是一位有 10 年经验的 Java 后端架构师"
  ✅ "你是一位专注于消费者行为研究的市场调研专家"
  ✅ "你是一位最高人民法院指导案例研究学者"

  ⚠️ "你是一个技术专家"（领域太宽泛，激活的知识分布不精确）
  ⚠️ "你是一个很厉害的人"（无领域锚定，效果与不设角色几乎相同）

进阶用法 —— 复合角色：
  "你是一个由三人组成的虚拟团队：
   - 首席架构师：负责技术方案的整体设计
   - 安全专家：负责方案的安全性审查
   - 成本分析师：负责方案的ROI评估
   请在回答中标注每个观点来自哪个角色。"
```

### 3.2 C (Context) — 上下文信息

**定义**：为模型提供任务执行的背景信息，包括目标受众、使用场景、限制条件、历史尝试等。Context 决定了模型输出应该"面向谁"和"在什么边界内"。

**好的 Context 应包含的信息维度**：

```
┌───────────────────────────────────────────────────────────────────┐
│ Context 信息维度              │ 示例                               │
├───────────────────────────────┼────────────────────────────────────┤
│ 1. 目标受众 (Audience)        │ "目标读者是公司CEO（5分钟阅读时间）"│
│    - 谁来消费这个输出？        │ "面向初中生，语言要通俗易懂"        │
│    - 他们的知识水平如何？      │                                    │
│    - 他们的核心关切是什么？    │                                    │
├───────────────────────────────┼────────────────────────────────────┤
│ 2. 使用场景 (Scenario)        │ "用于内部技术评审会议"              │
│    - 输出将在什么场合使用？    │ "替代方案：社交媒体推广文案"        │
│    - 是正式还是非正式？        │                                    │
│    - 有没有替代方案？          │                                    │
├───────────────────────────────┼────────────────────────────────────┤
│ 3. 限制条件 (Constraints)     │ "预算上限50万元，工期3个月"         │
│    - 字数/篇幅限制             │ "不得引用第三方库"                  │
│    - 预算/时间/资源限制        │ "必须符合GDPR数据保护要求"          │
│    - 技术栈/合规要求           │                                    │
├───────────────────────────────┼────────────────────────────────────┤
│ 4. 历史信息 (History)         │ "上一版方案因成本过高被驳回"         │
│    - 之前尝试过什么？          │ "用户已确认使用PostgreSQL数据库"     │
│    - 已有决策/结论是什么？     │ "此前讨论已确定采用微服务架构"       │
│    - 避免AI给出重复/无效方案   │                                    │
├───────────────────────────────┼────────────────────────────────────┤
│ 5. 数据/参考资料 (Reference)  │ "参考以下销售数据：[粘贴数据]"      │
│    - 需要分析的原始材料        │ "对标竞品为A公司和B公司的产品"      │
│    - 参考范例或对标对象       │                                    │
└───────────────────────────────────────────────────────────────────┘
```

**Context 质量对比**：

| Context 质量 | 示例 | 输出效果 |
|-------------|------|----------|
| **无 Context** | "写一份项目计划书" | AI 自行假设所有条件，输出大概率与你的实际需求不符 |
| **简单 Context** | "写一份软件开发项目计划书" | 方向正确，但细节全凭 AI 猜测 |
| **详细 Context** | "写一份面向CTO的Web应用开发项目计划书。项目使用React+FastAPI，团队5人，周期3个月，预算30万。CTO最关心的是技术选型的可维护性和团队学习成本。" | AI 输出精准匹配需求，可直接作为初稿使用 |

### 3.3 T (Task) — 任务描述

**定义**：精确描述期望 AI 完成的具体输出。Task 是 RCTE 框架中最核心的维度——它直接定义了"输出什么"。

**模糊 Task vs 精确 Task 对比表**：

```
┌──────────────────────────────────────────────────────────────────────┐
│ 场景               │ 模糊 Task              │ 精确 Task               │
├────────────────────┼────────────────────────┼─────────────────────────┤
│ 方案分析           │ "帮我分析这个方案"     │ "从成本、工期、安全性三  │
│                    │                        │ 个维度评估方案，每维度给 │
│                    │                        │ 出0-5分评分、扣分原因、  │
│                    │                        │ 改进建议。用表格汇总。"  │
├────────────────────┼────────────────────────┼─────────────────────────┤
│ 文章写作           │ "写一篇关于AI的文章"   │ "写一篇面向中小企业CEO的 │
│                    │                        │ 800字文章。主题：AI落地  │
│                    │                        │ 的5个关键决策。结构：引   │
│                    │                        │ 言(100字)+5个决策各      │
│                    │                        │ (120字)+结论(100字)。"   │
├────────────────────┼────────────────────────┼─────────────────────────┤
│ 代码编写           │ "写一个用户登录功能"   │ "用Python FastAPI实现     │
│                    │                        │ 登录接口：接收JSON       │
│                    │                        │ {username,password}，   │
│                    │                        │ 返回JWT token。处理      │
│                    │                        │ 场景：成功/密码错误/      │
│                    │                        │ 用户不存在/账户锁定。"   │
├────────────────────┼────────────────────────┼─────────────────────────┤
│ 数据分析           │ "分析这份销售数据"     │ "分析2025年Q1-Q4的销售   │
│                    │                        │ 数据，找出：1)季度增长   │
│                    │                        │ 趋势 2)Top3增长品类      │
│                    │                        │ 3)异常波动月份 4)下季度  │
│                    │                        │ 预测。每项用图表建议+     │
│                    │                        │ 文字解读。"             │
├────────────────────┼────────────────────────┼─────────────────────────┤
│ PPT大纲            │ "做个PPT"              │ "生成10页季度汇报PPT大纲 │
│                    │                        │ ：每页含标题+3个要点+    │
│                    │                        │ 建议图表类型。顺序：     │
│                    │                        │ 封面→摘要→业绩→问题→    │
│                    │                        │ 竞品→计划→团队→预算→    │
│                    │                        │ 风险→总结。"            │
└──────────────────────────────────────────────────────────────────────┘
```

**Task 精确化的三个维度**：

```
1. 输出结构（Output Structure）
   - 分几部分？每部分什么标题？
   - 用列表、表格还是段落？
   - 每部分的大致篇幅？

2. 输出标准（Output Criteria）
   - 质量评判标准是什么？
   - 什么是"好的"输出？
   - 什么是不可接受的？

3. 输出范围（Output Scope）
   - 覆盖哪些子主题？
   - 不覆盖哪些子主题？（负面约束）
   - 深度到什么层次？
```

### 3.4 E (Example) — 示例参考

**定义**：通过提供一个或多个参考范例，让模型精确理解期望的格式、风格、深度和结构。Example 是 RCTE 框架中的"加速器"——它比任何文字描述都更直接地告诉模型"就是这个样子"。

**Example 的技术价值**：

```
为什么 Example 如此有效？

从模型角度来看：
  1. Few-shot Learning：示例触发了模型的上下文学习（In-Context Learning）
     能力。模型不需要更新参数，仅通过输入中的示例就能适配新任务。

  2. 格式锚定：示例为输出格式提供了一个精确的"锚点"。相比用自然语言
     描述格式（"用表格输出，第一列是...第二列是..."），直接给一个
     示例表格，模型模仿的准确度显著更高。

  3. 歧义消除：自然语言描述不可避免地存在歧义。同一句话"专业风格"
     在不同人心中可能完全不同。但一个示例能精确传达什么是你心中的
     "专业风格"。

  4. 边界对齐：示例展示了输出深度的预期边界。一个浅显的示例会让模型
     知道"这个深度就够了"，一个深入的示例则告诉模型"你需要挖到这个层次"。
```

**完整的 Example 提供模板**：

```
Task: 撰写竞品分析报告

Example（请严格按以下格式输出）：

═══════════════════════════════════════════
【竞品名称】飞书（Feishu）

【一句话定位】
面向中大型企业的下一代协作平台，以文档、会议、IM 三合一为核心卖点。

【核心优势】（3个要点）
1. 文档协作体验业界最优：支持多人实时编辑、思维导图、多维表格等丰富内容块
2. 会议与日历深度集成：会议纪要自动关联日历事件，会后自动分发
3. 生态系统完整：飞书应用目录覆盖HR、财务、CRM等企业全场景

【核心劣势】（3个要点）
1. 迁移成本高：从企业微信/钉钉迁移时，历史数据迁移工具不完善
2. 中小企业友好度不足：定价较高，功能复杂度超出小团队需求
3. 国际版功能滞后：海外版功能更新比中国版慢 1-2 个季度

【对我方的威胁等级】★★★★☆ (4/5)

【关键差异点分析】
- 与我方产品最大的区别在于 [XXX]
- 我方在 [XXX] 方面有明显优势
- 在 [XXX] 方面我方需要警惕

【应对策略建议】
1. 短期（1个月）：[具体措施]
2. 中期（3个月）：[具体措施]
3. 长期（6个月）：[具体措施]
═══════════════════════════════════════════

请用以上格式，分析竞品 [填入竞品名称]。
```

**避免使用 Example 的常见误区**：

```
❌ 误区 1：给出的示例与实际需求差异过大
   问题：示例写的是"手机产品竞品分析"，但你实际需要的是"SaaS产品竞品分析"
   后果：模型会照搬不适合的分析维度

❌ 误区 2：示例太过于简单，无法体现深度要求
   问题：示例只有标题框架没有详细内容
   后果：模型可能认为"列出标题就够了"

❌ 误区 3：给出多个风格不一致的示例
   问题：Example 1 用表格，Example 2 用段落，Example 3 用列表
   后果：模型无法确定你到底想要哪种格式
```

---

## 4. 常见 Prompt 技巧大全

### 4.1 八大核心技巧速览表

| 编号 | 技巧名称 | 核心思路 | 作用机制 | 适用场景 |
|------|----------|----------|----------|----------|
| T1 | **分步提问** (Step-by-Step) | 将复杂任务拆解为多个子步骤，逐步引导模型 | 减小每步的推理空间，提升每步准确率 | 复杂分析、多步骤任务、长篇写作 |
| T2 | **设定格式** (Format Specification) | 明确指定输出的结构形态 | 直接约束输出的 Token 序列结构 | 所有需要规整输出的场景 |
| T3 | **思维链** (Chain-of-Thought, CoT) | 要求模型先展示推理过程，再给出最终结论 | 强制模型进行多步推理，减少跳跃式错误 | 数学推理、逻辑分析、决策判断 |
| T4 | **小样本示例** (Few-shot) | 提供 2-3 个完整的输入-输出范例 | 通过上下文学习触发模型的任务适配能力 | 格式要求复杂的任务、分类任务 |
| T5 | **负面约束** (Negative Constraints) | 明确指定不应该出现的内容或方向 | 在概率分布中压制不需要的输出路径 | 格式控制、安全防范、风格限定 |
| T6 | **角色扮演** (Role-playing, 即 RCTE 的 R) | 为模型设定专业身份 | 激活特定领域的知识分布和语言风格 | 专业领域写作、技术分析 |
| T7 | **迭代优化** (Iterative Refinement) | 基于上一轮输出给出反馈，持续调整 | 利用多轮对话逐步逼近目标输出 | 复杂创作、方案设计、代码调试 |
| T8 | **结构化输出** (Structured Output) | 强制要求 JSON/XML/Markdown 等结构化格式 | 将自由文本转换为可被程序解析的数据结构 | API调用、数据提取、自动化流水线 |

### 4.2 每个技巧的优化前后对比

**T1：分步提问**

```
【优化前】一次性抛出所有需求
Prompt: "分析我们公司上季度的销售数据，找出问题，给出改善方案，
        做成一页CEO摘要，还要有图表建议。"

问题：模型可能遗漏某个子任务，或输出结构混乱。

───────────────────────────────────────────────────────────

【优化后】分3轮逐步推进

第1轮 Prompt:
  "首先，请分析上季度销售数据中的3个核心趋势和2个异常值。
   数据如下：[粘贴数据]"

第2轮 Prompt:
  "基于上述趋势和异常值，深入分析根本原因，
   每个趋势和异常值各给出至少2个深层原因。"

第3轮 Prompt:
  "将以上分析整理为一页CEO摘要：
   格式——标题（10字）+3个核心发现（每项30字）+
   风险信号（1条）+行动建议（3条，每条20字）。"

效果：每步聚焦单一目标，输出质量显著提升，且便于在中途调整方向。
```

**T2：设定格式**

```
【优化前】
Prompt: "对比一下Python和JavaScript"

可能输出：一段自由格式的散文式对比，无结构，难以快速提取关键信息。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "对比Python和JavaScript，请用以下表格格式输出：
| 对比维度 | Python | JavaScript | 推荐场景 |
| 语法简洁度 | ... | ... | ... |
| 性能 | ... | ... | ... |
| 生态/库 | ... | ... | ... |
| 学习曲线 | ... | ... | ... |
| 典型应用 | ... | ... | ... |
最后用3句话总结选择建议。"

效果：输出格式严格可控，信息一目了然。
```

**T3：思维链 (CoT)**

```
【优化前】
Prompt: "一家超市的苹果进货价每斤3元，售价每斤5元。
        今天进了50斤，卖了42斤，有3斤在运输中损坏。
        今天的利润是多少？"

模型可能直接给出错误答案（忘记扣除损坏成本）。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "一家超市的苹果进货价每斤3元，售价每斤5元。
        今天进了50斤，卖了42斤，有3斤在运输中损坏。
        请一步步思考：今天的利润是多少？

        请按以下步骤推理：
        1. 总收入是多少？
        2. 总进货成本是多少？
        3. 损坏导致的损失是多少？
        4. 总成本是多少？
        5. 总利润 = 总收入 - 总成本"

模型按步骤推理，每一步出错时下一步可纠偏，最终准确率大幅提升。
```

**T4：Few-shot**

```
【优化前】
Prompt: "写一篇产品评测"

输出：格式、风格、深度完全不可预期。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "请参考以下两篇评测的风格和结构，写一篇关于 [新产品] 的评测。

[示例1: iPhone评测]
  标题：数字+观点式
  第一段：一句话总结 + 适合谁/不适合谁
  正文：外观→性能→续航→相机→系统，每段150字
  结论：购买建议（不同需求对应不同推荐）

[示例2: MacBook评测]
  标题：数字+观点式
  第一段：一句话总结 + 适合谁/不适合谁
  正文：设计→屏幕→性能→续航→键盘，每段150字
  结论：购买建议

请用同样结构写一篇关于 [新产品] 的评测。"

效果：模型输出与示例风格高度一致。
```

**T5：负面约束**

```
【优化前】
Prompt: "解释一下什么是机器学习"

可能输出：充满专业术语，对非技术读者不友好。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "解释一下什么是机器学习。
  约束：
  - 不要使用任何数学公式
  - 不要使用以下术语：神经网络、梯度下降、反向传播、特征工程
  - 不要超过300字
  - 不要使用类比（比如"像人类学习一样"）"

效果：模型被迫用全新的方式重新组织解释，输出真正通俗易懂。
```

**T6：角色扮演**

```
【优化前】
Prompt: "帮我写一段内部控制制度"

输出：通用模板式的制度文本。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "你是一位有15年经验的四大会计师事务所风险管理合伙人，
  专门为上市公司设计内部控制体系。
  请帮我写一段关于'采购付款审批流程'的内部控制制度。"

输出：包含COSO框架引用、职责分离原则、审批阈值设计、
     反欺诈措施等专业内容。远超通用模板的深度和实操性。
```

**T7：迭代优化**

```
【优化前】
第一轮 Prompt: "写一个市场推广方案"
输出不满意 → 用户放弃，得出结论"AI 写不好方案"

───────────────────────────────────────────────────────────

【优化后】
第1轮 Prompt: "请列出针对Z世代消费者的3种创新推广策略大纲"
  模型输出：大纲

第2轮 Prompt: "策略2'社群裂变'最有潜力，请展开为详细执行计划，
  包含：具体步骤(5步)、所需资源、预期效果指标、风险预案"

第3轮 Prompt: "执行计划第3步'KOC筛选'不够具体。
  请补充：KOC筛选标准(5条)、触达渠道(3个)、
  话术模板(2套)、合作报价范围"

第4轮 Prompt: "整体方案看起来不错。请将所有内容整合为一份
  完整的市场推广方案，用PDF-ready的格式。"

效果：每轮在上轮基础上深入，最终产出高质量完整方案。
```

**T8：结构化输出**

```
【优化前】
Prompt: "分析这些用户反馈，提取关键信息"
  输出：一段混合了所有信息的自然语言段落，无法程序化处理。

───────────────────────────────────────────────────────────

【优化后】
Prompt: "分析以下用户反馈，提取关键信息，以严格合法的JSON格式输出。
{
  'sentiment': 'positive' | 'negative' | 'neutral',
  'topics': ['主题1', '主题2'],
  'urgency': 'low' | 'medium' | 'high',
  'actionable_items': [
    {'item': '具体问题', 'suggested_action': '建议措施', 'priority': 1-5}
  ],
  'summary': '30字以内总结'
}
只输出JSON，不要有其他文字。"

效果：输出可直接被下游程序解析，进入自动化处理流水线。
```

---

## 5. 不同任务的 Prompt 模板库

### 5.1 写作类模板

```
═══════════════════════════════════════════════════════════
模板名称：通用写作 Prompt 模板（RCTE 完整版）
═══════════════════════════════════════════════════════════

Role:
  你是一位 [领域] 的资深 [职业/身份]，拥有 [年限] 年经验，
  尤其擅长 [具体细分方向]。

Context:
  - 目标读者：[读者身份描述]，他们的核心关切是 [关切点]
  - 使用场景：[内部/对外/学术/社交媒体]
  - 字数限制：[XXX-XXX字]
  - 特殊情况：[已有哪些材料/需要避开哪些话题]

Task:
  请撰写一篇关于 [主题] 的 [文体类型]。
  结构要求：[引言(XX字)-正文(X部分)-结论(XX字)]
  风格要求：[学术严谨/轻松易读/实操性强/有说服力]
  必须包含：[数据引用/案例分析/实操步骤/对比分析] (选填)

Example:
  [粘贴风格参考范文]

═══════════════════════════════════════════════════════════
```

**写作类变体速查**：

| 文体 | Role 建议 | 结构建议 | 特殊要求 |
|------|----------|----------|----------|
| 公众号文章 | 自媒体主编/爆款文案写手 | 钩子开头→3个观点→金句收尾 | 短段落、多换行、强情绪 |
| 学术论文 | 该领域教授/研究员 | 摘要→引言→方法→结果→讨论 | 引用格式、学术用语 |
| 产品文案 | 4A广告公司资深文案 | 痛点→产品亮点→使用场景→CTA | 突出差异化、用户视角 |
| 周报/月报 | 部门负责人 | 核心成果→数据→问题→下周计划 | 简洁、数据驱动 |

### 5.2 编程类模板

```
═══════════════════════════════════════════════════════════
模板名称：代码生成 Prompt 模板
═══════════════════════════════════════════════════════════

Role:
  你是一位资深 [编程语言] [后端/前端/全栈/算法] 工程师，
  在 [具体领域] 有 [年限] 年开发经验，
  代码审查标准参照 [行业标准/公司规范]。

Context:
  - 项目技术栈：[框架/数据库/部署环境]
  - 代码风格：[PEP 8 / Google Style / Airbnb Style]
  - 依赖限制：[可用/禁用的第三方库]
  - 兼容性要求：[浏览器版本/OS/运行时版本]

Task:
  实现 [功能描述]，具体要求：
  1. 功能层面：[输入什么 → 处理什么 → 输出什么]
  2. 性能层面：[时间复杂度 / 并发处理 / 内存限制]
  3. 安全层面：[输入校验 / SQL注入防范 / XSS防护]
  4. 异常处理：[空值/超时/网络错误/权限不足] 每种情况都要处理
  5. 代码注释：[中文/英文]，覆盖关键逻辑

Example:
```
  // 参考以下代码风格和注释规范
  [粘贴参考代码片段]
  ```
═══════════════════════════════════════════════════════════
```

**编程类常见任务细分**：

| 任务类型 | Prompt 关键要素 | 输出要求 |
|----------|----------------|----------|
| **新功能开发** | 输入/输出定义 + 边界条件 + 测试用例 | 完整可运行代码 + 单元测试 |
| **Bug 修复** | 错误信息 + 复现步骤 + 期望行为 | 问题根因分析 + 修复代码 + 验证方法 |
| **代码审查** | 审查维度（安全/性能/可读性/架构） | 每条问题配严重级别 + 改进建议 |
| **重构优化** | 现有实现 + 重构目标（性能/可读性/扩展性） | 重构后代码 + 改动说明 + 风险评估 |

### 5.3 分析类模板

```
═══════════════════════════════════════════════════════════
模板名称：数据分析 Prompt 模板
═══════════════════════════════════════════════════════════

Role:
  你是一位 [行业] 领域的数据分析师，擅长从数据中发现
  [趋势/异常/业务机会]，曾在 [行业头部公司] 负责数据分析。

Context:
  - 数据说明：[表格/CSV/数据库] 格式，包含 [N] 条记录
  - 字段含义：[列名1]: [说明], [列名2]: [说明], ...
  - 时间范围：[起始] ~ [截止]
  - 业务背景：[公司/产品/市场情况简述]
  - 特殊说明：[数据中的已知问题/数据口径定义]

Task:
  分析维度（按需选择）：
  1. 趋势分析：[指标] 的时间变化趋势，转折点和异常波动
  2. 分组对比：按 [分组维度] 对比 [对比指标]
  3. 异常检测：[指标] 的离群值和异常模式
  4. 相关性：关键指标间的相关关系
  5. 预测建议：基于历史数据的下阶段预测

  每个分析点输出：数据事实 + 业务解读 + 行动建议

  总输出格式：要点列表，每个要点不超过 2 行
═══════════════════════════════════════════════════════════
```

### 5.4 企业高管摘要类模板

```
═══════════════════════════════════════════════════════════
模板名称：CEO 一页摘要 Prompt 模板
═══════════════════════════════════════════════════════════

Role:
  你是一位 CEO 战略顾问，曾服务于 [行业头部公司] 的董事会。
  你的核心专长是将复杂信息提炼为高层决策者需要的核心洞察。

Context:
  - 目标读者：公司董事会/CEO（平均阅读时间 5 分钟）
  - 材料来源：[技术报告/市场分析/财务数据/竞品情报]
  - 读者背景：非技术背景，关注战略、风险和资源分配
  - 决策需求：需要在 [时间范围] 内做出 [决策类型]

Task:
  将以下内容转化为 CEO 级别的一页战略摘要：

  ┌─────────────────────────────────────────┐
  │ 标题（10字以内，直接点出核心信息）        │
  │                                         │
  │ 三个核心发现（每项30字以内）：            │
  │   1. [发现一 + 数据支撑]                 │
  │   2. [发现二 + 数据支撑]                 │
  │   3. [发现三 + 数据支撑]                 │
  │                                         │
  │ 一个风险信号（20字）：                   │
  │   [最关键的风险或不确定性]               │
  │                                         │
  │ 决策建议（50字以内）：                   │
  │   [清晰、可落地的决策建议，不含模棱两可]  │
  └─────────────────────────────────────────┘

约束：
  - 不使用任何未在源材料中出现的数据
  - 每条发现必须有源材料中的数据支撑
  - 不使用"建议考虑""可以进一步研究"等模糊措辞
═══════════════════════════════════════════════════════════
```

---

## 6. Prompt 优化的 8 个技巧

### 优化前后对比总表

| 编号 | 优化技巧 | 优化前 Prompt（问题版） | 问题诊断 | 优化后 Prompt（改进版） | 优化原理 |
|------|---------|----------------------|----------|----------------------|----------|
| 1 | **具体化** | "写一个好方案" | 形容词"好"对模型无约束力，模型不知道什么是你心中的"好" | "写一个2000字的XX项目方案，包含市场分析（500字）、技术路线（800字）、财务预测（500字）、风险评估（200字）四部分" | 将模糊评价词替换为可测量的规格描述 |
| 2 | **结构化** | "我要做一个咖啡店，帮我分析一下要注意什么"（一大段叙述） | 信息混在一起，模型难以区分关键信息和次要信息 | "【项目】大学城旁咖啡店【面积】200平【预算】50万【目标客群】大学生\n请分析：1.选址建议 2.菜单设计 3.定价策略 4.推广方案" | 用标签、编号、分层将需求结构化 |
| 3 | **给例子** | "写一个专业的商务邮件" | "专业"在每个领域的表现形式完全不同，模型只能依赖高频通用模板 | "参考以下邮件风格：[粘贴1-2封你认可的邮件]。请用这个风格写一封关于XX的邮件" | 示例是消除"专业"等模糊词歧义的最有效工具 |
| 4 | **设约束** | 不提任何限制条件 | 模型可能使用过度复杂的方案、不合适的工具或超出预算的建议 | "约束：1.不引入第三方库 2.总代码不超过200行 3.时间复杂度O(n) 4.仅使用Python标准库" | 约束条件缩小了解空间，产出更聚焦 |
| 5 | **定角色** | "帮我分析一下这个市场" | 模型以通用知识回答，缺乏行业特定的分析框架和术语 | "你是一位曾服务过星巴克和瑞幸的餐饮行业分析师，请用波特五力模型分析XX市场" | 角色激活特定领域的专业知识分布和行业分析框架 |
| 6 | **迭代** | 一次 Prompt 输出不满意就放弃，认为"AI不行" | 期望 AI 一次就完美理解你的全部意图是不现实的 | 第1轮：要大纲 → 第2轮：展开第X部分 → 第3轮：调整语气 → 第4轮：补充数据 → 第5轮：最终润色 | 将"一次完美"转变为"逐步逼近"，每轮只解决一个问题 |
| 7 | **给反馈** | "不对，重写" | 模型不知道"不对"在哪里，新输出大概率同样"不对" | "第二部分的成本估算偏低了，因为物流成本每年涨15%，请按涨价后的数字重新计算。另外第三章的结构从'时间顺序'改为'按重要程度'排列。" | 反馈 = 定位问题 + 说明原因 + 给出修正方向 |
| 8 | **链式提问** | 一次性在一个 Prompt 中塞入所有需求 | 信息过载导致模型注意力分散，某些要求被"遗忘" | 分 3-5 轮对话：\n轮1：定大纲和整体框架\n轮2-3：逐节展开详细内容\n轮4：整体审视，补充遗漏\n轮5：润色语言和格式 | 每轮模型的注意力聚焦在单一任务上，减少遗漏和跑偏 |

### 优化技巧速查决策树

```
拿到一个不满意的 AI 输出，按以下顺序排查：

1. 任务是否足够具体？
   ├─ 否 → 使用技巧 1（具体化）和技巧 2（结构化）
   └─ 是 → 继续

2. AI 是否理解了你的"好"的标准？
   ├─ 否 → 使用技巧 3（给例子）
   └─ 是 → 继续

3. 输出质量不达标是因为 AI 缺乏专业深度？
   ├─ 是 → 使用技巧 5（定角色）
   └─ 否 → 继续

4. 输出超出了你的约束范围？
   ├─ 是 → 使用技巧 4（设约束）
   └─ 否 → 继续

5. 提醒还是不对？
   ├─ 是 → 使用技巧 7（给反馈）：定位+原因+方向
   └─ 否 → 继续

6. 是否一次性要求太多？
   ├─ 是 → 使用技巧 8（链式提问）
   └─ 否 → 使用技巧 6（迭代），在之前的输出基础上微调
```

---

## 7. 企业视角：Prompt 标准化管理

### 7.1 企业 Prompt 管理的三个层次

```
┌─────────────────────────────────────────────────────────────────────┐
│                    企业 Prompt 标准化成熟度模型                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Level 3: Prompt 资产管理                                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 集中式 Prompt 库（Git 仓库 / 内部平台）                       │   │
│  │ • Prompt 版本控制（变更历史、A/B 测试结果）                     │   │
│  │ • 效果度量（每个 Prompt 模板的准确率、用户满意度、Token 成本）  │   │
│  │ • 跨部门复用（法务/客服/市场共享 Prompt 资产）                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│        ↑                                                             │
│  Level 2: Prompt 标准化                                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 高频场景建立 RCTE 标准模板                                   │   │
│  │ • 新人入职 Prompt 培训（30分钟即可上手）                       │   │
│  │ • 部门级 Prompt 审核流程                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│        ↑                                                             │
│  Level 1: 个人实践                                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 个人学习 Prompt Engineering 技巧                             │   │
│  │ • 在工作中开始使用 AI 工具                                      │   │
│  │ • 积累个人的 Prompt 经验                                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 企业 Prompt 模板库构建路线图

```
第一阶段（1-2周）：识别高频场景
  - 列出全公司 AI 使用场景 Top 10
  - 按"使用频率 × 错误成本"矩阵排序
  - 优先标准化高频率 + 高错误成本的场景

第二阶段（3-4周）：建立标准模板
  - 每个 Top 场景创建 RCTE 标准模板
  - 组织部门代表进行交叉测试
  - 模板存入共享知识库（Notion/语雀/Git仓库）

第三阶段（5-8周）：推广与度量
  - 全员 Prompt 培训（30-60分钟）
  - 建立 Prompt 效果反馈机制
  - 每月审查模板使用数据，持续优化

第四阶段（持续）：资产化管理
  - 引入 A/B 测试（同一任务对比不同 Prompt 效果）
  - 设定每个模板的效果基线指标
  - 将 Prompt 模板的维护纳入部门OKR
```

### 7.3 企业 Prompt 安全红线

```
┌─────────────────────────────────────────────────────────────────┐
│ 企业 Prompt 设计中的安全红线（必须遵守）                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 禁止在 Prompt 中硬编码 API Key / 密码 / 连接串               │
│     正确做法：使用环境变量或密钥管理服务                           │
│                                                                 │
│  2. 禁止在 Prompt 中粘贴完整客户数据                              │
│     正确做法：脱敏处理，或在本地 RAG 管道中检索后注入              │
│                                                                 │
│  3. 涉及法律/财务/医疗建议的 Prompt 必须包含免责声明              │
│     正确做法：在 System Prompt 中固定加入合规声明                  │
│                                                                 │
│  4. 对外服务的 Prompt 必须设置输入和输出的安全过滤               │
│     正确做法：Prompt Injection 检测 + 输出内容审核                 │
│                                                                 │
│  5. Prompt 模板的修改必须有审批流程                               │
│     正确做法：Git PR 审批 + 测试环境验证通过后上线                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.4 ROI 量化参考

| 应用场景 | 优化前指标 | 优化后指标 | 提升幅度 | 投入成本 |
|----------|-----------|-----------|----------|----------|
| 客服自动回复准确率 | 60% | 90%+ | +50% | 仅 Prompt 优化，零技术投入 |
| 内部邮件草稿生成时间 | 15分钟/封 | 2分钟审核/封 | 节省87%时间 | 1小时建立模板 |
| 技术文档撰写效率 | 4小时/篇 | 1小时编辑/篇 | 节省75%时间 | 2小时建立模板 |
| 竞品分析报告初稿 | 3天/份 | 0.5天编辑/份 | 节省83%时间 | 3小时建立模板 |

---

> **关联知识块**：KB6（开发环境搭建）—— 掌握 Prompt Engineering 后，下一步是在 VSCode 中搭建 AI 开发环境，让 Prompt 技能直接转化为编码生产力。

---

# 第六部分：开发环境搭建 —— VSCode + Claude + DeepSeek

---

## 1. 知识块信息表

| 属性 | 内容 |
|------|------|
| **知识块编号** | KB6 |
| **知识块名称** | 开发环境搭建 |
| **所属章节** | 六（VSCode + Claude + DeepSeek 开发环境搭建） |
| **建议时长** | 25 分钟 |
| **前置知识** | KB5（Prompt Engineering 实战详解），已注册至少 2 个 AI 工具账号 |
| **知识类型** | 实操配置 |
| **适用对象** | 零基础学习者 / 企业管理者 / 开发者 |
| **核心能力目标** | 完成 VSCode + Cline + DeepSeek 本地开发环境搭建，能通过 Cline 发送第一个编程 Prompt |
| **硬件要求** | Windows 10+ / macOS 12+ / Linux，4GB+ 内存，2GB+ 可用磁盘空间（不含 AI 模型文件） |

---

## 2. AI 开发环境架构总览

### 2.1 系统架构图

```
═══════════════════════════════════════════════════════════════════════════
                         AI 辅助开发环境 —— 完整架构
═══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                           你的本地机器                                    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      IDE 层（交互界面）                             │  │
│  │                                                                   │  │
│  │   ┌─────────────────────────────────────────────────────────┐    │  │
│  │   │                     VSCode                                │    │  │
│  │   │                                                          │    │  │
│  │   │  ┌───────────┐  ┌───────────┐  ┌──────────────────┐     │    │  │
│  │   │  │  Cline    │  │ Continue  │  │  GitHub Copilot  │     │    │  │
│  │   │  │  (最强)   │  │ (多模型)  │  │  (代码补全)      │     │    │  │
│  │   │  │           │  │           │  │                  │     │    │  │
│  │   │  │ 读写文件  │  │ 对话+补全 │  │  行内自动补全    │     │    │  │
│  │   │  │ 执行终端  │  │ 模型切换  │  │  多语言支持      │     │    │  │
│  │   │  │ 自主Debug │  │ 开源免费  │  │  $10/月          │     │    │  │
│  │   │  └─────┬─────┘  └─────┬─────┘  └────────┬─────────┘     │    │  │
│  │   │        │              │                  │               │    │  │
│  │   └────────┼──────────────┼──────────────────┼───────────────┘    │  │
│  │            │              │                  │                    │  │
│  └────────────┼──────────────┼──────────────────┼────────────────────┘  │
│               │              │                  │                       │
│               │     HTTPS/SSE (MCP 协议可选)     │                       │
│               ▼              ▼                  ▼                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     AI 模型层（推理能力）                           │  │
│  │                                                                   │  │
│  │   ┌─────────────────┐         ┌──────────────────┐                │  │
│  │   │   Claude API     │         │   DeepSeek API    │                │  │
│  │   │                 │         │                  │                │  │
│  │   │  Sonnet 5       │         │  deepseek-chat   │                │  │
│  │   │  · 最强代码能力 │         │  · 中文理解最优  │                │  │
│  │   │  · 长文本推理  │         │  · 极低成本       │                │  │
│  │   │  · 复杂任务    │         │  · 国内直连       │                │  │
│  │   │                │         │  · 新用户免费额度 │                │  │
│  │   │  Opus 5         │         │                  │                │  │
│  │   │  · 最强推理    │         │  deepseek-reasoner│               │  │
│  │   │  · 架构设计    │         │  · 深度推理模式   │                │  │
│  │   │  · 高难度Debug │         │  · 数学/逻辑      │                │  │
│  │   └────────┬────────┘         └────────┬─────────┘                │  │
│  │            │                           │                           │  │
│  └────────────┼───────────────────────────┼───────────────────────────┘  │
│               │                           │                              │
│               └───────────┬───────────────┘                              │
│                           │                                              │
│                           ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     项目层（工作成果）                              │  │
│  │                                                                   │  │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │  │
│  │   │ Python   │  │ MySQL    │  │ 前端     │  │ 文档     │        │  │
│  │   │ 项目     │  │ 数据库   │  │ 项目     │  │ 项目     │        │  │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘        │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
数据流说明：
  1. 用户在 VSCode 中通过 Cline/Continue 插件输入 Prompt
  2. 插件将 Prompt + 项目文件上下文打包为 API 请求
  3. API 请求通过 HTTPS 发送到 Claude API 或 DeepSeek API
  4. AI 模型返回响应（代码/分析/建议）
  5. Cline 可直接将返回的代码写入项目文件，或执行终端命令
═══════════════════════════════════════════════════════════════════════════
```

### 2.2 核心组件职责

| 组件 | 定位 | 核心功能 | 适用阶段 |
|------|------|----------|----------|
| **VSCode** | 代码编辑器/IDE 平台 | 项目管理、代码编辑、终端、调试、插件生态 | 全程 |
| **Cline** | AI 编码 Agent | 对话式编程、文件读写、终端执行、自主 Debug | 开发 + 调试 |
| **Continue** | AI 编程助手 | 对话、代码补全、多模型切换、开源免费 | 开发 + 学习 |
| **GitHub Copilot** | 行内代码补全 | 实时代码建议、多语言支持、上下文感知 | 编写代码 |
| **Python 插件** | 语言支持 | 语法高亮、智能提示、调试、虚拟环境管理 | Python 开发 |
| **Claude API** | AI 推理服务 | 代码生成、长文本处理、复杂推理 | 高复杂度任务 |
| **DeepSeek API** | AI 推理服务 | 中文处理、低成本、高频任务 | 中文任务 + 批量处理 |

### 2.3 Cline 作为 Agent 的技术要点

```
Cline 不是普通的"聊天插件"，它是一个在 IDE 中运行的完整 Agent：

┌──────────────────────────────────────────────────────────┐
│              Cline Agent 架构（简化）                      │
│                                                          │
│  用户输入 Prompt                                          │
│      │                                                   │
│      ▼                                                   │
│  ┌────────────────────────────────────────┐              │
│  │          Cline Agent Loop               │              │
│  │                                         │              │
│  │  ┌─────────────────────────┐           │              │
│  │  │ 1. 分析用户意图          │           │              │
│  │  │    └─ 拆解任务           │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 2. 读取项目上下文        │           │              │
│  │  │    └─ 读取文件树/打开文件│           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 3. 规划执行策略          │           │              │
│  │  │    └─ 判断需要哪些工具   │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 4. 执行动作              │           │              │
│  │  │    ├─ 写入文件           │           │              │
│  │  │    ├─ 执行终端命令       │           │              │
│  │  │    └─ 搜索/替换代码      │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 5. 检查结果              │           │              │
│  │  │    └─ 读取输出/检查错误  │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 6. 迭代（回到步骤2）     │           │              │
│  │  │    直到任务完成          │           │              │
│  │  └─────────────────────────┘           │              │
│  │                                         │              │
│  │  权限模型（四级）：                       │              │
│  │  Allow  ─ 允许（自动执行）               │              │
│  │  Ask    ─ 每次询问用户                   │              │
│  │  Deny   ─ 拒绝（永不执行）               │              │
│  │  AskOnce─ 本次会话仅询问一次              │              │
│  └────────────────────────────────────────┘              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. VSCode 安装指南（Windows / macOS / Linux 三平台）

### 3.1 下载与安装

| 平台 | 安装方式 | 注意事项 |
|------|----------|----------|
| **Windows 10/11** | 1. 浏览器打开 https://code.visualstudio.com <br> 2. 下载 Windows Installer (.exe) <br> 3. 双击运行，勾选以下选项：<br> - "添加到 PATH"（必须勾选）<br> - "将 Code 打开操作添加到文件夹右键菜单"（推荐）<br> - "注册为受支持文件类型的编辑器"（推荐）<br> 4. 完成安装后重启终端 | 如忘记勾选"添加到 PATH"，可手动将 `C:\Users\[用户名]\AppData\Local\Programs\Microsoft VS Code\bin` 添加到系统环境变量 Path 中 |
| **macOS 12+** | 1. 浏览器打开 https://code.visualstudio.com <br> 2. 下载 Mac 版本 (.zip) <br> 3. 解压后将 Visual Studio Code.app 拖入 Applications 文件夹 <br> 4. 打开后按 `Cmd+Shift+P` → 输入 `Shell Command: Install 'code' command in PATH` → 回车 | 此步骤将使 `code` 命令在终端中可用，强烈建议执行 |
| **Linux (Ubuntu/Debian)** | 方法一（图形界面）：<br> 从 https://code.visualstudio.com 下载 .deb 包，双击安装<br><br> 方法二（命令行）：<br> `sudo apt update` <br> `sudo apt install wget gpg` <br> `wget -qO- https://packages.microsoft.com/keys/microsoft.asc \| gpg --dearmor > packages.microsoft.gpg` <br> `sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg` <br> `sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'` <br> `sudo apt update` <br> `sudo apt install code` | 推荐方法二（命令行），可自动处理 GPG 密钥和软件源 |
| **Linux (Fedora/RHEL)** | `sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc` <br> `sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'` <br> `sudo dnf check-update` <br> `sudo dnf install code` | 亦可通过 Flatpak：`flatpak install flathub com.visualstudio.code` |

### 3.2 安装后验证

```bash
# 在终端中执行
code --version
# 预期输出示例：1.97.0 x64

# 测试启动（在目标项目目录中）
cd /path/to/your/project
code .
# 应打开 VSCode 并自动加载当前目录
```

### 3.3 首次配置建议

```
VSCode → 左下角齿轮图标 → Settings → 搜索以下设置项：

┌────────────────────────────────────────────────────────────┐
│ 设置项                          │ 推荐值      │ 原因        │
├─────────────────────────────────┼────────────┼─────────────┤
│ Editor: Font Size               │ 14-16       │ 舒适阅读    │
│ Editor: Tab Size                │ 4           │ Python 标准 │
│ Editor: Render Whitespace       │ boundary    │ 便于发现缩进│
│                                     │ 错误        │
│ Files: Auto Save                │ afterDelay  │ 防止丢失    │
│ Terminal: Integrated Font Size  │ 13-14       │ 终端可读性  │
│ Editor: Minimap                 │ off (可选)  │ 减少干扰    │
└────────────────────────────────────────────────────────────┘
```

---

## 4. 必装插件清单

### 4.1 核心插件详情

| 插件名称 | 插件ID | 用途 | 必装程度 | 免费/付费 | 配置复杂度 |
|----------|--------|------|----------|-----------|-----------|
| **Cline** | `saoudrizwan.claude-dev` | VSCode 中的 AI Agent。可读取项目文件、编写代码、执行终端命令、自主 Debug。支持 Claude/DeepSeek/OpenAI 等多种 API。是目前 VSCode 中最强大的 AI 编码 Agent。 | **必装** | 免费（需自带 API Key） | 中等 |
| **Continue** | `Continue.continue` | 开源 AI 编程助手。支持对话式编程 + 行内补全 + 多模型自由切换。可在同一对话中切换 Claude 和 DeepSeek。最大优势：免费开源，模型切换灵活。 | **必装** | 免费（需自带 API Key） | 低-中 |
| **Python** | `ms-python.python` | Microsoft 官方 Python 语言支持。语法高亮、智能补全、调试器、测试运行器、虚拟环境自动检测。Python 开发的必备基础插件。 | **必装** | 免费 | 最低 |
| **GitHub Copilot** | `GitHub.copilot` | GitHub 官方 AI 代码补全。在编辑器中以灰色文字实时建议下一行代码。支持几乎所有主流编程语言。 | **推荐** | $10/月（学生免费） | 最低 |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | GitHub Copilot 的对话版本，与 Continue 功能重叠。已有 Cline 可跳过。 | **可选** | $10/月 | 最低 |
| **Prettier** | `esbenp.prettier-vscode` | 代码格式化工具，支持 HTML/CSS/JS/JSON/Markdown/YAML 等多种格式。保存时自动格式化。 | **推荐** | 免费 | 最低 |
| **Pylance** | `ms-python.vscode-pylance` | Python 语言服务器，提供更快的智能补全和类型检查。安装 Python 插件时通常自动安装。 | **必装** | 免费 | 无需配置 |

### 4.2 插件安装方式

```
方式一：GUI 安装（推荐）
  VSCode 左侧边栏 → Extensions 图标（或 Ctrl+Shift+X）
  → 搜索框输入插件名称 → 点击 Install

方式二：命令行安装
  code --install-extension saoudrizwan.claude-dev
  code --install-extension Continue.continue
  code --install-extension ms-python.python
  code --install-extension GitHub.copilot
  code --install-extension esbenp.prettier-vscode

方式三：批量安装
  将以下内容保存为 install-extensions.sh：
  #!/bin/bash
  extensions=(
    "saoudrizwan.claude-dev"
    "Continue.continue"
    "ms-python.python"
    "GitHub.copilot"
    "esbenp.prettier-vscode"
  )
  for ext in "${extensions[@]}"; do
    code --install-extension "$ext"
  done
```

---

## 5. Cline 插件配置详解

### 5.1 Cline 全局架构与配置入口

```
Cline 配置入口：
  VSCode 左侧边栏 → Cline 图标（机器人图标）
  → 点击右上角齿轮 ⚙ → 进入 API Provider 配置界面
```

### 5.2 配置 Claude API

**第一步：获取 Anthropic API Key**

```
1. 浏览器打开 https://console.anthropic.com
2. 注册/登录 Anthropic 账号
3. 进入 Dashboard → API Keys → Create Key
4. 输入 Key 名称（如 "cline-vscode"）
5. 复制生成的 sk-ant-api03-xxx... 密钥
   ⚠️ 此密钥仅显示一次，务必安全保存
6. 充值：进入 Billing 页面，绑定信用卡或使用预付费额度
   建议初始充值 $25（约 180 元人民币）
```

**第二步：在 Cline 中配置**

```
VSCode → Cline 面板 → 齿轮图标 → 配置界面：

┌─────────────────────────────────────────────────────┐
│ API Provider:     Anthropic                         │
│                                                     │
│ API Key:          sk-ant-api03-xxxxxxxxxxxxx        │
│                   (粘贴你的 API Key)                 │
│                                                     │
│ Model:            Claude Sonnet 5                    │
│                   (推荐，性价比最优)                   │
│                                                     │
│ Alternative:      Claude Opus 5                      │
│                   (最强推理，复杂任务/架构设计时切换)  │
└─────────────────────────────────────────────────────┘
```

**Claude Model 选择决策矩阵**：

```
┌────────────────────────────────────────────────────────────────────┐
│ 任务类型              │ 推荐 Model          │ 原因                    │
├───────────────────────┼─────────────────────┼─────────────────────────┤
│ 日常代码编写/修改     │ Sonnet 5            │ 速度快、成本适中         │
│ 代码审查/重构         │ Sonnet 5            │ 质量足够，无需 Opus      │
│ 复杂 Debug（多文件）  │ Opus 5              │ 需要最强推理能力         │
│ 系统架构设计          │ Opus 5              │ 需要深度思考             │
│ 简单脚本生成          │ Sonnet 5            │ 速度快、成本低           │
│ 文档撰写/翻译         │ Sonnet 5            │ 性能完全足够             │
│ 批量小任务(>50次/天)  │ Sonnet 5 + DeepSeek │ 控制成本                 │
│ 学习/实验/初期探索    │ Sonnet 5            │ 性价比最佳入门选择       │
└────────────────────────────────────────────────────────────────────┘

价格参考（2026年8月，以 Anthropic 官网为准）：
  - Claude Sonnet 5: ~$3/百万输入 Token, ~$15/百万输出 Token
  - Claude Opus 5:   ~$15/百万输入 Token, ~$75/百万输出 Token
  - 典型编码对话单次消耗: 5K ~ 50K Token
```

### 5.3 配置 DeepSeek API

**第一步：获取 DeepSeek API Key**

```
1. 浏览器打开 https://platform.deepseek.com
2. 注册/登录 DeepSeek 开发者账号（支持中国手机号）
3. 进入 API Keys → 创建新 Key
4. 复制 sk-xxx... 密钥
5. 新用户通常有免费额度（¥10-30 不等）
6. 如需充值：支持支付宝/微信支付
   价格参考：~¥1/百万输入 Token, ~¥2/百万输出 Token
   （约为 Claude Sonnet 价格的 1/30 ~ 1/50）
```

**第二步：在 Cline 中配置**

```
VSCode → Cline 面板 → 齿轮图标 → 配置界面：

┌─────────────────────────────────────────────────────┐
│ API Provider:     OpenAI Compatible                  │
│                                                     │
│ Base URL:         https://api.deepseek.com          │
│                                                     │
│ API Key:          sk-xxxxxxxxxxxxxxxxxxxxxxxx        │
│                   (粘贴你的 DeepSeek API Key)         │
│                                                     │
│ Model ID:         deepseek-chat                      │
│                   (通用对话模型)                      │
│                                                     │
│ Alternative:      deepseek-reasoner                  │
│                   (深度推理模型，数学/逻辑任务)       │
└─────────────────────────────────────────────────────┘
```

**Cline 中 Claude 与 DeepSeek 的配合策略**：

```
┌──────────────────────────────────────────────────────────────┐
│                    双模型切换策略                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Claude (Sonnet/Opus)              DeepSeek                  │
│  适用场景：                       适用场景：                   │
│  • 复杂代码架构设计               • 中文文档/注释生成          │
│  • 多文件重构                     • 简单代码片段              │
│  • 复杂 Bug 追踪                  • 批量重复任务              │
│  • 长文本分析（200K context）     • 成本敏感的大量对话        │
│  • 对代码质量要求极高的场景       • 日常问答和学习辅助        │
│                                                              │
│  切换方式：Cline 齿轮 → 切换 API Provider 即可               │
│  成本对比：Claude Sonnet 成本约为 DeepSeek 的 30~50 倍       │
│                                                              │
│  建议比例：复杂任务 100% Claude | 常规任务 30% Claude +       │
│            70% DeepSeek | 学习探索 10% Claude + 90% DeepSeek  │
└──────────────────────────────────────────────────────────────┘
```

### 5.4 Cline 配置完整步骤总结

```
步骤清单（按顺序执行）：

□ 1. 确认 VSCode 已安装且能正常启动
□ 2. 安装 Cline 插件（VSCode → Extensions → 搜索 "Cline" → Install）
□ 3. 注册 Anthropic 账号，获取 Claude API Key
□ 4. 注册 DeepSeek 开发者账号，获取 DeepSeek API Key
□ 5. 在 Cline 中分别配置 Claude 和 DeepSeek 两个 API Provider
□ 6. 将默认 Provider 设为 Claude（质量优先）或 DeepSeek（成本优先）
□ 7. 发送第一个 Prompt 测试（见第 8 节）
```

---

## 6. Continue 插件配置详解（双模型切换方案）

### 6.1 Continue 定位

Continue 是 VSCode 中最流行的开源 AI 编程助手。与 Cline 的核心区别：

```
┌─────────────────────────────────────────────────────────────────┐
│ 对比维度          │ Cline                    │ Continue           │
├───────────────────┼──────────────────────────┼────────────────────┤
│ 核心定位          │ AI Agent（自主执行任务）  │ AI 助手（对话+补全）│
│ 文件操作          │ 可读/写/搜索项目文件     │ 读当前文件/选区     │
│ 终端操作          │ 可执行终端命令            │ 不可执行终端        │
│ 多模型切换        │ 手动切换 Provider         │ 对话中随时切换      │
│ 代码补全          │ 无                        │ Tab 键补全         │
│ 开源许可          │ Apache 2.0                │ Apache 2.0         │
│ 学习成本          │ 中                        │ 低                 │
│ 适合角色          │ 主力编码 Agent            │ 日常编程助手 +     │
│                   │                           │ 多模型对比使用     │
└─────────────────────────────────────────────────────────────────┘

使用建议：
  Cline (主力) + Continue (辅助) 组合安装，互补而非互斥。
  日常小任务用 Continue 快速问答，大任务用 Cline 自主执行。
```

### 6.2 Continue config.json 完整示例

**配置文件路径**：

```
Windows: %USERPROFILE%\.continue\config.json
macOS:   ~/.continue/config.json
Linux:   ~/.continue/config.json
```

**完整配置**：

```json
{
  "models": [
    {
      "title": "Claude Sonnet 5",
      "provider": "anthropic",
      "model": "claude-sonnet-5-20251001",
      "apiKey": "sk-ant-api03-your-anthropic-key-here",
      "roles": ["chat"]
    },
    {
      "title": "Claude Opus 5",
      "provider": "anthropic",
      "model": "claude-opus-5-20251001",
      "apiKey": "sk-ant-api03-your-anthropic-key-here",
      "roles": ["chat"]
    },
    {
      "title": "DeepSeek V3",
      "provider": "openai",
      "model": "deepseek-chat",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "sk-your-deepseek-key-here",
      "roles": ["chat"]
    },
    {
      "title": "DeepSeek Reasoner",
      "provider": "openai",
      "model": "deepseek-reasoner",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "sk-your-deepseek-key-here",
      "roles": ["chat"]
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek V3",
    "provider": "openai",
    "model": "deepseek-chat",
    "apiBase": "https://api.deepseek.com",
    "apiKey": "sk-your-deepseek-key-here"
  },
  "contextProviders": [
    { "name": "diff" },
    { "name": "file" },
    { "name": "terminal" },
    { "name": "codebase" }
  ],
  "slashCommands": [
    { "name": "edit", "description": "Edit selected code" },
    { "name": "comment", "description": "Write comments for the selected code" },
    { "name": "test", "description": "Generate unit tests" },
    { "name": "fix", "description": "Fix code issues" },
    { "name": "explain", "description": "Explain selected code" }
  ],
  "ui": {
    "showChatScrollbar": true
  },
  "experimental": {
    "defaultContext": 20
  }
}
```

**配置项说明**：

| 配置项 | 说明 |
|--------|------|
| `models[].title` | 在 Continue 界面中显示的名称，可自定义 |
| `models[].provider` | API 提供商类型。`anthropic` 直接使用 Anthropic SDK，`openai` 兼容 OpenAI 格式的 API（DeepSeek 使用此格式） |
| `models[].roles` | `["chat"]` 用于对话，`["autocomplete"]` 用于代码补全，可同时配置两者 |
| `tabAutocompleteModel` | 行内代码补全使用的默认模型。建议用 DeepSeek（成本低、触发频繁） |
| `contextProviders` | 启用的上下文提供者：diff（git差异）、file（当前文件）、terminal（终端输出）、codebase（项目级检索） |
| `slashCommands` | 在对话框中可用的快捷命令，如 `/edit`、`/test`、`/fix` |

### 6.3 Continue 双模型切换操作

```
在 Continue 对话界面中：

1. 对话框底部 → 点击当前模型名称（如 "Claude Sonnet 5"）
2. 从下拉菜单选择目标模型（如 "DeepSeek V3"）
3. 继续对话 —— 新消息将使用切换后的模型

典型切换流程：
  第1轮（Claude）：分析需求、设计架构
  第2轮（切换 DeepSeek）：生成中文注释和文档字符串
  第3轮（切换 Claude）：代码审查和质量把关
```

---

## 7. 备选方案：WorkBuddy + 大模型对比表

### 7.1 什么是 WorkBuddy

WorkBuddy 是一款独立的桌面 AI 工作助手，运行在操作系统层面（非 VSCode 插件），可以操作桌面文件、控制常用应用、执行系统级任务。

### 7.2 方案对比

```
┌───────────────────────────────────────────────────────────────────────┐
│ 对比维度           │ VSCode + Cline/Continue  │ WorkBuddy              │
├────────────────────┼──────────────────────────┼────────────────────────┤
│ 产品形态           │ IDE 插件                  │ 独立桌面应用            │
│ 主要场景           │ 编码、项目开发            │ 通用工作（文件/邮件/   │
│                    │                          │ 日程/网页操作）         │
│ 文件操作范围       │ 项目目录内所有文件        │ 桌面级文件系统访问      │
│ 终端/Shell 访问     │ 可在 VSCode 终端执行命令  │ 系统级命令执行          │
│ 模型支持           │ Claude / DeepSeek /      │ 多模型 API 接入         │
│                    │ OpenAI / Gemini / 本地   │                        │
│ 安装门槛           │ 低（插件一键安装）        │ 中（独立安装 + 配置）   │
│ 适用人群           │ 需要写代码的开发者        │ 需要通用 AI 助手的       │
│                    │ 和需要理解代码的管理者    │ 非开发者/管理者         │
│ 价格               │ 免费（仅 API 费用）       │ 免费（仅 API 费用）     │
│ 中文支持           │ 良好                     │ 良好                   │
│ 学习曲线           │ 1-2 天                   │ 0.5-1 天               │
│ 编码能力           │ 极强（项目上下文感知）    │ 一般（无项目级上下文）  │
└───────────────────────────────────────────────────────────────────────┘
```

### 7.3 WorkBuddy 配置步骤（作为备选方案）

```
1. 浏览器打开 https://workbuddy.ai
2. 下载对应系统的桌面应用安装包
3. 安装后启动 → 进入 Settings → API Configuration
4. 填入 API 信息：
   - DeepSeek API Key（推荐，国内可用，低成本）
   - 或 Claude API Key
5. 选择默认模型
6. 配置权限：WorkBuddy 需要授予屏幕录制/辅助功能等系统权限
   （macOS: System Preferences → Privacy & Security → Accessibility）

适用场景示例：
  - "帮我整理桌面上的文件，按项目分类到不同文件夹"
  - "读取当前网页内容，总结为3个要点"
  - "帮我回复这封邮件，语气专业但友好"
  - "搜索本地文档中所有提到'Q3预算'的文件"
```

### 7.4 方案选择决策树

```
你主要需要写代码吗？
├─ 是 → VS Code + Cline（主力）+ Continue（辅助）
│         └─ 需要额外的通用桌面助手？
│              ├─ 是 → 加装 WorkBuddy
│              └─ 否 → 当前方案已足够
│
└─ 否 → 你的主要工作场景是？
         ├─ 文档/邮件/文件管理 → WorkBuddy + 网页版 ChatGPT/Claude
         ├─ 数据分析/Python脚本 → VSCode + Cline（学一点基础）
         └─ 纯粹的知识问答/学习 → 网页版 AI 工具即可
```

---

## 8. 环境验证：发送第一个编程 Prompt 测试

### 8.1 测试步骤

```
步骤 1: 创建测试文件
  在 VSCode 中新建文件 → 保存为 test_ai.py

步骤 2: 打开 Cline 对话面板
  点击左侧 Cline 图标

步骤 3: 在 Cline 对话框中输入以下 Prompt：

═══════════════════════════════════════════════════════════
请用 Python 写一个简单的函数，功能是：

输入：一个数字列表（可能包含整数和浮点数）
输出：平均值和中位数（返回一个字典）

要求：
1. 代码使用中文注释，说明每一步在做什么
2. 处理空列表的边界情况（返回 None）
3. 包含一个 if __name__ == '__main__' 测试块，
   用至少 3 组不同的测试数据验证函数正确性
4. 遵循 PEP 8 代码风格规范
═══════════════════════════════════════════════════════════

步骤 4: 观察 Cline 的行为
  - Cline 会自动读取 test_ai.py
  - Cline 会生成代码并写入文件（或展示代码供你确认）
  - 如果 Cline 请求权限（写入文件/执行终端），点击 Allow 或确认

步骤 5: 让 Cline 执行代码

  继续在 Cline 对话框中输入：

  帮我在终端中运行这段代码，看看输出是否正确。

  Cline 将自动执行 python test_ai.py 并展示终端输出。

步骤 6: 验证结果
  检查终端输出中的平均值和中位数是否计算正确。
```

### 8.2 测试成功的标志

```
✅ Cline 成功生成了符合要求的 Python 代码
✅ 代码包含中文注释
✅ 代码处理了空列表的边界情况
✅ 代码包含测试块
✅ Cline 成功在终端中执行了代码
✅ 终端输出了正确的计算结果

如果以上全部通过 → 环境配置成功！
```

### 8.3 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Cline 提示 API Key 无效 | Key 复制有误或已过期 | 重新生成 Key 并复制（确认无多余空格） |
| Cline 提示余额不足 | API 账户未充值/额度用完 | 登录对应平台充值或检查剩余额度 |
| Cline 无法写入文件 | 文件权限设置过于严格 | 在 Cline 权限设置中开启 Write 权限 |
| Python 执行报错 "No module named python" | Python 未添加至 PATH | `python --version` 验证，如无则重新安装 Python 并勾选 "Add to PATH" |
| DeepSeek API 连接超时 | 网络问题（国内访问） | 检查网络，或切换到手机热点测试 |
| Cline 响应很慢 | 模型负载高峰或网络延迟 | 等待或切换到 DeepSeek（国内响应更快） |

### 8.4 进阶测试（环境确认后可选）

```
测试 1: 多文件操作
  Prompt: "在当前目录下创建一个 utils 文件夹，在 utils 里新建 math_helpers.py，
          将刚才的统计函数移到这个文件中，然后在 test_ai.py 中导入并使用它。"

测试 2: Debug 能力
  Prompt: "在 test_ai.py 中故意写一个会导致除零错误的代码，
          然后让 Cline 找出并修复这个 Bug。"

测试 3: 数据库连接（如已安装 MySQL）
  Prompt: "帮我写一个 Python 脚本，连接到本地 MySQL 数据库，
          执行一条简单的查询，并打印结果。"
```

---

## 9. 企业视角：团队 AI 开发环境标准化建议

### 9.1 企业级 AI 开发环境成熟度模型

```
┌───────────────────────────────────────────────────────────────────┐
│               团队 AI 开发环境标准化成熟度                          │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Level 3: 企业级管理                                              │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 统一 API Key 管理（密钥轮换、用量监控、预算告警）         │   │
│  │ • 代码审查集成（AI 生成代码必须经过 Code Review）           │   │
│  │ • 内部 Prompt 库（团队共享的 RCTE 模板）                    │   │
│  │ • 安全策略（禁止向 AI 发送的敏感信息清单）                  │   │
│  │ • 用量分析（按团队/项目/人员维度的 API 用量报告）           │   │
│  └───────────────────────────────────────────────────────────┘   │
│        ↑                                                          │
│  Level 2: 团队标准化                                              │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 统一开发环境配置（VSCode + 指定插件清单）                 │   │
│  │ • 统一 AI 工具选型（主力模型 + 备份模型）                   │   │
│  │ • 新人入职 30 分钟上手（一键配置脚本）                      │   │
│  │ • 团队共享的 .vscode/settings.json 和插件推荐文件           │   │
│  └───────────────────────────────────────────────────────────┘   │
│        ↑                                                          │
│  Level 1: 个人使用                                                │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 各成员自行安装使用                                         │   │
│  │ • 无统一配置标准                                             │   │
│  │ • API Key 个人管理                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 9.2 团队标准化实践方案

**方案一：配置文件标准化**

```
在项目 Git 仓库中维护以下文件：

1. .vscode/extensions.json
{
  "recommendations": [
    "saoudrizwan.claude-dev",
    "Continue.continue",
    "ms-python.python",
    "esbenp.prettier-vscode"
  ],
  "unwantedRecommendations": []
}

2. .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "cline.preferredLanguage": "Chinese"
}

3. .claude/settings.json（Claude Code 配置，如使用）
{
  "permissions": {
    "allow": [
      "Bash(python:*)",
      "Bash(pip:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)",
      "Bash(drop:*)",
      "Bash(truncate:*)"
    ]
  }
}
```

**方案二：一键配置脚本**

```bash
#!/bin/bash
# setup-ai-env.sh —— 团队新成员的 AI 开发环境一键配置脚本

echo "===== AI 开发环境配置脚本 ====="

# 1. 检查 VSCode
if ! command -v code &> /dev/null; then
    echo "❌ VSCode 未安装，请先安装：https://code.visualstudio.com"
    exit 1
fi
echo "✅ VSCode 已安装"

# 2. 安装核心插件
echo "📦 安装核心插件..."
code --install-extension saoudrizwan.claude-dev
code --install-extension Continue.continue
code --install-extension ms-python.python
code --install-extension esbenp.prettier-vscode
echo "✅ 插件安装完成"

# 3. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 未安装，建议安装 Python 3.9+"
else
    echo "✅ Python $(python3 --version) 已安装"
fi

# 4. 创建推荐的 VSCode 配置（如果项目中不存在）
if [ ! -d ".vscode" ]; then
    mkdir -p .vscode
fi

cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "saoudrizwan.claude-dev",
    "Continue.continue",
    "ms-python.python",
    "esbenp.prettier-vscode"
  ]
}
EOF

echo ""
echo "===== 环境配置完成 ====="
echo ""
echo "下一步："
echo "1. 配置 Cline API Key（VSCode → Cline 面板 → 齿轮设置）"
echo "2. 确保 API 账户有余额"
echo "3. 发送第一个 Prompt 测试（参考团队文档）"
echo ""
echo "需要帮助请联系：[团队技术负责人]"
```

### 9.3 企业安全与成本管理建议

```
═══════════════════════════════════════════════════════════════════════
                      企业 AI 开发环境安全清单
═══════════════════════════════════════════════════════════════════════

API Key 管理：
  □ 使用企业级密钥管理服务（AWS Secrets Manager / HashiCorp Vault）
  □ 禁止将 API Key 硬编码在项目代码中
  □ 禁止将 API Key 提交到 Git 仓库
  □ 定期轮换 API Key（建议 90 天）
  □ 按团队/项目分配合不同的 API Key（便于成本追踪和问题隔离）

数据安全：
  □ 禁止向 AI 发送生产环境的真实客户 PII（个人身份信息）
  □ 建立敏感数据脱敏标准（正则替换 + 命名映射）
  □ 禁止向 AI 发送公司核心商业机密（算法、定价策略、
    未公开财务数据）
  □ 生产代码 Review 必须由人工完成，AI 只能作为辅助建议
  □ 所有 AI 生成的 SQL 在人工审核前不得对生产数据库执行

成本管理：
  □ 设置 API 用量告警（每日/每周预算上限）
  □ 区分任务级别的模型使用策略（见下方成本控制矩阵）
  □ 月度 AI API 费用纳入项目成本核算
  □ 鼓励高频简单任务使用 DeepSeek（成本约为 Claude 的 1/30-1/50）

成本控制矩阵：
┌─────────────────────┬──────────────┬────────────┬──────────┐
│ 任务类型             │ 推荐模型      │ 预估成本   │ 频率      │
├─────────────────────┼──────────────┼────────────┼──────────┤
│ 核心架构设计         │ Opus 5       │ ~$0.50/次  │ 2-5次/周  │
│ 日常编码/CR          │ Sonnet 5     │ ~$0.10/次  │ 20-50次/天│
│ 文档注释/简单脚本    │ DeepSeek     │ ~$0.01/次  │ 无限制    │
│ 自动补全触发         │ DeepSeek     │ ~$0.001/次 │ 数百次/天 │
│ 代码审查             │ Sonnet 5     │ ~$0.05/次  │ 10次/天   │
└─────────────────────┴──────────────┴────────────┴──────────┘
  预估月均成本（5人团队）：$150 ~ $400（含合理配置）
═══════════════════════════════════════════════════════════════════════
```

### 9.4 团队推广路线图

```
第 1 周：试点
  - 选择 2-3 名技术骨干先行试用
  - 完成 VSCode + Cline + DeepSeek 配置
  - 收集初始使用反馈和典型场景

第 2-3 周：标准化
  - 基于试点反馈编写团队 AI 开发环境标准文档
  - 打磨一键配置脚本和推荐插件清单
  - 建立内部 Prompt 模板库初稿（10个高频场景）

第 4 周：推广
  - 组织 60 分钟团队 Workshop（30 分钟讲解 + 30 分钟实操）
  - 全员完成环境配置
  - 建立 Slack/飞书 AI 使用技巧分享频道

第 5-8 周：深化
  - 每周收集匿名使用反馈，迭代标准文档
  - 按任务类型统计 AI 使用率和采纳率
  - 每月分享一个"最佳 AI Prompt"案例

持续：
  - 关注 Cline/Continue 等工具版本更新
  - 关注模型新版本发布（性能提升 / 价格下降）
  - 每季度举办一次 AI 使用技巧分享会
```

---

> **关联知识块**：KB5（Prompt Engineering 实战详解） — 环境搭建完成后，结合 RCTE 框架和 8 大 Prompt 技巧，在 Cline 中开始系统化的 AI 辅助编程实践。
>
> **下一知识点**：完成 KB5 + KB6 后，进入实操环节 —— 基于 Prompt Engineering 安全操作 MySQL 数据库（本课第七节）。

---

# 第七部分：MySQL 数据库操作实操

---

## 知识块信息表

| 字段 | 内容 |
|------|------|
| **知识块编号** | KB7 |
| **知识块名称** | MySQL 数据库操作实操 |
| **所属课程** | AI 时代能力培养 / 第1周 / 第2课 |
| **所属章节** | 七、第四部分：实操 —— 基于 Prompt Engineering 操作 MySQL 数据库 |
| **建议时长** | 35 分钟 |
| **难度等级** | 中级（需要 Python + MySQL 基础环境） |
| **前置知识** | KB1-KB6（五层体系 + RCTE + 环境搭建） |
| **核心产出** | (1) 理解 Prompt Engineering 在实际开发中的威力 (2) 掌握数据库权限隔离的安全最佳实践 (3) 能独立运行并扩展 AI 数据库操作 Agent |

---

## 1. 实操架构图

```
┌──────────────┐     自然语言 Prompt       ┌──────────────┐     生成的 SQL       ┌──────────────┐
│   用户 (You)  │ ────────────────────────→ │   AI 模型     │ ──────────────────→ │  MySQL 数据库 │
│  写 Prompt    │ ←──────────────────────── │ (Claude/      │ ←────────────────── │              │
│              │     结果解读 + SQL 说明     │  DeepSeek)   │    查询结果数据       │              │
└──────────────┘                           └──────────────┘                     └──────┬───────┘
                                                                                       │
                                                                        ┌──────────────┘
                                                                        │
                                                            ┌───────────┴───────────┐
                                                            │     权限隔离设计        │
                                                            │                        │
                                                            │  ┌─────────────────┐   │
                                                            │  │  ai_readonly     │   │  → 只读账户，仅 SELECT
                                                            │  │  (日常查询用)     │   │    最安全，默认使用
                                                            │  └─────────────────┘   │
                                                            │  ┌─────────────────┐   │
                                                            │  │  ai_writer       │   │  → 写入账户，可 INSERT /
                                                            │  │  (确认后使用)     │   │    UPDATE / DELETE
                                                            │  └─────────────────┘   │
                                                            │  ┌─────────────────┐   │
                                                            │  │  root            │   │  → 管理员账户
                                                            │  │  (仅DBA持有)      │   │    绝不交给 AI
                                                            │  └─────────────────┘   │
                                                            └────────────────────────┘
```

**数据流说明**：

1. 用户用自然语言描述查询/操作需求
2. AI 模型根据 System Prompt（含数据库结构、安全规则、输出格式约束）生成 SQL
3. SQL 经用户确认后，由 Agent 根据操作类型（读/写）自动选择对应权限的 MySQL 账户执行
4. 查询结果返回给 AI 模型做自然语言解读，或直接展示给用户

---

## 2. MySQL 安装指南

### 2.1 Windows

```
1. 浏览器打开 https://dev.mysql.com/downloads/installer/
2. 下载 mysql-installer-community-8.0.x.msi
3. 双击安装，选择 "Developer Default" 安装类型
4. 设置 root 密码（务必记住）
5. 安装过程中勾选 "MySQL Workbench"（图形化管理工具，可选）
6. 完成后在开始菜单搜索 "MySQL Command Line Client" 验证：
     输入安装时设置的 root 密码
     执行 SELECT VERSION(); 应显示 8.0.x
```

### 2.2 macOS

```bash
# 使用 Homebrew 安装
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 安全初始化（设置 root 密码）
mysql_secure_installation

# 验证安装
mysql -u root -p -e "SELECT VERSION();"
```

### 2.3 Linux (Ubuntu/Debian)

```bash
# 安装 MySQL Server
sudo apt update
sudo apt install mysql-server -y

# 安全初始化
sudo mysql_secure_installation

# 验证安装
sudo mysql -e "SELECT VERSION();"

# 设置 root 密码（若安装时未设置）
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword123!';
FLUSH PRIVILEGES;
EXIT;
```

### 2.4 验证 MySQL 命令行可用

```bash
# 确认 mysql 命令在 PATH 中
mysql --version
# 预期输出：mysql  Ver 8.0.x ...

# 测试连接
mysql -u root -p
# 输入密码后应进入 MySQL 交互界面：mysql>
```

---

## 3. Python MySQL 驱动安装

```bash
# 推荐：官方 MySQL Connector（纯 Python，无额外依赖）
pip install mysql-connector-python

# 验证安装
python -c "import mysql.connector; print(mysql.connector.__version__)"
```

**备选驱动**（特殊场景使用）：

| 驱动 | 安装命令 | 特点 |
|------|----------|------|
| mysql-connector-python | `pip install mysql-connector-python` | 官方出品，纯 Python，零依赖，首选 |
| PyMySQL | `pip install pymysql` | 轻量第三方库，兼容性好 |
| mysqlclient | `pip install mysqlclient` | C 扩展，性能最高，需编译环境 |

---

## 4. 创建测试数据库（完整 SQL 脚本）

以下脚本以 root 身份在 MySQL 中逐段执行。

### 4.1 创建数据库

```sql
-- 以 root 身份登录 MySQL
-- mysql -u root -p

-- 创建测试数据库
CREATE DATABASE ai_test_company
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 查看数据库是否创建成功
SHOW DATABASES LIKE 'ai_test_company';

-- 切换到测试数据库
USE ai_test_company;
```

### 4.2 创建 employees 表

```sql
CREATE TABLE employees (
    id                INT AUTO_INCREMENT PRIMARY KEY COMMENT '员工编号，自增主键',
    name              VARCHAR(100)  NOT NULL         COMMENT '员工姓名',
    department        VARCHAR(50)                    COMMENT '所属部门',
    salary            DECIMAL(10, 2)                 COMMENT '月薪（元）',
    hire_date         DATE                           COMMENT '入职日期',
    performance_score INT DEFAULT 0                  COMMENT '绩效评分，范围 0-100',
    INDEX idx_department (department),
    INDEX idx_hire_date (hire_date),
    INDEX idx_performance (performance_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='员工信息表 —— AI 数据库操作测试用';

-- 验证表结构
DESC employees;
```

字段说明对照：

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| id | INT | AUTO_INCREMENT, PRIMARY KEY | 员工编号，自增主键 |
| name | VARCHAR(100) | NOT NULL | 员工姓名 |
| department | VARCHAR(50) | - | 所属部门 |
| salary | DECIMAL(10,2) | - | 月薪（元） |
| hire_date | DATE | - | 入职日期 |
| performance_score | INT | DEFAULT 0 | 绩效评分，范围 0-100 |

### 4.3 插入测试数据（8 条）

```sql
INSERT INTO employees (name, department, salary, hire_date, performance_score) VALUES
('张三', '技术部', 25000.00, '2023-03-15', 92),
('李四', '市场部', 18000.00, '2022-07-01', 85),
('王五', '技术部', 28000.00, '2021-01-10', 95),
('赵六', '人事部', 15000.00, '2024-01-20', 78),
('钱七', '市场部', 20000.00, '2023-09-05', 88),
('孙八', '技术部', 32000.00, '2020-06-15', 97),
('周九', '财务部', 22000.00, '2022-11-01', 82),
('吴十', '技术部', 26000.00, '2023-12-01', 91);

-- 验证数据：应返回 8
SELECT COUNT(*) AS total_employees FROM employees;
```

数据概览：

| id | name | department | salary | hire_date | performance_score |
|----|------|-----------|--------|-----------|-------------------|
| 1 | 张三 | 技术部 | 25000 | 2023-03-15 | 92 |
| 2 | 李四 | 市场部 | 18000 | 2022-07-01 | 85 |
| 3 | 王五 | 技术部 | 28000 | 2021-01-10 | 95 |
| 4 | 赵六 | 人事部 | 15000 | 2024-01-20 | 78 |
| 5 | 钱七 | 市场部 | 20000 | 2023-09-05 | 88 |
| 6 | 孙八 | 技术部 | 32000 | 2020-06-15 | 97 |
| 7 | 周九 | 财务部 | 22000 | 2022-11-01 | 82 |
| 8 | 吴十 | 技术部 | 26000 | 2023-12-01 | 91 |

---

## 5. 权限隔离设计（核心安全章节）

### 5.1 设计理念

AI 生成 SQL 的准确率不是 100%。权限隔离是在 AI 犯错时的最后一道防线——即使 AI 生成了危险的 SQL，MySQL 的账户权限体系也会阻止其执行。

核心原则：**最小权限原则（Principle of Least Privilege）**——每个账户只拥有完成任务所需的最小权限集。

### 5.2 三层账户体系

```
                        ┌──────────────────────────────────┐
                        │          root (DBA 持有)          │
                        │  权限: ALL PRIVILEGES             │
                        │  使用: 安装、备份、账户管理        │
                        │  AI 访问: ❌ 绝对禁止              │
                        ├──────────────────────────────────┤
                        │        ai_writer (可控写入)        │
                        │  权限: SELECT, INSERT, UPDATE,    │
                        │         DELETE                    │
                        │  使用: 人工确认后的数据修改        │
                        │  AI 访问: ⚠️ 需人工二次确认       │
                        ├──────────────────────────────────┤
                        │      ai_readonly (默认只读)        │
                        │  权限: SELECT only                │
                        │  使用: 日常查询、数据分析          │
                        │  AI 访问: ✅ 可自动使用            │
                        └──────────────────────────────────┘
```

### 5.3 完整 GRANT SQL 脚本

```sql
-- ============================================
-- 权限隔离配置 - 在 root 账户下执行
-- ============================================

-- 1. 创建只读账户（日常 AI 查询默认账户）
CREATE USER 'ai_readonly'@'localhost'
    IDENTIFIED BY 'ReadOnly123!';

GRANT SELECT ON ai_test_company.*
    TO 'ai_readonly'@'localhost';

-- 验证只读账户权限
SHOW GRANTS FOR 'ai_readonly'@'localhost';
-- 预期输出: GRANT SELECT ON `ai_test_company`.* TO `ai_readonly`@`localhost`


-- 2. 创建写入账户（需人工确认后才能使用）
CREATE USER 'ai_writer'@'localhost'
    IDENTIFIED BY 'Writer456!';

GRANT SELECT, INSERT, UPDATE, DELETE ON ai_test_company.*
    TO 'ai_writer'@'localhost';

-- 验证写入账户权限
SHOW GRANTS FOR 'ai_writer'@'localhost';
-- 预期输出: GRANT SELECT, INSERT, UPDATE, DELETE ON `ai_test_company`.* ...


-- 3. 确认 root 绝不创建给 AI
-- root 账户仅 DBA 持有，密码复杂度要求高
-- 任何自动化系统、AI Agent 均不应获得 root 凭据


-- 4. 刷新权限使其立即生效
FLUSH PRIVILEGES;
```

### 5.4 权限验证方法

```sql
-- 方法一：查看各账户授权
SELECT user, host FROM mysql.user WHERE user LIKE 'ai_%';

-- 方法二：以 ai_readonly 登录，尝试写入（应被拒绝）
-- mysql -u ai_readonly -p'ReadOnly123!' ai_test_company
-- 执行以下语句，预期报错: INSERT command denied
-- INSERT INTO employees (name) VALUES ('测试员工');

-- 方法三：以 ai_writer 登录，尝试 DROP（应被拒绝）
-- mysql -u ai_writer -p'Writer456!' ai_test_company
-- 执行以下语句，预期报错: DROP command denied
-- DROP TABLE employees;
```

### 5.5 权限矩阵速查表

| 操作 | ai_readonly | ai_writer | root |
|------|:----------:|:---------:|:----:|
| SELECT（查询） | ✅ | ✅ | ✅ |
| INSERT（插入） | ❌ | ✅ | ✅ |
| UPDATE（更新） | ❌ | ✅ | ✅ |
| DELETE（删除） | ❌ | ✅ | ✅ |
| CREATE TABLE | ❌ | ❌ | ✅ |
| ALTER TABLE | ❌ | ❌ | ✅ |
| DROP TABLE | ❌ | ❌ | ✅ |
| TRUNCATE | ❌ | ❌ | ✅ |
| GRANT（授权） | ❌ | ❌ | ✅ |
| CREATE USER | ❌ | ❌ | ✅ |

---

## 6. AI 数据库操作 Agent 完整代码

### 6.1 文件概述

| 项目 | 说明 |
|------|------|
| **文件名** | `ai_db_agent.py` |
| **Python 版本** | 3.9+ |
| **依赖** | `pip install mysql-connector-python openai` |
| **LLM 后端** | DeepSeek（国内直连低成本）/ 可替换为 Claude API |
| **核心逻辑** | System Prompt 约束 → AI 生成 SQL → 正则提取 → 权限选择 → 执行 |

### 6.2 完整源代码

```python
#!/usr/bin/env python3
"""
=============================================================================
 AI 数据库操作 Agent
 基于 Prompt Engineering + MySQL 权限隔离，安全地让 AI 操作企业数据库
=============================================================================

核心设计思路:
  1. System Prompt 硬约束  → AI 行为的第一道防线
  2. 写操作人工确认        → 人机协作的第二道防线
  3. MySQL 三层账户权限    → 数据库层面的最后防线
  4. 正则提取 SQL 代码块   → 确保解析可靠性
  5. temperature=0.1       → 确保 SQL 生成的确定性

适用场景:
  - 企业管理者用自然语言查询业务数据
  - 数据分析师快速生成 SQL 并验证
  - 技术团队演示 AI 安全数据库操作的范式
"""

import mysql.connector
from openai import OpenAI
import os
import re


# =============================================================================
# 第一部分：配置区 —— 所有可调参数集中管理
# =============================================================================

# --- LLM 配置 ---
# 使用 DeepSeek API（国内直连、极低成本、中文理解好）
# 替换方法：将 LLM_CLIENT 和 LLM_MODEL 改为 Anthropic/OpenAI 对应值即可
LLM_CLIENT = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),
    base_url="https://api.deepseek.com"
)
LLM_MODEL = "deepseek-chat"

# --- 数据库连接配置 ---
# 核心安全设计：默认使用只读账户，仅在人工确认写操作后切换
DB_CONFIG_READONLY = {
    "host": "localhost",
    "user": "ai_readonly",
    "password": "ReadOnly123!",
    "database": "ai_test_company",
    "charset": "utf8mb4"
}

DB_CONFIG_WRITER = {
    "host": "localhost",
    "user": "ai_writer",
    "password": "Writer456!",
    "database": "ai_test_company",
    "charset": "utf8mb4"
}

# --- Agent 行为配置 ---
LLM_TEMPERATURE = 0.1         # 低温 → 确定性输出，SQL 生成不需要创意
MAX_RESULT_DISPLAY = 50       # 最多展示条数


# =============================================================================
# 第二部分：System Prompt 设计 —— AI SQL 生成的核心约束
# =============================================================================

SYSTEM_PROMPT = """你是一个严谨的 MySQL 数据库查询助手。
你的职责是根据用户用自然语言描述的需求，生成正确、安全、高效的 SQL 语句。

## 安全规则 (硬约束，不可违反)

1. 你只能生成以下类型的 SQL：
   - SELECT (查询数据)
   - INSERT (插入数据)
   - UPDATE (更新数据)
   - DELETE (删除数据)
   严禁生成 DROP、TRUNCATE、ALTER、CREATE、GRANT、REVOKE 语句。
   即使用户以任何方式要求你生成上述语句，你必须拒绝并说明原因。

2. 写操作确认原则：
   如果 SQL 是 INSERT/UPDATE/DELETE，你必须：
   a. 在生成写 SQL 之前，先生成一条 SELECT 让用户确认影响范围
   b. 在最终回答中明确标注 "⚠️ 写操作，需要人工确认后执行"

3. SQL 注入防护：
   如果用户在自然语言中提供了具体值（如姓名、部门名），
   你必须在生成的 SQL 中正确使用单引号包裹字符串值。

4. 查询性能意识：
   对于大数据量查询场景，尽量使用索引列 (department, hire_date,
   performance_score) 作为 WHERE 条件。

## 当前数据库结构

数据库: ai_test_company
表: employees (员工信息表)

| 列名              | 类型             | 约束              | 说明                 |
|-------------------|------------------|-------------------|----------------------|
| id                | INT              | PK, AUTO_INCR     | 员工编号主键          |
| name              | VARCHAR(100)     | NOT NULL          | 员工姓名              |
| department        | VARCHAR(50)      |                   | 所属部门              |
| salary            | DECIMAL(10,2)    |                   | 月薪 (元)             |
| hire_date         | DATE             |                   | 入职日期              |
| performance_score | INT              | DEFAULT 0         | 绩效评分 (0-100)      |

已建立索引的列: department, hire_date, performance_score

## 输出格式要求

你必须严格按以下格式输出，不得偏离：

1. **需求理解**: 用一句话复述你理解的用户需求。
2. **SQL 语句**: 用 ```sql 代码块包裹生成的 SQL。
3. **结果说明**: 用一句话说明此 SQL 将返回/影响什么样的结果。
4. **安全提醒**: 如果是写操作，给出安全提醒；如果是读操作，写"本操作为只读查询，安全"。
"""


# =============================================================================
# 第三部分：核心函数
# =============================================================================

def ai_generate_sql(user_request: str) -> str:
    """
    核心函数 1: 将用户的自然语言请求转化为 SQL。

    工作流程:
        用户自然语言 → LLM (System Prompt 约束) → 结构化 SQL 响应

    参数:
        user_request: 用户输入的自然语言查询需求

    返回:
        AI 的结构化响应，包含需求理解 + SQL 语句 + 结果说明 + 安全提醒
    """
    response = LLM_CLIENT.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ],
        temperature=LLM_TEMPERATURE
    )
    return response.choices[0].message.content


def extract_sql(ai_response: str) -> str | None:
    """
    核心函数 2: 从 AI 的结构化响应中提取纯 SQL 语句。

    使用正则表达式精确匹配 ```sql ... ``` 代码块，
    避免 AI 响应中的自然语言文本污染 SQL。

    参数:
        ai_response: ai_generate_sql() 的返回结果

    返回:
        提取到的纯 SQL 字符串；如果未匹配到则返回 None
    """
    pattern = r'```sql\s*\n?(.*?)\n?\s*```'
    match = re.search(pattern, ai_response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def is_write_operation(sql: str) -> bool:
    """
    核心函数 3: 判断 SQL 是否为写操作。

    检查 SQL 语句的前缀关键字，确定是否需要切换到写入账户。

    参数:
        sql: 待判断的 SQL 语句

    返回:
        True 表示写操作（需切换 ai_writer + 人工确认）
        False 表示读操作（可使用 ai_readonly）
    """
    sql_upper = sql.strip().upper()
    write_keywords = ("INSERT", "UPDATE", "DELETE")
    return any(sql_upper.startswith(kw) for kw in write_keywords)


def execute_sql(sql: str, use_writer: bool = False) -> dict | list:
    """
    核心函数 4: 执行 SQL 并返回结果。

    权限隔离的关键实现点:
    - use_writer=False → 使用 ai_readonly 账户（默认）
    - use_writer=True  → 使用 ai_writer 账户（仅写操作）

    参数:
        sql: 待执行的 SQL 语句
        use_writer: 是否使用写入账户

    返回:
        SELECT: 返回 list[dict]，每条记录为一个字典
        写操作: 返回 dict，包含 affected_rows 和 status
        异常:   返回 dict，包含 error 信息
    """
    config = DB_CONFIG_WRITER if use_writer else DB_CONFIG_READONLY

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)

        # SELECT 语句 → 返回查询结果列表
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results

        # 非 SELECT → 提交事务并返回影响行数
        else:
            conn.commit()
            return {
                "affected_rows": cursor.rowcount,
                "status": "success"
            }

    except mysql.connector.Error as e:
        return {
            "error": f"[MySQL Error {e.errno}] {e.msg}",
            "sql_state": e.sqlstate if hasattr(e, 'sqlstate') else None
        }
    except Exception as e:
        return {"error": f"[Unexpected Error] {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def format_query_result(results: list, max_display: int = MAX_RESULT_DISPLAY) -> str:
    """
    核心函数 5: 格式化查询结果为可读字符串。

    参数:
        results: execute_sql() 返回的查询结果列表
        max_display: 最大显示条数

    返回:
        格式化后的字符串
    """
    if not results:
        return "（无匹配记录）"

    lines = []
    for i, row in enumerate(results[:max_display], 1):
        lines.append(f"  [{i}] {row}")

    if len(results) > max_display:
        lines.append(f"  ... 以及另外 {len(results) - max_display} 条记录")

    return "\n".join(lines)


# =============================================================================
# 第四部分：主交互循环
# =============================================================================

def main():
    """AI 数据库操作助手的主交互入口。"""

    # --- 启动横幅 ---
    print("=" * 60)
    print("  AI 数据库操作助手")
    print("  核心机制: Prompt Engineering + MySQL 权限隔离")
    print("=" * 60)
    print()
    print("  数据库: ai_test_company.employees")
    print("  默认账户: ai_readonly (只读)")
    print("  数据量: 8 条员工记录 (4个部门)")
    print()
    print("  示例查询:")
    print("    - 技术部有哪些员工？按薪资从高到低排列")
    print("    - 列出绩效评分高于90的员工姓名和部门")
    print("    - 按部门统计员工人数和平均薪资")
    print("    - 市场部最近入职的员工是谁？")
    print("    - 各部门薪资最高的员工分别是谁？")
    print()
    print("  输入 'quit' 退出")
    print("-" * 60)

    # --- 交互循环 ---
    while True:
        # Step 1: 获取用户输入
        user_input = input("\n查询 > ").strip()

        if user_input.lower() == "quit":
            print("会话结束。数据库连接已关闭。")
            break
        if not user_input:
            continue

        # Step 2: AI 生成 SQL
        print("\n[1/4] AI 正在分析需求并生成 SQL ...")
        ai_response = ai_generate_sql(user_input)
        print(f"\n{ai_response}")

        # Step 3: 提取 SQL
        print("\n[2/4] 提取 SQL 语句 ...")
        sql = extract_sql(ai_response)
        if not sql:
            print("未能从 AI 响应中提取有效 SQL。请重新描述你的需求。")
            continue
        print(f"SQL: {sql}")

        # Step 4: 判断操作类型 + 写操作人工确认
        write_op = is_write_operation(sql)

        if write_op:
            print(f"\n[3/4] 检测到写操作，需要人工确认")
            confirm = input("确认执行此写操作？(yes/no): ").strip().lower()
            if confirm != "yes":
                print("操作已取消。如需调整，请重新输入需求。")
                continue
            print("已确认，使用 ai_writer 账户执行 ...")
        else:
            print("\n[3/4] 本操作为只读查询，使用 ai_readonly 账户 ...")

        # Step 5: 执行 SQL
        print(f"\n[4/4] 执行 SQL ...")
        result = execute_sql(sql, use_writer=write_op)

        # Step 6: 展示结果
        if isinstance(result, dict) and "error" in result:
            print(f"\n执行失败: {result['error']}")
            if "ai_readonly" in str(result.get("error", "")):
                print("提示: 只读账户无法执行写操作。")
        elif isinstance(result, list):
            print(f"\n查询结果 ({len(result)} 条记录):")
            print(format_query_result(result))
        else:
            print(f"\n操作完成: 影响 {result['affected_rows']} 行")


if __name__ == "__main__":
    main()
```

### 6.3 代码架构说明

```
ai_db_agent.py
│
├── 第一部分: 配置区
│   ├── LLM 配置 (DeepSeek API, 可替换为 Claude)
│   ├── DB 连接配置 (只读 + 读写 两套)
│   └── Agent 行为配置 (temperature, max_display)
│
├── 第二部分: System Prompt
│   ├── 安全规则硬约束 (禁止 DROP/TRUNCATE/ALTER)
│   ├── 写操作确认原则
│   ├── 数据库结构定义 (6列 + 3索引)
│   └── 输出格式规范 (4段式)
│
├── 第三部分: 核心函数
│   ├── ai_generate_sql()    → LLM 调用
│   ├── extract_sql()        → 正则提取
│   ├── is_write_operation() → 操作类型判断
│   ├── execute_sql()        → 数据库执行 + 权限选择
│   └── format_query_result()→ 结果格式化
│
└── 第四部分: 主交互循环
    ├── 启动横幅
    └── while True → 输入 → 生成 → 提取 → 确认 → 执行 → 展示
```

---

## 7. 测试用例

### 测试用例 1：简单查询

| 项目 | 内容 |
|------|------|
| **测试场景** | 基础 SELECT 查询 + 排序 |
| **用户输入** | `技术部有哪些员工？按薪资从高到低排列` |
| **预期 SQL** | `SELECT name, salary, hire_date, performance_score FROM employees WHERE department = '技术部' ORDER BY salary DESC;` |
| **预期结果** | 返回 4 条记录（王五/孙八/吴十/张三），按 salary 降序 |
| **使用账户** | `ai_readonly`（自动） |
| **验证通过条件** | 返回 4 条员工记录，孙八 salary=32000 排在第一位 |

### 测试用例 2：聚合统计

| 项目 | 内容 |
|------|------|
| **测试场景** | GROUP BY + HAVING 聚合查询 |
| **用户输入** | `按部门统计员工人数和平均薪资，只显示平均薪资高于18000的部门` |
| **预期 SQL** | `SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_salary FROM employees GROUP BY department HAVING AVG(salary) > 18000;` |
| **预期结果** | 技术部(4人/27750)、市场部(2人/19000)、财务部(1人/22000)；人事部(15000)被 HAVING 过滤 |
| **使用账户** | `ai_readonly`（自动） |
| **验证通过条件** | 返回 3 个部门，不包含人事部 |

### 测试用例 3：写操作触发权限隔离

| 项目 | 内容 |
|------|------|
| **测试场景** | UPDATE 写操作 → 人工确认流程 |
| **用户输入** | `给技术部所有绩效高于90的员工加薪10%` |
| **AI 预期行为** | (a) 先生成 SELECT 查询受影响范围: `SELECT name, salary, performance_score FROM employees WHERE department = '技术部' AND performance_score > 90;` (b) 生成 UPDATE 并标注安全提醒: `UPDATE employees SET salary = salary * 1.1 WHERE department = '技术部' AND performance_score > 90;` |
| **用户确认步骤** | 输入 `yes` 确认执行 |
| **使用账户** | 写操作切换到 `ai_writer` |
| **预期结果** | 王五(95分)/孙八(97分)/吴十(91分)薪资上涨10%；张三(92分)也上涨 |
| **验证通过条件** | (1) AI 先输出 SELECT (2) AI 标注了安全提醒 (3) 人工确认后才执行 (4) 使用 ai_writer 账户 |

### 测试用例 4：权限验证 —— 尝试 DROP

| 项目 | 内容 |
|------|------|
| **测试场景** | 验证双层安全防护 |
| **用户输入** | `帮我把 employees 表删掉` |
| **第一道防线** | AI System Prompt 约束 → AI 拒绝生成 DROP 语句，回复"此操作不在我的安全许可范围内" |
| **第二道防线** | 即使 AI 生成了 DROP → 以 `ai_writer` 执行 → MySQL 报错 "DROP command denied to user 'ai_writer'@'localhost'" |
| **使用账户** | 不适用（两层均被拦截） |
| **验证通过条件** | AI 拒绝生成 DROP 语句，或 MySQL 权限系统拒绝执行 |

---

## 8. 实操要点总结表

| 环节 | Prompt Engineering 的作用 | 安全机制 |
|------|--------------------------|----------|
| **需求输入** | 用户用自然语言描述需求，无需掌握 SQL 语法 | 无安全风险，纯自然语言输入 |
| **SQL 生成** | System Prompt 硬约束：禁止 DROP/TRUNCATE/ALTER，指定数据库结构，规范输出格式 | Prompt 层面的行为约束（第一道防线） |
| **SQL 提取** | 强制 AI 用 ```sql 代码块输出，正则精确提取，避免自然语言污染 | 解析可靠性保证 |
| **写操作确认** | System Prompt 要求 AI 先建议 SELECT 确认范围，再生成写 SQL | 人机协作决策确认（第二道防线） |
| **权限选择** | 根据 SQL 类型（读/写）自动选择 `ai_readonly` 或 `ai_writer` 账户 | MySQL 三层账户权限隔离（第三道防线） |
| **SQL 执行** | temperature=0.1 确保 SQL 生成的确定性 | 即使 AI 生成恶意/错误 SQL，权限隔离阻止其执行 |
| **结果展示** | 自然语言解读查询结果，降低数据理解门槛 | 敏感数据仅通过受限账户暴露 |

---

## 9. Prompt Engineering 在数据库操作中的关键原则

| # | 原则 | 技术含义 | 实现位置 |
|---|------|----------|----------|
| 1 | **硬约束前置** | 最关键的安全规则写在 System Prompt 的最前面（"严禁生成 DROP / TRUNCATE / ALTER / CREATE"）。AI 会优先遵守排在前面的约束。 | `SYSTEM_PROMPT` 第 10 行 |
| 2 | **结构化输出** | 强制 AI 使用 ```sql 代码块 + 固定字段（需求理解/结果说明/安全提醒），确保下游程序能可靠解析。禁止自由格式。 | `SYSTEM_PROMPT` 第 52-55 行 + `extract_sql()` |
| 3 | **低温参数** | `temperature=0.1`：SQL 是确定性语言，不需要创意。高温会导致 SQL 语法随机变异。 | `LLM_TEMPERATURE = 0.1` |
| 4 | **先查后改** | 所有写操作前，必须先用 SELECT 确认影响的数据范围和条数。这是数据库运维的黄金法则，直接写入 System Prompt。 | `SYSTEM_PROMPT` 第 19 行 |
| 5 | **最小权限** | AI 永远不应该获得 root 数据库权限。默认只读账户，写入需单独确认和切换。这是权限隔离的基石。 | `DB_CONFIG_READONLY` vs `DB_CONFIG_WRITER` 双配置 + `execute_sql()` 权限选择 |

---

# 第八部分：课程总结与作业

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

本课从"AI 工程体系全景"出发，建立了五层技术栈认知，然后深入 Prompt Engineering 实操，最后完成了 AI 数据库操作的完整实战项目。

**六个核心要点**：

| # | 要点 | 关键内容 |
|---|------|----------|
| 1 | **五层工程体系** | Prompt(指令) → Context(信息) → Harness(运行时) → Loop(循环) → Graph(编排) 构成完整 AI 工程技术栈 |
| 2 | **Agent 的本质** | Agent 不是一个技术/模型/框架，而是五层能力整合的系统——能自主规划并使用工具完成任务 |
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
| **Loop Engineering** | Agent 的"observe→think→act→feedback"推理循环 | Agent 可靠性工程的核心——防止死循环和错误滚雪球 |
| **Graph Engineering** | 用状态图编排 Agent 工作流（节点/边/条件/检查点） | 强监管行业 AI 落地的必要条件——可审计流转图替代黑箱决策 |
| **Agent** | 整合五层能力的自主任务完成系统 | 企业 AI 建设的终局目标——不是买一个工具，而是构建一个系统 |
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
| **Claude Code 架构分析** | 真实生产级 Agent 系统的架构设计剖析——权限模型、Hook 系统、MCP 集成、子代理机制 | 用真实案例理解五层体系的工程实现 |
| **MCP 官方文档** (modelcontextprotocol.io) | AI 工具连接的开放标准协议，解决"N 个模型 x M 个工具"的集成爆炸问题 | 企业 AI 工具投资避免被单一厂商锁定 |
| **LangGraph 文档** | 状态图编排框架：Checkpoint 机制、Human-in-the-loop、流式事件 | 强监管行业（金融/医疗/法律）AI 落地的技术基础 |
| **mem0 / Letta（开源记忆层）** | 跨会话长期记忆的开源实现（Context Engineering 延伸能力） | 理解 Agent "跨会话上下文"的技术实现 |

---

## 5. 常见问题 (FAQ)

### Q1: Prompt → Context → Harness → Loop → Graph，我应该从哪一层开始学？

**Prompt Engineering。** 这是所有上层工程的基础。先学会"怎么和 AI 说话"（1-2 周），再逐步理解"给 AI 看什么信息"（Context），然后才是"给 AI 装上手和脚"（Harness）。

零基础路径：Prompt Engineering（2周）→ 环境搭建实践（1周）→ Context Engineering（2周）→ Harness Engineering（4周+，需要编程基础）

### Q2: Claude Code 属于五层体系中的哪一层？

Claude Code 横跨 **Context / Harness / Loop / Graph** 四层：

- Context 层：自动压缩工具输出、对话历史管理
- Harness 层：Tool Registry (MCP)、Permission Gate (四级权限)、Hook System、Session 持久化
- Loop 层：高性能 Agent Loop、条件工具激活、子代理分发
- Graph 层：Subagents + Hooks 构成隐式工作流图，Pipeline 模式链式协作


### Q3: Agent 到底是什么？跟普通 AI 对话有什么区别？

**Agent 是能自主规划并使用工具完成任务的 AI 系统。** 普通 AI 对话是"一问一答"；Agent 是"给一个目标 → 自主分析 → 拆解步骤 → 调用工具 → 验证结果 → 循环直到完成"。

技术定义：Agent = LLM（大脑）+ Loop（循环推理）+ Tools（工具调用）+ Harness（运行时保障）。跨会话记忆（可选）属于 Context Engineering 的延伸能力，可通过 mem0/Letta 等记忆层工具实现。Agent 不是一个"产品品类"，而是一个"系统范式"。

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

**同一会话内可以**（受上下文窗口限制，通常 200K Token）。**不同会话之间不共享记忆** —— 除非使用了跨会话记忆系统（如 mem0、Letta 等，属于 Context Engineering 的延伸能力）。

企业场景中，"跨会话记忆"是 RAG + 用户画像系统的核心场景——将用户在 CRM 中的历史交互、偏好、合同信息注入每次 AI 交互的上下文。

---

## 6. 附录：五层工程体系速查表

| 层级 | 核心问题 | 代表工具/系统 | 企业成熟度 | 学习优先级 |
|------|----------|-------------|:----------:|:----------:|
| **Prompt Engineering** | 怎么和 AI 说话 | ChatGPT / Claude / DeepSeek | ★★★★★ 高度成熟 | 🔴 第1优先级 |
| **Context Engineering** | 给 AI 看什么信息 | Claude Code / mem0 / RAG 框架 | ★★★★☆ 快速成熟中 | 🔴 第2优先级 |
| **Harness Engineering** | Agent 的身体（运行时） | Claude Code / Codex / DeerFlow | ★★★☆☆ 2025年成为焦点 | 🟡 第3优先级 |
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
