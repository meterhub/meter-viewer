"""view image and value"""

from meterviewer.datasets import dataset, config
from pathlib import Path as P
from matplotlib import pyplot as plt


def view_one_img_v(filepath: P):
    im = plt.imread(filepath)
    return (im,)
