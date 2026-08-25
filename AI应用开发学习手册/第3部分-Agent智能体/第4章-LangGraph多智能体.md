# 第 4 章 Multi-Agent 之 LangGraph

## 学习目标

- 理解 LangGraph 的定位与图计算模型
- 掌握 State / Nodes / Edges 三大核心抽象
- 掌握条件分支、循环、持久化、子图等高级特性
- 独立构建一个多 Agent 协作系统

---

## 4.1 LangGraph 基础概念

### 4.1.1 什么是 LangGraph

LangGraph 是 LangChain 推出的**基于图结构编排 Agent 工作流**的框架。核心洞察：Agent 的复杂流程（循环、分支、并行、人机协作）本质是**有向图**，而传统 Chain/AgentExecutor 难以表达循环与条件跳转。

### 4.1.2 与 AgentExecutor 的对比

| 维度 | AgentExecutor（ReAct） | LangGraph |
|------|------------------------|-----------|
| 流程表达 | 固定循环 | 任意图（循环/分支/并行） |
| 状态管理 | 隐式 | 显式 State 对象 |
| 持久化 | 无 | 内置 Checkpointer |
| 人机交互 | 困难 | `interrupt()` 原生支持 |
| 多 Agent | 需自己拼 | Supervisor / 子图原生支持 |

> 结论：LangGraph 是 AgentExecutor 的**超集**，官方已将其作为 Agent 开发首选。

## 4.2 LangGraph 三大核心组件

### 4.2.1 State（状态）

State 是图中**共享的数据结构**，每个节点读写 State，节点间通过 State 传递信息。

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # 消息累积器（追加合并）
    question: str
    context: list[str]
    final_answer: str
```

`Annotated[T, reducer]` 中的 reducer 定义如何合并旧值与新值——`add_messages` 表示追加，普通字段表示覆盖。

### 4.2.2 Nodes（节点）

节点是**接收 State 返回新 State 的函数**（或 Runnable）：

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini")

def retrieve_node(state: AgentState) -> dict:
    """检索节点：从向量库取上下文"""
    docs = retriever.invoke(state["question"])
    return {"context": [d.page_content for d in docs]}

def generate_node(state: AgentState) -> dict:
    """生成节点：LLM 基于上下文回答"""
    prompt = f"基于资料回答：{state['context']}\n问题：{state['question']}"
    resp = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [resp], "final_answer": resp.content}
```

### 4.2.3 Edges（边）

边定义节点间的连接关系：

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AgentState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()
result = app.invoke({"question": "年假政策", "messages": []})
```

## 4.3 条件分支与循环

### 4.3.1 条件边（Conditional Edges）

根据状态决定下一步走向——这是实现"Agent 自主决策"的关键：

```python
def route(state: AgentState) -> str:
    """根据是否有工具调用决定继续执行还是结束"""
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
        return "tools"        # 有工具调用 → 执行工具
    return "generate"         # 否则 → 生成最终答案

graph.add_conditional_edges("agent", route,
    {"tools": "tools", "generate": "generate"})
```

### 4.3.2 循环（Loop）

LangGraph 天然支持环状图：`agent → tools → agent → ...` 直到终止条件满足（结合 `recursion_limit` 防止死循环）。

## 4.4 高级特性

### 4.4.1 Checkpointer（持久化）

LangGraph 内置持久化——把每次"状态快照"存入数据库，支持**断点续跑、多轮记忆、时间旅行**：

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# 通过 thread_id 维护独立会话
config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"question": "我的名字是小明"}, config)
app.invoke({"question": "我叫什么？"}, config)   # 记得历史！
```

生产环境用 `SqliteSaver` / `PostgresSaver` 持久化到数据库。

### 4.4.2 Human-in-the-loop（人机协作）

用 `interrupt()` 暂停流程等待人工确认，适合审批、敏感操作：

```python
from langgraph.types import interrupt

def approval_node(state):
    user_ok = interrupt({"action": state["proposed_action"]})
    if not user_ok:
        return {"status": "rejected"}
    return {"status": "approved"}

# 执行到 interrupt 时暂停，应用层展示给用户确认
# 通过 Command(resume=True/False) 恢复
```

### 4.4.3 子图（Subgraphs）

把复杂流程拆成可复用的子图，主图调用子图：

```python
sub_graph = StateGraph(SubState).add_node(...).compile()   # 子图
main_graph.add_node("research", sub_graph)                 # 作为主图节点
```

### 4.4.4 并行执行

用 `Send` API 对列表元素并行发起多个节点执行（如"对 10 份文档并行分析"）。

## 4.5 多 Agent 实战：Supervisor 架构

构建"主管 Agent + 三个专家 Agent"（调研/写作/审查）：

```python
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# ── 1. 专家 Agent（每个封装为工具）──
@tool
def researcher_tool(question: str) -> str:
    """调研助手：检索资料回答问题"""
    agent = create_react_agent(llm, [search_tool])
    return agent.invoke({"messages": [("human", question)]})["messages"][-1].content

@tool
def writer_tool(topic: str) -> str:
    """写作助手：根据主题撰写初稿"""
    return llm.invoke(f"围绕{topic}写一篇500字初稿").content

@tool
def reviewer_tool(draft: str) -> str:
    """审查助手：检查逻辑与事实"""
    return llm.invoke(f"审查以下文稿并给出修改意见：{draft}").content

# ── 2. 主管 Agent（调度者）──
supervisor = create_react_agent(
    llm, tools=[researcher_tool, writer_tool, reviewer_tool],
    prompt="你是项目主管，负责任务拆解与调度，最终汇总输出。")

result = supervisor.invoke({
    "messages": [("human", "写一篇关于RAG技术趋势的报告")]})
print(result["messages"][-1].content)
```

### 4.5.1 多 Agent 设计最佳实践

1. **每个 Agent 一个工具**：把子 Agent 封装成工具，由主管统一调度，通信简单可控。
2. **定义 Agent 边界**：系统提示词明确"你负责什么、不负责什么、何时完成任务"。
3. **共享状态收敛**：子 Agent 结果统一写入 State 的固定字段，避免消息爆炸。
4. **设置 recursion_limit**：如 `app.invoke(..., {"recursion_limit": 50})`。
5. **先单测子图**：每个子 Agent 单独测试通过后，再组装主图。

---

## 高质量博客推荐

1. **LangGraph 多智能体实战：从入门到生产** — [CSDN](https://blog.csdn.net/weixin_41200786/article/details/143581587)
   含 State/Node/Edge 讲解与完整多 Agent 案例。
2. **LangGraph 官方文档（中文精读版）** — [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
   权威参考，推荐精读 concepts 与 tutorials。
3. **LangGraph 与 AgentExecutor 对比：为什么迁移** — [掘金](https://juejin.cn/post/7429099443533815819)
   架构演进视角的分析，帮助理解设计动机。
4. **LangGraph 实战：Human-in-the-loop 审批流** — [微信公众号](https://mp.weixin.qq.com/s/5dKk4F2fT9qGm3hQJ7y3SA)
   企业级人机协作 Agent 的实现详解。
5. **LangGraph 多智能体最佳实践（官方博客中文解读）** — [阿里云开发者社区](https://developer.aliyun.com/article/1631042)
   Supervisor、Swarm、Hierarchical 模式的官方推荐做法。

## 动手实践

1. 用 LangGraph 实现"检索 → 判断是否需要更多信息 → 生成"的条件流程。
2. 给图添加 MemorySaver，实现跨轮记忆的对话 Agent。
3. 实现一个"写报告"Supervisor：调研 Agent + 写作 Agent + 审查 Agent。
4. 用 interrupt() 实现"AI 起草 → 人工审批 → 继续执行"的审批流程。

## 常见问题（FAQ）

**Q1：LangGraph 的学习曲线陡峭吗？**
A：有一定门槛（图思维、State 合并、reducer）。建议按"单节点图 → 条件分支 → 循环 → 子图 → 多 Agent"顺序循序渐进。

**Q2：什么时候用 LangGraph 而不是 LangChain Chain？**
A：流程固定无循环用 Chain/LCEL 更简单；有循环、分支、多 Agent 协作、需要持久化时用 LangGraph。

**Q3：State 中消息太多导致上下文超限？**
A：用 reducer 对消息做滑动窗口裁剪或摘要压缩（如只保留最近 10 条 + 历史摘要），结合 Checkpointer 持久化完整历史。
