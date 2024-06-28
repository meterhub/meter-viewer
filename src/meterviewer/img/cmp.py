# compare two image
from meterviewer import types as T
import hashlib


def comp_ims(im1: T.Img, im2: T.Img):
    def compute_(im):
        return hashlib.md5(im.tobytes()).digest()
    return compute_(im1) == compute_(im2)
