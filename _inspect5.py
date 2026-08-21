# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = open(r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw/2.html", encoding="utf-8").read()
i = html.find("图表加载中")
print(html[i - 300:i + 100])
