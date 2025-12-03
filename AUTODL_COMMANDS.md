# 🚀 AutoDL 运行命令（复制即用）

## ✅ Bug已全部修复！

已推送到GitHub，现在可以安全运行。

---

## 📋 在AutoDL终端执行

### 步骤1: 拉取最新代码

```bash
cd ~/eris
git pull
```

### 步骤2: 重新运行（一键）

```bash
export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
./run_all.sh
```

---

## ⏱️ 预计耗时

- **数据生成**: 约20-25分钟
- **输出**: 400-500个训练样本

---

## 📊 进度监控

### 另开一个终端查看进度

```bash
cd ~/eris
watch -n 5 "python3 scripts/check_progress.py"
```

### 或实时查看日志

```bash
tail -f logs/generate_training.log
```

---

## ✅ 完成标志

看到这个输出即为成功：

```
=========================================
   ✅ 所有步骤完成！
=========================================

📁 生成的文件：
   - outputs/training_data/training_dataset.jsonl (400+样本)

🚀 下一步：
   运行模型微调：
   ./run_training.sh
```

---

## 🎯 然后训练模型

数据生成完成后：

```bash
./run_training.sh
```

预计：
- RTX 4090: 30-50分钟
- A100: 15-30分钟

---

## 💡 快速命令参考

```bash
# 完整流程（一行）
cd ~/eris && git pull && export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c" && export OPENAI_BASE_URL="https://api.deepseek.com/v1" && ./run_all.sh && ./run_training.sh

# 只生成数据
cd ~/eris && git pull && export OPENAI_API_KEY="sk-2696d151d5a746aca92217ef7fbb513c" && export OPENAI_BASE_URL="https://api.deepseek.com/v1" && ./run_all.sh

# 只训练模型（数据已生成）
cd ~/eris && ./run_training.sh

# 查看进度
cd ~/eris && python3 scripts/check_progress.py

# 测试模型
cd ~/eris && python3 scripts/test_model.py
```

---

## 🐛 如果遇到问题

### 查看错误日志

```bash
cat logs/generate_training.log | tail -50
cat logs/train_model.log | tail -50
```

### 清空重来

```bash
cd ~/eris
rm -rf outputs logs
mkdir -p outputs/{raw_data,processed_data,training_data} logs
./run_all.sh
```

---

**现在开始运行！** 🚀

