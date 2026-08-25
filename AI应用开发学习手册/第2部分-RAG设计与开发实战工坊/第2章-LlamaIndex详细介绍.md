# 第 2 章 LlamaIndex 详细介绍

## 学习目标

- 理解 LlamaIndex 的定位与设计哲学
- 掌握五大核心组件：Loading / Indexing / Storing / Querying / Workflow
- 掌握 Reader 加载器体系与 Node 解析
- 使用 LlamaIndex 快速构建企业 RAG 知识库

---

## 2.1 LlamaIndex 基础概念

### 2.1.1 什么是 LlamaIndex

LlamaIndex（原名 GPT Index）是**专为 RAG 场景设计的开源数据框架**，核心使命：**连接大模型与私有数据**。相比 LangChain 的"通用编排"，LlamaIndex 更专注数据索引与检索的深度优化。

### 2.1.2 与 LangChain 的定位差异

| 维度 | LlamaIndex | LangChain |
|------|------------|-----------|
| 定位 | 数据框架，RAG 深度优化 | 通用应用编排框架 |
| 核心抽象 | Document / Node / Index | Chain / Agent / Tool |
| 检索能力 | 检索策略丰富（树/图/向量混合） | 依赖集成组件 |
| 特色功能 | Knowledge Graph、SQL+向量统一检索 | 生态最广、Agent 链强大 |
| 适用 | RAG 重、检索复杂场景 | 综合应用、Agent 编排 |

> 学习建议：两者不互斥。生产实践常见 **LlamaIndex 做索引检索 + LangChain 做流程编排**。

## 2.2 LlamaIndex 五大核心组件

```
                    ┌─────────────┐
   原始数据 ───────▶ │  Loading    │ ──> Document/Node
                    └─────────────┘
                    ┌─────────────┐
   Document ───────▶ │  Indexing   │ ──> 各种 Index
                    └─────────────┘
                    ┌─────────────┐
   Index ──────────▶ │  Storing    │ ──> 持久化存储
                    └─────────────┘
                    ┌─────────────┐
   问题 ───────────▶ │  Querying   │ ──> 检索 + 合成
                    └─────────────┘
                    ┌─────────────┐
   复杂任务 ───────▶ │  Workflow   │ ──> 事件驱动编排
                    └─────────────┘
```

### 2.2.1 Loading（加载）

- **Document**：数据的最原始载体（一个文件 = 一个 Document）。
- **Reader**：将各种格式转为 Document，如 PDFReader、DocxReader、SimpleDirectoryReader、LlamaParse（复杂格式解析神器）。

```python
from llama_index.core import SimpleDirectoryReader
docs = SimpleDirectoryReader("./data", recursive=True).load_data()
```

### 2.2.2 Indexing（索引）

- **Node（节点）**：Document 被切分为的检索最小单元，包含文本 + 元数据（来源、页码）。
- **Index 类型**：

| Index 类型 | 原理 | 适用场景 |
|------------|------|----------|
| VectorStoreIndex | 向量化 + ANN 检索 | 语义检索（最常用） |
| SummaryIndex | 顺序遍历 + 摘要 | 小文档全量问答 |
| TreeIndex | 树状摘要聚合 | 长文档层次理解 |
| KnowledgeGraphIndex | 抽取实体关系构建图 | 关系密集型数据 |
| SQLIndex | 文本到 SQL | 结构化数据库问答 |

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex

parser = SentenceSplitter(chunk_size=512, chunk_overlap=64)
nodes = parser.get_nodes_from_documents(docs)
index = VectorStoreIndex(nodes)
```

### 2.2.3 Storing（存储）

- **StorageContext**：统一管理向量存储 + 文档存储 + 索引存储。
- 支持 Chroma、Milvus、Qdrant、Postgres 等；默认内存存储，可持久化。

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

chroma_client = chromadb.PersistentClient(path="./chroma")
col = chroma_client.get_or_create_collection("kb")
store = ChromaVectorStore(chroma_collection=col)
storage_context = StorageContext.from_defaults(vector_store=store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

### 2.2.4 Querying（查询）

- **Retriever（检索器）**：VectorIndexRetriever、BM25Retriever、混合检索（QueryFusionRetriever）、知识图谱检索器。
- **Query Engine（查询引擎）**：封装"检索 + 提示 + 合成"，常用 `index.as_query_engine()`。
- **Chat Engine（对话引擎）**：带多轮记忆的对话式问答。
- **Node Postprocessor（后处理器）**：重排序、相似度阈值过滤、去重。

```python
query_engine = index.as_query_engine(
    similarity_top_k=5,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)
resp = query_engine.query("退货政策是什么？")
print(resp.response, resp.source_nodes)  # 答案 + 来源
```

### 2.2.5 Workflow（工作流）

LlamaIndex Workflow 是**事件驱动**的轻量编排框架，适合构建复杂 RAG/Agent 管道：

```python
from llama_index.core.workflow import (
    Workflow, StartEvent, StopEvent, step
)

class RAGWorkflow(Workflow):
    @step
    async def retrieve(self, ev: StartEvent):
        nodes = retriever.retrieve(ev.question)
        return RetrievedEvent(nodes=nodes, question=ev.question)

    @step
    async def synthesize(self, ev: RetrievedEvent):
        answer = llm.complete(build_prompt(ev.question, ev.nodes))
        return StopEvent(result=answer)
```

## 2.3 LlamaIndex 加载器体系（Readers）

LlamaIndex 生态提供 **LlamaHub**（数百个现成 Reader），覆盖：

| 类别 | 示例 |
|------|------|
| 办公文档 | PDF、Docx、PPTX、Excel |
| 网页数据 | 网页抓取、RSS、Notion、Confluence |
| 数据库 | PostgreSQL、MySQL、SQLite、DuckDB |
| 云服务 | Google Drive、S3、阿里云 OSS |
| 专用格式 | Markdown、HTML、JSON、CSV、LaTeX |

**LlamaParse**：LlamaIndex 出品的 AI 文档解析服务，对复杂 PDF（表格、多栏）解析效果远超传统解析器，是生产 RAG 的"增强外挂"。

## 2.4 LlamaIndex 实战：快速构建企业 RAG 知识库

### 2.4.1 完整项目骨架

```bash
pip install llama-index-core llama-index-readers-file llama-index-llms-openai chromadb
```

```python
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. 全局配置（模型统一）
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 2. 加载 + 切分
docs = SimpleDirectoryReader("./docs").load_data()
parser = SentenceSplitter(chunk_size=512, chunk_overlap=64)
nodes = parser.get_nodes_from_documents(docs)

# 3. 建索引并持久化
index = VectorStoreIndex(nodes)
index.storage_context.persist("./storage")   # 保存到磁盘

# 4. 查询
query_engine = index.as_query_engine(similarity_top_k=5)
resp = query_engine.query("我们的退款政策是什么？")
print(resp.response)
for node in resp.source_nodes:
    print("来源:", node.metadata)
```

### 2.4.2 生产化要点

1. **元数据管理**：每个 Node 带上 `file_name`、`page_number`、`department` 等，实现检索过滤与溯源。
2. **向量存储换生产库**：上线时从内存换到 Milvus/Qdrant，并配置 HNSW 索引。
3. **多级检索**：先标量过滤（部门/年份）再向量检索，减少噪声。
4. **评估先行**：用第 5 章的评估体系验证效果再上线。

---

## 高质量博客推荐

1. **LlamaIndex 入门教程：从零构建 RAG 应用** — [PyLLM](https://pyllm.cc/llamaindex-tutorial/)
   中文入门精品，覆盖环境搭建到 Query Engine 全流程。
2. **LlamaIndex 入门笔记：核心概念与实战** — [CSDN](https://blog.csdn.net/qq_42837985/article/details/143013474)
   结合实例讲解 Document、Node、Index 等核心抽象。
3. **LlamaIndex 与 LangChain 深度集成实践** — [51CTO博客](https://blog.51cto.com/u_15863253/9010074)
   对比两大框架并给出协同架构方案。
4. **LlamaIndex Workflow 工作流官方指南（中文解读）** — [掘金](https://juejin.cn/post/7397247419467276355)
   事件驱动工作流的原理与 Agent 应用示例。
5. **LlamaHub 使用指南：上百种数据源一次接入** — [LlamaIndex 官方文档](https://docs.llamaindex.ai/stable/understanding/loading/llamahub/)

## 动手实践

1. 用 SimpleDirectoryReader 加载 10 篇混合格式文档（PDF/Word/网页），完成问答。
2. 对比 VectorStoreIndex 与 TreeIndex 在长文档问答上的效果差异。
3. 给 Node 添加元数据，实现"按部门过滤 + 向量检索"的组合查询。
4. 用 LlamaParse 解析一个复杂表格 PDF，对比与普通解析的效果。

## 常见问题（FAQ）

**Q1：LlamaIndex 和 LangChain 到底选哪个？**
A：检索与知识库为主选 LlamaIndex；Agent 编排与多工具链为主选 LangChain；大型项目两者结合。

**Q2：为什么我的 LlamaIndex 查询很慢？**
A：检查三处——Embedding 模型是否本地 CPU 推理（建议换 API 或 GPU）；是否每次启动重新建索引（应持久化/复用）；K 值是否过大。

**Q3：Node 切多大最合适？**
A：中文建议 256-512 字符，重叠 10-20%。同时结合文档结构（标题、段落）做智能切分更佳。
