# 工具目录

本目录包含用于数据管理和迁移的工具脚本。

## 迁移工具

### migrate_labels.py

将分散的 XML 标签文件迁移到统一的 JSON 文件中。

**功能:**
- 扫描指定目录下的所有图像文件
- 从对应的 XML 文件中提取标签信息
- 生成包含所有标签的统一 JSON 文件
- 保持原有 XML 文件不变
- 支持进度显示和错误处理

**使用方式:**
```bash
# 基本使用（默认参数）
uv run python tools/migrate_labels.py

# 指定根目录和输出文件
uv run python tools/migrate_labels.py --root data --output data/labels.json

# 只处理部分数据（测试用）
uv run python tools/migrate_labels.py --root data/lens_6/XL --output data/partial_labels.json
```

**参数:**
- `--root`: 数据集根目录（默认: data）
- `--output`: 输出 JSON 文件路径（默认: data/labels.json）

### validate_labels.py

验证迁移后的 JSON 标签文件的完整性和正确性。

**功能:**
- 检查 JSON 文件结构
- 验证标签数量是否匹配
- 检查样本数据的正确性
- 验证图像文件是否存在
- 生成详细的验证报告

**使用方式:**
```bash
# 基本使用（默认参数）
uv run python tools/validate_labels.py

# 指定 JSON 文件和根目录
uv run python tools/validate_labels.py --json data/labels.json --root data
```

**参数:**
- `--json`: JSON 标签文件路径（默认: data/labels.json）
- `--root`: 数据集根目录（默认: data）

## 使用流程

1. **运行迁移工具:**
   ```bash
   uv run python tools/migrate_labels.py
   ```

2. **验证迁移结果:**
   ```bash
   uv run python tools/validate_labels.py
   ```

3. **检查输出文件:**
   - 生成的 `data/labels.json` 文件
   - 验证报告输出

## 注意事项

- 迁移工具需要读取项目中的 `meterviewer` 模块
- 确保在项目根目录运行脚本
- 工具会跳过处理失败的文件，继续处理其他文件
- 生成的 JSON 文件包含完整的标签信息，便于后续处理

## 文件结构

迁移后的 JSON 文件包含以下结构：

```json
{
  "version": "1.0",
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "total_images": 15000,
    "successful_migrations": 14900,
    "failed_migrations": 100,
    "dataset_root": "/path/to/data"
  },
  "labels": {
    "image/path/1.jpg": {
      "meter_value": "123456",
      "rect": {"xmin": 100, "ymin": 50, "xmax": 300, "ymax": 200},
      "digits": [...],
      "source_xml": "path/to/xml/file.xml"
    }
  }
}
```