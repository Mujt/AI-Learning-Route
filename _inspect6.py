# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

raw = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw"
for i in range(1, 7):
    html = open(os.path.join(raw, f"{i}.html"), encoding="utf-8").read()
    # 找到所有 mermaid 相关容器，打印其属性与内部文本前 200 字
    containers = re.findall(r'<div class="mermaid[^"]*"[^>]*>(.*?)</div>\s*(?:<div|</div>|$)', html, re.S)
    print(f"=== 页面 {i}: mermaid containers = {len(containers)} ===")
    for idx, c in enumerate(containers[:5]):
        # 打印属性
        attrs = re.findall(r'data-[a-zA-Z-]+="[^"]*"', html[max(0, html.find(c)-300):html.find(c)][-400:])
        print(f"  container {idx}: attrs={attrs[:5]}")
        print(f"    text={c[:150]!r}")
