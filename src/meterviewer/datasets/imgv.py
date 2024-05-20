"""view image and value"""

from meterviewer.datasets import dataset, config
from PIL import ImageFile
from pathlib import Path as P
from matplotlib import pyplot as plt

# 修复 PIL 无法读取截断图片的问题; matplotlib 底层居然是 PIL？是我搞错了吗？
ImageFile.LOAD_TRUNCATED_IMAGES = True


def view_one_img_v(filepath: P):
    """同时浏览图片和值"""
    im = plt.imread(str(filepath))
    v, rect = config.get_xml_config(filepath)
    return (im, v, rect)
