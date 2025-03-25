from __future__ import annotations
import random
from meterviewer.config import get_root_path
import pathlib
import toml
import cv2
import numpy as np
from typing import Optional

def load_config(config_path: pathlib.Path) -> dict:
    """
    加载配置文件。
    Args:
        config_path: 配置文件路径。
    Returns:
        配置文件内容字典。
    """
    with open(config_path, "r") as f:
        config = toml.load(f)
    return config

def choose_random_image(dataset_path: pathlib.Path) -> pathlib.Path:
    """
    从指定的文件夹中随机选择一张图片。
    Args:
        dataset_path: 文件夹路径。
    Returns:
        随机图片的路径。
    """
    root_path = get_root_path()
    images_path = root_path / dataset_path / "ImageSets_block_zoom"
    if not images_path.exists():
        raise FileNotFoundError(f"The folder {images_path} does not exist.")
    
    image_files = list(images_path.glob("*.jpg"))  # 查找JPG格式的图片
    if not image_files:
        raise FileNotFoundError(f"No images found in {images_path}.")
    
    return random.choice(image_files)

def resize_image(image_path: pathlib.Path, size: tuple[int, int] = (201, 34)) -> np.ndarray:
    """
    调整图片尺寸。
    Args:
        image_path: 图片路径。
        size: 调整后的尺寸，默认是(201, 34)。
    Returns:
        调整后的图片。
    """
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Failed to load image from {image_path}.")
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    return resized_image

def show_image(image: np.ndarray, window_name: str = "Image"):
    """
    显示图片。
    Args:
        image: 要显示的图片。
        window_name: 窗口名称。
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(config_path: str):
    """
    主函数，加载配置文件并随机读取和调整图片尺寸。
    Args:
        config_path: 配置文件路径。
    """
    config_path = pathlib.Path(config_path)
    config = load_config(config_path)
    
    dataset_list = config.get("generate_config", {}).get("dataset", [])
    if not dataset_list:
        raise ValueError("No datasets found in the configuration file.")
    
    # 随机选择一个数据集路径
    dataset_path = pathlib.Path(random.choice(dataset_list))
    
    # 随机选择图片并调整尺寸
    image_path = choose_random_image(dataset_path)
    resized_image = resize_image(image_path)
    
    # 显示调整后的图片
    show_image(resized_image, window_name="Resized Image")

if __name__ == "__main__":
    # 修改为你的配置文件路径
    config_path = r"D:\Files\Code\2024Master\Xiu\meter-viewer-main\notebooks\dataset-gen copy.toml"
    main(config_path)
