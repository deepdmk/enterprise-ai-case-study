#!/usr/bin/env python3
"""
Fine-tune a custom 4x8B MoE model with LoRA.
Based on Llama 3.1 8B fine-tuning with Unsloth, adapted for MoE architecture.
"""

import torch
from trl import SFTTrainer
from datasets import load_dataset
from transformers import TrainingArguments, TextStreamer, AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType

# Configuration
MODEL_NAME = "your-org/custom-4x8b-moe"  # Replace with your MoE model
MAX_SEQ_LENGTH = 2048
OUTPUT_DIR = "output_moe"

# Load model and tokenizer
print(f"Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=True,
)

# Configure LoRA for MoE
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "up_proj", "down_proj", "gate_proj"],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load and prepare dataset
print("Loading dataset...")
dataset = load_dataset("mlabonne/FineTome-100k", split="train")

def apply_template(examples):
    """Apply chat template to examples"""
    messages = examples["conversations"]
    text = [
        tokenizer.apply_chat_template(
            message, 
            tokenize=False, 
            add_generation_prompt=False
        ) for message in messages
    ]
    return {"text": text}

dataset = dataset.map(apply_template, batched=True)

# Training
print("Starting training...")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_num_proc=2,
    packing=True,
    args=TrainingArguments(
        learning_rate=3e-4,
        lr_scheduler_type="linear",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=4,
        fp16=True,
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        warmup_steps=10,
        output_dir=OUTPUT_DIR,
        seed=0,
    ),
)

trainer.train()

# Save model
print(f"Saving model to {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Training complete!")
