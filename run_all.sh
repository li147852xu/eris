#!/bin/bash
# ========================================
# 金融助手训练数据生成 - 一键运行脚本
# 适用于云GPU平台（AutoDL/Colab等）
# ========================================

set -e  # 遇到错误立即退出

echo "========================================="
echo "   金融助手AI训练系统 - 完整流程"
echo "========================================="
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 步骤计数
STEP=1

# ========================================
# 步骤1: 环境检查
# ========================================
echo -e "${BLUE}[步骤 $STEP] 检查环境...${NC}"
STEP=$((STEP+1))

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到python3${NC}"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"
echo ""

# ========================================
# 步骤2: 安装依赖
# ========================================
echo -e "${BLUE}[步骤 $STEP] 安装依赖包...${NC}"
STEP=$((STEP+1))

pip install -q -r requirements.txt
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# ========================================
# 步骤3: 清洗数据（可选）
# ========================================
echo -e "${BLUE}[步骤 $STEP] 清洗数据...${NC}"
STEP=$((STEP+1))

if [ -f "cleaner.py" ]; then
    python3 cleaner.py
    echo -e "${GREEN}✓ 数据清洗完成${NC}"
else
    echo -e "${YELLOW}⚠ 跳过数据清洗（未找到cleaner.py）${NC}"
fi
echo ""

# ========================================
# 步骤4: 解析语料
# ========================================
echo -e "${BLUE}[步骤 $STEP] 解析语料文件...${NC}"
STEP=$((STEP+1))

python3 scripts/parse_corpus.py
echo -e "${GREEN}✓ 语料解析完成${NC}"
echo ""

# ========================================
# 步骤5: 生成训练数据（使用DeepSeek API）
# ========================================
echo -e "${BLUE}[步骤 $STEP] 生成训练数据（使用DeepSeek API）...${NC}"
STEP=$((STEP+1))

# 检查API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠ 警告: 未设置OPENAI_API_KEY环境变量${NC}"
    echo "将使用简化方法生成训练数据"
    python3 scripts/generate_training_data.py
else
    echo "✓ 检测到API配置，使用DeepSeek增强模式"
    python3 scripts/generate_training_data.py
fi

echo -e "${GREEN}✓ 训练数据生成完成${NC}"
echo ""

# ========================================
# 步骤6: 显示统计信息
# ========================================
echo -e "${BLUE}[步骤 $STEP] 生成完成！统计信息：${NC}"
STEP=$((STEP+1))

python3 scripts/check_progress.py

echo ""
echo "========================================="
echo -e "${GREEN}   ✅ 所有步骤完成！${NC}"
echo "========================================="
echo ""
echo "📁 生成的文件："
echo "   - outputs/processed_data/parsed_corpus.json"
echo "   - outputs/training_data/training_dataset.json"
echo "   - outputs/training_data/training_dataset.jsonl"
echo ""
echo "🚀 下一步："
echo "   运行模型微调："
echo "   python3 scripts/train_model.py"
echo ""
echo "📊 查看进度："
echo "   python3 scripts/check_progress.py"
echo ""

