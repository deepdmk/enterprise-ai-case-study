#!/usr/bin/env python3
"""
Merge 4 fine-tuned Llama 3.1 8B models into a Mixtral-style 4x8B MoE.
Uses mergekit-moe with hidden gate mode for optimal quality.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
EXPERT_PATHS = [
    "./output_moe/llama3_expert_1",
    "./output_moe/llama3_expert_2",
    "./output_moe/llama3_expert_3",
    "./output_moe/llama3_expert_4",
]

CONFIG_FILE = "merge_moe_config.yaml"
OUTPUT_DIR = "./output_merged_moe"

def verify_experts_exist():
    """Verify all expert models exist"""
    missing = []
    for expert_path in EXPERT_PATHS:
        if not Path(expert_path).exists():
            missing.append(expert_path)
    
    if missing:
        print("✗ Missing expert models:")
        for path in missing:
            print(f"  - {path}")
        sys.exit(1)
    
    print("✓ All expert models found")

def verify_config_exists():
    """Verify merge config file exists"""
    if not Path(CONFIG_FILE).exists():
        print(f"✗ Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    print(f"✓ Config file found: {CONFIG_FILE}")

def run_merge():
    """Execute mergekit-moe merge command"""
    cmd = [
        "mergekit-moe",
        CONFIG_FILE,
        OUTPUT_DIR,
        "--cuda",
        "--lazy-unpickle"
    ]
    
    print(f"\n{'=' * 60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"Estimated time: 30-60 minutes")
    print(f"{'=' * 60}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Merge completed successfully!")
        print(f"✓ MoE model saved to: {OUTPUT_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Merge failed with error code: {e.returncode}")
        sys.exit(1)

def main():
    print("=" * 60)
    print("Merging 4x Llama 3.1 8B into Mixtral-style 4x8B MoE")
    print("=" * 60)
    
    verify_experts_exist()
    verify_config_exists()
    run_merge()
    
    print("\nNext steps:")
    print(f"1. Merged MoE model: {OUTPUT_DIR}")
    print("2. Fine-tune: python finetune_moe.py")
    print("3. Push to Hub: huggingface-cli upload your_username/model_name ./output_merged_moe .")

if __name__ == "__main__":
    main()
