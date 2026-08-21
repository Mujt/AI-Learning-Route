# -*- coding: utf-8 -*-
"""尝试从 javaguide GitHub 仓库获取 RAG 系列 Markdown 源码，提取 Mermaid 图表"""
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW_DIR = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

names = [
    "rag-basis.md",
    "rag-document-processing.md",
    "rag-vector-store.md",
    "rag-knowledge-update.md",
    "graphrag.md",
    "rag-optimization.md",
]

for idx, name in enumerate(names, start=1):
    url = f"https://raw.githubusercontent.com/Snailclimb/JavaGuide/main/docs/ai/rag/{name}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        out = os.path.join(RAW_DIR, f"{idx}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(data)
        mm = re.findall(r"```mermaid\n(.*?)```", data, re.S)
        print(f"OK {idx} {name} len={len(data)} mermaid_blocks={len(mm)}")
    except Exception as e:
        print(f"FAIL {idx} {name} {e}")
