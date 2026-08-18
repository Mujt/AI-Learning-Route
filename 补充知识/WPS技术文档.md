# harness-anything WPS 自动化生成工具 技术文档

> 版本：v1.0
> 适用范围：`cli_anything/wps` 子包
> 平台：Windows + WPS Office（依赖 COM 接口）

---

## 1. 项目概述

`harness-anything` 是一套以 **命令行（CLI）/ REPL** 驱动 WPS Office 的 Python 工具集。其核心子包 `cli_anything/wps` 对 WPS 三大组件——**文字（Writer）、演示（Impress）、表格（Calc）** 做了高层面向对象封装，目标是让 AI Agent 或脚本能够**程序化生成**：

- Word 文档（`.docx`）
- PowerPoint 演示文稿（`.pptx`）
- Excel 电子表格（`.xlsx`）

并支持导出为 **PNG / PDF / JPG** 等静态格式，同时内置**设计预设、布局模板、质量检查**能力，保证生成物达到「可直接用于汇报 / 出版」的视觉水准。

### 1.1 设计目标

| 目标 | 说明 |
| --- | --- |
| **高层抽象** | 屏蔽底层 COM 调用的繁琐细节，提供语义化 API |
| **可复现** | 生成过程完全由代码驱动，结果可重复、可版本化 |
| **面向 Agent** | 通过 `SKILL.md` 暴露给 AI Agent，作为「技能」被调用 |
| **质量可控** | 内置溢出检测、字体/配色规范等自动检查 |
| **多格式导出** | 一份数据源，可导出多种交付格式 |

---

## 2. 目录结构

```
cli_anything/wps/
├── __init__.py            # 包入口，暴露核心 API
├── __main__.py            # 支持 python -m 方式运行
├── wps_cli.py             # CLI 入口：参数解析 + 命令分发
├── core/                  # 核心业务层
│   ├── document.py        # 文档基类（生命周期、公共属性）
│   ├── session.py         # 会话管理（WPS 进程/应用实例的创建与回收）
│   ├── impress.py         # 演示文稿（PPT）生成
│   ├── writer.py          # 文字（Word）生成
│   ├── calc.py            # 表格（Excel）生成
│   ├── export.py          # 导出：PNG / PDF / 图片序列
│   ├── styles.py          # 样式模型（字体、颜色、对齐等）
│   └── preset.py          # 预设（内置成品模板/样式包）
├── styles/                # 样式与规范层
│   ├── design_presets.py  # 设计预设（配色方案、字体组合）
│   ├── layout_templates.py# 布局模板（版式骨架）
│   └── quality_checks.py  # 质量检查（文本溢出、边界、一致性）
├── utils/                 # 工具层
│   ├── wps_backend.py     # WPS COM 后端封装（核心底层）
│   └── repl_skin.py       # REPL 交互界面（彩色输出、提示符）
└── skills/
    └── SKILL.md           # Skill 定义文件（供 AI Agent 识别）
```

配套示例项目：

```
WPS/
└── 南科大/
    ├── build_sustech.py   # 南科大 PPT 完整构建脚本（真实用例）
    └── gen_charts.py      # 图表生成脚本
```

---

## 3. 分层架构

```
┌─────────────────────────────────────────────┐
│  Skill 层   skills/SKILL.md                 │  ← AI Agent 调用协议
├─────────────────────────────────────────────┤
│  CLI 层     wps_cli.py / __main__.py        │  ← 命令行入口
├─────────────────────────────────────────────┤
│  业务层     core/*.py                       │  ← 语义化 API（impress/writer/calc）
├─────────────────────────────────────────────┤
│  规范层     styles/*.py                     │  ← 设计预设 / 布局模板 / 质量检查
├─────────────────────────────────────────────┤
│  工具层     utils/repl_skin.py              │  ← REPL 交互皮肤
├─────────────────────────────────────────────┤
│  后端层     utils/wps_backend.py            │  ← COM 调度（Kwpp/Kwps Application）
├─────────────────────────────────────────────┤
│  WPS Office（Kwpp / Kwps / Ket Application）│  ← 实际渲染引擎
└─────────────────────────────────────────────┘
```

**依赖方向**：上层只依赖下层，`core` 不直接触碰 COM，全部经由 `wps_backend` 中转，实现「后端可替换」的隔离。

---

## 4. 核心模块详解

### 4.1 后端层 `utils/wps_backend.py`

负责与 WPS 进程建立、维持、断开连接，是整个工具的唯一 COM 接触点。

- **职责**
  - 通过 COM（`Dispatch` / `EnsureDispatch`）创建 WPS 应用实例（演示 `Kwpp.Application`、文字 `Kwps.Application`、表格 `Ket.Application`）。
  - 管理应用/文档对象的引用计数与生命周期，确保进程在任务结束后被正确回收（`Quit`）。
  - 提供统一的「打开 / 新建 / 保存 / 关闭 / 导出」底层原语。
  - 异常兜底：COM 调用失败时的重试与清理。

- **关键点**
  - 隐藏「演示 / 文字 / 表格」三套不同 COM 接口的差异，向上层暴露统一命名。
  - 导出 PNG/PDF 的能力依赖 WPS 自带的 `Export` / `SaveAs` 接口。

### 4.2 文档基类 `core/document.py`

所有文档类型的公共抽象，定义统一的打开、保存、关闭生命周期，以及尺寸、路径、元数据等公共属性，让 `impress` / `writer` / `calc` 复用同一套骨架。

### 4.3 会话管理 `core/session.py`

- 管理「一次生成任务」的完整生命周期。
- 负责 `backend` 实例的创建、上下文切换（当前操作的是哪个文档）、以及 `finally` 式的资源清理。
- 典型用法：`with Session() as s: ...`，确保 WPS 进程不残留。

### 4.4 演示文稿 `core/impress.py`

面向 PPT 的高层 API，是三大组件中能力最丰富的一个。

- 新建演示文稿、设置页面尺寸与方向。
- 添加 / 删除 / 复制幻灯片。
- 在幻灯片上放置**文本框、图片、形状、表格、图表**等元素，并精确定位（`left/top/width/height`，单位通常为磅 pt）。
- 应用 `design_presets` 配色与字体。
- 应用 `layout_templates` 中的版式（封面页、目录页、内容页、章节过渡页、结束页等）。

### 4.5 文字 `core/writer.py`

面向 Word 的高层 API：

- 段落 / 标题 / 列表 / 表格 / 图片的插入。
- 样式（字体、字号、行距、首行缩进等）的设置。
- 目录、页眉页脚的生成。

### 4.6 表格 `core/calc.py`

面向 Excel 的高层 API：

- 单元格写入、合并、格式化（数字格式、边框、填充）。
- 公式、行列宽高调整、冻结窗格等。

### 4.7 导出 `core/export.py`

- 将当前文档导出为 **PDF**（用于分发、打印）。
- 将演示文稿导出为 **PNG/JPG 图片序列**（每页一张，用于预览、缩略图、网页展示）。
- 统一处理导出分辨率、文件命名与输出目录。

### 4.8 样式模型 `core/styles.py`

定义样式对象模型：`Color`、`Font`、`ParagraphStyle`、`ShapeStyle` 等数据结构，作为上层 API 与底层 COM 之间的「样式中间表示」。

### 4.9 预设 `core/preset.py`

内置若干「开箱即用」的成品样式包 / 模板，供快速套用，减少用户自行组合样式的成本。

---

## 5. 规范层（styles/）

### 5.1 设计预设 `design_presets.py`

- 内置多套**配色方案**（主色 / 辅色 / 强调色 / 背景色 / 文字色）。
- 内置**字体组合**（中文标题字体、正文字体、西文字体）。
- 用户只需指定预设名，即可整套套用，保证风格统一。

### 5.2 布局模板 `layout_templates.py`

- 提供结构化版式骨架，例如：
  - 封面页（标题 + 副标题 + 作者 + 日期）
  - 目录页
  - 章节分隔页（大标题 + 编号）
  - 两栏 / 三栏内容页
  - 图文混排页
  - 结束页（致谢）
- 模板与内容解耦：模板只规定「框在哪、多大」，内容由调用方填充。

### 5.3 质量检查 `quality_checks.py`

生成后自动执行的「体检」，常见检查项：

- **文本溢出检测**：估算文本渲染后的尺寸，判断是否超出所在文本框 / 幻灯片边界。
- **越界检测**：元素坐标是否超出页面可视范围。
- **字号过小 / 对比度不足**等可读性问题。
- 输出检查报告，供调用方定位并修正问题页。

---

## 6. 交互层

### 6.1 CLI 入口 `wps_cli.py` / `__main__.py`

- 解析命令行参数，支持子命令（如 `new`、`open`、`export` 等）。
- 分发到对应 `core` 模块执行。
- 支持 `python -m cli_anything.wps` 方式启动。

### 6.2 REPL 皮肤 `utils/repl_skin.py`

- 提供彩色终端输出、友好提示符、结果回显。
- 让用户在交互式会话中逐步构建文档，适合调试与教学演示。

### 6.3 Skill 定义 `skills/SKILL.md`

- 以结构化 Markdown 描述本工具的能力边界、调用方式、输入输出约定。
- 供外部 AI Agent（如 Claude Code / 各类 Skill 框架）识别并调用，实现「自然语言 → 文档」的自动生成链路。

---

## 7. 典型工作流程

以「生成一份 PPT 并导出 PNG」为例：

```
1. 初始化会话
   Session() 创建 WPS 应用实例（Kwpp.Application）

2. 新建 / 打开文档
   impress.create(size=...) 或 open(existing.pptx)

3. 套用设计预设
   apply_design_preset("预设名")

4. 逐页构建内容
   按 layout_templates 选择版式 → 填充文本 / 图片 / 图表
   （坐标精确到 pt，可完全掌控版式）

5. 质量检查
   run_quality_checks() → 得到问题清单 → 修正

6. 导出
   export.to_pdf() / export.to_png_sequence()

7. 清理
   Session 退出时自动 Quit，回收 WPS 进程
```

---

## 8. 示例项目：南科大 PPT（WPS/南科大/）

该目录是本工具的真实落地用例：

- `gen_charts.py`：先生成图表（数据可视化），产出图片资源。
- `build_sustech.py`：调用 `impress` 高层 API，套用设计预设与布局模板，把文字内容与图表资源组装成完整 PPT，并执行质量检查、导出成品。

该用例证明了工具具备「**数据 + 脚本 → 成品演示文稿**」的端到端能力。

---

## 9. 关键设计要点总结

1. **单一后端隔离**：COM 调用集中在 `wps_backend.py`，上层无 COM 依赖，便于日后扩展（如切换到 LibreOffice / python-pptx）。
2. **规范与内容解耦**：`styles/` 负责「长什么样」，`core/` 负责「放什么内容」，二者正交。
3. **质量内建**：`quality_checks.py` 让「生成即检查」成为默认流程，而非事后人工返工。
4. **面向 Agent**：通过 `SKILL.md` + CLI 双重入口，既可由人手动调用，也可被 AI Agent 作为技能驱动。
5. **资源生命周期可控**：`session.py` 以上下文管理器方式管理 WPS 进程，避免进程泄漏。
6. **多格式交付**：同一份内容可导出 PPTX / PDF / PNG 序列，满足汇报、归档、预览等不同场景。

---

## 10. 运行环境与依赖

- **操作系统**：Windows（依赖 WPS Office 的 COM 接口）。
- **WPS Office**：需已安装并支持 COM 自动化（Kwpp / Kwps / Ket）。
- **Python**：3.x，依赖 `pywin32`（`win32com`）。
- **运行方式**：
  ```bash
  # CLI 方式
  python -m cli_anything.wps <子命令> ...

  # 脚本方式
  from cli_anything.wps.core import impress, session, export
  ```

---

*（本文档基于代码结构静态分析整理，具体 API 签名以源码为准。）*
