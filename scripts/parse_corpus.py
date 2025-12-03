"""语料解析脚本 - 提取关键信息"""
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger
from tqdm import tqdm
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR

# 配置日志
logger.add(LOG_DIR / "parse_corpus.log", rotation="10 MB")


class CorpusParser:
    """语料解析器"""
    
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        
    def parse_date_from_filename(self, filename: str) -> Optional[str]:
        """从文件名提取日期"""
        match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', filename)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"
        return None
    
    def split_sections(self, content: str) -> Dict[str, str]:
        """分割早自习、主1、主2"""
        sections = {
            "早自习": "",
            "主1": "",
            "主2": ""
        }
        
        # 按一级标题分割
        parts = re.split(r'\n# ', content)
        
        for part in parts:
            if not part.strip():
                continue
            part = '# ' + part if not part.startswith('#') else part
            
            # 判断是哪个部分
            if '早自习' in part[:50]:
                sections["早自习"] = part
            elif '（主1）' in part[:100] or '(主1)' in part[:100]:
                sections["主1"] = part
            elif '（主2）' in part[:100] or '(主2)' in part[:100]:
                sections["主2"] = part
                
        return sections
    
    def extract_key_info(self, content: str, date: str) -> Dict:
        """提取关键信息"""
        info = {
            "date": date,
            "indices": [],  # 指数点位
            "sectors": [],  # 板块
            "stocks": [],  # 个股
            "predictions": [],  # 预测
            "fund_flow": [],  # 资金流向
            "sentiments": [],  # 情绪判断
        }
        
        # 提取指数点位
        index_patterns = [
            r'(\d{4})点',
            r'上证.*?(\d{4})',
            r'沪指.*?(\d{4})',
            r'深成指.*?(\d{4})',
            r'创业板.*?(\d{4})',
        ]
        for pattern in index_patterns:
            matches = re.findall(pattern, content)
            info["indices"].extend(matches)
        
        # 提取板块（中文词汇+可能的修饰词）
        sector_keywords = [
            '半导体', '芯片', 'AI', '人工智能', '军工', '新能源', '光伏', 
            '储能', '锂电', '医药', '创新药', '消费', '零售', '券商',
            '稀土', '有色', '煤炭', '航天', '机器人', '传媒', '游戏',
            'CPO', 'PCB', '算力', '大模型', '存储', '光刻胶', '福建',
            '海南', '两岸', '航母', '海防', '固态电池', '电池', '白酒',
            '短剧', '影视', '跨境电商', '冰雪', '造纸', '有机硅',
        ]
        for keyword in sector_keywords:
            if keyword in content:
                info["sectors"].append(keyword)
        
        # 提取个股（公司简称模式）
        stock_patterns = [
            r'[东西南北中][\u4e00-\u9fa5]{1,3}(?=[\s、，。！])',  # 方位+字
            r'[\u4e00-\u9fa5]{2,4}(?=涨停|跌停|上涨|下跌)',
        ]
        for pattern in stock_patterns:
            matches = re.findall(pattern, content)
            info["stocks"].extend(matches)
        
        # 提取预测关键词
        prediction_keywords = ['看涨', '看跌', '震荡', '反弹', '分化', '承压', '企稳', '冲高回落']
        for keyword in prediction_keywords:
            if keyword in content:
                info["predictions"].append(keyword)
        
        # 提取资金流向
        fund_flow_pattern = r'(净流入|净流出).*?(\d+\.?\d*)亿'
        matches = re.findall(fund_flow_pattern, content)
        info["fund_flow"] = [f"{m[0]}{m[1]}亿" for m in matches]
        
        # 去重
        for key in ['indices', 'sectors', 'stocks', 'predictions']:
            info[key] = list(set(info[key]))
        
        return info
    
    def parse_file(self, file_path: Path) -> Optional[Dict]:
        """解析单个文件"""
        try:
            logger.info(f"解析文件: {file_path.name}")
            
            # 提取日期
            date = self.parse_date_from_filename(file_path.name)
            if not date:
                logger.warning(f"无法从文件名提取日期: {file_path.name}")
                return None
            
            # 读取内容
            content = file_path.read_text(encoding='utf-8')
            
            # 分割章节
            sections = self.split_sections(content)
            
            # 提取关键信息
            result = {
                "filename": file_path.name,
                "date": date,
                "sections": sections,
                "key_info": {
                    section_name: self.extract_key_info(section_content, date)
                    for section_name, section_content in sections.items()
                    if section_content
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"解析文件失败 {file_path.name}: {e}")
            return None
    
    def parse_all(self) -> List[Dict]:
        """解析所有语料文件"""
        results = []
        
        # 获取所有.md文件（排除ReadMe.md）
        md_files = sorted([
            f for f in self.data_dir.glob("*.md")
            if f.name != "ReadMe.md"
        ])
        
        logger.info(f"找到 {len(md_files)} 个语料文件")
        
        # 添加进度条
        for file_path in tqdm(md_files, desc="📖 解析语料文件", 
                             unit="文件", colour="cyan"):
            result = self.parse_file(file_path)
            if result:
                results.append(result)
        
        return results
    
    def save_parsed_data(self, data: List[Dict], output_file: str = "parsed_corpus.json"):
        """保存解析结果"""
        output_path = PROCESSED_DATA_DIR / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"解析结果已保存到: {output_path}")


def main():
    """主函数"""
    parser = CorpusParser()
    results = parser.parse_all()
    parser.save_parsed_data(results)
    
    logger.info(f"成功解析 {len(results)} 个文件")
    
    # 打印统计信息
    total_sections = sum(len([s for s in r['sections'].values() if s]) for r in results)
    logger.info(f"总共章节数: {total_sections}")


if __name__ == "__main__":
    main()

