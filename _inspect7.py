# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

raw = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw"
for i in [2, 3, 4, 6]:
    html = open(os.path.join(raw, f"{i}.html"), encoding="utf-8").read()
    # 查找 flowchart / graph / sequenceDiagram / mermaid 定义文本
    hits = re.findall(r'(?:flowchart|graph\s+[A-Z]{2}|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie\s+showData)\b.{0,80}', html)
    print(f"=== 页面 {i}: mermaid 定义候选 {len(hits)} ===")
    for h in hits[:8]:
        print("   ", repr(h[:90]))
