# 📦 依赖安装指南

## ⚠️ 问题：transformers和peft未安装

这是因为`run_training.sh`中使用了`-q`静默参数，掩盖了安装错误。

---

## ✅ 解决方案

### 方法1: 使用独立安装脚本（推荐）

```bash
cd ~/eris
git pull

# 先单独安装训练依赖
./install_training_deps.sh
```

这个脚本会：
- ✅ 显示详细安装过程
- ✅ 每个包单独安装并验证
- ✅ 自动检测GPU并选择对应版本
- ✅ 最后验证所有包是否安装成功

### 方法2: 手动安装

```bash
cd ~/eris
git pull

# 1. 升级pip
pip install --upgrade pip setuptools wheel

# 2. 安装PyTorch（CUDA 12.1版本）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. 验证PyTorch
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

# 4. 安装transformers
pip install transformers

# 5. 安装datasets
pip install datasets

# 6. 安装peft
pip install peft

# 7. 安装accelerate
pip install accelerate

# 8. 安装其他
pip install sentencepiece protobuf scipy

# 9. 验证所有包
python3 << 'EOF'
import torch
import transformers
import datasets
import peft
import accelerate

print("✅ 所有包已安装：")
print(f"  torch: {torch.__version__}")
print(f"  transformers: {transformers.__version__}")
print(f"  datasets: {datasets.__version__}")
print(f"  peft: {peft.__version__}")
print(f"  accelerate: {accelerate.__version__}")
EOF
```

---

## 🔍 诊断问题

### 检查已安装的包

```bash
pip list | grep -E "torch|transformers|peft|datasets|accelerate"
```

### 检查Python环境

```bash
python3 --version
which python3
pip --version
which pip
```

### 查看安装错误

```bash
# 尝试单独安装，查看错误信息
pip install transformers

# 如果失败，查看详细错误
pip install transformers --verbose
```

---

## 🎯 完整安装流程（AutoDL）

### 步骤1: 拉取最新代码

```bash
cd ~/eris
git pull
```

### 步骤2: 安装训练依赖

```bash
./install_training_deps.sh
```

**预计时间**: 3-5分钟

**期待输出**:
```
[1/6] 升级pip...
✓ pip已升级

[2/6] 安装PyTorch...
✓ PyTorch安装完成
  PyTorch版本: 2.1.0+cu121
  CUDA可用: True

[3/6] 安装transformers...
✓ transformers安装完成
  版本: 4.36.2

[4/6] 安装datasets...
✓ datasets安装完成
  版本: 2.15.0

[5/6] 安装peft...
✓ peft安装完成
  版本: 0.7.1

[6/6] 安装其他依赖...
✓ 其他依赖安装完成

✅ 所有必需包已安装！
```

### 步骤3: 开始训练

```bash
python3 scripts/train_model.py
```

---

## 🐛 常见错误

### 错误1: torch安装失败

**症状**: `No matching distribution found for torch`

**解决**:
```bash
# 使用清华镜像
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 错误2: transformers版本冲突

**症状**: `ERROR: Cannot uninstall 'transformers'`

**解决**:
```bash
pip install transformers --upgrade --force-reinstall
```

### 错误3: peft安装失败

**症状**: `Could not find a version that satisfies the requirement peft`

**解决**:
```bash
pip install --upgrade pip
pip install peft
```

---

## 📋 安装检查清单

运行这个命令验证所有包：

```bash
python3 << 'EOF'
packages = [
    'torch',
    'transformers', 
    'datasets',
    'peft',
    'accelerate',
    'sentencepiece',
    'loguru',
    'tqdm',
    'openai'
]

print("检查已安装的包：\n")
missing = []

for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {pkg:20s} {version}")
    except ImportError:
        print(f"✗ {pkg:20s} 未安装")
        missing.append(pkg)

print()
if missing:
    print(f"❌ 缺少: {', '.join(missing)}")
    print("\n安装命令:")
    print(f"pip install {' '.join(missing)}")
else:
    print("✅ 所有包已安装！")
EOF
```

---

## 🚀 修复后运行

在AutoDL终端：

```bash
# 1. 拉取修复
cd ~/eris
git pull

# 2. 安装训练依赖（新脚本，显示详细输出）
./install_training_deps.sh

# 3. 验证安装
python3 -c "import transformers, peft, torch; print('✅ 核心包已安装')"

# 4. 开始训练
python3 scripts/train_model.py
```

---

## 💡 为什么会这样？

AutoDL镜像可能：
1. 预装了某些包的旧版本
2. Python环境有冲突
3. 网络问题导致下载失败

**解决办法**: 使用独立的安装脚本`install_training_deps.sh`，显示详细输出，便于定位问题。

---

**现在重新运行！** 🚀

