# compare two image
from meterviewer import types as T
import hashlib


def comp_ims(im1: T.Img, im2: T.Img) -> bool:
    return get_hash(im1) == get_hash(im2)


def get_hash(img: T.Img) -> bytes:
    return hashlib.md5(img.tobytes()).digest()