# Agent 工作流基本知识与搭建方法

> 本文档系统性地介绍 AI Agent 工作流的核心概念、主流框架、环境搭建、实现方法以及最佳实践，适合 AI 应用开发者、架构师及技术决策者参考。

---

## 目录

1. [Agent 工作流基本概念](#1-agent-工作流基本概念)
2. [Agent 核心架构](#2-agent-核心架构)
3. [主要 Agent 框架对比](#3-主要-agent-框架对比)
4. [搭建环境需求](#4-搭建环境需求)
5. [Agent 工作流搭建方法](#5-agent-工作流搭建方法)
6. [实战案例：构建一个智能文档分析 Agent](#6-实战案例构建一个智能文档分析-agent)
7. [Agent 工作流最佳实践](#7-agent-工作流最佳实践)
8. [常见问题与解决方案](#8-常见问题与解决方案)
9. [对比总结表](#9-对比总结表)

---

## 1. Agent 工作流基本概念

### 1.1 什么是 Agent 工作流

**Agent（智能体）工作流**是指由 LLM（大语言模型）驱动的自主程序，能够根据既定目标，自主地感知环境、进行推理、制定计划、调用工具并迭代执行，直至完成任务的一系列步骤与规则的集合。

Agent 的本质是将 LLM 从"被动的问答机器"升级为"主动的任务执行者"。

**核心特征：**

| 特征 | 描述 |
|------|------|
| **自主性 (Autonomous)** | 无需人类逐步指导，Agent 能自行决定下一步行动 |
| **目标驱动 (Goal-Driven)** | 围绕给定的目标进行规划和执行，而非仅响应当前输入 |
| **工具使用 (Tool-Using)** | 能够调用外部工具（搜索引擎、计算器、API、数据库等）来扩展能力边界 |
| **迭代执行 (Iterative)** | 通过"执行-反馈-调整"循环逐步逼近目标 |
| **记忆系统 (Memory)** | 具备短期/长期记忆，能跨多轮交互记住上下文 |
| **反思能力 (Self-Reflection)** | 能评估自身输出的质量，发现错误并自我纠正 |

### 1.2 Agent vs 传统自动化 vs RPA

```
+-------------------+-------------------+-------------------+
|     对比维度      |   传统自动化脚本   |  RPA (机器人流程)  |     AI Agent      |
+-------------------+-------------------+-------------------+-------------------+
| 规则驱动 vs 目标驱动|   纯规则驱动      |   规则驱动+录屏    |   目标驱动，自主规划 |
| 适应能力          |   无              |   低              |   高               |
| 非结构化数据处理  |   不支持          |   有限            |   原生支持          |
| 决策能力          |   无              |   无              |   具备推理与决策    |
| 工具调用          |   预定义          |   预定义          |   动态发现与调用    |
| 容错性            |   差              |   一般            |   强（自我纠错）    |
| 使用场景          |   固定批量任务    |   UI 桌面自动化   |   复杂认知任务      |
+-------------------+-------------------+-------------------+-------------------+
```

**本质区别：** 传统自动化和 RPA 是"如果 A 则做 B"的确定性系统；Agent 是"为了实现目标 G，我需要做 X、Y、Z"的非确定性推理系统。

### 1.3 Agent 能力模型

Agent 的完整能力可以抽象为以下五层循环模型：

```
                         +------------------+
                         |    Perception    |  <-- 感知：接收输入
                         |  (感知/理解输入)  |      文本、图像、音频、API 数据
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Reasoning     |  <-- 推理：分析问题
                         |  (推理/分析问题)  |      理解意图、提取关键信息
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Planning      |  <-- 规划：制定方案
                         |   (规划/分解任务) |      任务分解、步骤排序、资源评估
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Execution     |  <-- 执行：调用工具
                         |   (执行/调用工具) |      API 调用、代码运行、搜索
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Feedback      |  <-- 反馈：评估结果
                         |   (反馈/评估调整) |      结果验证、错误检测、策略调整
                         +------------------+
                                  |
                                  |  (循环回到 Perception 或结束)
                                  v
                          [目标达成 / 异常退出]
```

### 1.4 Agent 成熟度模型（L1-L6）

在工业界和学术界，Agent 的发展可以划分为六个成熟度级别：

```
L1: Simple Chain (简单链式)
    └── 固定的线性步骤，无分支逻辑
        示例：文档摘要流水线（读取 -> 分块 -> 总结 -> 输出）

L2: Tool-Using (工具调用)
    └── LLM 能根据上下文自主决定调用哪个工具
        示例：天气查询 Agent（理解用户意图 -> 调用天气 API -> 格式化返回）

L3: Multi-Step Reasoning (多步推理)
    └── 结合 CoT / ReAct 进行多步推理与工具组合
        示例：旅行规划 Agent（搜索航班 -> 比较价格 -> 推荐酒店 -> 生成行程）

L4: Autonomous Planning (自主规划)
    └── 自主分解任务，动态调整计划，具备错误恢复能力
        示例：软件开发 Agent（分析需求 -> 设计架构 -> 编写代码 -> 测试 -> 修复）

L5: Multi-Agent Collaboration (多 Agent 协作)
    └── 多个专业 Agent 分工协作，通过消息通信协调
        示例：内容创作团队（研究员 + 写手 + 编辑 + 排版 协同工作）

L6: Self-Improving (自我进化)
    └── Agent 能从历史经验中学习，优化自身行为策略
        示例：持续从用户反馈中学习的长期运行 Agent
```

---

## 2. Agent 核心架构

### 2.1 Agent 主循环 (The Agent Loop)

Agent 的运行本质是一个不断迭代的感知-决策-执行循环：

```
+===========================================================================+
||                          THE AGENT LOOP                                  ||
+===========================================================================+
||                                                                         ||
||    +----------+    +----------+    +----------+    +----------+         ||
||    |          |    |          |    |          |    |          |         ||
||    | OBSERVE  |--> |  THINK   |--> |  DECIDE  |--> |   ACT    |----+    ||
||    |          |    |          |    |          |    |          |    |    ||
||    +----------+    +----------+    +----------+    +----------+    |    ||
||         ^                                                          |    ||
||         |                     FEEDBACK                              |    ||
||         +----------------------------------------------------------+    ||
||                                                                         ||
||    观察环境状态     理解并推理        选择下一步行动     执行工具调用       ||
||    (感知输入)     (分析上下文)      (规划行动路径)    (副作用产生)        ||
||                                                                         ||
+===========================================================================+

详细流程：

  1. OBSERVE:  读取当前状态 (State)，包括用户输入、对话历史、上一步工具返回
  2. THINK:    LLM 分析当前状态，理解上下文，推理可能的解决方案
  3. DECIDE:   选择下一步行动 — 调用工具、返回用户、或结束任务
  4. ACT:      执行选定的行动 — 调用 API、运行代码、搜索信息
  5. FEEDBACK: 将行动结果写回状态，评估是否达成目标
     如果目标未达成: 回到 OBSERVE (继续循环)
     如果目标已达成: 退出循环，返回最终结果
```

**伪代码实现：**

```python
def agent_loop(task: str, tools: list, max_iterations: int = 50) -> str:
    state = initialize_state(user_input=task)
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": task}]

    for iteration in range(max_iterations):
        # Step 1 & 2 & 3: Observe + Think + Decide (LLM Call)
        response = llm.chat(messages, tools=tools)

        # Check if agent wants to respond to user
        if response.has_text_output():
            messages.append(response.message)
            state["final_output"] = response.text
            return state["final_output"]  # Task complete

        # Step 4: Act - Execute tool calls
        for tool_call in response.tool_calls:
            tool_result = execute_tool(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            state["tool_results"].append({tool_call.name: tool_result})

        # Step 5: Feedback - Evaluate if goal is achieved
        if evaluate_completion(state, task):
            return state["final_output"]

    raise MaxIterationsExceeded(f"Agent did not finish within {max_iterations} iterations")
```

### 2.2 Context Window 管理

LLM 的上下文窗口是 Agent 最稀缺的资源，需要精细管理：

```
+===========================================================+
|                  CONTEXT WINDOW LAYOUT                     |
+===========================================================+
|  System Prompt      |  固定，~500-2000 tokens              |
|  (角色+规则+工具)    |  定义 Agent 行为边界                 |
+---------------------+--------------------------------------+
|  Tool Definitions   |  固定，~200-2000 tokens              |
|  (工具名称+描述+参)  |  每个工具 ~50-200 tokens             |
+---------------------+--------------------------------------+
|  Conversation       |  增长中...                           |
|  History            |  每轮 ~200-2000 tokens               |
|  (用户+助手+工具)    |  旧轮次需要压缩或丢弃                 |
+---------------------+--------------------------------------+
|  Working Memory     |  变化，~200-1000 tokens              |
|  (便签/中间结果)     |  关键信息的手动存储                   |
+---------------------+--------------------------------------+
|  Retrieved Context  |  动态，~1000-5000 tokens             |
|  (RAG 检索结果)     |  从向量库检索的相关文档               |
+---------------------+--------------------------------------+
```

**管理策略：**

- **滑动窗口 (Sliding Window):** 保留最近 N 轮对话，丢弃更早的内容
- **智能摘要 (Smart Summarization):** 对较早的对话进行逐步摘要压缩
- **向量检索 (Vector Retrieval):** 将历史存为向量，按需检索相关片段
- **分层存储 (Hierarchical Storage):** 热点数据放上下文，温/冷数据放外部存储

### 2.3 Tool Registry 与 Tool Calling

Tool Registry 是 Agent 的工具注册中心，负责管理所有可用工具的定义、调用和权限。

**工具定义标准格式（OpenAI Function Calling 兼容）：**

```json
{
  "type": "function",
  "function": {
    "name": "web_search",
    "description": "Search the internet for current information. Use this when you need to find facts, news, or data that may not be in your training data.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The search query string. Be specific and include relevant keywords."
        },
        "max_results": {
          "type": "integer",
          "description": "Maximum number of results to return (1-20). Default is 5.",
          "default": 5
        }
      },
      "required": ["query"]
    }
  }
}
```

**Tool Registry 架构：**

```
+=====================================================+
|                  TOOL REGISTRY                       |
+=====================================================+
|                                                      |
|  +---------------+  +---------------+  +----------+ |
|  | Tool: search  |  | Tool: code    |  | Tool: DB | |
|  | permission: r  |  | permission: rw|  | perm: r  | |
|  | timeout: 10s  |  | timeout: 60s  |  | time: 5s | |
|  +---------------+  +---------------+  +----------+ |
|                                                      |
|  Metadata per tool:                                  |
|  - name: 唯一标识符                                   |
|  - description: 自然语言描述（LLM 靠这个选工具）       |
|  - parameters: JSON Schema                          |
|  - permission: read | write | execute | admin        |
|  - timeout_ms: 超时时间                              |
|  - retry_policy: 重试策略                            |
|  - sandbox: 是否需要沙箱环境                          |
+=====================================================+
```

### 2.4 记忆系统 (Memory Systems)

Agent 的记忆分为三个层次：

```
+===========+  +===========+  +===========+
| 短期记忆   |  | 工作记忆   |  | 长期记忆   |
| Short-Term |  | Working   |  | Long-Term |
+===========+  +===========+  +===========+
| 存储: 对话  |  | 存储: 便签  |  | 存储: 向量库 |
|    历史    |  |    中间结果 |  |    知识图谱  |
+===========+  +===========+  +===========+
| 容量: 受   |  | 容量: 手动  |  | 容量: 几乎  |
| Context    |  |    控制    |  |    无限    |
| Window 限制|  |            |  |            |
+===========+  +===========+  +===========+
| 作用: 保持  |  | 作用: 暂存  |  | 作用: 跨    |
| 对话连贯性  |  | 计算中间值  |  | Session    |
|            |  |            |  | 知识持久化  |
+===========+  +===========+  +===========+
| 实现:       |  | 实现:       |  | 实现:       |
| messages[]  |  | scratchpad |  | Vector DB  |
| list        |  | string     |  | + Embedding|
+===========+  +===========+  +===========+
```

**长期记忆实现示例：**

```python
import chromadb
from chromadb.utils import embedding_functions

class LongTermMemory:
    def __init__(self, collection_name: str = "agent_memory"):
        self.client = chromadb.PersistentClient(path="./memory_db")
        self.ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.ef
        )

    def store(self, content: str, metadata: dict = None):
        """存储记忆到向量库"""
        doc_id = f"mem_{hash(content)}_{int(time.time())}"
        self.collection.add(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """检索相关记忆"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results["documents"][0] if results["documents"] else []
```

### 2.5 规划 (Planning)

Agent 的规划能力决定了任务执行的效率和准确性。以下是几种主流的规划模式：

#### ReAct 模式 (Reasoning + Acting)

最经典的 Agent 推理模式，交替进行推理和行动：

```
Thought: 我需要了解今天的天气，然后根据天气建议用户穿什么衣服。
Action: get_weather(city="Beijing")
Observation: 北京今天晴天，气温 15-25°C
Thought: 天气晴朗且温暖，用户应该穿轻便的春秋装。
Action: respond(message="北京今天晴天，气温 15-25°C，建议穿薄外套或卫衣即可。")
```

#### Plan-Execute 模式

先制定完整计划，再逐步执行：

```
Phase 1 - Planning:
  目标: 写一份关于 AI Agent 的技术报告
  计划:
    1. 搜索 AI Agent 最新发展资料
    2. 整理资料，提炼关键观点
    3. 撰写报告大纲
    4. 按照大纲逐节撰写
    5. 自我审阅并修改
    6. 生成最终版本

Phase 2 - Execution:
  [逐步执行上述计划，每步完成后检查结果]
```

#### Tree of Thoughts (ToT)

对复杂问题进行树状探索，评估多条路径后选择最优方案：

```
                     +--------+
                     | Problem |
                     +--------+
                          |
          +---------------+---------------+
          |               |               |
     +----v----+     +----v----+     +----v----+
     | Thought |     | Thought |     | Thought |
     |    A    |     |    B    |     |    C    |
     +----+----+     +----+----+     +----+----+
          |               |               |
     +----v----+     +----v----+     +----v----+
     | Sub-A1  |     | Sub-B1  |     | Sub-C1  |
     +---------+     +---------+     +---------+
          |
     [评估后选择最优分支 A，继续展开]
```

### 2.6 自我反思与错误恢复 (Self-Reflection & Error Recovery)

**反思机制：**

```
Execution --> Result --> Self-Critique --> Adjustment --> Re-Execution
                             |
                     +-------+--------+
                     | 检查点:         |
                     | - 结果是否完整？ |
                     | - 是否有事实错误？|
                     | - 是否偏离目标？ |
                     | - 工具调用是否成功？|
                     +----------------+
```

**错误恢复策略：**

```python
class ErrorRecoveryStrategy:
    RETRY_COUNT = 3
    BACKOFF_FACTOR = 2.0  # Exponential backoff

    async def execute_with_recovery(self, tool_call):
        for attempt in range(self.RETRY_COUNT):
            try:
                result = await self.execute_tool(tool_call)
                if result.status == "success":
                    return result
                elif result.status == "tool_error":
                    # 工具报错 — 将错误信息发给 LLM 让它调整
                    yield self.create_error_feedback(result.error, tool_call)
            except TimeoutError:
                wait_time = self.BACKOFF_FACTOR ** attempt
                await asyncio.sleep(wait_time)
                yield f"Retry attempt {attempt + 1}/{self.RETRY_COUNT}"
        raise Exception(f"Tool {tool_call.name} failed after {self.RETRY_COUNT} attempts")
```

---

## 3. 主要 Agent 框架对比

### 3.1 框架全景图

```
                           Agent 框架生态全景
+===================================================================+
|                                                                   |
|  重量级/完整框架                  轻量级/专用框架                  |
|  +--------------------+          +--------------------+           |
|  | LangGraph          |          | OpenAI Agents SDK   |           |
|  | (StateGraph,       |          | (轻量级, Handoff)    |           |
|  |  Checkpoint,        |          |                     |           |
|  |  Streaming)         |          +--------------------+           |
|  +--------------------+                                           |
|           |                    +--------------------+              |
|  +--------------------+       | Smolagents          |              |
|  | AutoGen (Microsoft) |       | (Code-based Actions) |              |
|  | (Multi-Agent Chat)  |       +--------------------+              |
|  +--------------------+                                           |
|           |                    +--------------------+              |
|  +--------------------+       | PocketFlow          |              |
|  | CrewAI             |       | (轻量 Python)       |              |
|  | (Role-Based)       |       +--------------------+              |
|  +--------------------+                                           |
|                                                                   |
|  可视化/低代码平台                  企业级框架                      |
|  +--------------------+          +--------------------+           |
|  | Dify (开源)        |          | Semantic Kernel     |           |
|  | Coze (字节跳动)     |          | (Microsoft, .NET)   |           |
|  | FastGPT (开源)     |          +--------------------+           |
|  +--------------------+                                           |
|                                                                   |
+===================================================================+
```

### 3.2 LangGraph (LangChain)

**概述：** LangGraph 是 LangChain 生态中的有状态图执行框架，专为构建复杂 Agent 工作流设计。它基于有向图模型，用节点 (Node) 表示计算步骤，用边 (Edge) 表示数据流向，支持条件分支和循环。

**核心架构：**

```
+==============================================================+
|                   LANGGRAPH ARCHITECTURE                      |
+==============================================================+
|                                                               |
|   StateGraph[State]                                           |
|   +--------------------------------------------------+       |
|   |                                                   |       |
|   |   +----------+       +----------+       +------+ |       |
|   |   |   START  |------>|  Node A  |------>| Node | |       |
|   |   +----------+       +----+-----+       |  B   | |       |
|   |                           |             +--+---+ |       |
|   |                           | Cond. Edge     |     |       |
|   |                      +----v----+           |     |       |
|   |                      | Branch  |           |     |       |
|   |                      | Node C  |---------->+     |       |
|   |                      +---------+                 |       |
|   |                                                  |       |
|   |                      +---------+       +------+  |       |
|   |                      |  END    |<------| Node |  |       |
|   |                      +---------+       |  D   |  |       |
|   |                                        +------+  |       |
|   +--------------------------------------------------+       |
|                                                               |
|   Checkpointer: SQLite / Postgres / Memory                    |
|   (持久化状态, 支持 Human-in-the-loop, Time Travel)            |
|                                                               |
+==============================================================+
```

**关键特性：**

| 特性 | 说明 |
|------|------|
| **StateGraph** | 基于 TypedDict/Pydantic 的状态管理，类型安全 |
| **Conditional Edges** | 根据状态值动态选择下一个节点 |
| **Checkpointer** | 内置状态持久化，支持断点续传和时间回溯 |
| **Human-in-the-Loop** | 通过 `interrupt_before`/`interrupt_after` 实现人工介入 |
| **Streaming** | 支持多种流式模式（values, updates, debug, messages） |
| **Subgraph** | 支持嵌套图，实现复杂的层次化工作流 |

**编程模型：**

```python
# 1. 定义 State
# 2. 定义 Nodes (纯函数)
# 3. 定义 Edges (包括条件边)
# 4. Compile 编译为 Runnable
# 5. Invoke / Stream 运行
```

**完整代码示例：**

```python
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# --- Step 1: Define State ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 自动合并消息列表
    task_complete: bool                      # 任务是否完成
    iteration_count: int                     # 迭代计数器

# --- Step 2: Define Tools ---
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Input should be a valid Python expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    # 实际实现会调用搜索 API
    return f"Search results for '{query}': [模拟结果] ..."

tools = [calculator, web_search]
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# --- Step 3: Define Nodes ---
def agent_node(state: AgentState) -> AgentState:
    """Agent 决策节点：调用 LLM 决定下一步"""
    response = llm.invoke(state["messages"])
    return {
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def tool_executor_node(state: AgentState) -> AgentState:
    """工具执行节点：执行 LLM 请求的 tool calls"""
    last_message = state["messages"][-1]
    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        # 找到对应工具并执行
        for t in tools:
            if t.name == tool_name:
                result = t.invoke(tool_args)
                tool_messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"]
                ))
                break
    return {"messages": tool_messages}

# --- Step 4: Define Router (Conditional Edge) ---
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """判断下一步：执行工具还是结束"""
    last_message = state["messages"][-1]
    # 超过最大迭代次数则结束
    if state.get("iteration_count", 0) > 20:
        return "end"
    # 如果有 tool_calls 则执行工具
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # 否则结束
    return "end"

# --- Step 5: Build Graph ---
def build_agent_graph():
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_executor_node)

    # 添加边
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "end": END
    })
    workflow.add_edge("tools", "agent")  # 工具执行后回到 agent

    # 添加 Checkpointer（持久化）
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

# --- Run ---
graph = build_agent_graph()

# 运行并流式获取输出
for event in graph.stream(
    {"messages": [HumanMessage(content="计算 (15 * 8 + 42) / 3，然后告诉我结果")]},
    {"configurable": {"thread_id": "user-session-001"}},
    stream_mode="values"
):
    if "messages" in event:
        last_msg = event["messages"][-1]
        if isinstance(last_msg, AIMessage) and last_msg.content:
            print(f"Agent: {last_msg.content}")
```

**优势：**
- 精细的执行控制，可以精确指定每一步的逻辑
- 内置状态持久化，天然支持 Human-in-the-loop
- 与 LangSmith 集成，提供完整的调试、追踪和评估能力
- 生产级特性：并发、重试、缓存等

**劣势：**
- 学习曲线较陡，需要理解图、节点、边等概念
- 代码量相对较多，简单场景可能显得冗余
- 版本迭代快，API 变化频繁

### 3.3 CrewAI

**概述：** CrewAI 是一个基于"角色扮演"理念的多 Agent 框架。它将 Agent 定义为具有特定角色（Role）、目标（Goal）和背景故事（Backstory）的智能实体，通过 Task 定义任务，通过 Crew 编排协作。

**核心概念：**

```
+===========================================================+
|                   CREWAI STRUCTURE                         |
+===========================================================+
|                                                            |
|   Crew (团队)                                              |
|   +---------------------------------------------------+   |
|   |                                                    |   |
|   |   +----------+    +----------+    +----------+    |   |
|   |   | Agent A  |    | Agent B  |    | Agent C  |    |   |
|   |   | Role:    |    | Role:    |    | Role:    |    |   |
|   |   | 研究员   |    | 分析师   |    | 写作者   |    |   |
|   |   |          |    |          |    |          |    |   |
|   |   | Backstory|    | Backstory|    | Backstory|    |   |
|   |   | "资深.."|    | "数据.."|    | "创意.."|    |   |   |
|   |   +-----+----+    +-----+----+    +-----+----+    |   |
|   |         |               |               |          |   |
|   |         v               v               v          |   |
|   |   +----------+    +----------+    +----------+    |   |
|   |   | Task 1   |    | Task 2   |    | Task 3   |    |   |
|   |   | (输出 -> |--->| (处理 -> |--->| (生成    |    |   |
|   |   |  数据)   |    |  洞察)   |    |  报告)   |    |   |
|   |   +----------+    +----------+    +----------+    |   |
|   |                                                    |   |
|   |   Process: Sequential / Hierarchical               |   |
|   +---------------------------------------------------+   |
|                                                            |
+===========================================================+
```

**完整代码示例：**

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileReadTool

# --- Define Agents ---
researcher = Agent(
    role="高级研究员",
    goal="对给定的主题进行深入、准确的研究，找出关键趋势和洞察",
    backstory=(
        "你是一位拥有15年经验的行业研究员，曾在麦肯锡和Gartner工作。"
        "你擅长快速抓取关键信息，识别行业趋势，并以结构化的方式呈现发现。"
        "你对数据有敏锐的直觉，从不错过任何重要细节。"
    ),
    tools=[SerperDevTool()],
    verbose=True,
    allow_delegation=True
)

analyst = Agent(
    role="数据分析师",
    goal="分析和解读研究数据，提炼出可执行的商业洞察",
    backstory=(
        "你是一位资深数据科学家,擅长从复杂数据中发现模式。"
        "你能用数据讲故事,让非技术人员也能理解深层的洞察。"
        "你注重逻辑严密性,每个结论都有充分的数据支撑。"
    ),
    tools=[FileReadTool()],
    verbose=True
)

writer = Agent(
    role="资深技术写作者",
    goal="将研究和分析结果转化为条理清晰、引人入胜的行业报告",
    backstory=(
        "你是一位顶级技术内容创作者,先后在TechCrunch和The Verge工作。"
        "你擅长将复杂概念简化,写出既专业又易读的内容。"
        "你的文章结构清晰、论证有力、语言流畅。"
    ),
    verbose=True
)

# --- Define Tasks ---
research_task = Task(
    description=(
        "对'{topic}'进行全面的行业研究。"
        "1. 搜索该领域最新发展趋势（2024-2026）"
        "2. 识别主要玩家、市场份额和技术创新"
        "3. 找出3-5个关键趋势及其对行业的影响"
        "4. 整理成结构化的研究报告"
    ),
    expected_output="一份结构化的研究报告，包含市场规模、主要玩家、关键趋势和技术洞察",
    agent=researcher
)

analysis_task = Task(
    description=(
        "基于研究报告，进行深度数据分析："
        "1. 评估各个趋势的商业影响力和可行性"
        "2. 识别最大的市场机会和潜在风险"
        "3. 提供数据驱动的建议"
    ),
    expected_output="一份数据分析报告，包含SWOT分析、机会评估和风险预警",
    agent=analyst,
    context=[research_task]  # 依赖前一个任务
)

writing_task = Task(
    description=(
        "基于研究和分析，撰写一份面向高管的行业洞察报告："
        "1. 执行摘要（300字以内）"
        "2. 市场概览（关键数据可视化描述）"
        "3. 三大关键趋势详细分析"
        "4. 战略建议和行动方案"
        "5. 结论"
    ),
    expected_output="一份完整的面向高管的行业洞察报告，Markdown格式, 2000字以上",
    agent=writer,
    context=[research_task, analysis_task]
)

# --- Create Crew ---
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,  # 顺序执行
    verbose=True
)

# --- Execute ---
result = crew.kickoff(inputs={"topic": "2026年AI Agent技术发展趋势"})
print(result)
```

**优势：**
- 角色化设计直观易懂，非程序员也能理解
- 适合多 Agent 模拟和角色扮演场景
- API 简洁，快速上手

**劣势：**
- 执行流程的灵活控制不如 LangGraph
- 流式支持有限
- 复杂条件分支和循环不够自然

### 3.4 AutoGen (Microsoft)

**概述：** AutoGen 是微软开源的多 Agent 对话框架。核心理念是将 Agent 之间的协作建模为对话（Conversation），支持多种对话模式，包括双人对话、群聊和嵌套对话。

**核心架构：**

```
+===============================================================+
|                    AUTOGEN ARCHITECTURE                        |
+===============================================================+
|                                                                |
|   GroupChat (群聊)                                             |
|   +--------------------------------------------------------+  |
|   |                                                         |  |
|   |   +------------------+   +------------------+          |  |
|   |   | AssistantAgent   |   | UserProxyAgent   |          |  |
|   |   | (AI 助手)        |   | (人类代理/执行器) |          |  |
|   |   | - 推理规划       |   | - 执行代码        |          |  |
|   |   | - 提出方案       |   | - 代表用户        |          |  |
|   |   +--------+---------+   +--------+---------+          |  |
|   |            |                       |                    |  |
|   |            |    +-----------+      |                    |  |
|   |            +--->| 消息队列  |<-----+                    |  |
|   |                 +-----------+                           |  |
|   |                      |                                   |  |
|   |                 +----+----+                              |  |
|   |                 | Speaker |  (Selector 选择下一个发言者)  |  |
|   |                 | Selector|                              |  |
|   |                 +---------+                              |  |
|   +--------------------------------------------------------+  |
|                                                                |
|   对话模式:                                                     |
|   - Two-Agent Chat: Agent A <-> Agent B                       |
|   - Group Chat: N 个 Agent 在群聊中轮流发言                    |
|   - Nested Chat: 一个对话内部触发另一个子对话                   |
|                                                                |
+===============================================================+
```

**完整代码示例（AutoGen 0.7+）：**

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

async def main():
    # --- Model Client ---
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # --- Code Executor (Docker Sandbox) ---
    code_executor = DockerCommandLineCodeExecutor(
        work_dir="coding",
        timeout=60
    )

    # --- Define Agents ---
    assistant = AssistantAgent(
        name="Assistant",
        model_client=model_client,
        system_message=(
            "你是一个数据分析助手。你需要："
            "1. 理解用户的数据分析需求"
            "2. 编写 Python 代码进行分析"
            "3. 将代码交给 CodeRunner 执行"
            "4. 根据执行结果进行分析和总结"
        ),
        description="数据分析助手，负责规划分析和编写代码"
    )

    code_runner = CodeExecutorAgent(
        name="CodeRunner",
        code_executor=code_executor,
        description="代码执行器，运行 Python 代码并返回结果"
    )

    critic = AssistantAgent(
        name="Critic",
        model_client=model_client,
        system_message=(
            "你是代码审查员。检查代码质量、正确性和效率。"
            "如果发现问题，给出具体的改进建议。"
            "如果代码和结果都没有问题，回复 'APPROVE'。"
        ),
        description="代码审查员，检查代码质量"
    )

    # --- Create Group Chat ---
    team = RoundRobinGroupChat(
        participants=[assistant, code_runner, critic],
        termination_condition=TextMentionTermination("APPROVE") | MaxMessageTermination(20)
    )

    # --- Run ---
    task = "分析这份销售数据 sales_data.csv：计算月度增长率、绘制趋势图、找出异常点"
    result = await team.run(task=task)

    print(result)

asyncio.run(main())
```

**优势：**
- 成熟的多 Agent 对话生态，微软持续维护
- 强大的代码执行能力（Docker 沙箱）
- 灵活的对话模式
- 适用于研究和复杂协作场景

**劣势：**
- 配置较复杂，环境依赖多
- 基于对话的模型不如图结构直观
- AutoGen 0.7+ 与之前版本 API 不兼容

### 3.5 OpenAI Agents SDK / Swarm

**概述：** OpenAI 推出的轻量级 Agent 框架。Agents SDK 是 Swarm 实验项目的正式化版本，核心理念是通过 "Handoff"（转交）机制实现 Agent 之间的任务路由。

**核心概念：**

```
+==============================================================+
|               OPENAI AGENTS SDK STRUCTURE                     |
+==============================================================+
|                                                               |
|   Runner (运行器)                                             |
|   +--------------------------------------------------------+ |
|   |                                                         | |
|   |   +------------------+     +------------------+         | |
|   |   | Triage Agent     |     | Specialist Agent |         | |
|   |   | (分流 Agent)      |     | (专业 Agent)     |         | |
|   |   |                  |     |                  |         | |
|   |   | tools: [handoff  |---->| tools: [search,  |         | |
|   |   |  -> billing,     |     |  db_query, ...]  |         | |
|   |   |  -> support,     |     +------------------+         | |
|   |   |  -> sales]       |                                   | |
|   |   +------------------+                                   | |
|   |                                                         | |
|   |   Handoff: Agent A 将对话控制权转交给 Agent B            | |
|   |   Guardrail: 输入/输出安全检查                           | |
|   |   Tracing: 内置追踪和调试                                | |
|   +--------------------------------------------------------+ |
|                                                               |
+==============================================================+
```

**代码示例：**

```python
from agents import Agent, Runner, function_tool, handoff
from agents.guardrail import input_guardrail, GuardrailFunctionOutput

# --- 定义工具 ---
@function_tool
def search_knowledge_base(query: str) -> str:
    """搜索内部知识库"""
    return f"[知识库结果] 关于 '{query}' 的搜索结果..."

@function_tool
def create_ticket(issue: str, priority: str) -> str:
    """创建工单"""
    return f"工单已创建: #{hash(issue) % 10000}, 优先级: {priority}"

# --- 定义 Agent ---
billing_agent = Agent(
    name="Billing Agent",
    instructions="你是账单专家，帮助解决账单和付款问题。",
    tools=[search_knowledge_base, create_ticket]
)

support_agent = Agent(
    name="Support Agent",
    instructions="你是技术支持专家，帮助解决产品使用问题。",
    tools=[search_knowledge_base, create_ticket]
)

# Triage Agent: 分流
triage_agent = Agent(
    name="Triage Agent",
    instructions="根据用户问题判断类型，转交给账单或支持专家。",
    handoffs=[handoff(billing_agent), handoff(support_agent)]
)

# --- 运行 ---
result = Runner.run_sync(
    triage_agent,
    input="我的账单上多了一笔 $99 的收费，能帮我查一下吗？"
)
print(result.final_output)
```

**优势：**
- 极简 API，上手极快
- Handoff 模式自然直观
- 与 OpenAI 生态深度集成

**劣势：**
- 相对较新，生态不如其他框架成熟
- 强依赖 OpenAI 模型
- 复杂工作流编排能力有限

### 3.6 可视化/低代码 Agent 平台

#### Dify

Dify 是开源的可视化 AI 应用构建平台，支持 Agent 工作流的拖拽式搭建。

**核心特性：**
- 可视化工作流编辑器（拖拽节点）
- 内置 RAG Pipeline（文档解析、向量存储、检索）
- 丰富的工具插件市场
- 支持 Chatflow 和 Workflow 两种模式
- 自托管或云服务

```
Dify Workflow 示例：
[Start] -> [LLM: 理解意图] -> [条件分支]
                                 |
                  +--------------+--------------+
                  |              |              |
             [知识库检索]   [Web搜索]    [API调用]
                  |              |              |
                  +--------------+--------------+
                                 |
                          [LLM: 综合回答]
                                 |
                              [End]
```

#### Coze (字节跳动)

Coze 是字节跳动推出的 AI Bot 构建平台，提供免费额度。

**核心特性：**
- 可视化 Bot 编辑器
- 丰富的插件市场（搜索、图片生成、数据分析等）
- 多平台发布（飞书、微信、Discord、Telegram 等）
- 知识库和工作流支持
- 免费 tier 可用

#### FastGPT

FastGPT 是开源的知识库问答平台，专注于知识库 + Agent 场景。

**核心特性：**
- 强大的知识库管理与检索
- 可视化工作流
- 开源可自托管
- 与多种 LLM 兼容

**可视化平台的优势与劣势：**

| 优势 | 劣势 |
|------|------|
| 零代码/低代码，非程序员友好 | 自定义代码能力有限 |
| 快速原型验证 | 供应商依赖和锁定风险 |
| 内置运维和监控 | 复杂逻辑实现困难 |
| 开箱即用的集成 | 大规模生产部署的成本 |

### 3.7 其他值得关注的框架

#### Semantic Kernel (Microsoft)

企业级的 AI 编排框架，深度集成 .NET 和 Azure 生态。

```python
# 支持 Python，但主要优势在 .NET 生态
import semantic_kernel as sk

kernel = sk.Kernel()
kernel.add_service(sk.OpenAIChatCompletion("gpt-4o", api_key="..."))

# 定义插件（工具）
@kernel.register_function(description="Get weather for a city")
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 22°C"

# Planner 自动编排
planner = sk.SequentialPlanner(kernel)
plan = await planner.create_plan("What should I wear in Tokyo?")
result = await plan.invoke(kernel)
```

#### LlamaIndex Agent

LlamaIndex 的 Agent 模块深度集成了 RAG 能力：

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# RAG 查询工具
rag_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="document_search",
    description="Search in the uploaded documents"
)

agent = ReActAgent.from_tools([rag_tool, web_search_tool], llm=llm)
response = agent.chat("What does the document say about AI safety?")
```

#### 其他框架一览

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| **Bee Agent Framework (IBM)** | 开源，TypeScript，企业级 | 需要 TypeScript 的全栈项目 |
| **Agno** | 极轻量，多模态支持 | 快速实验，多模态 Agent |
| **Smolagents (HuggingFace)** | 代码即行动 (Code-as-Action) | 研究实验，HF 生态集成 |
| **PocketFlow (腾讯)** | 轻量 Python，中文友好 | 中文场景，快速上手 |

---

## 4. 搭建环境需求

### 4.1 开发环境

#### 基础环境

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| **Python** | 3.10+ (推荐 3.11/3.12) | 大部分 Agent 框架的基础语言 |
| **Node.js** | 20+ | TypeScript 框架（Bee, Vercel AI SDK）需要 |
| **包管理器** | Poetry / uv / pip | uv 速度最快，Poetry 管理最严格 |
| **Docker** | 24+ | 代码执行沙箱和容器化部署 |
| **Git** | 2.40+ | 版本控制和 prompt 版本管理 |

#### 推荐项目结构

```
my-agent-project/
+-- src/
|   +-- agents/              # Agent 定义
|   |   +-- __init__.py
|   |   +-- research_agent.py
|   |   +-- writing_agent.py
|   +-- tools/               # 工具定义
|   |   +-- __init__.py
|   |   +-- search_tools.py
|   |   +-- file_tools.py
|   +-- workflows/           # 工作流编排
|   |   +-- __init__.py
|   |   +-- research_workflow.py
|   +-- memory/              # 记忆系统
|   |   +-- __init__.py
|   |   +-- vector_store.py
|   +-- prompts/             # 提示词模板
|   |   +-- system_prompts.py
|   +-- api/                 # FastAPI 服务
|   |   +-- main.py
|   +-- config.py            # 配置管理
+-- tests/                   # 测试
+-- docker/                  # Docker 配置
+-- .env.example             # 环境变量模板
+-- pyproject.toml           # 依赖管理
+-- Dockerfile               # 容器化
```

### 4.2 LLM 接入

#### 主流 API 提供商对比

| 提供商 | 代表模型 | 上下文窗口 | Tool Calling | 输入价格/1M tokens | 输出价格/1M tokens | 特点 |
|--------|----------|-----------|-------------|--------------------|--------------------|------|
| **OpenAI** | GPT-4o | 128K | 原生支持 | $2.50 | $10.00 | 综合最强 |
| | GPT-4o-mini | 128K | 原生支持 | $0.15 | $0.60 | 性价比高 |
| | GPT-4.1 | 1M | 原生支持 | $2.00 | $8.00 | 超长上下文 |
| **Anthropic** | Claude Opus 4 | 200K | 原生支持 | $15.00 | $75.00 | 推理最强 |
| | Claude Sonnet 4 | 200K | 原生支持 | $3.00 | $15.00 | 速度+质量均衡 |
| | Claude Haiku 3.5 | 200K | 原生支持 | $0.80 | $4.00 | 最快最低价 |
| **DeepSeek** | DeepSeek-V3 | 128K | 原生支持 | ~$0.27 | ~$1.10 | 极低价格 |
| | DeepSeek-R1 | 128K | 支持 | ~$0.55 | ~$2.19 | 推理特化 |
| **智谱 (Zhipu)** | GLM-4-Plus | 128K | 原生支持 | ￥10 | ￥10 | 国产最强之一 |
| **阿里百炼** | Qwen3-235B | 128K | 原生支持 | ￥4 | ￥12 | 多模态+超长 |
| | Qwen3-32B | 128K | 原生支持 | ￥0.7 | ￥2.1 | 高性价比 |
| **Moonshot** | Kimi-K2 | 128K | 原生支持 | ￥2 | ￥8 | 长文本处理 |
| **百川 (Baichuan)** | Baichuan4 | 32K | 支持 | ￥0.25 | ￥0.50 | 中文优化 |

#### 本地模型选项

```bash
# Ollama — 最简单的本地模型部署
ollama pull qwen3:32b
ollama pull llama3.3:70b
ollama pull deepseek-r1:32b

# vLLM — 高性能推理服务
pip install vllm
vllm serve Qwen/Qwen3-32B-Instruct --port 8000

# llama.cpp — CPU/边缘设备推理
pip install llama-cpp-python
```

#### API Key 管理

```bash
# .env 文件（永远不应提交到 Git）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# LangSmith 追踪（可选）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGCHAIN_PROJECT=my-agent-project

# 搜索 API
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPAPI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

```python
# config.py — 配置加载
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    deepseek_api_key: str = ""
    qwen_api_key: str = ""
    tavily_api_key: str = ""
    langsmith_api_key: str = ""

    default_model: str = "gpt-4o"
    max_iterations: int = 50
    sandbox_enabled: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 4.3 工具与集成

#### 代码执行沙箱

| 方案 | 适用场景 | 安全级别 | 配置复杂度 |
|------|----------|----------|------------|
| **Docker 容器** | 通用代码执行 | 高 | 中 |
| **e2b.dev** | 云端安全沙箱 | 很高 | 低 |
| **subprocess (受限)** | 简单的本地执行 | 低 | 低 |
| **RestrictedPython** | 表达式求值 | 中 | 低 |

```python
# Docker 沙箱执行器
import docker

class DockerSandbox:
    def __init__(self, image: str = "python:3.12-slim", timeout: int = 30):
        self.client = docker.from_env()
        self.image = image
        self.timeout = timeout

    def execute(self, code: str) -> str:
        container = self.client.containers.run(
            self.image,
            command=["python", "-c", code],
            detach=True,
            mem_limit="256m",
            network_disabled=True,      # 禁止网络
            read_only=True,              # 只读文件系统
            security_opt=["no-new-privileges"]
        )
        try:
            result = container.wait(timeout=self.timeout)
            if result["StatusCode"] == 0:
                return container.logs(stdout=True).decode()
            else:
                return f"Error: {container.logs(stderr=True).decode()}"
        finally:
            container.remove(force=True)
```

#### Web 搜索工具

| 服务 | API | 免费额度 | 特点 |
|------|-----|----------|------|
| **Tavily** | tavily.com | 1000/月 | 专为 AI Agent 设计 |
| **SerpAPI** | serpapi.com | 100/月 | 搜索结果结构化 |
| **Bing Search API** | Azure | 按量付费 | Microsoft 生态 |
| **DuckDuckGo** | 免费 | 无限制 | 无需 API Key（注意速率限制） |

#### 文件处理工具

```python
# PDF 解析
import pdfplumber  # 适合提取表格
import PyPDF2      # 适合提取文本
# OCR
import pytesseract
from PIL import Image
# 或使用 API
# Azure Document Intelligence / 百度 OCR
```

#### 数据库连接

```python
from sqlalchemy import create_engine, text

# 使用只读凭证！
DB_URI_READONLY = "postgresql://reader:readonly_pass@host:5432/db"

engine = create_engine(DB_URI_READONLY)

def query_database(sql: str, params: dict = None) -> list[dict]:
    """安全执行查询（只允许 SELECT）"""
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise PermissionError("只允许 SELECT 查询")
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row) for row in result]
```

#### Web 抓取

```python
from playwright.async_api import async_playwright  # 动态页面
from bs4 import BeautifulSoup                      # HTML 解析
import crawl4ai                                    # 专为 AI 设计的爬虫

# crawl4ai 示例
from crawl4ai import AsyncWebCrawler

async def crawl_page(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown  # 返回 Markdown 格式
```

### 4.4 Python 关键依赖

```toml
# pyproject.toml — 完整依赖清单
[project]
name = "my-agent-project"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    # Agent 框架核心
    "langgraph>=0.2.0",
    "langchain>=0.3.0",
    "langchain-openai>=0.2.0",
    "langchain-community>=0.3.0",

    # 多 Agent 框架
    "crewai>=0.80.0",
    "crewai-tools>=0.12.0",
    "autogen-agentchat>=0.7.0",
    "autogen-ext[openai]>=0.7.0",

    # LLM SDK
    "openai>=1.50.0",
    "anthropic>=0.40.0",

    # 数据结构与验证
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "instructor>=1.0",

    # 记忆与向量数据库
    "chromadb>=0.5.0",
    "faiss-cpu>=1.8.0",

    # Web 抓取
    "playwright>=1.45.0",
    "beautifulsoup4>=4.12.0",
    "crawl4ai>=0.4.0",

    # 搜索
    "tavily-python>=0.4.0",
    "duckduckgo-search>=6.0",

    # 文件处理
    "pdfplumber>=0.10.0",
    "PyPDF2>=3.0.0",
    "python-docx>=1.1.0",
    "markdownify>=0.3.0",

    # Web 服务
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "streamlit>=1.38.0",

    # 工具
    "python-dotenv>=1.0.0",
    "docker>=7.0.0",
    "httpx>=0.27.0",
    "rich>=13.0.0",
    "tiktoken>=0.7.0",
]
```

---

## 5. Agent 工作流搭建方法

### Step 1: 需求分析

在开始编写任何代码之前，必须明确以下问题：

**需求分析清单：**

```
+=================================================================+
|                Agent 需求分析模板                                  |
+=================================================================+
|                                                                  |
|  1. 核心问题                                                      |
|     - Agent 解决什么问题？                                        |
|     - 没有 Agent 时，这个问题目前是如何解决的？                    |
|     - Agent 方案的核心价值在哪里？                                  |
|                                                                  |
|  2. 用户与使用场景                                                 |
|     - 目标用户是谁？技术能力如何？                                  |
|     - 使用频率和并发量预估？                                        |
|     - 用户在什么上下文中使用 Agent？                                |
|                                                                  |
|  3. 功能需求                                                      |
|     - Agent 需要完成哪些具体任务？                                  |
|     - 各项任务的优先级排序？                                        |
|     - 哪些是必须的，哪些是锦上添花的？                                |
|                                                                  |
|  4. 工具需求                                                      |
|     - 需要哪些外部工具/API？                                       |
|     - 哪些已有，哪些需要新开发？                                    |
|     - 各工具的安全级别要求？                                        |
|                                                                  |
|  5. 自主性等级                                                     |
|     - 期望的成熟度级别 (L1-L6)？                                   |
|     - 哪些环节需要 Human-in-the-loop？                             |
|     - 错误容忍度如何？                                             |
|                                                                  |
|  6. 非功能需求                                                     |
|     - 响应时间要求？                                               |
|     - 成本预算（每次运行）？                                       |
|     - 数据安全和隐私要求？                                         |
|     - 可观测性要求？                                               |
|                                                                  |
|  7. 失败模式分析                                                   |
|     - 最可能出错的环节是什么？                                      |
|     - 错误后果有多严重？                                           |
|     - 如何检测和恢复？                                             |
|                                                                  |
+=================================================================+
```

**需求分析案例：**

```
场景：构建一个"智能合同审查 Agent"

核心问题：法律团队每天需要审查数十份合同，耗费大量时间
当前方案：人工逐条审查，耗时且容易遗漏
Agent 价值：自动识别风险条款，标记异常，提高审查效率 80%

用户：企业法务团队（非技术背景）
自主性：L3（多步推理，但最终决策仍由人完成）
Human-in-the-loop：风险条款标记后需要人工确认

工具需求：
- 文档解析（PDF/DOCX）
- 条款知识库检索
- 风险评分计算
- 条款对比

失败模式：
- 漏检风险条款（高风险 -> 必须 HITL + 置信度阈值）
- 错误标记正常条款（低风险 -> 可接受的一定误报率）
```

### Step 2: 架构设计

基于需求分析，进行架构设计：

```
+===================================================================+
|                     架构设计决策树                                 |
+===================================================================+
|                                                                   |
|   Start                                                           |
|     |                                                             |
|     v                                                             |
|   Single Agent or Multi-Agent?                                    |
|     |                    |                                        |
|     v                    v                                        |
|   单 Agent             多 Agent                                    |
|   (简单到中等复杂度)   (复杂任务, 需要专业化分工)                    |
|     |                    |                                        |
|     v                    v                                        |
|   Sequential or Dynamic?  Hierarchical or Flat?                    |
|     |          |           |            |                         |
|     v          v           v            v                         |
|  顺序链式   动态图      层级式       扁平式                          |
|  (固定流程) (灵活路由)  (管理者-工人)(平等协作)                     |
|                                                                   |
|   框架推荐:                                                        |
|   - 顺序链式: LangGraph(简单图) / Dify / CrewAI(Sequential)        |
|   - 动态图: LangGraph(条件边) / AutoGen(群聊)                      |
|   - 层级式: CrewAI(Hierarchical) / AutoGen(Nested Chat)           |
|   - 扁平式: AutoGen(GroupChat) / OpenAI Agents SDK                |
|                                                                   |
+===================================================================+
```

**架构设计文档模板：**

```
1. 总体架构
   - Agent 数量与角色分工
   - 执行模式（顺序/并行/动态）
   - 通信方式（消息/共享状态）

2. State 设计
   - 哪些数据需要在 Agent 间流动？
   - State 的完整字段定义
   - 持久化策略

3. Memory 设计
   - 哪些信息需要跨 Session 记住？
   - 短期/工作/长期记忆的分配

4. Human-in-the-Loop 节点
   - 哪些节点需要暂停等待人工审批？
   - 审批的粒度（每个输出/关键决策点）

5. 错误处理策略
   - 重试策略
   - 降级方案
   - 超时处理

6. 工具集成方案
   - 工具列表与权限分级
   - API 密钥/凭证管理
```

### Step 3: 工具定义

**标准工具定义规范：**

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class ToolDefinition(BaseModel):
    """工具定义的标准化模型"""
    name: str
    description: str
    parameters: dict  # JSON Schema
    permission: Literal["read", "write", "execute", "deploy"]
    timeout_ms: int = 30000
    retry_count: int = 2
    requires_sandbox: bool = False
    requires_confirmation: bool = False
```

**工具描述最佳实践（写给 LLM 看的）：**

```python
# 好的工具描述 ✅
GOOD_DESCRIPTION = (
    "Search the internal employee database by name or department. "
    "Returns a list of matching employees with their email, title, and department. "
    "Use this when the user asks about specific employees or teams. "
    "Do NOT use for general company information — use company_search instead. "
    "This is a READ-ONLY operation."
)

# 不好的工具描述 ❌
BAD_DESCRIPTION = "Search employee database"
```

**工具权限分级模型：**

```
+===========================================================+
|               TOOL PERMISSION ESCALATION                   |
+===========================================================+
|                                                            |
|   Level 0: READ (只读)                                    |
|   - 无副作用，可安全重试                                    |
|   - 示例: 搜索、读文件、查数据库、获取 API 数据             |
|   +--------------------------------------------------+    |
|                                                        |
|   Level 1: WRITE (写入)                                |
|   - 有副作用但可逆                                       |
|   - 示例: 创建文件、写入草稿、创建数据库记录               |
|   - 需要: 确认或审批                                    |
|   +--------------------------------------------------+    |
|                                                        |
|   Level 2: EXECUTE (执行)                               |
|   - 运行代码或触发外部系统                                |
|   - 示例: 运行 Python 代码、发送 HTTP 请求、调用第三方 API |
|   - 需要: 沙箱环境 + 资源限制 + 超时控制                   |
|   +--------------------------------------------------+    |
|                                                        |
|   Level 3: DEPLOY (部署)                                |
|   - 修改生产环境                                        |
|   - 示例: 部署代码、修改配置、触发 CI/CD                  |
|   - 需要: 多层审批 + 完整审计日志                        |
|   +--------------------------------------------------+    |
|                                                            |
+===========================================================+
```

### Step 4: 系统提示词设计

Agent 的系统提示词是决定其行为和效果的关键因素。一个好的 Agent 系统提示词应该结构清晰、指令明确。

**系统提示词模板：**

```markdown
## 身份 (Identity)
你是一个 [角色名称]，专门负责 [核心职责]。
你的首要目标是 [主要目标]。

## 能力 (Capabilities)
你可以使用以下工具来完成工作：
1. **tool_name_1**: [工具描述和适用场景]
2. **tool_name_2**: [工具描述和适用场景]

## 工作流程 (Workflow)
遵循以下步骤完成任务：
1. [第一步：分析和理解]
2. [第二步：信息收集]
3. [第三步：执行和行动]
4. [第四步：验证和调整]
5. [第五步：输出最终结果]

## 约束规则 (Constraints)
- [关键约束 1]
- [关键约束 2]
- 如果遇到无法处理的情况，不要编造答案，明确告知用户你的限制
- 每次行动前，评估风险和副作用

## 工具使用指南 (Tool Usage Guidelines)
- 优先使用只读工具获取信息
- 写入操作前向用户确认
- 如果一个工具连续失败 2 次，尝试其他方案或向用户求助
- 并行调用不相互依赖的工具以提高效率

## 输出格式 (Output Format)
- 最终输出使用 Markdown 格式
- 涉及数据的部分使用表格呈现
- 代码使用代码块并指定语言
- 引用来源时注明出处

## 错误处理 (Error Handling)
- 工具调用失败：重试 1 次，若仍失败则使用备选方案
- 信息不足：明确列出需要补充的信息
- 超出能力范围：诚实地说明限制，而不是掩盖
```

**完整示例：研究 Agent 的系统提示词：**

```python
RESEARCHER_SYSTEM_PROMPT = """## 身份
你是一位资深研究分析师，专门负责对给定主题进行深入、准确的研究。
你的研究结果将被用于撰写高质量的分析报告。

## 可用工具
1. **web_search(query, max_results=5)**: 搜索互联网获取最新信息。适用于查找新闻、数据、趋势。
2. **fetch_page(url)**: 获取网页内容。适用于深入阅读特定来源。
3. **save_note(content, category)**: 保存研究发现到笔记。适用于记录关键发现。

## 工作流程
1. 分析研究主题，拆解为 2-4 个子话题
2. 对每个子话题进行搜索
3. 从搜索结果中筛选高质量的页面进行深入阅读
4. 将关键发现保存到笔记中
5. 汇总所有发现，生成研究报告

## 约束规则
- 优先使用权威来源（政府网站、学术期刊、知名媒体）
- 交叉验证关键信息（至少 2 个独立来源确认）
- 明确标注信息的时效性
- 区分事实和观点
- 如果搜索结果不相关，调整搜索关键词而不是重复同样的搜索

## 输出格式
研究报告使用以下结构：
# [主题] 研究报告
## 1. 概览 (2-3 句话总结)
## 2. 关键发现
### 2.1 [发现 1 标题]
[详细内容，附带来源]
### 2.2 [发现 2 标题]
[详细内容，附带来源]
## 3. 数据与统计
[表格呈现关键数据]
## 4. 趋势分析
## 5. 结论与建议

## 错误处理
- 搜索无结果：尝试调整搜索词，若 3 次仍无果则报告"信息不足"
- 页面无法访问：尝试从缓存或其他来源获取
- 信息矛盾：标注矛盾点，说明各来源的说法，不做主观判断
"""
```

### Step 5: 实现 — LangGraph 完整示例

**研究+写作 Agent 完整实现：**

```python
"""
研究+写作 Agent — 基于 LangGraph 的完整实现
功能：用户给出主题 -> Agent 搜索资料 -> 撰写报告 -> 人工审阅
"""

import os
import json
import operator
from typing import TypedDict, Annotated, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage, AIMessage, ToolMessage, SystemMessage
)
import sqlite3

# ============================================================
# Configuration
# ============================================================
MODEL_NAME = "gpt-4o"
MAX_ITERATIONS = 30
MAX_SEARCH_RESULTS = 5

# ============================================================
# State Definition
# ============================================================
class ResearchState(TypedDict):
    """研究工作流的完整状态"""
    messages: Annotated[list, add_messages]
    research_notes: Annotated[list, operator.add]  # 收集的研究笔记
    draft: str                                      # 报告草稿
    final_report: str                               # 最终报告
    phase: str                                      # 当前阶段
    iteration_count: int                            # 迭代计数

# ============================================================
# Tool Definitions
# ============================================================
@tool
def web_search(query: str, max_results: int = MAX_SEARCH_RESULTS) -> str:
    """
    Search the internet for current information about a topic.
    Use this to find facts, news, data, and latest developments.
    Be specific in your query — include key terms and time ranges if relevant.

    Args:
        query: The search query string
        max_results: Maximum number of results (1-10, default 5)
    """
    # 实际使用时替换为 Tavily/SerpAPI 等
    print(f"  [TOOL] Searching: {query}")
    return json.dumps({
        "query": query,
        "results": [
            {
                "title": f"Result {i} for: {query}",
                "snippet": f"This is a simulated search result snippet for '{query}'. In production, this would contain actual content from the web.",
                "url": f"https://example.com/result-{i}"
            }
            for i in range(1, min(max_results + 1, 4))
        ]
    })

@tool
def fetch_page_content(url: str) -> str:
    """
    Fetch and extract the main content of a web page.
    Use this to read articles or pages that were found via search.

    Args:
        url: The full URL of the page to fetch
    """
    print(f"  [TOOL] Fetching: {url}")
    return f"[Page content from {url}]: Detailed article content would appear here in production. For now, this is simulated content relevant to the research topic."

@tool
def save_research_note(content: str, category: str = "general") -> str:
    """
    Save a research finding to the research notes. Use this to record
    key facts, quotes, or insights discovered during research.

    Args:
        content: The research finding to save. Be concise but complete.
        category: Category label for organization (e.g., 'statistics', 'quote', 'trend')
    """
    print(f"  [TOOL] Saving note [{category}]: {content[:100]}...")
    return f"Note saved in category '{category}'"

TOOLS = [web_search, fetch_page_content, save_research_note]

# ============================================================
# System Prompts
# ============================================================
RESEARCHER_PROMPT = """## 身份
你是一位资深研究分析师。你的任务是对给定主题进行深入研究，收集足够的信息用于撰写高质量报告。

## 工作流程
1. 分析研究主题，确定需要覆盖的关键方面
2. 使用 web_search 搜索每个关键方面
3. 使用 fetch_page_content 深入阅读重要的文章
4. 使用 save_research_note 记录所有重要发现
5. 当你收集了足够的信息（至少 5-8 条有质量的笔记），回复 "RESEARCH_COMPLETE" 并附上研究摘要

## 搜索策略
- 第一次搜索使用较宽泛的关键词
- 根据搜索结果，进行更有针对性的后续搜索
- 确保覆盖多个角度和观点
- 优先搜索权威来源

## 注意
- 不要重复搜索相同或非常相似的内容
- 每条笔记只记录一个核心观点
- 在笔记中标注信息来源
"""

WRITER_PROMPT = """## 身份
你是一位资深技术写作专家。你的任务是基于研究发现撰写高质量报告。

## 报告结构
# [标题]
## 执行摘要
## 1. 背景与概述
## 2. 核心发现
## 3. 数据与分析
## 4. 趋势与展望
## 5. 结论与建议

## 写作风格
- 专业但不晦涩，面向有一定技术背景的读者
- 数据驱动，每个观点尽量有数据支撑
- 结构清晰，善用标题、列表和表格
- 引用时要注明来源

## 输出
使用 Markdown 格式输出完整报告。报告至少 1500 字。
"""

REVIEWER_PROMPT = """## 身份
你是一位严格的编辑审阅员。你的任务是审阅报告草稿，提出修改意见。

## 审阅标准
1. 事实准确性：数据和引用是否正确？
2. 逻辑完整性：论证链条是否完整？
3. 结构清晰度：章节组织是否合理？
4. 语言质量：表达是否精准流畅？

## 输出
如果报告质量合格，回复 "APPROVED"。
如果需要修改，输出具体的修改建议（按优先级排列）。
"""

# ============================================================
# Node Implementations
# ============================================================
class ResearchWorkflow:
    def __init__(self):
        self.llm = ChatOpenAI(model=MODEL_NAME, temperature=0.7)
        self.llm_with_tools = self.llm.bind_tools(TOOLS)

    async def planner_node(self, state: ResearchState) -> dict:
        """规划节点：分析主题并生成研究计划"""
        user_input = state["messages"][0].content if state["messages"] else ""
        plan_prompt = f"""分析以下研究主题，生成一个结构化的研究计划：

主题: {user_input}

请输出：
1. 关键研究方面（3-5个）
2. 推荐的搜索关键词（每个方面 1-2 个）
3. 报告的大纲框架

以 JSON 格式输出。"""

        response = await self.llm.ainvoke([HumanMessage(content=plan_prompt)])
        return {
            "messages": [response],
            "phase": "planning_complete"
        }

    async def researcher_node(self, state: ResearchState) -> dict:
        """研究节点：使用工具进行信息搜索和收集"""
        messages = state["messages"] + [
            SystemMessage(content=RESEARCHER_PROMPT),
            HumanMessage(content="请开始你的研究。使用搜索工具收集信息，并用 save_research_note 记录发现。")
        ]
        response = await self.llm_with_tools.ainvoke(messages)
        iter_count = state.get("iteration_count", 0) + 1

        return {
            "messages": [response],
            "iteration_count": iter_count,
            "phase": "researching"
        }

    async def tool_executor_node(self, state: ResearchState) -> dict:
        """工具执行节点：执行 LLM 调用的工具"""
        last_message = state["messages"][-1]
        tool_messages = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # 查找并执行工具
            for t in TOOLS:
                if t.name == tool_name:
                    try:
                        result = t.invoke(tool_args)
                    except Exception as e:
                        result = f"Tool execution error: {str(e)}"
                    tool_messages.append(ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    ))
                    # 如果是 save_research_note, 将内容添加到 research_notes
                    if tool_name == "save_research_note":
                        note_entry = {
                            "category": tool_args.get("category", "general"),
                            "content": tool_args.get("content", ""),
                            "timestamp": "now"
                        }
                        state.setdefault("research_notes", []).append(note_entry)
                    break

        return {"messages": tool_messages}

    async def writer_node(self, state: ResearchState) -> dict:
        """写作节点：基于研究笔记撰写报告"""
        notes_text = "\n\n---\n\n".join([
            f"[{n.get('category', 'general')}] {n.get('content', '')}"
            for n in state.get("research_notes", [])
        ])

        if not notes_text:
            notes_text = "（无研究笔记，请基于对话中的信息撰写）"

        prompt = f"{WRITER_PROMPT}\n\n## 研究笔记\n{notes_text}\n\n请基于以上研究笔记撰写完整报告。"
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])

        return {
            "messages": [response],
            "draft": response.content,
            "phase": "draft_complete"
        }

    async def reviewer_node(self, state: ResearchState) -> dict:
        """审阅节点：审查报告质量"""
        draft = state.get("draft", "")

        if not draft:
            return {"phase": "review_failed", "messages": [AIMessage(content="错误：没有找到报告草稿")]}

        prompt = f"{REVIEWER_PROMPT}\n\n## 待审阅报告\n{draft}"
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])

        is_approved = "APPROVED" in response.content.upper()

        return {
            "messages": [response],
            "phase": "approved" if is_approved else "needs_revision",
            "final_report": draft if is_approved else ""
        }

    async def reviser_node(self, state: ResearchState) -> dict:
        """修改节点：根据审阅意见修改报告"""
        draft = state.get("draft", "")
        feedback = state["messages"][-1].content if state["messages"] else ""

        prompt = f"""请根据以下审阅意见修改报告：

## 审阅意见
{feedback}

## 原报告
{draft}

请输出修改后的完整报告。"""

        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return {
            "messages": [response],
            "draft": response.content,
            "phase": "revision_complete"
        }


# ============================================================
# Routing Logic
# ============================================================
def route_after_researcher(state: ResearchState) -> Literal["tools", "writer"]:
    """研究后路由：继续使用工具 or 进入写作阶段"""
    last_message = state["messages"][-1]
    iter_count = state.get("iteration_count", 0)

    if iter_count >= MAX_ITERATIONS:
        return "writer"

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # 检查是否宣布研究完成
    if hasattr(last_message, "content") and last_message.content:
        if "RESEARCH_COMPLETE" in last_message.content:
            return "writer"

    # 继续研究
    return "writer" if iter_count >= 10 else "tools"

def route_after_review(state: ResearchState) -> Literal["reviser", "end"]:
    """审阅后路由：修改 or 结束"""
    if state.get("phase") == "approved":
        return "end"
    elif state.get("phase") == "needs_revision":
        return "reviser"
    return "end"


# ============================================================
# Graph Construction
# ============================================================
def build_research_graph(checkpointer=None):
    """构建完整的研究 Agent 工作流图"""
    wf = ResearchWorkflow()
    graph = StateGraph(ResearchState)

    # Add nodes
    graph.add_node("planner", wf.planner_node)
    graph.add_node("researcher", wf.researcher_node)
    graph.add_node("tools", wf.tool_executor_node)
    graph.add_node("writer", wf.writer_node)
    graph.add_node("reviewer", wf.reviewer_node)
    graph.add_node("reviser", wf.reviser_node)

    # Add edges
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")

    graph.add_conditional_edges("researcher", route_after_researcher, {
        "tools": "tools",
        "writer": "writer"
    })
    graph.add_edge("tools", "researcher")

    graph.add_edge("writer", "reviewer")
    graph.add_conditional_edges("reviewer", route_after_review, {
        "reviser": "reviser",
        "end": END
    })
    graph.add_edge("reviser", "reviewer")  # 修改后再次审阅

    if checkpointer:
        return graph.compile(checkpointer=checkpointer)
    return graph.compile()


# ============================================================
# Main Execution
# ============================================================
async def main():
    # Setup checkpointer for persistence
    db_path = "./checkpoints.db"
    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    # Build graph
    graph = build_research_graph(checkpointer=checkpointer)

    # Run
    topic = "2026年生成式AI在企业中的应用趋势"
    config = {"configurable": {"thread_id": "research-session-001"}}

    print(f"开始研究: {topic}\n")
    print("=" * 60)

    async for event in graph.astream(
        {"messages": [HumanMessage(content=topic)],
         "research_notes": [],
         "draft": "",
         "final_report": "",
         "phase": "init",
         "iteration_count": 0},
        config,
        stream_mode="values"
    ):
        phase = event.get("phase", "")
        if phase:
            print(f"\n[Phase: {phase}]")

        if "messages" in event and event["messages"]:
            last_msg = event["messages"][-1]
            if isinstance(last_msg, AIMessage) and last_msg.content:
                # Print a preview
                content_preview = last_msg.content[:200]
                print(f"  Output: {content_preview}...")

    # Get final state
    final_state = graph.get_state(config)
    final_report = final_state.values.get("final_report", "")
    if final_report:
        print("\n" + "=" * 60)
        print("FINAL REPORT:")
        print("=" * 60)
        print(final_report)

    conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Step 6: 实现 — CrewAI 完整示例

```python
"""
多 Agent 内容创作团队 — 基于 CrewAI 的完整实现
场景：3 个 Agent 协作完成一篇行业分析文章
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

# ============================================================
# Agent 1: 行业研究员
# ============================================================
researcher = Agent(
    role="行业研究员",
    goal="对'{topic}'进行深入的行业调研，收集最新数据、趋势和案例",
    backstory=(
        "你曾在麦肯锡担任行业分析师 8 年，后加入顶级科技媒体担任资深研究员。"
        "你擅长在短时间内识别行业关键趋势，"
        "从海量信息中提取最有价值的洞察。"
        "你的研究报告多次被行业领袖引用。"
        "你对数据的准确性有强迫症般的追求。"
    ),
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
    verbose=True,
    allow_delegation=False,
    max_iter=15
)

# ============================================================
# Agent 2: 数据分析师
# ============================================================
analyst = Agent(
    role="数据分析师",
    goal="分析研究数据，提炼关键洞察，量化行业趋势",
    backstory=(
        "你是一位资深数据科学家，精通统计分析和数据可视化。"
        "你相信数据比直觉更可靠，每个结论都必须有数据支撑。"
        "你已经帮助超过 50 家公司通过数据驱动的方式制定战略。"
        "你善于从纷杂的数据中发现 hidden pattern。"
    ),
    verbose=True,
    allow_delegation=False
)

# ============================================================
# Agent 3: 内容创作者
# ============================================================
writer = Agent(
    role="资深科技作家",
    goal="基于研究和分析结果，撰写一篇引人入胜且信息丰富的行业分析文章",
    backstory=(
        "你有 12 年的科技写作经验，作品曾发表在《连线》《经济学人》等顶级媒体。"
        "你擅长将复杂的技术概念转化为生动易懂的故事。"
        "你的写作风格：数据驱动、逻辑严密、语言优美。"
        "你深知一篇好文章要有观点、有故事、有数据，三者缺一不可。"
    ),
    verbose=True,
    allow_delegation=False
)

# ============================================================
# Task 1: 研究任务
# ============================================================
research_task = Task(
    description=(
        "对'{topic}'进行全面调研。按以下步骤执行：\n"
        "1. 搜索该领域 2024-2026 年的最新进展（至少 5 次不同角度的搜索）\n"
        "2. 识别 3-5 个最重要的行业趋势\n"
        "3. 收集每个趋势的关键数据：市场规模、增长率、主要玩家\n"
        "4. 找出 2-3 个典型案例\n"
        "5. 整理成结构化研究报告"
    ),
    expected_output=(
        "一份结构化研究报告，包含以下部分：\n"
        "1. 行业概览（2-3段）\n"
        "2. 趋势分析（每个趋势包含：现状、数据、影响评估）\n"
        "3. 典型案例（每个案例 1-2 段）\n"
        "4. 数据附录（关键数据表格）\n"
        "所有信息需注明来源 URL"
    ),
    agent=researcher
)

# ============================================================
# Task 2: 分析任务
# ============================================================
analysis_task = Task(
    description=(
        "基于研究报告，进行深度分析：\n"
        "1. 对每个趋势进行 TAM（可寻址市场）估算\n"
        "2. 评估各趋势的成熟度和商业可行性\n"
        "3. 进行竞争力分析（波特五力或类似框架）\n"
        "4. 识别最大的投资/创业机会\n"
        "5. 提出风险预警"
    ),
    expected_output=(
        "一份数据分析报告，包含：\n"
        "1. 趋势成熟度矩阵（横轴：影响力，纵轴：确定性）\n"
        "2. 市场机会排名与量化评估\n"
        "3. 风险清单及缓解建议\n"
        "4. 3 个具体的商业建议"
    ),
    agent=analyst,
    context=[research_task]
)

# ============================================================
# Task 3: 写作任务
# ============================================================
writing_task = Task(
    description=(
        "基于研究和分析，撰写一篇面向技术管理层的行业分析文章。\n"
        "要求：\n"
        "1. 标题吸引人，能概括核心洞察\n"
        "2. 开头用一个引人深思的数据或故事切入\n"
        "3. 正文分 3-4 个章节，每章展开一个核心趋势\n"
        "4. 使用副标题、列表和加粗增强可读性\n"
        "5. 每个关键论述都要有数据或案例支撑\n"
        "6. 结尾给出前瞻性判断和行动建议\n"
        "7. 字数：2000-3000 字\n"
        "8. 输出格式：Markdown"
    ),
    expected_output="一篇完整的面向技术管理层的行业分析文章，Markdown 格式，2000-3000 字",
    agent=writer,
    context=[research_task, analysis_task]
)

# ============================================================
# Create and Run Crew
# ============================================================
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,
    verbose=True,
    memory=True,    # 启用记忆
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    }
)

# Execute
result = crew.kickoff(inputs={
    "topic": "生成式AI Agent在企业自动化中的应用：2026年趋势与展望"
})
print("=" * 80)
print("FINAL OUTPUT:")
print("=" * 80)
print(result)
```

### Step 7: 实现 — AutoGen 完整示例

```python
"""
数据分析 Agent 团队 — 基于 AutoGen 的完整实现
场景：用户提供数据分析需求，团队协作完成分析并输出报告
"""

import asyncio
from pathlib import Path
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

async def main() -> None:
    # --- Model Client ---
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )

    # --- Code Executor (Docker) ---
    work_dir = Path("coding_workspace")
    work_dir.mkdir(exist_ok=True)

    async with DockerCommandLineCodeExecutor(
        work_dir=work_dir,
        timeout=120,
    ) as code_executor:

        # --- Agent 1: Analyst ---
        analyst = AssistantAgent(
            name="Analyst",
            model_client=model_client,
            system_message=(
                "你是一位资深数据分析师。你的职责是：\n"
                "1. 理解用户的数据分析需求\n"
                "2. 规划分析步骤和方法\n"
                "3. 将分析需求转化为 Python 代码\n"
                "4. 将代码交给 Coder 执行\n"
                "5. 解释执行结果并提出下一步行动\n\n"
                "当分析完成时，回复 '[ANALYSIS_COMPLETE]' 并附上最终分析总结。"
            ),
            description="数据分析师，规划分析方案并编写代码"
        )

        # --- Agent 2: Coder ---
        coder = CodeExecutorAgent(
            name="Coder",
            code_executor=code_executor,
            description="代码执行器，运行 Python 代码并返回执行结果"
        )

        # --- Agent 3: Reviewer ---
        reviewer = AssistantAgent(
            name="Reviewer",
            model_client=model_client,
            system_message=(
                "你是一位代码审查和结果验证专家。你的职责是：\n"
                "1. 审查 Analyst 的代码逻辑是否正确\n"
                "2. 验证执行结果是否符合预期\n"
                "3. 检查数据处理的边界条件\n"
                "4. 确保没有统计错误\n\n"
                "如果一切无误，回复 'APPROVE'。\n"
                "如果发现问题，指出具体问题并建议修正方案。"
            ),
            description="审查员，验证代码和结果的正确性"
        )

        # --- Agent 4: Reporter ---
        reporter = AssistantAgent(
            name="Reporter",
            model_client=model_client,
            system_message=(
                "你是一位数据报告撰写专家。你的职责是：\n"
                "1. 基于分析结果撰写数据分析报告\n"
                "2. 使用 Markdown 格式\n"
                "3. 包含以下章节：\n"
                "   - 分析概述\n"
                "   - 关键发现\n"
                "   - 数据可视化描述\n"
                "   - 结论与建议\n"
                "4. 确保报告面向非技术读者也能理解\n\n"
                "完成报告后回复 'FINAL_REPORT'。"
            ),
            description="报告撰写员，将分析结果转化为可读报告"
        )

        # --- Create Group Chat ---
        team = RoundRobinGroupChat(
            participants=[analyst, coder, reviewer, reporter],
            termination_condition=TextMentionTermination("FINAL_REPORT") | MaxMessageTermination(30),
            max_turns=30
        )

        # --- Run ---
        task = """
        请分析以下销售数据并生成报告：

        数据集: sales_data.csv
        包含字段: date, product_category, region, sales_amount, units_sold, customer_segment

        分析要求:
        1. 整体销售趋势分析（按月汇总）
        2. 产品类别表现对比
        3. 区域销售分布
        4. 客户群体分析
        5. 识别 Top 3 增长机会

        假设数据文件存在，请用 Python 模拟数据并完成分析。
        """

        print("Starting analysis team...\n")
        print("=" * 60)

        stream = team.run_stream(task=task)
        async for message in stream:
            if isinstance(message, TextMessage):
                source = message.source
                content = message.content
                print(f"\n[{source}]:")
                print(content[:300] + ("..." if len(content) > 300 else ""))

        print("\n" + "=" * 60)
        print("Analysis complete!")


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 8: 测试与评估

#### 单元测试 Agent

```python
"""
Agent 单元测试策略
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# ============================================================
# Strategy 1: Mock LLM 响应
# ============================================================
@patch("langchain_openai.ChatOpenAI.ainvoke")
async def test_agent_tool_selection(mock_llm):
    """测试 Agent 在需要搜索时是否选择了正确的工具"""
    # Mock LLM 返回一个 tool call
    mock_response = AIMessage(
        content="",
        tool_calls=[{
            "name": "web_search",
            "args": {"query": "test query"},
            "id": "call_123"
        }]
    )
    mock_llm.return_value = mock_response

    # Run agent node
    state = {"messages": [HumanMessage(content="Search for something")]}
    from my_agent import agent_node
    result = await agent_node(state)

    # Assert tool was called
    assert len(result["messages"]) > 0
    assert hasattr(result["messages"][-1], "tool_calls")
    assert result["messages"][-1].tool_calls[0]["name"] == "web_search"

# ============================================================
# Strategy 2: 集成测试工具执行
# ============================================================
async def test_tool_execution():
    """测试工具是否正确执行"""
    from my_agent.tools import calculator

    result = calculator.invoke({"expression": "2 + 2"})
    assert "4" in result

async def test_tool_error_handling():
    """测试工具错误处理"""
    from my_agent.tools import calculator

    result = calculator.invoke({"expression": "invalid"})
    assert "Error" in result

# ============================================================
# Strategy 3: 端到端工作流测试
# ============================================================
async def test_research_workflow_end_to_end():
    """端到端测试研究工作流"""
    # 使用小型快速模型进行测试
    from my_agent import build_research_graph

    graph = build_research_graph()
    result = await graph.ainvoke({
        "messages": [HumanMessage(content="Test topic: Python programming")],
        "research_notes": [],
        "draft": "",
        "final_report": "",
        "phase": "init",
        "iteration_count": 0
    })

    # 验证工作流完成
    assert result.get("phase") in ["approved", "needs_revision"]
```

#### Agent 评估指标

```
+===============================================================+
|                  AGENT EVALUATION FRAMEWORK                     |
+===============================================================+
|                                                                |
|  Task Completion Rate (任务完成率)                              |
|  - 给定任务集合，Agent 成功完成的百分比                          |
|  - 公式: TCR = Successfully_Completed / Total_Tasks            |
|                                                                |
|  Tool Selection Accuracy (工具选择准确率)                       |
|  - Agent 是否正确选择了执行任务所需的工具                        |
|  - 公式: TSA = Correct_Tool_Selections / Total_Tool_Selections |
|                                                                |
|  Execution Efficiency (执行效率)                                |
|  - 完成任务所需的平均步骤数/时间                                 |
|  - 越少越好（在正确的前提下）                                   |
|                                                                |
|  Output Quality (输出质量)                                      |
|  - 使用 LLM-as-Judge 或人工评分                                 |
|  - 维度: 准确性、完整性、清晰度、有用性                          |
|                                                                |
|  Cost per Task (单任务成本)                                     |
|  - 每次任务的平均 Token 消耗 × 模型单价                          |
|  - 结合质量计算 Cost-Quality Ratio                             |
|                                                                |
|  Failure Recovery Rate (错误恢复率)                             |
|  - 遇到错误后成功恢复的比例                                      |
|  - 公式: FRR = Recovered / Total_Errors                        |
|                                                                |
+===============================================================+
```

#### 追踪与调试工具

| 工具 | 适用框架 | 核心功能 |
|------|----------|----------|
| **LangSmith** | LangChain/LangGraph | 端到端追踪、数据集管理、A/B 测试、回归测试 |
| **Phoenix (Arize)** | 通用 | OpenTelemetry 集成、LLM 追踪、性能监控 |
| **Weights & Biases** | 通用 | 实验追踪、提示词版本管理、模型比较 |
| **LangFuse** | LangChain/LangGraph | 开源、自托管、成本追踪、评估 |

### Step 9: 部署与运维

#### Dockerfile 示例

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# Copy application
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Run
CMD ["uv", "run", "python", "-m", "src.api.main"]
```

#### FastAPI 服务封装

```python
"""
FastAPI Server — Agent 的 HTTP 接口
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uuid
from typing import Optional
import json
from src.agent.workflow import build_research_graph
from src.config import get_settings

app = FastAPI(title="Research Agent API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

settings = get_settings()

# ============================================================
# Models
# ============================================================
class RunRequest(BaseModel):
    topic: str = Field(..., description="Research topic", min_length=5, max_length=500)
    max_iterations: Optional[int] = Field(30, ge=5, le=100)

class RunResponse(BaseModel):
    run_id: str
    status: str

# ============================================================
# In-Memory Run Store (Use Redis/DB in production)
# ============================================================
runs = {}

# ============================================================
# Endpoints
# ============================================================
@app.post("/v1/run", response_model=RunResponse)
async def start_run(request: RunRequest, background_tasks: BackgroundTasks):
    """启动一个新的研究任务"""
    run_id = str(uuid.uuid4())
    runs[run_id] = {"status": "pending", "result": None, "progress": []}

    background_tasks.add_task(execute_agent_run, run_id, request)
    return RunResponse(run_id=run_id, status="pending")

@app.get("/v1/run/{run_id}")
async def get_run_status(run_id: str):
    """查询运行状态"""
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]

@app.get("/v1/run/{run_id}/stream")
async def stream_run(run_id: str):
    """流式获取运行结果 (SSE)"""
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")

    async def event_generator():
        graph = build_research_graph()
        run_data = runs[run_id]
        config = {"configurable": {"thread_id": run_id}}

        async for event in graph.astream(
            {"messages": [HumanMessage(content=run_data["topic"])]},
            config,
            stream_mode="values"
        ):
            run_data["progress"].append(event.get("phase", ""))
            yield f"data: {json.dumps({'phase': event.get('phase', '')}, ensure_ascii=False)}\n\n"

        final_state = graph.get_state(config)
        run_data["result"] = final_state.values.get("final_report", "")
        run_data["status"] = "completed"
        yield f"data: {json.dumps({'phase': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# ============================================================
# Background execution
# ============================================================
async def execute_agent_run(run_id: str, request: RunRequest):
    runs[run_id] = {"status": "running", "result": None, "progress": ["started"], "topic": request.topic}
    # ... 实际执行逻辑 ...
```

#### 速率限制与队列管理

```python
"""
Rate Limiter — 保护 LLM API 不被过量调用
"""
import time
import asyncio
from collections import defaultdict

class TokenBucketRateLimiter:
    """Token Bucket 算法实现速率限制"""

    def __init__(self, rate: int = 60, burst: int = 10):
        """
        rate: 每分钟最大请求数
        burst: 允许的突发请求数
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self.lock:
            now = time.time()
            # 补充 Token
            elapsed = now - self.last_refill
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate / 60)
            self.last_refill = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    async def wait_and_acquire(self) -> None:
        while not await self.acquire():
            await asyncio.sleep(1 / (self.rate / 60))
```

#### 成本追踪

```python
"""
Cost Tracker — 追踪每次 Agent 运行的 Token 消耗与成本
"""
from dataclasses import dataclass, field
from typing import Optional
import tiktoken

# 模型价格 (USD per 1M tokens)
MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    "deepseek-chat": {"input": 0.27, "output": 1.10},
}

@dataclass
class RunCost:
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0

class CostTracker:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
        self.encoder = tiktoken.encoding_for_model(model) if "gpt" in model else None
        self.costs: list[RunCost] = []

    def count_tokens(self, text: str) -> int:
        if self.encoder:
            return len(self.encoder.encode(text))
        # 粗估：中文 ~1.5 chars/token, 英文 ~4 chars/token
        return len(text) // 3

    def track(self, input_text: str, output_text: str) -> RunCost:
        input_tokens = self.count_tokens(input_text)
        output_tokens = self.count_tokens(output_text)
        cost = (input_tokens / 1_000_000 * self.pricing["input"] +
                output_tokens / 1_000_000 * self.pricing["output"])
        run_cost = RunCost(
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=round(cost, 6)
        )
        self.costs.append(run_cost)
        return run_cost

    def total_cost(self) -> float:
        return round(sum(c.cost for c in self.costs), 4)

    def summary(self) -> str:
        return (
            f"Total tokens: {sum(c.input_tokens + c.output_tokens for c in self.costs):,} | "
            f"Total cost: ${self.total_cost():.4f} | "
            f"Runs: {len(self.costs)}"
        )
```

#### 监控指标面板

```
+===============================================================+
|                   AGENT MONITORING DASHBOARD                     |
+===============================================================+
|                                                                 |
|  关键指标 (Grafana / Datadog / LangSmith):                      |
|                                                                 |
|  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  |
|  │  Requests/min   │ │  Avg Latency    │ │  Error Rate     │  |
|  │      24          │ │     3.2s        │ │     1.2%        │  |
|  └─────────────────┘ └─────────────────┘ └─────────────────┘  |
|                                                                 |
|  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  |
|  │  Token Usage/hr │ │  Cost/hr ($USD) │ │  Queue Depth    │  |
|  │    125,000       │ │     0.47        │ │      3          │  |
|  └─────────────────┘ └─────────────────┘ └─────────────────┘  |
|                                                                 |
|  告警规则:                                                      |
|  - 错误率 > 5%: Warning                                        |
|  - 错误率 > 10%: Critical                                      |
|  - 平均延迟 > 10s: Warning                                     |
|  - 每小时成本 > $5: Notification                               |
|                                                                 |
+===============================================================+
```

#### CI/CD Pipeline

```yaml
# .github/workflows/agent-deploy.yml
name: Deploy Agent Service

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'pyproject.toml'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install uv && uv sync
      - name: Run unit tests
        run: uv run pytest tests/ -v --cov=src
      - name: Run agent eval
        run: uv run python -m src.eval.run_eval
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t agent-service:${{ github.sha }} .
      - name: Push to registry
        run: |
          docker tag agent-service:${{ github.sha }} registry.example.com/agent-service:latest
          docker push registry.example.com/agent-service:latest
      - name: Deploy
        run: kubectl rollout restart deployment/agent-service
```

---

## 6. 实战案例：构建一个智能文档分析 Agent

### 6.1 需求分析

构建一个智能文档分析 Agent，能够：
- 接收用户上传的 PDF/DOCX 文档
- 自动解析文档内容（文本、表格、图片）
- 回答用户关于文档内容的问题
- 生成文档摘要和关键信息提取
- 将结构化数据导出到数据库

### 6.2 架构设计

```
+===========================================================================+
|              智能文档分析 Agent — 系统架构                                 |
+===========================================================================+
|                                                                           |
|   ┌──────────────────────────────────────────────────────────────────┐   |
|   │                        Web UI (Streamlit)                         │   |
|   │   [文件上传] [提问输入框] [摘要展示区] [数据表格] [下载按钮]        │   |
|   └──────────────────────────┬───────────────────────────────────────┘   |
|                              │                                            |
|   ┌──────────────────────────v───────────────────────────────────────┐   |
|   │                      FastAPI Server                                │   |
|   │   POST /upload  |  POST /chat  |  GET /summary  |  GET /export   │   |
|   └──────────────────────────┬───────────────────────────────────────┘   |
|                              │                                            |
|   ┌──────────────────────────v───────────────────────────────────────┐   |
|   │                    LangGraph Agent Workflow                        │   |
|   │                                                                    │   |
|   │   +-----------+    +-----------+    +-----------+    +----------+ │   |
|   │   | Document  |    |  Query    |    | Document  |    |  Data    | │   |
|   │   | Parser    |--->|  Router   |--->|  QA Node  |--->|  Export  | │   |
|   │   | Node      |    |  Node     |    |  Node     |    |  Node    | │   |
|   │   +-----------+    +-----------+    +-----------+    +----------+ │   |
|   │         |                |                |                |       │   |
|   │         v                v                v                v       │   |
|   │   +-----------+    +-----------+    +-----------+    +----------+ │   |
|   │   | PDF       |    | Tool-     |    | Vector    |    | SQL      | │   |
|   │   | Parser    |    | Calling   |    | Store     |    | Database | │   |
|   │   | OCR       |    | Search    |    | QA        |    | Writer   | │   |
|   │   +-----------+    +-----------+    +-----------+    +----------+ │   |
|   +-------------------------------------------------------------------+   |
|                                                                           |
+===========================================================================+
```

### 6.3 工具定义

```python
"""
文档分析 Agent — 工具定义
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional
import pdfplumber
import pytesseract
from PIL import Image
import io

# --- Document Parser Tool ---
class DocumentParserTool:
    name = "parse_document"
    description = (
        "Parse and extract text content from an uploaded document (PDF, DOCX, or TXT). "
        "Supports extracting text, tables, and metadata. "
        "Use this first when a document is uploaded to understand its content. "
        "This is a READ-ONLY operation."
    )

    class InputSchema(BaseModel):
        file_id: str = Field(..., description="The ID of the uploaded document")
        extract_tables: bool = Field(True, description="Whether to extract tables")
        page_range: Optional[str] = Field(None, description="Page range, e.g. '1-5'")

    async def execute(self, file_id: str, extract_tables: bool = True,
                      page_range: Optional[str] = None) -> dict:
        """解析文档并返回文本内容"""
        file_path = self._get_file_path(file_id)

        if file_path.endswith(".pdf"):
            return await self._parse_pdf(file_path, extract_tables, page_range)
        elif file_path.endswith(".docx"):
            return await self._parse_docx(file_path)
        else:
            return {"error": f"Unsupported file type: {file_path}",
                    "supported_types": [".pdf", ".docx", ".txt"]}

    async def _parse_pdf(self, path: str, extract_tables: bool,
                         page_range: Optional[str]) -> dict:
        text_content = []
        tables = []

        with pdfplumber.open(path) as pdf:
            pages_to_process = self._resolve_page_range(page_range, len(pdf.pages))
            for page_num in pages_to_process:
                page = pdf.pages[page_num]
                text_content.append(page.extract_text() or "")

                if extract_tables:
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        if table:
                            tables.append(table)

        return {
            "text": "\n\n".join(text_content),
            "tables": tables,
            "total_pages": len(pdf.pages),
            "total_chars": sum(len(t) for t in text_content)
        }

# --- OCR Tool ---
class OCRTool:
    name = "ocr_document"
    description = (
        "Perform OCR (Optical Character Recognition) on image-based PDF pages "
        "or image files. Use this when parse_document returns empty or garbled text "
        "(indicating scanned/image-based content). Supports Chinese and English."
    )

    class InputSchema(BaseModel):
        file_id: str
        language: str = Field("chi_sim+eng", description="OCR languages")
        page_range: Optional[str] = None

    async def execute(self, file_id: str, language: str = "chi_sim+eng",
                      page_range: Optional[str] = None) -> dict:
        # 将 PDF 页面转为图片后进行 OCR
        # ...
        return {"text": "OCR extracted text", "confidence": 0.95}

# --- Document QA Tool ---
class DocumentQATool:
    name = "query_document"
    description = (
        "Search and answer questions based on the parsed document content. "
        "Use this to find specific information, answer user questions, "
        "or extract details mentioned in the document."
    )

    class InputSchema(BaseModel):
        question: str = Field(..., description="The question to answer from the document")
        search_mode: Literal["semantic", "keyword", "hybrid"] = Field(
            "hybrid",
            description="Search strategy"
        )
        top_k: int = Field(5, ge=1, le=20)

    async def execute(self, question: str, search_mode: str = "hybrid",
                      top_k: int = 5) -> dict:
        # 从向量库检索相关片段并回答
        # ...
        return {
            "answer": "Based on the document...",
            "sources": [{"chunk_id": "c1", "text": "...", "page": 3}],
            "confidence": 0.87
        }

# --- Database Writer Tool ---
class DatabaseWriterTool:
    name = "export_to_database"
    description = (
        "Export structured data extracted from the document to the database. "
        "Use this to persist extracted information for later queries. "
        "THIS IS A WRITE OPERATION and requires user confirmation."
    )
    permission = "write"
    requires_confirmation = True

    class InputSchema(BaseModel):
        data: list[dict] = Field(..., description="List of records to insert")
        table_name: str = Field(..., description="Target database table name")
        mode: Literal["insert", "upsert"] = Field("insert")

    async def execute(self, data: list[dict], table_name: str,
                      mode: str = "insert") -> dict:
        # 执行数据库写入
        # ...
        return {"inserted": len(data), "table": table_name}
```

### 6.4 完整 LangGraph 实现

```python
"""
智能文档分析 Agent — 完整 LangGraph 实现
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import sqlite3

# ============================================================
# State
# ============================================================
class DocAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    uploaded_file_id: str
    document_content: dict          # 解析后的文档内容
    current_query: str              # 当前用户查询
    search_results: list            # 检索结果
    extracted_data: list[dict]      # 提取的结构化数据
    phase: str
    iteration_count: int

# ============================================================
# Tools Initialization
# ============================================================
doc_parser = DocumentParserTool()
ocr_tool = OCRTool()
doc_qa = DocumentQATool()
db_writer = DatabaseWriterTool()

ALL_TOOLS = [doc_parser, ocr_tool, doc_qa, db_writer]

# ============================================================
# Nodes
# ============================================================
async def document_parser_node(state: DocAgentState) -> dict:
    """文档解析节点：上传后自动解析文档"""
    file_id = state.get("uploaded_file_id", "")
    if not file_id:
        return {"phase": "no_document",
                "messages": [AIMessage(content="请先上传一个文档。")]}

    result = await doc_parser.execute(file_id=file_id)
    return {
        "document_content": result,
        "phase": "document_parsed",
        "messages": [AIMessage(content=f"文档解析完成：{result.get('total_pages', 0)} 页, "
                                        f"{result.get('total_chars', 0)} 字符。"
                                        f"您可以开始提问了。")]
    }

async def query_router_node(state: DocAgentState) -> dict:
    """查询路由节点：判断用户的查询类型"""
    messages = state["messages"]
    user_query = messages[-1].content if messages else ""

    # 使用轻量模型进行意图分类
    router_prompt = f"""分析以下用户查询的类型，只回复一个 JSON：

用户查询: {user_query}

分类标准:
- "document_qa": 关于文档内容的问题（查找、解释、分析文档中的信息）
- "extract_data": 从文档中提取结构化数据（表格、名单、数字等）
- "generate_summary": 生成文档摘要或总结
- "export": 导出或保存数据

JSON 回复格式: {{"type": "...", "reason": "..."}}"""

    llm = ChatOpenAI(model="gpt-4o-mini")
    response = await llm.ainvoke([HumanMessage(content=router_prompt)])

    try:
        intent = json.loads(response.content)
        query_type = intent.get("type", "document_qa")
    except json.JSONDecodeError:
        query_type = "document_qa"

    return {
        "current_query": user_query,
        "phase": f"routed_to_{query_type}"
    }

async def document_qa_node(state: DocAgentState) -> dict:
    """文档问答节点"""
    query = state.get("current_query", "")
    doc_content = state.get("document_content", {})

    if not doc_content:
        return {"phase": "qa_failed",
                "messages": [AIMessage(content="文档尚未解析，请先上传文档。")]}

    # 使用向量检索 + LLM 回答问题
    result = await doc_qa.execute(question=query)
    return {
        "search_results": result.get("sources", []),
        "phase": "qa_complete",
        "messages": [AIMessage(content=result.get("answer", "无法找到相关信息。"))]
    }

async def summary_node(state: DocAgentState) -> dict:
    """摘要生成节点"""
    doc_text = state.get("document_content", {}).get("text", "")

    if not doc_text:
        return {"phase": "summary_failed",
                "messages": [AIMessage(content="无文档内容可供摘要。")]}

    # 如果是长文档，先分块总结再合并
    summary_prompt = f"""请为以下文档生成一份结构化摘要：

{doc_text[:8000]}  # 前 8000 字符

摘要格式：
## 文档摘要
### 核心主题
### 关键要点（3-5条）
### 重要数据
### 结论"""

    llm = ChatOpenAI(model="gpt-4o")
    response = await llm.ainvoke([HumanMessage(content=summary_prompt)])

    return {
        "phase": "summary_complete",
        "messages": [AIMessage(content=response.content)]
    }

async def data_extraction_node(state: DocAgentState) -> dict:
    """数据提取节点"""
    doc_text = state.get("document_content", {}).get("text", "")
    query = state.get("current_query", "")

    extraction_prompt = f"""从以下文档中提取结构化数据：

文档内容：
{doc_text[:8000]}

提取要求：
{query}

请以 JSON 数组格式输出提取的数据，每条记录是一个对象。"""

    llm = ChatOpenAI(model="gpt-4o")
    response = await llm.ainvoke([HumanMessage(content=extraction_prompt)])

    try:
        # 解析 JSON
        extracted = json.loads(response.content)
    except json.JSONDecodeError:
        # 尝试从响应中提取 JSON 块
        import re
        json_match = re.search(r'\[[\s\S]*\]', response.content)
        extracted = json.loads(json_match.group()) if json_match else []

    return {
        "extracted_data": extracted if isinstance(extracted, list) else [],
        "phase": "extraction_complete",
        "messages": [AIMessage(content=f"提取完成，共 {len(extracted) if isinstance(extracted, list) else 0} 条记录。是否导出到数据库？")]
    }

async def export_node(state: DocAgentState) -> dict:
    """数据导出节点"""
    data = state.get("extracted_data", [])
    if not data:
        return {"phase": "export_failed",
                "messages": [AIMessage(content="没有数据可供导出。请先提取数据。")]}

    result = await db_writer.execute(data=data, table_name="extracted_documents")
    return {
        "phase": "export_complete",
        "messages": [AIMessage(
            content=f"导出完成！已将 {result.get('inserted', 0)} 条记录保存到数据库。"
        )]
    }

# ============================================================
# Router
# ============================================================
def route_by_query_type(state: DocAgentState) -> Literal["qa", "summary", "extract", "export"]:
    phase = state.get("phase", "")
    if "document_qa" in phase:
        return "qa"
    elif "generate_summary" in phase:
        return "summary"
    elif "extract_data" in phase:
        return "extract"
    elif "export" in phase:
        return "export"
    return "qa"  # default

# ============================================================
# Build Graph
# ============================================================
def build_doc_agent_graph():
    graph = StateGraph(DocAgentState)

    graph.add_node("parser", document_parser_node)
    graph.add_node("router", query_router_node)
    graph.add_node("qa", document_qa_node)
    graph.add_node("summary", summary_node)
    graph.add_node("extract", data_extraction_node)
    graph.add_node("export", export_node)

    # Workflow: START -> parser -> router -> {qa|summary|extract|export} -> END
    graph.add_edge(START, "parser")
    graph.add_edge("parser", "router")
    graph.add_conditional_edges("router", route_by_query_type, {
        "qa": "qa",
        "summary": "summary",
        "extract": "extract",
        "export": "export"
    })
    graph.add_edge("qa", END)
    graph.add_edge("summary", END)
    graph.add_edge("extract", END)
    graph.add_edge("export", END)

    return graph.compile()
```

### 6.5 Web UI (Streamlit)

```python
"""
文档分析 Agent — Streamlit UI
"""
import streamlit as st
import requests
import tempfile
import os

st.set_page_config(page_title="智能文档分析 Agent", layout="wide")

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.title("配置")
    api_url = st.text_input("API URL", "http://localhost:8000")
    uploaded_file = st.file_uploader(
        "上传文档",
        type=["pdf", "docx", "txt"],
        help="支持 PDF, DOCX, TXT 格式"
    )

# ============================================================
# Main Area
# ============================================================
st.title("智能文档分析 Agent")
st.markdown("上传文档后，您可以提问、生成摘要或提取数据。")

# Tabs
tab1, tab2, tab3 = st.tabs(["文档问答", "摘要生成", "数据提取"])

# --- Tab 1: Document QA ---
with tab1:
    st.subheader("向文档提问")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if question := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            with st.spinner("分析中..."):
                response = requests.post(
                    f"{api_url}/v1/chat",
                    json={"question": question, "file_id": "uploaded_file"}
                )
                answer = response.json().get("answer", "处理出错")
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

# --- Tab 2: Summary ---
with tab2:
    st.subheader("文档摘要")

    col1, col2 = st.columns(2)
    with col1:
        summary_type = st.radio(
            "摘要类型",
            ["简要摘要 (200字)", "详细摘要 (500字)", "关键要点列表"]
        )
    with col2:
        language = st.radio("语言", ["中文", "英文"])

    if st.button("生成摘要", type="primary"):
        with st.spinner("生成摘要中..."):
            # Call API
            response = requests.post(
                f"{api_url}/v1/summary",
                json={"file_id": "uploaded_file", "type": summary_type}
            )
            summary = response.json().get("summary", "")
            st.markdown(summary)
            st.download_button("下载摘要", summary, "summary.md")

# --- Tab 3: Data Extraction ---
with tab3:
    st.subheader("数据提取")

    extract_prompt = st.text_area(
        "描述你想提取的数据",
        placeholder="例如：提取文档中所有的日期、金额和公司名称..."
    )

    if st.button("提取数据", type="primary"):
        with st.spinner("提取数据中..."):
            response = requests.post(
                f"{api_url}/v1/extract",
                json={"file_id": "uploaded_file", "instruction": extract_prompt}
            )
            data = response.json().get("data", [])

            if data:
                st.success(f"提取到 {len(data)} 条记录")
                st.dataframe(data)

                if st.button("导出到数据库"):
                    export_resp = requests.post(
                        f"{api_url}/v1/export",
                        json={"data": data, "table": "extracted_data"}
                    )
                    if export_resp.status_code == 200:
                        st.success("导出成功！")
```

### 6.6 部署配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://agent:password@postgres:5432/agent_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
      - chroma
    volumes:
      - ./uploads:/app/uploads
      - ./checkpoints.db:/app/checkpoints.db

  agent-ui:
    build:
      context: .
      dockerfile: Dockerfile.ui
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://agent-api:8000
    depends_on:
      - agent-api

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: password
      POSTGRES_DB: agent_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  chroma:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  postgres_data:
  redis_data:
  chroma_data:
```

---

## 7. Agent 工作流最佳实践

### 7.1 Prompt Engineering for Agents

**关于工具使用的提示词：**

```markdown
## 工具使用原则
1. 明确何时使用工具，更重要的是——何时不要使用工具：
   - 对于你训练数据中已经有的常识性知识，不要调用搜索工具
   - 对于简单的问候和对话，直接回复，不要调用任何工具
   - 如果用户连续问了3个相似的问题而搜索都没找到，告诉用户你暂时找不到相关信息

2. 并行 vs 顺序：
   - 多个互不依赖的工具调用应该并行执行（提高效率）
   - 一个工具的输出是另一个工具的输入时，必须顺序执行

3. 工具失败处理：
   - 第一次失败：重试（可能是网络问题）
   - 第二次失败：尝试用不同参数
   - 第三次失败：向用户说明情况，不要再继续尝试
```

### 7.2 工具设计原则

```
+===============================================================+
|                  TOOL DESIGN PRINCIPLES                         |
+===============================================================+
|                                                                |
|  1. ATOMIC (原子性)                                            |
|     - 每个工具只做一件事                                         |
|     - ❌ 不好的设计: do_everything(query)                        |
|     - ✅ 好的设计: search(query) + summarize(text)              |
|                                                                |
|  2. IDEMPOTENT (幂等性)                                        |
|     - 读取操作天然幂等                                          |
|     - 写入操作考虑用 upsert 实现幂等                             |
|                                                                |
|  3. DESCRIPTIVE ERRORS (描述性错误)                              |
|     - 错误信息要具体，能指导 LLM 如何修正                         |
|     - ❌ "Error: failed"                                        |
|     - ✅ "Error: Query too long (max 500 chars). Shorten "     |
|           "your query and retry."                               |
|                                                                |
|  4. TYPED PARAMETERS (类型化参数)                                |
|     - 使用明确的类型（string, number, boolean, enum）            |
|     - 提供默认值                                                |
|     - 标记必填 vs 可选                                          |
|                                                                |
|  5. TESTABLE (可测试)                                          |
|     - 每个工具应该是纯函数或接近纯函数                            |
|     - Mock 外部依赖以便测试                                      |
|                                                                |
+===============================================================+
```

### 7.3 状态管理原则

```python
# 原则 1: Keep State Minimal — 只存储必要的状态
# ❌ 不好: 把整个历史都放进 state
class BloatedState(TypedDict):
    all_responses: list
    all_intermediate_results: list
    full_conversation_log: str
    # ... 太多字段

# ✅ 好: 只存 Agent 间需要传递的关键数据
class LeanState(TypedDict):
    messages: Annotated[list, add_messages]    # 对话历史
    research_findings: list[str]               # 关键发现
    current_phase: str                         # 当前阶段

# 原则 2: Use TypedDict with Annotated Reducers
# 使用 Annotated 指定状态合并策略
class State(TypedDict):
    messages: Annotated[list, add_messages]  # append 而不是覆盖
    counter: Annotated[int, operator.add]   # 累加而不是覆盖
    summary: str                             # 覆盖

# 原则 3: Version Your State Schema
class StateV1(TypedDict):
    query: str
    result: str

class StateV2(TypedDict):
    query: str
    result: str
    confidence: float  # 新增字段，向后兼容
```

### 7.4 错误处理策略

```python
"""
Agent 错误处理 — 多层防御体系
"""
import asyncio
from functools import wraps
from typing import Callable

# Layer 1: 工具级重试
def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    """指数退避重试装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        return f"Error after {max_retries} attempts: {str(e)}"
                    delay = base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator

# Layer 2: 工作流级退化
FALLBACK_CHAIN = {
    "gpt-4o": "gpt-4o-mini",        # 主模型失败 -> 备选模型
    "web_search": "cache_search",    # 实时搜索失败 -> 缓存搜索
    "db_write": "file_export",       # 数据库写入失败 -> 文件导出
}

async def execute_with_fallback(tool_name: str, args: dict) -> str:
    """执行工具，失败时自动降级"""
    try:
        return await execute_tool(tool_name, args)
    except Exception as e:
        fallback = FALLBACK_CHAIN.get(tool_name)
        if fallback:
            print(f"[WARN] {tool_name} failed ({e}), falling back to {fallback}")
            return await execute_tool(fallback, args)
        raise

# Layer 3: 全局熔断器
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        import time

        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise
```

### 7.5 成本优化

```python
"""
成本优化策略
"""
# Strategy 1: Model Routing — 简单任务用小模型
class ModelRouter:
    def __init__(self):
        self.models = {
            "cheap": "gpt-4o-mini",      # $0.15/$0.60 per 1M tokens
            "standard": "gpt-4o",        # $2.50/$10.00 per 1M tokens
            "powerful": "claude-sonnet-4-20250514"  # $3.00/$15.00
        }

    def select_model(self, task_complexity: str) -> str:
        routing = {
            "greeting": "cheap",              # 问候 -> 最便宜的模型
            "simple_qa": "cheap",             # 简单问答 -> 便宜模型
            "text_classification": "cheap",   # 文本分类 -> 便宜模型
            "summarization": "standard",      # 摘要 -> 标准模型
            "complex_reasoning": "powerful",  # 复杂推理 -> 强模型
            "code_generation": "powerful",    # 代码生成 -> 强模型
            "planning": "standard",           # 规划 -> 标准模型
        }
        model_tier = routing.get(task_complexity, "standard")
        return self.models[model_tier]

# Strategy 2: Prompt Caching
# 对于重复发送的 system prompt 和 tool definitions，使用缓存
# OpenAI 会自动缓存超过1024 token的相同前缀
# Anthropic 使用 cache_control 标记

# Strategy 3: Shorter Context
async def compress_messages(messages: list, max_tokens: int = 8000) -> list:
    """压缩消息历史"""
    # 保留 system message 和最近 N 轮对话
    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]

    # 从尾部保留，直到接近 token 限制
    compressed = list(system_msgs)
    token_count = sum(count_tokens(m["content"]) for m in system_msgs)

    for msg in reversed(other_msgs):
        msg_tokens = count_tokens(msg["content"])
        if token_count + msg_tokens > max_tokens:
            # 添加摘要标记
            compressed.insert(len(system_msgs),
                {"role": "system", "content": "[Earlier conversation summarized for brevity]"})
            break
        compressed.insert(len(system_msgs), msg)
        token_count += msg_tokens

    return compressed
```

### 7.6 安全实践

```python
"""
Agent 安全实践
"""
# 1. Input Validation
def validate_tool_input(tool_name: str, params: dict) -> bool:
    """验证工具输入"""
    # 检查 SQL 注入
    if tool_name == "db_query":
        sql = params.get("sql", "").upper()
        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
        for keyword in forbidden:
            if keyword in sql:
                raise PermissionError(f"Forbidden SQL keyword: {keyword}")

    # 检查路径遍历
    if tool_name == "read_file":
        path = params.get("path", "")
        if ".." in path or path.startswith("/"):
            raise PermissionError("Path traversal detected")

    # 检查命令注入
    if tool_name == "execute_command":
        cmd = params.get("command", "")
        dangerous = ["rm -rf", "fork", "reboot", "shutdown", "curl", "wget"]
        for pattern in dangerous:
            if pattern in cmd:
                raise PermissionError(f"Dangerous command: {pattern}")

    return True

# 2. Output Sanitization
def sanitize_output(content: str) -> str:
    """清理输出，移除敏感信息"""
    import re
    # 移除 API Keys
    content = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[REDACTED]', content)
    # 移除邮箱（可选）
    content = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                     '[EMAIL_REDACTED]', content)
    return content

# 3. Permission Gating
class PermissionGate:
    def __init__(self):
        self.need_approval = ["write", "execute", "deploy"]

    async def check(self, tool: str, action: str, user_id: str) -> bool:
        permission = TOOL_PERMISSIONS.get(tool, {}).get(action, "read")
        if permission in self.need_approval:
            return await self.request_approval(tool, action, user_id)
        return True

    async def request_approval(self, tool: str, action: str, user_id: str) -> bool:
        """发送审批请求并等待用户确认"""
        # 实现审批流程...
        pass
```

### 7.7 可观测性

```python
"""
Agent Observability — 结构化日志和追踪
"""
import logging
import json
import time
from contextlib import contextmanager

# Structured Logger
class AgentLogger:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.logger = logging.getLogger(f"agent.{run_id}")

    def log_llm_call(self, model: str, messages: list, response, duration_ms: float):
        self.logger.info(json.dumps({
            "event": "llm_call",
            "run_id": self.run_id,
            "model": model,
            "input_tokens": count_tokens(str(messages)),
            "output_tokens": count_tokens(str(response)),
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time()
        }))

    def log_tool_call(self, tool_name: str, args: dict, result: str, duration_ms: float):
        self.logger.info(json.dumps({
            "event": "tool_call",
            "run_id": self.run_id,
            "tool": tool_name,
            "args_summary": str(args)[:200],
            "result_summary": str(result)[:200],
            "success": "Error" not in str(result),
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time()
        }))

    def log_error(self, error_type: str, message: str, context: dict):
        self.logger.error(json.dumps({
            "event": "agent_error",
            "run_id": self.run_id,
            "error_type": error_type,
            "message": message,
            "context": context,
            "timestamp": time.time()
        }))

# Timing Context Manager
@contextmanager
def timed():
    start = time.time()
    yield
    duration = (time.time() - start) * 1000
    return duration
```

---

## 8. 常见问题与解决方案

### 8.1 Agent 陷入死循环

**问题：** Agent 反复调用同一个工具，或在不同决策之间无限切换。

**原因：**
- 工具返回的结果对 LLM 没有帮助，LLM 无法判断是否已完成
- 条件边的路由逻辑有缺陷
- LLM 在相似工具之间犹豫不决

**解决方案：**

```python
# Solution 1: Max Iterations Guard
MAX_ITERATIONS = 30

def should_continue(state: AgentState) -> str:
    if state.get("iteration_count", 0) >= MAX_ITERATIONS:
        logger.warning(f"Agent exceeded max iterations ({MAX_ITERATIONS})")
        return "force_exit"
    # ... 正常路由逻辑

# Solution 2: Loop Detection
from collections import defaultdict

class LoopDetector:
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.call_history = defaultdict(int)

    def check(self, tool_name: str, args: dict) -> bool:
        key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        self.call_history[key] += 1
        if self.call_history[key] >= self.threshold:
            return True  # Loop detected
        return False

    def inject_stop_message(self):
        """向 Agent 注入停止指令"""
        return ("你似乎在同一操作上重复了多次。"
                "请尝试不同的方法，或者告知用户当前遇到的困难。")

# Solution 3: Decay Factor — 减少重复调用的概率
def adjust_tool_weights(tools, call_history):
    """频繁调用的工具降低权重"""
    for tool in tools:
        repeat_count = call_history.get(tool.name, 0)
        tool.weight *= (0.8 ** repeat_count)
```

### 8.2 工具调用幻觉

**问题：** LLM 调用不存在的工具，或传递不符合 schema 的参数。

**解决方案：**

```python
# Solution 1: Better Tool Descriptions
# 使用具体、明确、区分度高的描述
GOOD_TOOL_DESC = (
    "Search the web for CURRENT news and information (2024-2026). "
    "Use for: latest events, real-time data, news articles. "
    "Do NOT use for: basic definitions, math calculations, "
    "converting units (use the calculator tool instead). "
    "Query should be specific keywords, not full sentences."
)

# Solution 2: Structured Output Validation
from pydantic import ValidationError

def validate_tool_args(tool_call: dict, tool_schema: type[BaseModel]) -> dict:
    try:
        validated = tool_schema(**tool_call["args"])
        return {"valid": True, "args": validated.model_dump()}
    except ValidationError as e:
        return {
            "valid": False,
            "errors": e.errors(),
            "suggestion": f"Expected schema: {tool_schema.model_json_schema()}"
        }

# Solution 3: Fuzzy Tool Matching
from difflib import get_close_matches

AVAILABLE_TOOLS = ["web_search", "web_fetch", "db_query", "calculate"]

def resolve_tool_name(requested: str) -> str:
    """模糊匹配工具名"""
    if requested in AVAILABLE_TOOLS:
        return requested
    matches = get_close_matches(requested, AVAILABLE_TOOLS, n=1, cutoff=0.6)
    if matches:
        logger.warning(f"Tool name '{requested}' not found, using '{matches[0]}' instead")
        return matches[0]
    raise ValueError(f"Unknown tool '{requested}'. Available: {AVAILABLE_TOOLS}")
```

### 8.3 高延迟

**问题：** Agent 响应时间过长，用户体验差。

**解决方案：**

```python
# Solution 1: Parallel Tool Calls
async def execute_tools_parallel(tool_calls: list) -> list[ToolMessage]:
    """并行执行互不依赖的工具调用"""
    tasks = []
    for tc in tool_calls:
        task = asyncio.create_task(execute_single_tool(tc))
        tasks.append(task)
    return await asyncio.gather(*tasks)

# Solution 2: Streaming — 边生成边返回
async for chunk in graph.astream(state, config, stream_mode="messages"):
    if isinstance(chunk, AIMessageChunk):
        yield chunk.content  # 实时返回给用户

# Solution 3: Speculative Tool Execution
# 在 LLM 还在生成响应时，预测可能需要的工具并预先执行
async def speculative_execute(partial_response: str, tools: list) -> dict:
    if "search" in partial_response.lower():
        # 预测可能需要搜索，预先准备搜索环境
        return await prepare_search_environment()
    return {}
```

### 8.4 成本过高

**问题：** 每次 Agent 运行消耗大量 Token，成本难以控制。

**解决方案：**

```python
# Solution 1: Task-Specific Model Routing (see 7.5)

# Solution 2: Prompt Caching
# Anthropic:
CACHE_CONTROL = {"type": "ephemeral"}
# 标记 system prompt 和 tool definitions 为可缓存

# Solution 3: Context Truncation
def smart_truncate(messages: list, max_tokens: int) -> list:
    """智能截断，保留最重要的消息"""
    # 评分每条消息的重要性
    importance_scores = []
    for msg in messages:
        score = 0
        if msg["role"] == "system":
            score = 100  # System prompt 最重要
        elif msg["role"] == "user":
            score = 50
        elif "tool_calls" in str(msg):
            score = 40  # LLM 决策
        else:
            score = 30  # Tool results

        importance_scores.append({
            "msg": msg,
            "score": score,
            "tokens": count_tokens(str(msg))
        })

    # 保留最高分消息直到接近 token 限制
    # ...
```

### 8.5 多 Agent 通信失败

**问题：** 多个 Agent 之间消息传递出错，或陷入循环对话。

**解决方案：**

```python
# Solution 1: Structured Message Protocol
class AgentMessage(BaseModel):
    """标准化的 Agent 间消息格式"""
    msg_id: str
    sender: str
    recipient: str
    msg_type: Literal["request", "response", "handoff", "error", "status"]
    content: dict  # 结构化内容，而非纯文本
    references: list[str] = []  # 引用的消息 ID
    timestamp: float

# Solution 2: Clear Handoff Protocol
class HandoffProtocol:
    """标准化的 Agent 交接协议"""
    @staticmethod
    def create_handoff(from_agent: str, to_agent: str, context: str) -> str:
        return json.dumps({
            "type": "HANDOFF",
            "from": from_agent,
            "to": to_agent,
            "context_summary": context[:500],
            "unresolved_items": [],  # 待处理事项
            "decisions_made": [],    # 已做出的决策
        })

# Solution 3: Terminator Agent — 监督多 Agent 对话
class TerminatorAgent:
    """监护 Agent，检测多 Agent 对话是否达成共识或需要终止"""
    def should_terminate(self, conversation: list) -> bool:
        last_5_messages = conversation[-5:]
        # 检查是否在重复相同内容
        unique_content = set(m.content for m in last_5_messages)
        if len(unique_content) <= 2:
            return True  # 陷入循环
        # 检查是否达成一致
        if all("agree" in m.content.lower() for m in last_5_messages):
            return True
        return False
```

### 8.6 Context Window 溢出

**问题：** Agent 运行过程中对话历史和工具结果超出模型上下文窗口。

**解决方案总结表：**

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| **滑动窗口** | 保留最近 K 轮，丢弃更早的 | 对历史依赖不强的任务 |
| **智能摘要** | 将早期对话压缩为摘要 | 需要保留上下文脉络 |
| **向量检索** | 历史存在外部，按需检索 | 需要引用早前的具体信息 |
| **混合策略** | 近期对话 + 早期摘要 + 关键信息检索 | 大多数生产场景 |

---

## 9. 对比总结表

### 9.1 框架对比矩阵

```
+============+==========+==========+==========+============+==========+==============+
| Framework  | Maturity | Ease of  | Flexibi- | Production | Community| Best For      |
|            |          | Use      | lity     | Readiness  | Size     |               |
+============+==========+==========+==========+============+==========+==============+
| LangGraph  | ★★★★★    | ★★★☆☆    | ★★★★★    | ★★★★★      | ★★★★★    | 复杂生产级    |
|            |          |          |          |            |          | 工作流        |
+------------+----------+----------+----------+------------+----------+--------------+
| CrewAI     | ★★★★☆    | ★★★★★    | ★★★☆☆    | ★★★☆☆      | ★★★★☆    | 多 Agent      |
|            |          |          |          |            |          | 角色扮演       |
+------------+----------+----------+----------+------------+----------+--------------+
| AutoGen    | ★★★★☆    | ★★★☆☆    | ★★★★☆    | ★★★★☆      | ★★★★☆    | 研究/代码     |
|            |          |          |          |            |          | 生成协作       |
+------------+----------+----------+----------+------------+----------+--------------+
| OpenAI     | ★★★☆☆    | ★★★★★    | ★★★☆☆    | ★★★☆☆      | ★★★☆☆    | 快速原型/    |
| Agents SDK |          |          |          |            |          | 路由式 Agent  |
+------------+----------+----------+----------+------------+----------+--------------+
| Dify       | ★★★★☆    | ★★★★★    | ★★★☆☆    | ★★★★☆      | ★★★★★    | 可视化快速    |
|            |          |          |          |            |          | 原型         |
+------------+----------+----------+----------+------------+----------+--------------+
| Coze       | ★★★☆☆    | ★★★★★    | ★★☆☆☆    | ★★★☆☆      | ★★★★☆    | Bot 快速     |
|            |          |          |          |            |          | 发布         |
+------------+----------+----------+----------+------------+----------+--------------+
| Semantic   | ★★★★☆    | ★★★☆☆    | ★★★★☆    | ★★★★☆      | ★★★☆☆    | .NET/Azure  |
| Kernel     |          |          |          |            |          | 企业集成      |
+------------+----------+----------+----------+------------+----------+--------------+
| LlamaIndex | ★★★★☆    | ★★★★☆    | ★★★☆☆    | ★★★☆☆      | ★★★★☆    | RAG 密集型   |
| Agent      |          |          |          |            |          | Agent        |
+------------+----------+----------+----------+------------+----------+--------------+
| Smolagents | ★★★☆☆    | ★★★★☆    | ★★★☆☆    | ★★☆☆☆      | ★★★☆☆    | 研究实验     |
+------------+----------+----------+----------+------------+----------+--------------+
| PocketFlow | ★★★☆☆    | ★★★★☆    | ★★★☆☆    | ★★★☆☆      | ★★☆☆☆    | 轻量中文     |
|            |          |          |          |            |          | 场景         |
+============+==========+==========+==========+============+==========+==============+
```

### 9.2 决策指南：选择哪个框架

```
+===================================================================+
|                    FRAMEWORK DECISION GUIDE                         |
+===================================================================+
|                                                                   |
|  Q1: 是否需要严格的生产级可靠性？                                   |
|   ├── Yes -> Q2                                                    |
|   └── No  -> Q3                                                    |
|                                                                   |
|  Q2: 工作流是否有复杂的条件分支和循环？                              |
|   ├── Yes -> LangGraph                                             |
|   └── No  -> 是否需要多 Agent 协作？                                |
|           ├── Yes -> AutoGen (研究) / CrewAI (内容创作)             |
|           └── No  -> LangChain Agent / LlamaIndex Agent            |
|                                                                   |
|  Q3: 团队是否有专业程序员？                                         |
|   ├── Yes -> 是否需要深度定制？                                     |
|   │         ├── Yes -> LangGraph / AutoGen                         |
|   │         └── No  -> CrewAI / OpenAI Agents SDK                  |
|   └── No  -> 可视化平台？                                           |
|             ├── Yes -> Dify / Coze / FastGPT                        |
|             └── No  -> CrewAI (API 最简洁)                          |
|                                                                   |
|  Q4: 技术栈偏好？                                                   |
|   ├── Python 为主 -> LangGraph / CrewAI / AutoGen                  |
|   ├── .NET 企业 -> Semantic Kernel                                 |
|   ├── TypeScript -> Bee Agent Framework / Vercel AI SDK            |
|   └── OpenAI 深度用户 -> OpenAI Agents SDK                         |
|                                                                   |
|  Q5: 特定场景？                                                     |
|   ├── 需要强 RAG -> LlamaIndex Agent                               |
|   ├── 需要代码执行 -> AutoGen (Docker 沙箱) / e2b                  |
|   ├── 需要 Human-in-the-loop -> LangGraph (Checkpoints)            |
|   ├── 快速发布 Bot -> Coze / Dify                                  |
|   └── 研究实验 -> Smolagents / AutoGen                             |
|                                                                   |
+===================================================================+
```

**按场景推荐速查：**

| 场景 | 首选框架 | 备选框架 |
|------|----------|----------|
| 企业级复杂 Agent 工作流 | LangGraph | AutoGen |
| 快速原型验证 | CrewAI / Dify | OpenAI Agents SDK |
| 研究实验 | AutoGen / Smolagents | LangGraph |
| 多 Agent 内容创作 | CrewAI | AutoGen (GroupChat) |
| 代码生成与执行 | AutoGen | LangGraph + Docker |
| RAG 问答 Agent | LlamaIndex Agent | LangGraph |
| 非程序员构建 Bot | Dify / Coze | FastGPT |
| .NET 企业集成 | Semantic Kernel | LangGraph (Python) |
| 移动端/轻量部署 | PocketFlow | OpenAI Agents SDK |
| 全栈 TypeScript 项目 | Bee Agent (IBM) | Vercel AI SDK |

---

## 附录 A: 术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| Agent | AI Agent | 由 LLM 驱动的自主任务执行程序 |
| Tool Calling | Function Calling | LLM 选择和调用外部函数/API 的能力 |
| ReAct | Reasoning + Acting | 交替推理和行动的 Agent 模式 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| HITL | Human-in-the-Loop | 人类介入审批或决策的环节 |
| Checkpoint | Checkpoint | 状态快照，用于持久化和恢复 |
| Handoff | Handoff | Agent 之间移交对话控制权 |
| Guardrail | Guardrail | 输入/输出的安全检查机制 |
| Token | Token | LLM 处理文本的最小单位 |
| MCP | Model Context Protocol | Anthropic 提出的模型上下文协议 |
| TAM | Total Addressable Market | 可寻址市场总量 |

## 附录 B: 参考资源

**官方文档：**
- LangGraph: https://langchain-ai.github.io/langgraph/
- CrewAI: https://docs.crewai.com/
- AutoGen: https://microsoft.github.io/autogen/
- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents
- Dify: https://docs.dify.ai/
- Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/

**论文与文章：**
- ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)
- Tree of Thoughts: Deliberate Problem Solving with Large Language Models (Yao et al., 2023)
- Plan-and-Solve Prompting (Wang et al., 2023)
- AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (Wu et al., 2023)

---

> 本文档持续更新中。Agent 技术发展日新月异，建议定期关注各框架的 Release Notes 和社区动态。
> 最后更新：2026年8月
