# process image, to fit the training proposals.

import typing as t
import numpy as np

# from matplotlib import pyplot as plt
from . import types as T
from PIL import Image


def resize_img(img: T.Img, size: t.List[int]) -> T.Img:
    if not size:
        size = list(img.shape)
    return np.asarray(Image.fromarray(img).resize(size), dtype=np.uint8)


def resize_imglist(imglist: T.ImgList, size: t.Optional[t.List[int]] = None) -> T.ImgList:
    if not size:
        size = list(imglist[0].shape[:2])
    return [resize_img(img, size) for img in imglist]


def join_img(
    imglist: T.ImgList,
    check_func: t.Callable[[t.Any], t.Any],
) -> T.Img:
    # merge images vertically
    check_func(imglist)
    return np.hstack(imglist)


def size_check(img_list: t.List[T.Img], size: t.Optional[t.List[int]] = None):
    assert img_list != [], "img_list should not be empty"
    if not size:
        size = list(img_list[0].shape)

    for i, img in enumerate(img_list):
        if list(img.shape) != size:
            raise ValueError(f"image: {i} size: {img.shape}, not match size: {size}")


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


def empty_check(*args, **kwargs):
    """do nothing function"""
    pass


def gen_block_img(number: int, length: int):
    num_l = [int(i) for i in number_to_string(number, length)]
    return join_img(get_img_list(num_l), empty_check)
