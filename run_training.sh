#!/bin/bash
# ========================================
# 云GPU平台 - 模型训练一键脚本
# ========================================

set -e

echo "========================================="
echo "   金融助手模型训练 - GPU加速"
echo "========================================="
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ========================================
# 检查GPU
# ========================================
echo -e "${BLUE}检查GPU环境...${NC}"

if python3 -c "import torch; print('CUDA可用' if torch.cuda.is_available() else 'CUDA不可用')" 2>/dev/null | grep -q "CUDA可用"; then
    echo -e "${GREEN}✓ 检测到CUDA GPU${NC}"
    python3 -c "import torch; print(f'GPU型号: {torch.cuda.get_device_name(0)}'); print(f'显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')"
else
    echo -e "${RED}⚠ 未检测到CUDA GPU，训练速度会很慢${NC}"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# ========================================
# 安装训练依赖
# ========================================
echo -e "${BLUE}安装训练依赖...${NC}"

pip install -q transformers torch datasets peft accelerate bitsandbytes sentencepiece

echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# ========================================
# 检查训练数据
# ========================================
echo -e "${BLUE}检查训练数据...${NC}"

if [ ! -f "outputs/training_data/training_dataset.jsonl" ]; then
    echo -e "${RED}错误: 未找到训练数据文件${NC}"
    echo "请先运行: ./run_all.sh 生成训练数据"
    exit 1
fi

SAMPLE_COUNT=$(wc -l < outputs/training_data/training_dataset.jsonl)
echo -e "${GREEN}✓ 找到训练数据: ${SAMPLE_COUNT} 个样本${NC}"

if [ "$SAMPLE_COUNT" -lt 50 ]; then
    echo -e "${RED}⚠ 警告: 样本数量较少（${SAMPLE_COUNT}个），建议至少180个${NC}"
    read -p "是否继续训练？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# ========================================
# 开始训练
# ========================================
echo -e "${BLUE}开始训练模型...${NC}"
echo ""

python3 scripts/train_model.py

echo ""
echo "========================================="
echo -e "${GREEN}   ✅ 训练完成！${NC}"
echo "========================================="
echo ""
echo "📁 模型保存在: models/financial_assistant/"
echo ""
echo "🧪 测试模型："
echo "   python3 scripts/test_model.py"
echo ""

