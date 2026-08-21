# -*- coding: utf-8 -*-
"""将抓取的 JavaGuide RAG 系列 HTML 正文完整转换为 Markdown（含图片本地引用）"""
import os
import re
import sys
import html as htmlmod
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW_DIR = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识/_raw"
OUT_DIR = r"d:/Buaa_2026/AI-Learning-Route/讲义/第2周/RAG知识"

FILES = [
    ("1.html", "https://javaguide.cn/ai/rag/rag-basis.html",
     "1-RAG基础概念-检索生成与工程取舍.md", "RAG 基础概念：检索、生成与工程取舍"),
    ("2.html", "https://javaguide.cn/ai/rag/rag-document-processing.html",
     "2-RAG文档处理与切分策略.md", "RAG 文档处理与切分策略"),
    ("3.html", "https://javaguide.cn/ai/rag/rag-vector-store.html",
     "3-RAG向量索引算法和向量数据库.md", "RAG 向量索引算法和向量数据库"),
    ("4.html", "https://javaguide.cn/ai/rag/rag-knowledge-update.html",
     "4-RAG知识库文档更新.md", "RAG 知识库文档更新策略"),
    ("5.html", "https://javaguide.cn/ai/rag/graphrag.html",
     "5-GraphRAG用图结构补充向量检索.md", "GraphRAG 详解"),
    ("6.html", "https://javaguide.cn/ai/rag/rag-optimization.html",
     "6-RAG优化-从召回到上下文工程.md", "RAG 检索优化"),
]

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "pre", "table", "div"}
PRE_BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "pre", "table", "tr"}

MERMAID_BLOCKS = []  # 当前页面的 Mermaid 图表源码列表（按顺序消费）


class Node:
    __slots__ = ("tag", "attrs", "children", "text")

    def __init__(self, tag=None, attrs=None, text=""):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.text = text


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in ("img", "br", "hr"):
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) > 1 and self.stack[-1].tag == tag:
            self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(Node(text=data))


def get_attr(node, key):
    return node.attrs.get(key, "")


def inline(node, join_blocks=True):
    """行内渲染：把子节点转成行内文本。"""
    if node.tag is None:
        return node.text
    out = []
    for ch in node.children:
        if ch.tag is None:
            out.append(ch.text)
        elif ch.tag == "strong":
            out.append("**" + inline(ch) + "**")
        elif ch.tag == "em":
            out.append("*" + inline(ch) + "*")
        elif ch.tag == "code":
            out.append("`" + inline(ch) + "`")
        elif ch.tag == "a":
            href = get_attr(ch, "href")
            txt = inline(ch)
            out.append("[{}]({})".format(txt, href) if href else txt)
        elif ch.tag == "img":
            src = get_attr(ch, "src").split("?")[0]
            name = src.rsplit("/", 1)[-1]
            alt = get_attr(ch, "alt") or name
            out.append("![{}](images/{})".format(alt, name))
        elif ch.tag == "br":
            out.append("\n")
        elif ch.tag == "span":
            out.append(inline(ch))
        elif ch.tag == "sub":
            out.append("<sub>" + inline(ch) + "</sub>")
        elif ch.tag == "sup":
            out.append("<sup>" + inline(ch) + "</sup>")
        else:
            out.append(inline(ch))
    return "".join(out)


def render_table(node):
    # 收集行（thead/tbody 内也有 tr）
    rows = []

    def walk(n):
        for c in n.children:
            if c.tag == "tr":
                cells = []
                for cell in c.children:
                    if cell.tag in ("td", "th"):
                        cells.append(inline(cell).strip().replace("\n", " "))
                if cells:
                    rows.append(cells)
            elif c.tag in ("thead", "tbody", "table"):
                walk(c)

    walk(node)
    if not rows:
        return ""
    # 第一个非表头行作为分隔
    lines = []
    header = rows[0]
    body = rows[1:]
    ncols = max(len(r) for r in rows)
    lines.append("| " + " | ".join(h for h in header) + " |")
    lines.append("|" + "---|" * ncols)
    for r in body:
        pad = r + [""] * (ncols - len(r))
        lines.append("| " + " | ".join(pad) + " |")
    return "\n".join(lines)


def render_list(node, ordered):
    lines = []
    index = 1
    for li in node.children:
        if li.tag != "li":
            continue
        # 提取 li 的直接文本内容与嵌套列表
        text_parts = []
        nested = []
        for ch in li.children:
            if ch.tag in ("ul", "ol"):
                nested.append(ch)
            else:
                text_parts.append(inline(ch))
        prefix = ("{}.".format(index) if ordered else "-")
        index += 1
        lines.append("{} {}".format(prefix, "".join(text_parts).strip()))
        for n in nested:
            sub = render_list(n, n.tag == "ol")
            for s in sub.splitlines():
                lines.append("    " + s)
    return "\n".join(lines)


def heading_text(node):
    """提取标题文本：header-anchor 里包裹的才是标题文字，去掉链接语法保留文本"""
    out = []
    for ch in node.children:
        if ch.tag == "a" and "header-anchor" in ch.attrs.get("class", ""):
            out.append(plain_text(ch))
        elif ch.tag is None:
            out.append(ch.text)
        else:
            out.append(inline(ch))
    return "".join(out).strip()


def render(node, level=0):
    out = []
    for ch in node.children:
        if ch.tag is None:
            txt = ch.text
            if txt.strip():
                out.append(txt)
            continue
        tag = ch.tag
        if tag in ("h1", "h2", "h3", "h4"):
            n = int(tag[1])
            out.append("\n\n" + "#" * n + " " + heading_text(ch) + "\n")
        elif tag == "p":
            txt = inline(ch).strip()
            if txt:
                out.append("\n\n" + txt)
        elif tag == "ul":
            out.append("\n\n" + render_list(ch, False))
        elif tag == "ol":
            out.append("\n\n" + render_list(ch, True))
        elif tag == "blockquote":
            q = render(ch)
            lines = ["".join("> " + l for l in q.splitlines())]
            out.append("\n\n" + "\n".join(lines))
        elif tag == "pre":
            # 代码块
            code = ""
            for c in ch.children:
                if c.tag == "code":
                    code = plain_text(c)
                else:
                    code += plain_text(c)
            lang = ""
            m = re.search(r"language-(\w+)", " ".join(ch.attrs.values()))
            if m:
                lang = m.group(1)
            out.append("\n\n```{}\n{}\n```".format(lang, code.rstrip()))
        elif tag == "table":
            out.append("\n\n" + render_table(ch))
        elif tag == "img":
            src = get_attr(ch, "src").split("?")[0]
            name = src.rsplit("/", 1)[-1]
            alt = get_attr(ch, "alt") or name
            out.append("\n\n![{}](images/{})".format(alt, name))
        elif tag == "hr":
            out.append("\n\n---\n")
        elif tag in ("div", "section", "article"):
            cls = ch.attrs.get("class", "")
            if "mermaid" in cls:
                if MERMAID_BLOCKS:
                    out.append("\n\n```mermaid\n" + MERMAID_BLOCKS.pop(0).strip() + "\n```")
                else:
                    out.append("\n\n<!-- Mermaid 图表（原文为懒加载图表，未获取到源码） -->")
                continue
            out.append(render(ch))
        elif tag in ("strong", "em", "code", "a", "span"):
            out.append(inline(ch))
        elif tag == "br":
            out.append("\n")
        else:
            out.append(render(ch))
    return "".join(out)


def plain_text(node):
    """提取纯文本（代码块内剥掉 span）"""
    parts = []
    for ch in node.children:
        if ch.tag is None:
            parts.append(ch.text)
        else:
            parts.append(plain_text(ch))
    return "".join(parts)


def find_node(node, tag, attrs):
    """深度优先查找满足条件的节点"""
    if node.tag == tag and all(node.attrs.get(k) == v for k, v in attrs.items()):
        return node
    for ch in node.children:
        r = find_node(ch, tag, attrs)
        if r:
            return r
    return None


def convert(html):
    builder = TreeBuilder()
    builder.feed(html)
    content_node = find_node(builder.root, "div", {"id": "markdown-content"})
    if content_node is None:
        return ""
    md = render(content_node)
    # 合并多余空行
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


def main():
    for raw_name, url, md_name, title in FILES:
        idx = int(raw_name.split(".")[0])
        with open(os.path.join(RAW_DIR, raw_name), encoding="utf-8") as f:
            html = f.read()
        # 从 GitHub Markdown 源码加载 Mermaid 图表
        md_src_path = os.path.join(RAW_DIR, f"{idx}.md")
        global MERMAID_BLOCKS
        MERMAID_BLOCKS = []
        if os.path.exists(md_src_path):
            with open(md_src_path, encoding="utf-8") as f:
                src = f.read()
            MERMAID_BLOCKS = re.findall(r"```mermaid\n(.*?)```", src, re.S)
        md = convert(html)
        header = (
            "# {title}\n\n"
            "> **原文来源**：[JavaGuide - {title}]({url})（作者：Guide）\n"
            "> 本文为网页原文的完整抓取转换：正文文字、表格、代码块均按原文保留，"
            "图片已下载到本目录 `images/` 下，Mermaid 图表以源码形式嵌入。\n\n"
            "---\n"
        ).format(title=title, url=url)
        out_path = os.path.join(OUT_DIR, md_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(header + "\n" + md + "\n")
        print("WROTE {} ({} chars, mermaid={})".format(md_name, len(md), len(MERMAID_BLOCKS)))


if __name__ == "__main__":
    main()
