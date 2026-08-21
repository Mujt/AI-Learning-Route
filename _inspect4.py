# -*- coding: utf-8 -*-
import sys
import importlib.util
spec = importlib.util.spec_from_file_location("html2md", r"d:/Buaa_2026/AI-Learning-Route/_html2md.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

html = open(r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw/1.html", encoding="utf-8").read()
b = mod.TreeBuilder()
b.feed(html)
node = mod.find_node(b.root, "div", {"id": "markdown-content"})

def first_ul(n):
    if n.tag == "ul":
        return n
    for c in n.children:
        r = first_ul(c)
        if r:
            return r
ul = first_ul(node)
li = ul.children[0]
print("li children type:", [type(c).__name__ for c in li.children])
for c in li.children:
    print("child tag:", repr(c.tag), "text:", repr(c.text)[:50])
print("inline result:", repr(mod.inline(li.children[0])))
