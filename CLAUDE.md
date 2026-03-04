# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**Deep Search Agent** 是一个无框架的深度搜索AI代理实现，用于生成高质量的研究报告。它采用多轮搜索和反思机制，通过整合多个信息源来提供全面、深入的研究结果。

## 核心架构

项目采用分层节点式架构：

- **控制层**: `DeepSearchAgent` 主控制器，协调整个研究流程
- **处理层**: 各种功能节点 (`ReportStructureNode`, `FirstSearchNode`, `ReflectionNode` 等)
- **模型层**: LLM抽象层 (`BaseLLM`, `DeepSeekLLM`, `OpenAILLM`)
- **工具层**: 搜索工具 (`tavily_search`) 和文本处理
- **状态层**: 状态管理和持久化 (`State`, `Paragraph`, `Research`)

## 常用开发命令

### 环境设置
```bash
# 安装依赖
pip install -r requirements.txt

# 创建输出目录
mkdir reports
```

### 运行示例
```bash
# 基本使用示例
python examples/basic_usage.py

# 高级使用示例
python examples/advanced_usage.py

# Web界面
streamlit run examples/streamlit_app.py
```

### 测试和调试
```bash
# 测试基本功能
python -c "from src import create_agent; agent = create_agent(); print('Agent created successfully')"

# 验证配置
python -c "from src.utils import load_config; config = load_config(); print(f'LLM Provider: {config.default_llm_provider}')"
```

## 核心工作流程

1. **结构生成**: `ReportStructureNode` 根据查询生成报告大纲
2. **初始研究**: `FirstSearchNode` 为每个段落生成搜索查询
3. **初始总结**: `FirstSummaryNode` 基于搜索结果生成段落初稿
4. **反思优化**: `ReflectionNode` 多轮反思发现遗漏并补充搜索
5. **最终整合**: `ReportFormattingNode` 整合所有段落为完整报告

## 配置管理

配置文件位于 `config.py`，主要参数：

- `MAX_REFLECTIONS`: 反思轮次 (默认2)
- `SEARCH_RESULTS_PER_QUERY`: 每查询搜索结果数 (默认3)
- `SEARCH_CONTENT_MAX_LENGTH`: 搜索内容长度限制 (默认20000)
- `DEFAULT_LLM_PROVIDER`: 默认LLM提供商 (默认"deepseek")
- `OUTPUT_DIR`: 报告输出目录 (默认"reports")

## 代码结构重点

### 主要模块
- `src/agent.py`: 主Agent类，核心协调逻辑
- `src/llms/`: LLM抽象层，支持DeepSeek和OpenAI
- `src/nodes/`: 处理节点，每个节点负责特定任务
- `src/state/state.py`: 状态数据结构，支持进程恢复
- `src/tools/search.py`: Tavily搜索集成
- `src/utils/config.py`: 配置管理

### 关键设计模式
- **节点模式**: 每个处理步骤封装为独立节点
- **状态模式**: 完整的状态跟踪和恢复机制
- **策略模式**: LLM提供商可插拔切换
- **工厂模式**: 配置和Agent创建的便捷接口

## 扩展指南

### 添加新LLM提供商
1. 继承 `src/llms/base.py` 中的 `BaseLLM` 类
2. 实现 `call_llm` 方法
3. 在 `src/agent.py` 的 `_initialize_llm` 方法中添加支持

### 自定义处理节点
1. 继承 `src/nodes/base_node.py` 中的 `BaseNode` 类
2. 实现 `process` 方法
3. 在 `src/agent.py` 中集成新节点

### 修改搜索逻辑
- 主要搜索实现在 `src/tools/search.py`
- 可以替换Tavily搜索或添加其他搜索引擎

## 常见问题解决

### API密钥配置
- 编辑 `config.py` 文件
- 设置 `DEEPSEEK_API_KEY` 和 `TAVILY_API_KEY`
- 可选设置 `OPENAI_API_KEY`

### 状态文件管理
- 状态文件保存在 `reports/` 目录
- 使用 `agent.save_state()` 和 `agent.load_state()` 管理状态
- 支持中断恢复和研究进度跟踪

### 性能优化
- 调整 `MAX_REFLECTIONS` 控制研究深度
- 调整 `SEARCH_RESULTS_PER_QUERY` 平衡质量和速度
- 使用更快的LLM模型提高响应速度

## 开发注意事项

- 项目采用无框架设计，避免重型依赖
- 所有模块高度解耦，便于测试和维护
- 支持中文和英文内容处理
- 状态文件使用JSON格式，便于调试
- 最终报告输出为Markdown格式