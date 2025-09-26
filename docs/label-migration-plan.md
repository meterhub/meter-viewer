# 标签迁移方案 - XML 到 JSON 集中化管理

## 概述

本方案旨在将分散的 XML 标签文件迁移到统一的 JSON 文件中，同时保持原有 XML 文件不变，提供更好的标签管理体验。

## 当前问题

- 标签信息分散在多个 XML 文件中
- 每个图像对应一个 XML 文件，管理困难
- 缺乏统一的标签视图和查询功能
- 文件访问效率低

## 解决方案

### 1. 创建统一的 JSON 标签文件

在 `data/` 目录创建 `labels.json` 文件，包含所有标签信息的汇总。

### 2. JSON 文件结构

```json
{
  "version": "1.0",
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "total_images": 15000,
    "source": "XML migration",
    "dataset_root": "/home/svtter/work/projects/meterhub/meter-viewer/data"
  },
  "labels": {
    "lens_6/XL/XL/M7666-1112L0C2640CS/2017-11-25-05-56-01.jpg": {
      "meter_value": "123456",
      "rect": {
        "xmin": 100,
        "ymin": 50,
        "xmax": 300,
        "ymax": 200
      },
      "digits": [
        {
          "index": 0,
          "value": "1",
          "rect": {"xmin": 110, "ymin": 60, "xmax": 130, "ymax": 80}
        },
        {
          "index": 1,
          "value": "2", 
          "rect": {"xmin": 140, "ymin": 60, "xmax": 160, "ymax": 80}
        }
      ],
      "source_xml": "lens_6/XL/XL/M7666-1112L0C2640CS/baocun/2017-11-25-05-56-01.xml"
    }
  }
}
```

### 3. 迁移工具实现

创建迁移脚本 `tools/migrate_labels.py`：

```python
#!/usr/bin/env python3
"""
XML 标签迁移工具 - 将分散的 XML 标签汇总到统一的 JSON 文件
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from meterviewer.datasets.read.config import get_xml_config, get_xml_config_path
from meterviewer.datasets.read.detection import read_area_pos


def find_all_image_files(root_path: Path):
    """查找所有图像文件"""
    return root_path.rglob("*.jpg")


def extract_label_info(image_path: Path) -> Dict[str, Any]:
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
                    digit_positions.append({
                        "index": i,
                        "value": meter_value[i] if i < len(meter_value) else "",
                        "rect": {
                            "xmin": digit_rect.xmin,
                            "ymin": digit_rect.ymin,
                            "xmax": digit_rect.xmax,
                            "ymax": digit_rect.ymax
                        }
                    })
        except:
            pass
        
        # 构建标签信息
        label_info = {
            "meter_value": meter_value,
            "rect": dict(rect_dict),
            "digits": digit_positions,
            "source_xml": str(get_xml_config_path(image_path, "value").relative_to(root_path))
        }
        
        return label_info
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def migrate_labels(root_path: Path, output_path: Path):
    """执行标签迁移"""
    print(f"开始迁移标签，根目录: {root_path}")
    
    labels = {}
    image_files = list(find_all_image_files(root_path))
    
    print(f"找到 {len(image_files)} 个图像文件")
    
    for i, image_path in enumerate(image_files):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(image_files)}")
        
        # 获取相对路径作为键
        rel_path = str(image_path.relative_to(root_path))
        
        # 提取标签信息
        label_info = extract_label_info(image_path)
        if label_info:
            labels[rel_path] = label_info
    
    # 构建完整的 JSON 结构
    result = {
        "version": "1.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "total_images": len(labels),
            "dataset_root": str(root_path),
            "source": "XML migration"
        },
        "labels": labels
    }
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存 JSON 文件到 data/ 目录
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"迁移完成！共处理 {len(labels)} 个标签")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='迁移 XML 标签到 JSON')
    parser.add_argument('--root', default='data', help='数据集根目录')
    parser.add_argument('--output', default='data/labels.json', help='输出 JSON 文件路径')
    
    args = parser.parse_args()
    
    root_path = Path(args.root)
    output_path = Path(args.output)
    
    if not root_path.exists():
        print(f"错误: 根目录 {root_path} 不存在")
        exit(1)
    
    migrate_labels(root_path, output_path)
```

### 4. 使用方式

```bash
# 基本使用（默认输出到 data/labels.json）
python tools/migrate_labels.py

# 指定根目录
python tools/migrate_labels.py --root data

# 指定输出路径
python tools/migrate_labels.py --output data/my_labels.json

# 只处理部分数据（测试用）
python tools/migrate_labels.py --root data/lens_6/XL --output data/partial_labels.json
```

### 5. 验证工具

创建验证脚本检查迁移结果：

```python
#!/usr/bin/env python3
"""
验证迁移后的 JSON 标签文件
"""

import json
from pathlib import Path


def validate_labels(json_path: Path, root_path: Path):
    """验证标签文件的完整性"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"版本: {data.get('version')}")
    print(f"总标签数: {len(data.get('labels', {}))}")
    print(f"创建时间: {data.get('metadata', {}).get('created_at')}")
    
    # 检查随机样本
    labels = data.get('labels', {})
    sample_keys = list(labels.keys())[:5]
    
    print("\n样本检查:")
    for key in sample_keys:
        label = labels[key]
        print(f"  {key}: {label.get('meter_value')}")
        
        # 检查对应的图像文件是否存在
        image_path = root_path / key
        if image_path.exists():
            print(f"    ✓ 图像文件存在")
        else:
            print(f"    ✗ 图像文件缺失")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='验证 JSON 标签文件')
    parser.add_argument('--json', default='data/labels.json', help='JSON 标签文件路径')
    parser.add_argument('--root', default='data', help='数据集根目录')
    
    args = parser.parse_args()
    
    validate_labels(Path(args.json), Path(args.root))
```

## 实施步骤

### 第一阶段：迁移工具开发
1. 创建 `tools/migrate_labels.py` 迁移脚本
2. 创建 `tools/validate_labels.py` 验证脚本
3. 测试迁移功能

### 第二阶段：数据迁移
1. 运行迁移工具生成 `data/labels.json`
2. 验证迁移结果的完整性
3. 备份生成的 JSON 文件

### 第三阶段：后续规划（可选）
1. 创建 LabelManager 统一接口
2. 更新 MeterSet 使用 JSON 标签
3. 开发标签查看和编辑工具

## 注意事项

- ✅ **不删除原有 XML 文件**：迁移工具只读取不修改
- ✅ **保持向后兼容**：现有代码继续正常工作
- ✅ **增量更新**：可以多次运行迁移工具更新 JSON
- ✅ **错误处理**：跳过处理失败的文件，继续迁移其他文件
- ✅ **进度显示**：显示处理进度，便于监控
- ✅ **文件位置**：`labels.json` 保存在 `data/` 目录

## 文件位置

- 迁移工具：`tools/migrate_labels.py`
- 验证工具：`tools/validate_labels.py` 
- 输出文件：`data/labels.json`

这个方案首先专注于创建迁移工具，将分散的 XML 标签汇总到统一的 JSON 文件中，为后续的标签管理改进奠定基础。