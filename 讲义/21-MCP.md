# 第7周 第3课：MCP —— AI 的 USB-C 接口

> **本课面向双轨受众**：💼 企业管理者/投资人 + 🎓 零基础学习者。正文为核心AI知识，📊「企业视角」框提供商业战略洞见。

---

## 一、课程信息

| 项目 | 内容 |
|------|------|
| **课程编号** | 第7周 第3课（总第21课） |
| **课程主题** | MCP（Model Context Protocol）—— AI 的 USB-C 接口 |
| **课程时长** | 2 小时（50 分钟讲解 + 70 分钟实操） |
| **所属模块** | 第7周：Agent 工具与协议 |
| **前置知识** | Agent 基本概念与循环（第7周第1课）、主流 Agent 框架概述（第7周第2课） |
| **课程定位** | 在理解 Agent 和框架之后，学习 Agent 连接外部工具与数据的标准协议 —— 这是让 Agent 从小白变成能干活的生产力工具的关键一课 |
| **教学对象** | 已掌握 Agent 基础概念，了解至少一种 Agent 框架（如 Claude Code、LangGraph、OpenAI Agents SDK）的学生 |

> **本节寄语**：前面两课你已经理解了 Agent 是什么，也了解了框架如何组织 Agent。但一个只会"空想"的 Agent 是没用的。这节课你要学的是，如何用 MCP 这个标准协议，让 Agent 能够真正地读写文件、搜索网络、查询数据库、操作 GitHub —— 就像一个没有接口的电脑什么都插不进去，MCP 就是给 AI 装上了通用接口。

---

## 二、学习目标

**💼 企业决策者**：
- 理解 MCP 对企业 AI 集成的战略意义——统一接口降低集成成本，消除供应商锁定风险
- 掌握 MCP 企业采纳的时间线和投资决策逻辑
- 建立"MCP兼容"的采购标准意识——未来选择企业软件时 MCP 兼容将成为刚需
- 理解 MCP + Skills 的组合如何实现 AI 能力的"一次开发、全公司复用"

---

通过本节课的学习，学生应能够：

| 序号 | 目标 | 具体描述 |
|------|------|----------|
| 1 | **理解 MCP 的核心价值** | 能用自己的话向别人解释 MCP 是什么，为什么被称为"AI 的 USB-C 接口"，以及 MxN 集成问题和 M+N 解决方案的区别 |
| 2 | **掌握 MCP 架构** | 能画出 MCP Host / Client / Server 三层架构图，说明 JSON-RPC 通信机制和连接生命周期 |
| 3 | **区分 MCP 三大能力** | 能准确区分 Tools（模型控制）、Resources（应用控制）、Prompts（用户选择）三种能力的角色和使用场景 |
| 4 | **独立配置 MCP Server** | 能在 Claude Code 中完成 Filesystem MCP 和 Fetch MCP 的完整配置、验证和测试 |
| 5 | **理解三大协议的关系** | 能说清 MCP、A2A、ACP 分别解决什么问题，以及三者如何构成 AI 协议栈 |
| 6 | **编写 MCP 模式代码** | 能用 Python 编写一个最小 MCP 风格的工具注册与调用系统，理解协议的核心模式 |

---

## 三、课前准备

### 3.1 软件与环境

| 准备事项 | 说明 |
|----------|------|
| **Node.js 18+** | MCP Server 的运行环境。检查命令：`node --version`。如未安装，访问 https://nodejs.org 下载 LTS 版本 |
| **Claude Code** | 本课主要实操平台。安装命令：`npm install -g @anthropic-ai/claude-code`。也可使用 Cursor / Continue 等支持 MCP 的工具替代 |
| **GitHub 账号** | 用于获取 GitHub Personal Access Token（实操2需要）。注册地址：https://github.com |
| **uvx（推荐）** | Python 项目快速运行工具，部分 MCP Server 需要。安装：`pip install uv` 或 `npm install -g uv` |
| **网络环境** | 确保能访问 npm registry 和 GitHub |

### 3.2 知识准备

| 准备事项 | 说明 |
|----------|------|
| **JSON 基础** | 理解 JSON 的键值对结构和基本语法规则（花括号、引号、逗号） |
| **命令行基础** | 能在终端中运行 `node`、`npx`、`cd` 等基本命令 |
| **Agent 概念回顾** | 回顾第7周第1课的内容：Agent = LLM + 工具 + 循环决策。MCP 解决的就是"工具"这一环的标准化问题 |

### 3.3 课前检查清单

- [ ] `node --version` 输出 v18.0.0 或更高
- [ ] `npx --version` 正常工作
- [ ] `claude --version` 或 IDE 中 AI 工具已就绪
- [ ] 理解 Agent 基本循环（observe -> think -> act -> observe）

---

## 四、核心知识点详解

---

### 4.1 MCP 是什么？—— AI 的 USB-C 接口

#### 4.1.1 先理解问题：MxN 集成噩梦

假设你要用 AI 做以下事情：读写本地文件、搜索网页、查询数据库、管理 GitHub 仓库。在没有 MCP 之前，每款 AI 应用都要**单独为每个工具写一套对接代码**。这就是经典的 **MxN 集成问题**：

```
没有 MCP 的世界（MxN 集成噩梦）：

Claude Desktop ──→ [自定义代码A] ──→ GitHub
Claude Desktop ──→ [自定义代码B] ──→ 数据库
Claude Desktop ──→ [自定义代码C] ──→ 文件系统
Claude Desktop ──→ [自定义代码D] ──→ 搜索引擎

Cursor ──────────→ [另一套代码E] ──→ GitHub
Cursor ──────────→ [另一套代码F] ──→ 数据库
Cursor ──────────→ [另一套代码G] ──→ 文件系统

Codex ───────────→ [又一套代码H] ──→ GitHub
Codex ───────────→ [又一套代码I] ──→ 数据库

结论：3个AI应用 x 4个工具 = 12套代码。每增加一个AI应用或一个工具，
     工作量呈乘法级增长。
```

**生活类比**：这就像你的笔记本电脑、台式机、平板，每台都需要各自品牌的专用鼠标、专用键盘、专用U盘 —— 换了设备就得全套换外设。

#### 4.1.2 MCP 的解决方案：M+N 标准化

有了 MCP 之后，所有 AI 应用通过**一个统一协议**连接所有工具：

```
有了 MCP 的世界（M+N 标准化）：

                   ┌── MCP 协议 ──→ GitHub MCP Server
Claude Desktop ────┤
                   ├── MCP 协议 ──→ 数据库 MCP Server
Cursor ────────────┤
                   ├── MCP 协议 ──→ 文件系统 MCP Server
Codex ─────────────┤
                   └── MCP 协议 ──→ 搜索引擎 MCP Server

结论：3个AI应用 + 4个工具 = 只需4个MCP Server。
     每增加一个AI应用，成本几乎为零。
```

**生活类比**：USB-C 标准的出现，让同一根线可以连接手机、笔记本、平板、显示器。你买一个 USB-C 设备，它可以插在任何支持 USB-C 的电脑上。**MCP 就是 AI 世界的 USB-C**。

#### 4.1.3 MCP 的严格定义

**MCP（Model Context Protocol，模型上下文协议）** 是由 Anthropic 于 2024 年 11 月发布的开放标准协议，用于在 AI 应用和外部工具/数据源之间建立标准化的通信通道。

| 对比维度 | 传统集成方式 | MCP 方式 |
|----------|-------------|---------|
| **集成关系** | M x N（每个 AI 应用 x 每个工具） | M + N（AI 应用 + 工具） |
| **开发成本** | 每次集成都需要重新开发 | 一次开发，到处复用 |
| **兼容性** | 各平台互不兼容 | 开放标准，跨平台通用 |
| **安全性** | 安全边界模糊，各管各的 | 统一权限模型，精细控制 |
| **维护成本** | 每个集成都需要独立维护 | 社区共建，生态共享 |
| **生态效应** | 孤岛式，各自为战 | 网络效应，越多人用越强 |

> 📊 **企业视角：MCP = AI 时代的 USB-C 接口 —— 企业的战略级基础设施**
>
> 如果 MCP 成为行业标准（趋势已经非常明确——2025年12月MCP已捐给Linux基金会，OpenAI/Google/Microsoft表态支持），企业所有内部工具（CRM/ERP/数据库/文件系统/邮件）都可以通过统一接口让 AI 调用。这意味着三个重大变化：
>
> **1. AI 集成成本降低 80%**
> - 传统方式：每接入一个AI应用（Claude Code/Cursor/Windsurf/自定义App），需要为每个内部工具单独开发对接代码。M×N的乘法成本。
> - MCP 方式：每个内部工具只需要开发一个 MCP Server，所有 AI 应用都能复用。M+N的加法成本。
> - 案例：一个中型企业有5个内部工具（CRM+ERP+OA+数据库+文件服务器），使用3种AI应用。传统集成需要15套对接代码，MCP只需5个Server。
>
> **2. 消除 AI 模型供应商锁定**
> - MCP Server 与 AI 模型完全解耦——你从 Claude 换成 DeepSeek 或通义千问，之前配置的所有 MCP Server 继续工作，零迁移成本。
> - 这意味着企业可以灵活切换模型供应商，利用竞争压低API成本。
>
> **3. "MCP 兼容"将成为企业软件采购的刚需**
> - 2026年开始，采购CRM/ERP/OA等企业软件时，"是否支持MCP"应该成为评估标准之一——像现在评估"是否有API"一样基本。
> - 不支持MCP的软件 = 不能被AI调用 = 数据孤岛 = 未来需要额外集成成本。

#### 4.1.4 MCP 的发展里程碑

| 时间 | 事件 | 意义 |
|------|------|------|
| **2024年11月** | Anthropic 发布 MCP 1.0 规范 | 开创 AI 工具标准化先河 |
| **2025年3月** | 引入 Streamable HTTP 传输 | 废弃旧 SSE 传输，支持远程部署 |
| **2025年11月** | 发布 2025-11-25 版本 | 当前最新稳定版规范 |
| **2025年12月9日** | MCP 捐赠给 Linux 基金会下的 AAIF | 从"Anthropic 的协议"升级为**行业标准**；OpenAI、Google DeepMind、Microsoft 等巨头表态支持 |

> **关键理解**：MCP 不是 Anthropic 的私有协议了。它现在是 Linux 基金会下的开放标准，就像 Kubernetes、Node.js 一样。这意味着你可以放心学习，不用担心被一家公司绑定。

---

### 4.2 MCP 架构详解

#### 4.2.1 三层架构

MCP 的架构设计遵循清晰的**三层分离**原则：

```
┌─────────────────────────────────────────────────┐
│                  MCP Host（宿主应用）              │
│   Claude Desktop / Claude Code / Cursor /        │
│   VS Code + Continue / Zed / Codex / 自定义App    │
├─────────────────────────────────────────────────┤
│                MCP Client（协议客户端）             │
│   嵌入在 Host 内部，负责：                         │
│   · 连接管理  · 消息路由  · 生命周期管理            │
│   · 能力发现  · 安全控制  · 协议编解码              │
├─────────────────────────────────────────────────┤
│           JSON-RPC over STDIO / HTTP              │
│               （通信通道）                         │
├─────────────────────────────────────────────────┤
│             MCP Server（功能服务器）                │
│   · filesystem  · github  · postgres             │
│   · puppeteer   · memory  · brave-search         │
│   · 你的自定义 Server ...                         │
└─────────────────────────────────────────────────┘
```

**三层角色一句话总结**：

| 层次 | 角色 | 生活类比 |
|------|------|----------|
| **MCP Host** | AI 应用本身，用户直接与之交互 | 你的笔记本电脑 |
| **MCP Client** | Host 内部的协议管理器，负责"翻译"和"路由" | 电脑里的 USB 控制器芯片 |
| **MCP Server** | 提供具体能力的轻量程序 | USB 设备（U盘、键盘、摄像头） |

#### 4.2.2 通信机制：JSON-RPC

MCP 的客户端和服务器之间使用 **JSON-RPC 2.0** 协议通信。所有消息都是 JSON 格式，结构清晰、人类可读。

**三种消息类型**：

**(1) 请求（Request）**—— 客户端发起调用：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/home/user/document.txt"
    }
  }
}
```

**(2) 响应（Response）**—— 服务器返回结果：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "这是文件的内容..."
      }
    ]
  }
}
```

**(3) 通知（Notification）**—— 单向消息，无需回复：

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "token-123",
    "progress": 50,
    "total": 100
  }
}
```

> **特点**：请求有 `id` 字段用于匹配响应；通知没有 `id`，发完即止，不需要对方回复。

#### 4.2.3 两种传输方式

| 特性 | STDIO（标准输入输出） | Streamable HTTP |
|------|----------------------|-----------------|
| **部署位置** | 必须与 Host 在同一台机器 | 可以在远程服务器 |
| **网络需求** | 无 | 需要 HTTP 连接 |
| **性能** | 最优（进程内通信） | 有网络开销 |
| **安全性** | 进程级隔离，天然安全 | 需要额外认证机制 |
| **适用场景** | 本地工具（文件系统、数据库） | 团队共享服务、云端工具 |
| **多客户端** | 不支持（一对一） | 支持（一对多） |

> **经验法则**：操作本地文件的工具用 STDIO，需要团队共享或远程访问的服务用 HTTP。

#### 4.2.4 连接生命周期

MCP 的每次连接遵循标准的三阶段生命周期：

```
阶段1：初始化（Initialization）
  Host 启动 MCP Server 进程
  Client → Server: initialize 请求（声明客户端能力）
  Server → Client: initialize 响应（声明服务器能力）
  Client → Server: initialized 通知（握手完成）

阶段2：操作（Operation）
  Client → Server: tools/list（获取可用工具列表）
  Client → Server: tools/call（调用具体工具）
  Server → Client: 返回结果或错误
  Client → Server: resources/read（读取资源）
  Server → Client: 流式进度通知（可选）

阶段3：关闭（Shutdown）
  Client 或 Server 发起关闭
  Server 清理资源（关闭文件句柄、断开数据库连接等）
  进程退出
```

> **关键点**：MCP Server 不需要常驻后台。Claude Code 等 Host 会在需要时自动启动 Server，任务完成后自动关闭。配置 10 个 Server 但只用 1 个，不会有额外性能开销。

---

### 4.3 MCP Server 三大能力

MCP Server 提供三种不同类型的交互方式，分别由不同角色主动发起：

```
能力类型对比：

  Tools（工具）          Resources（资源）        Prompts（提示模板）
  ─────────────────     ──────────────────      ──────────────────
  模型主动调用           应用主动暴露             用户主动选择
  LLM decides           App decides             User selects
  
  "让AI去操作"           "给AI看数据"             "帮用户表达"
  
  例：write_file()      例：数据库 Schema        例："代码审查"
  例：search_web()      例：项目文档              例："总结本文档"
  例：create_issue()    例：API 参考              例："生成发布说明"
```

#### 4.3.1 Tools（工具）—— 模型控制

**定义**：Tools 是 MCP Server 暴露给 AI 模型的可调用函数。模型根据上下文自主判断是否需要调用、何时调用、传什么参数。

**工具定义示例**（Server 向 Client 声明自己有哪些工具）：

```json
{
  "name": "read_file",
  "description": "读取指定路径的文件内容。仅在需要查看文件内容时使用。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "要读取的文件的绝对路径"
      }
    },
    "required": ["path"]
  }
}
```

**关键特征**：
- 由 **模型（LLM）决定** 何时调用哪个工具
- 每个工具都有严格的 `inputSchema` 定义输入格式
- 工具描述质量直接影响模型的使用效果 —— 描述写得好，模型用得对
- 这是 MCP 最核心的使用模式，90% 以上的 MCP 交互都是 Tool 调用

#### 4.3.2 Resources（资源）—— 应用控制

**定义**：Resources 是 MCP Server 暴露给 AI 应用的**只读数据**。与工具不同，资源的使用由**应用程序**控制，而不是模型决定。

**资源定义示例**：

```json
{
  "uri": "postgres://database/schema/users",
  "name": "Users 表结构",
  "description": "用户表的完整 schema 定义",
  "mimeType": "application/json"
}
```

**典型场景**：
- 数据库 MCP Server 把表结构作为 Resource 暴露，AI 可以随时查阅表结构
- 文档 MCP Server 把项目文档作为 Resource，AI 可以直接引用
- 配置 MCP Server 把系统配置作为 Resource，AI 可以读取但不能修改

> **区分 Tool vs Resource**：Tool = AI 可以**执行操作**（写文件、创建 Issue）；Resource = AI 可以**读取数据**（看表结构、查文档）。前者是动作，后者是数据。

#### 4.3.3 Prompts（提示模板）—— 用户选择

**定义**：Prompts 是 MCP Server 提供的**预设提示词模板**，由用户主动选择使用。它帮助用户标准化与 AI 的交互方式。

**提示模板定义示例**：

```json
{
  "name": "code_review",
  "description": "对指定代码进行结构化审查，输出问题分类和改进建议",
  "arguments": [
    {
      "name": "code",
      "description": "需要审查的代码片段",
      "required": true
    },
    {
      "name": "language",
      "description": "编程语言",
      "required": false
    }
  ]
}
```

**典型场景**：
- "Summarize this document" —— 自动生成文档摘要
- "Code review this file" —— 对代码进行系统性审查
- "Generate release notes" —— 从 commit 历史生成发布说明

> **三类能力定位总结**：Tools 像工具箱里的锤子螺丝刀（AI 自己拿），Resources 像书架上的参考书（AI 可以翻阅），Prompts 像标准表格模板（用户选好用哪个）。

---

### 4.4 常见 MCP Server 详解

本节逐一介绍最常用、最值得学习的 MCP Server。每个 Server 都给出功能说明、配置示例和典型用例。

#### 4.4.1 Filesystem（文件系统）—— 最基础、最必学

**功能**：在允许的目录范围内进行文件读写操作。所有其他 MCP 能力的基石。

**为什么第一个学它**：不需要任何 API Key，配置最简单，效果最直观。

**提供的工具**：

| 工具名 | 功能 | 典型用途 |
|--------|------|----------|
| `read_file` | 读取文件内容 | AI 查看代码、配置、文档 |
| `write_file` | 写入/创建文件 | AI 生成代码文件、创建配置 |
| `edit_file` | 编辑文件（基于 diff） | AI 修改代码片段 |
| `list_directory` | 列出目录内容 | AI 了解项目结构 |
| `search_files` | 按模式搜索文件 | AI 查找特定文件 |
| `get_file_info` | 获取文件信息 | AI 检查文件大小、修改时间 |

**配置示例**（`.mcp.json`）：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src", "./docs"],
      "env": {}
    }
  }
}
```

> **安全提示**：`args` 最后列出的路径是允许访问的目录。AI 无法访问这些目录之外的任何文件。**永远不要把 `/` 或 `C:\` 作为允许目录**。

**典型对话示例**：

```
用户：帮我看看 src 目录下有哪些 Python 文件
AI：[调用 filesystem.search_files，搜索 "*.py"] 找到 3 个文件：main.py, utils.py, config.py

用户：读取 utils.py 的内容，看看有没有 Bug
AI：[调用 filesystem.read_file("/project/src/utils.py")] 我来分析这段代码...
```

#### 4.4.2 GitHub —— 仓库管理全能

**功能**：完整的 GitHub 仓库管理能力，包括 Issue、PR、代码搜索、文件操作等。

**配置步骤**：

**Step 1：获取 Personal Access Token**

1. 登录 GitHub.com -> 右上角头像 -> Settings
2. 左侧菜单最下方 -> Developer settings
3. Personal access tokens -> Tokens (classic) -> Generate new token (classic)
4. 勾选权限：`repo`（必选）、`workflow`（可选，用于 Actions）
5. 点击 Generate token，**立即复制保存**（Token 只显示一次！）

**Step 2：设置环境变量**

Windows PowerShell：
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_你的Token内容', 'User')
```

macOS / Linux：
```bash
echo 'export GITHUB_TOKEN="ghp_你的Token内容"' >> ~/.zshrc
source ~/.zshrc
```

**Step 3：配置 MCP**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**核心工具一览**：

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `create_issue` | 创建 Issue | AI 自动记录 Bug、提交功能需求 |
| `create_pull_request` | 创建 PR | AI 提交代码变更请求 |
| `search_code` | 搜索代码 | AI 在仓库中查找特定实现 |
| `get_file_contents` | 读取文件 | AI 查看仓库代码 |
| `create_repository` | 创建仓库 | AI 初始化新项目 |
| `fork_repository` | Fork 仓库 | AI 帮助贡献开源项目 |
| `create_branch` | 创建分支 | AI 为功能开发创建分支 |

**典型对话示例**：

```
用户：帮我在 jjyaoao/HelloAgents 仓库创建一个 Issue，
     标题是"添加 MCP 集成文档"，描述用中文
AI：[调用 github.create_issue] Issue 创建成功！
    链接：https://github.com/jjyaoao/HelloAgents/issues/42
```

#### 4.4.3 PostgreSQL / SQLite —— 数据库直连

**功能**：让 AI 直接查询和操作数据库，把数据库能力变成 Agent 的原生能力。

**SQLite 配置**（本地数据库，适合学习和小型项目）：

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"],
      "env": {}
    }
  }
}
```

**PostgreSQL 配置**（生产数据库）：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/mydb"],
      "env": {}
    }
  }
}
```

> **安全最佳实践**：生产环境使用只读数据库用户，不要给 AI 写权限。连接字符串中的密码使用环境变量注入：`"postgresql://${PGUSER}:${PGPASSWORD}@localhost:5432/database"`

**典型对话示例**：

```
用户：users 表里有多少条注册记录？
AI：[调用 postgres.query "SELECT COUNT(*) FROM users"]
    共有 12,847 条注册记录。

用户：帮我查一下最近7天新增的用户里，来自北京的有多少？
AI：[调用 postgres.query "SELECT COUNT(*) FROM users WHERE created_at > ..."]
    近7天新增 342 人，其中北京地区 56 人，占比 16.4%。
```

#### 4.4.4 Brave Search —— 联网搜索

**功能**：通过 Brave 搜索引擎进行网页搜索，让 AI 获取最新网络信息（解决训练数据截止日期问题）。

**获取 API Key**：
1. 访问 https://brave.com/search/api/
2. 注册账号并创建 API Key
3. 免费层：每月 2000 次查询

**配置**：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

#### 4.4.5 Puppeteer —— 浏览器自动化

**功能**：无头浏览器自动化 —— 截图网页、填写表单、提取动态页面数据、自动化测试。

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "env": {}
    }
  }
}
```

#### 4.4.6 Fetch —— 获取网页内容

**功能**：获取任意 URL 的网页内容并转换为 Markdown 格式，方便 AI 分析和总结。

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {}
    }
  }
}
```

#### 4.4.7 Memory —— 持久化记忆

**功能**：让 AI 在跨会话之间记住信息 —— 你的偏好、项目背景、常用设置。

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
```

> **使用场景**：让 AI 记住"我喜欢用中文回复"、"这个项目使用 React 19 + TypeScript"、"数据库连接地址是 xxx"等上下文信息，下次对话自动加载。

#### 4.4.8 服务器分类速查

| 分类 | Server | 运行时 | 需要 API Key | 必学程度 |
|------|--------|--------|:-----------:|:-------:|
| **文件** | filesystem | npx (Node) | 否 | 必须 |
| **版本控制** | github | npx (Node) | 是 | 必须 |
| **数据库** | sqlite | uvx (Python) | 否 | 推荐 |
| **数据库** | postgres | npx (Node) | 否 | 推荐 |
| **搜索** | brave-search | npx (Node) | 是 | 推荐 |
| **网络** | fetch | uvx (Python) | 否 | 推荐 |
| **记忆** | memory | npx (Node) | 否 | 推荐 |
| **浏览器** | puppeteer | npx (Node) | 否 | 可选 |
| **推理** | sequential-thinking | npx (Node) | 否 | 可选 |

---

> 📊 **企业视角：MCP 采纳时间线与投资策略**
>
> **企业 MCP 成熟度路线图**：
>
> | 阶段 | 时间 | 关键动作 | 投入 | 预期回报 |
> |------|------|---------|:---:|---------|
> | **Level 1: 探索** | 1-2周 | 选1-2个非核心场景，配置Filesystem+Github MCP试水 | ¥0（使用社区免费Server） | 团队理解MCP概念 |
> | **Level 2: 试点** | 1-3个月 | 在1个核心业务场景部署MCP（如：客服系统对接知识库MCP） | ¥1-5万（人力投入为主） | 该场景效率提升30-50% |
> | **Level 3: 推广** | 3-6个月 | 为3-5个核心内部工具开发MCP Server，形成内部MCP工具库 | ¥5-20万（含开发人力） | 全部门AI效率跃升 |
> | **Level 4: 生态化** | 6-12个月 | MCP Server超过10个，建立内部MCP治理规范；"MCP兼容"纳入采购标准 | ¥20-50万（含治理体系建设） | AI成为企业基础设施 |
>
> **2026-2027年投资优先级建议**：
> 1. **立即投入**：为最核心的2-3个数据源（数据库/文件系统/CRM）开发MCP Server——这些是所有AI应用都会需要的
> 2. **6个月内**：建立企业内部MCP Server目录和治理规范（谁可以发布Server、安全审查流程、版本管理）
> 3. **12个月内**：推动所有新采购的企业软件必须具备MCP或标准API——从现在开始在采购合同中加入相关条款

### 4.5 MCP 配置实操

#### 4.5.1 三种配置作用域

MCP 支持三个级别的作用域，理解这个体系对安全使用 MCP 至关重要：

| 作用域 | 存储位置 | 优先级 | 适用场景 | 是否进入 Git |
|--------|----------|:------:|----------|:-----------:|
| **Local** | `~/.claude.json` 中的项目条目 | 最高 | 含 API Key 的个人配置 | 否 |
| **Project** | 项目根目录 `.mcp.json` | 中 | 团队共享的工具声明 | 是 |
| **User** | `~/.claude.json` 全局部分 | 最低 | 个人在所有项目中常用的工具 | 否 |

**优先级合并规则**：`Local > Project > User`（同一个 Server 在三处都有配置时，Local 生效）

**选择建议**：

| 场景 | 推荐作用域 | 原因 |
|------|-----------|------|
| 包含 API 密钥 | **Local** | 不会提交到 Git，安全 |
| 团队必需的工具 | **Project** | 提交到仓库，团队成员开箱即用 |
| 个人通用工具 | **User** | 所有项目自动可用 |
| CI/CD 自动化 | **Project** | 方便自动化部署 |

#### 4.5.2 完整配置步骤：Filesystem MCP

这是一个从零到一的完整配置示范，确保每个同学都能跑通：

**Step 1：创建项目目录并进入**

```bash
mkdir mcp-demo
cd mcp-demo
```

**Step 2：创建 `.mcp.json` 配置文件**

在项目根目录创建 `.mcp.json` 文件（注意文件名以点开头），写入：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    }
  }
}
```

**Step 3：验证配置文件存在**

```bash
# 查看文件内容
cat .mcp.json
# 应该看到上面的 JSON 内容
```

**Step 4：启动 Claude Code**

```bash
claude
```

启动时会看到类似输出：

```
MCP servers connected:
  ✓ filesystem (6 tools available)
```

> **关键确认**：看到绿色的 `✓ filesystem` 表示 MCP 连接成功！

**Step 5：测试工具调用**

在 Claude Code 中输入：

```
列出当前目录下的所有文件
```

预期 AI 会调用 `filesystem.list_directory` 工具并返回目录列表。

**进一步测试**：

```
读取 .mcp.json 的内容
```

```
创建一个 hello.txt 文件，内容是 "Hello from MCP!"
```

#### 4.5.3 配置 GitHub MCP（含 Token）

按 4.4.2 节的三个步骤操作。完成 Steps 1-3 后：

**Step 4：重启 Claude Code 并测试**

```
你：查看我的 GitHub 仓库列表
你：在 [你的仓库] 创建一个 Issue，标题是"MCP 测试"
```

#### 4.5.4 验证与排查

**完整验证清单**：
- [ ] `.mcp.json` 文件存在于项目根目录，JSON 格式正确
- [ ] Claude Code 启动时显示 MCP Server "已连接"（绿色对勾）
- [ ] 能成功调用 `list_directory`（列出文件）
- [ ] 能成功调用 `read_file`（读取文件内容）
- [ ] 能在允许目录内成功调用 `write_file`（创建文件）

**常见问题快速排查**：

| 症状 | 可能原因 | 解决方法 |
|------|----------|----------|
| 启动时不显示 MCP 连接 | 文件路径不对 | 确认 `.mcp.json` 在项目根目录，文件名以点开头 |
| `SyntaxError` | JSON 格式错误 | 使用 https://jsonlint.com 验证 JSON |
| `server failed to start` | Node.js 版本过低 | 升级到 Node.js 18+ |
| `ETIMEDOUT` | 无法访问 npm | 配置国内镜像：`npm config set registry https://registry.npmmirror.com` |
| 环境变量不生效 | 变量名错误或未导出 | `echo $VAR_NAME` 验证变量是否存在；重启终端 |

---

### 4.6 MCP / A2A / ACP 三大协议对比

2025-2026 年，AI 协议生态逐渐成形，MCP、A2A、ACP 三个协议分别解决不同层面的问题。理解它们的关系，你就看懂了 AI 应用的"协议栈"全景。

#### 4.6.1 三协议各自定位

```
┌─────────────────────────────────────────────────────────┐
│                     AI 协议栈全景图                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐     ACP      ┌──────────┐               │
│   │  编辑器   │◄────────────►│  AI      │               │
│   │  IDE     │  编辑器←→Agent│  Agent   │               │
│   │  Host    │   通信协议    │          │               │
│   └──────────┘              └────┬─────┘               │
│                                  │                      │
│                        MCP       │       A2A            │
│                  ┌───────────────┼───────────┐          │
│                  │               │           │          │
│                  ▼               ▼           ▼          │
│            ┌──────────┐   ┌──────────┐  ┌──────────┐  │
│            │ 工具/数据 │   │ 其他     │  │ 更多     │  │
│            │ MCP Server │   │ Agent    │  │ Agent    │  │
│            └──────────┘   └──────────┘  └──────────┘  │
│               Agent ↔ 工具          Agent ↔ Agent       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 4.6.2 三大协议详细对比

| 维度 | MCP | A2A | ACP |
|------|-----|-----|-----|
| **全称** | Model Context Protocol | Agent-to-Agent Protocol | Agent Client Protocol |
| **中文** | 模型上下文协议 | 智能体间通信协议 | 智能体客户端协议 |
| **解决什么问题** | Agent 如何连接**工具和数据源** | Agent 如何与**其他 Agent** 发现和协作 | 编辑器/IDE/Host 如何与 **Agent** 通信 |
| **通信方向** | Agent ↔ 工具/数据 | Agent ↔ Agent | Host ↔ Agent |
| **发起方** | Agent 主动调用工具 | Agent 之间互相发现 | Host 发起对话，Agent 响应 |
| **制定方** | Anthropic（已捐给 Linux 基金会） | Google | Agent Client Protocol Working Group |
| **当前状态** | 最成熟，生态最丰富 | 规范稳定，生态发展 | 较新，正在快速演进 |

#### 4.6.3 生活类比：让三个协议一次记住

| 协议 | 类比 | 说明 |
|------|------|------|
| **MCP** | **USB 线** | 连接设备到电脑。一个 USB-C 设备可以插到任何有 USB-C 口的电脑上。MCP 让一个工具可以被任何支持 MCP 的 AI 应用使用。 |
| **A2A** | **WiFi / 蓝牙** | 设备之间互相通信。两个手机通过 WiFi 传文件，不需要经过电脑。A2A 让两个 Agent 直接协作，不需要经过用户。 |
| **ACP** | **HDMI / 显示器线** | 连接主机到显示器。不同的显示器都可以显示同一台主机的画面。ACP 让不同的 Host 应用（编辑器、终端、IDE）以统一的方式接入 Agent。 |

#### 4.6.4 三者缺一不可：为什么需要三层协议

```
场景：一个完整的 AI 开发工作流

1. 你在 VS Code 中打开一个项目，通过 ACP 连接到一个 Coding Agent
    ↓
2. Agent 理解你的需求后，通过 MCP 调用 GitHub Server 查找相关 Issue
    ↓
3. Agent 需要更专业的安全审查，通过 A2A 把代码发送给一个 Security Agent
    ↓
4. Security Agent 通过 MCP 调用数据库查询已知漏洞模式
    ↓
5. 审查结果通过 A2A 返回给 Coding Agent
    ↓
6. Coding Agent 整合结果，通过 ACP 在 VS Code 中展示给你
```

> **一句话总结**：MCP 让 Agent **能干活**（有工具），A2A 让 Agent **能协作**（有同伴），ACP 让 Agent **能被接入**（有界面）。三者共同构成 AI 时代的基础协议栈。

---

> 📊 **企业视角：Skills = 企业 AI 能力的可复制单元**
>
> 除了 MCP（解决"AI能做什么"），企业还需要关注 Skills（解决"AI怎么做得好"）的概念。
>
> **Skills 的企业类比**：Skill = 麦当劳的操作手册。每个新员工照着操作手册做，就能产出标准化的产品。同理，一个Skill是一次开发后全公司所有员工和Agent都能复用的AI能力单元。
>
> **企业 Skills 示例**：
>
> | Skill名称 | 功能 | 企业价值 |
> |-----------|------|---------|
> | `contract-review` | 自动审查合同关键条款 | 法务审查从2小时→10分钟，全公司标准化 |
> | `weekly-report` | 从Git/任务系统自动生成周报 | 每个员工每周节省30分钟 |
> | `customer-summary` | 整合CRM数据生成客户画像 | 销售拜访前5分钟了解客户全貌 |
> | `code-review` | 代码提交时自动审查 | 保证代码质量底线的同时减少高级工程师的审查时间 |
>
> **MCP + Skills 的组合效应**：MCP 提供"工具连接"（AI能访问什么），Skills 提供"能力模板"（AI怎么做得好）。两者配合，企业可以实现 AI 能力的"一次开发、全公司复用、持续迭代"——这才是企业 AI 投资的真正杠杆点。

### 4.7 MCP 的现状与未来

#### 4.7.1 当前生态规模

- **社区 MCP Server 数量**：1000+（并且快速增长中）
- **官方参考 Server**：20+ 个（覆盖文件、数据库、搜索、通讯等核心场景）
- **支持 MCP 的 AI 产品**：Claude Desktop、Claude Code、Cursor、VS Code + Continue、Zed、Sourcegraph Cody、Codex App 等
- **开发 SDK**：TypeScript（官方推荐）、Python（官方）、Java、Kotlin（社区）

#### 4.7.2 正在发生的趋势

| 趋势 | 说明 |
|------|------|
| **从单机到云** | 早期 MCP 主要用 STDIO 本地通信，现在 HTTP 传输越来越成熟，远程/云端 MCP Server 成为可能 |
| **流式传输增强** | 协议从 SSE 演进到 Streamable HTTP，支持更好的实时响应和进度通知 |
| **交互式 MCP** | Elicitation 机制让 MCP Server 可以在运行中向用户请求额外输入（确认、选择、补填参数） |
| **懒加载优化** | 大量 MCP Server 时不再一次性加载所有工具定义，只在需要时搜索和加载（ToolSearch），节省高达 95% 上下文 |
| **MCP Agent-to-Agent** | 社区开始探索用 MCP 实现 Agent 间通信，与 A2A 形成互补模式 |

#### 4.7.3 你应该关注的方向

1. **学习 MCP 不是学一个工具，而是学一套思维**：任何想让 AI 做的"外部操作"，都应该先想"有没有现成的 MCP Server？"
2. **优先使用官方和社区验证的 Server**：避免自己从零开发，站在巨人肩膀上
3. **关注安全边界**：MCP 让 AI 获得了前所未有的"行动力"，但同时也意味着更大的安全责任。权限设计比工具数量更重要。
4. **MCP + Skills 是能力复用的黄金组合**：MCP 负责"能做什么"，Skills 负责"怎么做好"。两者配合才是完整的 Agent 能力体系。

---

## 五、实操环节（70 分钟）

---

### 实操 1：Claude Code 中配置 MCP Server（30 分钟）

**目标**：独立完成 Filesystem 和 Fetch 两个 MCP Server 的完整配置，并通过实际对话验证工具调用。

#### Step 1：创建项目（5 分钟）

```bash
# 创建实操项目目录
mkdir ~/mcp-practice
cd ~/mcp-practice

# 创建一些测试文件供后续测试使用
echo "# MCP Practice Project" > README.md
echo "print('Hello World')" > hello.py
mkdir data
echo '{"name": "test", "version": "1.0"}' > data/config.json
```

#### Step 2：配置 Filesystem MCP（10 分钟）

创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {}
    }
  }
}
```

启动 Claude Code：

```bash
claude
```

验证 MCP 连接：启动时应看到 `✓ filesystem` 和 `✓ fetch`。

#### Step 3：测试 Filesystem MCP（10 分钟）

在 Claude Code 中输入以下测试命令，观察每次的工具调用：

**测试 A — 列出文件**：
```
列出当前项目的所有文件
```
观察点：AI 是否调用了 `filesystem.list_directory`？

**测试 B — 读取文件**：
```
读取 hello.py 的内容，并说明它做了什么
```
观察点：AI 是否先调用 `read_file` 获取内容，然后做出分析？

**测试 C — 创建文件**：
```
在 data 目录下创建一个 info.txt，内容写"MCP 配置测试成功"
```
观察点：AI 是否调用了 `write_file`？是否需要确认权限？

**测试 D — 搜索文件**：
```
找到所有 .py 文件
```
观察点：AI 是否调用了 `search_files`？

#### Step 4：测试 Fetch MCP（5 分钟）

```
从 https://modelcontextprotocol.io 获取内容，并总结 MCP 是什么
```
观察点：AI 是否调用了 `fetch.fetch` 获取网页内容，然后基于内容生成中文总结？

---

### 实操 2：MCP 概念演示 —— 用 Python 构建 MCP 模式（25 分钟）

**目标**：用纯 Python 代码构建一个最小 MCP 系统，理解协议的核心模式 —— 工具注册、工具列表、工具调用。

> **重要说明**：本实操不依赖 MCP SDK，仅用原生 Python 演示 MCP 的**设计模式**。理解了这个模式，你就理解了所有 MCP Server 的底层逻辑。

#### 完整代码：`simple_mcp_demo.py`

在 `~/mcp-practice/` 目录下创建以下文件：

```python
"""
简单 MCP 模式演示 —— 理解 MCP 的核心设计

本代码演示 MCP 的三个核心动作：
1. 注册工具（register tools with name, description, schema）
2. 列出工具（list tools for the AI to discover）
3. 调用工具（call tools with structured arguments）

这是所有 MCP Server 的底层模式 —— 无论 TypeScript 还是 Python。
"""

import json
from typing import Any, Callable


# ============================================================
# 第一部分：SimpleMCPServer —— 最小 MCP Server 实现
# ============================================================

class SimpleMCPServer:
    """
    一个最小化的 MCP 风格 Server。

    核心数据结构：
    - self.tools: dict[str, dict]
        存储所有注册的工具，key 是工具名，value 包含：
        - name: 工具名称
        - description: 工具描述（AI 靠这个判断何时调用）
        - schema: 输入参数的 JSON Schema（AI 靠这个决定传什么参数）
        - handler: 实际执行的函数
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: dict[str, dict] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        schema: dict,
        handler: Callable
    ):
        """
        注册一个工具。

        这是 MCP 最核心的操作 —— 告诉系统：
        1. 这个工具叫什么（name）
        2. 这个工具做什么（description）—— 这是 AI 判断何时使用的关键！
        3. 这个工具需要什么参数（schema）
        4. 当被调用时执行什么逻辑（handler）
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": schema,
            "handler": handler
        }
        print(f"[{self.name}] ✅ 注册工具: {name}")

    def list_tools(self) -> list[dict]:
        """
        返回所有可用工具的列表。

        在真实 MCP 中，这对应 tools/list 请求。
        AI 通过这个列表知道"我能做什么"。
        """
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"]
            }
            for t in self.tools.values()
        ]

    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """
        调用指定工具并传入参数。

        在真实 MCP 中，这对应 tools/call 请求。
        AI 决定调用哪个工具、传什么参数，Client 负责执行。
        """
        if tool_name not in self.tools:
            return {"error": f"未知工具: {tool_name}"}

        tool = self.tools[tool_name]
        try:
            result = tool["handler"](**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# 第二部分：定义具体工具
# ============================================================

def read_file_tool(path: str) -> str:
    """读取文件内容的工具函数"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"错误：文件 {path} 不存在"
    except PermissionError:
        return f"错误：没有权限读取 {path}"


def write_file_tool(path: str, content: str) -> str:
    """写入文件内容的工具函数"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"文件已写入: {path} ({len(content)} 字符)"


def list_directory_tool(directory: str = ".") -> str:
    """列出目录内容的工具函数"""
    import os
    try:
        items = os.listdir(directory)
        return f"目录 {directory} 包含 {len(items)} 个项目:\n" + \
               "\n".join(f"  - {item}" for item in items)
    except FileNotFoundError:
        return f"错误：目录 {directory} 不存在"


def search_tool(query: str, count: int = 5) -> str:
    """模拟搜索工具"""
    # 模拟搜索结果
    mock_results = [
        {"title": f"关于 {query} 的官方文档", "url": f"https://docs.example.com/{query}"},
        {"title": f"{query} 入门教程", "url": f"https://tutorial.example.com/{query}"},
        {"title": f"GitHub: {query} 开源项目", "url": f"https://github.com/topics/{query}"},
        {"title": f"{query} 最佳实践", "url": f"https://bestpractices.example.com/{query}"},
        {"title": f"{query} 常见问题", "url": f"https://faq.example.com/{query}"},
    ]
    return json.dumps(mock_results[:count], ensure_ascii=False, indent=2)


# ============================================================
# 第三部分：Agent —— 模拟 AI 的决策过程
# ============================================================

class SimpleAgent:
    """
    一个简单的 Agent，模拟 AI 使用 MCP 工具的过程。

    它不是真 AI —— 它用预设规则模拟"看到用户消息 -> 判断需要什么工具 -> 调用工具 -> 返回结果"的流程。
    但这个过程就是所有 Agent 的核心循环！
    """

    def __init__(self, mcp_server: SimpleMCPServer):
        self.server = mcp_server

    def _decide_tool_and_args(self, user_message: str) -> tuple[str, dict] | None:
        """
        模拟 AI 的决策过程：根据用户消息，决定调用哪个工具。

        在真实 Agent 中，这一步由 LLM 完成。
        这里我们用关键词匹配来模拟。
        """
        msg = user_message.lower()

        if any(w in msg for w in ["列出", "目录", "有哪些文件", "ls"]):
            return ("list_directory", {"directory": "."})

        if any(w in msg for w in ["读取", "读一下", "查看", "cat"]):
            # 从消息中提取文件名（简化处理）
            words = user_message.split()
            for w in words:
                if "." in w and not w.startswith("http"):
                    return ("read_file", {"path": w})
            return ("read_file", {"path": "README.md"})

        if any(w in msg for w in ["写入", "创建", "写一个", "保存"]):
            return ("write_file", {
                "path": "output.txt",
                "content": "这是 Agent 通过 MCP 工具创建的文件。\n用户说：" + user_message
            })

        if any(w in msg for w in ["搜索", "查一下", "search", "找"]):
            return ("search", {"query": user_message, "count": 3})

        return None

    def run(self, user_message: str) -> str:
        """执行一次 Agent 循环"""
        print(f"\n{'='*60}")
        print(f"用户消息: {user_message}")
        print(f"{'='*60}")

        # Step 1: 决策（真实 Agent 中由 LLM 完成）
        decision = self._decide_tool_and_args(user_message)

        if decision is None:
            return "我没有找到合适的工具来处理这个请求。"

        tool_name, args = decision

        # Step 2: 展示可用工具列表（AI 在做决策前已经看到了这个列表）
        print(f"\n[Agent 思考] 可用工具:")
        for tool in self.server.list_tools():
            print(f"  · {tool['name']}: {tool['description']}")

        # Step 3: 调用工具
        print(f"\n[Agent 行动] 调用工具: {tool_name}")
        print(f"[Agent 行动] 参数: {json.dumps(args, ensure_ascii=False)}")

        result = self.server.call_tool(tool_name, args)

        # Step 4: 返回结果
        if result["success"]:
            print(f"\n[Agent 输出] 工具调用成功:")
            return result["result"]
        else:
            print(f"\n[Agent 输出] 工具调用失败:")
            return result["error"]


# ============================================================
# 第四部分：主演示 —— 跑通 MCP 全流程
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("   MCP 模式演示 —— AI 的 USB-C 接口")
    print("=" * 60)

    # Step 1: 创建 MCP Server
    print("\n[1] 创建 MCP Server...")
    server = SimpleMCPServer(name="demo-server")

    # Step 2: 注册工具 —— 这是 MCP 的核心动作
    print("\n[2] 注册工具...")
    server.register_tool(
        name="list_directory",
        description="列出指定目录下的所有文件和子目录",
        schema={
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "要列出的目录路径，默认为当前目录"
                }
            }
        },
        handler=list_directory_tool
    )

    server.register_tool(
        name="read_file",
        description="读取指定路径的文件内容",
        schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["path"]
        },
        handler=read_file_tool
    )

    server.register_tool(
        name="write_file",
        description="将内容写入指定路径的文件",
        schema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "content": {
                    "type": "string",
                    "description": "要写入的内容"
                }
            },
            "required": ["path", "content"]
        },
        handler=write_file_tool
    )

    server.register_tool(
        name="search",
        description="在网络上搜索指定关键词，返回相关结果列表",
        schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                },
                "count": {
                    "type": "integer",
                    "description": "返回结果数量，默认5条"
                }
            },
            "required": ["query"]
        },
        handler=search_tool
    )

    # Step 3: 展示工具列表（相当于 MCP 的 tools/list）
    print(f"\n[3] 工具列表 (共 {len(server.list_tools())} 个):")
    for tool in server.list_tools():
        print(f"   · {tool['name']}: {tool['description']}")

    # Step 4: 创建 Agent 并执行演示
    print("\n[4] 创建 Agent 并执行演示任务...")
    agent = SimpleAgent(server)

    # 演示任务序列
    demo_tasks = [
        "列出当前目录有哪些文件",
        "读取 hello.py 文件",
        "创建一个 output.txt 文件，内容是测试MCP工具调用",
        "搜索 Python MCP 教程"
    ]

    for task in demo_tasks:
        result = agent.run(task)
        print(f"\n>>> 最终结果:\n{result}")

    print(f"\n{'='*60}")
    print("   演示完成！")
    print(f"   MCP 核心模式: 注册工具 → 列出工具 → AI决策 → 调用工具")
    print(f"{'='*60}")
```

#### 运行演示

```bash
cd ~/mcp-practice
python simple_mcp_demo.py
```

#### 观察要点

运行代码时，请重点关注以下输出：

1. **工具注册阶段**：看到 4 个 `✅ 注册工具` 消息，每个工具有 name、description、schema
2. **工具列表展示**：Agent 能看到所有 4 个可用工具
3. **Agent 决策过程**：Agent 根据用户消息选择正确的工具
4. **工具调用和返回**：看到参数传递和结果返回的完整链路

#### 核心理解

这个不到 200 行的 Python 代码演示了 MCP 的核心设计模式：

```
MCP 的本质 = 统一的工具描述格式 + 统一的调用接口

- register_tool:   告诉系统"我能做什么"（name + description + schema）
- list_tools:      让 AI 发现"有哪些工具可用"
- call_tool:       让 AI 执行"用这个工具做这件事"

无论是官方 Filesystem MCP Server（数千行 TypeScript）还是我们这个
演示（不到 200 行 Python），底层的设计模式完全一样。
```

---

### 实操 3：探索 MCP 生态（15 分钟）

**目标**：了解 MCP 生态的丰富程度，找到对自己项目有用的 MCP Server。

#### Step 1：浏览 MCP 官方网站（5 分钟）

访问 https://modelcontextprotocol.io

关注：
- 首页的架构图——对比你在本课中学到的三层架构
- "Servers" 页面——看有哪些官方推荐的 Server
- "Quickstart"——跟我们的实操有什么异同？

#### Step 2：浏览 GitHub 上的 MCP Server 合集（5 分钟）

访问 https://github.com/modelcontextprotocol/servers

关注：
- 每个 Server 的 README —— 就是它的使用说明书
- 官方 Server 目录结构 —— 你未来自己开发 MCP Server 的参考模板

#### Step 3：讨论与分享（5 分钟）

思考和讨论以下问题：
1. 你目前做项目时，最想让 AI 帮你操作什么工具？（例如：数据库、GitHub、文件、搜索引擎...）
2. 在 MCP Server 合集中，你找到了哪些与你的需求匹配的 Server？
3. 如果有 Server 还没人开发，你可以自己做一个吗？（你已经在实操 2 中掌握了核心模式！）

---

## 六、课后作业（第7周综合大作业）

本周是整个 Agent 模块的综合实践周。请完成以下任务，将前三课学到的 Agent 知识整合成一个完整项目。

### 大作业：AI 私人秘书

**基础要求（必做）**：

1. **工具集成**：为你的 Agent 配置至少 3 个 MCP Server（建议：filesystem + fetch + memory）
2. **功能实现**：你的 Agent 需要能够完成以下任务：
   - 接收用户的自然语言指令
   - 使用 MCP 工具读取本地文件、获取网页信息
   - 将处理结果保存到本地文件
3. **Web UI**：使用 Streamlit 或 Gradio 构建一个简单的 Web 界面，可以让用户通过浏览器与你的 Agent 交互
4. **MCP 理解**：写一段不超过 500 字的文字，解释 MCP 在你的项目中扮演了什么角色，为什么选择这些 MCP Server

**进阶要求（选做）**：

5. 接入 GitHub MCP，实现"用户说一句话，自动创建 Issue"的功能
6. 使用 Memory MCP，实现跨会话的记忆（下次打开 Agent，它还记得你们上次聊了什么）

**提交格式**：
- 项目代码（GitHub 仓库链接或压缩包）
- `README.md` 说明运行方法
- 一段不超过 5 分钟的演示录屏（可选但推荐）

---

### 💼 企业版作业：MCP 采纳策略文档

为你的企业撰写一份 **"MCP 采纳策略"**（1-2页），包含：

1. **内部工具盘点**：列出你所在企业/部门使用的5-10个核心软件工具（CRM/ERP/OA/数据库/文件系统/邮件/IM...）
2. **MCP兼容性评估**：调研每个工具是否已有社区MCP Server，或是否可以自行开发MCP Server（是否有标准API）
3. **优先级排序**：按"使用频率 × AI集成价值"对工具排序，确定MCP化的优先级
4. **安全风险分析**：列出如果将每个工具通过MCP暴露给AI，潜在的安全风险和对策
5. **实施路线图**：制定3-6个月的MCP推广计划（参考上面📊框中的采纳时间线）

同时，浏览 https://github.com/modelcontextprotocol/servers 和 https://github.com/punkpeye/awesome-mcp-servers ，找出至少2个与你企业直接相关的MCP Server。

---

## 七、拓展阅读

### 7.1 官方资源（必读）

| 资源 | 链接 | 为什么重要 |
|------|------|-----------|
| MCP 官方文档 | https://modelcontextprotocol.io/ | 最权威的协议说明和入门教程 |
| MCP 规范（2025-11-25） | https://modelcontextprotocol.io/specification/2025-11-25 | 协议的完整技术规范，开发 MCP Server 时参考 |
| 官方 MCP Server 合集 | https://github.com/modelcontextprotocol/servers | 20+ 官方参考 Server，学习 MCP 开发的最佳样例 |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk | 开发 MCP Server 的官方 TS SDK |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk | 开发 MCP Server 的官方 Python SDK |

### 7.2 协议规范

| 资源 | 链接 | 为什么重要 |
|------|------|-----------|
| A2A 协议规范 | https://a2a-protocol.org/latest/specification/ | 理解 Agent 间通信机制，Google 制定 |
| ACP 协议规范 | https://agentclientprotocol.com/ | 理解 Host-Agent 通信机制，编辑器生态的核心 |
| Anthropic：Building Effective Agents | https://www.anthropic.com/engineering/building-effective-agents | Agent 设计原则的经典文章，MCP 的使用上下文 |

### 7.3 社区资源

| 资源 | 链接 | 为什么重要 |
|------|------|-----------|
| Awesome MCP Servers | https://github.com/punkpeye/awesome-mcp-servers | 社区精选 MCP Server 合集，发现更多工具 |
| MCP Server Finder | https://www.mcpserverfinder.com/ | MCP Server 搜索引擎 |
| Claude Code MCP 文档 | https://code.claude.com/docs/en/mcp | Claude Code 中 MCP 的详细配置文档 |

---

## 八、常见问题

### Q1：MCP 和我直接用 API 有什么区别？

**A**：MCP 是"标准插座"，API 是"特定设备"。当你用 MCP 连接 GitHub 时，你的 AI 应用不需要知道 GitHub API 的任何细节。换个 MCP Server，AI 应用一行代码不用改。这就像你不需要知道 U 盘里面的闪存芯片型号，插上去就能用。

| 对比 | MCP 方式 | 直接调用 API |
|------|----------|------------|
| **AI 应用改动** | 零（协议统一） | 每次都要写新代码 |
| **跨平台复用** | 天然支持 | 需要额外适配 |
| **生态共享** | 社区积累 | 各自为战 |

### Q2：我学了第7周第2课的某个框架（如 LangGraph、OpenAI Agents SDK），还需要 MCP 吗？

**A**：需要，而且是互补关系。框架负责 Agent 的**内部逻辑**（怎么思考、怎么循环、怎么编排），MCP 负责 Agent 的**外部能力**（能用什么工具、能访问什么数据）。一个类比：框架是"工厂的生产线设计"，MCP 是"生产线上各个机器之间的标准接口"。两者各司其职。

### Q3：我需要自己开发 MCP Server 吗？

**A**：大多数情况下不需要。1000+ 社区 MCP Server 已经覆盖了绝大部分常见需求。你应该先搜索有没有现成的，再考虑自己开发。但理解 MCP 的开发模式（如实操 2 所示）是很有价值的，它能帮你：1）更快看懂别人的 MCP Server 源码；2）在需要定制时快速上手；3）深入理解工具调用的底层机制。

### Q4：MCP Server 配置多了会影响性能吗？

**A**：不会。MCP Server 是按需启动的进程，只有被实际调用时才会运行。配置 10 个 Server 但目前只调用 filesystem，只有 filesystem 进程在运行。而且 Claude Code v2.1.52 后引入了懒加载机制（ToolSearch），工具定义也不会全部加载到上下文窗口，进一步减少了 token 消耗。

### Q5：MCP 安全吗？AI 会不会通过 MCP 做危险操作？

**A**：MCP 本身提供了权限控制的基础设施（允许目录白名单、读写权限、环境变量隔离），但安全最终还是取决于你的配置。核心原则：
- Filesystem MCP 只允许访问指定目录，**绝对不能给根目录权限**
- 包含 API Key 的配置放在 Local 作用域，不要提交到 Git
- 数据库连接使用只读用户
- 危险操作（删除文件、发邮件、付款）需要人工确认

### Q6：MCP、A2A、ACP 三个我都要学吗？

**A**：优先级从高到低——MCP > A2A > ACP。MCP 是目前最成熟、生态最丰富的协议，也是本课的重点。A2A 在你的 Agent 需要与其他 Agent 协作时才需要。ACP 目前主要关注的是编辑器/IDE 工具的开发者，终端用户暂时不需要深入了解。**先学 MCP，其他两个知道概念即可，用到了再深入**。

### Q7：MCP 现在还是 Anthropic 一家的东西吗？

**A**：不是了。2025 年 12 月 9 日，Anthropic 将 MCP 捐赠给了 Linux 基金会下的 Agentic AI Foundation（AAIF）。OpenAI、Google DeepMind、Microsoft 等主流 AI 厂商都已表态支持。MCP 现在是行业标准，不是一家公司的私有协议。

### Q8（企业）：MCP 还处于早期阶段，现在投入会不会太早？

**答**：这是合理的顾虑。但从2025年12月MCP捐给Linux基金会这个信号来看，"太早"可能正在变成"正好"。判断标准：如果你的企业目前没有任何AI Agent的应用场景，暂时观望是合理的。但如果你已经在使用Claude Code/Cursor等AI工具，或者已经在计划Agent项目——现在配置MCP就是"基础设施投资"，属于早投早受益的类型。关键是：不要等待"MCP完全成熟"——TCP/IP从诞生到完全标准化花了20年，但早期采用者早在1990年代就享受了互联网红利。

### Q9（企业）：MCP Server 的安全性如何保障？AI会不会通过MCP窃取数据？

**答**：MCP本身就设计了多层安全机制：1) Filesystem MCP只允许访问指定的目录白名单；2) STDIO模式的MCP Server只在本地运行，数据不经过网络；3) HTTP模式支持OAuth认证。但最终安全性取决于你的配置——永远不要给AI根目录权限、数据库使用只读账户、敏感操作设置人工审批。建议参考 Anthropic 的 MCP 安全最佳实践文档。

### Q10（企业）：A2A和ACP还需要关注吗？

**答**：MCP是当前的绝对优先。A2A在你的企业需要多Agent协作（如采购Agent和财务Agent需要通信）时才会用到，多数中小企业暂时不需要。ACP主要面向IDE/编辑器开发者，如果你是软件公司的产品经理需要考虑，否则可以暂时忽略。建议：2026年重点投入MCP，2027年视需要关注A2A。

---

## 九、本节小结

恭喜你完成了本节课程！让我们回顾一下核心收获：

```
┌───────────────────────────────────────────────────────┐
│                    MCP 学习路线图                        │
├───────────────────────────────────────────────────────┤
│                                                       │
│  理解问题 ──→ MxN 集成噩梦 vs M+N 标准化解决方案          │
│      │                                                │
│      ▼                                                │
│  理解架构 ──→ Host / Client / Server 三层 + JSON-RPC    │
│      │                                                │
│      ▼                                                │
│  理解能力 ──→ Tools（模型调用）vs Resources（数据）        │
│              vs Prompts（模板）                         │
│      │                                                │
│      ▼                                                │
│  动手配置 ──→ Filesystem MCP + GitHub MCP + Fetch MCP   │
│      │                                                │
│      ▼                                                │
│  理解生态 ──→ MCP + A2A + ACP 三层协议栈                 │
│              + 1000+ 社区 Server 生态                   │
│      │                                                │
│      ▼                                                │
│  动手编码 ──→ Python 实现 MCP 核心模式                   │
│              register → list → call                   │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**最重要的一个思维转变**：从这一课开始，每当你想让 AI 做一件事，你的第一反应应该是——**"有没有现成的 MCP Server 能搞定？"** 而不是"我该怎么从零写代码？"。这种"协议思维"是 AI Agent 时代的核心素养。

---

**作者**：AI Learning Route 课程团队
**更新日期**：2026年7月26日
**适用版本**：MCP 规范 2025-11-25 / Claude Code v2.1.x
**字数**：约 6500 字
