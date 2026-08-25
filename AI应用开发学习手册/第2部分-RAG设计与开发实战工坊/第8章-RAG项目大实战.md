# 第 8 章 RAG 项目大实战：通用文档智能问答多模态系统

## 学习目标

- 完成一个从 0 到 1 的企业级 RAG 项目全流程
- 掌握多模态文档解析（文本 + 表格 + 图片）的工程方案
- 掌握项目技术选型、架构设计、实现部署的完整方法论
- 理解 RAG 商业化落地的产品化要点

---

## 8.1 项目背景与技术选型

### 8.1.1 项目背景

**项目名称**：企业通用文档智能问答系统（支持 PDF/Word/PPT/Excel/扫描件/图片，实现"传文档即问即答"）。

**核心需求**：
- 多格式文档：文本、表格、扫描件、图片混合
- 回答准确可溯源：答案必须引用原文位置
- 支持多轮追问与跨文档关联
- 内网私有化部署，数据不出域
- 管理后台：文档管理、权限、审计

### 8.1.2 技术选型

| 层级 | 选型 | 理由 |
|------|------|------|
| 文档解析 | LlamaParse / RAGFlow DeepDoc | 复杂格式与表格解析能力强 |
| 切分 | MarkdownHeaderTextSplitter + 语义切分 | 保留结构语义 |
| Embedding | BAAI/bge-large-zh-v1.5 | 中文效果优、可私有部署 |
| 向量库 | Milvus（生产）/ Qdrant | 分布式、元数据过滤、混合索引 |
| 混合检索 | BM25 + 向量（EnsembleRetriever） | 精确 + 语义互补 |
| 重排序 | bge-reranker-v2-m3 | 中文重排首选 |
| LLM | Qwen2.5-72B（API 或私有化） | 中文强、可控 |
| 应用框架 | LangChain + FastAPI | 编排灵活 + 高并发服务 |
| 前端 | React + 聊天界面 | 用户体验 |
| 部署 | Docker Compose + Nginx | 内网一键部署 |

## 8.2 知识库构建

### 8.2.1 多模态文档解析流水线

```
上传文档 → 格式识别 → 
  ├── PDF/Word/PPT → LlamaParse 结构解析 → Markdown 结构化文本
  ├── 扫描件/图片 → OCR（PaddleOCR）→ 文本 + 版面坐标
  └── Excel/CSV → 表格结构化提取（行/列/单元格）
→ 统一转为 Markdown → 标题感知切分（保留层级路径） → 向量化入库
```

**关键设计：图片内容处理**
- 表格转 Markdown 表格（可被检索）
- 含文字的图片：OCR 提取文本 + 保留原图，回答时引用"图 X（第 Y 页）"
- 回答涉及图片时，可将图片送入多模态模型（Qwen-VL）做视觉理解

### 8.2.2 元数据体系（检索过滤的基石）

| 元数据字段 | 示例 | 用途 |
|------------|------|------|
| doc_id / doc_name | DOC-2026-001 / 采购合同.pdf | 溯源 |
| page | 12 | 页码定位 |
| section_path | 合同>违约责任>赔偿条款 | 结构定位 |
| department | 采购部 | 权限过滤 |
| doc_type | 合同 / 手册 / 报表 | 类型过滤 |
| created_at | 2026-01-15 | 时效过滤 |

### 8.2.3 父子分块（Parent-Child Chunking）

- **检索用子块**（256 字符，语义精准）
- **送入 LLM 用父块**（包含完整章节，上下文完整）
- 实现：先切父块，再细分父块为子块，子块记录父块 ID；检索命中子块 → 回取父块作为上下文。

## 8.3 检索与问答策略

### 8.3.1 检索链路

```
用户问题 → 查询改写（历史感知）
       → 混合检索：BM25(0.4) + 向量(0.6) → Top-20
       → 元数据过滤（部门/类型/时间，按用户权限）
       → bge-reranker 重排 → Top-4
       → 相似度阈值过滤（<0.55 丢弃）
       → 组装上下文（含元数据引用）
```

### 8.3.2 问答策略

```
主策略：标准 RAG（引用溯源）
  ├── 问题简单且知识库命中良好 → 直接回答
  ├── 涉及全局总结 → 切换到 GraphRAG / 多文档聚合
  ├── 多轮追问 → 历史改写后检索
  └── 检索不足 → 明确回答"资料中未找到"
```

**提示词工程（核心模板）**：

```
你是企业文档智能问答助手。请严格基于【参考资料】回答。
规则：
1. 只使用参考资料中的信息，禁止编造
2. 每句话结尾用 [来源:文件名-页码-章节] 标注
3. 涉及表格数据，用表格形式呈现
4. 资料不足时回答"资料中未找到相关信息"
5. 回答不超过 300 字
```

## 8.4 系统实现与部署

### 8.4.1 系统架构

```
┌────────────────────────────────────────────┐
│  前端（React 聊天界面 / 文档管理后台）         │
├────────────────────────────────────────────┤
│  API 网关（Nginx + JWT 鉴权）                │
├────────────────────────────────────────────┤
│  应用服务（FastAPI）                         │
│    ├── 文档服务：上传/解析/入库/任务队列(Celery)│
│    ├── 问答服务：改写→检索→重排→生成→溯源     │
│    └── 管理服务：文档/权限/审计/统计           │
├────────────────────────────────────────────┤
│  基础设施                                    │
│   Milvus(向量) | PostgreSQL(业务) | Redis(缓存)│
│   Qwen2.5 API | bge-embedding | bge-reranker │
└────────────────────────────────────────────┘
```

### 8.4.2 核心代码骨架（FastAPI）

```python
from fastapi import FastAPI, UploadFile
from langchain.retrievers import EnsembleRetriever, BM25Retriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CrossEncoderReranker
from pymilvus import connections, Collection

app = FastAPI()

def build_retriever():
    vector = MilvusRetriever(collection=COLLECTION, k=20)     # 向量路
    bm25 = BM25Retriever.from_documents(load_index(), k=20)   # 关键词路
    ensemble = EnsembleRetriever(retrievers=[bm25, vector], weights=[0.4, 0.6])
    return ContextualCompressionRetriever(
        base_compressor=CrossEncoderReranker(
            model=bge_reranker, top_n=4),
        base_retriever=ensemble)

@app.post("/api/chat")
async def chat(session_id: str, question: str):
    rewritten = rewrite_with_history(question, get_history(session_id))
    docs = final_retriever.invoke(rewritten)
    answer = generate_answer(question, docs)
    save_history(session_id, question, answer)
    return {"answer": answer, "citations": build_citations(docs)}

@app.post("/api/documents")
async def upload(file: UploadFile):
    task_id = enqueue_parse(file)   # 异步解析任务（Celery）
    return {"task_id": task_id}
```

### 8.4.3 部署要点

1. **Docker Compose 编排**：milvus（etcd+minio+pulsar 或 standalone）、postgres、redis、app、nginx。
2. **GPU 策略**：Embedding/重排可用 CPU；LLM 若本地部署需 GPU（72B 至少 4×A100/80G，或量化后 2 卡）。
3. **高可用**：应用无状态多副本 + 负载均衡；向量库集群 + 数据备份。
4. **安全**：HTTPS + JWT + 细粒度权限 + 操作审计日志。

## 8.5 商业化实战：行业解决方案与产品化

### 8.5.1 可复制的行业方案

| 行业 | 定制点 | 产品形态 |
|------|--------|----------|
| 金融 | 合规审计、财报对比、风控规则问答 | 研报问答助手 |
| 医疗 | 病历解析、指南检索、术语体系 | 临床知识助手 |
| 法律 | 合同审查、法规检索、案例分析 | 法务智能体 |
| 制造 | 设备手册、故障诊断、BOM 查询 | 维修知识平台 |
| 教育 | 教材解析、题库生成、学情分析 | 教学助理 |

### 8.5.2 产品化四要素

1. **效果可度量**：内置评估集，交付时给出"忠实度/召回率"报告。
2. **权限与审计**：企业采购的第一道门槛是合规。
3. **运维友好**：文档更新、模型切换、日志排查都要可视化。
4. **成本可控**：提供"API 模式/混合/全私有"三档部署，匹配不同预算。

### 8.5.3 演进路线

```
V1 基础问答（单文档 RAG）→ V2 多模态+多文档（本系统）
→ V3 智能体化（自动检索/联网/工具）→ V4 行业垂直（微调 + 图谱）
```

---

## 高质量博客推荐

1. **从零搭建企业级 RAG 问答系统（架构与部署全流程）** — [微信公众号](https://mp.weixin.qq.com/s/8a3pXyR2eNmJkFsT5yGcYg)
   一线架构师分享的完整生产架构，含踩坑记录。
2. **多模态文档解析在 RAG 中的工程实践** — [CSDN](https://blog.csdn.net/weixin_43572595/article/details/146050899)
   表格、扫描件、图片的解析与检索方案详解。
3. **RAG 产品化落地的 10 个坑与解法** — [知乎专栏](https://zhuanlan.zhihu.com/p/675872945)
   从"demo 能用"到"产品能卖"的差距与对策。
4. **Milvus 向量数据库生产实践指南** — [Milvus 官方中文文档](https://milvus.io/docs/zh/overview.md)
   索引类型、分区、标量过滤的权威配置参考。
5. **企业私有化大模型知识库建设方案** — [阿里云开发者社区](https://developer.aliyun.com/article/1631042)
   含本地模型部署与知识库治理的整体方案。

## 动手实践（项目验收标准）

1. **MVP**：上传 10 份 PDF → 可问答 → 答案带引用 → 答非所问率 < 20%。
2. **进阶**：接入扫描件 OCR 与 Excel 表格解析；支持多轮追问。
3. **生产化**：Docker 一键部署；接入评估集，忠实度 > 0.8；添加权限与审计。
4. **产品化**：编写项目方案书（技术选型、架构图、成本估算、里程碑）。

## 常见问题（FAQ）

**Q1：先做 POC 还是直接上生产架构？**
A：先用 LangChain + Chroma 快速跑通 POC（1-2 周），验证效果后再迁移 Milvus 等生产组件。避免过早陷入工程细节。

**Q2：多模态系统一定要用视觉模型吗？**
A：视需求而定。多数场景"OCR 提取文本 + 引用原图"即可；只有需要理解图表语义、照片内容时才引入 VLM。

**Q3：知识库文档太多，检索变慢怎么办？**
A：分层治理——按部门/项目分 Collection 或分区；建立"热文档/冷文档"索引；启用 HNSW 参数调优与 GPU 加速。
