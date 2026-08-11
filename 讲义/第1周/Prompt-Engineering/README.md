# 第二课：从 Prompt Engineering 到 Agent 工程体系 —— 教学总控文档

> **本文件用途**：作为第2课完整教学流程的总控台。教师按照本文档的顺序和时间安排，依次使用各知识块（KB）文档进行授课。
>
> **总时长**：约 180 分钟（3小时），可根据实际教学节奏弹性调整 ±20 分钟。

---

## 一、课程信息

| 项目 | 说明 |
|------|------|
| **课程名称** | AI时代能力培养 |
| **周次** | 第1周 |
| **课序** | 第2课（本周共2课） |
| **课题** | 从 Prompt Engineering 到 Agent 工程体系 + Prompt Engineering 深入 |
| **总时长** | 约 180 分钟（3小时） |
| **理论/实操比** | 约 55% 讲解 + 45% 实操 |
| **适合人群** | 💼 企业管理者/投资人 + 🎓 零基础学习者 |
| **前置要求** | 已完成第1课学习，已注册至少一个 AI 工具账号 |
| **本课定位** | 上半部分建立AI工程的完整技术栈视野（Prompt→Context→Harness→Hermes→Loop→Graph），下半部分深入 Prompt Engineering 实操 |

---

## 二、知识块总览与时间分配

```
┌──────────────────────────────────────────────────────────────────┐
│        第二课：从 Prompt Engineering 到 Agent 工程体系              │
│                      教学流程 (180分钟)                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [KB1] 六层AI工程体系概览            15分钟    理论讲解             │
│         ↓                                                        │
│  [KB2] Prompt + Context Engineering 深入   25分钟    深度讲解       │
│         ↓                                                        │
│  [KB3] Harness + Hermes Engineering 深入  25分钟    深度讲解       │
│         ↓                                                        │
│  [KB4] Loop + Graph Engineering 深入      20分钟    深度讲解       │
│         ↓                                                        │
│  [KB5] Prompt Engineering 实战详解        25分钟    讲解+示例       │
│         ↓                                                        │
│  [KB6] VSCode + Claude + DeepSeek 环境搭建  25分钟    实操          │
│         ↓                                                        │
│  [KB7] MySQL数据库操作实操               35分钟    动手实操         │
│         ↓                                                        │
│  [KB8] 课程总结与作业                   10分钟    收尾总结          │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  总计：约 180 分钟（可弹性调整 ±20 分钟）                            │
│  理论讲解：约 110 分钟    实操：约 60 分钟    机动/过渡：约 10 分钟   │
└──────────────────────────────────────────────────────────────────┘
```

### 各知识块文件索引

| 序号 | 知识块 | 文件名 | 时长 | 类型 |
|------|--------|--------|------|------|
| KB1 | 六层AI工程体系概览 | `KB1-六层AI工程体系概览.md` | 15分钟 | 理论讲解 |
| KB2 | Prompt + Context Engineering 深入 | `KB2-Prompt与Context工程深入.md` | 25分钟 | 深度讲解 |
| KB3 | Harness + Hermes Engineering 深入 | `KB3-Harness与Hermes工程深入.md` | 25分钟 | 深度讲解 |
| KB4 | Loop + Graph Engineering 深入 | `KB4-Loop与Graph工程深入.md` | 20分钟 | 深度讲解 |
| KB5 | Prompt Engineering 实战详解 | `KB5-Prompt工程实战详解.md` | 25分钟 | 讲解+示例 |
| KB6 | VSCode + Claude + DeepSeek 环境搭建 | `KB6-环境搭建实操.md` | 25分钟 | 实操 |
| KB7 | MySQL数据库操作实操 | `KB7-数据库操作实操.md` | 35分钟 | 动手实操 |
| KB8 | 课程总结与作业 | `KB8-课程总结与作业.md` | 10分钟 | 收尾总结 |

---

## 三、详细教学流程

### 课前准备（上课前15分钟）

- [ ] 确认教室投影/屏幕共享正常工作
- [ ] 确认教室网络通畅
- [ ] 打开本总控文档 + KB1 文档
- [ ] 在浏览器中登录 Claude、DeepSeek、ChatGPT 中至少 2 个
- [ ] 确认 VSCode + Cline 插件已安装并可正常使用
- [ ] 确认本地 MySQL 已安装并导入测试数据（ai_test_company 数据库）
- [ ] 准备故障预案：网络中断 → 用本地 DeepSeek；IDE故障 → 用网页版 AI 替代

---

### KB1：六层AI工程体系概览（15分钟）

> **文件**：[KB1-六层AI工程体系概览.md](KB1-六层AI工程体系概览.md)
> **定位**：建立 AI 工程的完整技术栈认知框架

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 0:00-0:03 | 六层金字塔总览图 | 展示 ASCII 金字塔图，逐层自上而下介绍 |
| 0:03-0:07 | 六层速览表 | 快速过表，每层一句话说明核心问题和代表工具 |
| 0:07-0:10 | Claude Code 在六层中的定位 | 重点讲解 Claude Code 横跨 Context/Harness/Loop/Graph 四层 |
| 0:10-0:13 | "Agent到底是什么？" | 结合六层体系给出完整定义 |
| 0:13-0:15 | 关键结论 + 过渡 | 总结 → 引出 KB2 对 Prompt 和 Context 的深入讲解 |

**关键要点**：
- 金字塔图是本节课的核心框架，确保学生能"看到"六层结构
- 强调"从底层 Prompt 到顶层 Graph，每层都建立在下层之上"
- Claude Code 定位必须讲清楚——它是贯穿多层的学习样本
- Agent 的定义要反复强化：不是单一技术，是六层整合的系统

**过渡到 KB2**：
聚焦到金字塔底层——Prompt Engineering（怎么和 AI 说话）和 Context Engineering（给 AI 看什么信息）。这两层是 ROI 最高、学习门槛最低的入口。

---

### KB2：Prompt + Context Engineering 深入（25分钟）

> **文件**：[KB2-Prompt与Context工程深入.md](KB2-Prompt与Context工程深入.md)
> **定位**：深度讲解金字塔底两层，建立"写好 Prompt"和"设计好上下文"的技术认知

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 0:15-0:22 | Prompt Engineering 深度解析 | Token预测原理 → 核心组件表（Role/Context/Task/Format/Constraints/Examples）→ 代表工具 → 企业视角 |
| 0:22-0:35 | Context Engineering 深度解析 | 上下文窗口管理原理 → 完整信息环境架构图 → 三大核心策略（压缩/选择/结构化）→ XML结构化示例 → 企业视角 |
| 0:35-0:40 | Prompt vs Context 对比 + 过渡 | 关系对比表 → 引出 KB3 |

**关键要点**：
- Token预测原理用"有Prompt vs 无Prompt"对比示例说明——直观
- 上下文信息环境架构图要展示清楚 6 个区块在 Context Window 中的分布
- 三大核心策略中，Compaction 最重要——直接关系到 Agent 会不会"失忆"
- XML 结构化示例要展示完整代码——这是可复用模式

**过渡到 KB3**：
Prompt 和 Context 解决了"AI 理解什么"的问题。但 AI 要真正"做事情"，需要一个运行时环境——这就是 Harness Engineering 和 Hermes Engineering。

---

### KB3：Harness + Hermes Engineering 深入（25分钟）

> **文件**：[KB3-Harness与Hermes工程深入.md](KB3-Harness与Hermes工程深入.md)
> **定位**：讲解 Agent 的"身体"（运行时基础设施）和"记忆"（长运行个人Agent）

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 0:40-0:47 | Harness Engineering 概念 + 裸Agent vs 完整Harness对比 | 展示裸Loop ~100行代码 vs 完整Harness 数千到数万行的对比图 |
| 0:47-0:55 | Harness 六大核心组件详解 | 逐组件讲解：Tool Registry、Permission Gate、Session Store、Context Compaction、Hook System、Trace/Log |
| 0:55-1:00 | Hermes Engineering 概念 + Harness vs Hermes 对比 | 传统Agent vs 长运行个人Agent 四个维度对比 |
| 1:00-1:05 | 企业视角总结 + 过渡 | Harness = Demo到生产的门槛；Hermes = 个人Agent的未来 |

**关键要点**：
- 裸 Agent Loop vs 完整 Harness 的对比图是最有冲击力的——强调"代码量差100倍"
- 六大组件中 Permission Gate 和 Context Compaction 最重要——关乎安全和成本
- Hermes 的"长期记忆"概念要讲透彻——跨会话/跨设备/跨应用
- 企业视角：Harness 是 2025 年新定义的学科，Claude Code 是最好学习样本

**过渡到 KB4**：
Harness 给了 Agent 身体，Hermes 给了它记忆。但 Agent 具体怎么思考？怎么编排复杂工作流？

---

### KB4：Loop + Graph Engineering 深入（20分钟）

> **文件**：[KB4-Loop与Graph工程深入.md](KB4-Loop与Graph工程深入.md)
> **定位**：讲解 Agent 的核心推理循环和工作流编排

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 1:05-1:10 | Loop Engineering 概念 + 标准 Agent Loop 流程图 | Observe→Think→Decide→Act→Feedback 五步循环 |
| 1:10-1:15 | Loop 关键参数 + 范式演进 | max_steps/timeout/retry 参数表；ReAct/Plan-Execute/Reflexion/ReWOO 对比 |
| 1:15-1:20 | Graph Engineering 概念 + Loop vs Graph 对比 | 线性循环 vs 有向图的对比；State/Node/Edge/Conditional Edge 核心概念 |
| 1:20-1:25 | 企业视角 + 上半部分总结 | Graph = 可审计的工作流；回顾六层金字塔全貌 |

**关键要点**：
- Loop 的五步循环图是理解 Agent 自主性的关键
- 四种 Loop 范式要对比讲清楚各自适用场景
- Graph 的条件分支图要展示完整——分支/并行/回退/暂停审批
- Checkpoint 概念必须强调——企业合规审计的刚需

**过渡到 KB5**：
上半部分建立了完整的六层技术栈认知。从 KB5 开始，回到最基础也最核心的一层——Prompt Engineering 实战。

---

### KB5：Prompt Engineering 实战详解（25分钟）

> **文件**：[KB5-Prompt工程实战详解.md](KB5-Prompt工程实战详解.md)
> **定位**：实操导向的 Prompt Engineering 教学——RCTE 框架 + 技巧大全 + 模板库

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 1:25-1:30 | Prompt Engineering 定义 + 基本概念 | 差的 Prompt vs 好的 Prompt 对比示例 |
| 1:30-1:38 | RCTE 框架详解 | 逐组件讲解 Role/Context/Task/Example，每个配表格和示例 |
| 1:38-1:42 | 常见 Prompt 技巧大全（8种） | 快速过技巧表，挑 3-4 个现场演示 |
| 1:42-1:48 | 四类任务的 Prompt 模板 | 写作/编程/分析/企业高管摘要，每类一个完整模板 |
| 1:48-1:50 | 8个优化技巧 + 过渡 | 优化前后对比表 |

**关键要点**：
- 差 Prompt vs 好 Prompt 的对比必须展示——让学生直观感受差距
- RCTE 框架是本节课最实用的知识点——反复强调"所有复杂 Prompt 都基于此"
- 四类任务模板要完整展示——学生可以直接复制使用
- 现场用至少 1 个 Prompt 演示 AI 输出效果

**过渡到 KB6**：
掌握了 Prompt 怎么写，下一步是搭建一个能让你高效使用 AI 的开发环境。

---

### KB6：VSCode + Claude + DeepSeek 环境搭建（25分钟）

> **文件**：[KB6-环境搭建实操.md](KB6-环境搭建实操.md)
> **定位**：动手搭建 AI 辅助开发环境

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 1:50-1:55 | 环境架构总览 | 展示 VSCode → Claude/DeepSeek → 项目 的架构图 |
| 1:55-2:02 | VSCode 安装 + 必装插件 | 引导安装 VSCode + Cline/Continue/Python 插件 |
| 2:02-2:08 | Cline 配置 Claude + DeepSeek API | 一步步引导配置两种 API Provider |
| 2:08-2:12 | Continue 双模型切换方案 + WorkBuddy 备选 | 配置 config.json；简单介绍 WorkBuddy |
| 2:12-2:15 | 验证环境 | 用 test_ai.py 验证环境配置成功 |

**关键要点**：
- 环境搭建是最容易卡住的环节——留出足够时间排错
- DeepSeek API 配置优先（国内直连 + 低成本），Claude API 作为高级选项
- 验证步骤必须全班一起做——Cline 生成代码 → Cline 执行代码
- 如果有学生卡在网络问题：跳过 Claude API，只用 DeepSeek

**过渡到 KB7**：
环境已就绪。现在将 Prompt Engineering 和环境结合起来，做一个实战项目：用 AI 安全操作数据库。

---

### KB7：MySQL数据库操作实操（35分钟）

> **文件**：[KB7-数据库操作实操.md](KB7-数据库操作实操.md)
> **定位**：完整的实操项目——通过 Prompt Engineering 让 AI 安全操作 MySQL

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 2:15-2:20 | 实操架构讲解 | 展示 You→Prompt→AI→SQL→MySQL 架构图 + 权限隔离设计 |
| 2:20-2:28 | MySQL 安装 + 测试数据导入 | 引导安装 MySQL + 执行 CREATE/INSERT 语句 + 创建权限隔离用户 |
| 2:28-2:35 | 代码讲解：ai_db_agent.py | 分段讲解 System Prompt 设计 + 核心函数 + 安全机制 |
| 2:35-2:45 | 运行与测试（4个测试用例） | 逐测试用例运行：简单查询→聚合统计→写操作确认→权限验证 |
| 2:45-2:50 | 关键原则总结 | 5条 Prompt Engineering 在数据库操作中的核心原则 |

**关键要点**：
- 权限隔离是核心安全概念——三层账户（ai_readonly/ai_writer/root）必须讲清楚
- System Prompt 的硬约束设计是重点——"绝不生成 DROP/TRUNCATE"
- 测试用例 4（权限验证）是高潮——两层保护同时生效的演示
- 如果 MySQL 安装大面积失败：教师投屏演示，学生看 + 课后补做

**过渡到 KB8**：
现在总结今天的内容，布置作业。

---

### KB8：课程总结与作业（10分钟）

> **文件**：[KB8-课程总结与作业.md](KB8-课程总结与作业.md)
> **定位**：收尾——巩固核心认知、明确作业要求、预告下次课

**时间线**：

| 时间段 | 内容 | 关键动作 |
|--------|------|----------|
| 2:50-2:54 | 核心回顾 | 六层金字塔快速回顾 + Prompt Engineering 核心要点（RCTE框架） |
| 2:54-2:56 | 六层体系速查表 | 快速过速查表（层级/核心问题/代表工具/企业成熟度） |
| 2:56-2:59 | 作业布置 | 作业1（RCTE实战）+ 作业2（环境搭建）+ 作业3（选做）+ 企业版作业 |
| 2:59-3:00 | 下次课预告 + 结束 | 下次课主题 + FAQ简要指引 |

**关键要点**：
- 10分钟收尾要快但不仓促
- 核心回顾聚焦"六层金字塔"和"RCTE框架"两个核心
- 作业截止时间强调：下次上课前一天 22:00
- 结束语强调：Prompt Engineering 是所有 AI 能力的基础——花再多时间打磨都值得

---

## 四、教学节奏控制指南

### 4.1 时间弹性策略

```
如果进度超前（讲得快）：
  → KB5 可以增加现场 Prompt 演示次数（多演示 2-3 个场景）
  → KB7 实操可以延长到 45 分钟（增加更多测试用例）
  → 鼓励学生在课堂上用 Cline 完成更多编程任务
  → KB8 可以穿插现场 Q&A（回答学生的实际问题）

如果进度落后（讲得慢）：
  → KB2+KB3+KB4（六层详解）每一层压缩 2-3 分钟
  → KB3 的 Hermes Engineering 可以压缩到 3 分钟（仅过概念和对比表）
  → KB6 的环境搭建改为"教师投屏演示 + 学生课后完成"
  → KB7 如果 MySQL 安装大面积失败 → 教师投屏演示 + 课后补做
  → KB5 的 8 个优化技巧改为快速过表（压缩到 2 分钟）
```

### 4.2 节奏节奏点

| 时间点 | 学生可能的状界 | 应对策略 |
|--------|---------------|----------|
| KB1 (0-15min) | 新鲜、好奇、"六层是什么" | 用金字塔图建立整体认知，节奏中等偏快 |
| KB2 (15-40min) | 注意力集中——Prompt 是核心话题 | 技术讲解要清晰，"Token预测"原理用对比示例讲透 |
| KB3 (40-65min) | 注意力可能开始下滑——Harness/Hermes 较抽象 | 用"裸Agent vs 完整Harness"对比制造冲击感 |
| KB4 (65-85min) | 逐渐疲劳——Loop/Graph 概念密集 | 流程图要直观，关键参数表快速过 |
| KB5 (85-110min) | 注意力回升——实战内容，实用性强 | 现场演示 Prompt 效果，保持互动感 |
| KB6 (110-135min) | 活跃、动手意愿强 | 一步步引导，走动帮助卡住的学生 |
| KB7 (135-170min) | 高度投入——数据库操作是完整项目 | 重点讲解安全机制，引导学生思考"为什么这样设计" |
| KB8 (170-180min) | 疲惫但有成就感 | 收尾果断，作业明确，结束语有力 |

### 4.3 过渡衔接质量

每次 KB 之间的过渡是串联整堂课的线。确保每个过渡都自然、有悬念、有逻辑关联：

- **KB1→KB2**："从金字塔底层开始——Prompt 和 Context"
- **KB2→KB3**："AI 理解了任务和信息，还需要'身体'来执行——Harness"
- **KB3→KB4**："有了身体和记忆，AI 怎么思考？怎么编排复杂流程？"
- **KB4→KB5**："建立完整认知后，回到最核心的一层：Prompt Engineering 实战"
- **KB5→KB6**："Prompt 写好了，需要一个高效的开发环境来承载"
- **KB6→KB7**："环境和工具就绪，做一个完整项目：AI 操作数据库"
- **KB7→KB8**："总结今天的核心——六层体系 + Prompt Engineering 实战"

---

## 五、教师备课清单

### 上课前一天

- [ ] 通读所有 8 个 KB 文档（约 1.5 小时）
- [ ] 确认 Claude/DeepSeek/ChatGPT 账号正常使用
- [ ] 确认 VSCode + Cline 插件工作正常
- [ ] 确认本地 MySQL 安装并导入测试数据
- [ ] 在教室电脑上测试网络、投影、IDE、数据库连接
- [ ] 准备故障预案：网络中断 → DeepSeek 直连；IDE故障 → 网页版 AI
- [ ] 在课程群里发课前准备提醒

### 上课前30分钟

- [ ] 到达教室
- [ ] 打开本总控文档
- [ ] 打开 KB1 文档
- [ ] 在浏览器中登录 Claude、DeepSeek、ChatGPT
- [ ] 打开 VSCode + Cline（确认 API 连接正常）
- [ ] 打开终端，确认 MySQL 连接正常
- [ ] 检查投影/屏幕共享

### 下课后

- [ ] 在课程群里确认作业要求和截止时间
- [ ] 上传本次课的 KB 文档到课程群文件
- [ ] 记录教学中遇到的问题（环境配置卡点、学生疑问等）
- [ ] 统计未完成环境搭建的学生，课后单独辅导

---

## 六、常见教学问题预案

### 问题1：学生无法安装 MySQL

**应对**：
- 优先方案：检查是否有 Docker，用 `docker run mysql` 替代
- 备选方案：使用 SQLite 替代（修改代码中连接配置）
- 最终方案：教师投屏演示，学生看 + 理解代码逻辑 + 课后补装

### 问题2：学生没有 API Key（Claude/DeepSeek）

**应对**：
- DeepSeek API Key 申请流程简单，课上花 2 分钟统一申请（platform.deepseek.com）
- Claude API Key 需要海外手机号 → 不强求，用 DeepSeek 替代
- 如果全班无 API Key：改用 VSCode + Continue 的免费模型选项

### 问题3：学生对六层体系感到 overwhelm

**应对**：
- 明确分层目标：零基础学生重点掌握 Prompt + Context 两层即可
- 六层体系是"全景地图"——不需要记住全部细节，知道"有什么"即可
- 金字塔比喻：每层建立在下层之上，学会第一层就能解决 80% 的问题

### 问题4：Cline 插件无法安装/不可用

**应对**：
- 备选：Continue 插件（开源免费，不需要 API Key 也能用免费模型）
- 最终备选：直接用浏览器版 Claude/ChatGPT + 手动复制代码
- 核心教学目标不变：AI 辅助编程的 workflow 理解

---

## 七、附录：本课文件结构

```
讲义/第1周/Prompt-Engineering/
├── README.md                          ← 本文件（教学总控文档）
├── KB1-六层AI工程体系概览.md           ← 15分钟
├── KB2-Prompt与Context工程深入.md      ← 25分钟
├── KB3-Harness与Hermes工程深入.md      ← 25分钟
├── KB4-Loop与Graph工程深入.md          ← 20分钟
├── KB5-Prompt工程实战详解.md           ← 25分钟
├── KB6-环境搭建实操.md                ← 25分钟
├── KB7-数据库操作实操.md              ← 35分钟
└── KB8-课程总结与作业.md              ← 10分钟
```

---

> **本课核心记忆点**：六层AI工程金字塔（Prompt→Context→Harness→Hermes→Loop→Graph）+ RCTE Prompt框架（Role/Context/Task/Example）。
>
> **学生课后应能回答**：Agent 是什么？Prompt Engineering 的核心框架是什么？Context Engineering 的三大策略是什么？
