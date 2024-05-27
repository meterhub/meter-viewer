# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

import os
import typing as t
import pathlib
import datetime
import functools

# import numpy as np
import random

from .. import img, files, types as T
from .view import view_dataset_in_rows, view_dataset, view_dataset_on_disk  # noqa


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


GenBlockImgFunc = t.Callable[[T.DigitStr], T.Img]
SaveDatasetFunc = t.Callable[[T.ImgList, t.List[T.DigitStr]], None]


def create_dataset_func(
    check_imgs: t.Callable[[T.ImgList], None],
) -> t.Callable[[int, int, GenBlockImgFunc, SaveDatasetFunc], None]:
    """创建新的数据库"""

    def inner(
        length: int,
        nums: int,
        gen_block_img: GenBlockImgFunc,
        save_dataset: SaveDatasetFunc,
    ):
        create_label = create_labels_func(length)
        _, str_digits = create_label(nums)

        imgs = []
        for digit in str_digits:
            im = gen_block_img(digit)
            imgs.append(im)

        # files.write_shape(imgs, 3)
        check_imgs(imgs)
        imgs = img.resize_imglist(imgs)
        save_dataset(imgs, str_digits)

    return inner


def get_random_dataset(root: pathlib.Path, get_dataset_list: t.Callable) -> t.Tuple[pathlib.Path, int]:
    datasets = list(get_dataset_list(root))
    random_index = random.randint(0, len(datasets) - 1)
    return datasets[random_index], random_index


def generate_block_img(
    the_digit: T.DigitStr,
    root_path: pathlib.Path,
    join_func: T.JoinFunc,
    get_dataset: t.Callable[[], str | pathlib.Path],
    read_rand_img: t.Callable[[pathlib.Path, str | pathlib.Path, int | str], T.Img],
) -> T.Img:
    img_list = []
    for digit in the_digit:
        im = read_rand_img(root_path, get_dataset(), digit)
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


def join_with_fix(imglist: T.ImgList, check_func: t.Callable, fix_func: t.Callable) -> T.Img:
    """修饰 join_func"""
    # merge images horizontally
    try:
        return img.join_img(imglist, check_func)
    except ValueError as e:
        print(e)
        imglist = fix_func(imglist)
    return img.join_img(imglist, check_func)


join_with_resize: T.JoinFunc = functools.partial(join_with_fix, fix_func=img.resize_imglist)
# def walk_dataset(dataset: str) -> t.Iterator[T.Img, T.DigitStr]:
#     """get img and dataset"""
#     pass
