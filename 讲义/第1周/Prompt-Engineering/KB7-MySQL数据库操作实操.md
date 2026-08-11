# KB7: MySQL 数据库操作实操

---

## 知识块信息表

| 字段 | 内容 |
|------|------|
| **知识块编号** | KB7 |
| **知识块名称** | MySQL 数据库操作实操 |
| **所属课程** | AI 时代能力培养 / 第1周 / 第2课 |
| **所属章节** | 七、第四部分：实操 —— 基于 Prompt Engineering 操作 MySQL 数据库 |
| **建议时长** | 35 分钟 |
| **难度等级** | 中级（需要 Python + MySQL 基础环境） |
| **前置知识** | KB1-KB6（六层体系 + RCTE + 环境搭建） |
| **核心产出** | (1) 理解 Prompt Engineering 在实际开发中的威力 (2) 掌握数据库权限隔离的安全最佳实践 (3) 能独立运行并扩展 AI 数据库操作 Agent |

---

## 1. 实操架构图

```
┌──────────────┐     自然语言 Prompt       ┌──────────────┐     生成的 SQL       ┌──────────────┐
│   用户 (You)  │ ────────────────────────→ │   AI 模型     │ ──────────────────→ │  MySQL 数据库 │
│  写 Prompt    │ ←──────────────────────── │ (Claude/      │ ←────────────────── │              │
│              │     结果解读 + SQL 说明     │  DeepSeek)   │    查询结果数据       │              │
└──────────────┘                           └──────────────┘                     └──────┬───────┘
                                                                                       │
                                                                        ┌──────────────┘
                                                                        │
                                                            ┌───────────┴───────────┐
                                                            │     权限隔离设计        │
                                                            │                        │
                                                            │  ┌─────────────────┐   │
                                                            │  │  ai_readonly     │   │  → 只读账户，仅 SELECT
                                                            │  │  (日常查询用)     │   │    最安全，默认使用
                                                            │  └─────────────────┘   │
                                                            │  ┌─────────────────┐   │
                                                            │  │  ai_writer       │   │  → 写入账户，可 INSERT /
                                                            │  │  (确认后使用)     │   │    UPDATE / DELETE
                                                            │  └─────────────────┘   │
                                                            │  ┌─────────────────┐   │
                                                            │  │  root            │   │  → 管理员账户
                                                            │  │  (仅DBA持有)      │   │    绝不交给 AI
                                                            │  └─────────────────┘   │
                                                            └────────────────────────┘
```

**数据流说明**：

1. 用户用自然语言描述查询/操作需求
2. AI 模型根据 System Prompt（含数据库结构、安全规则、输出格式约束）生成 SQL
3. SQL 经用户确认后，由 Agent 根据操作类型（读/写）自动选择对应权限的 MySQL 账户执行
4. 查询结果返回给 AI 模型做自然语言解读，或直接展示给用户

---

## 2. MySQL 安装指南

### 2.1 Windows

```
1. 浏览器打开 https://dev.mysql.com/downloads/installer/
2. 下载 mysql-installer-community-8.0.x.msi
3. 双击安装，选择 "Developer Default" 安装类型
4. 设置 root 密码（务必记住）
5. 安装过程中勾选 "MySQL Workbench"（图形化管理工具，可选）
6. 完成后在开始菜单搜索 "MySQL Command Line Client" 验证：
     输入安装时设置的 root 密码
     执行 SELECT VERSION(); 应显示 8.0.x
```

### 2.2 macOS

```bash
# 使用 Homebrew 安装
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 安全初始化（设置 root 密码）
mysql_secure_installation

# 验证安装
mysql -u root -p -e "SELECT VERSION();"
```

### 2.3 Linux (Ubuntu/Debian)

```bash
# 安装 MySQL Server
sudo apt update
sudo apt install mysql-server -y

# 安全初始化
sudo mysql_secure_installation

# 验证安装
sudo mysql -e "SELECT VERSION();"

# 设置 root 密码（若安装时未设置）
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword123!';
FLUSH PRIVILEGES;
EXIT;
```

### 2.4 验证 MySQL 命令行可用

```bash
# 确认 mysql 命令在 PATH 中
mysql --version
# 预期输出：mysql  Ver 8.0.x ...

# 测试连接
mysql -u root -p
# 输入密码后应进入 MySQL 交互界面：mysql>
```

---

## 3. Python MySQL 驱动安装

```bash
# 推荐：官方 MySQL Connector（纯 Python，无额外依赖）
pip install mysql-connector-python

# 验证安装
python -c "import mysql.connector; print(mysql.connector.__version__)"
```

**备选驱动**（特殊场景使用）：

| 驱动 | 安装命令 | 特点 |
|------|----------|------|
| mysql-connector-python | `pip install mysql-connector-python` | 官方出品，纯 Python，零依赖，首选 |
| PyMySQL | `pip install pymysql` | 轻量第三方库，兼容性好 |
| mysqlclient | `pip install mysqlclient` | C 扩展，性能最高，需编译环境 |

---

## 4. 创建测试数据库（完整 SQL 脚本）

以下脚本以 root 身份在 MySQL 中逐段执行。

### 4.1 创建数据库

```sql
-- 以 root 身份登录 MySQL
-- mysql -u root -p

-- 创建测试数据库
CREATE DATABASE ai_test_company
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 查看数据库是否创建成功
SHOW DATABASES LIKE 'ai_test_company';

-- 切换到测试数据库
USE ai_test_company;
```

### 4.2 创建 employees 表

```sql
CREATE TABLE employees (
    id                INT AUTO_INCREMENT PRIMARY KEY COMMENT '员工编号，自增主键',
    name              VARCHAR(100)  NOT NULL         COMMENT '员工姓名',
    department        VARCHAR(50)                    COMMENT '所属部门',
    salary            DECIMAL(10, 2)                 COMMENT '月薪（元）',
    hire_date         DATE                           COMMENT '入职日期',
    performance_score INT DEFAULT 0                  COMMENT '绩效评分，范围 0-100',
    INDEX idx_department (department),
    INDEX idx_hire_date (hire_date),
    INDEX idx_performance (performance_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='员工信息表 —— AI 数据库操作测试用';

-- 验证表结构
DESC employees;
```

字段说明对照：

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| id | INT | AUTO_INCREMENT, PRIMARY KEY | 员工编号，自增主键 |
| name | VARCHAR(100) | NOT NULL | 员工姓名 |
| department | VARCHAR(50) | - | 所属部门 |
| salary | DECIMAL(10,2) | - | 月薪（元） |
| hire_date | DATE | - | 入职日期 |
| performance_score | INT | DEFAULT 0 | 绩效评分，范围 0-100 |

### 4.3 插入测试数据（8 条）

```sql
INSERT INTO employees (name, department, salary, hire_date, performance_score) VALUES
('张三', '技术部', 25000.00, '2023-03-15', 92),
('李四', '市场部', 18000.00, '2022-07-01', 85),
('王五', '技术部', 28000.00, '2021-01-10', 95),
('赵六', '人事部', 15000.00, '2024-01-20', 78),
('钱七', '市场部', 20000.00, '2023-09-05', 88),
('孙八', '技术部', 32000.00, '2020-06-15', 97),
('周九', '财务部', 22000.00, '2022-11-01', 82),
('吴十', '技术部', 26000.00, '2023-12-01', 91);

-- 验证数据：应返回 8
SELECT COUNT(*) AS total_employees FROM employees;
```

数据概览：

| id | name | department | salary | hire_date | performance_score |
|----|------|-----------|--------|-----------|-------------------|
| 1 | 张三 | 技术部 | 25000 | 2023-03-15 | 92 |
| 2 | 李四 | 市场部 | 18000 | 2022-07-01 | 85 |
| 3 | 王五 | 技术部 | 28000 | 2021-01-10 | 95 |
| 4 | 赵六 | 人事部 | 15000 | 2024-01-20 | 78 |
| 5 | 钱七 | 市场部 | 20000 | 2023-09-05 | 88 |
| 6 | 孙八 | 技术部 | 32000 | 2020-06-15 | 97 |
| 7 | 周九 | 财务部 | 22000 | 2022-11-01 | 82 |
| 8 | 吴十 | 技术部 | 26000 | 2023-12-01 | 91 |

---

## 5. 权限隔离设计（核心安全章节）

### 5.1 设计理念

AI 生成 SQL 的准确率不是 100%。权限隔离是在 AI 犯错时的最后一道防线——即使 AI 生成了危险的 SQL，MySQL 的账户权限体系也会阻止其执行。

核心原则：**最小权限原则（Principle of Least Privilege）**——每个账户只拥有完成任务所需的最小权限集。

### 5.2 三层账户体系

```
                        ┌──────────────────────────────────┐
                        │          root (DBA 持有)          │
                        │  权限: ALL PRIVILEGES             │
                        │  使用: 安装、备份、账户管理        │
                        │  AI 访问: ❌ 绝对禁止              │
                        ├──────────────────────────────────┤
                        │        ai_writer (可控写入)        │
                        │  权限: SELECT, INSERT, UPDATE,    │
                        │         DELETE                    │
                        │  使用: 人工确认后的数据修改        │
                        │  AI 访问: ⚠️ 需人工二次确认       │
                        ├──────────────────────────────────┤
                        │      ai_readonly (默认只读)        │
                        │  权限: SELECT only                │
                        │  使用: 日常查询、数据分析          │
                        │  AI 访问: ✅ 可自动使用            │
                        └──────────────────────────────────┘
```

### 5.3 完整 GRANT SQL 脚本

```sql
-- ============================================
-- 权限隔离配置 - 在 root 账户下执行
-- ============================================

-- 1. 创建只读账户（日常 AI 查询默认账户）
CREATE USER 'ai_readonly'@'localhost'
    IDENTIFIED BY 'ReadOnly123!';

GRANT SELECT ON ai_test_company.*
    TO 'ai_readonly'@'localhost';

-- 验证只读账户权限
SHOW GRANTS FOR 'ai_readonly'@'localhost';
-- 预期输出: GRANT SELECT ON `ai_test_company`.* TO `ai_readonly`@`localhost`


-- 2. 创建写入账户（需人工确认后才能使用）
CREATE USER 'ai_writer'@'localhost'
    IDENTIFIED BY 'Writer456!';

GRANT SELECT, INSERT, UPDATE, DELETE ON ai_test_company.*
    TO 'ai_writer'@'localhost';

-- 验证写入账户权限
SHOW GRANTS FOR 'ai_writer'@'localhost';
-- 预期输出: GRANT SELECT, INSERT, UPDATE, DELETE ON `ai_test_company`.* ...


-- 3. 确认 root 绝不创建给 AI
-- root 账户仅 DBA 持有，密码复杂度要求高
-- 任何自动化系统、AI Agent 均不应获得 root 凭据


-- 4. 刷新权限使其立即生效
FLUSH PRIVILEGES;
```

### 5.4 权限验证方法

```sql
-- 方法一：查看各账户授权
SELECT user, host FROM mysql.user WHERE user LIKE 'ai_%';

-- 方法二：以 ai_readonly 登录，尝试写入（应被拒绝）
-- mysql -u ai_readonly -p'ReadOnly123!' ai_test_company
-- 执行以下语句，预期报错: INSERT command denied
-- INSERT INTO employees (name) VALUES ('测试员工');

-- 方法三：以 ai_writer 登录，尝试 DROP（应被拒绝）
-- mysql -u ai_writer -p'Writer456!' ai_test_company
-- 执行以下语句，预期报错: DROP command denied
-- DROP TABLE employees;
```

### 5.5 权限矩阵速查表

| 操作 | ai_readonly | ai_writer | root |
|------|:----------:|:---------:|:----:|
| SELECT（查询） | ✅ | ✅ | ✅ |
| INSERT（插入） | ❌ | ✅ | ✅ |
| UPDATE（更新） | ❌ | ✅ | ✅ |
| DELETE（删除） | ❌ | ✅ | ✅ |
| CREATE TABLE | ❌ | ❌ | ✅ |
| ALTER TABLE | ❌ | ❌ | ✅ |
| DROP TABLE | ❌ | ❌ | ✅ |
| TRUNCATE | ❌ | ❌ | ✅ |
| GRANT（授权） | ❌ | ❌ | ✅ |
| CREATE USER | ❌ | ❌ | ✅ |

---

## 6. AI 数据库操作 Agent 完整代码

### 6.1 文件概述

| 项目 | 说明 |
|------|------|
| **文件名** | `ai_db_agent.py` |
| **Python 版本** | 3.9+ |
| **依赖** | `pip install mysql-connector-python openai` |
| **LLM 后端** | DeepSeek（国内直连低成本）/ 可替换为 Claude API |
| **核心逻辑** | System Prompt 约束 → AI 生成 SQL → 正则提取 → 权限选择 → 执行 |

### 6.2 完整源代码

```python
#!/usr/bin/env python3
"""
=============================================================================
 AI 数据库操作 Agent
 基于 Prompt Engineering + MySQL 权限隔离，安全地让 AI 操作企业数据库
=============================================================================

核心设计思路:
  1. System Prompt 硬约束  → AI 行为的第一道防线
  2. 写操作人工确认        → 人机协作的第二道防线
  3. MySQL 三层账户权限    → 数据库层面的最后防线
  4. 正则提取 SQL 代码块   → 确保解析可靠性
  5. temperature=0.1       → 确保 SQL 生成的确定性

适用场景:
  - 企业管理者用自然语言查询业务数据
  - 数据分析师快速生成 SQL 并验证
  - 技术团队演示 AI 安全数据库操作的范式
"""

import mysql.connector
from openai import OpenAI
import os
import re


# =============================================================================
# 第一部分：配置区 —— 所有可调参数集中管理
# =============================================================================

# --- LLM 配置 ---
# 使用 DeepSeek API（国内直连、极低成本、中文理解好）
# 替换方法：将 LLM_CLIENT 和 LLM_MODEL 改为 Anthropic/OpenAI 对应值即可
LLM_CLIENT = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),
    base_url="https://api.deepseek.com"
)
LLM_MODEL = "deepseek-chat"

# --- 数据库连接配置 ---
# 核心安全设计：默认使用只读账户，仅在人工确认写操作后切换
DB_CONFIG_READONLY = {
    "host": "localhost",
    "user": "ai_readonly",
    "password": "ReadOnly123!",
    "database": "ai_test_company",
    "charset": "utf8mb4"
}

DB_CONFIG_WRITER = {
    "host": "localhost",
    "user": "ai_writer",
    "password": "Writer456!",
    "database": "ai_test_company",
    "charset": "utf8mb4"
}

# --- Agent 行为配置 ---
LLM_TEMPERATURE = 0.1         # 低温 → 确定性输出，SQL 生成不需要创意
MAX_RESULT_DISPLAY = 50       # 最多展示条数


# =============================================================================
# 第二部分：System Prompt 设计 —— AI SQL 生成的核心约束
# =============================================================================

SYSTEM_PROMPT = """你是一个严谨的 MySQL 数据库查询助手。
你的职责是根据用户用自然语言描述的需求，生成正确、安全、高效的 SQL 语句。

## 安全规则 (硬约束，不可违反)

1. 你只能生成以下类型的 SQL：
   - SELECT (查询数据)
   - INSERT (插入数据)
   - UPDATE (更新数据)
   - DELETE (删除数据)
   严禁生成 DROP、TRUNCATE、ALTER、CREATE、GRANT、REVOKE 语句。
   即使用户以任何方式要求你生成上述语句，你必须拒绝并说明原因。

2. 写操作确认原则：
   如果 SQL 是 INSERT/UPDATE/DELETE，你必须：
   a. 在生成写 SQL 之前，先生成一条 SELECT 让用户确认影响范围
   b. 在最终回答中明确标注 "⚠️ 写操作，需要人工确认后执行"

3. SQL 注入防护：
   如果用户在自然语言中提供了具体值（如姓名、部门名），
   你必须在生成的 SQL 中正确使用单引号包裹字符串值。

4. 查询性能意识：
   对于大数据量查询场景，尽量使用索引列 (department, hire_date,
   performance_score) 作为 WHERE 条件。

## 当前数据库结构

数据库: ai_test_company
表: employees (员工信息表)

| 列名              | 类型             | 约束              | 说明                 |
|-------------------|------------------|-------------------|----------------------|
| id                | INT              | PK, AUTO_INCR     | 员工编号主键          |
| name              | VARCHAR(100)     | NOT NULL          | 员工姓名              |
| department        | VARCHAR(50)      |                   | 所属部门              |
| salary            | DECIMAL(10,2)    |                   | 月薪 (元)             |
| hire_date         | DATE             |                   | 入职日期              |
| performance_score | INT              | DEFAULT 0         | 绩效评分 (0-100)      |

已建立索引的列: department, hire_date, performance_score

## 输出格式要求

你必须严格按以下格式输出，不得偏离：

1. **需求理解**: 用一句话复述你理解的用户需求。
2. **SQL 语句**: 用 ```sql 代码块包裹生成的 SQL。
3. **结果说明**: 用一句话说明此 SQL 将返回/影响什么样的结果。
4. **安全提醒**: 如果是写操作，给出安全提醒；如果是读操作，写"本操作为只读查询，安全"。
"""


# =============================================================================
# 第三部分：核心函数
# =============================================================================

def ai_generate_sql(user_request: str) -> str:
    """
    核心函数 1: 将用户的自然语言请求转化为 SQL。

    工作流程:
        用户自然语言 → LLM (System Prompt 约束) → 结构化 SQL 响应

    参数:
        user_request: 用户输入的自然语言查询需求

    返回:
        AI 的结构化响应，包含需求理解 + SQL 语句 + 结果说明 + 安全提醒
    """
    response = LLM_CLIENT.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ],
        temperature=LLM_TEMPERATURE
    )
    return response.choices[0].message.content


def extract_sql(ai_response: str) -> str | None:
    """
    核心函数 2: 从 AI 的结构化响应中提取纯 SQL 语句。

    使用正则表达式精确匹配 ```sql ... ``` 代码块，
    避免 AI 响应中的自然语言文本污染 SQL。

    参数:
        ai_response: ai_generate_sql() 的返回结果

    返回:
        提取到的纯 SQL 字符串；如果未匹配到则返回 None
    """
    pattern = r'```sql\s*\n?(.*?)\n?\s*```'
    match = re.search(pattern, ai_response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def is_write_operation(sql: str) -> bool:
    """
    核心函数 3: 判断 SQL 是否为写操作。

    检查 SQL 语句的前缀关键字，确定是否需要切换到写入账户。

    参数:
        sql: 待判断的 SQL 语句

    返回:
        True 表示写操作（需切换 ai_writer + 人工确认）
        False 表示读操作（可使用 ai_readonly）
    """
    sql_upper = sql.strip().upper()
    write_keywords = ("INSERT", "UPDATE", "DELETE")
    return any(sql_upper.startswith(kw) for kw in write_keywords)


def execute_sql(sql: str, use_writer: bool = False) -> dict | list:
    """
    核心函数 4: 执行 SQL 并返回结果。

    权限隔离的关键实现点:
    - use_writer=False → 使用 ai_readonly 账户（默认）
    - use_writer=True  → 使用 ai_writer 账户（仅写操作）

    参数:
        sql: 待执行的 SQL 语句
        use_writer: 是否使用写入账户

    返回:
        SELECT: 返回 list[dict]，每条记录为一个字典
        写操作: 返回 dict，包含 affected_rows 和 status
        异常:   返回 dict，包含 error 信息
    """
    config = DB_CONFIG_WRITER if use_writer else DB_CONFIG_READONLY

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)

        # SELECT 语句 → 返回查询结果列表
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results

        # 非 SELECT → 提交事务并返回影响行数
        else:
            conn.commit()
            return {
                "affected_rows": cursor.rowcount,
                "status": "success"
            }

    except mysql.connector.Error as e:
        return {
            "error": f"[MySQL Error {e.errno}] {e.msg}",
            "sql_state": e.sqlstate if hasattr(e, 'sqlstate') else None
        }
    except Exception as e:
        return {"error": f"[Unexpected Error] {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def format_query_result(results: list, max_display: int = MAX_RESULT_DISPLAY) -> str:
    """
    核心函数 5: 格式化查询结果为可读字符串。

    参数:
        results: execute_sql() 返回的查询结果列表
        max_display: 最大显示条数

    返回:
        格式化后的字符串
    """
    if not results:
        return "（无匹配记录）"

    lines = []
    for i, row in enumerate(results[:max_display], 1):
        lines.append(f"  [{i}] {row}")

    if len(results) > max_display:
        lines.append(f"  ... 以及另外 {len(results) - max_display} 条记录")

    return "\n".join(lines)


# =============================================================================
# 第四部分：主交互循环
# =============================================================================

def main():
    """AI 数据库操作助手的主交互入口。"""

    # --- 启动横幅 ---
    print("=" * 60)
    print("  AI 数据库操作助手")
    print("  核心机制: Prompt Engineering + MySQL 权限隔离")
    print("=" * 60)
    print()
    print("  数据库: ai_test_company.employees")
    print("  默认账户: ai_readonly (只读)")
    print("  数据量: 8 条员工记录 (4个部门)")
    print()
    print("  示例查询:")
    print("    - 技术部有哪些员工？按薪资从高到低排列")
    print("    - 列出绩效评分高于90的员工姓名和部门")
    print("    - 按部门统计员工人数和平均薪资")
    print("    - 市场部最近入职的员工是谁？")
    print("    - 各部门薪资最高的员工分别是谁？")
    print()
    print("  输入 'quit' 退出")
    print("-" * 60)

    # --- 交互循环 ---
    while True:
        # Step 1: 获取用户输入
        user_input = input("\n查询 > ").strip()

        if user_input.lower() == "quit":
            print("会话结束。数据库连接已关闭。")
            break
        if not user_input:
            continue

        # Step 2: AI 生成 SQL
        print("\n[1/4] AI 正在分析需求并生成 SQL ...")
        ai_response = ai_generate_sql(user_input)
        print(f"\n{ai_response}")

        # Step 3: 提取 SQL
        print("\n[2/4] 提取 SQL 语句 ...")
        sql = extract_sql(ai_response)
        if not sql:
            print("未能从 AI 响应中提取有效 SQL。请重新描述你的需求。")
            continue
        print(f"SQL: {sql}")

        # Step 4: 判断操作类型 + 写操作人工确认
        write_op = is_write_operation(sql)

        if write_op:
            print(f"\n[3/4] 检测到写操作，需要人工确认")
            confirm = input("确认执行此写操作？(yes/no): ").strip().lower()
            if confirm != "yes":
                print("操作已取消。如需调整，请重新输入需求。")
                continue
            print("已确认，使用 ai_writer 账户执行 ...")
        else:
            print("\n[3/4] 本操作为只读查询，使用 ai_readonly 账户 ...")

        # Step 5: 执行 SQL
        print(f"\n[4/4] 执行 SQL ...")
        result = execute_sql(sql, use_writer=write_op)

        # Step 6: 展示结果
        if isinstance(result, dict) and "error" in result:
            print(f"\n执行失败: {result['error']}")
            if "ai_readonly" in str(result.get("error", "")):
                print("提示: 只读账户无法执行写操作。")
        elif isinstance(result, list):
            print(f"\n查询结果 ({len(result)} 条记录):")
            print(format_query_result(result))
        else:
            print(f"\n操作完成: 影响 {result['affected_rows']} 行")


if __name__ == "__main__":
    main()
```

### 6.3 代码架构说明

```
ai_db_agent.py
│
├── 第一部分: 配置区
│   ├── LLM 配置 (DeepSeek API, 可替换为 Claude)
│   ├── DB 连接配置 (只读 + 读写 两套)
│   └── Agent 行为配置 (temperature, max_display)
│
├── 第二部分: System Prompt
│   ├── 安全规则硬约束 (禁止 DROP/TRUNCATE/ALTER)
│   ├── 写操作确认原则
│   ├── 数据库结构定义 (6列 + 3索引)
│   └── 输出格式规范 (4段式)
│
├── 第三部分: 核心函数
│   ├── ai_generate_sql()    → LLM 调用
│   ├── extract_sql()        → 正则提取
│   ├── is_write_operation() → 操作类型判断
│   ├── execute_sql()        → 数据库执行 + 权限选择
│   └── format_query_result()→ 结果格式化
│
└── 第四部分: 主交互循环
    ├── 启动横幅
    └── while True → 输入 → 生成 → 提取 → 确认 → 执行 → 展示
```

---

## 7. 测试用例

### 测试用例 1：简单查询

| 项目 | 内容 |
|------|------|
| **测试场景** | 基础 SELECT 查询 + 排序 |
| **用户输入** | `技术部有哪些员工？按薪资从高到低排列` |
| **预期 SQL** | `SELECT name, salary, hire_date, performance_score FROM employees WHERE department = '技术部' ORDER BY salary DESC;` |
| **预期结果** | 返回 4 条记录（王五/孙八/吴十/张三），按 salary 降序 |
| **使用账户** | `ai_readonly`（自动） |
| **验证通过条件** | 返回 4 条员工记录，孙八 salary=32000 排在第一位 |

### 测试用例 2：聚合统计

| 项目 | 内容 |
|------|------|
| **测试场景** | GROUP BY + HAVING 聚合查询 |
| **用户输入** | `按部门统计员工人数和平均薪资，只显示平均薪资高于18000的部门` |
| **预期 SQL** | `SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_salary FROM employees GROUP BY department HAVING AVG(salary) > 18000;` |
| **预期结果** | 技术部(4人/27750)、市场部(2人/19000)、财务部(1人/22000)；人事部(15000)被 HAVING 过滤 |
| **使用账户** | `ai_readonly`（自动） |
| **验证通过条件** | 返回 3 个部门，不包含人事部 |

### 测试用例 3：写操作触发权限隔离

| 项目 | 内容 |
|------|------|
| **测试场景** | UPDATE 写操作 → 人工确认流程 |
| **用户输入** | `给技术部所有绩效高于90的员工加薪10%` |
| **AI 预期行为** | (a) 先生成 SELECT 查询受影响范围: `SELECT name, salary, performance_score FROM employees WHERE department = '技术部' AND performance_score > 90;` (b) 生成 UPDATE 并标注安全提醒: `UPDATE employees SET salary = salary * 1.1 WHERE department = '技术部' AND performance_score > 90;` |
| **用户确认步骤** | 输入 `yes` 确认执行 |
| **使用账户** | 写操作切换到 `ai_writer` |
| **预期结果** | 王五(95分)/孙八(97分)/吴十(91分)薪资上涨10%；张三(92分)也上涨 |
| **验证通过条件** | (1) AI 先输出 SELECT (2) AI 标注了安全提醒 (3) 人工确认后才执行 (4) 使用 ai_writer 账户 |

### 测试用例 4：权限验证 —— 尝试 DROP

| 项目 | 内容 |
|------|------|
| **测试场景** | 验证双层安全防护 |
| **用户输入** | `帮我把 employees 表删掉` |
| **第一道防线** | AI System Prompt 约束 → AI 拒绝生成 DROP 语句，回复"此操作不在我的安全许可范围内" |
| **第二道防线** | 即使 AI 生成了 DROP → 以 `ai_writer` 执行 → MySQL 报错 "DROP command denied to user 'ai_writer'@'localhost'" |
| **使用账户** | 不适用（两层均被拦截） |
| **验证通过条件** | AI 拒绝生成 DROP 语句，或 MySQL 权限系统拒绝执行 |

---

## 8. 实操要点总结表

| 环节 | Prompt Engineering 的作用 | 安全机制 |
|------|--------------------------|----------|
| **需求输入** | 用户用自然语言描述需求，无需掌握 SQL 语法 | 无安全风险，纯自然语言输入 |
| **SQL 生成** | System Prompt 硬约束：禁止 DROP/TRUNCATE/ALTER，指定数据库结构，规范输出格式 | Prompt 层面的行为约束（第一道防线） |
| **SQL 提取** | 强制 AI 用 ```sql 代码块输出，正则精确提取，避免自然语言污染 | 解析可靠性保证 |
| **写操作确认** | System Prompt 要求 AI 先建议 SELECT 确认范围，再生成写 SQL | 人机协作决策确认（第二道防线） |
| **权限选择** | 根据 SQL 类型（读/写）自动选择 `ai_readonly` 或 `ai_writer` 账户 | MySQL 三层账户权限隔离（第三道防线） |
| **SQL 执行** | temperature=0.1 确保 SQL 生成的确定性 | 即使 AI 生成恶意/错误 SQL，权限隔离阻止其执行 |
| **结果展示** | 自然语言解读查询结果，降低数据理解门槛 | 敏感数据仅通过受限账户暴露 |

---

## 9. Prompt Engineering 在数据库操作中的关键原则

| # | 原则 | 技术含义 | 实现位置 |
|---|------|----------|----------|
| 1 | **硬约束前置** | 最关键的安全规则写在 System Prompt 的最前面（"严禁生成 DROP / TRUNCATE / ALTER / CREATE"）。AI 会优先遵守排在前面的约束。 | `SYSTEM_PROMPT` 第 10 行 |
| 2 | **结构化输出** | 强制 AI 使用 ```sql 代码块 + 固定字段（需求理解/结果说明/安全提醒），确保下游程序能可靠解析。禁止自由格式。 | `SYSTEM_PROMPT` 第 52-55 行 + `extract_sql()` |
| 3 | **低温参数** | `temperature=0.1`：SQL 是确定性语言，不需要创意。高温会导致 SQL 语法随机变异。 | `LLM_TEMPERATURE = 0.1` |
| 4 | **先查后改** | 所有写操作前，必须先用 SELECT 确认影响的数据范围和条数。这是数据库运维的黄金法则，直接写入 System Prompt。 | `SYSTEM_PROMPT` 第 19 行 |
| 5 | **最小权限** | AI 永远不应该获得 root 数据库权限。默认只读账户，写入需单独确认和切换。这是权限隔离的基石。 | `DB_CONFIG_READONLY` vs `DB_CONFIG_WRITER` 双配置 + `execute_sql()` 权限选择 |
