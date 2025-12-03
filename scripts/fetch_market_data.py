"""市场数据爬取脚本"""
import akshare as ak
import efinance as ef
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))
from config import RAW_DATA_DIR, LOG_DIR, INDEX_CODES

# 配置日志
logger.add(LOG_DIR / "fetch_market_data.log", rotation="10 MB")


class MarketDataFetcher:
    """市场数据获取器"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        
    def fetch_index_data(self, date: str) -> Dict:
        """获取指数数据"""
        logger.info(f"获取 {date} 的指数数据")
        result = {}
        
        try:
            # 格式化日期
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            
            # 获取上证指数
            try:
                sh_df = ak.stock_zh_index_daily(symbol="sh000001")
                sh_data = sh_df[sh_df['date'] == date]
                if not sh_data.empty:
                    result['上证指数'] = {
                        'open': float(sh_data.iloc[0]['open']),
                        'close': float(sh_data.iloc[0]['close']),
                        'high': float(sh_data.iloc[0]['high']),
                        'low': float(sh_data.iloc[0]['low']),
                        'volume': float(sh_data.iloc[0]['volume']),
                        'change_pct': round((sh_data.iloc[0]['close'] - sh_data.iloc[0]['open']) / sh_data.iloc[0]['open'] * 100, 2)
                    }
                    logger.info(f"上证指数: {result['上证指数']['close']}")
            except Exception as e:
                logger.warning(f"获取上证指数失败: {e}")
            
            # 获取深证成指
            try:
                sz_df = ak.stock_zh_index_daily(symbol="sz399001")
                sz_data = sz_df[sz_df['date'] == date]
                if not sz_data.empty:
                    result['深证成指'] = {
                        'open': float(sz_data.iloc[0]['open']),
                        'close': float(sz_data.iloc[0]['close']),
                        'high': float(sz_data.iloc[0]['high']),
                        'low': float(sz_data.iloc[0]['low']),
                        'volume': float(sz_data.iloc[0]['volume']),
                        'change_pct': round((sz_data.iloc[0]['close'] - sz_data.iloc[0]['open']) / sz_data.iloc[0]['open'] * 100, 2)
                    }
                    logger.info(f"深证成指: {result['深证成指']['close']}")
            except Exception as e:
                logger.warning(f"获取深证成指失败: {e}")
            
            # 获取创业板指
            try:
                cy_df = ak.stock_zh_index_daily(symbol="sz399006")
                cy_data = cy_df[cy_df['date'] == date]
                if not cy_data.empty:
                    result['创业板指'] = {
                        'open': float(cy_data.iloc[0]['open']),
                        'close': float(cy_data.iloc[0]['close']),
                        'high': float(cy_data.iloc[0]['high']),
                        'low': float(cy_data.iloc[0]['low']),
                        'volume': float(cy_data.iloc[0]['volume']),
                        'change_pct': round((cy_data.iloc[0]['close'] - cy_data.iloc[0]['open']) / cy_data.iloc[0]['open'] * 100, 2)
                    }
                    logger.info(f"创业板指: {result['创业板指']['close']}")
            except Exception as e:
                logger.warning(f"获取创业板指失败: {e}")
            
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
        
        return result
    
    def fetch_market_overview(self, date: str) -> Dict:
        """获取市场概况"""
        logger.info(f"获取 {date} 的市场概况")
        result = {}
        
        try:
            # 获取涨跌统计
            date_formatted = date.replace('-', '')
            try:
                market_df = ak.stock_zh_a_spot_em()
                if not market_df.empty:
                    up_count = len(market_df[market_df['涨跌幅'] > 0])
                    down_count = len(market_df[market_df['涨跌幅'] < 0])
                    flat_count = len(market_df[market_df['涨跌幅'] == 0])
                    
                    result['market_stats'] = {
                        'up_count': int(up_count),
                        'down_count': int(down_count),
                        'flat_count': int(flat_count),
                        'total_count': int(len(market_df))
                    }
                    logger.info(f"市场统计: 上涨{up_count}, 下跌{down_count}")
            except Exception as e:
                logger.warning(f"获取涨跌统计失败: {e}")
            
            # 获取成交额（使用上证指数的成交量作为参考）
            try:
                sh_df = ak.stock_zh_index_daily(symbol="sh000001")
                sh_data = sh_df[sh_df['date'] == date]
                if not sh_data.empty:
                    result['turnover'] = {
                        'amount': float(sh_data.iloc[0]['volume']) / 100000000,  # 转换为亿元
                        'unit': '亿元'
                    }
            except Exception as e:
                logger.warning(f"获取成交额失败: {e}")
                
        except Exception as e:
            logger.error(f"获取市场概况失败: {e}")
        
        return result
    
    def fetch_sector_data(self, date: str, sectors: List[str]) -> Dict:
        """获取板块数据"""
        logger.info(f"获取 {date} 的板块数据")
        result = {}
        
        # 板块映射（映射到东方财富的板块名称）
        sector_mapping = {
            '半导体': '半导体',
            '芯片': '芯片',
            'AI': '人工智能',
            '人工智能': '人工智能',
            '军工': '国防军工',
            '新能源': '新能源',
            '光伏': '光伏',
            '医药': '医药',
            '消费': '消费',
            '券商': '券商',
            '煤炭': '煤炭',
        }
        
        try:
            # 获取板块行情
            for sector in sectors[:10]:  # 限制数量避免请求过多
                mapped_sector = sector_mapping.get(sector, sector)
                try:
                    time.sleep(0.5)  # 避免请求过快
                    # 注意：实际实现时需要根据具体数据源API调整
                    result[sector] = {
                        'name': sector,
                        'change_pct': 0.0,  # 占位
                        'note': '需要实际API数据'
                    }
                except Exception as e:
                    logger.warning(f"获取板块 {sector} 数据失败: {e}")
                    
        except Exception as e:
            logger.error(f"获取板块数据失败: {e}")
        
        return result
    
    def fetch_fund_flow(self, date: str) -> Dict:
        """获取资金流向"""
        logger.info(f"获取 {date} 的资金流向")
        result = {}
        
        try:
            # 获取北向资金
            try:
                north_df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")
                north_data = north_df[north_df['日期'] == date]
                if not north_data.empty:
                    result['北向资金'] = {
                        'net_inflow': float(north_data.iloc[0]['当日资金流入']),
                        'unit': '亿元'
                    }
                    logger.info(f"北向资金净流入: {result['北向资金']['net_inflow']}亿")
            except Exception as e:
                logger.warning(f"获取北向资金失败: {e}")
            
            # 获取主力资金
            try:
                # 使用市场整体主力资金数据
                result['主力资金'] = {
                    'net_inflow': 0.0,  # 占位，需要实际API
                    'unit': '亿元',
                    'note': '需要实际API数据'
                }
            except Exception as e:
                logger.warning(f"获取主力资金失败: {e}")
                
        except Exception as e:
            logger.error(f"获取资金流向失败: {e}")
        
        return result
    
    def fetch_date_data(self, date: str, sectors: List[str] = None) -> Dict:
        """获取指定日期的所有市场数据"""
        logger.info(f"开始获取 {date} 的市场数据")
        
        data = {
            'date': date,
            'indices': self.fetch_index_data(date),
            'market_overview': self.fetch_market_overview(date),
            'fund_flow': self.fetch_fund_flow(date),
            'timestamp': datetime.now().isoformat()
        }
        
        if sectors:
            data['sectors'] = self.fetch_sector_data(date, sectors)
        
        return data
    
    def save_market_data(self, date: str, data: Dict):
        """保存市场数据"""
        filename = f"market_data_{date}.json"
        filepath = self.raw_data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"市场数据已保存到: {filepath}")


def main():
    """主函数"""
    fetcher = MarketDataFetcher()
    
    # 示例：获取单日数据
    test_date = "2025-12-02"
    data = fetcher.fetch_date_data(test_date)
    fetcher.save_market_data(test_date, data)
    
    logger.info("数据获取完成")


if __name__ == "__main__":
    main()

