# -*- coding: utf-8 -*-
"""验证讲义图片引用与 images 目录一一对应"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

base = os.path.join("d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识")
md_path = os.path.join(base, "RAG系统完整讲义.md")
md = open(md_path, encoding="utf-8").read()

refs = set(re.findall(r"\]\((images/[^)]+)\)", md))
missing = [r for r in refs if not os.path.exists(os.path.join(base, r))]
img_dir = os.path.join(base, "images")
actual = set(os.listdir(img_dir))

print("图片引用去重数量:", len(refs))
print("缺失引用:", missing if missing else "无")
print("images 目录文件数:", len(actual))

# 检查每个引用对应文件是否存在于目录
unmatched = [r.split("/", 1)[1] for r in refs if os.path.basename(r) not in actual]
print("引用与目录不匹配:", unmatched if unmatched else "无")

# 统计文档规模
print("讲义总字符数:", len(md))
print("标题数量(##):", md.count("\n## "))
print("Mermaid 图表数量:", md.count("```mermaid"))
