# Deep Search Agent - 深度研报 AI 助手

<div align="center">

🔍 告别漫无目的的搜索，迎接直达问题核心的深度研报

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 简介

**Deep Search Agent** 是一个无框架的深度搜索 AI 代理实现，用于生成高质量的研究报告。它采用多轮搜索和反思机制，通过整合多个信息源来提供全面、深入的研究结果。

### 核心特性

- 🧠 **多轮反思机制** - 自动发现知识盲点并进行补充搜索
- 📊 **结构化报告生成** - 智能生成报告大纲，分段深入研究
- 🔗 **多源信息整合** - 基于 Tavily 搜索整合多个权威信息源
- 📝 **状态持久化** - 支持中断恢复和研究进度跟踪
- 🎯 **可插拔 LLM** - 支持 DeepSeek、OpenAI 等多种模型
- 🖥️ **Web 界面** - 提供友好的 Streamlit Web 界面

---

## 项目结构

```
IRRA-Agent/
├── config.example.py       # 配置文件模板（可提交）
├── config.py               # 配置文件（已忽略，勿提交！）
├── requirements.txt          # Python 依赖
├── README.md                 # 项目文档
├── .gitignore                # Git 忽略文件
├── examples/                 # 使用示例
│   ├── basic_usage.py        # 基本使用示例
│   ├── advanced_usage.py     # 高级使用示例
│   └── streamlit_app.py      # Web 界面
└── src/                      # 源代码
    ├── agent.py              # 主 Agent 控制器
    ├── llms/                 # LLM 抽象层
    │   ├── base.py           # LLM 基类
    │   ├── deepseek.py       # DeepSeek 实现
    │   └── openai_llm.py     # OpenAI 实现
    ├── nodes/                # 处理节点
    │   ├── base_node.py      # 节点基类
    │   ├── report_structure_node.py  # 报告结构生成
    │   ├── search_node.py    # 搜索查询生成
    │   ├── summary_node.py   # 总结生成
    │   └── formatting_node.py # 报告格式化
    ├── state/                # 状态管理
    │   └── state.py          # 状态数据结构
    ├── tools/                # 工具层
    │   └── search.py         # Tavily 搜索集成
    ├── utils/                # 工具函数
    │   ├── config.py         # 配置管理
    │   └── text_processing.py # 文本处理
    └── prompts/              # 提示词模板
        └── prompts.py        # 系统提示词定义
```

---

## 快速开始

### 1. 环境要求

- Python 3.8+
- Tavily API 密钥（搜索）
- DeepSeek API 密钥 或 OpenAI API 密钥（LLM）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

> **安全提示**: 请勿将 `config.py` 提交到 git 仓库！`.gitignore` 已配置自动忽略此文件。

复制配置文件模板：
```bash
cp config.example.py config.py
```

然后编辑 `config.py` 文件，填入您的真实 API 密钥：
```python
# config.py
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key-here"  # 替换为真实密钥
TAVILY_API_KEY = "tvly-your-tavily-api-key-here"    # 替换为真实密钥
```

### 4. 运行示例

#### 基本使用

```bash
python examples/basic_usage.py
```

#### 高级使用（多任务、状态管理）

```bash
python examples/advanced_usage.py
```

#### Web 界面

```bash
streamlit run examples/streamlit_app.py
```

---

## 使用方法

### Python API 调用

```python
from src import DeepSearchAgent, load_config

# 加载配置
config = load_config()

# 创建 Agent
agent = DeepSearchAgent(config)

# 执行研究
query = "2025-2035 年适老化产业发展前景"
final_report = agent.research(query, save_report=True)

# 获取进度信息
progress = agent.get_progress_summary()
print(f"完成进度：{progress['progress_percentage']:.1f}%")
```

### 自定义配置

```python
from src import DeepSearchAgent, Config

# 创建自定义配置
config = Config(
    default_llm_provider="deepseek",
    max_reflections=3,           # 增加反思次数
    max_search_results=5,        # 更多搜索结果
    max_content_length=15000,
    output_dir="custom_reports"
)

# 设置 API 密钥
config.deepseek_api_key = "your_api_key"
config.tavily_api_key = "your_tavily_key"

# 创建 Agent 并执行研究
agent = DeepSearchAgent(config)
agent.research("您的研究问题")
```

### 状态管理（中断恢复）

```python
# 保存状态
agent.save_state("reports/state_backup.json")

# 加载状态（恢复研究）
new_agent = DeepSearchAgent(config)
new_agent.load_state("reports/state_backup.json")
```

---

## 核心工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. 报告结构生成 (ReportStructureNode)                       │
│     根据查询生成报告大纲和段落规划                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. 初始搜索与总结 (FirstSearchNode → FirstSummaryNode)      │
│     为每个段落生成搜索查询并总结                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 反思循环 (ReflectionNode → ReflectionSummaryNode)        │
│     多轮反思发现遗漏，补充搜索并更新总结                      │
│     循环次数：MAX_REFLECTIONS                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 最终报告整合 (ReportFormattingNode)                      │
│     将所有段落整合为完整报告                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `deepseek_api_key` | str | - | DeepSeek API 密钥 |
| `openai_api_key` | str | - | OpenAI API 密钥 |
| `tavily_api_key` | str | - | Tavily 搜索 API 密钥 |
| `default_llm_provider` | str | "deepseek" | 默认 LLM 提供商 |
| `max_reflections` | int | 2 | 最大反思轮次 |
| `max_search_results` | int | 3 | 每查询搜索结果数 |
| `max_content_length` | int | 20000 | 搜索内容最大长度 |
| `search_timeout` | int | 240 | 搜索超时（秒） |
| `output_dir` | str | "reports" | 报告输出目录 |
| `save_intermediate_states` | bool | true | 是否保存中间状态 |

---

## 扩展指南

### 添加新 LLM 提供商

1. 继承 `src/llms/base.py` 中的 `BaseLLM` 类
2. 实现 `invoke` 方法
3. 在 `src/agent.py` 的 `_initialize_llm` 方法中添加支持

### 自定义处理节点

1. 继承 `src/nodes/base_node.py` 中的 `BaseNode` 类
2. 实现 `process` 方法
3. 在 `src/agent.py` 中集成新节点

### 修改搜索逻辑

- 主要搜索实现在 `src/tools/search.py`
- 可以替换 Tavily 搜索或添加其他搜索引擎

---

## 示例查询

- "2025-2035 年适老化产业发展前景"
- "如何高效学习新知识"
- "人工智能发展趋势"
- "35 岁成年人通过自然习得方式学会英语的方法"
- "Web3 技术发展前景"

---

## 输出示例

运行成功后，报告将保存在 `reports/` 目录下：

```
reports/
├── deep_search_report_2025 适老化产业_20260304_143022.md
└── state_2025 适老化产业_20260304_143022.json
```

---

## 常见问题

### API 密钥配置

编辑 `config.py` 文件，设置 `DEEPSEEK_API_KEY` 和 `TAVILY_API_KEY`。

### 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 状态文件管理

- 状态文件保存在 `reports/` 目录
- 使用 `agent.save_state()` 和 `agent.load_state()` 管理状态
- 支持中断恢复和研究进度跟踪

---

## 技术栈

- **Python 3.8+** - 主要编程语言
- **OpenAI SDK** - LLM 调用（兼容 DeepSeek）
- **Tavily API** - 网络搜索
- **Streamlit** - Web 界面
- **Pydantic** - 数据验证

---

## 许可证

MIT License

---

## 反馈与支持

如有问题或建议，请提交 Issue 或联系项目维护者。
