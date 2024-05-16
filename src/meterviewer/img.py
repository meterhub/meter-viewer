# process image, to fit the training proposals.

import typing as t
import numpy as np
from . import types as T


def join_img(imglist: t.List[T.Img], check_func: t.Callable) -> T.Img:
    # merge images vertically
    check_func()
    return np.hstack(imglist)


def get_random_img(num: int, img_from: t.Callable) -> T.Img:
    """get random img
    num: digit num of img
    """
    get_img = img_from()
    return get_img(num)


def check_img_size(img: T.Img, size: t.Tuple[int, int], then: t.Callable[[T.Img], t.Any]) -> bool | t.Any:
    if img.shape == size:
        return then(img)
    return False


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


def empty_check():
    """do nothing function"""
    pass


def gen_block_img(number: int, length: int):
    num_l = [int(i) for i in number_to_string(number, length)]
    return join_img(get_img_list(num_l), empty_check)
