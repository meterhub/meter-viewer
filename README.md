# Meterviewer

Meter Data viewer, not only to view multiple dataset via notebook.

## Features

1. Meter Image generation.

- `./examples/playground/generate_1/main.py`
- `./examples/notebooks/generate-op-v2.ipynb`

2. Generate jsondb for meter dataset.

- `./examples/generate_jsondb/main.ipynb`

3. Generate sqlite.db for meter dataset.

- `./examples/generate_db/create_all.py`

## Install

`pip install meterviewer`

## Development

我们使用 [uv](https://github.com/astral-sh/uv) 来管理项目。

- 要安装 uv，运行 `python3 -m pip install uv`。
- 要安装依赖，运行 `uv sync`。

## Documentation

We use [sphinx](https://www.sphinx-doc.org/en/master/) for documentation.

## Notes

1. Pure functional is critial. Less things to worry about.


## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
