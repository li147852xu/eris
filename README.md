# 🤖 金融助手AI训练系统

基于你的独特分析风格，训练一个专业的A股市场分析助手。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**项目地址**: https://github.com/li147852xu/eris.git

---

## 🚀 快速开始（5分钟上手）

### 在AutoDL云GPU平台运行

```bash
# 1. 克隆项目
git clone https://github.com/li147852xu/eris.git
cd eris

# 2. 配置API
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 3. 生成训练数据（20分钟）
./run_all.sh

# 4. 安装训练依赖（5分钟）
./install_training_deps.sh

# 5. 训练模型（30-60分钟）
python3 scripts/train_model.py
```

**总耗时**: 约1小时  
**总成本**: ¥2-3元

---

## 📊 项目数据

- ✅ **29天语料**（2025-10-23 至 2025-12-02）
- ✅ **预计生成**: 400-500个训练样本
- ✅ **基座模型**: Qwen2.5-7B-Instruct
- ✅ **微调方法**: LoRA（参数高效）

---

## 🎯 项目目标

训练一个能够：
- 📊 分析当日市场走势
- 🔮 预测未来市场方向  
- 💡 提供板块和个股操作建议
- 🎨 保持你的独特表达风格（"草原"=股市、"羊"=股票、"吃桃"=亏损）

---

## 📁 项目结构

```
eris/
├── README.md                # 完整文档（本文件）
├── config.py                # 配置文件
├── requirements.txt         # 基础依赖
├── requirements_training.txt # 训练依赖
├── cleaner.py              # 数据清洗工具
├── run_all.sh              # 一键生成训练数据
├── run_training.sh         # 一键训练模型
├── install_training_deps.sh # 独立安装脚本
│
├── data/                    # 原始语料（29个文件）
├── outputs/                 # 生成的数据
│   ├── processed_data/     # 语料解析结果
│   └── training_data/      # 训练数据集
├── models/                 # 训练后的模型
├── logs/                   # 日志文件
└── scripts/                # 核心脚本
    ├── parse_corpus.py              # 语料解析
    ├── generate_training_data.py    # 训练数据生成
    ├── train_model.py               # 模型微调
    ├── check_progress.py            # 进度检查
    └── test_model.py                # 模型测试
```

---

## ⚡ AutoDL完整流程

### 1. 创建实例

访问: https://www.autodl.com/

**推荐配置**:
- GPU: **RTX 4090** (24GB)
- 镜像: PyTorch 2.1.0 - Python 3.10
- 硬盘: 50GB
- 费用: ¥1.5/小时

### 2. 克隆项目

```bash
cd /root/autodl-tmp
git clone https://github.com/li147852xu/eris.git
cd eris
```

### 3. 配置环境

```bash
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
```

### 4. 生成训练数据

```bash
./run_all.sh
```

**流程**:
- ✅ 安装依赖（pandas, openai等）
- ✅ 清洗数据（cleaner.py）
- ✅ 解析语料（29天 → 87章节）
- ✅ DeepSeek生成（87章节 → 400-500个样本）
- ⏱️ 耗时：约20分钟

### 5. 安装训练依赖

```bash
./install_training_deps.sh
```

**安装包**:
- torch (PyTorch)
- transformers
- datasets
- peft (LoRA)
- accelerate
- 其他工具包

**验证**:
```bash
python3 -c "import torch, transformers, peft; print('✅ 核心包已安装')"
```

⏱️ 耗时：3-5分钟

### 6. 训练模型

```bash
python3 scripts/train_model.py
```

**配置**:
- 基座: Qwen2.5-7B-Instruct
- LoRA rank: 64
- Epochs: 3
- Batch size: 4

⏱️ 耗时：30-60分钟（RTX 4090）

### 7. 测试模型

```bash
python3 scripts/test_model.py
```

### 8. 下载模型

```bash
cd models
tar -czf financial_assistant.tar.gz financial_assistant/
# 使用AutoDL文件管理器下载
```

---

## ⏱️ 时间和成本

| 阶段 | 时间 | GPU成本 | API成本 |
|------|------|---------|---------|
| 数据生成 | 20分钟 | ¥0.5 | ¥0.5 |
| 安装依赖 | 5分钟 | ¥0.125 | - |
| 模型训练 | 40分钟 | ¥1.0 | - |
| **总计** | **65分钟** | **¥1.625** | **¥0.5** |

**总成本**: ≈ ¥2.1元

---

## 🐛 已修复的Bug

### Bug #1: pandas编译错误 ✅
**问题**: pandas 2.1.0 与 Python 3.12 不兼容  
**修复**: 使用 `pandas>=2.0.0`

### Bug #2: DeepSeek JSON解析失败 ✅
**问题**: API返回JSON被代码块包裹  
**修复**: 正则提取代码块内容

### Bug #3: transformers/peft未安装 ✅
**问题**: `-q`静默安装掩盖错误  
**修复**: 创建 `install_training_deps.sh`，显示详细输出

### Bug #4: 中断数据丢失 ✅
**问题**: 生成过程中断导致数据丢失  
**修复**: 每5天自动保存 + Ctrl+C保护

### Bug #5: Python语法错误 ✅
**问题**: f-string中文引号冲突  
**修复**: 改用单引号

### Bug #6: RTX 5090 GPU不兼容 ✅
**问题**: RTX 5090 (sm_120) 不兼容PyTorch 2.1  
**症状**: `CUDA error: no kernel image is available for execution on the device`  
**修复**: 自动检测RTX 5090并安装PyTorch nightly版本

#### RTX 5090用户专用修复

如果遇到GPU不兼容错误，运行：

```bash
./fix_rtx5090.sh
```

或手动修复：

```bash
# 卸载旧版本
pip uninstall torch torchvision torchaudio -y

# 安装nightly版本（支持RTX 5090）
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

# 验证
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"

# 测试GPU
python3 -c "import torch; x = torch.randn(100,100).cuda(); print('✅ GPU可用')"
```

---

## 🔧 配置说明

### 环境变量

```bash
# DeepSeek API（必需）
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
```

### 模型配置 (config.py)

```python
# 训练数据生成
TRAINING_CONFIG = {
    "model": "deepseek-chat",
    "temperature": 0.3,
    "max_tokens": 4000,
}

# 模型微调
FINETUNE_CONFIG = {
    "base_model": "Qwen/Qwen2.5-7B-Instruct",
    "lora_r": 64,
    "learning_rate": 2e-4,
    "num_epochs": 3,
    "batch_size": 4,
}
```

---

## 📝 添加新语料

### 文件命名

必须严格按照格式：`YYYY-MM-DD.md`

### 文件结构

```markdown
# XX月XX日早自习，...
（盘前分析）

# （主1）今日复盘...
（当日复盘）

# （主2）明日展望...
（明日预测）
```

### 更新流程

```bash
# 1. 添加新文件到data/
# 2. 推送到GitHub
git add data/
git commit -m "添加新语料"
git push

# 3. 云端更新
cd ~/eris
git pull
./run_all.sh
python3 scripts/train_model.py
```

---

## 🛠️ 实用工具

### 1. 数据清洗

```bash
python3 cleaner.py
```

自动清洗data/目录：
- 删除公众号格式
- 去除图片链接
- 删除emoji

### 2. 进度检查

```bash
python3 scripts/check_progress.py
```

显示：
- 已生成样本数
- 各日期分布
- 最新日志

### 3. GPU监控

```bash
watch -n 1 nvidia-smi
```

---

## 💡 依赖安装问题排查

### 问题：transformers和peft未安装

**原因**: `run_training.sh`静默安装掩盖错误

**解决方案**:

#### 方法1: 使用独立脚本（推荐）

```bash
cd ~/eris
git pull
./install_training_deps.sh
```

#### 方法2: 手动安装

```bash
# 升级pip
pip install --upgrade pip setuptools wheel

# 安装PyTorch（CUDA 12.1）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 验证PyTorch
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

# 安装transformers
pip install transformers

# 安装datasets
pip install datasets

# 安装peft
pip install peft

# 安装accelerate
pip install accelerate

# 安装其他
pip install sentencepiece protobuf scipy

# 验证所有包
python3 -c "import torch, transformers, peft, datasets, accelerate; print('✅ 所有包已安装')"
```

#### 检查已安装

```bash
pip list | grep -E "torch|transformers|peft|datasets|accelerate"
```

---

## 📈 训练效果预期

### 29天数据（当前）

- 样本数: 400-500个
- 效果: ⭐⭐⭐ 基础可用
- 建议: 继续积累到60-180天

### 60天数据

- 样本数: 800-1000个
- 效果: ⭐⭐⭐⭐ 实用水平

### 180天数据

- 样本数: 2500-3000个
- 效果: ⭐⭐⭐⭐⭐ 专家级别

---

## 🎓 技术栈

- **数据处理**: pandas, json, regex
- **数据获取**: akshare（免费A股数据）
- **AI增强**: DeepSeek API（中文优化）
- **模型训练**: transformers, peft (LoRA), torch
- **基座模型**: Qwen2.5-7B-Instruct

---

## 💬 常见问题

**Q: 29天数据够吗？**  
A: 可以开始测试，但建议继续积累到60-180天。

**Q: 必须用云GPU吗？**  
A: 强烈建议。Mac本地需要1-7天，云GPU只需30-60分钟。

**Q: 数据格式有差异怎么办？**  
A: 已内置智能解析，运行 `cleaner.py` 可规范化。

**Q: transformers找不到怎么办？**  
A: 运行 `./install_training_deps.sh`，显示详细安装过程。

**Q: 训练中断怎么办？**  
A: 会自动保存checkpoint，直接继续运行 `train_model.py`。

**Q: 如何评估模型效果？**  
A: 运行 `python3 scripts/test_model.py` 测试推理。

---

## 🔍 故障排查

### 查看日志

```bash
cat logs/generate_training.log | tail -50
cat logs/train_model.log | tail -50
```

### 验证安装

```bash
python3 << 'EOF'
packages = ['torch', 'transformers', 'peft', 'datasets', 'accelerate']
for pkg in packages:
    try:
        module = __import__(pkg)
        print(f"✓ {pkg}: {module.__version__}")
    except ImportError:
        print(f"✗ {pkg}: 未安装")
EOF
```

### 清空重来

```bash
cd ~/eris
rm -rf outputs logs
mkdir -p outputs/{raw_data,processed_data,training_data} logs
./run_all.sh
```

---

## ⏱️ 详细时间预估

### 数据生成阶段

| 步骤 | 耗时 |
|------|------|
| 环境检查 | 10秒 |
| 安装依赖 | 2-3分钟 |
| 清洗数据 | 10秒 |
| 解析语料 | 5秒 |
| DeepSeek生成 | 15-20分钟 |
| **总计** | **~20分钟** |

### 模型训练阶段

| GPU | 训练时间 | 显存占用 | 小时费用 |
|-----|---------|---------|---------|
| RTX 4090 | 30-50分钟 | 18GB | ¥1.5 |
| A100 40GB | 15-30分钟 | 20GB | ¥3.0 |
| A100 80GB | 10-20分钟 | 35GB | ¥4.0 |
| V100 32GB | 1-1.5小时 | 20GB | ¥1.2 |
| T4 16GB | 2-3小时 | 14GB | ¥0.8 |

**推荐**: RTX 4090（性价比最高）

---

## 📦 训练数据格式

```json
{
  "instruction": "今天大盘走势怎么看？",
  "input": "日期：2025-11-14。今晨美股大跌。指数约3950点。",
  "output": "今天大盘受美股大跌影响，大概率会低开，尤其是科技线相关板块。关键看低开后的承接情况，如果承接好，可以低吸做T。记住，我们的草原（股市）有自己的节奏...",
  "section_type": "早自习",
  "date": "2025-11-14"
}
```

---

## 🔄 持续更新

### 添加新语料

1. 在 `data/` 添加 `YYYY-MM-DD.md` 文件
2. 包含：早自习、主1、主2
3. 推送到GitHub

### 重新训练

```bash
# 本地
git add data/
git commit -m "添加新语料"
git push

# 云端
cd ~/eris
git pull
./run_all.sh
python3 scripts/train_model.py
```

---

## 🎯 快速命令参考

### AutoDL上的完整命令（复制即用）

```bash
# 一键完成全部流程
cd /root/autodl-tmp && \
git clone https://github.com/li147852xu/eris.git && \
cd eris && \
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c" && \
export OPENAI_BASE_URL="https://api.deepseek.com/v1" && \
./run_all.sh && \
./install_training_deps.sh && \
python3 scripts/train_model.py
```

### 常用命令

```bash
# 查看进度
python3 scripts/check_progress.py

# 监控GPU
watch -n 1 nvidia-smi

# 查看日志
tail -f logs/train_model.log

# 测试模型
python3 scripts/test_model.py
```

---

## 🎓 工作原理

### 训练数据生成

```
原始语料 (data/*.md)
    ↓ [解析]
结构化数据 (parsed_corpus.json)  
    ↓ [DeepSeek增强]
训练样本 (training_dataset.jsonl)
    ↓ [LoRA微调]
金融助手模型
```

### 智能市场信息提取

从语料自动提取：
- 指数点位（"3950点"）
- 涨跌趋势（"上涨"、"震荡"）
- 成交量（"1.8万亿"）
- 资金流向（"净流入"）

**优势**: 不依赖外部API，更稳定

---

## 📊 成本对比

| 方案 | 时间 | 成本 |
|------|------|------|
| Mac本地 | 1-7天 | 电费 + 时间 > ¥100 |
| 云GPU (AutoDL) | 1小时 | ¥2-3 |

**云GPU优势明显！**

---

## 🎯 推荐平台

### AutoDL（推荐）
- 网址: https://www.autodl.com/
- 优势: 便宜稳定，按量付费
- RTX 4090: ¥1.5/小时

### Google Colab
- 网址: https://colab.research.google.com/
- 优势: 免费T4
- 付费: A100 ($9.99/月)

### Kaggle
- 网址: https://www.kaggle.com/
- 优势: 完全免费
- GPU: P100 (30小时/周)

---

## 📖 核心文件说明

### 一键运行脚本

| 脚本 | 功能 | 耗时 |
|------|------|------|
| `run_all.sh` | 生成训练数据 | 20分钟 |
| `install_training_deps.sh` | 安装训练依赖 | 5分钟 |
| `run_training.sh` | 训练模型（旧，推荐手动） | - |

### 核心Python脚本

| 脚本 | 功能 |
|------|------|
| `cleaner.py` | 清洗数据 |
| `scripts/parse_corpus.py` | 解析语料 |
| `scripts/generate_training_data.py` | 生成训练数据 |
| `scripts/train_model.py` | 模型微调 |
| `scripts/test_model.py` | 测试模型 |
| `scripts/check_progress.py` | 查看进度 |

---

## 🎁 特色功能

1. **零配置**: 克隆即用，一键运行
2. **智能提取**: 无需爬取历史数据
3. **格式兼容**: 自动适配差异
4. **中断保护**: 数据永不丢失
5. **成本极低**: 总计 < ¥3元
6. **完全自动化**: 无需手动干预

---

## 📈 数据规模建议

| 阶段 | 天数 | 样本数 | 状态 |
|------|------|--------|------|
| 当前 | 29天 | 400-500 | ⚠️ 基础测试 |
| 最低 | 60天 | 800-1000 | ✅ 可用 |
| 推荐 | 180天 | 2500-3000 | ⭐ 优秀 |
| 理想 | 360天 | 5000-6000 | ⭐⭐ 专家 |

---

## 🎊 成功标志

看到以下输出即为成功：

```
=========================================
   ✅ 所有步骤完成！
=========================================

📁 生成的文件：
   - outputs/training_data/training_dataset.jsonl (400+样本)

=========================================
   ✅ 训练完成！
=========================================

📁 模型保存在: models/financial_assistant/
```

---

## 📄 License

MIT License - 仅供学习研究使用

---

## 🚀 立即开始

在AutoDL终端复制运行：

```bash
git clone https://github.com/li147852xu/eris.git && \
cd eris && \
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c" && \
export OPENAI_BASE_URL="https://api.deepseek.com/v1" && \
./run_all.sh && \
./install_training_deps.sh && \
python3 scripts/train_model.py
```

**全自动，坐等1小时完成！** ⏳

---

**项目地址**: https://github.com/li147852xu/eris.git
