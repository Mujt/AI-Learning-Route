# 第 4 章 经典 Transformer 架构解析

## 学习目标

- 理解 Transformer 整体架构（编码器-解码器）
- 掌握 Embedding 与位置编码
- 深入理解自注意力机制与前馈网络
- 掌握残差连接与层归一化
- 用 PyTorch 实现一个可训练的 Transformer

---

## 4.1 Transformer 整体架构

Transformer 由 Google 在 2017 年提出（*Attention Is All You Need*），完全抛弃循环结构，用**注意力机制**建模序列，成为大模型时代的基石。

```
┌─────────────── 编码器（Encoder）×N ───────────────┐
│ 输入Embedding → 位置编码 → [多头自注意力 + 残差+LN]  │
│                             → [FFN + 残差+LN]      │
└───────────────────────────────────────────────────┘
                      │ 输出编码表示
┌─────────────── 解码器（Decoder）×N ───────────────┐
│ 输出Embedding → 位置编码 → [掩码多头自注意力 + 残差+LN]│
│                        → [交叉注意力 + 残差+LN]     │
│                        → [FFN + 残差+LN]           │
└───────────────────────────────────────────────────┘
                      │ 线性层 + Softmax
                      ▼
                  输出词概率
```

| 模块 | 作用 |
|------|------|
| 编码器 | 双向理解输入序列（BERT 类只用编码器） |
| 解码器 | 自回归生成输出（GPT 类只用解码器） |
| 交叉注意力 | 解码器关注编码器输出，实现"翻译"式映射 |
| 掩码注意力 | 预测时禁止看到未来 Token |

## 4.2 Embedding 与位置编码

### 4.2.1 Token Embedding

将 Token 映射为 d_model 维向量（可学习矩阵），如 d_model=512。

### 4.2.2 位置编码（Positional Encoding）

注意力本身**不感知顺序**（打乱句子顺序结果相同），必须注入位置信息：

**① 正弦位置编码（原论文）**：

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**② 可学习位置编码**：随机初始化，随模型训练。

**③ RoPE（旋转位置编码，现代主流）**：通过旋转矩阵注入相对位置信息，被 LLaMA、Qwen 等采用，外推能力强。

## 4.3 自注意力机制详解

### 4.3.1 计算流程

```
输入 X → 分别乘 W_Q、W_K、W_V 得到 Q、K、V
得分矩阵 = Q·Kᵀ / √d_k        （相关性）
权重 = softmax(得分)          （归一化）
输出 = 权重 · V               （加权求和）
```

### 4.3.2 单头注意力实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, d_model, d_k):
        super().__init__()
        self.W_Q = nn.Linear(d_model, d_k)
        self.W_K = nn.Linear(d_model, d_k)
        self.W_V = nn.Linear(d_model, d_k)
        self.d_k = d_k

    def forward(self, x, mask=None):
        Q, K, V = self.W_Q(x), self.W_K(x), self.W_V(x)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.d_k ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attn = F.softmax(scores, dim=-1)
        return torch.matmul(attn, V)
```

### 4.3.3 为什么要除以 √d_k

Q·K 点积随维度增大而增大，softmax 会进入梯度极小区间。除以 √d_k 将方差控制在 1 附近，保证梯度稳定。

### 4.3.4 多头注意力（Multi-Head）

将 Q/K/V 切成 h 个头独立计算，再拼接：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape
        Q = self.W_Q(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.d_k ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, V)                       # [b, h, s, d_k]
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, -1)
        return self.W_O(out)
```

**多头的好处**：不同头关注不同模式（语法、指代、语义、位置），增强表达多样性。

## 4.4 前馈网络（FFN）与残差连接

### 4.4.1 FFN

每层注意力后接两层的 MLP（先升维再降维）：

```
FFN(x) = max(0, x·W₁ + b₁)·W₂ + b₂     # ReLU 版本
FFN(x) = (x·W₁)·SiLU(x·W₂)             # SwiGLU（现代主流）
维度变化：d_model → d_ff（通常 4×d_model）→ d_model
```

### 4.4.2 残差连接 + 层归一化

```
x = x + SubLayer(x)          # 残差连接（梯度高速公路）
x = LayerNorm(x)             # 层归一化（稳定训练）
现代变体：Pre-Norm（先归一化再计算，训练更稳）
```

**为什么关键**：
- 残差让深层网络可训练（解决梯度消失/退化）。
- LayerNorm 稳定分布，允许更大学习率。

## 4.5 Transformer 实现与训练要点

### 4.5.1 编码器层完整实现

```python
class EncoderLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model),
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        x = self.norm1(x + self.dropout(self.attn(x, mask)))
        x = self.norm2(x + self.dropout(self.ffn(x)))
        return x
```

### 4.5.2 训练要点

1. **任务**：预训练（MLM/Next Token）→ 微调。
2. **优化器**：Adam（β₁=0.9, β₂=0.98）+ Warmup 学习率（先升后降）。
3. **正则**：Dropout 0.1 + Label Smoothing。
4. **并行**：数据并行 / 张量并行（大规模）。
5. **精度**：混合精度训练（BF16 + GradScaler）省显存提速。

### 4.5.3 复杂度

标准注意力 O(n²)（n=序列长度）——这是长上下文的根本瓶颈，催生了 FlashAttention、稀疏注意力、线性注意力等优化（回顾第一部分第 2 章）。

---

## 高质量博客推荐

1. **The Illustrated Transformer（中文图解版）** — [知乎专栏](https://zhuanlan.zhihu.com/p/672469127)
   最经典的 Transformer 图解入门，强烈推荐。
2. **Transformer 核心架构详解：从注意力到 FFN** — [掘金](https://juejin.cn/post/7506156129368948807)
   完整拆解 + PyTorch 代码。
3. **GPT 系列为何只用 Decoder：自回归架构解析** — [CSDN](https://blog.csdn.net/qq_38978225/article/details/142746065)
   理解 Decoder-only 与 Encoder-Decoder 的差别。
4. **RoPE 旋转位置编码详解** — [知乎专栏](https://zhuanlan.zhihu.com/p/662738559)
   现代大模型位置编码的主流方案。
5. **Attention Is All You Need 论文精读** — [CSDN](https://blog.csdn.net/u010666669/article/details/118837669)
   原始论文逐节精读。

## 动手实践

1. 实现完整的 MultiHeadAttention 并在小序列上验证输出形状。
2. 实现一个 2 层编码器，用于文本分类任务（IMDB）。
3. 画一张"编码器-解码器"架构图，标注每个张量形状。

## 常见问题（FAQ）

**Q1：为什么现代大模型几乎都用 Decoder-only？**
A：训练更简单稳定、与自回归生成天然契合；Encoder 的双向信息可通过训练技巧（如 RAG 注入）补偿。实践表明 Decoder-only 在 scale 到足够大时效果更优。

**Q2：Transformer 比 RNN 好在哪？**
A：①并行（RNN 必须串行）；②长距离依赖直接建模（注意力一步到位）；③无梯度消失问题（残差+归一化）。

**Q3：位置编码为什么必须存在？**
A：注意力计算对序列顺序不敏感（置换不变性），没有位置信息模型就分不清"我爱你"和"你爱我"。
