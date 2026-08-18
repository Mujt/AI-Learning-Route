# Python 多线程编程入门 —— 从"事故现场"到面向对象并发

> **文档定位**：零基础并发编程教学辅助材料。延续《一个例子学完Python基础语法.md》的风格，用**办公场景 + 可运行的短程序**讲清三件事：多线程怎么写、互斥锁为什么必须、异步（asyncio）与多线程什么关系。核心是一个面向对象的多线程完整例子——"办公打印室模拟"（约 60 行，已实际运行验证）。
>
> **为什么现在学**：调用大模型 API 是典型的 I/O 等待场景（网络请求几秒钟），本课之后的"多平台 API 调用实战""MCP 服务"都要靠并发同时发多个请求提速。多线程是最容易入门的并发方式。

---

## 目录

1. [概念地图：串行、并发、并行](#一概念地图串行并发并行)
2. [事故现场：没有锁会发生什么](#二事故现场没有锁会发生什么)
3. [起步：创建线程的两种方式](#三起步创建线程的两种方式)
4. [核心示例：办公打印室（面向对象多线程）](#四核心示例办公打印室面向对象多线程)
5. [互斥工具箱速览](#五互斥工具箱速览)
6. [线程池：ThreadPoolExecutor](#六线程池threadpoolexecutor)
7. [异步编程：asyncio](#七异步编程asyncio)
8. [选型总结：线程、异步、进程](#八选型总结线程异步进程)
9. [课堂练习](#九课堂练习)

---

## 一、概念地图：串行、并发、并行

```
串行（一个员工，做完一件再做下一件）
  任务1 ──→ 任务2 ──→ 任务3        总时间 = 3 + 2 + 4 = 9 分钟

并发（一个员工，烧水时去切菜 —— 交替推进，不闲着）★ 单核CPU本质如此
  任务1 ████──█──█
  任务2    ████████                总时间 < 9 分钟
  任务3 ────────████

并行（三个员工，同时各做一件）★ 需要多核CPU
  任务1 ████
  任务2    ██                      总时间 = max(4,2,4) = 4 分钟
  任务3 ████
```

| 概念 | 一句话 |
|------|--------|
| **进程** | 一个运行中的程序，有自己的内存空间（如同时开两个 Excel） |
| **线程** | 进程内的执行流，共享同一份内存（如 Excel 里同时排序和打印） |
| **GIL** | Python 的全局解释器锁：**同一时刻只允许一个线程执行 Python 字节码** |
| **GIL 的后果** | 多线程**不能**加速纯计算；但 I/O 等待（网络/磁盘/睡眠）时会释放 GIL，**多线程对 I/O 场景非常有效** |

> 记住结论即可：**等得多用线程/异步，算得多用进程**。本文所有例子都是 I/O 场景（打印耗时、下载耗时）。

---

## 二、事故现场：没有锁会发生什么

多线程最大的坑：**共享变量被多个线程同时修改**。`counter += 1` 看似一步，实际是"读→改→写"三步，线程可能读到旧值后写回，覆盖别人的成果：

```python
import threading, time

counter = 0

def add_without_lock():
    global counter
    for _ in range(1000):
        tmp = counter        # 第1步：读
        time.sleep(0.0001)   # 放大竞争窗口（模拟读取后还要做点别的）
        counter = tmp + 1    # 第2步：写回（此时别的线程可能已经改过 counter）

threads = [threading.Thread(target=add_without_lock) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("期望 4000，实际 =", counter)
```

实际运行（每次结果不同）：

```
期望 4000，实际 = 1003     ← 4个线程各加1000次，近3/4的更新丢了！
```

**事故复盘**：4 个线程都读到 `counter=250`，各自 +1 后写回 251——四次加法只生效一次。这就是**竞态条件（Race Condition）**：结果取决于线程抢跑的运气。

**解法预告**：给"读改写"这段**临界区**上一把互斥锁（`threading.Lock`），同一时刻只放一个线程进来——见第四节。

---

## 三、起步：创建线程的两种方式

### 方式一：函数式（把函数交给线程）

```python
import threading, time

def say_hello(name):
    time.sleep(1)                       # 模拟耗时工作
    print(f"{name} 说：大家好")

t = threading.Thread(target=say_hello, args=("小明",))  # args 是元组，记得带逗号
t.start()                               # 启动线程（不等它做完）
print("主线程没等它，先打印了这句")
t.join()                                # join：主线程在这里等 t 结束
```

### 方式二：面向对象（继承 Thread，把线程本身写成类）★ 本文主推

```python
import threading, time

class Greeter(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)     # 复用父类初始化，顺便给线程起名

    def run(self):                      # ★ 关键：必须叫 run，start() 会自动调用它
        time.sleep(1)
        print(f"{self.name} 说：大家好")

g = Greeter("小明")
g.start()                               # 注意：写 g.run() 就变成普通调用（不开线程）！
g.join()
```

| 对比 | 函数式 | 继承 Thread |
|------|--------|-------------|
| 写法 | `Thread(target=函数)` | 类中重写 `run()` |
| 适合 | 一次性小任务 | **线程自带状态和多个方法，可复用、可扩展**（如打印室的 Worker） |
| 共同点 | 都用 `start()` 启动、`join()` 等待 | 同左 |

---

## 四、核心示例：办公打印室（面向对象多线程）

**场景**：3 个员工（线程）共用 1 台打印机（共享资源），从任务队列（`queue.Queue`）领活，收到停工信号（`Event`）后下班。程序把多线程四大件——**Thread 子类、Lock 互斥锁、Queue 安全队列、Event 事件**——全部装进一个 60 行的程序：

```python
import threading, queue, time


class Printer:
    """共享打印机（共享资源）：必须用锁保护"""

    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()   # 互斥锁：一把钥匙
        self.printed = 0               # 共享变量：统计打印总数

    def print_doc(self, worker, doc):
        with self.lock:                # 进入临界区：同一时刻只有一个线程能进来
            self.printed += 1          # 若无锁，多线程同时 += 会丢更新（见第二节事故）
            time.sleep(0.05)           # 模拟打印耗时（放大竞争窗口）
            print(f"{worker} 正在用 {self.name} 打印《{doc}》（第{self.printed}份）")
        # with 块结束自动释放锁（即使中间出了异常）


class Worker(threading.Thread):        # 继承 Thread：面向对象的多线程写法
    def __init__(self, name, printer, task_queue, stop_event):
        super().__init__(name=name)    # 给线程起名字
        self.printer = printer
        self.task_queue = task_queue
        self.stop_event = stop_event   # Event：统一停工信号灯
        self.done_count = 0            # 每个线程自己的计数（无需加锁）

    def run(self):                     # 线程启动后自动执行的方法（必须叫 run）
        while not self.stop_event.is_set():
            try:
                doc = self.task_queue.get(timeout=1)   # 队列空则等1秒
            except queue.Empty:
                continue               # 没任务，回头再查（顺便看停工信号）
            self.printer.print_doc(self.name, doc)
            self.done_count += 1
            self.task_queue.task_done()


def main():
    printer = Printer("办公楼打印机")
    task_queue = queue.Queue()          # 线程安全的任务队列
    stop_event = threading.Event()      # 停工信号（初始为"未亮灯"）

    for doc in ["月度报告", "合同", "通知", "发票", "简历", "图纸"]:
        task_queue.put(doc)

    workers = [Worker(f"员工{i}", printer, task_queue, stop_event) for i in range(1, 4)]

    for w in workers:
        w.start()                       # 启动线程：自动在子线程中调用 run()

    task_queue.join()                   # 主线程等待：直到所有任务被处理完

    stop_event.set()                    # 亮红灯：通知所有员工线程下班
    for w in workers:
        w.join()                        # 等线程真正退出

    print(f"\n统计：打印机共输出 {printer.printed} 份文档")
    for w in workers:
        print(f"  {w.name} 完成了 {w.done_count} 份")


if __name__ == "__main__":
    main()
```

运行效果（员工顺序每次可能不同——这正是并发的特点）：

```
员工1 正在用 办公楼打印机 打印《月度报告》（第1份）
员工2 正在用 办公楼打印机 打印《合同》（第2份）
员工3 正在用 办公楼打印机 打印《通知》（第3份）
员工1 正在用 办公楼打印机 打印《发票》（第4份）
员工2 正在用 办公楼打印机 打印《简历》（第5份）
员工3 正在用 办公楼打印机 打印《图纸》（第6份）

统计：打印机共输出 6 份文档
  员工1 完成了 2 份
  员工2 完成了 2 份
  员工3 完成了 2 份
```

### 逐个部件讲解

| 部件 | 代码位置 | 一句话原理 |
|------|----------|------------|
| **Lock 互斥锁** | `Printer.lock` | 打印机只有一台（临界区），`with lock` 保证排队使用。注意锁放在 **Printer**（资源）里而不是 Worker 里——**锁保护谁，就放在谁身上** |
| **with lock** | `print_doc` 内 | 等价于 `lock.acquire()` + `try/finally` + `lock.release()`，异常也不会忘记还钥匙 |
| **Queue 队列** | `task_queue` | 自带锁的线程安全容器，员工们"抢任务"不需要你写任何锁。**线程间传数据首选队列，不要共享变量** |
| **Event 事件** | `stop_event` | 全局开关灯：`set()` 亮灯、`is_set()` 查灯、`clear()` 熄灯。优雅停机的标准做法 |
| **run 重写** | `Worker.run` | 线程的"工作内容"。`start()` 开新线程去跑 `run()`；误写成 `w.run()` 则在主线程普通调用，**没有并发** |
| **join** | 两处 | 主线程原地等待。任务用 `queue.join()`（等队列清空），线程用 `w.join()`（等线程退出） |
| **timeout=1** | `queue.get` | 防止员工在空队列上死等——每 1 秒醒来一次看有没有停工信号，否则永远退不出循环 |

### 设计要点（面向对象视角）

1. **类职责划分**：`Printer` 是被保护的**共享资源**（自带锁），`Worker` 是**执行流**（继承 Thread），`main` 是**调度者**——三种角色不混写。
2. **`done_count` 为什么不加锁**：它是每个 Worker 线程私有的实例变量，别人不碰，无需保护。**只锁真正共享的东西**。
3. **为什么任务分发用 Queue 而不是共享 list**：普通 list 的 `append`/`pop` 不是线程安全组合操作；`queue.Queue` 内部已用锁封装好"放任务/取任务"的完整流程。

---

## 五、互斥工具箱速览

`threading` 模块提供一族同步工具，各自解决一类协调问题：

| 工具 | 语义 | 类比 | 典型用途 |
|------|------|------|----------|
| `Lock` | 一把钥匙，谁拿到谁能进 | 单间卫生间 | 保护单个共享资源（本文主用） |
| `RLock` | 可重入锁：同一线程可反复拿 | 自己家的门（可反复进出） | 锁内的方法又调用了另一个加锁方法 |
| `Semaphore(3)` | 发 3 把相同钥匙 | 3 个车位的停车场 | 限流：最多 N 个线程同时访问 |
| `Condition` | 锁 + 等待/通知 | 取餐呼叫器 | 生产者-消费者（队列内部就用它） |
| `Event` | 全局开关灯 | 下班铃 | 通知所有线程启停 |

```python
# Semaphore 示例：最多2个线程同时访问数据库
import threading

db_semaphore = threading.Semaphore(2)   # 2个"车位"

def query_db(sql):
    with db_semaphore:                  # 满了就在这里排队
        print(f"执行 {sql} ...")
        # ... 实际查询 ...

# 死锁警示：两个线程互相等对方手里的锁
# 线程1: with lock_a: ... with lock_b: ...
# 线程2: with lock_b: ... with lock_a: ...   ← 顺序相反 = 死锁
# 预防：所有线程按相同顺序拿锁；或用 with 一次拿一把尽快释放
```

---

## 六、线程池：ThreadPoolExecutor

手写 Thread 适合"长命线程"（如 Worker 常驻领任务）。如果只是"一批任务并发跑完拿结果"，**线程池**是更省事的标准姿势——池子自动管理线程的创建、复用和回收：

```python
import time, random
from concurrent.futures import ThreadPoolExecutor, as_completed

def fake_download(name):
    time.sleep(random.uniform(0.2, 0.8))    # 模拟网络下载耗时
    return f"{name} 下载完成"

with ThreadPoolExecutor(max_workers=3) as pool:     # 3个工作线程的池子
    futures = {pool.submit(fake_download, f"文件{i}"): f"文件{i}" for i in range(1, 6)}
    for fu in as_completed(futures):                # 谁先完成先处理谁
        print(fu.result())

print("全部下载完成")
```

**代码说明**：
- `pool.submit(函数, 参数)`：丢任务进池子，立刻返回一个 `Future`（"未来才有结果"的凭条）；
- `fu.result()`：兑现凭条——若任务没做完会**阻塞等待**；若任务抛了异常，在这里重新抛出；
- `as_completed(futures)`：按**完成顺序**（非提交顺序）逐个弹出；
- `with ... as pool`：块结束时自动 `shutdown()`，等所有任务跑完并回收线程。

> **AI 学习衔接**：同时调用 DeepSeek/OpenAI/通义三个平台生成回答再汇总，就是"5 个下载任务 + 3 个池线程"的结构——本课后续实战会直接用到。

---

## 七、异步编程：asyncio

### 7.1 多线程 vs 异步：一个比喻

- **多线程**：雇 3 个员工，各泡各的咖啡（每人一个线程，操作系统负责切换）
- **asyncio**：**1 个员工**，烧上水就去磨豆，水开了回来冲（单线程内自己调度，切换点由 `await` 显式标出）

异步没有线程切换开销，单机高并发（几百上千路 I/O）时效率更高，是现代 Web 服务、AI 应用（FastAPI、aiohttp）的主流写法。

### 7.2 最小例子：三杯咖啡

```python
import asyncio

async def brew_coffee(name):
    print(f"开始煮{name}")
    await asyncio.sleep(2)         # 非阻塞等待：等水开的2秒里，事件循环去推进其他协程
    print(f"{name}煮好了")
    return f"一杯{name}"

async def main():
    results = await asyncio.gather(     # 并发执行3个协程
        brew_coffee("拿铁"),
        brew_coffee("美式"),
        brew_coffee("摩卡"),
    )
    print(results)

asyncio.run(main())
```

运行效果（注意总耗时约 2 秒而不是 6 秒——三杯咖啡是**并发**煮的）：

```
开始煮拿铁
开始煮美式
开始煮摩卡
拿铁煮好了
美式煮好了
摩卡煮好了
['一杯拿铁', '一杯美式', '一杯摩卡']  总耗时约 2.0 秒
```

### 7.3 三个新语法（对照多线程记忆）

| asyncio | 对应多线程 | 说明 |
|---------|-----------|------|
| `async def` 定义协程函数 | `def` + Thread | 调用它不执行，返回一个协程对象 |
| `await 等待物` | 无（隐式切换） | **唯一让出控制权的位置**：等待期间事件循环去跑别的协程 |
| `asyncio.gather(...)` | 多个 `Thread` + `join` | 并发收集多个协程的结果 |
| `async with asyncio.Lock()` | `with threading.Lock()` | 互斥锁的异步版，用法几乎一致 |
| `asyncio.run(main())` | `for t: t.start()` | 程序入口：创建事件循环并跑主协程 |

```python
# asyncio 也有锁：同样保护共享资源
import asyncio

counter = 0
lock = asyncio.Lock()

async def safe_add(n):
    global counter
    for _ in range(n):
        async with lock:            # 与 threading.Lock 用法一致，只是多了 async
            counter += 1
```

### 7.4 铁律

1. `await` 只能出现在 `async def` 函数内部；
2. 协程不会被自动运行——必须 `asyncio.run()` 或被 `gather` / `await`；
3. **不要在协程里调用阻塞函数**（如 `time.sleep(2)`、`requests.get()`）——单线程会被卡死，其他协程全部停摆。应使用 `asyncio.sleep()`、`aiohttp` 等异步版本；实在只有同步库时可用 `await asyncio.to_thread(阻塞函数)` 把它丢进线程。

---

## 八、选型总结：线程、异步、进程

| 方案 | 适用场景 | 本文化身 | 代价 |
|------|----------|----------|------|
| **不用并发** | 单个任务、几秒钟内完成 | 第二节之前的例子 | — |
| **多线程 threading** | I/O 密集 + 任务量中等（几个~几十个）+ 代码简单直接 | 打印室、线程池 | 有锁的心智负担；GIL 限制无 CPU 加速 |
| **asyncio 异步** | I/O 密集 + 高并发（成百上千路）+ 生态支持 | 三杯咖啡 | 语法侵入性强（async 传染整个调用链），阻塞函数会毁掉全局 |
| **multiprocessing 进程** | CPU 密集（大量计算：图像处理、数据分析） | 无（本文不含） | 进程开销大、跨进程通信麻烦 |

**记忆口诀**：**等得多（I/O）用线程或异步，算得多（CPU）用进程；几十路并发图省事用线程，成千上万路用异步。**

> 展望：Python 3.13 起官方提供实验性"自由线程版"（free-threaded，去掉 GIL），未来多线程也可能加速纯计算——目前生产环境仍按上表选型。

---

## 九、课堂练习

全部通过**修改打印室程序**完成（由易到难）：

1. **观察**：把 `Printer.print_doc` 中的 `with self.lock:` 去掉，多跑几次，观察"第N份"编号和 `printed` 统计是否还正确。（答案：`+=` 依然可能丢失更新——回到第二节的"事故现场"）
2. **改参数**：把员工人数从 3 改成 6、任务从 6 份改成 20 份，观察任务分配是否均匀。
3. **加功能**：给 `Worker` 增加 `is_urgent` 属性，紧急任务用 `task_queue.put(doc)` 前置方式优先处理（提示：研究 `queue.PriorityQueue`）。
4. **线程池改写**：用第六节的 `ThreadPoolExecutor` 重写"6 个任务、3 个工人"的下载场景，对比与打印室代码的长短。
5. **挑战（异步）**：把"三杯咖啡"改成"并发调用 3 次大模型 API"：用 `asyncio.sleep(2)` 模拟 API 延迟，用 `asyncio.gather` 并发请求，验证总耗时约等于最慢一次请求而非三次之和——这就是第 6 周"多平台 API 调用实战"将要真实发生的事。

---

## 附：与课程的衔接

| 本文内容 | 后续用在哪里 |
|----------|--------------|
| ThreadPoolExecutor 并发请求 | 第 6 周《多平台 API 调用实战》：同时调多家模型对比回答 |
| asyncio + aiohttp | 第 6 周 Web 应用：Streamlit/FastAPI 的非阻塞调用 |
| Lock 保护共享资源 | 第 7 周 MCP 实战：多个 AI 请求并发写同一个待办清单文件 |
| Queue 任务分发 | 第 8 周多 Agent：任务在多个 Agent 间流转 |

> **一句话总结**：多线程 = 多个工人共用一间办公室（共享内存）；锁 = 办公室里只能一人用的资源要排队；异步 = 一个工人聪明地穿插任务。I/O 等待是 Python 并发的主战场，也是 AI 应用最典型的耗时来源。
