# 第16讲：多平台API调用实战

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **课程阶段** | 第六周：API开发与集成 |
| **课时序号** | 第1讲（Week 6, Lesson 1） |
| **课程主题** | 多平台API调用实战 |
| **授课时长** | 90分钟（理论20分钟 + 实操70分钟） |
| **适用对象** | 已完成LLM基础API调用的学员 |
| **前置知识** | Python基础、HTTP基础、LLM基础API调用经验 |

---

## 二、学习目标

完成本课时后，学员应能：

1. **系统理解**主流LLM API平台（OpenAI、DeepSeek、通义千问、Claude）的差异、定价和适用场景
2. **独立设计**并实现统一的多平台API封装层（MultiLLM模式）
3. **掌握流式输出**的原理与实现，包括打字机效果和实时UI更新
4. **运用最佳实践**进行错误处理、重试、速率限制和成本追踪
5. **深入调优**模型参数（temperature、top_p、max_tokens等），理解其对输出的具体影响
6. **管理长对话上下文**：Token计数、窗口监控与对话摘要
7. **实施成本优化**：模型选择策略、缓存、Prompt压缩与批处理

---

## 三、课前准备

### 3.1 环境依赖

```bash
pip install openai>=1.0.0 tiktoken python-dotenv rich
```

- **openai**（≥1.0.0）：新版OpenAI SDK兼容多平台，支持流式调用
- **tiktoken**：精确计算Token数量，用于上下文管理
- **python-dotenv**：管理API Key等敏感配置
- **rich**：终端美化输出，模拟打字机效果

### 3.2 API Key 准备

请提前注册并获取以下平台的API密钥（至少准备两个）：

| 平台 | 注册地址 | API Key获取路径 |
|------|----------|-----------------|
| **OpenAI** | https://platform.openai.com | Dashboard → API keys |
| **DeepSeek** | https://platform.deepseek.com | 控制台 → API keys |
| **阿里云百炼（通义千问）** | https://bailian.console.aliyun.com | 模型广场 → API-KEY管理 |
| **Anthropic（Claude）** | https://console.anthropic.com | API Keys |

> **安全提醒**：API Key应存储在 `.env` 文件中，并加入 `.gitignore`，切勿提交到版本控制系统。

### 3.3 环境变量配置

在项目根目录创建 `.env` 文件：

```bash
OPENAI_API_KEY=sk-your-openai-key-here
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
DASHSCOPE_API_KEY=sk-your-dashscope-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

---

## 四、核心知识点详解

### 4.1 主流LLM API平台深度对比

#### 4.1.1 平台概览与模型矩阵

**OpenAI（GPT系列）**

OpenAI是当前LLM API生态的标杆，其SDK已成为事实上的行业标准。核心优势在于模型能力均衡、生态成熟、文档完善、社区活跃。不足在于价格较高，且对中国大陆开发者存在网络访问障碍。

| 模型 | 上下文窗口 | 输入价格（$/1M tokens） | 输出价格（$/1M tokens） | 核心优势 |
|------|-----------|------------------------|------------------------|---------|
| GPT-4o | 128K | $2.50 | $10.00 | 多模态，速度快，综合能力强 |
| GPT-4o-mini | 128K | $0.15 | $0.60 | 极致性价比，适合高频简单任务 |
| GPT-4.1 | 1M | $2.00 | $8.00 | 超长上下文，代码能力极强 |
| o3 | 200K | $10.00 | $40.00 | 深度推理，数学/编程顶级 |
| o4-mini | 200K | $1.10 | $4.40 | 轻量推理，性价比高 |

**DeepSeek**

国产大模型的黑马，以极低价格和出色中文能力著称。API完全兼容OpenAI SDK，迁移成本几乎为零。推荐作为中文场景的首选平台之一。

| 模型 | 上下文窗口 | 输入价格（￥/1M tokens） | 输出价格（￥/1M tokens） | 核心优势 |
|------|-----------|------------------------|------------------------|---------|
| DeepSeek-V3 | 128K | ￥2.00 | ￥8.00 | 综合能力均衡，中文友好 |
| DeepSeek-R1 | 128K | ￥4.00 | ￥16.00 | 深度推理，含思维链 |
| DeepSeek-R1-0528 | 128K | ￥4.00 | ￥16.00 | 最新推理模型 |

**阿里云百炼（通义千问系列）**

阿里云提供的企业级大模型平台，中文能力优秀，多模态支持丰富，与阿里云生态深度集成。适合需要企业级服务和多模态能力的场景。

| 模型 | 上下文窗口 | 输入价格（￥/1M tokens） | 输出价格（￥/1M tokens） | 核心优势 |
|------|-----------|------------------------|------------------------|---------|
| Qwen3-235B-A22B | 128K | ￥4.00 | ￥16.00 | MoE架构，旗舰推理 |
| Qwen-Plus | 128K | ￥0.80 | ￥2.00 | 性价比最优 |
| Qwen-Turbo | 128K | ￥0.30 | ￥0.60 | 超快速度，简单任务 |
| Qwen-VL-Plus | 视觉输入 | - | - | 多模态理解 |

**Anthropic Claude 系列**

Claude在长文本理解、代码生成和安全对齐方面表现出色。Claude Code CLI已成为AI辅助编程的代表性工具。Opus模型的深度推理能力在复杂任务中尤为突出。

| 模型 | 上下文窗口 | 输入价格（$/1M tokens） | 输出价格（$/1M tokens） | 核心优势 |
|------|-----------|------------------------|------------------------|---------|
| Claude Opus 4 | 200K | $15.00 | $75.00 | 旗舰推理，多模态，复杂任务 |
| Claude Sonnet 4 | 200K | $3.00 | $15.00 | 速度与智能的最佳平衡 |
| Claude Opus 4.5 | 200K | $5.00 | $25.00 | 深度推理优化 |
| Claude Haiku 3.5 | 200K | $0.80 | $4.00 | 最快速度，极高性价比 |

#### 4.1.2 平台选型决策矩阵

| 场景 | 推荐平台 | 推荐模型 | 理由 |
|------|---------|---------|------|
| **日常中文对话** | DeepSeek | V3 | 中文最优，价格极低 |
| **复杂推理/编程** | Claude / OpenAI | Opus 4 / o3 | 推理能力最强 |
| **高频低成本调用** | DeepSeek / OpenAI | V3 / GPT-4o-mini | 低延迟，低成本 |
| **多模态理解** | OpenAI / 通义千问 | GPT-4o / Qwen-VL-Plus | 视觉理解能力强 |
| **超长文档分析** | Claude | Opus 4（200K） | 上下文窗口大，长文理解强 |
| **企业级部署** | 阿里云百炼 | Qwen-Plus | 国内合规，SLA保障 |
| **快速原型验证** | DeepSeek | V3 | 兼容OpenAI SDK，零迁移成本 |

---

### 4.2 统一API封装模式

#### 4.2.1 设计理念

当项目需要对接多个LLM平台时，如果每个平台都写一套独立调用代码，会导致：
- 代码重复，维护成本高
- 切换平台需要大量修改
- 缺少统一的错误处理和日志机制
- 难以进行平台间的效果对比

**MultiLLM封装模式**通过适配器模式（Adapter Pattern）统一所有平台的调用接口，对外暴露一致的 `chat()` 和 `stream_chat()` 方法，对内根据 `provider` 参数自动路由到对应平台。

#### 4.2.2 架构设计

```
┌─────────────────────────────────────────────────┐
│                   业务代码层                       │
│   llm.chat("你好")  /  llm.stream_chat("你好")    │
└─────────────────────┬───────────────────────────┘
                      │ 统一接口
┌─────────────────────▼───────────────────────────┐
│               MultiLLM 封装层                     │
│  ┌─────────────────────────────────────────────┐ │
│  │  chat() / stream_chat() / switch_provider()  │ │
│  │  clear_history() / get_cost()               │ │
│  └─────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │  配置管理: ModelConfig / ProviderRegistry    │ │
│  │  模型映射: model_name -> API endpoint        │ │
│  │  成本追踪: input_tokens * price + ...         │ │
│  └─────────────────────────────────────────────┘ │
└──────┬──────────────┬──────────────┬────────────┘
       │              │              │
┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
│ OpenAI SDK  │ │DeepSeek   │ │ 通义千问     │
│ (原生)      │ │(OpenAI兼容)│ │(OpenAI兼容)  │
└─────────────┘ └───────────┘ └─────────────┘
```

> **关键设计决策**：DeepSeek和通义千问的API均兼容OpenAI SDK接口格式，因此可以通过同一个 `openai.OpenAI` 客户端实例，仅切换 `base_url` 和 `api_key` 来实现三平台的统一调用。Claude使用独立的Anthropic SDK。

#### 4.2.3 关键设计模式

**适配器模式（Adapter Pattern）**
- 每个平台一个内部适配器，负责将平台特定的API调用适配为统一格式
- 对外隐藏平台差异，对内充分利用各平台特性

**策略模式（Strategy Pattern）**
- `chat()` 和 `stream_chat()` 是策略上下文
- 根据 `provider` 动态选择执行策略（调用哪个平台）
- 新增平台只需添加新策略，无需修改现有代码

**工厂模式（Factory Pattern）**
- `_get_client()` 方法作为工厂函数，根据provider创建对应的客户端实例
- 客户端实例可缓存复用，避免重复创建

---

### 4.3 流式输出详解

#### 4.3.1 流式输出原理

传统API调用是**请求-全部响应**模式：

```
Client ──请求──▶ Server
Client ◄──完整响应── Server  （等待3-10秒）
```

流式输出（Streaming）采用**请求-逐块响应**模式：

```
Client ──请求──▶ Server
Client ◄──chunk1── Server  （"你好"）
Client ◄──chunk2── Server  （"，我"）
Client ◄──chunk3── Server  （"是A"）
Client ◄──chunk4── Server  （"I助手"）
...
Client ◄──[DONE]── Server
```

流式输出的核心机制是 **Server-Sent Events (SSE)** —— 服务器通过持久HTTP连接，持续向客户端推送数据块。每个数据块（chunk）通常是几个字符或一个token。

#### 4.3.2 OpenAI SDK中的流式实现

```python
from openai import OpenAI

client = OpenAI()
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,  # 开启流式输出
)

# 逐块迭代
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**chunk的结构**（stream=True时）：

```python
# 非流式 response.choices[0].message.content → "你好！我是AI助手..."
# 流式 chunk.choices[0].delta.content → "你好" → "！" → "我是" → "AI" → ...
```

**关键区别**：
- 非流式：`choice.message.content`（完整消息）
- 流式：`choice.delta.content`（增量内容，可能为None）

#### 4.3.3 打字机效果实现

使用 `rich` 库实现终端打字机效果：

```python
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

console = Console()
accumulated_text = ""

with Live(Markdown(accumulated_text), console=console, refresh_per_second=10) as live:
    for chunk in stream:
        if chunk.choices[0].delta.content:
            accumulated_text += chunk.choices[0].delta.content
            live.update(Markdown(accumulated_text))
```

`rich.Live` 提供实时更新的终端UI区域，`refresh_per_second` 控制刷新率（太高浪费CPU，太低打字效果不流畅，10Hz是较好的平衡点）。

#### 4.3.4 流式输出的用户体验价值

| 维度 | 非流式 | 流式 |
|------|--------|------|
| **首字时间** | 3-10秒（等待完整响应） | 0.2-0.5秒（立即看到反馈） |
| **用户感知延迟** | 高（空白等待焦虑） | 低（内容逐步呈现） |
| **中断能力** | 无法中途停止 | 可按Ctrl+C立即停止 |
| **长文本体验** | 等待时间与文本长度成正比 | 等待时间与首字时间成正比 |
| **适用场景** | 后台批处理、API-to-API | 聊天UI、实时对话 |

---

### 4.4 API调用最佳实践

#### 4.4.1 错误处理分层策略

LLM API调用可能遇到的错误分为以下几层：

```
第一层：网络错误（连接超时、DNS解析失败、SSL证书错误）
        → 指数退避重试（最多3次）

第二层：服务端错误（HTTP 5xx：服务过载、内部错误）
        → 指数退避重试（最多3次）

第三层：限流错误（HTTP 429：请求过于频繁）
        → 等待 Retry-After 头指定的时间后重试

第四层：客户端错误（HTTP 4xx：参数错误、认证失败、余额不足）
        → 不重试，直接提示用户修正

第五层：内容安全错误（finish_reason="content_filter"）
        → 提示用户修改输入内容
```

完整错误处理代码示例：

```python
import time
from typing import Generator

def safe_api_call(client_call, max_retries: int = 3):
    """带指数退避的安全API调用包装器"""
    for attempt in range(max_retries):
        try:
            return client_call()
        except openai.RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = int(
                e.response.headers.get("Retry-After", 2 ** attempt)
            )
            print(f"⚠ 频率限制，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
        except openai.APIConnectionError:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"⚠ 网络连接错误，{wait_time}秒后重试 ({attempt+1}/{max_retries})...")
            time.sleep(wait_time)
        except openai.InternalServerError:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"⚠ 服务器内部错误，{wait_time}秒后重试 ({attempt+1}/{max_retries})...")
            time.sleep(wait_time)
        except openai.AuthenticationError:
            raise ValueError("❌ API Key无效，请检查.env文件中的密钥配置")
        except openai.BadRequestError as e:
            error_msg = str(e)
            if "context_length" in error_msg.lower():
                raise ValueError("❌ 输入内容超出模型上下文窗口限制，请减少输入长度")
            raise
```

#### 4.4.2 指数退避（Exponential Backoff）详解

指数退避是处理瞬时错误的经典策略：

| 重试次数 | 等待时间（2^n秒） | 说明 |
|---------|-------------------|------|
| 第1次重试 | 1秒（2^0） | 快速重试，可能是瞬时网络抖动 |
| 第2次重试 | 2秒（2^1） | 给服务端更多恢复时间 |
| 第3次重试 | 4秒（2^2） | 最后一次尝试，继续等待 |
| 放弃 | - | 总计等待7秒后抛出异常 |

**为什么不用固定间隔？**
- 固定间隔可能导致"惊群效应"——多个客户端同时重试，再次压垮服务器
- 指数增长给服务器留出恢复时间
- 配合随机抖动（Jitter）效果更佳

#### 4.4.3 API Key安全管理

```python
# ❌ 绝对不要硬编码API Key
api_key = "sk-abc123..."

# ❌ 不要打印或记录API Key
print(f"Using key: {api_key}")

# ✅ 从环境变量读取
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ 日志脱敏
def mask_key(key: str) -> str:
    """遮蔽API Key，仅显示前6位和后4位"""
    if not key or len(key) < 12:
        return "***"
    return f"{key[:6]}...{key[-4:]}"

# ✅ 运行时验证
if not api_key:
    raise RuntimeError(
        "未找到OPENAI_API_KEY，请检查.env文件"
    )
```

#### 4.4.4 成本追踪系统

每次API调用后，记录Token消耗并折算为人民币成本：

```python
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class CostTracker:
    """成本追踪器"""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_rmb: float = 0.0
    call_count: int = 0
    # 价格表（元/1M tokens）
    price_map: Dict[str, tuple] = field(default_factory=lambda: {
        "gpt-4o-mini": (1.10, 4.40),      # (input, output) 按$1=￥7.3换算
        "deepseek-chat": (2.00, 8.00),
        "qwen-plus": (0.80, 2.00),
    })

    def add_usage(self, model: str, input_tokens: int, output_tokens: int):
        input_price, output_price = self.price_map.get(
            model, (0, 0)
        )
        cost = (input_tokens / 1_000_000) * input_price + \
               (output_tokens / 1_000_000) * output_price

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_rmb += cost
        self.call_count += 1

        return cost

    def summary(self) -> str:
        return (
            f"📊 成本汇总:\n"
            f"  调用次数: {self.call_count}\n"
            f"  输入Token: {self.total_input_tokens:,}\n"
            f"  输出Token: {self.total_output_tokens:,}\n"
            f"  总费用: ¥{self.total_cost_rmb:.4f}"
        )
```

---

### 4.5 模型参数深入

#### 4.5.1 核心参数详解

**temperature（温度）——控制随机性**

取值范围：0.0 ~ 2.0（OpenAI），各平台略有差异。

temperature决定了模型输出的"创造力"程度：

```
temperature = 0.0  →  "今天天气晴朗"         （确定性，重复调用答案相同）
temperature = 0.5  →  "今天阳光明媚"         （适度变化）
temperature = 1.0  →  "今天的天气真是太棒了！" （较丰富的变化）
temperature = 1.5  →  "啊，今日苍穹湛蓝如洗~"  （高随机性，可能跑偏）
```

**实际效果测试**（问"用一句话描述今天的天气"，重复5次）：

| temperature | 第1次 | 第2次 | 第3次 | 唯一样式数 |
|-------------|-------|-------|-------|-----------|
| 0.0 | "天气晴朗" | "天气晴朗" | "天气晴朗" | 1 |
| 0.5 | "天气晴朗" | "阳光明媚" | "天气不错" | 3 |
| 1.0 | "晴空万里" | "和风煦日" | "艳阳高照" | 4 |
| 1.5 | "天公作美" | "碧空如洗" | "金乌东升" | 5 |

**使用建议**：
- 代码生成、数学推理、事实问答：0.0 ~ 0.3（追求准确一致）
- 日常对话、内容创作：0.7 ~ 1.0（追求自然多样）
- 创意写作、头脑风暴：1.0 ~ 1.5（追求创新发散）

**top_p（核采样）——控制词汇选择范围**

取值范围：0.0 ~ 1.0

模型生成每个token时，会计算所有可能token的概率分布。top_p（Nucleus Sampling）只从累积概率达到p值的最小token集合中采样。

```
词汇概率分布：["晴": 0.4, "好": 0.3, "明": 0.15, "不": 0.08, "阴": 0.05, "雨": 0.02]

top_p = 0.5  → 候选集：["晴"]              （累积0.4，最保守]
top_p = 0.7  → 候选集：["晴", "好"]        （累积0.7）
top_p = 0.9  → 候选集：["晴", "好", "明", "不", "阴"] （累积0.98）
top_p = 1.0  → 候选集：全部词汇            （不限制）
```

**temperature 与 top_p 的关系**：
- 一般只调整其中一个，另一个保持默认
- temperature改变概率分布的"陡峭度"，top_p改变"截断点"
- 同时调整可能导致不可预测的效果

**max_tokens（最大输出长度）**

限制模型单次响应的最大Token数。这是控制成本和安全的重要手段。

```
问："请用100字介绍北京"  → max_tokens=1000（冗余）→ 可能输出500字，浪费
问："请用100字介绍北京"  → max_tokens=150 （合理）→ 输出约100字，精准
问："请写一篇5000字的文章" → max_tokens=200 （不足）→ 输出被截断
```

经验公式：中文场景 `max_tokens ≈ 所需字数 × 1.5 ~ 2.0`

**frequency_penalty（频率惩罚）——抑制重复**

取值范围：-2.0 ~ 2.0

正值降低模型逐字重复同一词汇的概率，用于避免输出中出现循环重复。

```
frequency_penalty = 0.0:  "很好，这个方案很好，因为很好用..."
frequency_penalty = 0.5:  "很好，这个方案不错，因为它非常实用..."
frequency_penalty = 1.0:  "很好，该方案出色，因其具备卓越的实用性..."
```

**presence_penalty（存在惩罚）——鼓励新话题**

取值范围：-2.0 ~ 2.0

正值降低模型重复已提及概念的概率，鼓励模型探索新话题。

```
presence_penalty = 0.0:  每次回答都提到"人工智能"（高频词）
presence_penalty = 0.5:  逐渐减少"人工智能"的重复使用
presence_penalty = 1.0:  明显避免重复概念，使用同义词或新角度
```

#### 4.5.2 参数组合速查表

| 任务类型 | temperature | top_p | frequency_penalty | presence_penalty |
|---------|-------------|-------|-------------------|-----------------|
| 代码生成 | 0.1 | 0.95 | 0.0 | 0.0 |
| 数学解题 | 0.0 | 1.0 | 0.0 | 0.0 |
| 翻译 | 0.3 | 0.95 | 0.1 | 0.0 |
| 日常聊天 | 0.8 | 0.95 | 0.2 | 0.2 |
| 创意写作 | 1.0 | 0.9 | 0.3 | 0.3 |
| 头脑风暴 | 1.2 | 0.9 | 0.5 | 0.5 |
| 事实问答 | 0.1 | 1.0 | 0.0 | 0.0 |
| 内容摘要 | 0.3 | 0.95 | 0.1 | 0.1 |

---

### 4.6 上下文管理

#### 4.6.1 Token计数原理

Token是LLM处理文本的最小单位。不同语言Token化效率差异很大：

```
英文："Hello, how are you?"       → 7 tokens
中文："你好，你最近怎么样？"        → 15+ tokens（1个汉字≠1个token）
```

使用 `tiktoken` 库精确计数：

```python
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

text_cn = "你好，你最近怎么样？"
text_en = "Hello, how are you?"

print(f"中文: {len(encoder.encode(text_cn))} tokens")  # 约17 tokens
print(f"英文: {len(encoder.encode(text_en))} tokens")  # 7 tokens
print(f"中文膨胀率: {len(encoder.encode(text_cn))/len(text_cn):.1f}x")
# 大部分中文模型，1个汉字 ≈ 1.5~2.5个token
```

**不同模型Token计数对照（"你好世界"）**：

| 编码器 | Token数 | 说明 |
|--------|---------|------|
| cl100k_base (GPT-4/GPT-4o) | 4 | OpenAI系列 |
| o200k_base (GPT-4.1) | 4 | 最新编码器 |
| DeepSeek tokenizer | 3 | DeepSeek系列 |

> **精度说明**：tiktoken 是OpenAI开源的，对OpenAI模型完全精确。对DeepSeek和通义千问，tiktoken计数有约±5%偏差，但对于上下文管理来说精度足够。生产环境建议使用各平台官方返回的 `usage.prompt_tokens`。

#### 4.6.2 上下文窗口监控

上下文窗口 = 输入token + 输出token ≤ 模型最大限制

```python
class ContextMonitor:
    """上下文窗口监控器"""

    def __init__(self, max_tokens: int = 128000, warning_ratio: float = 0.7):
        self.max_tokens = max_tokens
        self.warning_ratio = warning_ratio
        self.warning_threshold = int(max_tokens * warning_ratio)
        self.critical_threshold = int(max_tokens * 0.9)

    def check(self, current_tokens: int) -> str:
        """检查当前Token用量并返回状态"""
        usage_pct = current_tokens / self.max_tokens * 100

        if current_tokens >= self.critical_threshold:
            return f"🔴 危险: {current_tokens:,}/{self.max_tokens:,} tokens ({usage_pct:.1f}%)"
        elif current_tokens >= self.warning_threshold:
            return f"🟡 警告: {current_tokens:,}/{self.max_tokens:,} tokens ({usage_pct:.1f}%)"
        else:
            return f"🟢 正常: {current_tokens:,}/{self.max_tokens:,} tokens ({usage_pct:.1f}%)"

    def estimate_remaining_turns(self, current_tokens: int, avg_tokens_per_turn: int = 500) -> int:
        """估算剩余对话轮数"""
        remaining = self.max_tokens - current_tokens
        return max(0, remaining // avg_tokens_per_turn)
```

#### 4.6.3 对话摘要策略

当上下文接近窗口限制时，需要对历史对话进行压缩：

```python
class ConversationSummarizer:
    """对话摘要器——保留核心信息，压缩历史"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def should_summarize(self, messages: list, max_tokens: int, threshold: float = 0.7) -> bool:
        """判断是否需要摘要"""
        total = self._count_tokens(messages)
        return total > max_tokens * threshold

    def summarize_history(self, messages: list, keep_last: int = 3) -> list:
        """
        摘要策略：
        1. 保留最近 keep_last 轮对话不变
        2. 将更早的对话压缩为一段摘要
        3. 摘要作为系统消息插入
        """
        if len(messages) <= keep_last * 2 + 2:
            return messages  # 对话太短，不需要摘要

        # 分离需摘要的部分和需要保留的部分
        to_summarize = messages[:-keep_last * 2]
        to_keep = messages[-keep_last * 2:]

        # 调用模型生成摘要
        summary_prompt = "请将以下对话摘要为一段简洁的文字，保留关键信息、决策和重要上下文："
        summary = self.llm.chat(summary_prompt, system_msg=None)

        # 重构消息列表：系统摘要 + 最近对话
        summarized_messages = [
            {"role": "system", "content": f"[历史对话摘要]\n{summary}"}
        ] + to_keep

        return summarized_messages

    def _count_tokens(self, messages: list) -> int:
        encoder = tiktoken.encoding_for_model("gpt-4o")
        total = 0
        for msg in messages:
            total += len(encoder.encode(msg.get("content", "")))
            total += 4  # 每条消息的元数据token开销
        return total
```

**摘要策略对比**：

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **滑动窗口**（保留最近N条） | 简单，无额外API调用 | 丢失所有早期信息 | 闲聊对话 |
| **对话摘要** | 保留关键上下文 | 需额外API调用 | 客服、教育 |
| **混合策略**（摘要+最近N条） | 兼顾全局和细节 | 实现较复杂 | 复杂任务 |
| **向量检索**（RAG式） | 精确召回相关信息 | 需要embedding和向量库 | 超长对话 |

---

### 4.7 成本优化策略

#### 4.7.1 模型分层选择策略

根据任务复杂度智能路由到不同成本的模型：

```
任务复杂度判断 → 模型选择
     │
     ├── 简单（问候、确认、格式转换）
     │     → GPT-4o-mini / DeepSeek-V3 / Qwen-Turbo
     │     → 成本: ¥0.001~0.01/次
     │
     ├── 中等（解释、总结、翻译）
     │     → DeepSeek-V3 / Qwen-Plus / GPT-4o
     │     → 成本: ¥0.01~0.05/次
     │
     └── 复杂（推理、编程、分析）
           → Claude Opus / GPT-4.1 / o3 / DeepSeek-R1
           → 成本: ¥0.05~1.00/次
```

#### 4.7.2 缓存策略

```python
import hashlib
import json
from functools import lru_cache

class CachedLLM:
    """带缓存的LLM调用包装器"""

    def __init__(self, base_llm):
        self.llm = base_llm
        self._cache = {}  # 简单的内存缓存

    def _cache_key(self, messages, **kwargs) -> str:
        """生成缓存键"""
        content = json.dumps(messages, ensure_ascii=False, sort_keys=True)
        content += json.dumps(kwargs, ensure_ascii=False, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def chat(self, messages, use_cache: bool = True, **kwargs):
        """带缓存的chat调用"""
        if use_cache and kwargs.get("temperature", 1.0) == 0.0:
            # 只有temperature=0时才缓存（确定性输出）
            key = self._cache_key(messages, **kwargs)
            if key in self._cache:
                print("💾 缓存命中！")
                return self._cache[key]
            result = self.llm.chat(messages, **kwargs)
            self._cache[key] = result
            return result
        return self.llm.chat(messages, **kwargs)
```

**缓存适用条件**：
- temperature = 0（确定性输出才可缓存）
- 相同的system prompt + user message
- 适用于批量处理、模板化问答等场景

#### 4.7.3 Prompt压缩

```python
def compress_prompt(text: str, target_ratio: float = 0.5) -> str:
    """
    Prompt压缩策略：
    1. 去除多余空白和换行
    2. 去除重复内容
    3. 简化标点
    4. 如果仍超标，请模型自行压缩
    """
    import re

    # 去除多余空白
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # 去除重复段落（简单算法）
    paragraphs = text.split('\n')
    seen = set()
    unique_paragraphs = []
    for p in paragraphs:
        key = p.strip()[:50]  # 用前50个字符作为段落指纹
        if key not in seen:
            seen.add(key)
            unique_paragraphs.append(p)

    return '\n'.join(unique_paragraphs)
```

#### 4.7.4 综合成本优化清单

| 优化手段 | 预估节省 | 实施难度 | 说明 |
|---------|---------|---------|------|
| 任务分层路由 | 40-60% | 中 | 简单任务用便宜模型 |
| 确定性输出缓存 | 20-50% | 低 | temperature=0时缓存 |
| Prompt压缩 | 15-30% | 低 | 减少输入token |
| 限制max_tokens | 20-40% | 低 | 避免过长输出浪费 |
| 批处理 | 30-50% | 高 | 合并多个请求 |
| 系统提示优化 | 10-20% | 中 | 精简system prompt |

---

## 五、实操环节（70分钟）

### 实操1：MultiLLM统一封装工具类（30分钟）

> **目标**：实现一个完整的多平台API封装类，支持OpenAI、DeepSeek、通义千问三个平台，提供统一的对话、流式、切换和历史管理接口。

#### 完整代码实现

创建文件 `multillm.py`：

```python
"""
MultiLLM - 多平台LLM统一封装工具类
支持平台: OpenAI, DeepSeek, 阿里云百炼(通义千问)
"""

import os
import time
import json
from typing import Optional, Generator, Dict, List, Literal
from dataclasses import dataclass, field

from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

# ==================== 环境初始化 ====================
load_dotenv()
console = Console()

# ==================== 数据类 ====================

@dataclass
class ModelConfig:
    """单个模型的配置"""
    model_name: str
    base_url: str
    api_key: str
    description: str = ""
    input_price_per_1m: float = 0.0   # 单位：元
    output_price_per_1m: float = 0.0  # 单位：元

@dataclass
class UsageStats:
    """用量统计"""
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cost_rmb: float = 0.0
    latency_seconds: float = 0.0

# ==================== 平台配置注册表 ====================

class ProviderRegistry:
    """平台注册表：预置主流平台和模型配置"""

    REGISTRY: Dict[str, Dict[str, ModelConfig]] = {
        "openai": {
            "gpt-4o-mini": ModelConfig(
                model_name="gpt-4o-mini",
                base_url="https://api.openai.com/v1",
                api_key=os.getenv("OPENAI_API_KEY", ""),
                description="OpenAI GPT-4o Mini - 高性价比",
                input_price_per_1m=1.10,   # $0.15 * 7.3
                output_price_per_1m=4.40,  # $0.60 * 7.3
            ),
            "gpt-4o": ModelConfig(
                model_name="gpt-4o",
                base_url="https://api.openai.com/v1",
                api_key=os.getenv("OPENAI_API_KEY", ""),
                description="OpenAI GPT-4o - 旗舰多模态",
                input_price_per_1m=18.25,   # $2.50 * 7.3
                output_price_per_1m=73.00,  # $10.00 * 7.3
            ),
        },
        "deepseek": {
            "deepseek-chat": ModelConfig(
                model_name="deepseek-chat",
                base_url="https://api.deepseek.com",
                api_key=os.getenv("DEEPSEEK_API_KEY", ""),
                description="DeepSeek-V3 - 中文首选",
                input_price_per_1m=2.00,
                output_price_per_1m=8.00,
            ),
            "deepseek-reasoner": ModelConfig(
                model_name="deepseek-reasoner",
                base_url="https://api.deepseek.com",
                api_key=os.getenv("DEEPSEEK_API_KEY", ""),
                description="DeepSeek-R1 - 深度推理",
                input_price_per_1m=4.00,
                output_price_per_1m=16.00,
            ),
        },
        "dashscope": {
            "qwen-plus": ModelConfig(
                model_name="qwen-plus",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key=os.getenv("DASHSCOPE_API_KEY", ""),
                description="通义千问 Qwen-Plus - 性价比均衡",
                input_price_per_1m=0.80,
                output_price_per_1m=2.00,
            ),
            "qwen-turbo": ModelConfig(
                model_name="qwen-turbo",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key=os.getenv("DASHSCOPE_API_KEY", ""),
                description="通义千问 Qwen-Turbo - 极速响应",
                input_price_per_1m=0.30,
                output_price_per_1m=0.60,
            ),
        },
    }

    @classmethod
    def get(cls, provider: str, model_key: str) -> Optional[ModelConfig]:
        """获取指定平台和模型的配置"""
        provider_configs = cls.REGISTRY.get(provider, {})
        return provider_configs.get(model_key)

    @classmethod
    def list_all(cls) -> list:
        """列出所有可用模型"""
        results = []
        for provider, models in cls.REGISTRY.items():
            for key, config in models.items():
                results.append({
                    "provider": provider,
                    "key": key,
                    "model": config.model_name,
                    "desc": config.description,
                })
        return results

# ==================== 成本追踪器 ====================

@dataclass
class CostTracker:
    """全局成本追踪"""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_rmb: float = 0.0
    call_count: int = 0
    history: List[UsageStats] = field(default_factory=list)

    def record(self, stats: UsageStats):
        self.total_input_tokens += stats.input_tokens
        self.total_output_tokens += stats.output_tokens
        self.total_cost_rmb += stats.cost_rmb
        self.call_count += 1
        self.history.append(stats)

    def print_summary(self):
        table = Table(title="📊 API调用成本汇总")
        table.add_column("指标", style="cyan", no_wrap=True)
        table.add_column("数值", style="magenta")
        table.add_row("调用次数", str(self.call_count))
        table.add_row("总输入Token", f"{self.total_input_tokens:,}")
        table.add_row("总输出Token", f"{self.total_output_tokens:,}")
        table.add_row("总费用", f"¥{self.total_cost_rmb:.4f}")
        if self.call_count > 0:
            table.add_row("平均每次费用", f"¥{self.total_cost_rmb/self.call_count:.4f}")
        console.print(table)

# ==================== 核心封装类 ====================

class MultiLLM:
    """
    多平台LLM统一封装类

    使用示例:
        llm = MultiLLM()
        llm.switch_provider("deepseek", "deepseek-chat")
        response = llm.chat("你好，请介绍一下自己")
        llm.stream_chat("用Python写一个快速排序")
        llm.print_cost_summary()
    """

    # 默认参数
    DEFAULT_SYSTEM_PROMPT = "你是一个有帮助的AI助手。"

    def __init__(
        self,
        default_provider: str = "deepseek",
        default_model_key: str = "deepseek-chat",
    ):
        """
        初始化 MultiLLM

        Args:
            default_provider: 默认平台 (openai / deepseek / dashscope)
            default_model_key: 默认模型key
        """
        self.current_provider = default_provider
        self.current_model_key = default_model_key
        self.current_config: Optional[ModelConfig] = None
        self.client: Optional[OpenAI] = None

        # 对话历史（仅保留在当前实例中）
        self.conversation_history: List[Dict[str, str]] = []

        # 成本追踪
        self.cost_tracker = CostTracker()

        # 初始化客户端
        self._init_client()

    # ========== 内部方法 ==========

    def _init_client(self):
        """初始化当前平台的客户端"""
        config = ProviderRegistry.get(self.current_provider, self.current_model_key)

        if config is None:
            available = [
                f"{p}/{m}"
                for item in ProviderRegistry.list_all()
                for p, m in [(item["provider"], item["key"])]
            ]
            raise ValueError(
                f"未找到平台/模型配置: {self.current_provider}/{self.current_model_key}\n"
                f"可用的配置: {available}"
            )

        if not config.api_key:
            env_var_map = {
                "openai": "OPENAI_API_KEY",
                "deepseek": "DEEPSEEK_API_KEY",
                "dashscope": "DASHSCOPE_API_KEY",
            }
            env_var = env_var_map.get(self.current_provider, "API_KEY")
            raise ValueError(
                f"❌ 未配置 {self.current_provider} 的API Key。\n"
                f"请在 .env 文件中设置 {env_var}=你的密钥"
            )

        self.current_config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )
        console.print(
            f"✅ 已连接: [bold green]{self.current_provider}[/bold green] "
            f"→ {config.model_name} ({config.description})"
        )

    def _validate_provider(self) -> None:
        """验证当前配置是否有效，如无效则尝试修复"""
        if self.client is None or self.current_config is None:
            self._init_client()

    def _calculate_cost(self, model_config: ModelConfig, input_tokens: int, output_tokens: int) -> float:
        """计算调用成本（人民币）"""
        return (
            input_tokens / 1_000_000
        ) * model_config.input_price_per_1m + (
            output_tokens / 1_000_000
        ) * model_config.output_price_per_1m

    def _build_messages(self, user_message: str, system_message: Optional[str] = None) -> list:
        """构建完整的消息列表"""
        messages = []

        # 添加系统消息
        sys_msg = system_message or self.DEFAULT_SYSTEM_PROMPT
        messages.append({"role": "system", "content": sys_msg})

        # 添加历史对话
        messages.extend(self.conversation_history)

        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})

        return messages

    # ========== 公开方法 ==========

    def switch_provider(self, provider: str, model_key: str) -> None:
        """
        切换LLM平台和模型

        Args:
            provider: 平台名 (openai / deepseek / dashscope)
            model_key: 模型key (如 "deepseek-chat", "gpt-4o-mini")

        Example:
            llm.switch_provider("openai", "gpt-4o-mini")
            llm.switch_provider("dashscope", "qwen-plus")
        """
        if provider not in ProviderRegistry.REGISTRY:
            raise ValueError(
                f"❌ 不支持的平台: {provider}\n"
                f"可用平台: {list(ProviderRegistry.REGISTRY.keys())}"
            )

        self.current_provider = provider
        self.current_model_key = model_key
        self._init_client()

    def chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        save_history: bool = True,
    ) -> str:
        """
        非流式对话（返回完整响应）

        Args:
            user_message: 用户消息
            system_message: 系统提示词（None则使用默认）
            temperature: 温度参数 (0.0-2.0)
            max_tokens: 最大输出token数
            save_history: 是否将本轮对话保存到历史

        Returns:
            模型的完整文本响应
        """
        self._validate_provider()
        messages = self._build_messages(user_message, system_message)

        try:
            start_time = time.time()

            response = self.client.chat.completions.create(
                model=self.current_config.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            latency = time.time() - start_time

            # 提取响应文本
            reply = response.choices[0].message.content or ""

            # 提取用量信息
            usage = response.usage
            input_tokens = usage.prompt_tokens if usage else 0
            output_tokens = usage.completion_tokens if usage else 0

            # 记录成本
            cost = self._calculate_cost(self.current_config, input_tokens, output_tokens)
            self.cost_tracker.record(UsageStats(
                model=self.current_config.model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_rmb=cost,
                latency_seconds=latency,
            ))

            # 保存历史
            if save_history:
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": reply})

            return reply

        except Exception as e:
            console.print(f"[bold red]❌ API调用失败: {e}[/bold red]")
            raise

    def stream_chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        save_history: bool = True,
    ) -> str:
        """
        流式对话（逐步显示响应，打字机效果）

        Args:
            user_message: 用户消息
            system_message: 系统提示词
            temperature: 温度参数
            max_tokens: 最大输出token数
            save_history: 是否保存到历史

        Returns:
            完整的响应文本
        """
        self._validate_provider()
        messages = self._build_messages(user_message, system_message)

        try:
            start_time = time.time()

            stream = self.client.chat.completions.create(
                model=self.current_config.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,  # 关键：开启流式
                stream_options={"include_usage": True},  # 在最后chunk包含usage信息
            )

            full_reply = ""
            console.print(f"\n🤖 [bold cyan]{self.current_config.model_name}[/bold cyan]:")
            console.print("─" * 60)

            # 使用 rich Live 实现打字机效果
            with Live(Markdown(""), console=console, refresh_per_second=10, vertical_overflow="visible") as live:
                input_tokens = 0
                output_tokens = 0

                for chunk in stream:
                    # 最后一个chunk可能包含usage信息
                    if chunk.usage:
                        input_tokens = chunk.usage.prompt_tokens
                        output_tokens = chunk.usage.completion_tokens
                        continue

                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            full_reply += delta.content
                            live.update(Markdown(full_reply))

            latency = time.time() - start_time

            console.print("─" * 60)
            console.print(
                f"⏱ 耗时: {latency:.1f}s | "
                f"📥 {input_tokens} tokens入 | "
                f"📤 {output_tokens} tokens出"
            )

            # 记录成本
            if input_tokens > 0 or output_tokens > 0:
                cost = self._calculate_cost(self.current_config, input_tokens, output_tokens)
                self.cost_tracker.record(UsageStats(
                    model=self.current_config.model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_rmb=cost,
                    latency_seconds=latency,
                ))
            else:
                # 某些平台可能不返回usage，使用估算
                estimated_output = len(full_reply) // 2
                cost = self._calculate_cost(self.current_config, len(user_message) // 2, estimated_output)
                self.cost_tracker.record(UsageStats(
                    model=self.current_config.model_name,
                    input_tokens=len(user_message) // 2,
                    output_tokens=estimated_output,
                    cost_rmb=cost,
                    latency_seconds=latency,
                ))

            # 保存历史
            if save_history:
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": full_reply})

            return full_reply

        except KeyboardInterrupt:
            console.print("\n⚠ [yellow]用户中断了流式输出[/yellow]")
            return full_reply if 'full_reply' in dir() else ""
        except Exception as e:
            console.print(f"[bold red]❌ 流式调用失败: {e}[/bold red]")
            raise

    def clear_history(self) -> None:
        """清空对话历史"""
        cleared_count = len(self.conversation_history)
        self.conversation_history = []
        console.print(f"🗑 已清空 {cleared_count} 条历史对话记录")

    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history.copy()

    def print_history(self) -> None:
        """打印对话历史"""
        if not self.conversation_history:
            console.print("[dim]对话历史为空[/dim]")
            return

        console.print(f"\n📜 [bold]对话历史 ({len(self.conversation_history)//2} 轮):[/bold]")
        for i, msg in enumerate(self.conversation_history):
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            role_name = "用户" if msg["role"] == "user" else "模型"
            content_preview = msg["content"][:80] + ("..." if len(msg["content"]) > 80 else "")
            console.print(f"  {role_icon} [{i//2+1}] {role_name}: {content_preview}")

    def print_cost_summary(self) -> None:
        """打印成本汇总"""
        self.cost_tracker.print_summary()

    def compare_models(
        self,
        question: str,
        configs: List[tuple] = None,
    ) -> Dict:
        """
        多模型对比：向多个平台发送相同问题，对比结果

        Args:
            question: 要测试的问题
            configs: [(provider, model_key), ...] 要对比的平台模型列表

        Returns:
            {model_label: {"response": str, "latency": float, "cost": float}}
        """
        if configs is None:
            configs = [
                ("deepseek", "deepseek-chat"),
                ("openai", "gpt-4o-mini"),
                ("dashscope", "qwen-plus"),
            ]

        results = {}

        for provider, model_key in configs:
            config = ProviderRegistry.get(provider, model_key)
            if config is None:
                console.print(f"[yellow]⚠ 跳过 {provider}/{model_key}（配置未找到）[/yellow]")
                continue

            label = f"{provider}/{model_key}"
            console.print(f"\n📡 [bold blue]调用 {label}...[/bold blue]")

            # 临时切换平台
            original_provider = self.current_provider
            original_model = self.current_model_key

            try:
                self.switch_provider(provider, model_key)
                start = time.time()
                response = self.chat(question, save_history=False)
                latency = time.time() - start

                # 获取最近一次的成本
                last_usage = self.cost_tracker.history[-1] if self.cost_tracker.history else None
                cost = last_usage.cost_rmb if last_usage else 0

                results[label] = {
                    "response": response,
                    "latency": latency,
                    "cost": cost,
                }
            except Exception as e:
                results[label] = {
                    "response": f"❌ 调用失败: {e}",
                    "latency": 0,
                    "cost": 0,
                }
            finally:
                # 恢复原平台
                self.current_provider = original_provider
                self.current_model_key = original_model
                self._init_client()

        return results


# ==================== 便捷函数 ====================

def create_llm(provider: str = "deepseek", model: str = "deepseek-chat") -> MultiLLM:
    """快速创建 MultiLLM 实例"""
    return MultiLLM(default_provider=provider, default_model_key=model)


# ==================== 自测代码 ====================

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]MultiLLM 多平台统一封装[/bold cyan]\n"
        "支持 OpenAI / DeepSeek / 阿里云百炼(通义千问)",
        border_style="cyan"
    ))

    # 列出可用模型
    console.print("\n📋 [bold]可用模型列表:[/bold]")
    for item in ProviderRegistry.list_all():
        console.print(
            f"  [cyan]{item['provider']}/{item['key']}[/cyan] "
            f"→ {item['model']} ({item['desc']})"
        )

    # 创建实例（默认使用DeepSeek）
    llm = MultiLLM(default_provider="deepseek", default_model_key="deepseek-chat")

    # 测试非流式对话
    console.print("\n" + "="*60)
    console.print("[bold]测试1: 非流式对话[/bold]")
    reply = llm.chat("用一句话介绍Python语言")
    console.print(f"\n回复: {reply}")

    # 测试流式对话
    console.print("\n" + "="*60)
    console.print("[bold]测试2: 流式对话（打字机效果）[/bold]")
    llm.stream_chat("用50字简介深度学习的核心思想")

    # 查看成本和历史
    console.print("\n" + "="*60)
    llm.print_history()
    llm.print_cost_summary()

    # 测试跨平台对比
    console.print("\n" + "="*60)
    console.print("[bold]测试3: 多模型对比（同问题问不同平台）[/bold]")
    results = llm.compare_models(
        question="什么是机器学习中的过拟合？请用一句话解释。",
    )
    for label, data in results.items():
        console.print(f"\n[bold]{label}[/bold]:")
        console.print(f"  回复: {data['response'][:100]}...")
        console.print(f"  耗时: {data['latency']:.1f}s | 费用: ¥{data['cost']:.4f}")
```

---

### 实操2：多平台切换与对比（20分钟）

> **目标**：使用MultiLLM类，向3个平台发送相同问题，对比质量、速度和成本差异。

#### 对比实验脚本

创建文件 `model_compare_demo.py`：

```python
"""
模型对比实验：同一问题，多个平台，质量/速度/成本对比
"""

from multillm import MultiLLM, ProviderRegistry
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console()

# 测试问题集（涵盖不同类型）
TEST_QUESTIONS = [
    {
        "category": "事实问答",
        "question": "光合作用的基本过程是什么？请用2-3句话简要说明。",
    },
    {
        "category": "代码生成",
        "question": "用Python写一个函数，判断一个字符串是否为回文。只需给出代码。",
    },
    {
        "category": "中文理解",
        "question": '"塞翁失马，焉知非福" 这个成语是什么意思？请简要解释。',
    },
    {
        "category": "创意写作",
        "question": "用一句话赞美秋天，要求使用比喻修辞。",
    },
]

# 要对比的平台和模型
COMPARISON_CONFIGS = [
    ("deepseek", "deepseek-chat", "DeepSeek-V3"),
    ("openai", "gpt-4o-mini", "GPT-4o-mini"),
    ("dashscope", "qwen-plus", "Qwen-Plus"),
]


def run_comparison():
    """运行完整的对比实验"""
    console.print(Panel.fit(
        "[bold cyan]🔬 多平台模型对比实验[/bold cyan]\n"
        f"测试 {len(TEST_QUESTIONS)} 类问题 × {len(COMPARISON_CONFIGS)} 个模型",
        border_style="cyan"
    ))

    llm = MultiLLM(default_provider="deepseek", default_model_key="deepseek-chat")

    # 汇总统计
    all_results = []

    for question_item in TEST_QUESTIONS:
        category = question_item["category"]
        question = question_item["question"]

        console.print(f"\n{'='*70}")
        console.print(f"[bold yellow]📝 测试类别: {category}[/bold yellow]")
        console.print(f"[dim]问题: {question}[/dim]")

        for provider, model_key, display_name in COMPARISON_CONFIGS:
            console.print(f"\n  🚀 [bold blue]{display_name}[/bold blue] 调用中...", end=" ")

            # 切换到目标平台
            try:
                llm.switch_provider(provider, model_key)

                # 调用并计时
                start = time.time()
                response = llm.chat(question, save_history=False)
                latency = time.time() - start

                # 获取成本
                last = llm.cost_tracker.history[-1] if llm.cost_tracker.history else None
                input_tokens = last.input_tokens if last else 0
                output_tokens = last.output_tokens if last else 0
                cost = last.cost_rmb if last else 0

                all_results.append({
                    "category": category,
                    "model": display_name,
                    "response": response,
                    "latency": latency,
                    "cost": cost,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "status": "✅",
                })

                console.print(f"[green]✓ {latency:.1f}s[/green]")

            except Exception as e:
                all_results.append({
                    "category": category,
                    "model": display_name,
                    "response": str(e),
                    "latency": 0,
                    "cost": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "status": "❌",
                })
                console.print(f"[red]✗ 失败: {e}[/red]")

    # ========== 汇总报告 ==========

    console.print("\n\n" + "="*70)
    console.print("[bold cyan]📊 对比实验汇总报告[/bold cyan]")

    # 表格1: 性能对比
    table = Table(title="各模型性能对比")
    table.add_column("模型", style="cyan")
    table.add_column("平均耗时", style="yellow", justify="right")
    table.add_column("成功/总数", style="magenta", justify="center")
    table.add_column("总费用(￥)", style="green", justify="right")

    model_stats = {}
    for r in all_results:
        model = r["model"]
        if model not in model_stats:
            model_stats[model] = {
                "total_latency": 0,
                "success": 0,
                "total": 0,
                "total_cost": 0,
            }
        stats = model_stats[model]
        stats["total_latency"] += r["latency"]
        stats["total_cost"] += r["cost"]
        stats["total"] += 1
        if r["status"] == "✅":
            stats["success"] += 1

    for model, stats in model_stats.items():
        avg_latency = stats["total_latency"] / stats["total"] if stats["total"] > 0 else 0
        table.add_row(
            model,
            f"{avg_latency:.2f}s",
            f"{stats['success']}/{stats['total']}",
            f"{stats['total_cost']:.4f}",
        )

    console.print(table)

    # 表格2: 各问题类别的响应预览
    console.print("\n[bold]各模型响应对比:[/bold]")
    for question_item in TEST_QUESTIONS:
        category = question_item["category"]
        console.print(f"\n[bold yellow]【{category}】[/bold yellow]")

        for r in all_results:
            if r["category"] == category:
                preview = r["response"][:120].replace("\n", " ")
                console.print(
                    f"  [{r['model']:15s}] "
                    f"({r['latency']:.1f}s, ¥{r['cost']:.4f}) "
                    f"{preview}..."
                )

    # 最终成本汇总
    llm.print_cost_summary()


if __name__ == "__main__":
    run_comparison()
```

---

### 实操3：流式对话应用（20分钟）

> **目标**：构建一个完整的流式对话应用，支持实时显示、平台切换和历史管理。

#### 流式对话应用

创建文件 `streaming_chat_app.py`：

```python
"""
流式对话应用 - 带平台切换和历史管理的终端聊天程序
"""

import sys
import os

# 确保能找到 multillm 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multillm import MultiLLM, ProviderRegistry
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown

console = Console()


class StreamingChatApp:
    """流式对话应用主类"""

    COMMANDS = {
        "/help": "显示帮助信息",
        "/switch": "切换模型平台 用法: /switch <平台> <模型>",
        "/list": "列出所有可用模型",
        "/history": "查看对话历史",
        "/clear": "清空对话历史",
        "/cost": "查看API调用成本",
        "/system": "设置系统提示词 用法: /system <提示词>",
        "/stream": "切换流式/非流式模式 用法: /stream on|off",
        "/quit": "退出程序",
    }

    def __init__(self):
        self.llm = MultiLLM(default_provider="deepseek", default_model_key="deepseek-chat")
        self.stream_mode = True
        self.custom_system_prompt = None

    def show_welcome(self):
        """显示欢迎界面"""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]💬 流式对话应用[/bold cyan]\n\n"
            "[dim]一个支持多平台切换的流式AI聊天终端[/dim]\n\n"
            f"[green]当前平台:[/green] {self.llm.current_provider}\n"
            f"[green]当前模型:[/green] {self.llm.current_config.model_name}\n"
            f"[green]响应模式:[/green] {'⚡ 流式' if self.stream_mode else '📦 非流式'}\n\n"
            "[dim]输入 /help 查看可用命令[/dim]",
            border_style="cyan",
            padding=(1, 2),
        ))

    def show_help(self):
        """显示帮助信息"""
        table = Table(title="可用命令")
        table.add_column("命令", style="cyan")
        table.add_column("说明", style="white")

        for cmd, desc in self.COMMANDS.items():
            table.add_row(cmd, desc)

        console.print(table)

    def handle_command(self, user_input: str) -> bool:
        """
        处理命令输入。返回 True 表示继续对话，False 表示退出。
        """
        parts = user_input.strip().split(maxsplit=2)
        cmd = parts[0].lower()

        if cmd == "/quit" or cmd == "/exit":
            console.print("[yellow]👋 再见！[/yellow]")
            return False

        elif cmd == "/help":
            self.show_help()

        elif cmd == "/list":
            table = Table(title="可用模型列表")
            table.add_column("平台", style="cyan")
            table.add_column("模型Key", style="green")
            table.add_column("模型名", style="yellow")
            table.add_column("说明", style="white")

            for item in ProviderRegistry.list_all():
                table.add_row(
                    item["provider"],
                    item["key"],
                    item["model"],
                    item["desc"],
                )
            console.print(table)

        elif cmd == "/switch":
            if len(parts) < 3:
                console.print("[red]用法: /switch <平台> <模型>[/red]")
                console.print(
                    "例如: /switch openai gpt-4o-mini\n"
                    "     /switch deepseek deepseek-chat\n"
                    "     /switch dashscope qwen-plus"
                )
            else:
                provider = parts[1].lower()
                model_key = parts[2].lower()
                try:
                    self.llm.switch_provider(provider, model_key)
                    console.print(
                        f"[green]✅ 已切换到 {provider}/{model_key}[/green]"
                    )
                except Exception as e:
                    console.print(f"[red]❌ 切换失败: {e}[/red]")

        elif cmd == "/history":
            self.llm.print_history()

        elif cmd == "/clear":
            self.llm.clear_history()

        elif cmd == "/cost":
            self.llm.print_cost_summary()

        elif cmd == "/system":
            if len(parts) < 2:
                console.print("[red]用法: /system <提示词>[/red]")
                console.print(
                    f"当前自定义提示词: "
                    f"{self.custom_system_prompt or '未设置（使用默认）'}"
                )
            else:
                self.custom_system_prompt = parts[1]
                console.print(
                    f"[green]✅ 系统提示词已更新: {self.custom_system_prompt[:50]}...[/green]"
                )

        elif cmd == "/stream":
            if len(parts) < 2:
                console.print("[red]用法: /stream on|off[/red]")
            elif parts[1].lower() in ("on", "true", "1"):
                self.stream_mode = True
                console.print("[green]✅ 已切换到流式模式[/green]")
            elif parts[1].lower() in ("off", "false", "0"):
                self.stream_mode = False
                console.print("[yellow]✅ 已切换到非流式模式[/yellow]")
            else:
                console.print("[red]用法: /stream on|off[/red]")

        else:
            console.print(f"[red]未知命令: {cmd}。输入 /help 查看可用命令。[/red]")

        return True  # 继续对话

    def handle_chat(self, user_input: str) -> None:
        """处理普通聊天消息"""
        try:
            if self.stream_mode:
                self.llm.stream_chat(
                    user_input,
                    system_message=self.custom_system_prompt,
                )
            else:
                console.print(
                    f"\n🤖 [bold cyan]{self.llm.current_config.model_name}[/bold cyan]:"
                )
                reply = self.llm.chat(
                    user_input,
                    system_message=self.custom_system_prompt,
                )
                console.print(Markdown(reply))
        except Exception as e:
            console.print(f"[red]❌ 对话出错: {e}[/red]")

    def run(self):
        """主循环"""
        self.show_welcome()

        while True:
            try:
                user_input = Prompt.ask("\n[bold green]👤 你[/bold green]")

                if not user_input.strip():
                    continue

                # 判断是命令还是普通对话
                if user_input.startswith("/"):
                    should_continue = self.handle_command(user_input)
                    if not should_continue:
                        break
                else:
                    self.handle_chat(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]👋 再见！[/yellow]")
                break
            except EOFError:
                break

        # 退出前显示成本汇总
        if self.llm.cost_tracker.call_count > 0:
            console.print()
            self.llm.print_cost_summary()


# ==================== 主入口 ====================

if __name__ == "__main__":
    app = StreamingChatApp()
    app.run()
```

#### 运行方式

```bash
# 确保 .env 文件配置了至少一个平台的API Key

# 运行流式对话应用
python streaming_chat_app.py

# 运行模型对比实验
python model_compare_demo.py

# 测试MultiLLM封装类
python multillm.py
```

#### 应用交互演示

```
💬 流式对话应用
当前平台: deepseek
当前模型: deepseek-chat
响应模式: ⚡ 流式

👤 你: 你好，请用Python写一个斐波那契数列生成器

🤖 deepseek-chat:
──────────────────────────────────────────────────
def fibonacci(n):
    """生成前n个斐波那契数"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 使用示例
for num in fibonacci(10):
    print(num, end=' ')
# 输出: 0 1 1 2 3 5 8 13 21 34
──────────────────────────────────────────────────
⏱ 耗时: 1.2s | 📥 45 tokens入 | 📤 156 tokens出

👤 你: /switch openai gpt-4o-mini
✅ 已切换到 openai/gpt-4o-mini

👤 你: 用同样的题目，你怎么回答？

🤖 gpt-4o-mini:
──────────────────────────────────────────────────
[GPT-4o-mini 的流式响应...]
──────────────────────────────────────────────────

👤 你: /cost
📊 API调用成本汇总
调用次数: 2
总输入Token: 112
总输出Token: 389
总费用: ¥0.0023

👤 你: /quit
👋 再见！
```

---

## 六、课后作业

### 作业：构建"模型对比器"（Model Comparator）

**任务描述**：
开发一个命令行工具，能够向2-3个不同平台的LLM发送相同问题，并以格式化表格输出对比结果。

**基本要求（60分）**：

1. 支持至少两个平台（DeepSeek + OpenAI 或 DeepSeek + 通义千问）
2. 用户可输入问题，工具向所有已配置的平台发送相同问题
3. 以表格形式输出各平台的响应、耗时和费用
4. 正确处理API Key配置（从.env读取）

**进阶要求（30分）**：

5. 支持流式输出模式：各平台响应"同时"出现（用多线程实现并发调用）
6. 内置评分系统：用GPT-4o-mini作为"裁判"，评判各平台回答质量（1-10分）
7. 支持批量测试：从JSON文件读入多个问题，生成CSV汇总报告

**附加挑战（10分）**：

8. 添加"最佳性价比"计算：综合质量评分和成本，推荐最优选择
9. 支持Web界面（使用Gradio实现）

**提交内容**：
- `model_comparator.py` 源代码
- `results/sample_output.txt` 示例运行输出
- `README.md` 使用说明

**评分标准**：

| 评分维度 | 权重 | 说明 |
|---------|------|------|
| 功能完整性 | 40% | 核心对比功能是否完整可用 |
| 代码质量 | 25% | 代码结构清晰、注释充分、异常处理完善 |
| 用户体验 | 20% | 输出清晰美观，交互流畅 |
| 创新与扩展 | 15% | 额外功能的实现质量 |

**作业提示**：

```python
# 多线程并发调用的基本框架
from concurrent.futures import ThreadPoolExecutor, as_completed

def call_model(provider, model, question):
    """单个模型调用函数"""
    llm = MultiLLM(default_provider=provider, default_model_key=model)
    start = time.time()
    response = llm.chat(question, save_history=False)
    latency = time.time() - start
    last_usage = llm.cost_tracker.history[-1]
    return {
        "model": f"{provider}/{model}",
        "response": response,
        "latency": latency,
        "cost": last_usage.cost_rmb,
    }

# 并发调用
configs = [
    ("deepseek", "deepseek-chat"),
    ("openai", "gpt-4o-mini"),
    ("dashscope", "qwen-plus"),
]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(call_model, p, m, question): f"{p}/{m}"
        for p, m in configs
    }
    for future in as_completed(futures):
        result = future.result()
        print(f"✓ {result['model']}: {result['latency']:.1f}s")
```

---

## 七、拓展阅读

### 7.1 官方文档

| 资源 | 链接 | 说明 |
|------|------|------|
| OpenAI API 文档 | https://platform.openai.com/docs | 最完善的LLM API文档，推荐优先阅读 |
| DeepSeek API 文档 | https://platform.deepseek.com/api-docs | 国产替代首选，兼容OpenAI格式 |
| 阿里云百炼文档 | https://help.aliyun.com/zh/model-studio | 通义千问官方文档 |
| Anthropic API 文档 | https://docs.anthropic.com | Claude API参考，含MCP和Tool Use |
| OpenAI Python SDK | https://github.com/openai/openai-python | SDK源码，可学习底层实现 |

### 7.2 进阶主题

| 主题 | 推荐资源 | 说明 |
|------|---------|------|
| **Function Calling** | OpenAI Function Calling Guide | 让模型调用外部工具和API |
| **结构化输出** | OpenAI Structured Outputs | JSON Schema约束输出格式 |
| **Prompt Caching** | Anthropic Prompt Caching | 减少重复system prompt的token成本 |
| **Batch API** | OpenAI Batch API | 异步批处理，半价优惠，24小时完成 |
| **Assistants API** | OpenAI Assistants API | 托管多轮对话，内置RAG和Code Interpreter |
| **MCP协议** | Anthropic MCP Specification | 跨模型的工具调用标准协议 |
| **LangChain** | https://python.langchain.com | 更高级的LLM应用框架 |

### 7.3 推荐阅读

1. **《Building LLM Apps》** by Valentina Alto —— 实战导向的LLM应用开发指南
2. **OpenAI Cookbook** (https://cookbook.openai.com) —— 官方示例集合，包含最佳实践
3. **《Patterns for Building LLM-based Systems》** (eugeneyan.com) —— LLM系统设计的经典博文
4. **DeepSeek技术报告** —— 了解MoE架构如何实现极致性价比
5. **"What We Learned from a Year of Building with LLMs"** —— 来自业界实践者的经验总结

---

## 八、常见问题

### Q1: 为什么DeepSeek和通义千问可以直接用OpenAI SDK调用？

**答**：DeepSeek和阿里云百炼的API设计有意兼容了OpenAI的接口规范（`/v1/chat/completions`），这意味着只需修改 `base_url` 和 `api_key`，就可以复用OpenAI SDK的全部功能。这种设计降低了开发者的迁移成本，也是社区广泛采用的实践。但需注意：

- 部分高级参数（如 `response_format`、`logprobs`）各平台支持程度不同
- Streaming的 `usage` 信息返回方式可能存在差异
- 建议查阅各平台文档确认参数兼容性

### Q2: 流式输出会影响回答质量吗？

**答**：**不会**。流式和非流式调用使用相同的模型和参数，最终生成的文本完全相同。区别仅在于传输方式——流式将响应分块发送，提供更好的用户体验。唯一的细微差异是：如果用户在流式过程中按Ctrl+C中断，获得的回答是不完整的，但在非流式模式下无法中途中断。

### Q3: 如何选择合适的temperature值？

**答**：遵循以下原则：

- **需要事实准确**（代码、数学、翻译、问答）→ temperature = 0.0 ~ 0.3
- **需要自然多样**（聊天、客服、助手）→ temperature = 0.7 ~ 0.9
- **需要创意发散**（写作、头脑风暴、广告文案）→ temperature = 1.0 ~ 1.5
- **不确定时** → temperature = 0.7（大多数模型的默认值）

### Q4: 为什么我调用的费用比官网标价高？

**答**：可能原因：

1. **忘了计算system prompt的token**：每次请求都会将完整的system prompt发送给模型
2. **对话历史累积**：多轮对话中，历史消息每次都重新发送
3. **输出超出预期**：`max_tokens` 设得太大，模型实际输出了更多内容
4. **streaming的usage不完整**：部分平台在流式模式下不返回usage信息，需用 `stream_options={"include_usage": True}`
5. **价格变动**：各平台价格会调整，确保使用最新的价格表

### Q5: 如何处理网络不稳定导致的调用失败？

**答**：推荐三层防护：

```python
# 第1层: 客户端重试（指数退避）
# 第2层: 超时设置
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=60.0,  # 60秒超时
    max_retries=3,  # SDK内置重试
)

# 第3层: 应用层重试 + 模型降级
try:
    response = primary_llm.chat(question)
except Exception:
    print("主模型调用失败，降级到备用模型...")
    response = fallback_llm.chat(question)
```

### Q6: 多个用户同时使用，API Key会互相影响吗？

**答**：API Key本身是全局的，但需要注意：

- **速率限制（Rate Limit）** 是Key级别的：所有用户共享同一个Key的频率限制
- **计费**是Key级别汇总的：无法区分哪个用户产生了多少费用
- **生产环境建议**：为不同用户/租户分配不同的API Key（OpenAI支持创建多个Key；也可用API Proxy网关做Key管理）

### Q7: DeepSeek的API Key怎么获取？可以充值吗？

**答**：
1. 访问 https://platform.deepseek.com 注册账号
2. 进入"API Keys"页面创建密钥
3. DeepSeek采用预充值模式，在"充值"页面进行充值（支持支付宝）
4. 新用户通常有免费额度（政策可能变动，请以官网公告为准）
5. 定价极低，¥10可以调用约百万次简单对话

### Q8: 代码中为什么看不到Claude的调用实现？

**答**：Claude使用Anthropic官方SDK（`anthropic`），接口设计与OpenAI略有不同，因此暂时未包含在基于OpenAI SDK的MultiLLM封装中。如果需要调用Claude，可以参考以下方式扩展：

```python
# Claude调用示例（需要 pip install anthropic）
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 非流式
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}],
)
print(message.content[0].text)

# 流式
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

将其集成到MultiLLM类中，作为第四种provider，将作为本课程的进阶练习内容。

---

*本讲内容为第六周"API开发与集成"的第一课，下一课我们将深入探讨Function Calling与工具集成。*
