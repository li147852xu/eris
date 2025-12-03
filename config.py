"""配置文件"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
RAW_DATA_DIR = OUTPUT_DIR / "raw_data"
PROCESSED_DATA_DIR = OUTPUT_DIR / "processed_data"
TRAINING_DATA_DIR = OUTPUT_DIR / "training_data"
MODEL_DIR = PROJECT_ROOT / "models"
LOG_DIR = PROJECT_ROOT / "logs"

# 确保目录存在
for dir_path in [OUTPUT_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, TRAINING_DATA_DIR, MODEL_DIR, LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 数据爬取配置
MARKET_DATA_SOURCES = {
    "akshare": True,  # 免费，无需token
    "efinance": True,  # 免费，无需token
    "tushare": bool(TUSHARE_TOKEN),  # 需要token
}

# 股票指数代码
INDEX_CODES = {
    "上证指数": "000001",
    "深证成指": "399001", 
    "创业板指": "399006",
}

# 训练数据生成配置
TRAINING_CONFIG = {
    "model": "deepseek-chat",  # 用于生成训练数据的模型（DeepSeek）
    "temperature": 0.3,
    "max_tokens": 4000,
}

# 微调配置
FINETUNE_CONFIG = {
    "base_model": "Qwen/Qwen2.5-7B-Instruct",  # 基座模型
    "lora_r": 64,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "learning_rate": 2e-4,
    "num_epochs": 3,
    "batch_size": 4,
    "gradient_accumulation_steps": 8,
    "max_length": 2048,
}

