# 第 3 章 LangChain 最新应用解析

## 学习目标

- 理解 LangChain 核心组件（Models / Prompts / Chains / Memory / Agent / Tools）
- 掌握 LCEL 表达式语言与可组合管道
- 掌握 Memory 记忆机制的多种实现
- 理解 Agent 与工具调用机制
- 了解 LangChain v1.0 的新架构变化
- 完成 LangChain RAG 应用实战

---

## 3.1 LangChain 核心组件

LangChain 是构建大模型应用的**最流行编排框架**，核心抽象：

```
        ┌────────────────────────────────────────────┐
        │            LangChain 应用架构               │
        │                                            │
        │  Model（LLM/ChatModel）                     │
        │  Prompt（提示模板）  ↔  Memory（记忆）        │
        │  Chain / LCEL 管道（编排逻辑）                │
        │  Agent（智能体） ↔ Tool（工具）↔ Retriever    │
        └────────────────────────────────────────────┘
```

| 组件 | 职责 | 核心类 |
|------|------|--------|
| Models | 封装各类模型（LLM/Chat/Embedding） | `ChatOpenAI`、`ChatOllama` |
| Prompts | 模板化提示词、消息组装 | `ChatPromptTemplate`、`FewShotPromptTemplate` |
| Output Parsers | 结构化输出解析 | `StrOutputParser`、`PydanticOutputParser` |
| Memory | 多轮对话记忆 | `ConversationBufferMemory`、`ConversationSummaryMemory` |
| Chains | 串联多步逻辑 | `create_retrieval_chain`、`create_history_aware_retriever` |
| Tools | 工具定义与调用 | `@tool` 装饰器、`TavilySearchResults` |
| Agent | 自主决策执行 | `create_tool_calling_agent`、`AgentExecutor` |
| Retriever | 检索器（RAG 核心） | `VectorStoreRetriever`、`EnsembleRetriever` |

## 3.2 数据连接（Document Loaders 与 VectorStore）

- **Document Loaders**：`PyPDFLoader`、`TextLoader`、`WebBaseLoader`、`UnstructuredLoader` 等，将数据转为 Document 对象。
- **Text Splitters**：`RecursiveCharacterTextSplitter`（最常用，按分隔符递归切分）、`MarkdownHeaderTextSplitter`、`SemanticChunker`。
- **VectorStore 集成**：`Chroma`、`FAISS`、`Milvus`、`Pinecone`、`ElasticsearchStore` 等统一接口。

## 3.3 LCEL 表达式语言

**LCEL（LangChain Expression Language）** 是 LangChain 的核心语法，用 `|` 管道符声明式组合组件，天然支持流式输出、异步、重试与可观测性。

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("用一句话解释：{topic}")
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model | StrOutputParser()   # 声明式管道

print(chain.invoke({"topic": "什么是 RAG"}))
```

**LCEL 内置能力**：`.stream()` 流式输出、`.batch()` 批量处理、`.ainvoke()` 异步、`.with_retry()` 重试、`.with_fallbacks()` 回退。

## 3.4 Memory（记忆）

多轮对话需要记忆历史，LangChain 提供多种记忆策略：

| 记忆类型 | 原理 | 适用场景 |
|----------|------|----------|
| ConversationBufferMemory | 全量保留历史消息 | 短对话 |
| ConversationBufferWindowMemory | 只保留最近 K 轮 | 控制 token 成本 |
| ConversationSummaryMemory | LLM 定期压缩摘要 | 长对话 |
| ConversationSummaryBufferMemory | 窗口 + 超出部分摘要 | 长对话兼顾细节 |
| VectorStoreRetrieverMemory | 语义相似历史召回 | 个性化助手 |

**最新实践**：LangChain v1.0 推荐直接使用 `messages` 列表 + `ChatMessageHistory` 自行管理，或配合 Redis/SQLite 做持久化。

```python
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()          # 内存版
history.add_user_message("我叫小明")
history.add_ai_message("你好小明！")

# 持久化可配合 Redis: RedisChatMessageHistory(session_id=..., url=...)
```

## 3.5 Agent 与工具调用

### 3.5.1 工具定义

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气，参数 city 为城市名。"""
    return f"{city}今天晴，26°C"

@tool
def calc(expr: str) -> str:
    """安全计算数学表达式。"""
    return str(eval(expr, {"__builtins__": {}}, {}))
```

### 3.5.2 构建 Tool Calling Agent

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

tools = [get_weather, calc]
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的助手，可使用提供的工具完成任务。"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(model, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke({"input": "北京天气如何？顺便算一下 25*4+8"})
```

**工作流程**：LLM 判断需要调用工具 → 返回结构化函数调用参数 → 执行工具 → 结果回填 LLM → 生成最终答案。

## 3.6 LangChain v1.0 新趋势

- **langchain 与 langchain-community 拆分**：核心包更轻，集成按需安装。
- **langchain-core 稳定化**：接口统一，LCEL 成为一等公民。
- **Agent 优先**：官方重心从 Chain 转向 Agent，提供 `create_agent` API。
- **可观测性**：LangSmith 深度集成，支持 tracing、evaluation、monitoring。
- **结构化输出**：原生支持 Pydantic 约束输出，可靠性显著提升。

## 3.7 LangChain RAG 应用实战

### 3.7.1 标准 RAG 链（含历史对话）

```python
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# 1. 加载与切分
loader = PyPDFLoader("./企业制度.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.split_documents(docs)

# 2. 向量化入库
vectorstore = Chroma.from_documents(splits, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 3. 历史感知检索（将历史转化为更好的检索 query）
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "根据聊天历史，将最新问题改写为可独立检索的问题。"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt)

# 4. 组装问答链
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "基于以下资料回答，资料不足请说明：\n\n{context}"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
])
qa_chain = create_stuff_documents_chain(model, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

# 5. 使用
result = rag_chain.invoke({
    "input": "年假怎么算？",
    "chat_history": [("human", "我在公司工作三年了"), ("ai", "好的，已了解")],
})
print(result["answer"])
```

### 3.7.2 工程要点

- **Embedding 一致性**：建库与查询必须同模型。
- **检索后处理**：`search_kwargs` 调 K 值；可加 MMR（`fetch_k` + `mmr`）增加多样性。
- **来源追踪**：在 QA 提示中让模型输出引用，或从 `result["context"]` 取元数据。
- **性能**：长上下文可用 `MapReduceDocumentsChain` 分块摘要，避免超窗口。

---

## 高质量博客推荐

1. **LangChain v1.0 完全指南：从入门到生产** — [PyLLM](https://pyllm.cc/langchain-tutorial/)
   中文权威教程，覆盖 LCEL、Agent、RAG 全流程，推荐系统学习。
2. **LangChain 入门到精通系列（官方中文笔记）** — [CSDN](https://blog.csdn.net/weixin_45081575/article/details/134815709)
   十余篇系列笔记，组件粒度讲解清晰。
3. **LangChain Agent 实战：ReAct、Tool Calling 与多工具协作** — [掘金](https://juejin.cn/post/7392002792492564537)
   Agent 机制深度拆解，含工具调用时序图。
4. **LCEL 表达式语言官方文档（中文对照）** — [LangChain 官方](https://python.langchain.com/docs/concepts/lcel/)
   掌握 `|` 管道的全部能力，建议精读官方。
5. **LangChain 与 LlamaIndex 选型对比实践** — [51CTO博客](https://blog.51cto.com/u_15863253/9010074)
   生产环境架构选型参考。

## 动手实践

1. 用 LCEL 构建一个"翻译 + 润色"管道，体验流式输出。
2. 实现带 ConversationBufferWindowMemory 的多轮客服机器人。
3. 定义 3 个自定义工具（天气/计算器/数据库查询），构建 Tool Calling Agent。
4. 用 PyPDFLoader + RecursiveCharacterTextSplitter 完成企业 PDF 问答。

## 常见问题（FAQ）

**Q1：LCEL 和传统 Chain 类有什么不同？**
A：LCEL 是声明式组合语法，自动获得流式、异步、批处理、重试等能力，且类型安全、可序列化，官方推荐全面使用 LCEL。

**Q2：Agent 和 Chain 的区别？**
A：Chain 是固定执行路径；Agent 由 LLM 动态决定执行路径（选工具、定步骤）。任务流程固定用 Chain，需要自主决策用 Agent。

**Q3：多轮对话中 RAG 检索不准怎么办？**
A：使用 `create_history_aware_retriever`，先让 LLM 结合历史把问题改写成独立检索 query，再检索，效果显著提升。
