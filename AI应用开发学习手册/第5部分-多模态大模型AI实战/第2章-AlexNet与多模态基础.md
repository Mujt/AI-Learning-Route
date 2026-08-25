# 第 2 章 AlexNet 实现与多模态大模型基础

## 学习目标

- 理解 AlexNet 的网络结构与历史意义
- 用 PyTorch 完整实现 AlexNet 并训练
- 掌握多模态大模型的基本范式与关键技术

---

## 2.1 AlexNet 网络结构详解

### 2.1.1 历史地位

AlexNet 在 2012 年 ImageNet 竞赛中以远超第二名（top-5 错误率 15.3% vs 26.2%）的成绩夺冠，**引爆深度学习时代**。其成功来源于算力（GPU）+ 数据（ImageNet）+ 网络创新的结合。

### 2.1.2 结构总览

```
输入：224×224×3 图像
↓ 卷积 96×11×11, stride=4
↓ ReLU + 局部响应归一化(LRN) + 最大池化3×3 stride=2
↓ 卷积 256×5×5, pad=2
↓ ReLU + LRN + 最大池化
↓ 卷积 384×3×3, pad=1   (多个卷积堆叠)
↓ 卷积 384×3×3, pad=1
↓ 卷积 256×3×3, pad=1
↓ 最大池化
↓ 展平 → 全连接 4096 → ReLU → Dropout(0.5)
↓ 全连接 4096 → ReLU → Dropout(0.5)
↓ 全连接 1000 → Softmax
输出：1000 类概率
```

### 2.1.3 核心创新点

| 创新 | 作用 |
|------|------|
| **ReLU 激活** | 比 Tanh 快 6 倍，缓解梯度消失 |
| **GPU 并行训练** | 双卡并行，训练时间缩短数十倍 |
| **Dropout** | 随机丢弃神经元，防过拟合（全连接层后） |
| **数据增强** | 随机裁剪、翻转、颜色扰动，扩大训练集 |
| **LRN** | 局部响应归一化（后续证明收益有限，已少用） |
| **重叠池化** | 池化窗口大于步长，略降错误率 |

## 2.2 AlexNet 代码实现（PyTorch）

### 2.2.1 模型定义

```python
import torch
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.features = nn.Sequential(
            # 输入 224x224x3
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=2),   # 55x55x96
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),                    # 27x27x96
            nn.Conv2d(96, 256, kernel_size=5, padding=2),            # 27x27x256
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),                    # 13x13x256
            nn.Conv2d(256, 384, kernel_size=3, padding=1),           # 13x13x384
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, kernel_size=3, padding=1),           # 13x13x384
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),           # 13x13x256
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),                    # 6x6x256
        )
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        return self.classifier(torch.flatten(self.features(x), 1))

model = AlexNet(num_classes=10)
print(sum(p.numel() for p in model.parameters()))   # ~6100 万参数
```

### 2.2.2 训练循环（CIFAR-10）

```python
from torch.utils.data import DataLoader
import torchvision.transforms as T
import torchvision.datasets as datasets

transform = T.Compose([
    T.Resize(224),                     # AlexNet 要求 224 输入
    T.RandomHorizontalFlip(),          # 数据增强
    T.ToTensor(),
    T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
])
train_set = datasets.CIFAR10(root="./data", train=True, transform=transform, download=True)
loader = DataLoader(train_set, batch_size=64, shuffle=True, num_workers=4)

optimizer = torch.optim.SGD(model.parameters(), lr=1e-2, momentum=0.9)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for x, y in loader:
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
    print(f"epoch {epoch}: loss={loss.item():.4f}")
```

**训练技巧**：学习率阶梯衰减（每 3 epoch 降 10 倍）；ImageNet 规模需多卡与数天，CIFAR 小规模可 CPU 起步。

## 2.3 多模态大模型基础

### 2.3.1 什么是多模态大模型

**多模态大模型（LMM/VLM）**：能同时理解和生成**多种模态**（文本、图像、音频、视频）的模型。核心是**对齐不同模态的语义空间**——让"猫的图片"和"单词 cat"在向量空间中靠近。

### 2.3.2 主流范式演进

| 范式 | 代表 | 机制 |
|------|------|------|
| 双塔对比学习 | CLIP（2021） | 图文编码器分别编码，对比学习对齐 |
| 融合编码器 | FLAVA | 单塔双流融合 |
| **LLM 统一解码** | LLaVA / Qwen-VL | 视觉编码器 + 投影层 + LLM，文本为统一输出 |
| 原生多模态 | Gemini / GPT-4o | 从头统一训练 |

### 2.3.3 主流架构（Qwen-VL 类）

```
视觉编码器（ViT）──▶ 视觉 Token（图像分块嵌入）
                           │
                           ▼
                   投影层（Projector / Resampler）
                           │ 将视觉特征映射到 LLM 的嵌入空间
                           ▼
                  LLM 主干（Qwen2.5 等）
                           │ 文本 + 视觉 Token 一起自回归生成
                           ▼
                         输出文本
```

**关键组件**：
1. **视觉编码器**：Vision Transformer（ViT）把图像切成 Patch 后编码。
2. **投影器**：把视觉特征"翻译"成 LLM 能理解的 Token（MLP / Q-Former / Resampler）。
3. **LLM 主干**：承担理解与生成（可冻结或微调）。

### 2.3.4 训练范式（三阶段）

```
① 预训练对齐：图文对大规模对比学习（如 5 亿图文对）
② 视觉-语言指令微调：让模型学会"看图回答问题"
③ 人类偏好对齐：RLHF/DPO 提升有用性与安全性
```

### 2.3.5 关键技术问题

- **高分辨率**：长图、小物体识别需要多尺度/裁剪策略（Qwen-VL 采用 NaViT + M-RoPE 处理任意分辨率）。
- **多图理解**：跨图对比、多图对话。
- **视频/音频**：时间维度的建模。
- **幻觉**：视觉幻觉（模型说看到了图里没有的东西），是当前研究热点。

---

## 高质量博客推荐

1. **AlexNet 网络结构详解与 PyTorch 实现** — [CSDN](https://blog.csdn.net/qq_38978225/article/details/142746065)
   结构图解 + 完整代码，适合对照实现。
2. **从 AlexNet 到 ResNet：经典 CNN 演进史** — [知乎专栏](https://zhuanlan.zhihu.com/p/672469127)
   把握卷积网络发展脉络。
3. **CLIP 原理详解：图文对比学习范式** — [微信公众号](https://mp.weixin.qq.com/s/8qZ4h7wQvFmJTb3yFkpHxw)
   多模态对齐的奠基之作。
4. **多模态大模型入门：从 CLIP 到 Qwen-VL** — [CSDN](https://blog.csdn.net/m0_61066945/article/details/147875245)
   多模态架构演进与技术要点综述。
5. **PyTorch 官方 AlexNet 示例** — [PyTorch Vision](https://pytorch.org/vision/main/models/alexnet.html)
   官方实现参考。

## 动手实践

1. 用 PyTorch 复现 AlexNet，在 CIFAR-10 上训练并记录准确率曲线。
2. 分别去除 Dropout 和用 ReLU 换 Tanh，观察训练曲线变化（验证创新点）。
3. 用 CLIP 加载图文匹配 Demo：给一张图片生成候选文本，看相似度排序。

## 常见问题（FAQ）

**Q1：AlexNet 现在还有用吗？**
A：直接使用场景很少，但它奠定了"卷积+池化+全连接+ReLU+Dropout"的范式，是理解现代 CNN 的必修课。

**Q2：多模态大模型的"视觉 Token"是什么？**
A：图像被切成 16×16 的 Patch，每个 Patch 经 ViT 变成一个向量（Token），与文本 Token 一起送入 LLM 处理。

**Q3：为什么投影层至关重要？**
A：视觉特征和文本词嵌入的向量空间不同，投影层（如 MLP）负责"翻译"二者，对齐不好则模型无法理解图像内容。
