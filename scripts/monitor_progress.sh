#!/bin/bash
# 实时监控训练数据生成进度

echo "=== 训练数据生成监控 ==="
echo ""

while true; do
    clear
    echo "=== 训练数据生成监控 ==="
    echo "时间: $(date '+%H:%M:%S')"
    echo ""
    
    # 检查进程
    if pgrep -f "generate_training_data.py" > /dev/null; then
        echo "✅ 任务运行中"
    else
        echo "❌ 任务已停止"
    fi
    
    echo ""
    echo "--- 最新进度 ---"
    tail -10 /Users/tiantanghuaxiao/.cursor/projects/Users-tiantanghuaxiao-Documents-eris/terminals/6.txt 2>/dev/null | grep "处理\|生成\|完成"
    
    echo ""
    echo "--- 文件状态 ---"
    if [ -f "outputs/training_data/training_dataset.json" ]; then
        LINES=$(cat outputs/training_data/training_dataset.json | jq '. | length' 2>/dev/null || echo "解析中...")
        echo "主文件: $LINES 个样本"
    fi
    
    if [ -f "outputs/training_data/training_dataset_backup.json" ]; then
        BACKUP_LINES=$(cat outputs/training_data/training_dataset_backup.json | jq '. | length' 2>/dev/null || echo "解析中...")
        echo "备份文件: $BACKUP_LINES 个样本"
    fi
    
    echo ""
    echo "按 Ctrl+C 退出监控"
    sleep 5
done

