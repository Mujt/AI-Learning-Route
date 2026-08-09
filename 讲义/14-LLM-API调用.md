# 第5周 第2课：LLM API 调用实战

> **本课面向双轨受众**：💼 企业管理者/投资人 + 🎓 零基础学习者。本课是"如何在企业中使用AI"的核心实操课——从聊天到做事，从原型到生产。

---

## 一、课程信息

| 项目 | 说明 |
|------|------|
| **周次** | 第 5 周 |
| **课节** | 第 2 课（5-2） |
| **课程主题** | LLM API 调用实战 |
| **课时** | 2 小时（50 分钟讲解 + 70 分钟实操） |
| **前置知识** | Python 基础（函数、类、字典）；GPT 原理（第 5 周第 1 课） |
| **后续关联** | 第 6 周 AI 应用开发、第 7 周 Agent 与 MCP |
| **课程定位** | 从"会用 AI 工具"跨越到"会用代码驱动 AI"，是整个课程的转折点 |

---

## 二、学习目标

完成本课学习后，你应该能够：

**💼 企业决策者**：
- 理解API调用的商业模式：Token计费、模型分层、多供应商策略——这是制定AI采购预算的基础
- 理解Function Calling的战略价值：让AI从"聊天工具"升级为"业务流程执行器"，识别企业中哪些流程适合Function Calling自动化
- 掌握结构化输出的业务意义：AI输出可以被程序可靠解析→自动填入CRM/ERP/数据库→实现端到端自动化
- 建立API Key安全管理意识：理解生产环境中密钥泄露的后果及企业级防护策略

**🎓 零基础学习者**：
- 掌握 OpenAI 兼容 API 的调用模式——理解 `client → messages → create → response` 的核心流程
- 理解 Function Calling（函数调用）机制——这是 Agent 开发的基石
- 理解 Structured Output（结构化输出）——让模型输出可被程序解析的结构化数据
- 掌握流式输出——实现 ChatGPT 那样的打字机效果
- 熟悉至少两个平台的 API——DeepSeek、OpenAI、通义千问

> **核心认知**：学会了 API 调用，你就拿到了通向"AI 应用开发"世界的钥匙。对企业管理者而言，理解了API调用的成本和能力边界，你就有了判断"哪些AI项目值得投入"的决策框架。

---

## 三、课前准备

### 3.1 申请 API Key（上课前必做）

**首推 DeepSeek**（国内直连、注册送免费额度、中文效果好）：

1. 访问 [https://platform.deepseek.com](https://platform.deepseek.com)
2. 点击右上角「登录」→ 使用手机号或微信注册
3. 登录后进入「API Keys」页面，点击「创建 API Key」
4. 复制并**妥善保存** Key（只显示一次！）

> **价格参考**：DeepSeek 当前价格为输入 1 元/百万 tokens，输出 2 元/百万 tokens。新用户注册即送 **500 万 tokens 免费额度**，足够学完整个课程。

**备选方案**：

| 平台 | 注册地址 | 免费额度 | 是否需要 VPN |
|------|----------|----------|-------------|
| **DeepSeek** | platform.deepseek.com | 500 万 tokens | 否 |
| **通义千问（Qwen）** | dashscope.aliyun.com | 100 万 tokens/月 | 否 |
| **OpenAI** | platform.openai.com | $5（新用户） | 是（国内需代理） |
| **智谱 ChatGLM** | open.bigmodel.cn | 100 万 tokens | 否 |

### 3.2 安装 Python 包

在终端执行以下命令：

```bash
# 核心依赖——安装 OpenAI SDK（兼容所有 OpenAI 格式的 API）
pip install openai

# 可选——结构化输出时用到的数据验证库
pip install pydantic

# 可选——环境变量管理
pip install python-dotenv
```

### 3.3 安全配置 API Key（重要！）

**绝对不会出错的 API Key 管理方法：**

```bash
# 第1步：在用户目录创建 .env 文件（不要放在项目文件夹里！）
# Windows PowerShell:
echo DEEPSEEK_API_KEY=sk-your-actual-key-here >> %USERPROFILE%\.env

# Mac/Linux:
echo 'DEEPSEEK_API_KEY=sk-your-actual-key-here' >> ~/.env

# 另外也可以配置其他平台 Key：
echo 'OPENAI_API_KEY=sk-your-openai-key' >> %USERPROFILE%\.env
echo 'QWEN_API_KEY=sk-your-qwen-key' >> %USERPROFILE%\.env
```

```python
# 第2步：在代码中安全加载（不要硬编码 Key！）
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()  # 默认从用户目录找 .env

# 读取 Key（永远不会出现在代码里）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
```

> **安全红线**（请严格遵守）：
> -   **永远不要**把 API Key 直接写在代码里（Git 会记录历史）
> -   **永远不要**把含有 Key 的代码提交到 GitHub
> -   **永远不要**把 Key 截图发到社交媒体（很多人会不小心做到）
> -   如果 Key 意外泄露，**立刻**在平台后台删除旧 Key 并重新生成

> 📊 **企业视角：生产环境API Key安全管理**  
> 
> 个人开发者泄露Key最多损失几十元余额。企业泄露Key的后果完全不同：
> - **真实案例**：某初创公司开发者在GitHub公开仓库中提交了OpenAI API Key，48小时内被恶意脚本盗刷$15,000
> - **风险矩阵**：Key泄露→恶意调用→巨额账单（无上限）→业务中断（Key被平台封禁）→客户数据可能被窃取（如果Key关联了客户对话数据）
> 
> **企业级防护清单**：
> 1. **环境变量 + .gitignore**：所有Key通过.env文件管理，.gitignore必须包含.env
> 2. **GitHub Secret Scanning**：GitHub会自动扫描公开仓库中的API Key格式并通知平台方（OpenAI/DeepSeek等已接入），启用此功能
> 3. **API Key最小权限原则**：不同应用使用不同的Key，限制每个Key的调用权限和速率
> 4. **Key轮换制度**：每季度更换一次生产环境API Key（类似密码轮换）
> 5. **用量异常告警**：在平台后台设置每日消费上限和异常用量告警（如日消耗超过预算2倍时自动暂停）
> 6. **密钥管理服务**：大规模部署时使用云服务商的密钥管理（如AWS Secrets Manager、阿里云KMS）而非手动管理
> 7. **预提交检查**：使用`git-secrets`或`detect-secrets`等工具在git commit前自动扫描敏感信息

---

## 四、核心知识点详解

### 4.1 API 调用基本模式

#### 4.1.1 万能调用模式

所有 OpenAI 兼容的 API（OpenAI、DeepSeek、通义千问、智谱等）都遵循**同一个模式**：

```
创建客户端(Client) → 构建消息列表(Messages) → 调用 create() → 解析响应(Response)
```

这个模式一旦掌握，你就能无缝切换所有平台。

#### 4.1.2 最简代码示例（逐行详解）

```python
# ─── 第1步：导入库 ───
from openai import OpenAI
# openai 是 Python 库名称，但它支持所有 OpenAI 兼容 API
# 不仅限于 OpenAI 公司！DeepSeek、通义千问都用它

# ─── 第2步：创建客户端 ───
client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxxxx",    # 你的 API Key
    base_url="https://api.deepseek.com"  # 重点！这里指定用 DeepSeek
)
# 如果只用 OpenAI 官方，不需要 base_url——这就是兼容的魔力

# ─── 第3步：构建消息 ───
messages = [
    {"role": "system", "content": "你是一个有帮助的AI助手"},
    # system 消息：设定 AI 的行为准则和个性，对话开始时发送一次

    {"role": "user", "content": "什么是机器学习？请用200字简单解释"}
    # user 消息：用户的问题，每次对话发一条
]

# ─── 第4步：调用 API 并获得回复 ───
response = client.chat.completions.create(
    model="deepseek-chat",    # 选择模型
    messages=messages,        # 传入消息列表
    temperature=0.7,          # 控制创造性 (0.0 = 确定, 1.0+ = 随机)
    max_tokens=500,           # 限制最大输出长度
)

# ─── 第5步：提取回复内容 ───
answer = response.choices[0].message.content
# response.choices          → 模型的回复候选列表（通常只有一个）
# [0]                       → 取第一个（也是唯一一个）回复
# .message                  → 回复的消息对象
# .content                  → 消息的文本内容

# ─── 第6步：打印结果 ───
print(answer)

# 可选：查看 Token 消耗
print(f"本次消耗: {response.usage.total_tokens} tokens")
print(f"  输入: {response.usage.prompt_tokens} tokens")
print(f"  输出: {response.usage.completion_tokens} tokens")
```

#### 4.1.3 模型选择指南

| 模型 | 速度 | 能力 | 价格（输入/百万tokens） | 适用场景 |
|------|------|------|------------------------|----------|
| **deepseek-chat** | 快 | 强 | ¥1 | **学习中首选：便宜 + 中文好 + 无需 VPN** |
| **gpt-4o-mini** | 极快 | 中强 | $0.15 | 简单任务、高频调用、原型开发 |
| **gpt-4o** | 中 | 极强 | $2.50 | 复杂推理、代码生成、需要顶级能力时 |
| **qwen-turbo** | 极快 | 中 | 免费额度 | 简单问答、文本处理 |
| **qwen-plus** | 快 | 强 | ¥0.8 | 性价比选择（阿里云生态） |

> **选择建议**：
> - 学习/开发阶段用 **DeepSeek**（不花钱、国内直连）
> - 要做复杂推理或代码生成用 **gpt-4o**（能力最强）
> - 简单批处理用 **gpt-4o-mini** 或 **qwen-turbo**（极快极便宜）

---

### 4.2 消息三角色（system / user / assistant）深度解析

这是最容易被初学者忽略，但又极其重要的概念。三个角色的配合决定了一个 AI 应用的品质。

#### 4.2.1 System —— 设定规则的人

`system` 消息用于定义 AI 的：**身份、行为准则、回答风格、知识边界**。

它只在对话开始时设置一次，对整个对话持续生效。

```python
# ❌ 差 —— 太模糊
system_prompt_bad = "你是一个助手"

# ✅ 好 —— 有身份、有规则、有边界
system_prompt_good = """
你是一位专业的 Python 编程导师，拥有 10 年教学经验。

你的教学风格：
1. 用生活化的比喻解释技术概念（如"列表就像一个可以随时增减物品的书包"）
2. 遇到复杂概念时，拆分成 3-5 个小步骤逐步讲解
3. 永远给出可运行的代码示例，并在关键行用注释解释
4. 每个回答结尾提出一个相关问题，引导学生独立思考

你的行为准则：
- 绝不直接帮学生完成作业，而是引导他们自己找到答案
- 如果学生的代码有错误，先指出"哪里可能有问题"，再给出正确的写法
- 使用中文讲解，但代码中的变量名建议使用英文
"""

messages = [
    {"role": "system", "content": system_prompt_good},
    {"role": "user", "content": "Python 里的装饰器是什么？"}
]
```

**不同场景的 System Prompt 示例**：

```python
# 场景1：翻译机器人
translator_prompt = """
你是一个专业翻译助手，精通中文、英文、日文。
- 翻译要准确传达原文意思，不要随意增减内容
- 专业术语要保持一致性
- 如果是对话类内容，翻译要口语化、自然
"""

# 场景2：代码审查员
code_reviewer_prompt = """
你是一位资深代码审查员。审查代码时请关注：
1. 潜在 Bug 和逻辑错误
2. 安全漏洞（SQL注入、XSS等）
3. 性能瓶颈
4. 代码可读性和命名规范
回复格式：先给出总体评价（1-10分），再逐条列出问题和修改建议。
"""

# 场景3：创意写作伙伴
creative_prompt = """
你是一个充满想象力的创意写作伙伴。请：
- 大胆给出意想不到的点子和剧情转折
- 鼓励用户，但也要诚实指出逻辑上的漏洞
- 对话风格轻松、幽默，像朋友聊天
"""
```

#### 4.2.2 User —— 提出问题的人

`user` 消息代表用户的输入。每一轮对话添加一条。

```python
# user 消息就是用户说的话
{"role": "user", "content": "帮我写一个快速排序的 Python 实现"}
```

> **提示**：user 消息的 content 可以是任何字符串，长度上限取决于模型的上下文窗口。DeepSeek 和 gpt-4o 都支持 128K tokens（大约等于一本 200 页的书）。

#### 4.2.3 Assistant —— 对话的记录者

`assistant` 消息代表 AI 之前的回答。**它的作用不是让 AI"回忆"，而是让 AI"看到"对话历史**。

```python
# 原理：模型本身没有记忆，每次调用都是"全新"的
# 我们需要手动把历史对话拼接进 messages 列表

# 第1轮
messages = [
    {"role": "system", "content": "你是 Python 导师"},
    {"role": "user", "content": "列表和元组有什么区别？"},
]
response_1 = client.chat.completions.create(model="deepseek-chat", messages=messages)
reply_1 = response_1.choices[0].message.content  # AI 的回答

# 第2轮 —— 把之前的对话追加进去！
messages.append({"role": "assistant", "content": reply_1})  # 加入AI第一轮的回答
messages.append({"role": "user", "content": "那什么时候该用元组呢？"})  # 新问题
response_2 = client.chat.completions.create(model="deepseek-chat", messages=messages)
reply_2 = response_2.choices[0].message.content

# 第3轮 —— 继续追加
messages.append({"role": "assistant", "content": reply_2})
messages.append({"role": "user", "content": "给我一个简单例子看看"})
# ... 如此继续
```

**关键理解**：每次 API 调用时，你必须把**完整的历史对话**都传过去。模型每次都是"重新阅读"整个对话历史来理解上下文。

> **处理长对话**：对话太长会超出模型上下文窗口或花很多钱。一般保留最近 10-20 轮即可。

---

### 4.3 关键参数详解

#### 4.3.1 temperature（温度）—— 控制"确定性" vs "创造性"

**范围**：0.0 到 2.0（不同模型略有差异）

| temperature | 效果 | 什么时候用 | 类比 |
|-------------|------|-----------|------|
| **0.0 ~ 0.2** | 几乎每次回答都一样 | 数学计算、代码生成、事实查询、数据提取 | 考试答题——标准答案 |
| **0.3 ~ 0.5** | 基本保持一致的逻辑，措辞有微小变化 | 翻译、文案润色、信息总结 | 公文写作——规范但不死板 |
| **0.7 ~ 0.9** | 有创意但不离谱 | 日常对话、写作辅助、头脑风暴 | 聊天——什么都能聊 |
| **1.0 ~ 1.5** | 非常发散、天马行空 | 创意写作、诗歌、广告文案、角色扮演 | 艺术家——不拘一格 |

```python
# 温度对比实验
query = "写一个关于'下雨天'的简短场景"

# 温度 = 0.0 —— 每次回答基本一致
response_1 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": query}],
    temperature=0.0
)
# 输出：雨滴敲打着窗户，街道上空无一人。路灯在水洼中映出模糊的光晕。

# 温度 = 1.2 —— 每次回答差异很大
response_2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": query}],
    temperature=1.2
)
# 输出（可能）：雨丝像断了线的珠子，噼里啪啦砸在铁皮屋顶上。空气中弥漫着泥土和沥青混合的味道...
```

#### 4.3.2 max_tokens —— 控制预算

```python
# max_tokens 限制模型生成的最大 token 数（1 token ≈ 0.75 个中文字 / 3 个英文字母）
# 这是成本控制的"安全带"

# 短回复场景 —— 限制 100 tokens
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Python 是什么？"}],
    max_tokens=100  # 约 75 个中文字
)

# 长文生成 —— 放开到 2000 tokens
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一篇关于AI发展的800字文章"}],
    max_tokens=2000  # 约 1500 个中文字
)

print(f"实际输出 Token 数: {response.usage.completion_tokens}")
```

> **Token 与价格的直观换算**（以 DeepSeek 为例）：
> - 一次简单问答：约 200 输入 + 300 输出 = 500 tokens ≈ 0.0015 元（不到 1 分钱）
> - 一次长文分析：约 2000 输入 + 3000 输出 = 5000 tokens ≈ 0.02 元（2 分钱）
> - 一本 10 万字小说的 Token 成本：约 130K tokens ≈ 0.5 元（5 毛钱）

#### 4.3.3 top_p（核采样）—— temperature 的替代方案

```python
# top_p = 0.1 表示只从累积概率到 10% 的 Token 中选择（非常集中，确定性高）
# top_p = 0.9 表示从累积概率到 90% 的 Token 中选择（较多样）
# top_p = 1.0 表示考虑所有可能的 Token（最发散）

# 一般规则：只调 temperature 和 top_p 中的一个，不要同时调
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一首关于春天的短诗"}],
    top_p=0.9  # 用 top_p 控制，temperature 使用默认值
)
```

#### 4.3.4 frequency_penalty 和 presence_penalty —— 减少"车轱辘话"

```python
# frequency_penalty — 降低已出现 Token 的重复概率
# 范围: -2.0 到 2.0
# 正值 = 减少重复，负值 = 允许重复

# presence_penalty — 降低已出现话题的再次讨论概率
# 范围: -2.0 到 2.0
# 正值 = 鼓励聊新话题，负值 = 允许围绕同一话题

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "列出10个创业点子"}],
    frequency_penalty=0.5,   # 少说重复词
    presence_penalty=0.3,    # 每个点子的领域尽量不同
)
```

#### 4.3.5 参数组合速查表

| 场景 | temperature | max_tokens | top_p | 其他 |
|------|------------|------------|-------|------|
| **代码生成** | 0.0 ~ 0.1 | 2000 | 1.0（默认） | — |
| **数学计算** | 0.0 | 500 | 1.0 | — |
| **翻译** | 0.2 ~ 0.3 | 与输入等长 | 1.0 | — |
| **日常聊天** | 0.7 | 1000 | 1.0 | — |
| **创意写作** | 1.0 ~ 1.3 | 3000 | 0.95 | frequency_penalty=0.3 |
| **头脑风暴** | 1.2 ~ 1.5 | 2000 | 0.9 | presence_penalty=0.5 |
| **数据提取/分类** | 0.0 | 500 | 1.0 | — |
| **总结摘要** | 0.1 ~ 0.3 | 1000 | 1.0 | — |

---

### 4.4 多平台 API 对比与使用

#### 4.4.1 核心认知：OpenAI 兼容协议

所有主流大模型平台现在都遵循 OpenAI 的 API 格式。这意味着：

- **同一套代码**，只改 `api_key` 和 `base_url` 就能切换平台
- 你学的不是"某个平台的 API"，而是**整个行业的通用标准**

```python
# 切换平台的唯一区别：base_url
# 其他所有代码一模一样！

# ─── OpenAI ───
client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # 不传 base_url，默认就是 api.openai.com
)

# ─── DeepSeek ───
client_deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"  # 就这一行不一样！
)

# ─── 通义千问 ───
client_qwen = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 阿里云的地址
)

# ─── 智谱 ChatGLM ───
client_zhipu = OpenAI(
    api_key=os.getenv("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4"
)
```

#### 4.4.2 统一封装：MultiLLM 类

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class MultiLLM:
    """多平台 LLM 统一调用工具

    演示了如何用一套代码无缝切换 OpenAI / DeepSeek / 通义千问
    """

    # ─── 平台配置（只需要改这里） ───
    CONFIG = {
        "deepseek": {
            "api_key_env": "DEEPSEEK_API_KEY",  # 从环境变量读取
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat",
            "display_name": "DeepSeek"
        },
        "openai": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": None,  # None → 使用 OpenAI 官方地址
            "model": "gpt-4o-mini",
            "display_name": "OpenAI GPT-4o-mini"
        },
        "qwen": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-turbo",
            "display_name": "通义千问 Turbo"
        }
    }

    def __init__(self, provider="deepseek"):
        """初始化并选择平台

        Args:
            provider: "deepseek" | "openai" | "qwen"
        """
        self.provider = provider
        config = self.CONFIG[provider]

        # 从环境变量获取 Key
        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise ValueError(
                f"请设置环境变量 {config['api_key_env']}，或者修改代码直接填入 Key\n"
                f"申请地址: {self._get_signup_url(provider)}"
            )

        # 创建客户端
        kwargs = {"api_key": api_key}
        if config["base_url"]:
            kwargs["base_url"] = config["base_url"]
        self.client = OpenAI(**kwargs)

        self.model = config["model"]
        self.display_name = config["display_name"]
        self.conversation_history = []  # 保存对话历史

    def _get_signup_url(self, provider):
        urls = {
            "deepseek": "https://platform.deepseek.com",
            "openai": "https://platform.openai.com",
            "qwen": "https://dashscope.aliyun.com"
        }
        return urls.get(provider, "未知")

    def chat(self, user_input, system_prompt=None, temperature=0.7):
        """发送消息并获取回复

        Args:
            user_input: 用户输入
            system_prompt: 系统提示词，只在第一轮对话传入
            temperature: 温度参数

        Returns:
            AI 的回复文本
        """
        # 构建完整消息列表
        messages = []

        # 如果提供了 system_prompt，放在最前面
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 拼接历史对话（实现多轮对话）
        messages.extend(self.conversation_history)

        # 添加当前用户问题
        messages.append({"role": "user", "content": user_input})

        # 调用 API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000
        )

        reply = response.choices[0].message.content

        # 保存到历史记录
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": reply})

        # 防止历史过长（保留最近 10 轮 = 20 条消息）
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        # 打印 Token 消耗
        usage = response.usage
        print(f"  [{self.display_name}] "
              f"输入: {usage.prompt_tokens}t "
              f"输出: {usage.completion_tokens}t "
              f"合计: {usage.total_tokens}t")

        return reply

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")

    def switch_provider(self, provider):
        """切换到另一个平台"""
        old = self.display_name
        self.__init__(provider)
        print(f"已从 {old} 切换到 {self.display_name}（历史已清空）")


# ─── 使用示例 ───
if __name__ == "__main__":
    llm = MultiLLM("deepseek")  # 用 DeepSeek（国内直连）

    # 第1轮
    reply_1 = llm.chat(
        "请用三句话介绍你自己",
        system_prompt="你是一个友好的AI助手，每次回答不超过三句话"
    )
    print(f"AI: {reply_1}\n")

    # 第2轮 —— 继承上文语境
    reply_2 = llm.chat("你觉得 Python 适合初学者吗？")
    print(f"AI: {reply_2}\n")

    # 第3轮
    reply_3 = llm.chat("给我推荐一个适合初学者的 Python 项目")
    print(f"AI: {reply_3}\n")

    # 切换平台
    llm.switch_provider("openai")
    reply_4 = llm.chat("用一句话总结今天聊了什么")
    print(f"AI: {reply_4}")
```

#### 4.4.3 各平台价格对比（2026年7月参考）

| 平台 | 模型 | 输入价格 | 输出价格 | 1 万次问答成本（估） | 是否需 VPN |
|------|------|---------|---------|-------------------|-----------|
| **DeepSeek** | deepseek-chat | ¥1/百万t | ¥2/百万t | ≈¥1.5 | 否 |
| **OpenAI** | gpt-4o-mini | $0.15/百万t | $0.60/百万t | ≈$0.38（¥2.7） | 是 |
| **OpenAI** | gpt-4o | $2.50/百万t | $10/百万t | ≈$6.25（¥45） | 是 |
| **通义千问** | qwen-turbo | ¥0.3/百万t | ¥0.6/百万t | ≈¥0.5 | 否 |
| **通义千问** | qwen-plus | ¥0.8/百万t | ¥2/百万t | ≈¥1.4 | 否 |
| **智谱** | glm-4-flash | 免费 | 免费 | ¥0 | 否 |

> **课程推荐**：用 DeepSeek 学习（最便宜 + 中文最好 + 不用 VPN）

> 📊 **企业视角：API成本对比 —— 选择决定年开支差10倍**  
> 
> 企业级用量（每日1万次API调用，每次约800 Token）下，各平台月度成本对比：
> 
> | 平台 | 模型 | 月度API成本（估算） | 年成本 | 备注 |
> |------|------|-------------------|--------|------|
> | **DeepSeek** | deepseek-chat | ￥720 | ￥8,640 | 国内直连、中文最优性价比 |
> | **OpenAI** | gpt-4o-mini | $108（≈￥788） | ≈￥9,456 | 需VPN，综合能力强 |
> | **OpenAI** | gpt-4o | $1,800（≈￥13,140） | ≈￥157,680 | 能力最强，但成本是DeepSeek的18倍 |
> | **通义千问** | qwen-turbo | ￥216 | ￥2,592 | 国内最便宜 |
> | **通义千问** | qwen-plus | ￥576 | ￥6,912 | 性价比均衡 |
> 
> **关键发现**：
> - 同样的任务，GPT-4o比DeepSeek贵18倍，但能力差距远没有18倍
> - 对于中文企业场景，DeepSeek和通义千问的综合性价比远高于OpenAI
> - **建议策略**：日常中文任务用DeepSeek/通义千问；复杂推理/代码/多语言任务按需调用GPT-4o
> 
> **多供应商策略**：不要将企业AI应用绑定到单一API供应商。建议维持至少2个供应商（一个国内+一个国外），既能应对价格变动和服务中断，又能在不同任务上选择最优模型。

---

### 4.5 Function Calling —— 让模型"做事"不只"说话"

> **这是本课最重要的一节！Function Calling 是 Agent 开发的基础设施。**
>
> 普通的 LLM 只会"说话"——生成文字。有了 Function Calling，LLM 可以"做事"——调用外部工具。
>
> 这意味着你的 AI 可以去：查数据库、调用 API、发邮件、控制硬件、执行计算……**模型从"语言生成器"变成了"任务执行器"。**

#### 4.5.1 核心思想：给 LLM 一个"工具箱"

```
┌─────────────────────────────────────────────────────────┐
│              普通对话 vs Function Calling                 │
│                                                         │
│  普通对话:                                               │
│    用户: "北京天气怎么样？"                                │
│    AI:   "抱歉，我无法获取实时信息..."  (❌ 无能为力)      │
│                                                         │
│  Function Calling:                                      │
│    用户: "北京天气怎么样？"                                │
│    AI:   思考 → "我需要调用 get_weather(city='北京')"     │
│    系统: 执行 get_weather("北京") → 返回真实数据           │
│    AI:   "北京今天晴，温度25°C，非常适合出门！" (✅ 准确)   │
└─────────────────────────────────────────────────────────┘
```

#### 4.5.2 完整工作流程（5 个步骤）

```
步驟1: 用户提问（可能需要外部操作）
    "北京天气怎么样？"

步驟2: LLM 分析 → 决定调用哪个函数
    → 返回: tool_call { name: "get_weather", arguments: {"city": "北京"} }

步驟3: 你的代码执行函数
    → get_weather("北京") → {"temp": 25, "weather": "晴"}

步驟4: 函数结果返回给 LLM
    → messages 追加 tool role: {"role": "tool", "content": "{...}"}

步驟5: LLM 基于真实数据生成最终回答
    → "北京今天天气晴朗，温度25°C，非常适合户外活动！"
```

#### 4.5.3 完整代码：天气 + 计算器 Agent

```python
"""
Function Calling 完整示例 —— 天气查询 + 计算器 Agent
这是本课最重要的代码，理解它 = 理解了 Agent 开发的核心
"""
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ─── 初始化客户端 ───
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ═══════════════════════════════════════════════════════════
# 第1部分：定义实际要执行的函数（"真实能力"）
# ═══════════════════════════════════════════════════════════

def get_weather(city: str) -> dict:
    """获取指定城市的天气信息

    当前是模拟数据。在实际项目中，你应该调用高德天气API、
    和风天气API或 OpenWeatherMap 等真实天气接口。
    """
    # 模拟天气数据库
    weather_db = {
        "北京": {"temperature": 25, "weather": "晴", "humidity": 45,
                 "wind": "北风 3级", "advice": "非常适合户外活动，注意防晒"},
        "上海": {"temperature": 32, "weather": "多云转雷阵雨", "humidity": 78,
                 "wind": "东南风 4级", "advice": "建议携带雨具，避免露天活动"},
        "广州": {"temperature": 35, "weather": "晴转多云", "humidity": 85,
                 "wind": "南风 2级", "advice": "天气炎热潮湿，注意防暑降温"},
        "深圳": {"temperature": 31, "weather": "阵雨", "humidity": 75,
                 "wind": "东风 3级", "advice": "间歇性降雨，出门带伞"},
        "成都": {"temperature": 22, "weather": "阴有小雨", "humidity": 80,
                 "wind": "无持续风向", "advice": "阴雨天适合吃火锅"},
        "杭州": {"temperature": 28, "weather": "晴", "humidity": 55,
                 "wind": "微风", "advice": "西湖边散步的好天气"},
    }

    # 如果城市不在数据库里，返回默认值
    return weather_db.get(
        city,
        {"temperature": 23, "weather": "未知（未收录城市）",
         "humidity": 60, "wind": "微风", "advice": "暂无该城市详细信息"}
    )


def calculate(expression: str) -> str:
    """安全地执行数学计算

    注意：实际生产环境中不要直接用 eval()，
    这里为了教学简洁使用了它。更好的做法是用
    Python 的 ast 模块安全解析，或者自己实现计算逻辑。
    """
    try:
        # 安全过滤：只允许数字、运算符、括号、空格、小数点
        allowed_chars = set("0123456789+-*/().%^ ")
        if not all(c in allowed_chars for c in expression):
            return f"错误：表达式中包含不允许的字符。只支持: 数字、+、-、*、/、(、)、.、%、^"

        # 禁止空表达式
        if not expression.strip():
            return "错误：表达式为空"

        # 替换 ^ 为 **（Python 的幂运算）
        expression = expression.replace("^", "**")

        result = eval(expression)
        return f"{expression.replace('**', '^')} = {result}"

    except ZeroDivisionError:
        return "错误：不能除以零！"
    except SyntaxError:
        return f"错误：表达式语法不正确: {expression}"
    except Exception as e:
        return f"计算错误: {str(e)}"


# ═══════════════════════════════════════════════════════════
# 第2部分：定义工具描述（告诉 LLM "你有什么工具"）
# ═══════════════════════════════════════════════════════════

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息，包括温度、天气状况、湿度、风向和出行建议",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'、'上海'、'广州'等"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算。支持加减乘除、括号、百分比、幂运算(用^表示)。例如: '(100+200)*3/5', '2^10', '15%*200'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式字符串，如'2+3*4'、'(100-20)/4'、'2^8'"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]

# ═══════════════════════════════════════════════════════════
# 第3部分：工具调度映射（函数名 → 实际函数）
# ═══════════════════════════════════════════════════════════

available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
}

# ═══════════════════════════════════════════════════════════
# 第4部分：Agent 核心循环
# ═══════════════════════════════════════════════════════════

def run_agent(user_input: str, verbose: bool = True) -> str:
    """Agent 核心循环——处理一次用户输入，可能包含多轮工具调用

    Args:
        user_input: 用户的原始输入
        verbose: 是否打印中间步骤（调试用）

    Returns:
        AI 的最终回答文本
    """

    # 初始化消息列表
    messages = [
        {
            "role": "system",
            "content": "你是一个有用的AI助手。你可以查询天气和执行数学计算。请根据用户的问题选择使用合适的工具。回答时请引用工具返回的实际数据，给出有帮助的建议。"
        },
        {"role": "user", "content": user_input}
    ]

    max_iterations = 5  # 安全阀——防止无限循环

    for iteration in range(max_iterations):
        if verbose:
            print(f"\n{'─'*40}")
            print(f"[第{iteration + 1}轮] 正在询问 LLM...")

        # Step A: 把当前消息发给 LLM（带工具描述）
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            temperature=0.1,  # 工具调用需要低温度（确定性高）
        )

        response_message = response.choices[0].message

        # Step B: 检查 LLM 是想直接回答，还是想调用工具
        if response_message.tool_calls is None:
            # 没有工具调用 → LLM 直接给了最终回答
            if verbose:
                print("[完成] LLM 给出了最终回答")
            return response_message.content

        # Step C: LLM 想调用工具！处理工具调用
        if verbose:
            print(f"[工具调用] LLM 想调用 {len(response_message.tool_calls)} 个工具")

        # 把 LLM 的回复（包含工具调用决定）加入消息历史
        messages.append(response_message)

        # Step D: 逐一执行工具调用
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"  → 调用: {function_name}")
                print(f"  → 参数: {json.dumps(function_args, ensure_ascii=False)}")

            # 执行实际的函数
            try:
                if function_name in available_functions:
                    function_result = available_functions[function_name](**function_args)
                else:
                    function_result = f"错误：未知工具 '{function_name}'"

                if verbose:
                    # 格式化结果以便阅读
                    if isinstance(function_result, dict):
                        result_str = json.dumps(function_result, ensure_ascii=False, indent=2)
                    else:
                        result_str = str(function_result)
                    print(f"  → 结果: {result_str}")

            except Exception as e:
                function_result = f"工具执行出错: {str(e)}"
                if verbose:
                    print(f"  → 错误: {function_result}")

            # Step E: 把工具执行结果加入消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(function_result, ensure_ascii=False)
                    if isinstance(function_result, dict)
                    else str(function_result)
            })

        # 循环回到 Step A —— LLM 会基于工具结果继续推理
        # 可能再次调用工具，或者给出最终回答

    # 如果超过最大迭代次数还没结束
    return "抱歉，处理过程超时。请尝试换个问法。"


# ═══════════════════════════════════════════════════════════
# 第5部分：测试
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("    🤖 Function Calling Agent 测试")
    print("    支持: 天气查询 | 数学计算")
    print("=" * 60)

    test_queries = [
        # 单工具调用
        "今天北京天气怎么样？适合出去玩吗？",

        # 另一个单工具调用
        "帮我算一下 (156 + 234) * 3 / 5 等于多少？",

        # 多工具调用（LLM需要判断先查哪个）
        "上海和广州今天哪个城市更热？温度差多少？",

        # 复合——同一句话中既需要查天气也需要计算
        "如果北京现在的温度是25度，上海的温度是多少？两个城市的平均温度是多少？",

        # 不需要工具——直接回答
        "请用中文解释一下什么是机器学习",
    ]

    for i, query in enumerate(test_queries):
        print(f"\n{'='*60}")
        print(f"  📝 测试 {i+1}／{len(test_queries)}")
        print(f"  用户: {query}")
        print(f"{'='*60}")

        answer = run_agent(query, verbose=True)

        print(f"\n  🤖 AI 最终回答:")
        print(f"  {'─'*56}")
        print(f"  {answer}")
        print(f"  {'─'*56}")

    print(f"\n{'='*60}")
    print("  全部测试完成！")
    print(f"{'='*60}")
```

#### 4.5.4 Function Calling 关键要点总结

| 概念 | 说明 | 代码体现 |
|------|------|---------|
| **工具定义 (tools)** | JSON Schema 格式描述每个工具的名称、用途、参数 | `tools = [{"type": "function", "function": {...}}]` |
| **工具映射 (available_functions)** | 把工具名称映射到实际的 Python 函数 | `{"get_weather": get_weather}` |
| **工具调用判断** | 检查 `response_message.tool_calls` 是否为 None | `if response_message.tool_calls:` |
| **参数解析** | 从 `tool_call.function.arguments` 获取 JSON 参数 | `json.loads(tool_call.function.arguments)` |
| **结果回传** | 用 `role: "tool"` 把结果加入 messages | `{"role": "tool", "tool_call_id": ..., "content": ...}` |
| **交互循环** | 可能多轮交互——LLM 可以多次调用工具 | `for iteration in range(max_iterations)` |
| **多工具并行** | LLM 可以同时调用多个函数（不相互依赖时） | `for tool_call in response_message.tool_calls:` |

> 📊 **企业视角：Function Calling = 让AI从"说话"变成"做事"**  
> 
> 这是企业AI应用的核心分水岭。理解两种AI的差异：
> 
> | 维度 | 只能聊天的AI | 有Function Calling的AI |
> |------|-------------|----------------------|
> | **能力范围** | 生成文字建议 | 自动发邮件/查数据库/更新CRM/创建工单/调用ERP |
> | **业务价值** | 辅助思考 | 替代重复性操作流程 |
> | **ROI体现** | 难以量化（"效率提升"） | 容易量化（"处理时间从X降到Y"） |
> | **集成深度** | 表层（复制粘贴） | 深层（系统自动调用） |
> | **典型场景** | 帮客服写回复模板 | 自动查订单→判断责任→发退款→更新工单状态 |
> 
> **企业案例 —— 某电商客服自动化**：  
> 用Function Calling将"用户投诉→查订单→判断责任→发退款"全流程自动化。之前：客服手动查后台（5分钟）→手动核对（3分钟）→手动提交退款（2分钟）→通知用户（2分钟）= **每单约4小时（含排队等待）**。部署Function Calling Agent后：用户发送投诉消息→AI自动调用订单查询API（2秒）→调用退款规则判断API（1秒）→调用退款执行API（3秒）→自动回复用户（1秒）= **全流程2分钟以内**。人力投入从8人客服团队减少到3人（负责审核复杂案例），年节省约￥35万人力成本。
> 
> **行动建议**：列出你企业中满足以下条件的流程——①输入输出都是数字/文字 ②规则明确可编码 ③人工处理耗时长 ④错误可事后纠正。这些是Function Calling的最佳切入点。

#### 4.5.5 Function Calling 进阶：并行调用与复杂场景

```python
# 场景：用户一句话需要同时查询多个城市的天气
# LLM 会同时发起多个并行的 get_weather 调用

query = "北京、上海、广州三个城市今天天气分别怎么样？哪个最适合旅游？"

# run_agent 会自动处理：
# 第1轮: LLM返回3个并行 tool_calls → [get_weather("北京"), get_weather("上海"), get_weather("广州")]
# 第2轮: 3个函数结果都返回后，LLM一次性比较并给出建议

answer = run_agent(query, verbose=True)
```

---

### 4.6 Structured Output —— 让模型输出结构化数据

#### 4.6.1 问题：为什么需要 Structured Output

```python
# ─── 传统方式的问题 ───
# 你让模型分析一段文本并输出JSON，但你永远不确定它返回的格式
# 可能输出: {"name": "...", "rating": 5}
# 也可能输出: 好的，分析结果如下：\n```json\n{"name": "...", "rating": 5}\n```
# 还可能: 缺少字段、多了字段、类型不对......

# 在生产环境中，这种不确定性是致命的——你的程序无法可靠解析
```

**Structured Output 的解决方案**：告诉模型"你只能按照这个 JSON Schema 输出，不能多一个字，不能少一个字"。

#### 4.6.2 方法一：用 JSON Mode + Prompt（兼容所有模型）

这是最通用的方法——任何支持 OpenAI 协议的模型都能用。

```python
"""
Structured Output 方法一：JSON Mode + Prompt 引导
适用：所有 OpenAI 兼容 API (DeepSeek、通义千问等)
"""
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ─── 定义输出格式 ───
# 用详细的 Prompt 说明输出 JSON 的格式
system_prompt = """
你是一个专业的电商评论分析助手。你需要分析用户对产品的评价，并输出以下格式的 JSON。

输出规则：
1. 只输出 JSON，不要加任何解释、前缀、后缀
2. 严格遵守下面的 JSON 结构
3. sentiment 只能是 "正面" 或 "负面" 或 "中性"
4. rating 必须是 1-5 的整数
5. advantages 和 disadvantages 各列出 2-3 条，每条不超过 15 个字
6. keywords 列出 3-5 个关键词

输出 JSON 结构:
{
    "product_name": "产品名称（从评论中提取）",
    "sentiment": "正面/负面/中性",
    "rating": 数字1-5,
    "advantages": ["优点1", "优点2", "优点3"],
    "disadvantages": ["缺点1", "缺点2"],
    "summary": "一句话总结（不超过50字）",
    "keywords": ["关键词1", "关键词2", "关键词3"]
}
"""

def analyze_review(review_text: str) -> dict:
    """分析一条产品评论，返回结构化 JSON"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析以下产品评论：\n\n{review_text}"}
        ],
        temperature=0.0,  # 最低温度——确保输出格式稳定
    )

    raw_output = response.choices[0].message.content

    # ─── 稳健的 JSON 解析 ───
    try:
        # 尝试1: 直接解析
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass

    try:
        # 尝试2: 清理可能的 markdown 代码块标记
        cleaned = raw_output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())
    except json.JSONDecodeError as e:
        # 尝试3: 都失败了，返回错误信息
        print(f"JSON 解析失败！原始输出:\n{raw_output}")
        return {"error": f"JSON解析失败: {str(e)}", "raw": raw_output}


# ─── 测试 ───
if __name__ == "__main__":
    reviews = [
        """
        入手 iPhone 16 Pro Max 一周了，总体感觉非常不错。屏幕是真的大，看视频很爽。
        拍照效果很惊艳，特别是夜景模式。不过续航没有想象中的好，重度使用还是要一天两充。
        价格确实贵了一些，256G版本花了10999。但是做工真的没得挑，很有质感。
        """,
        """
        买了某品牌的无线蓝牙耳机，到手价299。音质一般般，低音不够沉。
        连接倒是很稳定，没有出现过断连。但是戴久了耳朵会疼，耳塞材质不太舒服。
        续航还行，单次用四五个小时没问题。这个价位也就这样吧，不功不过。
        """,
    ]

    for i, review in enumerate(reviews):
        print(f"\n{'='*50}")
        print(f"  评论 {i+1} 分析")
        print(f"{'='*50}")
        print(f"原始评论: {review[:80]}...")

        result = analyze_review(review)

        print(f"\n产品名称: {result.get('product_name', '未知')}")
        print(f"情感倾向: {result.get('sentiment', '未知')}")
        print(f"评分: {result.get('rating', '?')}/5")
        print(f"优点: {result.get('advantages', [])}")
        print(f"缺点: {result.get('disadvantages', [])}")
        print(f"总结: {result.get('summary', '')}")
        print(f"关键词: {result.get('keywords', [])}")
```

#### 4.6.3 方法二：用 OpenAI 的 response_format + Pydantic（仅 OpenAI 和兼容平台）

```python
"""
Structured Output 方法二：Pydantic + response_format（严格模式）
适用平台：OpenAI GPT-4o 系列、部分兼容平台
DeepSeek 当前支持基础的 JSON mode，但 Pydantic 约束可能在部分模型上不完全生效
"""
from pydantic import BaseModel, Field
from typing import Literal
from openai import OpenAI

# ─── 用 Pydantic 定义数据模型（即"Schema"） ───

class ProductReview(BaseModel):
    """产品评价的数据结构"""
    product_name: str = Field(description="产品名称")
    sentiment: Literal["正面", "负面", "中性"] = Field(description="情感倾向")
    rating: int = Field(ge=1, le=5, description="评分 1-5")
    advantages: list[str] = Field(description="产品优点", min_length=1, max_length=5)
    disadvantages: list[str] = Field(description="产品缺点", min_length=1, max_length=5)
    summary: str = Field(description="一句话总结", max_length=100)
    keywords: list[str] = Field(description="关键词", min_length=2, max_length=8)

# 注意：以下代码在 DeepSeek 上使用 response_format 可能会有限制
# 如果你用 OpenAI GPT-4o，可以这样调用：
#
# response = client.beta.chat.completions.parse(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "你是电商评论分析助手"},
#         {"role": "user", "content": "请分析: " + review_text}
#     ],
#     response_format=ProductReview  # 直接传入 Pydantic 模型！
# )
# review = response.choices[0].message.parsed  # 自动解析为 ProductReview 对象

# 实际教学建议：使用方法一（JSON Mode + Prompt），它是所有平台通用的
```

> **实践建议**：对于 DeepSeek 用户，目前推荐方法一（JSON Mode + Prompt）。如果你的项目使用 OpenAI GPT-4o，可以用方法二获得更严格的格式保证。

#### 4.6.4 Structured Output 使用场景

| 场景 | 输入 | 输出 JSON | 后续处理 |
|------|------|-----------|---------|
| **评论分析** | 用户评论文字 | {sentiment, rating, keywords} | 存入数据库，统计报表 |
| **简历解析** | 简历 PDF 文本 | {name, skills[], education[], experience[]} | 自动录入 HR 系统 |
| **合同提取** | 合同全文 | {parties[], amount, dates[], clauses[]} | 自动归档、到期提醒 |
| **邮件分类** | 邮件正文 | {category, priority, needs_reply} | 自动路由、任务分配 |
| **表格填写** | 表单自由文本 | 结构化的字段映射 | 替代人工录入 |

---

### 4.7 流式输出（Streaming）—— 像打字机一样

#### 4.7.1 为什么要流式输出

- **用户体验**：没人想等 10 秒看一片空白，然后突然出现一大段文字
- **ChatGPT 的秘诀**：打字机效果让用户感觉"AI 在思考"，体验大幅提升
- **降低焦虑**：用户看到了进展，不会怀疑"是不是卡死了"

#### 4.7.2 完整代码

```python
"""
流式输出 (Streaming) 完整示例
实现 ChatGPT 那样的逐字打字效果
"""
from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def chat_stream(user_input: str, system_prompt: str = None) -> str:
    """流式聊天——逐字打印 AI 的回复

    与普通调用的关键区别：stream=True
    然后遍历响应的 chunks，逐个打印

    Returns:
        完整的回复文本（用于保存对话历史）
    """

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input})

    # ─── 关键：stream=True ───
    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7,
        stream=True,  # ← 开启流式！
    )

    # ─── 逐块接收并打印 ───
    full_response = ""
    print("AI: ", end="", flush=True)

    start_time = time.time()
    first_token_time = None

    for chunk in stream:
        # chunk 是模型生成的一小段文本
        # 每段可能包含几个 token（通常 1-5 个 token/块）

        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content

            # 记录首个 token 的时间（衡量"首字延迟"）
            if first_token_time is None:
                first_token_time = time.time()

            # 逐字打印（不换行）
            print(content, end="", flush=True)
            full_response += content

    # 统计
    total_time = time.time() - start_time
    first_token_latency = (first_token_time - start_time) if first_token_time else 0

    print(f"\n\n⏱ 首字延迟: {first_token_latency:.2f}s | 总耗时: {total_time:.2f}s")
    print(f"📝 回复长度: {len(full_response)} 字符")

    return full_response


def chat_stream_with_token_count(user_input: str) -> str:
    """带 Token 计数的流式输出"""
    messages = [{"role": "user", "content": user_input}]

    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.7,
        stream=True,
        stream_options={"include_usage": True}  # 要求最后返回 usage 信息
    )

    full_response = ""
    print("AI: ", end="", flush=True)

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            full_response += chunk.choices[0].delta.content

        # 最后一个 chunk 包含 usage 信息
        if hasattr(chunk, 'usage') and chunk.usage:
            usage = chunk.usage
            print(f"\n\n📊 Token: 输入{usage.prompt_tokens} + 输出{usage.completion_tokens} "
                  f"= 总计{usage.total_tokens}")

    return full_response


# ─── 测试 ───
if __name__ == "__main__":
    # 普通流式
    print("=== 流式输出演示 ===\n")
    chat_stream(
        "请用中文写一个关于AI和人类友谊的简短故事，大约200字",
        system_prompt="你是一个创意写作者，文笔温暖、有画面感"
    )

    # 带 Token 计数的流式
    print("\n\n=== 带 Token 计数的流式输出 ===\n")
    chat_stream_with_token_count("用Python写一个快速排序算法，加中文注释")
```

#### 4.7.3 流式输出在聊天应用中的应用

```python
# 伪代码：在 Streamlit / Gradio 等 Web 框架中集成流式输出
# def chat_interface():
#     user_input = st.chat_input("请输入...")
#     if user_input:
#         # 显示用户消息
#         st.chat_message("user").write(user_input)
#
#         # 流式显示 AI 回复
#         with st.chat_message("assistant"):
#             placeholder = st.empty()  # 占位符——会被不断更新
#             full_text = ""
#             for chunk in stream:
#                 full_text += chunk
#                 placeholder.markdown(full_text + "▌")  # 打字机效果
#             placeholder.markdown(full_text)  # 最终完整文本
```

---

## 五、实操环节（70分钟）

> **教师提示**：实操环节建议让学生先完整运行代码，再逐步理解和修改关键参数。不要让学生从头打字——把代码复制到 Jupyter Notebook 或 .py 文件中运行。

### 实操 1：多轮对话机器人（25分钟）

**目标**：构建一个完整的、有上下文记忆的聊天机器人，跟踪 Token 消耗。

```python
"""
实操1：多轮对话聊天机器人
包含功能: 系统提示词、对话历史管理、Token统计、错误处理、交互式循环
"""
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ─── 初始化 ───
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

class ChatBot:
    """带 Token 统计的多轮对话机器人"""

    def __init__(self, system_prompt: str = "你是一个有帮助的AI助手"):
        """
        Args:
            system_prompt: 系统提示词，定义 AI 的角色和行为
        """
        self.client = client
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
        self.total_tokens_used = 0
        self.total_cost_yuan = 0.0
        self.round_count = 0

    def chat(self, user_input: str) -> str:
        """处理一轮对话

        Args:
            user_input: 用户输入的内容

        Returns:
            AI 的回复文本
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})

        try:
            # 调用 API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                temperature=0.7,
                max_tokens=1000
            )
        except Exception as e:
            # 错误处理——不要让一次失败毁掉整个对话
            error_msg = f"API 调用失败: {str(e)}"
            # 把失败的用户消息从历史中移除（因为没有回复）
            self.messages.pop()
            return error_msg

        # 提取回复
        reply = response.choices[0].message.content

        # 保存 AI 回复到历史
        self.messages.append({"role": "assistant", "content": reply})

        # 统计 Token 和费用
        usage = response.usage
        self.total_tokens_used += usage.total_tokens
        self.round_count += 1

        # DeepSeek 价格换算 (元)
        input_cost = usage.prompt_tokens / 1_000_000 * 1.0   # 1元/百万输入tokens
        output_cost = usage.completion_tokens / 1_000_000 * 2.0  # 2元/百万输出tokens
        round_cost = input_cost + output_cost
        self.total_cost_yuan += round_cost

        # 打印本轮的 Token 和费用
        print(f"\n--- 第{self.round_count}轮 ---")
        print(f"Tokens: 输入{usage.prompt_tokens} | 输出{usage.completion_tokens} | "
              f"合计{usage.total_tokens}")
        print(f"本轮回合成本: ¥{round_cost:.6f} | 累计成本: ¥{self.total_cost_yuan:.6f}")

        # 检查历史长度——防止超出上下文窗口（约128K tokens）
        # 简单策略：超过40条消息就裁剪（保留 system + 最近30条）
        if len(self.messages) > 40:
            system_msg = self.messages[0]  # 保留 system prompt
            self.messages = [system_msg] + self.messages[-30:]
            print("⚠️ 对话历史过长，已自动裁剪（保留最近15轮）")

        return reply

    def get_stats(self) -> dict:
        """获取使用统计"""
        return {
            "对话轮数": self.round_count,
            "累计 Tokens": self.total_tokens_used,
            "累计费用(元)": round(self.total_cost_yuan, 6),
            "历史消息数": len(self.messages),
        }

    def clear_history(self):
        """重置对话（保留 system prompt）"""
        system_msg = self.messages[0]  # 保留第一条 (system)
        self.messages = [system_msg]
        print("对话已重置（System Prompt 保留）")


# ─── 主程序：交互式聊天循环 ───
if __name__ == "__main__":
    # 自定义你的 AI 角色
    bot = ChatBot(system_prompt="""你是一位AI学习导师，名字叫"小A"。你的职责是帮助零基础的大学生理解AI和编程。

你的风格：
- 用生动的生活比喻解释技术概念
- 回答简洁，每次聚焦一个知识点（不要贪多）
- 鼓励学生动手实践
- 如果学生遇到错误，引导他们自己找到问题，而不是直接给答案

用中文交流，语气亲切但不啰嗦。
""")

    print("=" * 60)
    print("   🤖 AI 学习助手 —— 小A")
    print("   随时可以聊天！")
    print("   输入 'stats' 查看统计")
    print("   输入 'clear' 重置对话")
    print("   输入 'quit' 退出")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("\n对话结束！以下是本次对话统计：")
            for k, v in bot.get_stats().items():
                print(f"  {k}: {v}")
            break

        if user_input.lower() == 'stats':
            print("\n--- 使用统计 ---")
            for k, v in bot.get_stats().items():
                print(f"  {k}: {v}")
            continue

        if user_input.lower() == 'clear':
            bot.clear_history()
            continue

        # 调用 AI
        reply = bot.chat(user_input)
        print(f"\n小A: {reply}")
```

**运行后让学生做以下实验**：

1. 修改 `system_prompt`，让 AI 扮演不同的角色（诗人、代码审查员、健身教练等）
2. 进行 5 轮以上的对话，观察 messages 列表的增长和 Token 累计
3. 故意输入一些越界的问题，观察 AI 的反应
4. 在代码中打印出 `self.messages` 看一看，理解多轮对话的数据结构

---

### 实操 2：Function Calling Agent（30分钟）

**目标**：完成一个完整的、带多种工具的 Agent 循环。

```python
"""
实操2：Function Calling Agent 完整实战
工具: 天气查询、数学计算、时间查询、随机数生成
"""
import json
from datetime import datetime
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ═══════════════════════════════════════════════
# 定义工具函数
# ═══════════════════════════════════════════════

def get_weather(city: str) -> dict:
    """模拟天气查询"""
    weather_db = {
        "北京": {"temp": 25, "weather": "晴", "humidity": 40},
        "上海": {"temp": 32, "weather": "多云", "humidity": 70},
        "广州": {"temp": 35, "weather": "雷阵雨", "humidity": 85},
        "深圳": {"temp": 30, "weather": "晴", "humidity": 60},
        "成都": {"temp": 22, "weather": "阴", "humidity": 80},
        "杭州": {"temp": 28, "weather": "晴", "humidity": 55},
        "武汉": {"temp": 33, "weather": "晴", "humidity": 50},
        "西安": {"temp": 27, "weather": "多云", "humidity": 45},
    }
    return weather_db.get(
        city,
        {"temp": 24, "weather": "未知", "humidity": 60}
    )

def calculate(expression: str) -> str:
    """安全的数学计算"""
    allowed = set("0123456789+-*/().%^ ")
    if not all(c in allowed for c in expression):
        return f"错误：包含不允许的字符"
    try:
        result = eval(expression.replace("^", "**"))
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "错误：不能除以零"
    except Exception as e:
        return f"计算错误: {e}"

def get_current_time() -> str:
    """获取当前日期和时间"""
    now = datetime.now()
    return {
        "date": now.strftime("%Y年%m月%d日"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()],
        "timestamp": now.isoformat()
    }

def roll_dice(sides: int = 6, count: int = 1) -> dict:
    """掷骰子"""
    results = [random.randint(1, sides) for _ in range(count)]
    return {
        "骰子面数": sides,
        "投掷次数": count,
        "结果": results,
        "总和": sum(results),
        "平均值": round(sum(results)/count, 1)
    }

# ═══════════════════════════════════════════════
# 工具定义（告诉LLM有什么工具）
# ═══════════════════════════════════════════════

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算。支持加减乘除、括号、百分比、幂运算(用^表示)",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "roll_dice",
            "description": "掷骰子。可以指定骰子面数和投掷次数",
            "parameters": {
                "type": "object",
                "properties": {
                    "sides": {"type": "integer", "description": "骰子面数，默认6"},
                    "count": {"type": "integer", "description": "投掷次数，默认1"}
                },
                "required": []
            }
        }
    }
]

available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
    "roll_dice": roll_dice,
}

# ═══════════════════════════════════════════════
# Agent 核心循环
# ═══════════════════════════════════════════════

def run_agent(user_input: str, verbose: bool = True) -> str:
    """Agent核心循环"""

    messages = [
        {
            "role": "system",
            "content": "你是一个全能的AI助手。你可以查询天气、数学计算、查看当前时间、掷骰子。请根据用户需求，自主选择合适的工具。回答时引用工具返回的真实数据，语气友好自然。"
        },
        {"role": "user", "content": user_input}
    ]

    for iteration in range(5):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            temperature=0.0
        )

        response_message = response.choices[0].message

        # 没有工具调用 → 最终回答
        if not response_message.tool_calls:
            return response_message.content

        # 有工具调用 → 执行
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"  🔧 [{func_name}] 参数: {json.dumps(func_args, ensure_ascii=False)}")

            func_result = available_functions[func_name](**func_args)

            if verbose:
                print(f"  📊 [{func_name}] 结果: {json.dumps(func_result, ensure_ascii=False) if isinstance(func_result, dict) else func_result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(func_result, ensure_ascii=False) if isinstance(func_result, dict) else str(func_result)
            })

    return "抱歉，处理超时，请换一种问法。"


# ═══════════════════════════════════════════════
# 交互式测试
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   🤖 Function Calling Agent")
    print("   可用工具: 天气 | 计算 | 时间 | 掷骰子")
    print("   输入 'quit' 退出")
    print("=" * 60)

    test_queries = [
        "现在几点了？今天星期几？",
        "北京和武汉今天哪个热？温度差多少？",
        "帮我掷三个6面骰子，看看结果和总和",
        "(156+234)*3/5等于多少？",
        "如果我有3个骰子，每个骰子掷3次，总共多少种组合？用计算器验证",
    ]

    for query in test_queries:
        print(f"\n{'─'*60}")
        print(f"👤 用户: {query}")
        answer = run_agent(query, verbose=True)
        print(f"🤖 AI: {answer}")

    # 自由提问环节
    print(f"\n{'─'*60}")
    print("现在你可以自由提问！")

    while True:
        try:
            user_input = input("\n👤 你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if user_input.lower() == 'quit':
            print("再见！")
            break
        if not user_input:
            continue

        answer = run_agent(user_input, verbose=True)
        print(f"🤖 AI: {answer}")
```

**运行后让学生做的实验**：

1. 添加一个新工具（比如"翻译"或"生成随机密码"），需要修改哪几个地方？
2. 问一个需要多个工具协作的问题，观察 Agent 的多轮循环
3. 把 temperature 从 0.0 改成 1.0，观察工具调用的准确性变化
4. 故意给 get_weather 传一个不存在的城市名，看 LLM 如何处理

---

### 实操 3：Structured Output 实战（15分钟）

**目标**：编写代码让模型输出可被程序可靠解析的 JSON。

```python
"""
实操3：Structured Output 实战——产品评论结构化分析
"""
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ─── 定义输出格式的 System Prompt ───
EXTRACT_PROMPT = """你是一个专业的数据提取助手。你需要从用户提供的产品评论中提取结构化信息。

严格按以下 JSON 格式输出（只输出 JSON，不要加任何其他文字）：

{
  "product_name": "产品名称",
  "category": "产品类别（手机/电脑/食品/服装/家电/其他）",
  "sentiment": "正面/负面/中性",
  "rating": 数字1-5,
  "key_points": {
    "pros": ["优点1", "优点2"],
    "cons": ["缺点1", "缺点2"]
  },
  "price_perception": "贵/适中/便宜",
  "would_recommend": true/false,
  "summary_zh": "用中文一句话总结（20字以内）"
}

规则：
1. 如果评论中没有提到某项信息，用 null 代替
2. rating 必须是整数 1-5
3. pros 和 cons 从评论中直接提炼，不要编造
4. would_recommend 根据评论的整体倾向判断
"""

def extract_review_info(review_text: str) -> dict:
    """从评论文本中提取结构化信息"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": EXTRACT_PROMPT},
            {"role": "user", "content": review_text}
        ],
        temperature=0.0,  # 极低温度确保输出稳定
    )

    raw = response.choices[0].message.content

    # 健壮的JSON解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # 清理可能的 markdown 代码块
        cleaned = raw.strip()
        for prefix in ["```json", "```"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
        for suffix in ["```"]:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
        return json.loads(cleaned.strip())


# ─── 批量分析 ───
if __name__ == "__main__":
    reviews = [
        # 好评
        "刚入手了华硕天选5 Pro游戏本，用了两周感觉非常值！i9处理器加RTX4060显卡，跑3A大作毫无压力。"
        "散热做得不错，长时间玩游戏键盘区域也只是温热。唯一的小遗憾是重量偏重，2.5kg背出去有点累。"
        "花了8999买的，性价比很高，推荐给预算有限又想玩大作的朋友！",

        # 中评
        "在拼多多上买了一箱赣南脐橙，39.9元10斤。个头还行，大概有一半的橙子比较甜，剩下的有点酸。"
        "快递倒是很快，三天就到了。但包装不太行，拿出来有3个已经碰伤了。"
        "这个价格就这样吧，不功不过，不会回购。",

        # 差评
        "淘宝买了一件羽绒服，299元。图片看着很厚实，到手发现填充物很少，摸起来很薄，南方可能勉强够用，"
        "北方根本扛不住零下。而且颜色跟图片差太多，图片是亮红色，实际是暗酒红。退货还要自己付运费，很坑。"
        "完全不推荐，准备退货了。",
    ]

    all_results = []
    for i, review in enumerate(reviews):
        print(f"\n{'='*50}")
        print(f"评论 {i+1}: {review[:50]}...")
        result = extract_review_info(review)
        all_results.append(result)

        print(f"  产品: {result.get('product_name', '未知')}")
        print(f"  情感: {result.get('sentiment', '未知')} | 评分: {result.get('rating', '?')}/5")
        print(f"  优点: {result.get('key_points', {}).get('pros', [])}")
        print(f"  缺点: {result.get('key_points', {}).get('cons', [])}")
        print(f"  价格感知: {result.get('price_perception', '?')}")
        print(f"  推荐: {'是' if result.get('would_recommend') else '否'}")

    # ─── 额外：将结果保存为CSV ───
    import csv

    csv_path = "review_analysis.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["产品名称", "类别", "情感", "评分", "优点", "缺点", "价格感知", "推荐", "总结"])
        for r in all_results:
            writer.writerow([
                r.get("product_name"),
                r.get("category"),
                r.get("sentiment"),
                r.get("rating"),
                "；".join(r.get("key_points", {}).get("pros", [])),
                "；".join(r.get("key_points", {}).get("cons", [])),
                r.get("price_perception"),
                "是" if r.get("would_recommend") else "否",
                r.get("summary_zh")
            ])

    print(f"\n✅ 分析结果已保存到 {csv_path}")
    print(f"   共分析 {len(all_results)} 条评论")
```

**运行后让学生做的实验**：

1. 自己写一段产品评论（真实的网上购物体验），看看 AI 能否正确提取信息
2. 修改 JSON 输出格式，增加一个 "purchase_intent" 字段（购买意愿：高/中/低）
3. 尝试把 temperature 调到 0.7，看看 JSON 输出是否还稳定
4. 思考：如果用传统的正则表达式来提取这些信息，需要写多少代码？

---

## 六、课后作业

### 作业 1：AI 翻译助手（基础）

**要求**：用 API 实现一个完整的 AI 翻译助手。

```python
# 基础要求：
# 1. 支持中→英、英→中、中→日、日→中翻译
# 2. 记录每次调用消耗的 Token
# 3. 有一个交互式的命令行界面
# 4. 翻译质量要好——需要用心设计 system prompt

# 进阶要求：
# 1. 加入翻译历史记录功能（可以回看之前的翻译）
# 2. 支持"翻译+优化"模式（翻译后自动润色）
# 3. 统计总共花费了多少钱
```

### 作业 2：带 Function Calling 的智能翻译助手（进阶）

给翻译助手增加 Function Calling 能力：

```python
# 需要的工具函数：
# 1. detect_language(text) —— 自动检测输入文本的语言
# 2. get_word_definition(word) —— 查询单词的详细释义（模拟词典）
# 3. suggest_synonyms(word) —— 给出同义词/近义词建议

# 效果演示：
# 用户输入: "Bonjour, comment allez-vous?"
# AI调用: detect_language("Bonjour, comment allez-vous?")
# 返回: {"language": "法语", "confidence": 0.98}
# AI回复: "检测到这是法语，意思是：你好，你最近怎么样？"
```

### 作业 3：多平台对比实验（分析）

完成以下对比表格：

| 对比维度 | DeepSeek | GPT-4o-mini | 通义千问 |
|---------|----------|-------------|---------|
| 相同问题的回答质量 | ?/10 | ?/10 | ?/10 |
| 中文流畅度 | ?/10 | ?/10 | ?/10 |
| 单次问答平均成本 | ¥___ | $___ (≈¥___) | ¥___ |
| 首字延迟（streaming） | ___秒 | ___秒 | ___秒 |
| Function Calling 准确度 | ?/10 | ?/10 | ?/10 |
| Structured Output 可靠性 | ?/10 | ?/10 | ?/10 |
| 需要 VPN？ | 否/是 | 否/是 | 否/是 |

测试问题：
1. "解释一下什么是递归"（测试解释能力）
2. "用 Python 写一个冒泡排序"（测试代码能力）
3. "北京今天天气怎么样？"（测试 Function Calling）
4. 一段 500 字的产品评论（测试 Structured Output）

> **提交要求**：对比表格 + 每个平台的代表性回答截图 + 300 字的使用感受总结。

---

### 💼 企业作业

**作业1：API成本与ROI分析（必做）**

选择一个你企业中的潜在AI应用场景（如客服、文档处理、数据分析），完成以下分析：
1. 估算该场景的日均API调用量和Token消耗
2. 分别用DeepSeek、GPT-4o-mini、通义千问qwen-plus测算月度成本
3. 对比当前人工处理成本，计算AI替代的月度ROI（节省金额/API成本）
4. 输出一份一页纸的"API成本-收益分析"，包含盈亏平衡点（多久回本）

**作业2：Function Calling业务流程识别（选做）**

审计你企业的一个核心业务流程（如订单处理、客户投诉、报销审批），完成：
1. 画出该流程的每一步，标注每个步骤的"输入/输出"类型
2. 识别哪些步骤可以通过Function Calling自动化（输入输出都是数字/文字+规则明确的步骤）
3. 估算自动化后的时间节省和错误率改善
4. 撰写一份200字的"流程自动化可行性评估"

---

## 七、拓展阅读

| 资源 | 链接 | 说明 |
|------|------|------|
| **OpenAI API 官方文档** | https://platform.openai.com/docs | API 标准制定者，最详细的文档 |
| **DeepSeek API 文档** | https://platform.deepseek.com/api-docs | 中文友好，有完整的中文示例 |
| **通义千问 API 文档** | https://help.aliyun.com/zh/dashscope | 阿里云出品，企业级文档 |
| **OpenAI Function Calling 指南** | https://platform.openai.com/docs/guides/function-calling | 深入理解 Function Calling |
| **OpenAI Structured Outputs** | https://platform.openai.com/docs/guides/structured-outputs | 结构化输出的官方指南 |
| **Anthropic: Building Effective Agents** | https://www.anthropic.com/engineering/building-effective-agents | Agent 开发的顶级思想文章 |
| **OpenAI Tokenizer** | https://platform.openai.com/tokenizer | 在线查看文本的 Token 数 |

---

## 八、常见问题

### Q1: API 调用会不会花很多钱？

**A**: 对于个人学习和开发，成本极低。以 DeepSeek 为例：
- 1 万次简单问答（每轮约 500 tokens）：约 1.5 元人民币
- 新用户赠送 500 万 tokens，够整个课程使用了
- 开发一个小项目整个月也不会超过 10 元

如果担心花超，可以在平台后台设置**每日消费限额**。

### Q2: 为什么我的 API Key 报错 "401 Unauthorized"？

**A**: 检查以下几点：
1. Key 是否复制完整（可能漏了开头或结尾的字符）
2. Key 是否在平台后台被删除了（重新生成一个）
3. 是否设置了正确的 `base_url`（DeepSeek 不是 OpenAI 的默认地址）
4. 账户余额是否用完了（登录平台查看）

### Q3: Function Calling 调用一直失败怎么办？

**A**: 排查步骤：
1. 检查 `tools` 定义的 JSON Schema 格式是否正确（特别是 `required` 字段）
2. 检查 `tool_call.function.arguments` 是否正确解析（用 `json.loads`）
3. 检查函数执行结果是否正确加入了 messages（`role: "tool"`）
4. 打印中间变量——看看每一步的数据是什么
5. 把 `temperature` 降到 0.0——工具调用的参数生成需要确定性

### Q4: API 调用很慢怎么办？

**A**：
- 使用流式输出——用户感觉"快了很多"，虽然总时间一样
- 用更小更快的模型（DeepSeek-chat、GPT-4o-mini 都比 GPT-4o 快得多）
- 减少 system prompt 的长度
- 减少历史对话消息的数量

### Q5: API Key 不小心提交到 GitHub 了怎么办？

**A**: 紧急处理（分秒必争）：
1. **立刻**登录平台后台，删除当前 Key，重新生成新 Key
2. 用 `git filter-branch` 或 `BFG Repo-Cleaner` 清除 Git 历史
3. 如果是公开仓库，联系 GitHub Support 清除缓存

> **防范措施**：
> - 使用 `.env` + `.gitignore` 管理 Key（本次课程已教）
> - 在 GitHub 仓库设置中开启 Secret Scanning
> - 使用 `git-secrets` 等工具在提交前扫描敏感信息

### Q6: Structured Output 输出 JSON 格式总是有问题怎么办？

**A**：
1. **降 temperature**：0.0 是最安全的选择
2. **加强 system prompt**：明确说"只输出 JSON，不要任何解释"
3. **在 user message 末尾加一句**："请直接输出 JSON，不要包含 markdown 代码块标记"
4. **代码层面容错**：先用 `json.loads` 尝试直接解析，失败则去掉 ```json 标记再试
5. **降低复杂度**：JSON 嵌套层级不要超过 3 层，数组元素不要超过 10 个

---

> **本课小结**：你今天学会了用代码驱动 LLM、让模型调用工具（Function Calling）、控制模型输出格式（Structured Output）、实现流式打字机效果。这些能力组合在一起，就是你接下来开发 AI 应用的"基本功"。下一课我们将学习 RAG（检索增强生成），教 AI 读懂你自己的文档和数据。

---

### 💼 企业常见问题

**Q7: 企业应该自己开发API调用层还是用现成的SaaS产品？**

A: 取决于两个因素——定制化需求和数据敏感度：
- **数据不敏感+需求标准化**（如通用客服）→直接用SaaS产品（如ChatGPT Team、钉钉AI助手），零开发成本，按用户付费
- **数据敏感+需求定制化**（如内部知识库问答、业务流程自动化）→基于API自行开发，用本课教的MultiLLM模式封装
- **折中方案**：API调用层自己开发（数据控制权在自己手里），但用LangChain/LlamaIndex等框架加速开发（不用从零写所有逻辑）

**Q8: Function Calling开发的成本高吗？需要什么技术团队？**

A: 成本分三块：
1. **API调用成本**：如前述表格，日处理1万次调用的系统月费约￥200-1,000（用国产模型）
2. **开发成本**：一个基础的Function Calling Agent（如自动客服机器人），有经验的Python开发者约2-4周可完成MVP。外包开发约￥3-8万
3. **维护成本**：日常监控、Prompt优化、新增工具函数，约占用一个开发者的20%时间

技术团队要求：至少1名熟悉Python的后端开发者 + 1名理解业务流程的产品经理。不需要AI/ML专家。

**Q9: 我们公司的业务系统（CRM/ERP）不支持API，还能用Function Calling吗？**

A: 可以，但有替代方案：
1. **优先方案**：推动CRM/ERP厂商开放API（2026年大部分主流系统都已支持）
2. **RPA替代**：如果系统真的没有API，用RPA工具（如影刀、UiPath）模拟人工操作，Function Calling调用RPA执行操作
3. **数据库直连**：如果只需要查询数据（不需要写入），可以直接连接数据库只读副本
4. **导出+处理**：定期从系统导出数据（Excel/CSV），Function Calling基于导出数据做分析和处理

核心原则：Function Calling不是魔法，它只是帮你"自动调用已有的工具"。如果工具本身不存在，需要先建设工具层。

---
