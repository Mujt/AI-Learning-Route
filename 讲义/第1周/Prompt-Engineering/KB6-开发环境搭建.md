# KB6: 开发环境搭建 —— VSCode + Claude + DeepSeek

---

## 1. 知识块信息表

| 属性 | 内容 |
|------|------|
| **知识块编号** | KB6 |
| **知识块名称** | 开发环境搭建 |
| **所属章节** | 六（VSCode + Claude + DeepSeek 开发环境搭建） |
| **建议时长** | 25 分钟 |
| **前置知识** | KB5（Prompt Engineering 实战详解），已注册至少 2 个 AI 工具账号 |
| **知识类型** | 实操配置 |
| **适用对象** | 零基础学习者 / 企业管理者 / 开发者 |
| **核心能力目标** | 完成 VSCode + Cline + DeepSeek 本地开发环境搭建，能通过 Cline 发送第一个编程 Prompt |
| **硬件要求** | Windows 10+ / macOS 12+ / Linux，4GB+ 内存，2GB+ 可用磁盘空间（不含 AI 模型文件） |

---

## 2. AI 开发环境架构总览

### 2.1 系统架构图

```
═══════════════════════════════════════════════════════════════════════════
                         AI 辅助开发环境 —— 完整架构
═══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                           你的本地机器                                    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      IDE 层（交互界面）                             │  │
│  │                                                                   │  │
│  │   ┌─────────────────────────────────────────────────────────┐    │  │
│  │   │                     VSCode                                │    │  │
│  │   │                                                          │    │  │
│  │   │  ┌───────────┐  ┌───────────┐  ┌──────────────────┐     │    │  │
│  │   │  │  Cline    │  │ Continue  │  │  GitHub Copilot  │     │    │  │
│  │   │  │  (最强)   │  │ (多模型)  │  │  (代码补全)      │     │    │  │
│  │   │  │           │  │           │  │                  │     │    │  │
│  │   │  │ 读写文件  │  │ 对话+补全 │  │  行内自动补全    │     │    │  │
│  │   │  │ 执行终端  │  │ 模型切换  │  │  多语言支持      │     │    │  │
│  │   │  │ 自主Debug │  │ 开源免费  │  │  $10/月          │     │    │  │
│  │   │  └─────┬─────┘  └─────┬─────┘  └────────┬─────────┘     │    │  │
│  │   │        │              │                  │               │    │  │
│  │   └────────┼──────────────┼──────────────────┼───────────────┘    │  │
│  │            │              │                  │                    │  │
│  └────────────┼──────────────┼──────────────────┼────────────────────┘  │
│               │              │                  │                       │
│               │     HTTPS/SSE (MCP 协议可选)     │                       │
│               ▼              ▼                  ▼                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     AI 模型层（推理能力）                           │  │
│  │                                                                   │  │
│  │   ┌─────────────────┐         ┌──────────────────┐                │  │
│  │   │   Claude API     │         │   DeepSeek API    │                │  │
│  │   │                 │         │                  │                │  │
│  │   │  Sonnet 5       │         │  deepseek-chat   │                │  │
│  │   │  · 最强代码能力 │         │  · 中文理解最优  │                │  │
│  │   │  · 长文本推理  │         │  · 极低成本       │                │  │
│  │   │  · 复杂任务    │         │  · 国内直连       │                │  │
│  │   │                │         │  · 新用户免费额度 │                │  │
│  │   │  Opus 5         │         │                  │                │  │
│  │   │  · 最强推理    │         │  deepseek-reasoner│               │  │
│  │   │  · 架构设计    │         │  · 深度推理模式   │                │  │
│  │   │  · 高难度Debug │         │  · 数学/逻辑      │                │  │
│  │   └────────┬────────┘         └────────┬─────────┘                │  │
│  │            │                           │                           │  │
│  └────────────┼───────────────────────────┼───────────────────────────┘  │
│               │                           │                              │
│               └───────────┬───────────────┘                              │
│                           │                                              │
│                           ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     项目层（工作成果）                              │  │
│  │                                                                   │  │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │  │
│  │   │ Python   │  │ MySQL    │  │ 前端     │  │ 文档     │        │  │
│  │   │ 项目     │  │ 数据库   │  │ 项目     │  │ 项目     │        │  │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘        │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
数据流说明：
  1. 用户在 VSCode 中通过 Cline/Continue 插件输入 Prompt
  2. 插件将 Prompt + 项目文件上下文打包为 API 请求
  3. API 请求通过 HTTPS 发送到 Claude API 或 DeepSeek API
  4. AI 模型返回响应（代码/分析/建议）
  5. Cline 可直接将返回的代码写入项目文件，或执行终端命令
═══════════════════════════════════════════════════════════════════════════
```

### 2.2 核心组件职责

| 组件 | 定位 | 核心功能 | 适用阶段 |
|------|------|----------|----------|
| **VSCode** | 代码编辑器/IDE 平台 | 项目管理、代码编辑、终端、调试、插件生态 | 全程 |
| **Cline** | AI 编码 Agent | 对话式编程、文件读写、终端执行、自主 Debug | 开发 + 调试 |
| **Continue** | AI 编程助手 | 对话、代码补全、多模型切换、开源免费 | 开发 + 学习 |
| **GitHub Copilot** | 行内代码补全 | 实时代码建议、多语言支持、上下文感知 | 编写代码 |
| **Python 插件** | 语言支持 | 语法高亮、智能提示、调试、虚拟环境管理 | Python 开发 |
| **Claude API** | AI 推理服务 | 代码生成、长文本处理、复杂推理 | 高复杂度任务 |
| **DeepSeek API** | AI 推理服务 | 中文处理、低成本、高频任务 | 中文任务 + 批量处理 |

### 2.3 Cline 作为 Agent 的技术要点

```
Cline 不是普通的"聊天插件"，它是一个在 IDE 中运行的完整 Agent：

┌──────────────────────────────────────────────────────────┐
│              Cline Agent 架构（简化）                      │
│                                                          │
│  用户输入 Prompt                                          │
│      │                                                   │
│      ▼                                                   │
│  ┌────────────────────────────────────────┐              │
│  │          Cline Agent Loop               │              │
│  │                                         │              │
│  │  ┌─────────────────────────┐           │              │
│  │  │ 1. 分析用户意图          │           │              │
│  │  │    └─ 拆解任务           │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 2. 读取项目上下文        │           │              │
│  │  │    └─ 读取文件树/打开文件│           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 3. 规划执行策略          │           │              │
│  │  │    └─ 判断需要哪些工具   │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 4. 执行动作              │           │              │
│  │  │    ├─ 写入文件           │           │              │
│  │  │    ├─ 执行终端命令       │           │              │
│  │  │    └─ 搜索/替换代码      │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 5. 检查结果              │           │              │
│  │  │    └─ 读取输出/检查错误  │           │              │
│  │  ├─────────────────────────┤           │              │
│  │  │ 6. 迭代（回到步骤2）     │           │              │
│  │  │    直到任务完成          │           │              │
│  │  └─────────────────────────┘           │              │
│  │                                         │              │
│  │  权限模型（四级）：                       │              │
│  │  Allow  ─ 允许（自动执行）               │              │
│  │  Ask    ─ 每次询问用户                   │              │
│  │  Deny   ─ 拒绝（永不执行）               │              │
│  │  AskOnce─ 本次会话仅询问一次              │              │
│  └────────────────────────────────────────┘              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. VSCode 安装指南（Windows / macOS / Linux 三平台）

### 3.1 下载与安装

| 平台 | 安装方式 | 注意事项 |
|------|----------|----------|
| **Windows 10/11** | 1. 浏览器打开 https://code.visualstudio.com <br> 2. 下载 Windows Installer (.exe) <br> 3. 双击运行，勾选以下选项：<br> - "添加到 PATH"（必须勾选）<br> - "将 Code 打开操作添加到文件夹右键菜单"（推荐）<br> - "注册为受支持文件类型的编辑器"（推荐）<br> 4. 完成安装后重启终端 | 如忘记勾选"添加到 PATH"，可手动将 `C:\Users\[用户名]\AppData\Local\Programs\Microsoft VS Code\bin` 添加到系统环境变量 Path 中 |
| **macOS 12+** | 1. 浏览器打开 https://code.visualstudio.com <br> 2. 下载 Mac 版本 (.zip) <br> 3. 解压后将 Visual Studio Code.app 拖入 Applications 文件夹 <br> 4. 打开后按 `Cmd+Shift+P` → 输入 `Shell Command: Install 'code' command in PATH` → 回车 | 此步骤将使 `code` 命令在终端中可用，强烈建议执行 |
| **Linux (Ubuntu/Debian)** | 方法一（图形界面）：<br> 从 https://code.visualstudio.com 下载 .deb 包，双击安装<br><br> 方法二（命令行）：<br> `sudo apt update` <br> `sudo apt install wget gpg` <br> `wget -qO- https://packages.microsoft.com/keys/microsoft.asc \| gpg --dearmor > packages.microsoft.gpg` <br> `sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg` <br> `sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'` <br> `sudo apt update` <br> `sudo apt install code` | 推荐方法二（命令行），可自动处理 GPG 密钥和软件源 |
| **Linux (Fedora/RHEL)** | `sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc` <br> `sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'` <br> `sudo dnf check-update` <br> `sudo dnf install code` | 亦可通过 Flatpak：`flatpak install flathub com.visualstudio.code` |

### 3.2 安装后验证

```bash
# 在终端中执行
code --version
# 预期输出示例：1.97.0 x64

# 测试启动（在目标项目目录中）
cd /path/to/your/project
code .
# 应打开 VSCode 并自动加载当前目录
```

### 3.3 首次配置建议

```
VSCode → 左下角齿轮图标 → Settings → 搜索以下设置项：

┌────────────────────────────────────────────────────────────┐
│ 设置项                          │ 推荐值      │ 原因        │
├─────────────────────────────────┼────────────┼─────────────┤
│ Editor: Font Size               │ 14-16       │ 舒适阅读    │
│ Editor: Tab Size                │ 4           │ Python 标准 │
│ Editor: Render Whitespace       │ boundary    │ 便于发现缩进│
│                                     │ 错误        │
│ Files: Auto Save                │ afterDelay  │ 防止丢失    │
│ Terminal: Integrated Font Size  │ 13-14       │ 终端可读性  │
│ Editor: Minimap                 │ off (可选)  │ 减少干扰    │
└────────────────────────────────────────────────────────────┘
```

---

## 4. 必装插件清单

### 4.1 核心插件详情

| 插件名称 | 插件ID | 用途 | 必装程度 | 免费/付费 | 配置复杂度 |
|----------|--------|------|----------|-----------|-----------|
| **Cline** | `saoudrizwan.claude-dev` | VSCode 中的 AI Agent。可读取项目文件、编写代码、执行终端命令、自主 Debug。支持 Claude/DeepSeek/OpenAI 等多种 API。是目前 VSCode 中最强大的 AI 编码 Agent。 | **必装** | 免费（需自带 API Key） | 中等 |
| **Continue** | `Continue.continue` | 开源 AI 编程助手。支持对话式编程 + 行内补全 + 多模型自由切换。可在同一对话中切换 Claude 和 DeepSeek。最大优势：免费开源，模型切换灵活。 | **必装** | 免费（需自带 API Key） | 低-中 |
| **Python** | `ms-python.python` | Microsoft 官方 Python 语言支持。语法高亮、智能补全、调试器、测试运行器、虚拟环境自动检测。Python 开发的必备基础插件。 | **必装** | 免费 | 最低 |
| **GitHub Copilot** | `GitHub.copilot` | GitHub 官方 AI 代码补全。在编辑器中以灰色文字实时建议下一行代码。支持几乎所有主流编程语言。 | **推荐** | $10/月（学生免费） | 最低 |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | GitHub Copilot 的对话版本，与 Continue 功能重叠。已有 Cline 可跳过。 | **可选** | $10/月 | 最低 |
| **Prettier** | `esbenp.prettier-vscode` | 代码格式化工具，支持 HTML/CSS/JS/JSON/Markdown/YAML 等多种格式。保存时自动格式化。 | **推荐** | 免费 | 最低 |
| **Pylance** | `ms-python.vscode-pylance` | Python 语言服务器，提供更快的智能补全和类型检查。安装 Python 插件时通常自动安装。 | **必装** | 免费 | 无需配置 |

### 4.2 插件安装方式

```
方式一：GUI 安装（推荐）
  VSCode 左侧边栏 → Extensions 图标（或 Ctrl+Shift+X）
  → 搜索框输入插件名称 → 点击 Install

方式二：命令行安装
  code --install-extension saoudrizwan.claude-dev
  code --install-extension Continue.continue
  code --install-extension ms-python.python
  code --install-extension GitHub.copilot
  code --install-extension esbenp.prettier-vscode

方式三：批量安装
  将以下内容保存为 install-extensions.sh：
  #!/bin/bash
  extensions=(
    "saoudrizwan.claude-dev"
    "Continue.continue"
    "ms-python.python"
    "GitHub.copilot"
    "esbenp.prettier-vscode"
  )
  for ext in "${extensions[@]}"; do
    code --install-extension "$ext"
  done
```

---

## 5. Cline 插件配置详解

### 5.1 Cline 全局架构与配置入口

```
Cline 配置入口：
  VSCode 左侧边栏 → Cline 图标（机器人图标）
  → 点击右上角齿轮 ⚙ → 进入 API Provider 配置界面
```

### 5.2 配置 Claude API

**第一步：获取 Anthropic API Key**

```
1. 浏览器打开 https://console.anthropic.com
2. 注册/登录 Anthropic 账号
3. 进入 Dashboard → API Keys → Create Key
4. 输入 Key 名称（如 "cline-vscode"）
5. 复制生成的 sk-ant-api03-xxx... 密钥
   ⚠️ 此密钥仅显示一次，务必安全保存
6. 充值：进入 Billing 页面，绑定信用卡或使用预付费额度
   建议初始充值 $25（约 180 元人民币）
```

**第二步：在 Cline 中配置**

```
VSCode → Cline 面板 → 齿轮图标 → 配置界面：

┌─────────────────────────────────────────────────────┐
│ API Provider:     Anthropic                         │
│                                                     │
│ API Key:          sk-ant-api03-xxxxxxxxxxxxx        │
│                   (粘贴你的 API Key)                 │
│                                                     │
│ Model:            Claude Sonnet 5                    │
│                   (推荐，性价比最优)                   │
│                                                     │
│ Alternative:      Claude Opus 5                      │
│                   (最强推理，复杂任务/架构设计时切换)  │
└─────────────────────────────────────────────────────┘
```

**Claude Model 选择决策矩阵**：

```
┌────────────────────────────────────────────────────────────────────┐
│ 任务类型              │ 推荐 Model          │ 原因                    │
├───────────────────────┼─────────────────────┼─────────────────────────┤
│ 日常代码编写/修改     │ Sonnet 5            │ 速度快、成本适中         │
│ 代码审查/重构         │ Sonnet 5            │ 质量足够，无需 Opus      │
│ 复杂 Debug（多文件）  │ Opus 5              │ 需要最强推理能力         │
│ 系统架构设计          │ Opus 5              │ 需要深度思考             │
│ 简单脚本生成          │ Sonnet 5            │ 速度快、成本低           │
│ 文档撰写/翻译         │ Sonnet 5            │ 性能完全足够             │
│ 批量小任务(>50次/天)  │ Sonnet 5 + DeepSeek │ 控制成本                 │
│ 学习/实验/初期探索    │ Sonnet 5            │ 性价比最佳入门选择       │
└────────────────────────────────────────────────────────────────────┘

价格参考（2026年8月，以 Anthropic 官网为准）：
  - Claude Sonnet 5: ~$3/百万输入 Token, ~$15/百万输出 Token
  - Claude Opus 5:   ~$15/百万输入 Token, ~$75/百万输出 Token
  - 典型编码对话单次消耗: 5K ~ 50K Token
```

### 5.3 配置 DeepSeek API

**第一步：获取 DeepSeek API Key**

```
1. 浏览器打开 https://platform.deepseek.com
2. 注册/登录 DeepSeek 开发者账号（支持中国手机号）
3. 进入 API Keys → 创建新 Key
4. 复制 sk-xxx... 密钥
5. 新用户通常有免费额度（¥10-30 不等）
6. 如需充值：支持支付宝/微信支付
   价格参考：~¥1/百万输入 Token, ~¥2/百万输出 Token
   （约为 Claude Sonnet 价格的 1/30 ~ 1/50）
```

**第二步：在 Cline 中配置**

```
VSCode → Cline 面板 → 齿轮图标 → 配置界面：

┌─────────────────────────────────────────────────────┐
│ API Provider:     OpenAI Compatible                  │
│                                                     │
│ Base URL:         https://api.deepseek.com          │
│                                                     │
│ API Key:          sk-xxxxxxxxxxxxxxxxxxxxxxxx        │
│                   (粘贴你的 DeepSeek API Key)         │
│                                                     │
│ Model ID:         deepseek-chat                      │
│                   (通用对话模型)                      │
│                                                     │
│ Alternative:      deepseek-reasoner                  │
│                   (深度推理模型，数学/逻辑任务)       │
└─────────────────────────────────────────────────────┘
```

**Cline 中 Claude 与 DeepSeek 的配合策略**：

```
┌──────────────────────────────────────────────────────────────┐
│                    双模型切换策略                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Claude (Sonnet/Opus)              DeepSeek                  │
│  适用场景：                       适用场景：                   │
│  • 复杂代码架构设计               • 中文文档/注释生成          │
│  • 多文件重构                     • 简单代码片段              │
│  • 复杂 Bug 追踪                  • 批量重复任务              │
│  • 长文本分析（200K context）     • 成本敏感的大量对话        │
│  • 对代码质量要求极高的场景       • 日常问答和学习辅助        │
│                                                              │
│  切换方式：Cline 齿轮 → 切换 API Provider 即可               │
│  成本对比：Claude Sonnet 成本约为 DeepSeek 的 30~50 倍       │
│                                                              │
│  建议比例：复杂任务 100% Claude | 常规任务 30% Claude +       │
│            70% DeepSeek | 学习探索 10% Claude + 90% DeepSeek  │
└──────────────────────────────────────────────────────────────┘
```

### 5.4 Cline 配置完整步骤总结

```
步骤清单（按顺序执行）：

□ 1. 确认 VSCode 已安装且能正常启动
□ 2. 安装 Cline 插件（VSCode → Extensions → 搜索 "Cline" → Install）
□ 3. 注册 Anthropic 账号，获取 Claude API Key
□ 4. 注册 DeepSeek 开发者账号，获取 DeepSeek API Key
□ 5. 在 Cline 中分别配置 Claude 和 DeepSeek 两个 API Provider
□ 6. 将默认 Provider 设为 Claude（质量优先）或 DeepSeek（成本优先）
□ 7. 发送第一个 Prompt 测试（见第 8 节）
```

---

## 6. Continue 插件配置详解（双模型切换方案）

### 6.1 Continue 定位

Continue 是 VSCode 中最流行的开源 AI 编程助手。与 Cline 的核心区别：

```
┌─────────────────────────────────────────────────────────────────┐
│ 对比维度          │ Cline                    │ Continue           │
├───────────────────┼──────────────────────────┼────────────────────┤
│ 核心定位          │ AI Agent（自主执行任务）  │ AI 助手（对话+补全）│
│ 文件操作          │ 可读/写/搜索项目文件     │ 读当前文件/选区     │
│ 终端操作          │ 可执行终端命令            │ 不可执行终端        │
│ 多模型切换        │ 手动切换 Provider         │ 对话中随时切换      │
│ 代码补全          │ 无                        │ Tab 键补全         │
│ 开源许可          │ Apache 2.0                │ Apache 2.0         │
│ 学习成本          │ 中                        │ 低                 │
│ 适合角色          │ 主力编码 Agent            │ 日常编程助手 +     │
│                   │                           │ 多模型对比使用     │
└─────────────────────────────────────────────────────────────────┘

使用建议：
  Cline (主力) + Continue (辅助) 组合安装，互补而非互斥。
  日常小任务用 Continue 快速问答，大任务用 Cline 自主执行。
```

### 6.2 Continue config.json 完整示例

**配置文件路径**：

```
Windows: %USERPROFILE%\.continue\config.json
macOS:   ~/.continue/config.json
Linux:   ~/.continue/config.json
```

**完整配置**：

```json
{
  "models": [
    {
      "title": "Claude Sonnet 5",
      "provider": "anthropic",
      "model": "claude-sonnet-5-20251001",
      "apiKey": "sk-ant-api03-your-anthropic-key-here",
      "roles": ["chat"]
    },
    {
      "title": "Claude Opus 5",
      "provider": "anthropic",
      "model": "claude-opus-5-20251001",
      "apiKey": "sk-ant-api03-your-anthropic-key-here",
      "roles": ["chat"]
    },
    {
      "title": "DeepSeek V3",
      "provider": "openai",
      "model": "deepseek-chat",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "sk-your-deepseek-key-here",
      "roles": ["chat"]
    },
    {
      "title": "DeepSeek Reasoner",
      "provider": "openai",
      "model": "deepseek-reasoner",
      "apiBase": "https://api.deepseek.com",
      "apiKey": "sk-your-deepseek-key-here",
      "roles": ["chat"]
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek V3",
    "provider": "openai",
    "model": "deepseek-chat",
    "apiBase": "https://api.deepseek.com",
    "apiKey": "sk-your-deepseek-key-here"
  },
  "contextProviders": [
    { "name": "diff" },
    { "name": "file" },
    { "name": "terminal" },
    { "name": "codebase" }
  ],
  "slashCommands": [
    { "name": "edit", "description": "Edit selected code" },
    { "name": "comment", "description": "Write comments for the selected code" },
    { "name": "test", "description": "Generate unit tests" },
    { "name": "fix", "description": "Fix code issues" },
    { "name": "explain", "description": "Explain selected code" }
  ],
  "ui": {
    "showChatScrollbar": true
  },
  "experimental": {
    "defaultContext": 20
  }
}
```

**配置项说明**：

| 配置项 | 说明 |
|--------|------|
| `models[].title` | 在 Continue 界面中显示的名称，可自定义 |
| `models[].provider` | API 提供商类型。`anthropic` 直接使用 Anthropic SDK，`openai` 兼容 OpenAI 格式的 API（DeepSeek 使用此格式） |
| `models[].roles` | `["chat"]` 用于对话，`["autocomplete"]` 用于代码补全，可同时配置两者 |
| `tabAutocompleteModel` | 行内代码补全使用的默认模型。建议用 DeepSeek（成本低、触发频繁） |
| `contextProviders` | 启用的上下文提供者：diff（git差异）、file（当前文件）、terminal（终端输出）、codebase（项目级检索） |
| `slashCommands` | 在对话框中可用的快捷命令，如 `/edit`、`/test`、`/fix` |

### 6.3 Continue 双模型切换操作

```
在 Continue 对话界面中：

1. 对话框底部 → 点击当前模型名称（如 "Claude Sonnet 5"）
2. 从下拉菜单选择目标模型（如 "DeepSeek V3"）
3. 继续对话 —— 新消息将使用切换后的模型

典型切换流程：
  第1轮（Claude）：分析需求、设计架构
  第2轮（切换 DeepSeek）：生成中文注释和文档字符串
  第3轮（切换 Claude）：代码审查和质量把关
```

---

## 7. 备选方案：WorkBuddy + 大模型对比表

### 7.1 什么是 WorkBuddy

WorkBuddy 是一款独立的桌面 AI 工作助手，运行在操作系统层面（非 VSCode 插件），可以操作桌面文件、控制常用应用、执行系统级任务。

### 7.2 方案对比

```
┌───────────────────────────────────────────────────────────────────────┐
│ 对比维度           │ VSCode + Cline/Continue  │ WorkBuddy              │
├────────────────────┼──────────────────────────┼────────────────────────┤
│ 产品形态           │ IDE 插件                  │ 独立桌面应用            │
│ 主要场景           │ 编码、项目开发            │ 通用工作（文件/邮件/   │
│                    │                          │ 日程/网页操作）         │
│ 文件操作范围       │ 项目目录内所有文件        │ 桌面级文件系统访问      │
│ 终端/Shell 访问     │ 可在 VSCode 终端执行命令  │ 系统级命令执行          │
│ 模型支持           │ Claude / DeepSeek /      │ 多模型 API 接入         │
│                    │ OpenAI / Gemini / 本地   │                        │
│ 安装门槛           │ 低（插件一键安装）        │ 中（独立安装 + 配置）   │
│ 适用人群           │ 需要写代码的开发者        │ 需要通用 AI 助手的       │
│                    │ 和需要理解代码的管理者    │ 非开发者/管理者         │
│ 价格               │ 免费（仅 API 费用）       │ 免费（仅 API 费用）     │
│ 中文支持           │ 良好                     │ 良好                   │
│ 学习曲线           │ 1-2 天                   │ 0.5-1 天               │
│ 编码能力           │ 极强（项目上下文感知）    │ 一般（无项目级上下文）  │
└───────────────────────────────────────────────────────────────────────┘
```

### 7.3 WorkBuddy 配置步骤（作为备选方案）

```
1. 浏览器打开 https://workbuddy.ai
2. 下载对应系统的桌面应用安装包
3. 安装后启动 → 进入 Settings → API Configuration
4. 填入 API 信息：
   - DeepSeek API Key（推荐，国内可用，低成本）
   - 或 Claude API Key
5. 选择默认模型
6. 配置权限：WorkBuddy 需要授予屏幕录制/辅助功能等系统权限
   （macOS: System Preferences → Privacy & Security → Accessibility）

适用场景示例：
  - "帮我整理桌面上的文件，按项目分类到不同文件夹"
  - "读取当前网页内容，总结为3个要点"
  - "帮我回复这封邮件，语气专业但友好"
  - "搜索本地文档中所有提到'Q3预算'的文件"
```

### 7.4 方案选择决策树

```
你主要需要写代码吗？
├─ 是 → VS Code + Cline（主力）+ Continue（辅助）
│         └─ 需要额外的通用桌面助手？
│              ├─ 是 → 加装 WorkBuddy
│              └─ 否 → 当前方案已足够
│
└─ 否 → 你的主要工作场景是？
         ├─ 文档/邮件/文件管理 → WorkBuddy + 网页版 ChatGPT/Claude
         ├─ 数据分析/Python脚本 → VSCode + Cline（学一点基础）
         └─ 纯粹的知识问答/学习 → 网页版 AI 工具即可
```

---

## 8. 环境验证：发送第一个编程 Prompt 测试

### 8.1 测试步骤

```
步骤 1: 创建测试文件
  在 VSCode 中新建文件 → 保存为 test_ai.py

步骤 2: 打开 Cline 对话面板
  点击左侧 Cline 图标

步骤 3: 在 Cline 对话框中输入以下 Prompt：

═══════════════════════════════════════════════════════════
请用 Python 写一个简单的函数，功能是：

输入：一个数字列表（可能包含整数和浮点数）
输出：平均值和中位数（返回一个字典）

要求：
1. 代码使用中文注释，说明每一步在做什么
2. 处理空列表的边界情况（返回 None）
3. 包含一个 if __name__ == '__main__' 测试块，
   用至少 3 组不同的测试数据验证函数正确性
4. 遵循 PEP 8 代码风格规范
═══════════════════════════════════════════════════════════

步骤 4: 观察 Cline 的行为
  - Cline 会自动读取 test_ai.py
  - Cline 会生成代码并写入文件（或展示代码供你确认）
  - 如果 Cline 请求权限（写入文件/执行终端），点击 Allow 或确认

步骤 5: 让 Cline 执行代码

  继续在 Cline 对话框中输入：

  帮我在终端中运行这段代码，看看输出是否正确。

  Cline 将自动执行 python test_ai.py 并展示终端输出。

步骤 6: 验证结果
  检查终端输出中的平均值和中位数是否计算正确。
```

### 8.2 测试成功的标志

```
✅ Cline 成功生成了符合要求的 Python 代码
✅ 代码包含中文注释
✅ 代码处理了空列表的边界情况
✅ 代码包含测试块
✅ Cline 成功在终端中执行了代码
✅ 终端输出了正确的计算结果

如果以上全部通过 → 环境配置成功！
```

### 8.3 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Cline 提示 API Key 无效 | Key 复制有误或已过期 | 重新生成 Key 并复制（确认无多余空格） |
| Cline 提示余额不足 | API 账户未充值/额度用完 | 登录对应平台充值或检查剩余额度 |
| Cline 无法写入文件 | 文件权限设置过于严格 | 在 Cline 权限设置中开启 Write 权限 |
| Python 执行报错 "No module named python" | Python 未添加至 PATH | `python --version` 验证，如无则重新安装 Python 并勾选 "Add to PATH" |
| DeepSeek API 连接超时 | 网络问题（国内访问） | 检查网络，或切换到手机热点测试 |
| Cline 响应很慢 | 模型负载高峰或网络延迟 | 等待或切换到 DeepSeek（国内响应更快） |

### 8.4 进阶测试（环境确认后可选）

```
测试 1: 多文件操作
  Prompt: "在当前目录下创建一个 utils 文件夹，在 utils 里新建 math_helpers.py，
          将刚才的统计函数移到这个文件中，然后在 test_ai.py 中导入并使用它。"

测试 2: Debug 能力
  Prompt: "在 test_ai.py 中故意写一个会导致除零错误的代码，
          然后让 Cline 找出并修复这个 Bug。"

测试 3: 数据库连接（如已安装 MySQL）
  Prompt: "帮我写一个 Python 脚本，连接到本地 MySQL 数据库，
          执行一条简单的查询，并打印结果。"
```

---

## 9. 企业视角：团队 AI 开发环境标准化建议

### 9.1 企业级 AI 开发环境成熟度模型

```
┌───────────────────────────────────────────────────────────────────┐
│               团队 AI 开发环境标准化成熟度                          │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Level 3: 企业级管理                                              │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 统一 API Key 管理（密钥轮换、用量监控、预算告警）         │   │
│  │ • 代码审查集成（AI 生成代码必须经过 Code Review）           │   │
│  │ • 内部 Prompt 库（团队共享的 RCTE 模板）                    │   │
│  │ • 安全策略（禁止向 AI 发送的敏感信息清单）                  │   │
│  │ • 用量分析（按团队/项目/人员维度的 API 用量报告）           │   │
│  └───────────────────────────────────────────────────────────┘   │
│        ↑                                                          │
│  Level 2: 团队标准化                                              │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 统一开发环境配置（VSCode + 指定插件清单）                 │   │
│  │ • 统一 AI 工具选型（主力模型 + 备份模型）                   │   │
│  │ • 新人入职 30 分钟上手（一键配置脚本）                      │   │
│  │ • 团队共享的 .vscode/settings.json 和插件推荐文件           │   │
│  └───────────────────────────────────────────────────────────┘   │
│        ↑                                                          │
│  Level 1: 个人使用                                                │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ • 各成员自行安装使用                                         │   │
│  │ • 无统一配置标准                                             │   │
│  │ • API Key 个人管理                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 9.2 团队标准化实践方案

**方案一：配置文件标准化**

```
在项目 Git 仓库中维护以下文件：

1. .vscode/extensions.json
{
  "recommendations": [
    "saoudrizwan.claude-dev",
    "Continue.continue",
    "ms-python.python",
    "esbenp.prettier-vscode"
  ],
  "unwantedRecommendations": []
}

2. .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "cline.preferredLanguage": "Chinese"
}

3. .claude/settings.json（Claude Code 配置，如使用）
{
  "permissions": {
    "allow": [
      "Bash(python:*)",
      "Bash(pip:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)",
      "Bash(drop:*)",
      "Bash(truncate:*)"
    ]
  }
}
```

**方案二：一键配置脚本**

```bash
#!/bin/bash
# setup-ai-env.sh —— 团队新成员的 AI 开发环境一键配置脚本

echo "===== AI 开发环境配置脚本 ====="

# 1. 检查 VSCode
if ! command -v code &> /dev/null; then
    echo "❌ VSCode 未安装，请先安装：https://code.visualstudio.com"
    exit 1
fi
echo "✅ VSCode 已安装"

# 2. 安装核心插件
echo "📦 安装核心插件..."
code --install-extension saoudrizwan.claude-dev
code --install-extension Continue.continue
code --install-extension ms-python.python
code --install-extension esbenp.prettier-vscode
echo "✅ 插件安装完成"

# 3. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 未安装，建议安装 Python 3.9+"
else
    echo "✅ Python $(python3 --version) 已安装"
fi

# 4. 创建推荐的 VSCode 配置（如果项目中不存在）
if [ ! -d ".vscode" ]; then
    mkdir -p .vscode
fi

cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "saoudrizwan.claude-dev",
    "Continue.continue",
    "ms-python.python",
    "esbenp.prettier-vscode"
  ]
}
EOF

echo ""
echo "===== 环境配置完成 ====="
echo ""
echo "下一步："
echo "1. 配置 Cline API Key（VSCode → Cline 面板 → 齿轮设置）"
echo "2. 确保 API 账户有余额"
echo "3. 发送第一个 Prompt 测试（参考团队文档）"
echo ""
echo "需要帮助请联系：[团队技术负责人]"
```

### 9.3 企业安全与成本管理建议

```
═══════════════════════════════════════════════════════════════════════
                      企业 AI 开发环境安全清单
═══════════════════════════════════════════════════════════════════════

API Key 管理：
  □ 使用企业级密钥管理服务（AWS Secrets Manager / HashiCorp Vault）
  □ 禁止将 API Key 硬编码在项目代码中
  □ 禁止将 API Key 提交到 Git 仓库
  □ 定期轮换 API Key（建议 90 天）
  □ 按团队/项目分配合不同的 API Key（便于成本追踪和问题隔离）

数据安全：
  □ 禁止向 AI 发送生产环境的真实客户 PII（个人身份信息）
  □ 建立敏感数据脱敏标准（正则替换 + 命名映射）
  □ 禁止向 AI 发送公司核心商业机密（算法、定价策略、
    未公开财务数据）
  □ 生产代码 Review 必须由人工完成，AI 只能作为辅助建议
  □ 所有 AI 生成的 SQL 在人工审核前不得对生产数据库执行

成本管理：
  □ 设置 API 用量告警（每日/每周预算上限）
  □ 区分任务级别的模型使用策略（见下方成本控制矩阵）
  □ 月度 AI API 费用纳入项目成本核算
  □ 鼓励高频简单任务使用 DeepSeek（成本约为 Claude 的 1/30-1/50）

成本控制矩阵：
┌─────────────────────┬──────────────┬────────────┬──────────┐
│ 任务类型             │ 推荐模型      │ 预估成本   │ 频率      │
├─────────────────────┼──────────────┼────────────┼──────────┤
│ 核心架构设计         │ Opus 5       │ ~$0.50/次  │ 2-5次/周  │
│ 日常编码/CR          │ Sonnet 5     │ ~$0.10/次  │ 20-50次/天│
│ 文档注释/简单脚本    │ DeepSeek     │ ~$0.01/次  │ 无限制    │
│ 自动补全触发         │ DeepSeek     │ ~$0.001/次 │ 数百次/天 │
│ 代码审查             │ Sonnet 5     │ ~$0.05/次  │ 10次/天   │
└─────────────────────┴──────────────┴────────────┴──────────┘
  预估月均成本（5人团队）：$150 ~ $400（含合理配置）
═══════════════════════════════════════════════════════════════════════
```

### 9.4 团队推广路线图

```
第 1 周：试点
  - 选择 2-3 名技术骨干先行试用
  - 完成 VSCode + Cline + DeepSeek 配置
  - 收集初始使用反馈和典型场景

第 2-3 周：标准化
  - 基于试点反馈编写团队 AI 开发环境标准文档
  - 打磨一键配置脚本和推荐插件清单
  - 建立内部 Prompt 模板库初稿（10个高频场景）

第 4 周：推广
  - 组织 60 分钟团队 Workshop（30 分钟讲解 + 30 分钟实操）
  - 全员完成环境配置
  - 建立 Slack/飞书 AI 使用技巧分享频道

第 5-8 周：深化
  - 每周收集匿名使用反馈，迭代标准文档
  - 按任务类型统计 AI 使用率和采纳率
  - 每月分享一个"最佳 AI Prompt"案例

持续：
  - 关注 Cline/Continue 等工具版本更新
  - 关注模型新版本发布（性能提升 / 价格下降）
  - 每季度举办一次 AI 使用技巧分享会
```

---

> **关联知识块**：KB5（Prompt Engineering 实战详解） — 环境搭建完成后，结合 RCTE 框架和 8 大 Prompt 技巧，在 Cline 中开始系统化的 AI 辅助编程实践。
>
> **下一知识点**：完成 KB5 + KB6 后，进入实操环节 —— 基于 Prompt Engineering 安全操作 MySQL 数据库（本课第七节）。
