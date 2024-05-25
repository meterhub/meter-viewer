"""handle function based on single, that is dataset_name/[0-9] format"""

import typing as t
import functools
import random
import pathlib
from .dataset import get_dataset_path
from meterviewer import files, T
from matplotlib import pyplot as plt


def path_fusion(root: pathlib.Path, dataset_name: str, num: int):
    """return single digit"""
    p = get_dataset_path(root, dataset_name) / "Digit" / str(num)
    return p


def read_rand_img(root: pathlib.Path, dataset: str | pathlib.Path, digit: int | str) -> T.Img:
    get_one = read_single_digt(lambda: root, path_fusion, dataset_name=str(dataset), num=int(digit))
    all_imgs = list(get_one())
    length = len(all_imgs)
    i = random.randint(0, length - 1)
    im = plt.imread(all_imgs[i])
    return im


def read_single_digt(
    get_root_path: t.Callable,
    path_fusion: t.Callable,
    dataset_name: str,
    num: int,
) -> t.Callable:
    assert num in range(0, 10), "num must be 0~9"
    p: pathlib.Path = get_root_path() / path_fusion(get_root_path(), dataset_name, num)
    return functools.partial(files.scan_pics, p)
