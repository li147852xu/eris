"""自动生成训练数据脚本 - 使用GPT/Claude辅助生成"""
import json
import sys
import re
from pathlib import Path
from typing import Dict, List
from loguru import logger
import time
from tqdm import tqdm

# OpenAI是可选的，只有在使用GPT生成时才需要
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

sys.path.append(str(Path(__file__).parent.parent))
from config import (
    PROCESSED_DATA_DIR, RAW_DATA_DIR, TRAINING_DATA_DIR,
    OPENAI_API_KEY, OPENAI_BASE_URL, TRAINING_CONFIG, LOG_DIR
)

# 配置日志
logger.add(LOG_DIR / "generate_training.log", rotation="10 MB")


class TrainingDataGenerator:
    """训练数据生成器"""
    
    def __init__(self):
        if OPENAI_AVAILABLE and OPENAI_API_KEY:
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL
            )
            self.model = TRAINING_CONFIG["model"]
            self.temperature = TRAINING_CONFIG["temperature"]
            self.max_tokens = TRAINING_CONFIG["max_tokens"]
        else:
            self.client = None
            logger.warning("OpenAI不可用，将使用简化方法生成训练数据")
        
    def load_parsed_corpus(self) -> List[Dict]:
        """加载解析后的语料"""
        file_path = PROCESSED_DATA_DIR / "parsed_corpus.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_market_data(self, date: str) -> Dict:
        """加载市场数据"""
        file_path = RAW_DATA_DIR / f"market_data_{date}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_training_sample(self, corpus_item: Dict, market_data: Dict, section_name: str) -> List[Dict]:
        """生成单个训练样本"""
        date = corpus_item['date']
        section_content = corpus_item['sections'].get(section_name, '')
        
        if not section_content:
            return []
        
        # 构建prompt让GPT生成训练对
        prompt = self._build_generation_prompt(date, section_name, section_content, market_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的金融数据标注专家，擅长将市场数据和专家分析转换为结构化的训练数据。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 调试：打印API返回内容
            logger.debug(f"API返回内容前100字: {result_text[:100]}")
            
            # 尝试提取JSON（有时API会在代码块里返回）
            if '```json' in result_text:
                # 提取代码块中的JSON
                json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
                if json_match:
                    result_text = json_match.group(1)
            elif '```' in result_text:
                # 提取普通代码块
                json_match = re.search(r'```\s*(.*?)\s*```', result_text, re.DOTALL)
                if json_match:
                    result_text = json_match.group(1)
            
            # 解析返回的JSON
            training_samples = json.loads(result_text)
            
            if not isinstance(training_samples, list):
                logger.error(f"返回的不是数组: {type(training_samples)}")
                return []
            
            logger.info(f"✓ 生成 {len(training_samples)} 个样本 ({date} - {section_name})")
            return training_samples
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败 ({date} - {section_name}): {e}")
            logger.error(f"返回内容: {result_text[:500]}")
            return []
        except Exception as e:
            logger.error(f"生成失败 ({date} - {section_name}): {e}")
            return []
    
    def _extract_market_context_from_content(self, content: str, date: str) -> str:
        """从语料内容中智能提取市场背景信息"""
        import re
        
        contexts = []
        
        # 提取指数点位
        points = re.findall(r'(\d{4})点', content[:500])
        if points:
            contexts.append(f"指数点位约{points[0]}点")
        
        # 提取涨跌描述
        if '上涨' in content[:300] or '涨' in content[:300]:
            contexts.append("市场上涨")
        elif '下跌' in content[:300] or '跌' in content[:300]:
            contexts.append("市场下跌")
        elif '震荡' in content[:300]:
            contexts.append("市场震荡")
        
        # 提取成交量信息
        volume = re.findall(r'(\d+\.?\d*)万亿', content[:500])
        if volume:
            contexts.append(f"成交额{volume[0]}万亿")
        
        # 提取资金流向
        if '净流入' in content[:500]:
            contexts.append("资金净流入")
        elif '净流出' in content[:500]:
            contexts.append("资金净流出")
        
        return "。".join(contexts) if contexts else f"{date}市场数据"
    
    def _build_generation_prompt(self, date: str, section_name: str, content: str, market_data: Dict) -> str:
        """构建生成训练数据的prompt"""
        
        # 优先使用真实市场数据，否则从语料提取
        if market_data and market_data.get('indices'):
            market_info = self._format_market_data(market_data)
        else:
            market_info = self._extract_market_context_from_content(content, date)
        
        # 根据章节类型调整prompt
        section_prompts = {
            '早自习': {
                'context': '盘前预测',
                'questions': [
                    "今天大盘走势怎么看？",
                    "今天应该关注哪些板块？",
                    "今天有什么操作建议？",
                    "今天盘前怎么分析？"
                ]
            },
            '主1': {
                'context': '当日复盘',
                'questions': [
                    "今天市场表现如何？",
                    "今天资金流向哪里？",
                    "今天有什么值得注意的？",
                    "今天大盘走势怎么样？"
                ]
            },
            '主2': {
                'context': '明日预测',
                'questions': [
                    "明天大盘怎么看？",
                    "明天应该关注什么？",
                    "明天有什么操作建议？",
                    "明天市场怎么布局？"
                ]
            }
        }
        
        section_info = section_prompts.get(section_name, section_prompts['主1'])
        
        prompt = f"""请根据以下金融分析文章，生成4-5个高质量的问答训练样本。

**日期**: {date}
**文章类型**: {section_name}（{section_info['context']}）
**市场背景**: {market_info}

**专家分析原文**（节选）:
{content[:2500]}

**生成要求**:

1. **问题设计**：模拟真实用户提问，可参考：
{chr(10).join(['   - ' + q for q in section_info['questions']])}

2. **回答要求**：
   - 严格基于原文内容，不要编造
   - 必须保持原文独特风格：
     * "草原" 指代股市
     * "羊" 指代股票  
     * "吃桃" 指代亏损
     * "做T" 指代高抛低吸
     * 保持口语化、直白的表达
   - 结合市场背景给出具体建议
   - 回答长度150-300字

3. **输出格式**：
严格返回JSON数组，每个对象包含：
- instruction: 用户问题
- input: 市场背景（简短，1-2句话）
- output: 助手回答（保持原文风格，具体可操作）
- section_type: "{section_name}"
- date: "{date}"

**只返回JSON数组，不要有任何其他文字或解释。**
"""
        return prompt
    
    def _format_market_data(self, market_data: Dict) -> str:
        """格式化市场数据为文本"""
        if not market_data:
            return "暂无市场数据"
        
        lines = []
        
        # 指数数据
        if 'indices' in market_data and market_data['indices']:
            lines.append("**指数数据**:")
            for index_name, index_data in market_data['indices'].items():
                lines.append(f"- {index_name}: 收盘{index_data.get('close', 'N/A')}, "
                           f"涨跌幅{index_data.get('change_pct', 'N/A')}%")
        
        # 市场概况
        if 'market_overview' in market_data:
            overview = market_data['market_overview']
            if 'market_stats' in overview:
                stats = overview['market_stats']
                lines.append(f"\n**市场统计**: 上涨{stats.get('up_count', 'N/A')}家, "
                           f"下跌{stats.get('down_count', 'N/A')}家")
            if 'turnover' in overview:
                turnover = overview['turnover']
                lines.append(f"**成交额**: {turnover.get('amount', 'N/A')}{turnover.get('unit', '')}")
        
        # 资金流向
        if 'fund_flow' in market_data and market_data['fund_flow']:
            lines.append("\n**资金流向**:")
            for fund_type, fund_data in market_data['fund_flow'].items():
                lines.append(f"- {fund_type}: 净流入{fund_data.get('net_inflow', 'N/A')}{fund_data.get('unit', '')}")
        
        return '\n'.join(lines) if lines else "暂无详细市场数据"
    
    def generate_all_training_data(self) -> List[Dict]:
        """生成所有训练数据"""
        logger.info("开始生成训练数据（使用DeepSeek API）")
        
        # 加载解析后的语料
        corpus_data = self.load_parsed_corpus()
        logger.info(f"加载了 {len(corpus_data)} 个语料文件")
        
        all_training_samples = []
        total_sections = len(corpus_data) * 3  # 每天3个章节
        
        try:
            # 创建总进度条
            with tqdm(total=total_sections, desc="🤖 DeepSeek生成训练数据", 
                      unit="章节", colour="green") as pbar:
                
                for idx, corpus_item in enumerate(corpus_data):
                    date = corpus_item['date']
                    
                    # 尝试加载对应日期的市场数据（暂时跳过，使用语料信息）
                    market_data = self.load_market_data(date)
                    # if not market_data:
                    #     logger.debug(f"{date} 没有市场数据，将使用语料中的信息")
                    
                    # 为每个章节生成训练样本
                    for section_name in ['早自习', '主1', '主2']:
                        pbar.set_description(f"🤖 处理 {date} - {section_name}")
                        
                        samples = self.generate_training_sample(corpus_item, market_data, section_name)
                        all_training_samples.extend(samples)
                        
                        pbar.update(1)
                        pbar.set_postfix({"已生成样本": len(all_training_samples)})
                        
                        # 延迟避免API限流
                        time.sleep(0.5)
                    
                    # 每处理5天保存一次（防止中断丢失）
                    if (idx + 1) % 5 == 0:
                        self.save_training_data(all_training_samples, "training_dataset_backup.json")
                        logger.info(f"💾 已保存中间结果 ({idx+1}/{len(corpus_data)} 天)")
        
        except KeyboardInterrupt:
            logger.warning("⚠️ 检测到中断，保存已生成的数据...")
            if all_training_samples:
                self.save_training_data(all_training_samples, "training_dataset_interrupted.json")
                logger.info(f"已保存 {len(all_training_samples)} 个样本到 training_dataset_interrupted.json")
            raise
        
        logger.info(f"✅ 共生成 {len(all_training_samples)} 个训练样本")
        return all_training_samples
    
    def save_training_data(self, data: List[Dict], filename: str = "training_dataset.json"):
        """保存训练数据"""
        output_path = TRAINING_DATA_DIR / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"训练数据已保存到: {output_path}")
        
        # 同时保存为jsonl格式（微调常用格式）
        jsonl_path = TRAINING_DATA_DIR / filename.replace('.json', '.jsonl')
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"JSONL格式已保存到: {jsonl_path}")
    
    def generate_simple_training_data(self) -> List[Dict]:
        """生成简化版训练数据（不依赖GPT，直接从语料生成）"""
        logger.info("生成简化版训练数据（不使用API）")
        
        corpus_data = self.load_parsed_corpus()
        all_samples = []
        
        # 添加进度条
        for corpus_item in tqdm(corpus_data, desc="📝 生成简化训练数据", 
                                unit="文件", colour="blue"):
            date = corpus_item['date']
            sections = corpus_item['sections']
            
            # 早自习 -> 预测类问题
            if sections.get('早自习'):
                sample = {
                    "instruction": f"请分析{date}今天的市场走势，应该关注哪些方向？",
                    "input": f"日期：{date}",
                    "output": sections['早自习'][:500],  # 取前500字作为示例
                    "section_type": "早自习",
                    "date": date
                }
                all_samples.append(sample)
            
            # 主1 -> 复盘类问题
            if sections.get('主1'):
                sample = {
                    "instruction": f"请复盘{date}今天的市场表现",
                    "input": f"日期：{date}",
                    "output": sections['主1'][:500],
                    "section_type": "主1",
                    "date": date
                }
                all_samples.append(sample)
            
            # 主2 -> 明日预测问题
            if sections.get('主2'):
                sample = {
                    "instruction": f"{date}收盘后，明天应该如何布局？",
                    "input": f"日期：{date}",
                    "output": sections['主2'][:500],
                    "section_type": "主2",
                    "date": date
                }
                all_samples.append(sample)
        
        logger.info(f"✅ 生成了 {len(all_samples)} 个简化训练样本")
        return all_samples


def main():
    """主函数"""
    import sys
    generator = TrainingDataGenerator()
    
    # 检查命令行参数
    use_gpt = '--use-gpt' in sys.argv or '-g' in sys.argv
    
    # 如果没有指定参数，默认使用GPT（如果可用）
    if not use_gpt and OPENAI_AVAILABLE and OPENAI_API_KEY:
        use_gpt = True
        logger.info("检测到API配置，自动启用GPT增强模式")
    
    if use_gpt and OPENAI_AVAILABLE and OPENAI_API_KEY:
        logger.info("使用DeepSeek API生成高质量训练数据")
        training_data = generator.generate_all_training_data()
    else:
        logger.info("使用简化版本生成训练数据（不调用API）")
        training_data = generator.generate_simple_training_data()
    
    generator.save_training_data(training_data)
    
    logger.info("训练数据生成完成！")


if __name__ == "__main__":
    main()

