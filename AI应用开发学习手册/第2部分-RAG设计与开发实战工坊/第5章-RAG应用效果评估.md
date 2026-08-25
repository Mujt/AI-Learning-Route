# 第 5 章 RAG 应用效果评估

## 学习目标

- 理解 RAG 评估的必要性与评估体系设计
- 掌握 RAG 核心评估指标（忠实度 / 答案相关性 / 上下文相关性 / 上下文召回率）
- 掌握 Ragas、Trulens 等评估框架的使用
- 建立"评估 → 定位 → 优化"的闭环方法论

---

## 5.1 为什么必须评估 RAG

- **凭感觉优化不可靠**：一个 Prompt 改动可能让 30% 的问题变好、20% 变差，必须量化。
- **上线前风控**：企业场景错误回答可能造成经济损失或合规风险。
- **持续迭代基线**：每次优化都应与上一版本对比，防止"优化回归"。
- **指标体系统一语言**：让算法、产品、测试团队在同一标准下协作。

## 5.2 RAG 评估体系设计

RAG 系统由**检索（Retrieval）**与**生成（Generation）**两段组成，评估应分段进行：

```
┌───────────── 检索质量 ─────────────┐
│  上下文相关性（Context Relevancy）  │
│  上下文召回率（Context Recall）     │
│  上下文精确率（Context Precision）  │
├───────────── 生成质量 ─────────────┤
│  忠实度（Faithfulness）            │
│  答案相关性（Answer Relevancy）     │
│  答案正确性（Correctness）          │
└────────────────────────────────────┘
```

### 5.2.1 四大核心指标详解

| 指标 | 定义 | 评估对象 | 测量方法 |
|------|------|----------|----------|
| **忠实度（Faithfulness）** | 答案是否严格基于检索上下文，无编造 | 生成 | LLM 将答案拆成声明，逐一判断上下文是否支持 |
| **答案相关性（Answer Relevancy）** | 答案是否切题、完整 | 生成 | 反向提问法：由答案生成问题，与原始问题算相似度 |
| **上下文相关性（Context Relevancy）** | 检索到的片段与问题的相关程度 | 检索 | 统计片段中与问题相关的句子占比 |
| **上下文召回率（Context Recall）** | 标准答案中的关键信息是否被检索覆盖 | 检索 | 标准答案句子能否在上下文中找到依据 |

> 关键认知：**忠实度是 RAG 的"安全指标"**（防止幻觉），**召回率是"能力指标"**（防止漏检），两者必须同时监控。

### 5.2.2 评估数据准备

1. **构建测试集**：从真实用户问题中采样 50-200 条，覆盖不同主题/难度。
2. **人工标注**：为每个问题标注标准答案（Gold Answer）。
3. **LLM-as-Judge**：用更强模型（GPT-4/Claude/Qwen-Max）自动打分，与人工标注一致性达 80%+ 即可规模化。

## 5.3 Ragas 评估框架

### 5.3.1 什么是 Ragas

Ragas（Retrieval-Augmented Generation Assessment）是**专为 RAG 设计的开源评估库**，用 LLM 自动计算上述指标，无需人工逐条评分。

### 5.3.2 快速上手

```python
# pip install ragas
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy,
    context_precision, context_recall
)

# 构造评估数据集（每条含 question / answer / contexts / ground_truth）
dataset = Dataset.from_dict({
    "question": ["公司的年假政策是什么？", "产品支持哪些支付方式？"],
    "answer": ["工作满一年享 5 天年假...", "支持微信、支付宝..."],
    "contexts": [["年假政策：满一年5天..."], ["支付方式：微信/支付宝/银联..."]],
    "ground_truth": ["工作满一年享有5天带薪年假", "支持微信、支付宝、银联"],
})

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy,
             context_precision, context_recall],
)
print(result)   # 输出各指标分数（0-1）
```

### 5.3.3 Ragas 测试集生成

Ragas 还能**自动生成测试集**（基于知识库合成问题），解决"没有标注数据"的冷启动问题：

```python
from ragas.testset.generator import TestsetGenerator

generator = TestsetGenerator.from_default(
    llm=eval_llm, embedding_model=embed_model)
testset = generator.generate_with_langchain_docs(
    documents, testset_size=50)
```

### 5.3.4 指标解读与优化方向

| 指标偏低 | 说明 | 优先排查 |
|----------|------|----------|
| 忠实度 < 0.7 | 答案在编造 | 提示词约束、上下文压缩、切分质量 |
| 上下文召回率 < 0.6 | 关键信息没检索到 | K 值、混合检索、查询改写、Embedding |
| 上下文相关性 < 0.5 | 检索混入噪声 | 重排序、相似度阈值、元数据过滤 |
| 答案相关性 < 0.7 | 答非所问/不完整 | 提示词、多查询、生成温度 |

## 5.4 Trulens 等其他评估工具

### 5.4.1 Trulens

- 优势：**基于反馈函数的可组合评估**，可与 LangChain/LlamaIndex 应用直接接插件式评估。
- 特点：提供 RAG 三件套（Context Relevance / Groundedness / Answer Relevance）与多模态反馈、LLM 对抗评估。
- 支持 TruLens 云与本地；OpenAI 等模型的免费/付费反馈函数丰富。

```python
# pip install trulens-eval trulens-providers-openai
from trulens_eval import Feedback, Tru, TruLlama
from trulens_eval.feedback import Groundedness, OpenAI as fOpenAI

grounded = Groundedness(groundedness_provider=provider)
f_groundedness = Feedback(grounded.groundedness_measure_with_cot_reasons).on(
    TruLlama.select_source_nodes().str[:1000]).on_output()
```

### 5.4.2 其他工具

| 工具 | 特点 |
|------|------|
| LangSmith | 追踪 + 离线评估 + 在线监控一体 |
| DeepEval | 开源，指标丰富（偏置、毒性、幻觉） |
| RAGChecker | 专攻 RAG 的细粒度诊断（检索、证据链） |
| Phoenix / Arize | 可观测性 + 评估可视化 |

## 5.5 RAG 评估应用实战（闭环方法论）

```
① 建测试集（50-100 条真实问题 + 标准答案）
        ↓
② 运行评估（Ragas 四指标 + 人工抽检 10 条）
        ↓
③ 定位短板（忠实度？召回率？相关性？）
        ↓
④ 针对性优化（见第4章策略矩阵）
        ↓
⑤ 回归对比（同测试集重跑，指标↑ 且无回退）
        ↓
⑥ 沉淀基线（记录配置快照，形成版本库）
```

**实战建议**：
- 每次改动只改一个变量（如只换 Embedding 或只加重排），避免无法归因。
- 保存所有版本配置（chunk_size、K 值、权重、模型）为 JSON 快照。
- 生产环境接入在线评估（LangSmith/Phoenix），监控线上波动。

---

## 高质量博客推荐

1. **RAG 评估框架实战：Ragas 全指标详解** — [CSDN](https://blog.csdn.net/m0_62283830/article/details/143505026)
   逐个指标原理 + 代码实现，中文环境可复现。
2. **RAGAS 四维评估指标深度解读** — [smallyoung 博客](https://smallyoung.gitbook.io/rag/rag-2)
   从数学定义到业务解读，理解指标背后的含义。
3. **RAG 应用效果评估体系：从人工到 LLM-as-Judge** — [微信公众号](https://mp.weixin.qq.com/s/7s3xTlKtT5vQ-CJp2gNjig)
   企业级评估体系建设方法论，含评估数据治理。
4. **Trulens 官方文档（中文教程）** — [Trulens Docs](https://www.trulens.org/getting_started/)
   反馈函数与 RAG 三件套的完整用法。
5. **RAG 评估指标梳理：Retrieval 与 Generation 双维度** — [知乎专栏](https://zhuanlan.zhihu.com/p/672469127)
   常用指标汇总与公式对照表，便于快速查阅。

## 动手实践

1. 用 Ragas 评估你上一章的 RAG 系统，记录四个指标。
2. 人为制造"故障"（如切分过大、去掉重排），观察指标如何变化，建立敏感性认知。
3. 用 Ragas TestsetGenerator 生成 30 条测试问题，人工校验其质量。
4. 搭建"改一个变量 → 重跑 → 对比"的迭代实验流程，跑 3 轮优化。

## 常见问题（FAQ）

**Q1：LLM 评估（LLM-as-Judge）可信吗？**
A：与人类判断一致性约 80-90%。建议用强模型（GPT-4/Qwen-Max）评判，并定期人工抽检校准；有争议样本进入人工仲裁。

**Q2：指标要跑到多少才算及格？**
A：行业经验参考：忠实度 >0.75，上下文召回率 >0.6，上下文相关性 >0.5，答案相关性 >0.7。具体以业务容忍度为准。

**Q3：评估一次要花多少钱？**
A：50 条测试集 + 四指标，用闭源 API 评估成本约几十到几百元人民币。建议用国产强模型（Qwen-Max/DeepSeek）做 Judge 降本。
