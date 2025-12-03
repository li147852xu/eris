# 🤖 金融助手AI训练系统

基于你的独特分析风格，训练一个专业的A股市场分析助手。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 项目目标

训练一个能够：
- 📊 分析当日市场走势
- 🔮 预测未来市场方向  
- 💡 提供板块和个股操作建议
- 🎨 保持你的独特表达风格（"草原"=股市、"羊"=股票、"吃桃"=亏损）

## ✨ 核心特点

- **🎭 风格学习**: 从你的日常分析中学习独特的表达方式
- **📈 数据驱动**: 结合真实市场数据和专家分析
- **⚡ 自动化**: 一键生成训练数据，自动化微调流程
- **🔄 可扩展**: 持续添加新语料，不断提升模型能力
- **☁️ 云GPU友好**: 专为云平台优化，一键运行

## 📊 当前数据规模

- ✅ 语料文件: **29天**（2025-10-23 至 2025-12-02）
- ✅ 预计样本: **约400-500个**（使用DeepSeek增强）
- ⚠️ 推荐目标: 60-180天以上

## 🚀 快速开始（云GPU平台）

### 方案A: 完全一键运行

```bash
# 1. 克隆项目
git clone https://github.com/li147852xu/eris.git
cd eris

# 2. 设置API key（使用DeepSeek）
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 3. 一键生成训练数据（约15-25分钟）
./run_all.sh

# 4. 一键训练模型（约30-60分钟，需GPU）
./run_training.sh
```

### 方案B: 分步执行

```bash
# 步骤1: 安装依赖
pip install -r requirements.txt

# 步骤2: 清洗数据（可选）
python3 cleaner.py

# 步骤3: 解析语料
python3 scripts/parse_corpus.py

# 步骤4: 生成训练数据
python3 scripts/generate_training_data.py

# 步骤5: 训练模型（需GPU）
python3 scripts/train_model.py
```

## 📁 项目结构

```
eris/
├── README.md                # 本文件
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
├── cleaner.py              # 数据清洗工具
├── run_all.sh              # 一键生成训练数据
├── run_training.sh         # 一键训练模型
│
├── data/                    # 原始语料（29个文件）
│   ├── 2025-10-23.md
│   ├── 2025-10-24.md
│   └── ... (29个文件)
│
├── outputs/
│   ├── raw_data/           # 市场数据（爬取的）
│   ├── processed_data/     # 语料解析结果
│   │   └── parsed_corpus.json
│   └── training_data/      # 训练数据集
│       ├── training_dataset.json
│       └── training_dataset.jsonl
│
├── models/                 # 训练后的模型
│   └── financial_assistant/
│
├── logs/                   # 日志文件
│
└── scripts/
    ├── parse_corpus.py              # 语料解析
    ├── fetch_market_data_enhanced.py # 市场数据爬取（增强版）
    ├── generate_training_data.py    # 训练数据生成
    ├── train_model.py               # 模型微调
    ├── check_progress.py            # 进度检查
    └── test_model.py                # 模型测试
```

## 💡 训练数据生成原理

### 数据流转

```
原始语料 (data/*.md)
    ↓ [解析]
结构化数据 (parsed_corpus.json)  
    ↓ [DeepSeek增强]
训练样本 (training_dataset.jsonl)
    ↓ [LoRA微调]
金融助手模型
```

### 样本格式

```json
{
  "instruction": "今天大盘走势怎么看？",
  "input": "日期：2025-11-14。今晨美股大跌。指数点位3950点。",
  "output": "今天大盘受美股大跌影响，大概率会低开，尤其是科技线相关板块。关键看低开后的承接情况，如果承接好，可以低吸做T。记住，我们的草原（股市）有自己的节奏...",
  "section_type": "早自习",
  "date": "2025-11-14"
}
```

### 为什么需要DeepSeek API？

- **扩充样本数量**: 29天 × 3 = 87个 → **400-500个**样本
- **多样化问题**: 自动生成不同角度的提问
- **提取关键信息**: 从长文本中提取核心观点
- **成本极低**: 29天约 ¥0.5-1元

## ⏱️ 时间预估

### 数据生成（run_all.sh）

| 步骤 | 时间 | 说明 |
|------|------|------|
| 解析语料 | 5秒 | 29个文件 |
| DeepSeek生成 | 15-25分钟 | 87章节 → 400+样本 |
| **总计** | **~20分钟** | 完全自动化 |

### 模型训练（run_training.sh）

| GPU型号 | 显存 | 训练时间 | 成本 | 推荐度 |
|---------|------|---------|------|--------|
| RTX 4090 | 24GB | 30-50分钟 | ¥1-2 | ⭐⭐⭐⭐⭐ |
| A100 | 40/80GB | 15-30分钟 | ¥3-5 | ⭐⭐⭐⭐⭐ |
| V100 | 32GB | 1-1.5小时 | ¥1-2 | ⭐⭐⭐⭐ |
| T4 | 16GB | 1.5-2.5小时 | ¥0.5-1 | ⭐⭐⭐ |

**Mac本地**: 不推荐（1-7天，且可能失败）

## 🔧 配置说明

### 环境变量

创建 `.env` 文件或设置环境变量：

```bash
# DeepSeek API（必需，用于生成训练数据）
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 日志级别（可选）
export LOG_LEVEL="INFO"
```

### 模型配置

编辑 `config.py` 可修改：

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

## 📝 添加新语料

### 文件命名规范

**必须**严格按照格式：`YYYY-MM-DD.md`

示例：
- ✅ 正确：`2025-12-03.md`
- ❌ 错误：`12-03.md`, `2025-12-3.md`

### 文件结构模板

```markdown
# XX月XX日早自习，...

（盘前分析内容）

# （主1）今日复盘...

（当日复盘内容）

# （主2）明日展望...

（明日预测内容）
```

### 格式兼容性

✅ **高度兼容**: 
- 章节标题格式可以略有差异
- 内容长度不限
- 自动识别日期和章节

### 添加后重新生成

```bash
# 只需重新运行一键脚本
./run_all.sh
```

## 🛠️ 实用工具

### 1. 数据清洗

```bash
# 批量清洗data/目录下的所有markdown文件
python3 cleaner.py
```

功能：
- 删除公众号头部垃圾
- 删除图片链接
- 删除emoji
- 规范化格式

### 2. 进度检查

```bash
# 实时查看生成进度
python3 scripts/check_progress.py
```

### 3. 测试模式

```bash
# 只用2天数据快速测试（~5分钟）
python3 scripts/test_generate.py
```

## 📈 数据规模建议

| 阶段 | 天数 | 样本数（DeepSeek增强） | 状态 | 建议 |
|------|------|---------------------|------|------|
| 当前 | 29天 | ~400-500个 | ⚠️ 基础 | 可开始测试 |
| 最低 | 60天 | ~800-1000个 | ✅ 及格 | 可正式训练 |
| 推荐 | 180天 | ~2500-3000个 | ⭐ 优秀 | 效果显著 |
| 理想 | 360天 | ~5000-6000个 | ⭐⭐ 专家 | 顶级表现 |

## 🐛 常见问题与解决

### Q1: DeepSeek API调用失败

**症状**: "Expecting value: line 1 column 1"

**解决**: 
- 检查API key是否正确
- 检查网络连接
- 已内置重试机制和错误处理

### Q2: 数据格式不兼容

**症状**: 某些日期文件解析失败

**解决**:
- 运行 `python3 cleaner.py` 清洗数据
- 检查文件名是否为 `YYYY-MM-DD.md`
- 确保包含早自习、主1、主2三个部分

### Q3: Mac本地训练太慢

**解决**: 
- 使用云GPU平台（AutoDL推荐）
- 或使用Google Colab免费GPU
- 本地Mac训练需要1-7天

### Q4: 显存不足

**解决**: 
在 `config.py` 中调整：
```python
FINETUNE_CONFIG = {
    "batch_size": 2,  # 降低batch size
    "gradient_accumulation_steps": 16,  # 增加梯度累积
}
```

## 🎓 技术栈

- **数据处理**: pandas, json, regex
- **数据获取**: akshare, efinance（免费A股数据）
- **AI增强**: DeepSeek API（中文优化，成本低）
- **模型训练**: transformers, peft (LoRA), torch
- **基座模型**: Qwen2.5-7B-Instruct（中文金融能力强）

## 🌐 云GPU平台推荐

### AutoDL（推荐）
- 网址: https://www.autodl.com/
- 特点: 便宜稳定，按量付费
- GPU: RTX 4090 (¥1.5/小时)
- 预估: ¥2-3完成全流程

### Google Colab
- 网址: https://colab.research.google.com/
- 特点: 免费T4，付费A100
- GPU: T4免费，A100 ($9.99/月)

### Kaggle
- 网址: https://www.kaggle.com/
- 特点: 完全免费
- GPU: P100 (30小时/周)

## 📦 完整工作流程

### 在云GPU平台上

```bash
# 1. SSH连接到云GPU实例

# 2. 克隆项目
git clone https://github.com/li147852xu/eris.git
cd eris

# 3. 配置API key
export OPENAI_API_KEY="your_deepseek_key"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 4. 一键生成训练数据（~20分钟）
./run_all.sh

# 5. 一键训练模型（~30-60分钟）
./run_training.sh

# 6. 测试模型
python3 scripts/test_model.py
```

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 添加新语料到data/目录

# 3. 清洗数据
python3 cleaner.py

# 4. 重新生成训练数据
./run_all.sh
```

## 🔄 持续更新流程

### 每日工作

1. 在 `data/` 添加当天分析文件（格式：`YYYY-MM-DD.md`）
2. 包含三个部分：早自习、主1、主2

### 每周工作

```bash
# 重新生成训练数据
./run_all.sh

# 如果样本数达到500+，重新训练
./run_training.sh
```

### 里程碑

- [x] 29天语料 → 初步测试
- [ ] 60天语料 → 首次正式训练
- [ ] 90天语料 → 效果改善
- [ ] 180天语料 → 推荐训练
- [ ] 360天语料 → 达到专家级

## 🎯 训练配置详解

### 基座模型选择

默认使用 **Qwen2.5-7B-Instruct**：
- 中文能力优秀
- 金融领域理解好
- 7B参数适中，训练快
- 开源免费

### LoRA微调

- 只训练少量参数（~100MB）
- 显存需求低（16GB即可）
- 训练速度快
- 效果接近全量微调

### 超参数

```python
{
    "lora_r": 64,              # LoRA秩
    "lora_alpha": 16,          # LoRA alpha
    "learning_rate": 2e-4,     # 学习率
    "num_epochs": 3,           # 训练轮数
    "batch_size": 4,           # 批次大小
}
```

## 📊 数据质量保证

### 自动清洗 (cleaner.py)

- 删除公众号格式
- 去除图片和链接
- 规范化空行
- 幂等安全（不损坏内容）

### 格式验证

- 自动检测日期格式
- 识别三个章节
- 提取关键信息
- 兼容格式微小差异

### 智能提取

从语料中自动提取：
- 指数点位
- 涨跌趋势
- 成交量信息
- 资金流向
- 板块热点

## 🔐 API Key说明

### DeepSeek API

- 获取地址: https://platform.deepseek.com/
- 成本: 约¥0.001/1K tokens
- 29天数据: 约¥0.5-1元
- 比OpenAI便宜10倍+

### 为什么用DeepSeek？

1. ✅ 中文能力强
2. ✅ 成本极低
3. ✅ 专门优化推理能力
4. ✅ API稳定快速

## 🚀 性能优化

### 数据生成优化

- ✅ 自动保存中间结果（每5天）
- ✅ 捕获中断，防止数据丢失
- ✅ 多线程处理（可选）
- ✅ 智能重试机制

### 训练优化

- ✅ 梯度累积（显存优化）
- ✅ 混合精度训练（FP16）
- ✅ 自动checkpoint保存
- ✅ 训练日志记录

## 📚 学习资源

### 大模型微调

- [LoRA论文](https://arxiv.org/abs/2106.09685)
- [Qwen2.5文档](https://github.com/QwenLM/Qwen2.5)
- [PEFT库](https://github.com/huggingface/peft)

### A股数据获取

- [AKShare文档](https://akshare.akfamily.xyz/)
- [efinance文档](https://github.com/Micro-sheep/efinance)

## 💬 常见问题

**Q: 29天数据够吗？**
A: 可以开始测试，但建议继续积累到60-180天。

**Q: 一定要云GPU吗？**
A: 强烈建议。Mac本地训练需要1-7天，云GPU只需30-60分钟，成本更低。

**Q: 数据格式有差异怎么办？**
A: 已内置智能解析，可兼容章节标题的微小差异。运行cleaner.py可规范化格式。

**Q: 如何评估模型效果？**
A: 
1. 运行 `python3 scripts/test_model.py`
2. 给模型提供真实市场数据
3. 检查生成的分析是否符合风格
4. 与你的真实分析对比

**Q: 训练失败怎么办？**
A: 
1. 检查日志: `cat logs/train_model.log`
2. 降低batch_size
3. 确保GPU显存 ≥ 16GB

## 📞 问题反馈

遇到问题请检查：
1. 📂 日志文件: `logs/` 目录
2. ⚙️ 配置文件: `config.py`
3. 📊 数据文件: `outputs/` 目录

## 🎉 预期成果

完成后你将拥有：

1. ✅ **400-500个高质量训练样本**（29天数据）
2. ✅ **微调后的7B参数金融助手**
3. ✅ **完全自动化的更新流程**
4. ✅ **可随时添加新数据并重新训练**

## 📄 License

MIT License - 仅供学习研究使用

---

## 🚀 开始你的AI金融助手之旅

```bash
git clone https://github.com/li147852xu/eris.git
cd eris
./run_all.sh  # 生成训练数据
./run_training.sh  # 训练模型
```

**记住**: 数据质量和数量是关键！坚持每天积累语料 📈
