# KB1：六层AI工程体系概览

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB1 / 本课共8个KB |
| **知识块标题** | 六层AI工程体系概览 |
| **预计时长** | 15分钟 |
| **教学形式** | 理论讲解 |
| **适合人群** | 💼 企业管理者/投资人 + 🎓 零基础学习者 |
| **核心目标** | 建立AI工程的完整技术栈认知框架，理解六层金字塔的层次关系，掌握 Claude Code 在体系中的定位，建立"Agent是六层整合系统"的核心认知 |

---

## 二、六层金字塔总览

当前（2026年）的 AI 技术已经从"写好提示词"进化到了"构建自主运行的智能系统"。以下六层工程体系，从底层到顶层，逐层代表了 AI 能力的递进。每一层建立在下层之上，不可跳跃。

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI 工程体系六层金字塔                               │
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
│                        │ Hermes       │  ← 个人长运行 Agent           │
│                        │ Engineering  │     记忆+Skills+消息入口       │
│                        │ 信使工程      │     "数字影子"——永远在线的助手  │
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
│   Claude Code 横跨 Context / Harness / Loop / Graph 四层             │
│   ChatGPT/Claude/DeepSeek 网页版运行在 Prompt Engineering 层           │
└─────────────────────────────────────────────────────────────────────┘
```

### 金字塔解读原则

- **自底向上构建**：每一层的能力依赖下一层提供的基础
- **不可跳跃**：跳过 Context 直接做 Loop，Agent 必然"失忆"
- **入门从底层开始**：Prompt Engineering 是 ROI 最高的入口
- **企业评估从上往下看**：顶层（Graph）代表最成熟的企业级能力

---

## 三、为什么需要理解这六层？—— 从"会用AI"到"构建AI系统"的认知升级

### 3.1 当前 AI 学习的主要误区

| 常见误区 | 实际情况 |
|----------|----------|
| "AI 就是写 Prompt" | Prompt 只是第一层。真正强大的 AI 系统涉及六层整合 |
| "Agent 就是一个 while 循环调 LLM" | 裸 Loop 只有 ~100 行代码，但生产级 Agent 需要六层完备支撑（数千到数万行） |
| "买个 RAG 工具就能做好企业 AI" | RAG 只是 Context Engineering 的一个子集。上下文设计不当，RAG 效果远低于预期 |
| "用最好的模型就够了" | 模型能力只是上限，六层工程决定了实际能达到的下限 |

### 3.2 认知升级路径

```
会用 AI                   懂 AI 原理                构建 AI 系统
────────────────────── ────────────────────── ──────────────────────
使用 ChatGPT 网页版       理解 Prompt 设计原理       搭建企业 Prompt 模板库
问一个问题 → 得到一个答案   理解 Context 管理策略      构建 RAG 检索增强系统
                          理解 Agent 运行时机制      部署生产级 Agent 应用
                          理解 Loop 推理循环         设计多 Agent 协作编排
                          
认知层级: Prompt           认知层级: Prompt→Context    认知层级: 六层全覆盖
```

### 3.3 六层体系的来源：为什么是这六层？

这个六层体系并非凭空设计，而是总结了 2024-2026 年 AI 工程领域的多个独立趋势后归纳而成的认知框架：

| 趋势来源 | 对应的层 | 触发事件 |
|----------|---------|----------|
| Prompt Engineering 最佳实践文档化 | Layer 1 | Anthropic/OpenAI Prompt Engineering Guide (2024) |
| RAG 系统的广泛部署和"效果不好"的反思 | Layer 2 | 企业 RAG 部署潮 + Context Engineering 概念提出 (2024-2025) |
| AI Harness Engineering 论文发表 | Layer 3 | arXiv:2605.13357 "AI Harness Engineering" 定义性论文 (2025.05) |
| Hermes Agent 开源 + 个人 Agent 概念兴起 | Layer 4 | NousResearch Hermes Agent 开源 (2025) |
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

Harness (L3) ──→ Hermes (L4)
  解决了："每次启动 AI，它都不记得之前的事"
  升维方式：从"单次会话"升级为"长运行跨会话"

Hermes (L4) ──→ Loop (L5)
  解决了："AI 只能被一问一答驱动，不能自主规划"
  升维方式：从"被动响应"升级为"自主推理循环"

Loop (L5) ──→ Graph (L6)
  解决了："AI 的决策过程是一个黑箱，无法审计和恢复"
  升维方式：从"线性循环"升级为"可编排的状态图"
```

### 3.5 六层体系的实践意义

| 角色 | 需要重点关注的层 | 为什么 |
|------|-----------------|--------|
| **普通用户** | Prompt Engineering | 日常使用 AI 只需要写好 Prompt |
| **高级用户/超级个体** | Prompt + Context | 管理复杂的多轮对话和长文档任务 |
| **AI 应用开发者** | Prompt + Context + Harness | 构建可部署的 AI 应用 |
| **Agent 系统架构师** | 全部六层 | 设计完整的自主智能系统 |
| **企业技术决策者** | 六层全景 + Harness/Graph | 评估技术成熟度和采购决策 |

---

## 四、六层速览表

| 层级 | 核心问题 | 技术本质 | 代表工具/系统 | 企业成熟度 |
|------|----------|----------|-------------|-----------|
| **Prompt Engineering** (提示词工程) | 怎么和 AI 说话？ | 设计精准的自然语言指令，对 Token 预测方向施加约束 | ChatGPT、Claude、DeepSeek、Gemini | ★★★★★ 高度成熟 |
| **Context Engineering** (上下文工程) | 给 AI 看什么信息？看多少？怎么看？ | 管理模型在推理时可用的完整信息环境，在有限上下文窗口内最大化信息密度 | Claude Code、mem0、RAG 系统 | ★★★★☆ 快速成熟中 |
| **Harness Engineering** (根基工程) | Agent 的"身体"长什么样？ | 构建 Agent 运行时基础设施：工具注册、权限控制、会话管理、追踪日志 | Claude Code、Codex(OpenAI)、DeerFlow(字节) | ★★★☆☆ 2025年成为独立学科 |
| **Hermes Engineering** (信使工程) | 如何让 Agent 一直在线、记住一切？ | 长运行、本地优先、具备长期记忆和跨应用能力的个人 Agent | OpenClaw、Hermes Agent、CyberClaw | ★★☆☆☆ 早期阶段 |
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

## 五、Claude Code 在六层中的定位详解

Claude Code 是 Anthropic 官方推出的命令行 AI 编码 Agent。它不是"一个模型"或"一个框架"，而是六层体系的一个完整实例。理解 Claude Code 覆盖了哪些层、没覆盖哪些层，是理解六层体系最好的方式。

### 5.1 逐层分析

```
Claude Code 在六层体系中的定位：

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

  Hermes Engineering     ❌ 不包含长期记忆 —— 每次启动新会话，不记住过往对话
                             不包含多消息平台网关 —— 仅 CLI 入口
                             不包含跨设备同步 —— 本地运行
                             （Claude Code 是按需启动的 CLI，非常驻后台进程）

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
| Hermes Engineering | 无长期记忆、无跨会话上下文 | mem0/Letta（记忆层）、OpenClaw（长运行） |
| Graph Engineering（完整） | 无显式 State Graph 编排、无 Checkpoint | LangGraph（补充完整图编排能力） |

---

## 六、"Agent 到底是什么？"—— 结合六层体系的完整回答

### 6.1 一句话定义

> **Agent（智能体）不是一个技术、不是一种模型、不是一个框架。Agent 是一个系统——它整合了 Prompt Engineering（理解任务）、Context Engineering（信息环境）、Harness Engineering（运行时能力）、Hermes Engineering（记忆和持久化）、Loop Engineering（自主推理循环）、Graph Engineering（可编排工作流）的完整系统。**

### 6.2 逐层拆解：Agent 的六层构成

```
"Agent" 这个概念的六层拆解：

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

Layer 4 — Hermes Engineering:
  Q: 没有 Hermes，Agent 能记住你上周跟它说过的话吗？
  A: 不能。每次新会话，Agent 从零开始。Hermes 给了 Agent "长期记忆"。

Layer 5 — Loop Engineering:
  Q: 没有 Loop，Agent 怎么自主完成多步任务？
  A: 只能一问一答。Loop 给了 Agent 自主推理和迭代的能力——"大脑"。

Layer 6 — Graph Engineering:
  Q: 没有 Graph，Agent 怎么被编排到企业工作流中？
  A: 只能独立运行。Graph 让 Agent 可以被编排、被审计、被恢复——"企业级"。

结论：只有六层齐全，才是一个"完全体的 Agent"。
     但实际应用中，大多数"Agent"只具备其中 3-4 层。
```

### 6.3 Agent 分级：从 L1 到 L6

| 级别 | 具备的层 | 典型表现 | 实例 |
|------|---------|----------|------|
| **L1 Chatbot** | Prompt only | 一问一答，无工具调用，无记忆 | ChatGPT 基础对话 |
| **L2 RAG Bot** | Prompt + Context | 能检索知识库回答，但无自主行动 | 企业客服机器人 |
| **L3 Tool Agent** | Prompt + Context + Harness | 能调用工具，有权限控制 | Cline + 简单配置 |
| **L4 Persistent Agent** | + Hermes | 有长期记忆，跨会话记住用户偏好 | OpenClaw/Hermes Agent |
| **L5 Autonomous Agent** | + Loop | 能自主规划多步任务，自我纠错 | Claude Code、Devin |
| **L6 Orchestrated Agent** | + Graph | 可编排到企业工作流，可审计可恢复 | LangGraph 企业部署 |

### 6.4 关键澄清

| 常见说法 | 准确理解 |
|----------|----------|
| "这是一个 AI Agent" | 不精确。应该说"这是一个具备 L3 能力的 Agent"——明确了具备哪些层 |
| "Agent = LLM + Tools" | 不完整。这只是 L3。缺少 Context/Hermes/Loop/Graph |
| "用 LangChain 就能做 Agent" | LangChain 提供了 Harness 的一部分（工具注册），但不是完整 Harness |
| "Claude Code 是一个 Agent" | Claude Code 是一个 L5 Agent（具备 Context+Harness+Loop，缺失 Hermes） |

---

## 七、关键结论

### 7.1 本知识块的 5 个核心记忆点

1. **六层金字塔结构**：Prompt → Context → Harness → Hermes → Loop → Graph，底层是基础，顶层是编排
2. **不能跳跃**：每一层建立在下层之上，跳过 Context 做 Loop 必然导致 Agent "失忆"
3. **Agent 是系统，不是技术**：Agent = 六层能力的整合，不是单一模型或框架
4. **Claude Code 覆盖 Context/Harness/Loop/Graph 四层**，是目前最好的 Agent 学习样本
5. **入门从 Prompt 开始**：Prompt Engineering 是所有上层能力的入口和基础

### 7.2 不同角色的行动建议

| 角色 | 本课后续应重点关注 | 课后行动 |
|------|------------------|----------|
| 🎓 零基础学习者 | KB2（Prompt+Context）+ KB5（Prompt实战） | 动手写 20 个不同场景的 Prompt |
| 💼 企业管理者 | 六层速览表 + Claude Code 定位 + Agent 分级 | 评估企业当前处于哪一层，差距在哪 |
| 🔧 开发者 | 全部六层详解（KB2-KB4） | 搭建 Claude Code/Codex 环境深入体验 Harness 层 |

### 7.3 过渡到下一知识块

六层金字塔的最底层——Prompt Engineering 和 Context Engineering——是 ROI 最高、学习门槛最低的入口。下一知识块将深入这两层：Token 预测的数学原理、Prompt 的六组件构成、Context 的三大管理策略。

---

> **本知识块核心记忆点**：六层金字塔（Prompt→Context→Harness→Hermes→Loop→Graph）；Agent 是六层整合系统；Claude Code 横跨四层。
