# Transformer 的过去和现在：从 RNN 到 GPT-5 的深度学习序列模型演进史

> 本文系统梳理了序列建模从循环神经网络（RNN）到 Transformer 及其现代变体（BERT、GPT、ViT、MoE、Mamba 等）的发展脉络，涵盖核心公式、架构示意图、关键创新和前沿趋势，适合作为深度学习研究者与工程师的系统性技术参考。

---

## 目录

1. [RNN/LSTM：早期序列模型的黎明](#1-rnnlstm早期序列模型的黎明)
2. [Seq2Seq 与注意力机制](#2-seq2seq-与注意力机制)
3. [Transformer 的出现](#3-transformer-的出现)
4. [编码器类变体（BERT 家族）](#4-编码器类变体bert-家族)
5. [解码器类变体（GPT 家族）](#5-解码器类变体gpt-家族)
6. [编码器-解码器类变体](#6-编码器-解码器类变体)
7. [视觉 Transformer](#7-视觉-transformer)
8. [长序列优化技术](#8-长序列优化技术)
9. [混合专家模型（MoE）](#9-混合专家模型moe)
10. [状态空间模型（Mamba）](#10-状态空间模型mamba)
11. [其他前沿架构](#11-其他前沿架构)
12. [总结对比表](#12-总结对比表)
13. [专业名词解释](#13-专业名词解释)

---

## 1. RNN/LSTM：早期序列模型的黎明

### 1.1 循环神经网络（RNN）

#### 基本思想

循环神经网络（Recurrent Neural Network, RNN）是深度学习处理序列数据最早的经典架构之一。其核心思想是将"时间"引入神经网络——即当前时刻的输出不仅依赖于当前输入，还依赖于上一时刻的隐藏状态，从而形成一种"记忆"机制。

#### 架构示意图

```
时刻 t-1          时刻 t            时刻 t+1
┌─────────┐     ┌─────────┐       ┌─────────┐
│  y_{t-1}│     │   y_t   │       │  y_{t+1}│
│    ▲     │     │    ▲    │       │    ▲    │
│    │     │     │    │    │       │    │    │
│ ┌──┴──┐  │     │ ┌──┴──┐ │       │ ┌──┴──┐ │
│ │  V  │  │     │ │  V  │ │       │ │  V  │ │
│ └──┬──┘  │     │ └──┬──┘ │       │ └──┬──┘ │
│    │     │     │    │    │       │    │    │
│    ▼     │     │    ▼    │       │    ▼    │
│  h_{t-1} ├────►│   h_t   ├──────►│  h_{t+1}│────► ...
│    ▲     │     │    ▲    │       │    ▲    │
│    │     │     │    │    │       │    │    │
│    │     │     │    │    │       │    │    │
│  x_{t-1} │     │   x_t   │       │  x_{t+1}│
└─────────┘     └─────────┘       └─────────┘

共享权重: W_h (隐藏层), W_x (输入层), W_y (输出层)
```

#### 核心公式

**隐藏状态更新（前向传播）**：

```
h_t = tanh(W_h · h_{t-1} + W_x · x_t + b_h)
```

其中：
- `x_t` ∈ R^d：t 时刻的输入向量
- `h_t` ∈ R^n：t 时刻的隐藏状态向量
- `W_h` ∈ R^{n×n}：隐藏层循环权重矩阵
- `W_x` ∈ R^{n×d}：输入层权重矩阵
- `b_h` ∈ R^n：偏置向量
- `tanh`：双曲正切激活函数

**输出计算**：

```
y_t = W_y · h_t + b_y
```

通常输出层之后会接 softmax 进行分类：

```
P(y_t | x_1, ..., x_t) = softmax(W_y · h_t + b_y)
```

#### 损失函数

对于序列标注任务（如语言建模），使用交叉熵损失：

```
L = -Σ_{t=1}^{T} log P(y_t^* | x_1, ..., x_t)
```

其中 `y_t^*` 为时刻 t 的真实标签。

#### 反向传播：BPTT (Back-Propagation Through Time)

BPTT（通过时间的反向传播）是 RNN 训练的核心算法。其本质是将 RNN 按时间展开成一个"深度"前馈网络，然后沿时间轴做标准反向传播。

```
∂L/∂W_h = Σ_{t=1}^{T} ∂L_t/∂W_h

其中 ∂L_t/∂W_h = Σ_{k=1}^{t} ∂L_t/∂h_t · (Π_{j=k+1}^{t} ∂h_j/∂h_{j-1}) · ∂h_k/∂W_h
```

连乘项 `Π ∂h_j/∂h_{j-1}` 中，每个因子包含 `W_h` 和 `tanh'`，这是梯度消失/爆炸的根本原因。

#### RNN 的优点

1. **参数共享**：所有时间步共享同一组权重矩阵 `W_h`、`W_x`、`W_y`，参数量不随序列长度增长
2. **变长序列处理**：理论上可以处理任意长度的序列输入
3. **理论完备性**：RNN 是图灵完备的（Siegelmann & Sontag, 1995），理论上可模拟任意计算
4. **结构简洁**：循环结构直观，易于理解和实现

#### RNN 的缺点

1. **梯度消失/爆炸 (Vanishing/Exploding Gradients)**：BPTT 中的连乘导致梯度以指数级衰减或增长。当 `|W_h|` 的最大特征值小于 1 时，长序列的早期时间步梯度趋近于 0，导致无法学习长程依赖
2. **长程依赖能力弱**：即使梯度不消失，RNN 也难以捕获间隔超过约 10 步的依赖关系
3. **串行计算瓶颈**：当前时间步的计算依赖于上一时间步的隐藏状态，无法并行化，训练和推理效率低下
4. **记忆容量有限**：固定维度的隐藏状态必须"压缩"所有历史信息，形成信息瓶颈

#### 梯度裁剪 (Gradient Clipping)

梯度裁剪是缓解梯度爆炸的实用技术，通过限制梯度的范数来稳定训练：

```
if ||g|| > threshold:
    g = (threshold / ||g||) · g
```

通常设置 threshold = 1.0 或 5.0，虽然不能解决梯度消失，但能有效防止梯度爆炸带来的训练崩溃。

#### 教师强制 (Teacher Forcing)

在 RNN 训练中，Teacher Forcing 是指：在时刻 t 的输入不使用模型自己预测的 `y_{t-1}`，而是使用真实目标 `y_{t-1}^*`。这加速了训练收敛，避免了错误累积，但会导致训练和推理之间的分布不匹配（exposure bias）。

---

### 1.2 长短期记忆网络（LSTM）

LSTM（Long Short-Term Memory）由 Hochreiter & Schmidhuber 于 1997 年提出，是解决 RNN 梯度消失问题的里程碑式架构。其核心创新是引入"门控机制"和独立的"细胞状态"（Cell State），允许信息跨越多个时间步无衰减地传递。

#### 架构示意图

```
                        LSTM Cell
        ┌──────────────────────────────────────────────────┐
        │                                                  │
  C_{t-1} ──────────────────────────►[+]──────────────────► C_t
        │                    ▲       ▲   │                  │
        │                    │       │   ▼                  │
        │                f_t │   i_t │  C̃_t                 │
        │                  ┌─┴─┐  ┌─┴─┐ │                   │
        │                  │ σ │  │ σ │ │tanh│              │
        │                  └─┬─┘  └─┬─┘ └─┬─┘               │
        │                    │       │     │                 │
        │                    │   ┌───┴─────┴───┐             │
  h_{t-1} ───────────────────┼───┤    Concat    │             │
        │                    │   └───┬─────┬───┘             │
        │                    │       │     │                 │
        │                  ┌─┴─┐     │  ┌──┴──┐              │
        │                  │ σ │     │  │tanh │              │
        │           o_t    └─┬─┘     │  └──┬──┘              │
        │              ▲     │       │     │                 │
        │              │     │       │     │                 │
        │              └─────┴───────┴─────┘                 │
        │                       h_t                          │
        └────────────────────────────────────────────────────┘

  x_t ───────────────────────────────────────────────────────┘
```

#### 核心公式

LSTM 有四个关键门控组件：

**遗忘门 (Forget Gate)** — 决定丢弃哪些旧信息：

```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
```

**输入门 (Input Gate)** — 决定向细胞状态写入哪些新信息：

```
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
```

**候选细胞状态 (Cell State Candidate)** — 生成新候选信息：

```
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
```

**细胞状态更新 (Cell State Update)** — 核心的记忆"高速公路"：

```
C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
```

其中 ⊙ 表示逐元素乘积（Hadamard Product）。`C_t` 可以在时间维度上无衰减地传递，这是 LSTM 克服梯度消失的关键。

**输出门 (Output Gate)** — 决定当前隐藏状态输出什么：

```
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
h_t = o_t ⊙ tanh(C_t)
```

#### LSTM 如何解决梯度消失

在 BPTT 中，关于 `C_t` 的梯度传播路径中不存在连乘权重矩阵 `W_h`：

```
∂C_t/∂C_{t-1} = f_t  （仅逐元素乘以遗忘门的值）
```

这个路径是线性的、逐元素的，梯度可以无损（或通过遗忘门可控地）沿时间轴传播，从而避免了 RNN 中的梯度消失问题。

#### LSTM 的优点

1. 有效解决梯度消失问题，可建模数百步的长程依赖
2. 门控机制提供了灵活的信息流控制
3. 在实践中几乎全面替代了 vanilla RNN

#### LSTM 的缺点

1. 参数量大（4 个门控矩阵，约为 vanilla RNN 的 4 倍）
2. 计算复杂度高
3. 依然串行计算，无法并行化
4. 长程依赖仍有上限（实践中约 100-300 步）

---

### 1.3 门控循环单元（GRU）

GRU（Gated Recurrent Unit）由 Cho et al., 2014 年提出，是 LSTM 的简化版本，将三个门合并为两个门，并将细胞状态与隐藏状态合并，在保持类似性能的同时减少参数量。

**更新门 (Update Gate)** — 融合了 LSTM 的遗忘门和输入门：

```
z_t = σ(W_z · [h_{t-1}, x_t] + b_z)
```

**重置门 (Reset Gate)** — 控制如何将新输入与之前的记忆结合：

```
r_t = σ(W_r · [h_{t-1}, x_t] + b_r)
```

**候选隐藏状态**：

```
h̃_t = tanh(W · [r_t ⊙ h_{t-1}, x_t] + b)
```

**最终隐藏状态**：

```
h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t
```

更新门 `z_t` 在保留旧信息（`1 - z_t`）和接纳新信息（`z_t`）之间做线性插值。当 `z_t` 接近 0 时，`h_t ≈ h_{t-1}`（信息完全保留）；当 `z_t` 接近 1 时，`h_t ≈ h̃_t`（状态完全更新）。

GRU 参数量约为 LSTM 的 75%，在多数序列任务中表现与 LSTM 相当甚至更优。

---

### 1.4 双向 RNN 与深层 RNN

#### 双向 RNN (Bi-RNN)

Bi-RNN 同时使用两个 RNN：一个从前向后处理序列（正向），一个从后向前处理序列（反向），然后拼接两个方向的隐藏状态：

```
→    →
h_t = RNN_forward(x_t, h_{t-1})
←    ←
h_t = RNN_backward(x_t, h_{t+1})
      →   ←
h_t = [h_t; h_t]
```

这使得当前时刻的输出可以利用来自过去和未来的全部上下文信息，在序列标注（如 NER、POS Tagging）等需要全局信息的任务中表现优异。

#### 深层 RNN (Deep RNN)

深度 RNN 将多个 RNN 层垂直堆叠，第 l 层的隐藏状态作为第 l+1 层的输入：

```
h_t^(l) = RNN^(l)(h_t^(l-1), h_{t-1}^(l))
```

深层 RNN 可以学习到更抽象的层次化特征，但也会加剧梯度消失问题。实践中，RNN 层数通常不超过 3-4 层。

---

## 2. Seq2Seq 与注意力机制

### 2.1 编码器-解码器架构

Seq2Seq（Sequence-to-Sequence）架构由 Sutskever et al., 2014 和 Cho et al., 2014 同时提出，用于处理输入和输出都是变长序列的任务，如机器翻译、文本摘要等。

#### 架构示意图

```
┌──────────────────────────────────────────────────────────────────┐
│                        Seq2Seq 架构                              │
│                                                                  │
│  Encoder (编码器)                       Decoder (解码器)          │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐              ┌───┐ ┌───┐ ┌───┐ ┌───┐  │
│  │   │ │   │ │   │ │   │              │   │ │   │ │   │ │   │  │
│  │h_1│→│h_2│→│h_3│→│h_4│      c       │s_1│→│s_2│→│s_3│→│s_4│  │
│  │   │ │   │ │   │ │   │ ┌───────►     │   │ │   │ │   │ │   │  │
│  └─▲─┘ └─▲─┘ └─▲─┘ └─▲─┘ │            └─┬─┘ └─▲─┘ └─▲─┘ └─▲─┘  │
│    │     │     │     │    │              │     │     │     │       │
│  ┌─┴─┐ ┌─┴─┐ ┌─┴─┐ ┌─┴─┐ │            ┌─┴─┐   │   ┌─┴─┐ ┌─┴─┐  │
│  │x_1│ │x_2│ │x_3│ │x_4│ │        <S> │y_1│ y_1  y_2│ y_3│      │
│  └───┘ └───┘ └───┘ └───┘ │            └───┘       └───┘ └───┘  │
│                           │                                       │
│              上下文向量 c = h_T (编码器最后隐藏状态)                │
└──────────────────────────────────────────────────────────────────┘
```

**编码器**：将输入序列 `(x_1, ..., x_T)` 编码为上下文向量 `c`（通常是最后一时刻的隐藏状态 `h_T`）。

**解码器**：以上下文向量 `c` 为初始状态，逐步生成输出序列 `(y_1, ..., y_{T'})`。解码器中，每个输出 `y_t` 以上一时刻的输出和当前隐藏状态作为条件。

解码器的条件概率分解：

```
P(y_1, ..., y_{T'} | x_1, ..., x_T) = Π_{t=1}^{T'} P(y_t | y_{<t}, c)
```

#### 上下文向量瓶颈问题

在基础 Seq2Seq 中，整个输入序列的信息被压缩到一个固定维度的上下文向量 `c` 中。当输入序列较长时，这个向量成为信息瓶颈：
- 编码器必须将所有信息"挤压"到一个向量中
- 解码器无法有选择地关注输入的不同部分
- 对于长句翻译，性能会显著下降

这直接催生了注意力机制的诞生。

---

### 2.2 Bahdanau 注意力（加性注意力）

Bahdanau et al., 2015 首次将注意力机制引入 Seq2Seq 模型，允许解码器在每个输出时刻"动态地"关注输入序列的不同部分。

#### 架构示意

```
                        注意力机制

  Encoder Outputs           Attention Scores        Decoder
  ┌───┐  ┌───┐  ┌───┐
  │h_1│  │h_2│  │h_3│  ...
  └──┬┘  └──┬┘  └──┬┘       α_1  α_2  α_3         s_{i-1}
     │      │      │         │    │    │              │
     │      │      │         ▼    ▼    ▼              │
     └──────┼──────┼─────────┼────┼────┼──────────────┘
            │      │         │    │    │
            ▼      ▼         ▼    ▼    ▼
         ┌─────────────────────────────┐
         │   Σ α_ij · h_j =  c_i       │  ◄── 上下文向量
         └──────────────┬──────────────┘
                        │
                        ▼
                  ┌───────────┐
                  │ [s_{i-1}; │  ◄── 拼接后进入解码器
                  │   c_i   ] │
                  └───────────┘
```

#### 核心公式

**注意力能量计算 (Alignment Score)**：

```
e_{ij} = v_a^T · tanh(W_a · s_{i-1} + U_a · h_j)
```

其中：
- `s_{i-1}`：解码器在 i-1 时刻的隐藏状态
- `h_j`：编码器在 j 时刻的隐藏状态（或者说 encoder output）
- `W_a, U_a`：可学习的权重矩阵
- `v_a`：可学习的向量（将结果映射为标量得分）
- `e_{ij}`：标量，表示解码器位置 i 与编码器位置 j 之间的"匹配程度"

**注意力权重 (Attention Weights)**：

```
α_{ij} = softmax(e_{i·})_j = exp(e_{ij}) / Σ_{k=1}^{T} exp(e_{ik})
```

**上下文向量 (Context Vector)**：

```
c_i = Σ_{j=1}^{T} α_{ij} · h_j
```

上下文向量 `c_i` 是编码器所有隐藏状态的加权和，权重 `α_{ij}` 反映了解码器当前时刻对输入各位置的"关注"程度。

**解码器状态更新**：

```
s_i = RNN(s_{i-1}, [y_{i-1}; c_i])
```

**输出概率**：

```
P(y_i | y_{<i}, x) = softmax(W_o · [s_i; c_i] + b_o)
```

---

### 2.3 Luong 注意力（乘性注意力）

Luong et al., 2015 提出了几种替代的注意力计算方式，统称为乘性注意力：

**Dot（点积）**：

```
e_{ij} = s_i^T · h_j
```

**General（一般乘性）**：

```
e_{ij} = s_i^T · W_a · h_j
```

**Concat（拼接型，即 Bahdanau 的加性注意力）**：

```
e_{ij} = v_a^T · tanh(W_a · [s_i; h_j])
```

**Bahdanau vs Luong 的区别**：
- Bahdanau 使用 `s_{i-1}`（上一时刻的解码器状态）计算注意力
- Luong 使用 `s_i`（当前时刻的解码器状态，即先计算 `s_i`，再算注意力）
- 乘性注意力计算效率更高（矩阵乘法），加性注意力理论上表达力更强

---

### 2.4 关键术语

- **对齐分数 (Alignment Score) `e_{ij}`**：衡量解码器位置 i 与编码器位置 j 之间的相关性/匹配度
- **注意力权重 (Attention Weight) `α_{ij}`**：对齐分数经过 softmax 归一化后的概率分布
- **上下文向量 (Context Vector) `c_i`**：编码器隐藏状态的加权和，表示"被关注到的"输入表示
- **全局注意力 (Global Attention)**：考虑所有编码器位置（即为上述的 Bahdanau/Luong 注意力）
- **局部注意力 (Local Attention)**：仅考虑编码器的一个窗口子集，减少计算量
- **教师强制 (Teacher Forcing)**：训练时使用真实标签作为下一时刻输入
- **计划采样 (Scheduled Sampling)**：训练时以一定概率混合使用真实标签和模型预测，缓解 exposure bias

---

## 3. Transformer 的出现

2017 年，Vaswani et al. 在论文《Attention Is All You Need》中提出了 Transformer 架构，完全摒弃了循环结构，仅使用注意力机制进行序列建模。这一工作彻底改变了深度学习的发展轨迹。

### 3.1 完整架构图

```
┌──────────────────────────────────────────────────────────────────┐
│               Transformer 完整架构 (Vaswani et al., 2017)         │
│                                                                   │
│                       Output Probabilities                        │
│                             ▲                                     │
│                       ┌─────┴─────┐                               │
│                       │  Softmax  │                               │
│                       └─────┬─────┘                               │
│                       ┌─────┴─────┐                               │
│                       │  Linear   │                               │
│                       └─────┬─────┘                               │
│                   ┌─────────┴─────────┐                           │
│                   │    Add & Norm      │  ◄── 残差 + LayerNorm    │
│                   └─────────┬─────────┘                           │
│                   ┌─────────┴─────────┐                           │
│                   │   Feed Forward    │  ◄── FFN(x) = GELU/ReLU   │
│                   │     Network       │                           │
│                   └─────────┬─────────┘                           │
│                   ┌─────────┴─────────┐                           │
│ ┌─────────┐       │    Add & Norm      │       ┌─────────┐       │
│ │  Output │       └─────────┬─────────┘       │  Input  │       │
│ │Embedding│                 │                 │Embedding│       │
│ └────┬────┘       ┌─────────┴─────────┐       └────┬────┘       │
│      │      ┌────►│  Multi-Head       │◄─────┐     │             │
│      │      │     │  Attention        │      │     │             │
│      │      │     └─────────┬─────────┘      │     │             │
│      │      │               │                │     │             │
│      │ ┌────┴─────┐   ┌─────┴─────┐    ┌─────┴─────┐│             │
│ N×   │ │ Add&Norm │   │ Add&Norm  │    │ Add&Norm  ││    N×       │
│      │ └────┬─────┘   └─────┬─────┘    └─────┬─────┘│             │
│      │      │               │                │      │             │
│      │ ┌────┴─────┐   ┌─────┴─────┐    ┌─────┴─────┐│             │
│      │ │   FFN    │   │Masked MHA│     │   MHA     ││             │
│      │ └────┬─────┘   └─────┬─────┘    └─────┬─────┘│             │
│      │      │               │                │      │             │
│      │ ┌────┴─────┐         │                │      │             │
│      │ │ Add&Norm │         │                │      │             │
│      │ └────┬─────┘         │                │      │             │
│      │      │               │                │      │             │
│      │ ┌────┴─────┐         │                │      │             │
│      │ │Masked MHA│         │                │      │             │
│      │ └────┬─────┘         │                │      │             │
│      │      │               │                │      │             │
│      │    Positional    Positional       Positional               │
│      │    Encoding  +   Encoding    +   Encoding   +              │
│      │    Output        Output          Input                     │
│      │    Embedding     Embedding       Embedding                 │
│      │       ▲              ▲               ▲                     │
│  ┌───┴───────┴───┐     ┌───┴───────┐   ┌───┴───────────┐         │
│  │   Outputs     │     │  Outputs  │   │    Inputs     │         │
│  │ (shifted rt)  │     │           │   │               │         │
│  └───────────────┘     └───────────┘   └───────────────┘         │
│       Decoder (解码器)           Encoder (编码器)                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 自注意力机制 (Self-Attention)

自注意力（Self-Attention，也称 Scaled Dot-Product Attention）是 Transformer 的核心创新。它允许序列中的每个位置直接"关注"序列中的所有其他位置。

#### 计算流程

**Step 1: 生成 Q, K, V 矩阵**

对于输入序列表示 `X ∈ R^{n × d_model}`：

```
Q = X · W_Q      (Query,  查询)
K = X · W_K      (Key,    键)
V = X · W_V      (Value,  值)
```

其中：
- `X ∈ R^{n × d_model}`：n 个 token 的输入表示
- `W_Q, W_K, W_V ∈ R^{d_model × d_k}`：可学习的投影矩阵（通常 `d_k = d_model / h`）
- `Q, K, V ∈ R^{n × d_k}`：查询、键、值矩阵

**Step 2: 计算注意力分数**

```
Scores = (Q · K^T) / √d_k     结果形状: (n, n)
```

除以 `√d_k` 是为了防止当 `d_k` 较大时点积值过大导致 softmax 梯度进入饱和区（这就是"Scaled"的含义）。

**Step 3: Softmax 归一化**

```
Attention_Weights = softmax(Scores)     结果形状: (n, n)
```

**Step 4: 加权求和**

```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V     结果形状: (n, d_k)
```

#### 直观理解

```
输入序列:     "The   cat   sat   on   the   mat"
               │     │     │     │    │     │
               ▼     ▼     ▼     ▼    ▼     ▼
每个 token 通过 Q 矩阵"查询"其他所有 token，
用"键"的匹配度作为权重，聚合所有位置的"值"。

例如 "mat" 这个位置：
  - Q_mat 与所有位置的 K 计算相似度
  - 与 "cat"(0.30), "sat"(0.25), "on"(0.15), "the"(0.10)... 分配不同权重
  - 按权重聚合所有位置的 V 信息
  - 得到 "mat" 在此上下文中的丰富表示
```

#### 因果掩码 (Causal Mask)

在解码器中，为防止当前位置"看到"未来信息，使用上三角掩码矩阵 M：

```
Attention = softmax((Q·K^T / √d_k) + M) · V

其中 M_{ij} = { 0,    if i ≥ j
              { -∞,   if i < j   (softmax 后 → 0)
```

---

### 3.3 多头注意力 (Multi-Head Attention)

单头注意力可能只关注一种模式（如语法关系），多头注意力允许模型同时从不同的表示子空间关注不同的关系模式。

```
head_i = Attention(Q · W_Qi,  K · W_Ki,  V · W_Vi)
MultiHead(Q, K, V) = Concat(head_1, head_2, ..., head_h) · W_O
```

其中：
- `h`：头的数量（Transformer_base 中 h=8）
- `W_Qi, W_Ki, W_Vi ∈ R^{d_model × d_k}`：各头独立的投影矩阵
- `W_O ∈ R^{h·d_k × d_model}`：输出投影矩阵，融合多头信息
- `d_k = d_model / h`（通常如此设置以保持总参数量稳定）

**参数量**：每个头的维度降到 `d_model/h`，所以总计算量与单头全维度注意力基本一致，但表达力显著增强。

#### 三种注意力使用方式

1. **编码器自注意力 (Encoder Self-Attention)**：Q, K, V 均来自编码器输入，双向（无掩码），每个位置可关注所有位置
2. **解码器自注意力 (Masked Decoder Self-Attention)**：Q, K, V 均来自解码器输入，使用因果掩码防止信息泄露
3. **交叉注意力 (Cross-Attention)**：Q 来自解码器，K、V 来自编码器输出，允许解码器关注输入序列

---

### 3.4 位置编码 (Positional Encoding)

由于自注意力是排列等变的（permutation equivariant），即打乱输入顺序不改变输出值（仅改变输出顺序），Transformer 需要显式注入位置信息。

#### 正弦位置编码 (Sinusoidal PE)

原始 Transformer 使用固定正弦/余弦函数：

```
PE(pos, 2i)   = sin(pos / 10000^{2i/d_model})
PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model})
```

其中：
- `pos`：位置索引（0, 1, 2, ...）
- `i`：维度索引（0, 1, ..., d_model/2 - 1）
- `10000^{2i/d_model}`：频率项，低维对应高频（短程位置敏感），高维对应低频（长程位置模式）

**性质**：
- 任意偏移 k 的位置向量 `PE(pos+k)` 可表示为 `PE(pos)` 的线性变换（三角恒等式）
- 无需学习参数，可外推到训练时未见过的序列长度
- 值域在 [-1, 1] 之间，与词嵌入 + 位置编码的尺度一致

#### 可学习位置编码 (Learned PE)

BERT、GPT 等模型使用可学习的位置嵌入矩阵，在训练中学习位置表示。限制在于无法外推到超出训练最大长度的序列。

#### RoPE (旋转位置编码) — 现代主流

RoPE (Rotary Position Embedding) 由 Su et al., 2021 提出，LLaMA/Qwen/DeepSeek 等主流模型广泛使用：

```
RoPE 对每对维度 (2i, 2i+1) 施加旋转:
  [x_2i']   [cos(pos·θ_i)  -sin(pos·θ_i)] [x_2i]
  [x_2i+1']=[sin(pos·θ_i)   cos(pos·θ_i)] [x_2i+1]

  θ_i = 10000^{-2i/d}
  
在注意力计算中，Q·K^T 的内积仅依赖于 (pos_q - pos_k)，
即模型天然获得相对位置信息。
```

---

### 3.5 前馈网络 (Feed-Forward Network)

每个 Transformer 层中的 FFN 子层对每个位置独立应用相同的全连接网络：

```
FFN(x) = max(0, x · W_1 + b_1) · W_2 + b_2    (原始 ReLU 版本)
```

其中 `W_1 ∈ R^{d_model × d_ff}`，`W_2 ∈ R^{d_ff × d_model}`，通常 `d_ff = 4 × d_model`（如 d_model=512 时 d_ff=2048）。

**现代变体**：

```
GELU (Gaussian Error Linear Unit):
  GELU(x) = x · Φ(x) ≈ 0.5x(1 + tanh(√(2/π)(x + 0.044715x³)))

SwiGLU (LLaMA 等现代模型使用):
  SwiGLU(x) = (x · W_1 ⊙ SiLU(x · W_g)) · W_2
  其中 SiLU(x) = x · σ(x)  (亦称 Swish 激活函数)
```

SwiGLU 由 Shazeer (2020) 提出，已成为当前主流大语言模型（LLaMA、PaLM、Qwen 等）的标准 FFN 实现，相比 ReLU 和 GELU 在语言建模任务中表现出更好的性能。

---

### 3.6 层归一化 (Layer Normalization)

Transformer 使用 LayerNorm 而不是 BatchNorm，因为 LayerNorm 在特征维度上归一化，不依赖 batch 内的统计量，更适合变长序列和 NLP 场景。

```
LayerNorm(x) = γ ⊙ (x - μ) / √(σ² + ε) + β

其中 μ = mean(x_{:d}), σ² = var(x_{:d})
```

**Post-LN vs Pre-LN**：

```
Post-LN (原始 Transformer):         Pre-LN (现代主流):
x ← LayerNorm(x + Sublayer(x))     x ← x + Sublayer(LayerNorm(x))
```

Pre-LN 在训练中更稳定，梯度流动更好，已成为 GPT 系列和大多数现代 Transformer 的默认选择。

RMSNorm（LLaMA 使用）是 LayerNorm 的简化版：

```
RMSNorm(x) = x / √(mean(x²) + ε) · γ
```

去除了均值减去，计算效率更高。

---

### 3.7 残差连接 (Residual Connections)

每个子层（自注意力或 FFN）之后都使用残差连接：

```
Output = LayerNorm(x + Dropout(Sublayer(x)))
```

残差连接解决了深层网络的退化问题，允许梯度直接传递，使得训练数百层的 Transformer 成为可能。

---

### 3.8 训练配置

**优化器**：Adam，参数 β₁=0.9, β₂=0.98, ε=10⁻⁹

**学习率调度 (Warmup Schedule)**：

```
lr = d_model^{-0.5} · min(step_num^{-0.5}, step_num · warmup_steps^{-1.5})
```

先线性增加（warmup_steps=4000），再按步数的平方根倒数衰减。这一设计防止了训练初期的大梯度破坏尚未稳定的注意力分布。

**正则化技术**：
- **Dropout**：每个子层输出后、嵌入求和后，使用 dropout（比例通常 0.1）
- **Label Smoothing**：将 one-hot 标签平滑为 (1-ε) 的 one-hot + ε/(K-1) 的均匀分布，ε=0.1，防止模型过度自信

---

### 3.9 复杂度分析

| 层类型 | 每层复杂度 | 序列操作数 | 最大路径长度 |
|--------|-----------|-----------|-------------|
| Self-Attention | O(n² · d) | O(1) | O(1) |
| Recurrent (RNN/LSTM) | O(n · d²) | O(n) | O(n) |
| Convolutional (CNN) | O(k · n · d²) | O(1) | O(log_k(n)) |
| Self-Attention (restricted) | O(r · n · d) | O(1) | O(n/r) |

其中 n 为序列长度，d 为表示维度，k 为卷积核大小，r 为受限注意力的邻域大小。

对于 n < d 的情况（在 NLP 中通常如此），自注意力的 O(n² · d) 实际上优于 RNN 的 O(n · d²)。

---

### 3.10 Transformer 的优点

1. **并行计算**：所有位置同时计算，训练效率远超 RNN（序列操作 O(1) vs O(n)）
2. **长程依赖捕获**：每个位置直接关注所有其他位置，最短路径 O(1)，无需像 RNN 那样逐步传递信息
3. **可解释性**：注意力权重可视化提供了模型决策的直观解释
4. **通用性**：不局限于文本，广泛适用于图像、音频、代码等多种模态

### 3.11 Transformer 的缺点

1. **二次复杂度 O(n²)**：当 n 很大时（长文档、高分辨率图像），计算和内存开销急剧增大
2. **无内置位置感知**：需要显式注入位置编码，且绝对位置编码难以外推
3. **内存占用大**：需要存储 n×n 的注意力矩阵，长序列时内存成为瓶颈
4. **训练数据需求大**：缺少 RNN 的归纳偏置（如局部性、时间顺序），需要更多数据来学习这些模式

---

## 4. 编码器类变体（BERT 家族）

编码器类模型使用 Transformer 的编码器部分，通过双向自注意力捕获上下文信息，主要用于理解任务（分类、序列标注、语义匹配等）。

### 4.1 BERT (Bidirectional Encoder Representations from Transformers)

BERT 由 Google (Devlin et al., 2019) 提出，是 NLP 领域最具影响力的预训练模型之一。它是一个纯编码器 Transformer。

#### 模型规格

| 配置 | 层数 L | 隐藏维度 H | 注意力头 A | 参数量 |
|------|--------|-----------|-----------|--------|
| BERT_base | 12 | 768 | 12 | 110M |
| BERT_large | 24 | 1024 | 16 | 340M |

#### 输入表示

```
Input = Token Embedding + Segment Embedding + Position Embedding

特别地:
  [CLS] Token1 Token2 ... [SEP] TokenA TokenB [SEP]
    0      0      0    ...   0      1      1     1    (Segment ID)
```

- **Token Embeddings**：使用 WordPiece 分词（30,000 词表）
- **Segment Embeddings**：区分句子 A 和句子 B（NSP 任务需要）
- **Position Embeddings**：可学习的位置嵌入，最大长度 512

#### 预训练任务

**任务一：掩码语言模型 (Masked Language Model, MLM)**

随机掩盖输入中 15% 的 token，要求模型预测被掩盖的原始 token。关键的是，不是简单地替换为 [MASK]：

```
15% 选中的 token 中：
  - 80% 替换为 [MASK]
  - 10% 替换为随机 token
  - 10% 保持原样

目的：
  - 80% [MASK]：让模型学习预测
  - 10% 随机替换：迫使模型不能只依赖 [MASK] 标记
  - 10% 保持不变：保持词表示不偏向 [MASK]（因为微调阶段没有 [MASK]）
```

**任务二：下一句预测 (Next Sentence Prediction, NSP)**

```
输入：[CLS] A [SEP] B [SEP]
标签：IsNext (B 是 A 的下一句) or NotNext (B 是随机句子)

目的：学习句子间关系，对 NLI、QA 等任务有益
```

后续研究发现 NSP 对下游任务提升有限（RoBERTa 验证了去掉 NSP 甚至更好）。

#### 特殊 Token

- `[CLS]`：分类标记，其最终隐藏状态用作整个序列的聚合表示
- `[SEP]`：分隔符，标记句子边界
- `[MASK]`：掩码标记，用于 MLM 任务

#### 微调 (Fine-tuning) vs 特征提取 (Feature-based)

- **微调**：在预训练模型上为下游任务添加简单的分类层，端到端微调所有参数
- **特征提取**：冻结预训练参数，仅使用其输出作为下游模型的输入特征

BERT 论文发现微调在所有任务上全面超越特征提取方法。

---

### 4.2 RoBERTa (Robustly Optimized BERT Approach)

RoBERTa (Liu et al., 2019) 是对 BERT 的系统性优化，证明 BERT 被严重"欠训练"：

| 改进项 | BERT | RoBERTa |
|--------|------|---------|
| 训练数据 | 16GB (BooksCorpus + Wiki) | 160GB (CC-News, OpenWebText, Stories 等) |
| 训练步数 | 1M steps | 500K steps（但 batch 更大） |
| Batch Size | 256 | 8K |
| 掩码策略 | 静态掩码（数据预处理时固定） | 动态掩码（每个 epoch 重新生成） |
| NSP | 保留 | 移除 |
| 分词 | WordPiece (30K) | Byte-level BPE (50K) |
| 最大长度 | 512 | 512 |

**关键发现**：
1. 更多数据 + 更长训练 = 显著提升
2. NSP 对下游任务并非必要
3. 动态掩码带来了小幅但一致的提升
4. 更大的 batch size 提升了 perplexity

---

### 4.3 ALBERT (A Lite BERT)

ALBERT (Lan et al., 2020) 通过两种参数缩减技术降低了 BERT 的参数量：

**技术一：分解嵌入参数化 (Factorized Embedding Parameterization)**

将词嵌入矩阵分解为两个小矩阵：

```
词汇量 V × 隐藏维度 H → V × E + E × H     (E << H)
```

例如 BERT_base: 词嵌入参数量 = 30K × 768 ≈ 23M
ALBERT_base: 词嵌入参数量 = 30K × 128 + 128 × 768 ≈ 3.9M

**技术二：跨层参数共享 (Cross-Layer Parameter Sharing)**

所有 Transformer 层共享同一组参数（包括 Attention 和 FFN）。

**技术三：句子顺序预测 (Sentence Order Prediction, SOP)**

用 SOP 替代 NSP：判断两个句子的顺序是否正确（更难的预训练任务）。

ALBERT 将参数量压缩了 18 倍（ALBERT_large: 18M vs BERT_large: 340M），但保留了相当的性能。

---

### 4.4 ELECTRA

ELECTRA (Clark et al., 2020) 引入了新的预训练框架——**替换 token 检测 (Replaced Token Detection)**：

```
框架结构:
  ┌───────────────┐
  │  Generator    │  ← 小型 MLM 模型, 预测被 [MASK] 的 token
  └───────┬───────┘
          │ 生成"伪造"输入
          ▼
  ┌───────────────┐
  │ Discriminator │  ← 对每个 token 判断是原始还是被替换
  └───────┬───────┘
          │
          ▼
  Binary Classification (Original / Replaced)
```

由于判别器对**所有** token 做预测（而非仅 15% 的 [MASK] tokens），ELECTRA 比 MLM 训练效率高得多。ELECTRA-small 以 BERT_small 1/4 的计算量即可匹敌 BERT_small 的性能。

---

### 4.5 DeBERTa (Decoding-enhanced BERT with Disentangled Attention)

DeBERTa (He et al., 2021) 的核心创新是**解耦注意力 (Disentangled Attention)**：

```
A_{ij} = H_i^T · H_j + H_i^T · P_{j|i} + P_{i|j}^T · H_j

其中：
  - H_i, H_j:    内容表示 (Content)
  - P_{j|i}:     相对位置表示 (Position, i 相对于 j)
```

不同于传统方法将内容和位置简单相加，DeBERTa 分别计算内容-内容、内容-位置、位置-内容三种注意力，后两者使用相对位置编码。

此外，DeBERTa 还引入了**增强掩码解码器 (Enhanced Mask Decoder)**，在预训练输出层使用绝对位置信息，弥补了相对位置编码缺少绝对位置信息的不足。

DeBERTa 在 SuperGLUE 基准上首次超越人类水平。

---

### 4.6 ModernBERT (2024)

ModernBERT 是 2024 年底发布的新一代编码器模型，将现代 LLM 的技术融入编码器架构：

**关键技术整合**：
- **Flash Attention**：高效精确的注意力计算
- **RoPE 旋转位置编码**：替代绝对位置编码，支持更好的长度外推
- **GeGLU 激活**：替代标准 GELU
- **取消偏置项**：简化模型结构
- **8192 上下文**：8 倍于原始 BERT 的上下文窗口
- **交替全局/局部注意力**：每 3 层使用一次全局注意力，其余使用 128-token 滑动窗口

---

## 5. 解码器类变体（GPT 家族）

解码器类模型使用 Transformer 的解码器部分（带因果掩码的自注意力），自回归式地预测下一个 token，主要用于生成任务。

### 5.1 GPT 系列演进

#### GPT-1 (2018): Improving Language Understanding by Generative Pre-Training

| 属性 | 值 |
|------|-----|
| 参数量 | 117M |
| 层数 | 12 层 Decoder |
| 隐藏维度 | 768 |
| 注意力头 | 12 |
| 训练数据 | BooksCorpus + 1B Word Benchmark |
| 上下文长度 | 512 |

GPT-1 的核心范式：**生成式预训练 + 判别式微调**。先在大量无标注文本上做语言模型预训练，再为下游任务添加线性分类头进行微调。

#### GPT-2 (2019): Language Models are Unsupervised Multitask Learners

| 属性 | 值 |
|------|-----|
| 参数量 | 1.5B (48 层, 1600 维, 25 头) |
| 训练数据 | WebText (~40GB, 8M 网页) |
| 上下文长度 | 1024 |

GPT-2 的核心主张：**语言模型本身就是无监督的多任务学习器**。以 "zero-shot" 方式（仅给定任务描述，不做任何梯度更新）即可在多个 NLP 任务上取得有竞争力的结果。

**架构调整**：
- LayerNorm 移到每个子层之前（Pre-LN 的雏形）
- 最后一层自注意力层之后增加额外的 LayerNorm

#### GPT-3 (2020): Language Models are Few-Shot Learners

| 属性 | 值 |
|------|-----|
| 参数量 | 175B (96 层, 12288 维, 96 头) |
| 训练数据 | ~570GB (CommonCrawl, WebText2, Books, Wiki) |
| 上下文长度 | 2048 |
| 架构 | 密集 Decoder-Only Transformer (无稀疏/无 MoE) |

GPT-3 提出**上下文学习 (In-Context Learning)**：通过提示（Prompt）中的少量示例（Few-Shot），无需梯度更新即可适应新任务。

```
Zero-Shot:  "Translate English to French: hello →"                    (无示例)
One-Shot:   "Translate English to French: hello → bonjour. bye →"     (1个示例)
Few-Shot:   "Translate English to French: hello → bonjour.
             bye → au revoir. good →"                                 (多个示例)
```

GPT-3 展示了语言模型的**涌现能力**（Emergent Abilities）：随着模型规模增大，某些能力在小模型上完全不存在，但在大模型上突然涌现。

#### InstructGPT / GPT-3.5 (2022): Training Language Models to Follow Instructions

InstructGPT 解决了 GPT-3 不遵循人类意图的问题，核心是 **RLHF (Reinforcement Learning from Human Feedback)**：

```
RLHF 三步法:
  Step 1 ─ SFT (Supervised Fine-Tuning):
          收集人类演示数据，微调基础模型

  Step 2 ─ RM (Reward Model Training):
          收集人类偏好对比数据 (A vs B, 哪个回复更好?)
          训练奖励模型预测人类偏好

  Step 3 ─ PPO (Proximal Policy Optimization):
          使用奖励模型，通过强化学习优化策略模型
          同时加入 KL 散度惩罚，防止偏离 SFT 模型太远
```

PPO 目标函数：

```
L = E[ r(x, y) - β · KL(π_θ(y|x) || π_SFT(y|x)) ]
```

其中 `r(x, y)` 是奖励模型给出的奖励，`β` 控制 KL 惩罚的强度。

#### GPT-4 (2023)

| 属性 | 值（部分为社区推测） |
|------|---------------------|
| 架构 | Mixture of Experts (推测 8×220B) |
| 总参数量 | ~1.8T (推测) |
| 激活参数 | ~220B |
| 上下文长度 | 8K (初版), 32K, 128K |
| 多模态 | 支持图像输入 |

GPT-4 是首个大规模 MoE 架构的商业化模型（虽然技术报告未直接确认具体架构参数，但多家独立分析指向 8-expert MoE）。

**关键能力提升**：
- 多模态理解（图像 + 文本输入）
- 大幅提升的事实准确性
- 更强的推理和编码能力
- 可控性显著增强（system prompt）

#### GPT-4o (2024): Omni-Modal

GPT-4o 的 "o" 代表 "omni"（全能），是一个统一的多模态模型（原生多模态，而非串联多个模型）：

**关键特性**：
- 端到端训练的文本+视觉+音频模型
- 实时语音对话（平均延迟 ~320ms）
- 所有的多模态 token 在同一个 Transformer 中处理
- 视觉理解和生成能力的显著提升

#### GPT-4.5 / GPT-5 发展方向

截至 2026 年，GPT-5 系模型代表了推理范式的转变：

- **System 1 → System 2 思维**：从快思考到慢思考（推理时计算）
- **推理时扩展 (Inference-Time Scaling)**：在推理阶段投入更多计算资源
- **Agentic 能力**：工具使用、代码执行、多步规划
- **长上下文**：百万级 token 上下文窗口
- **原生多模态**：进一步融合文本、图像、音频、视频

---

### 5.2 LLaMA 家族 (Meta)

LLaMA (Large Language Model Meta AI) 是 Meta 的开源大模型系列，因其公开权重和在相对小规模下的优异性能，极大地推动了开源 LLM 社区的发展。

#### 架构详情

LLaMA 架构基于原始 Transformer 解码器，但做了以下关键修改：

```
┌────────────────────────────────┐
│           LLaMA Block          │
│                                │
│   输入 ──► RMSNorm ──►         │
│            ┌──────────┐        │
│            │   MHA    │        │
│            │ (w/ RoPE)│        │
│            └────┬─────┘        │
│                 │              │
│            ┌────┴─────┐        │
│            │ 残差连接  │        │
│            └────┬─────┘        │
│                 │              │
│            ┌────┴─────┐        │
│            │ RMSNorm  │        │
│            └────┬─────┘        │
│                 │              │
│            ┌────┴─────┐        │
│            │  SwiGLU  │        │
│            │   FFN    │        │
│            └────┬─────┘        │
│                 │              │
│            ┌────┴─────┐        │
│            │ 残差连接  │        │
│            └────┬─────┘        │
│                 ▼              │
│              输出              │
└────────────────────────────────┘
```

**三大架构创新**：

1. **RMSNorm (Root Mean Square Layer Normalization)**：简化版 LayerNorm，`RMSNorm(x) = x / RMS(x) · γ`。Zhang & Sennrich (2019) 发现 LayerNorm 的主要收益来自缩放不变性（re-centering 并非必要）。

2. **SwiGLU 激活函数**：`SwiGLU(x) = (x · W_1 ⊙ SiLU(x · W_g)) · W_2`。相比 ReLU/GELU，SwiGLU 在语言建模 perplexity 上带来约 2-3% 的改善（同等计算量下）。

3. **RoPE (Rotary Position Embedding)**：旋转位置编码，在注意力计算中自动注入了相对位置信息（QK^T 内积仅依赖相对位置差），且有良好的外推性质。

#### 各版本演进

| 版本 | 时间 | 最大参数 | 上下文 | 关键亮点 |
|------|------|---------|--------|---------|
| LLaMA 1 | 2023.02 | 65B | 2048 | 仅用公开数据，13B 即超越 GPT-3 175B |
| LLaMA 2 | 2023.07 | 70B | 4096 | GQA, 40% 更多数据，RLHF 微调版 |
| LLaMA 3 | 2024.04 | 405B | 8192 | 15T tokens 训练数据，分组查询注意力 |
| LLaMA 3.1 | 2024.07 | 405B | 128K | 长上下文支持，多语言扩展 |
| LLaMA 4 | 2025 | ~2T (MoE) | 128K+ | 原生多模态，MoE 架构，超大规模训练 |

---

### 5.3 DeepSeek 家族

DeepSeek（深度求索）系列在 2024-2025 年以极高的性能/成本比引起了全球关注。

#### DeepSeek-V2 (2024.05)

关键创新：**MLA (Multi-Head Latent Attention)** + **DeepSeekMoE**

**MLA (多头潜在注意力)**：通过低秩压缩大幅减少 KV Cache 占用

```
标准 MHA:
  K = X · W_K,  V = X · W_V          KV Cache 大小: 2·n·h·d_k

MLA:
  C_KV = X · W_down      (低秩, d_c << d_model)
  K = C_KV · W_up_K      (上投影到完整 K)
  V = C_KV · W_up_V      (上投影到完整 V)

  缓存 C_KV 而非 K 和 V:  Cache 大小: n·d_c  (大幅缩减)

  同样对 Q 做低秩分解:
  C_Q = X · W_down_Q
  Q = C_Q · W_up_Q
```

MLA 将 KV Cache 压缩至标准 MHA 的 1/5~1/10，使更长的上下文在同等显存下成为可能。

#### DeepSeek-V3 (2024.12)

| 属性 | 值 |
|------|-----|
| 总参数量 | 671B |
| 激活参数 | 37B (每 token) |
| 专家数 | 256 (1 共享 + 256 路由专家) |
| Top-K | 8 (1 共享 + 8 路由) |
| 训练数据 | 14.8T tokens |
| 上下文 | 128K (训练) |

**架构特点**：
- **DeepSeekMoE**：细粒度专家（每个专家更小、更多），1 个共享专家 + 256 个路由专家
- **无辅助损失负载均衡 (Auxiliary-Loss-Free Load Balancing)**：通过动态偏差调整实现负载均衡，避免辅助损失对模型性能的影响
- **多 Token 预测 (Multi-Token Prediction, MTP)**：每个位置预测多个未来 token，提升训练信号密度
- **FP8 混合精度训练**：首次实现超大规模 MoE 模型的 FP8 训练

#### DeepSeek-R1 (2025.01)

R1 是 DeepSeek 的推理专用模型，类似于 OpenAI o1 系列：

**训练流程**：
1. **DeepSeek-R1-Zero**：直接在基座模型上用 GRPO (Group Relative Policy Optimization) 训练，无 SFT 冷启动数据
2. **DeepSeek-R1**：收集少量冷启动数据（数千条高质量 CoT）→ SFT → GRPO → 拒绝采样 + SFT → 全场景 RL

**GRPO 算法**：

```
对于每个问题 q，从旧策略采样 G 个输出 {o_1, ..., o_G}
分组归一化奖励: r̃_i = (r_i - mean(r)) / std(r)
每个输出的优势: A_i = r̃_i (无需额外价值模型)

目标函数:
J = 1/G · Σ[min(ρ_i · A_i, clip(ρ_i, 1-ε, 1+ε) · A_i)] - β · KL(π_θ || π_ref)

其中 ρ_i = π_θ(o_i|q) / π_old(o_i|q)
```

相比于标准 PPO（需要 Critic 网络），GRPO 省略了价值模型，通过组内相对排名估计优势，训练效率更高。

**R1 的特点**：
- "Aha Moment"：模型自发学会在推理过程中"重新思考"和"自我纠错"
- 思维链长度随训练自动增长（用户无需显式要求）
- 开放权重，提供 1.5B 到 671B 的多个尺寸

---

### 5.4 Qwen 家族 (Alibaba)

Qwen（通义千问）是阿里巴巴的大模型系列，以其强大的多语言能力（尤其是中文）和全面的开源生态而著称。

| 版本 | 时间 | 关键特性 |
|------|------|---------|
| Qwen | 2023.08 | 首个开源中文大模型，7B/14B |
| Qwen 1.5 | 2024.02 | 多种尺寸 (0.5B-72B)，全面兼容 OpenAI API |
| Qwen 2 | 2024.06 | GQA, SwiGLU, 上下文扩展 (32K-128K), MoE 版本 |
| Qwen 2.5 | 2024.09 | 18T tokens 训练，128K 上下文，强大的代码和数学能力 |
| Qwen 3 | 2025 | 推理模型 (thinking/non-thinking 模式可切换)，MoE 架构 |

**Qwen 架构特点**：
- 标准 LLaMA-like 解码器架构（RMSNorm + SwiGLU + RoPE）
- MoE 版本使用细粒度专家 (Qwen2-57B-A14B: 64 专家, Top-8)
- 强大的分词器（覆盖 150+ 语言，中文分词质量优异）

---

### 5.5 其他重要解码器模型

#### Mistral / Mixtral (Mistral AI)

**Mistral 7B (2023.09)**：
- **滑动窗口注意力 (Sliding Window Attention, SWA)**：每个 token 仅关注前 W 个 token（W=4096），复杂度降至 O(n·W)
- **分组查询注意力 (Grouped Query Attention, GQA)**：减少 KV head 数量（Q 8个头，K/V 各 1 个头），大幅压缩 KV Cache

**Mixtral 8×7B (2023.12)**：开源 MoE 模型的里程碑
- 8 个专家，Top-2 路由
- 总参数 46.7B，每 token 激活 12.9B
- 性能匹敌 GPT-3.5 和 LLaMA 2 70B，推理速度 6 倍

#### Gemini 家族 (Google)

Gemini 是 Google 的原生多模态模型系列，从设计之初就同时处理文本、图像、音频和视频。

| 版本 | 时间 | 亮点 |
|------|------|------|
| Gemini 1.0 Ultra | 2023.12 | 首个在多任务上超越 GPT-4 的模型 |
| Gemini 1.5 Pro | 2024.02 | MoE 架构，上下文长度达 1M-10M tokens |
| Gemini 2.0 Flash | 2024.12 | 原生工具使用，低延迟 |
| Gemini 2.5 Pro | 2025.03 | "thinking" 推理模型，Deep Think 模式 |

#### Claude 家族 (Anthropic)

Claude 系列的核心差异化在于安全性和对齐技术：

- **Constitutional AI (CAI)**：用一套"宪法"（原则/规则）指导模型行为，减少对人工反馈的依赖
- **RLHF 变体**：基于 CAI 的强化学习流程（Constitutional RL）
- Claude 3 (2024.03): Haiku / Sonnet / Opus 三个尺寸
- Claude 3.5 Sonnet (2024.06): 编码和推理能力行业领先
- Claude 4 (2025): Agentic 能力，计算机使用 (computer use)

#### Gemma (Google, 开源)

Google 的轻量级开源模型：

- Gemma 1 (2024.02): 2B/7B, GeGLU 激活
- Gemma 2 (2024.06): 2B/9B/27B, 知识蒸馏, 交替全局/局部注意力
- 定位：研究社区和轻量部署

#### Phi 系列 (Microsoft)

Phi 系列证明：**数据质量 >> 模型规模**。

| 版本 | 参数量 | 特点 |
|------|--------|------|
| Phi-1 | 1.3B | "教科书质量"数据，纯代码 |
| Phi-1.5 | 1.3B | 合成数据，常识推理 |
| Phi-2 | 2.7B | 超越 7B 模型的推理能力 |
| Phi-3 | 3.8B/7B/14B | 小模型达到 GPT-3.5 水平 |
| Phi-4 | 14B | 合成数据 + 课程学习 |

**核心方法论**：使用 LLM 生成高质量合成数据，按"课程学习"（curriculum learning）方式由简到繁训练。

---

## 6. 编码器-解码器类变体

### 6.1 T5 (Text-to-Text Transfer Transformer)

T5 (Raffel et al., 2020) 将**所有 NLP 任务统一为文本到文本的格式**：

```
翻译:     "translate English to German: Hello" → "Hallo"
分类:     "cola sentence: This is good." → "acceptable"
摘要:     "summarize: [long text...]" → "[summary...]"
QA:       "question: Who wrote Hamlet? context: Shakespeare was..." → "Shakespeare"
```

**预训练目标**：Span Corruption（跨度破坏）

随机用哨兵 token 替换连续的 span，要求模型恢复被替换的文本：

```
输入:  "Thank you <X> me to your party <Y> week"
目标:  "<X> for inviting <Y> last <Z>"
```

**架构规格**：

| 配置 | 编码器层 | 解码器层 | d_model | d_ff | 头数 | 参数 |
|------|---------|---------|---------|------|------|------|
| T5-Small | 6 | 6 | 512 | 2048 | 8 | 60M |
| T5-Base | 12 | 12 | 768 | 3072 | 12 | 220M |
| T5-Large | 24 | 24 | 1024 | 4096 | 16 | 770M |
| T5-3B | 24 | 24 | 1024 | 16384 | 32 | 3B |
| T5-11B | 24 | 24 | 1024 | 65536 | 128 | 11B |

T5 的"文本到文本"范式极大简化了多任务建模，启发了后续的 Prompt 工程。

---

### 6.2 BART

BART (Lewis et al., 2019) 是去噪自编码器（Denoising Autoencoder）：

```
架构: Bidirectional Encoder + Autoregressive Decoder
     (与原始 Transformer 完全相同)

预训练: 对输入文本施加各种噪声破坏，训练模型恢复原始文本

噪声类型:
  1. Token Masking:    随机掩盖 token
  2. Token Deletion:   随机删除 token
  3. Text Infilling:   用单个 [MASK] 替换连续的 span
  4. Sentence Shuffling: 打乱句子顺序
  5. Document Rotation:  随机旋转文档 (从随机位置开始)
```

BART 在生成式任务（摘要、翻译、对话）上表现突出，在理解任务上也与 RoBERTa 相当。

---

### 6.3 Whisper (OpenAI)

Whisper 是一个语音识别模型，使用编码器-解码器 Transformer：

```
语音输入 (Log-Mel Spectrogram)
    │
    ▼
┌─────────┐
│ Encoder  │  ← 2 层 1D 卷积 + Transformer Encoder
└────┬────┘
     │
     ▼
┌─────────┐      ┌──────────────────┐
│ Decoder  │ ───► │ "Hello, world."  │
└─────────┘      └──────────────────┘
```

Whisper 在 68 万小时的多语言多任务监督数据上训练，表现出强大的鲁棒性和泛化能力。

---

## 7. 视觉 Transformer

Transformer 架构的通用性使其在视觉领域也取得了突破性进展。

### 7.1 ViT (Vision Transformer, 2020)

ViT (Dosovitskiy et al., 2021) 证明了"纯 Transformer 可以直接应用于图像"：

```
图像 (224×224×3)
    │
    ▼ 分割为 14×14 的 patches
    │ 196 patches, 每 patch 16×16×3 = 768 维
    ▼
线性投影 (768 → D) + 位置编码
    │
    ▼
[class_token]  patch_1  patch_2  ...  patch_196
    │             │        │              │
    ▼             ▼        ▼              ▼
┌─────────────────────────────────────────┐
│          Transformer Encoder (L 层)      │
└────────────────────┬────────────────────┘
                     │
                     ▼
         MLP Head (使用 [class_token] 的输出)
                     │
                     ▼
              分类: "Golden Retriever"
```

**关键设计**：
- Patch 嵌入：将图像分割为固定大小的 patch，线性投影到 Transformer 维度
- [class_token]：类似 BERT 的 [CLS]，其最终隐藏状态用于分类
- 可学习的位置嵌入（1D 或 2D）

**局限**：ViT 需要大规模预训练数据（如 JFT-300M），在中小数据集上不如 CNN。

---

### 7.2 DeiT (Data-efficient Image Transformers, 2020)

DeiT (Touvron et al., 2021) 解决了 ViT 需要海量数据的问题：

**核心技术：知识蒸馏 (Knowledge Distillation)**

```
                    ┌─────────────────┐
  输入图像 ────────►│  ViT (Student)  │────► 分类损失
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │ Distillation    │────► 蒸馏损失 (与教师输出对比)
                    │ Token           │
                    └─────────────────┘
                             ▼
                  ┌──────────────────┐
                  │  CNN Teacher      │
                  │  (e.g., RegNetY)  │
                  └──────────────────┘
```

蒸馏 token 与 [class_token] 并行处理，其输出与教师的 soft label 对比计算蒸馏损失。DeiT 仅在 ImageNet-1K 上训练即可达到与 CNN 相当的性能。

---

### 7.3 Swin Transformer (2021)

Swin Transformer (Liu et al., 2021) 是视觉 Transformer 的一座里程碑，通过**层次化特征图**和**移位窗口**机制，将计算复杂度从 O(n²) 降至 O(n)。

```
Swin Transformer 架构:
  Stage 1: H/4 × W/4 × C  ──► Swin Block ×2
  Stage 2: H/8 × W/8 × 2C ──► Swin Block ×2
  Stage 3: H/16 × W/16 × 4C──► Swin Block ×6
  Stage 4: H/32 × W/32 × 8C──► Swin Block ×2

每个 Stage 之间通过 Patch Merging 降采样 (2×2→1, 通道翻倍)
```

**Swin Block 核心机制**：

```
W-MSA (Window Multi-Head Self-Attention):
  将特征图划分为 M×M 的窗口，只在窗口内计算自注意力
  复杂度: O(n · M²) , M=7 (远小于总 token 数)

SW-MSA (Shifted Window MSA):
  窗口在空间上偏移 (M/2, M/2)
  捕获跨窗口的交互
  使用"循环移位 (cyclic shift) + 掩码"实现高效计算

连续两个 Swin Block:
  Block l:   LN → W-MSA  → LN → MLP
  Block l+1: LN → SW-MSA → LN → MLP
```

Swin Transformer 因其 O(n) 复杂度和层次化特征，成为视觉骨干网络的首选之一，广泛应用于检测、分割等任务。

---

### 7.4 Transformers 在视觉生成中的应用

#### DALL-E 系列 (OpenAI)

- **DALL-E 1 (2021)**：基于 VQ-VAE + 自回归 Transformer，将图像编码为离散 token 序列后由 Transformer 建模
- **DALL-E 2 (2022)**：CLIP 潜在空间 + 扩散模型（从 CLIP 图像嵌入生成图像）
- **DALL-E 3 (2023)**：在图像描述上大幅改进，使用合成的详细描述训练

#### Stable Diffusion 系列 (Stability AI)

- **Stable Diffusion 1/2 (2022)**：潜在扩散模型 (Latent Diffusion Model)，在 VAE 的潜在空间中通过 U-Net（含交叉注意力层）进行去噪
- **SD3 (2024)**：用 DiT (Diffusion Transformer) 替代 U-Net
- **SD3.5 (2024)**：多模态 DiT (MMDiT)，文本和图像表示同时注入 Transformer

#### DiT (Diffusion Transformer) 架构

```
时间步 t ──► 时间嵌入 ──┐
标签 c ──► 标签嵌入  ──┤
                       ├──► DiT Block × N ──► Noise Prediction
Noised Latent ────────┘
```

#### Sora (OpenAI, 2024)

Sora 是世界首个大规模视频生成 Transformer，将视频生成视为"时空 patch"的序列建模：

```
视频 (T×H×W×C)
    │ 分割为 spacetime patches
    │ (t, h, w) → 编码为 latent tokens
    ▼
Diffusion Transformer (DiT) ◄── 文本条件注入
    │
    ▼
去噪 latent → 视频解码器 → 生成视频 (最长 60s)
```

Sora 的出现证明了 Transformer 的 scaling law 在视频领域同样适用。

---

### 7.5 CLIP (Contrastive Language-Image Pre-training)

CLIP (Radford et al., 2021) 使用双编码器架构，通过对比学习将视觉和语言映射到同一嵌入空间：

```
┌────────────────────────────────────────────────────┐
│                  CLIP 架构                          │
│                                                    │
│  图像 "一只狗"                          文本       │
│     │                                     │        │
│     ▼                                     ▼        │
│ ┌──────────┐                        ┌────────┐     │
│ │ Vision   │                        │ Text   │     │
│ │ Encoder  │                        │Encoder │     │
│ │(ViT/CNN) │                        │(Transf)│     │
│ └────┬─────┘                        └───┬────┘     │
│      │ I_1      I_2  ...  I_N          │ T_1 T_2  │
│      ▼                                  ▼          │
│  ┌───────────────────────────────────────────┐     │
│  │        Contrastive Loss (InfoNCE)         │     │
│  │  Maximize cos_sim(I_i, T_i)              │     │
│  │  Minimize cos_sim(I_i, T_j) for i ≠ j   │     │
│  └───────────────────────────────────────────┘     │
│                                                    │
│  训练数据: 4 亿 (图像, 文本) 对                      │
└────────────────────────────────────────────────────┘
```

CLIP 的零样本分类能力为多模态 AI 奠定了基础，并直接催生了 DALL-E 2 和 Stable Diffusion。

---

## 8. 长序列优化技术

标准 Transformer 的 O(n²) 复杂度是长序列建模的核心瓶颈。以下技术致力于解决这一问题。

### 8.1 稀疏注意力 (Sparse Attention)

#### Longformer (2020)

Longformer 使用滑动窗口注意力 + 全局注意力：

```
注意力模式 (w=3, 两个全局 token 在位置 1 和 9):
位置:   1   2   3   4   5   6   7   8   9   10
       ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
   1   │ ● │ ● │ ● │   │   │   │   │   │ ● │ ● │  全局token
   2   │ ● │ ● │ ● │ ● │   │   │   │   │   │   │
   3   │ ● │ ● │ ● │ ● │ ● │   │   │   │   │   │
   4   │   │ ● │ ● │ ● │ ● │ ● │   │   │   │   │
   5   │   │   │ ● │ ● │ ● │ ● │ ● │   │   │   │  滑动窗口 (w=3)
   6   │   │   │   │ ● │ ● │ ● │ ● │ ● │   │   │
   7   │   │   │   │   │ ● │ ● │ ● │ ● │ ● │   │
   8   │   │   │   │   │   │ ● │ ● │ ● │ ● │ ● │
   9   │ ● │ ● │   │   │   │   │ ● │ ● │ ● │ ● │  全局token
  10   │ ● │ ● │   │   │   │   │   │ ● │ ● │ ● │
       └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘

复杂度: O(n · w)  (w 为窗口大小, 通常 512)
```

少数"全局 token"（如 [CLS]、标点符号）可以关注所有位置并被所有位置关注，为模型保留了全局信息传递的能力。

#### BigBird (2020)

BigBird 在 Longformer 的基础上增加随机注意力：

```
注意力类型 (3 种模式):
  1. 滑动窗口注意力  (每个 token 关注相邻 w 个 token)
  2. 全局注意力        (少数 g 个 token 关注全体, 全体关注这 g 个)
  3. 随机注意力        (每个 token 随机关注 r 个其他 token)

复杂度: O(n · (w + g + r))
```

Zaheer et al. 从理论上证明，这种稀疏注意力模式保留了全注意力的表达能力。

---

### 8.2 低秩近似

#### Linformer (2020)

Linformer 观察到自注意力矩阵通常是低秩的（由 softmax 的集中效应导致），因此可以通过低秩投影将 n×n 的注意力矩阵近似为 n×k（k << n）：

```
标准: Attention = softmax(QK^T/√d) · V       O(n²·d)

Linformer: 对 K 和 V 做低秩投影
  K' = E · K       (n→k)
  V' = F · V       (n→k)
  Attention = softmax(Q·K'^T/√d) · V'         O(n·k·d)
```

复杂度从 O(n²) 降为 O(n·k)，其中 k 是投影维度（如 k=256）。

---

### 8.3 核方法近似

#### Performer (2021)

Performer 使用核方法将 softmax 注意力近似为线性注意力：

```
标准注意力:  Attention(Q,K,V) = softmax(QK^T/√d) · V

核近似:
  softmax(QK^T/√d) ≈ φ(Q) · φ(K)^T

其中 φ(x) 是 FAVOR+ (Fast Attention Via Orthogonal Random features) 特征映射

利用结合律:
  φ(Q) · (φ(K)^T · V)  先算 K^T·V (d×d), 再左乘 φ(Q) (n×d)

复杂度: O(n·d²·log(d))  (当 d << n 时近似线性)
```

这使得 Performer 首次能以可接受的计算成本处理超长序列（如 8K+ tokens 的蛋白质序列）。

---

### 8.4 FlashAttention (1/2/3)

FlashAttention (Dao et al., 2022; Dao, 2023; Shah et al., 2024) 是当前 LLM 训练和推理中最重要的注意力优化技术之一，已被 GPT-4、Gemini、LLaMA 3 等几乎所有主流模型采用。

#### 核心思想：IO 感知的精确注意力

FlashAttention 的关键洞察是：注意力计算的瓶颈不是计算量本身，而是 GPU 高带宽内存 (HBM) 和片上 SRAM 之间的数据传输。

```
GPU 内存层级:
  HBM (High Bandwidth Memory): 大容量 (40-80GB), 高延迟
  SRAM (Static RAM, 片上): 小容量 (~20MB per SM), 低延迟 (快 ~10x)

传统做法:
  1. 读 Q,K 从 HBM → 计算 S = QK^T → 写 S 回 HBM (O(n²) 中间结果!)
  2. 读 S → 计算 softmax(S) → 写 P 回 HBM
  3. 读 P, V → 计算 O = PV → 写 O

FlashAttention:
  Tiling (分块): 将 Q,K,V 切分为小块, 逐块加载到 SRAM
  Recomputation: 不存储中间注意力矩阵, 反向传播时重新计算

  HBM 读写: O(n²·d²/M)  (M 为 SRAM 大小) — 显著减少
```

#### 各版本对比

| 版本 | 年份 | GPU 目标 | 关键改进 | 加速比 |
|------|------|---------|---------|--------|
| FA1 | 2022 | A100 | Tiling + 在线 Softmax | 2-4× (vs 标准实现) |
| FA2 | 2023 | A100/H100 | 优化 non-matmul, 并行策略 | 2-3× (vs FA1) |
| FA3 | 2024 | H100 | TMA, WGMMA, FP8 | 1.5-2× (vs FA2) |

FlashAttention 的出现，使得在单卡上训练和推理百万 token 长度的上下文成为现实，是 2023-2025 年长上下文 LLM 爆发的重要推动力。

---

### 8.5 Reformer (2020)

两种技术：
1. **LSH (Locality Sensitive Hashing) 注意力**：用 LSH 对 Q 和 K 做哈希，只计算同一桶内的注意力
2. **可逆残差层 (Reversible Residuals)**：每层可根据输出恢复输入，无需存储中间激活，节省内存

---

## 9. 混合专家模型（MoE）

MoE (Mixture of Experts) 并非新概念（Jacobs et al., 1991），但直到 2021 年在 Transformer 上规模化应用后才真正进入主流。

### 9.1 核心概念：稀疏激活

MoE 的核心思想是：模型拥有多个"专家"子网络（通常是 FFN 层），但对于每个 token，只有少部分专家被激活。

```
┌────────────────────────────────────────────────────────┐
│              MoE Layer 架构                             │
│                                                        │
│  输入 x (n tokens, d_model)                            │
│     │                                                  │
│     ├─────────────────┬──────────────────┐             │
│     │                 │                  │             │
│     ▼                 ▼                  ▼             │
│ ┌────────┐       ┌────────┐        ┌────────┐         │
│ │Expert 1│       │Expert 2│   ...  │Expert N│         │
│ │ (FFN)  │       │ (FFN)  │        │ (FFN)  │         │
│ └───┬────┘       └───┬────┘        └───┬────┘         │
│     │                 │                  │             │
│     └─────────────────┼──────────────────┘             │
│                       │                                │
│                       ▼                                │
│            ┌─────────────────────┐                     │
│            │   加权求和          │                     │
│            │ y = Σ g_i·E_i(x)   │                     │
│            └─────────────────────┘                     │
│                                                        │
│  同时:                                                 │
│     │                                                  │
│     ▼                                                  │
│ ┌──────────────────────────┐                           │
│ │  Router/Gate (线性层)     │                           │
│ │  g(x) = TopK(softmax     │                           │
│ │         (W_g · x + b_g)) │                           │
│ └──────────────────────────┘                           │
└────────────────────────────────────────────────────────┘
```

### 9.2 门控机制 (Gating/Router)

**标准 Top-K 门控**：

```
g(x) = softmax(W_g · x)           # 所有专家的概率分布
Selected = TopK(g(x), K)          # 选择概率最高的 K 个
g'(x) = softmax(Selected_scores)  # 在被选中的专家间重新归一化
y = Σ_{i in Selected} g'(x)_i · Expert_i(x)
```

**噪声 Top-K 门控 (Noisy Top-K Gating)**（Shazeer et al., 2017）：

```
H(x) = (W_g · x) + ε · softplus(W_noise · x)    # 标准正态噪声
Selected = TopK(H(x), K)
```

添加可学习的高斯噪声鼓励探索，防止路由器过早锁定在某些专家上。

### 9.3 负载均衡 (Load Balancing)

MoE 的一个核心挑战是**负载不均衡**：某些专家可能"被冷落"（接收很少的 token），而某些专家"过载"。

**辅助损失 (Auxiliary Loss)**：

```
L_aux = α · N · Σ_{i=1}^{N} f_i · P_i

其中:
  f_i = 分配给专家 i 的 token 比例
  P_i = 路由器对专家 i 的平均概率
  N = 专家总数
  α = 超参数 (控制负载均衡强度)
```

最小化此损失等价于鼓励均匀分配。

**DeepSeek 的无辅助损失方法**：

DeepSeek-V3 提出了一种"无辅助损失的负载均衡策略"：每个专家维护一个动态偏差项 `b_i`，当某专家接收 token 过多时降低其偏差（降低被选中的概率），反之提升。这种策略在不牺牲模型性能的前提下实现了负载均衡。

### 9.4 Switch Transformer (2021)

Fedus et al. 提出的 Switch Transformer 将 Top-K 路由简化为 **Top-1 (K=1)**：

每个 token 仅路由到概率最高的那一个专家。通过"专家容量"概念处理不均衡：

```
Expert Capacity = (tokens_per_batch / num_experts) × capacity_factor

其中 capacity_factor > 1 提供缓冲, 超出容量的 token 被"丢弃"
(通过残差连接直接传递到下一层)
```

Switch Transformer 将模型参数规模推至 **1.6T**，同时保持了计算效率。

### 9.5 DeepSeekMoE

DeepSeekMoE 在 DeepSeek-V2/V3 中提出，包含两个关键创新：

1. **细粒度专家**：将大型 FFN 专家拆分为更多、更小的专家（如 256 个细粒度专家），提升专家的专业化和组合灵活度
2. **共享专家**：设置少量（如 1-2 个）"共享专家"，所有 token 都会被路由到共享专家，确保基本知识的覆盖

```
对于每个 token:
  y = SharedExpert(x) + Σ_{i in TopK(Routed)} g_i · Expert_i(x)

  DeepSeek-V3: 1 共享 + Top-8(256 路由) = 9 个专家/token
```

### 9.6 MoE 的优缺点

**优点**：
- 计算效率：增加参数量的同时几乎不增加计算量（稀疏激活）
- 专家专业化：不同专家自动学习不同的知识/模式
- 更好的 scaling：同等计算预算下效果优于密集模型

**缺点**：
- 负载均衡难题：需要精心设计的路由和训练策略
- 通信开销：分布式训练中 expert 间的 all-to-all 通信成本高
- 微调困难：MoE 模型对微调更敏感，容易过拟合或崩溃
- 推理内存：虽然计算量小，但需加载全部专家权重到内存

### 9.7 代表性 MoE 模型

| 模型 | 总参数 | 激活参数 | 专家数 | Top-K | 年份 |
|------|--------|---------|--------|-------|------|
| Switch Transformer | 1.6T | ~32B | 2048 | 1 | 2021 |
| GLaM | 1.2T | ~97B | 64 | 2 | 2021 |
| Mixtral 8×7B | 46.7B | 12.9B | 8 | 2 | 2023 |
| GPT-4 (推测) | ~1.8T | ~220B | 8 | 2 | 2023 |
| DeepSeek-V2 | 236B | 21B | 160 | 6+2 | 2024 |
| DeepSeek-V3 | 671B | 37B | 256+1 | 8+1 | 2024 |
| Qwen2.5-MoE | ~57B | ~14B | 64 | 8 | 2024 |
| Gemini 1.5 Pro | - | - | - | - | 2024 |

---

## 10. 状态空间模型（Mamba）

状态空间模型 (State Space Models, SSMs) 是近年来除 Transformer 外最受关注的序列建模框架，其 O(n) 的线性复杂度使其在长序列建模上具有天然优势。

### 10.1 连续时间状态空间模型

连续时间 SSM 通过一组微分方程描述序列到序列的映射：

```
x'(t) = A · x(t) + B · u(t)      (状态方程)
y(t)  = C · x(t) + D · u(t)      (输出方程)

其中:
  u(t) ∈ R: 输入信号
  x(t) ∈ R^N: 隐藏状态 (N 维)
  y(t) ∈ R: 输出信号
  A ∈ R^{N×N}: 状态转移矩阵
  B ∈ R^{N×1}: 输入投影矩阵
  C ∈ R^{1×N}: 输出投影矩阵
  D ∈ R: 前馈项 (通常省略或设为 0)
```

这与 RNN 在数学形式上高度相似，核心区别在于 SSM 的 A, B, C 矩阵有特殊的参数化方式以实现长程记忆。

### 10.2 离散化：零阶保持 (ZOH)

将连续 SSM 离散化以用于深度学习：

```
Ā = exp(Δ · A)
B̄ = (Δ · A)^{-1} (exp(Δ · A) - I) · Δ · B
   ≈ Δ · B                       (一阶近似)

离散递归:
  x_k = Ā · x_{k-1} + B̄ · u_k
  y_k = C · x_k
```

Δ 是离散化步长，控制模型对当前输入的"关注"程度：小 Δ 倾向于忽略当前输入（关注过去），大 Δ 倾向于关注当前输入（类似遗忘门）。

### 10.3 HiPPO 矩阵 (High-order Polynomial Projection Operators)

HiPPO (Gu et al., 2020) 解决了 SSM 如何记忆长程历史的问题。HiPPO 矩阵是一种特殊构造的 A 矩阵，使得隐藏状态 x(t) 能够最优地"压缩"历史输入 u(τ) 的信息（在 L2 意义上）：

```
HiPPO-LegS (Scaled Legendre):
  A_{nk} = -{(2n+1)^{1/2} (2k+1)^{1/2},  if n > k
           {-(n+1),                       if n = k
           {0,                            if n < k
```

这个矩阵保证了状态空间模型理论上具有无限长程记忆能力。

### 10.4 S4 (Structured State Space)

S4 (Gu et al., 2022) 是首个有效将 SSM 应用于长序列建模的工作，核心是将 A 矩阵参数化为对角加低秩（DPLR）形式，使得 SSM 可通过卷积模式高效计算：

```
卷积核: K̄ = (CB̄, CĀB̄, CĀ²B̄, ..., CĀ^{L-1}B̄)

输出: y = K̄ * u      (整个序列通过一次卷积计算!)

时间复杂度: O(L·log(L))  (通过 FFT 加速卷积)
```

但 S4 的 A, B, C 在序列所有位置共享，这限制了其内容感知能力——它对所有 token "一视同仁"，无法像注意力那样选择性关注。

### 10.5 Mamba-1 (2023)：选择性 SSM

Mamba (Gu & Dao, 2023) 的关键突破是让 SSM 的 B, C, Δ 依赖于输入：

```
Δ(x) = softplus(W_Δ · x + b_Δ)       # 输入依赖的步长
B(x) = W_B · x                        # 输入依赖的输入投影
C(x) = W_C · x                        # 输入依赖的输出投影

A 保持不变 (使用 HiPPO 矩阵), 但 Δ 在 Ā = exp(Δ·A) 中起作用
```

**选择性 SSM 的含义**：
- 当 Δ(x) 较小时，Ā ≈ I（忽略当前输入，保留历史信息）
- 当 Δ(x) 较大时，Ā ≈ 0（重置状态，聚焦当前输入）
- B(x) 和 C(x) 则根据内容动态调整信息的"写入"和"读取"

这相当于在每个时间步有一个"内容感知的门控机制"，其表达力远超标准 SSM，接近注意力机制。

#### 硬件感知算法

Mamba 的核心工程创新是将选择性 SSM 的实现与 GPU 硬件深度耦合：

```
传统实现问题:
  - 选择性 SSM 不能用全局卷积 (B 和 C 是输入依赖的)
  - 必须按递归模式计算, 看似成了 O(n) 的 RNN
  - 但递归计算在 GPU 上效率极低 (内存带宽受限)

Mamba 的解决方案:
  1. Kernel Fusion: 将离散化、状态更新、扫描合并为一个 CUDA kernel
  2. Parallel Scan (并行扫描): 利用结合律将递归转化为并行计算
  3. Recomputation: 反向传播时不存储中间状态, 在 SRAM 中重新计算
     (类似 FlashAttention 的策略)
```

#### Mamba Block 结构

```
输入 x
  │
  ├─────────────────────────┐
  │                         │
  ▼                         ▼
Linear (→ d_inner)      Linear (→ d_inner)
  │                         │
  ▼                         │
1D Conv (depthwise)         │
  │                         │
  ▼                         │
SiLU 激活                   │
  │                         │
  ▼                         │
SSM (选择性) + 残差          │
  │                         │
  ▼                         │
SiLU(门控分支) · SSM输出 ◄──┘
  │
  ▼
Linear (→ d_model)
  │
  └── + x (残差连接)
  │
  ▼
输出
```

---

### 10.6 Mamba-2 (2024)：结构化状态空间对偶性

Mamba-2 (Dao & Gu, 2024) 揭示了 SSM 和线性注意力之间的深刻数学联系——**结构化状态空间对偶性 (Structured State Space Duality, SSD)**：

```
Mamba-2 的核心发现:

SSM 的卷积形式 (S4):
  y_t = Σ_{s=0}^{t} C·A^{t-s}·B·u_s

当 A 为标量矩阵 (所有通道共享) 时:
  y_t = Σ_{s=0}^{t} C·a^{t-s}·B·u_s
  
推广到矩阵形式:
  L 是多尺度衰减矩阵: L_{ij} = a_i · a_{i-1} · ... · a_{j+1}

则: Y = (L ⊙ (Q·K^T)) · V

  这正是多尺度门控的线性注意力!
```

**SSD 的实用价值**：
- Mamba-2 的 chunkwise 算法：支持张量并行
- 在 8×H100 上的扩展效率远超 Mamba-1
- 训练吞吐量达到 Transformer 的 2-8 倍（取决于序列长度）

---

### 10.7 Mamba-3 (2026)

Mamba-3 在 2026 年初发布，代表了 SSM 架构的最新进展：

**关键改进**：
1. **改进的状态空间参数化**：基于更强理论基础的矩阵初始化
2. **长度泛化**：通过特殊的 SSM 设计实现训练长度外推
3. **MoE + SSM 深度融合**：在 SSM 层中也引入专家混合

---

### 10.8 其他 SSM/RNN 架构

#### RWKV (Receptance Weighted Key Value)

RWKV 是一种"可并行训练的 RNN"，其核心公式同时支持类 Transformer 的并行训练和类 RNN 的串行推理：

```
并行模式 (训练):
  wkv_t = Σ_{i=0}^{t-1} e^{-(t-1-i)·w + k_i} · v_i / Σ_{i=0}^{t-1} e^{-(t-1-i)·w + k_i}

  其中 w 是学习到的通道级衰减参数 (控制遗忘速率)

串行模式 (推理):
  a_t = e^{-w}·a_{t-1} + e^{k_t}·v_t      (分子状态)
  b_t = e^{-w}·b_{t-1} + e^{k_t}           (分母状态)
  wkv_t = a_t / b_t

输出: o_t = σ(r_t) ⊙ wkv_t
```

#### RetNet (Retentive Network)

RetNet (Sun et al., 2023) 提出了"保留机制 (Retention Mechanism)"，支持三种等效表示：

```
1. 并行表示 (训练): Retention(X) = (Q·K^T ⊙ D) · V
   D 是带指数衰减矩阵: D_{ij} = γ^{i-j} (i≥j), 0 (i<j)

2. 递归表示 (推理): S_n = γ·S_{n-1} + K_n^T·V_n
   Retention(X_n) = Q_n·S_n

3. 分块递归 (混合): 块内并行 + 块间递归
```

#### xLSTM (Extended LSTM)

xLSTM (Beck et al., 2024) 是对经典 LSTM 的现代化改造：

- **sLSTM (Scalar LSTM)**：使用指数门控（exponential gating）替代 sigmoid，并引入新的记忆混合
- **mLSTM (Matrix LSTM)**：将标量细胞状态升级为矩阵形式，实现完全的并行化训练

```
mLSTM 的核心:
  C_t = f_t·C_{t-1} + i_t·(V_t^T·K_t)          (矩阵累积器, d×d)
  h_t = o_t ⊙ (C_t·Q_t)                        (矩阵查询)
```

矩阵记忆使 mLSTM 可以存储更多信息，性能超过 Transformer 和 Mamba。

### 10.9 SSM vs Transformer 对比

| 维度 | Transformer (标准) | Mamba/SSM |
|------|-------------------|-----------|
| 每步复杂度 | O(n²·d) | O(n·d) |
| 训练并行性 | 完全并行 | 需并行扫描 (kernel fusion) |
| 推理 | 需 KV Cache, O(n) 内存/步 | 固定状态, O(1) 内存/步 |
| 长程依赖 | 全局, 直接 | 间接, 通过状态传递 |
| 内容感知 | 强 (softmax 注意力) | 选择性 SSM (Mamba-1 起) |
| 硬件利用率 | 高 (矩阵乘法为主) | 中 (需特殊 kernel) |
| 生态成熟度 | 非常成熟 | 快速发展中 |

### 10.10 混合架构

将 Transformer 和 SSM 的长处结合是当前趋势：

| 模型 | 策略 |
|------|------|
| **Jamba** (AI21 Labs, 2024) | Mamba 层 + MoE Transformer 层交替 |
| **Griffin** (DeepMind, 2024) | 2 个 RNN 层 + 1 个注意力层 (2:1) |
| **Hawk** (DeepMind, 2024) | 纯线性 RNN (MLP-based)，无注意力 |
| **MambaFormer** | 注意力层和 Mamba 层交替排列 |
| **Zamba** (Zyphra) | SSM + 少量全局注意力层 |
| **DART** (MIT/NVIDIA, 2025) | 动态选择注意力或 Mamba 层 |

---

## 11. 其他前沿架构

### 11.1 线性注意力 (Linear Attention)

线性注意力通过核技巧将标准注意力的 O(n²) 复杂度降至 O(n)：

```
标准注意力:  O = softmax(QK^T/√d) · V

线性注意力:  O = φ(Q) · (φ(K)^T · V) / (φ(Q) · φ(K)^T · 1)

  其中 φ(·) 是特征映射 (如 ReLU, ELU+1, Softmax 近似)
  利用结合律先计算 K^T·V (d×d), 再左乘 φ(Q)
```

变体：
- **Linear Transformer** (Katharopoulos et al., 2020): φ(x) = elu(x) + 1
- **cosFormer** (Qin et al., 2022): 使用余弦加权替代 softmax，保持局部偏差
- **FLASH** (Hua et al., 2022): 门控线性注意力 + 局部卷积混合

### 11.2 H3 (Hungry Hungry Hippos)

H3 (Fu et al., 2023) 是 S4 和注意力的"语言建模"专用混合体，其关键设计是使用两个 SSM——一个用于"记住"重要的 token（模拟 K），另一个用于上下文压缩（模拟 V），配合一个移位操作（模拟 Q）。H3 在语言建模上首次让 SSM 达到 Transformer 水平。

### 11.3 Hyena Hierarchy

Hyena (Poli et al., 2023) 使用**隐式卷积**替代自注意力：

```
Hyena 的核心: 用长程卷积替代注意力
  O = H(q) · v   其中 H 是输入依赖的卷积算子

  使用快速傅里叶变换 (FFT) 高效计算:
  H(q) = FFT^{-1}(FFT(h_q) ⊙ FFT(v))
```

Hyena 将次二次复杂度的 long convolution 推到了接近注意力的质量水平。

### 11.4 RMT (Recurrent Memory Transformer)

RMT 通过引入显式的"记忆 token"来处理超长序列。记忆 token 随序列一起被处理，并在不同 segment 之间传递：

```
Segment 1: [mem_1 ... mem_k, token_1 ... token_n]
            处理 → 更新后的 [mem_1 ... mem_k]

Segment 2: [mem_1 ... mem_k, token_{n+1} ... token_{2n}]
            处理 → ...

通过记忆 token 传递跨 segment 的信息
```

### 11.5 Monarch Mixer

Monarch Mixer (Fu et al., 2024) 使用 Monarch 矩阵分解替代注意力：

```
Monarch 矩阵: M = P · L · P^T · R · P

其中 P 是排列矩阵, L 是块对角矩阵, R 是"逆"块对角矩阵
Monarch 矩阵参数量的 O(n^{3/2}), 远小于注意力 O(n²)
```

---

## 12. 总结对比表

### 12.1 编码器模型

| 模型 | 年份 | 参数量 | 位置编码 | 激活函数 | 上下文 | 关键创新 | 主要用途 |
|------|------|--------|---------|---------|--------|---------|---------|
| BERT_base | 2019 | 110M | Learned Abs | GELU | 512 | MLM + NSP | 分类、NER、QA |
| BERT_large | 2019 | 340M | Learned Abs | GELU | 512 | MLM + NSP | 分类、NER、QA |
| RoBERTa | 2019 | 355M | Learned Abs | GELU | 512 | 动态掩码，无NSP | 分类、检索 |
| ALBERT | 2020 | 12-235M | Learned Abs | GELU | 512 | 参数分解+共享 | 分类、NER |
| ELECTRA | 2020 | 14-335M | Learned Abs | GELU | 512 | RTD 预训练 | 分类、NER |
| DeBERTa | 2021 | 100M-1.5B | Disentangled | GELU | 512 | 解耦注意力 | 分类、NLU |
| ModernBERT | 2024 | 139-395M | RoPE | GeGLU | 8192 | FlashAttn, RoPE | 检索、编码 |

### 12.2 解码器模型（大语言模型）

| 模型 | 年份 | 总参数 | 激活参数 | 层数 | 类型 | 上下文 | 位置编码 | 关键技术 |
|------|------|--------|---------|------|------|--------|---------|---------|
| GPT-1 | 2018 | 117M | 117M | 12 | Dense | 512 | Learned | 生成式预训练+微调 |
| GPT-2 | 2019 | 1.5B | 1.5B | 48 | Dense | 1024 | Learned | Zero-shot 范式 |
| GPT-3 | 2020 | 175B | 175B | 96 | Dense | 2048 | Learned | In-Context Learning |
| InstructGPT | 2022 | 175B | 175B | 96 | Dense | 2048 | Learned | RLHF (RM+PPO) |
| GPT-4 | 2023 | ~1.8T* | ~220B* | - | MoE | 8-128K | - | MoE, 多模态 |
| LLaMA 1 | 2023 | 7-65B | 7-65B | 32-80 | Dense | 2048 | RoPE | SwiGLU, RMSNorm |
| LLaMA 2 | 2023 | 7-70B | 7-70B | 32-80 | Dense | 4096 | RoPE | GQA, RLHF |
| LLaMA 3 | 2024 | 8-405B | 8-405B | 32-126 | Dense | 8K | RoPE | 15T tokens |
| DeepSeek-V2 | 2024 | 236B | 21B | 60 | MoE | 128K | RoPE | MLA, DeepSeekMoE |
| DeepSeek-V3 | 2024 | 671B | 37B | 61 | MoE | 128K | RoPE | FP8, MTP |
| DeepSeek-R1 | 2025 | 671B | 37B | 61 | MoE | 128K | RoPE | GRPO 推理训练 |
| Qwen 2 | 2024 | 0.5-72B | - | - | Dense/MoE | 32-128K | RoPE | GQA, 多语言 |
| Qwen 3 | 2025 | - | - | - | MoE/Dense | 128K+ | RoPE | 双模式(thinking/non) |
| Mixtral 8×7B | 2023 | 46.7B | 12.9B | 32 | MoE | 32K | RoPE | SWA, GQA, MoE |
| Phi-4 | 2024 | 14B | 14B | - | Dense | - | RoPE | 合成数据+课程学习 |
| Gemma 2 | 2024 | 2-27B | 2-27B | - | Dense | 8K | RoPE | GeGLU, 交替注意力 |
| Claude 3.5 | 2024 | - | - | - | - | 200K | - | Constitutional AI |
| Gemini 1.5 Pro | 2024 | - | - | - | MoE | 1M-10M | - | 超长上下文 |

> *GPT-4 架构参数为社区推测，官方未确认。

### 12.3 编码器-解码器模型

| 模型 | 年份 | 参数量 | 预训练目标 | 关键特点 | 主要用途 |
|------|------|--------|-----------|---------|---------|
| T5 | 2020 | 60M-11B | Span Corruption | 统一 Text-to-Text 框架 | 翻译、摘要、QA |
| BART | 2019 | 140-406M | 多噪声去噪 | 任意噪声函数 | 摘要、生成 |
| Whisper | 2022 | 39M-1.5B | 监督学习 | 68 万小时语音 | 语音识别 |

### 12.4 视觉模型

| 模型 | 年份 | 架构 | 关键技术 | 主要用途 |
|------|------|------|---------|---------|
| ViT | 2021 | Encoder-only | Patch Embedding | 图像分类 |
| DeiT | 2021 | Encoder-only + KD | 知识蒸馏 | 图像分类 |
| Swin | 2021 | Encoder-only (窗口) | 移位窗口注意力 | 通用视觉骨干 |
| CLIP | 2021 | Dual Encoder | 对比学习 | 多模态对齐 |
| DALL-E 2 | 2022 | Diffusion + CLIP | CLIP 潜空间 | 文本到图像 |
| SD3 | 2024 | DiT | MMDiT | 文本到图像 |
| Sora | 2024 | DiT + spacetime patches | 视频扩散 | 文本到视频 |

### 12.5 SSM/非 Transformer 模型

| 模型 | 年份 | 类型 | 复杂度 | 关键创新 |
|------|------|------|--------|---------|
| S4 | 2022 | Structured SSM | O(n·log n) | HiPPO + NPLR |
| Mamba-1 | 2023 | Selective SSM | O(n) | 选择性 + 硬件融合 |
| Mamba-2 | 2024 | SSD | O(n) | SSM-Attention 对偶性 |
| Mamba-3 | 2026 | Improved SSD | O(n) | 更好的长度泛化 |
| RWKV v6 | 2024 | 可并行 RNN | O(n) | 时间衰减 + 通道混合 |
| RetNet | 2023 | Retention | O(n) | 三模式表示 |
| xLSTM | 2024 | 扩展 LSTM | O(n)/O(n²) | 矩阵记忆 + 指数门控 |
| Griffin | 2024 | 混合 | O(n) | 实时门控线性循环 |

### 12.6 关键注意力/效率技术

| 技术 | 年份 | 原理 | 加速比 | 是否精确 | 采用模型 |
|------|------|------|--------|---------|---------|
| FlashAttention-1 | 2022 | Tiling + 在线Softmax | 2-4× | 精确 | 通用 |
| FlashAttention-2 | 2023 | 优化 non-matmul | 2-3× (vs FA1) | 精确 | GPT-4, LLaMA 3 |
| FlashAttention-3 | 2024 | H100 专属 (TMA) | 1.5-2× (vs FA2) | 精确 | 最新 LLM |
| Longformer | 2020 | 滑动窗口+全局 | - | 近似 | 长文档编码 |
| Performer | 2021 | 核方法 (FAVOR+) | - | 近似 | 蛋白质/基因组 |
| Linformer | 2020 | 低秩投影 | - | 近似 | 研究用途 |

---

## 13. 专业名词解释

### A

**Adam (Adaptive Moment Estimation)**：结合动量和自适应学习率的优化算法，是 Transformer 系列模型的默认优化器。维护梯度的一阶矩（均值）和二阶矩（未中心化方差）的指数衰减估计。

**Alignment Score (对齐分数)**：在注意力机制中，衡量解码器当前位置与编码器某个位置之间相关性的标量，通常记为 `e_{ij}`。经过 softmax 归一化后成为注意力权重 `α_{ij}`。

**Attention Weight (注意力权重)**：对齐分数经过 softmax 归一化后的结果，表示解码器当前位置对编码器各位置的"关注"程度，所有位置权重之和为 1。

**Autoregressive (自回归)**：序列生成模式，当前输出依赖于之前所有时刻的输出。GPT 系列模型均采用自回归生成。

**Auxiliary Loss (辅助损失)**：在主损失函数之外添加的辅助目标函数。在 MoE 中用于鼓励专家间的负载均衡。

### B

**Back-Propagation Through Time (BPTT，通过时间的反向传播)**：RNN 的训练算法，将 RNN 沿时间展开为深度前馈网络后进行标准反向传播。BPTT 中的梯度连乘是梯度消失/爆炸的根源。

**Beam Search (束搜索)**：在序列生成过程中，同时保留 B 个最有可能的部分序列（beam size B），并在每步扩展和剪枝，以近似全局最优解。

**Bidirectional RNN (双向 RNN)**：使用两个 RNN 分别从前向后和从后向前处理序列，捕获两个方向的上下文信息。

**Byte-Pair Encoding (BPE, 字节对编码)**：一种子词分词算法，以字节为初始词表，迭代合并最频繁的字节对。

### C

**Causal Mask (因果掩码)**：在解码器自注意力中使用的上三角掩码，确保位置 i 只能关注位置 j ≤ i，防止信息从未来泄露。

**Cell State (细胞状态)**：LSTM 中的"记忆高速公路"，通过门控机制控制信息的写入和擦除，可以跨越多个时间步近乎无损地传递信息。

**Chain-of-Thought (CoT, 思维链)**：在提示中引导模型逐步推理的技术，显著提升复杂推理任务的性能。

**Constitutional AI (CAI, 宪法式 AI)**：Anthropic 提出的对齐方法，用一套"宪法"（原则集合）指导模型行为，而非完全依赖人工反馈。

**Context Vector (上下文向量)**：注意力机制中，编码器隐藏状态按其注意力权重加权求和的结果，`c_i = Σ α_{ij}·h_j`。

**Cross-Attention (交叉注意力)**：Q 来自解码器，K 和 V 来自编码器的注意力形式，用于连接编码器和解码器的信息。

### D

**Decoder-Only (纯解码器)**：仅使用 Transformer 解码器部分的架构（如 GPT 系列）。使用因果掩码的自注意力，自回归生成。

**Diffusion Model (扩散模型)**：生成模型的一种，通过逐步向数据添加噪声（前向过程），然后学习逆转这一过程（反向过程）来生成数据。

**Dropout**：随机丢弃神经元输出的正则化技术，防止过拟合。Transformer 中通常 dropout=0.1。

### E

**Emergent Abilities (涌现能力)**：小模型上不存在，但在模型规模达到一定阈值后突然出现的能力。

**Encoder-Decoder (编码器-解码器)**：由编码器（处理输入）和解码器（生成输出）组成的架构，如原始 Transformer、T5、BART。

**Encoder-Only (纯编码器)**：仅使用 Transformer 编码器部分的架构（如 BERT 系列）。双向自注意力，适合理解任务。

**Exposure Bias (曝光偏差)**：Teacher Forcing 导致的训练和推理不一致问题。

### F

**Feed-Forward Network (FFN, 前馈网络)**：Transformer 层中接在自注意力之后的两个线性变换（中间有非线性激活），对每个位置独立应用。

**Few-Shot Learning (少样本学习)**：提供少量示例（通常 2-64 个）供模型进行上下文学习，无需参数更新。

**FlashAttention**：IO-感知的精确注意力算法，通过分块计算（Tiling）和重计算策略大幅减少 GPU 高带宽内存的读写量。

**Forget Gate (遗忘门)**：LSTM 中的门控机制，`f_t = σ(W_f·[h_{t-1}, x_t] + b_f)`，控制从细胞状态中丢弃哪些旧信息。

### G

**Gated Recurrent Unit (GRU, 门控循环单元)**：LSTM 的简化变体，使用更新门和重置门两个门控，将细胞状态和隐藏状态合并。

**GELU (Gaussian Error Linear Unit)**：`GELU(x) = x·Φ(x)`（Φ 为标准正态累积分布函数），是 BERT 和 GPT-1/2 使用的激活函数。

**Grouped Query Attention (GQA, 分组查询注意力)**：将查询头分组，每组共享同一个 KV 头，在 MHA 和 MQA 之间折中。LLaMA 2/3 等使用 GQA 显著减少 KV Cache。

**Gradient Clipping (梯度裁剪)**：限制梯度范数的技术，防止梯度爆炸。当 `||g|| > threshold` 时缩放梯度。

**GRPO (Group Relative Policy Optimization)**：DeepSeek-R1 使用的强化学习算法，通过对同一问题的多个采样输出进行组内相对排名来估计优势函数，无需额外的价值模型。

### H

**Hidden State (隐藏状态)**：RNN/LSTM 中每个时间步的状态向量，编码了到目前为止的序列历史信息。

**HiPPO (High-order Polynomial Projection Operators)**：一种特殊的 SSM 状态矩阵参数化方法，使 SSM 能够在线性递归框架下最优地记忆长程历史信息。

### I

**In-Context Learning (上下文学习)**：GPT-3 首创的范式，通过在提示中提供示例，无需梯度更新即可让模型适应新任务。

**Input Gate (输入门)**：LSTM 中的门控机制，`i_t = σ(W_i·[h_{t-1}, x_t] + b_i)`，决定向细胞状态写入多少新候选信息。

### K

**KV Cache (键值缓存)**：自回归解码器推理时，将已生成的 token 的 K 和 V 向量缓存起来，避免每步重新计算。长上下文推理中 KV Cache 是主要的内存瓶颈。

### L

**Label Smoothing (标签平滑)**：将 one-hot 标签替换为平滑分布 `y_smooth = (1-ε)·y_onehot + ε/K`，其中 K 为类别数。提高泛化能力。

**Layer Normalization (层归一化, LayerNorm)**：沿特征维度进行归一化（而非 batch 维度），`y = γ·(x-μ)/σ + β`。适合 NLP 的变长序列场景。

**Long Short-Term Memory (LSTM, 长短期记忆网络)**：通过门控机制和独立的细胞状态解决 RNN 梯度消失问题的序列模型。

### M

**Masked Language Model (MLM, 掩码语言模型)**：BERT 的核心预训练任务，随机掩盖部分输入 token 并预测其原始值。

**Mixture of Experts (MoE, 混合专家模型)**：包含多个"专家"子网络（通常为 FFN 层），通过路由器为每个 token 选择激活部分专家的架构范式。

**Multi-Head Attention (MHA, 多头注意力)**：将 Q、K、V 线性投影到多个低维子空间，并行计算注意力，然后拼接和投影。

**Multi-Head Latent Attention (MLA, 多头潜在注意力)**：DeepSeek-V2 提出的注意力变体，通过低秩压缩将 KV Cache 大幅缩减。

### N

**Next Sentence Prediction (NSP, 下一句预测)**：BERT 的第二个预训练任务，判断句子 B 是否是句子 A 的下一句。RoBERTa 发现其收益有限。

### O

**Output Gate (输出门)**：LSTM 中的门控机制，`o_t = σ(W_o·[h_{t-1}, x_t] + b_o)`，控制从细胞状态输出多少信息作为隐藏状态。

### P

**Perplexity (困惑度)**：语言模型评估指标，定义为交叉熵损失的指数，`PPL = exp(cross-entropy loss)`。值越低越好。

**Positional Encoding (位置编码)**：由于自注意力是排列等变的，需要显式注入位置信息。方法包括正弦固定编码、可学习编码和旋转编码（RoPE）。

**Post-LN vs Pre-LN**：LayerNorm 放置在残差连接之后（Post-LN）还是之前（Pre-LN）。Pre-LN 训练更稳定，是现代默认选择。

**Pre-training (预训练)**：在大规模无标注数据上训练基础模型，学习通用的语言/视觉表示，随后为下游任务微调。

### R

**Receptive Field (感受野)**：模型某层输出能"看到"的原始输入范围。Transformer 的感受野是全局的。

**Recurrent Neural Network (RNN, 循环神经网络)**：通过隐藏状态在时间步之间循环传递信息的神经网络架构。

**Reinforcement Learning from Human Feedback (RLHF, 基于人类反馈的强化学习)**：三步对齐流程（SFT → RM → PPO），将人类偏好融入语言模型训练。

**Residual Connection (残差连接)**：`Output = x + F(x)`，将输入直接加到子层输出上，是训练深层 Transformer 的关键。

**RMSNorm (Root Mean Square Layer Normalization)**：简化版 LayerNorm，`RMSNorm(x) = x / RMS(x) · γ`。LLaMA 系列等现代模型使用。

**Rotary Position Embedding (RoPE, 旋转位置编码)**：通过旋转矩阵将位置信息编码到 Q 和 K 向量中，使注意力内积天然包含相对位置信息。

### S

**Scaled Dot-Product Attention (缩放点积注意力)**：Transformer 的基础注意力形式，`Attention(Q,K,V) = softmax(QK^T/√d_k)·V`。

**Scheduled Sampling (计划采样)**：训练时按一定概率混合使用真实目标（Teacher Forcing）和模型自身预测，缓解曝光偏差。

**Self-Attention (自注意力)**：Q、K、V 全部来自同一来源的注意力形式，用于学习序列内部的依赖关系。

**Selective SSM (选择性状态空间模型)**：Mamba 的核心创新，让 SSM 的参数（B, C, Δ）依赖于输入内容。

**Sinusoidal PE (正弦位置编码)**：使用固定频率的正弦/余弦函数生成位置编码，`PE(pos, 2i) = sin(pos/10000^{2i/d})`。

**SiLU / Swish (Sigmoid Linear Unit)**：`SiLU(x) = x·σ(x)`，SwiGLU FFN 中的激活函数。

**Span Corruption (跨度破坏)**：T5 的预训练目标，用哨兵 token 替换文本中的连续跨度，要求模型恢复被替换的内容。

**State Space Model (SSM, 状态空间模型)**：通过一组微分/差分方程描述序列输入到输出的映射。Mamba 系列的基础数学框架。

**Structured State Space Duality (SSD, 结构化状态空间对偶性)**：Mamba-2 提出的理论框架，揭示了 SSM 和线性注意力之间的深层数学联系。

**SwiGLU**：使用 Swish 门控的 GLU 变体，`SwiGLU(x) = (xW_1 ⊙ SiLU(xW_g))W_2`。现代 LLM 的标准 FFN 实现。

### T

**Teacher Forcing (教师强制)**：训练序列模型时，用真实目标而非模型预测作为下一时刻的输入的策略。

**Temperature (温度)**：控制 softmax 输出的"锐度"的超参数 T，`p_i ∝ exp(z_i/T)`。

**Tensor Parallelism (张量并行)**：将单个权重矩阵切分到多个 GPU 上的模型并行策略。

**Top-K / Top-P Sampling**：控制文本生成多样性的解码策略。Top-K 仅从概率最高的 K 个 token 中采样；Top-P 从累积概率达到 P 的最小 token 集合中采样。

**Transformer**：Vaswani et al. (2017) 提出的基于自注意力机制的序列建模架构，完全抛弃了循环结构。

### V

**Vanishing/Exploding Gradient (梯度消失/爆炸)**：深层网络或 RNN 中，反向传播时梯度在层数/时间轴上以指数级衰减或增长。

**Value (V, 值)**：自注意力中"值"的角色，决定了每个位置向其他位置传递的实际信息内容。最终输出是 V 向量的加权和。

### W

**Warmup (学习率预热)**：训练初期逐步将学习率从 0 提升到目标值的策略，防止训练初期不稳定。

### Z

**Zero-Shot (零样本)**：不提供任何示例，仅通过任务描述使模型执行任务的能力。

**Zero-Order Hold (ZOH, 零阶保持)**：将连续时间 SSM 离散化到离散时间步的标准方法。

---

> **文档版本**: 2026.08
>
> **说明**: 本文是一份系统性的技术参考文档，旨在梳理深度学习中序列建模从 RNN/LSTM 到 Transformer 及其现代变体的完整发展脉络。文档中的公式使用 LaTeX 风格表示，架构图使用 ASCII 绘制。所有内容均基于已公开发表的学术论文、技术报告和开源项目。
