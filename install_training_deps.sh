#!/bin/bash
# ========================================
# 安装训练依赖 - 独立脚本
# ========================================

set -e

echo "========================================="
echo "   安装模型训练依赖"
echo "========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ========================================
# 1. 升级pip
# ========================================
echo -e "${BLUE}[1/6] 升级pip...${NC}"
pip install --upgrade pip setuptools wheel -q
echo -e "${GREEN}✓ pip已升级${NC}"
echo ""

# ========================================
# 2. 安装PyTorch
# ========================================
echo -e "${BLUE}[2/6] 安装PyTorch...${NC}"

if command -v nvidia-smi &> /dev/null; then
    # 检测GPU型号
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n 1)
    echo "检测到GPU: $GPU_NAME"
    
    # RTX 5090需要PyTorch 2.5+ nightly版本
    if [[ "$GPU_NAME" == *"5090"* ]] || [[ "$GPU_NAME" == *"50 "* ]]; then
        echo "检测到RTX 5090，需要安装最新PyTorch nightly版本..."
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
    else
        echo "安装PyTorch CUDA 12.1稳定版..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    fi
else
    echo "未检测到GPU，安装CPU版本..."
    pip install torch torchvision torchaudio
fi

echo -e "${GREEN}✓ PyTorch安装完成${NC}"
python3 -c "import torch; print(f'  PyTorch版本: {torch.__version__}'); print(f'  CUDA可用: {torch.cuda.is_available()}')" 2>/dev/null || echo "  验证中..."
echo ""

# ========================================
# 3. 安装transformers
# ========================================
echo -e "${BLUE}[3/6] 安装transformers...${NC}"
pip install transformers
echo -e "${GREEN}✓ transformers安装完成${NC}"
python3 -c "import transformers; print(f'  版本: {transformers.__version__}')"
echo ""

# ========================================
# 4. 安装datasets
# ========================================
echo -e "${BLUE}[4/6] 安装datasets...${NC}"
pip install datasets
echo -e "${GREEN}✓ datasets安装完成${NC}"
python3 -c "import datasets; print(f'  版本: {datasets.__version__}')"
echo ""

# ========================================
# 5. 安装PEFT（LoRA）
# ========================================
echo -e "${BLUE}[5/6] 安装peft...${NC}"
pip install peft
echo -e "${GREEN}✓ peft安装完成${NC}"
python3 -c "import peft; print(f'  版本: {peft.__version__}')"
echo ""

# ========================================
# 6. 安装其他依赖
# ========================================
echo -e "${BLUE}[6/6] 安装其他依赖...${NC}"
pip install accelerate sentencepiece protobuf scipy

# bitsandbytes需要CUDA，可选
if command -v nvidia-smi &> /dev/null; then
    pip install bitsandbytes || echo -e "${RED}  ⚠ bitsandbytes安装失败（可选包，不影响训练）${NC}"
fi

echo -e "${GREEN}✓ 其他依赖安装完成${NC}"
echo ""

# ========================================
# 验证安装
# ========================================
echo "========================================="
echo "   验证安装"
echo "========================================="

python3 << 'PYTHON_EOF'
import sys

packages = {
    'torch': 'PyTorch',
    'transformers': 'Transformers',
    'datasets': 'Datasets',
    'peft': 'PEFT (LoRA)',
    'accelerate': 'Accelerate',
    'sentencepiece': 'SentencePiece',
}

print("\n检查已安装的包：\n")

all_ok = True
for pkg, name in packages.items():
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {name:20s} {version}")
    except ImportError:
        print(f"✗ {name:20s} 未安装")
        all_ok = False

print()

if all_ok:
    print("✅ 所有必需包已安装！")
    sys.exit(0)
else:
    print("❌ 有包未安装，请检查错误信息")
    sys.exit(1)
PYTHON_EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo -e "${GREEN}   ✅ 训练环境准备完成！${NC}"
    echo "========================================="
    echo ""
    echo "现在可以运行："
    echo "  python3 scripts/train_model.py"
    echo "或："
    echo "  ./run_training.sh"
else
    echo ""
    echo "========================================="
    echo -e "${RED}   ❌ 安装未完成${NC}"
    echo "========================================="
    exit 1
fi

