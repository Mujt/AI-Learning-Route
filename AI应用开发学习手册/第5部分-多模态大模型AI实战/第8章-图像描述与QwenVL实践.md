# 第 8 章 图像描述与 Qwen-VL 模型项目实践

## 学习目标

- 理解图像描述（Image Captioning）任务与评估
- 掌握经典模型：Show and Tell、Show Attend and Tell
- 掌握 Qwen-VL 系列模型的架构与能力
- 完成基于 Qwen-VL 的多模态项目实践

---

## 8.1 图像描述任务概述

### 8.1.1 任务定义

**图像描述（Image Captioning）**：给定一张图像，自动生成描述其内容的自然语言句子。

```
输入：一张"猫坐在沙发上"的图片
输出："A cat is sitting on a sofa."（一只猫坐在沙发上）
```

### 8.1.2 任务难点

- 需要**视觉理解**（识别物体、属性、关系）+ **语言生成**（组织成通顺句子）的双重能力。
- 细粒度：颜色、数量、位置、动作、语义关系。
- 与 VQA（视觉问答）的区别：Captioning 是开放式生成，VQA 是问答。

### 8.1.3 常用数据集与评估

| 数据集 | 规模 | 说明 |
|--------|------|------|
| MS COCO Caption | 33 万张 / 每张 5 句 | 最常用基准 |
| Flickr30k | 3 万张 | 经典数据集 |
| TextCaps | 2.8 万张 | 场景文字描述 |

**评估指标**：BLEU、METEOR、ROUGE、CIDEr（COCO 官方首选，与人工相关性最高）、SPICE（语义）。

## 8.2 经典图像描述模型

### 8.2.1 Show and Tell（2015）

**架构**：CNN（编码）+ RNN/LSTM（解码）——最简单的"编码器-解码器"范式：

```
图像 → CNN（VGG/ResNet）→ 图像特征向量 → LSTM 逐词生成句子
```

- 用最后一个 CNN 特征作为 LSTM 的初始状态。
- 局限：单向量压缩整张图，无法定位"描述时在看哪里"。

### 8.2.2 Show, Attend and Tell（2016）

**创新：空间注意力（Spatial Attention）**——解码每个词时动态聚焦图像的**特定区域**：

```
图像 → CNN 卷积特征图（14×14×512，保留空间位置）
                    │
          [注意力机制：当前词对 196 个区域加权]
                    ▼
        加权求和 → 上下文向量 → 送入 LSTM
```

**核心公式（Bahdanau 风格）**：

```
e_ti = f(h_(t-1), a_i)            # 计算第 i 区域与当前解码状态的相关性
α_ti = softmax(e_ti)              # 归一化成注意力权重
z_t = Σ α_ti · a_i                # 加权上下文向量（"注意力聚焦"）
```

**效果**：比 Show and Tell 提升 BLEU/CIDEr，且**注意力可视化**显示模型确实"看图说话"（描述猫时聚焦猫的区域）。

```python
# 注意力可视化的意义：可解释性——能画出"模型生成每个词时看哪里"
# 热力图叠加到原图上：白色=高关注区域
```

### 8.2.3 从经典到现代

```
Show and Tell → Show Attend and Tell → 
Bottom-Up Attention（目标检测提区域特征）→ 
Transformer（图像区域 + 文本序列统一注意力）→ 
VLM 时代（Qwen-VL：视觉编码 + LLM 统一生成）
```

## 8.3 Qwen-VL 模型介绍

### 8.3.1 模型系列

Qwen-VL 是阿里通义千问的**视觉语言模型**系列，开源且持续迭代：

| 版本 | 特点 |
|------|------|
| Qwen-VL / Qwen-VL-Chat | 初代，图文对话 |
| Qwen2-VL | 原生动态分辨率、视频理解、物体定位 |
| **Qwen2.5-VL** | 更强推理、文档解析、GUI 智能体、视觉定位 |
| Qwen3-VL | 推理增强（思考模式）、更强多模态 |

### 8.3.2 核心架构（Qwen2-VL 起）

```
图像 → 视觉编码器（ViT，SigLIP 类）
     → 投影层（MLP 适配器）
     → LLM 主干（Qwen2.5，视觉 Token 与文本 Token 统一处理）
```

**关键创新**：
1. **原生动态分辨率（NaViT）**：任意长宽比与分辨率，无需裁剪缩放，细节保留好。
2. **M-RoPE（多模态旋转位置编码）**：用一组 RoPE 统一建模文本（1D）、图像（2D）、视频（3D）的位置。
3. **多图与视频输入**：支持多图对比、视频帧序列。
4. **物体定位**：输出边界框坐标（相对坐标），可做"圈出图中物体"。
5. **OCR/文档理解**：密集文字识别能力强。

### 8.3.3 能力矩阵

| 能力 | 示例 |
|------|------|
| 图像描述 | 描述图片内容、场景、人物动作 |
| 视觉问答 | "图中有几个人？" |
| 文档/图表理解 | 解析 PDF、表格、图表并回答 |
| OCR | 提取图像中文字 |
| 定位 | 圈出指定物体位置 |
| 多图推理 | 对比两张图的差异 |
| 视频理解 | 视频内容问答（Qwen2.5-VL 支持） |

## 8.4 Qwen-VL 实践项目

### 8.4.1 本地部署推理

```bash
# transformers 方式
pip install "transformers>=4.44" torch accelerate qwen-vl-utils
```

```python
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct",
    torch_dtype=torch.bfloat16, device_map="auto")
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

messages = [{"role": "user", "content": [
    {"type": "image", "image": "cat.jpg"},
    {"type": "text", "text": "请详细描述这张图片的内容。"},
]}]

text = processor.apply_chat_template(messages, tokenize=False,
                                     add_generation_prompt=True)
inputs = process_vision_info(messages)
batch = processor(text=[text], images=inputs[0], videos=inputs[1],
                  padding=True, return_tensors="pt")
out = model.generate(**batch, max_new_tokens=256)
print(processor.decode(out[0], skip_special_tokens=True))
```

### 8.4.2 项目实战：通用视觉助手（Streamlit）

```python
# app.py —— 图片上传 → 问答/描述/OCR
import streamlit as st
# （模型加载与生成逻辑同上）

st.title("多模态视觉助手")
mode = st.radio("选择任务", ["图像描述", "视觉问答", "OCR 提取"])
img = st.file_uploader("上传图片", type=["jpg", "png"])

if img and st.button("开始"):
    # 组装 messages（根据 mode 构造不同提示）
    answer = run_qwen_vl(img_bytes, prompt_by_mode(mode))
    st.image(img, caption="上传图片")
    st.write(answer)
```

### 8.4.3 与 RAG/Agent 结合（多模态应用范式）

| 集成方式 | 场景 |
|----------|------|
| 多模态 RAG | 图文档知识库：图片检索 + 视觉理解回答 |
| 视觉 Agent | 读图 → 决策 → 调用工具（GUI 操作） |
| 文档智能体 | 扫描件解析 → 表格提取 → 结构化入库 |
| 质检助手 | 产品图片 → 缺陷识别 → 生成报告 |

### 8.4.4 模型选型建议

| 资源/需求 | 推荐 |
|-----------|------|
| API 快速开发 | Qwen-VL-Max / Qwen3-VL API（阿里百炼） |
| 本地部署 24G | Qwen2.5-VL-7B（INT4 约 8-12G） |
| 本地部署 48G+ | Qwen2.5-VL-32B |
| 推理要求高 | Qwen3-VL-30B / 235B（API） |
| 边缘 | Qwen2-VL-2B |

---

## 高质量博客推荐

1. **Show, Attend and Tell 论文精读：图像描述经典之作** — [CSDN](https://blog.csdn.net/u010666669/article/details/118837669)
   空间注意力机制详解与可视化。
2. **图像描述生成入门：从 Show and Tell 到 Transformer** — [知乎专栏](https://zhuanlan.zhihu.com/p/662738559)
   技术演进与数据集评估体系。
3. **Qwen-VL 系列多模态大模型详解** — [CSDN](https://blog.csdn.net/m0_61066945/article/details/147875245)
   架构、动态分辨率、M-RoPE 与能力矩阵。
4. **Qwen2.5-VL 官方文档（模型卡）** — [Qwen 官方](https://qwenlm.github.io/blog/qwen2.5-vl/)
   能力、评测、示例代码的权威来源。
5. **使用 Qwen-VL 构建多模态 RAG 实战** — [微信公众号](https://mp.weixin.qq.com/s/8qZ4h7wQvFmJTb3yFkpHxw)
   图文档知识库的落地实践。

## 动手实践

1. 用 Qwen2.5-VL 对 5 张不同类型图片（风景/表格/票据/人脸/截图）提问，记录能力边界。
2. 用 transformers 实现图片 OCR 提取，与 Tesseract 对比效果。
3. 构建"多模态 RAG"：10 张含文字的图片 → 检索 → 视觉理解回答。
4. 测试 Qwen-VL 的定位能力：让它输出图片中物体的坐标框。

## 常见问题（FAQ）

**Q1：Qwen-VL 和 GPT-4o/Gemini 差距大吗？**
A：整体接近，部分能力（中文场景、OCR、开源可控）有优势；复杂推理与极端场景略逊顶级闭源。开源+可私有化是核心价值。

**Q2：图像描述和 VQA 用什么模型最好？**
A：通用任务直接用 Qwen-VL/GPT-4o 等 VLM 即可；需要实时低延迟用 2B-7B 量化模型；特殊领域（医学影像）建议微调。

**Q3：图像描述评估为什么用 CIDEr？**
A：CIDEr 基于 TF-IDF 加权的 n-gram 相似度，对"信息量"更敏感，与人工判断的相关性高于 BLEU。
