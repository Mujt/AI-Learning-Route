# -*- coding: utf-8 -*-
"""Excel-Agent 可视化操作工具 · 开发文档技术展示PPT

遵循 harness-anything 官方工作流：JSON数据驱动 + WPS COM 构建（Kwpp.Application）。
内容来源：《补充知识/Excel-Agent可视化操作工具开发文档.md》
画布：960 × 540 pt（16:9）
"""
import os, pythoncom, win32com.client

# ====== 配置 ======
OUT = os.path.dirname(os.path.abspath(__file__))
FT = 'SimHei'            # 标题字体
FB = 'Microsoft YaHei'   # 正文字体
FC = 'Consolas'          # 代码字体
O = '#004098'            # 品牌蓝
D = '#333333'            # 正文黑
G = '#666666'            # 辅助灰
ACC = '#00A0E9'          # 亮蓝（强调）
ORG = '#F28C28'          # 橙（强调）
EXC = '#217346'          # Excel 绿
PUR = '#6B46C1'          # 紫

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

def draw_shape(s, e):
    st = e.get('shape', 'rect')
    x, y, w = e['x'], e['y'], e['w']
    h = e.get('h', e.get('w', 10))
    c = h2b(e.get('color', O))
    if st == 'circle':
        circle(s, x, y, w, h, c)
    else:
        rect(s, x, y, w, h, c)

def draw_codebox(s, e):
    """深色代码框：逐行渲染等宽文本，手动控制行高防溢出。"""
    lines = e['lines']
    x, y, w, h = e['x'], e['y'], e['w'], e['h']
    bg = h2b(e.get('bg', '#1E1E2E'))
    fs = e.get('fs', 12)
    lh = e.get('line_h', 15)
    pad = e.get('pad', 12)
    fg_hi = h2b('#F2C94C')
    fg_norm = h2b('#E8E8E8')
    font = e.get('font', FC)
    rect(s, x, y, w, h, bg)
    for i, line in enumerate(lines):
        ty = y + pad + i * lh
        if ty + lh > y + h - 2:
            break
        is_hi = line.startswith('# ') or line.startswith('class ') or line.startswith('def ')
        tb = s.Shapes.AddTextbox(1, x + pad, ty, w - pad * 2, lh)
        tr = tb.TextFrame.TextRange
        tr.Text = line
        tr.Font.Size = fs
        tr.Font.Color = fg_hi if is_hi else fg_norm
        tr.Font.Name = font
        tr.ParagraphFormat.Alignment = 1
        tb.TextFrame.WordWrap = False

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
    hex_colors = [O, ORG, ACC, EXC, PUR, O, ORG, ACC]
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
    'shape': draw_shape,
    'codebox': draw_codebox,
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
    {'type': 'shape', 'shape': 'rect', 'x': 60, 'y': 150, 'w': 60, 'h': 6, 'color': EXC},
    {'type': 'text', 'x': 60, 'y': 100, 'w': 840, 'h': 56,
     'text': 'Excel Agent 可视化操作工具', 'fs': 48, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 168, 'w': 840, 'h': 40,
     'text': '开发文档 · MVP · 技术路线讲解', 'fs': 26, 'color': EXC, 'bold': True, 'align': 1, 'font': FB},
    {'type': 'text', 'x': 60, 'y': 236, 'w': 840, 'h': 76,
     'text': '让 AI Agent 通过「语义化 API + CLI + Skill」驱动 Excel，\n完成写入、格式化、公式、图表、导出等简单可视化操作，并实时看到界面变化。',
     'fs': 19, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'num_big', 'x': 90, 'y': 350, 'w': 240, 'h': 88,
     'num': '10', 'label': 'MVP 功能', 'color': EXC, 'fs': 44},
    {'type': 'num_big', 'x': 360, 'y': 350, 'w': 240, 'h': 88,
     'num': '6', 'label': '核心模块', 'color': O, 'fs': 44},
    {'type': 'num_big', 'x': 630, 'y': 350, 'w': 240, 'h': 88,
     'num': 'COM', 'label': '技术路线', 'color': ORG, 'fs': 44},
    {'type': 'text', 'x': 60, 'y': 470, 'w': 840, 'h': 30,
     'text': '技术路线：Windows COM/OLE 自动化（pywin32） · 项目代号 excel-agent（MVP）',
     'fs': 16, 'color': G, 'bold': False, 'align': 2, 'font': FB},
]})

# ---- S2: 目录 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 16, 'w': 840, 'h': 40,
     'text': '目  录', 'fs': 42, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'card_list_wide', 'start_y': 95, 'item_h': 96, 'items': [
        {'num': '01', 'title': '可行性',
         'sub': 'COM 自动化原理可推广，为何选 Excel'},
        {'num': '02', 'title': 'MVP 功能清单',
         'sub': '10 项核心能力：写入 / 样式 / 公式 / 图表 / 导出'},
        {'num': '03', 'title': '架构与代码实现',
         'sub': 'backend → ExcelDoc → quality → CLI → Skill 全链路'},
        {'num': '04', 'title': '端到端示例与工程化',
         'sub': 'example.py · 资源回收 · 测试验证 · 扩展方向'},
    ]},
    {'type': 'tagline_bar', 'text': '从「可行性论证」到「MVP 交付」：一堂课讲完一个 Excel 自动化 Agent', 'color': EXC},
]})

# ---- S3: 可行性：原理可推广 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '可行性：原理可推广', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 82, 'w': 880, 'h': 30,
     'text': 'harness-anything 驱动 WPS 的本质：调用软件暴露的 COM 自动化对象模型',
     'fs': 20, 'color': D, 'bold': True, 'align': 1, 'font': FB},
    {'type': 'codebox', 'x': 45, 'y': 122, 'w': 870, 'h': 52, 'fs': 15, 'line_h': 26, 'pad': 14,
     'lines': ['Python ──pywin32──▶ COM 接口 ──▶ 软件进程 ──▶ 界面/文档']},
    {'type': 'text', 'x': 45, 'y': 196, 'w': 880, 'h': 30,
     'text': '只要软件对外暴露 COM/OLE 对象模型，即可用相同模式驱动：', 'fs': 20, 'color': D,
     'bold': True, 'align': 1, 'font': FB},
    {'type': 'table', 'x': 45, 'y': 238, 'w': 870, 'h': 220, 'rows': 6, 'cols': 3,
     'header_color': O, 'th_fs': 15, 'td_fs': 15,
     'data': [
         ['软件', 'COM 入口', '典型操作对象'],
         ['Excel', 'Excel.Application', '工作簿/单元格/公式/图表'],
         ['Word', 'Word.Application', '文档/段落/表格/样式'],
         ['PowerPoint', 'PowerPoint.Application', '幻灯片/形状/动画'],
         ['AutoCAD', 'AutoCAD.Application', '图形实体/图层/标注'],
         ['MATLAB', 'matlab.application', '矩阵/绘图/仿真'],
     ]},
    {'type': 'tagline_bar',
     'text': '结论：可行。选 Excel —— 最常用 · COM 自动化最成熟 · 可视化价值高 · 与 WPS 表格同源', 'color': EXC},
]})

# ---- S4: MVP 功能清单 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': 'MVP 功能清单（简单即可）', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'table', 'x': 45, 'y': 92, 'w': 870, 'h': 370, 'rows': 11, 'cols': 3,
     'header_color': O, 'th_fs': 15, 'td_fs': 15,
     'data': [
         ['#', '功能', 'API'],
         ['1', '新建/打开工作簿', 'new() / open(path)'],
         ['2', '写入单元格/整行/矩阵', 'write() / write_row() / write_matrix()'],
         ['3', '合并单元格', 'merge("A1:C1")'],
         ['4', '样式（加粗/字号/颜色/对齐）', 'style(...)'],
         ['5', '列宽行高', 'col_width() / row_height()'],
         ['6', '公式', 'formula("D2","=SUM(...)")'],
         ['7', '生成图表', 'add_chart(...)'],
         ['8', '图表导出 PNG', 'export_chart_png()'],
         ['9', '保存 xlsx / 导出 PDF', 'save() / export_pdf()'],
         ['10', '回收进程', 'close()'],
     ]},
    {'type': 'tagline_bar', 'text': '全部「语义化 API」：Agent 说需求，代码驱动 Excel 实时可视化执行', 'color': EXC},
]})

# ---- S5: 架构与目录 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '架构与目录', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 82, 'w': 880, 'h': 30,
     'text': 'excel-agent 项目 · 六模块 七文件', 'fs': 22, 'color': EXC, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'table', 'x': 45, 'y': 128, 'w': 520, 'h': 330, 'rows': 7, 'cols': 2,
     'header_color': O, 'th_fs': 15, 'td_fs': 14,
     'data': [
         ['模块', '职责'],
         ['backend.py', 'COM 后端（唯一 import win32com）'],
         ['core/excel_doc.py', '语义化 API（ExcelDoc）'],
         ['core/quality.py', '简单质量检查'],
         ['cli.py', '命令行入口'],
         ['example.py', '端到端示例'],
         ['skills/SKILL.md', 'Agent 技能定义'],
     ]},
    {'type': 'text', 'x': 600, 'y': 128, 'w': 330, 'h': 34,
     'text': '分层调用链', 'fs': 24, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'codebox', 'x': 600, 'y': 172, 'w': 320, 'h': 190, 'fs': 13, 'line_h': 19, 'pad': 12,
     'lines': ['Skill', '  ↓', 'CLI', '  ↓', 'ExcelDoc (语义API)', '  ↓', 'quality', '  ↓',
               'backend (COM)', '  ↓', 'Excel 进程 Visible=True']},
    {'type': 'text', 'x': 600, 'y': 380, 'w': 330, 'h': 70,
     'text': '核心原则：\n只有 backend.py import win32com，\n上层与 COM 完全解耦。',
     'fs': 17, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.5},
    {'type': 'tagline_bar', 'text': 'Skill → CLI → ExcelDoc → quality → backend → Excel：单向依赖，后端可替换', 'color': EXC},
]})

# ---- S6: 后端层 backend.py ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '后端层 · backend.py', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 88, 'w': 500, 'h': 380, 'fs': 12, 'line_h': 16.5, 'pad': 12,
     'lines': [
         '# backend.py  COM 后端',
         'import os, pythoncom',
         'import win32com.client as win32',
         '',
         'FILE_FORMAT  = {"xlsx": 51,',
         '               "xls": 56, "csv": 6}',
         'EXPORT_FORMAT = {"pdf": 0, "xps": 1}',
         '',
         'class ExcelBackend:',
         '    def __init__(self, visible=True):',
         '        pythoncom.CoInitialize()',
         '        self.app = win32.Dispatch(',
         '            "Excel.Application")',
         '        self.app.Visible = visible',
         '        self.app.DisplayAlerts = False',
         '        self._workbook = None',
         '',
         '    def save_as(self, path, fmt):',
         '        self._workbook.SaveAs(path,',
         '            FileFormat=FILE_FORMAT[fmt])',
         '    def export_pdf(self, path):',
         '        self._workbook.ExportAsFixedFormat(',
         '            EXPORT_FORMAT["pdf"], path)',
     ]},
    {'type': 'text', 'x': 580, 'y': 88, 'w': 350, 'h': 34,
     'text': '设计要点', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'cards_2x2', 'start_y': 140, 'items': [
        {'title': '唯一 COM 接触点', 'color': EXC,
         'desc': '整个项目只有 backend.py\nimport win32com\n上层全部解耦'},
        {'title': '可视化开关', 'color': O,
         'desc': 'Visible=True 实时看到\nExcel 界面变化\nDisplayAlerts=False 防弹窗'},
        {'title': '常量映射', 'color': ORG,
         'desc': '文件格式/导出格式\n用常量表集中管理\n避免魔法数字'},
        {'title': '生命周期', 'color': ACC,
         'desc': 'close() 统一回收进程\npythoncom.CoInitialize()\n线程安全'},
    ]},
    {'type': 'tagline_bar', 'text': '后端层 = 软件进程的唯一「接入口」：其余模块一律经由它中转', 'color': EXC},
]})

# ---- S7: 语义 API 层 ExcelDoc ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '语义 API 层 · core/excel_doc.py', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'cards_2x3', 'start_y': 82, 'items': [
        {'title': '数据写入', 'color': EXC,
         'desc': 'write(cell, v)\nwrite_row(start, vals)\nwrite_matrix(start, m)\nformula(cell, expr)'},
        {'title': '格式化', 'color': O,
         'desc': 'style(bold/size/color/…)\nmerge("A1:C1")\ncol_width / row_height'},
        {'title': '图表', 'color': ORG,
         'desc': 'add_chart(rng, type)\ncolumn/line/pie/bar\nexport_chart_png()'},
        {'title': '生命周期', 'color': ACC,
         'desc': 'new() / open(path)\nsave() / export_pdf()\nclose() 回收进程'},
        {'title': '常量设计', 'color': PUR,
         'desc': 'rgb(r,g,b) → BGR 长整型\nHALIGN / VALIGN\nCHART_TYPE 映射表'},
        {'title': '链式调用', 'color': '#007F6E',
         'desc': '每个方法 return self\nnew().write().style()\n一步到底'},
    ]},
    {'type': 'text', 'x': 45, 'y': 452, 'w': 880, 'h': 30,
     'text': 'Excel COM 颜色为长整型(BGR)：rgb = r + (g<<8) + (b<<16) · 图表类型：column=51 / line=4 / pie=5 / bar=57',
     'fs': 16, 'color': G, 'bold': False, 'align': 2, 'font': FB},
    {'type': 'tagline_bar', 'text': 'ExcelDoc = 把 COM 的「对象迷宫」翻译成一句句人话命令', 'color': O},
]})

# ---- S8: 质量检查 + CLI ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '质量检查 + CLI 入口', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 86, 'w': 420, 'h': 34,
     'text': 'core/quality.py', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 130, 'w': 440, 'h': 200, 'fs': 12, 'line_h': 16.5, 'pad': 12,
     'lines': [
         '# quality.py',
         'def check_empty_used_range(doc):',
         '    """检查已用区域内空单元格"""',
         '    used = doc.sheet.UsedRange',
         '    problems = []',
         '    for r in range(1, used.Rows.Count+1):',
         '        for c in range(1,',
         '            used.Columns.Count+1):',
         '            if used.Cells(r,c).Value in',
         '                (None, ""):',
         '                problems.append(',
         '                f"空单元格: ({r},{c})")',
         '    return problems',
     ]},
    {'type': 'text', 'x': 45, 'y': 352, 'w': 440, 'h': 80,
     'text': 'check_column_too_narrow(doc, cols, max_width=8)\n检测列宽过窄导致的「显示截断」问题',
     'fs': 16, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'text', 'x': 525, 'y': 86, 'w': 400, 'h': 34,
     'text': 'cli.py · 参数一览', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'table', 'x': 525, 'y': 130, 'w': 400, 'h': 300, 'rows': 9, 'cols': 2,
     'header_color': ORG, 'th_fs': 14, 'td_fs': 14,
     'data': [
         ['参数', '作用'],
         ['--new', '新建工作簿'],
         ['--open PATH', '打开已有文件'],
         ['--write CELL VALUE', '写单元格'],
         ['--formula CELL EXPR', '写公式'],
         ['--chart RANGE', '生成图表'],
         ['--save PATH', '保存 xlsx'],
         ['--pdf PATH', '导出 PDF'],
         ['--invisible', '后台运行不弹窗'],
     ]},
    {'type': 'tagline_bar', 'text': '一行命令 = 一次 Agent 调用：CLI 是 Skill 与 ExcelDoc 之间的「桥」', 'color': EXC},
]})

# ---- S9: Agent 技能定义 SKILL.md ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': 'Agent 技能定义 · skills/SKILL.md', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 88, 'w': 520, 'h': 330, 'fs': 12.5, 'line_h': 19, 'pad': 12,
     'font': 'Microsoft YaHei',
     'lines': [
         '---',
         'name: excel-agent',
         'description: 驱动 Excel 完成写入/',
         '  格式化/公式/图表/导出等简单',
         '  可视化操作。',
         '---',
         '',
         '## 能力',
         '- 新建/打开工作簿，写入数据',
         '- 合并、样式、公式、图表',
         '- 保存 xlsx、导出 PDF / PNG',
         '',
         '## 调用方式',
         'python example.py',
         'python cli.py --new --write A1 值',
         '',
         '## 约定',
         '- 操作默认 Visible=True',
         '- 结束必须 close() 回收进程',
     ]},
    {'type': 'text', 'x': 605, 'y': 96, 'w': 330, 'h': 34,
     'text': 'Skill = Agent 的操作手册', 'fs': 24, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'cards_2x2', 'start_y': 148, 'items': [
        {'title': 'frontmatter', 'color': EXC,
         'desc': 'name: excel-agent\ndescription: 一句话\n说明能力范围'},
        {'title': '能力清单', 'color': O,
         'desc': '写入 / 格式化\n公式 / 图表 / 导出\n对齐 MVP 10 项功能'},
        {'title': '调用方式', 'color': ORG,
         'desc': 'example.py 演示\ncli.py 命令行\n两种接入路径'},
        {'title': '工程约定', 'color': ACC,
         'desc': 'Visible=True 可视化\nclose() 必回收\n可被 AI Agent 自动调用'},
    ]},
    {'type': 'tagline_bar', 'text': '有了 SKILL.md，AI Agent 就能「读懂并驱动」excel-agent 工具', 'color': EXC},
]})

# ---- S10: 端到端示例 example.py ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '端到端示例 · example.py', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 86, 'w': 500, 'h': 340, 'fs': 11.5, 'line_h': 15, 'pad': 12,
     'lines': [
         '# example.py',
         'doc = ExcelDoc(visible=True)',
         'doc.new("销售报表")',
         '',
         '# 表头：合并 + 样式',
         'doc.merge("A1:D1").write("A1",',
         '    "季度销售报表")',
         'doc.style("A1:D1", bold=True,',
         '    size=16, bg=(31,78,121),',
         '    color=(255,255,255),',
         '    halign="center")',
         '',
         '# 数据 + 公式',
         'doc.write_row("A2", [季度,产品A,',
         '    产品B,合计])',
         'doc.write_matrix("A3", [...])',
         'for r in range(3,7):',
         '    doc.formula(f"D{r}",',
         '        f"=SUM(B{r}:C{r})")',
         '',
         '# 图表 + 导出',
         'chart = doc.add_chart("A2:C6",',
         '    chart_type="column")',
         'doc.export_chart_png(chart,',
         '    "chart.png")',
         'doc.save("销售报表.xlsx")',
         'doc.export_pdf("销售报表.pdf")',
         '',
         '# 关键：回收进程',
         'doc.close(save=True)',
     ]},
    {'type': 'text', 'x': 580, 'y': 86, 'w': 350, 'h': 34,
     'text': '运行效果 · 可视化全程', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'cards_2x2', 'start_y': 138, 'items': [
        {'title': '实时可见', 'color': EXC,
         'desc': 'Excel 窗口弹出\n数据逐格填入\n表头变色加粗'},
        {'title': '公式自动求和', 'color': O,
         'desc': '=SUM(B:C) 逐行计算\n合计列自动填充\n图表同步生成'},
        {'title': '三类产物', 'color': ORG,
         'desc': '销售报表.xlsx\n销售报表.pdf\nchart.png'},
        {'title': '进程回收', 'color': ACC,
         'desc': 'close(save=True)\n数据已保存\n进程不残留'},
    ]},
    {'type': 'text', 'x': 580, 'y': 400, 'w': 350, 'h': 60,
     'text': '一次运行，完整演示\n「新建 → 写数 → 美化 → 公式 → 图表 → 导出」全流程',
     'fs': 16, 'color': D, 'bold': False, 'align': 1, 'font': FB, 'line_spacing': 1.6},
    {'type': 'tagline_bar', 'text': 'example.py 是 Skill 的「活文档」：跑一遍 = 看一遍全部能力', 'color': EXC},
]})

# ---- S11: 资源回收与错误处理 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '资源回收与错误处理', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'table', 'x': 45, 'y': 88, 'w': 870, 'h': 170, 'rows': 4, 'cols': 2,
     'header_color': O, 'th_fs': 15, 'td_fs': 16,
     'data': [
         ['问题', '对策'],
         ['进程残留', 'close() 必须放在 finally 中；DisplayAlerts=False 避免卡弹窗'],
         ['脚本中途崩溃', '用上下文管理器包装，异常也自动回收'],
         ['多线程 COM 冲突', '__init__ 里调用 pythoncom.CoInitialize()'],
     ]},
    {'type': 'text', 'x': 45, 'y': 286, 'w': 870, 'h': 34,
     'text': '推荐的上下文管理器写法（推荐工程用法）', 'fs': 24, 'color': EXC, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 330, 'w': 870, 'h': 130, 'fs': 14, 'line_h': 20, 'pad': 14,
     'lines': [
         'class ExcelDoc:',
         '    def __enter__(self): return self',
         '    def __exit__(self, *a): self.close()',
         '',
         'with ExcelDoc() as doc:          # 离开 with 自动 close()',
         '    doc.new().write("A1", "hello").save("x.xlsx")',
     ]},
    {'type': 'tagline_bar', 'text': 'Agent 自动化最怕「进程残留」：with 写法让回收成为必然', 'color': EXC},
]})

# ---- S12: 测试验证 + 扩展方向 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '测试验证 + 扩展方向', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 45, 'y': 84, 'w': 420, 'h': 34,
     'text': '测试验证清单', 'fs': 26, 'color': O, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'codebox', 'x': 45, 'y': 128, 'w': 430, 'h': 210, 'fs': 13, 'line_h': 21, 'pad': 12,
     'lines': [
         '[x] example.py 弹出 Excel 并生成',
         '    3 个产物文件',
         '[x] --invisible 后台运行不弹窗',
         '[x] 反复运行后任务管理器',
         '    无残留 EXCEL.EXE',
         '[x] export_pdf 内容正确、图表完整',
         '[x] 中文写入不乱码',
     ]},
    {'type': 'text', 'x': 510, 'y': 84, 'w': 420, 'h': 34,
     'text': '扩展方向', 'fs': 26, 'color': ORG, 'bold': True, 'align': 1, 'font': FT},
    {'type': 'cards_2x3', 'start_y': 128, 'items': [
        {'title': '同原理迁移', 'color': O,
         'desc': '换 backend 为 Word /\nPowerPoint / AutoCAD\n架构不变'},
        {'title': '多软件统一', 'color': EXC,
         'desc': '抽象 Backend 接口\nExcel/Word/Ppt 同一套\nwrite/style/export 契约'},
        {'title': '非 COM 软件', 'color': ORG,
         'desc': '浏览器用 CDP\nGUI 用 UI Automation\n(pywinauto)'},
        {'title': '统一 Skill', 'color': ACC,
         'desc': '一个 Skill 通吃\nOffice 全家桶\nAgent 随调随用'},
        {'title': '质量扩展', 'color': PUR,
         'desc': '更多检查项\n数据一致性校验\n报表模板校验'},
        {'title': '云端化', 'color': '#007F6E',
         'desc': '本地 COM + 远程 API\nAgent 平台接入\nWeb 可视化'},
    ]},
    {'type': 'tagline_bar', 'text': '思路核心：接口驱动而非模拟点击 —— 同一模式可复制到所有带接口的软件', 'color': EXC},
]})

# ---- S13: 总结 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 5, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 535, 'w': 960, 'h': 5, 'color': O},
    {'type': 'text', 'x': 60, 'y': 14, 'w': 840, 'h': 38,
     'text': '总结 · 一条完整的自动化链路', 'fs': 40, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'codebox', 'x': 80, 'y': 90, 'w': 800, 'h': 120, 'fs': 16, 'line_h': 26, 'pad': 16,
     'lines': [
         'AI Agent（说需求）',
         '   ↓ SKILL.md（教怎么做）',
         '   ↓ cli.py（命令行）',
         '   ↓ ExcelDoc（语义 API）',
         '   ↓ backend.py（COM 封装）',
         '   ↓ Excel 进程（界面实时可见）',
     ]},
    {'type': 'cards_2x3', 'start_y': 240, 'items': [
        {'title': '可行性', 'color': EXC,
         'desc': 'COM 自动化\n原理可推广\nExcel 最成熟'},
        {'title': 'MVP 交付', 'color': O,
         'desc': '10 项功能\n6 大模块\n开箱即用'},
        {'title': '可视化', 'color': ORG,
         'desc': 'Visible=True\n操作实时可见\n教学演示友好'},
        {'title': 'Agent 化', 'color': ACC,
         'desc': 'SKILL.md 技能包\nCLI 一行调用\nAI 可直接驱动'},
        {'title': '工程化', 'color': PUR,
         'desc': 'with 自动回收\n质量检查\n无进程残留'},
        {'title': '可扩展', 'color': '#007F6E',
         'desc': '同原理迁移\nOffice 全家桶\nCDP / UIA'},
    ]},
    {'type': 'tagline_bar', 'text': 'excel-agent = 用 100 行代码，让 Agent 亲手操作 Excel 的完整范本', 'color': EXC},
]})

# ---- S14: 致谢 ----
slides.append({'elements': [
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 0, 'w': 960, 'h': 8, 'color': O},
    {'type': 'shape', 'shape': 'rect', 'x': 0, 'y': 532, 'w': 960, 'h': 8, 'color': O},
    {'type': 'text', 'x': 60, 'y': 150, 'w': 840, 'h': 60,
     'text': '谢  谢', 'fs': 56, 'color': O, 'bold': True, 'align': 2, 'font': FT},
    {'type': 'text', 'x': 60, 'y': 240, 'w': 840, 'h': 40,
     'text': '提问与交流', 'fs': 26, 'color': EXC, 'bold': True, 'align': 2, 'font': FB},
    {'type': 'text', 'x': 60, 'y': 300, 'w': 840, 'h': 80,
     'text': '「接口驱动而非模拟点击」\n让 AI 亲手操作 Excel，实时看见每一次变化。',
     'fs': 20, 'color': D, 'bold': False, 'align': 2, 'font': FB, 'line_spacing': 1.5},
    {'type': 'text', 'x': 60, 'y': 430, 'w': 840, 'h': 30,
     'text': 'Excel-Agent 可视化操作工具 · 开发文档 · 技术路线 COM/pywin32',
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

pptx_path = os.path.join(OUT, 'Excel-Agent开发文档-技术展示.pptx')
ppt.SaveAs(pptx_path)
print(f'PPTX saved: {os.path.getsize(pptx_path):,} bytes')

pdf_path = os.path.join(OUT, 'Excel-Agent开发文档-技术展示.pdf')
try:
    ppt.SaveAs(pdf_path, 32)
    print(f'PDF saved: {os.path.getsize(pdf_path):,} bytes')
except Exception:
    print('PDF export failed')

ppt.Close()
try:
    app.Quit()
except Exception:
    pass
print('Done!')
