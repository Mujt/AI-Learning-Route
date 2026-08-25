# 第 1 章 RAG 认知与基础项目实战

## 学习目标

- 理解 RAG 的核心思想与为什么需要 RAG
- 掌握 Naive RAG 的完整 Pipeline（索引→检索→生成）
- 理解向量化、向量数据库、相似度检索原理
- 独立完成一个基于开源模型的 RAG 问答项目

---

## 1.1 RAG 基础理论

### 1.1.1 为什么需要 RAG

大模型存在三大天然缺陷：

1. **知识滞后**：训练数据有截止日期，无法获取最新信息。
2. **幻觉**：对未知问题"一本正经地胡说八道"。
3. **数据安全**：企业私有知识无法（也不应）进入模型参数。

**RAG（Retrieval-Augmented Generation，检索增强生成）** 的解法：**先检索、再回答**——将外部知识库检索到的相关内容作为上下文注入 Prompt，让模型基于给定资料作答。

### 1.1.2 RAG 的三大优势

- **知识实时更新**：只改知识库，无需重新训练模型。
- **降低幻觉**：模型回答有依据，可溯源。
- **保护私有数据**：知识留在企业本地，模型只"读取"。

### 1.1.3 RAG 与微调的选型对比

| 维度 | RAG | 微调（Fine-tuning） |
|------|-----|---------------------|
| 知识更新 | 秒级（换库即可） | 需重新训练 |
| 幻觉控制 | 强（基于检索） | 弱（仍可能编造） |
| 成本 | 低 | 高 |
| 改变模型风格/格式 | 弱 | 强 |
| 适用场景 | 知识问答、事实查询 | 领域语言、输出格式定制 |

> 业界共识：**先 RAG，再微调**。RAG 解决"知识"问题，微调解决"风格与能力"问题，二者可结合。

## 1.2 Naive RAG Pipeline（基础版）

基础版 RAG（Naive RAG）包含三个核心阶段：

```
【索引阶段】文档 → 切分 → 向量化 → 存入向量库
【检索阶段】用户问题 → 向量化 → 相似度检索 Top-K
【生成阶段】问题 + 检索片段 → 组装 Prompt → LLM 生成答案
```

### 1.2.1 索引阶段（Indexing）

| 步骤 | 说明 | 关键选择 |
|------|------|----------|
| 文档加载 | 读取 PDF/Word/网页等 | Unstructured、PyMuPDF、Docx |
| 文本切分 | 按 chunk_size + overlap 切块 | 500-1000 字符/块，重叠 50-100 字符 |
| 向量化 | 文本 → 语义向量 | Embedding 模型（如 bge-large-zh） |
| 入库 | 向量 + 原文 + 元数据存入向量库 | Chroma / FAISS / Milvus |

**切分是 RAG 精度的第一杀手**：切得太碎丢语义，切得太大检索噪声多。进阶方案包括语义切分、结构化切分（Markdown/表格感知切分）。

### 1.2.2 检索阶段（Retrieval）

- 用户问题经**同一 Embedding 模型**向量化。
- 在向量库中计算**余弦相似度**（或内积），返回 Top-K 最相似片段。
- K 值一般取 3-8，过大引入噪声，过小覆盖不足。

### 1.2.3 生成阶段（Generation）

检索片段 + 用户问题组装成 Prompt（参考第一部分第 3 章 RAG 提示词模板），交给 LLM 生成答案。

## 1.3 核心组件详解

### 1.3.1 Embedding（嵌入）模型

- 作用：将文本映射为语义向量，语义相近的文本向量距离更近。
- 中文推荐：`BAAI/bge-large-zh-v1.5`、`m3e-base`、`text-embedding-v2`（API）。
- 关键指标：MTEB 榜单分数、维度（1024/1536/3072）、最长输入长度（512 字符常见）。
- 注意：**索引与查询必须使用同一个 Embedding 模型**，否则检索失效。

### 1.3.2 向量数据库

| 向量库 | 特点 | 适用场景 |
|--------|------|----------|
| Chroma | 轻量、Python 内嵌、零运维 | 学习原型、小规模 |
| FAISS | Meta 开源库、高性能 ANN 检索 | 中等规模、服务内嵌 |
| Milvus / Zilliz | 分布式、支持过滤与标量结合 | 生产级大规模 |
| Qdrant | Rust 实现、高性能、云原生 | 生产级 |
| pgvector | PostgreSQL 扩展，与业务库统一 | 已有 PG 体系 |
| Elasticsearch | 传统全文检索 + 向量混合 | 混合检索场景 |

### 1.3.3 相似度检索

- 余弦相似度：`cos(A,B) = A·B / (|A||B|)`，范围 [-1,1]，最常用。
- 内积（IP）：用于归一化向量，速度更快。
- 欧氏距离（L2）：越小越相似。
- ANN（近似最近邻）算法：HNSW、IVF，牺牲少量精度换取大规模检索速度。

## 1.4 基础 RAG 项目实战（Chroma + 开源模型）

### 1.4.1 环境准备

```bash
pip install chromadb sentence-transformers transformers streamlit
```

### 1.4.2 索引阶段代码示例

```python
import chromadb
from sentence_transformers import SentenceTransformer

# 1. 加载中文 embedding 模型
embed_model = SentenceTransformer("BAAI/bge-large-zh-v1.5")

# 2. 创建/连接向量库
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="company_kb", metadata={"hnsw:space": "cosine"}
)

# 3. 文档切分与入库
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks

documents = [
    {"id": "doc1", "text": "我们的产品支持7天无理由退货...", "source": "售后政策.txt"},
    # ... 更多文档
]
ids, docs, metas = [], [], []
for doc in documents:
    for i, chunk in enumerate(split_text(doc["text"])):
        ids.append(f"{doc['id']}_{i}")
        docs.append(chunk)
        metas.append({"source": doc["source"]})

collection.add(ids=ids, embeddings=embed_model.encode(docs).tolist(),
               documents=docs, metadatas=metas)
```

### 1.4.3 检索 + 生成代码示例

```python
from openai import OpenAI  # 以 OpenAI 兼容接口为例，可换 DeepSeek/通义

client = OpenAI(base_url="...", api_key="...")

def rag_query(question, top_k=4):
    # 1. 检索
    results = collection.query(
        query_embeddings=embed_model.encode([question]).tolist(),
        n_results=top_k, include=["documents", "metadatas"]
    )
    contexts = results["documents"][0]

    # 2. 组装 Prompt
    prompt = f"""你是企业知识库问答助手，请严格基于以下资料回答：
{chr(10).join(f"[{i+1}] {c}" for i, c in enumerate(contexts))}

问题：{question}
要求：只使用上述资料回答；资料不足时明确说明；不超过150字。"""
    # 3. 生成
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content

print(rag_query("退货政策是什么？"))
```

### 1.4.4 工程化改进清单

| 问题 | 症状 | 改进方案 |
|------|------|----------|
| 切分不当 | 答非所问、语义断裂 | 换语义切分/结构化切分，调 chunk_size |
| 检索不准 | 检索到无关内容 | 换更好 Embedding、调 K、加重排序 |
| 幻觉残留 | 答案有编造 | 强化"仅基于资料"约束、要求引用来源 |
| 多文档混淆 | 张冠李戴 | 检索时携带元数据过滤、答案标注来源 |

---

## 高质量博客推荐

1. **RAG 检索增强生成技术详解** — [腾讯云开发者社区](https://cloud.tencent.com/developer/article/2471106)
   从朴素 RAG 到高级 RAG 的完整演进路径，配图清晰。
2. **RAG 检索增强生成全解析：从原理到实战** — [百度智能云开发者社区](https://developer.baidu.com/article/details/3363553)
   覆盖 RAG 流程、向量化、向量数据库选型与代码示例。
3. **向量数据库与 RAG 实践** — [CSDN](https://blog.csdn.net/m0_60383600/article/details/139933277)
   深入讲解向量检索原理与 Chroma/FAISS/Milvus 用法对比。
4. **Naive RAG 到 Advanced RAG 演进路线** — [微信公众号](https://mp.weixin.qq.com/s?__biz=MzU1NjEwMTY0Mw==&mid=2247604157&idx=1&sn=9149c2ef7305465e86d577f2062499c3)
   一文看懂 RAG 的三个版本演进（Naive / Advanced / Modular）。

## 动手实践

1. 准备 5-10 篇你的领域文档（如产品说明、规章制度），搭建完整 RAG 问答。
2. 对比不同 chunk_size（200/500/1000）对回答质量的影响。
3. 换用 bge、m3e 两种 Embedding 模型，对比检索结果的语义相关性。
4. 在检索结果中加入来源标注，验证回答的"可追溯性"。

## 常见问题（FAQ）

**Q1：RAG 检索不到相关内容怎么办？**
A：优先检查三件事——①切分是否破坏语义；②Embedding 模型是否一致且合适；③K 值是否过小。再考虑重排序与混合检索。

**Q2：向量数据库和关系数据库能一起用吗？**
A：可以，这是常见生产架构。用 MySQL/PG 存业务数据与元数据，用向量库存向量，通过 ID 关联。

**Q3：RAG 必须用向量检索吗？**
A：不一定。可以只用 BM25 全文检索，也可以向量 + 关键词混合检索（Hybrid Search），后者在专有名词、代码、型号等场景效果更好。
