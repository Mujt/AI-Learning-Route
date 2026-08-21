# -*- coding: utf-8 -*-
"""下载 JavaGuide RAG 系列正文图片到 RAG知识/images/"""
import os
import urllib.request

IMG_DIR = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/images"
os.makedirs(IMG_DIR, exist_ok=True)

URLS = [
    # 页面1: RAG 基础
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-index-and-retrieval-explainer.webp",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-llm-challenges.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-rag-engineering-link.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-2-embedding-map-text-to-semantic-space.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-rag-vs-search-engine.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-2-evolution-stages.png",
    # 页面2: 文档处理
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-overall-link.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-chunking-strategy.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-semantic-loss.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-structure-loss.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-hierarchical-verification-strategy.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-document-processing-build-enterprise-document-processing-pipeline-from-scratch.png",
    # 页面3: 向量库
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-embedding-vector-retrieval.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-why-need-vector-store.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-vector-index-algorithms-Bjze1jhj.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/rag-hnsw-architecture.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/mysql9-vector-cannot-be-used-as-any-type-of-key.png",
    # 页面5: GraphRAG
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-knowledge-relationship-explainer.webp",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-vector-rag-limitation.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-vs-rag.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-core-concept.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-build-process.png",
    "https://oss.javaguide.cn/github/javaguide/ai/rag/graphrag-query-routing.png",
    # 推广图（Interview-Guide 项目，出现在多篇文末）
    "https://oss.javaguide.cn/xingqiu/pratical-project/interview-guide/interview-guide-architecture-diagram.png",
    "https://oss.javaguide.cn/xingqiu/pratical-project/interview-guide/page-skill-jd-parse.png",
    "https://oss.javaguide.cn/xingqiu/pratical-project/interview-guide/page-resume-analysis-detail.png",
    "https://oss.javaguide.cn/xingqiu/pratical-project/interview-guide/tutorial-overview.png",
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for url in URLS:
    name = url.rsplit("/", 1)[-1]
    out = os.path.join(IMG_DIR, name)
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"SKIP {name}")
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        with open(out, "wb") as f:
            f.write(data)
        print(f"OK   {name} size={len(data)}")
    except Exception as e:
        print(f"FAIL {name} {e}")
