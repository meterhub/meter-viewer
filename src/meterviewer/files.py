import pathlib
import typing as t
import numpy as np
from . import types as T
import hashlib

import toml


def use_smart_name(dataset: pathlib.Path) -> T.NameFunc:
    x_name_list = ["x_train.npy", "x_all.npy", "x.npy"]
    y_name_list = ["y_train.npy", "y_all.npy", "y.npy"]

    for x, y in zip(x_name_list, y_name_list):
        if (dataset / pathlib.Path(x)).exists() and (dataset / pathlib.Path(y)).exists():

            def get_x_y():
                return x, y

            return get_x_y
    else:
        raise Exception("No valid npy files found")


def compute_md5(file_path, chunk_size=8192):
    """
    Compute the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.
        chunk_size (int): The size of each chunk to read from the file.

    Returns:
        str: The MD5 hash of the file in hexadecimal format.
    """
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def read_toml(filename: pathlib.Path) -> t.Optional[t.Dict]:
    try:
        with open(filename, "r") as f:
            data = toml.load(f)
            print(f"Read '{filename}' successfully.")
            return data
    except Exception as e:
        print(f"Error to read '{filename}': {e}")


def write_toml(filename: pathlib.Path, data):
    try:
        with open(filename, "w") as f:
            toml.dump(data, f)
        print(f"Data written to '{filename}' successfully.")
    except Exception as e:
        print(f"Error writing to '{filename}': {e}")


def write_shape(img: T.ImgList, nums: int = 3):
    debug_file = pathlib.Path("debug.log")
    with open(debug_file, "w") as f:
        for i in range(nums):
            f.write(f"img_{i} shape is: {img[i].shape}\n")


def scan_pics(path: pathlib.Path) -> t.Iterator[pathlib.Path]:
    """scan pics in path"""
    for p in path.iterdir():
        if p.suffix in [".jpg", ".png", ".jpeg"]:
            yield p


def transform_img(img: T.Img) -> T.Img:
    """reshape image (35,25,3) to (1, 35, 25, 3)"""
    return np.expand_dims(img, axis=0)


def transform_label(label: T.DigitStr) -> T.Label:
    label_ = [int(i) for i in label]
    return np.expand_dims(np.array(label_), axis=0)


def save_img_labels(
    imgs: t.List[T.Img], labels: t.List[T.DigitStr], prefix_name: pathlib.Path, save_to_disk: t.Callable
):
    imgs = [np.expand_dims(img, axis=0) for img in imgs]
    x_train = np.vstack(imgs)
    labels_ = [transform_label(label) for label in labels]
    y_train = np.vstack(labels_)

    save_to_disk(str(prefix_name / T.x_name), x_train)
    save_to_disk(str(prefix_name / T.y_name), y_train)


def save_to_disk(filename: str, data: np.ndarray):
    with open(filename, "wb") as f:
        np.save(f, data)


def load_from_disk(filename) -> np.ndarray:
    with open(filename, "rb") as f:
        return np.load(f)


def load_from_disk_with_md5(filename, with_md5: str) -> t.Tuple[np.ndarray, str]:
    md5 = ""
    if with_md5:
        md5 = compute_md5(filename)
    return load_from_disk(filename), md5
