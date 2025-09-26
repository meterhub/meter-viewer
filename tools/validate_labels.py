#!/usr/bin/env python3
"""
验证迁移后的 JSON 标签文件

使用方式:
    python tools/validate_labels.py --json data/labels.json --root data
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any
import sys


def validate_labels(json_path: Path, root_path: Path):
    """验证标签文件的完整性"""
    if not json_path.exists():
        print(f"错误: JSON 文件 {json_path} 不存在")
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误: 无法读取 JSON 文件: {e}")
        return False
    
    print("=" * 50)
    print("JSON 标签文件验证报告")
    print("=" * 50)
    
    # 检查基本结构
    if 'version' not in data:
        print("✗ 缺少 version 字段")
        return False
    
    if 'metadata' not in data:
        print("✗ 缺少 metadata 字段")
        return False
    
    if 'labels' not in data:
        print("✗ 缺少 labels 字段")
        return False
    
    print(f"✓ 文件结构验证通过")
    print(f"版本: {data.get('version')}")
    
    # 检查元数据
    metadata = data.get('metadata', {})
    print(f"创建时间: {metadata.get('created_at')}")
    print(f"总标签数: {metadata.get('total_images', 0)}")
    print(f"成功迁移: {metadata.get('successful_migrations', 0)}")
    print(f"失败迁移: {metadata.get('failed_migrations', 0)}")
    
    # 检查标签数据
    labels = data.get('labels', {})
    actual_count = len(labels)
    expected_count = metadata.get('total_images', 0)
    
    if actual_count != expected_count:
        print(f"✗ 标签数量不匹配: 预期 {expected_count}, 实际 {actual_count}")
        return False
    
    print(f"✓ 标签数量验证通过: {actual_count}")
    
    # 检查随机样本
    sample_keys = list(labels.keys())[:5]
    print(f"\n随机样本检查 (前5个):")
    
    all_samples_valid = True
    
    for key in sample_keys:
        label = labels[key]
        print(f"\n  {key}:")
        print(f"    数值: {label.get('meter_value')}")
        
        # 检查对应的图像文件是否存在
        image_path = root_path / key
        if image_path.exists():
            print(f"    ✓ 图像文件存在")
        else:
            print(f"    ✗ 图像文件缺失: {image_path}")
            all_samples_valid = False
        
        # 检查必要的字段
        required_fields = ['meter_value', 'rect']
        for field in required_fields:
            if field not in label:
                print(f"    ✗ 缺少必要字段: {field}")
                all_samples_valid = False
        
        # 检查矩形字段
        rect = label.get('rect', {})
        rect_fields = ['xmin', 'ymin', 'xmax', 'ymax']
        for field in rect_fields:
            if field not in rect:
                print(f"    ✗ 矩形缺少字段: {field}")
                all_samples_valid = False
    
    if all_samples_valid:
        print(f"\n✓ 样本检查全部通过")
    else:
        print(f"\n✗ 样本检查发现问题")
    
    # 统计基本信息
    print(f"\n统计信息:")
    print(f"- 总标签数: {len(labels)}")
    
    # 检查是否有数字位置信息
    has_digits = sum(1 for label in labels.values() if label.get('digits'))
    print(f"- 包含数字位置信息的标签: {has_digits}")
    
    # 检查源 XML 信息
    has_source_xml = sum(1 for label in labels.values() if label.get('source_xml'))
    print(f"- 包含源 XML 信息的标签: {has_source_xml}")
    
    print("=" * 50)
    
    if all_samples_valid:
        print("✅ 验证通过! JSON 标签文件格式正确")
        return True
    else:
        print("❌ 验证失败! 请检查 JSON 文件")
        return False


def check_file_integrity(json_path: Path):
    """检查文件完整性"""
    try:
        file_size = json_path.stat().st_size
        print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        if file_size == 0:
            print("✗ 文件为空")
            return False
        
        return True
    except Exception as e:
        print(f"文件完整性检查失败: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='验证 JSON 标签文件')
    parser.add_argument('--json', default='data/labels.json', help='JSON 标签文件路径 (默认: data/labels.json)')
    parser.add_argument('--root', default='data', help='数据集根目录 (默认: data)')
    
    args = parser.parse_args()
    
    json_path = Path(args.json)
    root_path = Path(args.root)
    
    if not root_path.exists():
        print(f"错误: 根目录 {root_path} 不存在")
        sys.exit(1)
    
    # 检查文件完整性
    if not check_file_integrity(json_path):
        sys.exit(1)
    
    # 验证标签内容
    success = validate_labels(json_path, root_path)
    
    if not success:
        sys.exit(1)