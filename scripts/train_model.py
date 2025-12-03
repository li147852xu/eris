"""模型微调脚本 - 使用LoRA方法"""
import json
import sys
from pathlib import Path
from typing import Dict, List
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
from loguru import logger

sys.path.append(str(Path(__file__).parent.parent))
from config import TRAINING_DATA_DIR, MODEL_DIR, FINETUNE_CONFIG, LOG_DIR

# 配置日志
logger.add(LOG_DIR / "train_model.log", rotation="10 MB")


class FinancialAssistantTrainer:
    """金融助手训练器"""
    
    def __init__(self):
        self.base_model = FINETUNE_CONFIG["base_model"]
        self.output_dir = MODEL_DIR / "financial_assistant"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_training_data(self, filename: str = "training_dataset.jsonl") -> Dataset:
        """加载训练数据"""
        file_path = TRAINING_DATA_DIR / filename
        
        logger.info(f"加载训练数据: {file_path}")
        
        # 读取JSONL文件
        data_list = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data_list.append(json.loads(line))
        
        logger.info(f"加载了 {len(data_list)} 个训练样本")
        
        # 转换为Dataset格式
        dataset = Dataset.from_list(data_list)
        return dataset
    
    def preprocess_data(self, examples, tokenizer):
        """数据预处理"""
        # 构建完整的输入文本
        prompts = []
        for i in range(len(examples['instruction'])):
            instruction = examples['instruction'][i]
            input_text = examples.get('input', [''] * len(examples['instruction']))[i]
            output = examples['output'][i]
            
            # 格式化为对话格式
            if input_text:
                prompt = f"<|im_start|>system\n你是一个专业的A股市场分析助手，具有独特的表达风格。你用"草原"指代股市，"羊"指代股票，"吃桃"指代亏损。<|im_end|>\n<|im_start|>user\n{instruction}\n背景：{input_text}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
            else:
                prompt = f"<|im_start|>system\n你是一个专业的A股市场分析助手，具有独特的表达风格。你用"草原"指代股市，"羊"指代股票，"吃桃"指代亏损。<|im_end|>\n<|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
            
            prompts.append(prompt)
        
        # Tokenize
        model_inputs = tokenizer(
            prompts,
            max_length=FINETUNE_CONFIG["max_length"],
            truncation=True,
            padding=False
        )
        
        # 设置labels
        model_inputs["labels"] = model_inputs["input_ids"].copy()
        
        return model_inputs
    
    def setup_model_and_tokenizer(self):
        """设置模型和tokenizer"""
        logger.info(f"加载基座模型: {self.base_model}")
        
        # 加载tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model,
            trust_remote_code=True,
            padding_side="right"
        )
        
        # 设置pad_token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # 加载模型
        model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # 配置LoRA
        lora_config = LoraConfig(
            r=FINETUNE_CONFIG["lora_r"],
            lora_alpha=FINETUNE_CONFIG["lora_alpha"],
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=FINETUNE_CONFIG["lora_dropout"],
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # 应用LoRA
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
        
        return model, tokenizer
    
    def train(self):
        """开始训练"""
        logger.info("开始训练金融助手模型")
        
        # 加载数据
        dataset = self.load_training_data()
        
        # 设置模型和tokenizer
        model, tokenizer = self.setup_model_and_tokenizer()
        
        # 数据预处理
        logger.info("预处理训练数据")
        tokenized_dataset = dataset.map(
            lambda examples: self.preprocess_data(examples, tokenizer),
            batched=True,
            remove_columns=dataset.column_names
        )
        
        # 训练参数
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            per_device_train_batch_size=FINETUNE_CONFIG["batch_size"],
            gradient_accumulation_steps=FINETUNE_CONFIG["gradient_accumulation_steps"],
            learning_rate=FINETUNE_CONFIG["learning_rate"],
            num_train_epochs=FINETUNE_CONFIG["num_epochs"],
            logging_steps=10,
            save_steps=100,
            save_total_limit=3,
            fp16=True,
            report_to="none",
            remove_unused_columns=False,
        )
        
        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            padding=True
        )
        
        # 创建Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # 开始训练
        logger.info("开始训练...")
        trainer.train()
        
        # 保存模型
        logger.info(f"保存模型到: {self.output_dir}")
        trainer.save_model()
        tokenizer.save_pretrained(self.output_dir)
        
        logger.info("训练完成！")


def main():
    """主函数"""
    trainer = FinancialAssistantTrainer()
    trainer.train()


if __name__ == "__main__":
    main()

