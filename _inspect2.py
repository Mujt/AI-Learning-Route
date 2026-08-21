# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"d:/Buaa_2026/AI-Learning-Route")
import importlib.util
spec = importlib.util.spec_from_file_location("html2md", r"d:/Buaa_2026/AI-Learning-Route/_html2md.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

html = open(r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw/1.html", encoding="utf-8").read()
b = mod.TreeBuilder()
b.feed(html)
node = mod.find_node(b.root, "div", {"id": "markdown-content"})
# 找第一个 ul
def first_ul(n):
    if n.tag == "ul":
        return n
    for c in n.children:
        r = first_ul(c)
        if r:
            return r
ul = first_ul(node)
print("UL children tags:", [c.tag for c in ul.children])
for li in ul.children[:3]:
    print("LI children:", [(c.tag, repr(c.text)[:40] if c.tag is None else c.tag) for c in li.children])
