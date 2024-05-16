# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

import os
import typing as t
from string import Template
import pathlib
import functools
import numpy as np
from matplotlib import pyplot as plt
import random

from . import img, files, types as T


def join_with_fix(imglist: T.ImgList, check_func: t.Callable, fix_func: t.Callable) -> T.Img:
    # merge images horizontally
    try:
        return img.join_img(imglist, check_func)
    except ValueError as e:
        print(e)
        imglist = fix_func(imglist)
    return img.join_img(imglist, check_func)


def create_datasets(
    root: pathlib.Path,
    train_nums: int,
    test_nums: int,
    get_dataset_list: t.Callable,
):
    # write meta config file.
    # dataset: M8L5XL
    datasets = get_dataset_list(root)

    for length in [5, 6, 7, 8]:
        # block_imgs = generate_block_img(root, str_digits, get_dataset)
        raise Exception("not implement.")


def create_labels_func(
    length: int,
) -> t.Callable[[int], t.Tuple[t.List[int], t.List[T.DigitStr]]]:
    def generate_nums(train_nums: int):
        numbers = []
        str_digits = []
        for _ in range(train_nums):
            number = random.randint(0, 10**length)
            numbers.append(number)
            str_digits.append(img.number_to_string(number, length))
        return numbers, str_digits

    return generate_nums


def create_dataset(
    lenght: int,
    nums: int,
    gen_block_img: t.Callable[[T.DigitStr], T.Img],
    save_dataset: t.Callable,
):
    create_label = create_labels_func(lenght)
    _, str_digits = create_label(nums)

    imgs = []
    for digit in str_digits:
        im = gen_block_img(digit)
        imgs.append(im)

    save_dataset(imgs, str_digits)


def get_random_dataset(root: pathlib.Path, get_dataset_list: t.Callable) -> t.Tuple[pathlib.Path, int]:
    datasets = list(get_dataset_list(root))
    random_index = random.randint(0, len(datasets) - 1)
    return datasets[random_index], random_index


def generate_block_img(
    root_path: pathlib.Path,
    the_digit: t.List[str],
    join_func: T.JoinFunc,
    get_dataset: t.Callable,
) -> T.Img:
    img_list = []
    for digit in the_digit:
        im = read_rand_img(root_path, get_dataset(), digit)
        img_list.append(im)
    return join_func(img_list, img.size_check)


def read_rand_img(root: pathlib.Path, dataset: str | pathlib.Path, digit: int | str) -> T.Img:
    get_one = read_single_digt(lambda: root, path_fusion, dataset_name=str(dataset), num=int(digit))
    im = plt.imread(next(get_one()))
    return im


def path_fusion(root: pathlib.Path, dataset_name: str, num: int):
    p = root / "lens_6" / "XL" / "XL" / dataset_name / "Digit" / str(num)
    return p


def get_dataset_list(root: pathlib.Path) -> t.Iterator[pathlib.Path]:
    for dir in os.listdir(root):
        if os.path.isdir(root / dir):
            yield pathlib.Path(dir)


def read_single_digt(get_root_path: t.Callable, path_fusion: t.Callable, dataset_name: str, num: int) -> t.Callable:
    assert num in range(0, 10), "num must be 0~9"
    p: pathlib.Path = get_root_path() / path_fusion(get_root_path(), dataset_name, num)
    return functools.partial(files.scan_pics, p)
