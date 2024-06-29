from meterviewer import types as T
import numpy as np
from PIL import Image


def to_gray(im: T.Img) -> T.Img:
    im = Image.fromarray(im).convert("L")
    return np.asarray(im)
