# process image, to fit the training proposals.

from __future__ import annotations
import sys
import typing as t
import numpy as np

# from matplotlib import pyplot as plt
from .. import types as T
from .resize import resize_img, resize_imglist, size_check, check_img_size  # noqa
from matplotlib import pyplot as plt


def np_to_img(data: np.ndarray) -> T.ImgList:
    return list(data)


def join_img(
    imglist: T.ImgList,
    check_func: t.Callable[[t.Any], t.Any],
) -> T.Img:
    # merge images vertically
    check_func(imglist)
    return np.hstack(imglist)


def get_random_img(num: int, img_from: t.Callable) -> T.Img:
    """get random img
    num: digit num of img
    """
    get_img = img_from()
    return get_img(num)


def img_from(folder: str = ""):
    # open folder to get all images.
    def get_img(num):
        return np.random.randint(1, 255, size=(10, 20))

    return get_img


def get_img_list(nums: t.List[int]) -> t.List[T.Img]:
    imgs = []
    for i in nums:
        imgs.append(get_random_img(int(i), lambda: None))
    return imgs


def number_to_string(number: int, length: int) -> t.List[str]:
    # create a string list from number, with fixed length.
    return list(str(number).zfill(length))


def empty_check(*args, **kwargs):
    """do nothing function"""
    pass


def gen_block_img(number: int, length: int):
    """inside memory to generate, use as a sample function."""
    num_l = [int(i) for i in number_to_string(number, length)]
    return join_img(get_img_list(num_l), empty_check)


def show_img(img, is_stop):
    plt.imshow(img)
    plt.show()
    if is_stop:
        sys.exit(-1)


def gen_empty_im(size: t.Tuple[int, int, int]):
    return np.zeros(size, dtype=np.uint8)
