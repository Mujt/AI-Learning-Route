# 第2周 第3课：Python 数据分析入门

> **课程系列**：AI 时代能力培养（8周速成版）
> **本节课**：第2周第3课 | Python 数据分析入门
> **时长**：2小时（50分钟讲解 + 70分钟实操）
> **前置知识**：已掌握 Python 基本语法（变量、条件、循环、列表、字典）、函数与模块

---

## 一、课程信息

| 项目 | 说明 |
|------|------|
| **课程编号** | Week 2 - Lesson 3 |
| **课程名称** | Python 数据分析入门 |
| **所属模块** | Python 基础（第2周） |
| **课时** | 2小时 |
| **教学形式** | 课堂讲解 + Jupyter 实操 + 即时反馈 |
| **前置课程** | 第2周第1课（Python 语法入门）、第2周第2课（函数、模块与文件操作） |
| **后续课程** | 第3周（机器学习入门） |

---

## 二、学习目标

完成本节课后，你应该能够：

1. **理解**为什么 NumPy 比 Python 原生列表更快，以及向量化运算的核心思想
2. **创建和操作** NumPy 数组，完成基本的数值计算和统计
3. **使用 Pandas** 读取数据、筛选、分组聚合、处理缺失值、合并数据
4. **使用 Matplotlib** 绘制折线图、柱状图、饼图、散点图、直方图，并设置中文字体
5. **独立完成**一个从数据加载到图表输出的完整数据分析流程
6. **遇到问题**知道如何用 AI 工具（ChatGPT/Claude）辅助排查 Pandas 和绘图代码的错误

> **教学理念**：本节课不要求你记住所有 API，重点是建立"数据处理的直觉"——知道什么情况下用什么工具。具体的函数名和参数，后续实践中自然会记住，记不住就问 AI。

---

## 三、课前准备

### 3.1 环境确认

打开 Jupyter Notebook，在第一个 Cell 中运行以下命令确认环境就绪：

```python
# 检查必要的库是否已安装
import sys
print(f"Python 版本: {sys.version}")

# 尝试导入本节课需要用到的三个核心库
try:
    import numpy as np
    print(f"NumPy 版本: {np.__version__}  ✅")
except ImportError:
    print("NumPy 未安装 ❌ — 请在终端运行: pip install numpy")

try:
    import pandas as pd
    print(f"Pandas 版本: {pd.__version__}  ✅")
except ImportError:
    print("Pandas 未安装 ❌ — 请在终端运行: pip install pandas")

try:
    import matplotlib
    print(f"Matplotlib 版本: {matplotlib.__version__}  ✅")
except ImportError:
    print("Matplotlib 未安装 ❌ — 请在终端运行: pip install matplotlib")
```

### 3.2 安装缺失的库

如果上述检查发现任何库未安装，在 **Anaconda Prompt**（Windows）或 **终端**（macOS）中运行：

```bash
pip install numpy pandas matplotlib
```

如果你使用的是 Anaconda，也可以用：

```bash
conda install numpy pandas matplotlib
```

> **提示**：Anaconda 默认已经包含这三个库，通常不需要额外安装。如果你安装的是标准 Python（非 Anaconda），则需要手动 pip install。

### 3.3 课前心理准备

本节课代码量较大，但请不要慌张：

- **不需要背诵**：所有 API 都可以随时查阅文档或问 AI
- **关注流程**：理解"加载数据 → 探索 → 清洗 → 聚合 → 可视化"这条主线
- **遇到报错是正常的**：把错误信息复制给 ChatGPT/Claude，它会帮你分析原因
- **先跑通，再修改**：把示例代码完整运行一遍，再尝试修改参数观察变化

---

## 四、核心知识点详解

---

### 第一部分：NumPy 数值计算

#### 4.1.1 为什么需要 NumPy？

很多初学者会问："Python 不是已经有列表（list）了吗，为什么还需要 NumPy？"

答案浓缩为三个字：**快、省、强**。

**（1）Python 列表太慢**

Python 的列表是一个通用容器，可以装任意类型的元素。这种"灵活性"是有代价的——每次做运算，Python 都要检查每个元素是什么类型，然后决定该怎么算。当数据量上万甚至百万时，这个"类型检查"的开销就非常大了。

```python
# 直观对比：Python列表 vs NumPy数组
import numpy as np
import time

# 创建100万个数字
size = 1_000_000
py_list = list(range(size))
np_arr = np.arange(size)

# Python列表：每个元素平方（用循环）
start = time.time()
py_squared = [x**2 for x in py_list]
print(f"Python列表耗时: {time.time() - start:.3f} 秒")

# NumPy数组：每个元素平方（用向量化运算）
start = time.time()
np_squared = np_arr ** 2
print(f"NumPy数组耗时: {time.time() - start:.3f} 秒")
```

运行结果示例：
```
Python列表耗时: 0.152 秒
NumPy数组耗时: 0.003 秒
```

速度差距约 **50 倍**。数据量越大，NumPy 的优势越明显。

**（2）向量化运算**

NumPy 的核心优势在于**向量化运算**：你不需要写 for 循环，直接对整个数组进行操作，底层的 C/Fortran 代码会自动并行处理。

```python
# 向量化 vs 循环
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# NumPy风格（向量化，一行搞定）
result = a + b  # array([11, 22, 33, 44, 55])

# 传统Python风格（需要写循环，麻烦且慢）
result_list = []
for i in range(len(a)):
    result_list.append(a[i] + b[i])
```

**（3）科学计算的基础**

NumPy 是 Pandas、Scikit-learn、TensorFlow、PyTorch 等所有主流数据科学库的底层基础。这些库的数据结构在底层都依赖 NumPy 数组。学好 NumPy，后续所有工具都会事半功倍。

#### 4.1.2 创建数组

NumPy 中最核心的数据结构是 **ndarray**（N-dimensional array，多维数组）。

```python
import numpy as np

# --- 方式1：从Python列表创建 ---
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)  # [1 2 3 4 5]
print(type(arr1))  # <class 'numpy.ndarray'>

# --- 方式2：创建全0数组 ---
zeros_1d = np.zeros(5)          # 一维：[0. 0. 0. 0. 0.]
zeros_2d = np.zeros((3, 4))     # 二维3行4列全0矩阵
print("3×4全零矩阵:\n", zeros_2d)

# --- 方式3：创建全1数组 ---
ones = np.ones((2, 3))          # 2行3列全1矩阵
print("2×3全1矩阵:\n", ones)

# --- 方式4：创建等差数组 (类似Python内置的range) ---
arr_arange = np.arange(0, 20, 2)  # 起点0，终点20(不含)，步长2
print(arr_arange)  # [0 2 4 6 8 10 12 14 16 18]

# --- 方式5：创建指定数量的等差数组 (自动计算步长) ---
arr_linspace = np.linspace(0, 10, 5)  # 0到10之间均匀取5个点
print(arr_linspace)  # [0.  2.5 5.  7.5 10.]

# --- 方式6：创建随机数组 ---
np.random.seed(42)  # 设置随机种子，保证每次运行结果一样
random_int = np.random.randint(0, 100, 10)  # 10个0-100之间的随机整数
random_float = np.random.randn(5)            # 5个标准正态分布随机数
print("随机整数:", random_int)
print("标准正态分布:", random_float)
```

> **arange vs linspace**：arange 是你指定**步长**，linspace 是你指定**元素个数**。当你需要"在 X 和 Y 之间均匀取 N 个点"时，用 linspace 更方便。

#### 4.1.3 数组属性

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(f"形状 (shape):    {arr.shape}")     # (2, 3) — 2行3列
print(f"维度 (ndim):     {arr.ndim}")      # 2 — 二维数组
print(f"元素总数 (size): {arr.size}")      # 6 — 总共6个元素
print(f"数据类型 (dtype): {arr.dtype}")    # int64（或int32，取决于系统）
print(f"每个元素字节数:   {arr.itemsize}")  # 8（int64占8字节）
print(f"总内存占用:       {arr.nbytes}")    # 48（6个元素 × 8字节）
```

理解 `shape` 是最重要的：`shape` 是一个元组，告诉你每一维有多少个元素。
- 一维数组：`(n,)` — 比如 `(5,)` 表示 5 个元素
- 二维数组：`(m, n)` — m 行 n 列
- 三维数组：`(k, m, n)` — k 个 m×n 的矩阵

#### 4.1.4 数组索引与切片

NumPy 的索引和 Python 列表很像，但功能更强大。

**（1）一维数组切片**

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70])

print(arr[0])       # 10 — 单个元素
print(arr[-1])      # 70 — 倒数第一个
print(arr[1:4])     # [20 30 40] — 索引1到3（不含4）
print(arr[:3])      # [10 20 30] — 从头到索引2
print(arr[3:])      # [40 50 60 70] — 从索引3到末尾
print(arr[::2])     # [10 30 50 70] — 每隔一个取一个
print(arr[::-1])    # [70 60 50 40 30 20 10] — 反转数组
```

**（2）二维数组索引**

```python
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

print(arr2d[0, 0])    # 1 — 第0行第0列
print(arr2d[1, 2])    # 6 — 第1行第2列
print(arr2d[0])       # [1 2 3] — 第0行整行
print(arr2d[:, 1])    # [2 5 8] — 第1列整列（:表示所有行）
print(arr2d[:2, 1:])  # [[2 3], [5 6]] — 前2行、第1列及之后
```

> **理解 `:` 的含义**：逗号前面是"行"的选择，逗号后面是"列"的选择。`:` 单独出现表示"全部"。

**（3）布尔索引（Boolean Indexing）**

这是数据分析中最常用的筛选方式。

```python
scores = np.array([85, 92, 78, 90, 88, 65, 95, 72])

# 创建一个布尔数组：True表示该位置的元素满足条件
mask = scores >= 80
print(mask)  # [True True False True True False True False]

# 用布尔数组进行筛选
high_scores = scores[mask]
print(high_scores)  # [85 92 90 88 95]

# 通常一步搞定
print(scores[scores >= 80])  # 同上

# 多条件组合
print(scores[(scores >= 80) & (scores <= 90)])  # 80到90之间
# 注意：必须用 & (and) / | (or)，不能用 Python 的 and/or 关键字
```

**（4）花式索引（Fancy Indexing）**

```python
arr = np.array([100, 200, 300, 400, 500])
indices = [0, 2, 4]
print(arr[indices])  # [100 300 500] — 按指定索引取多个元素

# 对于二维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[[0, 2]])  # [[1 2 3], [7 8 9]] — 取第0行和第2行
```

#### 4.1.5 向量化运算

这是 NumPy 最强大的能力：直接对数组做数学运算，不需要写循环。

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# 逐元素运算 (Element-wise)
print(a + b)      # [11 22 33 44 55]
print(a - b)      # [-9 -18 -27 -36 -45]
print(a * b)      # [10 40 90 160 250] — 逐元素相乘，不是矩阵乘法！
print(a / b)      # [0.1 0.1 0.1 0.1 0.1]
print(a ** 2)     # [1 4 9 16 25] — 每个元素平方

# 数学函数（也是逐元素的）
print(np.sqrt(a))   # [1.   1.414 1.732 2.   2.236] — 开方
print(np.log(a))    # 自然对数
print(np.exp(a))    # e的幂

# 数组与标量运算 (Broadcasting)
print(a + 100)    # [101 102 103 104 105] — 每个元素+100
print(a * 10)     # [10 20 30 40 50] — 每个元素×10
```

**广播（Broadcasting）概念简述**：

Broadcasting 是 NumPy 最核心的机制之一。当两个形状不同的数组做运算时，NumPy 会自动将较小的数组"扩展"到较大数组的形状。

```python
# 最简单的广播：数组 vs 标量
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr + 10)  # 标量10被"广播"到和arr一样的形状
# [[11 12 13]
#  [14 15 16]]

# 一维数组 vs 二维数组
a = np.array([10, 20, 30])  # 形状 (3,)
b = np.array([[1, 2, 3],
              [4, 5, 6]])   # 形状 (2, 3)
print(a + b)  # a被"广播"成 (2, 3)，然后逐元素相加
# [[11 22 33]
#  [14 25 36]]

# 列向量 vs 行向量
col = np.array([[10], [20], [30]])  # 形状 (3, 1)
row = np.array([1, 2, 3])           # 形状 (3,)
# 两者相加，各自广播到 (3, 3)
print(col + row)
# [[11 12 13]
#  [21 22 23]
#  [31 32 33]]
```

> 广播规则总结：从最后一个维度开始比较，如果维度相同、或其中一个为 1、或其中一个不存在，则该维度兼容。不理解细节没关系，实际使用中遇到 shape 不匹配时报错，问 AI 就能解决。

#### 4.1.6 统计函数

```python
scores = np.array([85, 92, 78, 90, 88, 65, 95, 72, 85, 80])

print(f"平均值 (mean):     {scores.mean():.1f}")
print(f"标准差 (std):      {scores.std():.1f}")
print(f"求和 (sum):        {scores.sum()}")
print(f"最小值 (min):      {scores.min()}")
print(f"最大值 (max):      {scores.max()}")
print(f"中位数 (median):   {np.median(scores):.1f}")
print(f"25分位数:          {np.percentile(scores, 25):.1f}")
print(f"75分位数:          {np.percentile(scores, 75):.1f}")
print(f"最大值索引 (argmax): {scores.argmax()} — 第{scores.argmax()+1}个元素")
print(f"最小值索引 (argmin): {scores.argmin()} — 第{scores.argmin()+1}个元素")

# 二维数组按轴统计
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

print("按列求和 (axis=0):", arr2d.sum(axis=0))  # [12 15 18] — 每列纵向求和
print("按行求和 (axis=1):", arr2d.sum(axis=1))  # [6 15 24] — 每行横向求和
```

> **axis 参数的理解**：`axis=0` 表示沿第 0 个维度方向操作（纵向，"压扁"行），`axis=1` 表示沿第 1 个维度方向操作（横向，"压扁"列）。初学时容易混乱，多试几次就习惯了。

#### 4.1.7 数组变形

```python
arr = np.arange(1, 13)  # [1 2 3 4 5 6 7 8 9 10 11 12]
print("原始:", arr, arr.shape)  # (12,)

# reshape: 改变形状（元素总数必须一致）
mat_3x4 = arr.reshape(3, 4)     # 3行4列
print("3×4:\n", mat_3x4)

mat_4x3 = arr.reshape(4, 3)     # 4行3列
print("4×3:\n", mat_4x3)

# 用 -1 让NumPy自动计算该维度大小
mat_auto = arr.reshape(3, -1)    # 3行，列数自动计算 = 12/3 = 4
print("自动计算列数:\n", mat_auto)

# flatten: 将多维数组展平为一维
flat = mat_3x4.flatten()
print("展平:", flat)  # [1 2 3 4 5 6 7 8 9 10 11 12]

# transpose 或 .T: 转置（行列互换）
transposed = mat_3x4.T
print("转置后形状:", transposed.shape)  # (4, 3)
print("转置后:\n", transposed)
```

---

### 第二部分：Pandas 数据分析

#### 4.2.1 为什么需要 Pandas？

NumPy 擅长处理纯数值的矩阵运算，但现实中的数据通常是这样的：

| 姓名 | 年龄 | 城市 | 消费金额 | 购买时间 |
|------|------|------|----------|----------|
| 张三 | 25 | 北京 | 299.00 | 2026-01-15 |
| 李四 | 30 | 上海 | 158.00 | 2026-02-20 |
| 王五 |  | 广州 | 450.00 | 2026-03-10 |

这些数据的特点是：
- **混合数据类型**：有字符串（姓名、城市）、数值（年龄、金额）、日期
- **有缺失值**：王五的年龄是空的
- **需要列名**：每一列有不同的含义
- **需要对齐**：每一行是一条完整的记录

Pandas 就是为解决这些问题而生的。你可以把它理解为**"Python 世界的 Excel"**——它比 Excel 更强大，可以处理百万行级别的数据，而且可以用代码自动化操作。

#### 4.2.2 Series 与 DataFrame

Pandas 有两大核心数据结构：

| 结构 | 类比 | 说明 |
|------|------|------|
| **Series** | Excel 中的**一列** | 一维带标签数组，每个值有一个索引 |
| **DataFrame** | Excel 中的**一个工作表** | 二维表格，由多个 Series 组成 |

```python
import pandas as pd
import numpy as np

# Series — 带标签的一维数组
s = pd.Series([85, 92, 78, 90], 
              index=['张三', '李四', '王五', '赵六'],
              name='语文成绩')
print(s)
print(f"\n类型: {type(s)}")
print(f"形状: {s.shape}")
```

输出：
```
张三    85
李四    92
王五    78
赵六    90
Name: 语文成绩, dtype: int64
```

#### 4.2.3 创建 DataFrame

```python
# --- 方式1：从字典创建（最常用）---
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [25, 30, 22, 28],
    "城市": ["北京", "上海", "广州", "深圳"],
    "成绩": [85, 92, 78, 90]
}
df = pd.DataFrame(data)
print(df)

# --- 方式2：从列表嵌套创建 ---
data_list = [
    ["张三", 25, "北京", 85],
    ["李四", 30, "上海", 92],
    ["王五", 22, "广州", 78],
    ["赵六", 28, "深圳", 90],
]
df2 = pd.DataFrame(data_list, columns=["姓名", "年龄", "城市", "成绩"])
print(df2)

# --- 方式3：从CSV文件读取（实际工作中最常用）---
# df = pd.read_csv('data.csv')
# df = pd.read_csv('data.csv', encoding='utf-8')  # 指定编码

# --- 方式4：从Excel文件读取 ---
# df = pd.read_excel('data.xlsx')
# df = pd.read_excel('data.xlsx', sheet_name='Sheet1')  # 指定工作表
```

#### 4.2.4 数据查看

拿到一份数据，你最先要做的事情就是"看看长什么样"。以下方法是你的日常操作：

```python
# 使用前面创建的 df
print("=== 前3行 ===")
print(df.head(3))        # 默认显示前5行，这里指定3行

print("\n=== 后2行 ===")
print(df.tail(2))        # 默认显示后5行

print("\n=== 基本信息 ===")
print(df.info())         # 显示每列的数据类型、非空数量、内存占用

print("\n=== 统计摘要 ===")
print(df.describe())     # 数值列的均值、标准差、分位数等

# 注意：describe() 默认只统计数值列，如果想看所有列（包括分类列），使用：
# print(df.describe(include='all'))

print("\n=== 形状 ===")
print(f"行数: {df.shape[0]}, 列数: {df.shape[1]}")

print("\n=== 列名 ===")
print(df.columns.tolist())

print("\n=== 每列的数据类型 ===")
print(df.dtypes)
```

输出示例（`df.describe()`）：
```
             年龄        成绩
count   4.00000   4.000000
mean   26.25000  86.250000
std     3.40343   6.238322
min    22.00000  78.000000
25%    24.25000  83.250000
50%    26.50000  87.500000
75%    28.50000  90.500000
max    30.00000  92.000000
```

#### 4.2.5 数据选择

数据选择是 Pandas 中使用频率最高的操作，需要重点掌握。

```python
# 准备数据
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "年龄": [25, 30, 22, 28, 26],
    "城市": ["北京", "上海", "广州", "深圳", "杭州"],
    "成绩": [85, 92, 78, 90, 88],
    "性别": ["男", "男", "女", "男", "女"]
})

# === 选择列 ===
print(df['姓名'])           # 选一列，返回 Series
print(type(df['姓名']))     # <class 'pandas.core.series.Series'>

print(df[['姓名', '成绩']]) # 选多列，注意两层方括号！返回 DataFrame
print(type(df[['姓名', '成绩']]))  # <class 'pandas.core.frame.DataFrame'>

# === 选择行 (loc 和 iloc) ===
# .loc[] — 基于标签（索引名）选择
# .iloc[] — 基于位置（整数位置）选择

# 用 iloc 按位置选择
print(df.iloc[0])       # 第0行，返回 Series
print(df.iloc[0:3])     # 前3行（位置索引0,1,2）
print(df.iloc[0, 1])    # 第0行第1列 → 25
print(df.iloc[:3, [0, 3]])  # 前3行，取第0和第3列

# 用 loc 按标签选择（默认索引就是位置序号时和iloc类似）
print(df.loc[0:2])      # 索引标签0到2的行（注意：loc是包含终点2的！）

# 设置自定义索引后 loc 的优势就体现出来了
df.set_index('姓名', inplace=True)
print(df.loc['张三'])           # 直接用姓名查找
print(df.loc[['张三', '李四']])  # 选多行
print(df.loc['张三', '成绩'])    # 张三的成绩 → 85
```

> **loc vs iloc 速记**：`loc` = **L**abel（标签），`iloc` = **I**nteger **loc**ation（整数位置）。iloc 和 Python 列表切片一样是"左闭右开"，loc 是"左闭右闭"。

#### 4.2.6 数据筛选（Boolean Filtering）

这是数据分析中最常用的操作模式。

```python
# 先用原始 df 重新演示（重置索引）
df = df.reset_index()

# 单条件筛选
high_score = df[df['成绩'] >= 85]
print("成绩>=85的学生:\n", high_score[['姓名', '成绩']])

# 多条件筛选 — 注意：用 & (与) 和 | (或)，每个条件必须加括号！
male_high = df[(df['性别'] == '男') & (df['成绩'] >= 85)]  # 成绩>=85的男学生
print("\n成绩>=85的男学生:\n", male_high[['姓名', '性别', '成绩']])

young_or_high = df[(df['年龄'] <= 25) | (df['成绩'] >= 90)]  # 年龄<=25 或 成绩>=90
print("\n年龄<=25或成绩>=90:\n", young_or_high[['姓名', '年龄', '成绩']])

# isin() — 值是否在指定列表中
target_cities = ['北京', '上海']
capital_students = df[df['城市'].isin(target_cities)]
print("\n在北京或上海的学生:\n", capital_students[['姓名', '城市']])

# between() — 值是否在指定区间内
mid_age = df[df['年龄'].between(25, 30)]  # 年龄25-30之间（含）
print("\n年龄25-30岁:\n", mid_age[['姓名', '年龄']])

# str.contains() — 字符串筛选
contains_zhang = df[df['姓名'].str.contains('张')]
print("\n姓'张'的学生:\n", contains_zhang[['姓名']])

# query() — 更简洁的筛选方式（推荐）
result = df.query('成绩 >= 85 and 性别 == "男"')
print("\n用query()方法:\n", result[['姓名', '性别', '成绩']])
```

#### 4.2.7 数据添加与修改

```python
# 准备数据
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "数学": [85, 92, 78],
    "英语": [82, 88, 85]
})

# --- 添加新列：直接赋值 ---
df['语文'] = [90, 85, 88]         # 添加一列
print(df)

# --- 添加基于计算的新列 ---
df['总分'] = df['数学'] + df['英语'] + df['语文']
df['平均分'] = (df['总分'] / 3).round(1)  # 保留1位小数
print(df)

# --- 使用 apply() 对列进行变换 ---
# apply() 对一列或一行中的每个元素应用一个函数
df['等级'] = df['平均分'].apply(lambda x: '优秀' if x >= 90 else ('良好' if x >= 80 else '及格'))
print(df)

# 更复杂的 apply 示例 — 使用自定义函数
def get_grade(avg):
    """根据平均分返回等级"""
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

df['等级字母'] = df['平均分'].apply(get_grade)
print(df)

# --- 使用 map() 做字典映射 ---
city_map = {"张三": "北京", "李四": "上海", "王五": "广州"}
df['城市'] = df['姓名'].map(city_map)
print(df)

# --- 修改已有列的值 ---
df.loc[df['姓名'] == '张三', '数学'] = 88  # 修改张三的数学成绩
print(df)
```

> **apply() vs map()**：`apply()` 更通用，可以传任意函数；`map()` 主要用于 Series 的字典映射。`apply()` 是 Pandas 中最灵活的工具之一，建议多加练习。

#### 4.2.8 数据排序

```python
# 准备数据
df = pd.DataFrame({
    "产品": ["A", "B", "C", "A", "B", "C"],
    "月份": ["1月", "1月", "1月", "2月", "2月", "2月"],
    "销量": [100, 200, 150, 120, 180, 170],
    "金额": [5000, 10000, 7500, 6000, 9000, 8500]
})

# 按单列排序
df_sorted = df.sort_values('销量', ascending=False)  # 按销量降序
print("按销量降序:\n", df_sorted)

# 按多列排序
df_multi_sorted = df.sort_values(['月份', '销量'], ascending=[True, False])
print("\n按月份升序、同一月份内按销量降序:\n", df_multi_sorted)

# 按索引排序
df_index_sorted = df.sort_index(ascending=False)
print("\n按索引降序:\n", df_index_sorted)
```

#### 4.2.9 分组聚合（GroupBy）

分组聚合是数据分析中最强大的工具之一——先按某个维度分组，然后对每组做统计计算。这个概念和 Excel 的数据透视表（Pivot Table）类似。

```python
# 准备数据
df = pd.DataFrame({
    "部门": ["销售", "销售", "销售", "技术", "技术", "技术", "市场", "市场"],
    "员工": ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"],
    "工资": [8000, 8500, 7800, 12000, 15000, 13000, 9000, 9500],
    "奖金": [2000, 1500, 1800, 3000, 5000, 4000, 2500, 2000],
    "年龄": [25, 30, 28, 32, 35, 28, 27, 31]
})

print("原始数据:\n", df)

# --- 基本分组聚合 ---
# 按部门分组，计算工资的平均值
dept_salary = df.groupby('部门')['工资'].mean()
print("\n各部门平均工资:\n", dept_salary)

# 等价写法（更推荐，因为更灵活）：
# df.groupby('部门').agg({'工资': 'mean'})

# --- 多种聚合 ---
result = df.groupby('部门').agg({
    '工资': ['mean', 'min', 'max'],  # 工资的平均、最小、最大
    '奖金': 'sum',                    # 奖金总和
    '员工': 'count'                   # 员工人数（计数）
})
print("\n各部门综合统计:\n", result)

# --- 更简洁的多函数聚合 ---
result2 = df.groupby('部门')['工资'].agg(['mean', 'sum', 'count', 'std'])
print("\n工资多指标:\n", result2)

# --- 对分组结果进行筛选（having效果）---
# 筛选出平均工资高于10000的部门
high_salary_dept = df.groupby('部门').filter(lambda x: x['工资'].mean() > 10000)
print("\n平均工资>10000的部门数据:\n", high_salary_dept)

# --- transform：给每条记录附上其分组的统计值 ---
df['部门平均工资'] = df.groupby('部门')['工资'].transform('mean')
df['工资与均值差'] = df['工资'] - df['部门平均工资']
print("\n附上部门均值:\n", df)
```

输出示例（`各部门综合统计`）：
```
      工资              奖金 员工
     mean   min    max  sum count
部门                                
市场  9250  9000   9500  4500     2
技术 13333 12000  15000 12000     3
销售  8100  7800   8500  5300     3
```

> **agg() vs transform()**：`agg()` 返回的是分组级别的汇总（每组一行），`transform()` 返回的是原数据行级的广播（每行一个值）。

#### 4.2.10 处理缺失值

真实世界的数据几乎都有缺失值，处理缺失值是数据分析的基本功。

```python
# 创建一个包含缺失值的 DataFrame
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "成绩": [85, np.nan, 78, 90, np.nan],
    "年龄": [25, 30, np.nan, 28, 26],
    "城市": ["北京", np.nan, "广州", "深圳", np.nan]
})
print("包含缺失值的数据:\n", df)

# --- 检测缺失值 ---
print("\n哪些位置是缺失的:\n", df.isna())        # 完整布尔矩阵
print(f"\n每列缺失值数量:\n{df.isna().sum()}")    # 按列统计
print(f"\n总缺失值数量: {df.isna().sum().sum()}")  # 总计

# --- 处理方式1：删除含缺失值的行 ---
df_dropped_rows = df.dropna()           # 删除任何有缺失的行
df_dropped_rows2 = df.dropna(subset=['成绩'])  # 只根据'成绩'列是否缺失来判断

# --- 处理方式2：删除含缺失值的列 ---
df_dropped_cols = df.dropna(axis=1)     # 删除任何有缺失的列

# --- 处理方式3：填充缺失值 ---
df_filled_const = df.fillna(0)                        # 用常数填充所有缺失
df_filled_mean = df.fillna({'成绩': df['成绩'].mean(), '年龄': df['年龄'].mean()})  # 用均值填充指定列
df_filled_method = df.fillna(method='ffill')          # 用前一个有效值填充

# --- 常用策略 ---
# 数值列：用均值或中位数填充
df['成绩'] = df['成绩'].fillna(df['成绩'].median())
# 分类列：用众数（最常见的值）填充 或 '未知'
df['城市'] = df['城市'].fillna('未知')

print("\n填充后的数据:\n", df)
```

> **缺失值处理策略速查**：
> - `dropna()` — 缺失很少时直接删（<5%）
> - `fillna(mean/median)` — 数值列用均值/中位数（最常用）
> - `fillna(mode)` — 分类列用众数或"未知"
> - `fillna(method='ffill')` — 时间序列数据用前一个值填充

#### 4.2.11 数据合并

```python
# --- 方式1：concat — 纵向或横向拼接 ---
df1 = pd.DataFrame({'姓名': ['张三', '李四'], '成绩': [85, 92]})
df2 = pd.DataFrame({'姓名': ['王五', '赵六'], '成绩': [78, 90]})

# 纵向拼接（追加行）
df_v = pd.concat([df1, df2], ignore_index=True)  # ignore_index重置索引
print("纵向拼接:\n", df_v)

# 横向拼接（追加列）
df3 = pd.DataFrame({'年龄': [25, 30, 22, 28]})
df_h = pd.concat([df_v, df3], axis=1)
print("\n横向拼接:\n", df_h)

# --- 方式2：merge — 类似SQL的JOIN ---
students = pd.DataFrame({
    '学号': ['001', '002', '003', '004'],
    '姓名': ['张三', '李四', '王五', '赵六'],
    '班级': ['1班', '1班', '2班', '2班']
})

scores = pd.DataFrame({
    '学号': ['001', '002', '003', '004', '005'],
    '数学': [85, 92, 78, 90, 88],
    '英语': [82, 88, 85, 92, 90]
})

# 内连接（默认）— 只保留两边都有的
inner = pd.merge(students, scores, on='学号', how='inner')
print("内连接:\n", inner)

# 左连接 — 保留左边表的全部数据
left = pd.merge(students, scores, on='学号', how='left')
print("\n左连接:\n", left)

# 外连接 — 保留两边的全部数据
outer = pd.merge(students, scores, on='学号', how='outer')
print("\n外连接:\n", outer)
```

> **concat vs merge**：concat 是简单的"粘在一起"，merge 是基于某个列（键）的"匹配合并"。大多数实际场景中，你用的是 merge。

---

### 第三部分：Matplotlib 数据可视化

#### 4.3.1 为什么需要可视化？

假设有两份完全相同的数据：

- **方式A**：一个 100 行 x 10 列的数字表格
- **方式B**：一张清晰的折线趋势图

显然，方式B 能让你在 1 秒内看到趋势、异常和规律，而方式A 可能需要几分钟甚至更久。

> **一张好的图表胜过千言万语。**

Matplotlib 是 Python 中最基础、最灵活的绑图库。后续你会学的 Seaborn、Plotly 等高级绑图库底层都依赖 Matplotlib。

#### 4.3.2 基本绘图流程

Matplotlib 的标准绘图流程：

```
创建画布 (figure) → 绑定 (plot/bar/pie...) → 设置标签 (title/xlabel...) → 显示 (show)
```

```python
import matplotlib.pyplot as plt
import numpy as np

# 1. 准备数据
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# 2. 创建画布
plt.figure(figsize=(8, 5))       # figsize=(宽, 高)，单位英寸

# 3. 绑定
plt.plot(x, y, marker='o', linestyle='-', color='blue', linewidth=2)

# 4. 设置标签
plt.title('基本折线图', fontsize=14)
plt.xlabel('X轴标签')
plt.ylabel('Y轴标签')

# 5. 显示
plt.grid(True, alpha=0.3)  # 添加网格
plt.show()
```

#### 4.3.3 折线图（Line Plot）

折线图最适合展示**随时间变化的趋势**。

```python
# 设置中文字体（重要！）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据
months = ['1月', '2月', '3月', '4月', '5月', '6月']
revenue = [12000, 13500, 11800, 15000, 14200, 16800]
cost = [8000, 8500, 8200, 9000, 8800, 9500]
profit = [r - c for r, c in zip(revenue, cost)]

plt.figure(figsize=(10, 6))

# 多条折线 — 一条收入、一条成本
plt.plot(months, revenue, 
         marker='o', markersize=8,        # 圆形标记，大小8
         linestyle='-', linewidth=2.5,    # 实线，宽度2.5
         color='#2ecc71', label='收入',   # 绿色
         markerfacecolor='white',         # 标记填充白色
         markeredgewidth=2)               # 标记边框宽度

plt.plot(months, cost,
         marker='s', markersize=8,        # 方形标记
         linestyle='--', linewidth=2.5,   # 虚线
         color='#e74c3c', label='成本',   # 红色
         markerfacecolor='white',
         markeredgewidth=2)

# 在每个数据点上标注数值
for i, (r, c) in enumerate(zip(revenue, cost)):
    plt.annotate(f'{r/10000:.2f}万', (months[i], revenue[i]), 
                 textcoords="offset points", xytext=(0, 12), 
                 ha='center', fontsize=9)
    plt.annotate(f'{c/10000:.2f}万', (months[i], cost[i]), 
                 textcoords="offset points", xytext=(0, -15), 
                 ha='center', fontsize=9, color='#e74c3c')

plt.title('2026年上半年收入与成本趋势', fontsize=16, fontweight='bold')
plt.xlabel('月份', fontsize=12)
plt.ylabel('金额（元）', fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, alpha=0.3, linestyle=':')
plt.tight_layout()
plt.show()

# 常用线型：'-' 实线, '--' 虚线, '-.' 点划线, ':' 点线
# 常用标记：'o' 圆, 's' 方, '^' 上三角, 'v' 下三角, 'd' 菱形, '*' 星
# 常用颜色缩写：'b' 蓝, 'g' 绿, 'r' 红, 'c' 青, 'm' 品红, 'y' 黄, 'k' 黑
```

#### 4.3.4 柱状图（Bar Chart）

柱状图最适合**类别之间的对比**。

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

products = ['产品A', '产品B', '产品C', '产品D', '产品E']
sales_qty = [234, 189, 345, 156, 298]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

plt.figure(figsize=(10, 6))
bars = plt.bar(products, sales_qty, color=colors, edgecolor='white', linewidth=1.5)

# 在每个柱子上方标注数值
for bar, val in zip(bars, sales_qty):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('各产品销量对比', fontsize=16, fontweight='bold')
plt.xlabel('产品', fontsize=12)
plt.ylabel('销量（件）', fontsize=12)
plt.ylim(0, max(sales_qty) * 1.15)  # 留出标注空间
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 横向柱状图（barh）— 类别名较长时特别有用
plt.figure(figsize=(8, 5))
plt.barh(products, sales_qty, color=colors, edgecolor='white')
plt.title('各产品销量对比（横向）', fontsize=14)
plt.xlabel('销量（件）')
plt.tight_layout()
plt.show()
```

#### 4.3.5 饼图（Pie Chart）

饼图适合展示**各部分在整体中的占比**，特别是当类别不超过 5-6 个时。

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

regions = ['华东', '华南', '华北', '西南', '西北']
ratios = [35, 25, 20, 12, 8]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
explode = (0.08, 0, 0, 0, 0)  # 突出第一块（华东）

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    ratios,
    labels=regions,
    autopct='%1.1f%%',           # 显示百分比，1位小数
    explode=explode,
    colors=colors,
    shadow=True,                  # 阴影效果
    startangle=90,                # 起始角度（12点钟方向）
    textprops={'fontsize': 12}
)

# 设置百分比文字样式
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.title('各区域销售占比', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
```

> **饼图使用建议**：当类别超过 6 个时改用柱状图，因为饼图在小碎片的可读性上很差。

#### 4.3.6 散点图（Scatter Plot）

散点图最适合展示**两个数值变量之间的关系**。

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
# 模拟数据：50个学生的"学习时间"和"考试成绩"
study_hours = np.random.uniform(1, 10, 50)  # 学习时间（小时）
noise = np.random.normal(0, 8, 50)           # 随机噪音
scores = 40 + study_hours * 5 + noise        # 考试成绩（分）
scores = np.clip(scores, 0, 100)             # 限制分数在0-100之间

# 将学习时间映射到点的颜色
colors = study_hours

plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    study_hours, scores,
    c=colors,              # 颜色映射到学习时间
    cmap='RdYlGn',         # 颜色方案：红→黄→绿
    s=study_hours * 15,    # 点的大小也映射到学习时间
    alpha=0.7,             # 透明度
    edgecolors='gray',     # 边框颜色
    linewidth=0.5
)

# 添加颜色条
cbar = plt.colorbar(scatter)
cbar.set_label('学习时间（小时）', fontsize=11)

plt.title('学习时间与考试成绩的关系', fontsize=16, fontweight='bold')
plt.xlabel('每周学习时间（小时）', fontsize=12)
plt.ylabel('考试成绩（分）', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("观察结论：学习时间越长，成绩整体呈上升趋势。但也有一些学习时间短但成绩好的'学霸'。")
```

#### 4.3.7 直方图（Histogram）

直方图展示**数据的分布情况**，让你看到数据集中在什么范围、有没有偏态。

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
# 模拟一次大课的考试成绩（200个学生）
# 大部分在60-80分，少量高分和低分
scores = np.concatenate([
    np.random.normal(65, 10, 100),   # 成绩偏低的群体
    np.random.normal(78, 8, 70),     # 中等群体
    np.random.normal(90, 5, 30)      # 高分群体
])

plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(
    scores,
    bins=20,                       # 分成20个区间
    edgecolor='white',
    color='steelblue',
    alpha=0.8,
    linewidth=1.2
)

# 在柱子上标注频数
for i in range(len(n)):
    if n[i] > 0:
        plt.text(bins[i] + (bins[1]-bins[0])/2, n[i] + 0.3,
                 int(n[i]), ha='center', fontsize=9)

# 标注均值线
mean_score = scores.mean()
plt.axvline(mean_score, color='red', linestyle='--', linewidth=2,
            label=f'平均分: {mean_score:.1f}')
# 标注及格线
plt.axvline(60, color='orange', linestyle=':', linewidth=2,
            label='及格线: 60')

plt.title('考试成绩分布直方图', fontsize=16, fontweight='bold')
plt.xlabel('分数区间', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.legend(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

print(f"总人数: {len(scores)}")
print(f"平均分: {scores.mean():.1f}")
print(f"及格率: {(scores >= 60).sum() / len(scores) * 100:.1f}%")
```

#### 4.3.8 子图布局

当你需要在一张图中展示多个图表时，使用子图（subplots）。

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建数据
months = ['1月', '2月', '3月', '4月', '5月', '6月']
revenue = [12000, 13500, 11800, 15000, 14200, 16800]
products = ['A', 'B', 'C', 'D']
sales_by_product = [234, 189, 345, 156]
regions = ['华东', '华南', '华北', '西南']
scores = np.random.normal(72, 12, 100)

# 创建2×2的子图布局
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 子图1：折线图（左上）
axes[0, 0].plot(months, revenue, marker='o', color='#2ecc71', linewidth=2)
axes[0, 0].set_title('月度收入趋势', fontsize=13)
axes[0, 0].set_ylabel('收入（元）')
axes[0, 0].grid(True, alpha=0.3)

# 子图2：柱状图（右上）
bar_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
axes[0, 1].bar(products, sales_by_product, color=bar_colors, edgecolor='white')
axes[0, 1].set_title('各产品销量', fontsize=13)
axes[0, 1].set_ylabel('销量（件）')

# 子图3：饼图（左下）
axes[1, 0].pie(regions, labels=regions, autopct='%1.1f%%',
               colors=bar_colors[:4], startangle=90)
axes[1, 0].set_title('地区分布', fontsize=13)

# 子图4：直方图（右下）
axes[1, 1].hist(scores, bins=15, edgecolor='white', color='steelblue', alpha=0.8)
axes[1, 1].set_title('成绩分布', fontsize=13)
axes[1, 1].set_xlabel('分数')
axes[1, 1].set_ylabel('人数')

# 整体标题
fig.suptitle('销售数据分析面板', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
```

#### 4.3.9 图表美化

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Matplotlib 内置样式
# 可用样式: 'ggplot', 'seaborn', 'fivethirtyeight', 'classic', 'bmh', 'dark_background'
plt.style.use('ggplot')  # 使用类似R的ggplot2风格

months = ['1月', '2月', '3月', '4月', '5月', '6月']
revenue = [12000, 13500, 11800, 15000, 14200, 16800]

plt.figure(figsize=(10, 6))
plt.plot(months, revenue, marker='D', linewidth=2.5, markersize=8, color='#2c3e50')

# 美化
plt.title('2026年上半年收入趋势', fontsize=18, fontweight='bold', pad=15)
plt.xlabel('月份', fontsize=13, labelpad=10)
plt.ylabel('收入（元）', fontsize=13, labelpad=10)
plt.grid(True, alpha=0.3, linestyle='--')

# 添加数据标签
for i, val in enumerate(revenue):
    plt.text(i, val + 300, f'¥{val:,}', ha='center', fontsize=11, fontweight='bold')

# 调整坐标轴范围
plt.ylim(0, max(revenue) * 1.1)

plt.tight_layout()
plt.show()

# 查看所有可用样式
# print(plt.style.available)
```

#### 4.3.10 中文显示解决方案

**这是 Windows 用户最常遇到的问题**。如果你的图表中文显示为方块，按以下步骤解决：

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 方案1：使用 rcParams（最简单，适合大多数情况）---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块

# --- 方案2：查看系统已安装的字体 ---
# 找出可用的中文字体
fonts = [f.name for f in fm.fontManager.ttflist if any(k in f.name for k in ['Hei', 'YaHei', 'Song', 'Ming', 'Kai'])]
print("系统中可用的中文字体:", fonts)

# --- 方案3：macOS专用 ---
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC']

# --- 方案4：如果以上都不行，手动指定字体路径 ---
# font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows示例
# font_prop = fm.FontProperties(fname=font_path)
# 然后在每个绑图函数中使用 fontproperties=font_prop

print("中文显示测试 → 折线图、柱状图、饼图 应该全部正常显示")
```

> **如果仍然显示方块**：把截图发给 ChatGPT 或 Claude，描述你的操作系统，AI 可以给出针对性的解决方案。

---

## 五、实操环节（70分钟）

### 练习1：销售数据分析完整项目（约40分钟）

**任务描述**：你将模拟一个数据分析师的日常工作——从生成数据到输出分析报告的全流程。

#### 步骤1：生成模拟销售数据（5分钟）

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 生成模拟数据
np.random.seed(42)
n_records = 200

# 生成日期（2026年上半年随机200天）
dates = pd.date_range('2026-01-01', '2026-06-30', periods=n_records)

# 产品列表
products = np.random.choice(['手机', '电脑', '平板', '耳机', '手表'], n_records)

# 地区列表
regions = np.random.choice(['华东', '华南', '华北', '西南', '西北'], n_records)

# 销量（1到100件）
quantities = np.random.randint(1, 101, n_records)

# 单价
price_map = {'手机': 3999, '电脑': 6999, '平板': 2999, '耳机': 299, '手表': 1999}
prices = [price_map[p] for p in products]

# 金额 = 销量 × 单价
amounts = quantities * np.array(prices)

# 创建DataFrame
df = pd.DataFrame({
    '日期': dates,
    '产品': products,
    '地区': regions,
    '销量': quantities,
    '单价': prices,
    '金额': amounts
})

# 人为添加一些缺失值和异常值（模拟真实数据的"脏"状况）
# 随机把5个金额设为缺失
mask = np.random.choice(n_records, 5, replace=False)
df.loc[mask, '金额'] = np.nan
# 随机把3个销量设为离谱值（异常值）
mask2 = np.random.choice(n_records, 3, replace=False)
df.loc[mask2, '销量'] = 9999

print(f"数据已生成！共 {len(df)} 条记录")
print(f"时间范围：{df['日期'].min().date()} 到 {df['日期'].max().date()}")
print(f"产品种类：{df['产品'].nunique()} 种")
print(f"覆盖地区：{df['地区'].nunique()} 个")
```

#### 步骤2：数据探查与清洗（8分钟）

```python
print("=" * 60)
print("               数据探查与清洗")
print("=" * 60)

# 查看前10行
print("\n【数据预览】")
print(df.head(10))

# 查看基本信息
print("\n【数据信息】")
print(df.info())

# 查看缺失值
print("\n【缺失值统计】")
print(df.isna().sum())

# 查看异常值（销量>100就是异常）
abnormal = df[df['销量'] > 100]
print(f"\n【异常值检测】发现 {len(abnormal)} 条异常销量记录：")
print(abnormal[['日期', '产品', '销量']])

# 数据清洗
print("\n【开始清洗数据】")
# 1. 处理缺失值：缺失的金额用 销量×单价 重新计算
df['金额'] = df['金额'].fillna(df['销量'] * df['单价'])
print("✓ 已填充缺失的金额")

# 2. 处理异常值：将异常销量替换为该产品的中位数销量
for product in df['产品'].unique():
    median_qty = df.loc[(df['产品'] == product) & (df['销量'] <= 100), '销量'].median()
    abnormal_mask = (df['产品'] == product) & (df['销量'] > 100)
    df.loc[abnormal_mask, '销量'] = median_qty
    df.loc[abnormal_mask, '金额'] = df.loc[abnormal_mask, '销量'] * df.loc[abnormal_mask, '单价']
print("✓ 已修正异常销量")

# 3. 添加辅助列
df['月份'] = df['日期'].dt.month
df['月份标签'] = df['月份'].apply(lambda x: f'{x}月')
df['星期'] = df['日期'].dt.day_name()

print(f"\n清洗完成！当前有效记录数：{len(df)}")
print(f"剩余缺失值：{df.isna().sum().sum()}")

# 查看统计摘要
print("\n【统计摘要】")
print(df.describe().round(1))
```

#### 步骤3：产品维度分析（8分钟）

```python
print("=" * 60)
print("               产品维度分析")
print("=" * 60)

# 按产品汇总
product_stats = df.groupby('产品').agg(
    总销量=('销量', 'sum'),
    总金额=('金额', 'sum'),
    平均单价=('单价', 'mean'),
    订单数=('销量', 'count')
).sort_values('总金额', ascending=False)

print("\n【各产品销售统计】")
print(product_stats)

# 计算产品的"贡献度"
product_stats['金额占比'] = (product_stats['总金额'] / product_stats['总金额'].sum() * 100).round(1)
product_stats['销量占比'] = (product_stats['总销量'] / product_stats['总销量'].sum() * 100).round(1)

print("\n【产品贡献度】")
print(product_stats)

# 可视化
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 产品销售金额柱状图
colors_prod = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
bars = axes[0].bar(product_stats.index, product_stats['总金额'], 
                   color=colors_prod, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, product_stats['总金额']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
                 f'{val/10000:.1f}万', ha='center', fontsize=10, fontweight='bold')
axes[0].set_title('各产品总销售额', fontsize=14, fontweight='bold')
axes[0].set_xlabel('产品')
axes[0].set_ylabel('金额（元）')
axes[0].set_ylim(0, product_stats['总金额'].max() * 1.15)

# 产品金额占比饼图
axes[1].pie(product_stats['总金额'], labels=product_stats.index,
            autopct='%1.1f%%', colors=colors_prod, startangle=90,
            textprops={'fontsize': 11})
axes[1].set_title('各产品销售金额占比', fontsize=14, fontweight='bold')

plt.suptitle('产品维度分析', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
```

预期输出：
- 电脑的客单价最高，总金额一般排第一
- 耳机的单价低，但销量可能很大
- 金额占比饼图直观展示各产品的贡献权重

#### 步骤4：地区维度分析（8分钟）

```python
print("=" * 60)
print("               地区维度分析")
print("=" * 60)

# 按地区汇总
region_stats = df.groupby('地区').agg(
    总销量=('销量', 'sum'),
    总金额=('金额', 'sum'),
    订单数=('销量', 'count'),
    客单价=('金额', 'mean')
).sort_values('总金额', ascending=False)

region_stats['金额占比'] = (region_stats['总金额'] / region_stats['总金额'].sum() * 100).round(1)
print("\n【各地区销售统计】")
print(region_stats)

# 找出每个地区最畅销的产品
print("\n【各地区最畅销产品（按金额）】")
for region in df['地区'].unique():
    region_data = df[df['地区'] == region]
    top_product = region_data.groupby('产品')['金额'].sum().idxmax()
    top_amount = region_data.groupby('产品')['金额'].sum().max()
    print(f"  {region}: {top_product} (¥{top_amount:,.0f})")

# 可视化：地区-产品交叉分析
pivot = df.pivot_table(values='金额', index='地区', columns='产品', aggfunc='sum', fill_value=0)
print("\n【地区×产品交叉表（金额）】")
print(pivot)

# 堆叠柱状图
fig, ax = plt.subplots(figsize=(12, 6))
pivot.plot(kind='bar', stacked=True, ax=ax, 
           color=colors_prod, edgecolor='white', linewidth=1)
ax.set_title('各地区各产品销售金额（堆叠）', fontsize=14, fontweight='bold')
ax.set_xlabel('地区')
ax.set_ylabel('金额（元）')
ax.legend(title='产品', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.show()
```

#### 步骤5：月度趋势分析（5分钟）

```python
# 月度趋势
monthly_stats = df.groupby('月份标签').agg(
    总金额=('金额', 'sum'),
    总销量=('销量', 'sum'),
    订单数=('销量', 'count'),
    日均金额=('金额', lambda x: x.sum() / x.count())
).reindex(['1月', '2月', '3月', '4月', '5月', '6月'])

print("【月度销售趋势】")
print(monthly_stats)

# 计算环比增长率
monthly_stats['金额环比'] = monthly_stats['总金额'].pct_change() * 100
print("\n【月度金额环比增长率（%）】")
print(monthly_stats['金额环比'].round(1))

# 可视化：双轴图
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左轴：金额（柱状图）
bars = ax1.bar(monthly_stats.index, monthly_stats['总金额'], 
               color='steelblue', alpha=0.7, label='总金额', edgecolor='white')
ax1.set_xlabel('月份', fontsize=12)
ax1.set_ylabel('总金额（元）', fontsize=12, color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
for bar, val in zip(bars, monthly_stats['总金额']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f'{val/10000:.1f}万', ha='center', fontsize=10, fontweight='bold')

# 右轴：环比增长率（折线图）
ax2 = ax1.twinx()
ax2.plot(monthly_stats.index, monthly_stats['金额环比'], 
         marker='o', color='#e74c3c', linewidth=2.5, markersize=8, label='环比增长率')
ax2.set_ylabel('环比增长率（%）', fontsize=12, color='#e74c3c')
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
for i, (idx, row) in enumerate(monthly_stats.iterrows()):
    if not np.isnan(row['金额环比']):
        ax2.annotate(f'{row["金额环比"]:.1f}%', (idx, row['金额环比']),
                     textcoords="offset points", xytext=(0, 12),
                     ha='center', fontsize=10, color='#e74c3c', fontweight='bold')

fig.suptitle('月度销售趋势与环比增长', fontsize=16, fontweight='bold')
# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)
plt.tight_layout()
plt.show()

print("\n分析结论：")
best_month = monthly_stats['总金额'].idxmax()
worst_month = monthly_stats['总金额'].idxmin()
print(f"  销售额最高月份：{best_month}")
print(f"  销售额最低月份：{worst_month}")
print(f"  整体趋势：{'上升' if monthly_stats['总金额'].iloc[-1] > monthly_stats['总金额'].iloc[0] else '下降'}")
```

---

### 练习2：学生成绩分析报告（约30分钟）

**任务描述**：你是一个班主任，需要对班级期中考试成绩进行全方位分析，最后生成一份分析报告。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子
np.random.seed(2026)

# 生成30个学生的数据
n_students = 30
students_data = {
    '学号': [f'2026{i:03d}' for i in range(1, n_students + 1)],
    '姓名': ['学生' + str(i) for i in range(1, n_students + 1)],
    '语文': np.random.normal(78, 10, n_students).clip(40, 100).round(1),
    '数学': np.random.normal(72, 15, n_students).clip(30, 100).round(1),
    '英语': np.random.normal(75, 12, n_students).clip(35, 100).round(1),
    '物理': np.random.normal(68, 16, n_students).clip(25, 100).round(1),
    '化学': np.random.normal(73, 13, n_students).clip(30, 100).round(1),
}
df = pd.DataFrame(students_data)

# 人为添加少量缺失值（模拟缺考情况）
df.loc[np.random.choice(n_students, 2, replace=False), '数学'] = np.nan
df.loc[np.random.choice(n_students, 2, replace=False), '物理'] = np.nan

print("=" * 60)
print("            期中考试成绩分析报告")
print("=" * 60)

# ============================================
# 第1步：数据清洗与计算
# ============================================
print("\n【数据清洗】")

# 检测缺失值
missing = df.isna().sum()
print(f"原始缺失值:\n{missing[missing > 0]}")

# 填充缺失值（缺考按该科平均分的60%计，模拟补考分数）
score_cols = ['语文', '数学', '英语', '物理', '化学']
for col in score_cols:
    if missing[col] > 0:
        fill_value = round(df[col].mean() * 0.6, 1)
        df[col] = df[col].fillna(fill_value)
        print(f"  {col}: 缺考{int(missing[col])}人，按{fill_value}分计入")

# 计算总分、平均分、排名
df['总分'] = df[score_cols].sum(axis=1)
df['平均分'] = (df[df[score_cols].notna().all(axis=1)][score_cols].mean(axis=1))
df['平均分'] = df[score_cols].mean(axis=1).round(1)
df['排名'] = df['总分'].rank(ascending=False, method='min').astype(int)

# 添加等级
def assign_grade(avg):
    if avg >= 90:
        return 'A (优秀)'
    elif avg >= 80:
        return 'B (良好)'
    elif avg >= 70:
        return 'C (中等)'
    elif avg >= 60:
        return 'D (及格)'
    else:
        return 'F (不及格)'

df['等级'] = df['平均分'].apply(assign_grade)

# 按总分排序
df_sorted = df.sort_values('总分', ascending=False).reset_index(drop=True)

# ============================================
# 第2步：成绩概览
# ============================================
print(f"\n{'='*60}")
print(f"                    成绩概览")
print(f"{'='*60}")
print(f"班级人数：{len(df)} 人")
print(f"\n【总分统计】")
print(f"  平均分：{df['总分'].mean():.1f}")
print(f"  中位数：{df['总分'].median():.1f}")
print(f"  最高分：{df['总分'].max():.1f}")
print(f"  最低分：{df['总分'].min():.1f}")
print(f"  标准差：{df['总分'].std():.1f}")
print(f"  极差（最高-最低）：{df['总分'].max() - df['总分'].min():.1f}")

print(f"\n【各科统计】")
subject_stats = df[score_cols].describe().round(1)
print(subject_stats)

print(f"\n【等级分布】")
grade_dist = df['等级'].value_counts()
grade_order = ['A (优秀)', 'B (良好)', 'C (中等)', 'D (及格)', 'F (不及格)']
for g in grade_order:
    count = grade_dist.get(g, 0)
    pct = count / len(df) * 100
    bar = '█' * int(pct / 2)
    print(f"  {g}: {count}人 ({pct:.1f}%) {bar}")

print(f"\n【年级前5名】")
print(df_sorted[['排名', '姓名', '总分', '平均分', '等级']].head(5).to_string(index=False))

print(f"\n【年级后5名】")
print(df_sorted[['排名', '姓名', '总分', '平均分', '等级']].tail(5).to_string(index=False))

# ============================================
# 第3步：各科详细分析
# ============================================
print(f"\n{'='*60}")
print(f"                    各科详细分析")
print(f"{'='*60}")

for col in score_cols:
    data = df[col]
    pass_rate = (data >= 60).sum() / len(df) * 100
    excellent_rate = (data >= 90).sum() / len(df) * 100
    print(f"\n【{col}】")
    print(f"  平均分：{data.mean():.1f}  |  中位数：{data.median():.1f}")
    print(f"  最高分：{data.max():.1f}  |  最低分：{data.min():.1f}")
    print(f"  及格率：{pass_rate:.1f}%  |  优秀率(>=90)：{excellent_rate:.1f}%")
    print(f"  标准差：{data.std():.1f}")

# 找出各科最高分的学生
print(f"\n【各科状元】")
for col in score_cols:
    max_score = df[col].max()
    top_students = df[df[col] == max_score]['姓名'].tolist()
    print(f"  {col}: {', '.join(top_students)} ({max_score:.1f}分)")

# 单科不及格人数统计
print(f"\n【单科不及格统计】")
for col in score_cols:
    fail_count = (df[col] < 60).sum()
    if fail_count > 0:
        print(f"  {col}: {fail_count}人不及格")
    else:
        print(f"  {col}: 全部及格 ✓")

# ============================================
# 第4步：可视化分析（4张图）
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# --- 图1：各科成绩箱线图 ---
box_data = [df[col].dropna().values for col in score_cols]
bp = axes[0, 0].boxplot(box_data, labels=score_cols, patch_artist=True,
                          showmeans=True, meanprops=dict(marker='D', markerfacecolor='red', markersize=6))
colors_box = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0, 0].set_title('各科成绩箱线图', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('分数')
axes[0, 0].grid(axis='y', alpha=0.3)

# --- 图2：总分分布直方图 ---
n, bins, patches = axes[0, 1].hist(df['总分'], bins=12, edgecolor='white', 
                                    color='steelblue', alpha=0.8)
axes[0, 1].axvline(df['总分'].mean(), color='red', linestyle='--', linewidth=2, label=f'平均分: {df["总分"].mean():.0f}')
axes[0, 1].axvline(60 * len(score_cols), color='orange', linestyle=':', linewidth=2, label=f'总分及格线: {60*len(score_cols)}')
axes[0, 1].set_title('总分分布直方图', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('总分')
axes[0, 1].set_ylabel('人数')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(axis='y', alpha=0.3)

# --- 图3：各科目平均分对比 ---
avg_scores = df[score_cols].mean()
bar_colors = colors_box[:5]
bars = axes[1, 0].bar(avg_scores.index, avg_scores.values, color=bar_colors, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, avg_scores.values):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', fontsize=11, fontweight='bold')
axes[1, 0].set_title('各科目平均分对比', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('平均分')
axes[1, 0].set_ylim(0, 100)
axes[1, 0].grid(axis='y', alpha=0.3)
# 标注全科总平均
total_avg = avg_scores.mean()
axes[1, 0].axhline(total_avg, color='gray', linestyle='--', alpha=0.7, label=f'全科总平均: {total_avg:.1f}')
axes[1, 0].legend()

# --- 图4：等级分布饼图 ---
grade_order_short = ['A', 'B', 'C', 'D', 'F']
grade_full = ['A (优秀)', 'B (良好)', 'C (中等)', 'D (及格)', 'F (不及格)']
grade_counts = [grade_dist.get(g, 0) for g in grade_full]
pie_colors = ['#2ecc71', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
# 只显示非0的类别
non_zero_labels = [f'{s}({c}人)' for s, c in zip(grade_order_short, grade_counts) if c > 0]
non_zero_counts = [c for c in grade_counts if c > 0]
non_zero_colors = [pie_colors[i] for i, c in enumerate(grade_counts) if c > 0]
wedges, texts, autotexts = axes[1, 1].pie(
    non_zero_counts, labels=non_zero_labels, autopct='%1.1f%%',
    colors=non_zero_colors, startangle=90, textprops={'fontsize': 10}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
axes[1, 1].set_title('等级分布', fontsize=14, fontweight='bold')

fig.suptitle('期中考试成绩分析', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# ============================================
# 第5步：生成分析总结
# ============================================
print(f"\n{'='*60}")
print(f"                    分析总结")
print(f"{'='*60}")
print(f"""
一、整体情况
  - 班级{len(df)}人，总分平均{df['总分'].mean():.1f}分，中位数{df['总分'].median():.1f}分
  - 及格率：{grade_dist.get('D (及格)', 0) + grade_dist.get('C (中等)', 0) + grade_dist.get('B (良好)', 0) + grade_dist.get('A (优秀)', 0)}/{len(df)}人 ({(len(df) - grade_dist.get('F (不及格)', 0)) / len(df) * 100:.1f}%)
  - 优秀率：{grade_dist.get('A (优秀)', 0)}/{len(df)}人 ({grade_dist.get('A (优秀)', 0) / len(df) * 100:.1f}%)

二、学科差异
  - 平均分最高：{avg_scores.idxmax()} ({avg_scores.max():.1f}分)
  - 平均分最低：{avg_scores.idxmin()} ({avg_scores.min():.1f}分)
  - 标准差最大：{df[score_cols].std().idxmax()} — 学生分化最明显
  - 标准差最小：{df[score_cols].std().idxmin()} — 学生水平最均衡

三、重点关注
  - 不及格学生：{grade_dist.get('F (不及格)', 0)}人，需要重点关注和辅导
  - 边缘学生（D等级）：{grade_dist.get('D (及格)', 0)}人，有提升潜力的"临界生"
  - 单科薄弱：各科不及格人数如上表，建议针对性补课
""")
```

---

## 六、课后作业（第2周综合）

> **本周大作业**：独立完成一份数据分析项目

### 任务要求

**选题方向**（三选一）：

1. **找一份真实数据**：你的课程实验数据、学院发的统计表格、从网上下载的公开数据集都可以
2. **使用 Kaggle 入门数据集**：推荐 [Kaggle](https://www.kaggle.com/datasets) 搜索 "beginner"，如 Titanic、Iris、Walmart Sales 等
3. **自己编一份有意义的数据**：根据你专业的场景模拟一份数据（如建筑能耗数据、机械性能测试数据等）

**必须包含的分析内容**：

| 序号 | 分析步骤 | 说明 |
|------|----------|------|
| 1 | 数据清洗 | 检查并处理缺失值、异常值 |
| 2 | 描述性统计 | 均值、中位数、标准差、分位数等 |
| 3 | 分组聚合 | 至少从 **3个维度** 做分组聚合分析 |
| 4 | 数据可视化 | 至少 **3种不同类型** 的图表 |
| 5 | 分析报告 | 500字以上的文字分析报告 |
| 6 | 代码注释 | 关键代码行要有中文注释 |

**提交内容**：

1. **Jupyter Notebook 文件**（`.ipynb`）：包含完整代码和运行输出
2. **数据文件**：你使用的原始数据（CSV 或 Excel）
3. **分析报告**：Markdown 格式或 Word 格式，500字以上

**评分标准**：

| 维度 | 权重 | 说明 |
|------|------|------|
| 数据清洗完整性 | 20% | 缺失值、异常值处理得当 |
| 分析深度 | 25% | 多维度分析，有洞察 |
| 可视化质量 | 25% | 图表类型丰富、标注清晰 |
| 报告质量 | 20% | 结论清晰，有理有据 |
| 代码规范 | 10% | 有注释，结构清晰 |

> **提示**：整个过程中遇到任何困难，优先问 ChatGPT 或 Claude。把错误信息、你的意图和数据的基本信息告诉 AI，它能帮你写出正确的代码。这就是 AI 时代的学习方式——**不是记住所有 API，而是知道怎么让 AI 帮你找到正确的 API**。

---

## 七、拓展阅读

| 资源 | 说明 | 链接/获取方式 |
|------|------|--------------|
| 《利用 Python 进行数据分析》 | 数据分析领域最经典的书籍，作者是 Pandas 的创始人 Wes McKinney。强烈推荐作为案头参考书。 | 各电商平台搜索购买（O'Reilly 出版） |
| NumPy 官方教程 | NumPy 官方提供的快速入门教程，涵盖所有基础操作 | [numpy.org/doc/stable/user/quickstart.html](https://numpy.org/doc/stable/user/quickstart.html) |
| Pandas 官方教程 | Pandas 官方提供的 10 分钟入门，非常实用 | [pandas.pydata.org/docs/user_guide/10min.html](https://pandas.pydata.org/docs/user_guide/10min.html) |
| Matplotlib 官方教程 | 包含所有图表类型的示例代码，可以直接复制修改 | [matplotlib.org/stable/tutorials/index.html](https://matplotlib.org/stable/tutorials/index.html) |
| DataWhale Pandas 练习题 | 中文社区的 Pandas 练习，由浅入深 | 搜索 "DataWhale Pandas 练习" |
| Kaggle Learn — Pandas | 交互式在线课程，在浏览器中边学边练 | [kaggle.com/learn/pandas](https://www.kaggle.com/learn/pandas) |
| Real Python — Pandas 教程 | 图文并茂的英文教程，讲解非常细致 | [realpython.com/pandas-python-explore-dataset](https://realpython.com/pandas-python-explore-dataset/) |

---

## 八、常见问题

### Q1：图表中文显示为方块怎么办？

**答**：这是 Windows 上最常见的问题。按以下顺序尝试：

1. 确保设置了中文字体：`plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']`
2. 确保设置了负号：`plt.rcParams['axes.unicode_minus'] = False`
3. 如果仍然不行，检查系统是否安装了 SimHei（黑体）字体
4. 终极方案：把错误截图发给 AI，让它根据你的操作系统给出解决方案

### Q2：Pandas 读取 CSV 文件乱码怎么办？

**答**：这是编码问题，CSV 文件可能不是 UTF-8 编码。解决方法：

```python
# 尝试不同的编码
df = pd.read_csv('file.csv', encoding='utf-8')      # 先试UTF-8
df = pd.read_csv('file.csv', encoding='gbk')         # 再试GBK（中文Windows常用）
df = pd.read_csv('file.csv', encoding='gb2312')      # 再试GB2312
df = pd.read_csv('file.csv', encoding='latin-1')     # 兜底方案
```

如果不确定文件编码，可以把文件路径告诉 AI，让 AI 帮你写自动检测编码的代码。

### Q3：数据太大，Pandas 处理很慢怎么办？

**答**：
1. 使用 `chunksize` 分块读取：`pd.read_csv('file.csv', chunksize=10000)`
2. 使用 `dtype` 参数指定列类型，避免 Pandas 自动推断（特别是大文件）
3. 只读取需要的列：`pd.read_csv('file.csv', usecols=['col1', 'col2'])`
4. 先用 `df.info()` 查看内存占用，用 `df.memory_usage(deep=True)` 查看详细内存
5. 对于超大文件（GB 级别），考虑使用 Dask 或 Polars 替代 Pandas

### Q4：日期数据总是显示为奇怪的数字怎么办？

**答**：Pandas 的日期列默认是 `object` 或 `datetime64` 类型。使用以下方法转换：

```python
# 将字符串列转为日期类型
df['日期'] = pd.to_datetime(df['日期'])

# 如果格式非标准，指定格式
df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')

# 转换后可以提取各种时间信息
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month
df['周几'] = df['日期'].dt.day_name()
```

### Q5：groupby 之后结果很奇怪，不知道怎么用？

**答**：GroupBy 操作分三步：分裂 → 应用 → 组合。

```python
# 标准流程
result = df.groupby('分组列')['目标列'].agg(聚合函数)

# 常见错误1：groupby后直接print，看到的是GroupBy对象而非结果
print(df.groupby('产品'))  # 错误！不会显示数据
print(df.groupby('产品')['金额'].sum())  # 正确！会显示聚合结果

# 常见错误2：忘记reset_index
result = df.groupby('产品')['金额'].sum()  # 返回Series，索引是产品名
result = df.groupby('产品')['金额'].sum().reset_index()  # 返回DataFrame，更易操作
```

### Q6：如何快速记住 Pandas 的 API？

**答**：**不需要刻意记忆**。以下是实际工作中最高效的方式：

1. **问 AI**："Pandas 怎么按某列分组然后计算平均值？" AI 会给你正确的代码
2. **保留一份常用操作速查表**（贴在桌面上）：数据选择、筛选、分组聚合、缺失值处理
3. **多练习**：同一类操作做 5-10 次后，自然而然就记住了
4. **理解原理比记住 API 更重要**：知道 groupby 是"分裂-应用-组合"三阶段，知道 merge 是"按键匹配"，具体的函数名忘了查就行

在本课程中，请大胆使用 AI 工具辅助编程。AI 时代的学习不是比拼记忆力，而是比拼"知道问什么、怎么问、如何验证 AI 给出的答案"的能力。

---

> **本节完** | 下节预告：第3周 机器学习入门 — 垃圾邮件识别与鸢尾花分类
