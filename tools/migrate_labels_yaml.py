#!/usr/bin/env python3
"""
XML 标签迁移工具 - 将分散的 XML 标签汇总到统一的 YAML 文件

使用方式:
    uv run python tools/migrate_labels_yaml.py --root data --output data/labels.yaml
"""

import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from meterviewer.datasets.read.config import get_xml_config, get_xml_config_path, read_single_digit_rect
    from meterviewer.datasets.read.detection import read_area_pos
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


def find_all_image_files(root_path: Path) -> List[Path]:
    """查找所有图像文件"""
    return list(root_path.rglob("*.jpg"))


def extract_label_info(image_path: Path, root_path: Path) -> Dict[str, Any]:
    """从 XML 文件提取标签信息"""
    try:
        # 获取数值和矩形位置
        meter_value, rect_dict = get_xml_config(image_path)
        
        # 获取数字位置信息（如果存在）
        digit_positions = []
        try:
            single_xml_path = get_xml_config_path(image_path, "single")
            if single_xml_path.exists():
                digit_rects = read_single_digit_rect(single_xml_path)
                for i, digit_rect in enumerate(digit_rects):
                    if hasattr(digit_rect, 'xmin') and digit_rect.xmin:
                        digit_positions.append({
                            "index": i,
                            "value": meter_value[i] if i < len(meter_value) else "",
                            "rect": {
                                "xmin": int(digit_rect.xmin),
                                "ymin": int(digit_rect.ymin),
                                "xmax": int(digit_rect.xmax),
                                "ymax": int(digit_rect.ymax)
                            }
                        })
        except Exception as e:
            print(f"  警告: 无法读取数字位置信息: {e}")
        
        # 获取源 XML 文件路径
        xml_path = get_xml_config_path(image_path, "value")
        
        # 构建标签信息
        label_info = {
            "meter_value": meter_value,
            "rect": {
                "xmin": int(rect_dict.xmin),
                "ymin": int(rect_dict.ymin),
                "xmax": int(rect_dict.xmax),
                "ymax": int(rect_dict.ymax)
            },
            "digits": digit_positions,
            "source_xml": str(xml_path.relative_to(root_path)) if xml_path.exists() else ""
        }
        
        return label_info
        
    except Exception as e:
        print(f"处理 {image_path} 时出错: {e}")
        return None


def migrate_labels_yaml(root_path: Path, output_path: Path):
    """执行标签迁移到 YAML"""
    print(f"开始迁移标签到 YAML，根目录: {root_path}")
    print(f"输出文件: {output_path}")
    
    labels = {}
    image_files = find_all_image_files(root_path)
    
    print(f"找到 {len(image_files)} 个图像文件")
    
    success_count = 0
    error_count = 0
    
    for i, image_path in enumerate(image_files):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(image_files)} (成功: {success_count}, 失败: {error_count})")
        
        # 获取相对路径作为键
        rel_path = str(image_path.relative_to(root_path))
        
        # 提取标签信息
        label_info = extract_label_info(image_path, root_path)
        if label_info:
            labels[rel_path] = label_info
            success_count += 1
        else:
            error_count += 1
    
    # 构建完整的 YAML 结构
    result = {
        "version": "1.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "total_images": len(labels),
            "successful_migrations": success_count,
            "failed_migrations": error_count,
            "dataset_root": str(root_path),
            "source": "XML migration",
            "format": "yaml"
        },
        "labels": labels
    }
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存 YAML 文件到 data/ 目录
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\nYAML 迁移完成！")
    print(f"成功处理: {success_count} 个标签")
    print(f"处理失败: {error_count} 个文件")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='迁移 XML 标签到 YAML')
    parser.add_argument('--root', default='data', help='数据集根目录 (默认: data)')
    parser.add_argument('--output', default='data/labels.yaml', help='输出 YAML 文件路径 (默认: data/labels.yaml)')
    
    args = parser.parse_args()
    
    root_path = Path(args.root)
    output_path = Path(args.output)
    
    if not root_path.exists():
        print(f"错误: 根目录 {root_path} 不存在")
        sys.exit(1)
    
    try:
        migrate_labels_yaml(root_path, output_path)
    except KeyboardInterrupt:
        print("\n用户中断迁移过程")
        sys.exit(1)
    except Exception as e:
        print(f"迁移过程中发生错误: {e}")
        sys.exit(1)