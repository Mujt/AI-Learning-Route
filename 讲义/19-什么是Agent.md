# 第7周 第1课：什么是 Agent

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **周次** | 第7周 |
| **课序** | 第1课（共3课） |
| **课程主题** | 什么是 Agent |
| **课时** | 2小时（50分钟讲解 + 70分钟实操） |
| **课程类型** | 核心理论课 |
| **前置知识** | Python基础、LLM API调用基础 |
| **后续课程** | 第2课 LangChain/LangGraph、第3课 MCP |

> 这是整个8周课程中**最重要的一课**。学生能否真正理解"Agent是什么"，决定了他们后续所有学习的高度。本节课没有复杂代码，重点是建立清晰的概念框架。务必确保每位学生在离开教室时，能够用自己的话说出 Agent 和聊天机器人的本质区别。

---

## 二、学习目标

完成本课后，学生应能够：

1. **清晰区分** Chatbot、Workflow、Agent 三种形态，说出每种形态的核心特征和适用场景
2. **背诵并解释** Agent 四能力模型（感知、推理、规划、执行），并能用实例说明每个阶段的具体行为
3. **画出并讲解** Agent 核心循环的执行流程，理解每一步的输入输出
4. **理解** Context Engineering（上下文工程）的六大要素，知道"好的上下文设计"与"差的上下文设计"的区别
5. **理解** Harness Engineering（根基工程）的概念，能说出 Agent Harness 的六大核心组件
6. **做出判断**：面对一个具体任务，能判断是否应该使用 Agent，并给出理由
7. **引用** Anthropic "Building effective agents" 的核心观点来解释 Agent 的设计原则

---

## 三、课前准备

### 教师准备

- [ ] 熟读 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（本课最重要的参考文献）
- [ ] 准备好 Python 环境（deepseek-chat 或其他支持 Function Calling 的模型 API Key）
- [ ] 安装好 `openai` Python 包（用于调用兼容 OpenAI API 的模型）
- [ ] 准备一个"帮我规划一次北京三日游"的演示案例（课上多次用同一个例子贯穿讲解）
- [ ] 阅读 [Anthropic: What is an Agent?](https://docs.anthropic.com/en/docs/agents-and-tools/agent-overview) 补充背景

### 学生准备

- [ ] 确保已安装 `openai` 包：`pip install openai`
- [ ] 准备好 DeepSeek API Key（或任意支持 Function Calling 的模型）
- [ ] 回顾第6周的 API 调用知识（特别是如何创建 chat completion）
- [ ] 思考一个问题："你觉得聊天机器人'聪明'吗？它有什么做不了的事？"（带着这个问题来上课）

---

## 四、核心知识点详解

### 4.1 Chatbot → Workflow → Agent 的演进之路

理解 Agent，首先必须理解它不是什么。我们通过三个层次来建立认知。

---

#### 4.1.1 第一层：Chatbot（聊天机器人）

**本质定义**：一个搭载了大语言模型（LLM）的对话系统。

**执行流程**：

```
用户输入文字 → LLM 处理 → 生成文字回复
```

**核心特征**：

- **一问一答**：每次对话是独立的请求-响应周期
- **没有工具**：只能"说"，不能"做"。Chatbot 无法查天气、无法发邮件、无法读文件
- **没有状态**：不记得你上次说过什么（同一会话内的上下文除外）
- **输出即终点**：回复完就结束了，不会主动继续

**类比理解**：Chatbot 像一个知识渊博但被困在房间里的人。他可以回答你任何问题，但无法走出房间去查看外面的世界，也无法操作房间外的任何东西。他所有的"知识"都来自训练数据，截止于某个时间点。

**具体例子**：

你问：*"帮我规划一次北京三日游。"*

Chatbot 回复（基于训练数据中的通用知识）：

> 建议行程：
> 第一天：天安门广场 → 故宫 → 景山公园
> 第二天：八达岭长城 → 鸟巢水立方
> 第三天：颐和园 → 圆明园 → 清华大学
>
> 建议住在市中心地铁附近，方便出行。北京秋季最佳，天气凉爽宜人。

**问题在哪？** 这个回复看起来不错，但它：
- 不知道你现在在哪（没有查你的位置）
- 不知道你什么时候有空（没有查你的日历）
- 不知道机票酒店的实际价格（没有搜索实时数据）
- 不知道你去的那几天北京天气怎么样（没有查天气预报）
- 不能帮你实际预订任何东西（没有执行能力）

这就是 Chatbot 的**天花板**：它只能说，不能做。

---

#### 4.1.2 第二层：Workflow（工作流）

**本质定义**：将多个处理步骤按固定顺序串联起来的自动化流程。

**执行流程**：

```
用户输入 → [步骤1] → [步骤2] → [步骤3] → ... → 最终输出
```

**核心特征**：

- **流程固定**：步骤的先后顺序是预先定义好的，每次执行一样
- **可预测**：相同的输入大概率产生相同的输出
- **有条件分支**：可以在预设的路径中选择，但路径本身是提前设计好的
- **适合标准化任务**：比如审批流程、数据 ETL、报告生成

**类比理解**：Workflow 像一条工厂流水线。每个工位做固定的事，原料从一端进去，成品从另一端出来。效率高、质量稳定，但无法处理流水线设计之外的意外情况。

**对比 Chatbot**：

| 维度 | Chatbot | Workflow |
|------|---------|----------|
| 结构 | 单步：输入→输出 | 多步：输入→步骤1→步骤2→...→输出 |
| 灵活性 | 高（什么都能聊） | 低（只能按预设路径走） |
| 可预测性 | 低（回答可能不同） | 高（结果稳定） |
| 工具调用 | 无 | 可以有（在固定步骤中调用） |
| 决策能力 | 无（随机性而非决策） | 有限（条件分支） |

**具体例子**：

用 Workflow 实现"规划北京三日游"：

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 获取用户  │ → │ 查询机票  │ → │ 查询酒店  │ → │ 生成行程  │
│ 出发城市  │    │ 价格     │    │ 价格     │    │ 方案     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

这里有 4 个固定步骤，每次执行都按这个顺序。如果用户在最后说"等等，我不要住酒店，我想住民宿"，Workflow 需要重新从头开始跑一遍，甚至因为民宿不在预定义的步骤中而无法处理。

Workflow 比 Chatbot 进了一步：它能"做事"了（调用 API 查数据）。但它仍然**僵硬**：步骤是死的，不会根据中间结果调整策略。

---

#### 4.1.3 第三层：Agent（智能体）

**本质定义**：一个能够自主感知环境、推理分析、制定计划、调用工具执行，并根据执行结果动态调整策略的 AI 系统。

**执行流程**：

```
用户输入 → 理解意图 → 制定计划 → 选择工具 → 调用执行 → 
观察结果 → 分析结果 → 调整计划 → 再次执行 → ... → 完成任务
```

**核心特征**：

- **自主决策**：Agent 自己决定下一步做什么，而非遵循预设流程
- **动态调整**：根据中间结果改变策略。机票太贵？换高铁。酒店满了？换民宿
- **工具使用**：主动选择和调用工具（搜索、计算、API、数据库、文件系统等）
- **有记忆**：记住之前做了什么，结果是什么，为什么做了那个决定
- **目标导向**：围绕用户的目标来组织行动，而不是简单回答问题

**类比理解**：Agent 像一个真正的"旅行管家"。你告诉他想去北京玩三天，他会：
1. 先问你的偏好和预算
2. 查你的日历找空闲时间
3. 搜机票和火车票，对比价格
4. 查目的地的天气
5. 根据天气建议合适的活动和衣物
6. 搜酒店，对比位置和价格
7. 发现某天有雨，建议把室内活动调到那天
8. 最终给出一个**基于实时数据、考虑了你的偏好和约束的**完整行程
9. 需要时可以直接帮你预订

**完整对比表——六个维度看三种形态**：

| 维度 | Chatbot | Workflow | Agent |
|------|---------|----------|-------|
| **工具使用** | 无工具，纯文本交流 | 可有工具，但调用位置固定 | 自主选择和组合工具，动态调用 |
| **记忆能力** | 仅当前对话上下文 | 通常无跨步骤记忆 | 短期+长期记忆，记住历史决策和结果 |
| **决策方式** | 无决策，直接生成文本 | 预设条件分支（if-else） | 自主推理决策，考虑多种因素 |
| **适应性** | 零：无法适应新情况 | 低：需要人工添加/修改步骤 | 高：自动根据反馈调整计划和策略 |
| **任务复杂度** | 简单问答、闲聊 | 中等：标准化多步骤任务 | 高：开放式、多路径、不确定任务 |
| **典型场景** | 客服问答、知识查询 | 审批流程、定时报告、数据ETL | 旅行规划、代码开发、研究分析、个人助手 |

---

#### 4.1.4 同一个任务，三种形态的完整对比

以"帮我规划一次北京三日游"为例，展示三种形态在实际中的差异：

**Chatbot 的做法**：

给出基于训练数据的通用建议，看起来"正确"但脱离实际——不知道你的位置、时间、预算，给的是"最安全"的回答。如果你追问"那现在机票多少钱"，它会说"我无法获取实时数据"。

**Workflow 的做法**：

按预设顺序执行：查出发地→查机票→查酒店→生成行程。如果你中途说"我不想坐飞机"，它无法中途改变，因为"交通方式"这个变量在流程设计时就固定了。

**Agent 的做法**：

```
用户: 帮我规划一次北京三日游。

Agent 思考: 需要知道出发城市、时间、预算、偏好。先询问缺失信息。

Agent: 好的！我先了解几个信息：
1. 你从哪个城市出发？
2. 大概什么时间去？

用户: 从上海出发，下周五出发。

Agent 思考: 下周五是11月15日。需要查机票、高铁、天气、酒店。先并行查机票和高铁。

Agent 调用工具:
- search_flights(from="上海", to="北京", date="2025-11-15")
- search_trains(from="上海", to="北京", date="2025-11-15")
- get_weather(city="北京", date="2025-11-15")

工具返回:
- 机票: 680元(经济舱), 飞行2h30m
- 高铁: 550元(二等座), 4h28m
- 天气: 周五晴, 2-12°C; 周六阴, 0-8°C; 周日小雨, 1-6°C

Agent 思考: 机票比高铁只贵130元但节省2小时，推荐机票。天气偏冷，
周日有小雨。现在查酒店。

Agent 调用工具:
- search_hotels(city="北京", check_in="2025-11-15", check_out="2025-11-18")
- search_attractions(city="北京", top=10)

工具返回:
- 酒店: 经济型300-500元, 舒适型500-800元, 豪华型1000+
- 景点: 故宫80元, 长城45元, 颐和园30元...

Agent 思考: 周日有雨，应该把室内活动(故宫、博物馆)安排在周日。
周五到达后可以先去天安门和景山。周六天阴但没雨，可以去长城。

Agent: 根据你的情况，我建议如下行程：

🗓 **周五 11月15日**（晴，2-12°C）
   上午：上海→北京 推荐航班MU5101，10:00-12:30（¥680）
   下午：酒店入住后，游览天安门广场+景山公园（看故宫全景）
   晚上：王府井步行街

🗓 **周六 11月16日**（阴，0-8°C）
   全天：八达岭长城（穿厚外套！）- 建议早点出发避开人流
   晚上：鸟巢水立方夜景

🗓 **周日 11月17日**（小雨，1-6°C）
   室内为主：故宫博物院（需提前预约！）→ 国家博物馆
   下午：根据返程时间安排

💡 **预算估算**：交通¥1360 + 住宿3晚约¥1200-2400 + 餐饮门票约¥800 = 总计约¥3400-4600

需要我帮你预订机票和酒店吗？
```

**关键差异一目了然**：
- Chatbot：给了通用回答，没有任何实际行动
- Workflow：按固定流程走，不会因为天气调整行程
- Agent：根据实时数据（天气、价格）动态调整计划，考虑了室外/室内活动的搭配，甚至提醒了"故宫需要预约"

这就是 Agent 的核心价值：**不是让你知道更多，而是帮你做到更多。**

---

### 4.2 Agent 四能力模型（Agent Core Capability Framework）

理解 Agent 的工作原理，最核心的框架是四能力模型。这四个能力形成一个闭环，Agent 在其中不断循环直到任务完成。

```
                    ┌──────────────────────┐
                    │                      │
                    │   1. 感知 Perceive    │
                    │   理解用户意图        │
                    │   感知环境状态        │
                    │                      │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │                      │
                    │   2. 推理 Reason      │
                    │   分析信息            │
                    │   做出判断            │
                    │   评估置信度          │
                    │                      │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │                      │
                    │   3. 规划 Plan        │
                    │   分解任务            │
                    │   制定步骤            │
                    │   准备备选方案         │
                    │                      │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │                      │
                    │   4. 执行 Act         │
                    │   选择工具            │
                    │   构建参数            │
                    │   解读结果            │
                    │                      │
                    └──────────┬───────────┘
                               │
                               ↓
                    观察执行结果，回到感知
                    （新一轮循环开始）
```

---

#### 4.2.1 感知（Perceive）——"我在哪，用户想要什么？"

感知是 Agent 的"眼睛和耳朵"。在这一阶段，Agent 需要理解两件事：

**a) 用户意图**

- 用户真正想要完成什么？不只是字面意思，而是深层目标
- 用户说了什么，更重要的是用户没说什么（缺失的关键信息）
- 用户的优先级和约束条件是什么

**b) 环境状态**

- 当前对话的上下文（之前聊了什么，做了什么）
- 已有的信息（查到了什么数据，得到了什么结果）
- 工具返回的结果意味着什么

**以旅行规划为例**：

| 感知内容 | 具体体现 |
|----------|----------|
| 用户意图 | "规划北京三日游"——底层需求是：一个可行、具体、考虑了各种约束的旅行方案 |
| 缺失信息 | 出发地？时间？预算？偏好？——这些都是制定计划必需的 |
| 环境感知 | 刚才查了机票680元，高铁550元——有了比较基准 |
| 结果解读 | 天气预报说周日有雨——这意味着周日不适合户外活动 |

**技术实现**：
- 用户输入经 LLM 解析为结构化的意图和槽位（slot filling）
- 工具调用结果被解析为 Agent 可理解的状态描述
- 上下文管理：哪些信息重要？哪些可以丢弃？

---

#### 4.2.2 推理（Reason）——"这意味着什么？我该怎么办？"

推理是 Agent 的"大脑"。感知到信息后，Agent 需要对这些信息进行分析、关联和判断。

**推理的四个层次**：

| 层次 | 说明 | 示例 |
|------|------|------|
| **因果推理** | 理解因果关系 | "因为周日有雨，所以户外活动应该安排在周五和周六" |
| **对比推理** | 比较不同选项的优劣 | "机票680元2.5小时 vs 高铁550元4.5小时：多花130元省2小时，大部分人会选机票" |
| **风险评估** | 判断不确定性和风险 | "故宫门票需要提前预约，如果现在不提醒用户，到时可能买不到票" |
| **置信度评估** | 判断信息的可靠程度 | "天气预报是3天前的预测，准确率约80%，需要提醒用户关注更新" |

**以旅行规划为例的推理过程**：

```
已知信息:
- 出发地: 上海，日期: 11月15日
- 天气: 周五晴、周六阴、周日小雨
- 机票: 680元，高铁: 550元
- 故宫门票: 需要预约

推理过程:
1. 交通选择: 机票只贵130元，节省2小时 → 推荐机票
2. 行程安排: 周日有雨 → 故宫(室内)调到周日 → 长城(户外)安排在周六
3. 风险评估: 故宫门票紧俏 → 必须提醒用户提前预约
4. 衣着建议: 气温0-12°C → 厚外套必备，尤其长城风大
```

**关键认知**：推理能力是 Agent 区别于 Workflow 的核心。Workflow 不"推理"，它只是按预设路径执行。Agent 面对的是**开放式的决策空间**，它必须在多种可能的行动中做出选择。

---

#### 4.2.3 规划（Plan）——"我分几步走？先做什么？"

规划是将推理的结论转化为可执行的行动序列。

**规划的关键要素**：

| 要素 | 说明 | 示例 |
|------|------|------|
| **任务分解** | 把大任务拆成小步骤 | "规划三日游" → 查交通、查天气、查酒店、排行程、出预算 |
| **步骤排序** | 确定先后次序 | 先查天气（影响行程安排）→ 再排行程（基于天气） |
| **依赖关系** | 哪些步骤可以并行，哪些必须串行 | 机票和天气可以并行查（无依赖），但排行程依赖于天气结果 |
| **备选方案** | 如果某步失败了怎么办 | 如果机票售罄 → 查高铁；如果经济型酒店满房 → 查舒适型 |
| **资源预估** | 大概需要多少步骤、多少时间 | 预计5-8步，需要查3个API |

**以旅行规划为例的规划**：

```
第1轮规划（初始计划）:
Step 1: 并行查询 ①机票 ②高铁 ③天气（三者无依赖）
Step 2: 比较交通方式，和用户确认选择
Step 3: 查询酒店
Step 4: 查询景点信息
Step 5: 综合所有信息，生成行程方案
Step 6: 和用户确认
Step 7: 如有需要，帮用户预订

执行完 Step 1 后，Agent 发现天气不好 → 调整规划：

第2轮规划（调整后）:
Step 3': 筛选适合雨天的室内景点（新增需求）
Step 4': 将室内活动排到周日，室外活动排到周五六
Step 5': 提醒用户带雨具和厚外套
```

**关键认知**：规划不是"一次性"的。Agent 的规划是**动态的、持续调整的**。每执行一步，拿到新的信息，就重新评估和调整后续计划。这才是 Agent 真正的"智能"所在。

---

#### 4.2.4 执行（Act）——"选什么工具？传什么参数？结果怎么说？"

执行是 Agent 的"手脚"。规划好的步骤需要通过工具来落地。

**执行的三个关键决策**：

| 决策 | 说明 | 示例 |
|------|------|------|
| **工具选择** | 当前这一步需要哪个工具？ | 查天气 → `get_weather` 函数 |
| **参数构建** | 传给工具什么参数？ | `get_weather(city="北京", date="2025-11-15")` |
| **结果解读** | 工具返回的数据说明什么？ | 温度2-12°C、周日小雨 → 需要保暖和雨具 |

**工具调用的完整生命周期**：

```
1. Agent 决定: "我需要知道北京的天气"
2. 选择工具: get_weather
3. 构建参数: {"city": "北京", "date": "2025-11-15"}
4. 调用执行: function_call → API/函数 → 返回数据
5. 解读结果: "周五晴、周六阴、周日小雨，气温0-12°C"
6. 更新状态: 将结果存入Agent的记忆
7. 继续循环: 回到"感知"阶段，基于新信息推理和规划
```

**工具调用的常见错误和 Agent 如何处理**：

| 错误类型 | 示例 | Agent 的处理 |
|----------|------|-------------|
| 工具不可用 | API 挂了 | 换一个工具/备选方案 |
| 参数错误 | 城市名拼错了 | 修正参数后重试 |
| 结果为空 | 查不到航班 | 换交通工具（查高铁） |
| 结果异常 | 机票显示99999元 | 质疑结果，换一个数据源验证 |

---

#### 4.2.5 四能力的循环关系

这四个能力不是线性的一二三四，而是一个**持续循环**：

```
感知 → 推理 → 规划 → 执行 → 感知 → 推理 → 规划 → 执行 → ...
  ↑                            ↓
  └──── 观察执行结果，获得新信息 ─┘
```

**一次完整循环的旅行规划示例**：

| 循环 | 感知 | 推理 | 规划 | 执行 |
|------|------|------|------|------|
| 第1轮 | 用户想去北京玩三天 | 需要更多信息 | 先问缺失信息 | 向用户提问 |
| 第2轮 | 用户说从上海出发，下周五 | 日期确定，开始查数据 | 并行查机票/高铁/天气 | 调用3个API |
| 第3轮 | 天气周日有雨，机票680元 | 周日不适合户外，机票价格合理 | 室内活动排周日 | 查酒店 |
| 第4轮 | 酒店价格300-1000元 | 需要确认用户预算 | 向用户确认预算 | 向用户提问 |
| ... | ... | ... | ... | ... |
| 最后一轮 | 所有信息就绪 | 方案完整可行 | 输出最终行程 | 生成完整回复 |

---

### 4.3 Agent 核心循环（The Agent Loop）

如果说四能力模型是 Agent 的"解剖学"（静态结构），那核心循环就是 Agent 的"生理学"（动态运行）。

#### 4.3.1 伪代码

```
def agent_loop(user_input, max_steps=10, timeout=300):
    """
    Agent 核心循环
    - max_steps: 最大执行步数（防止无限循环）
    - timeout: 超时时间（秒）
    """
    # 初始化
    messages = [{"role": "user", "content": user_input}]
    step = 0
    start_time = time.time()
    
    while step < max_steps:
        # 超时检查
        if time.time() - start_time > timeout:
            return "任务超时，Agent 停止执行"
        
        step += 1
        
        # ===== 1. 观察 (Observe) =====
        # 当前状态 = 对话历史 + 所有工具调用结果
        current_state = messages
        
        # ===== 2. 思考 (Think) =====
        # 让 LLM 分析当前状态，决定下一步
        response = llm.chat(
            messages=current_state,
            tools=available_tools  # 告诉模型有哪些工具可用
        )
        
        # ===== 3. 决策 (Decide) =====
        if response.has_tool_calls():
            # 需要调用工具 → 执行工具
            for tool_call in response.tool_calls:
                # 安全检查（可选）
                if tool_call.is_dangerous():
                    if not ask_human_approval(tool_call):
                        messages.append({"role": "tool", "content": "用户拒绝了此操作"})
                        continue
                
                # ===== 4. 执行 (Act) =====
                result = execute_tool(
                    name=tool_call.function.name,
                    arguments=tool_call.function.arguments
                )
                
                # ===== 5. 反馈 (Feedback) =====
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
                
                # 回到循环开头，基于新信息继续思考
        
        else:
            # 没有工具调用 → Agent 认为任务完成
            return response.content
    
    return "达到最大步数限制，请简化任务后重试"
```

---

#### 4.3.2 一步步追踪 Agent 的实际执行过程

以下是一次真实 Agent 调用的完整 trace，任务为：**"帮我查看现在的时间，然后在当前目录搜索所有 Markdown 文件，最后设置一个下午3点的提醒'交Agent作业'。"**

```
═══════════════════════════════════════════════════════
Step 1/5
═══════════════════════════════════════════════════════
【当前状态】
  用户输入: "帮我查看现在的时间，然后在当前目录搜索所有
            Markdown文件，最后设置一个下午3点提醒'交Agent作业'"

【LLM思考】
  "用户有三个任务：1) 查时间 2) 搜文件 3) 设提醒。
   我需要分步执行。先从查时间开始，因为这个不需要参数。"

【行动决策】
  调用工具: get_current_time()
  参数: 无

【工具执行】
  工具返回: "2026-07-26 14:32:15"

═══════════════════════════════════════════════════════
Step 2/5
═══════════════════════════════════════════════════════
【当前状态】
  用户输入 + [工具结果: 当前时间 2026-07-26 14:32:15]

【LLM思考】
  "已获取时间。接下来搜索 Markdown 文件。当前目录不确定，
   先用当前目录搜索所有 .md 文件。"

【行动决策】
  调用工具: search_file(pattern="*.md", directory=".")
  参数: {"pattern": "*.md", "directory": "."}

【工具执行】
  工具返回: ["README.md", "notes.md", "讲义/19-什么是Agent.md"]

═══════════════════════════════════════════════════════
Step 3/5
═══════════════════════════════════════════════════════
【当前状态】
  用户输入 + [时间: 14:32:15] + [文件: README.md, notes.md, ...]

【LLM思考】
  "时间和文件都已获取。最后一个任务是设置提醒。
   现在时间是14:32，用户说下午3点，就是15:00。"

【行动决策】
  调用工具: create_reminder(task="交Agent作业", time_str="15:00")
  参数: {"task": "交Agent作业", "time_str": "15:00"}

【工具执行】
  工具返回: "✅ 已创建提醒：'交Agent作业' - 15:00"

═══════════════════════════════════════════════════════
Step 4/5
═══════════════════════════════════════════════════════
【当前状态】
  用户输入 + [时间: 14:32:15] + [3个md文件] + [提醒已创建]

【LLM思考】
  "三个任务全部完成：时间拿到了、文件搜到了、提醒设好了。
   现在可以汇总所有结果给用户。"

【行动决策】
  不调用工具，直接生成最终回复

【最终输出】
  "已经帮你完成了以下任务：
  
  1️⃣ **当前时间**：2026年7月26日 14:32:15
  
  2️⃣ **当前目录的 Markdown 文件**：
     - README.md
     - notes.md
     - 讲义/19-什么是Agent.md
  
  3️⃣ **提醒已设置**：今天下午3点——「交Agent作业」
  
  现在距离提醒时间还有约28分钟，抓紧时间完成作业哦！"

═══════════════════════════════════════════════════════
任务完成！总共执行 3 个步骤，调用了 3 个工具。
═══════════════════════════════════════════════════════
```

---

#### 4.3.3 核心循环中的关键机制

**a) 最大步数限制 (max_steps)**

防止 Agent 陷入无限循环。如果 Agent 一直调工具、一直不满意结果、一直重试，max_steps 是最后的安全阀。典型设置：5-15步。

```python
if step >= max_steps:
    return f"任务在{max_steps}步后仍未完成。当前进度：{summarize_progress()}"
```

**b) 超时控制 (timeout)**

防止单次工具调用耗时过长。例如调用外部 API 迟迟不返回，Agent 应该有超时处理。

```python
try:
    result = tool_function(**args, timeout=30)
except TimeoutError:
    result = "工具调用超时，请尝试简化请求或稍后重试"
```

**c) 错误处理**

工具调用可能失败（网络问题、参数错误、权限不足等）。Agent 必须能处理这些异常：

```python
try:
    result = tool_function(**args)
except Exception as e:
    result = f"工具调用失败：{e}。Agent 将尝试备选方案。"
    # Agent 收到这个错误信息后，可以决定换一个工具
    # 或者询问用户怎么处理
```

**d) 人工介入检查点 (Human-in-the-Loop)**

对于高风险操作（删除文件、发送邮件、转账、发布内容），Agent 应该在执行前暂停，请求人类确认。

```python
dangerous_operations = ["delete_file", "send_email", "publish_post", "transfer_money"]

if tool_call.function.name in dangerous_operations:
    print(f"⚠️ Agent 想执行: {tool_call.function.name}")
    print(f"   参数: {tool_call.function.arguments}")
    approval = input("是否批准？(y/n): ")
    if approval.lower() != 'y':
        continue  # 跳过这个工具调用
```

这就是 Anthropic "Building effective agents" 中强调的核心原则之一：**在工具和用户之间保持适当的摩擦（friction）——让高风险操作需要明确的用户确认。**

---

### 4.4 Agent vs Chatbot：本质区别

这是本课最重要的"顿悟时刻"（Aha Moment）。学生必须理解：Agent 不是 Chatbot 的加强版，而是一种**本质不同的系统架构**。

#### 4.4.1 结构对比

**Chatbot 的架构**：

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  用户输入  │ ──→ │   LLM    │ ──→ │  文本输出  │
└──────────┘     └──────────┘     └──────────┘
```

最简单的架构。只有三个组件。LLM 就是一切。

**Agent 的架构**：

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  用户输入  │ ──→ │  Agent   │ ──→ │  Tool 1  │ ──→ │          │
│  (目标)   │     │  Core    │     │  Tool 2  │     │  最终输出  │
└──────────┘     │  Loop    │     │  Tool 3  │     │  (成果)   │
                 │          │     │  ...     │     │          │
                 └────┬─────┘     └──────────┘     └──────────┘
                      │
                 ┌────┴─────┐
                 │  Memory   │
                 │  记忆系统  │
                 └──────────┘
```

Agent 多出了关键的组件：Core Loop（决策循环）、Tools（工具系统）、Memory（记忆系统）。LLM 从"全部"变成了"核心引擎"之一。

#### 4.4.2 一句话区分

> Chatbot 只能回答你的问题。Agent 能帮你**完成**你的任务。

或者更精炼：

> Chatbot = 知道很多，什么都说。
> Agent = 做得多，说得少，但结果实打实。

#### 4.4.3 关键洞察：Agent "做"事，Chatbot 只"说"话

用一个最直观的对比：

| 任务 | Chatbot 的表现 | Agent 的表现 |
|------|---------------|-------------|
| "帮我发一封邮件给团队" | 写好邮件草稿，告诉你去哪里发 | 写好草稿，调用Gmail API，**真的发出去了**（经过你确认） |
| "帮我整理桌面文件" | 告诉你整理文件的方法 | 调用文件系统API，**真的帮你分类整理了** |
| "帮我分析这份数据" | 告诉你怎么分析 | 写Python代码→执行→生成图表→**给你图表文件** |
| "帮我订一张机票" | 告诉你去哪里订、怎么订 | 搜索航班→对比价格→**帮你下单**（等你确认支付） |

**Agent 跨过了那道"从说到做"的鸿沟。**

---

### 4.5 Agent 的上下文工程（Context Engineering）

> 如果说 Prompt Engineering 解决的是"如何给 AI 下一个好指令"，那么 **Context Engineering 解决的是"如何给 AI 一个好环境"**。它是 Agent 工程中最容易被忽视、却又决定成败的关键环节。

#### 4.5.1 什么是 Context Engineering？

**定义**：Context Engineering（上下文工程）是设计和管理 Agent 在执行任务过程中所能"看到"的所有信息的工程实践。它决定了模型在每一步推理时拥有什么样的信息基础。

```
Prompt Engineering:                   Context Engineering:
  "你是一个优秀的助手..."               ┌────────────────────────────┐
  关注：指令怎么写                      │ System Prompt（角色+规则）    │
                                       │ 对话历史（本次会话上下文）     │
                                       │ 工具定义（可用工具的描述）     │
                                       │ 工具返回结果（上一步的输出）   │
                                       │ 检索到的文档（RAG 结果）      │
                                       │ 记忆提取（长期记忆中的相关项） │
                                       │ 用户偏好（个性化设置）        │
                                       └────────────────────────────┘
                                       关注：给模型看什么、看多少、怎么看
```

> 💡 **一句话理解**：Prompt Engineering 编写"台词"，Context Engineering 搭建"舞台"。

#### 4.5.2 Context Engineering 的六大要素

| 要素 | 说明 | 为什么重要 | 典型问题 |
|------|------|-----------|----------|
| **系统提示词（System Prompt）** | 设定 Agent 的角色、规则、行为边界 | Agent 的"宪法"，决定能做什么、不能做什么 | 太长 → 模型忽略规则；太短 → 约束不够 |
| **对话历史（Conversation History）** | 当前会话的所有来往消息 | 提供连贯的交互上下文 | 多轮对话后历史过长，超过上下文窗口 |
| **工具定义（Tool Definitions）** | 所有可用工具的名称、描述、参数 Schema | 模型需要精确定义才知道何时、如何调用工具 | 工具太多定义太长；描述模糊导致调用错误 |
| **检索上下文（Retrieved Context）** | RAG 从知识库中检索的相关文档片段 | 为模型提供实时、私有的事实依据 | 检索不相关；片段太多超出窗口 |
| **记忆提取（Memory Retrieval）** | 从长期记忆中提取的与当前任务相关的信息 | 让 Agent 在跨会话时仍能"记得"用户 | 记忆提取不准确；记忆膨胀 |
| **结构化指令（Structured Instructions）** | 元层面的输出格式要求、校验规则、工作流定义 | 确保输出可被下游程序消费 | 格式约束与任务指令混淆 |

#### 4.5.3 上下文窗口管理 — Context Engineering 的核心挑战

每个大模型都有有限的上下文窗口（如 128K、200K Tokens），而 Agent 的多轮交互会快速消耗这个窗口：

```
一轮工具调用消耗的 Token 分布：

  System Prompt         ~500-2000 Tokens
  + 工具定义 × N         ~200-1000 × N Tokens（工具越多，占用越大）
  + 对话历史             ~500-5000+ Tokens（随轮次增长）
  + 检索上下文           ~500-3000 Tokens（RAG 文档片段）
  + 工具返回结果          ~100-10000 Tokens（可能很大！）
  ─────────────────────────────────────────
  = 单轮总消耗           ~2000-20000+ Tokens
```

**三大核心策略**：

| 策略 | 英文名 | 核心做法 | 适用场景 |
|------|--------|----------|----------|
| **上下文压缩** | Context Compaction | 将冗长的对话历史或工具输出"压缩"为精炼摘要，保留关键信息、丢弃细节 | 工具返回了大量文本（如整个网页内容）；对话轮次过多 |
| **上下文选择** | Context Selection | 根据当前任务，从所有可用上下文中**只选择最相关**的部分放入窗口 | 有很多工具定义但当前只需几个；有很多 RAG 片段 |
| **上下文结构化** | Context Structuring | 用 XML 标签、Markdown 标题、优先级标记等组织上下文，让模型能快速定位关键信息 | 所有 Agent 场景——这是上下文工程的"代码规范" |

**上下文结构化的实际示例**（Claude 推荐的 XML 格式）：

```xml
<system_instructions>
  你是一个数据分析助手。始终先理解数据再给出建议。
</system_instructions>

<tool_definitions>
  <tool name="query_database">
    <description>执行SQL查询</description>
    <parameters>...</parameters>
  </tool>
</tool_definitions>

<conversation_history>
  <user_query>帮我分析上个月的销售趋势</user_query>
  <assistant_response>好的，我先查询数据库...</assistant_response>
  <tool_result>...</tool_result>
</conversation_history>

<retrieved_context priority="high">
  上个月销售数据摘要...
</retrieved_context>

<current_task>
  基于上述分析结果，生成一份销售报告
</current_task>
```

> 🔑 **关键认知**：Context Engineering 不是"越满越好"——填满 200K Token 上下文窗口会让模型"注意力稀释"，在大量无关信息中迷失。**好的上下文工程追求的是"精准"而非"全面"**。

#### 4.5.4 Context Engineering 与 Prompt Engineering 的关系

| 维度 | Prompt Engineering | Context Engineering |
|------|-------------------|-------------------|
| **关注点** | 文本指令本身的质量 | 信息环境的整体设计 |
| **操作对象** | 一段 Prompt 文本 | System Prompt + 历史 + 工具 + 检索 + 记忆 |
| **核心问题** | "AI 听懂了我的话吗？" | "AI 拥有了做出正确判断所需的全部信息吗？" |
| **优化方式** | A/B 测试不同的 Prompt 表述 | 调整上下文结构、压缩策略、信息优先级 |
| **典型产出** | 一个精心打磨的 Prompt 模板 | 一套上下文组装和管理的工程框架 |
| **成熟度** | 相对成熟，有大量方法论 | 2025-2026 年快速发展的前沿领域 |

> 📌 **结论**：Prompt Engineering 是 Context Engineering 的一个子集。在 2025-2026 年的 Agent 开发中，只关心 Prompt 已经不够了——你需要系统地设计 Agent 每一步能"看到"的完整信息环境。

---

### 4.6 Agent 的根基工程（Harness Engineering）

> 如果说 Agent Loop 是 Agent 的"大脑"，那么 **Agent Harness（Agent 运行框架）就是 Agent 的"身体"**——它提供了 Agent 运行所需的一切基础设施。

#### 4.6.1 什么是 Agent Harness？

**Harness** 这个词的本义是"马具"或"安全带"——它不决定马往哪里跑，但它确保马**能跑、受控、不脱缰**。

在 AI Agent 领域，**Agent Harness（Agent 运行框架）** 是指支撑 Agent 运行的完整基础设施层，包括：

```
┌─────────────────────────────────────────────────────────┐
│                   Agent Harness（运行框架）               │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  Tool        │  │  Permission │  │  Session     │      │
│  │  Registry    │  │  Gate       │  │  Store       │      │
│  │  工具注册中心  │  │  权限门控    │  │  会话存储    │      │
│  └──────┬───────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                 │                │              │
│  ┌──────┴───────┐  ┌──────┴──────┐  ┌──────┴──────┐      │
│  │  Context     │  │  Hook       │  │  Trace/Log  │      │
│  │  Compaction  │  │  System     │  │  追踪日志    │      │
│  │  上下文压缩   │  │  钩子系统    │  │              │      │
│  └──────────────┘  └─────────────┘  └─────────────┘      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Agent Loop（Agent 循环引擎）          │   │
│  │  observe → think → decide → act → observe         │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 4.6.2 Harness 的六大核心组件

Harness Engineering 不仅仅是"写一个 Agent Loop"——它是关于如何构建一个**可靠、安全、可观测、可扩展**的 Agent 运行时环境。以下是 Harness 的六大核心组件：

| 组件 | 英文名 | 作用 | 没有它会怎样 |
|------|--------|------|-------------|
| **工具注册中心** | Tool Registry | 统一管理所有可用工具的定义、版本、调用方式 | 工具分散在各处，难以管理、更新和安全审计 |
| **权限门控** | Permission Gate | 在 Agent 执行敏感操作前拦截并请求用户确认 | Agent 可能擅自删除文件、发送邮件、花光 API 费用 |
| **会话存储** | Session Store | 持久化 Agent 的会话状态，支持暂停/恢复 | Agent 崩溃后无法恢复，所有上下文丢失 |
| **上下文压缩** | Context Compaction | 当对话历史超出窗口时自动压缩/摘要 | 多轮对话后模型"失忆"或 API 费用暴涨 |
| **钩子系统** | Hook System | 在 Agent 执行关键节点（调用前/后、错误时）插入自定义逻辑 | 无法实现日志审计、合规检查、自定义安全策略 |
| **追踪日志** | Trace/Log | 记录每一步的输入、输出、工具调用、Token 消耗 | 出问题时无法排查，无法评估 Agent 的行为质量 |

#### 4.6.3 裸 Agent Loop vs Agent Harness

这是理解 Harness Engineering 最直观的方式——对比"手写的 Agent 循环"和"完整的 Agent 运行框架"：

| 维度 | 裸 Agent Loop | Agent Harness |
|------|--------------|---------------|
| **代码量** | 50-200 行 Python | 数千到数万行（Claude Code 是完整产品级 Harness） |
| **工具管理** | 手动写工具函数，散落在代码中 | Tool Registry 统一注册、发现、版本管理 |
| **权限控制** | 无——Agent 可以调用任何工具 | Permission Gate 拦截敏感操作、要求人工确认 |
| **状态管理** | 内存中的 messages 列表，重启即丢失 | Session Store 持久化，支持恢复和回放 |
| **上下文管理** | 不做任何处理，超出窗口就截断 | Context Compaction 智能压缩、优先级排序 |
| **错误处理** | 简单的 try-catch | 分级重试策略、优雅降级、熔断机制 |
| **可观测性** | print() 日志 | 结构化 Trace（每一步的时间/Token/工具调用/结果） |
| **安全性** | 无防护 | Prompt 注入检测、输出过滤、沙箱执行 |

#### 4.6.4 Harness Engineering 为什么在 2025-2026 年成为焦点？

```
2023 ─ "只要会调 API 就能做 AI 应用"
       Agent = LLM + 一个 while 循环

2024 ─ "Agent 能做 Demo，但一上生产就崩"
       工具调用失败、权限失控、成本爆炸、行为不可预测
       → 开发者意识到 Agent 需要的远不止"循环+工具"

2025 ─ Harness Engineering 概念正式提出
       学术论文：AI Harness Engineering (arXiv:2605.13357)
       最佳实践：Claude Code 的 harness 架构被广泛研究和模仿
       → 行业共识：Agent 的能力很大一部分来自 harness，不是模型本身

2026 ─ Harness Engineering 成为 Agent 开发的必修课
       开源项目：learn-claude-code, claw0, DeerFlow
       协议标准化：MCP/A2A/ACP 统一了工具和 Agent 的连接方式
       → "你会写 Agent Loop"不够了，"你会设计 Agent Harness"才是关键
```

> 📄 **关键论文**：[AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents](https://arxiv.org/abs/2605.13357) — 这篇 2025 年的论文首次系统性地定义了 Harness Engineering 作为一门工程学科的地位。

#### 4.6.5 Harness Engineering 的学习路径

| 阶段 | 学习内容 | 推荐资源 |
|------|----------|----------|
| **Stage 1**: 理解概念 | 读懂一个真实 Agent 系统的目录结构，找出它的 Agent Loop、Tool Registry、Permission Gate、Session Store、Context Compaction | 阅读 Claude Code 架构分析文章 |
| **Stage 2**: 动手实践 | 跑通现存 harness 的最小示例，加一个自己的工具，观察一次完整 Trace | [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) |
| **Stage 3**: 对比反思 | 把同一个任务分别用「裸 Agent Loop」和「harness」实现，对比稳定性、可调试性、成本 | 自己写对比实验 |
| **Stage 4**: 构建自己的 | 设计并实现一个最小可用的 Agent Harness，包含 Tool Registry + Permission Gate + Session Store | [claw0](https://github.com/shareAI-lab/claw0)、[hello-agents](https://github.com/datawhalechina/hello-agents) |

> 💡 **核心认知**：Prompt Engineering 让你做出一个好 Demo，Context Engineering 让你的 Agent 能处理复杂任务，**Harness Engineering 让你的 Agent 能从 Demo 走向生产**。三者是从"会说话"到"能做事"再到"可靠地做事"的递进。

---

### 4.7 什么时候用 Agent？什么时候不用？

这是 Agent 工程中最重要的判断力。Anthropic 在 "Building effective agents" 中给出的核心建议是：

> "Start with the simplest solution and only add complexity when needed."
> （从最简单的方案开始，只在确实需要时才增加复杂度。）

#### 4.5.1 判断矩阵

| 判断维度 | ✅ 适合用 Agent | ❌ 不适合用 Agent |
|----------|----------------|-------------------|
| **步骤确定性** | 步骤不确定，需要根据情况调整 | 步骤明确、固定、可穷举 |
| **决策复杂度** | 需要根据中间结果做出动态判断 | 决策逻辑简单（几个if-else就够） |
| **工具数量** | 需要使用多种工具，工具选择不确定 | 只需1个工具或完全不需要工具 |
| **探索程度** | 需要多轮尝试，摸着石头过河 | 一次调用就能得到确定结果 |
| **失败成本** | 失败可以重试，不会造成严重后果 | 失败后果不可逆（付款、删库、发公告） |
| **变化频率** | 任务需求经常变化 | 任务稳定，长期不变 |

#### 4.5.2 场景举例

**✅ 适合用 Agent 的场景**：

| 场景 | 为什么适合 |
|------|-----------|
| 代码开发与调试 | 不确定需要改哪些文件，需要读代码→改代码→测试→看报错→再改，循环迭代 |
| 旅行规划 | 需要综合多种信息（天气、交通、酒店、景点），根据中间结果动态调整 |
| 资料研究 | 不确定有哪些资料，需要搜索→阅读→判断→再搜索→综合→引用 |
| 客服工单处理 | 需要查用户信息、查订单、查物流、判断责任方、给出补偿方案，每个案例路径不同 |
| 个人助理 | 任务类型多样（提醒、搜索、总结、预订），需要根据上下文自主决策 |

**❌ 不适合用 Agent 的场景**：

| 场景 | 为什么不合适 | 更好的方案 |
|------|-------------|-----------|
| 定时数据备份 | 流程完全固定，每天做同样的事 | Cron Job / 简单脚本 |
| 查询余额 | 一次API调用，不需要推理 | 普通API调用 |
| 汇率换算 | 输入→计算→输出，纯粹确定性的 | 简单函数 |
| 审批工作流 | 规则明确：金额>10000找经理，否则自动通过 | 固定Workflow |
| 给全体用户群发消息 | 后果不可逆（发错了就是事故），且步骤固定 | 固定Workflow + 人工审核 |

#### 4.5.3 决策流程图

```
接收到一个任务需求
        │
        ↓
  ┌─────────────┐
  │ 步骤是否确定？│
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
   确定      不确定
    │         │
    ↓         ↓
┌───────┐  ┌──────────┐
│ 简单吗？│  │ 需要多种   │
└───┬───┘  │ 工具吗？   │
    │      └────┬─────┘
  ┌─┴─┐       ┌─┴─┐
  │   │       │   │
 简单 复杂    需要 不需要
  │   │       │   │
  ↓   ↓       ↓   ↓
用脚本 Workflow Agent 聊天机器人
或函数        就够了   就够了
```

#### 4.5.4 Anthropic 的核心建议

引用 "Building effective agents" 中的原话精神：

1. **简单优先**：如果几行代码能解决，就不要用 Agent
2. **Workflow 优先于 Agent**：如果任务可以分解为固定的步骤链，用 Workflow 就够了
3. **Agent 是最后的选择**：只有当任务确实需要动态推理和决策时，才引入 Agent
4. **保持工具简洁**：工具越多、Agent 越容易混淆，保持每个工具职责单一
5. **增加必要的摩擦**：高风险操作必须有人工确认环节

> "The most successful agent implementations we've seen are those that keep the architecture as simple as possible."

---

### 4.8 Agent 类型概述

Agent 不是只有一种形态。根据架构和用途，可以分为以下几类：

#### 4.6.1 按架构分类

**单 Agent（Single Agent）**：

一个 Agent 完成所有任务。适合中等复杂度、不需要分工的场景。

```
用户 → [单个 Agent: 感知→推理→规划→执行] → 结果
```

**多 Agent（Multi-Agent）**：

多个专门的 Agent 协作完成复杂任务。每个 Agent 有自己的职责、工具和知识。

```
用户 → [协调者 Agent]
              │
     ┌────────┼────────┐
     ↓        ↓        ↓
[Agent A] [Agent B] [Agent C]
 研究员     写作者     审查者
     │        │        │
     └────────┼────────┘
              ↓
           最终成果
```

#### 4.6.2 按应用场景分类

| 类型 | 代表项目 | 核心能力 | 典型任务 |
|------|---------|---------|---------|
| **编程 Agent** | Claude Code, Codex, Aider, SWE-agent | 读代码、写代码、执行命令、改文件、跑测试 | 修Bug、加Feature、重构代码 |
| **个人助理 Agent** | OpenClaw, Hermes Agent | 长期记忆、跨应用操作、Skills、消息网关 | 日常任务管理、信息整理、自动化 |
| **研究 Agent** | GPT Researcher, STORM | 网络搜索、信息筛选、引用追踪、报告生成 | 文献调研、市场调研、技术调研 |
| **浏览器 Agent** | browser-use, UI-TARS | 网页解析、元素定位、点击操作、表单填写 | 网页数据采集、流程自动化 |
| **通用 Agent** | LangGraph Agent, smolagents, Qwen-Agent | 可扩展工具集、可编排流程、状态管理 | 各种自定义场景 |

**本课程重点关注**：
- **Claude Code**：作为编程 Agent 的最佳工程样本，值得深入研究其架构设计
- **GPT Researcher / STORM**：作为研究 Agent 的典型，适合理解"搜索→筛选→综合"的多步 Agent 流程
- **LangGraph**：作为 Agent 工程的通用框架基础

---

## 五、实操环节（70分钟）

### 实操 1：聊天机器人 vs Agent 对比实验（30分钟）

**目标**：亲手对比 Chatbot 和 Agent 对同一个任务的处理，感受本质差异。

**完整可运行代码**：

```python
"""
================================================================
实操 1：聊天机器人 vs Agent 对比实验
================================================================
任务: "帮我查看现在的时间，搜索所有Python文件，然后设置提醒"
================================================================
"""

import json
import os
import glob
from datetime import datetime
from openai import OpenAI

# ============================================================
# 准备工作：初始化客户端
# ============================================================
client = OpenAI(
    api_key="your-deepseek-api-key",  # 替换为你的API Key
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-chat"

# ============================================================
# 辅助函数：模拟工具
# ============================================================

def get_current_time():
    """获取当前日期和时间"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

def get_weather(city: str):
    """查询城市天气（模拟）"""
    weather_data = {
        "北京": "晴，5°C ~ 15°C，北风3级",
        "上海": "多云，12°C ~ 20°C，东风2级",
        "深圳": "小雨，18°C ~ 25°C，南风4级",
    }
    return weather_data.get(city, f"未找到{city}的天气数据")

def search_files(pattern: str, directory: str = "."):
    """搜索文件"""
    try:
        files = glob.glob(f"{directory}/**/{pattern}", recursive=True)
        return files[:15] if files else f"未找到匹配'{pattern}'的文件"
    except Exception as e:
        return f"搜索出错：{e}"

def create_reminder(task: str, time_str: str):
    """创建提醒（模拟写入文件）"""
    reminder = f"[{time_str}] - {task}\n"
    with open("reminders.txt", "a", encoding="utf-8") as f:
        f.write(reminder)
    return f"✅ 已创建提醒：'{task}' - {time_str}"

# ============================================================
# 方式1：纯聊天机器人（Chatbot）
# ============================================================

def chatbot(query: str) -> str:
    """
    聊天机器人：只能生成文本，没有任何工具。
    它对世界的了解完全来自训练数据。
    """
    print("\n" + "=" * 60)
    print("  🤖 聊天机器人模式")
    print("=" * 60)
    print(f"\n用户输入: {query}\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个有帮助的AI助手，用中文回答。"},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content
    print(f"机器人回答:\n{answer}\n")
    print("-" * 60)
    print("⚠️ 注意：Chatbot 只是在'说'，没有真正'做'任何事。")
    print("它不知道现在几点，没有搜索你的文件，也没有设置提醒。")
    print("-" * 60)
    return answer


# ============================================================
# 方式2：Agent（有工具、会决策、能执行）
# ============================================================

# --- 定义工具列表 ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间，精确到秒",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'、'上海'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "在指定目录中搜索匹配模式的文件，支持通配符",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "文件名匹配模式，如'*.py'、'*.md'、'test*.py'"
                    },
                    "directory": {
                        "type": "string",
                        "description": "搜索的目录路径，默认为当前目录"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "创建一个提醒事项，会记录到文件中",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "提醒的内容"
                    },
                    "time_str": {
                        "type": "string",
                        "description": "提醒的时间，如'15:00'、'明天上午9点'"
                    }
                },
                "required": ["task", "time_str"]
            }
        }
    }
]

# --- 工具函数映射 ---
AVAILABLE_FUNCTIONS = {
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "search_files": search_files,
    "create_reminder": create_reminder,
}

# --- Agent 主循环 ---
def agent_loop(user_input: str, max_steps: int = 8) -> str:
    """
    Agent 核心循环：
    1. 把用户输入和工具列表发给 LLM
    2. LLM 决定是调工具还是直接回答
    3. 如果要调工具 → 执行工具 → 把结果喂回 LLM → 回到2
    4. 如果直接回答 → 返回答案
    """
    print("\n" + "=" * 60)
    print("  🧠 Agent 模式")
    print("=" * 60)
    print(f"\n用户输入: {user_input}\n")

    messages = [{"role": "user", "content": user_input}]
    step = 0

    while step < max_steps:
        step += 1
        print(f"{'─' * 60}")
        print(f"🔄 Step {step}/{max_steps}")
        print(f"{'─' * 60}")

        # 调用 LLM
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0.3
        )

        response_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        # 打印 LLM 的文字输出（如果有的话）
        if response_message.content:
            content_preview = response_message.content[:200]
            print(f"💭 Agent 思考: {content_preview}")

        # 判断：需要调工具吗？
        if response_message.tool_calls:
            print(f"🔧 Agent 决定调用 {len(response_message.tool_calls)} 个工具")

            # 将 assistant 消息加入历史
            messages.append(response_message)

            # 逐个执行工具
            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"   📞 调用: {func_name}")
                print(f"   📝 参数: {func_args}")

                # 执行工具
                func = AVAILABLE_FUNCTIONS.get(func_name)
                if func:
                    try:
                        result = func(**func_args)
                        print(f"   ✅ 结果: {result}")
                    except Exception as e:
                        result = f"工具执行出错: {e}"
                        print(f"   ❌ 错误: {result}")
                else:
                    result = f"未知工具: {func_name}"
                    print(f"   ❌ {result}")

                # 将工具结果加入历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            # 没有工具调用 → Agent 认为完成了
            print(f"\n🎯 Agent 完成任务!")
            print(f"   最终回答: {response_message.content}")
            print(f"{'─' * 60}")
            print("✅ Agent 真正'做'了事：获取了实时时间、搜索了文件、设置了提醒。")
            print(f"{'─' * 60}")
            return response_message.content

    print(f"⚠️ 达到最大步数限制({max_steps})")
    return "任务未能在限定步数内完成"


# ============================================================
# 对比实验
# ============================================================

if __name__ == "__main__":
    TASK = """
    请帮我完成以下任务：
    1. 现在几点了？
    2. 北京天气怎么样？
    3. 在当前目录搜索所有 Python 文件（*.py）
    4. 设置一个下午5点的提醒："完成Agent课程作业"
    """

    print("\n" + "█" * 60)
    print("█  Agent vs Chatbot 对比实验")
    print("█" * 60)

    # 实验一：用 Chatbot
    chatbot_answer = chatbot(TASK)

    print("\n按 Enter 继续到 Agent 实验...")
    # input()  # 实际运行时取消注释

    # 实验二：用 Agent
    agent_answer = agent_loop(TASK)

    # ============================================================
    # 对比总结
    # ============================================================
    print("\n" + "█" * 60)
    print("█  对比分析")
    print("█" * 60)

    print("""
┌────────────────────┬──────────────────────┬──────────────────────┐
│       维度          │   🤖 Chatbot         │   🧠 Agent           │
├────────────────────┼──────────────────────┼──────────────────────┤
│ 是否获取了实时时间？ │   ❌ 不知道           │   ✅ 调用了时间函数    │
│ 是否查询了天气？    │   ❌ 可能编造          │   ✅ 调用了天气API     │
│ 是否搜索了文件？    │   ❌ 不可能做到        │   ✅ 调用了文件搜索    │
│ 是否设置了提醒？    │   ❌ 只是说"我帮你设"   │   ✅ 写入了文件        │
│ 输出了什么？        │   一段"看起来不错"     │   每个任务的实际结果   │
│                    │   但没有实据的文字      │                      │
└────────────────────┴──────────────────────┴──────────────────────┘

💡 关键启示：
  - Chatbot 在"扮演"一个助手（说的都对，但什么都没做）
  - Agent 在"成为"一个助手（真的做了事，每个结果都可验证）
  - 打开 reminders.txt 文件，你会看到 Agent 真的写入了提醒
    """)

    # 验证 Agent 真的设置了提醒
    if os.path.exists("reminders.txt"):
        print("📄 reminders.txt 内容验证：")
        with open("reminders.txt", "r", encoding="utf-8") as f:
            print(f.read())
```

---

### 实操 2：带详细日志的 Agent 决策观察（25分钟）

**目标**：通过逐步日志，近距离观察 Agent "思考→决策→执行→反馈"的完整心智过程。

**完整可运行代码**：

```python
"""
================================================================
实操 2：Agent 决策过程观察器
================================================================
给 Agent 一个需要多步推理的任务，观察它每一步的思考过程。
================================================================
"""

import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-chat"

# ============================================================
# 更丰富的工具集
# ============================================================

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression: str):
    """安全计算数学表达式"""
    try:
        # 只允许安全的字符
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return f"表达式包含不允许的字符: {expression}"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算出错: {e}"

def read_file(filepath: str):
    """读取文件内容"""
    try:
        if not os.path.exists(filepath):
            return f"文件不存在: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if len(content) > 1000:
            return content[:1000] + f"\n...(共{len(content)}字符，已截断)"
        return content
    except Exception as e:
        return f"读取文件出错: {e}"

def create_reminder(task: str, time_str: str):
    """创建提醒"""
    reminder_entry = f"[{time_str}] {task}\n"
    with open("agent_reminders.txt", "a", encoding="utf-8") as f:
        f.write(reminder_entry)
    return f"✅ 提醒已记录: '{task}' @ {time_str}"

import os

TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算，支持 + - * / ( ) % 等基本运算。例如: '2+3*4' 会返回 14",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '128+256'、'(15+9)*3'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取指定文件的内容，返回文件全文（最多1000字符）",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "文件路径"
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "创建一个提醒事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "提醒内容"},
                    "time_str": {"type": "string", "description": "提醒时间"}
                },
                "required": ["task", "time_str"]
            }
        }
    }
]

ALL_TOOLS = {
    "get_current_time": get_current_time,
    "calculator": calculator,
    "read_file": read_file,
    "create_reminder": create_reminder,
}


def observe_agent_thinking(user_input: str, verbose: bool = True):
    """
    Agent 决策过程观察器
    - 打印每一步的完整思考过程
    - 展示 LLM 的原始输出（包括推理文字）
    - 展示工具选择和参数构建的细节
    """

    system_prompt = """你是一个善于推理的AI助手。在每次行动前，请先思考：
- 当前已知什么信息？
- 还缺少什么信息？
- 下一步应该做什么？为什么？
- 需要调用哪个工具？

请把你的推理过程说出来，然后再决定行动。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    step = 0

    while step < 10:
        step += 1

        if verbose:
            print(f"\n{'█' * 70}")
            print(f"█  Step {step} — Agent 思考与决策")
            print(f"{'█' * 70}")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS_CONFIG,
            temperature=0.3
        )

        msg = response.choices[0].message

        # ====== 展示 LLM 的文字输出（推理过程） ======
        if msg.content and verbose:
            print(f"\n💬 【Agent 的文字输出（思考过程）】")
            print(f"{'─' * 60}")
            print(msg.content)
            print(f"{'─' * 60}")

        # ====== 展示工具调用决策 ======
        if msg.tool_calls:
            print(f"\n🔧 【Agent 决定使用工具】- 共 {len(msg.tool_calls)} 个调用")

            messages.append(msg)

            for i, tc in enumerate(msg.tool_calls, 1):
                func_name = tc.function.name
                func_args = json.loads(tc.function.arguments)

                print(f"\n  Tool Call #{i}:")
                print(f"  ├─ 工具名称: {func_name}")
                print(f"  ├─ 调用参数: {json.dumps(func_args, ensure_ascii=False)}")

                # 执行工具
                func = ALL_TOOLS.get(func_name)
                if func:
                    try:
                        result = func(**func_args)
                        print(f"  ├─ 执行结果: {result}")
                    except Exception as e:
                        result = f"❌ 错误: {e}"
                        print(f"  ├─ ❌ 执行失败: {e}")
                else:
                    result = f"❌ 未找到工具 '{func_name}'"
                    print(f"  ├─ ❌ {result}")

                # 结果反馈到对话历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })

                if verbose:
                    print(f"  └─ （结果已反馈给 LLM，进入下一轮思考）")

        else:
            # 没有工具调用 = Agent 认为任务完成
            print(f"\n✅ 【Agent 完成任务】")
            print(f"{'─' * 60}")
            print(msg.content)
            print(f"{'─' * 60}")

            if verbose:
                print(f"\n📊 任务统计：")
                print(f"   总步数: {step}")
                print(f"   工具调用总数: 在历史消息中体现")
                print(f"   最终回复长度: {len(msg.content)} 字符")

            return msg.content

    return "⚠️ 达到步数上限"


# ============================================================
# 运行观察
# ============================================================

if __name__ == "__main__":
    # 创建一个测试文件，让 Agent 可以读取
    with open("test_data.txt", "w", encoding="utf-8") as f:
        f.write("项目名称: AI Agent 课程\n")
        f.write("学生人数: 45人\n")
        f.write("课程进度: 第7周\n")
        f.write("本周任务: 完成 Agent 课程学习\n")

    print("=" * 70)
    print("   🧠 Agent 决策过程实时观察器")
    print("=" * 70)

    TASK = """
    请帮我完成以下任务，按顺序执行：
    1. 查看现在几点了
    2. 计算 (456 + 789) * 12 / 3 的结果
    3. 读取 test_data.txt 的内容
    4. 根据文件中的课程进度信息，设置一个提醒
    提示：以上4个任务中有3个需要调用工具，请一步一步完成。
    """

    print(f"\n📋 任务描述: {TASK.strip()}")

    final_answer = observe_agent_thinking(TASK)

    print(f"\n{'=' * 70}")
    print("   观察完成")
    print(f"{'=' * 70}")

    # 讨论题
    print("""
📝 观察后讨论：

1. Agent 一共执行了几步？每一步做了什么？
2. Agent 有没有做"多余"的事？（调了不需要的工具？）
3. Agent 的文字输出（思考过程）和实际操作一致吗？
4. 如果让你手动写代码完成这个任务，要写多少行？
   相比之下，Agent 为你省去了什么？
5. 你观察到 Agent 在什么情况下会"来回调整"？
    """)
```

---

### 实操 3：Claude Code Agent 架构分析（15分钟）

**目标**：通过分析 Claude Code 这个真实的、产品级的 Agent 系统，理解 Agent 工程中的关键设计决策。

**讨论指南**：

#### 3.1 Claude Code 的 Agent Loop 是怎样的？

不同于简单的 `while True` 循环，Claude Code 的 Agent Loop 有更精细的阶段：

```
接收用户输入
    ↓
理解意图 (Parse Intent)
    ↓
制定计划 (Make Plan) — 需要哪些步骤？用到哪些工具？
    ↓
──→ 执行工具 (Execute Tool)
│       ↓
│   观察结果 (Observe Result)
│       ↓
│   评估 (Evaluate) — 结果符合预期吗？
│       ↓
│   ├── 符合 → 继续下一步
│   └── 不符合 → 调整策略 (Adapt)
│                    ↓
│                    └── 回到执行或重新规划
│       ↓
└── 所有步骤完成 → 生成最终回复
```

**讨论要点**：
- 为什么 Claude Code 的规划不是一次性的？因为代码项目太复杂，计划必须随执行结果动态调整
- 和我们在实操1中写的简单 Agent Loop 比，多了哪些环节？多了"评估"和"策略调整"

#### 3.2 Claude Code 有哪些工具？

| 工具类别 | 具体工具 | 用途 |
|---------|---------|------|
| **文件系统** | Read, Write, Edit, Glob, Grep | 理解和修改代码 |
| **命令执行** | Bash | 运行命令、测试、安装依赖、git操作 |
| **搜索** | WebSearch, WebFetch | 获取最新信息 |
| **任务管理** | TodoWrite, TaskStop | 管理复杂任务 |
| **子代理** | SendMessage, Skill | 将子任务分派给专用子Agent |

**讨论要点**：
- 为什么工具要分"读"和"写"？——权限分离：读操作可以自动执行，写操作（特别是破坏性操作）需要用户确认
- 为什么有 TodoWrite 这种"管理自身的工具"？——复杂任务需要自我跟踪，Agent 也需要"记笔记"

#### 3.3 Claude Code 的权限机制是怎样的？

```
操作类型分级：
┌─────────────────────────────────────────────────────────────┐
│ 🟢 安全操作（自动批准）                                     │
│    - 读取文件 (Read, Glob, Grep)                            │
│    - WebSearch, WebFetch                                    │
├─────────────────────────────────────────────────────────────┤
│ 🟡 一般操作（在同目录内自动批准）                            │
│    - 编辑文件 (Edit, Write)                                 │
│    - 在项目目录内执行命令                                    │
├─────────────────────────────────────────────────────────────┤
│ 🔴 危险操作（必须用户确认）                                  │
│    - 在项目目录外写文件                                      │
│    - 执行可能破坏性的命令 (rm, force push)                    │
│    - 发送消息到外部 (SendMessage to external)                │
└─────────────────────────────────────────────────────────────┘
```

**讨论要点**：
- 为什么"安全操作"要自动批准？——减少摩擦，让 Agent 高效工作
- 为什么"危险操作"必须确认？——Agent 可能犯错，不可逆操作需要人类把关
- 这和 Anthropic "Building effective agents" 中的"保持适当摩擦"原则完全一致

#### 3.4 Claude Code 的 Subagents（子代理）机制

```
用户: 帮我重构这个项目的数据库层

主 Agent (Coordinator):
  ├── 子Agent 1: "阅读所有数据库相关代码，画出当前架构"
  ├── 子Agent 2: "设计新的数据库接口"
  ├── 子Agent 3: "实现新接口，迁移旧代码"
  └── 子Agent 4: "编写并运行测试，确保迁移正确"
```

**为什么需要 Subagents？**
1. **上下文隔离**：每个子Agent只看相关代码，不会上下文爆炸
2. **专注**：专门的子Agent比通用Agent在特定子任务上更准确
3. **并行**：独立的子任务可以同时执行

#### 3.5 Claude Code Hooks（钩子）机制

Hooks 允许在 Agent 行为的关键节点插入自定义逻辑：

```
事件: Agent 决定编辑文件
  → PreToolUse Hook: 检查文件名是否符合团队规范？
  → 执行编辑
  → PostToolUse Hook: 自动运行 linter，格式检查
  → 如果有问题 → 反馈给 Agent 自动修正

事件: Agent 任务完成
  → Stop Hook: 自动运行测试套件，确保没有破坏现有功能
  → 如果测试失败 → 通知 Agent 继续修复
```

**讨论要点**：
- Hooks 让 Agent 的行为变得**可控、可审查、可扩展**
- 这是一种将"工程最佳实践"编码进 Agent 运行时的机制
- 思考：在你的场景中，你会在 Agent 行为前后加什么检查？

---

## 六、课后作业

> 本次作业重点在**理解和反思**，而非写代码。高质量的思考是本课最重要的产出。

### 作业1：绘制 Agent 核心循环图

用自己的话（不要抄讲义），手绘或使用工具绘制一张 Agent 核心循环图，包含：
- 四个核心能力（感知、推理、规划、执行）
- 它们之间的循环关系
- 至少标注 3 个关键决策点

**提交要求**：图片 + 200字以内的文字说明

### 作业2：场景判断练习

列举 **3 个适合用 Agent 的场景**和 **3 个不适合用 Agent 的场景**，对每个场景说明：
- 场景描述（一句话）
- 判断结论（适合/不适合）
- 判断理由（至少2条原因，结合本课学到的判断矩阵）

**示例**：
- 场景：每天早上自动从数据库导出昨天的销售数据，生成日报发送到管理层邮箱
- 判断：**不适合**用 Agent
- 理由：①步骤完全固定，不需要动态决策 ②Workflow/定时脚本完全可以胜任且更可靠

### 作业3：Building Effective Agents 读后感

阅读 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，写一篇 300 字的读后感，回答以下问题：
- 文章的核心观点是什么？（用你自己的话总结，不要翻译）
- 你觉得最有启发性的一点是什么？为什么？
- 这篇文章和本节课的内容有哪些互相印证的地方？

---

## 七、拓展阅读

### 必读（核心参考）

| 资料 | 链接 | 为什么重要 |
|------|------|-----------|
| Anthropic: Building effective agents | [链接](https://www.anthropic.com/engineering/building-effective-agents) | Agent 设计的圣经级参考，讲清了什么时候该用/不该用 Agent |
| OpenAI: A practical guide to building agents | [链接](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | 从产品和工程视角的 Agent 落地指南 |
| Anthropic: What is an Agent? | [链接](https://docs.anthropic.com/en/docs/agents-and-tools/agent-overview) | Anthropic 官方 Agent 概念文档 |

### 进阶阅读

| 资料 | 链接 | 适合阶段 |
|------|------|---------|
| hello-agents 教程 | [GitHub](https://github.com/datawhalechina/hello-agents) | 学完本课后，跟着从零构建 Agent |
| Lilian Weng: LLM Powered Autonomous Agents | [博客](https://lilianweng.github.io/posts/2023-06-23-agent/) | Agent 架构的系统综述，经典长文 |
| Claude Code 文档 | [链接](https://code.claude.com/docs/en/overview) | 真实产品级 Agent 的架构参考 |
| LangGraph 文档 | [链接](https://langchain-ai.github.io/langgraph/) | Agent 工程框架，下节课会用到 |
| ReAct 论文 | [arXiv](https://arxiv.org/abs/2210.03629) | Reasoning + Acting 的基础范式论文 |

---

## 八、常见问题

### Q1: Agent 和 RAG 是什么关系？

**答**：RAG（检索增强生成）是一种特定的技术模式：检索相关文档 → 让 LLM 基于文档回答。RAG 可以作为 Agent 的一个**工具**：Agent 发现用户问的问题需要查资料时，调用 RAG 工具进行检索。但 Agent 远不止 RAG——Agent 可以搜索、计算、发邮件、操作文件、运行代码、调用API……RAG 只是 Agent 工具箱里的一件工具。

一句话概括：**RAG 让 LLM "知道更多"，Agent 让 LLM "做到更多"。**

### Q2: Agent 是不是就是加了工具的聊天机器人？

**答**：不完全是。加上工具是必要条件，但不是充分条件。真正的 Agent 还必须具备：
- **自主决策**：自己决定什么时候用哪个工具，用几次
- **动态规划**：根据中间结果调整计划
- **错误恢复**：工具调用失败后能想到备选方案
- **目标导向**：所有行动围绕用户的目标展开，而不是无方向地调工具

一个只加了工具但没有决策循环的"聊天机器人"仍然不是 Agent ——它与 Agent 的区别就像电动螺丝刀和机器人之间的区别：电动螺丝刀是工具增强了人，而机器人能自主判断该拧哪个螺丝、用多大扭矩、拧几圈。

### Q3: Agent 会不会替代人类工作？

**答**：Agent 替代的是**具体任务**不是**完整职业**。就像计算器替代了手工计算，但没有替代数学家。Agent 让人类从繁琐的"执行"中解放出来，专注于更有价值的"决策"和"创造"。

理解这组关系：

```
人类：设定目标、做出关键决策、承担最终责任
Agent：分解任务、执行步骤、调用工具、处理异常
```

Agent 是"执行者"，人类是"指挥者"。这也是 Anthropic "Building effective agents" 中的核心理念之一。

### Q4: 多 Agent 一定比单 Agent 好吗？

**答**：**不一定。简单优先。** 多 Agent 引入了更多组件和通信开销，调不好反而比单 Agent 更差。Anthropic 的经验是：大多数有效部署的 Agent 系统都是单 Agent + 精心设计的工具集。只有在以下情况才考虑多 Agent：
- 任务天然可以分解为独立子任务（可以并行）
- 不同子任务需要不同的专业知识（如编码 + 设计 + 测试）
- 上下文窗口限制迫使你必须拆分

**默认原则：先用单 Agent 做到最好，不够用时再加。**

### Q5: 学完这节课，我现在能做什么？

**答**：你已经有能力：
1. 判断一个需求是否应该用 Agent 来解决
2. 用 Python 写一个最小但完整的 Agent Loop（参考实操1的代码）
3. 给 Agent 添加自定义工具
4. 理解 Agent 每一步决策背后的逻辑
5. 带着正确的概念框架去学习 LangGraph、MCP 等进阶内容（下两节课）

### Q6: Agent 的"智能"到底来自哪里？

**答**：Agent 的智能来自三个部分的协同：
1. **LLM 的推理能力**（知道"下一步该做什么"）
2. **工具系统的丰富性**（有手段去"做"）
3. **Agent Harness 的设计**（循环机制、错误处理、权限控制、上下文管理）

这其中，**Harness Engineering（Agent 运行时工程）** 正在成为一个独立的工程领域。很多团队发现：即使使用相同的 LLM 和相同的工具，不同的 Harness 设计会导致显著不同的成功率和可靠性。这也是为什么像 Claude Code 这样的产品值得深入研究。

---

## 九、本课总结

本课建立了 Agent 的六个核心认知支柱：

```
┌──────────────────────────────────────────────────────────────────┐
│                        什么是 Agent？                             │
│                                                                  │
│  支柱1: 演进路径                                                 │
│  Chatbot (只会说) → Workflow (按流程做) → Agent (自主做)          │
│                                                                  │
│  支柱2: 四能力模型                                               │
│  感知 → 推理 → 规划 → 执行 → (循环)                               │
│                                                                  │
│  支柱3: 核心循环                                                 │
│  while not done: observe → think → decide → act → feedback       │
│                                                                  │
│  支柱4: Context Engineering（上下文工程）                         │
│  不止写好 Prompt，更要设计好 Agent "看到"的完整信息环境            │
│  六大要素：System Prompt / 对话历史 / 工具定义 / 检索上下文        │
│           / 记忆提取 / 结构化指令                                  │
│  核心策略：压缩(Compaction) / 选择(Selection) / 结构化(Structuring)│
│                                                                  │
│  支柱5: Harness Engineering（根基工程）                           │
│  Agent 的能力很大一部分来自它的 harness，不是模型本身               │
│  六大组件：Tool Registry / Permission Gate / Session Store        │
│           / Context Compaction / Hook System / Trace/Log          │
│  Prompt→Context→Harness：从"会说话"到"能做事"再到"可靠地做事"      │
│                                                                  │
│  支柱6: 判断力                                                   │
│  知道什么时候该用 Agent，什么时候不该用                            │
│  简单优先，复杂靠后                                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**下节课预告**：第2课将学习 LangChain/LangGraph，把今天的概念用工程框架落地，动手做一个"AI 秘书"。

---

> **教学参考**：本节课的核心参考文献为 Anthropic 的 "Building effective agents"（2024年12月）。建议教师在备课前仔细阅读全文，并在课上多次引用其中的观点。课程中贯穿的"用同一个例子（旅行规划）从 Chatbot 讲到 Agent"是为了帮助学生建立连贯的认知，请在实际教学中保持这个主线。
