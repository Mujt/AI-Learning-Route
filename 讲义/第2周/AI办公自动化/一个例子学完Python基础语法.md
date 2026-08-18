# 一个例子学完 Python 基础语法 —— 迷你待办清单

> **文档定位**：零基础语法教学辅助材料。用一个尽可能短的程序（约 90 行）覆盖 Python 全部基础语法——变量、数据类型、条件、循环、列表、字典、函数、类与对象、继承。适合第2周课程作为"语法总复习"或"期末串讲"的例子，也可直接发给学生自学。
>
> **设计思路**：与其学十个零散小例子，不如把所有语法装进**同一个贴近办公场景的程序**里——"待办清单管理"。它也是本课第六章"MCP 待办事项实战"的纯 Python 前置版本，学完即可无缝衔接。

---

## 目录

1. [完整程序](#一完整程序)
2. [运行效果](#二运行效果)
3. [语法覆盖对照表](#三语法覆盖对照表)
4. [按语法点讲解](#四按语法点讲解)
5. [课堂练习](#五课堂练习)
6. [可选扩展](#六可选扩展)

---

## 一、完整程序

将以下代码保存为 `todo_demo.py`，运行 `python todo_demo.py` 即可。

```python
"""todo_demo.py —— 一个例子学完 Python 基础语法（含面向对象）"""


class Task:
    """任务类：一条待办事项"""

    count = 0  # 类变量：所有任务共享，统计创建了多少条

    def __init__(self, name, minutes=30, done=False):
        Task.count += 1
        self.name = name        # 实例变量：每个任务自己的属性
        self.minutes = minutes
        self.done = done

    def finish(self):
        self.done = True

    def __str__(self):          # 定义 print() 时的显示格式
        mark = "[已完成]" if self.done else "[未完成]"
        return f"{mark} {self.name}（约{self.minutes}分钟）"


class UrgentTask(Task):
    """紧急任务类：继承自 Task，多了一个标记"""

    def __init__(self, name, minutes=30):
        super().__init__(name, minutes)   # 调用父类的构造方法
        self.urgent = True

    def __str__(self):
        return "【加急】" + super().__str__()


class TodoList:
    """待办清单类：管理多个任务"""

    def __init__(self, owner):
        self.owner = owner
        self.tasks = []                   # 列表：存放 Task 对象

    def add(self, task):
        self.tasks.append(task)

    def unfinished(self):
        result = []
        for t in self.tasks:              # for 循环遍历列表
            if not t.done:                # 条件判断
                result.append(t)
        return result

    def total_minutes(self):
        total = 0
        for t in self.unfinished():
            total += t.minutes
        return total

    def show(self):
        print(f"===== {self.owner} 的待办清单 =====")
        for i, t in enumerate(self.tasks, start=1):
            print(f"  {i}. {t}")
        rest = self.total_minutes()
        if rest > 120:
            print(f"  >> 共 {rest} 分钟，任务太重，建议分摊！")
        elif rest > 0:
            print(f"  >> 剩余工作量约 {rest} 分钟")
        else:
            print("  >> 全部完成，下班！")


def main():
    # ---- 变量与四种基本数据类型 ----
    name = "小明"          # 字符串 str
    age = 20               # 整数 int
    work_hours = 7.5       # 浮点数 float
    is_busy = True         # 布尔值 bool

    print(f"{name}，{age}岁，今天工作 {work_hours} 小时\n")

    # ---- 创建对象并加入清单 ----
    todo = TodoList(name)
    todo.add(Task("回复邮件", 15))
    todo.add(Task("写周报", minutes=45))       # 关键字参数
    todo.add(UrgentTask("准备下午会议"))
    todo.add(Task("取快递", 10, done=True))    # 默认参数 + 关键字参数

    todo.show()
    print(f"\n共创建了 {Task.count} 条任务")

    # ---- while 循环 + 字典：简易交互菜单 ----
    menu = {"1": "完成第一条任务", "2": "查看清单", "0": "退出"}
    while True:
        print("\n请选择操作：", menu)
        choice = input("> ")
        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            undone = todo.unfinished()
            if len(undone) == 0:
                print("没有未完成的任务了")
            else:
                undone[0].finish()
                print(f"已完成：{undone[0].name}")
        elif choice == "2":
            todo.show()
        else:
            print("输入无效，请重新输入")


if __name__ == "__main__":
    main()
```

---

## 二、运行效果

```
小明，20岁，今天工作 7.5 小时

===== 小明 的待办清单 =====
  1. [未完成] 回复邮件（约15分钟）
  2. [未完成] 写周报（约45分钟）
  3. 【加急】[未完成] 准备下午会议（约30分钟）
  4. [已完成] 取快递（约10分钟）
  >> 剩余工作量约 90 分钟

共创建了 4 条任务

请选择操作： {'1': '完成第一条任务', '2': '查看清单', '0': '退出'}
> 已完成：回复邮件

请选择操作： {'1': '完成第一条任务', '2': '查看清单', '0': '退出'}
> 再见！
```

---

## 三、语法覆盖对照表

教学时按此表逐行"点名"语法点，学生可直观看到**每个语法长在哪、为什么用**。

| 语法点 | 程序中的位置 | 一句话解释 |
|--------|--------------|------------|
| 变量 | `name = "小明"` | 给数据起名字，无需声明类型 |
| 字符串 str | `"回复邮件"` | 文本，用引号包裹 |
| 整数 int | `age = 20` | 不带小数点的数 |
| 浮点数 float | `work_hours = 7.5` | 带小数点的数 |
| 布尔 bool | `done=False` | 只有 True / False 两个值 |
| f-string 格式化 | `f"{name}，{age}岁"` | 把变量嵌入字符串的最简方式 |
| 三元表达式 | `"[已完成]" if self.done else "[未完成]"` | 单行版 if-else |
| 算术运算符 | `total += t.minutes` | 加减乘除，`+=` 是累加简写 |
| 比较运算符 | `rest > 120`、`len(undone) == 0` | 大于、等于等，结果是布尔值 |
| 逻辑运算符 | `not t.done` | not / and / or |
| if / elif / else | `show()` 和菜单部分 | 三分支条件判断 |
| for 循环 | `for t in self.tasks:` | 遍历列表，逐个处理 |
| enumerate | `for i, t in enumerate(...)` | 遍历时同时拿到序号 |
| while 循环 | `while True:` | 满足条件就一直重复（交互菜单） |
| break | `break` | 立即跳出循环 |
| 列表 list | `self.tasks = []`、`.append()` | 有序可改的容器，可存对象 |
| 索引访问 | `undone[0]` | 从0开始编号取元素 |
| 字典 dict | `menu = {"1": "完成任务", ...}` | 键值对容器，按键查值 |
| 函数定义 | `def unfinished(self):` | 封装一段可复用的逻辑 |
| 参数与返回值 | `def __init__(self, name, minutes=30)` | 位置参数、**默认参数** |
| 关键字参数 | `Task("写周报", minutes=45)` | 指名传参，更清晰 |
| 类定义 | `class Task:` | 自定义数据类型（对象的模板） |
| 类变量 vs 实例变量 | `count` vs `self.name` | 全类共享 vs 每个对象独有 |
| `__init__` 构造方法 | 创建对象时自动执行 | `Task("回复邮件")` 背后发生的事 |
| `self` | 每个方法的第一个参数 | "这个对象自己" |
| 魔法方法 `__str__` | `print(t)` 时的显示格式 | 让对象"会说话" |
| 继承 | `class UrgentTask(Task):` | 子类复用父类的属性和方法 |
| `super()` | `super().__init__(name, minutes)` | 调用父类的方法 |
| 方法调用 | `todo.add(...)`、`t.finish()` | 对象.方法() 的点语法 |
| 内置函数 | `print` / `input` / `len` / `enumerate` | Python 自带的工具 |
| 程序入口 | `if __name__ == "__main__":` | 直接运行才执行，被导入则不执行 |
| 注释 | `#` 和 `"""文档字符串"""` | 给人看的说明，机器忽略 |

---

## 四、按语法点讲解

### 4.1 变量与数据类型（main 函数开头）

```python
name = "小明"      # str   字符串
age = 20           # int   整数
work_hours = 7.5   # float 浮点数
is_busy = True     # bool  布尔值（True/False）
```

Python 不需要声明类型，赋什么值就是什么类型。用 `type(name)` 可以查看类型。

### 4.2 字符串与 f-string

```python
print(f"{name}，{age}岁，今天工作 {work_hours} 小时")
# 输出：小明，20岁，今天工作 7.5 小时
```

f-string（ formatted string）是**最推荐的格式化方式**：字符串前加 `f`，变量放进 `{}` 即可。字符串还支持 `+` 拼接（见 `UrgentTask.__str__`）。

### 4.3 条件语句

```python
if rest > 120:          # 第一个条件成立就走这里
    print("任务太重")
elif rest > 0:          # 否则再看第二个条件
    print(f"剩余 {rest} 分钟")
else:                   # 都不成立走这里
    print("全部完成")
```

注意冒号 `:` 和**四格缩进**——Python 用缩进表示代码块，这是它最显眼的语法特征。

### 4.4 循环

```python
for t in self.tasks:        # for：把列表里的东西挨个拿出来
    print(t)

while True:                 # while：条件为真就一直转（交互菜单）
    choice = input("> ")
    if choice == "0":
        break               # break：立即跳出循环
```

口诀：**知道循环几次用 for，不知道何时结束用 while**。

### 4.5 列表与字典

```python
self.tasks = []                    # 列表：有序、可增删改
self.tasks.append(task)            # 追加元素
undone[0]                          # 按下标取元素（从0开始）

menu = {"1": "完成任务", "0": "退出"}  # 字典：键 → 值
menu["0"]                          # 按键取值 → "退出"
```

关键认知：**列表里可以存任何东西，包括你自己定义的对象**——`TodoList.tasks` 里存的就是一个个 `Task` 对象，这是面向对象与容器结合的典型用法。

### 4.6 函数

```python
def __init__(self, name, minutes=30, done=False):  # minutes/done 是默认参数
    ...

Task("写周报", minutes=45)     # 关键字参数：指名道姓地传，顺序无关
Task("取快递", 10, done=True)  # 部分用位置、部分用关键字
```

函数三要素：**参数（输入）、函数体（处理）、返回值（输出，`return`）**。默认参数让调用更灵活——`Task("回邮件")` 不写分钟数也不会报错。

### 4.7 类与对象（核心）

三个类的分工像一家公司：

| 类 | 角色 | 说明 |
|----|------|------|
| `Task` | 员工 | 一条任务：有属性（name/minutes/done），有行为（finish） |
| `UrgentTask` | 加急员工 | **继承** Task 的一切，再加个"加急"标记 |
| `TodoList` | 部门经理 | 管理一队任务对象（增删查、统计） |

**对象 = 属性（数据） + 方法（行为）**。创建对象的瞬间 `__init__` 自动执行：

```python
t = Task("回复邮件", 15)   # 幕后：Task.count += 1，self.name="回复邮件"，...
t.finish()               # 调用方法：self.done = True
print(t)                 # 自动调用 __str__，输出定制格式
```

**类变量 vs 实例变量**（易混点）：

```python
Task.count   # 类变量：全类共享一份，统计总数（Task.count == 4）
self.name    # 实例变量：每个对象各自一份（"回复邮件" ≠ "写周报"）
```

### 4.8 继承

```python
class UrgentTask(Task):            # 括号里写父类
    def __init__(self, name, minutes=30):
        super().__init__(name, minutes)   # 先让父类完成基础初始化
        self.urgent = True                # 再加自己的特色

    def __str__(self):
        return "【加急】" + super().__str__()   # 复用并增强父类行为
```

继承的意义：**不重写一行代码就获得父类全部能力**，只写"差异部分"。`UrgentTask` 只加了 6 行代码，就同时拥有 `finish()`、`count` 统计等一切。

### 4.9 程序中未包含的三个小语法

为保持程序最简，元组、集合、import 用一分钟口头带过即可：

```python
# 元组 tuple：不可改的列表，适合固定搭配
steps = ("收件", "分类", "归档")     # steps[0] == "收件"，但不能 append

# 集合 set：自动去重
tags = {"工作", "工作", "生活"}      # 只剩 {"工作", "生活"}

# 导入模块：使用别人写好的功能
from datetime import datetime
print(datetime.now())                # 当前时间
```

---

## 五、课堂练习

由易到难，全部通过**修改这个程序**完成（不新开文件）：

1. **入门**：给 `main` 再加一条任务"整理桌面"（20分钟），运行观察输出变化。
2. **条件**：把 `show()` 中的阈值 120 改成 60，观察提示语何时变成"任务太重"。
3. **方法**：给 `TodoList` 添加 `remove(name)` 方法，按名字删除任务（提示：`self.tasks.remove(...)`）。
4. **类设计**：仿照 `UrgentTask`，写一个 `MeetingTask(Task)` 类，多一个 `room`（会议室）属性，`__str__` 中显示"[会议室 A301]"。
5. **挑战**：让菜单支持"3：查看未完成任务"，直接打印 `todo.unfinished()` 列表，观察输出的是不是对象地址——然后思考：为什么 `print(t)` 单独打印却是漂亮格式？（答案：`print(列表)` 会对每个元素调用 `repr` 而不是 `__str__`，可在 Task 中再定义 `__repr__ = __str__` 解决）

---

## 六、可选扩展

学有余力或需要衔接后续课程时，按需增加：

```python
# 1. 文件保存：清单写入本地（with 自动关闭文件）
with open("todo.txt", "w", encoding="utf-8") as f:
    for t in todo.tasks:
        f.write(f"{t.done}|{t.name}|{t.minutes}\n")

# 2. @property：把方法伪装成属性，调用时不用加括号
class Task:
    @property
    def status(self):
        return "已完成" if self.done else "未完成"

# t.status    → "未完成"（而不是 t.status()）
```

这两个扩展正好对应课程后续内容：**文件持久化**是第六章 MCP 待办实战中"数据存哪里"的前置知识，**@property** 是第2周 Python 课"装饰器"概念的实例。

---

> **衔接提示**：本例的 `Task` / `TodoList` 类可直接"搬"进第六章的 MCP 实战——把方法注册为 MCP 工具，就是一次"普通 Python 程序 → AI 可操作服务"的升级演示，前后呼应。
