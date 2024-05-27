import numpy as np
from meterviewer import img
from PIL import Image


def test_gen_pics():
    im = np.zeros([30, 120, 3], dtype=np.uint8)
    im = Image.fromarray(im)
    filename = "/tmp/test.png"
    im.save(filename)
    img.show_img(im, is_stop=False)
