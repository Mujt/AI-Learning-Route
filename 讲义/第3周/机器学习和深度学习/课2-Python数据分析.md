# 课2：Python 数据分析（NumPy / Pandas / Matplotlib）

> **课时**：2 小时（120 分钟）
> **定位**：第2周 Python 开发第 2 堂。学习数据分析三件套——NumPy（数值计算）、Pandas（表格处理）、Matplotlib（可视化）。
> **目标**：学完后，能读懂项目中"读取数据 → 清洗 → 分析 → 可视化"的代码流程，并借助 AI 完成简单分析报告。
> **前置**：课1（Python 基础与 Skills 实战）。
> **安装**：`pip install numpy pandas matplotlib`

---

## 一、为什么学数据分析（10 分钟）

### 1.1 Python 最大的应用场景之一

```
数据分析/机器学习 是 Python 的"主场"：
- 数据分析师 / 数据科学家：Python 第一语言
- 机器学习（第3周）：数据处理阶段几乎全用 Pandas
- Agent 开发：工具函数经常要处理结构化数据（表格、CSV、JSON）
- 前端/后端项目：报表接口、数据统计、爬虫数据清洗
```

### 1.2 三件套的分工

```
NumPy（Numerical Python）→ 多维数组 + 高效数值计算（底层引擎）
Pandas → 表格（DataFrame）+ 数据处理（读CSV/筛选/分组/聚合）
Matplotlib → 画图（折线/柱状/饼图/散点）
```

> **比喻**：
> - NumPy = 计算器（速度快，处理数字）
> - Pandas = Excel 高级版（表格 + 公式 + 透视表）
> - Matplotlib = 图表工具（把数据画成图）

### 1.3 本课"读代码"目标

- 认识 `np.array`、`df`（DataFrame）、`plt` 三种对象的核心操作
- 能看懂"读 CSV → 筛选 → 分组 → 画图"的标准流程
- 学会中文乱码、CSV 乱码的解决方案

---

## 二、NumPy：高效数值计算（25 分钟）

### 2.1 数组创建

```python
import numpy as np

# 从列表创建
arr = np.array([1, 2, 3, 4, 5])
print(arr)                # [1 2 3 4 5]
print(type(arr))          # <class 'numpy.ndarray'>

# 二维数组（矩阵）
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)

# 常用创建函数
np.zeros(3)               # [0. 0. 0.]
np.ones((2, 3))           # 2行3列全1
np.arange(10)             # [0 1 2 ... 9]（类似 range）
np.linspace(0, 1, 5)      # [0. 0.25 0.5 0.75 1.]（0-1 均匀分5份）
np.random.rand(3)         # 3个0-1随机数
np.random.randint(1, 100, 5)  # 5个1-99随机整数
```

### 2.2 数组属性与索引切片

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

arr.shape         # (2, 3)：2行3列（最常用属性）
arr.ndim          # 2：维度
arr.size          # 6：元素总数
arr.dtype         # dtype('int64')：数据类型

# 索引：跟列表类似，但用 [行, 列]
print(arr[0, 1])      # 2（第0行第1列）
print(arr[1, :])      # [4 5 6]（第1行全部）
print(arr[:, 2])      # [3 6]（第2列全部）
print(arr[0:2, 0:2])  # 左上2x2子矩阵
```

### 2.3 向量化运算（NumPy 的灵魂）

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)      # [11 22 33]（对应位置相加，不需要循环！）
print(a * 2)      # [2 4 6]（标量广播）
print(a ** 2)     # [1 4 9]
print(a > 2)      # [False False  True]（布尔数组）

# 广播（broadcasting）：不同形状也能算
print(np.array([1, 2, 3]) + 100)   # [101 102 103]
```

> **读懂意义**：NumPy 最重要的特性是**向量化**——对一整个数组做运算，不用写 for 循环。**读代码时看到数组直接参与 `+ - * /` 和比较，就知道是向量化运算**。

### 2.4 统计函数（数据分析最常用）

```python
data = np.array([85, 92, 67, 88, 59, 76])

data.mean()           # 77.83...（平均值）
data.sum()            # 467
data.min()            # 59
data.max()            # 92
data.std()            # 标准差（数据波动程度）
data.median()         # 中位数（用 np.median(data)）
np.percentile(data, 75)   # 75%分位数
np.argmax(data)       # 3（最大值的索引）
np.argmin(data)       # 4（最小值的索引）
```

### 2.5 布尔索引（条件筛选）

```python
data = np.array([85, 92, 67, 88, 59, 76])

# 筛选出及格（>=60）的成绩
passed = data[data >= 60]
print(passed)     # [85 92 67 88 76]

# 复杂条件
selected = data[(data >= 70) & (data <= 90)]
print(selected)   # [85 88 76]
```

> **读懂重点**：`数组[布尔数组]` 就是布尔索引——"只保留条件为 True 的元素"。这是 Pandas 筛选的底层原理，必须吃透。

---

## 三、Pandas：表格数据处理（35 分钟）

### 3.1 两种核心结构

```python
import pandas as pd

# Series：一列数据（带索引）
s = pd.Series([85, 92, 88], index=["张三", "李四", "王五"])
print(s["张三"])     # 85（用标签索引）

# DataFrame：表格（多列）
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "成绩": [85, 92, 88],
    "年龄": [20, 21, 19]
})
print(df)
#   姓名  成绩  年龄
# 0  张三   85   20
# 1  李四   92   21
# 2  王五   88   19
```

> **DataFrame 就是"带表头的 Excel 表格"**——行是记录，列是字段。读项目代码时，见到 `df` 变量基本就是 DataFrame。

### 3.2 从文件创建（数据分析的第一步）

```python
# 读 CSV（注意 encoding 处理中文）
df = pd.read_csv("scores.csv", encoding="utf-8-sig")

# 读 Excel
df = pd.read_excel("scores.xlsx")

# 读 JSON
df = pd.read_json("data.json")

# 从字典/列表创建
df = pd.DataFrame([{"name": "张三", "age": 20}, {"name": "李四", "age": 21}])

# 保存
df.to_csv("output.csv", index=False, encoding="utf-8-sig")
df.to_excel("output.xlsx", index=False)
```

> **安装依赖**：读 Excel 需要 `pip install openpyxl`。

### 3.3 数据查看（读陌生数据的标准动作）

```python
df.head()          # 前5行（快速看一眼）
df.tail(3)         # 后3行
df.info()          # 每列的类型、非空数量（超常用！）
df.describe()      # 数值列的统计（count/mean/std/min/max）
df.shape           # (行数, 列数)
df.columns         # 列名列表
df.dtypes          # 每列类型
```

> **读数据分析代码第一动作**：`df.head()` + `df.info()`——先知道数据长什么样。

### 3.4 数据选择（读代码最高频操作）

```python
# 选一列（返回 Series）
df["成绩"]
df.成绩              # 等价简写（列名像变量名时才可用）

# 选多列
df[["姓名", "成绩"]]

# 按行号选：iloc（integer location）
df.iloc[0]           # 第0行
df.iloc[1:3]         # 第1-2行

# 按标签选：loc
df.loc[0]            # 第0行（索引为0）
df.loc[df["成绩"] > 85]   # 成绩>85的所有行（最常用！）

# 同时选行和列
df.loc[0, "成绩"]    # 第0行的成绩
df.loc[:, "姓名"]    # 所有行的姓名列
```

> **iloc vs loc（必须分清）**：
> - `iloc`：按**位置**（数字）选
> - `loc`：按**标签**选（行索引名 / 列名 / 布尔条件）
> - 记忆：**i = index 位置**；布尔筛选用 `df[df["列"] > 值]` 或 `df.loc[条件]`

### 3.5 数据筛选与清洗

```python
# 条件筛选（读代码最最常见）
high = df[df["成绩"] >= 90]
in_class = df[df["班级"] == "1班"]
between = df[(df["成绩"] >= 80) & (df["成绩"] <= 90)]

# 字符串筛选
df[df["姓名"].str.contains("张")]

# 缺失值处理（脏数据必备）
df.isna().sum()        # 每列有多少缺失值
df.dropna()            # 删除有缺失的行
df.fillna(0)           # 缺失值填 0
df["成绩"].fillna(df["成绩"].mean())   # 用均值填充

# 删除重复
df.drop_duplicates()

# 排序
df.sort_values("成绩", ascending=False)   # 按成绩降序
```

> **读代码套路**：`df[df["列"] 比较 值]` 这个模式出现频率极高，翻译成人话就是"把满足条件的行挑出来"。

### 3.6 新增列与运算

```python
# 新增列（向量化）
df["总分"] = df["语文"] + df["数学"] + df["英语"]
df["是否及格"] = df["成绩"] >= 60        # 布尔列
df["平均分"] = df[["语文", "数学"]].mean(axis=1)  # 按行平均

# apply：对每行/每列应用函数（读 Agent 代码常遇到）
df["成绩等级"] = df["成绩"].apply(lambda x: "优" if x >= 90 else "良")
```

### 3.7 分组聚合（groupby，数据分析的灵魂操作）

```python
# 场景：每个班级的平均成绩
df = pd.DataFrame({
    "班级": ["1班", "1班", "2班", "2班", "2班"],
    "姓名": ["张三", "李四", "王五", "赵六", "孙七"],
    "成绩": [85, 92, 78, 88, 65]
})

# 按班级分组，算平均成绩
result = df.groupby("班级")["成绩"].mean()
print(result)
# 班级
# 1班    88.5
# 2班    77.0

# 多列聚合
df.groupby("班级")["成绩"].agg(["mean", "max", "min", "count"])

# 分组后遍历（读代码遇到）
for class_name, group in df.groupby("班级"):
    print(class_name, len(group))
```

> **读懂 groupby 三要素**：`df.groupby(分组依据)[要计算的列].聚合函数`。
> - 分组依据：按什么分（班级）
> - 计算列：对哪列算（成绩）
> - 聚合函数：怎么算（mean/max/min/sum/count）
>
> **翻译成人话**："按班级分组，算出每个班的平均成绩。"这是**数据分析代码中出现频率最高的模式**，第3周机器学习预处理也会用到。

### 3.8 数据合并

```python
# concat：纵向拼接（上下合并）
df_all = pd.concat([df1, df2], ignore_index=True)

# merge：横向合并（类似 Excel VLOOKUP）
df_merge = pd.merge(df_scores, df_students, on="学号", how="left")
```

---

## 四、Matplotlib：数据可视化（25 分钟）

### 4.1 基本绘图流程（固定五步）

```python
import matplotlib.pyplot as plt

# 第1步：准备数据
x = [1, 2, 3, 4, 5]
y = [10, 25, 15, 40, 30]

# 第2步：创建图形
plt.figure(figsize=(8, 5))

# 第3步：画图（这里用折线图）
plt.plot(x, y, marker="o")

# 第4步：标签和标题
plt.xlabel("月份")
plt.ylabel("销量")
plt.title("月度销量")

# 第5步：显示/保存
plt.show()                    # 显示窗口
# plt.savefig("chart.png", dpi=150)   # 或保存为图片
```

> **读代码重点**：Matplotlib 代码结构永远是"准备数据 → `plt.xxx()` 画图 → 标签 → `plt.show()`/`savefig`"。

### 4.2 五种基础图（读代码识别）

```python
# 折线图：趋势
plt.plot(x, y)

# 柱状图：对比
plt.bar(["苹果", "香蕉", "橙子"], [30, 45, 20])

# 饼图：占比
plt.pie([30, 45, 20], labels=["苹果", "香蕉", "橙子"], autopct="%1.1f%%")

# 散点图：两个变量的关系
plt.scatter([1, 2, 3, 4], [2, 4, 5, 8])

# 直方图：分布
plt.hist(np.random.randn(1000), bins=30)
```

### 4.3 与 Pandas 联用（数据分析标准流程）

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scores.csv", encoding="utf-8-sig")

# 柱状图：各班平均分
avg = df.groupby("班级")["成绩"].mean()
avg.plot(kind="bar")          # Pandas 内置 plot 方法
plt.title("各班平均成绩")
plt.show()

# 折线图：趋势
df.plot(x="日期", y="销量", kind="line")
```

### 4.4 中文显示解决方案（Windows 必备）

```python
import matplotlib.pyplot as plt

# 解决中文乱码：设置中文字体（在画图前执行）
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]   # 黑体/微软雅黑
plt.rcParams["axes.unicode_minus"] = False   # 解决负号显示为方块

# 验证
plt.plot([1, 2, 3], [1, 4, 9])
plt.title("中文标题测试")
plt.show()
```

### 4.5 子图布局（多图对比）

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1行2列
axes[0].plot([1, 2, 3], [3, 1, 4], title="左图")
axes[1].bar(["A", "B"], [5, 3], title="右图")
plt.tight_layout()
plt.show()
```

---

## 五、完整实战：学生成绩分析报告（25 分钟）

综合运用三件套，完成一个"读数据 → 分析 → 画图"的完整项目。

```python
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 第1步：创建模拟数据（真实项目中这里是 df = pd.read_csv(...)）
data = {
    "姓名": ["张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十"],
    "班级": ["1班", "1班", "1班", "2班", "2班", "2班", "3班", "3班"],
    "语文": [85, 92, 78, 88, 65, 95, 72, 80],
    "数学": [90, 76, 88, 95, 70, 85, 82, 91],
    "英语": [78, 88, 90, 66, 85, 92, 75, 86],
}
df = pd.DataFrame(data)

# 第2步：数据查看
print(df.head())
print(df.info())

# 第3步：新增"总分"和"平均分"列
df["总分"] = df["语文"] + df["数学"] + df["英语"]
df["平均分"] = df[["语文", "数学", "英语"]].mean(axis=1).round(1)

# 第4步：描述统计
print(df.describe())

# 第5步：班级平均分对比（groupby 灵魂操作）
class_avg = df.groupby("班级")["总分"].mean()
print(class_avg)

# 第6步：最高分学生
top_student = df.sort_values("总分", ascending=False).head(1)
print(f"最高分：{top_student['姓名'].values[0]}，{top_student['总分'].values[0]}分")

# 第7步：可视化
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)                      # 1行3列第1个
class_avg.plot(kind="bar")
plt.title("各班总分平均")
plt.ylabel("平均分")

plt.subplot(1, 3, 2)
df.plot(x="姓名", y="总分", kind="bar", ax=plt.gca(), legend=False)
plt.title("各学生总分")
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
plt.scatter(df["语文"], df["数学"])
plt.xlabel("语文成绩")
plt.ylabel("数学成绩")
plt.title("语数成绩散点")

plt.tight_layout()
plt.savefig("成绩分析报告.png", dpi=150)
plt.show()

# 第8步：导出结果
df.to_csv("成绩分析结果.csv", index=False, encoding="utf-8-sig")
print("分析完成，结果已保存")
```

> **读代码练习**：运行后，按流程复述："读数据 → 加列 → 统计 → 分组 → 排序 → 画图 → 导出"。**这就是所有数据分析项目的骨架**，第3周机器学习的数据预处理也是这套流程。

---

## 六、读代码速查卡（本课精华）

| 你想看什么 | 用哪个 |
|------------|--------|
| 数据长什么样 | `df.head()` / `df.info()` |
| 选一列 | `df["列名"]` |
| 筛选行 | `df[df["列"] > 值]` |
| 按位置选 | `df.iloc[行, 列]` |
| 按标签选 | `df.loc[条件, "列"]` |
| 分组统计 | `df.groupby("列")["值列"].mean()` |
| 排序 | `df.sort_values("列", ascending=False)` |
| 缺失值 | `df.dropna()` / `df.fillna(值)` |
| 数值数组运算 | NumPy（`np.array` 直接 `+ - * /`） |
| 画折线/柱状/饼图 | `plt.plot/bar/pie/scatter` |
| 保存图 | `plt.savefig("图.png", dpi=150)` |

---

## 七、课后作业

1. **销售数据分析**：构造或下载一份含"日期/地区/产品/销售额"的 CSV，完成：按地区分组求总销售额 → 画柱状图 → 输出 Top3 地区。（AI 辅助生成数据 + 代码，但必须理解每步）
2. **读代码题**：向 AI 要一段"真实项目风格"的数据分析代码（包含 read_csv、groupby、plot），用"读代码速查卡"逐行解释。
3. **自选小项目（三选一）**：
   - 图书销量排行榜（读 JSON + Pandas + 柱状图）
   - 天气数据分析（温度折线图 + 平均值）
   - 班级成绩对比分析（两个班级的分布直方图）

---

## 八、FAQ

**Q1：NumPy、Pandas 装不上 / 很慢？**
用清华镜像：`pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple`；或直接装 Anaconda（自带全部）。

**Q2：CSV 读出来是乱码？**
读文件时指定 `encoding`：先试 `utf-8-sig`，不行试 `gbk`。写文件用 `encoding="utf-8-sig"`（Excel 才能正常打开）。

**Q3：画图中文是方块？**
执行 `plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]` 和 `plt.rcParams["axes.unicode_minus"] = False`。

**Q4：`df["成绩"]` 和 `df.成绩` 有什么区别？**
没本质区别（后者是简写）。但列名含空格或特殊字符时只能用 `df["成绩"]`。

**Q5：`iloc` 和 `loc` 分不清？**
- `iloc` = position（位置），用数字
- `loc` = label（标签），用名字/条件
- 记：**i-loc：i 像 1（数字）**。

**Q6：为什么 groupby 后直接 print 看不到全部？**
`groupby(...)` 只是"分组"，必须接聚合（`mean/sum/max/count`）才有结果。**groupby 本身不计算**——这是新手最常见的误区。

**Q7：我只想"读代码"，数据分析要练到什么程度？**
能看懂流程即可。重点认识：`df["列"]`、`df[条件]`、`df.groupby().mean()`、`plt.plot/bar` 这四个核心模式——它们覆盖了 90% 的数据分析代码。

> **KB 结束。下一课预告：课3 综合实战——用前面 2 堂课学到的所有知识，读真正的项目代码（前后端 + Agent）。**
