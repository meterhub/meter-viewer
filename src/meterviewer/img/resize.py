from __future__ import annotations
import typing as t

import numpy as np
from PIL import Image

from meterviewer import types as T


def resize_img(img: T.Img, size: T.ImgSize) -> T.Img:
    # resize will reverse the size. height -> weight, weight -> height
    im = np.asarray(Image.fromarray(img).resize(list(reversed(size))), dtype=np.uint8)
    assert list(im.shape[:2]) == list(size), (im.shape, size)
    return im


def resize_imglist(
    imglist: T.ImgList,
    size: t.Optional[T.ImgSize] = None,
) -> T.ImgList:
    if not size:
        size = list(imglist[0].shape[:2])
    return [resize_img(img, size) for img in imglist]


def check_img_size(
    img: T.Img, size: t.Tuple[int, int], then: t.Callable[[T.Img], t.Any]
) -> bool | t.Any:
    if img.shape == size:
        return then(img)
    return False


def size_check(img_list: t.List[T.Img], size: t.Optional[t.List[int]] = None):
    assert img_list != [], "img_list should not be empty"
    if not size:
        size = list(img_list[0].shape)

    for i, img in enumerate(img_list):
        if list(img.shape) != size:
            raise ValueError(f"image: {i} size: {img.shape}, not match size: {size}")
