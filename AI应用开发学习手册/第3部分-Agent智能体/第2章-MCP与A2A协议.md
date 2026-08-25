# 第 2 章 大模型工程新协议：MCP 与 A2A

## 学习目标

- 理解 MCP（模型上下文协议）的架构与价值
- 掌握 MCP Server 的开发与客户端集成
- 理解 A2A（Agent-to-Agent）协议的设计思想
- 掌握 MCP 与 A2A 的分工与联合应用

---

## 2.1 为什么需要 MCP

### 2.1.1 现状痛点：N×M 集成地狱

每个大模型应用都要对接 N 个外部系统（数据库、SaaS、内部服务），而每个系统又有不同的 API 协议。接入方与提供方**两两对接**，复杂度呈 N×M 爆炸。

```
传统模式（N×M 对接）：
  LLM 应用 A ──▶ 数据库 / CRM / 邮件 / 文件系统
  LLM 应用 B ──▶ 数据库 / CRM / 邮件 / 文件系统   ← 每个连接都要单独开发
```

### 2.1.2 MCP 的解法：统一协议

**MCP（Model Context Protocol，模型上下文协议）** 由 Anthropic 于 2024 年底开源，是"大模型应用连接外部工具的**USB-C 标准**"：

- **Server 侧**：把能力（工具、数据、提示词）按统一协议暴露一次。
- **Client 侧**：任何支持 MCP 的应用（Claude、Cursor、自研 Agent）即插即用。

```
MCP 模式（N+M 对接）：
  LLM 应用 ──▶ MCP Client ──▶ MCP Server（数据库/CRM/邮件/文件...）
  任何支持 MCP 的宿主应用都可复用同一批 Server
```

### 2.1.3 MCP 三大原语

| 原语 | 方向 | 作用 | 类比 |
|------|------|------|------|
| **Tools（工具）** | Client → Server | 执行动作（查询、写入、调用） | 函数调用 |
| **Resources（资源）** | Server → Client | 提供上下文数据（文件、文档、查询结果） | 数据文件 |
| **Prompts（提示词）** | 双向 | 可复用的提示模板 | 预置模板 |

## 2.2 MCP 架构详解

### 2.2.1 组成要素

```
┌────────────┐   JSON-RPC 2.0    ┌─────────────────┐
│ MCP Host   │ ◄───────────────► │  MCP Server     │
│ (Claude/   │    (stdio / SSE)  │  ├── Tools      │
│  IDE/自研)  │                   │  ├── Resources  │
└────────────┘                   │  └── Prompts    │
    │                            └─────────────────┘
    ▼
 LLM（可访问工具列表与上下文）
```

- **传输方式**：stdio（本地子进程）、Streamable HTTP / SSE（远程服务）。
- **通信协议**：JSON-RPC 2.0 之上的自定义方法（`tools/list`、`tools/call`、`resources/read` 等）。
- **Server 类型**：本地（文件系统、数据库）、远程（SaaS API、内部服务）。

## 2.3 MCP Server 开发实战

### 2.3.1 用 Python SDK 开发一个"天气查询"Server

```python
# pip install "mcp[cli]" httpx
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询指定城市的实时天气。
    Args:
        city: 城市名（中文）
        unit: 温度单位 celsius/fahrenheit
    """
    # 此处对接真实天气 API
    return f"{city}：晴，26°C，湿度 40%"

@mcp.resource("weather://{city}")
def weather_resource(city: str) -> str:
    """以资源形式暴露天气数据"""
    return f"city={city}, temp=26, humidity=40"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 2.3.2 客户端接入（FastMCP Client / 兼容 OpenAI 接口）

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["weather_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("get_weather", {"city": "上海"})
            print(result)

asyncio.run(main())
```

### 2.3.3 MCP 集成到 LangChain Agent

```python
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_tool_calling_agent

# 加载远程 MCP Server 的工具
tools = await load_mcp_tools(
    "https://mcp.example.com/mcp"   # Streamable HTTP 传输
)
agent = create_tool_calling_agent(llm, tools, prompt)
```

### 2.3.4 开发最佳实践

1. **工具命名与描述**：LLM 靠描述选工具，描述要写清用途、参数含义、返回结构。
2. **错误处理**：每个工具捕获异常返回友好错误信息。
3. **认证安全**：远程 Server 用 OAuth/API Key；最小权限原则。
4. **工具数量控制**：单个 Server 暴露 5-20 个工具为宜，过多导致选择困难。
5. **输入校验**：对参数做类型与范围校验，防止恶意输入。

## 2.4 A2A（Agent2Agent）协议

### 2.4.1 定位

**A2A（Agent-to-Agent）** 由 Google 于 2025 年提出，是**Agent 之间通信的开放协议**，解决"多个独立 Agent 如何协作"的问题。如果说 MCP 解决"Agent 连工具"，A2A 解决"Agent 连 Agent"。

### 2.4.2 A2A 核心机制

| 机制 | 说明 |
|------|------|
| Agent Card | 每个 Agent 暴露能力描述（JSON 格式） |
| 任务（Task） | 发起方创建任务，执行方返回状态与结果 |
| 消息流 | 结构化消息：文本、文件、功能调用、指令 |
| 技能（Skills） | Agent 声明的可调用能力 |
| 传输 | 基于 HTTP + JSON-RPC，支持 SSE 流式 |

### 2.4.3 A2A 工作示例

```
【任务】"帮我组织一场产品发布会"
主 Agent（策划）─┬─► A2A 请求 ──► 场地 Agent（订场地，返回酒店列表）
                ├─► A2A 请求 ──► 供应商 Agent（订物料，返回报价）
                └─► A2A 请求 ──► 宣传 Agent（生成海报文案）
各 Agent 返回结构化任务结果 → 主 Agent 汇总编排
```

## 2.5 MCP 与 A2A 的对比与联合

| 维度 | MCP | A2A |
|------|-----|-----|
| 解决的问题 | Agent → 工具/数据 | Agent ↔ Agent |
| 发起方 | 模型客户端 | 任意 Agent |
| 核心概念 | Tools / Resources / Prompts | Agent Card / Task / Skills |
| 通信 | JSON-RPC（stdio/HTTP/SSE） | HTTP + SSE |
| 生态 | Anthropic 发起，行业广泛采用 | Google 发起，Anthropic/OpenAI 等参与 |
| 类比 | USB-C（统一硬件接口） | 电子邮件（标准化的 Agent 通信） |

**2026 年趋势**：业界普遍采用 **"MCP 管工具、A2A 管协作"** 的组合架构：

```
                    ┌── MCP Server: 数据库 ──┐
Agent A ──A2A──► Agent B ──MCP──► ├── MCP Server: 邮件 ──┤
                    └── MCP Server: ERP  ──┘
```

## 2.6 实战：打造"连接一切"的 Agent

**项目：企业助手 Agent**
1. 开发 MCP Server：企业内部数据库查询、文档库检索、审批系统。
2. 配置远程 MCP 端点，LangChain/自研 Agent 加载工具。
3. 若需跨部门协作，用 A2A 将"财务 Agent"、"人事 Agent"接入协作网络。
4. 安全设计：OAuth2 认证、审计日志、工具级权限。

---

## 高质量博客推荐

1. **MCP（模型上下文协议）完整深度解析** — [CSDN](https://blog.csdn.net/2401_87876783/article/details/147978565)
   从架构到三大原语到 Server 开发的全景教程。
2. **一文读懂 MCP：大模型工具连接的 USB-C** — [腾讯云开发者社区](https://cloud.tencent.com/developer/article/2486694)
   用通俗类比讲透 MCP 价值与工作流，适合入门。
3. **MCP Server 开发实战：从零实现一个文件管理服务** — [微信公众号](https://mp.weixin.qq.com/s/5dKk4F2fT9qGm3hQJ7y3SA)
   完整代码级实战，含 stdio 与 HTTP 两种传输。
4. **A2A 协议解读：Google Agent 互操作新标准** — [CSDN](https://blog.csdn.net/github_38336963/article/details/149861345)
   A2A 机制拆解与 MCP/A2A 对比分析。
5. **MCP 官方文档（中文）** — [Model Context Protocol Docs](https://modelcontextprotocol.io/)
   协议规范的权威参考，含各语言 SDK 指南。

## 动手实践

1. 用 FastMCP 开发一个"待办事项管理"Server，在支持 MCP 的客户端（如 Claude Desktop）中调用。
2. 将 MCP 工具接入你已有的 LangChain Agent，完成"工具即插即用"。
3. 阅读一个真实开源 MCP Server（如 GitHub 官方 MCP），分析其工具划分与错误处理设计。
4. 画一张"MCP + A2A"混合架构图，标注企业场景中的 Agent、工具、数据流。

## 常见问题（FAQ）

**Q1：MCP 会取代 Function Calling 吗？**
A：不会。Function Calling 是模型侧的能力（模型输出函数调用），MCP 是生态侧的协议（统一工具接入）。两者互补：Function Calling 决定"怎么调"，MCP 决定"调什么、怎么连"。

**Q2：自己公司要不要搭 MCP Server？**
A：如果内部系统（ERP、CRM、数据库）要被多个 AI 应用复用，强烈建议按 MCP 统一暴露，避免重复开发。

**Q3：MCP 安全吗？**
A：MCP 本身是传输层协议，安全取决于实现：必须做认证、权限最小化、工具输入校验、审计日志。远程 MCP 建议走 OAuth 2.0 与私有网络。
