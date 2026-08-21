# -*- coding: utf-8 -*-
"""抓取 JavaGuide RAG 系列 6 个页面的原始 HTML，并列出其中的图片链接"""
import os
import re
import urllib.request

BASE = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识"
RAW_DIR = os.path.join(BASE, "_raw")
os.makedirs(RAW_DIR, exist_ok=True)

URLS = [
    "https://javaguide.cn/ai/rag/rag-basis.html",
    "https://javaguide.cn/ai/rag/rag-document-processing.html",
    "https://javaguide.cn/ai/rag/rag-vector-store.html",
    "https://javaguide.cn/ai/rag/rag-knowledge-update.html",
    "https://javaguide.cn/ai/rag/graphrag.html",
    "https://javaguide.cn/ai/rag/rag-optimization.html",
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for i, url in enumerate(URLS, start=1):
    html_path = os.path.join(RAW_DIR, f"{i}.html")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK {i} size={len(html)}")
        # 提取图片链接
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
        print(f"  imgs({len(imgs)}):")
        for img in imgs[:60]:
            print("   ", img)
    except Exception as e:
        print(f"FAIL {i} {e}")
