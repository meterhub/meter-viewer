# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

import os
import typing as t
import pathlib
import datetime
import functools

# import numpy as np
from matplotlib import pyplot as plt
import random

from . import img, files, types as T


def get_data(path: pathlib.Path, name: str):
    return files.load_from_disk(path / name)


def generate_func() -> t.List[t.Callable[[pathlib.Path], T.ImgDataset]]:
    funcs = []
    names: t.List[str] = [T.x_name, T.y_name, T.x_test, T.y_test]
    for n in names:

        def get_func(path: pathlib.Path, name: str = n):
            return get_data(path, name)

        funcs.append(get_func)

    return funcs


get_x_train, get_y_train, get_x_test, get_y_test = generate_func()


def get_details(path: pathlib.Path, x: T.ImgDataset, y: T.LabelData) -> t.Dict:
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
    get_x_train,
    get_y_train,
    get_details,
    write_to_file: t.Callable[[t.Any], None],
):
    x = get_x_train()
    y = get_y_train()
    details = get_details(x, y)
    write_to_file(details)


def view_dataset_on_disk(name: str):
    def mmm(
        prefix_name: pathlib.Path,
        load_from_disk: t.Callable,
        view_dataset: t.Callable,
        show: bool = True,
        nums: int = 3,
    ):
        if not show:
            return

        assert prefix_name.exists()
        x = load_from_disk(prefix_name / name)
        x = img.np_to_img(x)
        view_dataset(nums, x)

    return mmm

view_dataset_on_disk_train = view_dataset_on_disk(T.x_name)
view_dataset_on_disk_test = view_dataset_on_disk(T.x_test)


def view_dataset_in_rows(num: int, imglist: T.ImgList):
    # 创建一个 GridSpec 实例，1行3列
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(15, 5))
    gs = GridSpec(1, 3, figure=fig)

    # 第一个子图
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(imglist[0])

    # 第二个子图
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(imglist[1])

    # 第三个子图
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.imshow(imglist[2])

    plt.tight_layout()
    plt.show()


def view_dataset(num: int, imglist: T.ImgList):
    for im in imglist[:num]:
        plt.imshow(im)
        plt.show()


def join_with_fix(imglist: T.ImgList, check_func: t.Callable, fix_func: t.Callable) -> T.Img:
    """修饰 join_func"""
    # merge images horizontally
    try:
        return img.join_img(imglist, check_func)
    except ValueError as e:
        print(e)
        imglist = fix_func(imglist)
    return img.join_img(imglist, check_func)


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


def create_dataset(
    check_imgs: t.Callable[[T.ImgList], None],
):
    def inner(
        length: int,
        nums: int,
        gen_block_img: t.Callable[[T.DigitStr], T.Img],
        save_dataset: t.Callable[[T.ImgList, t.List[T.DigitStr]], None],
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


def read_single_digt(
    get_root_path: t.Callable,
    path_fusion: t.Callable,
    dataset_name: str,
    num: int,
) -> t.Callable:
    assert num in range(0, 10), "num must be 0~9"
    p: pathlib.Path = get_root_path() / path_fusion(get_root_path(), dataset_name, num)
    return functools.partial(files.scan_pics, p)


join_with_resize: T.JoinFunc = functools.partial(join_with_fix, fix_func=img.resize_imglist)
