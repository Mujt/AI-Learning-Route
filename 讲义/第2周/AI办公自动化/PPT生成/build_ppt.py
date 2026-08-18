# -*- coding: utf-8 -*-
"""AI办公自动化课程 - 技术展示PPT构建引擎（WPS COM 自动化）

遵循 harness-anything 官方工作流：JSON数据驱动 + WPS COM 构建。
画布：960 × 540 pt（16:9）
"""
import os, pythoncom, win32com.client

# ====== 配置 ======
OUT = os.path.dirname(os.path.abspath(__file__))
FT = 'SimHei'           # 标题字体
FB = 'Microsoft YaHei'  # 正文字体
O = '#004098'           # 品牌色（科技蓝）
B = '#000000'           # 辅色黑
D = '#333333'           # 正文黑
G = '#666666'           # 辅助灰
ACC = '#00A0E9'         # 亮蓝（强调）
ORG = '#F28C28'         # 橙色（强调）

def h2b(h):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b << 16) | (g << 8) | r

# ====== 基础形状函数 ======

def rect(s, x, y, w, h, color):
    r = s.Shapes.AddShape(1, x, y, w, h)
    r.Fill.ForeColor.RGB = color
    r.Fill.Visible = True
    r.Line.Visible = False
    return r

def circle(s, x, y, w, h, color):
    c = s.Shapes.AddShape(9, x, y, w, h)
    c.Fill.ForeColor.RGB = color
    c.Fill.Visible = True
    c.Line.Visible = False
    return c

def txt(s, x, y, w, h, text, fs=24, color=0x333333, bold=False,
        align=1, font=FB, spacing=1.3):
    t = s.Shapes.AddTextbox(1, x, y, w, h)
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

# ====== 元素路由器 ======

def draw_text(s, e):
    c = h2b(e.get('color', D))
    return txt(s, e['x'], e['y'], e['w'], e['h'], e['text'],
               fs=e.get('fs', 24), color=c,
               bold=e.get('bold', False),
               align=e.get('align', 1),
               font=e.get('font', FB),
               spacing=e.get('line_spacing', 1.3))

def draw_image(s, e):
    p = os.path.join(OUT, e['file'])
    if os.path.exists(p):
        s.Shapes.AddPicture(p, False, True, e['x'], e['y'], e['w'], e['h'])

def draw_shape(s, e):
    st = e.get('shape', 'rect')
    x, y, w = e['x'], e['y'], e['w']
    h = e.get('h', e.get('w', 10))
    c = h2b(e.get('color', O))
    if st == 'circle':
        circle(s, x, y, w, h, c)
    else:
        rect(s, x, y, w, h, c)

def draw_table(s, e):
    rows = e['rows']
    cols = e['cols']
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    dta = e['data']
    hdr_color = h2b(e.get('header_color', O))
    min_rh = 28
    row_h = max(h // rows, min_rh)
    col_w = w // cols
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + c * col_w, y + r * row_h
            val = dta[r][c] if r < len(dta) and c < len(dta[r]) else ''
            is_hdr = (r == 0)
            bg_c = hdr_color if is_hdr else (
                0xFFFFFF if r % 2 == 0 else h2b('#F0F4FA'))
            fs = e.get('th_fs', 13) if is_hdr else e.get('td_fs', 14)
            tc = 0xFFFFFF if is_hdr else 0x333333
            al = 2 if c > 0 else 1
            rect(s, cx, cy, col_w, row_h, bg_c)
            if val:
                tb = s.Shapes.AddTextbox(1, cx + 3, cy + 2, col_w - 6, row_h - 4)
                tr = tb.TextFrame.TextRange
                tr.Text = str(val)
                tr.Font.Size = fs
                tr.Font.Color = tc
                tr.Font.Name = FT if is_hdr else FB
                tr.Font.Bold = is_hdr
                tr.ParagraphFormat.Alignment = al
                tb.TextFrame.WordWrap = False

def draw_card_list_wide(s, e):
    items = e['items']
    sy = e.get('start_y', 90)
    ih = e.get('item_h', 52)
    hex_colors = [O, ORG, ACC, O, ORG, ACC, O, ORG]
    for i, item in enumerate(items):
        y = sy + i * ih
        col = h2b(hex_colors[i % len(hex_colors)])
        circle(s, 100, y + 4, 34, 34, col)
        t2 = s.Shapes.AddTextbox(1, 100, y + 4, 34, 34)
        tr2 = t2.TextFrame.TextRange
        tr2.Text = item['num']
        tr2.Font.Size = 14
        tr2.Font.Color = 0xFFFFFF
        tr2.Font.Name = FT
        tr2.Font.Bold = True
        tr2.ParagraphFormat.Alignment = 2
        txt(s, 150, y + 2, 300, 30, item['title'],
            fs=24, color=h2b('#1A1A1A'), bold=True, font=FT)
        txt(s, 150, y + 34, 700, 18, item['sub'],
            fs=16, color=h2b('#555555'), bold=False, font=FB)

def draw_tagline_bar(s, e):
    rect(s, 30, 498, 900, 28, h2b(e.get('color', O)))
    txt(s, 40, 501, 880, 22, e['text'],
        fs=14, color=0xFFFFFF, bold=True, align=2, font=FB)

def draw_num_big(s, e):
    c = h2b(e.get('color', O))
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    num_h = int(h * 0.40)
    gap = int(h * 0.10)
    lbl_h = int(h * 0.50)
    t1 = s.Shapes.AddTextbox(1, x, y, w, num_h)
    tr1 = t1.TextFrame.TextRange
    tr1.Text = e['num']
    tr1.Font.Size = e.get('fs', 34)
    tr1.Font.Color = c
    tr1.Font.Name = 'Arial'
    tr1.Font.Bold = True
    tr1.ParagraphFormat.Alignment = 2
    t2 = s.Shapes.AddTextbox(1, x, y + num_h + gap, w, lbl_h)
    tr2 = t2.TextFrame.TextRange
    tr2.Text = e['label']
    tr2.Font.Size = 14
    tr2.Font.Color = h2b(G)
    tr2.Font.Name = FB
    tr2.ParagraphFormat.Alignment = 2

def draw_cards_2x3(s, e):
    items = e['items']; sy = e.get('start_y', 80); cw, ch = 295, 145; gx, gy = 15, 14
    for i, item in enumerate(items):
        r, c = i // 3, i % 3
        x = 22 + c * (cw + gx)
        y = sy + r * (ch + gy)
        col = h2b(item['color'])
        rect(s, x, y, cw, 5, col)
        txt(s, x + 12, y + 16, cw - 24, 32, item['title'],
            fs=22, color=col, bold=True, align=1, font=FT)
        txt(s, x + 12, y + 56, cw - 24, ch - 62, item['desc'],
            fs=15, color=h2b('#333333'), bold=False, align=1, font=FB, spacing=1.35)

def draw_cards_2x2(s, e):
    items = e['items']; sy = e.get('start_y', 80); cw, ch = 405, 190; gx, gy = 25, 25
    for i, item in enumerate(items):
        r, c = i // 2, i % 2
        x = 45 + c * (cw + gx)
        y = sy + r * (ch + gy)
        col = h2b(item['color'])
        rect(s, x, y, cw, 5, col)
        txt(s, x + 18, y + 16, cw - 36, 32, item['title'],
            fs=24, color=col, bold=True, align=1, font=FT)
        txt(s, x + 18, y + 58, cw - 36, ch - 68, item['desc'],
            fs=16, color=h2b('#333333'), bold=False, align=1, font=FB, spacing=1.4)

# ====== 路由表 ======
ROUTERS = {
    'text': draw_text,
    'image': draw_image,
    'shape': draw_shape,
    'table': draw_table,
    'card_list_wide': draw_card_list_wide,
    'tagline_bar': draw_tagline_bar,
    'num_big': draw_num_big,
    'cards_2x3': draw_cards_2x3,
    'cards_2x2': draw_cards_2x2,
}

# ====== 幻灯片数据 ======
slides = []

# ---- S1: 封面 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 8, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 532, 'w': 960, 'h': 8, 'color': O},
    {'type': 'text', 'x': 60, 'y': 60, 'w': 840, 'h': 52,
     'text': 'AI 办公自动化', 'fs': 52, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 124, 'w': 840, 'h': 30,
     'text': '第1周 · 第3课 · 技术展示', 'fs': 22, 'color': D, 'bold': False, 'align': 2, 'font': FB},
    {'type': 'shape', 'shape': 'rect', 'x': 380, 'y': 176, 'w': 200, 'h': 3, 'color': ORG},
    {'type': 'num_big', 'x': 120, 'y': 220, 'w': 220, 'h': 90,
     'num': '10', 'label': '知识块', 'color': O, 'fs': 44},
    {'type': 'num_big', 'x': 370, 'y': 220, 'w': 220, 'h': 90,
     'num': '200', 'label': '分钟课时', 'color': ORG, 'fs': 44},
    {'type': 'num_big', 'x': 620, 'y': 220, 'w': 220, 'h': 90,
     'num': '50%', 'label': '动手实操', 'color': ACC, 'fs': 44},
    {'type': 'text', 'x': 60, 'y': 350, 'w': 840, 'h': 60,
     'text': '三层进阶：从「用 AI 办公」到「亲手开发 AI 工具」\n对话式办公 → 自动化产出 → 开发者之路',
     'fs': 20, 'color': D, 'bold': True, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 60, 'y': 460, 'w': 840, 'h': 30,
     'text': '文档 · 数据 · 演示 · 阅读 · 自动化 · Skills · MCP',
     'fs': 16, 'color': G, 'bold': False, 'align': 2, 'font': FB},
]})


# ---- S2: 目录 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 16, 'w': 840, 'h': 40,
     'text': '目  录', 'fs': 42, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 95, 'item_h': 100, 'items': [
        {'num': '01', 'title': '对话式办公',
         'sub': 'Word 文档撰写 · Excel 数据处理 · PPT 演示文稿 · PDF 文献阅读'},
        {'num': '02', 'title': '自动化产出',
         'sub': '一键生成 PPT · 一键生成图表'},
        {'num': '03', 'title': '开发者之路',
         'sub': 'Skills 技能包开发 · MCP 连接器开发'},
    ]},
    {'type': 'tagline_bar', 'text': '从「让 AI 替你干活」到「让 AI 生态替你干活」 · 三层进阶 全程实战'},
]})


# ---- S3: 课程全景 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '课程全景 · 十个知识块', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'table', 'x': 45, 'y': 90, 'w': 620, 'h': 385, 'rows': 7, 'cols': 3,
     'header_color': O, 'th_fs': 14, 'td_fs': 14,
     'data': [
         ['知识块', '主题', '类型'],
         ['KB1', '课程导入与全景', '认知'],
         ['KB2-3', 'Word 文档 / Excel 数据', '实操'],
         ['KB4-5', 'PPT 演示 / PDF 阅读', '实操'],
         ['KB6-7', '自动化生成 PPT / 图表', '自动化'],
         ['KB8-9', 'Skills / MCP 开发', '开发者'],
         ['KB10', '课程总结与作业', '总结'],
     ]},
    {'type': 'num_big', 'x': 700, 'y': 105, 'w': 220, 'h': 80,
     'num': '200min', 'label': '总课时', 'color': O, 'fs': 32},
    {'type': 'num_big', 'x': 700, 'y': 200, 'w': 220, 'h': 80,
     'num': '50%', 'label': '实操占比', 'color': ORG, 'fs': 32},
    {'type': 'num_big', 'x': 700, 'y': 295, 'w': 220, 'h': 80,
     'num': '4+', 'label': 'AI 工具实战', 'color': ACC, 'fs': 32},
    {'type': 'tagline_bar', 'text': '认知 → 实操 → 自动化 → 开发：三小时走完「使用到创造」的完整路线',
     'color': ORG},
]})


# ---- S4: 第一层 对话式办公 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '第一层 · 对话式办公', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'cards_2x2', 'start_y': 78, 'items': [
        {'title': 'Word 文档撰写', 'color': O,
         'desc': '定框架 → AI 生成初稿 → 润色 → 人工校对\n人机协作，AI 是「高效的笔」'},
        {'title': 'Excel 数据处理', 'color': ORG,
         'desc': '问公式 · 问思路 · 写代码\n告别复杂函数记忆，直接说需求'},
        {'title': 'PPT 演示文稿制作', 'color': ACC,
         'desc': '定主题 → 建大纲 → 写内容 → 配图 → 加备注\nAI 是「排版与美工助手」'},
        {'title': 'PDF 文献阅读', 'color': '#007F6E',
         'desc': '提取 → 总结 → 对比 → 综述\nAI 是「速读与综述助手」'},
    ]},
    {'type': 'tagline_bar', 'text': '四大高频办公场景：把重复劳动交给 AI，把时间留给思考',
     'color': O},
]})


# ---- S5: Word 与 Excel ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': 'AI × Word · Excel', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 90, 'w': 420, 'h': 34,
     'text': 'Word：AI 撰写四步法', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 134, 'w': 440, 'h': 130,
     'text': '① 定框架：列提纲，明确结构\n② 填内容：AI 生成初稿\n③ 润色：AI 优化语言与逻辑\n④ 校对：人工把关，人机协作',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 45, 'y': 288, 'w': 440, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 500, 'y': 90, 'w': 420, 'h': 34,
     'text': 'Excel：三种问法', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 134, 'w': 440, 'h': 130,
     'text': '① 问公式：直接要函数与写法\n② 问思路：讲解数据处理逻辑\n③ 写代码：让 AI 输出可运行脚本\n\n示例：AI 写个公式统计各部门业绩？',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'table', 'x': 45, 'y': 320, 'w': 895, 'h': 150, 'rows': 3, 'cols': 2,
     'header_color': O, 'th_fs': 14, 'td_fs': 15,
     'data': [
         ['场景', 'AI 提示词一句话'],
         ['写通知', '帮我起草一份会议通知，语气正式'],
         ['做统计', '把这份表按月份汇总，并标出最高值'],
     ]},
    {'type': 'tagline_bar', 'text': '「人给方向、AI 给产出」是文档与数据处理的核心心法', 'color': O},
]})


# ---- S6: PPT 与 PDF ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': 'AI × PPT · PDF', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 90, 'w': 420, 'h': 34,
     'text': 'PPT：五步制作法', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 134, 'w': 440, 'h': 130,
     'text': '① 定主题与观众\n② 建大纲（金字塔结构）\n③ 写每页内容\n④ 配图与排版\n⑤ 加备注并检查',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'shape', 'shape': 'rect', 'x': 45, 'y': 288, 'w': 440, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 500, 'y': 90, 'w': 420, 'h': 34,
     'text': 'PDF：四步精读法', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 134, 'w': 440, 'h': 130,
     'text': '① 提取：AI 解析全文要点\n② 总结：按问题重组信息\n③ 对比：多文献交叉印证\n④ 综述：产出结构化报告',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.55},
    {'type': 'table', 'x': 45, 'y': 320, 'w': 895, 'h': 150, 'rows': 3, 'cols': 2,
     'header_color': O, 'th_fs': 14, 'td_fs': 15,
     'data': [
         ['场景', 'AI 提示词一句话'],
         ['做汇报', '把这段文字做成 10 页大纲，主题要突出'],
         ['读论文', '总结这篇 PDF 的核心方法、数据与结论'],
     ]},
    {'type': 'tagline_bar', 'text': '演示重「结构」，阅读重「提取」——AI 让两者都变简单', 'color': O},
]})


# ---- S7: 第二层 自动化产出 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '第二层 · 自动化产出', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 88, 'w': 420, 'h': 34,
     'text': '一键生成 PPT（KB6）', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 132, 'w': 440, 'h': 150,
     'text': '原理：.pptx 文件本质由代码描述\n自然语言 → AI 写代码 → 运行生成文件\n\n工具：python-pptx · Marp · 在线工具',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'text', 'x': 500, 'y': 88, 'w': 420, 'h': 34,
     'text': '一键生成图表（KB7）', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 132, 'w': 440, 'h': 150,
     'text': '有数据 → matplotlib 图表\n讲流程 → Mermaid 流程/时序图\n要美观 → AI 文生图插画',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'table', 'x': 45, 'y': 310, 'w': 895, 'h': 160, 'rows': 4, 'cols': 2,
     'header_color': O, 'th_fs': 14, 'td_fs': 15,
     'data': [
         ['需求', '推荐工具', ],
         ['生成 PPTX 文件', 'python-pptx（AI 生成代码）'],
         ['数据可视化', 'matplotlib / Excel 图表'],
         ['流程示意图', 'Mermaid 代码 / 文生图'],
     ]},
    {'type': 'tagline_bar', 'text': '从「帮 AI 说需求」到「让 AI 造文件」——本课第一个惊喜时刻', 'color': O},
]})


# ---- S8: 第三层 Skills ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '第三层 · Skills 开发', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 90, 'w': 880, 'h': 66,
     'text': 'Skills 是什么：一套「教 AI 怎么做某事」的指令文件包，\n让固定流程无需反复描述，即装即用、可复用可分享。',
     'fs': 20, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 45, 'y': 180, 'w': 420, 'h': 34,
     'text': 'SKILL.md 结构', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 224, 'w': 440, 'h': 150,
     'text': '① Frontmatter：名称与描述\n② 何时使用：适用场景\n③ 执行步骤：具体操作流程\n④ 示例：输入输出样例',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'shape', 'shape': 'rect', 'x': 45, 'y': 288, 'w': 440, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 500, 'y': 180, 'w': 420, 'h': 34,
     'text': '核心技巧', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 224, 'w': 440, 'h': 150,
     'text': '让 AI 帮你写 Skill（元技能）\n描述需求 → AI 生成 SKILL.md\n解决：重复描述 · 格式不稳 · 经验难沉淀',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'tagline_bar', 'text': 'Skills = 给 AI 装「操作手册」：一次封装，处处复用', 'color': O},
]})


# ---- S9: 第三层 MCP ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '第三层 · MCP 开发', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 90, 'w': 880, 'h': 66,
     'text': 'MCP（Model Context Protocol）：Anthropic 2024 年提出的开放标准，\n是「AI 的万能 USB 接口」——让 AI 安全、标准化地连接外部工具与数据。',
     'fs': 20, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'table', 'x': 45, 'y': 185, 'w': 560, 'h': 270, 'rows': 6, 'cols': 2,
     'header_color': O, 'th_fs': 14, 'td_fs': 15,
     'data': [
         ['概念', '大白话'],
         ['Client', '需要外部能力的 AI 程序'],
         ['Server', '提供特定能力的程序'],
         ['Tool', '可调用动作（动手）'],
         ['Resource', '可读数据（眼睛）'],
         ['Prompt', '提示模板（套路）'],
     ]},
    {'type': 'text', 'x': 630, 'y': 185, 'w': 300, 'h': 34,
     'text': '最小 MCP Server', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 630, 'y': 229, 'w': 300, 'h': 130,
     'text': '两个工具：\n· add(a, b) 计算加法\n· greet(name) 打招呼\n\nPython / TypeScript 均可',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'text', 'x': 630, 'y': 380, 'w': 300, 'h': 66,
     'text': '配置一句命令，AI 客户端即可发现并自动调用工具。',
     'fs': 16, 'color': G, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'MCP = 给 AI 装「电源插座」：一次开发，所有 AI 客户端通用', 'color': O},
]})


# ---- S10: Skills vs MCP ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': 'Skills vs MCP', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'table', 'x': 60, 'y': 95, 'w': 840, 'h': 280, 'rows': 5, 'cols': 3,
     'header_color': O, 'th_fs': 16, 'td_fs': 16,
     'data': [
         ['对比项', 'Skills', 'MCP'],
         ['类比', '操作手册', '电源插座'],
         ['本质', '教 AI 怎么做', '给 AI 能做什么'],
         ['需要', '指令文件，无需代码', '开发 Server（可 AI 代写）'],
         ['适用', '固定流程复用', '访问外部世界能力'],
     ]},
    {'type': 'text', 'x': 60, 'y': 410, 'w': 840, 'h': 50,
     'text': 'Skills 是「内功心法」，MCP 是「外接武器」\n两者结合，AI 既能按套路办事，又能连接真实世界',
     'fs': 22, 'color': D, 'bold': True, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'Skills 教 AI 怎么做 · MCP 给 AI 能做什么 —— 本课两大核心产物', 'color': ORG},
]})


# ---- S11: 课程总结 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '课程总结 · 三层进阶', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'cards_2x3', 'start_y': 80, 'items': [
        {'title': '① 对话式办公', 'color': O,
         'desc': 'Word · Excel\nPPT · PDF\n四场景全覆盖'},
        {'title': '② 自动化产出', 'color': ORG,
         'desc': '一键生成 PPT\n一键生成图表\nAI 写代码造文件'},
        {'title': '③ 开发者之路', 'color': ACC,
         'desc': 'Skills 技能包\nMCP 连接器\n从使用到创造'},
        {'title': '方法论', 'color': '#007F6E',
         'desc': '人给方向\nAI 给产出\n人机协作闭环'},
        {'title': '元技能', 'color': '#6B46C1',
         'desc': '让 AI 帮你写\nSkills 与 MCP\n会提问就会开发'},
        {'title': '核心心法', 'color': '#BE1E2D',
         'desc': '重复即自动化\n需求即代码\n未来属于创造者'},
    ]},
    {'type': 'tagline_bar', 'text': '过去你是 AI 的遥控器；今天，AI 是你的生产线', 'color': O},
]})


# ---- S12: 作业与预告 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '作业与下周预告', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 90, 'w': 420, 'h': 34,
     'text': '本周作业', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 134, 'w': 440, 'h': 200,
     'text': '① AI 使用记录\n   记录本周用 AI 完成的 3 个任务\n② 诚信声明\n   说明哪些由 AI 完成\n③ 课后挑战（加分）\n   完成一个最小 MCP Server',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'shape', 'shape': 'rect', 'x': 45, 'y': 288, 'w': 440, 'h': 4, 'color': ORG},
    {'type': 'text', 'x': 500, 'y': 90, 'w': 420, 'h': 34,
     'text': '下周预告', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 500, 'y': 134, 'w': 440, 'h': 200,
     'text': 'AI 工具链实战\n\n· 组合使用多个 AI 工具\n· 把本周 Skills/MCP 用起来\n· 完成一个综合自动化任务',
     'fs': 18, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.7},
    {'type': 'tagline_bar', 'text': '学以致用：把「会问」变成「会用」，把「会用」变成「会造」', 'color': O},
]})


# ---- S13: 致谢 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 8, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 532, 'w': 960, 'h': 8, 'color': O},
    {'type': 'text', 'x': 60, 'y': 150, 'w': 840, 'h': 60,
     'text': '谢  谢', 'fs': 56, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 240, 'w': 840, 'h': 40,
     'text': '提问与交流', 'fs': 26, 'color': ORG, 'bold': True, 'align': 2, 'font': FB},
    {'type': 'text', 'x': 60, 'y': 300, 'w': 840, 'h': 80,
     'text': '「让 AI 替你干活，让 AI 生态替你干活，\n最后，让 AI 按你的规则干活。」',
     'fs': 20, 'color': D, 'bold': False, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 60, 'y': 430, 'w': 840, 'h': 30,
     'text': 'AI 办公自动化 · 第1周第3课 · 全程实战 · 学以致用',
     'fs': 16, 'color': G, 'bold': False, 'align': 2, 'font': FB},
]})


# ====== 构建引擎 ======
pythoncom.CoInitialize()
app = win32com.client.Dispatch('KWPP.Application')
app.Visible = True

ppt = app.Presentations.Add()
ppt.PageSetup.SlideWidth = 960
ppt.PageSetup.SlideHeight = 540

idx = [1]

def new_slide():
    s = ppt.Slides.Add(idx[0], 12)
    idx[0] += 1
    try:
        s.FollowMasterBackground = False
    except:
        pass
    bg = os.path.join(OUT, 'template_bg.png')
    if os.path.exists(bg):
        s.Background.Fill.UserPicture(bg)
    return s

for elist in slides:
    s = new_slide()
    for elem in elist['elements']:
        router = ROUTERS.get(elem.get('type', 'text'))
        if router:
            try:
                router(s, elem)
            except Exception as ex:
                print(f"WARN: {ex}")

pptx_path = os.path.join(OUT, 'AI办公自动化-技术展示.pptx')
ppt.SaveAs(pptx_path)
print(f'PPTX saved: {os.path.getsize(pptx_path):,} bytes')

pdf_path = os.path.join(OUT, 'AI办公自动化-技术展示.pdf')
try:
    ppt.SaveAs(pdf_path, 32)
    print(f'PDF saved: {os.path.getsize(pdf_path):,} bytes')
except:
    print('PDF export failed')

ppt.Close()
try:
    app.Quit()
except:
    pass
print('Done!')
