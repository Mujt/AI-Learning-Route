# -*- coding: utf-8 -*-
"""验证：检查 Markdown 中引用的图片文件是否存在、目录结构、统计信息"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识"
md_files = [f for f in os.listdir(BASE) if f.endswith(".md") and not f.startswith("_")]
missing = []
total_imgs = 0
for fname in sorted(md_files):
    p = os.path.join(BASE, fname)
    txt = open(p, encoding="utf-8").read()
    refs = re.findall(r"!\[([^\]]*)\]\((images/[^)]+)\)", txt)
    n_titles = len(re.findall(r"^#{1,4} ", txt, re.M))
    n_mermaid = len(re.findall(r"```mermaid", txt))
    n_code = len(re.findall(r"```", txt)) // 2
    print(f"{fname}: chars={len(txt)} titles={n_titles} imgs={len(refs)} mermaid={n_mermaid} codeblocks={n_code}")
    total_imgs += len(refs)
    for alt, rel in refs:
        target = os.path.join(BASE, rel.replace("/", os.sep))
        if not os.path.exists(target):
            missing.append((fname, rel))

print("\n=== 图片目录 ===")
img_dir = os.path.join(BASE, "images")
for f in sorted(os.listdir(img_dir)):
    print(" ", f, os.path.getsize(os.path.join(img_dir, f)))

print(f"\n总引用图片: {total_imgs}")
print("缺失图片:", missing if missing else "无")
