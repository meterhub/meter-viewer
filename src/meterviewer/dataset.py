# 统一数据集表示
# 只在一个文件里修改目录，方便快捷

import os
import typing as t
from string import Template
import pathlib
import functools
from matplotlib import pyplot as plt
from . import img
from . import types as T


def create_dataset(
    root: pathlib.Path,
    train_nums: int,
    test_nums: int,
    save_method: t.Callable,
):
    # write meta config file.
    datasets = get_dataset_list(root)
    # dataset: M8L5XL

    num_len = [5, 6, 7, 8]
    for length in num_len:
        for num in range(10**length):
            str_digits = img.number_to_string(num, length)
            for digit in str_digits:
                for dataset in datasets:
                    im = read_rand_img(root, dataset, digit)


def read_rand_img(root: pathlib.Path, dataset: str | pathlib.Path, digit: int | str) -> T.Img:
    get_one = read_single_digt(lambda: root, path_fusion, dataset_name=str(dataset), num=int(digit))
    im = plt.imread(next(get_one()))
    return im


def path_fusion(root: pathlib.Path, dataset_name: str, num: int):
    p = root / "lens_6" / "XL" / "XL" / dataset_name / "Digit" / str(num)
    return p


def scan_pics(path: pathlib.Path) -> t.Iterator[pathlib.Path]:
    for p in path.iterdir():
        yield p


def get_dataset_list(root: pathlib.Path) -> t.Iterator[pathlib.Path]:
    for dir in os.listdir(root):
        if os.path.isdir(root / dir):
            yield pathlib.Path(dir)


def read_single_digt(get_root_path: t.Callable, path_fusion: t.Callable, dataset_name: str, num: int) -> t.Callable:
    assert num in range(0, 10), "num must be 0~9"
    p: pathlib.Path = get_root_path() / path_fusion(get_root_path(), dataset_name, num)
    return functools.partial(scan_pics, p)


def dataset():
    data = {}
    str_template = Template("$name_$peroid.npy")

    names = ["x", "y"]
    peroids = ["train", "test"]

    s = str_template.safe_substitute(name="train", peroid="2021")

    def get_root_path():
        pass
