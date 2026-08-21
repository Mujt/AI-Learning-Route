# -*- coding: utf-8 -*-
"""解析 HTML 正文，输出每张图片对应的前一个标题，用于定位图片在 Markdown 中的插入位置"""
import os
import re
import sys
import html as htmlmod

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW_DIR = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw"

def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return htmlmod.unescape(s).strip()

for i in range(1, 7):
    p = os.path.join(RAW_DIR, f"{i}.html")
    with open(p, encoding="utf-8") as f:
        html = f.read()
    # 提取正文容器（VitePress: <div class="vp-doc"> 或 <div class="content">）
    m = re.search(r'<div class="vp-doc[^"]*"[^>]*>(.*?)</div>\s*(?:<footer|</main|<div class="page-edit)',
                  html, re.S)
    body = m.group(1) if m else html
    # 按顺序扫描标题和图片
    tokens = re.findall(r'<h([1-3])[^>]*>(.*?)</h\1>|<img[^>]*src=["\']([^"\']+)["\']', body, re.S)
    print(f"===== 页面 {i} =====")
    last_title = "(开头)"
    for t in tokens:
        if t[0]:
            last_title = strip_tags(t[1])
        else:
            src = t[2].split("?")[0]
            name = src.rsplit("/", 1)[-1]
            print(f"  [{last_title}] -> {name}")
    # 检查 interview-guide 推广图出现位置
    for pg in re.findall(r'<img[^>]+src=["\']([^"\']*interview-guide[^"\']+)["\']', html, re.I):
        print(f"  [推广图] -> {pg.split('/')[-1].split('?')[0]}")
