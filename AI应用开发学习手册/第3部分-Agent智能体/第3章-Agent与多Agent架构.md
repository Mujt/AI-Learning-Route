# 第 3 章 Agent 与多 Agent 架构设计与实战

## 学习目标

- 理解 Agent 的核心概念、架构组成与设计原则
- 掌握 Function Calling 机制的原理与实现
- 掌握 ReAct 模式的思考-行动循环
- 理解 Plan-and-Execute 与 AutoGen 多智能体框架
- 学会多 Agent 架构的设计模式

---

## 3.1 Agent 核心概念与架构

### 3.1.1 什么是 Agent（智能体）

**AI Agent = 大模型（大脑）+ 规划（Planning）+ 记忆（Memory）+ 工具（Tools）+ 行动（Action）**，是一个能**自主感知、决策、执行**的智能系统。

```
用户输入 → [记忆/上下文] → LLM 推理决策
                            ├── 需要工具？ → 调用工具（Function Calling）→ 观察结果
                            ├── 需要分解？ → 规划子任务 → 逐步执行
                            └── 任务完成？ → 生成最终回答
```

### 3.1.2 Agent 架构五要素

| 要素 | 作用 | 关键设计 |
|------|------|----------|
| **大模型（Brain）** | 决策与推理核心 | 选推理能力强的模型；规划能力与模型成正比 |
| **规划（Planning）** | 拆解任务、制定步骤 | 任务分解、反思修正、子任务排序 |
| **记忆（Memory）** | 短期（会话）与长期（知识） | 会话记忆、向量记忆、图谱记忆 |
| **工具（Tools）** | 与外部世界交互 | 函数定义清晰、MCP 统一接入 |
| **行动（Action）** | 执行并观察反馈 | 工具调用、API 请求、错误处理 |

### 3.1.3 Agent 设计原则

1. **工具粒度适中**：工具太少能力受限，太多选择困难；每个工具职责单一、描述清晰。
2. **明确终止条件**：定义"任务完成的判断标准"，防止无限循环。
3. **错误容错**：工具调用失败要有重试/回退/求助用户机制。
4. **预算控制**：限制最大迭代步数与 Token 消耗。
5. **可观测性**：记录每一步"思考→行动→观察"，便于调试与审计。

## 3.2 Function Calling（函数调用）

### 3.2.1 原理

Function Calling 是**模型结构化输出工具调用参数**的能力：模型不直接执行函数，而是输出"要调用哪个函数、参数是什么"的 JSON，由应用代码执行后把结果回填给模型。

```
用户："上海明天天气怎么样？"
模型（结构化输出）：
  {name: "get_weather", arguments: {"city": "上海", "date": "明天"}}
应用执行 get_weather("上海") → 返回 "晴 26°C"
模型结合结果生成自然语言回答
```

### 3.2.2 优势

- **可靠性**：参数由模型按 Schema 生成，JSON 结构化输出稳定。
- **无需提示词模板**：工具描述通过 API 参数传递，比"文本式工具说明"更准确。
- **生态标准**：OpenAI、Claude、DeepSeek、GLM、Qwen 均支持，OpenAI 兼容格式统一。

### 3.2.3 OpenAI 兼容实现

```python
from openai import OpenAI
client = OpenAI(base_url="...", api_key="...")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询城市实时天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市名"}},
            "required": ["city"]
        }
    }
}]

# 第一轮：模型决定调用工具
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "上海天气怎么样？"}],
    tools=tools,
)
msg = resp.choices[0].message
print(msg.tool_calls)   # [ToolCall(name="get_weather", arguments={city: 上海})]

# 第二轮：执行工具后回填结果
if msg.tool_calls:
    result = get_weather(**json.loads(msg.tool_calls[0].function.arguments))
    messages = [
        {"role": "user", "content": "上海天气怎么样？"},
        msg,   # 模型工具调用消息
        {"role": "tool", "tool_call_id": msg.tool_calls[0].id, "content": result},
    ]
    final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print(final.choices[0].message.content)  # "上海今天晴，26°C..."
```

## 3.3 ReAct（Reasoning + Acting）

### 3.3.1 核心思想

ReAct 模式（论文 *ReAct: Synergizing Reasoning and Acting in Language Models*）将**推理（Thought）**与**行动（Action）**交替循环，让模型"边想边做"：

```
Thought: 用户要查天气，我需要调用天气工具
Action: get_weather["上海"]
Observation: 晴 26°C
Thought: 有了天气数据，可以生成回答了
Final Answer: 上海今天晴，26°C
```

### 3.3.2 相比纯 Function Calling 的差异

- **Function Calling**：工具由模型单步输出，多步任务需外部循环控制。
- **ReAct**：把"思考-行动-观察"的循环内建到提示词模式中，更适合**需要推理规划**的复杂任务，也兼容"先搜索再计算"的多步流程。

### 3.3.3 ReAct 提示词模板

```
你是一个可以调用工具完成任务的助手。请按以下格式回复：
Thought: 分析当前需要做什么
Action: 工具名
Action Input: {"参数": "值"}
Observation: 工具返回结果
...（可多轮）
Thought: 我认为可以给出最终答案了
Final Answer: 完整回答

可用工具：
- get_weather: 查询天气
- web_search: 网页搜索
```

### 3.3.4 LangChain 中的 AgentExecutor（ReAct）

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

react_prompt = PromptTemplate.from_template("""...ReAct 模板...""")
agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools,
                         max_iterations=5, verbose=True)   # max_iterations 防死循环
executor.invoke({"input": "先查上海天气，再查北京天气，对比一下"})
```

## 3.4 Plan-and-Execute

### 3.4.1 核心思想

把"规划"与"执行"分离：**Planner（规划器）** 先制定完整步骤，**Executor（执行器）** 逐步执行。

```
Planner: 将任务拆成子任务清单
  [1] 搜索酒店  [2] 查询航班  [3] 汇总行程
Executor: 对每个子任务调用工具执行
Reflector（可选）: 根据执行结果修订计划
```

### 3.4.2 适用场景与优缺点

| 优点 | 缺点 |
|------|------|
| 全局视野，适合复杂长任务 | 计划与实际偏差时需重规划 |
| 步骤清晰，可解释性强 | 规划本身消耗额外 Token |
| 可并行执行独立子任务 | 动态变化场景适应差 |

**选型对比**：任务步骤明确 → Plan-and-Execute；任务需要边做边看 → ReAct；简单单步 → Function Calling。

## 3.5 AutoGen 多智能体框架

### 3.5.1 什么是 AutoGen

AutoGen 是微软开源的**多智能体对话框架**，核心思想：**多个 Agent 通过"对话"协作完成任务**，支持人与 Agent、Agent 与 Agent 之间的多轮交互。

### 3.5.2 核心概念

| 概念 | 说明 |
|------|------|
| ConversableAgent | 可对话智能体基类 |
| AssistantAgent | 助手角色（出主意、写代码） |
| UserProxyAgent | 模拟用户（执行代码、给反馈） |
| GroupChat / GroupChatManager | 多 Agent 群聊调度 |
| 双人对话 | 两个 Agent 自动交替发言直至终止 |

### 3.5.3 快速上手

```python
from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "gpt-4o-mini", "api_key": "..."}

# 写代码的助手
assistant = AssistantAgent(
    name="coder", llm_config=llm_config,
    system_message="你是 Python 专家，编写并调试代码，完成后回复 TERMINATE。")

# 执行代码的代理（模拟用户）
user_proxy = UserProxyAgent(
    name="user", human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False})

# 对话启动：让 assistant 写一个冒泡排序
user_proxy.initiate_chat(
    assistant, message="请用 Python 实现冒泡排序并运行验证。")
```

### 3.5.4 多 Agent 协作（GroupChat）

```python
from autogen import GroupChat, GroupChatManager

planner = AssistantAgent(name="planner", system_message="负责拆分任务...")
researcher = AssistantAgent(name="researcher", system_message="负责检索资料...")
writer = AssistantAgent(name="writer", system_message="负责撰写报告...")

group_chat = GroupChat(agents=[planner, researcher, writer],
                       messages=[], max_round=20)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="调研AI Agent行业趋势并写报告")
```

### 3.5.5 AutoGen 适用场景

- 代码生成 + 执行验证（写代码 Agent + 执行 Agent）
- 研究任务（规划者 + 检索者 + 写作者）
- 对抗式任务（审稿人 vs 作者）提升质量

## 3.6 多 Agent 架构设计模式

### 3.6.1 常见模式

| 模式 | 结构 | 适用 |
|------|------|------|
| **Supervisor（主管）** | 主 Agent 调度多个子 Agent | 任务可分发（研究、客服） |
| **Pipeline（流水线）** | 顺序传递：A → B → C | 固定流程（生成→审查→发布） |
| **Group Chat（群聊）** | 多 Agent 自由讨论 | 头脑风暴、综合决策 |
| **Hierarchical（层级）** | 多级主管-工人树 | 大型复杂任务 |
| **Debate（辩论）** | 多 Agent 对抗论证 | 质量评审、事实核查 |

### 3.6.2 设计决策要点

1. **单 Agent 优先**：能用单 Agent 解决就不要多 Agent——多 Agent 引入通信开销、协调难度与不确定性。
2. **角色清晰分工**：每个 Agent 只做一件事，系统提示词明确边界。
3. **通信协议化**：定义好消息结构与终止信号（如 TERMINATE）。
4. **成本控制**：多 Agent 会成倍消耗 Token，先算账。
5. **可观测**：记录所有 Agent 间消息，便于排查"话痨"与死循环。

---

## 高质量博客推荐

1. **万字长文讲透 AI Agent 架构设计** — [掘金](https://juejin.cn/post/7397247419467276355)
   从大脑/规划/记忆/工具四要素到多 Agent 模式的系统讲解。
2. **Function Calling 与 ReAct 深度对比** — [百度智能云开发者社区](https://developer.baidu.com/article/details/3381412)
   机制原理、代码示例与选型建议。
3. **ReAct 架构设计模式：让大模型学会思考与行动** — [CSDN](https://blog.csdn.net/fengye_ai/article/details/136194097)
   论文级解读 + LangChain 实现。
4. **AutoGen 多智能体框架实战指南** — [CSDN](https://blog.csdn.net/qq_37530322/article/details/137976564)
   从安装到 GroupChat 协作的完整教程。
5. **多 Agent 系统设计模式与最佳实践（微软研究）** — [微信公众号](https://mp.weixin.qq.com/s/8qZ4h7wQvFmJTb3yFkpHxw)
   一线团队多 Agent 落地经验与踩坑总结。

## 动手实践

1. 用 OpenAI 兼容接口实现"两步函数调用"（查天气→算温差），不用框架手写循环。
2. 用 LangChain AgentExecutor 实现一个 ReAct 智能体（搜索 + 计算）。
3. 用 AutoGen 实现"写代码 Agent + 执行 Agent"协作完成一个算法任务。
4. 设计并实现一个 Supervisor 多 Agent 架构，完成"资料收集→报告撰写"。

## 常见问题（FAQ）

**Q1：Agent 死循环/话痨怎么办？**
A：三招：①`max_iterations` 硬限制；②明确终止条件（如"当...时回复 FINISH"）；③加"循环检测"（重复动作达到阈值即终止）。

**Q2：多 Agent 一定比单 Agent 强吗？**
A：不一定。多 Agent 适合任务可分解、需要多角色互补的场景；简单任务多 Agent 反而更慢更贵。评估标准是"效果/成本"比。

**Q3：Function Calling 和 ReAct 怎么选？**
A：单步工具调用用 Function Calling（API 原生支持、可靠）；需要多步推理+工具交替用 ReAct；明确多步骤长任务用 Plan-and-Execute。
