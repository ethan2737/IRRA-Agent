# Deep Search Agent 配置文件模板
# 复制此文件为 config.py 并填入您的真实 API 密钥

# DeepSeek API Key
# 获取地址：https://platform.deepseek.com/
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key-here"

# OpenAI API Key (可选，如果使用 DeepSeek 则不需要)
# 获取地址：https://platform.openai.com/
OPENAI_API_KEY = "sk-your-openai-api-key-here"

# Tavily 搜索 API Key
# 获取地址：https://app.tavily.com/
TAVILY_API_KEY = "tvly-your-tavily-api-key-here"

# 配置参数
# 默认模型提供商 (deepseek 或 openai)
DEFAULT_LLM_PROVIDER = "deepseek"

# DeepSeek 模型
DEEPSEEK_MODEL = "deepseek-chat"

# OpenAI 模型
OPENAI_MODEL = "gpt-4o-mini"

# 最大反思次数
MAX_REFLECTIONS = 3

# 每个查询的搜索结果数
SEARCH_RESULTS_PER_QUERY = 5

# 搜索内容最大长度 (字符)
SEARCH_CONTENT_MAX_LENGTH = 20000

# 输出目录
OUTPUT_DIR = "reports"

# 是否保存中间状态
SAVE_INTERMEDIATE_STATES = True
