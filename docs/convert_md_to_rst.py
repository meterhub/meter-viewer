import os
import shutil
from pathlib import Path

from m2r2 import convert


def convert_md_to_rst(source_dir, target_dir):
  """将指定目录下的所有 Markdown 文件转换为 RST 格式"""
  source_path = Path(source_dir)
  target_path = Path(target_dir)

  # 确保目标目录存在
  target_path.mkdir(parents=True, exist_ok=True)

  # 遍历源目录中的所有文件
  for md_file in source_path.rglob("*.md"):
    # 计算相对路径
    relative_path = md_file.relative_to(source_path)
    # 创建目标文件路径
    rst_file = target_path / relative_path.with_suffix(".rst")

    # 确保目标文件的父目录存在
    rst_file.parent.mkdir(parents=True, exist_ok=True)

    # 转换文件内容
    with md_file.open("r", encoding="utf-8") as f:
      md_content = f.read()
    rst_content = convert(md_content)

    # 写入转换后的内容
    with rst_file.open("w", encoding="utf-8") as f:
      f.write(rst_content)

    print(f"Converted {md_file} -> {rst_file}")


def main():
  # 获取脚本所在目录
  script_dir = Path(__file__).parent

  # 源文档目录（原始的 markdown 文件目录）
  source_dir = script_dir / "docs"
  # 目标目录（sphinx source 目录）
  target_dir = script_dir / "source"

  # 如果目标目录已存在，先删除
  if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

  # 转换文件
  convert_md_to_rst(source_dir, target_dir)

  # 复制其他必要的文件（如图片等）
  for item in os.listdir(source_dir):
    source_item = os.path.join(source_dir, item)
    if os.path.isfile(source_item) and not item.endswith(".md"):
      target_item = os.path.join(target_dir, item)
      shutil.copy2(source_item, target_item)
      print(f"Copied {source_item} -> {target_item}")


if __name__ == "__main__":
  main()
