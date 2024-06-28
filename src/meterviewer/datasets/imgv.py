"""view image and value"""

import typing as t
from pathlib import Path as P

from loguru import logger
from matplotlib import pyplot as plt
from PIL import ImageFile

from meterviewer import T
from meterviewer.datasets import config
from meterviewer.img import cmp

logger.add("./logs/meterviewer-proc.log")

# 修复 PIL 无法读取截断图片的问题; matplotlib 底层居然是 PIL？是我搞错了吗？
ImageFile.LOAD_TRUNCATED_IMAGES = True


def view_one_img_v(filepath: P) -> t.Tuple[T.Img, str, T.Rect]:
    """同时浏览图片和值"""
    im = plt.imread(str(filepath))
    v, rect = config.get_xml_config(filepath)
    return (im, v, rect)


hash_store = {}


def save_hash(im: T.Img, index: int):
    hash = cmp.get_hash(im)
    res = hash_store.get(hash, None)
    if res is None:
        hash_store[hash] = index
    else:
        logger.error(f"Hash: {hash} is same with {res} and {index}")
        raise Exception("Img should not be same.")


def find_files(img_list: T.ImgList):
    for i, img in enumerate(img_list):
        save_hash(img, i)
