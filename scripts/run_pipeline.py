"""完整流程主控脚本"""
import sys
from pathlib import Path
from loguru import logger
import argparse

sys.path.append(str(Path(__file__).parent.parent))
from config import LOG_DIR

# 配置日志
logger.add(LOG_DIR / "pipeline.log", rotation="10 MB")

# 导入各个模块
from parse_corpus import CorpusParser
from fetch_market_data import MarketDataFetcher
from generate_training_data import TrainingDataGenerator


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='金融助手训练数据生成流程')
    parser.add_argument('--step', type=str, default='all',
                      choices=['all', 'parse', 'fetch', 'generate', 'train'],
                      help='执行步骤: all=全部, parse=解析语料, fetch=爬取数据, generate=生成训练数据, train=训练模型')
    parser.add_argument('--use-gpt', action='store_true',
                      help='使用GPT生成训练数据（需要API key）')
    parser.add_argument('--dates', nargs='+',
                      help='指定要爬取数据的日期列表（格式: YYYY-MM-DD）')
    return parser.parse_args()


def step_parse_corpus():
    """步骤1: 解析语料"""
    logger.info("=" * 50)
    logger.info("步骤1: 解析语料文件")
    logger.info("=" * 50)
    
    parser = CorpusParser()
    results = parser.parse_all()
    parser.save_parsed_data(results)
    
    logger.info(f"✓ 成功解析 {len(results)} 个语料文件")
    return results


def step_fetch_market_data(dates=None):
    """步骤2: 爬取市场数据"""
    logger.info("=" * 50)
    logger.info("步骤2: 爬取市场数据")
    logger.info("=" * 50)
    
    fetcher = MarketDataFetcher()
    
    if dates:
        target_dates = dates
    else:
        # 从解析的语料中提取日期
        import json
        from config import PROCESSED_DATA_DIR
        
        parsed_file = PROCESSED_DATA_DIR / "parsed_corpus.json"
        if parsed_file.exists():
            with open(parsed_file, 'r', encoding='utf-8') as f:
                corpus_data = json.load(f)
            target_dates = [item['date'] for item in corpus_data]
        else:
            logger.error("未找到解析后的语料文件，请先运行parse步骤")
            return
    
    logger.info(f"准备爬取 {len(target_dates)} 个日期的数据")
    
    success_count = 0
    for date in target_dates:
        try:
            logger.info(f"爬取 {date} 的数据...")
            data = fetcher.fetch_date_data(date)
            fetcher.save_market_data(date, data)
            success_count += 1
        except Exception as e:
            logger.error(f"爬取 {date} 数据失败: {e}")
    
    logger.info(f"✓ 成功爬取 {success_count}/{len(target_dates)} 个日期的数据")


def step_generate_training_data(use_gpt=False):
    """步骤3: 生成训练数据"""
    logger.info("=" * 50)
    logger.info("步骤3: 生成训练数据")
    logger.info("=" * 50)
    
    generator = TrainingDataGenerator()
    
    if use_gpt:
        logger.info("使用GPT生成训练数据")
        training_data = generator.generate_all_training_data()
    else:
        logger.info("使用简化方法生成训练数据")
        training_data = generator.generate_simple_training_data()
    
    generator.save_training_data(training_data)
    
    logger.info(f"✓ 成功生成 {len(training_data)} 个训练样本")


def step_train_model():
    """步骤4: 训练模型"""
    logger.info("=" * 50)
    logger.info("步骤4: 训练模型")
    logger.info("=" * 50)
    
    logger.info("请确保:")
    logger.info("1. 已安装所有依赖: pip install -r requirements.txt")
    logger.info("2. 有足够的GPU内存（建议16GB以上）")
    logger.info("3. 训练数据已生成")
    logger.info("\n运行训练命令:")
    logger.info("python scripts/train_model.py")
    
    # 可选：自动运行训练
    # from train_model import FinancialAssistantTrainer
    # trainer = FinancialAssistantTrainer()
    # trainer.train()


def main():
    """主函数"""
    args = parse_arguments()
    
    logger.info("金融助手训练数据生成流程")
    logger.info(f"执行步骤: {args.step}")
    
    try:
        if args.step in ['all', 'parse']:
            step_parse_corpus()
        
        if args.step in ['all', 'fetch']:
            step_fetch_market_data(args.dates)
        
        if args.step in ['all', 'generate']:
            step_generate_training_data(args.use_gpt)
        
        if args.step in ['all', 'train']:
            step_train_model()
        
        logger.info("\n" + "=" * 50)
        logger.info("流程完成！")
        logger.info("=" * 50)
        
        if args.step == 'all':
            logger.info("\n下一步:")
            logger.info("1. 检查生成的训练数据: outputs/training_data/")
            logger.info("2. 运行训练: python scripts/train_model.py")
            logger.info("3. 继续积累更多语料，重复此流程")
        
    except Exception as e:
        logger.error(f"流程执行失败: {e}")
        raise


if __name__ == "__main__":
    main()

