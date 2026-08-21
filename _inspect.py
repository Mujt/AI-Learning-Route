# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = open(r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw/1.html", encoding="utf-8").read()

# 1) 看 "常见场景包括这些" 后面的列表结构
idx = html.find("常见场景包括这些")
print("=== 列表结构 ===")
print(html[idx:idx + 1500])
print()

# 2) 看标题锚点结构
idx2 = html.find("为什么需要 RAG")
start = html.rfind("<h2", 0, idx2)
print("=== 标题锚点结构 ===")
print(html[start:start + 400])
