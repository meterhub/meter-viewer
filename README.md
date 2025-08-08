# MeterViewer - 仪表数据集处理工具

[![PyPI Version](https://img.shields.io/pypi/v/meterviewer)](https://pypi.org/project/meterviewer/)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 处理仪表格式数据集的Python工具库，支持生成、查看和管理仪表数据集。

## 功能特性
- **仪表图像生成**：创建标准化仪表图像数据集
- **数据集管理**：支持JSON/SQLite数据库生成
- **可视化工具**：Jupyter Notebook集成
- **数据验证**：确保数据集格式正确性

## 安装
```bash
pip install meterviewer
```

## 快速开始
```python
from meterviewer import generate_dataset, view_meter

# 生成仪表数据集
dataset = generate_dataset(config="dataset-config.toml")

# 可视化仪表数据
view_meter(dataset[0])
```

## 文档
- [在线文档](https://meterhub.github.io/meter-viewer)
- 本地构建：`cd docs && make html`

## 示例
- [图像生成示例](./examples/notebooks/generate-op-v2.ipynb)
- [数据集分析示例](./examples/notebooks/view_dataset.ipynb)
- [JSON数据库生成](./examples/generate_jsondb/main.ipynb)

## 开发指南
```bash
# 安装开发依赖
uv sync --group dev

# 运行测试
pytest tests/

# 代码检查
ruff check . --fix
```

## 贡献
欢迎提交Issue和PR！详见[贡献指南](CONTRIBUTING.md)

## 许可证
[MIT](LICENSE) © 2025 svtter
