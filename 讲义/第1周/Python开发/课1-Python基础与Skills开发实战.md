# 课1：Python 基础与 Skills 开发实战

> **课时**：2 小时（120 分钟）
> **定位**：第2周 Python 开发第 1 堂，也是**唯一一堂语法课**。把传统 3 堂语法课压缩为"读懂基本 Python 代码"所需的全部核心，后半堂实战开发一个 **Skills 技能包**（Python 代码讲解助手），用技能反哺阅读能力。
> **目标**：学完后，能**读懂**基本 Python 代码（变量/类型/条件/循环/列表/字典/函数/类），并能亲手编写一个可用的 Skill。
> **前置**：第1周 AI 办公自动化（会用 AI、了解 Skills 概念）。
> **核心心法**：本课不要求背语法、不要求熟练写——**要求"看到认识、不懂会问、能猜会验"**。

---

## 一、导入：这堂课学什么（8 分钟）

### 1.1 教学目标：不是"会写"，而是"能读"

```
为什么 Python 代码到处都是？
- 后端开发（FastAPI/Django/Flask）、AI Agent 框架（LangChain/CrewAI）
- 数据分析/机器学习（第3周）、爬虫、自动化脚本

本课目标 = 看到一段 Python 代码，能大致说出：
① 这段代码在干什么？  ② 数据从哪来、到哪去？
③ 哪里是核心逻辑？    ④ 想改一个功能，该改哪里？
```

> **记住**：**读代码 ≠ 写代码**。读代码需要的知识大约是写代码的 30%——你只需要认识"积木"是什么、有什么用，不需要亲手搭。真正的"写"，交给 AI（第1周已学会）。

### 1.2 时间分配总览

| 时间段 | 内容 | 分钟 |
|--------|------|------|
| 一 | 导入与本课目标 | 8 |
| 二 | 环境准备 + Hello World | 10 |
| 三 | 语法快览一：变量 / 类型 / 条件 | 20 |
| 四 | 语法快览二：循环 / 列表 / 字典 | 20 |
| 五 | 函数与模块：项目的"积木" | 15 |
| 六 | 面向对象：看懂"类" | 15 |
| 七 | **Skills 开发实战**（本堂重点） | 30 |
| 八 | 总结 / 作业 / FAQ | 2 |

### 1.3 本课的"读代码三步法"（贯穿全课）

```
看到一行代码 → ① 用"大白话翻译"（它是干什么的）
              → ② 猜输出（这段代码跑完会得到什么）
              → ③ 问 AI 验证（复制给 AI："这段代码输出什么？"）
```

---

## 二、环境准备 + Hello World（10 分钟）

### 2.1 三种跑 Python 的方式（选一种即可）

```
方式A：VS Code + Python（推荐，第1周已装 VS Code）
  扩展安装：Python（微软官方）→ 新建 01.py → 点右上角 ▶ 运行

方式B：在线环境（免安装，急用时用）
  https://www.online-python.com 或 https://pythontutor.com（可看逐步执行动画）

方式C：Python 官方 IDLE（装 Python 时自带）
```

### 2.2 第一段代码：Hello World

```python
print("你好，Python！")   # 在屏幕上显示文字
print(1 + 2)              # 算数也能直接算
```

- `print(...)` = "把括号里的东西显示到屏幕"——**项目里 90% 的调试输出都靠它**
- `#` 开头是**注释**，给人看的，程序会忽略

### 2.3 两个"读代码"立即上手

```python
# 例1：猜输出——下面会打印什么？
name = "小明"
print("你好，" + name)
```

```python
# 例2：读报错——运行报错不可怕，看最后一行：
# NameError: name 'name' is not defined
# → 意思是：有个名字没定义。拼写错了？没赋值？
```

> **经验**：读报错 = 看**最后一行** + 看**箭头指的行**。这是每个 Python 开发者的日常。

---

## 三、语法快览一：变量、类型、条件（20 分钟）

### 3.1 变量：给数据起个名字

```python
age = 20          # 整数 int
price = 9.9       # 小数 float
name = "张三"     # 文本 str（字符串）
is_student = True # 布尔 bool（只有 True/False）
nothing = None    # 空值 None（"还没值"）
```

**读代码要点**：
- 看到 `名字 = 值` → 这就是"变量"，在存数据
- **Python 不用写类型**（不像 Java 的 `int age`）——类型靠值判断
- 类型决定它能干什么：数字能算、字符串能拼接、布尔能做判断

### 3.2 类型转换与 f-string（项目里高频出现）

```python
# 类型转换：字符串数字 → 数字（input 拿到的都是字符串）
num = int("20")          # "20" → 20
price = float("9.9")     # "9.9" → 9.9
text = str(20)           # 20 → "20"

# f-string：把变量"塞"进字符串里（现代 Python 最常用写法）
name = "张三"
score = 95
print(f"{name}考了{score}分")   # f 开头，{变量} 自动替换
# 输出：张三考了95分
```

> **看到 `f"..."` 就认识**：里面的 `{变量}` 会被替换成值。**AI 生成的后端/Agent 代码里到处是它**。

### 3.3 条件判断：让代码"做选择"

```python
score = 75
if score >= 60:              # 如果...就
    print("及格了")
elif score >= 90:            # 否则如果...
    print("优秀")
else:                        # 否则...
    print("不及格")
```

**读代码三要素**：
- `if / elif / else` = 条件分支，代码执行哪条取决于条件成立与否
- `>=` `<=` `==` `!=` = 比较符号（**注意：判断相等是两个 `=`**）
- `:` 冒号 + 下面**缩进**的代码 = "这个分支的代码块"

**缩进是 Python 的灵魂**：看到同一缩进的代码就是一个"块"。`if` 下面缩进的 4 格代码，条件成立才会执行。

**实操 1（2 分钟）**：猜输出
```python
x = 10
if x > 5:
    print("大")
else:
    print("小")
# 输出：？
```

---

## 四、语法快览二：循环、列表、字典（20 分钟）

### 4.1 列表 list：一串数据的"排队"

```python
students = ["小明", "小红", "小刚"]
print(students[0])     # 小明（注意：从 0 开始数）
print(students[-1])    # 小刚（负数 = 从后往前）
students.append("小丽") # 末尾加一个
print(len(students))   # 4（有几个元素）
```

> **比喻**：列表 = 排队。`[0]` 是第一个人（从 0 开始），`[-1]` 是最后一个人，`append` = 排到队尾，`len` = 数数有几个人。

### 4.2 for 循环：逐个处理列表里的每个元素

```python
# 给每个学生加一句问候
for name in students:
    print(f"你好，{name}")
```

```
读法：for 每个 名字 in 列表：逐个取出来，执行下面缩进的代码
```

### 4.3 列表推导式（项目代码里最常见的"压缩写法"）

```python
scores = [60, 80, 95, 55]
passed = [s for s in scores if s >= 60]   # 挑出及格的
# 等价于：passed = []
#         for s in scores:
#             if s >= 60: passed.append(s)
```

> **看到 `[x for x in ... if ...]` 就认识**：这是"遍历+筛选+生成新列表"的快捷写法。**AI 生成的代码极爱用它**，认出来 = 胜利。

### 4.4 字典 dict：名片夹 / 小档案

```python
person = {
    "name": "张三",
    "age": 20,
    "major": "计算机"
}
print(person["name"])       # 张三（按"名字"取"值"）
person["city"] = "北京"     # 加一条
print(person.keys())        # 所有键（名片上的标题）
print(person.values())      # 所有值
```

> **比喻**：字典 = 名片夹。`{"标题": 内容}`，用 `["标题"]` 取内容。
> **读代码关键**：JSON 数据（API 接口返回）几乎就是字典！看到 `data["name"]`、`config["host"]` 这类，就是"从数据里取一个字段"。

### 4.5 组合拳：遍历字典列表（后端/Agent 项目日常）

```python
users = [
    {"name": "张三", "score": 95},
    {"name": "李四", "score": 78},
]
for u in users:
    print(f"{u['name']}: {u['score']}分")
```

> **这是最重要的一个模式**：**列表里装字典** = 一表格的数据。后端返回的"用户列表"、"订单列表"都是这个形状。

**实操 2（3 分钟）**：猜输出
```python
nums = [1, 2, 3, 4, 5]
total = 0
for n in nums:
    total = total + n
print(total)
# 输出：？
```

---

## 五、函数与模块：项目的"积木"（15 分钟）

### 5.1 函数 def：把一段逻辑封装起来，反复调用

```python
def add(a, b):      # 定义函数：名字 add，两个输入 a、b
    return a + b    # 返回结果

result = add(3, 5)  # 调用：把 3、5 传进去
print(result)       # 8
```

**读代码要点**：
- 看到 `def 名字(参数):` → "定义一个函数"，下面是它的功能
- 看到 `名字(...)` → "调用函数"，括号里是喂给它的数据
- `return` = 把结果送出来；**函数里不写 return 就返回 None**
- **看到函数，先别读内部实现，先看名字猜用途**：`send_email()` 是发邮件，`get_user()` 是拿用户

### 5.2 参数的花样（AI 生成的代码里常见）

```python
def greet(name, greeting="你好"):   # 默认参数：不传就用"你好"
    print(f"{greeting}，{name}")

greet("张三")               # 你好，张三
greet("张三", "早上好")     # 早上好，张三

def add(*args):            # *args = 任意多个参数
    return sum(args)

def show(**kwargs):        # **kwargs = 任意多个"名字=值"
    for k, v in kwargs.items():
        print(k, v)
```

> **认识即可**：`*args`/`**kwargs` 在框架代码里到处都是（FastAPI、Agent 框架），意思是"这里参数个数不确定"。看到它，知道"灵活收参数"就够了。

### 5.3 模块与 import：用别人写好的积木

```python
import math                # 导入整个模块
import os                  # 文件/系统操作（爬虫、后端必用）
import json                # JSON 数据解析（前后端通信格式）
from datetime import datetime  # 从模块里导入一个功能

print(math.sqrt(16))       # 4.0
print(datetime.now())      # 当前时间
```

**读代码要点**：
- 文件**开头那一堆 import** = "这个项目用了哪些积木（库）"
- 认识常用库名，就能猜项目是干什么的：
  - `flask`/`fastapi`/`django` → Web 后端
  - `requests` → 发 HTTP 请求（爬虫、调 API）
  - `numpy`/`pandas`/`matplotlib` → 数据分析
  - `openai`/`langchain`/`crewai` → AI/Agent
  - `os`/`json`/`time` → 基础工具

### 5.4 pip：安装积木

```
pip install 库名          # 安装
pip install pandas numpy  # 一次装多个
pip list                  # 看装了哪些
```

> **读项目第一步**：看 `requirements.txt`——里面列了这个项目要装的所有库。装不上 = 缺库；看不懂库 = 问 AI"这个库是干什么的"。

---

## 六、面向对象：看懂"类"（15 分钟）

### 6.1 为什么必须认识"类"？

```
前端/后端框架（FastAPI/Django）、Agent 框架（LangChain/CrewAI）、
几乎所有现代 Python 项目 → 代码几乎全是"类"
不认识类 = 看不懂 80% 的项目代码
但认识类 ≠ 会设计类——本课只教"看到类怎么读"
```

> **比喻**：类 = 图纸，对象 = 按图纸造出来的实物。
> - `class 汽车:` 是图纸；`my_car = 汽车()` 是造出一辆车
> - 图纸上写的"属性"（颜色、速度）= 每辆车都有的数据
> - 图纸上写的"方法"（加速、刹车）= 每辆车都会的动作

### 6.2 类的标准长相（认识这四个部分）

```python
class Student:
    def __init__(self, name, score):   # ① 构造函数：造人的时候执行
        self.name = name               # ② self.xxx = 每个人自己的数据
        self.score = score

    def say_hello(self):               # ③ 方法：这个人会做的事
        print(f"我是{self.name}")

s = Student("张三", 95)    # ④ 创建对象（自动调用 __init__）
s.say_hello()              # 我是张三
```

**读代码四看**：
```
一看 class 名字 → 这是什么"物种"（Student=学生）
二看 __init__   → 造对象时要传哪些参数（name, score）
三看 self.xxx   → 对象有哪些数据（属性）
四看 def 方法   → 对象会做哪些事（行为）
```

> **`self` = 对象自己**。看到 `self.name` 就翻译成"这个对象自己的 name"。**`__init__` 是 Python 里最重要的函数**，看到它就找到了类的"出生证明"。

### 6.3 继承：新图纸抄旧图纸

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print("...")

class Dog(Animal):            # Dog 继承 Animal：拥有 Animal 的一切
    def speak(self):          # 重写：狗有自己的叫法
        print(f"{self.name}汪汪！")

d = Dog("旺财")
d.speak()                     # 旺财汪汪！
```

- `class Dog(Animal)` → "Dog 继承了 Animal"（括号里的就是父类）
- **读框架代码关键**：`class 我的Agent(BaseAgent)` = 我的 Agent 继承框架现成的 BaseAgent，只需改一小部分
- 看到 `super().__init__(...)` → 调父类的构造（先让老爸把基础建好）

**`super().__init__(...)` 到底怎么用？** 当子类要新增自己的属性时，必须先用 `super().__init__(...)` 把父类需要的参数交回去，再补自己的：

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):   # 子类多了个"品种"属性
        super().__init__(name)         # ① 先把 name 交给父类构造（老爸建好 name）
        self.breed = breed             # ② 再补上自己独有的属性

d = Dog("旺财", "柯基")
print(d.name, d.breed)                 # 旺财 柯基
```

**读框架代码时这样对照**（看一遍就懂）：

```python
class 我的Agent(BaseAgent):
    def __init__(self):
        super().__init__(name="我的助手")  # 先完成框架要求的初始化（必须做）
        self.temperature = 0.7             # 再设置我自己的参数
```

> **一句话记忆**：`super().__init__(...)` = "先把父类该做的事做完，再干我自己的事"。看到它就往上找父类的 `__init__`，看它需要哪些参数。

### 6.4 装饰器 @：给函数"贴标签"（Agent/框架代码核心）

```python
@app.get("/")          # FastAPI：把函数变成"网页接口"
def home():
    return "Hello"

@tool                 # Agent框架：把函数变成"AI可调用的工具"
def search(q):
    return "结果"
```

> **看到 `@开头` 的符号**：是"装饰器"——给下面那个函数**加功能/打标签**，函数本身不用改。**前端后端接口、Agent 工具、框架扩展全靠它**。记住"看到 @ = 下面是个被加工过的函数"即可。

### 6.5 类型注解（认识即可，不用会写）

```python
def add(a: int, b: int) -> int:   # 提示：a、b 是整数，返回整数
    return a + b
```

> `a: int`、`-> int` 只是"提示"，不强制。**读代码时它帮你猜参数类型**，很好用。

**实操 3（2 分钟）**：读下面的类，回答三个问题
```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def to_dict(self):
        return {"title": self.title, "author": self.author}
```
① 造一本书需要传什么？② 这本书有哪些数据？③ `to_dict()` 干什么用？
（答案：① title、author；② 书名、作者；③ 把书变成字典，方便转成 JSON 返回给前端——**这是 Flask/Django 项目里最常见的类**）

### 6.6 对象与对象：它们怎么"互相配合"（综合实例）

前面都是"一个对象自己玩"，真实项目里是**一堆对象互相调用**。看这个"学生选课"的例子，重点看对象之间怎么传、怎么调：

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []              # 这个学生选了哪些课（存的是课程对象）

    def enroll(self, course):          # ① 学生"选课"：收到一个课程对象
        self.courses.append(course)    # ② 学生记下这门课
        course.add_student(self)       # ③ 反向通知课程：把"自己"加进课程名单

class Course:
    def __init__(self, title):
        self.title = title
        self.students = []             # 这门课有哪些学生（存的是学生对象）

    def add_student(self, student):
        self.students.append(student)

# 造对象
s1 = Student("张三")
s2 = Student("李四")
c = Course("Python基础")

# 对象之间的交互
s1.enroll(c)                          # 张三选了 Python基础
s2.enroll(c)                          # 李四也选了 Python基础

print(c.students[0].name)             # 张三（课程的名单里有张三）
print(s1.courses[0].title)            # Python基础（张三的选课里有这门课）
```

**看懂交互的三条线**（这是读框架代码的核心）：
```
① 对象当参数传：s1.enroll(c) → 把"课程对象 c"传给"学生对象 s1"
② 对象里存对象：self.courses = [课程对象] → 一个对象持有另一个对象的引用
③ 方法里回调对方：course.add_student(self) → s1 的方法里，调用了 c 的方法
```

> **映射到框架**：Agent 调用工具、服务之间互相调用、订单里挂着一堆商品——本质上都是**对象持有对象、对象调用对象**。看到 `a.b(c)` 就是"A 对象在调用 B 对象（c）"。

### 6.7 前后端交互 + 调用远程 API（项目怎么"联网"）

前面都在"单机"里跑，真实项目里**前端和后端要对话、还要调别人家的远程服务**。看两组代码，本质都是"发数据 → 收数据"。

**第一组：前后端交互（后端 FastAPI + 前端页面）**

后端（Python，用 FastAPI 框架）：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()                    # ① 创建后端应用对象（app 就是个对象）

class Student(BaseModel):          # ② 用"类"定义接口要接收的数据格式
    name: str                      # 类型注解：name 必须是字符串
    score: int                     # score 必须是整数

@app.post("/student")              # ③ 装饰器：把函数变成"网页接口"（URL=/student）
def add_student(s: Student):       # ④ FastAPI 自动把前端发来的 JSON 转成 Student 对象
    return {"msg": f"收到 {s.name}，分数 {s.score}"}   # ⑤ 返回 JSON 给前端
```

前端（HTML + JavaScript，浏览器里跑）：

```html
<!-- 一个简单表单：两个输入框 + 一个按钮 -->
<input id="name" placeholder="姓名">
<input id="score" placeholder="分数">
<button onclick="send()">提交</button>

<script>
async function send() {
    // ① 从输入框取出用户填的内容，拼成一个对象
    let data = {
        name: document.getElementById("name").value,
        score: Number(document.getElementById("score").value)
    };

    // ② fetch：浏览器自带的"发请求"函数，请求后端的 /student
    let res = await fetch("/student", {
        method: "POST",                            // 用 POST 方式发送
        headers: {"Content-Type": "application/json"},  // 声明：我发的是 JSON
        body: JSON.stringify(data)                 // 把 JS 对象转成 JSON 字符串
    });

    // ③ 拿到后端返回的结果，转成对象后打印
    let result = await res.json();
    console.log(result.msg);      // 打印："收到 张三，分数 95"
}
</script>
```

> **交互流程**：前端填表 → `fetch` 发 JSON → 后端 FastAPI 收到 → 自动转成 `Student` 对象 → 返回 JSON → 前端打印。**记住：前端发 JSON，后端收 JSON、转对象、再回 JSON**，这就是"前后端交互"。

**第二组：调用远程 API 服务（Python 用 requests 库）**

```python
import requests                        # ① requests：Python 最常用的"发 HTTP 请求"库

url = "https://api.example.com/v1/chat"   # ② 远程服务的网址（别人的服务器）
api_key = "sk-xxxxxxxx"                   # ③ 身份凭证（密钥，别泄露）

# ④ 要发给对方的数据（请求体，通常是字典）
payload = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "用一句话介绍 Python"}]
}

# ⑤ 发请求：密钥放请求头里认证，数据自动序列化成 JSON
resp = requests.post(
    url,
    headers={"Authorization": f"Bearer {api_key}"},  # 认证：Bearer + 密钥
    json=payload                                     # json= 自动把字典转成 JSON
)

# ⑥ 解析返回结果：把 JSON 字符串转成 Python 字典
data = resp.json()
print(data["choices"][0]["message"]["content"])   # 取出 AI 的回答
```

**读这类代码的三个关键点**：
```
① url + headers + json = 三个核心参数：发到哪、带什么凭证、发什么数据
② 看到 headers 里的 Authorization / Bearer → 就是"带密钥认证"，几乎所有远程 API 都这样
③ resp.json() → 把对方返回的 JSON 字符串转成字典，然后按 key 一层层取
```

> **一句话总结**：前后端交互是"前端 ↔ 后端"，调远程 API 是"你的代码 ↔ 别人的服务器"，**本质完全一样——发 JSON、收 JSON**。区别只是"发给谁"。

---

## 七、Skills 开发实战（30 分钟）⭐本堂重点

### 7.1 Skills 是什么（快速回顾，2 分钟）

```
Skills（技能包）= 给 AI 的"岗位说明书"包
├── SKILL.md  ← 说明书：教 AI 怎么完成一类任务
└── (可选) 辅助文件：脚本、模板、数据

放哪里？
  项目级：.claude/skills/<技能名>/SKILL.md   （跟着项目走，推荐先用这个）
  个人级：~/.claude/skills/<技能名>/SKILL.md （所有项目都能用）
  CodeBuddy 对应：.codebuddy/skills/ 或 ~/.codebuddy/skills/
```

> 第1周已经学过 Skills 概念（KB8）。**本课是第一次"从零开发一个真正能用的 Skill"**——而且我们用刚学的 Python 来当助手。

### 7.2 实战任务：开发"Python 代码讲解助手"Skill（25 分钟）

**任务**：做一个 Skill，让 AI 用固定格式讲解 Python 代码——正好把本课的"读代码三步法"固化下来，以后你贴任何代码给 AI，它都会按标准流程讲给你听。

#### 步骤 1：创建技能目录（1 分钟）

```
在项目文件夹里创建：
.claude/skills/python-code-reader/SKILL.md
```

#### 步骤 2：写 SKILL.md（15 分钟，跟着写）

```markdown
---
name: python-code-reader
description: 用大白话讲解 Python 代码。当用户粘贴 Python 代码、问"这段代码干什么/怎么运行/哪里看不懂"时使用。
---

# Python 代码讲解助手

## 你负责的任务
把用户给的 Python 代码，按固定流程讲清楚，目标是让零基础的人听懂。

## 执行步骤（必须按顺序）

### 第1步：一句话概括
用不超过 30 个字，说明这段代码整体在干什么。
示例："这段代码在统计学生成绩，输出及格名单。"

### 第2步：拆块讲解
按逻辑块讲解，每块用这个格式：
- 【代码】贴出原代码
- 【干什么】大白话解释
- 【关键词】标注出现的语法点（变量/列表/字典/函数/类/装饰器等），
  每个语法点用一句话说明含义

### 第3步：数据流
用箭头说明数据从哪里来、怎么被处理、到哪里去。
示例：
输入学生名单 → for循环逐个判断分数 → 及格者加入新列表 → 打印

### 第4步：猜输出
在代码后写出："这段代码运行后会输出：..."并给出结果。

### 第5步：常见坑
如果有，用 1-2 句提示新手容易错的地方
（如索引从 0 开始、== 才是判断相等、缩进错误等）。

## 示例对话
用户：def add(a, b): return a + b
助手：
- 【干什么】定义一个加法函数：输入两个数，返回它们的和
- 【关键词】def=定义函数；return=返回结果
- 【数据流】a、b → 相加 → 返回给调用者
- 【猜输出】print(add(3, 4)) → 7
```

> **写 SKILL.md 的黄金法则**：`description` 写清楚"什么情况下用"（让 AI 自动触发）；`执行步骤` 写清楚"先做什么后做什么"（让 AI 有章法）；`示例对话` 给 AI 打样。

#### 步骤 3（加分项）：写一个 Python 辅助脚本（5 分钟）

在 `.claude/skills/python-code-reader/` 下新建 `analyze.py`——用今天学的知识统计一段代码：

```python
# analyze.py —— 统计一段 Python 代码的基本信息
import sys

def analyze(code):
    lines = code.split("\n")
    non_empty = [l for l in lines if l.strip()]        # 去掉空行
    funcs = [l for l in non_empty if l.strip().startswith("def ")]
    classes = [l for l in non_empty if l.strip().startswith("class ")]

    print("代码总行数:", len(lines))
    print("非空行数:", len(non_empty))
    print("函数数量:", len(funcs))
    print("类数量:", len(classes))
    for f in funcs:
        print("  函数:", f.strip().split("(")[0].replace("def ", ""))

if __name__ == "__main__":
    code = sys.stdin.read()     # 读取传入的代码
    analyze(code)
```

在 SKILL.md 的执行步骤里加一句："**先运行 `python analyze.py` 传入用户代码，把统计结果作为讲解开头**"——这样 Skill 就真的"会干活"了，而不只是让 AI 动嘴。

> **这就是真实 Skills 的结构**：`SKILL.md`（让 AI 知道怎么用）+ 辅助脚本（真正干活的工具）。LangChain、CrewAI 里的工具函数也是这个思路。

#### 步骤 4：测试 Skill（4 分钟）

1. 在项目里写一段你今天的练习题代码（如 4.5 的组合拳）
2. 对 AI 说："帮我看看这段代码是干什么的" + 粘贴代码
3. 如果 AI 用了 `python-code-reader` 的格式讲解 → **成功！**
4. 没触发？检查 `description` 是否写清了使用场景，或手动对 AI 说"使用 python-code-reader 技能"

### 7.3 验收标准（1 分钟）

```
✅ SKILL.md 放在 .claude/skills/python-code-reader/ 下
✅ description 清楚说明"什么场景用"
✅ 执行步骤 >= 4 步，且包含"猜输出"
✅ 有一个示例对话
✅ （加分）analyze.py 能运行并输出统计
```

### 7.4 Skills 开发的三条心法

```
① 从自己的痛点出发：你最常让 AI 干什么？把它做成 Skill
② description 是灵魂：写不清"什么时候用"，AI 就不会主动用
③ 先小后大：先做一个 10 行的 Skill，跑通流程再慢慢加功能
```

> **教学提示**：本堂的 Skill 是"样板"。课后让学员为自己最常用的一件事各写一个 Skill（如"读论文""写周报""改简历"），第2周结束时进行小组分享。

---

## 八、总结、作业与 FAQ（2 分钟）

### 8.1 本课知识地图（一张图记住）

```
读 Python 代码所需的一切：
词汇表  变量 = 存数据；列表 = 排队；字典 = 名片夹
流程    条件 if/else（做选择）；循环 for（逐个处理）
积木    函数 def（封装逻辑）；import（用现成库）
骨架    类 class（图纸）+ self + __init__ + 继承 + @装饰器
武器    Skills：把"读代码三步法"做成 AI 技能包
```

### 8.2 课后作业

1. **读代码练习**：把本课 4 个实操的代码，每段用"三步法"（翻译 → 猜输出 → 验证）过一遍。
2. **Skills 实战（核心作业）**：完善 `python-code-reader` 技能包，再仿照它为自己写 1 个新 Skill（题材自选：论文阅读/周报生成/简历修改均可），写好 `description` 和至少 3 步执行步骤。
3. **预习**：找一段真实项目代码（GitHub 搜索 `flask` 或 `fastapi` 小项目），下课前带过来——课3 要用它实战阅读。

### 8.3 FAQ

**Q1：两个小时的语法会不会太少？**
不会。本课目标是"读懂"，不是"熟练写"。真正的写法、排错、性能优化，未来在实践中遇到再学。**读代码需要的语法量，2 小时足够覆盖 90%**。

**Q2：我连 `self` 都还没完全懂，能继续吗？**
完全能。`self` 只需要记住"对象自己"这一个理解就够读了。剩下的一边读项目一边自然就懂了。

**Q3：Skills 和第1周学的有什么区别？**
第1周是"会用现成 Skills"（装别人的技能包）；本课是**第一次自己写**——把重复性提问固化成一个技能，这是"AI 协作开发者"的核心能力。

**Q4：为什么把 3 堂语法课压成 1 堂？**
因为课程目标是"能读懂基本代码"。细节（异常处理、文件读写、模块深入）放到课2 数据分析、课3 项目实战里"遇到再学"——**项目是最好的老师**，比单独学语法高效得多。

**Q5：我写 analyze.py 时卡住了怎么办？**
三步：① 对照 7.2 步骤3 抄一遍；② 看不懂的复制给 AI："帮我解释这段代码"；③ 报错了就把报错信息发给 AI。**这不是作弊——是这门课教你的核心工作方式**。

---

## 九、Python 数据分析（NumPy / Pandas / Matplotlib）—— 延伸章节

> 本章由原"课2：Python 数据分析"合并而来。学完前面的语法基础后，这里用数据分析三件套 NumPy / Pandas / Matplotlib，读懂"读取数据 → 清洗 → 分析 → 可视化"的项目代码流程。
> **安装**：`pip install numpy pandas matplotlib`

### 9.1 为什么学数据分析

#### 9.1.1 Python 最大的应用场景之一

```
数据分析/机器学习 是 Python 的"主场"：
- 数据分析师 / 数据科学家：Python 第一语言
- 机器学习（后续课程）：数据处理阶段几乎全用 Pandas
- Agent 开发：工具函数经常要处理结构化数据（表格、CSV、JSON）
- 前端/后端项目：报表接口、数据统计、爬虫数据清洗
```

#### 9.1.2 三件套的分工

```
NumPy（Numerical Python）→ 多维数组 + 高效数值计算（底层引擎）
Pandas → 表格（DataFrame）+ 数据处理（读CSV/筛选/分组/聚合）
Matplotlib → 画图（折线/柱状/饼图/散点）
```

> **比喻**：
> - NumPy = 计算器（速度快，处理数字）
> - Pandas = Excel 高级版（表格 + 公式 + 透视表）
> - Matplotlib = 图表工具（把数据画成图）

#### 9.1.3 本章"读代码"目标

- 认识 `np.array`、`df`（DataFrame）、`plt` 三种对象的核心操作
- 能看懂"读 CSV → 筛选 → 分组 → 画图"的标准流程
- 学会中文乱码、CSV 乱码的解决方案

### 9.2 NumPy：高效数值计算

#### 9.2.1 数组创建

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

#### 9.2.2 数组属性与索引切片

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

#### 9.2.3 向量化运算（NumPy 的灵魂）

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

#### 9.2.4 统计函数（数据分析最常用）

```python
data = np.array([85, 92, 67, 88, 59, 76])

data.mean()           # 77.83...（平均值）
data.sum()            # 467
data.min()            # 59
data.max()            # 92
data.std()            # 标准差（数据波动程度）
np.median(data)       # 中位数
np.percentile(data, 75)   # 75%分位数
np.argmax(data)       # 3（最大值的索引）
np.argmin(data)       # 4（最小值的索引）
```

#### 9.2.5 布尔索引（条件筛选）

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

### 9.3 Pandas：表格数据处理

> Pandas 是数据分析的核心，几乎读任何"处理表格数据"的代码都会遇到它。**惯例导入 `import pandas as pd`**。

#### 9.3.1 两种核心结构

```python
import pandas as pd

# Series：一列数据（带索引的列表）
s = pd.Series([85, 92, 67], index=["张三", "李四", "王五"])
print(s)
# 张三    85
# 李四    92
# 王五    67
# dtype: int64

# DataFrame：二维表格（核心！）
data = {
    "姓名": ["张三", "李四", "王五"],
    "成绩": [85, 92, 67],
    "班级": ["1班", "2班", "1班"],
}
df = pd.DataFrame(data)
print(df)
#    姓名  成绩  班级
# 0  张三  85   1班
# 1  李四  92   2班
# 2  王五  67   1班
```

> **记忆**：`df` 是 DataFrame 的缩写（读代码最常见变量名）。Series 是一列，DataFrame 是多列组成的表格。

#### 9.3.2 从文件创建（数据分析的第一步）

```python
df = pd.read_csv("data.csv")              # 读 CSV（最常用）
df = pd.read_excel("data.xlsx")           # 读 Excel（需 pip install openpyxl）
df = pd.read_json("data.json")            # 读 JSON

# 常见参数（解决中文乱码）
df = pd.read_csv("data.csv", encoding="utf-8")      # 指定编码
df = pd.read_csv("data.csv", encoding="gbk")        # 中文 Windows 常见编码
```

> **读代码重点**：`pd.read_csv()` 是数据分析代码的"第一行"，几乎所有项目都以读文件开头。

#### 9.3.3 数据查看（读陌生数据的标准动作）

```python
df.head()           # 看前5行
df.head(10)         # 看前10行
df.tail()           # 看后5行
df.info()           # 每列的类型、缺失情况（读代码必看！）
df.describe()       # 数值列的统计（count/mean/std/min/max）
df.shape            # (行数, 列数)
df.columns          # 列名列表
df.dtypes           # 每列数据类型
```

> **读代码重点**：看到 `df.head()` / `df.info()` / `df.describe()`，说明作者在"探索数据、了解数据长什么样"——这是读陌生数据的标准三连。

#### 9.3.4 数据选择（读代码最高频操作）

```python
# ① 选一列（返回 Series）
df["成绩"]              # 按列名选
df.成绩                 # 点号也能选（列名不能有空格）

# ② 选多列（返回 DataFrame）
df[["姓名", "成绩"]]

# ③ 按行选：iloc（按位置）、loc（按标签/索引）
df.iloc[0]              # 第0行
df.iloc[1:3]            # 第1~2行
df.loc[0]               # 标签为0的行
df.loc[0, "成绩"]       # 第0行的"成绩"列

# ④ 条件筛选（最常用！返回满足条件的行）
df[df["成绩"] >= 90]    # 成绩>=90的行
```

#### 9.3.5 数据筛选与清洗

```python
# 多条件：用 &（与）、|（或），条件要加括号
df[(df["成绩"] >= 80) & (df["班级"] == "1班")]

# 处理缺失值
df.isnull()             # 哪些是空值（NaN）
df.isnull().sum()       # 每列缺失数量
df.dropna()             # 删除含空值的行
df.fillna(0)            # 空值填0
df.drop_duplicates()    # 去重

# 排序
df.sort_values("成绩")              # 按成绩升序
df.sort_values("成绩", ascending=False)  # 降序
```

#### 9.3.6 新增列与运算

```python
# 新增一列（直接赋值）
df["及格"] = df["成绩"] >= 60

# 对某列做运算
df["成绩加10"] = df["成绩"] + 10
df["平均分"] = df[["成绩"]].mean()

# apply：对某列逐元素应用函数
def 等级(score):
    return "优秀" if score >= 90 else "合格"

df["等级"] = df["成绩"].apply(等级)
```

#### 9.3.7 分组聚合（groupby，数据分析的灵魂操作）

```python
# 按班级分组，统计每班成绩平均分
df.groupby("班级")["成绩"].mean()
# 班级
# 1班    76.0
# 2班    92.0

# 一次算多个统计量
df.groupby("班级")["成绩"].agg(["mean", "max", "count"])

# 多列分组
df.groupby(["班级", "及格"])["成绩"].sum()
```

> **读代码重点**：`groupby("分组列")["统计列"].统计函数()` 是标准套路——"按某列分组，对另一列做统计"。**看到 groupby 就知道在做"分类汇总"**，类似 Excel 透视表。

#### 9.3.8 数据合并

```python
# 横向拼接：两个表按某列"对齐"合并（类似 SQL 的 JOIN）
df1 = pd.DataFrame({"姓名": ["张三", "李四"], "成绩": [85, 92]})
df2 = pd.DataFrame({"姓名": ["张三", "李四"], "班级": ["1班", "2班"]})
merged = pd.merge(df1, df2, on="姓名")

# 纵向拼接：上下堆叠
combined = pd.concat([df1, df2], axis=0)
```

### 9.4 Matplotlib：数据可视化

> **惯例导入 `import matplotlib.pyplot as plt`**（pyplot 是画图入口，几乎永远缩写成 plt）。

#### 9.4.1 基本绘图流程（固定五步）

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

#### 9.4.2 五种基础图（读代码识别）

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

#### 9.4.3 与 Pandas 联用（数据分析标准流程）

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

#### 9.4.4 中文显示解决方案（Windows 必备）

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

#### 9.4.5 子图布局（多图对比）

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1行2列
axes[0].plot([1, 2, 3], [3, 1, 4], title="左图")
axes[1].bar(["A", "B"], [5, 3], title="右图")
plt.tight_layout()
plt.show()
```

### 9.5 完整实战：学生成绩分析报告

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

### 9.6 读代码速查卡（本章精华）

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

### 9.7 课后作业

1. **销售数据分析**：构造或下载一份含"日期/地区/产品/销售额"的 CSV，完成：按地区分组求总销售额 → 画柱状图 → 输出 Top3 地区。（AI 辅助生成数据 + 代码，但必须理解每步）
2. **读代码题**：向 AI 要一段"真实项目风格"的数据分析代码（包含 read_csv、groupby、plot），用"读代码速查卡"逐行解释。
3. **自选小项目（三选一）**：
   - 图书销量排行榜（读 JSON + Pandas + 柱状图）
   - 天气数据分析（温度折线图 + 平均值）
   - 班级成绩对比分析（两个班级的分布直方图）

### 9.8 FAQ

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

---

> **KB 结束。下一课预告：课3 综合实战——用前面所学知识，读真正的项目代码（前后端 + Agent）。**
