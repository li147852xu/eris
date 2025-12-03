"""检查训练数据生成进度"""
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import TRAINING_DATA_DIR, LOG_DIR

def check_progress():
    # 检查训练数据文件
    dataset_file = TRAINING_DATA_DIR / "training_dataset.json"
    
    if dataset_file.exists():
        with open(dataset_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 已生成样本数: {len(data)}")
        
        # 统计每天的样本
        date_count = {}
        for item in data:
            date = item.get('date', 'unknown')
            date_count[date] = date_count.get(date, 0) + 1
        
        print(f"\n📊 各日期样本数:")
        for date in sorted(date_count.keys()):
            print(f"  {date}: {date_count[date]}个")
        
        print(f"\n📈 总计: {len(data)}个样本")
    else:
        print("⏳ 训练数据文件尚未生成...")
    
    # 检查日志
    log_file = LOG_DIR / "generate_training.log"
    if log_file.exists():
        print(f"\n📝 最新日志 (最后10行):")
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(f"  {line.rstrip()}")

if __name__ == "__main__":
    check_progress()

