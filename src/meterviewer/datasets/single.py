"""handle function based on single, that is dataset_name/[0-9] format"""

import typing as t
import functools
import random
import pathlib
from .dataset import get_dataset_path
from meterviewer import files, T
from meterviewer import func, img
from matplotlib import pyplot as plt


def path_fusion(
    root: pathlib.Path,
    dataset_name: str,
    num: int,
):
    """return single digit"""
    p = get_dataset_path(root, dataset_name) / "Digit" / str(num)
    return p


def read_rand_img(
    root: pathlib.Path,
    get_dataset: t.Callable[[], str | pathlib.Path],
    digit: int | str,
    promise=False,
) -> T.Img:
    if digit == "x":
        im = img.gen_empty_im((32, 40, 3))
        return im

    get_one = read_single_digit(
        root,
        get_dataset=get_dataset,
        num=int(digit),
        promise=promise,
    )
    all_imgs = list(get_one())
    length = len(all_imgs)
    i = random.randint(0, length - 1)
    im = plt.imread(all_imgs[i])
    return im


def read_single_digit(
    root_path: pathlib.Path,
    get_dataset: t.Callable[[], str | pathlib.Path],
    num: int,
    promise: bool,
):
    """promised return"""
    assert num in range(0, 10), "num must be 0~9"

    def might_fail_func() -> pathlib.Path:
        return path_fusion(root_path, str(get_dataset()), num)

    if promise:
        p = func.try_again(15, might_fail_func, lambda p: p.exists(), fail_message=f"cannot num: {num}")
    else:
        p = might_fail_func()

    return functools.partial(files.scan_pics, p)
