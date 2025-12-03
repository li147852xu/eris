"""增强版市场数据爬取 - 整合多个数据源"""
import akshare as ak
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from loguru import logger
from tqdm import tqdm
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR

# 配置日志
logger.add(LOG_DIR / "fetch_market.log", rotation="10 MB")


class EnhancedMarketDataFetcher:
    """增强版市场数据获取器"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        
    def fetch_all_data_for_dates(self, dates: List[str]):
        """批量获取多个日期的数据"""
        logger.info(f"开始批量获取 {len(dates)} 个日期的市场数据")
        
        results = {}
        
        with tqdm(dates, desc="📈 爬取市场数据", unit="天", colour="cyan") as pbar:
            for date in pbar:
                pbar.set_description(f"📈 爬取 {date}")
                try:
                    data = self.fetch_date_data(date)
                    results[date] = data
                    self.save_market_data(date, data)
                    pbar.set_postfix({"成功": len(results)})
                    time.sleep(1)  # 避免请求过快
                except Exception as e:
                    logger.error(f"获取 {date} 失败: {e}")
                    pbar.set_postfix({"成功": len(results), "失败": len(dates)-len(results)})
        
        logger.info(f"✅ 成功获取 {len(results)}/{len(dates)} 个日期的数据")
        return results
    
    def fetch_date_data(self, date: str) -> Dict:
        """获取单日所有市场数据"""
        data = {
            'date': date,
            'indices': self.fetch_indices(date),
            'market_stats': self.fetch_market_stats(date),
            'fund_flow': self.fetch_fund_flow(date),
            'top_sectors': self.fetch_top_sectors(date),
            'timestamp': datetime.now().isoformat()
        }
        return data
    
    def fetch_indices(self, date: str) -> Dict:
        """获取三大指数数据"""
        indices = {}
        
        try:
            # 上证指数
            df = ak.stock_zh_index_daily(symbol="sh000001")
            row = df[df['date'] == date]
            if not row.empty:
                indices['上证指数'] = {
                    'code': '000001',
                    'open': float(row.iloc[0]['open']),
                    'close': float(row.iloc[0]['close']),
                    'high': float(row.iloc[0]['high']),
                    'low': float(row.iloc[0]['low']),
                    'volume': float(row.iloc[0]['volume']),
                    'change': round(row.iloc[0]['close'] - row.iloc[0]['open'], 2),
                    'change_pct': round((row.iloc[0]['close'] - row.iloc[0]['open']) / row.iloc[0]['open'] * 100, 2)
                }
        except Exception as e:
            logger.debug(f"获取上证指数失败: {e}")
        
        try:
            # 深证成指
            df = ak.stock_zh_index_daily(symbol="sz399001")
            row = df[df['date'] == date]
            if not row.empty:
                indices['深证成指'] = {
                    'code': '399001',
                    'open': float(row.iloc[0]['open']),
                    'close': float(row.iloc[0]['close']),
                    'high': float(row.iloc[0]['high']),
                    'low': float(row.iloc[0]['low']),
                    'volume': float(row.iloc[0]['volume']),
                    'change': round(row.iloc[0]['close'] - row.iloc[0]['open'], 2),
                    'change_pct': round((row.iloc[0]['close'] - row.iloc[0]['open']) / row.iloc[0]['open'] * 100, 2)
                }
        except Exception as e:
            logger.debug(f"获取深证成指失败: {e}")
        
        try:
            # 创业板指
            df = ak.stock_zh_index_daily(symbol="sz399006")
            row = df[df['date'] == date]
            if not row.empty:
                indices['创业板指'] = {
                    'code': '399006',
                    'open': float(row.iloc[0]['open']),
                    'close': float(row.iloc[0]['close']),
                    'high': float(row.iloc[0]['high']),
                    'low': float(row.iloc[0]['low']),
                    'volume': float(row.iloc[0]['volume']),
                    'change': round(row.iloc[0]['close'] - row.iloc[0]['open'], 2),
                    'change_pct': round((row.iloc[0]['close'] - row.iloc[0]['open']) / row.iloc[0]['open'] * 100, 2)
                }
        except Exception as e:
            logger.debug(f"获取创业板指失败: {e}")
        
        return indices
    
    def fetch_market_stats(self, date: str) -> Dict:
        """获取市场涨跌统计"""
        stats = {}
        
        try:
            # 获取A股实时数据（注意：只能获取当日或最近的数据）
            # 对于历史数据，这个方法可能不准确
            df = ak.stock_zh_a_spot_em()
            if not df.empty:
                stats = {
                    'up_count': int(len(df[df['涨跌幅'] > 0])),
                    'down_count': int(len(df[df['涨跌幅'] < 0])),
                    'limit_up': int(len(df[df['涨跌幅'] >= 9.9])),
                    'limit_down': int(len(df[df['涨跌幅'] <= -9.9])),
                    'total': int(len(df)),
                    'note': '当日数据或最近交易日数据'
                }
        except Exception as e:
            logger.debug(f"获取市场统计失败: {e}")
        
        return stats
    
    def fetch_fund_flow(self, date: str) -> Dict:
        """获取资金流向"""
        fund_flow = {}
        
        try:
            # 北向资金
            df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上资金")
            row = df[df['日期'] == date]
            if not row.empty:
                fund_flow['北向资金'] = {
                    'net_inflow': float(row.iloc[0]['当日资金流入']),
                    'unit': '亿元'
                }
        except Exception as e:
            logger.debug(f"获取北向资金失败: {e}")
        
        return fund_flow
    
    def fetch_top_sectors(self, date: str) -> List[Dict]:
        """获取涨跌幅前10的板块"""
        sectors = []
        
        try:
            # 获取板块行情
            df = ak.stock_board_industry_name_em()
            if not df.empty and len(df) > 0:
                # 按涨跌幅排序，取前10
                df_sorted = df.sort_values('涨跌幅', ascending=False).head(10)
                for _, row in df_sorted.iterrows():
                    sectors.append({
                        'name': str(row['板块名称']),
                        'change_pct': float(row['涨跌幅']),
                        'lead_stock': str(row.get('领涨股票', 'N/A'))
                    })
        except Exception as e:
            logger.debug(f"获取板块数据失败: {e}")
        
        return sectors
    
    def save_market_data(self, date: str, data: Dict):
        """保存市场数据"""
        filepath = self.raw_data_dir / f"market_data_{date}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    # 从parsed_corpus.json读取所有日期
    corpus_file = PROCESSED_DATA_DIR / "parsed_corpus.json"
    
    if not corpus_file.exists():
        logger.error("请先运行 parse_corpus.py 解析语料")
        return
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        corpus_data = json.load(f)
    
    dates = [item['date'] for item in corpus_data]
    logger.info(f"准备爬取 {len(dates)} 个日期的数据")
    
    fetcher = EnhancedMarketDataFetcher()
    fetcher.fetch_all_data_for_dates(dates)


if __name__ == "__main__":
    main()

