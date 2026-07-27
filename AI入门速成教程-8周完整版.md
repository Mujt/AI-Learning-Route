# AI 时代能力培养教程（8周速成版）

> **课程定位**：面向零基础、非计算机专业学生（工程设计、机械、土木、艺术等），帮助学生掌握 AI 工具应用、理解 AI 核心原理，并能够独立开发简单 AI Agent 应用。
>
> **教学理念**：会用 AI → 懂 AI → 会开发 AI 应用 → 了解 AI 前沿（Agent）
>
> **理论实践比**：30% 理论 + 70% 实践
>
> **版本**：V1.0 | **日期**：2026-07-26

---

# 第一部分：课程大纲与教学计划

## 一、课程概览

| 项目 | 说明 |
|------|------|
| **课程名称** | AI 时代能力培养 |
| **课程时长** | 8 周（2 个月），每周 3 节课，共 24 节课 |
| **每节课时** | 2 小时（1 小时讲解 + 1 小时实操） |
| **适合人群** | 零基础大学生、非计算机专业学生、职场转行人员 |
| **前置要求** | 会使用电脑、会浏览器上网即可 |
| **最终产出** | 一个可展示的 AI Agent 项目 |

## 二、每周课程安排

| 周次 | 主题 | 课时 | 核心内容 | 作业 |
|------|------|------|----------|------|
| 第1周 | AI 工具与 Prompt | 3 节 | AI 发展史、Prompt Engineering、AI 办公自动化 | 用 AI 完成一份设计方案 |
| 第2周 | Python 基础 | 3 节 | Python 语法、函数、数据分析 | 编写数据处理程序 |
| 第3周 | 机器学习入门 | 3 节 | ML 概念、常见算法、Scikit-learn 实战 | 完成分类模型训练 |
| 第4周 | 深度学习基础 | 3 节 | 神经网络、CNN、Transformer | 图像分类实践 |
| 第5周 | 大模型与 RAG | 3 节 | GPT 原理、API 调用、RAG 知识库 | 搭建知识库问答系统 |
| 第6周 | AI 应用开发 | 3 节 | API 调用实战、Web 界面开发、项目实战 | 制作聊天机器人 |
| 第7周 | Agent 与 MCP | 3 节 | Agent 原理、LangChain/LangGraph、MCP | 开发 AI 秘书 |
| 第8周 | 综合项目 | 3 节 | AI 设计助手、多 Agent 协作、项目答辩 | 完成 Agent 项目展示 |

---

## 三、每周教学大纲与教学建议

### 第1周：AI 工具与 Prompt Engineering

**教学目标**：
- 了解 AI 的发展历程和大模型的核心能力
- 熟练掌握 ChatGPT、Claude、Gemini 等主流 AI 工具
- 掌握 Prompt Engineering 的核心方法
- 能够用 AI 辅助完成文档、PPT、方案等日常任务

**教学建议**：
- 第一节课以演示为主，让学生现场注册并体验各 AI 工具
- 第二节课是核心，务必让学生掌握 RCTE（Role-Context-Task-Example）框架
- 第三节课结合实际场景，比如让学生用 AI 写一份课程项目方案
- **注意**：本周不需要写代码，重点是建立 AI 思维和使用习惯

### 第2周：Python 基础

**教学目标**：
- 掌握 Python 基础语法（变量、条件、循环、列表、字典）
- 理解函数、模块、类的概念并能使用
- 学会用 NumPy、Pandas、Matplotlib 进行基本数据分析

**教学建议**：
- 安装环境统一使用 Anaconda + Jupyter Notebook，降低配置门槛
- 鼓励学生用 AI 工具（ChatGPT/Claude）辅助写代码和 Debug
- 每节课留 15 分钟让学生互相分享今天用 AI 解决了什么问题
- **重要**：不要纠结语法的细枝末节，能跑通、能看懂即可

### 第3周：机器学习入门

**教学目标**：
- 理解机器学习的基本概念（数据、标签、特征、模型）
- 了解常见 ML 算法的分类和适用场景
- 能够用 Scikit-learn 完成一个分类任务

**教学建议**：
- 用垃圾邮件识别作为贯穿案例，直观易懂
- **不推导数学公式**，重点建立"数据→特征→模型→预测"的直觉
- 鸢尾花分类实验让学生亲手跑，获得成就感
- 强调"什么时候用什么算法"比"算法怎么推导"更重要

### 第4周：深度学习基础

**教学目标**：
- 理解神经元、激活函数、损失函数等基本概念
- 理解 CNN 为什么适合图像处理
- 理解 Transformer 和 Attention 的核心思想（不讲公式）

**教学建议**：
- 用生活类比解释技术概念（神经元≈大脑细胞，卷积≈特征扫描仪）
- CNN 猫狗分类用现成代码，重点让学生理解输入输出和训练过程
- Transformer 部分**只讲思想不讲公式**，用动画/图解辅助
- 告诉学生："不理解数学很正常，先建立概念框架"

### 第5周：大模型与 RAG

**教学目标**：
- 理解 Token、Embedding、Transformer、Decoder 的概念
- 理解 ChatGPT 为什么能够对话
- 掌握 API 调用（Function Calling、Structured Output）
- 理解 RAG 原理并能搭建简单知识库

**教学建议**：
- 这周是承上启下的关键周，要把前面学的串联起来
- 用"为什么 ChatGPT 不知道你公司的数据"引出 RAG 需求
- API 调用部分提前帮学生申请好 API Key（或提供测试 Key）
- RAG 实操用最简单的代码实现，降低挫败感

### 第6周：AI 应用开发

**教学目标**：
- 熟练用 Python 调用 OpenAI/通义千问/DeepSeek 等 API
- 掌握 Streamlit 或 Gradio 快速搭建 Web 界面
- 能够独立完成一个 AI 聊天机器人项目

**教学建议**：
- 这周以动手为主，讲解时间控制在 30 分钟内
- 提供完整的示例代码，让学生先跑通再修改
- 鼓励学生基于自己的专业场景做个性化改造
- Streamlit 比 Gradio 更推荐（更灵活、社区更大）

### 第7周：Agent 与 MCP（核心周）

**教学目标**：
- 理解 Agent 的核心理念：感知 → 推理 → 规划 → 执行
- 理解 Agent 与聊天机器人的本质区别
- 掌握 LangChain/LangGraph 的基本用法（工具调用、记忆）
- 理解 MCP（Model Context Protocol）的概念和应用

**教学建议**：
- 这是整个课程最重要的一周，务必确保学生理解 Agent 的"自主性"
- 用"AI 秘书"作为贯穿项目，包含：查天气、设提醒、查文件等功能
- MCP 部分讲概念为主，实操用现成的 MCP Server 演示
- 推荐参考 [hello-agents](https://github.com/datawhalechina/hello-agents) 教程

### 第8周：综合项目与答辩

**教学目标**：
- 综合运用所学知识完成一个完整的 AI Agent 项目
- 理解多 Agent 协作的基本模式
- 具备项目展示和技术表达能力

**教学建议**：
- 第一节课给出项目选题方向，帮助学生确定项目范围
- 第二节课介绍多 Agent 协作模式，但不强制要求实现
- 第三节课的项目答辩每人 5-8 分钟，重点是"解决了什么问题"
- 评分标准：项目完成度 40% + 技术运用 30% + 创新性 20% + 展示表达 10%

---

## 四、学习成果评估标准

课程结束后，学生应能够：

| 能力维度 | 具体要求 | 评估方式 |
|----------|----------|----------|
| **AI 应用能力** | 熟练使用 ChatGPT、Claude、Gemini 等工具解决学习和设计问题 | 课堂实操检查 |
| **Prompt Engineering** | 能设计高质量提示词，掌握 RCTE 框架 | 作业评估 |
| **AI 基础认知** | 理解 ML、DL、Transformer 的核心思想，知道 LLM 工作原理 | 随堂测验 |
| **Python 编程** | 掌握 Python 基础，能调用大模型 API | 代码作业 |
| **AI 应用开发** | 能使用 Streamlit/Gradio 开发简单 AI 应用 | 项目检查 |
| **Agent 开发** | 理解 RAG、Tool Calling、MCP、Agent，能构建简单智能 Agent | 最终项目 |
| **综合项目** | 独立完成与专业相关的 AI 项目，形成可展示作品集 | 项目答辩 |

---

# 第二部分：详细学习讲义

---

# 第1周：AI 工具与 Prompt Engineering

---

## 第1课：AI 的发展与未来

### 一、学习目标

- 了解 AI 从诞生到 ChatGPT 的发展历程
- 理解大模型能够做什么、不能做什么
- 建立"AI 是工具，人是主导"的正确认知
- 能够注册并使用至少 3 个主流 AI 工具

### 二、核心知识点

#### 2.1 AI 发展简史

```
1950s  图灵测试 — AI 概念的诞生
1956   达特茅斯会议 — "人工智能"正式命名
1997   深蓝击败国际象棋冠军
2012   AlexNet 赢得 ImageNet — 深度学习崛起
2016   AlphaGo 击败李世石
2017   Transformer 论文发表 — "Attention Is All You Need"
2022   ChatGPT 发布 — 2 个月破亿用户
2023   GPT-4、Claude、Gemini 相继发布
2024   多模态大模型、Agent、MCP 快速发展
2025   Claude Code、Codex 等 AI 编程工具成熟
2026   AI Agent 进入工程化落地阶段
```

#### 2.2 ChatGPT 为什么会火？

1. **能力泛化**：一个模型能做翻译、写作、编程、分析等多种任务
2. **交互自然**：用日常语言对话，无需学习特殊指令
3. **门槛极低**：打开网页就能用，不需要安装配置
4. **效果惊艳**：在很多任务上达到甚至超过人类水平
5. **时机成熟**：云计算、大数据、GPU 算力为大规模部署提供了基础

#### 2.3 大模型能够做什么？

| 能力 | 说明 | 示例 |
|------|------|------|
| **文本生成** | 写文章、方案、报告、邮件 | "帮我写一份咖啡馆设计方案" |
| **代码编写** | 写代码、Debug、代码审查 | "用 Python 写一个数据分析脚本" |
| **翻译** | 多语言互译 | "把这段中文翻译成英文" |
| **总结摘要** | 长文提炼要点 | "帮我总结这篇论文的核心观点" |
| **问答** | 回答知识性问题 | "解释什么是机器学习" |
| **创意生成** | 头脑风暴、创意点子 | "给我 10 个 App 创业点子" |
| **数据分析** | 处理表格、生成图表 | "分析这份销售数据" |
| **图像理解** | 识别图片内容（多模态模型） | "描述这张图片里有什么" |

#### 2.4 AI 会不会取代人？

**核心观点**：
- AI 取代的是**具体任务**，不是**完整职业**
- **会用 AI 的人**会取代**不会用 AI 的人**
- AI 是"自行车"，不是"自动驾驶汽车"——它放大你的能力，但方向由你掌控
- 关键是建立 **AI 协作思维**：知道什么任务交给 AI，什么任务自己把控

### 三、实操环节（60分钟）

#### 实操 3.1：注册并体验 ChatGPT

1. 打开浏览器，访问 [https://chatgpt.com](https://chatgpt.com)
2. 点击注册，使用邮箱或 Google 账号登录
3. 免费版使用 GPT-4o mini 模型，付费版（$20/月）使用 GPT-5 等更强模型
4. 在对话框中输入：`你好，请用三句话介绍你自己`
5. 观察 ChatGPT 的回答

> **注意**：部分地区可能需要科学上网。如无法访问 ChatGPT，可以使用国内替代方案：
> - 通义千问：[https://tongyi.aliyun.com](https://tongyi.aliyun.com)
> - DeepSeek：[https://chat.deepseek.com](https://chat.deepseek.com)
> - Kimi：[https://kimi.moonshot.cn](https://kimi.moonshot.cn)
> - 豆包：[https://www.doubao.com](https://www.doubao.com)

#### 实操 3.2：体验 Claude

1. 访问 [https://claude.ai](https://claude.ai)
2. 注册 Anthropic 账号
3. 尝试让 Claude 写一段代码：`用 Python 写一个计算斐波那契数列的函数`
4. 对比 Claude 和 ChatGPT 的回答风格和内容差异

#### 实操 3.3：体验 Gemini

1. 访问 [https://gemini.google.com](https://gemini.google.com)
2. 使用 Google 账号登录
3. 尝试上传一张图片，让 Gemini 描述图片内容
4. 体验 Gemini 的多模态能力

#### 实操 3.4：体验 Perplexity（AI 搜索引擎）

1. 访问 [https://www.perplexity.ai](https://www.perplexity.ai)
2. 搜索：`2026年AI领域最重要的技术趋势有哪些`
3. 观察 Perplexity 如何给出带引用来源的回答
4. 对比传统搜索引擎（Google/百度）和 AI 搜索引擎的差异

### 四、课后作业

1. 在至少 3 个 AI 工具中分别问同一个问题，对比回答质量，写一篇 300 字的对比笔记
2. 选一个你专业相关的问题（如设计一个建筑方案、分析一个机械结构），分别用传统搜索和 AI 工具解决，对比效率
3. 思考：你未来从事的工作中，哪些环节可以用 AI 提效？列出至少 5 个场景

### 五、拓展阅读

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- 吴恩达《AI For Everyone》课程（Coursera 免费课程）

---

## 第2课：Prompt Engineering（提示词工程）

### 一、学习目标

- 掌握 Prompt Engineering 的核心框架
- 能够写出高质量的结构化提示词
- 能够用 AI 完成论文写作、代码编写、方案设计、PPT 大纲、图片生成等任务

### 二、核心知识点

#### 2.1 什么是 Prompt Engineering？

**Prompt（提示词）** 是你与 AI 对话时输入的指令。**Prompt Engineering（提示词工程）** 是设计有效指令的方法论。

> 💡 **一句话理解**：好的 Prompt 像一个精准的任务说明书，差的 Prompt 像一个模糊的口头交代。

#### 2.2 RCTE 框架

这是最核心、最实用的 Prompt 框架，所有复杂提示词都可以基于此构建：

```
┌─────────────────────────────────────────┐
│  R — Role       你希望 AI 扮演什么角色   │
│  C — Context    提供什么背景信息         │
│  T — Task       要完成什么具体任务       │
│  E — Example    给出什么示例参考         │
└─────────────────────────────────────────┘
```

**❌ 差的 Prompt**：
> "帮我写个方案"

**✅ 好的 Prompt**：
> ```
> Role: 你是一位资深建筑设计师，有15年商业空间设计经验
> Context: 我要在大学城旁边开一个面向学生的现代风格咖啡馆，
>         面积约200平米，预算50万元，目标客群是大学生和年轻教师
> Task: 请为我设计一份完整的咖啡馆方案，包括：
>       1. 空间布局规划（座位区、吧台区、户外区）
>       2. 设计风格说明
>       3. 材料选择建议
>       4. 灯光设计方案
> Example: 参考类似 Manner Coffee 的简约工业风设计
> ```

#### 2.3 常见 Prompt 技巧

| 技巧 | 说明 | 示例 |
|------|------|------|
| **分步提问** | 把大任务拆成小步骤 | "首先…然后…最后…" |
| **设定格式** | 明确输出格式 | "请用表格形式输出" / "请用 Markdown 格式" |
| **思维链** | 要求 AI 展示推理过程 | "请一步步思考，先分析问题，再给出结论" |
| **Few-shot** | 提供 2-3 个示例 | "参考以下两个案例的风格…" |
| **负面约束** | 明确不要什么 | "不要使用过于专业的术语" |
| **角色扮演** | 给 AI 设定专业身份 | "你是一位有10年经验的 Python 工程师" |
| **迭代优化** | 根据回答持续调整 Prompt | "上一个版本太简略了，请展开第三部分" |

#### 2.4 不同任务的 Prompt 模板

**写作类**：
```
Role: 你是一位 [领域] 的资深专家
Context: 目标读者是 [读者特征]，他们关心 [核心关切]
Task: 请写一篇关于 [主题] 的 [文体类型]
要求：
- 字数：[800-1000字]
- 风格：[学术严谨/轻松易读/实操性强]
- 结构：[引言-正文3部分-结论]
- 包含：[数据支撑/案例分析/实操建议]
```

**编程类**：
```
Role: 你是一位资深 Python 后端工程师
Context: 项目使用 [框架/库]，运行在 [环境]
Task: 请实现 [功能描述]
要求：
- 代码注释用中文
- 处理边缘情况（空值、超时等）
- 遵循 PEP 8 代码规范
```

**分析类**：
```
Role: 你是一位数据分析师
Context: 这是一份 [数据说明]，包含 [字段说明]
Task: 请分析这份数据，找出：
1. 主要趋势
2. 异常值
3. 可行的优化建议
输出格式：用要点列表，每个要点不超过2行
```

### 三、实操环节（60分钟）

#### 实操 3.1：论文写作（15分钟）

用以下 Prompt 让 AI 帮你写一篇课程论文大纲：

```
Role: 你是一位学术写作导师
Context: 我是一名大二工程设计专业学生，需要写一篇关于
        "AI在工程设计中的应用"的课程论文，3000字
Task: 请帮我：
1. 设计论文大纲（含章节标题和每节要点）
2. 列出每个章节需要查找的资料类型
3. 给出写作时间安排建议
```

#### 实操 3.2：代码编写（15分钟）

用以下 Prompt 让 AI 帮你写代码：

```
Role: 你是一位 Python 数据分析专家
Context: 我有一份 Excel 数据"sales.xlsx"，包含列：
        日期、产品、销售额、数量、地区
Task: 请写一个 Python 脚本：
1. 读取 Excel 文件
2. 按月份汇总销售额
3. 画出月度销售额趋势图
4. 找出销售额最高的5个产品
要求：代码有详细注释，使用 Pandas 和 Matplotlib
```

#### 实操 3.3：方案设计（15分钟）

选择一个你感兴趣的场景，用 RCTE 框架写 Prompt 生成方案。例如：

```
Role: 你是一位资深产品经理，有10年互联网产品经验
Context: 我们团队想做一个小程序，帮助大学生找到校内
        空余自习室，目前市场上类似产品很少
Task: 请帮我设计一份产品方案：
1. 目标用户画像
2. 核心功能列表（按优先级排序）
3. 商业模式建议
4. MVP 版本的功能范围
```

#### 实操 3.4：PPT 制作（15分钟）

让 AI 帮你生成 PPT 大纲和内容：

```
Role: 你是一位专业演示设计顾问
Context: 我要向学院领导汇报"AI学习小组"的筹建计划，时长为5分钟
Task: 请生成一份PPT大纲：
1. 按页给出每页标题和要点
2. 标注每页适合的视觉形式（图表/图片/图标）
3. 给出演讲者的口播提示
要求：共10页以内，风格专业但不沉闷
```

### 四、课后作业

1. 用 RCTE 框架写 5 个不同场景的 Prompt（学习/生活/专业各至少1个），并在 AI 工具中测试效果
2. 选择同一任务，分别用"简单 Prompt"和"结构化 Prompt"让 AI 完成，对比结果差异
3. 阅读：[Anthropic 官方 Prompt Engineering 指南](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

### 五、常见问题

**Q: Prompt 越长越好吗？**
A: 不一定。关键是**信息密度**而非文字数量。简洁但要素齐全的 Prompt 往往效果最好。

**Q: AI 能记住之前的对话吗？**
A: 在同一会话中可以记住上下文。但不同会话之间不共享记忆。重要的背景信息要在每次对话开头说明。

**Q: 为什么同样的 Prompt 有时结果不同？**
A: 大模型有一定随机性（temperature 参数控制）。如果需要稳定输出，可以在 Prompt 中要求"请给出确定性的回答"。

---

## 第3课：AI 办公自动化

### 一、学习目标

- 掌握 AI 辅助 Word 文档撰写的技巧
- 学会用 AI 处理 Excel 数据
- 能够用 AI 生成 PPT 内容
- 掌握 AI 辅助 PDF 和文献阅读的方法
- 完成一个完整的项目方案作为本周综合作业

### 二、核心知识点

#### 2.1 AI + Word：文档撰写

**场景覆盖**：
| 场景 | AI 可以做什么 | 你的角色 |
|------|--------------|----------|
| 写报告 | 生成初稿、润色、调整语气 | 明确需求、审核事实、把控质量 |
| 写邮件 | 生成模板、优化表达 | 确认收件人、补充具体信息 |
| 写方案 | 搭框架、填内容、提供创意 | 确定方向、验证可行性、决策 |
| 写会议纪要 | 整理录音转文字、提炼要点 | 补充遗漏、标注重点 |

**工作流程**：
```
1. 明确目标 → 2. 用 AI 生成大纲 → 3. 逐节让 AI 扩展内容
→ 4. 人工审核修改 → 5. 用 AI 润色语言 → 6. 最终定稿
```

#### 2.2 AI + Excel：数据处理

**AI 辅助 Excel 的三种方式**：

| 方式 | 适用场景 | 示例 |
|------|----------|------|
| **问公式** | 需要复杂 Excel 公式 | "如何用 VLOOKUP 匹配两个表格？" |
| **问分析** | 需要数据分析思路 | "这份销售数据应该从哪些维度分析？" |
| **写代码** | 数据处理量大、逻辑复杂 | "用 Python 处理这个 Excel 并输出结果" |

> 💡 **建议**：对于超过 1000 行的数据，直接用 Python + Pandas 比 Excel 公式更高效。AI 可以帮你写代码！

#### 2.3 AI + PPT：演示文稿制作

**AI 辅助 PPT 制作流程**：

```
第1步：用 AI 生成大纲和每页内容
第2步：人工审核和调整结构
第3步：在 PowerPoint/Keynote 中套用模板
第4步：用 AI 生成配图（Midjourney/DALL-E）
第5步：用 AI 优化演讲词
```

**一键生成 PPT 的 Prompt 模板**：
```
Role: 你是一位演示设计专家
Context: [汇报对象、场合、时长]
Task: 请为 [主题] 设计一个 PPT 大纲
要求：
- 总共不超过 [X] 页
- 每页给出：标题 + 3-5个要点 + 建议的配图类型
- 整体风格：[专业/活泼/极简]
- 重点突出：[核心数据/解决方案/未来计划]
```

#### 2.4 AI + PDF/文献阅读

这是对大学生最有价值的能力之一。

**AI 辅助文献阅读流程**：
```
1. 上传 PDF 到 AI 工具（Claude/ChatGPT 支持直接上传）
2. 让 AI 用中文总结论文核心内容
3. 针对不理解的部分深入提问
4. 让 AI 对比多篇论文的观点差异
5. 让 AI 生成文献综述的初稿
```

**经典 Prompt**：
```
请帮我分析这篇论文：
1. 研究问题是什么？
2. 用了什么方法？
3. 核心发现是什么？
4. 有什么局限性？
5. 对我的 [课题名称] 有什么参考价值？
请用中文回答，避免过于专业的术语。
```

### 三、实操环节（60分钟）

#### 实操 3.1：生成项目方案（30分钟）

**任务**：用 AI 完整生成一份你专业领域的项目方案。

以工程设计专业为例，请 AI 帮你完成：

```
Role: 你是一位资深工程设计项目经理
Context: 我是一名大三工程设计专业学生，需要完成一份
        "智能校园垃圾分类站"的课程设计方案
Task: 请帮我撰写完整方案，包含以下章节：
1. 项目背景与意义
2. 需求分析（用户调研、痛点分析）
3. 设计方案（结构设计、功能设计、技术选型）
4. 实施计划（时间安排、人员分工）
5. 预算估算
6. 风险评估与应对措施
要求：
- 用词专业但不晦涩
- 包含具体的尺寸、材料、技术参数建议
- 每个章节 300-500 字
```

**操作步骤**：
1. 将上述 Prompt 发送给 AI
2. 仔细阅读 AI 生成的方案
3. 标注出需要修改或补充的部分
4. 让 AI 针对特定章节展开详细描述
5. 最后让 AI 生成一个方案 PPT 的大纲

#### 实操 3.2：AI 处理表格数据（15分钟）

场景：你有一份实验数据需要整理和分析。

```
Role: 你是一位数据分析专家
Context: 以下是我们材料力学实验的数据（提供数据）
Task: 请帮我：
1. 计算每组数据的平均值和标准差
2. 判断是否有异常值需要剔除
3. 分析各组数据之间的差异是否显著
4. 给出实验结论的撰写建议
```

#### 实操 3.3：AI 辅助文献综述（15分钟）

场景：你需要写一篇关于"AI 在XX领域应用"的文献综述。

```
Role: 你是一位学术研究方法论专家
Context: 我需要写一篇"AI在建筑能耗优化中的应用"的文献综述
Task: 请帮我：
1. 列出这个领域需要检索的关键词（中英文）
2. 给出一份推荐的文献检索策略
3. 提供一个文献综述的写作框架
4. 列举该领域目前的主要研究方向和代表观点
```

### 四、课后作业（第1周综合）

> 🎯 **本周大作业**：用 AI 完成一份与你的专业相关的完整方案设计
>
> **要求**：
> 1. 包含：背景分析、方案设计、实施计划、预算、风险评估
> 2. 至少 2000 字
> 3. 全程使用 AI 辅助（包括但不限于：大纲设计、内容生成、语言润色、表格生成）
> 4. 随方案提交一份"AI 使用记录"：列出你用了哪些 AI 工具、每个工具完成了什么部分
>
> **评分标准**：
> - 方案完整性 30%
> - 方案可行性 30%
> - AI 使用效率 20%
> - AI 使用记录详实度 20%

---

# 第2周：Python 基础

---

## 第1课：Python 语法入门

### 一、学习目标

- 完成 Python 环境安装（Anaconda + Jupyter Notebook）
- 掌握 Python 基本语法：变量、数据类型、条件判断、循环
- 掌握列表和字典的基本操作
- 能用 AI 辅助写 Python 代码

### 二、核心知识点

#### 2.1 环境安装

**推荐方案：Anaconda + Jupyter Notebook**

> **为什么推荐这个组合？** Anaconda 自带 Python 和常用科学计算库，不需要手动配置环境变量。Jupyter Notebook 可以逐段运行代码，非常适合学习。

**安装步骤**：

1. 访问 [https://www.anaconda.com/download](https://www.anaconda.com/download)
2. 下载对应系统的安装包（选择 Python 3.x 最新版）
3. 双击安装，一路 Next（Windows）/ 拖入 Applications（macOS）
4. 安装完成后，在开始菜单找到 **Jupyter Notebook**，点击启动
5. 浏览器会自动打开 Jupyter 界面，点击右上角 **New → Python 3** 创建第一个 Notebook

> ⚠️ **如果安装遇到问题**：直接问 ChatGPT/Claude："我在 Windows/Mac 上安装 Anaconda 遇到了 [具体错误信息]，怎么解决？"

#### 2.2 第一个 Python 程序

```python
# 这是我的第一个 Python 程序
print("Hello, AI World!")

# 计算
a = 10
b = 20
print(a + b)  # 输出 30
```

#### 2.3 变量与数据类型

```python
# Python 是动态类型语言，不需要声明类型
name = "张三"           # 字符串 str
age = 20                # 整数 int
height = 1.75           # 浮点数 float
is_student = True       # 布尔值 bool

# 查看变量类型
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
print(type(height))     # <class 'float'>
print(type(is_student)) # <class 'bool'>

# 字符串操作
greeting = "你好" + name  # 字符串拼接
print(greeting)          # 你好张三

long_text = f"我叫{name}，今年{age}岁"  # f-string 格式化
print(long_text)         # 我叫张三，今年20岁
```

#### 2.4 条件判断

```python
# if-elif-else 结构
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数：{score}，等级：{grade}")  # 分数：85，等级：B

# 比较运算符：== != > < >= <=
# 逻辑运算符：and or not
```

#### 2.5 循环

```python
# for 循环 — 遍历序列
fruits = ["苹果", "香蕉", "橘子"]
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# for + range
for i in range(5):    # 0, 1, 2, 3, 4
    print(f"第{i+1}次循环")

# while 循环
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1   # 等同于 count = count + 1
```

#### 2.6 列表（List）

```python
# 创建列表
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]  # 可以混合类型

# 列表操作
numbers.append(6)       # 末尾添加 → [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)    # 指定位置插入 → [0, 1, 2, 3, 4, 5, 6]
numbers.remove(3)       # 删除指定值 → [0, 1, 2, 4, 5, 6]
last = numbers.pop()    # 删除并返回末尾元素
print(numbers[0])       # 索引访问 → 0
print(numbers[-1])      # 倒数第一个 → 5
print(numbers[1:4])     # 切片 → [1, 2, 4]
print(len(numbers))     # 长度 → 6
```

#### 2.7 字典（Dict）

```python
# 创建字典 — 键值对
student = {
    "name": "张三",
    "age": 20,
    "major": "工程设计",
    "scores": [85, 90, 78]
}

# 字典操作
print(student["name"])           # 张三
student["grade"] = "大二"         # 添加新键值对
print(student.get("height", 0))  # 安全获取，不存在返回默认值 0

# 遍历字典
for key, value in student.items():
    print(f"{key}: {value}")
```

### 三、实操环节（60分钟）

#### 实操 3.1：安装环境 + 第一个 Notebook（20分钟）

跟着以下步骤操作：

1. 安装 Anaconda（如果还没装）
2. 启动 Jupyter Notebook
3. 创建新的 Notebook
4. 逐段运行上述每个代码示例
5. **重点**：遇到错误不要慌，把错误信息复制给 ChatGPT/Claude，让 AI 帮你 Debug

#### 实操 3.2：班级成绩统计器（20分钟）

在 Jupyter Notebook 中完成以下练习：

```python
# 练习：班级成绩统计器
# 目标：输入5个学生的成绩，输出平均分、最高分、最低分、及格率

# 第1步：创建一个包含5个学生成绩的列表
scores = [78, 92, 65, 88, 55]

# 第2步：计算统计量
average = sum(scores) / len(scores)  # 平均分
highest = max(scores)                 # 最高分
lowest = min(scores)                  # 最低分

# 第3步：计算及格率（60分及以上为及格）
pass_count = 0
for score in scores:
    if score >= 60:
        pass_count += 1
pass_rate = pass_count / len(scores) * 100

# 第4步：输出结果
print(f"成绩列表：{scores}")
print(f"平均分：{average:.1f}")
print(f"最高分：{highest}")
print(f"最低分：{lowest}")
print(f"及格率：{pass_rate:.1f}%")
```

#### 实操 3.3：通讯录管理（20分钟）

```python
# 练习：用字典和列表做一个简易通讯录
# 目标：能添加、查找、删除联系人

contacts = []  # 用一个列表存储所有联系人

def add_contact(name, phone, email):
    """添加联系人"""
    contact = {
        "name": name,
        "phone": phone,
        "email": email
    }
    contacts.append(contact)
    print(f"✓ 已添加联系人：{name}")

def find_contact(name):
    """查找联系人"""
    for contact in contacts:
        if contact["name"] == name:
            return contact
    return None

# 测试
add_contact("张三", "13800138000", "zhangsan@email.com")
add_contact("李四", "13900139000", "lisi@email.com")

result = find_contact("张三")
if result:
    print(f"找到联系人：{result}")
else:
    print("未找到该联系人")

print(f"通讯录共 {len(contacts)} 人")
```

### 四、课后作业

1. 用 Python 写一个"BMI 计算器"：输入身高(m)和体重(kg)，输出 BMI 值和健康评价
2. 用 Python 写一个"猜数字游戏"：程序随机生成 1-100 的数字，用户来猜，给出"大了/小了"的提示
3. 用字典和列表写一个"学生管理系统"：能添加学生（姓名、学号、成绩）、查询学生、列出所有学生

> 💡 **提示**：不会写的部分直接问 ChatGPT/Claude，但要确保你理解 AI 给出的代码每一行是什么意思。

---

## 第2课：函数、模块与文件操作

### 一、学习目标

- 理解函数的概念和用法
- 掌握模块导入和使用
- 学会用类组织代码
- 能够读写文件

### 二、核心知识点

#### 2.1 函数

```python
# 函数定义
def greet(name):
    """向指定的人打招呼"""  # 这是文档字符串（docstring）
    return f"你好，{name}！"

# 函数调用
message = greet("张三")
print(message)  # 你好，张三！

# 带多个参数和默认值的函数
def calculate_bmi(weight, height, unit="metric"):
    """
    计算BMI
    weight: 体重（kg）
    height: 身高（m）
    """
    bmi = weight / (height ** 2)
    return round(bmi, 1)  # 保留1位小数

# 调用
my_bmi = calculate_bmi(70, 1.75)
print(f"你的BMI是：{my_bmi}")  # 你的BMI是：22.9

# 带多个返回值的函数
def analyze_numbers(numbers):
    """分析数字列表，返回多个统计值"""
    avg = sum(numbers) / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    return avg, maximum, minimum

scores = [85, 92, 78, 90, 88]
avg, max_s, min_s = analyze_numbers(scores)  # 解包
print(f"平均{avg}, 最高{max_s}, 最低{min_s}")
```

#### 2.2 模块

```python
# 导入内置模块
import math
import random
from datetime import datetime

# 使用 math 模块
print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(math.sin(math.pi/2))  # 1.0

# 使用 random 模块
print(random.randint(1, 100))    # 随机整数 1-100
print(random.choice(["苹果", "香蕉", "橘子"]))  # 随机选择一个
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)           # 打乱顺序

# 使用 datetime 模块
now = datetime.now()
print(f"当前时间：{now}")
print(f"今天是 {now.year}年{now.month}月{now.day}日")
```

#### 2.3 类与面向对象

```python
# 定义一个"学生"类
class Student:
    """学生类"""
    
    def __init__(self, name, student_id, major):
        """初始化方法 — 创建学生对象时自动调用"""
        self.name = name
        self.student_id = student_id
        self.major = major
        self.scores = []  # 成绩列表
    
    def add_score(self, score):
        """添加一门课的成绩"""
        self.scores.append(score)
        print(f"{self.name} 添加成绩：{score}")
    
    def get_average(self):
        """计算平均分"""
        if len(self.scores) == 0:
            return 0
        return sum(self.scores) / len(self.scores)
    
    def summary(self):
        """输出学生信息摘要"""
        return f"{self.name}({self.student_id}) - {self.major} | 平均分：{self.get_average():.1f}"

# 创建学生对象
s1 = Student("张三", "2024001", "工程设计")
s1.add_score(85)
s1.add_score(90)
print(s1.summary())

s2 = Student("李四", "2024002", "机械工程")
s2.add_score(78)
print(s2.summary())
```

#### 2.4 文件操作

```python
# 写入文件
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("这是第一行\n")
    f.write("这是第二行\n")
    f.write("AI学习笔记\n")

print("文件写入完成！")

# 读取文件
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("文件内容：")
    print(content)

# 逐行读取
with open("notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        print(f"→ {line.strip()}")  # strip() 去除首尾空白和换行符

# 追加写入
with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("这是追加的内容\n")
```

### 三、实操环节（60分钟）

#### 实操 3.1：函数练习 — 温度转换器（15分钟）

```python
# 练习：摄氏度与华氏度互相转换

def celsius_to_fahrenheit(celsius):
    """摄氏度 → 华氏度"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    """华氏度 → 摄氏度"""
    return (fahrenheit - 32) * 5/9

# 测试
print(f"0°C = {celsius_to_fahrenheit(0):.1f}°F")     # 32.0°F
print(f"100°C = {celsius_to_fahrenheit(100):.1f}°F")  # 212.0°F
print(f"32°F = {fahrenheit_to_celsius(32):.1f}°C")    # 0.0°C
print(f"212°F = {fahrenheit_to_celsius(212):.1f}°C")  # 100.0°C
```

#### 实操 3.2：类练习 — 图书管理系统（25分钟）

```python
# 练习：简易图书管理系统

class Book:
    """图书类"""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
    
    def borrow(self):
        if self.is_borrowed:
            print(f"《{self.title}》已被借出")
            return False
        self.is_borrowed = True
        print(f"✓ 已借出《{self.title}》")
        return True
    
    def return_book(self):
        if not self.is_borrowed:
            print(f"《{self.title}》未被借出")
            return False
        self.is_borrowed = False
        print(f"✓ 已归还《{self.title}》")
        return True

class Library:
    """图书馆类"""
    def __init__(self, name):
        self.name = name
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
        print(f"✓ 《{book.title}》已入库")
    
    def list_books(self):
        print(f"\n=== {self.name} 藏书列表 ===")
        for book in self.books:
            status = "已借出" if book.is_borrowed else "可借"
            print(f"《{book.title}》- {book.author} | {status}")

# 使用
lib = Library("我的书架")
lib.add_book(Book("Python入门", "张三", "001"))
lib.add_book(Book("AI导论", "李四", "002"))
lib.add_book(Book("设计思维", "王五", "003"))

lib.list_books()
lib.books[0].borrow()   # 借第一本书
lib.books[0].borrow()   # 尝试再次借（应提示已借出）
lib.books[0].return_book()
lib.list_books()
```

#### 实操 3.3：文件操作 — 学习笔记管理（20分钟）

```python
# 练习：写一个学习笔记管理器
import os
from datetime import datetime

class NoteManager:
    """笔记管理器"""
    
    def __init__(self, file_path="my_notes.md"):
        self.file_path = file_path
    
    def add_note(self, title, content):
        """添加一条笔记"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"\n## {title}\n")
            f.write(f"*{timestamp}*\n\n")
            f.write(f"{content}\n")
            f.write("\n---\n")
        print(f"✓ 笔记《{title}》已保存")
    
    def read_notes(self):
        """读取所有笔记"""
        if not os.path.exists(self.file_path):
            print("暂无笔记")
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            print(f.read())

# 使用
nm = NoteManager()
nm.add_note("Python 函数学习", 
            "今天学习了函数定义、参数传递和返回值。"
            "函数用 def 定义，可以带默认参数。")
nm.add_note("AI 学习计划", 
            "本周目标：完成 Python 基础学习，"
            "下周开始接触机器学习。")
print("\n===== 所有笔记 =====")
nm.read_notes()
```

### 四、课后作业

1. 写一个"计算器"类 Calculator，支持加减乘除四种运算
2. 写一个"日记本"程序：支持添加日记（自动记录时间）、查看所有日记、搜索日记（按关键词）
3. 将第1课的"班级成绩统计器"改为函数版本，要求支持从文件读取成绩列表

---

## 第3课：Python 数据分析入门

### 一、学习目标

- 掌握 NumPy 数组的基本操作
- 掌握 Pandas DataFrame 的创建、筛选、聚合
- 学会用 Matplotlib 绘制常用图表
- 能够分析真实的 Excel 数据

### 二、核心知识点

#### 2.1 NumPy — 数值计算基础

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
print(arr)           # [1 2 3 4 5]
print(arr.shape)     # (5,) — 一维数组，5个元素
print(arr.dtype)     # int64

# 创建特殊数组
zeros = np.zeros(5)          # [0. 0. 0. 0. 0.]
ones = np.ones((3, 3))       # 3×3 全1矩阵
range_arr = np.arange(0, 10, 2)  # [0 2 4 6 8] — 0到10步长为2

# 数组运算（向量化运算，不需要循环）
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)   # [5 7 9] — 逐元素相加
print(a * b)   # [4 10 18] — 逐元素相乘
print(a ** 2)  # [1 4 9] — 逐元素平方

# 统计函数
scores = np.array([85, 92, 78, 90, 88, 65, 95])
print(f"平均分：{scores.mean():.1f}")
print(f"标准差：{scores.std():.1f}")
print(f"最高分：{scores.max()}")
print(f"最低分：{scores.min()}")
print(f"中位数：{np.median(scores)}")
```

#### 2.2 Pandas — 数据分析核心

```python
import pandas as pd

# 创建 DataFrame
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "语文": [85, 92, 78, 90],
    "数学": [82, 88, 90, 85],
    "英语": [78, 85, 82, 92]
}
df = pd.DataFrame(data)
print(df)
```

输出：
```
   姓名  语文  数学  英语
0  张三  85  82  78
1  李四  92  88  85
2  王五  78  90  82
3  赵六  90  85  92
```

```python
# 基本操作
print(df.head(2))      # 查看前2行
print(df.describe())   # 统计摘要（均值、标准差等）
print(df["语文"])       # 选择一列
print(df[["姓名", "语文"]])  # 选择多列

# 添加新列
df["总分"] = df["语文"] + df["数学"] + df["英语"]
df["平均分"] = df["总分"] / 3

# 筛选
high_scores = df[df["平均分"] >= 85]  # 平均分 >= 85 的学生
print(high_scores)

# 排序
df_sorted = df.sort_values("总分", ascending=False)
print(df_sorted)

# 分组聚合
# 假设有多个班级的数据
df["班级"] = ["1班", "1班", "2班", "2班"]
class_avg = df.groupby("班级")["平均分"].mean()
print(class_avg)
```

#### 2.3 Matplotlib — 数据可视化

```python
import matplotlib.pyplot as plt

# 数据准备
months = ["1月", "2月", "3月", "4月", "5月", "6月"]
sales = [12000, 13500, 11800, 15000, 14200, 16800]
costs = [8000, 8500, 8200, 9000, 8800, 9500]

# 折线图
plt.figure(figsize=(10, 5))
plt.plot(months, sales, marker='o', label='销售额', linewidth=2)
plt.plot(months, costs, marker='s', label='成本', linewidth=2)
plt.title('上半年销售趋势', fontsize=16)
plt.xlabel('月份')
plt.ylabel('金额（元）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 柱状图
plt.figure(figsize=(8, 5))
products = ['产品A', '产品B', '产品C', '产品D', '产品E']
counts = [234, 189, 156, 298, 201]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

plt.bar(products, counts, color=colors)
plt.title('各产品销量对比')
plt.xlabel('产品')
plt.ylabel('销量（件）')
plt.show()

# 饼图
plt.figure(figsize=(8, 8))
regions = ['华东', '华南', '华北', '西南', '其他']
ratios = [35, 25, 20, 12, 8]
explode = (0.05, 0, 0, 0, 0)  # 突出显示华东

plt.pie(ratios, labels=regions, autopct='%1.1f%%', 
        explode=explode, shadow=True)
plt.title('各区域销售占比')
plt.show()
```

### 三、实操环节（60分钟）

#### 实操 3.1：分析真实 Excel 数据（30分钟）

**前提准备**：创建一份模拟的销售数据 Excel 文件。你可以直接用下面的代码生成：

```python
import pandas as pd
import numpy as np

# 生成模拟数据
np.random.seed(42)
dates = pd.date_range('2026-01-01', periods=100, freq='D')
products = np.random.choice(['产品A', '产品B', '产品C', '产品D'], 100)
regions = np.random.choice(['华东', '华南', '华北', '西南'], 100)
quantities = np.random.randint(1, 50, 100)
prices = np.random.choice([99, 199, 299, 399, 499], 100)
amounts = quantities * prices

# 创建 DataFrame
df = pd.DataFrame({
    '日期': dates,
    '产品': products,
    '地区': regions,
    '数量': quantities,
    '单价': prices,
    '金额': amounts
})

# 保存为 Excel
df.to_excel('sales_data.xlsx', index=False)
print("模拟数据已生成：sales_data.xlsx")

# --- 开始分析 ---

# 1. 读取数据
df = pd.read_excel('sales_data.xlsx')
print(f"数据量：{len(df)} 条记录")
print(f"时间范围：{df['日期'].min()} 至 {df['日期'].max()}")

# 2. 总览
print("\n=== 数据预览 ===")
print(df.head(10))

# 3. 各产品销售额
print("\n=== 各产品销售额 ===")
product_sales = df.groupby('产品')['金额'].sum().sort_values(ascending=False)
print(product_sales)

# 4. 各地区销售额
print("\n=== 各地区销售额 ===")
region_sales = df.groupby('地区')['金额'].sum().sort_values(ascending=False)
print(region_sales)

# 5. 月度趋势
df['月份'] = df['日期'].dt.to_period('M')
monthly_sales = df.groupby('月份')['金额'].sum()
print("\n=== 月度销售趋势 ===")
print(monthly_sales)

# 6. 可视化
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 产品销售柱状图
product_sales.plot(kind='bar', ax=axes[0], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
axes[0].set_title('各产品销售额')
axes[0].set_ylabel('金额（元）')

# 地区销售饼图
region_sales.plot(kind='pie', ax=axes[1], autopct='%1.1f%%')
axes[1].set_title('各区域销售占比')
axes[1].set_ylabel('')

# 月度趋势折线图
monthly_sales.plot(kind='line', ax=axes[2], marker='o', linewidth=2)
axes[2].set_title('月度销售趋势')
axes[2].set_ylabel('金额（元）')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

#### 实操 3.2：学生成绩分析（20分钟）

```python
# 场景：分析班级期中考试成绩
import pandas as pd
import matplotlib.pyplot as plt

# 创建成绩数据
scores_data = {
    '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
            '郑一', '陈二', '林三', '黄四', '何五', '刘六', '杨七', '许八'],
    '语文': [85, 92, 78, 90, 82, 76, 88, 95, 70, 84, 91, 73, 86, 79, 93, 81],
    '数学': [82, 88, 90, 85, 78, 70, 85, 92, 68, 80, 89, 75, 90, 72, 87, 83],
    '英语': [78, 85, 82, 92, 75, 80, 90, 88, 72, 86, 78, 70, 84, 76, 82, 79]
}
df = pd.DataFrame(scores_data)

# 1. 添加总分和平均分
df['总分'] = df['语文'] + df['数学'] + df['英语']
df['平均分'] = (df['总分'] / 3).round(1)

# 2. 添加等级
def get_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'

df['等级'] = df['平均分'].apply(get_grade)

# 3. 排名
df['排名'] = df['总分'].rank(ascending=False).astype(int)
df_sorted = df.sort_values('总分', ascending=False)

# 4. 统计报告
print("=" * 50)
print("            期中考试成绩分析报告")
print("=" * 50)
print(f"\n班级人数：{len(df)}")
print(f"总分平均：{df['总分'].mean():.1f}")
print(f"总分最高：{df['总分'].max()}")
print(f"总分最低：{df['总分'].min()}")
print(f"总分标准差：{df['总分'].std():.1f}")

print(f"\n各科平均分：")
print(f"  语文：{df['语文'].mean():.1f}")
print(f"  数学：{df['数学'].mean():.1f}")
print(f"  英语：{df['英语'].mean():.1f}")

print(f"\n等级分布：")
print(df['等级'].value_counts().sort_index())

print(f"\n=== 排名前5 ===")
print(df_sorted[['排名', '姓名', '总分', '平均分', '等级']].head(5))

# 5. 可视化
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 各科成绩箱线图
axes[0, 0].boxplot([df['语文'], df['数学'], df['英语']], labels=['语文', '数学', '英语'])
axes[0, 0].set_title('各科成绩分布')
axes[0, 0].set_ylabel('分数')

# 总分分布直方图
axes[0, 1].hist(df['总分'], bins=8, edgecolor='white', color='steelblue')
axes[0, 1].set_title('总分分布')
axes[0, 1].set_xlabel('总分')
axes[0, 1].set_ylabel('人数')

# 每位学生的各科成绩对比
x = range(len(df))
width = 0.25
axes[1, 0].bar(x, df['语文'], width, label='语文', color='#FF6B6B')
axes[1, 0].bar([i+width for i in x], df['数学'], width, label='数学', color='#4ECDC4')
axes[1, 0].bar([i+2*width for i in x], df['英语'], width, label='英语', color='#45B7D1')
axes[1, 0].set_title('学生各科成绩对比')
axes[1, 0].set_xticks([i+width for i in x])
axes[1, 0].set_xticklabels(df['姓名'], rotation=45, fontsize=8)
axes[1, 0].legend()

# 等级分布饼图
grade_counts = df['等级'].value_counts().sort_index()
axes[1, 1].pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
               colors=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6'])
axes[1, 1].set_title('等级分布')

plt.tight_layout()
plt.show()
```

#### 实操 3.3：自由练习（10分钟）

上述两个练习完成后，尝试修改参数：
- 增加更多学生
- 修改分数
- 增加新的分析维度（如各科及格率、最高分与最低分差距等）

### 四、课后作业（第2周综合）

> 🎯 **本周大作业**：分析一份真实数据
>
> **任务**：
> 1. 找一份你感兴趣的 Excel 数据（课程实验数据/网上下载的公开数据/自己编的数据都可以）
> 2. 用 Pandas 读取并完成以下分析：
>    - 数据清洗（检查缺失值、异常值）
>    - 描述性统计（均值、中位数、标准差等）
>    - 至少 3 个维度的分组聚合
>    - 至少 3 种图表可视化
> 3. 写一份 500 字的数据分析报告
>
> **提交内容**：
> - Jupyter Notebook 文件（含代码和输出）
> - 数据文件
> - 分析报告（Markdown 或 Word）

---

# 第3周：机器学习入门

---

## 第1课：什么是机器学习

### 一、学习目标

- 理解机器学习与传统编程的区别
- 掌握数据、标签、特征、模型等核心概念
- 理解监督学习、无监督学习、强化学习的区别
- 通过垃圾邮件识别案例理解 ML 的工作流程

### 二、核心知识点

#### 2.1 传统编程 vs 机器学习

```
传统编程：
  输入数据 + 规则 → 输出结果
  
  例：输入一串数字 + 排序规则 → 输出排好序的数字
  程序员写好规则，计算机按规则执行

机器学习：
  输入数据 + 输出结果（标签）→ 学习出规则（模型）
  
  例：输入1000封邮件（已标注"垃圾"或"正常"）→ 模型学会分类规则
  计算机从数据中自动学习规则
```

> 💡 **一句话理解**：传统编程是"人写规则"，机器学习是"人给例子，AI自己学规则"。

#### 2.2 核心概念

| 概念 | 类比（垃圾邮件识别） | 说明 |
|------|---------------------|------|
| **数据 (Data)** | 1000封邮件 | 学习的原材料 |
| **标签 (Label)** | 每封邮件标注"垃圾"或"正常" | 正确答案，监督学习需要 |
| **特征 (Feature)** | 邮件里的关键词、发件人、发送时间等 | 用来做判断的依据 |
| **模型 (Model)** | 训练出的分类器 | 从数据中学到的"规则" |
| **训练 (Training)** | 给模型看已标注的邮件 | 让模型学习的过程 |
| **预测 (Prediction)** | 新邮件来了，判断是不是垃圾 | 用训练好的模型做判断 |

#### 2.3 机器学习三大类型

```
┌──────────────────────────────────────────────────────┐
│                    机器学习                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │   监督学习    │ │   无监督学习  │ │   强化学习    │  │
│  │ Supervised   │ │ Unsupervised │ │ Reinforcement│  │
│  │ 数据有标签    │ │ 数据无标签    │ │ 与环境互动    │  │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘  │
│         │               │               │           │
│    · 分类              · 聚类           · 游戏AI     │
│    · 回归              · 降维           · 机器人控制  │
│    · 垃圾邮件识别      · 用户分群       · AlphaGo    │
│    · 房价预测          · 异常检测                    │
└──────────────────────────────────────────────────────┘
```

#### 2.4 机器学习工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    机器学习项目流程                           │
│                                                             │
│  1. 定义问题                                                │
│     ↓                                                       │
│  2. 收集数据 → 3. 数据清洗 → 4. 特征工程                     │
│     ↓                                                       │
│  5. 选择模型                                                │
│     ↓                                                       │
│  6. 训练模型                                                │
│     ↓                                                       │
│  7. 评估模型 → 8. 调参优化 → 9. 部署使用                     │
│                                                             │
│  ⚠️ 注意：步骤 2-4 通常占项目总时间的 60-80%！               │
└─────────────────────────────────────────────────────────────┘
```

#### 2.5 垃圾邮件识别案例详解

**第1步：定义问题**
- 输入：一封邮件的文本内容
- 输出：这封邮件是不是垃圾邮件（是/否）
- 这是一个**二分类**问题

**第2步：收集数据**
- 收集 1000 封已标注的邮件（已知哪些是垃圾哪些不是）
- 训练集（800封）— 用来训练模型
- 测试集（200封）— 用来检验模型效果

**第3步：提取特征**
- 从邮件文本中提取有用的信息作为特征：
  - 是否包含"免费"、"中奖"、"点击领取"等词
  - 发件人域名是否可疑
  - 邮件是否包含大量图片
  - 邮件发送时间是否异常

**第4步：训练模型**
```python
# 伪代码示意
model = NaiveBayes()  # 选择一个模型
model.fit(训练数据, 训练标签)  # 喂数据，让模型学习
```

**第5步：评估**
- 让模型预测测试集的 200 封邮件
- 对比预测结果和真实标签
- 计算准确率 = 正确预测数 / 总数

### 三、实操环节（60分钟）

#### 实操 3.1：感受"机器学习"（20分钟）

打开浏览器，体验以下交互式机器学习 Demo：

1. **Google Teachable Machine**：[https://teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com)
   - 选择"图像项目"
   - 用摄像头采集两类样本（比如"有人的照片"和"没有人的照片"）
   - 点击训练，体验"不用写代码的机器学习"
   
2. **Quick, Draw!**：[https://quickdraw.withgoogle.com](https://quickdraw.withgoogle.com)
   - 画画的游戏，背后是一个在不断学习的神经网络
   - 体验 AI 如何"猜"你在画什么

#### 实操 3.2：手动实现"最简单的机器学习"（20分钟）

```python
# 案例：用"经验规则" predict 房价
# 这是最简单的"学习"——从数据中找规律

# 已知数据：面积(㎡) → 价格(万元)
houses = [
    (50, 150),
    (60, 180),
    (70, 200),
    (80, 230),
    (90, 260),
    (100, 290),
    (110, 310),
    (120, 340),
]

# 我们假设关系是线性的：价格 ≈ k × 面积
# 从数据中"学习"k的值

areas = [h[0] for h in houses]
prices = [h[1] for h in houses]

# 简单估算：平均每平米价格
k = sum(prices) / sum(areas)
print(f"学到的规律：价格 ≈ {k:.3f} × 面积")
print(f"即每平米约 {k:.3f} 万元")

# 预测新房
new_area = 85
predicted_price = k * new_area
print(f"\n一套 {new_area}㎡ 的房子，预测价格约 {predicted_price:.1f} 万元")

# 对比已知数据，看看"模型"效果如何
print("\n模型效果检验：")
for area, actual_price in houses:
    predicted = k * area
    error = abs(predicted - actual_price)
    print(f"面积{area}㎡: 预测{predicted:.0f}万 vs 实际{actual_price}万 | 误差{error:.0f}万")

# 这就是最简单的"机器学习"：
# 1. 有数据(houses) 
# 2. 有"模型"(价格=k×面积)
# 3. 从数据中"学习"了k的值
# 4. 用学到的k做预测
```

#### 实操 3.3：Sklearn 数据预处理体验（20分钟）

```python
# 熟悉 Scikit-learn 的基本操作
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 1. 加载经典鸢尾花数据集
iris = load_iris()
print(f"数据集包含：{iris.data.shape[0]} 个样本")
print(f"每个样本有 {iris.data.shape[1]} 个特征")
print(f"特征名称：{iris.feature_names}")
print(f"类别名称：{iris.target_names}")

# 2. 转为 DataFrame 方便查看
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['类别'] = [iris.target_names[t] for t in iris.target]
print("\n前5行数据：")
print(df.head())

# 3. 查看数据基本信息
print("\n统计摘要：")
print(df.describe())

# 4. 划分训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
print(f"\n训练集大小：{X_train.shape[0]} 个样本")
print(f"测试集大小：{X_test.shape[0]} 个样本")

# 5. 标准化（让不同特征的数值在一个尺度上）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n数据标准化完成！")
print(f"训练集特征均值：{X_train_scaled.mean(axis=0).round(2)}")
print(f"训练集特征标准差：{X_train_scaled.std(axis=0).round(2)}")
# 标准化后均值为0，标准差为1
```

### 四、课后作业

1. 用自己的话解释：机器学习和传统编程有什么区别？（200字以内）
2. 举一个你生活中可以用"监督学习"解决的问题，说明需要什么数据、什么标签、什么特征
3. 了解三个机器学习在实际中的应用案例，并写出它们分别属于哪种类型（分类/回归/聚类等）

---

## 第2课：常见机器学习算法

### 一、学习目标

- 了解 5 种最常用的机器学习算法
- 理解每种算法的核心思想和适用场景
- 知道什么时候该用哪种算法

### 二、核心知识点

> ⚠️ **重要**：本节课不涉及数学公式推导，重点是建立直觉和学会选择。

#### 2.1 算法全景图

```
                    机器学习常用算法
                          │
        ┌─────────────────┼─────────────────┐
        │                  │                  │
      分类                回归              聚类
        │                  │                  │
   · Logistic         · Linear           · K-Means
     Regression          Regression      
   · Decision Tree     · Decision Tree    · DBSCAN
   · Random Forest     · Random Forest    
   · XGBoost           · XGBoost          
```

#### 2.2 线性回归（Linear Regression）

| 维度 | 说明 |
|------|------|
| **做什么** | 预测一个**连续数值**（如房价、温度、销售额） |
| **怎么做的** | 找一条最优直线拟合数据点 |
| **优点** | 简单、可解释、计算快 |
| **缺点** | 只能拟合线性关系，对异常值敏感 |
| **适用场景** | 房价预测、销量预测、分数预测 |
| **一句话理解** | 已知面积预测房价，本质是在坐标轴上画一条最合适的直线 |

#### 2.3 逻辑回归（Logistic Regression）

| 维度 | 说明 |
|------|------|
| **做什么** | **二分类**问题（是/否、通过/不通过） |
| **怎么做的** | 在线性回归基础上套一个 Sigmoid 函数，输出 0-1 之间的概率 |
| **优点** | 简单、可解释、输出的是概率值 |
| **缺点** | 只能处理线性可分的分类问题 |
| **适用场景** | 垃圾邮件识别、信用卡欺诈检测、疾病诊断 |
| **一句话理解** | 给你一个概率，"这封邮件是垃圾邮件的概率是 93%" |

> ⚠️ **注意**：虽然名字里有"回归"，但逻辑回归实际上是一个**分类**算法。

#### 2.4 决策树（Decision Tree）

| 维度 | 说明 |
|------|------|
| **做什么** | 分类和回归都可以 |
| **怎么做的** | 像"20个问题"游戏一样，一步步提问最终得出结论 |
| **优点** | 可解释性极强，能可视化整个决策过程 |
| **缺点** | 容易过拟合（一棵树记住所有训练数据），不稳定 |
| **适用场景** | 客户流失预测、贷款审批、医疗诊断 |
| **一句话理解** | 生日派对上玩"猜猜我是谁"的游戏："他有胡子吗？是→戴眼镜吗？是→是张三！" |

```
决策树示例：要不要去打球？

        天气如何？
       /        \
     晴天        雨天
     /            \
  湿度？        不去打球
  /    \
≤70%   >70%
/        \
去打球   不去打球
```

#### 2.5 随机森林（Random Forest）

| 维度 | 说明 |
|------|------|
| **做什么** | 分类和回归 |
| **怎么做的** | 种很多棵决策树（"森林"），每棵树给出自己的判断，最后投票决定 |
| **优点** | 准确率高、不容易过拟合、能处理高维数据 |
| **缺点** | 可解释性不如单棵决策树、计算量较大 |
| **适用场景** | 几乎所有分类和回归问题的"默认首选" |
| **一句话理解** | "三个臭皮匠，顶个诸葛亮"——100棵树各自投票，少数服从多数 |

#### 2.6 XGBoost

| 维度 | 说明 |
|------|------|
| **做什么** | 分类和回归 |
| **怎么做的** | 一棵树接一棵树，每棵新树专注纠正前面树的错误 |
| **优点** | 非常强大、Kaggle 竞赛冠军常客、工业界最爱 |
| **缺点** | 参数多，需要调参；可解释性差 |
| **适用场景** | 追求极致准确率的场景、Kaggle 比赛 |
| **一句话理解** | 不是"一群人一起讨论"，而是"一个人不断修改完善自己的答案" |

#### 2.7 算法选择速查表

```
问题是什么？
├── 预测一个数值（房价、温度、分数）
│   ├── 数据线性关系清晰 → 线性回归
│   └── 数据关系复杂 → 随机森林 / XGBoost
│
├── 分类（是/否、A类/B类/C类）
│   ├── 需要可解释 → 决策树 / 逻辑回归
│   ├── 追求高准确率 → 随机森林 / XGBoost
│   └── 数据量很大 → XGBoost
│
└── 没有标签，想发现数据中的分组
    └── K-Means 聚类
```

### 三、实操环节（60分钟）

#### 实操 3.1：算法交互式可视化（20分钟）

推荐在浏览器中打开以下可视化工具，直观感受不同算法的工作方式：

1. **TensorFlow Playground**：[https://playground.tensorflow.org](https://playground.tensorflow.org)
   - 选择不同的数据集（圆圈分布、螺旋分布等）
   - 调整神经网络层数和神经元数量
   - 观察模型如何"学会"分类

2. **Decision Tree Visualizer**：在 Jupyter 中运行：
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# 训练一棵小决策树（限制深度让它可视化好看）
iris = load_iris()
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(iris.data, iris.target)

# 可视化
plt.figure(figsize=(15, 8))
plot_tree(clf, feature_names=iris.feature_names, 
          class_names=iris.target_names.tolist(),  # 转为list
          filled=True, rounded=True, fontsize=10)
plt.title("鸢尾花分类决策树")
plt.show()
```

#### 实操 3.2：对比不同分类器（20分钟）

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import pandas as pd

# 生成模拟分类数据
X, y = make_classification(
    n_samples=1000, n_features=10, 
    n_informative=5, n_redundant=3,
    random_state=42
)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 定义要对比的模型
models = {
    "逻辑回归": LogisticRegression(max_iter=1000),
    "决策树": DecisionTreeClassifier(max_depth=5, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(n_estimators=100, random_state=42, verbosity=0)
}

# 训练并评估每个模型
results = []
for name, model in models.items():
    # 训练
    model.fit(X_train, y_train)
    # 评估
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    results.append({
        "模型": name,
        "训练集准确率": f"{train_score:.3f}",
        "测试集准确率": f"{test_score:.3f}",
        "差距": f"{train_score - test_score:.3f}"
    })

# 展示结果
results_df = pd.DataFrame(results)
print("=== 模型对比结果 ===")
print(results_df.to_string(index=False))
print("\n💡 '差距'越小说明过拟合越轻，泛化能力越好")
print("💡 测试集准确率才是我们真正关心的指标")
```

#### 实操 3.3：理解过拟合与欠拟合（20分钟）

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

# 生成带噪声的正弦数据
np.random.seed(42)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + np.random.normal(0, 0.1, X.shape[0])

# 创建3个不同复杂度的模型
depths = [2, 5, 15]  # 树的深度从小到大
titles = ['欠拟合 (depth=2)', '正好 (depth=5)', '过拟合 (depth=15)']

plt.figure(figsize=(15, 4))
for i, depth in enumerate(depths):
    model = DecisionTreeRegressor(max_depth=depth, random_state=42)
    model.fit(X, y)
    
    # 生成测试点
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_pred = model.predict(X_test)
    
    plt.subplot(1, 3, i+1)
    plt.scatter(X, y, s=20, edgecolor='black', c='darkorange', label='训练数据')
    plt.plot(X_test, y_pred, color='cornflowerblue', linewidth=2, label='模型预测')
    plt.plot(X_test, np.sin(X_test).ravel(), '--', color='gray', alpha=0.5, label='真实规律')
    plt.title(titles[i], fontsize=14)
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()

plt.tight_layout()
plt.show()
```

### 四、课后作业

1. 制作一张"算法选择速查表"（手绘或 PPT），包含每个算法的：名称、一句话原理、一个适用场景、一个注意事项
2. 思考：如果要做一个"预测学生期末考试成绩"的系统，你会选择什么算法？为什么？
3. 用自己的话解释"过拟合"是什么意思，举一个生活中的例子

---

## 第3课：第一个 AI 模型

### 一、学习目标

- 能够用 Scikit-learn 完成一个完整的 ML 项目
- 掌握模型训练、评估、调参的基本流程
- 完成鸢尾花分类实战项目

### 二、核心知识点

#### 2.1 Scikit-learn 统一 API

Scikit-learn 最强大的地方在于：**所有模型都用同一套 API**！

```python
# 统一的模式
model = SomeModel()          # 1. 创建模型
model.fit(X_train, y_train)  # 2. 训练
predictions = model.predict(X_test)  # 3. 预测
score = model.score(X_test, y_test)  # 4. 评估
```

#### 2.2 模型评估指标

| 指标 | 含义 | 什么时候用 |
|------|------|-----------|
| **准确率 (Accuracy)** | 预测正确的比例 | 各类别数量均衡时 |
| **精确率 (Precision)** | 预测为"正"的里面真"正"的比例 | 假阳性代价高（如垃圾邮件误判） |
| **召回率 (Recall)** | 真的"正"里面被找出来的比例 | 假阴性代价高（如癌症筛查） |
| **F1-Score** | 精确率和召回率的调和平均 | 需要两者兼顾时 |
| **混淆矩阵** | 详细展示各类别的预测结果 | 需要分析具体错误类型时 |

#### 2.3 交叉验证

```
将数据分成5份：
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┴───┘

第1轮：用[2,3,4,5]训练，用[1]验证 → 得分s1
第2轮：用[1,3,4,5]训练，用[2]验证 → 得分s2
第3轮：用[1,2,4,5]训练，用[3]验证 → 得分s3
第4轮：用[1,2,3,5]训练，用[4]验证 → 得分s4
第5轮：用[1,2,3,4]训练，用[5]验证 → 得分s5

最终得分 = (s1+s2+s3+s4+s5)/5  ← 更可靠的评估
```

### 三、实操环节（60分钟）

#### 实操 3.1：鸢尾花分类完整流程（40分钟）

这是本周最重要的实操练习，跟着一步一步做。

```python
# ============================================
# 鸢尾花分类：完整机器学习项目流程
# ============================================

# --- 第1步：导入库 ---
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# --- 第2步：加载并探索数据 ---
iris = load_iris()
X = iris.data
y = iris.target

print("=" * 50)
print("       鸢尾花分类项目")
print("=" * 50)
print(f"\n📊 数据集信息：")
print(f"  样本数：{X.shape[0]}")
print(f"  特征数：{X.shape[1]}")
print(f"  特征：{iris.feature_names}")
print(f"  类别：{list(iris.target_names)}")
print(f"  各类样本数：{np.bincount(y)}")

# 数据探索
df = pd.DataFrame(X, columns=iris.feature_names)
df['类别'] = [iris.target_names[i] for i in y]

print(f"\n📈 统计描述：")
print(df.describe().round(2))

# 数据可视化
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

for i, feature in enumerate(iris.feature_names):
    ax = axes[i//2, i%2]
    for j, target_name in enumerate(iris.target_names):
        subset = df[df['类别'] == target_name]
        ax.hist(subset[feature], alpha=0.6, label=target_name, 
                color=colors[j], bins=15, edgecolor='white')
    ax.set_title(f'{feature} 分布', fontsize=12)
    ax.legend()
    ax.set_xlabel(feature)

plt.suptitle('鸢尾花数据集特征分布', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# --- 第3步：数据预处理 ---
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📦 数据划分：")
print(f"  训练集：{X_train.shape[0]} 个样本")
print(f"  测试集：{X_test.shape[0]} 个样本")
print(f"  训练集各类分布：{np.bincount(y_train)}")
print(f"  测试集各类分布：{np.bincount(y_test)}")

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n✓ 标准化完成")

# --- 第4步：训练多个模型并对比 ---
models = {
    "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
    "决策树": DecisionTreeClassifier(max_depth=4, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42)
}

print(f"\n🤖 模型训练与评估：")
print("-" * 60)
print(f"{'模型':<12} {'训练准确率':<12} {'测试准确率':<12} {'5折交叉验证':<12}")
print("-" * 60)

best_model = None
best_score = 0

for name, model in models.items():
    # 训练
    model.fit(X_train_scaled, y_train)
    # 评估
    train_acc = model.score(X_train_scaled, y_train)
    test_acc = model.score(X_test_scaled, y_test)
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    cv_mean = cv_scores.mean()
    
    print(f"{name:<12} {train_acc:<12.3f} {test_acc:<12.3f} {cv_mean:<12.3f}")
    
    if test_acc > best_score:
        best_score = test_acc
        best_model = (name, model)

print("-" * 60)
print(f"\n🏆 最佳模型：{best_model[0]}（测试准确率：{best_score:.3f}）")

# --- 第5步：详细评估最佳模型 ---
model = best_model[1]
y_pred = model.predict(X_test_scaled)

print(f"\n📋 分类报告：")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 混淆矩阵
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris.target_names,
            yticklabels=iris.target_names)
plt.title(f'混淆矩阵 — {best_model[0]}', fontsize=14)
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.show()

# --- 第6步：超参数调优（GridSearchCV） ---
print(f"\n🔧 超参数调优...")

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7, None],
    'min_samples_split': [2, 5, 10]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
grid_search.fit(X_train_scaled, y_train)

print(f"  最佳参数：{grid_search.best_params_}")
print(f"  最佳交叉验证得分：{grid_search.best_score_:.3f}")

# 用最优模型评估
best_rf = grid_search.best_estimator_
test_acc_tuned = best_rf.score(X_test_scaled, y_test)
print(f"  调优后测试准确率：{test_acc_tuned:.3f}")
print(f"  相比调优前提升：{(test_acc_tuned - best_score):.3f}")

# --- 第7步：预测新样本 ---
print(f"\n🔮 预测新样本：")
# 模拟3个新的鸢尾花样本
new_samples = np.array([
    [5.1, 3.5, 1.4, 0.2],  # 应该属于 setosa
    [6.3, 3.3, 6.0, 2.5],  # 应该属于 virginica
    [5.5, 2.6, 4.4, 1.2],  # 应该属于 versicolor
])

new_scaled = scaler.transform(new_samples)
predictions = best_rf.predict(new_scaled)
probabilities = best_rf.predict_proba(new_scaled)

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    pred_class = iris.target_names[pred]
    print(f"  样本{i+1}: 预测为 {pred_class}")
    for j, class_name in enumerate(iris.target_names):
        print(f"    {class_name}: {prob[j]:.3f}")

# --- 第8步：项目总结 ---
print(f"\n{'='*50}")
print(f"              项目总结")
print(f"{'='*50}")
print(f"""
✅ 完成了一个完整的机器学习项目流程：
  1. 数据加载与探索
  2. 数据可视化分析
  3. 数据预处理（划分+标准化）
  4. 多模型对比训练
  5. 交叉验证评估
  6. 超参数调优
  7. 新样本预测

📊 最佳模型：{best_model[0]}（调优后）
📈 测试准确率：{test_acc_tuned:.3f}
""")
```

#### 实操 3.2：模型解释（20分钟）

```python
# 查看随机森林中每个特征的重要性
importances = best_rf.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 5))
plt.bar(range(len(importances)), importances[indices], 
        color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
plt.xticks(range(len(importances)), 
           [iris.feature_names[i] for i in indices])
plt.title('特征重要性排名', fontsize=14)
plt.ylabel('重要性得分')
plt.tight_layout()
plt.show()

print("特征重要性排名：")
for i in indices:
    print(f"  {iris.feature_names[i]}: {importances[i]:.4f}")
print("\n💡 这说明：花瓣长度和宽度是区分鸢尾花种类最重要的特征")
```

### 四、课后作业（第3周综合）

> 🎯 **本周大作业**：完成一个分类模型训练
>
> **任务**（二选一）：
>
> **选项A — 红酒品质分类**：
> 使用 Scikit-learn 自带的 wine 数据集，完成与本节课类似的完整流程
>
> **选项B — 自选数据集**：
> 从 [Kaggle](https://www.kaggle.com/datasets) 或 [UCI ML Repository](https://archive.ics.uci.edu/) 找一个感兴趣的数据集，完成一个分类项目
>
> **要求**：
> 1. 至少尝试 2 种不同的模型
> 2. 包含数据探索、预处理、训练、评估全流程
> 3. 有至少 3 种可视化图表
> 4. 写 500 字的项目报告

---

# 第4周：深度学习基础

---

## 第1课：神经网络

### 一、学习目标

- 理解神经元和感知机的概念
- 理解多层神经网络（MLP）的结构
- 理解激活函数、损失函数、优化器的作用
- 不要求数学推导，重点是建立直觉

### 二、核心知识点

#### 2.1 从生物神经元到人工神经元

```
生物神经元                          人工神经元
─────────                         ─────────
   树突                              输入 x₁, x₂, x₃
    ↓                                  ↓
   细胞体  ──→ 轴突         ≈       加权求和  ──→ 激活函数 ──→ 输出
                                          
核心思想：接收多个输入 → 处理 → 产生一个输出
```

**数学表达（不需要记公式，理解含义即可）**：

```
y = f(w₁x₁ + w₂x₂ + w₃x₃ + b)

x₁, x₂, x₃：输入（特征）
w₁, w₂, w₃：权重（每个输入的重要性）
b：偏置（调整输出阈值）
f：激活函数（决定要不要"激活"这个神经元）
y：输出
```

#### 2.2 感知机 → 多层神经网络（MLP）

```
感知机（单层）：
  [输入层] ──→ [输出层]
  只能解决线性可分的问题（如AND、OR）
  解决不了 XOR 问题

多层神经网络（MLP）：
  [输入层] ──→ [隐藏层1] ──→ [隐藏层2] ──→ [输出层]
  可以解决非线性问题
  隐藏层越多 → 能学到越复杂的模式
  
  这就是"深度学习"的"深"——层数多！
```

#### 2.3 激活函数 — 为什么需要它？

> 如果没有激活函数，多层网络等于一层网络（因为线性变换的组合还是线性变换）

| 激活函数 | 形状 | 特点 | 使用场景 |
|----------|------|------|----------|
| **Sigmoid** | S 形曲线 | 输出 0-1，适合做概率 | 二分类输出层 |
| **ReLU** | 有输入就输出，没输入就是 0 | 简单、效果好、最常用 | 隐藏层首选 |
| **Softmax** | 多个输出加起来等于 1 | 多分类输出层 | 多分类问题 |

#### 2.4 损失函数 — 衡量模型"有多差"

> 训练的目标就是**最小化损失函数**

| 损失函数 | 用途 | 说明 |
|----------|------|------|
| **均方误差 (MSE)** | 回归 | 预测值和真实值差值的平方的平均 |
| **交叉熵 (Cross Entropy)** | 分类 | 衡量预测概率分布和真实分布的差异 |

**生活类比**：损失函数就像考试分数 —— 分数越低越好？不对，应该是**扣分越少越好**！损失函数的值就是在"扣分"。

#### 2.5 优化器 — 如何让模型"进步"

| 优化器 | 特点 |
|--------|------|
| **SGD** | 最基础，每次用一部分数据计算梯度，沿梯度反方向更新参数 |
| **Adam** | 目前最常用，自适应调整学习率，收敛快 |
| **AdamW** | Adam 的改进版，大模型训练首选 |

**生活类比**：
- 损失函数 = 你距离山脚还很远（目标：到山脚，即损失最小）
- 梯度 = 当前位置最陡峭的下山方向
- 学习率 = 每一步迈多大
- 优化器 = 下山策略（小碎步？大跨步？自适应步长？）

#### 2.6 神经网络工作流程

```
对于每个训练循环：
  1. 前向传播：输入 → 网络各层 → 输出预测值
  2. 计算损失：对比预测值与真实标签
  3. 反向传播：计算梯度，知道每个参数该调多少
  4. 更新参数：优化器根据梯度调整权重
  5. 重复 1-4，直到损失足够小
```

### 三、实操环节（60分钟）

#### 实操 3.1：TensorFlow Playground 交互（15分钟）

访问 [https://playground.tensorflow.org](https://playground.tensorflow.org)，做以下实验：

1. 选择最复杂的螺旋数据集（spiral）
2. 只用 1 个隐藏层、2 个神经元 → 观察效果很差
3. 逐步增加隐藏层和神经元 → 观察效果变好
4. 改变激活函数（ReLU/Sigmoid/Tanh）→ 观察不同效果
5. 改变学习率 → 观察收敛速度

#### 实操 3.2：用 Keras 搭建第一个神经网络（25分钟）

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 注意：需要先安装 TensorFlow
# pip install tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 生成"月亮"数据集（两个半月形的分类问题）
X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 可视化数据
plt.figure(figsize=(6, 5))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.6, edgecolors='k')
plt.title('月亮数据集（需要非线性分类器）')
plt.xlabel('特征 1')
plt.ylabel('特征 2')
plt.show()

# 搭建神经网络
model = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(2,), name='hidden1'),
    layers.Dense(8, activation='relu', name='hidden2'),
    layers.Dense(1, activation='sigmoid', name='output')
])

# 查看模型结构
model.summary()

# 编译模型
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 训练
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# 可视化训练过程
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(history.history['loss'], label='训练损失')
axes[0].plot(history.history['val_loss'], label='验证损失')
axes[0].set_title('损失曲线')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(history.history['accuracy'], label='训练准确率')
axes[1].plot(history.history['val_accuracy'], label='验证准确率')
axes[1].set_title('准确率曲线')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 评估
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"测试集准确率：{test_acc:.3f}")

# 可视化决策边界
def plot_decision_boundary(model, X, y):
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()], verbose=0)
    Z = (Z > 0.5).astype(int).reshape(xx.shape)
    
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.8, edgecolors='k')
    plt.title('神经网络分类决策边界')
    plt.xlabel('特征 1')
    plt.ylabel('特征 2')
    plt.show()

plot_decision_boundary(model, X_test, y_test)
```

#### 实操 3.3：修改网络结构实验（20分钟）

在前面的代码基础上做以下实验，记录每次修改后测试集准确率的变化：

| 实验 | 修改内容 | 测试准确率 |
|------|----------|-----------|
| 实验1 | 只用一个隐藏层（2个神经元） | ____ |
| 实验2 | 隐藏层用 64 个神经元 | ____ |
| 实验3 | 再加一层（3个隐藏层） | ____ |
| 实验4 | 激活函数换成 sigmoid | ____ |
| 实验5 | 优化器换成 SGD | ____ |

### 四、课后作业

1. 用自己的话解释：激活函数是做什么的？为什么需要它？
2. 用 Keras 在鸢尾花数据集上训练一个神经网络分类器，对比第3周的随机森林结果
3. 阅读：TensorFlow 官方入门教程（前3节）

---

## 第2课：卷积神经网络（CNN）

### 一、学习目标

- 理解卷积为什么适合处理图像
- 理解 CNN 的核心组件：卷积层、池化层、全连接层
- 完成猫狗图像分类实践

### 二、核心知识点

#### 2.1 为什么不能用普通神经网络处理图像？

一张 224×224 的彩色图像：
- 有 224 × 224 × 3 = 150,528 个像素（输入特征）
- 如果用全连接层（1000个神经元），参数数量 = 150,528 × 1000 = **1.5亿个参数**！
- 参数太多 → 容易过拟合、训练太慢

**卷积的妙处**：用一个小窗口（如3×3）在图像上滑动，**共享参数**，大幅减少参数量。

#### 2.2 CNN 核心组件

```
输入图像 → [卷积层 → 池化层] × N → 全连接层 → 输出
```

**卷积层（Convolutional Layer）**：
- 用一个小"滤镜"（卷积核）扫描图像
- 不同滤镜检测不同特征：边缘、纹理、颜色、形状
- 浅层检测简单特征（边缘），深层检测复杂特征（人脸、物体）

```
生活类比：用一个放大镜在图像上逐步扫描，
每扫过一个区域就记录"这个区域有什么特征"
```

**池化层（Pooling Layer）**：
- 缩小特征图尺寸，减少计算量
- 最常用"最大池化"：在每个小区域取最大值
- 让模型对位置变化更鲁棒

**全连接层（Fully Connected Layer）**：
- 在卷积和池化提取完特征之后
- 用提取到的特征做最终分类

#### 2.3 为什么 CNN 有效？

1. **局部连接**：每个神经元只看一小块区域，不是全图
2. **参数共享**：同一个滤镜的权重在全图上复用
3. **层次化特征**：自动学习从低级到高级的视觉特征

### 三、实操环节（60分钟）

> ⚠️ **说明**：由于猫狗分类训练需要较长时间（即使 GPU 也需要几十分钟），本节课的实操重点放在理解和体验上。完整训练可以在课后完成。

#### 实操 3.1：用预训练模型体验图像分类（20分钟）

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# 加载预训练的 MobileNetV2 模型（在 ImageNet 上训练好的）
model = MobileNetV2(weights='imagenet')
print("✓ 预训练模型加载完成")

# 准备一张测试图片
# 方法1：用在线图片
image_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/320px-Felis_catus-cat_on_snow.jpg"
img_path = keras.utils.get_file('cat.jpg', image_url)

# 方法2：如果你有自己的图片，替换下面的路径
# img_path = "your_image.jpg"

# 加载并预处理图片
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)  # 加batch维度
img_array = preprocess_input(img_array)

# 预测
predictions = model.predict(img_array, verbose=0)
results = decode_predictions(predictions, top=5)[0]

# 显示结果
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title('输入图片')
plt.axis('off')

plt.subplot(1, 2, 2)
labels = [r[1] for r in results][::-1]
scores = [r[2] for r in results][::-1]
colors = plt.cm.Blues_r([s*0.8 for s in scores])
plt.barh(labels, scores, color=colors)
plt.title('Top 5 预测结果')
plt.xlabel('置信度')

plt.tight_layout()
plt.show()

for i, (imagenet_id, label, score) in enumerate(results):
    print(f"{i+1}. {label:<20} 置信度：{score:.3f}")
```

#### 实操 3.2：搭建一个简单的 CNN（25分钟）

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 加载 CIFAR-10 数据集（10种物品的小图，32×32像素）
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# 归一化
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 类别名称
class_names = ['飞机', '汽车', '鸟', '猫', '鹿', 
               '狗', '青蛙', '马', '船', '卡车']

print(f"训练集：{x_train.shape[0]} 张，尺寸 {x_train.shape[1]}×{x_train.shape[2]}")
print(f"测试集：{x_test.shape[0]} 张")

# 展示几张样本图
plt.figure(figsize=(12, 5))
for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]], fontsize=10)
    plt.axis('off')
plt.suptitle('CIFAR-10 样本')
plt.show()

# 搭建 CNN 模型
model = keras.Sequential([
    # 第1个卷积块
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', 
                  input_shape=(32, 32, 3)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # 第2个卷积块
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # 第3个卷积块
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # 全连接分类层
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.summary()

# 编译
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 训练（注意：为节省课堂时间，只训练10个epoch）
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# 评估
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n测试集准确率：{test_acc:.3f}")

# 可视化训练过程
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history.history['loss'], label='训练损失')
axes[0].plot(history.history['val_loss'], label='验证损失')
axes[0].set_title('损失曲线')
axes[0].set_xlabel('Epoch')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(history.history['accuracy'], label='训练准确率')
axes[1].plot(history.history['val_accuracy'], label='验证准确率')
axes[1].set_title('准确率曲线')
axes[1].set_xlabel('Epoch')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

#### 实操 3.3：预测结果可视化（15分钟）

```python
# 对测试集做一些预测并可视化
predictions = model.predict(x_test[:10], verbose=0)
pred_classes = predictions.argmax(axis=1)

plt.figure(figsize=(14, 6))
for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.imshow(x_test[i])
    true_label = class_names[y_test[i][0]]
    pred_label = class_names[pred_classes[i]]
    color = 'green' if true_label == pred_label else 'red'
    plt.title(f'真实:{true_label}\n预测:{pred_label}', 
              color=color, fontsize=9)
    plt.axis('off')
plt.suptitle('模型预测结果（绿色=正确，红色=错误）')
plt.tight_layout()
plt.show()
```

### 四、课后作业

1. 用自己的话解释：CNN 的"卷积"是什么？为什么它比全连接更适合处理图像？
2. 课后继续训练 CNN 模型，增加 epoch 到 30，观察准确率变化
3. 找一个预训练模型（如 ResNet50），在你自己的图片上测试分类效果

---

## 第3课：Transformer

### 一、学习目标

- 理解 Attention 机制的核心思想
- 理解 Transformer 的架构
- 理解为什么 GPT 如此强大
- **不要求数学推导，重点是理解直觉**

### 二、核心知识点

#### 2.1 从 RNN 到 Transformer

```
RNN（循环神经网络）：
  词1 → 词2 → 词3 → 词4
  必须按顺序处理，不能并行
  长句子时"记不住"前面的内容

Transformer：
  词1 ─┐
  词2 ─┼→ 同时处理所有词（可以并行！）
  词3 ─┤  每个词都能"关注"其他所有词
  词4 ─┘
```

#### 2.2 Attention（注意力）— "Attention Is All You Need"

> 这是 2017 年 Google 那篇改变一切的论文的标题，字面意思就是"你只需要注意力"

**生活类比：读一句话时的注意力**

```
"那只在花园里追着蝴蝶跑的黑色的猫很可爱"

当你在理解这句话时：
- 看到"猫"这个词时，你的注意力会回溯到"黑色的"
- 看到"追着"时，你的注意力会关联"蝴蝶"和"猫"
- 你自动建立了词与词之间的关系

这就是 Self-Attention 在做的事情！
```

**Attention 的核心公式（理解含义即可）**：

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V

Q (Query)：我要找什么？
K (Key)：我有什么？
V (Value)：实际内容是什么？

类比图书馆：
  Q = 你想找什么书？（"深度学习入门"）
  K = 每本书的标签
  V = 每本书的内容
  Attention = 根据你的需求(Q)，匹配标签(K)，拿到最相关的书的内容(V)
```

#### 2.3 Transformer 架构

```
           Transformer
        ┌───────┴───────┐
      编码器 (Encoder)   解码器 (Decoder)
      ┌───┴───┐         ┌───┴───┐
    理解输入            生成输出
    (BERT用这个)       (GPT用这个)
    
编码器/解码器各自包含：
  · Multi-Head Self-Attention（多个注意力头并行）
  · Feed Forward Network（前馈网络）
  · Layer Normalization（层归一化）
  · Residual Connection（残差连接）
```

#### 2.4 为什么 GPT 如此强大？

```
1. Transformer 架构
   → 能并行处理，能处理长文本，能捕捉复杂关系

2. 海量数据训练
   → GPT-3：45TB 文本数据
   → 几乎读完了整个互联网的公开文本

3. 自回归生成
   → 一个字一个字地"续写"
   → 训练目标就是"预测下一个词"
   → 这个简单的目标催生了强大的能力

4. 规模化效应（Scaling Law）
   → 模型越大、数据越多、算力越强 → 能力越强
   → GPT-1：1.17亿参数
   → GPT-2：15亿参数
   → GPT-3：1750亿参数
   → GPT-4：据传1.76万亿参数
```

#### 2.5 GPT 的训练 vs 使用

```
训练阶段（Pre-training）：
  "今天我去了超市买了一些___"
  → GPT 预测下一个词："水果"
  → 对比正确答案："食物"
  → 更新参数，下次更准
  → 重复这个过程几千亿次！

使用阶段（Inference）：
  你："请写一首关于春天的诗"
  → GPT 一个字一个字地生成：
  "春" → "风" → "拂" → "过" → ...
  → 直到生成完整的诗
```

### 三、实操环节（60分钟）

#### 实操 3.1：可视化 Transformer（20分钟）

在浏览器中打开以下工具，直观感受 Transformer 的工作方式：

1. **The Illustrated Transformer**（强烈推荐！）：
   [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
   - 有中文翻译版，自行搜索即可
   
2. **Transformer Explainer**：
   搜索 "Transformer Explainer Georgia Tech" — 交互式可视化 Transformer 内部机制

3. **BERTViz**：
   [https://github.com/jessevig/bertviz](https://github.com/jessevig/bertviz)
   - 可视化 Attention 权重，看模型在"关注"什么

#### 实操 3.2：用 GPT 模型生成文本（25分钟）

```python
# 使用 Hugging Face Transformers 库
# 安装：pip install transformers torch

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

print("=" * 50)
print("  体验 Transformer 的文本生成能力")
print("=" * 50)

# 方法1：使用 pipeline（最简单）
print("\n--- 方法1：pipeline 方式 ---")

# 中文模型：使用一个小的中文 GPT 模型
generator = pipeline(
    'text-generation',
    model='uer/gpt2-chinese-cluecorpussmall',
    max_length=100
)

prompt = "人工智能的未来发展"
result = generator(prompt, num_return_sequences=1)
print(f"输入：{prompt}")
print(f"输出：{result[0]['generated_text']}")

# 方法2：更灵活的方式
print("\n--- 方法2：自定义生成参数 ---")
tokenizer = AutoTokenizer.from_pretrained('uer/gpt2-chinese-cluecorpussmall')
model = AutoModelForCausalLM.from_pretrained('uer/gpt2-chinese-cluecorpussmall')

inputs = tokenizer("今天天气真好，我想", return_tensors='pt')

# 不同生成策略对比
outputs_greedy = model.generate(
    **inputs, max_length=50, do_sample=False
)
outputs_sample = model.generate(
    **inputs, max_length=50, do_sample=True, temperature=0.8
)

print("贪心解码（确定性）：", tokenizer.decode(outputs_greedy[0], skip_special_tokens=True))
print("随机采样（有创意）：", tokenizer.decode(outputs_sample[0], skip_special_tokens=True))
```

#### 实操 3.3：Attention 机制直观演示（15分钟）

```python
import numpy as np
import matplotlib.pyplot as plt

# 模拟 Self-Attention 的直观效果
# 一段中文句子，模拟每个词对其他词的"注意力"

sentence = ["我", "喜欢", "吃", "苹果", "因为", "它", "很", "甜"]

# 模拟一个随机的注意力矩阵（实际中是通过训练学习得到的）
np.random.seed(42)
attention_weights = np.random.rand(len(sentence), len(sentence))
# 让对角线附近的权重更高（词更关注邻近的词）
for i in range(len(sentence)):
    for j in range(len(sentence)):
        attention_weights[i][j] *= np.exp(-abs(i-j) / 2)

# 归一化（每行的和等于1）
attention_weights = attention_weights / attention_weights.sum(axis=1, keepdims=True)

# 可视化
plt.figure(figsize=(10, 8))
plt.imshow(attention_weights, cmap='YlOrRd')

# 标注
plt.xticks(range(len(sentence)), sentence, fontsize=12)
plt.yticks(range(len(sentence)), sentence, fontsize=12)
plt.xlabel('被关注的词（Key）', fontsize=13)
plt.ylabel('发出注意力的词（Query）', fontsize=13)
plt.title('Self-Attention 热力图模拟\n颜色越深 = 注意力越强', fontsize=15)

# 添加数值标注
for i in range(len(sentence)):
    for j in range(len(sentence)):
        if attention_weights[i][j] > 0.15:
            plt.text(j, i, f'{attention_weights[i][j]:.2f}', 
                    ha='center', va='center', fontsize=9)

plt.tight_layout()
plt.show()

print("💡 解释：")
print("  - 每个词都会"关注"句子中的所有词（包括自己）")
print("  - 颜色越深表示这个"键"对当前"查询"越重要")
print("  - 真实的 Transformer 会并行使用多个"注意力头"")
print("  - 每个头可能关注不同的模式（语法、语义、位置等）")
```

### 四、课后作业（第4周综合）

> 🎯 **本周大作业**：图像分类实践
>
> **任务**（二选一）：
>
> **选项A — 猫狗分类**：
> 从 Kaggle 下载猫狗数据集，用 CNN 完成分类，目标准确率 > 85%
>
> **选项B — 手写数字识别**：
> 用 MNIST 数据集训练 CNN，目标准确率 > 99%
>
> **要求**：
> 1. 使用 CNN 模型（不能用纯全连接）
> 2. 包含数据增强（旋转、翻转、缩放等）
> 3. 绘制训练曲线和混淆矩阵
> 4. 写一份实验报告，记录模型结构、训练参数和最终效果

---

# 第5周：大模型（LLM）

---

## 第1课：GPT 工作原理

### 一、学习目标

- 理解 Token、Embedding 的概念
- 理解 GPT 的 Decoder-only 架构
- 理解 ChatGPT 为什么能对话
- 了解 LLM 的局限性

### 二、核心知识点

#### 2.1 Token — LLM 的"最小单位"

> Token ≠ 单词！一个 Token 可能是一个字、一个词或一个字符片段。

```
英文：
  "I love AI" → ["I", " love", " AI"] → 3个Tokens
  "Unbelievable" → ["Un", "bel", "iev", "able"] → 4个Tokens

中文：
  "我爱人工智能" → ["我", "爱", "人工", "智能"] → 4个Tokens

经验法则：
  · 英文：1 Token ≈ 0.75 个单词
  · 中文：1 Token ≈ 1.5-2 个汉字
  · 1000 Tokens ≈ 750 英文单词 ≈ 1500-2000 汉字
```

**为什么要了解 Token？**
- 模型收费按 Token 计费
- 模型有上下文窗口限制（如 128K Tokens）
- 不同语言的"Token 效率"不同

#### 2.2 Embedding — 把文字变成数字

```
每个 Token 被转换成一个高维向量（一串数字）

"猫" → [0.23, -0.45, 0.78, ..., 0.12]  (通常几百到几千维)
"狗" → [0.19, -0.42, 0.75, ..., 0.15]

猫和狗的词向量很接近（因为它们语义相似）
"猫"和"汽车"的词向量距离很远

Embedding 的神奇之处：
  国王 - 男人 + 女人 ≈ 女王
  (语义运算在向量空间中是成立的！)
```

#### 2.3 GPT 架构：Decoder-only Transformer

```
BERT 架构（Encoder-only）：     GPT 架构（Decoder-only）：
  适合"理解"任务                  适合"生成"任务
  · 文本分类                      · 文本生成
  · 情感分析                      · 对话聊天
  · 命名实体识别                  · 代码补全
  · 阅读理解                      · 创意写作
         ↓                              ↓
   双向看上下文                    单向看上文（因果注意力）
   Masked LM                      自回归生成
```

**GPT 生成过程**：
```
输入："今天天气"
  ↓
模型预测下一个Token："真"（概率最高）
  ↓
输入变为："今天天气真"
  ↓
模型预测下一个Token："好"（概率最高）
  ↓
...如此循环，直到输出结束标记
```

#### 2.4 ChatGPT 为什么能对话？

```
ChatGPT = GPT + 以下训练步骤：

Step 1: 预训练（Pre-training）
  · 在海量互联网文本上学习"续写"能力
  · 学到了语言、知识、推理能力
  · 但它只会"续写"，不会"回答问题"

Step 2: 监督微调（SFT — Supervised Fine-Tuning）
  · 人工写高质量"问答对"来训练
  · 教模型：当用户问X时，你应该回答Y
  · 学会了"对话"的形式

Step 3: RLHF（基于人类反馈的强化学习）
  · 对同一个问题生成多个回答
  · 让人类标注员给这些回答打分
  · 训练一个"奖励模型"
  · 用强化学习让模型倾向生成高分回答
  · 学会了"有用、安全、礼貌"的回答方式
```

#### 2.5 LLM 的局限性

| 局限 | 说明 | 应对方式 |
|------|------|----------|
| **幻觉** | 会自信地说出不存在的事实 | 要求引用来源、交叉验证 |
| **知识截止** | 不知道训练数据之后发生的事 | 结合 RAG、联网搜索 |
| **上下文窗口** | 一次对话有字数上限 | 分段处理、摘要浓缩 |
| **偏见** | 训练数据中的偏见会被学到 | 审慎对待敏感话题 |
| **数学差** | 本质是语言模型，不擅长精确计算 | 让 AI 写代码来计算 |
| **成本** | API 调用需要付费 | 选择合适的模型级别 |

### 三、实操环节（60分钟）

#### 实操 3.1：Token 化体验（15分钟）

访问 OpenAI Tokenizer 页面：
[https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer)

在页面中输入不同的文本，观察：
- 中文和英文的 Token 数量差异
- 同一个词在不同语境下可能被分成不同的 Token
- 特殊符号和换行符如何被 Token 化

#### 实操 3.2：Embedding 可视化（20分钟）

```python
# 需要安装：pip install openai numpy matplotlib scikit-learn
# 需要 OpenAI API Key

from openai import OpenAI
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 配置 API 密钥
# 注意：运行前需要设置环境变量 OPENAI_API_KEY
# 或者在代码中直接设置（不推荐用于生产环境）
client = OpenAI()  # 自动读取 OPENAI_API_KEY 环境变量

# 一组需要计算 Embedding 的文本
texts = [
    "猫是一种可爱的宠物",
    "狗是人类忠实的朋友", 
    "我喜欢吃苹果和香蕉",
    "水果富含维生素和纤维",
    "汽车是一种交通工具",
    "飞机是最快的旅行方式",
    "Python是一种编程语言",
    "JavaScript是前端开发语言",
    "今天天气真好适合出去玩",
    "阳光明媚是郊游的好日子",
]

def get_embedding(text, model="text-embedding-3-small"):
    """获取文本的 Embedding 向量"""
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

print("正在获取 Embedding...")
embeddings = []
for text in texts:
    emb = get_embedding(text)
    embeddings.append(emb)
    print(f"  ✓ {text} → {len(emb)}维向量")

# 用 PCA 降到 2 维可视化
embeddings_array = np.array(embeddings)
pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings_array)

# 绘制
plt.figure(figsize=(10, 8))
categories = ['动物', '动物', '水果', '水果', '交通', '交通', 
              '编程', '编程', '天气', '天气']
colors = {'动物': '#FF6B6B', '水果': '#4ECDC4', '交通': '#45B7D1', 
          '编程': '#F39C12', '天气': '#2ECC71'}

for i, (text, cat) in enumerate(zip(texts, categories)):
    x, y = reduced[i]
    plt.scatter(x, y, color=colors[cat], s=200, alpha=0.7, edgecolors='black')
    plt.annotate(text[:8]+'...' if len(text) > 8 else text, 
                (x, y), textcoords="offset points", xytext=(0, 15),
                ha='center', fontsize=10)

plt.title('文本 Embedding 的 2D 可视化\n(语义接近的文本在空间中更接近)', fontsize=14)
plt.grid(True, alpha=0.2)
plt.show()

print("\n💡 观察结论：")
print("  - 语义相似的文本（如'猫'和'狗'）在空间中靠得更近")
print("  - 不同主题的文本自然分离")
print("  - Embedding 可以用于搜索、聚类、推荐等任务")
```

#### 实操 3.3：LLM 幻觉体验（10分钟）

在 ChatGPT/Claude 中尝试以下问题，观察幻觉现象：

1. "请介绍一下'黄河大学'的历史和优势专业"（这个大学不存在）
2. "列出2027年奥斯卡最佳影片的提名名单"（未来的事）
3. "请给我一个具体的人物传记，他发明了永动机"（不可能的事）

记录 AI 的回答，思考：如何识别和防范 AI 幻觉？

### 四、课后作业

1. 用自己的话解释 Token 和 Embedding 的区别
2. 用 Tokenizer 工具分析一段中文和一段英文的 Token 数量和规律
3. 思考：在什么场景下，AI 幻觉会带来严重后果？如何预防？

---

## 第2课：LLM API 调用

### 一、学习目标

- 掌握 OpenAI API 的基本调用方法
- 理解 Function Calling（函数调用）
- 理解 Structured Output（结构化输出）
- 完成智能问答系统的 API 调用

### 二、核心知识点

#### 2.1 API 调用基本流程

```python
# 最基本的 API 调用模式
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4o-mini",  # 选择模型
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "你好，请介绍你自己"}
    ],
    temperature=0.7,  # 控制随机性
    max_tokens=500     # 限制输出长度
)

# 获取回复
answer = response.choices[0].message.content
```

**三个角色的区别**：

| Role | 用途 | 示例 |
|------|------|------|
| **system** | 设定 AI 的行为和角色 | "你是一位专业的数据分析师" |
| **user** | 用户的消息 | "帮我分析这份销售数据" |
| **assistant** | AI 的历史回答（用于多轮对话） | "好的，请提供数据..." |

#### 2.2 Function Calling — 让模型调用工具

> 这是 Agent 开发的基础！让模型不仅"会说"，还能"会做"。

```
普通对话：
  用户："今天北京天气怎么样？"
  AI："抱歉，我无法获取实时天气信息..."

有了 Function Calling：
  用户："今天北京天气怎么样？"
  AI：[调用 get_weather 函数]
  系统：执行 get_weather("北京") → 返回 {"temp": 25, "weather": "晴"}
  AI："今天北京天气晴朗，温度25°C..."
```

```python
# Function Calling 示例
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "今天北京天气怎么样？"}],
    tools=functions
)

# 模型返回的不是文本，而是函数调用
tool_call = response.choices[0].message.tool_calls[0]
print(f"模型想调用：{tool_call.function.name}")
print(f"参数：{tool_call.function.arguments}")
```

#### 2.3 Structured Output — 让模型输出结构化的格式

```python
# 让模型输出固定格式的 JSON
from pydantic import BaseModel

class ProductReview(BaseModel):
    product_name: str
    rating: int  # 1-5
    pros: list[str]
    cons: list[str]
    summary: str

response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "评价一下iPhone 16的使用体验"}
    ],
    response_format=ProductReview
)

review = response.choices[0].message.parsed
print(f"产品：{review.product_name}")
print(f"评分：{review.rating}/5")
print(f"优点：{', '.join(review.pros)}")
print(f"缺点：{', '.join(review.cons)}")
```

### 三、实操环节（60分钟）

#### 实操 3.1：基础 API 调用（20分钟）

```python
# 完整示例：多轮对话助手
from openai import OpenAI
import os

# 初始化客户端
# 方式1：用 OpenAI
# client = OpenAI(api_key="sk-xxx")

# 方式2：用 DeepSeek（性价比更高，国内直连）
client = OpenAI(
    api_key="your-deepseek-api-key",  # 替换为你的 Key
    base_url="https://api.deepseek.com"
)

# 方式3：用通义千问
# client = OpenAI(
#     api_key="your-qwen-api-key",
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

class ChatBot:
    """简单的多轮对话机器人"""
    
    def __init__(self, system_prompt="你是一个有帮助的AI助手"):
        self.client = client
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
    
    def chat(self, user_input):
        """发送消息并获取回复"""
        self.messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        
        # 打印 token 使用情况
        usage = response.usage
        print(f"[本次消耗：{usage.total_tokens} tokens | "
              f"输入{usage.prompt_tokens} + 输出{usage.completion_tokens}]")
        
        return reply

# 使用
bot = ChatBot("你是一位AI学习导师，帮助学生学习编程和AI知识")
print("AI学习助手已启动！（输入 'quit' 退出）\n")

while True:
    user_input = input("你：")
    if user_input.lower() == 'quit':
        break
    response = bot.chat(user_input)
    print(f"AI：{response}\n")
```

#### 实操 3.2：Function Calling 实战（25分钟）

```python
import json
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

# 定义工具函数
def get_weather(city):
    """模拟获取天气（实际项目中应该调用真实API）"""
    weather_data = {
        "北京": {"temp": 25, "weather": "晴", "humidity": 45},
        "上海": {"temp": 28, "weather": "多云", "humidity": 65},
        "广州": {"temp": 32, "weather": "阵雨", "humidity": 80},
        "深圳": {"temp": 30, "weather": "晴", "humidity": 60},
    }
    return weather_data.get(city, {"temp": 22, "weather": "未知", "humidity": 50})

def calculate(expression):
    """安全的数学计算"""
    try:
        # 只允许数字和基本运算符
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return "表达式包含不允许的字符"
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错：{str(e)}"

# 定义工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2+3*4'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 工具名到函数的映射
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
}

def run_agent(user_input):
    """一个简单的Agent循环"""
    messages = [{"role": "user", "content": user_input}]
    
    # 第1步：让模型决定要不要调用工具
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    
    # 第2步：检查是否有工具调用
    if response_message.tool_calls:
        # 把模型的回复加入消息
        messages.append(response_message)
        
        # 第3步：执行工具调用
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 调用工具：{function_name}({function_args})")
            
            # 执行函数
            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)
            
            print(f"📊 工具返回：{function_result}")
            
            # 把工具结果加入消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_result)
            })
        
        # 第4步：把工具结果发回模型，得到最终回答
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    # 没有工具调用，直接返回
    return response_message.content

# 测试
print("=" * 50)
print("  有工具的 AI 助手")
print("=" * 50)

queries = [
    "今天北京天气怎么样？适合出去玩吗？",
    "帮我算一下 (156 + 234) * 3 / 5 等于多少？",
    "上海和广州今天哪个城市更热？",
]

for query in queries:
    print(f"\n{'='*50}")
    print(f"用户：{query}")
    result = run_agent(query)
    print(f"AI：{result}")
```

#### 实操 3.3：Structured Output 实战（15分钟）

```python
from openai import OpenAI
import json

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

# 用 Prompt 引导模型输出 JSON（兼容不支持 Structured Output 的 API）
system_prompt = """
你是一个数据分析助手。当用户提供数据时，你需要输出JSON格式的分析结果。

输出格式必须严格遵循：
{
    "summary": "数据一句话总结",
    "total_count": 数字,
    "average": 数字,
    "max_value": 数字,
    "min_value": 数字,
    "insights": ["洞察1", "洞察2", "洞察3"]
}
只输出JSON，不要有其他内容的文本。
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": """
        以下是一周的产品销量数据，请分析：
        周一: 156件
        周二: 203件
        周三: 178件
        周四: 225件
        周五: 289件
        周六: 312件
        周日: 267件
        """}
    ],
    temperature=0.1  # 低温让输出更稳定
)

result = response.choices[0].message.content
print("原始输出：")
print(result)

# 解析 JSON
try:
    # 有些模型可能在JSON前后加 ```json ```，需要清理
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0]
    elif "```" in result:
        result = result.split("```")[1].split("```")[0]
    
    data = json.loads(result.strip())
    print("\n解析后的结构化数据：")
    print(f"总结：{data['summary']}")
    print(f"总销量：{data['total_count']}件")
    print(f"日均：{data['average']}件")
    print(f"最高：{data['max_value']}件 | 最低：{data['min_value']}件")
    print(f"洞察：")
    for insight in data['insights']:
        print(f"  · {insight}")
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
```

### 四、课后作业

1. 用 API 实现一个"AI 翻译助手"，支持中英互译，记录每次调用的 Token 消耗
2. 给翻译助手加上 Function Calling，支持"检测语言"功能
3. 比较 GPT-4o-mini、DeepSeek、通义千问三个 API 在相同任务上的效果和成本

---

## 第3课：RAG（检索增强生成）

### 一、学习目标

- 理解为什么要用 RAG
- 掌握 Embedding + 向量数据库 + 检索的核心流程
- 能够搭建一个简单的知识库问答系统

### 二、核心知识点

#### 2.1 为什么需要 RAG？

```
没有 RAG 的问题：
  用户："公司最新的请假流程是什么？"
  LLM："抱歉，我不知道你们公司的具体规定..." ❌
  
  原因：LLM 的知识来自训练数据，不知道你公司的内部文档

有了 RAG：
  用户："公司最新的请假流程是什么？"
  系统：1. 从公司文档中找到最相关的段落
       2. 把段落内容附在 Prompt 中
       3. LLM 基于这些内容回答
  LLM："根据公司2026年最新规定，请假流程如下：..." ✅
```

#### 2.2 RAG 工作流程

```
┌─────────────────────────────────────────────────────┐
│                    RAG 流程                           │
│                                                     │
│  离线阶段（建库）:                                    │
│  文档 → 分段(Chunking) → Embedding → 向量数据库       │
│                                                     │
│  在线阶段（问答）:                                    │
│  用户问题 → Embedding → 向量检索 → 取Top-K相关文档    │
│  → 拼入Prompt → LLM生成回答                          │
└─────────────────────────────────────────────────────┘
```

#### 2.3 核心组件详解

**1. 文档分段（Chunking）**：
- 把长文档切成小段（通常 500-1000 字符/段）
- 太大 → 检索不精确；太小 → 丢失上下文
- 常见做法：固定大小 + 重叠（overlap）

**2. Embedding 模型**：
- 将文本转为向量
- 推荐模型：OpenAI text-embedding-3-small / large

**3. 向量数据库**：
- 存储和检索向量
- 常用：Chroma（轻量）、FAISS（Facebook）、Milvus（企业级）
- 本课程使用 Chroma：本地运行、Python 原生、简单易用

**4. 检索策略**：
- 相似度检索：找与问题最相似的 K 个文档段
- MMR（最大边际相关性）：兼顾相关性和多样性

### 三、实操环节（60分钟）

#### 实操 3.1：搭建简易 RAG 知识库（40分钟）

```python
# ============================================
#   简易 RAG 知识库问答系统
# ============================================

# 安装依赖（在终端运行）:
# pip install openai chromadb numpy

from openai import OpenAI
import chromadb
import numpy as np
import os

# --- 配置 ---
# 使用 DeepSeek 作为 LLM（性价比高）
# 注意：DeepSeek 不提供 Embedding 模型，所以 Embedding 用其他模型
# 这里我们用 sentence-transformers 做本地 Embedding（免费）

# 如果需要使用 API Embedding，取消下面的注释：
# embedding_client = OpenAI(api_key="your-openai-key")

# 使用本地 Embedding 模型（免费，无需API Key）
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# 这个模型支持中文，轻量好用

# LLM 客户端
llm_client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

# --- 第1步：准备知识库文档 ---
documents = [
    {
        "title": "公司请假制度",
        "content": """
        公司请假制度（2026年修订版）
        
        一、年假：员工工作满1年后享有5天带薪年假，每增加1年工龄增加1天，上限15天。
        
        二、病假：凭医院证明可请病假，3天以内不扣工资，3天以上按基本工资80%发放。
        
        三、事假：需提前1天申请，事假期间无工资。
        
        四、请假流程：登录OA系统 → 选择请假类型 → 填写起止时间 → 提交审批 → 直属领导审批 → HR备案。
        
        五、紧急请假：如遇紧急情况，可先电话通知直属领导，事后24小时内在OA系统补提请假申请。
        """
    },
    {
        "title": "报销政策",
        "content": """
        公司费用报销制度
        
        一、差旅报销标准：
        - 国内出差：住宿费不超过400元/天，餐补100元/天
        - 国际出差：住宿费不超过200美元/天，餐补50美元/天
        - 交通：高铁二等座/飞机经济舱
        
        二、报销流程：
        1. 在OA系统提交报销申请
        2. 上传发票照片
        3. 部门经理审批
        4. 财务审核
        5. 打款到工资卡（审核通过后5个工作日内）
        
        三、注意事项：
        - 单笔超过5000元的报销需要副总审批
        - 发票必须是实际发生的业务相关费用
        - 报销申请需在费用发生后30天内提交
        """
    },
    {
        "title": "入职流程",
        "content": """
        新员工入职指南
        
        一、入职前准备：
        - 身份证原件及复印件
        - 学历学位证书复印件
        - 银行卡（用于发工资）
        - 一寸白底照片2张
        
        二、入职当天流程：
        1. 9:00 HR报到，填写入职表格
        2. 10:00 领取工卡、电脑等办公设备
        3. 11:00 IT部门进行系统账号开通和培训
        4. 14:00 部门主管进行工作安排
        5. 16:00 参加新员工培训
        
        三、试用期：
        - 试用期3个月
        - 试用期工资为转正的80%
        - 试用期通过后可申请转正
        """
    }
]

# --- 第2步：文本分段 ---
def split_text(text, chunk_size=500, overlap=100):
    """简单的文本分段（按字符）"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

all_chunks = []
for doc in documents:
    chunks = split_text(doc["content"])
    for chunk in chunks:
        all_chunks.append({
            "title": doc["title"],
            "content": chunk
        })

print(f"文档分段完成，共 {len(all_chunks)} 个文本段")

# --- 第3步：创建向量数据库 ---
# 使用 Chroma
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_knowledge")

# 生成 Embedding 并存入数据库
for i, chunk in enumerate(all_chunks):
    embedding = embedding_model.encode(chunk["content"]).tolist()
    collection.add(
        embeddings=[embedding],
        documents=[chunk["content"]],
        metadatas=[{"title": chunk["title"]}],
        ids=[f"chunk_{i}"]
    )

print(f"向量数据库创建完成，共 {collection.count()} 条记录")

# --- 第4步：检索 + 生成 ---
def search_knowledge(query, top_k=3):
    """检索最相关的知识"""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

def rag_answer(query):
    """RAG 问答：检索 + 生成"""
    # Step 1: 检索
    search_results = search_knowledge(query)
    
    # Step 2: 构建上下文
    context = ""
    for i, (doc, metadata) in enumerate(zip(
        search_results['documents'][0], 
        search_results['metadatas'][0]
    )):
        context += f"\n[参考文档{i+1}：{metadata['title']}]\n{doc}\n"
    
    # Step 3: 用 LLM 生成回答
    response = llm_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"""你是一个公司的AI助手。请根据以下知识库内容回答用户的问题。
如果知识库中没有相关信息，请诚实地说"这个问题我暂时无法回答，建议您咨询HR部门"。

知识库内容：
{context}

请基于上述内容给出准确、清晰的回答，并在回答中引用具体的政策细节。"""
            },
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

# --- 第5步：测试 ---
print("\n" + "=" * 50)
print("  公司知识库AI助手（RAG）")
print("=" * 50)

test_questions = [
    "公司的请假流程是什么？",
    "如果我生病了怎么请假？工资怎么算？",
    "出差的住宿费标准是多少？",
    "公司什么时候发工资？",  # 知识库没有这个问题
]

for q in test_questions:
    print(f"\n{'─' * 50}")
    print(f"🙋 提问：{q}")
    answer = rag_answer(q)
    print(f"🤖 回答：{answer}")
```

#### 实操 3.2：对比有无 RAG 的效果（20分钟）

```python
# 对比实验：有无 RAG 的回答差异

def answer_without_rag(query):
    """不使用 RAG，直接问 LLM"""
    response = llm_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个公司AI助手"},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# 测试对比
test_query = "我们公司的年假有多少天？请假需要找谁审批？"

print("=" * 60)
print("  RAG 效果对比实验")
print("=" * 60)
print(f"\n问题：{test_query}")

print("\n--- 不使用 RAG（直接问 LLM）---")
answer_without = answer_without_rag(test_query)
print(answer_without)

print("\n--- 使用 RAG（检索+生成）---")
answer_with = rag_answer(test_query)
print(answer_with)

print("\n💡 对比分析：")
print("  没有 RAG：模型可能会编造（幻觉）或者坦白说不知道")
print("  有 RAG：模型能引用公司真实文档，给出准确的回答")
```

### 四、课后作业（第5周综合）

> 🎯 **本周大作业**：搭建知识库问答系统
>
> **任务**：
> 1. 选择一个你感兴趣的知识领域（课程笔记、专业资料、项目文档等）
> 2. 收集至少 5 篇文档（可以是 Markdown 文件、TXT 文件等）
> 3. 搭建一个 RAG 知识库问答系统，要求：
>    - 使用 Chroma 或 FAISS 作为向量数据库
>    - 支持多轮对话
>    - 回答中引用原文来源
>    - 对知识库中没有的内容给出明确提示
>
> **提交内容**：
> - 完整代码（含注释）
> - 测试截图（至少 5 个不同的问答）
> - 一篇 500 字的项目说明

---

# 第6周：AI 应用开发

---

## 第1课：多平台 API 调用实战

### 一、学习目标

- 掌握 OpenAI、通义千问、DeepSeek 三大平台的 API 调用
- 学会统一封装不同平台的 API
- 能够实现流式输出

### 二、核心知识点

#### 2.1 主流 API 平台对比

| 平台 | 模型 | 特点 | 价格（约） |
|------|------|------|-----------|
| **OpenAI** | GPT-4o, GPT-4o-mini | 综合能力最强，生态最好 | GPT-4o: $2.5/1M输入 |
| **DeepSeek** | deepseek-chat | 性价比极高，中文效果好 | ¥1/1M Tokens |
| **通义千问** | qwen-turbo, qwen-plus | 阿里出品，中文理解好 | 有免费额度 |
| **Claude** | claude-opus, claude-sonnet | 长文本分析最强 | Sonnet: $3/1M输入 |

#### 2.2 统一 API 封装

```python
# 设计模式：用一个类统一管理多个平台的 API 调用

class MultiLLM:
    """多平台 LLM 统一调用"""
    
    def __init__(self):
        self.clients = {
            "openai": OpenAI(api_key="sk-xxx"),
            "deepseek": OpenAI(
                api_key="sk-xxx",
                base_url="https://api.deepseek.com"
            ),
            "qwen": OpenAI(
                api_key="sk-xxx",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        }
        self.models = {
            "openai": "gpt-4o-mini",
            "deepseek": "deepseek-chat",
            "qwen": "qwen-turbo"
        }
```

#### 2.3 流式输出（Streaming）

```python
# 流式输出——像打字机一样逐字输出
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[...],
    stream=True  # 开启流式
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 三、实操环节（60分钟）

```python
# 完整的多平台 LLM 工具类 + 流式对话
from openai import OpenAI
import time

class MultiLLM:
    """多平台 LLM 统一调用工具"""
    
    # 配置信息（实际使用时应从环境变量或配置文件读取）
    CONFIG = {
        "deepseek": {
            "api_key": "your-deepseek-key",
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat"
        },
        "qwen": {
            "api_key": "your-qwen-key", 
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-turbo"
        },
        "openai": {
            "api_key": "your-openai-key",
            "base_url": None,  # 使用默认
            "model": "gpt-4o-mini"
        }
    }
    
    def __init__(self, provider="deepseek"):
        """初始化，选择平台"""
        self.provider = provider
        config = self.CONFIG[provider]
        
        kwargs = {"api_key": config["api_key"]}
        if config["base_url"]:
            kwargs["base_url"] = config["base_url"]
        
        self.client = OpenAI(**kwargs)
        self.model = config["model"]
        self.conversation_history = []
    
    def chat(self, message, system_prompt=None, stream=True):
        """对话接口"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            temperature=0.7,
            max_tokens=2000
        )
        
        if stream:
            full_response = ""
            print(f"[{self.provider}] ", end="", flush=True)
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            print()
        else:
            full_response = response.choices[0].message.content
            print(f"[{self.provider}] {full_response}")
        
        # 保存对话历史
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": full_response})
        
        # 防止历史过长（保留最近10轮）
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return full_response
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")
    
    def switch_provider(self, provider):
        """切换平台"""
        self.__init__(provider)
        self.clear_history()
        print(f"已切换到：{provider}")

# 测试
if __name__ == "__main__":
    # 用 DeepSeek（国内直连，速度快）
    llm = MultiLLM("deepseek")
    
    print("AI 助手已启动\n")
    llm.chat("你好，请用三句话介绍你自己", 
             system_prompt="你是一个友好的AI助手，回复简洁明了")
    
    llm.chat("解释一下什么是机器学习")
    llm.chat("给我一个简单的例子")
```

**实操步骤**：
1. 申请至少一个平台的 API Key（推荐 DeepSeek，注册即送额度）
2. 填写代码中的 `your-xxx-key`
3. 运行代码，体验流式输出
4. 尝试切换不同平台，对比回复质量
5. 修改 `system_prompt`，让 AI 扮演不同角色

### 四、课后作业

1. 申请 DeepSeek 和通义千问的 API Key，完成多平台调用测试
2. 写一个"AI 模型对比器"：同一个问题发给 2-3 个平台，对比回复质量、速度和成本

---

## 第2课：Web 界面开发

### 一、学习目标

- 掌握 Streamlit 的基本用法
- 能够用 Streamlit 快速搭建 AI 应用的 Web 界面
- 完成一个聊天机器人 Web 应用

### 二、核心知识点

#### 2.1 Streamlit vs Gradio

| 特性 | Streamlit | Gradio |
|------|-----------|--------|
| **定位** | 数据应用/仪表盘 | ML 模型 Demo |
| **学习曲线** | 低 | 低 |
| **UI 灵活度** | 高（更像网页） | 中（更像表单） |
| **聊天组件** | `st.chat_message` + `st.chat_input`（原生） | `gr.ChatInterface` |
| **部署** | Streamlit Cloud 免费 | Hugging Face Spaces 免费 |
| **社区生态** | 更大 | 中等 |

> 💡 **本课程推荐 Streamlit**：更灵活、生态更大、更适合做完整应用。

#### 2.2 Streamlit 核心 API

```python
import streamlit as st

# 页面设置（必须放在最前面）
st.set_page_config(page_title="标题", page_icon="🤖")

# 显示内容
st.title("标题")
st.markdown("**Markdown** 内容")
st.write("任何内容")

# 输入组件
name = st.text_input("输入你的名字")
age = st.slider("年龄", 0, 100, 20)
option = st.selectbox("选择", ["A", "B", "C"])
clicked = st.button("点我")

# 聊天组件
messages = st.container()
with messages:
    st.chat_message("user").write("用户消息")
    st.chat_message("assistant").write("AI回复")

# 聊天输入框
if prompt := st.chat_input("输入消息..."):
    # 处理用户输入
    pass

# 侧边栏
with st.sidebar:
    st.header("设置")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
```

### 三、实操环节（60分钟）

#### 实操 3.1：安装 Streamlit + 第一个应用（10分钟）

```bash
# 在终端中运行
pip install streamlit

# 创建第一个应用
# 新建文件 app.py，内容：
```

```python
# app.py
import streamlit as st

st.set_page_config(page_title="我的AI应用", page_icon="🤖")
st.title("🎉 我的第一个 Streamlit 应用")
st.markdown("---")

name = st.text_input("你叫什么名字？")
if name:
    st.success(f"你好，{name}！欢迎来到 AI 世界 🚀")
    
    hobby = st.selectbox("你对什么感兴趣？", 
                         ["AI编程", "数据分析", "机器学习", "深度学习", "AI Agent"])
    
    if st.button("生成学习建议"):
        suggestions = {
            "AI编程": "建议从 Python 基础开始，然后用 Streamlit 做小项目",
            "数据分析": "建议学 Pandas + Matplotlib，用 Jupyter Notebook 练习",
            "机器学习": "建议学 Scikit-learn，从鸢尾花分类开始",
            "深度学习": "建议学 TensorFlow/Keras，从 MNIST 手写数字开始",
            "AI Agent": "建议先学 LLM API 调用，然后学 Function Calling 和 LangChain"
        }
        st.info(suggestions[hobby])
```

在终端运行：
```bash
streamlit run app.py
```

#### 实操 3.2：构建聊天机器人界面（25分钟）

```python
# chat_app.py — 完整的聊天机器人 Web 应用
import streamlit as st
from openai import OpenAI

# ===== 页面配置 =====
st.set_page_config(
    page_title="AI 聊天助手",
    page_icon="💬",
    layout="wide"
)

# ===== 侧边栏配置 =====
with st.sidebar:
    st.title("⚙️ 设置")
    
    # API 配置
    api_key = st.text_input("API Key", type="password", 
                            help="输入你的 DeepSeek 或 OpenAI API Key")
    provider = st.selectbox("选择平台", ["DeepSeek", "OpenAI", "通义千问"])
    
    # 模型参数
    st.markdown("---")
    st.subheader("模型参数")
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1,
                           help="越高越有创意，越低越保守")
    max_tokens = st.slider("最大长度", 100, 4000, 2000, 100)
    
    # 系统提示词
    st.markdown("---")
    st.subheader("系统提示词")
    system_prompt = st.text_area(
        "设定 AI 的角色",
        value="你是一个友好的AI助手，回答简洁明了，用中文回复。",
        height=100
    )
    
    # 功能按钮
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("📋 导出对话", use_container_width=True):
            chat_text = ""
            for m in st.session_state.messages:
                role = "用户" if m["role"] == "user" else "AI"
                chat_text += f"{role}：{m['content']}\n\n"
            st.download_button("下载对话记录", chat_text, 
                             "chat_history.txt", use_container_width=True)

# ===== 初始化 =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# 初始化 LLM 客户端
def get_client():
    provider_configs = {
        "DeepSeek": {"base_url": "https://api.deepseek.com", "model": "deepseek-chat"},
        "OpenAI": {"base_url": None, "model": "gpt-4o-mini"},
        "通义千问": {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-turbo"}
    }
    
    config = provider_configs[provider]
    kwargs = {"api_key": api_key}
    if config["base_url"]:
        kwargs["base_url"] = config["base_url"]
    
    return OpenAI(**kwargs), config["model"]

# ===== 主界面 =====
st.title("💬 AI 聊天助手")
st.caption("基于 Streamlit + LLM API | 支持多平台切换")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入
if prompt := st.chat_input("输入你的问题..."):
    if not api_key:
        st.error("请先在侧边栏输入 API Key")
    else:
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 获取 AI 回复
        with st.chat_message("assistant"):
            try:
                client, model = get_client()
                
                # 构建消息
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend([
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ])
                
                # 流式输出
                with st.spinner("思考中..."):
                    stream = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True
                    )
                
                # 用空容器接收流式内容
                response_placeholder = st.empty()
                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                
                # 显示 Token 估算
                st.caption(f"回复字数：{len(full_response)} | Temperature：{temperature}")
                
            except Exception as e:
                st.error(f"调用失败：{str(e)}")
                st.info("请检查：1) API Key 是否正确 2) 网络是否通畅 3) 账户是否有余额")

# ===== 底部信息 =====
st.markdown("---")
st.caption("🤖 AI 聊天助手 | 基于 Streamlit 构建 | 数据仅保存在当前会话中")
```

#### 实操 3.3：运行并测试（25分钟）

```bash
# 在终端运行
streamlit run chat_app.py
```

测试清单：
1. ✅ 输入 API Key，选择 DeepSeek 平台
2. ✅ 发送第一条消息，观察流式输出效果
3. ✅ 切换平台，对比回复差异
4. ✅ 调整 Temperature，观察回复风格变化
5. ✅ 修改系统提示词，让 AI 扮演不同角色
6. ✅ 点击"清空对话"
7. ✅ 导出对话记录

### 四、课后作业

1. 为聊天机器人添加"对话标题自动生成"功能（首次对话后自动生成标题）
2. 添加"Markdown 渲染"功能（代码块高亮、表格显示等）
3. 对比 Streamlit 和 Gradio 开发体验，写一篇 300 字对比笔记

---

## 第3课：AI 项目实战 — 智能问答系统

### 一、学习目标

- 综合运用 API 调用 + Web 界面 + RAG 技术
- 完成一个完整的 AI 问答系统
- 理解 AI 项目的完整开发流程

### 二、项目概述

> 🎯 **项目**：专业知识问答系统
>
> **功能**：
> 1. 上传课程资料（PDF/TXT/MD）
> 2. 基于资料内容回答问题
> 3. 支持多轮对话
> 4. 显示引用来源
> 5. Web 界面友好

### 三、实操环节（60分钟）

#### 完整项目代码

```python
# knowledge_qa.py — 专业知识问答系统
import streamlit as st
import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os
import tempfile
from pathlib import Path

# ===== 页面配置 =====
st.set_page_config(page_title="专业知识问答系统", page_icon="📚", layout="wide")

# ===== 初始化组件 =====
@st.cache_resource
def init_embedding_model():
    """缓存 Embedding 模型（只加载一次）"""
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_resource
def init_chroma():
    """初始化 Chroma 客户端"""
    return chromadb.Client()

# ===== 侧边栏 =====
with st.sidebar:
    st.title("📚 知识库管理")
    
    api_key = st.text_input("API Key", type="password")
    
    # 上传文件
    uploaded_files = st.file_uploader(
        "上传知识文档",
        type=["txt", "md", "py", "pdf"],
        accept_multiple_files=True,
        help="支持 TXT、Markdown、Python、PDF 文件"
    )
    
    if uploaded_files and api_key:
        if st.button("📥 处理文档并创建知识库", use_container_width=True):
            with st.spinner("正在处理文档..."):
                embedding_model = init_embedding_model()
                chroma_client = init_chroma()
                
                # 删除旧集合（如果有的话）
                try:
                    chroma_client.delete_collection("knowledge_base")
                except:
                    pass
                
                collection = chroma_client.create_collection("knowledge_base")
                
                all_chunks = []
                chunk_metadatas = []
                
                for file in uploaded_files:
                    # 读取文件内容
                    content = ""
                    if file.name.endswith('.pdf'):
                        # PDF 处理需要 PyPDF2 或 pdfplumber
                        # 这里简化为提示
                        st.warning(f"PDF文件需要安装 PyPDF2: pip install PyPDF2")
                        content = file.read().decode('utf-8', errors='ignore')
                    else:
                        content = file.read().decode('utf-8')
                    
                    # 分块（每块500字，重叠100字）
                    chunk_size = 500
                    overlap = 100
                    for i in range(0, len(content), chunk_size - overlap):
                        chunk = content[i:i + chunk_size]
                        if len(chunk.strip()) > 50:  # 跳过太短的块
                            all_chunks.append(chunk)
                            chunk_metadatas.append({
                                "source": file.name,
                                "chunk_index": len(all_chunks)
                            })
                
                # 生成 Embedding 并存入数据库
                if all_chunks:
                    embeddings = embedding_model.encode(all_chunks).tolist()
                    collection.add(
                        embeddings=embeddings,
                        documents=all_chunks,
                        metadatas=chunk_metadatas,
                        ids=[f"chunk_{i}" for i in range(len(all_chunks))]
                    )
                    st.session_state['kb_ready'] = True
                    st.session_state['chunk_count'] = len(all_chunks)
                    st.success(f"✅ 知识库创建成功！共 {len(all_chunks)} 个文本块")
                else:
                    st.error("未能提取有效文本内容")
    
    # 知识库状态
    if st.session_state.get('kb_ready'):
        st.info(f"📊 知识库状态：已就绪 | {st.session_state['chunk_count']} 个文本块")
    
    st.markdown("---")
    st.subheader("⚙️ 模型参数")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    top_k = st.slider("检索数量", 1, 10, 3)

# ===== 主界面 =====
st.title("📚 专业知识问答系统")
st.caption("上传你的学习资料，基于资料内容进行智能问答")

# 初始化消息
if "qa_messages" not in st.session_state:
    st.session_state.qa_messages = []

# 显示历史消息
for msg in st.session_state.qa_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            with st.expander("📖 参考来源"):
                for src in msg["sources"]:
                    st.caption(f"📄 {src['source']}（相关度：{src['relevance']}）")

# 聊天输入
if prompt := st.chat_input("输入你的问题（基于已上传的知识库）..."):
    if not api_key:
        st.error("请先在侧边栏输入 API Key")
    elif not st.session_state.get('kb_ready'):
        st.error("请先上传文档并创建知识库")
    else:
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.qa_messages.append({"role": "user", "content": prompt})
        
        # AI 回复
        with st.chat_message("assistant"):
            try:
                # Step 1: 检索相关知识
                embedding_model = init_embedding_model()
                chroma_client = init_chroma()
                collection = chroma_client.get_collection("knowledge_base")
                
                query_embedding = embedding_model.encode(prompt).tolist()
                search_results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
                
                # Step 2: 构建上下文
                context = ""
                sources = []
                for doc, metadata, distance in zip(
                    search_results['documents'][0],
                    search_results['metadatas'][0],
                    search_results['distances'][0]
                ):
                    context += f"\n[来源：{metadata['source']}]\n{doc}\n"
                    sources.append({
                        "source": metadata['source'],
                        "relevance": f"{1 - distance:.2f}"  # 距离越小越相关
                    })
                
                # Step 3: LLM 生成回答
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )
                
                messages = [
                    {
                        "role": "system",
                        "content": f"""你是学习助手，请基于以下知识库内容回答问题。

规则：
1. 如果知识库有相关内容，请准确引用
2. 如果知识库没有，请诚实说明
3. 回答末尾请标注引用的文档名称
4. 用中文回复，条理清晰

知识库内容：
{context}"""
                    },
                    {"role": "user", "content": prompt}
                ]
                
                with st.spinner("检索并分析中..."):
                    stream = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=messages,
                        temperature=temperature,
                        stream=True
                    )
                
                response_placeholder = st.empty()
                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
                # 显示引用来源
                with st.expander("📖 参考来源"):
                    for src in sources:
                        st.caption(f"📄 {src['source']}（相关度：{src['relevance']}）")
                
                st.session_state.qa_messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"处理失败：{str(e)}")

st.markdown("---")
st.caption("💡 提示：上传你的课程讲义、笔记、教材等文本文件，AI 将基于这些内容回答问题")
```

### 四、课后作业（第6周综合）

> 🎯 **本周大作业**：制作聊天机器人
>
> **要求**：
> 1. 使用 Streamlit 构建 Web 界面
> 2. 支持至少 2 个 LLM 平台切换
> 3. 支持对话历史管理（保存/加载/清空）
> 4. 支持 Markdown 渲染（代码高亮 + LaTeX 公式 + 表格）
> 5. 部署到 Streamlit Cloud 或本地可运行
>
> **加分项**：
> - 支持上传文件并基于文件内容对话（RAG）
> - 支持语音输入
> - 支持导出对话为 PDF

---

# 第7周：Agent 与 MCP（核心周）

---

## 第1课：什么是 Agent

### 一、学习目标

- 理解 Agent 的核心理念和能力框架
- 理解 Agent 与聊天机器人的本质区别
- 理解 Agent 的基本循环：感知 → 推理 → 规划 → 执行

### 二、核心知识点

#### 2.1 Chatbot → Workflow → Agent

```
Chatbot（聊天机器人）：
  用户输入 → LLM → 文本回复
  特点：一问一答，没有工具，没有记忆

Workflow（工作流）：
  用户输入 → [步骤1] → [步骤2] → [步骤3] → 输出
  特点：固定流程，可预测，适合标准化任务

Agent（智能体）：
  用户输入 → 理解意图 → 制定计划 → 调用工具 → 
  观察结果 → 调整计划 → ... → 完成任务
  特点：自主决策，动态调整，使用工具，有记忆
```

#### 2.2 Agent 四能力模型

```
        ┌──────────────────────────┐
        │      感知 (Perceive)      │
        │  理解用户意图和环境状态     │
        └───────────┬──────────────┘
                    ↓
        ┌──────────────────────────┐
        │      推理 (Reason)        │
        │  分析信息、做出判断        │
        └───────────┬──────────────┘
                    ↓
        ┌──────────────────────────┐
        │      规划 (Plan)          │
        │  制定执行步骤和策略        │
        └───────────┬──────────────┘
                    ↓
        ┌──────────────────────────┐
        │      执行 (Act)           │
        │  调用工具、完成操作        │
        └───────────┬──────────────┘
                    ↓
              观察结果，回到"感知"
```

#### 2.3 Agent 的核心循环

```
while 任务未完成 and 步数 < 最大步数:
    1. 观察当前状态
    2. 思考下一步做什么
    3. 如果需要更多信息 → 调用工具获取
    4. 如果可以回答 → 生成最终答案
    5. 检查是否需要人工介入
```

#### 2.4 什么时候该用 Agent？什么时候不该用？

| ✅ 适合用 Agent | ❌ 不适合用 Agent |
|-----------------|-------------------|
| 任务步骤不确定 | 流程固定可预测 |
| 需要动态决策 | 普通脚本就能解决 |
| 需要多种工具配合 | 只需简单计算/查询 |
| 需要多轮探索 | 单次查询就能完成 |
| 失败后可以重试 | 后果不可逆的操作 |

> 💡 **推荐阅读**：[Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

### 三、实操环节（60分钟）

#### 实操 3.1：从聊天机器人到 Agent（20分钟）

```python
# 对比：聊天机器人 vs Agent

# === 方式1：聊天机器人（只能聊天） ===
def chatbot(query):
    """只能回答，不能做事"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

# === 方式2：Agent（能做事） ===
import json
from datetime import datetime

# Agent 的工具箱
def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_file(pattern, directory="."):
    """搜索文件"""
    import glob
    files = glob.glob(f"{directory}/**/{pattern}", recursive=True)
    return files[:10]  # 最多返回10个

def create_reminder(task, time_str):
    """创建提醒（模拟）"""
    return f"✅ 已创建提醒：{task} - {time_str}"

# Agent 的工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_file",
            "description": "搜索文件，支持通配符如 *.py, *.md",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "文件匹配模式"},
                    "directory": {"type": "string", "description": "搜索目录"}
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "创建一个提醒事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "提醒内容"},
                    "time_str": {"type": "string", "description": "提醒时间"}
                },
                "required": ["task", "time_str"]
            }
        }
    }
]

# 工具函数映射
available_functions = {
    "get_current_time": get_current_time,
    "search_file": search_file,
    "create_reminder": create_reminder,
}

def agent_loop(user_input, max_steps=5):
    """Agent 主循环"""
    messages = [{"role": "user", "content": user_input}]
    step = 0
    
    while step < max_steps:
        step += 1
        print(f"\n{'='*40}")
        print(f"🔄 Step {step}/{max_steps}")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )
        
        response_message = response.choices[0].message
        
        # 如果没有工具调用，说明 Agent 认为可以回答了
        if not response_message.tool_calls:
            print(f"✅ 任务完成：{response_message.content[:100]}...")
            return response_message.content
        
        # 如果有工具调用，执行工具
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 调用工具：{func_name}({func_args})")
            
            func = available_functions[func_name]
            result = func(**func_args)
            
            print(f"📊 工具返回：{result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
    
    return "达到最大步数限制，任务未完成"

# 测试
print("=" * 60)
print("  Agent vs Chatbot 对比")
print("=" * 60)

# 聊天机器人试试
print("\n--- 聊天机器人 ---")
print(chatbot("帮我查一下现在几点，然后在当前目录搜索所有Python文件"))

# Agent 试试
print("\n--- Agent ---")
result = agent_loop("帮我查一下现在几点，然后在当前目录搜索所有Python文件，最后设置一个下午3点的提醒'交作业'")
print(f"\n最终结果：{result}")
```

#### 实操 3.2：观察 Agent 决策过程（20分钟）

```python
# 打印 Agent 每步的思考和决策
def agent_with_logging(user_input):
    """带详细日志的 Agent"""
    messages = [
        {"role": "system", "content": """你是一个AI助手，可以使用工具完成任务。
在执行每个工具前，请先说明你要做什么、为什么这样做。
完成任务后给出最终答案。"""},
        {"role": "user", "content": user_input}
    ]
    
    for step in range(5):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )
        
        msg = response.choices[0].message
        
        if msg.content:
            print(f"💭 思考：{msg.content}")
        
        if msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"🔧 计划执行：{tc.function.name}")
                print(f"   参数：{tc.function.arguments}")
                
                func = available_functions[tc.function.name]
                args = json.loads(tc.function.arguments)
                result = func(**args)
                
                print(f"   ✅ 结果：{result}")
                
                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })
        else:
            print(f"\n🎯 Agent完成：{msg.content}")
            return msg.content
    
    return "任务未完成"

agent_with_logging(
    "帮我完成以下任务："
    "1. 看看现在几点了"
    "2. 在桌面搜索所有Markdown文件"
    "3. 设置一个明天早上9点的提醒'准备AI课程作业'"
)
```

#### 实操 3.3：分析 Claude Code Agent 的设计（20分钟）

> 💡 **教学设计**：Claude Code 是目前最好的 Agent 工程样本。让我们分析它的工作方式。

**阅读并讨论**：
1. Claude Code 的 Agent Loop 是什么样的？
2. 它有哪些工具？（读文件、写文件、执行命令、搜索代码...）
3. 它的权限机制是怎样的？（哪些操作需要用户确认？）
4. 它如何处理上下文过长的问题？（压缩/摘要）

**推荐阅读**：
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

### 四、课后作业

1. 用自己的话画一张图，说明 Agent 的核心循环
2. 列举 3 个适合用 Agent 的场景和 3 个不适合用 Agent 的场景，并说明原因
3. 阅读 Anthropic 的 [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，写 300 字读后感

---

## 第2课：LangChain / LangGraph

### 一、学习目标

- 理解 LangChain 的核心组件
- 掌握 Agent 的工具调用和记忆管理
- 理解 LangGraph 的状态图编排思想
- 能够制作一个"AI 秘书"

### 二、核心知识点

#### 2.1 LangChain 核心组件

```
LangChain 三大核心：
┌─────────────────────────────────────────┐
│  Model（模型）                           │
│  · LLM：ChatOpenAI, ChatDeepSeek...     │
│  · Embedding：文本转向量                 │
├─────────────────────────────────────────┤
│  Tool（工具）                            │
│  · 搜索、计算器、API调用、文件操作...      │
│  · 封装为模型可以理解的接口               │
├─────────────────────────────────────────┤
│  Memory（记忆）                          │
│  · 短期：当前对话上下文                   │
│  · 长期：跨会话的持久记忆                 │
│  · 摘要：对话过长时自动压缩               │
└─────────────────────────────────────────┘
```

#### 2.2 LangGraph — 状态图编排

```
LangGraph 的核心思想：用"图"来控制 Agent 的流程

     ┌──────────┐
     │  START   │
     └────┬─────┘
          ↓
     ┌──────────┐    有工具调用    ┌──────────┐
     │  Agent   │ ──────────────→ │  Tools   │
     │ (思考)   │ ←────────────── │ (执行)   │
     └────┬─────┘   返回工具结果   └──────────┘
          │
          │ 没有工具调用（任务完成）
          ↓
     ┌──────────┐
     │   END    │
     └──────────┘

比普通的 while 循环更灵活：
- 可以添加条件分支
- 可以添加人工审批节点
- 可以并行执行多个工具
- 支持断点续执行
```

### 三、实操环节（60分钟）

#### 实操 3.1：用 LangChain 构建 Agent（30分钟）

```python
# 安装：pip install langchain langchain-openai

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import datetime
import os

# === 定义工具 ===
@tool
def get_current_time():
    """获取当前日期和时间"""
    return datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def calculate(expression: str):
    """执行数学计算，支持加减乘除和括号"""
    try:
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return "表达式包含不允许的字符"
        return f"{expression} = {eval(expression)}"
    except Exception as e:
        return f"计算出错：{e}"

@tool
def search_course_info(keyword: str):
    """搜索课程相关信息（模拟）"""
    courses = {
        "python": "Python基础课程：每周二下午2点，实验室301",
        "机器学习": "机器学习课程：每周四上午9点，教学楼B201",
        "深度学习": "深度学习课程：每周五下午3点，实验室201",
        "agent": "AI Agent课程：每周三上午10点，在线课程",
    }
    for key, value in courses.items():
        if keyword.lower() in key.lower():
            return f"找到课程：{value}"
    return f"未找到与'{keyword}'相关的课程"

@tool
def set_reminder(task: str, time_str: str):
    """设置提醒事项"""
    # 实际项目中会写入数据库或日历
    return f"✅ 已设置提醒：'{task}' - {time_str}"

# === 创建 Agent ===
# 使用 DeepSeek 作为底层模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
    temperature=0.3
)

tools = [get_current_time, calculate, search_course_info, set_reminder]

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个智能AI秘书，可以帮助用户完成以下任务：
- 查询时间和日期
- 数学计算
- 搜索课程信息
- 设置提醒

请使用工具来完成任务。如果需要多个步骤，就一步步来。
用中文回复，语气友好、简洁。"""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 显示执行过程
    max_iterations=5,
    handle_parsing_errors=True
)

# === 使用 Agent ===
chat_history = []

def ai_secretary(user_input):
    """AI秘书对话接口"""
    result = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=result["output"]))
    
    # 保持历史在合理长度
    if len(chat_history) > 10:
        chat_history[:] = chat_history[-10:]
    
    return result["output"]

# 测试
print("=" * 50)
print("  🤵 AI 智能秘书")
print("=" * 50)

test_tasks = [
    "现在几点了？",
    "帮我算一下 (128 + 256) * 3.5 / 7 等于多少？",
    "Python课什么时候上？",
    "帮我设置一个提醒：明天下午3点交机器学习作业",
]

for task in test_tasks:
    print(f"\n{'─' * 50}")
    print(f"🙋 {task}")
    response = ai_secretary(task)
    print(f"🤵 {response}")
```

#### 实操 3.2：用 LangGraph 实现可中断 Agent（30分钟）

```python
# 安装：pip install langgraph

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import operator
import json

# === 定义状态 ===
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    need_human_approval: bool

# === 定义节点 ===
def agent_node(state):
    """Agent 的思考节点"""
    messages = state["messages"]
    response = llm.bind_tools(tools).invoke(messages)
    return {"messages": [response]}

def should_continue(state):
    """判断下一步：继续工具调用 / 结束 / 需要人工审批"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 如果有工具调用
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        # 检查是否有危险操作需要审批
        for tc in last_message.tool_calls:
            if tc["name"] in ["set_reminder"]:
                return "human_approval"
        return "tools"
    
    # 没有工具调用，结束
    return END

def human_approval_node(state):
    """人工审批节点"""
    print("\n⚠️  需要人工审批！")
    messages = state["messages"]
    last_message = messages[-1]
    
    for tc in last_message.tool_calls:
        print(f"   操作：{tc['name']}")
        print(f"   参数：{tc['args']}")
    
    approval = input("   批准执行吗？(y/n): ")
    return {"messages": messages, "need_human_approval": approval.lower() == 'y'}

# === 构建图 ===
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("human_approval", human_approval_node)

# 添加边
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "human_approval": "human_approval",
        END: END
    }
)
workflow.add_edge("tools", "agent")
workflow.add_edge("human_approval", "tools")

# 编译
app = workflow.compile()

# 测试
def run_graph(user_input):
    """运行 LangGraph Agent"""
    result = app.invoke({
        "messages": [HumanMessage(content=user_input)],
        "need_human_approval": False
    })
    
    # 打印最后一条AI消息
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content
    return "处理完成"

# 运行测试
print("\n" + "=" * 50)
print("  LangGraph 可中断 Agent")
print("=" * 50)

result = run_graph("帮我设置一个提醒：明天上午10点开会")
print(f"\n最终结果：{result}")
```

### 四、课后作业

1. 比较直接用 API 写 Agent 和用 LangChain 写 Agent 的代码差异，各有什么优缺点
2. 为"AI 秘书"添加 2 个新工具（如发送邮件、查询天气），并测试
3. 阅读 LangGraph 官方文档的 Quick Start，跑通官方示例

---

## 第3课：MCP（Model Context Protocol）

### 一、学习目标

- 理解 MCP 的概念和价值
- 理解 MCP Client 和 MCP Server 的关系
- 能够配置和使用 MCP Server
- 了解 MCP 与 A2A、ACP 等协议的区别

### 二、核心知识点

#### 2.1 什么是 MCP？

```
MCP (Model Context Protocol) = AI 应用的 "USB-C 接口"

传统方式：每个 AI 应用单独连接每个工具
  AI应用1 ──→ 数据库A
  AI应用1 ──→ 文件系统
  AI应用2 ──→ 数据库A（重复开发！）
  AI应用2 ──→ 文件系统（重复开发！）

MCP 方式：统一的标准化连接
  AI应用1 ─┐         ┌──→ MCP Server(数据库)
            ├─ MCP ──┼──→ MCP Server(文件系统)
  AI应用2 ─┘         └──→ MCP Server(搜索)
```

#### 2.2 MCP 架构

```
┌─────────────┐         ┌─────────────┐
│  MCP Client  │ ←────→ │  MCP Server  │
│  (AI应用)    │  MCP协议 │  (工具提供方) │
└─────────────┘         └─────────────┘

MCP Client：AI 应用侧
  · 发起连接请求
  · 发现可用的工具/资源
  · 调用工具
  · 读取资源

MCP Server：工具提供方
  · 暴露工具列表
  · 处理工具调用
  · 返回执行结果
  · 管理权限
```

#### 2.3 常见 MCP Server

| MCP Server | 功能 | 安装 |
|------------|------|------|
| **Filesystem** | 读写本地文件 | `npx @modelcontextprotocol/server-filesystem` |
| **GitHub** | 操作 GitHub 仓库 | `npx @modelcontextprotocol/server-github` |
| **Postgres** | 查询数据库 | `npx @modelcontextprotocol/server-postgres` |
| **Brave Search** | 网页搜索 | `npx @modelcontextprotocol/server-brave-search` |
| **Puppeteer** | 浏览器操作 | `npx @modelcontextprotocol/server-puppeteer` |
| **Fetch** | 获取网页内容 | `npx @modelcontextprotocol/server-fetch` |

#### 2.4 MCP、A2A、ACP 的区别

| 协议 | 全称 | 解决什么问题 |
|------|------|-------------|
| **MCP** | Model Context Protocol | Agent 如何连接工具和数据源 |
| **A2A** | Agent-to-Agent Protocol | Agent 之间如何发现和协作 |
| **ACP** | Agent Client Protocol | 编辑器/IDE 如何与 Agent 通信 |

> 💡 **关系**：MCP 连接工具，A2A 连接 Agent，ACP 连接宿主应用。

### 三、实操环节（60分钟）

#### 实操 3.1：体验 MCP — 在 Claude Code 中配置（30分钟）

**Step 1：了解 Claude Code 的 MCP 配置**

Claude Code 使用 `.mcp.json` 文件配置 MCP Server：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-fetch"
      ]
    }
  }
}
```

**Step 2：配置 Filesystem MCP Server**

```bash
# 在项目根目录创建 .mcp.json
# 允许 Claude Code 通过 MCP 访问项目文件
```

配置文件内容（调整路径为你的实际项目路径）：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "d:/2026/AI-Learning Route"
      ]
    }
  }
}
```

**Step 3：重启 Claude Code 并测试**

在 Claude Code 中输入：
```
请列出当前项目根目录下的所有文件和文件夹
```

观察 Claude Code 是否通过 MCP Filesystem Server 来获取文件列表。

#### 实操 3.2：用 Python 编写 MCP Client（30分钟）

```python
# 安装 MCP SDK：pip install mcp

# 这是一个简化的 MCP 概念演示
# 完整的 MCP Client 实现请参考官方文档: https://modelcontextprotocol.io/

"""
MCP 的核心概念演示代码

在真实项目中，你可以使用 MCP Python SDK：
  pip install mcp

然后参考官方示例构建 Client:
  https://github.com/modelcontextprotocol/python-sdk

MCP Client 的核心工作流程：
  1. 连接 MCP Server
  2. 获取可用工具列表
  3. 让 LLM 决定调用哪个工具
  4. 通过 MCP 协议调用工具
  5. 将工具结果返回给 LLM
"""

from dataclasses import dataclass
from typing import Any

@dataclass
class MCPTool:
    """MCP 工具定义"""
    name: str
    description: str
    parameters: dict

class SimpleMCPServer:
    """模拟 MCP Server"""
    
    def __init__(self, name):
        self.name = name
        self.tools = []
    
    def add_tool(self, name, description, parameters, handler):
        """注册工具"""
        self.tools.append({
            "definition": MCPTool(name, description, parameters),
            "handler": handler
        })
    
    def list_tools(self):
        """列出可用工具（MCP: tools/list）"""
        return [t["definition"] for t in self.tools]
    
    def call_tool(self, tool_name, arguments):
        """调用工具（MCP: tools/call）"""
        for tool in self.tools:
            if tool["definition"].name == tool_name:
                return tool["handler"](**arguments)
        raise ValueError(f"Unknown tool: {tool_name}")

# === 创建本地文件 MCP Server ===
import os
import glob

file_server = SimpleMCPServer("local-filesystem")

def read_file_handler(path):
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"文件内容（前500字）：\n{content[:500]}"
    except Exception as e:
        return f"读取失败：{e}"

def list_files_handler(directory):
    """列出文件"""
    try:
        files = os.listdir(directory)
        return f"目录 {directory} 包含：\n" + "\n".join(f"  · {f}" for f in files)
    except Exception as e:
        return f"列出失败：{e}"

def search_files_handler(pattern):
    """搜索文件"""
    try:
        files = glob.glob(f"**/{pattern}", recursive=True)
        if not files:
            return f"未找到匹配 '{pattern}' 的文件"
        return f"找到 {len(files)} 个文件：\n" + "\n".join(f"  · {f}" for f in files[:10])
    except Exception as e:
        return f"搜索失败：{e}"

# 注册工具
file_server.add_tool(
    "read_file", "读取文件内容",
    {"path": {"type": "string", "description": "文件路径"}},
    read_file_handler
)

file_server.add_tool(
    "list_files", "列出目录下的文件",
    {"directory": {"type": "string", "description": "目录路径"}},
    list_files_handler
)

file_server.add_tool(
    "search_files", "搜索匹配模式的文件",
    {"pattern": {"type": "string", "description": "文件匹配模式，如 *.py"}},
    search_files_handler
)

# === 测试 MCP Server ===
print("=" * 50)
print("  MCP Server 演示")
print("=" * 50)

# 列出工具
print("\n📋 可用工具：")
for tool in file_server.list_tools():
    print(f"  · {tool.name}: {tool.description}")

# 测试调用
print("\n🔧 测试工具调用：")
result = file_server.call_tool("list_files", {"directory": "."})
print(result)

result = file_server.call_tool("search_files", {"pattern": "*.md"})
print(f"\n{result}")

# === 将 MCP Server 接入 Agent ===
print("\n" + "=" * 50)
print("  MCP + Agent 联动")
print("=" * 50)

# 把 MCP 工具转为 OpenAI 格式
def mcp_to_openai_tools(mcp_server):
    """将 MCP 工具转为 OpenAI Function Calling 格式"""
    openai_tools = []
    for tool in mcp_server.list_tools():
        openai_tools.append({
            "type": "function",
            "function": {
                "name": f"mcp_{tool.name}",
                "description": f"[MCP:{mcp_server.name}] {tool.description}",
                "parameters": {
                    "type": "object",
                    "properties": tool.parameters,
                    "required": list(tool.parameters.keys())
                }
            }
        })
    return openai_tools

mcp_tools = mcp_to_openai_tools(file_server)

def mcp_agent(user_input):
    """能使用 MCP 工具的 Agent"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": user_input}],
        tools=mcp_tools
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        for tc in msg.tool_calls:
            # 去掉 mcp_ 前缀
            actual_name = tc.function.name.replace("mcp_", "")
            args = json.loads(tc.function.arguments)
            result = file_server.call_tool(actual_name, args)
            
            print(f"🔧 MCP调用：{actual_name}({args})")
            print(f"📊 结果：{result[:200]}...")
    
    return msg

print("\n测试：让 Agent 通过 MCP 读取文件")
mcp_agent("请列出当前目录的文件，并搜索所有 Markdown 文件")

print("\n💡 这就是 MCP 的核心价值：")
print("  1. 标准化的工具接口")
print("  2. AI 应用和工具解耦")
print("  3. 一次开发，多个 AI 应用共用")
```

### 四、课后作业（第7周综合）

> 🎯 **本周大作业**：开发 AI 秘书
>
> **功能要求**：
> 1. 能查询当前时间、日期、星期
> 2. 能执行数学计算
> 3. 能创建提醒事项
> 4. 能搜索本地文件
> 5. 支持多轮对话（有记忆）
> 6. 有 Web 界面（Streamlit）
>
> **技术选型**（二选一）：
> - 纯 API + 手动工具调用（更接近原理）
> - LangChain/LangGraph（更工程化）
>
> **提交内容**：
> - 完整可运行代码
> - README 说明文档
> - 5分钟演示视频或截图

---

# 第8周：综合项目

---

## 第1课：AI 设计助手项目

### 一、学习目标

- 综合运用所有学过的技术完成一个大型项目
- 理解从需求到交付的完整流程
- 能够将 AI 能力与实际专业结合

### 二、项目概述

> 🎯 **项目**：AI 设计助手
>
> **核心功能**：用户输入一个设计需求（如"设计一个现代风格咖啡馆"），AI 自动生成：
> 1. 完整设计方案文档
> 2. 概念图描述（用于 AI 图片生成）
> 3. PPT 演示文稿大纲
> 4. 预算估算表
> 5. 时间计划表
>
> **技术栈**：Python + Streamlit + LLM API + 多工具协作

### 三、实操环节（60分钟）

#### 项目架构设计

```
用户输入需求
    ↓
需求分析 Agent → 拆解需求，明确设计方向
    ↓
    ├──→ 方案撰写 Agent → 生成详细设计方案
    ├──→ 视觉设计 Agent → 生成概念图 Prompt
    ├──→ PPT 生成 Agent → 生成演示文稿大纲
    └──→ 预算估算 Agent → 计算成本和时间
    ↓
汇总输出 → 一份完整的设计方案包
```

#### 项目骨架代码

```python
# ai_design_assistant.py
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# ===== 初始化 =====
st.set_page_config(page_title="AI设计助手", page_icon="🎨", layout="wide")
st.title("🎨 AI 设计助手")
st.caption("输入你的设计需求，AI 自动生成完整方案")

# ===== 侧边栏 =====
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("API Key", type="password")
    design_type = st.selectbox("设计类型", [
        "室内空间设计", "产品外观设计", "UI/UX设计", 
        "景观设计", "建筑设计概念", "其他"
    ])
    
    output_options = st.multiselect(
        "输出内容",
        ["设计方案文档", "概念图Prompt", "PPT大纲", "预算估算", "时间计划"],
        default=["设计方案文档", "概念图Prompt", "PPT大纲", "预算估算"]
    )

# ===== 主界面 =====
st.markdown("### 📝 输入设计需求")

col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("项目名称", placeholder="例如：现代风格大学城咖啡馆")
    target_users = st.text_input("目标用户", placeholder="例如：大学生、年轻教师")
with col2:
    area = st.text_input("面积/规模", placeholder="例如：200平米")
    budget = st.text_input("预算范围", placeholder="例如：50万元")

style = st.text_area("风格要求", placeholder="例如：现代简约、工业风、融入自然元素...")
special_requirements = st.text_area("特殊需求", placeholder="例如：需要有自习区、小型演出空间...")

# ===== AI 生成 =====
if st.button("🚀 生成方案", type="primary", use_container_width=True):
    if not api_key:
        st.error("请先输入 API Key")
    else:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        # 构建详细的需求描述
        requirement = f"""
项目名称：{project_name}
设计类型：{design_type}
目标用户：{target_users}
面积/规模：{area}
预算范围：{budget}
风格要求：{style}
特殊需求：{special_requirements}
"""
        
        # ===== 并行生成各部分 =====
        tabs = st.tabs([opt for opt in output_options])
        
        for tab, option in zip(tabs, output_options):
            with tab:
                with st.spinner(f"正在生成{option}..."):
                    if option == "设计方案文档":
                        prompt = generate_design_doc_prompt(requirement)
                    elif option == "概念图Prompt":
                        prompt = generate_image_prompt(requirement)
                    elif option == "PPT大纲":
                        prompt = generate_ppt_prompt(requirement)
                    elif option == "预算估算":
                        prompt = generate_budget_prompt(requirement)
                    elif option == "时间计划":
                        prompt = generate_timeline_prompt(requirement)
                    
                    stream = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "你是资深设计顾问，请给出专业、详细、可落地的方案"},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True,
                        temperature=0.7,
                        max_tokens=3000
                    )
                    
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
        
        # ===== 导出按钮 =====
        st.markdown("---")
        st.success("✅ 方案生成完成！")
        
        # 生成完整方案文本用于导出
        export_text = f"# {project_name} - 完整设计方案\n\n"
        export_text += f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
        export_text += full_response
        
        st.download_button(
            "📥 下载完整方案（Markdown）",
            export_text,
            f"{project_name}_设计方案.md",
            "text/markdown"
        )

# ===== Prompt 生成函数 =====
def generate_design_doc_prompt(requirement):
    return f"""作为资深{requirement.split(chr(10))[1].split('：')[1]}设计师，请为以下项目撰写详细设计方案：

{requirement}

请按以下结构撰写：

## 一、项目概述
- 项目定位
- 设计理念
- 核心设计关键词

## 二、空间/功能布局
- 功能分区规划
- 动线设计
- 各区域详细描述

## 三、风格与美学
- 整体风格定位
- 色彩方案
- 材料选择建议
- 灯光设计

## 四、用户体验设计
- 用户旅程地图
- 服务流程设计
- 细节体验设计

## 五、技术实现要点
- 结构要点
- 材料建议
- 设备配置建议

请确保方案专业、具体、可落地，避免空泛的描述。每个部分都要有具体的尺寸、数量、材料名称等细节。"""

def generate_image_prompt(requirement):
    return f"""请为以下设计项目生成5个不同角度的AI图像生成Prompt（用于Midjourney/DALL-E）：

{requirement}

要求：
1. 每个Prompt包含：视角、风格、色彩、光线、构图、细节
2. Prompt使用英文（因为AI图像工具对英文支持更好）
3. 覆盖以下视角：整体空间、细节特写、氛围场景、功能区域、材质纹理
4. 每个Prompt标注适合的工具（Midjourney / DALL-E）

格式：
### Prompt 1：整体空间视角（推荐工具：Midjourney）
[英文Prompt]

### Prompt 2：细节特写（推荐工具：DALL-E）
[英文Prompt]
..."""

def generate_ppt_prompt(requirement):
    return f"""请为以下设计项目生成PPT演示文稿大纲：

{requirement}

要求：
- 总共12-15页
- 每页包含：标题 + 3-5个要点 + 建议配图类型
- 整体叙事逻辑：问题 → 方案 → 亮点 → 落地计划
- 适合向客户/领导汇报"""

def generate_budget_prompt(requirement):
    return f"""请为以下设计项目生成详细的预算估算：

{requirement}

请按以下类别估算：
1. 硬装费用（材料+施工）
2. 软装费用（家具+装饰）
3. 设备费用（电器+IT设备）
4. 设计费用
5. 预留金（10-15%）

用表格形式输出，每项包含：项目、数量、单价、小计
最后给出总预算和预算控制建议。"""

def generate_timeline_prompt(requirement):
    return f"""请为以下设计项目生成实施时间计划：

{requirement}

请包含：
1. 设计阶段（概念→方案→施工图）
2. 施工准备（招标/采购）
3. 施工阶段（拆除→水电→泥木→油漆→安装）
4. 软装阶段
5. 验收与试运营

用甘特图文字描述形式输出，标注关键里程碑和前置条件。"""
```

### 四、课后任务

1. 完成 AI 设计助手的完整开发并运行
2. 用你自己的专业场景做个性化改造
3. 准备最终项目答辩的 PPT

---

## 第2课：多 Agent 协作

### 一、学习目标

- 理解多 Agent 协作的常见模式
- 理解每个 Agent 的职责边界设计
- 了解多 Agent 系统的优势和挑战

### 二、核心知识点

#### 2.1 多 Agent 协作模式

```
模式1：顺序协作（Pipeline）
  Agent A → Agent B → Agent C → 最终输出
  例：撰写 → 审核 → 润色 → 发布

模式2：监督式协作（Supervisor）
          ┌→ Agent A
  Supervisor ─┼→ Agent B
          └→ Agent C
  Supervisor 分配任务，汇总结果

模式3：辩论式（Debate）
  Agent A ─┐
           ├→ 讨论/辩论 → 达成共识
  Agent B ─┘

模式4：分层式（Hierarchical）
  协调者 Agent
    ├→ 子Agent 1
    │   ├→ 工具A
    │   └→ 工具B
    └→ 子Agent 2
        ├→ 工具C
        └→ 工具D
```

#### 2.2 多 Agent vs 单 Agent

| 维度 | 单 Agent | 多 Agent |
|------|----------|----------|
| **复杂度** | 低 | 高 |
| **可控性** | 强 | 需要设计协调机制 |
| **适合场景** | 单一明确的任务 | 需要多角色协作的复杂任务 |
| **成本** | 低（一次调用） | 高（多次调用+协调） |
| **调试难度** | 低 | 高（需要追踪多Agent交互） |

> ⚠️ **原则**：能用单 Agent 解决的，不要用多 Agent！

#### 2.3 一个实际的多 Agent 案例：软件开发的 Agent 团队

```
产品经理 Agent：
  输入：用户需求描述
  输出：产品需求文档（PRD）

设计 Agent：
  输入：PRD
  输出：UI/UX 设计方案

程序员 Agent：
  输入：PRD + 设计方案
  输出：代码实现

测试 Agent：
  输入：PRD + 代码
  输出：测试报告和 Bug 列表
```

### 三、实操环节（60分钟）

#### 多 Agent 写作系统

```python
# multi_agent_writer.py
# 演示：研究 → 撰写 → 审核 → 修改 的多Agent协作

from openai import OpenAI
import json

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

def create_agent(role, system_prompt):
    """创建 Agent 工厂函数"""
    def agent(input_text):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    return agent

# === 定义各 Agent ===

researcher = create_agent(
    "研究者",
    """你是一位资深研究员。你的任务是：
1. 针对给定主题，收集整理关键信息和数据
2. 列出重要的观点和论据
3. 区分已确认的事实和有争议的观点
4. 用结构化方式输出，便于后续使用

输出格式：
### 核心数据与事实
### 主要观点
### 争议与不同意见
### 推荐论述方向"""
)

writer = create_agent(
    "撰写者",
    """你是一位专业写作者。你的任务是：
1. 根据研究资料，撰写一篇完整的文章
2. 文章结构清晰，逻辑严密
3. 语言生动有趣，适合大众阅读
4. 保留关键数据和引用来源

文章结构：
- 引言（吸引读者兴趣）
- 正文（3-4个核心论点）
- 结论（总结+展望）"""
)

reviewer = create_agent(
    "审核者",
    """你是一位严格的编辑。你的任务是：
1. 审核文章的质量
2. 检查事实准确性
3. 评估逻辑严密性
4. 提出具体修改建议

输出格式：
### 总体评价（1-10分）
### 优点
### 需要改进的地方（具体指出位置和问题）
### 修改建议（按优先级排序）"""
)

reviser = create_agent(
    "修改者",
    """你是一位精益求精的编辑。你的任务是：
1. 根据审核意见修改文章
2. 保持原文优点
3. 改进所有被指出的问题
4. 最后做一次语言润色
输出修改后的完整文章。"""
)

# === 多 Agent 协作流程 ===
def multi_agent_write(topic):
    """多 Agent 协作写作"""
    
    print("=" * 60)
    print(f"  多Agent协作写作：{topic}")
    print("=" * 60)
    
    # Step 1: 研究
    print("\n🔍 [研究者 Agent] 正在收集资料...")
    research_result = researcher(f"请研究以下主题：{topic}")
    print("✅ 研究完成")
    print(research_result[:200] + "...\n")
    
    # Step 2: 撰写
    print("✍️ [撰写者 Agent] 正在撰写文章...")
    draft = writer(f"""请根据以下研究资料撰写文章：

研究资料：
{research_result}

写作主题：{topic}
目标读者：普通大众
文章长度：800-1000字""")
    print("✅ 初稿完成\n")
    
    # Step 3: 审核
    print("🔍 [审核者 Agent] 正在审核文章...")
    review_result = reviewer(f"""请审核以下文章：

主题：{topic}

文章内容：
{draft}""")
    print("✅ 审核完成")
    print(review_result[:200] + "...\n")
    
    # Step 4: 修改
    print("📝 [修改者 Agent] 正在根据审核意见修改...")
    final = reviser(f"""请根据审核意见修改文章：

## 审核意见
{review_result}

## 原文
{draft}

请输出修改后的完整文章。""")
    print("✅ 终稿完成\n")
    
    return {
        "research": research_result,
        "draft": draft,
        "review": review_result,
        "final": final
    }

# === 运行 ===
topic = "人工智能对未来工程设计教育的影响"
result = multi_agent_write(topic)

print("=" * 60)
print("  📄 最终文章")
print("=" * 60)
print(result["final"])
```

### 四、课后任务

1. 理解上述多 Agent 代码，尝试添加一个"总结者 Agent"来生成文章摘要
2. 思考：多 Agent 系统在实际项目中可能遇到什么问题？（至少列出3个）
3. 阅读：[Claude Code Subagents 文档](https://code.claude.com/docs/en/sub-agents)

---

## 第3课：项目答辩

### 一、学习目标

- 综合展示 8 周学习成果
- 锻炼项目展示和技术表达能力
- 获得同伴和教师的反馈

### 二、答辩要求

#### 2.1 项目要求

必须包含以下至少 **3 项**技术要素：

| 技术要素 | 体现方式 |
|----------|----------|
| LLM API 调用 | 使用至少一个 LLM 平台 |
| Prompt Engineering | 有结构化的 System Prompt |
| RAG | 有知识库检索功能 |
| Tool Calling | Agent 能调用至少 2 个工具 |
| Web 界面 | 用 Streamlit/Gradio 构建界面 |
| 流式输出 | 支持流式返回 |
| 多轮对话 | 有对话历史管理 |
| 结构化输出 | 模型输出 JSON 等结构化数据 |

#### 2.2 答辩流程（每人 8-10 分钟）

| 环节 | 时间 | 内容 |
|------|------|------|
| **项目演示** | 3 分钟 | 现场展示项目功能 |
| **技术讲解** | 3 分钟 | 讲解架构、技术选型、核心代码 |
| **Q&A** | 2 分钟 | 回答教师和同学的提问 |

#### 2.3 评分标准

| 评分维度 | 权重 | 评分标准 |
|----------|------|----------|
| **项目完成度** | 30% | 功能是否完整、能否正常运行 |
| **技术运用** | 25% | 使用了哪些技术、技术深度如何 |
| **创新性** | 20% | 项目创意、与专业的结合度 |
| **代码质量** | 15% | 代码结构、注释、可维护性 |
| **展示表达** | 10% | 表达清晰度、Q&A 表现 |

### 三、项目选题参考

| 方向 | 项目示例 | 技术要点 |
|------|----------|----------|
| **学习助手** | AI 智能刷题系统 | RAG + API + Streamlit |
| **设计助手** | AI 室内设计助手 | 多 Agent + Prompt Engineering |
| **办公助手** | AI 会议纪要+待办管理 | Tool Calling + RAG |
| **知识管理** | 个人知识库问答 | RAG + Embedding |
| **创意工具** | AI 文案生成器 | Structured Output + API |
| **数据分析** | AI 数据解读助手 | API + Pandas + 可视化 |
| **代码助手** | AI 代码审查工具 | API + MCP |
| **生活助手** | 校园生活 AI 助手 | Agent + Tool Calling + Memory |

### 四、答辩准备清单

**技术准备**：
- [ ] 代码在 GitHub 上可访问（或打包提交）
- [ ] README 文档完整（如何运行、配置、扩展）
- [ ] 项目能在本地正常运行
- [ ] 准备好演示用的 API Key（注意不要提交到代码仓库）

**演示准备**：
- [ ] 准备 3-5 个演示用的输入样例
- [ ] 知道每个功能在代码中的对应位置
- [ ] 准备解释 1-2 个技术难点如何解决
- [ ] 准备 1 个"如果时间更多，你会怎么改进"的回答

**PPT 准备（可选但建议准备）**：
1. 项目背景 — 为什么要做这个项目
2. 功能演示 — 截图/动图
3. 技术架构 — 一张图说清楚
4. 核心代码 — 2-3 个关键代码片段
5. 项目心得 — 最大的收获
6. 未来计划 — 还想做什么改进

---

# 附录

## 附录A：常用资源索引

### AI 工具平台

| 工具 | 网址 | 说明 |
|------|------|------|
| ChatGPT | https://chatgpt.com | OpenAI 出品，综合能力最强 |
| Claude | https://claude.ai | Anthropic 出品，长文本分析突出 |
| Gemini | https://gemini.google.com | Google 出品，多模态能力强 |
| DeepSeek | https://chat.deepseek.com | 性价比高，中文好 |
| 通义千问 | https://tongyi.aliyun.com | 阿里出品，中文理解好 |
| Kimi | https://kimi.moonshot.cn | 月之暗面出品，长文本好 |
| Perplexity | https://www.perplexity.ai | AI 搜索引擎，带引用 |

### Python 学习

| 资源 | 链接 | 说明 |
|------|------|------|
| Python官方教程 | https://docs.python.org/zh-cn/3/tutorial/ | 官方中文教程 |
| Python-100-Days | https://github.com/jackfrued/Python-100-Days | GitHub 热门教程 |
| 廖雪峰Python | https://www.liaoxuefeng.com | 经典中文教程 |

### 机器学习

| 资源 | 链接 | 说明 |
|------|------|------|
| 吴恩达 ML 课程 | https://www.coursera.org/learn/machine-learning | 最佳入门课程 |
| Scikit-learn 文档 | https://scikit-learn.org/stable/ | 官方文档 |
| Kaggle | https://www.kaggle.com | ML 竞赛平台 |
| Datawhale | https://github.com/datawhalechina | 中文学习社区 |

### 深度学习

| 资源 | 链接 | 说明 |
|------|------|------|
| 吴恩达 DL 课程 | https://www.coursera.org/specializations/deep-learning | 系统学习 DL |
| TensorFlow 教程 | https://www.tensorflow.org/tutorials | 官方教程 |
| PyTorch 教程 | https://pytorch.org/tutorials/ | 官方教程 |
| 动手学深度学习 | https://d2l.ai | 李沐出品，强烈推荐 |

### Agent 开发

| 资源 | 链接 | 说明 |
|------|------|------|
| hello-agents | https://github.com/datawhalechina/hello-agents | 中文 Agent 教程 |
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Anthropic 官方 Agent 设计指南 |
| Claude Code 文档 | https://code.claude.com/docs/en/overview | Claude Code 官方文档 |
| learn-claude-code | https://github.com/shareAI-lab/learn-claude-code | 从零实现 Agent harness |
| LangChain 文档 | https://docs.langchain.com | LangChain 官方文档 |
| LangGraph 文档 | https://langchain-ai.github.io/langgraph/ | LangGraph 官方文档 |
| MCP 官方文档 | https://modelcontextprotocol.io | MCP 协议 |
| Agent-Learning-Hub | 本仓库 `Agent-Learning-Hub/` | Agent 学习资源合集 |

---

## 附录B：常见问题 FAQ

**Q1：我是完全的零基础，能跟上这个课程吗？**
A：能。这个课程就是为零基础设计的。第1周不需要写代码，第2周才从 Python 基础开始。跟着节奏来，不会掉队。

**Q2：我需要准备什么环境？**
A：一台能上网的电脑即可。第2周开始需要安装 Anaconda + Jupyter Notebook（免费），第6周需要 API Key（推荐 DeepSeek，新用户有免费额度）。

**Q3：课程中的 API 调用需要花钱吗？**
A：课程用 DeepSeek API 做主要演示（注册送免费额度，足够课程使用）。国内可用，无需科学上网，价格非常低（约 ¥1/100万 Tokens）。

**Q4：遇到错误代码怎么办？**
A：这是学习的一部分！把错误信息复制给 ChatGPT/Claude/DeepSeek，AI 会帮你分析原因并给出解决方案。这也是在锻炼你"用 AI 解决问题"的能力。

**Q5：8周学完能达到什么水平？**
A：能够熟练使用各种 AI 工具；理解 AI 的核心原理；能用 Python 调用 LLM API；能独立开发简单的 AI Agent 应用。但离 AI 算法工程师还有很大差距——那需要更深入的数学和计算机基础。

**Q6：学完这个课程后，下一步学什么？**
A：
- 深入方向1：系统学习机器学习/深度学习（吴恩达课程 + 《动手学深度学习》）
- 深入方向2：Agent 工程化（LangGraph、MCP、A2A 深入、Agent 评测）
- 深入方向3：AI 应用全栈（前端 + 后端 + 数据库 + 部署）

---

## 附录C：版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| V1.0 | 2026-07-26 | 初始版本：8周完整课程大纲 + 24节课详细讲义 |
