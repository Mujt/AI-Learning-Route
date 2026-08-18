# Excel Agent 可视化操作工具 · 开发文档

> 项目代号 `excel-agent`（MVP）｜技术路线：Windows COM/OLE 自动化（`pywin32`）
> 目标：让 AI Agent 通过「语义化 API + CLI + Skill」驱动 Excel，完成写入、格式化、公式、图表、导出等**简单可视化操作**，并实时看到界面变化。

---

## 1. 可行性：原理可推广

`harness-anything` 驱动 WPS 的本质是调用其 **COM 自动化对象模型**：

```
Python ──pywin32──▶ COM 接口 ──▶ 软件进程 ──▶ 界面/文档
```

只要软件对外暴露 COM/OLE 对象模型，即可用相同模式驱动。常见适用软件：

| 软件 | COM 入口 | 典型操作对象 |
| --- | --- | --- |
| **Excel** | `Excel.Application` | 工作簿/单元格/公式/图表 |
| Word | `Word.Application` | 文档/段落/表格/样式 |
| PowerPoint | `PowerPoint.Application` | 幻灯片/形状/动画 |
| AutoCAD | `AutoCAD.Application` | 图形实体/图层/标注 |
| MATLAB | `matlab.application` | 矩阵/绘图/仿真 |

> 结论：**可行**。选 **Excel** 是因为它最常用、COM 自动化最成熟（VBA 即其 COM 宏语言）、可视化价值高，且与 WPS 表格同源。

---

## 2. MVP 功能清单（简单即可）

| # | 功能 | API |
| --- | --- | --- |
| 1 | 新建/打开工作簿 | `new()` / `open(path)` |
| 2 | 写入单元格/整行/矩阵 | `write()` / `write_row()` / `write_matrix()` |
| 3 | 合并单元格 | `merge("A1:C1")` |
| 4 | 样式（加粗/字号/颜色/对齐） | `style(...)` |
| 5 | 列宽行高 | `col_width()` / `row_height()` |
| 6 | 公式 | `formula("D2","=SUM(...)")` |
| 7 | 生成图表 | `add_chart(...)` |
| 8 | 图表导出 PNG | `export_chart_png()` |
| 9 | 保存 xlsx / 导出 PDF | `save()` / `export_pdf()` |
| 10 | 回收进程 | `close()` |

---

## 3. 架构与目录

```
excel-agent/
├── backend.py          # COM 后端（唯一接触 win32com）
├── core/excel_doc.py   # 语义化 API（ExcelDoc）
├── core/quality.py     # 简单质量检查
├── cli.py              # CLI 入口
├── example.py          # 端到端示例
├── skills/SKILL.md     # Agent 技能定义
└── requirements.txt    # pywin32>=306
```

分层：`Skill → CLI → ExcelDoc(语义API) → quality → backend(COM) → Excel进程(Visible=True)`。核心原则：**只有 `backend.py` import `win32com`**，上层与 COM 解耦。

---

## 4. 后端层 `backend.py`

```python
import os, pythoncom
import win32com.client as win32

FILE_FORMAT = {"xlsx": 51, "xls": 56, "csv": 6}
EXPORT_FORMAT = {"pdf": 0, "xps": 1}

class ExcelBackend:
    def __init__(self, visible=True):
        pythoncom.CoInitialize()
        self.app = win32.Dispatch("Excel.Application")
        self.app.Visible = visible          # True = 可视化操作
        self.app.DisplayAlerts = False      # 关闭弹窗
        self._workbook = None

    def new_workbook(self):
        self._workbook = self.app.Workbooks.Add()
        return self._workbook

    def open_workbook(self, path):
        self._workbook = self.app.Workbooks.Open(os.path.abspath(path))
        return self._workbook

    def get_sheet(self, index=1):
        return self._workbook.Worksheets(index)

    def save_as(self, path, fmt="xlsx"):
        self._workbook.SaveAs(os.path.abspath(path), FileFormat=FILE_FORMAT[fmt])

    def export_pdf(self, path):
        self._workbook.ExportAsFixedFormat(EXPORT_FORMAT["pdf"], os.path.abspath(path))

    def close(self, save=False):
        try:
            if self._workbook:
                self._workbook.Close(SaveChanges=save)
        finally:
            self.app.Quit()
            pythoncom.CoUninitialize()
```

---

## 5. 语义 API 层 `core/excel_doc.py`

```python
from backend import ExcelBackend

def rgb(r, g, b):
    return r + (g << 8) + (b << 16)   # Excel COM 颜色为长整型(BGR)

HALIGN = {"left": -4131, "center": -4108, "right": -4152}
VALIGN = {"top": -4160, "center": -4108, "bottom": -4107}
CHART_TYPE = {"column": 51, "line": 4, "pie": 5, "bar": 57}

class ExcelDoc:
    def __init__(self, visible=True):
        self._bk = ExcelBackend(visible)
        self.sheet = None

    def new(self, name=None):
        self._bk.new_workbook()
        self.sheet = self._bk.get_sheet(1)
        if name: self.sheet.Name = name
        return self

    def open(self, path, sheet_index=1):
        self._bk.open_workbook(path)
        self.sheet = self._bk.get_sheet(sheet_index)
        return self

    def write(self, cell, value):
        self.sheet.Range(cell).Value = value
        return self

    def write_row(self, start, values):
        col, row = self._col(start), self._row(start)
        for i, v in enumerate(values):
            self.sheet.Cells(row, col + i).Value = v
        return self

    def write_matrix(self, start, matrix):
        col, row = self._col(start), self._row(start)
        for r, line in enumerate(matrix):
            for c, v in enumerate(line):
                self.sheet.Cells(row + r, col + c).Value = v
        return self

    def formula(self, cell, expr):
        self.sheet.Range(cell).Formula = expr
        return self

    def merge(self, rng):
        self.sheet.Range(rng).Merge()
        return self

    def style(self, rng, bold=False, size=None, color=None, bg=None,
              halign=None, valign=None):
        r = self.sheet.Range(rng)
        if bold: r.Font.Bold = True
        if size: r.Font.Size = size
        if color: r.Font.Color = rgb(*color)
        if bg: r.Interior.Color = rgb(*bg)
        if halign: r.HorizontalAlignment = HALIGN[halign]
        if valign: r.VerticalAlignment = VALIGN[valign]
        return self

    def col_width(self, col, w):
        self.sheet.Columns(col).ColumnWidth = w
        return self

    def row_height(self, row, h):
        self.sheet.Rows(row).RowHeight = h
        return self

    def add_chart(self, data_range, chart_type="column",
                  left=300, top=50, width=400, height=280):
        co = self.sheet.ChartObjects().Add(left, top, width, height)
        ch = co.Chart
        ch.ChartType = CHART_TYPE[chart_type]
        ch.SetSourceData(self.sheet.Range(data_range))
        return ch

    def export_chart_png(self, chart, path):
        chart.Export(os.path.abspath(path), "PNG")
        return self

    def save(self, path, fmt="xlsx"):
        self._bk.save_as(path, fmt)
        return self

    def export_pdf(self, path):
        self._bk.export_pdf(path)
        return self

    def close(self, save=False):
        self._bk.close(save)
        return self

    @staticmethod
    def _col(cell):
        s = "".join(c for c in cell if c.isalpha()).upper()
        n = 0
        for ch in s: n = n * 26 + ord(ch) - 64
        return n

    @staticmethod
    def _row(cell):
        return int("".join(c for c in cell if c.isdigit()))
```

> `excel_doc.py` 需 `import os`（`export_chart_png` 用到）。

---

## 6. 质量检查层 `core/quality.py`

```python
def check_empty_used_range(doc):
    """检查已使用区域内空单元格（首行表头场景）。"""
    used = doc.sheet.UsedRange
    if used is None:
        return []
    problems = []
    for r in range(1, used.Rows.Count + 1):
        for c in range(1, used.Columns.Count + 1):
            if used.Cells(r, c).Value in (None, ""):
                problems.append(f"空单元格: ({r},{c})")
    return problems

def check_column_too_narrow(doc, cols, max_width=8):
    """检查指定列是否过窄（可能被截断显示）。"""
    out = []
    for col in cols:
        w = doc.sheet.Columns(col).ColumnWidth
        if w < max_width:
            out.append(f"列 {col} 宽度 {w} 过窄")
    return out
```

---

## 7. CLI 入口 `cli.py`

```python
import argparse
from core.excel_doc import ExcelDoc

def main():
    p = argparse.ArgumentParser(description="Excel Agent 工具")
    p.add_argument("--new", action="store_true", help="新建工作簿")
    p.add_argument("--open", help="打开已有工作簿")
    p.add_argument("--write", nargs=2, metavar=("CELL", "VALUE"), help="写单元格")
    p.add_argument("--formula", nargs=2, metavar=("CELL", "EXPR"), help="写公式")
    p.add_argument("--chart", metavar="RANGE", help="生成图表")
    p.add_argument("--save", metavar="PATH", help="保存 xlsx")
    p.add_argument("--pdf", metavar="PATH", help="导出 PDF")
    p.add_argument("--invisible", action="store_true", help="后台运行(不显示界面)")
    args = p.parse_args()

    doc = ExcelDoc(visible=not args.invisible)
    if args.open:
        doc.open(args.open)
    else:
        doc.new()
    if args.write:
        doc.write(args.write[0], args.write[1])
    if args.formula:
        doc.formula(args.formula[0], args.formula[1])
    if args.chart:
        doc.add_chart(args.chart)
    if args.save:
        doc.save(args.save)
    if args.pdf:
        doc.export_pdf(args.pdf)
    doc.close(save=bool(args.save))

if __name__ == "__main__":
    main()
```

用法示例：

```bash
python cli.py --new --write A1 标题 --formula B2 =SUM(B2:B10) --chart A1:B10 --save out.xlsx --pdf out.pdf
```

---

## 8. Agent 技能定义 `skills/SKILL.md`

```markdown
---
name: excel-agent
description: 驱动 Excel 完成写入/格式化/公式/图表/导出等简单可视化操作。
---

## 能力
- 新建/打开工作簿，写入数据（单元格/行/矩阵）
- 合并单元格、设置字体字号颜色对齐、调整行列
- 写入公式、生成柱状/折线/饼图/条形图
- 保存 xlsx、导出 PDF、导出图表 PNG

## 调用方式
python example.py   # 运行内置示例
python cli.py --new --write A1 值 --save out.xlsx

## 约定
- 操作过程默认 Visible=True，界面实时可见
- 任务结束必须调用 close() 回收 Excel 进程
```

---

## 9. 端到端示例 `example.py`

```python
from core.excel_doc import ExcelDoc

doc = ExcelDoc(visible=True)          # 1. 打开 Excel，界面可见
doc.new("销售报表")

# 2. 写表头并美化
doc.merge("A1:D1").write("A1", "季度销售报表")
doc.style("A1:D1", bold=True, size=16, bg=(31, 78, 121),
          color=(255, 255, 255), halign="center")

# 3. 写数据
doc.write_row("A2", ["季度", "产品A", "产品B", "合计"])
doc.write_matrix("A3", [["Q1", 120, 90, None],
                        ["Q2", 150, 110, None],
                        ["Q3", 180, 130, None],
                        ["Q4", 200, 160, None]])

# 4. 公式：合计列自动求和
for r in range(3, 7):
    doc.formula(f"D{r}", f"=SUM(B{r}:C{r})")

# 5. 格式：表头加粗、列宽
doc.style("A2:D2", bold=True, halign="center")
doc.col_width("A", 12)
for col in "BCD":
    doc.col_width(col, 14)

# 6. 生成图表并导出 PNG
chart = doc.add_chart("A2:C6", chart_type="column", left=300, top=50)
doc.export_chart_png(chart, "chart.png")

# 7. 保存并导出 PDF
doc.save("销售报表.xlsx")
doc.export_pdf("销售报表.pdf")

# 8. 回收进程（关键！）
doc.close(save=True)
```

运行后你将看到：Excel 窗口实时弹出 → 数据逐格填入 → 表头变色加粗 → 公式自动求和 → 柱状图生成 → 最终保存 `销售报表.xlsx` 与 `销售报表.pdf`，图表另存为 `chart.png`。

---

## 10. 资源回收与错误处理

| 问题 | 对策 |
| --- | --- |
| 进程残留 | `close()` 必须在 `finally` 中调用；`DisplayAlerts=False` 避免卡弹窗 |
| 脚本中途崩溃 | 用上下文管理器包装（见下） |
| 多线程 COM 冲突 | `__init__` 里 `pythoncom.CoInitialize()` |

推荐的上下文管理器写法：

```python
class ExcelDoc:
    def __enter__(self): return self
    def __exit__(self, *a): self.close()

# 使用
with ExcelDoc() as doc:
    doc.new()
    doc.write("A1", "hello")
    doc.save("x.xlsx")
# 离开 with 块自动 close()，即使中途抛异常也会回收
```

---

## 11. 测试验证清单

- [ ] `python example.py` 能弹出 Excel 并生成 3 个产物文件
- [ ] `--invisible` 模式后台运行不弹窗
- [ ] 反复运行多次后，任务管理器无残留 `EXCEL.EXE` 进程
- [ ] `export_pdf` 生成的 PDF 打开内容正确、图表完整
- [ ] 中文写入不乱码

---

## 12. 扩展方向

1. **同原理迁移**：把 `backend.py` 换成 `Word.Application` / `PowerPoint.Application` / `AutoCAD.Application`，上层 `ExcelDoc` 换成对应语义 API，架构不变。
2. **多软件统一**：抽象出 `Backend` 接口，`ExcelDoc`/`WordDoc`/`PptDoc` 实现同一套 `write/style/export` 契约，Agent 一个 Skill 通吃 Office 全家桶。
3. **非 COM 软件**：对浏览器可用 Chrome DevTools Protocol（CDP），对任意 GUI 软件可用 UI Automation（`pywinauto`），思路同为「接口驱动而非模拟点击」。

---

## 附录：常用 Excel COM 常量速查

| 用途 | 常量 | 值 |
| --- | --- | --- |
| 文件格式 xlsx | xlOpenXMLWorkbook | 51 |
| 文件格式 csv | xlCSV | 6 |
| 导出 PDF | xlTypePDF | 0 |
| 柱状图 | xlColumnClustered | 51 |
| 折线图 | xlLine | 4 |
| 饼图 | xlPie | 5 |
| 条形图 | xlBarClustered | 57 |
| 水平居中 | xlCenter | -4108 |
| 垂直居中 | xlCenter | -4108 |
