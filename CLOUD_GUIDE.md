# ☁️ 云GPU平台完整使用指南

## 🎯 推荐方案：AutoDL

成本：¥2-3元，耗时：约50分钟（数据生成20分钟 + 训练30分钟）

## 📋 完整流程

### 1. 注册AutoDL

访问：https://www.autodl.com/

### 2. 创建实例

**推荐配置**:
- GPU: RTX 4090 (24GB) 或 A100
- 镜像: PyTorch 2.1.0 - Python 3.10 - CUDA 12.1
- 硬盘: 50GB
- 费用: ¥1.5-2.0/小时

### 3. 连接实例

```bash
# 点击"JupyterLab"或使用SSH连接
# SSH示例：
ssh -p xxxxx root@region-x.autodl.com
```

### 4. 克隆项目

```bash
cd /root/autodl-tmp
git clone https://github.com/li147852xu/eris.git
cd eris
```

### 5. 配置API Key

```bash
# 方法A: 设置环境变量（推荐）
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 方法B: 创建.env文件
cat > .env << EOF
OPENAI_API_KEY=sk-2696d151d5a746aca92217ef7fbb513c
OPENAI_BASE_URL=https://api.deepseek.com/v1
EOF
```

### 6. 一键运行

```bash
# 生成训练数据（约20分钟）
./run_all.sh

# 训练模型（约30-60分钟）
./run_training.sh
```

### 7. 查看结果

```bash
# 检查生成的训练数据
python3 scripts/check_progress.py

# 测试模型
python3 scripts/test_model.py
```

### 8. 下载模型

```bash
# 打包模型
cd models
tar -czf financial_assistant.tar.gz financial_assistant/

# 使用AutoDL文件管理器下载
# 或使用scp：
scp -P xxxxx root@region-x.autodl.com:/root/autodl-tmp/eris/models/financial_assistant.tar.gz ./
```

## ⏱️ 详细时间预估

### 数据生成阶段 (run_all.sh)

```
环境检查          : 10秒
安装依赖          : 2-3分钟
清洗数据          : 10秒
解析语料(29天)    : 5秒
DeepSeek生成      : 15-20分钟
━━━━━━━━━━━━━━━━━━━━━━━━━
总计              : ~20分钟
生成样本          : 400-500个
```

### 模型训练阶段 (run_training.sh)

| GPU | Batch Size | 训练时间 | 显存占用 |
|-----|-----------|---------|---------|
| RTX 4090 | 4 | 30-50分钟 | ~18GB |
| A100 40GB | 4 | 15-30分钟 | ~20GB |
| A100 80GB | 8 | 10-20分钟 | ~35GB |
| V100 32GB | 4 | 1-1.5小时 | ~20GB |
| T4 16GB | 2 | 2-3小时 | ~14GB |

**epoch数**: 3轮
**样本数**: 400-500个

## 💰 成本估算

### AutoDL成本

| GPU型号 | 单价/小时 | 预计时长 | 总成本 |
|---------|----------|---------|--------|
| RTX 4090 | ¥1.5 | 1小时 | **¥1.5** |
| A100 40GB | ¥3.0 | 0.8小时 | **¥2.4** |
| V100 32GB | ¥1.2 | 1.5小时 | **¥1.8** |

### DeepSeek API成本

- 29天数据: ¥0.5-1元

### 总成本

**完整流程**: ¥2-4元

## 🐛 常见问题

### Q1: 如何查看实时进度？

```bash
# 查看训练数据生成进度
python3 scripts/check_progress.py

# 查看训练进度（在另一个终端）
tail -f logs/train_model.log
```

### Q2: 训练中断怎么办？

训练会自动保存checkpoint，可以继续训练：
```bash
# 模型会从最后的checkpoint继续
python3 scripts/train_model.py
```

### Q3: 显存不足怎么办？

编辑 `config.py`:
```python
FINETUNE_CONFIG = {
    "batch_size": 2,  # 从4降到2
    "gradient_accumulation_steps": 16,  # 从8增到16
}
```

### Q4: 如何更换GPU？

AutoDL支持热迁移：
1. 创建快照
2. 新建更强GPU的实例
3. 从快照恢复
4. 继续训练

## 📊 监控训练

### 查看GPU使用

```bash
# 实时监控
watch -n 1 nvidia-smi

# 或使用
gpustat -i 1
```

### 查看训练日志

```bash
# 实时查看
tail -f logs/train_model.log

# 查看最新
tail -100 logs/train_model.log
```

## 🎓 优化建议

### 提升训练速度

1. 使用更大batch_size（如果显存够）
2. 使用flash attention（需要安装flash-attn）
3. 使用混合精度训练（已默认开启）

### 提升模型质量

1. 增加epoch数（3 → 5）
2. 使用更大的LoRA rank（64 → 128）
3. 积累更多语料（29天 → 180天）

## 🔄 迭代流程

### 本地添加新语料

```bash
# 1. 本地添加新的.md文件到data/
# 2. 推送到GitHub
git add data/
git commit -m "添加新语料：2025-12-03至2025-12-10"
git push
```

### 云端更新训练

```bash
# 1. 拉取最新代码
cd /root/autodl-tmp/eris
git pull

# 2. 重新生成训练数据
./run_all.sh

# 3. 重新训练
./run_training.sh
```

## 💡 高级用法

### 自定义训练参数

```bash
# 编辑config.py后训练
python3 scripts/train_model.py
```

### 使用更大模型

编辑 `config.py`:
```python
FINETUNE_CONFIG = {
    "base_model": "Qwen/Qwen2.5-14B-Instruct",  # 14B模型
    # 需要更多显存（32GB+）
}
```

### 多GPU训练

```bash
# 使用accelerate
accelerate launch scripts/train_model.py
```

## 📦 导出和部署

### 导出模型

```bash
# 合并LoRA权重
python3 -c "
from transformers import AutoModelForCausalLM
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct')
model = PeftModel.from_pretrained(base_model, 'models/financial_assistant')
merged_model = model.merge_and_unload()
merged_model.save_pretrained('models/financial_assistant_merged')
"
```

### 部署推理

```bash
# 使用vLLM加速推理
pip install vllm
vllm serve models/financial_assistant_merged --port 8000
```

## 🎉 完成标志

训练完成后，你会看到：

```
=========================================
   ✅ 训练完成！
=========================================

📁 模型保存在: models/financial_assistant/

包含文件:
  - adapter_config.json
  - adapter_model.safetensors
  - tokenizer配置
  - 训练日志
```

## 🚀 快速命令参考

```bash
# 完整流程
git clone https://github.com/li147852xu/eris.git && cd eris
export OPENAI_API_KEY="your_key"
./run_all.sh && ./run_training.sh

# 查看进度
python3 scripts/check_progress.py

# 测试模型
python3 scripts/test_model.py

# 更新数据
git pull && ./run_all.sh && ./run_training.sh
```

---

**祝训练顺利！** 🎉

