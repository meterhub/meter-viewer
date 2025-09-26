#!/usr/bin/env python3
"""
测试迁移工具的基本功能

这个脚本用于快速测试迁移工具是否能正常工作
"""

import subprocess
import sys
from pathlib import Path


def test_basic_functionality():
    """测试基本功能"""
    print("测试迁移工具基本功能...")
    
    # 检查工具文件是否存在
    migrate_script = Path("migrate_labels.py")
    validate_script = Path("validate_labels.py")
    
    if not migrate_script.exists():
        print("✗ migrate_labels.py 不存在")
        return False
    
    if not validate_script.exists():
        print("✗ validate_labels.py 不存在")
        return False
    
    print("✓ 工具文件存在")
    
    # 测试帮助信息
    try:
        result = subprocess.run(
            [sys.executable, "migrate_labels.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "usage:" in result.stdout.lower():
            print("✓ migrate_labels.py 帮助信息正常")
        else:
            print("✗ migrate_labels.py 帮助信息异常")
            return False
    except Exception as e:
        print(f"✗ 测试帮助信息失败: {e}")
        return False
    
    # 测试验证工具帮助信息
    try:
        result = subprocess.run(
            [sys.executable, "validate_labels.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "usage:" in result.stdout.lower():
            print("✓ validate_labels.py 帮助信息正常")
        else:
            print("✗ validate_labels.py 帮助信息异常")
            return False
    except Exception as e:
        print(f"✗ 测试验证工具帮助信息失败: {e}")
        return False
    
    print("✓ 基本功能测试通过")
    return True


def test_imports():
    """测试必要的导入"""
    print("\n测试必要的导入...")
    
    try:
        # 测试迁移工具的导入
        with open("migrate_labels.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查必要的导入
        required_imports = [
            "import json",
            "import argparse", 
            "from pathlib import Path",
            "from datetime import datetime",
            "from meterviewer"
        ]
        
        for imp in required_imports:
            if imp not in content:
                print(f"✗ 缺少必要的导入: {imp}")
                return False
        
        print("✓ 所有必要的导入都存在")
        return True
        
    except Exception as e:
        print(f"✗ 测试导入失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 50)
    print("迁移工具测试")
    print("=" * 50)
    
    # 切换到工具目录
    original_dir = Path.cwd()
    tools_dir = Path(__file__).parent
    
    try:
        os.chdir(tools_dir)
        print(f"工作目录: {tools_dir}")
        
        # 运行测试
        success = True
        success &= test_basic_functionality()
        success &= test_imports()
        
        print("\n" + "=" * 50)
        if success:
            print("✅ 所有测试通过!")
            print("\n下一步:")
            print("1. 运行: python migrate_labels.py")
            print("2. 运行: python validate_labels.py")
            print("3. 检查生成的 data/labels.json 文件")
        else:
            print("❌ 测试失败!")
            
        return success
        
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    import os
    
    success = main()
    sys.exit(0 if success else 1)