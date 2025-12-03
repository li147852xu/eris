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
echo ""

# 先检查是否已安装
if python3 -c "import transformers, peft, torch" 2>/dev/null; then
    echo -e "${GREEN}✓ 训练依赖已安装${NC}"
else
    echo "开始安装训练依赖（显示详细输出）..."
    echo ""
    
    # 升级pip
    echo "[1/7] 升级pip..."
    pip install --upgrade pip setuptools wheel
    
    # 安装PyTorch
    echo ""
    echo "[2/7] 安装PyTorch..."
    if command -v nvidia-smi &> /dev/null; then
        echo "检测到NVIDIA GPU，安装CUDA 12.1版本..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    else
        echo "安装CPU版本..."
        pip install torch torchvision torchaudio
    fi
    
    # 验证PyTorch
    python3 -c "import torch; print(f'✓ PyTorch {torch.__version__} 已安装')"
    
    # 安装transformers
    echo ""
    echo "[3/7] 安装transformers..."
    pip install transformers
    python3 -c "import transformers; print(f'✓ transformers {transformers.__version__} 已安装')"
    
    # 安装datasets
    echo ""
    echo "[4/7] 安装datasets..."
    pip install datasets
    python3 -c "import datasets; print(f'✓ datasets {datasets.__version__} 已安装')"
    
    # 安装peft
    echo ""
    echo "[5/7] 安装peft..."
    pip install peft
    python3 -c "import peft; print(f'✓ peft {peft.__version__} 已安装')"
    
    # 安装accelerate
    echo ""
    echo "[6/7] 安装accelerate..."
    pip install accelerate
    python3 -c "import accelerate; print(f'✓ accelerate {accelerate.__version__} 已安装')"
    
    # 安装其他
    echo ""
    echo "[7/7] 安装其他依赖..."
    pip install sentencepiece protobuf scipy
    
    echo ""
    echo -e "${GREEN}✓ 所有依赖安装完成${NC}"
fi

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

