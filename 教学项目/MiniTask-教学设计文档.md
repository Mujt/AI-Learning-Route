# MiniTask —— 简易任务管理系统 · 教学设计文档

> **用途**：Agent 辅助编程教学——学生使用 VSCode + Claude Code，按照本文档中的 7 个 Prompt 逐步生成一个完整的前后端项目。
>
> **预计耗时**：~30 分钟（含理解设计 5 分钟 + 执行 7 个 Prompt 约 25 分钟）
>
> **覆盖知识点**：数据库设计与初始化、用户认证与JWT、RBAC角色权限控制、RESTful API设计、前后端交互、SQL查询与过滤、数据库权限概念

---

## 目录

1. [项目整体设计](#一项目整体设计)
   - 1.1 项目简介
   - 1.2 技术栈
   - 1.3 系统架构
   - 1.4 数据库设计
   - 1.5 API 设计
   - 1.6 权限模型
   - 1.7 前端页面设计
2. [Prompt 序列](#二prompt-序列按步骤生成项目)
   - Prompt 1：项目骨架初始化
   - Prompt 2：数据库模型与初始化脚本
   - Prompt 3：用户认证系统
   - Prompt 4：任务 CRUD API
   - Prompt 5：用户管理 API（管理员专属）
   - Prompt 6：前端三件套（HTML + CSS + JS）
   - Prompt 7：集成整合与启动脚本
3. [运行与验证](#三运行与验证)
4. [扩展思考题](#四扩展思考题)

---

## 一、项目整体设计

### 1.1 项目简介

**MiniTask** 是一个极简的任务管理系统，支持：

- **用户注册/登录**：使用 JWT 令牌认证
- **任务 CRUD**：创建、查看、编辑、删除任务
- **角色权限**：管理员（admin）vs 普通用户（user）
  - 管理员：管理所有任务、管理所有用户
  - 普通用户：仅能查看和更新分配给自己的任务
- **任务看板**：按状态分列展示（待办 / 进行中 / 已完成）

### 1.2 技术栈

| 层级 | 技术 | 选型理由 |
|------|------|----------|
| **后端框架** | Python 3 + Flask | 轻量、易读、零学习曲线 |
| **数据库** | SQLite | 零配置，文件即数据库，适合教学 |
| **认证** | PyJWT (JSON Web Token) | 业界标准，前端携带 token 访问 API |
| **密码加密** | Werkzeug Security | Flask 内置依赖，安全哈希 |
| **前端** | 原生 HTML + CSS + JavaScript | 无框架依赖，聚焦核心概念 |
| **跨域** | Flask-CORS | 前后端分离的必备中间件 |

### 1.3 系统架构

```
┌──────────────────────────────────────────────────────────┐
│                    用户浏览器                              │
│  ┌──────────────────────────────────────────────────┐    │
│  │  frontend/                                        │    │
│  │  ├── index.html    (登录/注册/主界面)              │    │
│  │  ├── style.css     (响应式 UI)                    │    │
│  │  └── app.js        (API 调用 + DOM 渲染)           │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │  HTTP (fetch + JWT Bearer)       │
└─────────────────────────┼────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────┐
│                    后端服务器 (Flask)                       │
│  ┌──────────────────────┴───────────────────────────┐    │
│  │  backend/                                         │    │
│  │  ├── run.py          (启动入口)                    │    │
│  │  ├── app.py          (Flask 应用 + 路由注册)       │    │
│  │  ├── models.py       (数据库表定义)                │    │
│  │  ├── auth.py         (认证 + JWT 中间件)           │    │
│  │  ├── task_api.py     (任务 CRUD API)               │    │
│  │  ├── user_api.py     (用户管理 API，管理员专属)     │    │
│  │  ├── init_db.py      (数据库初始化脚本)            │    │
│  │  └── task.db         (SQLite 数据库文件，自动生成) │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

**数据流**：

```
用户操作 → app.js (fetch) → Flask路由 → 认证中间件(解析JWT)
    → 权限检查(admin/user) → SQL查询(SQLite) → JSON响应
    → app.js (更新DOM)
```

### 1.4 数据库设计

#### ER 图

```
┌──────────────────┐         ┌──────────────────────────┐
│      users       │         │          tasks            │
├──────────────────┤         ├──────────────────────────┤
│ id (PK, AUTO)    │◄────────│ assigned_to (FK → users)  │
│ username (UNIQUE)│  分配    │ created_by  (FK → users)  │
│ password_hash    │◄────────│                          │
│ role (admin/user)│  创建    │ id (PK, AUTO)            │
│ created_at       │         │ title                    │
└──────────────────┘         │ description              │
                              │ status (todo/in_progress │
                              │         /done)           │
                              │ priority (low/medium/high)│
                              │ created_at               │
                              │ updated_at               │
                              └──────────────────────────┘
```

#### 建表 SQL

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
        CHECK(role IN ('admin', 'user')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo'
        CHECK(status IN ('todo', 'in_progress', 'done')),
    priority TEXT NOT NULL DEFAULT 'medium'
        CHECK(priority IN ('low', 'medium', 'high')),
    assigned_to INTEGER,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- 索引：加速按分配人查询
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status);
```

#### 预置数据

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| `admin` | `admin123` | admin | 管理员账号 |
| `testuser` | `test123` | user | 普通用户账号 |

### 1.5 API 设计

#### 认证接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/auth/register` | 用户注册 | 公开 |
| POST | `/api/auth/login` | 用户登录，返回 JWT | 公开 |

**POST /api/auth/login**

```json
// 请求体
{ "username": "admin", "password": "admin123" }
// 响应体
{
  "success": true,
  "token": "eyJhbGciOi...",
  "user": { "id": 1, "username": "admin", "role": "admin" }
}
```

#### 任务接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/tasks` | 获取任务列表 | 登录用户 |
| POST | `/api/tasks` | 创建任务 | 登录用户 |
| PUT | `/api/tasks/<id>` | 更新任务 | 登录用户 |
| DELETE | `/api/tasks/<id>` | 删除任务 | 仅管理员 |

**数据过滤规则**（核心权限逻辑）：

- 管理员执行 `GET /api/tasks` → `SELECT * FROM tasks`（看到所有任务）
- 普通用户执行 `GET /api/tasks` → `SELECT * FROM tasks WHERE assigned_to = <当前用户id>`
- 普通用户执行 `PUT /api/tasks/<id>` → 先检查 `assigned_to` 是否为当前用户，否则返回 403
- 普通用户执行 `DELETE /api/tasks/<id>` → 返回 403（禁止删除）

#### 用户管理接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/users` | 获取所有用户 | 仅管理员 |
| PUT | `/api/users/<id>/role` | 修改用户角色 | 仅管理员 |
| DELETE | `/api/users/<id>` | 删除用户及关联任务 | 仅管理员 |

### 1.6 权限模型

本项目通过**两层权限控制**来展示数据库权限概念：

#### 第一层：应用层 RBAC（Role-Based Access Control）

```
                    ┌──────────────┐
                    │   HTTP 请求    │
                    │ Authorization │
                    │ Bearer <JWT>  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  JWT 解析     │
                    │  提取: user_id│
                    │  username    │
                    │  role        │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  角色判断      │
                    │              │
                    │  admin ──► 全部数据 │
                    │  user  ──► 仅自己的数据 │
                    └──────────────┘
```

#### 第二层：数据库权限概念（教学讲解）

虽然 SQLite 不支持用户/角色级别的 GRANT，但本项目的 `models.py` 和 API 代码中详细注释了**如果使用 MySQL/PostgreSQL 应如何设置**：

```sql
-- 【教学参考】如果使用 MySQL，数据库层权限设置示例：

-- 创建应用访问账号（仅拥有基础 CRUD 权限）
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON minitask.tasks TO 'app_user'@'localhost';
GRANT SELECT ON minitask.users TO 'app_user'@'localhost';
-- 注意：app_user 不能 DELETE 任务（由应用层控制）
-- 注意：app_user 不能修改 users 表（密码字段保护）

-- 创建管理员账号（拥有全部权限）
CREATE USER 'app_admin'@'localhost' IDENTIFIED BY 'admin_strong_password';
GRANT ALL PRIVILEGES ON minitask.* TO 'app_admin'@'localhost';
```

这样学生既理解了**应用层 RBAC**（本项目实现），也了解了**数据库层 GRANT/REVOKE**（注释讲解）。

### 1.7 前端页面设计

#### 页面结构

```
┌──────────────────────────────────────────────────┐
│  MiniTask · 任务管理系统        [用户名] [退出]    │  ← 导航栏
├──────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 📋 待办   │  │ 🔄 进行中 │  │ ✅ 已完成 │        │  ← 看板三列
│  │          │  │          │  │          │        │
│  │ [任务卡] │  │ [任务卡] │  │ [任务卡] │        │
│  │ [任务卡] │  │          │  │ [任务卡] │        │
│  │          │  │          │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘        │
│                                                    │
│  [+ 新建任务]                          [管理用户]  │  ← 操作按钮
└──────────────────────────────────────────────────┘
```

#### 状态流转

```
     ┌─────────┐      ┌─────────────┐      ┌────────┐
     │  todo   │ ───► │ in_progress │ ───► │  done  │
     │  待办   │      │   进行中     │      │  已完成 │
     └─────────┘      └─────────────┘      └────────┘
          ▲                                       │
          └───────────────────────────────────────┘
                     （可回退到待办）
```

---

## 二、Prompt 序列（按步骤生成项目）

> **使用方法**：在 VSCode 中打开一个空文件夹（如 `D:\minitask\`），按顺序将以下 Prompt 发送给 Claude Code。每个 Prompt 生成完成后，检查代码，确认无误后继续下一个。
>
> **提示**：每个 Prompt 都标注了预计耗时和覆盖的知识点，方便教学节奏把控。

---

### Prompt 1：项目骨架初始化

**⏱ 预计耗时**：3 分钟  
**📘 覆盖知识点**：Flask 项目结构、虚拟环境、依赖管理

```
## 任务：初始化 MiniTask 项目骨架

请创建以下项目结构，这是一个 Flask + 原生前端 的简易任务管理系统：

### 目录结构
```
minitask/
├── backend/
│   └── app.py          # Flask 应用入口（基础骨架）
├── frontend/
│   ├── index.html      # 前端主页（先放一个 <h1>MiniTask</h1>）
│   ├── style.css       # 样式文件（空文件，后续填充）
│   └── app.js          # 前端逻辑（空文件，后续填充）
├── requirements.txt    # Python 依赖
└── README.md           # 项目说明
```

### 具体要求

1. **backend/app.py**：
   - 创建 Flask 应用
   - 配置 `flask-cors` 允许所有来源跨域
   - 添加一个 `GET /api/health` 健康检查路由，返回 `{"status": "ok"}`
   - 使用 `if __name__ == '__main__'` 启动，端口 5000，debug=True

2. **requirements.txt**：包含 flask、flask-cors、pyjwt、werkzeug

3. **README.md**：写清楚项目名称、简介、如何安装依赖（`pip install -r requirements.txt`）、如何启动后端（`python backend/app.py`）

4. 所有文件请用 `Write` 工具一次性创建完成。
```

**✅ 验证标准**：
```bash
pip install -r requirements.txt
python backend/app.py
# 浏览器访问 http://localhost:5000/api/health 看到 {"status":"ok"}
```

---

### Prompt 2：数据库模型与初始化脚本

**⏱ 预计耗时**：5 分钟  
**📘 覆盖知识点**：SQLite 表设计、外键、CHECK约束、索引、DEFAULT值、数据库初始化模式

```
## 任务：创建数据库模型和初始化脚本

基于已有的 `backend/app.py`，创建数据库相关文件。

### 1. 创建 `backend/models.py` —— 数据库操作层

请实现以下函数（使用 Python 内置 sqlite3 模块，数据库路径 `backend/task.db`）：

```python
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'task.db')

def get_db():
    """获取数据库连接。开启 WAL 模式提升并发性能。设置 row_factory 为 Row 以便用字典方式访问结果。"""
    pass  # TODO

def init_db():
    """创建 users 和 tasks 表，如果不存在的话。同时创建索引。"""
    pass  # TODO
```

#### 数据库表设计

**users 表**：
| 列名 | 类型 | 约束 |
|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | TEXT | NOT NULL UNIQUE |
| password_hash | TEXT | NOT NULL |
| role | TEXT | NOT NULL DEFAULT 'user' CHECK(role IN ('admin','user')) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**tasks 表**：
| 列名 | 类型 | 约束 |
|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| title | TEXT | NOT NULL |
| description | TEXT | DEFAULT '' |
| status | TEXT | NOT NULL DEFAULT 'todo' CHECK(status IN ('todo','in_progress','done')) |
| priority | TEXT | NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high')) |
| assigned_to | INTEGER | FOREIGN KEY → users(id) |
| created_by | INTEGER | NOT NULL, FOREIGN KEY → users(id) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

额外创建两个索引：
- `idx_tasks_assigned_to` ON tasks(assigned_to)
- `idx_tasks_status` ON tasks(status)

**重要——请在代码注释中标注**：
- 为什么 `password_hash` 不能存明文
- `CHECK` 约束的作用（数据库层面的数据完整性保障）
- 外键的作用（确保数据引用完整性）
- 如果使用 MySQL/PostgreSQL，数据库层面可以如何设置用户权限（如：创建一个仅有 SELECT,INSERT 权限的 app_user，和一个有 ALL PRIVILEGES 的 app_admin）——写在注释里即可

### 2. 创建 `backend/init_db.py` —— 数据库初始化脚本

```python
"""
数据库初始化脚本。
运行方式：python backend/init_db.py
功能：
1. 创建所有表
2. 插入默认用户：admin/admin123 (角色:admin) 和 testuser/test123 (角色:user)
3. 插入 3 条示例任务
"""
```

要求：
- 调用 models.py 中的 init_db() 创建表
- 检查是否已有数据（避免重复插入默认用户）
- 密码使用 `werkzeug.security.generate_password_hash()` 加密
- 插入 3 条示例任务（分配给不同用户、不同状态）

### 3. 修改 `backend/app.py`

- 导入 models 模块
- 在 `if __name__ == '__main__'` 之前调用 `models.init_db()` 确保表存在
```

**✅ 验证标准**：
```bash
python backend/init_db.py
# 输出：数据库初始化完成
# 使用 sqlite3 命令行检查 task.db 中是否有 users 和 tasks 表且有预置数据
```

---

### Prompt 3：用户认证系统

**⏱ 预计耗时**：4 分钟  
**📘 覆盖知识点**：JWT 令牌、密码哈希、认证装饰器、Bearer Token、HTTP 状态码

```
## 任务：实现用户认证系统

创建 `backend/auth.py`，实现完整的认证功能。

### 1. JWT 工具函数

```python
import jwt
import datetime

SECRET_KEY = 'minitask-secret-key-2024'  # 教学用固定密钥
TOKEN_EXPIRY_HOURS = 24

def generate_token(user_id, username, role):
    """生成 JWT token，payload 包含 user_id, username, role, exp"""
    pass

def verify_token(token):
    """验证并解析 JWT token，成功返回 payload 字典，失败返回 None"""
    pass
```

### 2. 认证装饰器 `@require_auth`

```python
from functools import wraps
from flask import request, g

def require_auth(f):
    """
    从请求头 Authorization: Bearer <token> 中提取 JWT 并验证。
    验证成功：将 user_id, username, role 存入 flask.g 对象
    验证失败：返回 401 {"success": false, "error": "未登录或token已过期"}
    """
    pass
```

### 3. 注册路由 POST `/api/auth/register`

- 接收 JSON：`{"username": "xxx", "password": "xxx"}`
- 校验：用户名长度 ≥ 3，密码长度 ≥ 6
- 检查用户名是否已存在（返回 409）
- 使用 `werkzeug.security.generate_password_hash()` 加密密码
- 默认角色为 `'user'`
- 返回 201：`{"success": true, "message": "注册成功"}`

### 4. 登录路由 POST `/api/auth/login`

- 接收 JSON：`{"username": "xxx", "password": "xxx"}`
- 查询用户是否存在（返回 401 "用户名或密码错误"——注意不要区分是用户不存在还是密码错误，防枚举攻击）
- 使用 `werkzeug.security.check_password_hash()` 验证密码
- 生成 JWT token
- 返回：`{"success": true, "token": "...", "user": {"id": 1, "username": "xxx", "role": "admin"}}`

### 5. 修改 `backend/app.py`

- 导入 auth 模块
- 注册 `/api/auth/register` 和 `/api/auth/login` 路由
- 添加 CORS 的 Authorization header 支持：
  ```python
  CORS(app, supports_credentials=True, expose_headers=['Authorization'])
  ```

### 重要注释要求
请在代码中添加注释说明：
- JWT 的三段结构（header.payload.signature）
- 为什么密码要哈希存储（参考：即使数据库泄露，攻击者也拿不到明文密码）
- Bearer Token 的规范格式
```

**✅ 验证标准**：
```bash
python backend/app.py
# 使用 curl 测试：
# curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'
# 应该返回 token 和 user 信息
#
# curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"wrong"}'
# 应该返回 401
```

---

### Prompt 4：任务 CRUD API

**⏱ 预计耗时**：5 分钟  
**📘 覆盖知识点**：RESTful API 设计、RBAC 权限制、SQL JOIN 查询、数据过滤、HTTP 状态码规范、403 vs 401

```
## 任务：实现任务 CRUD API（含权限控制）

创建 `backend/task_api.py`，这是项目的**核心教学模块**——展示了"不同角色看到不同数据"的完整实现。

### 1. GET /api/tasks —— 获取任务列表（带 JOIN + 权限过滤）

```python
@app.route('/api/tasks', methods=['GET'])
@require_auth
def get_tasks():
    """
    获取任务列表。

    【核心教学点——RBAC 数据过滤】：
    - 管理员：查询所有任务
    - 普通用户：仅查询 assigned_to = 自己的任务

    查询使用 INNER JOIN 连接 users 表，返回任务的创建者和执行者的用户名。

    支持可选的 ?status=todo 查询参数筛选。

    返回格式：
    {
      "success": true,
      "tasks": [
        {
          "id": 1,
          "title": "示例任务",
          "description": "...",
          "status": "todo",
          "priority": "high",
          "assigned_to": 2,
          "assigned_username": "testuser",
          "created_by": 1,
          "created_username": "admin",
          "created_at": "2024-01-01 00:00:00",
          "updated_at": "2024-01-01 00:00:00"
        }
      ]
    }
    """
```

**请务必在注释中写清楚**：
- 管理员走什么 SQL 分支，普通用户走什么 SQL 分支
- 为什么使用 JOIN 而不是两次查询（N+1 问题）
- 为什么用参数化查询而不是字符串拼接（SQL 注入防护）

### 2. POST /api/tasks —— 创建任务

- 任何登录用户都可以创建
- 接收：`{"title": "xxx", "description": "可选", "priority": "medium", "assigned_to": 2}`
- `created_by` 自动设置为当前用户（从 `g.user_id` 获取）
- 验证：title 不能为空
- 返回 201

### 3. PUT /api/tasks/<int:task_id> —— 更新任务

**【核心教学点——权限检查】**：
- 先查询任务是否存在（不存在返回 404）
- **普通用户**：检查 `assigned_to` 是否为当前用户，不是则返回 403 `{"error": "您只能修改分配给自己的任务"}`
- **管理员**：可以修改任何任务
- 支持更新：title, description, status, priority, assigned_to
- `updated_at` 自动更新为当前时间

### 4. DELETE /api/tasks/<int:task_id> —— 删除任务

- **仅管理员**可以删除
- 普通用户返回 403 `{"error": "仅管理员可以删除任务"}`
- 任务不存在返回 404

### 5. 修改 `backend/app.py`

- 导入 task_api 模块
- 注册所有任务路由（需要确保路由和认证装饰器正确搭配）

### 代码质量要求
- 所有 SQL 使用参数化查询（`?` 占位符），绝不拼接字符串
- 每个函数都有 docstring 说明权限规则
- 错误时返回一致的 JSON 格式：`{"success": false, "error": "具体错误信息"}`
```

**✅ 验证标准**：
```bash
# 1. 管理员登录 → 获取所有任务
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/tasks
# 应返回所有任务

# 2. 普通用户登录 → 只看到分配给自己的任务
TOKEN2=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -H "Authorization: Bearer $TOKEN2" http://localhost:5000/api/tasks
# 应仅返回 assigned_to=2 的任务

# 3. 普通用户尝试删除 → 应返回 403
curl -X DELETE -H "Authorization: Bearer $TOKEN2" http://localhost:5000/api/tasks/1
# 应返回 {"success":false,"error":"仅管理员可以删除任务"}
```

---

### Prompt 5：用户管理 API（管理员专属）

**⏱ 预计耗时**：3 分钟  
**📘 覆盖知识点**：级联删除、角色变更、更高级的权限检查、SQL 事务

```
## 任务：实现用户管理 API（仅管理员可访问）

创建 `backend/user_api.py`。

### 1. 管理员权限装饰器

在 `backend/auth.py` 中添加：

```python
def require_admin(f):
    """
    先调用 require_auth 认证，再检查 g.role 是否为 'admin'。
    不是管理员返回 403。
    """
    pass
```

### 2. GET /api/users —— 获取用户列表

```python
@app.route('/api/users', methods=['GET'])
@require_admin
def get_users():
    """
    返回所有用户（不含密码哈希）。
    返回格式：
    {
      "success": true,
      "users": [
        {"id": 1, "username": "admin", "role": "admin", "created_at": "..."},
        ...
      ]
    }
    """
```

### 3. PUT /api/users/<int:user_id>/role —— 修改用户角色

```python
@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@require_admin
def update_user_role(user_id):
    """
    修改用户角色。
    接收：{"role": "admin"} 或 {"role": "user"}
    注意：不允许将自己的角色改为 user（防止锁死）
    返回更新后的用户信息
    """
```

### 4. DELETE /api/users/<int:user_id> —— 删除用户（级联）

```python
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """
    删除用户。

    【教学点——级联删除】：
    使用事务（BEGIN...COMMIT）：
    1. 删除该用户创建的任务（created_by = user_id）
    2. 将分配给该用户的任务的 assigned_to 设为 NULL
    3. 删除用户本身

    如果任何一步失败，回滚事务。
    不允许删除自己。
    """
```

### 5. 修改 `backend/app.py`

- 导入 user_api 模块并注册路由

### 注释要求
- 说明 `require_admin` 和 `require_auth` 的区别和调用顺序
- 说明事务（BEGIN/COMMIT/ROLLBACK）在级联删除中的作用
- 为什么返回用户列表时要去掉 password_hash 字段
```

**✅ 验证标准**：
```bash
# 管理员获取用户列表
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:5000/api/users

# 普通用户尝试获取用户列表 → 403
curl -H "Authorization: Bearer $USER_TOKEN" http://localhost:5000/api/users
```

---

### Prompt 6：前端三件套（HTML + CSS + JS）

**⏱ 预计耗时**：7 分钟  
**📘 覆盖知识点**：Fetch API、JWT 管理（localStorage）、DOM 操作、事件委托、看板 UI、响应式布局

```
## 任务：创建前端页面

请创建/修改 frontend/ 目录下的三个文件，实现完整的任务管理系统界面。

### 设计风格
- 现代化简洁风格，配色以蓝白为主
- 移动端响应式（使用 CSS Grid / Flexbox）
- 任务卡片根据优先级显示不同颜色边框（高=红色，中=橙色，低=灰色）
- 合理的过渡动画和悬停效果

### 1. frontend/index.html

结构要求：
- 登录/注册区域（初始显示，未登录状态）
  - 用户名 + 密码输入框 + 登录按钮 + "没有账号？去注册"链接
  - 注册模式：用户名 + 密码 + 确认密码 + 注册按钮 + "已有账号？去登录"链接
- 主应用区域（登录后显示，初始隐藏）
  - 顶部导航栏：logo + 当前用户名 + 角色标签 + 退出按钮
  - 看板区域（三个状态列）：
    ```
    ┌─────────────────────────────────────────────┐
    │  📋 待办          🔄 进行中        ✅ 已完成 │
    │  ┌─────────┐    ┌─────────┐    ┌─────────┐ │
    │  │ 任务卡片 │    │ 任务卡片 │    │ 任务卡片 │ │
    │  │ - 标题   │    │ - 标题   │    │ - 标题   │ │
    │  │ - 优先级 │    │ - 优先级 │    │ - 优先级 │ │
    │  │ - 负责人 │    │ - 负责人 │    │ - 负责人 │ │
    │  └─────────┘    └─────────┘    └─────────┘ │
    └─────────────────────────────────────────────┘
    ```
  - 底部操作栏：+ 新建任务按钮 + 管理用户按钮（仅管理员可见）
- 新建/编辑任务的模态框
  - 标题输入、描述输入、优先级下拉、负责人下拉、状态下拉
- 用户管理模态框（仅管理员可见）
  - 用户列表表格 + 删除按钮 + 角色切换按钮
- 所有的 CSS 类名和 ID 命名要有清晰的语义

### 2. frontend/style.css

请实现完整的样式：

- **CSS 变量**：定义主色调、背景色、边框色、阴影等
  ```css
  :root {
    --primary: #3b82f6;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #10b981;
    --bg: #f8fafc;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --radius: 8px;
  }
  ```
- **登录表单**：居中卡片样式，圆角阴影
- **导航栏**：固定顶部，flexbox 布局
- **看板**：三列 CSS Grid 布局（移动端堆叠）
- **任务卡片**：白色背景、圆角、阴影、左侧彩色边框（按优先级）
- **模态框**：居中弹出，半透明遮罩
- **按钮**：主按钮、危险按钮、次要按钮三种样式
- **响应式**：屏幕宽度 < 768px 时看板堆叠为单列

### 3. frontend/app.js

这是前端的核心逻辑文件。请实现：

#### 全局状态管理
```javascript
const state = {
  token: localStorage.getItem('minitask_token') || null,
  user: JSON.parse(localStorage.getItem('minitask_user') || 'null'),
  tasks: [],
  users: []
};
```

#### API 请求封装
```javascript
async function api(path, options = {}) {
  // 自动添加 Authorization header
  // 自动处理 401（token 过期 → 跳转登录页）
  // 返回解析后的 JSON
}
```

#### 功能函数（每个都要完整实现）
- `login()` / `register()` —— 表单提交、存储 token、刷新界面
- `logout()` —— 清除 token、重置界面
- `loadTasks()` —— 调用 GET /api/tasks，按 status 分组渲染看板
- `renderBoard()` —— 将任务按 status 分成三列渲染
- `createTaskCard(task)` —— 生成单个任务卡片的 HTML
- `createTask()` / `updateTask()` / `deleteTask()` —— CRUD 操作
- `loadUsers()` —— 管理员加载用户列表
- `renderUserTable()` —— 渲染用户管理表格
- `changeUserRole()` / `deleteUser()` —— 用户管理操作
- `showModal()` / `hideModal()` —— 模态框控制
- `showMessage(text, type)` —— toast 提示（成功/错误/警告）

#### 事件绑定
- 页面加载时检查 token 是否已存在，存在则自动登录
- 所有按钮的点击事件
- 任务卡片的点击事件（打开编辑模态框）
- 模态框关闭事件（点击遮罩或关闭按钮）

### 关键交互细节
- 创建任务成功后，自动关闭模态框并刷新看板
- 编辑任务时，模态框预填当前数据
- 删除操作前弹出确认框 `confirm()`
- 错误时显示 toast 提示（红色）
- 成功操作显示 toast 提示（绿色）
- 所有 toast 3秒后自动消失
```

**✅ 验证标准**：
- 直接用浏览器打开 `frontend/index.html`（file:// 协议即可，CORS 已配置）
- 能用 admin/admin123 登录
- 看到三列看板
- 能创建、编辑任务
- 切换 testuser 账号，只能看到分配给自己的任务
- 普通用户尝试删除任务时看到 toast 错误提示

---

### Prompt 7：集成整合、测试与启动脚本

**⏱ 预计耗时**：3 分钟  
**📘 覆盖知识点**：项目集成、启动脚本、端到端测试、README 完善

```
## 任务：最终集成整合

请完成以下收尾工作：

### 1. 创建 `backend/run.py` 启动脚本

```python
"""
MiniTask 启动脚本
运行方式：python run.py
"""
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("  MiniTask 任务管理系统")
    print("  后端地址: http://localhost:5000")
    print("  前端页面: 用浏览器打开 frontend/index.html")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 2. 更新 `backend/app.py`

- 检查确认所有路由都已注册
- 确保 CORS 配置正确（允许 Authorization header）
- 确保在启动时自动调用 init_db()
- 添加全局错误处理器（404、500），返回统一 JSON 格式

### 3. 更新 `README.md`

完善 README，包含：
- 项目简介
- 技术栈说明
- 快速开始步骤（安装依赖 → 初始化数据库 → 启动后端 → 打开前端）
- 默认账号密码
- API 文档（所有接口的表格 + 请求/响应示例）
- 项目结构说明
- 权限设计说明
- 数据库 ER 图（文字版）

### 4. 全局检查

请逐一检查以下文件，确保没有遗漏或错误：
- [ ] backend/app.py —— 所有路由注册完整
- [ ] backend/models.py —— get_db(), init_db() 正确实现
- [ ] backend/auth.py —— JWT 生成/验证、require_auth 装饰器
- [ ] backend/task_api.py —— 4 个任务接口 + 完整的权限检查
- [ ] backend/user_api.py —— 3 个用户管理接口 + @require_admin
- [ ] backend/init_db.py —— 可独立运行，幂等（重复运行不报错）
- [ ] frontend/index.html —— 结构完整，API 路径正确
- [ ] frontend/style.css —— 响应式，三列看板布局正确
- [ ] frontend/app.js —— API 调用路径与后端路由匹配

### 5. 验证整个流程

在 README.md 末尾添加一个"端到端验证清单"章节：

```
## 端到端验证清单

1. [ ] python backend/init_db.py → 数据库初始化成功
2. [ ] python backend/run.py → 后端启动无报错
3. [ ] 浏览器打开 frontend/index.html
4. [ ] admin/admin123 登录 → 看到看板 + 用户管理按钮
5. [ ] testuser/test123 登录 → 只看到分配给自己的任务
6. [ ] 新建任务 → 出现在对应状态列
7. [ ] 点击任务卡片 → 编辑弹窗正常
8. [ ] 修改状态 → 任务移到对应列
9. [ ] 普通用户删除任务 → 403 toast 错误提示
10. [ ] 管理员删除任务 → 任务消失
11. [ ] 管理员查看用户列表 → 能看到所有用户
12. [ ] 管理员修改用户角色 → 生效
```
```

**✅ 最终验证**：
```bash
# 全新环境从零开始
pip install -r requirements.txt
python backend/init_db.py
python backend/run.py
# 浏览器打开 frontend/index.html
# 按照 README 中的"端到端验证清单"逐项检查
```

---

## 三、运行与验证

### 快速开始（学生版本）

```bash
# Step 1: 安装依赖
cd minitask
pip install -r requirements.txt

# Step 2: 初始化数据库（创建表 + 插入示例数据）
python backend/init_db.py

# Step 3: 启动后端
python backend/run.py

# Step 4: 打开前端
# 方式一：直接用浏览器打开 frontend/index.html
# 方式二：用 Python 启动一个简单的 HTTP 服务器
#   cd frontend && python -m http.server 8080
#   然后访问 http://localhost:8080
```

### 默认账号

| 角色 | 用户名 | 密码 | 权限范围 |
|------|--------|------|----------|
| 管理员 | `admin` | `admin123` | 全部任务 + 用户管理 |
| 普通用户 | `testuser` | `test123` | 仅自己名下的任务 |

### 接口速查

```bash
# 登录获取 token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取任务（管理员 = 全部，用户 = 仅自己的）
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/tasks

# 创建任务
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"新任务","priority":"high","assigned_to":2}'

# 更新任务状态
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"status":"done"}'

# 删除任务（仅管理员）
curl -X DELETE -H "Authorization: Bearer <token>" http://localhost:5000/api/tasks/1

# 用户管理（仅管理员）
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/users
```

---

## 四、扩展思考题

完成项目后，可以让学生思考以下问题（巩固知识）：

### 基础

1. **SQL 注入**：如果 `task_api.py` 中使用字符串拼接 SQL（如 `f"SELECT * FROM tasks WHERE id = {task_id}"`），会有什么风险？给出一个具体的攻击示例。
2. **密码存储**：为什么存储 `password_hash` 而不是明文密码？`generate_password_hash` 和 `hashlib.md5` 有什么区别？
3. **401 vs 403**：用户未登录访问 `/api/tasks` 返回 401，普通用户尝试删除任务返回 403。这两个状态码的设计逻辑是什么？

### 进阶

4. **Token 刷新**：当前 JWT token 24小时过期。如何设计一个 token 刷新机制（refresh token）？
5. **数据库迁移**：如果新版本需要在 tasks 表增加一个 `due_date` 字段，如何在不丢失数据的情况下修改表结构？
6. **前后端分离部署**：如果要把前端部署到 Nginx、后端部署到 Gunicorn，需要什么配置？CORS 配置需要改吗？
7. **数据库权限**：如果从 SQLite 迁移到 MySQL，如何设置两个数据库账号（`app_reader` 只读、`app_writer` 读写），为应用层提供额外的安全保障？

### 实战

8. **新增功能**：尝试为系统添加"任务评论"功能。需要修改哪些文件？新增哪些 API？数据库表如何设计？
9. **性能优化**：如果 tasks 表有 100 万条记录，`GET /api/tasks` 会变慢。你会如何优化（索引、分页、缓存）？
10. **安全审计**：尝试找到一个你之前没注意到的安全问题（提示：XSS、CSRF、密码强度、输入校验），并修复它。

---

## 附录：教学节奏建议

| 环节 | 内容 | 时间 |
|------|------|------|
| **讲解设计** | 讲师讲解项目架构、数据库设计、权限模型 | 10 分钟 |
| **Prompt 1** | 初始化项目骨架 | 3 分钟 |
| **Prompt 2** | 数据库模型 + init_db | 5 分钟 |
| **Prompt 3** | 用户认证系统 | 4 分钟 |
| **Prompt 4** | 任务 CRUD API（重点） | 5 分钟 |
| **Prompt 5** | 用户管理 API | 3 分钟 |
| **Prompt 6** | 前端三件套 | 7 分钟 |
| **Prompt 7** | 集成整合 | 3 分钟 |
| **验证测试** | 端到端测试 + 调试 | 5 分钟 |
| **总结讨论** | 扩展思考题讨论 | 10 分钟 |
| **合计** | | **~55 分钟** |

> 纯 Prompt 执行约 30 分钟，加讲解和讨论约一节课（55 分钟）。

---

> **文档版本**：v1.0  
> **最后更新**：2026-08-12  
> **适用于**：Claude Code + VSCode 教学场景
