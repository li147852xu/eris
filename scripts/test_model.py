"""测试训练后的模型"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_DIR, FINETUNE_CONFIG

def load_model():
    """加载训练后的模型"""
    model_path = MODEL_DIR / "financial_assistant"
    base_model = FINETUNE_CONFIG["base_model"]
    
    print("加载模型...")
    
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        base_model,
        trust_remote_code=True
    )
    
    # 加载基座模型
    base_model_loaded = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # 加载LoRA权重
    model = PeftModel.from_pretrained(base_model_loaded, str(model_path))
    model = model.merge_and_unload()  # 合并LoRA权重
    
    print("✓ 模型加载完成")
    return model, tokenizer

def test_inference(model, tokenizer, question: str, context: str = ""):
    """测试推理"""
    # 构建prompt
    if context:
        prompt = f"<|im_start|>system\n你是一个专业的A股市场分析助手，具有独特的表达风格。你用"草原"指代股市，"羊"指代股票，"吃桃"指代亏损。<|im_end|>\n<|im_start|>user\n{question}\n背景：{context}<|im_end|>\n<|im_start|>assistant\n"
    else:
        prompt = f"<|im_start|>system\n你是一个专业的A股市场分析助手，具有独特的表达风格。你用"草原"指代股市，"羊"指代股票，"吃桃"指代亏损。<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # 生成
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
    
    # 解码
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    # 提取assistant的回答
    assistant_response = response.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0]
    
    return assistant_response

def main():
    """主函数"""
    print("=" * 60)
    print("   金融助手模型测试")
    print("=" * 60)
    print()
    
    # 加载模型
    model, tokenizer = load_model()
    
    # 测试用例
    test_cases = [
        {
            "question": "今天大盘走势怎么看？",
            "context": "日期：2025-12-03。上证指数3900点，涨幅0.5%。"
        },
        {
            "question": "军工板块后续怎么操作？",
            "context": ""
        },
        {
            "question": "现在应该关注哪些主流方向？",
            "context": ""
        }
    ]
    
    print("开始测试...")
    print()
    
    for i, test in enumerate(test_cases, 1):
        print(f"[测试 {i}]")
        print(f"问题: {test['question']}")
        if test['context']:
            print(f"背景: {test['context']}")
        print()
        
        response = test_inference(model, tokenizer, test['question'], test['context'])
        print(f"回答: {response}")
        print()
        print("-" * 60)
        print()
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()

