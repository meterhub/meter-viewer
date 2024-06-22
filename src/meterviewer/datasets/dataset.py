# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

import os
import typing as t
import pathlib
import datetime
from tqdm import tqdm

# import numpy as np
import random

from ..imgs import img

from .. import files, types as T
from .view import view_dataset_in_rows, view_dataset, view_dataset_on_disk  # noqa
from .join import join_with_fix, join_with_resize  # noqa


def generate_func() -> t.List[t.Callable[[pathlib.Path], T.ImgDataset]]:
    funcs = []
    names: t.List[str] = [T.x_name, T.y_name, T.x_test, T.y_test]
    for n in names:

        def get_func(path: pathlib.Path, name: str = n):
            return files.load_from_disk(path / name)

        funcs.append(get_func)

    return funcs


def get_details(
    path: pathlib.Path,
    x: T.ImgDataset,
    y: T.LabelData,
) -> t.Dict:
    data = {}

    def create_sub(name):
        data[name] = {}

    for name in ["Dataset", "Meta"]:
        create_sub(name)

    data["Dataset"]["path"] = str(path)
    data["Meta"]["config.create_time"] = datetime.datetime.now()
    data["Dataset"]["created_time"] = ""
    data["Dataset"]["updated_time"] = ""
    data["Dataset"]["x_shape"] = x.shape
    data["Dataset"]["y_shape"] = y.shape
    return data


def show_details(
    get_x_train: t.Callable,
    get_y_train: t.Callable,
    get_details: t.Callable[[t.Any, t.Any], t.Dict],
    write_to_file: t.Callable[[t.Dict], None],
):
    x, y = get_x_train(), get_y_train()
    details = get_details(x, y)
    write_to_file(details)


def dataset_length_list() -> t.List[int]:
    return [5, 6, 7, 8]


def create_str_with_fill(
    number: int,
    length: int,
    total: int,
) -> T.DigitStr:
    return fill_digit(img.number_to_string(number, length), total)


def create_labels_func(
    length: int,
    total: int,
) -> t.Callable[[int], t.Tuple[t.List[int], t.List[T.DigitStr]]]:
    """total length"""

    def generate_nums(train_nums: int):
        numbers = []
        str_digits = []
        for _ in range(train_nums):
            number = random.randint(0, 10**length)
            numbers.append(number)
            str_digits.append(
                create_str_with_fill(number, length, total),
            )
        return numbers, str_digits

    return generate_nums


class GenBlockImgFunc(t.Protocol):
    def __call__(self, digit: T.DigitStr) -> T.Img: ...


class SaveDatasetFunc(t.Protocol):
    def __call__(self, imgs: T.ImgList, str_digits: t.List[T.DigitStr]) -> None: ...


class CreateDatasetFunc(t.Protocol):
    def __call__(
        self,
        length: int,
        nums: int,
        gen_block_img: GenBlockImgFunc,
    ) -> t.Tuple[t.List[T.Img], t.List[T.DigitStr]]: ...


def create_dataset_func(
    check_imgs: t.Callable[[T.ImgList], None],
    total: int,
) -> CreateDatasetFunc:
    """创建新的数据库"""

    def inner(
        length: int,
        nums: int,
        gen_block_img: GenBlockImgFunc,
    ):
        _, str_digits = create_labels_func(length, total)(nums)

        imgs = []
        for digit in tqdm(str_digits):
            im = gen_block_img(digit)
            imgs.append(im)

        # files.write_shape(imgs, 3)
        check_imgs(imgs)
        imgs = img.resize_imglist(imgs, size=[37, 297])
        return imgs, str_digits

    return inner


def get_random_dataset(
    root: pathlib.Path, get_dataset_list: t.Callable
) -> t.Tuple[pathlib.Path, int]:
    datasets = list(get_dataset_list(root))
    random_index = random.randint(0, len(datasets) - 1)
    return datasets[random_index], random_index


def generate_block_img(
    the_digit: T.DigitStr,
    join_func: T.JoinFunc,
    read_rand_img: t.Callable[[int | str], T.Img],
) -> T.Img:
    img_list = []
    for digit in the_digit:
        im = read_rand_img(digit)
        img_list.append(im)
    return join_func(img_list, img.size_check)


def get_dataset_path(root: pathlib.Path, dataset_name: str) -> pathlib.Path:
    p = root / "lens_6" / "XL" / "XL" / dataset_name
    return p


def get_dataset_list(
    root: pathlib.Path,
    default_func: t.Callable = lambda: pathlib.Path("lens_6/XL/XL"),
) -> t.Iterator[pathlib.Path]:
    root = root / default_func()
    for dir in os.listdir(root):
        if os.path.isdir(root / dir):
            yield pathlib.Path(dir)


def handle_datasets(root: pathlib.Path, handle_func: t.Callable[[pathlib.Path], None]):
    """handle"""
    for dataset in get_dataset_list(root):
        handle_func(dataset)


def fill_digit(digit: T.DigitStr, total_length: int) -> T.DigitStr:
    digit2 = digit.copy()
    if len(digit) < 5:
        raise ValueError(f"digit lenght must > 5, {digit}")

    if len(digit) <= total_length:
        digit2.extend(["x"] * (total_length - len(digit)))
    else:
        raise ValueError(f"digit lenght must < {total_length}, {digit}")
    return digit2
