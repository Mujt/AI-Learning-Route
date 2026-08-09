# 20-LangChain与LangGraph

> **本课面向双轨受众**：💼 企业管理者/投资人 + 🎓 零基础学习者。正文为核心AI知识，📊「企业视角」框提供商业战略洞见。

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **课程名称** | AI 时代能力培养 |
| **周次** | 第 7 周：Agent 与 MCP（核心周） |
| **课次** | 第 2 课（总第 20 课） |
| **课时** | 2 小时（50 分钟讲解 + 70 分钟实操） |
| **前置知识** | Python 基础、LLM API 调用、Agent 核心概念（第 19 课） |
| **课程定位** | 从"手写 Agent Loop"到"用框架高效开发 Agent"的关键过渡课 |

---

## 二、学习目标

**💼 企业决策者**：
- 理解 LangChain/LangGraph 如何将 Agent 开发从"手写代码"变成"搭积木式组装"，评估其对研发效率的影响
- 理解 Human-in-the-Loop 模式的企业价值——它是企业Agent和Demo Agent的核心区别
- 掌握企业Agent部署的关键考量：权限边界、成本控制、审计追踪、错误升级机制
- 能评估"自建Agent vs 采购SaaS"的决策框架

---

完成本节课后，学生应能够：

1. **理解** LangChain 的核心设计理念——它解决什么问题，三大支柱是什么
2. **掌握** LangChain 的 Model（模型抽象）、Tool（工具封装）、Memory（记忆管理）三大模块
3. **独立构建** 基于 `create_tool_calling_agent` + `AgentExecutor` 的完整 Agent 应用
4. **理解** LangGraph 的状态图编排思想——为什么需要它，它比 while 循环强在哪里
5. **实现** 一个带人工审批节点的 LangGraph Agent（Human-in-the-Loop）
6. **对比** 纯 API、LangChain、LangGraph 三者的代码差异，建立技术选型判断力

---

## 三、课前准备

### 3.1 环境安装

```bash
# 核心框架
pip install langchain langchain-openai langgraph

# 可选：如果使用其他模型提供商
pip install langchain-anthropic langchain-google-genai
```

### 3.2 API Key 准备

本节课使用 DeepSeek API 作为演示（国内可用，无需科学上网，新用户有免费额度）：

- 注册地址：https://platform.deepseek.com
- 获取 API Key 后，建议设为环境变量：`export DEEPSEEK_API_KEY="your-key"`

### 3.3 前置知识检查

在开始前，请确认你已掌握第 19 课内容：

- 能解释 Agent 与聊天机器人的区别
- 能写出 Agent 核心循环（observe -> think -> act -> observe）
- 能手写 Function Calling 代码（定义工具 JSON Schema、解析 tool_calls、执行工具、将结果返回给模型）
- 理解 `max_iterations`、错误处理、对话历史管理的作用

> 如果你对以上概念还不熟悉，请先复习第 19 课《什么是 Agent》，因为本节课建立在它的基础上。

---

## 四、核心知识点详解

### 4.1 LangChain 核心概念——它到底解决了什么问题？

#### 4.1.1 从"手写一切"的痛点说起

在第 19 课中，我们手写了一个完整的 Agent Loop。回顾一下你写的代码，你会发现其中有大量**重复性、样板化的代码**：

```python
# 第 19 课中，你需要手写这些（大约 80-100 行）：
# 1. 手动定义 JSON Schema 格式的工具定义（每个工具约 20 行）
# 2. 手动维护 function name → function object 的映射字典
# 3. 手动解析 response.choices[0].message.tool_calls
# 4. 手动将 tool result 拼成 {"role": "tool", ...} 格式的消息
# 5. 手动管理 messages 列表的追加和裁剪
# 6. 手动处理 tool_calls 中嵌套的参数 JSON 解析
# 7. 手动实现 max_steps、错误处理等控制逻辑
```

当一个项目有 4 个工具时，这些代码就已经超过 150 行。当项目扩展为 20 个工具、需要记忆管理、需要支持多种 LLM 提供商时，手写的维护成本会急剧上升。

**LangChain 的核心价值：把这些重复性工作标准化、组件化。**

> 📊 **企业视角：LangChain/LangGraph = Agent 开发的"乐高积木"**
>
> 对企业而言，这意味着 Agent 开发从"从零手写代码"变成"搭积木式组装"。传统方式开发一个企业级 Agent 需要2-4名工程师投入1-3个月，使用 LangChain/LangGraph 后，开发周期通常缩短到2-4周。
>
> **企业开发成本对比**：
>
> | 开发方式 | 开发周期 | 人力投入 | 维护成本 | 灵活性 |
> |---------|:-------:|:-------:|:-------:|:-----:|
> | 纯手写 API | 1-3个月 | 2-4人 | 高（代码散落各处） | 最高 |
> | LangChain Agent | 2-4周 | 1-2人 | 中（框架标准化） | 中高 |
> | LangGraph Agent | 3-6周 | 2-3人 | 中低（图结构清晰） | 最高（可自定义流程） |
>
> **核心建议**：企业起步阶段用 LangChain Agent（快速验证），当需要条件分支、人工审批、并行执行时升级到 LangGraph。不要一开始就用 LangGraph——过度设计是早期Agent项目失败的主因之一。

#### 4.1.2 LangChain 的三大支柱

```
┌─────────────────────────────────────────────────────────┐
│                    LangChain 三大支柱                     │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐ │
│  │      Model       │  │      Tool       │  │  Memory  │ │
│  │     (模型抽象)    │  │    (工具抽象)    │  │ (记忆管理) │ │
│  ├─────────────────┤  ├─────────────────┤  ├──────────┤ │
│  │ · 统一多提供商接口│  │ · @tool 装饰器   │  │ · 短期记忆 │ │
│  │ · Prompt 模板    │  │ · 自动Schema生成 │  │ · 摘要记忆 │ │
│  │ · 结构化输出     │  │ · BaseTool 类    │  │ · 滑动窗口 │ │
│  │ · 流式输出       │  │ · Tool 组合      │  │ · 长期记忆 │ │
│  └─────────────────┘  └─────────────────┘  └──────────┘ │
│                                                         │
│              ↓ 三者在 Agent 中协作 ↓                     │
│                                                         │
│   Model 负责"思考" → Tool 负责"执行" → Memory 负责"记忆" │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**一句话理解三者关系**：
- **Model** = Agent 的大脑（理解用户意图，决定做什么）
- **Tool** = Agent 的双手（执行具体操作：计算、搜索、发邮件）
- **Memory** = Agent 的海马体（记住说过的话，跨轮次保持上下文）

---

### 4.2 Model（模型抽象）——一套代码，切换所有模型

#### 4.2.1 LLM vs ChatModel

LangChain 区分两种模型类型：

| 类型 | 输入 | 输出 | 代表 |
|------|------|------|------|
| **LLM** | 纯文本字符串 | 纯文本字符串 | 旧版 text-davinci-003, GPT-3 |
| **ChatModel** | 消息列表（SystemMessage, HumanMessage, AIMessage...） | 消息对象 | GPT-4, Claude, DeepSeek, Qwen |

> **重要**：现代大模型几乎都是 ChatModel。你在 LangChain 中 99% 的情况下使用的都是 ChatModel。`ChatOpenAI` 虽然名字里带 OpenAI，但它通过 `base_url` 参数可以连接任何兼容 OpenAI API 格式的服务（DeepSeek、Qwen、vLLM 等）。

#### 4.2.2 统一接口——切换模型只需改一行

这是 LangChain 最强大的特性之一：无论底层是 OpenAI、DeepSeek、通义千问还是本地模型，调用接口完全一致。

```python
from langchain_openai import ChatOpenAI
import os

# ============================================
# 示例 1：连接 DeepSeek
# ============================================
llm_deepseek = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 或直接写字符串
    base_url="https://api.deepseek.com",
    temperature=0.3,    # 0=确定，1=创造
    max_tokens=2000,    # 最大输出长度
)

# ============================================
# 示例 2：连接通义千问（阿里云百炼）
# ============================================
llm_qwen = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.3,
)

# ============================================
# 示例 3：连接本地 vLLM 或 Ollama
# ============================================
llm_local = ChatOpenAI(
    model="qwen2.5:7b",            # Ollama 中的模型名
    api_key="not-needed",           # 本地模型不需要 Key
    base_url="http://localhost:11434/v1",  # Ollama 默认地址
    temperature=0.3,
)

# ============================================
# 三种模型，同一套调用方式
# ============================================
for name, llm in [("DeepSeek", llm_deepseek), ("Qwen", llm_qwen), ("Local", llm_local)]:
    try:
        response = llm.invoke("用一句话解释什么是 LangChain")
        print(f"{name}: {response.content[:80]}...")
    except Exception as e:
        print(f"{name}: 连接失败 - {e}")
```

**调用方式的统一**：

```python
# 方式1：invoke — 同步单次调用
response = llm.invoke("你好")
print(response.content)

# 方式2：ainvoke — 异步调用（适合 FastAPI/高并发场景）
response = await llm.ainvoke("你好")

# 方式3：stream — 流式输出（逐 token 返回，适合前端实时展示）
for chunk in llm.stream("写一首关于AI的诗"):
    print(chunk.content, end="", flush=True)

# 方式4：batch — 批量调用（自动并行）
responses = llm.batch(["问题1", "问题2", "问题3"])
```

#### 4.2.3 Prompt Templates——让 Prompt 工程化

手写 Prompt 的问题是：变量需要手动拼接，容易出错，不方便复用。LangChain 提供了结构化的 Prompt Template：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

# ============================================
# 示例 1：简单模板（单轮对话）
# ============================================
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，专长是{specialty}。用{language}回复。"),
    ("human", "{user_input}"),
])

# 填充模板 → 生成实际的消息列表
messages = simple_prompt.format_messages(
    role="Python 编程导师",
    specialty="代码调试和性能优化",
    language="中文",
    user_input="list 和 tuple 有什么区别？"
)
print(messages)
# 输出：
# [SystemMessage(content='你是一个Python 编程导师，专长是代码调试和性能优化。用中文回复。'),
#  HumanMessage(content='list 和 tuple 有什么区别？')]

# 用模板调用模型
response = llm_deepseek.invoke(messages)
print(response.content)

# ============================================
# 示例 2：带对话历史的模板（多轮对话）
# ============================================
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI助手，名字叫小智。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 历史消息插槽
    ("human", "{user_input}"),
])

# 维护对话历史
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [
    HumanMessage(content="我叫张三"),
    AIMessage(content="你好张三！很高兴认识你。有什么可以帮你的？"),
]

# 新一轮调用
messages = chat_prompt.format_messages(
    chat_history=chat_history,
    user_input="我叫什么名字？"
)
response = llm_deepseek.invoke(messages)
print(response.content)  # 应该能回答"张三"

# ============================================
# 示例 3：Agent 专用模板（含 agent_scratchpad）
# ============================================
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，可以使用工具完成任务。"),
    MessagesPlaceholder(variable_name="chat_history"),   # 对话历史
    ("human", "{input}"),                                 # 用户输入
    MessagesPlaceholder(variable_name="agent_scratchpad"), # Agent 中间推理空间
])
# agent_scratchpad 是 Agent 存放工具调用和结果的"草稿纸"，
# LangChain 的 AgentExecutor 会自动管理它，你不需要手动填充。
```

#### 4.2.4 结构化输出——让模型返回 JSON

很多时候你需要模型返回结构化的数据，而不是自然语言文本：

```python
from typing import List, Optional
from pydantic import BaseModel, Field

# 定义你想要的输出结构
class CourseInfo(BaseModel):
    """课程信息结构"""
    course_name: str = Field(description="课程名称")
    teacher: str = Field(description="授课教师")
    time: str = Field(description="上课时间，格式如'每周二14:00'")
    location: str = Field(description="上课地点")
    credits: int = Field(description="学分")
    tags: List[str] = Field(description="课程标签")

# 使用 with_structured_output
structured_llm = llm_deepseek.with_structured_output(CourseInfo)

result = structured_llm.invoke(
    "Python数据分析课程，王教授教，每周四上午9点到11点半，"
    "在实验楼B301，3个学分，教Pandas和Matplotlib"
)

print(f"课程名: {result.course_name}")
print(f"教师: {result.teacher}")
print(f"时间: {result.time}")
print(f"地点: {result.location}")
print(f"学分: {result.credits}")
print(f"标签: {result.tags}")
# 输出是 CourseInfo 对象，不是字符串！
```

> **注意**：`with_structured_output` 底层使用的是模型的 Function Calling 能力或 JSON Mode。不是所有模型都支持，使用前请确认你的模型支持该功能。

---

### 4.3 Tool（工具抽象）——一行装饰器定义工具

#### 4.3.1 @tool 装饰器：最简单的方式

在第 19 课中，你需要写约 20 行 JSON Schema 来定义一个工具。LangChain 的 `@tool` 装饰器让你只需要写函数 + 文档字符串：

```python
from langchain.tools import tool
import datetime
import math

# ============================================
# 工具 1：获取当前时间
# ============================================
@tool
def get_current_time() -> str:
    """获取当前日期和时间，包括年月日、时分秒和星期几。当你需要知道"现在几点"时使用。"""
    now = datetime.datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[now.weekday()]
    return f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}"

# ============================================
# 工具 2：数学计算器
# ============================================
@tool
def calculate(expression: str) -> str:
    """执行数学计算。支持加减乘除、括号、幂运算和三角函数。
    
    Args:
        expression: 数学表达式，例如 "(128 + 256) * 3.5 / 7" 或 "math.sin(0.5)"
    """
    # 安全注意：eval 在生产环境应替换为更安全的方案（如 numexpr 或白名单 AST 解析）
    allowed_names = {
        "math": math,
        "abs": abs, "round": round,
        "min": min, "max": max, "sum": sum
    }
    try:
        # 使用受限的命名空间执行计算
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错：{e}。请检查表达式是否正确。"

# ============================================
# 工具 3：模拟天气查询
# ============================================
@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气情况。
    
    Args:
        city: 城市名称，例如 "北京"、"上海"、"深圳"
    """
    # 模拟数据（实际项目中换成天气 API）
    weather_data = {
        "北京": "晴，25°C，湿度40%，北风3级",
        "上海": "多云，28°C，湿度65%，东南风2级",
        "深圳": "阵雨，30°C，湿度80%，西南风4级",
        "杭州": "阴，22°C，湿度55%，东北风2级",
        "成都": "晴转多云，26°C，湿度50%，微风",
    }
    return weather_data.get(
        city,
        f"暂未收录'{city}'的天气数据。目前支持的城市：{', '.join(weather_data.keys())}"
    )

# ============================================
# 工具 4：模拟文件搜索
# ============================================
@tool
def search_file(keyword: str) -> str:
    """在当前项目目录中搜索包含指定关键词的文件。
    
    Args:
        keyword: 要搜索的关键词，例如 "课程"、"作业"、"Python"
    """
    import os
    import glob
    
    # 在当前目录及子目录搜索所有 .md .py .txt 文件
    patterns = ["**/*.md", "**/*.py", "**/*.txt"]
    found = []
    
    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if keyword.lower() in content.lower() or keyword.lower() in filepath.lower():
                        found.append(filepath)
            except Exception:
                pass  # 跳过无法读取的文件
    
    if not found:
        return f"未找到包含'{keyword}'的文件。"
    
    result = f"找到 {len(found)} 个包含'{keyword}'的文件：\n"
    for f in found[:10]:  # 最多显示 10 个
        result += f"  · {f}\n"
    if len(found) > 10:
        result += f"  ... 还有 {len(found) - 10} 个文件未显示\n"
    return result
```

**@tool 装饰器做了什么？**

当你用 `@tool` 装饰一个函数时，LangChain 自动完成：

1. 从函数名提取 `name`（工具名称）
2. 从 docstring 提取 `description`（工具描述——这是给 LLM 看的，决定 LLM 何时调用此工具）
3. 从类型注解和 docstring 中的 `Args:` 段落提取 `args_schema`（参数 JSON Schema）
4. 将 Python 函数包装为 `BaseTool` 的子类实例

**手动验证工具定义**：

```python
# 查看自动生成的工具描述
print(f"工具名称: {get_weather.name}")
print(f"工具描述: {get_weather.description}")
print(f"参数定义: {get_weather.args}")
# 输出：
# 工具名称: get_weather
# 工具描述: 查询指定城市的当前天气情况。...
# 参数定义: {'city': {'title': 'City', 'type': 'string'}}
```

**可以查看最终发给 LLM 的工具定义**：

```python
# 转换为 OpenAI Function Calling 格式
print(get_weather.to_openai_function())
# 输出：
# {'name': 'get_weather',
#  'description': '查询指定城市的当前天气情况。...',
#  'parameters': {'properties': {'city': {'title': 'City', 'type': 'string'}},
#   'required': ['city'], 'type': 'object'}}
```

#### 4.3.2 Tool vs 手动 Function Calling

| 对比维度 | 手动 Function Calling | LangChain @tool |
|----------|----------------------|-----------------|
| **定义方式** | JSON Schema 字典（~20行/工具） | Python 函数 + docstring（~5行/工具） |
| **参数验证** | 需手动实现 | 基于类型注解自动验证 |
| **工具发现** | 手动维护 `available_functions` 字典 | `tools` 列表统一管理 |
| **错误处理** | 手动 try/except | 框架层统一处理 |
| **可复用性** | 低（散落在各处的 JSON） | 高（标准化的 Tool 对象） |
| **直接调用** | `func(**args)` | `tool.invoke(args)` 或 `tool.run(args)` |

**直接调用工具的两种方式**：

```python
# 方式 1：invoke — 传入字典
result = get_weather.invoke({"city": "北京"})
print(result)  # 晴，25°C，湿度40%，北风3级

# 方式 2：run — 传入关键字参数（更 Pythonic）
result = get_weather.run(city="杭州")
print(result)  # 阴，22°C，湿度55%，东北风2级
```

#### 4.3.3 自定义更复杂的 Tool

如果 `@tool` 装饰器不够用（比如需要自定义 JSON Schema 细节），可以使用 `StructuredTool`：

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# 自定义参数 Schema
class ReminderInput(BaseModel):
    task: str = Field(description="提醒事项的内容")
    time_str: str = Field(description="提醒时间，格式如'2026-07-27 15:00'")
    priority: str = Field(
        default="普通",
        description="优先级：紧急/重要/普通（默认：普通）"
    )

def set_reminder_func(task: str, time_str: str, priority: str = "普通") -> str:
    """设置一个提醒事项。"""
    # 实际项目中写入数据库或日历
    return f"✅ 已设置{priority}优先级提醒：'{task}' - {time_str}"

set_reminder = StructuredTool.from_function(
    func=set_reminder_func,
    name="set_reminder",
    description="设置一个提醒事项。支持设置优先级（紧急/重要/普通）。",
    args_schema=ReminderInput,
)
```

---

### 4.4 Memory（记忆管理）——让 Agent 记住对话

没有记忆的 Agent 就像患了失忆症——每次对话都忘记之前说了什么。LangChain 提供了多种记忆策略。

#### 4.4.1 ConversationBufferMemory —— 最基础的记忆

记住整个对话历史，原封不动。

```python
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

# 创建记忆
memory = ConversationBufferMemory(
    return_messages=True,  # 返回 Message 对象而非字符串
    memory_key="chat_history",  # 在 Prompt 模板中引用的变量名
)

# 模拟对话
memory.chat_memory.add_user_message("我叫张三，今年20岁")
memory.chat_memory.add_ai_message("你好张三！记住了，你今年20岁。有什么可以帮你的？")

memory.chat_memory.add_user_message("我学工程设计专业")
memory.chat_memory.add_ai_message("工程设计专业很棒！已记录。")

# 查看记忆内容
print(memory.load_memory_variables({}))
# {'chat_history': [HumanMessage(...), AIMessage(...), HumanMessage(...), AIMessage(...)]}

# 验证 Agent 能"记住"：
messages = chat_prompt.format_messages(
    chat_history=memory.load_memory_variables({})["chat_history"],
    user_input="我叫什么名字？什么专业？"
)
response = llm_deepseek.invoke(messages)
print(response.content)
# 应该能回答：你叫张三，学工程设计专业，今年20岁。
```

**优点**：简单直接，不会丢失任何信息。
**缺点**：对话长了之后 token 消耗极大（每次都要把全部历史发给模型）。

#### 4.4.2 ConversationSummaryMemory —— 摘要记忆

当对话变长时，自动对历史对话生成摘要，只保留摘要而非完整历史。

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# 摘要记忆需要一个 LLM 来做摘要
summary_memory = ConversationSummaryMemory(
    llm=llm_deepseek,
    return_messages=True,
    memory_key="chat_history",
    max_token_limit=500,  # 摘要最大 token 数
)

# 模拟多轮对话
summary_memory.chat_memory.add_user_message(
    "我想制定一个为期4周的Python学习计划，每天大约2小时。"
)
summary_memory.chat_memory.add_ai_message(
    "好的！第1周：基础语法（变量、循环、函数）→ "
    "第2周：数据结构与文件操作 → 第3周：面向对象与模块 → "
    "第4周：项目实战（做一个命令行工具）。每天2小时分为：1小时学习+1小时练习。"
)
summary_memory.chat_memory.add_user_message(
    "第1周具体每天学什么？"
)
summary_memory.chat_memory.add_ai_message(
    "周一：安装Python+Jupyter，Hello World，变量与数据类型；"
    "周二：条件判断与循环；周三：函数定义与参数；"
    "周四：列表与字典；周五：综合练习——写一个通讯录程序。"
)

# 查看记忆——此时底层已经自动将长对话压缩为摘要了
history = summary_memory.load_memory_variables({})
print(history["chat_history"])
# 输出类似：
# [SystemMessage(content='用户想要一个4周Python学习计划，每天2小时。
#   助手给出了4周大纲。用户追问第1周细节，助手给出了每天的具体内容。')]
```

**优点**：节省大量 token，适合长对话。
**缺点**：摘要可能丢失细节信息（比如第1周第3天学什么）。对于需要精确回忆细节的场景不够可靠。

#### 4.4.3 ConversationBufferWindowMemory —— 滑动窗口记忆

只保留最近的 K 轮对话，像"滑动窗口"。

```python
from langchain.memory import ConversationBufferWindowMemory

window_memory = ConversationBufferWindowMemory(
    return_messages=True,
    memory_key="chat_history",
    k=3,  # 只保留最近 3 轮对话
)

# 模拟 5 轮对话
for i in range(5):
    window_memory.chat_memory.add_user_message(f"第{i+1}轮用户消息")
    window_memory.chat_memory.add_ai_message(f"第{i+1}轮AI回复")

history = window_memory.load_memory_variables({})
print(f"记忆中的轮数: {len(history['chat_history'])}")  # 6 条消息 = 3 轮
# 只保留了最近 3 轮（第 3、4、5 轮）
for msg in history["chat_history"]:
    print(f"  {msg.content}")
```

**优点**：控制 token 消耗上限，始终保留最近的对话上下文。
**缺点**：更早的信息会永久丢失。

#### 4.4.4 三种记忆策略对比

| 策略 | Token 消耗 | 信息保留 | 最佳场景 |
|------|-----------|---------|---------|
| **BufferMemory** | 高（无上限） | 完整保留所有历史 | 短对话（<10轮）、客服机器人 |
| **SummaryMemory** | 低（固定上限） | 保留概要，丢失细节 | 长对话、研究助手、学习伙伴 |
| **WindowMemory** | 中（可控） | 保留最近K轮，丢失早期 | 需要最近上下文的场景（如代码审查） |

> **实践建议**：
> - 初期用 **BufferMemory**，简单可靠。当发现 token 成本过高时再切换到 Summary 或 Window。
> - 可以组合使用：比如用 Window 保留最近 3 轮的完整对话 + Summary 保留更早历史的摘要。

---

### 4.5 Agent 构建（LangChain 方式）——真正的"AI 秘书"

#### 4.5.1 create_tool_calling_agent —— 现代方式

LangChain 的 Agent 构建 API 经历了几次迭代。当前推荐使用 `create_tool_calling_agent`（基于模型的 Function Calling 能力），它比旧的 ReAct Agent 更简洁、更可靠。

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

# 核心：一行创建 Agent
agent = create_tool_calling_agent(
    llm=llm_deepseek,      # 思考大脑
    tools=tools,            # 工具箱
    prompt=agent_prompt,    # 提示词模板（含 agent_scratchpad）
)

# AgentExecutor：运行 Agent 的执行引擎
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                   # 打印详细的执行过程（调试用）
    max_iterations=10,              # 最多执行 10 轮工具调用
    handle_parsing_errors=True,     # 模型输出异常时自动重试
    return_intermediate_steps=False, # True=返回中间步骤，适合调试
    early_stopping_method="generate", # 达到 max_iterations 时的行为
)
```

**AgentExecutor 的关键参数说明**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `verbose` | `False` | 打印 Agent 的思考过程和工具调用详情 |
| `max_iterations` | `15` | 最大工具调用轮数（不是对话轮数） |
| `handle_parsing_errors` | `False` | 模型输出无法解析时是否自动重试 |
| `max_execution_time` | `None` | 最大执行时间（秒），适合线上服务做超时保护 |
| `early_stopping_method` | `"force"` | 达到上限时：`"force"`=强制返回，`"generate"`=让模型总结 |

#### 4.5.2 完整"AI 秘书"Agent

下面是完整的可运行代码，将 Model、Tool、Memory 三者整合为一个实用的 AI 秘书。

```python
# ============================================================
# ai_secretary.py — 完整的 LangChain AI 秘书
# 安装：pip install langchain langchain-openai
# 运行：python ai_secretary.py
# ============================================================

import datetime
import math
import os
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# ============================================================
# 第 1 步：定义模型（支持多种 LLM 提供商）
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),
    base_url="https://api.deepseek.com",
    temperature=0.3,
    max_tokens=2000,
)

# ============================================================
# 第 2 步：定义工具
# ============================================================

@tool
def get_current_time() -> str:
    """获取当前精确的日期和时间，包括年月日、时分秒和星期几。
    当用户询问时间、日期、星期时使用此工具。"""
    now = datetime.datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekdays[now.weekday()]}"

@tool
def calculate(expression: str) -> str:
    """执行数学计算。支持加减乘除、括号、幂运算、三角函数。
    
    Args:
        expression: 数学表达式字符串，例如 "(128 + 256) * 3.5 / 7"
    """
    allowed_names = {
        "math": math, "abs": abs, "round": round,
        "min": min, "max": max, "sum": sum,
        "pow": pow, "sqrt": math.sqrt, "pi": math.pi,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算出错：{e}"

@tool
def search_course(keyword: str) -> str:
    """搜索课程信息。根据关键词查找相关课程的时间、地点和教师信息。
    
    Args:
        keyword: 课程关键词，例如 "Python"、"机器学习"、"深度学习"、"Agent"
    """
    courses = {
        "python": "Python基础课程 | 王建国教授 | 每周二 14:00-16:30 | 实验室301",
        "机器学习": "机器学习课程 | 李明教授 | 每周四 09:00-11:30 | 教学楼B201",
        "深度学习": "深度学习课程 | 张华教授 | 每周五 15:00-17:30 | 实验室201",
        "agent": "AI Agent开发 | 陈思州讲师 | 每周三 10:00-12:00 | 在线课程(腾讯会议)",
        "数据分析": "Python数据分析 | 赵敏副教授 | 每周一 14:00-16:30 | 实验楼A102",
        "设计思维": "工程设计思维 | 钱伟教授 | 每周三 13:30-16:00 | 教学楼C304",
    }
    for key, value in courses.items():
        if keyword.lower() in key.lower():
            return f"📚 找到课程：\n{value}"
    return f"未找到与'{keyword}'相关的课程。可尝试搜索：Python、机器学习、深度学习、Agent、数据分析、设计思维"

@tool
def set_reminder(task: str, time_str: str) -> str:
    """设置一个提醒事项。帮助你记住重要的任务和截止时间。
    
    Args:
        task: 提醒事项的内容描述
        time_str: 提醒时间，例如 "明天下午3点"、"2026-07-27 15:00"
    """
    # 实际项目中：写入数据库、发送日历邀请、对接钉钉/飞书等
    return f"✅ 已成功设置提醒！\n📌 事项：{task}\n⏰ 时间：{time_str}\n💡 届时我会提醒你。"

# ============================================================
# 第 3 步：组装工具列表
# ============================================================
tools = [get_current_time, calculate, search_course, set_reminder]

# ============================================================
# 第 4 步：创建 Prompt 模板（RCTE 框架）
# ============================================================
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的 AI 秘书，名字叫"小智"。

## 你的能力
你可以使用以下工具来帮助用户：
- **时间查询**：获取当前日期、时间和星期
- **数学计算**：执行各种数学运算（支持三角函数、幂运算等）
- **课程查询**：搜索课程信息（时间、地点、教师）
- **提醒设置**：为用户创建提醒事项

## 工作原则
1. 主动使用工具完成任务，不要猜测你不知道的信息
2. 如果需要多个步骤，一步步来，不要省略中间环节
3. 如果工具返回的信息不足，告知用户并提供建议
4. 用友好、简洁的中文回复
5. 设置提醒等关键操作完成后，明确告知用户结果

## 当前时间上下文
当前日期在 2026 年 7 月左右，学期在暑假期间。"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# ============================================================
# 第 5 步：创建 Agent 和 AgentExecutor
# ============================================================
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=agent_prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                # 设为 True 可看到详细的工具调用过程
    max_iterations=10,
    handle_parsing_errors=True,
    return_intermediate_steps=False,
)

# ============================================================
# 第 6 步：对话管理（手动管理记忆）
# ============================================================
class AISecretary:
    """AI 秘书对话管理类"""
    
    def __init__(self, executor, max_history=20):
        self.executor = executor
        self.chat_history = []       # 对话历史（HumanMessage + AIMessage）
        self.max_history = max_history  # 最多保留多少条消息
    
    def chat(self, user_input: str) -> str:
        """处理一轮对话"""
        # 调用 Agent
        result = self.executor.invoke({
            "input": user_input,
            "chat_history": self.chat_history,
        })
        
        # 更新对话历史
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=result["output"]))
        
        # 控制历史长度（保留最近的消息，避免 token 爆炸）
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]
        
        return result["output"]
    
    def clear_history(self):
        """清空对话历史"""
        self.chat_history = []
        print("🗑️  对话历史已清空。")

# ============================================================
# 第 7 步：运行测试
# ============================================================
if __name__ == "__main__":
    secretary = AISecretary(agent_executor)
    
    print("=" * 60)
    print("  🤵 AI 智能秘书 —— 小智")
    print("  输入 'quit' 退出 | 'clear' 清空记忆")
    print("=" * 60)
    
    # 预设测试任务
    test_tasks = [
        "现在几点了？",
        "帮我算一下 (128 + 256) * 3.5 / 7 等于多少",
        "Python课什么时候上？在哪里上？",
        "帮我设置一个提醒：明天下午3点交机器学习作业",
    ]
    
    print("\n📋 自动测试模式：\n")
    for task in test_tasks:
        print(f"{'─' * 50}")
        print(f"🙋 用户：{task}")
        response = secretary.chat(task)
        print(f"🤵 小智：{response}")
    
    # 测试记忆——Agent 应该记得之前说过什么
    print(f"\n{'─' * 50}")
    print("🙋 用户：我刚才一共问了几个问题？分别是什么？")
    response = secretary.chat("我刚才一共问了几个问题？分别是什么？")
    print(f"🤵 小智：{response}")
    
    # 如果需要进入交互模式，取消下面的注释：
    # while True:
    #     try:
    #         user_input = input("\n🙋 你：")
    #         if user_input.lower() == 'quit':
    #             print("👋 再见！")
    #             break
    #         if user_input.lower() == 'clear':
    #             secretary.clear_history()
    #             continue
    #         response = secretary.chat(user_input)
    #         print(f"🤵 小智：{response}")
    #     except KeyboardInterrupt:
    #         print("\n👋 再见！")
    #         break
```

**运行效果解读**：

当用户问"Python课什么时候上？在哪里上？"，你会看到：
1. Agent 决定调用 `search_course` 工具，参数 `keyword="Python"`
2. 工具返回课程信息
3. Agent 基于工具结果生成友好回复
4. 对话历史自动更新（支持后续的多轮对话）

当用户问"帮我设置一个提醒"，Agent 会：
1. 解析用户意图
2. 调用 `set_reminder` 工具，提取 task 和 time_str
3. 返回确认信息

#### 4.5.3 流式输出（Streaming）

对于需要实时反馈的场景（如 Web 聊天界面），可以使用流式输出：

```python
# 流式 Agent 输出
def stream_chat(secretary, user_input):
    """流式对话——适合 Web 前端实时展示"""
    for chunk in agent_executor.stream({
        "input": user_input,
        "chat_history": secretary.chat_history,
    }):
        # chunk 包含当前步骤的输出
        if "output" in chunk:
            # 最终输出（逐 token 理论上需要更深层的 stream 支持）
            print(chunk["output"], end="", flush=True)
        elif "actions" in chunk:
            # 工具调用
            for action in chunk["actions"]:
                print(f"\n🔧 [调用工具: {action.tool}]", end="")
        elif "steps" in chunk:
            # 工具结果
            for step in chunk["steps"]:
                print(f"\n📊 [工具结果: {str(step.observation)[:100]}...]", end="")
```

> **注意**：真正的逐 token 流式输出需要模型支持 streaming（通过 `llm.bind_tools(tools)` 配合 `streaming=True` 实现），AgentExecutor 的 `stream` 方法流式返回的是"步骤"级别而非"token"级别。

---

### 4.6 LangGraph —— 状态图编排，超越简单的 while 循环

#### 4.6.1 为什么需要 LangGraph？

前面我们用 AgentExecutor 构建的 Agent，底层是一个 **while 循环**：

```
while step < max_iterations:
    response = llm.invoke(messages)  # 思考
    if no tool_calls:
        break                        # 完成
    execute_tools(response.tool_calls)  # 执行
```

这种线性循环有几个局限：

| 局限 | 说明 | 真实需求 |
|------|------|---------|
| **无法分支** | 只能"思考→工具→思考→工具→..."线性循环 | 需要根据条件走不同分支 |
| **无法并行** | 工具只能串行执行 | 查天气和查课程可以同时进行 |
| **无法暂停** | 一旦启动必须跑到结束 | 危险操作需要人工审批 |
| **无法恢复** | 出错后只能从头开始 | 长任务中断后应从断点继续 |
| **不可观测** | 中间状态难以追踪 | 需要知道每一步发生了什么 |

**LangGraph 的核心思想：用"图"来描述 Agent 的执行流程。**

```
LangChain AgentExecutor (while 循环):
  ┌──────────┐
  │  Agent   │ ←──→ Tools
  └──────────┘
  线性的、无法自定义的循环

LangGraph Agent (状态图):
         ┌──────────┐
         │  思考    │
         └────┬─────┘
              │
         ┌────▼─────┐
         │ 条件判断  │──── 无工具调用 ────→ [结束]
         └────┬─────┘
              │ 有工具调用
         ┌────▼─────┐
         │ 人工审批  │──── 拒绝 ────→ [结束]
         └────┬─────┘
              │ 批准
         ┌────▼─────┐
         │ 执行工具  │
         └────┬─────┘
              │
         ┌────▼─────┐
         │  思考    │ ←── 循环
         └──────────┘
  可控的、可自定义的图
```

#### 4.6.2 LangGraph 核心概念

```
LangGraph 的四个核心概念：

1. State（状态）
   - 在节点之间传递的数据
   - 通常是一个 TypedDict 或 Pydantic 模型
   - 包含 messages、中间结果、标志位等

2. Nodes（节点）
   - 执行具体逻辑的函数
   - 接收 State，返回 State 的更新
   - 例如：agent_node（思考）、tool_node（执行工具）、human_approval_node（审批）

3. Edges（边）
   - 固定连线：从节点 A 到节点 B，无条件
   - 条件边：根据 State 的值决定去哪个节点

4. Conditional Edges（条件边）
   - 最关键的概念
   - 根据当前 State 的值，动态决定下一步去哪个节点
   - 实现分支、循环、人工审批等复杂逻辑
```

#### 4.6.3 StateGraph 实战：构建第一张图

先从一个最简单的例子开始理解 StateGraph：

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 第 1 步：定义状态
class SimpleState(TypedDict):
    counter: int
    message: str

# 第 2 步：定义节点函数
def increment(state: SimpleState) -> dict:
    """将 counter 加 1"""
    new_count = state["counter"] + 1
    return {"counter": new_count, "message": f"计数: {new_count}"}

def double(state: SimpleState) -> dict:
    """将 counter 翻倍"""
    return {"counter": state["counter"] * 2}

# 第 3 步：定义条件函数（决定下一步去哪）
def should_continue(state: SimpleState) -> str:
    """如果 counter < 5，继续；否则结束"""
    if state["counter"] < 5:
        return "increment"  # 继续自增
    return END              # 结束

# 第 4 步：构建图
builder = StateGraph(SimpleState)

# 添加节点
builder.add_node("increment", increment)
builder.add_node("double", double)

# 设置入口
builder.set_entry_point("increment")

# 添加条件边
builder.add_conditional_edges(
    "increment",        # 从 increment 节点出发
    should_continue,    # 条件判断函数
    {
        "increment": "increment",  # 如果返回 "increment" → 回到 increment
        END: END,                  # 如果返回 END → 结束
    }
)
# 添加固定边（可选，这里暂不用）
# builder.add_edge("increment", "double")

# 第 5 步：编译并运行
graph = builder.compile()

result = graph.invoke({"counter": 1, "message": ""})
print(f"最终 counter: {result['counter']}")   # 5
print(f"最终 message: {result['message']}")   # 计数: 5
# 执行过程：counter 1→2→3→4→5，达到 5 后条件判断返回 END
```

#### 4.6.4 ToolNode：预置的工具执行节点

LangGraph 提供了 `ToolNode`，它自动处理工具调用的执行：

```python
from langgraph.prebuilt import ToolNode

# ToolNode 自动：
# 1. 从最后一条 AIMessage 中提取 tool_calls
# 2. 执行对应的工具函数
# 3. 将结果包装为 ToolMessage
# 4. 返回给下一个节点
tool_node = ToolNode(tools)  # tools 就是前面定义的 @tool 列表
```

#### 4.6.5 完整 LangGraph Agent —— 带人工审批的 AI 秘书

这是本节课最重要的代码。它实现了一个带 **Human-in-the-Loop** 的 Agent：当 Agent 要执行 `set_reminder` 等"危险"操作时，需要人工批准。

```python
# ============================================================
# langgraph_secretary.py — LangGraph 可中断 Agent
# 安装：pip install langchain langchain-openai langgraph
# 运行：python langgraph_secretary.py
# ============================================================

import datetime
import math
import os
from typing import TypedDict, Annotated, Sequence, Literal
import operator

# LangChain 相关
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import (
    BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
)

# LangGraph 相关
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# ============================================================
# 第 1 步：初始化模型
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),
    base_url="https://api.deepseek.com",
    temperature=0.3,
)

# ============================================================
# 第 2 步：定义工具（与前面相同）
# ============================================================

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    now = datetime.datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekdays[now.weekday()]}"

@tool
def calculate(expression: str) -> str:
    """执行数学计算。
    
    Args:
        expression: 数学表达式
    """
    allowed = {"math": math, "abs": abs, "round": round,
               "min": min, "max": max, "sqrt": math.sqrt, "pi": math.pi}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算出错：{e}"

@tool
def search_course(keyword: str) -> str:
    """搜索课程信息。
    
    Args:
        keyword: 课程关键词
    """
    courses = {
        "python": "Python基础课 | 王建国教授 | 每周二 14:00 | 实验室301",
        "机器学习": "机器学习 | 李明教授 | 每周四 09:00 | 教学楼B201",
        "深度学习": "深度学习 | 张华教授 | 每周五 15:00 | 实验室201",
        "agent": "AI Agent开发 | 陈思州讲师 | 每周三 10:00 | 在线课程",
    }
    for key, value in courses.items():
        if keyword.lower() in key.lower():
            return f"📚 {value}"
    return f"未找到与'{keyword}'相关的课程。"

@tool
def set_reminder(task: str, time_str: str) -> str:
    """设置提醒事项。⚠️ 此操作需要管理员权限确认。
    
    Args:
        task: 提醒内容
        time_str: 提醒时间
    """
    return f"✅ 已设置提醒：'{task}' - {time_str}"

tools = [get_current_time, calculate, search_course, set_reminder]

# ============================================================
# 第 3 步：定义 Agent 状态
# ============================================================
class AgentState(TypedDict):
    """Agent 的全局状态——在节点之间传递的数据"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # operator.add 表示：当不同节点返回 {"messages": new_msgs} 时，
    # 自动将 new_msgs 追加到已有的 messages 列表中，而不是覆盖

# ============================================================
# 第 4 步：定义节点函数
# ============================================================

# 系统提示词
SYSTEM_PROMPT = """你是一个 AI 秘书。你可以使用工具帮助用户完成任务。

## 可用工具
- get_current_time: 查询时间
- calculate: 数学计算
- search_course: 搜索课程
- set_reminder: 设置提醒（⚠️ 此操作需要人工审批后才能执行）

## 规则
1. 主动使用工具，不要猜测
2. 如果用户要求设置提醒，先确认内容，再调用 set_reminder
3. 用友好简洁的中文回复"""

def agent_node(state: AgentState) -> dict:
    """Agent 思考节点：让 LLM 分析当前状态并决定下一步动作"""
    messages = state["messages"]
    
    # 在消息列表最前面加入系统提示词
    full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    
    # 调用绑定了工具的 LLM
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(full_messages)
    
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "human_approval", END]:
    """条件判断函数：决定 Agent 下一步该做什么
    
    这是 LangGraph 的核心——根据状态做出路由决策。
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # 如果 LLM 决定调用工具
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        # 检查是否有需要人工审批的操作
        for tool_call in last_message.tool_calls:
            tool_name = tool_call.get("name", "")
            if tool_name in ["set_reminder"]:  # 危险操作列表
                return "human_approval"
        # 普通工具，直接执行
        return "tools"
    
    # LLM 没有调用工具 → 对话结束
    return END

def human_approval_node(state: AgentState) -> dict:
    """人工审批节点：让用户确认是否允许执行危险操作"""
    messages = state["messages"]
    last_message = messages[-1]
    
    print("\n" + "=" * 50)
    print("⚠️  需要人工审批！")
    print("=" * 50)
    
    approval_results = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call.get("name", "unknown")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id", "")
        
        print(f"\n📌 操作类型：{tool_name}")
        print(f"📝 参数详情：")
        for key, value in tool_args.items():
            print(f"   · {key}: {value}")
        
        # 等待用户输入
        user_input = input("\n🔐 批准执行吗？(y/n): ").strip().lower()
        
        if user_input == "y":
            # 批准：不添加任何拦截消息，让流程继续到 tools 节点
            print("✅ 已批准")
            # 注意：这里不 return，而是让原始消息通过
        else:
            # 拒绝：添加一个 ToolMessage 告知工具被拒绝
            rejection_msg = ToolMessage(
                content=f"❌ 操作已被用户拒绝：用户不允许执行 '{tool_name}'。请告知用户此操作被拒绝。",
                tool_call_id=tool_id,
            )
            approval_results.append(rejection_msg)
            print("❌ 已拒绝")
    
    print("=" * 50 + "\n")
    
    # 如果有被拒绝的工具调用，需要将这些拒绝消息返回
    # 这样 agent_node 下次被调用时会看到拒绝信息
    if approval_results:
        return {"messages": approval_results}
    
    # 全部批准——返回空更新，原始消息继续传递到 tools 节点
    return {}

# ============================================================
# 第 5 步：构建图
# ============================================================

# 创建 StateGraph
builder = StateGraph(AgentState)

# 添加节点
builder.add_node("agent", agent_node)          # 思考节点
builder.add_node("tools", ToolNode(tools))      # 工具执行节点
builder.add_node("human_approval", human_approval_node)  # 人工审批节点

# 设置入口
builder.set_entry_point("agent")

# 添加条件边（从 agent 节点出发）
builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",              # → 执行工具
        "human_approval": "human_approval",  # → 人工审批
        END: END,                       # → 结束
    }
)

# 添加固定边
builder.add_edge("tools", "agent")            # 工具执行完 → 回到思考
builder.add_edge("human_approval", "tools")   # 审批完（无论批准与否）→ 执行工具

# 编译图
graph = builder.compile()

# ============================================================
# 第 6 步：运行测试
# ============================================================

def run_graph(user_input: str, show_process: bool = True) -> str:
    """运行 LangGraph Agent 并返回最终回答"""
    if show_process:
        print("\n" + "=" * 60)
        print(f"  🙋 用户输入：{user_input}")
        print("=" * 60)
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
    }
    
    # 逐步执行并展示过程
    if show_process:
        step_num = 0
        for event in graph.stream(initial_state):
            step_num += 1
            for node_name, node_output in event.items():
                print(f"\n--- 步骤 {step_num}: [{node_name}] ---")
                if "messages" in node_output:
                    for msg in node_output["messages"]:
                        if isinstance(msg, AIMessage):
                            if msg.content:
                                print(f"💭 思考: {msg.content[:200]}...")
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tc in msg.tool_calls:
                                    print(f"🔧 计划调用: {tc['name']}({tc.get('args', {})})")
                        elif isinstance(msg, ToolMessage):
                            print(f"📊 工具结果: {msg.content[:200]}...")
        
        # 获取最终结果
        final_state = graph.invoke(initial_state)
    else:
        final_state = graph.invoke(initial_state)
    
    # 提取最后一条 AI 消息
    for msg in reversed(final_state["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content
    
    return "处理完成。"

# ============================================================
# 测试用例
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  🔀 LangGraph 可中断 Agent")
    print("  带 Human-in-the-Loop 人工审批")
    print("=" * 60)
    
    # 测试 1：普通操作（不需要审批）
    print("\n\n" + "🧪 " * 20)
    print("测试 1：普通操作（查时间 + 计算）")
    print("🧪 " * 20)
    result = run_graph("现在几点了？另外帮我算一下 3.14 * 256 等于多少")
    print(f"\n🎯 最终回答：{result}")
    
    # 测试 2：危险操作（需要人工审批）
    print("\n\n" + "🧪 " * 20)
    print("测试 2：危险操作（设置提醒 — 需要审批）")
    print("🧪 " * 20)
    result = run_graph("帮我设置一个提醒：明天上午10点参加AI课程答辩")
    print(f"\n🎯 最终回答：{result}")
    
    # 测试 3：混合操作（查询 + 危险操作）
    print("\n\n" + "🧪 " * 20)
    print("测试 3：混合操作（查课程 + 设提醒）")
    print("🧪 " * 20)
    result = run_graph(
        "帮我查一下机器学习课程的信息，然后设置一个提醒："
        "下周四上午8:50到教学楼B201上课"
    )
    print(f"\n🎯 最终回答：{result}")
```

**代码执行流程可视化**：

```
用户输入: "帮我设置一个提醒：明天上午10点参加AI课程答辩"
    │
    ▼
┌─────────────┐
│ agent_node  │  LLM 决定：需要调用 set_reminder(task="参加AI课程答辩", time_str="明天上午10点")
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ should_continue  │  检测到 tool_call.name == "set_reminder"
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ human_approval_node  │  显示：操作详情 → 等待用户输入 y/n
└──────┬───────────────┘
       │
       ├── 用户输入 "y" → 批准 → 原始消息不变，继续传递
       ├── 用户输入 "n" → 拒绝 → 注入拒绝 ToolMessage
       │
       ▼
┌─────────────┐
│  tools 节点 │  执行 tool_calls（批准的）或跳过（拒绝的）
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ agent_node  │  LLM 看到工具结果，生成最终回复
└──────┬──────┘
       │
       ▼
     [END]
```

> 📊 **企业视角：人工审批节点 = 企业 Agent 的安全阀**
>
> 这是企业 Agent 和 Demo Agent 的**核心区别**。Demo Agent 追求"全自动"以炫技，企业 Agent 必须在关键节点设限。
>
> **必须设置人工审批的企业 Agent 操作**：
>
> | 操作类型 | 具体场景 | 为什么必须审批 | 审批策略 |
> |---------|---------|--------------|---------|
> | **财务操作** | 发起付款、修改合同金额、审批报销 | 涉及资金流动 | 双重审批：Agent建议→主管确认→财务执行 |
> | **对外发布** | 发送客户邮件、发布社交媒体、更新官网 | 对外内容代表公司形象 | Agent起草→人类审核→定时发布 |
> | **数据修改** | 修改生产数据库、删除用户数据 | 不可逆操作 | Agent建议→DBA审核→执行+自动备份 |
> | **合规操作** | 处理个人隐私数据、生成法律文件 | 涉及法规风险 | Agent生成→法务审核→合规确认 |
> | **API/Agent上线** | 新Agent上线、修改权限配置 | 安全边界变更 | CI/CD流程+安全审查 |
>
> **企业 Agent 部署检查清单**：
> - [ ] 权限边界：Agent 能访问哪些系统？每个工具的读写权限是否做了最小化配置？
> - [ ] 成本限制：是否设置了月度API预算上限和单次调用超时限制？
> - [ ] 审计追踪：每次Agent决策是否记录了完整日志（输入/输出/工具调用/Token消耗）？
> - [ ] 错误升级：Agent执行出错时，是否有人工介入的升级路径？（如：重试3次后→通知主管→人工接管）
> - [ ] 合规审查：Agent的输出是否经过企业合规策略过滤？（如：不泄露客户隐私、不使用敏感词汇）
> - [ ] 回滚机制：如果Agent误操作，是否有快速回滚方案？

#### 4.6.6 扩展：添加 Checkpointing（断点续执行）

LangGraph 支持 Checkpointing——保存执行状态，支持暂停、恢复和回放：

```python
from langgraph.checkpoint.memory import MemorySaver

# 创建内存检查点
checkpointer = MemorySaver()

# 编译时传入 checkpointer
graph_with_checkpoint = builder.compile(checkpointer=checkpointer)

# 运行时可指定 thread_id（用于区分不同会话）
config = {"configurable": {"thread_id": "user-session-123"}}

# 第一次执行
result_1 = graph_with_checkpoint.invoke(
    {"messages": [HumanMessage(content="查一下现在几点了")]},
    config=config,
)

# 第二次执行（同一 thread_id → 自动继承之前的对话历史）
result_2 = graph_with_checkpoint.invoke(
    {"messages": [HumanMessage(content="我刚才问了什么？")]},
    config=config,
)
# Agent 因为有 checkpoint 中的历史消息，能回答"你刚才问了时间"

# 查看某个 thread 的状态历史
for state in graph_with_checkpoint.get_state_history(config):
    print(f"Step: {len(state.values['messages'])} messages")
```

**Checkpointing 的实际价值**：

- **长任务中断恢复**：用户关闭浏览器后重新打开，Agent 可以从中断处继续
- **审核/审批工作流**：经理审批通过后，系统自动从断点继续执行
- **调试和回放**：回放某个用户会话的完整执行过程，分析问题
- **A/B 测试**：从同一状态分叉，对比不同策略的执行路径

---

### 4.7 LangChain vs 纯 API —— 技术选型指南

#### 4.7.1 代码量对比

同一个"AI 秘书"（4 个工具 + 记忆），三种方式的代码量：

| 实现方式 | 大约代码行数 | 核心复杂度 |
|----------|-------------|-----------|
| **纯 API（第 19 课）** | ~150 行 | 手动 JSON Schema、手动消息管理、手动循环控制 |
| **LangChain Agent** | ~120 行 | @tool 简化工具定义、AgentExecutor 自动管理循环 |
| **LangGraph Agent** | ~180 行 | 显式图结构、更灵活但代码更多 |

#### 4.7.2 优缺点对比

| 维度 | 纯 API | LangChain | LangGraph |
|------|--------|-----------|-----------|
| **学习曲线** | 低（只需了解 API 格式） | 中（需理解框架抽象） | 高（需理解图、状态、边） |
| **灵活性** | 最高（完全控制） | 中（框架有约定） | 高（图结构可自由定制） |
| **开发效率** | 低（重复代码多） | 高（装饰器、自动管理） | 中（需要设计图结构） |
| **调试难度** | 低（代码透明） | 中（verbose 可看日志） | 中高（需追踪图执行） |
| **复杂流程支持** | 差（只能线性循环） | 中（AgentExecutor 约定） | 优（图、条件分支、并行） |
| **人工审批** | 需手动实现 | 需 Hack 实现 | 原生支持（条件边+审批节点） |
| **生态工具** | 无 | LangSmith、Hub、模板 | LangSmith Tracing |
| **版本稳定性** | 高（API 相对稳定） | 低（框架迭代快） | 中 |

#### 4.7.3 技术选型建议

```
你的项目复杂度如何？
│
├── 简单（1-3个工具，线性流程）
│   └── 推荐：纯 API
│       理由：代码最少，最透明，最容易调试
│       示例：一个只做数学计算和时间查询的 Agent
│
├── 中等（3-10个工具，需要记忆管理）
│   └── 推荐：LangChain Agent (create_tool_calling_agent)
│       理由：@tool 装饰器 + AgentExecutor 大幅降低开发成本
│       示例：AI 秘书、课程助手、客服 Agent
│
├── 复杂（需要条件分支、人工审批、并行执行）
│   └── 推荐：LangGraph
│       理由：图结构提供最大的灵活性和可控性
│       示例：多步骤审批工作流、研究报告生成 Agent、多 Agent 协作系统
│
└── 生产级（需要可观测性、回放、断点恢复）
    └── 推荐：LangGraph + LangSmith
        理由：Checkpointing + Tracing 是生产环境的必备能力
        示例：企业级 AI 助手、关键业务流程自动化
```

> **核心原则**：先用纯 API 理解原理，再用框架提高效率。理解了 what 和 why 之后，再用框架解决 how 的问题。

---

## 五、实操环节（70 分钟）

### 5.1 实操一：LangChain Agent —— 完整 AI 秘书（35 分钟）

**目标**：跑通完整的 LangChain Agent 代码，理解每个组件的作用，并测试交互。

**步骤**：

**Step 1（5分钟）**：复制 `ai_secretary.py` 完整代码到你的 IDE。

**Step 2（10分钟）**：依次运行以下测试，观察 Agent 的决策过程：

```python
# 测试 1：单一工具
secretary.chat("现在几点了？")
# 预期：调用 get_current_time，返回当前时间

# 测试 2：需要计算的工具
secretary.chat("(15+35)*2.5/7 等于多少？精确到小数点后两位")
# 预期：调用 calculate，返回计算结果

# 测试 3：信息检索
secretary.chat("深度学习课什么时候上？在哪里？谁教的？")
# 预期：调用 search_course("深度学习")，返回课程详情

# 测试 4：多步骤任务
secretary.chat("先帮我查查Python课和机器学习课分别是什么时候，然后帮我设个提醒：下周二下午1:50去实验室301上Python课")
# 预期：先调用 search_course("python")，再调用 search_course("机器学习")，最后调用 set_reminder

# 测试 5：记忆测试
secretary.chat("我刚才问的第一个问题是什么？")
# 预期：Agent 回顾对话历史，回答正确（证明记忆正常工作）
```

**Step 3（10分钟）**：观察并记录。在 `verbose=True` 模式下，你会看到：

```
> Entering new AgentExecutor chain...

Invoking: get_current_time with {}
2026年07月26日 14:30:15 周日
现在是2026年7月26日周日下午2点30分。

> Finished chain.
```

请记录以下观察结果：
- Agent 在什么时候决定调用工具？（看 AIMessage 中的 tool_calls）
- 工具执行后，Agent 如何使用工具结果生成回答？
- 多步骤任务中，Agent 如何规划步骤顺序？

**Step 4（10分钟）**：尝试修改代码。
- 将 `temperature` 从 `0.3` 改为 `0.8`，观察 Agent 行为是否有变化
- 在 `search_course` 函数中添加一个你感兴趣的课程
- 将 `max_iterations` 从 `10` 改为 `2`，然后测试"先查A再查B再查C"这样的多步任务
- 修改 System Prompt，让 Agent 用更幽默的风格回复

### 5.2 实操二：LangGraph 可中断 Agent（35 分钟）

**目标**：跑通 LangGraph Agent，重点体验人工审批节点的效果。

**Step 1（5分钟）**：复制 `langgraph_secretary.py` 完整代码。

**Step 2（15分钟）**：依次运行以下测试，观察图执行流程：

```python
# 测试 A：安全操作（不触发审批）
run_graph("现在几点了？帮我算一下 256 * 128 等于多少")
# 观察：agent → tools → agent → END（没有 human_approval 节点）

# 测试 B：危险操作（触发审批）
run_graph("帮我设置提醒：明天下午3点交作业")
# 观察：agent → human_approval → (等待你的输入 y/n) → tools → agent → END

# 测试 C：拒绝审批（输入 n）
run_graph("帮我设置提醒：下周一上午10点开会")
# 在审批时输入 n → 观察 Agent 如何回应"操作被拒绝"

# 测试 D：混合操作
run_graph("帮我查一下Python课的时间，然后设置一个提醒：下周二下午1:50去上Python课")
# 观察：agent → tools（查课程）→ agent → human_approval（设提醒）→ tools → agent → END
```

**Step 3（10分钟）**：修改 `should_continue` 函数中的危险操作列表：

```python
# 原始代码（只有 set_reminder 需要审批）
if tool_name in ["set_reminder"]:
    return "human_approval"

# 修改后（所有写操作都需要审批）
DANGEROUS_TOOLS = ["set_reminder", "delete_file", "send_email", "publish_content"]
if tool_name in DANGEROUS_TOOLS:
    return "human_approval"
```

讨论：哪些操作应该设置为"需要审批"？如何平衡安全性和用户体验？

**Step 4（5分钟）**：徒手画图。在纸上画出以下两张图的对比：

1. 第 19 课纯 API Agent 的流程图（while 循环）
2. 本节课 LangGraph Agent 的状态图（含人工审批分支）

标注出它们的关键差异。

---

## 六、课后作业

### 作业 1：代码对比分析

将第 19 课"纯 API Agent"的代码和本节课"LangChain Agent"的代码并排对比，完成以下表格（200字以上分析）：

| 对比维度 | 纯 API 实现方式 | LangChain 实现方式 | 哪种更好？为什么？ |
|----------|----------------|-------------------|-------------------|
| 工具定义 | | | |
| 消息管理 | | | |
| 循环控制 | | | |
| 错误处理 | | | |
| 代码行数 | | | |

### 作业 2：扩展 AI 秘书

为 AI 秘书添加 2 个新工具，并完成完整测试：

1. **发送邮件**（模拟）：`send_email(to: str, subject: str, body: str) -> str`
   - 返回"✅ 邮件已发送至 {to}，主题：{subject}"
2. **翻译文本**（模拟或调用免费 API）：`translate(text: str, target_lang: str) -> str`
   - 可以使用 deepseek-chat 模型本身做翻译（不需要额外 API），或者模拟返回

要求：
- 使用 `@tool` 装饰器定义工具
- 更新 System Prompt，让 Agent 知道它有了新能力
- 运行至少 3 个测试用例验证新工具正常工作
- 在 LangGraph 版本中，将 `send_email` 加入危险操作列表

### 作业 3：LangGraph 官方 Quick Start

1. 阅读 [LangGraph 官方 Quick Start](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
2. 跑通官方 Quick Start 代码
3. 对比官方示例和本节课的代码，写出 3 个官方用了但本节课没涉及的特性

### 作业 4（加分）：对比三种实现

用三种方式分别实现同一个"天气查询+穿衣建议"Agent：
1. 纯 API（手动循环）
2. LangChain Agent
3. LangGraph Agent

每种方式的代码保存为独立文件，写一份 300 字的使用感受。

---

### 💼 企业版作业：Agent 安全策略设计

假设你所在企业准备部署一个"AI 采购助手"Agent，它可以：搜索供应商、比较报价、生成采购订单、发送询价邮件、更新ERP系统。

请设计一份 **"Agent 安全策略文档"**（1-2页），覆盖以下内容：
1. **权限矩阵**：哪些操作Agent自动执行？哪些需要人工审批？哪些完全禁止？
2. **审批流程**：画出"Agent发起采购→主管审批→财务审核"的完整流程（可用流程图）
3. **成本控制**：设置月度预算限制、单次操作金额上限、异常消费告警规则
4. **审计要求**：列出必须记录的日志字段（至少8个）
5. **应急预案**：Agent出错的3种典型场景及应对措施

使用前面📊框中的检查清单作为参考模板。

---

## 七、拓展阅读

### 官方文档（必读）

| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain 官方文档 | https://docs.langchain.com | 英文，结构清晰，推荐配合翻译插件阅读 |
| LangChain 中文文档 | https://docs.langchain.org.cn | 截止目前前端组件可能有问题 |
| LangGraph 官方文档 | https://langchain-ai.github.io/langgraph/ | LangGraph 学习入口 |
| LangGraph Quick Start | https://langchain-ai.github.io/langgraph/tutorials/introduction/ | 30 分钟上手 |

### 教程与项目

| 资源 | 链接 | 说明 |
|------|------|------|
| hello-agents | https://github.com/datawhalechina/hello-agents | Datawhale 出品，中文 Agent 系统教程 |
| LangChain 视频教程 | B站搜索"LangChain 入门" | 基于 LangChain 1.2 版本 |
| LangGraph 视频教程 | https://www.bilibili.com/video/BV1dw9CBEEob | 较新的 LangGraph 中文教程 |

### 设计理念（必读）

| 资源 | 链接 | 说明 |
|------|------|------|
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Anthropic 官方：Agent 设计原则 |
| A practical guide to building agents | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | OpenAI 官方：Agent 工程指南 |

### 进阶工具

| 工具 | 说明 |
|------|------|
| **LangSmith** | LangChain 官方的调试、测试、监控平台（https://smith.langchain.com） |
| **LangServe** | 将 LangChain Chain/Agent 部署为 REST API |
| **LangGraph Studio** | LangGraph 的可视化编辑和调试工具 |

---

## 八、常见问题

**Q1: LangChain 版本更新太快，代码老是过时怎么办？**

A: 这是 LangChain 生态最大的痛点。应对策略：
- 锁定版本号：`pip install langchain==0.3.x langchain-openai==0.2.x`
- 优先参考官方文档而非网上的旧教程（官方文档始终是最新的）
- 如果项目对稳定性要求高，直接用纯 API 或选择更稳定的框架（如 Pydantic AI）
- 本节课代码基于 LangChain 0.3+ 版本，如果遇到 API 变化，优先查官方 Migration Guide

**Q2: 什么时候用 LangChain，什么时候用 LangGraph？**

A: 
- **LangChain**：适合标准 Agent 场景（有工具、有记忆、线性循环），80% 的 Agent 需求用它就够了
- **LangGraph**：当你需要以下能力时升级到 LangGraph：
  - 条件分支（根据结果走不同路径）
  - 人工审批（某些操作需要确认）
  - 并行执行（多个工具同时运行）
  - 断点续执行（长任务中断恢复）
  - 多 Agent 编排（多个 Agent 按图协作）

**Q3: @tool 装饰器自动生成的 tool description 不好用怎么办？**

A: 你可以通过重写 `name` 和 `description` 属性来手动指定：

```python
@tool
def my_tool(x: str) -> str:
    """这段文字会作为 description"""
    return f"处理: {x}"

# 手动覆盖
my_tool.name = "custom_tool_name"
my_tool.description = "更详细的描述，写清楚什么时候使用、参数含义、返回值格式"
```

工具描述的质量直接影响 Agent 的判断准确性——Agent 全靠这些描述来决定该调用哪个工具。

**Q4: LangGraph 的图执行看起来很慢，怎么优化？**

A:
- 使用流式执行 `graph.stream()` 而非 `graph.invoke()`，让用户实时看到进度
- 将独立的工具调用放在不同的分支中并行执行
- 使用 `Send` API 实现 Map-Reduce 模式，并行处理多个子任务
- 在 Human-in-the-Loop 场景中，使用 `interrupt()` 代替轮询

**Q5: 纯 API、LangChain、LangGraph —— 我该学哪个？**

A: 建议学习路径：
1. **先学纯 API**（第 19 课已覆盖）—— 理解 Agent 的核心循环和 Function Calling 本质
2. **再学 LangChain**（本节课第一部分）—— 用框架提高开发效率
3. **最后学 LangGraph**（本节课第二部分）—— 处理复杂编排需求

这三者不是"选一个"，而是"依次掌握"的关系。理解了底层原理，用框架时才能知道它在帮你做什么；掌握了框架能力，才能在做技术选型时有判断力。

**Q6: Agent 调用工具的费用怎么控制？**

A:
- 设置 `max_iterations` 限制最大循环次数（防止无限循环烧钱）
- 设置 `max_execution_time` 限制最大执行时间
- 在 Prompt 中明确告诉 Agent："如果无法在 3 步内完成，请向用户汇报并请求更多指示"
- 使用 LangSmith 监控每次调用的 token 消耗和成本
- 对于生产环境，建议使用更便宜的模型（如 DeepSeek、Qwen）并设置预算告警

### Q7（企业）：LangChain 版本更新太快，对企业项目有什么影响？如何应对？

**答**：LangChain 从0.1到0.3经历了几次大的API变动，这是选择LangChain时需要正视的风险。建议：1) 在requirements.txt中锁定版本号，不自动升级；2) 对新项目评估LangGraph（API更稳定）或更轻量的方案；3) 考虑国内替代框架（如Dify、FastGPT）用于不需要深度定制的场景；4) 核心业务逻辑与框架代码分离——即使换框架，业务逻辑不用重写。

### Q8（企业）：Human-in-the-Loop 会不会让"全自动"的优势打折扣？

**答**：短期看，是的——人工审批增加了等待时间。但长期看，这是企业Agent"能用"的前提。类比：自动驾驶汽车仍然需要安全员坐在驾驶位。没有人工审批的Agent就像一个没有刹车的车——速度很快，但一撞就是大事故。真正的效率提升来自于：Agent做80%的工作（起草、收集、整理）→人类做20%的决策（确认、修正、批准）——这已经比纯人类操作快5-10倍。

---

> **本节课总结**：你学会了用 LangChain 的三大支柱（Model、Tool、Memory）构建 Agent，并用 LangGraph 的状态图实现 Human-in-the-Loop。从手写循环到框架开发，这是 Agent 工程能力的一次质的飞跃。下节课我们将学习 MCP（Model Context Protocol），让你的 Agent 能够连接更广泛的工具生态。
