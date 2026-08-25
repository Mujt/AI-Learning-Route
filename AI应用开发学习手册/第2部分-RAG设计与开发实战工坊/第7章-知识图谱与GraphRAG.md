# 第 7 章 知识图谱与 GraphRAG

## 学习目标

- 理解知识图谱与 RAG 结合的价值
- 掌握 Neo4j 图数据库的核心概念与操作
- 理解 GraphRAG 的索引与检索原理
- 独立完成一个基于知识图谱的企业知识问答

---

## 7.1 知识图谱与 RAG

### 7.1.1 什么是知识图谱

知识图谱（Knowledge Graph）用**三元组（头实体, 关系, 尾实体）**表示知识，例如：

```
（华为, 创始人, 任正非）
（华为, 总部位于, 深圳）
（任正非, 国籍, 中国）
```

实体是节点（Node），关系是边（Edge），形成一张语义网络。

### 7.1.2 为什么 RAG 需要知识图谱

向量 RAG 的三大弱点，知识图谱恰好可以弥补：

| 向量 RAG 弱点 | 知识图谱的优势 |
|---------------|----------------|
| 多跳推理差（"A 的供应商 B 的客户是谁"） | 图遍历天然支持多跳 |
| 关系理解弱（实体间复杂关系） | 显式建模关系 |
| 聚合统计难（"哪个部门员工最多"） | Cypher 查询直接统计 |
| 无全局视角 | 图谱提供结构化全局视图 |

### 7.1.3 RAG 与知识图谱的三种结合方式

1. **GraphRAG（微软）**：用 LLM 抽取实体关系建图，再从图中检索子图辅助回答。
2. **Neo4j + RAG 混合**：图查询（精确关系）+ 向量检索（语义）双路召回。
3. **文本转 Cypher**：让 LLM 将问题翻译为图查询语句（Text-to-Cypher）。

## 7.2 Neo4j 图数据库

### 7.2.1 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| Node（节点） | 实体，可带标签与属性 | 关系表的一行 |
| Relationship（关系） | 节点间的有向边，可带属性 | 外键关联 |
| Label（标签） | 节点类型（如 Person、Company） | 表名 |
| Property（属性） | 键值对 | 字段值 |
| Cypher | 声明式图查询语言 | SQL 的图版本 |

### 7.2.2 Cypher 基本语法

```cypher
// 创建节点与关系
CREATE (h:Person {name:'任正非'})
CREATE (c:Company {name:'华为', founded:1987})
CREATE (h)-[:FOUNDED]->(c)

// 查询：华为的创始人
MATCH (c:Company {name:'华为'})<-[:FOUNDED]-(p:Person)
RETURN p.name

// 多跳查询：与华为总部所在城市相关的所有公司
MATCH (c:Company {name:'华为'})-[:HQ]->(:City)<-[:HQ]-(other:Company)
RETURN other.name

// 聚合统计
MATCH (e:Employee)-[:WORKS_AT]->(:Dept {name:'研发部'})
RETURN count(e)
```

### 7.2.3 Neo4j 部署与接入

- **部署**：Neo4j Desktop（开发）/ Docker（生产）`docker run -p 7474:7474 -p 7687:7687 neo4j:5`
- **Python 接入**：`neo4j` 官方驱动 或 LangChain `Neo4jGraph` 集成。

```python
from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(url="bolt://localhost:7687",
                   username="neo4j", password="password")
graph.query("MATCH (n) RETURN count(n) AS total")
```

## 7.3 GraphRAG 原理

GraphRAG 由微软研究院于 2024 年提出，论文 *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*，针对向量 RAG **无法回答全局性问题**（如"本语料库的核心主题有哪些"）的缺陷。

### 7.3.1 索引阶段（Indexing）

```
① 文本分块 → ② LLM 抽取实体与关系（构建局部图）
③ 实体描述语义嵌入 → ④ 社区检测（Leiden 算法）
⑤ 社区层级聚合 → ⑥ 为每个社区生成摘要（Community Summary）
```

- **实体抽取**：Prompt 驱动 LLM 从文本块中抽取实体、关系与描述（保留不确定性）并去重合并。
- **社区检测**：用 Leiden 算法把图分成层次化社区（类似"篇章→章节→段落"）。
- **社区摘要**：对每个社区用 LLM 生成概括性摘要（图约简，控制规模）。

### 7.3.2 检索阶段（Querying）

- **局部检索（Local Search）**：先向量检索找到相关实体，沿图扩展邻居，把实体描述 + 社区摘要拼进上下文。
- **全局检索（Global Search）**：用 Map-Reduce 对所有社区摘要提问——先让 LLM 对每个社区摘要分别回答问题（Map），再综合所有答案生成全局结论（Reduce）。

```
问题："这份公司文档中涉及哪些主要风险？"
Map:    对每个社区摘要 → LLM 独立回答该社区涉及的风险
Reduce: 汇总所有社区的答案 → 生成全局综合回答
```

### 7.3.3 GraphRAG 适用场景

| 场景 | 效果 |
|------|------|
| 全局性、总结性问题 | 显著优于向量 RAG |
| 实体关系多跳推理 | 强 |
| 需要理解语料整体结构 | 强 |
| 精确事实问答 | 需配合局部检索，不比向量 RAG 强太多 |
| 成本 | 建图消耗大量 LLM Token（比向量 RAG 贵 10-50 倍） |

## 7.4 GraphRAG 实战

### 7.4.1 快速上手（微软官方实现）

```bash
pip install graphrag
# 准备输入文档目录 ./ragtest/input/*.txt
graphrag index --root ./ragtest      # 建立索引（需配置 LLM API）
graphrag query --root ./ragtest --method global "主要风险有哪些？"
graphrag query --root ./ragtest --method local "某实体的关系是什么？"
```

### 7.4.2 LangChain + Neo4j 方案（更可控）

```python
# 1. 用 LLM 从文本抽取三元组并写入 Neo4j
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

llm = ChatOpenAI(model="gpt-4o-mini")
transformer = LLMGraphTransformer(llm=llm, allowed_nodes=["Person","Company","City"],
                                  allowed_relationships=["FOUNDED","HQ","EMPLOYED_BY"])

docs = loader.load()
graph_documents = transformer.convert_to_graph_documents(docs)
graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password")
graph.add_graph_documents(graph_documents, baseEntityLabel=True)

# 2. 图 + 向量混合问答：实体查询走图，语义查询走向量
# 3. Text-to-Cypher：让 LLM 生成 Cypher 查询
```

### 7.4.3 中文优化建议

- **中文实体抽取**：使用中文能力强的模型（Qwen/DeepSeek），并在 Prompt 中强调中英混合实体名处理。
- **同义词归并**：设置 `merge` 规则处理"华为 / 华为技术有限公司 / Huawei"。
- **结合向量库**：GraphRAG + 向量双引擎，按问题类型路由（全局性→Graph，事实性→向量）。

---

## 高质量博客推荐

1. **GraphRAG 原理与源码剖析（微软开源）** — [知乎专栏](https://zhuanlan.zhihu.com/p/13925846058)
   从论文到代码的深度拆解，含社区检测与 Map-Reduce 检索细节。
2. **GraphRAG 中文部署实战：基于 Neo4j 的可视化** — [百度智能云开发者社区](https://developer.baidu.com/article/details/3381412)
   完整部署流程 + Neo4j Browser 可视化查询演示。
3. **GraphRAG 基于 Neo4j 的六步智能检索** — [博客园](https://www.cnblogs.com/ChineseWind/p/19017297)
   从建图到检索的六步方法论，工程可落地。
4. **Neo4j Cypher 查询语言入门教程** — [Neo4j 官方（中文）](https://neo4j.com/docs/cypher-manual/current/introduction/)
   图查询语法权威参考。
5. **知识图谱 + RAG：企业级知识库的未来形态** — [微信公众号](https://mp.weixin.qq.com/s/8qZ4h7wQvFmJTb3yFkpHxw)
   图检索与向量检索融合的业界实践案例。

## 动手实践

1. 用 Neo4j 创建一个 20 个节点的人物关系图谱，练习 5 种 Cypher 查询。
2. 用 LLMGraphTransformer 从 3 篇公司文档中自动抽取实体关系建图。
3. 部署 GraphRAG 并对比：同一语料下，全局问题用 GraphRAG vs 向量 RAG 的答案质量。
4. 实现"问题路由"：全局性问题走 GraphRAG，事实性问题走向量 RAG。

## 常见问题（FAQ）

**Q1：GraphRAG 比向量 RAG 更好吗？**
A：不是"更好"，是"互补"。GraphRAG 擅长全局总结与多跳推理，但建图成本高、事实精确问答未必更强。生产上建议混合架构。

**Q2：建图很贵怎么办？**
A：控制语料规模（选核心文档）、用便宜的国产模型（DeepSeek）做抽取、只对必要字段建图、采用增量建图。

**Q3：Text-to-Cypher 生成错误查询怎么办？**
A：多管齐下——给模型提供 Schema 与示例、限制只读查询、对生成的 Cypher 做语法校验、加入"查询失败就回退向量检索"的兜底逻辑。
