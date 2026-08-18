# -*- coding: utf-8 -*-
"""课1：Python 基础与 Skills 开发实战 —— PPT 构建引擎（WPS COM 自动化 / harness-anything 工作流）"""
import os, pythoncom, win32com.client

OUT = os.path.dirname(os.path.abspath(__file__))
FT = 'SimHei'
FB = 'Microsoft YaHei'
CF = 'Consolas'
O = '#306998'
B = '#000000'
D = '#333333'
G = '#666666'
ACC = '#4B8BBE'
ORG = '#FF8C00'

def h2b(h):
    h = h.lstrip('#')
    r, g, bl = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (bl << 16) | (g << 8) | r

def rect(s, x, y, w, h, color):
    r = s.AddShape(1, x, y, w, h)
    r.Fill.ForeColor.RGB = color
    r.Fill.Visible = True
    r.Line.Visible = False
    return r

def circle(s, x, y, w, h, color):
    c = s.AddShape(9, x, y, w, h)
    c.Fill.ForeColor.RGB = color
    c.Fill.Visible = True
    c.Line.Visible = False
    return c

def txt(s, x, y, w, h, text, fs=24, color=0x333333, bold=False,
        align=1, font=FB, spacing=1.3):
    t = s.AddTextbox(1, x, y, w, h)
    tr = t.TextFrame.TextRange
    tr.Text = text
    tr.Font.Size = fs
    tr.Font.Color = color
    tr.Font.Name = font
    tr.Font.Bold = bold
    tr.ParagraphFormat.Alignment = align
    try:
        tr.ParagraphFormat.SpaceWithin = spacing
    except:
        pass
    return t

def draw_text(s, e):
    return txt(s, e['x'], e['y'], e['w'], e['h'], e['text'],
               fs=e.get('fs', 24), color=h2b(e.get('color', D)),
               bold=e.get('bold', False), align=e.get('align', 1),
               font=e.get('font', FB), spacing=e.get('line_spacing', 1.3))

def draw_shape(s, e):
    x, y, w = e['x'], e['y'], e['w']
    h = e.get('h', 10)
    c = h2b(e.get('color', O))
    if e.get('shape') == 'circle':
        circle(s, x, y, w, h, c)
    else:
        rect(s, x, y, w, h, c)

def draw_table(s, e):
    rows, cols = e['rows'], e['cols']
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    dta = e['data']
    hdr = h2b(e.get('header_color', O))
    row_h = max(h // rows, 28)
    col_w = w // cols
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + c * col_w, y + r * row_h
            val = dta[r][c] if r < len(dta) and c < len(dta[r]) else ''
            is_h = (r == 0)
            bg = hdr if is_h else (0xFFFFFF if r % 2 == 0 else h2b('#EEF3F9'))
            fs = e.get('th_fs', 13) if is_h else e.get('td_fs', 14)
            tc = 0xFFFFFF if is_h else 0x333333
            al = 2 if c > 0 else 1
            rect(s, cx, cy, col_w, row_h, bg)
            if val:
                tb = s.AddTextbox(1, cx + 4, cy + 2, col_w - 8, row_h - 4)
                tr = tb.TextFrame.TextRange
                tr.Text = str(val)
                tr.Font.Size = fs
                tr.Font.Color = tc
                tr.Font.Name = FT if is_h else FB
                tr.Font.Bold = is_h
                tr.ParagraphFormat.Alignment = al
                tb.TextFrame.WordWrap = False

def draw_code(s, e):
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    code = e['code']
    title = e.get('title', '')
    fs = e.get('fs', 12)
    rect(s, x, y, w, h, h2b('#1E1E2E'))
    if title:
        rect(s, x, y, w, 20, h2b('#2A2A3A'))
        circle(s, x + 8, y + 6, 8, 8, h2b('#FF5F57'))
        circle(s, x + 22, y + 6, 8, 8, h2b('#FEBC2E'))
        circle(s, x + 36, y + 6, 8, 8, h2b('#28C840'))
        tb = s.AddTextbox(1, x + 52, y + 3, w - 60, 14)
        tr0 = tb.TextFrame.TextRange
        tr0.Text = title
        tr0.Font.Size = 10
        tr0.Font.Color = h2b('#9AA0A6')
        tr0.Font.Name = CF
        tr0.ParagraphFormat.Alignment = 1
        ty = y + 22
        th = h - 26
    else:
        ty = y + 6
        th = h - 12
    t = s.AddTextbox(1, x + 12, ty, w - 20, th)
    tr = t.TextFrame.TextRange
    tr.Text = code
    tr.Font.Size = fs
    tr.Font.Color = h2b('#D4D4D4')
    tr.Font.Name = CF
    tr.ParagraphFormat.Alignment = 1
    try:
        tr.ParagraphFormat.SpaceWithin = 1.05
    except:
        pass
    return t

def draw_card_list_wide(s, e):
    items = e['items']
    sy = e.get('start_y', 90)
    ih = e.get('item_h', 52)
    cols = [O, ORG, ACC, O, ORG, ACC]
    for i, item in enumerate(items):
        y = sy + i * ih
        col = h2b(cols[i % len(cols)])
        circle(s, 100, y + 4, 34, 34, col)
        t2 = s.AddTextbox(1, 100, y + 4, 34, 34)
        tr2 = t2.TextFrame.TextRange
        tr2.Text = item['num']
        tr2.Font.Size = 14
        tr2.Font.Color = 0xFFFFFF
        tr2.Font.Name = FT
        tr2.Font.Bold = True
        tr2.ParagraphFormat.Alignment = 2
        txt(s, 150, y + 2, 300, 30, item['title'], fs=24,
            color=h2b('#1A1A1A'), bold=True, font=FT)
        txt(s, 150, y + 34, 700, 18, item['sub'], fs=16,
            color=h2b('#555555'), font=FB)

def draw_tagline_bar(s, e):
    rect(s, 30, 498, 900, 28, h2b(e.get('color', O)))
    txt(s, 40, 501, 880, 22, e['text'], fs=14, color=0xFFFFFF,
        bold=True, align=2, font=FB)

def draw_num_big(s, e):
    c = h2b(e.get('color', O))
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    num_h = int(h * 0.40)
    gap = int(h * 0.10)
    lbl_h = int(h * 0.50)
    t1 = s.AddTextbox(1, x, y, w, num_h)
    tr1 = t1.TextFrame.TextRange
    tr1.Text = e['num']
    tr1.Font.Size = e.get('fs', 34)
    tr1.Font.Color = c
    tr1.Font.Name = 'Arial'
    tr1.Font.Bold = True
    tr1.ParagraphFormat.Alignment = 2
    t2 = s.AddTextbox(1, x, y + num_h + gap, w, lbl_h)
    tr2 = t2.TextFrame.TextRange
    tr2.Text = e['label']
    tr2.Font.Size = 14
    tr2.Font.Color = h2b(G)
    tr2.Font.Name = FB
    tr2.ParagraphFormat.Alignment = 2

def draw_cards_2x3(s, e):
    items = e['items']
    sy = e.get('start_y', 80)
    cw, ch = 295, 145
    gx, gy = 15, 14
    for i, item in enumerate(items):
        r, c = i // 3, i % 3
        x = 22 + c * (cw + gx)
        y = sy + r * (ch + gy)
        col = h2b(item['color'])
        rect(s, x, y, cw, 5, col)
        txt(s, x + 12, y + 16, cw - 24, 32, item['title'], fs=22,
            color=col, bold=True, align=1, font=FT)
        txt(s, x + 12, y + 56, cw - 24, ch - 62, item['desc'], fs=15,
            color=h2b('#333333'), align=1, font=FB, spacing=1.35)

def draw_cards_2x2(s, e):
    items = e['items']
    sy = e.get('start_y', 80)
    cw, ch = 405, 190
    gx, gy = 25, 25
    for i, item in enumerate(items):
        r, c = i // 2, i % 2
        x = 45 + c * (cw + gx)
        y = sy + r * (ch + gy)
        col = h2b(item['color'])
        rect(s, x, y, cw, 5, col)
        txt(s, x + 18, y + 16, cw - 36, 32, item['title'], fs=24,
            color=col, bold=True, align=1, font=FT)
        txt(s, x + 18, y + 58, cw - 36, ch - 68, item['desc'], fs=16,
            color=h2b('#333333'), align=1, font=FB, spacing=1.4)

ROUTERS = {
    'text': draw_text,
    'shape': draw_shape,
    'table': draw_table,
    'code': draw_code,
    'card_list_wide': draw_card_list_wide,
    'tagline_bar': draw_tagline_bar,
    'num_big': draw_num_big,
    'cards_2x3': draw_cards_2x3,
    'cards_2x2': draw_cards_2x2,
}

slides = []

# ---- S1: 封面 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 8, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 532, 'w': 960, 'h': 8, 'color': O},
    {'type': 'text', 'x': 60, 'y': 70, 'w': 840, 'h': 56, 'text': 'Python 基础与 Skills 开发实战',
     'fs': 48, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 140, 'w': 840, 'h': 30, 'text': '第2周 · 第1课 · 唯一一堂语法课',
     'fs': 22, 'color': D, 'align': 2, 'font': FB},
    {'type': 'shape', 'shape': 'rect', 'x': 380, 'y': 188, 'w': 200, 'h': 3, 'color': ORG},
    {'type': 'num_big', 'x': 120, 'y': 220, 'w': 220, 'h': 90, 'num': '120min', 'label': '课时长度', 'color': O, 'fs': 40},
    {'type': 'num_big', 'x': 370, 'y': 220, 'w': 220, 'h': 90, 'num': '8', 'label': '知识块', 'color': ORG, 'fs': 40},
    {'type': 'num_big', 'x': 620, 'y': 220, 'w': 220, 'h': 90, 'num': '30min', 'label': 'Skills 实战', 'color': ACC, 'fs': 40},
    {'type': 'text', 'x': 60, 'y': 340, 'w': 840, 'h': 60,
     'text': '从「读懂 Python 代码」到「亲手开发一个 Skills 技能包」\n读懂 · 会问 · 能开发',
     'fs': 20, 'color': D, 'bold': True, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 60, 'y': 450, 'w': 840, 'h': 30,
     'text': '变量 · 类型 · 条件 · 循环 · 列表 · 字典 · 函数 · 类 · Skills',
     'fs': 16, 'color': G, 'align': 2, 'font': FB},
]})

# ---- S2: 课程定位 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '一、导入 · 这堂课学什么',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 78, 'w': 420, 'h': 34, 'text': '为什么 Python 代码到处都是？',
     'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 120, 'w': 440, 'h': 160,
     'text': '· 后端开发：FastAPI / Django / Flask\n· AI Agent 框架：LangChain / CrewAI\n· 数据分析 / 机器学习（第3周）\n· 爬虫、自动化脚本',
     'fs': 18, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'shape', 'shape': 'rect', 'x': 45, 'y': 292, 'w': 440, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 45, 'y': 312, 'w': 440, 'h': 70,
     'text': '本课目标 = 看到一段 Python 代码，\n能大致说出它「在干什么」。',
     'fs': 18, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 500, 'y': 78, 'w': 420, 'h': 34, 'text': '四个「能回答」的问题',
     'fs': 26, 'color': ACC, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 120, 'w': 440, 'h': 250,
     'text': '① 这段代码在干什么？\n② 数据从哪来、到哪去？\n③ 哪里是核心逻辑？\n④ 想改一个功能，该改哪里？\n\n读代码 ≠ 写代码\n读代码只需写代码 30% 的知识量',
     'fs': 18, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.65},
    {'type': 'tagline_bar', 'text': '不要求背语法、不要求熟练写 —— 看到认识、不懂会问、能猜会验', 'color': O},
]})

# ---- S3: 时间分配 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '时间分配总览 · 8 个知识块',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'table', 'x': 60, 'y': 80, 'w': 580, 'h': 400, 'rows': 9, 'cols': 3,
     'header_color': O, 'th_fs': 14, 'td_fs': 14,
     'data': [
         ['段', '内容', '分钟'],
         ['一', '导入与本课目标', '8'],
         ['二', '环境准备 + Hello World', '10'],
         ['三', '变量 / 类型 / 条件', '20'],
         ['四', '循环 / 列表 / 字典', '20'],
         ['五', '函数与模块', '15'],
         ['六', '面向对象：看懂「类」', '15'],
         ['七', 'Skills 开发实战（重点）', '30'],
         ['八', '总结 / 作业 / FAQ', '2'],
     ]},
    {'type': 'num_big', 'x': 680, 'y': 120, 'w': 220, 'h': 80, 'num': '60min', 'label': '语法快览（三+四+五）', 'color': O, 'fs': 30},
    {'type': 'num_big', 'x': 680, 'y': 215, 'w': 220, 'h': 80, 'num': '30min', 'label': 'Skills 实战（重点）', 'color': ORG, 'fs': 30},
    {'type': 'num_big', 'x': 680, 'y': 310, 'w': 220, 'h': 80, 'num': '15min', 'label': '面向对象', 'color': ACC, 'fs': 30},
    {'type': 'tagline_bar', 'text': '语法是手段，Skills 是目的 —— 用实战反哺阅读能力', 'color': O},
]})

# ---- S4: 读代码三步法 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '本课的「读代码三步法」',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 90, 'item_h': 100, 'items': [
        {'num': '①', 'title': '大白话翻译',
         'sub': '看到一行代码 → 用大白话说清楚「它是干什么的」'},
        {'num': '②', 'title': '猜输出',
         'sub': '这段代码跑完会得到什么？心里先给个答案'},
        {'num': '③', 'title': '问 AI 验证',
         'sub': '复制给 AI：「这段代码输出什么？」—— 对照自己的猜测'},
    ]},
    {'type': 'tagline_bar', 'text': '三步法贯穿全课：每个语法点，都要「翻译 → 猜 → 验证」', 'color': ORG},
]})

# ---- S5: 环境准备 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '二、环境准备 · 三种跑 Python 的方式',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'cards_2x2', 'start_y': 80, 'items': [
        {'title': '方式A · VS Code（推荐）', 'color': O,
         'desc': '第1周已装 VS Code\n装「Python」扩展 → 新建 01.py\n点右上角 ▶ 运行'},
        {'title': '方式B · 在线环境', 'color': ORG,
         'desc': '免安装，急用时用\nonline-python.com\npythontutor.com（看逐步动画）'},
        {'title': '方式C · 官方 IDLE', 'color': ACC,
         'desc': '装 Python 时自带\n最简单的交互窗口\n适合快速试一行代码'},
        {'title': '本课怎么用', 'color': '#007F6E',
         'desc': '选一种即可，不纠结\n重点是「能跑起来」\n后面跟着敲、跟着读'},
    ]},
    {'type': 'tagline_bar', 'text': '环境只是工具，能跑就行 —— 选你最顺手的一种', 'color': O},
]})

# ---- S6: Hello World ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'Hello World + 注释',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 60, 'y': 80, 'w': 500, 'h': 180, 'fs': 15, 'title': '01.py',
     'code': r'''# 这是一行注释，人看、机器不看
print("Hello, World!")   # 输出到屏幕

name = "北航"            # 变量：起个名字装数据
print("你好", name)       # 逗号自动加空格

# print 三个用法
print("a", "b", "c")      # 输出：a b c
print("a", "b", "c", sep="-")  # 输出：a-b-c
print("换行", end="!")     # 结尾用 !，不换行''', },
    {'type': 'text', 'x': 590, 'y': 90, 'w': 320, 'h': 30, 'text': '# 是注释，解释给人看',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 590, 'y': 128, 'w': 320, 'h': 100,
     'text': '· 注释是「旁白」，机器直接跳过\n· print() = 把内容打印到屏幕\n· 变量 = 给数据起个名字，方便反复用\n· sep 改分隔符，end 改结尾',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 590, 'y': 250, 'w': 320, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 590, 'y': 270, 'w': 320, 'h': 60,
     'text': '试试：把 "Hello, World!"\n改成你的名字，再运行',
     'fs': 17, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '第一行代码的意义：确认环境能跑通，后面的代码才有意义', 'color': O},
]})

# ---- S7: 读报错 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '读报错 · 报错是朋友不是敌人',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 60, 'y': 80, 'w': 520, 'h': 180, 'fs': 14, 'title': '报错信息',
     'code': r'''Traceback (most recent call last):
  File "01.py", line 1, in <module>
    print(Hello)
NameError: name 'Hello' is not defined''', },
    {'type': 'text', 'x': 610, 'y': 90, 'w': 300, 'h': 30, 'text': '读报错只看两行',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 610, 'y': 128, 'w': 300, 'h': 120,
     'text': '① 最后一行：错误类型\n   NameError = 名字没定义\n\n② 带 ↑ 的那一行：\n   出错的具体位置',
     'fs': 17, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 610, 'y': 260, 'w': 300, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 610, 'y': 278, 'w': 300, 'h': 60,
     'text': '常见错误类型：\nNameError 未定义 / TypeError 类型错\nSyntaxError 语法错 / IndentationError 缩进错',
     'fs': 15, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '报错 = 机器在告诉你：改这里。先看最后一行，再看箭头指向', 'color': O},
]})

# ---- S8: 变量与类型 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '三、变量与类型 · 数据的四只「盒子」',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 210, 'fs': 15, 'title': 'types.py',
     'code': r'''age = 20            # int   整数
price = 19.9        # float 小数
name = "张三"       # str   字符串
is_student = True   # bool  真假

print(type(age))        # <class 'int'>
print(type(name))       # <class 'str'>

# 变量可重新赋值，类型也会变
age = "二十岁"          # 现在 age 变成 str''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': 'type() 看类型',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 150,
     'text': '· int：整数，如 20\n· float：小数，如 19.9\n· str：字符串，加引号\n· bool：只有 True / False\n\n变量 = 一个贴了标签的盒子\n标签能撕掉重贴（重新赋值）',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 290, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 308, 'w': 325, 'h': 50,
     'text': '记忆点：str 必须加引号\n数字才是不加引号的 20 / 19.9',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '四只盒子：int / float / str / bool —— 看到认识即可', 'color': O},
]})

# ---- S9: 类型转换与 f-string ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '类型转换 + f-string 拼接',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 200, 'fs': 15, 'title': 'convert.py',
     'code': r'''age = 20
# 数字不能直接和文字相加
# print("我" + age)   # 报错 TypeError

# 转换三兄弟：int() / float() / str()
text = "20"
num = int(text)          # 字符串 → 整数
print(num + 1)           # 21

# f-string：f 开头，{ } 里放变量
print(f"我今年{age}岁")   # 我今年20岁''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': '拼接推荐用 f-string',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 150,
     'text': '· int(x) 转整数\n· float(x) 转小数\n· str(x) 转字符串\n\nf-string 最常用：\nf"文字{变量}文字"\n花括号里的变量会自动替换',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 290, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 308, 'w': 325, 'h': 50,
     'text': '记：数字 + 文字 = 报错\n必须先 str() 或 f-string',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'f-string 是最高频的字符串写法，务必看熟', 'color': O},
]})

# ---- S10: 条件判断 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '条件判断 if / elif / else',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 220, 'fs': 15, 'title': 'if_demo.py',
     'code': r'''score = 85

if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 比较运算符
#  >  >=  <  <=  ==  !=
#  and(且)  or(或)  not(非)''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': '三个关键字',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 170,
     'text': '· if：如果（第一个条件）\n· elif：否则如果（可多个）\n· else：否则（兜底）\n\n== 是比较相等，= 是赋值\n千万别搞混\n\nand / or / not 组合多个条件',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 300, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 318, 'w': 325, 'h': 50,
     'text': '猜：score = 59 输出什么？\nscore = 90 输出什么？',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '条件块从 if 开始，依次判断，命中一个就停', 'color': O},
]})

# ---- S11: 缩进 + 实操1 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '缩进是 Python 的灵魂 + 实操1',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 480, 'h': 200, 'fs': 14, 'title': '缩进对比',
     'code': r'''if True:
    print("属于 if")     # 缩进 4 空格
print("不属于 if")       # 顶格，一定执行

# 错误示范（少了缩进会报错）
if True:
print("这行会报错 IndentationError")''', },
    {'type': 'text', 'x': 565, 'y': 90, 'w': 350, 'h': 30, 'text': '缩进 = 归属关系',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 565, 'y': 128, 'w': 350, 'h': 130,
     'text': '· 冒号 : 后面要另起一行并缩进\n· 缩进的代码「属于」上面的块\n· 同一块缩进必须对齐\n· 推荐统一用 4 个空格',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 565, 'y': 270, 'w': 350, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 565, 'y': 288, 'w': 350, 'h': 90,
     'text': '【实操1】写一个分数判断：\n输入 score，>60 输出「及格」\n否则输出「不及格」，用上 if/else',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '看到冒号 : 就想到「接下来要缩进」', 'color': O},
]})

# ---- S12: 列表 list ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '四、列表 list · 排队的盒子',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 230, 'fs': 15, 'title': 'list_demo.py',
     'code': r'''fruits = ["苹果", "香蕉", "橙子"]

print(fruits[0])      # 苹果（从 0 开始数）
print(fruits[-1])     # 橙子（-1 是最后一个）

fruits.append("葡萄")  # 往尾巴加一个
print(len(fruits))    # 4（长度）

# 切片：取一部分 [起点:终点]
print(fruits[0:2])    # ['苹果', '香蕉']''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': '下标从 0 开始',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 170,
     'text': '· 列表用 [ ] 包住，逗号分隔\n· 下标：0 是第一个，-1 是最后一个\n· append() 往尾巴添加\n· len() 看长度\n· 切片 [0:2] 取第0到第1个\n  （含头不含尾）',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 300, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 318, 'w': 325, 'h': 50,
     'text': '比喻：列表 = 有编号的抽屉\n每个抽屉能装任意数据',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '列表是数据「排好队」的容器，靠下标取值', 'color': O},
]})

# ---- S13: for 循环 + 列表推导式 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'for 循环 + 列表推导式',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 230, 'fs': 15, 'title': 'for_demo.py',
     'code': r'''fruits = ["苹果", "香蕉", "橙子"]

# for 循环：挨个拿、挨个处理
for f in fruits:
    print(f)          # 依次打印三个水果

# range()：生成一串数
for i in range(5):
    print(i)          # 0 1 2 3 4

# 列表推导式：一行生成新列表
nums = [x * 2 for x in range(5)]
print(nums)           # [0, 2, 4, 6, 8]''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': 'for = 循环处理',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 170,
     'text': '· for x in 列表：\n  逐个取出，缩进块里处理\n· range(n)：0 到 n-1 的数\n· 列表推导式：\n  [表达式 for x in 列表]\n  一行顶一个 for 循环',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 300, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 318, 'w': 325, 'h': 50,
     'text': 'AI 代码里 for + 推导式极常见\n看到能认出即可',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'for 循环 = 流水线：同一件事，对每个元素都做一遍', 'color': O},
]})

# ---- S14: 字典 dict ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '字典 dict · 带标签的盒子',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 230, 'fs': 15, 'title': 'dict_demo.py',
     'code': r'''student = {
    "name": "张三",
    "age": 20,
    "score": 85
}

print(student["name"])   # 张三（用键取值）

student["city"] = "北京"  # 新增一个键值对
print(student.keys())     # 所有键

# 用 get 更安全，键不存在不报错
print(student.get("sex", "未知"))  # 未知''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': '键值对 key: value',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 170,
     'text': '· 字典用 { } 包住\n· 每个元素是 键: 值\n· 靠「键」取值，不靠位置\n· 新增：dict["新键"] = 值\n· get() 取不到给默认值，更安全',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 300, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 318, 'w': 325, 'h': 50,
     'text': '比喻：字典 = 通讯录\n按「名字」找人，不按「排第几」',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'AI 里的配置、参数，几乎都用字典表示（JSON 同源）', 'color': O},
]})

# ---- S15: 组合拳 + 实操2 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '组合拳：遍历「字典列表」 + 实操2',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 510, 'h': 210, 'fs': 15, 'title': 'combo.py',
     'code': r'''students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 58},
]

# 列表里套字典，逐个取出处理
for s in students:
    name = s["name"]
    score = s["score"]
    if score >= 60:
        print(f"{name} 及格")
    else:
        print(f"{name} 不及格")''', },
    {'type': 'text', 'x': 590, 'y': 90, 'w': 320, 'h': 30, 'text': '最实用的组合',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 590, 'y': 128, 'w': 320, 'h': 150,
     'text': '列表 + 字典 + for + if\n是 AI 处理数据的「标准模板」\n\n看到 for s in xxx：\n心里默念「挨个处理每个元素」',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 590, 'y': 290, 'w': 320, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 590, 'y': 308, 'w': 320, 'h': 60,
     'text': '【实操2】把上面代码里\nprint 改成 f"姓名：{name}，成绩：{score}"',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '能读懂「列表套字典的 for 循环」，就能读懂一半 AI 代码', 'color': O},
]})

# ---- S16: 函数 def ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '五、函数 def · 打包一段操作',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 500, 'h': 230, 'fs': 15, 'title': 'func_demo.py',
     'code': r'''# 定义：def 函数名(参数):
def greet(name):
    """这个函数用来打招呼"""
    return f"你好，{name}"

# 调用
msg = greet("张三")
print(msg)            # 你好，张三

# 多个参数 + 默认值
def add(a, b=10):
    return a + b

print(add(3))         # 13（b 用默认值 10）
print(add(3, 5))      # 8''', },
    {'type': 'text', 'x': 585, 'y': 90, 'w': 325, 'h': 30, 'text': 'def + return',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 585, 'y': 128, 'w': 325, 'h': 170,
     'text': '· def 定义函数，之后反复调用\n· 参数 = 传给函数的「输入」\n· return = 把结果「交回去」\n· 默认值：调用时不传就用它\n· 三引号 """ 是函数说明（docstring）',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 585, 'y': 300, 'w': 325, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 585, 'y': 318, 'w': 325, 'h': 50,
     'text': '看到 def：把这段代码当成\n一个「有名字的黑盒子」',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '函数 = 可复用的积木，看懂输入输出即可，不必抠内部', 'color': O},
]})

# ---- S17: 参数花样 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '参数的花样 · *args 与 **kwargs',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 230, 'fs': 15, 'title': 'args_kwargs.py',
     'code': r'''def demo(a, *args, **kwargs):
    print("a =", a)
    print("args =", args)      # 多余的位置参数
    print("kwargs =", kwargs)  # 多余的键值参数

demo(1, 2, 3, name="张三", age=20)
# a = 1
# args = (2, 3)
# kwargs = {'name': '张三', 'age': 20}''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': '看到 * 和 ** 别慌',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 170,
     'text': '· *args：\n  装多余的位置参数 → 元组\n· **kwargs：\n  装多余的键值参数 → 字典\n\nAI 框架里到处是 **kwargs\n只要知道「在收一堆参数」即可',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 300, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 318, 'w': 310, 'h': 50,
     'text': '不用背写法，看到能认出\n「这是在收集灵活参数」就够了',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '*args / **kwargs = 灵活参数的口袋，看懂即可', 'color': O},
]})

# ---- S18: 模块 import ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '模块 import · 搬别人写好的代码',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 480, 'h': 200, 'fs': 15, 'title': 'import_demo.py',
     'code': r'''import math

print(math.sqrt(16))   # 4.0（开平方）

from math import pi
print(pi)              # 3.14159...

import json
data = '{"name": "张三"}'
obj = json.loads(data)  # 字符串 → 字典
print(obj["name"])      # 张三''', },
    {'type': 'text', 'x': 565, 'y': 90, 'w': 350, 'h': 30, 'text': '两种导入方式',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 565, 'y': 128, 'w': 350, 'h': 130,
     'text': '· import 模块：\n  用 模块.函数 调用\n· from 模块 import 名字：\n  直接调用\n\njson 模块超常用：\nloads() 字符串→对象\ndumps() 对象→字符串',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 565, 'y': 270, 'w': 350, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 565, 'y': 288, 'w': 350, 'h': 60,
     'text': '常用库速记：\nos 文件系统 / sys 系统 / json 数据\ntime 时间 / requests 网络',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'import = 借用别人造好的轮子，不用自己重写', 'color': O},
]})

# ---- S19: pip 安装 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'pip 安装第三方库',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 170, 'fs': 15, 'title': '终端命令',
     'code': r'''# 安装（在终端里敲，不是 .py 里）
pip install requests

# 指定版本
pip install requests==2.31.0

# 查看已安装
pip list

# 卸载
pip uninstall requests''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': 'pip = 装库的工具',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 150,
     'text': '· 标准库：自带，import 就能用\n· 第三方库：先 pip install 再 import\n· 装在「终端」里，不是代码里\n\nVS Code 里：\n菜单 终端 → 新建终端 → 敲命令',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 290, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 308, 'w': 310, 'h': 50,
     'text': '报错 ModuleNotFoundError？\n= 没装这个库，先 pip install',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '缺啥装啥：看到 ModuleNotFoundError 就去 pip install', 'color': O},
]})

# ---- S20: 为什么认识类 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '六、面向对象 · 为什么要认识「类」',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 90, 'w': 420, 'h': 34, 'text': '现实世界 → 代码世界',
     'fs': 24, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 130, 'w': 420, 'h': 120,
     'text': '· 类 class = 设计图 / 模板\n· 对象 = 按图造出来的具体东西\n· 属性 = 它的数据（姓名、年龄）\n· 方法 = 它能做的事（自我介绍）',
     'fs': 18, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'shape', 'shape': 'rect', 'x': 60, 'y': 265, 'w': 420, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 285, 'w': 420, 'h': 80,
     'text': '为什么必须认识类？\n因为 LangChain / CrewAI 的\nAgent、Tool 都是「类」写出来的',
     'fs': 18, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'code', 'x': 520, 'y': 90, 'w': 400, 'h': 210, 'fs': 15, 'title': '类的最简示例',
     'code': r'''class Dog:
    def __init__(self, name):
        self.name = name       # 属性

    def bark(self):            # 方法
        print(f"{self.name}：汪汪！")

d = Dog("旺财")   # 造出一个对象
d.bark()          # 旺财：汪汪！'''},
    {'type': 'text', 'x': 520, 'y': 310, 'w': 400, 'h': 80,
     'text': 'class Dog 是「模板」\nd = Dog("旺财") 是「造出一只狗」\nself 代表「当前这个对象自己」',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
]})

# ---- S21: 类的标准长相 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '类的标准长相 · 四看',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 240, 'fs': 15, 'title': 'book_class.py',
     'code': r'''class Book:
    def __init__(self, title, author):
        self.title = title    # ① 属性
        self.author = author

    def info(self):           # ② 方法
        return f"{self.title} by {self.author}"

b = Book("三体", "刘慈欣")
print(b.info())   # 三体 by 刘慈欣''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': '看类就找这四样',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 180,
     'text': '① __init__：初始化函数\n   造对象时自动跑\n② self.xxx：属性（数据）\n③ def 方法：能做的事\n④ 类名(参数)：造对象\n\n看到 __init__ 就想到：\n「这是对象的出厂设置」',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 310, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 328, 'w': 310, 'h': 50,
     'text': '双下划线 __init__ 是特殊方法\n不是写错了，别怕',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '读类四看：__init__ / self 属性 / 方法 / 类名()', 'color': O},
]})

# ---- S22: 继承 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '继承 · 子类复用父类',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 220, 'fs': 15, 'title': 'inherit.py',
     'code': r'''class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(f"{self.name} 在叫")

# 子类继承父类：class 子类(父类)
class Dog(Animal):
    def speak(self):        # 覆盖父类方法
        print(f"{self.name}：汪汪！")

d = Dog("旺财")
d.speak()   # 旺财：汪汪！''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': 'class 子类(父类)',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 170,
     'text': '· 继承 = 儿子继承老子的家产\n· 子类自动拥有父类的方法\n· 覆盖：子类重写同名方法\n· 扩展：加自己独有功能\n\n看到 class X(Y)：\nX 是 Y 的一种特殊版本',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 300, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 318, 'w': 310, 'h': 50,
     'text': 'AI 框架常见：自定义 Tool 类\n继承框架的 BaseTool',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '继承 = 复用父类 + 按需改造', 'color': O},
]})

# ---- S23: 装饰器 + 类型注解 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '装饰器 @ 与类型注解',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 220, 'fs': 15, 'title': 'decorator.py',
     'code': r'''# 装饰器：给函数「套一层壳」
def log(func):
    def wrapper(*args, **kwargs):
        print("开始调用")
        return func(*args, **kwargs)
    return wrapper

@log
def hello(name):
    print(f"你好 {name}")

hello("张三")   # 先打印"开始调用"再"你好 张三"''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': '@ 开头 = 装饰器',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 130,
     'text': '· @xxx 在函数上面 = 给函数加功能\n· 看不懂没关系，先知道「在装饰」\n\n类型注解（新版常见）：\ndef add(a: int, b: int) -> int:\n   a: int 表示 a 是整数\n   -> int 表示返回整数',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 270, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 288, 'w': 310, 'h': 80,
     'text': '看到 -> 别当成箭头\n是「函数返回什么类型」\n类型注解只是提示，不强制',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'tagline_bar', 'text': '@ 装饰器 = 加壳；-> int = 返回类型提示', 'color': O},
]})

# ---- S24: 实操3 读 Book 类 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '【实操3】读一段类代码，答三问',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 250, 'fs': 15, 'title': 'quiz.py',
     'code': r'''class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_pass(self):
        return self.score >= 60

    def level(self):
        if self.score >= 90:
            return "优秀"
        elif self.score >= 60:
            return "及格"
        return "不及格"

s = Student("小明", 75)
print(s.is_pass())   # ?
print(s.level())     # ?''', },
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': '三个问题',
     'fs': 22, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 150,
     'text': 'Q1：这个类叫什么？\nQ2：有哪些属性和方法？\nQ3：s.is_pass() 和 s.level()\n   分别输出什么？',
     'fs': 18, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 290, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 308, 'w': 310, 'h': 80,
     'text': '答案：\nQ3 → is_pass() 输出 True\n    level() 输出「及格」',
     'fs': 17, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'tagline_bar', 'text': '能答出这三问，读类能力就达标了', 'color': O},
]})

# ---- S25: Skills 是什么回顾 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '七、Skills 开发实战 · 先回顾 Skills 是什么',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 80, 'w': 520, 'h': 250, 'fs': 14, 'title': 'Skills 的结构',
     'code': r'''Skills（技能包）= 给 AI 的"岗位说明书"包
├── SKILL.md  ← 说明书：教 AI 怎么完成一类任务
└── (可选) 辅助文件：脚本、模板、数据

放哪里？
  项目级：.claude/skills/<技能名>/SKILL.md
         （跟着项目走，推荐先用这个）
  个人级：~/.claude/skills/<技能名>/SKILL.md
         （所有项目都能用）
  CodeBuddy 对应：.codebuddy/skills/ 或
         ~/.codebuddy/skills/'''},
    {'type': 'text', 'x': 605, 'y': 90, 'w': 310, 'h': 30, 'text': '一句话记住',
     'fs': 22, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 605, 'y': 128, 'w': 310, 'h': 170,
     'text': 'SKILL.md 是「说明书」\n告诉 AI：\n· 什么时候用我\n· 怎么一步步干活\n· 输出成什么样子\n\n辅助脚本 = 真正干活的工具\n让 AI 不只是动嘴',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 605, 'y': 300, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 605, 'y': 318, 'w': 310, 'h': 60,
     'text': '本课实战：\n亲手写一个 python-code-reader\n技能包（30 分钟）',
     'fs': 17, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'Skills = SKILL.md 说明书 + 可选辅助脚本', 'color': ORG},
]})

# ---- S26: 实战任务介绍 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '实战任务：做一个「Python 代码讲解助手」',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 80, 'w': 500, 'h': 60,
     'text': '任务目标\n做一个叫 python-code-reader 的 Skill，\n让 AI 用大白话讲清任意 Python 代码。',
     'fs': 19, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'text', 'x': 60, 'y': 160, 'w': 840, 'h': 30, 'text': '四个步骤 · 总共约 30 分钟',
     'fs': 24, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 200, 'item_h': 56, 'items': [
        {'num': '1', 'title': '创建目录（1 分钟）',
         'sub': '建 .claude/skills/python-code-reader/ 文件夹'},
        {'num': '2', 'title': '写 SKILL.md（15 分钟）',
         'sub': '写 description + 5 步执行流程 + 示例对话'},
        {'num': '3', 'title': '写 analyze.py 辅助脚本（5 分钟）',
         'sub': '用今天学的语法，统计代码行数/函数数/类数'},
        {'num': '4', 'title': '测试 Skill（4 分钟）',
         'sub': '粘贴代码让 AI 讲，看是否触发技能'},
    ]},
    {'type': 'tagline_bar', 'text': '今天学的所有语法，都会在写这个 Skill 时用上', 'color': ORG},
]})

# ---- S27: 步骤1+2 目录与 frontmatter ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '步骤1+2 · 建目录 & 写 SKILL.md 头部',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 55, 'y': 76, 'w': 450, 'h': 26, 'text': '① 在项目文件夹里创建：',
     'fs': 18, 'color': D, 'bold': True, 'align': 1, 'font': FB},
    {'type': 'code', 'x': 55, 'y': 104, 'w': 450, 'h': 90, 'fs': 14, 'title': '目录结构',
     'code': r'''.claude/skills/python-code-reader/SKILL.md'''},
    {'type': 'text', 'x': 55, 'y': 208, 'w': 450, 'h': 80,
     'text': '② SKILL.md 开头要有 frontmatter：\n--- 包裹的 name 和 description\nname：技能名\ndescription：什么场景下触发',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 55, 'y': 300, 'w': 450, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 55, 'y': 318, 'w': 450, 'h': 70,
     'text': '黄金法则：description 写清「什么时候用」\nAI 才会自动触发这个技能',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'code', 'x': 520, 'y': 80, 'w': 400, 'h': 250, 'fs': 13, 'title': 'SKILL.md（头部）',
     'code': r'''---
name: python-code-reader
description: 用大白话讲解 Python 代码。
  当用户粘贴 Python 代码、问
  "这段代码干什么/怎么运行/
  哪里看不懂"时使用。
---

# Python 代码讲解助手

## 你负责的任务
把用户给的 Python 代码，按固定流程讲
清楚，目标是让零基础的人听懂。'''},
    {'type': 'tagline_bar', 'text': 'frontmatter 的 description 决定 AI 会不会主动用这个技能', 'color': ORG},
]})

# ---- S28: SKILL.md 执行步骤 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'SKILL.md 核心 · 五步执行流程',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 78, 'w': 500, 'h': 280, 'fs': 13, 'title': '执行步骤（必须按顺序）',
     'code': r'''### 第1步：一句话概括
用不超过 30 个字，说明整体在干什么。
示例："这段代码统计学生成绩，输出及格名单。"

### 第2步：拆块讲解
每块用：
- 【代码】贴出原代码
- 【干什么】大白话解释
- 【关键词】标注语法点（变量/列表/字典/
  函数/类/装饰器等），每个一句话解释

### 第3步：数据流
用箭头说明数据从哪来、怎么处理、到哪去。
示例：输入名单 → for循环判断 → 及格者加入
新列表 → 打印

### 第4步：猜输出
写出："这段代码运行后会输出：..." 并给结果。

### 第5步：常见坑
1-2 句提示新手易错处（索引从0开始、
==才是判断相等、缩进错误等）。'''},
    {'type': 'code', 'x': 570, 'y': 78, 'w': 345, 'h': 280, 'fs': 13, 'title': '示例对话',
     'code': r'''用户：
def add(a, b): return a + b

助手：
- 【干什么】定义一个加法函数：
  输入两个数，返回它们的和
- 【关键词】def=定义函数；
  return=返回结果
- 【数据流】a、b → 相加 → 返回给调用者
- 【猜输出】print(add(3, 4)) → 7'''},
    {'type': 'text', 'x': 55, 'y': 372, 'w': 850, 'h': 60,
     'text': '要点：执行步骤写清「先做什么后做什么」，示例对话给 AI 打样 —— 有章法 + 有样例，AI 才能稳定输出',
     'fs': 17, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'description 管「触发」，执行步骤管「章法」，示例对话管「打样」', 'color': ORG},
]})

# ---- S29: analyze.py 辅助脚本 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '步骤3 · 写 analyze.py 辅助脚本（加分项）',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'code', 'x': 55, 'y': 76, 'w': 520, 'h': 330, 'fs': 13, 'title': '.claude/skills/python-code-reader/analyze.py',
     'code': r'''# analyze.py —— 统计一段 Python 代码的基本信息
import sys

def analyze(code):
    lines = code.split("\n")
    non_empty = [l for l in lines if l.strip()]   # 去掉空行
    funcs = [l for l in non_empty
             if l.strip().startswith("def ")]
    classes = [l for l in non_empty
               if l.strip().startswith("class ")]

    print("代码总行数:", len(lines))
    print("非空行数:", len(non_empty))
    print("函数数量:", len(funcs))
    print("类数量:", len(classes))
    for f in funcs:
        print("  函数:", f.strip().split("(")[0]
              .replace("def ", ""))

if __name__ == "__main__":
    code = sys.stdin.read()   # 读取传入的代码
    analyze(code)'''},
    {'type': 'text', 'x': 600, 'y': 90, 'w': 310, 'h': 30, 'text': '今天学的语法全用上了',
     'fs': 22, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 310, 'h': 190,
     'text': '· import sys：导入标准库\n· def analyze()：函数\n· code.split()：字符串切分\n· 列表推导式：过滤空行\n· startswith()：判断开头\n· if __name__：入口判断\n\n这段代码 = 本课知识的浓缩',
     'fs': 16, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 600, 'y': 320, 'w': 310, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 600, 'y': 338, 'w': 310, 'h': 60,
     'text': '写进 SKILL.md 执行步骤：\n「先运行 analyze.py 传代码，\n把统计结果当讲解开头」',
     'fs': 16, 'color': ORG, 'bold': True, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': '辅助脚本让 Skill 真的「会干活」，而不只是让 AI 动嘴', 'color': ORG},
]})

# ---- S30: 步骤4 测试 + 验收标准 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '步骤4 测试 + 验收标准',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 55, 'y': 80, 'w': 460, 'h': 30, 'text': '测试 Skill（4 分钟）',
     'fs': 24, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 55, 'y': 120, 'w': 460, 'h': 200,
     'text': '① 写一段今天练习的代码\n② 对 AI 说「帮我看看这段代码\n   是干什么的」+ 粘贴代码\n③ AI 用了 python-code-reader 的\n   格式讲解 → 成功！\n④ 没触发？检查 description 是否\n   写清场景，或手动指定技能',
     'fs': 17, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'text', 'x': 545, 'y': 80, 'w': 380, 'h': 30, 'text': '验收标准（都满足 = 完成）',
     'fs': 24, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'code', 'x': 545, 'y': 120, 'w': 380, 'h': 220, 'fs': 14, 'title': 'checklist',
     'code': r'''✅ SKILL.md 放在
   .claude/skills/python-code-reader/ 下
✅ description 清楚说明"什么场景用"
✅ 执行步骤 >= 4 步，且包含"猜输出"
✅ 有一个示例对话
✅ （加分）analyze.py 能运行并输出统计'''},
    {'type': 'tagline_bar', 'text': '做完即验收：五条全勾，技能包就立起来了', 'color': ORG},
]})

# ---- S31: 三条心法 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'Skills 开发的三条心法',
     'fs': 40, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 95, 'item_h': 110, 'items': [
        {'num': '①', 'title': '从自己的痛点出发',
         'sub': '你最常让 AI 干什么？把它做成 Skill。自己用得上，才写得动'},
        {'num': '②', 'title': 'description 是灵魂',
         'sub': '写不清「什么时候用」，AI 就不会主动用 —— 触发全靠它'},
        {'num': '③', 'title': '先小后大',
         'sub': '先做一个 10 行的 Skill，跑通流程，再慢慢加功能'},
    ]},
    {'type': 'text', 'x': 60, 'y': 445, 'w': 840, 'h': 40,
     'text': '本堂的 Skill 是「样板」：课后为自己最常用的一件事各写一个（读论文 / 写周报 / 改简历）',
     'fs': 17, 'color': ORG, 'bold': True, 'align': 2, 'font': FB},
    {'type': 'tagline_bar', 'text': '先跑通，再优化 —— 别在第一步就追求完美', 'color': ORG},
]})

# ---- S32: 知识地图 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '八、本课知识地图 · 一张图记住',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 85, 'item_h': 80, 'items': [
        {'num': '词', 'title': '词汇表',
         'sub': '变量 = 存数据；列表 = 排队；字典 = 名片夹'},
        {'num': '流', 'title': '流程',
         'sub': '条件 if/else（做选择）；循环 for（逐个处理）'},
        {'num': '木', 'title': '积木',
         'sub': '函数 def（封装逻辑）；import（用现成库）'},
        {'num': '骨', 'title': '骨架',
         'sub': '类 class（图纸）+ self + __init__ + 继承 + @装饰器'},
        {'num': '武', 'title': '武器',
         'sub': 'Skills：把「读代码三步法」做成 AI 技能包'},
    ]},
    {'type': 'tagline_bar', 'text': '读代码所需的一切 = 词汇 + 流程 + 积木 + 骨架 + 武器', 'color': O},
]})

# ---- S33: 课后作业 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': '课后作业',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 90, 'item_h': 115, 'items': [
        {'num': '1', 'title': '读代码练习',
         'sub': '把本课 4 个实操代码，每段用「三步法」（翻译 → 猜输出 → 验证）过一遍'},
        {'num': '2', 'title': 'Skills 实战（核心作业）',
         'sub': '完善 python-code-reader，再仿照它写 1 个新 Skill（论文阅读/周报/简历），含 description + 至少 3 步'},
        {'num': '3', 'title': '预习',
         'sub': 'GitHub 搜 flask / fastapi 小项目，找一段真实代码，下节课带来 —— 课3 要用它实战阅读'},
    ]},
    {'type': 'tagline_bar', 'text': '作业2 是重点：从「会用」到「会造」的第一次跨越', 'color': O},
]})

# ---- S34: FAQ ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38, 'text': 'FAQ · 常见疑问',
     'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 55, 'y': 76, 'w': 420, 'h': 210,
     'text': 'Q1 两小时语法会不会太少？\n不会，目标是「读懂」不是「熟练写」，\n2 小时已覆盖 90% 读代码需求。\n\nQ2 连 self 都没完全懂能继续吗？\n能，记住 self =「对象自己」即可，\n剩下的读项目时自然就懂。\n\nQ3 和第1周 Skills 有啥区别？\n第1周「会用现成」；本课「第一次自己写」。',
     'fs': 15, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'text', 'x': 500, 'y': 76, 'w': 420, 'h': 210,
     'text': 'Q4 为什么 3 堂语法压成 1 堂？\n因为目标是「读懂」，细节放项目里\n「遇到再学」—— 项目是最好的老师。\n\nQ5 写 analyze.py 卡住怎么办？\n① 对照 7.2 步骤3 抄一遍\n② 看不懂的复制给 AI 解释\n③ 报错了把报错发给 AI\n这不是作弊，是这门课的核心工作方式。',
     'fs': 15, 'color': D, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'tagline_bar', 'text': '卡住就问 AI —— 这正是本课要训练的核心能力', 'color': O},
]})

# ---- S35: 致谢 + 下节预告 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 8, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 532, 'w': 960, 'h': 8, 'color': O},
    {'type': 'text', 'x': 60, 'y': 100, 'w': 840, 'h': 60, 'text': '读懂 · 会问 · 能开发',
     'fs': 46, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'shape', 'shape': 'rect', 'x': 360, 'y': 180, 'w': 240, 'h': 3, 'color': ORG},
    {'type': 'text', 'x': 60, 'y': 205, 'w': 840, 'h': 80,
     'text': '今天：认了 Python 的词汇、流程、积木、骨架\n亲手造出第一个 Skills 技能包',
     'fs': 22, 'color': D, 'bold': False, 'align': 2, 'font': FB, 'line_spacing': 1.6},
    {'type': 'text', 'x': 60, 'y': 320, 'w': 840, 'h': 30, 'text': '下节预告',
     'fs': 26, 'color': ORG, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 360, 'w': 840, 'h': 60,
     'text': '课2 · Python 数据分析：读代码 + 处理表格数据\nNumPy / Pandas / Matplotlib —— 第3周机器学习的直接基础',
     'fs': 18, 'color': D, 'bold': False, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 60, 'y': 455, 'w': 840, 'h': 30,
     'text': '课后把「读代码三步法」变成肌肉记忆，我们下节课见',
     'fs': 16, 'color': G, 'bold': False, 'align': 2, 'font': FB},
]})

# ====== SLIDES_END ======

def build():
    pythoncom.CoInitialize()
    app = win32com.client.Dispatch('KWPP.Application')
    try:
        app.Visible = False
    except:
        pass
    try:
        app.DisplayAlerts = False
    except:
        pass
    try:
        pres = app.Presentations.Add()
        pres.PageSetup.SlideWidth = 960
        pres.PageSetup.SlideHeight = 540
        while pres.Slides.Count > 0:
            pres.Slides.Item(1).Delete()
        for i, sd in enumerate(slides, 1):
            slide = pres.Slides.Add(i, 12)  # 12 = 空白版式
            s = slide.Shapes
            for e in sd.get('elements', []):
                fn = ROUTERS.get(e['type'])
                if fn:
                    fn(s, e)
        pptx = os.path.join(OUT, '课1-Python基础与Skills开发实战.pptx')
        pres.SaveAs(pptx)
        pdf = os.path.join(OUT, '课1-Python基础与Skills开发实战.pdf')
        pdf_ok = False
        try:
            pres.SaveAs(pdf, 32)  # 32 = ppSaveAsPDF
            pdf_ok = os.path.exists(pdf)
        except Exception as ex:
            print('SaveAs PDF 失败:', ex)
        if not pdf_ok:
            try:
                pres.ExportAsFixedFormat(pdf, 1)
                pdf_ok = os.path.exists(pdf)
            except Exception as ex:
                print('ExportAsFixedFormat PDF 失败:', ex)
        pres.Close()
        print('SAVED:', pptx)
        print('SAVED PDF:', pdf, pdf_ok)
    finally:
        try:
            app.Quit()
        except:
            pass

if __name__ == '__main__':
    build()

