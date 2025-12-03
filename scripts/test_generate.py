"""测试脚本 - 只处理2天数据验证流程"""
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from scripts.generate_training_data import TrainingDataGenerator
from config import PROCESSED_DATA_DIR, TRAINING_DATA_DIR
from loguru import logger

def test_with_two_days():
    """测试：只用前2天数据"""
    logger.info("=" * 60)
    logger.info("测试模式：只处理前2天数据")
    logger.info("=" * 60)
    
    generator = TrainingDataGenerator()
    
    # 加载语料
    corpus_file = PROCESSED_DATA_DIR / "parsed_corpus.json"
    with open(corpus_file, 'r', encoding='utf-8') as f:
        all_corpus = json.load(f)
    
    # 只取前2天
    test_corpus = all_corpus[:2]
    logger.info(f"测试数据: {[item['date'] for item in test_corpus]}")
    
    # 临时保存测试语料
    test_corpus_file = PROCESSED_DATA_DIR / "test_corpus.json"
    with open(test_corpus_file, 'w', encoding='utf-8') as f:
        json.dump(test_corpus, f, ensure_ascii=False, indent=2)
    
    # 修改生成器读取测试数据
    original_method = generator.load_parsed_corpus
    def load_test_corpus():
        return test_corpus
    generator.load_parsed_corpus = load_test_corpus
    
    # 生成训练数据
    training_data = generator.generate_all_training_data()
    
    # 保存测试结果
    test_output = TRAINING_DATA_DIR / "test_training_dataset.json"
    with open(test_output, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    logger.info("=" * 60)
    logger.info(f"测试完成！生成了 {len(training_data)} 个训练样本")
    logger.info(f"测试结果保存到: {test_output}")
    logger.info("=" * 60)
    
    # 打印样本示例
    if training_data:
        logger.info("\n示例样本:")
        logger.info(json.dumps(training_data[0], ensure_ascii=False, indent=2))
    
    return len(training_data) > 0

if __name__ == "__main__":
    success = test_with_two_days()
    sys.exit(0 if success else 1)

