# 第6-2课：Web界面开发 —— Streamlit 快速构建AI应用前端

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **课程阶段** | 第六周：API调用与Web应用 |
| **课程序号** | 第2课 |
| **课程主题** | Web界面开发 —— 用Streamlit为AI应用穿上"外衣" |
| **课时安排** | 1.5小时（讲授50分钟 + 实操70分钟） |
| **前置知识** | Python基础、API调用（第6-1课） |
| **适用对象** | 完成了API调用学习，希望将AI能力封装为Web应用的学员 |

---

## 二、学习目标

完成本课学习后，学员应能：

1. **理解** Streamlit 的运行模型与核心概念（脚本重运行、Session State、缓存）
2. **掌握** Streamlit 核心API，能独立搭建功能完整的Web界面
3. **实践** 构建一个完整的AI聊天机器人Web应用，包含流式输出、对话管理、配置面板等功能
4. **部署** 将Streamlit应用发布到Streamlit Cloud，生成可分享的公网链接

---

## 三、课前准备

### 3.1 环境安装

```bash
# 安装Streamlit（推荐在虚拟环境中）
pip install streamlit

# 验证安装
streamlit --version

# 额外依赖（本课聊天机器人需要）
pip install openai httpx  # openai用于调用兼容API，httpx用于HTTP请求
```

### 3.2 前置检查清单

- [ ] Python 3.8+ 已安装
- [ ] 拥有至少一个大模型API Key（OpenAI / DeepSeek / 硅基流动等）
- [ ] 能成功运行 `streamlit hello`（验证安装）
- [ ] 注册 GitHub 账号（部署环节需要）
- [ ] 基本了解命令行操作

---

## 四、核心知识点详解

### 4.1 为什么需要Web界面？

在上一课中，学员已学会通过代码调用大模型API。然而，纯代码交互存在明显局限：

- 每次使用需要修改代码或手动传参
- 无法分享给非技术用户使用
- 缺乏交互体验（无历史记录、无流式输出视觉反馈）
- 不便于调整参数、切换模型等操作

Web界面解决了以上所有问题。**Streamlit** 是Python生态中构建数据/AI应用Web界面的首选框架，它让"纯Python代码"直接转化为可交互的Web应用——无需学习HTML/CSS/JavaScript。

### 4.2 Streamlit vs Gradio 详细对比

AI开发者最常纠结的问题：**Streamlit还是Gradio？** 二者都能用纯Python构建Web UI，但定位和取舍截然不同。

| 对比维度 | Streamlit | Gradio |
|----------|-----------|--------|
| **定位** | 通用数据应用/仪表盘框架 | AI模型演示/推理接口框架 |
| **灵活性** | 高。组件布局自由组合（sidebar、columns、tabs等），适合构建完整的应用 | 中。布局相对固定，以输入→输出为核心范式，适合单一模型展示 |
| **社区规模** | GitHub 36k+ Stars，生态丰富（streamlit-aggrid、streamlit-echarts等第三方组件库） | GitHub 35k+ Stars，Hugging Face深度集成，模型演示首选 |
| **部署便捷度** | Streamlit Cloud一键部署，也支持Docker、云服务器 | Hugging Face Spaces原生支持，Gradio一键生成可分享链接 |
| **聊天支持** | `st.chat_message` + `st.chat_input` 官方原生支持（1.24+） | `gr.Chatbot` + `gr.ChatInterface` 原生支持，开发更简洁 |
| **学习曲线** | 中等。需要理解"脚本重运行"模型、Session State等概念 | 较低。API设计直观，block/interface模式容易上手 |
| **数据展示** | 强大。原生支持DataFrame、图表（内置plotly/matplotlib/vega-lite）、Metric卡片 | 较弱。数据展示非核心功能，主要服务模型输入输出 |
| **流式输出** | 需要手动实现（yield/fragments），代码量较大 | `gr.ChatInterface` 原生支持流式，开发更省力 |
| **自定义样式** | 有限。通过主题配置或CSS注入，深层次定制困难 | 有限。通过主题系统，同样受限于框架约束 |
| **适合场景** | 数据分析仪表盘、企业内部工具、完整的AI聊天应用、需要复杂布局的应用 | 模型Demo演示、Hugging Face模型展示、快速分享单功能AI应用、多输入多输出任务 |

**选择建议（本课观点）**：

- 如果你要构建**功能完整的AI聊天应用**（带侧边栏配置、对话导出、多会话管理等），选 **Streamlit**
- 如果你要**快速演示单个模型效果**（上传图片→生成描述），选 **Gradio**
- 如果**不确定选哪个**：本课程选Streamlit。因为它的灵活性在构建完整应用时优势明显，且概念可迁移（理解了Streamlit的Session State，再学Gradio的State会很容易）

### 4.3 Streamlit核心概念（深入理解）

#### 4.3.1 脚本重运行模型（Script Rerun Model）

这是理解Streamlit最关键的概念。**每一次用户与页面交互（点击按钮、输入文本、拖动滑块），Streamlit都会从头到尾重新执行整个Python脚本。** 这与你写惯的命令行脚本完全不同。

```python
# 示例：理解重运行模型
import streamlit as st

name = st.text_input("输入你的名字")  # 用户每次输入，整个脚本重跑

if st.button("打招呼"):              # 用户点击按钮，整个脚本重跑
    st.success(f"你好，{name}！")

st.write(f"当前输入框的值是：{name}")  # 每次重跑都会执行这一行
```

**关键理解：**
- 普通Python变量在每次重运行时**会被重置**（name的值之所以保留，是因为Streamlit在底层帮你管理了widget状态）
- `st.button()` 只在被点击的那一次重运行中返回True，之后立即变回False
- 这意味着你在代码中写的任何"判断逻辑"本质上都是在每次重运行时重新评估的

#### 4.3.2 Session State（会话状态）

脚本重运行意味着普通变量无法跨交互保留。**Session State** 是解决此问题的核心机制——它像一个"跨重运行的字典"。

```python
import streamlit as st

# 初始化：仅在会话开始时执行一次
if "counter" not in st.session_state:
    st.session_state.counter = 0
    st.session_state.messages = []

# 交互逻辑
if st.button("计数器+1"):
    st.session_state.counter += 1

st.metric("点击次数", st.session_state.counter)
```

**Session State的核心规则：**
- 数据存储在服务端内存中，与用户浏览器窗口的会话绑定
- 刷新页面会重置Session State
- 不同用户的Session State相互独立
- 适合存储：聊天历史、用户偏好、API调用结果、临时状态

**聊天历史的标准管理模式：**

```python
# 标准模式：初始化 + 追加
if "messages" not in st.session_state:
    st.session_state.messages = []  # 存储 {"role": "user/assistant", "content": "..."}

# 用户发送消息时
st.session_state.messages.append({"role": "user", "content": user_input})
# 助手回复时
st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
```

#### 4.3.3 缓存机制（Caching）

每次脚本重运行都完整执行，这可能导致性能问题（重复加载大文件、重复API调用）。Streamlit提供两种缓存装饰器：

| 装饰器 | 用途 | 何时数据会过期 |
|--------|------|---------------|
| `@st.cache_data` | 缓存**数据**：DataFrame、API响应、计算结果等可序列化对象 | 输入参数改变、TTL到期 |
| `@st.cache_resource` | 缓存**资源**：数据库连接、模型加载、大对象等不可/不应序列化的资源 | 通常在整个应用生命周期内有效 |

```python
import streamlit as st

@st.cache_data(ttl=3600)  # 缓存1小时
def load_large_dataset(file_path):
    """缓存大数据集加载结果"""
    return pd.read_csv(file_path)

@st.cache_resource          # 整个应用生命周期有效
def load_model():
    """缓存模型加载（加载一次，全局复用）"""
    return SomeLargeModel("model.bin")
```

**使用原则：**
- 数据加载类函数（如读取CSV、调用不频繁变化的API）用 `@st.cache_data`
- 重量级资源（ML模型、数据库连接、SDK客户端）用 `@st.cache_resource`
- 不要缓存用户输入相关的数据（那会导致不同用户看到相同数据）
- 设置合理的 `ttl`（time-to-live）确保数据新鲜度

### 4.4 Streamlit核心API大全

Streamlit的API设计遵循"一切皆组件"的哲学。以下按功能分类介绍。

#### 4.4.1 页面设置

```python
st.set_page_config(
    page_title="我的AI应用",      # 浏览器标签页标题
    page_icon="🤖",               # 浏览器标签页图标（emoji或图片路径）
    layout="wide",                # "centered"（居中窄版）| "wide"（宽版）
    initial_sidebar_state="expanded"  # 侧边栏初始状态："auto"|"expanded"|"collapsed"
)
```

**注意：** `st.set_page_config` 必须是脚本中第一个Streamlit命令（放在所有import之后，其他st调用之前），否则会报错。

#### 4.4.2 显示组件

```python
st.title("一级标题")                    # 页面主标题
st.header("二级标题")                    # 章节标题
st.subheader("三级标题")                 # 子章节标题
st.markdown("**粗体** *斜体* `代码`")    # Markdown渲染
st.write("任意内容")                     # 万能显示（自动识别数据类型）
st.text("纯文本，不渲染格式")             # 纯文本

# 消息提示
st.success("操作成功！")                 # 绿色提示
st.info("提示信息")                      # 蓝色提示
st.warning("警告信息")                   # 黄色提示
st.error("错误信息")                     # 红色提示

# 专用显示
st.code("print('hello')", language="python")  # 代码块（语法高亮）
st.dataframe(df, use_container_width=True)    # 交互式表格
st.image("photo.png", caption="图片说明")     # 图片显示
st.metric("温度", "25°C", delta="3°C")       # KPI指标卡片
st.json({"key": "value"})                    # 格式化JSON显示
st.divider()                                  # 分割线
st.latex(r"e^{i\pi} + 1 = 0")               # LaTeX公式
```

#### 4.4.3 输入组件

```python
# 文本输入
name = st.text_input("姓名", placeholder="请输入你的名字")
bio = st.text_area("自我介绍", height=150, placeholder="写点什么...")

# 选择器
role = st.selectbox("角色", ["用户", "管理员", "访客"])
tags = st.multiselect("标签", ["Python", "AI", "Web"], default=["Python"])
agree = st.checkbox("我同意服务条款")

# 数值输入
age = st.number_input("年龄", min_value=0, max_value=150, value=25)
score = st.slider("评分", 0, 100, 50)  # (最小值, 最大值, 默认值)

# 文件上传
uploaded_file = st.file_uploader("上传文件", type=["pdf", "txt", "png"])

# ⭐ 核心：按钮（每次点击触发一次重运行，那一次返回True）
if st.button("开始生成", type="primary"):
    do_something()
```

#### 4.4.4 布局组件

```python
# 侧边栏
with st.sidebar:
    st.title("配置面板")
    api_key = st.text_input("API Key", type="password")

# 多列布局
col1, col2, col3 = st.columns([2, 1, 1])  # 宽度比例
with col1:
    st.write("左侧内容（占2份宽度）")
with col2:
    st.write("中间内容（占1份宽度）")

# 标签页
tab1, tab2 = st.tabs(["对话", "设置"])
with tab1:
    st.write("对话区域")
with tab2:
    st.write("设置区域")

# 可展开区域
with st.expander("查看详情"):
    st.write("这些内容默认折叠，点击展开")

# 通用容器
container = st.container(border=True)
container.write("带边框的容器")

# 空占位符（用于后续动态更新，如流式输出）
placeholder = st.empty()
placeholder.write("这将被后续内容替换")
```

#### 4.4.5 聊天组件（AI应用最重要的部分！）

Streamlit 1.24+ 版本引入了原生聊天组件，这是构建AI对话应用的基石。

```python
# 显示聊天消息
with st.chat_message("user"):     # "user" | "assistant" | "ai" | "human"
    st.write("你好！")

with st.chat_message("assistant", avatar="🤖"):  # 可自定义头像
    st.write("你好！有什么可以帮助你的？")

# 聊天输入框（固定在页面底部）
prompt = st.chat_input("输入你的消息...")
if prompt:
    # 1. 显示用户消息
    st.chat_message("user").write(prompt)
    # 2. 调用AI生成回复
    with st.chat_message("assistant"):
        st.write(generate_response(prompt))
```

**聊天组件与Session State的配合模式（标准范式）：**

```python
# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染所有历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收新输入
if prompt := st.chat_input("请输入..."):
    # 追加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 生成并追加助手回复
    with st.chat_message("assistant"):
        response = call_llm_api(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

#### 4.4.6 状态管理与流程控制

```python
# 禁用状态（常用于等待响应期间）
button = st.button("提交", disabled=is_loading)

# 进度条
with st.spinner("AI正在思考..."):
    result = call_api()  # 耗时操作

# 状态文本
status = st.status("正在处理...", expanded=True)
status.update(label="处理完成！", state="complete")

# 弹出对话框（实验性功能）
@st.dialog("确认操作")
def confirm():
    st.write("确定要删除吗？")
    if st.button("确定"):
        st.session_state.confirmed = True
        st.rerun()

# 停止执行
st.stop()  # 通常用于条件判断后的提前退出

# 手动重运行
st.rerun()
```

### 4.5 Streamlit AI应用最佳实践

#### 4.5.1 项目结构建议

```
my-ai-app/
├── app.py              # 主入口，页面布局和交互逻辑
├── utils/
│   ├── __init__.py
│   ├── llm_client.py   # LLM API调用封装
│   └── helpers.py      # 辅助函数（格式化、导出等）
├── requirements.txt    # 依赖清单
├── .streamlit/
│   └── secrets.toml    # 本地密钥（不入Git仓库）
└── .gitignore
```

#### 4.5.2 错误处理最佳实践

```python
def safe_llm_call(messages, model, temperature):
    """带错误处理的LLM调用包装"""
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "rate" in error_msg.lower() or "429" in error_msg:
            st.error("API调用频率过高，请稍后重试。")
        elif "auth" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
            st.error("API Key无效或已过期，请检查。")
        elif "timeout" in error_msg.lower():
            st.warning("请求超时，正在重试...")
            time.sleep(2)
            return safe_llm_call(messages, model, temperature)  # 简单重试
        else:
            st.error(f"调用失败：{error_msg}")
        return None
```

#### 4.5.3 加载状态与用户体验

```python
# 原则：任何超过500ms的操作都应有加载提示
with st.spinner("正在生成回复..."):
    response = call_llm(prompt)

# 长时间操作使用进度条
progress_bar = st.progress(0)
for i, chunk in enumerate(stream_response()):
    st.write(chunk)
    progress_bar.progress((i + 1) / total_chunks)
```

#### 4.5.4 移动端响应式设计

Streamlit的布局在移动端会自动适配（columns会变为纵向堆叠），但需要注意：

- Sidebar在移动端默认折叠，重要操作不要只放在Sidebar
- 避免过宽的表格，使用 `use_container_width=True`
- 测试你的应用在手机浏览器中的表现

---

## 五、实操环节（70分钟）

### 实操1：第一个Streamlit应用（15分钟）

**目标：** 熟悉Streamlit基本开发流程，创建一个带输入的名字建议生成器。

**完整代码**（保存为 `app.py`）：

```python
import streamlit as st
import random

# ========== 页面配置 ==========
st.set_page_config(
    page_title="AI名字工坊",
    page_icon="✨",
    layout="centered"
)

# ========== 标题 ==========
st.title("✨ AI名字工坊")
st.markdown("输入你的名字，获取创意变体建议！")

# ========== 输入区 ==========
col1, col2 = st.columns([3, 1])
with col1:
    name = st.text_input("你的名字", placeholder="例如：小明")
with col2:
    language = st.selectbox("风格", ["中文创意", "English", "日系"])

# ========== 生成逻辑 ==========
suggestions_db = {
    "中文创意": ["星辰", "追风", "凌云", "沐光", "远航"],
    "English": ["Nova", "Phoenix", "Echo", "Atlas", "Orion"],
    "日系": ["ハル（春）", "ソラ（天空）", "カイト（海斗）", "レン（蓮）", "ユウキ（勇気）"]
}

if st.button("🎲 生成建议", type="primary"):
    if name:
        with st.spinner("正在为你构思..."):
            suggestion = random.choice(suggestions_db[language])
        st.success(f"{name} → **{suggestion}**")
        st.balloons()  # 彩蛋动画
    else:
        st.warning("请先输入你的名字！")

# ========== 展开：更多说明 ==========
with st.expander("💡 使用说明"):
    st.write("""
    - 输入你的名字后点击生成按钮
    - 可以选择不同的风格偏好
    - 每次生成结果随机，不满意可以再次点击
    """)

# ========== 侧边栏 ==========
with st.sidebar:
    st.header("关于")
    st.write("这是你的第一个Streamlit应用！")
    st.write(f"已生成次数：{st.session_state.get('count', 0)}")
```

**运行方式：**

```bash
cd 你的项目目录
streamlit run app.py
```

运行后浏览器自动打开 `http://localhost:8501`，修改代码保存后页面自动刷新（热重载）。

### 实操2：完整聊天机器人Web应用（45分钟）

这是本课的**核心实操**。我们将从零构建一个功能完备的AI聊天机器人Web应用。

**功能清单：**
- 侧边栏配置面板（API Key、模型提供商选择、Temperature滑块、System Prompt）
- 聊天消息显示（用户/助手头像、历史记录渲染）
- 流式输出（Typewriter效果）
- 对话导出（一键导出为Markdown文件）
- 清除历史按钮
- Token用量统计
- 错误处理（认证失败、超时、速率限制）

**完整代码**（保存为 `chatbot_app.py`）：

```python
import streamlit as st
import time
from datetime import datetime
from openai import OpenAI

# ============================================================
# 页面配置（必须是第一个Streamlit命令）
# ============================================================
st.set_page_config(
    page_title="AI 聊天助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 侧边栏 —— 配置面板
# ============================================================
with st.sidebar:
    st.title("⚙️ 配置面板")

    # ---- API配置 ----
    st.header("🔑 API 设置")
    provider = st.selectbox(
        "模型提供商",
        ["OpenAI", "DeepSeek", "硅基流动 (SiliconFlow)", "自定义兼容接口"],
        help="选择你要使用的大模型服务商"
    )

    # 根据提供商自动填充默认Base URL
    base_url_map = {
        "OpenAI": "https://api.openai.com/v1",
        "DeepSeek": "https://api.deepseek.com",
        "硅基流动 (SiliconFlow)": "https://api.siliconflow.cn/v1",
        "自定义兼容接口": ""
    }
    base_url_default = base_url_map[provider]

    api_base = st.text_input(
        "API Base URL",
        value=base_url_default,
        help="API服务端点地址，如使用自定义代理请修改此字段",
        disabled=(provider != "自定义兼容接口")
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-...",
        help="你的API密钥，仅保存在当前会话中，不会上传"
    )

    # ---- 模型选择 ----
    st.header("🧠 模型设置")
    model_options = {
        "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        "DeepSeek": ["deepseek-chat", "deepseek-reasoner"],
        "硅基流动 (SiliconFlow)": [
            "Qwen/Qwen2.5-7B-Instruct",
            "deepseek-ai/DeepSeek-V3",
            "Pro/Llama-3.3-70B-Instruct"
        ],
        "自定义兼容接口": ["gpt-3.5-turbo", "gpt-4", "claude-3-opus"]
    }
    model = st.selectbox("模型", model_options[provider])

    # ---- 参数设置 ----
    st.header("🎛️ 参数调整")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="控制回复的随机性：0=确定性强，2=创意性强"
    )
    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
        help="单次回复的最大token数"
    )

    # ---- 系统提示词 ----
    st.header("💬 系统提示词")
    system_prompt = st.text_area(
        "设定助手角色",
        value="你是一个智能助手，请用中文回答用户的问题。回答应简洁、准确、有帮助。",
        height=120,
        help="定义AI助手的行为和回复风格"
    )

    # ---- 操作按钮 ----
    st.header("🛠️ 操作")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        clear_btn = st.button("🗑️ 清除对话", use_container_width=True)
    with col_btn2:
        export_btn = st.button("📥 导出对话", use_container_width=True)

    # ---- 统计信息 ----
    st.header("📊 会话统计")
    stat_placeholder = st.empty()  # 动态更新占位符

# ============================================================
# 初始化 Session State
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0

# ============================================================
# 工具函数
# ============================================================
def build_messages(user_msg: str) -> list[dict]:
    """构建完整的消息列表（系统提示词 + 历史 + 新消息）"""
    full_messages = [{"role": "system", "content": system_prompt}]
    # 添加历史消息
    for msg in st.session_state.messages:
        full_messages.append({"role": msg["role"], "content": msg["content"]})
    # 添加当前用户消息
    full_messages.append({"role": "user", "content": user_msg})
    return full_messages


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """估算API调用费用（USD，按常见定价）"""
    pricing = {
        "gpt-4o": (2.5, 10.0),
        "gpt-4o-mini": (0.15, 0.6),
        "gpt-4-turbo": (10.0, 30.0),
        "deepseek-chat": (0.14, 0.28),
        "deepseek-reasoner": (0.55, 2.19),
    }
    input_price, output_price = pricing.get(model, (0.5, 2.0))
    cost = (prompt_tokens / 1_000_000) * input_price + (completion_tokens / 1_000_000) * output_price
    return round(cost, 6)


def export_chat():
    """导出对话为Markdown格式"""
    if not st.session_state.messages:
        return None
    md_lines = [f"# AI 对话记录\n\n> 导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n"]
    for msg in st.session_state.messages:
        role_label = "🧑 用户" if msg["role"] == "user" else "🤖 助手"
        md_lines.append(f"### {role_label}\n\n{msg['content']}\n\n---\n")
    return "\n".join(md_lines)


def handle_clear():
    """清除对话历史"""
    st.session_state.messages = []
    st.session_state.total_tokens = 0
    st.session_state.total_cost = 0.0


# ============================================================
# 操作处理：清除对话
# ============================================================
if clear_btn:
    handle_clear()
    st.rerun()

# ============================================================
# 操作处理：导出对话
# ============================================================
if export_btn:
    md_content = export_chat()
    if md_content:
        st.sidebar.download_button(
            label="⬇️ 下载对话记录",
            data=md_content,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.sidebar.warning("暂无对话内容可导出")

# ============================================================
# 更新侧边栏统计
# ============================================================
with stat_placeholder.container():
    st.metric("消息数", len(st.session_state.messages))
    st.metric("Token总用量", f"{st.session_state.total_tokens:,}")
    st.metric("预估费用", f"${st.session_state.total_cost:.4f}")

# ============================================================
# 主界面 —— 标题区
# ============================================================
st.title("🤖 AI 聊天助手")
st.markdown("基于多模型兼容接口的智能对话工具 —— 支持流式输出、对话管理和多模型切换")

# ============================================================
# 主界面 —— 历史消息渲染
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # 显示每条消息的元数据（如果有）
        if "metadata" in msg:
            with st.expander("📊 消息详情"):
                st.json(msg["metadata"])

# ============================================================
# 主界面 —— 聊天输入与响应
# ============================================================
if prompt := st.chat_input("输入你的问题，按Enter发送..."):

    # ---- 前置校验 ----
    if not api_key:
        st.error("⚠️ 请先在侧边栏配置API Key！")
        st.stop()

    if not api_base:
        st.error("⚠️ 请先配置API Base URL！")
        st.stop()

    # ---- 1. 显示用户消息 ----
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ---- 2. 调用LLM获取响应 ----
    with st.chat_message("assistant"):
        # 流式输出占位符
        response_placeholder = st.empty()
        full_response = ""

        try:
            # 初始化客户端
            client = OpenAI(api_key=api_key, base_url=api_base)

            # 发起流式请求
            with st.spinner("🤔 AI正在思考..."):
                stream = client.chat.completions.create(
                    model=model,
                    messages=build_messages(prompt),
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )

            # ---- 流式输出（Typewriter效果） ----
            chunk_count = 0
            display_buffer = ""

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    display_buffer += content

                    # 每累积5个chunk更新一次UI（平衡流畅度和性能）
                    chunk_count += 1
                    if chunk_count % 5 == 0:
                        response_placeholder.markdown(
                            display_buffer + " ▌"  # 闪烁光标效果
                        )
                        time.sleep(0.01)  # 最小延迟，确保UI更新

                # Token统计（如果有usage信息）
                if hasattr(chunk, "usage") and chunk.usage:
                    st.session_state.total_tokens += chunk.usage.total_tokens
                    cost = estimate_cost(
                        model,
                        chunk.usage.prompt_tokens,
                        chunk.usage.completion_tokens
                    )
                    st.session_state.total_cost += cost

            # 最终渲染（无光标）
            response_placeholder.markdown(full_response)

        except Exception as e:
            error_str = str(e)

            # 分类处理错误
            if "401" in error_str or "403" in error_str or "auth" in error_str.lower():
                full_response = "❌ **认证失败**：API Key无效或已过期。请检查侧边栏的API Key设置。"
            elif "429" in error_str or "rate" in error_str.lower():
                full_response = "⏳ **速率限制**：API调用过于频繁，请稍等片刻后再试。"
            elif "timeout" in error_str.lower() or "connect" in error_str.lower():
                full_response = "🌐 **连接超时**：无法连接到API服务器。请检查网络或API Base URL配置。"
            elif "insufficient_quota" in error_str.lower():
                full_response = "💳 **额度不足**：API账户余额或配额已用尽，请充值后重试。"
            else:
                full_response = f"❌ **调用出错**：\n```\n{error_str[:500]}\n```"

            response_placeholder.error(full_response)

    # ---- 3. 保存助手回复 ----
    assistant_msg = {
        "role": "assistant",
        "content": full_response,
        "metadata": {
            "model": model,
            "temperature": temperature,
            "timestamp": datetime.now().isoformat()
        }
    }
    st.session_state.messages.append(assistant_msg)

# ============================================================
# 底部信息
# ============================================================
st.divider()
st.caption(f"💡 提示：所有配置和对话数据仅保存在当前浏览器会话中。| 当前模型：{model} | Temperature：{temperature}")
```

**运行方式：**

```bash
streamlit run chatbot_app.py
```

**代码结构解读（讲师对照讲解）：**

| 代码段 | 行数 | 功能说明 |
|--------|------|----------|
| 页面配置 | 1-6 | 设置标题、图标、布局 |
| 侧边栏配置 | 7-95 | 用户可调整的所有参数 |
| Session State | 97-103 | 持久化聊天历史和统计 |
| 工具函数 | 106-140 | 封装复用逻辑 |
| 操作处理 | 143-165 | 清除和导出功能 |
| 历史渲染 | 168-174 | 恢复之前的对话显示 |
| 核心交互 | 177-270 | 用户输入→API调用→流式渲染 |

### 实操3：Streamlit Cloud部署指南（10分钟）

将应用从本地搬到云端，只需三步。

#### 步骤一：准备部署文件

在项目目录创建 `requirements.txt`：

```
streamlit>=1.28.0
openai>=1.0.0
httpx>=0.25.0
```

#### 步骤二：推送到GitHub

```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: AI Chatbot"

# 创建GitHub仓库（在GitHub网页操作）后：
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main

# 重要：确保 .streamlit/secrets.toml 在 .gitignore 中！
```

`.gitignore` 示例：

```
.streamlit/secrets.toml
__pycache__/
*.pyc
.env
.venv/
```

#### 步骤三：Streamlit Cloud部署

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用GitHub账号登录并授权
3. 点击 "New app"，选择仓库、分支（main）和主文件（`chatbot_app.py`）
4. 在 "Advanced settings" 中配置Secrets（用于存储API Key等敏感信息）
5. 点击 "Deploy!"，等待2-5分钟构建完成
6. 获得公网URL：`https://你的用户名-仓库名.streamlit.app/`

**Secrets管理：**
Streamlit Cloud通过环境变量管理密钥。在部署页面的Secrets配置中输入：

```toml
# 这将在应用中通过 st.secrets["MY_API_KEY"] 访问
# 但本课示例直接在侧边栏输入，无需此步骤
```

如需预置默认API Key（仅限教学环境）：

```toml
DEFAULT_API_KEY = "sk-xxx"
```

然后在代码中读取：`st.secrets.get("DEFAULT_API_KEY", "")`

---

## 六、课后作业

基于实操2的聊天机器人，添加以下至少三个功能（四选三）：

### 作业1：自动生成对话标题 ⭐⭐
**要求：** 当用户发送第一条消息后，调用LLM自动生成一个简洁的对话标题（如"Python爬虫技术讨论"），显示在页面顶部，替换固定的标题文字。

**提示：** 在 `st.session_state.messages` 长度变为2时（用户第1条+助手第1条回复），调用一次轻量级API生成标题，存入 `st.session_state.conversation_title`。

### 作业2：Markdown渲染优化 ⭐
**要求：** 当前代码已使用 `st.markdown()` 渲染，但在流式输出时会导致不完整的Markdown语法显示异常。改进流式输出逻辑：当检测到完整的代码块（```）配对时才渲染Code部分。

**提示：** 检查 `full_response` 中 `` ``` `` 的数量，奇数时用 `st.text()` 渲染，偶数时用 `st.markdown()` 渲染。

### 作业3：语音输入支持 ⭐⭐⭐
**要求：** 添加语音输入按钮，用户点击后通过浏览器麦克风录音，调用语音识别API（如Whisper）转文字后填入聊天输入框。

**提示：** 使用 `st.audio_input()`（Streamlit 1.35+）或 `streamlit-mic-recorder` 第三方组件；转文字可使用OpenAI Whisper API。

### 作业4：多会话管理 ⭐⭐⭐
**要求：** 侧边栏添加"新建对话"按钮和会话列表。不同会话的聊天历史独立存储（可用字典 `st.session_state.conversations = {id: [messages]}`），支持切换和删除。

**建议交付方式：** 将改进后的代码推送到GitHub并部署到Streamlit Cloud，提交应用链接。

---

## 七、拓展阅读

### 7.1 官方资源
- [Streamlit官方文档](https://docs.streamlit.io/) —— API参考和教程
- [Streamlit Chat Elements](https://docs.streamlit.io/develop/api-reference/chat) —— 聊天组件专题
- [Streamlit Cheat Sheet](https://docs.streamlit.io/develop/quick-reference/cheat-sheet) —— API速查表
- [Streamlit Gallery](https://streamlit.io/gallery) —— 社区优秀应用案例

### 7.2 进阶主题
- **Streamlit + LangChain集成**：使用 `StreamlitChatMessageHistory` 实现对话持久化
- **Data Connection**：`st.connection()` 连接数据库（MySQL、Snowflake等）
- **Custom Components**：用React/Vue开发自定义Streamlit组件（双向通信）
- **Authentication**：使用 `streamlit-authenticator` 添加用户登录功能
- **Multipage Apps**：`pages/` 目录下的多页面应用结构
- **Theming**：`.streamlit/config.toml` 自定义主题颜色和字体

### 7.3 备选框架对比学习
- **Gradio**（[gradio.app](https://gradio.app)）：更适合快速演示单个模型，`gr.ChatInterface` 一行代码构建聊天UI
- **Chainlit**（[chainlit.io](https://chainlit.io)）：专为LLM应用设计，原生支持LangChain/LlamaIndex
- **NiceGUI**（[nicegui.io](https://nicegui.io)）：基于Vue.js，自由度更高但学习成本也更高
- **Shiny for Python**（[shiny.posit.co](https://shiny.posit.co/py/)）：R Shiny的Python移植，适合统计背景用户

---

## 八、常见问题

### Q1：为什么修改代码后页面没有自动刷新？
**A：** Streamlit默认开启热重载（检测.py文件变化自动刷新）。如果失效：① 检查控制台是否报错；② 手动刷新浏览器；③ 确认 `streamlit run` 时没有加 `--server.runOnSave false` 参数。

### Q2：`st.session_state` 数据什么时候会丢失？
**A：** 三种情况：① 用户刷新浏览器页面；② Streamlit服务重启；③ 用户关闭浏览器窗口后重新打开。如需持久化，可配合 `st.connection` 或写入文件/数据库。

### Q3：流式输出为什么会"卡住"或显示不全？
**A：** 常见原因：① 网络不稳定导致流中断——添加重试逻辑；② Streamlit的渲染机制限制——增加chunk累积阈值（如前例中的每5个chunk更新一次）；③ API服务端的流式实现不标准——换用 `httpx` 库手动处理SSE流。

### Q4：部署到Streamlit Cloud后，为什么API调用失败？
**A：** 最常见的原因是**API Key没有配置**。本地开发时Key存在环境变量或直接输入，但Cloud环境没有。解决方案：① 让用户自己在页面输入（本课示例的做法，最简单）；② 在Cloud的Secrets配置中添加（适合内部工具）。

### Q5：多个用户同时访问，他们的聊天历史会互相干扰吗？
**A：** 不会。Streamlit为每个浏览器会话维护独立的 `st.session_state`。但注意 `@st.cache_resource` 是跨会话共享的（所有用户共用一个缓存实例），这是设计特性而非bug。

### Q6：Sidebar太窄了，能调整宽度吗？
**A：** Streamlit不直接提供Sidebar宽度参数，但可以通过CSS注入调整。在代码中添加：
```python
st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 350px; max-width: 500px; }
</style>
""", unsafe_allow_html=True)
```

### Q7：如何在Streamlit中使用本地模型（如Ollama）？
**A：** Ollama提供了OpenAI兼容API端点（`http://localhost:11434/v1`），因此本课代码无需修改，只需在侧边栏中：
- API Base URL 填入：`http://localhost:11434/v1`
- API Key 填入任意字符串（如 `ollama`，Ollama不验证Key）
- 模型选择：输入你本地运行的模型名（如 `llama3.2`、`qwen2.5`）

### Q8：`st.chat_input` 可以放在非底部位置吗？
**A：** 不可以。`st.chat_input()` 固定显示在页面底部，这是Streamlit的设计决定（模仿聊天应用的UX习惯）。如需灵活位置的输入框，使用 `st.text_input()` + `st.button()` 组合。

---

> **讲师备注：** 本课的核心是让学员理解"脚本重运行模型"和"Session State"，这是Streamlit区别于传统Web框架的关键思维转变。实操2的完整聊天机器人代码建议学员从头敲一遍而非复制粘贴——理解每行代码的作用比得到一个能跑的应用更重要。如果时间紧张，实操3（部署）可以作为课后任务，但务必在课堂上演示一遍部署流程的完整录屏/截图。

---

*本讲义的聊天机器人代码已完全自包含，复制到本地保存为 `.py` 文件，`pip install streamlit openai` 后即可运行。所有API Key在侧边栏手动输入，不会持久化存储，安全可控。*
