# 第 9 章 Qwen-VL 2.5 多模态大模型微调实战

## 学习目标

- 理解多模态微调与文本微调的差异
- 掌握 Qwen-VL 微调的数据格式与准备方法
- 用 LLaMA-Factory 完成 Qwen2.5-VL 微调实战
- 掌握多模态微调的评估与常见问题

---

## 9.1 Qwen-VL 2.5 微调概述

### 9.1.1 为什么需要微调多模态模型

通用 VLM 在以下场景力不从心，需要微调：

1. **垂直领域知识**：医疗影像、工业缺陷、特定商品识别。
2. **专属指令与格式**：按企业模板输出质检报告、票据结构化。
3. **风格对齐**：行业术语、口语习惯。
4. **边界能力增强**：小目标检测、密集文字、特定图表。

### 9.1.2 微调 vs RAG（多模态场景）

| 维度 | 多模态微调 | 多模态 RAG |
|------|-----------|-----------|
| 知识注入 | 学习视觉特征与领域模式 | 检索文本/图片上下文 |
| 视觉能力 | 强（改变"看"的能力） | 弱（不改视觉编码） |
| 格式定制 | 强 | 中 |
| 数据成本 | 需成对图文数据 | 只需语料 |
| 适用 | 识别类、风格类 | 知识类问答 |

> 结论：**视觉识别类任务（看懂领域图像）→ 微调；知识查询类 → RAG**。

### 9.1.3 微调策略选择

| 策略 | 说明 | 适用 |
|------|------|------|
| **全参数微调** | 更新视觉编码器 + 投影层 + LLM | 数据充足（>10万）、能力改变大 |
| **LoRA/QLoRA（推荐）** | 冻结大部分，只训低秩适配器 | 数据少（数千-数万）、成本敏感 |
| **仅微调投影层** | 只训视觉→文本映射 | 图文对齐问题 |

**实践建议**：默认 QLoRA 起步；效果不足再考虑全参微调。

## 9.2 微调数据准备

### 9.2.1 数据格式（LLaVA 格式）

```json
[
  {
    "id": "sample_001",
    "image": "path/to/image1.jpg",
    "conversations": [
      {"from": "human", "value": "这张肺部 X 光片有什么异常？"},
      {"from": "gpt", "value": "右肺下叶可见结节样高密度影，直径约1.2cm，建议进一步CT检查。"},
      {"from": "human", "value": "请给出初步诊断意见"},
      {"from": "gpt", "value": "结合影像特征，初步考虑良性结节可能，建议定期随访。"}
    ]
  }
]
```

### 9.2.2 多图与定位数据

**多图数据**（对比图）：

```json
{
  "id": "sample_002",
  "images": ["before.jpg", "after.jpg"],
  "conversations": [
    {"from": "human", "value": "比较这两张图片，工程进度有什么变化？"},
    {"from": "gpt", "value": "第二张图相比第一张，建筑主体已封顶..."}
  ]
}
```

**定位数据**（边界框，坐标归一化到 [0,1000]）：

```
"value": "图中用<|box_start|>(421,213)<|box_end|>标出缺陷位置"
```

### 9.2.3 数据准备要点

1. **图文对应**：每张图片本地路径，确保文件存在。
2. **对话质量**：领域专家撰写或审核，每图 1-3 轮对话。
3. **多样性**：覆盖不同图像、角度、难度、表达。
4. **数量参考**：LoRA 起步 500-2000 条；全参 1 万+。
5. **图片预处理**：统一格式（jpg/png），控制分辨率（长边 ≤ 2560）。

### 9.2.4 数据样例：工业质检微调

| 图像 | 问题 | 回答 |
|------|------|------|
| 电路板照片 | 检查焊接质量 | 焊点 P1 有虚焊迹象（坐标xxx），需补焊... |
| 零件侧视图 | 判断缺陷类型 | 划痕缺陷，长度为 3.2mm，位于边缘... |

## 9.3 微调实战（LLaMA-Factory）

### 9.3.1 环境准备

```bash
# LLaMA-Factory 支持 Qwen-VL 多模态微调
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e .[torch,bitsandbytes,multimodal]
```

### 9.3.2 数据配置

```yaml
# data/dataset_info.json 中注册
"vl_quality": {
  "images": ["image"],            # 图片字段名
  "conversations": "conversations",  # 对话字段名
  "format": "sharegpt",
  "tags": {
    "role_tag": "from",
    "content_tag": "value",
    "user_tag": "human",
    "assistant_tag": "gpt"
  }
}
```

### 9.3.3 启动微调（QLoRA）

```bash
llamafactory-cli train \
  --model_name_or_path Qwen/Qwen2.5-VL-7B-Instruct \
  --stage sft \
  --finetuning_type lora \
  --quantization_bit 4 \
  --dataset vl_quality \
  --template qwen_vl \
  --cutoff_len 2048 \
  --learning_rate 1e-4 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 8 \
  --output_dir ./outputs/vl-qlora \
  --lora_rank 32 \
  --lora_alpha 64 \
  --logging_steps 10 \
  --save_steps 500
```

### 9.3.4 合并导出与部署

```bash
# 合并 LoRA 到基座模型
llamafactory-cli export \
  --model_name_or_path Qwen/Qwen2.5-VL-7B-Instruct \
  --adapter_name_or_path ./outputs/vl-qlora \
  --template qwen_vl \
  --finetuning_type lora \
  --export_dir ./outputs/vl-full

# 部署推理（vLLM 支持多模态）
vllm serve ./outputs/vl-full --served-model-name qwen2.5-vl-custom
```

### 9.3.5 关键超参与技巧

| 超参 | 多模态建议 | 说明 |
|------|-----------|------|
| learning_rate | 1e-4 ~ 2e-4（LoRA） | 全参用 1e-5 |
| cutoff_len | 2048-4096 | 多图需更长 |
| 图像 Token 数 | 动态分辨率，最多约 1280 Tokens/图 | 注意上下文预算 |
| freeze_vision_tower | 可尝试冻结视觉编码器 | 数据少时更稳 |
| gradient_checkpointing | 开启 | 大幅省显存 |

## 9.4 评估与调优

### 9.4.1 评估维度

| 维度 | 方法 |
|------|------|
| 视觉识别准确率 | 自建标注测试集（分类/检测） |
| 描述质量 | 人工评分 + CIDEr/BLEU（如有参考） |
| 指令遵循 | 检查输出格式/字段完整 |
| 通用能力回归 | 通用 VQA 基准（MMBench/SEED-Bench） |
| 幻觉 | 反事实提问检测 |

### 9.4.2 常见问题排查

| 现象 | 原因 | 对策 |
|------|------|------|
| 微调后"不看图" | 数据量太少 / 学习率过高 | 增大数据、降学习率 |
| 复制训练集回答 | 过拟合 | 加正则、数据增强、减 epoch |
| 中文变差 | 灾难性遗忘 | 混入通用多模态数据（10-20%） |
| 显存不足 | 图像 Token 太多 | 降分辨率、开 gradient_checkpointing、QLoRA |
| 输出格式混乱 | 数据格式不统一 | 统一模板、示例对齐 |

### 9.4.3 数据配比建议

```
领域图文数据 60% + 通用图文数据 20%（防遗忘）
+ 纯文本指令 10%（保持语言能力）+ 安全数据 10%
```

---

## 高质量博客推荐

1. **Qwen2.5-VL 微调实战：数据格式与完整流程** — [CSDN](https://blog.csdn.net/m0_62283830/article/details/143505026)
   从数据准备到训练到部署的完整教程。
2. **LLaMA-Factory 多模态微调官方文档** — [LLaMA-Factory Docs](https://llamafactory.readthedocs.io/zh-cn/latest/)
   Qwen-VL 数据格式、训练参数权威参考。
3. **多模态微调避坑指南：数据与超参** — [微信公众号](https://mp.weixin.qq.com/s/50oi2d7m5JZ-G6FdGjnpig)
   图像分辨率、Token 数量、显存优化的工程经验。
4. **MMBench 多模态评测基准详解** — [知乎专栏](https://zhuanlan.zhihu.com/p/672469127)
   微调前后多模态能力评估方法。

## 动手实践

1. 准备 200 条"商品图片 + 描述/问答"数据（可用公开数据集），完成 QLoRA 微调。
2. 微调前后对同一批测试图片问答，量化效果提升。
3. 尝试冻结/不冻结视觉编码器两种方案，对比效果与显存。
4. 将微调模型部署到 vLLM，接入一个简单的图片问答应用。

## 常见问题（FAQ）

**Q1：微调 Qwen-VL 需要多少显存？**
A：7B 模型 QLoRA（4bit）：约 12-20G；LoRA（BF16）：约 30-40G；全参微调：约 70G+。消费级显卡用 QLoRA 可行。

**Q2：不微调视觉编码器会不会效果差？**
A：通常不会——视觉编码器已在大规模图文数据上充分训练，领域适配主要靠投影层与 LLM 的学习。数据少时冻结更稳。

**Q3：微调后模型还能做通用对话吗？**
A：会退化，但可通过混入通用数据缓解。建议领域模型保留一个通用模型备用，或按需加载 LoRA 适配器切换。
