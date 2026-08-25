# 第 4 章 基于 LangChain 的 RAG 系统优化实战

## 学习目标

- 掌握 Advanced-RAG 的整体架构与优化维度
- 掌握 RAG-Fusion 与查询改写技术
- 掌握混合检索（向量 + 关键词）的实现
- 掌握重排序（Rerank）的原理与集成
- 构建一个多策略融合的高质量 RAG 系统

---

## 4.1 Advanced-RAG 架构

Naive RAG（切分 → 向量检索 → 生成）在真实场景中命中率往往不足 60%。**Advanced-RAG** 从"检索前、检索中、检索后、生成"四个阶段全面优化：

```
┌─────────── 检索前 Pre-Retrieval ───────────┐
│  查询改写 / 查询扩展 / 多查询 / HyDE        │
├─────────── 检索中 Retrieval ───────────────┤
│  混合检索(向量+BM25) / 元数据过滤 / 多路召回 │
├─────────── 检索后 Post-Retrieval ──────────┤
│  重排序(Rerank) / 相似度过滤 / 上下文压缩    │
├─────────── 生成 Generation ────────────────┤
│  提示词强化 / 引用溯源 / 可验证回答          │
└────────────────────────────────────────────┘
```

**效果提升优先级**：重排序 > 混合检索 > 查询改写 > 切分优化 > 提示词。

## 4.2 查询改写与扩展（Pre-Retrieval）

### 4.2.1 多查询检索（Multi-Query）

将原问题用 LLM 生成多个角度的子问题，分别检索后合并结果，覆盖不同表述。

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, llm=model
)
docs = retriever.invoke("如何申请年假？")
```

### 4.2.2 HyDE（假设性文档嵌入）

思路：先让 LLM 根据问题**写一段假设答案**，再用假设答案的向量去检索（"用答案找文档"），对答案型问题效果显著。

```python
from langchain_core.output_parsers import StrOutputParser

hyde_prompt = ChatPromptTemplate.from_template(
    "请写一段回答以下问题的假设性回答（约100字）：{question}")
hyde_docs = (hyde_prompt | model | StrOutputParser() |
             retriever).invoke({"question": q})
```

### 4.2.3 查询分解与历史改写

- **查询分解**：复杂问题拆成多个子查询逐个检索。
- **历史感知改写**：结合对话历史重写当前问题（见第 3 章 `create_history_aware_retriever`）。

## 4.3 RAG-Fusion 检索增强

**RAG-Fusion** 的核心是 **RRF（Reciprocal Rank Fusion，倒数排名融合）**：

1. 用 LLM 将原问题生成 3-5 个变体问题。
2. 每个变体独立检索，得到多份"排名列表"。
3. 用 RRF 公式融合打分：`score(d) = Σ 1/(k + rank(d))`（k 通常取 60）。
4. 取融合后 Top-K 作为最终上下文。

**优点**：不同表述召回互补文档，显著提升召回率与覆盖率；无需训练，纯工程实现。

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
# 先做多查询 + 混合检索得到多路结果，再做 RRF 融合（详见混合检索示例）
```

## 4.4 混合检索技术

### 4.4.1 为什么需要混合检索

- **向量检索**擅长语义相近表达，但对专有名词、型号、精确短语（如 "A100 GPU"、"条款 3.2"）不敏感。
- **关键词检索（BM25）**精确匹配强，但不理解同义改写。

混合检索 = 向量 + BM25 互补，**"精确命中靠 BM25，语义泛化靠向量"**。

### 4.4.2 LangChain 实现：EnsembleRetriever

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.vectorstores import Chroma

bm25 = BM25Retriever.from_documents(splits, k=4)
vector_retriever = Chroma.from_documents(splits, embeddings).as_retriever(k=4)

# 按权重融合（RRF 模式）
ensemble = EnsembleRetriever(
    retrievers=[bm25, vector_retriever],
    weights=[0.4, 0.6],      # 关键词/向量权重可调
    c=60,                    # RRF 常数
)
docs = ensemble.invoke("2025年销售目标中 A100 集群的采购预算")
```

**权重调优经验**：IT/代码/型号类场景关键词权重可提到 0.5；自然语言问答场景向量权重 0.6-0.7。

## 4.5 重排序技术（Rerank）

### 4.5.1 为什么需要重排序

初检 Top-K 中常混入"语义相似但答非所问"的噪声。**重排序**用更强的模型对候选列表**逐对打分重排**，把真正相关的文档提到最前。

### 4.5.2 常用重排序模型

| 模型 | 特点 | 场景 |
|------|------|------|
| BGE-Reranker（bge-reranker-v2-m3） | 中文强、开源 | 中文企业场景首选 |
| Cohere Rerank | API 服务、效果顶级 | 海外场景 |
| Cross-Encoder | 通用范式（query+doc 拼接打分） | 自训/开源模型 |
| LLM Rerank | 用 LLM 对候选打分排序 | 无专用模型时兜底 |

### 4.5.3 LangChain 集成

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

compressor = CrossEncoderReranker(
    model=HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3"),
    top_n=3,          # 重排后保留 Top3
)
rerank_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=ensemble
)
docs = rerank_retriever.invoke("退款政策是什么？")
```

**调参要点**：初检 Top-N（如 20-50 个）→ 重排后取 Top-K（3-5 个）。初检数量太少会漏，太多增加重排延迟。

## 4.6 上下文压缩与过滤（Post-Retrieval）

- **相似度阈值过滤**：低于阈值（如 0.7）的片段直接丢弃。
- **LLMChainExtractor**：用 LLM 从检索片段中抽取与问题相关的句子，压缩上下文。
- **文档去重**：`BaseDocumentCompressor` 去重相似片段，避免重复内容稀释注意力。
- **LongContextReorder**：重排片段位置（关键信息放首尾），缓解"上下文迷失"。

## 4.7 RAG 系统优化实战（完整流水线）

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_chroma import Chroma

# ── 1. 数据层 ──
# 加载 → 智能切分（标题感知 + 512字符/overlap 10%）

# ── 2. 多路召回 ──
bm25 = BM25Retriever.from_documents(splits, k=20)          # 关键词路
vector = Chroma.from_documents(splits, embeddings).as_retriever(
    search_kwargs={"k": 20})                                # 向量路
ensemble = EnsembleRetriever(retrievers=[bm25, vector],
                             weights=[0.4, 0.6])

# ── 3. 重排序 ──
reranker = CrossEncoderReranker(
    model=HuggingFaceCrossEncoder("BAAI/bge-reranker-v2-m3"), top_n=4)
final_retriever = ContextualCompressionRetriever(
    base_compressor=reranker, base_retriever=ensemble)

# ── 4. 生成（强化提示词，见第一部分第3章）──
# RAG 提示词 + 引用溯源 + "资料不足请说明"

# ── 5. 评估闭环（见第5章）──
# Ragas 评分 → 定位短板 → 针对性调参
```

### 优化效果参考（企业真实案例）

| 策略 | 命中率/评分提升 |
|------|-----------------|
| 混合检索（+BM25） | 召回率 +15~25% |
| 重排序（bge-reranker） | 答案相关性 +20~35% |
| 查询改写（Multi-Query/HyDE） | 覆盖度 +10~20% |
| 智能切分（结构化） | 精确度 +10~15% |

> 注意：以上数值因数据集而异，务必用第 5 章的评估体系量化验证，而非凭感觉。

---

## 高质量博客推荐

1. **RAG 检索优化全攻略：从混合检索到重排序** — [CSDN](https://blog.csdn.net/2201_75999177/article/details/137516303)
   系统讲解多路召回 + RRF 融合 + Rerank 的完整工程实践。
2. **RAG 完整教程：混合检索与重排序实战（LangChain）** — [vivy-yi 博客](https://blog.vivy-yi.com/2024-10-30-rag-tutorial/)
   以代码驱动讲解 LangChain 实现，可直接复现。
3. **RAG 检索质量优化：改写、扩展与 HyDE** — [QubitTool](https://qubittool.com/ja/landing/rag-document-optimization/)
   检索前优化策略专题，含多查询与假设文档示例。
4. **bge-reranker 重排序模型使用指南** — [BAAI 官方/魔搭社区](https://www.modelscope.cn/models/Xorbits/bge-reranker-v2-m3)
   中文重排序模型的开箱即用指南与效果对比。
5. **Advanced RAG 架构演进与业界实践** — [微信公众号](https://mp.weixin.qq.com/s/50oi2d7m5JZ-G6FdGjnpig)
   一线大厂 RAG 优化实践总结，覆盖十几种优化手段。

## 动手实践

1. 在同一个数据集上对比：Naive RAG vs 混合检索 vs 混合+重排，记录 10 个问题的回答质量。
2. 实现 Multi-Query Retriever，观察多路召回对答案完整性的影响。
3. 调整 BM25/向量权重（0.3/0.7、0.5/0.5、0.7/0.3），找到你数据集的最优权重。
4. 为 RAG 系统添加相似度阈值过滤与来源引用，对比幻觉出现频率。

## 常见问题（FAQ）

**Q1：重排序一定有效吗？**
A：多数场景显著有效，但如果初检召回本身就差（top-20 全是噪声），重排序也无能为力——所以"混合检索打底 + 重排序提纯"是黄金组合。

**Q2：RRF 和权重融合有什么区别？**
A：RRF 基于排名位置融合（对排名敏感、无需分数归一）；权重融合基于相似度分数加权（需要对分数做归一化）。RRF 更稳健，是默认选择。

**Q3：检索应该先扩再压还是先压再扩？**
A：先扩（多路召回 Top-20~50）再压（重排序取 Top-3~5）。扩保证覆盖率，压保证精准率，两个目标分开优化。
