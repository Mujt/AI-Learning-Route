# KB3：Harness Engineering 与 Hermes Engineering 深度解析

---

## 一、知识块信息

| 项目 | 内容 |
|------|------|
| **所属课程** | AI 时代能力培养 |
| **所属课次** | 第2课：从 Prompt Engineering 到 Agent 工程体系 |
| **知识块序号** | KB3 / 本课共4个KB |
| **知识块标题** | Harness Engineering 与 Hermes Engineering 深度解析 |
| **前置知识块** | KB1 (Prompt+Context Engineering)、KB2 (RCTE框架+Prompt技巧) |
| **预计时长** | 25分钟 |
| **知识块类型** | 技术讲授 |
| **适用对象** | 💼 企业管理者/投资人 + 🎓 零基础学习者（技术深度分级标注） |
| **核心议题** | 1. Agent 运行时基础设施（Harness）的六大组件<br>2. 长运行个人 Agent（Hermes）的四大能力<br>3. Harness vs Hermes 的工程定位差异 |

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

## 三、Hermes Engineering 深度解析

### 3.1 定义

**Hermes Engineering（信使工程）** 是以 Hermes Agent（NousResearch 开源项目）为代表的长运行、本地优先、具备长期记忆和跨应用能力的个人 Agent 工程范式。名称来源于古希腊神话中的信使之神赫尔墨斯（Hermes）——在众神与凡人之间传递信息。

前三层（Prompt / Context / Harness）共同构建了 Agent 的"单次任务执行能力链"。但一个真正有用的个人 Agent 需要更进一步：在数天、数周甚至数月内持续运行，记住用户偏好，跨不同应用和平台完成任务，并在离线时仍能收到消息并自主响应。

**Hermes Engineering 是第四层——它在 Harness 之上叠加了"时间维度"（长期运行）和"空间维度"（跨平台）的能力。**

### 3.2 技术原理：传统 Harness Agent vs Hermes-style Agent

```
传统 Harness Agent                     Hermes-style Personal Agent
──────────────────────                 ─────────────────────────────────

执行模式：                             执行模式：
  单次会话执行                           长运行 (Always-On)
  启动 → 执行 → 结束                     持续监听 → 自主触发 → 后台执行
  生命周期 = 一次对话                     生命周期 = 类似操作系统的守护进程

记忆模型：                             记忆模型：
  短期上下文 (当前对话窗口)                三层记忆系统
  重启 / 新会话后全部丢失                   · 短期: 当前会话上下文
                                         · 工作: 当前任务的关键状态
                                         · 长期: 跨会话持久化的偏好/事实/关系

交互入口：                             交互入口：
  单一入口 (CLI / Web UI)               多平台消息网关
  只能从固定界面交互                      统一消息路由层
                                         WhatsApp / Telegram / Slack / 飞书
                                         用户在任何平台都能触发 Agent

能力范围：                             能力范围：
  工具限于当前运行环境                     Skills 系统
  只能调用本地或 API 工具                 可复用的操作手册 (SKILL.md)
                                         一次编写, 多场景复用
                                         跨应用能力 (浏览器/文件/终端/API)

容错机制：                             容错机制：
  崩溃 = 从头开始                        心跳检测 + 状态持久化
  无自我恢复能力                          崩溃后自动重启
                                         从断点继续执行
```

**Hermes Engineering 解决的核心问题**：

| 问题 | 传统 Agent 的表现 | Hermes-style 的表现 |
|------|------------------|---------------------|
| 用户偏好记忆 | 每次对话都要重新告知偏好 | 跨会话记住用户偏好，自动应用 |
| 异步任务 | 用户必须守着 Agent 执行 | Agent 后台执行，完成后通知用户 |
| 跨平台使用 | 换个界面就要重新开始 | 统一身份，跨平台无缝切换 |
| 长时间任务 | 断开连接 = 任务丢失 | 后台持续执行，随时查看进度 |
| 知识积累 | 每次都是"新人" | Agent 越用越懂你 |

### 3.3 四大核心组件详解

#### 3.3.1 长期记忆系统（Long-term Memory）

**三层记忆架构**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     三层记忆系统                                  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     短期记忆 (Short-term)                   │  │
│  │                                                           │  │
│  │  存储: LLM 上下文窗口 (200K Token)                          │  │
│  │  内容: 当前会话的完整对话历史 + 工具输出                       │  │
│  │  生命周期: 当前会话                                          │  │
│  │  访问速度: 即时 (在上下文窗口中)                               │  │
│  │  容量限制: 受上下文窗口限制                                   │  │
│  │                                                           │  │
│  │  例: "刚才用户说他的数据库是 PostgreSQL 14"                   │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             │                                    │
│         Context Compaction  │  提取关键信息                       │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     工作记忆 (Working)                      │  │
│  │                                                           │  │
│  │  存储: 结构化 JSON (Redis / 应用内存)                        │  │
│  │  内容: 当前任务的关键状态、中间结果、已确认的决策                │  │
│  │  生命周期: 跨会话 (同一任务内)                                │  │
│  │  访问速度: 毫秒级 (内存/Redis)                                │  │
│  │  容量: 通常 < 10KB (只保留最相关的)                           │  │
│  │                                                           │  │
│  │  例: {"task": "数据库迁移", "source": "MySQL 5.7",          │  │
│  │        "target": "PostgreSQL 14", "tables_done": 12,       │  │
│  │        "tables_total": 45}                                 │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             │                                    │
│              记忆蒸馏 (AI)   │  结构化提取 + 去重 + 合并            │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     长期记忆 (Long-term)                    │  │
│  │                                                           │  │
│  │  存储: 向量数据库 (ChromaDB / Pinecone / Milvus)            │  │
│  │  内容: 用户偏好、领域事实、关系图谱、经验教训                   │  │
│  │  生命周期: 永久 (除非主动删除)                                │  │
│  │  访问速度: 百毫秒级 (语义检索)                                │  │
│  │  检索方式: 语义相似度 → Top-K 相关记忆注入当前上下文            │  │
│  │                                                           │  │
│  │  结构化记忆示例:                                             │  │
│  │  {                                                        │  │
│  │    "type": "preference",                                   │  │
│  │    "content": "用户偏好使用 async/await 而非回调",           │  │
│  │    "context": "编程任务",                                    │  │
│  │    "confidence": 0.95,                                     │  │
│  │    "last_updated": "2026-08-05T10:30:00Z"                  │  │
│  │  }                                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**跨会话记忆检索流程**：

```
新会话开始
    │
    ▼
提取用户当前输入的语义特征
    │
    ▼
在长期记忆向量库中检索 Top-K 相关记忆
    │  query: "帮我写个数据库迁移脚本"
    │  retrieved:
    │    1. (score: 0.92) 用户使用 PostgreSQL 14
    │    2. (score: 0.87) 用户偏好 async/await
    │    3. (score: 0.81) 上次迁移使用了 Alembic
    │
    ▼
将检索到的记忆注入 System Prompt 或上下文
    │  "<user_preferences>
    │     数据库: PostgreSQL 14
    │     编码风格: async/await
    │     迁移工具: Alembic (上次使用)
    │   </user_preferences>"
    │
    ▼
LLM 在该上下文中进行推理 → 输出尊重用户偏好的结果
    │
    ▼
会话结束时：提取本次对话中的新信息 → 写入长期记忆
    │  新增: "用户现在同时管理 MySQL 和 PostgreSQL"
    │  更新: "迁移工具偏好 → 本次也使用了 Alembic (confidence ↑)"
```

#### 3.3.2 Skills 系统

**技术原理**：Skill 是一份小型的、自包含的操作手册（通常命名为 `SKILL.md`），包含该技能的触发条件、执行步骤、所需工具、验收标准。Agent 按需加载相关 Skills 作为操作指导——Skill 不是代码（不是 Tool），不是对话（不是 Prompt），不是外部服务（不是 MCP），而是一种**可复用的操作知识**。

**SKILL.md 标准结构**：

```markdown
# Skill: deploy-aws-lambda

## Trigger (触发条件)
- When: user mentions "deploy" + "lambda" or "serverless deploy"
- Priority: high (匹配后优先加载)

## Description (功能描述)
Deploy a Node.js/Python function to AWS Lambda with proper IAM
role configuration and environment variable setup.

## Prerequisites (前置条件)
- AWS CLI configured (`aws configure`)
- Lambda execution role exists (arn:aws:iam::*)

## Steps (执行步骤)
1. Validate function code (`npm run build` or `python -m py_compile`)
2. Package code + dependencies into ZIP
3. Check if Lambda function exists → update or create
4. Set environment variables from .env.production
5. Verify deployment with a test invocation

## Scripts (可用脚本)
- `scripts/validate-lambda.sh` — pre-deploy validation
- `scripts/rollback.sh` — rollback to previous version

## Acceptance Criteria (验收标准)
- [ ] Lambda function responds to test event
- [ ] CloudWatch logs show no errors
- [ ] Environment variables correctly injected

## Common Pitfalls (常见陷阱)
- Lambda 超时默认 3 秒 → 需要根据函数复杂度调整
- IAM Role 权限不足 → 检查 CloudWatch Logs 写入权限
```

**Skill vs Tool vs Prompt vs MCP 四维区分**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    四者定位对比                                    │
│                                                                 │
│  Skill             Tool             Prompt           MCP        │
│  ──────            ────             ──────           ───        │
│  操作知识          执行能力           任务指令          通信协议     │
│  "怎么做"          "能做什么"         "要做什么"         "怎么连"    │
│                                                                 │
│  ┌──────────┐    ┌──────────┐     ┌──────────┐    ┌──────────┐ │
│  │ SKILL.md │    │function()│     │  自然语言  │    │ JSON-RPC │ │
│  │ 步骤+验收 │    │ API调用   │     │  指令描述  │    │ 接口规范  │ │
│  └──────────┘    └──────────┘     └──────────┘    └──────────┘ │
│                                                                 │
│  例:             例:              例:             例:            │
│  "部署 AWS       aws_lambda       "帮我把这个     MCP Server     │
│   Lambda 的       .update_        函数部署到      提供            │
│   完整操作        function_        AWS Lambda     tools/list     │
│   手册"          code()           上"            接口            │
│                                                                 │
│  Skill 可以调用 Tool, 使用 MCP 协议接入的外部服务,                     │
│  并被 Prompt 引用。四者协同，而非互斥。                               │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.3.3 多平台消息网关（Multi-Platform Message Gateway）

**技术原理**：构建统一的消息路由层，将不同平台（WhatsApp / Telegram / Slack / Discord / 飞书 / 微信）的用户消息统一转换为标准化的 Agent 输入格式；Agent 的回复由网关根据来源平台反向分发。

```
                          ┌─────────────────────┐
      WhatsApp ──────────→│                     │
                          │   Message Gateway   │
      Telegram ──────────→│                     │
                          │  ┌───────────────┐  │
      Slack ─────────────→│  │ 统一消息格式    │  │
                          │  │                │  │
      飞书 ───────────────→│  │ {              │  │      ┌──────────────┐
                          │  │   "platform":  │  │─────→│              │
      微信 ───────────────→│  │     "whatsapp",│  │      │   Hermes     │
                          │  │   "user_id":   │  │      │   Agent      │
      ...                 │  │     "U12345",  │  │      │   Core       │
                          │  │   "message":   │  │←─────│              │
                          │  │     "帮我...",  │  │      └──────────────┘
                          │  │   "timestamp": │  │
                          │  │     "...",     │  │
                          │  │   "attachments":│ │
                          │  │     [...]      │  │
                          │  │ }              │  │
                          │  └───────────────┘  │
                          │                     │
                          │  路由回发:            │
                          │  Agent 回复 → 识别    │
                          │  来源平台 → 格式化    │
                          │  → 发回对应平台       │
                          └─────────────────────┘
```

**网关核心功能**：

| 功能 | 说明 | 技术实现 |
|------|------|----------|
| **协议适配** | 将各平台 API 差异归一化 | Adapter 模式: 每平台一个 Adapter |
| **消息归一化** | 文本/图片/文件/语音 → 统一内部格式 | JSON Schema 强约束 |
| **身份映射** | 不同平台的用户 ID → 统一用户身份 | User Identity Mapping Table |
| **会话管理** | 同一用户跨平台消息归入同一会话 | Session Affinity (Redis) |
| **限流保护** | 防止用户滥用 → 按用户/平台限流 | Token Bucket / Sliding Window |

#### 3.3.4 心跳与恢复（Heartbeat & State Recovery）

**技术原理**：Agent 以守护进程方式运行时，通过定期心跳信号证明自己"还活着"；如果进程崩溃或被杀死，看门狗检测到心跳丢失后自动重启 Agent，Agent 从持久化的状态中恢复，从断点继续执行。

```
┌─────────────────────────────────────────────────────────────────┐
│                    心跳与恢复机制                                  │
│                                                                 │
│    ┌──────────┐       每 5s 心跳         ┌──────────────┐       │
│    │          │ ──────────────────────→  │              │       │
│    │  Hermes  │                          │  Watchdog    │       │
│    │  Agent   │ ←──────────────────────  │  (看门狗)     │       │
│    │  Process │       ACK / NACK         │              │       │
│    └────┬─────┘                          └──────┬───────┘       │
│         │                                       │               │
│         │  每步保存状态到 Session Store            │  心跳超时 30s   │
│         ▼                                       │  未收到 → 杀进程 │
│    ┌──────────┐                                 │  重启 Agent     │
│    │ Session  │                                 │               │
│    │ Store    │ ←────────────────────────────────┘               │
│    │(Redis/DB)│                                                 │
│    └──────────┘                                                 │
│                                                                 │
│    恢复流程:                                                      │
│    1. Watchdog 检测心跳超时                                        │
│    2. 发送 SIGTERM → 等待 5s → SIGKILL (确保僵尸进程被清理)          │
│    3. 启动新 Agent 进程                                            │
│    4. Agent 从 Session Store 加载最新状态                          │
│    5. Agent 从最后 Checkpoint 继续执行                             │
│    6. 向用户发送通知: "Agent 已恢复，任务继续执行中"                  │
│                                                                 │
│    CyberClaw 改进 — 两段式心跳:                                    │
│    · L1 心跳 (轻量): 仅报告进程存活, 每 5s                          │
│    · L2 心跳 (深度): 报告任务进度 + 资源消耗, 每 60s                 │
│    · L1 超时 → 重启 | L2 未到但 L1 正常 → 任务可能卡死, 告警        │
│                                                                 │
│    OpenClaw State Recovery — 快照 + 增量日志:                      │
│    · 每 100 步: 全量快照 (State Snapshot)                          │
│    · 每步: 增量操作日志 (WAL - Write Ahead Log)                    │
│    · 恢复: 加载最近快照 → 重放增量日志 → 精确恢复到断点               │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 代表系统对比

| 维度 | OpenClaw | Hermes Agent | CyberClaw |
|------|----------|-------------|-----------|
| **定位** | 本地优先个人 Agent | 自托管个人 Agent | 透明可控 Agent |
| **长期记忆** | 文件 + 向量检索 | 三层记忆 (短期/工作/长期) + 向量数据库 | 双水位记忆 (快速+深度) |
| **Skills 系统** | SKILL.md 操作手册 | SKILL.md + Toolsets 组合 | 审计型 Skill 执行 |
| **消息网关** | Channel 系统 | 多平台 Message Gateway | 审计消息队列 |
| **心跳/恢复** | State Recovery (快照+WAL) | 心跳 + 会话恢复 | 两段式心跳 (L1+L2) |
| **安全审计** | 本地执行, 用户控制 | 权限分级 | 全行为审计 + 两段式安全调用 |
| **部署方式** | 本地 (macOS/Linux) | 自托管 Docker | 自托管 + 云端可选 |
| **开源** | 开源 | 开源 (NousResearch) | 部分开源 |

### 3.5 企业视角

> 📊 **企业视角**：Hermes Engineering 代表了 AI 从"生产力工具"向"个人操作系统"的进化。对企业而言，这意味着每个知识工作者未来都会拥有一个"数字影子"——它记住你的所有工作上下文，理解你的偏好和决策模式，在你休假时能代替你回答 80% 的日常问题，在你返回时以结构化摘要汇报"你不在时发生了什么"。这不是科幻，OpenClaw 和 Hermes Agent 已经在 2025-2026 年实现了这个愿景的基础版本。企业 CIO 应关注：长运行 Agent 的安全审计、多平台消息网关的数据合规（GDPR/PIPL）、以及记忆系统的隐私控制（用户能否一键清除所有记忆）。

---

## 四、Harness vs Hermes 定位对比

```
┌─────────────────────────────────────────────────────────────────┐
│               Harness Engineering vs Hermes Engineering          │
│                                                                 │
│                          ┌──────────┐                            │
│                          │  Hermes  │  ← 长运行、记忆、跨平台      │
│                          │  (第四层) │    个人 Agent 的完整形态     │
│                          └────┬─────┘                            │
│                               │                                   │
│                          ┌────┴─────┐                            │
│                          │  Harness │  ← 工具注册、权限、会话       │
│                          │  (第三层) │    Agent 的运行基础设施       │
│                          └────┬─────┘                            │
│                               │                                   │
│                     Context + Prompt (第一、二层)                  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  核心区别:                                                        │
│                                                                 │
│  ┌──────────────┬──────────────────┬──────────────────┐        │
│  │    维度       │     Harness      │     Hermes       │        │
│  ├──────────────┼──────────────────┼──────────────────┤        │
│  │ 时间跨度      │ 单次会话 (分钟~小时)│ 持续运行 (天~月)  │        │
│  │ 记忆范围      │ 当前会话窗口      │ 跨会话持久记忆     │        │
│  │ 启动方式      │ 用户主动触发      │ 常驻后台自主响应    │        │
│  │ 入口形态      │ 单一 (CLI/Web)   │ 多平台消息网关     │        │
│  │ 与人关系      │ 工具 (用完即走)   │ 伙伴 (长期协作)    │        │
│  │ 代表系统      │ Claude Code      │ OpenClaw          │        │
│  └──────────────┴──────────────────┴──────────────────┘        │
│                                                                 │
│  关系: Hermes = Harness + 时间维度 + 空间维度 + 记忆系统           │
│        每个 Hermes Agent 内部都包含一个 Harness 层                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、关键结论

1. **Harness Engineering 是 Agent 进入生产环境的必要条件**。没有 Harness 的 Agent 只是 Demo 玩具——缺乏权限控制、会话持久化、日志审计和错误恢复能力。

2. **Harness 的六个组件构成一个完整的运行时闭环**：Tool Registry（能力）→ Permission Gate（安全）→ Hook System（扩展）→ Context Compaction（效率）→ Session Store（可靠性）→ Trace/Log（可观测性）。缺少任何一个，生产环境都会出现致命短板。

3. **Hermes Engineering 在 Harness 之上叠加了"时间"和"空间"两个维度**。时间维度 = 长期运行 + 记忆积累；空间维度 = 跨平台 + 跨应用。这让 Agent 从"单次工具"进化为"长期伙伴"。

4. **三层记忆系统是 Hermes 的核心差异**。短期记忆（上下文窗口）解决"现在在做什么"，工作记忆（结构化状态）解决"这一步做到哪了"，长期记忆（向量数据库）解决"用户是谁、偏好什么"。

5. **Skill / Tool / Prompt / MCP 四者不是竞争关系，而是互补关系**。Skill 定义操作知识（怎么做），Tool 提供执行能力（能做什么），Prompt 传达任务意图（要做什么），MCP 标准化通信协议（怎么连）。一个成熟的 Agent 系统需要四者协同。

6. **对企业而言，Harness 是"安全底线"，Hermes 是"进化方向"**。先保证 Agent 的安全可控（Harness），再追求 Agent 的长期协作能力（Hermes）。
