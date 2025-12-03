#!/bin/bash
# ========================================
# RTX 5090 PyTorch修复脚本
# ========================================

set -e

echo "========================================="
echo "   RTX 5090 PyTorch兼容性修复"
echo "========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}问题: RTX 5090 (sm_120) 不兼容当前PyTorch${NC}"
echo "需要安装支持sm_120的PyTorch版本"
echo ""

# 卸载旧版本
echo -e "${BLUE}[1/3] 卸载旧版PyTorch...${NC}"
pip uninstall torch torchvision torchaudio -y 2>/dev/null || echo "未找到旧版本"
echo ""

# 安装最新nightly版本（支持RTX 5090）
echo -e "${BLUE}[2/3] 安装PyTorch Nightly (CUDA 12.4)...${NC}"
echo "这个版本支持RTX 5090的sm_120架构"
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

echo ""

# 验证
echo -e "${BLUE}[3/3] 验证安装...${NC}"
python3 << 'EOF'
import torch

print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU数量: {torch.cuda.device_count()}")
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
    print(f"GPU计算能力: sm_{torch.cuda.get_device_capability()[0]}{torch.cuda.get_device_capability()[1]}")
    
    # 测试是否可以分配内存
    try:
        x = torch.randn(1000, 1000).cuda()
        print("✅ GPU内存分配测试: 成功")
    except Exception as e:
        print(f"❌ GPU测试失败: {e}")
else:
    print("❌ CUDA不可用")
EOF

echo ""
echo "========================================="
echo -e "${GREEN}   ✅ 修复完成！${NC}"
echo "========================================="
echo ""
echo "现在可以运行训练："
echo "  python3 scripts/train_model.py"
echo ""

